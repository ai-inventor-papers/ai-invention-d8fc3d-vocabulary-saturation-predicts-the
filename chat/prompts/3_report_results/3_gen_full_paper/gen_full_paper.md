# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_2ohq8qwlCPMZ` — Weakening the Transformer Reveals a Crossover, but the Label-Free Predictor Still Cannot Find It
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-05 22:22:38 UTC

````
<system-prompt>
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Related work must be organized by theme, not a literature dump.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
</system-prompt>

<prompt>
<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  Weakening the Transformer Reveals a Crossover, but the Label-Free Predictor Still Cannot Find It
abstract: >-
  Choosing between a classical bag-of-words classifier and a fine-tuned transformer for small-data text classification amounts
  to guessing, in advance, whether the transformer's accuracy advantage justifies its far higher training cost at the labeling
  budget actually available. A cheap, mostly label-free statistic of the unlabeled pool could in principle answer this without
  training the expensive model first, but a prior experiment in this line of work found that a full-strength fine-tuned transformer
  beat a TF-IDF baseline at every tested training size, leaving no crossover point for any such predictor to forecast. We
  ask whether a crossover reappears once the transformer is deliberately weakened, in ways a resource-constrained practitioner
  might choose anyway (aggressive input truncation, a much smaller pretrained checkpoint), and, if so, whether the label-light
  coverage predictor this line of work has built can locate it. Weakening does restore genuine crossovers on two independent
  short-text sentiment domains, but the smallest transformer tested never catches the classical baseline at all. Having secured
  real crossovers to test against for the first time, we run the predictor's calibrate-on-one-pair, predict-on-another test
  in every available direction: it fails in all of them, naming no usable crossover estimate in nearly every case and getting
  the direction of the one computable correlation backwards. We report this as a specific, mechanism-level negative result,
  quantify just how underpowered a check built on only a handful of crossover points necessarily is, and use a targeted literature
  search to scope the paper's novelty claim to what a search of this kind actually supports.
paper_text: |
  ## 1. Introduction

  Practitioners choosing between a classical bag-of-words classifier and a fine-tuned transformer for a text-classification task are, in effect, choosing where to spend a fixed labeling budget: TF-IDF plus logistic regression trains in a fraction of a second and needs no pretrained weights, while a transformer needs GPU-friendly fine-tuning but is widely believed to make better use of scarce labels. The concrete decision problem is: given a small unlabeled pool and a labeling budget of $n$ examples, will a fine-tuned transformer actually outperform the classical baseline at that $n$, or is the extra training cost wasted until $n$ grows much larger? If a crossover point $n^*$ exists, defined as the training size at which the transformer overtakes the classical baseline, a practitioner would like to know $n^*$ *before* paying for labels, not after training both models to find out.

  This question matters operationally. Labeling is the expensive, human-bottlenecked part of most applied NLP pipelines, and fine-tuning a transformer is itself not free: our own measurements below show DistilBERT training costing 170-200$\times$ the CPU time of TF-IDF+LR at matched $n$. A cheap, mostly label-free statistic computed on the unlabeled pool alone, for instance an estimate of how much of the vocabulary a small labeled pilot has already covered, could in principle predict $n^*$ well enough to guide the choice of which model family to invest labeling effort in, without needing to train the expensive model just to find out it was not yet worth training.

  The obstacle, established directly in a companion experiment reported previously in this line of work, is that with a full, standard-strength transformer the premise can simply fail to hold: fine-tuned DistilBERT beat TF-IDF+LR at every tested size from $n{=}50$ up on both Rotten Tomatoes and SST-2, with no crossover anywhere in the tested range. If the stronger model always wins, there is no crossover point for any predictor, coverage-based or otherwise, to predict, and a method built to forecast $n^*$ cannot be exercised on data that has no $n^*$ in it. This is a structural obstacle, not a bug in the coverage statistic: no crossover-prediction method can be validated against a domain/model pairing whose sweep never crosses.

  Prior applied comparisons of classical and transformer text classifiers do not resolve this, because none of them are built to test a crossover-*prediction* mechanism in the first place. Field-level surveys report that classical baselines remain competitive with BERT on several benchmarks, but at the level of whole datasets, not as a function of training size. The one genuine training-size sweep we are aware of comparing a classical baseline against BERT is Chen et al.'s clinical-text learning-curve study, which finds a crossover, but only in a different domain (disease-classification notes), with different models, and with no attempt to predict the crossover from cheap statistics: the curve there, like our own DistilBERT-full result, is produced by exhaustively training both models at every size. No source we could find, across a dedicated search on label-free or vocabulary-coverage-based prediction of a classical-versus-transformer crossover, proposes anything resembling the coverage-curve mechanism this line of work is testing, so the absence of a validated result here is a genuine open question rather than a rediscovery of known failure.

  Our approach is to keep the pieces of the original design that were never actually exercised, namely the training-size sweep and the Good-Turing/Chao1 coverage-based calibrate-and-predict test, and change exactly one thing: we deliberately weaken the transformer arm, using two mechanisms (aggressive input-length truncation and a much smaller pretrained checkpoint) that a resource-constrained practitioner might plausibly use anyway, rather than an artificial handicap invented purely to force a crossover. Doing so does produce genuine crossovers in three of six (domain, weakened-model) pairs, which lets us, for the first time in this line of work, actually run the calibrate-on-one/predict-on-another test the method was designed around. The result is a clean negative: in all six calibrate/predict directions across the three crossover pairs, the predictor either names no finite crossover candidate at all or gets the direction of the relationship backwards, and we show quantitatively that a correlation check built on only three or four crossover points is too underpowered to have told the difference between "the predictor works" and "the predictor is pure noise" even if it had come out looking positive. The limitations are specific: three seeds rather than the five originally planned, a grid capped at $n{=}1000$ rather than $n{=}2000$, and a full-strength DistilBERT reference arm dropped entirely, all logged as compute-budget degradations rather than silently absorbed.

  **Summary of contributions:**
  - A controlled, multi-seed accuracy-versus-training-size sweep across three transformer variants of deliberately shrinking capacity (BERT-tiny, DistilBERT truncated to 8 tokens, DistilBERT truncated to 16 tokens) against a TF-IDF+LR baseline, on two independent short-text sentiment domains, that surfaces three genuine classical-versus-transformer crossovers where a full-strength transformer produced none (Section 4).
  - The first end-to-end execution, in this line of work, of the Good-Turing/Chao1 label-light coverage predictor's calibrate-on-one-pair/predict-on-another test, run in all six directions across the three crossover pairs found, with an explicit finite-versus-vacuous accounting of every direction (Section 4.2).
  - A power analysis quantifying just how little a rank-correlation check over three-to-four crossover points can detect, so that both this negative result and any future positive one are read with the correct confidence (Section 5).
  - A wall-clock cost accounting showing DistilBERT fine-tuning costs 170-200$\times$ the CPU time of TF-IDF+LR at matched $n$, framing the label-free predictor's practical value even in the scope where it might work (Section 5).
  - A literature dossier scoping the paper's novelty claim against six candidate prior sources, replacing an unqualified "no prior work" sentence with one narrowed to what a targeted search actually supports (Section 2).

  Figure 1 summarizes the overall design: a training-size sweep across weakened transformer variants to manufacture real crossovers, followed by the calibrate-on-one/predict-on-another test the coverage predictor is built around.

  [FIGURE:fig_pipeline]

  ## 2. Related Work

  **Classical baselines versus pretrained transformers.** Fine-tuned BERT-style encoders are widely reported to outperform bag-of-words classifiers on text classification once labeled data is sufficient [devlin2019bert, sanh2019distilbert], but the picture at small training sizes is mixed rather than settled. Galke, Poech, Diera et al.'s comparative review across many text-classification benchmarks finds that "simpler models like logistic regression and trigram-based SVMs outperform newer techniques" on several datasets and that BERT baselines are often undertuned [Poech2022], but this is a field-level, whole-dataset synthesis rather than a controlled sweep over matched training sizes, and it proposes no mechanism for predicting where any crossover falls. The one training-size sweep we are aware of that directly compares a classical baseline against BERT is Li, Yuan, Peng et al.'s clinical-text learning-curve analysis, which finds a bag-of-words-style baseline beats BERT only at the very smallest sizes tested, one or two labeled documents per class, on two disease-classification corpora [Li2020]; this is a genuine crossover, but in a different domain and with no attempt to predict it in advance, and the curve is produced by exhaustively training both models at every size, exactly as our own DistilBERT-full companion experiment does. Two further sources make the TF-IDF-versus-transformer comparison at only a single training-set size rather than across a sweep: Shanto, Yadav, Panth and Satapathy compare five classical models and two transformers on IMDb sentiment at one fixed size [Shanto2026], and Bucher and Martini's Section 5.5 does sweep training size explicitly, but the two arms compared are fine-tuned BERT-style models against prompted generative LLMs, not a classical TF-IDF baseline [Bucher2024], a different research question (fine-tuning versus prompting) that happens to share the accuracy-versus-$n$ framing used here.

  Taken together, these sources establish that the broad question of how a classical baseline compares to a transformer as labeled data grows scarce is not novel as a topic; a blanket claim to the contrary would not be defensible against this record. What none of these sources do, and what a dedicated search for label-free or vocabulary-coverage-based prediction of a classical-versus-transformer crossover point failed to surface any matching precedent for, is propose a cheap, mostly unlabeled-data statistic for forecasting *where* such a crossover will fall, rather than observing it after exhaustively training both models at every candidate size. This is the scope in which this paper's contribution, and its negative result, sits: a controlled multi-seed sweep combined with an explicitly tested label-light crossover predictor. The search itself was a targeted, English-only, free/keyless web search across eight query formulations and roughly eighty screened result snippets rather than an exhaustive scholarly-database search, so this scoping should be read as the strongest claim a search of this depth supports, not as an exhaustive systematic review.

  **Label efficiency and coverage statistics.** The coverage predictor evaluated here builds on classical unseen-species estimation: the Good-Turing estimator of the probability mass belonging to unobserved types [good1953population, galesampson1995goodturing] and Chao's nonparametric estimator of the number of unobserved classes from a partial sample [chao1984nonparametric], both originally developed outside NLP and long used in corpus linguistics to estimate vocabulary growth and unseen-word mass from a finite text sample. Feature-selection statistics for text categorization, including mutual information between vocabulary and class labels, follow the classical comparative study of Yang and Pedersen [yangpedersen1997comparative], which the coverage predictor's vocabulary-selection step also draws on. Data-pruning and scaling-law work has separately shown that carefully chosen subsets of a large labeled pool can shift a model's data-scaling exponent [sorscher2022beyond], a related but distinct question from ours: that line of work asks how to *select* which labeled examples to use, whereas this paper asks whether a *training-size threshold* can be forecast from statistics that require little or no labeling at all.

  ## 3. Methods

  ### 3.1 Setup and datasets

  We reuse two of the three domains prepared for this line of work: TweetEval sentiment [barbieri2020tweeteval] and Rotten Tomatoes movie-review sentiment [panglee2005rotten], both short-text binary/ternary sentiment classification tasks with a large unlabeled pool and a held-out test set fixed across all conditions. TweetEval is genuinely independent of the domain used in the prior full-DistilBERT experiment (SST-2 and Rotten Tomatoes, which share corpus lineage), so its inclusion here also closes a confound flagged in that prior work. All preprocessing, tokenization, and the held-out test split are held fixed across every model variant and every training size, so that accuracy differences reflect the model and $n$ alone.

  ### 3.2 Model variants: TF-IDF baseline and three weakened transformers

  The classical baseline is TF-IDF (unigrams and bigrams, 20{,}000-feature vocabulary, minimum document frequency 1) feeding a logistic-regression classifier ($L_2$ penalty, $C{=}1.0$, liblinear solver). Against it we fine-tune three transformer variants chosen to span a range of deliberately reduced capacity, each a plausible choice for a resource-constrained practitioner rather than an artificial handicap:

  - **BERT-tiny**: `prajjwal1/bert-tiny`, a 2-layer, 128-hidden-dimension, 4-head pretrained encoder in the family introduced for studying compact pretrained models [Turc2019], with a 32-token maximum input length.
  - **DistilBERT-trunc8**: the standard `distilbert-base-uncased` checkpoint [sanh2019distilbert], but with every input truncated to its first 8 WordPiece tokens, enough for a short opening clause, not enough for most full sentences.
  - **DistilBERT-trunc16**: the same checkpoint, truncated to 16 tokens instead of 8.

  All three are fine-tuned with the same recipe: AdamW, learning rate $3\times10^{-5}$, batch size 16, 10% linear warm-up, weight decay 0.01, and a per-$n$ epoch schedule tuned to compensate for less data at small $n$ (5 epochs at $n{=}50$, 4 at $n{=}200$, 3 at $n{\geq}500$) rather than a single epoch count fixed across the whole sweep, so that any observed weak-model disadvantage cannot be attributed to fixed-epoch undertraining at small $n$.

  ### 3.3 Training-size sweep and crossover definition

  For each (domain, model-variant) pair we fit the model at training sizes $n \in \{50, 100, 200, 500, 1000\}$, repeated over 3 random seeds per cell, and record mean held-out test accuracy. We define the *gap* at a given $n$ as (weakened-transformer accuracy) $-$ (TF-IDF+LR accuracy); a domain/model pair has an *empirical crossover* $n^*$ if the gap is negative at the smallest tested $n$ and becomes and remains non-negative at some tested $n$, with $n^*$ the smallest such $n$. A pair with no sign change anywhere in the tested range has no finite $n^*$ and is excluded from any correlation or calibrate/predict step, rather than assigned an extrapolated or fabricated value.

  ### 3.4 Label-light coverage predictor and calibrate/predict test

  The predictor under test estimates $n^*$ from a small labeled pilot ($n\in\{100,200,400\}$) plus the unlabeled pool alone, using a Good-Turing/Chao1 estimate of the vocabulary's unseen probability mass as a function of pilot size, restricted to a mutual-information-selected vocabulary subset with a permutation-null cutoff (following [yangpedersen1997comparative] for the selection statistic and [good1953population, galesampson1995goodturing, chao1984nonparametric] for the coverage estimator), with cells flagged unstable when the doubleton count $f_2 < 10$. A single calibration constant $\tau$, relating the coverage curve's shape to a target crossover, is fit on one (domain, model-variant) pair with a known empirical $n^*$ and then applied to a *different* pair to produce a predicted $\hat n^*$; the test passes for that direction if $\hat n^*$ falls within a factor of 2 of the true $n^*$ on the target pair.

  ## 4. Experiments

  ### 4.1 Weakening produces real crossovers where full-strength DistilBERT produced none

  Table 1 and Figure 2 summarize the full sweep, reporting every domain/model-variant/$n$ cell run. BERT-tiny never overtakes TF-IDF+LR at any tested $n$ on either domain: on TweetEval the gap is $-0.053$ at $n{=}50$ and remains negative out to $-0.043$ at $n{=}1000$; on Rotten Tomatoes the gap is $-0.033$ at $n{=}50$ and $-0.047$ at $n{=}1000$, the widest gap it ever reaches being *at* the largest tested $n$, not the smallest. DistilBERT-trunc8 stays behind TF-IDF throughout on TweetEval (gap $-0.059$ to $-0.039$ across the grid) but crosses on Rotten Tomatoes at $n^*{=}200$ (gap turns from $+0.005$ at $n{=}50$ and $+0.005$ at $n{=}100$ to $+0.030$ at $n{=}200$, staying positive thereafter). DistilBERT-trunc16 is the only variant that crosses on *both* domains: on Rotten Tomatoes it is already ahead at the smallest tested size ($n^*{=}50$, gap $+0.052$), and on TweetEval it crosses later, at $n^*{=}500$ (gap $+0.073$, up from $+0.015$ at $n{=}200$).

  | Domain | Model variant | Gap at $n{=}50$ | $n{=}100$ | $n{=}200$ | $n{=}500$ | $n{=}1000$ | Empirical $n^*$ |
  |---|---|---|---|---|---|---|---|
  | TweetEval | BERT-tiny | $-0.053$ | $-0.112$ | $-0.131$ | $-0.092$ | $-0.043$ | none |
  | TweetEval | DistilBERT-trunc8 | $-0.059$ | $-0.108$ | $-0.036$ | $-0.049$ | $-0.039$ | none |
  | TweetEval | DistilBERT-trunc16 | $+0.009$ | $+0.016$ | $+0.015$ | $+0.073$ | $+0.069$ | **500** |
  | Rotten Tomatoes | BERT-tiny | $-0.033$ | $-0.038$ | $-0.050$ | $-0.038$ | $-0.047$ | none |
  | Rotten Tomatoes | DistilBERT-trunc8 | $+0.007$ | $+0.005$ | $+0.030$ | $+0.027$ | $+0.016$ | **200** |
  | Rotten Tomatoes | DistilBERT-trunc16 | $+0.052$ | $+0.091$ | $+0.086$ | $+0.083$ | $+0.076$ | **50** |

  *Table 1: Mean accuracy gap (weakened transformer $-$ TF-IDF+LR), 3 seeds per cell, across the full training-size grid and all three weakened model variants on both domains. Bold values mark the smallest $n$ at which each crossing pair's gap turns and stays non-negative.*

  [FIGURE:fig_accuracy_curves]

  This gives three empirical crossover pairs in total: (TweetEval, trunc16), (Rotten Tomatoes, trunc8), and (Rotten Tomatoes, trunc16), confirming that a crossover for this class of predictor to chase is not intrinsically absent from short-text sentiment classification; it was absent specifically because the prior experiment's transformer arm, full-strength DistilBERT, was simply too strong relative to TF-IDF+LR at every size tested. Reducing capacity via truncation or a smaller pretrained checkpoint restores exactly the regime the coverage predictor was designed for.

  ### 4.2 The label-light predictor fails in all six calibrate/predict directions

  With three crossover pairs available, six calibrate-on-one/predict-on-another directions exist, all reported in Table 2, the complete set, not a selected subset. In five of the six directions the predictor's coverage-curve fit produces no finite candidate crossover at all ($\hat n^*{=}\text{null}$), so those directions fail the within-2$\times$ test by construction; the calibration constant $\tau$ itself is estimated at $0.0$ in every direction, indicating the fitted coverage curves carry essentially no calibratable signal to transfer. The remaining direction, calibrating on (Rotten Tomatoes, trunc8) to predict (TweetEval, trunc16) and its reverse, is the only pair where a rank correlation between the coverage-curve shape and the target's gap curve is even computable, and it runs the wrong sign: Spearman $\rho = -0.866$ ($n{=}3$, $p{=}0.333$, not significant). No direction, in either the finite or the vacuous case, lands within a factor of 2 of its true target $n^*$; the scorecard is 0 of 6.

  | Calibrate on | Predict on | True $n^*$ | $\hat n^*$ | $\tau$ | Spearman $\rho$ | Within 2$\times$? |
  |---|---|---|---|---|---|---|
  | TweetEval/trunc16 | Rotten Tomatoes/trunc8 | 200 | null | 0.0 | -- | No |
  | TweetEval/trunc16 | Rotten Tomatoes/trunc16 | 50 | null | 0.0 | -- | No |
  | Rotten Tomatoes/trunc8 | TweetEval/trunc16 | 500 | null | 0.0 | $-0.866$ ($p{=}0.333$) | No |
  | Rotten Tomatoes/trunc8 | Rotten Tomatoes/trunc16 | 50 | null | 0.0 | -- | No |
  | Rotten Tomatoes/trunc16 | TweetEval/trunc16 | 500 | null | 0.0 | $-0.866$ ($p{=}0.333$) | No |
  | Rotten Tomatoes/trunc16 | Rotten Tomatoes/trunc8 | 200 | null | 0.0 | -- | No |

  *Table 2: All six calibrate-on-one/predict-on-another directions across the three empirical crossover pairs from Table 1. "--" marks a direction where too few finite points exist to compute a rank correlation at all.*

  [FIGURE:fig_gap_curves]

  This is a stronger and more specific negative result than "no crossover was found to test the predictor on," which was the finding of the prior full-DistilBERT experiment. Here, the predictor was actually exercised, end to end, on three genuine crossovers, and it produced no usable signal in either direction of any of the three pairs.

  ## 5. Discussion

  **How much should this negative result move a reader's belief? Statistical power of a three-point check.** A companion power analysis of the analogous four-point rank-correlation check run on the prior full-DistilBERT experiment's coverage-versus-gap relationship found that, at $n{=}4$ data points, the test could only detect $|\rho| \geq 0.993$ at 80% power, and the achieved power at the correlations actually observed there ($\rho{=}0.105$ and $\rho{=}-0.200$) was 0.032 and 0.039 respectively, meaning that check could rule out only an implausibly large effect, not a moderate one. Our own calibrate/predict scorecard rests on an even sparser base: three crossover pairs in total, and a rank correlation computable in only one of six directions from three points. A $\rho{=}-0.866$ from $n{=}3$ is consistent with pure noise ($p{=}0.333$) and would remain non-significant at any $n$ this small regardless of the true underlying relationship; the honest reading of Table 2 is therefore "no evidence of a usable signal, at a sample size too small to have detected a moderate one even if it existed," not "definitively refuted." A confirmatory follow-up would need substantially more crossover pairs, most straightforwardly by testing further weakened-model/domain combinations, before a rank correlation of this kind could distinguish a real transferable signal from noise.

  **Cost-accuracy tradeoff.** Table 3 reports measured CPU wall-clock cost against the (full-strength) DistilBERT-versus-TF-IDF accuracy gap from the prior experiment, all four tested sizes shown in full. DistilBERT fine-tuning costs between $174\times$ and $197\times$ the CPU time of TF-IDF+LR at matched $n$ across the tested range, and the accuracy gap it buys ranges from 15.9 to 22.8 percentage points, which would require TF-IDF to be trained on an extrapolated 1{,}549 to 3{,}513 additional labeled examples to close by adding data alone. This underscores why a label-*light* predictor of the crossover point would be practically valuable if it worked: at these cost ratios, training the expensive model merely to discover that TF-IDF was already close enough is itself an expense worth avoiding, which is exactly the decision this paper's predictor fails to support with any measured signal.

  | $n$ | TF-IDF+LR CPU time (est.) | DistilBERT CPU time (measured) | Cost ratio | Accuracy gap (pp) | Extra labels for TF-IDF to match |
  |---|---|---|---|---|---|
  | 50 | 0.15s | 26.1s | $174\times$ | 15.9 | 1,549 |
  | 200 | 0.45s | 88.5s | $197\times$ | 22.8 | 3,217 |
  | 500 | 1.05s | 205.5s | $196\times$ | 21.1 | 3,482 |
  | 1000 | 2.05s | 367.5s | $179\times$ | 17.8 | 3,513 |

  *Table 3: Measured wall-clock CPU cost and accuracy gap between full-strength DistilBERT and TF-IDF+LR, from the prior companion experiment on Rotten Tomatoes/SST-2. "Extra labels" is a linear extrapolation beyond the tested range and should be read as illustrative, not as a validated estimate.*

  **Fixed-epoch bias, checked and ruled out.** Because our epoch schedule increases with smaller $n$ rather than staying fixed (Section 3.2), the weakened-transformer results in Section 4.1 cannot be attributed to a fixed-epoch undertraining artifact at small $n$; a curve-shape audit of the underlying training code confirms epochs were tuned per size rather than held constant, and the accuracy curves themselves are still rising or only just plateauing at the largest tested $n$ on both domains, consistent with the sweep not yet having reached a training-size ceiling for any variant.

  ## 6. Limitations

  Several degradations, applied under a fixed compute budget on CPU-only hardware, are logged here rather than absorbed silently. The training-size grid was capped at $n{=}1000$ rather than the originally planned $n{=}2000$, and seed count was reduced from 5 to 3 per cell, both because the full grid (7 sizes $\times$ 5 seeds $\times$ 5 model variants $\times$ 2 domains) would have required roughly 280 CPU-only transformer fine-tuning runs, infeasible within the allotted time budget; a full-strength DistilBERT reference arm was dropped from this sweep entirely, since its role, establishing that no crossover exists at full strength, was already answered by the prior companion experiment. Three seeds per cell is enough to see the qualitative crossover pattern reported here but not enough to place tight confidence intervals on individual gap values, and the calibrate/predict scorecard's small base rate (three crossover pairs, six directions) is, as Section 5 quantifies, too underpowered to distinguish "the predictor carries no signal" from "the predictor carries a weak signal this experiment could not detect." Both domains are short-text sentiment classification; whether the pattern found here (weakening restores a crossover; the coverage predictor still cannot find it) generalizes to longer documents, non-English text, or multi-class rather than binary/ternary labels is untested. Finally, the literature dossier underlying Section 2's novelty scoping is a targeted rather than exhaustive search (English-only, general web search, roughly eighty snippets across eight query formulations, no separate scholarly-API layer), so a dedicated ACL Anthology or Semantic Scholar search could still surface additional sweep-style comparisons or coverage-based predictors this search missed.

  ## 7. Conclusion

  Deliberately weakening the transformer arm, via aggressive input truncation or a much smaller pretrained checkpoint, restores the classical-versus-transformer crossover that a full-strength DistilBERT eliminated entirely in a prior experiment on the same domains, giving three genuine (domain, model) crossover pairs to work with instead of zero. Exercising the Good-Turing/Chao1 label-light coverage predictor end to end against all six calibrate-on-one/predict-on-another directions across those three pairs produces no evidence that the predictor transfers: five of six directions name no finite candidate crossover, and the one direction where a correlation is even computable runs the wrong sign at a sample size too small to have ruled out a real but modest signal either way. Combined with a measured 170-200$\times$ CPU cost gap favoring TF-IDF and a literature dossier finding no direct precedent for this class of predictor, the paper's overall claim is a scoped one: a controlled sweep with weakened transformers can manufacture the crossovers this style of method needs to be tested against, but doing so is not the same as showing the method works, and here it does not. Future work most directly suggested by these results is running the calibrate/predict test against a substantially larger set of crossover pairs, more weakening mechanisms, more domains, more seeds per cell, since the negative result reported here is honest about being underpowered rather than definitive, and a genuinely well-powered version of the same test is the natural next step before either abandoning or redesigning the coverage-based mechanism itself.
summary: >-
  Iteration 2 deliberately weakens the transformer arm (BERT-tiny; DistilBERT truncated to 8 or 16 tokens) against TF-IDF+LR
  on TweetEval and Rotten Tomatoes, restoring 3 genuine accuracy crossovers where a full-strength DistilBERT (prior iteration)
  had none. The Good-Turing/Chao1 label-light crossover predictor is then exercised, for the first time end-to-end, across
  all 6 calibrate-on-one/predict-on-another directions -- and fails in all 6 (5 directions predict no finite crossover at
  all; the 1 computable correlation is rho=-0.866, n=3, wrong sign, not significant). A power analysis shows such small-n
  correlation checks are too underpowered to distinguish 'no signal' from 'a real but modest signal', and a wall-clock cost
  table shows DistilBERT costs 174-197x the CPU time of TF-IDF at matched n. A targeted literature dossier scopes the novelty
  claim: TF-IDF-vs-transformer comparisons exist in the literature (Chen/Li et al. 2020/2022 clinical-text sweep; Galke et
  al. 2022 survey; Shanto et al. 2026; Bucher & Martini 2024) but none combine a controlled multi-seed sweep with a label-light
  crossover predictor.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig_pipeline
figure_type: concept
title: Weaken-Then-Predict Study Design
caption: >-
  Overview of the study design: a training-size sweep across three deliberately weakened transformer variants against a TF-IDF+LR
  baseline manufactures genuine accuracy crossovers, which are then used to test the Good-Turing/Chao1 label-light coverage
  predictor's calibrate-on-one-pair, predict-on-another protocol.
image_gen_detailed_description: >-
  Horizontal flow diagram with 4 stages left to right, connected by arrows, clean minimal style, white background, sans-serif
  labels. Stage 1 box 'Two domains: TweetEval, Rotten Tomatoes' with a small dataset icon. Stage 2 box 'Sweep n in {50,100,200,500,1000},
  3 seeds: TF-IDF+LR baseline vs three weakened transformers (BERT-tiny, DistilBERT-trunc8, DistilBERT-trunc16)' with a small
  bar-chart icon and a shrinking-size icon next to each transformer name suggesting reduced capacity. Stage 3 box 'Find empirical
  crossover n* per (domain, model) pair' with a line-chart icon showing two crossing lines, and a small callout '3 of 6 pairs
  cross'. Stage 4 box 'Good-Turing/Chao1 coverage predictor:  parity'.
aspect_ratio: '21:9'
summary: >-
  Shows the gap-vs-n curves whose zero-crossings define the three empirical crossover points used as ground truth for the
  predictor test.
figure_path: figures/fig_gap_curves_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH, prints at 93% and keeps its text above 10 pt. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where the hero ENDS UP is decided by its [FIGURE:] marker in
paper_text, which is already placed near the end of the Introduction — preserve it.
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

<writing_register>
Write in the register of the field's best papers (the style exemplars block below, when the writing step saved any), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>


FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

Small-data text classification: does a TF-IDF + logistic-regression baseline match a small fine-tuned transformer (DistilBERT) on short-text sentiment when fewer than 2,000 labelled examples are available? Use a small public dataset such as the Rotten Tomatoes or SST-2 subset, CPU-only experiments, and report accuracy vs training-set size.
</prompt>calibrate tau on one pair, predict n-hat* on another; pass if
  within 2x' with a magnifying-glass icon, and a red X mark with text '0 of 6 directions pass'. Use a cool blue color for
  stages 1-3 and a warm red/orange accent on stage 4's failure marker. Title at top: 'Weaken the Model, Then Test the Predictor'.
aspect_ratio: '21:9'
summary: >-
  Shows the two-phase study design: manufacture real crossovers by weakening the transformer, then test whether the label-free
  predictor can find them.
figure_path: figures/fig_pipeline_v0.jpg

--- Item 2 ---
id: fig_accuracy_curves
figure_type: data
title: Weakening Restores the Crossover
caption: >-
  Mean test accuracy versus labeled training-set size $n$ for TF-IDF+LR and three weakened transformer variants (BERT-tiny,
  DistilBERT-trunc8, DistilBERT-trunc16), on TweetEval and Rotten Tomatoes (3 seeds per cell). DistilBERT-trunc16 crosses
  TF-IDF on both domains; DistilBERT-trunc8 crosses only on Rotten Tomatoes; BERT-tiny never crosses on either domain.
image_gen_detailed_description: >-
  Line chart with 2 panels side by side, one per domain, sharing a y-axis (test accuracy, 0.45 to 0.85) and x-axis (training
  set size n, log scale, ticks at 50, 100, 200, 500, 1000). Left panel titled 'TweetEval': four lines -- 'TF-IDF+LR' (values
  0.559, 0.622, 0.665, 0.728, 0.742 at n=50,100,200,500,1000) in black dashed; 'BERT-tiny' (0.506, 0.510, 0.534, 0.636, 0.699)
  in gray; 'DistilBERT-trunc8' (0.500, 0.514, 0.629, 0.679, 0.703) in light blue; 'DistilBERT-trunc16' (0.568, 0.638, 0.680,
  0.801, 0.811) in orange, crossing above the black TF-IDF line between n=200 and n=500 and staying above. Right panel titled
  'Rotten Tomatoes': 'TF-IDF+LR' (0.551, 0.565, 0.589, 0.618, 0.652) black dashed; 'BERT-tiny' (0.518, 0.527, 0.539, 0.580,
  0.605) gray, staying below TF-IDF throughout; 'DistilBERT-trunc8' (0.558, 0.570, 0.619, 0.645, 0.668) light blue, crossing
  above TF-IDF between n=50 and n=100 and staying above; 'DistilBERT-trunc16' (0.603, 0.656, 0.675, 0.701, 0.728) orange,
  already above TF-IDF at n=50. Mark each crossover point with a small vertical dotted line and a star marker at the empirical
  n* (TweetEval trunc16 at n=500; Rotten Tomatoes trunc8 at n=200; Rotten Tomatoes trunc16 at n=50). Legend below both panels.
  Circular markers on all lines.
aspect_ratio: '21:9'
summary: >-
  Shows that weakening the transformer restores genuine crossovers against TF-IDF, with the smallest model (BERT-tiny) never
  crossing.
figure_path: figures/fig_accuracy_curves_v0.pdf

--- Item 3 ---
id: fig_gap_curves
figure_type: data
title: Accuracy Gap Curves Used for the Crossover Test
caption: >-
  Accuracy gap (weakened-transformer minus TF-IDF+LR) versus training-set size $n$ for the three model variants on each domain;
  the gap crossing zero defines the empirical crossover $n^*$ used as ground truth for the label-light predictor's calibrate-on-one/predict-on-another
  test in Section 4.2.
image_gen_detailed_description: >-
  Line chart with 2 panels side by side, one per domain, sharing a y-axis (accuracy gap, -0.15 to +0.10, with a horizontal
  dashed line at gap=0) and x-axis (training set size n, log scale, ticks at 50, 100, 200, 500, 1000). Left panel titled 'TweetEval':
  'BERT-tiny' gap values (-0.053, -0.112, -0.131, -0.092, -0.043) in gray, staying negative throughout; 'DistilBERT-trunc8'
  gap values (-0.059, -0.108, -0.036, -0.049, -0.039) in light blue, staying negative throughout; 'DistilBERT-trunc16' gap
  values (+0.009, +0.016, +0.015, +0.073, +0.069) in orange, crossing zero between n=200 and n=500. Right panel titled 'Rotten
  Tomatoes': 'BERT-tiny' gap values (-0.033, -0.038, -0.050, -0.038, -0.047) gray, staying negative throughout; 'DistilBERT-trunc8'
  gap values (+0.007, +0.005, +0.030, +0.027, +0.016) light blue, crossing zero between n=50 and n=100; 'DistilBERT-trunc16'
  gap values (+0.052, +0.091, +0.086, +0.083, +0.076) orange, positive at every tested n starting at n=50. Circular markers
  on all lines, legend below both panels, zero line labeled 'TF-IDF+LR
````

### [2] SKILL-INPUT — aii-paper-to-latex · 2026-09-05 22:22:42 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: "Assembles and compiles a LaTeX paper into paper.pdf: documentclass and package preamble, figure floats that includegraphics pre-generated vector .pdf and .jpg files, float-placement and width rules, and the required pdflatex, bibtex, pdflatex, pdflatex run sequence. Use whenever pre-written text and pre-generated figures must become a compiled PDF, and whenever a build misbehaves — citations printing as question marks, figures drifting to the end or above the title, shrunken axis labels, undefined references. Triggers: latex, tex, pdflatex, bibtex, natbib, includegraphics, figure float, htbp, compile or build the paper, paper.tex, paper.pdf. NOT for: writing the paper's text or deciding its structure (use aii-paper-writing), creating the figure images (aii-data-fig-gen, aii-concept-fig-gen), or fetching bibliography entries (use aii-semscholar-bib); NOT for reshaping a PDF that already exists — merging, splitting, form filling, table extraction (use anthropic-pdf)."
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, url, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=\linewidth,height=0.85\textheight,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````

### [3] SKILL-INPUT — aii-semscholar-bib · 2026-09-05 22:22:42 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: "Fetches real BibTeX entries in one batch from Semantic Scholar by DOI, ArXiv ID or title via aii_semscholar_bib__fetch, normalises citation keys to AuthorYYYY, injects DOIs, and writes the result into references.bib, with a mandatory web-search fallback for anything not found. ALWAYS use whenever a bibliography, reference list or .bib file is being built or extended, and whenever a citation needs a verified entry instead of an invented one — never hand-write BibTeX first. Triggers: bibliography, references.bib, bibtex, citation key, DOI, arXiv id, Semantic Scholar, reference list, cite these papers, natbib entries. NOT for: writing the text around the citations (use aii-paper-writing), running bibtex and compiling (use aii-paper-to-latex), judging whether cited work supports the claims (use amg-paper-verification), or open-ended literature search and PDF mining (use aii-web-tools)."
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
