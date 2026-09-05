# Three-Domain Short-Text Sentiment Corpus

Normalized `{text, label, domain, lineage_group, split}` corpus assembled from
three HuggingFace Hub sources, for the small-data TF-IDF-vs-DistilBERT
learning-curve experiment.

## Sources (exact versions)

| domain | HF repo id | config | rows used (post filter+dedup) |
|---|---|---|---|
| `rotten_tomatoes` | `cornell-movie-review-data/rotten_tomatoes` | default | 10,660 (10,662 raw, 2 exact dups dropped) |
| `sst2` | `stanfordnlp/sst2` | default (GLUE SST-2) | 52,732 (68,221 raw train+validation only — test split excluded, its labels are masked `-1`; 8,736 within-domain dups dropped; **6,753 further dropped as cross-set duplicates/near-duplicates of `rotten_tomatoes`**) |
| `tweet_eval` | `cardiffnlp/tweet_eval` | `sentiment` | 32,378 (59,899 raw across train+val+test, 27,479 dropped as the neutral class [label==1] to binarize, 42 within-domain dups dropped) |

Binarization: `rotten_tomatoes` and `sst2` are natively 0=negative/1=positive.
`tweet_eval` sentiment is natively 3-class (0=negative,1=neutral,2=positive);
the neutral class is dropped and the remainder remapped {0:0 (neg), 2:1 (pos)}.

## ⚠️ Lineage caveat (read before using for any cross-domain claim)

`rotten_tomatoes` and `sst2` **both derive from the same Pang & Lee Cornell
movie-review corpus** — SST-2's sentences are Socher et al.'s constituency-parsed
re-split of the same underlying reviews. They are treated here as ONE lineage
group (`lineage_group: "pang_lee_lineage"`), and a normalized-text +
first-8-token-shingle-hash cross-check found **6,753 SST-2 rows that were
exact or near duplicates of `rotten_tomatoes` rows** — these were removed from
the SST-2 pool before splitting. Even after that removal, RT and SST-2 are
**not independent evidence** of anything — treat them as one calibration
source. `tweet_eval` (`lineage_group: "independent"`) is the only genuinely
independent domain (disjoint source corpus, social-media register) and is
what should carry any "does this generalize across truly distinct domains"
claim. See `manifest.json`'s `lineage_caveat` field.

## Files

- `full_val.json` / `full_test.json` — fixed held-out sets, class-balanced,
  500 and 1000 rows per domain respectively (1500 / 3000 rows combined
  across the 3 domains).
- `full_train_n{50,100,200,500,1000,1500,2000}.json` — nested labeled train
  pools per domain, class-balanced, seeded (seed=42) so every smaller-n pool
  is a strict subset of every larger-n pool for the same domain — enables
  matched-seed learning-curve comparisons.
- `full_unlabeled_pool.json` — remaining raw text (label still present but
  intended for unsupervised use only, e.g. the Good-Turing/Chao1 subsampling
  curve), capped at 10,000 rows/domain.
- `manifest.json` — exact source versions, row counts before/after
  filtering and dedup, per-domain split sizes, and the lineage caveat.
- Every `full_*.json` has matching `mini_*.json` (first 3 rows) and
  `preview_*.json` (first 3 rows, text truncated to 150 chars) variants.

Each row: `{"text": str, "label": 0|1, "domain": "rotten_tomatoes"|"sst2"|"tweet_eval", "lineage_group": "pang_lee_lineage"|"independent", "split": "val"|"test"|"train_n{N}"|"unlabeled_pool"}`.

## Sanity check (TF-IDF(1-2gram) + LogisticRegression, n_train=1000)

| domain | test accuracy (n_test=1000) |
|---|---|
| rotten_tomatoes | 0.652 |
| sst2 | 0.701 |
| tweet_eval | 0.745 |

All three domains show clear above-chance (50%) signal, confirming the
corpus supports the planned TF-IDF-vs-DistilBERT small-data comparison.

## Total size

~13 MB across all full/mini/preview files — well under the 300 MB cap.
