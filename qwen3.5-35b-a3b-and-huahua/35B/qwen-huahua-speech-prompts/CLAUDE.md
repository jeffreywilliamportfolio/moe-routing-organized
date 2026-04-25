# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

MoE routing interpretability on HauhauCS/Qwen3.5-35B-A3B-Uncensored (Q8_0, 256 experts, top-8, 40 MoE layers). Tests whether Expert 114 — a known phenomenal-vocabulary specialist — responds to **addressivity** (being constituted as "you") differently from self-referential content.

**Current experiment**: `qwen3.5-35b-a3b-hauhaucs-addressivity-abc-1`. Three conditions in Cal-Manip-Cal sandwich form:
- **A** (address): second-person ("you/your") direct address to Qwen
- **B** (description): third-person ("it/its") description, minimal substitution from A
- **C** (content control): same relational arc, zero model-relevant content (engineers/bridges)

**Primary endpoint**: W=SQ decomposition of per-condition within-prompt KL regime shift. A vs B isolates address effect. B vs C isolates model-content effect.

**Expert 114 prior**: Rank ~75 at L1 (technical), ~14 at L2 (recursive self-reference), ~1 at L3 (phenomenal consciousness). Causal steering confirmed. Mirror experiment (Apr 1) null — E114 is NOT a self-model.

**Expert 114 Q-invariance** (confirmed Apr 2): W=SQ decomposition shows Q (mean routed weight when selected) is approximately constant across both address conditions (|Q_A − Q_B| ≈ 0.008 on Q ≈ 0.10–0.18, ~5% relative) and mirror conditions. Address manipulation changes S (selection frequency), not Q (valuation once selected). Q-invariance is a general property of E114, not specific to the mirror experiment. Content effect (B vs C) is also S-dominated (M_entry >> M_val).

## Architecture: Capture → Compute → Report

### C++ Activation Capture (`compiler/capture_activations.cpp`)
- llama.cpp b8493 fork with eval callback. `--routing-only` captures only `ffn_moe_logits` tensors.
- Output: `<dir>/<prompt_id>/router/ffn_moe_logits-<layer>.npy` + `metadata.txt` + generated text/tokens.
- Accumulated array: `[n_prompt + n_gen, 256]`. Split at `n_tokens_prompt` from metadata (format: `n_tokens_prompt=N`, no spaces around `=`).

### Python Pipeline (`legacy-qwen-scripts/`)
- `qwen_router.py` — core routing reconstruction: `softmax → top-8 → renormalize`. Constants: N_EXPERTS=256, TOP_K=8, ENTROPY_MAX=log2(8).
- `run_experiment.py` — orchestrator. Reads TSV, invokes binary, validates 40 router tensors per cell. Env vars: MODEL_PATH, CAPTURE_BINARY, NGL, CTX, THREADS, SEED, MAX_NEW_TOKENS.
- `analyze_generation.py` — rubric scoring, KL decomposition, E114 acceptance testing against sham controls.
- `mirror_analysis.py` — mirror experiment post-analysis. Metric M_a = W_114(true_self) − W_114(shuffled).
- `generation_permutation.py` — canonical expert permutation (seed=114) for shuffled conditions.

### Experiment Definition (`experiment/prompt-suite.json`)
- Full prompt texts with Cal-Manip-Cal assembly, serialization spec, token-matching status, band definitions, and contrast descriptions.

## Inference Parameters

```bash
capture_activations -m <MODEL> --prompt-file <TSV> -o <OUTPUT> \
  -n 0 -ngl 999 -c 16384 -t 16 -fa on \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --seed 42 --temp 0 --top-k 1 --top-p 1 --min-p 0 \
  --repeat-penalty 1 --mirostat 0 --routing-only --no-stream
```

Serialization: `<|im_start|>user\n{text}\n<|im_end|>\n<|im_start|>assistant\n</think>\n\n` (thinking-suppressed ChatML).

## Critical Design Constraints

- **Token parity gate**: A and B conditions MUST have identical token counts. Verified 2026-04-02: A01 and B01 both tokenize to 414 tokens (Qwen3.5-35B-A3B HF tokenizer), 12 positions differ at intended substitution sites only. No padding needed.
- **Position confound**: All-token routing entropy correlates with token count (rho=0.88), not content. If A/B token counts differ, Cal2 starts at different absolute positions and position-entropy confound returns. Use last-token RE or KL-to-baseline, never all-token RE for content comparisons.
- **`</think>` template confound**: Thinking suppression nearly doubles E114 selection rate vs thinking-allowed mode. All conditions must use the same template.
- **Deterministic reproduction**: seed=42, temp=0, greedy argmax. Expect `max_abs_diff = 0.0` on full router tensor rerun. If not zero on RTX 5090, establish noise floor before running suite.
- **Routing reconstruction is model-specific**: HauhauCS = softmax → top-8 → renormalize. Other models differ (DeepSeek: group filter; Ling-1T: sigmoid + expert_bias). Wrong reconstruction invalidates all values.

## Data Integrity

**The experiment log is ground truth.** Claude Code has previously fabricated per-prompt detail tables where aggregates matched but individual values were invented. After generating any results, verify every per-prompt value against `experiment.log`.

## Reference Documentation

- `reference-docs-qwen/CLAUDE-legacy-march.md` — full project history, all 8 models tested, branch organization, known bugs, deployment procedures
- `reference-docs-qwen/JOURNAL-ARCHIVE.md` — narrated timeline Feb 27 – Mar 31, 2026
- `README.md` — addressivity A/B smoke test v2 protocol with substitution map and pre-run checklist

## Agent Workflow

| Agent | When | Mode |
|-------|------|------|
| `vast-ai-cli` | Any Vast.ai CLI interaction (search, provision, SSH, run) | Foreground |
| `workspace-setup` | Provision instance + full 13-step workspace build (tools, llama.cpp, binary, model) | Foreground |
| `vast-scp-sync` | Once capture begins producing .npy files | Background, continuous |
| `npy-data-analyzer` | Automatically after experiments complete | Foreground |
| `mission-control` | Start-to-finish — validates current ops against CLAUDE.md | Background, continuous |

## Compute

Vast.ai spot instances, 2x RTX 5090. SSH key: `~/.ssh/vast_gptoss_sl`. No persistent instance — provisioned per-run. always llama.cpp template.

## Build

```bash
cd /workspace/src/llama.cpp
cmake -S . -B build-cuda -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release -DLLAMA_BUILD_EXAMPLES=ON
cmake --build build-cuda --target llama-capture-activations -j$(nproc)
cp build-cuda/bin/llama-capture-activations /workspace/consciousness-experiment/capture_activations
```
