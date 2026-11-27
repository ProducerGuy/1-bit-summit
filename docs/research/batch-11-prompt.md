# Reviewer prompt, batch 11

The task given to the second reviewer for batch 11. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights along a row (1.125 bits per weight), with the embedding and output matrix included and tied. The formula is proven first on Qwen3-1.7B, where a published 1-bit model of the same format exists to measure against (PrismML's 1-bit Bonsai 1.7B), and then on a Liquid AI LFM model.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision parent's average, same suite, same settings. The suite is ten benchmarks, thinking off: MATH-500, BFCL v3, MMLU-Redux, GSM8K, MBPP+, HumanEval+, GPQA Diamond, IFEval, MuSR, IFBench. The end goal is 99%.
- Decisions already recorded by the project, given so you know where things stand. You may argue against any of them:
  - The strict target is every learned weight in the binary format. A second, named track keeps normalization gains in 16 bits with everything else strict. A convolution kernel kept in 16 bits is its own labelled arm.
  - A transform that must run at inference is a separate track. A change that can be folded into the stored weights exactly, offline, is allowed.
  - The recipe is developed on Qwen3-1.7B and frozen before any LFM target is scored. LFM2-1.2B is scored first; LFM3-1.7B is the second target, locked to the same Qwen freeze.
  - A recipe is not chosen by reading the ten-benchmark suite over and over. Every attempt is kept in a ledger that is never rewritten. A confirmed claim comes from a recipe picked by a rule fixed in advance and then trained fresh. A separate set of items that no selection has read backs any broad claim, beside the ten benchmarks and without changing them.
- Time and compute are not limits on this project. Do not rule out or discount any route because of what it costs to train or to read.
- The project is open, public research. Licensing is settled and needs no work from you.
- The project's public repository on GitHub, named 1-bit-summit, holds its plan, its registers and every earlier batch. The plan is PLAN.md; its list of sources, numbered S1 onward, is in the same file.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, proved this or measured this, and bring back what you find.

ITEM 1. Figures in the sources the plan rests on
Problem: neither reviewer has routinely looked at figures. One reviewer's reading tool returns text only. Where a source gives a result only in a plot, or where its text describes a plot, the project has taken the text's word. In the one case checked so far, a patent application, the text said a histogram had modes near plus and minus 0.3 and the drawing's axis showed plus and minus 0.03; the same filing labelled two figures the other way round from its text and carried a drawing from a different application. Any statement in the plan that rests on a description of a figure, or that would change if a figure were read, is unchecked.
Starting sources, in order of how often the plan cites them. Each by its number in PLAN.md's source list:
- PrismML's whitepapers: S1, S2, S3, S4, S5
- Outside studies of PrismML's files and format: S19, S20, S65, S73
- Low-bit methods and measurements the plan leans on: S35, S9 with its code S57, S47, S53, S71, S74, S76, S33, S61, S22, S55, S34, S135, S24, S52, S36 with its code S134, S137, S136, S155, S21, S23
- Studies of where damage sits and what predicts it: S44, S45, S75
- Training from scratch at low bit widths: S7, S169
- Mirror descent: S14, S15, S17
- Liquid AI: S12, S177
- Every other source in the list whose figures carry a result that the plan states or relies on.
What we need you to find:
- For each source: every figure that carries a measured result, what the figure shows when read off its axes, and whether the text says the same. Give numbers read from the plot with the method used (axis ticks, pixel positions, the source's own data file where one exists).
- Every statement in PLAN.md and in the repository's research documents that rests on a figure or on a text description of one, checked against the figure: confirmed, corrected with the right value, or not checkable and why.
- Results that exist only in a figure and that the plan has not used but should.
- Any figure that contradicts its own paper's text or tables.
- For each source, whether a data file, notebook or code behind its figures is public, and whether the figure can be reproduced from it.

ITEM 2. What development reads
Problem: the project has ruled that the recipe is chosen on Qwen3-1.7B without reading the ten-benchmark suite over and over, and that a separate set of items no selection has read backs any broad claim. Nothing yet says what development does read: which measure, on which text, how much of it, and how that measure is shown to rank recipes as the ruler would before it is trusted. Nothing says what goes in the unread set either. The project holds some evidence on the first question: its own measurements on small decoders (PLAN.md, section 1A row U3, and sections 2K to 2M), and Liquid AI's distillation paper, S177, which compares four recipes on several measures. Test both; accept neither.
What we need you to find:
- Every published study that tests whether a cheap measure ranks compressed or quantized language models the way downstream benchmarks do: perplexity, divergence from the parent's next-token distribution, top-token agreement with the parent, the share of answers that flip, measures read from hidden states, and any other. For each: the setting, how many models were ranked, whether they came from different recipes or from one recipe at different points, the rank agreement, and where the measure failed. Results at 1 to 2 bits and on models under 4B count most.
- Measures read with the parent's text fed in against measures read from the model's own generations; on chat-formatted text with reasoning off; on tool calls; on code. Which kind tracks which of the ten benchmarks.
- What happens when the training loss and the selection measure are the same quantity, or nearly so, and how a selection rule guards against a recipe that improves the measure without improving the model.
- A development measure for this project: the measure, the text it is read on and where that text comes from, how much text gives a ranking that is stable, and how the measure is validated against the ruler on Qwen3-1.7B before it decides anything, without that validation itself becoming repeated reading of the suite.
- The unread set: what it should contain, how large it should be, how it is kept apart from training text, development text and the ten benchmarks, how many times it may be read and by whom, and what it can and cannot support. Published methods for a test set that is read more than once.
- Your view on whether the project's ruling on development and the unread set is right, and what you would change.

ITEM 3. Sources known to the project and not yet read
Problem: earlier batches named sources that neither reviewer could open or finish. Each may hold a result the project needs.
The sources, each in full:
- Pipette, Liquid AI's benchmark site: the rows of its results table and raw data, https://pipette.liquid.ai/results and https://pipette.liquid.ai/data . Its tables are drawn by script; a plain fetch returns column headers only. Wanted: whether it holds quality scores (IFBench, IFStruct, GPQA Diamond, MATH-500) for any 1-bit, ternary or sub-2-bit file, PrismML's Bonsai-27B and Ternary-Bonsai-27B included, and for LFM2, LFM2.5 and LFM3 files at any width, each beside its full-precision reference, with the thinking mode of each row.
- The international publication of the Caltech application, WO 2026/161822 A1, with its drawings, and anything on the record of US application 19/460,181 and its provisional 63/749,353 that is public without an account.
- ARB-LLM's supplementary file, with its proofs and pseudocode, published separately from its code repository: https://github.com/ZHITENGLI/ARB-LLM
- The appendix of the Nemotron 3.5 Bolt paper, arXiv 2610.33039
- Quamba2's code, arXiv 2503.22879
- In llama.cpp: src/llama-quant.cpp whole, conversion/base.py whole, and the vision and audio parts of conversion/lfm3.py
- In CEWT's code, base_linear.py whole: https://github.com/1733116199/cewt
- The tokenizer files (tokenizer.json, tokenizer_config.json) of LFM2-1.2B and LFM3-1.7B, and the safetensors headers of LFM2-1.2B and LFM2-350M
- Every page of the listing of quantized versions of LFM2-1.2B: https://huggingface.co/models?other=base_model:quantized:LiquidAI/LFM2-1.2B
- Liquid AI's documentation: https://docs.liquid.ai
- Precision Numerics' announced Boole models, a 2B and a 1-bit Qwen3.8-27B preview: whether either is public, and if so its card, files and any statement of method, data or budget
What we need you to find:
- For each source: what it holds that bears on the project, with numbers and links.
- For Pipette: every quality row for a file under 4 bits and for any LFM model, in a table with its full-precision reference, and the retention it implies.
- For the WO publication: whether its text, equations and drawings differ from the US publication, with each difference.
- For the tokenizer files and headers: the vocabulary size, special tokens, the tensor list with shapes and data types, and anything that disagrees with the configuration files.
- What remains unread after this item, and why.

READING STANDARD, A CONDITION OF RETURN
- Every source named in this brief, and every source a conclusion of yours rests on, is read in full from its primary file: all sections, tables, figures, proofs, appendices, and the released code, notebooks and configuration where they exist. Abstracts, index pages, search snippets and other people's summaries do not count as reading.
- Figures are part of a source. Look at them, not at their captions.
- Code is part of a source. Where a repository exists, open it and check the written claims against it.
- If a source resists, try other routes until one works. If it still cannot be read in full, list it at the very top of your document under "Not read in full", with every route you tried, and build no conclusion on it.
- Before you return, check every label. If most of your sources are not read in full, the brief is not met; keep reading instead of returning.

FREEDOM
- Use any route to a source: another URL for the same document, an HTML version, a mirror, the code repository, the authors' pages, works that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing and its recorded decisions are wanted. Flag blind spots.
- You may write and run small scripts that check a derivation or a count numerically, read values off a figure, or read public files, listings and model file headers. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count; say which sources are behind such a gate.

WHAT TO RETURN
One markdown document, with any image crops or data files you made attached beside it. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- every derivation and every figure reading written out so it can be checked
- your answer to what the item asks you to find
- what is still unknown and the cheapest way to find out
Then four probabilities, each before and after this batch, as numbers with your reasons. State the "before" figure first, before you read, and keep it.
- that a formula fixed on Qwen3-1.7B and applied under the project's transfer rule lands on LFM2-1.2B within five points of the retention it reached on Qwen3-1.7B
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
