# Function-Preserving Binary Group Assignment

## 1. The overlooked variable: which 128 weights share a scale?

The target representation is one sign per weight and one FP16 scale per group of 128, with all matrix weights, including the tied embedding/output interface, covered:

\[
\hat w_i=s_g\operatorname{sign}(w_i).
\]

The error depends on more than which sign each weight gets. It also depends on which other 127 weights share the scale. For one fixed group of 128 and ordinary squared weight reconstruction, the optimal positive scale is the mean absolute magnitude, giving:

\[
E_g=\sum_{i\in g}w_i^2-\frac1{128}\left(\sum_{i\in g}|w_i|\right)^2.
\]

Consider two groups, each having 64 entries of magnitude 1 and 64 of magnitude 10. Their combined minimum error is **5,184**. If those same 256 weights could instead be assigned so one group contains all 128 magnitude-1 values and the other all 128 magnitude-10 values, the minimum weight reconstruction error would be **zero**. This is an analytic illustration, not a result on an LLM. In actual models one cannot freely reorder all weights without changing the function.

## 2. Exact function-preserving permutations in SwiGLU

For a SwiGLU feed-forward layer

\[
f(x)=W_d[\operatorname{SiLU}(W_gx)\odot(W_ux)],
\]

any common permutation matrix \(P\) on the hidden feed-forward neurons induces an exact algebraic reparameterization:

\[
W'_g=PW_g,\qquad W'_u=PW_u,\qquad W'_d=W_dP^\top.
\]

This preserves the full-precision function while changing the order of columns in \(W_d\), and hence which weights share each row's contiguous g128 groups. The permutation may be folded into tensors before packing: **no new deployed matrix, persistent permutation table, or inference operation** is needed for that block. Additional residual-channel permutations are possible with all attention, embedding, normalization and tied-head transformations performed consistently. RoPE/head/grouped-query constraints must be respected; an arbitrary attention permutation is **not** automatically a symmetry.

The new optimization variable is the valid permutation itself. We can search over equivalent full-precision networks and choose the one whose **entire binary-converted network**, not just its individual tensors, best preserves the teacher. A permutation selected from local weight MSE may not improve benchmark retention. Nor is the search guaranteed to yield any improvement once stronger rotations, scale optimization, and recovery training are included.

## 3. Prior evidence and precise boundaries

- [PermuQuant, 2026](https://arxiv.org/abs/2605.09503): channel reordering and rotation improve fixed-bit *diffusion* quantization; one reported GenEval comparison is 0.68 to 0.80 in a three-bit setting. These are neither language model results nor exact 1.125-bpw signed binary.
- [Reversible coordinate permutations in pretrained TinyLlama](https://huggingface.co/blog/nmicic/int-llm-coordinate-permutation): shows a practical family of symmetries including SwiGLU neurons and carefully constrained attention/head rearrangements at 1.1B; it does not establish a 1-bit retention gain.
- [Transforms for LLM Quantization: The Great Inversion and Format Co-Design](https://arxiv.org/abs/2608.25188): broader review of quantization transforms, supporting deployment-format-specific choice rather than assuming a good FP16 reconstruction transfers directly to one-bit inference.
- [ThinkBit, 2026](https://arxiv.org/abs/2610.34886): two-bit codeword search and scale calibration with Qwen3-1.7B reasoning results; the method and scores do not meet a one-sign g128 format.

These links are antecedents. The proposed **full-model fixed-g128 group-assignment objective** is a specific hypothesis, not an established breakthrough or a verified novelty claim.

## 4. A quantitative, falsifiable prediction

Subjective probability estimates before Qwen measurement:

| Target outcome on Qwen3-1.7B at fixed strict binary precision | Probability |
|---|---:|
| Measurable improvement over a matched, non-permuted baseline | 50% |
| At least +5 percentage points of benchmark retention over that baseline | 20% |
| At least +5 points **on top of** a strong rotation-and-recovery baseline | 10% to 15% |

The decisive evidence must compare the exact same original teacher, fixed ten-benchmark suite, training tokens and compute, sign and scale format, and tied embedding policy. Include random-permutation controls and a separately selected permutation. Measure numerical full-precision equivalence before conversion, final deployed bit count, inference runtime and loss on individually reported benchmarks. The probability estimates are judgments, not frequencies estimated from past experiments.

## 5. Larger hypothesis: optimize an equivalent model before quantization

Rather than only asking for the signs and scales closest to a fixed pretrained tensor, solve:

> Among all exact, functionally equivalent parameterizations that fit in the permitted deployment format, which can be binarized and *subsequently trained* most effectively?

The distinction is between (a) an initialization that minimizes instantaneous reconstruction error and (b) one whose binary signs have a favorable optimization trajectory after continuation. Earlier work on sign-flip inertia and cross-layer compensation warns that these objectives need not agree. This creates a joint research direction spanning U2 (retention per compute), P3 (leading recipe), U5 (co-adaptation) and CH1 (budget), while requiring zero additional inference bits after folding.

**Status:** mathematical mechanism established for certain layer symmetries; +5-point efficacy entirely unmeasured. The hypothesis deserves comparison against existing rotation and student-input compensation, not a product milestone in advance.
