# Batch 7: the two reviews compared

The first reviewer's findings are `batch-7-findings.md`. The second reviewer's document is filed as `batch-7-second-reviewer.md`. Each worked without sight of the other. What was taken from the second reviewer was checked at its source first, and the check is named.

## 1. Result

- The two reviews agree on the facts of the LFM2 models to the last weight: the same tensor table, the same totals, the same shares, the same block equations, the same four exact scale factors per channel in the convolution block, the same license reading, and the same figures for Liquid AI's 4-bit distillation.
- Neither found an LFM model trained or converted to 1 bit or three levels.
- They disagree on the target. The second reviewer keeps the original LFM2-1.2B as the transfer target and treats LFM3 as a different family that would change the hypothesis. The first recommends LFM3-1.7B with LFM2-1.2B as a second point. Both positions are set out in section 6 for the owner.
- They disagree on the depthwise kernels and normalization gains. The second reviewer wants every learned weight under the binary rule and offers a grouping for the kernels. The first leaves them in 16 bits as a declared exception. The reference runtime settles what the format does today: it does not quantize these kernels at any width (section 4B).
- The second reviewer read more of the LFM2 files than the first: all eight configuration files, the chat template, the report's result tables, the runtime's base code. The first read more of what surrounds LFM2: the LFM3 model code, Liquid AI's lowest-bit build, and three 1-bit and three-level papers on blocks of the same shape.
- Neither met the reading standard. The second reviewer says so at the top of its document, lists what is missing, and asks for an acquisition pass.

## 2. Depth of the second reviewer's read

| Read in full | Read in part | Not read |
|---|---|---|
| Eight configuration files (four LFM2, four LFM2.5); the LFM2-1.2B chat template, generation settings and license; the transformers configuration file; the runtime's shared LFM file; the distilled build's README and provenance file; the file lists of the official and community quantized repositories | The technical report (text, no figures); the transformers model file; the runtime's LFM2 file, converter and quantizer; Liquid AI's catalog and releases; Bi-Mamba; five other papers | The model files' headers; the tokenizer file; one paper beyond its abstract |

- Better than batch 6: the files that fix the target were read in full, and the document does not rest conclusions on the papers it read in part.
- Short of the brief: it returned with most papers read in part and no model file header read. It proposes a script that reads only the header of a model file and asks that the first reviewer run it.

## 3. Where the two agree

| Subject | Both find |
|---|---|
| LFM2 architecture | 16 blocks with attention at indices 2, 5, 8, 10, 12, 14 (30 blocks and 8 attention at 2.6B); widths 1,024, 1,536, 2,048; effective feed-forward widths 4,608, 6,912, 8,192, 10,752; heads of 64 over 8 key and value groups; kernel 3; vocabulary 65,536; tied embedding; no biases |
| Totals | 354,483,968; 742,489,344; 1,170,340,608; 2,569,272,320 |
| Shares in LFM2-1.2B | Feed-forward 68.81%, embedding 11.47%, attention 5.38%, convolution projections 14.34%, kernels 0.005% |
| The convolution block | A projection to three parts, a product, a causal depthwise filter, a second product, a projection out, with no activation function |
| Exact freedoms of the block | A common channel permutation; exchange of the two multiplied rows; four nonzero scale factors per channel with the inverse product in the output column |
| Groups of 128 | Every dense matrix dimension is a multiple of 128; the kernels and the small normalization vectors are not |
| Training | 10 trillion tokens at 4,096 then 1 trillion at 32,768; the LFM1-7B teacher with top-32 logits; the teacher for a conversion is the model itself |
| Tokens per weight | Lower for LFM2-1.2B than for Qwen3-1.7B; no conclusion about fragility follows |
| Harness dependence | Qwen3-1.7B scores 51.4 on GSM8K in Liquid AI's harness and 83.1 in PrismML's; published scores cannot be the denominator |
| License | Research, conversion and distribution of converted weights are permitted with the license attached and changes noted; commercial use below 10 million US dollars of annual revenue; nothing restricts publishing results |
| Liquid AI's 4-bit distillation | 97.1%, 96.5%, 97.4%, 96.6% kept; plain 4-bit rounding keeps 90.1%, 86.8%, 92.5%, 93.4% by the same arithmetic |
| Community builds | Importance-weighted rounding, no scores, none in our format |
| Bi-Mamba | 86.3%, 86.7%, 84.9% of the zero-shot average with both projections binary; the convolution and the embedding in full precision |
| The measurement | The 16-bit model scored on our own harness is the denominator; each model's own template and tool syntax; restoring one kind of tensor at a time to locate damage |

## 4. What the second reviewer found that the first did not

### 4A. Checked at source and confirmed

- The technical report's result tables. LFM2-1.2B: MATH-500 42.40, MMLU-Pro 19.71, Multi-IF 45.28, GSMPlus 36.09; LFM2-2.6B: MATH-500 63.60, GSM8K 82.41. Liquid AI's harness gives Qwen3-1.7B 70.00 on MATH-500. So five of our ten benchmarks have published LFM2 scores, MATH-500 among them; the first reviewer's findings listed these tables as not read.
- The full-precision weights behind Liquid AI's distilled 4-bit build are published. The `qad` directory of the LFM2.5-1.2B-Instruct quantized repository holds the 32-bit weights after distillation and before conversion, with a note to keep them in 32 bits and a statement that converting them with a named llama.cpp revision reproduces the released file byte for byte. No training details are given there. This is a pair of checkpoints with one architecture and one known difference, an adaptation to 4-bit rounding.
- The reference runtime's 1-bit type is 18 bytes per 128 weights: a half-precision scale and 16 bytes of signs. That is 1.125 bits per weight, the project's format.
- The reference runtime's quantizer skips the short-convolution kernel by name, with the comment that small convolution weights are not quantized. It does the same for Mamba's.

### 4B. What the last point settles

- The second reviewer argues that a claim of "every weight binary" must include the kernels and normalization gains, and that leaving them in 16 bits must not be discovered after a result. The second half is right and is adopted: the exceptions are written into the format before any run.
- The first half goes beyond the format the project measures against. In the runtime that defines that format, these kernels stay unquantized at every width, and by the second reviewer's read of the same file small vectors are handled separately. Whether PrismML's released 1-bit Qwen file keeps its normalization gains in 16 bits has not been checked here and is a check for S2. A 1-bit LFM file that keeps kernels and gains in 16 bits is therefore in the same format as the reference, at 1.1266 bits per weight overall for LFM2-1.2B.
- The stricter variant, kernels included, stays available as a separate labelled arm. The second reviewer's grouping for it is recorded as idea I28.

### 4C. Taken on its own reasoning, checked by hand

- Five points of retention is not the same number of score points on two teachers. On PrismML's Qwen table it is 29.1 summed points. On an LFM teacher with mean F it is half of F summed over ten tasks. The trophy threshold for LFM is computed from its own 16-bit scores.
- "Within five points" is an equivalence claim and needs an equivalence test: two one-sided tests against a margin of five points, with a paired resampling of questions that keeps the four score vectors together. A point estimate inside the margin with an interval that crosses it is inconclusive. Its worked example, about 3,400 independent questions for 80% power at a spread of 1.0, was recomputed and is right as arithmetic.
- More symmetries than the first reviewer listed: a signed permutation of the residual stream carried through every matrix, gain and the tied embedding; the limits that rotary positions and the small constant inside the normalization put on changes of basis for queries and keys. One correction to common practice follows: rescaling before a normalization is not exact when that constant is not negligible.
- A dense rotation across the gated channels is not an exact symmetry of the convolution block, by a short argument on the product of two rotated vectors. Rotation methods built for plain linear layers do not carry into that block.
- What "nothing changes but shapes" has to mean before a run: which settings are functions of shape, which of data, and whether a rule computed from the teacher's statistics is allowed. To be fixed before the Qwen recipe is frozen.
- The pinned commit and the hash of the weight file are two identifiers. A change to the tool template changes BFCL without changing the weights. Both are recorded.

### 4D. Taken as leads, not checked

- The second reviewer's revisions and hashes for LFM2-350M and LFM2-1.2B, the hashes in the provenance file, and its file sizes for community builds of the original models (a Q2_K file of LFM2-1.2B at 483 MB, about 3.3 bits per weight as a file).
- The LFM2.5 configuration files: the same shapes as LFM2 at 350M and 1.2B; a 128,000 vocabulary at 2.6B.
- A later Liquid AI table with the original LFM2-350M on BFCL v3 (22.95).
- A published 1-bit conversion that includes a parent which was itself distilled, at 86% to 88% of a zero-shot average with the embedding left out of the count.
- Two papers on training history and rounding, read by it in part.

## 5. What the first reviewer found that the second did not

- LFM3 from its own code: the block order, the head gates, the normalization after each sublayer, the kernel of 7, and the parameter table. The second reviewer lists LFM3 in its catalog and reads none of its files.
- That LFM3-1.7B and Qwen3-1.7B match in size, width and head size.
- Liquid AI's lowest-bit LFM3 build, which quantizes the feed-forward matrices only, and its distilled 4-bit LFM3 build.
- Three low-bit papers on blocks of the same shape besides Bi-Mamba, one of which uses groups of 128 with one scale each from a pretrained start and keeps 87% at three levels on about 100 million tokens; and a maker's mixed-precision 2-bit release of a hybrid that keeps its convolution weights in 32 bits.
- The one fitted law on training tokens and rounding damage, read in full; the second reviewer read its abstract.
- The spread of 17 points between families under one published 1-bit recipe, held from batch 6.
- PrismML's own ten-benchmark score for LFM2-1.2B, held in the plan. The second reviewer did not have it and lists six of the ten as unverified for LFM2.

## 6. Disagreements, held open

| Subject | First reviewer | Second reviewer | Note |
|---|---|---|---|
| The target | LFM3-1.7B, with LFM2-1.2B as a second point and LFM2-350M as the check | LFM2-1.2B, with LFM2-350M as the check; LFM2.5-1.2B-Instruct as the first extension; LFM3 afterwards as a third family | The second reviewer's case: one technical report covers the family, LFM2.5 gives a same-shape control, and the project named LFM2. The first reviewer's case: equal size with the Qwen reference, the maker's current model, a friendlier design. Both include LFM2-1.2B. The owner decides the order |
| Kernels and normalization gains | 16 bits, declared in advance | Under the binary rule, with a grouping for the kernels | Section 4B. The reference format leaves them unquantized; the stricter arm is kept as a labelled variant |
| A recipe at 70% to 80% on Qwen lands within five points on the LFM target | 32% | 40% (45% before) | The second reviewer's is for LFM2-1.2B with every weight binary; it lowered its figure on the kernel grouping problem. The first reviewer's weighs the spread between families |
| A 1-bit LFM keeps 70% of its own scores by any recipe | 40% | 60% (55% before) | The second reviewer leans on the shared feed-forward majority. Neither figure rests on a measurement at 1 bit with the embedding converted |

## 7. Errors

### 7A. The first reviewer's

- The report's result tables were left unread and listed as such. They hold LFM2 scores for MATH-500 and three other tasks that the findings should have carried.
- The full-precision weights behind the distilled 4-bit builds were missed. The findings said Liquid AI published no method; that stands, but the artifact that lets the effect be measured was one directory away.
- The low-bit community files for the original LFM2 models were not listed; only derivatives and later models were.
- The findings spoke of a five-point step on LFM without saying that its size in score points differs from Qwen's.
- The reference runtime's treatment of the kernel was not looked up, though it decides whether the 16-bit exception is part of the format. The second reviewer's read supplied it.
- The transfer claim was given no statistical test.

### 7B. The second reviewer's

- The reading standard was a condition of return and was not met; most papers were read in part.
- LFM3 was not opened. Its recommendation to treat LFM3 as outside the hypothesis was made without the facts in section 5.
- "The Low-Bit Quantization Favors Undertrained LLMs" paper was cited from its abstract, and the document declines to draw any direction from training history, where the paper's law gives one.
- It proposes binarizing the kernels while its own reading of the quantizer shows the reference format does not.
- Its two "before" probabilities are stated as reconstructed after the fact.
- It lists six of our ten benchmarks as lacking an LFM2 score. PrismML's whitepaper has all ten for LFM2-1.2B on one harness.

## 8. What is adopted

- The format's exceptions are written down before any run: depthwise kernels and one-dimensional tensors in 16 bits, as in the reference runtime, with the true overall bits per weight reported. A strict arm with the kernels binary is a separate labelled variant.
- The transfer claim is tested as an equivalence with a five-point margin, by paired resampling of questions, and the definition of "nothing changes but shapes" is fixed before the Qwen recipe is frozen.
- The step threshold on LFM is computed from the LFM teacher's own scores on the ruler.
- A control from public files: the same binarization applied to LFM2.5-1.2B-Instruct and to its 4-bit-adapted 32-bit weights, to see whether adaptation to 4 bits moves weights toward or away from the binary shell. Idea I27.
- The second reviewer's header-only script as the method for checklist row C9.
- Both identifiers are pinned: the repository commit and the weight file's hash.
- The published LFM2 scores from the report's tables are added to the findings.

## 9. Odds after the comparison

| Subject | After the first reviewer's findings | After the comparison | Why |
|---|---|---|---|
| A recipe that reaches a given retention on Qwen3-1.7B lands within five points on the LFM target | 32% | 33% | The reference format already allows the 16-bit kernels, which removes the grouping problem the second reviewer lowered its figure on. The equivalence test makes the claim harder to pass by chance |
| A 1-bit LFM at the target size keeps 70% of its own scores by any recipe | 40% | 45% | A second independent judgment at 60% from the shared feed-forward majority; a published conversion of a distilled parent at 86% to 88% on easy tasks, taken as a lead |
| Kernels and normalization gains in 16 bits are the only exceptions needed | 60% | 60% | |
| LFM3-1.7B converts at least as well as LFM2-1.2B under one recipe | 60% | 60% | |

## 10. Still open

- The owner's choice of target and order.
- The model files' headers, read by neither reviewer.
- The papers read in part by both, the figures of every source, and the list in section 8 of the first reviewer's findings.
- What the first reviewer did not read is taken up next, by the owner's instruction.
