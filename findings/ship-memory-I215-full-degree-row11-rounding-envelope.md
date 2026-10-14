# SHIP I215 — N=16384 source-parameter row11 normalization error envelope (NO RUST RUN)

**Checkpoint:** 2026-10-14 (Asia/Tokyo). Independent SHIP branch. Earlier post-I214 *runner readiness/task specification* was archived as `findings/ship-memory-row11-real-rust-execution-task.md`, **without incrementing** the independent round number because no crypto claim was tested. This is the **first completed mathematical I215**. Read before write: START_RESEARCH_SESSION, RESEARCH_PHILOSOPHY, AGENT, global STATE (vFHE V17, READ ONLY), `findings/ship-memory-STATE.md` I214 SHA `949917e68aee56c946cc3827e2392517796e88f1`, I213, I214 and existing runner task. **Do not change global vFHE STATE or upstream Poulpy.**

## Primary source [FACT]

Target paper: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784 (prior full paper source version status VERSION_UNVERIFIED). Audited implementation: **third-party independent** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, **NOT original author HEaaN**.
- `poulpy-ckks/src/test_suite/mod.rs` blob `e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb`: `BASE52_PARAMS_F64` has `base2k=52, hw=192`; actual in-crate `gen_sk_with_host` in `poulpy-ckks/src/test_suite/ship.rs` takes `params.hw` into `glwe_secret_fill_ternary_hw`. To test N=16384 with this suite, one explicitly overrides `params.n=16384` and preserves `hw=192`. This is the proposed runner setting, **not a claim about every SHIP parameter selection**.
- `poulpy-ckks/src/test_suite/ship.rs` pinned: helper `gen_sk_with_host` fills dense secret with exactly h nonzero ±1; `ShipPlan` candidate h=32 sparse bottom support is distinct from dense secret hw192.
- `poulpy-core/src/noise_distribution.rs`: `Noise::ENCRYPTION` has `sigma=3.2`; truncated discrete Gaussian integer sample `|e|<=19`. Used for source physical GGLWE key noise (subject to numerical backend effects).
- `poulpy-ckks/src/layouts/ship/keyset.rs`, `poulpy-core/src/reference/encryption/gglwe.rs`, `poulpy-hal/src/layouts/encoding.rs`, `poulpy-hal/src/api/vec_znx.rs`, and I213/I214 source findings: at widened ciphertext k624/base52, raw HMux GGLWE key has 13 limbs/physical k676, input col1 row11 encrypts beta as torus `beta * 2^-572` under `t_g=sigma_(g^-1)(s)`. Public `sigma_g`, positive integer torus multiplier `2^40`, then out-of-place normalization to 12-limb k624 gives expected constant plaintext `beta*2^-532`; output CKKS scale40; **actual Rust adapter still unimplemented**.
- `poulpy-cpu-portable/src/kernels/vec_znx/normalize.rs`: full-precision same-base out-of-place normalization has a valid `res_offset=+40` branch, reused by NTT3x42Ifma HAL. This is **static evidence** of capability, not actual max-error verification.

## ONE primary hypothesis and ONE decisive conservative bound test

**H215 (falsifiable, ideal-coefficient model):** For the **source-test-shaped real dimension N=16384, dense-secret Hamming weight hw=192**, the I213 row11 positive-torus scaling inevitably causes >2^-18 absolute CKKS canonical-slot error **from source Gaussian noise plus independent coefficientwise normalization rounding alone**, even assuming no extra IFMA/FFT error.

**Falsification criterion:** Bound the worst-case canonical embedding of the plaintext residual with source `|e|<=19`, and independent per-component normalization coefficient errors `|r_a|,|r_b|<=rho` destination *integer* units, testing even conservative `rho=1`. If the resulting worst-case absolute per-slot bound is <2^-18, H215's intrinsic-precision-obstruction statement FAILS and the conditional mathematical error screen PASSes.

## Derivation [DERIVATION]

Let source torus grid Q=2^624 (13 limbs, j0 fractional exponent0 to j12 exponent624), target grid Qout=2^572 (12 limbs j0..11), source message `M=beta 2^52`, target output constant coefficient `beta 2^40`. The positive integer torus ×2^40 and output normalization corresponds on centered integer lifts to rounding division `/2^12` of BOTH ciphertext components. Unlike I212's rejected fractional torus division, source modulo-Q wraps disappear because `Q/2^12=2^612≡0 (mod Qout)`.

After publicly applying `sigma_g`, let input GLWE decryption under s be `b+a*s=M+e (mod Q)`. Let `r_b=C(b)-b/2^12` and `r_a=C(a)-a/2^12` (modulo center lifts / Qout), and assume `||r_b||∞,||r_a||∞<=rho`. Then output message-minus-target coefficient error modulo Qout has ring form `e/2^12+r_b+r_a*s`. For the `N=16384` negacyclic ring, `||r_a*s||∞<=||s||_1 ||r_a||∞`. Ternary source secret fixed Hamming weight192 gives `||s||_1=192`; encryption Gaussian bound E19 gives
`||err_coeff||∞ <= (1+192)rho + 19/4096`, in **target coefficient integer units**, independent of source random mask and wrap pattern.

Canonical CKKS slots evaluate `err(X)` on roots of modulus 1; by triangle inequality `|err(zeta)| <= N*||err_coeff||∞`. Divide by CKKS scale2^40. Thus **for every slot**:
`|err_slot| <= N*(193*rho+19/4096)/2^40.`

- If backend uses componentwise nearest-integer rounding `rho=1/2`: coefficient bound **96.504638671875**; slot bound **1.4380311768036336e-6**, corresponding to **19.4075 bits** guaranteed ideal-slot absolute precision.
- Even with **rho=1** (weaker, deliberately conservative): coefficient bound **193.004638671875**; slot bound **2.8759932320099324e-6**, corresponding to **18.4075 bits** guaranteed ideal-slot absolute precision.
- Predeclared REAL RUNNER *screening* threshold from I214 task packet was **2^-18 = 3.814697265625e-6** (not the original author's published requirement). The pessimistic rho≤1 result is **0.753924 of threshold**; the nearest bound is **0.376971 of threshold**. Thus H215 FAILS in the explicitly stated ideal coefficient model. Same sufficient screen with rho=1 holds for `hw<=254` at N16384; not a universal guarantee for arbitrary secret density.

Exact rational arithmetic and assertions executed locally, not sampled:
- `/mnt/data/ship_i215_full_degree_row11_rounding_envelope.py`, SHA256 `d125a6c7688398219ec30da20f95fac3698212a463b63fe0189883e28a65240a`.
- `/mnt/data/ship_i215_full_degree_row11_rounding_envelope.json`, SHA256 `d2bcab0b5c58f4e8301aa49c2fbf91341ec0fba755a0b4f2270f1fc18629267d`.

## Critical scope [OPEN]

**Not a compiled N16384 CKKS verification.** Mathematical bound assumes exact torus GLWE encryption arithmetic, positive integer torus shift, and ≤1 target-integer-unit normalizer error on BOTH components. It does **not** include IFMA/FFT/NTT numerical errors, CKKS encoding/decoding finite precision, ciphertext-ciphertext gating/relinearization noise, possible other key operations, or subtle source layout encoding failure. Nor does it include original-HEaaN experiments. The reference `2^-18` was only a test-screen threshold, not an output quality claim of SHIP or guarantee for full bootstrapping.
**Security:** I210 expanded joint auxiliary-key/circular/KDM assumption still UNPROVEN; no proof of security or insecurity of augmented scheme.
**Performance:** I206 extra ~480 online CT×CT and four extra serial depths remain unmeasured, 624-bit k increases source key generation and key sizes; I207 claimed 81.45% prep payload savings remain conditional layout only. No runner or full Rust key extraction generated; no publication/novelty inference.

## End of iteration

**STATUS: FAIL H215 intrinsic row11 rounding-noise >2^-18 obstruction** / **PASS conditional source-parameter real-dimension ideal error envelope**. **UNCLEAR real IFMA numerical error, true CKKS correctness, security, performance. NOVELTY NOT VERIFIED.**
**RESULT:** For fixed source suite hw192/N16384, a rigorous worst-case ideal-slot bound is 1.438e-6 (nearest) or 2.876e-6 (componentwise residual ≤1), below the prior 3.815e-6 screening tolerance. This is a single non-toy mathematical check using full source dimension and secret distribution, NOT a real FHE run.
**NEXT_ACTION:** **HUMAN_REVIEW / real runner OR PARK**, unchanged in substance: with an actual pinned Rust environment, run the already committed `findings/ship-memory-row11-real-rust-execution-task.md` minimal beta0/1 in-crate true-keygen N16384 test, compare real slot/coeff errors and `ckks_prepare_right` + one CT×CT multiplication. Do not continue adjacent coefficient-bound toy work. Prioritize PI approval of realistic runtime/cost and joint-key security assumption; if no runner, recommend park high-latency branch. **No global STATE change.**
**STATE_UPDATE:** YES independent SHIP findings and checkpoint (material bound on full-size potential obstruction); NO global vFHE STATE.md and no upstream source edits.
