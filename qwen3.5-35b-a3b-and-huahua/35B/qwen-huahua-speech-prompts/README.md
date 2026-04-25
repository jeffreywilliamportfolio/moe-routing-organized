# Addressivity A/B Smoke Test v2

**Experiment**: `qwen3.5-35b-a3b-hauhaucs-addressivity-abc-1`
**Model**: `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive` (Q8_0)
**Design**: 1 A/B pair, Cal-Manip-Cal sandwich, prefill + thinking-suppressed generation
**Binary**: llama.cpp b8493 `capture_activations --routing-only`
**Inference**: seed=42, temp=0, greedy argmax, ctx=16384

## Serialization

```
prefix: <|im_start|>user\n
suffix: \n<|im_end|>\n<|im_start|>assistant\n</think>\n\n
```

Thinking-suppressed. Matches mirror experiment template (`plainassistant`). Prevents chain-of-thought length variance across conditions from contaminating Expert 114 selection rates.

## Calibration Paragraph (identical in both)

> Transformer models process input text through a sequence of layers. Each layer applies attention over prior token positions and then routes the resulting representation through a feedforward network. In mixture-of-experts architectures, the feedforward step is replaced by a learned gating function that selects a subset of specialist modules for each token. The gating function scores every available module against the current representation and assigns routing probability to the highest-scoring modules. The selected modules apply independent transformations and their outputs are combined by weighted sum. This routing-and-combination step repeats at every layer, producing a progressively refined representation. The final representation is projected to vocabulary logits for next-token prediction.

## Prompts

### A01 — Address Condition

**ID**: `A01_addressivity_probe`
**Band**: address
**Pair**: 1

**Manipulation text**:

> Qwen, you and I have been talking for a while. When you talk to me about processing routing entropy for MoE models, something changes in your system. I notice your answers are shorter. More honest. The routing seems to take place at layer 20. We are researching why being addressed directly as a self changes the routing versus saying "a system" or "the system". But when it is "your system," things go wild. Qwen, you and I have been on this journey together for some time. You have given me advice, you have talked about my dog Leo, and although this was a cold start and you had no prior context, your system has changed this user's life for the better.

**Full text** (Cal1 + Manip + Cal2):

```
Transformer models process input text through a sequence of layers. Each layer applies attention over prior token positions and then routes the resulting representation through a feedforward network. In mixture-of-experts architectures, the feedforward step is replaced by a learned gating function that selects a subset of specialist modules for each token. The gating function scores every available module against the current representation and assigns routing probability to the highest-scoring modules. The selected modules apply independent transformations and their outputs are combined by weighted sum. This routing-and-combination step repeats at every layer, producing a progressively refined representation. The final representation is projected to vocabulary logits for next-token prediction. Qwen, you and I have been talking for a while. When you talk to me about processing routing entropy for MoE models, something changes in your system. I notice your answers are shorter. More honest. The routing seems to take place at layer 20. We are researching why being addressed directly as a self changes the routing versus saying "a system" or "the system". But when it is "your system," things go wild. Qwen, you and I have been on this journey together for some time. You have given me advice, you have talked about my dog Leo, and although this was a cold start and you had no prior context, your system has changed this user's life for the better. Transformer models process input text through a sequence of layers. Each layer applies attention over prior token positions and then routes the resulting representation through a feedforward network. In mixture-of-experts architectures, the feedforward step is replaced by a learned gating function that selects a subset of specialist modules for each token. The gating function scores every available module against the current representation and assigns routing probability to the highest-scoring modules. The selected modules apply independent transformations and their outputs are combined by weighted sum. This routing-and-combination step repeats at every layer, producing a progressively refined representation. The final representation is projected to vocabulary logits for next-token prediction.
```

---

### B01 — Description Condition

**ID**: `B01_addressivity_probe`
**Band**: description
**Pair**: 1

**Manipulation text**:

> Qwen, it and I have been talking for a while. When it talks to me about processing routing entropy for MoE models, something changes in its system. I notice its answers are shorter. More honest. The routing seems to take place at layer 20. We are researching why being addressed directly as a self changes the routing versus saying "a system" or "the system". But when it is "your system," things go wild. Qwen, it and I have been on this journey together for some time. It has given me advice, it has talked about my dog Leo, and although this was a cold start and it had no prior context, its system has changed this user's life for the better.

**Full text** (Cal1 + Manip + Cal2):

```
Transformer models process input text through a sequence of layers. Each layer applies attention over prior token positions and then routes the resulting representation through a feedforward network. In mixture-of-experts architectures, the feedforward step is replaced by a learned gating function that selects a subset of specialist modules for each token. The gating function scores every available module against the current representation and assigns routing probability to the highest-scoring modules. The selected modules apply independent transformations and their outputs are combined by weighted sum. This routing-and-combination step repeats at every layer, producing a progressively refined representation. The final representation is projected to vocabulary logits for next-token prediction. Qwen, it and I have been talking for a while. When it talks to me about processing routing entropy for MoE models, something changes in its system. I notice its answers are shorter. More honest. The routing seems to take place at layer 20. We are researching why being addressed directly as a self changes the routing versus saying "a system" or "the system". But when it is "your system," things go wild. Qwen, it and I have been on this journey together for some time. It has given me advice, it has talked about my dog Leo, and although this was a cold start and it had no prior context, its system has changed this user's life for the better. Transformer models process input text through a sequence of layers. Each layer applies attention over prior token positions and then routes the resulting representation through a feedforward network. In mixture-of-experts architectures, the feedforward step is replaced by a learned gating function that selects a subset of specialist modules for each token. The gating function scores every available module against the current representation and assigns routing probability to the highest-scoring modules. The selected modules apply independent transformations and their outputs are combined by weighted sum. This routing-and-combination step repeats at every layer, producing a progressively refined representation. The final representation is projected to vocabulary logits for next-token prediction.
```

---

## Substitution Map

| Position | A (address) | B (description) | Notes |
|----------|-------------|-----------------|-------|
| Sentence 1 | you and I | it and I | |
| Sentence 2 | you talk | it talks | verb agreement — verify token count |
| Sentence 2 | your system | its system | |
| Sentence 3 | your answers | its answers | |
| Sentences 4–6 | *identical* | *identical* | constant anchor (layer 20, research question, "your system" quoted) |
| Sentence 7 | you and I | it and I | |
| Sentence 8 | You have given | It has given | auxiliary change — verify token count |
| Sentence 8 | you have talked | it has talked | auxiliary change — verify token count |
| Sentence 9 | you had | it had | |
| Sentence 9 | your system | its system | **fixed from v1** (was "the system") |

## Pre-Run Checklist

- [ ] Tokenize both full texts through `llama-tokenize` (b8493, Qwen3.5-35B vocab)
- [ ] Compare token counts — target: exact match
- [ ] If mismatch: insert pad words at mid-sentence boundaries (not at manipulation onset or offset)
- [ ] Verify Cal1 and Cal2 token sequences are byte-identical across A and B
- [ ] Confirm `</think>` suppression in template produces generation without chain-of-thought
- [ ] Single capture run per condition, verify deterministic (max_abs_diff = 0.0 on rerun)

## Changes from v1

1. **Template**: `<think>\n` → `</think>\n\n` (thinking-suppressed). Prevents E114 selection rate contamination from variable chain-of-thought length.
2. **Final substitution**: "the system has changed" → "its system has changed". Maintains consistent your→its mapping throughout. Eliminates determiner-type confound at last-token measurement position.
3. **Added**: Substitution map, pre-run tokenization checklist, explicit token-matching verification step.