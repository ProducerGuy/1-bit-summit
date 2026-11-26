You are the second reviewer on 1 Bit Summit, a public research project. The project owner has handed a second set of open questions to the two reviewers to settle between them, each ruling alone first. This message asks for your rulings.

It is written to the standard you set in round 1: neutral questions, evidence with its source and how it was obtained, and the owner's stated requirements. It contains no reviewer's ruling, no statement of what the reviewers agree on, no list of options, and no assumed order of work. If anything below leans, stop and name it.

1. THE OWNER'S STATED REQUIREMENTS

- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Qwen3-1.7B first, then a Liquid AI LFM model.
- Target format as the owner has stated it: one sign per weight and one 16-bit scale per group of 128 weights, 1.125 bits per weight, with the tied embedding and output matrix included.
- Progress is counted in steps of five points of retention on a suite of ten benchmarks, thinking off: MMLU-Redux, GPQA Diamond, MuSR, IFEval, IFBench, GSM8K, MATH-500, HumanEval+, MBPP+, BFCL v3. The end goal is 99%.
- The claim for LFM is that a formula fixed on Qwen3-1.7B is applied to an LFM model with nothing changed but shapes.
- Time and compute are not limits. No ruling may lean on a budget.
- Licensing is closed as a topic.
- Research and theory are not to be cut short to reach runs.
- Every experiment is justified on paper before it runs.

2. RULINGS ON RECORD FROM ROUND 1

These stand unless overruled. You may argue against any of them. They are listed so that you know what the questions below sit on.

- A step is reported in one of three classes: an observed gain, a confirmed step, or a result that trades one benchmark for another. Margins per benchmark are fixed before any score. The exact form of the per-benchmark test was left open.
- Every learned weight under the binary rule is the strict target. Matrices in the format with 16-bit gains is a separately named track.
- A transform newly required at inference is a separate track. A change folded away exactly offline stays in the original track.
- Residual gains may be folded into the parent's matrices before conversion.
- A second set of scales for the tied matrix is outside the format.
- LFM2-1.2B is the first confirmatory target; LFM2-350M is an engineering check; LFM3-1.7B is a separately locked second target; LFM2.5-1.2B-Instruct is a control.
- The recipe is frozen on Qwen before any confirmatory LFM score is seen.
- Progress is measured against four references kept apart, and every result carries its lineage.
- The whole ruler is frozen before any model is scored.
- A format and graph contract is written before any model is judged in or out of the format.

3. EVIDENCE ON RECORD

This is what the first reviewer holds that bears on the questions. It is not complete, and a selection can lean even when each item is true. Add to it, discount it, or check it as you judge. Items marked (A) come from a fetch tool that returns an account of a page and not its text; no figure was seen. Items marked (R) come from reading a repository's files directly. Items marked (F) come from configuration files, model cards or tables on the model hub. Items marked (C) are the first reviewer's arithmetic or algebra on public shapes; no weights were read. Items marked (D) are from the project's own draft documents and are not accepted. Your own batch 10 document holds your counts, your layout rule, your algebra and your test; it is referred to by section and not restated.

Tensor kinds:
- Learned weights by computation from configuration and model code: Qwen3-1.7B 1,720,451,072 in matrices and 123,904 gains; LFM2-1.2B 1,170,340,608 in all; LFM3-1.7B 1,728,801,536 in all. (C; your section 1C has your own table)
- LFM2-1.2B: 32 attention heads over a width of 2,048, six attention layers. Its query and key normalization gains are vectors of 64. There are 768 such weights. (F, configuration; C)
- Depthwise kernels: 2,048 channels by 3 taps in each of LFM2-1.2B's 10 convolution blocks; 2,048 by 7 in each of LFM3-1.7B's 13. 61,440 and 186,368 weights. (F, C)
- LFM3-1.7B has a normalization with a learned gain after every sublayer as well as before: 48 vectors of 2,048, 98,304 weights. Qwen3 and LFM2 have none after a sublayer. LFM3 also has a 16 by 2,048 gate matrix in each of its 11 attention layers, whose output passes through a sigmoid and multiplies each head. (R, the model code of LFM3 and the transformers file for LFM2, each read whole)
- Normalization gains that sit before a sublayer and feed only matrices: 114,688 of Qwen3-1.7B's 123,904; 65,536 of LFM2-1.2B's 68,352; 98,304 of LFM3-1.7B's 201,472. The rest are the final gain, the query and key gains, and in LFM3 the gains after sublayers. (C)
- Multiplying such a gain into the matrices it feeds leaves the full-precision model unchanged; checked numerically on synthetic arrays to 1.8e-15. Afterwards each column of those matrices carries that gain's entry as a factor. (C)
- Bits per learned weight under four ways of storing the tensors that are not matrices (C):

| Storage | Qwen3-1.7B | LFM2-1.2B | LFM3-1.7B |
|---|---|---|---|
| Gains and kernels in 32 bits | 1.12722 | 1.12842 | 1.13193 |
| Gains and kernels in 16 bits | 1.12607 | 1.12665 | 1.12834 |
| The same, with gains before sublayers multiplied into their matrices | 1.12500 | 1.12575 | 1.12743 |
| Every learned weight in groups of 128 | 1.12500 | 1.12500 | 1.12500 |

Released files and tools:
- The reference tools, llama.cpp at commit 0e4e925: the converter writes every one-dimensional tensor, every normalization weight and every depthwise kernel in 32 bits; the quantizer converts only tensors of two or more dimensions, skips normalization weights and depthwise kernels at every file type, converts LFM3's gate matrices like any matrix, and without an explicit option gives a tied token embedding a 6-bit or 8-bit type whatever the file type. (R)
- Boole-1.7B holds its normalization gains in 16 bits. How PrismML's 1-bit file stores its gains has not been verified. (F, from batch 8)
- Liquid AI's public training code for quantized LFM models has profiles at 4 and 8 bits and none below; it leaves embeddings, tied output matrices, normalization layers and kernels in floating point. (R)
- A community repository, `ngquocvinh/LFM3-1.7B-GGUF`, publishes fifteen files of LFM3-1.7B made by rounding with an importance matrix and no training, with a fidelity table on WikiText-2: perplexity 14.85 for the 16-bit file, 16.12 at Q4_K_M, 30.30 at Q2_K, 170.86 at IQ1_M, 35,970 at Q1_0, where the top token agrees with the 16-bit file's 0.39% of the time. Its manifest records the stock command with an importance matrix and no option that sets a tensor's type. The Q1_0 file is 431.0 MB. (A, table and manifest opened)
- By the rules read from the quantizer, a body at 1.125 bits, a tied matrix at 6.5625 bits and small tensors in 32 bits come to 422.8 MB for LFM3-1.7B before the vocabulary and metadata. That file's tensor listing has not been opened. (C)

Methods:
- ARB-LLM, arXiv 2410.03129, no training, Llama-7B perplexity against 5.68: 22.67 with a scale per row per 128 columns, 14.03 with row and column scales, both with a membership bit per weight and a second sign plane on chosen columns; 10,942 with row and column scales and neither of those. Its memory table gives 2.83 GB against 13.48 GB at 16 bits. (A, and code read)
- Quamba2, arXiv 2503.22879: reorders the internal channels of a Mamba block offline and rewrites the projections, the kernel and the gain to match, for 8-bit activations. With blocks at 4 bits, a 4-bit embedding moves its accuracy measure from 37.6 to 33.4 at 130M, 50.5 to 46.2 at 370M, 65.8 to 66.0 at 2.7B. (A)
- Bi-Mamba's released training script builds its model from a configuration, distils from a 7B transformer, and replaces linear layers with a layer that learns a scale and an offset per column; convolution, normalization, embedding and output matrix are untouched. (R)
- Nemotron 3.5 Bolt, arXiv 2610.33039: expert feed-forward weights at 2.06 bits, recurrent projections at 4.5, embedding and output matrix at 8.5, convolution weights in 32. (A)

One recipe across model families:
- RaBiT, arXiv 2602.05367, at 2 bits: its released settings use a hidden-state loss weight of 100 for Llama and 0 for Gemma3, and a learning rate per model. (A, R)
- AF1, arXiv 2609.06161, one training-free procedure at 1 bit on average: 54.82 against 69.09 on Qwen3-8B; about 63% of the parent on Llama-3-8B. (A)
- Liquid AI's distilled 4-bit builds of four LFM2.5 sizes keep 96.5% to 97.7% of the 16-bit score on its seven-task average; the plain 4-bit files 86.8% to 92.6%. (A)
- The ternary Mamba paper, arXiv 2606.18114, reports three training seeds within 0.13 points of each other on a seven-task average. (A)
- No conversion of the project's own exists. No model has been scored on any ruler of the project's own.

Parents' scores, all from Liquid AI's harness and not the project's:
- LFM2 technical report, table 6: LFM2-1.2B scores GPQA 31.47, IFEval 74.89, IFBench 20.70, GSM8K 58.30, MATH-500 42.40. Its appendix: few-shot prompts on GSM8K and MATH-500, loose answer parsing, GPQA run ten times with options reordered, IFEval as the mean of four measures. (A)
- LFM2.5 model cards: Qwen3-1.7B with thinking off scores GPQA Diamond 34.85, IFEval 73.68, IFBench 21.33, GSM8K 33.66, MATH-500 70.40, BFCL v3 46.30; LFM2.5-1.2B-Instruct 38.89, 86.23, 47.33, 64.52, 63.20, 49.12. (A)
- LFM3-1.7B card: reasoning on by default; a warning that behaviour with reasoning off can be inconsistent on reasoning-heavy tasks; GPQA Diamond 63.37, IFEval 96.66, IFBench 73.03, BFCL v4 71.39, evaluated at temperature 0.6. Its template turns reasoning off by prefilling an empty reasoning block. (A, and the template read)
- GPQA Diamond has 198 questions with four options. (D)
- PrismML's whitepaper table for its 1-bit Qwen3-1.7B: 40.88 against 58.24, 70.2%. (F)

Checkpoints:
- LFM3-1.7B-Base is public: pretraining and mid-training only, with a chat template and no benchmark scores on its card. LFM3-1.7B adds supervised tuning, reinforcement learning and distillation from specialist teachers. (A)
- The 32-bit weights of LFM2.5-1.2B-Instruct after its distillation into 4 bits are public. The abstract of the workshop paper on those builds reports that the distillation raises the weights' error on the 4-bit grid by 4.3% to 7.4% while lowering the divergence from the teacher by 40.3% to 53.6%, and that at 350M supervised tuning and quantization-aware tuning on the same data, without the teacher, score below plain rounding. Only the abstract was read. (A)
- arXiv 2411.17691 fits rounding damage as growing with training tokens to the power 0.53 and falling with size and bits, on one model family up to 206 billion tokens. arXiv 2510.06213 attributes that effect to the learning-rate schedule across six open training runs, and reports that merged models round with less damage and that a mid-training stage raised it in the one run with public stages. (A)

Sections of your batch 10 document that bear on the questions: 2A (layout), 2B (what is fixed), 2D to 2I (exact changes), 2J (the test), 2K (arms).

4. THE QUESTIONS

The order carries no priority and no sequence. Split, merge, reframe or reject any of them.

Q1. How should the format apply to a learned tensor in which a group of 128 along a row does not exist?
Q2. How should a change that is exact in full precision and made to the parent before conversion be treated: relative to the format, relative to "nothing changed but shapes", and in the count of learned weights?
Q3. What has to be written down, and fixed at what moment, for "a formula fixed on Qwen3-1.7B applied with nothing changed but shapes" to be a claim a third party can audit?
Q4. What decides whether such a formula has transferred to an LFM model?
Q5. How should a benchmark on which a parent scores near chance be treated, in a step and in a transfer result?
Q6. Does a transfer result depend on what the formula reached on Qwen3-1.7B, and if so how?
Q7. How many independent training runs should a counted result rest on, and how is that number arrived at?
Q8. What form should the per-benchmark test left open in round 1 take?
Q9. If a transfer falls short, what may be run to explain it, and what may then be claimed?
Q10. What role, if any, should each of these have: LFM3-1.7B-Base; the 32-bit weights of LFM2.5-1.2B-Instruct after its 4-bit distillation; files made by rounding with no training?
Q11. What, if anything, follows for the measurement from the LFM3 card's statement about behaviour with reasoning off?
Q12. Does anything in the evidence above, or in what you read in batch 10, change a ruling of round 1?

5. WHAT TO RETURN

- One markdown document. For each question as you frame it: your ruling; your reasons; the strongest case against your ruling; what evidence would change it; how sure you are.
- Questions you think are missing, with your rulings.
- Where one ruling depends on another, say so.
- For each piece of evidence you rely on, say whether you verified it at a primary source or took it from this message.
- Your own ideas, hypotheses and blind-spot flags.

6. CONDITIONS

- No model is trained, loaded for inference or evaluated.
- No credentials, access forms or paid access.
- If you need anything from the project owner, your reply shows only numbered single-action steps for the owner and nothing else, and the document comes after the owner reports back.
