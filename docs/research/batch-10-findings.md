# Batch 10 findings

First reviewer. The brief is `batch-10-prompt.md`. Three items: LFM3 in depth, the transfer rule in writing, and the sources that batches 6 and 7 read in part. Every figure has its source in section 8. What was not read is in section 9. Probabilities are judgments.

How sources were read. Web pages and papers through a fetch tool that returns an account of a page and not its text; no figure was seen. Code through the repository reader, file by file. Counts and identities were checked by `scripts/b10_bits.py`.

## 1. Result

- **LFM3 is now in one place.** Its graph, counts, template, reasoning switch, training history, runtime treatment and every quantized build are in section 2. Nothing in it contradicts batch 7's tensor table, and the total of 1,728,801,536 weights is confirmed a second way from the model code.
- **The reference runtime does not store what the project calls its format.** Its converter writes every normalization gain and every depthwise kernel in 32 bits, not 16. Its quantizer leaves them alone at every file type, gives a tied embedding 6 bits unless told otherwise, and converts LFM3's head-gate matrices like any other matrix. A file in the project's format has to be asked for tensor by tensor.
- **Liquid AI has published how it trains LFM models against a quantizer, in code and in a workshop paper.** Its public training code keeps the embedding, the tied output matrix, the normalization layers and the kernels in floating point, even at 4 bits; the paper's own recipe rounds the tied matrix to 6 bits and nothing lower. The paper reports that the gain comes from distillation and not from extra training, and that the trained weights sit further from the rounding grid, not closer.
- **That result lowers idea I27.** The 4-bit-adapted twin is not expected to have more equal magnitudes within a group. The weights-only comparison is still worth its small cost, with the expected answer now "no difference".
- **Idea I34 is not free.** Folding a gain into the matrices it feeds is exact in full precision, and it turns a 16-bit vector the format could store into a factor per column, which the format cannot store. This is a correction to what the first reviewer wrote in the rulings comparison.
- **The nearest published trainer was not carried across model families unchanged.** RaBiT used a hidden-state loss weight of 100 for Llama and 0 for Gemma3, a learning rate per model, and its authors say convergence across Llama, Gemma and Qwen needed tuning to prevent collapse. "Nothing changed but shapes" is a stronger claim than its closest relative has met.
- **A transfer rule, a tensor table, a test and five attribution arms are written out in section 3.**
- **Three of the project's ten benchmarks have an open scorer written by Liquid AI,** with its own prompts and with scores of quantized files, thinking off. Its results table could not be opened in this session.
- **The two one-shot "1-bit" baselines store two to three bits.** By the memory table in ARB-LLM's own paper, its converted weights carry about 2.85 bits each and BiLLM's 2.97, against headlines of 1.06 to 1.13. With the extra structure removed, ARB-LLM's own ablation puts a sign matrix with fitted scales at perplexity 10,942. In the project's format everything rests on training.
- **No source read makes a depthwise kernel, an embedding or a normalization gain binary in a model built like LFM.** Bi-Mamba, DF-SSM, the ternary Mamba paper, Nemotron Bolt and Liquid AI's own training all leave them in 8 to 32 bits. The one case the plan holds at three levels, PrismML's first 27B release, converted the convolution and the normalization weights, and its next release put them back in full precision. The reasons given in vision for binary depthwise filters failing rest on binary activations and batch normalization, which LFM does not have.
- **A correction to batch 7.** Bi-Mamba's released training does not compute its scale from the weights. It learns a scale and an offset per column, from a random start, against a transformer teacher. It is neither a conversion nor a sign-and-scale format.
- **Small models pay for a low-bit embedding.** Quamba2 measures 4 points lost from a 4-bit embedding at 130M and 370M and none at 2.7B and above. The project's 1.7B sits between, and its embedding goes to 1 bit.
- **LFM2's block is Qwen3's block plus the convolution operator.** It has no normalization after a sublayer and no head gates. LFM3 adds both. LFM2 is the closer neighbour of the two targets.
- **Parent scores cannot be taken from Liquid AI's tables.** They come from a harness with few-shot prompts and loose parsing. Its cards do give the project's Qwen parent, thinking off, on six of the ten benchmarks, which is an outside figure to hold the ruler against.
- **Probabilities, before and after:** LFM2-1.2B within five points of the Qwen result 33% to 30%; LFM3-1.7B 35% to 30%; 90% on Qwen3-1.7B 38% to 36%; 99% unchanged at 4%. Section 5.

## 2. Item 1: LFM3 in depth

### 2A. What was read

| Source | Read |
|---|---|
| Model card, LiquidAI/LFM3-1.7B | Whole |
| Release post, liquid.ai/blog/lfm3 | Whole, from its text version |
| `config.json`, `modeling_lfm3.py`, `lfm3_conv.py`, `chat_template.jinja`, the two files under `.eval_results` | Whole |
| Model card, LiquidAI/LFM3-1.7B-Base | Whole |
| Cards of LFM3-1.7B-GGUF and LFM3-1.7B-NVFP4 | Whole |
| Listing of quantized versions of LFM3-1.7B | All six pages, 177 repositories, by name |
| llama.cpp, repository read directly, commit 0e4e925 | `src/models/lfm3.cpp` whole; the text-model part of `conversion/lfm3.py`; in `src/llama-quant.cpp` the function that decides which tensors are converted and the rules that pick a type; in `conversion/base.py` the rule for tensors that must stay in 32 bits |
| Liquid AI's post on its distilled 4-bit builds, liquid.ai/blog/qad | Whole, from its text version; per-task numbers are in images |
| Card of LFM2.5-1.2B-Instruct-GGUF and its `qad/README.md` | Whole |
| "Quantization-Aware Distillation for 4-Bit On-Device Language Models", NeurIPS 2026 workshop | Whole: 13 pages with tables, figures and appendices, from a copy the project owner supplied |
| Liquid AI's training code, `Liquid4All/liquid-finetune`, repository read directly | File list; the quantization-aware training README, profiles, operations and controller; the quality-matrix manifest; the example job |
| Pipette, Liquid AI's benchmarking suite: its release post; `Liquid4All/pipette-scores`, repository read directly | Post whole; file list; the scoring document whole; the dataset document, prompt profiles and model list by search |

### 2B. The graph

From the configuration and the model code. Width 2,048; feed-forward width 7,680; 24 blocks; 16 heads of size 128 with 4 key-value heads; kernel of 7 taps; vocabulary 128,000; embedding and output matrix tied; no biases.

- Block order: convolution at 0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23; global attention at 2, 6, 10, 14, 18, 22; windowed attention (256 tokens) at 4, 8, 12, 16, 20.
- Every block: `o = operator(norm_in(h))`, `o = norm_out(o)`, `h = h + o`; then `f = mlp(norm_in2(h))`, `f = norm_out2(f)`, `h = h + f`. All four normalizations are RMS normalizations with a learned gain per channel.
- Convolution operator: one projection from 2,048 to 6,144, split into three parts B, C and x; `z = B * x` element by element; a causal depthwise convolution of 7 taps over z, one kernel per channel, no bias; the result times C; a 2,048 by 2,048 projection out. There is no activation function in it. It is a product of three linear readings of the input, so it is multilinear, not linear.
- Attention operator: queries 2,048 to 2,048, keys and values 2,048 to 512, RMS normalization with a learned gain on queries and on keys (128 gains each, shared by all heads), rotary positions, attention, then each head's output is multiplied by `sigmoid(G x)` where G is a 16 by 2,048 matrix, then the projection out. Global blocks rotate half of each head; windowed blocks rotate all of it.
- Feed-forward: `W2(silu(W1 x) * (W3 x))`.
- A last normalization, then the tied matrix.

Counts, recomputed from the code and equal to batch 7's table:

| Kind | Count |
|---|---|
| Tied embedding and output matrix, 128,000 by 2,048 | 262,144,000 |
| Feed-forward, three matrices in each of 24 blocks | 1,132,462,080 |
| Attention queries, keys, values, projection out, 11 blocks | 115,343,360 |
| Head-gate matrices, 16 by 2,048, 11 blocks | 360,448 |
| Convolution projections in and out, 13 blocks | 218,103,808 |
| Depthwise kernels, 2,048 by 7, 13 blocks | 186,368 |
| Normalization gains: four vectors of 2,048 in each block, one final vector, 256 query and key gains in each attention block | 201,472 |
| Total | 1,728,801,536 |

The weight file is 3.46 GB in 16 bits, which is this total times two bytes.

### 2C. How it was trained, as published

- 22T tokens before post-training: about 15T of web and synthetic text, 3T of code, mathematics and science at a 4K context, then 3T of curated agent data at 32K, 500B at 128K and 50B at 256K.
- LFM3-1.7B-Base is the model at that point. It is published, with a chat template, and its card recommends it only for heavy fine-tuning. It has no benchmark numbers.
- Post-training, giving LFM3-1.7B: supervised tuning on 1.75T tokens; reinforcement learning on mixed domains with a length penalty; on-policy distillation from six specialist teachers that were themselves trained by reinforcement learning (code, mathematics, tool use, long context, agents, enterprise work); reinforcement learning inside agent harnesses.
- No optimizer, learning rate or precision is published. No technical report exists; the release post links only the LFM2 report.
- One design statement touches quantization: the gate on each attention head "can help suppress activation outliers that hurt quantization". The model code has no comment on it.

### 2D. Template, reasoning and tools

- ChatML roles. Thinking is on by default. With `enable_thinking=False` the template ends the prompt with an empty think block, `<think></think>`, after the assistant header. That is the same mechanism Qwen3 uses, and Liquid AI's own launch command for a server uses the Qwen3 reasoning parser.
- The card warns that with thinking off the behaviour "can be inconsistent, especially for reasoning-heavy tasks".
- Reasoning in earlier turns is dropped unless a flag keeps it.
- Tools are listed as JSON lines inside a `<tools>` block in the system turn. Calls are written in XML: `<tool_call>`, `<function=name>`, `<parameter=name>`. Qwen3 writes JSON inside `<tool_call>`. A BFCL run needs a handler for this format, and a fault in the handler would look like a loss of ability.
- Recommended sampling: temperature 0.1, top-k 50, repetition penalty 1.1 in general; temperature 1.0, top-p 0.95, top-k 20 for mathematics.

### 2E. Published scores against the project's ten benchmarks

- The card's table has 29 rows. Three are in the project's suite: IFEval 96.66, IFBench 73.03, GPQA Diamond 63.37. BFCL is there as version 4 (71.39); the project uses version 3. There is no row for MATH-500, MMLU-Redux, GSM8K, MBPP+, HumanEval+ or MuSR.
- The card says its evaluations use temperature 0.6 and top-p 0.95 in 16 bits on vLLM. The scoring document of Pipette says Liquid AI's internal harness samples at temperature 0.6 with a fresh seed per call and that its model-card MATH-500 figure is a mean of five runs. So Liquid AI's card numbers are sampled means, not greedy single runs, and the mode per row is not stated. The default is thinking on.
- Pipette scores quantized files on IFBench, GPQA Diamond and MATH-500, tags each result with its thinking mode, and publishes its comparisons with thinking off, against a 16-bit reference. Its scorer is open: the IFBench loose checker at a pinned revision, 300 prompts; GPQA Diamond's 198 questions with shuffled options; MATH-500 in two prompt versions, each served five times. Its list of formats includes the 1-bit block type, used there for a 27B model. Its results table is drawn by script and a fetch returns only the headers, so whether it holds LFM3-1.7B with thinking off is still not established. The leaderboard's visible rows are all 4-bit files and show the mean of four evaluations only: LFM3-1.7B 79.5%, LFM2.5-1.2B-Thinking 44.2%, LFM2.5-1.2B-Instruct 38.2%, with no mode shown. Bonsai-27B in the 1-bit block type is in its list of models. Its data export is given against an email address and a license, and holds speed and memory only, no quality scores.
- Pipette's method, from its documentation and its three public repositories, read whole where named in section 8:
  - Each item is drawn five times at temperature 0.6 with no fixed seed, and the score is the mean over all draws. Each evaluation also has a greedy sibling in the catalog.
  - A score belongs to the model, file, runtime and flags together. Multiple choice is answered by one grammar-constrained token on one runtime, free text on another, and by a guided choice or first-token probabilities on a third. Its documentation says not to compare scores across runtimes.
  - Greedy decoding is not repeatable under batching. On a 9B model at temperature 0, 17 of 30 completions matched the one-at-a-time run exactly; the other 13 diverged after a shared prefix. Its documentation says a reference run that has to attribute a small difference should be run one sample at a time.
  - The thinking setting on record is what the job sent to the chat template, not what the model did. Closed reasoning blocks are stripped before scoring. A completion cut off inside a reasoning block usually fails, and a second, strict count marks those wrong outright. Completions that hit the token cap are scored as they stand; on reasoning models that is described as routinely the majority.
  - GPQA Diamond is scored from generated text: options shuffled by a hash of the question, an answer line extracted, and an answer that cannot be parsed counted wrong. A model that returns no valid letter scores zero there, not 25.
  - The MATH-500 figure on Liquid AI's model cards comes from the later of two versions: the problem followed by one instruction, a 32,768-token bound on prompt plus output, and a grader that tries an exact match, then symbolic equivalence, then the last 150 lines of the response. The two versions are stated not to be comparable with each other.
  - IFBench is scored loose and by prompt: a prompt passes when every constraint passes under any of eight transformations. Empty and collapsed outputs are rejected first.
- For the project's ruler: parent and student go through one runtime and one answer path; counted runs are made one sample at a time; a chance value is stated for the scorer in use, since a generative scorer gives zero to output it cannot parse; truncations and mode breaks are counted per item.
- For the project: the parent's ten scores with thinking off have to be measured, none can be taken from the card, and the card's three overlapping rows are not comparable with a greedy thinking-off run.

### 2F. What each runtime does with each kind of tensor

| Tensor kind | Reference converter | Reference quantizer, any file type | Liquid AI's NVFP4 build | Liquid AI's own quantization-aware training |
|---|---|---|---|---|
| Block matrices | As given | Converted | Feed-forward only, with activations, in 4 bits; attention and convolution projections left in 16 bits | Fake-quantized |
| Head-gate matrices | As given | Converted. An exclusion for gates exists in the code for another architecture only | Left in 16 bits | Fake-quantized: the excluded name is `gate`, and LFM3's is `gate_proj` |
| Tied embedding and output matrix | As given | 6 bits (Q6_K), or 8, whatever the file type, unless a type is forced | Left in 16 bits | Left in floating point, and its export command keeps it in 16 bits |
| Depthwise kernels | Forced to 32 bits | Never converted | Left in 16 bits | Not touched: only linear layers are targets |
| Normalization gains | Forced to 32 bits | Never converted | Left in 16 bits | Left in floating point |

- A stock 1-bit conversion of LFM3 with the reference tools would therefore give 1-bit block and gate matrices, a 6-bit embedding, and 32-bit kernels and gains. The project's layout needs a forced type on the embedding.
- The same rules apply to Qwen3-1.7B. If PrismML used the reference converter, its gains are in 32 bits. Its file page shows no tensor table, so this was not verified from the file. At 32 bits the gains raise Qwen3-1.7B from 1.12607 to 1.12722 bits per weight.
- Notes in the quantizer about other architectures with attention gates say their gate and attention-output tensors carry most of the low-bit loss, and one family has its gates raised to 8 bits. None is LFM3. It is a reason to measure the head gates before assuming they convert like other matrices.
- The reference runtime's CPU kernels quantize the activations entering a quantized matrix to 8 bits. Liquid AI's training reproduces that. A score taken "from the packed file" depends on which backend ran it.

### 2G. Low-bit measurements of LFM3 and LFM2

- Liquid AI publishes nothing below 4 bits for LFM3 or LFM2.
- Its 4-bit file for LFM3 is a distilled one. No score is published for it.
- For LFM2.5 it reports a seven-task average, five repeats: the plain 4-bit files keep 86.8% to 92.6% of the 16-bit score across 230M, 350M and 1.2B; the distilled ones 96.5% to 97.7%. Distillation closes 70.6%, 73.4%, 65.5% and 48.4% of the gap at 230M, 350M, 1.2B and 2.6B.
- Among 177 community quantizations of LFM3-1.7B, those below 4 bits are importance-weighted rounding series, mixed-precision MLX series, and one repository with a fidelity table, `ngquocvinh/LFM3-1.7B-GGUF`, which the listing scan did not open and the second reviewer found. Its files were made by rounding with an importance matrix and no training. Against the 16-bit file's perplexity of 14.85 on WikiText-2: 16.12 at Q4_K_M, 17.75 at Q3_K_M, 30.30 at Q2_K, 170.86 at IQ1_M and 35,970 at Q1_0, where the top token agrees with the parent's 0.39% of the time. The Q1_0 file is 431.0 MB. By the quantizer's rules in 2F a stock run gives a 1-bit body, a 6-bit tied matrix and 32-bit small tensors, 422.8 MB before the vocabulary, so that is what this file holds to the accuracy of its size; its tensor listing was not opened. No trained 1-bit or three-level LFM3 was found on the model hub.

### 2H. The 4-bit-adapted weights

- What is published: for each of four LFM2.5 models, a 4-bit file trained by distillation. For LFM2.5-1.2B-Instruct, also the 32-bit weights after that training and before conversion, in a `qad` folder, with a provenance file. Converting them to 16 bits and then to 4 bits with a pinned revision of the reference tools reproduces every tensor byte of the released file.
- The card warns that the published results describe the 4-bit file only, not the 32-bit weights run directly or any other format.
- How it was done, from the workshop paper and from the public training code: a 16-bit teacher; a student whose linear weights pass through an exact copy of the runtime's 4-bit rounding in blocks of 32, with the gradient passed straight through; activations entering each linear layer rounded to 8 bits the same way; embeddings, tied output matrix, normalization layers and kernels untouched; trained weights held in 32 bits because "low learning rates can leave most BF16 weights bit-identical". The paper says the runtime's per-tensor type assignment was matched as well.
- What the paper reports about the result: at 350M, supervised tuning and quantization-aware tuning on the same data, without the teacher, both score below plain rounding, so the gain is not from more training. Distillation raises the weight error on the 4-bit grid by 4.3% to 7.4% and lowers the divergence from the teacher by 40.3% to 53.6%. Exported through a second, similar 4-bit format, the models lose 0.9 to 1.6 points of the gain.
- What the project can learn from the pair with weights only: the distance between original and adapted weights by tensor kind, which shows where the training put its changes; whether the adapted weights' rounding error to the project's format differs from the original's. The paper's finding predicts the second will show little.
- From the paper's full text:
  - Models: LFM2.5-230M, 350M and 1.2B-Instruct. One stage after post-training, of about 22, 10 and 22 billion tokens, on internal instruction-tuning mixtures. AdamW, gradient clipping at 1, linear warmup then cosine decay. Peak learning rate 1e-6 at 230M and 3e-6 at 350M and 1.2B, tuned for each size. One training run per model.
  - Loss: the divergence from the 16-bit teacher's next-token distribution to the student's, at temperature 1, on the positions of assistant responses only. The student starts as the teacher, so the loss is exactly zero until the quantizer is applied.
  - The student's forward pass rounds linear weights to the 4-bit block type, activations to 8 bits, and the tied embedding to 6 bits, as the released file stores them. The public training code leaves the tied embedding in floating point. Neither goes below 6 bits on that matrix.
  - Scores, mean of seven benchmarks, five sampled repeats at temperature 0.6 through the reference runtime, for 230M, 350M and 1.2B: 16-bit 34.62, 37.42, 43.82; plain 4-bit 31.22, 32.46, 40.56; distilled 4-bit 33.42, 36.10, 42.80. The mean's spread over the five repeats is 0.14 to 0.31 points. A single benchmark spreads up to about 2 points (GPQA Diamond at 1.2B). These are repeats of the evaluation, not of the training.
  - Controls at 350M on the same data and settings: supervised tuning then rounding 25.20; quantization-aware tuning on labels 28.30; plain rounding 32.46; distillation 36.10. Divergence from the original teacher on 96 fixed prompts, in the same order: 1.276, 1.050, 0.870, 0.506. It ranks the four as their scores do. The change in weight error does not (-0.01%, +3.31%, none, +4.25%), and neither does each file's divergence from its own unrounded source (0.721, 0.619, 0.870, 0.621), which cannot tell the label-trained model from the distilled one.
  - Across formats at 1.2B: trained against one 4-bit format and exported in a second with the same block size, a model keeps 0.47 of its 2.24 points in one direction and 1.22 of 1.91 in the other. The loss is larger going to the format whose scales are more restricted.
  - GPQA Diamond is the one benchmark distillation did not improve: 1.25 points lower at 230M and 1.12 lower at 1.2B. At 230M the 16-bit model scores 25.05 on it, which is guessing, and the quantized files score from 23.6 to 28.0.
  - The gain is uneven. At 1.2B the seven benchmarks' changes from plain 4-bit to distilled 4-bit add to 15.67 points; AIME25 supplies 6.26 of them and IFBench 4.80, and tool calling moves 0.24. On the three benchmarks shared with the project's ruler the changes are GPQA Diamond -1.12, IFEval +1.72, IFBench +4.80.
  - Not given in the paper: the data mixture, sequence lengths, batch size, warmup length, weight decay, which weights are trained, and any second training run.
  - The paper says the trained weights are held in 16 bits. The public code holds them in 32 bits, with the reason that 16-bit weights do not move at low learning rates, and the released checkpoint is 32-bit. The paper is not a complete description of the released recipe.
  - The lowest file measured is a 3-bit one: 38.79 against 43.82 at 1.2B, and 27.98 against 34.62 at 230M.
  - The parents' training budgets are given as 19, 28 and 28 trillion tokens. The paper cites the finding that loss from rounding grows with training tokens per parameter and places LFM2.5 in that regime.
- For the project:
  - Divergence from the parent on fixed prompts is the one cheap signal here that tracks the benchmark result across recipes: four recipes, one model size. It is a candidate for what development reads on Qwen (row C142), with prompts drawn from outside the ten benchmarks. Weight error is not such a signal, so a weights-only reading can describe a parent and cannot rank recipes.
  - A model trained against one layout loses most of its gain when stored in another. The strict track and the named track each need their own training; a file trained for one and repacked as the other is a result for neither.
  - Liquid AI changed a learning rate between sizes of one family. A formula carried number for number may fail to hold even within LFM.
  - Training on labels alone did harm. That supports distillation from each model's own parent as the loss.
  - The spread between training runs on an LFM model is still unpublished.

### 2I. Unknown, and the cheapest way to learn each

| Unknown | Cheapest way |
|---|---|
| The parent's ten scores with thinking off, greedy | Measure them; they are the denominator of every LFM3 claim |
| How far thinking-off scores of the parent move between runs | Repeat the parent's run with three seeds on the sampled benchmarks |
| LFM3 scores of quantized files with thinking off on three benchmarks | Pipette's results table, read in a browser. A fetch returns its headers only |
| Whether the head gates are sensitive at 1 bit | A weights-and-activations measurement: convert only the 11 gate matrices and compare outputs |
| The spread of tap shapes across channels in the kernels | A count from the weights, inside row C63 |
| Whether LFM3-1.7B-Base converts better than LFM3-1.7B | The attribution arm in section 3E |

## 3. Item 2: the transfer rule in writing

### 3A. What the released files and tools establish

- The reference tools define the 1-bit block type for tensors of two or more dimensions whose first dimension is a multiple of the block. Everything else is carried in 32 bits. So "the format" as PrismML's file can carry it is: matrices binary, everything else 32-bit floating point.
- Boole's files, read in batch 8, keep gains in 16 bits and add a second set of scales for the tied matrix.
- Liquid AI's own low-bit work on this family has never converted the embedding, the kernels or the gains at any bit width.
- So the project's strict target, every learned weight binary, goes beyond every released file and every published LFM result. That is a statement of where the evidence stops, not an argument against the target.

### 3B. Every kind of tensor, and how the format applies

"Row" below means a row of the matrix as the model code stores it: one output unit, its weights running along the input dimension. Groups of 128 run along that dimension.

| Kind | In Qwen3 | LFM2-1.2B | LFM3-1.7B | How the format applies | Where a group of 128 is not defined, and what replaces it |
|---|---|---|---|---|---|
| Block matrices | Yes | Yes | Yes | Unchanged. Every input width is a multiple of 128 | Defined everywhere |
| Tied matrix | Yes | Yes | Yes | One sign per entry, groups of 128 along the hidden dimension, 16 groups per token, one set of scales | Defined |
| Head-gate matrix, 16 by 2,048 | No | No | Yes | Unchanged: 16 rows of 16 groups | Defined |
| Depthwise kernel, 2,048 by 3 or by 7 | No | Yes | Yes | A row has 3 or 7 weights | Not defined. Three choices: leave it in 16 or 32 bits; signs only, with the channel's size moved into a row of the projection in (exact, 3E below), which leaves 4 shapes a channel in LFM2 and 64 in LFM3; or groups of 128 across channels, tap by tap, after the same move and a reordering of channels |
| Gain before a sublayer | Yes | Yes | Yes | Can be multiplied into the columns of the matrices it feeds, exactly, leaving a gain of one. Not free: see 3F | Defined as a vector of 16 groups if kept |
| Gain after a sublayer | No | No | Yes, 48 vectors | Cannot be moved: it sits after a normalization and before the residual sum | 16 groups if made binary |
| Final gain | Yes | Yes | Yes | Feeds the tied matrix. Moving it into that matrix changes the embedding as well, so it cannot be moved | 16 groups if made binary |
| Query and key gains | Yes | Yes | Yes | 128 or 64 a vector. Cannot be moved | One group in Qwen3 and LFM3: a single magnitude for every dimension. In LFM2 a vector is 64 long, half a group, and the layout has to be chosen: pair query with key in one group, 1.125 bits; pad each to 128, 2.25 bits; or a short group of 64 signs and a scale, 1.25 bits. The sizes below count the pairing |

Bits per weight and file size for each layout, from `scripts/b10_bits.py`:

| Layout | Qwen3-1.7B | LFM2-1.2B | LFM3-1.7B |
|---|---|---|---|
| Reference tools: matrices binary, gains and kernels in 32 bits | 1.12722, 242.43 MB | 1.12842, 165.08 MB | 1.13193, 244.61 MB |
| Named track: gains and kernels in 16 bits | 1.12607, 242.19 MB | 1.12665, 164.82 MB | 1.12834, 243.83 MB |
| The same with gains before sublayers folded away | 1.125005, 241.96 MB | 1.12575, 164.69 MB | 1.12743, 243.64 MB |
| Strict: everything in groups of 128 | 1.12500, 241.96 MB | 1.12500, 164.58 MB | 1.12500, 243.11 MB |

Gains that cannot be folded: 9,216 in Qwen3-1.7B, 2,816 in LFM2-1.2B, 103,168 in LFM3-1.7B. The whole difference between the named track and the strict target is 0.23 MB on Qwen3, 0.24 MB on LFM2-1.2B and 0.72 MB on LFM3-1.7B.

### 3C. The rule

A third party should be able to take the frozen Qwen recipe and this rule and produce the LFM run without asking anyone a question.

Carried over as written, number for number:

- The format: one sign per weight, one 16-bit scale per group of 128 along a row, one sign set and one scale set for the tied matrix.
- The order of stages and what each stage trains.
- The loss, term by term, with its weights. A term defined "per block" is applied to every block of the target.
- The optimizer and every setting of it: peak learning rate, schedule shape, warm-up as a share of steps, betas, weight decay, clipping, precision of the trained variables.
- Batch size and sequence length in tokens, and the number of tokens seen in each stage.
- The data: the same sources in the same mixture, drawn by the same procedure with the same seeds.
- The definition of the teacher: the full-precision parent of the target, in 16 bits, thinking off, giving its distribution over the whole vocabulary.
- The stopping rule and the rule for which checkpoint is scored.
- The number of seeds, and that every seed is reported.
- The evaluation: the ten benchmarks, their settings, the scoring code and its revision, the runtime and backend that run the packed file.

Recomputed from the target, by a procedure written before the run:

- Shapes: number of blocks, widths, heads, vocabulary, kernel length, group counts.
- Every statistic the recipe takes from the parent: starting scales, importance weights, any per-layer quantity defined as a function of the parent's weights or activations.
- The teacher's outputs.
- The tokenizer and the chat template of the target, used to render the same data; the thinking-off form of the target's template.
- The tool-call format in the function-calling benchmark.
- The parent's own ten scores under the frozen evaluation, which are the denominator.
- The treatment of each tensor kind, read from a table fixed before the run. Section 3B is a draft of that table. A kind that is not in the table stops the run.

Not to be touched:

- Any setting, after an LFM score has been seen.
- Any exception for a layer or a tensor chosen from LFM results.
- The checkpoint, chosen by benchmark score.
- The number of attempts. A rerun is a new run and is reported beside the first.

Three things look like shapes and are not, and each needs its line in the recipe before the Qwen run is frozen:

- The treatment of a tensor kind Qwen does not have. The Qwen run cannot fix it by example, so the recipe has to state it as a rule ("every tensor of fewer than two dimensions is treated as ...").
- The hidden-state term of a loss, if the recipe has one. RaBiT, the nearest published trainer, set its weight to 100 for Llama and 0 for Gemma3. A recipe with such a term has to say how its weight is set from the target, or carry one number and accept the result.
- Sequence length against context. LFM3's 256K context and Qwen3's 32K do not change a recipe that trains at a fixed length, and the recipe should say that the length is fixed.

### 3D. The test of a transfer

- Quantity: retention on the ten benchmarks, with chance removed. For each benchmark take the converted score minus the chance score and the parent's score minus the chance score; sum each over the ten; divide. Chance is zero for generated answers and the reciprocal of the number of options for multiple choice.
- Reason for removing chance: batch 7 found LFM2-1.2B at chance on two of the ten. A converted model that is also at chance there keeps "100%" of those two, and the plain ratio of averages rises for a reason that has nothing to do with the formula.
- A benchmark on which the parent is within three standard errors of chance is reported and left out of both sums. Which benchmarks those are is decided from the parent's run, before any converted model is scored.
- Reference: the retention the frozen recipe reached on Qwen3-1.7B, computed the same way, mean over its seeds.
- Rule: the transfer holds if the LFM mean is no more than five points below the Qwen mean. Above it by any amount also holds. Five points is the project's unit of progress and the margin batch 7 chose.
- Runs: the same number of seeds on both sides, three at least, every seed reported.
- What it would wrongly pass: a recipe whose Qwen result is itself low, since being near a low figure is easy; and a true shortfall of up to five points plus the noise of the two means.
- What it would wrongly fail: a recipe that works, on a parent whose thinking-off behaviour is itself unstable, as LFM3's card warns; and a fault in the tool-call handler that costs the converted model more than the parent.
- Both failures of the second kind are measured by the parent's own repeat runs in section 2I, which is a reason to do those first.

### 3E. If a transfer falls short: five arms

Each arm changes one thing against the failed run. Each has a price in what may then be claimed.

| Arm | Change | What a recovery would show | Price |
|---|---|---|---|
| 1 | Kernels, gains after sublayers and head gates left in 16 bits | The shortfall is in the tensor kinds Qwen lacks | The claim becomes the named track for LFM, with the kinds listed |
| 2 | Tied matrix left in 16 bits | The shortfall is in the embedding and output matrix (11.5% of LFM2-1.2B's weights, 15.2% of LFM3-1.7B's, 18.1% of Qwen3-1.7B's) | The claim loses the tied matrix, which no published trainer of this family has converted |
| 3 | LFM3-1.7B-Base as the parent in place of LFM3-1.7B, each against itself | The shortfall is in what reinforcement learning and specialist distillation added | A claim about the base model only; its ten scores are low and partly at chance, so the test of 3D may leave little to compare |
| 4 | The same recipe on text rendered without the target's chat template, or with the Qwen data replaced by text closer to the target's training | The shortfall is in the data | The recipe's data line becomes a function of the target |
| 5 | One alternative setting fixed in advance: the learning rate halved and doubled | The shortfall is in a setting | The claim becomes "one setting re-derived", and the rule for deriving it has to be written |

Arms 1 and 2 need no new idea and should be planned with the transfer run. Batch 7's seven arms contain these and two more, the design generation and post-training, which arm 3 covers for LFM3.

### 3F. The seven ideas

**a. Closing by a fixed group norm (I24), on LFM tensors.** It applies to any group that has a scale. For block matrices, the tied matrix and the head gates it is unchanged. For gains in groups of 128 it is unchanged. For kernels it depends on the grouping chosen in 3B and works with either. One thing is different in LFM3: the three matrices that end a sublayer are followed by a normalization, so multiplying all their scales by one number changes nothing. The radius of the closing is then free up to that number, which removes one way the closing could go wrong. Verdict: carries over; no change to the idea.

**b. Factors and signs moved inside the convolution block (I25).** For channel c the block computes `C_c * sum_k w_c[k] * (B_c x_c)[t-k]`, then the projection out reads channel c through its column c. Multiply the three rows of the projection in that produce B_c, C_c and x_c by a, g and b, the kernel by k, and column c of the projection out by e. The output is unchanged when `a * b * g * k * e = 1`. Signs are included. Checked numerically: largest difference 9e-13. Two corrections to how the idea was written: the block is multilinear, not free of nonlinearity; and the factor does not have to go into the 16-bit kernel, because a row factor on the projection in is already in the format. So a kernel with signs only needs no scale of its own. A further freedom of the same kind: the 2,048 channels inside the block are not the residual stream, so they can be reordered, exactly, block by block. Reordering regroups the columns of the projection out and the channels of the kernel. The same holds for the hidden units of every feed-forward block, which regroups the columns of its last matrix. Verdict: exact; worth what free column factors were measured to be worth in the plan, 0.2% to 2.9% of weight error; the reordering is unmeasured.

**c. Gains after sublayers in the scale-only stage (I26).** Confirmed from the code: 48 vectors of 2,048, each after a normalization. Two consequences on paper. The overall size of the matrix that ends a sublayer carries no information, exactly up to the small constant inside the normalization (checked: 1.9e-5 with a constant of 1e-5). And in the named track each sublayer keeps a 16-bit factor per channel after its converted matrices, which Qwen and LFM2 do not have. In the strict target that factor is binary and the advantage goes. Verdict: holds for the named track; it predicts LFM3 easier than LFM2 there and not in the strict target.

**d. The 4-bit-adapted twin as a control (I27).** The workshop paper says the adapted weights are further from their own grid, by 4.3% to 7.4%, while the model is closer to its teacher. Adaptation moved the function, not the weights toward round values. Verdict: the idea's premise is weakened; the odds that the adapted twin has lower group error fall from 45% to 20%. The comparison still costs only weights, and the map of where the adapted weights moved, by tensor kind, is worth more than the single error figure.

**e. Kernel groups across channels, tap by tap (I28).** The move of each channel's size into the projection in is exact (b above). The reordering of channels is exact and internal to the block. After both, tap k of 128 neighbouring channels shares one scale, so the profile of a kernel across its taps is kept to the extent that neighbouring channels have the same profile. Cost 1.125 bits per kernel weight. One reordering has to serve the kernel and the columns of the projection out at once. Verdict: exact where claimed; needed only for the strict target; its worth depends on the spread of tap shapes, which is a count from the weights.

**f. Everything binary (I29).** By tensor kind: head gates fit unchanged. Gains before sublayers can be folded, with the cost in g. Kernels by e, or signs only with 64 shapes a channel in LFM3 and 4 in LFM2. Gains after sublayers, the final gain and the query and key gains become one magnitude per group. For the query and key gains that is one magnitude for all dimensions of a head, a single temperature. The whole saving is 0.72 MB of 243 on LFM3. Verdict: the value is in the sentence "every learned weight is one bit", and the risk sits in 103,168 gains on LFM3 against 9,216 on Qwen3. The Qwen run cannot show what LFM3's gains after sublayers are worth, because Qwen has none. A gains-only measurement on LFM3 is needed before the strict target is claimed for it.

**g. Folding gains away before conversion (I34).** Exact for a gain that feeds only linear maps, which is every gain before a sublayer: checked, 1.8e-15. It covers 114,688 of Qwen3's 123,904 gains, 65,536 of LFM2-1.2B's 68,352 and 98,304 of LFM3-1.7B's 201,472. What was missed when the idea was written: the fold turns the gain into a factor on each column of the matrices it feeds. The format stores one scale per 128 columns of a row and no factor per column. So a gain that the named track stores exactly becomes structure the binary matrix has to give up. The size of that loss is the measured worth of column factors. Verdict: the algebra is right and the saving is real, and it is "binary gains before sublayers" by another name, not a free step. It belongs with idea f, as one of its parts.

### 3G. One recipe across families, as published

| Source | Recipe | Families | Spread |
|---|---|---|---|
| RaBiT, 2 bits, trained | Hidden-state weight and learning rate set per family | Llama2, Llama3, Gemma3, Qwen3 | Gemma3-1B 92% and Qwen3-1.7B to 8B 94% to 95% of an easy-task average, with per-family settings |
| AF1, 1 bit on average, no training | One procedure | Qwen3-8B 79%, Llama-3-8B 63% | 16 points |
| Liquid AI's distilled 4-bit builds | One procedure, one family | LFM2.5 at 230M, 350M, 1.2B, 2.6B | 96.5% to 97.7%, about one point |
| TWLA, three levels, no training | One procedure | Llama2-7B, Llama3-8B, Qwen3-8B | Read in batch 9; calibration text alone moves the result by two to three points |

No source read applies one trained low-bit recipe to two model families with every setting held and reports both. The nearest, RaBiT, changed settings.

## 4. Item 3: sources read in part in batches 6 and 7

### 4A. What was read in this batch, and where every other source of the item stands

Read here, each to its end unless a limit is stated:

| Source | Read |
|---|---|
| Code of the mirror-descent-view paper, `kartikgupta-at-anu/md-bnn` | The update rule, the schedule and the training script |
| Code of the greedy rounding paper, `elybrand/quantized_neural_networks` | README and `scripts/quantized_network.py` whole |
| MagR code, `AozhongZhang/MagR` | The preprocessing routine and its groupwise variant |
| CEWT, arXiv 2609.32659, and its code `1733116199/cewt` | The paper's remaining appendices A to M; the projection and optimizer code; `base_linear.py` in outline only |
| Survey of transforms for quantization, arXiv 2608.25188 | Whole, 505 thousand characters in six parts |
| BiLLM, arXiv 2402.04291 | Whole |
| ARB-LLM, arXiv 2410.03129, and its code `ZHITENGLI/ARB-LLM` | Paper whole; `binary_arb.py`, `bigptq_arb.py`, the three files under `utils`, `modelutils.py` whole; `run_arb.py` by its settings and layer loop. Its supplementary file is a separate download and was not read |
| INQ code, `AojunZhou/Incremental-Network-Quantization` | README, `run.py`, the quantization block of `blob.cpp`, `power2.cpp`, the masked update in the solver |
| Low-bit quantization and training tokens, arXiv 2411.17691 | Whole |
| Scaling laws for precision, arXiv 2411.04330 | Whole, 290 thousand characters in three parts, appendices A to O |
| Training dynamics and rounding damage, arXiv 2510.06213 | Whole, appendices A to H |
| Ternary Mamba, arXiv 2606.18114 | Whole, appendix A.1 to A.7 |
| Nemotron 3.5 Bolt, arXiv 2610.33039 | Main text whole. Its appendix is not on the page |
| Bi-Mamba code, `Tangshengku/Bi-Mamba` | `qat/learnable_binarizer.py`, `qat/replace_module.py`, `qat/base_binarizer.py`, `mamba_ssm/modules/bimamba2.py`, `train_bimamba.py`, `sbatch.sh`, README, whole |
| DF-SSM code, `cs-cmyk/df-ssm` | README and `training/df_ssm_mamba2_distill_dfw.py` whole |
| BD-Net, binary depthwise convolution in vision, arXiv 2511.17633 | Whole, appendices A to D |
| Binarizing MobileNet, arXiv 2005.06305 | Whole |
| Quamba2, arXiv 2503.22879 | Whole |
| LFM2 technical report, arXiv 2511.23404 | The parts batch 7 left: tables 6 to 16 and appendices A to D |
| transformers `modeling_lfm2.py` and `configuration_lfm2.py` | Whole |
| mlx-lm `mlx_lm/models/lfm2/model.py` and `layers.py` | Whole |
| The two LFM2 chat templates, as text, from `Liquid4All/liquid-finetune` | Whole |
| Cards of LFM2.5-1.2B-Instruct, LFM2.5-1.2B-Thinking, LFM2.5-1.2B-Base | Whole |
| `tokenizer_config.json` of LFM2-1.2B | Whole |

Read in full in earlier batches, and relied on here as read then: the three mirror-descent papers, the random-features and the two linear-classification papers, the democratic-representations paper, the three greedy-rounding theory papers, Qronos and its analysis, MagR's paper, Noda's compensation paper, the double binary factorization paper, OneBit with its code, INQ's paper, the random-partition and exact-backpropagation papers, the structure-of-damage paper, the feature-damage paper, "Linger and Lose", the memorization paper, the binary perceptron note, the patent application.

Still not read in full: see section 9.

### 4B. Group A: does a mirror-descent argument say where training ends

What the code adds to batch 6:

- The released tanh method starts from random weights, stores no scale, raises its sharpness by 1% to 2% at each annealing step, and ends by taking the sign. Its stable form is ordinary straight-through training with a sharpened squashing function. Nothing in the code is specific to a pretrained start.
- The projection code of CEWT is the nearest working relative of "keep the latent weights on a chosen shape while training": after each step it maps the latent weights back to a fixed distribution. Its paper's last appendices give the 1-bit numbers: on a 95M model with weights and activations at 1 bit, perplexity 52.85 with plain straight-through training, 50.61 with injected noise, 48.02 with the projection; full precision 23.95. With weights only at 1 bit on a vision model, 56.41 to 58.88. All of it is training from scratch. The paper states the gain is negligible for short training and for models much larger than their data.

Answer for a 1.7B decoder in the project's format:

- Proved: for linear models, where training under a potential ends, from a zero start. For networks, only locally and with no constants. Nothing for a two-value target on a network.
- Measured: the tanh form reaches 1 bit on small vision networks; a projection that fixes the latent distribution lowers perplexity by 9% to 10% at 1 bit from scratch, against plain straight-through training.
- Inferred: no argument in this group says a pretrained model moves toward equal magnitudes under any potential. The useful residue is practical: a rule that holds the latent weights' distribution fixed during sign training is a tested way to reduce oscillation at the boundary. Idea I24, the fixed group norm, is a rule of that kind, and CEWT is evidence for the kind, not for I24 itself.
- The patent application's description was read again from a copy the project owner supplied: Justia's rendering, through the opening of its kurtosis section, without the claims. One thing is new. As printed there, the inverse map of the rigid cage's gradient has two slips against the algebra. It asks for the largest count `k` of top entries that satisfies its inequality, where the algebra needs the smallest; and it returns the other entries unchanged, where the algebra divides them by the ridge constant. On 2,000 made-up vectors the printed rule never returns a valid gradient and the corrected rule always does (`scripts/cage_inverse_check.py`). Google Patents' rendering of the same publication, read afterwards in full, carries both slips in the same words, so they are not Justia's. The typeset pages have not been seen. The same reading found a third inconsistency: the kurtosis term is weighted by one constant in equation 30 and by a differently named one in the sentence after equation 31. The project's toy test of the cage used the derived map, so no result changes.
- From the second reviewer's reading of the same copy, each checked (`batch-10-followup-comparison.md`, section 3): at the zero vector the cage's gradient may be any vector whose absolute values add to one or less, where the text says exactly one, so dual values adding to one or less map to all-zero weights; a group that is already a scale times signs is reproduced exactly by starting each dual entry at its sign times the ridge constant times the scale plus one over the group size; and the application's joint potential has a flat step, an interval of dual values that all land on one exact magnitude set by its scaling constant. Off that step on the low side, with the small power close to one, a weight is near zero, so the map moves between three states: plus the magnitude, zero, minus the magnitude (`scripts/plateau_check.py`).

### 4C. Group B: rounding one weight at a time, and equal-magnitude representations

What the code and the survey add:

- The greedy code rounds each weight of a neuron in turn against a running error on real inputs, and takes its inputs from the already-rounded network, so each layer absorbs the error of the layers before it. Its alphabet has one radius per layer, a multiple of the median magnitude, found by search. It handles depthwise filters, each channel as its own neuron. Its experiments stop at VGG16 with only the dense layers rounded. One branch, for 1 by 1 filters, refers to names that do not exist and would fail.
- MagR's code has a groupwise form: it lowers the largest magnitude in each group of 128 along the input dimension while holding the layer's output on calibration inputs, 200 iterations at strength 1e-4. That is the project's grouping, and among the routines read it is the one that reshapes a pretrained matrix toward flat groups without changing what the layer computes on data.
- The survey proves, for a shared scale set from a group's largest value at 4 bits and above, that error is lowest when the values in each group are flat, and that this is the opposite of what classical transform coding wants. Its formulas use `2^(b-1) - 1` levels, which is zero at 1 bit; it has no result at 1 bit, at three levels, or for trained conversions, and says retraining is out of its scope. The flatness condition itself does carry: with one sign and the mean magnitude per group, the error of a group is the sum of squared differences between each magnitude and the mean, which is zero exactly when the group is flat.
- The survey's list of what can be folded into stored weights at no run-time cost: a normalization gain into the matrix that reads it; a rotation of the whole residual stream, only if the normalizations have no per-channel gain, and with small transforms still left to run before the down-projection and on queries and keys; a permutation, whose "only lever is the grouping". Non-orthogonal maps on the residual stream do not commute with the normalization.

Answer:

- Proved: bounds for greedy rounding on alphabets that contain zero or are unbounded, needing many more weights per row than input directions in use. Flat groups minimize shared-scale error. Neither covers two levels.
- Measured: MagR about halves column maxima and moves full-precision perplexity from 5.47 to 5.52 on a 7B model; at 2 bits its result is 9.94. A rotation supplies nearly all of the 2-bit gain in the incoherence methods the survey tabulates (123.9 to 6.33 perplexity on a 70B model).
- Inferred, for the project: three exact moves are open inside the format, and one is closed.
  - Open: reorder the hidden units of each feed-forward block and the internal channels of each convolution block so that the columns sharing a scale are alike. Quamba2 does exactly this reordering on a Mamba block, for 8-bit activations, and rewrites the projections, the kernel and the gain to match. This is idea I1 extended to the convolution block.
  - Open: move per-unit factors between the two sides of a feed-forward block or a convolution block (idea I25).
  - Open: reshape groups toward flatness on data before conversion, as MagR's groupwise routine does. This is a candidate for the "migrate before converting" step.
  - Closed: rotating the residual stream, while per-channel gains are kept and no transform may run at inference.

### 4D. Group C: published low-bit conversions and trainings at small sizes

The two one-shot methods read here for the first time, and what their fine print says:

| | BiLLM | ARB-LLM |
|---|---|---|
| Training | None | None |
| Smallest model | OPT-1.3B | OPT-1.3B |
| Perplexity there, against full precision 14.62 | 69.97 | 45.40 with calibration; 26.63 with row and column scales |
| OPT-2.7B, against 12.47 | 49.55 | 34.37; 19.84 |
| Headline bits | 1.07 to 1.13 | 1.06 to 1.11 |
| What the headline counts | Sign planes only | Sign planes only |
| What is also stored | A second sign plane on chosen columns; one membership bit per weight for the split into dense and sparse magnitudes; a scale per row for each part | The same, with up to four parts per block of 128 columns, a mean per part, and in one variant a scale per column |
| Stored size, from ARB-LLM's memory table | Llama-7B: 2.93 GB of 13.48 | Llama-7B, row-and-column variant: 2.83 GB of 13.48 |
| Embedding and output matrix | Not converted, not counted | Not converted, not counted |

- From ARB-LLM's memory table: 2.83 GB of 13.48 GB is 3.36 bits per parameter on average. With the embedding and output matrix, 3.89% of the parameters, at 16 bits, the converted weights carry about 2.85 bits each, or 1.93 with the membership bits compressed. For BiLLM the same arithmetic gives 2.97 and 2.06. These methods are 2-bit methods by storage. The arithmetic is the first reviewer's; the gigabytes are the paper's.
- ARB-LLM's ablation prices the plain format. On Llama-7B, signs with row and column scales and error compensation, but without the membership bits and the second plane, give perplexity 10,942. With them, 14.03. A sign and a scale alone, however well the scale is fitted, is not usable without training.
- The row scale in both methods is one scale per row per block of 128 columns, which is the project's group. BiLLM's block-size table shows what that choice costs before training: Llama-7B perplexity 74.14, 48.91, 35.04, 27.23 and 17.56 at blocks of 512, 256, 128, 64 and 32.
- After training the group size stops mattering: the ternary Mamba paper finds 64, 128 and 256 indistinguishable (21.64, 21.66, 21.68).
- Column scales are worth a great deal with no training: 22.67 to 14.03 on Llama-7B. The format has no place for a column scale. A 16-bit gain before a sublayer is one, shared by the matrices that read it. This supports the correction to idea I34 in section 3F and gives the named track a reason to train those gains with the scales.
- "First to surpass full-precision models of the same size" in ARB-LLM compares a binarized 13B model with a full-precision 2.7B model of equal memory. It is not a retention claim.
- Refitting scales converges fast: 15.23, 14.34 and 14.03 after 1, 3 and 15 passes.
- INQ's released code freezes the largest 30% of each layer at their rounded values, retrains the rest, and repeats at 60%, 80% and 100%, rebuilding the program each time. The freeze is applied in the accelerator branch of the update only.

Answer:

- Measured: with no training, the best published result near 1 bit at this size is perplexity 26.63 against 14.62 on a 1.3B model, at about 2 to 3 stored bits. With training from a pretrained start, OneBit and its successors reach about 1.4 to 1.5 times the parent's perplexity at 7B (7.88 to 8.36 against 5.47, batch 9) in one sign matrix with scale vectors on both sides. PrismML's 1-bit 1.7B model keeps 74.5% of its parent on the ten benchmarks.
- Inferred: every one-shot result at this size buys its quality with stored structure the project's format forbids. For the project's format the question is entirely one of training, which is what the plan already assumes. No source in this group contradicts that, and BiLLM and ARB-LLM should not be used as 1-bit baselines without their true storage beside them.

### 4E. Group D: where low-bit damage sits and what predicts it

What the full readings add:

- The token-count law (damage grows as tokens to the power 0.53, falls with size to the power 0.23, and with bits to the power 5.5) is fitted on one model family up to 206 billion tokens, with no training after rounding, and its authors limit it to single-stage pretraining.
- The training-dynamics paper disputes its reading: across six open training runs, rounding damage jumps when the learning rate decays and is otherwise nearly independent of tokens seen. Higher peak rates, weight decay, checkpoint averaging and merged models lower it. In the one run with public stages, a mid-training stage raised the damage and the tuning stages after it lowered it. Its mechanism, sharper minima after decay, is offered as a hypothesis.
- The precision law fits training from scratch at 3 to 16 bits as a loss of effective parameters: a model trained at P bits behaves like one with a share `1 - exp(-P / 2.67)` of its parameters. It has no data below 3 bits and reports loss only. Extended to 1.125 bits by the first reviewer, the share is 0.34, so a 1.72B model would behave like one of about 0.59B. In Liquid AI's table, Qwen3-0.6B scores 78% of Qwen3-1.7B on the five benchmarks that table shares with the project's ten. PrismML's 1-bit 1.7B keeps 74.5%. At three levels the same arithmetic gives about 0.77B, and PrismML's three-level 1.7B keeps 87.8%, more than Qwen3-0.6B's 78% suggests for a model of about that size. So the extension is close at the one measured 1-bit point and too low at three levels. It is a law for training from scratch, used here on a distilled conversion, and is a rough prior only.
- The ternary Mamba paper measures the same thing two ways in one model: weight error is the same in every layer (0.57, varying by under half a percent) while activation error falls from 1.68 in early layers to 0.79 in late ones. Weight error does not locate damage, as batch 6 found from other sources.
- The same paper's control: a 16-bit student trained with the same distillation scores better than the untouched parent (perplexity 9.52 against 11.69 on its second test set). Distillation on a chosen text moves the parent itself, so a converted model can look closer to its parent than it is. The ruler's four references already include a parent given the same training; this is a measured reason for that reference.
- Quamba2 measures what the embedding costs at small sizes, at 4 bits: with the blocks already at 4 bits, adding a 4-bit embedding costs 4.2 points at 130M and 4.3 at 370M and nothing at 2.7B and 8B; a 4-bit output matrix costs nothing at any size. The project's 1.7B sits between the sizes that lose and the sizes that do not, and its embedding goes to 1 bit, not 4.
- Nemotron Bolt, the one hybrid below 4 bits among the sources read, gives its tensor kinds different widths with no measurement shown: expert feed-forward weights 2.06 bits, recurrent projections 4.5, embedding and output matrix 8.5, convolution 32. Its largest relative loss is on a knowledge-recall benchmark (21.80 to 16.90). Summed over 13 of its 14 benchmark rows it keeps 95%; the row left out is a rate that rose.

Answer:

- Measured: damage is spread over layers and additive in pairs at 4 bits; nothing that reads only the weights locates it; knowledge and weak features go first; small models pay for a low-bit embedding where large ones do not.
- Disputed between sources: whether a parent trained on more tokens is harder to convert. One paper fits a law, a later one attributes the effect to the learning-rate schedule.
- Inferred, for the project: neither law should rank the project's parents. By the token law LFM2-1.2B would round 0.58 times as badly as Qwen3-1.7B, LFM2.5-1.2B 0.96 times and LFM3-1.7B 0.77 times; by the dynamics paper what matters is how each parent's training ended, which is not published for any of them. A direct reading costs only weights and forward passes: the same converter at 3 and 4 bits on each parent.

### 4F. Group E: LFM2 and its relatives

- The block, from the transformers file read whole and confirmed in mlx-lm: `h = x + op(norm(x))`, then `out = h + mlp(norm(h))`. There is no normalization after a sublayer and no gate on attention heads. Queries and keys pass through normalizations with learned gains. One final normalization. LFM2's block is Qwen3's block with the convolution operator in 10 of 16 places. LFM3 adds the normalizations after sublayers, the head gates, sliding-window attention and a 7-tap kernel.
- Consequence for section 3F: the point that a matrix ending a sublayer has a free overall size holds for LFM3 only. In LFM2 that size matters, as in Qwen3.
- The report's language table, in Liquid AI's own harness, LFM2-1.2B against Qwen3-1.7B: GPQA 31.47 and 27.72; IFEval 74.89 and 73.98; IFBench 20.70 and 21.27; GSM8K 58.30 and 51.40; MATH-500 42.40 and 70.00; MMLU 55.23 and 59.11. Trained on 11 trillion tokens against 36 trillion.
- The harness behind those numbers, from the report's appendix: "more permissive answer parsing than open-source harnesses"; GPQA run ten times with the options reordered; IFEval as the mean of four measures; GSM8K with five examples in the prompt and the loose score reported; MATH-500 with four fixed examples. The project's zero-shot, strict ruler will read these parents lower. Parent scores have to be measured on the project's ruler and never taken from these tables.
- The LFM2.5 cards add Liquid AI's measurements of the project's Qwen parent with thinking off, on six of the ten benchmarks: GPQA Diamond 34.85, IFEval 73.68, IFBench 21.33, GSM8K 33.66, MATH-500 70.40, BFCL v3 46.30 (its own handler). LFM2.5-1.2B-Instruct on the same six: 38.89, 86.23, 47.33, 64.52, 63.20, 49.12. Protocol stated on the card: greedy for instruct models, the mean of five runs at temperature 0.6 for thinking models.
- GPQA Diamond has 198 questions. A score of 31.47 is 6.5 points above the 25% of guessing, and one standard error is 3.3 points. LFM2-1.2B on GPQA is inside the three-standard-error band of section 3D and would be left out of the test, unless the ten-reordering protocol is adopted to shrink the error.
- Templates, read as text. LFM2: tools are appended to the system turn between `<|tool_list_start|>` and `<|tool_list_end|>`, tool results are wrapped in `<|tool_response_start|>` and `<|tool_response_end|>`. LFM2.5: the system turn gets a line with today's date and the list of tools as JSON; the assistant's calls are written in Python call syntax between `<|tool_call_start|>` and `<|tool_call_end|>`; reasoning is kept only on the last assistant turn; the template has no switch for thinking. LFM3 uses XML. So the three generations need three handlers for the tool benchmark, and the date line makes an LFM2.5 tool prompt depend on the day it is run. The ruler should pin the date.
- Tokenizer configuration of LFM2-1.2B: beginning-of-text token added by default; the end-of-turn token is the end-of-sequence token; ids 16 to 500 are reserved and unused, 485 rows of the tied matrix that no text ever selects as input.
- The report's deployment section says its recipes were tuned for 8-bit activations with 4-bit weights in one runtime and the 4-bit block format in another. It has no table of accuracy under quantization.
- An official 4-bit MLX build of LFM3 exists with its own model type, in groups of 64 with a scale and an offset, so MLX support exists. A code search of mlx-lm did not locate the file that implements it.

### 4G. Group F: binary and three-level state-space and convolution models

What the code and the full readings change:

| Work | What batch 7 recorded | What the full reading shows |
|---|---|---|
| Bi-Mamba | Scale computed from the weights, held out of the gradient | The released training path uses a different class: a learned scale and a learned offset per column, both trained, started from the mean and the mean absolute deviation. The gradient passes through the sign unclipped. The model is built from its configuration with no pretrained weights loaded. The teacher is a 7B transformer and the default loss is cross-entropy against the teacher's distribution alone |
| Bi-Mamba | Both projections binary | Confirmed. The depthwise convolution with its bias, the recurrence parameters, the normalization gain, the embedding and the output matrix all stay in full precision |
| DF-SSM | Stored 1-bit with an 8-bit low-rank correction | The training forward pass is not binary: weights take 17 to 257 levels through random thresholds, blended in over 2,000 steps, and the export takes the sign of the latent weights. What is trained and what is shipped differ, and the low-rank stage exists to repair that. The README gives no teacher scores |
| Ternary Mamba | 87% of an easy-task average kept | Confirmed, with three seeds within 0.13 points. Next-token loss alone gives perplexity 87.55, distillation alone 37.96, half of each 21.67. Tokens from 102M to 307M move it from 21.67 to 20.65 against 17.47. A learned scale collapsed; a relaxation by soft sampling was worse than straight-through |
| BD-Net | Binary depthwise filters fail for two reasons | Three stated reasons, none with a number. All three involve binary activations or the batch normalization that follows. The untreated binary depthwise network still trained: 54.94% against 69.62% for full precision, 58.28% with both fixes. Its better variant keeps some depthwise layers real |
| Binarizing MobileNet | Seen in search results only | Read whole. Its claim that binary depthwise convolution diverges rests on the range of a sum of binary inputs, shows curves and no number, and replaces the layer with grouped convolution |

- An offset per column, as Bi-Mamba trains, is a second stored number per column that adds the same amount to every output of the layer. The project's format has no place for it.
- Quamba2 covers both Mamba generations at 4 and 8 bits. It quantizes the convolution kernel at 8 bits and nothing below 4 anywhere.

Answer:

- Measured: projections around a depthwise convolution convert to two or three levels and keep 85% to 87% of an easy-task average at 1.3B, with distillation from the parent and straight-through training. No work in this group makes the depthwise kernel, the embedding, the output matrix or a normalization gain binary in a language model. The plan holds one case at three levels: PrismML's first 27B release converted the convolution and the normalization weights of its hybrid, and its next release returned them to full precision.
- Inferred: the reasons given in vision for binary depthwise filters failing do not carry to LFM, where activations stay in 16 bits and no batch normalization follows the kernel. What carries is that a 3- or 7-tap filter has too few weights for its rounding error to average out. A sign-only kernel keeps one of 4 shapes per channel in LFM2 and one of 64 in LFM3, and what it loses is each channel's profile across taps. That loss is a number readable from the parent's weights, and it has not been read.

### 4H. What a quick reading of these sources would miss

- BiLLM and ARB-LLM: the bits. Section 4D.
- ARB-LLM: a sign matrix with fitted row and column scales, alone, is at perplexity 10,942.
- Bi-Mamba: trained from scratch against a transformer teacher, with a learned offset per column. It is not a conversion and not a sign-and-scale format.
- DF-SSM: the shipped signs were not what was trained.
- Ternary Mamba: one baseline figure in its correction section (22.04) does not match its main result (20.31 and 21.67), one run in its collapse table reports a perplexity below the teacher's with no explanation, and confidence intervals for the same run differ between tables.
- BD-Net: several figures in its text do not match its tables, its first variant is below the baseline on three of five datasets, and "1.58-bit" there is a label for two summed binary filters.
- Nemotron Bolt: its text and its table disagree on which layers use the 4-bit floating-point format, and no sensitivity measurement supports its allocation.
- The precision law: nothing below 3 bits, loss only, models up to 220M in the main fits.
- The token-count law: no control for the learning-rate schedule, which a later paper shows drives the effect.
- CEWT: all results are training from scratch with activations quantized too; the authors say short runs gain little.
- LFM2 report: scores come from a harness with loose parsing and few-shot prompts.
- The LFM2.5 template writes today's date into every tool prompt.
- INQ's code: the freeze is missing from the processor branch of the update.

### 4I. Superseded, corrected or contradicted

- The token-count law of arXiv 2411.17691 is contradicted in its interpretation by arXiv 2510.06213.
- Batch 7's line that Bi-Mamba's released code computes its scale and holds it out of the gradient described a class the training script does not use. The trained models learn a scale and an offset.
- BiLLM is superseded as a baseline by ARB-LLM, and both by PBBQ, read in batch 9, on the same accounting.
- The first reviewer's own statement of idea I34 is corrected in section 3F.

## 5. Probabilities

Stated before reading, then after. They are judgments.

| | Before | After | Why it moved |
|---|---|---|---|
| A formula fixed on Qwen3-1.7B, applied under the rule of section 3C, lands on LFM2-1.2B within five points of its Qwen retention | 33% | 30% | For: LFM2's block is Qwen's block plus one operator whose projections convert in every published relative; fewer gains that cannot be folded than Qwen has (2,816 against 9,216); the tied matrix is a smaller share. Against: the nearest published trainer needed settings per family; no source applies one trained recipe unchanged to two families; the parent sits at or near guessing on some of the ten, which thins the comparison; its scores come from a looser harness than the project's |
| The same for LFM3-1.7B | 35% | 30% | For: same size as Qwen; a normalization after every sublayer in the named track. Against: 103,168 gains that cannot be folded, which the Qwen run cannot inform; head gates; the card's warning that thinking-off behaviour is inconsistent; a mid-training stage of the kind one paper finds raises rounding damage; Liquid AI's own 4-bit training leaves the embedding, gains and kernels alone |
| A 1-bit Qwen3-1.7B in the project's format reaches 90% retention by some training | 38% | 36% | The precision law, extended below its range, lands near the one measured 1-bit point at this size (74.5%), and reaching 90% would need the 1-bit model to do far better per stored bit than that law allows. Against that, the same arithmetic underestimates the published three-level model by about ten points, so distilled conversion beats the law. One-shot methods are far from usable in this format, which was already assumed |
| It reaches 99% | 4% | 4% | Nothing read bears on it |

## 6. What this batch serves in the plan

- U6, whether a Qwen recipe carries to LFM: the rule (3C), the tensor table (3B), the test (3D). These are the content of checklist row C142 and part of C139.
- CH5, attributing a failed transfer: the five arms (3E). Quamba2's embedding figures add weight to arm 2.
- C139, the format and graph contract: what the reference runtime does with each tensor kind (2F); three tool formats and the date line (4F); the bits table (3B).
- C140, the ruler: Liquid AI's open scorer for three of the ten; its measurements of the Qwen parent with thinking off on six of the ten; the harness differences; the GPQA standard error; pinning the date.
- C143, the form of the per-benchmark test: the chance-corrected ratio and the three-standard-error exclusion are a proposal for the reviewers to settle.
- C144, the fold of gains: its cost is now stated (3F, g) and ARB-LLM gives a measured size for what column factors are worth without training.
- P3, no recipe of ours leads: nothing here changes the named starting recipe. MagR's groupwise routine is a candidate for the step before conversion.
- Ideas: I1 gains a published precedent and an extension to the convolution block; I24 gains indirect support; I25 confirmed exact; I26 limited to LFM3 and to the named track; I27 lowered; I28 exact where claimed; I29 priced; I34 corrected.

## 7. Could not be opened in this session

- The drawings of the patent application. Google Patents lists 16 drawing sheets and a fetch returns text only. Neither reviewer has seen figures 6 and 7.
- The rows of Pipette's results table at `pipette.liquid.ai/results` and of its raw data page. Both are drawn by script, and a fetch returns the column headers only. The table has columns for IFBench, IFStruct, GPQA Diamond, MATH-500 and their mean, each beside its full-precision counterpart.

## 8. Sources

Item 1:

- LFM3-1.7B, card and files: https://huggingface.co/LiquidAI/LFM3-1.7B
- LFM3-1.7B-Base: https://huggingface.co/LiquidAI/LFM3-1.7B-Base
- LFM3-1.7B-GGUF: https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF
- LFM3-1.7B-NVFP4: https://huggingface.co/LiquidAI/LFM3-1.7B-NVFP4
- Release post: https://www.liquid.ai/blog/lfm3
- Quantized versions of LFM3-1.7B: https://huggingface.co/models?other=base_model:quantized:LiquidAI/LFM3-1.7B
- Distilled 4-bit builds, post: https://www.liquid.ai/blog/qad
- LFM2.5-1.2B-Instruct-GGUF with its `qad` folder: https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF
- "Quantization-Aware Distillation for 4-Bit On-Device Language Models", NeurIPS 2026 workshop, read whole from a copy the project owner supplied: https://openreview.net/forum?id=Lc5ByfbARS
- Liquid AI's training code: https://github.com/Liquid4All/liquid-finetune
- Pipette scorer: https://github.com/Liquid4All/pipette-scores
- Pipette documentation, pages read: introduction, reading results, quantization, evaluation methodology, coverage and selection, result selection, limitations, data exports, and the pages for GPQA Diamond, MATH-500 and IFBench: https://pipette.liquid.ai/docs/introduction
- `Liquid4All/pipette-clients`, repository read directly: `docs/methodology/evals.md` whole: https://github.com/Liquid4All/pipette-clients
- `Liquid4All/pipette-mgmt`, repository read directly: `docs/scoring-service.md`, the accuracy section of `docs/benchmarks.md`, and the methodology pages for GPQA Diamond, IFBench and both MATH-500 versions, whole: https://github.com/Liquid4All/pipette-mgmt
- llama.cpp at commit 0e4e925: https://github.com/ggml-org/llama.cpp

Item 2:

- RaBiT: https://arxiv.org/abs/2602.05367 and its code
- AF1: https://arxiv.org/abs/2609.06161
- TWLA: https://arxiv.org/abs/2606.13054
- The counts and identities: `scripts/b10_bits.py`, run on public shapes only

Item 3:

- Mirror-descent view, code: https://github.com/kartikgupta-at-anu/md-bnn
- Greedy rounding, code: https://github.com/elybrand/quantized_neural_networks
- MagR, code: https://github.com/AozhongZhang/MagR
- CEWT: https://arxiv.org/abs/2609.32659 and https://github.com/1733116199/cewt
- Survey of transforms: https://arxiv.org/abs/2608.25188
- BiLLM: https://arxiv.org/abs/2402.04291
- ARB-LLM: https://arxiv.org/abs/2410.03129 and https://github.com/ZHITENGLI/ARB-LLM
- INQ, code: https://github.com/AojunZhou/Incremental-Network-Quantization
- Low-bit quantization and training tokens: https://arxiv.org/abs/2411.17691
- Scaling laws for precision: https://arxiv.org/abs/2411.04330
- Training dynamics and rounding damage: https://arxiv.org/abs/2510.06213
- Ternary Mamba: https://arxiv.org/abs/2606.18114
- Nemotron 3.5 Bolt: https://arxiv.org/abs/2610.33039
- Bi-Mamba, code: https://github.com/Tangshengku/Bi-Mamba
- DF-SSM, code: https://github.com/cs-cmyk/df-ssm
- BD-Net: https://arxiv.org/abs/2511.17633
- Binarizing MobileNet: https://arxiv.org/abs/2005.06305
- Quamba2: https://arxiv.org/abs/2503.22879
- LFM2 technical report: https://arxiv.org/abs/2511.23404
- transformers, LFM2 model file: https://github.com/huggingface/transformers
- mlx-lm, LFM2 implementation: https://github.com/ml-explore/mlx-lm
- LFM2.5-1.2B-Instruct: https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct
- LFM2.5-1.2B-Thinking: https://huggingface.co/LiquidAI/LFM2.5-1.2B-Thinking
- LFM2.5-1.2B-Base: https://huggingface.co/LiquidAI/LFM2.5-1.2B-Base
- LFM2-1.2B tokenizer configuration: https://huggingface.co/LiquidAI/LFM2-1.2B

## 9. Not read

- Any figure in any paper or post. The reading tool returns text. Where a result exists only in a figure, it is not used.
- The two pages of section 7.
- ARB-LLM's supplementary file, with its proofs and the pseudocode of two variants. It is a separate download from the code repository's releases.
- The appendix of the Nemotron Bolt paper, which the page does not carry.
- In llama.cpp, `src/llama-quant.cpp` and `conversion/base.py` outside the rules that decide which tensors are converted and to what; the vision and audio parts of `conversion/lfm3.py`.
- In the CEWT code, `base_linear.py` beyond its outline.
- The vocabulary file `tokenizer.json` of any LFM model. Only the configuration was read.
- The headers of the LFM2 model files.
- The second page of the listing of quantized versions of LFM2-1.2B.
- Liquid AI's documentation pages.
- Quamba2's code.
