# Batch 3 findings

First reviewer's work on the three items of batch 3. No run was made. Probabilities are judgments. The second reviewer has the same three items and has not seen this document.

Reference figures: the released 1-bit 1.7B keeps 70.2% of Qwen3-1.7B on the ten-benchmark suite with thinking off. One five-point step is 29.1 summed points. The largest losses are MATH-500 39.6, BFCL 36.9, MMLU-Redux 23.6, GSM8K 16.8, MBPP+ 15.9, HumanEval+ 12.2.

## 1. What the released 1-bit model's weights show

### 1A. What was read

| Source | How much | Route |
|---|---|---|
| The outside reproduction study, https://github.com/ThakiCloud/bonsai-1bit-repro | REPORT.md, results.json, paper/main.tex, README, and all five scripts, each in full | Repository read directly |
| PrismML's launch press release, https://prismml.com/news/prismml-launches-worlds-first-1-bit-ai-model | The technical-details passage as returned by search | Search result |
| A second fingerprint analysis, Kalaris Labs, "PrismML Bonsai: the team and how to reverse-engineer 1-bit LLMs", 28 October 2026, https://kalarislabs.com/blog/prismml-bonsai-team-1-bit-reverse-engineering | The whole page, two extractions | Direct |
| Discussion 62 on the 27B model page, "I took Bonsai 2 27B apart, part 2", https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/62 | The whole thread, one extraction | Direct |
| The config files of prism-ml/Bonsai-1.7B-unpacked and Qwen/Qwen3-1.7B | Both in full | Direct |

### 1B. Facts: how the two published numbers were computed

- The files compared are Qwen/Qwen3-1.7B and prism-ml/Bonsai-1.7B-unpacked, which is PrismML's own release of the 1-bit weights written out as 16-bit numbers. Both are loaded with standard tooling.
- Matrices covered: every two-dimensional parameter with the same name and shape in both, except names containing "embed" or "norm". That is the 196 block matrices. The tied embedding and output matrix is skipped by name, so no figure exists for it.
- Sign change: the share of positions where the sign of the released weight differs from the sign of the base weight, weighted by matrix size. Result 28.38%.
- Scale ratio: weights are flattened row by row and cut into 128s, which puts each group along the input side of one row. For each group, the largest absolute released weight is divided by the mean absolute base weight. The median over a matrix's groups is taken, and the published 2.257 is the median of those 196 medians.
- "Identical to naive": 0.03% of released weights equal the plain sign-and-mean conversion of the base.
- Structure check: on one matrix, the first 2,000 groups each hold exactly one magnitude and no zeros.
- No breakdown is published. The script prints the first four and last four matrices and stores only totals. Nothing by kind of matrix, by weight magnitude or by position exists in this source.

### 1B2. Facts: the second analysis

It reads PrismML's unpacked 16-bit files against Qwen3-1.7B, Qwen3-1.7B-Base and Qwen3-8B. Its sample is the seven matrices of blocks 0, 14 and 27 of the 1.7B, 8,192 embedding rows taken at several places in the vocabulary, and for the 8B two matrices of one block plus embedding and output rows. Its script is printed in the page; no repository.

- The tied embedding and output matrix of the 1-bit 1.7B is not trained. Its signs agree with the base in 99.9% of places and its scales are within about 1% of the group mean. It is the plain sign-and-mean conversion.
- In the 8B, where the two matrices are separate, the embedding is the same plain conversion (99.8% to 99.95%, scale ratio 1.000) and the output matrix is trained: the rows of the first 128 token numbers agree in 80% of signs with a median scale of 1.70 times the plain value; 128 rows starting at token 100,000 agree in 90% with scales within 1%.
- The body of the 1.7B is trained. Sign agreement is 71% on average and 64% to 79% by matrix. Within each group, 6.7% of the largest tenth of weights changed sign and 47.5% of the smallest tenth. Its cosine to the base is 0.50, against 0.79 for the plain conversion.
- Body scales: the median ratio to the group mean is 2.1 in this sample, about 1.2 in the query matrices and above 3 in the value and up matrices. The scale's correlation with the base group's mean is about 0.9 in some attention matrices and about zero in the last block's feed-forward matrices.
- Normalization gains barely moved: under 0.1% in blocks 14 and 27. The first block's input gain moved 12%.
- Every matrix checked is closer to the post-trained Qwen3-1.7B than to Qwen3-1.7B-Base.
- The first-generation ternary 1.7B: embedding 100% plain conversion; body 86% agreement on non-zeros, scale ratio 1.9, 39% zeros.

### 1B3. Facts: the thread and the config files

- The thread is about the ternary 27B and matches the forensics repository read in batch 1. No PrismML staff reply. It states independently that the reproduction study's "2.1 times" result is produced by scoring on the calibration passage, and that the same settings collapse by a thousand to thirty-five thousand times on held-out text.
- Its 1.7B ternary table: a mirror map at two settings is 23.01 times the teacher's perplexity against 2.93 for the straight-through control; the rotation inside training takes 2.09 to 1.37; a managed decay of the rate reaches 1.14 and 1.11 on two seeds; a constant rate diverges past 16,000 steps; 32-bit weights behind the codes change nothing (23.94 to 23.79).
- One new experiment: on a frozen ternary model with routed experts, 6.29M correction parameters placed on the residual stream recover 158 times in perplexity, and 52M placed inside the experts recover 6 times. Where a correction sits mattered more than its size. It uses extra full-precision parameters, so it is outside our format.
- Config files, released 1-bit 1.7B against Qwen3-1.7B: vocabulary 151,669 against 151,936; maximum positions 32,768 against 40,960; position scaling of the YaRN kind with factor 4.0 over an original length of 8,192 against none; both tie the embedding to the output matrix; the same 28 blocks, widths and head counts.

### 1C. Facts: what the study's quality claims rest on

- "Near-lossless" is perplexity on one fixed passage of six sentences repeated four times: 3.507 for the base against 3.492 for the released model, and 2.027 against 1.971 on a second passage. The report itself says benchmark retention was not checked.
- The study's own conversions with public methods are measured in sample. The activation statistics that drive its error compensation come from one forward pass over the same passage the perplexity is then measured on.
- Its best "pure 1-bit" figure (perplexity 4.213 against 2.027) uses a random rotation that is folded back into the matrix afterwards. The stored matrix is then dense, not signs and group scales.
- Multiplying the plain conversion's scales by 2.0, 2.26 or 3.0 makes it worse, on a model that is already collapsed.
- The study reasons that sign agreement far above 50% shows an unmodified base and therefore no retraining. The inference does not hold: a model trained from the base also keeps most signs. The study attributes a "no retraining" claim to PrismML; PrismML's whitepapers contain no such statement (batch 1).
- PrismML's launch press release says the 1-bit Bonsai 8B "has been trained using Google v4 TPUs". This is PrismML's own statement that a first-generation 1-bit model was trained. It gives no data, loss or budget.

### 1D. Reasoning on paper about the 2.257

This is inference, not a measurement.

- The scale is read from written-out weights, not from a packed field. The idea that 2.257 is a storage convention read as a scale (the MLX packing stores twice the scale) is not supported by this script. It survives only if the unpacked release itself were written with a doubled magnitude, which the cross-check between packagings in the S2 specification settles.
- A group has one magnitude s and signs S. Three natural rules for s give three different ratios to the mean absolute base weight:

| Rule | What it preserves | Ratio it predicts |
|---|---|---|
| Least-squares fit to the base weights for the stored signs | Weight error | Below 1 once signs are flipped: 1 minus twice the magnitude-weighted share of flipped signs |
| Root-mean-square of the base group | The group's norm | About 1.25 for bell-shaped weights, 1.41 for heavier tails |
| Sum of squared base weights divided by the sum of sign times base weight | The size of the group's projection onto the base, that is, the amplitude of the signal the group passes on | 1.57 for bell-shaped weights and 2.0 for heavier tails with no flips; 2.0 to 2.3 with 5% to 15% of weight mass flipped |

- Only the third rule lands near 2.26. So the published total is about what scales look like when they keep the amplitude of what each group passes on, not when they minimize weight error. End-to-end training against a teacher would push scales the same way.
- The second analysis shows the total hides a wide spread: about 1.2 in query matrices, above 3 in value and up matrices. No single rule gives 1.2: the third rule's floor is 1.57. And in the last block's feed-forward matrices the scale has no correlation with the base group's size. So the body's scales were trained freely, at least in part.
- This is testable from weights alone, per group: divide the released scale by each of the three closed forms and see which ratio clusters tightly at 1.
- If the third rule fits tightly, the scales carry little that is specific to PrismML's recipe: they follow from the signs. That would lower the headroom of scale-only training. If no rule fits tightly, the scales were trained freely and hold information of their own.

### 1E. Answer

- The released 1-bit 1.7B is two different things. Its body, 82% of the weights, is trained: signs and scales both moved far from the plain conversion. Its tied embedding and output matrix, 18% of the weights and the whole of the last decision, is the plain conversion and was never trained.
- PrismML did train the output matrix where it was a separate matrix, in the 8B. Of the two row ranges sampled there, the first 128 token numbers moved far more than rows near token 100,000.
- The two published totals (28.38% and 2.257) are over the 196 block matrices from PrismML's unpacked release. The second analysis adds breakdowns on a sample of three blocks: by matrix type for scales, and the top and bottom tenth by magnitude for signs. Nothing exists by position, and nothing for all 28 blocks.
- The file settings differ in vocabulary size, maximum length and position scaling. Each model has to be run with its own.
- The study's reading (rounding with error compensation, no retraining) is not supported by its own evidence. Its error-compensated conversions never reach a working model out of sample, and its argument from sign agreement does not separate training from rounding.
- PrismML's press release says a first-generation 1-bit model was trained.
- The S2 specification already asks for every missing breakdown. This reading adds one test to it, the three closed-form scale rules, and one expectation: the tied matrix should come out as the plain conversion.
- Inference, to be tested: in Qwen's vocabulary the lowest token numbers are single characters, among them digits, quotes, brackets and braces. Those are the output rows that moved in the 8B sample. In the 1.7B they were not moved at all, and the 1.7B's two largest losses are mathematics and tool calling, where the 8B keeps 78% and 81% against 46% and 49%. Part of the 1.7B's loss may sit in output rows that were never trained.

### 1F. What it means for the next five points

- The body of the first-generation 1-bit 1.7B was trained: 90% before, 97% after.
- The tied embedding and output matrix of the 1.7B was left as the plain conversion: 85%. One source, a sample of rows, supported by the first block's input gain being the only gain that moved.
- Scale-only training reaches a step: 50% before, 58% after. The body's scales are already trained, which takes headroom away. The tied matrix's scales, 16 per token, have never been trained, and they sit at the last decision, which adds headroom of a kind nobody has used.
- The paired damage map (S4) gains a sharp question: with the teacher's full-precision matrix put in the output role of the released model, and nothing else changed, how many lost items return.
- The reproduction study's error-compensated conversion is the reference implementation for "rounded with compensation" in trial M4. Its scale is the mean of the error-updated block and its signs are those of the error-updated weights, column by column, so its sign changes should rise along each row. S2 already measures that trend on the released model.

### 1G. Still unknown

- Which 8,192 rows of the tied matrix were sampled, and whether all rows are the plain conversion.
- The breakdowns over all 28 blocks, by position, and by matrix type for sign changes.
- Whether the released model was trained with its declared position scaling or had it added afterwards.
- Whether the 4B, which keeps 61% of tool calling, ties its matrices and how they were treated.

## 2. Bringing reasoning back with the model's own text

### 2A. What was read

| Source | How much | Route |
|---|---|---|
| "Right On Q" (the method is called OnQ), https://arxiv.org/abs/2610.29378 | Abstract page and the whole paper, one extraction | Direct |
| DiscQuant, https://arxiv.org/abs/2501.06417 | The whole paper, one extraction; the code repository's README in full, https://github.com/jerry-chee/DiscQuant | Direct; repository read directly |
| On-policy distillation (arXiv 2609.26708) and "What Makes Low-Bit QAT Work" (arXiv 2601.14888) | Read in batch 2; figures reused | |

### 2B. Facts: OnQ

- Format: 2-bit and 3-bit weights with a scale and an offset per group of 128, block matrices only. Qwen3-1.7B, 4B and 8B. Scores are with reasoning on (the teacher's MATH-500 is 90.13).
- Stage 1, block-wise calibration: 4,096 windows of 2,048 tokens of reasoning text (mathematics, code, science, general), each block trained to match the teacher's block output.
- Stage 2, on-policy distillation: the converted student writes one answer per prompt; the same-size teacher scores the student's own partial answers. The loss mixes, for each candidate next token, the teacher-to-student and student-to-teacher divergences in proportion to who gives the token more probability. 25,600 prompts (mathematics 7,680, code 7,680, science 3,840, general instructions 5,120, constrained instructions 1,280), 128 per step, 400 steps for 1.7B, constant rate 1e-6, weights and scales trained. Token count and compute are not reported. No code link.
- Qwen3-1.7B at 2 bits, teacher in brackets: GSM8K 79.05 (90.55), MATH-500 69.33 (90.13), HumanEval+ 47.76 (79.07), MBPP+ 42.59 (68.96), MMLU-Redux 55.49 (74.36), GPQA Diamond 27.10 (38.72), IFEval 55.70 (71.10). Average of nine 45.24 (67.58), 66.9%.
- By stage, average of nine: plain rounding 3.91, after calibration 23.35, after on-policy distillation 45.24. Best baseline trained on fixed text 40.82.
- At 3 bits: 60.77 of 67.58, 89.9%; calibration alone 54.58.
- The comparison that isolates the idea, Qwen3-1.7B at 2 bits, same calibration:

| Training after calibration | MATH-500 | HumanEval+ | MMLU-Redux |
|---|---|---|---|
| Fixed teacher answers, forward divergence | 59.00 | 39.63 | 52.28 |
| Fixed teacher answers, the mixed divergence | 61.00 | 42.07 | 52.68 |
| The student's own answers, the mixed divergence | 69.40 | 48.78 | 55.75 |

- What does the work, 400 steps from a cold start on mathematics prompts only:

| Objective | MATH-500 | HumanEval+ | MMLU-Redux |
|---|---|---|---|
| Start | 41.40 | 3.66 | 45.12 |
| Student-to-teacher divergence | 63.00 | 10.98 | 48.18 |
| The same plus rewards for correct answers | 66.00 | 4.27 | 48.84 |
| Teacher-to-student divergence | 66.20 | 11.59 | 48.82 |
| Rewards alone | 31.40 | 0.61 | 34.05 |
| The mixed divergence | 67.20 | 10.98 | 49.58 |

- The failure it repairs: in the calibrated 2-bit student, repeated tokens rise from 6.7% of the first 4,000 answer tokens to 21.1% past 8,000, and fall to about 1% everywhere after 100 on-policy steps. Answers cut at the limit, averaged over nine benchmarks at 2 bits on 1.7B: 26.49% after calibration, 3.86% after on-policy distillation, 9.47% to 46.28% for baselines trained on fixed text.
- Not covered: tool calling, anything under 2 bits, teacher size.

### 2C. Facts: DiscQuant

- It only chooses, for each weight, the grid point above or below it. The grid and its scales are given. Each weight gets a variable between 0 and 1; the variables are trained with distillation to the original model plus a term that pushes them to 0 or 1; the few left in between are rounded greedily.
- Its theory: with m data samples, all but a number of weights proportional to m can be rounded with small expected error, if the model's gradients lie close to a low-dimensional space.
- Evidence: Phi-3-mini 3.8B and Llama-3.1-8B at 3 to 4.5 bits, 8,192 samples of 2,048 tokens, 1,024 iterations. GSM8K on Phi-3-mini, nearest rounding, error-compensated rounding, DiscQuant: at 3.0 bits 1.0, 2.3, 26.8; at 3.25 bits 31.0, 54.3, 64.2; at 4.0 bits 62.2, 71.5, 77.3; the original scores 84.4. On Llama-3.1-8B at 3.0 bits 0.5, 3.6, 14.3 of 77.0. Nothing under 3 bits.
- Its loss is the divergence to the original model's next-token distribution. In its own ablation that plain loss beat losses on intermediate layers and mixtures of the two. OneBit found the opposite for hidden states (batch 2); the two results are at different bit widths and starts.
- Its theory is proven for a linear stand-in for the loss, and the shipped algorithm is a heuristic. It does not report how many weights end away from nearest rounding. Scales are not optimized in its reported runs.

### 2D. Answer

- What brings mathematics and code back is training on the student's own answers with the teacher scoring every token. Two independent papers now show it on Qwen3-1.7B: this one at 2 and 3 bits, the batch 2 paper at 1.88 and 2.79 bits. Over the same loss on fixed teacher answers it adds 8.4 points of MATH-500, 6.7 of HumanEval+ and 3.1 of MMLU-Redux.
- The teacher's per-token score does the work. Rewards for correct answers add little on top and, alone, leave the model worse than it started. This answers a question batch 2 left open, and it removes the need for answer checkers and code tests in training.
- Knowledge does not pay for it: MMLU-Redux rises with it.
- The same-size teacher is used throughout. The prompts are public reasoning sets; the answers are the student's.
- It was run with full-precision weights behind the codes and a full-precision embedding and output matrix. Nothing in the method needs them: the loss is on outputs, and the trained parameters are weights and scales. Whether it works when the weights behind the signs are only the signs themselves is untested.
- DiscQuant is a rounding method for 3 and 4 bits and is not a candidate. One thing carries over as a design fact: at 1 bit its variable between 0 and 1 is a relaxed sign, a released binary model starts with every variable at 0 or 1, and its theory says only a small number of weights, tied to the amount of data, need to leave their corner.

### 2E. What it means for the next five points

- An on-policy stage adds at least a third of a step after sign and scale training: 45% before, 55% after. A second paper on our teacher, a matched comparison, and no need for rewards.
- Sign and scale training from the released model reaches a step: 63% before, 65% after.
- The mix of training text is now documented twice for this teacher: mathematics, code, science and instruction prompts, with the student's own answers.
- The loss for the scale-only and sign-and-scale trials has a measured ranking on this teacher: the mixed divergence, then the teacher-to-student divergence, then student-to-teacher, within 1 to 4 points of each other on the student's own answers.
- The baseline run's failure split still sets the size of the prize. The released 1-bit model was scored with thinking off, where answers are short. The repair is largest on long answers.

### 2F. Still unknown

- Token counts and compute of the on-policy stage.
- Its effect on tool calling. No paper measures it.
- Whether the gain holds from a model that already keeps 70% on a suite scored with thinking off.

## 3. Training quantized weights faster and under control

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| WinQ, https://arxiv.org/abs/2605.17471 | Abstract page and the whole paper, one extraction | Direct |
| WinQ's code, https://github.com/facebookresearch/WinQ | The reset routine, the quantizer file, the sample training script and the README, in full | Repository read directly |
| "Latent Weights Do Not Exist" (Bop), https://arxiv.org/abs/1906.02107 | The whole paper, one extraction | Direct |
| "Error Diffusion Replaces Latent Weights: Training Binary-Weight Language Models on a Few Bits of Dithered State", https://arxiv.org/abs/2610.34566 | The whole paper, one extraction | Direct |

### 3B. Facts

- The problem it names: training of quantized weights settles in flat regions near saddle points, and more so at fewer bits. On LLaMA-3-1B after 80 thousand steps the largest curvature is about 6 at 3 bits, 2 at 2 bits and under 1 at 1 bit, and the share of directions with almost no curvature is 41%, 55% and 63%.
- What it changes: at long intervals the full-precision weights behind the codes are pulled part of the way to their quantized values (a factor of 0.1 to 0.6, at most three times in a run); and at every step the gradient is taken after adding small random noise to those weights.
- Evidence at equal cost, 20 billion tokens, next-token loss, no teacher, against ParetoQ:

| Setting | Perplexity | Accuracy |
|---|---|---|
| LLaMA-3-1B, 1 bit | 16.9 to 15.3 | 51.9 to 52.6 |
| LLaMA-3-1B, ternary | 14.0 to 12.9 | 54.7 to 55.6 |
| LLaMA-3-1B, 2 bits | 12.5 to 11.9 | 56.7 to 56.6 |
| LLaMA-3-1B, 3 bits | 10.9 to 10.9 | 57.2 to 57.8 |
| Qwen3-0.6B, 1 bit, 8-bit activations | 64.0 to 61.9 | |
| Qwen3-1.7B, 2 bits, 8-bit activations | 22.2 to 21.8 | |

- Its speed-up is 1.5 to 2.8 times for 1-bit to 2-bit weights.
- Ablations at 1 bit on LLaMA-3-1B, perplexity: no pull 16.5; pull of 0.2, 0.4, 0.6, 0.8 gives 15.5, 15.3, 15.5, 16.0; pull without noise 16.0; noise at half, one, two and four times the chosen size gives 15.7, 15.3, 16.3, 18.5.
- The best settings change with model, bit width and batch size. Gains on Qwen are small.
- It does not use a teacher, and it does not measure how many codes change.
- From its code: the 1-bit quantizer is the sign with one learned scale per output row; the gradient reaches a weight only while its size is under that scale, so it is a clipped estimator whose clip is the learned scale; noise is added to the weights behind the codes and to the scales. The reset in code keeps a fraction alpha of the weight and takes the rest from its quantized value, the reverse of the paper's formula as extracted, and the sample script uses alpha 0.2. Whichever convention the tables use, pulls of 0.6 to 0.8 toward the quantized value beat none.

### 3B2. Facts: training binary weights with nothing behind the sign but a small counter

- Bop (2019, vision models) is an optimizer whose only action is to flip a weight, when a gradient signal that stays consistent over steps passes a threshold. It reads the size of the weight behind a sign as inertia against flipping, nothing more. It proves that the binary weights are unchanged when the learning rate and the starting size are scaled together, so only their ratio matters. Settings that flip aggressively learn fast and then level off at worse accuracy; a threshold that filters weak signals helps most; settings that flip too rarely barely learn. On ImageNet it is 0.2 to 1.7 points above ordinary training.
- The error-diffusion paper (2026) applies the idea to language models. Each weight keeps its sign and a counter of 2 to 8 bits. The gradient, divided by the scale and multiplied by one rate, accumulates in the counter; the sign flips when the counter points away from it and reaches the threshold. Scales are fixed per layer; embeddings, normalizations and the output matrix are full precision. Models are trained from scratch, up to a 19M binary core, on byte-level and tokenized text.
- Against ordinary training with full-precision weights behind the signs, its loss is within 0% to 3% at every size when a cap is on.
- It measures sign changes. In a 19M run about 37 to 38 thousand signs flip per step (0.2% of the core). In an avalanche the count doubles to 79 thousand, validation loss rises by 0.6 to 1.4 nats within 100 steps, and the core then runs at a tenth of its flip rate. Two of five uncapped runs stalled this way. A cap on each weight's movement per step (a quarter of the distance to the threshold) removed every stall: the gap to ordinary training fell from 10.2% and 16.5% to 1.0% and 0.3%.
- It recommends a drive of 1.0 to 1.3 thousandths of the flip distance per step, found by a 250-step probe.
- One experiment matches our starting point in miniature: a trained binary model has everything behind its signs thrown away and is then adapted to new text for 5,000 steps. Loss falls from 2.32 to 1.520, against 1.533 for continuing with the full state kept.
- Limits: 19M at most, losses only, no benchmark, no teacher, no conversion of a pretrained model. Code: https://github.com/pierreolivierbonin/error-diffusion-binary-weight-lms

### 3C. Answer

- It holds at 1 bit and at 1B, with a modest gain: 1.6 points of perplexity and 0.7 of accuracy at equal cost. It is a setting, not a route.
- Its steps assume full-precision weights behind the codes. Read for a model that has none, they say two useful things:
  - A full pull puts every weight behind the codes exactly on its quantized value. That is the state a released binary model is in. Partial pulls toward that state help, and a pull of 0.8 still beats none. Starting sign training from bare signs is therefore a strong form of something that helps, not a handicap.
  - Noise at the right size helps and at four times that size destroys the gain. When every weight behind the signs has the same magnitude, the noise size relative to that magnitude sets how many signs move in a step. That is the budget on sign changes in another form, and it has to be set, not left to chance.
- Controlling sign changes directly is published and measured, at small scale. The error-diffusion paper shows the failure a budget prevents (an avalanche of flips, then a stall), the control that prevents it (a cap on movement per step), a working range for the drive, and that training can resume from a binary model with nothing behind its signs. ΣΔ-Sampler's cap (batch 2) is the same finding at larger scale with thinner evidence.

### 3D. What it means for the next five points

- The risk that sign training cannot start from a model with only signs and scales: lowered again. OneBit starts there (batch 2), and WinQ shows moving toward that state helps.
- The flat landscape at 1 bit is a measured reason for slow sign training and for giving scales a much higher rate than signs, as the published recipes do.
- The budget on sign changes (idea I13) stays a required setting of sign and scale training, and now has a measured form: a cap on each weight's movement per step, a drive near a thousandth of the flip distance per step set by a short probe, and the count of flips per step logged as the health signal. With equal magnitudes behind the signs this is the ratio of step size and noise to that magnitude.
- Two sources conflict on the estimator. "Linger and Lose" finds the clipped estimator collapses on tiny models from scratch. ParetoQ and WinQ train 1-bit LLaMA-1B with a clipped estimator whose clip is the learned scale. This joins the schedule conflict as a point the sign-and-scale specification has to settle.
- Probabilities do not move on this item.

### 3E. Still unknown

- Whether WinQ's noise step helps under a distillation loss.
- Sign changes per step in a model above 19M, and in one converted from a pretrained model.

## 4. Across the three items

- Three papers on Qwen3-1.7B now agree on the shape of a working repair: calibrate, then train on the student's own answers with the same-size teacher scoring every token. None is at 1 bit, none has a converted embedding or output matrix, none measures tool calling.
- The scale-only trial can carry the on-policy arm from its start. The loss needs no rewards, so the arm needs no answer checkers.
- The question of what the released model's scales are has a sharper form: do they follow from the signs by a closed rule, or were they trained freely. One added table in S2 answers it and moves the odds of scale-only training in a stated direction either way.
- Starting from a binary model with nothing behind its signs is now supported from three directions: OneBit starts there, WinQ shows moving toward that state helps, and the error-diffusion paper resumes training from it and matches the run that kept everything.
- The largest fact of this batch is about where PrismML did not train. The tied matrix of the 1.7B is the plain conversion. Scale training there, with its two roles handled separately (idea I12), is the least explored part of the released model and the cheapest to try, because it is 2.4 million scales.
- The reproduction study should no longer be cited for "no retraining" or for "public methods reach twice the perplexity". Neither survives a reading of its scripts.

## 5. Probabilities after this batch

| Candidate | Before | After | Reason |
|---|---|---|---|
| Scale-only training from the released 1-bit 1.7B reaches a step | 50% | 58% | The tied embedding and output matrix was never trained; the body's scales already were |
| Sign and scale training from the same model reaches a step | 63% | 67% | Second paper on the teacher for on-policy training; starting from bare signs supported again; an untrained output matrix to train |
| Either of the two | 70% | 75% | |
| The tied matrix of the released 1.7B is the plain conversion | Not held | 85% | One analysis on a sample of rows |
| An on-policy stage adds at least a third of a step | 45% | 55% | Matched comparison on the teacher; rewards not needed |
| The body of the first-generation 1-bit models was trained | 90% | 97% | Second analysis: half the smallest weights changed sign, scales uncorrelated with the base in places; PrismML's press release says the 8B was trained |
| The published 2.257 is a storage convention | Not held as a number | Under 10% | The script reads written-out weights |

## 6. Sources found in this batch that the plan does not yet hold

- PrismML's launch press release, https://prismml.com/news/prismml-launches-worlds-first-1-bit-ai-model
- Kalaris Labs, "PrismML Bonsai: the team and how to reverse-engineer 1-bit LLMs", https://kalarislabs.com/blog/prismml-bonsai-team-1-bit-reverse-engineering
- Discussion 62 on the 27B model page, https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/62
- DiscQuant's code, https://github.com/jerry-chee/DiscQuant
- WinQ's code, https://github.com/facebookresearch/WinQ
- Helwegen et al., "Latent Weights Do Not Exist: Rethinking Binarized Neural Network Optimization", NeurIPS 2019, https://arxiv.org/abs/1906.02107
- "Error Diffusion Replaces Latent Weights: Training Binary-Weight Language Models on a Few Bits of Dithered State", 2026, https://arxiv.org/abs/2610.34566, code https://github.com/pierreolivierbonin/error-diffusion-binary-weight-lms

## 7. Not read

- Nothing listed for this batch is left unread. The Kalaris page and the thread were read through extractions that condense; the numbers above are every number those extractions returned.
