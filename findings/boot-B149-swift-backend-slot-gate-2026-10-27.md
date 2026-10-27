# BOOT-B149 — SWIFT backend gate for B145 under matched SIMD packing

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145
- Source: supplied ePrint 2026/1163, supplied 2026/1869, supplied 2026/2368
- Status: FAIL_MATCHED_THROUGHPUT / SMALL-BATCH_LATENCY_ONLY / PARK_AS_PRIMARY_BACKEND
- CODEX_REQUIRED: NO

## First: stage-boundary re-audit of B145

A potential ambiguity was rechecked against 2026/1869 Section 5.2.

Before the first functional bootstrap, coefficient-to-radix linear processing already gives, for the power-of-two specialization,

    x_j = d_j + I'_{sj-1} - B I'_{s(j+1)-1},

because kappa=0 and alpha_j=0.

The original 1869 pipeline then:
1. FBS1 computes remainders r_j = x_j mod B;
2. quotients are recovered linearly;
3. neighboring data are combined to obtain a_j with the boundary overflow cancelled;
4. FBS2 evaluates local carry/bit functions.

Therefore B145's pre-FBS construction

    y_j = B x_j + x_{j-1}

really does move the neighboring cancellation before FBS1 and aims to replace the two sequential FBS calls by one B^2-window FBS. B145 was not accidentally operating only after FBS1.

## SWIFT slot requirement

SWIFT FactorGen uses one ExpBTS but replicates each scalar input across SIMD slots to generate tensor factors.

For t factors of size n, its batch size is

    beta = floor(N / (2 t n)),

so each scalar input occupies approximately t*n complex slots.

For a 12-bit LUT (degree 4095), the paper's relevant equal-factor configurations are:
- t=2, n=64: 128 slots/input;
- t=3, n=16: 48 slots/input;
- t=4, n=8: 32 slots/input.

These are source-backed by the factor-capacity equation and the reported 12-to-12 batch sizes.

## Why B145 compounds this slot cost

In B145, a 256-bit arithmetic message with B=64 has

    u = ceil(256/6) = 43

independent adjacent windows. Each window is a separate LUT input and must retain its own output for the prefix scan.

The direct 2368-style route keeps one window per slot (plus padding). It fits the 43 positions comfortably within the slot interval already available to a 256-bit arithmetic message.

Applying SWIFT separately to all windows would require approximately:

- t=2: 43*128 = 5504 slots/message;
- t=3: 43*48 = 2064 slots/message;
- t=4: 43*32 = 1376 slots/message.

At N=2^16 there are N/2=32768 complex slots, giving at most roughly:
- 5 messages/ciphertext for t=2;
- 15 for t=3;
- 23 for t=4.

By contrast, 2026/1869's N=2^16 arithmetic representation at n=256 packs 256 messages/ciphertext.

Thus the matched-throughput loss is about:
- 51x for t=2;
- 17x for t=3;
- 11x for t=4.

This is before accounting for B145's multiple output functions.

## Multi-output cost

SWIFT's ExpBTS/factor generation and tensor factors can in principle be reused for several target trigonometric polynomials on the same window, but each target has its own coefficient contraction. Unlike AKP-style MVB, this contraction includes ciphertext-ciphertext products for t>=2.

B145 needs a carry state and six bit/correction outputs. Some outputs can be algebraically derived from others, but this does not repair the fundamental per-window slot expansion above.

## Latency caveat

SWIFT is still a valid latency Pareto point for small batches:
- its paper reports strong 12-to-12 LUT latency at moderate batch sizes;
- for a workload containing only a few arithmetic messages, sacrificing SIMD occupancy may be acceptable.

But 1869's representation-conversion result is explicitly a SIMD packed construction. A backend that cuts the number of packed 256-bit messages from 256 to 5-23 cannot be called a matched improvement without a separate low-batch objective.

## Decision

- SWIFT as B145 primary/matched-throughput backend: FAIL.
- Reason: slot expansion applies per radix window and compounds with u=43 windows/message.
- SWIFT as small-batch latency variant: potentially useful but secondary.
- No Codex/native work.

The primary B145 path remains the 2368-style direct B^2 root/MVB, which evaluates each window in place and preserves the packed arithmetic-message layout.

## Next

The remaining desirable optimization is an **in-place** reduction of the 4096-point LUT cost: no extra root production and no per-window slot replication.

The most relevant source is ePrint 2026/1026, "Sparse Hermite Interpolation Method for Discrete-CKKS Functional Bootstrapping", explicitly cited by SWIFT as a sparse-frequency direction.

Before any native work, audit whether B145's needed LUT family has exploitable sparse Hermite support when considered jointly.
