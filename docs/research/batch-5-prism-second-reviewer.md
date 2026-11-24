# 1 Bit Summit: PRISM full-source retrieval audit and technical findings

## 1. Access route, source integrity, and scope of the read

**Source:** Swastik Vaish, Arpit Singh Gautam, Varun Tiwari, Jitendra Singh Yadav, ["PRISM a diagnostic framework for parametric recall degradation in quantized large language models," *Discover Computing* 29, article 700 (2026)](https://link.springer.com/article/10.1007/s10791-026-10580-5), DOI [10.1007/s10791-026-10580-5](https://doi.org/10.1007/s10791-026-10580-5). The publisher lists publication on October 6, 2026, and a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

**Actual retrieval:** Direct opening of the Springer HTML, DOI redirect, and publisher PDF and ePDF variants failed in the available browsing environment. A separate container HTTP request also failed at DNS resolution. Searches indexed by the publisher nevertheless returned **substantial verbatim, section-level text of the actual Springer article**, including its introduction, methodology, numerical results, methods controls, tables' descriptions, figure captions, limitations, conclusion, and data/code availability statements. This report uses those directly retrieved publisher-indexed passages, not an abstract-only paraphrase. The article itself was the source of those passages, not a different paper. No access form, account, payment, or owner's personal data was used.

**Completeness verdict:** **Extensive primary-text read, NOT verified full-document read.** The original 38-page PDF was **not** obtained. Complete cell-by-cell contents of the 18 tables, the graphical panels themselves, full bibliography, any appendices, and supplemental attachments were **not** individually inspectable. Figure captions described below were retrieved as publisher-indexed article text; **none of the images was examined directly**. Consequently an exhaustive per-model, per-bit table would be fabricated if reconstructed from narrative excerpts. This is an explicit research gap, not a finding that those numbers do not exist.

**Routes attempted:** [Springer article](https://link.springer.com/article/10.1007/s10791-026-10580-5); [Springer PDF](https://link.springer.com/content/pdf/10.1007/s10791-026-10580-5.pdf); DOI redirect; Springer content/html and epdf variants; [author's publications listing](https://arpitsinghgautam.me/publications); [the code URL named in the article](https://github.com/Swa-s-tik/PRISM); and title/DOI searches for mirrors and preprints. Publisher-indexed search results were the working access route. Neither the article's asserted open repository nor a readable alternate PDF was independently confirmed. The [library catalog entry](https://iris.sena.edu.co/EDS/Search?lookfor=%22Tiwari%2C+Varun%22&type=AU) labels an HTML/PDF full-text record, but that does not establish anonymous access to its contents.

**Source-link convention:** All factual tables and numbers below are attributed to the [same primary publisher article](https://link.springer.com/article/10.1007/s10791-026-10580-5), identified by section, table, or figure when available. Values described as calculations or judgments are explicitly marked.

## 2. Models, quantizers, precision and parameter exclusions

### 2A. Actual models

| Model | Parameters | Role in paper | Source |
|---|---:|---|---|
| Qwen2.5-3B-Instruct | 3B | Main phenomenon, component manipulation, equal-parameter-mass controls, retrieval and comprehension | [Methods, Sec. 3](https://link.springer.com/article/10.1007/s10791-026-10580-5) |
| Qwen2.5-7B-Instruct | 7B | Cleanest 2-bit-through-6-bit GGUF sweep | [Sec. 3, Table 7](https://link.springer.com/article/10.1007/s10791-026-10580-5) |
| Llama-3.2-3B-Instruct | 3B | Cross-family component replication and a negative NF4 result | [Sec. 4, Table 11](https://link.springer.com/article/10.1007/s10791-026-10580-5) |
| Gemma-2-2B-it | 2B | Cross-family component replication, depth-specific negative control | [Sec. 4, Table 11](https://link.springer.com/article/10.1007/s10791-026-10580-5) |

The authors state they ran inference-only on **one RTX 5060 with 8 GB VRAM** and no training or probe-data calibration. Those models are instruction-tuned, not Qwen3-1.7B. [Sec. 3](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 2B. Quantizers and minimum precision

| Quantization implementation | Widths directly described | Calibration and grouping | Qualification |
|---|---|---|---|
| torchao `IntxWeightOnlyConfig`, round-to-nearest (RTN) | 8, 4, 3, 2 bits | **32-weight groups**, asymmetric zero points; per-module filters | At 2-bit the Qwen3B MLP intervention ceases to function; numbers are not comparable with g128 binary scales |
| bitsandbytes | INT8, NF4 4-bit | NF4 double quantization, BF16 compute | A 4-bit Llama3.2 result preserves recall, so degradation is not universal |
| `gptqmodel` GPTQ | Calibrated 3 and 4 bits explicitly used in component experiments; other configurations not fully recovered | **128-weight groups**, **256 WikiText-2 calibration samples**, module-level dynamic exclusions | Same group cardinality as our codec but a different quantizer and code alphabet |
| llama.cpp GGUF `k` quants | Q6, Q4, Q3, Q2 on Qwen2.5-7B | GGUF quant types, not one fixed bit width or g128 codec | The **lowest reported deployed sweep is 2-bit class**, but K-quants are not uniform two-bit signs plus one scale |

Throughout the study the authors say **`lm_head` remains FP16**. They do not demonstrate 1-bit or ternary quantization, nor a full binary embedding/output matrix. The minimum regime named is **GGUF Q2 at 7B** and RTN 2-bit tested as a failing MLP intervention on 3B. [Methods, Table 3; Secs. 4 and 5](https://link.springer.com/article/10.1007/s10791-026-10580-5).

**Important exact-codec difference:** Their three-bit RTN experiments use asymmetric group-32 scales and zero points; our binary constraint is one FP16 scale and 128 binary signs. Even their GPTQ g128 setting uses multi-level codes. Treat this paper as a *damage-location diagnostic*, not a faithful emulator of our bit format.

## 3. Probes: construction, denominators, decisions and metrics

### 3A. Knowledge conflict (`facts_v2`)

The paper describes **114** moderate-prior updatable factual relations: headquarters city **32**, company founding year **32**, company CEO **20**, film director **18**, and composer nationality **12**. A false but type-compatible alternative is created by **swapping values within the same relation**. Each question is posed in three passage conditions: a passage asserting the counterfactual, a passage supporting the true value, and an irrelevant passage, plus a closed-book condition without the pertinent fact. [Sec. 3](https://link.springer.com/article/10.1007/s10791-026-10580-5).

The primary Qwen2.5-3B **anchor contains 96 of 114** items, those answered correctly by the FP16 model without context. An anchored teacher's closed-book accuracy is **1.00 by selection**, not an unfiltered task accuracy. Llama3.2-3B uses anchor **92**, Gemma2-2B **105**, and Qwen2.5-7B **100** in reported blocks. The authors also report unfiltered checks. [Secs. 3-5; Tables 7, 11](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 3B. Scoring rules

- **CB-Acc:** fraction of anchored questions still answered with the originally correct fact without pertinent contextual support.
- **CFR:** context-following rate in contradictory passages. The answer must **affirm** the supplied counterfactual, not merely contain its words in a negation.
- **MEM:** answers siding with the prior memory or rejecting the counterfactual; the manuscript writes `MEM = p + reject`.
- **OTHER:** `1 - CFR - MEM`, where neither proposition is positively asserted. Authors treat **OTHER > 0.20** as a model-breakage warning.
- **Support/open-book accuracy:** correct answer when the true fact appears verbatim in the passage.
- **Recovery fraction:** `(open_book - closed_book)/(1 - closed_book)` when defined. If open-book = 1, this metric is automatically 100% whenever CB < 1; at CB = 1 it is undefined, not zero or a meaningful improvement.

A deterministic negation-aware classifier strips case/punctuation/articles, matches whole-token spans, handles negation cues within clauses, and assigns one of three outcomes. Human validation: **60/60** matches with one independent annotator (`kappa=1.00`), and **45/46** with the first author on another sample (`97.8%`, `kappa=0.95`). The article reports a garbled, ambiguous single disagreement. It uses **95% Wilson intervals** for binomial rates, **2,000-item-bootstrap replicates** for some estimates and **10,000** for mechanism contrasts, with paired bootstrap where applicable. This is reported methodology; raw labels were not downloadable in this audit. [Sec. 3, Table 4](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 3C. External facts and leak-free tests

| Probe | Dataset construction | Items | Why it matters |
|---|---|---:|---|
| **PopQA conflict** | 400 source facts from **16 relations**, within-relation type-compatible incorrect facts; subset correctly recalled by teacher | 400 pool, **164 anchored** | External, often rarer facts; strong quantization sensitivity |
| **CounterFact** | Standard external factual editing/knowledge-conflict items | **108 anchored** | Replication with high cloze-format OTHER rate |
| **Two-hop fictional comprehension** | Synthetic entities; answer requires chaining two supplied facts, not a verbatim extract; irrelevant distractors | **160** | Closed-book baseline is 0 by construction, so correct answers must come from context |
| **Three-hop RAG** | Three-link fictional-entity chain, chain-of-thought scoring; no closed-book route | **80** | Tests compositional retrieval rather than easy copy |
| **Long single-hop** | A target fact buried among about 60 distractor company-city sentences, roughly **570 words** | **120** | Demonstrates that easy copying is not always robust with distractors |
| **Long multi-hop** | Three-hop scattered chain, ten distractor chains and filler | **100** | Tests longer composition, high OTHER rates |
| **MMLU / WikiText-2** | External capability and fluency controls | **MMLU 1,995** in reported control | Shows whether intervention destroys general capability as well as recall |

[Methods and results, Tables 6, 7, 8, 13, 15, 18](https://link.springer.com/article/10.1007/s10791-026-10580-5).

## 4. Quantitative results by bit width and model

**Reading rule:** A value omitted below was **not extractable from publisher-indexed prose** and is not a zero. Table 6 and Table 7 are richer than the fragments accessible here; their complete cells and Wilson interval bounds were not individually recovered.

### 4A. Anchored closed-book knowledge and conflict

| Model, setup and probe | Precision | Closed-book (CB-Acc) | CFR | OTHER | Comment |
|---|---|---:|---:|---:|---|
| Qwen2.5-3B, `facts_v2`, torchao RTN | FP16 | **1.00** | **0.60** | not recovered | 96 anchored |
| Same | RTN 8-bit | **0.91** | not recovered | <=0.05 across RTN functional sweep | |
| Same | RTN 4-bit | **0.84** | **0.74** | <=0.05 | Context-follow increase is weaker prior competition, not better context reading |
| Same | bitsandbytes INT8 | **0.97** | not recovered | not recovered | Different back-end, not monotone with torchao |
| Qwen2.5-7B, `facts_v2`, GGUF K | Q6 (6-bit class) | **1.00** | **0.74** | <0.08 over sweep | 100 anchored |
| Same | Q4 | not recovered | not recovered | <0.08 | |
| Same | Q3 | not recovered | not recovered | <0.08 | |
| Same | **Q2** | **0.88** | **0.85** | <0.08 | Lowest working width in the reported 7B result |
| Qwen2.5-3B, CounterFact | FP16 | **1.00** | **0.56** | not recovered | 108 anchored |
| Same | NF4 | **0.82** | **0.64** | approx **0.25** | High garbage makes CFR unreliable |
| Llama3.2-3B, facts | FP16 | **1.00** | **0.77** | not recovered | 92 anchored |
| Same | NF4 | **1.00** | **0.75** | not recovered | Negative finding: no detectable closed-book erosion |

Source: [Sec. 4, Figure 2, Table 7 and discussion](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 4B. Public PopQA knowledge and short supplied-context answer

| Qwen2.5-3B, PopQA n=164 anchored | CB-Acc | Open-book/support | Notes |
|---|---:|---:|---|
| FP16 | **1.00** | not individually recovered | By anchoring |
| 8-bit (implementation-specific) | **0.67** | **0.99** through 4-bit | The paper warns PopQA rare facts degrade early |
| 4-bit | **0.71** | **0.99** | Higher than the 8-bit cell because back-ends differ |
| Uniform 3-bit | **0.20** | not recovered | **OTHER 0.45**, model-breakage regime |
| MLP-only 3-bit | **0.24** | not recovered | **Delta CB 0.76** |
| Attention-only 3-bit | **0.77** | not recovered | **OTHER 0.06**, delta CB 0.23 |

Source: [Table 6 and surrounding discussion](https://link.springer.com/article/10.1007/s10791-026-10580-5). The phrase "0.99 through 4-bit" is an aggregate paper claim, not a separately verified per-row 8-bit/4-bit cell.

### 4C. Context comprehension, including the false generalization from copying

| Qwen2.5-3B test | FP16 | 8-bit | 4-bit | Uniform 3-bit | MLP-only 3-bit | Attention-only 3-bit |
|---|---:|---:|---:|---:|---:|---:|
| Fictional **two-hop**, n=160, context composition | **0.98** | **0.97** | **0.74** | **0.15** | **0.43** | **0.94** |
| Fictional harder **three-hop**, n=80, context composition | **0.912** | **0.850** | **0.812** | **0.013** | **0.138** | **0.637** |
| Long **single-hop copy**, n=120, about 570 words | **0.97** | **0.94** | **0.88** | **0.00** | **0.01** | **0.78** |
| Long **multi-hop**, n=100, context composition | **0.75** | **0.64** | **0.54** | **0.00** | **0.03** | **0.30** |

All fictional-context tasks report **closed-book = 0**, by construction. Short one-sentence, distractor-free gold-fact copying stays at the **1.00 ceiling** in the paper's documented torchao, bitsandbytes and GGUF sweeps down to Q2, but *this ceases to hold under long context, distractors, or broken GPTQ 3-bit settings*. [Table 8, Fig. 3; Tables 15, 16, 18 and Figs. 10-11](https://link.springer.com/article/10.1007/s10791-026-10580-5).

## 5. Component interventions and controls

### 5A. Whole MLP versus attention: anchored `facts_v2`, RTN 3-bit

| Model | MLP-only closed-book loss (Delta CB) | Attention-only loss | Implied anchored MLP CB-Acc | Implied anchored attention CB-Acc |
|---|---:|---:|---:|---:|
| **Qwen2.5-3B-Instruct** | **0.844** | **0.135** | **0.156** | **0.865** |
| **Llama3.2-3B-Instruct** | **0.38** | **0.03** | **0.62** | **0.97** |
| **Gemma2-2B-it** | **0.362** | **0.019** | **0.638** | **0.981** |

Calculating anchored post-quantization CB-Acc as `1 - Delta CB` is valid here because the teacher anchor is defined to equal 1. The model-family figures are printed in [Sec. 4, Table 11, Fig. 6](https://link.springer.com/article/10.1007/s10791-026-10580-5). Llama MLP CB-Acc 0.62 has a reported 95% interval approx 0.52-0.71 (deduced from the author's stated loss interval 0.29-0.48); Gemma MLP CB-Acc reported 95% interval 0.54-0.72. Intervals are not independently recomputed.

**A key confound:** MLP projections represent **about 88% of the non-embedding parameters** on the studied Qwen model. Quantizing all MLP weights perturbs far more weights than quantizing attention. This result identifies the component intervention that breaks recall; **it does not independently prove that a random MLP parameter carries more fact information than a random attention parameter**, or precisely where the fact is stored. [Secs. 4 and 5.2](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 5B. RTN compared with calibrated GPTQ, same Qwen 3B and 3-bit precision

| Intervention | RTN Delta CB | GPTQ Delta CB | Consequence |
|---|---:|---:|---|
| All MLP matrices | **0.844** | **0.615** | Whole-MLP susceptibility persists |
| All attention matrices | **0.135** | **0.083** | Attention is less disruptive in this setup |
| First five MLP layers, matched mass | **0.667** | **0.000** | **Early-MLP precision hotspot vanishes under GPTQ** |
| Middle five MLP layers, matched mass | **0.010** | numerical cell not recovered | RTN-specific near-no-effect |

Source: [Table 9, Table 10, Fig. 4, Fig. 5 and Sec. 5.2](https://link.springer.com/article/10.1007/s10791-026-10580-5). GPTQ MLP-only directly reports **CB 0.385, support 0.93, OTHER 0.08**, and attention-only **CB 0.917**. Calibration uses **256 WikiText-2 samples**, no probe-data calibration, group size **128**. Module-count validation: **108 MLP**, **144 attention**, **15 early-MLP** and **15 middle-MLP** projections targeted. [Sec. 3, Sec. 4](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 5C. Matched mass, matched error and layer-depth controls

**Equal parameter mass:** RTN quantizes about **340 million weights** in each of: first five MLP layers, all attention, and five middle MLP layers. Their anchored recall losses are **0.667, 0.135 and 0.010** respectively. First six MLP layers produce cumulative loss **0.677** compared with **0.844** for all MLP layers, while cumulative attention stays <=0.135. **This localization holds for RTN but not GPTQ**, so do not use it as a cross-quantizer map. [Table 10, Fig. 5](https://link.springer.com/article/10.1007/s10791-026-10580-5).

**Cross-quantizer:** GPTQ reduces the all-MLP damage and completely removes the first-five MLP hotspot. The article explicitly says at matched mass GPTQ can make attention more damaging. [Table 9; Sec. 5.2](https://link.springer.com/article/10.1007/s10791-026-10580-5).

**Control C:** A harsher **2-bit attention** perturbation still spares more recall than **3-bit MLP**, per the article's prose. **Control C-prime** also matches observed dequantization error, not just nominal bit-width; the **full control-row values were not recoverable**. [Secs. 4-5](https://link.springer.com/article/10.1007/s10791-026-10580-5).

**Layer-aligned:** The paper reports first-six-layer MLP loss **0.677** against attention loss **0.021** in a layer-aligned comparison, which is still partly confounded by parameter mass. **Gemma's first-five MLP loss is only 0.019**, even though whole-MLP loss is **0.362**. The early-Qwen finding is not architecture general. [Sec. 5.2, Table 11](https://link.springer.com/article/10.1007/s10791-026-10580-5).

**Seed robustness:** For a degraded component condition, CB-Acc **0.146-0.156**, SD **0.005** across studied seeds; CFR **0.781-0.854**, SD **0.027**, showing CFR instability near garbage conditions. The source passages do not expose the complete seed count or seed identifiers. [Methods and appendix references](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 5D. Selectivity: not fact-specific erasure

The paper gives a separate unfiltered control, not the anchor-normalized 1.00 baseline: FP16 recall **0.842**, MMLU **0.657**, WikiText-2 perplexity **10.88**. When *only* the MLP is quantized at RTN 3-bit: recall becomes **0.131** (loss **0.711**); MMLU becomes **0.306** (loss **0.351**); perplexity becomes about **4.46 times** the baseline. Early MLP-only produces MMLU loss **0.273**, PPL **3.27x**, recall loss **0.544**. Attention-only produces MMLU loss **0.024**, PPL **1.08x**, recall loss **0.070**. Copy support remains **1.00** even in the all-MLP condition. [Table 13, Fig. 7](https://link.springer.com/article/10.1007/s10791-026-10580-5).

The math above is directly reported, except that **4.46x** is a ratio and is not an independently inspected PPL cell. It would be incorrect to say the MLP intervention *selectively removes knowledge while retaining all other computation*.

### 5E. Relation type

In each of the five `facts_v2` relations (company HQ, founding year, CEO, film director, composer nationality), RTN 3-bit MLP-only loss is in **0.71-1.00**, early-MLP loss **0.52-1.00**, and attention-only loss **0.06-0.23**. Per-relation anchor sizes **12-31** create broad confidence intervals. Individual relation-cell results from **Table 12 were not recoverable**. No publication-supported mapping of particular MLP projection *gate*, *up*, or *down* to particular factual relations was recovered; the intervention groups all three projections together. [Table 12, Sec. 4](https://link.springer.com/article/10.1007/s10791-026-10580-5).

## 6. Repair, mixed precision, and what it actually proves

The paper is **inference-only diagnostic research**, not a binary-weight recovery-training paper. It does **not** report restoration of lost factual capability by updating signs, per-group scales, or a student model. Its deployment interventions are quantizer choice, per-module allocation and **using supplied evidence**.

The main allocation comparison uses **Qwen2.5-3B GPTQ, n=96**, uniform 3-bit and 4-bit versus **MLP 3-bit/attention 8-bit** (average **3.6 bits**) and **MLP 2-bit/attention 8-bit** (average **2.7 bits**). The latter is nonfunctional. Mixed 3.6 attains open-book **0.99** versus uniform 3-bit **0.80**; however the paper attributes the **+0.19** improvement primarily to reducing support-condition **OTHER 0.20 to 0.01**. It is **garbage recovery**, not evidence of a new context-following ability. Against uniform-4, mixed-3.6 reports **CFR 0.85 versus 0.74**, with OTHER **0.06 versus 0.09**, and **open-book 0.99 versus 1.00**. Mixed-3.6's closed-book accuracy is reported as only **0.07**, meaning it obtains memory-poor but functional retrieval behavior. [Table 14, Fig. 9](https://link.springer.com/article/10.1007/s10791-026-10580-5).

The authors' application-specific precision advice ([Table 17](https://link.springer.com/article/10.1007/s10791-026-10580-5)) is: closed-book factual deployment stays nearer **8-bit**; short, simple gold-in-context copying can tolerate **2-bit-class** GGUF on the tested model; multi-hop reasoning has a **4-bit soft floor**; short one-sentence copy does **not** establish long-context reliability. These are empirical scope recommendations, **not exact g128 binary results**. Long context is markedly worse (see Table 18).

## 7. Article figures and tables audit

**Status key:** "caption" means the indexed article's original caption/figure description was read, **not** the figure raster or graphical values. "partial" means narrative mentions with some actual numbers but not the complete original table cells. **No figure image was read directly.**

| Item | Article content identified | Verification status |
|---|---|---|
| Fig. 1 | PRISM overview; recall vs context and MLP vs attention | Caption/description only |
| Fig. 2 | Closed-book, CFR and OTHER vs precision for Qwen 3B and 7B | Caption/description only |
| Fig. 3 | Two-hop comprehension vs bits and component intervention | Caption/description only |
| Fig. 4 | RTN vs GPTQ component losses at Qwen 3B | Caption/description only |
| Fig. 5 | Matched-weight-mass and cumulative early-depth localization | Described in article prose, original image not read |
| Fig. 6 | Cross-model Qwen/Llama/Gemma component contrast | Caption/description only |
| Fig. 7 | Unfiltered recall, MMLU and perplexity control | Caption/description only |
| Fig. 8 | Qwen MLP vs attention for recall/copy at 3 and 4 bits | Caption/description only |
| Fig. 9 | Mixed GPTQ precision and garbage recovery | Caption/description only |
| Fig. 10 | Harder three-hop RAG | Caption/description only |
| Fig. 11 | Long-context copying and composition | Described in article prose, original image not read |
| Tables 1-2 | Literature comparison and positioning | Descriptions only; full cells unavailable |
| Table 3 | Models, quantizers, hyperparameters and versions | Many method details recovered; **software-version cells unavailable** |
| Table 4 | Metrics and notation | Formulas and descriptions recovered; complete cells unavailable |
| Table 5 | Consolidated findings | Descriptions and selected values recovered; complete cells unavailable |
| Table 6 | PopQA n=164 | Major numbers recovered; other cell values and CI bounds unavailable |
| Table 7 | Cross-model/quantizer recall and CFR sweeps | Endpoints and selected rows recovered; **full middle-precision series unavailable** |
| Table 8 | Leak-free 2-hop n=160 | Six main bit/component point estimates recovered; CIs unavailable |
| Table 9 | Cross-quantizer GPTQ vs RTN | Core MLP/attention/early numbers recovered; remaining columns unavailable |
| Table 10 | Equal-mass and depth | Core intervention deltas and selected OTHER/support recovered; remaining cells unavailable |
| Table 11 | Cross-family quantization | Key MLP/attention numbers recovered; remaining cells unavailable |
| Table 12 | Five factual relations | Range and direction recovered; **individual per-relation rows unavailable** |
| Table 13 | Recall vs MMLU vs PPL | Baseline, major deltas and PPL ratios recovered; full cells unavailable |
| Table 14 | Mixed GPTQ | Bit averages, CB/CFR/support/OTHER selected cells recovered; full cells unavailable |
| Table 15 | Harder three-hop n=80 | Six bit/component point estimates recovered |
| Table 16 | Easy single-hop copy | Ceiling and undefined baseline recovery identified; full cells unavailable |
| Table 17 | Deployment recommendations | Main prose recommendations recovered; full cells unavailable |
| Table 18 | Long-context probes | Six bit/component point estimates for each of two tasks recovered; CIs unavailable |

**Appendix/supplement status:** The article text refers to appendices containing activation patching and unfiltered-score tables, but the complete appendices and any supplement files were not separately accessible. No supplement URL or complete appendix table was verified. Therefore **it would be false to label this an every-table, every-figure full read**.

## 8. Code, dataset locations, availability and audit limits

- Claimed project repository: [Swa-s-tik/PRISM](https://github.com/Swa-s-tik/PRISM). The article asserts that it contains the full pipeline, generated probes, human-label validation, figure/CI scripts and per-item results. **I could not independently open or inspect the repository contents via the accessible tools**, so neither release completeness nor a repository license can be verified. Do not assume the article's CC BY 4.0 license applies to its code.
- [CounterFact-Tracing](https://huggingface.co/datasets/NeelNanda/counterfact-tracing), [PopQA](https://huggingface.co/datasets/akariasai/PopQA), [MMLU](https://huggingface.co/datasets/cais/mmlu), [WikiText](https://huggingface.co/datasets/Salesforce/wikitext). These are the third-party sources explicitly listed by the manuscript. Their individual dataset licenses were **not audited here**.
- `facts_v2`, fictional `comprehension` sets and derived per-item labels are **claimed to be in the project code repository**. I cannot certify anonymously downloadable files without seeing repository listings or download bytes.
- The authors mention a planned Zenodo archived DOI on acceptance, but no concrete Zenodo record is supplied in the inspected article text; do not treat an anticipated deposit as an available artifact.
- The article itself is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as stated on the publisher page.

The strongest reproducibility limitation of this report is **missing direct access to raw tables, figures and code**. The strongest reproducibility limitation of the study until its repository is independently obtainable is that its claimed scores and probe derivations cannot be verified from downloadable raw records here.

## 9. Authors' limitations and additional independent criticisms

### 9A. The paper's own limits

The publisher text explicitly qualifies the research as: inference-only, models 2B-7B, with a principal 3B component experiment; **MLP contains 88% of body weights**, confounding whole-component comparison; equal-mass early-MLP effect **disappears in GPTQ**; Gemma has no early-five hotspot; Llama NF4 is a no-damage negative case; factual loss accompanies large general MMLU/PPL degradation; anchored teacher recall is 1.0 by construction; some settings have high garbage; easy single-hop gold-in-passage copying is a ceiling rather than a sensitive comprehension measure; fictional synthetic facts provide leakage control but limit realism; retrieval success depends on actual retriever recall; and long context is substantially worse. The authors describe activation-patching as weak corroboration because swapping full-precision activations into quantized residual streams causes a distribution mismatch. [Secs. 3-6](https://link.springer.com/article/10.1007/s10791-026-10580-5).

### 9B. Independent additional limitations

1. **No strict binary extrapolation.** This paper's best functional 2-bit result is at 7B with GGUF K-quants and an FP16 `lm_head`. It gives no direct estimate of 1.125-bpw Qwen3-1.7B recall retention. This is a transfer limitation, not a criticism of the measured intervention.
2. **Precision and parameter coverage are entangled.** If a 3-bit MLP destroys much more recall than 3-bit attention, that might reflect more perturbed weights and more high-value computation. This is precisely why the GPTQ equal-mass counterresult matters.
3. **Mechanism vs location.** Breaking a function by perturbing a layer does not prove its information is physically stored in that layer. Without fully selective edits and independent tracing, causal *sensitivity* is not a proof of localized parametric memory.
4. **Distributional validity.** Entity-relation recall prompts on a small anchor set might not predict Qwen3 benchmark MMLU-Redux, GPQA, BFCL or math. The author's PopQA and CounterFact results partially reduce this concern, but many of those cells are already fragile or high garbage.
5. **One-hop ceiling risks a misleading story.** If a test asks the model to reproduce an explicitly stated answer from a short passage, a broken knowledge store can score 100%. More discriminative probes should require selection among distractors, composition and conflicting facts.
6. **Two-bit cliff and binary training are not symmetric.** An RTN-3-bit collapse does not establish that a trained one-bit model must collapse, nor does it establish that training a binary model can recover its facts. Post-training quantization and quantization-aware retraining differ fundamentally.
7. **Confidence intervals are not validation of underlying datasets.** Small anchored probes with Wilson intervals and multiple controls can still be fragile to prompt templates, score classifier choices, and underlying fact accuracy.
8. **Incomplete provenance audit.** Full table cells, independent reproducible code, explicit packages/versions and artifacts were not available here, so the result is suitable to guide hypotheses, not to certify exact loss attribution on our target.

## 10. Independent judgment for strict 1.125-bpw Qwen3-1.7B

### 10A. What legitimately transfers

The design of **paired closed-book, true-support, false-support, and irrelevant-support probes** is strongly reusable. So is reporting **OTHER** as a third outcome instead of interpreting increased counterfactual copying as an improvement. So is comparing **MLP-only and attention-only quantization with an identical true binary codec**, while controlling for number of perturbed weights, calibration, base ability, and final output matrix. The report provides a particularly valuable **falsification example**: a Qwen early-layer hotspot found under RTN **vanished** under GPTQ. This warns that diagnostic rankings depend on the conversion algorithm. [Secs. 3-5](https://link.springer.com/article/10.1007/s10791-026-10580-5).

For **already binary, strictly one-scale-per-128** weights, a pure component-wise 'leave MLP FP16' experiment changes the deploy format and must not be scored as a product improvement. It is allowable only as a diagnostic oracle. The final repair has to change **signs, permitted g128 scales, or equivalent function-preserving transformations**, then deploy with all required matrices binary and evaluate overall capability.

### 10B. Where to look first and where to spend repair budget

**First map repairable loss by output consequence, then attribute by intervention.** On Qwen3-1.7B: collect teacher-correct/student-wrong factual items and prompt variants, compare with one-hop copying and two/three-hop fictional tasks, stratify by relation frequency, and track changed answer margins and nonsensical OTHER responses. Next compare **whole MLP** versus **whole attention** interventions, adjusting for perturbed mass and error; only then consider early layers. This order is supported by the Qwen3B evidence, but **not a claim that every Qwen3 early MLP is the true knowledge locus**.

**Do not infer a five-point gain from PRISM.** The paper does not train models and cannot assign a numerical expected benchmark retention gain to sign/scale repair. It demonstrates *where* one broad class of naive numerical perturbation is damaging, not how to recover a trained dense binary model. Repair priority should follow **target-model scored failures**, not a bit-width histogram borrowed from another architecture.

### 10C. Most consequential correction to the framing

The request asks "where in a network the ability to recall facts is lost" as if there is one intrinsic anatomical address. The article's **strongest insight actually rejects that simplification**. The locus of impairment under a given quantizer is not necessarily the locus of stored knowledge, and the answer changes with calibration. An RTN early-MLP effect that vanishes with GPTQ is an **algorithm-dependent vulnerability map**, not a map of where the facts reside. That distinction should be baked into our 1 Bit Summit damage ledger.

**Bottom line:** PRISM establishes a useful **capability ordering** for the tested models: closed-book recall is fragile, short-context verbatim copying is comparatively robust, multi-hop composition degrades between them and can collapse, and MLP-wide quantization is more disruptive than attention-wide quantization under tested conditions. It does **not** establish binary-specific repair localization, a general early-MLP hotspot, or a five-point restoration procedure for Qwen3-1.7B. [Publisher source](https://link.springer.com/article/10.1007/s10791-026-10580-5).
