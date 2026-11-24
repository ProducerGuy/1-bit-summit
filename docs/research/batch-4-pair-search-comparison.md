# Reference pair search: the two reviews compared

Both reviewers searched for a reference pair for the fingerprint without seeing each other's work. The second reviewer's document is `batch-4-pair-search-second-reviewer.md`. The first reviewer's results are in `batch-4-findings.md`, section 2E, and `fingerprint-displacement-reading.md`. Every location and claim below was checked at source.

## 1. Agreement

- Meta's ParetoQ files are behind a form that asks for a legal name, a date of birth and an organization. They are not used.
- No copy of those files exists that can be shown to be genuine. The first reviewer adds two checks: the model host's full listing holds one third-party repository, a 4-bit bundle with no original weights file, and ModelScope's entries for the 1.5B pair hold only a readme.
- No open pair meets every condition at once: a 1-bit child trained from a known parent by a published recipe at a known budget.
- A fingerprint compares the parent with the weights the child actually runs with, in the same coordinates. A child stored in a rotated basis, or as the weights behind a quantizer, has to be brought to that form first.

## 2. Found by the second reviewer only, and checked

### 2A. Boole-1.7B: a second released 1-bit Qwen3-1.7B

| Fact | Source | Check |
|---|---|---|
| A 1-bit model derived from Qwen3-1.7B, published 11 October 2026 by Precision Numerics, Apache-2.0, not gated | https://huggingface.co/precision-numerics/Boole-1.7B, https://precisionnumerics.ai/blog/boole-1p7b | Confirmed. The file list shows one weights file of 247 MB in safetensors with ordinary download links |
| Its scores on the ten-benchmark suite with PrismML's settings and thinking off, by the publisher's own run: Qwen3-1.7B 58.83, Boole 50.55, which is 85.9% | The same | Confirmed as published. Per-benchmark numbers are in a chart only. Nobody outside the publisher has reproduced them |
| On the same run PrismML's 1-bit 1.7B scores 44.97 and its ternary 1.7B 51.57 | The blog post | Confirmed. That is 76.4% and 87.7% of the publisher's teacher score. PrismML's own figure for its 1-bit 1.7B is 40.88 of 58.24, 70.2%: the two harnesses differ by four points on the same model |
| Boole beats the 1-bit Bonsai on 7 of 10 benchmarks, most in mathematics and code, and scores lower on MuSR, IFEval and BFCL | The blog post | Confirmed |
| How it was made is not published: no method, data, budget or teacher setup | Model card, blog post, runtime code | Confirmed. The runtime code's reader calls the scales "learned per-group scale" |
| Format: packed sign bits and a scale for each group, every projection in every block binary, embedding and output head binary, normalization gains dense. The embedding and the head share one set of signs and have separate scales | https://github.com/PrecisionNumerics/boole-demo, files `w1.py`, `qwen3.py`, `vllm_quant.py`, read in full | Confirmed in code |
| Group size 128 | Not stated on the card or the blog; the reader takes it from the file | Confirmed by arithmetic: 1.7206 billion signs are 215.1 MB, which the blog gives as the ideal; one 16-bit scale for each 128 weights adds 26.9 MB; a second set for the tied matrix adds 4.86 MB; the total, 246.8 MB before the normalization gains, is the published 247.0 to 247.1. PrismML's 242.4 MB is the same count without the second set |

- The format is ours with one addition: 2.4 million extra scales, so the tied matrix can be sized differently in its two roles. That is 1.148 bits per weight against 1.125.
- That addition is ideas I12 and I17 built into a released model: the roles of the tied matrix separated by scales.

### 2B. An independent ternary reproduction on our teacher

| Fact | Source | Check |
|---|---|---|
| A ternary child of Qwen3-1.7B trained by straight-through training with distillation from the full-precision model, Apache-2.0, not gated | https://huggingface.co/alllwang/bonsai-repro-1.7B-ternary | Confirmed. One weights file of 3.44 GB |
| Recipe: 128 weights to a group with 42 zeros and one scale, in a Hadamard-rotated basis of block 1,024, tied matrix included; FineWeb-Edu text; 20,000 steps of 8,192 tokens at rate 6e-5 with cosine decay, about 164 million tokens | Model card | Confirmed. The command-line settings the second reviewer lists from the training log were not opened; the card's totals agree with them |
| Final state: 0.034% of signs changed against the starting codes, 9.44% of zero positions changed, perplexity 35.0, 66.5% top-1 agreement with the teacher | Model card | Confirmed |
| Scores beside the parent: ARC-C 33.5 of 43.0, HellaSwag 46.5 of 60.5, MMLU 34.5 of 60.2, GSM8K 54.7 of 68.8. It trails PrismML's ternary 1.7B on every task | Model card | Confirmed |
| The released file is 16-bit values folded back to the original basis. The ternary codes are recovered by applying the rotation again | Model card | Confirmed as stated. Whether packed codes are also published in its training folder is not checked |

### 2C. A distinction worth keeping

- Three comparisons are different objects: the parent against the weights behind the quantizer; the parent against the weights the child runs with; the child at the start of training against the child at the end. The published 29% for PrismML is the second. The 0.034% above is the third.

## 3. Found by the first reviewer only

- A reading of the fingerprint that needs no reference files (`fingerprint-displacement-reading.md`): one displacement number, r near 1.25, reproduces PrismML's published sign statistics, and ParetoQ's reported movement corresponds to r near 0.4.
- Two more open pairs, weaker than the two above: a short 1-bit run on TinyLlama 1.1B in groups of 128, and ternary children of Llama-3-8B-Instruct at 10 and 100 billion tokens, whose parent has an untouched open copy at NousResearch/Meta-Llama-3-8B-Instruct.
- The size arithmetic that pins Boole's group size and its second set of scales.

## 4. Errors

Second reviewer:

- The group size of 128 and 16-bit scales are attributed to the publisher's statements. Neither the card nor the blog states them. They follow from the code and from the file size.
- No other error found. The document separates what it confirmed from what it did not, and it is right on each point checked.

First reviewer:

- Missed Boole-1.7B through four batches. It is a released 1-bit conversion of our own teacher, six weeks old, scoring above the model the whole project has used as its outside reference. No search asked the plain question: who else has released a 1-bit Qwen3-1.7B. The one listing that could have shown it was sorted by downloads and cut at 100.
- Missed the independent ternary reproduction the same way.
- Reported "no open copy" of ParetoQ's files from a listing that was cut off, before the full listing confirmed it.

## 5. What it changes

- The outside reference. A second team has published a 1-bit Qwen3-1.7B at nearly our format that keeps 85.9% by its own run, where the same run gives PrismML's model 76.4%. If the ruler confirms it, the public line at this size is about nine points above the one the project has been counting from, and it was reached with open weights under a permissive license.
- The first full run. It scores three models, not two: the teacher, PrismML's 1-bit 1.7B and Boole. That run is also the only check on the publisher's number.
- The fingerprint. Boole has the same parent, the same group size, and a 247 MB file. S2 runs on it unchanged for the body. Two released models from one parent, one of them nine points better, is a stronger comparison than any reference pair: where their movement and their scales differ is where the nine points are.
- The reference pair. The ternary reproduction gives one known-recipe point on our own teacher: 164 million tokens changed 9.44% of zero positions and almost no signs. By a rough use of the displacement reading that is r near 0.15. With ParetoQ near 0.4 at about 30 billion tokens and PrismML near 1.25, the movement axis has three marks.
- The tied matrix. Boole's separate head scales are the first released evidence that separating the two roles goes with a better model. It is a correlation: the method is unpublished.
- Tool calling. Boole is below PrismML's model on BFCL while nine points above it overall. Whatever Boole did, it did not return tool calling. That fits the block-by-block evidence that this damage is not at the output.
- The starting model. Training from Boole would start higher, if its number holds and if its second set of scales is allowed in the format. Both are open.

## 6. Decisions for the project owner

| Decision | Options | What it changes |
|---|---|---|
| Is a second set of scales for the tied matrix inside the format | Yes: 1.148 bits per weight, as Boole ships. No: one scale set, 1.125, as PrismML ships | Whether Boole counts as a model at our format, whether it can be a starting model, and whether idea I12 may add scales or must work within one set |
| Which model the steps count from | PrismML's 1-bit 1.7B as now. Or the best released model at the format that the ruler confirms | Where "the next five points" starts. On the publisher's run Boole is about nine points higher |

## 7. Adopted

- M1 scores Boole as a third model, with the same records.
- S2 and S4 run on Boole as well as on PrismML's model. S5 is redefined around it: the two released children of Qwen3-1.7B first, then the ternary reproduction brought back to its codes, then the weaker open pairs.
- Two decisions added to the ruler's list for the owner.
- A reading row for batch 5: everything Precision Numerics has published, in full, for any statement of method.
- Odds: Boole's retention on our ruler is at least 80%: 65%. Scale-only training from PrismML's model reaches a step: 57%, from 55%, on the evidence of the separated head scales.
