# Directive ledger

Every instruction issued to another agent, with its verification status.

| Date | To | Directive | Verified against | Status |
|---|---|---|---|---|
| 2026-11-23 | Second reviewer | Paper only: no experiments or code runs | Second reviewer's returned document | Followed. The document states no model was trained or evaluated |
| 2026-11-23 | Second reviewer | Part 1: damage table of retention per benchmark for every released PrismML 1-bit and ternary size, each number with table and page | Returned table against the whitepaper text, tables 5, 7, 8 and 9 of the 1-bit 8B whitepaper | Partly followed. Every size is covered and the 1.7B, 4B and 8B numbers match the whitepapers where they overlap. The first-generation tables carry six benchmarks, not ten: MATH-500, MBPP+, GPQA Diamond and IFBench are absent because the whitepaper files were not read. No page numbers, and the document says so |
| 2026-11-23 | Second reviewer | Part 2: reading record for the ten listed sources, each marked read in full or in part | Returned record against the sources | Followed in form. All ten are present and each is marked read in part. None was read in full |
| 2026-11-23 | Second reviewer | Part 3: ranked repair candidates with loss targeted, evidence, starting model, expected points, probability, cost, gaps, single proving test | Returned list, claims checked at source | Followed. Six candidates, every field present. Checked at source and confirmed: OpenBonsai's 2.892 against 3.191, 30 of 100 and 6 of 50 against 77 and 45; the forensics swap of 18.5851 to 23,606 and its retracted 1.7B numbers. Not checked: the LFQ and OneBit table values, the 0.21 margin factor |
| 2026-11-23 | Second reviewer | Part 4: own suggestions, hypotheses and blind-spot flags | Returned document | Followed |
| 2026-11-23 | Second reviewer | Every factual claim cited with a link; no time estimates; plain markdown; no decimal numbering; no em dashes | Returned document | Followed. One claim not confirmed: a full-precision 8B IFEval of 84.2 on a separate model card. The whitepaper gives 81.5 in tables 5 and 7 |
| 2026-11-23 | Second reviewer | Stop after the one document | Returned document | Followed |
