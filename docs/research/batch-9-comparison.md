# Batch 9: the two reviews compared

The first reviewer's findings are `batch-9-findings.md`. The second reviewer's document is filed as `batch-9-second-reviewer.md`. Each worked without sight of the other. What was taken from the second reviewer was checked at its source or by arithmetic first, and the check is named.

## 1. Result

- The two reviews reach the same paper verdicts on the training methods by different routes: straight-through training from a released file has a latent margin that is a free choice; a clipping cage does not close by itself and closes exactly only with a norm held fixed; from the parent a pure teacher loss has a zero first gradient; a smooth map never reaches the format at a finite point; a sign budget and scale-only training are in the format at every step.
- The second reviewer adds exact algebra the first did not have: a straight-through variant with the scale as its own parameter, a closed-form price for a sign flip with the group scale re-fitted, the true projection onto the closing cage, the exact condition under which a rotation of the residual stream survives a tied matrix, a weighted rule for re-tying two scales, and an information bound that says what 1.125 bits per weight can and cannot hold.
- The first reviewer adds what the second did not open: the code of RaBiT and NanoQuant read to the layer classes, the two papers that start exactly at the parent and move from the first step, the isolation of sign solutions, the quarter-of-raw-bits pattern across measured formats, and where Boole's missing points are.
- The second reviewer caught three faults in the first review. The RaBiT paper has a published version with a Qwen3 table, which the first reviewer missed by reading the first version: Qwen3-1.7B at 2 bits keeps 94% of an easy-task average. Two sources the first reviewer reported as not found were at addresses in the project's own brief. And the first reviewer repeated the Spectra authors' reading of a closing gap without the task tables, which show two levels falling further behind 16 bits as size grows.
- The second reviewer's return does not meet the reading standard, by its own statement: no source read in full, no figures, most code not opened.
- Odds: 90% retention in the strict format, 38% (first reviewer) and 45% (second). 99%: 4% and 8%.

## 2. Depth of the second reviewer's read

| Item | What it did |
|---|---|
| Sources | Thirty named, every one marked read in part. No figure of any paper seen |
| Code | Single files of ProxQuant, the PV-Tuning repository, LittleBit, NanoQuant and RaBiT fetched raw. RaBiT's layer class, backward function and initializer not reached. The factorization notebooks not reached |
| Its own mathematics | Complete, with two numerical checks on synthetic vectors |
| Papers the first reviewer did not read | PBBQ, the 2026 memorization paper, the first Kashin paper, the three-level Qwen3-4B report, the binary perceptron note, LittleBit's own paper |
| Papers the first reviewer read that it did not | BinaryLLM, the expressive-power paper, the strong-freezing paper; the capacity paper's appendix; AF1 to its end |
| Odds | Stated before and after; left unchanged because its reading condition was unmet |

## 3. Where the two agree

| Point | First reviewer | Second reviewer |
|---|---|---|
| Straight-through training from a released file starts exactly, and its latent magnitudes are a free choice | Section 2C, method A | Section 1B |
| A sign flips only after a cumulative push of the size of the scale; until then only the scale moves | 360 steps at a rate of 1e-4 for a scale of 0.036 | 2,000 steps for a scale of 0.02 and a step of 1e-5 |
| The scale must be rounded to 16 bits inside the forward pass, with a full-precision master kept | Section 2F | Section 1B |
| From the parent with a teacher loss alone the first gradient is zero; the cap or the map makes the first move | Section 2C, method B | Section 1A |
| A cage closes exactly only with the group norm held: a sphere and the cube inside it meet at corners | Section 2C | Section 1C, with the proof |
| A fixed norm pins the scale at the root-mean-square, above the mean magnitude, so the radius must be trained | Section 2C | Section 1C: the bias is `n (a_rms - a_mean)^2` |
| From a released file the cage is already closed and no sign can move without reopening | Section 2C | Section 1C |
| A smooth map reaches the format only in the limit; a clipped map reaches it and stalls past the cap | Section 2C, method C | Section 1D |
| A sign budget is in the format at every step and needs no latent crossing | Section 2C, method D | Section 1E |
| Scale-only training is exact from a released file and is the first control | Section 2F | Section 1F |
| A compensating start applied to a file already in the format does nothing | Section 2C, method F | Section 1G |
| No proof in any of the five papers covers a learned group scale, a tied matrix or a language model | Section 2E | Section 1I |
| No factorized, rotated or oversampled method stores the project's format | Section 3B | Sections 2B to 2G |
| RaBiT with one path is a row scale times signs times a column scale, not a scale per 128 | Section 3C | Section 2H |
| Boole is neither RaBiT's nor NanoQuant's storage, and author overlap proves nothing about its trainer | Section 3C | Section 2H |
| Counting rules out 99% of a fully loaded parent and does not rule out 99% on the benchmarks | Section 4D | Sections 3F, 3G |
| The capacity measurement as designed measures a trainer's reach, not the format's ceiling; it needs a load sweep, more than one trainer, results per stored bit, and a real tied matrix | Section 4E | Section 3H |

## 4. What the second reviewer found that the first did not

Each was checked before it was taken.

### 4A. A straight-through variant with its own scale

- The rule: keep a sign latent `z` and a separate trained scale `a`; the forward weight is `a16 * sign(z)`. From a released file set `z` to the stored signs times any margin and `a` to the stored scale.
- Why it matters: the first reviewer found that the margin of every latent is a hidden choice tied to the weight's size. With the scale separate, the margin is a setting of the optimizer and nothing else, and the scale gets an exact gradient, the sum of signed gradients of its group.
- Check: by algebra. It is also what RaBiT's forward function does with one path (first reviewer's code read) and what Boole's card suggests.
- It also names a choice the first reviewer had not separated: passing the gradient through the whole rounding as the identity is a different rule from differentiating the mean magnitude and passing only the sign through. The second has an extra shared term, `s s^T / n`. A specification has to say which.

### 4B. The price of a flip with the scale re-fitted

- For a group with signs `s`, target `w` and a positive-definite `H`, with `r = s^T H w` and `d = s^T H s`, the best scale is `r / d` and the cost is `0.5 w^T H w - 0.5 r^2 / d`. Flipping sign `i` gives `r' = r - 2 s_i (H w)_i` and `d' = d - 4 s_i (H s)_i + 4 H_ii`, and the change in cost is `0.5 (r^2 / d - r'^2 / d')`.
- Check: recomputed for all 128 flips of a random group; largest difference 5e-15.
- It is exact for the stated quadratic and a ranking rule for the real loss. It is the closed form of idea I13.
- Also from it: a flip is favourable to first order only when the gradient points against the sign, and helps for certain only when `s_i g_i` exceeds the scale times the curvature. Flips that each help can hurt together through cross terms.

### 4C. The projection onto the closing cage, and a certificate

- The nearest point with norm `r` and every magnitude at most `c` keeps each sign and has magnitudes `min(c, t |y_i|)`, with `t` found by bisection. Clipping and then rescaling is not that projection.
- A cage written as norm `sqrt(n) a` and magnitudes at most `rho a`, with `rho` falling to 1 and `a` trained, is the same thing the first reviewer reached as "a trained radius", stated completely.
- Distance to the format while closing is at most `n c^2 - r^2`. That is a number to log.
- Check: by algebra.

### 4D. When a rotation survives a tied matrix

- Rotating the residual stream by `R` is absorbed by every untied matrix. At the output it leaves `R D' R^T` where the final normalization's gain `D` was, and the tied matrix cannot absorb the difference. With distinct gains only signed permutations pass. With equal gains every rotation passes.
- In the feed-forward block only a shared reordering of channels and a rescaling of the up branch pass. In attention, maps on a query and key pair must commute with the position rotation.
- After conversion a reordering is free only if it keeps each group of 128 together.
- Check: by algebra. The first reviewer's list of free transforms was looser on the query and key pair and silent on the tied matrix; its findings now carry the tighter wording.

### 4E. What 1.125 bits per weight can hold

- Distinct values of one group: 31,743 positive finite 16-bit scales times `2^128` sign patterns, plus zero. That is 1.1168 bits per weight, not 1.125.
- For `K` independent fair bits recalled with error rate `e`, the format needs at least `K (1 - h2(e))` bits. With a parent holding 2 bits per weight: 90% bit accuracy needs 1.062 bits per weight and fits; 99% needs 1.838 and does not; exact recall fits for 56% of the bits.
- The highest parent load at which 99% bit accuracy still fits is 1.22 bits per weight; for 90% it is 2.12.
- Check: recomputed. It replaces the first reviewer's looser counting sentence and says the same thing more exactly: counting forbids 99% of a fully loaded parent, permits 90%, and says nothing about a benchmark average.

### 4F. A weighted rule for re-tying Boole

- One scale for two roles with sensitivities `h_in` and `h_out`: `a = (h_in u + h_out v) / (h_in + h_out)`, at a cost of `h_in h_out / (h_in + h_out) * (u - v)^2`.
- Check: recomputed. With equal weights it is the `64 (a - c)^2` of the batch 8 comparison.
- Its warning that two scales of opposite sign would oppose each other does not arise for Boole: the card applies an absolute value.

### 4G. Readings

| Finding | Check | Kept |
|---|---|---|
| RaBiT's published paper has a Qwen3 table: 1.7B at 2 bits, 60.38 of 64.21 on easy tasks, perplexity 10.19 against 7.12 | Third version of the paper fetched: confirmed, with 4B and 8B rows and two baselines (11.89 and 11.19 perplexity at 1.7B). No settings for Qwen3 are given | Yes |
| Spectra's task tables: two levels from scratch keep 90%, 88%, 86% of the 16-bit twin at 99M, 560M, 1.1B | Second half of the paper fetched: confirmed. Also there: binary MMLU at chance at all three sizes | Yes |
| PBBQ reorders columns for the compensation pass and undoes it before storage; BiLLM 32.48 to 25.51, ARB-LLM 16.44 to 12.82 | Publisher page fetched to its midpoint: confirmed | Yes, as a search order |
| The 2026 memorization paper: 0.5 to 1 bits per weight on random strings shown by a Zipf law; relearning after a data swap is faster | Fetched to 72%: confirmed. 16-bit weights only | Yes |
| An old LittleBit unpacker shifts left where it must shift right, so every bit but the lowest reads as zero | Repository read directly at that commit: confirmed. RaBiT's unpacker shifts right | Yes, as the reason for a packed round-trip test |
| Double binary factorization on Llama2-7B: perplexity 9.57, and 8.76 with sign tuning; 52.01 and 53.10 on tasks | Agrees with the batch 6 record | Already held |
| ParetoQ at 1.5B: three levels 60.5 against 62.7 | Agrees with the batch 4 record, where 1 bit is 55.9 | Already held |
| A possible divide-by-zero in NanoQuant's start routine on an all-zero residual | Not checked; that file was not read by either reviewer | Noted only |

## 5. What the first reviewer found that the second did not

- **RaBiT's code to the layer.** One path is refused in three places while the forward function accepts it; scales are a row and a column vector trained as free parameters; the embedding and output matrix are untouched and frozen; a chat-data path with the loss on assistant turns exists and is unreported. The second reviewer did not reach these files.
- **RaBiT's own ablation** credits its gain to coupling two paths, which one path lacks.
- **NanoQuant's block procedure** in code and its ablation: retraining the unconverted matrices is worth more than the factorization.
- **Two published starts at the parent itself:** the fixed-norm cage, and the smooth map sharpened from zero (BinaryLLM). The second reviewer treats the smooth map as unspecified; a published one exists with results from 135M to 7B.
- **The working sign-budget script** and its rates: one sign in a million per step, evidence kept for 50 steps; and its measured effect, perplexity 9.57 to 8.76.
- **Isolated sign solutions** (one neuron, random patterns): the reason to start from a trained sign pattern.
- **A theorem that pure two-value networks are not universal,** and why it does not reach a format with full-precision group scales.
- **The share of raw bits stored as knowledge** across every measured format, at most about a quarter, and the 0.28 bits per weight it predicts for this format.
- **Where Boole's missing points are:** mostly mathematics, so 90% does not have to come from stored facts.
- **For the capacity measurement:** a conversion arm, the vocabulary size needed for the tied arm to mean anything, and a prediction stated in advance.
- **Size series for training-free 1 bit:** 79%, 82%, 89% at 8B, 14B, 32B.

## 6. Disagreements, held open

| Question | First reviewer | Second reviewer | Standing |
|---|---|---|---|
| Odds of 90% and 99% | 38% and 4% | 45% and 8%, unmoved | Both are judgment. The first reviewer weighs the from-scratch and saturated-training results against; the second declines to move on partial reads. Held side by side |
| What Boole's signed scales show | Evidence that its scales were trained as free numbers | No inference about the optimizer; a negative scale is a second way to write the same group | The first reviewer's wording is softened to evidence, not proof. The count of negative scales in the file (trial S5) will show whether any exist |
| Whether a smooth map is a method | Yes for a start from the parent: published, with results | Not until a map, a start and a closing are specified | No conflict once the published one is named; both hold that it needs a separate closing stage |
| The order of runs, and a combined method of local re-fitting with priced flips | Not in scope of this batch | Proposed in its section 5A | Approved as an idea by the project owner's ruling of 26 November 2026, and entered in the ideas register as I33. It is an idea to learn from, not a judged plan |

## 7. Errors

First reviewer:

- Read the first version of the RaBiT paper and reported no Qwen results. The published version trains Qwen3-1.7B, 4B and 8B. Corrected in the findings.
- Reported PBBQ, arXiv 2611.01564 and arXiv 2609.01962 as not found after searching for them. Their addresses were in the brief the first reviewer wrote. The first two are now read in part.
- Repeated the Spectra authors' statement that the gap between two and three levels closes with size, from their validation losses, without the task tables. Corrected.
- Stated as fact that Boole's scales are free parameters. It is an inference.
- Listed rotations inside a query and key pair as free without the condition that they commute with the position rotation.
- Before its own push it had re-read three sources earlier batches had read and carried one wrong figure from a tool's account; both were caught then.

Second reviewer:

- The reading standard set as a condition of return is unmet, as it states. No source was read whole, no figure was seen, and the code that settles what RaBiT does with one path and with the tied matrix was not opened.
- It treats the smooth-map and sign-budget methods as unspecified proposals. Both are published with code or results that earlier batches had already recorded.
- It leaves open whether Boole's two scales could oppose each other. Boole's card settles that they cannot.
- Its table for ASkewSGD and for ProxQuant quotes different rows than the first reviewer's read. Neither set was cross-checked; nothing rests on them.
- It asks for archives and file headers to be fetched for it. The parts the first reviewer has already read are in the findings; the rest is row C136.

## 8. What is adopted

1. The straight-through variant with its own scale is named as its own candidate, and any specification must state which backward rule it uses (C111).
2. The closed-form price of a flip with the scale re-fitted is recorded under idea I13.
3. The cage is written as a shape bound with a trained scale, with the true projection and the closing certificate (idea I24, hypothesis H20).
4. The condition for a rotation to survive the tied matrix, and the list of exact transforms in the feed-forward and attention blocks, are recorded under H11.
5. The information bound replaces the looser counting statement under U2 and the 99% row.
6. The weighted re-tying rule is added to trial S5.
7. A packed round-trip test on synthetic matrices (bit order, shift direction, padding, scale rounding, tied aliases) is recorded as a rule for every trial, with the old LittleBit unpacker as the example.
8. The capacity measurement's design takes both reviewers' criticisms (C124).
9. Spectra's task tables and the RaBiT Qwen3 table go under U2 and U4.

## 9. Odds after the comparison

| Claim | First reviewer | Second reviewer | Note |
|---|---|---|---|
| 90% retention, strict format, 1.7B | 38% | 45% | Unchanged by the comparison. New for: the same group's trainer keeps 94% of easy tasks at 2 bits on this parent. New against: from scratch, two levels fall further behind as size grows and sit at chance on MMLU |
| 99% retention | 4% | 8% | Unchanged |
| Five points from PrismML's released file | 78% | Not restated | The separate-scale variant removes the first reviewer's caution about latent margins |
| Conversion from public recipes reaches 70.2% | 50% | Not restated | |
| Boole was trained by a one-matrix form of its author's group's trainers | 55% | No inference | Up from 50%: the published RaBiT paper trains Boole's own parent |

## 10. Still open

- Row C136: the unread parts of PBBQ, the memorization paper, TWLA, NanoQuant's code, the factorization notebooks, SDQ-LLM's code, LittleBit's paper, the first Kashin paper, the three-level Qwen3-4B report, and three papers found by search.
- No figure of any paper has been seen by either reviewer in this batch.
- The count of negative scales in Boole's file (trial S5).
- Which backward rule the straight-through specification uses (C111). This is settled on paper between the reviewers; nothing is needed from the project owner for it.
