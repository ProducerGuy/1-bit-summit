# 1 Bit Summit: Independent Reviewer Research, Three-Item Batch

**Date:** 2026-11-23  
**Scope:** Source-based research and forensic analysis only. No language model was trained or evaluated.  
**Target:** one sign per weight plus one FP16 scale for each contiguous 128-weight group, exactly 1.125 bits per weight for the quantized matrices, covering embeddings and output projection. Qwen3-1.7B first, Liquid AI LFM2 next.  
**Scoreboard:** five **percentage points** of the same-suite, same-settings FP16-normalized average score; no outside model result is our own product milestone.

## 1. Interpretation and evidence standard

Two potential traps in the brief require explicit controls. First, the statement that BFCL v3 has no training split is relevant but not a clean-data certificate. Its test combines legacy expert-curated prompts and live/user-contributed prompts, so a public tool dataset can overlap in API definitions, task structures or semantics even when sentences differ. Second, the three research programs have different formats and measurement rules. CAT-Q and ScaleQ are **ternary** and use other benchmark suites; Bonsai uses the strict 1-bit endpoint. Their numbers cannot be pooled.

**Source status:** I read the published main text, methods, results tables and applicable appendices of the arXiv HTML versions of [CAT-Q](https://arxiv.org/html/2606.26650) and [ScaleQ-1.58](https://arxiv.org/html/2608.01078), and checked the main [BitTern/CAT-Q README and released project file tree](https://github.com/IntelChina-AI/BitTern/tree/main/projects/cat-q). I read the [BFCL v3 official blog, including its category table and curation account](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html), and examined the primary dataset cards and links below; I **did not download and semantic-deduplicate the full datasets**. I read the [ThakiCloud README](https://github.com/ThakiCloud/bonsai-1bit-repro), its [REPORT](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md) and substantive sections of its [paper source](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/paper/main.tex); its complete executable script set and private raw runtime were **not independently executed or exhaustively line-audited**. The specified [sky-is-green forensic repository](https://github.com/sky-is-green/bonsai2-ternary-forensics), its complete gate logs, scripts, paper drafts and model-page discussions **could not be retrieved in full through the available browser routes**. Search-indexed snippets and earlier plan claims are explicitly labeled secondary, not a complete read. Accordingly, **Item 3 is not a claim of full-repository audit**. These limits constrain the strength of my conclusions.

**Reference-score arithmetic:** The user-supplied PrismML [1-bit Bonsai 1.7B whitepaper](https://github.com/PrismML-Eng/Bonsai-demo) table 9 gives mean FP16 **58.24** and 1-bit **40.88**, or **70.19%** retention. On this fixed ten-task arithmetic mean, another five retention percentage points requires **2.912 average-score points**, or **29.12 summed task-score points**. A probability of delivering five points always means this total-product criterion, not five raw points on one task. All probabilities below are subjective and conditional on a valid unseen-data comparison at fixed precision.

## 2. Item 1: Tool-calling data without BFCL v3 leakage

### 2A. What BFCL v3 actually tests

The [official BFCL v3 specification](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html) says the benchmark retains **BFCL v1 expert-curated non-live** and **BFCL v2 user-contributed live** data, and adds a distinct multistep/multiturn component. The following are its **13 single-turn subsets**, distinct from the four 200-example multi-turn subsets. Counts and names are from its **Full Leaderboard Score Composition** table (as published for v3, not the subsequently changed BFCL v4 composition):

| No. | BFCL v3 single-turn subset | Official item count | What success requires |
|---|---|---:|---|
| 1 | Python Simple AST | 400 | Pick function and exact Python arguments |
| 2 | Java Simple AST | 100 | Parse Java-style signature and arguments |
| 3 | JavaScript Simple AST | 50 | Parse JS-style call and arguments |
| 4 | Python Multiple AST | 200 | Distinguish among multiple offered tools |
| 5 | Python Parallel AST | 200 | Produce multiple independent calls |
| 6 | Python Parallel Multiple AST | 200 | Combine multiple-tool selection and parallel calls |
| 7 | Non-live Irrelevance | 240 | Avoid calling an irrelevant tool |
| 8 | Python Live Simple AST | 258 | Function and arguments from contributed real-use tasks |
| 9 | Python Live Multiple AST | 1,053 | Selection among live API functions |
| 10 | Python Live Parallel AST | 16 | Independent live calls |
| 11 | Python Live Parallel Multiple AST | 24 | Multiple simultaneous live tools |
| 12 | Live Relevance | 18 | Call a valid relevant live tool |
| 13 | Live Irrelevance | 882 | Refuse or omit irrelevant live calls |

[Source, category table and curation](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html). The v3 page also describes AST-based checks for ordinary single-turn results, executable/state-based checking for the added multi-turn component, and human curation. It should not be assumed that every displayed one-shot scenario is a pure call-schema-format test; relevance, no-call decisions, output parsing and function selection are distinguishable abilities.

The live subsets are not equivalent to an arbitrary collection of open-source APIs. Their sourcing from user-contributed material is precisely why a synthetic or publicly scraped tool corpus could share APIs or tasks. Older synthetic benchmarks, public APIs and common examples can coincide conceptually with the expert-curated legacy sets. **A dataset released before BFCL v3 is not necessarily independent of v1 and v2 source material.** [BFCL v3 methodology](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html); [BFCL prior official history](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html).

### 2B. Candidate public sources and realistic coverage

The ranking below concerns **coverage potential, not certified cleanliness**. Availability is sourced to the original dataset/model authors. The ratings are my analysis, not empirical BFCL results.

| Source and primary link | What it offers | Likely strengths across the 13 subsets | Important deficits or leakage risks |
|---|---|---|---|
| **[Salesforce xLAM function-calling 60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k)**; [APIGen paper](https://arxiv.org/abs/2406.18518) | Synthetic function calls from automatically checked/executable API scenarios | Strong candidate for Python simple, multiple, argument typing, some parallel combinations | Public APIs and templates may overlap v1/v2; no certified BFCL-v3 semantic exclusion in dataset card; weak Java/JS guarantees |
| **[Team-ACE/ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE)** | Diverse tool-use instruction and function-call examples | Useful for multi-function selection, required arguments and relevance/irrelevance if independently filtered | Tool schemas/prompts must be inspected; formatting conventions may differ; no proof of zero BFCL overlap |
| **[glaiveai/glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2)** | Synthetic conversational function calling | Simple calls, tool schema familiarity, some no-call or multiple-call examples | Potential template repetition and conversational artifacts; uncertain Java/JS and live weighting |
| **[OpenBMB ToolBench](https://github.com/OpenBMB/ToolBench)**; [ToolLLM](https://arxiv.org/abs/2307.16789) | Real-API documentation and multi-action tool-use instructions | Realistic tool selection, API ambiguity, longer chains and API diversity | Long trajectories not directly equivalent to single-turn AST calls; APIs could be shared with live tasks; broad source reuse |
| **New independently generated function corpus** using novel invented APIs and tasks, with public provenance and frozen scripts | Function-selection, schema, parallel/no-call, format-language variants can be controlled explicitly | **Best controllability** across all 13 target capabilities, especially Java/JS and live-style irrelevance | Not automatically clean if generated from leaked benchmark examples; generated semantics need independent reviewing; unpublished data cannot establish external prior art |

**Candidate coverage crosswalk, qualitative:**

| BFCL subset family | xLAM | ToolACE | Glaive | ToolBench | New independently generated APIs |
|---|---|---|---|---|---|
| Python simple and argument typing (1) | High | High | High | Medium | High |
| Java/JavaScript syntactic variants (2-3) | Unverified | Unverified | Unverified | Low/unclear | High by explicit design |
| Multiple tool selection (4,9) | Medium/high | High | Medium | High | High |
| Parallel + parallel multiple (5,6,10,11) | Verify | Verify | Verify | Medium/high | High by explicit design |
| No-tool / irrelevance (7,13) | Verify | Medium/high | Verify | Verify | High with deliberate negatives |
| Live simple and relevance (8,12) | Medium | Medium | Medium | Medium/high | High in task type, not same API domain |

"High" means the **data-generation mechanism could cover** the target capability. It is not a measured sample count, verified annotation distribution or BFCL score. In particular the tiny live parallel and relevance subsets are easy to overlook if sampling uniformly from general function-call datasets. The BFCL v3 score has internal category weighting, so 13 equal-sample training buckets need not be evaluation-optimal. [Official v3 score composition](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html).

### 2C. How to establish cleanliness, not just assert it

A strong audit has at least seven boundaries:

1. **Freeze benchmark identity.** Pin the exact BFCL v3 dataset revision and scoring protocol; never silently use v4. Preserve item IDs, task-family tags, API schema, reference function/arguments, and canonical parsed intent **on the audit side only**. [Official BFCL repository](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard).
2. **Provenance quarantine.** Exclude public corpora whose generation chains are explicitly BFCL-based, including alternate dataset packagings of benchmark prompts, prompt rewrites or gold function calls. For instance, a dataset explicitly derived from BFCL v3 is unacceptable even if it contains independently templated prompts. [BFCL v3 curation](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html).
3. **Exact and normalized deduplication.** Hash original texts and normalized instruction/tool signatures, strip formatting and whitespace, compare normalized AST/function arguments, and detect duplicate API documentation blocks. This eliminates only straightforward copies.
4. **Semantic deduplication.** Cluster paraphrases, equivalent API intents, function call graphs and interchangeable user constraints. A text with a new city/name but the same required call sequence remains a contaminated template. Use manual adjudication for uncertain matches. Matching semantics is a judgment process, not a provable zero-overlap guarantee.
5. **Hold out source families.** Distinct, independently invented API namespaces, argument schemas and task construction templates should be separated between training and benchmark; no BFCL public reference examples may seed synthetic generation. Similar *abilities* are allowed, near-isomorphic *items* are not.
6. **Inspect weighting and inference interface.** Report separate changes in choose-a-tool, arguments, number of calls, no-call decision and output serialization. Do not mistake a parser/template fix for recovered model capability. [BFCL v3 evaluator](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html).
7. **Document positive and negative matches.** Produce a reproducible audit manifest and an exclusion ledger. If a prospective training set has not undergone this audit, label it "candidate, cleanliness unverified," not "clean."

If every public dataset is suspect, a **new API universe with separately authored requests and independently verified reference calls** provides a more defensible clean source than any old scraping corpus, with the caveat that structural similarity is intentionally necessary to teach transferable behavior. Overzealous deduplication that excludes every shared *skill* would make useful function-call training impossible; the boundary must be task instance, not competence category.

### 2D. Does training repair low-bit tool calling?

A primary 2026 low-bit study, [Quantization Damage Is Multiplicative, Not Additive](https://arxiv.org/abs/2608.06564), measures tool-use decision-margin shrinkage across 16 models and bit widths down to two bits. It reports that compression can cause an assistant **not to call tools at all** even when its selection of a tool would otherwise be correct. This demonstrates the *failure mechanism*, **not** its repair at our 1-bit g128 format.

I did **not** verify a published controlled study in the inspected papers demonstrating that clean tool-use-specific retraining takes a pretrained **1-bit 1.7B** Qwen from BFCL 34.9 to near its FP16 71.8 under the **same** BFCL v3 scoring. Tool-use SFT and data-generation papers establish that data can train tool-use in other precision settings, not that this exact lost ability is cheaply recoverable. [xLAM/APIGen](https://arxiv.org/abs/2406.18518); [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE).

A better target than indiscriminate BFCL-style SFT is **paired decision-margin distillation**: on held-out, non-BFCL tool tasks, distinguish (i) tool call vs abstention, (ii) correct tool vs wrong tool, (iii) correct arguments, (iv) valid serialization. Repair the actual damaged margin and its downstream syntax, while keeping non-tool general tasks in replay to limit regressions. This is my proposed mechanism, not a documented 1-bit recovery result.

### 2E. Five-point potential and verdict

The BFCL deficit is **71.8 - 34.9 = 36.9 raw benchmark points**. Its contribution to the total ten-task deficit is **36.9 / (10 × 17.36) = 21.26%**. Fully restoring BFCL and changing nothing else would raise ten-task retention by **36.9 / (10 × 58.24) = 6.34 percentage points**. Therefore **+5 retention points from BFCL alone requires a raw BFCL gain of 29.12**, taking 34.9 to **64.02**, recovering **78.9% of its current BFCL deficit**. This is a demanding upper-envelope target, not a modest BFCL repair.

**Subjective probability that tool-call-data specialization alone delivers ≥+5 product retention points on our exact Qwen target:** prior **8%**, after source review **12%**. Probability it restores *some* BFCL points is considerably higher, but not the contracted milestone. The BFCL specialization may be more valuable in combination with other task repairs than as the sole five-point engine.

**Cheapest decisive evidence:** Before model training, conduct and publish a dataset provenance plus semantic-duplication audit on one selected corpus against pinned BFCL v3, then define a clean auxiliary holdout with different APIs and templates. The one eventual decisive model comparison is equal-compute strict-binary continuation with and without this corpus, scored on BFCL v3 **and** the untouched other nine benchmarks, with tool call-rate, choice, arguments and format separately logged. Without that split, a BFCL improvement is ambiguous.

## 3. Item 2: CAT-Q, ScaleQ-1.58, and BitTern code

### 3A. Reading record and what the code actually contains

- **[CAT-Q, arXiv:2606.26650](https://arxiv.org/html/2606.26650):** main text sections 1 through 5, formulas, result/ablation tables and Appendix B implementation and quantization notes examined via the full arXiv HTML. Appendix E's math/code failure pilot and Appendix G's stated limitations were checked for scope; I did not independently reproduce hardware throughput.
- **[ScaleQ-1.58 / Attend to Your Own Thoughts, arXiv:2608.01078](https://arxiv.org/html/2608.01078):** method, results tables and calibration/composition ablations, Appendix C sampling/optimization and Appendix D further results examined via arXiv HTML. The full output of all qualitative sample generations was not independently graded.
- **[BitTern](https://github.com/IntelChina-AI/BitTern) and [projects/cat-q](https://github.com/IntelChina-AI/BitTern/tree/main/projects/cat-q):** repository README, top-level project listing, available configuration and execution entry points checked; **not** a complete audit of every code file. Its own README explicitly says training code is **not yet released** and lists available **model checkpoints, inference and evaluation code**. The exported model is *fake-quantized floating-point tensors*, not a deployment-packed 1.125-bpw model. Consequently a claim of complete independently reproducing CAT-Q/ScaleQ learning dynamics from this public code would be unfounded. The CAT-Q paper's textual algorithm is the primary source for the absent training procedure.

### 3B. Exact CAT-Q mechanism

The target is **ternary** \(T\in\{-1,0,+1\}\), not our two-level sign code. CAT-Q starts from an existing full-precision pretrained model and learns a small set of **groupwise modulation variables**, rather than ordinary task fine-tuning of all FP16 teacher weights. Its reconstructed effective weight uses a per-group scale \(\alpha\) and ternary code \(T\). A shift \(\mu\) redistributes the source weights to make thresholding easier, but is **removed during reconstruction**, preserving a zero-point-free ternary deployment. A learnable threshold parameter determines the zero region. [CAT-Q, sections 2.2-2.3](https://arxiv.org/html/2606.26650).

The **Softened Ternarization** (ST) schedule initially uses a smooth function based on \(\tanh\) and increasingly sharp decision boundaries, then changes to hard ternary. Its stated defaults are transition fraction \(\gamma=0.8\), sharpness initialization 30, threshold initialization 0.5, nonoverlapping **group size 128**, AdamW with 0.001 initial modulation learning rate, batch 3, **60 epochs** with linear LR decay. It trains using **sliding-layer feature/output reconstruction** of the original high-precision model, not task reward or direct original benchmark answers. [CAT-Q sections 2 and Appendix B](https://arxiv.org/html/2606.26650).

Default data are **512 C4 sequences × 2,048 tokens = 1,048,576 distinct calibration token positions**. The **60 calibration epochs** mean repeated presentation of those data. A nominal product is **62,914,560 calibration-token presentations** if a token is counted once per epoch, but the actual GPU computation is greater and depends on how many sliding windows are optimized; neither that multiplication nor the paper's “1M calibration tokens” should be mislabeled unique *training work*. [CAT-Q Appendix B Table A](https://arxiv.org/html/2606.26650).

In W1.58A8 comparisons the paper leaves **softmax output probabilities in full precision** for stability. MoE routing exceptions are described for relevant architectures. The paper's method and released assets do **not** provide sufficient per-tensor evidence to certify that every Qwen3-1.7B tied input/output embedding weight was packed to strict signed-binary precision. This is a material specification gap, not a declaration that the model's tied head was definitely excluded. [CAT-Q Appendix B.2](https://arxiv.org/html/2606.26650); [BitTern released source and checkpoint notes](https://github.com/IntelChina-AI/BitTern/tree/main/projects/cat-q).

**CAT-Q Qwen3-1.7B Table 1, zero-shot commonsense suite.** All student/teacher ratios computed from the paper's own corresponding FP16 teacher row, *not* the PrismML ten-benchmark suite:

| Test | FP16 teacher | CAT-Q W1.58A8 | Ratio | CAT-Q W1.58A16 | Ratio |
|---|---:|---:|---:|---:|---:|
| PIQA | 72.25 | 68.16 | 94.3% | 68.40 | 94.7% |
| ARC-e | 69.95 | 54.94 | 78.5% | 55.88 | 79.9% |
| ARC-c | 42.66 | 28.67 | 67.2% | 28.16 | 66.0% |
| HellaSwag | 60.36 | 47.22 | 78.2% | 47.77 | 79.1% |
| Winogrande | 61.88 | 54.62 | 88.3% | 54.83 | 88.6% |
| **Mean of five** | **61.42** | **50.72** | **82.58%** | **51.01** | **83.05%** |

[CAT-Q Table 1](https://arxiv.org/html/2606.26650). The ability profile shows asymmetric damage, particularly ARC-c, but the paper's five-task mean is not our product scoreboard.

### 3C. Exact ScaleQ-1.58 / AYOT mechanism

ScaleQ is **CAT-Q's ternary optimization with a different, reasoning-aware calibration distribution**. For each prompt, the unquantized **same model being compressed** generates its reasoning trace and final answer. The prompt, reasoning and response are concatenated as calibration context. The algorithm trains the CAT-Q **scale, mean/redistribution and threshold variables** by sliding feature reconstruction on those self-generated passages. The distinction is not that ScaleQ fine-tunes the LM with ordinary next-token cross-entropy or trains it end to end on gold CoT answers. It changes **what activations the quantizer must preserve**. [ScaleQ sections 2.1-2.2](https://arxiv.org/html/2608.01078).

Default source inputs are **1,024 MetaMathQA prompts plus 1,024 NVIDIA OpenCodeInstruct prompts**, expanded by the teacher's generated reasoning, then truncated or padded to **2,048 tokens each**, total **4,194,304 context positions, called 4M calibration tokens**. The authors use **60 epochs** and batch size 3, inheriting CAT-Q's other settings. They also evaluate replacements using GSM8K **training** and MBPP **training** examples and ProofWriter **training**, specifically identifying source splits. The nominal 60-epoch exposure is about **252M token positions**, but again the per-window optimization makes direct FLOPs comparison inappropriate unless the exact sliding schedule is accounted for. [ScaleQ Appendix C.1-C.2](https://arxiv.org/html/2608.01078).

Default reported representation is **W1.58A16**, i.e. ternary weight coding, higher-precision activations. The output reports reasoning and coding generation tasks. A *thinking-enabled* original Qwen model and a *thinking-disabled* PrismML harness are not directly comparable without checking their full prompts and decoding configurations; the papers' score rows alone do not establish harness equivalence. [ScaleQ section 3](https://arxiv.org/html/2608.01078); [PrismML model/reproducibility repository](https://github.com/PrismML-Eng/Bonsai-demo).

**ScaleQ Qwen3-1.7B Table 1, the paper's own mathematics and coding task family:**

| Test | Original Qwen3-1.7B FP16 | ScaleQ W1.58A16 | Student / teacher |
|---|---:|---:|---:|
| MATH-500 | 90.80 | 38.60 | 42.5% |
| GSM8K | 84.08 | 54.35 | 64.6% |
| Omni-MATH | 27.76 | 12.23 | 44.1% |
| HumanEval+ | 76.22 | 34.14 | 44.8% |
| MBPP+ | 53.97 | 33.33 | 61.8% |
| **Mean** | **66.57** | **34.53** | **51.87%** |

[ScaleQ Table 1](https://arxiv.org/html/2608.01078). This is a very different picture from the paper's **90.52%** abstract headline. That headline measures its four overlapping math/code tasks **relative to a separately trained, ternary BitNet b1.58 2B4T model**, **not the original FP16 Qwen3-1.7B teacher**. It is not 90.52% teacher retention, and it is not a 1-bit result. [ScaleQ abstract and Table 1](https://arxiv.org/html/2608.01078).

**What the evidence actually supports:** The paper's **Qwen3-4B** data-composition ablation shows dramatic variation depending on calibration context. With its reported settings, a particular Qwen3-4B task suite increases from **17.43** on generic C4 calibration to **45.60** with model-self-generated CoT, while supplied external reasoning is weaker in that comparison. Its ProofWriter supplementary ablation similarly suggests that calibration samples can recover out-of-domain logic task accuracy. This effect is not established at one bit or on the PrismML ten-task suite, and those are **four-billion-parameter** results, not Qwen 1.7B. [ScaleQ Table 4, Table 7 and ablations](https://arxiv.org/html/2608.01078).

### 3D. What actually transfers to strict 1.125-bpw binary

| Component | Transfer judgment | Constraint |
|---|---|---|
| Teacher-generated reasoning and solution **as calibration activations** | **Strong conceptual transfer** | Separate generated tasks from the evaluation's problems and paraphrases; no direct 1-bit result |
| Sliding reconstruction at nonlinear block or paired-projection level | **Plausible transfer** | Must optimize end-to-end student-conditioned activations and tied output decisions, not only teacher-side single layers |
| Learnable per-g128 **scale** | **Directly compatible** | Exactly one **FP16** stored scale per 128 after folding; no additional learned zero point |
| Redistribution via training-only shift \(\mu\) | **Possible transfer** | Shift may choose binary signs, but must be entirely dropped from deployed representation and validated for true binary endpoints |
| Smooth-to-hard quantizer transition | **Possible but unproven** | Binary has no zero region, and gradient trajectories can differ substantially |
| Learned ternary threshold \(\Delta\) creating zeros | **Not directly transferable** | A third code violates strict binary; one must choose signs for all erstwhile zeros or replace this by a binary code-selection parameter |
| Ternary-specific packing and 1.58-bit representation | **Not transferable** | May have different memory and kernel rules; does not meet 1.125 bpw |
| 8-bit activations/softmax exceptions, MoE router exclusions | **Not benchmark-equivalent** | The target permits specific non-matrix parameters at high precision but includes every target matrix, including tied input/output; document all exceptions |
| Task-aware **reasoning and function-calling** calibration | **Potentially high value** | Real 1-bit task recovery and other-task regressions remain completely unmeasured in these papers |

The underlying lesson is neither “ternary success proves binary success” nor “CAT-Q fails because its teacher retention is low on one task family.” **Calibration states can matter enormously**, but the **loss landscape and missing ternary zero code** change fundamentally at our operating point. This is a candidate mechanism, not a successful conversion recipe.

### 3E. Five-point potential, probability, and cheapest discriminating evidence

For the distinct **calibration-content mechanism** (self-generated CoT, code and tool trajectories vs otherwise identical C4/general calibration), I assign a prior **12%** chance of delivering ≥+5 retention points on strict Qwen3-1.7B. After reading the task-data ablations and tiny-model limitations, my posterior judgment is **24%**. This is not a statistical posterior and assumes the rest of a competent binary conversion recipe is held fixed.

For **porting CAT-Q's ternary threshold/soft optimization itself** into signed binary without teacher-generated calibration, prior **10%**, after **12%** for a full +5-point step. Its original algorithm and ablations do not isolate a binary two-code solution. The two candidate probabilities are not independent; they should not be added.

**Cheapest way to reduce uncertainty before model training:** verify the **released** Qwen3-1.7B CAT-Q tensors, excluded parameter classes and head/embedding tie against a complete manifest; inspect exactly which preprocessing/scoring mode the evaluation scripts implement; acquire the genuine CAT-Q training code if released later or explicitly label it unavailable; run a source-only overlap audit for MetaMathQA/OpenCodeInstruct against fixed benchmark tasks. The single eventual result that would justify a five-point milestone is an **equal-total-compute, same-harness Qwen 1-bit g128 comparison** between generic C4 and student/teacher reasoning-aware calibration, with embeddings converted and reasoning/code/tool subtests reported separately. A gain on a different ternary format or suite cannot award that trophy.

## 4. Item 3: What the public Bonsai forensics establish

### 4A. Source inventory, including inaccessible material

| Source | What was inspected | Completeness and limits |
|---|---|---|
| [PrismML Bonsai demo and whitepaper index](https://github.com/PrismML-Eng/Bonsai-demo) and [Bonsai 1.7B model repository](https://huggingface.co/prism-ml/Bonsai-1.7B-gguf) | Published model formats, 1-bit scores, architecture and target claims | Relevant public pages and model metadata; PDF paper's every page was **not** independently re-read in this batch. Baseline numbers are explicitly user-supplied from table 9. |
| [ThakiCloud/bonsai-1bit-repro](https://github.com/ThakiCloud/bonsai-1bit-repro) | README, [REPORT.md](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md), substantive full paper content from [paper/main.tex](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/paper/main.tex), available script-file descriptions | Report and paper accessible; complete executable script/JSON output audit not performed, no rerun. |
| [ThakiCloud forensic script](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/scripts/bonsai_repro.py) | Public script summary and specific fingerprint/selftest function references from indexed source | **Partial inspection only**, no byte-level replication of its outputs. |
| [sky-is-green/bonsai2-ternary-forensics](https://github.com/sky-is-green/bonsai2-ternary-forensics) | Indexed repository description and cross-references from the linked model-page discussions | **Not read in full.** Live repository and file routes failed access, including the exact requested gate reports, experiments, draft, ledger and failure register. Do not interpret this document as having verified every entry. |
| [Bonsai 2 discussion 44](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44) and [discussion 62](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/62) | Search-indexed excerpts and linked titles | **Partial indexed excerpts only**, direct threads not fully retrievable. |
| [Independent ternary reproduction by AbdelH2O](https://github.com/AbdelH2O/ternary-bonsai-study) | Public indexed repository scope | Discovery only, **not a full independent read**. |
| [A separate 1-bit Bonsai fingerprint interpretation](https://kalarislabs.com/blog/prismml-bonsai-team-1-bit-reverse-engineering) | Indexed blog excerpt with layer sampling, sign-by-magnitude and projection scale breakdown | Source surfaced, direct full page did not resolve. The inference should be marked tentative until full methods/data can be inspected. |

These limitations are central. The prompt requests a **complete** forensic record, but the accessible evidence is not a complete copy of sky-is-green's entire repository. I will give findings supported by accessible primary accounts, and explicitly separate reported but unverified results. I cannot responsibly invent missing gate, ledger, file contents or revisions.

### 4B. First-generation 1-bit: what can actually be checked

ThakiCloud's [independent report](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md) and [paper](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/paper/main.tex) report these **different** kinds of evidence:

1. **Format verification.** Sampling 2,000 groups from PrismML's dequantized 1.7B release yielded exactly one magnitude per 128 weights and no zero ternary entries. This supports the claim that the released matrix weights are true signed-binary groups. It does not verify every tensor, every embedding row or the original conversion pipeline. [Report, Experiment A](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md).
2. **Short-passage perplexity.** On the report's fixed passage, dequantized Bonsai perplexity was **3.492** against Qwen FP16 **3.507**, whereas naïve g128 rounding yielded roughly **2,109,839** perplexity. This proves that basic rounding is a terrible approximation in this setup, and that the published model functions well on that passage. **It does not establish task-level retention or a clean held-out proof of near-lossless ability.** The source reports other passage/harness PPL values elsewhere; they must not be pooled as identical experiments. [Report, experiments A and B](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md).
3. **Signs and scales.** Across the sampled matching body matrices, ThakiCloud reports approximately **71.6% sign agreement** with base Qwen3-1.7B, hence **28.4% changed signs**, and dequantized Bonsai scales approximately **2.26 times** the base group's naive mean magnitude. These are useful fingerprints. They are not evidence of an exclusive algorithm or a proof that zero training occurred. [Paper and report](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/paper/main.tex).
4. **Public-method frontier.** QuIP-like rotation and compensation reaches about **2.1×** the FP16 perplexity on the authors' passage for pure strict 1-bit. Preserving a small salient fraction at higher precision improves perplexity but violates our exact format. Naive 1-bit collapse is substantially worse. [ThakiCloud README, REPORT and paper](https://github.com/ThakiCloud/bonsai-1bit-repro).

These are partly *single-passage or calibration-passage* demonstrations. A very low perplexity ratio on one passage cannot imply 99% retention, and the unit `FP16 PPL / 1-bit PPL` is not our ten-benchmark scoreboard. The independent [model discussion identifying a clean-holdout problem](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44) specifically warns that published QuIP-like PPL success can reflect reuse of a calibration passage for evaluation. Treat ThakiCloud's cited 2.1× ratio as a **limited local result** unless the actual frozen, disjoint-passage manifest is present and audited.

**Configuration alignment is material.** The [original Qwen3-1.7B config](https://huggingface.co/Qwen/Qwen3-1.7B/raw/main/config.json) lists `vocab_size=151936`, context 40960 and no rope scaling; the [unpacked Bonsai config](https://huggingface.co/prism-ml/Bonsai-1.7B-unpacked/raw/main/config.json) lists `vocab_size=151669`, context 32768 and YaRN scaling. The vocabulary difference is **267 rows**. It could be a deliberate cropped/padding representation in the dequantized distribution, not a fundamentally different original tokenizer. Before attributing logits/perplexity differences to quantization, inspect the original GGUF token IDs, removed-row probability mass, padded-vocabulary treatment, RoPE regime and whether the same attention settings were evaluated. A naive full-distribution KL comparison with mismatched vocabularies is not even well-defined without a documented conditioning or alignment rule.

### 4C. Can the sign/scale fingerprint prove rounding rather than training?

**No. It is not identifiable from these observables alone.**

A direct binary reconstruction from a source tensor starts with the original signs and chooses scales; then an input-conditioned linear solver can flip some signs. But an optimizer that carries training-only FP32 latent magnitudes through a binary STE process can also leave almost all signs unchanged, especially when flip inertia is high. Few sign flips do not imply no training; many flips do not imply a particular training objective. A global 2.26× scale-ratio median can arise from **activation-weighted functional fitting**, scale redistribution across neighboring projections, or actual weight re-training. For fixed sign codes \(b\), weights \(w\) and positive-semidefinite input covariance \(C\), the optimal function-space scale is

\[
s^*=\max\left(0,\frac{b^\top C w}{b^\top C b}\right),
\]

which **can exceed** \(\frac1{128}\sum_i|w_i|\) with no outward movement of the original teacher weights. Under plain unweighted weight MSE, by contrast, the best same-sign scale is exactly the group's mean absolute magnitude and cannot exceed it. Thus the fingerprint rejects *naive unweighted weight-MSE fitting* but not functional PTQ and not QAT/continued training. This argument is analytic; it does not establish that PrismML used a particular route.

**An independent, conflicting interpretation exists.** [Kalaris Labs' indexed analysis](https://kalarislabs.com/blog/prismml-bonsai-team-1-bit-reverse-engineering) reports, on a **sample of three of 28 layers at 1.7B and one layer at 8B**, that first-generation 1-bit signs flipped about **47.5% of the smallest original-weight magnitude decile** but **6.7% in the largest**, and that 1-bit scales were closer to a **2.1× median** in its sample. That author interprets the pattern as more compatible with extensive natural-text training than a handful of calibration updates. These numbers use **different sampled layers/statistics** than ThakiCloud's 2.26; they are not a true contradiction in measurement until protocols are aligned. Its training conclusion is also an inference, not a reproducible disclosed PrismML recipe. I inspected an indexed excerpt, not the complete paper, so I do not adopt its mechanistic claim as established.

**Verdict:** The evidence supports *sophisticated optimization of binary signs and scales relative to an existing pretrained model*. It does **not** independently establish whether the first-generation release was end-to-end trained, short calibration-optimized, mirror-descent adapted, or combined approaches. The evidence cannot uniquely reconstruct a private training trajectory from the released endpoint. PrismML's conversion is proprietary in the [Bonsai project materials](https://github.com/PrismML-Eng/Bonsai-demo).

### 4D. Second generation must not be used to answer the first-generation question

The 2026 [sky-is-green forensic repository description](https://github.com/sky-is-green/bonsai2-ternary-forensics) and author posts [44](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44) / [62](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/62) describe a **different** release, Bonsai 2 **ternary 27B** derived from Qwen3.8-27B, with a structured rotated basis, a trained-weights residual and approximately the **last 8% of ternary codes** appearing to receive ordinary ternary-QAT correction. The author explicitly reports that its format and some mechanics were reconstructed, and links a failure register and archived experiments. This is **reported author analysis from indexed material**, not my own line-by-line verification of its scripts or tests.

**Inference:** Even compelling evidence of a trained residual in second-generation *ternary* weights would not establish how first-generation *signed binary 1.7B* weights were obtained. The architectures, backing pretrained models, bit codes, transformations and production procedures may differ. Conversely, finding some inference-time rotation in Bonsai 2 cannot be back-projected onto the first-generation 1.7B release.

### 4E. Public negative results, decisive settings, and retractions

**Source-confirmed negative observations:**

- Plain 1-bit sign/mean-scale rounding collapses on Qwen3-1.7B. A small fixed-bit correction without suitable context can leave extreme downstream error. [ThakiCloud report](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/REPORT.md).
- Permitting a **salient higher-precision fraction** is a highly favorable reconstruction baseline but **not a valid strict 1.125-bpw product**. Any result using it must be separated from the product scoreboard. [ThakiCloud paper](https://github.com/ThakiCloud/bonsai-1bit-repro/blob/main/paper/main.tex).
- A reported QuIP-style **2.1×** evaluation result on Qwen3-1.7B is specifically challenged for **same-passage calibration/evaluation**, according to the [public second-generation forensic discussion](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/discussions/44). The author reports that a clean, multi-region holdout instead has roughly **2.09×** PPL ratio *on average*, with considerable regional variability, and warns against the more favorable retention interpretation. Because the discussion was only available via indexed excerpt, the exact checkpoint, metric direction, seeds, region manifest and full correspondence are **not independently verified here**. Do not turn a PPL reciprocal into a ten-task accuracy ratio.
- The same [sky-is-green archive's indexed description](https://github.com/sky-is-green/bonsai2-ternary-forensics) says an early **1.7B STE+KD** achievement was **retracted** to approximately **48% retention on a clean holdout**. The original metric, test text, 48%-ratio definition, detailed reason and numerical history are **not verified without the complete failure register**. Its status is **author-reported retraction**; do not cite the earlier favorable claim as standing evidence.

**Which settings appear decisive in outside attempts:** source material supports careful attention to (i) **rotation/basis and correlated-weight structure**, (ii) **calibration distributions that reflect subsequent use**, (iii) **whether calibration and evaluation truly occupy disjoint passages**, (iv) **strict packed-bit accounting with every matrix included**, (v) **student-versus-teacher activation inputs and cross-layer compensation**, (vi) **training-only discrete-code adaptation**, and (vii) **harness alignment for tokens, RoPE and thinking mode**. Some of these are demonstrated controls in [ThakiCloud](https://github.com/ThakiCloud/bonsai-1bit-repro); others are explicitly studied in [CAT-Q](https://arxiv.org/html/2606.26650), [ScaleQ](https://arxiv.org/html/2608.01078), and the [sky-is-green author's indexed descriptions](https://github.com/sky-is-green/bonsai2-ternary-forensics). I have **not** verified a complete ranked experiment ledger of the latter, so I cannot assign an empirical causal effect size to each setting from that repository.

The question "Did the first-generation model train end to end or use rounded error compensation?" may be aimed too narrowly. Multiple procedures could lead to similar final signs/scales. The meaningful independent target is **which specific, affordable procedure matches its output quality at identical bits, and which measured mechanism explains the difference**. Reconstructing an undisclosed algorithm exactly is not required for the project's product scoreboard.

### 4F. Five-point potential, probability and cheapest information gain

**Before/after probability that insights from public forensics alone allow an independent strict-binary Qwen conversion to gain ≥+5 points versus a matched non-forensic baseline:** prior **12%**, after inspected evidence **18%**. The positive update reflects known high-value structural clues and clear failures of naive baselines; the ceiling remains low because mechanisms are not identified and clean public reproductions still trail the released product. This is a **distinct research-lead probability**, not the probability that PrismML used a particular private algorithm.

For the narrow proposition **"first-generation Bonsai used no recovery training, just rounding plus error compensation"**, I assign **25%** subjective probability based on the currently accessible record, with **wide uncertainty**. This is not an evidential frequency. Sophisticated PTQ remains a live possibility, as does continued training. Giving it a number does **not** make the author's fingerprint proof.

**Cheapest missing information:** obtain a complete, immutable export of sky-is-green's repository and its linked model-page discussions; audit each file/gate-report and the raw holdout indices. Align the ThakiCloud and Kalaris fingerprint comparisons to a **single identical tensor list, sampled group count and original teacher configuration** before ranking training-versus-PTQ explanations. On the available published GGUF or dequantized files, quantify scale ratios and sign flips *conditional on original magnitude percentile and layer type* and repeat on a matched held-out data suite; no model training is necessary for that forensic step. The first decisive *recipe* proof, later, is a strict-g128 matched-harness Qwen conversion whose capability/compute Pareto point beats a locked baseline. A closer forensic fingerprint without capability improvement earns a science result, **not** five product points.

## 5. Across all three items: the course correction

### 5A. Put the five-point arithmetic before method selection

The source split matters. **BFCL can supply at most ~6.34 points** of retention if fully restored alone, and reaching +5 points from it requires nearly 79% restoration of its deficit. [PrismML ten-task numbers supplied in the brief, original whitepaper](https://github.com/PrismML-Eng/Bonsai-demo). Meanwhile, **MATH-500** has a teacher/student gap of **39.6** raw points, creating a **6.80-point retention ceiling** if fully restored alone. A blended program that recovers, say, 15 raw points on math and 14.12 raw points on BFCL would clear +5, while no single task needs near-complete repair. This is arithmetic, not a forecast.

### 5B. Separate three independent variables rather than mixing them

1. **Function-preserving parameterization**: rotation, channel/neuron permutations, scales and tied-head-compatible transformations before quantization. See the other file in this archive, `01_function_preserving_binary_group_assignment.md`. Published [PermuQuant](https://arxiv.org/abs/2605.09503) is an adjacent higher-bit diffusion precedent, not a strict 1-bit LLM proof.
2. **Quantization decision policy**: how group signs and scales are selected, whether ternary zeros serve as training-only intermediates, and whether latent sign inertia permits coordinated updates. [CAT-Q](https://arxiv.org/html/2606.26650) teaches transferable modulation principles but not a direct binary threshold.
3. **Information presented during conversion**: general C4, self-generated math/code reasoning and **truly independent** tool-use scenarios. [ScaleQ](https://arxiv.org/html/2608.01078) shows that calibration content can dominate ternary results, but this needs honest g128 binary verification.

Treating all three as one enormous candidate obscures whether any gain is from a better basis, better discrete-code search, or a task-domain change. Source cleanliness is particularly critical for Item 1.

### 5C. Individual predictions, not additive success probabilities

| Research direction | Prior chance of +5 product retention points | After this reading | Confidence and caveat |
|---|---:|---:|---|
| Clean tool-call specialization alone | 8% | **12%** | One BFCL task has a hard 6.34-point ceiling; requires ~79% of its damage restored |
| Reasoning-aware calibration content in otherwise fixed binary recipe | 12% | **24%** | Strong ternary evidence, weak strict-binary transfer evidence |
| CAT-Q soft/threshold mechanism adapted to two signs, without new data | 10% | **12%** | Ternary zero code is a nontrivial discontinuity |
| Public Bonsai forensics translate into an independent better conversion | 12% | **18%** | Forensic record partly inaccessible, training path underidentified |
| Function-preserving binary group reassignment from companion note | 10% | **20%** | Algebraically valid in parts of the architecture, benefit unmeasured at strict 1-bit |

All probabilities are **subjective judgments**, not estimates from controlled trials, not mutually exclusive, and **must not be summed**. A single combined model might gain five points by repairing several small capability losses rather than one large one.

### 5D. Named gaps and scope boundary

- Clean **BFCL v3** training examples are not a public fact until the candidate dataset goes through provenance, lexical/semantic and API-level decontamination. Matching task families is necessary; copying benchmark instances is not.
- The **CAT-Q training/calibration source** is still advertised as *forthcoming* in the inspected BitTern repository. An inference/checkpoint export is insufficient for reconstructing its optimizer behavior. [BitTern CAT-Q README](https://github.com/IntelChina-AI/BitTern/tree/main/projects/cat-q).
- Qwen3-1.7B **ScaleQ/CAT-Q** published rows are **ternary**, sometimes with different activations, task sets, and reasoning modes. They do not establish one-bit, tied-embedding preservation.
- PrismML's **first-generation training method is undisclosed**, and multiple distinct algorithms can produce its observed signs and scales. The second-generation ternary experiments do not resolve the first-generation method.
- The requested full sky-is-green forensics **was not actually accessible**, and source titles/snippets do not replace a complete audit. In particular do not award success to a retracted validation, inferred training schedule, or apparently clean set without a raw split manifest.
- Our own conversion baseline on the **target Qwen ten-benchmark suite** is unmeasured. All five-point figures in this paper are conditioned on the user-supplied outside PrismML reference and mathematical upper envelopes. Neither this review nor its companion idea earns a product trophy.

**Independent judgment:** The most actionable cross-item idea is a *capability-conditioned binary conversion objective*: choose exact no-overhead group/basis transformations, select binary signs/scales through student-conditioned optimization, and calibrate the resulting full-network decisions on **decontaminated** teacher-generated math, code and tool-use contexts, with explicit replay protecting unaffected tasks. The literature makes each component plausible, but supplies **no direct evidence** that their combination yields a five-point improvement at the specified precision or size. Protect that distinction when the project owner compares reviewers.
