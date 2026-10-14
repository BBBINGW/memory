# SHIP-M04 — Source-grounded early-conjugation GGLWE noise falsifier

**Date:** 2026-10-14 (Asia/Tokyo).
**Series:** independent SHIP-M04, **NOT** any vFHE I-series iteration. PI said “好的，请继续” after M03.
**Primary target:** prepared evaluation-key selector memory of Cheon–Hanrot–Kim–Stehlé, SHIP ePrint **2025/784**, original §3.3 and §4.4; source mirror PDF 33 pp SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official VERSION_UNVERIFIED.
**STATUS:** PASS *very narrow necessary* source-layout truncated-Gaussian + exact-algebraic-key-switch + output-rounding noise gate; **UNCLEAR** real backend correctness, full CKKS precision, source HEaaN, runtime, RAM, and novelty. No security claims.

## Read before write / prior findings

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, independent `findings/ship-memory-STATE.md` (SHA `3ad56557d97ec38fc7168709cfe1041e6283fd8d`), `findings/ship-memory-M03-toy-rlwe-early-conjugation-noise.md` (SHA `6598e09e9356a06b7e9ed74f9b5eb3da44fb03d3`), global vFHE `STATE.md` only for concurrency check (it was vFHE I195, SHA `8198c8e183b52c937bc564d7a4328d893d382f74`). Earlier SHIP findings M01–M03 are preserved. No changes to shared `STATE.md`.

Previous M01 establishes ideal pair-packing formula `F=(U+Conj(V))/2`; M02 locates available dense-key conjugation automorphism key and the early mask output width `k_mask=raised_k-log_delta`; M03 toy N16 encrypted ciphertext experiment showed non-negligible noise for a **different**, unguarded radix-64 low-precision gadget key. That toy noise is NOT source-Poulpy noise.

## ONE hypothesis and ONE decisive technical test

**[PRIMARY HYPOTHESIS, falsification framing]** At the illustrative, source-compatible Poulpy SHIP plan `N=16384,h=32,θ=4,base2k=52,log_delta=40,log_budget_out=104,dsize=1`, the *fresh GGLWE key-encryption error and mandatory ideal output normalization-rounding noise ALONE* of an extra early conjugation would already exhaust a nominal 18.1-bit SHIP output error budget after the h-product tree; thus source-precision early conjugation cannot support the packed-selector candidate even if all other arithmetic were exact.

**[ONE MINIMAL FALSIFIER]** Read the exact pinned GGLWE/Galois key shape and error-support law, derive a coefficient-wise worst-case key-switch + normalization bound and lift it through slot embedding, mask reconstruction, h-fold product tree (ideal bounded factors). If a valid conservative upper bound is *much below* the nominal output tolerance, falsify **this narrow unavoidable-noise bottleneck hypothesis**. Do not claim the converse (a crude upper bound > tolerance would not prove actual failure).

## Source provenance / factual contracts (pinned independent Poulpy, NOT authors' HEaaN)

Repository: `poulpy-fhe/poulpy` commit `250d4392656cd313f92ca66d96d8865702d39ddf`.

- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: `raised_k=roundUp(((tree_depth+2)*log_delta_work+log_budget_out),base2k)`; `tree_depth=ceil(log2(h+1))`.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`: standard masked plaintext product scale `ld`, effective `k_mask=raised_k-ld` under the cited model; uses DFT-domain accumulation then normalization.
- `poulpy-ckks/src/test_suite/mod.rs` blob `e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb`: `CKKSTestParams::atk_layout` sets `dnum=ceil(raised_k/(dsize*base2k))` and `k_aux=dsize*base2k+log2(N)`.
- `poulpy-core/src/layouts/gglwe.rs` blob `37fd5350861393263c6b10bd827ad40a67d1a622`: **total GGLWE key precision** `key.k=dnum*dsize*base2k+k_aux`, not just gadget precision. A k-bit ciphertext uses only the live input digit limbs. This is an auxiliary-guard layout.
- `poulpy-core/src/reference/encryption/glwe_automorphism_key.rs` blob `b584a17659347200c3fb8da8653f33f0a776ed8c`: key is a GGLWE encryption of the **inverse-automorphized secret**; `gglwe_encrypt_sk` is invoked for every automorphism key, `p=-1` existing in SHIP.
- `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5ba5fca808a07d0`: per-rank, per-gadget-row independent GLWE encryption, plaintext gadget shift by `(dsize-1)+row*dsize`, uses `glwe_encrypt_sk_internal`; source keys at `key.k` precision.
- `poulpy-core/src/reference/encryption/glwe.rs` blob `8caec305a9412fa769bf36ccea122cbeae3bd697`: `glwe_encrypt_sk_internal` injects `Noise::ENCRYPTION` into body via `vec_znx_add_noise(base2k,k,...)`, so error coefficients live on that **key.k integer grid**.
- `poulpy-core/src/noise_distribution.rs` blob `e231917a72be54a5e8dca47ece9f7d8672828020`: `Noise::ENCRYPTION=Gaussian{sigma:3.2}` truncated to `|e| <= floor(6*sigma)=19` as support bound. No probability tail estimates required *for this source sampling distribution*.
- `poulpy-core/src/reference/keyswitching/glwe.rs`: mask limbs contribute digit-wise matrix products; output `vec_znx_idft_normalize_consume` to destination torus width, source says limb window covers carry growth.
- `poulpy-core/src/reference/automorphism/glwe.rs` blob `436e883662d4518b245edae6e739bb7c7865f22e`: the default automorphism first GLWE-keyswitches then permutes; Galois automorphism is coefficient-norm-preserving (up to sign/reordering).
- `poulpy-ckks/src/reference/conjugate.rs` blob `4eb738484cb542cdea2a7ca2357182bd4295c5dd`: `ckks_conjugate_into` metadata stays at same k/scale when offset=0, but actual error not tracked.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: existing root conjugation AFTER product tree, proposed early conjugation BEFORE mux and product tree.

Source key layout is corroborated by public https://github.com/poulpy-fhe/poulpy/blob/main/poulpy-ckks/README.md under “Evaluation Keys and k_aux”; that main-branch document is explanatory only, pinned code above is authoritative.

## Test derivation and explicit assumptions

**Shape [FACT + source-derived]:**
```
N=2^14, h=32, theta=4, base2k=52, log_delta=40,
log_budget_out=104, dsize=1, tree_depth=6.
raised_k=468 bits; masking output k_mask=428 bits.
D=ceil(raised_k/52)=9 gadget rows. Actual mask has <=ceil(428/52)=9 live radix-52 limbs.
k_aux = 52 + log2(N) = 66 bits.
key.k = D*52 + 66 = 534 bits.
```

**[DERIVATION, IDEAL algebra]** Take the key sample errors `e_i(X)` with integer coefficient norm <=19 at torus grid `2^-534`. Treat mask limb digits `d_i(X)` conservatively as polynomials in `Z[X]/(X^N+1)` with coefficient absolute values <= `2^52` (even allowing unsigned limbs). For rank1, the key-switch component attributable *solely* to key sample errors is
```
  e_KS(X) = sum_{i=0}^{D-1} d_i(X) * e_i(X) * 2^(-534).
```
Since a negacyclic coefficient is the sum of at most N products, by triangle inequality,
```
  ||e_KS||_infty <= N * D * 2^52 * 19 * 2^(-534).
```
**[ASSUMPTION]** The integer gadget products, DFT/IDFT and carry propagation are exact, and output normalization is ideal nearest-integer rounding to k_mask=428 bits. Each output ciphertext polynomial is rounded by at most `2^(-429)` in torus coefficient units. Decrypting with a secret satisfying `||s||_1 <= N` yields an additional coefficient term bounded by
```
  e_round_coeff <= (1+N) * 2^(-429).
```
(This is deliberately more conservative than e.g. dense key h=192; the output under the proper secret adds one rounded mask polynomial product.)

Evaluate a ring polynomial at an odd 2N-th root: coefficient-to-slot amplification has operator-norm at most N under coefficient infinity norm. Divide torus by scale `2^(-40)` to express **message-level CKKS slot error**:
```
  kappa <= 2^40 * N *
       [N * D * 2^52 * 19 * 2^(-534)
        + (1+N)*2^(-429)] .
```
The packed selector leaf has one half of this added error, `delta_leaf<=kappa/2`. For `h=32` ideal factors satisfying `|f_j|<=1`, the product-tree perturbation and final real extraction can be bounded:
```
  eps_final_extra <= 2*((1+kappa/2)^h-1).
```
This bound includes **ONLY** sampled GGLWE encryption error + nearest-grid output rounding, propagated by ideal multiplications. It excludes *all* backend rounding, existing mask/CKKS encoding noise, extra public-reencoding error, mux key switching noise and its interaction with the new error, correlations, the final bootstrap's inherent phase approximation, and other implementation behavior. The `|f_j|<=1` assumption is satisfied by the ideal SHIP phase factors, not a proven bound on approximate encrypted leaves at finite precision.

**[NUMERIC TEST EXECUTED]** Local script `/mnt/data/ship_m04_source_noise_bound.py`, SHA256 `f589cb2fe2608635a57830a87faa2f1133a16e532721c7f7abb32399883642b5`; JSON `/mnt/data/ship_m04_source_noise_bound.json`, SHA256 `506733c31ca28a4fc42c74ac7c4c364f7361f3542d94d71125a43104469c7726`. Python `decimal` 190-digit arithmetic, uses exact binomial rather than float cancellation.
```
coeff_KS_error_torus_bound       = 2.2436656531132269e-139
coeff_norm_round_torus_bound    = 1.1818933957220256e-125
message_slot_kappa_bound        = 2.1291098626261863e-109  ~ 2^(-361.00)
added_packed_leaf_error         = kappa/2            ~ 2^(-362.00)
end_to_end_extra_pessimistic    = 6.8131515604037963e-108 ~ 2^(-356.00)
nominal output tolerance        = 2^(-18.1) = 3.5592384e-6
bound / tolerance               = 1.91421613046e-102
nominal margin                  ~ 337.9 bits
```
This is **NOT** evidence the SHIP algorithm achieves 356 bits or even 18 bits in actual execution; it certifies only that these **two narrow noise terms cannot by themselves be a precision bottleneck** under the algebraic assumptions. The enormous gap comes from GGLWE evaluation-key guard precision and is absent from the toy's 74-bit unguarded key. M03's observed ~1e-6 **cannot** be transposed directly to the source key layout.

## Falsification decision and limits

**[FAIL original “these two noise mechanisms alone exhaust target precision” HYPOTHESIS]** A conservative upper bound is ~1e102 times smaller than the *full* nominal 18.1-bit tolerance (using a separate 32-support toy and the paper's HT15 precision only as a **reference error scale**, NOT as measured accuracy of this source shape). Within exact integer torus key switching and ideal k-grid rounding, early conjugation is **not noise-forbidden** by GGLWE fresh-sample errors and output rounding. The observed negative M03 phenomenon is an **unguarded toy-parameter artifact**, not grounds to abandon packed-mask SHIP.

**[UNCLEAR]** Backend FFT/NTT precision and correctness at 534-bit guarded key layout, CKKS packed mask encoding width and numerical transformations, actual Galois key reuse at k=428 on optimized backend, full output error incl mux and product tree, and online h extra Galois operations + two masking accumulator finalizations; no Poulpy/HEaaN run has been performed. Unconditional security/novelty/real peak resident memory also unverified.

## End of SHIP-M04

**STATUS:** **FAIL** primary “sample + ideal normalization noise alone kills early conjugation” claim; **PASS** source-conditioned analytic error-envelope falsifier; **UNCLEAR** actual FHE precision/latency/prepared memory. **NOVELTY NOT VERIFIED**.
**RESULT:** Source GGLWE key has **534-bit** total precision (468-bit gadget +66-bit guard) and truncated coefficient errors |e|<=19 at that precision. Under exact arithmetic and pessimistic digit/rounding/slot norms, h32 output *added* error bound ~2^-356 vs nominal 2^-18.1 tolerance. M03 toy's high noise is not a valid estimate for this key layout. Runtime cost and backend precision now dominate research uncertainty, not ideal evaluation-key sample noise.
**NEXT_ACTION (SHIP-M05, PI only):** ONE **implementation-specific cost/feasibility gate** focused on the **extra per-leaf higher-precision conjugations** and **two DFT accumulator finalizations**: obtain a real Poulpy runner at fixed commit if possible; record packed baseline/variant same-plan selector prepared buffers, max slot error and elapsed masking/conjugation. If no runner, perform ONE pinned-backend asymptotic / concrete operation-count and peak scratch bound and STOP as an estimate; do not claim benchmark. If extra h key switches obviously erase SHIP's low-latency competitiveness even with improved memory, recommend PARK, not auto-pivot.
**STATE_UPDATE:** YES **independent SHIP state only**. Do NOT touch global vFHE `STATE.md` (concurrent changes), I193 or I195.
