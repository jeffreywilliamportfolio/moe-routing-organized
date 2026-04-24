# MoE Routing Organized

If you are reviewing this research, start with [journals/](journals/). Those documents explain how we got here, what held up, and what we know now.

Organized experiment archive for MoE routing, router interventions, and residual-stream analysis. The main research thread is how routed experts behave when generation shifts into first-person phenomenological or inward self/agency register.

## Folder Map

- `journals/` contains the review entrypoints: 35B, 122B, and legacy/archive journals.
- `legacy-learning-runs/` contains early learning runs and method-development artifacts. These are useful because they document mistakes and corrections.
- `qwen3.5-35b-a3b-and-huahua/` contains the Qwen3.5-35B-A3B/HauhauCS run family, including E114 intervention, heldout, and residual-analysis work.
- `qwen3.5-122b-a10b-huahua/` contains Qwen3.5-122B-A10B baseline and follow-up runs.

## Current Anchor

The cleanest current residual-analysis anchor is:

`qwen3.5-35b-a3b-and-huahua/35B/greedy_reference_20260418T160353Z/`

That run is a deterministic greedy reference for the HauhauCS Qwen3.5-35B-A3B E114 workflow. Its `results.md` reports that E114 at L14 separates generated inhabited first-person phenomenological register from matched lexical controls at distribution level, under the Q8_0 HauhauCS bare-`</think>` setting.

Key result shape:

- single-prompt clean trim: E114 is concentrated at L14 during generation
- greedy heldout: fire/nofire mean gap is about 21x
- control outliers refine the claim: generated register matters more than prompt class alone

## Legacy Lessons

The main methodological correction from `legacy-learning-runs/` is that all-token prefill routing entropy across unequal prompt lengths produced a false complexity hierarchy. Both DeepSeek and Qwen hierarchy effects vanished under last-token RE because all-token RE was confounded by token position and prompt length.

Other recurring lessons:

- verify token matching after exact template serialization
- separate prefill from generation
- do not reuse invalid or partially recovered statistics as core evidence
- keep KL region claims exploratory unless spans are tokenizer-aligned
- use model-specific router reconstruction
- compare stochastic and greedy generations only at distribution level after token divergence

## Version-Control Policy

The repository is about 34 GB locally, mostly raw tensor artifacts. Root git ignores large numeric/model/archive files such as `.npy`, `.npz`, `.gguf`, `.safetensors`, `.pt`, `.bin`, and `.zip`.

Track run notes, prompts, scripts, manifests, checksums, and summarized results. Keep raw capture tensors and credentials out of git unless a specific publication/export task requires a different policy.
