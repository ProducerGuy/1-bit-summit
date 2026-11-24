# Reviewer prompt, batch 7

The task given to the second reviewer for batch 7. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included. The formula is proven first on Qwen3-1.7B, where a published 1-bit model of the same format exists to measure against, and then on a Liquid AI LFM2 model, where none exists.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The outside reference on Qwen is PrismML's 1-bit Bonsai 1.7B. Its published scores, thinking off, ten benchmarks (table 9 of 1-bit-bonsai-8b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo), teacher then 1-bit:
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
- The claim the project wants to be able to make is a formula claim: the recipe that works on Qwen3-1.7B, applied to an LFM2 model with nothing changed except what the shapes force, keeps the same share of that model's ability. This batch is about the second half of that claim. Nothing in the project has yet been run on LFM2 weights.
- Time and compute are not limits on this project. Do not rule out or discount any route because of what it costs to train or to read. What limits the project is what is not yet known.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, released this, proved this or measured this, and bring back what you find.

ITEM 1. The target: which LFM2 model, exactly what is inside it, and what its license allows
Problem: the project has to choose one LFM2 checkpoint as the target of the transfer test and a smaller one as an engineering check, pin both to an exact revision, and know them completely before anything is run: every tensor, how the model was trained, what scores are published for it, and what the license permits. We hold the technical report and nothing checked against the released files. We also do not know what Liquid AI has released since, and whether a later model is the better target.
Starting sources, each in full with every table, figure, appendix and released file:
- Liquid AI, "LFM2 Technical Report", arXiv 2511.23404
- Liquid AI's model pages, model cards, configuration files, tokenizer files, chat templates and licence text for every model in the LFM2 family and any successor, wherever they are hosted
- Liquid AI's own documentation, blog posts and release notes on these models
- The LFM2 implementations in the open runtimes: the transformers library, ggml-org/llama.cpp (src/models/lfm2.cpp and its conversion script), and MLX
What we need you to find:
- Every model Liquid AI has released in this family to date: name, size, release date, modality, what changed from the one before, and where its files are.
- For each text model near our sizes (about 350M to 2.6B): the exact architecture, layer by layer. Which blocks are convolution and which are attention, every width, the kernel, the gates, the normalization, the position scheme, the vocabulary, whether the embedding and output matrix are one tensor or two, and the context length.
- A table of every weight tensor in the checkpoint you would pin as the target and in the smaller check model: name pattern, shape, count, element type, and each kind's share of all weights. Taken from the released files, not from the report. State whether every matrix dimension that would carry groups of 128 is a multiple of 128.
- How the model was made: data, token counts, the teacher, the distillation objective, any stages after pretraining. Whether a larger model of the same family, or the model's own teacher, is available to distil from.
- Every published score for these models, by Liquid AI or anyone else, with settings: which of the ten benchmarks above have a published LFM2 score, and what suite Liquid AI itself reports.
- How the model is meant to be prompted: chat template, system prompt, tool-calling format, whether it has a reasoning mode, recommended sampling. Anything that would change a benchmark score if done differently.
- The licence in full: what it permits and forbids for research use, for converting the weights, for publishing converted weights, for publishing benchmark results, and any revenue or use limit. Quote the governing clauses briefly and link them.
- Your recommendation: which checkpoint to pin as the target and which as the check, at which exact revision, and why. If two are close, say what would decide between them.

ITEM 2. Low-bit LFM2, and low-bit models built like it: who has done it
Problem: we do not know whether anyone has taken an LFM2 model, or any language model that mixes convolution blocks with attention, to 1 bit, to three levels, or anywhere under 4 bits, by any method, and what happened when they did. Without that we have no comparator for the LFM2 half of the project and no warning of what breaks.
What we are looking for, by any name and from any source:
- Every low-bit build of any LFM2 family model: Liquid AI's own quantized releases and what it says about them; community builds at any width, with the 1-bit, 2-bit and 3-bit ones (including GGUF types such as IQ1, IQ2, Q2 and any 1-bit tensor type) listed one by one with who made them, by what method, what is kept in higher precision, the true stored bits per weight, and any score or usable report of quality.
- Any quantization-aware training, distillation into low-bit weights, ternary or binary conversion of an LFM2 model or a derivative, published, released or described in public.
- Anything Liquid AI or its researchers have published or said about how these models hold up under quantization, at which widths, and which parts are sensitive.
- Any sign that PrismML, or anyone else working in the same 1-bit format, has converted or plans to convert a model of this family.
- Which runtimes can today load and run an LFM2 model whose weights are stored as one sign per weight with one scale per group, and what each would still need.
- Beyond LFM2: results on binarizing or going to very low bits in language models with convolution blocks, depthwise convolutions, multiplicative gates or other non-transformer blocks, and the nearest results from vision or speech where the same block types were pushed to 1 or 2 bits. For each: which block types broke first, what was kept in higher precision, and what fixed it.
What we need you to find:
- The list above, complete, with a link for every entry and your check of each claim against the files or code where they exist.
- The best public low-bit build of each LFM2 text model near our sizes, by evidence, to serve as the comparator.
- Where nothing exists, say so with the searches you ran and where.

ITEM 3. Carrying a recipe from Qwen to LFM2: what is different, and what the difference does
Problem: the formula claim fails if a recipe tuned on a plain transformer does not carry to a model with a different block design and a different training history. LFM2 differs from Qwen3 in at least these ways: most of its blocks are gated convolutions and few are attention; it was itself produced by distillation from a larger teacher on a very large token count; its vocabulary and tokenizer are different; and it has no published 1-bit version to measure against. We do not know which of these differences matter for conversion to 1 bit, in which direction, or how a failed transfer could be told apart from a recipe that was never general.
What we need you to find:
- Evidence on whether low-bit recipes carry across architectures and model families: every study that applied one conversion or low-bit training recipe unchanged to more than one family, what carried, what had to be retuned, and by how much the results differed.
- Evidence on training history: whether models that were trained longer, on more tokens, or by distillation lose more or less under conversion and low-bit training than models trained less, and why.
- For each part of an LFM2 block that Qwen3 does not have, what is known about its tolerance to very low-bit weights: the projection into the gates, the two multiplicative gates, the depthwise kernel, the projection out. What published low-bit work on such parts keeps in higher precision, and whether any of it holds at 1 bit.
- Every exact, function-preserving change of variables an LFM2 block admits (scalings, permutations, rotations that can be folded into the weights at no stored cost), set beside those of a transformer block, and which of them a conversion could use.
- What a fair measurement on LFM2 looks like: the benchmark suite, the prompt format and the settings under which retention on LFM2 can be compared with retention on Qwen3-1.7B; what to use as the reference line when no published 1-bit model exists; and how many questions and seeds a claim of equal retention needs.
- A way to grade a transfer result so that its cause can be named: what to vary and what to hold fixed so that a shortfall on LFM2 can be attributed to the architecture, to the training history, to the data and teacher, or to the recipe.
- What you would change in the project's formula claim, or in the order of work, in the light of what you found.

READING STANDARD, A CONDITION OF RETURN
- Every source named in this brief, and every source a conclusion of yours rests on, is read in full from its primary file: all sections, tables, figures, appendices, and the released code, configuration and model files where they exist. Abstracts, index pages, search snippets and other people's summaries do not count as reading.
- Code and files are part of a source. Where a repository or a model file exists, open it and check the paper's or the card's statements against it.
- If a source resists, try other routes until one works. If it still cannot be read in full, list it at the very top of your document under "Not read in full", with every route you tried, and build no conclusion on it.
- Before you return, check every label. If most of your sources are not read in full, the brief is not met; keep reading instead of returning.

FREEDOM
- Use any route to a source: another URL for the same paper, an HTML version, a mirror, the code repository, the authors' pages, model hubs and their mirrors, papers that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that read or compare public files, listings and datasets, including the headers, tensor names and shapes of released model files, or that check a derivation numerically. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count; say which sources are behind such a gate.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- your answer to what the item asks you to find
- what is still unknown and the cheapest way to find out
Then two probabilities, each before and after this batch, as numbers with your reasons:
- that a recipe which reaches a given retention on Qwen3-1.7B, applied to the LFM2 target with only shape-dependent settings changed, lands within five points of that retention on LFM2
- that a 1-bit LFM2 at the target size in this format, by any recipe, keeps 70% of its own full-precision scores
Then a short closing section: anything across the three items that the project should do differently. New ideas go in that section, not in a second document.

HOUSE RULES
- Separate what a source proves or shows from what you infer.
- No claim that nobody has done something unless you searched and say where.
- Probabilities are judgments and are given as numbers. No time estimates, and no conclusion that rests on a training or reading budget.
- Plain markdown, no em dashes, sections numbered 1, 1A, 1B.
- If you need the project owner to do something, reply with only the numbered steps, one action per line, and nothing else. Results come after he reports back.

BEFORE YOU START
If anything in this brief looks wrong, unclear or badly aimed, say so first and then proceed with your best reading.

STOP
Stop after the one document.
```
