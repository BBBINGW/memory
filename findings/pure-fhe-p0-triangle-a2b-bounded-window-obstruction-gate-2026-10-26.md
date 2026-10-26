# PURE-FHE P0-PRESCOUT-18 — Triangle A2B Bounded-Window Obstruction Gate

Date: 2026-10-26 (Asia/Hong_Kong)
TRACK_ID: PURE-FHE
PREVIOUS: P0-PRESCOUT-17
SCOPE: no writes to other tracks, no Codex
STATUS: FAIL_BOUNDED_WINDOW_A2B
RESULT: PASS_ALGEBRAIC_LOCALITY_OBSTRUCTION
NOVELTY: NOT_ESTABLISHED

## [FACT] Primary source / prior art

Gao–Zheng, "FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext", CRYPTO 2026, https://eprint.iacr.org/2026/233 ; user-accessible GitHub Notes cached paper SHA256 f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92 (mirror version VERSION_UNVERIFIED). Original extracted PDF physical pp15–16, Def.10–11/Theorem 1: triangle representation f=Δ(I+t^{-1}[m]_t)+e in real algebra R[X]/(X^n−X+2), with t=X−2, bit polynomial [m]_t=Σ b_i X^i and integer-coefficient overflow I. Decode multiplies by t, rounds the *coefficients* before evaluating X=2 mod 2^n. Original pp21–23 §5.2: A2B extracts blocks with D-CKKS.LUT then subtracts lower-bit contribution; O(n/w) iterations per ciphertext, amortized across n/w ciphertexts. p30 §9 open question asks for O(1) without amortization.

Author blog https://ckks.org/blog/2026/fhe-simd-alu/ (dated July 27, 2026) explicitly says more direct A2B conversion methods will be discussed separately. Seoul National University June 11 2026 seminar page https://cse.snu.ac.kr/en/community/seminar/1126 mentions 2–3 bootstrapping for refreshing/conversion and some new results in preparation; insufficient details to claim new direct conversion exists, but strong unpublished-prior-art warning.

## [SPECULATION] One primary H18 and cheapest decisive test

H18: Given normalized, correctly rounded integral coefficient vector Y=tI+[m]_t, and a small bounded overflow (in particular I_i ∈{0,1}), each desired bit b_j can be recovered using *only* the fixed-radius window Y_{j-r},...,Y_{j+r} for a constant r independent of word width n. Local linear preprocessing followed by arbitrary local nonlinear LUT is included as a special case.

Define coefficient order in Z[X]/(X^n−X+2). Choose integers 1≤l≤j≤u≤n−2, let W=[l,u], for example l=j-r,u=j+r. Compare states:
 A: m_A=0, I_A=0; hence Y_A=0 and b_j(A)=0.
 B: [m_B]_t=Σ_{k=l}^{u}X^k, I_B=Σ_{k=l−1}^{u}X^k. All coefficients of I_B are in {0,1}.
 Then Y_B=(X−2)I_B+[m_B]_t=−2X^{l−1}+X^{u+1}.
 Therefore for every k∈[l,u], Y_B,k=Y_A,k=0, yet b_j(B)=1 and b_j(A)=0.
 Thus no function, even arbitrarily nonlinear, of this entire window can recover bit b_j in both cases. This is strictly stronger than P0-17's single-coefficient collision.
 Example n=8, j=3, r=1: I_B=X+X²+X³+X⁴, [m_B]_t=X²+X³+X⁴, Y_B=−2X+X^5; coefficients Y2,Y3,Y4 are all zero; b3(B)=1, b3(A)=0; m_B=28.
 Strong example n=8, W=[1,6]: I_B=1+X+...+X^6, [m_B]_t=X+...+X^6, Y_B=−2+X^7. Six of eight coefficients match all-zero Y_A even though the message bits b1..b6 differ.
 Correctness checked with deterministic Python for all 129 interior windows at n=4,8,16; all test cases passed. This is a mathematical model of accepted *formal encoding states*, not a proof that each tuple is reachable from a particular ciphertext sampler or workload. Not a cryptographic attack.

## [DERIVATION] Exact nonlocal recovery exists algebraically

Because the quotient polynomial f(X)=X^n−X+2 satisfies f(2)=2^n, and t(2)=0, evaluation at X=2 mod 2^n yields Y(2)≡m mod 2^n.
For integers Y0,...,Y_{n−1} as coefficients of Y, each bit j is
 b_j = floor( ( ( Σ_{i=0}^j 2^i Y_i ) mod 2^{j+1} ) / 2^j )
using least nonnegative residue. This identity is exact, even for general integer I, but requires nonlocal prefix-weighted sums and a different modulus per target bit. It does NOT constitute a cheap FHE implementation: coefficients need noise-certified rounding, weights up to 2^j create range/precision burdens, different per-slot modular reductions and output layout cost real work.
There is no information-theoretic impossibility of nonamortized A2B from the entire vector. The proven obstruction applies ONLY to fixed neighborhoods not touching all necessary boundary information; global mixing / suitable LUT / other encoding may work.

## [FACT] Adjacent prior work and novelty boundary

- Gao–Zheng's actual A2B uses bit-block iteration, corrective subtraction, and across-ciphertext amortization; local-window cleanup is ruled out in the formal algebra, without comparing speed.
- REFHE already describes algebraic carry constraints, source references in Gao–Zheng pp5–6. CPL / improved Radix-based CKKS ePrint 2025/1740 uses O(log n) bootstrapped carry in its own layout; source mirror SHA256 f2ff530c44b44c35af56e201c1828d03c8e06c02dfe1abc572607a6de28ab912, version not independently authenticated. https://eprint.iacr.org/2025/1740
- SNU seminar claims are unpublished-idea risk, not verified source code or proof.

## Decision / cheapest next gate

Reject bounded-window A2B under generic bounded coefficientwise overflow, rather than allocating Codex. The nonlocal weighted-prefix formula is a mathematical restatement of decoding and not a new FHE mechanism. Before any native work, check whether a GLOBAL linear transform plus a *single* ordinary discrete CKKS LUT can implement all heterogenous powers-of-two modular reductions without exponential precision/modulus/key requirements. Search new author versions / releases first due to possible announced new direct methods.
NEXT_TEST: GLOBAL_PREFIX_MODULAR_PRECISION_COST_GATE
CODEX: NOT_RUN
STATE_UPDATE: YES, one isolated Pure FHE finding, no STATE.md mutation.
OTHER_TRACKS: UNCHANGED.
