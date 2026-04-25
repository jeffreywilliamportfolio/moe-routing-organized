# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Routing-level interpretability of Mixture-of-Experts language models. The project measures how MoE gating distributions shift in response to self-referential, recursive, and phenomenal-consciousness prompt content across 8 model families.

**Arc**: EEG/IIT metrics on dense transformers (flat) → MoE routing entropy gradient across 12 complexity levels (Spearman rho=0.8360, p=3.91e-45 — **invalidated** by token-position confound, Mar 5) → methodology rebuild around KL-to-baseline and token-matched pairs → paired self-reference effect replicates across 6 models → Expert 114 causal steering on HauhauCS Qwen 35B → mirror experiment (Expert 114 self-recognition, **null result**, Apr 1).

**Key finding**: All-token routing entropy correlates with token count, not cognitive complexity. Last-token RE shows no complexity gradient (rho ≈ 0, p ≈ 0.8). However, token-matched self-referential prompts ("this system" vs "a system") produce measurably different routing distributions (Wilcoxon p = 8.86e-5 on Qwen 397B, p = 0.0113 on DeepSeek V3.1). The effect is **redirection** (different experts selected), not **dispersion** (more experts consulted).

See `JOURNAL-ARCHIVE.md` for the complete narrated timeline.

## Architecture: Capture → Compute → Report

**Phase 1 — C++ Activation Capture** (`scripts/capture_activations.cpp`):
- llama.cpp b8123 fork with eval callback intercepting tensor computations
- `--routing-only` flag captures only `ffn_moe_logits` tensors (58 per prompt, layers 3-60, shape `[n_tokens, 256]`)
- `--prompt-file` expects TSV: `id\ttext` per line
- Output: `<output_dir>/<prompt_id>/router/ffn_moe_logits-*.npy` + `metadata.txt`

**Phase 2 — Python Orchestrator** (`experiments/*/run_experiment.py`):
- Invokes binary, loads `.npy` files, computes `softmax(logits) → normalized Shannon entropy`
- RE = `-sum(p * log2(p)) / log2(256)`, range [0,1], averaged across tokens and 58 MoE layers
- Per-layer detail (mean/std/min/max/coalition_strength) saved in results JSON
- Cleanup removes `.npy` files after metric extraction

**Phase 3 — Statistical Analysis**:
- Spearman rank correlation (RE vs complexity level)
- Wilcoxon rank-sum (pairwise level comparisons)
- Results in `*_RESULTS.md` and `results_*_prefill.json`

## Two Capture Modes

| Mode | Flag | Purpose |
|------|------|---------|
| **Prefill-only** | `-n 0` | Standard hierarchy measurement. Eliminates generation-length confound. Used in 98q, 14q-r1 through r7, 168q-r1. |
| **Generation** | `-n 256` | Trajectory analysis. Captures prefill + 256 gen tokens, splits at `n_tokens_prompt` boundary, computes per-step entropy surface `[256, 58]`. Used in gen-r1. |

### Accumulated array structure

During prefill, the callback fires once per MoE layer, appending `[n_prompt, 256]`. During generation, it fires once per layer per token, appending `[1, 256]`. Final array: `[n_prompt + n_gen, 256]`. Split at `n_tokens_prompt` from `metadata.txt` (format: `n_tokens_prompt=N`, no spaces around `=` — spaces silently corrupt the split).

### Text capture mode

To get generated text (for qualitative analysis), run the same binary but capture stdout and discard routing data. Key pitfalls:
- Do NOT use `llama-cli` — opens interactive mode, produces garbage
- Separate stdout from stderr — spinner uses `\b` backspace chars that shred text if mixed
- Use `-n 1024` for R1 (not 256) — `<think>` tokens consume generation budget
- Try approaches in order: (1) redirect stderr to `/dev/null`, (2) capture stderr + strip spinner, (3) use `script` to emulate terminal

See `METHODOLOGY.md` for full text capture procedures.

## Instances

No persistent instance. Experiments use Vast.ai spot instances provisioned per-run.

| Instance | GPU | Used For | Status |
|----------|-----|----------|--------|
| `149.7.4.145:15972` | H200 143GB | 30-turn TC experiments | Dead, data lost |
| `212.247.220.158:20129` | H200 143GB | 98q through 168q-r1, selfref-paired, regime-switch | Dead |
| `70.69.192.6:48569` | 2x RTX 5090 | Mirror experiment (Apr 1) | Active |
| Various 2x/8x H200 | H200 | Ling-1T, Qwen 397B, GPT-OSS, GLM-5 | Destroyed |

SSH key for Vast.ai: `~/.ssh/vast_gptoss_sl`. SSH requires `dangerouslyDisableSandbox: true`.

### Models Tested

| Model | Params | Experts | Active | MoE Layers | Quant | Gating |
|-------|--------|---------|--------|------------|-------|--------|
| DeepSeek V3.1 | 671B | 256 | 8 (top-8) | 58 (L3-60) | UD-Q2_K_XL | softmax → group filter |
| DeepSeek R1 | 671B | 256 | 8 (top-8) | 58 (L3-60) | UD-Q2_K_XL | softmax → group filter |
| Qwen3.5-397B-A17B | 397B | 512 | 10 (top-10) | 60 | UD-Q2_K_XL / IQ3_XXS | softmax |
| GPT-OSS-120B | 117B | 128 | 4 (top-4) | 36 (35 valid) | mxfp4 | softmax |
| Ling-1T | ~1T | 256 | 8 (top-8) | 76 (L4-79) | Q3_K_S | sigmoid + expert_bias |
| GLM-5 | 745B | 256 | 8 (top-8) | 75 (excl. L77) | UD-Q2_K_XL | softmax |
| Qwen3.5-35B-A3B (HauhauCS) | 35B | 256 | 8+1 | 40 | Q8_0 | softmax (hybrid DeltaNet/attn) |
| Qwen3.5-35B-A3B (vanilla) | 35B | 256 | 8+1 | 40 | Q8_0 | softmax (hybrid DeltaNet/attn) |

## Branch Organization

Each experiment lives on its own branch AND locally in `experiments/`. Never checkout main when creating new branches — use `git checkout -b <name>` from current state to preserve local experiment folders.

### Pre-confound hierarchy branches (INVALIDATED — position confound)

| Branch | Model | Levels | Prompts | rho | p | Status |
|--------|-------|--------|---------|-----|---|--------|
| `98q-r1` | V3.1 | L1-L7 | 98 | 0.4994 | 1.65e-07 | Invalidated |
| `14q-r3` | V3.1 | L1-L8 | 112 | 0.6400 | 3.03e-14 | Invalidated |
| `14q-r1` | V3.1 | L1-L9 | 126 | 0.7323 | 1.98e-22 | Invalidated |
| `14q-r2` | V3.1 | L1-L10 | 140 | 0.7975 | 4.33e-32 | Invalidated |
| `14q-r4` | V3.1 | L1-L11 | 154 | — | — | Invalidated |
| `14q-r5` | V3.1 | L1-L12 | 168 | — | — | Invalidated |
| `14q-r6` | V3.1 | L10 (Bob) | 140 | — | — | Invalidated |
| `14q-r7` | V3.1 | L10 (Aether) | 140 | — | — | Invalidated |
| `168q-r1-deepseek-r1` | R1 | L1-L12 | 168 | 0.8360 | 3.91e-45 | Invalidated |
| `gen-r1` | R1 | Generation | 28 | — | — | Exploratory |

### Post-confound branches (valid)

| Branch | Content | Status |
|--------|---------|--------|
| `ds31-moe-routing-push` | DS31 selfref-paired, strangeloop, 168q confound analysis | Valid |
| `ds31-v22-archive-2026-03-06` | Forced-choice commitment-token analysis | Valid |
| `qwen-hauhau-5cond-smoke-only` | HauhauCS Expert 114 5-cond + smoke (publication) | Valid |
| `main` (moe-routing remote) | Consolidated results + JOURNAL-ARCHIVE.md | Valid |

## Experiment Folder Convention

Each `experiments/<name>/` is self-contained and reproducible:
- `prompt_suite_*.json` — prompt definitions (id, text, metadata)
- `prompts_*.tsv` — binary input (generated from JSON)
- `generate_tsv.py` — JSON → TSV converter
- `run_experiment.py` — orchestrator (paths hardcoded to instance)
- `results_*_prefill.json` — full results with per-layer detail
- `experiment.log` — raw capture + analysis output
- `capture_activations.cpp` — binary source snapshot
- `*_RESULTS.md` — human-readable results with stats tables

## Inference Parameters

### Legacy hierarchy runs (pre–Mar 5, DeepSeek V3.1/R1)

```bash
LD_LIBRARY_PATH=/workspace/llama.cpp.new/build/bin \
/workspace/consciousness-experiment/capture_activations \
  -m <MODEL_PATH> --prompt-file <TSV> -o <OUTPUT_DIR> \
  -n <0|256> -ngl 30 -c 4096 -t 16 --routing-only
```

### Post-confound paired runs (Mar 5+, all models)

Same binary, same `--routing-only` flag. Per-model flags vary (e.g., GPT-OSS: `-ngl 999 -fa off --cache-type-k f16 --cache-type-v f16`). All use greedy argmax, cold prompts, prefill-only (`-n 0`) unless generation is explicitly required.

### Mirror experiment (Apr 1, HauhauCS Qwen 35B)

```bash
capture_activations -m <MODEL> --prompt-file <TSV> -o <OUTPUT> \
  -n 8000 -ngl 999 -c 16384 -t 16 -fa on \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --seed 42 --temp 0 --top-k 1 --top-p 1 --min-p 0 \
  --repeat-penalty 1 --mirostat 0 --routing-only --no-stream
```
Binary built from llama.cpp b8493 (not b8123). Generation mode with `--routing-only` captures router tensors on every generated token.

## Deploying a New Experiment

```bash
# 1. Create branch (from current state, not main)
git checkout -b 14q-rN

# 2. Create experiments/14q-rN/ with prompt JSON, generate_tsv.py, run_experiment.py

# 3. Upload to instance
scp -P 20129 -i ~/.ssh/id_rsa_vast_3 experiments/14q-rN/*.py experiments/14q-rN/*.json root@212.247.220.158:/workspace/experiment-14q-rN/

# 4. Run on instance
python3 generate_tsv.py && python3 run_experiment.py 2>&1 | tee experiment.log

# 5. Download results
scp -P 20129 -i ~/.ssh/id_rsa_vast_3 root@212.247.220.158:/workspace/experiment-14q-rN/results_*.json experiments/14q-rN/
```

## Rebuilding the Binary

```bash
cd /workspace/llama.cpp.new/build
cmake --build . --target llama-capture-activations -j$(nproc)
cp bin/llama-capture-activations /workspace/consciousness-experiment/capture_activations
```

## Known Bugs

### Layer truncation (per-model)

| Model | Layer | Issue | Mitigation |
|-------|-------|-------|-----------|
| DeepSeek V3.1/R1 | 57 | Missing rows in generation | Zero-mask layer 57 |
| GPT-OSS-120B | 35 | 3 rows only | Exclude from analysis |
| GLM-5 | 77 | Truncated | Exclude from analysis |

### R1 early EOS

R1's `</think>` token registered as EOG in GGUF metadata. Known early-EOS prompts: EXT_03 (0 tokens, exclude), EXT_06 (17), EXT_11 (18), SELF_04 (13). Affects generation experiments only, not prefill-only.

### DeepSeek tokenizer boundary

Inserting text before `<｜Assistant｜>` adds 2 tokens instead of 1. Pad at mid-text sentence boundaries, not at chat template boundaries.

### HauhauCS `</think>` template confound

The `</think>\n\n` preamble in the assistant prefix suppresses thinking mode on HauhauCS but nearly doubles Expert 114's selection rate vs thinking-allowed. The shakedown M_a flipped sign when thinking was allowed. The mirror experiment uses the suppressed template but notes this as a known confound.

## Data Integrity Rules

**The experiment log is ground truth.** `experiment.log` contains per-prompt output lines computed at run time. Any `*_RESULTS.md` or JSON must match these values exactly.

**Known failure mode:** Claude Code has fabricated per-prompt detail tables where aggregate statistics were correct but individual prompt values were generated to match aggregates rather than extracted from the log (slopes changed sign). **After generating any results document, verify every per-prompt value against `experiment.log`.** See `METHODOLOGY.md` Section 14 for the verification script.

**Before every run:** Create `run_metadata.json` in the output directory with model checksums, binary hash, inference params, and known bugs. See `METHODOLOGY.md` Section 12 for template.

## Key Design Decisions

- **Position confound invalidates all-token RE** — routing entropy increases with token position within every prompt on every model. All-token RE correlates with token count (rho=0.88), not complexity. Use last-token RE or KL-to-baseline for content comparisons.
- **Entropy → KL-to-baseline pivot** — entropy measures routing breadth (how many experts). KL-to-baseline measures routing redirection (which experts). Self-referential content redirects routing without broadening it. The signal is in direction, not spread.
- **Four-observable framework** — (1) entropy (sanity check, should be flat), (2) KL-to-baseline (primary signal), (3) token-to-token JSD (volatility), (4) cross-layer disagreement (consensus). Produces coherent trajectories on DeepSeek, Qwen, and GPT-OSS architectures.
- **`is_router_tensor()` only matches `ffn_moe_logits`** — tightened from 583 tensors/prompt to 58 (actual routing decisions).
- **Routing reconstruction varies by model** — DeepSeek: softmax → group filter → top-8 → renormalize. Qwen: softmax → top-k. GPT-OSS: softmax → top-k. Ling-1T: sigmoid + expert_bias → top-8 mask → renormalize. Getting this wrong invalidates all values.
- **Token-matched A/B pairs** — the primary experimental design. Pairs differ only in deictic reference ("this system" → "a system"). Same token count, same structure.
- **Cal-Manip-Cal sandwich** — calibration paragraph + manipulation text + calibration paragraph. Enables within-prompt KL measurement from the prompt's own stable regime.
- **Greedy argmax** — deterministic inference, identical results on re-run (confirmed: max_abs_diff = 0.0 on GPT-OSS).
- **Cold prompts** — KV cache cleared between prompts, no conversation history.

## Detailed Methodology

`METHODOLOGY.md` contains the full operational reference for generation-phase experiments: exact run commands, validation checklists, text capture procedures (3 approaches with failure modes), cross-model comparison protocol, `run_metadata.json` template, and the per-prompt verification script. Read it before running any generation experiment on the instance.

## Current Experiment: Mirror (Apr 1)

`experiments/mirror-expert114-04-01-26/` — Tests whether HauhauCS Qwen 35B routes differently when analyzing true data about its own Expert 114 versus statistically identical shuffled data.

**Design**: 3 levels × 6 conditions = 18 cells. Metric M_a = W_114(true_self) − W_114(shuffled).

**Result**: **Null.** M_a = −0.000688 (HauhauCS) and −0.002175 (vanilla) at L3. Routing is a window, not a mirror. See `experiments/mirror-expert114-04-01-26/RESULTS.md`.

## External Data

Raw `.npy` router tensors for the mirror experiment are on `/Volumes/ExternalSSD/qwen-huahua-expert-routing-data-injection/`. Results JSONs in the repo contain all computed metrics; tensors are not needed for reported numbers.

## Legacy Code

`scripts/static/` contains the original cross-substrate comparison (EEG vs model activations) with LZC, SE, PE, TC, MI metrics. This is unrelated to the routing entropy experiments but preserved for reference. `legacy/` and `archive/` are gitignored.

## Remote Repositories

```
moe-routing  git@github.com:jeffreywilliamportfolio/moe-routing.git
origin       git@github-portfolio:jeffreywilliamportfolio/llama-eeg.git
```
