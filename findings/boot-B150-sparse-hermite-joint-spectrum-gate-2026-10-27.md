# BOOT-B150 — Sparse-Hermite value gate for the B145 4096-point multi-output LUT

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B149
- Target source: ePrint 2026/1026, "Sparse Hermite Interpolation Method for Discrete-CKKS Functional Bootstrapping"
- Status: SOURCE_GATED_1026 / JOINT_SPECTRAL_DENSITY_LOW_UPSIDE
- CODEX_REQUIRED: NO

## Source status

The full 2026/1026 paper is not currently available:
- official ePrint PDF returns HTTP 403;
- no exact-title arXiv copy was found;
- fixed ePrint GitHub mirror does not contain the PDF;
- no obvious author implementation repository was located.

Therefore this round does not claim the exact algorithm or complexity of 2026/1026.

## Exact Fourier-support audit of the B145 bit outputs

Let B=64, W=B^2=4096, w=Bb+c with b,c in Z_64.

For each output bit k=0,...,5 define

    F_k(w) = bit_k(b).

As a function of b on Z_64, bit_k has nonzero discrete Fourier frequencies only at:
- DC, and
- odd multiples of 2^(5-k).

There are 2^k nonzero non-DC residues modulo 64.

Lifting the block-constant function from b to w=Bb+c expands every nonzero residue modulo B to all B frequencies with that residue class modulo B; the residue-zero component survives only at frequency 0 because the length-B c-sum cancels the other multiples of B.

Hence the exact W-point DFT support size is

    |supp(F_k)| = 1 + B*2^k.

For B=64:
- k=0: 65
- k=1: 129
- k=2: 257
- k=3: 513
- k=4: 1025
- k=5: 2049.

The nonzero residue classes contributed by k=0,...,5 partition all nonzero residues modulo 64 according to their 2-adic valuation. Therefore

    |union_k supp(F_k)| = W-B+1 = 4033.

So the six Boolean output bits jointly require 4033 of the 4096 ordinary Fourier frequencies.

For the c-side range test

    L(c)=1[c<32],

the W-point support has only 33 frequencies (the DC component plus the nonzero odd multiples of B), so this one function is highly sparse. But the six bit outputs dominate the joint support.

## Implication

If sparse-Hermite acceleration mainly reduces the shared power basis by exploiting a sparse union of active Fourier frequencies, the complete six-bit A2B output family leaves little room: 4033/4096 frequencies are already required at the value-interpolation level before adding Hermite derivative constraints.

This is not a theorem that 2026/1026 cannot help:
- its sparse Hermite construction may use a different basis;
- it may exploit approximate rather than exact support;
- derivative constraints and numerical optimization can change the concrete evaluation circuit.

But the exact value spectrum gives a strong prior that the full six-bit multi-output family is not globally sparse.

## Decision

- 2026/1026 remains useful to audit when supplied.
- It is no longer a blocking prerequisite for B145.
- Do not delay the primary B145 evaluation solely waiting for sparse-Hermite.
- Expected gain from a shared sparse-frequency basis for all six bits: LOW based on exact joint spectral density.

The better immediate optimization is to reduce redundant output LUTs algebraically, addressed in B151.
