# 1 Bit Summit: independent research review, Batch 8

November 25, 2026 | Second reviewer | Research and mathematical audit only

## 0. Not read in full

**Return-condition exception:** This is an extensive but incomplete audit, not certification that the brief's full-reading condition has been met. I continued the three investigations rather than stopping on a blocked source, in accordance with the owner's correction after Batch 7. The source acquisition requests are consolidated at the end. No model training or benchmark execution was performed. The arithmetic below was independently checked with small local scripts. No credentials, paid access or personal-information forms were used.

| Primary source or corpus | Label and access route | What remains missing |
|---|---|---|
| [Boole-1.7B model card](https://huggingface.co/precision-numerics/Boole-1.7B) | Read in full from the primary file, substantive model card via HF rendered page | Separate binary checkpoint and ancillary files not read in full |
| [Boole post](https://precisionnumerics.ai/blog/boole-1p7b) | Read in part, main article, evaluation discussion and chart captions via publisher HTML | Interactive point-by-point chart data and JS assets, raw responses |
| [Boole checkpoint](https://huggingface.co/precision-numerics/Boole-1.7B/tree/main), [GGUF checkpoint](https://huggingface.co/precision-numerics/Boole-1.7B-GGUF) | Read in part, file listings, cards, checkpoint layout documentation; binary payload not read | Actual Safetensors JSON header, byte offsets, all tensor dtypes and values, GGUF directory, scales, file hashes and code comparisons |
| [Boole demo](https://github.com/PrecisionNumerics/boole-demo) | Read in part, repository root, install requirements and raw source files w1.py, vllm_export.py, vllm_quant.py, plugin and model directory helper, CLI, build script; actual implementation inspected | Complete recursive repository tree, all tests and assets, exact GGUF exporter and full runtime-fork diff. GitHub subdirectory and API routes did not reliably return them. |
| [PrecisionNumerics llama.cpp fork](https://github.com/PrecisionNumerics/llama.cpp) | Read in part, repository description and published runtime instructions | Pinned full source tree, build and inference parity evidence |
| [Boole larger preview](https://huggingface.co/precision-numerics/Boole-32B-A2.5B-Preview-GGUF), [organization](https://huggingface.co/precision-numerics) | Read in part, preview card, model listing and reported scores | Binary files, complete publication history, runtime kernels and pruning logs |
| [Founder public discussion](https://www.reddit.com/r/LocalLLaMA/comments/1x452zj/boole17b_a_1bit_qwen317b_model_that_outperforms/) | Read in part, post and selected replies | Every nested reply and cross-platform statement; no claim of complete founder record |
| [AbdelH2O study](https://github.com/AbdelH2O/ternary-bonsai-study) | Read in part, research log, replication reports, forensic reports and actual QAT code via raw GitHub, including forward quantization, model assembly, loss, optimizer and export | Entire recursively enumerated pinned source tree, all run logs and JSONs, all scripts and every report line, checkpoint payloads. GitHub tree/API routes failed; direct raw paths worked for known names. |
| [alllwang reproduction](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary) | Read in full from the primary file, model card; read in part for repository, training file listing | Raw HF trainer route failed, but the rendered blob route then exposed the actual trainer, complete r9 summary and launch script, and start of the run log. All r1-r8 logs, full r9 step log, eval JSONs and independent packed weight verification still missing. |
| [Under-2-bit survey](https://github.com/arpitsinghgautam/llm-quantization-gallery/blob/main/under_2bit_literature_survey.md) | Read in part, raw survey sections on methods, cross-cutting mechanisms and bibliography | Entire gallery and bundled PDFs, exact commit, every source in survey; survey is navigation, not primary empirical evidence |
| [November Bonsai whitepaper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-5-27b-whitepaper.pdf), [September whitepaper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf) | Not read, actual PDF contents not accessible. GitHub wrapper, raw, refs/heads, raw redirect and CDN paths attempted; wrapper is not a PDF read | Both complete PDFs, figures, appendices and raw harness/run metadata |
| [November release article](https://prismml.com/news/bonsai-2-5-27b) | Read in full from the primary file, substantive publisher article | External demo videos and whitepaper separate |
| [November model card](https://huggingface.co/prism-ml/Ternary-Bonsai-2.5-27B-GGUF) | Read in part, benchmark tables, runtime notes and file descriptions directly from card | Every figure, every binary file, all discussions and exact benchmark outputs |
| [GSQ](https://arxiv.org/html/2604.18556), [RCO](https://arxiv.org/html/2605.00649) | Read in part, primary HTML, method and selected experimental sections and tables | Full appendices, complete code and release provenance; not a source-complete reproduction |
| [GSQ-RCO GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF), [Unsloth Dynamic](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/discussions/143) | Read in part, publication records, card and release discussion | Exact evaluated file revisions, all tensor types, allocation recipe, calibration matrix and code |
| [llama.cpp integration](https://github.com/ggml-org/llama.cpp/pull/29600), [PTQ CPU](https://github.com/ggml-org/llama.cpp/pull/29672), [PTQ CUDA](https://github.com/ggml-org/llama.cpp/pull/29676) | Read in part, primary PR status, descriptions and selected technical comments; [backend support](https://raw.githubusercontent.com/PrismML-Eng/Bonsai-demo/main/BACKEND-SUPPORT.md) read in part | All patch hunks, review threads and backend PRs, pinned upstream source/MLX parity test |
| Other literature identified in section 3A | Read in part or not read as explicitly labeled there; arXiv HTML, original publication routes, search results | Full-paper and code audit not yet complete |

Network workarounds: direct raw GitHub paths were substantially more productive than browsing GitHub's UI; HF rendered blob/tree views were more productive than raw HF file URLs. The container's public DNS/network requests failed. HF binary previews did not expose the required metadata in the retrieved representation. I could not issue a successful byte-range request for the binary headers through the available browsing route. The container download helper also failed on the raw November PDF and its GitHub wrapper; the raw PDF web endpoint rejected application/octet-stream. No inaccessible source is represented as fully read. Exact facts from inspected code and independently calculated results are distinguished from documentary claims and provisional leads. I do not claim to have established empirical conclusions from unread papers or uninspected model payloads. Consequently the source-complete empirical conclusions demanded in the brief remain pending.

## 0A. Corrections to the framing before interpreting evidence

1. Boole is the same reported parent and a binary-sign model. Whether it is the **same exact codec and same parameterization** is a separate question. The actual loader proves that the shared embedding/output signs can have two different scale tensors. The stated project format does not automatically permit that. A 16-bit BF16 scale also differs from an FP16 scale even when the byte count is identical.
2. Same benchmark titles do not establish identical evaluation. There is a directly measured difference in the publisher-reported Bonsai baseline between the two reports. That difference is large enough to exceed one project milestone if the denominators are casually mixed.
3. A released pair with the same size and codebook establishes the possibility of two different abilities at a common storage constraint. It does not establish a training path from the older checkpoint to the newer checkpoint. Do not conflate release order with optimizer lineage.
4. 'Under 2 bits' must distinguish entropy, average payload, physical bytes, all unique parameters, and logical matrix coefficients. A two-factor representation with sub-1-bit amortized cost is not one dense binary sign per original weight. A mixed-precision codebook is not uniform binary. A rotated checkpoint is not ordinarily a plain sign matrix in the original basis.
5. The question of completeness is not answerable by a universal negative from a bounded public search. The correct deliverable is a dated inventory with primary-file provenance and explicit unknowns. The current inventory is not yet exhaustive.

## 1. Boole: second same-parent public binary checkpoint

### 1A. Provenance and what the makers disclose

Primary sources: [model card](https://huggingface.co/precision-numerics/Boole-1.7B), [release article](https://precisionnumerics.ai/blog/boole-1p7b), [demo repository](https://github.com/PrecisionNumerics/boole-demo), [founder public discussion](https://www.reddit.com/r/LocalLLaMA/comments/1x452zj/boole17b_a_1bit_qwen317b_model_that_outperforms/). Source scope as in section 0. Publisher statements below are documentary evidence, not a verified training run.

The October 2026 release identifies Qwen3-1.7B as its parent. It targets English non-thinking generation. The author describes in-place binarization rather than the low-rank NanoQuant approach. It explicitly compares against PrismML and ordinary quantizations. The published artifact is a deployable checkpoint rather than a recipe. The inspected materials identify learned scales and packed signs; they do not establish the latent optimizer, learning schedule, loss, token corpus, token count, teacher trajectory generation, temperature, training hardware or whether norms were trained. Do not confuse the demo's inference GPU or vLLM install requirements with the training hardware. Nor should we infer that scales being learned means a particular sign estimator was used.

| Question | Evidence status |
|---|---|
| Parent | Publisher identifies Qwen3-1.7B, not an independently verified parent revision |
| Conversion vs new model | Described as a binary version of pretrained Qwen |
| Sign optimizer | Unknown |
| Scale optimization | Loader documents learned scales; optimizer and parameterization unknown |
| Distillation loss | Unknown |
| Calibration/training text | Unknown |
| Training positions and repeated positions | Unknown |
| Hardware / distributed setup | Unknown |
| Frozen or trained norms | Unknown |
| Tied vocabulary code | Explicit alias in loader |
| Tied vocabulary effective weights | Not guaranteed; separate scales |
| Derivative of Bonsai | Not established; no byte comparison completed |

A second team publishing a stronger candidate is important, but publication by a different organization is not proof that two files have independent training ancestry. The actual mechanism could be independently developed, adapted from the original parent, warm-started from a public binary artifact, or influenced by common earlier research. I found no inspected statement proving a PrismML-derived checkpoint. The proper test is section 1E, not an inference from author identity.

### 1B. Implementation audit: what the Boole loader actually does

Read in part from primary code: [w1.py](https://raw.githubusercontent.com/PrecisionNumerics/boole-demo/main/src/boole_demo/w1.py), [vllm_export.py](https://raw.githubusercontent.com/PrecisionNumerics/boole-demo/main/src/boole_demo/vllm_export.py), [vllm_quant.py](https://raw.githubusercontent.com/PrecisionNumerics/boole-demo/main/src/boole_demo/vllm_quant.py), [vllm_plugin.py](https://raw.githubusercontent.com/PrecisionNumerics/boole-demo/main/src/boole_demo/vllm_plugin.py), [pyproject.toml](https://raw.githubusercontent.com/PrecisionNumerics/boole-demo/main/pyproject.toml). The following is a code-interface audit, not a checkpoint header audit.

The loader discovers modules from names ending in `.weight_scale`. A corresponding `.weight` holds packed bytes or aliases a tensor through Safetensors metadata. It checks two-dimensional U8 code arrays and two-dimensional floating scale arrays. Row counts must match. Input features equal eight times the stored byte width; group size is inferred from the scale width. All discovered modules must agree on their group size. This does not itself prove group 128 for the actual file. The permitted scale dtypes in the implementation include BF16, F16 and F32, although the documented release uses BF16. Only the output head can alias another module. The decoder takes the magnitude of the scale with a floor of 1e-5. The documented bit convention maps the low-order bit first, zero to negative and one to positive.

Most significant finding: the vocabulary signs are shared while the two scale arrays are not tied. Thus with code vector b_g and input scale a_g and output scale c_g, the effective input and output groups are a_g b_g and c_g b_g. Equality holds only if a_g=c_g. A checkpoint with shared codes is not necessarily a checkpoint with tied effective weights.

The Humming exporter preserves the signs as unsigned binary levels, with zero point 0.5 and scale twice the decoded magnitude. Algebraically, 2s(q-0.5)=s(2q-1). Other dense keys are exported in BF16. The special runtime plugin uses Humming for linear layers and handles the packed embedding and vocabulary-head code sharing. This is not a normal stock Transformers BF16 checkpoint. The published vLLM path pins vLLM 0.31.0 and humming-kernels 0.1.16. The demo's installation and export procedure are primary evidence of required plumbing, not a measured successful run here.

The separate [GGUF release](https://huggingface.co/precision-numerics/Boole-1.7B-GGUF) has a larger stated footprint (292.1 MB). The card attributes the increase to separate embedding and output matrices. Even if both use an upstream-recognized binary tensor type, the exact export, actual type directory, scale conversions and output parity still need checking. Do not count the packed Safetensors as directly loadable by an unmodified upstream GGUF loader. Do not call the GGUF incompatible merely because the packed Safetensors needs a plugin. They are different artifacts.

### 1C. Byte accounting and the exact codec question

Independent calculation using the expected [Qwen3-1.7B configuration](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/config.json) and the loader's documented layout. The config and checkpoint payload have not both been pinned and audited to a complete primary revision, so this is a conditional reconstruction rather than an actual tensor inventory.

Assume 28 layers, hidden width 2048, intermediate 6144, 16 query heads and 8 KV heads of width 128, vocabulary 151936, and tied input/output in the original parent.

| Matrix class | Elements per occurrence | Occurrences | Total elements |
|---|---:|---:|---:|
| Q and O projections | 4,194,304 | 56 | 234,881,024 |
| K and V projections | 2,097,152 | 56 | 117,440,512 |
| Gate/up/down | 12,582,912 | 84 | 1,056,964,608 |
| Unique vocabulary matrix | 311,164,928 | 1 | 311,164,928 |
| Total unique matrix coefficients | | 197 | 1,720,451,072 |
| Norm coefficients | | 113 tensors | 123,904 |

The strict g128 sign-and-scale payload is P/8+2P/128 bytes, for P=1,720,451,072. That is 215,056,384 + 26,882,048 = 241,938,432 bytes. If the norm coefficients remain BF16, they add 247,808 bytes. The project needs an explicit decision whether vector norms are part of the strict denominator or a separately reported fixed overhead. This is a general format issue already present for ordinary Bonsai, not an excuse to relax matrix precision.

For Boole's conditional shared-sign/separate-scale layout, let E=311,164,928. The additional E/64=4,861,952 bytes produce 247,048,192 bytes including the assumed BF16 norms. The model card's 247.1 MB is consistent with this prediction plus a small header. That is a strong consistency check, **not direct observation of the file header**.

Using the unique parent coefficient denominator including norms, the predicted payload is 1.148677 bits/weight. The reported decimal file size gives approximately 1.148918. The GGUF card's 292.1 MB gives approximately 1.358151 bits per original unique parent coefficient. Its excess above the packed file includes another 38,895,616 bytes of sign codes plus metadata and any other packing differences. The size difference alone cannot determine every remaining byte.

There are three defensible comparator categories:

- Strict original tied binary g128 FP16: one code and one scale for both vocabulary roles. Required for a fully tied same-parent strict comparison if that is the project interpretation.
- Shared binary signs with role-dependent scales: an interesting near-budget alternative at about 1.149 physical bits per unique coefficient, assuming the reconstruction. It has an extra vocabulary scale degree of freedom.
- Untied binary matrices, each g128: if accepted as two actual logical matrices, nominal 1.125 per matrix coefficient but the architecture and parameter denominator changed. Parent-equivalent storage is higher. It cannot win a fixed-parent storage comparison by increasing the denominator.

The BF16 vs FP16 distinction matters. For finite BF16 numbers that fall within the normal FP16 exponent range, all BF16 significand bits fit exactly in FP16. For values outside that range or near FP16 subnormal boundaries, equivalence must be checked. The loader's 1e-5 clipping floor may itself change the actual value; an exact conversion of stored BF16 scales is not proof of exact effective decoded scales if the runtime applies a floor. Check before claiming a lossless repack.

**Mathematical bound on tying scales.** Suppose a group has shared b in {-1,+1}^128 and two scales a,c. If we replace them by a common t, the unweighted squared error over both roles is 128[(t-a)^2+(t-c)^2]. Minimum t=(a+c)/2 and minimum error 64(a-c)^2. More generally if the two errors are weighted by A and C, the optimum is t=(Aa+Cc)/(A+C), and the group residual is 128 AC/(A+C)(a-c)^2. For task-sensitive curvature, replace A,C by the appropriate local directional curvatures along b; the algebra is unchanged under a diagonal quadratic approximation, but cross-terms between the roles can invalidate separability. Exact tie is possible only when effective scales agree or an actual function-preserving reparameterization removes their differences. An arbitrary per-vocabulary-row rescaling is not generally such a symmetry because input lookup affects the residual stream and output scaling affects competition between logits.

This suggests an important controlled experiment in section 4. No source claims that Boole's advantage is caused by its extra scales. The discrepancy makes that hypothesis testable, not proven.

### 1D. Score reconciliation

Directly inspected [Boole card evaluation settings](https://huggingface.co/precision-numerics/Boole-1.7B#evaluation) and [publisher comparison](https://precisionnumerics.ai/blog/boole-1p7b). The individual interactive chart values and raw outputs were not retrieved, so only the visible averages and directional comparisons are transcribed. The project's original ten-task values come from the supplied brief, not a new reading of PrismML's PDF.

| Evaluation | Teacher | Binary Bonsai | Boole | Ternary Bonsai |
|---|---:|---:|---:|---:|
| Project's supplied original comparison | 58.24 | 40.88 | Not evaluated | Not supplied |
| Precision Numerics comparison | 58.83 | 44.97 | 50.55 | 51.57 |
| Retention within respective matched Precision Numerics row | 100% | 76.44% | 85.93% | 87.66% |

Original retention is 70.1923%. Five percentage points correspond to 2.912 average points, or 29.12 sum points over ten tasks. An original-protocol step would require a mean of 43.792 using the exact supplied baseline rather than rounding the retention. Precision Numerics reports a 5.58-point absolute mean advantage for Boole over binary Bonsai, or 9.485 percentage points of retention on its own teacher denominator. It is not a demonstrated 15.7-point advantage under our protocol. The same reference Bonsai scores 4.09 average points higher in the other reported run. This already exceeds a project milestone's 2.912 mean points and needs explanation before awarding anything.

| Task | Project teacher | Project binary Bonsai | Boole exact per-task score in inspected record | Publisher reports direction vs its own Bonsai |
|---|---:|---:|---|---|
| MATH-500 | 74.0 | 34.4 | Not extracted | Higher |
| BFCL v3 | 71.8 | 34.9 | Not extracted | Lower |
| MMLU-Redux | 66.8 | 43.2 | Not extracted | Higher |
| GSM8K | 83.1 | 66.3 | Not extracted | Higher |
| MBPP+ | 58.2 | 42.3 | Not extracted | Higher |
| HumanEval+ | 57.3 | 45.1 | Not extracted | Higher |
| GPQA Diamond | 32.5 | 20.7 | Not extracted | Higher |
| IFEval | 70.3 | 63.0 | Not extracted | Lower |
| MuSR | 50.1 | 45.1 | Not extracted | Lower |
| IFBench | 18.3 | 13.8 | Not extracted | Higher |

The publisher reports especially large math/code gains. The same comparison gives Q3_K_S=46.57 and Q3_K_M=53.66, with materially greater weight storage. This is not evidence that rounding to 3 bits is generally inferior to 1 bit; the training and format differ.

Evaluation controls disclosed by Precision Numerics: EvalScope 1.4.2; bfcl-eval 2025.10.27.1; native chat templates; thinking off; zero shot; full splits; greedy default, seed 42, top-p 1, no top-k/min-p, repetition penalty 1. GPQA uses temperature .6, top-p .95, ten seeds 42 through 51. MMLU/MuSR/GSM output cap 2048; GPQA/MATH/HumanEval 8192; IFEval/IFBench/MBPP/BFCL 4096. Context generally 16384 and BFCL 40960 subject to model limit. Strict instruction and prompt metrics averaged, augmented code tests pass@1, BFCL macro mean 13 single-turn subsets with native-function mode disabled and no underscore-to-dot conversion, math scoring timeout 10 seconds. Those are useful details, but raw item records and harness modifications remain absent.

Potential causes of protocol difference: checkpoint revision; template text or tokenizer; max length; quantized kernel; dtype; arithmetic extractor; timeout; task version; generation engine; BFCL parser; judge policy; invalid example handling; code sandbox; GPQA repeat aggregation; stopped vs truncated outputs. Check these in a paired replay rather than assuming the paper or the new team is wrong. Re-running the two model files, teacher and ternary comparator with one pinned harness is the empirical reference. The project should use its own same-run binary baseline and provide the original 70.2% external target separately.

### 1E. Independence and the least ambiguous file comparison

A byte-level comparison is the most valuable outstanding work for this item. It needs both Boole and the original published Bonsai binary, each pinned by full revision and SHA-256, and the parent. Align actual tensor names and group direction. Decode into the same orientation and sign convention. Check dimensions, tied aliases, scales, norms and any rotations before comparison. Use streaming per tensor or group; no generation is required.

Measure:

1. Bit agreement, Hamming distances and joint frequencies per layer, matrix role, group and ancestor magnitude quantile, and separate input/output vocabulary roles.
2. Compare group scale distributions and rank correlations, not merely averages. Report exact bit-pattern equality of scales after lossless type normalization, and magnitude ratios.
3. Compare conditional agreement between two independent sign vectors when both are selected using the same parent. Raw agreement is inflated by common ancestry. If independently flipped relative to the ancestor with probabilities p and q in a stratum, expected pairwise agreement is (1-p)(1-q)+pq. Evaluate deviations with strata or conditional permutation nulls. Correlated task gradients can also violate independent flips without shared checkpoints.
4. Search for exact long runs of matching packed codes or scales after canonicalizing group order, not just a global percentage. Exact matching of high-entropy modified groups across many matrices is stronger evidence than matching raw ancestor signs.
5. Check norms and embeddings for exact identity to parent, Bonsai or each other. If Boole's scale roles differ, isolate the extra parameters.
6. Estimate alignment under function-preserving permutations only if a straightforward tensor comparison fails. Do not silently use a free arbitrary rotation that changes the deployed format.

The answer to whether Boole is an independent second conversion is presently unknown. A separate public binary checkpoint is enough to make it an important external comparator. It is not yet a sound strict-codec milestone comparator or assured independent warm-start. Both become much more useful after byte audit and a matched evaluation. It is already a particularly interesting candidate to project back into the original constraint if the scale mismatch is its only structural difference.

### 1F. Larger Boole and other releases

Read in part: [organization listing](https://huggingface.co/precision-numerics), [Boole-32B-A2.5B-Preview-GGUF](https://huggingface.co/precision-numerics/Boole-32B-A2.5B-Preview-GGUF). I found the two 1.7B file-format releases and the larger preview in the retrieved listing. This is a snapshot of visible publications, not proof that no deleted or private release existed.

The preview describes a sparse MoE derivative of Flint, with 2,491 of 12,032 experts pruned and the remaining 9,541 experts assigned mixed 1/2/4-bit precision averaging approximately 1.8 bits. Other weights are four-bit, routers BF16. The advertised 2.5B is active parameters, not a 2.5B dense model; the footprint is approximately 9 GB. Nominal 9e9*8/32e9=2.25 bits per original parameter, not a uniform binary checkpoint. It is evidence of another engineering strategy, not an independent strict 1-bit result below 3B.

| Preview card task | Flint baseline | Boole preview |
|---|---:|---:|
| GSM8K | 96.1 | 93.2 |
| IFEval | 94.8 | 90.6 |
| IFBench | 89.2 | 75.9 |
| LiveCodeBench | 81.9 | 67.3 |
| HumanEval+ | 92.7 | 90.0 |
| MBPP+ | 79.8 | 76.7 |

The preview's sampled generation setting differs from the 1.7B non-thinking evaluation; the scores should remain in their own table. The preview cannot support the strict dense binary recipe claim.

Other relevant small-model release records: [alllwang reproduction](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary) is a dequantized ternary checkpoint discussed in item 2; [PrismML's organization](https://huggingface.co/prism-ml) includes later small ternary family releases; [CAT-Q BitTern](https://github.com/IntelChina-AI/BitTern) and the related [ScaleQ paper](https://arxiv.org/html/2608.01078v1) are research candidates; [ThakiCloud](https://github.com/ThakiCloud/bonsai-1bit-repro) is an independent reproduction lead. Their complete payloads and results were not all audited in this batch, so they are not promoted to additional verified strict-codec releases. Search routes used: HF organization/model pages, GitHub exact project names, public web search for Qwen 1.7B/0.8B binary and ternary conversion, Bonsai replication, 1.125 bits, ScaleQ/CAT-Q, and founder names. A complete enumeration of all public builds since mid-2026 remains unfinished. IQ1 GGUF files are not automatically one-sign g128 files: a lattice or vector codebook plus side information is a different representation even when the average storage is low.

## 2. Independent study of PrismML and low-bit Qwen training

### 2A. Source ledger and study boundaries

Read in part from primary raw files under [replication/](https://github.com/AbdelH2O/ternary-bonsai-study/tree/main/replication). The most valuable direct routes were:

- [PRISM_FORENSICS_17B.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PRISM_FORENSICS_17B.md): storage, ancestry, scales, conditional sign flips and style probes.
- [PHASE1_17B.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PHASE1_17B.md): matched 1.7B forensic and PTQ comparisons.
- [GPTQ_PILOT.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/GPTQ_PILOT.md), [GPTQ_V2.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/GPTQ_V2.md): calibration changes, controls and failures.
- [QAT08.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08.md), [QAT08_CHAT.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08_CHAT.md), [QAT08_MCU.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08_MCU.md): 0.8B training reports and interventions.
- [DIAG_READOUT.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/DIAG_READOUT.md), [CODE_DRIFT.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/CODE_DRIFT.md): diagnostic validation and latent/code movement.
- [QAT17B_DESIGN.md](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT17B_DESIGN.md): planned full 1.7B training, not a completed result.
- [qat_08b.py](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/qat_08b.py): actual implementation; quantizer, STE, signed rotation, frozen teacher and embedding, KL calculation, custom optimizer, training loop, export and selected self-tests inspected.
- [prism_variants_17b.py](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/prism_variants_17b.py), [prism_lineage_17b.py](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/prism_lineage_17b.py): selected actual forensic code.

This is materially more than a README review, but not the entire pinned corpus. The table results in this section are investigator-reported outcomes and not independent replication by the second reviewer. The proper next step is to acquire the entire repository with all included files, freeze its commit, and audit the referenced logs and datasets against the narrative.

### 2B. What the investigator reports about Bonsai 1.7B

The forensic report compares the 1.7B binary and ternary siblings to the parent, rather than extrapolating from 27B. The 1.7B ternary file inventory is reported as 197 quantized matrices and 113 FP32 norm tensors, with tied embedding/head. First-generation Prism 1.7B did not use the later H1024 folding; the investigator separately tested it as an improvement candidate. The [forensics](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PRISM_FORENSICS_17B.md) report identical ternary codes at all 1.72B positions between the g64 and g128 repacks, sampled duplicated scales matching 100% in two blocks and embedding, and 99.998% in one FFN-up tensor. All 13.4M ternary scales and 99.997% of binary scales are reported exactly BF16-representable despite FP16 storage. The binary and ternary embedding scales match every group, with 99.9% sign agreement. The authors interpret the embedding as data-free; static agreement does not prove that historical training never touched it. The embedding looks unusually close to a simple parent-derived quantization. Those observations motivate candidate initialization strategies, not a proven PrismML training process.

Reported fingerprints, with the denominator distinguished:

| Fingerprint | Reported result | Interpretation limit |
|---|---|---|
| Ternary projection zero proportion | ~39.9% | Three-level population, not binary |
| Nonzero ternary sign agreement with ancestor | 89.4% | Conditional on nonzeros |
| Projection group scale relative to ancestor mean absolute weight | medians about 1.73-2.14 by depth | Can arise from distribution/scale changes, not proof of optimizer |
| Binary sign flips vs ancestor | 23.3% overall as described in forensic report | Check exact tensor subset before reconciling counts with other reports |
| Binary scales vs ancestor | ~1.9-2.5x | Larger scale not necessarily larger useful activation |
| Binary agreement on weights zeroed in ternary | 62.7% | Selection effects substantial |
| Binary agrees with ternary on ternary nonzeros | 91.8% | Common ancestry and objective confound lineage |
| Conditional binary flip where ternary flipped | 80%, versus 7% where ternary retained sign | Raw correlation insufficient to prove common optimizer run |

The independent-run control is especially well chosen: compare two runs with common initial parent/data/objective and different quantization masks. Within ancestor-size bins, the reported conditional flip coincidence is 0.89, 0.79, 0.67, 0.53 for the independent runs, against 0.80, 0.78, 0.76, 0.71 for the Prism pair. Thus a substantial correlation can emerge from shared initialization without one checkpoint being trained from the other. This is precisely why Boole ancestry cannot be inferred from Hamming agreement alone.

A useful theoretical observation: under the ternary rule q=sign(w) if |w|>=mean(|w|)/2, zeros depend on the distribution of latent magnitudes. For a zero-mean Laplace latent with mean absolute magnitude b, P(|w|<b/2)=1-exp(-1/2)=0.39347. For a zero-mean Gaussian, mean absolute magnitude sigma sqrt(2/pi), so P(|w|<sigma/sqrt(2pi))=2Phi(1/sqrt(2pi))-1, approximately 0.310. These numbers help explain the reported 32% to 40% shift. But two distributions with the same mean and threshold mass can have very different tails; neither scale nor sparsity identifies the latent distribution. A learned threshold or explicit regularization could produce the same static footprint. The calculation is not a way to infer the training token count.

The report also probes style using GSM8K. The binary or ternary sibling's answers must not be confused: the relevant Phase 1 results pertain to the investigator's Prism reference. The report records markedly different openings even when boxed-answer format and answer lengths are similar. Approximately 0.2% of outputs share the first 200 characters with the parent. On a small 100-question style test, larger Qwen 4B and 8B did not reproduce the Prism distribution of openings. First-token probabilities were not captured. This rules out neither larger-teacher training nor direct parent distillation: a small change in a near-tied opening logit can radically alter the generated trajectory. It is descriptive evidence, not teacher identification.

The report's near-identity of embedding codes/scales across related comparisons suggests parent-derived initialization or freezing. Frozen vs reconstructed identically are observationally equivalent without additional logs. It is not a reason to forbid trainable embeddings in our warm-start.

### 2C. 1.7B and 0.8B PTQ runs

Sources: [Phase 1](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PHASE1_17B.md), [GPTQ pilot](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/GPTQ_PILOT.md), [GPTQ v2](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/GPTQ_V2.md), partial primary reading. Results apply only to each report's specific evaluation.

The investigator pinned a parent revision identified by the short prefix 70d244cc. For 1.7B it reports a no-YaRN decision after a context-setting check: disabling YaRN slightly improves the tested NLL, but costs about 1.5 MMLU points in that comparison. That is a reminder that even an apparently harmless runtime setting can alter measured accuracy.

| Phase 1 comparison at 1.7B | Parent | Released ternary Prism | Best reported GPTQ-H1024 attempt |
|---|---:|---:|---:|
| NLL | 3.067 | 3.285 | 4.591 |
| MMLU letter scoring | 49.0 | 47.7 | 23.5 |
| GSM8K | 82.0 | 74.7 | 0 |
| Retrieval | 99.5 | ~100 | 54 |

The [Phase 1 report](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PHASE1_17B.md) specifies 5,330 clean MMLU-Redux 2.0 items, 1,319 GSM8K test items with 1,024 output token cap, 200 synthetic retrieval registries, and 12 held-out books plus three validation books. Softmax used the first 151,669 vocabulary entries because Prism trims Qwen's padded vocabulary. This is another storage denominator and parity issue. Its author reports reproducing all 310 tensor payloads from the released unpacked Prism checkpoint byte-for-byte using the converter. MMLU letter scoring here is not MMLU-Redux generative scoring in the project's suite. The investigator's reported relative weight error is much larger in Prism than the naive Hessian-optimized attempt, despite better language ability. This is strong motivation to measure function rather than coordinate error. A raw layer relative Frobenius error is not invariant to changes of basis or interlayer scale symmetries. It can be a useful diagnostic in a fixed basis, but cannot serve as a sole optimization target or prove that a weight matrix has been 'destroyed'.

For the 0.8B GPTQ pilot the reported calibration used 64 sequences of 512 positions, 32,768 positions from novels, group 128, 1% Hessian damping, sequential processing, no activation ordering, with tied vocabulary handling at the end. Reported NLL 4.90 versus simple ternary 10.30 and full precision 3.41. In terms of excess NLL, the pilot closed (10.30-4.90)/(10.30-3.41)=78.37% of the naive quantization gap, while still failing serious capability checks. That is not 78% benchmark retention. The v2 2x2 comparison changed calibration budget (256x512) and within-layer staged compensation alongside a mask rule change; reported mean improvement was small, and the strongest remaining result still had a substantial NLL gap. A higher-quality initialization can improve subsequent training, but the raw PTQ result does not establish usability.

### 2C1. Additional runtime and initial-rounding controls

Primary [Phase 0](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/PHASE0_RESULTS.md) and [quality pilot](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QUALITY_PILOT.md), read in part. The 0.8B pinned parent revision is `2fc06364715b967f1860aea9cf38778875588b17`. The investigator reports F32 fold equivalence for H512 and partial H1024, where 24 FFN-down matrices of width 3584 remain unrotated. Reported maximum prefill difference .00242 (H512) or .00299 (H1024), 10/10 matching top tokens. A synthetic GDN grouped-V control changes only the metadata boolean by one byte and takes top-token agreement from 10/10 to 0/10, with max prefill difference jumping from .0432 to 25.16. That fixture is not a quality-preserving derivative; it isolates a runtime graph error. It is valuable for our LFM export validation. The one-shot quality pilot selected unrotated least-squares on validation and reported held-out book NLL 10.2819 versus FP 3.3839. Format acceptance and functional acceptance are separate gates.

### 2D. Actual QAT mechanism and an implementation discrepancy

Primary [qat_08b.py](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/qat_08b.py), selected implementation regions read, not an executed audit. The training code is more revealing than the paper-style narrative.

The student uses a folded latent matrix L=W R^T at initialization with a signed orthogonal Hadamard transform R on blocks. Forward is Q(L)(Rx), where Q is group ternarization with half-rounded scales. The straight-through surrogate has the quantized value in the forward pass and identity gradient to L. Two rules were compared: mean-absolute thresholding and selecting the 86 largest magnitudes in each group of 128 (ties deterministic in sorting). Top-86 has 42 zeros, barring a degenerate zero scale. The scale follows the chosen magnitudes; the discrete mask itself is not a learned separate output variable.

Model assembly freezes all original parameters, then replaces the targeted projections with trainable latent modules. The embedding is quantized in the rotated basis, unfolded to an effective BF16 table, frozen and used as the shared output head. The teacher is BF16 and frozen. The full vocabulary KL uses teacher probabilities and student log-probabilities at hidden positions, with BF16 matrix multiplication and FP32 probability arithmetic. It is forward KL, not label-only cross entropy. The model's cache is disabled for training. The actual loss is chunked; the export writes code/scale payload into a GGUF template, checks size and a decoded group, and records file, latent, protocol and exporter hashes.

An implementation detail worth correcting in our own terminology: the custom optimizer class is named AdamWBF16. Its inspected step updates first and second moments, applies bias correction and a parameter update; it has no explicit decoupled weight-decay term in that step. It is effectively Adam with BF16 stored moments unless an external decay operation exists elsewhere. Calling it AdamW without documenting a decay coefficient would be misleading. Moment arithmetic uses FP32 intermediate values and writes back BF16. This could affect long training, but no causal attribution is justified without matched optimizer comparisons.

Rotation matters: with orthogonal R, (WR^T)(Rx)=Wx exactly before quantization. After quantization the equality is no longer guaranteed. Unless the rotation can be folded into neighboring operators without changing their function, the deployed model needs the activation transform and its metadata. The project must not call a rotated representation identical to unrotated dense binary just because both use one sign and scale per group in their respective stored bases.

### 2E. 0.8B training results and failure of the loss proxy

Primary [QAT08 report](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08.md). The model is Qwen3.5-0.8B, a hybrid architecture, not the dense Qwen3-1.7B target. It uses 18 gated delta-network blocks and six attention blocks, and the training scope described in the report is 150 projections totaling roughly 497M trainable coefficients. The embedding/head remains a fixed ternary effective table, with other original parameters frozen. No binary transfer is proved by this experiment.

Reported training settings: FineWeb-Edu, 65,536,000 positions, 2,000 steps at 32,768 positions/step, sequence length 1024, Adam-style BF16 moments, betas .9/.95, peak LR 1e-4, 50 warmup steps, cosine decay to 10% peak, gradient clip 1, RTX 5070 12GB with reported peak about 7.9 GiB. A training-domain LR probe reports monitor losses of 1.26, 1.13 and 2.80 for 2e-5, 1e-4 and 5e-4 respectively. That is evidence for selecting the tested 1e-4 in that setting, not a universal optimizer choice.

| Run | NLL | Retrieval % | Retrieval margin | MMLU % | GSM8K % |
|---|---:|---:|---:|---:|---:|
| FP teacher | 3.284 | 100 | 8.41 | 48.2 | 55.8 |
| GPTQ | 4.815 | 55 | 0.28 | 22.5 | 0.1 |
| Naive absmean | 10.564 | 52 | 0.01 | 22.5 | not reported |
| Naive top86 | 10.836 | 52 | 0.12 | 22.5 | not reported |
| Trained absmean | 3.799 | 94.5 | 3.44 | 22.5 | 1.1 |
| Trained top86 | 3.773 | 90.5 | 3.25 | 22.5 | 0.2 |

The report's diagnostic logs indicate severe answer collapse, with near-universal A selection on MMLU, very low letter probability, and repetitive/truncated GSM8K outputs. Some apparent math successes were parser artifacts. It is possible to reduce excess prose NLL by roughly 93% while preserving essentially none of the tested math capability. That is the most practical negative finding for our project.

An exact reason in terms of the loss: training KL is an expectation over the training context distribution D. For any evaluation-relevant context region S, if D(S)=0, the objective imposes no direct penalty on errors there. Even if D(S)=epsilon, a severe local KL contribution can be diluted by epsilon. Low KL on prose therefore gives no general guarantee about tool-state transitions, answer letters or multi-step arithmetic. Pinsker-type distribution bounds apply to the same contexts and distributions, not to an unrelated task distribution or arbitrary on-policy trajectories. This is an objective-support issue, not simply insufficient model capacity.

### 2F. Chat mixture, multiple choice, unfrozen parameters and continued training

Sources: [QAT08_CHAT](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08_CHAT.md), [QAT08_MCU](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT08_MCU.md), [DIAG_READOUT](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/DIAG_READOUT.md), partial primary readings.

Chat arm C repeats the original training length with 25% chat positions. The source describes 4,722 completed examples from 10,000 Daring Anteater prompts, generated greedily by the full-precision parent, with a 768-token cap. Total chat positions 16.384M, unique corpus positions about 2.098M, approximately 7.81 passes. This distinguishes processed tokens from unique evidence. The resulting model retains retrieval but restores only modest math and almost no MMLU accuracy. Letter mass increases sharply, yet the answer bias persists. This proves neither that chat is useless nor that more prose is needed. It shows that format recovery and semantic decision recovery differ.

The next arms isolate three interventions. M substitutes 6.25% multiple-choice positions (4.096M, from 12,599 MC items derived from ARC training and in-context FineWeb material) into the C mixture, yielding 25% chat and 68.75% prose. Unique MC positions about 2.666M, approximately 1.54 passes. U unfreezes additional parameters, with a reported 1e-3 LR for their parameter group. B continues the existing C run for another 65.536M positions at a fixed 1e-5 LR. These are not equally initialized arms: B is a continuation; C/M/U require the relevant fixed-token comparison as designed. Do not treat all reported differences as clean single-variable estimates if checkpoint ancestry or data differs.

| Arm | MMLU % | GSM8K % | Book NLL (within MCU report) | Other findings |
|---|---:|---:|---:|---|
| Parent | 48.2 | 55.8 | not transcribed here | Fresh probe 44.3 MMLU |
| C chat | 23.86 | 14.56 | 3.650 | Letter mass ~77.95%; format improves, bias persists |
| M multiple choice | 35.9 | 16.3 | 3.681 | Fresh 35.2, pairwise 58.9, binding 82%, retrieval 93 |
| U unfrozen extras | 22.7 | 15.3 | 3.654 | No broad gain from this specific unfreezing intervention |
| B continued C | 22.7 | 18.4 | 3.640 | ~3.9 GSM absolute points over C |

M did not pass the prespecified 90% binding gate. The author's reported negative hypothesis judgment must be preserved even though raw MMLU improved. The diagnostic mean-log-offset correction also failed an FP reference check (94% vs 99.25% raw in the stated probe). A modified diagnostic after outcomes should be labeled exploratory. It cannot silently replace the original predeclared metric. The 13-gram overlap check addresses direct textual overlap but is not a complete paraphrase/semantic contamination audit.

There is a practical difference between recovery of option-symbol binding, ability to compare the content of two options, and answer selection. A model may know that option A is a worse answer but still emit A due to label bias; conversely a well-calibrated letter distribution does not demonstrate correct content retrieval. Our diagnostic matrix should therefore include shuffled option positions, forced candidate log likelihood under identical answer delimiters, free-form answers, and prompt-template controls, while the fixed official benchmark remains unchanged. These diagnostic tests must not be used to retrospectively redefine a success.

### 2G. Did the author actually train 1.7B?

The retrieved research log and [QAT17B design](https://raw.githubusercontent.com/AbdelH2O/ternary-bonsai-study/main/replication/QAT17B_DESIGN.md) document a planned 1.7B run, design changes, throughput profiling and real 1.7B PTQ/forensic work. They do not establish a completed 1.7B QAT result. A later planned MC12 report URL did not resolve. The proper statement is **no completed 1.7B QAT result verified in the inspected record**, not 'the author never ran it'. The rest of the history, final logs, branches and unmerged work are outstanding.

The design discusses H1024 rotation and BF16 rounding as an optional intervention. A design document is not a completed run, and a throughput smoke test cannot count as one. The reported drift study is also interesting: training arms have much greater code agreement with RTN than the released Prism checkpoint does, with very few flips on significant weights. This could be due to objective support, different optimizer, scale learning, amount of training, latent parameterization or architecture. It cannot identify which without an intervention. It is not evidence that simply maximizing sign flips will improve the model.

### 2H. Other small-scale reproduction: an actual 1.7B training checkpoint

[alllwang/bonsai-repro-1.7B-ternary](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary): model card read in full from the primary file; [training directory](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/tree/main/training) read in part. The raw trainer endpoint failed, but the HF rendered blob route succeeded in the final acquisition pass. I inspected the actual trainer, launch script, summary and beginning of the run log. Full raw eval JSONs and previous runs remain unaudited. This is separate from AbdelH2O's study, and must not be mistaken for completion of its planned 1.7B run.

This release reports a Qwen3-1.7B same-parent ternary checkpoint with H1024 rotation, 86 nonzero/42 zero per g128, including tied embedding/head. The published tensors are dequantized BF16 in the original basis, not a demonstrated physically packed low-bit release. The author says the ternary form can be recovered via the inverse basis procedure. Rounding BF16 unfolded tensors can disturb exact rotated representability; only byte-level reconstruction establishes this. The card reports 20,000 steps x 8,192 positions = 163.84M training positions and summarizes FineWeb-Edu plus forward KL. **The actual launch script, summary and log contradict that abbreviated data/loss description.** The code and run configuration show a mixed corpus and an additional CE term, as detailed below. The optimizer is AdamW with zero decay, cosine LR 6e-5, 20 warmup steps, betas .9/.95, gradient clip 1, microbatch 4, accumulation 2, sequence length 1024, seed 0. Norms and the tied vocabulary are trainable. WikiText-2 test subset perplexity 35, KL 0.651 nats/position, top-1 agreement 66.5%, signs changed 0.034%, mask changes 9.44% vs init.

| Six-task comparison | FP teacher | Released Prism ternary | Independent r9 |
|---|---:|---:|---:|
| ARC-C | 43.0 | 39.4 | 33.5 |
| HellaSwag | 60.5 | 52.5 | 46.5 |
| PIQA | 72.2 | 70.3 | 66.1 |
| Winogrande | 60.5 | 59.0 | 58.3 |
| MMLU | 60.2 | 49.1 | 34.5 |
| GSM8K | 68.8 | 59.1 | 54.7 |
| Calculated ratio of sums | 100% | 90.20% | 80.39% |

Evaluation is lm-evaluation-harness 0.4.13, HF BF16, ARC/HellaSwag/PIQA normalized accuracy, Winogrande accuracy, zero-shot for those four, five-shot MMLU and GSM8K strict-match. The reference is on a materially different six-task suite, and ternary rather than binary. The result does not meet or fail the project's ten-task 70.2% threshold. It is a valuable comparator because it shares the parent, includes the vocabulary constraint, and exposes training artifacts. Its significant shortfall to released ternary Prism despite substantial QAT and small code movement is consistent with the AbdelH2O failure mode. It is not an identical experiment or a proof that particular changes are necessary.


**2H1. Late acquisition: actual r9 trainer and run metadata override the abbreviated card.** The [trainer](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/train_bonsai_repro.py) was read in part (CLI, rotation, quantizer, tied embedding/head, training scope, data, eval, optimizer, export); [launch script](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/run_r9.sh) and [summary JSON](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/summary.json) were read in full from the primary rendered files; [log](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/log.txt) read in part (start/config). This is a concrete example of why the model card cannot substitute for code.

| Actual r9 data mixture | Sampling weight | Expected processed positions (not measured exact counts) |
|---|---:|---:|
| FineWeb-Edu | 25% | 40.960M |
| Cosmopedia, Stanford subset | 15% | 24.576M |
| Wikipedia English | 10% | 16.384M |
| OpenWebMath | 25% | 40.960M |
| MetaMathQA | 25% | 40.960M |

Sampling is at the packed sequence level with a seeded categorical draw; the above is the expectation. The actual run has `data_mix_v2=true`, `quant_embed=true`, `unfreeze_norms=true`, and `ce_weight=0.1`. It is not prose-only distillation. The loss is full next-position forward KL plus 0.1 times observed-token cross entropy. MetaMathQA prompt/answer strings enter the corpus; no held-out contamination audit was verified. That matters particularly for the reported GSM8K score. The code uses fixed signed Hadamard per input width (seed 1234 + width), trains all 196 decoder linears plus vocabulary and norms, and folds back to BF16 for publication. The actual quantizer uses strict magnitude greater-than the kth order statistic, not an exact fixed cardinality in the presence of ties. It does not explicitly FP16-round the scale in the quantizer function. Therefore exact 86 retained values and FP16 scale representability cannot be assumed from the card. An independent repack/reconstruction check is required. The drift statistic averages per-module conditional nonzero sign-flip rates and mask-change fractions, not a global coefficient-weighted sign flip rate.

| r9 checkpoint | WikiText-2 PPL | KL | Top-1 agreement | Reported average sign-flip fraction | Mask change fraction |
|---|---:|---:|---:|---:|---:|
| Initial | 1,329,085.69 | 12.04655 | .000734 | 0 | 0 |
| 2,000 | 58.2557 | 1.20481 | .52801 | .0000206 | .04907 |
| 4,000 | 46.4568 | 1.02619 | .57693 | .0000838 | .06715 |
| 6,000 | 43.2305 | .92102 | .60616 | .0001543 | .07877 |
| 8,000 | 39.8304 | .86424 | .61473 | .0002235 | .08629 |
| 10,000 | 41.7716 | .83465 | .61399 | .0002738 | .09076 |
| 12,000 | 37.6709 | .76353 | .63760 | .0003106 | .09312 |
| 14,000 | 36.8241 | .70690 | .65851 | .0003299 | .09411 |
| 16,000 | 36.2373 | .68628 | .65729 | .0003394 | .09439 |
| 18,000 | 34.6076 | .65815 | .65484 | .0003425 | .09441 |
| Final | 34.9799 | .65115 | .66451 | .0003423 | .09440 |

This is the published JSON record, not a run I executed. Its mask and sign movement nearly flatten as LR decays while KL continues declining. The correct interpretation is not that optimizing for more flips is guaranteed to help; the data support a controlled test of explicit scale optimization, sign movement and a nonzero-LR continuation. The measured run's mixed data and CE loss also mean it cannot be used as a clean replication of AbdelH2O's prose-only KL training. The code's default model revision is not pinned in the call; the exact downloaded parent hash must be obtained before lineage comparison. An export function called during the loop would also need to be defined before use if intermediate save is enabled; r9 did not enable that flag. This is a static code observation, not a claim that the completed r9 failed.

Other reproduction routes examined as leads include [ThakiCloud/bonsai-1bit-repro](https://github.com/ThakiCloud/bonsai-1bit-repro), [sky-is-green forensic repository](https://github.com/sky-is-green/bonsai2-ternary-forensics) and [PrismML community benchmarks](https://github.com/PrismML-Eng/Bonsai-demo/tree/main/community-benchmarks). Read in part or not read as a complete corpus. The larger 27B forensics are not the same as a 1.7B experiment. The current record does not establish an additional completed strict-binary 1.7B training run with a matched ten-task score. These repositories need their actual logs and artifacts before the inventory can be called complete.

### 2I. Implications for our first warm-start experiment

The investigator reports a combination of strong prose improvement, weak task recovery, and very small significant-sign movement. We should not assume a warm-start from an already capable binary model behaves the same as initial conversion from a high-precision parent to ternary. The former begins near a usable solution and is a different optimization regime. The key scientific question is whether the existing function can be locally improved without damaging retained skills.

Copy the exact codec export checks, frozen-teacher provenance, explicit token counts, per-task diagnostics, paired controls and negative-result reporting. Avoid using raw-text NLL or letter mass as the sole graduation gate, relying on a frozen embedding by default, confusing processed with unique tokens, or treating a planned training run as a measured result. Test the warm-start's step-zero identity first, then measure data-mixture effects and scale/sign update separation. Section 4 specifies the causal design.

## 3. Under-two-bit methods, targeted recovery and runtime progress

### 3A. Literature inventory: what the survey adds and what it does not

This subsection begins with navigation and partially read primary sources, not a full new survey of every paper or an empirical ranking. The [June 2026 survey](https://raw.githubusercontent.com/arpitsinghgautam/llm-quantization-gallery/main/under_2bit_literature_survey.md) contains 15 method entries and a useful taxonomy. It predates many of the project's leads and the November releases. The rest of the gallery and bundled papers were not exhaustively read. The survey cannot establish absence of other methods, and I have not treated a survey paraphrase as an experimental fact. The entries below are an acquisition and classification ledger. Numerical values transcribed from inspected primary tables are explicitly scoped to those tables.

| Candidate not explicitly in the brief's existing list | Primary publication / code lead | Family and relationship to the required codec | Reading status in this batch |
|---|---|---|---|
| Original BitNet | [2310.11453](https://arxiv.org/abs/2310.11453) | Binary-native training; not a dense same-parent g128 conversion proof | Not read in full; navigation |
| PB-LLM | [2309.10968](https://arxiv.org/abs/2309.10968) | Partially binarized, salient values retained in more bits; all storage must be counted | Not read in full; navigation |
| Spectra / TriLM and BinaryLM control | [2407.12327](https://arxiv.org/html/2407.12327) | Native ternary/binary training; FP vocabulary excluded from linear quantization | Read in part, architecture/appendix tables |
| MatMul-free LM | [2406.02528](https://arxiv.org/abs/2406.02528) | Ternary native hybrid recurrent architecture; not same-parent transformer conversion | Not read in full; navigation |
| Tequila | [2509.23809](https://arxiv.org/html/2509.23809) | Ternary QAT with differentiable dead-zone reactivation | Read in part, method/experiment tables |
| LittleBit | [2506.13771](https://arxiv.org/html/2506.13771) | KD plus binary low-rank factorization; effective sub-bit rate, not dense sign codec | Read in part, method and results |
| SAGE-PTQ | [2606.05429](https://arxiv.org/html/2606.05429) | Saliency, graph-guided group allocation, lookup scale sharing; mixed bits and index bookkeeping | Read in part, methods/results |
| TWLA | [2606.13054](https://arxiv.org/html/2606.13054) | PTQ ternary plus learned structured rotation and activation allocation | Read in part, methods/table |
| BWLA | [2605.00422](https://arxiv.org/html/2605.00422) | Binary weight PTQ, orthogonal Kronecker reshaping, residual correction and activation constraints | Read in part, methods/results |
| LBLLM | [2604.19167](https://arxiv.org/html/2604.19167) | Three-stage distillation, binary weights plus learned group bitmap; not automatically 1.125 bpw | Read in part, methods/setup |
| Spectral-LLM | [2605.25203](https://arxiv.org/abs/2605.25203) | Spectral rotation candidate, investigate actual precision grid; 2-bit result alone not sub-2 | Not read in full; navigation |
| BinaryMoS | [2406.12311](https://arxiv.org/abs/2406.12311), [code](https://github.com/dongwonjo/BinaryMoS) | Multiple token-adaptive scale experts on shared binary codes; extra storage and inference computation | Read in part, code README and comparison table in LittleBit |
| CAT-Q | [2606.26650](https://arxiv.org/html/2606.26650v1), [BitTern](https://github.com/IntelChina-AI/BitTern) | Ternary sliding-window calibration, important 1.7B lead | Previous-batch primary work; not reaudited in full here |
| ScaleQ-1.58 | [2608.01078](https://arxiv.org/html/2608.01078v1) | Teacher-generated reasoning calibration for ternary PTQ, prior batch's important lead | Previous-batch primary work; not reaudited in full here |
| BitNet Distillation | [2510.13998](https://arxiv.org/abs/2510.13998) | Native/teacher-guided ternary training, separate from inference format | Not read in full this batch |
| NanoQuant | [2602.06694](https://arxiv.org/abs/2602.06694) | Low-rank compression, founder-adjacent work; do not assume Boole uses it | Not read in full; navigation |
| DBellQuant | [BWLA reference/benchmark](https://arxiv.org/html/2605.00422) | Binary distribution shaping lead | Not read, original source still to identify and audit |
| RaBiT | [author publication list](https://d7chong.github.io/) | Related binary method lead; exact scope and connection to Boole unverified | Not read in full; navigation |
| TernaryLLM | Search by method name on arXiv and HF | Potential ternary PTQ/QAT lead; exact eligibility needs primary identification | Not read; search lead only |
| Boole | [release](https://huggingface.co/precision-numerics/Boole-1.7B), [code](https://github.com/PrecisionNumerics/boole-demo) | Binary sign conversion with role-dependent vocabulary scales, section 1 | Partial code and file audit |
| Independent Bonsai reproductions | Section 2 | Ternary or binary research leads, only actual matched results count | Mixed primary access; incomplete corpus |

The already known set is BitNet b1.58, OneBit, BiLLM, ARB-LLM, STBLLM, ParetoQ, BitDistill, EfficientQAT, double binary factorization, AF1, GSQ, EdgeRazor, ASkewSGD, MagR, Qronos, SDQ-LLM, Bi-Mamba and Ternary Mamba. I did not treat these as newly discovered or claim to have reread their full primary corpus in this batch. Prior Batch 5/6 work on CAT-Q, ScaleQ and optimization theory remains separate evidence. EfficientQAT often targets 2+ bits; nominal two-bit runs do not pass the strict under-two criterion. GSQ has an actually reported ternary case but its other configurations can be above two. STBLLM, OneBit, BiLLM and factorization papers require a physical accounting of extra scales, sparsity indices, mixed weights and embedding exemptions rather than comparing nominal bit labels. None of the methods in this ledger is awarded a product trophy.

Specific search families covered: `under 2 bit LLM quantization`, `Qwen 1.7B ternary binary 2026`, `Boole Bonsai reproduction small models`, `binary language model quantization BinaryMoS DBellQuant`, `ScaleQ CAT-Q Tequila`, `Qwen 0.8B ternary QAT`, `Bonsai 1 bit reproduction`, `PrismML Bonsai 2.5 November 2026`, `llama.cpp PTQ1_0 Q1_0 Hadamard`, and exact URLs or author/repository names. Search surfaces were web search, arXiv HTML, Hugging Face model/card/file listings, GitHub rendered and direct raw files, publisher sites and public author discussion. This is a search log, not proof of universal completeness. Several newly surfaced methods still need full-source work, exact release dates, size and weight-coverage verification before inclusion in a complete evidence table.

### 3B. Small-model results worth not missing

The following are primary-table transcriptions from partial readings; they are not a verified survey-wide conclusion or claims of strict-codec equivalence. Where a row is perplexity only, do not transform that to benchmark retention. A model independently pretrained at low precision is a control for capacity, not a conversion of the FP teacher.

**Spectra / TriLM.** [Primary appendix tables](https://arxiv.org/html/2407.12327) span models from 99M to 3.9B, with native ternary and selected native binary controls. In one appendix five-task average, 99M FP 44.3, TriLM 43.5, Binary 39.8; ratios 98.2% and 89.8%. At 560M the corresponding FP/ternary/binary averages are 50.5/48.4/44.5, ratios 95.8% and 88.1%. These are easy-task averages with substantial chance floors. Other appendix measures at 390M show large language modeling gaps (perplexity 77.7 versus 21.9 in one table). The embedding exemption and independent pretraining make it improper to interpret the high accuracy ratios as proof of retention after conversion. The important opportunity is a controlled small-model binary vs ternary capacity comparison; the primary paper is not source-complete in this review.

**Tequila.** [Table 1](https://arxiv.org/html/2509.23809) gives 1B FP average .502, absmean .445, Tequila .471, or 88.65% and 93.82% of the reported FP score. At 3B, FP .580, absmean .510, Tequila .530, or 87.93% and 91.38%. The evaluation is six tasks including ARC, HellaSwag, PIQA, Winogrande and GPQA; 10B QAT positions. The improvement addresses the inactive region of a ternary quantizer by a differentiable reactivation mechanism. A strict binary quantizer has no zero-level dead zone, so literal reuse is not justified. A related opportunity is gradient routing for latent signs that are effectively trapped by the chosen parameterization. The table reports all linear layers within transformer blocks quantized, not verified packed embedding/head inclusion.

**LittleBit.** [Table 1](https://arxiv.org/html/2506.13771) includes OPT-1.3B. FP perplexity 14.62; at nominal 1 bit, OneBit 20.27, BinaryMoS 18.09, LittleBit 20.33; LittleBit .8/.7/.55/.3/.1 BPW gives 21.32/21.99/23.35/28.30/53.76. These are perplexities, not ten-task scores, and the effective factorization budget is not our dense codebook. Under the same table STBLLM .55 nominal yields 123.03. This suggests why a representation with additional structure can be a strong budget comparator but is not a strict dense binary starting point until projected into our feasible set. A direct collapse of two binary factors generally creates multiple values per entry and violates the common magnitude constraint. The paper's accuracy appendix and all code still need audit.

**SAGE-PTQ.** [Table 1](https://arxiv.org/html/2606.05429) includes OPT-1.3B/2.7B with FP perplexity 14.62/12.47. Its LUT-4 case reports 15.63/13.23, with weight bits 1.07 and stated scale bits .009. LUT-3 is 17.90/14.60. At 1.3B and 2.7B those are much smaller excess losses than several comparator quantizers in the same table. However, 1.07+.009 is not a proof of whole-model physical storage; the salient subset, indices, graph partition membership, lookup tables, unquantized tensors, and codebook storage must be audited. The method does not impose uniform equal magnitude g128. This is a high-priority full-code acquisition lead because the claimed small-model PTQ results would be important if reproduced with transparent accounting.

**TWLA, BWLA, LBLLM.** In the inspected TWLA table the smallest model is 7B, and the actual paper uses both asymmetric ternary placement and rotations. BWLA Table 1 includes a 1.16-bit reported configuration and a learned orthogonal/low-rank correction mechanism. LBLLM explicitly stores an additional fine-grained binary bitmap along with the binary weight code and uses 4-bit activations and KV cache; its inspected experiments are Llama-2-7B. Those are not direct evidence of a 3B-or-below strict dense binary conversion. Their optimization or compensation mechanisms can be tested in training while ensuring all extra residuals or bitmap parameters disappear from the final exported model. I have not established exact all-model physical bits, full-precision gaps or embedding coverage for these papers; the missing table entries are genuine research gaps.

**BinaryMoS.** The [official repository](https://github.com/dongwonjo/BinaryMoS) shows token-conditioned scale mixtures on a common sign matrix. This changes the function class relative to a single fixed group scale. Small OPT-1.3B comparison in LittleBit gives perplexity 18.09 vs FP 14.62. That number is a secondary experiment in the LittleBit primary paper, not an independent full reading of BinaryMoS's original report. Treat the scaling mechanism as a possible teacher or offline initializer, not deployable strict g128 without a projection test.

A general caution on all small-model percentages: if both scores have a chance baseline b, raw ratio q/p can look excellent even with low excess-over-chance retention. For example, teacher 40%, student 30%, chance 25% gives raw retention 75% but (30-25)/(40-25)=33.3% of above-chance performance. Our official metric remains the specified raw score ratio; supplementary chance-corrected scores should diagnose failure rather than replace the scoreboard.

### 3C. Bonsai 2.5 27B: independent arithmetic audit of the primary model-card tables

**Source limitation:** Neither the November nor September whitepaper PDF could be read from its actual primary binary file in this session. This section audits the numbers displayed in the [November publisher model card](https://huggingface.co/prism-ml/Ternary-Bonsai-2.5-27B-GGUF) and [release article](https://prismml.com/news/bonsai-2-5-27b), not the unread paper. It is an independent arithmetic audit of author-reported numbers, not empirical reproduction. The requested complete whitepaper audit remains outstanding.

The November 24 release reports Qwen3.8-27B as the same base as the September 17 release. The stated change is better multi-turn tool execution and agent coding, with less repetitive or excessive reasoning. The advertised text weight size remains 5.93 GB in PTQ1_0. The released file set includes alternate packings and separate optional components. These descriptions support a common advertised footprint, not a verified identical tensor inventory or proof of warm-start training. The publisher provides no inspected optimizer lineage, training loss, teacher choice, token distribution or training budget.

Numbers below use the following abbreviations: FP is Qwen3.8-27B, G3/G2S/G2XS are the three displayed GSQ-RCO variants in descending storage, UD is Unsloth UD-IQ2_XS, B2 is September ternary Bonsai 2, B2.5 is November ternary. Exact labels and revision hashes still need the paper/file manifest.

| Displayed storage | FP | G3 | G2S | G2XS | UD | B2 | B2.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Advertised weight GB | 53.8 | 10.1 | 9.3 | 8.4 | 7.6 | 5.93 | 5.93 |
| Advertised bits/weight | 16 | 3 | 2.75 | 2.5 | 2.27 | 1.76 | 1.76 |

Use those figures as the card's advertised text storage, not precisely normalized physical bytes per every model parameter. The 27.36B total includes separately delivered components, while the text path is about 26.89B. A text GGUF byte count includes metadata and padding. PTQ1_0's core 28 bytes per 128 corresponds to exactly 1.75 bits/weight in the core block; 1.76 is a reported effective average. The optional MTP and vision files must be reported separately, and cannot be silently counted in only some competitors.

| Tool / agentic workflow | FP | G3 | G2S | G2XS | UD | B2 | B2.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tau2-Bench | 80.6 | 77.7 | 78.8 | 79.5 | 82.0 | 80.2 | 82.0 |
| tau3-Bench | 72.8 | 70.7 | 69.6 | 67.5 | 67.2 | 69.1 | 73.9 |
| BFCL v3 | 71.2 | 71.6 | 71.8 | 70.2 | 71.5 | 70.3 | 72.6 |
| BFCL v4 | 70.8 | 70.6 | 67.7 | 64.2 | 66.2 | 64.4 | 67.2 |
| AppWorld | 93.2 | 86.1 | 82.8 | 46.5 | 89.6 | 51.2 | 90.5 |
| Independently calculated mean | 77.72 | 75.34 | 74.14 | 65.58 | 75.30 | 67.04 | 77.24 |
| Retention on this group | 100% | 96.94% | 95.39% | 84.38% | 96.89% | 86.26% | 99.38% |

| Agentic coding | FP | G3 | G2S | G2XS | UD | B2 | B2.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Terminal-Bench 2.1 | 70.8 | 66.3 | 59.6 | 53.4 | 53.9 | 52.8 | 60.1 |
| SWE-bench Verified | 80.6 | 73.2 | 75.4 | 74.4 | 71.8 | 60.8 | 75.6 |
| DeepSWE v1.1 | 30.1 | 27.0 | 22.6 | 17.7 | 17.7 | 0.0 | 27.0 |
| Independently calculated mean | 60.50 | 55.50 | 52.53 | 48.50 | 47.80 | 37.87 | 54.23 |
| Retention on this group | 100% | 91.74% | 86.83% | 80.17% | 79.01% | 62.59% | 89.64% |

| General category averages | FP | G3 | G2S | G2XS | UD | B2 | B2.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Knowledge | 86.67 | 85.57 | 83.63 | 82.40 | 80.97 | 83.80 | 84.27 |
| Math | 93.15 | 88.15 | 86.00 | 84.80 | 80.75 | 89.00 | 90.10 |
| Coding | 74.55 | 68.20 | 67.80 | 63.80 | 64.70 | 70.50 | 71.65 |
| Instruction following | 81.15 | 81.95 | 81.40 | 79.25 | 78.20 | 82.55 | 80.90 |
| Vision | 86.07 | 84.73 | 84.07 | 83.16 | 82.64 | 81.89 | 83.66 |
| Equal-category mean | 84.318 | 81.720 | 80.580 | 78.682 | 77.452 | 81.548 | 82.116 |
| Category-mean retention | 100% | 96.92% | 95.57% | 93.32% | 91.86% | 96.71% | 97.39% |

The calculated means agree with the displayed card means after rounding. General categories are not necessarily equal numbers of tasks. With category counts 3,2,2,2,7 as indicated by the table structure, task-weighted means would instead be 85.0125, 82.90125, 81.86125, 80.31375, 79.293125, 81.795625, 82.733125. This is a sensitivity calculation using the displayed rounded category means, not a claim that the authors used the latter weighting. A report must say which aggregation is used. Do not splice earlier September headline percentages to the November suite without checking the denominator, benchmark set and settings.

Key arithmetic:

- Tool group improvement +10.20 mean points, 95.51% closure of previous FP gap: (77.24-67.04)/(77.72-67.04).
- Agentic coding improvement +16.3667 mean points, 72.31% gap closure. It still trails FP by 6.27 points.
- General category improvement +0.568 mean points, 20.51% gap closure. The benefit is concentrated in the formerly weak skills.
- AppWorld +39.3 points, closing 93.57% of the original 42-point gap.
- DeepSWE 0 to 27. Relative percentage improvement from zero is undefined; gap closure is 89.70%. Do not market this as an infinite improvement.
- Instruction average declines 82.55 to 80.90, and the release article reports LiveCodeBench v6 down from 83.8 to 83.0. This is evidence of a trade-off in reported scores, not uniform improvement.
- At least one higher-storage competitor remains superior on some agentic coding measurements. For example G3 agentic average 55.50 vs B2.5 54.23. The broad claim of best at its own storage class differs from the claim of winning every task.

A simple illustrative model of compounded execution failure: if each of L steps independently succeeds with probability p, whole-episode success is p^L. Increasing per-step correctness from .95 to .98 changes 20-step success from .3585 to .6676. Real steps are dependent and adaptive; this is not a fit to AppWorld or DeepSWE, but it demonstrates why a modest per-token or per-turn change can yield a large task-level improvement. Conversely, a modest reduction in repetitive loops can improve success by allowing more useful attempts within a fixed budget without changing factual knowledge.

The model card's thinking-mode settings include xhigh reasoning and sampled generation, unlike the project's non-thinking greedy evaluation. The reported native BFCL v3 mode is not the same as the project's non-native setting. Without exact benchmark commit hashes, episode budgets, sandbox/agent harness, tools, sampling seeds, reasoning caps, judge policy and raw outputs, we cannot assess equivalence or independent replicability. A point estimate of 99.38% retention is not a statistical equivalence result. For example, paired differences can have substantial variability even when two mean percentages are close. Tool success rate, trajectory length, invalid calls, retries, termination reasons, timeout and budget exhaustion must be reported.

The public release article and model-card arithmetic are meaningful artifacts. They are not evidence that the older released weights themselves were further trained rather than independently regenerated from the full parent with a different objective. The only rigorous conclusion available without the lineage is that the reported comparison places substantially different capabilities at the same nominal ternary footprint. The scientific implication is a testable hypothesis that targeted capacity allocation can repair specific behaviors. It does not provide a validated binary warm-start recipe at 1.7B.

### 3D. GSQ and RCO behind the comparison files

Read in part from primary [GSQ paper](https://arxiv.org/html/2604.18556), [RCO paper](https://arxiv.org/html/2605.00649), [published files](https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF). Code repositories and complete appendices were not audited end to end. The following is a method-level description and selected directly transcribed table data, not an empirical conclusion about the exact compared GGUF revisions.

GSQ uses a discrete scalar grid with soft stochastic selection during optimization, letting a Gumbel-softmax relaxation provide gradient information to categorical choices. It differs from simply rounding continuous latent weights and applying the identity STE. The optimization works blockwise and includes scale-only end-to-end tuning. The paper reports FineWeb-Edu for Llama and OpenThoughts for Kimi calibration, ordinarily 4,096 sequences of length 4,096, 20 block epochs for Llama, 10 for Kimi, and one end-to-end scale epoch in the Llama setup. Distinguish unique calibration positions (16.777M for the stated sequence count) from repeated processing in blockwise optimization. Repeated block fitting does not equal the same number of global full-model optimizer steps. No 3B-or-below result was established in the inspected main table.

| Llama-3.1-8B-Instruct, five-task average | Bits per quantized parameter, stated | Score | Calculated retention |
|---|---:|---:|---:|
| FP | 16 | 73.71 | 100% |
| GSQ 3-bit | 3.13 | 72.32 | 98.11% |
| GSQ nonuniform | 2.62 | 69.62 | 94.45% |
| GSQ nonuniform | 2.37 | 69.44 | 94.21% |
| GSQ 2-bit | 2.13 | 68.55 | 93.00% |
| GSQ ternary | 1.71 | 63.44 | 86.07% |
| EfficientQAT 2-bit | 2.25 | 63.79 | 86.54% |
| GPTQ 2-bit | 2.25 | 37.53 | 50.92% |
| QuIP 2-bit | 2.25 | 39.20 | 53.18% |
| QTIP | 2.00 | 69.88 | 94.80% |
| PV-Tuning | 2.27 | 69.83 | 94.74% |

The table explicitly excludes nonquantized tensors from its bit/parameter figure. It does not establish all-inclusive 1.71 bits, nor the target g128 binary code. The table is useful to motivate a two-choice categorical relaxation experiment with only sign categories and one scale per group. With q in {-1,+1}, parameterize p=sigmoid(u), expected code m=2p-1, and use an annealed stochastic binary sample or relaxed m during training. At export use sign(u), not a ternary grid or side vector. The expected-code relaxation has an interior magnitude freedom not present in the hard binary model; hard-forward training and the final export must be tested separately. There is no guarantee of a better local optimum than STE.

RCO is a global budget allocation optimizer. In the inspected quantization experiment it chooses among preconstructed discrete precisions per Qwen3-8B linear layer (252 layers, 2 through 8 bits), using a calibration KL objective and 256 sequences of length 2048. It reports improvements over some competing allocation optimizers, e.g. FineWeb perplexity 20.47 at average 2.25 bits vs EvoPress 21.40 and HIGGS 32.07 in its matched study. This is not the exact GSQ-RCO Qwen3.8-27B evaluation, nor a 1.7B binary result. The relevance of the two methods differs: GSQ offers a discrete optimization strategy; RCO permits nonuniform bit allocation. Our fixed bit rate prohibits the latter as a deployed bit allocation mechanism, but the same global importance reasoning can allocate **training effort**, gradient updates, diagnostic attention, or initialization choices rather than extra stored bits. That transfer is a new hypothesis.

The published GSQ-RCO files are mixed bit-rate comparators on the same reported 27B base. Their smaller nominal averages cannot identify which tensors are higher precision from a filename. Acquire their exact type inventories, the quantization assignments, base revision, calibration and evaluation revision. Do not assume a GSQ-RCO file's type name corresponds to every tensor. No inspected source establishes a verified application of both methods to 3B or less at the requested rate. That remains open rather than a claim of nonexistence.

### 3E. Unsloth Dynamic and what a fair equal-storage comparison requires

Read in part from [official Qwen3.8 release discussion](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/discussions/143) and [model repository](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF). The discussion indicates revised Dynamic v3.1 files and revision history. Dynamic methods assign tensor-dependent quantizers using calibration sensitivity or importance data; the file suffix is not proof of a single scalar bit width. The exact file in PrismML's experiment is not pinned in our recovered record. The author allocation script, importance-matrix bytes, all tensor types and full file metadata have not been inspected. Search also surfaced same-base third-party comparative work [Arki05](https://huggingface.co/Arki05/Qwen3.8-27B-GGUF) and [Xylolabs](https://huggingface.co/Xylolabs/Qwen3.8-27B-GGUF/blob/main/README.md); these are not promoted to confirmed benchmark comparisons without full source review. They are relevant because KL, top-1 agreement and task accuracy can differ across PTQ implementations even at the same reported file size.

The same public organization publishes small Qwen variants, and Precision Numerics' own comparison includes 1.7B Unsloth quantizations. That is evidence of small-model dynamic artifacts in the publisher comparison, not proof that the exact v3.1 27B recipe was transferred unchanged. The full audit needs the exact smaller files, the release-specific recipe, precision mix, parent revision and benchmark outputs. No inference about a 3B-or-below recipe reaching strict binary can be made from the 27B table.

Fair accounting requires recording physical file size, actual tensor payload excluding metadata, unique original parameter denominator, logical effective weights, retained high-precision coefficients, codebooks and scales, side information, optional vision and MTP weights, and any runtime-expanded copies. For training comparisons, use identical full parent, data, objective, generation settings and held-out tasks. Do not compare a 5.93 GB text-only ternary file to a 7.6 GB file that also includes components not used by the tasks without itemizing them.

### 3F. Runtime and codec status, November 25, 2026

Primary PR pages were inspected for merge state, not every code diff. The [Prism backend ledger](https://raw.githubusercontent.com/PrismML-Eng/Bonsai-demo/main/BACKEND-SUPPORT.md) and [November card](https://huggingface.co/prism-ml/Ternary-Bonsai-2.5-27B-GGUF) supply the publisher's compatibility description. A merged pull request proves source integration at a commit, not performance or model parity on every backend.

| Type or operation | Current retrieved evidence | Implication |
|---|---|---|
| Q1_0 | [CPU PR 21273](https://github.com/ggml-org/llama.cpp/pull/21273), [upstream block definitions](https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h) | Existing upstream sign-and-scale type, group 128, 18 bytes/block; relevant direct path for our first model |
| Runtime graph with folded Hadamard metadata | [PR 29600](https://github.com/ggml-org/llama.cpp/pull/29600) merged October 11, commit prefix a9d27ac, 8 commits | Integration of Bonsai 2 family; not a guarantee every architecture consumes identical metadata |
| PTQ1_0 format and CPU | [PR 29672](https://github.com/ggml-org/llama.cpp/pull/29672), Open at retrieval | 128 coefficients, 28-byte block, published ternary packing remains under review |
| PTQ1_0 CUDA | [PR 29676](https://github.com/ggml-org/llama.cpp/pull/29676), Open at retrieval | Model-level acceptance and backend implementation still need validation |
| PQ2_0 | [issue 29058](https://github.com/ggml-org/llama.cpp/issues/29058), [backend ledger](https://raw.githubusercontent.com/PrismML-Eng/Bonsai-demo/main/BACKEND-SUPPORT.md) | Publisher identifies fork-dependent compact representation; don't infer merged from Q2_0 support |
| Q2_0 | November card reports upstream support for the folded model from b11556 | Uses larger payload than PTQ1_0; same effective weights only if packing conversion and metadata are correct |
| LoRA graph support | [PR 30910](https://github.com/ggml-org/llama.cpp/pull/30910) referenced as merged in 29600 discussion | Folded-weight adapter support is not proof of sign/scale training or strict export |

Hadamard backend PRs named in the publisher card: CPU [27779](https://github.com/ggml-org/llama.cpp/pull/27779), CUDA [29096](https://github.com/ggml-org/llama.cpp/pull/29096) and [29100](https://github.com/ggml-org/llama.cpp/pull/29100), Metal [29094](https://github.com/ggml-org/llama.cpp/pull/29094), [29095](https://github.com/ggml-org/llama.cpp/pull/29095), [29602](https://github.com/ggml-org/llama.cpp/pull/29602), Vulkan [29772](https://github.com/ggml-org/llama.cpp/pull/29772), SYCL [29243](https://github.com/ggml-org/llama.cpp/pull/29243) and [29605](https://github.com/ggml-org/llama.cpp/pull/29605), MUSA [30167](https://github.com/ggml-org/llama.cpp/pull/30167), Hexagon [30627](https://github.com/ggml-org/llama.cpp/pull/30627). These individual patches were not all read; these are primary links for the pending runtime audit, not individually certified merge/quality claims. The independent [feature request 32160](https://github.com/ggml-org/llama.cpp/issues/32160) discusses further 1024-wide folded ternary and multi-plane formats. Multiple ternary planes with different scales do not become a single ternary or binary weight merely because they share an activation rotation.

Core codec accounting: Q1_0 = (16+2) bytes per 128 = 1.125 bpw. Two-bit codes plus one 16-bit group scale = (32+2) bytes per 128 = 2.125 bpw. PTQ1_0's 28 bytes per 128 = 1.75 bpw. The mathematical entropy log2(3) is about 1.585, not an actual physical format. A ternary quantizer may be represented by 2-bit codes on disk, 8-bit intermediate compute, or a compact packed representation; these are separate measurements.

MLX: the [1.7B ternary MLX card](https://huggingface.co/prism-ml/Ternary-Bonsai-1.7B-mlx-2bit) reports a 2-bit physical export. The newer 27B MLX variant is separately published and the publisher describes parity checks for its own converted model. Do not infer a generally available native one-bit linear primitive from the existence of 2-bit MLX inference. A full audit of MLX and mlx-lm requires examining quantized matmul, gather, embedding and scale dtype paths at pinned commits. A possible research implementation is unpack binary weights for a reference forward in MLX and use a custom packed inference kernel later; physical checkpoint precision must be reported separately from transient expanded training memory. I did not execute or verify a MLX kernel in this batch.

For a non-Qwen model (particularly LFM) the packed scalar type is architecture-agnostic only at the storage/dequantization level. The runtime must support every relevant operator, correct group orientation and packing, embedding gather, head tying, unusual convolution tensors, norms and state caches. If a three-coefficient convolution kernel cannot be grouped row-wise into 128, a custom flattening scheme or explicit separate overhead accounting is required. The first-generation unrotated Q1_0 route is distinct from Hadamard-folded ternary. Support for one does not prove support for the other or training support. This reinforces Batch 7's graph and tensor-type audit before transferring to Liquid models.

## 4. What the project should do differently

This section is an independent proposal, not claims of experiments already performed. It integrates the mathematically established codec differences and the documented research leads; it does not treat the uninspected papers as confirmed empirical outcomes.

### 4A. Two scoreboards and two binary starting points

Use original 70.1923% as the frozen historical external target and measure our own exact released Bonsai file under the pinned local harness before training. If the matched value differs, do not rebase without publishing both. A five-point improvement of the warm-start should be calculated relative to the same-run teacher and same-run starting checkpoint, while the historical milestone is separately reported. Example: if the local starting checkpoint obtains 76% and later 77%, the historical 75.2% target is exceeded but the warm-start gained only one point. This distinction prevents the protocol from earning a trophy rather than the training.

Boole becomes a second reference immediately in the acquisition plan, but two modes must be distinguished: native Boole (shared sign and dual vocabulary scales) and projected strict Boole (one scale per shared group and FP16). Its native score can help map the small-model Pareto frontier; projected Boole may be a strict warm-start if byte equivalence or controlled retie is demonstrated. No dual-scale result counts as a strict tied model unless the project explicitly revises its codec and denominator. Use the same teacher, tasks and evaluation settings for both.

### 4B. Start from the actual released binary function, not a naive quantization of its decoded weights

For every group decode b and s and preserve them at step zero. If the latent surrogate initializes L=s b and computes scale mean absolute, it must reconstruct the same decoded values, including the exact half-precision scale. If the optimizer has a learned explicit scale, use a positive parameterization with initial effective scale equal to the file's value. Do not normalize scales or use an arbitrary temperature that changes step-zero logits. Preserve exact norms, vocabulary ties, tokenizer, model revisions and graph. Validate per-matrix byte roundtrips, group bit order, scale dtype and first-layer arithmetic before any generation testing. Once permitted to run the model, compare logits to reference at fixed inputs and record worst/mean deviations before declaring the warm-start valid.

A scale-only arm is an important control. With fixed codes b, W=s b, gradient of loss w.r.t. s is sum_j b_j dL/dW_j. A continuous scale update can adjust 128 weights simultaneously without sign flips. A sign flip at position j changes that coefficient by -2s b_j. A first-order estimate of improvement is -2s b_j g_j, and a local quadratic penalty adds 2s^2 H_jj. Thus beneficial candidate flips satisfy a local gradient/curvature tradeoff. These approximations are not global guarantees; validate on held-out contexts. For a joint multi-flip update the off-diagonal Hessian terms matter, especially within a shared group and coupled embedding/head. This is a rationale for comparing scale-only, sign-only and joint updates, not a prescription to force a target sign-flip fraction.

In a tied vocabulary group, the gradient must combine input-side and output-side derivatives of the same parameter. Independent optimization of the two roles gives a different feasible set (as Boole illustrates). Log gradient conflict using dot products or cosine between the two contributions without storing separate deployed scales. A group with strongly opposed gradients is a useful diagnostic for how much tying restricts recovery. If a teacher-style loss on the output role dominates, an explicit feature-side auxiliary loss can investigate balancing the two roles while preserving final tying.

### 4C. Data coverage before optimizer complexity

Design a controlled factorial comparison, not one giant recipe that cannot explain a success. Freeze all benchmark suites, prompt variants and contamination filters first. Use a matched distribution of teacher-generated trajectories outside held-out evaluation data, and report training-token counts and unique evidence separately. Suggested arms:

| Arm | Initialization | Trainable binary fields | Data/objective | Scientific question |
|---|---|---|---|---|
| R0 | Exact released Bonsai | None | No training | Export/harness identity |
| S | R0 | Scales only | Fixed mixed teacher contexts | What is recoverable without sign flips? |
| B | R0 | Signs only | Same contexts and objective | What is recoverable by discrete assignments alone? |
| SB | R0 | Signs and scales | Same | Joint effect and interference |
| P | R0 | Signs and scales | Prose-only, same position count | Does domain support cause differential recovery? |
| T | R0 | Signs and scales | Mixed task contexts, same positions | Teacher-trajectory coverage effect |
| A | R0 | Signs and scales | Same T data plus replay/anchor on retained skills | Catastrophic regression control |
| C | FP parent | Same strict fields | Same objective with frozen conversion initializer | Cold-start formula vs warm-start |
| U | Strict-projected Boole if verified | Same strict fields | Same T data | Dependence on starting checkpoint |

The first three optimization arms can use a common STE baseline. A later two-category soft relaxation, mirror method or discrete coordinate search is compared at identical data and objective, not assumed superior from literature. Preserve a fixed seed family and independent runs. Any new optimizer must improve measured retention or an independently validated scientific outcome. Training cost is not a selection criterion; it is metadata for reproducibility. Equal processed tokens are for causal comparison, not a budget cap.

For task data, use prose/general knowledge; teacher-produced math and code trajectories; answer-selection contexts with shuffled positions; instructions and multi-constraint examples; multi-turn tool execution with tool errors, recovery and successful completion; and a replay buffer of already retained abilities. Use held-out prompts, programmatic task generators where appropriate, distinct datasets, exact-match and semantic deduplication. Do not train on evaluation answers. A teacher can be wrong; retain whether a trajectory was verified and distinguish imitation of the teacher distribution from imitation of ground truth. When comparing parent-generated versus stronger-teacher trajectories, treat teacher identity as its own intervention.

A candidate loss is L = lambda_K E_D KL(p_T||p_S) + lambda_H sum_l E_D normalized hidden error + lambda_A E_R KL(p_R0||p_S). The anchor on retained-skill contexts R reduces destructive drift, but could resist genuine improvement. It should be ablated. All lambdas and feature normalizations must be selected on independent validation. No auxiliary hidden vector, correction matrix or teacher component survives export. The final parameter constraint is hard. It is not permissible to hide an additional correction path in the runtime.

### 4D. Diagnostic outcomes and statistical meaning

The project's ten-task mean stays the only product scoreboard. Add a science panel of raw held-out prose NLL, teacher/student token KL, option binding under permutation, unconditioned and forced-candidate margin, free generation, invalid tool calls, tool result conditioning, task completion and repetition/termination rates, length-conditioned code and math performance, sign flips stratified by group and ancestor magnitude, and scale change distributions. Include both raw and baseline-corrected accuracy where meaningful. Do not select diagnostic thresholds after seeing the official test scores.

The raw mean ratio across ten tasks is R=(sum_i S_i)/(sum_i T_i). For fixed teacher scores, an absolute benchmark-score improvement delta on one task changes retention by delta/(sum_i T_i). With supplied sum 582.4, a 10-point MATH gain is 1.717 percentage points retention. To earn five points using MATH alone requires 29.12 points of absolute gain; across MATH and BFCL an equal split needs 14.56 each. Those two large gaps account for substantial available headroom. But allocating all recovery effort to them could degrade the other eight tasks. Report the entire score vector and enforce prespecified regression gates as a scientific safeguard, even though the product metric is an average.

For uncertainty, preserve paired item outcomes rather than only means. Resample questions within each benchmark and preserve prompt/seed clusters; recompute the ratio using paired teacher/student draws and equal task weights. For sampled GPQA, resample question clusters including their repetitions, not each response as independent. To assess training variance, use independent seeds and show between-run differences separately from conditional evaluation variance. A five-point milestone is a point criterion; a confidence interval that straddles it should be reported as such. Claiming equivalent transfer to LFM requires an equivalence margin and appropriate interval, not merely failure to detect a difference. Use validation sets for tuning and keep final evaluation locked. A fully powered equivalence study cannot be sized without pilot paired variance, correlation, benchmark weighting, and desired confidence level.

### 4E. Probability judgments, before and after this batch

These are reconstructed subjective pre-batch judgments and conservative post-batch judgments, not estimates derived from sample frequencies or claimed archived forecasts. No training or reading budget is used as a reason for the probabilities. The source-complete empirical update remains unavailable; I do not assign a strong update solely because a publisher table reports success.

| Event | Before | After |
|---|---:|---:|
| Further strict training of released 1.7B signs/scales gives +5 retention points over a 70.2% matched starting point on the exact ten-task suite | 50% | 59% |
| A public-work-derived conversion of the full Qwen3-1.7B parent reaches 70.2% on the exact strict format and suite | 35% | 42% |

Reasons: the first event begins in an already functional region of the discrete solution space, and the independently inspected code clarifies that scale-only adaptation, tied-role gradient accounting and hard-export validation are concrete feasible interventions. The publisher's second binary candidate is a useful acquisition lead but its extra scaling degree and unmatched harness prevent counting it as direct strict success. The independent small Qwen reports and 27B model-card comparisons remain provisional documentary leads until complete audit, so they motivate controlled tests rather than a large probability increase. Warm-start may be in a difficult local optimum, the most damaged skills may need capacity reallocation, and the parent teacher's errors or data support may limit improvements. The direction of the second update reflects richer public candidate mechanisms and a clearer cold-start control plan, but no verified public formula in this batch establishes the exact event. Neither estimate implies probability of 99%, and neither is a measured trophy.

A stricter alternative judgment if the owner insists that *only* fully source-complete empirical work can change the probability is to retain 50% and 35% until missing files arrive. The numerical updates above explicitly include my own mathematical/experimental-design assessment, not claims that the unread corpora have been established.

## 5. Consolidated source acquisition requests and completion blockers

The following are requests at the end, not reasons to stop all other research. The first reviewer may retrieve primary files without disclosing its independent scientific analysis. No personal data, paid access or credential request is needed.

### 5A. Request for the first reviewer or the project owner: primary files

1. Retrieve the November [bonsai-2-5-27b-whitepaper.pdf](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-5-27b-whitepaper.pdf) and September [bonsai-2-27b-whitepaper.pdf](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf) as actual PDFs, not HTML wrappers. Include [1-bit-bonsai-8b-whitepaper.pdf](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/1-bit-bonsai-8b-whitepaper.pdf) if the original protocol needs reconciliation.
2. Retrieve a pinned archive of [PrecisionNumerics/boole-demo](https://github.com/PrecisionNumerics/boole-demo/archive/refs/heads/main.zip) with all source/test files and the full commit hash; obtain the relevant [llama.cpp fork](https://github.com/PrecisionNumerics/llama.cpp) diff and exact GGUF export implementation.
3. Retrieve all public [Boole-1.7B](https://huggingface.co/precision-numerics/Boole-1.7B/tree/main) and [Boole-1.7B-GGUF](https://huggingface.co/precision-numerics/Boole-1.7B-GGUF/tree/main) metadata, config, tokenizer, template, manifests, Safetensors header and GGUF tensor directory. Include raw benchmark CSV/JSON or the JS chart data if published in [the release article](https://precisionnumerics.ai/blog/boole-1p7b). Include public discussion threads and all other blog posts with exact URL and date.
4. Retrieve the entire [AbdelH2O repository](https://github.com/AbdelH2O/ternary-bonsai-study/archive/refs/heads/main.zip), including all source files, research notes, reports, protocol JSONs, training logs and raw metrics. Provide the commit hash, branch/tag listing and file manifest; separately supply any public checkpoint files and later 1.7B training records or say which paths are absent from the retrieved snapshot.
5. Retrieve all [alllwang training files](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/tree/main/training), including the trainer, summary JSON, run script, raw evaluation JSON and full logs, and any earlier r1-r8 report. The trainer, r9 launch script, and summary were recovered via rendered HF blobs; no need to re-acquire those unless pinning full hashes. Obtain [ThakiCloud](https://github.com/ThakiCloud/bonsai-1bit-repro) and [sky-is-green](https://github.com/sky-is-green/bonsai2-ternary-forensics) manifests and exact run records that refer to models of at most 3B.
6. Retrieve the full [quantization gallery](https://github.com/arpitsinghgautam/llm-quantization-gallery/archive/refs/heads/main.zip), its bundled papers, and the original paper/code archives for the candidates identified in 3A. Include primary paper PDFs, not just abstracts.
7. Retrieve the exact compared [GSQ-RCO](https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF) and [Unsloth](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF) GGUF directories, calibration manifests, precision assignment files, parent/quantizer revision hashes, and the complete GSQ/RCO papers and code. Pin all file hashes if available.
8. Retrieve PR patch files for [29600](https://github.com/ggml-org/llama.cpp/pull/29600.patch), [29672](https://github.com/ggml-org/llama.cpp/pull/29672.patch), [29676](https://github.com/ggml-org/llama.cpp/pull/29676.patch), [21273](https://github.com/ggml-org/llama.cpp/pull/21273.patch), the Hadamard backend patches in 3F, and exact relevant MLX quantized primitive/embedding code. Include the PR merge status and commit hashes.

### 5B. Technical workaround: read only the binary headers and stream comparisons

No need to transfer gigabytes merely to resolve tensor counts and dtypes. For Safetensors, issue `Range: bytes=0-7` against the public resolve URL, follow redirects, verify HTTP 206 and `Content-Range`, interpret the eight bytes as unsigned little-endian header length H, then fetch bytes 8 through H+7. Save that exact JSON and the source URL, resolved revision, reported length, ETag and SHA-256 if the hub exposes it. A server that returns 200 rather than 206 may be sending the whole file; stop that stream after the needed prefix rather than loading the payload. Validate every data offset against file size, every element count against shape and dtype, and shared-key alias metadata. An HF metadata API's total parameter count is not a substitute for the tensor directory.

For GGUF, progressively retrieve prefix ranges and parse magic, version, tensor count, key-value count, variable-width metadata and tensor directory. A parser must handle strings, arrays and alignment correctly; do not assume the directory is contained in the first 64 KB. Once the data start is known, request just each tensor or sampled group range for code/scale comparisons. For ancestry claims, sampled comparisons are exploratory; full streaming comparisons of both pinned files are needed. Record actual quantization type enums and group layouts against the pinned runtime. Avoid reconstructing a hash from partial bytes; only a fully streamed file can be independently hashed.

If the first reviewer can access the repositories directly, the preferred handoff is one archive of primary text/code, headers, manifests and logs, with a source-to-file mapping. This does not compromise independent analysis. We can calculate the same derivations independently after both reviewers have access to the same raw evidence.

### 5C. Final completion state

The most concrete contribution of the current audit is the mathematically significant distinction between sign sharing and actual weight tying in Boole, the reproducible byte-accounting reconciliation, the implementation-level details of the independent QAT trainer, and arithmetic checking of the November publisher's tables. These are actionable for our experimental design. The complete empirical corpus is not yet acquired. I cannot certify every requested run, every published small-model release, every interactive chart value, every table of the two whitepapers, all code files, exact binary hashes, or the statistical reliability of the vendor benchmark results. A completed source audit must address the requests above rather than treating this draft as source-complete.

End of Batch 8 research document.
