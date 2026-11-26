# Research queue

Every piece of reading and paper work the project still owes, what each helps, and what is already done. Every part names the trial, the decision or the goal it helps.

- Trials are named as in `trials.md`: S1 to S4 are scripts and forward passes on public files, M1 to M4 are model runs.
- Checklist rows (C numbers) and sources (S numbers) are those of `PLAN.md`.
- Both reviewers work each part separately, three parts to a batch.

## 1. When research is finished

- For the next five points: every part in section 3 is marked done, and section 5 is settled.
- For the project: every part in sections 3 and 4 is marked done.
- A part is done when both reviewers have returned, the claims that matter are checked at source, the comparison is filed under `research/`, and the registers and the plan carry what was adopted.
- A new part may be added only with its checklist row and what it helps. Section 7 accounts for every open checklist row, so nothing sits outside this document.

## 2. Done

| Batch | Part | Checklist rows | What it helped | Record |
|---|---|---|---|---|
| 1 | Tool-calling data clean of BFCL | C105 | S1, M2 | `research/batch-1-findings.md`, `batch-1-comparison.md` |
| 1 | ScaleQ-1.58 and CAT-Q, which led to ThinkBit | C105, C62 in part | M2, M3 | The same |
| 1 | The public record on PrismML's method | C105, C100 in part | S2, M3, M4 | The same |
| 2 | Knowledge loss | C109, C62 in part | S4, M1 records, M3 settings | `research/batch-2-findings.md`, `batch-2-comparison.md` |
| 2 | Optimizers for discrete weights | C109, C37 | M3 settings, ideas I13 and I14 | The same |
| 2 | BitDistill, OneBit, BinaryLLM | C109, C5, C77 | M3 settings, idea I15, the starting-model decision | The same |
| 3 | Parts A, B and C of section 3 | C114, C7, C108, C34, C51 | S2, S4, M2, M3, ideas I12 to I18 | `research/batch-3-findings.md`, `batch-3-comparison.md` |
| 4 | Parts D, E and F of section 3 | C115, C102, C53, C57, C31 | S4, S5, M1 records, M2 and M3 settings, the ruler, ideas I19 and I20 | `research/batch-4-findings.md`, `batch-4-comparison.md` |

## 3. Open, for the next five points

Ten parts, three batches. Batches 3, 4 and 5 are done, except part O of batch 5 (Precision Numerics' releases), which was not one of batch 5's three items. Two new reading rows, C119 and C122, came out of batch 5. Within a batch the order does not matter. Batches are ordered so that what a specification already written depends on comes first.

| Batch | Part | Checklist rows | What is read | What it helps | Status |
|---|---|---|---|---|---|
| 3 | A. Fingerprint sources | C7, C108 | The outside reproduction study in full with its fingerprint scripts (S19). Three sources surfaced by the second reviewer: a second fingerprint analysis, a second discussion thread on the 27B model page, the released 1.7B's config files | S2: whether the published 2.257 scale figure is a storage convention read as a scale, and the breakdowns already computed by others. S4's coordinate check. M4. Idea I8 | Done. `research/batch-3-findings.md`, `batch-3-comparison.md` |
| 3 | B. Reasoning recovery from self-generated text | C34 | "Right On Q" (S29) and DiscQuant (S28), with code. The third paper of the row (S30) was read in batch 2 | M2 and M3: what training text returns mathematics and code. Idea I14. DiscQuant: M4 and our own conversion | Done. `research/batch-3-findings.md`, `batch-3-comparison.md` |
| 3 | C. Faster sign training | C51 | WinQ (S46) with code: whether its reset and noise steps apply at 1 bit with group scales | M3: its optimizer settings and the form of the budget on sign changes (idea I13) | Done. `research/batch-3-findings.md`, `batch-3-comparison.md` |
| 4 | D. The decisions paper | C102 | The last 78 thousand characters of S75. S74 and S76 are read in whole | M1: the failure split. S4: how its outcomes are read. Idea I7 | Done. `research/batch-4-findings.md`, `batch-4-comparison.md` |
| 4 | E. Published low-bit training recipes | C53, C57 | ParetoQ (S47) to the end with its result tables and code; QuEST with code | M3: schedule, estimator and token budget. M2: the token ladder | Done. `research/batch-4-findings.md`, `batch-4-comparison.md` |
| 4 | F. Scale-only precedent and exact symmetries | C31 | EfficientQAT (S21), whose second stage trains scales alone; FPTQuant (S22); exact gauges (S23); STBLLM (S24); with code | M2: the nearest published precedent for training scales alone. S3 and idea I1: which reorderings and rescalings are exact. M3 | Done. `research/batch-4-findings.md`, `batch-4-comparison.md` |
| 5 | G. Leftovers of batches 1 and 2 | C62, C112 | ScaleQ-1.58 and CAT-Q in full with code; YAQA; LR-QAT; the body of the JointQ paper; the PRISM article on recall under quantization | M2 and M3: training text and reconstruction settings. Idea I2. S4 and idea I16 | Done by both reviewers. `research/batch-5-findings.md`, `research/batch-5-comparison.md`. The PRISM article in full: `research/batch-5-prism-comparison.md` |
| 5 | N. A reference pair for the fingerprint | C116 | A public full-precision parent and its 1-bit child trained by a known recipe, not behind an access form: mirrors of ParetoQ's files, or another released pair | S5 and idea I20: how PrismML's fingerprint is read, and the total for the budget on sign changes | Done. `research/batch-4-pair-search-comparison.md` |
| 5 | O. Precision Numerics' releases in full | C118 | Both Boole model cards, its blog posts, the runtime repository, its llama.cpp fork, the 32B preview: any statement of method, data or budget | M1's third model, S5, the starting-model decision | Open |
| 5 | H. The outside forensics project in full | C100, C56 | Whitepaper, forensic archive, failure register, experiments, the three gate reports, the paper draft, the scripts behind its Qwen3-1.7B ladder, its newer discussion thread; token count, batch size and step count of each 1.7B run | M3: the learning-rate schedule, where it conflicts with "Linger and Lose" (C111). M4. S2 | Done. `research/batch-5-findings.md`, `research/batch-5-comparison.md` |
| 5 | I. Facts the runs stand on | C3, C4, C6, C8 | The Qwen3-1.7B model card; PrismML's MLX fork and 1-bit kernels; which upstream MLX and mlx-lm versions load the 1-bit files; the evaluation harness on Apple Silicon | M1: the ruler's harness and settings. S2 and S4: reading and loading the released files | Done. `research/batch-5-findings.md`, `research/batch-5-comparison.md` |

## 3A. Batches 8 to 10, in the order agreed on 25 November 2026

Each batch has three parts and is worked by both reviewers independently. Each part names the open problem, challenge or unknown it serves (`PLAN.md`, section 1A).

| Batch | Part | Checklist rows | What is read or worked | Serves | Status |
|---|---|---|---|---|---|
| 8 | A. A second 1-bit model of the same parent | C118 | Everything Precision Numerics has published on its Boole models: model pages and files, posts, code, forks | U4, P3; the first benchmark run and the choice of starting model | Done by the first reviewer (`research/batch-8-findings.md`); second reviewer's return awaited. Brief: `research/batch-8-prompt.md` |
| 8 | B. The outside study of PrismML's 1.7B files | C119 | The whole repository with code: research log, replication plan, the low-bit training reports on a small Qwen, any 1.7B run | U4, P3; the fingerprint run and the sign-and-scale run | Done by the first reviewer; second reviewer's return awaited |
| 8 | C. What may be missing under 2 bits | C122 | The public survey of methods under 2 bits; an independent audit of the Bonsai 2.5 report; the two post-training methods behind its comparison files; the packed low-bit types in upstream runtimes | P3, U2 | Done by the first reviewer; second reviewer's return awaited. Left for a later read: LBLLM at source, the later appendices of PV-Tuning |
| 9 | A. Constraint and relaxation methods, and two paper checks | C125 | BinaryRelax, ProxQuant and ASkewSGD in full; for each method of ours, whether its first step moves the model and whether its end point fits the format | P3 | Open |
| 9 | B. Factorization and rotation papers not finished | C125 | LittleBit-2, the TWLA method, the structured Kashin paper, PBBQ, the rest of AF1, the factorization notebooks, with code | P3, U2 | Open |
| 9 | C. What two-level weights can store | C125, C124 | The capacity papers and their appendices; the theory behind the 99% goal; the design of the capacity measurement | U2, CH3 | Open |
| 10 | A. LFM3 in depth | new | Everything public on LFM3, which has no technical report; Liquid AI's 4-bit-adapted weights as a control | U6 | Open |
| 10 | B. The transfer rule in writing | new | What "nothing changes but shapes" means; the format's exceptions; the equivalence test; ideas I24 to I29 worked through | U6, CH5 | Open |
| 10 | C. Sources read in part in batches 6 and 7 | new | Every source either reviewer read in part, figures included | P3, U6 | Open. Needs the files for the figures |

Not in a batch: C111 waits on the result of S4; the model file headers are a run (C9).

## 4. Open, for later goals

These do not change which trial runs first. They stay open until their goal is taken up.

| Batch | Part | Checklist rows | What is read | What it helps | Status |
|---|---|---|---|---|---|
| 6 | J. Mirror-descent theory | C26, C27, C43 | S14, S17, S18 and the matrix mirror-descent paper; S15, S16 and the noise-shaping follow-ups; S38 and its results at 1 bit | Our own conversion formula. Idea I5 (the Caltech potential at 1 bit). The implementation row C42 follows it | Done by both reviewers. `research/batch-6-findings.md`, `research/batch-6-second-reviewer.md`, `research/batch-6-comparison.md` |
| 6 | K. Compensation and factorization | C38, C41 | Noda's cross-layer compensation (S35); double binary factorization (S36) with code | Our own conversion formula. M4 | Done by both reviewers. `research/batch-6-findings.md`, `research/batch-6-second-reviewer.md`, `research/batch-6-comparison.md` |
| 6 | L. Structure of the damage, and prior art for one hypothesis | C52, C47, C46 | S44 and S45; clipping schedules, box-constrained and proximal quantization training, arXiv 2609.32659; any measurement of bits stored per parameter in binary or ternary transformers | The science scoreboard. Hypothesis H20. How S4's results are read | Done by both reviewers. `research/batch-6-findings.md`, `research/batch-6-second-reviewer.md`, `research/batch-6-comparison.md` |
| 7 | M. LFM2 | C11, C18 | Any published low-bit LFM2 work; the checkpoint chosen and pinned, its license | The LFM2 goal. The scripts C9 and C63 follow it | Done by both reviewers: `research/batch-7-findings.md`, `research/batch-7-second-reviewer.md`, `research/batch-7-comparison.md`. Three items: the target and its licence; low-bit LFM2 and models built like it; carrying a recipe from Qwen to LFM2. Brief: `research/batch-7-prompt.md` |

## 5. Paper work that is not reading

| Item | Checklist row | Depends on | What it helps | Status |
|---|---|---|---|---|
| Settle the learning-rate schedule, the form of the budget on sign changes, and the handling of the tied matrix's two roles | C111 | Parts C, E and H; the result of S4 | M3's specification | Open |
| Specifications of M2, M3 and M4 | C107 | Section 3 done and approved; the results of S4 and M1 | The runs themselves | Not started, by the project owner's ruling |

## 6. Watched, not readable yet

Code announced and not released. Each is checked again when its part comes up.

| What | Would help |
|---|---|
| ThinkBit's training code | M2, M3 |
| The PRISM article's code, probes and per-item results. The address the article gives returns not found | S4's probe of recall, copying and composition |
| CAT-Q's training code | M3 |
| On-policy distillation's code | Idea I14 |
| ΣΔ-Sampler's code | Idea I13 |
| BitDistill's and BinaryLLM's training code | M3 |

## 7. Every open checklist row, accounted for

`PLAN.md` has 53 rows marked open, and two more with an open remainder.

| Kind | Rows | Where they are tracked |
|---|---|---|
| Reading and paper work, 6 rows | C18, C111, C118, C119, C122, C125 | Sections 3, 4 and 5 of this document |
| Scripts and runs, 33 rows | C9, C10, C28, C29, C32, C33, C42, C49, C50, C55, C58, C59, C60, C63, C64, C65, C67, C69, C75, C76, C79, C81, C89, C90, C92, C93, C95, C96, C97, C98, C99, C110, C124 | `trials.md` for those with a trial (C76, C90 and C92 are S2; C67 and C50 are S3 in part; C110 is S4); the plan for the rest |
| Registers, kept current | C106, C107, C113 | `ideas.md`; `trials.md` and `specs/`; this document |
| Written, with decisions open | C104 | `ruler-spec.md`, section 11: five decisions for the project owner |
| Milestones, 12 rows | C12 to C17, C19 to C24 | The plan's ladder |
