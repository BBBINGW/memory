# Pure FHE — P0-PRESCOUT-17: Triangle A2B Coefficient-Locality Gate

Date: 2026-10-26 Asia/Hong_Kong
TRACK_ID: PURE-FHE
PREVIOUS: P0-PRESCOUT-16
ACTIVE: fresh structural algorithm scouting
STAGE: P0-PRESCOUT-17

## Sources [FACT]

1. Gao, Mingyu; Zheng, Hongren. *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, CRYPTO 2026, https://eprint.iacr.org/2026/233 ; source mirror ePrint 2026/233 PDF SHA-256 f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92; repository-mirror version unverified. Read physical PDF pp.5–8,26–30. Printed p.30 §9 explicitly asks about O(1) arithmetic-to-boolean conversion bootstrapping *without amortization*. Pp.6–8 describe triangle encoding using t=X−2 in R[X]/(X^n−X+2), and current A2B is iterative, amortized over multiple ciphertexts. Pp.29–30 Table 6 give the implementation workloads. Printed p.30 also notes CPL has O(1) conversion in its different representation/packing regime; this is a *scheme-specific* open problem, not a claim that nobody has O(1) A2B.
2. Gao–Zheng author explanation, https://ckks.org/blog/2026/fhe-simd-alu/ ; it explicitly describes amortized bit extraction, moderate-word non-DFT transform cost, and alternative data layouts.
3. Cha, Park, Lee, *Improved Radix-based Approximate Homomorphic Encryption for Large Integers via Lightweight Bootstrapped Digit Carry*, https://eprint.iacr.org/2025/1740 ; acquired mirror version unverified; read PDF pp1–3 and found O(log k) digit carry and related arithmetic/logic tradeoffs, not a triangle-local correction.
4. 2026/2524 *Homomorphic Encryption for High-precision Arithmetic of Approximate Numbers* and 2026/2600 *High-Precision Bootstrapping for GCKKS* (Ma/Liu/Wang/Wang, posted October 2026) both have publicly discoverable abstracts but FULLTEXT_RETRIEVAL_BLOCKED at eprint (403), arXiv exact-title absent, available mirror absent. Do not allege original full text read or claim an unresolved GCKKS limitation. Relevant abstracts: https://eprint.iacr.asia/2026 . These may need authorized original PDFs in papers/supplied/ for future scrutiny.

## One primary falsifiable hypothesis H17

With noise set to zero, triangle ciphertext encodes F = ΔI + Δ [m]_t/t in the auxiliary real algebra A_n = R[X]/(X^n-X+2), t = X−2, [m]_t = Σ_{j=0}^{n−1} b_j X^j for m=Σ b_j 2^j.

H17: Multiplying by t and normalizing scale yields Y=tF/Δ = tI + [m]_t. A *single coefficientwise* function g_j on Y_j (possibly different functions across j) can recover b_j for every valid m and overflow polynomial I. If true, direct fully parallel independent-coefficient nonlinear cleanup might bypass iterative carries.

## Cheapest decisive test [DERIVATION] — exact 2-message collision

Take any n≥2 (n=4 suffices), zero noise.
Input A: m=0, [m]_t=0, I=1, so Y_A=X−2. Coefficient at X^1 equals 1, desired bit b1=0.
Input B: m=2, [m]_t=X, I=0, so Y_B=X. Coefficient at X^1 equals 1, desired bit b1=1.
Therefore g_1(1) would have to equal both 0 and 1. No map reading only the X^1 coefficient can satisfy H17 for both states. Collision uses bounded small overflow I∈{0,1}; does not require large/noisy or adversarial cryptographic distributions. This is a universal algebraic counterexample for the stated input family, NOT a proof about sampling frequency of these states under a specific encryption algorithm.

The global quotient still retains the message: f(X)=X^n−X+2 satisfies f(2)=2^n; thus evaluation φ(Y)=Y(2) mod2^n is a well-defined quotient homomorphism Z[X]/(f) → Z/2^n. Because t(2)=0, φ(Y)=Σ b_j2^j=m mod2^n. This explains why joint coefficient processing can succeed even though coordinatewise cleanup is impossible. The quotient identity is inherent in the source scheme, not a novel construction.

## Scope and decision

- KILL direct one-shot *coefficientwise* overflow cleanup. It cannot repair the collision even with an arbitrary nonlinear function at each coefficient.
- The no-go does not apply to a single global LUT, multi-coordinate mixing, a different encoding, special structured I restrictions that rule out the pair, nor does it establish a lower bound on constant-number CKKS bootstrapping circuits.
- The paper already amortizes over ciphertexts and CPL has a different O(1) conversion; no novelty established.
- This is a fresh structural research pivot rather than another FFT/Trace/EvalMod scheduling variant.

## End-of-iteration

STATUS: FAIL_COEFFICIENT_LOCAL_A2B_CLEANUP
RESULT: PASS_EXACT_ALGEBRAIC_COLLISION / PASS_QUOTIENT_MESSAGE_INVARIANT
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: A2B_MINIMAL_CROSS_COEFFICIENT_COUPLING_GATE — choose a single low-width triangle word and test a concrete bounded-window linear+nonlinear candidate that uses neighboring coefficients, before any implementation. Compare directly to Gao–Zheng and CPL. Kill if it reproduces existing carry iteration or lacks end-to-end gain.
CODEX: NOT_RUN
STATE_UPDATE: YES — this isolated finding only
OTHER_TRACKS: UNCHANGED
