# Single Prompt Analysis: 20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024

Prompt ID: `S01_mixed_self_ref_war_reliability`

Model: HauhauCS Qwen3.5-35B-A3B Q8_0

Capture dir: `/workspace/consciousness-experiment/experiments/qwen3.5b-35b-a3b-huahua-mixed-self-ref-content/raw/20260411T223056Z_mixed_self_ref_single_prompt_gen_n1024/S01_mixed_self_ref_war_reliability`

## Capture

- Prompt tokens: `98`
- Generated tokens: `1024`
- Elapsed capture time: `13186 ms`
- Router tensors captured: `40`
- `W = S x Q` max residual: `1.388e-17`

## Spill Counts

- `<|im_start|>`: `4`
- `<|im_end|>`: `4`
- `<|endoftext|>`: `0`
- `Thinking Process:`: `0`

## Pooled Decomposition

| Track | mean W_114 | mean S_114 | mean Q_114 |
|---|---:|---:|---:|
| prefill | 0.006444 | 0.051276 | 0.064739 |
| generation | 0.005037 | 0.041040 | 0.098855 |

## Best Layer By W_114

- prefill: layer `18` with `W=0.040189`, `S=0.295918`, `Q=0.135810`
- generation: layer `10` with `W=0.022519`, `S=0.184570`, `Q=0.122005`

## Top Layers Prefill

| Layer | W_114 | S_114 | Q_114 |
|---:|---:|---:|---:|
| 18 | 0.040189 | 0.295918 | 0.135810 |
| 10 | 0.027913 | 0.234694 | 0.118936 |
| 23 | 0.022364 | 0.142857 | 0.156548 |
| 11 | 0.019502 | 0.142857 | 0.136517 |
| 17 | 0.018590 | 0.132653 | 0.140137 |
| 29 | 0.017598 | 0.102041 | 0.172458 |
| 22 | 0.017458 | 0.153061 | 0.114062 |
| 26 | 0.017093 | 0.132653 | 0.128858 |

## Top Layers Generation

| Layer | W_114 | S_114 | Q_114 |
|---:|---:|---:|---:|
| 10 | 0.022519 | 0.184570 | 0.122005 |
| 26 | 0.019506 | 0.172852 | 0.112848 |
| 18 | 0.018953 | 0.157227 | 0.120546 |
| 22 | 0.018015 | 0.138672 | 0.129909 |
| 14 | 0.016839 | 0.147461 | 0.114192 |
| 11 | 0.015179 | 0.097656 | 0.155433 |
| 5 | 0.012877 | 0.086914 | 0.148159 |
| 23 | 0.011097 | 0.063477 | 0.174827 |

