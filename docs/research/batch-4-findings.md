# Batch 4 findings

First reviewer's work on the three items of batch 4. No run was made. Probabilities are judgments. The second reviewer has the same three items and has not seen this document.

Reference figures: the released 1-bit 1.7B keeps 70.2% of Qwen3-1.7B on the ten-benchmark suite with thinking off. One five-point step is 29.1 summed points. The largest losses are MATH-500 39.6, BFCL 36.9, MMLU-Redux 23.6, GSM8K 16.8, MBPP+ 15.9, HumanEval+ 12.2.

## 1. Which decisions low-bit conversion breaks

### 1A. What was read

| Source | How much | Route |
|---|---|---|
| Wu, Dhiman, Koshiyama, "Which Decisions Low-Bit Quantization Breaks, and How to Predict Them", https://arxiv.org/abs/2608.06564 | Whole paper. The first 200,000 characters earlier, the last 77,669 (appendices A.16 to A.22) now | HTML, extraction |
| Lee and others, "LFQ: Logit-aware Final-block Quantization", https://arxiv.org/abs/2605.29756 | Whole paper, read again with a full extraction | PDF |
| Lotfi and others, "Quantized Reasoning Models Think They Need to Think Longer, but They Do Not", https://arxiv.org/abs/2606.00206 | Whole paper, read again with a full extraction | PDF |
| Alimaskina and others, "Extreme Low-Bit Inference in Reasoning Models: Failure Modes and Targeted Recovery", https://arxiv.org/abs/2606.02011 | Whole paper in two extractions. Code: file tree, the loop and commit triggers, two run settings files | HTML. Repository read directly, https://github.com/brain-lab-research/quantized-reasoning |
| Jang and others, "Flat Score, Amplified Failures: How the Error Budget Masks Damage in Quantized LLM Agents", https://arxiv.org/abs/2607.27275 | Whole paper | PDF |
| Li and others, "Quantization Meets Reasoning", https://arxiv.org/abs/2505.11574 | Whole paper, version 4 | PDF |
| Shah, "Same Score, Different Model: Two Regimes of Quantization Damage Below and Above the Accuracy Plateau", NeurIPS 2026 workshop oral, https://neurips.cc/virtual/2026/160501 | Abstract page only | Direct |

- The last four were found by search. None of the first three papers links code.
- All extractions condense. The numbers below are the numbers the extractions returned.

### 1B. Facts: first-token decisions under plain rounding

Source: Wu and others, Table 6 and appendix A.18 to A.22. "Survival" is the slope of a decision's margin after conversion against its margin before. 1 means the margin is intact, 0 means nothing of it is left.

| Decision kind | 4 bits | 3 bits | 2 bits |
|---|---|---|---|
| Whether to call a tool | 0.86 | 0.21, 47% of decisions flipped | 0.00, 54% flipped |
| Which tool (BFCL) | 0.85 | 0.25 | 0.03 |
| Argument fill (BFCL) | 0.92 | 0.60 | 0.02 |
| Use of a tool's result | 0.80 | 0.35 | not estimable |
| MMLU | 0.83 | 0.19 | -0.01 |
| BoolQ | 0.89 | 0.51 | 0.01 |
| Arithmetic | 0.84 | 0.33 | 0.04 |
| Code token | 1.00 | 0.94 | not estimable |
| Refusal, forced choice | 0.83 | 0.27 | 0.00 |

- Calibrated builds hold far more than plain rounding at the same width. Whether to call: GPTQ 0.88 at 4 bits and 0.55 at 3; shipped mixed-precision files 1.00, 0.94, 0.71 and 0.56 from 8 bits down to about 2.
- In matched pairs at 3 bits the decision whether to call changes side in all 48 model and quantizer pairs, median rate 0.32. Which tool changes side in none of 48.
- Direction is not shared. Of 17 models, 10 lean toward not calling, 6 the other way, 1 is level (p = 0.63). The offset also appears in base models, so it is not only instruction tuning being undone.
- Live BFCL test, 400 requests, 3 bits, plain rounding, share of calls lost and share of tool names lost:

| Model | Calls lost | Names lost |
|---|---|---|
| Gemma-3-4B | 0.87 | 0.32 |
| Qwen2.5-7B | 0.57 | 0.12 |
| Qwen3-4B | 0.75 | 0.55 |
| Qwen3-1.7B | 0.93 | 0.96 |
| Hermes-3-Llama-3.2-3B | 0.44 | 0.59 |

- At 1.7B both halves go. The paper's headline, that the decision to call breaks before the choice of tool, holds at 4B and 7B and does not hold on our teacher.
- With calibrated rounding Qwen3-4B loses 0.00 of calls and 0.01 of names at 3 bits.
- Failure shapes seen: prose that names the tool without opening the call; a call opened on 42% of tasks against 97% before, finished and parseable on 24%; a call token followed at once by end of turn (41 of 53 lost calls in one calibrated build).
- The paper states its own limits: post-training rounding only, 2 bits at the lowest, first-token decisions, no training-based repair, and its simulator is harsher than shipped files.

### 1C. Facts: how predictable a flip is

- Wu and others: with a slope and an offset fitted for one model, one quantizer and one decision kind, the share of flips in a held-out half is predicted to a median of 1.0 point (1,082 conditions). Per item, the Brier score is 0.079 against 0.165 for guessing the average rate (193,779 predictions).
- The constants do not transfer. Leave-one-condition-out at 3 bits: 9.8 points of error. Held-out models: 2.6 points at 4 bits, 26.8 at 3 bits.
- On live BFCL behavior the per-item forecast beats the base rate only at 4 bits on Qwen3-4B (37% better Brier) and fails at 3 bits.
- Shah, abstract: on 3,658 MMLU-Pro questions and seven builds of one 30B model, the full-precision margin on the answer token predicts which questions flip. Only 12.2% of questions are contested at all. Above about 3.9 bits accuracy is flat while agreement with the original keeps rising, 0.927 to 0.969. Below it, losses are about twice the wins.
- Jang and others, agents at 4 bits: quantization repeats the full-precision model's own failures at a higher rate. On the one model with a large effect, the wrong-tool-name rate goes from 19.51% to 38.26%; the per-tool frequency of wrong names correlates 0.97 between the two precisions; 3 of 1,646 wrong calls at 4 bits name a tool never invented at full precision. The rise is additive across tasks (17.6 points, slope -0.06 against the task's own baseline rate). A high baseline rate is needed for the effect and does not guarantee it.
- Li and others, mathematics at 4 bits: among problems the full-precision model solved and the 4-bit model failed, the failure kinds are about 55% conceptual, 17% method, 26% slips in computation or symbols, 1% logical (Llama-3.1-8B, 517 cases). The full-precision model's own failures are 59.6%, 12.5%, 13.0% and 13.1%. Labels are by five model judges with human arbitration, 97.2% agreement with the final human label on 9,908 cases.

### 1D. Facts: free-running generation

- Lotfi and others, thinking on, 3 and 4 bits: the gap between the two models' next-token distributions, measured under identical prefixes, tracks the full-precision model's own entropy at that position (rank correlation 0.92). The widest gaps are on "Wait", "But", "Alternatively", "maybe", "verify". The narrowest are on the end of thinking, the end of the answer, "boxed" and digits.
- The consequence is length and abandonment. On the 1.5B model at 3 bits, 139 of 265 MATH-500 failures (52%) reach the right answer and leave it, against 19 of 72 at full precision. Mean thinking length goes from 11,248 to 28,048 tokens. Across 28 model and quantizer pairs, accuracy loss and length growth correlate at -0.73.
- Alimaskina and others, thinking on, 2 bits (calibrated with AutoRound, files from a public collection): the accuracy drop tracks the loop rate (rank correlation -0.88) and the share of answers that hit the budget (-0.89). Qwen3-8B on MATH-500 goes from 92.40 to 17.20 with thinking closed in 23.6% of answers; on GSM8K from 96.13 to 52.69. Greedy decoding loops more than sampling (32B: loops 28.8% at temperature 0 against 18.0% at 0.6). Short budgets hide the effect.
- LFQ: its diagnosis rests on a two-token toy and one trajectory. Its measured fact is that generation loses more than recognition at 4 bits: MMLU -2.15 against IFEval -4.25 and GSM8K -3.64 on Llama-3.1-8B; on a reasoning model MMLU -1.15 against AIME -16.67.
- Li and others: the drop grows as the model shrinks and as the task gets longer. Qwen2.5 at 4 bits on MATH: 0.5B 23.98 to 8.02, 1.5B 43.74 to 25.6, 7B 72.48 to 69.84. Averaged over models: MATH -29.8% relative, GSM8K -13.2%, five recognition and instruction benchmarks -4% to -5%.

### 1E. Facts: where in the network, and the repairs tested

Where:

- None of these papers measures damage by layer. Two place it at the output by what fixes it. LFQ: fitting the last block alone, through the output matrix, carries the whole gain; adding the second and third from last adds nothing (77.13 against 76.78 on its IFEval and GSM8K mean, 75.80 with none). Wu and others: the tool-call shift behaves as a penalty on the one token that opens a call.

Repairs:

| Repair | Changes | Bit width, size | Result |
|---|---|---|---|
| LFQ: last block fitted by cross-entropy on the next-token distribution | Stored weights | 3 and 4 bits, 3B to 30B | MATH-500 +0.8 to +2.4, IFEval +1.3 to +1.9 on Qwen2.5-7B; AIME greedy 30.00 to 43.33 on a 7B reasoning model; Llama-3.2-3B IFEval +1.5, GSM8K +0.3 |
| A bias on the call-opening token, calibrated | One logit | 3 bits | Returns the lost calls and loses the correct refusals |
| Label-free repairs as a class (Wu and others) | Various | 3 bits | Win on no majority of models; none equals one more bit |
| Penalty on 50 hesitation words | Decoding | 3 bits, 1.5B to 32B, thinking on | 1.5B: five-benchmark mean 29.0 to 35.2, abandoned answers 139 to 58. Under 1 point on many rows at 7B and above. Strength picked per configuration on the reported results |
| Loop detector: commit to the answer already given, else rerun in full precision | Decoding, with a full-precision fallback | 2 bits, 8B and 32B, thinking on | Qwen3-8B MATH-500 17.20 to 74.20, mostly through the fallback |
| A short plan written by the full-precision model | Prompt, needs the full-precision model | 2 bits | Qwen3-8B MATH-500 17.20 to 26.40; 32B 65.00 to 80.60 |
| Validate each tool call, ask for a corrected one | Harness | 4 bits, 31B | +5.9 points on one model, wrong names 38.26% to 2.90%; not significant elsewhere |
| Preference training on the model's own first wrong step against a strong model's completion, 332 pairs | A 16-bit adapter on top of 4-bit weights | 4 bits, 0.5B to 8B | MATH-500: Qwen2.5-1.5B 21.0 to 26.4 (full precision 22.2), 3B 29.0 to 38.4 (39.0), 0.5B 8.2 to 9.4 (16.6). Targeted pairs beat random pairs by 1.7 on its average |

- No repair in this set is tested at 1 bit, on a model trained after conversion, or with thinking off on generation tasks.
- Every repair shrinks at the small end or leans on the full-precision model at run time.

### 1F. Answer

- Which decisions break. Under rounding, every kind of first-token decision loses its margin at about the same pace: most of it kept at 4 bits, a fifth to a half at 3, none at 2. Code tokens and argument filling hold longest. The decision that flips most is the one with two near-equal options and a standing bias: whether to call a tool. In running text the damage lands on the model's open choices, the points where the original was itself unsure, and determined tokens survive. The visible result is longer answers, loops, answers reached and abandoned, and calls opened and not finished.
- By task. Long generation loses several times what recognition loses. Mathematics loses most, and more as the model shrinks.
- How predictable. Which items are at risk can be told before conversion: the ones the full-precision model decides by a thin margin, and the failure it then falls into is usually the full-precision model's own nearest alternative. How many flip cannot be told before conversion: the two constants have to be fitted on the converted model, and they do not carry between models at 3 bits.
- Where. At the output, on this evidence: the last block and the output matrix carry the repair that works on stored weights, and the tool-call shift is a shift on one output token. The layer-by-layer evidence is in batch 2 and is not extended here.
- The gap in all of it. Every measurement is on rounded models. Rounding at 2 bits leaves a survival of zero, so the instrument reads "all gone" there. Nothing in these papers, or in the searches run for this item, measures margin survival on a 1-bit or ternary model that was trained after conversion. The released 1-bit 1.7B is such a model, and its survival by decision kind is a number nobody has.

### 1G. What it means for the next five points

Sorting the failed items of the first full run. Each failed item gets these fields, all from forward passes or from the two models' saved answers:

| Field | Reads | Sorts the item as |
|---|---|---|
| Was the teacher right | Both answers | A flip, or a failure the teacher shares |
| The teacher's margin on its first deciding token | Teacher logits | Thin margin: at risk before conversion. Thick margin: the conversion destroyed something |
| Is the 1-bit answer the teacher's runner-up | Both answers | Yes: the teacher's own near miss, amplified. No: a new kind of error |
| First position where the 1-bit model's top token leaves the teacher's, with the teacher's entropy there | Teacher-forced pass | Divergence at an open choice, or at a determined token |
| Looped; hit the budget; right answer present in the text and not the final one | 1-bit answer | Process failure |
| Tool items: no call opened; opened and not parseable; wrong name; wrong arguments; called when it should not | 1-bit answer | Which half of a call broke |

What to repair first, by what the sort returns:

- A one-sided shift on a decision that otherwise keeps its margin (calls never opened, a letter bias on multiple choice): the cheapest repair, at the output. In our format that is scale training on the tied matrix, which holds 16 scales for each token and which the released 1.7B never trained (batch 3). The published bias repair shows the limit to watch: it traded lost calls for lost refusals, so both sides are scored.
- Thin-margin flips into the teacher's runner-up: no targeted repair exists. They fall only as overall agreement with the teacher rises, which is scale training first and sign training after.
- Process failures: the training text has to contain the states where they happen. That is training on the 1-bit model's own answers with the teacher scoring each token (idea I14).
- Thick-margin flips into a new kind of error: information the signs no longer hold. Sign training, with text that carries those items.

Two additions to the trials:

- S4 gains a margin-survival table: for each decision kind that can be read from one token (answer letter, call or reply, tool name, first argument token, yes or no, a digit), the slope and offset of the 1-bit model's margin against the teacher's, on items outside the ruler's test sets. A high slope with an offset points to the output and to scale training. A low slope points to sign training. Under rounding at 2 bits this number is zero everywhere; what a trained 1-bit model shows is unmeasured.
- M1 records the fields in the table above.

One caution on the ruler: the two largest published gains at the small end are decoding rules (a word penalty, a stop on loops). They change the harness, not the weights. The ruler fixes decoding, so they do not count as retention, and the suite's allowances (answer budget, retries) are written down before the first run, since a tolerant harness can hide damage (a gap of 1.3 points at ten allowed failures was 16.7 at two).

Probabilities:

| Candidate | Before | After | Reason |
|---|---|---|---|
| An on-policy stage adds at least a third of a step | 50% | 52% | Three more papers put low-bit generation failures in the process (loops, budget, abandonment). All three are with thinking on, and our suite is thinking off |
| The tool-calling loss of the released 1.7B is mainly a one-sided shift on the decision to call | Not held | 30% | The shift is the common pattern at 4B and above. On Qwen3-1.7B at 3 bits both halves of the call go, and BFCL has parts that never test the decision |

### 1H. Still unknown

- Margin survival by decision kind on the released 1-bit 1.7B. S4's added table answers it with forward passes.
- The shares of each failure kind on our suite with thinking off. M1's records answer it.
- Whether the full-precision margin predicts flips on a trained 1-bit model as it does on rounded ones. The same S4 pass answers it.
- The body of Shah's paper and its per-question files. The page that holds them needs an approval that went unanswered.

## 2. Published recipes for training at 1 bit and ternary

### 2A. What was read

| Source | How much | Route |
|---|---|---|
| Liu and others, "ParetoQ", https://arxiv.org/abs/2502.02631 | Whole paper in two extractions | PDF |
| ParetoQ code, https://github.com/facebookresearch/ParetoQ | README, the training script, the run script, each in full | Repository read directly |
| Panferov and others, "QuEST: Stable Training of LLMs with 1-Bit Weights and Activations", https://arxiv.org/abs/2502.05003 | Whole paper, version 2, in two extractions | HTML |
| QuEST code, https://github.com/IST-DASLab/QuEST | README, the quantizer file in full, the run script | Repository read directly |

### 2B. Facts: ParetoQ

Recipe:

| Part | 1 bit | Ternary and 2 bits |
|---|---|---|
| Quantizer | scale times sign of the weight | A stretched grid: the weight divided by the scale, clipped to -1..1, rounded to 3 or 4 levels that reach the clip |
| Scale | One per output row, started at the row's mean magnitude, then learned through the loss | One per output row, started at the row's largest magnitude, then learned |
| Gradient | Passed to a weight only while its magnitude is below the scale | The same |
| Left in full precision | Embedding and output matrix | The same |
| Start | Pretrained full-precision weights | The same |
| Optimizer | AdamW, no weight decay, rate 2e-5 with cosine decay, 120,000 steps, sequences of 2,048 | The same. 3 and 4 bits: 40,000 steps at 1e-5 |
| Loss | Next token on text. No teacher | The same |

Findings the paper reports:

- Token budget. At 1, 1.58 and 2 bits the scores stop rising near 30 billion tokens. At 3 and 4 bits near 10 billion.
- Split of a fixed budget of 100 billion tokens on a 125M model: about 90% in full-precision training and 10% in quantized training is best. Quantized training from random weights and rounding without training are both worse.
- How far weights move, as the summed absolute change over the summed absolute start: 10% to 20% at 3 and 4 bits, about 40% at 2 bits and below. The paper names the two regimes compensation and reconstruction, with the change between them at 2 bits.
- Learned scales beat scales computed from statistics at every width (figures, no table).
- A 4-bit embedding sits on the size and accuracy front; 8-bit and 16-bit embeddings do not.

Results at 3B and below. Mean of eight zero-shot tasks, then WikiText-2 perplexity. From the paper's tables and the code's README, which lists released models the paper does not tabulate:

| Model | Full precision | 1 bit | 1.58 bits | 2 bits | 1 bit kept |
|---|---|---|---|---|---|
| MobileLLM-125M | 48.5 / 15.1 | 43.7 / 25.8 | 46.5 | 47.1 | 90.1% |
| MobileLLM-350M | 54.8 / 10.5 | 47.6 / 17 | 51.4 | 52.8 | 86.9% |
| MobileLLM-600M | 58.2 / 9.1 | 50.3 / 14 | 55.5 | 56.6 | 86.4% |
| MobileLLM-1B | 62.1 / 8 | 53.8 / 12.8 | 58.5 | 61.0 | 86.6% |
| MobileLLM-1.5B | 62.7 / 7.9 | 55.9 / 11 | 60.5 | 61.8 | 89.2% |
| LLaMA-3 8B (paper) | 74.6 / 6.15 | 64.1 / 9.5 | 69.0 | | 85.9% |

- These are recognition tasks with a guess rate near 35. Above the guess rate the 1-bit 1B keeps 69% and the 1.5B 75%.
- The embedding and output matrix are in full precision in every row.
- The full-precision parents and the 1-bit, 1.58-bit, 2-bit, 3-bit and 4-bit children are published as model files.

### 2C. Facts: QuEST

- It trains from random weights only: 30M to 800M models on C4 at 100 tokens for each parameter. There is no result from a pretrained start anywhere in the paper or the code.
- Forward: a Hadamard transform in blocks of 128 along the input side, each row divided by its root-mean-square, then a uniform grid with the clip that is optimal for a bell-shaped distribution. Weights and activations both.
- Scale: computed at every step, not learned. At 1 bit it is 0.798 times the row's root-mean-square, which for a bell shape is the row's mean magnitude. One per output row.
- Gradient: passed only where the quantized value is within a set distance of the weight. At 1 bit the paper widens the outer region by 1.30, which by my arithmetic passes gradient for weights up to about 2.3 times the scale. It is a clipped estimator with a wider clip than ParetoQ's.
- Validation loss with 1-bit weights and 1-bit activations:

| Size | Plain straight-through | Rotation with plain training | Learned step size | Adaptive binary | QuEST |
|---|---|---|---|---|---|
| 30M | 5.256 | 4.932 | 3.991 | 3.988 | 3.945 |
| 50M | 6.867 | 5.007 | 3.862 | 3.843 | 3.791 |

- The plain estimator fails outright. Methods that tie the gradient to a scale are within about 1% of one another.
- Worth of a parameter against 16 bits, with weights and activations both quantized: 0.02 at 1 bit, 0.16 at 2, 0.43 at 3, 0.70 at 4.
- Its run names carry "UNTIED": the embedding and output matrix are separate matrices. Its zero-shot results are for 4 bits only.

### 2D. Answer

What the recipes are, at 3B and below:

- One published recipe converts a pretrained model to 1 bit at this size with numbers beside its own full-precision model: ParetoQ. It keeps 86% to 90% of an eight-task recognition mean, with the embedding and output matrix untouched, after about 30 billion tokens of next-token training.
- QuEST is a from-scratch recipe. Its use to us is its estimator evidence, not its results.
- WinQ (batch 3) is ParetoQ's recipe with resets and noise added, and it is the only one of the three run on our teacher: 73% of an eight-task mean on Qwen3-1.7B at 1-bit weights with 8-bit activations after 20 billion tokens. ParetoQ's own 1.5B model keeps 89% under the same family of recipe. A stronger teacher loses more, as BinaryLLM also reported.

What the ablations say matters:

- Budget, above all. Tens of billions of tokens at 2 bits and below, three times what 3 and 4 bits need. With next-token loss and no teacher.
- Starting from pretrained weights beats starting from random weights at any split of the budget.
- A gradient gated by the scale. Three working 1-bit recipes use one (ParetoQ, WinQ, QuEST), and QuEST measures the ungated estimator failing. The collapse of the clipped estimator in "Linger and Lose" (batch 2) is on tiny models trained from random weights and is now the outlier. This moves the estimator conflict toward a gated estimator, with the clip set relative to the scale and wider than the scale itself (QuEST's 2.3 against ParetoQ's 1).
- Scales. ParetoQ: learned beats computed. QuEST: computed every step, within 1% of learned. BinaryLLM (batch 2): a learned scale alone is unstable when signs move under it; it keeps the computed scale and multiplies a learned one onto it. The three agree on one form: scale equals a value computed from the weights times a learned factor that starts at 1.

What carries to one sign per weight, one scale per 128, tied matrix included:

| Part | Carries | Note |
|---|---|---|
| Scale per group, started from mean magnitude, learned | Yes | Per-row scales are the special case where a row's 16 groups are equal. The finer grid contains every per-row solution |
| Gated gradient | Yes, with a choice to make | From a model that is already binary, every weight behind a sign sits exactly at the scale, which is the edge of ParetoQ's gate. The magnitudes behind the signs must start inside the gate (OneBit starts at sign times 0.01) |
| Budget of tens of billions of tokens | No | It is the cost of rebuilding a model from full precision by next-token loss alone. From a model already trained at 1 bit, with a teacher, the published costs are far lower (batch 2: with distillation in place 10 billion tokens added 0.13 points; batch 3: on-policy training at about 2 bits used tens of thousands of prompts) |
| The 90% and 10% split | No | It concerns budgets that include pretraining |
| 40% weight movement at 2 bits and below | As a warning | Reaching 1 bit from full precision is a rebuild, not an adjustment. A model already at 1 bit has done the rebuild |
| Results | As a ceiling only | Every number has a full-precision embedding and output matrix. None of these recipes has ever trained a binary tied matrix |

- Nothing in either paper covers a binary embedding or output matrix. That part of our format has no published training recipe in this batch. Batch 2's sources on the output matrix remain the only ones.

### 2E. A measurement these files make possible

- ParetoQ's released files are pairs: a full-precision parent and a 1-bit child, with a known recipe between them (gated gradient, learned row scale, next-token loss, about 30 billion tokens).
- The fingerprint script of S2 run on one pair gives the fingerprint of ordinary 1-bit training from a pretrained model: share of signs changed, by magnitude tenth; scale against mean magnitude; cosine to the parent.
- PrismML's body beside it (batch 3: 71% sign agreement, 47.5% of the smallest tenth and 6.7% of the largest changed, scale ratio near 2.1, cosine 0.50) then reads one of two ways:
  - Alike: the body is ordinary training at that budget. Headroom from more of the same is small, and the next points come from what PrismML did not do: the tied matrix, task text, on-policy text.
  - Fewer changes in ParetoQ's children: PrismML moved signs further than ordinary training does, by method or by budget, and the flip budget of sign training has a second reference point.
- Either way it gives the budget on sign changes (idea I13) a measured total: how many signs a full training run changes, by magnitude.
- It needs two checks first: that the published full-precision file is the parent the child was trained from, and whether the child's file stores signs and scales or the weights behind them.
- It is a script on public files and trains nothing. It is proposed as a fifth script trial.

### 2F. What it means for the next five points

- Sign and scale training settings: a gated gradient with the gate wider than the scale; scales as a computed value times a learned factor; magnitudes behind the signs started inside the gate. These go to the settings list of that trial.
- The published 1-bit budgets are not our budgets. They price a rebuild from full precision without a teacher. Our start has paid that price already.
- The 73% on our own teacher after 20 billion tokens, with the embedding spared, beside PrismML's 70.2% on a harder suite with the tied matrix converted, suggests the released model is at least level with the best public recipe at this size: a harder suite and a harder format, for about the same share kept. It supports starting from the released model, and it says the public recipes will not supply the next step by themselves.
- Probabilities for the two training trials do not move on this item.

### 2G. Still unknown

- The fingerprint of ordinary 1-bit training from a pretrained model. Section 2E's script answers it.
- Whether any published run trains a binary tied matrix. None in the sources of batches 2 to 4.
- ParetoQ's training data. The paper does not name it.

## 3. Training scales alone, and transformations that change nothing

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| Chen and others, "EfficientQAT", https://arxiv.org/abs/2407.11062 | Whole paper | PDF |
| EfficientQAT code, https://github.com/OpenGVLab/EfficientQAT | The end-to-end stage's script, the quantizer, the packed linear layer, two run scripts, each in full | Repository read directly |
| van Breugel and others, "FPTQuant: Function-Preserving Transforms for LLM Quantization", https://arxiv.org/abs/2506.04985 | Whole paper | HTML. The plan held only a ResearchGate address; the arXiv address was found by search |
| Koike-Akino, "Neural Compression over Equivalence Classes: Exact Gauges and Functional Rate-Distortion", https://arxiv.org/abs/2611.07233 | Whole paper in two extractions | PDF |
| Dong and others, "STBLLM", https://arxiv.org/abs/2408.01803 | Whole paper, version 2 | PDF |
| STBLLM code, https://github.com/pprp/STBLLM | README, the demo run script, the mask file | Repository read directly |
| Zhao and others, "All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs", https://arxiv.org/abs/2609.06161 | Whole paper in two extractions | PDF. Found by search for scale-only training with frozen binary weights |

### 3B. Facts: training scales with the codes frozen

EfficientQAT, Llama-2-7B, 2 bits, groups of 64. Mean of five zero-shot tasks, full precision 64.86:

| Start | Before scale training | After | Share of the gap to full precision closed |
|---|---|---|---|
| Plain rounding, no block training | 40.69 | 55.71 | 62% |
| After block-by-block training of weights and scales | 58.99 | 60.14 | 20% of what remained |

- The stage, from its code: every scale in the blocks trainable and nothing else; next-token loss on text, no teacher; 4,096 sequences of 4,096 tokens, about 16.8 million tokens; one pass, 128 optimizer steps; AdamW at 2e-5.
- More data, same model: 128 sequences 59.03; 512 59.81; 2,048 60.13; 4,096 60.14; 8,192 60.19; 32,764 60.31. Accuracy is flat after about two thousand sequences. Perplexity keeps falling, 8.09 to 7.50.
- Training zero points as well as scales: 60.18 against 60.14.
- Group size at 2 bits: 32 gives 60.28, 64 gives 60.14, 128 gives 59.50, 256 gives 58.67.
- Within block training, training scales and zero points alone reaches 55.20; weights alone 46.50; both 58.99.
- Lowest width 2 bits (the code refuses less), smallest model 7B, embedding and output matrix in full precision.
- As a fine-tuning method at 2 bits (5-shot MMLU, Llama-7B): 32.6 against 28.1 for an earlier scale-only method, full precision 34.6.

All for 1-Bit, at 1.00 bit, post-training:

- Its last step freezes every sign and trains every scale vector end to end against the full-precision model's output distribution, on 128 sequences of 2,048 tokens, about 262 thousand tokens.
- LLaMA-3.2-3B: perplexity 41.34 to 30.47, mean of seven zero-shot tasks 34.85 to 40.79. One model only; the full-precision row for it is not in the ablation.
- Its format is two binary factors with three scale vectors for each matrix. It is not ours.
- Its finished models at 1.00 bit, mean of seven tasks then perplexity, full precision in brackets: Qwen3-8B 54.82 / 16.26 (69.09 / 9.00); Gemma-3-4B 49.86 / 32.82 (67.12 / 17.39); Qwen3-14B GSM8K 64.66 (94.77). Nothing below 3B.

Already on file, for the same question:

- OpenBonsai, ternary: scale-only distillation on its own conversion took loss from 3.32 to 2.89, and from PrismML's released ternary 9B, a trained model, 2.1 million tokens halved the held-out gap (`repair-candidates.md`, section 1).
- The reproduction study: raising scales by a fixed factor, without training, made its own rounded model worse.
- BinaryLLM: a learned scale alone is unstable when signs train under it. That is about training both together.

### 3C. Facts: transformations that leave the function unchanged

Two papers list them independently and agree.

| Transformation | Acts on | Exact because | Folds into the weights | Stays in our format after conversion |
|---|---|---|---|---|
| Reorder the MLP's inner channels | Rows of gate and up, columns of down | The activation and the product act channel by channel | Yes | It changes which columns of down share a scale. This is S3's regrouping arm for down |
| Scale each inner channel on the up branch, inverse on down | Rows of up, columns of down | The gate times up product is elementwise and the activation is on the gate branch | Yes | Only a factor shared by a whole group of 128 inner channels, which moves scale between two matrices and changes nothing |
| Any invertible matrix inside a head between value and output | Rows of value, columns of output, repeated across the query heads that share a key and value head | Attention sums over positions, not features | Yes | Only sign changes and reorderings inside a head, and one factor for each head. A head's 128 channels are exactly one scale group of the output matrix, so nothing regroups |
| A rotation with a scale on each pair of query and key channels | Rows of query and key | Rotations of a pair commute with the position encoding's rotation of that pair; reflections do not | Yes | The factor yes (row scaling). The rotation mixes two rows before conversion and has no meaning after |
| Reorder the residual channels | Every matrix that reads or writes the residual stream, every normalization gain, the tied matrix | A reordering passes through the normalization | Yes | It changes the groups of every residual reader and of the tied matrix at once. This is S3's shared-order arm |
| Rotate the residual stream | The same matrices | The normalization passes orthogonal matrices, once its gains are folded away | Yes, but the folded gains and the rotation make the matrices dense | No: after it no weight keeps its sign |
| A factor for each token on the residual stream | Activations | Linear layers without bias pass a scalar | No, it runs at inference | No |
| A Hadamard transform at the down projection's input | Activations | It is undone by its inverse | No, it runs at inference | No |

- Floating point: only reorderings and factors that are powers of two are exact bit for bit. A dense matrix between value and output is exact in algebra and changes outputs once cast to the stored precision (Koike-Akino's strict audit).
- The compression paper does not treat the position encoding, so its "reorder query and key channels" is exact only when whole pairs move together with their frequencies. FPTQuant states the pair constraint.

How much conversion error they remove:

- FPTQuant trains its transforms at 4-bit weights with 4-bit or 8-bit activations and nothing lower. Llama-3.2-3B at 4 and 4: perplexity 11.71 against 10.48 at full precision, behind a method with unfolded transforms (11.38). It is aimed at activations.
- The compression paper measures file size, not conversion error. Exact transformations save almost nothing (14,416 bytes on a 135M model); its large savings come from small accepted changes to the function.
- Neither paper, and nothing found in the search for this item, measures an exact, foldable transformation at 2 bits or below.

### 3D. Facts: STBLLM

- It is post-training only. On top of an existing 1-bit rounding method it zeroes 2, 3 or 4 of every 8 weights by a score of weight size and input size, gives the sensitive columns a second binary layer, and splits the remaining weights of each block into three magnitude bands with a scale each.
- Its "0.55, 0.70, 0.80 bits" count kept weights. They do not count the positions of the zeros, the band of each weight, or the scales. Its own kernel section describes 6 bits for 4 weights. A later paper recounts the storage of this family with everything included: STBLLM at 4 of 8 is 3.50 bits per weight, the method it builds on 2.88 (All for 1-Bit, appendix A.3).
- WikiText-2 perplexity, full precision, then the base method at "1.09", then STBLLM at "0.80" and "0.55": LLaMA-2-7B 5.47, 32.48, 13.06, 27.93. LLaMA-3-8B 6.10, 28.30, 33.44, 253.76. Smallest model OPT-1.3B, 29.84 at "0.80", with no full-precision row.
- Its demo run calibrates on the set it reports perplexity on.
- Its own tables contradict its text in three places: the two components alone each score better than the two together; group size 64 beats 128 and the text says larger is better; the random-flip table is not monotonic.

### 3E. Answer

(a) What training only the scales recovers.

- From a model never trained end to end, a large share of the gap, fast: 62% at 2 bits on 7B with 17 million tokens of plain text, and at 1 bit a quarter off perplexity and 6 points of accuracy on 3B with a quarter of a million tokens.
- From a model whose codes are already well fitted, a smaller share: 20% of the remaining gap in the one clean measurement. The one case on a released, trained low-bit model (OpenBonsai on the ternary 9B) still halved a held-out gap.
- It stops helping early in data. Accuracy is flat after about two thousand sequences, a few million tokens. Perplexity keeps improving a little.
- Finer groups help it a little: groups of 32 against 256 is 1.6 points at 2 bits.
- It has not been measured below 3B, on generation or tool benchmarks, or on a converted embedding or output matrix. Every number is recognition accuracy or perplexity.
- Read against the released 1.7B: its body is the "already fitted" case and its tied matrix is the "never trained" case. The published numbers say the second is where scale training pays. One five-point step is 17% of the released model's gap to its teacher, which is the size of the smaller of the two published effects.

(b) Exact transformations.

- The list is section 3C. Reorderings, per-channel factors, per-head matrices and per-pair rotations fold away at no cost. Per-token factors and transforms on activations do not.
- No error reduction from the exact, foldable ones is published at 2 bits or below.
- For choosing which 128 weights share a scale: two of them apply and S3 already holds both. Reordering the MLP's inner channels regroups the down projection. Reordering the residual channels regroups every residual reader and the tied matrix with one shared order. The attention output matrix cannot be regrouped, as the specification already says. This batch adds one constraint: query and key channels move only as whole pairs.
- For a model that is already binary: nothing. An exact transformation leaves the function as it is, so it cannot improve the model. A reordering across groups puts two magnitudes in one group, so scales must be fitted again and the function changes. The knowledge of a better grouping lives in the teacher's weights, not in the binary model's.

(c) STBLLM.

- Below one bit only by a count that leaves out most of what is stored. By a full count it is about 3.5 bits. No training, results on perplexity that collapse on the newest 8B model, and an in-sample demo.
- Nothing carries to our format: zeros and several magnitudes inside a group are both outside one sign and one scale for each 128 weights.

### 3F. What it means for the next five points

- The scale-only trial is cheap to read. Published scale training saturates within a few million tokens, so a short ladder of budgets tells quickly whether there is a slope.
- Where to expect its gain: the tied matrix first. It is the one part of the released model in the state where scale training has its large published effect, and it is 2.4 million scales. The trial's tied-matrix arm should not wait on a condition; it is the main arm, with the body's scales as the second.
- The loss: one precedent uses next-token loss on text, the other the teacher's distribution. Both work. The teacher's distribution is the choice already made, and nothing here argues against it.
- Grouping stays where it was. No published evidence, an existing script trial that measures its ceiling, and no use on a binary model.

Probabilities:

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from the released 1-bit 1.7B reaches a step | 55% | 57% | Two more measured cases of scale training with frozen codes, one at 1 bit. The large effect is on untrained scales, which is the tied matrix's state. All of it is recognition and perplexity, none at this size |
| Sign and scale training from the same model reaches a step | 67% | 67% | Settings sharpened, nothing on its odds |
| Either of the two | 74% | 75% | |
| A better choice of groups adds points on its own (idea I1) | Under 5% | Under 5% | No evidence found at any width |
| Our own conversion by a published 1-bit route beats the released model | Under 5% | Under 5% | The best post-training 1-bit result keeps 79% of recognition accuracy at 8B in another format |

### 3G. Still unknown

- What scale training returns on a tied embedding and output matrix. Unpublished. The scale-only trial's first arm answers it.
- Whether the gain shows on generation and tool benchmarks. The same trial.
- The size of any error reduction from regrouping at 1 bit. S3.

## 4. Across the three items

- The three items point at the same place from three sides. Item 1: the repair that works on stored weights is at the output, and the tool-call damage is a shift on an output token. Item 3: scale training has its large effect on scales that were never trained. Batch 3: the tied output matrix of the released 1.7B was never trained. The first thing to train is the tied matrix's scales, and the first thing to measure is whether the failures are of the kind an output repair can reach.
- That measurement is one table: margin survival by decision kind on the released model against its teacher. It turns "what to repair first" into a reading: slope high with an offset means the output and scales; slope low means signs.
- The published 1-bit training recipes do not hold the next step. The best of them on our own teacher lands near where the released model already is, with an easier format. They supply settings for sign training, not a route.
- A reference fingerprint of ordinary 1-bit training is available from public files without training anything. It is the missing comparison for every reading of PrismML's fingerprint made so far.
- Decoding rules are the strongest published repairs at the small end and are outside what the ruler counts. Their existence is a reason to fix the ruler's decoding and allowances in writing before the first run.
- Everything about failure kinds in this batch is on rounded models. Whether a trained 1-bit model fails the same way is the open fact under all of item 1.

## 5. Probabilities after this batch

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from the released 1-bit 1.7B reaches a step | 55% | 57% | Section 3F |
| Sign and scale training from the same model reaches a step | 67% | 67% | |
| Either of the two | 74% | 75% | |
| An on-policy stage adds at least a third of a step | 50% | 52% | Section 1G |
| The tool-calling loss of the released 1.7B is mainly a one-sided shift on the decision to call | Not held | 30% | Section 1G |
| The published full-precision ParetoQ files are the true parents of the 1-bit files, so a reference fingerprint can be computed | Not held | 70% | The README lists them side by side; the model cards are unread |
| A better choice of groups adds points on its own | Under 5% | Under 5% | |
| Our own conversion by a published 1-bit route beats the released model | Under 5% | Under 5% | |

## 6. Sources found in this batch that the plan does not yet hold

- QuEST, https://arxiv.org/abs/2502.05003, code https://github.com/IST-DASLab/QuEST
- ParetoQ's code and released model list, https://github.com/facebookresearch/ParetoQ
- EfficientQAT's code, https://github.com/OpenGVLab/EfficientQAT
- FPTQuant on arXiv, https://arxiv.org/abs/2506.04985 (replaces the ResearchGate address)
- STBLLM's code, https://github.com/pprp/STBLLM
- "All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs", https://arxiv.org/abs/2609.06161
- "Extreme Low-Bit Inference in Reasoning Models: Failure Modes and Targeted Recovery", https://arxiv.org/abs/2606.02011, code https://github.com/brain-lab-research/quantized-reasoning
- "Flat Score, Amplified Failures: How the Error Budget Masks Damage in Quantized LLM Agents", https://arxiv.org/abs/2607.27275
- "Quantization Meets Reasoning: Exploring and Mitigating Degradation of Low-Bit LLMs in Mathematical Reasoning", https://arxiv.org/abs/2505.11574
- "Same Score, Different Model: Two Regimes of Quantization Damage Below and Above the Accuracy Plateau", NeurIPS 2026 workshop, https://neurips.cc/virtual/2026/160501

## 7. Not read

- The body of "Same Score, Different Model" and its per-question files. Only the abstract page opened; the page holding the paper needs an approval that was not answered.
- "One Model, Two Precisions" (https://arxiv.org/abs/2611.16478), surfaced by the same search. It uses disagreement between two precisions of one model to detect wrong answers, which is a use of the damage and not a study of it. Not opened.
- The model cards of ParetoQ's released files. They decide the two checks in section 2E, and the model host is not reachable from this workspace.
- Every source listed for the batch was read whole. All were read through extractions that condense; where an extraction marked a table as garbled, the numbers from that table are left out above.
