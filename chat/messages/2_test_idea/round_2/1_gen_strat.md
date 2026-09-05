# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_strat`
> Run: `run_2ohq8qwlCPMZ` — Weakening the Transformer Reveals a Crossover, but the Label-Free Predictor Still Cannot Find It
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-09-05 19:21:16 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1
```

### [2] SYSTEM-USER prompt · 2026-09-05 19:21:22 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_PAPER_TEXT → REVIEW_PAPER → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, paper_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

<available_resources>
<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **SPEND BUDGET**: at most $10 USD of OpenRouter API calls for this artifact. Nothing outside your own code enforces this — the key you are given has no per-artifact cap — so it holds only if you track cumulative cost after every call and stop when you approach it. Budget the work up front: estimate the per-call cost and the number of calls BEFORE starting a sweep, not after it overruns. Exceeding it spends real money that the run cannot recover.
</software_constraints>
</available_resources>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is about the approach, not the hypothesis. Try different methods, parameters, data, or formulations within the hypothesis bounds.
5. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
6. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
7. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

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
Your workspace: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/file.py`, `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<hypothesis>
Your strategy should advance this hypothesis.

kind: hypothesis
title: No Small-n Crossover, So Predictor Untested
hypothesis: >-
  For short-text sentiment classification, we no longer claim that a Good-Turing/Chao1 unseen-vocabulary-mass statistic predicts
  a crossover between TF-IDF+logistic-regression and fine-tuned DistilBERT within practically relevant training sizes (n<=2000),
  because the premise the predictor depends on does not hold in the regime tested: on Rotten Tomatoes and SST-2, DistilBERT's
  mean test accuracy exceeds TF-IDF+LR's at every tested n from 50 to 1000 (gaps of 15-25 accuracy points, non-shrinking),
  so no finite empirical crossover exists for either domain and the label-light predictor has never been evaluated against
  a real target. The revised, narrower hypothesis is two-part: (1) [established negative result, evolution of the original
  scope claim] for curated short-text sentiment domains with a modern distilled transformer, the classical folk crossover
  point lies below n=50 or does not exist in [50,2000] at all - a scope-boundary finding about when bag-of-words vs. transformer
  model selection is even a live question; and (2) [the original mechanism claim, now demoted to unvalidated and requiring
  a genuine test] the Good-Turing/Chao1 coverage-based predictor's calibrate-on-one-domain/predict-on-another mechanism can
  only be judged once a domain/model pair with a real, finite crossover in the tested range is found - which requires either
  a domain further from DistilBERT's comparative advantage (e.g., a genuinely independent, noisier register such as tweet_eval,
  or a harder/longer-context task) or a deliberately weakened model (a smaller/less-pretrained transformer, or a context-truncated
  variant) to induce a crossover to predict against. Until such a target is found and the predictor is shown to give a within-2x
  cross-domain prediction there, the coverage machinery is future work, not a validated contribution. We also retract the
  implicit claim that Rotten Tomatoes and SST-2 constitute two independent confirmations: given their shared Pang & Lee/Socher
  lineage, all 'both domains' language should be read as one domain plus its near-duplicate, and the 4-point Spearman correlation
  check (rho=0.105/-0.200, p=0.89/0.80) is acknowledged as underpowered rather than as evidence of a null relationship.
motivation: >-
  Practitioners currently decide 'TF-IDF or transformer?' by training both models across several dataset sizes - itself a
  small experiment. If the decision can instead be read off a cheap, label-free statistic computed on unlabeled text in seconds,
  it turns an empirical sweep into a closed-form annotation-budgeting tool: before spending money on labels, a team could
  estimate whether their corpus's vocabulary structure means a fine-tuned transformer is worth the extra 2,000th label, or
  whether the simple baseline will remain competitive well beyond it.
assumptions:
- >-
  Class-discriminative n-grams (those with high mutual information with the label, estimated from a small labeled pilot set)
  are a proxy for the actual bag-of-words features TF-IDF+LR exploits.
- >-
  The corpus is homogeneous enough that vocabulary-coverage statistics from unlabeled subsampling transfer to the labeled
  subsample actually drawn for training.
- >-
  DistilBERT's held-out accuracy gain over the baseline is monotonically related to the unseen-n-gram mass, rather than dominated
  by other factors (e.g., syntactic compositionality) at the sample sizes tested (<=2,000).
- >-
  A short-text, single-domain sentiment task (Rotten Tomatoes / SST-2-scale) is representative enough that the coverage-curve
  mechanism, not dataset-specific idiosyncrasy, drives the crossover.
investigation_approach: >-
  Using Rotten Tomatoes (and SST-2 as a second dataset), (1) build the discriminative n-gram set via mutual information on
  a small labeled pilot (e.g., 200 examples); (2) compute the unseen-mass curve 1-C(n) for that discriminative vocabulary
  via repeated random subsampling of the unlabeled pool at increasing n, using a Good-Turing/Chao1 estimator; (3) separately,
  run the real experiment - train TF-IDF+LR and fine-tune DistilBERT (CPU-only) at n in {50, 100, 200, 500, 1000, 1500, 2000}
  with multiple seeds, recording accuracy vs. n for both; (4) fit the predicted crossover n-hat* as the n where the unseen-mass
  curve crosses a fitted threshold calibrated on one dataset, then test whether n-hat* (computed with NO knowledge of the
  actual accuracy curves) falls near the true empirical crossover n* on the held-out dataset (SST-2), and repeat the reverse
  direction (calibrate on SST-2, predict on Rotten Tomatoes).
success_criteria: >-
  The hypothesis is supported if the vocabulary-coverage-predicted crossover n-hat* falls within a small multiplicative band
  (e.g., within 2x) of the true empirical crossover n* on the held-out dataset, and if the unseen-mass curve's shape correlates
  significantly (e.g., Spearman rho) with the DistilBERT-minus-baseline accuracy gap across sample sizes on both datasets.
  It is disconfirmed if the coverage curve is flat or uncorrelated with the accuracy gap, or if the predicted crossover is
  off by an order of magnitude or more, indicating the mechanism does not transfer across datasets and the crossover is dominated
  by other factors.
related_works:
- >-
  'From TF-IDF to Transformers: A Comparative and Ensemble Approach to Sentiment Classification' (arXiv 2605.22003) and similar
  comparative studies benchmark TF-IDF+LR against DistilBERT/RoBERTa at fixed dataset sizes but do not model or predict where
  a crossover occurs, nor use any label-free predictor - they report accuracy tables, not a mechanism.
- >-
  'Revisiting Sample Size Determination in Natural Language Understanding' / power-law learning-curve extrapolation work fits
  a power law to labeled accuracy points from the same model at several sizes to extrapolate its own future performance; it
  requires training the model itself at multiple sizes and doesn't predict a crossover between two different model families
  from unlabeled statistics alone.
- >-
  'UCS: Estimating Unseen Coverage for Improved In-Context Learning' (arXiv 2604.12015) applies Good-Turing-style unseen-coverage
  estimation to in-context example selection for LLM prompting - a different problem (which examples to put in a prompt) rather
  than predicting a supervised-training data-size crossover between architectures.
inspiration: >-
  Imported from ecology/biostatistics: the Chao1 and Good-Turing 'unseen species' estimators, developed to predict how many
  species remain undiscovered in an ecological survey from the number of singleton/doubleton observations, are repurposed
  here to predict how much class-discriminative vocabulary remains unseen in a text corpus at a given sample size - treating
  n-grams as 'species' and documents as 'individuals' sampled from a community. This turns a biodiversity-survey-design tool
  into an NLP annotation-budgeting tool.
terms:
- term: Good-Turing estimator
  definition: >-
    A statistical method for estimating the probability of encountering previously unseen items in a sample, based on the
    frequency of items observed exactly once or twice.
- term: Chao1 estimator
  definition: >-
    A nonparametric estimator (from ecology) of the total number of distinct types in a population, computed from the counts
    of rare (singleton/doubleton) types observed in a sample.
- term: Discriminative n-gram
  definition: >-
    A word or short word-sequence whose presence is strongly informative about the class label, identified via mutual information
    with the label on a small labeled pilot set.
- term: Crossover point (n*)
  definition: >-
    The training-set size at which a fine-tuned transformer's accuracy first exceeds that of the TF-IDF+logistic-regression
    baseline.
- term: Unseen mass
  definition: >-
    The estimated total probability (or fraction) of discriminative vocabulary items not yet observed at a given sample size,
    i.e., 1 minus sample coverage.
summary: >-
  The training-set size at which DistilBERT overtakes a TF-IDF+logistic-regression baseline on short-text sentiment can be
  predicted from a label-free statistic - the estimated fraction of class-discriminative n-grams still unseen at that size,
  computed via ecology-derived (Good-Turing/Chao1) unseen-species estimators on unlabeled text alone.
_relation_rationale: >-
  Same predictor mechanism kept; scope narrowed to where a crossover exists, predictor demoted to unvalidated.
_confidence_delta: decreased
_key_changes:
- >-
  Demoted the central claim from 'predictor works and transfers' to 'predictor has never been tested against a real crossover'
  per reviewer MAJOR #1
- >-
  Narrowed scope: within curated short-text sentiment at n<=2000 with DistilBERT, no finite crossover exists (established
  negative result), so the search for a validating domain/model pair becomes the next required step (weaker model, truncated
  context, or a noisier/independent register like tweet_eval)
- >-
  Explicitly retracted the 'two independent domains' framing given Rotten Tomatoes/SST-2 shared Pang & Lee/Socher lineage,
  per reviewer MAJOR #2
- >-
  Downgraded the n=4 Spearman correlation from 'no reliable relationship' to 'underpowered, cannot rule out a real relationship',
  per reviewer MAJOR #3
- >-
  Kept the core Good-Turing/Chao1 vocabulary-coverage mechanism and calibrate/predict design unchanged, since it was never
  actually falsified - only left without a target to test it on
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<iteration_status>
Current iteration: 2 of 2
Remaining (including this one): 1
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: Test the Label-Free Vocabulary-Coverage Crossover Predictor
objective: >-
  Determine whether a cheap, mostly-label-free unseen-vocabulary-mass statistic (Good-Turing/Chao1 coverage curves over class-discriminative
  n-grams) can predict, in advance, the training-set size at which fine-tuned DistilBERT overtakes a TF-IDF+logistic-regression
  baseline on short-text sentiment -- and whether that predictive mechanism transfers across genuinely distinct short-text
  corpora rather than just two samples of the same movie-review distribution.
rationale: >-
  The reviewed hypothesis is novel and falsifiable but was flagged for three fixable weaknesses: (1) the 'label-free' framing
  hides a real ~200-example labeled-pilot cost used to define discriminative n-grams, (2) the cross-dataset validation as
  designed has an effective n of 2 (Rotten Tomatoes <-> SST-2), which are not independent since SST-2 is itself derived from
  Rotten Tomatoes snippets, and (3) the Chao1/Good-Turing estimators are known to be unstable at small sample sizes and no
  uncertainty is reported. This iteration builds a genuinely multi-domain short-text sentiment dataset (movie reviews + at
  least one non-review domain, e.g. product or social-media text), runs the full accuracy-vs-size sweep for both models on
  every domain, computes the coverage-based crossover prediction with an explicit pilot-label cost accounting and bootstrap
  uncertainty on the Chao1 estimate, and evaluates the calibrate-on-one/predict-on-another test across >=3 independent domain
  pairs instead of 2. This directly answers reviewer soundness/evidence critiques while keeping the core mechanism and falsification
  criteria intact.
artifact_directions:
- id: dataset_iter1_dir1
  type: dataset
  objective: >-
    Assemble a multi-domain short-text binary-sentiment corpus spanning at least 3 genuinely distinct sources so the crossover-prediction
    test has more than 2 independent calibrate/predict pairs.
  approach: >-
    Pull Rotten Tomatoes, SST-2, and one non-review-domain short-text sentiment set (e.g. a Twitter/social-media sentiment
    corpus or Amazon/Yelp product reviews) from HuggingFace Hub, normalize to a common {text,label} schema, dedupe near-identical
    snippets across RT/SST-2 (they share lineage), and reserve a fixed unlabeled pool plus stratified train/val/test splits
    per domain for sample sizes n in {50,100,200,500,1000,1500,2000}. Explicitly flag the RT/SST-2 shared-lineage caveat in
    metadata so downstream analysis can treat that pair as weaker evidence than the third, independent domain.
  depends_on: []
- id: research_iter1_dir2
  type: research
  objective: >-
    Work out and document the exact label-free (and label-light) crossover-prediction procedure, its labeling-cost accounting,
    and its known failure modes before running any experiment.
  approach: >-
    Specify: (a) the MI-based discriminative-n-gram extraction from a small labeled pilot, explicitly reporting pilot size
    as a labeling cost rather than calling the method label-free; (b) an MI-free alternative (raw n-gram frequency deltas
    between classes on the same pilot) as a robustness check on whether the mechanism depends on MI specifically; (c) the
    Good-Turing/Chao1 coverage-curve computation via repeated subsampling with bootstrap confidence intervals, and the known
    bias regime (few singleton/doubleton n-grams) under which the estimator should be flagged unstable; (d) the exact crossover-fitting
    and cross-domain calibrate/predict protocol across >=3 domain pairs.
  depends_on: []
- id: experiment_iter1_dir3
  type: experiment
  objective: >-
    Empirically measure, per domain, the TF-IDF+LR vs DistilBERT accuracy-vs-training-size curves and the true crossover point
    n*, and separately compute the label-free coverage-based prediction n-hat* with its uncertainty, then compare the two
    label-free predicted-vs-observed crossovers across domain pairs.
  approach: >-
    For each of the 3 domains: train TF-IDF+LR and fine-tune DistilBERT (CPU-only) at n in {50,100,200,500,1000,1500,2000}
    with >=5 seeds each, recording mean+/-CI accuracy and the empirical crossover n*. Separately, using only the pilot-labeled
    subset and the unlabeled pool, compute the Good-Turing/Chao1 unseen-mass curve for discriminative n-grams (with bootstrap
    CIs), fit the crossover threshold on each domain, and predict n-hat* on every OTHER domain (>=3x2=6 calibrate/predict
    directions). Run the pilot-size sensitivity ablation (100/200/400-example pilots) and the MI-vs-frequency discriminative-vocabulary
    ablation to test whether the prediction is robust to how the pilot is used.
  depends_on: []
expected_outcome: >-
  A per-domain accuracy-vs-n curve for both model families with measured empirical crossovers n*, a label-free (pilot-cost-accounted)
  coverage-based crossover predictor n-hat* with bootstrap uncertainty, and a distribution of |n-hat*/n*| ratios across >=6
  calibrate/predict domain-pair directions (instead of 2 point estimates) -- enough evidence to say whether the vocabulary-coverage
  mechanism genuinely transfers across distinct domains, is confined to same-lineage movie-review text, or fails outright,
  while also reporting how sensitive the prediction is to pilot size and to the MI-based discriminative-vocabulary proxy.
summary: >-
  Re-runs the vocabulary-coverage crossover-prediction idea with a 3rd, non-review domain added, an explicit pilot-labeling-cost
  accounting instead of a 'label-free' framing, bootstrap-uncertainty Chao1/Good-Turing estimates, and >=6 independent calibrate/predict
  domain-pair tests -- directly addressing the reviewer's soundness and evidence-strength critiques of the original 2-dataset,
  same-lineage design.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
--- Item 1 ---
id: art_jvhKSROMmhCr
type: dataset
title: Three-Domain Short-Text Sentiment Corpus
summary: >-
  Provides a normalized, deduplicated, class-balanced binary-sentiment corpus spanning three HuggingFace-sourced domains:
  cornell-movie-review-data/rotten_tomatoes (Cornell Pang & Lee movie-review snippets, 10,660 rows post-dedup), stanfordnlp/sst2
  (GLUE SST-2 sentence-level movie reviews, train+validation only since the test split's labels are masked -1; 52,732 rows
  after within-domain dedup and 6,753 cross-set duplicates/near-duplicates vs rotten_tomatoes removed via normalized-text
  + first-8-token shingle hashing), and cardiffnlp/tweet_eval (config=sentiment, 3-class SemEval-2017 Task 4 tweets binarized
  by dropping the neutral class and remapping {negative:0, positive:1}, 32,378 rows post-filter/dedup). rotten_tomatoes and
  sst2 share upstream Pang & Lee/Socher lineage (metadata_lineage_group='pang_lee_lineage') and are explicitly flagged as
  NOT independent evidence of anything; tweet_eval (metadata_lineage_group='independent') is the only genuinely independent
  domain, breaking the RT/SST-2 shared-lineage confound. Each domain provides a fixed class-balanced held-out val (500 rows)
  and test (1000 rows) set, a large capped unlabeled_pool (7,160-10,000 rows, raw text for a Good-Turing/Chao1 subsampling
  curve), and nested labeled train pools at n in {50,100,200,500,1000,1500,2000} built with fixed seed 42 so every smaller-n
  pool is a strict subset of every larger-n pool (enabling matched-seed learning-curve comparisons). full_data_out.json conforms
  to the exp_sel_data_out schema (validated): one group per dataset (rotten_tomatoes/sst2/tweet_eval), each row a separate
  {input: review/tweet text, output: '0'|'1' label, metadata_split: val|test|train|unlabeled_pool, metadata_lineage_group,
  metadata_task_type='classification', metadata_n_classes=2, metadata_train_min_n (train rows only, the smallest n in {50...2000}
  the row belongs to, since nested pools are deduplicated into one unique set per domain rather than repeated 7x)} object.
  A TF-IDF(1-2gram)+LogisticRegression sanity baseline at n_train=1000 scores 0.652/0.701/0.745 test accuracy on rotten_tomatoes/sst2/tweet_eval
  respectively, confirming clear above-chance signal in all three domains. output/manifest.json and output/README.md document
  exact source versions, row counts before/after filtering and dedup, and the lineage caveat for downstream citation. Total
  workspace size ~48MB, well under the 300MB/100MB caps.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Item 2 ---
id: art_Ak7R4sTP2lE4
type: research
title: Label-Free Crossover Predictor Protocol
summary: >-
  This research artifact fully specifies, before any experiment is run, the exact algorithm for the label-free crossover-point
  predictor described in the artifact plan: (A) discriminative n-gram extraction via classical discrete/expected mutual information
  (a 2x2 contingency-table formula, distinct from scikit-learn's k-NN-based mutual_info_classif, which is the wrong tool for
  already-binary presence/absence features) computed on a labeled pilot (100/200/400 examples, cost explicitly reported, never
  called 'label-free'), with a permutation-null (max-statistic, family-wise) top-k selection rule as the recommended alternative
  to a fixed top-k, plus an MI-free robustness variant based on |class-conditional frequency deltas| and a Jaccard/Spearman
  comparison protocol between the two; (B) a Good-Turing missing-mass coverage curve C(n)=1-f1(n)/N(n) computed on document-occurrence
  counts of the fixed discriminative vocabulary across B=100 bootstrap subsamples per grid point, with the bias-corrected
  Chao1 richness estimator (S_obs + f1(f1-1)/(2*(f2+1))) as a secondary cross-check, an explicit f2<10 instability flag with
  a mandatory per-dataset unstable-fraction table, and exclusion of unstable grid points from curve-fitting; (C) an exact
  operational definition of empirical crossover n* (first grid n where the DistilBERT-vs-TF-IDF accuracy gap exceeds one pooled
  standard error), a single-free-parameter calibrate/predict rule (tau fit from the calibration dataset's own 1-C(n*) value),
  a concrete >=3-domain matrix (Rotten Tomatoes and SST-2 as a flagged WEAK near-transfer pair, plus cardiffnlp/tweet_eval
  sentiment as the mandatory genuinely-distinct third domain, with fancyzhx/yelp_polarity as a documented fallback), all 6
  directed calibrate/predict pairs, and the within-2x success band plus a per-dataset Spearman-rho check between coverage-curve
  shape and accuracy gap; and (D) five explicitly documented failure modes (small-f2 instability, pilot-noise-driven vocabulary
  variance, near-transfer domain contamination, tau's single-degree-of-freedom fragility with a stated multi-dataset-mean
  robustness check, and a monotonicity precondition check) plus disconfirmation triggers including a new one this protocol
  adds: >50% of grid points falling in the unstable regime renders the whole estimate NOT INTERPRETABLE rather than scoreable.
  Every numeric formula/threshold is either cited to a primary source (Gale & Sampson 1995 for Good-Turing; Chao's bias-corrected
  Chao1 form per scikit-bio/ecology convention; Yang & Pedersen 1997 for MI-based text feature selection; scikit-learn docs
  clarifying mutual_info_classif's k-NN estimator is inapplicable to binary features) or explicitly labeled 'convention chosen
  here, no canonical source' (e.g., the df>=2 pilot cutoff, the Laplace-smoothing constant for MI contingency cells, the f2<10
  instability threshold, and the document-occurrence-count unit choice for Good-Turing instead of the more common raw-token-count
  unit). Dataset sizes and licenses were verified directly from HuggingFace dataset cards rather than assumed. The downstream
  experiment executor can implement this protocol directly with no remaining design decisions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json

--- Item 3 ---
id: art__VSV4YQ0_oJD
type: experiment
title: TF-IDF vs DistilBERT Crossover on Small Text Data
summary: >-
  Implements method.py: a controlled comparison of TF-IDF+logistic-regression versus CPU-fine-tuned DistilBERT on short-text
  sentiment classification (Rotten Tomatoes, SST-2), sweeping training-set size n in {50,200,500,1000} with 2 seeds per (domain,n)
  (15/16 combos completed; 1 combo skipped by the wall-clock guard), plus a label-free Good-Turing/Chao1 unseen-vocabulary-mass
  predictor of the accuracy crossover point, calibrated on one domain and tested for cross-domain transfer on the other, with
  pilot-size (100/200/400) and discriminative-vocab-selection (mutual-information vs raw-frequency) ablations, and a Spearman
  correlation between the unseen-mass curve shape and the DistilBERT-minus-TFIDF accuracy gap. A 35-minute wall-clock guard
  on the DistilBERT sweep triggered the fallback plan's degradation ladder: seeds were kept at their reduced value (2), IMDB
  was dropped, leaving 2 domains (rotten_tomatoes, sst2) and 2 cross-domain calibrate/predict directions instead of the planned
  3 domains/6 directions; the script checkpoints every completed (domain,n,seed) run to disk so an interrupted sweep resumes
  rather than recomputing, and every degradation is logged verbatim in method_out.json's summary.degradations_applied field
  rather than hidden. DistilBERT beat TF-IDF+LR at every tested n on BOTH domains (no finite empirical crossover in [50,1000]
  for either rotten_tomatoes or sst2), so the label-free Good-Turing predictor had no true crossover to calibrate against
  and the cross-domain-transfer test could not be scored numerically in either direction (both marked skipped, not silently
  dropped). The gap-vs-unseen-mass Spearman correlation is weak/non-significant on both domains where it could be computed
  (rotten_tomatoes rho=0.105 p=0.89; sst2 rho=-0.20 p=0.80; n=4 points each). Overall verdict recorded in method_out.json:
  DISCONFIRMED. The artifact still delivers a fully working, checkpointed (crash-safe) side-by-side implementation of both
  the baseline (TF-IDF+LR) and proposed method (fine-tuned DistilBERT), with per-example predict_tfidf_lr_acc/predict_distilbert_acc
  (and predict_n_hat_star for the label-free predictor) fields, plus the full label-free coverage-curve machinery (Good-Turing
  unseen-mass, Chao1 richness with the bias-corrected f2==0 fallback, MI-vs-frequency discriminative n-gram extraction, pilot-size
  ablation), so a downstream paper can report both the accuracy-vs-n curves and the honest negative result on crossover predictability,
  with the degradation path fully logged. Raw per-(domain,n,seed) results, per-n aggregated accuracy curves with 95% CIs,
  coverage curves for every (domain,pilot_n,method) combination, and the cross-domain prediction table are all in method_out.json
  under the exp_gen_sol_out schema's datasets array (raw_results, accuracy_curve, true_crossovers, coverage_curves, cross_domain_predictions,
  pilot_and_vocab_ablation, gap_vs_unseen_correlations, summary).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# Introduction

A practitioner who needs a text classifier and has only a handful of labeled examples faces a real choice: train a classical bag-of-words model such as TF-IDF features with logistic regression, which needs almost no data and no GPU, or fine-tune a pretrained transformer such as DistilBERT [sanh2019distilbert], which is more expensive to train but is widely believed to eventually pull ahead as labeled data accumulates. The concrete decision is when to switch: at what training-set size n does the fine-tuned transformer's accuracy first exceed the classical baseline's, and can a practitioner know this in advance, before they have labeled n examples of either model's training data?

This question matters because labeling is the expensive step, not training. A team building a new text-classification pipeline typically has a large pool of unlabeled text and a labeling budget they would like to spend efficiently. If the crossover training size n* could be estimated cheaply from the unlabeled pool -- without first labeling n* examples for both models and comparing them, which defeats the purpose -- a team could commit to the transformer only once it is worth the training cost, or stop early with the classical baseline when the crossover would fall outside their labeling budget entirely.

Estimating n* in advance is hard because the crossover, if it exists, is a property of how quickly a domain's discriminative vocabulary saturates as more examples are seen, not a property visible in any single labeled example. A domain with a small, rapidly-saturating vocabulary of sentiment-bearing terms should let a bag-of-words model catch up to a transformer quickly, while a domain with a long tail of rare, informative terms should favor the transformer's ability to generalize from subword and semantic structure rather than surface term overlap. This intuition motivates using a vocabulary-coverage statistic -- specifically, a Good-Turing / Chao1 unseen-mass estimate [galesampson1995goodturing, good1953population, chao1984nonparametric] over a fixed discriminative n-gram vocabulary -- as a label-light proxy for how fast the crossover approaches.

No prior work we are aware of has tested whether such a coverage-based statistic actually predicts the empirical TF-IDF-versus-transformer crossover, largely because doing so requires first establishing that a finite, predictable crossover exists at all in realistic short-text settings, which is itself an empirical question rather than an assumption to import from folklore. We built the full label-light predictor -- pilot-based discriminative-vocabulary extraction, bootstrap-uncertain Good-Turing coverage curves, and a single-parameter calibrate-on-one-domain/predict-on-another rule -- and ran it alongside the accuracy sweep it is meant to predict, on two short-text sentiment domains (Rotten Tomatoes movie-review snippets [panglee2005rotten] and SST-2 [socher2013recursive]) at training sizes n in {50, 200, 500, 1000}.

We find that the premise fails before the predictor can be evaluated: DistilBERT's mean test accuracy exceeds TF-IDF plus logistic regression's at every tested n in both domains, by 15 to 25 accuracy points even at the smallest size, n=50. There is no finite empirical crossover in either domain within the tested range, so the cross-domain calibrate/predict test -- the paper's originally intended headline result -- has nothing to calibrate against and is reported as skipped rather than as a pass or fail. A secondary, weaker check correlates the coverage curve's shape with the (always-positive, never-crossing) accuracy gap itself and finds no reliable relationship in either domain. We report the overall experiment as DISCONFIRMED, not because the coverage-based mechanism was tested and found wanting, but because its target quantity does not exist in the regime tested, and we discuss what that implies for where a crossover-based model-selection heuristic could ever apply.

## Summary of Contributions

- We report a controlled accuracy-vs-training-size sweep of TF-IDF plus logistic regression against a fine-tuned DistilBERT on two short-text sentiment domains at four training sizes, with matched seeds, test sets, and preprocessing (Section 3).
- We show that DistilBERT accuracy exceeds the classical baseline at every tested training size in both domains, meaning no finite crossover point exists to predict in this regime -- a negative result about the premise, not the predictor (Section 4).
- We built the full label-light Good-Turing / Chao1 vocabulary-coverage machinery a crossover predictor would need, including bootstrap uncertainty and an explicit pilot-labeling-cost accounting, and show it cannot be evaluated on its intended task once the crossover it targets is absent (Section 3.2).
- We report a secondary correlation check between the coverage curve's shape and the (non-crossing) accuracy gap and find no reliable signal, and we discuss the scope-boundary implications for crossover-based small-data model selection more broadly (Section 5).

# Related Work

The accuracy-versus-training-size relationship of neural models is well studied in the neural scaling-law literature, which typically fits smooth power-law curves to a single model's accuracy or loss as training data grows [sorscher2022beyond], rather than asking when one model family overtakes another. That framing implicitly assumes both models are on the same power-law family and differ only in a scale constant; it does not address a discontinuous switch between architecturally distinct model classes, such as bag-of-words linear models and fine-tuned transformer encoders, which is the comparison this paper is concerned with.

Work introducing pretrained transformer encoders such as BERT [devlin2019bert] and its distilled variant DistilBERT [sanh2019distilbert] reports strong few-shot and low-resource fine-tuning results relative to classical baselines, which is consistent with our finding that DistilBERT can lead from very small training sizes on short-text sentiment; these papers do not, however, characterize a crossover point or attempt to predict one from unlabeled data. The folk intuition that classical bag-of-words methods are competitive or superior at very small n is common in practitioner discussion but, to our knowledge, has not been directly tested at the training sizes we sweep (50 to 1000 examples) on the specific short-text sentiment domains used here.

The unseen-vocabulary-mass statistics underlying our coverage-based predictor -- the Good-Turing missing-mass estimator [galesampson1995goodturing, good1953population] and the Chao1 richness estimator [chao1984nonparametric] -- originate in ecology and corpus linguistics, where they estimate the probability mass or species count belonging to classes not yet observed in a sample; we adapt them here to a fixed, pilot-derived discriminative n-gram vocabulary, following mutual-information-based feature selection conventions from text categorization [yangpedersen1997comparative]. These estimators are known to be unstable when the count of doubleton (frequency-2) classes is small, a caveat we account for but which is not the source of the null result reported here -- our coverage curves themselves behave as expected (monotonically decreasing unseen mass with n); the null result is that this well-behaved statistic does not correlate with an accuracy gap that never changes sign.

# Methods

## Datasets

We use two short-text binary-sentiment domains sourced from the HuggingFace Hub: Rotten Tomatoes movie-review snippets [panglee2005rotten] and SST-2 [socher2013recursive]. A third, genuinely independent domain (`cardiffnlp/tweet_eval` sentiment, social-media text) was assembled and is documented in the released dataset artifact, but was not run in this iteration's experiment due to a compute-time budget; results below therefore cover only the Rotten Tomatoes/SST-2 pair, which the dataset's own documentation flags as a *weak* transfer pair because SST-2's sentences derive from the same underlying Cornell movie-review corpus as Rotten Tomatoes (a shared-lineage caveat we inherit and repeat here rather than treat as resolved). For each domain we use class-balanced, seeded (seed=42) nested training pools at sizes n in {50, 200, 500, 1000} -- a reduced grid relative to the originally planned {50,100,200,500,1000,1500,2000}, again due to the compute-time budget -- and a fixed 800-example held-out test set per domain, disjoint from all training pools.

## Accuracy-vs-size sweep

At each training size n we fit two classifiers per domain, per seed: (1) TF-IDF features (unigrams and bigrams) with L2-regularized logistic regression, and (2) DistilBERT (`distilbert-base-uncased`) fine-tuned on CPU for a fixed number of epochs, both evaluated on the same held-out 800-example test set. We use 2 random seeds per (domain, n) cell, below the 5 originally intended, due to the same compute-time budget; one cell (Rotten Tomatoes, n=1000) completed only 1 seed after a mid-sweep runtime-budget cutoff. We report the mean accuracy and a 95% confidence interval computed from the seed replicates (a single point estimate with zero-width interval where only one seed completed).

## Label-light coverage predictor

Independent of which model wins, we built the full coverage-based crossover predictor specified in the accompanying research protocol. A discriminative n-gram vocabulary is extracted from a small labeled pilot (100, 200, or 400 examples, cost reported explicitly rather than the method being called "label-free") using classical contingency-table mutual information with a permutation-null significance cutoff, plus a frequency-delta alternative for robustness. Holding that vocabulary fixed, we compute a Good-Turing missing-mass coverage curve C(n) = 1 - f1(n)/N(n) over document-occurrence counts, bootstrapped over B=100 subsamples of the unlabeled pool at each of the same four training sizes, with the Chao1 estimator as a secondary cross-check and an explicit instability flag for any grid point where the doubleton count f2 falls below 10. Empirical crossover n* is defined, per domain, as the first grid point where the DistilBERT-minus-TF-IDF accuracy gap exceeds the pooled standard error of the two means; the label-light predictor is n_hat* = min{n : 1 - C(n) < tau}, with the single free parameter tau fit from a calibration domain's own value and applied unseen to a different, predict-on domain.

[FIGURE:fig1]

# Experiments

## Accuracy sweep results

Figure 1 shows mean test accuracy for TF-IDF-plus-logistic-regression and DistilBERT at each of the four training sizes, for both domains. On Rotten Tomatoes, TF-IDF accuracy rises from 0.536 at n=50 to 0.673 at n=1000, while DistilBERT rises from 0.689 at n=50 to 0.833 at n=500 (0.825 at n=1000, single seed); the accuracy gap in DistilBERT's favor is 0.153, 0.201, 0.188, and 0.153 accuracy points at n=50, 200, 500, and 1000 respectively -- positive, and of comparable magnitude, at every tested size. On SST-2, TF-IDF rises from 0.546 to 0.650 across the same grid while DistilBERT rises from 0.711 to 0.853; the gap is 0.166, 0.254, 0.233, and 0.203 accuracy points, again positive throughout and, if anything, larger than on Rotten Tomatoes. In neither domain does the gap approach zero or change sign at any tested n, so the empirical crossover n* is undefined (formally, `None`, with direction recorded as "DistilBERT ahead at all tested n") for both domains.

## Coverage predictor: not evaluable on its intended task

Because no domain has a finite empirical crossover, the cross-domain calibrate/predict test could not be run in either direction: calibrating tau on Rotten Tomatoes and predicting SST-2's crossover is undefined because Rotten Tomatoes has no n* to calibrate tau from, and the same holds calibrating on SST-2 and predicting Rotten Tomatoes. Both directions are recorded as skipped, with the explicit reason "domain has no finite empirical crossover," rather than scored as either a successful or failed within-2x prediction. We regard this as the central finding of the experiment: the method's premise, not its coverage-based mechanism, is what fails in this regime, and no amount of tuning the coverage statistic could have produced a meaningful crossover prediction once the quantity it targets does not exist.

## Secondary check: coverage shape versus accuracy gap

As a weaker, exploratory check of whether the coverage curve's shape tracks the accuracy gap even without a sign change to predict, we compute the Spearman correlation between 1 minus the unseen-vocabulary-mass estimate and the accuracy gap across the four shared training sizes, per domain. On Rotten Tomatoes, rho = 0.105 (p = 0.89, n = 4 points); on SST-2, rho = -0.200 (p = 0.80, n = 4 points). Both correlations are statistically indistinguishable from zero at this sample size, and the two domains do not even agree in sign. Figure 2 plots the coverage curve alongside the accuracy gap for both domains: the coverage curve itself is well-behaved and monotonically decreasing as expected (for example, on Rotten Tomatoes with a 100-example pilot and mutual-information vocabulary selection, the unseen mass falls from 0.537 at n=50 to 0.250 at n=200, 0.111 at n=500, and 0.053 at n=1000), but the accuracy gap it is meant to track is roughly flat and does not shrink toward zero over the same range, so the two curves have no shared structure for a correlation to pick up.

[FIGURE:fig2]

# Discussion

The result reported here is a negative one, but it is informative about scope rather than merely null. The crossover-based framing this paper set out to test -- that classical bag-of-words models beat fine-tuned transformers below some threshold training size, and that the threshold can be predicted from unlabeled vocabulary coverage -- presupposes that the crossover exists somewhere in the range a practitioner would plausibly operate in. On two short-text sentiment domains, at training sizes from 50 to 1000 labeled examples, we find DistilBERT ahead from the very first grid point, which means the crossover this class of method targets, if it exists at all for these domains, lies below n=50 -- a training size so small that fitting a stable TF-IDF-plus-logistic-regression baseline is itself questionable, and one a practitioner is unlikely to stop at deliberately. This narrows, rather than eliminates, the space in which a coverage-based (or any other label-light) crossover predictor could be useful: it would need domains and model pairs where the crossover genuinely falls in a labeling-budget-relevant range, which short-text sentiment with a distilled transformer does not appear to provide.

A second limitation is that both domains tested share the same underlying Cornell movie-review corpus lineage, a caveat the dataset documentation itself flags; even had a crossover existed, treating Rotten Tomatoes and SST-2 as two independent evidence points for cross-domain transfer would have overstated the method's generality. The third, genuinely independent domain (tweet_eval sentiment, social-media register) assembled for this purpose was not run in this iteration because of the compute-time budget, and remains the natural next check -- a register shift of that kind could plausibly produce a smaller initial DistilBERT advantage, or even a crossover within the tested range, since social-media text's shorter, noisier sentiment vocabulary may be closer to bag-of-words classifiers' comparative strength than curated movie-review prose is.

Third, our accuracy sweep itself ran on a reduced grid (four training sizes instead of the originally planned seven, up to n=1000 rather than n=2000) and with two random seeds per cell instead of five, with one cell (Rotten Tomatoes, n=1000) completing only a single seed after a mid-run time cutoff. The accuracy gaps we report are large enough (15-25 points) relative to their seed-to-seed variability (0-7 points) that we do not believe additional seeds would close them, but a genuinely intermediate result -- a domain and model pair where the gap is small and its sign is uncertain -- would need the fuller seed budget to resolve, and we did not observe such a case here.

Taken together, these results suggest that with a strong, cheaply-fine-tunable pretrained encoder available, the classical wisdom that bag-of-words methods win at small n may already be outdated for short, curated sentiment text specifically: the crossover this line of small-data model-selection work assumes may have moved below any labeling budget worth reasoning about, leaving nothing for a label-light predictor -- coverage-based or otherwise -- to usefully predict. Whether this also holds for register-shifted, longer, or more technical text remains open, and is exactly the kind of domain where a crossover, if it exists further out, would make a coverage-based predictor worth revisiting.

# Conclusion

We set out to test whether a label-light Good-Turing / Chao1 vocabulary-coverage statistic could predict the training-set size at which fine-tuned DistilBERT overtakes TF-IDF plus logistic regression on short-text sentiment, and whether that prediction transfers across domains. We built the full predictor and the accuracy sweep it depends on, and found that the premise does not hold in the regime tested: DistilBERT leads by 15 to 25 accuracy points at every training size from 50 to 1000 examples, in both of the two domains run, so no finite crossover exists for the predictor to target, and the intended cross-domain transfer test is vacuous by construction. We report the experiment as DISCONFIRMED and view its value as a scope-boundary result: crossover-based small-data model-selection heuristics, coverage-based or otherwise, need a domain and model pair where the crossover genuinely sits inside a practically relevant training-size range, which curated short-text sentiment with a distilled transformer baseline does not provide. Future work should (1) run the already-assembled third, register-shifted domain (tweet_eval sentiment) to test whether a crossover appears outside curated movie-review text, (2) extend the accuracy sweep to the originally planned training sizes up to n=2000 and to five seeds per cell to rule out a crossover hiding at larger n or within noise, and (3) if a genuine crossover is found in some domain, revisit the coverage-based predictor on that domain specifically, since the machinery built here was never actually exercised against a real target.
</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (scope) The paper's headline predictor -- the very method the paper is about -- is never evaluated against a real target: the cross-domain calibrate/predict test is skipped in both directions because no domain has a finite crossover. The paper thus reports a fully built, but completely untested, algorithm. A reviewer at a top venue would ask: what evidence is there that the Good-Turing/Chao1 coverage predictor works at all, on any task, even a toy one? None is presented.
  Action: Add at least one validation of the predictor mechanism itself, even synthetically: e.g., construct or find a domain/model pair (possibly a much weaker/smaller transformer, or truncated context) where a crossover genuinely exists in the tested range, and show the predictor calibrated on one domain gives a within-2x prediction on the other. Without this, restrict the paper's claims strictly to the accuracy-sweep negative result and demote the predictor machinery to 'not yet validated future work' rather than a contribution.
- [MAJOR] (evidence) The two tested domains (Rotten Tomatoes, SST-2) share upstream Pang & Lee/Socher lineage, which the paper itself and the dataset artifact flag as a 'weak transfer pair' that should not be treated as two independent evidence points. Yet the paper's entire empirical base rests on exactly these two domains, and its conclusions ('DistilBERT leads in both domains run', 'no finite crossover in either domain') are still presented with the rhetorical weight of two independent confirmations.
  Action: Run the already-assembled, genuinely independent tweet_eval sentiment domain (present in the dataset artifact but not executed this iteration) before submission, or explicitly downgrade every claim of the form 'in both domains' to 'in one domain and its near-duplicate' throughout the text, including the abstract/intro/conclusion, not just the Discussion section.
- [MAJOR] (rigor) Seed count is far below what is needed to support the paper's negative conclusions with confidence: 2 seeds per (domain, n) cell (1 seed for Rotten Tomatoes n=1000), and only 4 grid points feeding the Spearman correlation reported as 'statistically indistinguishable from zero' (n=4, p=0.89 and p=0.80). A correlation test with n=4 has essentially no power to detect any but an enormous effect, so 'no reliable relationship' is not a supportable conclusion from this data -- it is simply an underpowered test.
  Action: Either (a) run the originally planned 5 seeds and 7 grid points (up to n=2000) before drawing the 'no reliable correlation' conclusion, explicitly computing statistical power for the correlation test at the achieved n, or (b) soften the claim throughout to 'this exploratory 4-point check found no detectable signal, but was underpowered to rule out a real relationship' and drop language implying a settled null result.
- [MINOR] (novelty) Related Work asserts that no prior work has directly tested the classical-vs-transformer crossover at small n on short-text sentiment, but this claim is supported only by 'to our knowledge' with no evidence of a systematic literature search for prior TF-IDF-vs-BERT small-data comparisons, which are common in applied NLP blog posts, Kaggle writeups, and some workshop papers (e.g., work on few-shot text classification baselines).
  Action: Do a targeted search (e.g., on 'TF-IDF logistic regression vs BERT few-shot text classification', 'small-data baseline comparison transformer') and either cite the closest matches with an explicit statement of how this paper differs (controlled sweep + label-light predictor, vs ad hoc anecdote), or narrow the novelty claim to 'we are not aware of a peer-reviewed study doing X' rather than an unqualified absence claim.
- [MINOR] (methodology) DistilBERT is fine-tuned on CPU 'for a fixed number of epochs' with no stated hyperparameter search or early-stopping criterion; if the number of epochs was tuned informally to make DistilBERT perform well, this could bias the sweep in DistilBERT's favor, deepening the very asymmetry that produced the paper's negative result. Likewise no hyperparameter search is mentioned for the TF-IDF+LR baseline's regularization strength.
  Action: Report the exact epoch count, learning rate, and any hyperparameter selection procedure for both models, and confirm (or add) a light hyperparameter sweep or validation-based early stopping for each baseline at each n, so a reviewer can rule out 'undertuned baseline' as an alternative explanation for the always-positive gap.
- [MINOR] (clarity) The paper never states what a practically 'meaningful' gap size would be, or connects the 15-25 point gap to any labeling-cost tradeoff a practitioner would actually weigh (e.g., DistilBERT's training/inference cost vs. the accuracy gain in dollar or wall-clock terms), even though the introduction motivates the whole paper around exactly this cost tradeoff.
  Action: Add a short quantitative comparison of wall-clock/compute cost for TF-IDF+LR vs. CPU-fine-tuned DistilBERT at each n, so the paper's own motivating cost-benefit question ('when is switching worth it') is answered with data rather than left as framing.
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 3 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool

**BROADER IS NOT THE SAME AS DEEPER.** Adding models, datasets, or settings to
an experiment that already ran makes the table bigger; it does not make the
contribution stronger, and it is the default a strategy generator drifts into
when it has nothing sharper to propose. Spend an artifact on scale only when
the SPREAD itself is the finding (a scaling trend, a regime boundary, a
generalisation claim the paper actually makes). Otherwise spend it on
something that could change the conclusion: the mechanism behind an observed
effect, the condition under which it disappears, the confound that would
explain it away, or the baseline whose absence a reviewer would name first.


</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-05 19:21:22 UTC

```
Small-data text classification: does a TF-IDF + logistic-regression baseline match a small fine-tuned transformer (DistilBERT) on short-text sentiment when fewer than 2,000 labelled examples are available? Use a small public dataset such as the Rotten Tomatoes or SST-2 subset, CPU-only experiments, and report accuracy vs training-set size.
```

### [4] TOOL CALL — Write · 2026-09-05 19:22:04 UTC

```
File: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json

{
  "strategies": [
    {
      "title": "Find a Real Crossover to Test the Predictor",
      "objective": "Give the Good-Turing/Chao1 crossover predictor an actual target to be evaluated against -- by weakening the model side (a much smaller/less-pretrained transformer and a context-truncated DistilBERT) and adding the genuinely independent tweet_eval domain -- so the paper can report a real within-2x (or fails-to-predict) verdict instead of an untested algorithm, while fixing the statistical-power and cost-accounting gaps the reviewer flagged.",
      "rationale": "The reviewer's top-priority MAJOR issue is that the paper's headline method was never evaluated against a real crossover: both calibrate/predict directions were skipped because DistilBERT always won. Rather than re-running the same losing comparison at more sizes, this strategy deliberately engineers a domain/model pair where a crossover can plausibly exist -- a weaker model (e.g. a from-scratch-embedding tiny transformer or logistic-regression-comparable capacity like a 2-layer LSTM/tinyBERT distillation) and/or a severely context-truncated DistilBERT (first 8-16 tokens only, discarding the long-range signal that gives it its edge on short movie-review text) -- alongside the already-assembled but unused tweet_eval domain, whose noisier, shorter register is the paper's own stated best candidate for a smaller initial gap. This directly answers MAJOR #1 (validate the predictor on a real target) and MAJOR #2 (stop treating RT/SST-2 as two independent domains by finally running the independent third domain). A dedicated evaluation artifact then fixes MAJOR #3 (statistical power of the n=4 Spearman check) and the two MINOR issues (hyperparameter/tuning transparency, cost-benefit quantification) without re-running the expensive sweep twice. A short targeted-research artifact closes MINOR #4 (novelty claim needs a real search, not 'to our knowledge').",
      "artifact_directions": [
        {
          "type": "experiment",
          "objective": "Establish at least one domain/model pair with a genuine, finite empirical crossover in the tested range, and use it as the first real test of the label-light coverage-based crossover predictor's calibrate-on-one/predict-on-another mechanism.",
          "approach": "Reuse the existing dataset (rotten_tomatoes, sst2, tweet_eval) and the existing coverage-predictor code/protocol from the prior experiment and research artifacts. Add two model-weakening arms designed to induce a crossover: (a) a context-truncated DistilBERT that only sees the first 8 and 16 tokens of each example (removing the long-range signal that gives it its edge on short text), and (b) a much smaller/less-pretrained transformer (e.g. a 2-layer randomly-initialized or lightly-pretrained tiny-BERT-scale encoder, trained under the same CPU budget) as a genuinely weaker alternative to full DistilBERT. Run the full accuracy-vs-n sweep (TF-IDF+LR vs each weakened-model variant) on tweet_eval (the genuinely independent domain, not yet executed) plus at least one of rotten_tomatoes/sst2, at n in {50,100,200,500,1000,1500,2000} with >=5 seeds per cell, budgeting compute explicitly (drop the largest n or extra seeds first if a wall-clock guard triggers, exactly as before, and log every degradation). For whichever domain/model pair yields a finite empirical n* in this grid, run the Good-Turing/Chao1 predictor's calibrate-on-one-domain/predict-on-another test in both directions and report whether n_hat* falls within 2x of true n*; if no pair yields a finite crossover even after weakening, report that explicitly as a stronger, harder-to-dismiss negative result (crossover survives model weakening) rather than silently repeating the prior skip. Also report exact hyperparameters (epochs, learning rate, LR regularization strength, any validation-based selection) for every model variant to close the tuning-transparency gap, and log wall-clock/CPU-time per (domain,n,model) cell for the cost-benefit accounting.",
          "depends_on": [
            {"id": "art_jvhKSROMmhCr", "label": "dataset"},
            {"id": "art_Ak7R4sTP2lE4", "label": "protocol"},
            {"id": "art__VSV4YQ0_oJD", "label": "extends"}
          ]
        },
        {
          "type": "evaluation",
          "objective": "Provide the statistical rigor the reviewer demanded: a properly powered assessment of the coverage-curve/accuracy-gap relationship across all available (old and new) grid points and domains, an explicit power analysis for the small-n Spearman checks, and a quantitative wall-clock/compute cost-benefit comparison answering the paper's own motivating question.",
          "approach": "Pool per-(domain,n,seed) accuracy results and coverage curves from both the original experiment (art__VSV4YQ0_oJD, rotten_tomatoes/sst2/DistilBERT) and the new weakened-model/tweet_eval experiment. Compute (1) a post-hoc power analysis for Spearman correlation at the achieved n (4, and now up to 7x3 domain-model grid points), stating explicitly what effect size the test could and could not detect, replacing 'no reliable relationship' with a power-qualified statement; (2) the full within-2x calibrate/predict scorecard across every domain-model pair that has a finite empirical crossover (old and new), plus honest 'not evaluable' entries where none exists; (3) a bootstrap or permutation-based significance test on any newly observed crossover to rule out noise; (4) a wall-clock-cost-vs-accuracy-gain table (CPU-seconds to train TF-IDF+LR vs each transformer variant at each n, converted to a rough labeling-budget tradeoff) directly answering the introduction's 'when is switching worth it' framing; and (5) an explicit audit of whether DistilBERT's fixed-epoch training could have biased the original sweep, using the newly-logged hyperparameters.",
          "depends_on": [
            {"id": "art__VSV4YQ0_oJD", "label": "prior results"}
          ]
        },
        {
          "type": "research",
          "objective": "Conduct a targeted literature search for existing TF-IDF-vs-BERT small-data comparisons and few-shot text-classification baseline studies, to replace the paper's unsupported 'to our knowledge, no prior work' novelty claim with either concrete citations and a stated differentiation or an appropriately narrowed claim.",
          "approach": "Search terms such as 'TF-IDF logistic regression vs BERT few-shot text classification', 'small-data baseline comparison transformer NLP', 'when does BERT beat bag-of-words', and 'classical vs pretrained model crossover training size', across scholarly and general web modes, including workshop papers, Kaggle writeups, and applied-NLP blog posts. For each closest match found, extract what training sizes and datasets they used, whether they report a controlled sweep or an anecdotal one-off comparison, and whether they attempt any label-free prediction of the crossover point. Produce a short comparison table (this paper vs. each prior source) that the paper's Related Work section can cite directly, plus a recommended precise wording for the novelty claim scoped to what the search actually found (e.g. 'no peer-reviewed study we found combines a controlled sweep with a label-light crossover predictor').",
          "depends_on": []
        }
      ],
      "expected_outcome": "A genuinely tested crossover predictor: either a documented within-2x (or clearly-failed) prediction on at least one weakened-model/tweet_eval domain-model pair with a real finite crossover, or -- if no weakening produces one -- a much stronger negative result showing the crossover survives deliberate model weakening and an independent domain. Combined with a properly powered statistical analysis (replacing the unsupportable n=4 null claim), a wall-clock cost-benefit table answering the paper's own motivating question, full hyperparameter transparency, and a grounded novelty claim backed by an actual literature search, this directly resolves all three MAJOR and both MINOR reviewer critiques without merely re-running the same losing comparison at larger scale.",
      "summary": "Deliberately engineers a domain/model pair (weakened transformer variants + the unused independent tweet_eval domain) likely to produce a real, finite crossover, giving the label-light coverage predictor its first genuine test; pairs this with a properly powered statistical evaluation, a cost-benefit accounting, and a targeted novelty literature search to close every reviewer-flagged gap."
    }
  ]
}
```

### [5] TOOL RESULT — Write · 2026-09-05 19:22:04 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"strategies\": [\n    {\n      \"title\": \"Find a Real Crossover to Test the Predictor\",\n      \"objective\": \"Give the Good-Turing/Chao1 crossover predictor an actual target to be evaluated against -- by weakening the model side (a much smaller/less-pretrained transformer and a context-truncated DistilBERT) and adding the genuinely independent tweet_eval domain -- so the paper can report a real within-2x (or fails-to-predict) verdict instead of an untested algorithm, while fixing the statistical-power and cost-accounting gaps the reviewer flagged.\",\n      \"rationale\": \"The reviewer's top-priority MAJOR issue is that the paper's headline method was never evaluated against a real crossover: both calibrate/predict directions were skipped because DistilBERT always won. Rather than re-running the same losing comparison at more sizes, this strategy deliberately engineers a domain/model pair where a crossover can plausibly exist -- a weaker model (e.g. a from-scratch-embedding tiny transformer or logistic-regression-comparable capacity like a 2-layer LSTM/tinyBERT distillation) and/or a severely context-truncated DistilBERT (first 8-16 tokens only, discarding the long-range signal that gives it its edge on short movie-review text) -- alongside the already-assembled but unused tweet_eval domain, whose noisier, shorter register is the paper's own stated best candidate for a smaller initial gap. This directly answers MAJOR #1 (validate the predictor on a real target) and MAJOR #2 (stop treating RT/SST-2 as two independent domains by finally running the independent third domain). A dedicated evaluation artifact then fixes MAJOR #3 (statistical power of the n=4 Spearman check) and the two MINOR issues (hyperparameter/tuning transparency, cost-benefit quantification) without re-running the expensive sweep twice. A short targeted-research artifact closes MINOR #4 (novelty claim needs a real search, not 'to our knowledge').\",\n      \"artifact_directions\": [\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Establish at least one domain/model pair with a genuine, finite empirical crossover in the tested range, and use it as the first real test of the label-light coverage-based crossover predictor's calibrate-on-one/predict-on-another mechanism.\",\n          \"approach\": \"Reuse the existing dataset (rotten_tomatoes, sst2, tweet_eval) and the existing coverage-predictor code/protocol from the prior experiment and research artifacts. Add two model-weakening arms designed to induce a crossover: (a) a context-truncated DistilBERT that only sees the first 8 and 16 tokens of each example (removing the long-range signal that gives it its edge on short text), and (b) a much smaller/less-pretrained transformer (e.g. a 2-layer randomly-initialized or lightly-pretrained tiny-BERT-scale encoder, trained under the same CPU budget) as a genuinely weaker alternative to full DistilBERT. Run the full accuracy-vs-n sweep (TF-IDF+LR vs each weakened-model variant) on tweet_eval (the genuinely independent domain, not yet executed) plus at least one of rotten_tomatoes/sst2, at n in {50,100,200,500,1000,1500,2000} with >=5 seeds per cell, budgeting compute explicitly (drop the largest n or extra seeds first if a wall-clock guard triggers, exactly as before, and log every degradation). For whichever domain/model pair yields a finite empirical n* in this grid, run the Good-Turing/Chao1 predictor's calibrate-on-one-domain/predict-on-another test in both directions and report whether n_hat* falls within 2x of true n*; if no pair yields a finite crossover even after weakening, report that explicitly as a stronger, harder-to-dismiss negative result (crossover survives model weakening) rather than silently repeating the prior skip. Also report exact hyperparameters (epochs, learning rate, LR regularization strength, any validation-based selection) for every model variant to close the tuning-transparency gap, and log wall-clock/CPU-time per (domain,n,model) cell for the cost-benefit accounting.\",\n          \"depends_on\": [\n            {\"id\": \"art_jvhKSROMmhCr\", \"label\": \"dataset\"},\n            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"},\n            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"extends\"}\n          ]\n        },\n        {\n          \"type\": \"evaluation\",\n          \"objective\": \"Provide the statistical rigor the reviewer demanded: a properly powered assessment of the coverage-curve/accuracy-gap relationship across all available (old and new) grid points and domains, an explicit power analysis for the small-n Spearman checks, and a quantitative wall-clock/compute cost-benefit comparison answering the paper's own motivating question.\",\n          \"approach\": \"Pool per-(domain,n,seed) accuracy results and coverage curves from both the original experiment (art__VSV4YQ0_oJD, rotten_tomatoes/sst2/DistilBERT) and the new weakened-model/tweet_eval experiment. Compute (1) a post-hoc power analysis for Spearman correlation at the achieved n (4, and now up to 7x3 domain-model grid points), stating explicitly what effect size the test could and could not detect, replacing 'no reliable relationship' with a power-qualified statement; (2) the full within-2x calibrate/predict scorecard across every domain-model pair that has a finite empirical crossover (old and new), plus honest 'not evaluable' entries where none exists; (3) a bootstrap or permutation-based significance test on any newly observed crossover to rule out noise; (4) a wall-clock-cost-vs-accuracy-gain table (CPU-seconds to train TF-IDF+LR vs each transformer variant at each n, converted to a rough labeling-budget tradeoff) directly answering the introduction's 'when is switching worth it' framing; and (5) an explicit audit of whether DistilBERT's fixed-epoch training could have biased the original sweep, using the newly-logged hyperparameters.\",\n          \"depends_on\": [\n            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"prior results\"}\n          ]\n        },\n        {\n          \"type\": \"research\",\n          \"objective\": \"Conduct a targeted literature search for existing TF-IDF-vs-BERT small-data comparisons and few-shot text-classification baseline studies, to replace the paper's unsupported 'to our knowledge, no prior work' novelty claim with either concrete citations and a stated differentiation or an appropriately narrowed claim.\",\n          \"approach\": \"Search terms such as 'TF-IDF logistic regression vs BERT few-shot text classification', 'small-data baseline comparison transformer NLP', 'when does BERT beat bag-of-words', and 'classical vs pretrained model crossover training size', across scholarly and general web modes, including workshop papers, Kaggle writeups, and applied-NLP blog posts. For each closest match found, extract what training sizes and datasets they used, whether they report a controlled sweep or an anecdotal one-off comparison, and whether they attempt any label-free prediction of the crossover point. Produce a short comparison table (this paper vs. each prior source) that the paper's Related Work section can cite directly, plus a recommended precise wording for the novelty claim scoped to what the search actually found (e.g. 'no peer-reviewed study we found combines a controlled sweep with a label-light crossover predictor').\",\n          \"depends_on\": []\n        }\n      ],\n      \"expected_outcome\": \"A genuinely tested crossover predictor: either a documented within-2x (or clearly-failed) prediction on at least one weakened-model/tweet_eval domain-model pair with a real finite crossover, or -- if no weakening produces one -- a much stronger negative result showing the crossover survives deliberate model weakening and an independent domain. Combined with a properly powered statistical analysis (replacing the unsupportable n=4 null claim), a wall-clock cost-benefit table answering the paper's own motivating question, full hyperparameter transparency, and a grounded novelty claim backed by an actual literature search, this directly resolves all three MAJOR and both MINOR reviewer critiques without merely re-running the same losing comparison at larger scale.\",\n      \"summary\": \"Deliberately engineers a domain/model pair (weakened transformer variants + the unused independent tweet_eval domain) likely to produce a real, finite crossover, giving the label-light coverage predictor its first genuine test; pairs this with a properly powered statistical evaluation, a cost-benefit accounting, and a targeted novelty literature search to close every reviewer-flagged gap.\"\n    }\n  ]\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-09-05 19:22:05 UTC

```
Strategy generated and written to `./.terminal_claude_agent_struct_out.json`.
```

### [7] SYSTEM-USER prompt · 2026-09-05 19:22:06 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'experiment_iter2_dir1' (experiment): dependency 'art__VSV4YQ0_oJD' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})

</verification_results>

<task>
Fix ALL issues above and regenerate your strategies:

1. Fix dependency errors:
   - depends_on is a list of {id, label} objects — every entry MUST have a non-empty short label
   - id can ONLY reference IDs from <existing_artifacts>
   - You CANNOT reference artifacts you are proposing in this strategy as dependencies (they all run in parallel)
   - Follow the dependency type rules (e.g., experiments require datasets)
   - If no suitable existing artifacts exist, use depends_on: []

Output the corrected JSON with the fixed strategies.
</task>
```

### [8] TOOL CALL — Edit · 2026-09-05 19:22:12 UTC

```
File: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json
OLD:           "depends_on": [
            {"id": "art_jvhKSROMmhCr", "label": "dataset"},
            {"id": "art_Ak7R4sTP2lE4", "label": "protocol"},
            {"id": "art__VSV4YQ0_oJD", "label": "extends"}
          ]
        },
        {
          "type": "evaluation",
NEW:           "depends_on": [
            {"id": "art_jvhKSROMmhCr", "label": "dataset"},
            {"id": "art_Ak7R4sTP2lE4", "label": "protocol"}
          ]
        },
        {
          "type": "evaluation",
```

### [9] TOOL RESULT — Edit · 2026-09-05 19:22:12 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_2/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json", "oldString": "          \"depends_on\": [\n            {\"id\": \"art_jvhKSROMmhCr\", \"label\": \"dataset\"},\n            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"},\n            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"extends\"}\n          ]\n        },\n        {\n          \"type\": \"evaluation\",", "newString": "          \"depends_on\": [\n            {\"id\": \"art_jvhKSROMmhCr\", \"label\": \"dataset\"},\n            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"}\n          ]\n        },\n        {\n          \"type\": \"evaluation\",", "originalFile": "{\n  \"strategies\": [\n    {\n      \"title\": \"Find a Real Crossover to Test the Predictor\",\n      \"objective\": \"Give the Good-Turing/Chao1 crossover predictor an actual target to be evaluated against -- by weakening the model side (a much smaller/less-pretrained transformer and a context-truncated DistilBERT) and adding the genuinely independent tweet_eval domain -- so the paper can report a real within-2x (or fails-to-predict) verdict instead of an untested algorithm, while fixing the statistical-power and cost-accounting gaps the reviewer flagged.\",\n      \"rationale\": \"The reviewer's top-priority MAJOR issue is that the paper's headline method was never evaluated against a real crossover: both calibrate/predict directions were skipped because DistilBERT always won. Rather than re-running the same losing comparison at more sizes, this strategy deliberately engineers a domain/model pair where a crossover can plausibly exist -- a weaker model (e.g. a from-scratch-embedding tiny transformer or logistic-regression-comparable capacity like a 2-layer LSTM/tinyBERT distillation) and/or a severely context-truncated DistilBERT (first 8-16 tokens only, discarding the long-range signal that gives it its edge on short movie-review text) -- alongside the already-assembled but unused tweet_eval domain, whose noisier, shorter register is the paper's own stated best candidate for a smaller initial gap. This directly answers MAJOR #1 (validate the predictor on a real target) and MAJOR #2 (stop treating RT/SST-2 as two independent domains by finally running the independent third domain). A dedicated evaluation artifact then fixes MAJOR #3 (statistical power of the n=4 Spearman check) and the two MINOR issues (hyperparameter/tuning transparency, cost-benefit quantification) without re-running the expensive sweep twice. A short targeted-research artifact closes MINOR #4 (novelty claim needs a real search, not 'to our knowledge').\",\n      \"artifact_directions\": [\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Establish at least one domain/model pair with a genuine, finite empirical crossover in the tested range, and use it as the first real test of the label-light coverage-based crossover predictor's calibrate-on-one/predict-on-another mechanism.\",\n          \"approach\": \"Reuse the existing dataset (rotten_tomatoes, sst2, tweet_eval) and the existing coverage-predictor code/protocol from the prior experiment and research artifacts. Add two model-weakening arms designed to induce a crossover: (a) a context-truncated DistilBERT that only sees the first 8 and 16 tokens of each example (removing the long-range signal that gives it its edge on short text), and (b) a much smaller/less-pretrained transformer (e.g. a 2-layer randomly-initialized or lightly-pretrained tiny-BERT-scale encoder, trained under the same CPU budget) as a genuinely weaker alternative to full DistilBERT. Run the full accuracy-vs-n sweep (TF-IDF+LR vs each weakened-model variant) on tweet_eval (the genuinely independent domain, not yet executed) plus at least one of rotten_tomatoes/sst2, at n in {50,100,200,500,1000,1500,2000} with >=5 seeds per cell, budgeting compute explicitly (drop the largest n or extra seeds first if a wall-clock guard triggers, exactly as before, and log every degradation). For whichever domain/model pair yields a finite empirical n* in this grid, run the Good-Turing/Chao1 predictor's calibrate-on-one-domain/predict-on-another test in both directions and report whether n_hat* falls within 2x of true n*; if no pair yields a finite crossover even after weakening, report that explicitly as a stronger, harder-to-dismiss negative result (crossover survives model weakening) rather than silently repeating the prior skip. Also report exact hyperparameters (epochs, learning rate, LR regularization strength, any validation-based selection) for every model variant to close the tuning-transparency gap, and log wall-clock/CPU-time per (domain,n,model) cell for the cost-benefit accounting.\",\n          \"depends_on\": [\n            {\"id\": \"art_jvhKSROMmhCr\", \"label\": \"dataset\"},\n            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"},\n            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"extends\"}\n          ]\n        },\n        {\n          \"type\": \"evaluation\",\n          \"objective\": \"Provide the statistical rigor the reviewer demanded: a properly powered assessment of the coverage-curve/accuracy-gap relationship across all available (old and new) grid points and domains, an explicit power analysis for the small-n Spearman checks, and a quantitative wall-clock/compute cost-benefit comparison answering the paper's own motivating question.\",\n          \"approach\": \"Pool per-(domain,n,seed) accuracy results and coverage curves from both the original experiment (art__VSV4YQ0_oJD, rotten_tomatoes/sst2/DistilBERT) and the new weakened-model/tweet_eval experiment. Compute (1) a post-hoc power analysis for Spearman correlation at the achieved n (4, and now up to 7x3 domain-model grid points), stating explicitly what effect size the test could and could not detect, replacing 'no reliable relationship' with a power-qualified statement; (2) the full within-2x calibrate/predict scorecard across every domain-model pair that has a finite empirical crossover (old and new), plus honest 'not evaluable' entries where none exists; (3) a bootstrap or permutation-based significance test on any newly observed crossover to rule out noise; (4) a wall-clock-cost-vs-accuracy-gain table (CPU-seconds to train TF-IDF+LR vs each transformer variant at each n, converted to a rough labeling-budget tradeoff) directly answering the introduction's 'when is switching worth it' framing; and (5) an explicit audit of whether DistilBERT's fixed-epoch training could have biased the original sweep, using the newly-logged hyperparameters.\",\n          \"depends_on\": [\n            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"prior results\"}\n          ]\n        },\n        {\n          \"type\": \"research\",\n          \"objective\": \"Conduct a targeted literature search for existing TF-IDF-vs-BERT small-data comparisons and few-shot text-classification baseline studies, to replace the paper's unsupported 'to our knowledge, no prior work' novelty claim with either concrete citations and a stated differentiation or an appropriately narrowed claim.\",\n          \"approach\": \"Search terms such as 'TF-IDF logistic regression vs BERT few-shot text classification', 'small-data baseline comparison transformer NLP', 'when does BERT beat bag-of-words', and 'classical vs pretrained model crossover training size', across scholarly and general web modes, including workshop papers, Kaggle writeups, and applied-NLP blog posts. For each closest match found, extract what training sizes and datasets they used, whether they report a controlled sweep or an anecdotal one-off comparison, and whether they attempt any label-free prediction of the crossover point. Produce a short comparison table (this paper vs. each prior source) that the paper's Related Work section can cite directly, plus a recommended precise wording for the novelty claim scoped to what the search actually found (e.g. 'no peer-reviewed study we found combines a controlled sweep with a label-light crossover predictor').\",\n          \"depends_on\": []\n        }\n      ],\n      \"expected_outcome\": \"A genuinely tested crossover predictor: either a documented within-2x (or clearly-failed) prediction on at least one weakened-model/tweet_eval domain-model pair with a real finite crossover, or -- if no weakening produces one -- a much stronger negative result showing the crossover survives deliberate model weakening and an independent domain. Combined with a properly powered statistical analysis (replacing the unsupportable n=4 null claim), a wall-clock cost-benefit table answering the paper's own motivating question, full hyperparameter transparency, and a grounded novelty claim backed by an actual literature search, this directly resolves all three MAJOR and both MINOR reviewer critiques without merely re-running the same losing comparison at larger scale.\",\n      \"summary\": \"Deliberately engineers a domain/model pair (weakened transformer variants + the unused independent tweet_eval domain) likely to produce a real, finite crossover, giving the label-light coverage predictor its first genuine test; pairs this with a properly powered statistical evaluation, a cost-benefit accounting, and a targeted novelty literature search to close every reviewer-flagged gap.\"\n    }\n  ]\n}\n", "structuredPatch": [{"oldStart": 11, "oldLines": 8, "newStart": 11, "newLines": 7, "lines": ["           \"approach\": \"Reuse the existing dataset (rotten_tomatoes, sst2, tweet_eval) and the existing coverage-predictor code/protocol from the prior experiment and research artifacts. Add two model-weakening arms designed to induce a crossover: (a) a context-truncated DistilBERT that only sees the first 8 and 16 tokens of each example (removing the long-range signal that gives it its edge on short text), and (b) a much smaller/less-pretrained transformer (e.g. a 2-layer randomly-initialized or lightly-pretrained tiny-BERT-scale encoder, trained under the same CPU budget) as a genuinely weaker alternative to full DistilBERT. Run the full accuracy-vs-n sweep (TF-IDF+LR vs each weakened-model variant) on tweet_eval (the genuinely independent domain, not yet executed) plus at least one of rotten_tomatoes/sst2, at n in {50,100,200,500,1000,1500,2000} with >=5 seeds per cell, budgeting compute explicitly (drop the largest n or extra seeds first if a wall-clock guard triggers, exactly as before, and log every degradation). For whichever domain/model pair yields a finite empirical n* in this grid, run the Good-Turing/Chao1 predictor's calibrate-on-one-domain/predict-on-another test in both directions and report whether n_hat* falls within 2x of true n*; if no pair yields a finite crossover even after weakening, report that explicitly as a stronger, harder-to-dismiss negative result (crossover survives model weakening) rather than silently repeating the prior skip. Also report exact hyperparameters (epochs, learning rate, LR regularization strength, any validation-based selection) for every model variant to close the tuning-transparency gap, and log wall-clock/CPU-time per (domain,n,model) cell for the cost-benefit accounting.\",", "           \"depends_on\": [", "             {\"id\": \"art_jvhKSROMmhCr\", \"label\": \"dataset\"},", "-            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"},", "-            {\"id\": \"art__VSV4YQ0_oJD\", \"label\": \"extends\"}", "+            {\"id\": \"art_Ak7R4sTP2lE4\", \"label\": \"protocol\"}", "           ]", "         },", "         {"]}], "userModified": false, "replaceAll": false}
```

### [10] ASSISTANT · 2026-09-05 19:22:14 UTC

```
Fixed — removed the disallowed `experiment`-type dependency (`art__VSV4YQ0_oJD`) from the new experiment artifact, keeping it only for the evaluation artifact where an EXPERIMENT dependency is valid. The dataset and research dependencies on the experiment artifact remain, satisfying the "experiments require at least one dataset" rule.
```
