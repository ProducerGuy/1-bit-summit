# Reviewer prompt, batch 8

The task given to the second reviewer for batch 8. The first reviewer worked the same three items.

```
ROLE
You are one of two independent reviewers on a research project called 1 Bit Summit. The other reviewer is working on the same three items at the same time. You will not see their work and they will not see yours. Disagreement between you is useful, so reach your own conclusions.

THE PROJECT
- Goal: a repeatable way to convert a pretrained language model to 1-bit weights and keep its ability. Format: one sign per weight plus one FP16 scale per group of 128 weights (1.125 bits per weight), with the embedding and output matrix included. The formula is proven first on Qwen3-1.7B, where a published 1-bit model of the same format exists to measure against, and then on a Liquid AI LFM model.
- Small models are the point. Results at 7B and above, or at 2 to 4 bits, count as evidence only as far as they carry down.
- Progress is counted in steps of five percentage points of benchmark retention: the converted model's average score divided by the full-precision teacher's average, same suite, same settings. The end goal is 99%.
- The outside reference is PrismML's 1-bit Bonsai 1.7B. Its published scores, thinking off, ten benchmarks (table 9 of 1-bit-bonsai-8b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo), teacher then 1-bit:
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
- PrismML has never stated how its models are made. The project has two routes to its next step. One starts from PrismML's released 1-bit 1.7B model and trains its signs and scales further against the full-precision teacher. The other converts the full-precision Qwen3-1.7B itself.
- Time and compute are not limits on this project. Do not rule out or discount any route because of what it costs to train or to read.
- The project is open, public research. Licensing is settled and needs no work from you.

THIS BATCH: THREE ITEMS
Each has a problem, what we are looking for, and what we need you to find. How you get there is up to you. The named sources are a starting point, not a boundary: for every item, also ask the plain question of who else has done this, released this, proved this or measured this, and bring back what you find.

ITEM 1. A second 1-bit model of the same parent: Precision Numerics' Boole
Problem: a second team has released a 1-bit model built from Qwen3-1.7B. If it says anything about method, data, training amount or format, it is the only other public data point for 1 bit at exactly this size, and it could serve the project as a second reference and a second starting point. We have not read what its makers have published, and we do not know how it relates to PrismML's model.
Starting sources, each in full with every table, figure, file list and released file:
- The model page and files: https://huggingface.co/precision-numerics/Boole-1.7B and every other model that organization has published, including any larger preview
- Its post: https://precisionnumerics.ai/blog/boole-1p7b and every other post on that site
- Its code: https://github.com/PrecisionNumerics/boole-demo and any runtime or llama.cpp fork the team maintains
- Anything its authors have said elsewhere: discussions on the model pages, talks, threads, issues
What we need you to find:
- Every statement of how Boole is made: the starting point, the method, the loss, the training text, the amount of training, the hardware, what is trained and what is frozen.
- The exact format of its weights, from the files and the loader code: sign and scale layout, group size, which tensors are 1-bit and which stay in higher precision, whether the embedding and output matrix are converted, the true stored bits per weight, and whether a file loads in an unmodified upstream runtime.
- Every score its makers or anyone else has published for it, with settings, set beside PrismML's 1-bit 1.7B and the teacher on the ten benchmarks above wherever the numbers allow.
- How it relates to PrismML's model: independent work or a derivative, any statement on that, and any public comparison of the two sets of weights.
- Whether it is a sound second reference and a sound second starting point for further training, and what would have to be checked on the files to be sure.
- Anyone else who has released a 1-bit or three-level conversion of a model of 3B or less since mid 2026, by any method, with what they report.

ITEM 2. The outside study of PrismML's 1.7B files, and its own low-bit training on a small Qwen
Problem: an outside researcher has published a study of PrismML's released 1.7B files together with their own attempts to train low-bit small Qwen models: https://github.com/AbdelH2O/ternary-bonsai-study. It is the nearest thing to an independent replication at our size, and it holds real training reports on a model of the same family. We have read only part of it. We do not know what its training runs found, what failed, or whether its planned run at 1.7B happened.
Starting source: that repository, every file, with its code. Among them a research log, a replication plan, and reports named QAT08.md, QAT08_CHAT.md, GPTQ_PILOT.md and GPTQ_V2.md.
What we need you to find:
- Everything the study established about PrismML's 1.7B files, 1-bit and three-level: how the stored weights relate to the full-precision parent, what is kept in higher precision, anything that bears on how they were made, and how each finding was reached.
- Every training or conversion run the study made: the model, the starting point, the method, the loss, the text, the token count, every setting, the result against its teacher, and the author's own account of what worked, what failed and why.
- Whether a run at 1.7B was made, and its result.
- Where the study's findings agree or disagree with other public analyses of PrismML's files, and which is better supported.
- Every other public attempt to reproduce a PrismML model at 3B or less, or to train one further, with its result.
- What in this study a project that plans to train PrismML's 1-bit 1.7B model further should copy, avoid or test first.

ITEM 3. What we may be missing under 2 bits, and what PrismML's newest release adds
Problem: we do not know that our list of 1-bit and three-level recipes and measurements is complete, and three things have appeared that we have not worked through. A public survey of methods under 2 bits exists that we have not read. PrismML released Ternary Bonsai 2.5 27B in November 2026: the same format and size as its September model, retrained for agent and tool work, compared against rounded files of the same base model made by two post-training methods at 2.27 to 3 bits. And the packed low-bit file types are on their way into upstream llama.cpp.
Starting sources, each in full:
- The survey: under_2bit_literature_survey.md in https://github.com/arpitsinghgautam/llm-quantization-gallery, and the rest of that repository
- PrismML, "Ternary Bonsai 2.5 27B" (November 2026), wherever PrismML hosts it, with its model page, files and any discussion there; and its predecessor, bonsai-2-27b-whitepaper.pdf in github.com/PrismML-Eng/Bonsai-demo
- The comparison files it names and the methods behind them: ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF and the Unsloth Dynamic files of the same model, with whatever papers, code or notes describe how they are made
- The llama.cpp pull requests that add the packed three-level and 1-bit types and the Hadamard kernels
What we need you to find:
- From the survey and your own search: every method that trains or converts a language model to under 2 bits per weight. For each: what it is, whether it starts from a pretrained model, the smallest model it was shown on, the share of the full-precision score it keeps there, whether the embedding and output matrix are converted, and whether code or weights exist. The project already holds BitNet b1.58, OneBit, BiLLM, ARB-LLM, STBLLM, ParetoQ, BitDistill, EfficientQAT, double binary factorization and its successor AF1, GSQ, EdgeRazor, ASkewSGD, MagR, Qronos, SDQ-LLM, Bi-Mamba and Ternary Mamba. Tell us what is missing from that list, and anything about a listed method at 3B or below that a careful reader would not want to miss.
- An independent reading and audit of the Bonsai 2.5 report: what it claims, whether its arithmetic and its tables agree with each other, how its scores were measured and what that does to their reliability, and what changed between the September and November models as far as any public statement or file shows.
- What the two post-training methods behind the comparison files are, how low they have been shown to go, on what sizes, and with what scores. Whether either has been applied to a model of 3B or less.
- Any published evidence on retraining a model inside a fixed low-bit format to recover a particular ability, and on which abilities are lost first and recovered last.
- The state of the packed 1-bit and three-level types in upstream llama.cpp and in MLX: what is merged, what is under review, and what a packed 1-bit file of a model that is not a Qwen would still need.
- What all of this changes for a project whose first run trains PrismML's released 1-bit 1.7B model further.

READING STANDARD, A CONDITION OF RETURN
- Every source named in this brief, and every source a conclusion of yours rests on, is read in full from its primary file: all sections, tables, figures, appendices, and the released code, configuration and model files where they exist. Abstracts, index pages, search snippets and other people's summaries do not count as reading.
- Code and files are part of a source. Where a repository or a model file exists, open it and check the written claims against it.
- If a source resists, try other routes until one works. If it still cannot be read in full, list it at the very top of your document under "Not read in full", with every route you tried, and build no conclusion on it.
- Before you return, check every label. If most of your sources are not read in full, the brief is not met; keep reading instead of returning.

FREEDOM
- Use any route to a source: another URL for the same document, an HTML version, a mirror, the code repository, the authors' pages, model hubs and their mirrors, works that cite it. Use any workaround you judge sound and say which one worked.
- Go beyond the listed sources whenever something better exists. If you think an item asks the wrong question, say so and answer the better one as well.
- Workarounds, new ideas, alternative solutions and disagreement with the project's framing are wanted. Flag blind spots.
- You may write and run small scripts that read or compare public files, listings and datasets, including the headers, tensor names and shapes of released model files, or that check a derivation or a table numerically. Do not train or evaluate a language model.
- The project owner will not submit any access form that asks for personal information, and no credentials or paid access are used. A source that needs them does not count; say which sources are behind such a gate.

WHAT TO RETURN
One markdown document. For each item, in whatever structure serves it best:
- for every source, one of three labels: read in full from the primary file; read in part, with the parts named; not read. Say by which route. A section built from summaries, indexes or earlier knowledge of a source says so in its first line.
- the facts, each with a link to where it can be checked
- your answer to what the item asks you to find
- what is still unknown and the cheapest way to find out
Then two probabilities, each before and after this batch, as numbers with your reasons:
- that further training of the signs and scales of a released 1-bit 1.7B model against its full-precision teacher gains five points of retention over 70.2% on the ten benchmarks
- that a conversion of the full-precision Qwen3-1.7B by a recipe assembled from public work reaches 70.2%
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
