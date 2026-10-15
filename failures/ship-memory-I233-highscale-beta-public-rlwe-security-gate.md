# SHIP-I233 — Public RLWE-zero-sample extraction from high-scale HMux selector keys: concrete security-gate failure

Date: 2026-10-15 (Asia/Tokyo). PI-selected active SHIP research. One smallest falsifiable technical claim/test after I232. This file closes the specific I232 highscale-beta candidate at the pinned illustrative N=16384, HW192, q_high=2^896. **DOES NOT CLAIM A BREAK OF ORIGINAL SHIP / AUTHOR HEaaN, NOR EXECUTED SECRET RECOVERY.**

## Sources and read-before-write

- FHE local `STATE.md` SHA `0581e141c3c0741c47afd11e83a496c6380c68a4`, topic `findings/ship-memory-STATE.md` SHA `04fa8fd90fbe79d90e995c01a770d360d9973854`, previous I232 finding SHA `485b6489e6f6e7817e7ba4f9fe022cdb611ef4d7`, earlier I216 sparse-safety warning and I210 related-key observation. No other topic edited.
- Original Cheon–Hanrot–Kim–Stehlé, *SHIP*, EUROCRYPT 2025 / IACR ePrint **2025/784**, original §5.1 Algorithm5 PDF physical p23. Original mirror 33 pages, PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. Source key/secret relation independently audited from third-party **Poulpy** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, not author HEaaN: `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` (candidate t_d=sigma_{g_d^-1}(s), beta bit); `poulpy-ckks/src/test_suite/ship.rs` `gen_sk_with_host` calls `glwe_secret_fill_ternary_hw(...,params.hw)`, source illustrative dense `HW192`; `poulpy-core/src/noise_distribution.rs` source Gaussian sigma3.2 conditioned |e|<=19.
- PRIMARY attack paper Tabitha Ogilvie, *On the Concrete Hardness Gap Between MLWE and LWE*, ePrint **2026/279**, cached original mirror PDF 48 physical pp sha256 `2066c5591723582c42182ad0c1e080168ba28bf9791d34c94d4b84fe65ea1f7b`, VERSION_UNVERIFIED. Abstract and §1–3 discuss signed-permutation isometries and sparse-secret RLWE stronger rotated hybrid attacks. Independent merged CRYPTO2026 journal venue paper Hou–Jiang–Ogilvie, *Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE*, CRYPTO2026 Springer DOI https://doi.org/10.1007/978-3-032-35377-1_15, published Aug 9 2026.
- SPECIFIC ESTIMATOR AND PRECOMPUTED TABLE: Jules Dumezy `jdumezy/sparse-key-estimate` repo https://github.com/jdumezy/sparse-key-estimate, `Precomputed-Tables/128bits_security.md` blob **`350df85fa8198351fbc096b5ab49caa6073280ea`**, and `Precomputed-Tables/README.md` blob `3932915ca466e2d828593091d4fd3e451c8b7967`. This is an attack-estimator model based on Ogilvie rotated primal-hybrid, fixed sparse-ternary Hamming weight, error sigma3.2, power-of-two RLWE. **NOT a proof of security at/below the table, NOT a rigorously established attack work factor above it, and NOT the 2024 uniform-ternary general HE-guidelines table**.
- Local runtime `sage` and `fpylll` NOT available, so the estimator was **NOT independently re-executed**. A 100-case EXACT RING algebra test was executed below. No public secret recovery, no BKZ run, no formal cryptanalytic success probability calculated.

## ONE primary H233 and decisive test

**H233 [FALSIFIED as concrete 128bit candidate in specific model]:** For the I232 added `Enc_{t_d}(2^468 beta)` selector GLWE at q_high=2^896 under fixed ternary HW192 secret, there is **no publicly computable mapping** from the emitted selector ciphertexts to a sufficiently ordinary *known-plaintext* RLWE sample family at a modulus large enough to violate the available 128-bit rotated-primal-hybrid `N=16384,h=192,sigma3.2` target table.

**ONE cheapest decisive gate:** Exhibit a **PUBLIC** coefficient-modulus projection and output-secret automorphism to zero-message RLWE, with exact distribution matching the sparse-secret/known small-error attack model; read the 2026 fixed-HW specialized attack table, find its exact N/h/q cell; optionally use the given onehot relation to show full-q unmasking. No parameter micro-sweep or Sage approximation substituting for actual estimator output.

## Derived PUBLIC reduction 1: erase high-scaled hidden bit (exact, no guessing)

I232 outputs a fresh GLWE `E_{j,d}=(A_{j,d},B_{j,d})` at `q_H=2^896` where
```
B_{j,d} + A_{j,d}*t_d = 2^468 beta_{j,d} + e_{j,d} (mod 2^896),
t_d = sigma_(g_d^-1)(s);
beta_{j,d} in {0,1}.
```
Since the public message is a multiple of `q_0=2^468`, reduce BOTH publicly known GLWE components coefficientwise modulo `q_0`:
```
bar_B + bar_A*t_d = e_{j,d} (mod 2^468).
```
The **unknown beta disappears identically**. The reduction of a uniform mask in `R_(2^896)` gives a uniform mask in `R_(2^468)`; sampled encryption error remains the same sigma3.2, truncated to ±19 per coefficient. Next apply public ring automorphism `sigma_(g_d)` to bar_A and bar_B; because `sigma_(g_d)(t_d)=s`, resulting sample is
```
sigma_g(bar_B) + sigma_g(bar_A)*s = sigma_g(e) (mod 2^468).
```
Galois sigma_g in the negacyclic ring permutes coefficient positions and signs, preserving iid symmetric error and HW192 fixed ternary secret. This is a **concrete public map to standard (zero-plaintext) RLWE under one shared s**, not marginal encryption security speculation. All 480 I232 selector ciphertexts can produce these converted samples (independently sampled masks and e under the assumed candidate generation), far more than a single instance; maximum number of independent RLWE *ring samples* and estimator sample model must still be matched before computing exact work factor.

The candidate must therefore consider `n=2^14, h=192, q=2^468, sigma=3.2` at minimum. The table `128bits_security.md` gives for h192:
```
logn = 14 (N16384): maximum logq = 367
logn = 15 (N32768): maximum logq = 737
logn = 16 (N65536): maximum logq = 1475
```
The *publicly extractable* instance already has logq468, exceeding table's N16384 h192 maximum by **101 modulus bits**. This is a failure of a **concrete attack-cost-model 128-bit gate**, not an established 101-bit attack or proof the secret can be recovered in 2^27 operations. The source error is truncated to |e|<=19 whereas tabulated Gaussian is conventionally not identically truncated; the near-tail modeling distinction must be addressed in a faithful new estimator run. Nor does the precomputed table provide a specific cost at logq468; attack runtime <2^128 is a model extrapolation from its monotone maximum admissible q rather than independently run full target parameters.

## Additional full-q public relation from onehot [exact but different error variance]

The candidate source HMux per support j and radix group D has `sum_{d∈D} beta_{j,d}=1`. After applying each original ciphertext's public automorphism `sigma_gd` to align output secrets to `s`, sum the transformed *FULL* q_H ciphertexts and subtract the public trivial plaintext ciphertext `(a=0,b=2^468)`. Under original s, the result decrypts to
```
   sum_d sigma_gd(e_{j,d}) (mod 2^896),
```
because the hidden beta messages sum to the known 1. This gives **128 groupwise independent (32 supports ×4 digit groups) zero-message RLWE samples at full 896-bit modulus**, with per-coefficient noise that is a sum of |D| independent sigma3.2 errors (variance |D|*sigma², sigma≈6.4 for radix4), and absolute support bound |D|*19<=76. PUBLIC, no beta revealed or guessed, no actual attack implementation. One cannot naively reuse the sigma3.2 precomputed table for these aggregated sigma6.4 full-q samples; a matching attack estimate must be run.

This strengthens the critique: simply treating hidden onehot beta as protected encrypted plaintext does NOT hide known-message RLWE instances at q896.

## ONE executed deterministic validation and artifacts

- Executed Python **`/mnt/data/ship_i233_security_reduction.py`**, SHA256 `960dd4c339cb42899bd72b25aa30a1fad83c835f7cc311032e82346efb07fd35`.
- JSON **`/mnt/data/ship_i233_security_reduction_results.json`**, SHA256 `07c274ff83f4117b4893c807b3702c58573d11455138529f5dafddb75ab9b372`.
- Exact toy R=Z[X]/(X16+1) at q_H=2^24, p12, beta selected among four candidates, g_d={1,3,5,7} automorphisms, ternary nontrivial s, independent uniform masks, error polynomials each coefficient sampled bounded integer[-19,19]. **100/100 chosen onehot-group tests PASS BOTH** (i) q2^12 public message-erasing GLWE projection to sigma_g(e) under s, and (ii) q2^24 public group-sum known-message cancellation under s. No simulated BKZ attacks, no Gaussian sampling, no N16384 ciphertext implementation: algebra identities scale to any N.
- Table numeric values read directly via GitHub connector to exact blobs above; sigma3.2/h192 match in reference, but Sage estimator unexecuted. Scripts and JSON local, complete formulas stored here.

## Security-program implications

**STATUS:** **FAIL H233 security-safe high-scale-key claim for the PINNED N16384,H192,q896 illustrative implementation under 2026 rotated primal-hybrid sparse-key attack reference; PASS two exact PUBLIC known-message RLWE sample extraction derivations and 100-case toy validation.** Actual 128-bit security of this parameter set is NOT confirmed and attack cost NOT independently evaluated; likely unacceptably risky according to published specialized estimator. No original SHIP/HEaaN bug found, no demonstrated practical break.

**RESULT:** The I232 improvement (~37.89% conditional key payload at N16384) is not a defensible security-matched cryptographic improvement: high-scale Enc(2^468 β) publicly projects to exact q2^468 fixed-HW192 RLWE known-message samples, for which published rotated primal-hybrid threshold at N16384 is logq367; onehot relation also exposes q2^896 known-message RLWE with sigma roughly6.4. At N32768 the SAME source-sigma3.2 table q737 exceeds reduced q468 but is below **full q896** (full sample sigma differs): needs fresh estimator at sigma6.4. N65536 table q1475 at sigma3.2 exceeds q896 in isolation, but 4x larger N and changed key-bundle, security/circular KDM and all performance must be reassessed. **No constant-sigma 2026 table can certify q896 in the correlated bundle by itself.** Never claim multiplying N by four is sufficient for safety.

**NOVELTY:** PUBLIC modulus projection and onehot sum are elementary attacks-on-candidate interfaces, not a newly discovered weakness in original SHIP nor a publishable cryptanalysis; the specialized rotated primal attack is independent prior art (2026/279, 2026/366/CRYPTO2026).

**RECOMMENDATION:** PARK I232 highscale-beta HMux cryptographic compression at pinned N16384 parameters; do not implement / present memory gain as secure. Reopen only with exact sparse-secret λ128 estimator with multi-sample and covariance/joint-KDM analysis at a **security-matched** ring dimension AND performance/packed-mux Pareto analysis against equally secure original SHIP, or a genuinely new low-q key format eliminating both issue and online highprecision operation. SHIP parent remains PI-selected HUMAN_REVIEW. No automatic pivot to another project.

**NEXT_TEST:** No new SHIP-I234 trivial scaling/parameter sweep. Ask PI for whether to PARK full SHIP research direction; if PI says continue SHIP, source-screen ONE genuinely new secure HMux key representation or obtain actual attack/runner capability, not accumulate similar toy gate checks. **STATE_UPDATE YES.**
