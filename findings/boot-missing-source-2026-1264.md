# BOOT missing source — ePrint 2026/1264

- Date: 2026-10-27
- TRACK_ID: BOOT
- Source: Zhihao Li, Xuan Shen, Cheng Hong, Ruida Wang, Xianhui Lu, Tao Wei, "The Power of Low Rank: Fast CKKS Functional Bootstrapping for High-Precision Lookup Tables", ePrint 2026/1264
- Status: SOURCE_GATED / P0 FOR B145 PERFORMANCE

## Why critical

BOOT-B145 needs fourteen functions on a 4096-point window domain. Under the natural 64x64 reshape, every required LUT is exactly rank 1.

Public abstract-level evidence says 2026/1264 introduces LRMT-FBT for low-rank reshaped CKKS LUTs, gives exact rank treatment for separable functions, and supports multi-value/multi-input extensions.

The full source is needed to determine:
1. exact CMult and rotation count at rank 1;
2. multiplicative depth;
3. whether one preprocessing/root stage is shared across all fourteen outputs;
4. ciphertext/slot layout and packing loss;
5. precision/error bound for discontinuous rank-1 indicator functions;
6. security/modulus parameters;
7. benchmark comparability with 2026/2368 and 2026/1869.

## Retrieval status

- official ePrint PDF: HTTP 403;
- exact-title arXiv: unavailable;
- fixed GitHub ePrint mirror: unavailable;
- public GitHub search: abstract copy only, no author implementation located.

Do not infer concrete LRMT performance from the abstract.

## Related finding

- findings/boot-B145-single-fbs-adjacent-window-a2b-2026-10-27.md
- findings/boot-B146-b145-lowrank-lut-backend-gate-2026-10-27.md
