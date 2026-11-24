# Batch 6: the two reviews compared

The first reviewer's findings are `batch-6-findings.md`. The second reviewer's document is filed unchanged in substance as `batch-6-second-reviewer.md`. Each worked without sight of the other. Everything taken from the second reviewer below was checked at its source first, and the check is named.

## 1. Result

- The two reviews agree on every conclusion that matters: mirror descent does not move a model that already fits; no source shows this family working on a language model at 1 bit; cross-layer compensation is an end-to-end loss worth carrying over; double binary factorization is a different format; damage on our parent is spread out; the shrinking cage is a combination of published parts; no measurement of two-level capacity exists.
- The second reviewer's reading is shallower than asked and says so: every source is labelled read in part, ten of them from an abstract or index entry only, and no code was read. Its mathematics is the strongest part of either review.
- It found three sources the first reviewer missed, all confirmed: ASkewSGD, the nearest published relative of the shrinking cage; SDQ-LLM, noise shaping applied to language models including two small ones; and AF1, a successor to double binary factorization tested on Qwen3 from 8B up.
- It showed, with a two-weight example, that lowering a cap cannot by itself bring every weight onto the cap, and gave a condition that does: hold the group's norm and lower the cap to that norm over the square root of the group size. This changes how the hypothesis is stated.
- The first reviewer found what the second did not: MagR, the published form of the equal-magnitude idea for language model weights; a result on our own parent at 2 bits; the Caltech group's own one-bit linear theory; INQ; a conversion-only result on Qwen3-4B; and the content of the factorization code.
- The first reviewer made one factual error that reached the plan and is reversed here: the damage-structure paper does have a second version.
- On the odds of a conversion of our own both stand at 45%. The project sets no limit on training, so no figure is conditioned on a budget; section 7 sets the judgments side by side.

## 2. Depth of the second reviewer's read

| Kind of read | Sources |
|---|---|
| Primary text, in part, with tables | The Caltech application (one country's text), the three Caltech mirror-descent papers, the random-features paper, the mirror-descent-view paper, democratic representations, greedy path following, SDQ-LLM, Noda, double binary factorization, AF1, the damage-structure paper (version 2), the feature paper, CEWT, ASkewSGD, Morris, the binary perceptron note, "Linger and Lose" |
| Abstract or index entry only | The follow-up to greedy path following, the knowledge-capacity paper, ProxQuant, OneBit, BiLLM, ARB-LLM, PBBQ, the 2026 memorization paper, the random-transformers paper, the 2024 Kashin paper |
| Code | None. One repository's front page was opened |

It states at the top that the report does not meet the brief's request for full reads and a code audit. That is accurate, and it is the honest way to return less than was asked. No figure it gives was found wrong.

## 3. Where the two agree

| Subject | Both find |
|---|---|
| Mirror descent from a pretrained start | The proved solution is the one nearest the start. With the student equal to the teacher the gradient is zero and nothing moves. A second force is needed |
| The mirror-descent-view paper | Real 1-bit results on CNNs; nothing on language models; its tables transcribed identically |
| Random features | A statement about random hidden weights with a full-precision last layer. Not a conversion theorem. A warning about the output matrix |
| Democratic representations | At least N minus M plus 1 entries at the maximum; nothing forces all of them; the room depends on input rank, which has to be measured |
| Greedy rounding | The theorems are for alphabets with a zero; nothing proved at two levels |
| Noda | Qwen2.5-1.5B, our block format, tied matrix in 16 bits; the final-state loss beats logit distillation (9.56 against 14.09); layer by layer fails; statistics matching does not bring quality; off its own text it is far worse; all table values agree |
| Double binary factorization | A different model class and file format; nothing under 7B; all table values agree |
| Damage structure | Spread out on Qwen3-1.7B at 4 bits; no proxy locates it; 66.9% against 14.9% for the global against the local use of the same extra bits |
| Feature damage | Perplexity can improve while a fifth of features degrade; values agree |
| CEWT | A projection to a Gaussian histogram during pre-training from scratch; not a cage |
| Capacity | 3.5 to 3.8 bits per weight on random strings, 2 on synthetic facts, nothing measured at two levels; the ternary figures of "Linger and Lose"; rounding after training at three levels stores nothing |
| The smallest capacity experiment | Tiny models, synthetic facts, 16-bit, three-level and two-level arms, packed checkpoints, not run without approval |

## 4. What the second reviewer found that the first did not

Each was checked against the paper itself through the text mirror.

### 4A. ASkewSGD

- Leconte, Schechtman, Moulines, arXiv 2211.03741. The second reviewer cites its AISTATS 2023 record; the arXiv text read here is marked as a preprint.
- Training with binary or low-bit weights is written as a sequence of problems, each allowing every weight to lie within a small interval around one of its levels. The interval width is annealed toward zero, so the allowed set shrinks onto the discrete one. Full-precision weights are updated by ordinary backpropagation. A weight outside its interval is pulled toward it instead of following the gradient. Iterates are allowed to be infeasible. No estimator is used for weights. Signs are taken at the end.
- Its theorem covers a fixed interval width and says the iterates approach stationary points of that relaxed problem. Nothing is proved for the annealing as a whole.
- Confirmed table, ResNet-18 on ImageNet, binary weights, 100 epochs, one run:

| Method | Top-1 |
|---|---|
| Full precision | 66.39 |
| BinaryConnect | 45.85 |
| Mirror descent (the tanh method) | 46.38 |
| AdaSTE | 35.37 |
| Projected gradient | 2.58 |
| ASkewSGD | 46.95 |

- On TinyImageNet: 50.23 against 42.35 for BinaryConnect, 48.79 for ProxQuant, 34.89 for the tanh method and 56.46 in full precision.
- The projected-gradient arm projects onto a sphere, as far as the text says; how that yields binary weights is not described. It is not a clip to a box, and the second reviewer says so. It scored 2.58% on ImageNet and 71.34% against 88.98% on CIFAR-10.
- Relation to the shrinking cage: it shares the central move, a feasible set that tightens on a schedule while exact gradients train full-precision weights with no estimator. It differs in the constraint (two-sided intervals around fixed levels of plus and minus 1, per weight, where the cage is an upper bound per group whose value is the scale), in having no distillation and no pretrained start, and in scale (CNNs). This is the closest published method and the first reviewer's search did not surface it.

### 4B. Why a descending cap alone does not finish

- The second reviewer's example: fit the target (1, 0) with two independent inputs. Under a cap c below 1 the best point in the box is (c, 0). Lower the cap as far as you like and the second weight stays at zero; it never reaches the cap. The best two-level answer with a free scale is (0.5, plus or minus 0.5). Checked by hand here.
- So the cap fixes the large weights and leaves the small ones wherever the loss wants them. The plan's statement of the hypothesis already ends with a sign search or a short straight-through pass for the weights left free. The example shows that step can be most of the work.
- Its closure condition: if a group's Euclidean norm is held at R and its cap lowered to R over the square root of the group size, every magnitude must equal the cap. A box and a sphere that touch only at the corners leave nothing else. The allowed set is not convex, so no mirror-descent theorem applies, and nothing says a suitable R keeps the teacher's function. It is a testable design, and it is recorded as idea I24.
- Its derivation of the inverse map for the Caltech rigid-cage potential (the largest magnitude plus a small ridge term) was re-derived here and is correct: subtract from the dual vector its projection onto the unit ball of the sum-of-magnitudes norm, and divide by the ridge weight. All weights of a group sit on the shell exactly when the threshold of that projection is no larger than the smallest dual magnitude. It independently found the missing division by the ridge weight in the application's printed equation 28, which checklist row C42 already records from an earlier review.

### 4C. SDQ-LLM

- Xia and others, arXiv 2510.03275. Each weight block is upsampled and passed through a first-order sigma-delta quantizer after a Hadamard transform.
- Confirmed table, WikiText-2 perplexity at three levels with an oversampling ratio of 2:

| Model | 16-bit | SDQ |
|---|---|---|
| Llama-3.2 1B | 9.75 | 298.31 |
| Llama-3.2 3B | 7.81 | 31.65 |
| Llama-3 8B | 6.13 | 17.02 |
| LLaMA-2 7B | 5.47 | 14.06 |
| LLaMA-2 13B | 4.88 | 6.95 |
| OPT 1.3B | 14.62 | 38.24 |

- The second reviewer warned that the stored size had to be counted. Counted here from the paper's own formula: three levels at an oversampling ratio of 2 is 3.16 bits per original weight, not 1.58. The paper reports no result at two levels.
- So noise shaping with a rotation, at more than 3 bits per weight, leaves a 1B model at thirty times its teacher's perplexity. It joins Qronos and MagR in section 2F of the first reviewer's findings as a third failure of conversion alone at small size.

### 4D. AF1

- Zhao and others, "All for 1-Bit", arXiv 2609.06161. Double binary factorization with a correction steered into the unused directions of the fixed factor, a per-layer rank budget from Shapley estimates, and a last stage that freezes every sign and trains only the scaling vectors against the teacher's output distribution on 128 sequences. The first 100 thousand of 121 thousand characters were read here.
- Confirmed table at an average of 1.00 bit: Qwen3-8B 54.82 against 69.09 on seven zero-shot tasks, perplexity 16.26 against 9.00; Qwen3-14B 59.61 against 72.47; Qwen3-32B 64.26 against 72.42; Llama-3 8B 45.48 against 72.51. No model under 4B in the main results.
- Not in the second reviewer's text, read here: on instruction-tuned models at 1.00 bit, Llama-3.1 8B falls from 83.24 to 44.78 on GSM8K and from 67.07 to 36.71 on HumanEval; Qwen3-14B from 94.77 to 64.66 and from 89.63 to 49.76.
- Its own accounting puts BiLLM at 2.88 bits per weight, STBLLM at 3.50 and ARB-LLM at 2.51 once every mask and scale is counted. Published "1-bit" labels in this literature are not comparable to our 1.125.
- It is a second source that uses scale-only distillation with signs frozen as a repair stage. Its isolated effect was not extracted.

### 4E. Other points taken

- The exact storage of double binary factorization with 16-bit vectors, and the largest middle width that fits our rate: 1,131 for a 2,048-square matrix, so the factorized matrix has rank at most 55% of full. Arithmetic checked here.
- "Linger and Lose" under its other scoring conventions. The retention figures for 25M and 50M depend on how one attribute is floored: 0.090 and 0.058 become 0.126 and 0.109. A second estimator, of the Morris kind, gives 0.200 and 0.185 at 10M and 25M and does not register the collapse at all (0.567 after, 0.557 before). One 16-bit run also crashed. Confirmed in the paper. The first reviewer's findings gave the headline figures without these qualifications; they are added there.
- The fine-tuning control of the same paper ends at 0.402 and 0.371 bits per weight without collapsing. This is the same fact the first reviewer reported as losing 90% of what the 16-bit model knew and landing on the from-scratch level; both descriptions are in the paper.
- A tied embedding and output matrix cannot be given two optimizers without untying it. Any separate treatment of its two roles has to act on the two gradient paths. This matches idea I12.
- Two checks before any proposed optimizer is run: that its first update at the teacher is not zero, and that its end point is exactly representable in the format.
- Tokens spent in a final straight-through phase count against the method that needs them.

## 5. What the first reviewer found that the second did not

- MagR: a penalty on the largest magnitude of language model weights that keeps each layer's output, with a per-group form, and its table of how much of each layer's input space is in use. The second reviewer reasoned about that rank in the abstract and noted it must be measured; this is a published measurement, on other models.
- Qronos, with our own parent at 2 bits (zero-shot 36.7 against 61.4) and Llama-3 1B at 1.58 bits near chance.
- The Caltech group's two papers on infinity-norm regression, where every coordinate goes to plus or minus one value and the price in the ideal case is a factor of 2 over pi.
- The two follow-ups of greedy path following read in full, and the analysis of GPTQ, which settle that no theorem in that line covers two levels.
- INQ and random partition relaxation, the two published methods that train free weights with exact gradients while others are held quantized, with the result that weighs against a cage that starts mostly free.
- The conversion-only report on Qwen3-4B.
- The factorization code: its loss, its frozen full-precision embedding and output matrix, and its per-step rule for flipping signs.
- What the large-power step does from each of the three starts, including that from a binary start it is an ordinary step.

## 6. Errors

### 6A. The first reviewer's

- The damage-structure paper has a version 2 dated 15 November 2026. The first reviewer saw version 1 on the mirror, took one reading of the arXiv listing as showing a single version, and changed the plan's source line. The mirror serves version 2 at its own address and it was read there afterwards. The plan's line is restored. The budget table is the same in both versions; version 2 adds a column for the share held by the single largest layer.
- ASkewSGD was missed. The prior-art searches used terms for clipping and boxes and did not reach a paper that describes its constraint as intervals.
- SDQ-LLM and AF1 were missed. The findings said greedy and noise-shaping rounding had been applied to language models only through one line of work.
- The capacity figures of "Linger and Lose" were given without the paper's own qualifications on how they are scored, and the odds of the 99% goal were moved on them. The move is withdrawn.
- The findings did not state that a descending cap leaves small weights off the cap. The plan's hypothesis text allowed for it; the findings should have said how large that remainder can be.

### 6B. The second reviewer's

- The brief asked for full reads with code. None was delivered, and ten sources were read from abstracts or index entries. Stated openly.
- SDQ-LLM is presented at "nominal 1.58 bits" with a warning. The stored size, 3.16 bits per original weight, is in the paper.
- It presents "Linger and Lose" as a new discovery. The project has held it since batch 2. A reviewer new to the project could not know.
- Its overall odds, 45% for a conversion of our own reaching 70.2%, are conditioned on a budget it chose (a billion processed tokens). The project sets none. The figure is a judgment in both reviews: the only 1-bit result on a model of this size in either is 9.56 times the teacher's perplexity with the tied matrix exempt.
- It raised the odds of the mirror-centred route (25% to 30%) on the application's plateau geometry while its own section shows the method does not move from the teacher.

## 7. Disagreements, held open

| Subject | First reviewer | Second reviewer | Note |
|---|---|---|---|
| A conversion of our own from the full-precision parent reaches 70.2% | 45%, with no cap on training: the plan's standing figure for matching the released model | 45%, given a billion processed tokens | The same figure. Neither is backed by a 1-bit result at this size with the tied matrix converted; what limits it is the recipe |
| The mirror or greedy family as the route | 8% that the mirror step is the missing piece | 30% that this route reaches 70.2% | Different events |
| Global compensation as the route | A final-state term helps any end-to-end training: 60% | 38% that this route reaches 70.2% | Different events; both favor it as the loss |
| The 99% goal | 5% | No number: no figure from a count of states is defensible | The first reviewer's move to 4% is withdrawn |

## 8. What is adopted

- The hypothesis H20 is restated with its end condition: a descending cap needs a closure rule, and holding the group norm is one. ASkewSGD is named as its nearest published relative, ahead of INQ and MagR.
- Idea I24: closing the cage by a fixed group norm. From the second reviewer.
- Two pre-run checks for any optimizer of our own: a nonzero first update at the teacher, and an end point the format can represent.
- The capacity measurement (C124) takes from the second reviewer's design: an arm on random strings beside the synthetic facts, estimators reported both signed and floored, scoring from packed checkpoints, and a stated plateau rule.
- Sources S135 to S137. Reading row C125 extended with what neither reviewer read.
- M3's record keeps scores of packed checkpoints through training with a knowledge probe beside them, so a late loss of facts is seen when it happens.
- Not adopted as new, because the registers already hold it: scoring the packed file (the ruler's stored-form check), the list of damage measures (S4 and the ruler), the schedule as a variable (batch 2).

## 9. Odds after the comparison

| Subject | After the first reviewer's findings | After the comparison | Why |
|---|---|---|---|
| Sign and scale training from the released model reaches a step | 72% | 72% | |
| Scale-only training reaches a step | 55% | 55% | AF1 is a second source using it as a stage; its isolated effect is not known |
| Our own conversion reaches 70.2% | 45% | 45% | The plan's figure for matching the released model. Time and compute are not limits on this project |
| The shrinking cage as a whole is unpublished | 65% | 55% | ASkewSGD shares its central move |
| The shrinking cage, with a closure rule, beats straight-through training at equal tokens | 15% | 15% | The closure rule makes it complete; ASkewSGD's own margin over BinaryConnect is about one point |
| The mirror step is the missing piece of our own conversion | 8% | 8% | |
| 99% retention, strict format, 1.7B | 4% | 5% | Section 6A |

## 10. Still open

- Read by neither reviewer in full: the structured Kashin paper (arXiv 2609.11687), PBBQ, the 2026 memorization paper (arXiv 2611.01564), the last fifth of AF1, BinaryRelax and ProxQuant, LittleBit-2, the TWLA paper, the appendix of the knowledge-capacity paper, the figures of every paper in this batch, and all code except one fine-tuning script.
- The share of input directions in use in each matrix of Qwen3-1.7B (C28).
- What two-level weights store (C124, not approved to run).
- Whether a cage with a closure rule works on anything larger than a toy.
