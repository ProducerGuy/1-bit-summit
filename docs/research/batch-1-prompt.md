# Reviewer prompt, batch 1

The task given to the second reviewer for batch 1. The first reviewer worked the same three items.

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
  Average 58.24 / 40.88, retention 70.2%.
- What we want now: the next five points of retention at this size and format, and an understanding of what the conversion breaks.

THIS BATCH: THREE ITEMS
Each has a question that must be answered. How you get there is up to you.

ITEM 1. Tool-calling training data
BFCL v3 is 21% of the published loss and has no training split.
Question: which public sources of tool-calling prompts could be used to train or calibrate a converted model without touching BFCL v3's test items, in their original words or restated? How do you know they are clean, given how BFCL v3 itself was built? How well do they cover what BFCL v3's 13 single-turn subsets test? Is there any published evidence that tool-calling ability lost to low-bit conversion comes back with the right data?

ITEM 2. ScaleQ-1.58 and CAT-Q, in full, with code
Sources: arXiv 2608.01078 ("Attend to Your Own Thoughts"), arXiv 2606.26650 (CAT-Q), the code release the first paper names (github.com/IntelChina-AI/BitTern), plus anything they lead to.
Question: what exactly do these methods do (what is trained, against what target, on what text, with how many tokens, with which parts of the model left in full precision, scored in which mode), what does every Qwen3-1.7B result look like beside its own teacher, and which parts carry over to one sign per weight with one scale per 128 weights and which do not?

ITEM 3. The public record on how PrismML's models were made
Sources: github.com/sky-is-green/bonsai2-ternary-forensics in full (all documents, gate reports, paper draft, scripts, and its discussion threads on the model pages), github.com/ThakiCloud/bonsai-1bit-repro in full (report, paper, scripts), plus anything they lead to.
Question: what does the complete record establish, and what does it only suggest, about how PrismML's models were made? In particular the first-generation 1-bit 1.7B: trained end to end, or rounded with error compensation? Which training settings did outside attempts find decisive, which results were retracted, and which results stand on clean held-out data?

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
Then a short closing section: anything across the three items that the project should do differently.

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
