# BOOT missing source — ePrint 2026/2368

- Date: 2026-10-27
- TRACK_ID: BOOT
- Source: Cheon, Cho, Jung, Lim, "Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS", ePrint 2026/2368
- Status: SOURCE_GATED / HIGH PRIORITY FULL PDF NEEDED

## Why this source matters

Public metadata/abstract reports a construction that extracts all radix-B digits of a CKKS input in parallel using a single bootstrapping, with:
- 2.04x reported speedup for coefficient-integer digit decomposition at ten radix-64 digits;
- 7.83x reported speedup for sign evaluation on 1024 real input pairs at 2^-60 separation;
- O(log B) lookup depth and O(log u) carry look-ahead;
- Theta(u) slots per input;
- a claimed shift from Theta(p^2) to Theta(p) modulus consumption for close-input sign evaluation in the stated model.

These claims directly affect the BOOT line's understanding of discrete-CKKS digit extraction / cleaning bottlenecks used by recent high-precision bootstrap constructions.

## Retrieval attempts

Current research MCP:
- official ePrint PDF -> HTTP 403;
- exact-title arXiv search -> no matching copy;
- fixed GitHub ePrint mirror -> unavailable;
- no obvious public GitHub implementation repository found by exact-title/author/radix-64 searches.

Public abstract-level evidence is insufficient to audit:
- exact algorithm and correctness;
- whether "single bootstrapping" shares one expensive stage or changes the encoding;
- parameter/security/precision match;
- stage-level bottleneck;
- overlap with CKSS25, Focused CKKS 2026/2531, or GCKKS 2026/2600;
- whether any further optimization is plausible.

## Action when supplied

If an authorized copy is placed under papers/supplied/, prioritize it before further fresh scouting. Audit exact decomposition interface, carry-lookahead structure, modulus/precision budget, parallelism model, and matched benchmark.


## Resolution update — 2026-10-27
RESOLVED: the human supplied the full PDF under papers/supplied/ and it has now been read in the BOOT audit. This source is no longer blocking.
