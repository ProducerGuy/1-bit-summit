# 1 Bit Summit: no-form reference-pair search

Research date: 24 November 2026. Scope: publicly listed checkpoint files, publisher statements, public code and reported evaluations. No model was trained or evaluated. I did not inspect the bytes of a multi-gigabyte weight file or calculate a checkpoint checksum; the distinction between a publicly listed repository and a byte-verified download is preserved throughout.

## 1. Decision and access rule

**Decision:** Do not submit Meta's ParetoQ access form. The official Meta checkpoints are gated and the model card expressly requests a full legal name, date of birth and organization information. That violates the owner's access rule even though ParetoQ is the cleanest *documented* binary fine-tuning parent-child lineage in the candidate set. The repository containing its training code is public, but public source code does not remove the checkpoint gate.

**More important discovery:** There are two useful, ungated Qwen3-1.7B alternatives with different evidentiary roles:

1. **`precision-numerics/Boole-1.7B`** is a publicly listed, approximately 247 MB packed **1-bit/g128** child of `Qwen/Qwen3-1.7B`. This is the best *exact-parent and exact-format weight comparator*. Its training procedure and budget are not publicly established in the material I could verify, so it is **not** a known-recipe training reference.
2. **`alllwang/bonsai-repro-1.7B-ternary`** is a publicly listed **trained** ternary child of the exact Qwen3-1.7B parent, with training configuration, a training log and task evaluations. This is the best *known-training reference*. Its ternary codebook, Hadamard basis and BF16 export are not directly comparable with Bonsai's first-generation binary sign/scale fingerprint.

No accessible candidate that I could verify simultaneously satisfies all five strict conditions: ungated files, exact pretrained parent, a trained binary child, a sufficiently published recipe and budget, and a directly comparable g128 deployment representation. That is a statement about this documented search, **not** a claim that such a pair does not exist anywhere.

### 1A. Ranked candidate table

Probabilities below are subjective judgments of **practical usefulness as a reference under the no-form rule**, not probabilities that a scientific hypothesis is true. For clarity, the strict-reference column separately answers whether the candidate meets *all* requirements without additional missing facts.

| Rank | Candidate | Public file listing | True parent + known training | Same binary g128 format | Chance usable for a meaningful reference | Chance satisfies *strict* definition now |
|---|---|---|---|---|---:|---:|
| 1 | **Boole-1.7B + Qwen3-1.7B** | Yes, ungated repository listing | Parent is identified; training recipe/budget **not documented** | Claimed yes, with tied-head scale qualification | **90%** for actual deployed-weight fingerprint | **8%** |
| 2 | **alllwang ternary QAT + Qwen3-1.7B** | Yes, publicly indexed model and training files | Yes, documented community reproduction | No, ternary and rotated | **85%** for known-training *ternary* comparator | **0%** for binary; **75%** for weaker ternary definition after byte checks |
| 3 | **Meta MobileLLM-ParetoQ-1.5B BF16 + 1-bit** | Both official repositories exist but **gated** | Yes, explicitly established by publisher | No, rowwise binary scale and latent checkpoint | **0%** under no-form rule | **0%** |
| 4 | **Meta MobileLLM-ParetoQ-1B BF16 + 1-bit** | Same gate | Same publisher-established lineage | Same mismatch | **0%** under no-form rule | **0%** |
| 5 | **PrismML Bonsai-1.7B unpacked + Qwen3-1.7B** | Public | Parent known; training method unknown | Yes, exported/deployed equivalent | **95%** for reproducing original fingerprint | **0%** as *independent known-recipe* control |
| 6 | **FBI-LLM 1.3B and other from-scratch binary releases** | Some public artifacts/code | **No pretrained FP parent** for the claimed binary training | Varies | **15%** as contextual evidence | **0%** |

See evidence and caveats in Sections 2 to 6. A probability of 0% for a gated candidate reflects the owner's absolute access constraint, not a view of the underlying research's value.

## 2. First choice: Meta MobileLLM-ParetoQ

### 2A. Exact official file locations and provenance

Publisher's training repository: <https://github.com/facebookresearch/ParetoQ>.

Official paired repositories, preferred sizes:

- 1.5B FP parent: <https://huggingface.co/facebook/MobileLLM-ParetoQ-1.5B-BF16/tree/main>
- 1.5B binary child: <https://huggingface.co/facebook/MobileLLM-ParetoQ-1.5B-1-bit/tree/main>
- 1B FP parent: <https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-BF16/tree/main>
- 1B binary child: <https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-1-bit/tree/main>
- Also listed for 600M, 350M and 125M via the publisher's model-release table and linked model collection in the [ParetoQ README](https://github.com/facebookresearch/ParetoQ#model-release).

The 1B 1-bit child file listing identifies a `pytorch_model.bin` checkpoint of about **2.01 GB**, together with config/tokenizer files: <https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-1-bit/tree/main>. The specific size of the 1.5B file and both BF16 parents was **not independently verified** from downloaded files in this environment. For either size, the canonical location is the official `facebook` repository and its `Files` tree, not a third-party repost.

Publisher statement, verbatim in substance: its quantized MobileLLM models were **all fine-tuned on top of `MobileLLM-ParetoQ-BF16`**. This proves the **documented** parent-child relationship much more strongly than matching architecture/config files alone. Source: [official README, Model Release/News](https://github.com/facebookresearch/ParetoQ). The statement alone is not a cryptographic derivation proof; final byte-level confirmation would require checkpoint access and training provenance.

### 2B. Access and license

- On the official 1.5B child page, Meta requires a **full legal name, date of birth, and full organization name**, and provides a gated-access form. See [the official page](https://huggingface.co/facebook/MobileLLM-ParetoQ-1.5B-1-bit), particularly its access statement and embedded license.
- The 1B and smaller model file listings also say **Gated model**. Example: [1B tree](https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-1-bit/tree/main) and [125M tree](https://huggingface.co/facebook/MobileLLM-ParetoQ-125M-1-bit/tree/main).
- The **model weights** are marked `fair-noncommercial-research`, with the FAIR Noncommercial Research License printed on the model card. The publisher's **code** is distributed under a separate GitHub license. Do not confuse those terms or claim that the model weights inherit the code license.
- **Actual access outcome:** The metadata/card were readable without signing in. The protected weight bytes were **not available** under the permitted no-form/no-credential route. This disqualifies the models.
- A mirror would only be a trustworthy substitute if the exact content can be tied to official weight hashes or a publisher-endorsed release, and redistribution is permitted under the license. I found **no independently authenticated ungated mirror** in the search performed, and therefore do not recommend an unauthorized or unauthenticated repost.

### 2C. What is in the child checkpoint

The child is labeled 1-bit **at training/forward quantization**, but the model file is approximately full-sized. The `.bin` format is a PyTorch serialized checkpoint containing high-precision tensor state, not a byte-packed 1.125-bpw inference artifact. The indexed tensor/file viewer identifies PyTorch/BF16 tensor storage. Source: [1B file listing](https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-1-bit/tree/main); [released training implementation](https://github.com/facebookresearch/ParetoQ/blob/main/train.py).

The [training script](https://github.com/facebookresearch/ParetoQ/blob/main/train.py) constructs a quantized causal LM from a pretrained checkpoint and initializes the binary weight scale/clip value using the **mean absolute value along the output row**. This is an output-channel/row scale, **not a separate FP16 scale for each consecutive 128 weights**. Its weight representation, module exemptions, optional full-precision elements and exact per-checkpoint training-token count must be audited in the [model implementation](https://github.com/facebookresearch/ParetoQ/tree/main/models), [launch script](https://github.com/facebookresearch/ParetoQ/blob/main/1_run_train.sh) and paper <https://arxiv.org/abs/2502.02631>. The release statement establishes the training family, not a unique reproducible token count for the MobileLLM checkpoint itself.

**Critical comparator rule:** To analyze ParetoQ sign differences, apply the released **forward quantizer** to the latent tensors and compare its effective deployed binary matrices with the BF16 parent. Comparing latent BF16 shadow weights directly with the parent would measure a different object and produce a false fingerprint. Even after applying the correct quantizer, ParetoQ's per-row scale geometry is not Bonsai's group-of-128 geometry.

### 2D. Published paired scores

These are the publisher's **eight-benchmark averages**, not PrismML's ten benchmark suite, and `retention` below is computed from its own displayed teacher/child averages. Perplexity is shown separately, not used in the percentage calculation. Source for every row: [official ParetoQ README, Model Release](https://github.com/facebookresearch/ParetoQ#model-release).

| MobileLLM size | BF16 parent avg | 1-bit child avg | Child / parent | BF16 Wiki ppl | 1-bit Wiki ppl |
|---|---:|---:|---:|---:|---:|
| 125M | 48.5 | 43.7 | 90.1% | 15.1 | 25.8 |
| 350M | 54.8 | 47.6 | 86.9% | 10.5 | 17.0 |
| 600M | 58.2 | 50.3 | 86.4% | 9.1 | 14.0 |
| 1B | 62.1 | 53.8 | 86.6% | 8.0 | 12.8 |
| 1.5B | 62.7 | 55.9 | 89.2% | 7.9 | 11.0 |

These strong results make ParetoQ an interesting *scientific reference*, but they neither override the access prohibition nor establish equivalent results in our whole-model codec. No full-precision parent weight bytes or exact child latent checkpoint bytes were read here.

## 3. Strongest ungated exact-format comparator: Boole-1.7B

### 3A. Parent, child, files and access

- Official parent: <https://huggingface.co/Qwen/Qwen3-1.7B/tree/main>. The parent repository's weight filenames are `model-00001-of-00002.safetensors` and `model-00002-of-00002.safetensors`, with `model.safetensors.index.json`; format SafeTensors; approximately 3.4 GB of BF16/FP weights in total. The parent is **Qwen3-1.7B**, not Qwen3-1.7B-Base.
- Child: <https://huggingface.co/precision-numerics/Boole-1.7B/tree/main>, with **`Boole-1.7B.safetensors` (~247.1 MB)**, `config.json` and license/notice files. File format: **SafeTensors**. Model card: <https://huggingface.co/precision-numerics/Boole-1.7B>.
- Separate inference encoding: <https://huggingface.co/precision-numerics/Boole-1.7B-GGUF>, with `Boole-1.7B-Q1_0.gguf`; model card describes the GGUF download path.
- Publisher announcement: <https://precisionnumerics.ai/blog/boole-1p7b>. Public runtime/code: <https://github.com/PrecisionNumerics/boole-demo>.
- Access: the public Hugging Face model listing shows **no gated-model restriction**, and the model card provides the ordinary public file links. **I could inspect the listing without credentials but did not fetch the 247 MB weight bytes**, so direct unauthenticated transfer and cryptographic hash validation remain unverified in this research environment.
- License in the published model listing: **Apache-2.0**. The official Qwen3 parent is likewise Apache-2.0. Verify the actual `LICENSE`/`NOTICE` files alongside the checkpoint before redistribution.

### 3B. What its file represents and why it is valuable

The publisher states that the child is derived from Qwen3-1.7B and that the 247 MB checkpoint stores **packed binary sign bits plus per-group FP16 scales for groups of 128**, including embedding/head treatment. This is the same structural neighborhood as Bonsai and uniquely useful as a same-parent control. The separate GGUF Q1_0 encoding is also published. Sources: [publisher model card](https://huggingface.co/precision-numerics/Boole-1.7B) and [technical announcement](https://precisionnumerics.ai/blog/boole-1p7b).

**Qualification:** The public description indicates that embedding and output can share sign bits while retaining different scales. That is a storage and function-level detail to audit: it may not be a bit-for-bit match for a strict *one* FP16 scale per shared group if both input and output roles need independent scales. Use **body-only comparisons first** if exact treatment differs. The claimed 247.1 MB size alone does not prove every matrix conforms to the codec or that there are no extra learned degrees of freedom; inspect the SafeTensors header, config and pack/decode code.

**Not demonstrated:** I found no disclosed training loss, dataset, token budget, optimizer trajectory or staged checkpoints showing how the binary child was obtained. It might be trained, distillation-assisted or conversion-optimized, but the **public file listing does not prove a particular procedure**. Consequently it is not the known-training reference sought in the strict definition. A binary checkpoint can still yield exact parent-relative sign/scale statistics without its training recipe; it cannot identify the *cause* of those statistics by itself.

### 3C. Reported scores, and a serious comparison warning

The publisher reports **50.55** for the Boole-1.7B student against **58.83** for its Qwen3-1.7B BF16 teacher on its reported ten-benchmark run, equivalent to **85.9%** retention. Source: [Boole announcement](https://precisionnumerics.ai/blog/boole-1p7b) and [model card](https://huggingface.co/precision-numerics/Boole-1.7B).

For comparison, PrismML's separate original publication gives Qwen3-1.7B **58.24** and Bonsai-1.7B **40.88**, or **70.2%** on *its* run. Source: [PrismML whitepaper repository](https://github.com/PrismML-Eng/Bonsai-demo), `1-bit-bonsai-8b-whitepaper.pdf`, table 9.

**Do not directly subtract 85.9% from 70.2% and award three five-point milestones.** The teacher scores already differ, and the independent publisher's measurements must be reproduced with a matched harness, model loading path, scoring and prompts before the relative result is treated as comparable. Also, it is not known from the public model card whether the Boole model used test-related optimization. I have not trained or evaluated either model here.

### 3D. Cheapest verification and likely payoff

The lowest-cost resolution is **metadata and header verification**, not model inference:

1. From an unauthenticated client, download the exact public repository snapshot of the parent, child, config, and unpack/runtime code; pin the full Hugging Face revision SHA and retain the publisher's canonical paths.
2. Record file sizes and independently computed SHA-256 hashes, including the child's `Boole-1.7B.safetensors`. Do not invent official hashes: a displayed Xet object identifier is not necessarily the SHA-256 of the downloaded SafeTensors bytes.
3. Read the SafeTensors tensor directory and the decoder to confirm which tensors store the sign bits, which store FP16 scales, how the 128-element grouping is ordered, and whether the tied embedding/head has extra scales. Check the emitted per-tensor weight count equals the parent for comparable matrices.
4. Reconstruct effective weight matrices **without generating text or training**, then compute the same magnitude-binned sign flips, scale-to-parent mean ratios and cosines used in the Bonsai forensic analysis. This gives a useful *second released binary fingerprint* even if its training process is still undisclosed.

**Recommendation:** Pursue as the first publicly accessible **binary, same-parent, codec-close** pair; label it *unknown-recipe binary comparator*, never *proved known-QAT comparator*.

## 4. Best ungated known-training comparator: independent Qwen3-1.7B ternary reproduction

### 4A. Exact model and training record

- FP parent: <https://huggingface.co/Qwen/Qwen3-1.7B/tree/main>, official SafeTensors files described in Section 3A.
- Child repository: <https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary> and its [complete tree](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/tree/main).
- Child model-card provenance/recipe: <https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/README.md>.
- Recorded training configuration: <https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/log.txt>.
- Training source: see the repository's `training/` directory and the `train_bonsai_repro.py` referenced in the model card. A direct exact `model.safetensors` or shard filename and checksum **could not be confirmed from the available indexed listing**, so I will not invent one. The precise location for obtaining whichever shard(s) the publisher actually uploaded is the linked **child repository Files tree**. This is an explicit remaining verification failure against the user's requested exact-file standard.
- License in the child model's published metadata: **Apache-2.0**. Public page/tree do not display a form requirement. An unauthenticated *actual checkpoint byte transfer* was **not completed** here.

### 4B. Mechanism, weights and tokens

The public model card describes a **teacher Qwen3-1.7B -> ternary student** recovered through QAT, using a blockwise signed Hadamard representation, with **42 zeros among 128 weights**, 86 nonzero ternary codes, and a scale per 128-weight group. It includes the tied input/output matrix in the quantized path, unlike many body-only low-bit results. The model uses a 1024-wide transform block and an inverse transform to materialize an ordinary Hugging Face model for evaluation. Source: [model card](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary).

The published command-line settings in [training/log.txt](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/log.txt) include:

| Field | Recorded value |
|---|---|
| `model` | `Qwen/Qwen3-1.7B` |
| `steps` | 20,000 |
| `lr` | 0.00006 |
| `bs` | 4 |
| `accum` | 2 |
| `seq` | 1,024 |
| `nzero` | 42 |
| `block` | 1,024 |
| `no_rot` | `False` |
| `seed` | 0 |
| `quant_embed` | `True` |
| `unfreeze_norms` | `True` |
| `ce_weight` | 0.1 |
| `data_mix_v2` | `True` |

From these parameters, nominal processed training tokens equal **20,000 × 4 × 2 × 1,024 = 163,840,000**. This is calculated processed token positions, not a guarantee of unique text tokens; it assumes the logged run completed the stated steps without padding reductions or truncation. The exact data mixture and loss implementation are defined by the training source rather than the abbreviated command line. The model card/log are primary evidence for a published training process, not independent proof of every operation.

**Extremely important representation caveat:** The released Hugging Face checkpoint is described as a **BF16 reconstructed/dequantized and inverse-rotated representation**, not a native file of explicit `{-1,0,+1}` codes and scales. Directly counting the signs of the loaded child tensor against the parent's raw weights mixes coordinate systems and therefore does **not** measure ternary sign-flip training. To recover comparable discrete codes, inspect the transform, use its correct rotation direction and code-selection rule, recover ternary coordinates (allowing for BF16 round-trip error), and compare within the same basis. If exact group scales are not saved separately, reconstructing them from BF16 output may be approximate.

The model's logged sign-change and mask-change rates are **between training checkpoints / initial ternary state and final state**. They do not equal the fraction of the parent FP weights whose signs differ from a deployed binary child. This is precisely why the reference helps explain how training evolves, but does not automatically classify Bonsai's 29% parent-child sign differences.

### 4C. Reported task scores

The following public results use an `lm-eval` evaluation family, including mixed zero-shot and five-shot settings, **not** the exact PrismML ten-task harness. Parent and child are from the community reproducer's published card, not measured in this research session. Source: <https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary>.

| Benchmark | Qwen3-1.7B parent | Trained ternary reproduction | Child / parent |
|---|---:|---:|---:|
| ARC-Challenge | 43.0 | 33.5 | 77.9% |
| HellaSwag | 60.5 | 46.5 | 76.9% |
| PIQA | 72.2 | 66.1 | 91.6% |
| Winogrande | 60.5 | 58.3 | 96.4% |
| MMLU | 60.2 | 34.5 | 57.3% |
| GSM8K | 68.8 | 54.7 | 79.5% |

Some of these reported results fall substantially below the publisher's original Qwen baseline. Their value here is not demonstrated state-of-the-art retention. It is that **training-derived sign/mask/scale behavior is potentially inspectable with a named starting point and disclosed training settings**.

### 4D. Cheapest verification

Before investing in large-file downloads, confirm the child `Files` tree names and exact tensor header, and inspect `train_bonsai_repro.py` to verify whether packed ternary code/mask/scale checkpoints survive in `training/`. **If intermediate packed code checkpoints do exist, prefer them over trying to reverse-engineer codes from an inverse-rotated BF16 export.** Those intermediate artifacts, if publicly downloadable, would make this candidate an especially useful training-trajectory control. I did not verify their existence.

## 5. Other candidates and exclusions

### 5A. PrismML's own published Bonsai 1.7B

- Parent: <https://huggingface.co/Qwen/Qwen3-1.7B/tree/main>.
- Child released unfolded FP representation: <https://huggingface.co/prism-ml/Bonsai-1.7B-unpacked/tree/main>, with [`model.safetensors`](https://huggingface.co/prism-ml/Bonsai-1.7B-unpacked/blob/main/model.safetensors) shown at **3.44 GB**. It contains effective unpacked full-precision values, not the compact deployed sign-bit file.
- Deployed binary is also distributed through PrismML's GGUF/other 1-bit repositories. See the publisher namespace and [official whitepapers](https://github.com/PrismML-Eng/Bonsai-demo).
- The parent/child relation is publisher stated, the benchmark scores are published, and the original fingerprint can be repeated. **Its construction recipe is still undisclosed**; using it as a training-reference would simply restate the unresolved question. The 3.44 GB file size is expected for dequantized FP values and does not violate the low-bit packed deployment claim.

### 5B. FBI-LLM and binary-from-scratch releases

- FBI-LLM paper/code: <https://github.com/LiqunMa/FBI-LLM>. Its published methodology is training binary networks **from scratch**, not a known transformation of a specific released pretrained FP parent.
- Published binary checkpoints, where accessible, can help with binary weight-distribution statistics but **cannot yield trained-from-parent sign-flip rates** unless a true source parent is identified. No such parent was confirmed in the search.

### 5C. OneBit, BinaryLLM, HESTIA and other research checkpoints

- OneBit source: <https://github.com/xuyuzhuang11/OneBit> and <https://arxiv.org/abs/2402.11295>. It begins from a pretrained model, but the quantized parameterization includes learned row/column magnitude factors. It is not g128 sign plus one FP16 scale, and I did not establish an authenticated, publicly downloadable finished pretrained-parent/child pair of the requested kind from its released listings.
- BinaryLLM research: <https://arxiv.org/abs/2508.06974>. Its experimental weight-accounting commonly leaves major matrices in FP; a suitable ungated *trained 1-bit pair* with authoritative parent and budget was not verified in this search.
- HESTIA: <https://arxiv.org/abs/2601.20745>. Ternary conversion research with public code claims, but no specific checkpoint pair passed the exact availability, file/lineage and no-form proof in the material inspected. This is a candidate for later vetting, not a confirmed match.
- Related generative/ternary community ports whose parent is already Bonsai, or whose only change is repacking, are **not** independent known-recipe Qwen-FP-to-binary conversions. A byte-for-byte lossless repack provides storage evidence but no new trained parent-child fingerprint.

## 6. What fingerprint would actually settle the causal question?

### 6A. Three different objects must not be conflated

Let `W0` denote the original pretrained FP tensor, `Z` the latent floating-point parameter optimized during QAT, and `Q(Z)` the weight matrix produced by the actual deployed quantizer.

- **Parent to shadow:** `W0` versus `Z` is *latent movement*. ParetoQ saves this kind of state.
- **Parent to effective child:** `W0` versus `Q(Z)` is *deployed code movement*. This is the proper counterpart to PrismML's unpacked binary model.
- **Early deployed child to late deployed child:** `Q(Z_start)` versus `Q(Z_end)` is the *sign-flip rate during training*. It can be tiny even when `sign(Q(Z_end))` differs substantially from `sign(W0)` because the initial code assignment may already differ.

The user's 29% parent-relative sign discrepancy therefore cannot, on its own, establish a trained versus compensation-only history. Both a discrete sign search and a trained checkpoint can alter code assignments, while transformed coordinate systems introduce further ambiguity.

### 6B. Common definition of the three requested measurements

For each *matching matrix* in the *same coordinate basis and transpose convention*, define:

1. **Parent-child sign-change fraction**: number of elements with `sign(W0_ij) != sign(Q(Z)_ij)` divided by the total number of comparable nonzero-parent elements. Define how exact zeros, ties and BF16 rounding are treated. Report per-matrix unweighted values **and** a pooled, weight-count-weighted value; never mix them without labeling.
2. **Magnitude-conditioned sign changes**: same fraction within explicitly stated quantiles of `abs(W0)` **per matrix or globally, consistently**. Parent near-zero entries can change signs frequently with little functional impact. State bin edges and sample counts.
3. **Scale ratio**: for each actual g128 grouping used by the deployed child, `scale_child(g) / mean(abs(W0[g]))`, where the denominator is computed **after any equivalent permutation or rotation** that determines the deployment groups. Distinguish a median over all groups from a median of per-matrix medians and from a ratio of global means. For a row-scaled model, use the appropriate row grouping, not synthetic g128 slices.
4. **Cosine similarity**: `dot(W0,Q(Z)) / (norm(W0)*norm(Q(Z)))`, always on a matched matrix and basis; report pooled flattening separately from per-layer medians. Also consider activation-weighted functional similarity, since raw weight cosine does not establish capability retention.

**Position breakdowns** must distinguish tensor kind (attention `q/k/v/o`, gate/up/down MLP, embedding/head), layer depth, output/input axis and actual quantizer group offsets. A dramatic change in one matrix type can be concealed by pooled averages.

### 6C. A more decisive comparator than a single trained endpoint

**My inference:** A known-QAT parent and final child remain useful, but two additional checkpoints would answer the actual research question more directly:

- `W0`, the authenticated FP parent;
- `Q(Z_init)`, the child *immediately after initialization/rounding*;
- `Q(Z_final)`, the child after documented recovery training, with actual step/token count;
- optionally `Q(Z_mid)` for the trajectory.

This decomposes parent-child changed signs into initialization effects and training effects. A final checkpoint alone does not permit that decomposition. If matching public intermediate checkpoints cannot be found, the published training source and publicly accessible parent allow a controlled *future* reproduction, but **no experiment or training was undertaken for this research task**.

The same decomposition applies to scales: parent group mean, initial binary optimum and final learned scale should be tracked separately. The empirical 2.1x scale ratio may come from activation-aware reconstruction, trained gain compensation, a different effective group definition or several mechanisms combined. An endpoint histogram cannot distinguish them.

## 7. Final recommendation and evidence status

**Recommendation 1:** Use the **ungated Boole-1.7B/Qwen3-1.7B** listing to build a second *binary, same-parent, g128-close* weight fingerprint. This bypasses Meta's form entirely. It is particularly useful for testing whether Bonsai's roughly 29% changed signs and enlarged scales are unusual among publicly released g128 binary models. Do not attribute Boole's fingerprint to a known training algorithm; its recipe is unverified.

**Recommendation 2:** Use the **alllwang Qwen3-1.7B trained ternary reproduction** as a clearly labeled *weaker, known-training mechanism control*, preferably from authentic saved ternary-code checkpoints rather than the BF16 inverse-transformed export. Its accessible training log documents approximately 164 million processed token positions, and its exact parent is Qwen3-1.7B. It does not settle the behavior of *binary* g128 training.

**Recommendation 3:** Stop pursuing gated ParetoQ weights under the owner's rules. The documented official parent-child lineage is valuable evidence, but the weight files are not obtainable by an approved route from the official repository. The FAIR Noncommercial Research License and required personally identifying form are independent barriers to adoption as an unrestricted reference.

**What I confirmed:** Official publisher/author repository identities, public model-card links and listings, ParetoQ's model gate and request for identifying information, Meta's documented model lineage, public training-log settings for the ternary reproduction, Boole's published model size/format claims, and the cited scores.

**What I could not confirm:** Actual unauthenticated transfer of the full public checkpoint bytes in this runtime, byte-level hashes or signed release manifests for the proposed public pairs, exact r9 ternary weight shard filenames, the full Boole training recipe and training budget, or intermediate binary sign trajectories from any ungated parent-child pair with a fully disclosed large-budget recipe. These are real evidentiary limits, not proof that no matching reference exists elsewhere.

The decisive distinction is: **Boole appears accessible and format-compatible, but is not known-QAT; the r9 Qwen ternary checkpoint is documented-QAT, but is not binary. Neither should be mislabeled.**

## 8. Source ledger and search coverage

Primary source paths inspected through public indexed pages and repository listings:

- [Meta ParetoQ official repository, parent-child statement, scores and code](https://github.com/facebookresearch/ParetoQ)
- [Meta 1.5B gated child and FAIR Noncommercial Research License](https://huggingface.co/facebook/MobileLLM-ParetoQ-1.5B-1-bit)
- [Meta 1B child file tree](https://huggingface.co/facebook/MobileLLM-ParetoQ-1B-1-bit/tree/main)
- [Meta 125M child file tree](https://huggingface.co/facebook/MobileLLM-ParetoQ-125M-1-bit/tree/main)
- [Meta quantized training driver](https://github.com/facebookresearch/ParetoQ/blob/main/train.py)
- [ParetoQ paper](https://arxiv.org/abs/2502.02631)
- [Official Qwen3-1.7B pretrained parent](https://huggingface.co/Qwen/Qwen3-1.7B/tree/main)
- [Boole child model card](https://huggingface.co/precision-numerics/Boole-1.7B)
- [Boole child file tree](https://huggingface.co/precision-numerics/Boole-1.7B/tree/main)
- [Boole publisher announcement](https://precisionnumerics.ai/blog/boole-1p7b)
- [Boole runtime code](https://github.com/PrecisionNumerics/boole-demo)
- [Boole GGUF release](https://huggingface.co/precision-numerics/Boole-1.7B-GGUF)
- [alllwang public Qwen3-1.7B ternary QAT model and scores](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary)
- [alllwang training log](https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary/blob/main/training/log.txt)
- [PrismML Bonsai 1.7B unpacked model](https://huggingface.co/prism-ml/Bonsai-1.7B-unpacked)
- [PrismML Bonsai whitepaper source repository](https://github.com/PrismML-Eng/Bonsai-demo)
- [FBI-LLM source](https://github.com/LiqunMa/FBI-LLM)
- [OneBit paper](https://arxiv.org/abs/2402.11295) and [public repository](https://github.com/xuyuzhuang11/OneBit)
- [BinaryLLM paper](https://arxiv.org/abs/2508.06974)
- [HESTIA paper](https://arxiv.org/abs/2601.20745)

Searches covered the ParetoQ model collection and filename/gate listings, ungated public binary Qwen-derived models, public Qwen3-1.7B ternary QAT reproductions, known from-scratch binary releases, the OneBit/BinaryLLM/HESTIA families, checkpoint files, and alternative public repacks. **No access form was submitted, no paid source was used, and no model training or inference was performed.**
