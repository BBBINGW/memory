# SHIP-I240 — Matched sparse-secret estimator source audit: fixed-sign mixture, finite ring samples, clipped noise

Date: 2026-10-16 Asia/Tokyo. PI said **continue SHIP** following I239. One primary falsifiable hypothesis / one cheapest decisive test. Original SHIP: Cheon–Hanrot–Kim–Stehlé ePrint 2025/784; present q520/secret HW192 example is from **independent third-party Poulpy** commit `250d4392656cd313f92ca66d96d8865702d39ddf`, not the authors' HEaaN tested parameters. No claimed original SHIP vulnerability, no attacker key recovery, no numerical log2 attack cost.

## Hypothesis and minimum gate

**H240 (negative screening target):** The precomputed 2026 rotated primal-hybrid attack table for `logn14,h192,sigma3.2` can be transferred *as an exact 128-bit quantitative security answer* for the q2^468, 960-ring-sample first-gadget projection found in I239 by merely substituting `logq=468`; differences in fixed positive/negative composition, finite sample count and clipped noise are already represented by that table, and the original estimator can be executed in the available local runtime.

**Smallest decisive test:** Read source of actual `jdumezy/sparse-key-estimate` and pinned Poulpy key generator/noise; characterize exact secret distribution and ring/scalar sample count; compute **exact sign-bin probabilities and discrete Gaussian cutoff statistics** in Python; check availability of Sage and fpylll; build and syntax-check a separate Sage-run reproduction harness *without fabricating an attack output*. Falsify direct transfer if the precomputed model differs or the estimator cannot be run. Do not repeat I239's public reduction; inherited exact proof/test there.

## Original and estimator source [FACT]

- Original paper ePrint 2025/784 §5.1 HMuxRot, §5.2 author's separately evaluated security parameters; original PDF cached 33pp GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED.
- I239 finding `findings/ship-memory-I239-direct-gadget-prefix-projection-security-gate.md`: third-party Poulpy original first GGLWE gadget row in both columns encrypts `2^468 M` at physical `2^520`; reducing each public component modulo `2^468` yields independent original-noise zero-message RLWE with nominal Gaussian sigma3.2 under automorphized dense secret. 480 HMux candidates×2 first-row input columns =960 ring ciphertext samples, publicly alignable to original s, source-shaped `N16384, HW192`; I239 exact 3072/3072 toy tests. This is an elementary *public reduction*, not key recovery.
- Fixed Poulpy reference `poulpy-cpu-oracle/src/scalar_znx_fill.rs`, blob `4e277ff8d439b96af86b2865b09cf6e4e89be5ae10ddb36`: `fill_ternary_hw` puts **exactly 192 nonzeros** at uniformly shuffled positions, sign of every nonzero independently chosen by `source.next_u32()&1`. Hence **H_plus ~ Binomial(192,1/2)**, NOT exactly 96 each sign.
- Poulpy `poulpy-core/src/noise_distribution.rs` blob `e231917a72be54a5e8dca47ece9f7d8672828020`: `Noise::ENCRYPTION` discrete Gaussian stddev3.2, conditioned `|z|<=floor(6*3.2)=19`.
- Attack prior art Tabitha Ogilvie ePrint **2026/279**, combined *Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE*, CRYPTO2026, and contemporaneous Hou–Jiang ePrint2026/366. The `jdumezy/sparse-key-estimate` fork read via GitHub source:
  - `PrimalHybrid/sparse_estimates.py` blob `d0d59eb0bf6ac514e6eeb56a08af7485dd504fbd`: `build_sparse_lwe_parameters` creates `LWE.Parameters(n=2^logn,q=2^logq,Xs=ND.SparseTernary(p=h//2,m=h-h//2,n=n),Xe=ND.DiscreteGaussian(stddev=sigma))` **without supplying m**. That is **EXACT fixed sign counts**, error modeled *untruncated* standard discrete Gaussian and sample count **m=oo**.
  - `PrimalHybrid/lwe_rot_primal.py` blob `a2bea82715f23089afc606398933623122c583c4`: `RotPrimalHybrid.cost` accepts finite scalar sample `m`; `__call__` passes `m=params.m + params.n if params.Xs<=params.Xe else params.m`, and uses `poly_degree=n`; 4 evaluated attacks include projected-CVP, no-MITM, square-root MITM, estimator-MITM. This is a generic LWE sample count interface, not a proof that `960*N` ring-derived scalar rows are IID.
  - `Precomputed-Tables/128bits_security.md` blob `350df85fa8198351fbc096b5ab49caa6073280ea`: reference **largest logq 367** for logn14,h192,sigma3.2 and >=128 model bits (attacker-estimated, NOT a security proof). I239 projected logq468 exceeds table threshold by **101 modulus bits**, which is NOT 101 lost security bits or a computed key recovery cost.
  - `README.md` blob `f22867fced9c3832668d9515f357ac77c6f23b3f`: needs Sage 10+/Sage packaged Python, scipy and lattice_estimator submodule, prior attack estimates depend on heuristics. The exact clone revision SHOULD be pinned when execution becomes possible; only file blob SHAs recorded here.
  - Standard upstream `malb/lattice-estimator` `estimator/lwe_parameters.py`: `LWEParameters.m` defaults to Sage `oo`, finite count may be passed explicitly; source `__call__` uses `params.m`.

## Exact distribution and finite-sample computations [DERIVED, EXECUTED]

Standalone Python standard-library analysis, **executed**, at `/mnt/data/ship_i240_distribution_audit.py` SHA256 `56fe38294a7ac7c93ce4f6a551c178ad16d0b93fa430192ce8353fb6389a3eab`, resulting `/mnt/data/ship_i240_distribution_audit.json` SHA256 `d49b14a60454363330576fbce3ef730b5747430aec691f2c246889097df5d99b`. Rigorous combinatorics and integer-Gaussian summation:
```
H_plus ~ Binomial(192,1/2)
Pr[H_plus=96]=C(192,96)*2^-192 = 0.0575074303467762.
-log2 Pr[balanced] = 4.120107815771868 bits of SOURCE PRIOR CONDITIONING, NOT attack/security-bit overhead.
Pr[86<=H_plus<=106]=0.8705810684842414.
Pr[82<=H_plus<=110]=0.963916597707066.
Pr[76<=H_plus<=116]=0.9970127214400895.
```
The relative *support counts* for source vs exactly balanced prior differ by ~2^4.12 but this is NOT a quantitative bound on any specific attack's log2 cost or average key recovery work. Running separate conditional-sign composition estimators and combining the attack's prior success is necessary for an actual security statement.

Per-coefficient full (integer) Gaussian q(k) proportional to exp(-k²/(2*3.2²)) and source-truncated q(k||k|<=19):
- Full discrete mass beyond |k|19 = `9.474447350703154e-10`.
- Truncated variance `10.239999624809412`, standard deviation `3.19999994137647`, vs nominal variance10.24; numerically minuscule *single-coefficient* difference.
- ALL `960*16384=15,728,640` independent error coefficients jointly: total variation between iid original full Gaussian product and per-coordinate conditional truncated Gaussian product exactly `1-(1-p_tail)^15,728,640 =0.014791531607175296` (~1.48%) if the ideal fresh coefficient independence holds. **Not negligible at 128-bit statistical security**; cannot equate original estimator distribution to true source under a composable proof, even though concrete heuristic attack costs should be similar. The TV calculation is conditioned on the ideal sample model; actual PRG/IFMA correlations may require separate checks.

Finite sample correction:
- Exactly 960 independently seeded original HMux row RLWE ciphertexts (within ordinary PRG security model).
- Taking the **same single coefficient index from each ring sample** gives 960 *independent* uniform-mask scalar LWE equations under a common signed-permuted sparse secret (this is a legitimate restricted sample view).
- Taking **ALL** coefficients yields `15,728,640` scalar equations; within each ring sample the LWE mask rows are related by signed-circulant permutations of a common uniformly random polynomial, so they are NOT 15.7M IID scalar LWE masks. The ring-aware attack may exploit this relation. The default m=oo precomputed estimator is NOT a faithful finite *Ring-LWE* resource model; simply setting `m=960*N` creates an optimistic IID scalar proxy and is NOT a rigorous implementation of a finite ring sample attack.
- No sample-limited attacker cost `W(N16384,h192,q2^468,sigma3.2,960 ring samples)` is calculated.

## Executable-at-Sage reproduction harness (NOT run here)

`/mnt/data/ship_i240_sage_estimator_runner.py` SHA256 `ea81e0aef641a33267acc706fa35d137b6fef27d033afcbe7f47821ef4758b6b`: implemented parameterized LWE.Parameters `n, q, Xs=SparseTernary(p=hpos,m=192-hpos), Xe=DiscreteGaussian(stddev=3.2), m=finite_scalar_count`. Calls four original `rot_primal_hybrid` attack families using MATZOV red-cost and `poly_degree=n`, returns per-sign-subclass attack estimates and source mixture mass; retains SOURCE-BLOCKED caveats (independent ring rows, truncated Gaussian, KDM). Exact syntax compiled with `python -m py_compile`; standalone `--self-check --positive 82,96,110 --scalar-m 15728640` PASS without Sage. **Real estimator import/call NEVER EXECUTED**, because command `sage` and Python modules `sage`, `fpylll` missing from current container. No fake beta,d,zeta,log2-attack-work values.

Example (once suitable Sage environment installed, full repo/submodule pinned):
```
sage /mnt/data/ship_i240_sage_estimator_runner.py -- \
  --repo /path/to/jdumezy/sparse-key-estimate \
  --positive 82,96,110 --scalar-m 15728640
```
**CAUTION:** m=960N is *optimistic iid-scalar-equation approximation*, not a cryptographically exact model; run `m=960` to obtain a restricted independent scalar projection sensitivity case, then reason correctly about structured ring sample access. The custom CLI does **not** implement exact source clipped discrete Gaussian error in estimator, joint related-key KDM, or source backend numerical noise. It does not turn a table parameter into a 128-bit certificate.

## End of I240

**STATUS:** **FAIL H240 direct numeric transfer of table into a security verdict**, **PASS exact distribution/sample audit and runnable source harness syntax**, **SOURCE_BLOCKED actual specific attack-cost computation** (no Sage/fpylll). No proof of original SHIP/author paper insecurity or security. **RESULT:** 367-bit table threshold (balanced, unbounded samples, untruncated Gaussian) versus 468-bit projection is still a serious security mismatch warning; source independent-sign mixture, finite 960 ring samples (up to 15.7M *dependent* coefficient rows), clipped errors preclude unqualified claim of practical break. Exact 4.1201-bit prior conditioning and 1.479%-joint truncated/uncut TV quantified; no invented `log2(W)`.

**NEXT_TEST:** NO I241 repetition of estimator tables/secret probability if Sage execution environment unavailable. To resume this exact line, obtain actual Sage+submodule execution (no need to ask PI to re-specify parameters) and require output `beta,d,zeta,attack family,log2(W)` for matching sign-bin mixtures and finite ring sample assumptions, plus real compiled source KSK ciphertext validation. Otherwise put security certification task in **SOURCE_BLOCKED / HUMAN_REVIEW** and PI decide whether to PARK SHIP branch or resource estimator infrastructure. PI retains topic and other tracks unchanged. **STATE_UPDATE:** YES finding and root/topic state, read back.
