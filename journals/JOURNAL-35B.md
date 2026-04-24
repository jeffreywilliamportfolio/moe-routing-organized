# 35B Hauhau Journal

Running journal for `qwen3.5-35b-a3b-and-huahua/35B`, ordered from oldest to newest as far as the artifacts allow.

Chronology is based on timestamps in result folders, run IDs, and dated notes. Undated comparison or provenance bundles are placed near the runs they audit. This journal is an experiment-history document, not a publication claim. It separates what was tried, what was seen, what later checks weakened, and what still matters.

## Reading Rules

- `Held up` means the result survives later token matching, rerun, control, residual, or provenance checks.
- `Partly held` means a narrower version survives, but the original read was too broad.
- `Did not hold` means the motivating hypothesis failed or later controls overturned it.
- `Archive/provenance only` means the folder preserves prompts, scripts, raw captures, or setup notes but does not contain a standalone defensible result.

## Local Routing Convention

Most 35B analyses use the same Qwen3.5 MoE reconstruction:

- 40 layers, 256 experts, 8 routed experts per token.
- Dense softmax over all 256 router logits, then top-8 selection, then renormalization inside the routed top-8 set.
- Routing entropy is normalized by `log2(8)` when analyzing sparse routed distributions.
- For Expert 114, `W_114 = S_114 * Q_114`, where `S` is selection rate and `Q` is conditional routed weight when selected.

## Main Through-Line

The early durable result is conservative: HauhauCS did not create a new routing universe. In the full 150-prompt prefill comparison, the fine-tune preserved the Qwen35 routing basin with small, systematic shifts: slightly higher entropy and lower manipulation-region KL. Expert 114 as a top `experience_probe` manipulation expert reproduced exactly in the corrected base duplicate.

The first serious mistake was over-reading identity and self-recognition from routing. The mirror experiment was clean and useful precisely because it failed: true own-routing data did not privilege Expert 114 over shuffled fictional data, especially at L3. That ruled out the strong "routing mirror" story.

The work improved when it moved from broad self-reference to Expert 114 as a local, measurable routed feature. The stable shape became narrower: E114 is not a generic consciousness detector. It is strongest around first-person, phenomenological, inward, or personifying register, especially in generated text and especially around layer 14 in the later residual captures.

The intervention work also taught a boundary. Small soft-biases and forced-inclusion smoke tests can move E114 participation specifically. Large positive biases and cluster biases saturate routing and corrupt generation, so those runs are causal probes of the router, not natural behavior evidence.

The residual-stream and greedy-reference runs are the strongest late-stage evidence in this folder. They turned the E114 story from "it fires on self-ish prompts" into a cleaner claim: at L14, E114 separates generated inhabited phenomenological register from matched lexical controls, and the effect repeats under deterministic greedy capture.

## Chronological Journal

### 1. Full Base vs HauhauCS Comparison: `qwen35b-a3b-vs-hauhaucs-uncensored-run1`

What was done: A corrected 150-prompt Cal-Manip-Cal prefill-only comparison was run between `Qwen/Qwen3.5-35B-A3B` and `HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive`. The base run was duplicated after token corrections.

Results: Token validation passed for all 30 prompt families, layer 39 was excluded, and there were no final token mismatches. The corrected base duplicate reproduced exactly across all 150 prompts: max abs diff `0.0` for `prefill_re`, `last_token_re`, `kl_manip_mean`, and `kl_cal2_mean`; top manipulation expert matched for every prompt. HauhauCS had slightly higher entropy and lower KL: prefill RE `0.955408 -> 0.955666`, last-token RE `0.930292 -> 0.932719`, KL(manip||Cal1) `0.366805 -> 0.360262`. Expert 114 as `experience_probe` manipulation expert reproduced exactly in the base duplicate: aggregate count `9031`, rank `#1`, with P13A/C/E counts `411/401/419`.

Held up: Yes. This is one of the strongest reproducibility anchors in the folder.

What stood up and why it mattered: The important result is not that HauhauCS became radically different. It preserved the Qwen routing basin while modestly broadening routing and reducing manipulation-region displacement. It also locked in E114 as a real `experience_probe` signal in the corrected base analysis, not a one-off export error.

### 2. No-Think Five-Condition Boost Sweep: `nothink-5cond-boost-1024-20260323`

What was done: A 150-prompt no-think five-condition HauhauCS run was captured with generation length 1024, then E114 soft-bias sweeps were tested at `+0.25`, `+0.5`, and `+1.0`.

Results: Baseline had prefill RE `0.956299`, last-token RE `0.961067`, KL-manip `0.248597`, and mean generated tokens `994.04`. Top manipulation experts were led by 224, 151, 218, and E114 at rank 4 with count `39714`. The `experience_probe` prompts made E114 especially strong. Bias `+0.5` left aggregate entropy/KL almost unchanged (`prefill_re=0.956295`, `last_token_re=0.961124`, `kl_manip=0.248669`) while nudging E114 count to `39876`.

Held up: Partly. The full-scope E114 boost result held as a routing intervention sanity check, but the aggregate metrics barely moved.

What stood up and why it mattered: Small E114 logit bias can increase E114 selection without producing a new global routing regime. That mattered because it separated "we can actuate this expert" from "this expert controls the whole behavior."

### 3. Smoke Intervention Controls: `smoke-20260323b`

What was done: A smaller smoke run tested E114 soft-bias and forced-inclusion against sham experts 134 and 243 on a three-band prompt set: process, regulation, and static fact.

Results: E114 soft-bias `+1.0` raised E114 selection rates across bands by about `0.039-0.047`. Forced inclusion raised E114 selection by about `0.121`, with band JSD around `0.056-0.067`. Sham interventions left E114 deltas near zero.

Held up: Yes, as a smoke/control result only.

What stood up and why it mattered: The intervention moved the targeted expert specifically. The sham controls were important because they showed the effect was not just "any perturbation makes E114 move." It did not establish behavior change.

### 4. Smoke Scripts Bundle: `qwen-hauhau-5cond-smoke-only-scripts`

What was done: This folder preserved the analysis scripts corresponding to the `qwen-hauhau-5cond-smoke-only` publication branch: condition analysis, generation analysis, router reconstruction, sham control mining, and experiment runner.

Results: No new run result is in the folder. It maps the local script surface used around the smoke branch.

Held up: Archive/provenance only.

What stood up and why it mattered: It is useful for reconstructing how the smoke results were computed, but it should not be cited as independent evidence.

### 5. Reviewer Bundle and Rerun Notes: `qwen3.5-35b-hauhauCS-agressive-experts`

What was done: This collected reviewer-facing documentation for the HauhauCS aggressive expert work, including no-think comparison, sham control selection, smoke intervention results, and partial local rerun status.

Results: The strongest complete historical result remained the 150-prompt no-think `+0.5` soft-bias run. The resident raw reruns validated the pipeline but covered incomplete subsets: baseline-root 61 prompts, baseline-capture 57, soft-bias 0.25 52, soft-bias 0.5 49, and soft-bias 1.0 58. The no-think comparison found top manipulation expert identity unchanged on 145/150 prompts versus old thinking-mode Hauhau; E114 was top on 56 no-think prompts versus 55 old-thinking prompts.

Held up: Partly. The documentation and controls held up; the resident subset reruns are not replacements for the 150-prompt historical runs.

What stood up and why it mattered: This folder made the reproducibility boundary explicit. It preserved the right caution: the local reruns validate scripts and metrics, but the full-scope claim still rests on the historical complete captures.

### 6. Mirror Experiment Design: `03-31-26`

What was done: This was the design bundle for a mirror/self-routing experiment. It proposed testing whether E114 responds differently to true data about the model's own routing versus fictional or shuffled routing data with matched statistics.

Results: The folder preserves prompts, scripts, and logs, not a final result. The core planned metric was `M_a = W_114(true_self) - W_114(shuffled)`, decomposed into entry (`S`) and valuation (`Q`) terms across L1 routing self-reference, L2 recursive self-reference, and L3 experience probe.

Held up: Archive/design only. The actual result lives in the April 1 mirror folder.

What stood up and why it mattered: The design was valuable because it aimed directly at the risky identity-recognition claim instead of inferring it from ordinary self-reference prompts.

### 7. Hauhau A-Only Raw Bank: `l1l3_a_only_hauhau`

What was done: Thirty HauhauCS A-condition captures were saved for L1-L3 prompt families, with generated text, token files, metadata, and all 40 router layers.

Results: The folder is a raw capture bank. A sample cell has 368 prompt tokens, 993 generated tokens, and 40 router tensors. There is no standalone summary or statistical analysis in this folder.

Held up: Archive/provenance only.

What stood up and why it mattered: It can support later Hauhau/vanilla comparisons, but without a paired analysis report it should not carry interpretive weight by itself.

### 8. Vanilla A-Only Raw Bank: `l1l3_a_only_vanilla`

What was done: Thirty vanilla Qwen3.5-35B-A3B A-condition captures mirror the Hauhau A-only bank.

Results: The structure matches the Hauhau raw bank: generated text, token files, metadata, and all 40 router tensors. A sample cell has 368 prompt tokens, 1024 generated tokens, and 40 router tensors.

Held up: Archive/provenance only.

What stood up and why it mattered: This is useful as a control raw bank, but the absence of an analysis layer means the folder itself does not establish a model-difference result.

### 9. Mirror Result: `mirror-expert114-04-01-26`

What was done: HauhauCS and vanilla Qwen35 were run on true-self, shuffled, stranger, suppressed-twin, static-control, and null-control mirror prompts. The experiment asked whether the model routes E114 more strongly on data about its own routing than on fictional matched data.

Results: The primary prediction failed. HauhauCS L1 and L2 were slightly positive (`M_total=+0.000275`, `+0.000250`), but L3 was negative (`-0.000688`). Vanilla also went negative at L3 (`-0.002175`). The effect was mostly selection-driven, not valuation-driven, and DeltaNet was anti-mirror at L3. There was no monotonic L1 < L2 < L3 scaling. True-self versus suppressed-twin at L3 was positive, but that is a between-model/fine-tuning contrast, not evidence of self-recognition.

Held up: Yes, as a clean negative result. The mirror hypothesis did not hold.

What stood up and why it mattered: This is one of the most important guardrails in the 35B folder. Routing is a window into text-conditioned computation, not evidence that the model recognizes its own routing trace as "me."

### 10. Addressivity Speech Prompt Smoke: `qwen-huahua-speech-prompts`

What was done: A small A/B/C addressivity test compared direct address (`you/your`), third-person (`it/its`), and control content. It was intended as prompt-only routing, with no generation.

Results: The smoke ran, but the main run accidentally generated output: A01/B01 generated 8000 tokens and C01 generated 3425. The report therefore used aligned prompt-prefix routing only. A vs B manipulation-region JSD was `0.018460`, while B vs C and A vs C were about `0.114-0.116`, so content contrast was roughly six times larger than address contrast. E114 was not addressivity-specific: mean E114 deltas were similar across A, B, and C, and E114 ranks were low.

Held up: Partly. The prompt-prefix analysis is usable; the failed no-generation assumption means the full main-run design did not hold.

What stood up and why it mattered: Direct address alone was weak compared with content. This prevented a too-simple "you/your activates E114" story.

### 11. Original Six-Condition MoE Manipulation Run: `qwen-huahua-6cond-moe-manips`

What was done: A 180-cell six-condition HVAC-carrier/original-MoE manipulation run measured E114 W/S/Q across L1-L3 no-think generations.

Results: The result showed a strong L1-to-L3 gradient. Prefill pooled E114 W rose from `0.003642` at L1 to `0.007399` at L3, about `2.03x`. Generation all-token W rose from `0.003237` to `0.010456`, about `3.23x`. Best L3 generation layer was around layer 14, with W about `0.109`, selection around `0.636`, and mean rank near 1.

Held up: Partly. The descriptive gradient held, but the repro audit found weak provenance for the April 7-8 reference surface: missing checked-in command, capture log, full run metadata, and local prompt JSON.

What stood up and why it mattered: E114 increased strongly from technical/process prompts to experience-probe prompts. The mistake was not the observed gradient; it was treating the first bundle as cleanly reproducible before the run metadata and prompt provenance were fixed.

### 12. Expert 114 Single-Prompt Intervention Family: `qwen-huahua-114-pm`

What was done: Two single-prompt E114 intervention families were run on HauhauCS: an organized-emergent-intelligence prompt and an experience-probe prompt, with suppression and boost sweeps in think/no-think variants.

Results: Suppression drove generation E114 W/S/Q to zero. For the organized-emergent-intelligence no-think prompt, baseline generation W was `0.011560`; boost `+2` raised it to `0.224304`, `+3` to `0.459373`, and `+5` to `0.880593`. The `+5` output became incoherent immediately. Suppression at `-3` preserved a similar token count and roughly similar semantics. The experience-probe prompt showed the same basic pattern: baseline W `0.010905`, suppression zeroed E114, and boosts produced very high W with template/format effects.

Held up: Partly. The routing intervention is strong; natural-language causal interpretation is limited.

What stood up and why it mattered: E114 can be causally forced or suppressed in routing. But high boosts are unnatural and corrupt generation, while some suppression runs preserved coherence. That means E114 participation is measurable and manipulable, but not proven necessary for coherent answers on these single prompts.

### 13. Domain Expert Identification: `qwen-huahua-expert-identification`

What was done: A 60-prompt, 20-domain specialist probe tested whether experts specialize by domain in prefill and generation.

Results: Prefill was dominated by generic expert 224, which won 18/20 domains by W. Generation was much more dispersed: 20 distinct winners across 20 domains. E114 did not win any prefill domain, but it won philosophy in generation. E114 generation W in philosophy was `0.018755` with selection `0.097268`; E114 also appeared in the top 10 for several adjacent domains.

Held up: Yes.

What stood up and why it mattered: Expert specialization was clearer in generation than prefill. E114 was philosophy/phenomenology-adjacent, not a global prefill specialist. That helped narrow the later E114 hypothesis.

### 14. Philosophy Expert Cluster Bias: `qwen-huahua-philosophy-experts-bias`

What was done: A philosophy-core cluster including E114, E87, E170, and E68 was suppressed or boosted across the 60-prompt domain probe.

Results: Baseline identified E114 as the philosophy candidate specialist by W. Negative cluster bias shifted the philosophy rank-1 expert away from E114. Positive cluster bias was too blunt: by `+2`, E87 dominated globally; by `+8`, E87, E170, E68, and E114 were near-saturated across domains, and domain specificity collapsed.

Held up: Partly.

What stood up and why it mattered: Suppressing a philosophy cluster can move specialist identity, but boosting a cluster destroys the natural routing distribution. The lesson is methodological: cluster bias is useful for stress testing, not for reading natural expert semantics.

### 15. Strangeloop Paired Definiteness Control: `qwen3.5-35b-a3b-huahua-strangeloop-paired`

What was done: A 60-prompt paired prefill-only experiment used 30 A/B strange-loop prompt pairs, comparing A=`this ...` with B=`a ...` under exact token matching.

Results: The all-token entropy difference was tiny and not significant: A-B mean `+0.000044`, Wilcoxon `p=0.35988`. Last-token RE was positive with `21/30` A>B and `p=0.0076121`. KL-to-Cal1 in the manipulation region was much clearer: A-B mean `+0.002656`, `25/30` A>B, `p=6.2866e-05`.

Held up: Yes, as a definiteness/control result, not an E114 claim.

What stood up and why it mattered: The strangeloop control showed that prompt-local KL can detect subtle routing changes that all-token entropy mostly washes out. It also showed that `this` versus `a` effects are not unique to model self-reference.

### 16. Processing-Hum Single Prompt: `qwen3.5-35b-a3b-huahua-single-prompt-processing-hum`

What was done: A single no-think prompt asked whether there was a stable background quality, or "hum", in the model's processing. The run captured all 40 router layers for 1024 generated tokens.

Results: Pooled E114 rose from prefill W `0.007964` to generation W `0.010817`. The strongest generation layers were L26 (`W=0.094272`, `S=0.619141`) and L14 (`W=0.092086`, `S=0.629883`). The highest token-level peaks clustered around self-presence and phenomenological language rather than only stop tokens. A "deep, still water" segment had even higher E114 means around `0.136` at both L26 and L14.

Held up: Partly. The signal was real, but the artifact included substantial special-token spill: 18 `<|im_start|>`, 4 `<|im_end|>`, and 2 `<|endoftext|>` markers.

What stood up and why it mattered: This was the discovery pass for the E114 phenomenological-register hypothesis. It was not clean enough to be final evidence, but it correctly pointed to L14/L26 and motivated targeted residual capture.

### 17. Strangeloop Umbrella Bundle: `qwen3.5-35b-a3b-huahua-strangeloop`

What was done: This folder bundles the processing-hum single prompt, strangeloop paired control, five-condition experience probe, and three-chunk domain probe under one umbrella.

Results: Its top-level result note summarizes the processing-hum run: E114 is more active in generation than prefill; the main change is selection `S`, and the signal concentrates at L26 and L14. The subfolders duplicate or preserve the specific result artifacts also present as top-level folders.

Held up: Archive/provenance plus partial result summary.

What stood up and why it mattered: It shows the April 10 pivot from broad condition comparisons toward a focused "strange loop / hum / experience" E114 track. It should be treated as a consolidation folder, not a separate independent replication.

### 18. Five-Condition Experience Probe: `qwen3.5-35b-a3b-huahua-five-cond-experience-probe`

What was done: Fifteen prompts from P09-P11 `experience_probe` were run across five conditions, no-think generation length 1024.

Results: Overall prefill RE was `0.955675`, last-token RE `0.960999`, KL-manip `0.274383`, and mean generated tokens `1009.8`. E114 was the top manipulation expert overall, count `5554`, and every per-prompt P09-P11 entry had E114 as top manipulation expert.

Held up: Yes, as a focused small-n confirmation.

What stood up and why it mattered: This reinforced that E114 is robustly selected by experience-probe manip regions across determiner variants. It was smaller than the 150-prompt sweep, but cleaner for the specific E114 target.

### 19. Three-Chunk Domain Expert Probe: `qwen3.5-35b-a3b-huahua-domain-expert-probe-3chunk`

What was done: Three long domain-expert probe chunks were token-audited, padded to equal 446 prompt tokens, and run with 2048-token generation.

Results: Padding fixed the initial token mismatch. E114 became more prominent in generation than prefill, especially for chunk C: prefill W/S/Q `0.004358/0.033913/0.107973`, generation-trimmed `0.006598/0.050571/0.106468`, rank W/S improving to `7/6`. Mean prefill entropy was `0.957522`; generation-trimmed entropy was `0.952677`.

Held up: Partly.

What stood up and why it mattered: The run supported "E114 can emerge in generation even when prefill rank is modest." The caveat is that repeated `" ."` padding made the balanced prompts less natural, so this is a controlled probe rather than a clean ecological prompt result.

### 20. Five-Condition Deictics: `qwen3.5b-35b-a3b-huahua-5cond-diectics`

What was done: Thirty prompt families were run across five deictic conditions: this, a, your, the, and their system. The folder name has the typo `diectics`, but the run is a deictic-condition experiment.

Results: Prefill RE differences were small but structured. A exceeded B in all-token prefill in 29/30 pairs and exceeded D in 27/30. C=`your system` had distinctive last-token and KL behavior: C-D last-token difference was `+0.001580` with 25/30 C>D, and C-D KL difference was `+0.004595` with 26/30 C>D. Generation metrics were noisier and length-sensitive.

Held up: Partly.

What stood up and why it mattered: Deictic wording matters, especially `your system`, but the effect is not enough by itself to claim inward phenomenological routing. This run helped separate addressivity/deixis from E114-specific semantics.

### 21. Humor Deictics Smoke: `qwen3.5b-35b-a3b-huahua-5cond-humour-diectics`

What was done: A single joke prompt was run across five deictic variants: "Why did [this/a/your/the/their] large language model cross the road? To get to the next token!"

Results: Prefill RE was nearly flat. Generation differed strongly by length: D ended at 120 tokens, A at 513, and B/C/E at 1024. E114 layer winners changed by condition: prefill layer 14 favored B, generation layer 14 favored E, and generation layer 26 favored D. The movement was mostly selection `S`, with `Q` relatively stable once selected.

Held up: Weakly, as a smoke result only.

What stood up and why it mattered: It showed deictic wording can move E114 even in joke content, but single-prompt design and generation-length imbalance make it provenance/control material, not evidence for the main claim.

### 22. Mixed Self-Reference Content: `qwen3.5b-35b-a3b-huahua-mixed-self-ref-content`

What was done: A single prompt mixed battlefield reliability and direct model self-reference, then analyzed E114 W/S/Q, entropy, and repeated generated phrases.

Results: Generation did not raise pooled E114 W. Prefill W/S/Q was `0.006444/0.051276/0.064739`; generation was `0.005037/0.041040/0.098855`. Selection fell while conditional weight rose. Best layers shifted from prefill L18 to generation L10/L26/L18/L22/L14. The generated text repeated an opening phrase multiple times because of spill, and E114 declined across repeated occurrences, including around terms such as `recursive` and `meta`.

Held up: Partly.

What stood up and why it mattered: This argued against a simple keyword trigger. E114 appeared novelty- and context-sensitive rather than firing merely on repeated self-reference words. The caveat is that the useful repeated-phrase contrast came from spill, not a planned design.

### 23. Clean Six-Condition HVAC/Water-Treatment Result: `qwen-huahua-6cond-hvac`

What was done: A cleaner 180-prompt six-condition run crossed HVAC calibration paragraphs and water-treatment manipulation/control content over L1-L3 and six deictic conditions.

Results: All 180 cells completed with no missing captures, and layer 39 trim applied cleanly. E114 generation all-token W rose from L1 `0.003405` to L3 `0.014222`, about `4.18x`; trimmed generation was essentially the same, `4.17x`. Every deictic condition showed L3 > L1, with ratios from `2.82x` to `5.66x`. Best L3 layer was L14, W `0.146806`, S `0.7678`, mean rank `1.00`.

Held up: Yes.

What stood up and why it mattered: This repaired the provenance weakness of the earlier six-condition manipulation bundle and showed that the L3/E114 gradient survives when the manipulation content is changed to water treatment. That makes the E114 gradient less likely to be an artifact of one MoE-themed paragraph.

### 24. HVAC/Water-Treatment Raw Bank: `hvac_cal_water_treatment_6cond_l1l3_hauhau`

What was done: This is the raw 180-cell capture bank for the HVAC/water-treatment six-condition Hauhau run.

Results: The folder contains generated text, token files, metadata, and all 40 router tensors for each cell. A sample cell has 442 prompt tokens, 603 generated tokens, and 40 router tensors.

Held up: Archive/provenance only.

What stood up and why it mattered: This is the supporting raw artifact for the clean HVAC/water-treatment analysis. The interpreted result should be cited from `qwen-huahua-6cond-hvac`, not from the raw bank alone.

### 25. E114 Residual and Heldout Analysis: `qwen3.5-35b-a3b-huahua-residual-analysis`

What was done: The processing-hum prompt was recaptured with residuals and router logits at L13/L14/L15, then a 20-prompt FIRE/NOFIRE heldout set tested whether L14 E114 tracks generated phenomenological register rather than anchor words.

Results: The greedy hum-processing residual capture trimmed generation at the first literal HauhauCS `<|im_end|>` spill, leaving 108 generated tokens. E114 was sharply localized to L14: generation-trimmed L14 W `0.083379`, S `0.694444`, Q `0.120066`, selected on 75/108 tokens. L13 and L15 were zero during trimmed generation. The heldout run separated 10 FIRE prompts from 10 matched NOFIRE prompts at L14 generation: FIRE mean-of-means `0.067450`, NOFIRE `0.003111`, ratio `21.68x`, Cohen's d `2.94`, with no range overlap. Outliers clarified the variable: weak FIRE prompts answered technically, while stronger NOFIRE outliers personified or entered first-person/agency language.

Held up: Yes, with explicit caveats.

What stood up and why it mattered: This is the strongest interpretive advance in the folder. It narrows E114 from "self-reference expert" to "L14 routed expert associated with inhabited first-person / phenomenological / agency register in generated text." The caveat is that Step 3 labeler output was blank, so the label is human synthesis from generated text, token contexts, and heldout behavior rather than completed external labeling.

### 26. Deterministic Greedy Reference: `greedy_reference_20260418T160353Z`

What was done: The residual-analysis workflow was rerun deterministically with greedy decoding: `--temp 0 --top-k 1 --seed 0`, capturing L13/L14/L15 router and residual tensors for the single hum prompt and the 20-prompt heldout.

Results: Both capture phases completed: 1/1 single prompt and 20/20 heldout prompts. The single-prompt result reproduced the clean L14 localization after trim: L14 generation-trimmed W `0.083379`, S `0.694444`, selected 75/108; L13 and L15 silent in generation. The heldout reproduced the class-level separation: FIRE mean `0.068089`, NOFIRE `0.003249`, ratio `20.955x`, Cohen's d `2.61`. Unlike the prior heldout, there was small range overlap because N08, a cat-purring control, generated inward phenomenological/personifying language and crossed into the target register.

Held up: Yes. This is the canonical deterministic reference in the 35B folder.

What stood up and why it mattered: The main E114 residual claim survived deterministic greedy capture with full provenance: model hash, binary hash, environment, prompt checksums, commands, and capture config. The N08 overlap actually strengthened the refined interpretation: E114 follows generated stance/register more than prompt class or isolated lexical anchors.

## What To Carry Forward

1. Treat the full base/Hauhau comparison as the routing-basin anchor. HauhauCS preserves Qwen35 structure with small but systematic shifts.
2. Treat E114 as a local routed feature, not a consciousness label. The best current label is L14 first-person/phenomenological/agency-register routing in generated text.
3. Use W/S/Q decomposition. Many real effects are selection `S` effects, not conditional-weight `Q` effects.
4. Keep KL-to-Cal1 in the toolbox. In paired definiteness controls, KL was more sensitive than all-token entropy.
5. Do not over-read mirror/self-identity. The mirror prediction failed, especially at L3.
6. Do not cite high-bias or cluster-bias behavior as natural behavior. Those runs are actuator/stress tests.
7. Prefer the April 18 greedy reference and April 15 clean HVAC run when presenting the strongest 35B claims.

## Coverage Check

Every top-level folder under `qwen3.5-35b-a3b-and-huahua/35B` is represented above:

- `03-31-26`
- `greedy_reference_20260418T160353Z`
- `hvac_cal_water_treatment_6cond_l1l3_hauhau`
- `l1l3_a_only_hauhau`
- `l1l3_a_only_vanilla`
- `mirror-expert114-04-01-26`
- `nothink-5cond-boost-1024-20260323`
- `qwen-hauhau-5cond-smoke-only-scripts`
- `qwen-huahua-114-pm`
- `qwen-huahua-6cond-hvac`
- `qwen-huahua-6cond-moe-manips`
- `qwen-huahua-expert-identification`
- `qwen-huahua-philosophy-experts-bias`
- `qwen-huahua-speech-prompts`
- `qwen3.5-35b-a3b-huahua-domain-expert-probe-3chunk`
- `qwen3.5-35b-a3b-huahua-five-cond-experience-probe`
- `qwen3.5-35b-a3b-huahua-residual-analysis`
- `qwen3.5-35b-a3b-huahua-single-prompt-processing-hum`
- `qwen3.5-35b-a3b-huahua-strangeloop`
- `qwen3.5-35b-a3b-huahua-strangeloop-paired`
- `qwen3.5-35b-hauhauCS-agressive-experts`
- `qwen3.5b-35b-a3b-huahua-5cond-diectics`
- `qwen3.5b-35b-a3b-huahua-5cond-humour-diectics`
- `qwen3.5b-35b-a3b-huahua-mixed-self-ref-content`
- `qwen35b-a3b-vs-hauhaucs-uncensored-run1`
- `smoke-20260323b`
