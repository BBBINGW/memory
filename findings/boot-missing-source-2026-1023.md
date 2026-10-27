# BOOT missing source — ePrint 2026/1023

- Date: 2026-10-27
- TRACK_ID: BOOT
- Source: Xiaopeng Zheng, "Faster CoeffToSlot and SlotToCoeff for Sparsely Packed Ciphertexts with Application to CKKS Bootstrapping", ePrint 2026/1023
- Status: SOURCE_GATED / SUPPORTING PRIOR SOURCE

## Why needed

This source is directly relevant to BOOT-B144 because public metadata and downstream implementations identify it as a sparse-packing CtS/StC optimization for CKKS bootstrapping. It is needed to separate:
- already-known sparse slot repetition / depth-1 transform improvements,
from
- the stronger no-slot-recovery architecture claimed by ePrint 2026/1779.

## Retrieval status

- official ePrint PDF -> HTTP 403;
- no exact-title arXiv copy;
- fixed GitHub ePrint mirror unavailable.

Public codebases reference its algorithms, but those references are not a substitute for the paper's proof/parameter analysis.

## Action when supplied

Audit jointly with 2026/1779 before making novelty claims about ring-switched sparse-packing bootstrapping.
