# Batch 3: the two reviews compared

Both reviewers worked the same three items without seeing each other's work. The first reviewer's findings are in `batch-3-findings.md`, the second reviewer's in `batch-3-second-reviewer.md`. This document records where they agree, what each found that the other did not, what was checked at source, and what is adopted. No run was made.

## 1. Agreement

- The reproduction study's two numbers (28.38% of signs changed, scales 2.257 times the group mean) cover the 196 block matrices only, are read from PrismML's unpacked release, and define scale as the largest released magnitude in a group over the mean absolute base weight. Both reviewers read the script in full and report the same definitions.
- The second analysis shows the released 1.7B's tied embedding and output matrix is close to the plain sign-and-mean conversion (99.9% of signs, scales within about 1%), while the body is far from it. Both reviewers call this the most important fact of the item.
- The config files differ in vocabulary size (151,669 against 151,936), maximum positions (32,768 against 40,960) and position scaling (YaRN with factor 4.0 over 8,192, against none). Each model has to run with its own settings.
- The reproduction study's short-passage perplexity proves nothing about benchmark ability, and its salient-weight variants are outside the format.
- Training on the student's own answers with the teacher scoring every token is the strongest lead of the batch for mathematics and code, and it is shown at 2 and 3 bits, not at 1.
- DiscQuant is a rounding method for 3 bits and above and is not a candidate. Its loss ablation favors plain output divergence over intermediate-layer losses.
- WinQ is a setting, not a route. Its released code applies the reset with the reverse convention of the paper's formula. Both reviewers found this separately.
- Rankings agree: on-policy training first, the forensic lead second, WinQ and DiscQuant last.

## 2. Found by the second reviewer only

| Finding | Checked at source | Weight |
|---|---|---|
| The comparison of on-policy training with fixed answers in "Right On Q" is not matched on prompts. The fixed arms use the baselines' 32,768 question and answer pairs; the on-policy arm uses its own pool of 25,600 prompts. Only the number of answer tokens is matched | Confirmed. The paper says so in the setup of that table | High. The first reviewer called it a matched comparison that isolates the idea. That was wrong and is rewritten. The matched control that does exist is in the batch 2 paper (same prompts, 16 of 16) |
| WinQ on our own teacher at 1 bit: Qwen3-1.7B with 1-bit weights and 8-bit activations goes from perplexity 46.5 and 42.3 average accuracy to 45.9 and 42.4, against 16.2 and 58.2 at full precision | Confirmed in the appendix table. The main-text table prints 42.2 for both | High. The first reviewer reported the gain on LLaMA-1B and only "small" for Qwen. The gain on our teacher is 0.1 point. It is also a published reference for 1-bit training of the Qwen3-1.7B body at 20 billion tokens: 73% of the teacher on eight easy tasks, with the embedding left in full precision |
| The prompt mixture decides code ability: on-policy training on mathematics prompts alone leaves HumanEval+ near 11, and the mixed pool reaches 48.78 | Confirmed, with a correction to the wording: 11 is a gain from a start of 3.66, not a loss. The two figures come from different tables and starts | High for the training-text design |
| DiscQuant's loss ablation in numbers: output divergence alone 64.9; layer outputs alone 54.1; linear outputs alone 60.1; ground-truth tokens 52.7 | Confirmed | Medium. Against adding hidden-state matching (idea I15) |
| More mathematics in DiscQuant's calibration text raises GSM8K and lowers PIQA | Confirmed as a trend; the paper gives figures, not numbers | Medium. A second source for fixing the mixture in advance |
| In the reproduction study an exact zero in the base counts as a changed sign; "identical to naive" is a tolerance match; the final median treats matrices equally whatever their size | Consistent with the script both read | Low. Carried into S2's definitions |
| The 8B's output-matrix findings should not be carried over to the 1.7B's tied matrix; token number is not token frequency | A caution, not a claim | High. It bears directly on an inference of the first reviewer (section 4) |
| The body may have been trained to compensate for a fixed rounded interface, so a working model need not train the tied matrix at all | A reading of the same fact. Not testable from weights | High. It is the opposite reading to the first reviewer's and both go into the register |
| Ledgers to keep apart for every trial: memory used only in training, total conversion compute, operations at inference, stored bits | A proposal | Adopted |
| A bank of failure kinds built from the baseline run, with training text chosen from separate sources by failure kind and the suite checked only at fixed points | A proposal. The ruler already weights training text by failure class and forbids choosing settings on the suite | Adopted as wording for the training-text design; no new trial |

## 3. Found by the first reviewer only

- Discussion 62 in full. The second reviewer could not open it. It confirms independently that the reproduction study's best public result is scored on its own calibration passage.
- The reproduction study's own conversions are measured in sample, and its rotation variant stores a dense matrix. Found by reading its other four scripts.
- PrismML's press release says the 1-bit 8B was trained.
- Arithmetic from the second analysis's two cosines: Qwen3's weights are bell-shaped within groups; about 18% of the weight mass carries a changed sign; the released body passes on 83% to 89% of the base signal's amplitude against 62% for the plain conversion. The second analysis's script was read in full for this.
- "Right On Q"'s objective ablation: rewards alone leave the model worse than it started (31.40 against 41.40), so the teacher's per-token score does the work and no answer checkers are needed.
- "Right On Q"'s failure measurements: repetition by position in the answer, and answers cut at the limit falling from 26.49% to 3.86%.
- The error-diffusion paper (arXiv 2610.34566): sign changes per step measured in binary-weight language models, the avalanche that an uncapped rate causes, the cap that prevents it, a working range for the drive, and training resumed from a binary model with nothing behind its signs.
- Bop in full: only the ratio of learning rate to the size behind the sign matters.
- WinQ's quantizer in code: a clipped estimator whose clip is the learned scale, which conflicts with "Linger and Lose" on the estimator.
- Two tests added to the specifications: the three closed-form scale rules in S2, and the exchange of the tied matrix alone in S4.

## 4. Not confirmed, and two errors

- Second reviewer, error: the DiscQuant rows quoted for Phi-3-mini at 3.0 bits (0.5, 3.6, 14.3 against 77.0) and at 3.25 bits (10.8, 56.3, 58.3) are Llama-3.1-8B's. Phi-3-mini's are 1.0, 2.3, 26.8 and 31.0, 54.3, 64.2 against 84.4. Checked in the paper's two tables.
- First reviewer, error: the on-policy comparison in "Right On Q" was described as matched. It is not (section 2).
- First reviewer, inference now weakened: that part of the 1.7B's loss in mathematics and tool calling sits in untrained output rows for digits and brackets. It rested on the 8B's output matrix having moved most in its first 128 token numbers. The second reviewer's caution stands: two small row ranges in a different model with a separate output matrix do not establish this. It stays a hypothesis, and S4's exchange of the tied matrix is its test.
- Not checked: the second reviewer's reading of "Right On Q" came through indexed copies and summaries, declared as such. Every number of its that could be set against the first reviewer's extraction of the paper agrees.
- WinQ's paper does not say whether the output matrix is quantized. It says the embedding is not.

## 5. Where the probabilities differ

| Question | First reviewer | Second reviewer | Why they differ |
|---|---|---|---|
| On-policy training | 50% that it adds at least a third of a step after sign and scale training | 25% that it delivers a full step from a matched binary baseline | Different quantities. Both rank it first. The first reviewer's figure was 55% before the unmatched comparison was found |
| WinQ | No change to any odds | 7% | Agreement in substance |
| DiscQuant | Not a candidate | 9% | Agreement in substance |
| The forensic finding | Scale-only training from the released model at 55% | 11% that the finding alone delivers a step | Different quantities. The second reviewer starts from a conversion of our own; the first from the released model |

## 6. Left open by both

- Whether training the tied matrix helps or disturbs a body that was trained around its plain conversion.
- Whether every row of the tied matrix is the plain conversion. Only 8,192 rows were sampled, at unnamed positions.
- Whether on-policy training works at 1 bit, with a converted embedding and output matrix, and what it does to tool calling. No paper measures any of the three.
- Token and compute cost of an on-policy stage. The paper gives prompt and step counts only.
- Whether the released model was trained with its declared position scaling.

## 7. Adopted

- Into the training-text design of the scale-only and sign-and-scale trials: a mixture across mathematics, code, science, instructions and tool calls, with quotas fixed before training; the student's own answers scored by the same-size teacher; no rewards.
- Into every trial's records: four ledgers kept apart (training-only memory, total conversion compute including the student's generated tokens and the teacher's passes, operations at inference, stored bits).
- Into the ideas register: the tied matrix as the untrained part of the released model, with both readings; the scale growth as a free by-product closed as false; sign-change control with its measured form; on-policy training with its second source and the limit on that source.
- Into the scale-only trial: scale training of the tied matrix as an arm, decided by S4's exchange test.
- Odds: scale-only training 55%, sign and scale training 67%, either 74%, an on-policy stage 50%.
- Not adopted: a binary adaptation of DiscQuant; WinQ's reset as a method of its own; the second reviewer's own-conversion baseline as the starting point, which batch 2 already weighed.
