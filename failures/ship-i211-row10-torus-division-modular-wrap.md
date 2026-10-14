# Failure archive — I211 row10 negative torus shift cannot extract a general CKKS selector

**Date:** 2026-10-14. **Track:** SHIP independent I212 (not global I; vFHE STATE unaffected). Detailed proof, source and executed reproducibility in `findings/ship-memory-I212-fullwidth-modular-wrap-falsifier.md`; this file is the concise failure register. Former I211 source-limb bounded-mask PASS is **superseded on general correctness**.

**Primary hypothesis killed:** With Poulpy radix52, source HMux row10 from dnum12/kaux52 key (k676), public `σ_g` followed by `res_offset=-12` torus componentwise normalization to k624 produces a valid scale40 CKKS `Enc_s(β)` under full-width RLWE masks.

**Precise falsifier [DERIVED + EXECUTED]:** Source ciphertext correctness is `b+as=M+e (mod 1)`, but signed componentwise division by 4096 is NOT well-defined on `R/Z`: if lifted relation `b+as=M+e+k`, the destination includes `k/4096` (not 0 mod1). Exact N16 standard negacyclic model, uniformly generated 624-bit torus mask coefficients and noise ≤19, seed 21220261014, β0/1 (10 tests) all miss the ≤2 target coefficient-unit bound. At first β0 trial coefficient6, k=+1 creates error `2^560+O(3)` destination integer units, torus ≈`2^-12`, compared with a 40-bit CKKS target. Original source key is correct; our publicly proposed normalization fails. All errors after removing `k2^560` are ≤3 integer units.

**Source:** Independent Poulpy pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`: `poulpy-core/src/reference/encryption/gglwe.rs`, `poulpy-core/src/layouts/mod.rs`, `poulpy-hal/src/layouts/encoding.rs`, `poulpy-hal/src/api/vec_znx.rs`. Scientific parent SHIP EUROCRYPT 2025 / ePrint 2025/784, no error claimed against original SHIP. Actual full-size Rust backend/IFMA unexecuted.

**Local artifact:** `/mnt/data/ship_i212_fullwidth_torus_wrap_gate.py` SHA256 `64ca0486f85df973643341c8ca22cb3f8c24db9f8bfed8b66ee69d740d8f7552`; JSON SHA256 `ced7491358189a95dd599f1a9ff029cb87fa884ce0f642c5642be4382a3b55fc`.

**STATUS:** FAIL this row10 public division. **UNCLEAR:** row11 with integer torus multiplication by `2^40` (a genuine endomorphism) and source full error; overall I207 key-sharing security, payload, latency. No general impossibility for other rows or encrypted selector representations.

**NEXT_TEST:** PI continuation can falsify the distinct row11 positive-power-of-two public conversion under full-width masks and real source-noise bounds, one test. No generic cyclic/KDM theorem proven; not yet a viable optimization. **STATE_UPDATE:** YES independent SHIP only, no global `STATE.md` change.
