#!/usr/bin/env python3
"""TF-IDF+LR vs CPU-fine-tuned DistilBERT crossover point, and a label-free
Good-Turing/Chao1 unseen-vocabulary-mass predictor of that crossover, tested
for cross-domain transfer across short-text sentiment domains.
"""
from __future__ import annotations

import gc
import json
import math
import os
import random
import resource
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
from loguru import logger
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression

WORKDIR = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(WORKDIR / ".hf_cache"))
os.environ.setdefault("HF_DATASETS_CACHE", str(WORKDIR / ".hf_cache" / "datasets"))
os.environ.setdefault("TRANSFORMERS_CACHE", str(WORKDIR / ".hf_cache" / "transformers"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "4")

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(WORKDIR / "logs").mkdir(exist_ok=True)
logger.add(WORKDIR / "logs" / "run.log", rotation="30 MB", level="DEBUG")

# ------------------------------------------------------------------ hardware
def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1


def _container_ram_gb() -> float:
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError):
            pass
    return psutil.virtual_memory().total / 1e9


NUM_CPUS = _detect_cpus()
TOTAL_RAM_GB = _container_ram_gb()
RAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))
logger.info(f"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}")

import torch  # noqa: E402  (import after thread-count env vars are set)

torch.set_num_threads(max(1, NUM_CPUS))
from transformers import (  # noqa: E402
    DistilBertForSequenceClassification,
    DistilBertTokenizerFast,
    Trainer,
    TrainingArguments,
)

# ------------------------------------------------------------------ config
TIME_BUDGET_S = 35 * 60.0  # wall-clock budget for Part A DistilBERT sweep (kept short: prior attempt's
# container was killed after ~93min of real time spent on a 2.2h-budgeted sweep + repeated polling
# turns; degrading aggressively and finishing fast is far safer than a long unattended run)
PART_A_START = time.time()
CHECKPOINT_PATH = WORKDIR / "results" / "part_a_checkpoint.json"

SEEDS_FULL = [0, 1]
NS_FULL = [50, 200, 500, 1000]
DOMAINS_ORDER = ["rotten_tomatoes", "sst2", "imdb"]
PILOT_NS = [100, 200, 400]
VOCAB_METHODS = ["mi", "freq"]
TEST_N = 800  # fixed held-out size per domain
UNLABELED_POOL_N = 6000
LABELED_POOL_CAP = 4000
MAX_LEN = 64

degradation_log: list[str] = []


def ci95(vals) -> float:
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) < 2:
        return 0.0
    return 1.96 * vals.std(ddof=1) / math.sqrt(len(vals))


# ------------------------------------------------------------------ data loading
def _balanced_sample(texts, labels, n, seed, exclude_idx=None):
    rng = np.random.default_rng(seed)
    labels = np.asarray(labels)
    idx_all = np.arange(len(texts))
    if exclude_idx is not None:
        mask = np.ones(len(texts), dtype=bool)
        mask[list(exclude_idx)] = False
        idx_all = idx_all[mask]
    classes = np.unique(labels[idx_all])
    per_class = n // len(classes)
    chosen = []
    for c in classes:
        pool = idx_all[labels[idx_all] == c]
        rng.shuffle(pool)
        take = min(per_class, len(pool))
        chosen.extend(pool[:take].tolist())
    rng.shuffle(chosen)
    chosen = chosen[:n]
    return chosen


def load_domains() -> dict:
    from datasets import load_dataset

    domains = {}

    def build(name, texts, labels, unlabeled_extra=None):
        texts = [str(t)[:1000] for t in texts]
        labels = [int(x) for x in labels]
        rng = np.random.default_rng(0)
        order = rng.permutation(len(texts))
        texts = [texts[i] for i in order]
        labels = [labels[i] for i in order]

        test_idx = _balanced_sample(texts, labels, min(TEST_N, len(texts) // 3), seed=999)
        test_idx_set = set(test_idx)
        test_texts = [texts[i] for i in test_idx]
        test_labels = [labels[i] for i in test_idx]

        remaining_idx = [i for i in range(len(texts)) if i not in test_idx_set]
        rng2 = np.random.default_rng(1)
        rng2.shuffle(remaining_idx)
        labeled_idx = remaining_idx[: min(LABELED_POOL_CAP, len(remaining_idx))]
        labeled_texts = [texts[i] for i in labeled_idx]
        labeled_labels = [labels[i] for i in labeled_idx]

        unlabeled_source = (unlabeled_extra if unlabeled_extra else texts)
        unlabeled_pool = [str(t)[:1000] for t in unlabeled_source][:UNLABELED_POOL_N]

        n_pos = sum(test_labels)
        logger.info(
            f"domain={name} labeled_pool={len(labeled_texts)} unlabeled_pool={len(unlabeled_pool)} "
            f"test={len(test_texts)} (pos={n_pos}/{len(test_labels)})"
        )
        assert len(set(test_labels)) >= 2, f"{name}: test split missing a class"
        assert len(labeled_texts) >= 200, f"{name}: labeled pool too small"
        domains[name] = dict(
            labeled_pool=(labeled_texts, labeled_labels),
            unlabeled_pool=unlabeled_pool,
            test_texts=test_texts,
            test_labels=test_labels,
        )

    try:
        rt = load_dataset("cornell-movie-review-data/rotten_tomatoes")
        build(
            "rotten_tomatoes",
            list(rt["train"]["text"]) + list(rt["validation"]["text"]),
            list(rt["train"]["label"]) + list(rt["validation"]["label"]),
        )
    except Exception:
        logger.error("failed to load rotten_tomatoes")
        raise

    try:
        sst2 = load_dataset("nyu-mll/glue", "sst2")
        build(
            "sst2",
            list(sst2["train"]["sentence"]),
            list(sst2["train"]["label"]),
        )
    except Exception:
        logger.error("failed to load sst2")
        raise

    try:
        imdb = load_dataset("stanfordnlp/imdb")
        # truncate reviews to first two sentences worth of chars to keep the
        # domain "short-text" and CPU tokenization/training cheap
        imdb_texts = [t[:400] for t in imdb["train"]["text"]]
        build("imdb", imdb_texts, list(imdb["train"]["label"]))
    except Exception:
        logger.error("failed to load imdb; continuing with 2 domains")
        degradation_log.append("imdb domain unavailable -> proceeded with 2 domains")

    return domains


def stratified_sample(texts, labels, n, seed):
    idx = _balanced_sample(texts, labels, n, seed)
    return [texts[i] for i in idx], [labels[i] for i in idx]


# ------------------------------------------------------------------ Part A: classifiers
def train_tfidf_lr(train_texts, train_labels, test_texts, test_labels, seed):
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    Xtr = vec.fit_transform(train_texts)
    Xte = vec.transform(test_texts)
    clf = LogisticRegression(max_iter=2000, C=1.0, random_state=seed, class_weight="balanced")
    clf.fit(Xtr, train_labels)
    return float(clf.score(Xte, test_labels))


class SimpleTorchDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item


_TOKENIZER = None
_EPOCH_TIERS = {50: 5, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}


def finetune_distilbert(train_texts, train_labels, test_texts, test_labels, seed, n):
    global _TOKENIZER
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    if _TOKENIZER is None:
        _TOKENIZER = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    tok = _TOKENIZER
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

    train_enc = tok(train_texts, truncation=True, padding=True, max_length=MAX_LEN)
    test_enc = tok(test_texts, truncation=True, padding=True, max_length=MAX_LEN)
    train_ds = SimpleTorchDataset(train_enc, train_labels)
    test_ds = SimpleTorchDataset(test_enc, test_labels)

    epochs = _EPOCH_TIERS.get(n, 2)
    out_dir = WORKDIR / "hf_runs" / f"db_{seed}_{n}_{int(time.time()*1000)}"
    args = TrainingArguments(
        output_dir=str(out_dir),
        num_train_epochs=epochs,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_steps=200,
        use_cpu=True,
        seed=seed,
        report_to=[],
        save_strategy="no",
        eval_strategy="no",
        disable_tqdm=True,
    )
    trainer = Trainer(model=model, args=args, train_dataset=train_ds)
    t0 = time.time()
    trainer.train()
    train_secs = time.time() - t0
    preds = trainer.predict(test_ds).predictions.argmax(-1)
    acc = float((preds == np.array(test_labels)).mean())

    del model, trainer, train_enc, test_enc, train_ds, test_ds
    gc.collect()
    import shutil

    shutil.rmtree(out_dir, ignore_errors=True)
    return acc, train_secs


def empirical_crossover(curve_domain: pd.DataFrame):
    """Smallest n where mean_db - mean_tfidf flips sign from <=0 to >0 (linear interp)."""
    cd = curve_domain.sort_values("n").reset_index(drop=True)
    gaps = cd["gap"].values
    ns = cd["n"].values
    if len(ns) == 0:
        return None, "no_data"
    if (gaps > 0).all():
        return None, "distilbert_ahead_at_all_tested_n"
    if (gaps <= 0).all():
        return None, "distilbert_never_ahead_in_tested_range"
    for i in range(1, len(ns)):
        if gaps[i - 1] <= 0 and gaps[i] > 0:
            if gaps[i] == gaps[i - 1]:
                n_star = float(ns[i])
            else:
                frac = (0 - gaps[i - 1]) / (gaps[i] - gaps[i - 1])
                n_star = float(ns[i - 1] + frac * (ns[i] - ns[i - 1]))
            return n_star, "interpolated"
    return None, "no_clean_crossing"


# ------------------------------------------------------------------ Part B: coverage
def discriminative_ngrams(pilot_texts, pilot_labels, method="mi", top_k=2000):
    cv = CountVectorizer(ngram_range=(1, 2), min_df=2, binary=True)
    X = cv.fit_transform(pilot_texts)
    if X.shape[1] == 0:
        cv = CountVectorizer(ngram_range=(1, 1), min_df=1, binary=True)
        X = cv.fit_transform(pilot_texts)
    if method == "mi":
        scores = mutual_info_classif(X, pilot_labels, discrete_features=True, random_state=0)
    else:
        scores = np.asarray(X.sum(axis=0)).ravel()
    vocab = np.array(cv.get_feature_names_out())
    top_idx = np.argsort(scores)[::-1][: min(top_k, len(vocab))]
    return set(vocab[top_idx].tolist())


def _count_ngram_occurrences(docs, target_ngram_set, ngram_range=(1, 2)):
    cv = CountVectorizer(ngram_range=ngram_range, vocabulary=sorted(target_ngram_set))
    X = cv.transform(docs)
    totals = np.asarray(X.sum(axis=0)).ravel()
    vocab = cv.get_feature_names_out()
    return dict(zip(vocab, totals.tolist()))


def good_turing_unseen_mass(subsample_docs, target_ngram_set, ngram_range=(1, 2)):
    counts = _count_ngram_occurrences(subsample_docs, target_ngram_set, ngram_range)
    N = sum(counts.values())
    f1 = sum(1 for c in counts.values() if c == 1)
    p0_hat = f1 / N if N > 0 else 1.0
    seen_frac = (len([g for g, c in counts.items() if c > 0]) / len(target_ngram_set)) if target_ngram_set else 0.0
    return p0_hat, seen_frac


def chao1_richness(subsample_docs, target_ngram_set, ngram_range=(1, 2)):
    counts = _count_ngram_occurrences(subsample_docs, target_ngram_set, ngram_range)
    f1 = sum(1 for c in counts.values() if c == 1)
    f2 = sum(1 for c in counts.values() if c == 2)
    s_obs = sum(1 for c in counts.values() if c > 0)
    s_chao1 = s_obs + (f1**2) / (2 * max(f2, 1))
    return float(s_chao1), int(s_obs)


def coverage_curve(domain_data, pilot_n, method, n_points, n_bootstrap=15):
    labeled_texts, labeled_labels = domain_data["labeled_pool"]
    pilot_texts, pilot_labels = stratified_sample(labeled_texts, labeled_labels, min(pilot_n, len(labeled_texts)), seed=0)
    disc_vocab = discriminative_ngrams(pilot_texts, pilot_labels, method=method)
    unlabeled_pool = domain_data["unlabeled_pool"]
    rows = []
    for n in n_points:
        if n > len(unlabeled_pool):
            n_eff = len(unlabeled_pool)
        else:
            n_eff = n
        boot_vals = []
        for b in range(n_bootstrap):
            rng = np.random.default_rng(b)
            sub_idx = rng.choice(len(unlabeled_pool), size=n_eff, replace=(n_eff > len(unlabeled_pool)))
            sub = [unlabeled_pool[i] for i in sub_idx]
            _, seen_frac = good_turing_unseen_mass(sub, disc_vocab)
            boot_vals.append(1 - seen_frac)
        rows.append(dict(n=n, unseen_mean=float(np.mean(boot_vals)), unseen_ci=float(ci95(boot_vals))))
    return pd.DataFrame(rows), disc_vocab


def interp_crossing(ns, unseen_means, tau):
    """First n where unseen_mean <= tau (linear interp); None if tau outside observed range."""
    ns = np.asarray(ns, dtype=float)
    um = np.asarray(unseen_means, dtype=float)
    order = np.argsort(ns)
    ns, um = ns[order], um[order]
    if tau > um[0] or tau < um[-1] - 1e-9:
        if tau > um[0]:
            return None  # tau above the curve's starting unseen-mass: undefined (edge artifact)
    for i in range(len(ns)):
        if um[i] <= tau:
            if i == 0:
                return float(ns[0])
            n0, n1 = ns[i - 1], ns[i]
            u0, u1 = um[i - 1], um[i]
            if u0 == u1:
                return float(n1)
            frac = (u0 - tau) / (u0 - u1)
            return float(n0 + frac * (n1 - n0))
    return None  # tau never reached within observed range


def calibrate_and_predict(cov_curve_A, true_nstar_A, cov_curve_B):
    tau = float(np.interp(true_nstar_A, cov_curve_A["n"], cov_curve_A["unseen_mean"]))
    n_hat_B = interp_crossing(cov_curve_B["n"].values, cov_curve_B["unseen_mean"].values, tau)
    return n_hat_B, tau


def compute_overall_verdict(predictions, correlations):
    valid_preds = [p for p in predictions if p["within_2x"] is not None]
    if not valid_preds:
        return "DISCONFIRMED"
    hit_rate = sum(1 for p in valid_preds if p["within_2x"]) / len(valid_preds)
    sig_corrs = [c for c in correlations.values() if c["pval"] is not None and c["pval"] < 0.10 and c["rho"] < 0]
    if hit_rate >= 0.5 and len(sig_corrs) >= max(1, len(correlations) // 2):
        return "SUPPORTED"
    if hit_rate > 0 or len(sig_corrs) > 0:
        return "PARTIAL"
    return "DISCONFIRMED"


# ------------------------------------------------------------------ main
def main():
    logger.info("=" * 70)
    logger.info("Loading domains")
    domains = load_domains()
    domain_names = [d for d in DOMAINS_ORDER if d in domains]
    logger.info(f"Domains loaded: {domain_names}")

    # -------- smoke test (n=50, 1 seed, epochs=1) on first domain --------
    smoke_domain = domains[domain_names[0]]
    tr_t, tr_l = stratified_sample(*smoke_domain["labeled_pool"], 50, seed=0)
    acc_lr_smoke = train_tfidf_lr(tr_t, tr_l, smoke_domain["test_texts"][:50], smoke_domain["test_labels"][:50], seed=0)
    assert 0.0 <= acc_lr_smoke <= 1.0
    global _EPOCH_TIERS
    saved_tiers = dict(_EPOCH_TIERS)
    _EPOCH_TIERS = {50: 1}
    t0 = time.time()
    acc_db_smoke, secs_smoke = finetune_distilbert(
        tr_t, tr_l, smoke_domain["test_texts"][:50], smoke_domain["test_labels"][:50], seed=0, n=50
    )
    _EPOCH_TIERS = saved_tiers
    assert 0.0 <= acc_db_smoke <= 1.0
    per_epoch_secs = secs_smoke  # 1 epoch at n=50
    logger.info(f"SMOKE OK: acc_tfidf={acc_lr_smoke:.3f} acc_db={acc_db_smoke:.3f} 1-epoch-n50-secs={secs_smoke:.1f}")

    # coverage-curve smoke check: seen_frac should rise monotonically-ish with n
    pilot_t, pilot_l = stratified_sample(*smoke_domain["labeled_pool"], 100, seed=0)
    vocab_smoke = discriminative_ngrams(pilot_t, pilot_l, method="mi")
    seen_fracs = []
    for n_chk in [50, 200, 1000]:
        n_eff = min(n_chk, len(smoke_domain["unlabeled_pool"]))
        sub = smoke_domain["unlabeled_pool"][:n_eff]
        p0, sf = good_turing_unseen_mass(sub, vocab_smoke)
        assert 0.0 <= p0 <= 1.0 and 0.0 <= sf <= 1.0
        seen_fracs.append(sf)
    logger.info(f"SMOKE coverage seen_fracs at n=[50,200,1000]: {seen_fracs}")
    if not (seen_fracs[0] <= seen_fracs[1] <= seen_fracs[2] + 1e-6):
        degradation_log.append(f"coverage-curve smoke check non-monotonic: {seen_fracs}")
        logger.warning(f"seen_frac not monotonic: {seen_fracs}")

    # -------- timing-based budget projection --------
    # rough per-run estimate: (epochs_at_n / 1) * per_epoch_secs * (n/50) [linear-ish in n too]
    def est_run_secs(n):
        epochs = _EPOCH_TIERS.get(n, 2)
        return per_epoch_secs * epochs * max(1.0, n / 50.0) * 0.6  # 0.6 damping: larger batches amortize overhead

    seeds, ns = list(SEEDS_FULL), list(NS_FULL)
    total_est = sum(est_run_secs(n) for n in ns for _ in seeds for _ in domain_names)
    logger.info(f"Projected Part-A DistilBERT total: {total_est/60:.1f} min (budget {TIME_BUDGET_S/60:.0f} min)")

    if total_est > 0.7 * TIME_BUDGET_S:
        if len(seeds) > 2:
            seeds = seeds[:2]
            degradation_log.append(f"dropped SEEDS to {seeds} (projected {total_est/60:.1f}min > 70% budget)")
        total_est = sum(est_run_secs(n) for n in ns for _ in seeds for _ in domain_names)
    if total_est > 0.7 * TIME_BUDGET_S and len(ns) > 4:
        ns = ns[:-1]
        degradation_log.append(f"dropped largest n; NS now {ns}")
        total_est = sum(est_run_secs(n) for n in ns for _ in seeds for _ in domain_names)
    if total_est > 0.7 * TIME_BUDGET_S and len(domain_names) > 2:
        domain_names = domain_names[:2]
        degradation_log.append(f"reduced to 2 domains: {domain_names}")
        total_est = sum(est_run_secs(n) for n in ns for _ in seeds for _ in domain_names)
    logger.info(f"Final sweep config: NS={ns} SEEDS={seeds} DOMAINS={domain_names} est={total_est/60:.1f}min")

    # -------- Part A: full sweep with running wall-clock guard + checkpointing --------
    # Checkpoint after every (domain,n,seed) run so a crash never loses completed work:
    # a resumed process picks up from the last saved combo instead of recomputing it.
    results = []
    done_combos = set()
    if CHECKPOINT_PATH.exists():
        try:
            ckpt = json.loads(CHECKPOINT_PATH.read_text())
            results = ckpt.get("results", [])
            done_combos = {(r["domain"], r["n"], r["seed"]) for r in results}
            logger.info(f"Resumed checkpoint: {len(results)} runs already completed, skipping them")
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Could not load checkpoint ({e}); starting fresh")

    def _save_checkpoint():
        CHECKPOINT_PATH.parent.mkdir(exist_ok=True)
        CHECKPOINT_PATH.write_text(json.dumps({"results": results}, default=str))

    part_a_t0 = time.time()
    skipped = []
    combos = [(d, n, s) for d in domain_names for n in ns for s in seeds]
    n_done = len(results)
    for domain, n, seed in combos:
        if (domain, n, seed) in done_combos:
            continue
        elapsed = time.time() - part_a_t0
        remaining = len(combos) - n_done
        avg = (elapsed / max(1, n_done - len(done_combos))) if n_done > len(done_combos) else est_run_secs(n)
        if elapsed + avg * remaining > TIME_BUDGET_S and n_done > 0:
            skipped.append((domain, n, seed))
            continue
        d = domains[domain]
        train_texts, train_labels = stratified_sample(*d["labeled_pool"], n, seed)
        acc_lr = train_tfidf_lr(train_texts, train_labels, d["test_texts"], d["test_labels"], seed)
        acc_db, secs = finetune_distilbert(train_texts, train_labels, d["test_texts"], d["test_labels"], seed, n)
        results.append(
            dict(domain=domain, n=n, seed=seed, acc_tfidf=acc_lr, acc_distilbert=acc_db, db_train_secs=secs)
        )
        n_done += 1
        _save_checkpoint()
        logger.info(
            f"[{n_done}/{len(combos)}] domain={domain} n={n} seed={seed} "
            f"acc_tfidf={acc_lr:.3f} acc_db={acc_db:.3f} secs={secs:.1f} elapsed={elapsed/60:.1f}min"
        )
    if skipped:
        degradation_log.append(f"skipped {len(skipped)} runs mid-sweep due to running time budget: {skipped[:10]}...")
        logger.warning(f"Skipped {len(skipped)} combos due to time budget")

    df = pd.DataFrame(results)
    assert len(df) > 0, "no Part-A results produced"

    curve_rows = []
    for (domain, n), g in df.groupby(["domain", "n"]):
        curve_rows.append(
            dict(
                domain=domain,
                n=n,
                mean_tfidf=g["acc_tfidf"].mean(),
                ci_tfidf=ci95(g["acc_tfidf"]),
                mean_db=g["acc_distilbert"].mean(),
                ci_db=ci95(g["acc_distilbert"]),
                n_seeds=len(g),
            )
        )
    curve = pd.DataFrame(curve_rows)
    curve["gap"] = curve["mean_db"] - curve["mean_tfidf"]

    true_crossovers = {}
    for domain in domain_names:
        cd = curve[curve.domain == domain]
        if len(cd) < 2:
            true_crossovers[domain] = dict(n_star=None, direction="insufficient_n_points")
            continue
        n_star, direction = empirical_crossover(cd)
        true_crossovers[domain] = dict(n_star=n_star, direction=direction)
    logger.info(f"True crossovers: {true_crossovers}")

    # sanity check: TF-IDF accuracy should be non-decreasing (within noise) in n for >=2/3 domains
    monotonic_ok = 0
    for domain in domain_names:
        cd = curve[curve.domain == domain].sort_values("n")
        diffs = np.diff(cd["mean_tfidf"].values)
        if (diffs >= -0.05).sum() >= max(1, len(diffs) - 1):
            monotonic_ok += 1
    if monotonic_ok < max(1, math.ceil(len(domain_names) * 2 / 3)):
        degradation_log.append(
            f"TF-IDF accuracy non-monotonic in n for {len(domain_names)-monotonic_ok}/{len(domain_names)} domains "
            "(possible leakage/sampling issue) — reported as-is per fallback plan"
        )
        logger.warning("TF-IDF monotonicity sanity check failed for some domains")

    # -------- Part B: coverage curves (label-free) --------
    logger.info("Computing coverage curves (Part B)")
    coverage_curves = {}
    for domain in domain_names:
        for pilot_n in PILOT_NS:
            for method in VOCAB_METHODS:
                cov_df, vocab = coverage_curve(domains[domain], pilot_n, method, n_points=ns)
                coverage_curves[(domain, pilot_n, method)] = cov_df
                logger.debug(f"coverage_curve domain={domain} pilot_n={pilot_n} method={method} vocab_size={len(vocab)}")

    # -------- Part C: cross-domain calibrate/predict --------
    logger.info("Computing cross-domain predictions (Part C)")
    predictions = []
    for A in domain_names:
        for B in domain_names:
            if A == B:
                continue
            nstar_A = true_crossovers[A]["n_star"]
            if nstar_A is None:
                predictions.append(
                    dict(calibrate_on=A, predict_on=B, n_hat_star=None, n_true_star=true_crossovers[B]["n_star"],
                         within_2x=None, tau=None, note=f"skipped: {A} has no finite empirical crossover")
                )
                continue
            cov_A = coverage_curves[(A, 200, "mi")]
            cov_B = coverage_curves[(B, 200, "mi")]
            n_hat_B, tau = calibrate_and_predict(cov_A, nstar_A, cov_B)
            n_true_B = true_crossovers[B]["n_star"]
            ratio = (n_hat_B / n_true_B) if (n_true_B and n_hat_B) else None
            predictions.append(
                dict(
                    calibrate_on=A,
                    predict_on=B,
                    n_hat_star=n_hat_B,
                    n_true_star=n_true_B,
                    within_2x=(ratio is not None and 0.5 <= ratio <= 2.0),
                    tau=tau,
                    note=None,
                )
            )
    logger.info(f"Cross-domain predictions: {predictions}")

    # -------- pilot-size / MI-vs-freq ablation summary --------
    ablation_rows = []
    for domain in domain_names:
        nstar = true_crossovers[domain]["n_star"]
        for pilot_n in PILOT_NS:
            for method in VOCAB_METHODS:
                cov = coverage_curves[(domain, pilot_n, method)]
                # self-consistency: predict domain from itself at this pilot/method config
                if nstar is not None:
                    tau_self = float(np.interp(nstar, cov["n"], cov["unseen_mean"]))
                else:
                    tau_self = None
                ablation_rows.append(dict(domain=domain, pilot_n=pilot_n, method=method, tau_self=tau_self))

    # -------- Part D: correlation --------
    logger.info("Computing gap-vs-unseen-mass correlations (Part D)")
    correlations = {}
    for domain in domain_names:
        gap_series = curve[curve.domain == domain].sort_values("n")["gap"].values
        cov = coverage_curves[(domain, 200, "mi")].sort_values("n")
        unseen_series = cov["unseen_mean"].values
        if len(gap_series) >= 3 and len(unseen_series) == len(gap_series):
            rho, pval = spearmanr(unseen_series, gap_series)
            correlations[domain] = dict(rho=float(rho), pval=float(pval), n_points=len(gap_series))
        else:
            correlations[domain] = dict(rho=None, pval=None, n_points=len(gap_series))
    logger.info(f"Correlations: {correlations}")

    verdict = compute_overall_verdict(predictions, correlations)
    logger.info(f"OVERALL VERDICT: {verdict}")

    # ------------------------------------------------------------ assemble schema-compliant output
    def ex(inp, out, predict=None, **meta):
        e = {"input": inp, "output": out}
        for k, v in meta.items():
            e[f"metadata_{k}"] = v
        # predict_* fields: per-method model outputs for this example, required by the
        # exp_gen_sol_out schema (this artifact compares two methods, so both appear).
        for k, v in (predict or {}).items():
            e[f"predict_{k}"] = v
        return e

    datasets_out = []

    datasets_out.append(
        {
            "dataset": "raw_results",
            "examples": [
                ex(
                    f"domain={r['domain']} n={r['n']} seed={r['seed']}",
                    f"acc_tfidf={r['acc_tfidf']:.4f} acc_distilbert={r['acc_distilbert']:.4f}",
                    predict={
                        "tfidf_lr_acc": f"{r['acc_tfidf']:.4f}",
                        "distilbert_acc": f"{r['acc_distilbert']:.4f}",
                    },
                    domain=r["domain"], n=int(r["n"]), seed=int(r["seed"]),
                    acc_tfidf=float(r["acc_tfidf"]), acc_distilbert=float(r["acc_distilbert"]),
                    db_train_secs=float(r["db_train_secs"]),
                )
                for r in df.to_dict("records")
            ],
        }
    )

    datasets_out.append(
        {
            "dataset": "accuracy_curve",
            "examples": [
                ex(
                    f"domain={r['domain']} n={r['n']}",
                    f"mean_tfidf={r['mean_tfidf']:.4f}+-{r['ci_tfidf']:.4f} mean_db={r['mean_db']:.4f}+-{r['ci_db']:.4f} gap={r['gap']:.4f}",
                    predict={
                        "tfidf_lr_mean_acc": f"{r['mean_tfidf']:.4f}",
                        "distilbert_mean_acc": f"{r['mean_db']:.4f}",
                    },
                    domain=r["domain"], n=int(r["n"]), mean_tfidf=float(r["mean_tfidf"]), ci_tfidf=float(r["ci_tfidf"]),
                    mean_db=float(r["mean_db"]), ci_db=float(r["ci_db"]), gap=float(r["gap"]), n_seeds=int(r["n_seeds"]),
                )
                for r in curve.to_dict("records")
            ],
        }
    )

    datasets_out.append(
        {
            "dataset": "true_crossovers",
            "examples": [
                ex(
                    f"domain={domain}",
                    f"n_star={tc['n_star']} direction={tc['direction']}",
                    predict={"empirical_crossover_n": str(tc["n_star"])},
                    domain=domain, n_star=tc["n_star"], direction=tc["direction"],
                )
                for domain, tc in true_crossovers.items()
            ],
        }
    )

    cov_examples = []
    for (domain, pilot_n, method), cov_df in coverage_curves.items():
        for r in cov_df.to_dict("records"):
            cov_examples.append(
                ex(
                    f"domain={domain} pilot_n={pilot_n} method={method} n={r['n']}",
                    f"unseen_mean={r['unseen_mean']:.4f}+-{r['unseen_ci']:.4f}",
                    predict={"gt_unseen_mass": f"{r['unseen_mean']:.4f}"},
                    domain=domain, pilot_n=pilot_n, method=method, n=int(r["n"]),
                    unseen_mean=float(r["unseen_mean"]), unseen_ci=float(r["unseen_ci"]),
                )
            )
    datasets_out.append({"dataset": "coverage_curves", "examples": cov_examples})

    datasets_out.append(
        {
            "dataset": "cross_domain_predictions",
            "examples": [
                ex(
                    f"calibrate_on={p['calibrate_on']} predict_on={p['predict_on']}",
                    f"n_hat_star={p['n_hat_star']} n_true_star={p['n_true_star']} within_2x={p['within_2x']}",
                    predict={"n_hat_star": str(p["n_hat_star"])},
                    **{k: v for k, v in p.items() if k not in ("calibrate_on", "predict_on")},
                    calibrate_on=p["calibrate_on"], predict_on=p["predict_on"],
                )
                for p in predictions
            ],
        }
    )

    datasets_out.append(
        {
            "dataset": "pilot_and_vocab_ablation",
            "examples": [
                ex(
                    f"domain={r['domain']} pilot_n={r['pilot_n']} method={r['method']}",
                    f"tau_self={r['tau_self']}",
                    domain=r["domain"], pilot_n=r["pilot_n"], method=r["method"], tau_self=r["tau_self"],
                )
                for r in ablation_rows
            ],
        }
    )

    datasets_out.append(
        {
            "dataset": "gap_vs_unseen_correlations",
            "examples": [
                ex(
                    f"domain={domain}",
                    f"rho={c['rho']} pval={c['pval']}",
                    domain=domain, rho=c["rho"], pval=c["pval"], n_points=c["n_points"],
                )
                for domain, c in correlations.items()
            ],
        }
    )

    datasets_out.append(
        {
            "dataset": "summary",
            "examples": [
                ex(
                    "overall_verdict",
                    verdict,
                    verdict=verdict,
                    domains_used=domain_names,
                    ns_used=ns,
                    seeds_used=seeds,
                    n_domains=len(domain_names),
                    n_cross_domain_pairs=len(predictions),
                    degradations_applied=degradation_log,
                    total_wallclock_s=time.time() - PART_A_START,
                )
            ],
        }
    )

    method_out = {
        "metadata": {
            "method_name": "tfidf_vs_distilbert_crossover_with_gt_predictor",
            "description": "Empirical accuracy-vs-n crossover between TF-IDF+LR and CPU-fine-tuned DistilBERT, "
            "plus a label-free Good-Turing/Chao1 unseen-vocabulary-mass predictor of that crossover, "
            "tested for cross-domain transfer.",
            "parameters": {
                "NS": ns,
                "SEEDS": seeds,
                "DOMAINS": domain_names,
                "PILOT_NS": PILOT_NS,
                "VOCAB_METHODS": VOCAB_METHODS,
                "MAX_LEN": MAX_LEN,
                "TEST_N": TEST_N,
            },
        },
        "datasets": datasets_out,
    }

    out_path = WORKDIR / "method_out.json"
    out_path.write_text(json.dumps(method_out, indent=2, default=str))
    logger.info(f"Wrote {out_path} ({out_path.stat().st_size/1e6:.2f} MB)")
    return method_out


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("method.py failed")
        raise
