# Reviewer prompt, batch 10

The task given to the second reviewer for batch 10. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights along a row (1.125 bits per weight), with the embedding and output matrix included and tied. The formula is proven first on Qwen3-1.7B, where a published 1-bit model of the same format exists to measure against (PrismML's 1-bit Bonsai 1.7B), and then on a Liquid AI LFM model.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision parent's average, same suite, same settings. The suite is ten benchmarks, thinking off: MATH-500, BFCL v3, MMLU-Redux, GSM8K, MBPP+, HumanEval+, GPQA Diamond, IFEval, MuSR, IFBench. The end goal is 99%.
- Decisions already recorded by the project, given so you know where things stand. You may argue against any of them:
  - The strict target is every learned weight in the binary format. A second, named track keeps the matrices binary and leaves normalization gains in 16 bits.
  - A transform that must run at inference is a separate track. A change that can be folded into the stored weights exactly, offline, is allowed.
  - Order of LFM models: LFM2-1.2B is the first confirmatory target, LFM2-350M is an engineering check, LFM3-1.7B is a second target locked separately, LFM2.5-1.2B-Instruct is a control.
- Time and compute are not limits on this project. Do not rule out or discount any route because of what it costs to train or to read.
- The project is open, public research. Licensing is settled and needs no work from you.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, proved this or measured this, and bring back what you find.

ITEM 1. LFM3 in depth
Problem: LFM3-1.7B is the same size as Qwen3-1.7B and is one of the project's two LFM targets. Liquid AI has published no technical report for LFM3. What is public is spread over a release post, model cards, model code, runtime code and quantized builds, and the project has not put it in one place or checked it line by line. The project also holds one control it has not examined: Liquid AI publishes full-precision weights of LFM2.5-1.2B-Instruct as they stand after its distillation into 4 bits.
Starting sources, each in full, every file of each repository included:
- LFM3 release: https://www.liquid.ai/blog/lfm3 and https://huggingface.co/blog/LiquidAI/lfm3
- https://huggingface.co/LiquidAI/LFM3-1.7B with its card, configuration, model code, tokenizer files and chat template; https://huggingface.co/LiquidAI/LFM3-1.7B-Base; every other LFM3 repository Liquid AI has published
- Liquid AI's quantized builds of LFM3 (GGUF, NVFP4 and any other) and the listing of community quantized versions: https://huggingface.co/models?other=base_model:quantized:LiquidAI/LFM3-1.7B
- Runtime support: llama.cpp (the LFM3 and LFM2 model files, their conversion scripts, the quantization code and the 1-bit block type), mlx-lm, transformers
- Liquid AI's distilled 4-bit builds: https://www.liquid.ai/blog/qad , with the repositories it links, the adapted full-precision weights included
- The LFM2 technical report, arXiv 2511.23404, and the LFM2, LFM2.5 release posts and model cards, for what LFM3 changed
- Liquid AI's documentation: https://docs.liquid.ai/lfm/models/text-models
What we need you to find:
- The exact computation graph of LFM3-1.7B from the released code: every kind of block, every learned tensor by kind, shape and count, the total by kind, and which tensors are matrices, which are convolution kernels, which are gains, gates or anything else. The same for LFM2-1.2B, and a line-by-line list of what differs between the two.
- What is published about how LFM3 was trained: data, token counts, stages, any distillation or reinforcement step, context length, and anything stated about design choices made with quantization in mind.
- The tokenizer, the chat template and the tool-call format, as they bear on running the ten benchmarks.
- Reasoning: how thinking is switched on and off, what the model card says about each mode, and how a score with thinking off should be taken so that it is comparable with the Qwen3 runs. Which of the ten benchmarks have published LFM3 scores, in which mode, by which harness, and which have none.
- What each runtime does with each kind of LFM3 tensor when it quantizes: converted, left in 16 bits, or left in 32. What the 1-bit block type in llama.cpp would and would not cover on an LFM3 file.
- Every published measurement of LFM3 or LFM2 at low bit widths, official or community, with its scores, and what it shows about which tensors are sensitive.
- The 4-bit-adapted weights: what exactly is published, how the adaptation was done as far as it is stated, what differs between the adapted and the original weights that can be known without loading them, and what the project could learn from the pair with weights only.
- What is unknown about LFM3 that the project needs, and the cheapest way to learn each.

ITEM 2. The transfer rule in writing
Problem: the project's claim is that a formula fixed on Qwen3-1.7B is then applied to an LFM model with nothing changed but shapes. That sentence is not defined anywhere. Nothing says which things count as shapes, which settings may be re-derived from the new model and which must be carried over as numbers, what is done with tensors that Qwen does not have, or what result counts as the transfer having worked. Without that, a success cannot be claimed and a failure cannot be attributed.
What the project holds, for you to test, not to accept:
- LFM models contain kinds of learned tensor that Qwen3 does not, as read from their released code. You should establish the list yourself under item 1.
- Seven ideas, each a claim that has not been run. For each, we want the algebra checked against the released model code, the conditions under which it is exact, what breaks it, what it is worth on paper, and how it could be tested with weights only.
  - a. Closing by a fixed group norm: while a per-group cap on magnitudes is lowered, hold each group's Euclidean norm fixed, so that the group ends with all magnitudes equal to the cap and nothing is left to round. Asked here: whether this applies unchanged to every kind of tensor in an LFM model.
  - b. In LFM's convolution block there is no nonlinearity between the projection in, the depthwise kernel and the projection out, so per-channel factors and signs can be moved among the three with their product held at one. That would give the projection out a free factor per column.
  - c. LFM3 normalizes the output of every sublayer with a learned gain per channel. Those gains could be trained together with the group scales in a stage that changes no sign.
  - d. The 4-bit-adapted weights of LFM2.5-1.2B-Instruct as a control: put the original and the adapted weights through the same group binarization and compare the error.
  - e. If the depthwise kernels are put in the binary format: fold each channel's overall size into the block, order channels by the shape of their taps, permute the block consistently, and form groups of 128 across channels tap by tap.
  - f. Everything binary: every learned tensor under the binary rule, kernels and gains included, with nothing left in 16 bits.
  - g. Folding gains away before conversion: where a normalization gain feeds only matrices, multiply it into those matrices in the parent, so that the gain becomes one and needs no storage.
What we need you to find:
- A written transfer rule that a third party could apply and audit. It should say, item by item, what is carried over from the Qwen run as a fixed number or a fixed procedure, what is recomputed from the target model by a procedure fixed in advance, and what may not be touched. Cover at least: the format and its grouping, the order of operations, every training setting, the data, the teacher, the stopping rule, the evaluation settings, and the handling of each tensor kind.
- For every kind of tensor in LFM2 and LFM3 that Qwen3 lacks, and for the tied matrix and the normalization gains in all three: how the format applies to it, with the bits it costs, and what the alternatives are. State where a group of 128 along a row is not defined and what replaces it.
- What the released 1-bit files of the Qwen3-1.7B parent actually store for tensors that are not matrices (PrismML's Bonsai file and Precision Numerics' Boole file), as far as can be read from their listings, headers, loaders and cards.
- The test that decides whether a transfer worked: the quantity compared, the margin, how many runs, which model's result is the reference, and how benchmarks on which the LFM parent itself scores near chance are treated. Say what your test would wrongly pass and wrongly fail.
- If a transfer falls short: the smallest set of extra arms that would put the shortfall down to one cause (the new tensor kinds, the embedding, the parent's own training, the data, the settings), and what each arm costs in claims.
- Published cases where one low-bit recipe was applied unchanged across model families, with the spread of results between families.
- For each of the ideas a to g: your verdict, with the derivation.

ITEM 3. Sources that earlier batches read only in part
Problem: parts of the project's plan rest on sources that one or both reviewers read in part in batches 6 and 7. No reviewer saw the figures of most of them. A partial reading can miss the assumption, the appendix table or the line of code that changes what a source supports.
The sources, grouped by the question each bears on. Each in full: every section, table, figure, proof and appendix, and the released code where it exists.
- 3A. Does a mirror-descent or implicit-bias argument say where training under a chosen potential ends, and does it hold for a network and a two-value target? arXiv 1906.03830; 2202.10788; 2510.16250; 2602.18997; 2402.10474; 2311.02270; 1910.08237 with its code https://github.com/kartikgupta-at-anu/md-bnn ; the patent publications US20260220467A1 and WO2026161822A1.
- 3B. What is proved about rounding weights one at a time while correcting the error, and about representations with equal-magnitude coefficients? arXiv 1401.3420; 2010.15979 with its code https://github.com/elybrand/quantized_neural_networks ; 2201.11113; 2309.10975; 2505.11695; 2508.04853; 2406.00800 with its code https://github.com/AozhongZhang/MagR ; 2609.32659 with its code https://github.com/1733116199/cewt ; the survey arXiv 2608.25188.
- 3C. What do published low-bit conversions and trainings report at small sizes, and with what method? arXiv 2607.14630; 2505.11076; BiLLM, arXiv 2402.04291; OneBit, arXiv 2402.11295; ARB-LLM, arXiv 2410.03129, with its code https://github.com/ZHITENGLI/ARB-LLM ; 1702.03044 with its code; 2001.01091; 2107.01400.
- 3D. Where does low-bit damage sit and what predicts it? arXiv 2609.01587; 2606.03002; 2609.32902; 2505.24832; 2401.15092; 2411.17691; 2411.04330; 2510.06213.
- 3E. LFM2 and its relatives: the LFM2 technical report, arXiv 2511.23404, tables for every modality included; the transformers LFM2 model file whole; the llama.cpp LFM2 model file, conversion script, quantization code and block definitions whole; the mlx-lm LFM2 implementation; the LFM2.5 model cards; the tokenizer files and both chat templates as text; the safetensors headers of LFM2-1.2B and LFM2-350M if you can reach them.
- 3F. Binary and three-level state-space and convolution models: arXiv 2411.11843 with its code https://github.com/Tangshengku/Bi-Mamba ; 2606.18114; 2606.10932 with its code https://github.com/cs-cmyk/df-ssm ; 2610.33039; 2511.17633; 2005.06305; Quamba2.
What we need you to find:
- For each source: what it proves or shows on its group's question, with the assumptions and the numbers, and what its figures and its code add to or take away from the text.
- For each source: anything in the parts a quick reading would skip (an appendix, a footnote, a figure, a default in the code) that limits or reverses its headline claim.
- For each group: your answer to the group's question for a 1.7B decoder in the project's format, separating what is proved, what is measured and what you infer.
- Any source in these groups that has been superseded, corrected or contradicted since, with the later source.

READING STANDARD, A CONDITION OF RETURN
- Every source named in this brief, and every source a conclusion of yours rests on, is read in full from its primary file: all sections, tables, figures, proofs, appendices, and the released code, notebooks and configuration where they exist. Abstracts, index pages, search snippets and other people's summaries do not count as reading.
- Code is part of a source. Where a repository exists, open it and check the written claims against it.
- If a source resists, try other routes until one works. If it still cannot be read in full, list it at the very top of your document under "Not read in full", with every route you tried, and build no conclusion on it.
- Before you return, check every label. If most of your sources are not read in full, the brief is not met; keep reading instead of returning.

FREEDOM
- Use any route to a source: another URL for the same document, an HTML version, a mirror, the code repository, the authors' pages, works that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing and its recorded decisions are wanted. Flag blind spots.
- You may write and run small scripts that check a derivation or a count numerically, or that read public files, listings and model file headers. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count; say which sources are behind such a gate.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- every derivation written out so it can be checked line by line
- your answer to what the item asks you to find
- what is still unknown and the cheapest way to find out
Then four probabilities, each before and after this batch, as numbers with your reasons. State the "before" figure first, before you read, and keep it.
- that a formula fixed on Qwen3-1.7B and applied under your transfer rule lands on LFM2-1.2B within five points of the retention it reached on Qwen3-1.7B
- the same for LFM3-1.7B
- that a 1-bit model of Qwen3-1.7B in the project's format can reach 90% retention on the ten benchmarks by some training
- that it can reach 99%
Then a short closing section: anything across the three items that the project should do differently. New ideas go in that section, not in a second document.

HOUSE RULES
- Separate what a source proves or shows from what you infer.
- No claim that nobody has done something unless you searched and say where.
- Probabilities are judgments and are given as numbers. No time estimates, and no conclusion that rests on a training or reading budget.
- Plain markdown, no em dashes, sections numbered 1, 1A, 1B.
- If you need the project owner to do something, reply with only the numbered steps, one action per line, and nothing else. Results come after he reports back.

BEFORE YOU START
If anything in this brief looks wrong, unclear, badly aimed or leading, say so first and then proceed with your best reading.

STOP
Stop after the one document.
```
