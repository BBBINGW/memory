# BOOT-B051 — SIMD ALU A2B prefix-window extraction: integer-overflow alias

**Track:** BOOT  
**Date:** 2026-10-20  
**Status:** `PASS_ZERO_OVERFLOW_PREFIX_IDENTITY / FAIL_INTEGER_LIFT_CORRECTNESS / NO_NEW_PUBLISHABLE_ALGORITHM`  
**State update:** NOT SAVED TO GITHUB (connector write blocked); this file is a local handoff. SHIP remains paused.

## Primary hypothesis

Can the sequential `LUTID` cleanup in the Arithmetic-to-Boolean (A2B) conversion of Gao–Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext* (CRYPTO 2026, ePrint 2026/233), be replaced by a *single public linear finite difference* on the triangular bit representation, followed by simultaneous width-`w` `LUTMSB` evaluation?

## Sources and provenance

- Primary full paper: https://eprint.iacr.org/2026/233 — §5.2, physical pages 21–23, and Theorem 6 on physical page 27. The cached research copy was title-verified, 43 physical pages, PDF SHA-256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`; version status `VERSION_UNVERIFIED`.
- Author implementation: https://github.com/tsinghua-ideal/fhe-simd-alu, default branch `fhe-simd-alu`, file `src/pke/lib/scheme/ckksrns/z-fhe.cpp`, Git blob SHA `8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02`. Lines 391–470 contain sparse A2B; lines 583–800 contain batched A2B, including masked `LUTID`, `LUTMSB`, and scaled subtraction of the recovered lower digits.
- Author explanation (2026-07-27): https://ckks.org/blog/2026/fhe-simd-alu/ — integer overflow `I` in the triangular encoding is retained and the authors explicitly motivate nonlinear bit peeling; the resulting serial operations are amortized over a batch.

## [DERIVATION] Ideal finite-difference identity

For an `n`-bit message `m = sum_i b_i 2^i`, the signed triangle can be normalized to prefix fractions (away from the separately corrected special constant coefficient):

`u_k = sum_(i=0)^k b_i 2^(i-k-1) = 0.b_k b_(k-1)...b_0 (binary)`.

Let `p = 2^w`. For `k >= w`:

`u_k - u_(k-w)/p = sum_(i=k-w+1)^k b_i 2^(i-k-1) = D_k/p`, 

where `D_k` is exactly the `w`-bit word in positions `k-w+1..k`. If all integer overflow coefficients were known to be zero, a public shift/subtraction would isolate these digit windows simultaneously. This is a correct *plaintext* algebraic rearrangement.

## [COUNTEREXAMPLE] Unknown integer overflow aliases the digit

The actual source representation has unknown integral quotient coefficients:

`x_k = I_k + u_k + e_k/Delta`.

Applying the candidate transform gives

`x_k - x_(k-w)/p = D_k/p + I_k - I_(k-w)/p + (e_k - e_(k-w)/p)/Delta`.

The integer `I_k` disappears under a period-1 LUT, but the fraction `-I_(k-w)/p` does not. It changes the apparent `w`-bit digit to `D_k-I_(k-w)` modulo `p`.

**Exact zero-noise alias:** take `w=4`, `p=16`, `k=7`, and `I_7=0`.

- Case A: true 4-bit digit `D=0`, earlier overflow `I_3=0`; transformed input `0 mod 1`, target MSB `0`.
- Case B: true 4-bit digit `D=8`, earlier overflow `I_3=8`; transformed input `(8-8)/16=0 mod 1`, target MSB `1`.

Both overflow values satisfy `|I_3| < 16` (a bound considered in the original construction). The same candidate LUT input would require different outputs. This refutes the public finite-difference + one scalar LUT shortcut, **not** the published sequential algorithm.

The general quotient-lattice obstruction: for a public linear `L` to preserve equivalence `x ~ x+z` for *every* `z` in `Z^n` under a period-1 LUT, one must have `L(Z^n) ⊆ Z^m`, equivalently integral matrix entries. The candidate `Id-(1/p)Shift` is not integral. This scoped result does not exclude a new ciphertext representation or additional nonlinear procedure.

## [VERIFICATION] Exact rational enumeration

Performed with Python `fractions.Fraction` and exhaustive bit strings, with no rounding or encryption:

| Parameters | Tests | Exact digit mismatch | MSB mismatch |
|---|---:|---:|---:|
| `n=8,w=4,I_prev=0` | 1,024 | 0 | 0 |
| `n=8,w=4,I_prev=-15..15` | 31,744 | 30,720 (96.77%) | 51.61% |
| `n=6,w=2,I_prev=-3..3` | 1,792 | 85.71% | 57.14% |
| `n=12,w=4,I_prev=0..15` | 524,288 | 93.75% | 50.00% |

These frequencies refer to *uniform enumeration of toy inputs and overflow values*, **not** to the actual scheme's failure probability, security level or DFR.

## Repair attempts and costs

1. Restricting `I_(k-w)` to multiples of `p` suffices for this identity, but the original `Truncate/ModRaise` bounds the overflow magnitude without ensuring this sublattice property. Establishing it would require a new cryptographic construction and security proof.
2. Removing the unknown integer part of `x_(k-w)` before dividing by `p` restores the digit, but requires a nonlinear homomorphic modular/integer-cleaning operation. The source's `LUTID` is already designed to clean recovered lower bits; the cost has not been removed.
3. Multiplying the proposed difference by `p` yields an integer linear transform `p*x_k-x_(k-w)`, but the target digit then becomes an integer and is erased by an ordinary period-1 LUT. Scaling back revives the same hidden-quotient problem.

Even a successful one-shot extraction would need a fair comparison against the original **batched** A2B, which already amortizes `d=ceil(n/w)` nonlinear operations over `d` ciphertexts. A plaintext-window count is not an end-to-end FHE cost or depth proof.

## End of iteration

**STATUS:** `FAIL_NATIVE_INTEGER_LIFT`  
**RESULT:** The noiseless prefix-difference identity is correct, but the full encrypted interface has an unknown integer-quotient residue that aliases the digit. No source-compatible, noise-safe, lower-cost repair was constructed; no publication claim.  
**NEXT_TEST (B052):** Archive this naive shortcut. Select a different fully sourced Bootstrapping algorithm with a stronger potential for new dataflow or nonlinear primitive (e.g., ePrint 2025/1301 on large LUTs); one primary hypothesis and cheapest decisive test. Keep SHIP paused.  
**STATE_UPDATE:** Pending; connector did not accept writes.

## GitHub archival reconciliation (2026-10-20)
This document was originally created in ChatGPT Library after earlier GitHub Notes connector refused writes; statements above describing the original LOCAL state are historical. This archive copy was subsequently created in the isolated BOOT GitHub Notes repository solely to close the numbered gap. No new B051 hypothesis or test was executed in the archival step. Follow B052 for next technical iteration. SHIP remains paused.
