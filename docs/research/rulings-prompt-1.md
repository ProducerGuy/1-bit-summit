You are the second reviewer on 1 Bit Summit, a public research project. The project owner has handed nine open decisions to the two reviewers to settle between them. This message asks for your ruling on each, reached on your own. The first reviewer's rulings are withheld from you on purpose. Nothing below is meant to steer you: it lists facts and options. If you think an option is missing, a decision is framed wrongly, or a decision is absent from the list, say so and rule on your version.

THE PROJECT

- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Qwen3-1.7B first, then a Liquid AI LFM model.
- Format as it stands: one sign per weight, one 16-bit scale per group of 128 weights, 1.125 bits per weight, the tied embedding and output matrix included as one stored matrix.
- Progress is counted in steps of five points of retention on a fixed suite of ten benchmarks (MMLU-Redux, GPQA Diamond, MuSR, IFEval, IFBench, GSM8K, MATH-500, HumanEval+, MBPP+, BFCL v3), thinking off. Retention is the student's ten-benchmark average over the parent's on the same harness. One step is about 29 summed points. The end goal is 99%.
- The owner's standing rules: time and compute are not limits and no ruling may lean on a budget. Licensing is closed as a topic. Research and theory are not to be cut short to reach runs. Every experiment must be justified on paper before it runs. The owner has approved your proposed order of runs from batch 9 as an idea to learn from.

FACTS ON RECORD

Scores:
- PrismML's own table: its released 1-bit Qwen3-1.7B averages 40.88 against 58.24 for the parent, 70.2%.
- One outside harness (run by Boole's maker) scored four models: parent 58.83; PrismML 1-bit 44.97, 76.4%; Boole-1.7B 50.55, 85.9%; PrismML's three-level 1.7B 51.57, 87.7%. It did not publish the parent's per-benchmark scores.
- The two harnesses differ most on BFCL: PrismML's 1-bit model scores 34.9 in PrismML's table and 67.4 on the outside harness. The project's ruler uses the outside harness's BFCL setting.
- No model has been scored on the project's own ruler yet. The ruler is written and not yet accepted.
- Sampling error of the ruler from item counts alone: 0.7 to 3.9 points per benchmark (smallest for MMLU-Redux, largest for HumanEval+), 1.2 points of retention for one model, 1.7 for the difference of two models scored as unrelated samples. Two BFCL subsets have 16 and 18 items and each carries one thirteenth of the BFCL score.

Released models:
- PrismML's 1-bit 1.7B is exactly in the format above. Its method is unpublished. Its body signs agree with the parent's in 71.6% of positions; its tied matrix's signs agree in 99.93%.
- Boole-1.7B stores one sign per weight with a scale per 128, and for the tied matrix one shared sign tensor with two scale tensors, one per role. That is about 1.148 bits per weight. Its card says a stored scale can have either sign and is used through an absolute value with a floor. Its method is unpublished.
- Both released models keep normalization gains in 16 bits, to the first reviewer's reading of their files; treat that as unverified for PrismML's.
- The published RaBiT paper (version 3) trains Qwen3-1.7B at 2 bits and keeps 60.38 of 64.21 on easy tasks. Its released code leaves the embedding and output matrix in full precision and refuses a single sign matrix.

Rotation:
- PrismML's first-generation 1-bit format has no rotation. Its second-generation three-level format has one.
- Upstream llama.cpp now applies that rotation exactly at run time: a stored weight is W times D times H, with D one vector of plus and minus ones per input width and H a normalized Hadamard matrix in blocks; the graph multiplies each such matrix's input by D, then H; a tied model stores one rotated table for both roles. The loader accepts it only for the Llama and Qwen families, not for LFM2.
- A fixed rotation of this kind adds no stored bits beyond its sign vector and adds a transform at inference.
- Published effects of a rotation before rounding: SDQ-LLM on Llama3-8B, perplexity 2,435 without a Hadamard step and 20 with it; LittleBit-2 on Llama3-8B at 1 bit, 16.30 to 12.63 from a random rotation between its factors; TWLA at three levels on Qwen3-14B, 23.64 with its quantizer alone and 17.26 with its rotation added.
- Your own batch 9 algebra: a rotation of the residual stream survives a tied matrix with a final gain only as a signed permutation unless the gains are equal.

Training, from batch 9, agreed by both reviews:
- Scale-only training from a file already in the format is exact at step zero and in the format at every step.
- Straight-through training from such a file is exact at step zero; with the scale as its own parameter the latent margin is a free setting.
- A sign budget is in the format at every step. A public script flips about one sign in a million per step; its sign tuning took a factorized 7B model from perplexity 9.57 to 8.76.
- From the parent, a teacher loss alone has a zero first gradient. A published smooth map sharpened from zero (BinaryLLM) starts at the parent and kept 85% to 88% of easy-task averages from 135M to 7B with the embedding in full precision.
- For one neuron with sign weights and random patterns, almost every solution is isolated from every other; training finds rare connected ones (arXiv 2610.06275).
- Published scale-only results: accuracy flat after about two thousand sequences at 2 bits on 7B (EfficientQAT); a quarter of a million tokens moved a 3B model at 1 bit by 6 points (AF1); NanoQuant's scale-only teacher step took Qwen3-8B from perplexity 13.58 to 12.47.

LFM:
- LFM3-1.7B: released 27 October 2026, 1,728,801,536 weights, 24 blocks (13 gated convolution, 6 global attention, 5 attention with a 256-token window), width 2,048, no technical report. Liquid AI marks the LFM2 text models as deprecated in favor of it.
- LFM2-1.2B and LFM2-350M have a technical report. LFM2.5 (January 2026) has the same architecture as LFM2. Liquid AI publishes the full-precision weights of LFM2.5-1.2B-Instruct after its distillation into 4 bits.
- The owner earlier took up the idea "everything binary": every learned weight under the binary rule, depthwise kernels and normalization gains included.

THE NINE DECISIONS

1. Can a step be bought by trading one benchmark for another? Options on the table: a step does not count if any one benchmark falls by more than twice the standard error of its paired difference; or no benchmark may fall below the previous step at all.
2. Where does the first step start? Options: PrismML's released 1-bit 1.7B; or only models the project converts itself; or both in some stated relation.
3. Is a fixed rotation inside the format or a change of format?
4. Is a second set of scales for the tied matrix inside the format (about 1.148 bits per weight, as Boole ships) or not (1.125)? This also decides whether Boole counts as a model at the project's format and whether it may be a starting model.
5. Which model do the five-point steps count from? Options: PrismML's 1-bit 1.7B; or the best released model at the format that the project's ruler confirms.
6. Which LFM checkpoint is the target of the claim, and which are second points or engineering checks? Your batch 7 recommendation is on record; keep it or change it, and say what in the facts above moved you or did not.
7. Do normalization gains stay in 16 bits in the strict format, or is everything binary the target? If one is the target, what is the other?
8. May the specification for the first model run (scale-only training of the released 1-bit 1.7B: signs frozen, group scales and normalization gains trained against the parent's output distribution) be written now, while the LFM reading of batch 10 goes on, or do all specifications wait until batch 10 is done?
9. The small capacity measurement (two-level weights on synthetic facts, as criticized by both reviews in batch 9): is its specification written now, to run only on the owner's later approval, or does it stay a design?

WHAT TO RETURN

- One markdown document. For each of the nine: your ruling in one line; your reasons; the strongest case against your ruling; what evidence would change it; and how sure you are.
- Any decision you think is missing, with your ruling on it.
- Where a ruling depends on another, say so.
- Push back on this message wherever a fact looks wrong, incomplete or slanted. Name it and say what you would need to check it.
- Your own ideas, hypotheses and blind-spot flags are wanted, not only answers to the nine.

CONDITIONS

- Reason from the facts above, your own earlier documents, and anything you verify at a primary source. Mark what you verified and what you took from this message.
- No model is to be trained, loaded for inference or evaluated.
- No credentials, access forms or paid access.
- If you need anything from the project owner, your reply shows only numbered single-action steps for the owner and nothing else, and the document comes after the owner reports back.
