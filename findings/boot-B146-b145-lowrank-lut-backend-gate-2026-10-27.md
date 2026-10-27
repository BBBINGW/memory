# BOOT-B146 — Performance/backend gate for B145 single-FBS arithmetic A2B

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: BOOT-B145
- Sources:
  - supplied 2026/2368
  - supplied 2026/1163
  - public artifact/code for ePrint 2026/1200
  - public abstract/metadata for ePrint 2026/1264
- Status: PASS_STRUCTURE / SOURCE_GATED_1264 / NATIVE_NOT_YET

## Question

Does B145 necessarily pay the worst-case cost of fourteen generic 4096-point Hermite LUT evaluations, making one large FBS slower than the two smaller FBS calls of 2026/1869?

## 1. Character Block Encoding (2026/1200) is not the main backend

2026/1200 decouples LUT evaluation from bootstrapping by representing a t-ary value in a character basis, so arbitrary LUTs become affine maps / one-level computations.

However, the released BRU implementation encodes a value modulo t with width t-1 coordinates.

For t=4096, direct BRU would therefore require 4095 block coordinates per value. This destroys the high packing density that makes 2026/1869 attractive.

The public artifact also caps its direct from_standard BRU conversion at log2(t)<=7 for the reported LogN=15 chain. This is an implementation constraint rather than an impossibility theorem, but it reinforces that direct 4096-symbol block conversion is not the obvious B145 path.

Decision: 2026/1200 is relevant prior art and may inspire factored encodings, but direct BRU-4096 is PARKED as the primary backend.

## 2. B145 LUTs are exactly rank one after 64x64 reshaping

Write each 4096-window as

    w = 64 b + c,   b,c in Z_64.

B145 needs:
- carry intercept:
      G(b,c)=H(b);
- carry slope:
      S(b,c)=L(c)(P(b)-T(b));
- six raw bit functions:
      F_k(b,c)=bit_k(b);
- six correction functions:
      D_k(b,c)=L(c)(bit_k(b-1)-bit_k(b)).

Under the matrix view with row index b and column index c:

    G = H(b) * 1(c)                   rank 1
    S = (P(b)-T(b)) * L(c)            rank 1
    F_k = bit_k(b) * 1(c)             rank 1
    D_k = Delta_k(b) * L(c)           rank 1

where Delta_k(b)=bit_k(b-1)-bit_k(b).

Thus every one of the fourteen real LUT outputs is exactly separable / rank 1. No numerical low-rank approximation is needed.

## 3. Direct match to ePrint 2026/1264

Public abstract-level evidence for ePrint 2026/1264, "The Power of Low Rank: Fast CKKS Functional Bootstrapping for High-Precision Lookup Tables", states that:
- large LUTs are reshaped into matrices;
- separable/structured functions admit exact low-rank bounds;
- LRMT-FBT evaluates via a low-rank decomposition rather than the full matrix;
- it supports multi-value and multi-input extensions.

This is a near-ideal structural match to B145 because the required matrices have exact rank r=1.

However, the full 2026/1264 PDF is currently unavailable to the research MCP:
- official ePrint PDF returns HTTP 403;
- no exact-title arXiv copy was found;
- fixed GitHub ePrint mirror has no PDF;
- no public author implementation repository was found.

Therefore exact operation counts, level depth, precision loss, packing layout, and sharing across fourteen rank-1 outputs cannot yet be certified.

## 4. Fallback evidence if LRMT is unavailable

B145 remains algebraically viable without 1264.

2026/2368 already implements a one-bootstrap B=64, B^2=4096 digit-decomposition circuit at N=2^16. This establishes that the 4096 root domain itself is feasible under CKKS.

2026/1163 SWIFT independently evaluates 12-bit / 4096-point LUTs, including configurations at N=2^15. It substantially reduces latency by spending extra SIMD slots on exponential powers.

These are not matched performance estimates for B145, but they falsify the strongest negative claim that a 4096-point LUT necessarily forces an impractical ring dimension or an unusable bootstrap.

## 5. Current cost picture

For n=256, B145 uses u=43 radix positions and one sequential 4096-domain FBS/root stage followed by a six-round affine prefix scan.

The post-LUT tail is small:
- 6 prefix CMults;
- 6 parallel bit-correction CMults;
- depth about 7 in the cheap-output variant.

The dominant uncertainty is therefore the multi-output rank-1 LUT backend.

The strongest candidate implementation hierarchy is now:

1. LRMT-FBT / low-rank matrix backend from 2026/1264 — preferred if full-source audit confirms multi-value sharing and favorable depth.
2. Standard 2026/2368-style root + multi-value Hermite/PS — correctness fallback, likely worse latency.
3. SWIFT-style power expansion — optional small/moderate-batch latency backend; costs slots.
4. Direct 2026/1200 BRU-4096 — reject as main path because width is 4095 coordinates/value.

## 6. Decision

B145 remains PROMISING and is not killed by the 4096-point lookup size.

The lookup family has stronger structure than a generic 12-bit LUT: every required output is exact rank 1 under the natural 64x64 decomposition. This makes ePrint 2026/1264 the decisive performance source.

No Codex/native experiment yet. The cheapest next decisive action is to obtain and audit the full 2026/1264 paper, then derive a matched level/modulus/CMult model for the fourteen rank-1 outputs.

If the audited LRMT cost is favorable, B145 should advance to a native prototype; otherwise test the standard 2368 backend before killing it.
