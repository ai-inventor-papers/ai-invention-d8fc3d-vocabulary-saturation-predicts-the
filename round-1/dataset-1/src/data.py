# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru"]
# ///
"""Standardize the three-domain short-text sentiment corpus to exp_sel_data_out schema.

Reads the already-normalized, deduplicated, class-balanced splits written by
build_dataset.py into output/ (one JSON file per split: val, test,
train_n{50,100,200,500,1000,1500,2000}, unlabeled_pool - each row already
carries {text, label, domain, lineage_group, split}), and reshapes them into
the exp_sel_data_out.json schema: one group per dataset (domain), each row a
separate {input, output, metadata_*} example.

Nested train pools (train_n50 subset of train_n100 subset of ... subset of
train_n2000, by construction in build_dataset.py) are collapsed into a SINGLE
set of unique training examples per domain, each carrying
`metadata_train_min_n`: the smallest n in {50,100,200,500,1000,1500,2000} for
which the row is included in that domain's train pool. Because the pools are
strictly nested, a row belongs to train_n<N> for every N >= its
metadata_train_min_n - this lets a downstream experiment reconstruct any of
the 7 nested train-pool sizes by filtering on this one field, without the
example being repeated 7 times in the output (which would misrepresent
"one example = one row").

val/test/unlabeled_pool rows are disjoint from the train pool and from each
other by construction (build_dataset.py's stratified_split reserves them
before slicing train pools), so those are emitted as-is with metadata_split.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/data.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent.resolve()
OUTPUT_DIR = WORKSPACE / "output"
DATASET_DIR = WORKSPACE / "temp" / "datasets"  # raw HF downloads (see build_dataset.py)

TRAIN_SIZES = [50, 100, 200, 500, 1000, 1500, 2000]
DOMAINS = ["rotten_tomatoes", "sst2", "tweet_eval"]


def load_split(name: str) -> list[dict[str, Any]]:
    path = OUTPUT_DIR / f"full_{name}.json"
    logger.info(f"Loading {path.name}")
    rows = json.loads(path.read_text())
    assert isinstance(rows, list), f"{path} did not contain a list"
    return rows


def build_examples_for_domain(domain: str, val: list, test: list, unlabeled: list, train_by_n: dict[int, list]) -> list[dict[str, Any]]:
    """Collapse nested train pools into unique rows + metadata_train_min_n,
    then combine with val/test/unlabeled_pool (already disjoint) into one
    flat example list for this domain."""
    examples: list[dict[str, Any]] = []

    # --- val / test / unlabeled_pool: emitted as-is, disjoint by construction ---
    for split_name, rows in [("val", val), ("test", test), ("unlabeled_pool", unlabeled)]:
        for r in rows:
            examples.append(
                {
                    "input": r["text"],
                    "output": str(r["label"]),
                    "metadata_split": split_name,
                    "metadata_lineage_group": r["lineage_group"],
                    "metadata_task_type": "classification",
                    "metadata_n_classes": 2,
                }
            )

    # --- train pools: nested, so dedupe by exact text and keep the MIN n it appears at ---
    min_n_by_text: dict[str, int] = {}
    row_by_text: dict[str, dict[str, Any]] = {}
    for n in TRAIN_SIZES:
        for r in train_by_n.get(n, []):
            key = r["text"]
            row_by_text[key] = r
            if key not in min_n_by_text or n < min_n_by_text[key]:
                min_n_by_text[key] = n

    n_raw = sum(len(train_by_n.get(n, [])) for n in TRAIN_SIZES)
    logger.info(
        f"{domain}: collapsed {n_raw} nested train-pool row-occurrences into "
        f"{len(min_n_by_text)} unique train examples (min_n metadata preserves nesting)"
    )

    for key, min_n in min_n_by_text.items():
        r = row_by_text[key]
        examples.append(
            {
                "input": r["text"],
                "output": str(r["label"]),
                "metadata_split": "train",
                "metadata_train_min_n": min_n,
                "metadata_lineage_group": r["lineage_group"],
                "metadata_task_type": "classification",
                "metadata_n_classes": 2,
            }
        )

    return examples


def main() -> None:
    val_all = load_split("val")
    test_all = load_split("test")
    unlabeled_all = load_split("unlabeled_pool")
    train_all_by_n = {n: load_split(f"train_n{n}") for n in TRAIN_SIZES}

    datasets_out = []
    for domain in DOMAINS:
        val = [r for r in val_all if r["domain"] == domain]
        test = [r for r in test_all if r["domain"] == domain]
        unlabeled = [r for r in unlabeled_all if r["domain"] == domain]
        train_by_n = {n: [r for r in train_all_by_n[n] if r["domain"] == domain] for n in TRAIN_SIZES}

        examples = build_examples_for_domain(domain, val, test, unlabeled, train_by_n)
        assert len(examples) > 0, f"{domain}: produced zero examples"
        datasets_out.append({"dataset": domain, "examples": examples})
        logger.info(f"{domain}: {len(examples)} total examples "
                    f"(val={len(val)}, test={len(test)}, unlabeled_pool={len(unlabeled)}, "
                    f"train_unique={len(examples) - len(val) - len(test) - len(unlabeled)})")

    out = {
        "metadata": {
            "description": "Three-domain short-text binary-sentiment corpus (rotten_tomatoes, sst2, tweet_eval)",
            "lineage_caveat": (
                "rotten_tomatoes and sst2 share upstream Pang & Lee lineage (metadata_lineage_group="
                "'pang_lee_lineage') and are NOT independent evidence of anything; tweet_eval "
                "(metadata_lineage_group='independent') is the only genuinely independent domain."
            ),
            "train_sizes": TRAIN_SIZES,
            "train_nesting_note": (
                "Train examples are deduplicated across the 7 nested pool sizes; use "
                "metadata_train_min_n <= N to reconstruct the train_nN pool for any N in train_sizes."
            ),
        },
        "datasets": datasets_out,
    }

    out_path = WORKSPACE / "full_data_out.json"
    out_path.write_text(json.dumps(out, indent=2))
    total = sum(len(d["examples"]) for d in datasets_out)
    logger.info(f"Wrote {out_path} - {len(datasets_out)} datasets, {total} total examples")


if __name__ == "__main__":
    main()
