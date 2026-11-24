# 1 Bit Summit | Independent research review, Part 3

November 25, 2026 | Research batch following Batch 5

## 0. Brief corrections, scope and evidence standard

Three parts of the brief require qualification before proceeding.

1. A decreasing upper bound on the absolute value of a weight is not a constraint that forces its absolute value to equal the bound. The proposed shrinking cage therefore needs an explicit endpoint mechanism. Likewise, a large-power mirror potential promotes equal magnitudes under particular conditions, not automatically for every coordinate.
2. Two binary factors can encode a matrix economically without the represented matrix itself being binary. Equal storage does not mean equal deployed representation, arithmetic or hypothesis class. We must not mistake these results for a solution to our codec.
3. Information retained from independent random training data, factual recall, and average benchmark retention are three different quantities. None can be substituted for another. A newly located 2026 study directly measures factual capacity in ternary transformers; its evidence belongs in this batch even though it is not in the starting list.

**Fixed target.** Qwen3-1.7B, followed by LFM2. For every full group of 128 weights, store 128 signs and a single FP16 scale. No separately stored correction, rotation, outlier matrix, second binary factor or higher-precision embedding/head. Ordinary non-matrix parameters, padding, alignment and weight tying must be reported separately. A matrix written as `s_g b_g` has rate 144/128 = 1.125 bits per weight, excluding explicitly identified metadata. The 1.72B count is the brief's rounded reference, not an independently counted checkpoint.

**Scoreboard.** From the supplied [PrismML whitepaper reference](https://github.com/PrismML-Eng/Bonsai-demo), the sums are 582.4 teacher and 408.8 student. Their quotient is 70.1923%. At this teacher score, five retention percentage points are 29.12 summed task points; 99% requires mean 57.6576. The supplied score is an outside reference, not our own measured conversion. I have not independently rerun its harness. When the new baseline is measured, use its own unrounded denominator.

**Reading limitations.** This is an independent documentary and mathematical investigation, not an executed experiment. Primary arXiv HTML, indexed full-text passages, conference landing pages, a patent text mirror, author repositories and related-paper search were used. Direct container retrieval failed at DNS resolution; browser retrieval of selected raw code also failed. Bounded HTML excerpts expose many equations and tables but do not certify a continuous read of every proof, image, appendix and code file. I therefore label the named papers **read in part**, even where substantial primary material was available. No paper is labeled read in full on the strength of search snippets. Figures not numerically transcribed, missing appendices, and unavailable code runs remain open tasks. No access forms, credentials, paid access, language-model training or model evaluation were used. I ran only arithmetic checks of derived rates and retention. This report does not fulfill the requested exhaustive full-file/code audit; it does provide a substantial primary-source-grounded analysis and distinguishes the gaps. Source-specific limitations below are controlling.

**Probability convention.** Event P is that we produce a reproducible conversion from the actual FP parent that reaches at least 70.2% retention on the matched ten-task suite, with the strict codec and both embedding/head included. For judgment comparisons, I assume a serious conversion campaign with up to roughly one billion total processed student token positions across a bounded series of trials, with teacher-target generation counted separately and no unrestricted pretraining. The brief did not specify a compute budget; this is an explicit conditioning assumption, not a project decision. The before numbers are reconstructed subjective priors before considering this batch's evidence, not timestamped prior predictions. The after numbers are not statistical estimates. Per-item updates concern pursuing that route with otherwise competent shared infrastructure; events overlap and must not be added.

## 1. Mirror descent, equal-magnitude geometry and sign selection

### 1A. Source and access ledger

| Source | Reading label and route | Scope inspected; unresolved |
|---|---|---|
| Hassibi, Lale, Naucler, [US20260220467A1](https://patents.justia.com/patent/20260220467), [WO2026161822A1](https://patents.google.com/patent/WO2026161822A1/en) | Read in part, US publication via Justia patent text | Compression/SMD discussion, equations 6, 9-10, 21-28, 32, regularizer discussion. WO counterpart not independently read. Complete claims, all figures, prosecution history and implementation not audited. |
| Azizan, Lale, Hassibi, [1906.03830](https://arxiv.org/html/1906.03830) | Read in part, primary arXiv HTML | Sections on SMD, nonlinear assumptions, convergence, experimental norm comparisons; not all proofs/appendices. |
| Azizan, Lale, Hassibi, [2202.10788](https://arxiv.org/html/2202.10788) | Read in part, primary arXiv HTML | RMD construction, convergence theorem, experimental section; complete proof and code missing. |
| Akhtiamov, Ghane, Hassibi, [2510.16250](https://arxiv.org/html/2510.16250) | Read in part, primary HTML v1 | Random-feature equivalence, experimental settings, discussion and portions of appendices B/C. Full technical proof, figure-point data and kernel code not audited. |
| [Implicit Bias and Convergence of Matrix Stochastic Mirror Descent, 2602.18997](https://arxiv.org/html/2602.18997) | Read in part, primary HTML v2 | Linear measurement model, convergence/rate statements, matrix-completion experiments; not complete proofs. |
| Ajanthan et al., [1910.08237](https://arxiv.org/html/1910.08237), [AISTATS paper](https://proceedings.mlr.press/v130/ajanthan21a.html) | Read in part, primary HTML and conference record | Mirror-map construction, optimization, main binary results and comparisons. [md-bnn code](https://github.com/kartikgupta-at-anu/md-bnn) located from index; not executed or audited line by line. |
| Studer et al., [1401.3420](https://arxiv.org/html/1401.3420) | Read in part, primary HTML | Democratic representation definitions, extremal-coordinate lemmas, norm bounds and uncertainty principle. All proof details and code not read. |
| Lybrand, Saab, [2010.15979](https://arxiv.org/html/2010.15979) | Read in part, primary HTML v2 | Greedy algorithm, main probabilistic results and selected experimental descriptions. [Code](https://github.com/elybrand/quantized_neural_networks) located, not executed. |
| Zhang, Zhou, Saab, [2201.11113](https://arxiv.org/abs/2201.11113) | Read in part, arXiv abstract/index | Follow-up GPFQ theory; no complete proof or code audit. |
| [SDQ-LLM, 2510.03275](https://arxiv.org/html/2510.03275) | Read in part, primary HTML | Methods and main experimental/ablation tables; [code repository](https://github.com/Dreamlittlecat/LLM-Quant-Factory) not audited. |
| [Kashin post-training quantization, UAI 2024](https://proceedings.mlr.press/v244/merkulov24a.html); [structured Kashin, 2609.11687](https://arxiv.org/html/2609.11687) | Read in part, conference abstract and selected primary HTML | Representation and model-level results; not exhaustive. |

### 1B. What the patent actually offers

The Caltech application is a highly pertinent starting point, but not proof that a distilled 1.7B model can attain a binary shell. Its proposals exploit SMD's preference among multiple feasible parameter solutions. The large-power and infinity-norm constructions are explicit compression-oriented geometry; the application also presents a nonsmooth hybrid geometry. The important step is choosing a geometry in which small maximum magnitude or near-common magnitude becomes attractive, rather than imposing a hard binary forward model at each update. [Patent compression discussion and equations](https://patents.justia.com/patent/20260220467).

**Derivation: mirror descent is not ordinary gradient descent through a soft quantizer.** Let `w` be the weights, `z` the dual variables, and `ψ` a proper convex mirror potential. For differentiable Legendre geometry:

```
z_t = ∇ψ(w_t)
z_(t+1) = z_t - η_t ∇_w L(w_t)
w_(t+1) = ∇ψ*(z_(t+1))
```

Equivalently the update minimizes a linearized loss plus a Bregman proximal distance. Strong convexity guarantees a unique primal minimizer even for some nonsmooth potentials. For those potentials use subgradients and the conjugate, not a fictitious ordinary derivative. The loss is evaluated at the actual continuous weights during training. The dual update uses the gradient with respect to the primal weights. Ordinary differentiation of `L(w(z))` adds the Jacobian of `w(z)` and is a different algorithm.

**Large power.** For the separable group potential `ψ_q(w)=Σ |w_i|^q/q`, q>1, the inverse is `w_i=sign(z_i)|z_i|^(1/(q-1))`. This is a valid strictly convex mirror geometry on its natural domain. For q>2 it is not globally strongly convex near zero. If every dual magnitude is nonzero and bounded independently of q, then increasing q drives the absolute primal coordinates toward 1. At finite q, the ratio of the largest to smallest nonzero primal magnitude is `(max|z|/min|z|)^(1/(q-1))`. For a dual ratio of one million, q=32 leaves a ratio about 1.56; q=128 about 1.115. Neither is exact equality. A coordinate with dual zero is primal zero. If the dual shrinks exponentially in q, the limiting argument can fail. Normalizing each group to a chosen scale is necessary to avoid treating the absolute numerical value 1 as a useful LLM weight magnitude. Annealing q changes the geometry; a fixed-potential theorem does not automatically cover it.

**Rigid cage.** Patent equation 21 onward uses a maximum-norm-based potential with a quadratic term. For a group of length g, consider `ψ(w)=||w||∞ + ε||w||²/2`, ε>0. The quadratic ensures strict/strong convexity. The inverse mirror map is explicit:

```
w(z) = (z - projection_L1_ball(z, radius=1)) / ε
```

This follows from the conjugate of the infinity norm being the indicator of the unit L1 ball and the quadratic proximal identity. If `||z||1≤1`, w=0. Otherwise find α>0 satisfying `Σ max(|z_i|-α,0)=1`, then `w_i=sign(z_i) min(|z_i|,α)/ε`. The inverse is a clipping operation with a threshold determined by the entire dual group. This is a mathematically closer relative of our shrinking cage than conventional weight clipping.

There is an apparent scale omission in the interior branch of the patent's displayed equation 28 as retrieved. The correct interior primal coordinate from the minimization is `z_i/ε`, not `z_i` unless ε=1. At the origin the infinity-norm subgradient has L1 norm at most 1, not necessarily equal to 1. These are derivations, not an accusation that the implementation uses the printed expression. Verify against the original patent PDF before implementing.

Full saturation is possible but conditional. All coordinates are on the common nonzero shell exactly when `0 < α ≤ min_i |z_i|`. In that case `α=(Σ|z_i|-1)/g`. For g=128, the condition can be written `0 < Σ|z_i|-1 ≤128 min|z_i|`. If a dual coordinate lies inside the threshold it remains unsaturated. Keeping the dual variables is important because a saturated primal coordinate does not determine a unique dual coordinate.

**Hybrid potential.** The patent also discusses a group-separable maximum of convex powers such as `max(|w|^(1+ε), β|w|^q)`. For `q>1+ε`, β>0, the nonzero crossover occurs at `a=β^(-1/(q-1-ε))`. A slope jump creates an interval of dual values that all map to the same primal magnitude a. This produces exact magnitude plateaus at finite parameters, unlike a smooth power alone. The interval need not capture every dual coordinate. Convexity is maintained because both terms are convex; verify strictness and domain before choosing the inverse. A squared penalty `( |w|-a )²` is not a globally convex mirror potential: its two minima and interior maximum are the problem. It may instead be a nonconvex regularizer or proximal target.

**What is not established.** No primary evidence retrieved from the patent establishes strict g128 full-model language-model retention, a matched token budget against STE, or convergence to a globally optimal binary neural network. The WO counterpart and inventor code or post-filing experimental announcements were not exhaustively recovered. Search routes included the publication numbers, inventor combinations with mirror descent, binary quantization and language model, and the related Caltech papers below. No matching public g128 transformer result was verified, not a claim that none exists.

### 1C. What the SMD theorems imply and where they stop

[Azizan et al. 1906.03830](https://arxiv.org/html/1906.03830): For interpolating linear models, mirror geometry selects the feasible parameter nearest the initialization in Bregman distance. For nonlinear overparameterized models, the convergence/implicit-regularization argument depends on local regularity, existence of interpolants in a suitable neighborhood, repeated data sampling, a sufficiently small step, and conditions ensuring descent of the local Bregman terms. The nonlinear guarantee is proximity to the Bregman-selected solution, not a global binary optimum. Their MNIST/CIFAR norm experiments are continuous-parameter training comparisons, not 1-bit codec demonstrations.

The important dependence is on initialization. Minimizing `Dψ(w,w0)` is not generally equivalent to minimizing `ψ(w)`. The anchor term `-<∇ψ(w0),w>` can preserve an existing high-precision teacher geometry. A zero-initialized model can select a minimum-potential interpolant, but throwing away the pretrained parent defeats the purpose of our conversion. The core transfer gap is therefore not simply finding a good potential; it is retaining teacher information while changing the implicit preference.

[Explicit Regularization via RMD](https://arxiv.org/html/2202.10788): introduces auxiliary variables for example losses, transforming a regularized objective into an augmented interpolation problem. The theorem concerns local convergence in the enlarged space under regularity and stepsize conditions, with the regularizer/loss tradeoff represented in its metric. It is not a universal guarantee of solving discrete compression. CIFAR-10/ResNet-18 experiments, including corrupted labels, concern explicit regularization rather than strict bit weights. A regularization term changes the objective; its effect must be distinguished from the implicit bias of SMD itself.

[Matrix SMD, 2602.18997](https://arxiv.org/html/2602.18997): treats linear matrix measurements, convex loss and strong convexity of the mirror map with additional operator conditions. The Bregman projection result and linear-rate analysis rely on those conditions. Matrix completion is the demonstrated regime. A Schatten norm controlling singular values is not a constraint on the magnitudes of individual matrix entries. Neither the rate nor the selected solution can be directly imported into a nonlinear transformer with trainable normalization, attention and MLPs.

**Critical counterexample at initialization.** If the student starts at the exact teacher and the loss is only self-distillation KL, its gradient is zero (at exact arithmetic and matching inference conditions). A fixed mirror potential cannot move the weights. Calling an optimizer mirror descent does not resolve this. One needs an actual intervention: a nontrivial feasible-set projection, explicit regularizer, perturbation, or time-dependent geometry with carefully defined state transport. This is a basic preflight test for any proposed conversion formula.

### 1D. Actual mirror-descent binary networks

[Ajanthan et al., main results](https://arxiv.org/html/1910.08237): quantization is expressed using continuous maps toward discrete values, with an inverse map defining a mirror potential. A continuously differentiable strictly monotonic scalar mapping onto an open interval admits a convex potential from the integral of its inverse. Vector maps need an integrable inverse field, or an appropriate convex conjugate, not just a componentwise assertion. The convex convergence analysis and annealed-discreteness result carry assumptions; they do not prove successful deep nonconvex optimization.

For binary values in (-1,1), a useful example is `ψ'(w)=atanh(w)`, giving `w=tanh(z)`. A softmax map on a probability simplex similarly comes from entropy, with a dual gauge redundancy. The simplex distribution may describe the two signs but a soft expectation can remain interior. Finite-temperature tanh is not an exact sign; increasing inverse temperature tends to a sign for nonzero dual, but training stability, scale and the zero-dual case matter.

Main binary image-classification results, accuracy %, as tabulated in the paper (these are not LLM benchmark results):

| Method | CIFAR10 VGG16 | CIFAR10 Res18 | CIFAR100 VGG16 | CIFAR100 Res18 | TinyImageNet Res18 |
|---|---:|---:|---:|---:|---:|
| Float | 93.33 | 94.84 | 71.50 | 76.31 | 58.35 |
| BinaryConnect | 89.04 | 91.64 | 59.13 | 72.14 | 49.65 |
| ProxQuant | 85.41 | 90.76 | 39.61 | 65.13 | 44.32 |
| ProxQuant* | 90.11 | 92.32 | 55.10 | 68.35 | 49.97 |
| PMF | 90.51 | 92.73 | 61.52 | 71.85 | 51.00 |
| PMF* | 91.40 | 93.24 | 64.71 | 71.56 | 51.52 |
| GD tanh | 91.47 | 93.27 | 60.67 | 71.46 | 51.43 |
| MD softmax | 90.47 | 91.28 | 56.25 | 68.49 | 46.52 |
| MD tanh | 91.64 | 92.97 | 61.31 | 72.13 | 54.62 |
| Stable MD softmax | 91.30 | 93.28 | 63.97 | 72.18 | 51.81 |
| Stable MD tanh | 91.53 | 93.18 | 61.69 | 72.18 | 52.32 |

MobileNetV2 all-parameter binary experiment: full precision 93.67/73.97 (CIFAR10/100), BinaryConnect 86.84/65.04, stable MD softmax 89.71/66.40, stable MD tanh 89.99/66.63. ImageNet ResNet18 top-1/top-5 FP 70.61/89.40; reported MD variants 56.67/79.66 (scratch, broader binarization except BN), 65.92/86.29 (scratch, partial), 66.78/87.01 (standard setting). Do not compare protocols as if identical. In particular, first/last-layer exemptions and normalization are important. [Paper experimental section and tables](https://arxiv.org/html/1910.08237).

These results demonstrate useful optimizer competition at binary precision. They do not establish that a 1.7B language-model conversion with a tied vocabulary interface and strict group scales will reproduce the advantage. Dataset budgets and all paper-specific training schedules were not independently transcribed. Source code was located but not run.

### 1E. One-bit random features: an equivalence, not a conversion theorem

[Akhtiamov et al.](https://arxiv.org/html/2510.16250) compare trained readouts over frozen random features built using Gaussian versus Rademacher random weights. Under wide random-feature assumptions and regularity of activation/loss/mirror geometry, relevant asymptotic test losses agree. This supports the idea that random feature distributions can retain useful capacity with binary hidden weights, not that sign-rounding a learned transformer preserves its knowledge. The final readout is itself fitted in continuous precision.

Reported settings include synthetic n=1000, input width 8192 and feature width 4096, tanh features with different readout geometries, 5000 test samples; MNIST experiments with width 512, depths 1 through 5, small per-class training subsets, 20 trials and width sweeps. A kernel demonstration reports roughly 4x acceleration in a particular batch-one setting on an RTX 2060 with a different group layout. No exact point-by-point accuracy gap was recovered from the figures, and no language-model experiment was verified. A learned attention head is not an independent Rademacher random-feature matrix. In particular, the last-layer caveat makes this paper more relevant to our interface risk than to an all-matrix proof.

### 1F. Democratic and Kashin representations: how many coordinates can be on the wall?

[Studer et al.](https://arxiv.org/html/1401.3420) study redundant representations solving `D x = y` with minimized maximum coefficient magnitude. For a full-rank M-by-N frame, N>M, extremal optimal solutions can have at least N-M+1 coordinates at maximum magnitude under the appropriate assumptions (full-spark conditions strengthen the statement). Their bounds relate democracy to frame constants and an uncertainty principle; they do not say all coordinates are always at the maximum. Kashin representations use redundancy to distribute signal energy rather than simply clipping an arbitrary pretrained vector.

Translate this to a real calibration problem. For one row/group, let `X` be T-by-128 input activations, rank r, and target y in its column space. We seek `min ||w||∞` subject to `Xw=y`. A real LP optimum can be selected with at least 129-r saturated coordinates in the nondegenerate full-rank setting (the original literature includes complex frames; our real LP argument follows from counting free variables at an extreme point). Consequently:

| Effective rank r | Guaranteed extremal saturation count under the stated real LP conditions | Remaining potentially free |
|---:|---:|---:|
| 1 | 128 | 0 |
| 8 | 121 | 7 |
| 32 | 97 | 31 |
| 64 | 65 | 63 |
| 128 | 1 | 127 |

This is a structural insight, not a measured property of Qwen. Exact binary at a shared scale corresponds to the finite collection of rays `{s X b : b∈{-1,+1}^128, s≥0}`. For rank r>1, almost every continuous y in the r-dimensional range lies off those rays. No method can guarantee exact reconstruction of arbitrary y with this alphabet. Redundant calibration inputs can reduce the relevant dimension, but calibration rank can be large despite a small sample; approximate numerical rank is not exact rank. Real distribution coverage matters.

If the extremal solution has at most r-1 interior weights and the cap is s, rounding those weights to nearest signs produces `||δ||₂≤s sqrt(r-1)` and `||Xδ||₂≤||X||₂ s sqrt(r-1)`. This crude worst-case bound ignores favorable cancellation. An activation covariance bound below is more informative. It also explains why selecting signs jointly across groups can outperform separate group minimization: each output is the sum of group contributions.

[UAI 2024 Kashin](https://proceedings.mlr.press/v244/merkulov24a.html) and [2026 structured Kashin](https://arxiv.org/html/2609.11687) bring redundant representations to neural compression using frames or structured transforms. The latter includes low-bit Pythia/OPT experiments in the 1.3B-1.4B range, but the retrieved examples were 4-bit, not strict binary. Overcomplete coefficients and a nontrivial decoder are deployed side information/arithmetic unless folded into the original matrices and requantized. Folding is not guaranteed to preserve the representation. These are meaningful precedents for reducing peak-to-average ratio but not demonstrations of our format.

### 1G. Greedy path following and sigma-delta

[Lybrand and Saab](https://arxiv.org/html/2010.15979) quantize coefficients sequentially while maintaining a residual in calibration output space. With columns x_j, the recurrence is:

```
u_0 = 0
q_j = argmin_(q in alphabet) ||u_(j-1)+(w_j-q)x_j||₂²
u_j = u_(j-1)+(w_j-q_j)x_j
```

Equivalently, choose the quantization level nearest `w_j + <x_j,u_(j-1)>/||x_j||²` when x_j is nonzero. A binary alphabet `{-s,+s}` is algorithmically valid. However, the original probabilistic theorem is for its specified ternary quantizer and assumptions, including Gaussian calibration columns, bounded coefficient distribution independent of columns and distance from quantizer levels. In that regime the relative error has the approximate redundancy dependence `C sqrt(m) log(N)/||w||₂`, where m is sample dimension and N width, with constants depending on assumptions. The result must not be restated as a proven binary g128 bound. Its generalization result relies on controlled test inputs, not arbitrary distribution shift. [Follow-up GPFQ](https://arxiv.org/abs/2201.11113) expands the analysis, but I did not recover every hypothesis and proof.

Original reported neural experiments include fully connected MNIST networks with widths 500 and 300, using 25k calibration examples from the 60k training set, and CNN comparisons. These are primarily ternary/multilevel evidence; complete image-level numerical results were not recovered. No exact 1-bit LLM result can be claimed from this source.

The especially relevant follow-up is **[SDQ-LLM](https://arxiv.org/html/2510.03275)**. It explicitly brings noise shaping and overcomplete representations to transformer PTQ. Hadamard preprocessing and oversampled FFT/resampling mechanisms reduce quantization residuals in selected directions. Main results at nominal 1.58-bit ternary precision with oversampling are as follows. This is *not* a verified deployed 1.125-bit codec; the actual number of retained coefficients and transforms must be counted.

| Model | FP16 Wiki PPL | SDQ reported PPL |
|---|---:|---:|
| OPT 1.3B | 14.62 | 38.24 |
| OPT 2.7B | 12.47 | 20.30 |
| OPT 6.7B | 10.86 | 14.87 |
| OPT 13B | 10.12 | 11.60 |
| Llama2 7B | 5.47 | 14.06 |
| Llama2 13B | 4.88 | 6.95 |
| Llama3.2 1B | 9.75 | 298.31 |
| Llama3.2 3B | 7.81 | 31.65 |
| Llama3 8B | 6.13 | 17.02 |

The small Llama result is a serious negative transfer signal. The 8B ablation reports 2434.87 without the relevant transforms, 20.13 with Hadamard, 2751.13 for the other isolated intervention and 17.02 for the combined mechanism; verify the table labels before implementation. The FP baseline in that ablation differs from the main table. Code and exact storage accounting were not recovered. [Source](https://arxiv.org/html/2510.03275).

### 1H. Equal-magnitude cost: exact derivations for our format

For one group `w∈R^g`, the Euclidean optimum over a common scale and signs is `b=sign(w)` and `s=mean(|w|)`. The minimum squared error is `||w||₂² - ||w||₁²/g`. This is the residual variance of the magnitudes. It does not depend on a training optimizer. For i.i.d. Gaussian weights of large g, the relative residual approaches `1-2/π≈0.36338`. That is 36.34% weight energy, not 36.34% lost task score. Heavy tails often raise this cost. Grouping similar magnitudes can lower it, provided any rearrangement is function-preserving and deploys without a stored permutation.

For finite g, the expected *numerator* for independent Gaussian samples is `(g-1)σ²(1-2/π)`; dividing by expected total energy gives `(1-1/g)(1-2/π)≈0.36054` at g128. This is a ratio of expectations, not the expectation of the per-group ratio. The common scale itself must be rounded to legal FP16; for a fixed sign vector, quantization of the scale adds a quadratic term, potentially worse for very small/subnormal groups.

For activation-aware optimization let `C=E[x xᵀ]` (uncentered second moment). The relevant output MSE is `(w-sb)ᵀ C (w-sb)`. For fixed b and positive denominator, `s*=(bᵀ C w)/(bᵀ C b)`, clipped to the allowed nonnegative range and discretized to the best feasible FP16 value. If C is diagonal and positive, signs of w are optimal at fixed positive s; the scale is the weighted mean of |w|. Off-diagonal correlations change optimal signs and make the problem combinatorial. Exact selection is a binary quadratic problem for fixed scale. There is no reason to prefer Euclidean RTN when C is badly conditioned, but covariance estimated from a narrow corpus can overfit. Near-null directions allow compensation; broad isotropic inputs penalize it.

Increasing group size saves scale overhead but ties together more magnitudes and may worsen local approximation. At fixed alphabet and independent input distribution, redundancy can improve sign-selection cancellation only when input directions are genuinely correlated. No nullspace theorem is a license to assume a 128-weight group is redundant. The relevant rank and error must be measured on both training and held-out activations.

Finally, with a group norm fixed at R and max magnitude capped at c, `R²≤g c²`. At `c=R/sqrt(g)` equality forces every magnitude equal to c. This simple identity is the mathematical endpoint condition the shrinking-box idea lacks. The intersection is not convex, so it cannot be presented as an ordinary convex-mirror convergence theorem.

### 1I. Searches, applicability and probability

Search directions included inventor names/publication numbers, matrix SMD, binary mirror descent tanh, rigid cage, high-power/infinity-norm compression, Kashin/democratic LLM quantization, greedy path following transformer, and sigma-delta language models. The direct LLM sigma-delta and Kashin studies are more relevant than image accuracy alone. I did not find a *verified* successful full-model strict g128 transformer conversion using the specific Caltech potential or these redundant transforms. The literature search is not exhaustive enough to support a universal negative.

To outperform STE distillation at matched tokens, the method must preserve the teacher basin while changing geometry, create more than near-equal magnitudes, and avoid a terminal discrepancy between soft and hard inference. It must also preserve embedding/head capacity and use held-out activations that generalize. Exact gradients of the continuous model remove STE bias only for the continuous objective; they do not guarantee gradients of the discrete deployment problem. A soft model with good loss can still fail on hard signs. Mirror descent's strongest theorem regime (feasible linear interpolation with redundancy) is precisely where our local activation approximations are most plausible, and weakest for jointly changing nonlinear transformer layers and arbitrary full-rank calibration targets.

**P before: 25%; P after: 30%.** The patent's exact plateau geometry and genuine binary image results raise the probability. Lack of direct strict LLM evidence and SDQ's small-model failures limit the update. This is a judgment for the mirror/greedy-centered conversion route, not a five-point trophy.

**Cheapest unresolved work:** obtain complete patent PDF and related claims, reproduce the exact conjugate map algebra in a unit test, obtain all Ajanthan recipes, inspect RF and GPFQ proof assumptions/figures and SDQ deployed packing. Before a model run, check whether the proposed optimizer has a nonzero first update at the teacher, whether its endpoint is exactly representable, and whether a fixed low-dimensional synthetic regression can attain zero output error where the theorem predicts it. No such training or model evaluation was performed here.

## 2. Cross-layer compensation and binary factorization

### 2A. Source and access ledger

| Source | Reading label and route | Scope inspected; unresolved |
|---|---|---|
| Noda, [2607.14630](https://arxiv.org/html/2607.14630) | Read in part, primary arXiv HTML v1 | Method, calibration/training setup, main tables, selected appendix A-C material. Complete appendices, notebooks and reproducibility not independently verified. |
| Boža, Macko, [2505.11076](https://arxiv.org/html/2505.11076), TMLR 2026 | Read in part, primary HTML v4 (February 28) | Factorization, optimization, main tables, throughput and selected appendices. All appendix tables and kernels not audited. [double_binary](https://github.com/usamec/double_binary) repository root opened; selected raw access failed. |
| [BiLLM](https://arxiv.org/abs/2402.04291) | Read in part, abstract/index and related primary comparison | Salient residual binary components. Full code/packing audit missing. |
| [OneBit](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7a7a3f53faafc0161be0fcb57e5fa078-Abstract-Conference.html) | Read in part, conference record/index | SVID/scale-vector construction; complete training recipe not reopened. |
| [ARB-LLM](https://arxiv.org/abs/2410.03129), [code](https://github.com/ZHITENGLI/ARB-LLM) | Read in part, abstract/index | Alternating refinement and salience; no code execution. |
| [PBBQ](https://www.mdpi.com/2079-9292/15/4/819) | Read in part, publisher-indexed text | Reordering and propagated error; full paper/code not inspected. |
| [All for 1-Bit, 2609.06161](https://arxiv.org/html/2609.06161) | Read in part, primary HTML | Nullspace-aware factorization, Shapley allocation, main table; appendix A.4.1 and complete code audit unfinished. |

### 2B. Noda: the first direct small-model compensation evidence in this batch

Noda's comparison uses Qwen2.5-1.5B, about 1.31B weights in 196 linear operators, with FP16 embedding and output interface. Each quantized group contains 128 binary weights and a scale. The reported linear-weight size is about 184.2 MB. This is directly relevant to the body codec but excludes an important part of our target. [Primary method and setup](https://arxiv.org/html/2607.14630).

The method combines differentiable binary-weight optimization, teacher/student cross-layer residual matching and projected feature statistics. In broad terms, it penalizes accumulated error relative to the teacher, not merely each layer's standalone reconstruction. The feature objective compares low-dimensional projected means and covariance/Gram information (projection dimension 64 in the reported setup); the logit objective uses a restricted teacher distribution (top 256, temperature 2). The optimization uses AdamW on latent signs and scales, with the sign temperature sharpened and a late hard-forward surrogate phase. This is not purely exact-gradient, no-rounding training through to deployment.

Reported setup: roughly 130k unique WikiText2 calibration tokens, 1000 steps, batch 8, length 512, i.e. 4.096 million processed token positions with repeated data; seeds 1234, 2025 and 7; sign-latent learning rate 5e-4, scale rate 5e-3, inverse temperature 1 to 16, hard-forward stage in last 20%. INT4 comparison uses 300 steps. A100 runs reported around nine minutes per seed/condition. This is a reported historical experimental duration, not an estimate of our work. Teacher WikiText2 PPL 11.951, OOD C4 16.18 and CNN/DailyMail 14.70. No ten-task benchmark suite reported in the material recovered.

Main binary comparison (PPL ratios to the paper's teacher, smaller is better; global feature error E_GE is a different metric):

| Condition | Ratio | E_GE | Implied Wiki PPL, approximately |
|---|---:|---:|---:|
| A RTN | 2.2e9 | not extracted | 2.63e10 |
| B layer-local | 1.4e3 | not extracted | 16,731 |
| G logit KD | 14.09 ±0.53 | 1.56 ±0.07 | 168.4 |
| C feature statistics | 262 ±47 | 0.29 ±0.09 | 3,131 |
| D accumulated error | 9.56 ±0.15 | 1.41 ±0.12 | 114.3 |
| E combined | 11.50 ±0.20 | 0.48 ±0.24 | 137.4 |

INT4 ratios: A 1.201; B 1.088±.003; C 1.176±.006; D 1.060±.002; E 1.060±.003. This demonstrates that the ordering of objectives depends on precision. At binary, D alone outperforms E on perplexity. At INT4, D and E are effectively tied. C has better feature metric but drastically worse PPL. Neither local nor feature matching alone can substitute for end-task validation.

OOD table, reported ratios:

| Condition | WT2 | C4 | CNN/DM | E_GE WT2 / C4 / CNN/DM |
|---|---:|---:|---:|---|
| G | 13.91 | 73.8 | 54.1 | 1.56 / 1.70 / 2.99 |
| C | 313 | 780 | 484 | .29 / .62 / .42 |
| D | 9.62 | 46.1 | 33.4 | 1.41 / 1.46 / 1.52 |
| E | 11.57 | 62.9 | 44.9 | .26 / .53 / .88 |

The in-domain table entries are not identical to the main comparison; do not silently merge them. D implies OOD perplexities roughly 746 and 491. These are very large absolute penalties. D improves substantially over G, about 32% lower WT PPL ratio in the main table, not a 32-point task-retention gain. [Main and OOD tables](https://arxiv.org/html/2607.14630).

**Independent mathematical assessment.** Let teacher layer F and student layer Q act on h and h+e. Then `e_next = Q(h+e)-F(h) = [Q(h+e)-Q(h)] + [Q(h)-F(h)]`. The second term is local conversion error, the first the transport of already accumulated error. This exact decomposition needs no linearization and shows why downstream layers can cancel upstream error. Its identity does not establish that cancellation is robust out of distribution. If an objective is simply norm of accumulated e_next, it is a version of teacher hidden-state matching, not a proof of a new universal error-compensation law. Analyze both aligned residuals and their interaction, particularly at residual joins.

Projected feature moments can coincide while tokenwise outputs differ; a low-dimensional projection may miss the most important error direction. Covariance estimates from a finite sample are noisy and biased by dimension; the projection is an auxiliary constraint, not an information-preserving sufficient statistic. The C result is unusually clear empirical evidence of that distinction.

Two implementation caveats from the equations: a tanh initialization obtained from a clipped ratio `w/s` cannot exactly reproduce weights outside the scale interval, and ordinary AdamW on z through a tanh map does not equal the mirror update using primal gradients. Treat the paper's differentiable parameterization as such unless an explicit custom-gradient/dual update is verified in code.

**True rate.** If f is the fraction of unique model weights in quantized matrices, then `R=1.125 f +16(1-f)` before additional metadata. With 1.31B/1.54B, the approximate full-parameter rate is 3.35 bits per weight; 1.31/1.50 gives 3.01. The exact count depends on tied parameters and model revision. [Qwen2.5-1.5B model card](https://huggingface.co/Qwen/Qwen2.5-1.5B). The 184.2 MB body figure is compatible with 1.31B*1.125/8≈184.22 MB, not with an all-matrix 184 MB model. For our codec, the trained body is a possible starting point and the compensation objective is directly transplantable, but the interface must also be binarized and jointly repaired. No public executable notebook/code audit or successful run established. The full-model result is likely worse before additional repair; magnitude unmeasured.

### 2C. Double binary factorization: representation and exact cost

[Boža and Macko](https://arxiv.org/html/2505.11076) propose representing a dense n-by-m matrix using binary n-by-k and k-by-m factors with scaling vectors:

```
W_hat = diag(a) A diag(c) B diag(b)
A ∈ {-1,+1}^(n×k), B ∈ {-1,+1}^(k×m)
```

The optimization fits weighted reconstruction, factorizes the matrix and alternates refinements, with sign and scale optimization and an optional PV fine-tuning stage. Input activation statistics and output-gradient importance participate in weighting. The paper uses a small RedPajama calibration sample (256 sequences) and reports RTX 4090 compression and multi-A100 fine-tuning configurations; exact token lengths and all appendix settings were not recovered. Reported historical compute includes 6-8 hours for compression and about 24 hours on four A100s for fine-tuning, not estimates for this project. [Method and compute discussion](https://arxiv.org/html/2505.11076).

If all three scaling vectors are FP16, the exact matrix rate (before padding, alignment and other metadata) is

`[k(n+m)+16(n+m+k)]/(nm)`.

If the vectors are FP32, replace 16 by 32. A nominal rate b that sets `k≈b nm/(n+m)` counts only signs and understates total storage. To hit our rate exactly or lower with FP16 scales, use `k≤floor([1.125 nm-16(n+m)]/[n+m+16])`. Examples from arithmetic only:

| Square matrix dimension | Maximum k | True matrix rate | Rank upper bound relative to n |
|---:|---:|---:|---:|
| 128 | 52 | 1.11328 | 40.6% |
| 1024 | 555 | 1.12370 | 54.2% |
| 2048 | 1131 | 1.12443 | 55.2% |
| 4096 | 2283 | 1.12474 | 55.7% |

Rank(W_hat)≤k. A full-size strict binary sign matrix can have full rank. Conversely, the factorization produces many different magnitudes per group, which a single-scale dense binary matrix cannot express. These are different model classes. A general factorized matrix cannot be converted exactly into our format. Collapsing the factors then performing g128 sign-scale fitting introduces another error. It may still be useful as an offline continuous teacher/initialization, but the original parent is the clean control. No factor or scale vector may remain deployed as an extra side channel.

At inference, the two factor operations require a scaled input, intermediate of dimension k and scaled output, with an extra central scale. The paper's kernels can exploit binary addition and memory bandwidth; this does not turn them into a single standard packed g128 matrix multiplication. The exact speed on Apple hardware is not established. For whole-model rates, the precision and unique counts of all nonfactorized weights (especially tied or untied embeddings/head) must be added; I did not recover a sufficient manifest to certify them. The paper reports a small scale-overhead example consistent with 16-bit vectors, but independent byte-level verification remains necessary.

### 2D. DBF results, matched to each paper baseline

No ≤3B model result was verified in this paper. The following main table values are for larger models; do not extrapolate linearly. Task order ArcChallenge, ArcEasy, PIQA, WinoGrande. PPL lower is better. Rates are the paper's nominal settings, not our fully counted model rate.

| Llama2-7B | PPL | ArcC | ArcE | PIQA | Wino | Mean |
|---|---:|---:|---:|---:|---:|---:|
| Full | 5.12 | 43.43 | 76.34 | 78.07 | 69.06 | 66.73 |
| 2.3 DBF | 5.87 | 38.39 | 73.35 | 76.49 | 66.85 | 63.77 |
| 2.3 +PV | 5.85 | 39.33 | 73.65 | 76.55 | 67.08 | 64.15 |
| 2 DBF | 6.14 | 37.03 | 72.05 | 76.22 | 65.82 | 62.78 |
| 2 +PV | 6.09 | 36.94 | 71.88 | 76.16 | 66.06 | 62.76 |
| 1.5 DBF | 7.16 | 35.06 | 66.32 | 73.28 | 64.40 | 59.77 |
| 1.5 +PV | 7.01 | 35.58 | 67.12 | 73.72 | 63.69 | 60.03 |
| 1 DBF | 9.57 | 26.45 | 55.30 | 67.41 | 58.87 | 52.01 |
| 1 +PV | 8.76 | 27.47 | 57.87 | 68.66 | 58.40 | 53.10 |

| Llama3-8B | PPL | ArcC | ArcE | PIQA | Wino | Mean |
|---|---:|---:|---:|---:|---:|---:|
| Full | 5.54 | 50.43 | 80.09 | 79.71 | 72.61 | 70.71 |
| 2.3 DBF | 6.97 | 45.73 | 76.93 | 77.47 | 70.32 | 67.61 |
| 2.3 +PV | 6.86 | 45.56 | 76.76 | 78.01 | 71.90 | 68.06 |
| 2 DBF | 7.48 | 41.04 | 74.45 | 76.82 | 67.95 | 65.07 |
| 2 +PV | 7.30 | 44.45 | 75.33 | 76.98 | 70.08 | 66.71 |
| 1.5 DBF | 9.37 | 33.61 | 67.59 | 73.99 | 64.64 | 59.96 |
| 1.5 +PV | 9.05 | 35.58 | 68.68 | 74.10 | 65.43 | 60.95 |
| 1 DBF | 15.61 | 21.67 | 50.25 | 65.17 | 56.43 | 48.38 |
| 1 +PV | 13.57 | 25.08 | 56.22 | 67.46 | 58.80 | 51.89 |

The nominal 1-bit fine-tuned retention on these four tasks is 79.57% and 73.38% respectively. At 8B, the separate MMLU/GSM8K table gives full 65.29/54.89, DBF+PV nominal 2.3 bits 56.37/27.59 and 2 bits 52.67/26.15. QTIP 2 bits 56.20/24.79 and AQLM 2.3 bits 56.20/35.25 are comparisons at different nominal rates. The reasoning penalty is material even with more bits than our target. Nonuniform rank allocation reports PPL 7.30 to 7.26 for a tested variant, not a large effect. Reported nominal-1-bit RTX4090 decoding rates for the 7B/8B cases were approximately 170/174 tokens/s against 68/60, batch one and a specific short-generation protocol. [Source tables and speed section](https://arxiv.org/html/2505.11076). I did not recover all appendix comparisons or run the repository. There is no evidence here for 1.7B all-matrix retention.

### 2E. Other compensation and factorized routes, including equal-bit traps

| Approach | Mechanism and evidence | Strict g128 assessment |
|---|---|---|
| [BiLLM](https://arxiv.org/abs/2402.04291) | Different treatment for salient weights, including additional binary residuals. Published nominal ~1.08-bit descriptions depend on bookkeeping. | Any extra sign plane, masks, scales or reordering information must count. A subset given two signs is not our uniform format. Useful for identifying loss directions, not a permitted deployed residual. |
| [OneBit](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7a7a3f53faafc0161be0fcb57e5fa078-Abstract-Conference.html) | Sign matrix with scaling vectors and teacher-guided training. | Per-input/per-output scales generally create differing magnitudes within g128. Fold only if exact common magnitudes remain; otherwise re-fit. |
| [ARB-LLM](https://arxiv.org/abs/2410.03129) | Alternating residual/refinement and structured salience. | Separate rates and deployed representation from training-only residual. Code not byte-audited. |
| [PBBQ](https://www.mdpi.com/2079-9292/15/4/819) | Quantization with propagation-aware compensation and reordering. | Offline error propagation is potentially legal. Persistent reordering/extra representations require folding or accounting. |
| [All for 1-Bit, AF1](https://arxiv.org/html/2609.06161) | Nullspace-aware double-binary factorization, scale-space KD, adaptive structural rank allocation informed by Shapley estimates. | Budget-matched alternative class, not original dense sign/group scale representation. Rank redistribution breaks a fixed rate per original group even if average rate matches. |

AF1's primary Table 1 reports explicit effective weight-bit comparisons, exposing the problem with nominal labels. Its comparison implementation counts BiLLM at 2.88, STBLLM at 3.50, ARB at 2.51 and HBLLM at 3.25 effective bits in the reported configuration. These figures are the AF1 authors' accounting, not verified universal rates for the respective methods. AF1's own 1.00 and 2.50 settings represent factors and side scales, not our format. Smallest model is 4B, above our cutoff.

| Model | BF16 seven-task mean / PPL | AF1 1.00 / PPL | AF1 2.50 / PPL |
|---|---|---|---|
| Llama3-8B | 72.51 / 6.14 | 45.48 / 22.18 | 67.35 / 8.07 |
| Llama3-70B | 79.08 / 2.86 | 61.80 / 8.91 | 72.27 / 4.52 |
| Qwen3-8B | 69.09 / 9.00 | 54.82 / 16.26 | 67.95 / 9.71 |
| Qwen3-14B | 72.47 / 8.64 | 59.61 / 13.32 | 70.33 / 8.87 |
| Qwen3-32B | 72.42 / 7.61 | 64.26 / 11.28 | 72.49 / 8.38 |
| Gemma3-4B-it | 67.12 / 17.39 | 49.86 / 32.82 | 62.29 / 15.39 |
| Gemma3-12B-it | 72.20 / 25.20 | 59.02 / 27.07 | 70.44 / 15.88 |

[AF1 primary table and allocation method](https://arxiv.org/html/2609.06161). Qwen3-8B at 1.00 has 79.35% mean retention on the AF1 suite, not the Bonsai suite. More encouraging at large size; Qwen3-1.7B was not tested in the recovered table. The study's interaction-aware sensitivity estimation is a possible diagnostic, independent of its illegal deployed factorization. In a strict fixed-rate format, allocation means where to spend *training effort*, not extra stored bits.

**Equal-bit comparison principle.** For r residual sign planes over a fraction p of entries, the signs alone cost `1+rp` average bits; add scales, masks, per-group metadata and exceptions. A two-factor representation must count each factor, every side vector and any rank map. An offline residual with no deployment state is free in storage but costs optimization. A learned permutation is free only if the network is exactly reparameterized, all adjacent operators co-permuted and the deployed codec already defines the order. Arbitrary learned transforms stored at runtime are not free. There is no verified apples-to-apples small-model comparison of these methods on our full codec in this batch.

### 2F. Implication and probability

Noda supplies a real 1.5B controlled result that supports cross-layer repair as a conversion stage, but its absolute binary quality is poor and its interface exemption is significant. DBF and AF1 show that binary factors are a different useful compression design, particularly at larger size. Their strong outcomes do not solve the mathematical constraint in our project. The highest-value transferable aspect is the objective: optimize global residual error and preserve end behavior, not isolated quantized matrices. Compensation in subsequent layers is legal if the final corrected layers themselves are strict binary.

**P before: 30%; P after: 38%.** Direct small-model evidence makes global compensation a more credible ingredient. The update is limited because no measured all-matrix strict result with acceptable benchmark retention was shown.

**Cheapest next checks:** recover Noda notebooks/complete implementation if openly released, verify exact quantized-module manifest, compute calibration-data hashes and compare G versus D versus E with fixed token positions and tied-head coverage in a later approved experiment. For DBF, get released packed files and exact vector dtypes plus rank map; enumerate bytes and inspect kernels without inference. If it cannot be deployed exactly as g128, use it only as an offline comparison or initialization with a separately measured hard-collapse gap. No code was run in this review.

## 3. Damage structure, the shrinking cage and information capacity

### 3A. Source and access ledger

| Source | Reading label and route | Scope and outstanding work |
|---|---|---|
| Hu and Ramachandran, [2609.01587](https://arxiv.org/html/2609.01587) | Read in part, primary HTML v2, November 15, 2026 | Main hypotheses, experiments, causal interventions and bit-budget table. All appendix-level statistics, figures and released scripts not audited. |
| Duan et al., [2606.03002](https://arxiv.org/html/2606.03002) | Read in part, primary HTML v2 | SAE matching protocol, main results and pruning comparison; complete supplementary details and code not audited. |
| [Constrained Empirical Weight Distribution, CEWT, 2609.32659](https://arxiv.org/html/2609.32659) | Read in part, primary HTML | Optimizer constraint, main results, selected appendix tables and headings. Complete appendix including FP reference comparisons not audited; [repository](https://github.com/1733116199/cewt) located and opened at root, not run. |
| Leconte et al., [ASkewSGD, AISTATS 2023](https://proceedings.mlr.press/v206/leconte23a.html), [2211.03741](https://arxiv.org/html/2211.03741) | Read in part, conference record and primary arXiv HTML v2 | Constraint formulation, update/KKT discussion, experimental section and Appendix B.4. The HTML header contains an unrelated title string, but the arXiv ID, author/title in body and conference record match. Proofs, complete tables and code not audited. |
| [ProxQuant](https://arxiv.org/abs/1810.00861), [code](https://github.com/allenbai01/ProxQuant); [DSQ](https://pmc.ncbi.nlm.nih.gov/articles/PMC8492711/) | Read in part, abstract/index and accessible publisher text | Proximal and soft-to-hard quantization methods. Not complete primary-file/code audits. |
| Morris et al., [2505.24832](https://arxiv.org/html/2505.24832), [ICML 2026 version](https://proceedings.mlr.press/v306/morris26a.html) | Read in part, primary HTML v3 and proceedings record | Capacity definition, random corpus setup, scaling and precision comparisons. Not every appendix/figure; code not run. |
| Altschuler and Tikhomirov, [2401.15092](https://arxiv.org/html/2401.15092) | Read in part, primary HTML | Binary perceptron model, bound and discussion of threshold; full mathematical proof not audited. |
| [Physics of LLMs, Part 3.3, 2404.05405](https://arxiv.org/abs/2404.05405) | Read in part, abstract/index and cross-reference in primary capacity paper | Factual capacity and low-bit PTQ; full derivations/code not audited in this batch. |
| [Linger and Lose: Knowledge Collapse in Low-Bit Language Models, 2609.32902](https://arxiv.org/html/2609.32902) | Read in part, primary HTML v1, September 26, 2026 | Sections 3-10, Tables 1-6 and 9, selected appendices B/C/H/I/K/L, reproducibility statement. Complete per-seed archive, implementation and other appendices not independently audited; author states code/logs to be released with camera-ready. |
| [Meta-memorization, 2611.01564](https://arxiv.org/abs/2611.01564); [Algorithmic Capabilities of Random Transformers](https://papers.nips.cc/paper_files/paper/2024/file/bccdd196d798a51a4961989984a9ed4a-Paper-Conference.pdf) | Read in part, abstract/index only | Random-data memorization and trained versus fixed-random transformer results. PDF not opened; no binary-weight capacity established. |

### 3B. Where is quantization damage? A direct causal test

[Hu and Ramachandran](https://arxiv.org/html/2609.01587) measure quantization-induced damage and interventions across nine models, including the exact Qwen3-1.7B architecture we target. Their design uses 22 CORE tasks, approximately 200 examples per task, continuation scoring and fixed selection; primary experiments start from 4-bit RTN and repair selected components at higher precision, with groupwise GPTQ/AWQ comparisons. Models include Qwen2.5-0.5B, Qwen3-0.6B/1.7B/8B, Llama3.2-1B/3B, Llama3-8B, Mistral7B and OpenLlama3B. One model is excluded from the groupwise comparison because of shape compatibility.

Three broad propositions are tested: whether circuit drift localizes task damage, whether first/last MLP repairs recover most damage, and whether static weight statistics predict the sensitive regions. Raw circuit-drift association is around .377, falling to around .05 after controls. Boundary MLP repairs explain at most 13% for six of nine models, with exceptions including Mistral at 55.5%. Weight standard deviation is not a model-independent sensitivity criterion; local reconstruction error is even inversely associated in one Qwen condition. These are not general proofs that no vulnerable circuit exists. They challenge extrapolating layer sensitivity from a single metric or family.

The central same-budget comparison allocates an additional approximately 0.146 effective bits per weight either globally through groupwise quantization or locally via selective 8-bit repair. Recovery below is a fraction of the damage between baseline quantization and FP reference, not fraction of teacher accuracy. The third column is a concentrated alternative.

| Model | Global g128 recovery % | Local repair % | Top-one concentrated % |
|---|---:|---:|---:|
| Llama3-8B | 78.8 | 44.7 | 43.7 |
| Qwen3-8B | 76.6 | 54.9 | 39.7 |
| Mistral7B | 72.9 | 51.7 | 50.9 |
| Qwen3-1.7B | 66.9 | 14.9 | 14.9 |
| Llama3.2-1B | 64.9 | 17.2 | 29.5 |
| Llama3.2-3B | 62.9 | 36.7 | 36.5 |
| Qwen2.5-0.5B | 41.1 | 3.4 | 3.9 |
| Qwen3-0.6B | 33.4 | 4.8 | 4.7 |

[Latest primary text, budget comparison](https://arxiv.org/html/2609.01587). Their rate matching is an approximation using the specified accounting, not a byte audit. These data particularly support distributed improvement at small size. The Qwen3-1.7B result is almost 4.5x larger recovery under the global intervention than local repair. This is about 4-bit compression and additional bits, not a measured 1-bit result. We cannot spend extra bits under our project rule. The useful inference is to investigate global optimization and grouping, and not rely on a handful of repaired layers to carry the whole conversion. The study does not establish that every coordinate is equally important, that a particular groupwise layout is optimal, or that second-order sensitivity would fail.

### 3C. Feature damage invisible to perplexity

[Duan et al.](https://arxiv.org/html/2606.03002) run the same pretrained sparse autoencoder on FP and quantized activations and measure featurewise correlations on the same token stream. Pythia70M layer 4 and Gemma2-2B layer 12 are examined, with 200k and 500k token samples respectively; the Gemma SAE has 16,384 features. Quantization is signed per-channel RTN at 8 through 4 bits, with embedding/normalization treatment outside the quantized linear matrices. The pruning control approximately matches aggregate loss while changing the damage mechanism.

Selected full numerical tables, with ΔPPL as reported percentage change and correlations across matched features:

| Pythia70M | ΔPPL % | Mean correlation | Surviving % | Severely damaged % |
|---|---:|---:|---:|---:|
| FP | 0 | 1 | 100 | 0 |
| INT8 | 1.020 | .981 | 98.312 | 0 |
| INT7 | 2.258 | .957 | 86.322 | 0 |
| INT6 | 14.722 | .888 | 62.395 | 1.020 |
| INT5 | 71.208 | .777 | 37.957 | 12.588 |
| INT4 | 371.112 | .583 | 14.504 | 37.711 |
| Matched pruning | 13.488 | .891 | 60.970 | .299 |

| Gemma2-2B | ΔPPL % | Mean correlation | Surviving % | Severely damaged % |
|---|---:|---:|---:|---:|
| FP | 0 | 1 | 100 | 0 |
| INT8 | 2.624 | .966 | 99.090 | 0 |
| INT7 | -5.648 | .943 | 81.257 | 0 |
| INT6 | 3.989 | .891 | 51.302 | 0 |
| INT5 | 17.716 | .764 | 27.716 | 5.921 |
| INT4 | 46.081 | .494 | 12.402 | 54.703 |
| Matched pruning | 6.126 | .841 | 38.578 | .238 |

[Source results and definitions](https://arxiv.org/html/2606.03002). These numbers make PPL an inadequate sole diagnostic. At INT7 Gemma's reported PPL improves but nearly 19% of features do not meet the survival threshold. At INT6 the loss change is modest compared with the fraction of features classified as no longer surviving. Feature survival thresholds and population filters are specific to the paper.

Important limitation: a fixed teacher SAE is a coordinate system. Quantization-induced rotation or change of basis can make a feature unreadable by that decoder without erasing the information from the model. Correlation damage is neither a direct causal measure of knowledge deletion nor a proof that re-training an SAE could not recover an equivalent concept. Conversely, correlation can stay high for a feature whose downstream readout has failed. The paper measures feature alignment, not full causal equivalence. Compare representations under linear alignment and conduct actual behavior/patch tests before calling a feature destroyed. Both studies start at 4 bits or higher, so quantitative damage at 1 bit is still unknown.

### 3D. What a 1-bit damage map should measure

The two papers are consistent, not contradictory. Damage can be spread through many operators while particular representational features suffer disproportionate loss. A global training remedy may work better even if a rare capability has a localized causal bottleneck. The appropriate unit of damage is a task, a token position, a representation direction, a layer interface and the effect of a controlled repair, not just a layer's weight histogram.

Minimum damage record for a later approved experiment:

| Measurement | Why it matters | What it cannot prove alone |
|---|---|---|
| Full ten-task retention and per-item teacher/student paired outcomes | Actual product scoreboard; localizes which examples change | Unknown abilities outside the suite |
| Teacher correct -> student wrong, and teacher wrong -> student correct, with paired bootstrap | Separates damage from compensating improvements in averages | Mechanism |
| Per-token teacher KL, true-token NLL, top-k rank and margin, stratified by rare and frequent tokens | Separates output drift, tail losses and factual-token errors | Correct reasoning or feature survival |
| Per-layer local reconstruction and accumulated teacher-student residual | Locates amplification, cancellation and drift | Causality without interventions |
| Controlled activation or layer patching, including embedding/head | Tests effect of restoring a component or representation | Deployed legality; FP patches are diagnostic only |
| Fixed teacher SAE at selected layers and optional aligned/fresh SAE | Detects representation damage hidden in aggregate loss | Actual causal concept removal |
| Magnitude saturation, scale range, sign flips, activation covariance rank/eigenvalues | Relates optimizer mechanism to realized codec | Benchmark performance |
| Held-out factual associations, instruction and tool-call behavior, rare-token accuracy | Detects collapse not visible in text likelihood | Entire teacher knowledge |
| Time series at hard-sign endpoints during training | Detects late regressions and irreversible loss | Complete optimization optimum |

For the ten-task suite do not fit any calibration or weighting schedule to its test items. The benchmark suite must remain a clean scoreboard. Task-family calibration and damage probes require independent datasets or train/validation partitions. Never use PPL, weight MSE, activation CKA, SAE survival or a single patch as the sole graduation criterion.

### 3E. Shrinking cage: closest known prior art

Search routes included `annealed interval-constrained optimization binary weights`, `shrinking box constraint neural network binarization`, `weight clipping schedule binary quantization training`, `homotopy continuation binary weights quantization`, `proximal binary neural networks quantization`, `progressive annealed binarization transformer`, `exact gradients quantization no straight-through`, `empirical weight distribution constrained pretraining` and the earlier Caltech inventor searches. Conference and arXiv results were cross-checked, including ASkewSGD and ProxQuant. This is not a patent novelty or exhaustive prior-art opinion.

| Precedent | Core procedure | Relation to our hypothesis |
|---|---|---|
| [ASkewSGD, Leconte et al.](https://arxiv.org/html/2211.03741) | Anneals smooth inequality constraints around discrete levels and uses constrained stochastic update directions; infeasible iterates allowed. | Very close in principle: continuous loss and increasingly restrictive feasible sets, then discrete endpoint. Unlike our single box it can explicitly exclude the middle between binary levels. Not group-scale LLM distillation. |
| [Caltech patent](https://patents.justia.com/patent/20260220467) | Maximum-norm plus quadratic mirror potential yields a groupwise, dual-driven clipping map. | Near-direct mathematical relative of the group cage; threshold endogenous instead of scheduled. No guaranteed all-coordinate saturation. |
| [ProxQuant](https://arxiv.org/abs/1810.00861) | Continuous gradients followed by proximal update under a quantization-attracting nonconvex regularizer. | No STE needed for continuous gradient; annealed attraction to both signs, unlike upper clipping. |
| [Mirror Descent View](https://arxiv.org/html/1910.08237) | Invertible soft projections and annealed temperature/dual updates. | Continuous forward, soft-to-hard homotopy. The geometry differs from projected ordinary gradients. |
| [Differentiable Soft Quantization](https://pmc.ncbi.nlm.nih.gov/articles/PMC8492711/) | Smooth approximation to staircase quantization with a sharpening parameter. | Annealed forward map, not post-step clipping of real weights. |
| [BinaryConnect](https://arxiv.org/abs/1511.00363) | Real latent weight accumulation with binary forward weights and clipping. | Its bound stabilizes latent weights but does not avoid hard forward quantization or the gradient-estimation issue. |
| [CEWT](https://arxiv.org/html/2609.32659) | Constrains the empirical distribution of weights during low-bit pretraining using ordered-statistic projection. | Shows a distribution constraint can stabilize low-bit optimization, but the target is Gaussian-like, not a two-point shell. |
| [Noda](https://arxiv.org/html/2607.14630) | Teacher distillation with soft binary parameters and late hardening. | Closest LLM setting among these sources, but already uses an explicitly sign-oriented parameterization and a late surrogate. |

**ASkewSGD is the strongest prior art against calling the shrinking cage novel.** Its method creates a family of continuous constrained optimization problems that approach a discrete feasible set as annealing proceeds. Its update corrects gradient directions using active-constraint information; it does not require projecting every iterate into the entire feasible set. Its convergence statement applies to the relaxed fixed subproblem under assumptions, not a global optimum of the discrete problem. The binary ImageNet Appendix B.4 provides a particularly useful direct comparison under one protocol (single run):

| Method | ResNet18 ImageNet top-1 | Top-5 |
|---|---:|---:|
| Full precision | 66.39 | 95.32 |
| BinaryConnect | 45.85 | 71.05 |
| Mirror descent | 46.38 | 71.18 |
| AdaSTE | 35.37 | 62.22 |
| Projected gradient | 2.58 | 7.93 |
| ASkewSGD | 46.95 | 72.11 |

The 100-epoch experiment uses Adam, batch 512, annealing over its latter half and final sign evaluation. Its broader 200-epoch study has different first/last-layer treatments and should not be merged with this comparison. The simple projected-gradient control is especially cautionary; it does not directly implement our proposed group cap and thus is not a refutation of our exact method. [Appendix B.4 and algorithm](https://arxiv.org/html/2211.03741). No g128 transformer demonstration found in this source.

**CEWT:** the relevant result is not a proof of the cage. The paper constrains an empirical distribution through sorting/rank assignment to target order statistics, together with hyperspherical optimization. Its objective is stable distribution geometry during pretraining, including low-bit weights and activations, not converting a fixed parent with an equal-magnitude sign shell. It tests GPT-style and Llama-style models, roughly 95M-610M parameters, on C4. Selected reported low-bit perplexity comparisons for its optimizer recipes:

| Model/recipe | Without CEWT | With CEWT |
|---|---:|---:|
| Llama95M AdamH BBQ | 51.06 | 46.12 |
| Llama206M | 36.76 | 33.20 |
| Llama332M | 30.91 | 28.77 |
| Llama610M | 25.89 | 24.49 |
| GPT-style 94M LSQ LionH | 95.35 | 74.04 |
| GPT-style 325M BBQ | 35.46 | 32.74 |

[CEWT primary results and supplementary tables](https://arxiv.org/html/2609.32659). The 95M example also reports reduction of its RBM metric from .034 to .010. The paper's reported aggregate extra training cost is about 4%. These are within-method comparisons, not FP-parent retention ratios. I could not fully inspect the full-precision reference tables, exact quantization exclusions and each W/A configuration. Do not label all rows strict W1 or compare them directly to the Bonsai score. Its distribution concentration argument relies on sufficiently large coordinate sets; 128 is much smaller than the >1024-size guidance encountered in the text. This motivates checking the statistical behavior of any per-group distribution constraint instead of assuming large-sample guarantees.

**Novelty judgment.** Gradually restricting continuous weights, annealing toward a discrete set, clipping latent weights, exact gradients before hardening and proximal projection are all established ideas. The particular combination of (a) distilled pretrained decoder-only LLM, (b) individual 128-weight shared FP16 caps, (c) an upper-only scheduled clip with free interior coordinates, (d) final closure into every sign plus scale, and (e) complete embedding/head coverage was not verified in a public implementation from the searches above. That is a specific untested combination, not a claim of invention. ASkewSGD and the Caltech patent are the priority references before any novelty claim.

### 3F. Mathematical failure of an upper-only cage, and criteria for a fair test

Define the proposed update with group cap c_t>0:

```
w_(t+1) = clip(w_t - η_t ∇L_distill(w_t), -c_(t+1), +c_(t+1))
```

This is Euclidean projected gradient for a moving convex box when using SGD; AdamW would give a different metric/dynamics. A boundary component is exactly representable by the target codec only if c is exactly the deployed FP16 scale. Every interior component is not yet binary. Distillation with exact teacher initialization gives no update until the constraint acts. Once active, outward gradients are truncated while inward gradients may free previously saturated weights. Saturation is therefore not monotonic in general.

A counterexample is enough to disprove guaranteed closure. Take the least-squares target `(1,0)`, with independent inputs and equal weight importance. Under cap `0<c<1`, the box optimum is `(c,0)`, not `(c,c)` or `(c,-c)`. Lower the cap arbitrarily close to zero: the second coordinate remains zero. At positive c it always needs a final sign; at c=0 every weight collapses to zero. The best strict binary least-squares solution with free common scale is `(0.5,±0.5)`. Thus merely reducing the cap cannot guarantee a no-rounding-loss endpoint.

For a fixed nonzero c, a strict binary solution is a vertex of the box. Continuous loss can prefer an interior face; KKT conditions do not imply vertex selection. Exact sign selection is combinatorial. An all-saturated feasible state may still be suboptimal and may be difficult to change without temporarily returning through the interior. Freezing boundary weights unconditionally could eliminate necessary compensation. The group's L2 norm, free-coordinate count and actual endpoint error are therefore required observations. The fixed-norm equality argument in 1H is one mathematically sufficient endpoint, but no theorem says that suitable group radii preserve the teacher. A closure condition must be tested against the softer alternatives rather than silently appending STE and attributing the result to exact-gradient training.

A fair comparison uses the same teacher checkpoint, data positions, number of processed tokens, hard-format validation protocol, scale representation, optimizer-state budget and teacher signals. Compare actual hard-forward checkpoint loss throughout, not just each method's own continuous training objective. If the final STE phase consumes tokens, count them. A training-only floating tensor is legal; an inference-time floating escape hatch is not. The new ideas for endpoint closure and controls are consolidated in Section 4.

### 3G. Capacity: the requested Morris measurement and what it does not establish

[Morris et al.](https://arxiv.org/html/2505.24832) isolate memorization by training on unstructured uniform sequences so that compression of those sequences measures stored sample-specific information rather than shared regularities. For N sequences of length S over alphabet size V, with independent uniform symbols, the nominal data entropy is `NS log2 V`. A cross-entropy code using the model with total NLL measured in bits gives the compression-gain estimator `NS log2 V - NLL_bits` (up to context/boundary and estimation conventions). Divide by the count of model parameters. This is an experimentally achieved quantity, not a universal mathematical maximum for all transformers.

The capacity sweeps use small GPT-style networks (roughly 100k-20M in the relevant random-data regime), widths 32-512, depths 1-8, sequence length 64 and vocabulary 2048 in the described configuration, extensive training and multiple seeds. The reported typical plateau is approximately 3.5-3.6 bits/parameter; precision comparisons report means near 3.83 FP32 and 3.51 BF16. The broader membership-inference experiments span roughly 500k to 1.5B but are not identical to the saturation sweep. [Published ICML record](https://proceedings.mlr.press/v306/morris26a.html). It does not establish strict binary capacity. A smaller bit alphabet bounds the number of distinct states, but reaching that bound through optimization is a separate issue.

[Allen-Zhu and Li, 2404.05405](https://arxiv.org/abs/2404.05405) use structured random synthetic facts rather than uniform text, and report roughly 2 bits per model parameter in the relevant regime. Their quantization investigation indicates that 8-bit PTQ largely preserves that measured knowledge while lower-bit PTQ loses substantial knowledge. The metric measures a particular factual encoding task. The fact that it is smaller than Morris's 3.6 is not a contradiction: task entropy, architecture, training protocol and measured information differ. Their results do not prove that a 1.72B teacher's natural-language knowledge is 3.44B independent bits.

[Meta-memorization, 2611.01564](https://arxiv.org/abs/2611.01564) and [Algorithmic Capabilities of Random Transformers](https://papers.nips.cc/paper_files/paper/2024/file/bccdd196d798a51a4961989984a9ed4a-Paper-Conference.pdf) surfaced in related searches. The former uses random binary *data*, which is distinct from binary *weights*. The latter compares learned with largely fixed random transformer components. Neither indexed result verifies a strict binary weight capacity measurement. I did not treat an indexed PDF as a fully inspected paper.

### 3H. Major additional discovery: direct ternary-transformer factual capacity

**[Linger and Lose: Knowledge Collapse in Low-Bit Language Models, arXiv 2609.32902](https://arxiv.org/html/2609.32902)** is the most directly relevant additional source uncovered by the capacity search. It answers a question the starting sources leave open. It is a September 2026 preprint, not independently replicated here. Its public reproducibility statement says the code/logs will be released with the camera-ready version. It must not be treated as a currently reproduced result.

The authors train GPT-2-style decoders from scratch at 2.5M, 10M, 25M and 50M parameters on synthetic biographies, supplying 2.25 known data bits per parameter at full load. Five weight precisions are compared. Crucially the ternary runs use ternary transformer bodies but INT4 embeddings and output heads; activations remain BF16. This is more permissive than our format. A factual-capacity estimator combines name/attribute entropy with their NLL. The main schedule has 1000 exposures, AdamW peak LR 5e-4, cosine decay to 10% of peak. A separate short warmup-stable-decay cooldown comparison tests stability.

Main reported retention of factual capacity against matched FP16 (not benchmark score):

| Precision | 2.5M | 10M | 25M | 50M |
|---|---:|---:|---:|---:|
| INT8 | .979 | .936 | .926 | .754 |
| INT4 | .893 | .686 | .581 | .316* |
| INT3 | .660 | .468 | .320 | .504 |
| Ternary body | .364 | .235 | .090* | .058* |
| Ternary PPL multiplier | 1.39x | 1.41x | 1.58x | 2.88x |

`*` Estimator convention affects these cells. The primary table explicitly flags that problem. A per-attribute floor changes ternary cosine 25M to .126 and 50M to .109; 50M INT4 changes to .490. The alternative Morris-style estimator returns .200 at 10M and .185 at 25M for ternary cosine, and an anomalous signed negative value at 50M due to the held-out entropy cap. This is essential: the paper's most alarming numbers partly reflect an evaluation convention and the behavior of a single unpredictable attribute. Do not claim 94% of all useful knowledge was literally erased.

The authors' measured 25M absolute bits/parameter are particularly useful:

| Precision | Standard cosine | WSD with 10% cooldown |
|---|---:|---:|
| FP16 | 1.720 (6 seeds) | 1.644 (3) |
| INT8 | 1.593 (2) | 1.684 (2) |
| INT4 | .999 (2) | 1.229 (2) |
| INT3 | .551 (2) | .898 (3) |
| Ternary | .155 (6) | .412 (5) |

WSD ternary retention at 10M/25M/50M is .257/.240/.247 compared to the standard cosine .235/.090/.058. Under the alternative per-attribute/Morris estimators the magnitude of improvement is smaller in some cells. Appendix K reports FP16 Morris-style values around 3.0-3.3 bits/parameter at 10M/25M, and 2.5-2.7 at 50M. At 25M a collapsed checkpoint scores .567 bits/parameter on that alternative while a pre-collapse checkpoint scores .557. That estimator largely misses the factual-collapse event. This is a second important metric-blindness result, not evidence one estimator is universally better. [Tables 1, 3, 4, 9 and Appendix K](https://arxiv.org/html/2609.32902).

Mechanism evidence: controlled branches from the same checkpoint kept at rates near 0.8e-4 to 2e-4 showed collapse with extended exposure, whereas higher rates were more stable over the tested horizons. A short cooldown crossed that region faster. At a 25M checkpoint, an unpredictable birth-month token drove the large NLL degradation while other token predictions largely persisted; removing or making that attribute predictable avoided the same collapse in the tested conditions. The head LR intervention was more effective than slowing the embedding alone. In one longer preregistered branch the head intervention delayed rather than conclusively prevented collapse. FP16 also exhibited a related failure in a 50M seed. This supports a training-instability mechanism, not an exclusively ternary representational impossibility. Do not copy absolute LR values directly to Qwen. [Sections 5-8 and appendix controls](https://arxiv.org/html/2609.32902).

PTQ on the 25M pretrained checkpoints, factual capacity in bits/parameter:

| Method | INT8 | INT4 | INT3 | Ternary |
|---|---:|---:|---:|---:|
| RTN | 1.710 | .136 | 0 | 0 |
| AWQ | 1.672 | .122 | 0 | 0 |
| GPTQ | 1.674 | .142 | 0 | 0 |
| NF4 | not tested | .174 | not tested | not tested |
| QAT cosine | 1.593 | .999 | .551 | .155 |

The reported fine-tuning-from-FP control at 25M ends at .402/.371 bits per parameter in two seeds, without the same collapse, rather than demonstrating full factual recovery. See [Section 9 and Appendix C](https://arxiv.org/html/2609.32902). This is concrete evidence that straightforward low-bit PTQ can lose factual capacity on one synthetic task, and that learning under the lattice and training schedule matter. It does not rule out a better conversion algorithm, nor establish that a 1.7B model exhibits precisely the same behavior. The paper explicitly leaves open whether natural text has the same trigger, and whether measured collapse is actual erased knowledge or a localized readout/metric pathology. Its 50M ceiling and mixed-precision vocabulary interface constrain transfer.

**Transfer to 1 Bit Summit:** this is now a priority primary source for both the science scoreboard and training design. We should record factual-capacity/rare-token probes before and throughout conversion and avoid relying on final loss. Because our vocabulary interface must be binary, unlike this study, it is a high-risk subsystem that needs separate diagnosis, not an excuse to exempt it. Learning-rate cooldown, head/body update ratios, weight decay coupling and hard checkpoint selection must be controlled. If the embedding is tied to the head, independent head and embedding optimizers cannot be implemented as separate parameter groups without changing the architecture. Separate gradients from lookup/output paths can be diagnosed, but any alternative update must be explicit and preserve tying.

### 3I. Binary perceptron and information-theoretic limits

[Altschuler and Tikhomirov](https://arxiv.org/html/2401.15092) analyze the storage capacity of a binary perceptron on random patterns. For a sign weight vector in dimension n and random independent constraints, the question is the maximum number of feasible patterns relative to n. Their result improves the rigorous upper bound to approximately .847 constraints per weight in the specified model. The commonly discussed threshold is near .833, with other rigorous results depending on hypotheses; I did not independently audit the lower-bound proof and will not call .833 a universal proven threshold.

One simple bound can be derived without their advanced proof. There are 2^n sign vectors. For any fixed vector with Gaussian random inputs and independent fair binary labels, the chance of satisfying m independent labels is 2^-m. Expected satisfying weight vectors are 2^(n-m). Markov's inequality then rules out satisfiability with high probability when m>(1+ε)n. Correlations between solutions tighten the result below 1. This is about random classification constraints, not bits of arbitrary LLM information. A single global positive scale changes no perceptron classification. Multiple trainable group scales change the hypothesis class and invalidate a direct use of the simple sign-only theorem.

Other searches (`binary synapse information capacity bits per synapse`, `ternary transformer capacity factual bits per parameter`, `binary language model random sequence memorization`, `BitNet knowledge capacity`, `binary perceptron discrete weights capacity`) surfaced [binary-synapse perceptron learning studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC1904114/), [recurrent memory capacity with discrete synapses](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003727), and [finite-synapse memory models](https://pmc.ncbi.nlm.nih.gov/articles/PMC2580035/). These were read in part via index/abstract only. They measure pattern retrieval or biologically constrained memory, not language-model weight-bit capacity; their constants must not be transferred. The new ternary study above is the direct measurement of transformer capacity found, but it does not cover strict binary or our vocabulary interface. No direct strict 1.125-bit all-matrix Morris-style saturation experiment was verified. This is a bounded search result, not a universal statement that it has never been done.

### 3J. What can a 1.72-billion-weight model actually hold?

Pure codec count, assuming exactly 1.72B unique weights divisible into g128 and no padding:

| Quantity | Value |
|---|---:|
| Sign bits | 1,720,000,000 |
| Groups | 13,437,500 |
| FP16 scale bits | 215,000,000 |
| Total encoded weight bits | 1,935,000,000 |
| Sign bytes | 215,000,000 |
| Scale bytes | 26,875,000 |
| Total weight bytes | 241,875,000 (241.875 MB decimal; 230.67 MiB) |

This is an upper bound on the state-description budget, not an estimate of useful learned knowledge. Some states are redundant. For example, if scales are strictly positive finite FP16, there are 31,743 nonzero values, about 14.954 bits of scale state per group. Negative scales need not be distinct because their sign can be absorbed in all signs. Zero collapses many sign configurations into the same decoded group. The upper rate for distinct positive-scale group states is about `1+14.954/128=1.116829` bits/weight, plus the separately possible zero group. The difference is small but conceptually important. Additional learned norm/bias tensors count toward whole-model information capacity even if exempt from the matrix codec. Fixed tokenizer and architecture are public shared side information; learned external tensors, retrieval corpora or data-dependent code are not free.

For fixed architecture and a public training-independent decoder, a model state θ represented by B bits satisfies `I(D;θ)≤H(θ)≤B`, where D denotes a random dataset. If a teacher stores B_teacher independent random data bits and the student must reconstruct them all, B<B_teacher rules out perfect transfer in the general case. For M independent fair random labels, under expected label error e, a standard entropy/Fano-style bound is `M[1-h₂(e)]≤B`, where h₂ is binary entropy. In the idealized exact case M≤B. This is a bound on information, not on benchmark points.

Hypothetical comparison if the same 1.72B network were actually saturated on these synthetic tasks:

| Teacher storage rate | Hypothetical teacher bits | Maximum fraction under raw 1.125-bit budget |
|---:|---:|---:|
| 2.0 bits/parameter | 3.44 billion | 56.25% |
| 3.5 bits/parameter | 6.02 billion | 32.14% |
| 3.6 bits/parameter | 6.192 billion | 31.25% |

These are conditional ceilings for reconstructing independent random information. They are not measured Qwen3 knowledge capacities. Natural-language tasks have shared algorithms, redundancy, correlations, predictable world structure, and finite evaluation sets. A model can generalize many correct outputs from fewer bits, and a teacher can waste representational capacity. Conversely, some rare factual associations may be almost incompressible. A binary network may preserve the majority of selected reasoning behavior while losing substantial rare factual content. Exactly that separation motivates measuring both.

The 99% benchmark goal therefore remains logically possible. It is not implied by any capacity theorem or current reference. A universal 99% preservation of arbitrary teacher behavior is generally much stronger and cannot be promised. If the user ultimately means full teacher functional equivalence over all inputs, the project needs to distinguish that from the current finite-suite metric. The current scientific claim should remain 99% of the matched ten-task average, plus independently reported damage measures. No probability of 99% derived from the state count is defensible without assumptions about the actual teacher and task distribution.

### 3K. Smallest informative capacity experiment, not executed

A useful study should separate theoretical codec state count from empirical trained information and from retention during conversion. Reusing existing random-data/factual-capacity generators is preferable to inventing a harder benchmark. Proposed later experiment, pending approval, with no model run performed in this review:

1. Construct a small decoder-only transformer (roughly 0.5M-2M unique weights, tied embedding if the architecture normally ties it), with all quantized matrix dimensions and vocabulary aligned for g128. Report all remaining FP parameters. Use two parameter sizes initially to distinguish finite-size artifacts. This is a proposed scale, not an assertion that results extrapolate to 1.7B.
2. Generate uniformly random token sequences following Morris's protocol, plus separate synthetic factual key/value associations from a known-entropy generator. Fix independent held-out seeds; use identical data and architecture in each precision. Sweep data entropy per parameter, not only token count. Include enough points below and above the nominal 1.125 cap to identify saturation.
3. Train a FP16 reference from scratch to a measured plateau. Independently train a strict binary model from scratch with a standard hard-forward STE and the same data. Convert a copy of the full-precision reference using the candidate conversion formula and a matched STE-distillation control. A ternary control with its actual packing/scales recorded separates alphabet from optimizer. Equal-token comparisons and longer plateau comparisons answer different questions; report both if approved.
4. At intervals, serialize and decode the actual packed weights, including embedding/head. Evaluate exact hard checkpoint NLL in bits, memorized factual bits, key/value top-1 and per-attribute NLL, including unpredictable-token controls. Record unquantized parameter contribution and dataset entropy. No test-only facts enter calibration. Store checkpoint sizes and file hashes. Ensure teacher/student count the same context and prefix information.
5. Compute compression gain and the factual estimator with raw signed and per-attribute variants, retaining negative values instead of silently flooring. Report held-out cross entropy and estimator differences. Measure peak and endpoint; use multiple independently chosen seeds. Stop when a documented convergence/plateau criterion is satisfied, not merely when a fixed schedule ends. Do not infer a representational ceiling from an optimizer that has not converged.

Minimal primary outcome: achieved bits/unique parameter at strict binary plateau, compared with the 1.125 raw budget and the FP baseline; secondary outcome: recovered teacher factual bits after conversion, hard-checkpoint benchmark proxy and collapse behavior. The experiment may produce a lower bound on attainable capacity, not a proof of an upper bound. The largest uncertainties are data load, optimizer choice, readout limitations, and scaling to Qwen3-1.7B.

### 3L. Probability and unresolved work

**P before: 35%; P after: 32%.** The distributed-damage finding on Qwen3-1.7B and constrained-training precedents are encouraging. The mathematical incompleteness of the naive shrinking box, the direct factual-capacity/PTQ results and their mixed-precision vocabulary interface are significant negative evidence. The 70.2% goal is still a benchmark-retention event, not a factual-capacity event, so the probability update is limited. The ternary paper's own estimator controversy prevents taking its smallest retention values as a literal bound.

Cheapest documentary work: fully read ASkewSGD proofs/appendices, CEWT FP baselines and code, Hu/Ramachandran appendix and evaluator, SAE feature definitions and released scripts, Morris exact random-data code, binary perceptron proof and the Linger and Lose raw run ledger when available. Before spending full-model compute, the exact endpoint and metric conventions can be checked algebraically, then tested on controlled synthetic regressions and the small capacity experiment only when authorized. The direct capacity lead changes the experimental priorities; it does not justify a model run in a research-only batch.

## 4. Cross-item decisions and new ideas for the project owner

### 4A. What should change now

1. **Make endpoint feasibility a formal gate.** The proposed mirror descent and shrinking cage both need explicit proof of what weights are representable at the end. Add a hard codec validator: exactly one legal FP16 scale and 128 signs per full group, correct padding, embedding/head included, no hidden tensors or conversion metadata at inference. Validate the serialized model, not merely the latent training model. A soft model is not a product checkpoint.
2. **Split the research scoreboard into geometry, behavior and capacity.** Keep the ten-task retention as the product score. Add science outcomes for local/global activation compensation, hard-vs-soft endpoint gap, causal recovery and knowledge bits retained. A low PPL or high saturation fraction cannot award a benchmark trophy. Conversely, a benchmark improvement with an unresolved factual-collapse mechanism must be documented rather than called complete preservation.
3. **Treat the vocabulary interface as an explicit coupled optimization problem.** Noda exempts it, the random-feature paper warns about a continuous readout, and Linger and Lose finds a head-driven instability even with INT4 or occasional FP interfaces. Verify tying in Qwen3 and LFM2. Test tied-matrix gradient contributions and optimizer dynamics, rather than quietly breaking tying. The interface is included in every final score.
4. **Use global compensation as the principal objective candidate, not factorization as a deployment workaround.** Noda's comparison favors accumulated residual matching over logit KD at the same short run and its feature-only objective fails on PPL. Use this as a controlled training-loss comparison. Do not add all losses and optimizer ideas simultaneously. DBF/AF1 are useful counterfactual compressors but should not count on our product scoreboard.
5. **Track capacity at checkpoints, not just at the end.** Include rare-token margins, factual probes, scale range, logit drift and per-attribute metrics, with cooldown and interface update rules recorded. The late-capacity preprint makes this particularly urgent. Stop and preserve the best *hard* checkpoints; do not assume more tokens or lower LR always help.

### 4B. New ideas, explicitly hypotheses rather than reported results

**A. Norm-conserving cage closure.** Parameterize each group with radius R_g and cap c_g. Begin from feasible `c_g≥||w_g||∞`. Anneal the ratio `c_g sqrt(128)/R_g` toward one, while maintaining group norm approximately R_g. At equality, all magnitudes must match; a representable endpoint follows algebraically. R_g may need to move slowly and be projected to a scale consistent with FP16 at the endpoint. Projection onto a box intersected with a sphere is nonconvex, so use a separately specified solver or controlled alternating method. Do not assert that naive clipping followed by renormalization is a valid exact projection or always feasible. A toy constrained regression should falsify or validate the mechanism before any large run. Compare with ASkewSGD-style two-sided intervals and the patent's endogenous rigid cage. The hypothesis is that preserving norm avoids trivial collapse while free coordinates permit compensation until closure; not that it guarantees low loss.

**B. Shell closure via activation-space residual.** At the terminal stage, for a group with a small count of free coordinates, keep saturated signs fixed only during a local search. Choose remaining signs and the legal FP16 scale to minimize calibration output residual, carrying the residual across groups in a greedy or beam refinement. Consider optional saturated sign swaps after closure. The proof in 1F explains when few free weights suffice; the covariance criterion in 1H identifies the right loss. Distinct controls: naive final sign, covariance-aware scale, greedy residual signs and short matched STE. This uses no additional inference state. The key diagnostic is actual closure loss on held-out activations and full hard model, not the calibration residual alone.

**C. Offline global error cancellation with no side vectors.** Treat continuous compensation updates as an optimizer search state and require them to be absorbed into legal sign/scale changes in downstream layers. For a residual network, jointly fit small blocks with teacher-forced and free-running student inputs. A diagnostic teacher activation restore can estimate where a fixed-rate correction would have greatest effect, while the deployed model remains uniform. Compare layer-local versus accumulated-error objectives and global KL before adding feature moment terms. A held-out covariance mismatch probe is essential.

**D. Schedule as causal variable, not housekeeping.** The new capacity study suggests testing a short cooldown versus slow cosine at the same token budget and measuring hard checkpoints frequently. Record effective AdamW decay (`η λ`), sign-flip activity and tied vocabulary path gradient magnitudes. Select a safe schedule using independent validation probes, not the final ten benchmarks. No absolute small-model LR threshold is transferred without measurement. Test whether irreversible rare-token damage begins before benchmark or PPL degradation. This could produce a scientific result even if it does not immediately yield a five-point improvement.

### 4C. Integrated judgment and remaining blockers

Overall event P, conditioned on the campaign in Section 0: **40% before, 45% after**. These are correlated route judgments, not combined independent probabilities. The most persuasive positive evidence is a direct small-model comparison of global compensation, mathematical closure opportunities, and the exact-architecture distributed-damage evidence at higher bits. The most persuasive negative evidence is poor absolute binary PPL in small-model PTQ, the special difficulty of the vocabulary interface, lack of verified strict full-model transfers from the mirror literature, and the new measured gap between ternary factual capacity and FP capacity. I would not raise the probability further until we have a matched measured binary baseline of our own, an actual closure experiment, and a capacity probe.

The project owner should prioritize the following unresolved documentary gaps, not interpret them as completed: full reading of every named primary PDF and all mathematical appendices; patent counterpart/prosecution and inventor releases; exact code audit and runtime reproducibility; full per-model table extraction for RF/greedy/Kashin and CEWT; exact whole-model storage manifests for DBF/Noda/AF1; independent raw logs and code for the late capacity paper. Direct container downloads failed, and several repository raw paths were inaccessible. I did not use credentials or paid access, and I did not train/evaluate a language model. No product or science trophy is claimed from this review alone.
