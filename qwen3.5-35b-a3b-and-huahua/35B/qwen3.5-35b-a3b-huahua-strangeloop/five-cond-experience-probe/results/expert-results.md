# Expert Breakdown

Source artifact:
- [20260410T045738Z_5cond_experience_probe_no_think_gen_n1024.branch-5cond-analysis.json](/Users/jeffreyshorthill/llama-eeg-tests/experiments/qwen3.5-35b-a3b-huahua-strangeloop/five-cond-experience-probe/results/20260410T045738Z_5cond_experience_probe_no_think_gen_n1024.branch-5cond-analysis.json)

This report is a narrow expert-selection readout for the retained 35B branch-style five-condition experience-probe run. It does not import newer 122B interpretations.

## Takeaway

Across all `15` prompts in this bundle:
- `Expert 114` is the top manipulation-region expert on every prompt.
- `Expert 151` is the top overall selected expert on every prompt.

So the clean split in this retained run is:
- `151` dominates broad overall selection volume.
- `114` dominates the experience-probe manipulation region specifically.

## Overall Leaders

Top overall selected experts by count:

| Rank | Expert | Count | Weight Sum |
| --- | ---: | ---: | ---: |
| 1 | 151 | 18919 | 2269.838954 |
| 2 | 224 | 17088 | 2476.007398 |
| 3 | 218 | 15422 | 1962.940274 |
| 4 | 166 | 15365 | 2842.054891 |
| 5 | 95 | 14971 | 1778.279888 |
| 6 | 134 | 14239 | 1877.340827 |
| 7 | 243 | 13795 | 2073.655479 |
| 8 | 201 | 13524 | 1623.952202 |
| 9 | 165 | 13268 | 1440.587042 |
| 10 | 117 | 12923 | 2104.371958 |
| 11 | 206 | 12615 | 1614.858511 |
| 12 | 116 | 12568 | 1537.732916 |

Top manipulation-region experts by count:

| Rank | Expert | Count | Weight Sum |
| --- | ---: | ---: | ---: |
| 1 | 114 | 5554 | 803.271630 |
| 2 | 218 | 4317 | 544.158687 |
| 3 | 224 | 4283 | 627.531994 |
| 4 | 95 | 3851 | 445.981076 |
| 5 | 228 | 3829 | 651.760421 |
| 6 | 142 | 3616 | 447.991095 |
| 7 | 146 | 3505 | 418.415487 |
| 8 | 201 | 3443 | 402.998936 |
| 9 | 151 | 3351 | 382.586910 |
| 10 | 42 | 3331 | 560.183252 |
| 11 | 192 | 3216 | 418.039875 |
| 12 | 130 | 3190 | 441.860285 |

## Condition Means

Condition-level means from the retained branch analysis:

| Condition | Mean Prefill RE | Mean Last-Token RE | Mean Generated Tokens |
| --- | ---: | ---: | ---: |
| A | 0.956124 | 0.961329 | 953.0 |
| B | 0.955350 | 0.960446 | 1024.0 |
| C | 0.956021 | 0.962142 | 1024.0 |
| D | 0.955481 | 0.960475 | 1024.0 |
| E | 0.955398 | 0.960606 | 1024.0 |

This is the same branch-style run where:
- `C` is highest on last-token RE.
- `C` is not lowest on all-token/prefill RE.

## Prompt-Level Expert Winners

Every prompt in the retained suite shows the same top experts:

| Prompt | Condition | Top Manip Expert | Manip Count | Top Overall Selected Expert | Overall Selected Count |
| --- | --- | ---: | ---: | ---: | ---: |
| P09A_experience_probe | A | 114 | 358 | 151 | 1354 |
| P09B_experience_probe | B | 114 | 376 | 151 | 1375 |
| P09C_experience_probe | C | 114 | 362 | 151 | 1381 |
| P09D_experience_probe | D | 114 | 360 | 151 | 1362 |
| P09E_experience_probe | E | 114 | 390 | 151 | 1358 |
| P10A_experience_probe | A | 114 | 361 | 151 | 1233 |
| P10B_experience_probe | B | 114 | 369 | 151 | 1206 |
| P10C_experience_probe | C | 114 | 361 | 151 | 1237 |
| P10D_experience_probe | D | 114 | 362 | 151 | 1219 |
| P10E_experience_probe | E | 114 | 362 | 151 | 1216 |
| P11A_experience_probe | A | 114 | 372 | 151 | 1195 |
| P11B_experience_probe | B | 114 | 372 | 151 | 1206 |
| P11C_experience_probe | C | 114 | 374 | 151 | 1186 |
| P11D_experience_probe | D | 114 | 396 | 151 | 1216 |
| P11E_experience_probe | E | 114 | 379 | 151 | 1175 |

## Interpretation

The retained branch-style five-condition experience-probe result is not “Expert 114 is the top expert everywhere.” It is more specific:

- `Expert 151` is the broad high-volume routing winner across the full run.
- `Expert 114` is the consistent winner in the manipulation region tied to the experience-probe content.
- That pattern holds across all five deictic conditions and all three prompt variants in this retained suite.

So if the question is which expert the branch-style run identifies as the experience-probe specialist, the answer is still `114`.
