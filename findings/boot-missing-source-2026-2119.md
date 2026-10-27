# BOOT missing source — ePrint 2026/2119

- Date: 2026-10-27
- TRACK_ID: BOOT
- Source: Ouyang et al., "CKKS Bootstrapping in less than 10ms", IACR ePrint 2026/2119
- Status: SOURCE_GATED / FULL PDF NEEDED

## Why this source matters

Public metadata verifies the author-reported latency claims (8.2 ms single complex ciphertext, 4.6 ms/ciphertext at batch 64) and that the construction builds on SHIP with claimed communication/computation improvements.

The current environment cannot acquire a verified full PDF: direct ePrint PDF retrieval is blocked and the fixed mirror does not contain a verified copy.

Without the full paper, do not claim or compare:
- ring dimension;
- modulus chain;
- precision / recovered levels;
- security level / secret distribution;
- CPU/GPU/hardware;
- thread count;
- evaluation-key sizes;
- stage-by-stage runtime;
- fair speedup versus SHIP, HEAAN, OpenFHE, or other CKKS bootstrapping.

## Required action when supplied

If the PI supplies an authorized copy under papers/supplied/, immediately resume B135 and audit:
1. exact parameter sets and security;
2. hardware/threading;
3. output precision / remaining levels;
4. stage breakdown;
5. what is shared across batch vs mandatory per-ciphertext work;
6. matched comparison to SHIP and relevant contemporary baselines.

Do not send Codex a reproduction task before this audit.
