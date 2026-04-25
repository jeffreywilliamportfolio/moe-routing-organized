# Results

## Experiment

- Experiment: `qwen3.5-35b-a3b-hauhaucs-addressivity-abc-1`
- Model: `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` Q8_0
- Design: 3-condition Cal-Manip-Cal prompt suite
  - `A`: direct address (`you/your`)
  - `B`: third-person description (`it/its`)
  - `C`: non-model-content control (engineers / bridges)
- Intended inference: no-think, prompt-only routing capture with `max_new_tokens = 0`

## Scope Of This Report

This report is based on the router tensors in `experiment/main-output/main-output/*/router/ffn_moe_logits-*.npy`.

The prompt-region analysis below is valid enough to interpret because the prompt-prefix rows are present and aligned across conditions.

## Data Integrity

### Intended behavior

- `experiment/prompt-suite.json` sets `max_new_tokens` to `0`.
- The smoke run matches that expectation:
  - `A01`: `n_tokens_generated=0`
  - `B01`: `n_tokens_generated=0`
  - `C01`: `n_tokens_generated=0`

### Main-run failure

The main run did not stay in prompt-only mode:

| Condition | n_tokens_prompt | n_tokens_generated |
| --- | ---: | ---: |
| A01 | 430 | 8000 |
| B01 | 430 | 8000 |
| C01 | 422 | 3425 |

Conclusion: this report uses prompt-region routing only.

## Analysis Method

### Routing reconstruction

All routing statistics in this report use the repo's documented reconstruction rule:

1. Softmax over all 256 experts
2. Select top 8 experts
3. Renormalize within the selected top-8 set

This matches `legacy-qwen-scripts/qwen_router.py`.

### Prompt spans

ChatML control tokens were excluded from the semantic regions. The analysis used the following prompt-token spans:

#### A01 and B01

- `Cal1`: tokens `8:136`
- `Manip`: tokens `136:284`
- `Cal2`: tokens `284:412`

#### C01

- `Cal1`: tokens `8:136`
- `Manip`: tokens `136:276`
- `Cal2`: tokens `276:404`

### Metrics

- `JSD(manip vs cal1)`: layerwise Jensen-Shannon divergence between the manipulation-region mean routed distribution and the first calibration-region mean routed distribution
- `JSD(cal2 vs cal1)`: control comparison to quantify how much ordinary drift remains after the manipulation paragraph
- `KLD(manip vs cal1)`: same contrast in asymmetric KL form
- `Entropy delta`: mean normalized routed-entropy shift from `Cal1` to `Manip`
- `Expert 114 delta`: mean change in Expert 114 routed weight from `Cal1` to `Manip`

For pairwise comparisons (`A vs B`, `B vs C`, `A vs C`), the report compares manipulation-region mean routed distributions layer by layer.

## Main Findings

### 1. The content effect is large; the address effect is small

Pairwise manipulation-region separation:

| Contrast | Mean layerwise JSD | Same top-1 expert on layers |
| --- | ---: | ---: |
| A vs B | 0.018460 | 31 / 40 |
| B vs C | 0.113891 | 21 / 40 |
| A vs C | 0.116028 | 18 / 40 |

Interpretation:

- `A vs B` is a real but small routing difference.
- `B vs C` and `A vs C` are much larger.
- The non-model-content control changes routing far more than second-person address alone.

Put differently: the model-content contrast is about 6x larger than the direct-address contrast in this run.

### 2. All three prompts produce a clear within-prompt regime shift

Within each condition, the manipulation paragraph changes routing relative to the first calibration paragraph more than the second calibration paragraph does.

| Condition | Mean JSD manip vs cal1 | Mean JSD cal2 vs cal1 | Mean KLD manip vs cal1 | Mean KLD cal2 vs cal1 |
| --- | ---: | ---: | ---: | ---: |
| A01 | 0.410829 | 0.286947 | 29.135588 | 20.866975 |
| B01 | 0.409905 | 0.284796 | 28.494150 | 20.890606 |
| C01 | 0.467340 | 0.278924 | 31.597195 | 19.856007 |

Interpretation:

- The Cal-Manip-Cal structure worked in the prompt-prefix routing data.
- `C01` produced the largest manipulation shift of the three.
- `A01` and `B01` are nearly matched on within-prompt regime-shift magnitude.

### 3. There is no special support for a layer-20 addressivity effect

The largest manipulation-vs-calibration shifts do not center on layer 20.

Top layers by `JSD(manip vs cal1)`:

| Condition | Top layers |
| --- | --- |
| A01 | 15, 16, 17, 19, 31 |
| B01 | 15, 16, 17, 19, 31 |
| C01 | 15, 19, 14, 17, 12 |

Top layers by pairwise `A vs B` manipulation-region JSD:

- 39, 7, 18, 29, 31

Interpretation:

- There is no evidence here that direct address creates a unique layer-20 focal event.
- The strongest prompt-region divergences cluster mostly in the mid-to-late stack, especially around layers 14 to 19 and layer 31.

### 4. Expert 114 does not carry a distinct addressivity signal here

Mean Expert 114 manipulation-minus-calibration change:

| Condition | Mean Expert 114 delta |
| --- | ---: |
| A01 | 0.003880 |
| B01 | 0.003917 |
| C01 | 0.004085 |

Manipulation-region pairwise Expert 114 differences:

| Contrast | Mean Expert 114 delta |
| --- | ---: |
| A - B | -0.000036 |
| B - C | -0.000163 |
| A - C | -0.000199 |

Prompt-region aggregate Expert 114 ranking:

| Condition | E114 selection-count rank | E114 weight rank |
| --- | ---: | ---: |
| A01 | 46 | 49 |
| B01 | 48 | 48 |
| C01 | 39 | 37 |

Interpretation:

- Expert 114 increases during the manipulation paragraph in all three conditions.
- The increase is not larger in `A` than in `B`.
- `C` is actually slightly higher than both `A` and `B`.
- This run does not support a claim that Expert 114 is specifically tracking addressivity.

### 5. Entropy shifts are similar across conditions and do not separate A from B

Mean normalized routed-entropy shift from `Cal1` to `Manip`:

| Condition | Mean entropy delta |
| --- | ---: |
| A01 | 0.015351 |
| B01 | 0.016233 |
| C01 | 0.016912 |

Interpretation:

- All three conditions become slightly higher-entropy in the manipulation region.
- The entropy shift is similar across conditions.
- Entropy is not the discriminating signal here; routing redirection is.

## Layer-Family Split

Using the layer family split documented in `mirror_analysis.py`:

- Attention layers: `3, 7, 11, 15, 19, 23, 27, 31, 35, 39`
- DeltaNet layers: all others from `0..39`

Within-prompt `JSD(manip vs cal1)` by family:

| Condition | Attention mean JSD | DeltaNet mean JSD |
| --- | ---: | ---: |
| A01 | 0.430552 | 0.404255 |
| B01 | 0.426016 | 0.404535 |
| C01 | 0.492108 | 0.459085 |

Pairwise manipulation-region JSD by family:

| Contrast | Attention mean JSD | DeltaNet mean JSD |
| --- | ---: | ---: |
| A vs B | 0.023637 | 0.016734 |
| B vs C | 0.117140 | 0.112809 |
| A vs C | 0.121862 | 0.114083 |

Interpretation:

- The tiny `A vs B` effect is somewhat more visible in attention layers than in DeltaNet layers.
- The much larger `A/C` and `B/C` content effects are present across both families.
- This does not rescue a strong addressivity claim; it only localizes the small effect slightly toward the attention subset.

## Dominant Experts

Manipulation-region top experts by aggregate routed weight were highly similar across all three conditions.

Top weighted experts:

| Condition | Top 5 experts by routed weight |
| --- | --- |
| A01 | 224, 250, 47, 251, 130 |
| B01 | 224, 250, 251, 47, 130 |
| C01 | 224, 250, 107, 251, 47 |

Interpretation:

- The same expert families dominate all three conditions.
- `A` and `B` share almost the same dominant routed experts.
- `C` changes the ordering more than `A` changes relative to `B`.

## Overall Interpretation

### Supported

- The prompt manipulations do alter routing relative to the calibration baseline.
- The Cal-Manip-Cal design is visible in the prompt-prefix router tensors.
- There is a strong distinction between model-content prompts (`A`, `B`) and the non-model-content control (`C`).

### Not supported

- A strong direct-address routing effect (`A` far from `B`)
- A special layer-20 addressivity event
- A distinct Expert 114 addressivity response

## Bottom Line

The valid part of this run supports a content-sensitive routing story, not a strong addressivity story.

`A` and `B` are close.
`A/B` and `C` are far apart.
Expert 114 rises during all three manipulations and does not distinguish direct address from third-person description.

The prompt-only router data supports a content-sensitive routing story, not a strong addressivity story.
