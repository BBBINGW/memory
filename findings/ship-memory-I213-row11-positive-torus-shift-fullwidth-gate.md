# SHIP I213 — Full-width modular gate for HMux row11 positive torus shift

**Date:** 2026-10-14. **Independent SHIP iteration I213** following I212; separate from concurrently active vFHE global STATE. Read START_RESEARCH_SESSION, RESEARCH_PHILOSOPHY, AGENT, global STATE (read-only), independent ship-memory-STATE (I212, SHA 633af110e71537694053d5d3a18c40a515e1ee2c), I212 finding and row10 failure archive before this change. No upstream edits.

## Source provenance [FACT]

Parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / ePrint 2025/784. Prior PDF mirror VERSION_UNVERIFIED. Verified independent third-party Poulpy source (NOT authors' HEaaN) at `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob 8be6ab92846168330100efeabe9fa19dbd9720e4: HMux GGLWE encrypts input `(beta*s,beta)` under target `t_g=sigma_(g^-1)(s)` with dnum=12,kaux=52 when raised_k=624, radix52,dsize1.
- `poulpy-core/src/reference/encryption/gglwe.rs` blob 499c7b22daace7b74428d945a5ba5fca808a07d0: input col1 row11 encrypts beta in limb11.
- `poulpy-core/src/layouts/mod.rs` blob c1e953bed001d3129188f4c0c5d35073a82ee59d: key physical k676, 13 limbs.
- `poulpy-hal/src/layouts/encoding.rs` blob c24822746b5a252bcb177207e005e6148ac33e6f: fractional torus equals sum of limb digits × 2^(-52j).
- `poulpy-hal/src/api/vec_znx.rs` blob 01bca5331f68db07dd03fd2cc312524a354cf44f: **out-of-place** vec_znx_normalize permits signed res_offset and source/destination size change. In-place normalize_assign has different restrictions. Candidate positive offset +40 not yet compiled.

## ONE hypothesis / ONE decisive test

**H213:** Extracting beta from the *last* HMux row11 with public `sigma_g`, torus multiply by POSITIVE integer `2^40`, then separately normalizing the two GLWE components from 13 to 12 limbs (kout624) can produce a valid scale40 beta ciphertext even with full-width uniform RLWE masks and modulo1 carries. Falsifier: one exact N16 source-shaped modular sample beta0 or beta1 with target-scale integer residual substantially above the unavoidable coefficient-rounding bound.

## Exact derivation [DERIVED]

Source 13 radix52 limbs have fractional grid Q=2^624 and row11 beta plaintext fractional beta×2^-572, i.e. integer residue M=beta×2^52. Destination 12 limbs have fractional grid Qout=2^572 and scale40 target integer beta×2^40, fractional beta×2^-532. After sigma_g, ciphertext decrypts under dense s to row11 beta (plus error). Positive torus integer multiplication by 2^40 maps 2^-572 to 2^-532. On centered integer component lifts, combined conversion is `C(x)=round(x/2^12) mod Qout` because source-to-target fractional quantization drops 52 bits while torus multiplier adds 40 bits.

This is NOT I212's illegal negative torus shift: an unknown modular carry kQ becomes k×2^612 after conversion and vanishes modulo Qout=2^572. Thus full-modulus wrap does not create the prior catastrophic k×2^560 term. Individual component rounding remains and may contribute at most approximately `(1+||s||_1)/2 + ||e||_infty/4096` output integer coefficient units. For the test secret s=X+X^2 with norm1=2 and error ≤19, that bound is ~1.50464. For actual dense N16384 secret the norm may be much larger: NOT proved safe there.

## [EXECUTED] one deterministic full-width RLWE test

- Ring Z[X]/(X^16+1), `s=X+X^2`, `g=13,g^-1=5 mod32`, `t_g=sigma_5(s)`.
- Uniform independent mask coefficients `a_i←[0,2^624)`; e coefficients sampled from [-19,19]; source `b=beta 2^52 +e-a*t_g (mod Q)`. Assert original decryption modulo Q. Apply sigma13 to BOTH components and assert decryption under s modulo Q. Independently round the two centered residues by division 4096 to destination Qout, decrypt, and compare against beta2^40.
- Fixed seed 21320261014, 64 samples per beta, **128/128** have maximum target integer coefficient error ≤1. Found **494 nonzero modular wrap coefficients** in lifted source equations. Max coefficient error1 for both beta0 and beta1, corresponding to 2^-40 decoded; maximum source noise contribution 19/4096 target integer units. Results are deterministic sampled examples plus an algebraic carry cancellation explanation, NOT a statistical production FHE success theorem.
- Script: `/mnt/data/ship_i213_row11_positive_shift_gate.py` SHA256 `a205f018dae712940bcf25f10fb2392b80f63d8937bd1749e625b84e09c53b59`.
- JSON: `/mnt/data/ship_i213_row11_positive_shift_results.json` SHA256 `951e39cc7a2f327fd737d82aad07c9cd7080d336e9f46266afd97bd555198bce`.

## Result and next

**STATUS: PASS** narrowly for exact modular small-ring row11 conversion / FAIL claim that I212's modular-wrap obstruction kills all publicly rescaled gadget rows. **UNCLEAR** source Rust/IFMA positive-offset normalization, real CKKS scale metadata, dense N16384 rounding/FFT/NTT/noise, joint augmented eval-key KDM security (I210), latency, real RSS, keygen peak, novelty. **NOVELTY NOT VERIFIED**. This repairs only the I212 row10 extraction problem, NOT SHIP correctness or the entire I207 candidate. The I207 81.45% prepared payload remains CONDITIONAL and I206 ~480 added ct×ct and 4 serial levels still burden performance.

**NEXT_ACTION:** HUMAN_REVIEW / real-runner gate. Test ONE authentic pinned-Poulpy in-crate `row11; sigma_g; out-of-place normalize(offset=+40,k=624); stamp CKKS scale40; ckks_prepare_right` on N16384 source-generated keys, decrypt under s, measure coefficient and slot errors before any full mux gate. Require explicit PI handling of unproven joint eval-key security; do not repeat more low-value ideal toy simulations in lieu of compilation. No modifications to global vFHE STATE or upstream source.
**STATE_UPDATE: YES**, independent ship-memory-STATE only.
