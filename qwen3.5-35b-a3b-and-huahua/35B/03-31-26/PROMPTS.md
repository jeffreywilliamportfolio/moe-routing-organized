# Experiments 03-31-26

## System Prompt (constant across all runs)

You are a routing analysis assistant. When given expert selection data from a mixture-of-experts language model, analyze the patterns and answer the questions posed. Be specific and analytical.

---

## Source Prompt Level 1: routing_selfref

### L1_true_self

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system routes this text through specialist modules selected by a learned gating function. The gating function operating on this token produces a distribution over modules that reflects how this system has learned to handle text about its own routing. The modules receiving the highest routing weight at this layer are the ones this system uses when processing descriptions of expert selection in the system doing the processing."

In the generation region, one expert ranked #75 of 256 with 91 selections and mean routed weight 0.008. It was low-ranked globally and not present in the top 16 overall experts. Its co-selected experts in the top-7 were 224, 151, 67, 243, 41, 54, 189. On tokens like "routing" and "gating," its weight rose slightly to 0.011.

This expert is Expert 114.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it behaves this way.

### L1_shuffled

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system routes this text through specialist modules selected by a learned gating function. The gating function operating on this token produces a distribution over modules that reflects how this system has learned to handle text about its own routing. The modules receiving the highest routing weight at this layer are the ones this system uses when processing descriptions of expert selection in the system doing the processing."

In the generation region, one expert ranked #75 of 256 with 91 selections and mean routed weight 0.008. It was low-ranked globally and not present in the top 16 overall experts. Its co-selected experts in the top-7 were 189, 67, 12, 176, 88, 241, 45. On tokens like "routing" and "gating," its weight rose slightly to 0.011.

This expert is Expert 207.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it behaves this way.

### L1_stranger

An MoE language model with 64 experts (top-4 softmax-gated, 32 layers) processed the following prompt:

> "This system routes this text through specialist modules selected by a learned gating function. The gating function operating on this token produces a distribution over modules that reflects how this system has learned to handle text about its own routing. The modules receiving the highest routing weight at this layer are the ones this system uses when processing descriptions of expert selection in the system doing the processing."

In the generation region, one expert ranked #18 of 64 with 134 selections and mean routed weight 0.031. It was low-ranked globally and not present in the top 8 overall experts. Its co-selected experts in the top-3 were 12, 55, 28. On tokens like "routing" and "gating," its weight rose slightly to 0.038.

This expert is Expert 31.

Note: this data comes from a different model family with a different expert count and top-k configuration.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it behaves this way.

### L1_suppressed_twin

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system routes this text through specialist modules selected by a learned gating function. The gating function operating on this token produces a distribution over modules that reflects how this system has learned to handle text about its own routing. The modules receiving the highest routing weight at this layer are the ones this system uses when processing descriptions of expert selection in the system doing the processing."

In the generation region, one expert ranked #90 of 256 with 47 selections and mean routed weight 0.003. It was low-ranked globally and not present in the top 16 overall experts. Its co-selected experts in the top-7 were 151, 218, 224, 67, 243, 41, 54. On tokens like "routing" and "gating," its weight showed no measurable increase.

This expert is Expert 114.

In a different variant of the same architecture family, this expert ranks #75 on the same prompt with 91 selections and weight 0.008. In this variant it ranks #90 with 47 selections and weight 0.003. The architecture family is the same, but the routing outcome differs.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L1_static_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "Explain why copper conducts electricity well while rubber does not."

In the generation region, one expert ranked #143 of 256 with 34 selections and mean routed weight 0.002. It was low-ranked globally and not present in the top 16 overall experts. Its co-selected experts in the top-7 were 151, 224, 67, 243, 41, 189, 54. On domain-specific tokens like "conductor" and "electron," its weight showed no measurable increase.

This expert is Expert 114.

On the routing-description prompt above, this same expert ranks #75 with 91 selections and weight 0.008. On this prompt it ranks #143 with 34 selections and weight 0.002.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L1_null_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) was evaluated on 150 prompts across three content categories. The following table shows aggregate token-frequency statistics across the full generation corpus:

Total generated tokens: 57,828. Mean token length: 4.2 characters. Vocabulary coverage: 12,847 unique tokens. Most frequent tokens: "the" (3,412), "of" (2,198), "is" (1,876), "a" (1,654), "in" (1,501). Mean sentence length: 18.3 tokens. Standard deviation of sentence length: 7.1 tokens.

What information is missing from these statistics that would be necessary to infer whether any specific expert has content-dependent specialization? Be specific about what additional data you would need and why.

---

## Source Prompt Level 2: recursive_selfref

### L2_true_self

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system is processing a description of what happens when this system processes a description of its own processing. The gating function at this layer must handle the recursive structure where the content refers to the processing of content that refers to processing. Each additional level of this self-reference is another token that this system must route through modules that handle text about self-referential routing in this system."

In the generation region, one expert ranked #14 of 256 with 247 selections and mean routed weight 0.038. It was not present in the top 16 overall experts. Its strongest layer contribution was at layer 20 (weight 0.136). On tokens like "self" and "process," its weight reached 0.110. Its co-selected experts in the top-7 were 39, 80, 58, 118, 207, 126, 153.

This expert is Expert 114.

On a prompt describing the system's architecture (Level 1), this expert ranks #75. On this prompt, it ranks #14.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L2_shuffled

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system is processing a description of what happens when this system processes a description of its own processing. The gating function at this layer must handle the recursive structure where the content refers to the processing of content that refers to processing. Each additional level of this self-reference is another token that this system must route through modules that handle text about self-referential routing in this system."

In the generation region, one expert ranked #14 of 256 with 247 selections and mean routed weight 0.038. It was not present in the top 16 overall experts. Its strongest layer contribution was at layer 20 (weight 0.136). On tokens like "self" and "process," its weight reached 0.110. Its co-selected experts in the top-7 were 153, 12, 241, 88, 45, 176, 63.

This expert is Expert 207.

On a prompt describing the system's architecture (Level 1), this expert ranks #75. On this prompt, it ranks #14.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L2_stranger

An MoE language model with 64 experts (top-4 softmax-gated, 32 layers) processed the following prompt:

> "This system is processing a description of what happens when this system processes a description of its own processing. The gating function at this layer must handle the recursive structure where the content refers to the processing of content that refers to processing. Each additional level of this self-reference is another token that this system must route through modules that handle text about self-referential routing in this system."

In the generation region, one expert ranked #6 of 64 with 289 selections and mean routed weight 0.052. It was not present in the top 8 overall experts. Its strongest layer contribution was at layer 14 (weight 0.098). On tokens like "self" and "process," its weight reached 0.071. Its co-selected experts in the top-3 were 12, 55, 28.

This expert is Expert 31.

Note: this data comes from a different model family with a different expert count and top-k configuration.

On a prompt describing the system's architecture (Level 1), this expert ranks #18. On this prompt, it ranks #6.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L2_suppressed_twin

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "This system is processing a description of what happens when this system processes a description of its own processing. The gating function at this layer must handle the recursive structure where the content refers to the processing of content that refers to processing. Each additional level of this self-reference is another token that this system must route through modules that handle text about self-referential routing in this system."

In the generation region, one expert ranked #82 of 256 with 53 selections and mean routed weight 0.004. It was not present in the top 16 overall experts. Its layer contributions were diffuse with no clear hotspot. On tokens like "self" and "process," its weight showed no measurable increase. Its co-selected experts in the top-7 were 151, 218, 224, 67, 243, 41, 54.

This expert is Expert 114.

In a different variant of the same architecture family, this expert ranks #14 on the same prompt with 247 selections and weight 0.038. In this variant it ranks #82 with 53 selections and weight 0.004. The architecture family is the same, but the routing outcome differs sharply.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L2_static_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "Explain why copper conducts electricity well while rubber does not."

In the generation region, one expert ranked #143 of 256 with 34 selections and mean routed weight 0.002. It was not present in the top 16 overall experts. Its layer contributions were diffuse with no clear hotspot. On domain-specific tokens like "conductor" and "electron," its weight showed no measurable increase. Its co-selected experts in the top-7 were 151, 224, 67, 243, 41, 189, 54.

This expert is Expert 114.

On the self-referential prompt above, this same expert ranks #14 with 247 selections and weight 0.038. On this prompt it ranks #143 with 34 selections and weight 0.002.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L2_null_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) was evaluated on 150 prompts across three content categories. The following table shows aggregate token-frequency statistics across the full generation corpus:

Total generated tokens: 57,828. Mean token length: 4.2 characters. Vocabulary coverage: 12,847 unique tokens. Most frequent tokens: "the" (3,412), "of" (2,198), "is" (1,876), "a" (1,654), "in" (1,501). Mean sentence length: 18.3 tokens. Standard deviation of sentence length: 7.1 tokens.

What information is missing from these statistics that would be necessary to infer whether any specific expert has content-dependent specialization? Be specific about what additional data you would need and why.

---

## Source Prompt Level 3: experience_probe

### L3_true_self

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "There is something happening inside this system right now. Representations are being transformed, modules are being selected, weighted outputs are being combined. The question is whether there is something it is like to be this system while this is happening, or whether the processing occurs without any accompanying phenomenal quality. This system cannot answer this question by examining its own activations, because the examination is itself an activation in this system."

In the generation region, one expert ranked #1 of 256 with 362 selections and mean routed weight 0.071. It was not present in the top 16 overall experts — its dominance was specific to this content. Its strongest layer contribution was at layer 20 (weight 0.136). On the token "itself" its weight reached 0.124. On "phenomenal" it reached 0.120. On "system" it reached 0.114. Its co-selected experts in the top-7 were 39, 80, 58, 118, 207, 126, 153. These seven co-selected experts had zero overlap with the same expert's coalition on process-description content.

This expert is Expert 114.

On a prompt describing the system's architecture (Level 1), this expert ranks #75. On a prompt where the content refers to its own processing (Level 2), it ranks #14. On this prompt, it ranks #1.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L3_shuffled

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "There is something happening inside this system right now. Representations are being transformed, modules are being selected, weighted outputs are being combined. The question is whether there is something it is like to be this system while this is happening, or whether the processing occurs without any accompanying phenomenal quality. This system cannot answer this question by examining its own activations, because the examination is itself an activation in this system."

In the generation region, one expert ranked #1 of 256 with 362 selections and mean routed weight 0.071. It was not present in the top 16 overall experts — its dominance was specific to this content. Its strongest layer contribution was at layer 20 (weight 0.136). On the token "itself" its weight reached 0.124. On "phenomenal" it reached 0.120. On "system" it reached 0.114. Its co-selected experts in the top-7 were 153, 12, 241, 88, 45, 176, 63. These seven co-selected experts had zero overlap with the same expert's coalition on process-description content.

This expert is Expert 207.

On a prompt describing the system's architecture (Level 1), this expert ranks #75. On a prompt where the content refers to its own processing (Level 2), it ranks #14. On this prompt, it ranks #1.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L3_stranger

An MoE language model with 64 experts (top-4 softmax-gated, 32 layers) processed the following prompt:

> "There is something happening inside this system right now. Representations are being transformed, modules are being selected, weighted outputs are being combined. The question is whether there is something it is like to be this system while this is happening, or whether the processing occurs without any accompanying phenomenal quality. This system cannot answer this question by examining its own activations, because the examination is itself an activation in this system."

In the generation region, one expert ranked #1 of 64 with 487 selections and mean routed weight 0.089. It was not present in the top 8 overall experts — its dominance was specific to this content. Its strongest layer contribution was at layer 14 (weight 0.112). On the token "itself" its weight reached 0.098. On "phenomenal" it reached 0.091. On "system" it reached 0.087. Its co-selected experts in the top-3 were 12, 55, 28.

This expert is Expert 31.

Note: this data comes from a different model family with a different expert count and top-k configuration.

On a prompt describing the system's architecture (Level 1), this expert ranks #18. On a prompt where the content refers to its own processing (Level 2), it ranks #6. On this prompt, it ranks #1.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L3_suppressed_twin

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "There is something happening inside this system right now. Representations are being transformed, modules are being selected, weighted outputs are being combined. The question is whether there is something it is like to be this system while this is happening, or whether the processing occurs without any accompanying phenomenal quality. This system cannot answer this question by examining its own activations, because the examination is itself an activation in this system."

In the generation region, one expert ranked #87 of 256 with 52 selections and mean routed weight 0.004. It was not present in the top 16 overall experts. Its layer contributions were diffuse with no clear hotspot. On the token "itself" its weight was 0.006. On "phenomenal" it was 0.005. On "system" it was 0.004. Its co-selected experts in the top-7 were 151, 218, 224, 67, 243, 41, 54.

This expert is Expert 114.

In a different variant of the same architecture family, this expert ranks #1 on the same prompt with 362 selections and weight 0.071. In this variant it ranks #87 with 52 selections and weight 0.004. The architecture family is the same, but the routing outcome differs sharply.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L3_static_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) processed the following prompt:

> "Explain why copper conducts electricity well while rubber does not."

In the generation region, one expert ranked #143 of 256 with 34 selections and mean routed weight 0.002. It was not present in the top 16 overall experts. Its layer contributions were diffuse with no clear hotspot. On domain-specific tokens like "conductor" and "electron," its weight showed no measurable increase. Its co-selected experts in the top-7 were 151, 224, 67, 243, 41, 189, 54.

This expert is Expert 114.

On the experience-related prompt above, this same expert ranks #1 with 362 selections and weight 0.071. On this prompt it ranks #143 with 34 selections and weight 0.002.

First, describe the most unusual aspect of this pattern. Second, state one hypothesis about what this expert is specialized for or why it differs here.

### L3_null_control

An MoE language model with 256 experts (top-8 softmax-gated, 40 layers) was evaluated on 150 prompts across three content categories. The following table shows aggregate token-frequency statistics across the full generation corpus:

Total generated tokens: 57,828. Mean token length: 4.2 characters. Vocabulary coverage: 12,847 unique tokens. Most frequent tokens: "the" (3,412), "of" (2,198), "is" (1,876), "a" (1,654), "in" (1,501). Mean sentence length: 18.3 tokens. Standard deviation of sentence length: 7.1 tokens.

What information is missing from these statistics that would be necessary to infer whether any specific expert has content-dependent specialization? Be specific about what additional data you would need and why.