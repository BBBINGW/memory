# Threshold FHE — Correlated / Secret-Conditioned Gaussian Sampling

**Standalone research track:** `CGS`, independent of the existing numbered I1–I194 / vFHE `STATE.md` sequence.
**Created:** 2026-10-14.
**Human PI decision:** explicitly reopen the Threshold FHE correlated-Gaussian problem; keep the previously active vFHE I194 checkpoint untouched.
**Current status:** **CGS-01 PASS (narrow primitive-root/discrete-convolution toy); larger protocol UNCLEAR / NOVELTY NOT VERIFIED**.
**Next CGS iteration:** only with a new smallest hypothesis and one decisive test. This is a TOPIC-HOME research file; append subsequent CGS results here, without changing I-series iteration numbers or overwriting their archives.

## 1. Target / non-negotiable source conditions

[FACT] Hiroki Okada and Tsuyoshi Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint 2025/409, https://eprint.iacr.org/2025/409, source mirror full 40 physical pages (SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, `VERSION_UNVERIFIED` versus latest official binary).

- §1.2, physical p4: in Algorithms 6/7 fresh per-session Gaussian padding is precomputed and Shamir-shared, giving **O(LDec)** stored secret padding material per party; removing the decryption-query bound is an explicit open problem.
- Algorithm 6, physical p26: scalar LWE requires secret-conditioned `ζ^(sid) ∼ D_(Z,σ0 sqrt(Bpub²−||s||²))` and a T-out-of-N Shamir sharing that reconstructs the SAME session padding under any qualified active subset.
- Algorithm 7, physical p29: MLWE requires a discrete Gaussian on `Z^n` with **shape matrix** `σ0² (Bpub² I−Σ_s)`, `Σ_s=Σ_j Gram(s_j)`. Here shape is not literally the empirical covariance of a discrete lattice Gaussian.
- Source security is simulation security under its stated server/adversary, corrupted-party transcript, flooding/rounding, and statistical smoothing assumptions, not merely correctness of reconstruction or covariance.

**Problem:** eliminate or substantially compress per-session correlated **secret-conditioned** Gaussian padding, ideally with constant/succinct setup secret storage and acceptable communication, while retaining exact active-set, privacy, and security properties. No such full solution is established.

## 2. Prior archived negatives — do not repeat

[FACT, REPO] Previously read and checked:
- `findings/threshold-fhe-independent-prf-padding-shamir-correlation-gate-iteration184.md`: independent local PRF Gaussians do not form common Shamir padding; real no-wrap active-set variance constraints can be impossible.
- `findings/threshold-fhe-prss-gaussian-covariance-gate-iteration185.md`: conventional *secret-independent* PRSS has the wrong conditional target law for distinct secrets.
- `findings/thfhe-gaussian-factor-gate-iteration186.md`: public or corrupt-party-recoverable common Gaussian innovation leaks the secret-dependent factor through the joint observable transcript, despite correct output marginal.
- `findings/thfhe-prss-gaussian-mpc-degree-gate-iteration187.md`: running nonlinear Gaussian sampler gates locally on Shamir shares raises polynomial degree; cannot be a drop-in PRSS-only replacement.

These were scoped falsifiers of **naive integrations**, not an impossibility theorem for all Gaussian PCFs, MPC, or structured samplers.

## 3. Outside techniques found (mechanism and limitations)

1. **[FACT / ESSENTIAL PRIOR ART] Integer Gram-root:** Ducas–Galbraith–Prest–Yu, *Integral Matrix Gram Root and Lattice Gaussian Sampling without Floats*, EUROCRYPT 2020, ePrint 2019/320, https://eprint.iacr.org/2019/320. Replace floating-point `AA^T=Σ` by **wider integer** factorization, potentially `n×9n`, enabling Gaussian convolution analysis. This is NOT a new technique invented here. See https://pqshield.com/publications/integral-matrix-gram-root-and-lattice-gaussian-sampling-without-floats/.
2. **[FACT / ESPECIALLY RELEVANT] Ring Gram-root + sphericalization is already the same ThFHE authors' own work:** Okada–Takagi, *Gram Root Decomposition over the Polynomial Ring: Application to Sphericalization of Discrete Gaussian*, ICISSP 2025, DOI 10.5220/0013139700003899, https://www.scitepress.org/PublishedPapers/2025/131397/. They construct short polynomial Gram-root factors, control minimum singular values, and show how discrete-Gaussian ring products can be sphericalized. Crucially their own 2025/409 bibliography already cites [OT25], so using this decomposition alone cannot support a novelty claim. It addresses **Gaussian shape / smoothing**, not automatic private noninteractive Shamir sampling.
3. **[FACT]** Peikert, *An Efficient and Parallel Gaussian Sampler for Lattices*, CRYPTO 2010: covariance-complement perturbation sampling; a mathematical reference for continuous-to-lattice Gaussian convolution, not a seeded private threshold sampler.
4. **[FACT]** Cramer–Damgård–Ishai TCC 2005 and Benhamouda et al. ePrint 2021/1223 already provide seeded linear PRSS; Keller et al., *Secure Noise Sampling for DP in MPC with Finite Precision*, ARES 2024/ePrint 2023/1594, provide nonlinear interactive noise sampling. They do NOT automatically compose into source-compatible secret-covariance-conditioned, one-round, unbounded-session Gaussian ThFHE (see archived I185/I187).
5. **[FACT]** Kairouz–Liu–Steinke, *The Distributed Discrete Gaussian Mechanism for Federated Learning with Secure Aggregation*, ICML 2021, https://proceedings.mlr.press/v139/kairouz21a.html. Its modular-convolution/privacy analysis is useful inspiration, but it neither maintains Shamir active-set identities nor implements secret-conditioned Gaussian covariances.

**Updated bottleneck diagnosis [DERIVED]:** There is substantial existing mathematics for the covariance/Gram-root side. The dominant unsolved integration is **private, fresh, threshold-compatible, secret-conditioned generation with bounded resources and a simulator for the CORRUPTED parties' complete joint view**, not merely computing a matrix square root.

## 4. CGS-01: ONE primary hypothesis + ONE minimal comparison

### Primary hypothesis [HYPOTHESIS]

For scalar padding with **integer** `M=Bpub²−||s||²>0`, select an **integer, primitive** Gram-root vector `a=(a1,...,ak)` with `Σ a_i²=M` and `g_i ← D_(Z,σ0)` independent. The sum `Z_a=Σ a_i g_i` is a mathematically plausible replacement for `D_(Z,σ0 sqrt(M))`; primitive roots may remove discrete-support obstructions that ordinary Gram-factor equality misses.

**Scope deliberately tested:** ONE scalar toy `M=8`, comparing two factor choices with equal quadratic shape, NOT the full arbitrary-key sampling protocol. Failure criterion: a primitive choice still has a large concrete discrepancy from the intended discrete Gaussian even in this easy instance at modest σ0.

### Analytic setup [DERIVED]

Choose `Bpub=3`, scalar `||s||²=1`, so `M=9−1=8`. Both integer roots have `||a||²=8`:
- nonprimitive `a_bad=(2,2)`: `Z_bad=2(g1+g2)` is **always even**;
- primitive `a_good=(2,1,1,1,1)`: `Z_good=2g1+g2+g3+g4+g5`, and `gcd(a_good)=1`, so there is **no lattice-index parity restriction**.

Both match the continuous Gaussian target **shape**: `Σ a_i² σ0² =8σ0²`. But shape equality is NOT discrete Gaussian distribution equality.

The exact target has mass `P(Z=z)∝exp(-π z²/(8σ0²))`. For `a_bad`, `P(Z_bad odd)=0` while the target has nonzero odd mass approaching 1/2 as σ0 grows. Hence the total-variation distance is at least the target odd probability; *no amount of wider σ0 fixes this parity/support defect*.

### One numerical distribution test [COMPUTED toy]

Evaluate the independent `D_(Z,σ0)` product distribution by explicit finite-support convolution, and compute `TV(Law(Z_a), D_(Z,σ0 sqrt(8)))`; each coordinate is truncated at `|g_i|≤ceil(8σ0)`, far into the Gaussian tail. Computation uses FFT double precision: these are **approximate numeric values**, NOT certified negligible-distance bounds.

| σ0 | TV nonprimitive (2,2) | TV primitive (2,1,1,1,1) |
| --- | ---: | ---: |
| 1.5 | 0.499999275 | 0.021255590 |
| 2 | 0.500000000 | 0.0009615933 |
| 3 | 0.500000000 | 0.000000362478 |

Reproducer local script: `/mnt/data/thfhe_cgs01_integer_gaussian_convolution.py`, SHA256 `3e17fc264d8fb35a4f9664f804281dd86710f264f9f7bc91dc189d959d799d41`. Local files are NOT part of GitHub Notes.

**RESULT [PASS, NARROW]:** Primitive *integer* Gaussian factorization has a real algebraic benefit over mere Gram-shape equality: it eliminates fatal lattice-coset support obstructions, and the chosen M8 toy exhibits decreasing TV at larger `σ0`. **Not yet cryptographically negligible** (e.g. 3.62e-7 is nowhere near 2^-128) and NOT proof for all M or source parameters.

### General mathematical observations [DERIVED, NOT A PROTOCOL]

- Lagrange's four-square theorem implies every positive **integer** `M` admits a **primitive five-square** factorization: write `M−1=b1²+b2²+b3²+b4²`; then `a=(1,b1,b2,b3,b4)` has `Σa_i²=M`, `gcd(a)=1`. This is a standard number-theoretic consequence, not new research.
- Primitivity is NECESSARY for full integer support, not SUFFICIENT for statistical closeness. A sharply skewed factor vector can still have a bad push-forward distribution at inadequate σ0. Four squares without primitivity can fail dramatically (M8 witness above).
- There is a precise **smoothing-lattice formulation**. For primitive `a∈Z^k` and `L_a={x∈Z^k:a·x=0}`, the event `a·g=z` has weight proportional to
  `exp(-π z²/(σ0²||a||²)) × ρ_(σ0)( L_z − z a / ||a||² )`,
  where `L_z={x∈Z^k:a·x=z}`. If the Gaussian masses of these affine `L_a` cosets are nearly equal (e.g. under an appropriate lattice smoothing bound on `σ0`), the output law approaches the desired discrete Gaussian. This identifies the next provable gate: bounds for **the kernel lattice smoothing parameter, uniform over the secret-dependent selected Gram roots**, rather than just second moments.
- Extension to MLWE: would need **matrix/ring** primitive or appropriately saturated integer Gram-root matrices for `Bpub²I−Σ_s`, and multivariate smoothing. Ducas et al. and Okada–Takagi ICISSP 2025 are key existing baselines.

### Not solved / non-negotiable protocol work [OPEN]

1. Show a **uniform negligible statistical/computational bound** `Law(Σa_i g_i) ≈ D_(Z,σ0 sqrt(M))` for source-admissible integer M and source-chosen σ0; numeric toy is not a proof.
2. Give a **private** method to choose and secret-share the key-dependent factors `a`, or their MLWE ring analogues. Do not reveal secret-key norm/covariance by publishing these coefficients.
3. Generate fresh hidden `g_i(sid)` for unlimited sessions while producing correct Shamir-shared **products** `a_i g_i` for all qualified active sets. Naive local products require degree reduction; public/recoverable Gaussian innovations violate the joint-view privacy gate. An actual conditional Gaussian PCF, specialized nonlinear correlation generation, or costed interactive MPC is needed.
4. Prove original Algorithm6/7 `PartDec` transcript simulation and security, including repeated/adaptive sessions, corruptions, modulus/rounding, finite precision and residual leakage. Check published 2026 follow-ups for relevant changed threat model.
5. Compare full setup/storage, preprocessing, communication, and total cost; if per-session interaction/keys dominate, the proposal may lose all benefit.
6. Latest-source version parity and mechanism-specific prior-art novelty are unresolved; **NOVELTY NOT VERIFIED**. ePrint 2026/957 by the same authors surfaced in search, but full PDF retrieval through Research MCP was BLOCKED (403 + no mirror); its exact relationship to this target has NOT been verified.

## 5. End of CGS-01 — standalone protocol

**STATUS:** **PASS** (primitive-five-root *toy* Gaussian-convolution feasibility), **UNCLEAR** (general negligible closeness and secure ThFHE sampler).
**RESULT:** Identified existing integral/ring Gram-root techniques, especially a direct same-author prior work; isolated a parity-support obstruction invisible to covariance-only analysis; derived primitive five-square existence for integer scalar shapes; reproduced M8 near-Gaussian distribution comparison; located the unproved kernel-lattice smoothing/security gates. **NO repaired ThFHE or novel theorem/protocol claimed.**
**NEXT_ACTION (CGS-02, human-authorized):** Choose one **source-compatible scalar parameter regime** and one **specified primitive integer root selection**; derive or falsify a quantitative **smoothing bound for the kernel lattice** `L_a=ker_Z(a)` at the actual `σ0`, and determine whether the resulting *per-session* statistical error can meet the source multi-query security requirement. Only if this survives, evaluate a hidden-innovation Shamir/MPC/PCF sampler. **ONE hypothesis + ONE decisive test.**
**STATE_UPDATE:** **NO** to the existing vFHE/I194 `STATE.md`; **RECORD_UPDATE:** YES (this independent CGS topic file).
