# Batch 6 findings: mirror descent and its relatives, compensation and factorization, the structure of damage, a prior-art search and capacity

First reviewer's findings for batch 6. The same three items went to the second reviewer in `batch-6-prompt.md`. Nothing here was written with sight of that reviewer's work.

How sources were read. arXiv papers were read through the text mirror at alphaxiv.org, which serves the whole paper as text; the reading tool returns a detailed account of that text, section by section, with every table. Figures were not seen. Code was read directly from its repository. Where only part of a source was read, section 9 says which part.

This batch serves the further goal: a conversion formula of our own from the full-precision parent. It does not change which trial runs first.

## 1. Result

- No theorem in any source covers the case this project is in. Every guarantee found is for a model that starts at zero, or is linear, or has random weights, or keeps a zero in its alphabet.
- Mirror descent is proved to end at the fitting solution nearest its start. From a pretrained start that is the pretrained model. From a model that is already binary, the large-power step is an ordinary step. The Caltech potential is a from-scratch idea; as a conversion it needs a second force, and the sources do not supply one.
- The one published method at 1 bit that calls itself mirror descent is, in its working form, straight-through training with a sharpening tanh. Its author says so.
- The equal-magnitude idea has been applied to language model weights, by a method this project did not hold: MagR. It includes a per-group form. It works as a preparation step at 2 to 4 bits on 7B models and above. With rotation and the best greedy rounding it still leaves a 1B model near chance at 1.58 bits and our own parent near chance at 2 bits.
- The measured room for it is small. MagR's own table puts the typical layer of a 7B model at 70% to 77% of its input directions in use. By this project's count that lets about a quarter of a row sit at its group's maximum for free.
- Cross-layer compensation is an end-to-end training loss, in our block format, on a 1.5B model: nine minutes of training gives 9.56 times the teacher's perplexity with the tied matrix left in 16 bits. It shows that a final-state loss beats a logit loss at a tiny budget, and that fitting layer by layer fails at 1 bit.
- Double binary factorization is a different format and has no result under 7B. At equal stored bits it beats one sign matrix with row and column scales. It cannot be written as one sign per weight.
- The shrinking cage is not found published as a whole. Every one of its parts is: largest weights converted first while the rest train with exact gradients (INQ), a per-group penalty on the largest magnitude (MagR), the end point for one layer (Cadzow, democratic representations), a fixed box (BinaryConnect), a projection after every step (CEWT).
- Capacity. Real weights store about 2 bits of facts each, 3.5 by another measure. Ternary weights trained from scratch store 0.16 to 0.41 at full load, a quarter of what the same model stores in 16 bits, and half to three quarters at light load. No measurement exists for binary weights in a transformer. The 99% goal at 1.7B stands on the teacher being lightly loaded, which is not known.

## 2. Item 1: mirror descent and its relatives

### 2A. What was read

| Source | How much | Route |
|---|---|---|
| Azizan, Lale, Hassibi, stochastic mirror descent on overparameterized nonlinear models, arXiv 1906.03830 | Whole paper with appendices | Mirror |
| Azizan, Lale, Hassibi, regularizer mirror descent, arXiv 2202.10788 | Whole paper with appendices | Mirror |
| Akhtiamov, Ghane, Hassibi, one-bit quantization for random features models, arXiv 2510.16250 | Whole paper | Mirror |
| Akhtiamov, Ghane, Pooladzandi, Hassibi, matrix stochastic mirror descent, arXiv 2602.18997 | Whole paper | Mirror, found by title search |
| Ajanthan and others, mirror descent view for neural network quantization, arXiv 1910.08237 | Whole paper with appendices | Mirror |
| Studer and others, democratic representations, arXiv 1401.3420 | Whole paper | Mirror |
| Lybrand, Saab, greedy path-following quantization, arXiv 2010.15979 | Whole paper | Mirror |
| Zhang, Zhou, Saab, post-training quantization with provable guarantees, arXiv 2201.11113 | Whole paper | Mirror |
| Zhang, Saab, stochastic path-following quantization, arXiv 2309.10975 | Whole paper | Mirror |
| Qronos, arXiv 2505.11695 | Whole paper | Mirror |
| Zhang, Zhang, Colbert, Saab, analysis of OPTQ and Qronos, arXiv 2508.04853 | Whole paper | Mirror |
| MagR, arXiv 2406.00800 | Whole paper | Mirror. Found through Qronos |
| Ghane, Akhtiamov, Hassibi, one-bit quantization for multiclass linear classification, arXiv 2402.10474 | Whole paper | Mirror. Found by search |
| Akhtiamov, Ghane, Hassibi, regularized linear regression for binary classification, arXiv 2311.02270 | Whole paper | Mirror. Found by search |
| Quantization of language models with an overdetermined basis (Kashin quantization), arXiv 2404.09737 | Whole paper | Mirror. Found by its title |
| The Caltech application, US 20260220467 A1 | Read in full in an earlier batch (checklist C25). Not re-read | |

### 2B. What each one proves

**Mirror descent (the three Caltech papers).**

- For a linear model with more weights than data, mirror descent with any strictly convex, differentiable potential converges to the fitting solution with the smallest Bregman distance from the starting point. If the start is the potential's own minimum, that is the fitting solution with the smallest potential.
- For a nonlinear model the same holds approximately and locally: the start must already lie within a small Bregman distance of a fitting solution. No constants are given. The claim that a random start is close enough rests on a heuristic the authors label as one.
- The regularized form solves "loss times a weight, plus the potential" by adding one helper number per training example. Its guarantee is again local, and the authors state it does not imply zero training error. When started from a given model instead of zero, what it minimizes is the Bregman distance from that model, not the potential.
- The matrix paper extends the linear result to matrix weights with a rate. Its potentials are spectral norms. It contains nothing on quantization, equal magnitudes or networks.
- Experiments: a small network on MNIST and ResNet-18 on CIFAR-10 from a start near zero, with powers 1, 2, 3 and 10. At power 10 nearly every weight is nonzero and magnitudes lie between about 0.005 and 0.04: a band eight times wide, not one shell. The regularized form was tested with the square potential only. Both papers say a large power should suit quantization. Neither tests it.

**One-bit theory from the same group.**

- Random features: when hidden weights are random and only the last layer is trained, replacing every hidden weight by its sign changes nothing in the limit of wide layers. The last layer stays in full precision, and the authors say quantizing it would cost accuracy. A trained weight carries exactly the information this setting assumes away.
- Linear classification under strong infinity-norm regularization: as the regularization grows, every coordinate of the solution moves to plus or minus one common value, so its sign is the same classifier. Shown for Gaussian mixtures with 1.5 to 10 times more weights than samples, and on five MNIST digits. The equality of the one-bit and unquantized errors at large regularization is, in the authors' words, an empirical observation.
- The same papers give the price in the cleanest case. With the class means known, the best classifier has error set by a signal-to-noise term; the best one-bit classifier has the same term multiplied by 2 over pi. That is the same 0.637 by which this project's toy tests found plain sign conversion to shrink a matrix's signal.

**Democratic representations.**

- For a row of N weights whose inputs span M directions, an exactly equivalent row exists with at least N minus M plus 1 entries at the maximum magnitude. For generic inputs every minimum-maximum row has this property. This is this project's count with one group.
- An upper bound on the maximum needs the inputs to satisfy an uncertainty principle, shown for random inputs at redundancy 2 and above, and it tightens as redundancy grows.
- The equal-magnitude row has more energy than the minimum-energy row. The paper bounds the increase. Nothing is guaranteed at low redundancy, and the paper notes that adverse cases exist.
- That such rows survive rounding better is stated in words. No theorem is given.

**Greedy and noise-shaping rounding.**

- Each weight is rounded in turn so that a running error vector on real inputs stays small. The error bound is of the order of the square root of (input directions in use, divided by fan-in), so it needs many more weights per row than directions in use.
- Every theorem in this line is for an alphabet that contains zero, or for an infinite grid. The first paper's proof uses the zero case. The second covers grids of the form plus or minus k steps. The third needs an alphabet that grows with the logarithm of the width. The analysis of GPTQ assumes an infinite grid and names the two-level case only in a remark on a different problem. No theorem covers two levels.
- The third paper's exact variant first replaces each row by its minimum-maximum equivalent, then rounds. It also proves that a small change in the inputs can enlarge that row's maximum without bound, and restricts its results to random weights for that reason.

### 2C. Which maps are valid, and where each ends

| Map or potential | Valid mirror map | Ends at plus or minus one scale without a rounding loss |
|---|---|---|
| Power potential, any power above 1 | Yes | Only approximately, from a zero start: a band eight times wide at power 10 |
| Infinity norm itself | No: neither strictly convex nor differentiable | The limit the large power stands in for |
| Any strictly increasing continuous squashing function onto an open interval (tanh and others) | Yes, by the theorem of the mirror-descent-view paper | Yes as the sharpness goes to infinity, on a fixed box of plus or minus 1. The scale is a separate parameter |
| Shifted tanh for three levels | Yes, no closed form | Three levels |
| Infinity-norm penalty in linear regression, strength to infinity | Not a mirror map; a penalty | Yes, proved for the linear case |
| Spectral norms | Yes | Not relevant |

The numerically stable form of the tanh method updates a latent weight with the gradient taken at the squashed weight. The paper states this is the straight-through estimator. The direct form was unstable in the authors' hands.

### 2D. Every result at 1 bit

| Source | Model | Method | 1-bit result | Full precision |
|---|---|---|---|---|
| Mirror-descent view | ResNet-18, CIFAR-10, every layer binary | Tanh, stable form | 93.18% | 94.84% |
| Same | ResNet-18, TinyImageNet, every layer binary | Tanh, direct and stable | 54.62% and 52.32% | 58.35% |
| Same | ResNet-18, ImageNet, first and last layers kept | Tanh, stable, from pretrained | 66.78% | 70.61% |
| Same | ResNet-18, ImageNet, every layer and bias binary | Same | 56.60% | 70.61% |
| Same | ResNet-18, ImageNet, with a scale per layer | Same | 61.91%, worse than without | 70.61% |
| Noda (section 3B) | Qwen2.5-1.5B, blocks only, sign and one scale per 128 | Tanh sharpened 1 to 16, final-state loss, 4.1M tokens | 9.56 times the teacher's perplexity | 11.951 |
| Linear classification, Caltech | Five MNIST digits, linear | Infinity-norm regression, sign | About 0.09 test error, same as unquantized | Same |
| Random features | Synthetic and MNIST | Sign of random hidden weights | Curves coincide | |

No result at 1 bit was found for the large-power potential on any network, and none for greedy or noise-shaping rounding on any language model.

### 2E. The cost of forcing equal magnitudes

- In the one case with a closed form, taking signs of the ideal direction multiplies signal-to-noise by 2 over pi (section 2B).
- Exact equivalence only covers N minus M plus G entries of a row with G groups. MagR measured the share of input directions in use, counted as singular values above 1% of the largest, for every layer of seven models:

| Model | Mean | 25th percentile | 75th percentile | Smallest |
|---|---|---|---|---|
| LLaMA-1 7B | 70.4% | 65.1% | 81.8% | 0.2% |
| LLaMA-2 7B | 76.8% | 67.7% | 91.0% | 0.1% |
| LLaMA-2 13B | 78.3% | 66.5% | 98.6% | 0.4% |
| LLaMA-2 70B | 81.6% | 74.9% | 99.6% | 0.1% |

- Arithmetic on that table: at 77% of directions in use, a row of 2,048 weights in 16 groups has (2,048 minus 1,577 plus 16) over 2,048, 24%, of its entries free to sit at their group's maximum. At 67% it is 34%. At 91% it is 10%. This project's toy tests found the equivalent-row route worse than plain signs below a redundancy of about 1.33, which is 75% of directions in use. The typical layer sits at that boundary; a few layers, at under 2%, have nearly unlimited room.
- The count is exact equivalence. Most of the gain a real conversion can have must therefore come from accepting error in weakly used directions, weighted by the data, not from equivalence. That is what calibrated rounding does, and what an end-to-end loss does.
- MagR's penalty has a narrow useful range. On LLaMA-2 7B at 3 bits, perplexity is 6.41 at its chosen strength, 6.64 at five times that and 7.08 at a hundredth. Inside Qronos, on a 1B model, ten times the chosen strength triples perplexity.
- The count above is from 7B models of another family. The same table for Qwen3-1.7B is this project's checklist row C28.

### 2F. Who has used this family on a transformer

| What | Who | Models | Lowest width | Outcome |
|---|---|---|---|---|
| Minimum-maximum weights per column or per group, layer by layer, before rounding | MagR | LLaMA 7B to 70B | 2 bits | Column maxima about halved; full-precision perplexity moves 5.47 to 5.52; at 2 bits with groups of 128, 9.94 against 5.47 on 7B. Zero-shot 42.4 against 63.8 at 2 bits per channel |
| The same, inside a greedy rounder with rotation | Qronos | Llama-3 1B, 3B, 8B; Qwen3 0.6B to 32B | 1.58 bits | Llama-3 1B at 1.58 bits: perplexity 39.3 against 8.9, zero-shot 34.8 against 59.4 with a floor near 32. Qwen3-1.7B at 2 bits: perplexity 23.5 against 15.2, zero-shot 36.7 against 61.4 |
| Kashin representation of weight matrices | Overdetermined-basis paper | OPT 125M and 350M, BERT, RoBERTa | 4 bits | A fifth of layers do not converge. Concentration of coefficients shown on a random matrix only. Stored bits per weight not stated |
| Greedy path following | Lybrand and Saab line, then Brevitas | CNNs; Llama-3 and Qwen3 inside Qronos's tables | 1.58 bits | At 1.58 bits on Llama-3 1B: perplexity about 100 |
| Mirror descent by tanh | Ajanthan and others; Noda | CNNs; Qwen2.5-1.5B | 1 bit | Section 2D |
| A mirror step in a ternary training script | Outside forensics project (batch 5) | Qwen3-1.7B | Ternary | Worse than its baseline, 23.01 against 2.93 |
| Large-power potential on any network at 1 bit | Nobody found | | | Searches: the inventors' papers since the filing, the application's citations, two open searches on mirror descent and 1-bit language models |

Since the filing, the inventors' group has published the random-features paper and the matrix paper. Neither trains a network with a large-power potential. PrismML's public statements say its models were trained on accelerators and give no method.

### 2G. What the large-power step does from each start

Reasoning on paper, from the update rule the first two papers give.

- With potential "magnitude to the power q, over q", the step in the weight is the gradient step divided by (q minus 1) times the magnitude to the power q minus 2. Large weights barely move. Small weights move fast.
- From zero. Every weight starts small and fast. A weight with a steady gradient grows until its own size slows it. Weights end at similar sizes because all were stopped by the same brake. This is where the method's equal-magnitude tendency comes from, and it matches the band seen at power 10.
- From a pretrained model under distillation. The student equals the teacher, so the gradient is zero and nothing moves. If something disturbs it, the large weights are pinned in place by the potential and only the small ones adapt. Nothing in the rule shrinks a large weight toward a shell. The theorem says the same thing: the method stays as near its start as it can.
- From a model that is already binary. Every latent weight in a group has the same magnitude, so the divisor is one number per group. The step is an ordinary gradient step with a group-wise rate. The method has no effect of its own until training has spread the magnitudes.
- So the potential is a way to train from scratch toward equal magnitudes. As a conversion it needs a force that first moves large weights inward. An explicit penalty on the maximum does that (MagR, the linear theory). So does a cap that descends (section 4C).

### 2H. Answer: what would have to be true

For this family to beat ordinary straight-through distillation at equal tokens on Qwen3-1.7B in our format, all of these:

1. A force toward the shell that acts from a pretrained start. The theory supplies none.
2. Enough unused input room that near-shell rows cost little. MagR's count says a quarter to a third of a typical row, more in a few layers. Unknown for our parent until C28 is run.
3. The gain must survive the last step. Rows that are 24% on the shell still have 76% of their entries to snap, and that error has to be absorbed end to end.
4. A stable numerical form. The direct tanh update was unstable for its authors, and the outside project that ran a mirror step notes it needs 32-bit arithmetic.

Where the theory says it cannot: at low redundancy (no guarantee, adverse cases), for the last layer (the random-features paper), and from a start that already fits (nearest-solution property).

### 2I. Unknown, and the cheapest way to find out

- The share of input directions in use for each matrix of Qwen3-1.7B. C28, forward passes only.
- Whether a per-group maximum penalty, raised on a schedule and trained end to end, yields better signs than straight-through training at equal tokens. This is the shrinking cage; section 4C.

## 3. Item 2: compensation and factorization

### 3A. What was read

| Source | How much | Route |
|---|---|---|
| Noda, cross-layer error compensation, arXiv 2607.14630 | Whole paper with appendix | Mirror |
| Boža, Macko, double binary factorization, arXiv 2505.11076, version 4 | Whole paper | Mirror |
| Its code, github.com/usamec/double_binary | File list, both READMEs, the fine-tuning script, the run script, the license. The two compression notebooks were not opened | Repository read directly |
| Post-training ternarization of Qwen3-4B, arXiv 2609.01962 | Whole report | Mirror. Found by search |

### 3B. Cross-layer compensation

- One model: Qwen2.5-1.5B. The 196 block matrices, about 1.31 billion weights, become one sign per weight with one 16-bit scale per 128 consecutive weights of a row: 1.125 bits, this project's block format. The embedding and output matrix stay in 16 bits.
- The name describes a loss, not a correction applied after the fact. The loss is the squared difference between the converted model's final hidden state and the teacher's, divided by the teacher's squared norm. A lemma shows that this equals the layer-by-layer error recursion exactly, which is why two forward passes replace any Jacobian. Every sign and scale in the model is trained jointly against it.
- Signs come from a tanh of a latent weight whose sharpness rises from 1 to 16; the last fifth of the steps use the hard sign forward with the tanh's gradient. Scales are learned in the log domain from the group mean.
- The author calls the tanh parameterization mirror descent and presents it as a restatement of the mirror-descent-view paper.
- Data and cost: WikiText-2 training text, 0.13 million tokens; 1,000 steps of 8 sequences of 512 tokens, 4.1 million tokens processed, so about 31 passes over the same text. One A100, about nine minutes a run, three seeds.

| Arm | Perplexity against the teacher's, WikiText-2 | On C4 | On CNN/DailyMail |
|---|---|---|---|
| Plain conversion | About 2 billion times | | |
| Each layer fitted to its own output | About 1,400 times | | |
| Logit distillation only | 14.09 | 73.8 | 54.1 |
| Statistics matching only | 262 | 780 | 484 |
| Final-state loss only | 9.56 | 46.1 | 33.4 |
| Both | 11.50 | 62.9 | 44.9 |

- At 4 bits with the same groups: 1.201 by rounding, 1.088 layer by layer, 1.060 with the final-state loss.
- No benchmark scores. No public baseline was run. No code address; notebooks are offered on request. A patent application is said to be pending.
- What it shows for us: the final-state loss beats logit distillation by a third at this budget; fitting layer by layer is three orders of magnitude worse than end to end at 1 bit, which is what batch 5 held; matching feature statistics is not what brings quality. The 9.56 is a nine-minute, in-domain figure with the tied matrix untouched. It is a floor for what training can do, and off its own text it is five times worse.

### 3C. Double binary factorization

- A weight matrix becomes a product of two sign matrices with three scaling vectors: one per output, one per middle unit, one per input. The middle width sets the storage: at an average of 1 bit per original weight a square matrix gets a middle width of half its size. The vectors add about 0.012 bits per weight on a 4,096-square matrix.
- Factorization alternates between the two factors with ADMM; each projection is a sign matrix times a rank-one fit to the magnitudes. Weights are scaled by input activation norms and output gradient norms first. Then the continuous parameters are fine-tuned block by block on 256 sequences, and signs are tuned on a random tenth of the layers at a time.
- Results exist for Llama-2 7B and Llama-3 8B only.

| Model | Bits | Method | Perplexity | Zero-shot average |
|---|---|---|---|---|
| Llama-2 7B | 16 | | 5.12 | 66.73 |
| | 1 | OneBit | 9.73 | 49.43 |
| | 1.1 | BiLLM | 32.48 | 43.40 |
| | 1 | This, with sign tuning | 8.76 | 53.10 |
| | 1.5 | This, with sign tuning | 7.01 | 60.03 |
| | 2 | This, with sign tuning | 6.09 | 62.76 |
| Llama-3 8B | 16 | | 5.54 | 70.71 |
| | 1 | This, with sign tuning | 13.57 | 51.89 |

- On Llama-3 8B at 2 bits, MMLU falls from 65.29 to 52.67 and GSM8K from 54.89 to 26.15. The authors call these results erratic.
- At an average of 1 bit, the number of sign additions is the same as for one sign matrix of the original shape. Decoding is 2.5 to 2.9 times faster than 16-bit on one desktop card.
- The code is Apache-2.0 and is a working directory, not a tool: two notebooks, one per model, and a fine-tuning script whose layer loop is fixed at 32 blocks. Nothing in it runs a model under 7B as written.
- Read in the fine-tuning script: the loss is the student's log-probabilities against the teacher's probabilities, both through the frozen full-precision output matrix; the embedding is frozen too. Sign tuning keeps a latent copy of a sign matrix for the layers picked, and at each step flips only the entries whose latent has moved furthest against its sign: the top 0.001% in the run script. That is a working per-step budget on sign changes.

### 3D. Can either live in our format

- Noda's block format is ours. Its training recipe is a candidate for a conversion of our own and carries over directly, with the tied matrix as the open part.
- Double binary factorization cannot be written as one sign per weight: a product of two sign matrices is not a sign matrix. It is two sign layers in series. Each sign layer's row scales fit one scale per group. The per-input vector does not fit anywhere in a format with scales per row group, and the stock runtime has no place for the extra layer. Using it means a different file format and kernel.
- What is lost by not using it: at equal stored bits on 7B it is one point of perplexity and 3.7 points of zero-shot better than a single sign matrix with row and column scales. Nothing says what it does at 1.7B.

### 3E. Other work that gets more from few bits

- Post-training ternarization of Qwen3-4B, no training at all: a rotation, a ternary plane with a row offset, a second ternary plane on the 3.6% most salient weights, GPTQ, calibrated on 64 sequences. 1.641 bits per converted weight; embedding and output matrix in 16 bits. Perplexity 1.375 times the teacher's on WikiText-2. MMLU 68.5 to 51.0, which is 59.7% after correcting for chance; ARC-Challenge 43.8% after correction; BoolQ 84.6%. No single-plane result, no 1-bit result, no released files. It shows what conversion alone reaches at ternary on the next size up when a row offset and a second plane are allowed. Neither is in our format.
- LittleBit-2 (Samsung): below 1 bit by factorization with a rotation of the factors, trained with distillation. Found, not read.
- OneBit, BiLLM, STBLLM and the residual-plane methods are already in this project's sources.

### 3F. What to take

- As a stage: a final-hidden-state term beside the logit term in any end-to-end training this project specifies. Two sources now support it at small budgets (this one, and EdgeRazor's feature term in batch 5).
- As a setting: a per-step budget on sign changes of the kind the factorization code uses, chosen by how far a latent has moved against its sign. It is one concrete form for checklist row C111.
- As a warning: layer-by-layer fitting at 1 bit, and any perplexity figure measured on the text trained on.
- Not as a starting point: neither source gives a better start than the released 1-bit model for the nearer goal.

## 4. Item 3: damage, one hypothesis, capacity

### 4A. What was read

| Source | How much | Route |
|---|---|---|
| Hu, Ramachandran, structure of quantization damage, arXiv 2609.01587 | Whole paper, version 1 of 2 September 2026. Version 2 of 15 November 2026 read against it: the same budget table, with one added column for the share held by the single largest layer | Mirror, at the address of each version |
| Duan, perplexity can miss feature damage, arXiv 2606.03002, version 2 | Whole paper | Mirror |
| CEWT, quantization-aware pre-training with constrained weight distribution, arXiv 2609.32659 | All but the last 500 characters | Mirror |
| Morris and others, how much do language models memorize, arXiv 2505.24832, version 3 | Whole paper | Mirror |
| Altschuler, Tikhomirov, capacity of the binary perceptron, arXiv 2401.15092 | Whole note | Mirror |
| "Linger and Lose", arXiv 2609.32902 | Whole paper. Held since batch 2 for its schedule findings; re-read here for its capacity figures | Mirror |
| Allen-Zhu, Li, knowledge capacity scaling laws, arXiv 2404.05405 | Main text, first 100 thousand of 190 thousand characters | Mirror. Found through Morris |
| INQ, arXiv 1702.03044 | Whole paper | Mirror |
| Random partition relaxation, arXiv 2001.01091 | Whole paper | Mirror |
| Exact backpropagation with group weight transformations, arXiv 2107.01400 | Whole paper | Mirror. Found by search |
| Quantized-endpoint descent (QAR), arXiv 2609.21834 | Whole paper | Mirror. Found by search |
| BinaryRelax, arXiv 1801.06313; ProxQuant, arXiv 1810.00861 | Abstracts and the account of them in the mirror-descent-view paper | Search results |

### 4B. How conversion damage is structured

**The structure paper.** Nine models, among them Qwen3-0.6B, Qwen3-1.7B and Llama-3.2 1B and 3B. Only 4 bits and 8 bits. Damage is the loss on a 22-task suite when the whole model is rounded per row to 4 bits; the probe restores one layer at a time to 8 bits.

- Spread out: no layer holds more than about 44% of the damage in any model. Recovering half the gap takes a fifth of the layers; nine tenths takes three quarters of them.
- Additive across pairs of layers, within 0.91 to 1.10.
- Nothing predicts which layers matter. Circuit drift correlates with damage at 0.377 raw and 0.054 once model and task are controlled. Activation patching points at the first and last MLP layers; protecting them recovers 13% or less in six of nine models. Weight statistics and reconstruction error fail too. Reconstruction error rises with depth while the recoverable damage sits early.
- "Globally" means: at an equal 0.146 extra bits per weight, giving every row one scale per 128 weights in place of one per row recovers 66.9% of the gap on Qwen3-1.7B, against 14.9% for restoring the best whole layers. That margin is the largest of the nine. Finer scales add more than GPTQ or AWQ do on top.
- No split by matrix type, nothing below 4 bits, no repair, no code.

**The feature paper.** Pythia-70M and Gemma-2 2B, rounded per channel at 8 down to 4 bits, read through a fixed sparse autoencoder trained on the full-precision model.

- On Gemma at 7 bits perplexity improves by 5.65% while 18.7% of active features have degraded. At 6 bits half have. At 4 bits 12.4% survive.
- The fragile features are the weak ones: by quartile of peak activation, survival runs from 5% to 92%.
- No link to task scores is measured, nothing below 4 bits, no repair.

**What a damage map of a 1-bit model should measure, and should not trust.**

| Do not trust | Why |
|---|---|
| Weight or layer reconstruction error as a guide to where damage is | It rises with depth where the recoverable damage does not (structure paper); the same error gave 0.84 and 0.14 loss of recall in two components (PRISM) |
| Circuit analysis, activation patching, weight statistics as locators | None predicted the layers that matter in nine models |
| Perplexity or a logit distance alone | Half the features can blur while perplexity improves; stored facts fell 2.7 to 17 times while perplexity rose 1.4 to 2.9 times ("Linger and Lose") |
| A map made on another model or with another converter | PRISM, batch 5 |
| Sums of parts without a check | Pairs of layers added up at 4 bits; the two matrix classes did not (PRISM) |

| Measure | Why |
|---|---|
| Exchange tests on the model itself, by block | The only locator that worked |
| An additivity check on a few pairs | It says whether single-block figures may be summed |
| Task outcomes item by item, and knowledge directly | Section 4D; the PRISM probe |
| Weak signals separately from strong ones | Rare facts and weak features go first in three sources |

S4 measures by exchange of states on the released model, which is cumulative by block: it has no single-block figures, and the steps of its curve are not separate effects to be summed. Section 7 adds that caution to its text. A pair check would need blocks exchanged by weight, which means something only while the two models' blocks are still interchangeable.

The finer-scales result is about a rounding with one scale per row. Our format already has one per 128.

### 4C. The shrinking cage: nearest prior work

The hypothesis: train full-precision weights under distillation with exact gradients; after every step clip each group of 128 to a cap that descends on a schedule; a weight on the cap is binary with the cap as its scale; free weights compensate; no estimator until the end.

| Work | What it shares | How it differs | Scale tested | Reported |
|---|---|---|---|---|
| INQ, 2017 | Largest weights are converted first; the rest stay full precision and are retrained with ordinary gradients to compensate; repeated until none are free; no estimator | Converted weights are rounded to a grid and frozen for good; the share converted is a hand-set ladder per network; powers of two, no scale per group; no distillation | CNNs on ImageNet, from pretrained | ResNet-18 at three levels: 66.02% against 68.27%. No 1-bit result. Choosing by magnitude beat choosing at random by 1.09 points |
| Random partition relaxation, 2020 | A share of weights held at their quantized values while the rest train with ordinary gradients; the share rises to all | The frozen set is random and redrawn each epoch; it starts at 90% frozen. Results were about equal for 75% to 92.5% frozen and worse outside | CNNs on ImageNet, from pretrained | ResNet-18 at 1 bit: 64.62% against 69.76%. ResNet-50: 65.14% against 76.15% |
| MagR, 2024 | A penalty on the largest magnitude per group of weights, subject to keeping each layer's output; groups of 128 among its settings | One layer at a time, one fixed small strength, a preparation for rounding at 2 to 4 bits; never driven to saturation | 7B to 70B | Section 2F |
| Cadzow 1971, democratic representations, the exact variant of stochastic path following | The end point for a single linear layer: the minimum-maximum equivalent row | A solved problem for one row; no training, no network | Signals; CNN layers | Section 2B |
| BinaryConnect, 2015 | Real weights clipped to a box after every update | The box is fixed; the forward pass uses the sign of every weight through an estimator | CNNs | |
| CEWT, 2026 | A hard projection of each weight tensor after every optimizer step | The target is a Gaussian histogram, not a cap; fixed, not tightened; from scratch; the estimator stays | 95M to 610M language models, 1 and 2 bits | At 1 bit, 610M: perplexity 25.89 to 24.49 |
| Group weight transformations, 2021 | Exact gradients, no estimator, weights squeezed toward plus and minus one on a schedule | A smooth squeeze of each filter's positive and negative sets toward their means; from scratch | CNNs on CIFAR | ResNet-18, CIFAR-10: 5.63% error against 5.52% |
| BinaryRelax, ProxQuant, 2018 | A pull toward the quantized set whose strength rises during training | A penalty with wells at the quantized values, not a bound; a hard phase at the end | CNNs | ProxQuant, every layer binary, CIFAR-10 ResNet-18: 90.76% against 94.84% (as reported by the mirror-descent-view paper) |
| Infinity-norm regression at growing strength, Caltech | Every coordinate driven to plus or minus one value | Linear model, a penalty, from scratch | Linear | Section 2B |
| Quantized-endpoint descent, 2026 | No estimator, no latent weights | Samples moves between codes; scales fixed; not a bound | Qwen2.5-0.5B, Llama-3.2 3B | At three levels on the 3B model both it and the baseline are near chance |

Judgment.

- Published: converting the largest weights first while the others compensate with exact gradients; a per-group penalty on the maximum for language model weights; the single-layer end point; clipping to a box; projecting after every step.
- Not found: a cap per group that descends on a schedule and serves as that group's scale; run end to end under distillation; on a language model; with membership of the saturated set left free to change as the cap moves.
- Searches run: the citations of the mirror-descent-view paper and of quantized-endpoint descent; open searches for projected or box-constrained binarization with a shrinking bound, for clipping schedules without an estimator, and for annealed constraints in quantization training; MagR and its citing work; the Caltech group's papers. A search of this kind cannot show absence.
- Two published results bear on whether it works. Random partition relaxation did best with at least three quarters of the weights already quantized from the start, which is the opposite of a cage that begins mostly free. INQ's loss grows as levels fall and it reports nothing at two levels. Both are on CNNs without distillation.

### 4D. Capacity

**Every measurement or bound found.**

| Source | Weights | What is stored | Per weight |
|---|---|---|---|
| Morris and others | 16-bit and 32-bit, GPT-2 style, 80 thousand to 7 million weights, from scratch | Random token strings | 3.51 bits (16-bit), 3.83 (32-bit); rows from 2.9 to 4.2 |
| Allen-Zhu, Li | 16-bit, 1 million to 500 million | Synthetic facts, 1,000 exposures | 2 bits |
| Same | Same | Same, 100 exposures | 1 bit |
| Same | Rounded to 8 bits after training | Same | No loss |
| Same | Rounded to 4 bits after training | Same | 0.7 bits |
| "Linger and Lose", 27M model at full load | 16-bit | Synthetic facts | 1.720 |
| Same | 8-bit, trained | | 1.593 |
| Same | 4-bit, trained | | 0.999 |
| Same | 3-bit, trained | | 0.551 |
| Same | Three levels, trained, cosine schedule | | 0.155 |
| Same | Three levels, trained, held rate then short drop | | 0.412 |
| Same | Three levels or 3 bits by rounding after training | | 0.000 |
| Binary perceptron | Two levels, one neuron, random patterns | Patterns, one bit each | At most 0.847, conjectured 0.833 |
| Spherical perceptron | Real, one neuron | Same | 2 |

- Share of the 16-bit model's stored facts kept by the three-level model, by the paper's main estimator: 0.36, 0.24, 0.09 and 0.06 at 2.5M, 10M, 25M and 50M weights under a cosine schedule (with a floor applied per attribute the last two are 0.13 and 0.11; a second estimator of the Morris kind gives 0.20 and 0.19 at 10M and 25M and does not register the late collapse; one of three 16-bit runs at 50M also crashed); 0.24 to 0.26 at every size under the better schedule; 0.49 and 0.78 at 25M and 50M when the data asks for less per weight.
- Fine-tuning a trained 16-bit model into three levels destroyed about 90% of what it knew within 25 passes and ended where training from scratch ends. A model first adapted to 4 bits did better.
- Doubling numeric precision from 16 to 32 bits adds 9% (Morris). Most stored bits are not used for storage.
- Models with no MLP store as much at 1,000 exposures and 1.5 times less at 100. The gated MLP that Qwen uses stores about 1.3 times less than a plain one at 100 exposures (Allen-Zhu, Li).
- No source measures a transformer with two-level weights. No source uses distillation. The largest model in any of them is 500 million weights, and the three-level ones stop at 50 million.

**What it says about 1.72 billion weights at 1.125 bits.**

- Ratios, binary or ternary against real: one neuron in theory 0.42; three levels measured 0.25 at full load, 0.49 to 0.78 at light load. The released 1-bit 1.7B keeps (43.2 minus 25) over (66.8 minus 25), 44%, of its teacher's MMLU-Redux score above chance, and scores below chance on GPQA. All of these sit in one range.
- The measured loss depends on load: how much the data asks each weight to hold. How loaded Qwen3-1.7B is, nobody has measured. Real pretraining shows most facts few times, and at 100 exposures a 16-bit model holds half of what it holds at 1,000, so the teacher is probably well under its ceiling. That is the favorable case.
- The pattern across PrismML's own sizes fits a load account: retention is 70% at 1.7B and 89.5% at 27B.
- For the 99% goal at this size: every measured low-bit retention below 8 bits is under 1, and at light load three levels still lose a quarter to a half. Nothing measured shows two levels holding 99% of what an equal-sized 16-bit model knows. The goal needs the teacher to be far under-loaded on what the ruler tests, or a student with more weights than its teacher.
- The knowledge benchmarks are where capacity binds. Mathematics, code and tool calling are procedures, and no capacity measure here speaks to them.

**The smallest experiment that would measure two-level weights.** A design, not a request to run it.

- Models: GPT-2 style at 2.5 million and 10 million weights on the synthetic-biography data, at the full and light loads of "Linger and Lose".
- Arms: 16 bits; three levels in groups of 64, to reproduce that paper's 0.36 and 0.24 as a check on the harness; one sign with one scale per 128, trained from scratch; the same distilled from the 16-bit model of the same size; the same with the output matrix tied to the embedding and with it separate.
- Schedule: held rate with a short final drop, and the output matrix at a tenth of the rate, since without those the measurement records the collapse and not the capacity.
- Output: stored bits per weight and the share of the 16-bit model's, per arm.
- It answers two things no source does: what two levels hold, and whether a distilled student holds more of its teacher's facts than one trained on the data.

### 4E. Unknown

- Whether damage in a trained 1-bit model adds up across blocks. No trial measures it.
- How loaded the teacher is. The recall probe added to S4 in batch 5 measures the outcome; nothing measures the load itself.
- Whether a public sparse autoencoder exists for Qwen3-1.7B. Not searched in this batch.

## 5. Across the three items

- Conversion without training fails at small sizes in every source that tries it, above 1 bit: near chance at 1.58 bits on 1B to 3B models with the best rounding, rotation and magnitude reduction; near chance at 2 bits on our parent; zero stored facts at three levels. The one conversion-only result with usable scores is at 4B, three levels, with a row offset and a second plane. A formula of our own has training in it.
- What the training loss should contain is clearer than what the optimizer should be: a final-hidden-state term has support from two sources at small budgets.
- The schedule and the output matrix matter more than the estimator. The capacity paper's collapse sits in the output matrix and is set off by the learning rate; this project's format converts that matrix too.
- Three ideas this project came to on its own are the same object seen from three sides: the equivalent row at its group maxima, the rigid cage, and MagR's penalty. MagR is the published one, and it stops well short of saturation.
- Weak signals are lost first in every measurement that separates them: rare facts, weak features, facts shown few times.

## 6. Probabilities

Judgments.

| Subject | Before | After | Why |
|---|---|---|---|
| A conversion of our own from the full-precision parent, with end-to-end training this project can afford, reaches the released model's 70.2% | 12% | 12% | The batch says what to put in the loss and the schedule and gives no cheaper route. Published budgets for a rebuild are far above ours |
| The same by a published conversion-only route | Under 5% | Under 3% | Near chance at 2 bits on our parent with the best such route |
| The large-power mirror step is the missing piece of a conversion of our own | 15% to 20% | 8% | It stays at its start; a different force is needed first. Open only as a from-scratch method |
| The mirror step helps training from the released 1-bit model | 25% | 5% | From equal magnitudes it is an ordinary step |
| The shrinking cage as a whole is unpublished | Not held | 65% | Section 4C. Every part is published |
| The shrinking cage beats straight-through training at equal tokens on a small language model | Not held | 15% | For: exact gradients and largest-first conversion work on CNNs. Against: the best published partial-freezing result wants most weights quantized from the start; nothing at two levels; compensation by free weights has to be repaid when they convert |
| A final-hidden-state term improves any end-to-end training we run, at equal tokens | Not held | 60% | Two sources at small budgets, none at ours |
| 99% retention, strict format, 1.7B | 5% | 4% | Section 4D |
| Sign and scale training from the released model reaches a step | 72% | 72% | Nothing here bears on it beyond settings already taken in batch 2 |
| Scale-only training reaches a step | 55% | 55% | Same |

## 7. Asks of the registers

- Plan: C26, C27, C43, C38, C41, C52, C47 done. C46 done for the search, with the design in section 4D. New rows: the two-level capacity measurement as a designed, unapproved experiment (C124); one reading row (C125) for LittleBit-2, the TWLA method behind the Qwen3-4B report, the second half of the knowledge-capacity paper, and BinaryRelax and ProxQuant in full. Sources S119 to S134 added. The odds of the 99% goal move from 5% to 4%.
- Ideas: I5 lowered, with the reason. A note on the cage hypothesis: its nearest prior work and the two results that bear on it.
- S4 specification: the exchange curve is cumulative and its steps are not summed; a line on what not to trust.
- Trials: the sign-change budget of the factorization code as one form for the budget in M3; the final-state term for M3 and for any conversion of our own.
- Ranked work: research row 9 done.
- Queue: batch 6 done; the reading rows.

## 8. Sources

- https://arxiv.org/abs/1906.03830
- https://arxiv.org/abs/2202.10788
- https://arxiv.org/abs/2510.16250
- https://arxiv.org/abs/2602.18997
- https://arxiv.org/abs/1910.08237 Code https://github.com/kartikgupta-at-anu/md-bnn
- https://arxiv.org/abs/1401.3420
- https://arxiv.org/abs/2010.15979 Code https://github.com/elybrand/quantized_neural_networks
- https://arxiv.org/abs/2201.11113
- https://arxiv.org/abs/2309.10975
- https://arxiv.org/abs/2505.11695
- https://arxiv.org/abs/2508.04853
- https://arxiv.org/abs/2406.00800 Code https://github.com/AozhongZhang/MagR
- https://arxiv.org/abs/2402.10474
- https://arxiv.org/abs/2311.02270
- https://arxiv.org/abs/2404.09737
- https://arxiv.org/abs/2607.14630
- https://arxiv.org/abs/2505.11076 Code https://github.com/usamec/double_binary
- https://arxiv.org/abs/2609.01962
- https://arxiv.org/abs/2609.01587
- https://arxiv.org/abs/2606.03002
- https://arxiv.org/abs/2609.32659 Code https://github.com/1733116199/cewt
- https://arxiv.org/abs/2505.24832
- https://arxiv.org/abs/2401.15092
- https://arxiv.org/abs/2609.32902
- https://arxiv.org/abs/2404.05405
- https://arxiv.org/abs/1702.03044 Code https://github.com/Zhouaojun/Incremental-Network-Quantization
- https://arxiv.org/abs/2001.01091
- https://arxiv.org/abs/2107.01400
- https://arxiv.org/abs/2609.21834
- https://arxiv.org/abs/1801.06313
- https://arxiv.org/abs/1810.00861
- PrismML's launch coverage: https://www.hpcwire.com/aiwire/2026/04/06/prismml-emerges-from-stealth-with-1-bit-llm-family/

## 9. Not read

- Any figure in any paper. The mirror serves text.
- The two compression notebooks of the factorization code.
- The second half of the knowledge-capacity paper (its appendix), and the last 500 characters of the CEWT paper.
- BinaryRelax and ProxQuant beyond their abstracts.
- LittleBit-2; the TWLA paper (arXiv 2606.13054) behind the Qwen3-4B report; a 2026 survey of transforms for quantization (arXiv 2608.25188).
- The code of the mirror-descent-view paper, of the greedy rounding papers, of MagR and of CEWT. Their addresses are in section 8.
- The Caltech application was not re-read; it was read in full under checklist row C25.
