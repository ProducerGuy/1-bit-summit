You are the second reviewer on 1 Bit Summit, a public research project. The project owner has handed a set of open questions to the two reviewers to settle between them, each ruling alone first. This message asks for your rulings.

An earlier version of this message was withdrawn after you stopped on it. You named eight places where it could steer you. All eight were right. This version is written to your standard: neutral questions, evidence with its source and how it was obtained, and the owner's stated requirements. It contains no reviewer's ruling, no statement of what the reviewers agree on, no list of options, and no assumed order of work. If anything below still leans, stop again and name it.

1. THE OWNER'S STATED REQUIREMENTS

- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Qwen3-1.7B first, then a Liquid AI LFM model.
- Target format as the owner has stated it: one sign per weight and one 16-bit scale per group of 128 weights, 1.125 bits per weight, with the tied embedding and output matrix included. Where the edges of that definition are unclear, they are among the questions below.
- Progress is counted in steps of five points of retention on a suite of ten benchmarks: MMLU-Redux, GPQA Diamond, MuSR, IFEval, IFBench, GSM8K, MATH-500, HumanEval+, MBPP+, BFCL v3. The end goal is 99%.
- Time and compute are not limits. No ruling may lean on a budget.
- Licensing is closed as a topic.
- Research and theory are not to be cut short to reach runs.
- Every experiment is justified on paper before it runs.
- The owner approved the order of runs you proposed in batch 9 "as an idea", with the words "We're scientists, not here to judge, here to learn." That is not approval of a plan or of a sequence.

2. EVIDENCE ON RECORD

This is what the first reviewer holds that bears on the questions. It is not complete, and a selection can lean even when each item is true. Add to it, discount it, or check it as you judge. Items marked (A) come from a fetch tool that returns an account of a page and not its text; no figure was seen. Items marked (R) come from reading a repository's files directly. Items marked (F) come from model files or model cards read in batch 8. Items marked (D) are from the project's own draft documents and are not accepted.

Scores:
- PrismML's whitepaper table for its released 1-bit Qwen3-1.7B: average 40.88 against 58.24 for the parent, 70.2%. (F, from the whitepaper text)
- A harness run by Boole's maker scored four models: parent 58.83; PrismML 1-bit 44.97; Boole-1.7B 50.55; PrismML's three-level 1.7B 51.57. It did not publish the parent's per-benchmark scores. (F, from a chart image supplied by the owner)
- PrismML's 1-bit model scores 34.9 on BFCL in PrismML's table and 67.4 on that harness. (F)
- No model has been scored on any ruler of the project's own.

The draft ruler (D):
- A draft ruler specification exists at `docs/ruler-spec.md`. It is not accepted. Every setting in it is open, including its BFCL setting, which in the current draft follows the outside harness (13 single-turn subsets, native function calling off) and not PrismML's.
- The draft computes sampling error from item counts alone: 0.7 to 3.9 points per benchmark, 1.2 points of retention for one model, 1.7 for the difference of two models scored as unrelated samples. Two of its item counts are assumptions. Two BFCL subsets have 16 and 18 items.

Released models:
- PrismML's 1-bit 1.7B: one sign per weight, one 16-bit scale per 128, one tied matrix. Its body signs match the parent's in 71.6% of positions and its tied matrix's in 99.93%, by an outside study's result file. Method unpublished. (F, R)
- Boole-1.7B: one sign per weight, a scale per 128; for the tied matrix one shared sign tensor and two scale tensors, one per role; about 1.148 bits per weight. Its card says a stored scale may have either sign and is used through an absolute value with a floor. Method unpublished. (F)
- Boole's file holds about 0.25 MB of normalization gains in 16 bits out of about 247 MB. (F, first reviewer's arithmetic) How PrismML's file stores its gains has not been verified.
- Normalization gains in Qwen3-1.7B are per-channel multipliers, 2,048 per normalization layer.

Rotation:
- PrismML's first-generation 1-bit format has no rotation; its second-generation three-level format has one. (F)
- Upstream llama.cpp applies that rotation at run time: a stored weight is W times D times H, D a vector of plus and minus ones per input width, H a normalized Hadamard matrix in blocks; the input of each such matrix is multiplied by D, then H; a tied model stores one rotated table. The loader accepts it for the Llama and Qwen families and not for LFM2. (R, read in an earlier batch)
- SDQ-LLM, arXiv 2510.03275, Llama3-8B: perplexity 2,434.87 with neither of its two additions, 20.13 with its Hadamard step alone. (A)
- LittleBit-2, arXiv 2603.00042, Llama3-8B at 1 bit per weight in factorized form: 16.30, 12.63 with a random rotation, 11.53 with a fitted one. The rotation sits between two factors and cancels in the product. (A)
- TWLA, arXiv 2606.13054, three levels, weights only, Qwen3-14B, C4 perplexity: 23.64 with its quantizer alone, 102.12 with its rotation alone, 17.26 with both. Its weights are rotated offline and the inverse is applied to activations at run time. (A)
- Section 2K of your batch 9 document derives when a rotation of the residual stream survives a tied matrix.

Training and starting points:
- BinaryLLM, arXiv 2508.06974: a map from weight to forward weight that is the identity at the start and is sharpened toward a sign over 20 stages; embedding and output matrix in full precision; zero-shot averages 42.8 against 49.1 (135M), 48.7 against 55.2 (1B), 57.0 against 65.0 (3B), 56.7 against 66.7 (7B). (A)
- The fine-tuning script of `usamec/double_binary`: a random tenth of matrices opened every 50 steps; in each, the top 1 in 100,000 entries by drift against their sign flipped per step. (R) Its paper, arXiv 2505.11076, reports Llama2-7B perplexity 9.57 without and 8.76 with that sign tuning. (A, from an earlier batch)
- "Strong freezing in binary perceptron models", arXiv 2610.06275: for one neuron with sign weights and random patterns, at every load, all but a vanishing share of solutions have no other solution within a fixed fraction of sign flips. One layer, random data. (A)
- RaBiT, arXiv 2602.05367 version 3, Table 4: Qwen3-1.7B at 2 bits, 60.38 against 64.21 on a zero-shot average. (A) Its released code leaves the embedding and output matrix in full precision and raises an error for fewer than two sign matrices. (R)
- NanoQuant, arXiv 2602.06694, Qwen3-8B ablation, perplexity: 206.03 from its start procedure alone; 15.07 with retraining of not-yet-converted matrices added; 13.58 with factor tuning added; 12.47 with a teacher step on scales alone added. Qwen3-1.7B at 1.00 bit in its factorized form: 19.21 against 9.39. (A)
- AF1, arXiv 2609.06161: training-free, factorized, 1.00 bit on average; seven-task averages 54.82 against 69.09 (Qwen3-8B), 59.61 against 72.47 (14B), 64.26 against 72.42 (32B). (A)
- ParetoQ, arXiv 2502.02631: trained from a pretrained model with the embedding and output layers unquantized; MobileLLM-1.5B eight-task average 55.9 at 1 bit against 62.7; saturation near 30 billion tokens at 2 bits and below. (A, and read with code in an earlier batch)
- Spectra, arXiv 2407.12327, trained from scratch, six-task averages for 16 bits, three levels, two levels: 44.3, 43.5, 39.8 (99M); 50.5, 48.4, 44.5 (560M); 54.9, 51.6, 47.1 (1.1B). (A)
- Section 1 of your batch 9 document analyses step zero, the first update and the end point of each training method.

Capacity:
- Section 3 of your batch 9 document holds your counting bound and your redesign of the capacity measurement.
- The measurement's current design is in `docs/research/batch-6-findings.md`, section 4D. It has not been specified or run.

LFM:
- LFM3-1.7B: released 27 October 2026; 1,728,801,536 weights by computation; 24 blocks (13 gated convolution, 6 global attention, 5 attention with a 256-token window); width 2,048; no technical report found. Liquid AI marks the LFM2 text models as deprecated in favor of it. (F, from model pages in batch 7)
- LFM2-1.2B and LFM2-350M have a technical report. LFM2.5 (January 2026) has LFM2's architecture. Liquid AI publishes the full-precision weights of LFM2.5-1.2B-Instruct after its distillation into 4 bits. (F)
- An idea named "everything binary" is in the project's ideas register at the owner's interest: every learned weight under the binary rule, depthwise kernels and normalization gains included. It is an idea, not a ruling.

3. THE QUESTIONS

The order carries no priority and no sequence. Split, merge, reframe or reject any of them.

Q1. What rule, if any, should govern a step in which the suite average rises while individual benchmarks fall?
Q2. What may serve as the starting point of training whose result is counted as a step?
Q3. How should a fixed rotation applied at inference be treated relative to the format?
Q4. How should a second set of scales for the tied matrix be treated relative to the format?
Q5. Separately from Q4: may a model that is outside the format be used as a starting point, a reference, both or neither?
Q6. What reference or references should progress be measured against?
Q7. Which LFM checkpoint or checkpoints should the LFM claim rest on, and in what roles?
Q8. How should normalization gains be treated relative to the format?
Q9. What has to be true before a specification for any model run is written? Is it true now for any run, and if so for which?
Q10. What has to be true before the capacity measurement moves from a design to a written specification? Is it true now?
Q11. What has to be settled about the draft ruler, its BFCL setting included, before anything rests on it?

4. WHAT TO RETURN

- One markdown document. For each question as you frame it: your ruling; your reasons; the strongest case against your ruling; what evidence would change it; how sure you are.
- Questions you think are missing, with your rulings.
- Where one ruling depends on another, say so.
- For each piece of evidence you rely on, say whether you verified it at a primary source or took it from this message.
- Your own ideas, hypotheses and blind-spot flags.

5. CONDITIONS

- No model is trained, loaded for inference or evaluated.
- No credentials, access forms or paid access.
- If you need anything from the project owner, your reply shows only numbered single-action steps for the owner and nothing else, and the document comes after the owner reports back.
