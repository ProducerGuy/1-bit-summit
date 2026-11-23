# Ranked repair candidates for the next five points

Steps 2 and 3 of the order of work. Target: five more points of benchmark retention at fixed 1-bit precision at 1.7B. The damage it must repair is in `damage-table.md`. No run was made for this document.

## 1. Reading record

| Source | How much was read | What it establishes | What it does not show |
|---|---|---|---|
| LFQ, https://arxiv.org/abs/2605.29756 | Whole page, through an extraction | Fitting only the last block by cross-entropy on the logits, through the output matrix, improves generation tasks over block-wise rounding: about 1 to 3 points on IFEval and MATH-500, up to 13 on AIME greedy. Applying it to more than the last block adds nothing | Only 4-bit and 3-bit. Smallest model in the main results is 7B. No optimizer, cost or code given |
| Lotfi and others, https://arxiv.org/abs/2606.00206 | Whole page, in two extractions | On a 1.5B reasoning model rounded to 3 bits, 52% of MATH-500 failures contain the right answer and abandon it. A fixed penalty on 50 hesitation words lifts the five-benchmark average from 29.0 to 35.2 and cuts length by 28% | Thinking mode only, post-training rounding only, 3 bits at the lowest. The penalty strength is the best per configuration, chosen on the reported results; no fixed-strength result is given. Gains shrink to under 1 point at 7B and above |
| BitNet Distillation, https://arxiv.org/abs/2510.13998 | Whole page, through an extraction | From pretrained Qwen3 0.6B to 4B to ternary: plain fine-tuning leaves 14 to 15 points; an extra normalization, 10 billion tokens of continued pretraining, and logit plus attention distillation close it. A larger teacher gives a student that beats the same-size full-precision model | Three classification tasks and one summarization task. No reasoning or general benchmark. Ternary, with 8-bit activations |
| Wu and others, https://arxiv.org/abs/2608.06564 | First 200,000 of 277,669 characters | Across 16 models from 0.6B to 32B, Qwen3-1.7B among them, the margin after rounding is a line in the margin before: slope 0.86 at 4 bits, 0.29 at 3, 0.00 at 2. Whether to call a tool flips in 47% of cases at 3 bits under plain rounding, 21% under GPTQ; which tool to call and its arguments barely move. The shift acts as a penalty on the token that opens the call. Label-free repairs win on no majority of models and none matches one extra bit. A calibrated bias on the call-opening token recovers the lost calls at the price of the correct refusals to call. In the Qwen3 family the smaller model loses more: 93% of refusals at 1.7B, 13% at 4B | Post-training rounding only, 2 bits at the lowest, first-token decisions only. No training-based repair is tested. The last 77,000 characters are unread |
| Forensics project, https://github.com/sky-is-green/bonsai2-ternary-forensics | README, recipe ledger, retention report, forensic archive, failure summary and entries F6 to F8, the third gate report, the run settings in the experiments file. Whitepaper and the rest of the experiments file unread | Section 2B of the plan. In addition: training each block against its own output on 8,192 tokens, with student or teacher inputs, gives an assembled perplexity above one million on the 27B, worse than plain rounding. Choosing distillation text by loss lost to random text (172 against 116 perplexity). Error-feedback rounding agrees with PrismML's first-generation ternary 1.7B codes no better than plain rounding (0.618 against 0.612). Its own 1.7B training used 300 thousand tokens of text repeated for thousands of steps | Ternary. Its training text is small |
| OpenBonsai, https://github.com/esokullu/openbonsai | Pipeline code and run logs (checklist C88) | Scale-only distillation with codes frozen: NLL 3.32 to 2.89 on its own model; from PrismML's released ternary 9B, 2.1 million tokens halved the held-out gap. Distilling on the teacher's own answers to math and code prompts took GSM8K from 30 to 69 of 100 | Ternary, 8B and 9B |
| Attend to Your Own Thoughts (ScaleQ-1.58), https://arxiv.org/abs/2608.01078 | Tables 1, 2 and 4, method and limits, through an extraction | On Qwen3-4B at 1.58 bits, the calibration text decides mathematics and code: generic text scores 0.00 on MATH-500, task text 24.20, a far stronger model's answers 31.80, the model's own answers 58.40. Scores rise without a plateau from 256 thousand to 16 million tokens (MATH-500 20.90 to 66.20). On Qwen3-1.7B with 4 million tokens it keeps 38.60 of 90.80 on MATH-500 and 54.35 of 84.08 on GSM8K | 1.58, 2 and 4 bits. No 1-bit result. Fitting is by reconstruction over a window of layers, not on logits. Whether the embedding and output matrix are rounded, and whether thinking is on, are not stated |
| Reproduction study, https://github.com/ThakiCloud/bonsai-1bit-repro | Report, results file and the fingerprint script. Paper source and the four other scripts unread | PrismML publishes its 1-bit 1.7B weights unpacked for standard tools (`prism-ml/Bonsai-1.7B-unpacked`); every group holds exactly one magnitude. On a fixed passage that model's perplexity is 0.995 times its teacher's. Fingerprint over 196 matrices: 28.4% of signs changed, median scale 2.26 times naive, aggregated per matrix only. Its own error-feedback binary rounding of Qwen3-0.6B ends at perplexity 184,896, and inflating scales alone makes it worse | The fingerprint is not broken down by position within a matrix or by weight magnitude. Perplexity is on one short passage |
| OneBit | In full earlier (C72) | In the plan | |
| BinaryLLM, https://arxiv.org/abs/2508.06974 | Whole page, through an extraction | Pretrained to 1-bit by training in which a smooth function is sharpened into the sign over 20 phases, with one learned scale on top of the analytic one. On SmolLM-135M: perplexity 17.6 to 26.8 on WikiText-2 and zero-shot average 49.1 to 42.8. On LLaMA3-1B: 9.8 to 14.7 and 55.2 to 48.7. Its special initialization changes the final average perplexity from 20.4 to 20.0. Stronger bases lose more | Embedding and output matrix are outside its bit count. Ablations use 50 billion tokens; the main token count is not stated. No reasoning or generation benchmark. No code |
| FBI-LLM, https://arxiv.org/abs/2407.07093 | Abstract only | Binary models trained from random initialization by distillation at pretraining scale match those started from pretrained weights | Not read beyond the abstract |

## 2. Two facts the ranking rests on

### 2A. Nobody has shown which way the first-generation 1-bit model was made, and it decides the headroom

- Reading A: sequential error-compensated rounding with no end-to-end training. This is the reproduction study's reading of the fingerprint.
- Reading B: end-to-end training, by the patent's mirror descent or otherwise.
- The weight of evidence is on reading B, about 85 to 15. Every public attempt at error-compensated 1-bit rounding collapses on text it was not fitted on: the reproduction study's own run ends at perplexity 184,896, and its best rotated variant holds only on its fitting passage. Error feedback moves codes no closer to PrismML's first-generation ternary 1.7B than plain rounding does. The released 1-bit model sits at its teacher's perplexity on ordinary text, which no rounding method has reached.
- Both readings produce many sign changes and inflated scales. Under error feedback at 1 bit, weights not yet rounded absorb large errors and grow, so scales chosen from them come out well above the naive mean. Under training, scales are simply learned.
- A least-squares scale cannot explain the fingerprint. With unit input covariance the least-squares scale of a group is its mean magnitude times one minus twice the flipped share of magnitude, so sign changes lower it. A scale 2.26 times naive is therefore either error accumulation or training.
- The two readings differ in one measurable place. Error feedback runs along the input columns in order, so its inflation rises with a group's position along the input dimension. Training has no reason to produce a trend with position.
- Consequence: under reading A the released model has never seen an end-to-end loss, and the open pipeline's experience (30 to 69 on GSM8K from distilling on task answers) says the headroom is large. Under reading B the general headroom is smaller, but the task headroom remains: the first generation keeps 46% of MATH-500 at 1 bit and 74% in ternary, where PrismML's second generation keeps over 100% of mathematics at 2B. Its first-generation training evidently did not aim at these tasks.

### 2B. PrismML's own second generation shows the two largest losses are repairable at this size, and how

- At 2B its ternary model beats its own teacher on GSM8K by fifteen points and keeps 95% of tool calling, while losing knowledge (damage table, section 5).
- A student does not exceed its teacher by copying it. That training used task data, a larger teacher, or both. BitNet Distillation reports the same effect from a larger teacher.
- So the route to the mathematics and tool-calling points is the content of the distillation data and the choice of teacher, more than the optimizer.

### 2C. A better start matters only at small budgets

- BinaryLLM's special initialization moves its final perplexity by 2% after tens of billions of tokens. FBI-LLM reports that at pretraining scale a pretrained start and a random one end in the same place.
- Our conversion work improves the start. On this evidence its value is confined to budgets of millions of tokens, which is the budget we have. At PrismML's scale it would wash out.
- That is a reason to judge every conversion idea by what it buys within a small training budget, and by nothing else.

## 3. Candidates, ranked

Five points of retention is 29 points summed over the ten benchmarks. Probabilities are judgments.

| Rank | Candidate | Loss it targets | Evidence | Starting model | Expected gain in retention | Probability of five points | Cost |
|---|---|---|---|---|---|---|---|
| 1 | Scale-only distillation on task answers: signs frozen, the 13 million group scales and the norm gains trained end to end against the same-size teacher's own answers to mathematics, tool-calling and code prompts mixed with general text | MATH-500, BFCL v3, GSM8K, code: 70% of the loss | OpenBonsai scale-only results, including from a released trained model; the 1.58-bit study of calibration text (generic text scores 0 on MATH-500, the model's own answers 58.40, and scores still rise from 256 thousand to 16 million tokens); PrismML's 2B result; our own scale-only arm on SmolLM2 (KL 2.76 to 1.97 in 38,400 tokens); published level refits with codes fixed lowering held-out loss | PrismML's released 1-bit 1.7B, from its unpacked weights | 4 to 8 points under reading A, 2 to 6 under reading B | 45% overall: 70% under A, 40% under B | A ladder of training-token budgets through a 1.7B model, so the slope is seen and not one point. No change to stored bits or inference |
| 2 | Full training of signs and scales from the released model, straight through, with a managed learning-rate decay | Everything, including knowledge | Forensics ledger (longer training keeps helping; decay needed); our SmolLM2 curve (48% to 65% in 230,400 tokens) | Same | More than rank 1 in the end, about equal early | 50% | Several times rank 1 in memory and tokens. Second stage after rank 1 |
| 3 | Rank 1 with a larger teacher's logits as the target, on the same-size teacher's own text | Same, plus the teacher's own weak spots | For: BitNet Distillation figure 3; PrismML's 2B model beating its teacher. Against using a stronger model's text: at 1.58 bits on Qwen3-4B, a far stronger model's text scored 31.80 on MATH-500 where the model's own scored 58.40 | Same | 0 to 2 points beyond rank 1 | No added odds over rank 1 on present evidence | Rank 1 plus one pass of the larger model over the same text |
| 4 | Tool-call bias: one added constant on the logit that starts a tool call | BFCL v3, 21% of the loss | Wu and others measured exactly this on rounded models: the best bias recovers the lost calls and loses as many correct refusals to call | Any | About 0 | Under 5% | None. Dropped unless the failure split of section 4 shows a one-sided loss |
| 5 | Last-block logit fit | Final decisions on generation tasks | LFQ at 3 and 4 bits; our final-gain refit on SmolLM2 | Our own conversion, where no end-to-end loss exists | Under 1.5 points | 10% | Small. Already contained in ranks 1 and 2, which train against logits |
| 6 | Hesitation penalty at decoding | Reasoning in thinking mode | Lotfi and others, 3-bit, 1.5B | Any, thinking mode only | 0 on the published suite, which is scored with thinking off | 35% on a thinking-mode suite, with the strength fixed in advance | None. An inference-side change, recorded as such |
| 7 | Rotation inside the conversion and training | The rounding error itself | Forensics ledger: essential for ternary training | Our own conversion | Not countable at fixed format: it adds a transform at inference | Science scoreboard | Format change |
| 8 | Our own conversion of Qwen3-1.7B from scratch | Everything | Sections 2K to 2M of the plan | Qwen3-1.7B | Its ladder starts at its own baseline, far below 70% | Not the route to 75% | Largest |

### 3A. Why rank 1 leads

- It aims at the abilities that hold 70% of the loss.
- It leaves the format untouched: same signs, same number of scales, no inference cost.
- Every piece of it has published or measured support. None of it is new.
- It is the cheapest candidate that can plausibly move 29 summed points.

### 3B. Its gaps

- Whether the released model was already trained end to end (section 2A).
- No scale-only result exists at 1 bit on a released model. All of the evidence is ternary or on a small proxy.
- Benchmark retention after scale-only distillation has not been published by anyone. OpenBonsai's 9B run from released weights measured text loss only.
- Scale changes can raise one ability and lower another. The step rule requires recording what newly broke.
- Loading is not a gap: PrismML publishes the weights unpacked, and each group's sign pattern and scale can be read back exactly.

## 4. The proofs, in order

| Order | Proof | What each outcome changes |
|---|---|---|
| 1 | Ruler acceptance, baseline and failure split (`docs/ruler-spec.md`): the teacher and the released 1-bit model scored on the full suite, with every failed item sorted by the way it failed | Fixes our position on the ladder. Decides whether rank 4 is worth a test and which task answers rank 1 is trained on |
| 2 | Rank 1 on a ladder of token budgets, scored on the whole suite before and after, with the lists of items gained and lost | Five points earns the first step. A rising slope short of five points says spend more tokens. A flat slope sends the work to rank 2 |
| 3 | Fingerprint by script on the released unpacked 1-bit 1.7B and its base: scale over naive mean as a function of group position along the input dimension, per matrix kind, and sign changes by base magnitude. No model is run. The reproduction study's script computes neither breakdown | A rising trend with position means reading A: rank 1 goes to 70% and our own formula gains a public target that needs no training. No trend confirms reading B and the profile of sign changes by magnitude tells our own formula which weights training re-decides |

Proof 3 does not change the order of proofs 1 and 2 under either outcome. It reads files, needs no training, and can run at any point.

## 5. Blind spots

- The whole ranking takes PrismML's suite as the ruler. It is scored with thinking off. A product used in thinking mode may lose its points elsewhere.
- Knowledge is 14% of the loss and no candidate above has evidence of repairing it at small size. PrismML's own second generation did not.
- Starting from a released model makes the first step fast and teaches less about conversion. Proof 3 is what carries the lesson back to our own formula.
- The evidence that selecting distillation text by loss is worse than random is one pilot. Selecting by task type has support; selecting by per-example loss does not.
