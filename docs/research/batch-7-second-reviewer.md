# 1 Bit Summit: Independent research review, Batch 7

LFM2 transfer, binary compatibility and experimental identification | November 25, 2026

## 0. Scope, corrections and evidence status

This is the independent review, not a completed conversion or a claim of experimental replication. No language model has been trained, evaluated or downloaded in full. All percentages labeled retention are either calculations from published numbers or explicitly subjective forecasts. The four original LFM2 configurations were inspected from their released JSON files; the expected parameter inventory below is independently reconstructed from those configurations and executable architecture definitions, and cross-checked against the released weight-file sizes. It is **not** a claim that the binary Safetensors headers were obtained.

The brief needs four clarifications before the evidence is interpreted.

1. A three-tap convolution kernel has no row dimension divisible by 128. A truly identical binary recipe must define grouping of short tensors in advance, not discover that exception after seeing an LFM2 result. The same problem already exists for small learned normalization tensors. The dense-matrix constraint alone is not a complete file-format specification.
2. LFM2 is a hybrid by block count, not necessarily by weight count. Most of its parameters reside in SwiGLU matrices familiar from transformers. Architecture transfer is not synonymous with replacing every parameter by an unfamiliar operator.
3. The original LFM2 models are not the current Liquid flagship. LFM3 was released October 27, 2026. LFM2.5 also provides unusually useful architecture-matched controls and actual trained low-bit releases. Replacing LFM2 with LFM3 would change the stated hypothesis rather than merely update a checkpoint.
4. Equal relative retention is not equal absolute ability, equal compression damage, or statistical equivalence. A single pair of independently pretrained checkpoints cannot causally identify architecture versus training history. The transfer test can nevertheless be rigorous as a predictive, out-of-family test.

### Not read in full

The strict return condition in the assignment has not been met in full. I continued all three investigations rather than stopping at acquisition problems, as directed by the owner. The source-acquisition handoff is at the end. The status below applies to each source or artifact separately: opening a primary file is not the same as reading every line or verifying its binaries. Findings restricted to a checked configuration or code statement are explicitly identified; incomplete paper readings are not treated as complete evidence. Preliminary leads are not evidence that the claimed conversion will work. The probabilities are judgment, not a result of a fitted literature model.

| Source / primary artifact | Reading label and route | Remaining verification |
|---|---|---|
| [LFM2 Technical Report](https://arxiv.org/html/2511.23404v1) | Read in part, primary HTML v1: architecture, model table, training stages and objective, main language benchmark tables and several appendix settings | Complete PDF figures, all supplementary tables, full evaluation appendix sweep. Direct [PDF](https://arxiv.org/pdf/2511.23404) exceeded web retrieval size limit; export.arxiv alternate and container download unsuccessful. HTML worked. |
| Original [350M](https://huggingface.co/LiquidAI/LFM2-350M/blob/main/config.json), [700M](https://huggingface.co/LiquidAI/LFM2-700M/blob/main/config.json), [1.2B](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/config.json), [2.6B](https://huggingface.co/LiquidAI/LFM2-2.6B/blob/main/config.json) configs | Read in full from primary file through HF blob text | Exact historical revision config routes failed for 350M and 1.2B; compare main with selected immutable snapshot before binding manifests. |
| LFM2.5 [350M](https://huggingface.co/LiquidAI/LFM2.5-350M/blob/main/config.json), [1.2B-Instruct](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct/blob/main/config.json), [1.2B-Thinking](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Thinking/blob/main/config.json), [2.6B](https://huggingface.co/LiquidAI/LFM2.5-2.6B/blob/main/config.json) configs | Read in full from primary files through HF blob pages | Other base, JP, 230M, specialized and multimodal checkpoints not fully audited. |
| Original 1.2B [template](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/chat_template.jinja), [generation config](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/generation_config.json), [license](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/LICENSE) | Read in full from primary files through blob renderings | Verify each file at immutable revision and compare 350M. |
| Original 350M and 1.2B model cards, repository trees, commit pages and weight-file pointer metadata | Read in part, primary HF pages, architecture metadata, usage examples, file listings, size and hash; commit pages accessed | Neither tokenizer JSON nor complete binary header read. No exact on-disk tensor-name certification. Cards for other variants partially read or not read. |
| Safetensors binary headers and weights, both proposed checkpoints | Not read. HF blob pointer page, resolve URL, model metadata endpoints, CDN/range routes and mirror requests attempted; environment did not expose binary bytes | Retrieve header only, then compare key names, shapes, dtype, offsets, file size and pinned SHA. No need for gigabyte download for this audit. |
| Transformers [configuration_lfm2.py](https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/lfm2/configuration_lfm2.py) | Read in full from primary file | Pin library commit, verify original checkpoint compatibility. |
| Transformers [modeling_lfm2.py](https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/lfm2/modeling_lfm2.py) | Read in part, primary raw source, RMSNorm, MLP, RoPE, attention, short convolution, decoder, embedding and tied output forward | Full dependency tree, accelerated kernels, backward and exact old-version parity not audited. |
| llama.cpp [lfm2.cpp](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/models/lfm2.cpp) | Read in part, primary raw source: loader tensors, dense attention and convolution dispatch, FFN and graph | Entire file includes newer decision and MoE paths; no full runtime build/test. |
| llama.cpp [lfm-base.cpp](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/models/lfm-base.cpp) | Read in full from primary file, raw source | Backend-specific ssm_conv implementations not fully audited. |
| llama.cpp [conversion/lfm2.py](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/conversion/lfm2.py) | Read in part, raw source, dense causal-LM class, effective FFN sizing, metadata, conv squeeze; actual path identified after old monolithic script and wrong modular path | Other classes and base conversion logic not fully audited. |
| llama.cpp [llama-quant.cpp](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-quant.cpp), [ggml-common.h](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/ggml/src/ggml-common.h), [Q1_0 PR](https://github.com/ggml-org/llama.cpp/pull/21273) | Read in part, primary code, tensor exclusions and block struct, PR opened | Full mixed-type assignment and backend support matrix at pinned commit not certified. |
| [MLX-LM LFM2 Python implementation](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/lfm2.py) | Read in part from search-indexed primary code; direct raw, refs/heads and GitHub blob attempts returned errors | Exact file and version required. [MLX Swift LFM2](https://raw.githubusercontent.com/ml-explore/mlx-swift-lm/main/Libraries/MLXLLM/Models/LFM2.swift) primary file opened, partial configuration and model implementation inspected; full quantized-loading path not certified. |
| Liquid [model library](https://docs.liquid.ai/lfm/models/complete-library), [hub models](https://huggingface.co/LiquidAI/models), [collections](https://huggingface.co/LiquidAI/collections), launch pages linked in §1 | Read in part: primary catalog rows, relevant release text and tables; full historical catalog pagination, all charts, all variant cards/configs/templates/licenses not finished | Catalog is curated and omits retired models; complete historic API manifest required. |
| Liquid [QAD release](https://www.liquid.ai/blog/qad) | Read in part: all substantive article text and original aggregate benchmark figure opened; deployment figure tabs not all inspected | Training code, complete per-tensor storage and exact recipe not published on article page; inspect released QAD source checkpoints and GGUF metadata. |
| Official QAD GGUF trees (four links in §2), community GGUF trees (links in §2) | Read in full from the listed repository-tree file-list view for the explicitly tabulated files, not their binaries; model cards and other files read in part or not read | Mixed tensor types, actual BPW, scores not inferred solely from filenames. |
| [Bi-Mamba](https://arxiv.org/html/2411.11843), [released repository](https://github.com/Tangshengku/Bi-Mamba) | Read in part, primary paper §§3,4,5, Tables 3,5,6,8 and selected appendix; repository README and tree inspected | Full code audit and exact release payload pending. Numerical observations in §2 are table transcriptions, not independent replication or a compliant binary result. |
| [Scaling Laws for Precision](https://arxiv.org/html/2411.04330), [Training Dynamics](https://arxiv.org/html/2510.06213), [Low-Bit Quantization Favors Undertrained LLMs](https://aclanthology.org/2025.acl-long.1555/) | Read in part: first two primary HTML, selected methods, results and appendix headings; third primary abstract/index only | Complete papers, figures and code, especially causal training interventions. Treat as preliminary evidence, not a quantified LFM2 effect. |
| [ParetoQ](https://arxiv.org/html/2502.02631), [OneBit](https://arxiv.org/html/2402.11295), [Rethinking 1-bit Optimization](https://arxiv.org/html/2508.06974) | Read in part: primary HTML and earlier project research, not a fresh complete audit; table checks where stated | Re-audit multi-family experiment configurations and code. |
| Quamba2, BD-Net, Binary MobileNet, other neighboring papers linked below | Read in part, primary index/abstract or paper excerpts only | Leads, not used as empirical estimates for LFM2. |

No paywall or personal-information request was necessary for the main LFM2 paper or original model cards. Some sources failed because binary retrieval and direct network access were unavailable, not because they were shown to be privately gated. The distinction matters.

## 1. Target model, architecture and provenance

### 1A. Model selection

**Recommendation:** select `LiquidAI/LFM2-1.2B` as the first transfer target and `LiquidAI/LFM2-350M` as the engineering check. These are original-generation, non-thinking general-purpose instruction models, not the newer reasoning-only variants. The main reasons are the common four-model technical report, the identical operator schedule between the two sizes, and the availability of later architecture-matched LFM2.5 controls. This choice favors clean scientific identification rather than the largest current benchmark score.

| Role | Repository and proposed immutable revision | Observed weight identity on main | Status |
|---|---|---|---|
| Target | [LFM2-1.2B](https://huggingface.co/LiquidAI/LFM2-1.2B/commit/40f3da0d0164913923aee9462c23077868b816a3), `40f3da0d0164913923aee9462c23077868b816a3` | [model.safetensors](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/model.safetensors): 2.34 GB, SHA256 `60fef6ef4481c533ce7427793bed50200b55b3c68d0d00c52bc56f207a9acecd` | Commit verified as an available revision; binary identity at that revision not independently verified. |
| Engineering check | [LFM2-350M](https://huggingface.co/LiquidAI/LFM2-350M/commit/f37d3f5c8c5484bc01dad379a595cf4c68c4e70e), `f37d3f5c8c5484bc01dad379a595cf4c68c4e70e` | [model.safetensors](https://huggingface.co/LiquidAI/LFM2-350M/blob/main/model.safetensors): 709 MB, SHA256 `387638dc889ff1a1395c3c2ab9605211e4c7e16f2d375361dd4e423b909a254e` | Same limitation. |

Do not lock these main-branch hashes into a production manifest until matching them to the exact revision. The pinned commit and the binary hash are distinct identifiers. The commit includes the prompt files; a model revision that changes the tool-call template may change BFCL without changing weights.

The 1.2B choice deliberately tests down in parameter count from Qwen3-1.7B, not a perfectly matched architecture-only comparison. It is not the fairest possible same-size architecture study. The 2.6B original is a useful upper bracket but has 30 layers and a different operator schedule. LFM2.5-1.2B-Instruct should be the first robustness extension once the original pair passes, or the target if the project owner changes the stated endpoint from original LFM2 to latest compatible LFM2.5. Its direct QAD comparator is valuable, but it is more heavily post-trained. The LFM2.5-2.6B is not a pure training-history control: vocabulary and RoPE also changed. LFM3-1.7B is a compelling third-family test, not a replacement for the required LFM2 test.

### 1B. Family catalog and releases

This catalog is an initial primary-release inventory, not a certified exhaustive list of every derived hub repository. Exact dates are given only when the announcement was checked. A dash in the date column denotes not independently recovered. Model IDs are linked to their public hub repository or the publisher's catalog; the individual model files for most variants are not audited. Quantized siblings are listed in §2 rather than counted as new pretrained backbones.

| Generation / model | Release date or evidence window | Modality and difference | Primary location |
|---|---|---|---|
| LFM2-350M, 700M, 1.2B | 2025-07-10 | Initial dense text, shared 16-layer hybrid schedule | [launch](https://www.liquid.ai/blog/liquid-foundation-models-v2-our-second-series-of-generative-ai-models); [350M](https://huggingface.co/LiquidAI/LFM2-350M), [700M](https://huggingface.co/LiquidAI/LFM2-700M), [1.2B](https://huggingface.co/LiquidAI/LFM2-1.2B) |
| LFM2-2.6B | 2025, in report | 30-layer dense text | [weights](https://huggingface.co/LiquidAI/LFM2-2.6B) |
| LFM2-8B-A1B | 2025, in report | MoE, ~1B active | [weights](https://huggingface.co/LiquidAI/LFM2-8B-A1B) |
| LFM2-24B-A2B | 2026 | Larger sparse text model; not a validated historical teacher of original LFM2 | [release](https://www.liquid.ai/blog/lfm2-24b-a2b) |
| LFM2-VL-450M, 1.6B, 3B | 2025 | Image-text variants, vision encoder/projector plus language backbone | [official collections](https://huggingface.co/LiquidAI/collections) |
| LFM2-Audio-1.5B | 2025 | Audio-text I/O | [model](https://huggingface.co/LiquidAI/LFM2-Audio-1.5B) |
| LFM2-350M-ENJP-MT, LFM2-350M-Math, LFM2-350M-PII-Extract-JP | - | Specialized translation, math and extraction | [model library](https://docs.liquid.ai/lfm/models/complete-library) |
| LFM2-2.6B-Transcript | - | Specialized transcription text model | [weights](https://huggingface.co/LiquidAI/LFM2-2.6B-Transcript) |
| LFM2-1.2B-Tool | - | Specialized tool use, candidate identified in community tree; official revision not inspected | [community conversion](https://huggingface.co/mradermacher/LFM2-1.2B-Tool-GGUF) |
| LFM2 ColBERT-350M, other extraction/RAG, experimental, longevity and medical variants | - | Specialized/retrieval releases or candidates, not general teacher candidates; exact publisher IDs and access terms require full catalog sweep | [hub catalog](https://huggingface.co/LiquidAI/models) |
| LFM2.5-1.2B-Base, Instruct, JP, VL-1.6B, Audio-1.5B | 2026-01-05 | Same LFM2 backbone class, much longer training, stronger RL/post-training; base and derivative variants | [launch](https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai); [base](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Base), [instruct](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct) |
| LFM2.5-1.2B-Thinking | 2026-01 | Separate reasoning checkpoint, not a switch on original LFM2 | [weights](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Thinking) |
| LFM2.5-350M and 350M-Base | 2026-03 release window | Architecture-matched small text model; improved instruction, extraction and tool use | [release](https://www.liquid.ai/blog/lfm2-5-350m-no-size-left-behind); [weights](https://huggingface.co/LiquidAI/LFM2.5-350M) |
| LFM2.5-230M and 230M-Base | before 2026-08-19 QAD | Smaller dense text | [weights](https://huggingface.co/LiquidAI/LFM2.5-230M) |
| LFM2.5-1.2B-JP-202606 | 2026-06 identifier | Updated Japanese text | [weights](https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP-202606) |
| LFM2.5-8B-A1B, 24B-A2B | 2026 | Sparse text, later generation | [8B](https://huggingface.co/LiquidAI/LFM2.5-8B-A1B), [24B](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) |
| LFM2.5-2.6B and Base | 2026-08 release window | Dense agents, expanded vocabulary, specialist on-policy distillation and agentic RL | [release](https://www.liquid.ai/blog/lfm2-5-2-6b), [weights](https://huggingface.co/LiquidAI/LFM2.5-2.6B) |
| LFM2.5-VL-450M, 1.6B, 3B; 450M-Extract, 1.6B-Extract | 2026 | Multimodal and document extraction variants | [official matrix](https://docs.liquid.ai/lfm/models/complete-library) |
| LFM2.5-Audio-1.5B-JP | 2026 | Japanese audio | [matrix](https://docs.liquid.ai/lfm/models/complete-library) |
| LFM2.5-Encoder-230M, Encoder-350M, Embedding-350M, ColBERT-350M | 2026 | Bidirectional/retrieval variants, not ordinary causal decoder checkpoints | [matrix](https://docs.liquid.ai/lfm/models/complete-library) |
| LFM3-1.7B and Base | 2026-10-27 | New tri-hybrid architecture, 22T pretraining tokens and 256K context claim | [release](https://www.liquid.ai/blog/lfm3), [1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) |
| LFM3-VL-2B, LFM3-Audio-2B, LFM3-Omni-2B | 2026-10-27 | New shared backbone, distinct vision/audio and omni systems | [release](https://huggingface.co/blog/LiquidAI/lfm3) |
| d1-2B, d1-omni-2B, d1-omni-600M and API-only d1 variants | 2026, current catalog | Decision models; not ordinary comparable chat LMs | [matrix](https://docs.liquid.ai/lfm/models/complete-library) |

The November 19 update of the official matrix omits some older releases, including models that remain accessible on the hub. It is a deployment recommendation list, not a complete historic record. A programmatic hub inventory should record repo creation time, first public commit and announcement date separately. They are not interchangeable. The same caution applies to derivative repos and QAD files added to pre-existing repositories. We need not identify every copy of a model as a new family member.

### 1C. Exact architecture from released configurations and source

Read in full: the eight linked configuration files in the source ledger. Model construction and forward paths read directly in the Transformers and llama.cpp code listed there. These are facts about those files, not an inference from parameter-count marketing labels.

Use zero-based layer indices. All other indices are convolution. `d` is residual width, `f` is effective SwiGLU intermediate width. The apparent configuration `block_ff_dim` is not always the actual matrix width. The implementation multiplies by 2/3 when automatic adjustment is on and rounds up to a multiple of 256. This was independently checked in `conversion/lfm2.py`, lines 16-29, and the Transformers MLP implementation.

| Checkpoint | Layers | Attention indices | d | Raw FF width | Effective f | Q/KV heads | vocab | Position config |
|---|---:|---|---:|---:|---:|---|---:|---|
| LFM2-350M | 16 | 2,5,8,10,12,14 | 1024 | 6656 | 4608 | 16/8 | 65536 | 128000 |
| LFM2-700M | 16 | same | 1536 | 10240 | 6912 | 24/8 | 65536 | 128000 |
| LFM2-1.2B | 16 | same | 2048 | 12288 | 8192 | 32/8 | 65536 | 128000 |
| LFM2-2.6B | 30 | 2,5,9,13,17,21,24,27 | 2048 | 10752 | 10752 | 32/8 | 65536 | 128000 |
| LFM2.5-350M | 16 | same as 350M | 1024 | 6656 | 4608 | 16/8 | 65536 | 128000 |
| LFM2.5-1.2B-Instruct | 16 | same as 1.2B | 2048 | 12288 | 8192 | 32/8 | 65536 | 128000 |
| LFM2.5-1.2B-Thinking | 16 | same as 1.2B | 2048 | 12288 | 8192 | 32/8 | 65536 | 128000 |
| LFM2.5-2.6B | 30 | same as original 2.6B | 2048 | 10752 | 10752 | 32/8 | 128000 | 131072 |

Every listed row has 64-dimensional query/key/value heads and eight KV heads. The convolution kernel length is 3, with no learned convolution bias. RMSNorm epsilon is 1e-5. The original four and first three LFM2.5 configs use RoPE theta 1,000,000, while the new 2.6B uses 10,000,000. Original token IDs are pad 0, BOS 1, EOS 7. New 2.6B has pad 124893, BOS 124894, EOS 124900. All configurations indicate BF16 and tied token embedding/output. This is not a proof that every tensor on disk is BF16 or that the tied alias has been deduplicated. The report gives training at 4096 then 32768 positions, so a 128000 positional configuration is not evidence of performance at 128000. Pin 32K as the initially supported comparison ceiling unless separately validated.

The exact small-model layer sequence is C,C,A,C,C,A,C,C,A,C,A,C,A,C,A,C. The 30-layer sequence is C,C,A,C,C,A,C,C,C,A,C,C,C,A,C,C,C,A,C,C,C,A,C,C,A,C,C,A,C,C. Every layer also contains the same style of feed-forward network. It is not a sequence of ten convolution-only layers without MLPs.

For an input column vector h, the decoder is:

```
z = RMSNorm_operator(h)
r = h + (ShortConv(z) or GQA(z))
h_next = r + W2 [SiLU(W1 RMSNorm_ffn(r)) * W3 RMSNorm_ffn(r)]
```

The final embedding norm is applied before multiplication by the tied vocabulary matrix. Attention uses the Q/K per-head RMS normalization followed by RoPE, grouped KV expansion, causal scaled dot-product softmax and linear output. There is no learned positional embedding table in this architecture. For the convolution operator:

```
[B_t, C_t, X_t] = W_in z_t       # three d-dimensional linear outputs
u_t = B_t * X_t                  # first multiplicative gate
v_t = sum(l=0..2) k_l * u_(t-l) # channelwise causal convolution
s_t = C_t * v_t                  # second multiplicative gate
y_t = W_out s_t
```

`*` denotes elementwise multiplication. The orientation of stored tap order depends on cross-correlation convention; the equation labels lags, not disk positions. There is no sigmoid on B or C. The llama.cpp primary implementation has matching B/C/X slicing, product, state prepend, convolution, second product and output projection in `lfm-base.cpp` lines 17-57. This is an actual independent runtime cross-check, not just two architecture diagrams. Cached and uncached conv paths must agree in future parity testing. Padding is masked before the conv projection in Transformers. The history length required by a 3-tap filter is two previous positions; the config field is 3 and runtime state conventions differ.

### 1D. Tensor accounting and exact 128-group compatibility

**Evidence boundary:** the following is the complete expected learned tensor inventory of the two selected configurations, obtained from the actual constructor names and sizes, not a read of the released Safetensors header. It is deliberately marked as such because the assignment specifically required a header audit. Expected dtype is BF16 from the config and file-size cross-check. A duplicate alias, unexpected buffer, mixed dtype or differing immutable revision must be caught by the header script at the end.

The prefix `model.layers.{i}.` is shared by all per-layer tensors. A means the six attention blocks, C the ten convolution blocks. Weight shapes are in PyTorch order (output, input); GGUF dimension order reverses these. The three `feed_forward` matrices appear in all 16 layers. `lm_head.weight` is an alias of `model.embed_tokens.weight` according to source and config, not counted twice.

| Expected name | Copies | Target shape | Target elements / share | Check shape | Check elements / share | Expected dtype |
|---|---:|---|---|---|---|---|
| `model.embed_tokens.weight (tied head)` | 1 | 65536 × 2048 | 134,217,728 / 11.46826% | 65536 × 1024 | 67,108,864 / 18.93142% | BF16 |
| `operator_norm.weight` | 16 | 2048 | 32,768 / 0.00280% | 1024 | 16,384 / 0.00462% | BF16 |
| `ffn_norm.weight` | 16 | 2048 | 32,768 / 0.00280% | 1024 | 16,384 / 0.00462% | BF16 |
| `feed_forward.w1.weight` | 16 | 8192 × 2048 | 268,435,456 / 22.93652% | 4608 × 1024 | 75,497,472 / 21.29785% | BF16 |
| `feed_forward.w2.weight` | 16 | 2048 × 8192 | 268,435,456 / 22.93652% | 1024 × 4608 | 75,497,472 / 21.29785% | BF16 |
| `feed_forward.w3.weight` | 16 | 8192 × 2048 | 268,435,456 / 22.93652% | 4608 × 1024 | 75,497,472 / 21.29785% | BF16 |
| `self_attn.q_proj.weight` | 6 | 2048 × 2048 | 25,165,824 / 2.15030% | 1024 × 1024 | 6,291,456 / 1.77482% | BF16 |
| `self_attn.k_proj.weight` | 6 | 512 × 2048 | 6,291,456 / 0.53757% | 512 × 1024 | 3,145,728 / 0.88741% | BF16 |
| `self_attn.v_proj.weight` | 6 | 512 × 2048 | 6,291,456 / 0.53757% | 512 × 1024 | 3,145,728 / 0.88741% | BF16 |
| `self_attn.out_proj.weight` | 6 | 2048 × 2048 | 25,165,824 / 2.15030% | 1024 × 1024 | 6,291,456 / 1.77482% | BF16 |
| `self_attn.q_layernorm.weight` | 6 | 64 | 384 / 0.00003% | 64 | 384 / 0.00011% | BF16 |
| `self_attn.k_layernorm.weight` | 6 | 64 | 384 / 0.00003% | 64 | 384 / 0.00011% | BF16 |
| `conv.in_proj.weight` | 10 | 6144 × 2048 | 125,829,120 / 10.75150% | 3072 × 1024 | 31,457,280 / 8.87411% | BF16 |
| `conv.out_proj.weight` | 10 | 2048 × 2048 | 41,943,040 / 3.58383% | 1024 × 1024 | 10,485,760 / 2.95804% | BF16 |
| `conv.conv.weight` | 10 | 2048 × 1 × 3 | 61,440 / 0.00525% | 1024 × 1 × 3 | 30,720 / 0.00867% | BF16 |
| `model.embedding_norm.weight` | 1 | 2048 | 2,048 / 0.00017% | 1024 | 1,024 / 0.00029% | BF16 |
| Total unique expected weights | 148 | | 1,170,340,608 | | 354,483,968 | |

Cross-checks:

| Model | Expected unique parameters | BF16 payload bytes | Ideal 1.125-bpw payload bytes |
|---|---:|---:|---:|
| 350M | 354,483,968 | 708,967,936 | 49,849,308 |
| 700M | 742,489,344 | 1,484,978,688 | 104,412,564 |
| 1.2B | 1,170,340,608 | 2,340,681,216 | 164,579,148 |
| 2.6B | 2,569,272,320 | 5,138,544,640 | 361,303,920 |
| 2.5-2.6B | 2,697,198,592 | 5,394,397,184 | 379,293,552 |

The BF16 sizes match the rounded hub file sizes for 350M and 1.2B. The change in vocabulary alone adds 127,926,272 parameters to the newer 2.6B, with otherwise matching widths and operator counts. These checks give confidence in the reconstruction, not certification of the serialized tensors.

In the 1.2B target, the three MLP matrices account for 68.80955% of all weights; the tied embedding is 11.46826%; the four attention matrices together account for approximately 5.376%; the conv projections account for 14.33533%; actual conv kernels are 0.00525%. In the check model the corresponding fractions are approximately 63.89355%, 18.93142%, 5.32446%, 11.83215% and 0.00867%. The unusual operation occupies a tiny number of kernel weights but influences every token in most layers. Its structural sensitivity cannot be ranked by parameter count.

All dense matrices have both dimensions divisible by 128. This includes vocabulary rows, GQA K/V projections with 512 outputs, and all effective FFN widths. The kernel has shape `(d,1,3)`. The final dimension 3 does not divide 128; the entire kernel has `3d` elements and is divisible. The Q/K norm vectors have length 64 each. Every other norm length is divisible by 128. A single group of 128 can fit a pair of Q/K norm vectors, if an explicitly defined cross-tensor group is allowed; sharing their scale may hurt. Alternatively pad each 64-vector to one group (12 partial groups per model), which adds 768 sign slots, i.e. 96 bytes relative to the unpadded sign budget, and 12 scales rather than 6, i.e. 12 extra bytes. This is 108 bytes relative to perfectly pooled grouping. It is not exactly 1.125 bpw across useful entries. State the real payload and do not silently count padding as learned weights.

The brief requires the embedding and head included, but does not explicitly settle whether normalization gains are subject to the binary constraint. I recommend distinguish **strict-all** from **dense-only** and commit to strict-all for the literal claim; do not relabel the latter as the former. Keeping all norms and conv kernels at FP16 would raise ideal effective payload to about 1.12665 bpw on the 1.2B and 1.12774 bpw on 350M. The fractional overhead is tiny but the functional exception could be enormous. A five-point trophy cannot be credited to a hidden precision exemption.

The best deterministic convention to test is: rowwise contiguous grouping for all eligible dense matrices, tap-major grouping across channels for short depthwise filters, and an explicitly universal deterministic rule for tiny vectors, with padding counted. The tap-major change is a serialization/shape rule, not a learned codebook. It can be declared before Qwen fitting and applied automatically to any short depthwise tensor. It is not compatible with stock rowwise Q1_0 storage of a tensor whose fastest dimension is 3 without reshaping or a special loader. One could instead flatten every short tensor row-major into groups, but that would couple unrelated tap positions; see §3C. The project owner must decide this rule before the primary result is unblinded.

### 1E. Training provenance and distillation

The original technical report's §3.1-3.3 was inspected in primary HTML. Dense models are reported to use 10T initial tokens at 4096 context plus 1T higher-quality tokens at 32768 with accelerated learning-rate decay. Approximate original mixture: 75% English, 20% multilingual, 5% code. Half of code examples use fill-in-the-middle. The 8B-A1B mixture shifts toward code and uses 12T initial plus 1T mid-training. The post-training sections report multi-source SFT, preference training and model merging. The SFT figure of 5.39 million samples across 67 sources and three epochs was found in the report; a complete per-stage mixture/reward/optimizer extraction is still outstanding. No original token corpus or teacher logit cache was retrieved.

The teacher is LFM1-7B. Do not infer that LFM2-8B-A1B or 24B-A2B was this teacher merely because it is larger. The latter releases offer alternative supervision, not the original training target. I did not obtain a public exact LFM1-7B teacher checkpoint. Its availability is unverified, not proven impossible. The correct teacher for our primary conversion is the frozen selected LFM2 checkpoint itself, just as Qwen3-1.7B is the parent in the Qwen experiment. This avoids making the experiment contingent on unreleased internal weights and avoids teacher leakage from a larger model.

The original training objective is worth reproducing independently. Let T be the teacher's top 32 token IDs for a context, p=P(T), q=Q(T). For full distributions P and Q, partitioning vocabulary gives exactly

```
KL(P || Q) = KL(Bern(p) || Bern(q))
           + p KL(P(.|T) || Q(.|T))
           + (1-p) KL(P(.|not T) || Q(.|not T)).
```

The report retains the first two terms and applies conditional temperature and tau-squared scaling to the second. At temperature one it is a lower bound on full KL. For non-unit temperature, the tempered quantity is not literally a bound on untempered full KL. The first term ensures total selected mass is matched; a softmax normalized solely within T discards that signal. The tail distribution is not matched except for total mass. This may be valuable for our own general recipe, because Qwen and Liquid have different vocabularies and tail shapes. It should be a fixed algorithmic choice rather than a rescue added only to LFM2. We can compare all-logit KL and top-k mass-aware KL without relying on proprietary teacher data.

The later LFM2.5-1.2B release explicitly increases initial pretraining from 10T to 28T tokens and scales up reinforcement-learning post-training ([Jan 5 announcement](https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai)). It is therefore a nearly shape-matched natural history contrast, not an independently controlled treatment: exact corpus, LR, RL and teacher changes are bundled. The August 2.6B announcement also describes successive SFT stages, domain expert branching, on-policy token-level distillation from those experts, followed by agentic GRPO in actual harness environments ([release, Training Pipeline](https://www.liquid.ai/blog/lfm2-5-2-6b)). The newer 2.6B vocabulary prevents treating it as only a training-history contrast.

The project's statement about LFM2's large token count is true in absolute terms, but does not imply it is more extensively trained than Qwen. The Qwen3 family report describes a roughly 36T-token pretraining corpus ([Qwen3 Technical Report](https://arxiv.org/abs/2505.09388), not read in full in this batch). The exact token exposures of the 1.7B parent require confirming the report and checkpoint. On the original LFM2 size calculations, 11T/1.170B is about 9,399 training tokens per unique parameter, versus 31,031 for the 350M. The ratio alone does not establish quantization fragility: tokenizers, distributions, loss geometry, teacher targets and learning-rate schedules differ.

### 1F. Published scores and comparability

The original report's Tables 6 and 7 were checked in primary HTML. The following selected score rows preserve source values. They are not a complete scrape of every reported metric. All are percentages in the paper's own setting, not scores generated during this review.

| Metric | LFM2-350M | LFM2-700M | LFM2-1.2B | LFM2-2.6B |
|---|---:|---:|---:|---:|
| MMLU | 43.43 | 49.90 | 55.23 | 64.42 |
| MMLU-Pro | 15.85 | 18.65 | 19.71 | 25.96 |
| GPQA | 27.46 | 28.48 | 31.47 | 26.57 |
| IFEval | 65.12 | 72.23 | 74.89 | 79.56 |
| IFBench | 16.41 | 20.56 | 20.70 | 22.19 |
| Multi-IF | 32.85 | 40.92 | 45.28 | 60.26 |
| GSM8K | 30.10 | 46.40 | 58.30 | 82.41 |
| GSMPlus | 22.16 | 29.99 | 36.09 | 60.75 |
| MATH-500 | 24.20 | 31.80 | 42.40 | 63.60 |
| MATH level 5 | 5.79 | 11.27 | 18.61 | 54.38 |
| MMMLU | 37.99 | 43.28 | 46.73 | 55.39 |
| MGSM | 29.52 | 45.36 | 55.04 | 74.32 |

Source: [technical report Tables 6 and 7 and Appendix B](https://arxiv.org/html/2511.23404v1). In particular the source's GPQA protocol uses the Diamond set with ten choice-order permutations; results from permutations of one question are not independent questions. Selected settings checked in Appendix B: greedy generation; GSM8K 5-shot and MATH-500 4-shot, 4096 generation limits; IFEval/IFBench use their specified aggregates and greedy settings; longer 8192-token ceiling for some knowledge tasks. The exact suite revisions, shot construction and scorers still need export. The report's Qwen3-1.7B GSM8K result of 51.40 is not the 83.1 from PrismML's reference, illustrating the magnitude of harness dependence.

Of our ten metrics:

| Project task | Original LFM2 public coverage found | Action |
|---|---|---|
| MATH-500 | Yes, report | Re-run exact common harness. |
| BFCL v3 | Yes for 350M in later release comparison; complete original 1.2B v3 score provenance not established | Do not substitute BFCL v4. |
| MMLU-Redux | Not verified; MMLU and MMLU-Pro are different datasets | Obtain exact Redux version. |
| GSM8K | Yes | Match shots and answer extraction. |
| MBPP+ | Not verified | Run exact EvalPlus plus version. |
| HumanEval+ | Not verified | Same. |
| GPQA Diamond | Yes | Match choice ordering, answer extraction and aggregation. |
| IFEval | Yes | Same strict/loose and prompt/instruction averaging. |
| MuSR | Not verified | Re-run. |
| IFBench | Yes | Same rules and any judge version. |

A later public result for the original 350M is useful. The [LFM2.5-350M release](https://www.liquid.ai/blog/lfm2-5-350m-no-size-left-behind) gives a common publisher comparison across both checkpoints:

| Metric | Original 350M | 2.5-350M |
|---|---:|---:|
| GPQA Diamond | 27.58 | 30.64 |
| MMLU-Pro | 19.29 | 20.01 |
| IFEval | 64.96 | 76.96 |
| IFBench | 18.20 | 40.69 |
| Multi-IF | 32.92 | 44.92 |
| CaseReportBench | 11.67 | 32.45 |
| BFCL v3 | 22.95 | 44.11 |
| BFCL v4 | 12.29 | 21.86 |
| tau2 Telecom | 10.82 | 18.86 |
| tau2 Retail | 5.56 | 17.84 |

These differences are **teacher capability**, not evidence of quantization robustness. The original 350M IFEval and IFBench numbers differ from the technical report; they should not be pooled as repeated runs without matching settings. The newer 2.6B release uses its own benchmark suite and sampling, including BFCL v4 and agent benchmarks; those numbers have not all been extracted. The current audit cannot honestly claim every published LFM2 score or an exhaustive independent leaderboard. Independent benchmark harnesses should be searched and ingested as item-level raw results, not as leaderboard screenshots alone.

### 1G. Prompt and tokenizer contract

The original 1.2B card demonstrates a native ChatML prompt with `<|startoftext|>` then role-delimited `<|im_start|>user` / `<|im_end|>` and an assistant generation prefix. It recommends sampling temperature 0.3, min-p 0.15, repetition penalty 1.05 in the example, not necessarily as the benchmark defaults ([card](https://huggingface.co/LiquidAI/LFM2-1.2B)). The actual generation JSON has only BOS/EOS/pad and Transformers version, not these sampling defaults. The 350M card uses the same example settings.

The inspected [Jinja template](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/chat_template.jinja) inserts the system role when supplied or when tools require instructions, serializes tool definitions, emits Python-like function calls within special tool-call markers, wraps tool results and appends the assistant marker when requested. It is not the same syntax as Qwen's tool-call template. The native template must be used on teacher and converted model, including exact generation prompt and stop tokens. Do not strip tool definitions or reasoning content in one but not the other. No thinking toggle appears in the original template. LFM2.5-Thinking is a separate checkpoint; its exact tokenizer and reasoning template need auditing before it is used. The selected original checkpoint does not have a verified explicit thinking mode. Treat Qwen thinking-off as a distinct native setting, not a parameter to pass blindly to LFM2.

Use the published vocabulary size and special IDs as configuration facts. Full tokenizer JSON (merge table, added tokens, normalization, special-token flags and postprocessor) remains uninspected. Neither equal vocabulary length nor matching example tokens establishes equal tokenizer behavior. The native tokenization of identical text should be measured in future calibration; don't use a common token-ID file across the two families. Pin raw template bytes, tokenizer files and generation configuration in the manifest alongside weights.

### 1H. License and publication

The full original 1.2B [Liquid LFM Open License v1.0](https://huggingface.co/LiquidAI/LFM2-1.2B/blob/main/LICENSE) was accessed as a primary text file. This is a technical interpretation, not legal advice or a blanket statement about all Liquid releases. Check the actual target revision and future derived model licenses before publication.

- Sections 1 and 2 define the work, derivative work, contributor, source/object form and the copyright permissions, including modification and redistribution. Converted weights are appropriately treated as modified derivative weights for compliance purposes.
- Section 3 gives a limited patent grant for contributor claims necessarily infringed by the work, subject to the license terms, with termination of the patent grant on relevant infringement litigation. It is not a freedom-to-operate opinion for an independent quantization invention.
- Section 4 permits source/object redistribution of modified and original works. It requires a copy of the license, prominent changed-file notices, retention of applicable attribution and other notices, and preservation of NOTICE attribution if provided. New terms on one's own modifications cannot override upstream obligations. The governing phrase is “copies of the Work or Derivative Works thereof”.
- Section 5 restricts commercial use above the defined threshold, which is USD 10 million annual revenue; read the Legal Entity/affiliate and revenue definitions, not just revenue of the individual repo. The operative language is “not exceeding the Threshold”. There is a specific research/noncommercial exception for qualified nonprofit organizations. The threshold definition and operative wording should be clarified with Liquid if exactly at the boundary; do not assume eligibility by dividing a business into subsidiaries.
- Section 6 covers contributions, §7 trademarks, §8 warranty disclaimer, §9 liability, §10 additional warranty/liability commitments, §11 automatic termination upon noncompliance and deletion/cessation obligations.

Research conversion and noncommercial scientific publication are within the apparent copyright grant. Distribution of derived binary checkpoints is permitted subject to compliance and applicable commercial restrictions. I found no benchmark-publication prohibition in this text. A published result should identify the base revision, modifications, license and reproducibility artifacts, avoid implying endorsement, and use the model name descriptively. This is not OSI-style unrestricted commercial licensing. No personal information form was needed to read the selected license. Not every family member's license has been inspected; do not apply this license by assumption to all successors or specialized partnerships.

### 1I. Cheapest remaining verification for item 1

Obtain binary headers and complete small metadata files at the two proposed immutable revisions, compare against §1D, and record commit + weight SHA + template hash. Obtain the original report PDF with all figures and appendices. Export the official catalog API and immutable release manifest for each dense text variant, not all gigabytes of data. Freeze the target only after these agree. A technical workaround to obtain the missing binary headers is provided in §5, which avoids running a model.

## 2. Low-bit LFM2 and neighboring hybrid architectures

### 2A. Direct evidence: Liquid's quantization-aware distillation (QAD)

Primary article text and aggregate figure inspected, but the training implementation and all deployment figure tabs were not read in full. The official [August 19, 2026 QAD release](https://www.liquid.ai/blog/qad) is the strongest direct lead found for trained low-bit LFM2.5. It is not a binary experiment. It adapts weights using simulated deployment quantization and a distillation objective from the original model, then uses ordinary GGUF Q4_0 deployment. The publisher reports five repeats over seven tasks: GPQA Diamond, MMLU-Pro, IFEval, IFBench, MultiIF, BFCL v4 and either GSM8K for the two smallest checkpoints or AIME25 for the two larger checkpoints. Do not transfer the resulting average to our ten-task suite.

| QAD parent | Reported QAD retention vs original | Fraction of PTQ loss recovered | Implied PTQ retention, calculated from the two previous columns |
|---|---:|---:|---:|
| 230M | 97.1% | 70.6% | 90.14% |
| 350M | 96.5% | 73.4% | 86.84% |
| 1.2B-Instruct | 97.4% | 65.5% | 92.46% |
| 2.6B | 96.6% | 48.4% | 93.41% |

Calculation: if recovery F=(R_QAD-R_PTQ)/(1-R_PTQ), then R_PTQ=1-(1-R_QAD)/(1-F). The small differences from using rounded chart values are expected. This is reconstruction from published aggregate numbers, not an independent benchmark. The lowest size is not monotonically worst, and the 350M parent has a substantially greater immediate PTQ gap than 1.2B. Architecture and training are confounded even across this family. QAD closes much of the gap at four bits; it does not establish that a one-bit feasible set has comparable approximation or recovery properties. No loss weights, full training data manifest or complete code was obtained. I will not claim the recipe is independently reproducible from this article.

The physical artifact evidence is unusually good. Publisher trees list both ordinary Q4_0 and QAD-Q4_0 at the same rounded file size:

| Official repository | F16/BF16 file | Q4_0 PTQ | QAD-Q4_0 | Q4_K_M | Q5_K_M | Approx QAD file bpw using F16/2 as weight-count proxy |
|---|---:|---:|---:|---:|---:|---:|
| [230M](https://huggingface.co/LiquidAI/LFM2.5-230M-GGUF/tree/main) | 462 MB | 149 MB | 149 MB | 153 MB | 172 MB | 5.16 |
| [350M](https://huggingface.co/LiquidAI/LFM2.5-350M-GGUF/tree/main) | 711 MB | 219 MB | 219 MB | 229 MB | 260 MB | 4.93 |
| [1.2B-Instruct](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/tree/main) | 2.34 GB | 696 MB | 696 MB | 731 MB | 843 MB | 4.76 |
| [2.6B](https://huggingface.co/LiquidAI/LFM2.5-2.6B-GGUF/tree/main) | 5.40 GB | 1.59 GB | 1.59 GB | 1.67 GB | 1.94 GB | 4.71 |

File bpw is not nominal tensor precision. The proxy assumes the F16 file contains only two bytes per unique parameter, approximately true for these tied dense models but not exact because of metadata and small higher-precision tensors. A Q4_0 block itself stores 32 four-bit codes and a 16-bit scale, hence 4.5 bpw. The above larger figures include metadata, unquantized tensors and any mixed types. They are not proof of the exact type composition. Read the GGUF directory, not just its filename.

**Important new primary artifact: full-precision QAD source weights.** The [QAD README](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/blob/main/qad/README.md) and [provenance.json](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/blob/main/qad/provenance.json) were read in full from their HF file views. The publisher confirms that `qad/model.safetensors` is FP32 after QAD, before actual packing. The provenance file specifies:

- FP32 source SHA256 `992954801538bcb9462f129df78b5ff961ee598148977bb8fbf401d1e35e13ec`.
- QAD GGUF revision `6767265158422fb8a19c62ceb45f16f05363615b`, GGUF SHA256 `bb741ebb106d543e9de114b843a3d3d73d51c74b5801e69da2abde821a0cb3e1`.
- llama.cpp revision `74ade52741203e5c8f81eaf06a96cb1cfe15f2a3`; conversion FP32 HF to F16 GGUF to Q4_0.
- September 22, 2026 validation: publisher reports that both packed tensor bytes and complete file hash were reproduced with matching metadata.

This is stronger than a marketing score because it specifies a falsifiable exact artifact reproduction. I did not independently re-create the file or read the binary header. The README explicitly warns against casting the source to BF16 before reproduction. The [350M QAD directory](https://huggingface.co/LiquidAI/LFM2.5-350M-GGUF/tree/main/qad) also lists the corresponding source checkpoint. These give controlled same-architecture weight-distribution comparisons that were previously unavailable to the project. They are not interchangeable with the original LFM2 teachers selected for transfer. A model tuned for four-bit rounding might become either easier or harder to compress to signs. Its performance in direct FP32 inference is not established by the Q4_0 score.

### 2B. Original Liquid quantized releases

Primary file listings read for the four linked original GGUF repositories. Binary tensor tables and independent score traces were not read. The following is a verified filename and rounded size inventory, not a verified per-tensor precision audit.

| Original parent | F16 | Q4_0 | Q4_K_M | Additional higher-precision preset (exact name pending) | Q5_K_M | Q6_K | Q8_0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| [350M](https://huggingface.co/LiquidAI/LFM2-350M-GGUF/tree/main) | 711 MB | 219 MB | 229 MB | 255 MB | 260 MB | 293 MB | 379 MB |
| [700M](https://huggingface.co/LiquidAI/LFM2-700M-GGUF/tree/main) | 1.49 GB | 446 MB | 469 MB | 514 MB | 538 MB | 612 MB | 792 MB |
| [1.2B](https://huggingface.co/LiquidAI/LFM2-1.2B-GGUF/tree/main) | 2.34 GB | 696 MB | 731 MB | 796 MB | 843 MB | 963 MB | 1.25 GB |
| [2.6B](https://huggingface.co/LiquidAI/LFM2-2.6B-GGUF/tree/main) | 5.14 GB | 1.48 GB | 1.56 GB | 1.67 GB | 1.83 GB | 2.11 GB | 2.73 GB |

The additional higher-precision variant column is deliberately not used for comparison until its exact naming and types are checked. The four listings do not supply verified IQ1/Q1_0/Q2/Q3 publisher releases for these exact original parents. Official MLX and ONNX variants also exist in the [model library](https://docs.liquid.ai/lfm/models/complete-library); the complete width-by-width catalog and quantized payloads were not recovered. Absence from the above four trees is not proof that no other publisher repository exists. Nominal Q4_0 is not four stored bits, and Q4_K_M is not a uniform four-bit model.

### 2C. Community builds below nominal four bits

The named file listings in this section were directly inspected, not the packed payloads. All rows are candidate PTQ artifacts rather than claimed trained binary conversions. For community builds the release does not establish the exact parent commit, complete quantizer command or a matched task-score dataset unless the card and metadata are separately checked. `i1` in mradermacher's repo naming is not evidence of 1-bit weights; these are importance-matrix builds. The Unsloth tree lists an importance matrix. I have not independently verified its calibration dataset or exact mixed-precision assignments. In this table every listed low-bit file is identified by its individual quant suffix. Sizes are decimal MB and file bpw is approximate using the unique count reconstructed from the original same-shape architecture or, when unknown, the F16 size proxy. This includes metadata. It is not a claim of exact tensor-only bits.

| Parent and converter (link to files) | File suffix | File MB | Approx file bpw |
|---|---|---:|---:|
| [DevQuasar / original 700M](https://huggingface.co/DevQuasar/LiquidAI.LFM2-700M-GGUF/tree/main) | Q2_K | 315 | 3.38 |
| [DevQuasar / original 700M](https://huggingface.co/DevQuasar/LiquidAI.LFM2-700M-GGUF/tree/main) | Q3_K_L | 410 | 4.40 |
| [DevQuasar / original 700M](https://huggingface.co/DevQuasar/LiquidAI.LFM2-700M-GGUF/tree/main) | Q3_K_M | 388 | 4.17 |
| [DevQuasar / original 700M](https://huggingface.co/DevQuasar/LiquidAI.LFM2-700M-GGUF/tree/main) | Q3_K_S | 361 | 3.88 |
| [DevQuasar / original 1.2B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-1.2B-GGUF/tree/main) | Q2_K | 483 | 3.30 |
| [DevQuasar / original 1.2B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-1.2B-GGUF/tree/main) | Q3_K_L | 635 | 4.34 |
| [DevQuasar / original 1.2B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-1.2B-GGUF/tree/main) | Q3_K_M | 600 | 4.10 |
| [DevQuasar / original 1.2B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-1.2B-GGUF/tree/main) | Q3_K_S | 558 | 3.81 |
| [DevQuasar / original 2.6B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-2.6B-GGUF/tree/main) | Q2_K | 984 | 3.06 |
| [DevQuasar / original 2.6B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-2.6B-GGUF/tree/main) | Q3_K_L | 1340 | 4.17 |
| [DevQuasar / original 2.6B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-2.6B-GGUF/tree/main) | Q3_K_M | 1260 | 3.92 |
| [DevQuasar / original 2.6B](https://huggingface.co/DevQuasar/LiquidAI.LFM2-2.6B-GGUF/tree/main) | Q3_K_S | 1160 | 3.61 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | Q2_K | 483 | 3.30 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | Q2_K_L | 483 | 3.30 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | Q3_K_M | 600 | 4.10 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | Q3_K_S | 558 | 3.81 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | UD-Q2_K_XL | 483 | 3.30 |
| [Unsloth / 2.5 1.2B Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF/tree/main) | UD-Q3_K_XL | 600 | 4.10 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ1_M | 327 | 2.24 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ1_S | 304 | 2.08 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ2_M | 434 | 2.97 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ2_S | 404 | 2.76 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ2_XS | 396 | 2.71 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ2_XXS | 365 | 2.50 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ3_M | 567 | 3.88 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ3_S | 558 | 3.81 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ3_XS | 538 | 3.68 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | IQ3_XXS | 491 | 3.36 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | Q2_K | 483 | 3.30 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | Q2_K_S | 461 | 3.15 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | Q3_K_L | 635 | 4.34 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | Q3_K_M | 600 | 4.10 |
| [mradermacher / 2.5 1.2B Thinking](https://huggingface.co/mradermacher/LFM2.5-1.2B-Thinking-i1-GGUF/tree/main) | Q3_K_S | 558 | 3.81 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ1_M | 732 | 2.17 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ1_S | 677 | 2.01 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ2_M | 981 | 2.91 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ2_S | 909 | 2.69 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ2_XS | 896 | 2.65 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ2_XXS | 822 | 2.44 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ3_M | 1280 | 3.79 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ3_S | 1270 | 3.76 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ3_XS | 1220 | 3.61 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | IQ3_XXS | 1120 | 3.32 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | Q2_K | 1090 | 3.23 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | Q2_K_S | 1040 | 3.08 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | Q3_K_L | 1450 | 4.30 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | Q3_K_M | 1370 | 4.06 |
| [mradermacher / 2.5 2.6B](https://huggingface.co/mradermacher/LFM2.5-2.6B-i1-GGUF/tree/main) | Q3_K_S | 1270 | 3.76 |

The original 350M community-tree path `DevQuasar/LiquidAI.LFM2-350M-GGUF` did not resolve. Further indexed candidates include [NANI-Nithin/LFM2.5-350M-RLCD-GGUF](https://huggingface.co/NANI-Nithin/LFM2.5-350M-RLCD-GGUF), [LFM2.5-2.6B-Base-i1](https://huggingface.co/mradermacher/LFM2.5-2.6B-Base-i1-GGUF), [LFM2-2.6B-Transcript-i1](https://huggingface.co/mradermacher/LFM2-2.6B-Transcript-i1-GGUF), [LFM2.5-1.2B-Instruction-following-i1](https://huggingface.co/mradermacher/LFM2.5-1.2B-Instruction-following-i1-GGUF) and [Luth-LFM2-700M-i1](https://huggingface.co/mradermacher/Luth-LFM2-700M-i1-GGUF). These are leads from index pages or incomplete card reads, not verified exact file inventories. They should not be merged with canonical parents. No quality measurement against the exact FP parent and suite was obtained for the rows in the table. Ranking these by assumed quality from size or downloads would not meet the brief.

**Which comparator is actually defensible?** For the selected original 350M and 1.2B, use official F16 and Q4_0, plus Q2_K and Q3_K_S/M from the original 1.2B DevQuasar tree as lower-bit engineering comparators after verifying parent identity. For original 700M and 2.6B, the corresponding DevQuasar PTQ series is available. For LFM2.5 230M, 350M, 1.2B-Instruct and 2.6B, the official QAD-Q4_0 has the best directly reported evidence among the located trained artifacts; it is not the smallest artifact or necessarily the best absolute score among all precisions. For 1.2B-Thinking, the IQ1/2/3 series offers a size ladder only. The 2.6B IQ1_S at 677 MB is roughly 2.01 stored bpw on a 2.70B parent, much greater than 1.125. The 1.2B Thinking IQ1_S is roughly 2.08 file bpw, also far outside the codec. Neither should be advertised as our comparator in the sense of equal bits, equal parent and equal tasks. The direct comparator at our format remains to be created or discovered. An exhaustive cross-hub search and complete GGUF metadata extraction are still outstanding; see §5.

### 2D. The name of a tensor type is not its storage cost

Read in part from actual [ggml-common.h](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/ggml/src/ggml-common.h) declarations. The relevant cost accounting uses payload structure sizes, not the GGUF marketing name. For types with blocks of 256, table values include their scales and other in-block metadata.

| Tensor type | Payload bytes per block | Block weights | Tensor bpw | Strict target? |
|---|---:|---:|---:|---|
| Q1_0 | 18 | 128 | 1.125 | Yes for a complete contiguous 128-weight sign group |
| IQ1_S | 50 | 256 | 1.5625 | No |
| IQ1_M | 56 | 256 | 1.75 | No |
| IQ2_XXS | 66 | 256 | 2.0625 | No |
| IQ2_XS | 74 | 256 | 2.3125 | No |
| IQ2_S | 82 | 256 | 2.5625 | No |
| Q2_K | 84 | 256 | 2.625 | No |
| IQ3_XXS | 98 | 256 | 3.0625 | No |
| IQ3_S | 110 | 256 | 3.4375 | No |
| Q3_K | 110 | 256 | 3.4375 | No |
| Q4_0 | 18 | 32 | 4.5 | No |

IQ codebooks and extra side information do not in general decode as one uniform magnitude per group of 128. The various `_M`, `_L`, `_S`, `UD` presets can use different tensor types in a single file. The exact accounting formula is `sum(tensor.n_bytes)*8/sum(tensor.n_elements)` with actual stored unique tensors; report whole-file bits separately. Verify padding, tensor offsets, tied head duplication, and alignment. At this stage the public tree sizes are only the file cost evidence. No claim that every discovered low-bit file contains its stated quantizer uniformly.

### 2E. Runtime inspection: why Q1_0 is necessary but not sufficient

Primary code read in part as documented above. In llama.cpp the [Q1_0 addition](https://github.com/ggml-org/llama.cpp/pull/21273) and `block_q1_0` structure establish the dense codec, with one half-precision magnitude and sixteen bytes of sign codes. LFM2 dense matmuls already use ggml's standard graph; architecture support and type support can therefore meet at those matmuls if the backend dispatch supports them. However, the [quantizer](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/llama-quant.cpp) explicitly excludes short convolution and SSM convolution weight names from ordinary quantization. Small vectors are also handled separately. The [LFM graph](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/src/models/lfm-base.cpp) uses `ggml_ssm_conv` for the depthwise operation. The [conversion code](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/conversion/lfm2.py) squeezes the singleton kernel dimension. Hence there are two independent barriers: a row of length three fails a 128-element block contract and the convolution kernel is not an ordinary binary matmul consumer. Even for dense weights, a default mixed-type quantizer can retain higher-precision embeddings or output; inspect exported types, not the requested command-line name.

| Runtime | Verified relevant support | What is missing for strict all-weight LFM2 |
|---|---|---|
| llama.cpp | LFM2 model graph and Q1_0 storage type in current source; source-based evidence for both components | Pin one compatible revision, verify dense input/head lookup and matmul on CPU/Metal, add short-kernel packed loader or a dedicated implementation, decide norm representation and prevent higher-precision tensor overrides. No execution was performed. |
| Transformers / PyTorch | Released LFM2 model implementation, ordinary dense and convolution operators | A strict serializer and a loader which reconstructs exact signs times FP16 scales. Reference inference can decode to FP32/BF16 temporaries, which does not add trainable stored parameters. Faster packed kernels are separate engineering work. |
| MLX / MLX-LM | LFM2 architecture support; official MLX-family artifacts; Python implementation not completely retrieved | Exact support for group-128 symmetric sign packing, embedding lookup, all matrix and conv consumers must be checked. Standard affine quantized-linear APIs cannot simply be assumed identical. PrismML's [Bonsai demo](https://github.com/PrismML-Eng/Bonsai-demo) is a relevant runtime lead, not proof of LFM2 support. |
| Other runtimes (vLLM, ONNX, mobile engines) | General LFM2 and/or low-bit deployment mentioned in official cards | No inspected end-to-end strict-binary LFM2 backend. A reference unpack-on-load implementation is possible independently of whether a native fused binary kernel exists. |

There is a practical distinction between storing weights in one bit and performing every arithmetic operation in one bit. Our current format restricts weight storage, not activations or accumulators. Therefore an exact dequantizing reference loader is a legitimate first validation path, provided it never keeps a separate learned high-precision master checkpoint in the deployed model and all decoded values are determined by the packed signs/scales. It is not a claim of accelerated inference. Q1_0 support in a runtime that runs Qwen does not prove the depthwise kernel is supported.

### 2F. A close empirical precedent: Bi-Mamba

Read in part from [primary paper](https://arxiv.org/html/2411.11843), including the method and relevant experimental tables; [repository](https://github.com/Tangshengku/Bi-Mamba) tree and README inspected, not the full training implementation. This is adjacent evidence, not a verified strict binary LFM2 experiment. Mamba's input projection, depthwise convolution, multiplicative gating, state-space recurrence and output projection are closer to LFM2 than a pure transformer is, but its selective recurrence is different. Bi-Mamba trains a binarized architecture using teacher distillation and an affine, flexible binary linear representation. The learned per-column affine terms are not the project's symmetric group-128 representation. The paper binarizes input and output projections, not every weight. In particular, the depthwise convolution and small state-space parameters are not evidence of successful 1-bit conversion.

| Parameter scale | FP average downstream accuracy | Binary input projection only | Binary both projections | Both / FP, computed |
|---|---:|---:|---:|---:|
| 780M | 52.5 | 45.5 | 45.3 | 86.29% |
| 1.3B | 55.8 | 49.6 | 48.4 | 86.74% |
| 2.7B | 59.6 | 53.1 | 50.6 | 84.90% |

These values are from the paper's reported averages, not our ten-task suite. Quantizing the output projection in addition to the input projection drops another 0.2, 1.2 and 2.5 absolute points respectively. That is not a ranking of intrinsic sensitivity because input-only was not contrasted here with output-only, and the models were trained under different constraints. The paper reports a 105B-token distillation regime using a Llama2-7B teacher. The main value of this study is existence of a workable learned binary projection in a gated, recurrent hybrid, including sub-3B scales. It does not prove post-training conversion of the original parent, unchanged Qwen recipe transfer, or binary depthwise taps. If the claimed 95.2% binary coverage is interpreted as fraction of all unique weights, a remaining 4.8% at FP16 alone raises the floor to 1.72 bpw even before affine scales, not 1.125. Verify the author's denominator and artifact before using that figure as an exact model storage number.

Other source-table comparisons at 1.3B include GPTQ 3-bit 47.8, SqueezeLLM 3-bit 53.9, GPTQ 2-bit 35.3, SqueezeLLM 2-bit 46.5, AQLM nominal 1.92-bit 39.6, BiLLM 36.2 and OneBit 46.8. Bi-Mamba's 48.4 therefore compares favorably with some extreme-low-bit baselines, but not all three-bit methods. Without matched total stored bits and an exact parent it is not an equal-codec result. Perplexity for three listed corpora at 1.3B changes from (10.4,17.7,14.8) to (11.7,29.9,12.9); the final corpus improves despite the downstream mean dropping. That is a caution against relying on one perplexity number as the transfer scoreboard. All data in this subsection should be rechecked against the full paper and appendix before being treated as fully audited results under the brief's reading standard.

### 2G. Adjacent research not yet at the required reading standard

The following are partial-source leads rather than conclusions resting on uninspected material. They merit follow-up because they isolate the operators the project cares about.

| Lead | Why relevant | What must be checked |
|---|---|---|
| [Quamba2, ICML 2025](https://proceedings.mlr.press/v267/chiang25a.html), [code](https://github.com/enyac-group/Quamba) | Quantization of Mamba-family state-space language models, including W4 regimes | Exact state, convolution, gate and projection types, per-layer bit choices and full task tables. No one-bit conclusion. |
| [BD-Net](https://arxiv.org/html/2511.17633) | Binary depthwise convolution in vision | Full primary methods, which operators remain real-valued, depthwise versus pointwise ablations, accuracy and parameter cost. |
| [Binarizing MobileNet](https://mlanthology.org/cvpr/2020/phan2020cvpr-binarizing/) | Depthwise-separable binary vision models; channel redundancy and kernel size are especially relevant | Original paper, implementation, control architecture and exact first/last layer exceptions. Vision classification is not autoregressive language modeling. |
| [ParetoQ](https://arxiv.org/html/2502.02631) | Same research method across mobile-scale transformers and Llama families | Model-specific schedule and exceptions, actual whole-model costs. |
| [BinaryLLM](https://arxiv.org/html/2508.06974) | Converted pretrained small transformer families and a parent previously distilled from a larger model | Full appendix and code; see §3A for checked main-table evidence. |

Searches included `LFM2 binary quantization`, `LFM2 Q1_0 Bonsai PrismML`, `LFM2 IQ1_S IQ1_M GGUF`, `LFM2 quantization-aware training distillation ternary BitNet`, `LFM2.5 IQ2 Q2_K`, `binary Mamba language model depthwise convolution`, `binary gated convolution language model`, `binary depthwise separable convolution network`, and architecture-specific searches on Hugging Face and GitHub. These surfaced the community builds, official QAD release and Bi-Mamba, rather than a verified same-parent strict 1.125-bit LFM2 checkpoint. No verified public PrismML LFM2 announcement or checkpoint was obtained. This is a bounded search result, not a claim of universal absence or of what PrismML plans privately. Additional full hub pagination, author repositories, discussions, speech literature and exact payload inspection remain necessary.

## 3. Transferring the formula: mathematical and experimental analysis

### 3A. Cross-family evidence: what actually transfers

This subsection is based on partial primary-paper readings. These studies are candidate precedents, not certified complete source audits. Their task results cannot be used as estimates of strict-binary LFM2 performance. The proposed experimental design and mathematical arguments later in this section do not depend on those results.

| Study | Cross-family comparison | What does not establish our claim |
|---|---|---|
| [BinaryLLM, Rethinking 1-bit Optimization, v2](https://arxiv.org/html/2508.06974v2), §3, §4, Table 2 and Appendix A | Progressive pretrained conversion with consistent forward/backward interpolation, binary-aware initialization and two scale terms that are multiplied together. SmolLM-135M, Llama 3.2-1B and Llama3-3B parents; Pythia-70M ablations. The paper specifically describes the 1B parent as pruned/distilled from a larger model. | Common method, not a frozen identical recipe across unrelated architectures. Embedding and output excluded from the reported bpw; scales are not verified group-128. Training exposures differ. Task suite consists of seven older zero-shot classification tasks, not our reasoning, coding and instruction suite. |
| [ParetoQ](https://arxiv.org/html/2502.02631), main experiments and Appendix A.1 | Family of precision-dependent QAT methods tested on small MobileLLM variants and Llama 3 models; provides relevant controls across architecture size and quantization levels. | Not a single unchanged codec-inclusive recipe. Exact treatment of embeddings, norms, task settings, quantizer and training stages must be checked against code and appendix. |
| [OneBit](https://arxiv.org/html/2402.11295), method and main comparison | Learned sign matrices, vector scaling and normalization, investigated on several pretrained LLMs. | Additional representation and scale parameters; does not by itself validate our equal-group binary constraint or gated convolution. |
| [Bi-Mamba](https://arxiv.org/html/2411.11843) | Binary projection training at 780M, 1.3B and 2.7B in a hybrid recurrent model; see §2F. | Does not hold the Qwen recipe fixed or compress all tensors. Teacher and target architecture differ. |
| [Liquid QAD](https://www.liquid.ai/blog/qad) | Common public method and fixed Q4_0 deployment across four LFM2.5 sizes. | One architecture family, four bits, unpublished complete training recipe. |

The strongest directly relevant *methodological* precedent among the inspected BinaryLLM results is the fact that a pretrained small model can be progressively converted, including a previously distilled parent. The checked table gives the SmolLM-135M average as 49.1 FP versus 42.3 binary (86.15% ratio), and the Llama3-3B average as 65.0 FP versus 57.0 binary (87.69%). The paper uses 20B tokens for its smallest example and discloses AdamW, sequence length 2048, batch size 128, cosine learning-rate decay from 1e-4 to 2e-6 and weight decay 0.1. These scores do not validate a fixed schedule or storage-compliant transfer; the embeddings are excluded from the bit accounting. The main comparison is not a factorial test of training history. Full code and appendix inspection is still required. I have found no fully audited study in this search demonstrating the precise claim: a strict sign plus FP16 group-128 recipe, frozen on a small plain transformer, transferred unchanged to a small gated-conv language model. That is a research gap in the audited corpus, not proof of novelty.

The key distinction is between (i) portability of a mathematical optimizer, (ii) portability of a model-specific fitting procedure and (iii) portability of the outcome. Any trainable network can in principle be fitted with a sign-constrained parameterization. That alone proves neither a feasible solution of the desired quality nor convergence to it. Defining an architecture-specific layer weighting rule after LFM2 failure is new recipe tuning. Defining a universal rule using measured tensor shapes and sensitivity before any LFM2 outcomes are available is a legitimate alternative claim, but different from only changing shape-dependent settings.

### 3B. Training history and the strength of the teacher

Partial-source leads: [Scaling Laws for Precision](https://arxiv.org/html/2411.04330), [Training Dynamics](https://arxiv.org/html/2510.06213) and [Low-Bit Quantization Favors Undertrained LLMs](https://aclanthology.org/2025.acl-long.1555/). The first two primary HTML method and result sections were inspected selectively. The third was inspected only at index/abstract level and supports no numerical conclusion here. No source in this group was completely audited with code and all appendices. I therefore do not assign a quantitative LFM2 penalty or advantage from these studies. The hypothesis to resolve is more specific than whether longer training is good or bad: for a fixed sign-codec, how does compression error in task-relevant functions change along a pretraining trajectory with fixed architecture, data distribution and optimizer?

There are several competing mechanisms:

1. Longer training can encode more learned distinctions in the same number of parameters. If those distinctions require magnitude resolution not available in a binary shell, loss can increase. This is a capacity hypothesis, not a theorem that more tokens make every model harder to quantize.
2. Longer training can also reduce error, produce more redundant solutions, move decision margins farther from zero, and allow information to be encoded in signs and activation patterns. In that case the same weight error can cause less functional damage.
3. Optimization trajectory matters. Two equal-loss checkpoints may have very different curvature, outliers, signs, activation covariance and distance to the binary feasible set. The controlled WSD/cosine and learning-rate experiments in the Training Dynamics paper are worth inspecting in full precisely because they attempt to separate training settings from loss. Their partial results at 70M/160M and nonbinary precision cannot establish a 1-bit LFM2 result.
4. Distillation can provide soft targets and structured information about alternatives that makes the student's responses more predictable. It can also pack a larger teacher's behavior into a smaller student. Either smoother targets or less unused capacity may dominate after the second distillation into binary weights. The words "already distilled" alone do not determine the direction of the effect.
5. The larger original teacher of LFM2 is not a verified accessible checkpoint. Distilling from a modern LFM2.5 or LFM3 teacher is not replication of original training. It may improve final task scores but could mask a loss of the exact parent function, changing the scientific question.

The selected target's 11.47% embedding share versus the check's 18.93% is one structural confound even before pretraining. The absolute number of unique sign bits is smaller than Qwen's. Better teacher scores can yield a smaller ratio for the same absolute score degradation; worse baseline scores can yield a larger ratio. Separate initial weight approximation, post-training behavior imitation, ground-truth task accuracy and calibration, rather than using retention as the only causal outcome.

**A useful natural control available now in public checkpoints:** original LFM2 versus LFM2.5 at 350M or 1.2B (same dimensions and operator sequence), followed by original LFM2.5 versus its published FP32 QAD source. The second pair is particularly interesting because the QAD change is a known quantization adaptation. Neither pair by itself randomizes token count, post-training data or optimizer. Compare their raw and normalized weight distributions, groupwise mean-absolute scale, sign agreement, relative reconstruction error and depthwise filter shape distributions without training a model. A follow-up with matched checkpoint training histories is needed for causal inference. The release artifacts are sufficient to formulate this control but not to claim its result. No such weight comparison was run in this assignment.

### 3C. Mathematics of the gated short convolution

The operator equation in §1C is reconstructed from the primary Transformers and llama.cpp implementation. Everything derived below is my mathematical analysis, not a result claimed by a cited quantization paper. Assume bias-free projections, the stated channelwise depthwise filter and exact arithmetic. No norm or nonlinearity is inserted between B and X, the depthwise convolution and C, or the output projection. These conditions matter for the symmetry group. Finite precision implementation can break mathematically exact equality at rounding level.

Write the channel-i contribution as:

```
y_t = sum_i o_i c_i(t) sum_l k_i,l b_i(t-l) x_i(t-l)
```

where o_i is the i-th column of W_out; b_i, c_i, x_i are scalar linear forms of the normalized input. For each channel select four arbitrary nonzero real numbers a_i, b'_i, c'_i, d_i. Transform the corresponding B row, X row, C row, kernel and output column as:

```
B'_i = a_i B_i
X'_i = b'_i X_i
C'_i = c'_i C_i
k'_i,l = d_i k_i,l
O'_i = O_i / (a_i b'_i c'_i d_i)
```

Every term in the output remains exactly unchanged. This is a four-dimensional continuous scaling family for each channel, including sign changes. The individual transformations may be folded into the stored projection and kernel weights; no learned scales beyond the already-existing weights need be deployed. In practice the product of many very large or small factors can cause overflow or FP16-scale underflow, so constrain the numerical range during search. There are additional exact generic symmetries:

- A common arbitrary channel permutation across B, X, C, kernel and output columns.
- Independent swap of the B and X linear rows in any channel, since their pointwise product commutes. This is not a swap of the C branch, which is at a different token position for nonzero lags.
- Internal layer input normalization gain can be folded into all consumers of that normalized vector. If a gain coordinate is changed by a nonzero factor, inversely rescale the corresponding columns of every input projection consuming that gain. Unlike changing the normalized activation itself, this is exact even at fixed epsilon.
- Linear dependencies, identical channels or degenerate zero filters may admit additional accidental transformations. They are not structural symmetries of a generic checkpoint. I do not claim an exhaustive classification of all accidental checkpoint-specific equivalences.

**Why arbitrary rotations are not an exact general symmetry:** suppose we want to transform two independent feature vectors b and x so that their coordinatewise product transforms linearly for every possible pair. Write `(A b)_i (D x)_i = sum_j E_ij b_j x_j`. Expanding gives coefficients `A_ij D_ik = 0` for every j != k. If A and D are invertible, each row must have a single nonzero coordinate, and both use the same coordinate in that row. The resulting invertible transformations are monomial matrices with a common permutation. The third gate and diagonal convolution impose analogous restrictions. This is a sufficient structural argument on independently variable feature vectors; in a particular network b and x are both functions of the same input, so exceptional dependencies could expand the stabilizer. Dense rotations in the gating space are therefore not generically function-preserving, even though rotations are useful in ordinary linear networks and in some attention subspaces. Nor may time lags be arbitrarily permuted: that would change the causal response. Rescaling a channel's depthwise filter does not change ratios among its three tap magnitudes. Those ratios are invariants of this generic scaling family.

**Quantization sensitivity:** set `u=Bz * Xz`, `v=K*u`, `s=Cz*v`. Under small weight perturbations and fixed z, let e_B=deltaB z, e_X=deltaX z and e_C=deltaC z. To first order:

```
delta_u = e_B * Xz + Bz * e_X
delta_v = deltaK*u + K*delta_u
delta_s = e_C*v + Cz*delta_v
delta_y = deltaO*s + O*delta_s
```

For a single lag term, if all factors are nonzero, the relative error is approximately the sum of the five relative errors (B, X, C, kernel, O). Exactly, the product of perturbed factors equals the original product times the product of their `1+relative_error` factors; higher-order cross terms need not be small at one bit. Across channels and lags there may be cancellation, so no uniform bound on *relative output error* follows from a bound on each relative weight error. For example, two equal and opposite lag terms may produce zero output before quantization but nonzero output after. Errors in B and X are not independent merely because their weights are separate: both see the same input, and a common scale balancing step can correlate their perturbations. Conversely, paired errors can compensate. For squared output error the first-order expectation includes every covariance between the five terms, not just their individual variances. Independent tensor reconstruction can discard useful cancellation.

This suggests a measurement that differs from Qwen's ordinary attention diagnostics without changing the primary training recipe: record each gate's preactivation RMS, sign agreement, outlier tail, product RMS, conditional error by activation magnitude, lag-wise kernel response and the error after the output projection. Preserve same-example and same-token pairing. Record local reconstructed output against FP and complete downstream effect separately. The parameter count of the kernel is tiny, but the product and convolution create a high-leverage operation. That is a reason to measure its sensitivity, not a prediction that it is the first thing to break. Our derivation does not imply that LFM2 is inherently less quantizable than an attention network. Attention is also a multiplicative, nonlinear operation with potentially large amplification.

### 3D. Exact group approximation and the small-kernel problem

For a given vector w of 128 real weights and unrestricted scale s >= 0, minimizing Euclidean distance over sign vector q gives q_j=sign(w_j) and s=(sum |w_j|)/128. This follows from expanding squared error and maximizing q dot w before minimizing the quadratic in s. The residual is `||w||^2 - (sum |w|)^2/128`. Actual FP16 rounding of s adds `128*(s_FP16-s)^2` to this objective, assuming no sign changes and finite representable s. This is a useful implementation unit test.

For iid centered Gaussian weights, the large-group normalized squared reconstruction error tends to `1 - 2/pi = 0.36338`, independent of variance. This is an asymptotic Euclidean approximation result, not an expected benchmark loss. Actual groups of 128 fluctuate, and trained weight distributions are not necessarily iid Gaussian. If every magnitude is equal, the residual is zero before FP16 scale rounding. High variance in magnitudes creates greater residual even if signs are accurately retained.

For a row acting on input covariance H = E[xx^T], the actual linear reconstruction error is `(w-sq)^T H (w-sq)`. For fixed signs and q^T H q > 0, the minimizing signed scale is `(q^T H w)/(q^T H q)`; a nonnegative-scale convention can flip q globally or clip a negative candidate to zero. With singular H, multiple different weight vectors may implement the same map on the observed inputs. Sign(w) is not generally optimal for a correlated H. The grouped multirow case adds cross-group terms, so independent group fitting is not globally optimal if covariance couples groups. None of these derivations require a specific architecture. This is where a universal data-aware method could be better than a simple rowwise magnitude objective. It is not evidence of any observed score improvement.

For the LFM2 kernel, there are three taps per channel. Suppose row-major grouping couples all three magnitudes of a channel into the same 128-weight group. Within that group its possible three-tap vectors have equal absolute magnitudes, up to sign. The exact symmetries of §3C permit multiplication by a scalar, but cannot restore an arbitrary ratio such as 1:2:4. If the channels are packed tap-major, each 128-channel block can have independent scales for lag 0, 1 and 2, so the magnitudes of the three taps need not be equal. However, all channels sharing those three groups then have the same absolute tap ratios, with independent signs. Per-channel scaling can absorb different overall filter norms, but not different normalized filter shapes. Tap-major grouping is thus a better *representation candidate* for certain distributions, not an exact generic solution. It cannot be selected after seeing the test score and still be called a shape-only transfer. Both row-major and tap-major should be defined before experiments, and any additional learned permutation must be an allowed conversion rule, not silently stored side information.

A group sign pattern also cannot express zero except by setting the entire group scale to zero. Some learned kernels may be near zero at a particular lag. If the normalized tap shape has a very small component, forcing it nonzero can inject a spurious temporal dependency. The scale error on a lag with very small teacher weights can be large relative to that lag, while its absolute effect may be small or large depending on the associated gated input. This is a mathematically identified failure mode, not an observed LFM2 pathology.

### 3E. Comparison with exact transformer changes of variables

The following is a generic structural symmetry analysis, not a claim that a published paper implements every change. Use the same normalizations and dimensions as §1C. Any proposed folded change should be verified in exact arithmetic and in FP parity before quantization, with tied embeddings and cache handling included.

| Substructure | Generic exact folded changes | Not generally exact |
|---|---|---|
| SwiGLU, both Qwen and LFM2 | Common intermediate permutation of gate/up rows and corresponding down columns; arbitrary nonzero per-channel scaling of the linear up branch with inverse scaling of down columns. | Arbitrary scaling of the SiLU input row compensated by its output: SiLU is not homogeneous. Arbitrary intermediate rotation does not commute with SiLU and elementwise product. |
| LFM2 short convolution | Common channel permutation; B/X independent swap per channel; four nonzero diagonal scalings with inverse product in output; normalization gain folding. | General rotations across gated channels; lag permutations; independent rescaling of taps while leaving all other factors invariant. |
| Attention value branch | Per-KV-head invertible basis change in the value vector, with inverse in every output-projection block that consumes that KV head. Attention weights are scalar across features, so the transform commutes with the weighted value sum. | Independent value transforms for query heads sharing a KV head without compatible adjustment; arbitrary feature transforms if an additional value normalization intervenes. |
| GQA head ordering | Common KV-head permutation and permutation of its associated query group; within each KV group, permutation of query heads and corresponding output columns. | Arbitrary reassignment of queries to KV heads without preserving their attention function. |
| Query/key feature basis | In the absence of normalization and RoPE, `Q -> A Q`, `K -> A^{-T}K` preserves logits. With RoPE and Q/K RMSNorm, use only changes satisfying both normalization equivariance and commutation/intertwining with the relative rotations. Reciprocal global scalar gains on the *post-normalization* Q and K gains preserve dot products if applied to all paired heads. | Arbitrary nonorthogonal inverse transforms before RMSNorm; arbitrary rotations mixing different RoPE frequencies; arbitrary scaling of pre-norm Q/K with epsilon held fixed. |
| Residual stream and embedding | Common global signed permutation (with all corresponding tensor rows/columns, norm gains and tied embedding transformed consistently). | Generic arbitrary orthogonal residual rotation if learned diagonal RMSNorm gains, tied embedding/head and all consumers are not simultaneously handled. |

For the residual signed-permutation proof, let P be orthogonal and monomial, so RMS is invariant, and map h to Ph. If gamma is the learned gain, permuting its coordinates by the unsigned part of P gives `D_gamma' P = P D_gamma`. Transform every residual-input projection W by W P^T and every residual-output projection U by P U. The residual identity map and addition commute with P. For the tied vocabulary embedding E with token rows, transform E to E P^T, so lookup yields Ph and output logits `(E P^T)(P h)=E h`. This establishes a generic exact symmetry including the tied output. Arbitrary orthogonal residual rotations also preserve RMS denominator but transform a diagonal gain into a generally nondiagonal operator. They can sometimes be absorbed into adjacent dense projections, yet the final norm directly followed by a tied output restricts the simple construction. No unconditional full orthogonal symmetry should be assumed. Degenerate identical gains can enlarge the allowable group.

For Q/K RoPE, the exact relative dot product is `q_t^T R_t^T R_s k_s`. If both bases are transformed by a common orthogonal U after normalization, preservation for every position requires `U^T R_t^T R_s U=R_t^T R_s`. Within a single two-dimensional frequency plane ordinary planar rotations commute with the RoPE rotations; mixing unequal frequencies generically fails. Implementing U by changing the *pre-norm projections* additionally requires commutation with diagonal Q/K gains, or a valid new diagonal gain and compatible transformation. A learned unequal pair of gamma entries generally removes the arbitrary planar rotation from that simple folded implementation. Independent scalar reciprocal post-norm gains are much simpler, because they cancel in the logits without altering RoPE. The epsilon in RMS normalization prevents an otherwise often-invoked exact invariance under arbitrary pre-norm scaling: `RMSNorm(a x)=a x/sqrt(a^2 mean(x^2)+eps)*gamma`, not identically RMSNorm(x) for all x unless special conditions hold. This is important when proposing scale balancing at binary precision.

The common SwiGLU and residual transformations cover a majority of both models' learned weights. The convolution symmetry family adds substantial balancing freedom but not arbitrary linear rotations. That is a reason to develop a structural framework rather than assuming every rotation-based Qwen quantization method can be copied unchanged. A recipe can specify universally valid graph-local equivalences by operator type, but if it uses LFM2-specific new equations or objective weights, its claim must be described as architecture-aware generalization, not merely shape substitution.

### 3F. A fair measurement when no exact-format LFM2 comparator exists

**Primary outcome:** use the original ten specified benchmark versions, equal task weights, identical scoring implementation and semantic prompts. Record the exact benchmark split, question IDs, dataset revision, shot examples and their order, max generation tokens and decoding policy. Use each model's native tokenizer and chat/tool template, same within each FP/binary pair. Qwen thinking off, LFM2 ordinary non-thinking instruction checkpoint; no reasoning-only substitute. The same raw natural-language problem may yield different token counts; forcing identical token IDs is wrong. The equal-harness choice can differ from original Liquid and PrismML papers. Preserve a separate published-protocol reproduction track if the exact historical settings are recovered.

| Task | Main comparability danger | Required lock |
|---|---|---|
| MATH-500, GSM8K | Shot count, answer extraction, partial solution versus final answer, reasoning length | Dataset revisions, shots, exact-answer rules and generation ceiling |
| BFCL v3 | Native tool schema, tool message syntax, AST/execution scorer, subset weighting | Task version, same canonical tools and calls, native serialization, no hidden repair agent |
| MMLU-Redux, GPQA Diamond, MuSR | Multiple-choice ordering, number of shots, generation vs likelihood scoring | Same item and permutation IDs, same score type, cluster repeated permutations |
| MBPP+, HumanEval+ | Base versus plus tests, pass@k, execution environment | EvalPlus commit, deterministic output extraction, pass@1 and isolated execution |
| IFEval, IFBench | Strict/loose metrics and aggregate choice, evaluator version | One prespecified aggregate and scorer; do not substitute instruction accuracy for prompt accuracy |

No absolute FP LFM2 score from the different official suite can be used as the denominator in our primary experiment. Obtain matched raw scores from the pinned parent. Define `R_A = mean_j(B_Aj)/mean_j(F_Aj)` where j is task, and `D=100*(R_LFM-R_Qwen)` in percentage points. The mean is taken before division, exactly as in the project. This is not the mean of ten per-task ratios. Publish the ten individual scores as well, with absolute differences and task-specific retention when denominator nonzero. Chance-adjusted accuracy, per-token KL, teacher/student agreement, next-token loss and calibration are diagnostic metrics, not replacements for the official scoreboard. A model that has a weak full-precision score on a task may appear to retain that score at chance. A ratio alone will not detect loss of the same functions if the teacher distribution changes.

Reference lines:

1. Pinned FP teacher, matched suite and settings, exactly 100% by definition.
2. Deterministic strict group-128 round-to-sign baseline, no learned correction, including all weights according to the frozen codec rule. This is the initial LFM2 baseline, not a surrogate for Bonsai's trained result.
3. Frozen converted model from the final Qwen-proven recipe, no retuning based on LFM2 outcome. This is the primary transfer test.
4. Separate Q4_0/Q2_K/other published checkpoints at their actual stored bits, if parent match established; separate official QAD comparison on its own LFM2.5 teacher. Never blend the denominators or credit mixed precision as a strict result.
5. Optional later best-effort LFM2-specific recipe, explicitly named as such. Its success can distinguish generality failure from an impossible format, but it cannot rescue the original frozen-recipe claim.

**Uncertainty and sample size:** the target is an equivalence test, not a test that D differs significantly from zero. Prespecify margin 5 percentage points. Use two one-sided tests at alpha 0.05, which corresponds to a 90% confidence interval entirely contained within (-5,+5); a 95% interval is a stronger reporting convention. If the interval overlaps a margin, the evidence is inconclusive even when the point estimate is within five points. If a confidence interval lies outside the margin, the transfer claim fails under this definition. This is an inferential choice proposed here, not an already approved project rule.

For each architecture a, denote the mean task scores as b_a and f_a on 0-to-1 scale. The delta-method first-order perturbation is `dR_a = db_a/f_a - (b_a/f_a^2) df_a`. Thus the variance of the retention difference includes both covariance between student and teacher scores and covariance across the same questions used by the two architectures. Assuming all four means independent is generally wrong. A stratified paired bootstrap over question IDs within each task, jointly resampling the four score vectors, retains this covariance and respects equal task weights. Treat variations of the same question as one cluster. For code benchmarks use the problem as the cluster, not each unit test. For IFEval, use the prompt as the cluster if multiple instructions share it. Resample independent training seeds separately, and include decoding seeds as nested repeated measurements if sampling is used. A deterministic teacher run need not be artificially randomized. Do not count stochastic completions of a single question as independent new questions.

An illustrative sample-size calculation: suppose we had independent equally weighted questions with a linearized paired residual SD of 1.0 in ratio units, and true D=0. Under a normal approximation, for 80% power of equivalence at a 5-point margin the two-sided inclusion probability is approximately `P(|Z| < margin*sqrt(n)/SD - 1.645)=0.8`; solve using z_0.9=1.282 to get n about (2.927/0.05)^2 = 3427 independent questions. For SD 1.5, about 7711. For a 95% interval half-width of 2.5 points at SD 1.0, n about (1.96/0.025)^2 = 6147. These are illustrative notional equal-weight effective sample sizes, not requirements for the actual suite. Unequal task sizes, correlations and seed variance can raise or lower them. The original ten datasets have fixed lengths, so collect all eligible questions and calculate the achievable stratified CI. If statistical equivalence is not established, report that fact and prespecify an independent matched extension rather than duplicate prompts. Three independent training seeds are a proposed floor for engineering replication, five or more for a stronger scientific comparison, with additional seeds guided by observed seed variance. A fixed number of seeds cannot guarantee equivalence; more seeds do not remove finite test-item uncertainty. No evaluation was performed to estimate SD or actual confidence intervals.

### 3G. Diagnosing transfer failure without moving the goalposts

A frozen-recipe test and a causal study are different experiments. We can run the former without proving the cause of failure. The latter requires deliberate controls. The following is an experimental design proposal, not an executed experiment.

| Question | Compare | Hold fixed | What can be inferred |
|---|---|---|---|
| Engineering validity | FP and reference unpacked binary on 350M; independent runtime parity later | Weights, dtype/accumulator conventions, prompt tokens, caches | Format/loader error versus actual representation error. A successful loader does not prove retention. |
| Predictive transfer | Qwen3-1.7B and original LFM2-1.2B under frozen recipe | Codec, deterministic shape rules, token-source policy, loss definition, schedule formula, optimizer, selection rule, eval | Whether that recipe's relative performance generalizes to this exact new checkpoint. Not pure architecture causality. |
| Architecture vs scale | Matched-size hybrid and plain transformer parents trained from scratch under same corpus/tokenizer/objectives; bracket 350M, 700M, 1.2B, 2.6B | Data order, training tokens, optimizer and seed families, target dense bit budget, post-training protocol | Difference attributable to controlled architectural intervention, conditional on the matched training design. Exact width and FLOPs matching may be impossible; define both parameter-matched and compute-matched controls. |
| Training history | Same architecture/checkpoint family at multiple saved training exposures; distillation versus non-distillation controlled parents | Architecture, tokenizer, data distribution, training-stage protocol, quantizer | Effect of trajectory or training objective, rather than a confounded cross-release correlation. |
| Teacher and data | Same fixed parent, same training procedure, different prespecified calibration text/teacher targets | Student initialization and codec, optimizer/schedule, semantic examples where possible | Sensitivity to teacher choice or distillation data. If target tokenizers differ, use aligned text or appropriately defined sequence-level objectives. |
| Recipe failure vs feasibility | Frozen recipe versus an independently optimized LFM2-specific strict recipe | Parent, codec, suite and validation split | Whether an alternative solution can attain the target. Failure of both recipes does not prove infeasibility. |
| Locate damage | One-at-a-time precision restoration of kernels, gate projections, embedding/head, norms or attention in an already converted model; paired perturbations | All other tensors, task prompts, evaluation | Counterfactual diagnostic leverage of the restored group. Such mixed-precision models are never compliant product entries. Interactions mean contributions need not sum. |

A clean causal factorial model could use factors `architecture A`, `training history H`, `recipe R`, and `calibration source C`, with random seeds as replicates; include A×R and H×R interactions. The primary question is the interaction in the response surface, not merely marginal average scores. Cross-family pretrained checkpoints already differ on A, H, vocab and data and thus cannot identify the individual effects. For the causal branch one would design both teachers to be trained under a common controlled protocol; that is separate from preserving the exact public teachers in the primary claim. Neither experiment should be discarded for training cost under this brief.

The universal definition of shape dependence must be formalized. For example, row group count, padding, tensor fan-in/out, number of layers, vocabulary count and number of eligible elements are shape-derived. Selecting calibration texts according to a frozen semantic sampling policy is data-derived but not necessarily model-tuned. Selecting different learning-rate schedules or loss weights based on target validation scores is not shape-only. The project should state whether a deterministic function of *teacher statistics* is permitted. It may be a stronger general formula to say all targets use the same algorithm with no manual tuning, even if the algorithm computes data-dependent scales or losses. But this is not logically identical to "nothing changes except shapes" unless the fixed algorithm and inputs are defined at the outset. This issue should be resolved before any Qwen success is used to choose what counts as transfer.

**Unknown and cheapest discriminating observation:** complete the header/code parity audit, then derive per-tensor groupwise magnitude-error and lag-ratio distributions from the exact released weights (no model evaluation required for those statistics). Later, run the small strict loader check, freeze the recipe on Qwen, and only then unblind LFM2. That order distinguishes basic engineering defects from statistical or training failure. No result of those proposed tests is asserted here.

## 4. Probability judgments and project recommendations

### 4A. Two before/after probabilities

The forecasts are subjective, not empirical frequencies, not estimates from a fitted model, and not updates from incomplete papers treated as verified proof. They are conditional on the original LFM2-1.2B target, strict codec including embedding/output and every other learned weight, and a valid matched evaluation protocol. The first event needs a Qwen retention value. The natural near-term conditioning event is a recipe that attains the released reference's 70.2% or a similar 70-80% retention on the exact Qwen teacher. An unconditional forecast valid at both 70% and 99% would be misleading. A high-performing recipe may have very different transfer characteristics. The values below are elicited judgments, including the retrospective pre-batch prior, not a probability previously recorded at the start of the batch.

| Event | Before batch | After batch | Direction and rationale |
|---|---:|---:|---|
| A frozen recipe achieving roughly 70-80% on Qwen3-1.7B lands within five retention points on LFM2-1.2B with only prespecified shape-dependent changes | 45% | 40% | The released architecture and source code expose a genuine short-kernel grouping issue, independent multiplicative gates and a smaller unique sign budget. Shared SwiGLU structure and exact folded symmetries limit the downside, but do not establish a similar attainable function. The four-bit QAD release does not directly support this event. |
| A strict 1-bit LFM2-1.2B, by any repeatable recipe, keeps at least 70% of its own FP scores on our ten-task suite | 55% | 60% | The shared dense parameter majority, mathematically valid packed reference loader, available exact parent and freedom to optimize the codec-compatible function support feasibility. The direct QAD provenance shows a real adaptive quantization route at a much higher precision, so it suggests a tractable control but not binary success. Unknown behavior of the short kernel, small norms, tied embedding and instruction/tool tasks prevents a stronger upward update. |

No probability was discounted for training time, compute or reading budget. The judgments deliberately do not incorporate unaudited neighboring paper scores as if they were strict binary LFM2 measurements. The data do not justify 99% retention as an expected near-term outcome, nor do they prove it impossible. The event of matching 99% is much stronger than matching 70%, particularly on a small model with one shared magnitude for every 128 weights. There is no valid extrapolation from QAD's 97.4% at approximately 4.76 file bpw to 99% at 1.125 bpw.

### 4B. Changes to the project and new ideas

1. **Freeze the format before freezing the formula.** Write an explicit shape-dependent group traversal, padding, tiny-vector pooling, scale sign and rounding rule. Require exact payload audit and unique embedding/head accounting. If a dense-only variant is scientifically useful, label it separately. Do not move the binary finish line by a hidden norm or convolution exemption.
2. **Add a quantization-adapted weight control.** The publisher's FP32 QAD source is an unusually valuable intermediate artifact. Compare the original LFM2.5 weight distribution with the same architecture after QAD. For a later experiment, apply identical g128 binarization to both, keep the original model as the main denominator, and test whether four-bit adaptation moves the weights toward or away from the binary shell. Also score the QAD FP32 source on its own as a diagnostic before interpreting its compressed variant. The publisher explicitly warns that its Q4_0 result does not apply to the source or other formats. This new control is not part of the primary original-LFM2 transfer.
3. **New hypothesis: lag-ratio grouping with exact folded channel rearrangement.** Normalize each channel's three-tap filter by a nonzero channel scale, absorb that scale into the output or gate row as in §3C, cluster channels by normalized absolute lag shape, permute B/C/X rows, kernel channels and output columns together, then assign tap-major groups of 128. This can reduce dispersion in the required three shared magnitudes without introducing a side vector into the deployed checkpoint, because the permutation and scaling are already folded. To be a fair formula test, the grouping algorithm must be fixed before target outcomes and apply to any eligible depthwise tensor. It is not guaranteed to improve the *joint* binary error: the permutation changes grouping in the output projection and the scaling changes gate matrices, so optimize a joint objective and compare with no rearrangement. The invariance proof only proves preservation before quantization. The proposed improvement is untested.
4. **Use operator-specific counterfactual diagnostics, not operator-specific exemptions.** In the frozen primary recipe all weights remain binary. For scientific diagnosis restore one tensor family to its parent in temporary reference tests and measure changes; a disproportionately important tiny kernel should not be ignored because it consumes few bytes. Measure per-gate product and lag response, attention logits and teacher/student task disagreement, not only average perplexity. This is diagnosis, not a compliant deployment model.
5. **Separate predictive generalization from an architecture-aware formula.** A strict frozen recipe is the strongest transfer claim and must get the first unblinded result. A subsequent version that applies universal graph-local symmetry rules could be a more useful repeatable formula, but must declare the changed rule and earn its own trophy. Do not silently update the first formula after observing LFM2. Run the original 350M engineering check for correctness without using its benchmark outcomes to tune the target formula unless the declared training/validation policy explicitly includes that model. Then evaluate original 1.2B and later the architecture-matched 2.5 control, followed by LFM3 only as a distinct family.
6. **Do not treat 5 points of retention as a fixed absolute score gain across teachers.** If the matched LFM2 FP mean is F on a 0-to-100 scale, five retention points require 0.05 F mean score points, or 0.5 F summed points over ten equally weighted tasks. PrismML's 58.24 mean implies 29.12 summed points; LFM2's denominator will differ. The same 29.1 summed points is not the appropriate LFM2 trophy threshold unless its FP mean happens to match Qwen's.

## 5. Outstanding acquisition requests and technical workarounds

These requests are recorded at the end rather than halting the research. They do not delegate my independent analysis. The assignment's full-reading condition remains unfulfilled until the missing primary material is actually inspected. I have completed a substantive independent review of all three questions using accessible evidence, but the complete corpus, exact checkpoint-header certification, every independent score and exhaustive low-bit catalog cannot be claimed. Sections 2 and 3 explicitly distinguish provisional empirical leads from checked file facts and original derivations.

### 5A. Technical retrieval routes used and remaining alternatives

HF rendered blob views succeeded for many small JSON and license files when raw resolution failed. The actual GitHub raw code paths worked for Transformers, llama.cpp and its split converter. The arXiv HTML route recovered the report text when the PDF binary could not be loaded. HF weight-file blob pointer views exposed exact file hashes, but a pointer is not a Safetensors header. Requests to resolve links, HF metadata/range endpoints, mirrors and container network failed to yield those binary bytes. I cannot claim those files are unavailable to an ordinary external browser. Similarly, the rendered GGUF tree proves a file is listed, not what tensor types it contains. No paid account, access form or credentials should be used to overcome these failures.

The best workaround is to request only the first 8 bytes and the JSON header of each Safetensors payload. Safetensors begins with an unsigned 64-bit little-endian header length, followed by JSON; actual data offsets are relative to the end of that header. We can therefore check every name, shape, element type and byte length without reading the tensor values. The [official format specification](https://github.com/huggingface/safetensors#format) and [metadata parsing documentation](https://huggingface.co/docs/safetensors/metadata_parsing) are acquisition references, not read-in-full research sources in this review. A second workaround is Hugging Face Hub's metadata client, where supported, and the third is running the range request from a different network. The exact script below is an unexecuted external acquisition utility; it does not run or evaluate any model. Python is used only to demonstrate the short file-inspection procedure, not proposed as the project's implementation language. It can be handed to the first reviewer to run independently.

```python
import os, json, struct, math, re
from pathlib import Path
import requests
from huggingface_hub import HfApi, hf_hub_download, hf_hub_url

os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
api = HfApi()
session = requests.Session()
root = Path('lfm2-primary-audit')
root.mkdir(exist_ok=True)
models = {
    'LiquidAI/LFM2-350M': 'f37d3f5c8c5484bc01dad379a595cf4c68c4e70e',
    'LiquidAI/LFM2-1.2B': '40f3da0d0164913923aee9462c23077868b816a3',
    'LiquidAI/LFM2-700M': 'main',
    'LiquidAI/LFM2-2.6B': 'main',
    'LiquidAI/LFM2.5-350M': 'main',
    'LiquidAI/LFM2.5-1.2B-Instruct': 'main',
    'LiquidAI/LFM2.5-1.2B-Thinking': 'main',
    'LiquidAI/LFM2.5-2.6B': 'main',
}
small = {'config.json','generation_config.json','tokenizer.json',
         'tokenizer_config.json','special_tokens_map.json','chat_template.jinja',
         'README.md','LICENSE','LICENSE.txt','NOTICE','merges.txt','vocab.json',
         'model.safetensors.index.json','provenance.json'}

# Read exactly n bytes from a binary stream without reading the whole file.
def exact_read(raw, n):
    result = bytearray()
    while len(result) < n:
        part = raw.read(min(1048576, n-len(result)))
        if not part:
            raise IOError('Truncated response')
        result.extend(part)
    return bytes(result)

def prefix(url, start, n):
    # Some CDNs ignore Range and return HTTP 200. Stream only the required prefix.
    with session.get(url, headers={'Range': f'bytes={start}-{start+n-1}',
                                   'Accept-Encoding': 'identity'},
                     stream=True, timeout=(30,120)) as r:
        r.raise_for_status()
        if r.status_code == 206:
            m = re.fullmatch(r'bytes (\d+)-(\d+)/(\d+|\*)',
                             r.headers.get('Content-Range',''))
            if not m or int(m[1]) != start or int(m[2]) < start+n-1:
                raise IOError('Unexpected Content-Range')
        elif r.status_code == 200:
            if start > 8:
                raise IOError('Unbounded prefix skip refused')
            exact_read(r.raw,start)
        else:
            raise IOError(f'Unexpected status {r.status_code}')
        return exact_read(r.raw,n)

def get_header(repo, rev, filename, file_size):
    url = hf_hub_url(repo, filename, revision=rev)
    n = struct.unpack('<Q',prefix(url,0,8))[0]
    if n < 2 or n > 100_000_000:
        raise ValueError(f'Invalid header length {n}')
    raw = prefix(url,8,n)
    header = json.loads(raw)
    if not isinstance(header,dict):
        raise ValueError('Not a tensor header')
    widths = {'BOOL':1,'U8':1,'I8':1,'F8_E4M3':1,'F8_E5M2':1,
              'BF16':2,'F16':2,'I16':2,'U16':2,'F32':4,'I32':4,
              'U32':4,'F64':8,'I64':8,'U64':8}
    ranges=[]
    for name,t in header.items():
        if name == '__metadata__':
            continue
        a,b = t['data_offsets']
        assert 0 <= a <= b
        if t['dtype'] in widths:
            assert b-a == math.prod(t['shape'])*widths[t['dtype']], name
        ranges.append((a,b,name))
    cursor=0
    for a,b,name in sorted(ranges):
        assert a==cursor, (name,'gap or overlap',a,cursor)
        cursor=b
    if file_size is not None:
        assert 8+n+cursor == file_size, (8+n+cursor,file_size)
    return header

errors=[]
for repo, requested in models.items():
    folder=root/repo.replace('/','__')
    folder.mkdir(exist_ok=True)
    try:
        info=api.model_info(repo,revision=requested,files_metadata=True,token=False)
        rev=info.sha
        manifest={'repo':repo,'requested':requested,'revision':rev,'files':[]}
        for s in info.siblings:
            fn=s.rfilename
            lfs=getattr(s,'lfs',None)
            manifest['files'].append({'name':fn,'size':s.size,
                'sha256':getattr(lfs,'sha256',None),'blob_id':getattr(s,'blob_id',None)})
            try:
                if Path(fn).name in small:
                    hf_hub_download(repo,fn,revision=rev,local_dir=folder,token=False)
                elif fn.endswith('.safetensors'):
                    data=get_header(repo,rev,fn,s.size)
                    out=folder/(fn+'.header.json')
                    out.parent.mkdir(parents=True,exist_ok=True)
                    out.write_text(json.dumps(data,indent=2))
            except Exception as e:
                errors.append({'repo':repo,'revision':rev,'file':fn,'error':repr(e)})
        (folder/'manifest.json').write_text(json.dumps(manifest,indent=2))
    except Exception as e:
        errors.append({'repo':repo,'revision':requested,'error':repr(e)})
(root/'errors.json').write_text(json.dumps(errors,indent=2))
```

This utility is deliberately limited to metadata, configuration, templates and header reads. If the server sends a full response, streaming and immediate closure avoids intentionally downloading the entire tensor payload. Some proxies still buffer whole responses, so the failure log is important. An independently run local utility should report actual HTTP codes and content ranges, rather than assuming a Range header is honored. The header audit cannot verify the SHA256 of the entire model payload without reading the whole payload; the manifest records the publisher's declared hash, not an independent hash of the weights. For full authenticity, download and hash the actual target weights later, which is necessary before training anyway. For new model IDs in the family catalog, first obtain the real repo name using the official API, rather than hardcoding every unverified candidate above.

For GGUF, use the pinned llama.cpp repository's `gguf-py` reader on the actual files, or a range-aware header parser. Collect every tensor name, shape, type, offset, `n_elements` and `n_bytes`. Calculate both tensor payload bpw and complete file bpw. Save the metadata key/value table and parent references. Where the package can only memory-map a local file, downloading the binary is necessary for that route, but no inference is needed. A range-aware parser can traverse GGUF metadata and tensor descriptors using the format specification, with bounds checks, without retrieving weights; it should be independently compared against the local reference reader on one small file. This is preferable to inferring type composition from filenames. I did not execute such a parser on remote GGUF files in this batch.

### 5B. Handoff to the first reviewer: acquisition only

Provide this section to the first reviewer without asking for its independent scientific conclusions. Request one ZIP of original primary files and raw metadata, plus a manifest of URLs, commits, file hashes, access failures and exact retrieval commands. No account credentials or gated forms. The deliverables are:

1. Complete original [LFM2 Technical Report PDF](https://arxiv.org/pdf/2511.23404), any supplemental or source archive, official release figures and full benchmark appendix.
2. The pinned original 350M/1.2B binary header JSON, exact configs/tokenizer/chat templates/licenses and public file SHA metadata; then the other original and LFM2.5 dense text variants, using the utility or an equivalent range reader. Include both `main` and requested pinned revisions for the selected checkpoints to verify that the current reconstruction matches the historical snapshot.
3. All publisher model cards, config/tokenizer/license/template files and official full historic repository catalog, with API pagination, revision and release-date evidence, including specialized family models and LFM3 successor. Record actual repository IDs and remove any erroneous candidate in §1B.
4. The four official QAD directories, including their README, provenance, original source header and released GGUF tensor descriptors. Obtain the complete blog charts and any public QAD implementation, training configuration or accompanying technical note if it exists. Identify precisely what is not published.
5. Full GGUF metadata manifests of the files in §2C, then enumerate additional LFM2 and LFM2.5 family PTQ/QAT builds across Hugging Face and public GitHub. For each preserve original card, parent revision, exact quantizer method if documented, importance-matrix data provenance, file size and any raw evaluation outputs. Include the original 350M and 1.2B even if additional lower-bit repos are found. Do not simply collect generated usage instructions as evidence of tested functionality.
6. Pin and archive the complete relevant source paths in [Transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/lfm2), [llama.cpp](https://github.com/ggml-org/llama.cpp), [MLX-LM](https://github.com/ml-explore/mlx-lm) and [MLX Swift](https://github.com/ml-explore/mlx-swift-lm). Include actual packed lookup/matmul kernels, convolution kernel dispatch, quantizer selection, converter, norm and embedding handling. Capture the exact commit of each repository, and include Q1_0 support history where relevant. I need the files, not another reviewer's conclusion about whether they run.
7. Full primary PDFs/HTML source archives, appendices and public code for the adjacent research in §§2F,2G,3A,3B: Bi-Mamba, Quamba2, BD-Net, binary MobileNet, BinaryLLM, ParetoQ, OneBit, Scaling Laws for Precision, Training Dynamics and Low-Bit Quantization Favors Undertrained LLMs. Follow author code links and record exact commit. Where a paper has no released code, include evidence of the code availability statement instead of inventing a repository.

### 5C. Owner acquisition fallback

If the first reviewer cannot retrieve the materials, the priority owner downloads are the [full report PDF](https://arxiv.org/pdf/2511.23404), the two original selected model header/metadata bundles, and the [MLX-LM source archive](https://github.com/ml-explore/mlx-lm/archive/refs/heads/main.zip). Prefer the metadata-only script output to downloading gigabytes solely for a shape check. The [QAD primary source directory](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/tree/main/qad) has a separate source checkpoint and provenance; retrieve its metadata only at this stage. The exact public links and missing artifacts are documented above. These requests are not a reason to defer the substantive research already recorded in this document.

The evidence required to upgrade the review to the original full-reading standard is explicit. A later ingestion must verify each primary file independently, revise the source ledger, replace reconstructed tensor metadata with actual header entries, and change scientific conclusions only where the new primary evidence warrants it.
