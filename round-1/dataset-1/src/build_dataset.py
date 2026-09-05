#!/usr/bin/env python3
"""Assemble the three-domain short-text sentiment corpus.

Sources:
  - cornell-movie-review-data/rotten_tomatoes  (RT, Pang & Lee lineage)
  - stanfordnlp/sst2                            (SST-2, GLUE; Socher-derived from
                                                  the SAME upstream Pang & Lee review
                                                  corpus as RT -> lineage-linked)
  - cardiffnlp/tweet_eval (config=sentiment)    (independent social-media domain;
                                                  3-class -> binarize by dropping
                                                  the neutral class, label 1)

Normalizes every source to {text, label, domain}, dedups within each domain,
cross-dedups the RT/SST-2 lineage pair specifically, then builds per-domain:
  - a fixed held-out val (~500) and test (~1000) set
  - nested labeled train pools at n in {50,100,200,500,1000,1500,2000},
    seeded so smaller-n pools are subsets of larger-n pools
  - a large unlabeled pool (raw text only, capped at 10,000 rows) for the
    downstream Good-Turing/Chao1 subsampling curve

Emits full/mini/preview JSON variants plus a manifest documenting exact
source versions, row counts before/after filtering, dedup counts, and the
RT/SST-2 lineage caveat.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent.resolve()
RAW_DIR = WORKSPACE / "temp" / "datasets"
OUT_DIR = WORKSPACE / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
TRAIN_SIZES = [50, 100, 200, 500, 1000, 1500, 2000]
VAL_SIZE = 500
TEST_SIZE = 1000
UNLABELED_CAP = 10000


def _norm_text(t: str) -> str:
    """Lowercase + strip punctuation, for cross-duplicate detection only."""
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _shingle_key(t: str) -> str:
    """Hash of the first 8 normalized tokens - cheap near-duplicate key."""
    toks = _norm_text(t).split()[:8]
    return hashlib.sha1(" ".join(toks).encode("utf-8")).hexdigest()


def load_json(path: Path) -> list[dict[str, Any]]:
    logger.info(f"Loading {path.name}")
    data = json.loads(path.read_text())
    assert isinstance(data, list), f"{path} did not contain a list"
    return data


@logger.catch(reraise=True)
def load_rotten_tomatoes() -> list[dict[str, Any]]:
    rows = []
    for split in ["train", "validation", "test"]:
        rows.extend(load_json(RAW_DIR / f"full_cornell-movie-review-data_rotten_tomatoes_default_{split}.json"))
    out = [{"text": r["text"].strip(), "label": int(r["label"])} for r in rows if r["text"].strip()]
    logger.info(f"rotten_tomatoes: {len(out)} raw rows (train+val+test pooled, we re-split ourselves)")
    return out


@logger.catch(reraise=True)
def load_sst2() -> list[dict[str, Any]]:
    # sst2 test split labels are masked (-1) per the GLUE leaderboard convention;
    # use only train + validation, which carry real labels.
    rows = []
    for split in ["train", "validation"]:
        rows.extend(load_json(RAW_DIR / f"full_stanfordnlp_sst2_default_{split}.json"))
    out = [{"text": r["sentence"].strip(), "label": int(r["label"])} for r in rows if r["sentence"].strip() and r["label"] != -1]
    logger.info(f"sst2: {len(out)} raw rows (train+validation only, test excluded: masked labels)")
    return out


@logger.catch(reraise=True)
def load_tweet_eval() -> list[dict[str, Any]]:
    rows = []
    for split in ["train", "validation", "test"]:
        rows.extend(load_json(RAW_DIR / f"full_cardiffnlp_tweet_eval_sentiment_{split}.json"))
    n_before = len(rows)
    # 3-class: 0=negative, 1=neutral, 2=positive. Drop neutral, remap {0:0, 2:1}.
    kept = [r for r in rows if r["label"] != 1]
    out = [{"text": r["text"].strip(), "label": 0 if r["label"] == 0 else 1} for r in kept if r["text"].strip()]
    logger.info(f"tweet_eval sentiment: {n_before} raw rows -> {len(out)} after dropping neutral (label==1)")
    return out


def dedup_within(rows: list[dict[str, Any]], domain: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out = []
    n_dropped = 0
    for r in rows:
        key = _norm_text(r["text"])
        if key in seen:
            n_dropped += 1
            continue
        seen.add(key)
        out.append(r)
    logger.info(f"{domain}: dropped {n_dropped} exact-duplicate texts (within-domain), {len(out)} remain")
    return out


def cross_dedup_rt_sst2(rt: list[dict[str, Any]], sst2: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    """RT and SST-2 both derive from the Pang & Lee movie-review corpus -
    remove cross-set exact and near-duplicates (first-8-token shingle hash)."""
    rt_exact = {_norm_text(r["text"]) for r in rt}
    rt_shingle = {_shingle_key(r["text"]) for r in rt}

    kept_sst2 = []
    n_removed = 0
    for r in sst2:
        if _norm_text(r["text"]) in rt_exact or _shingle_key(r["text"]) in rt_shingle:
            n_removed += 1
            continue
        kept_sst2.append(r)
    logger.info(f"cross-dedup RT/SST-2: removed {n_removed} cross-set duplicate/near-duplicate rows from SST-2")
    return rt, kept_sst2, n_removed


def stratified_split(rows: list[dict[str, Any]], rng: random.Random) -> dict[str, Any]:
    """Build val/test/unlabeled_pool + nested train pools, class-balanced."""
    pos = [r for r in rows if r["label"] == 1]
    neg = [r for r in rows if r["label"] == 0]
    rng.shuffle(pos)
    rng.shuffle(neg)

    n_val_per_class = VAL_SIZE // 2
    n_test_per_class = TEST_SIZE // 2
    max_train_per_class = TRAIN_SIZES[-1] // 2

    min_class = min(len(pos), len(neg))
    required = n_val_per_class + n_test_per_class + max_train_per_class
    if min_class < required:
        # Scale down val/test proportionally so we never oversample a class.
        scale = min_class / required
        n_val_per_class = max(10, int(n_val_per_class * scale))
        n_test_per_class = max(20, int(n_test_per_class * scale))
        max_train_per_class = min_class - n_val_per_class - n_test_per_class
        logger.warning(
            f"Insufficient rows per class ({min_class}) for full splits; scaled down to "
            f"val={n_val_per_class * 2}, test={n_test_per_class * 2}, max_train={max_train_per_class * 2}"
        )

    val = pos[:n_val_per_class] + neg[:n_val_per_class]
    test = pos[n_val_per_class : n_val_per_class + n_test_per_class] + neg[n_val_per_class : n_val_per_class + n_test_per_class]
    train_pool_pos = pos[n_val_per_class + n_test_per_class : n_val_per_class + n_test_per_class + max_train_per_class]
    train_pool_neg = neg[n_val_per_class + n_test_per_class : n_val_per_class + n_test_per_class + max_train_per_class]

    rng.shuffle(val)
    rng.shuffle(test)

    # Nested train pools: n=50 subset of n=100 subset of ... subset of n=2000.
    train_pools: dict[str, list[dict[str, Any]]] = {}
    usable_sizes = [n for n in TRAIN_SIZES if n // 2 <= max_train_per_class]
    for n in usable_sizes:
        k = n // 2
        pool = train_pool_pos[:k] + train_pool_neg[:k]
        rng.shuffle(pool)
        train_pools[f"train_n{n}"] = pool

    # Unlabeled pool: everything left over after val/test/max-train, text only, capped.
    used_pos = set(id(r) for r in pos[: n_val_per_class + n_test_per_class + max_train_per_class])
    used_neg = set(id(r) for r in neg[: n_val_per_class + n_test_per_class + max_train_per_class])
    remainder = [r for r in pos if id(r) not in used_pos] + [r for r in neg if id(r) not in used_neg]
    rng.shuffle(remainder)
    unlabeled_pool = remainder[:UNLABELED_CAP]

    return {
        "val": val,
        "test": test,
        "train_pools": train_pools,
        "unlabeled_pool": unlabeled_pool,
        "usable_train_sizes": usable_sizes,
    }


def attach_metadata(rows: list[dict[str, Any]], domain: str, lineage_group: str, split: str) -> list[dict[str, Any]]:
    return [{"text": r["text"], "label": r["label"], "domain": domain, "lineage_group": lineage_group, "split": split} for r in rows]


@logger.catch(reraise=True)
def main() -> None:
    rng = random.Random(SEED)

    rt_raw = dedup_within(load_rotten_tomatoes(), "rotten_tomatoes")
    sst2_raw = dedup_within(load_sst2(), "sst2")
    tweet_raw = dedup_within(load_tweet_eval(), "tweet_eval")

    rt_raw, sst2_raw, n_cross_removed = cross_dedup_rt_sst2(rt_raw, sst2_raw)

    domains = {
        "rotten_tomatoes": {"rows": rt_raw, "lineage_group": "pang_lee_lineage"},
        "sst2": {"rows": sst2_raw, "lineage_group": "pang_lee_lineage"},
        "tweet_eval": {"rows": tweet_raw, "lineage_group": "independent"},
    }

    manifest: dict[str, Any] = {
        "seed": SEED,
        "train_sizes_requested": TRAIN_SIZES,
        "val_size_requested": VAL_SIZE,
        "test_size_requested": TEST_SIZE,
        "unlabeled_pool_cap": UNLABELED_CAP,
        "cross_dedup_rt_sst2_removed": n_cross_removed,
        "lineage_caveat": (
            "rotten_tomatoes and sst2 both derive from the Pang & Lee Cornell movie-review "
            "corpus (SST-2's sentences are parsed/re-split from the same underlying reviews). "
            "They are NOT independent evidence for any cross-dataset generalization claim and "
            "must be reported/weighted separately from the tweet_eval result, which is the only "
            "genuinely independent domain (social media, disjoint source corpus)."
        ),
        "domains": {},
        "source_versions": {
            "rotten_tomatoes": "cornell-movie-review-data/rotten_tomatoes (HF Hub, config=default)",
            "sst2": "stanfordnlp/sst2 (HF Hub, config=default; GLUE SST-2; test split excluded, labels masked -1)",
            "tweet_eval": "cardiffnlp/tweet_eval (HF Hub, config=sentiment; 3-class SemEval-2017 Task 4 pooled; "
            "neutral class [label==1] dropped to binarize, remap {0:negative->0, 2:positive->1})",
        },
    }

    combined: dict[str, list[dict[str, Any]]] = {
        "val": [],
        "test": [],
        "unlabeled_pool": [],
    }
    train_pools_combined: dict[str, list[dict[str, Any]]] = {f"train_n{n}": [] for n in TRAIN_SIZES}

    for domain_name, info in domains.items():
        raw_n = len(info["rows"])
        split_result = stratified_split(info["rows"], rng)
        val = attach_metadata(split_result["val"], domain_name, info["lineage_group"], "val")
        test = attach_metadata(split_result["test"], domain_name, info["lineage_group"], "test")
        unlabeled = attach_metadata(split_result["unlabeled_pool"], domain_name, info["lineage_group"], "unlabeled_pool")

        combined["val"].extend(val)
        combined["test"].extend(test)
        combined["unlabeled_pool"].extend(unlabeled)

        domain_manifest = {
            "raw_rows_after_filter_and_dedup": raw_n,
            "lineage_group": info["lineage_group"],
            "val_rows": len(val),
            "test_rows": len(test),
            "unlabeled_pool_rows": len(unlabeled),
            "usable_train_sizes": split_result["usable_train_sizes"],
            "train_pool_rows": {},
        }
        for n in TRAIN_SIZES:
            key = f"train_n{n}"
            pool = split_result["train_pools"].get(key, [])
            rows = attach_metadata(pool, domain_name, info["lineage_group"], key)
            train_pools_combined[key].extend(rows)
            domain_manifest["train_pool_rows"][key] = len(rows)

        manifest["domains"][domain_name] = domain_manifest
        logger.info(f"{domain_name}: val={len(val)} test={len(test)} unlabeled_pool={len(unlabeled)} "
                    f"train_sizes={domain_manifest['train_pool_rows']}")

    # Write per-split files: full/mini/preview.
    def write_variant(name: str, rows: list[dict[str, Any]]) -> None:
        full_path = OUT_DIR / f"full_{name}.json"
        full_path.write_text(json.dumps(rows, indent=2))
        mini_path = OUT_DIR / f"mini_{name}.json"
        mini_path.write_text(json.dumps(rows[:3], indent=2))
        preview_path = OUT_DIR / f"preview_{name}.json"
        preview_rows = []
        for r in rows[:3]:
            r2 = dict(r)
            if len(r2.get("text", "")) > 150:
                r2["text"] = r2["text"][:150] + "..."
            preview_rows.append(r2)
        preview_path.write_text(json.dumps(preview_rows, indent=2))
        logger.info(f"wrote {name}: {len(rows)} rows -> {full_path.name}")

    write_variant("val", combined["val"])
    write_variant("test", combined["test"])
    write_variant("unlabeled_pool", combined["unlabeled_pool"])
    for n in TRAIN_SIZES:
        key = f"train_n{n}"
        write_variant(key, train_pools_combined[key])

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"wrote manifest -> {manifest_path}")

    total_rows = len(combined["val"]) + len(combined["test"]) + len(combined["unlabeled_pool"]) + sum(
        len(v) for v in train_pools_combined.values()
    )
    logger.info(f"DONE. total emitted rows across all splits/domains: {total_rows}")


if __name__ == "__main__":
    main()
