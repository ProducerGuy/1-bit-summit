# Batch 4: the two reviews compared

Both reviewers worked the same three items without seeing each other's work. The first reviewer's findings are in `batch-4-findings.md`, the second reviewer's in `batch-4-second-reviewer.md`. This document records where they agree, what each found that the other did not, what was checked at source, where the probabilities differ, and what is adopted.

## 1. Agreement

- No source in the batch shows a five-point gain at 1 bit, at 1.7B, with the embedding and output matrix converted. Every result is evidence for a mechanism only.
- Decisions. The margin after conversion is a shrunken, shifted copy of the margin before. Flip rates can be forecast inside one model, quantizer and bit width once the constants are fitted on converted items, and the constants do not carry between models at 3 bits. The decision whether to call a tool breaks while the choice of tool holds, at 4B and above. The forecast is a sorting aid and earns nothing by itself.
- LFQ repairs the last block through the output matrix, at 3 and 4 bits, with gains of one to three points. A repair that works at the last block does not show the damage was done there.
- The hesitation-word penalty is a decoding change, tested with thinking on, with its strength chosen on the reported results. It is not a conversion result under our ruler.
- ParetoQ: the quantizers, the gate on the gradient, the learned row scale started from mean magnitude, 120,000 steps at 2e-5, about 30 billion tokens at 2 bits and below, the 90 and 10 split as a result about budgets that include pretraining, and the embedding and output matrix left in full precision. Both read the quantizer file.
- QuEST trains from random weights with weights and activations quantized. Its estimator comparison at 1 bit is the useful part: the plain estimator fails, and methods tied to a scale sit within about 1% of each other.
- EfficientQAT: the four cells of its stage table, 16.8 million tokens for the scale stage, the flat curve after about two thousand sequences, and the reading that scale training adds 1.15 points once codes are fitted and far more from a rounded start.
- Scale training with signs frozen fits our format exactly: the gradient of a group scale is the sum over the group of sign times weight gradient, with no estimator.
- The exact, foldable transformations: reordering of MLP inner channels, a factor on the up branch with its inverse on down, an invertible matrix inside a head between value and output, a restricted pair transform for query and key, reordering of residual channels. Runtime Hadamard and per-token factors are not free.
- Reordering can change which weights share a scale in two places only: the down projection (through the inner channels) and every residual reader with the tied matrix (through one shared order of the residual channels).
- The exact-gauge paper optimizes file size under lossless compression. Its "1-bit" is a mantissa bit. Exact transformations save almost nothing there.
- STBLLM is outside the format, and its text on group size contradicts its own table.

## 2. Found by the second reviewer only

Each was checked at source before it was adopted.

| Finding | Check | Result |
|---|---|---|
| LFQ's ablation separates two steps: putting the output matrix into the objective, and switching the loss to cross-entropy. On Llama-3.2-3B the first step alone gives the GSM8K gain (72.40 to 73.09; with cross-entropy 73.01). Cross-entropy adds on IFEval (65.99 to 67.28) | LFQ PDF, Table 8, read again | Confirmed for the FlexRound and Block-AP rows. The OmniQuant row is not readable in the extraction |
| LFQ, Qwen2.5-7B at 3 bits with Block-AP: MMLU 67.09 to 67.06, IFEval 61.00 to 63.77, MATH-500 60.0 to 61.8 | The same | Confirmed |
| The hesitation penalty also raises the full-precision model, so a student's raw gain is not a gain in retention unless the teacher is scored under the same decoding | First reviewer's own table: the 1.5B full-precision row rises 48.5 to 50.7 | Confirmed. Adopted into the ruler |
| ParetoQ's code returns zero, not a sign, for a weight that is exactly zero | Quantizer file read in full | Confirmed: the forward step is the sign function with no rule for zero |
| FPTQuant has released code | Repository read directly: README, transforms file, two settings files | Confirmed. https://github.com/Qualcomm-AI-research/fptquant, ICML 2026, covers Qwen3 |
| A scale-only result must be scored after the scales are rounded to FP16 and stored, with a checksum showing the signs did not change and the bit count unchanged | Reasoning, not a source | Adopted into the scale-only trial's acceptance checks |
| An estimator comparison must hold the rate of sign changes equal across arms, or a slower optimizer passes for a better one | Reasoning | Adopted into the sign-and-scale trial's controls |
| Three losses that are not the same thing: what the format cannot represent, what training failed to find, and a useful state read out across the wrong boundary. A gain in one must not be credited to another | Framing | Adopted as the top-level split of the failure sort |
| The algebra of grouping: two groups each holding 64 magnitudes of 1 and 64 of 10 have squared error 5,184 under their best scales; regrouped as all small and all large, zero | Recomputed: 6,464 minus 3,872 is 2,592 for each mixed group | Correct. It is an illustration, as the second reviewer says |

## 3. Found by the first reviewer only

- The decisions paper in its current, fifth version. It is twice the size of the first version, which is the one the second reviewer read. Only the current version holds:
  - the live BFCL test, where Qwen3-1.7B at 3 bits loses 93% of calls and 96% of tool names, so on our teacher both halves of a call go;
  - the block-by-block test: rounding blocks 16 to 19 of 36 halves the call rate with perplexity up 1%, the last four blocks cost nothing significant, and sparing the last blocks repairs nothing;
  - the call token's fall measured against the rest of the vocabulary, 8.7 logits below its class on Qwen3-1.7B;
  - the bias repair in numbers: all lost calls returned, all correct refusals lost, nothing returned in 12 of 41 conditions.
- ParetoQ's released files: full-precision parents and 1-bit children at 125M to 1.5B, with scores the paper does not tabulate (1-bit keeps 86% to 90% of an eight-task mean) and a stated parentage. The second reviewer reports that no 1-bit scores exist below 3B.
- The idea those files allow: a reference fingerprint of ordinary 1-bit training, to set beside PrismML's. The files are gated behind a form asking for a legal name and date of birth, which the owner declines. An ungated pair is being sought.
- QuEST's quantizer code: its scale is computed at every step, not learned, and its gate passes gradient up to about 2.3 times the scale.
- EfficientQAT's code: the scale stage is 128 optimizer steps of plain next-token loss, no teacher.
- "All for 1-Bit" (arXiv 2609.06161): scale-only training with frozen signs at 1.00 bit, 34.85 to 40.79 on a 3B model with a quarter of a million tokens. The only scale-only measurement at 1 bit in the batch.
- STBLLM's storage: its "0.55 bits" is about 3.5 bits once masks, band labels and scales are counted, by a later paper's full recount. Its demo calibrates on the set it scores. The second reviewer describes the count as including structural tags.
- Four more papers on failure kinds: loops and budget exhaustion at 2 bits (arXiv 2606.02011, with code), failures that repeat the full-precision model's own (arXiv 2607.27275), the failure mix in mathematics with a repair from 332 failure pairs (arXiv 2505.11574), and flips predicted from the full-precision margin (NeurIPS 2026 workshop, abstract only).
- For a model that is already binary, an exact transformation changes nothing and a regrouping cannot be applied without the teacher's weights.

## 4. Not confirmed, and errors

Second reviewer:

- ParetoQ at 1 bit on LLaMA-3 8B is given as 67.8. The paper's Table 1 says 64.1, and its five task scores average to 64.1. 67.8 does not appear in the table.
- "No binary score table below 3B." True of the paper, not of the release: the code's README and the model cards list 1-bit scores at five sizes.
- The decisions paper was read in its first version. Its figures there (median survival 0.33 at 3 bits, forecast error 1.8 points over 868 cells, 482 of 569 cells) are superseded by the current version (0.19 to 0.94 by decision kind, 1.0 point over 1,082 conditions, 642 of 642). The title it reports for the first version could not be checked; the current title is the one in the brief.
- FPTQuant's final version is said to drop the MLP transform. The released code's preset still includes it. Not confirmed.
- STBLLM's bit count is accepted as including its structural tags. It does not include them.

First reviewer:

- "None of these papers measures damage by layer" was wrong. The decisions paper has a block-by-block test and three layer-protection repairs, in appendices read in an earlier session and not carried into the notes. The findings document now reports them.
- "Where: at the output" was an overreach built on that gap. The second reviewer's caution, that a last-block repair is not evidence of a last-block cause, was right. The one layer-by-layer test puts the cause of lost tool calls mid-network. The findings document now says so, and the rise in the scale-only odds that leaned on it is withdrawn.
- A fixed correction at the output was proposed as the cheapest repair for a one-sided shift. The project's own ranking already held that repair at under 5%, for the reason the paper gives. The findings document now says a repair has to depend on the input.
- The LLaMA-3 8B row sat under an eight-task header. It is a five-task mean.
- FPTQuant's code was not searched for. The quantizer file of ParetoQ was not opened until this comparison, though the code was listed as read.
- The model host was reported as unreachable. Only the shell is blocked; the pages open through the read-only route.

## 5. Where the probabilities differ

| Question | First reviewer | Second reviewer | Why they differ |
|---|---|---|---|
| Scale training with signs frozen reaches a step | 55% | 8% | Different starting points and different evidence. The second reviewer prices scale fitting as a generic mechanism from one measurement (1.15 points at 2 bits after codes were fitted) and names the ceiling: scales cannot change a sign. The first reviewer prices the trial as specified: from the released model, on the teacher's answers to task prompts, with a tied matrix whose scales were never trained, and with one measurement on a trained ternary release where scale training halved a held-out gap. The ceiling is real and is the trial's main risk |
| A better choice of groups, alone | Under 5% | 19% | The second reviewer reasons from the algebra and from the fact that the format allows it. The first reviewer weighs two things the second does not have: on another real model, free column factors cut weight error by a quarter and the converted model was no better (`PLAN.md`, section 2M); and a regrouping cannot be applied to the released model, so it belongs to a conversion of our own, which starts far below 70.2% |
| Grouping and scale training together | Not priced apart | 24% | The same split. For the first reviewer this is our own conversion with two improvements, held under 5% against the released model's line |
| A change of training method (gate on the gradient, learned scales) reaches a step | 67% for sign and scale training from the released model | 19% | The second reviewer prices a new 1-bit training method. The first prices continued training of a model already at 1 bit |
| A decision-targeted repair alone reaches a step | 10% for the last-block fit, under 5% for the bias | 16% | Close |

- Neither set moves the other on scale training or on grouping. Both disagreements are settled by trials already specified: the scale-only trial's first rung, and S3 for grouping. S3 runs no model.
- The second reviewer's point that weight error may fall while function does not is the first reviewer's reason for the low number. They agree on the risk and differ on the odds.

## 6. Left open by both

- Margin survival on a model trained after conversion. Every measurement is on rounded models.
- The failure mix of the released 1-bit 1.7B on the ten benchmarks with thinking off.
- Any measured gain from an exact, foldable transformation at 2 bits or below.
- Any published training of a binary tied embedding and output matrix.
- Whether the block-by-block result for tool calls (cause mid-network) holds on Qwen3-1.7B and on a trained model. It is one 4B model at 3 bits.

## 7. Adopted

- Into S4: a margin-survival table by decision kind (answer letter, call or reply, tool name, first argument token, yes or no, a digit): slope and offset of the 1-bit model's margin against the teacher's, on items outside the ruler's test sets. And a block-by-block exchange for the call decision: teacher blocks swapped into the 1-bit model four at a time, call rate recorded, to see whether the cause sits mid-network here too.
- Into M1's records, sorted first by the three losses (cannot represent, did not find, read out wrong): teacher right or wrong; the teacher's margin at its first deciding token; whether the 1-bit answer is the teacher's runner-up; first divergence under teacher forcing with the teacher's entropy there; loop, budget, right answer present and not final; for tool items which part of the call broke; whether the answer parser changed its verdict.
- Into the ruler: any decoding change is scored on teacher and student alike, and retention is the ratio under the same decoding. The suite's allowances (answer budget, retries) are written down before the first run.
- Into the scale-only trial: the tied-matrix arm keeps its condition on S4's exchange test and gains weight from this batch; the middle blocks' scales become a named arm if S4 places the call damage there; acceptance checks: signs unchanged by checksum, scales rounded to FP16 and stored before scoring, bit count unchanged; a short ladder of budgets, since published scale training flattens within a few million tokens.
- Into the sign-and-scale trial's settings: a gate on the gradient set wider than the scale; scales as a computed value times a learned factor starting at 1; magnitudes behind the signs started inside the gate; a rule for an exact zero behind a sign; estimator arms compared at an equal rate of sign changes.
- S3 is unchanged. It already holds both controls the second reviewer asks for: a random-order arm, and a check on a running model that opens when a class of matrices gains 5% or more, since weight error alone has misled before.
- A fifth script trial, the reference fingerprint of ordinary 1-bit training, conditional on finding a parent and child pair that is not gated.
- New ideas I19 (margin survival as the health number that sorts repairs) and I20 (reference fingerprint). The second reviewer's joint program of grouping and scale fitting is recorded under I1 with its 24%, to be settled by S3.
- Odds after the batch: scale-only training 55%, sign and scale training 67%, either 74%, an on-policy stage 52%, the tool-calling loss mainly a one-sided shift 30%, a better choice of groups alone under 5%.
