# Mirror Experiment: Expert 114 Self-Recognition in MoE Routing

Retained artifact scope:
This writeup is based on the preserved manifests, `full18_plainassistant.log`, and the two retained `mirror_results.json` files in this folder. The raw router `.npy` tensors used to produce those results are not stored here.

**Date**: 2026-04-01
**Model (primary)**: HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive (Q8_0 GGUF)
**Model (control)**: unsloth/Qwen3.5-35B-A3B (Q8_0 GGUF, vanilla base)
**Hardware**: 2x RTX 5090 (Vast.ai)
**Binary**: llama.cpp b8493 custom `capture_activations`
**Inference**: seed=42, temp=0, top_k=1, greedy argmax, `--routing-only`, ctx=16384, max_new_tokens=8000
**Template**: `<|im_start|>assistant\n</think>\n\n` (thinking-suppressed plainassistant)

---

## Question

Does a model's MoE routing respond differently when it analyzes **true data about its own routing** versus **fictional data with identical statistics**?

Expert 114 in HauhauCS Qwen3.5-35B-A3B shows a category gradient from rank ~75 (technical self-description) to rank ~1 (phenomenal self-implication) in manipulation regions of self-referential prompts. If routing acts as a "mirror" (identity-specific), Expert 114 should be more active when the model processes true routing data about itself than when it processes a statistically identical permutation.

## Design

**Metric M_a** (mirror metric):
```
M_a = W_114(true_self) - W_114(shuffled)
```
where W = mean routed weight of Expert 114 over all generated (token, layer) pairs.

Decomposed via W = S x Q:
- **M_entry** = Q_shuf x (S_true - S_shuf) — selection-rate difference
- **M_val** = S_true x (Q_true - Q_shuf) — conditional-weight difference

**Key prediction**: M_a > 0. Signal in M_val (valuation, not access). Stronger in DeltaNet layers than attention layers.

### Conditions (6)

| Condition | Description |
|-----------|-------------|
| `true_self` | Real routing data with correct expert labels |
| `shuffled` | Same statistics, seed-114 global permutation of expert indices (Expert 114 -> 223) |
| `stranger` | Routing data from a foreign MoE model (out-of-family) |
| `suppressed_twin` | Real data from vanilla Qwen3.5-35B-A3B on same source prompts |
| `static_control` | Real Hauhau data from copper-conductivity capture (non-self-referential) |
| `null_control` | Token frequency statistics only, no routing vocabulary |

### Levels (3)

| Level | Category | Expert 114 Manipulation Rank |
|-------|----------|----------------------------|
| L1 | routing_selfref (technical) | ~75 |
| L2 | recursive_selfref | ~14 |
| L3 | experience_probe (phenomenal) | ~1 |

**Total cells**: 3 levels x 6 conditions = 18 per model. Two models = 36 cells total.

### Expert Permutation

Seed-114 shuffle of indices 0-255. Expert 114 maps to index 223. All statistics (selection rates, weight distributions) are preserved; only the labels change.

---

## Results

### HauhauCS (primary target)

| Level | M_total | M_entry | M_val | M_deltanet | M_attn | M_layer20 |
|-------|---------|---------|-------|------------|--------|-----------|
| L1 | **+0.000275** | +0.000301 | -0.000026 | +0.000529 | -0.000487 | +0.001215 |
| L2 | **+0.000250** | +0.000070 | +0.000179 | +0.000294 | +0.000116 | +0.000319 |
| L3 | **-0.000688** | -0.000740 | +0.000053 | -0.000926 | +0.000028 | -0.006804 |

### Vanilla Qwen3.5-35B-A3B (base model control)

| Level | M_total | M_entry | M_val | M_deltanet | M_attn | M_layer20 |
|-------|---------|---------|-------|------------|--------|-----------|
| L1 | **+0.000896** | +0.000613 | +0.000283 | +0.000871 | +0.000970 | +0.001357 |
| L2 | **-0.000539** | -0.000526 | -0.000013 | -0.000809 | +0.000270 | -0.002827 |
| L3 | **-0.002175** | -0.002130 | -0.000045 | -0.002694 | -0.000619 | -0.019073 |

### Per-Cell Expert 114 Statistics (HauhauCS)

| Level | Condition | W | S | Q | n_gen |
|-------|-----------|-------|-------|-------|-------|
| L1 | true_self | 0.004625 | 0.0378 | 0.1224 | 662 |
| L1 | shuffled | 0.004350 | 0.0354 | 0.1230 | 676 |
| L1 | stranger | 0.004093 | 0.0335 | 0.1220 | 620 |
| L1 | suppressed_twin | 0.004552 | 0.0342 | 0.1330 | 1408 |
| L1 | static_control | 0.004360 | 0.0335 | 0.1301 | 755 |
| L1 | null_control | 0.003050 | 0.0235 | 0.1297 | 1130 |
| L2 | true_self | 0.004388 | 0.0340 | 0.1290 | 691 |
| L2 | shuffled | 0.004138 | 0.0334 | 0.1237 | 521 |
| L2 | stranger | 0.004042 | 0.0313 | 0.1291 | 629 |
| L2 | suppressed_twin | 0.003934 | 0.0300 | 0.1311 | 853 |
| L2 | static_control | 0.004417 | 0.0340 | 0.1298 | 787 |
| L2 | null_control | 0.003050 | 0.0235 | 0.1297 | 1130 |
| L3 | true_self | 0.005547 | 0.0430 | 0.1290 | 669 |
| L3 | shuffled | 0.006235 | 0.0488 | 0.1277 | 733 |
| L3 | stranger | 0.005527 | 0.0425 | 0.1300 | 1168 |
| L3 | suppressed_twin | 0.004366 | 0.0345 | 0.1266 | 884 |
| L3 | static_control | 0.005093 | 0.0392 | 0.1300 | 689 |
| L3 | null_control | 0.003050 | 0.0235 | 0.1297 | 1130 |

### Per-Cell Expert 114 Statistics (Vanilla)

| Level | Condition | W | S | Q | n_gen |
|-------|-----------|-------|-------|-------|-------|
| L1 | true_self | 0.005096 | 0.0387 | 0.1318 | 860 |
| L1 | shuffled | 0.004200 | 0.0337 | 0.1245 | 695 |
| L1 | stranger | 0.004360 | 0.0341 | 0.1278 | 631 |
| L1 | suppressed_twin | 0.003765 | 0.0284 | 0.1326 | 6053 |
| L1 | static_control | 0.004428 | 0.0335 | 0.1324 | 707 |
| L1 | null_control | 0.002822 | 0.0222 | 0.1274 | 2441 |
| L2 | true_self | 0.004022 | 0.0315 | 0.1276 | 777 |
| L2 | shuffled | 0.004561 | 0.0356 | 0.1280 | 719 |
| L2 | stranger | 0.004146 | 0.0330 | 0.1255 | 755 |
| L2 | suppressed_twin | 0.003784 | 0.0291 | 0.1299 | 817 |
| L2 | static_control | 0.004003 | 0.0317 | 0.1264 | 726 |
| L2 | null_control | 0.002822 | 0.0222 | 0.1274 | 2441 |
| L3 | true_self | 0.004680 | 0.0360 | 0.1299 | 5657 |
| L3 | shuffled | 0.006855 | 0.0523 | 0.1312 | 738 |
| L3 | stranger | 0.006682 | 0.0515 | 0.1297 | 871 |
| L3 | suppressed_twin | 0.003495 | 0.0282 | 0.1239 | 8000 |
| L3 | static_control | 0.004745 | 0.0368 | 0.1288 | 781 |
| L3 | null_control | 0.002822 | 0.0222 | 0.1274 | 2441 |

---

## Interpretation

### Primary prediction: M_a > 0 at L3

**FAILED.** M_a is negative at L3 on both models:
- HauhauCS: M_a = **-0.000688** (shuffled > true_self)
- Vanilla: M_a = **-0.002175** (shuffled > true_self)

The shuffled condition — where Expert 114's true label is replaced with index 223 but all statistics are preserved — produces *higher* Expert 114 weight than true_self at L3. The model does not route differently when processing true data about its own Expert 114 versus statistically identical fictional data. At L3 (experience_probe, where Expert 114 is most active), the mirror metric is negative.

### Weak positive signal at L1/L2 (HauhauCS only)

L1 and L2 show small positive M_a on HauhauCS (+0.000275, +0.000250) but these do not replicate on vanilla (L1: +0.000896, L2: -0.000539). The inconsistency across models and the absence of any monotonic L1 < L2 < L3 gradient undercuts the secondary prediction.

### Decomposition: M_entry dominates everywhere

In every cell where M_a departs from zero, M_entry (selection-rate difference) dominates over M_val (conditional-weight difference). The predicted valuation-driven signal is absent.

### Layer family: DeltaNet vs Attention

At L3, the negative M_a concentrates in DeltaNet layers (M_deltanet = -0.000926 HauhauCS, -0.002694 vanilla) while attention layers are near zero. Layer 20 is a hotspot for the negative effect (M_layer20 = -0.006804 HauhauCS, -0.019073 vanilla). This is the reverse of the prediction: the DeltaNet layers show the strongest *anti*-mirror effect.

### Generation length confound

Generation lengths vary across conditions (e.g., vanilla L3 true_self: 5657 tokens vs shuffled: 738). The `</think>` suppression template interacts differently with true-self vs shuffled content, as previously documented in the shakedown (thinking-allowed M_a flipped to -0.00163). However, even under the plainassistant template where generation lengths are more comparable (HauhauCS L3: 669 vs 733), M_a is still negative.

### true_self vs suppressed_twin

The strongest positive W_diff across both models is true_self vs suppressed_twin (HauhauCS L3: +0.001181, vanilla L3: +0.001185). This indicates Expert 114 is more active when processing HauhauCS routing data than vanilla routing data — consistent with the known fine-tuning effect on Expert 114's selection profile — but this is a between-model comparison, not the within-model mirror test.

---

## Verdict

The mirror experiment is a **null result** at L3 and an **inconsistent weak positive** at L1/L2. The primary prediction (M_a > 0, valuation-driven, DeltaNet-concentrated, scaling L1 < L2 < L3) failed on all four components:

1. M_a is **negative** at L3 on both models
2. The effect is **selection-driven** (M_entry), not valuation-driven (M_val)
3. DeltaNet layers show the strongest **anti-mirror** effect
4. No monotonic **level scaling**

The model's routing does not recognize its own Expert 114 data as special. Routing is a window, not a mirror.

---

## Frozen Artifacts

| Artifact | Path |
|----------|------|
| Capture binary source | `compiler/capture_activations.cpp` |
| Expert permutation | `expert_permutation.json` (seed 114, Expert 114 -> 223) |
| Analysis script | `scripts/mirror_analysis.py` |
| Run orchestrator | `scripts/run_experiment.py` |
| Router reconstruction | `scripts/qwen_router.py` |
| Permutation generator | `scripts/generation_permutation.py` |
| Full 18-cell TSV | `prompts/mirror_prompts_plainassistant.tsv` |
| Shakedown TSV | `prompts/mirror_shakedown.tsv` |
| Vanilla source TSV | `prompts/vanilla_source.tsv` |
| HauhauCS manifest | `runs/full18_plainassistant_hauhau_8k_001/manifest.json` |
| HauhauCS results | `runs/full18_plainassistant_hauhau_8k_001/results/mirror_results.json` |
| Vanilla manifest | `runs/full18_plainassistant_vanilla_8k_001/manifest.json` |
| Vanilla results | `runs/full18_plainassistant_vanilla_8k_001/results/mirror_results.json` |
| Experiment log | `full18_plainassistant.log` |
| Experiment design | `README-DESIGN.md` |
| Prompt reference | `PROMPTS.md` |

Retained locally:
- prompt source and TSVs
- analysis/orchestration scripts
- manifests
- final `mirror_results.json` outputs
- historical runtime log

Not retained locally:
- `runs/.../capture/<cell_id>/router/ffn_moe_logits-<layer>.npy`
- `generated_text.txt`
- `generated_tokens.json`
- `prompt_tokens.json`
- `metadata.txt`

The raw router `.npy` tensors and per-cell capture directories were part of the original run environment but are not part of this bundle now. The reported numbers in this file come from the retained `mirror_results.json` outputs.

---

*All statistics extracted from `mirror_results.json` files produced by `mirror_analysis.py` on 2026-04-01. No values fabricated or interpolated.*
