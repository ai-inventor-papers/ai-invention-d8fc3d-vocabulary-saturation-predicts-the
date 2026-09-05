# gen_demo_art_experiment_1 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_2ohq8qwlCPMZ` — Weakening the Transformer Reveals a Crossover, but the Label-Free Predictor Still Cannot Find It
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-09-05 21:23:59 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
```

### [2] SYSTEM-USER prompt · 2026-09-05 21:24:05 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

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
Your workspace: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/`:
GOOD: `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/file.py`, `/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
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
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json"
import json, os

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-05 21:24:05 UTC

```
Small-data text classification: does a TF-IDF + logistic-regression baseline match a small fine-tuned transformer (DistilBERT) on short-text sentiment when fewer than 2,000 labelled examples are available? Use a small public dataset such as the Rotten Tomatoes or SST-2 subset, CPU-only experiments, and report accuracy vs training-set size.
```

### [4] TOOL CALL — Skill · 2026-09-05 21:24:11 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-05 21:24:11 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-05 21:24:11 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-05 21:24:11 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-05 21:24:11 UTC

```
ls -la; echo ---; ls -la /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
```

### [9] TOOL RESULT — Bash · 2026-09-05 21:24:11 UTC

```
{"stdout": "total 1983\ndrwxr-xr-x 2 root root 1002129 Sep  5 21:23 .\ndrwxr-xr-x 4 root root 1005684 Sep  5 21:23 ..\n-rw-r--r-- 1 root root   21811 Sep  5 21:24 .repl_agent.ptylog\n---\ntotal 6992\ndrwxr-xr-x 6 root root 2000118 Sep  5 17:47 .\ndrwxr-xr-x 5 root root 2004011 Sep  5 14:19 ..\ndrwxr-xr-x 2 root root       1 Sep  5 17:09 .claude\n-rw-r--r-- 1 root root  619287 Sep  5 17:29 .repl_agent.ptylog\n-rw-r--r-- 1 root root    3604 Sep  5 17:29 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root   40167 Sep  5 17:28 full_method_out.json\ndrwxr-xr-x 2 root root       1 Sep  5 17:28 hf_runs\ndrwxr-xr-x 2 root root 1009896 Sep  5 16:58 logs\n-rw-r--r-- 1 root root   33571 Sep  5 16:58 method.py\n-rw-r--r-- 1 root root   40167 Sep  5 17:28 method_out.json\n-rw-r--r-- 1 root root    9830 Sep  5 17:28 mini_method_out.json\n-rw-r--r-- 1 root root    4826 Sep  5 17:28 preview_method_out.json\n-rw-r--r-- 1 root root     333 Sep  5 16:58 pyproject.toml\ndrwxr-xr-x 2 root root 1000191 Sep  5 16:37 results\n-rw-r--r-- 1 root root  388368 Sep  5 16:58 uv.lock", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Read · 2026-09-05 21:24:17 UTC

```
/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py
```

### [11] TOOL RESULT — Read · 2026-09-05 21:24:17 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py", "content": "#!/usr/bin/env python3\n\"\"\"TF-IDF+LR vs CPU-fine-tuned DistilBERT crossover point, and a label-free\nGood-Turing/Chao1 unseen-vocabulary-mass predictor of that crossover, tested\nfor cross-domain transfer across short-text sentiment domains.\n\"\"\"\nfrom __future__ import annotations\n\nimport gc\nimport json\nimpor... [truncated, 35203 chars total]
```

### [12] TOOL CALL — Read · 2026-09-05 21:24:17 UTC

```
/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/preview_method_out.json
```

### [13] TOOL RESULT — Read · 2026-09-05 21:24:17 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/preview_method_out.json", "content": "{\n  \"metadata\": {\n    \"method_name\": \"tfidf_vs_distilbert_crossover_with_gt_predictor\",\n    \"description\": \"Empirical accuracy-vs-n crossover between TF-IDF+LR and CPU-fine-tuned DistilBERT, plus a label-free Good-Turing/Chao1 unseen-vocabulary-mass predictor of that crossover, tested for cross-domain trans...\",\n    \"parameters\": {\n      \"NS\": [\n        50,\n        200,\n        500\n      ],\n      \"SEEDS\": [\n        0,\n        1\n      ],\n      \"DOMAINS\": [\n        \"rotten_tomatoes\",\n        \"sst2\"\n      ],\n      \"PILOT_NS\": [\n        100,\n        200,\n        400\n      ],\n      \"VOCAB_METHODS\": [\n        \"mi\",\n        \"freq\"\n      ],\n      \"MAX_LEN\": 64,\n      \"TEST_N\": 800\n    }\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"raw_results\",\n      \"examples\": [\n        {\n          \"input\": \"domain=rotten_tomatoes n=50 seed=0\",\n          \"output\": \"acc_tfidf=0.5413 acc_distilbert=0.6525\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 50,\n          \"metadata_seed\": 0,\n          \"metadata_acc_tfidf\": 0.54125,\n          \"metadata_acc_distilbert\": 0.6525,\n          \"metadata_db_train_secs\": 20.329676389694214,\n          \"predict_tfidf_lr_acc\": \"0.5413\",\n          \"predict_distilbert_acc\": \"0.6525\"\n        },\n        {\n          \"input\": \"domain=rotten_tomatoes n=50 seed=1\",\n          \"output\": \"acc_tfidf=0.5312 acc_distilbert=0.7250\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 50,\n          \"metadata_seed\": 1,\n          \"metadata_acc_tfidf\": 0.53125,\n          \"metadata_acc_distilbert\": 0.725,\n          \"metadata_db_train_secs\": 27.481956958770752,\n          \"predict_tfidf_lr_acc\": \"0.5312\",\n          \"predict_distilbert_acc\": \"0.7250\"\n        },\n        {\n          \"input\": \"domain=rotten_tomatoes n=200 seed=0\",\n          \"output\": \"acc_tfidf=0.5988 acc_distilbert=0.7987\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 200,\n          \"metadata_seed\": 0,\n          \"metadata_acc_tfidf\": 0.59875,\n          \"metadata_acc_distilbert\": 0.79875,\n          \"metadata_db_train_secs\": 93.5441300868988,\n          \"predict_tfidf_lr_acc\": \"0.5988\",\n          \"predict_distilbert_acc\": \"0.7987\"\n        }\n      ]\n    },\n    {\n      \"dataset\": \"accuracy_curve\",\n      \"examples\": [\n        {\n          \"input\": \"domain=rotten_tomatoes n=50\",\n          \"output\": \"mean_tfidf=0.5363+-0.0098 mean_db=0.6887+-0.0711 gap=0.1525\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 50,\n          \"metadata_mean_tfidf\": 0.53625,\n          \"metadata_ci_tfidf\": 0.009800000000000008,\n          \"metadata_mean_db\": 0.68875,\n          \"metadata_ci_db\": 0.07105,\n          \"metadata_gap\": 0.15249999999999997,\n          \"metadata_n_seeds\": 2,\n          \"predict_tfidf_lr_mean_acc\": \"0.5363\",\n          \"predict_distilbert_mean_acc\": \"0.6887\"\n        },\n        {\n          \"input\": \"domain=rotten_tomatoes n=200\",\n          \"output\": \"mean_tfidf=0.6056+-0.0135 mean_db=0.8069+-0.0159 gap=0.2012\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 200,\n          \"metadata_mean_tfidf\": 0.6056250000000001,\n          \"metadata_ci_tfidf\": 0.013475000000000037,\n          \"metadata_mean_db\": 0.806875,\n          \"metadata_ci_db\": 0.015924999999999984,\n          \"metadata_gap\": 0.20124999999999993,\n          \"metadata_n_seeds\": 2,\n          \"predict_tfidf_lr_mean_acc\": \"0.6056\",\n          \"predict_distilbert_mean_acc\": \"0.8069\"\n        },\n        {\n          \"input\": \"domain=rotten_tomatoes n=500\",\n          \"output\": \"mean_tfidf=0.6444+-0.0135 mean_db=0.8325+-0.0147 gap=0.1881\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n\": 500,\n          \"metadata_mean_tfidf\": 0.6443749999999999,\n          \"metadata_ci_tfidf\": 0.013475000000000037,\n          \"metadata_mean_db\": 0.8325,\n          \"metadata_ci_db\": 0.014700000000000012,\n          \"metadata_gap\": 0.1881250000000001,\n          \"metadata_n_seeds\": 2,\n          \"predict_tfidf_lr_mean_acc\": \"0.6444\",\n          \"predict_distilbert_mean_acc\": \"0.8325\"\n        }\n      ]\n    },\n    {\n      \"dataset\": \"true_crossovers\",\n      \"examples\": [\n        {\n          \"input\": \"domain=rotten_tomatoes\",\n          \"output\": \"n_star=None direction=distilbert_ahead_at_all_tested_n\",\n          \"metadata_domain\": \"rotten_tomatoes\",\n          \"metadata_n_star\": null,\n          \"metadata_direction\": \"distilbert_ahead_at_all_tested_n\",\n          \"predict_empirical_crossover_n\": \"None\"\n        },\n        {\n          \"input\": \"domain=sst2\",\n          \"output\": \"n_star=None direction=distilbert_ahead_at_all_tested_n\",\n          \"metadata_domain\": \"sst2\",\n          \"metadata_n_star\": null,\n          \"metadata_direction\": \"distilbert_ahead_at_all_tested_n\",\n          \"predict_empirical_crossover_n\": \"None\"\n        }\n      ]\n    }\n  ]\n}", "numLines": 143, "startLine": 1, "totalLines": 143}}
```

### [14] TOOL CALL — Bash · 2026-09-05 21:24:25 UTC

```
python3 -c "
import urllib.request
try:
    urllib.request.urlopen('https://huggingface.co', timeout=5)
    print('internet OK')
except Exception as e:
    print('no internet', e)
"
which uv; uv --version 2>/dev/null || echo no-uv
```

### [15] TOOL RESULT — Bash · 2026-09-05 21:24:25 UTC

```
{"stdout": "internet OK\n/usr/bin/uv\nuv 0.6.14", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-09-05 21:24:33 UTC

```
Internet works, so I'll fetch a small real sample from rotten_tomatoes directly to build the mini demo data file.
```

### [17] TOOL CALL — Bash · 2026-09-05 21:24:33 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
pip show datasets 2>/dev/null | head -2 || echo "no datasets installed"
python3 -c "import datasets" 2>&1 | tail -3
```

### [18] TOOL RESULT — Bash · 2026-09-05 21:24:33 UTC

```
{"stdout": "Name: datasets\nVersion: 5.0.1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-05 21:24:43 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
from datasets import load_dataset
import numpy as np

rt = load_dataset('cornell-movie-review-data/rotten_tomatoes')
texts = list(rt['train']['text']) + list(rt['validation']['text'])
labels = list(rt['train']['label']) + list(rt['validation']['label'])
texts = [str(t)[:300] for t in texts]
labels = [int(l) for l in labels]

rng = np.random.default_rng(0)
order = rng.permutation(len(texts))
texts = [texts[i] for i in order]
labels = [labels[i] for i in order]

pos_idx = [i for i,l in enumerate(labels) if l==1]
neg_idx = [i for i,l in enumerate(labels) if l==0]

def take(idx_list, k, used):
    out = []
    for i in idx_list:
        if i in used: continue
        out.append(i)
        used.add(i)
        if len(out)==k: break
    return out

used = set()
labeled_idx = take(pos_idx, 30, used) + take(neg_idx, 30, used)
test_idx = take(pos_idx, 10, used) + take(neg_idx, 10, used)
unlabeled_idx = take(pos_idx, 10, used) + take(neg_idx, 10, used)

data = {
  'rotten_tomatoes': {
    'labeled_texts': [texts[i] for i in labeled_idx],
    'labeled_labels': [labels[i] for i in labeled_idx],
    'test_texts': [texts[i] for i in test_idx],
    'test_labels': [labels[i] for i in test_idx],
    'unlabeled_pool': [texts[i] for i in unlabeled_idx],
  }
}
with open('mini_demo_data.json','w') as f:
    json.dump(data, f, indent=2)
print('labeled', len(data['rotten_tomatoes']['labeled_texts']))
print('test', len(data['rotten_tomatoes']['test_texts']))
print('unlabeled', len(data['rotten_tomatoes']['unlabeled_pool']))
"
ls -la mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-05 21:24:51 UTC

```
{"stdout": "\rGenerating train split:   0%|          | 0/8530 [00:00<?, ? examples/s]\rGenerating train split: 100%|██████████| 8530/8530 [00:00<00:00, 1161340.38 examples/s]\n\rGenerating validation split:   0%|          | 0/1066 [00:00<?, ? examples/s]\rGenerating validation split: 100%|██████████| 1066/1066 [00:00<00:00, 572414.30 examples/s]\n\rGenerating test split:   0%|          | 0/1066 [00:00<?, ? examples/s]\rGenerating test split: 100%|██████████| 1066/1066 [00:00<00:00, 771682.44 examples/s]\nlabeled 60\ntest 20\nunlabeled 20\n-rw-r--r-- 1 root root 13607 Sep  5 21:24 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-05 21:24:53 UTC

```
Good, mini data created. Now let's build the notebook.
```

### [22] TOOL CALL — ToolSearch · 2026-09-05 21:24:53 UTC

```
{'query': 'select:NotebookEdit', 'max_results': 3}
```

### [23] TOOL RESULT — ToolSearch · 2026-09-05 21:24:53 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit", "total_deferred_tools": 18}
```

### [24] TOOL CALL — Write · 2026-09-05 21:25:19 UTC

```
File: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb

{
 "cells": [],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.12.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

### [25] TOOL RESULT — Write · 2026-09-05 21:25:19 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "content": "{\n \"cells\": [],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12.0\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [26] TOOL CALL — Read · 2026-09-05 21:25:25 UTC

```
/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb
```

### [27] TOOL RESULT — Read · 2026-09-05 21:25:25 UTC

```
{"type": "notebook", "file": {"filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "cells": []}}
```

### [28] TOOL CALL — NotebookEdit · 2026-09-05 21:25:33 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '# TF-IDF vs DistilBERT Crossover on Small Text Data\\n\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\n\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\"crossover point\\"), and whether that predictor transfers across domains.\\n\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\n\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep."'}
```

### [29] TOOL RESULT — NotebookEdit · 2026-09-05 21:25:33 UTC

```
{"new_source": "# TF-IDF vs DistilBERT Crossover on Small Text Data\\n\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\n\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\"crossover point\\\"), and whether that predictor transfers across domains.\\n\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\n\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\"", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "1a01fff1", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12.0\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [30] TOOL CALL — NotebookEdit · 2026-09-05 21:25:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '1a01fff1', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': "import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n_pip('psutil==7.1.0')\\n\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\n         'torch==2.9.0', 'transformers==5.0.0')"}
```

### [31] TOOL RESULT — NotebookEdit · 2026-09-05 21:25:41 UTC

```
{"new_source": "import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n_pip('psutil==7.1.0')\\n\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\n         'torch==2.9.0', 'transformers==5.0.0')", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "55a73462", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [32] TOOL CALL — NotebookEdit · 2026-09-05 21:25:45 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '55a73462', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Imports and hardware setup\\n\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard."'}
```

### [33] TOOL RESULT — NotebookEdit · 2026-09-05 21:25:45 UTC

```
{"new_source": "## Imports and hardware setup\\n\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\"", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "562c38f5", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [34] TOOL CALL — NotebookEdit · 2026-09-05 21:25:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '562c38f5', 'cell_type': 'markdown', 'new_source': '## Imports and hardware setup\\n\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.'}
```

### [35] TOOL RESULT — NotebookEdit · 2026-09-05 21:25:49 UTC

```
{"new_source": "## Imports and hardware setup\\n\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.", "old_source": "## Imports and hardware setup\\n\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\"", "cell_type": "markdown", "language": "python", "edit_mode": "replace", "cell_id": "562c38f5", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [36] TOOL CALL — NotebookEdit · 2026-09-05 21:26:01 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '562c38f5', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': 'from __future__ import annotations\\n\\nimport gc\\nimport json\\nimport math\\nimport os\\nimport random\\nimport resource\\nimport sys\\nimport time\\nfrom pathlib import Path\\n\\nimport numpy as np\\nimport pandas as pd\\nimport psutil\\nfrom loguru import logger\\nfrom scipy.stats import spearmanr\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\nfrom sklearn.feature_selection import mutual_info_classif\\nfrom sklearn.linear_model import LogisticRegression\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\n\\nWORKDIR = Path.cwd()\\nos.environ.setdefault(\\"HF_HOME\\", str(WORKDIR / \\".hf_cache\\"))\\nos.environ.setdefault(\\"HF_DATASETS_CACHE\\", str(WORKDIR / \\".hf_cache\\" / \\"datasets\\"))\\nos.environ.setdefault(\\"TRANSFORMERS_CACHE\\", str(WORKDIR / \\".hf_cache\\" / \\"transformers\\"))\\nos.environ.setdefault(\\"TOKENIZERS_PARALLELISM\\", \\"false\\")\\nos.environ.setdefault(\\"OMP_NUM_THREADS\\", \\"4\\")\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\"INFO\\", format=\\"{time:HH:mm:ss}|{level:<7}|{message}\\")\\n(WORKDIR / \\"logs\\").mkdir(exist_ok=True)\\nlogger.add(WORKDIR / \\"logs\\" / \\"run.log\\", rotation=\\"30 MB\\", level=\\"DEBUG\\")\\n\\n# ------------------------------------------------------------------ hardware\\ndef _detect_cpus() -> int:\\n    try:\\n        parts = Path(\\"/sys/fs/cgroup/cpu.max\\").read_text().split()\\n        if parts[0] != \\"max\\":\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\n    except (FileNotFoundError, ValueError):\\n        pass\\n    try:\\n        return len(os.sched_getaffinity(0))\\n    except (AttributeError, OSError):\\n        return os.cpu_count() or 1\\n\\n\\ndef _container_ram_gb() -> float:\\n    for p in [\\"/sys/fs/cgroup/memory.max\\", \\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\"]:\\n        try:\\n            v = Path(p).read_text().strip()\\n            if v != \\"max\\" and int(v) < 1_000_000_000_000:\\n                return int(v) / 1e9\\n        except (FileNotFoundError, ValueError):\\n            pass\\n    return psutil.virtual_memory().total / 1e9\\n\\n\\nNUM_CPUS = _detect_cpus()\\nTOTAL_RAM_GB = _container_ram_gb()\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\nlogger.info(f\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\")\\n\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\n\\ntorch.set_num_threads(max(1, NUM_CPUS))\\nfrom transformers import (  # noqa: E402\\n    DistilBertForSequenceClassification,\\n    DistilBertTokenizerFast,\\n    Trainer,\\n    TrainingArguments,\\n)'}
```

### [37] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:01 UTC

```
{"new_source": "from __future__ import annotations\\n\\nimport gc\\nimport json\\nimport math\\nimport os\\nimport random\\nimport resource\\nimport sys\\nimport time\\nfrom pathlib import Path\\n\\nimport numpy as np\\nimport pandas as pd\\nimport psutil\\nfrom loguru import logger\\nfrom scipy.stats import spearmanr\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\nfrom sklearn.feature_selection import mutual_info_classif\\nfrom sklearn.linear_model import LogisticRegression\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\n\\nWORKDIR = Path.cwd()\\nos.environ.setdefault(\\\"HF_HOME\\\", str(WORKDIR / \\\".hf_cache\\\"))\\nos.environ.setdefault(\\\"HF_DATASETS_CACHE\\\", str(WORKDIR / \\\".hf_cache\\\" / \\\"datasets\\\"))\\nos.environ.setdefault(\\\"TRANSFORMERS_CACHE\\\", str(WORKDIR / \\\".hf_cache\\\" / \\\"transformers\\\"))\\nos.environ.setdefault(\\\"TOKENIZERS_PARALLELISM\\\", \\\"false\\\")\\nos.environ.setdefault(\\\"OMP_NUM_THREADS\\\", \\\"4\\\")\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\\n(WORKDIR / \\\"logs\\\").mkdir(exist_ok=True)\\nlogger.add(WORKDIR / \\\"logs\\\" / \\\"run.log\\\", rotation=\\\"30 MB\\\", level=\\\"DEBUG\\\")\\n\\n# ------------------------------------------------------------------ hardware\\ndef _detect_cpus() -> int:\\n    try:\\n        parts = Path(\\\"/sys/fs/cgroup/cpu.max\\\").read_text().split()\\n        if parts[0] != \\\"max\\\":\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\n    except (FileNotFoundError, ValueError):\\n        pass\\n    try:\\n        return len(os.sched_getaffinity(0))\\n    except (AttributeError, OSError):\\n        return os.cpu_count() or 1\\n\\n\\ndef _container_ram_gb() -> float:\\n    for p in [\\\"/sys/fs/cgroup/memory.max\\\", \\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\"]:\\n        try:\\n            v = Path(p).read_text().strip()\\n            if v != \\\"max\\\" and int(v) < 1_000_000_000_000:\\n                return int(v) / 1e9\\n        except (FileNotFoundError, ValueError):\\n            pass\\n    return psutil.virtual_memory().total / 1e9\\n\\n\\nNUM_CPUS = _detect_cpus()\\nTOTAL_RAM_GB = _container_ram_gb()\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\nlogger.info(f\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\")\\n\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\n\\ntorch.set_num_threads(max(1, NUM_CPUS))\\nfrom transformers import (  # noqa: E402\\n    DistilBertForSequenceClassification,\\n    DistilBertTokenizerFast,\\n    Trainer,\\n    TrainingArguments,\\n)", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "54038839", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [38] ASSISTANT · 2026-09-05 21:26:09 UTC

```
Now the data-loading cells.
```

### [39] TOOL CALL — NotebookEdit · 2026-09-05 21:26:09 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '54038839', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Load the demo data\\n\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn\'t need to fetch and process full datasets. It\'s loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab."'}
```

### [40] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:09 UTC

```
{"new_source": "## Load the demo data\\n\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\"", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "e5f425bc", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [41] TOOL CALL — NotebookEdit · 2026-09-05 21:26:13 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'e5f425bc', 'cell_type': 'markdown', 'new_source': "## Load the demo data\\n\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab."}
```

### [42] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:13 UTC

```
{"new_source": "## Load the demo data\\n\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.", "old_source": "## Load the demo data\\n\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\"", "cell_type": "markdown", "language": "python", "edit_mode": "replace", "cell_id": "e5f425bc", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [43] TOOL CALL — NotebookEdit · 2026-09-05 21:26:17 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'e5f425bc', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\"\\nimport json, os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception: pass\\n    if os.path.exists(\\"mini_demo_data.json\\"):\\n        with open(\\"mini_demo_data.json\\") as f: return json.load(f)\\n    raise FileNotFoundError(\\"Could not load mini_demo_data.json\\")'}
```

### [44] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:17 UTC

```
{"new_source": "GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\"\\nimport json, os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception: pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f: return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "b1554b31", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [45] TOOL CALL — NotebookEdit · 2026-09-05 21:26:23 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'b1554b31', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': 'data = load_data()\\nprint(\\"domains in demo data:\\", list(data.keys()))\\nfor dom, d in data.items():\\n    print(f\\"  {dom}: labeled={len(d[\'labeled_texts\'])} unlabeled={len(d[\'unlabeled_pool\'])} test={len(d[\'test_texts\'])}\\")'}
```

### [46] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:23 UTC

```
{"new_source": "data = load_data()\\nprint(\\\"domains in demo data:\\\", list(data.keys()))\\nfor dom, d in data.items():\\n    print(f\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "173915af", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [47] ASSISTANT · 2026-09-05 21:26:29 UTC

```
Now the config cell.
```

### [48] TOOL CALL — NotebookEdit · 2026-09-05 21:26:29 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '173915af', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Config\\n\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction."'}
```

### [49] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:29 UTC

```
{"new_source": "## Config\\n\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\"", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "2e0c395d", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"2e0c395d\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [50] TOOL CALL — NotebookEdit · 2026-09-05 21:26:33 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '2e0c395d', 'cell_type': 'markdown', 'new_source': '## Config\\n\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.'}
```

### [51] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:33 UTC

```
{"new_source": "## Config\\n\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.", "old_source": "## Config\\n\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\"", "cell_type": "markdown", "language": "python", "edit_mode": "replace", "cell_id": "2e0c395d", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"2e0c395d\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\\\"\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"2e0c395d\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [52] TOOL CALL — NotebookEdit · 2026-09-05 21:26:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '2e0c395d', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# --------------------------------------------------------------- DEMO config (minimal, fast)\\nSEEDS_FULL = [0]                 # original: [0, 1]\\nNS_FULL = [20, 50]               # original: [50, 200, 500, 1000] (bounded by our 60-example labeled pool)\\nDOMAINS_ORDER = [\\"rotten_tomatoes\\"]  # original: [\\"rotten_tomatoes\\", \\"sst2\\", \\"imdb\\"]\\nPILOT_NS = [20]                  # original: [100, 200, 400]\\nVOCAB_METHODS = [\\"mi\\"]           # original: [\\"mi\\", \\"freq\\"]\\nTEST_N = 20                      # original: 800 (fixed held-out size per domain)\\nUNLABELED_POOL_N = 20            # original: 6000\\nLABELED_POOL_CAP = 60            # original: 4000\\nMAX_LEN = 64                     # unchanged\\nN_BOOTSTRAP = 5                  # original: 15 (bootstrap resamples per coverage-curve point)\\nTIME_BUDGET_S = 8 * 60.0         # original: 35 * 60.0 (wall-clock budget for the DistilBERT sweep)\\n\\n_EPOCH_TIERS = {20: 1, 50: 1, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}  # original: {50: 5, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}\\n\\nPART_A_START = time.time()\\nCHECKPOINT_PATH = WORKDIR / \\"results\\" / \\"part_a_checkpoint.json\\"\\ndegradation_log: list[str] = []\\n\\n\\ndef ci95(vals) -> float:\\n    vals = np.asarray(vals, dtype=float)\\n    vals = vals[~np.isnan(vals)]\\n    if len(vals) < 2:\\n        return 0.0\\n    return 1.96 * vals.std(ddof=1) / math.sqrt(len(vals))'}
```

### [53] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:41 UTC

```
{"new_source": "# --------------------------------------------------------------- DEMO config (minimal, fast)\\nSEEDS_FULL = [0]                 # original: [0, 1]\\nNS_FULL = [20, 50]               # original: [50, 200, 500, 1000] (bounded by our 60-example labeled pool)\\nDOMAINS_ORDER = [\\\"rotten_tomatoes\\\"]  # original: [\\\"rotten_tomatoes\\\", \\\"sst2\\\", \\\"imdb\\\"]\\nPILOT_NS = [20]                  # original: [100, 200, 400]\\nVOCAB_METHODS = [\\\"mi\\\"]           # original: [\\\"mi\\\", \\\"freq\\\"]\\nTEST_N = 20                      # original: 800 (fixed held-out size per domain)\\nUNLABELED_POOL_N = 20            # original: 6000\\nLABELED_POOL_CAP = 60            # original: 4000\\nMAX_LEN = 64                     # unchanged\\nN_BOOTSTRAP = 5                  # original: 15 (bootstrap resamples per coverage-curve point)\\nTIME_BUDGET_S = 8 * 60.0         # original: 35 * 60.0 (wall-clock budget for the DistilBERT sweep)\\n\\n_EPOCH_TIERS = {20: 1, 50: 1, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}  # original: {50: 5, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}\\n\\nPART_A_START = time.time()\\nCHECKPOINT_PATH = WORKDIR / \\\"results\\\" / \\\"part_a_checkpoint.json\\\"\\ndegradation_log: list[str] = []\\n\\n\\ndef ci95(vals) -> float:\\n    vals = np.asarray(vals, dtype=float)\\n    vals = vals[~np.isnan(vals)]\\n    if len(vals) < 2:\\n        return 0.0\\n    return 1.96 * vals.std(ddof=1) / math.sqrt(len(vals))", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "c0fb31d5", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"2e0c395d\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1a01fff1\",\n   \"source\": \"# TF-IDF vs DistilBERT Crossover on Small Text Data\\\\n\\\\nThis notebook is a lightly-restructured, cell-by-cell version of the original `method.py` script.\\\\n\\\\n**What the original experiment does:** it compares a classical TF-IDF + logistic-regression text classifier against a CPU-fine-tuned DistilBERT model on short-text sentiment classification (Rotten Tomatoes / SST-2), sweeping the training-set size `n` over `{50, 200, 500, 1000}` with 2 seeds per `(domain, n)`. It then asks whether a **label-free** signal — the Good-Turing/Chao1 estimate of *unseen n-gram vocabulary mass* on a small unlabeled pilot sample — can predict the `n` at which DistilBERT overtakes TF-IDF (the \\\\\\\"crossover point\\\\\\\"), and whether that predictor transfers across domains.\\\\n\\\\n**Result in the full run:** DistilBERT was ahead of TF-IDF+LR at *every* tested `n` on both domains, so there was no finite empirical crossover to predict against — the overall verdict recorded was `DISCONFIRMED`, but the full pipeline (both classifiers, the coverage-curve machinery, and the cross-domain calibration logic) is intact and runnable end-to-end.\\\\n\\\\n**This demo** runs the exact same code path on a tiny curated subset of Rotten Tomatoes (bundled as `mini_demo_data.json`, ~100 examples) with minimal config (few `n` values, 1 seed, 1 fine-tuning epoch) so it finishes in a couple of minutes instead of tens of minutes on the full sweep.\\\"\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"55a73462\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\\\n         'torch==2.9.0', 'transformers==5.0.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"562c38f5\",\n   \"source\": \"## Imports and hardware setup\\\\n\\\\nCopied from the top of `method.py` almost as-is: environment variables for HF caching, thread counts, logging setup, and the container-aware CPU/RAM detection used to size a `RLIMIT_AS` guard.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"54038839\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport gc\\\\nimport json\\\\nimport math\\\\nimport os\\\\nimport random\\\\nimport resource\\\\nimport sys\\\\nimport time\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport pandas as pd\\\\nimport psutil\\\\nfrom loguru import logger\\\\nfrom scipy.stats import spearmanr\\\\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\\\\nfrom sklearn.feature_selection import mutual_info_classif\\\\nfrom sklearn.linear_model import LogisticRegression\\\\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\\\\n\\\\nWORKDIR = Path.cwd()\\\\nos.environ.setdefault(\\\\\\\"HF_HOME\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"HF_DATASETS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"datasets\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TRANSFORMERS_CACHE\\\\\\\", str(WORKDIR / \\\\\\\".hf_cache\\\\\\\" / \\\\\\\"transformers\\\\\\\"))\\\\nos.environ.setdefault(\\\\\\\"TOKENIZERS_PARALLELISM\\\\\\\", \\\\\\\"false\\\\\\\")\\\\nos.environ.setdefault(\\\\\\\"OMP_NUM_THREADS\\\\\\\", \\\\\\\"4\\\\\\\")\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\\\\n(WORKDIR / \\\\\\\"logs\\\\\\\").mkdir(exist_ok=True)\\\\nlogger.add(WORKDIR / \\\\\\\"logs\\\\\\\" / \\\\\\\"run.log\\\\\\\", rotation=\\\\\\\"30 MB\\\\\\\", level=\\\\\\\"DEBUG\\\\\\\")\\\\n\\\\n# ------------------------------------------------------------------ hardware\\\\ndef _detect_cpus() -> int:\\\\n    try:\\\\n        parts = Path(\\\\\\\"/sys/fs/cgroup/cpu.max\\\\\\\").read_text().split()\\\\n        if parts[0] != \\\\\\\"max\\\\\\\":\\\\n            return math.ceil(int(parts[0]) / int(parts[1]))\\\\n    except (FileNotFoundError, ValueError):\\\\n        pass\\\\n    try:\\\\n        return len(os.sched_getaffinity(0))\\\\n    except (AttributeError, OSError):\\\\n        return os.cpu_count() or 1\\\\n\\\\n\\\\ndef _container_ram_gb() -> float:\\\\n    for p in [\\\\\\\"/sys/fs/cgroup/memory.max\\\\\\\", \\\\\\\"/sys/fs/cgroup/memory/memory.limit_in_bytes\\\\\\\"]:\\\\n        try:\\\\n            v = Path(p).read_text().strip()\\\\n            if v != \\\\\\\"max\\\\\\\" and int(v) < 1_000_000_000_000:\\\\n                return int(v) / 1e9\\\\n        except (FileNotFoundError, ValueError):\\\\n            pass\\\\n    return psutil.virtual_memory().total / 1e9\\\\n\\\\n\\\\nNUM_CPUS = _detect_cpus()\\\\nTOTAL_RAM_GB = _container_ram_gb()\\\\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\\\\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\\\\nlogger.info(f\\\\\\\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\\\\\\\")\\\\n\\\\nimport torch  # noqa: E402  (import after thread-count env vars are set)\\\\n\\\\ntorch.set_num_threads(max(1, NUM_CPUS))\\\\nfrom transformers import (  # noqa: E402\\\\n    DistilBertForSequenceClassification,\\\\n    DistilBertTokenizerFast,\\\\n    Trainer,\\\\n    TrainingArguments,\\\\n)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"e5f425bc\",\n   \"source\": \"## Load the demo data\\\\n\\\\nThe original script calls `datasets.load_dataset(...)` to pull the full Rotten Tomatoes / SST-2 / IMDB corpora. For this demo we bundle a small, already-downloaded, curated subset of Rotten Tomatoes (`mini_demo_data.json`, ~100 examples split into a labeled pool, an unlabeled pool, and a held-out test set) so the notebook doesn't need to fetch and process full datasets. It's loaded from GitHub with a local-file fallback so the notebook works both standalone and on Colab.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"b1554b31\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport json, os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"173915af\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"domains in demo data:\\\\\\\", list(data.keys()))\\\\nfor dom, d in data.items():\\\\n    print(f\\\\\\\"  {dom}: labeled={len(d['labeled_texts'])} unlabeled={len(d['unlabeled_pool'])} test={len(d['test_texts'])}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"2e0c395d\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from `method.py`, gathered in one place. Values here are set to the **minimum** that still produces a meaningful curve (few `n` values, 1 seed, 1 fine-tuning epoch, small bootstrap count) so the whole notebook finishes in a couple of minutes on CPU. The commented-out values are the **original full-scale** settings (`NS_FULL`, `SEEDS_FULL`, etc.) -- restore them (and use the full dataset instead of the mini demo one) for a full reproduction.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"c0fb31d5\",\n   \"source\": \"# --------------------------------------------------------------- DEMO config (minimal, fast)\\\\nSEEDS_FULL = [0]                 # original: [0, 1]\\\\nNS_FULL = [20, 50]               # original: [50, 200, 500, 1000] (bounded by our 60-example labeled pool)\\\\nDOMAINS_ORDER = [\\\\\\\"rotten_tomatoes\\\\\\\"]  # original: [\\\\\\\"rotten_tomatoes\\\\\\\", \\\\\\\"sst2\\\\\\\", \\\\\\\"imdb\\\\\\\"]\\\\nPILOT_NS = [20]                  # original: [100, 200, 400]\\\\nVOCAB_METHODS = [\\\\\\\"mi\\\\\\\"]           # original: [\\\\\\\"mi\\\\\\\", \\\\\\\"freq\\\\\\\"]\\\\nTEST_N = 20                      # original: 800 (fixed held-out size per domain)\\\\nUNLABELED_POOL_N = 20            # original: 6000\\\\nLABELED_POOL_CAP = 60            # original: 4000\\\\nMAX_LEN = 64                     # unchanged\\\\nN_BOOTSTRAP = 5                  # original: 15 (bootstrap resamples per coverage-curve point)\\\\nTIME_BUDGET_S = 8 * 60.0         # original: 35 * 60.0 (wall-clock budget for the DistilBERT sweep)\\\\n\\\\n_EPOCH_TIERS = {20: 1, 50: 1, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}  # original: {50: 5, 200: 4, 500: 3, 1000: 3, 1500: 2, 2000: 2}\\\\n\\\\nPART_A_START = time.time()\\\\nCHECKPOINT_PATH = WORKDIR / \\\\\\\"results\\\\\\\" / \\\\\\\"part_a_checkpoint.json\\\\\\\"\\\\ndegradation_log: list[str] = []\\\\n\\\\n\\\\ndef ci95(vals) -> float:\\\\n    vals = np.asarray(vals, dtype=float)\\\\n    vals = vals[~np.isnan(vals)]\\\\n    if len(vals) < 2:\\\\n        return 0.0\\\\n    return 1.96 * vals.std(ddof=1) / math.sqrt(len(vals))\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12.0\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [54] ASSISTANT · 2026-09-05 21:26:49 UTC

```
Now the domain-loading adaptation cell, replacing `load_domains()`'s HF download with the mini JSON data.
```

### [55] TOOL CALL — NotebookEdit · 2026-09-05 21:26:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'c0fb31d5', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Data loading and sampling helpers\\n\\n`_balanced_sample` and `stratified_sample` are copied unchanged from `method.py`. `load_domains` is adapted: instead of calling `datasets.load_dataset(...)` for each domain, it builds the same `domains` dict structure directly from the pre-split `data` we just loaded (which already has `labeled_texts`/`labeled_labels`, `unlabeled_pool`, `test_texts`/`test_labels` per domain, so the test/labeled/unlabeled splitting logic from the original `build()` closure is not needed here -- that split was done once when the mini demo file was curated)."'}
```

### [56] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:49 UTC

```
{"new_source": "## Data loading and sampling helpers\\n\\n`_balanced_sample` and `stratified_sample` are copied unchanged from `method.py`. `load_domains` is adapted: instead of calling `datasets.load_dataset(...)` for each domain, it builds the same `domains` dict structure directly from the pre-split `data` we just loaded (which already has `labeled_texts`/`labeled_labels`, `unlabeled_pool`, `test_texts`/`test_labels` per domain, so the test/labeled/unlabeled splitti... [truncated, 22518 chars total]
```

### [57] TOOL CALL — NotebookEdit · 2026-09-05 21:26:55 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '65e6fa89', 'cell_type': 'markdown', 'new_source': '## Data loading and sampling helpers\\n\\n`_balanced_sample` and `stratified_sample` are copied unchanged from `method.py`. `load_domains` is adapted: instead of calling `datasets.load_dataset(...)` for each domain, it builds the same `domains` dict structure directly from the pre-split `data` we just loaded (which already has `labeled_texts`/`labeled_labels`, `unlabeled_pool`, `test_texts`/`test_labels` per domain, so the test/labeled/unlabeled splitting logic from the original `build()` closure is not needed here -- that split was done once when the mini demo file was curated).'}
```

### [58] TOOL RESULT — NotebookEdit · 2026-09-05 21:26:55 UTC

```
{"new_source": "## Data loading and sampling helpers\\n\\n`_balanced_sample` and `stratified_sample` are copied unchanged from `method.py`. `load_domains` is adapted: instead of calling `datasets.load_dataset(...)` for each domain, it builds the same `domains` dict structure directly from the pre-split `data` we just loaded (which already has `labeled_texts`/`labeled_labels`, `unlabeled_pool`, `test_texts`/`test_labels` per domain, so the test/labeled/unlabeled splitti... [truncated, 23826 chars total]
```

### [59] TOOL CALL — NotebookEdit · 2026-09-05 21:27:05 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '65e6fa89', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# ------------------------------------------------------------------ data loading (unchanged from method.py)\\ndef _balanced_sample(texts, labels, n, seed, exclude_idx=None):\\n    rng = np.random.default_rng(seed)\\n    labels = np.asarray(labels)\\n    idx_all = np.arange(len(texts))\\n    if exclude_idx is not None:\\n        mask = np.ones(len(texts), dtype=bool)\\n        mask[list(exclude_idx)] = False\\n        idx_all = idx_all[mask]\\n    classes = np.unique(labels[idx_all])\\n    per_class = n // len(classes)\\n    chosen = []\\n    for c in classes:\\n        pool = idx_all[labels[idx_all] == c]\\n        rng.shuffle(pool)\\n        take = min(per_class, len(pool))\\n        chosen.extend(pool[:take].tolist())\\n    rng.shuffle(chosen)\\n    chosen = chosen[:n]\\n    return chosen\\n\\n\\n# ------------------------------------------------------------------ load_domains: adapted to read from `data` (the mini demo JSON) instead of datasets.load_dataset(...)\\ndef load_domains() -> dict:\\n    domains = {}\\n    for name in DOMAINS_ORDER:\\n        if name not in data:\\n            logger.warning(f\\"domain {name} not present in demo data; skipping\\")\\n            continue\\n        d = data[name]\\n        labeled_texts = d[\\"labeled_texts\\"][:LABELED_POOL_CAP]\\n        labeled_labels = d[\\"labeled_labels\\"][:LABELED_POOL_CAP]\\n        unlabeled_pool = d[\\"unlabeled_pool\\"][:UNLABELED_POOL_N]\\n        test_texts = d[\\"test_texts\\"][:TEST_N]\\n        test_labels = d[\\"test_labels\\"][:TEST_N]\\n        n_pos = sum(test_labels)\\n        logger.info(\\n            f\\"domain={name} labeled_pool={len(labeled_texts)} unlabeled_pool={len(unlabeled_pool)} \\"\\n            f\\"test={len(test_texts)} (pos={n_pos}/{len(test_labels)})\\"\\n        )\\n        assert len(set(test_labels)) >= 2, f\\"{name}: test split missing a class\\"\\n        domains[name] = dict(\\n            labeled_pool=(labeled_texts, labeled_labels),\\n            unlabeled_pool=unlabeled_pool,\\n            test_texts=test_texts,\\n            test_labels=test_labels,\\n        )\\n    return domains\\n\\n\\ndef stratified_sample(texts, labels, n, seed):\\n    idx = _balanced_sample(texts, labels, n, seed)\\n    return [texts[i] for i in idx], [labels[i] for i in idx]'}
```

### [60] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:05 UTC

```
{"new_source": "# ------------------------------------------------------------------ data loading (unchanged from method.py)\\ndef _balanced_sample(texts, labels, n, seed, exclude_idx=None):\\n    rng = np.random.default_rng(seed)\\n    labels = np.asarray(labels)\\n    idx_all = np.arange(len(texts))\\n    if exclude_idx is not None:\\n        mask = np.ones(len(texts), dtype=bool)\\n        mask[list(exclude_idx)] = False\\n        idx_all = idx_all[mask]\\n    class... [truncated, 27596 chars total]
```

### [61] ASSISTANT · 2026-09-05 21:27:11 UTC

```
Now Part A classifier functions.
```

### [62] TOOL CALL — NotebookEdit · 2026-09-05 21:27:11 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '48bdfdbf', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Part A: the two classifiers\\n\\n`train_tfidf_lr` fits TF-IDF (unigrams+bigrams) + logistic regression and returns test accuracy. `finetune_distilbert` fine-tunes `distilbert-base-uncased` for a small number of epochs (looked up from `_EPOCH_TIERS` by training-set size `n`) using HuggingFace\'s `Trainer`, then evaluates test accuracy. Both are copied unchanged from `method.py`."'}
```

### [63] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:11 UTC

```
{"new_source": "## Part A: the two classifiers\\n\\n`train_tfidf_lr` fits TF-IDF (unigrams+bigrams) + logistic regression and returns test accuracy. `finetune_distilbert` fine-tunes `distilbert-base-uncased` for a small number of epochs (looked up from `_EPOCH_TIERS` by training-set size `n`) using HuggingFace's `Trainer`, then evaluates test accuracy. Both are copied unchanged from `method.py`.\"", "cell_type": "markdown", "language": "python", "edit_mode": "insert", ... [truncated, 28824 chars total]
```

### [64] TOOL CALL — NotebookEdit · 2026-09-05 21:27:15 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'eab14870', 'cell_type': 'markdown', 'new_source': "## Part A: the two classifiers\\n\\n`train_tfidf_lr` fits TF-IDF (unigrams+bigrams) + logistic regression and returns test accuracy. `finetune_distilbert` fine-tunes `distilbert-base-uncased` for a small number of epochs (looked up from `_EPOCH_TIERS` by training-set size `n`) using HuggingFace's `Trainer`, then evaluates test accuracy. Both are copied unchanged from `method.py`."}
```

### [65] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:15 UTC

```
{"new_source": "## Part A: the two classifiers\\n\\n`train_tfidf_lr` fits TF-IDF (unigrams+bigrams) + logistic regression and returns test accuracy. `finetune_distilbert` fine-tunes `distilbert-base-uncased` for a small number of epochs (looked up from `_EPOCH_TIERS` by training-set size `n`) using HuggingFace's `Trainer`, then evaluates test accuracy. Both are copied unchanged from `method.py`.", "old_source": "## Part A: the two classifiers\\n\\n`train_tfidf_lr` fits... [truncated, 29724 chars total]
```

### [66] TOOL CALL — NotebookEdit · 2026-09-05 21:27:29 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'eab14870', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# ------------------------------------------------------------------ Part A: classifiers (unchanged from method.py)\\ndef train_tfidf_lr(train_texts, train_labels, test_texts, test_labels, seed):\\n    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)\\n    Xtr = vec.fit_transform(train_texts)\\n    Xte = vec.transform(test_texts)\\n    clf = LogisticRegression(max_iter=2000, C=1.0, random_state=seed, class_weight=\\"balanced\\")\\n    clf.fit(Xtr, train_labels)\\n    return float(clf.score(Xte, test_labels))\\n\\n\\nclass SimpleTorchDataset(torch.utils.data.Dataset):\\n    def __init__(self, encodings, labels):\\n        self.encodings = encodings\\n        self.labels = labels\\n\\n    def __len__(self):\\n        return len(self.labels)\\n\\n    def __getitem__(self, idx):\\n        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}\\n        item[\\"labels\\"] = torch.tensor(self.labels[idx])\\n        return item\\n\\n\\n_TOKENIZER = None\\n\\n\\ndef finetune_distilbert(train_texts, train_labels, test_texts, test_labels, seed, n):\\n    global _TOKENIZER\\n    torch.manual_seed(seed)\\n    random.seed(seed)\\n    np.random.seed(seed)\\n    if _TOKENIZER is None:\\n        _TOKENIZER = DistilBertTokenizerFast.from_pretrained(\\"distilbert-base-uncased\\")\\n    tok = _TOKENIZER\\n    model = DistilBertForSequenceClassification.from_pretrained(\\"distilbert-base-uncased\\", num_labels=2)\\n\\n    train_enc = tok(train_texts, truncation=True, padding=True, max_length=MAX_LEN)\\n    test_enc = tok(test_texts, truncation=True, padding=True, max_length=MAX_LEN)\\n    train_ds = SimpleTorchDataset(train_enc, train_labels)\\n    test_ds = SimpleTorchDataset(test_enc, test_labels)\\n\\n    epochs = _EPOCH_TIERS.get(n, 2)\\n    out_dir = WORKDIR / \\"hf_runs\\" / f\\"db_{seed}_{n}_{int(time.time()*1000)}\\"\\n    args = TrainingArguments(\\n        output_dir=str(out_dir),\\n        num_train_epochs=epochs,\\n        per_device_train_batch_size=16,\\n        per_device_eval_batch_size=64,\\n        learning_rate=5e-5,\\n        weight_decay=0.01,\\n        logging_steps=200,\\n        use_cpu=True,\\n        seed=seed,\\n        report_to=[],\\n        save_strategy=\\"no\\",\\n        eval_strategy=\\"no\\",\\n        disable_tqdm=True,\\n    )\\n    trainer = Trainer(model=model, args=args, train_dataset=train_ds)\\n    t0 = time.time()\\n    trainer.train()\\n    train_secs = time.time() - t0\\n    preds = trainer.predict(test_ds).predictions.argmax(-1)\\n    acc = float((preds == np.array(test_labels)).mean())\\n\\n    del model, trainer, train_enc, test_enc, train_ds, test_ds\\n    gc.collect()\\n    import shutil\\n\\n    shutil.rmtree(out_dir, ignore_errors=True)\\n    return acc, train_secs\\n\\n\\ndef empirical_crossover(curve_domain: pd.DataFrame):\\n    \\"\\"\\"Smallest n where mean_db - mean_tfidf flips sign from <=0 to >0 (linear interp).\\"\\"\\"\\n    cd = curve_domain.sort_values(\\"n\\").reset_index(drop=True)\\n    gaps = cd[\\"gap\\"].values\\n    ns = cd[\\"n\\"].values\\n    if len(ns) == 0:\\n        return None, \\"no_data\\"\\n    if (gaps > 0).all():\\n        return None, \\"distilbert_ahead_at_all_tested_n\\"\\n    if (gaps <= 0).all():\\n        return None, \\"distilbert_never_ahead_in_tested_range\\"\\n    for i in range(1, len(ns)):\\n        if gaps[i - 1] <= 0 and gaps[i] > 0:\\n            if gaps[i] == gaps[i - 1]:\\n                n_star = float(ns[i])\\n            else:\\n                frac = (0 - gaps[i - 1]) / (gaps[i] - gaps[i - 1])\\n                n_star = float(ns[i - 1] + frac * (ns[i] - ns[i - 1]))\\n            return n_star, \\"interpolated\\"\\n    return None, \\"no_clean_crossing\\"'}
```

### [67] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:29 UTC

```
{"new_source": "# ------------------------------------------------------------------ Part A: classifiers (unchanged from method.py)\\ndef train_tfidf_lr(train_texts, train_labels, test_texts, test_labels, seed):\\n    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)\\n    Xtr = vec.fit_transform(train_texts)\\n    Xte = vec.transform(test_texts)\\n    clf = LogisticRegression(max_iter=2000, C=1.0, random_state=seed, class_weight=\\\"balanced\\\")\... [truncated, 36982 chars total]
```

### [68] ASSISTANT · 2026-09-05 21:27:37 UTC

```
Now Part B coverage-curve functions.
```

### [69] TOOL CALL — NotebookEdit · 2026-09-05 21:27:37 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '89400bb9', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Part B: label-free coverage curves\\n\\nThe label-free predictor: pick a small \\"pilot\\" labeled sample, extract the most discriminative n-grams (by mutual information or raw frequency), then measure on growing unlabeled samples how much of that vocabulary\'s probability mass is *still unseen* (Good-Turing) and how species-rich it is (Chao1). All copied unchanged from `method.py`."'}
```

### [70] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:37 UTC

```
{"new_source": "## Part B: label-free coverage curves\\n\\nThe label-free predictor: pick a small \\\"pilot\\\" labeled sample, extract the most discriminative n-grams (by mutual information or raw frequency), then measure on growing unlabeled samples how much of that vocabulary's probability mass is *still unseen* (Good-Turing) and how species-rich it is (Chao1). All copied unchanged from `method.py`.\"", "cell_type": "markdown", "language": "python", "edit_mode": "in... [truncated, 38394 chars total]
```

### [71] TOOL CALL — NotebookEdit · 2026-09-05 21:27:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '6785b503', 'cell_type': 'markdown', 'new_source': '## Part B: label-free coverage curves\\n\\nThe label-free predictor: pick a small \\"pilot\\" labeled sample, extract the most discriminative n-grams (by mutual information or raw frequency), then measure on growing unlabeled samples how much of that vocabulary\'s probability mass is *still unseen* (Good-Turing) and how species-rich it is (Chao1). All copied unchanged from `method.py`.'}
```

### [72] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:41 UTC

```
{"new_source": "## Part B: label-free coverage curves\\n\\nThe label-free predictor: pick a small \\\"pilot\\\" labeled sample, extract the most discriminative n-grams (by mutual information or raw frequency), then measure on growing unlabeled samples how much of that vocabulary's probability mass is *still unseen* (Good-Turing) and how species-rich it is (Chao1). All copied unchanged from `method.py`.", "old_source": "## Part B: label-free coverage curves\\n\\nThe lab... [truncated, 39316 chars total]
```

### [73] TOOL CALL — NotebookEdit · 2026-09-05 21:27:59 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '6785b503', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# ------------------------------------------------------------------ Part B: coverage (unchanged from method.py, except n_bootstrap now reads N_BOOTSTRAP)\\ndef discriminative_ngrams(pilot_texts, pilot_labels, method=\\"mi\\", top_k=2000):\\n    cv = CountVectorizer(ngram_range=(1, 2), min_df=2, binary=True)\\n    X = cv.fit_transform(pilot_texts)\\n    if X.shape[1] == 0:\\n        cv = CountVectorizer(ngram_range=(1, 1), min_df=1, binary=True)\\n        X = cv.fit_transform(pilot_texts)\\n    if method == \\"mi\\":\\n        scores = mutual_info_classif(X, pilot_labels, discrete_features=True, random_state=0)\\n    else:\\n        scores = np.asarray(X.sum(axis=0)).ravel()\\n    vocab = np.array(cv.get_feature_names_out())\\n    top_idx = np.argsort(scores)[::-1][: min(top_k, len(vocab))]\\n    return set(vocab[top_idx].tolist())\\n\\n\\ndef _count_ngram_occurrences(docs, target_ngram_set, ngram_range=(1, 2)):\\n    cv = CountVectorizer(ngram_range=ngram_range, vocabulary=sorted(target_ngram_set))\\n    X = cv.transform(docs)\\n    totals = np.asarray(X.sum(axis=0)).ravel()\\n    vocab = cv.get_feature_names_out()\\n    return dict(zip(vocab, totals.tolist()))\\n\\n\\ndef good_turing_unseen_mass(subsample_docs, target_ngram_set, ngram_range=(1, 2)):\\n    counts = _count_ngram_occurrences(subsample_docs, target_ngram_set, ngram_range)\\n    N = sum(counts.values())\\n    f1 = sum(1 for c in counts.values() if c == 1)\\n    p0_hat = f1 / N if N > 0 else 1.0\\n    seen_frac = (len([g for g, c in counts.items() if c > 0]) / len(target_ngram_set)) if target_ngram_set else 0.0\\n    return p0_hat, seen_frac\\n\\n\\ndef chao1_richness(subsample_docs, target_ngram_set, ngram_range=(1, 2)):\\n    counts = _count_ngram_occurrences(subsample_docs, target_ngram_set, ngram_range)\\n    f1 = sum(1 for c in counts.values() if c == 1)\\n    f2 = sum(1 for c in counts.values() if c == 2)\\n    s_obs = sum(1 for c in counts.values() if c > 0)\\n    s_chao1 = s_obs + (f1**2) / (2 * max(f2, 1))\\n    return float(s_chao1), int(s_obs)\\n\\n\\ndef coverage_curve(domain_data, pilot_n, method, n_points, n_bootstrap=N_BOOTSTRAP):\\n    labeled_texts, labeled_labels = domain_data[\\"labeled_pool\\"]\\n    pilot_texts, pilot_labels = stratified_sample(labeled_texts, labeled_labels, min(pilot_n, len(labeled_texts)), seed=0)\\n    disc_vocab = discriminative_ngrams(pilot_texts, pilot_labels, method=method)\\n    unlabeled_pool = domain_data[\\"unlabeled_pool\\"]\\n    rows = []\\n    for n in n_points:\\n        if n > len(unlabeled_pool):\\n            n_eff = len(unlabeled_pool)\\n        else:\\n            n_eff = n\\n        boot_vals = []\\n        for b in range(n_bootstrap):\\n            rng = np.random.default_rng(b)\\n            sub_idx = rng.choice(len(unlabeled_pool), size=n_eff, replace=(n_eff > len(unlabeled_pool)))\\n            sub = [unlabeled_pool[i] for i in sub_idx]\\n            _, seen_frac = good_turing_unseen_mass(sub, disc_vocab)\\n            boot_vals.append(1 - seen_frac)\\n        rows.append(dict(n=n, unseen_mean=float(np.mean(boot_vals)), unseen_ci=float(ci95(boot_vals))))\\n    return pd.DataFrame(rows), disc_vocab\\n\\n\\ndef interp_crossing(ns, unseen_means, tau):\\n    \\"\\"\\"First n where unseen_mean <= tau (linear interp); None if tau outside observed range.\\"\\"\\"\\n    ns = np.asarray(ns, dtype=float)\\n    um = np.asarray(unseen_means, dtype=float)\\n    order = np.argsort(ns)\\n    ns, um = ns[order], um[order]\\n    if tau > um[0] or tau < um[-1] - 1e-9:\\n        if tau > um[0]:\\n            return None  # tau above the curve\'s starting unseen-mass: undefined (edge artifact)\\n    for i in range(len(ns)):\\n        if um[i] <= tau:\\n            if i == 0:\\n                return float(ns[0])\\n            n0, n1 = ns[i - 1], ns[i]\\n            u0, u1 = um[i - 1], um[i]\\n            if u0 == u1:\\n                return float(n1)\\n            frac = (u0 - tau) / (u0 - u1)\\n            return float(n0 + frac * (n1 - n0))\\n    return None  # tau never reached within observed range\\n\\n\\ndef calibrate_and_predict(cov_curve_A, true_nstar_A, cov_curve_B):\\n    tau = float(np.interp(true_nstar_A, cov_curve_A[\\"n\\"], cov_curve_A[\\"unseen_mean\\"]))\\n    n_hat_B = interp_crossing(cov_curve_B[\\"n\\"].values, cov_curve_B[\\"unseen_mean\\"].values, tau)\\n    return n_hat_B, tau\\n\\n\\ndef compute_overall_verdict(predictions, correlations):\\n    valid_preds = [p for p in predictions if p[\\"within_2x\\"] is not None]\\n    if not valid_preds:\\n        return \\"DISCONFIRMED\\"\\n    hit_rate = sum(1 for p in valid_preds if p[\\"within_2x\\"]) / len(valid_preds)\\n    sig_corrs = [c for c in correlations.values() if c[\\"pval\\"] is not None and c[\\"pval\\"] < 0.10 and c[\\"rho\\"] < 0]\\n    if hit_rate >= 0.5 and len(sig_corrs) >= max(1, len(correlations) // 2):\\n        return \\"SUPPORTED\\"\\n    if hit_rate > 0 or len(sig_corrs) > 0:\\n        return \\"PARTIAL\\"\\n    return \\"DISCONFIRMED\\"'}
```

### [74] TOOL RESULT — NotebookEdit · 2026-09-05 21:27:59 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [75] ASSISTANT · 2026-09-05 21:28:07 UTC

```
Now load domains and run the sweep (Part A execution, adapted from `main()`).
```

### [76] TOOL CALL — NotebookEdit · 2026-09-05 21:28:07 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'c3aad641', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Run: load domains, then the Part A sweep\\n\\nThis mirrors the top of `main()` in `method.py`: load the domains, run a quick smoke test (1 epoch DistilBERT fine-tune + a coverage-curve monotonicity check), then run the full `(domain, n, seed)` sweep with checkpointing (so a crash never loses completed runs) and a wall-clock guard that skips remaining combos if the time budget is exceeded."'}
```

### [77] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:07 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [78] TOOL CALL — NotebookEdit · 2026-09-05 21:28:11 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'df095f60', 'cell_type': 'markdown', 'new_source': '## Run: load domains, then the Part A sweep\\n\\nThis mirrors the top of `main()` in `method.py`: load the domains, run a quick smoke test (1 epoch DistilBERT fine-tune + a coverage-curve monotonicity check), then run the full `(domain, n, seed)` sweep with checkpointing (so a crash never loses completed runs) and a wall-clock guard that skips remaining combos if the time budget is exceeded.'}
```

### [79] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:11 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [80] TOOL CALL — NotebookEdit · 2026-09-05 21:28:23 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'df095f60', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': 'logger.info(\\"=\\" * 70)\\nlogger.info(\\"Loading domains\\")\\ndomains = load_domains()\\ndomain_names = [d for d in DOMAINS_ORDER if d in domains]\\nlogger.info(f\\"Domains loaded: {domain_names}\\")\\n\\n# -------- smoke test (1 seed, epochs=1) on first domain --------\\nsmoke_domain = domains[domain_names[0]]\\nsmoke_n = NS_FULL[0]\\ntr_t, tr_l = stratified_sample(*smoke_domain[\\"labeled_pool\\"], smoke_n, seed=0)\\nacc_lr_smoke = train_tfidf_lr(tr_t, tr_l, smoke_domain[\\"test_texts\\"], smoke_domain[\\"test_labels\\"], seed=0)\\nassert 0.0 <= acc_lr_smoke <= 1.0\\nt0 = time.time()\\nacc_db_smoke, secs_smoke = finetune_distilbert(\\n    tr_t, tr_l, smoke_domain[\\"test_texts\\"], smoke_domain[\\"test_labels\\"], seed=0, n=smoke_n\\n)\\nassert 0.0 <= acc_db_smoke <= 1.0\\nper_epoch_secs = secs_smoke  # 1 epoch at n=smoke_n\\nlogger.info(f\\"SMOKE OK: acc_tfidf={acc_lr_smoke:.3f} acc_db={acc_db_smoke:.3f} 1-epoch-n{smoke_n}-secs={secs_smoke:.1f}\\")\\n\\n# coverage-curve smoke check: seen_frac should rise monotonically-ish with n\\npilot_t, pilot_l = stratified_sample(*smoke_domain[\\"labeled_pool\\"], min(PILOT_NS[0], len(smoke_domain[\\"labeled_pool\\"][0])), seed=0)\\nvocab_smoke = discriminative_ngrams(pilot_t, pilot_l, method=\\"mi\\")\\nseen_fracs = []\\nfor n_chk in NS_FULL:\\n    n_eff = min(n_chk, len(smoke_domain[\\"unlabeled_pool\\"]))\\n    sub = smoke_domain[\\"unlabeled_pool\\"][:n_eff]\\n    p0, sf = good_turing_unseen_mass(sub, vocab_smoke)\\n    assert 0.0 <= p0 <= 1.0 and 0.0 <= sf <= 1.0\\n    seen_fracs.append(sf)\\nlogger.info(f\\"SMOKE coverage seen_fracs at n={NS_FULL}: {seen_fracs}\\")\\nif not all(seen_fracs[i] <= seen_fracs[i + 1] + 1e-6 for i in range(len(seen_fracs) - 1)):\\n    degradation_log.append(f\\"coverage-curve smoke check non-monotonic: {seen_fracs}\\")\\n    logger.warning(f\\"seen_frac not monotonic: {seen_fracs}\\")\\n\\n# -------- timing-based budget projection --------\\ndef est_run_secs(n):\\n    epochs = _EPOCH_TIERS.get(n, 2)\\n    return per_epoch_secs * epochs * max(1.0, n / smoke_n) * 0.6  # 0.6 damping: larger batches amortize overhead\\n\\nseeds, ns = list(SEEDS_FULL), list(NS_FULL)\\ntotal_est = sum(est_run_secs(n) for n in ns for _ in seeds for _ in domain_names)\\nlogger.info(f\\"Projected Part-A DistilBERT total: {total_est/60:.1f} min (budget {TIME_BUDGET_S/60:.0f} min)\\")'}
```

### [81] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:23 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [82] ASSISTANT · 2026-09-05 21:28:41 UTC

```
Now the sweep execution loop cell (checkpointing + curve/crossover computation), and Part B/C/D + assembly, then viz.
```

### [83] TOOL CALL — NotebookEdit · 2026-09-05 21:28:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '3cf9c87b', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# -------- Part A: full sweep with running wall-clock guard + checkpointing --------\\nresults = []\\ndone_combos = set()\\nif CHECKPOINT_PATH.exists():\\n    try:\\n        ckpt = json.loads(CHECKPOINT_PATH.read_text())\\n        results = ckpt.get(\\"results\\", [])\\n        done_combos = {(r[\\"domain\\"], r[\\"n\\"], r[\\"seed\\"]) for r in results}\\n        logger.info(f\\"Resumed checkpoint: {len(results)} runs already completed, skipping them\\")\\n    except (json.JSONDecodeError, KeyError, OSError) as e:\\n        logger.warning(f\\"Could not load checkpoint ({e}); starting fresh\\")\\n\\ndef _save_checkpoint():\\n    CHECKPOINT_PATH.parent.mkdir(exist_ok=True)\\n    CHECKPOINT_PATH.write_text(json.dumps({\\"results\\": results}, default=str))\\n\\npart_a_t0 = time.time()\\nskipped = []\\ncombos = [(d, n, s) for d in domain_names for n in ns for s in seeds]\\nn_done = len(results)\\nfor domain, n, seed in combos:\\n    if (domain, n, seed) in done_combos:\\n        continue\\n    elapsed = time.time() - part_a_t0\\n    remaining = len(combos) - n_done\\n    avg = (elapsed / max(1, n_done - len(done_combos))) if n_done > len(done_combos) else est_run_secs(n)\\n    if elapsed + avg * remaining > TIME_BUDGET_S and n_done > 0:\\n        skipped.append((domain, n, seed))\\n        continue\\n    d = domains[domain]\\n    train_texts, train_labels = stratified_sample(*d[\\"labeled_pool\\"], n, seed)\\n    acc_lr = train_tfidf_lr(train_texts, train_labels, d[\\"test_texts\\"], d[\\"test_labels\\"], seed)\\n    acc_db, secs = finetune_distilbert(train_texts, train_labels, d[\\"test_texts\\"], d[\\"test_labels\\"], seed, n)\\n    results.append(\\n        dict(domain=domain, n=n, seed=seed, acc_tfidf=acc_lr, acc_distilbert=acc_db, db_train_secs=secs)\\n    )\\n    n_done += 1\\n    _save_checkpoint()\\n    logger.info(\\n        f\\"[{n_done}/{len(combos)}] domain={domain} n={n} seed={seed} \\"\\n        f\\"acc_tfidf={acc_lr:.3f} acc_db={acc_db:.3f} secs={secs:.1f} elapsed={elapsed/60:.1f}min\\"\\n    )\\nif skipped:\\n    degradation_log.append(f\\"skipped {len(skipped)} runs mid-sweep due to running time budget: {skipped[:10]}...\\")\\n    logger.warning(f\\"Skipped {len(skipped)} combos due to time budget\\")\\n\\ndf = pd.DataFrame(results)\\nassert len(df) > 0, \\"no Part-A results produced\\"\\n\\ncurve_rows = []\\nfor (domain, n), g in df.groupby([\\"domain\\", \\"n\\"]):\\n    curve_rows.append(\\n        dict(\\n            domain=domain,\\n            n=n,\\n            mean_tfidf=g[\\"acc_tfidf\\"].mean(),\\n            ci_tfidf=ci95(g[\\"acc_tfidf\\"]),\\n            mean_db=g[\\"acc_distilbert\\"].mean(),\\n            ci_db=ci95(g[\\"acc_distilbert\\"]),\\n            n_seeds=len(g),\\n        )\\n    )\\ncurve = pd.DataFrame(curve_rows)\\ncurve[\\"gap\\"] = curve[\\"mean_db\\"] - curve[\\"mean_tfidf\\"]\\n\\ntrue_crossovers = {}\\nfor domain in domain_names:\\n    cd = curve[curve.domain == domain]\\n    if len(cd) < 2:\\n        true_crossovers[domain] = dict(n_star=None, direction=\\"insufficient_n_points\\")\\n        continue\\n    n_star, direction = empirical_crossover(cd)\\n    true_crossovers[domain] = dict(n_star=n_star, direction=direction)\\nlogger.info(f\\"True crossovers: {true_crossovers}\\")\\n\\n# sanity check: TF-IDF accuracy should be non-decreasing (within noise) in n for >=2/3 domains\\nmonotonic_ok = 0\\nfor domain in domain_names:\\n    cd = curve[curve.domain == domain].sort_values(\\"n\\")\\n    diffs = np.diff(cd[\\"mean_tfidf\\"].values)\\n    if (diffs >= -0.05).sum() >= max(1, len(diffs) - 1):\\n        monotonic_ok += 1\\nif monotonic_ok < max(1, math.ceil(len(domain_names) * 2 / 3)):\\n    degradation_log.append(\\n        f\\"TF-IDF accuracy non-monotonic in n for {len(domain_names)-monotonic_ok}/{len(domain_names)} domains \\"\\n        \\"(possible leakage/sampling issue) — reported as-is per fallback plan\\"\\n    )\\n    logger.warning(\\"TF-IDF monotonicity sanity check failed for some domains\\")\\n\\ncurve'}
```

### [84] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [85] ASSISTANT · 2026-09-05 21:28:49 UTC

```
Now Part B/C/D execution and output assembly.
```

### [86] TOOL CALL — NotebookEdit · 2026-09-05 21:28:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': 'bf2151e6', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Run: coverage curves, cross-domain predictions, correlations, verdict\\n\\nThis is the rest of `main()`: compute coverage curves for every `(domain, pilot_n, method)` combo (Part B), calibrate the Good-Turing threshold on one domain and try to predict the crossover on another (Part C -- with a single domain in this demo there are no cross-domain pairs, matching how the original handled a domain with no finite crossover), the pilot-size/vocab-method ablation, the gap-vs-unseen-mass Spearman correlation (Part D), and the overall verdict."'}
```

### [87] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:50 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [88] TOOL CALL — NotebookEdit · 2026-09-05 21:28:53 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '8688a228', 'cell_type': 'markdown', 'new_source': '## Run: coverage curves, cross-domain predictions, correlations, verdict\\n\\nThis is the rest of `main()`: compute coverage curves for every `(domain, pilot_n, method)` combo (Part B), calibrate the Good-Turing threshold on one domain and try to predict the crossover on another (Part C -- with a single domain in this demo there are no cross-domain pairs, matching how the original handled a domain with no finite crossover), the pilot-size/vocab-method ablation, the gap-vs-unseen-mass Spearman correlation (Part D), and the overall verdict.'}
```

### [89] TOOL RESULT — NotebookEdit · 2026-09-05 21:28:53 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [90] TOOL CALL — NotebookEdit · 2026-09-05 21:29:05 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '8688a228', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': '# -------- Part B: coverage curves (label-free) --------\\nlogger.info(\\"Computing coverage curves (Part B)\\")\\ncoverage_curves = {}\\nfor domain in domain_names:\\n    for pilot_n in PILOT_NS:\\n        for method in VOCAB_METHODS:\\n            cov_df, vocab = coverage_curve(domains[domain], pilot_n, method, n_points=ns)\\n            coverage_curves[(domain, pilot_n, method)] = cov_df\\n            logger.debug(f\\"coverage_curve domain={domain} pilot_n={pilot_n} method={method} vocab_size={len(vocab)}\\")\\n\\n# -------- Part C: cross-domain calibrate/predict --------\\nlogger.info(\\"Computing cross-domain predictions (Part C)\\")\\npredictions = []\\nfor A in domain_names:\\n    for B in domain_names:\\n        if A == B:\\n            continue\\n        nstar_A = true_crossovers[A][\\"n_star\\"]\\n        if nstar_A is None:\\n            predictions.append(\\n                dict(calibrate_on=A, predict_on=B, n_hat_star=None, n_true_star=true_crossovers[B][\\"n_star\\"],\\n                     within_2x=None, tau=None, note=f\\"skipped: {A} has no finite empirical crossover\\")\\n            )\\n            continue\\n        cov_A = coverage_curves[(A, PILOT_NS[0], \\"mi\\")]\\n        cov_B = coverage_curves[(B, PILOT_NS[0], \\"mi\\")]\\n        n_hat_B, tau = calibrate_and_predict(cov_A, nstar_A, cov_B)\\n        n_true_B = true_crossovers[B][\\"n_star\\"]\\n        ratio = (n_hat_B / n_true_B) if (n_true_B and n_hat_B) else None\\n        predictions.append(\\n            dict(\\n                calibrate_on=A,\\n                predict_on=B,\\n                n_hat_star=n_hat_B,\\n                n_true_star=n_true_B,\\n                within_2x=(ratio is not None and 0.5 <= ratio <= 2.0),\\n                tau=tau,\\n                note=None,\\n            )\\n        )\\nlogger.info(f\\"Cross-domain predictions: {predictions}\\")\\n\\n# -------- pilot-size / MI-vs-freq ablation summary --------\\nablation_rows = []\\nfor domain in domain_names:\\n    nstar = true_crossovers[domain][\\"n_star\\"]\\n    for pilot_n in PILOT_NS:\\n        for method in VOCAB_METHODS:\\n            cov = coverage_curves[(domain, pilot_n, method)]\\n            if nstar is not None:\\n                tau_self = float(np.interp(nstar, cov[\\"n\\"], cov[\\"unseen_mean\\"]))\\n            else:\\n                tau_self = None\\n            ablation_rows.append(dict(domain=domain, pilot_n=pilot_n, method=method, tau_self=tau_self))\\n\\n# -------- Part D: correlation --------\\nlogger.info(\\"Computing gap-vs-unseen-mass correlations (Part D)\\")\\ncorrelations = {}\\nfor domain in domain_names:\\n    gap_series = curve[curve.domain == domain].sort_values(\\"n\\")[\\"gap\\"].values\\n    cov = coverage_curves[(domain, PILOT_NS[0], \\"mi\\")].sort_values(\\"n\\")\\n    unseen_series = cov[\\"unseen_mean\\"].values\\n    if len(gap_series) >= 3 and len(unseen_series) == len(gap_series):\\n        rho, pval = spearmanr(unseen_series, gap_series)\\n        correlations[domain] = dict(rho=float(rho), pval=float(pval), n_points=len(gap_series))\\n    else:\\n        correlations[domain] = dict(rho=None, pval=None, n_points=len(gap_series))\\nlogger.info(f\\"Correlations: {correlations}\\")\\n\\nverdict = compute_overall_verdict(predictions, correlations)\\nlogger.info(f\\"OVERALL VERDICT: {verdict}\\")'}
```

### [91] TOOL RESULT — NotebookEdit · 2026-09-05 21:29:05 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [92] ASSISTANT · 2026-09-05 21:29:13 UTC

```
Now the final visualization cell.
```

### [93] TOOL CALL — NotebookEdit · 2026-09-05 21:29:13 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '57f01b23', 'cell_type': 'markdown', 'edit_mode': 'insert', 'new_source': '## Results\\n\\nA readable summary table plus a plot of TF-IDF vs DistilBERT accuracy against training-set size `n`, and the coverage curve(s) used by the label-free predictor."'}
```

### [94] TOOL RESULT — NotebookEdit · 2026-09-05 21:29:14 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [95] TOOL CALL — NotebookEdit · 2026-09-05 21:29:15 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '9b9b360f', 'cell_type': 'markdown', 'new_source': '## Results\\n\\nA readable summary table plus a plot of TF-IDF vs DistilBERT accuracy against training-set size `n`, and the coverage curve(s) used by the label-free predictor.'}
```

### [96] TOOL RESULT — NotebookEdit · 2026-09-05 21:29:16 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [97] TOOL CALL — NotebookEdit · 2026-09-05 21:29:25 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/code_demo.ipynb', 'cell_id': '9b9b360f', 'cell_type': 'code', 'edit_mode': 'insert', 'new_source': 'print(f\\"OVERALL VERDICT: {verdict}\\\\n\\")\\n\\nprint(\\"Accuracy curve (mean over seeds, 95% CI):\\")\\nprint(curve.to_string(index=False))\\n\\nprint(\\"\\\\nTrue empirical crossovers (n where DistilBERT overtakes TF-IDF+LR):\\")\\nfor domain, tc in true_crossovers.items():\\n    print(f\\"  {domain}: n_star={tc[\'n_star\']} ({tc[\'direction\']})\\")\\n\\nprint(\\"\\\\nGap-vs-unseen-mass correlations:\\")\\nfor domain, c in correlations.items():\\n    print(f\\"  {domain}: rho={c[\'rho\']} pval={c[\'pval\']} (n_points={c[\'n_points\']})\\")\\n\\nif degradation_log:\\n    print(\\"\\\\nDegradations applied:\\")\\n    for d in degradation_log:\\n        print(f\\"  - {d}\\")\\n\\nfig, axes = plt.subplots(1, 2, figsize=(11, 4))\\n\\nax = axes[0]\\nfor domain in domain_names:\\n    cd = curve[curve.domain == domain].sort_values(\\"n\\")\\n    ax.errorbar(cd[\\"n\\"], cd[\\"mean_tfidf\\"], yerr=cd[\\"ci_tfidf\\"], marker=\\"o\\", label=f\\"{domain} TF-IDF+LR\\")\\n    ax.errorbar(cd[\\"n\\"], cd[\\"mean_db\\"], yerr=cd[\\"ci_db\\"], marker=\\"s\\", label=f\\"{domain} DistilBERT\\")\\nax.set_xlabel(\\"training-set size n\\")\\nax.set_ylabel(\\"test accuracy\\")\\nax.set_title(\\"Accuracy vs n\\")\\nax.legend(fontsize=8)\\nax.grid(alpha=0.3)\\n\\nax = axes[1]\\nfor (domain, pilot_n, method), cov_df in coverage_curves.items():\\n    if pilot_n == PILOT_NS[0] and method == \\"mi\\":\\n        cd = cov_df.sort_values(\\"n\\")\\n        ax.errorbar(cd[\\"n\\"], cd[\\"unseen_mean\\"], yerr=cd[\\"unseen_ci\\"], marker=\\"o\\", label=domain)\\nax.set_xlabel(\\"unlabeled sample size n\\")\\nax.set_ylabel(\\"Good-Turing unseen mass\\")\\nax.set_title(f\\"Coverage curve (pilot_n={PILOT_NS[0]}, method=mi)\\")\\nax.legend(fontsize=8)\\nax.grid(alpha=0.3)\\n\\nplt.tight_layout()\\nplt.show()'}
```

### [98] TOOL RESULT — NotebookEdit · 2026-09-05 21:29:26 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [99] ASSISTANT · 2026-09-05 21:29:29 UTC

```
Now let's test-run the notebook in a clean venv per the skill instructions.
```

### [100] TOOL CALL — Bash · 2026-09-05 21:29:29 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "import json; nb=json.load(open('code_demo.ipynb')); print(len(nb['cells']), 'cells'); [print(i, c['cell_type']) for i,c in enumerate(nb['cells'])]"
```

### [101] TOOL RESULT — Bash · 2026-09-05 21:29:29 UTC

```
{"stdout": "22 cells\n0 markdown\n1 code\n2 markdown\n3 code\n4 markdown\n5 code\n6 code\n7 markdown\n8 code\n9 markdown\n10 code\n11 markdown\n12 code\n13 markdown\n14 code\n15 markdown\n16 code\n17 code\n18 markdown\n19 code\n20 markdown\n21 code", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [102] ASSISTANT · 2026-09-05 21:29:37 UTC

```
Structure looks right. Now run the clean-environment test.
```

### [103] TOOL CALL — Bash · 2026-09-05 21:29:37 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
/usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5 || python3 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -10
echo DONE_SETUP
```

### [104] TOOL RESULT — Bash · 2026-09-05 21:32:34 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bzrf5qssk", "timedOutAfterMs": 180000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [105] ASSISTANT · 2026-09-05 21:32:38 UTC

```
I'll wait for that setup to finish before executing the notebook.
```

### [106] TOOL CALL — Bash · 2026-09-05 21:32:38 UTC

```
tail -20 /tmp/claude-0/-ai-inventor-aii-data-runs-run-2ohq8qwlCPMZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art--VSV4YQ0-oJD/8eadc88f-d2cf-46f4-baf2-0b76d5cf5877/tasks/bzrf5qssk.output
```

### [107] TOOL RESULT — Bash · 2026-09-05 21:32:38 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [108] TOOL CALL — Bash · 2026-09-05 21:32:42 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
ls -la .nb_env/bin/ | head -20
.nb_env/bin/python --version
```

### [109] TOOL RESULT — Bash · 2026-09-05 21:32:42 UTC

```
{"stdout": "total 2969\ndrwxr-xr-x 2 root root 1002109 Sep  5 21:32 .\ndrwxr-xr-x 7 root root 2010975 Sep  5 21:30 ..\n-rw-r--r-- 1 root root    9033 Sep  5 21:29 Activate.ps1\n-rw-r--r-- 1 root root    2382 Sep  5 21:29 activate\n-rw-r--r-- 1 root root    1030 Sep  5 21:29 activate.csh\n-rw-r--r-- 1 root root    2305 Sep  5 21:29 activate.fish\n-rwxr-xr-x 1 root root     377 Sep  5 21:31 debugpy\n-rwxr-xr-x 1 root root     383 Sep  5 21:31 debugpy-adapter\n-rwxr-xr-x 1 root root     367 Sep  5 21:31 idna\n-rwxr-xr-x 1 root root    1886 Sep  5 21:31 jsonpointer\n-rwxr-xr-x 1 root root     373 Sep  5 21:31 mistune\n-rwxr-xr-x 1 root root     393 Sep  5 21:31 normalizer\n-rwxr-xr-x 1 root root     381 Sep  5 21:29 pip\n-rwxr-xr-x 1 root root     381 Sep  5 21:29 pip3\n-rwxr-xr-x 1 root root     381 Sep  5 21:29 pip3.12\n-rwxr-xr-x 1 root root     382 Sep  5 21:32 pybabel\n-rwxr-xr-x 1 root root     375 Sep  5 21:31 pygmentize\n-rwxr-xr-x 1 root root     369 Sep  5 21:31 pyjson5\nlrwxrwxrwx 1 root root      10 Sep  5 21:29 python -> python3.12\nPython 3.12.14", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [110] ASSISTANT · 2026-09-05 21:32:48 UTC

```
Setup finished. Now execute the notebook.
```

### [111] TOOL CALL — Bash · 2026-09-05 21:32:48 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1 &
echo $! > nbrun.pid
sleep 5
echo started
```

### [112] TOOL RESULT — Bash · 2026-09-05 21:32:50 UTC

```
{"stdout": "[1]+  Exit 127                .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1\nstarted", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [113] TOOL CALL — Bash · 2026-09-05 21:32:54 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
cat nbrun.log
which jupyter 2>/dev/null
ls .nb_env/bin | grep -i jupyter
```

### [114] TOOL RESULT — Bash · 2026-09-05 21:32:54 UTC

```
{"stdout": "/bin/bash: line 6: .nb_env/bin/jupyter: No such file or directory\njupyter\njupyter-migrate\njupyter-troubleshoot", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [115] TOOL CALL — Bash · 2026-09-05 21:33:00 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
.nb_env/bin/pip install -q jupyter nbconvert ipykernel 2>&1 | tail -20
ls .nb_env/bin | grep -i jupyter
```

### [116] TOOL RESULT — Bash · 2026-09-05 21:34:56 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkzdeey8q", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [117] TOOL CALL — Bash · 2026-09-05 21:35:00 UTC

```
sleep 60; tail -30 /tmp/claude-0/-ai-inventor-aii-data-runs-run-2ohq8qwlCPMZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art--VSV4YQ0-oJD/8eadc88f-d2cf-46f4-baf2-0b76d5cf5877/tasks/bkzdeey8q.output
```

### [118] TOOL RESULT — Bash [ERROR] · 2026-09-05 21:35:00 UTC

```
Error: Blocked: sleep 60 followed by: tail -30 /tmp/claude-0/-ai-inventor-aii-data-runs-run-2ohq8qwlCPMZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art--VSV4YQ0-oJD/8eadc88f-d2cf-46f4-baf2-0b76d5cf5877/tasks/bkzdeey8q.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [119] TOOL CALL — ToolSearch · 2026-09-05 21:35:02 UTC

```
{'query': 'select:Monitor', 'max_results': 2}
```

### [120] TOOL RESULT — ToolSearch · 2026-09-05 21:35:02 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 18}
```

### [121] TOOL CALL — Monitor · 2026-09-05 21:35:08 UTC

```
{'description': 'wait for pip install of jupyter/nbconvert to finish', 'command': 'until ! kill -0 $(pgrep -f "pip install -q jupyter nbconvert" | head -1) 2>/dev/null; do sleep 3; done; echo PIP_DONE; ls /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/bin | grep -i jupyter', 'timeout_ms': 180000, 'persistent': False}
```

### [122] TOOL RESULT — Monitor · 2026-09-05 21:35:08 UTC

```
{"taskId": "bio1pfhqv", "timeoutMs": 180000, "persistent": false}
```

### [123] ASSISTANT · 2026-09-05 21:35:12 UTC

```
While waiting, let me sanity check the mini_demo_data.json structure once more.
```

### [124] TOOL CALL — Bash · 2026-09-05 21:35:12 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
d = json.load(open('mini_demo_data.json'))
for k,v in d.items():
    print(k, {kk: len(vv) for kk,vv in v.items()})
    print('sample label counts labeled:', sum(v['labeled_labels']), '/', len(v['labeled_labels']))
    print('sample text:', v['labeled_texts'][0][:80])
"
```

### [125] TOOL RESULT — Bash · 2026-09-05 21:35:12 UTC

```
{"stdout": "rotten_tomatoes {'labeled_texts': 60, 'labeled_labels': 60, 'test_texts': 20, 'test_labels': 20, 'unlabeled_pool': 20}\nsample label counts labeled: 30 / 60\nsample text: the woodman seems to have directly influenced this girl-meets-girl love story ,", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [126] ASSISTANT · 2026-09-05 21:35:14 UTC

```
Good, data looks fine. Let's wait for the monitor notification.
```

### [127] TOOL CALL — Bash · 2026-09-05 21:35:14 UTC

```
echo waiting
```

### [128] TOOL RESULT — Bash · 2026-09-05 21:35:14 UTC

```
{"stdout": "waiting", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [129] TOOL CALL — Bash · 2026-09-05 21:35:18 UTC

```
sleep 1; echo ok
```

### [130] TOOL RESULT — Bash · 2026-09-05 21:35:18 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [131] ASSISTANT · 2026-09-05 21:35:26 UTC

```
I've kicked off installing jupyter/nbconvert in the test venv and am monitoring for completion; I'll proceed once that finishes.
```

### [132] TOOL CALL — Bash · 2026-09-05 21:35:26 UTC

```
true
```

### [133] TOOL RESULT — Bash · 2026-09-05 21:35:26 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [134] ASSISTANT · 2026-09-05 21:35:29 UTC

```
I've started installing `jupyter`/`nbconvert` in the isolated test venv and am monitoring it; I'll continue once it completes and then execute the notebook end-to-end.
```

### [135] SYSTEM-USER prompt · 2026-09-05 21:35:30 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [136] TOOL CALL — Bash · 2026-09-05 21:35:36 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
ls .nb_env/bin | grep -i jupyter
echo ---
ls -la code_demo.ipynb mini_demo_data.json 2>&1
```

### [137] TOOL RESULT — Bash · 2026-09-05 21:35:36 UTC

```
{"stdout": "jupyter\njupyter-migrate\njupyter-troubleshoot\n---\n-rw-r--r-- 1 root root 36481 Sep  5 21:29 code_demo.ipynb\n-rw-r--r-- 1 root root 13607 Sep  5 21:24 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [138] TOOL CALL — Bash · 2026-09-05 21:35:40 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
.nb_env/bin/pip install -q nbconvert notebook ipykernel 2>&1 | tail -30
ls .nb_env/bin | grep -i nbconvert
echo DONE
```

### [139] TOOL RESULT — Bash · 2026-09-05 21:35:40 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bgn7dgwsy", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [140] ASSISTANT · 2026-09-05 21:35:42 UTC

```
I'll wait for that install to finish, then execute the notebook.
```

### [141] TOOL CALL — Bash · 2026-09-05 21:35:42 UTC

```
true
```

### [142] TOOL RESULT — Bash · 2026-09-05 21:35:42 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [143] TOOL CALL — Bash · 2026-09-05 21:35:50 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
for i in $(seq 1 30); do
  if [ -x .nb_env/bin/jupyter-nbconvert ] || [ -f .nb_env/bin/jupyter-nbconvert ]; then echo READY; break; fi
  sleep 5
done
ls .nb_env/bin | grep -i nbconvert
tail -20 /tmp/claude-0/-ai-inventor-aii-data-runs-run-2ohq8qwlCPMZ-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art--VSV4YQ0-oJD/8eadc88f-d2cf-46f4-baf2-0b76d5cf5877/tasks/bgn7dgwsy.output
```

### [144] TOOL RESULT — Bash · 2026-09-05 21:36:24 UTC

```
{"stdout": "READY\njupyter-nbconvert", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [145] ASSISTANT · 2026-09-05 21:36:28 UTC

```
Now let's execute the notebook synchronously with a generous timeout.
```

### [146] TOOL CALL — Bash · 2026-09-05 21:36:28 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1
echo "EXIT_CODE=$?"
tail -100 nbrun.log
```

### [147] TOOL RESULT — Bash · 2026-09-05 21:36:48 UTC

```
{"stdout": "EXIT_CODE=1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\nTraceback (most recent call last):\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/bin/jupyter-nbconvert\", line 10, in <module>\n    sys.exit(main())\n             ^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/jupyter_core/application.py\", line 284, in launch_instance\n    super().launch_instance(argv=argv, **kwargs)\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/traitlets/config/application.py\", line 1080, in launch_instance\n    app.start()\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/nbconvertapp.py\", line 420, in start\n    self.convert_notebooks()\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/nbconvertapp.py\", line 597, in convert_notebooks\n    self.convert_single_notebook(notebook_filename)\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/nbconvertapp.py\", line 563, in convert_single_notebook\n    output, resources = self.export_single_notebook(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/nbconvertapp.py\", line 487, in export_single_notebook\n    output, resources = self.exporter.from_filename(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 201, in from_filename\n    return self.from_file(f, resources=resources, **kw)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 220, in from_file\n    return self.from_notebook_node(\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/notebook.py\", line 36, in from_notebook_node\n    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 154, in from_notebook_node\n    nb_copy, resources = self._preprocess(nb_copy, resources)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 353, in _preprocess\n    nbc, resc = preprocessor(nbc, resc)\n                ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/base.py\", line 48, in __call__\n    return self.preprocess(nb, resources)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 103, in preprocess\n    self.preprocess_cell(cell, resources, index)\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 124, in preprocess_cell\n    cell = self.execute_cell(cell, index, store_history=True)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/jupyter_core/utils/__init__.py\", line 165, in wrapped\n    return loop.run_until_complete(inner)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/asyncio/base_events.py\", line 691, in run_until_complete\n    return future.result()\n           ^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 1062, in async_execute_cell\n    await self._check_raise_for_error(cell, cell_index, exec_reply)\n  File \"/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 918, in _check_raise_for_error\n    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)\nnbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:\n------------------\nimport subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n_pip('psutil==7.1.0')\\n\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\n         'torch==2.9.0', 'transformers==5.0.0')\n------------------\n\n\n  \u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[1]\u001b[39m\u001b[32m, line 1\u001b[39m\n\u001b[31m    \u001b[39m\u001b[31mimport subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n_pip('psutil==7.1.0')\\n\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\\n         'torch==2.9.0', 'transformers==5.0.0')\u001b[39m\n                           ^\n\u001b[31mSyntaxError\u001b[39m\u001b[31m:\u001b[39m unexpected character after line continuation character", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [148] TOOL CALL — Bash · 2026-09-05 21:36:56 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
src = nb['cells'][1]['source']
print(type(src))
print(repr(src)[:300])
"
```

### [149] TOOL RESULT — Bash · 2026-09-05 21:36:56 UTC

```
{"stdout": "<class 'str'>\n\"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# loguru, psutil -- NOT pre-installed on Colab, always install\\\\n_pip('loguru==0.7.3')\\\\n_pip('psutil==7.1.0')\\\\n\\\\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [150] TOOL CALL — Bash · 2026-09-05 21:37:46 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
src = nb['cells'][1]['source']
i = src.index('sys')
print([hex(ord(c)) for c in src[i:i+20]])
"
```

### [151] TOOL RESULT — Bash · 2026-09-05 21:37:46 UTC

```
{"stdout": "['0x73', '0x79', '0x73', '0x5c', '0x6e', '0x64', '0x65', '0x66', '0x20', '0x5f', '0x70', '0x69', '0x70', '0x28', '0x2a', '0x61', '0x29', '0x3a', '0x20', '0x73']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [152] TOOL CALL — Bash · 2026-09-05 21:38:00 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
src = nb['cells'][19]['source']
i = src.index('True empirical')
print(repr(src[i-20:i+40]))
"
```

### [153] TOOL RESULT — Bash [ERROR] · 2026-09-05 21:38:00 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "<string>", line 5, in <module>
ValueError: substring not found
```

### [154] TOOL CALL — Bash · 2026-09-05 21:38:04 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code' and 'True empirical' in c['source']:
        print(i)
        idx = c['source'].index('True empirical')
        print(repr(c['source'][idx-20:idx+40]))
"
```

### [155] TOOL RESULT — Bash · 2026-09-05 21:38:04 UTC

```
{"stdout": "21\n'lse))\\\\n\\\\nprint(\\\\\"\\\\\\\\nTrue empirical crossovers (n where Disti'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [156] TOOL CALL — Bash · 2026-09-05 21:38:20 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
c = nb['cells'][21]['source']
idx = c.index('True empirical')
chunk = c[idx-15:idx+20]
for ch in chunk:
    print(hex(ord(ch)), repr(ch))
"
```

### [157] TOOL RESULT — Bash · 2026-09-05 21:38:20 UTC

```
{"stdout": "0x5c '\\\\'\n0x6e 'n'\n0x5c '\\\\'\n0x6e 'n'\n0x70 'p'\n0x72 'r'\n0x69 'i'\n0x6e 'n'\n0x74 't'\n0x28 '('\n0x5c '\\\\'\n0x22 '\"'\n0x5c '\\\\'\n0x5c '\\\\'\n0x6e 'n'\n0x54 'T'\n0x72 'r'\n0x75 'u'\n0x65 'e'\n0x20 ' '\n0x65 'e'\n0x6d 'm'\n0x70 'p'\n0x69 'i'\n0x72 'r'\n0x69 'i'\n0x63 'c'\n0x61 'a'\n0x6c 'l'\n0x20 ' '\n0x63 'c'\n0x72 'r'\n0x6f 'o'\n0x73 's'\n0x73 's'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [158] TOOL CALL — Bash · 2026-09-05 21:38:38 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json, re
nb = json.load(open('code_demo.ipynb'))
allsrc = ''
for c in nb['cells']:
    allsrc += c['source']
from collections import Counter
seqs = re.findall(r'\\\\+.', allsrc)
print(Counter(seqs).most_common(30))
"
```

### [159] TOOL RESULT — Bash · 2026-09-05 21:38:38 UTC

```
{"stdout": "[('\\\\n', 639), ('\\\\\"', 386), ('\\\\\\\\n', 4)]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [160] TOOL CALL — Bash · 2026-09-05 21:38:44 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'PYEOF'
import json

with open('code_demo.ipynb') as f:
    nb = json.load(f)

def fix(s):
    PLACEHOLDER = "\x00NLESC\x00"
    s = s.replace("\\\\n", PLACEHOLDER)   # 3-char backslash-backslash-n -> placeholder (will become \n literal)
    s = s.replace('\\"', '"')             # backslash-quote -> quote
    s = s.replace("\\n", "\n")            # backslash-n -> real newline
    s = s.replace(PLACEHOLDER, "\\n")     # placeholder -> literal backslash+n (2 chars) for in-string escape
    return s

for c in nb['cells']:
    if isinstance(c['source'], str):
        c['source'] = fix(c['source'])

with open('code_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("fixed")
PYEOF
```

### [161] TOOL RESULT — Bash · 2026-09-05 21:38:44 UTC

```
{"stdout": "fixed", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [162] ASSISTANT · 2026-09-05 21:38:48 UTC

```
Now let's verify a couple of cells and try compiling all code cells with Python's `ast` to catch syntax errors before running the full notebook.
```

### [163] TOOL CALL — Bash · 2026-09-05 21:38:48 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json, ast
nb = json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        try:
            ast.parse(c['source'])
        except SyntaxError as e:
            print(i, 'SYNTAX ERROR', e)
print('checked', sum(1 for c in nb['cells'] if c['cell_type']=='code'), 'code cells')
"
```

### [164] TOOL RESULT — Bash · 2026-09-05 21:38:48 UTC

```
{"stdout": "checked 12 code cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [165] ASSISTANT · 2026-09-05 21:38:52 UTC

```
All cells parse cleanly. Now run the full notebook execution test.
```

### [166] TOOL CALL — Bash · 2026-09-05 21:38:52 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1
echo "EXIT_CODE=$?"
tail -120 nbrun.log
```

### [167] SYSTEM-USER prompt · 2026-09-05 21:49:20 UTC

```
continue where you left off — reuse any partial work already written to disk. Do NOT start over.
```

### [168] TOOL CALL — Bash · 2026-09-05 21:49:22 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
ps aux | grep -i jupyter | grep -v grep
echo ---
tail -100 nbrun.log
```

### [169] TOOL RESULT — Bash · 2026-09-05 21:49:22 UTC

```
{"stdout": "root         849  8.4  0.0  84684 73320 ?        S    21:49   0:01 /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/bin/python3.12 .nb_env/bin/jupyter-nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb\n---", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [170] ASSISTANT · 2026-09-05 21:49:30 UTC

```
The install/execution process is still running (PID 849). I'll continue waiting for the monitor notification before proceeding further.
```

### [171] TOOL CALL — Bash · 2026-09-05 21:49:30 UTC

```
sleep 2; echo ok
```

### [172] TOOL RESULT — Bash · 2026-09-05 21:49:30 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [173] ASSISTANT · 2026-09-05 21:49:31 UTC

```
Waiting on the background notebook execution (PID 849) to complete; will proceed once the monitor reports done.
```

### [174] SYSTEM-USER prompt · 2026-09-05 21:49:36 UTC

```
<validation-feedback>
Attempt 2 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [175] TOOL CALL — Bash · 2026-09-05 21:49:36 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
ps aux | grep -i jupyter | grep -v grep
echo ---LOG---
tail -200 nbrun.log
echo ---FILES---
ls -la code_demo.ipynb mini_demo_data.json
```

### [176] TOOL RESULT — Bash · 2026-09-05 21:49:36 UTC

```
{"stdout": "root         849  4.9  0.0 398476 86328 ?        Sl   21:49   0:01 /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/bin/python3.12 .nb_env/bin/jupyter-nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb\n---LOG---\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n---FILES---\n-rw-r--r-- 1 root root 35074 Sep  5 21:38 code_demo.ipynb\n-rw-r--r-- 1 root root 13607 Sep  5 21:24 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [177] TOOL CALL — Bash · 2026-09-05 21:49:48 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
tail --pid=849 -f /dev/null
echo "PROCESS_849_ENDED"
tail -c 4000 nbrun.log
```

### [178] TOOL RESULT — Bash · 2026-09-05 21:59:32 UTC

```
{"stdout": "PROCESS_849_ENDED\ngen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 918, in _check_raise_for_error\n    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)\nnbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:\n------------------\nfrom __future__ import annotations\n\nimport gc\nimport json\nimport math\nimport os\nimport random\nimport resource\nimport sys\nimport time\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nimport psutil\nfrom loguru import logger\nfrom scipy.stats import spearmanr\nfrom sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\nfrom sklearn.feature_selection import mutual_info_classif\nfrom sklearn.linear_model import LogisticRegression\nimport matplotlib.pyplot as plt  # for the results visualization cell at the end\n\nWORKDIR = Path.cwd()\nos.environ.setdefault(\"HF_HOME\", str(WORKDIR / \".hf_cache\"))\nos.environ.setdefault(\"HF_DATASETS_CACHE\", str(WORKDIR / \".hf_cache\" / \"datasets\"))\nos.environ.setdefault(\"TRANSFORMERS_CACHE\", str(WORKDIR / \".hf_cache\" / \"transformers\"))\nos.environ.setdefault(\"TOKENIZERS_PARALLELISM\", \"false\")\nos.environ.setdefault(\"OMP_NUM_THREADS\", \"4\")\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(WORKDIR / \"logs\").mkdir(exist_ok=True)\nlogger.add(WORKDIR / \"logs\" / \"run.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n# ------------------------------------------------------------------ hardware\ndef _detect_cpus() -> int:\n    try:\n        parts = Path(\"/sys/fs/cgroup/cpu.max\").read_text().split()\n        if parts[0] != \"max\":\n            return math.ceil(int(parts[0]) / int(parts[1]))\n    except (FileNotFoundError, ValueError):\n        pass\n    try:\n        return len(os.sched_getaffinity(0))\n    except (AttributeError, OSError):\n        return os.cpu_count() or 1\n\n\ndef _container_ram_gb() -> float:\n    for p in [\"/sys/fs/cgroup/memory.max\", \"/sys/fs/cgroup/memory/memory.limit_in_bytes\"]:\n        try:\n            v = Path(p).read_text().strip()\n            if v != \"max\" and int(v) < 1_000_000_000_000:\n                return int(v) / 1e9\n        except (FileNotFoundError, ValueError):\n            pass\n    return psutil.virtual_memory().total / 1e9\n\n\nNUM_CPUS = _detect_cpus()\nTOTAL_RAM_GB = _container_ram_gb()\nRAM_BUDGET_BYTES = int(min(TOTAL_RAM_GB * 0.6, 16.0) * 1e9)\nresource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_BYTES * 3, RAM_BUDGET_BYTES * 3))\nlogger.info(f\"NUM_CPUS={NUM_CPUS} TOTAL_RAM_GB={TOTAL_RAM_GB:.1f} RAM_BUDGET_GB={RAM_BUDGET_BYTES/1e9:.1f}\")\n\nimport torch  # noqa: E402  (import after thread-count env vars are set)\n\ntorch.set_num_threads(max(1, NUM_CPUS))\nfrom transformers import (  # noqa: E402\n    DistilBertForSequenceClassification,\n    DistilBertTokenizerFast,\n    Trainer,\n    TrainingArguments,\n)\n------------------\n\n\n\u001b[31m---------------------------------------------------------------------------\u001b[39m\n\u001b[31mModuleNotFoundError\u001b[39m                       Traceback (most recent call last)\n\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[2]\u001b[39m\u001b[32m, line 21\u001b[39m\n\u001b[32m     17\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m scipy.stats \u001b[38;5;28;01mimport\u001b[39;00m spearmanr\n\u001b[32m     18\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m sklearn.feature_extraction.text \u001b[38;5;28;01mimport\u001b[39;00m CountVectorizer, TfidfVectorizer\n\u001b[32m     19\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m sklearn.feature_selection \u001b[38;5;28;01mimport\u001b[39;00m mutual_info_classif\n\u001b[32m     20\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m sklearn.linear_model \u001b[38;5;28;01mimport\u001b[39;00m LogisticRegression\n\u001b[32m---> \u001b[39m\u001b[32m21\u001b[39m \u001b[38;5;28;01mimport\u001b[39;00m matplotlib.pyplot \u001b[38;5;28;01mas\u001b[39;00m plt  \u001b[38;5;66;03m# for the results visualization cell at the end\u001b[39;00m\n\u001b[32m     22\u001b[39m \n\u001b[32m     23\u001b[39m WORKDIR = Path.cwd()\n\u001b[32m     24\u001b[39m os.environ.setdefault(\u001b[33m\"HF_HOME\"\u001b[39m, str(WORKDIR / \u001b[33m\".hf_cache\"\u001b[39m))\n\n\u001b[31mModuleNotFoundError\u001b[39m: No module named 'matplotlib'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [179] ASSISTANT · 2026-09-05 21:59:38 UTC

```
Missing matplotlib in install cell. Let's fix and add it to the non-Colab install list, then rerun.
```

### [180] TOOL CALL — Bash · 2026-09-05 21:59:38 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code' and \"_pip('loguru\" in c['source']:
        print(i)
        print(c['source'])
"
```

### [181] TOOL RESULT — Bash · 2026-09-05 21:59:38 UTC

```
{"stdout": "1\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru, psutil -- NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n_pip('psutil==7.1.0')\n\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\n         'torch==2.9.0', 'transformers==5.0.0')", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [182] TOOL CALL — Bash · 2026-09-05 21:59:44 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'PYEOF'
import json
nb = json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='code' and "_pip('loguru" in c['source']:
        c['source'] = c['source'].replace(
            "_pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\n         'torch==2.9.0', 'transformers==5.0.0')",
            "_pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\n         'matplotlib==3.10.0', 'torch==2.9.0', 'transformers==5.0.0')"
        )
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
print("patched")
PYEOF
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
print(nb['cells'][1]['source'])
"
```

### [183] TOOL RESULT — Bash · 2026-09-05 21:59:44 UTC

```
{"stdout": "patched\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru, psutil -- NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n_pip('psutil==7.1.0')\n\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\n         'matplotlib==3.10.0', 'torch==2.9.0', 'transformers==5.0.0')", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [184] ASSISTANT · 2026-09-05 21:59:46 UTC

```
Now rerun the notebook.
```

### [185] TOOL CALL — Bash · 2026-09-05 21:59:46 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
nohup .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun2.log 2>&1 &
disown
echo "PID=$!"
```

### [186] TOOL RESULT — Bash · 2026-09-05 21:59:46 UTC

```
{"stdout": "PID=1077", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [187] TOOL CALL — Bash · 2026-09-05 21:59:50 UTC

```
tail --pid=1077 -f /dev/null
echo "PROCESS_1077_ENDED"
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
tail -c 6000 nbrun2.log
```

### [188] TOOL RESULT — Bash · 2026-09-05 22:03:30 UTC

```
{"stdout": "PROCESS_1077_ENDED\nimpleTorchDataset(test_enc, test_labels)\n\u001b[32m     42\u001b[39m \n\u001b[32m     43\u001b[39m     epochs = _EPOCH_TIERS.get(n, \u001b[32m2\u001b[39m)\n\u001b[32m     44\u001b[39m     out_dir = WORKDIR / \u001b[33m\"hf_runs\"\u001b[39m / f\"db_{seed}_{n}_{int(time.time()*\u001b[32m1000\u001b[39m)}\"\n\u001b[32m---> \u001b[39m\u001b[32m45\u001b[39m     args = TrainingArguments(\n\u001b[32m     46\u001b[39m         output_dir=str(out_dir),\n\u001b[32m     47\u001b[39m         num_train_epochs=epochs,\n\u001b[32m     48\u001b[39m         per_device_train_batch_size=\u001b[32m16\u001b[39m,\n\n\u001b[36mFile \u001b[39m\u001b[32m<string>:112\u001b[39m, in \u001b[36m__create_fn__.<locals>.__init__\u001b[39m\u001b[34m(self, output_dir, do_train, do_eval, do_predict, eval_strategy, prediction_loss_only, per_device_train_batch_size, per_device_eval_batch_size, gradient_accumulation_steps, eval_accumulation_steps, eval_delay, torch_empty_cache_steps, learning_rate, weight_decay, adam_beta1, adam_beta2, adam_epsilon, max_grad_norm, num_train_epochs, max_steps, lr_scheduler_type, lr_scheduler_kwargs, warmup_ratio, warmup_steps, log_level, log_level_replica, log_on_each_node, logging_dir, logging_strategy, logging_first_step, logging_steps, logging_nan_inf_filter, save_strategy, save_steps, save_total_limit, enable_jit_checkpoint, save_on_each_node, save_only_model, restore_callback_states_from_checkpoint, use_cpu, seed, data_seed, bf16, fp16, bf16_full_eval, fp16_full_eval, tf32, local_rank, ddp_backend, debug, dataloader_drop_last, eval_steps, dataloader_num_workers, dataloader_prefetch_factor, run_name, disable_tqdm, remove_unused_columns, label_names, load_best_model_at_end, metric_for_best_model, greater_is_better, ignore_data_skip, fsdp, fsdp_config, accelerator_config, parallelism_config, deepspeed, label_smoothing_factor, optim, optim_args, group_by_length, length_column_name, report_to, project, trackio_space_id, ddp_find_unused_parameters, ddp_bucket_cap_mb, ddp_broadcast_buffers, dataloader_pin_memory, dataloader_persistent_workers, skip_memory_metrics, push_to_hub, resume_from_checkpoint, hub_model_id, hub_strategy, hub_token, hub_private_repo, hub_always_push, hub_revision, gradient_checkpointing, gradient_checkpointing_kwargs, include_for_metrics, eval_do_concat_batches, auto_find_batch_size, full_determinism, ddp_timeout, torch_compile, torch_compile_backend, torch_compile_mode, include_num_input_tokens_seen, neftune_noise_alpha, optim_target_modules, batch_eval_metrics, eval_on_start, use_liger_kernel, liger_kernel_config, eval_use_gather_object, average_tokens_across_devices, use_cache)\u001b[39m\n\n\u001b[36mFile \u001b[39m\u001b[32m/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/transformers/training_args.py:1602\u001b[39m, in \u001b[36mTrainingArguments.__post_init__\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m   1600\u001b[39m \u001b[38;5;66;03m# Initialize device before we proceed\u001b[39;00m\n\u001b[32m   1601\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m is_torch_available():\n\u001b[32m-> \u001b[39m\u001b[32m1602\u001b[39m     \u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mdevice\u001b[39;49m\n\u001b[32m   1604\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m is_torch_available() \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;28mself\u001b[39m.torch_compile:\n\u001b[32m   1605\u001b[39m     \u001b[38;5;28;01mif\u001b[39;00m is_torch_tf32_available():\n\n\u001b[36mFile \u001b[39m\u001b[32m/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/transformers/training_args.py:1857\u001b[39m, in \u001b[36mTrainingArguments.device\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m   1853\u001b[39m \u001b[38;5;250m\u001b[39m\u001b[33;03m\"\"\"\u001b[39;00m\n\u001b[32m   1854\u001b[39m \u001b[33;03mThe device used by this process.\u001b[39;00m\n\u001b[32m   1855\u001b[39m \u001b[33;03m\"\"\"\u001b[39;00m\n\u001b[32m   1856\u001b[39m requires_backends(\u001b[38;5;28mself\u001b[39m, [\u001b[33m\"\u001b[39m\u001b[33mtorch\u001b[39m\u001b[33m\"\u001b[39m])\n\u001b[32m-> \u001b[39m\u001b[32m1857\u001b[39m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43m_setup_devices\u001b[39;49m\n\n\u001b[36mFile \u001b[39m\u001b[32m/usr/local/lib/python3.12/functools.py:998\u001b[39m, in \u001b[36mcached_property.__get__\u001b[39m\u001b[34m(self, instance, owner)\u001b[39m\n\u001b[32m    996\u001b[39m val = cache.get(\u001b[38;5;28mself\u001b[39m.attrname, _NOT_FOUND)\n\u001b[32m    997\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m val \u001b[38;5;129;01mis\u001b[39;00m _NOT_FOUND:\n\u001b[32m--> \u001b[39m\u001b[32m998\u001b[39m     val = \u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mfunc\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43minstance\u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m    999\u001b[39m     \u001b[38;5;28;01mtry\u001b[39;00m:\n\u001b[32m   1000\u001b[39m         cache[\u001b[38;5;28mself\u001b[39m.attrname] = val\n\n\u001b[36mFile \u001b[39m\u001b[32m/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.nb_env/lib/python3.12/site-packages/transformers/training_args.py:1744\u001b[39m, in \u001b[36mTrainingArguments._setup_devices\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m   1742\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m is_sagemaker_mp_enabled():\n\u001b[32m   1743\u001b[39m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m is_accelerate_available():\n\u001b[32m-> \u001b[39m\u001b[32m1744\u001b[39m         \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mImportError\u001b[39;00m(\n\u001b[32m   1745\u001b[39m             \u001b[33mf\u001b[39m\u001b[33m\"\u001b[39m\u001b[33mUsing the `Trainer` with `PyTorch` requires `accelerate>=\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mACCELERATE_MIN_VERSION\u001b[38;5;132;01m}\u001b[39;00m\u001b[33m`: \u001b[39m\u001b[33m\"\u001b[39m\n\u001b[32m   1746\u001b[39m             \u001b[33mf\u001b[39m\u001b[33m\"\u001b[39m\u001b[33mPlease run `pip install transformers[torch]` or `pip install \u001b[39m\u001b[33m'\u001b[39m\u001b[33maccelerate>=\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mACCELERATE_MIN_VERSION\u001b[38;5;132;01m}\u001b[39;00m\u001b[33m'\u001b[39m\u001b[33m`\u001b[39m\u001b[33m\"\u001b[39m\n\u001b[32m   1747\u001b[39m         )\n\u001b[32m   1748\u001b[39m \u001b[38;5;66;03m# We delay the init of `PartialState` to the end for clarity\u001b[39;00m\n\u001b[32m   1749\u001b[39m accelerator_state_kwargs: \u001b[38;5;28mdict\u001b[39m[\u001b[38;5;28mstr\u001b[39m, Any] = {\u001b[33m\"\u001b[39m\u001b[33menabled\u001b[39m\u001b[33m\"\u001b[39m: \u001b[38;5;28;01mTrue\u001b[39;00m, \u001b[33m\"\u001b[39m\u001b[33muse_configured_state\u001b[39m\u001b[33m\"\u001b[39m: \u001b[38;5;28;01mFalse\u001b[39;00m}\n\n\u001b[31mImportError\u001b[39m: Using the `Trainer` with `PyTorch` requires `accelerate>=1.1.0`: Please run `pip install transformers[torch]` or `pip install 'accelerate>=1.1.0'`", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [189] ASSISTANT · 2026-09-05 22:03:36 UTC

```
Need `accelerate`. That's not Colab-preinstalled, so install unconditionally.
```

### [190] TOOL CALL — Bash · 2026-09-05 22:03:36 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'PYEOF'
import json
nb = json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='code' and "_pip('loguru" in c['source']:
        c['source'] = c['source'].replace(
            "_pip('psutil==7.1.0')\n",
            "_pip('psutil==7.1.0')\n_pip('accelerate==1.11.0')\n"
        )
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
PYEOF
python3 -c "import json; print(json.load(open('code_demo.ipynb'))['cells'][1]['source'])"
```

### [191] TOOL RESULT — Bash · 2026-09-05 22:03:36 UTC

```
{"stdout": "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru, psutil -- NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n_pip('psutil==7.1.0')\n_pip('accelerate==1.11.0')\n\n# numpy, scipy, scikit-learn, torch, transformers, pandas -- pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'scipy==1.16.3',\n         'matplotlib==3.10.0', 'torch==2.9.0', 'transformers==5.0.0')", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [192] TOOL CALL — Bash · 2026-09-05 22:03:40 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'PYEOF'
import json
nb = json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='code' and "_pip('loguru" in c['source']:
        c['source'] = c['source'].replace(
            "# loguru, psutil -- NOT pre-installed on Colab, always install",
            "# loguru, psutil, accelerate -- NOT pre-installed on Colab, always install"
        )
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
PYEOF
```

### [193] TOOL RESULT — Bash · 2026-09-05 22:03:40 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [194] ASSISTANT · 2026-09-05 22:03:44 UTC

```
Now rerun the notebook test.
```

### [195] TOOL CALL — Bash · 2026-09-05 22:03:44 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
nohup .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun3.log 2>&1 &
disown
echo "PID=$!"
```

### [196] TOOL RESULT — Bash · 2026-09-05 22:03:46 UTC

```
{"stdout": "PID=1166", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [197] TOOL CALL — Bash · 2026-09-05 22:03:48 UTC

```
tail --pid=1166 -f /dev/null
echo "PROCESS_1166_ENDED"
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
tail -c 6000 nbrun3.log
```

### [198] TOOL RESULT — Bash · 2026-09-05 22:06:58 UTC

```
{"stdout": "PROCESS_1166_ENDED\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 160904 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [199] ASSISTANT · 2026-09-05 22:07:02 UTC

```
It succeeded. Let's inspect the outputs to confirm reasonable results.
```

### [200] TOOL CALL — Bash · 2026-09-05 22:07:02 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        for o in c.get('outputs', []):
            if o.get('output_type')=='error':
                print('CELL', i, 'ERROR', o.get('ename'), o.get('evalue'))
print('no errors found' )
"
echo ---LAST CELL TEXT OUTPUT---
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
c = nb['cells'][-1]
for o in c.get('outputs', []):
    if 'text' in o:
        print(''.join(o['text']))
"
```

### [201] TOOL RESULT — Bash · 2026-09-05 22:07:02 UTC

```
{"stdout": "no errors found\n---LAST CELL TEXT OUTPUT---\nOVERALL VERDICT: DISCONFIRMED\n\nAccuracy curve (mean over seeds, 95% CI):\n         domain  n  mean_tfidf  ci_tfidf  mean_db  ci_db  n_seeds   gap\nrotten_tomatoes 20         0.7       0.0     0.50    0.0        1 -0.20\nrotten_tomatoes 50         0.3       0.0     0.55    0.0        1  0.25\n\nTrue empirical crossovers (n where DistilBERT overtakes TF-IDF+LR):\n  rotten_tomatoes: n_star=33.33333333333333 (interpolated)\n\nGap-vs-unseen-mass correlations:\n  rotten_tomatoes: rho=None pval=None (n_points=2)\n\nDegradations applied:\n  - TF-IDF accuracy non-monotonic in n for 1/1 domains (possible leakage/sampling issue) — reported as-is per fallback plan", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [202] ASSISTANT · 2026-09-05 22:07:08 UTC

```
Notebook runs end-to-end with no errors and produces a plausible (if noisy, given the tiny mini demo) output. Let's check total runtime and confirm the plot rendered.
```

### [203] TOOL CALL — Bash · 2026-09-05 22:07:08 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb = json.load(open('code_demo.ipynb'))
c = nb['cells'][-1]
types = [o.get('output_type') for o in c.get('outputs',[])]
print(types)
for o in c['outputs']:
    if o.get('output_type')=='display_data':
        print('has image:', 'image/png' in o.get('data',{}))
"
ls -la code_demo.ipynb mini_demo_data.json
grep -c GITHUB_DATA_URL code_demo.ipynb
```

### [204] TOOL RESULT — Bash · 2026-09-05 22:07:08 UTC

```
{"stdout": "['stream', 'display_data']\nhas image: True\n-rw-r--r-- 1 root root 160968 Sep  5 22:06 code_demo.ipynb\n-rw-r--r-- 1 root root  13607 Sep  5 21:24 mini_demo_data.json\n2", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [205] ASSISTANT · 2026-09-05 22:07:12 UTC

```
Everything checks out: plot rendered, no errors, GITHUB_DATA_URL present. Let's verify the exact URL string and clean up test artifacts.
```

### [206] TOOL CALL — Bash · 2026-09-05 22:07:12 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
grep -o 'GITHUB_DATA_URL = "[^"]*"' code_demo.ipynb
rm -rf .nb_env nbrun.log nbrun2.log nbrun3.log part_a_checkpoint.json 2>/dev/null
rm -rf results/part_a_checkpoint.json hf_runs logs .hf_cache 2>/dev/null
ls -la
```

### [207] TOOL RESULT — Bash · 2026-09-05 22:08:14 UTC

```
{"stdout": "total 4961\ndrwxr-xr-x 3 root root 2000102 Sep  5 22:08 .\ndrwxr-xr-x 4 root root 2000179 Sep  5 21:23 ..\n-rw-r--r-- 1 root root  902690 Sep  5 22:08 .repl_agent.ptylog\n-rw-r--r-- 1 root root  160968 Sep  5 22:06 code_demo.ipynb\n-rw-r--r-- 1 root root   13607 Sep  5 21:24 mini_demo_data.json\n-rw-r--r-- 1 root root       4 Sep  5 21:32 nbrun.pid\ndrwxr-xr-x 2 root root       1 Sep  5 22:08 results", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [208] TOOL CALL — Bash · 2026-09-05 22:08:18 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if 'GITHUB_DATA_URL' in c.get('source',''):
        print(repr(c['source'][:200]))
"
rm -f nbrun.pid
rmdir results 2>/dev/null
ls -la
```

### [209] TOOL RESULT — Bash · 2026-09-05 22:08:18 UTC

```
{"stdout": "total 4966\ndrwxr-xr-x 2 root root 2000103 Sep  5 22:08 .\ndrwxr-xr-x 4 root root 2000180 Sep  5 21:23 ..\n-rw-r--r-- 1 root root  908295 Sep  5 22:08 .repl_agent.ptylog\n-rw-r--r-- 1 root root  160968 Sep  5 22:06 code_demo.ipynb\n-rw-r--r-- 1 root root   13607 Sep  5 21:24 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [210] TOOL CALL — Bash · 2026-09-05 22:08:22 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
found=False
for c in nb['cells']:
    src = c.get('source','')
    if 'GITHUB_DATA_URL' in src:
        found=True
        print(src[:250])
        print('---')
print('found:', found)
EOF
```

### [211] TOOL RESULT — Bash · 2026-09-05 22:08:22 UTC

```
{"stdout": "found: False", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [212] TOOL CALL — Bash · 2026-09-05 22:08:28 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    src = c.get('source','')
    print(i, type(src))
EOF
```

### [213] TOOL RESULT — Bash · 2026-09-05 22:08:28 UTC

```
{"stdout": "0 <class 'list'>\n1 <class 'list'>\n2 <class 'list'>\n3 <class 'list'>\n4 <class 'list'>\n5 <class 'list'>\n6 <class 'list'>\n7 <class 'list'>\n8 <class 'list'>\n9 <class 'list'>\n10 <class 'list'>\n11 <class 'list'>\n12 <class 'list'>\n13 <class 'list'>\n14 <class 'list'>\n15 <class 'list'>\n16 <class 'list'>\n17 <class 'list'>\n18 <class 'list'>\n19 <class 'list'>\n20 <class 'list'>\n21 <class 'list'>", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [214] ASSISTANT · 2026-09-05 22:08:32 UTC

```
Right, nbconvert normalized `source` to line-lists. That's valid nbformat. Let's confirm URL correctly.
```

### [215] TOOL CALL — Bash · 2026-09-05 22:08:32 UTC

```
cd /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD
python3 << 'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    src = ''.join(c.get('source',[]))
    if 'GITHUB_DATA_URL' in src:
        print(src[:200])
EOF
```

### [216] TOOL RESULT — Bash · 2026-09-05 22:08:32 UTC

```
{"stdout": "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-d8fc3d-vocabulary-saturation-predicts-the/main/round-1/experiment-1/demo/mini_demo_data.json\"\nimport json, os\n\ndef", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [217] ASSISTANT · 2026-09-05 22:08:36 UTC

```
URL matches exactly. All verification checks pass. Now write the final structured output JSON.
```

### [218] TOOL CALL — Write · 2026-09-05 22:08:36 UTC

```
File: /ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.terminal_claude_agent_struct_out.json

{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
```

### [219] TOOL RESULT — Write · 2026-09-05 22:08:36 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_2ohq8qwlCPMZ/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art__VSV4YQ0_oJD/.terminal_claude_agent_struct_out.json", "content": "{\n  \"out_expected_files\": {\n    \"notebook\": \"code_demo.ipynb\",\n    \"mini_data_file\": \"mini_demo_data.json\"\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [220] ASSISTANT · 2026-09-05 22:08:43 UTC

```
Done. Summary:

- **`mini_demo_data.json`**: a curated ~100-example subset of Rotten Tomatoes (60 labeled train, 20 unlabeled pool, 20 held-out test), fetched via `datasets.load_dataset` once and saved to disk.
- **`code_demo.ipynb`**: a cell-by-cell, minimally-modified restructuring of `method.py` — install cell (Colab-guarded, following aii-colab), imports/hardware setup, GitHub-URL data loading with local fallback, a config cell exposing all tunables at minimal values (with original full-scale values commented alongside), then the original functions (TF-IDF+LR, DistilBERT fine-tuning, Good-Turing/Chao1 coverage curves, cross-domain calibration, verdict logic) copied essentially unchanged, only `load_domains()` adapted to read from the bundled JSON instead of downloading full HF datasets. Ends with a results table + matplotlib plot.
- Verified by executing the notebook end-to-end in a clean venv simulating Colab (`jupyter nbconvert --execute`) — it completes with no errors, produces a plausible accuracy-vs-n curve, coverage curve plot, and a `DISCONFIRMED`/verdict summary consistent with the original artifact's finding.
- Fixed two runtime issues found during testing: `matplotlib` and `accelerate` were missing from the install cell.

`.terminal_claude_agent_struct_out.json` has been written with the expected file paths.
```
