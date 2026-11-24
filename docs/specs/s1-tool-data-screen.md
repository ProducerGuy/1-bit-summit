# S1 specification: cleanliness screen of tool-calling training sources against BFCL v3

Trial S1 of `trials.md`. No language model is trained or scored. One embedding model and one small set of control restatements are used, both local.

## 1. Purpose

BFCL v3 has no training split, and no public tool-calling set is certified clean of it. Tool calling is 36.9 of the 173.6 summed points the released 1-bit 1.7B loses. Any training text for tool calling therefore has to come from other sets, and the ruler forbids test items in training text in their original words or restated (`ruler-spec.md`, section 9).

This trial measures, for each candidate set, how much of it overlaps the BFCL v3 test files, removes the overlap, and counts what is left by kind of case. Its output is the tool-calling pool that the scale-only and sign-and-scale trials may draw from, with a ledger of everything excluded.

## 2. Inputs

### 2A. Reference set

- The 13 single-turn subsets of BFCL v3 that the ruler scores: simple 400, multiple 200, parallel 200, parallel_multiple 200, java 100, javascript 50, live_simple 258, live_multiple 1,053, live_parallel 16, live_parallel_multiple 24, irrelevance 240, live_relevance 18, live_irrelevance 882. Total 3,641 items.
- The same pinned files the ruler uses. The commit and the hash of every file are recorded in the report.
- From each item: the user query (every user turn), every tool definition offered (name, description, parameter names, parameter descriptions), and the reference calls where the benchmark supplies them.

### 2B. Candidate sets

| Set | Why it is a candidate | Known caution |
|---|---|---|
| xLAM function-calling 60k | Largest verified single-turn set; 3,673 executable APIs in 21 categories | Built with BFCL in view. One published measurement of its tool definitions against BFCL: 0.656% by shared token runs, 5.247% by embedding similarity (ToolFlow, arXiv 2410.18447). Distributed behind an access agreement |
| xlam-irrelevance-7.5k | 7,500 items whose correct function was removed, the published repair for the loss of refusals | Derived from xLAM-60k, so it inherits its overlap |
| ToolACE | 26,507 tools; multiple-candidate, parallel and when-to-call cases | None measured |
| Hermes Function Calling v1 | 8,940 items | One subset is derived from Glaive. Glaive's test data is one of four sets BFCL's curators removed overlap against, so Glaive-derived text is the likeliest to restate benchmark items |
| When2Call | Built for the decision of whether to call | None measured |

For every set the report records: the exact source, the revision, the file hashes, the license, and the item count as downloaded. If a name, size or license differs from this table, the difference is reported and nothing is assumed.

### 2C. Controls

- Positive controls, 100 BFCL items in four planted forms, placed in a dummy candidate set: exact copies; copies with case, spacing and punctuation changed; copies with every number and proper name replaced; restatements written by the full-precision Qwen3-1.7B teacher, thinking off, asked to reword the request while keeping the task.
- Negative control: 1,000 items from a public instruction set that contains no function calling.
- Controls measure the screen. They are never training text.

## 3. Definitions

### 3A. Text preparation

- Normalized text: Unicode NFKC, lower case, runs of whitespace collapsed, punctuation removed.
- Tool definition as text: the name, the description and each parameter's name and description, in a fixed order, from the definition's canonical form (keys sorted).
- Tokens: the Qwen3-1.7B tokenizer, because that is what training would see.
- Embeddings: one open embedding model run locally, the same for every set. The report names it and its revision.

### 3B. When an item is flagged

A candidate query is flagged against the reference set when any of these holds against any BFCL query:

| Test | Threshold |
|---|---|
| Exact match of normalized text | Equal |
| Shared token run | A run of 11 or more consecutive tokens in common that covers more than 10% of the candidate query's tokens |
| Character-level similarity of normalized text | 0.9 or higher |
| Embedding cosine similarity | 0.9 or higher |

A candidate tool definition is flagged when either holds against any BFCL tool definition. These are the two tests of the one published measurement, kept so the result can be set beside it:

| Test | Threshold |
|---|---|
| Shared token runs | More than 10% of the definition's tokens sit in shared runs of more than 10 tokens |
| Embedding cosine similarity | Above 0.9 |

Also recorded and not used alone to flag: a candidate tool whose name equals a BFCL tool's name after normalization; a candidate reference call that equals a BFCL reference call in function name and arguments.

### 3C. Uncertain cases

- A query or tool definition with embedding similarity from 0.8 up to 0.9 and no other flag is uncertain.
- Uncertain cases are clustered by their nearest BFCL item and written to a review file with both texts side by side.
- Uncertain cases are held out of the pool until reviewed. The review is done by the first reviewer, not by the agent that runs the script.

### 3D. What is removed

- A flagged query removes its item.
- A flagged tool definition removes every item that offers that tool.
- A set is dropped whole when more than 10% of its queries or more than 25% of its tool definitions are flagged. At that level the set shares a source with the benchmark and its unflagged items are suspect. These two thresholds are proposals; see section 8.

### 3E. Provenance

For each set, from its paper and dataset card: where its APIs and queries came from, and whether any source is BFCL, the Gorilla project's earlier sets, NexusRaven, Firefunctions, Anyscale or Glaive. A stated derivation from BFCL test data drops the set without further testing.

### 3F. Coverage count

For each set after removal, and for the union, the number of items of each kind:

- One call with one tool offered; one call chosen among several tools; several calls in parallel; several calls among several tools.
- No call correct because no offered tool fits; no call correct because a required argument is missing and the right move is to ask.
- Function definitions written as Java signatures; as JavaScript signatures; as Python or JSON schema.
- Median and 95th percentile of the tool-definition length in tokens, beside the same figures for BFCL's live subsets. The live subsets' definitions come from real users and are less tidy.

## 4. Outputs

| File | Content |
|---|---|
| Report | Sources, revisions, hashes, licenses; the embedding model; every table below; every acceptance check with its result |
| Overlap table | Per set: items, queries flagged by each test, tool definitions flagged by each test, items removed, items uncertain, items kept, and whether the set is dropped |
| Exclusion ledger | One row per removed or uncertain item: set, item identifier, which test fired, the BFCL subset and item it matched, the score |
| Kept lists | Per set, the identifiers of kept items, so the pool can be rebuilt from the public source |
| Review file | Uncertain cases with both texts |
| Coverage table | Section 3F |
| Control table | Share of each planted form caught by each test; share of the negative control flagged |

The candidate sets themselves are not committed. Scripts, tables, ledger and kept lists are.

## 5. Acceptance of the script

- Planted exact copies and copies with case, spacing and punctuation changed: 100% flagged.
- Planted copies with numbers and names replaced, and teacher restatements: the caught share is reported for each test. A share under 80% for restatements by all tests together is reported as a limit of the screen in the report's first lines.
- Negative control: under 1% flagged. A higher share means a threshold is too loose and the run stops.
- xLAM-60k tool definitions by shared token runs: reported beside the published 0.656%. This is a comparison, not a gate; the published tokenizer is not stated in what was read.
- A second run on the same inputs gives an identical ledger.

## 6. How each outcome is read

Fixed before the run:

- A set that is not dropped enters the pool after removal.
- A dropped set is not used, in whole or in part.
- If the union after removal has no Java-signature or JavaScript-signature items, or its no-call items are fewer than its call items by more than ten to one, the missing kinds come from tool prompts written for the purpose (idea I3), which pass through this same screen before use.
- If restatements are caught at under 80%, the pool is still usable for scale-only training on the teacher's own answers, and the limit is carried into the data-hygiene statement of any step claimed on BFCL.
- The mix of kinds in the training text is not decided here. It is decided when the failure split of the baseline run shows which BFCL subsets carry the loss.

## 7. Running constraints

- Runs on the project owner's hardware. No paid model APIs.
- Downloads that require an account, an access agreement or a token are the project owner's to perform. The agent does not request, read or print any credential. If a set cannot be fetched without one, the agent stops on that set and reports it.
- Installing software is the project owner's step. The agent lists what it needs before starting.
- Downloaded files are treated as untrusted data: read by scripts, never executed.
- The agent writes and runs scripts and reads script output. It does not judge overlap by reading raw data itself.
- Logs prune themselves within three days.
- Nothing from the machine (paths, account names, hostnames) enters results, code or commit messages.
- Work is done on a local task branch. Nothing merges without the project owner's approval.

## 8. Decisions needed from the project owner

- The two drop thresholds of section 3D: 10% of queries, 25% of tool definitions.
- Whether to accept the access agreement for xLAM-60k. Without it, xLAM-60k and its irrelevance set are screened only if another lawful copy exists, and otherwise left out.

## 9. Gaps

- No published overlap measurement exists for queries, for any set. The thresholds for queries are set here by analogy with the one published for tool definitions.
- The 0.9 embedding threshold depends on the embedding model. The control table is what shows whether it is placed well for the model chosen.
- A restatement that changes the task's surface and keeps its solution can pass every test here. No automatic screen read so far claims to catch that.
