# 1 Bit Summit: Follow-up to Batch 10 and Round 2

26 November 2026 | Independent reviewer | Scope restricted to the two owner-supplied PDFs

## 0. Source status and changes to the record

- `pdf.pdf`: Tadimeti and Maltsev, *Quantization-Aware Distillation for 4-Bit On-Device Language Models*, NeurIPS 2026 workshop. **Previously read in part**: the abstract and associated checkpoint documentation, not the full workshop paper. Round 2 sections 11B and 14 explicitly reserved judgment on the abstract. **Now read in full from the supplied 13-page paper**, including main method, Tables 1-13, appendices A-C and Figures 1-7. All figures inspected through rendered PDF pages. The training data, full training implementation, checkpoint bytes and independent replication are not supplied by this PDF and are not certified here.
- `U.S. Patent Application for Systems and Methods for Training Neural Networks and.pdf`: Caltech, publication [US20260220467A1](https://patents.justia.com/patent/20260220467). **Previously read in part** through Justia, specifically the rigid-cage discussion and equations 26-31 in Batch 10 section 3A. The supplied file is a 29-page printout of the same Justia website, not the official typeset patent. It ends mid-discussion immediately before the derivative of the kurtosis term; the actual drawings and complete claims are absent. **Read in part from the supplied transcription**, with additional inspection of the potential functions and rendered equations. It does not resolve the outstanding original-publication verification request. The prior mathematical correction survives.

No earlier rulings are withdrawn. The QAD evidence strengthens several of them and supplies exact controlled experiments that were previously missing. The patent adds a second useful mathematical mechanism but does not establish an exact binary endpoint or any measured task retention at 1.7B. This addendum changes the evidentiary record only for these two sources. No model was loaded for inference, trained or evaluated.

## 1. Liquid AI QAD: What the full paper adds

### 1A. Exact training target and protocol

Source: supplied workshop paper, section 2, pages 2-3, Eq. 1; section 3 and appendix B.

The student is initialized from its own frozen BF16 parent. The objective is forward KL on assistant-response positions in chat-formatted sequences, conditioned on identical ground-truth prefixes, not on the student's free-running generations:

    L = E_x [(1/|M|) sum_(t in M) KL(p_teacher(.|x_<t) || p_student,q(.|x_<t))].

The simulated deployment map includes Q4_0 linear weights (32 entries per group), Q8_0 activations and Q6_K tied embeddings. The master weights are BF16; the student forward uses fake quantization and the backward uses STE for rounding. The final conversion is via llama.cpp. Consequently this is neither a uniform four-bit checkpoint nor an experiment on a binary embedding, binary gain or binary convolution kernel. It also is not a weight-only deployment experiment in our sense: activation quantization is part of its stated training map.

| Model | Reported original training tokens | Additional QAD tokens | Peak LR | QAD tokens / original tokens |
|---|---:|---:|---:|---:|
| 230M | 19T | 22B | 1e-6 | 0.116% |
| 350M | 28T | 10B | 3e-6 | 0.0357% |
| 1.2B | 28T | 22B | 3e-6 | 0.0786% |

All use AdamW, betas (0.9, 0.999), epsilon 1e-8, gradient clipping 1, distillation temperature 1, linear warmup then cosine decay. The paper does not give the complete internal instruction-mixture manifest, exact training sequence lengths, batch size, warmup length, optimizer weight decay, per-parameter trainability manifest or seed-level independent training results. The peak LR and token schedule differ by scale, so this is evidence for a family of related procedures, not a demonstration that literally identical hyperparameters transfer across architectures.

Evaluation uses five repeats at temperature 0.6, llama.cpp on AMD MI325X GPUs, and seven tasks. The tasks are GPQA Diamond, MMLU-Pro, IFEval, IFBench, Multi-IF, BFCLv4, and GSM8K for 230M/350M or AIME25 for 1.2B. Only GPQA Diamond, IFEval and IFBench are common to the 1.2B run and our ten-task ruler. Neither repeated decoding nor hardware profiling constitutes independent training-seed replication.

### 1B. Recalculated retention, not just percentage of gap recovered

Source: Table 1, p. 3, checked against appendix Tables 4, 7 and 10.

| Model | BF16 | PTQ Q4_0 | QAD Q4_0 | PTQ retention | QAD retention | Gain in retention points | Gap recovered |
|---|---:|---:|---:|---:|---:|---:|---:|
| 230M | 34.62 | 31.22 | 33.42 | 90.18% | 96.53% | 6.35 | 64.71% |
| 350M | 37.42 | 32.46 | 36.10 | 86.75% | 96.47% | 9.73 | 73.39% |
| 1.2B | 43.82 | 40.56 | 42.80 | 92.56% | 97.67% | 5.11 | 68.71% |

Formula: retention gain = 100*(QAD-PTQ)/BF16. Gap recovery = 100*(QAD-PTQ)/(BF16-PTQ). The 230M rounded cells imply 96.53% and 64.71% versus the table's 96.6% and 64.9%. These are consistent with independent rounding of underlying unrounded task means, not evidence of a substantive arithmetic error. The other two rows agree at the stated precision. In our terminology the measured 1.2B improvement is one five-point increment on their own suite, not a 68.7-point increment and not a Summit trophy.

Full 1.2B task breakdown from Table 10, p. 11 (paper's mean scores, points):

| Task | BF16 | Q4_0 PTQ | Q4_0 QAD | QAD - PTQ | QAD - BF16 |
|---|---:|---:|---:|---:|---:|
| GPQA Diamond | 36.26 | 33.56 | 32.44 | -1.12 | -3.82 |
| MMLU-Pro | 43.50 | 40.28 | 42.01 | +1.73 | -1.49 |
| IFEval | 86.45 | 84.64 | 86.36 | +1.72 | -0.09 |
| IFBench | 43.12 | 38.27 | 43.07 | +4.80 | -0.05 |
| Multi-IF | 60.72 | 57.88 | 59.92 | +2.04 | -0.80 |
| BFCLv4 | 24.04 | 23.64 | 23.88 | +0.24 | -0.16 |
| AIME25 | 12.67 | 5.67 | 11.93 | +6.26 | -0.74 |

AIME25 contributes 6.26 of the approximately 15.67 summed improvement points, about 40%. IFBench contributes another 31%. Tool calling contributes only 0.24. The recovery is highly heterogeneous. GPQA declines despite the aggregate increase, and also declines at 230M (26.20 to 24.95). Figure 2 makes these disparities visible. This is a concrete example supporting Round 1's separate aggregate-gain and per-task guardrail judgments. We cannot adjudicate noninferiority from these published summary statistics: the item-level paired outcomes and independent training replicates are absent.

Additional low-bit controls newly available from Tables 4 and 10: Unsloth UD-Q3_K_XL averages 27.98 vs BF16 34.62 at 230M (80.82%), and 38.79 vs 43.82 at 1.2B (88.52%). The appendix does not report these as trained ternary or 3-bit uniform models. The type label is not a complete effective-bit audit. At 1.2B, QAD Q4_0 (42.80) also exceeds the reported dynamic UD-Q4_K_XL (42.48) and ordinary Q4_K_M (42.43), while remaining below Q5_K_M (43.18). Figures 1, 4-7 show the deployment comparisons, with no independent benchmark of binary kernels. Table 13 uses the PTQ Q4_0 throughput measurements for QAD because the format and kernels are shared, rather than an independently timed QAD checkpoint. Distinguish inferred deployment equivalence from direct measurement.

### 1C. The decisive mechanistic control: preserving the original teacher, not just quantization robustness

Source: Table 2 and Figure 3, pp. 4-5.

| 350M arm | Seven-task average | Retention vs 37.42 BF16 | Teacher KL | Own-source KL | Relative weight error change |
|---|---:|---:|---:|---:|---:|
| Original PTQ | 32.46 | 86.75% | 0.870 | 0.870 | 0 |
| SFT then PTQ | 25.20 | 67.34% | 1.276 | 0.721 | -0.01% |
| QAT with CE | 28.30 | 75.63% | 1.050 | 0.619 | +3.31% |
| QAD with forward KL | 36.10 | 96.47% | 0.506 | 0.621 | +4.25% |

The authors match the data and training configuration for these controls. The quantization-aware CE and distillation arms have almost identical own-source KL, but radically different teacher-referenced KL and task scores. Relative improvement in teacher KL from PTQ to QAD is (0.870-0.506)/0.870 = 41.84%. The aggregate gain versus CE-QAT is 7.80 raw points, or 20.85 points of teacher-relative retention. Relative to original PTQ, QAD's weight reconstruction error increased rather than decreased.

Across sizes the paper reports 4.3-7.4% higher normalized squared weight reconstruction error, 40.3-53.6% lower original-teacher KL and about 20-29% lower own-source KL. Figure 3 shows the three quantities move differently. The KL estimates use 96 prompts drawn from the evaluated benchmarks with identical prefixes, not an independently drawn, broad held-out diagnostic corpus. This does not invalidate their comparison but limits the generalization of KL as a predictive ruler. The paper does not establish that reducing teacher KL monotonically improves every benchmark, or prove that the observed changes are mediated by a particular layer or channel.

**Ruling refinement:** Preserve both KL references for the QAD checkpoint-history control, but designate original-parent KL as primary for preservation of the original model. Own-source KL measures quantization sensitivity of the adapted FP checkpoint and can improve when the underlying capability is lost. Report both; do not use own-source KL alone to choose a checkpoint or stop training. Weight-only error is a geometry diagnostic, not a selection criterion for the product scoreboard. A controlled CE-QAT arm is worth specifying for Summit, with the identical training data and exact binary forward map. It is not necessary to choose CE as the principal objective.

### 1D. Exact quantizer matters even at the same nominal bit width

Source: section 4, Table 3, p. 6; duplicate rows in Table 10.

| Training map | Export Q4_0 | Export LPBQ |
|---|---:|---:|
| No adaptation | 40.56 | 40.78 |
| Q4_0 | 42.80 | 41.25 |
| LPBQ | 41.78 | 42.69 |

Both maps use symmetric four-bit blocks of 32. LPBQ has more restricted scale parameterization. Relative to each export's own PTQ baseline:

- Q4_0-trained model: on-target recovery +2.24; off-target +0.47, retaining 20.98% of the on-target gain.
- LPBQ-trained model: on-target +1.91; off-target +1.22, retaining 63.87% of the on-target gain.
- Off-target export losses relative to each on-target export are 1.55 and 0.91 raw points, respectively. Even export to the less constrained map loses quality.

A more expressive representation need not give a better result for a frozen checkpoint when the actual export algorithm chooses a different approximation. This is an empirical observation about quantizer mismatch, not a theorem about optimized representational capacity. It strengthens the Round 2 recipe-freeze and runtime-conformance rulings: training and packing must agree on signs, FP16 scale representation, zero handling, grouping, tied reuse and the activation arithmetic. The strict format cannot be approximated during training and silently replaced at evaluation. The QAD result supplies no direct evidence that a four-bit-adapted source will be easier to binarize.

The next weight-only analysis remains the paired original/adapted checkpoint comparison previously specified. Add a comparison of Q4_0 grid residual and strict g128 binary residual, and distinguish both from the later teacher and own-source KL analyses. No fresh teacher, target substitution, or retrospective choice of the more convenient denominator is authorized by this paper.

## 2. Caltech patent: correction and implications

### 2A. What this particular upload resolves

Source: supplied Justia printout, pp. 23-29, Eqs. 18-30. The paper printout describes illustrative weight histograms (Figs. 6 and 7) but does not reproduce those drawings. Described bimodality in one LLM layer, with peaks near +/-0.3, does not identify a complete model, exact grouping, held-out task score, training corpus or reproducible 1.7B result. There is no basis to award a product or science milestone for that description. The patent is a technical disclosure, not independent experimental verification.

Page 29's visually inspected rendering of Eq. 28 indeed gives the saturated branch alpha/epsilon times sign(x), and the unsaturated branch x. It is the same suspect formula seen in Batch 10. The file does not establish that the omission originated in the official typeset application. Do not attribute a verified typo to the inventors until the primary patent PDF is available. There is also a zero-vector edge case in Eq. 27: at w=0, the infinity-norm subdifferential is the entire closed unit L1 ball, not merely the unit L1 sphere. The distinction matters for initializing the dual.

### 2B. Exact rigid-cage inverse, endpoint and initialization

Source: Eq. 26-28, pp. 27-29. Independent derivation, consistent with Batch 10.

For a group of n=128, let psi(w)=||w||_infinity + epsilon*||w||_2^2/2 with epsilon>0. Its conjugate-gradient map is unique because psi is strongly convex, despite nonsmooth ties. For dual x:

    w = argmin_v [||v||_infinity + epsilon/2 ||v||^2 - x.v].

Fix cap r>=0. Then w_i = sign(x_i)*min(|x_i|/epsilon,r). Minimizing over r gives the derivative

    F'(r) = 1 - sum_i max(|x_i|-epsilon*r,0).

If sum_i |x_i| <= 1, the minimizer is r=0. Otherwise alpha=epsilon*r solves

    sum_i max(|x_i|-alpha,0) = 1.

Sort absolute dual values descending, a_1>=...>=a_n, and find the active count k with

    alpha = (sum_(i<=k) a_i - 1)/k,
    a_k >= alpha >= a_(k+1).

Then the correct unsaturated branch is x_i/epsilon, not x_i. The KKT condition on any strictly unsaturated nonzero component is x_i=epsilon*w_i. A counterexample is x=(3,0.1), epsilon=0.2: alpha=2, r=10, w=(10,0.5), not (10,0.1) and not binary.

For nonzero cap and all n coordinates attaining its magnitude, the exact condition is

    sum_i a_i > 1,
    (sum_i a_i - 1)/n <= min_i a_i,

or equivalently sum_i a_i - n*min_i a_i <= 1 together with sum_i a_i > 1. The endpoint condition depends on the spread of dual magnitudes, not merely on epsilon being small. It can be monitored per group directly. The resulting cap is still real-valued; FP16 rounding is a separate final error unless the cap already lies on the deployment scale grid.

For a released binary group w=s*b, b_i in {-1,+1}, s>0, an exact deterministic dual initialization is

    x_i = (epsilon*s + 1/n)*b_i.

Indeed x=epsilon*w+u, where u=b/n is a valid subgradient of the max norm at the tie. This reproduces the binary model at step zero. It avoids arbitrary random tie-breaking. Under a subsequent dual update x'=x-eta*g, the group may leave the common-magnitude region, and signs may remain frozen until a dual coordinate crosses zero. Thus step-zero exactness is not a convergence or sign-mobility guarantee. Store dual state throughout training and measure the fraction of exact endpoint groups, sign mobility, and the residual introduced by FP16 scale conversion. The method remains distinct from the fixed-norm shrinking cage, which geometrically enforces a terminal equal-magnitude constraint rather than hoping the mirror map saturates.

### 2C. An additional disclosed potential with a literal plateau

Source: Eqs. 23-25, pp. 26-27. This is not a newly invented Summit technique. The patent's joint-compression potential is separable:

    psi(w)=sum_i max(|w_i|^(1+delta), beta*|w_i|^q),
    0<delta<1, q>1+delta, beta>0.

The branches meet at m=beta^(-1/(q-1-delta)). For a positive coefficient, the left derivative there is L=(1+delta)*m^delta; the right derivative is U=beta*q*m^(q-1)=q*m^delta. Hence the dual-to-primal inverse has a plateau: any |x_i| in [L,U] maps to sign(x_i)*m. For |x_i|<L use (|x_i|/(1+delta))^(1/delta); for |x_i|>U use (|x_i|/(beta*q))^(1/(q-1)), attaching the dual sign to both branches. This is the proper inverse of the displayed max-of-powers potential. Unlike the rigid cage, the interval is componentwise and the magnitude is fixed by beta. All coordinates must reach the plateau to obtain an exact binary group. If a group's desired magnitude is s>0, selecting beta=s^(-(q-1-delta)) makes the plateau magnitude s. A fixed, exactly representable FP16 s gives an exact codec endpoint when all coordinates are within the plateau, but does not train scales. Changing beta dynamically changes the mirror potential and invalidates any theorem relying on a fixed potential unless separately established.

Useful design implication: an exact binary start can be placed anywhere in this dual interval by choosing a valid subgradient; placing it near the lower boundary makes it easier to move off the plateau than starting centrally. Neither choice guarantees a sign flip or task improvement. This gives a distinct candidate for future specification, not evidence of superiority over STE. The patent also describes a quartic-magnitude dispersion penalty in Eq. 29. Such a penalty can encourage equal absolute values, but zero weights also minimize it; without a task objective or norm constraint it cannot guarantee nonzero scales. The supplied PDF cuts off before the gradient expression. No certification of that missing expression is possible here.

## 3. Decisions affected and remaining blockers

- Round 2 Q3 (recipe definition and lock): strengthened by the controlled Q4_0/LPBQ result; freeze the actual numeric quantizer and all allowed adaptation rules, not merely bit width.
- Q8 (per-benchmark regression): strengthened by the GPQA regression despite QAD's mean gain. Do not declare a confirmed noninferior step from aggregate results alone.
- Q10 (QAD checkpoint-history control): unchanged in role, strengthened in evidentiary basis. Require original-teacher versus own-source fidelity separation; retain the two authentic FP denominators and the original-teacher preservation comparison as distinct estimands.
- Batch 10 mirror-descent audit: retain the corrected inverse and exact endpoint caveat. The supplied patent additionally motivates deterministic dual initialization and testing the max-of-powers plateau as a distinct method. Neither resolves exact task-preserving convergence.
- No change to strict format, gain exception classification, transfer target order, benchmark margins, or authorization to run models. No defensible new numerical probability of strict 1-bit success follows from these two files alone.

Remaining acquisition note for the first reviewer: the QAD PDF reading gap is closed at the paper level, not the private training implementation/data or weight-header level. For the patent, obtain the actual public typeset US20260220467A1 or WO2026161822A1 document with drawings and all claims, not another printout of Justia. Compare Eq. 28's unsaturated branch against the official original and inspect Figs. 6-7, including any stated model, axes and experiment conditions. The supplied copy was useful for visual confirmation of the transcription but does not close that outstanding acquisition item.
