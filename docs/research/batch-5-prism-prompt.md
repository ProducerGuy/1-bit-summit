# Reviewer prompt: the PRISM article in full

Sent to the second reviewer on 2026-11-25. It carries none of the first reviewer's findings.

```
One source for the 1 Bit Summit project still has to be read in full, and I need you to read it and report back.

THE SOURCE
"PRISM: a diagnostic framework for parametric recall degradation in quantized large language models"
Vaish, Gautam, Tiwari, Yadav. Discover Computing, volume 29, article 700, 2026. Open access, CC BY 4.0.
Article: https://link.springer.com/article/10.1007/s10791-026-10580-5
DOI: 10.1007/s10791-026-10580-5

THE PROBLEM
The project converts a pretrained language model (Qwen3-1.7B first) to 1-bit weights: one sign per weight and one FP16 scale per group of 128 weights, embedding and output matrix included. We need to know where in a network the ability to recall facts is lost when weights are quantized, and how firmly that is established, because it decides where we look first for damage and where a repair should spend its budget. This article claims to measure exactly that. So far the project holds only its abstract. An abstract is not enough.

WHAT I NEED FROM YOU
Read the whole article: every section, every table, every figure caption, and any appendix or supplementary file. Get to the full text by whatever route works. How you get there is yours to choose. The outcome is what matters: the full text read, and reported.

Then report, with the article's own numbers:
1. Models and sizes tested, and how each was quantized: every scheme, every bit width, group or channel settings. State the lowest bit width tested and whether anything at 2 bits, ternary or 1 bit appears.
2. The probes: what each one measures, how its items are built, how many items, and how an answer is scored.
3. Results by bit width for recall of memorized facts, for copying an answer from supplied context, and for comprehension, per model.
4. The component results in full: quantizing only the MLP matrices against only the attention matrices, per model and per bit width, with every control the authors ran (equal weight mass, equal error, calibrated quantizers, seeds).
5. Any result by layer or depth, by matrix type within the MLP or attention, or by kind of fact (frequency, relation type, single-hop against multi-hop).
6. Any repair, mixed-precision recommendation or mitigation, and what it gains.
7. Code and data: links, licenses, and whether the probe sets can be downloaded.
8. Limitations the authors state, and any you see that they do not.

Then, separately and clearly marked as your own judgment:
9. What transfers to a 1-bit model with one scale per 128 weights on Qwen3-1.7B, and what does not.
10. Anything in the article that changes where you would look first for damage, or where you would spend a repair budget.
11. Anything you think I have framed wrongly in this request. Push back if so.

HOW TO REPORT
- One markdown document.
- Start with how you reached the full text and how much of the article you read. If any part could not be read, say exactly which part.
- Mark every figure as read from the article itself or taken from somewhere else. Do not fill a gap from memory.
- Quote sparingly; report in your own words with the numbers.

STANDING RULES OF THE PROJECT
- No personal information of the owner goes into any form, and no credentials or payment are used.
- If you need the owner to do something, your reply shows only his steps, as numbered single-action lines, and nothing else. Results come after he reports back.
```
