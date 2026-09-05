#!/usr/bin/env python3
"""Weaken-the-transformer crossover experiment.

Compares TF-IDF+LogisticRegression against three deliberately-weakened
transformer arms (DistilBERT truncated to 8/16 tokens, and bert-tiny) on
tweet_eval and rotten_tomatoes, across a training-size grid, to look for a
genuine finite empirical crossover n*. Where a crossover exists, runs the
label-free Good-Turing/Chao1 coverage-curve predictor (calibrate on one
domain, predict on another) per the protocol in research_out.json.

CPU-only (4 cores, no GPU). Because full-grid transformer fine-tuning is
prohibitively slow on CPU, the grid is PRE-DEGRADED relative to the plan's
maximal spec, following the fallback_plan's stated priority order exactly:
drop n=1500/2000 first, then extra seeds beyond 3, then the distilbert_full
reference arm -- before ever dropping a domain or a truncation/tiny arm.
This pre-degradation is logged explicitly in the output.
"""

from __future__ import annotations

import gc
import json
import random
import resource
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger
from scipy import stats as sstats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKDIR = Path(__file__).parent
DATA_PATH = WORKDIR.parent.parent.parent / "iter_1" / "gen_art" / "gen_art_dataset_1" / "full_data_out.json"
OUT_PATH = WORKDIR / "method_out.json"

# ---------------------------------------------------------------------------
# RAM guard (aii-use-hardware): container limit is 29GB; budget generously
# below that since transformer weights + activations are the dominant cost.
# ---------------------------------------------------------------------------
RAM_BUDGET_BYTES = 20 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 1, RAM_BUDGET_BYTES * 1))

# ---------------------------------------------------------------------------
# Experiment configuration (pre-degraded from the artifact plan's maximal
# grid; see module docstring and DEGRADATION_LOG below).
# ---------------------------------------------------------------------------
DOMAINS = ["tweet_eval", "rotten_tomatoes"]
N_GRID_FULL_PLAN = [50, 100, 200, 500, 1000, 1500, 2000]
N_GRID = [50, 100, 200, 500, 1000]  # dropped 1500, 2000 first (fallback_plan priority 1)
SEEDS = [0, 1, 2]  # 3 seeds kept (fallback_plan: keep >=3 minimum)
MODEL_VARIANTS = ["tfidf_lr", "bert_tiny", "distilbert_trunc8", "distilbert_trunc16"]
# distilbert_full dropped entirely (fallback_plan priority 3: "not needed for
# the crossover-finding purpose, only informative context")
WEAKENED_VARIANTS = ["bert_tiny", "distilbert_trunc8", "distilbert_trunc16"]

TFIDF_HPARAMS = {"ngram_range": (1, 2), "max_features": 20000, "min_df": 1}
LR_HPARAMS = {"C": 1.0, "penalty": "l2", "solver": "liblinear", "max_iter": 1000}
TRANSFORMER_HPARAMS = {
    "n_epochs": 3,
    "learning_rate": 3e-5,
    "batch_size": 16,
    "optimizer": "AdamW",
    "warmup_ratio": 0.1,
    "weight_decay": 0.01,
}
MODEL_CHECKPOINTS = {
    "bert_tiny": "prajjwal1/bert-tiny",
    "distilbert_trunc8": "distilbert-base-uncased",
    "distilbert_trunc16": "distilbert-base-uncased",
}
MAX_LENGTHS = {"bert_tiny": 32, "distilbert_trunc8": 8, "distilbert_trunc16": 16}

TIME_BUDGET_S = 3.0 * 3600  # main sweep wall-clock budget; leaves margin for
# env setup (already spent), predictor calc, and writeup within the overall
# 6h nominal / ~5.9h actually-remaining budget for this run.
PILOT_SIZES = [100, 200, 400]
COVERAGE_N_GRID = [50, 100, 200, 400, 800, 1600, 3200]
B_BOOTSTRAP = 100
F2_INSTABILITY_THRESHOLD = 10
LAPLACE_SMOOTH = 0.5

DEGRADATION_LOG: list[dict[str, Any]] = [
    {
        "reason": "pre_degradation_before_run",
        "detail": (
            "Full plan grid is 7 n-values x 5 seeds x 5 model-variants x 2 domains "
            "= 350 model-fit cells, of which ~280 require transformer fine-tuning "
            "on CPU-only hardware (4 cores, no GPU). This is infeasible within the "
            "compute budget. Applying fallback_plan's stated degradation priority "
            "BEFORE starting: (1) drop n=1500 and n=2000 from the grid; (2) keep "
            "exactly 3 seeds (drop seeds 3,4); (3) drop the distilbert_full "
            "reference arm entirely. Domains and the three weakened arms "
            "(the actual object of study) are NOT dropped."
        ),
        "n_grid_used": N_GRID,
        "n_grid_dropped": [n for n in N_GRID_FULL_PLAN if n not in N_GRID],
        "seeds_used": SEEDS,
        "model_variants_used": MODEL_VARIANTS,
        "model_variants_dropped": ["distilbert_full"],
    }
]


def set_all_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    import torch

    torch.manual_seed(seed)


def load_domain_data(data: dict, domain: str) -> dict[str, list[dict]]:
    group = next(g for g in data["datasets"] if g["dataset"] == domain)
    out: dict[str, list[dict]] = {"val": [], "test": [], "train": [], "unlabeled_pool": []}
    for row in group["examples"]:
        out[row["metadata_split"]].append(row)
    return out


def nested_train_subset(train_rows: list[dict], n: int) -> list[dict]:
    subset = [r for r in train_rows if r.get("metadata_train_min_n") is not None and r["metadata_train_min_n"] <= n]
    return subset


def fit_eval_tfidf_lr(train_rows: list[dict], val_rows: list[dict], test_rows: list[dict], seed: int) -> dict:
    x_train = [r["input"] for r in train_rows]
    y_train = [int(r["output"]) for r in train_rows]
    vec = TfidfVectorizer(**TFIDF_HPARAMS)
    xt = vec.fit_transform(x_train)
    clf = LogisticRegression(random_state=seed, **LR_HPARAMS)
    clf.fit(xt, y_train)
    x_val = vec.transform([r["input"] for r in val_rows])
    x_test = vec.transform([r["input"] for r in test_rows])
    val_acc = clf.score(x_val, [int(r["output"]) for r in val_rows])
    test_acc = clf.score(x_test, [int(r["output"]) for r in test_rows])
    return {"val_acc": val_acc, "test_acc": test_acc}


def fit_eval_transformer(model_variant: str, train_rows: list[dict], val_rows: list[dict], test_rows: list[dict], seed: int) -> dict:
    import torch
    from torch.utils.data import DataLoader, Dataset
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

    torch.set_num_threads(4)
    set_all_seeds(seed)
    ckpt = MODEL_CHECKPOINTS[model_variant]
    max_len = MAX_LENGTHS[model_variant]
    tok = AutoTokenizer.from_pretrained(ckpt)
    model = AutoModelForSequenceClassification.from_pretrained(ckpt, num_labels=2)
    device = torch.device("cpu")
    model.to(device)

    class TxtDS(Dataset):
        def __init__(self, rows):
            self.texts = [r["input"] for r in rows]
            self.labels = [int(r["output"]) for r in rows]

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, i):
            return self.texts[i], self.labels[i]

    def collate(batch):
        texts, labels = zip(*batch)
        enc = tok(list(texts), padding="max_length", truncation=True, max_length=max_len, return_tensors="pt")
        enc["labels"] = torch.tensor(labels, dtype=torch.long)
        assert enc["input_ids"].shape[1] <= max_len, "tokenized length exceeds configured max_length"
        return enc

    bs = TRANSFORMER_HPARAMS["batch_size"]
    train_loader = DataLoader(TxtDS(train_rows), batch_size=bs, shuffle=True, collate_fn=collate, generator=torch.Generator().manual_seed(seed))
    n_epochs = TRANSFORMER_HPARAMS["n_epochs"]
    total_steps = max(1, len(train_loader) * n_epochs)
    optimizer = torch.optim.AdamW(model.parameters(), lr=TRANSFORMER_HPARAMS["learning_rate"], weight_decay=TRANSFORMER_HPARAMS["weight_decay"])
    n_warmup = int(TRANSFORMER_HPARAMS["warmup_ratio"] * total_steps)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=n_warmup, num_training_steps=total_steps)

    model.train()
    nan_loss_detected = False
    for _epoch in range(n_epochs):
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            if torch.isnan(loss):
                nan_loss_detected = True
                continue
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

    def evaluate(rows: list[dict]) -> float:
        model.eval()
        correct = 0
        loader = DataLoader(TxtDS(rows), batch_size=32, shuffle=False, collate_fn=collate)
        with torch.no_grad():
            for batch in loader:
                labels = batch.pop("labels")
                batch = {k: v.to(device) for k, v in batch.items()}
                logits = model(**batch).logits
                preds = torch.argmax(logits, dim=-1)
                correct += (preds.cpu() == labels).sum().item()
        return correct / len(rows)

    val_acc = evaluate(val_rows)
    test_acc = evaluate(test_rows)
    del model, optimizer, scheduler, train_loader
    gc.collect()
    return {"val_acc": val_acc, "test_acc": test_acc, "nan_loss_detected": nan_loss_detected}


def run_main_sweep(all_domain_data: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    results: list[dict] = []
    degradations: list[dict] = list(DEGRADATION_LOG)
    start_time = time.time()

    def remaining_time() -> float:
        return TIME_BUDGET_S - (time.time() - start_time)

    cells = [(d, mv, n, s) for d in DOMAINS for mv in MODEL_VARIANTS for n in N_GRID for s in SEEDS]
    n_cells = len(cells)
    logger.info(f"Main sweep: {n_cells} cells over domains={DOMAINS}, variants={MODEL_VARIANTS}, n_grid={N_GRID}, seeds={SEEDS}")

    ckpt_path = WORKDIR / "method_out_partial.jsonl"
    cached: dict[tuple, dict] = {}
    if ckpt_path.exists():
        for line in ckpt_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            cached[(row["domain"], row["model_variant"], row["n"], row["seed"])] = row
        logger.info(f"Resuming from checkpoint: {len(cached)} cells already cached in {ckpt_path}")
    ckpt_file = ckpt_path.open("a")

    done_count = 0
    for domain, model_variant, n, seed in cells:
        done_count += 1
        key = (domain, model_variant, n, seed)
        if key in cached:
            row = cached[key]
            results.append(row)
            logger.info(f"[{done_count}/{n_cells}] (cached) {domain}/{model_variant}/n={n}/seed={seed}: test_acc={row['test_acc']:.4f}")
            continue
        if remaining_time() < 30:
            logger.warning(f"Wall-clock guard tripped before cell {done_count}/{n_cells}; degrading rest.")
            degradations.append(
                {
                    "reason": "wall_clock_guard",
                    "domain": domain,
                    "model_variant": model_variant,
                    "n": n,
                    "seed": seed,
                    "elapsed_s": time.time() - start_time,
                }
            )
            continue
        pool = all_domain_data[domain]
        train_subset = nested_train_subset(pool["train"], n)
        val_rows, test_rows = pool["val"], pool["test"]
        t0, cpu0 = time.time(), time.process_time()
        try:
            if model_variant == "tfidf_lr":
                metrics = fit_eval_tfidf_lr(train_subset, val_rows, test_rows, seed)
            else:
                metrics = fit_eval_transformer(model_variant, train_subset, val_rows, test_rows, seed)
        except Exception:
            logger.exception(f"Cell failed: {domain}/{model_variant}/n={n}/seed={seed}")
            degradations.append({"reason": "exception", "domain": domain, "model_variant": model_variant, "n": n, "seed": seed})
            continue
        wall, cpu = time.time() - t0, time.process_time() - cpu0
        row = {
            "domain": domain,
            "model_variant": model_variant,
            "n": n,
            "seed": seed,
            "n_train_actual": len(train_subset),
            "val_acc": metrics["val_acc"],
            "test_acc": metrics["test_acc"],
            "wall_clock_s": wall,
            "cpu_time_s": cpu,
            "degraded": False,
        }
        results.append(row)
        ckpt_file.write(json.dumps(row) + "\n")
        ckpt_file.flush()
        logger.info(
            f"[{done_count}/{n_cells}] {domain}/{model_variant}/n={n}/seed={seed}: "
            f"test_acc={metrics['test_acc']:.4f} wall={wall:.1f}s (remaining budget {remaining_time():.0f}s)"
        )
        gc.collect()

    ckpt_file.close()
    return results, degradations


def compute_gap_and_pooled_se(results: list[dict], domain: str, weak_variant: str, n_grid: list[int], seeds: list[int]) -> list[dict]:
    curve = []
    for n in n_grid:
        weak_accs = [r["test_acc"] for r in results if r["domain"] == domain and r["model_variant"] == weak_variant and r["n"] == n]
        base_accs = [r["test_acc"] for r in results if r["domain"] == domain and r["model_variant"] == "tfidf_lr" and r["n"] == n]
        if not weak_accs or not base_accs:
            curve.append({"n": n, "gap": None, "pooled_se": None, "weak_mean": None, "base_mean": None, "n_weak_seeds": len(weak_accs), "n_base_seeds": len(base_accs)})
            continue
        weak_mean, base_mean = float(np.mean(weak_accs)), float(np.mean(base_accs))
        weak_se = float(np.std(weak_accs, ddof=1) / np.sqrt(len(weak_accs))) if len(weak_accs) > 1 else 0.0
        base_se = float(np.std(base_accs, ddof=1) / np.sqrt(len(base_accs))) if len(base_accs) > 1 else 0.0
        pooled_se = float(np.sqrt(weak_se**2 + base_se**2))
        curve.append(
            {
                "n": n,
                "gap": weak_mean - base_mean,
                "pooled_se": pooled_se,
                "weak_mean": weak_mean,
                "base_mean": base_mean,
                "n_weak_seeds": len(weak_accs),
                "n_base_seeds": len(base_accs),
            }
        )
    return curve


def first_n_where_gap_exceeds_se(gap_curve: list[dict]) -> int | None:
    for pt in gap_curve:
        if pt["gap"] is not None and pt["pooled_se"] is not None and pt["gap"] > pt["pooled_se"]:
            return pt["n"]
    return None


# ---------------------------------------------------------------------------
# Label-free coverage predictor (research_out.json protocol)
# ---------------------------------------------------------------------------
def tokenize_simple(text: str) -> list[str]:
    return [t.lower() for t in text.split() if t.strip()]


def build_ngram_vocab(texts: list[str], ngram_range=(1, 2)) -> list[list[str]]:
    docs_ngrams = []
    for t in texts:
        toks = tokenize_simple(t)
        grams = list(toks)
        for i in range(len(toks) - 1):
            grams.append(toks[i] + "_" + toks[i + 1])
        docs_ngrams.append(sorted(set(grams)))
    return docs_ngrams


def mi_contingency(present_pos: int, present_neg: int, absent_pos: int, absent_neg: int, smooth: float = LAPLACE_SMOOTH) -> float:
    n11, n10, n01, n00 = present_pos + smooth, present_neg + smooth, absent_pos + smooth, absent_neg + smooth
    n = n11 + n10 + n01 + n00
    mi = 0.0
    for n_xy, n_x, n_y in [
        (n11, n11 + n10, n11 + n01),
        (n10, n11 + n10, n10 + n00),
        (n01, n01 + n00, n11 + n01),
        (n00, n01 + n00, n10 + n00),
    ]:
        p_xy, p_x, p_y = n_xy / n, n_x / n, n_y / n
        if p_xy > 0 and p_x > 0 and p_y > 0:
            mi += p_xy * np.log2(p_xy / (p_x * p_y))
    return float(mi)


def build_discriminative_vocab(pilot_rows: list[dict], top_k: int = 200, min_df: int = 2, n_perm: int = 200, seed: int = 0) -> dict:
    texts = [r["input"] for r in pilot_rows]
    labels = np.array([int(r["output"]) for r in pilot_rows])
    docs_ngrams = build_ngram_vocab(texts)
    term_doc_count: dict[str, int] = {}
    for grams in docs_ngrams:
        for g in grams:
            term_doc_count[g] = term_doc_count.get(g, 0) + 1
    candidate_terms = [t for t, c in term_doc_count.items() if c >= min_df]
    n_pos, n_neg = int(labels.sum()), int((1 - labels).sum())

    def compute_mi_for_terms(terms: list[str], lbls: np.ndarray) -> dict[str, float]:
        mi_scores = {}
        for t in terms:
            present = np.array([1 if t in grams else 0 for grams in docs_ngrams])
            pp = int(((present == 1) & (lbls == 1)).sum())
            pn = int(((present == 1) & (lbls == 0)).sum())
            ap = int(((present == 0) & (lbls == 1)).sum())
            an = int(((present == 0) & (lbls == 0)).sum())
            mi_scores[t] = mi_contingency(pp, pn, ap, an)
        return mi_scores

    mi_scores = compute_mi_for_terms(candidate_terms, labels)
    freq_scores: dict[str, float] = {}
    for t in candidate_terms:
        present = np.array([1 if t in grams else 0 for grams in docs_ngrams])
        p_pos = present[labels == 1].mean() if n_pos > 0 else 0.0
        p_neg = present[labels == 0].mean() if n_neg > 0 else 0.0
        freq_scores[t] = abs(float(p_pos) - float(p_neg))

    rng = np.random.RandomState(seed)
    max_mi_null = []
    n_perm_terms = candidate_terms if len(candidate_terms) <= 500 else list(rng.choice(candidate_terms, 500, replace=False))
    for _ in range(n_perm):
        shuffled = rng.permutation(labels)
        perm_scores = compute_mi_for_terms(n_perm_terms, shuffled)
        max_mi_null.append(max(perm_scores.values()) if perm_scores else 0.0)
    mi_cutoff = float(np.percentile(max_mi_null, 95)) if max_mi_null else 0.0

    mi_selected = sorted([t for t, s in mi_scores.items() if s > mi_cutoff], key=lambda t: -mi_scores[t])[:top_k]
    if not mi_selected:
        mi_selected = sorted(candidate_terms, key=lambda t: -mi_scores[t])[:top_k]
    freq_selected = sorted(candidate_terms, key=lambda t: -freq_scores[t])[:top_k]

    jaccard = len(set(mi_selected) & set(freq_selected)) / max(1, len(set(mi_selected) | set(freq_selected)))
    return {
        "vocab_mi": mi_selected,
        "vocab_freq": freq_selected,
        "mi_cutoff": mi_cutoff,
        "jaccard_mi_vs_freq": jaccard,
        "pilot_size": len(pilot_rows),
    }


def good_turing_coverage_curve(pool_texts: list[str], vocab: list[str], n_grid: list[int], b: int = B_BOOTSTRAP, seed: int = 0) -> list[dict]:
    rng = np.random.RandomState(seed)
    pool_docs_terms = []
    vocab_set = set(vocab)
    for t in pool_texts:
        toks = tokenize_simple(t)
        grams = set(toks)
        for i in range(len(toks) - 1):
            grams.add(toks[i] + "_" + toks[i + 1])
        pool_docs_terms.append(grams & vocab_set)
    n_pool = len(pool_docs_terms)
    curve = []
    for n in n_grid:
        n_eff = min(n, n_pool)
        c_vals, chao1_vals, f2_lt10_flags = [], [], []
        for _ in range(b):
            idx = rng.choice(n_pool, size=n_eff, replace=False)
            counts: dict[str, int] = {}
            for i in idx:
                for term in pool_docs_terms[i]:
                    counts[term] = counts.get(term, 0) + 1
            freq_of_freq: dict[int, int] = {}
            for c in counts.values():
                freq_of_freq[c] = freq_of_freq.get(c, 0) + 1
            f1 = freq_of_freq.get(1, 0)
            f2 = freq_of_freq.get(2, 0)
            n_total = sum(counts.values())
            c_hat = 1 - (f1 / n_total if n_total > 0 else 1.0)
            s_obs = len(counts)
            chao1 = s_obs + (f1 * (f1 - 1) / (2 * (f2 + 1)))
            c_vals.append(c_hat)
            chao1_vals.append(chao1)
            f2_lt10_flags.append(f2 < F2_INSTABILITY_THRESHOLD)
        unstable_frac = float(np.mean(f2_lt10_flags))
        curve.append(
            {
                "n": n,
                "n_effective": n_eff,
                "coverage_median": float(np.median(c_vals)),
                "coverage_ci_lo": float(np.percentile(c_vals, 2.5)),
                "coverage_ci_hi": float(np.percentile(c_vals, 97.5)),
                "chao1_median": float(np.median(chao1_vals)),
                "unstable_fraction": unstable_frac,
                "unstable": unstable_frac > 0.5,
            }
        )
    return curve


def fit_tau(coverage_curve: list[dict], n_star: int) -> float | None:
    pt = next((c for c in coverage_curve if c["n"] == n_star), None)
    if pt is None:
        closest = min(coverage_curve, key=lambda c: abs(c["n"] - n_star))
        pt = closest
    return 1.0 - pt["coverage_median"]


def predict_crossover(coverage_curve: list[dict], tau: float) -> int | None:
    for pt in sorted(coverage_curve, key=lambda c: c["n"]):
        if (1.0 - pt["coverage_median"]) < tau:
            return pt["n"]
    return None


def main() -> None:
    logger.info(f"Loading data from {DATA_PATH}")
    data = json.loads(DATA_PATH.read_text())
    all_domain_data = {d: load_domain_data(data, d) for d in DOMAINS}
    for d in DOMAINS:
        logger.info(f"{d}: train={len(all_domain_data[d]['train'])} val={len(all_domain_data[d]['val'])} test={len(all_domain_data[d]['test'])} pool={len(all_domain_data[d]['unlabeled_pool'])}")

    logger.info("=== MAIN SWEEP ===")
    sweep_start = time.time()
    results, degradations = run_main_sweep(all_domain_data)
    sweep_wall_s = time.time() - sweep_start
    logger.info(f"Main sweep done: {len(results)} cells completed, {len(degradations) - 1} degradation events, wall={sweep_wall_s:.1f}s")

    logger.info("=== CROSSOVER DETECTION ===")
    all_pairs = []
    for domain in DOMAINS:
        for mv in WEAKENED_VARIANTS:
            gap_curve = compute_gap_and_pooled_se(results, domain, mv, N_GRID, SEEDS)
            n_star = first_n_where_gap_exceeds_se(gap_curve)
            all_pairs.append({"domain": domain, "model_variant": mv, "n_star": n_star, "gap_curve": gap_curve})
            logger.info(f"{domain}/{mv}: n_star={n_star}")

    crossover_pairs = [p for p in all_pairs if p["n_star"] is not None]

    predictor_results: list[dict] = []
    negative_result = None
    if crossover_pairs:
        logger.info(f"=== COVERAGE PREDICTOR ({len(crossover_pairs)} crossover pair(s) found) ===")
        for pair in crossover_pairs:
            domain = pair["domain"]
            pool_texts = [r["input"] for r in all_domain_data[domain]["unlabeled_pool"]]
            pilot_size = min(PILOT_SIZES[-1], len(all_domain_data[domain]["train"]))
            pilot_rows = all_domain_data[domain]["train"][:pilot_size]
            vocab_info = build_discriminative_vocab(pilot_rows)
            pair["vocab_info"] = vocab_info
            pair["coverage_curve_mi"] = good_turing_coverage_curve(pool_texts, vocab_info["vocab_mi"], COVERAGE_N_GRID)
            pair["coverage_curve_freq"] = good_turing_coverage_curve(pool_texts, vocab_info["vocab_freq"], COVERAGE_N_GRID)
            logger.info(f"{domain}/{pair['model_variant']}: vocab built (jaccard mi-vs-freq={vocab_info['jaccard_mi_vs_freq']:.3f})")

        for calib in crossover_pairs:
            for predict in crossover_pairs:
                if calib is predict:
                    continue
                tau = fit_tau(calib["coverage_curve_mi"], calib["n_star"])
                n_hat = predict_crossover(predict["coverage_curve_mi"], tau)
                within_2x = n_hat is not None and (predict["n_star"] / 2 <= n_hat <= predict["n_star"] * 2)
                shared_ns = [pt["n"] for pt in predict["coverage_curve_mi"] if pt["n"] in N_GRID]
                cov_vals = [1 - pt["coverage_median"] for pt in predict["coverage_curve_mi"] if pt["n"] in N_GRID]
                gap_vals = [gp["gap"] for gp in predict["gap_curve"] if gp["n"] in shared_ns and gp["gap"] is not None]
                rho, p_val = (None, None)
                if len(cov_vals) >= 3 and len(gap_vals) == len(cov_vals):
                    rho, p_val = sstats.spearmanr(cov_vals, gap_vals)
                    rho, p_val = float(rho), float(p_val)
                predictor_results.append(
                    {
                        "calibrate_on": f"{calib['domain']}/{calib['model_variant']}",
                        "predict_on": f"{predict['domain']}/{predict['model_variant']}",
                        "tau": tau,
                        "n_hat_star": n_hat,
                        "true_n_star": predict["n_star"],
                        "within_2x": within_2x,
                        "spearman_rho": rho,
                        "spearman_p": p_val,
                    }
                )
    else:
        negative_result = {
            "claim": (
                "No (domain, weakened-model) pair among "
                f"{DOMAINS} x {WEAKENED_VARIANTS} produced a finite empirical "
                f"crossover n* within the grid {N_GRID}."
            ),
            "interpretation": (
                "The coverage predictor remains untested against a real target. "
                "Either the weakening applied (token-truncation to 8/16 tokens, "
                "or substituting bert-tiny) was insufficient to create a regime "
                "where TF-IDF+LR beats the transformer at small n, or curated "
                "short-text sentiment structurally favors any pretrained "
                "transformer representation over bag-of-n-grams regardless of "
                "how weak the transformer's capacity or context window is made. "
                "This is reported as a stronger negative result than the "
                "unweakened DistilBERT case, since weakening was attempted and "
                "still did not produce a crossover to predict."
            ),
        }
        logger.warning("No crossover pairs found; recording explicit negative result.")

    any_crossover_found = len(crossover_pairs) > 0
    predictor_validated = any(pr["within_2x"] for pr in predictor_results) if predictor_results else None
    if not any_crossover_found:
        verdict = "NO_CROSSOVER_FOUND: stronger negative result -- weakening (trunc-8/16, bert-tiny) did not induce any finite crossover on tweet_eval or rotten_tomatoes within n<=1000; predictor remains untested."
    elif predictor_validated is True:
        verdict = f"CROSSOVER_FOUND_AND_PREDICTOR_VALIDATED: {len(crossover_pairs)} crossover pair(s) found; >=1 calibrate/predict direction landed within the 2x band."
    elif predictor_validated is False:
        verdict = f"CROSSOVER_FOUND_PREDICTOR_REFUTED: {len(crossover_pairs)} crossover pair(s) found; no calibrate/predict direction landed within the 2x band."
    else:
        verdict = f"CROSSOVER_FOUND_PREDICTOR_UNTESTED: {len(crossover_pairs)} crossover pair(s) found but <2 pairs available so no cross-pair calibrate/predict test could be run."

    logger.info(f"TOP-LINE VERDICT: {verdict}")

    # Reshape into the exp_gen_sol_out schema: one dataset group per domain,
    # one "example" per sweep cell (input=cell description, output=test_acc),
    # with all per-cell fields carried as metadata_* and all aggregate
    # analysis (config, degradations, crossover/predictor results, verdict)
    # carried in the top-level metadata object (schema allows additionalProperties there).
    datasets_out = []
    for domain in DOMAINS:
        examples = []
        for r in results:
            if r["domain"] != domain:
                continue
            examples.append(
                {
                    "input": f"{r['model_variant']} fit on n={r['n']} train examples (seed={r['seed']}) from {domain}, evaluated on the fixed test set",
                    "output": f"{r['test_acc']:.6f}",
                    f"predict_{r['model_variant']}": f"{r['test_acc']:.6f}",
                    "metadata_model_variant": r["model_variant"],
                    "metadata_n": r["n"],
                    "metadata_seed": r["seed"],
                    "metadata_n_train_actual": r["n_train_actual"],
                    "metadata_val_acc": r["val_acc"],
                    "metadata_test_acc": r["test_acc"],
                    "metadata_wall_clock_s": r["wall_clock_s"],
                    "metadata_cpu_time_s": r["cpu_time_s"],
                    "metadata_degraded": r["degraded"],
                }
            )
        if not examples:
            examples.append(
                {
                    "input": f"No cells completed for {domain} (see degradation_log in top-level metadata)",
                    "output": "N/A",
                    "metadata_degraded": True,
                }
            )
        datasets_out.append({"dataset": domain, "examples": examples})

    output = {
        "metadata": {
            "method": "weaken-the-transformer crossover search + label-free Good-Turing/Chao1 coverage predictor",
            "config": {
                "domains": DOMAINS,
                "n_grid": N_GRID,
                "n_grid_full_plan": N_GRID_FULL_PLAN,
                "seeds": SEEDS,
                "model_variants": MODEL_VARIANTS,
                "tfidf_hparams": {k: (list(v) if isinstance(v, tuple) else v) for k, v in TFIDF_HPARAMS.items()},
                "lr_hparams": LR_HPARAMS,
                "transformer_hparams": TRANSFORMER_HPARAMS,
                "model_checkpoints": MODEL_CHECKPOINTS,
                "max_lengths": MAX_LENGTHS,
                "time_budget_s": TIME_BUDGET_S,
                "pilot_sizes": PILOT_SIZES,
                "coverage_n_grid": COVERAGE_N_GRID,
                "b_bootstrap": B_BOOTSTRAP,
                "f2_instability_threshold": F2_INSTABILITY_THRESHOLD,
                "laplace_smooth": LAPLACE_SMOOTH,
            },
            "degradation_log": degradations,
            "sweep_wall_clock_s": sweep_wall_s,
            "crossover_pairs_all": all_pairs,
            "crossover_pairs_found": [p["domain"] + "/" + p["model_variant"] for p in crossover_pairs],
            "predictor_results": predictor_results,
            "explicit_negative_result": negative_result,
            "top_line_verdict": verdict,
        },
        "datasets": datasets_out,
    }
    OUT_PATH.write_text(json.dumps(output, indent=2, default=str))
    logger.info(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
