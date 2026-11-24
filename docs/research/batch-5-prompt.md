# Reviewer prompt, batch 5

The task given to the second reviewer for batch 5. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included. Qwen3-1.7B first, Liquid AI LFM2 after.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The first outside reference at this format is PrismML's 1-bit Bonsai 1.7B. Its published scores, thinking off, ten benchmarks (table 9 of 1-bit-bonsai-8b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo), teacher then 1-bit:
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
- What we want now: the next five points of retention at this size and format, an understanding of what the conversion breaks, and a first full benchmark run on Apple hardware that we can trust.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, released this, or measured this, and bring back what you find.

ITEM 1. Low-bit training recipes and repairs we have not read to the end
Problem: our plan for training a 1-bit Qwen3-1.7B rests on a handful of published recipes. Several that bear directly on it have been read only in part, and there may be others we have never seen.
Starting sources, each in full with every table, appendix and released code:
- "Attend to Your Own Thoughts" (ScaleQ-1.58), arXiv 2608.01078
- CAT-Q, "Cost-efficient and Accurate Ternary Quantization for LLMs", arXiv 2606.26650
- "Model-Preserving Adaptive Rounding" (YAQA)
- LR-QAT, low-rank quantization-aware training
- JointQ, "Joint Scale-and-Integer Quantization for Large Language Models", arXiv 2611.20384, with the OneCompression repository (github.com/FujitsuResearch/OneCompression)
- The PRISM article on recall under quantization, https://link.springer.com/article/10.1007/s10791-026-10580-5
What we need you to find:
- For each: the exact method, what is trained and what is frozen, the loss, the training or calibration text and how it was chosen, the token budget, what is left in full precision, every result beside its own full-precision model at 3B parameters and below, and every ablation with what it shows matters.
- Anything in them about: which text to train on to bring back mathematics, code, tool calling and knowledge; fitting scales or reconstructing layers after signs are fixed; moving weights between scale groups; how recall of facts degrades and what restores it.
- Any other published recipe, repair or released model for 1-bit, ternary or 2-bit conversion of a pretrained model at 3B and below that the list above does not name. Released models on Qwen3-1.7B itself matter most: who has published low-bit versions of it, by what method, with what scores.
- Which parts carry to one sign per weight with one scale per 128, embedding and output matrix included, starting from a model that is already binary.

ITEM 2. The outside forensics of PrismML's models, in full
Problem: one outside project took PrismML's second-generation ternary models apart and trained its own versions, including a ladder on Qwen3-1.7B. It is the most detailed public record of how such a model is trained at our size. We have read its summary documents and not its full record, and two published training recipes disagree about the learning-rate schedule (one drops the rate when held-out loss stalls; this project describes a managed decay), which our own training plan has to settle.
Starting sources, each in full:
- github.com/sky-is-green/bonsai2-ternary-forensics: whitepaper, forensic archive, failure register, experiments file, the three gate reports, the paper draft, and the scripts behind its Qwen3-1.7B ladder
- Its two discussion threads on the model page: huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44 and /discussions/62
What we need you to find:
- For every Qwen3-1.7B run it made: starting point, what was trained, loss, text, token count, batch size, step count, learning rate and schedule, and the result at each stage.
- Its full account of the learning-rate schedule and of every failure it logged, with the evidence behind each.
- What it established about how PrismML's models were made, separated into what it measured and what it inferred.
- Any other outside analysis or reproduction of PrismML's models, first or second generation, 1-bit or ternary, that this project does not cite.
- What all of it means for training a 1-bit Qwen3-1.7B from a released 1-bit model.

ITEM 3. The facts the first benchmark run stands on
Problem: before any training, we will score the teacher and the released 1-bit models on the ten-benchmark suite on Apple Silicon, with per-item records. The score is only worth having if the models are loaded and run exactly as their makers intend and the harness matches the published one. We have not confirmed those facts.
What we need you to find:
- Qwen3-1.7B from its own model card and files: architecture numbers, license, recommended decoding with thinking off and on, the difference between the base and the post-trained variant, context length, chat template behavior.
- PrismML's 1-bit runtime: its MLX fork and its llama.cpp fork, the 1-bit kernel code paths, how the 1-bit files are loaded and unpacked, and which upstream MLX, mlx-lm and llama.cpp versions can load the 1-bit files without the forks.
- The evaluation harness: what PrismML used (EvalScope, bfcl-eval, versions, its own patches and whether they are public), what is needed to run the same ten benchmarks against a local server on Apple Silicon, how the code benchmarks are sandboxed, and every setting that changes a score (answer budgets, sampling, parsers, the BFCL subsets and how they are averaged).
- Any other released 1-bit model of Qwen3-1.7B, with its runtime, its file format and its published scores and settings, and whether its numbers and PrismML's can be compared as published.
- Every place where two published runs of the same model on this suite disagree, and the most likely cause.

FREEDOM
- Use any route to a source: another URL for the same paper, an HTML version, a mirror, the code repository, the authors' pages, papers that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that read or compare public files, listings and datasets. Do not train or evaluate a model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- what you read and how much of it (in full, or which parts), and by which route
- the facts, each with a link to where it can be checked
- your answer to what the item asks you to find
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
