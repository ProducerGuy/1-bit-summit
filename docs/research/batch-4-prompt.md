# Reviewer prompt, batch 4

The task given to the second reviewer for batch 4. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included. Qwen3-1.7B first, Liquid AI LFM2 after.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The outside reference at our exact format is PrismML's 1-bit Bonsai 1.7B. Its published scores, thinking off, ten benchmarks (table 9 of 1-bit-bonsai-8b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo), teacher then 1-bit:
  MATH-500 74.0 / 34.4
  BFCL v3 71.8 / 34.9
  MMLU-Redux 66.8 / 43.2
  GSM8K 83.1 / 66.3
  MBPP+ 58.2 / 42.3
  HumanEval+ 57.3 / 45.1
  GPQA Diamond 32.5 / 20.7
  IFEval 70.3 / 63.0
  MuSR 50.1 / 45.1
  IFBench 18.3 / 13.8
  Average 58.24 / 40.88, retention 70.2%. A step of five points is 29.1 summed score points across the ten.
- What we want now: the next five points of retention at this size and format, and an understanding of what the conversion breaks.

THIS BATCH: THREE ITEMS
Each has a question that must be answered. How you get there is up to you.

ITEM 1. Which decisions low-bit conversion breaks
Sources, each in full: "Which Decisions Low-Bit Quantization Breaks, and How to Predict Them" (arXiv 2608.06564); "LFQ: Logit-aware Final-block Quantization" (arXiv 2605.29756); "Quantized Reasoning Models Think They Need to Think Longer, but They Do Not" (arXiv 2606.00206); their code; plus anything better you find.
Question: which individual decisions break when a model is converted to low bits: which tokens, which items, which kinds of step, by kind of task? How well can a broken decision be predicted before conversion, and from what? What do these papers show about where in the network the damage is done, and what repair do they test (at the last block, at the output, on answer length), with what result and at what bit widths and sizes? What does it mean for sorting the failed items of a ten-benchmark run on a 1-bit 1.7B model, and for choosing what to repair first?

ITEM 2. Published recipes for training at 1 bit and ternary
Sources, each in full with every result table and released code: ParetoQ (arXiv 2502.02631); QuEST, the quantization-aware training method used as the base for 1-bit weights with 4-bit activations in later work (locate the paper and its code); plus anything better you find.
Question: for 1-bit and ternary weights at 3B parameters and below: the exact quantizer for each bit width, how scales are defined and at what granularity, what stays in full precision, the gradient estimator, optimizer, schedule, data and token budget; every result beside its own full-precision model; every ablation and what it shows matters (budget, how the budget is split between full-precision and quantized training, initialization, estimator, learned scales); and which parts carry to one sign per weight with one scale per 128 weights, embedding and output matrix included, starting from a pretrained model or from a model that is already binary.

ITEM 3. Training scales alone, and transformations that change nothing
Sources, each in full with code where released: EfficientQAT (arXiv 2407.11062), in particular its end-to-end stage that trains only the quantization parameters; FPTQuant ("Function-Preserving Transforms for LLM Quantization"); "Neural Compression over Equivalence Classes: Exact Gauges and Functional Rate-Distortion" (arXiv 2611.07233); STBLLM (arXiv 2408.01803); plus anything better you find.
Question, in three parts. (a) What does training only the scales recover when the codes are frozen: at which bit widths and model sizes, with what data and how many tokens, against which baselines, and where does it stop helping? (b) Which transformations of a transformer leave its function exactly unchanged (reorderings, rescalings, rotations, merges)? Which can be folded away with no cost at inference? How much conversion error has each been shown to remove, at the lowest bit widths tested? Does any of it apply to choosing which 128 weights share a scale, or to a model that is already binary? (c) STBLLM: what it does below one bit per weight, on what evidence, and whether any part of it carries to our format.

FREEDOM
- Use any route to a source: another URL for the same paper, an HTML version, a mirror, the code repository, the authors' pages, papers that cite it. If one door is closed, find another and say which one you used.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that read or compare public files and datasets. Do not train or evaluate a model.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- what you read and how much of it (in full, or which parts), and by which route
- the facts, each with a link to where it can be checked
- your answer to the item's question
- what it means for getting the next five points at 1.7B in this format, with your probability before and after
- what is still unknown and the cheapest way to find out
Then a short closing section: anything across the three items that the project should do differently. New ideas go in that section, not in a second document.

HOUSE RULES
- Separate what a source shows from what you infer.
- No claim that nobody has done something unless you searched and say where.
- Probabilities are judgments and are given as numbers. No time estimates.
- Plain markdown, no em dashes, sections numbered 1, 1A, 1B.

BEFORE YOU START
If anything in this brief looks wrong, unclear or badly aimed, say so first and then proceed with your best reading.

STOP
Stop after the one document.
```
