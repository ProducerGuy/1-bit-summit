# Batch 9 findings, first reviewer

Three parts: training under a constraint with two paper checks on each candidate method (C125), factorization, rotation and binary-training papers (C125, C132), and what two-value weights can store (C125, C124). Brief: `docs/research/batch-9-prompt.md`. The reading was done before the second reviewer's return was seen, except the sources marked in sections 3A and 4A as opened while checking it.

Odds set before reading: a 1-bit Qwen3-1.7B in the strict format reaches 90% retention by some training, 40%; reaches 99%, 5%.

## 1. Result

Training under a constraint:

- Two methods start at the parent itself and move the model from their first step: the shrinking cage, provided it closes by holding each group's norm and trains the radius, and a smooth map sharpened in stages from zero (published as BinaryLLM). The cage ends exactly in the format by geometry. The smooth map does not and needs a last stage.
- Straight-through training from a model already in the format has a hidden choice that decides what happens first: the latent magnitudes, which the file does not hold. With the plain choice nothing but scales moves for hundreds to thousands of steps, then signs cross in a wave.
- A sign budget is the only method that is in the format at every step and cannot stall. It is straight-through training with a cap on crossings. The public working form, in the double binary factorization repository, flips about one sign in a million per step and forgets its evidence every 50 steps.
- Scale-only training is the exact first stage of any run from a released model.
- No proof read covers any of these as the project would use them. Each proof stops short at a fixed band, a hard phase, or a smooth loss.

Factorization, rotation and binary-training papers:

- Nothing published stores what the project stores, and at 1 bit a single sign matrix is not behind the factorized methods in their own tables.
- A rotation is free only where it can cancel. A single sign matrix has no inside, so only the network's own symmetries are free.
- Boole's storage matches neither RaBiT's code nor NanoQuant's. Its card points to scales trained as free numbers, not group means. The published RaBiT paper trains Boole's own parent, Qwen3-1.7B, at 2 bits and keeps 94% of an easy-task average. RaBiT's code refuses a single path, leaves the embedding and output matrix in full precision, and its own ablation credits its gain to coupling two paths, which one path does not have.
- NanoQuant's largest gain is letting the not-yet-converted matrices retrain to absorb the error of the converted ones: perplexity 206 to 15 on Qwen3-8B.

What two-value weights can store:

- Every measured format stores at most about a quarter of its raw bits as knowledge. At that share the project's format holds 0.28 bits per weight. Two levels are still unmeasured.
- 99% of a fully loaded parent cannot fit by counting. 99% of a lightly loaded one can. The parent's load is unknown.
- 90% does not have to come from stored facts: on the outside harness the points Boole is missing sit mostly in mathematics.
- For one neuron with sign weights, almost every solution is isolated from every other, and the ones training finds are rare connected ones. A trained 1-bit model is such a point. A rounded parent is not.
- The planned capacity measurement lacks a conversion arm, uses too few loads and sizes, and will measure its trainer as much as the format.

Odds after reading: 90% retention in the strict format, 38%. 99%, 4%.

## 2. Part A: training under a constraint

### 2A. What was read

All through a fetch tool that returns an account of a page, not its text. No figures were seen.

| Source | Read |
|---|---|
| BinaryRelax, arXiv 1801.06313 | Whole paper |
| ProxQuant, arXiv 1810.00861 | Whole paper with appendices |
| ASkewSGD, arXiv 2211.03741 | Whole paper with appendices (read in part in batch 6) |
| PV-Tuning, arXiv 2405.14852 | Appendices D to O, added to the main text read in batch 8; the page closes with a publication checklist and nothing else. Code `Vahe1994/AQLM`, branch `pv-tuning`, repository read directly: the optimizer and its helper file |
| Quantized-endpoint descent, arXiv 2609.21834 | Read whole in batch 6; not re-read |
| "Rethinking 1-bit Optimization Leveraging Pre-trained Large Language Models" (BinaryLLM), arXiv 2508.06974 | Read whole in batch 2. Read again here for the two checks; its ablation figures are quoted as verified in the batch 2 comparison |
| The fine-tuning script of the double binary factorization repository (`usamec/double_binary`) | Read in batch 6, which recorded it as a working per-step budget on sign changes. Read again here line by line for its rates and windows. Both compression notebooks: every code cell (section 3) |
| ECO, arXiv 2601.22101; CAGE, arXiv 2510.18784; "Gradients at quantized weights bias to the low-loss basin", arXiv 2606.09012 | Each page as one fetch returned it |

Code, repository read directly: BinaryRelax (`penhunt/binaryrelax`: the quantizer and the training loop), ProxQuant (`allenbai01/ProxQuant`: `reg.py`, the training script, the run scripts), ASkewSGD (`aistats2023/537`: the ImageNet trainer and both binary notebooks). No public code was found for the quantized-endpoint paper.

### 2B. The four papers in one table

| Paper | Where the gradient is taken | What pulls weights to the two values | Scale | How it ends | Proved | Shown at two values |
|---|---|---|---|---|---|---|
| BinaryRelax | At a blend of the float weight and its rounding: `x = (lam * round(y) + y) / (lam + 1)` | `lam` grows 2% an epoch from 1 to about 115 | Mean magnitude, the project's rule | A last fifth of training with hard rounding, which is straight-through training | Convergence of the hard phase only, under a condition the paper does not guarantee. Nothing for the blended phase | From pretrained: ImageNet ResNet-18 63.2 against 60.8 for hard rounding throughout, 69.6 full precision |
| ProxQuant | At the float weight itself | A pull toward plus or minus 1 after every step, strength rising linearly | None | Hard rounding at two thirds, then only normalization statistics settle | Best-iterate stationarity for a fixed pull. Straight-through training with full gradients has a fixed sign pattern only if every gradient points outward, which may never hold | From pretrained ResNet-20: fewer signs changed than straight-through (28% against 38%) with lower error |
| ASkewSGD | At the float weight itself | A band around each value; weights outside are pushed back in; the band narrows from 1 to 0.01 | None | Weights within 0.01 of a value, then a sign is taken | For a fixed band width: iterates approach stationary points of that problem. Nothing as the band narrows | From scratch: ImageNet ResNet-18 46.95, straight-through 45.85, a mirror method 46.38, plain projection 2.58, full precision 66.39 |
| PV-Tuning | At the stored weights | Nothing: weights are always stored values; each step changes the few with the largest update by a full jump | Trained between jumps | In the format at every step | The loss does not rise for a smooth loss | Vector codes near 1 bit, not sign and scale: a 3.8B model keeps 45.3 of 67.6 zero-shot points going from 2.3 bits to 1.03 |
| BinaryLLM | At the forward weight, with the true derivative of the map | A hyperbolic tangent `tanh(t x) / tanh(t)` whose sharpness `t` rises from 0 to about 84 over 20 stages | Mean magnitude times a trained scale | The tangent is swapped for a sign; the gap is called negligible and not measured | Nothing | From pretrained, embedding and output matrix in full precision: at 135M, perplexity 35.0 against 38.1 and an easy-task average of 42.0 against 41.0 for a sign from the start; 1B, 3B and 7B models keep 88%, 88% and 85% of the parent's average on easy tasks |
| Double binary factorization, fine-tuning script | At the stored signs | Nothing: a full-precision copy of the signs drifts with the gradient, and at each step the 1 in 100,000 that drifted furthest against their sign are flipped | A trained vector | In the format at every step | Nothing | Signs of two binary factors, 7B: perplexity 9.25 at 1 bit after 1.38B tokens, as reported in the NanoQuant paper's table |

Three facts from these papers that the checks below use:

- ProxQuant shows straight-through training is the lazy form of projection: gradients pile up in a hidden variable and the stored weight is that variable projected. Its theorem says a sign pattern stays put only when every gradient points outward.
- ASkewSGD states that a weight inside its band feels no pull toward the value. Only the narrowing band squeezes it. Batch 6 reached the same point for a falling cap.
- PV-Tuning measured why few-and-large beats many-and-small: on a 1.1B model the curvature constant is 33 on the 5% of weights with the largest gradients and 9,481 on all weights. A step confined to the few can be some 300 times longer.

### 2C. The two checks, method by method

Notation: a group of 128 stored weights is `w_i = s * b_i`, with signs `b_i` and one scale `s`. "Released model" is a model already in the format. "Parent" is the 16-bit model.

**A. Straight-through training** (latent `L_i`; forward weight `sign(L_i) * mean|L|`).

- Step zero from a released model: exact for any latents with the right signs and mean magnitude `s`. That leaves 127 free numbers per group, the latent magnitudes, which the released file does not contain and the function does not see. They decide which signs move first.
- With the plain choice `L_i = s * b_i` every weight is the same distance `s` from changing sign. An optimizer that moves a latent by at most the learning rate per step needs `s / rate` steps pushing one way before any sign changes: about 360 steps at a rate of 1e-4 for a scale of 0.036, and 3,600 at 1e-5. Until then the method changes scales only. Then the signs with the steadiest push all cross together.
- Step zero from the parent: `L = W` gives plain rounding, a broken model, and not the parent.
- First updates: the scale moves at once, by the average of the signed updates in its group. Signs move only when a latent crosses zero.
- End point: in the format at every step, provided the scale is rounded to 16 bits inside the forward pass. One of the two public trainers read in batch 8 does this and the other does not.
- Scale: it is not a parameter. It follows the latents. With no decay, a latent pushed outward keeps growing and takes the scale with it. At the best scale for the loss the signed gradients of a group sum to zero, so some weights are always being pushed inward: these shrink to zero, change sign, are pushed back, and repeat. Straight-through training with this scale rule has no resting point in general. The weights that keep crossing are the ones the loss wants small.
- This matches the released 1-bit file: its signs on the small weights agree with the parent 55% to 58% of the time, and its scales grew along the signs of the large ones (batch 8, section 3F).

**B. The shrinking cage** (exact gradients on full-precision weights, each group clipped to a cap that falls).

- Step zero from the parent: exact, with the cap at the group's largest magnitude. B is the only candidate that starts at the parent itself.
- First updates from the parent: with the parent as teacher the loss and its gradient are zero at the start. Nothing moves until the cap cuts a weight. The cap schedule drives the method and the loss repairs behind it.
- End point: a falling cap alone does not put every weight on the cap. With the closing rule that holds the group's norm fixed, it does, by geometry: a sphere of radius `r` and a cube of half-width `r / sqrt(128)` meet only at the 2^128 corners. So B with that rule ends exactly in the format with nothing left to round.
- Scale: under that rule the scale is the group's root-mean-square, fixed at the parent's value, which for bell-shaped weights is 1.25 times the mean magnitude. Both released models store more (2.26 times for PrismML's). So the radius has to be a trained parameter of its own. With that change B is a direction on a sphere inside a shrinking cube, times a trained radius, and both get exact gradients.
- Step zero from a released model: exact, and stuck. The group is already at a corner, corners are isolated points, and no sign can move. Only the radius trains. To move signs the cube has to be opened again and closed again, and the opening width is a new schedule the project has not written.

**C. A mirror step** (a hidden variable updated by the gradient, mapped to the weight through a map that flattens at plus and minus the scale).

- With a map that flattens exactly (a clip), step zero is exact from both starts, and C is the lazy form of B: the hidden variable keeps moving past the cap while the weight stays on it. A weight deep past the cap does not come back until the hidden variable has travelled the whole way back. That is the stall of method A again.
- With a smooth map sharpened in stages (BinaryLLM's `tanh(t x) / tanh(t)`), step zero from the parent is exact: at `t = 0` the map is the identity and the forward weight is the parent's weight. The gradient is the map's own, so every step moves the model. This is a second method that starts at the parent itself.
- The same smooth map from a released model has the free latent magnitudes of method A, and at a high `t` its gradient is close to zero away from the sign boundary, so it stalls like A.
- End point: the smooth map reaches the scale only in the limit. BinaryLLM ends by swapping in a sign. At its last sharpness, 84, a weight is within 1% of saturation only if its latent is above about 3% of the mean magnitude; for bell-shaped latents about 2% of weights are short of that. Its paper does not measure the swap.
- Scale: a separate parameter with an exact gradient.
- Evidence for the smooth form: at 135M, perplexity 35.0 against 38.1 for a sign from the start, and one point of easy-task accuracy. Evidence against the clipped form: in ASkewSGD's tables a mirror method scores level with straight-through training on ImageNet and far below it on TinyImageNet (34.9 against 42.4).

**D. A budget on sign changes** (signs changed directly, a limited number per step).

- Step zero: exact from a released model. From the parent it needs a conversion first.
- First updates: always move the model, by construction. This is the one candidate that cannot stall.
- Size of a step: flipping `k` of `n` signs moves the weights by `2 * sqrt(k / n)` of their norm. PV-Tuning's limit of 1% per step allows 25 flips per million weights, about 35,000 flips per step over the 1.41 billion body weights of Qwen3-1.7B. PrismML's 1-bit body differs from the parent in 28% of signs: at that limit, 11,200 steps if none is undone.
- Every flip is a full jump of `2s`. There is no small move in a two-value format, so a first-order score is equally rough for every candidate flip. A flip needs a steady push across batches before it is trusted. That needs a running total per weight, which is the latent of method A under another name. D is A with the count of crossings per step capped and the scale handled apart.
- It exists in code, as batch 6 recorded. Read line by line: the double binary factorization fine-tuning script keeps packed signs and a trained scale. Every 50 steps it opens a random tenth of the matrices: each gets a full-precision copy of its signs that the gradient moves (rate 3e-3, no momentum). After each step the copy's drift against its sign is ranked and the top 1 in 100,000 flip; the first five steps of a window flip nothing. Matrices that are not open train scales only. That is about one sign in a million per step over the model, and the copy is thrown away when the window closes, so no push is remembered for more than 50 steps.
- At that rate PrismML's 28% of body signs is 280,000 steps of flips all in one direction. The script's rate is a fine-tuning rate for a model whose signs are already placed, not a conversion rate.
- End point: in the format at every step.
- Scale: trained on its own between flips.

**E. Scale-only training.**

- Exact at step zero from a released model, moves at the first step, ends in the format once the 16-bit rounding is inside the forward pass. Step size of a 16-bit scale near 0.036 is 3e-5, under 0.1% of the value.
- It trains 13.4 million numbers, 0.8% of the weights.
- The tied matrix: each of its groups has one scale and two jobs. The gradient is the sum over both. The output job sees every token at every position and the lookup job sees only the tokens in the batch, so the output job dominates. Boole stores two scales per group here; PrismML left the whole matrix as converted.

**F. A compensating conversion first.**

- Step zero from the parent is the converted model and not the parent.
- For A after F the latent magnitudes are again free. The signs the conversion changed against the parent are the natural ones to start nearest to zero.

### 2D. The checks in one table

| Method | Step zero from a released model | Step zero from the parent | Do the first updates move the stored model | End point in the format |
|---|---|---|---|---|
| A. Straight-through | Exact; latent magnitudes are a free choice | Plain rounding, not the parent | Scales at once; signs only after `s / rate` steady steps | Yes, if the scale is rounded in the forward pass |
| B. Cage with fixed-norm closing | Exact but stuck until reopened | The parent itself | From the parent, when the cap first cuts | Yes, by geometry |
| C. Mirror, clipped map | Exact | The parent itself | Stalls like A | Only in the limit where it becomes A |
| C. Smooth map sharpened from zero | Exact; latent magnitudes are a free choice; stalls at high sharpness | The parent itself | From the parent, always | No: a sign is swapped in at the end and the gap is unmeasured |
| D. Budget on sign changes | Exact | Needs a conversion | Always | Always |
| E. Scale only | Exact | Needs signs | Always | Yes |

### 2E. Nearest published method, and what is not covered

| Candidate | Nearest | Difference not covered by any proof or test read |
|---|---|---|
| A | BinaryConnect with a scale; BinaryRelax's last phase | The group scale tied to the latents; the warm start from a model already in the format |
| B | ASkewSGD | A cap in place of a band, a group norm held fixed, a trained radius, a start from the parent, a language model. ASkewSGD has no scale and proves nothing as its band narrows |
| C, clipped | The mirror method in ASkewSGD's tables | Nothing in its favour found |
| C, smooth | BinaryLLM | A scale per group of 128, the tied matrix, a teacher (its loss is not stated and no teacher is mentioned), and an end that is exactly in the format |
| D | PV-Tuning for the rule; the double binary factorization fine-tuning script for scalar signs | The script flips signs of two low-rank binary factors with vector scales, not one sign per weight with a group scale; no result for one sign matrix was found |
| A to D with a blend | BinaryRelax's first phase | Blending the forward weight between its rounding and its latent keeps every step moving the model, at the price of leaving the format until the blend ends |

### 2F. What this changes, on paper

- **C splits in two.** Its clipped form is the lazy form of B and stalls like A, and nothing was found in its favour. Its smooth form sharpened from zero is published at language-model scale, starts at the parent, moves at every step and beat a sign from the start. Its measured edge over a sign from the start is small (perplexity 35.0 against 38.1 at 135M). It does not end in the format: its last stage has to be A or the fixed-norm closing of B.
- **From the parent there are two exact starts, B and smooth C.** They differ in what stays exact. B leaves every weight under the cap untouched and is wrong only where it has clipped. Smooth C bends every weight a little from the first stage on.
- **A needs two lines added to its definition:** the scale rounded to 16 bits in the forward pass, and a stated rule for the latent magnitudes at a warm start. The plain rule is the worst one: nothing but scales moves for hundreds or thousands of steps, then a wave of signs.
- **B holds only with the fixed-norm closing and a trained radius.** From the parent it passes both checks and is the only method that starts at the parent. From a released model it cannot start without a reopening schedule.
- **D is the only method that is in the format at every step and cannot stall.** It is method A with a cap on crossings per step, so the two are one trainer with the cap as a setting. The public working form has a cap of about one sign in a million per step and a memory of 50 steps.
- **E is the exact first stage of any run from a released model.**
- **A sixth option appears: the blend of BinaryRelax.** It answers the first check for every method by construction.
- Other published methods to hold: ECO (arXiv 2601.22101), CAGE (arXiv 2510.18784) and a 2026 analysis of why gradients taken at rounded weights lead to low-loss regions (arXiv 2606.09012). What each proves and tests is in section 2G; none goes below 2 bits.

### 2G. What the code of these methods adds

- **BinaryRelax's code is its paper.** The forward weight is `(eta * Q(w) + w) / (1 + eta)` with `Q` the sign times the layer's mean magnitude. `eta` grows 5% an epoch for 80 epochs, and hard rounding is used after that. The latent is kept throughout.
- **ProxQuant reaches the format by a freeze.** Each step pulls a weight's magnitude toward one by the learning rate times a strength that grows with the epoch. At epoch 200 of 300 every weight is set to its sign and stops training, and the last 100 epochs train only what is not binary. The binary path has no scale: batch normalization carries the magnitude. The script logs the share of signs changed since the start.
- **ASkewSGD's own code also ends with a snap.** In its binary notebooks the band is wide enough to be inactive for the first 20 to 50 epochs, then narrows by 1% to 4% an epoch. Where a weight is outside the band and the loss gradient does not bring it back, the gradient is replaced by the push-back term. After the last epoch the sign is still taken. The model is a 2-3-1 network with batch normalization, started at random, with no scale. The ImageNet trainer is the 4-bit path with a scale frozen at epoch 100. This agrees with section 2C: the band alone does not land in the format.
- **PV-Tuning's optimizer has three modes behind one number.** With no latent: step the stored weights as if continuous, re-fit the codes to the result, cap the share of codes changed per step (largest change first, or sampled), then overwrite the weights with what the codes give. With a persistent latent: plain straight-through training. In between: a latent that is pulled toward the stored value by a fixed fraction after every step. The capped re-fit is candidate D as published code. The leaky latent bears on candidate A from a released file: with leak `d` the latent forgets its starting magnitude in about `1/d` steps, so the hidden choice of that magnitude stops mattering. Neither mode has been run on one sign per weight with a scale per group of 128.
- **Three newer optimizer papers stop above the project's rate.** ECO (arXiv 2601.22101) drops the latent and feeds the rounding error into the optimizer's momentum; proved for SGD with momentum under unbiased random rounding; lowest setting 4-bit weights. CAGE (arXiv 2510.18784) subtracts a multiple of the gap between a weight and its rounding after each step, ramped in over the last tenth of training; lowest setting 2 bits. arXiv 2606.09012 proves that straight-through steps return to a low-loss basin when the rounding error is small against the basin's width, and says the guarantee can fail as bits fall; lowest setting 2 bits. None trains a scale and none tests two values.

## 3. Part B: factorization, rotation and binary-training papers

### 3A. What was read

| Source | Read |
|---|---|
| RaBiT, arXiv 2602.05367 | The first version to the start of its kernel listing; the published third version whole, kernel listing included; the authors' blog post. Code `SamsungLabs/RaBiT`, repository read directly: every source file |
| NanoQuant, arXiv 2602.06694 | Whole paper. Code `SamsungLabs/NanoQuant`, repository read directly: every source file, the factorization routine, the importance statistics, the rank rule, the loader, the three kernels and the bundled optimizer included |
| LittleBit-2, arXiv 2603.00042 | Whole paper |
| LittleBit, arXiv 2506.13771 | Whole paper with appendices. Code `SamsungLabs/LittleBit`, repository read directly: every source file |
| All for 1-Bit (AF1), arXiv 2609.06161 | Whole paper in two parts, the last fifth and its appendix included |
| TWLA, arXiv 2606.13054 | Whole paper, its calibration ablation included |
| Structured Kashin transforms, arXiv 2609.11687 | Whole paper |
| SDQ-LLM, arXiv 2510.03275 | Whole paper. Code `Dreamlittlecat/LLM-Quant-Factory`, repository read directly: the README, the run script, the quantizer in both versions, the layer routine in both versions, the scale search, the masking helper |
| Double binary factorization | The fine-tuning script (section 2) and every code cell of the two compression notebooks |
| PBBQ, Electronics 15(4), 819 | Whole page with its result tables |
| "Post-Training Ternarization of Qwen3-4B", arXiv 2609.01962 | Whole report |
| The first Kashin paper, arXiv 2404.09737 | Whole paper |

No figure of any paper was seen.

### 3B. Each method against the project's format

The format: one sign per weight, one 16-bit scale per 128 weights, the tied matrix included, nothing else.

| Method | What is stored | True bits per weight | Fits the format | Smallest model, and what it keeps at about 1 bit | Training | Rotation |
|---|---|---|---|---|---|---|
| RaBiT | Two or three sign matrices, each with a row vector and a column vector of trained scales | 2 or 3 plus the vectors | No. One path would fit after swapping its two vectors for group scales, but the code refuses one path in four places | Qwen3-1.7B at 2 bits: 60.38 of 64.21 on easy tasks, 94%, perplexity 10.19 against 7.12; Gemma3-1B 92%. No 1-bit result | 200M tokens, six passes, a teacher's outputs plus every layer's hidden states | None |
| NanoQuant | Two low-rank sign factors and two or three scale vectors | 1.00, 0.80, 0.55 by its count, which covers the block matrices only: its Qwen3-1.7B file is 0.74 GB, most of it the 16-bit embedding | No | Qwen3-0.6B. Qwen3-1.7B at 1.00: perplexity 19.21 against 9.39. Qwen3-8B: 48.9 of 71.2 on six easy tasks, 69% | None beyond 0.26M tokens of calibration | None |
| LittleBit-2 | Two paths of low-rank sign factors with three scale vectors each | 1.0 down to 0.1 | No | Llama2-7B at 1.0: perplexity 8.27 against OneBit's 8.36 | Straight-through training, settings "identical" to LittleBit and not given | Yes, between the two factors, folded into them at no cost |
| LittleBit | The same two paths, without the fitted rotation | 1.0 down to 0.1; block matrices only, embedding and output matrix in 16 bits | No | Llama2-7B: perplexity 9.08 at 1.0, 12.00 at 0.3, 15.92 at 0.1. OPT-1.3B is the smallest: 20.33 at 1.0, behind OneBit's 20.27 and BinaryMoS's 18.09 | Teacher's outputs plus ten times the hidden-state error; the first of 1,024 C4 training shards with WikiText-2; five passes | None |
| AF1 | Two low-rank sign factors, three scale vectors, a rank per layer set by a sensitivity search | 1.00 on average over layers | No | Gemma-3-4B-it: 74%. Qwen3-8B 79%, 14B 82%, 32B 89% of a seven-task average; Llama-3-8B 63%, 70B 78%. Qwen3-14B-Instruct keeps 56% of MMLU-Pro, 56% of HumanEval, 68% of GSM8K | None beyond 262 thousand tokens for scales | None; a per-channel rescaling only |
| TWLA | Three-level codes, a scale and an offset per row | 1.58 plus the row numbers | No: three levels, an offset the format has no place for, and a transform at run time | Qwen3-8B weight-only: 90%; 14B 94.5%; 32B 96%. Nothing under 7B | None | A learned Kronecker rotation. Weights are rotated offline and the inverse is applied to activations at run time: about 524 thousand multiply-adds per 4,096-wide vector by its own count |
| TWLA applied to Qwen3-4B (arXiv 2609.01962) | Three-level block matrices at 1.641 bits by its count; embedding and an untied output matrix in 16 bits; 40.1M rotation numbers | 3.96 GiB for a 4B model | No | Mean of ten benchmarks 54.7 against 64.5, 85%; MMLU 50.96 against 68.50 | None; 64 WikiText-2 samples | Applied to activations at run time; slower than 16 bits, 21.28 against 27.41 tokens a second |
| Kashin transforms | Two 2-bit codes per weight in two bases | 4 | No | Only 4-bit results; no 1-bit result | None | A fast transform that is not folded: applied at load or on activations |
| SDQ-LLM | Three-level or two-level codes on a row stretched to twice or more its length | 3.16 at the tested setting; its tables call this 1.58. In two-level mode the rate is the stretch factor: 2 bits at a factor of 2 | No. The code is a simulation that writes ordinary real weights back; a stored file would need a decoder (a resampling step and a Hadamard transform) at load or at run time | Llama3.2-1B collapses (perplexity 298 against 9.75) | None | A Hadamard transform before rounding, undone after it |
| PBBQ | Whatever its host method stores | The host's | It changes the order of error compensation and undoes its column reordering before storage, so it is a search order and not a format | Llama2-7B perplexity: BiLLM 32.48 to 25.51, ARB-LLM 16.44 to 12.82; Llama3-8B 27.42 to 25.96. Its MMLU on Llama2-7B stays near chance: 23.7 to 25.3 against 41.8. Nothing under 7B | None | None |
| BinaryLLM (section 2) | One sign matrix with scale vectors; embedding and output matrix in full precision | 1.01 on block matrices | Closest of all: the scale vectors would become group scales | 135M: 87% of easy-task average. 1B 88%, 3B 88%, 7B 85% | Next-token training on RedPajama; token count given only for a 70M test (50B) | None |

Readings:

- **Nothing published stores what the project stores,** and no low-rank method can be repacked into one sign per weight.
- **At 1 bit a single sign matrix is not behind the factorized methods.** Llama2-7B perplexity, trained methods, as the papers' tables give them: 7.88 for BinaryMoS (one sign matrix with mixed scale vectors), 8.27 LittleBit-2, 8.36 OneBit (one sign matrix; the NanoQuant paper lists it at 9.73), 9.08 LittleBit, 9.25 double binary factorization, 8.85 to 10.34 NanoQuant without training. Factorization buys rates under 1 bit. It does not buy quality at 1 bit.
- **A free rotation needs somewhere to sit.** LittleBit-2's rotation sits between two factors and cancels. A single sign matrix has no inside. The only transforms that cancel for it are those the network already allows: reordering channels, rescaling a channel where a normalization follows, and maps inside an attention head's query and key pair that commute with the position rotation. This is the content of idea H11 and no paper read here adds to it.
- **Rotations are worth a lot where they can be used.** SDQ-LLM: 2,435 perplexity without the Hadamard step, 20 with it. LittleBit-2: 16.30 to 12.63 from a random rotation alone, 11.53 with a fitted one. BWLA in batch 8 showed the same. The gain is from making weights two-humped before the sign is taken. TWLA's own ablation at three levels, weights only, on Qwen3-14B: perplexity 23.64 with its quantizer alone, 102.12 with its rotation alone, 17.26 with both, and 57.6, 25.0 and 69.2 on MMLU. Its rotation is not free: the inverse runs on activations.
- **Where the bits go matters as much as how they are fitted.** AF1 at an average of 1 bit on Qwen3-8B: perplexity 28.92 with the same rank everywhere, 16.26 with rank given to layers by sensitivity. The project's format gives every weight the same rate, so this lever is closed to it. It is evidence for idea I20 only in its other form, effort per layer.
- **Training-free 1 bit stops near 70% to 90% on easy tasks and near 56% to 68% on hard ones, and rises with size.** AF1's 79%, 82%, 89% at 8B, 14B, 32B is the clearest size series read. Qwen3-1.7B is below every point in it.
- **NanoQuant's largest single gain is not its factorization.** In its ablation on Qwen3-8B the factorization alone gives perplexity 206. Letting the block's not-yet-converted full-precision matrices retrain to absorb the error of the converted ones gives 15.07. Tuning the factors after that gives 13.58, and the scale-only teacher step 12.47. Its code does this matrix by matrix: tune the rest, convert one, tune that one's signs and scales, move on. The step is older than NanoQuant: both double binary factorization notebooks retrain a block's remaining full-precision weights before they convert its query and key matrices. ProxQuant's freeze in section 2G is the same move for a small network.
- **The backward rule made no measurable difference where it was ablated.** LittleBit replaces the straight-through rule by the derivative of a steep tanh, a spike that is felt only by latents within about 0.03 of zero. Its own ablation on OPT-1.3B: 60.011 against 60.401 at 0.1 bits and under 0.1 perplexity apart at every other rate. This is evidence for row C111 and against expecting a gain from the backward rule alone.
- **A second path is not always a gain.** LittleBit's residual path helps at 1.0, 0.55 and 0.3 bits (20.33 against 21.69 at 1.0) and hurts at 0.1 (60.01 against 48.51).
- **Signs barely move after a good start.** NanoQuant's refinement flips 0.5% to 7% of signs per matrix and the flips sit on the smallest latents. LittleBit-2 reports 3.8 times fewer flips during training with its rotation than without.

### 3C. RaBiT and NanoQuant against Boole's files

Boole's files (batch 8): one sign per weight; a scale tensor per matrix of shape rows by columns over 128, labelled a learned per-group scale of any sign; the embedding and output matrix share one sign tensor and have a scale tensor each; normalization gains in 16 bits.

| Trait | RaBiT code | NanoQuant code | Boole's files |
|---|---|---|---|
| Sign matrices per weight matrix | 2 or 3; 1 is refused | 2 low-rank factors | 1, full size |
| Scales | A row vector and a column vector per path, trained as free parameters | Two or three vectors, trained as free parameters | One per 128 weights along a row, of either sign |
| Embedding and output matrix | Left in full precision and frozen | Not converted: only the decoder blocks are processed | Both binary, one shared sign tensor |
| Source of the signs | Sign of one trained full-precision matrix, recomputed every step | Sign of trained low-rank latents | Unknown |
| Loss | Teacher's outputs over the whole vocabulary plus hidden states of every layer | Block outputs, then teacher's outputs for scales only | Unknown |
| Data in the code | C4 with WikiText-2; also LMSYS-Chat-1M with the loss taken on assistant turns only, and a mix of both, none of which the paper reports | 128 WikiText-2 sequences | Unknown |

- Boole's storage is neither method's. NanoQuant is ruled out by the files alone: a low-rank product of signs is not one free sign per weight.
- One fact in Boole's files does carry information. Its card says a stored scale can have either sign and is used through an absolute value with a floor. A mean magnitude is never negative and needs neither. That points to scales trained as free numbers, as in both of these code bases, and away from the mean-magnitude rule that both public Qwen trainers read in batch 8 use. It is evidence and not proof: a negative scale is also only another way to write the same group.
- The published version of the RaBiT paper has a Qwen3 table: 1.7B, 4B and 8B at 2 bits keep 94%, 95% and 94% of an easy-task average; at 1.7B that is ahead of the two baselines it lists. So the group around Boole's author trained Boole's parent with this trainer at 2 bits. The paper gives no settings for Qwen3; its blog post says only that getting Llama, Gemma and Qwen to converge needed a careful start and tuning of activation ranges to prevent collapse. For scale: its Gemma3-1B run took 8 hours on four H100 cards, 200M tokens seen six times. At 8B it is behind QTIP on the task average, 70.25 against 70.93.
- RaBiT's forward function accepts one path. The refusals are in the wrapper, the argument parser, the initializer and the evaluation script. With one path it is: sign of a trained matrix, times trained scales, the gradient passed straight through, a teacher's outputs and hidden states as the loss. That is method A with the scale made a parameter.
- RaBiT's code has a chat-data path with the loss on assistant turns only that its paper never uses, and its loader keeps the file name of the older LittleBit configuration. The code is a working tree of that group, wider than the paper.
- What none of this settles: Boole's start, data, token count, loss, and how it trains a tied matrix that both code bases leave alone.
- RaBiT's own ablation says where its gain comes from: on Llama2-7B, coupling the paths takes perplexity from 6.55 to 5.84, and the start procedure adds 0.06 after that. Coupling does not exist with one path. So the paper gives no reason to expect its trainer to be better than plain straight-through training at 1 bit.

### 3D. Code against paper

| Item | RaBiT paper | RaBiT code default |
|---|---|---|
| Weight on the hidden-state term | 100 for Llama, 0 for Gemma3 | 10 |
| Start iterations | 20 | 150 in the argument parser, 20 in the module |
| Importance powers | 0.75 to 0.95 and 0.45 to 0.70 by model | 0.85 and 0.35 |
| Optimizer | Muon | AdamW unless a flag is set |

| Item | NanoQuant paper | NanoQuant code default |
|---|---|---|
| Scale-only teacher step, learning rate | 1e-6 | 1e-5 |
| Shrinkage of the statistics | 0.2 for Llama and Qwen, 0.6 for Gemma | 0.4 |

NanoQuant's code defaults not compared with its paper: 128 WikiText-2 sequences of 2,048 tokens; eight passes at 1e-4 for the unconverted weights; 400 outer steps of factorization; eight passes at 1e-5 for the factors; eight passes at 1e-5 for the whole-model step. Its factorization routine divides by a vector norm with no floor and never uses its own `eps` argument, so a residual of all zeros gives not-a-number; its port of the double binary routine in the same repository has the guard. Its optimizer is a bundled copy of a public AdamW with compensated summation for 16-bit parameters and has nothing specific to signs. Its kernels include one for a single sign matrix with a row vector and a column vector of scales; none takes a scale per group of 128.

## 4. Part C: what two-value weights can store

### 4A. What was read

| Source | Read |
|---|---|
| Allen-Zhu and Li, arXiv 2404.05405 | Main text read in batch 6 and again here; the appendix read here. The values in its rounding figures came back unreadable |
| ParetoQ, arXiv 2502.02631 | Read whole with its code in batch 4. Its tables were read again here for the 1-bit rows |
| Spectra, arXiv 2407.12327 | Whole paper in two parts; the binary rows of its appendix tables in the second (opened while checking the second review). No figure values |
| "On the Expressive Power of Weight Quantization in Large Language Models", arXiv 2606.22249 | Whole paper. Found by search during this batch |
| "Strong freezing in binary perceptron models", arXiv 2610.06275 | Whole paper. Found by search during this batch |
| BitNet b1.58 2B4T, arXiv 2504.12285 | Whole report |
| "Meta-memorization and memorization scaling laws in transformers", arXiv 2611.01564 | Whole paper |

The capacity table of batch 6 (section 4D of that document) already holds the measured figures. This part adds to it and does not repeat it.

### 4B. New facts

- **Two levels against three, trained from scratch (Spectra).** Binary models were trained at 99M, 560M and 1.1B weights on the same data as the three-level ones, with one scale per matrix and the embedding in 16 bits. Six-task averages for 16 bits, three levels and two: 44.3, 43.5, 39.8 at 99M; 50.5, 48.4, 44.5 at 560M; 54.9, 51.6, 47.1 at 1.1B. Two levels keep 90%, 88% and 86% of the 16-bit twin, falling with size, and a steady 91% to 92% of three levels. On MMLU the binary models score 23.1, 22.9 and 23.0, at chance at every size, while 16 bits rises from 25.3 to 30.0. The authors read their validation losses as a gap that closes above 10B; the task tables do not show it closing.
- **Random strings shown unevenly (arXiv 2611.01564).** With 100-bit random strings presented by a Zipf law, 16-bit transformers hold 0.5 bits per weight at one layer and 1 at twelve. The MLP holds the associations. After the data is swapped for fresh strings, the model learns the new ones faster than it learned the first. No low-bit weights were tested. Its theory is a toy associative memory and derives no capacity per weight.
- **Two levels from a pretrained model, trained to saturation (ParetoQ).** Llama-3 8B, embedding and output matrix in full precision, five easy tasks: 64.1 at 1 bit, 69.0 at three levels, 71.2 at 2 bits, 74.6 in 16 bits. That is 86%, 92.5% and 95%. Saturation took about 30B tokens at 2 bits and below and 10B at 3 and 4 bits. Weights moved about 40% from their start at 2 bits and below and 10% to 20% above. Its own appendix finds embeddings at the weights' precision or at 4 bits on the best size-accuracy line.
- **A theorem that pure 1-bit networks are not universal (arXiv 2606.22249).** With weights of 2 bits or more, three levels included, attention with an MLP can approximate any continuous function. With weights in two values there is a target function no such network gets within a fixed distance of. The paper concludes that three levels is the limit. Its class has no full-precision scale per group and no full-precision normalization gain, both of which the project's format has, so as read it does not bound the format. Its experiments show trends only.
- **Solutions of the two-value perceptron are isolated (arXiv 2610.06275).** For one neuron with sign weights and random patterns, at every load, all but a vanishing share of solutions have no other solution within a fixed fraction of sign flips. Methods that do find solutions find rare ones that sit in a connected cluster. The result is for one layer and random data.
- **From the capacity paper's appendix.** Rounding used 1,000 biographies for calibration. The 4-bit loss is largest where each fact carries the most bits. Tying the embedding to the output matrix raises capacity in models of 10M weights and under. Its 16-bit models tie them; its LLaMA and Mistral models do not.
- **Three levels from scratch at 2B weights and 4 trillion tokens (BitNet b1.58 2B4T).** Weights in three levels by mean magnitude, activations in 8 bits, then supervised tuning and two passes of preference tuning. Average of sixteen benchmarks 54.19 against 55.23 for Qwen2.5-1.5B in 16 bits. The average hides a split: ahead on GSM8K (58.38 against 56.79) and instruction following (53.48 against 50.12), behind on MMLU (53.17 against 60.25), HumanEval+ (38.40 against 50.60) and MATH-500 (43.40 against 53.00). On a three-benchmark subset the same Qwen at 4 bits by GPTQ or AWQ scores 52.15 and 51.17 against 55.72 in 16 bits and 55.01 for BitNet.

### 4C. One pattern across every measured format

From the batch 6 table, stored knowledge as a share of raw stored bits:

| Format | Stored bits per weight | Raw bits per weight | Share |
|---|---|---|---|
| 16-bit | 1.72 to 2 | 16 | 11% to 12.5% |
| 8-bit, rounded or trained | 1.59 to 2 | 8 | 20% to 25% |
| 4-bit, trained | 1.0 | 4 | 25% |
| 4-bit, rounded | 0.7 | 4 | 17.5% |
| 3-bit, trained | 0.55 | 3 | 18% |
| Three levels, best schedule | 0.41 | 1.58 | 26% |
| One neuron with sign weights, theory | 0.83 | 1 | 83% |

- No trained transformer in any source stores more than about a quarter of its raw bits. The one figure above that is a single neuron on random patterns.
- At a quarter, the project's format stores 0.28 bits per weight: 0.48 billion bits for Qwen3-1.7B. At the perceptron's share it stores 0.93 per weight.
- Two levels are still unmeasured. This table is the prediction to test: 0.2 to 0.3 bits per weight at full load in the batch 6 harness.

### 4D. Are 90% and 99% consistent with what is known

By counting:

- The format holds 1.94 billion raw bits for 1.72 billion weights. A 16-bit parent at the measured ceiling of 2 bits per weight would hold 3.4 billion. So 99% of a fully loaded parent cannot fit, by counting alone. A parent at the 100-exposure figure of 1 bit per weight would need the format to store at 89% of its raw bits, above the perceptron figure.
- At a quarter of raw bits, 99% fits only if the parent holds under 0.28 bits per weight of what the ruler tests, a seventh of its ceiling. Where Qwen3-1.7B sits is unknown (plan item U2).

By the two released models, crudely (PrismML's teacher scores, another harness's student scores, a straight line through chance):

- Boole keeps 61% of the parent's MMLU-Redux score above chance; PrismML's model keeps 44%. If Boole stores a quarter of its raw bits, the parent's load on that kind of knowledge is near 0.46 bits per weight, and 90% and 99% of it need 0.41 and 0.46: 37% and 40% of raw bits. Both are above every trained transformer measured and below the perceptron figure.

By where the points are:

- On the outside harness Boole is at 85.9% and needs 4.1 points of retention for 90%: 24 summed points. That harness did not publish the parent's score per benchmark, so the gaps are taken against PrismML's published parent scores, whose total is within 1% of the outside harness's. Boole's largest gaps are MATH-500 (about 24 points), MMLU-Redux (16), GSM8K (8), MuSR (6) and GPQA (6). Instruction following, code and tool calling are at 90% to 100%.
- So 90% does not have to come from stored facts. Mathematics alone holds enough points, and batch 8 found that the text a student is trained on moves exactly these scores (chat text moved GSM8K, multiple-choice text moved MMLU; the independent three-level run fed half mathematics).
- 99% leaves 6 summed points of loss across ten benchmarks. It needs the knowledge benchmarks too.

Against:

- On the one harness that scored all three models, the best three-level model of this size is at 87.7%. Reaching 90% at two levels means passing it with 71% of its bits.
- Trained to saturation, 1 bit kept 86% of easy-task accuracy at 8B with the embedding in full precision. Easy tasks have high chance floors, which flatters that figure.
- From scratch at 1.1B, two levels keep 86% of the 16-bit twin's easy-task average and sit at chance on MMLU.

Verdict on paper: 90% is consistent with everything read and shown by nothing. 99% is not ruled out by a bound, and needs two-level weights to store well above a quarter of their raw bits or a parent far under its ceiling, neither of which is measured.

### 4E. The planned capacity measurement (C124), criticized

The design (batch 6, section 4D, with the second reviewer's additions) trains small models on synthetic biographies in 16 bits, three levels and the project's format, from scratch and distilled, tied and untied.

1. **It has no conversion arm.** The project converts a trained parent. The design trains from scratch or distills into a fresh student. The one source that fine-tuned a trained model into three levels saw 90% of its facts destroyed. An arm that starts from the trained 16-bit model and moves into the format is the project's own operation and is missing.
2. **Two loads are too few.** The question is where retention falls off as the data asks more of each weight. That needs a curve: requested load at four or more points from well under to well over 0.28 bits per weight, so the result can be read at the parent's load once that is known.
3. **It will measure the trainer as much as the format.** At three levels the schedule alone moved the figure from 0.155 to 0.412. The freezing result says sign solutions that small moves can reach are rare ones. A single trainer gives a floor on what the format holds. Two different trainers (straight-through, and a sign budget or a progressive start) show how wide the trainer's share is.
4. **The group size does not scale down.** At 2.5M to 10M weights the hidden width is a few hundred, so a row holds one to four groups of 128. Qwen3-1.7B has 16 per row in its attention matrices. Either the width is kept at 512 or more, or the group is shrunk in proportion and the result reported as bits per stored bit.
5. **The tied arm does not test the project's tied matrix.** The synthetic data uses about 3,300 tokens. The tied matrix is then a sliver of the model. In Qwen3-1.7B it is 18% of the weights. The arm answers a different question unless the vocabulary is made large. The capacity paper also found that tying helps models of 10M weights and under, so at the planned sizes the arm would show a small-model effect.
6. **Two sizes cannot show a trend.** Spectra's gap between two and three levels shrinks with size. A third size is the minimum for a slope.
7. **Report per stored bit as well as per weight,** with the scales counted, since the format's 1.125 includes them and the 16-bit parts (gains, scales) hold information too.
8. **It speaks to facts, not procedures.** By section 4D the points needed for 90% sit mostly in mathematics. The measurement can move the odds of 99% and says little about 90%.
9. **State the prediction first:** 0.2 to 0.3 bits per weight at full load, 12% to 17% of the 16-bit model's figure in the same harness; over 0.45 would be a result that changes the 99% odds.

## 5. Probabilities

Judgment, not measurement.

| Claim | Before this batch | After | Why |
|---|---|---|---|
| Some training puts a 1-bit Qwen3-1.7B in the strict format at 90% retention | 40% | 38% | For: the missing points sit in mathematics, where data moves scores; two starts from the parent now pass both paper checks. Against: the best three-level model of this size is at 87.7% on the harness that scored it beside Boole; saturated 1-bit training at 8B kept 86% of easy tasks |
| The same at 99% | 5% | 4% | The quarter-of-raw-bits pattern is new and points down; no bound rules it out |
| Sign-and-scale training from PrismML's released model gains five points on the project's ruler | 76% | 78% | A sign-budget trainer exists in code; the freezing result favours starting from a trained sign pattern over a rounded one |
| A conversion from public recipes reaches 70.2% | 48% | 50% | Two published starts from the parent itself; NanoQuant's retraining of unconverted matrices is a stronger compensating start than any in the plan |
| Boole was trained by a one-matrix form of its author's group's published trainers | 50% | 50% | Its scales look like free parameters, as theirs are, and the published RaBiT paper trains the same parent at 2 bits; its group scales, binary tied matrix and single path match neither code base |
| Boole's method can be learned from public text | 3% | 3% | Nothing new |

## 6. What this serves in the plan

| Item | What this batch adds |
|---|---|
| P3, no recipe of ours leads | Two checks passed on paper by B with a fixed-norm closing and a trained radius, and by smooth C, both from the parent; which methods end in the format by construction (B with fixed norm, D, E) and which need a last stage (smooth C, the blend); NanoQuant's sequential compensation |
| CH3, proof for 99% | The counting limits of section 4D. The evidence rule itself is unchanged |
| U2, how far two values can go | The share-of-raw-bits table; the counting limits; where the missing points are; the criticism of C124 |
| U4, how PrismML and Boole trained | Boole's scales look like free parameters; RaBiT's one-path form; code and paper differences |
| H8, H11 | Sequential compensation as a form of migrate-then-convert; no rotation is free for a single sign matrix beyond the network's own symmetries |
| I13, I24 | A published scalar-sign budget trainer; the fixed-norm closing needs a trained radius |
| C125, C132, C136 | Closed. What cannot be read with these tools is in section 9 |

## 7. Needed from the project owner

Nothing.

## 8. Sources

Read in this batch, in the order used: arXiv 1801.06313; 1810.00861; 2211.03741; 2405.14852; 2508.06974; `usamec/double_binary`; arXiv 2602.05367 with `SamsungLabs/RaBiT`; 2602.06694 with `SamsungLabs/NanoQuant`; 2603.00042; 2609.06161; 2606.13054; 2609.11687; 2510.03275; 2404.05405; 2502.02631; 2407.12327; 2606.22249; 2610.06275. Opened while checking the second review: the PBBQ paper (Electronics 15(4), 819) and arXiv 2611.01564. Also read: the rest of PBBQ, arXiv 2611.01564, TWLA, NanoQuant and LittleBit; arXiv 2609.01962; arXiv 2404.09737; arXiv 2504.12285; ECO (arXiv 2601.22101), CAGE (arXiv 2510.18784) and arXiv 2606.09012; the published version of RaBiT and its blog post; the code of BinaryRelax, ProxQuant, ASkewSGD, PV-Tuning, LittleBit, NanoQuant, RaBiT and SDQ-LLM; both double binary factorization notebooks. New to the project among all of these: 1801.06313 and 1810.00861 in full, the two code bases, 2603.00042, 2407.12327, 2606.22249, 2610.06275, 2611.01564, PBBQ.

## 9. Not read

- No figure of any paper. Every paper was read through a tool that returns an account of the page, so quoted numbers are as that tool reported them. The values in the figures of Spectra and of the appendix of Allen-Zhu and Li cannot be read this way.
- No public code was found for the quantized-endpoint paper (arXiv 2609.21834).
- In the SDQ-LLM repository: its table of Hadamard matrices and its runners for other published methods.
