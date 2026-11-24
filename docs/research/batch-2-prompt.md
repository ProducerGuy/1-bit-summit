# Reviewer prompt, batch 2

The task given to the second reviewer for batch 2. The first reviewer worked the same three items.

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

ITEM 1. Knowledge loss
MMLU-Redux and GPQA Diamond together are 20% of the published loss.
Question: what is known about why low-bit conversion loses factual knowledge and multiple-choice accuracy, and is there any published repair (a method, a kind of data, a training stage) that brings it back at 2 bits or below, at small model size? What does the repair cost other abilities? Starting point: "Linger and Lose: Knowledge Collapse in Low-Bit Language Models", plus anything better you find.

ITEM 2. Optimizers for discrete weights
Sources: arXiv 2611.20384 (JointQ), arXiv 2610.22621 ("Noise-shaped Sampling and Annealing for Scalable On-the-edge Training of Binary and Ternary AI Models"), their code, plus anything better you find.
Question: is there an optimizer or search procedure for binary weights that beats straight-through training at language-model scale? On what evidence (models, sizes, budgets, baselines)? What exactly does it do, and would it apply to training signs with one scale per 128 weights, starting from a pretrained model or from a model that is already binary?

ITEM 3. The published routes from a pretrained model to 1-bit or ternary
Sources, each in full with appendices and released code: BitNet Distillation (arXiv 2510.13998), OneBit (arXiv 2402.11295, github.com/xuyuzhuang11/OneBit), BinaryLLM (arXiv 2508.06974), plus anything they lead to.
Question: for each, the exact losses, schedules, data, token budgets and what stays in full precision; every result at 2B parameters or below beside its own teacher; which ingredients are shown by ablation to matter and by how much; and which of them carry to one sign per weight with one scale per 128 weights, embedding included.

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
