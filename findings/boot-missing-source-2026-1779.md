# BOOT missing source — ePrint 2026/1779

- Date: 2026-10-27
- TRACK_ID: BOOT
- Source: Zhaoyang Liang, Dan Ding, "Bootstrapping via Ring Switching without Slot Recovery: Independent Leaf Evaluation for SIMD-Packed Ciphertexts", ePrint 2026/1779
- Status: SOURCE_GATED / HIGH PRIORITY FULL PDF NEEDED

## Why this source matters

Public abstract-level evidence describes a whole-bootstrap ring-switching result rather than a local implementation tweak:
- CKKS/BGV/BFV ring-switched bootstrapping without the usual slot-recovery step;
- independent evaluation on smaller-ring leaves;
- a claimed affine iff boundary for arbitrary real CKKS slotwise functions without slot recovery;
- CKKS throughput gains around 99.7%-121.3% in the reported configurations;
- BGV speedups and server-key reductions.

If correct under matched parameters, this is directly in the high-value BOOT design space because it changes the ring-switching bootstrap architecture and removes an entire recovery phase.

## Retrieval status

Current research MCP:
- official ePrint PDF -> HTTP 403;
- exact-title arXiv search -> no matching full text;
- fixed GitHub ePrint mirror -> unavailable.

Public GitHub archives expose title/metadata/abstract only. No obvious author implementation repository was found.

Do not infer the detailed construction, proof, security budget, or benchmark comparability from the abstract.

## Direct prior source also needed

ePrint 2026/1023, Xiaopeng Zheng,
"Faster CoeffToSlot and SlotToCoeff for Sparsely Packed Ciphertexts with Application to CKKS Bootstrapping"
is a direct sparse-packing/CtS-StC prior source and is likewise unavailable to the research MCP.

When 1779 is supplied, audit it together with 1023 to determine:
1. exact ring-switch map and leaf layout;
2. why ordinary CKKS bootstrap remains correct without slot recovery;
3. exact function-class limitation and where nonlinearity fails;
4. CtS/StC complexity as ring dimension shrinks;
5. correction/noise-capacity savings;
6. security and sparse/dense secret parameter matching;
7. whether any residual leaf recombination, key-switch, or transform bottleneck remains.

## Priority

P0 together with ePrint 2026/2368.
