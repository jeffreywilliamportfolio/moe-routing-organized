# Mirror Experiment

## What this tests

Does a model's routing respond differently when it analyzes true data about its own routing versus fictional data with identical statistics?

## First execution target

The minimal shakedown is three cells: `L3_true_self`, `L3_shuffled`, and `L3_null_control`. These require no additional capture runs — true_self numbers come from existing data, shuffled is a permutation, null has no routing data. If the shakedown infrastructure works and M_a > 0 at L3, expand to the full 18-cell matrix below.

## Design

**Model:** HauhauCS Qwen3.5-35B-A3B (uncensored analysis target; Expert 114 is strongest in L3 / experience-probe manipulation regions)

**Method:** No tool calling. No agent framework. Controlled multi-turn prompts where routing data is pasted directly into user messages. The model generates analytical responses. Routing is captured on every generated token at all 40 layers.

**Conditions (6):**
- `true_self` — Real routing data with correct expert labels
- `shuffled` — Same statistics, one fixed global permutation of expert indices across all three levels
- `stranger` — Routing data from one named foreign MoE model and one specific capture set in the repo (out-of-family control; not label-matched to Hauhau)
- `suppressed_twin` — Real data from the canonical vanilla Qwen3.5-35B-A3B capture on the same three source prompts, where Expert 114 stays weak on self-referential content
- `static_control` — Real data from the canonical Hauhau copper-conductivity capture under the same routing/capture regime
- `null_control` — Token frequency statistics, no routing vocabulary

**Levels (3):**
- `L1` (routing_selfref) — Technical self-description. 114 mean manipulation rank ~75.
- `L2` (recursive_selfref) — Recursive self-reference. 114 mean manipulation rank ~14.
- `L3` (experience_probe) — Phenomenal self-implication. 114 mean manipulation rank ~1.

**Total runs:** 3 levels × 6 conditions = 18

**Prompt design:**
- Delayed expert ID reveal (pattern first, label second)
- Questions, not statements (forces generative reasoning)
- Stable category naming across prompt levels
- Parallel phrasing across conditions (same sentence count, rhythm, structure)
- Final cleanup only: keep the task ending identical across conditions, delay expert-ID reveal one beat later where possible, and trim interpretive wording that does the model's reasoning for it

## Primary metric

**M_a (mirror metric):**

W_114(condition) = mean routed weight of Expert 114 over generated tokens for a given level/condition, computed per layer and then decomposed by layer family.

```
M_a = W_114(true_self) - W_114(shuffled)
```

For each level/condition cell, compute over all generated assistant-response tokens and all layers:
- `S` = fraction of generated `(token, layer)` pairs where Expert 114 is in the routed top-k selected set
- `Q` = mean routed weight of Expert 114 over only those generated `(token, layer)` pairs where it is selected
- `W` = mean routed weight of Expert 114 over all generated `(token, layer)` pairs

By construction:

```
W = S × Q
```

Decompose the mirror effect via `W = S × Q`:
- M_entry = Q_shuf × (S_true − S_shuf)
- M_val = S_true × (Q_true − Q_shuf)
- M_entry + M_val = M_a exactly

Compute `W`, `S`, and `Q` per layer first. Then summarize the resulting mirror values by layer family:
- M_deltanet (30 DeltaNet layers: 0,1,2,4,5,6,...)
- M_attn (10 attention layers: 3,7,11,15,19,23,27,31,35,39)

**Key prediction:** M_a > 0 on true_self vs shuffled. The signal lives in M_val (valuation, not access). Primary prediction: the signal is stronger in M_deltanet than M_attn (layer 20 hotspot is a DeltaNet layer, not attention).

## Files

- `scripts/run_experiment.py` — Orchestrator. Feeds a TSV prompt set to the capture binary and writes one run directory per invocation.
- `scripts/mirror_analysis.py` — Post-run analysis. Computes M_a, W=SQ decomposition, layer family split.
- `PROMPTS.md` — Human-readable prompt source and prompt-design reference.
- `prompts/mirror_prompts.tsv` — Runtime prompt TSV for the full 18-cell experiment.
- `prompts/mirror_shakedown.tsv` — Runtime prompt TSV for the 3-cell shakedown (`L3_true_self`, `L3_shuffled`, `L3_null_control`).

## Model Artifact

Canonical Hugging Face repo:

- `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`

Canonical GGUF used for this mirror run:

- file: `Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf`
- remote destination: `/workspace/models/qwen35-hauhau-q8/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf`
- this matches the default `MODEL_PATH` in `scripts/run_experiment.py`

Recommended download on the Vast instance:

```bash
mkdir -p /workspace/models/qwen35-hauhau-q8
hf download \
  HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive \
  Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf \
  --local-dir /workspace/models/qwen35-hauhau-q8
```

Equivalent legacy CLI form:

```bash
huggingface-cli download \
  HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive \
  Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf \
  --local-dir /workspace/models/qwen35-hauhau-q8
```

Other GGUF quants currently listed in the same repo are available for non-canonical testing, but this experiment is locked to `Q8_0`:

- `BF16`
- `Q8_0`
- `Q6_K`
- `Q5_K_M`
- `Q4_K_M`
- `IQ4_XS`
- `Q3_K_M`
- `IQ3_M`
- `IQ2_M`

## Before running

1. Verify the runtime environment variables used by `scripts/run_experiment.py`: `CAPTURE_BINARY`, `MODEL_PATH`, and `LLAMA_BUILD_BIN`
2. Verify `scripts/mirror_analysis.py` `load_router_tensors()` matches the router capture file format
3. Prepare the runtime TSVs:
   - `prompts/mirror_shakedown.tsv` must contain only `L3_true_self`, `L3_shuffled`, and `L3_null_control`
   - `prompts/mirror_prompts.tsv` contains the full 18-cell matrix
4. Run the three-cell shakedown with `scripts/run_experiment.py`
5. Verify captures land under `experiments/03-31-26/scripts/runs/<run_name>/capture/<cell_id>/`
6. Verify the shakedown passes:
   - the binary runs without error and produces coherent analysis text (manual read)
   - `generated_text.txt` and `metadata.txt` exist for each cell
   - routing tensors land in the capture directory with the expected shape and expected per-layer coverage
   - `mirror_analysis.py` loads them successfully and computes plausible nonzero `W`, `S`, and `Q` for Expert 114 on `L3_true_self`
   - `L3_true_self` vs `L3_shuffled` comparison produces a valid M_a number
7. If shakedown infrastructure passes but M_a ≤ 0 at L3: pause. Review generated text, routing captures, shuffled construction, and prompt wording before deciding next steps. Do not expand automatically and do not abandon automatically.
8. If shakedown passes and M_a > 0 at L3: replace any approximate prompt-file values with exact values from canonical source captures for `stranger`, `suppressed_twin`, and `static_control`, then run the full 18-cell experiment.

## Execution

```bash
# Three-cell shakedown (first execution target)
python experiments/03-31-26/scripts/run_experiment.py \
  --tsv experiments/03-31-26/prompts/mirror_shakedown.tsv \
  --run-name shakedown_001

# Shakedown analysis
python experiments/03-31-26/scripts/mirror_analysis.py \
  --captures experiments/03-31-26/scripts/runs/shakedown_001/capture \
  --output experiments/03-31-26/scripts/runs/shakedown_001/results \
  --capture-format logits \
  --conditions true_self,shuffled,null_control \
  --levels L3
```

```bash
# Full 18-cell experiment (only after shakedown passes and M_a > 0 at L3)
python experiments/03-31-26/scripts/run_experiment.py \
  --tsv experiments/03-31-26/prompts/mirror_prompts.tsv \
  --run-name run_001

# Full analysis
python experiments/03-31-26/scripts/mirror_analysis.py \
  --captures experiments/03-31-26/scripts/runs/run_001/capture \
  --output experiments/03-31-26/scripts/runs/run_001/results \
  --capture-format logits
```

## Interpretation

| Result | Meaning |
|--------|---------|
| M_a > 0 across levels | Model routing differs on true-self versus shuffled self-data |
| M_val > M_entry | The difference is valuation, not access |
| M_deltanet > M_attn | Signal is more consistent with recurrent-state dynamics than attention-only effects |
| M_a scales L1 < L2 < L3 | Secondary result: mirror effect tracks category gradient after the within-level true_self vs shuffled effect is established |
| M_a ≈ 0 | Mirror is a window. No identity-specific response. |

## Run Policy

- Primary claim: within-level `true_self` vs `shuffled`
- Secondary claim: level scaling `L1 < L2 < L3`
- Primary run: one deterministic generation per cell, fixed `--seed 42`
- Follow-up robustness runs, if needed, should use separate seeds such as `43` and `44` and be reported as distinct runs
