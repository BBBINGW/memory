# SHIP I214 — Pinned IFMA normalization source-contract gate and real-Rust integration blocker

**Date:** 2026-10-14 Asia/Tokyo. **Track:** Independent SHIP key-memory workstream, immediately after I213, separate from concurrently active vFHE global state (global I192 frozen). Read BEFORE write: START_RESEARCH_SESSION, RESEARCH_PHILOSOPHY, AGENT, shared global STATE (vFHE V17; read only), independent findings/ship-memory-STATE.md I213 SHA `3aabc653e6f69164362b1f5f21d0e041ea94ea7a`, and I213 finding. The PI said continue. Do not modify global STATE or upstream Poulpy.

## ONE primary hypothesis + minimum decisive source test

**H214:** The specific I213 source-row11 `positive res_offset=+40`, 13 input limbs at radix 52 (physical GGLWE key k676) to 12 destination limbs (CKKS k624) is *not available in pinned Poulpy's AVX512-IFMA HAL* because the IFMA backend either has no signed-offset out-of-place normalization or rejects this radix/size/offset combination.

**Test:** Trace actual pinned IFMA HAL implementation to its normalization kernel and evaluate the documented **branch guards**, without inventing a compiled Rust result. Check exactly `a.size=13, a_base2k=res_base2k=52, res.size=12,res_k=624,res_offset=+40`.

## Source provenance [FACT]

Scientific parent: Cheon–Hanrot–Kim–Stehlé, SHIP, EUROCRYPT 2025, ePrint 2025/784, prior cached PDF VERSION_UNVERIFIED. Source under inspection **independent Poulpy, NOT HEaaN**, pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `hmux_rot_key_encrypt_sk` ~350–415 constructs rank2 input `(beta*s,beta)`, output `sigma_(gal^-1)(s)`, dnum12/kaux52 at k_ct624. `HMuxRotKey::key()` and `gal_el()` public accessors; `ShipKeySet` stored keys and actual beta choice per support are private to crate, so put any key-origin integration experiment **in crate**.
- `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5ba5fca808a07d0`: `row_i=11,col_i=1` encrypts the constant polynomial beta in gadget limb11; `GGLWEBackendRef::at_view(row,col)` gives GLWE rank1 row.
- `poulpy-core/src/layouts/mod.rs` blob `c1e953bed001d3129188f4c0c5d35073a82ee59d`: source key `k_key=dnum*52+kaux=676`, 13 limbs.
- `poulpy-hal/src/api/vec_znx.rs` blob `01bca5331f68db07dd03fd2cc312524a354cf44f`: **out-of-place** `VecZnxNormalize::vec_znx_normalize` permits signed `res_offset`, unlike in-place normalize_assign's constraints, with `res_k<=res.size*res_base2k`.
- `poulpy-cpu-avx512/src/hal_impl.rs`: NTT3x42Ifma Standard `HalVecZnxImpl` invokes `poulpy_cpu_portable::hal_impl_vec_znx_normalize!()`; `poulpy-cpu-avx512/src/ntt3x42_ifma/rayon.rs` separately passes `res_offset` to parallel `vec_znx_normalize_par` using serial kernel.
- `poulpy-cpu-portable/src/hal_defaults/vec_znx.rs` blob `32c2e0e385f26f0984041117da145eb64d1e5102`: default `vec_znx_normalize` forwards signed offset to portable kernel.
- `poulpy-cpu-portable/src/kernels/vec_znx/normalize.rs` (pinned): `vec_znx_normalize_portable` ~102–150 checks `res_k<=res.size*radix`; `normalize_needs_exact` ~36–48 computes `min_offset = (a_bits−a_base2k)−res_bits` for equal bases and chooses exact path only if offset<min_offset or offset≥a_bits; `vec_znx_normalize_range_raw_portable` ~228–374 contains handling for same-base precision drops.
- `poulpy-ckks/src/layouts/ciphertext.rs` blob `929b6f4239d787fec22bb73e251d7a76bf1ad80b`: `set_meta_checked` checks scale/storage against k, not whether true encryption error meets any numerical precision claim.
- `poulpy-ckks/src/reference/mul.rs` blob `783a231eb98b8871107270e2f3354884644bfcfd`: `ckks_prepare_right_reference` transforms source CKKS ciphertext to prepared-right buffer and propagates `log_delta`, precision, slots, layout; `ckks_mul_prepared_assign_reference` still requires a valid tensor key and correct prepared layout. Metadata preservation does not independently certify target plaintext/noise.

## [EXECUTED STATIC ARITHMETIC] HAL compatibility result

For a_size13, base52 => a_bits676. res_size12, base52 => res_bits624. `min_offset=(676−52)−624=0`. `res_k=624<=12*52=624`. Proposed `res_offset=40` lies in `[0,676)`, hence `normalize_needs_exact(13,52,12,52,40)=false`. The pinned equal-radix normalizer has a valid handling branch; IFMA uses the macro implementing that normalizer. This **FAILS H214's missing-op/rejected-parameter assertion** (static supported source contract). It is not a compiled test proving numeric output or metadata compatibility for an actual HMux GLWE view; `RUST_BUILD` environment variables are not a rustc binary.

## [EXECUTED ENVIRONMENT CHECK] Real runner blocked

Local `command -v cargo` and `command -v rustc` empty, no local pinned Poulpy checkout; `git ls-remote https://github.com/poulpy-fhe/poulpy.git HEAD` fails DNS resolution `Could not resolve host: github.com`. `g++` exists, but cannot compile source Rust. GitHub connector supports immutable source reads and repository mutations but **no new workflow_dispatch/run-code executor**; existing CI would not test an unimplemented adapter. No remote CI workflow was modified or triggered. **No compiled FHE ciphertext experiment.**

## One REAL in-crate integration test specification (ready for a runner, not executed)

Use `poulpy-ckks/src/test_suite/ship.rs` or an in-crate test module so `pub(crate)` keys, helper and backend GLWE rows are visible:
1. Fixed `ShipPlan(log_n14,h32,theta4,window256,mux_base4,ld40,budget_out104)`, `base2k52`, candidate `raised_k624` MUST be explicitly configured in the modified plan/test fixture (source unmodified `ShipPlan::raised_k` still computes **468**, so do not accidentally test original 468). Prefer direct `hmux_rot_key_encrypt_sk(...,k_ct=624)` to avoid generating the 480-key bundle just for one test; it generates one ~156 MiB raw rank2 GGLWE key. Use source-generated rank1 dense GLWE secret; test beta0 and beta1 at nontrivial `rot`, with separate valid source RNG streams.
2. Access raw unprepared KSK `key()`, GGLWE input **col1 / row11**, prepare source GLWE view and publicly apply the exact `gal_el()` automorphism to BOTH `b,a` components under target dense secret; no actual secret used in conversion.
3. Allocate CKKS target rank1 `n=16384,k624,base2k52` (12 limbs). Apply **out-of-place** `module.vec_znx_normalize(&mut dst,res_base2k52,res_k624,res_offset40, col=0 and1, &src,...)`; do not call in-place normalize_assign. Use source-appropriate scratch. Avoid input aliasing.
4. Stamp `log_delta=40`, `SlotsKind::Complex` and `log_sparsity=0` and record effective k. **Do not invent a log_budget noise guarantee from metadata.** Decrypt with the authentic dense secret and check all coefficients/CKKS slots equal beta within a predeclared numerical tolerance (e.g. < 2^-18; also report actual maxima, not just PASS).
5. Call `ckks_prepare_right` and inspect prepared width (expected `N*2*12*16 = 6 MiB` in pinned IFMA CnvPVecR) and `log_delta=40`/effective k624; check prepare-layout errors separately. If all pass, check **one** actual CKKS prepared multiplication with an independently encrypted plaintext-controlled test operand using widened tensor key; compare with expected beta*x. Only after this would full mux pipeline / timing be warranted.
6. If this actual source test cannot run, status remains **IMPLEMENTATION BLOCKED**, not hypothetical PASS. Full security of augmented SHIP + general rotation-key joint bundle (I210) is independently OPEN. Candidate I207 8.263GiB/81.45% prepared memory is model-only; I206 ~480 added ct×ct and 4 serial levels, peak keygen memory and latency unmeasured. Original SHIP not attacked.

## Additional integration obstruction — ShipPlan cannot express k624 for the original output target [FACT/DERIVED]

The **original**, unmodified `ShipPlan::raised_k(base2k)` in pinned `poulpy-ckks/src/layouts/ship/plan.rs` is defined as
`round_up_52((tree_depth+2)*ld+log_budget_out)`. With `tree_depth=6,ld=40,log_budget_out=104`, it remains `round_up_52(424)=468`, while I206's extra four serial 40-bit selector multiplications require `k>=624` (52-bit limb aligned) to retain ≥104 at the root. The actual `ShipKeySet::generate`, `prepare`, and `bootstrap` derive key layout, mask width and pipeline scratch from **`plan.raised_k`**, so merely allocating a k624 output/selector ciphertext does NOT turn the original source plan into the widened candidate.

A superficial workaround would raise `log_budget_out` to `264`, since `round_up_52(320+264)=624`; but that field semantically means **desired final output budget**, while the new candidate's modeled root is only `144` after the four extra multiply levels, so this silently misstates the plan's output-budget contract. A valid integration should add an explicit extra-mux-multiplication depth or widened-modulus field that preserves `log_budget_out=104`, or construct a clearly isolated test fixture with direct `hmux_rot_key_encrypt_sk(k_ct=624)` independent of the ordinary SHIP plan. The full pipeline needs coherent widened key shapes, masking layouts, tensor keys, checks and a controlled baseline comparison. This is a **source-level non-drop-in implementation obstacle**, not a proof that the proposed design is impossible or insecure.

Note `poulpy-ckks/src/reference/ship/bootstrap.rs` checks output capacity ≥plan.raised_k but uses the same `kk` for intermediate leaf allocation and product tree, so changing only an output buffer does not suffice.

## End of iteration

**STATUS: FAIL H214** hypothesis that IFMA out-of-place positive-offset normalization cannot accept the needed size/radix/offset, based on pinned source. **PASS source-contract compatibility only. HUMAN_REVIEW/IMPLEMENTATION BLOCKED** for an authentic compilation, source-generated ciphertext/noise check and CKKS prepared multiplication. **NOVELTY NOT VERIFIED**.
**RESULT:** One lower-level IFMA API blocker ruled out, but the original SHIP plan's k468 construction is a separate verified **non-drop-in parameter/interface obstruction** for the widened k624 candidate. Larger cryptographic/cost problem unchanged.
**NEXT_ACTION:** Do NOT fabricate another toy round. Run the above one actual pinned-Rust test when a runner/checkout is available (PI must approve any GitHub infrastructure or implementation changes), or PARK the HMux branch for now. No global vFHE STATE edit.
**STATE_UPDATE: YES** independent SHIP source-contract checkpoint only.
