# Threshold FHE — Correlated / Secret-Conditioned Gaussian Sampling

> **TOPIC ARCHIVE + CURRENT DETAILED CGS CHECKPOINT (single-session mode, PI decision 2026-10-15):** CGS-34 completed; CGS-35 not started. Naive public online padding-share delivery reusing the PartDec PRF mask is BROKEN (exact one-session RLWE key recovery). Server-direct ciphertext-pad shift passes only aggregate algebra; giving secret covariance to untrusted Server remains an unverified trust/security change. Original O(LDec) problem OPEN. NGP covariance, naive fresh flooding and dummy-covariance self-randomization detours PARK recommended. Original standard-(M)LWE O(LDec) secret-conditioned Gaussian sharing remains OPEN. CGS22–27 structured-NGP and CGS28–31 flooding-only subbranches PARKed. Per-session dummy covariance FAILS joint-view test; persistent dummy requires new known-covariance-MLWE-like PK-covariance hybrid; original O(LDec) question OPEN. NGP fixed-covariance detour PARKed. CGS28–31 fresh-independent-flooding-only statistically-public-Gaussian strategy PARKed under p-cancellation and centered variance gap; original standard-(M)LWE secret-conditioned Gaussian O(LDec) problem still OPEN. NGP/covariance branch remains PARKed; CGS28–30 naive independent-Server flooding-only replacement PARK recommended due to p-cancellation/small-q obstruction; original Gaussian pad-storage problem remains OPEN. NGP/key-covariance branch remains PARKed; flooding-only route is still an UNCLEAR conditional tradeoff, and prior n1024 example FAILED the 128-bit security-guideline screen. This is the complete CGS technical history and next-test detail, NOT a separate write-permission namespace or session lock. The one active research task is selected in root `STATE.md`. Prior track-isolation restrictions in historical sections below are retired; preserve all prior technical findings and numbering. Current Gaussian-padding problem remains OPEN / HUMAN_REVIEW.


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

---

## 6. CGS-02 — source-shaped primitive-five-square Gaussian has a large modular-residue defect (2026-10-14)

**Research numbering:** `CGS-02`, independent of the vFHE `I` iteration sequence. This section **supersedes CGS-01's open smoothing test** only for the single specified primitive factor; it does NOT contradict CGS-01's finite M8 experiment or invalidate all primitive roots.

### One primary hypothesis and one decisive falsifier

**[HYPOTHESIS]** The generic primitive five-square strategy `a=(1,b1,b2,b3,b4)`, `sum ai²=M=Bpub²-||s||²`, with independent `Gi←D_(Z,σ0)`, may be adopted as an across-source-parameters discrete-Gaussian padding primitive at the **original allowed σ0**, simply because `gcd(a)=1` and `||a||²=M`.

**[FALSIFIER / ONE TEST]** Choose one bounded-secret, scalar Algorithm 6 source-shape-compatible `M, σ0` and primitive five-square root, and find one explicit residue distinguisher with constant total-variation separation between `sum ai Gi` and `D_(Z,σ0 sqrt(M))`. This is a quantitative kernel-smoothing necessary gate, not a test of complete interactive ThFHE security.

### Primary paper and parameter envelope

[FACT] Okada–Takagi ePrint 2025/409, 40-physical-page mirror PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED:
- §3.3 p13 Lemma 3.4 gives `η_ε(Z) ≤ sqrt(ln(2(1+1/ε))/π)`.
- **Lemma 3.7 p14** (citing MP13 Theorem 3.3) already gives a sufficient linear-combination discrete-Gaussian convolution condition `s_i ≥ 2 ||z||∞ η_ε(L)`; primitivity determines output lattice support but alone does not guarantee closeness. This is **existing published machinery**, not new insight to claim as theorem.
- Algorithm 6 p26 and Lemma 6.1 pp26–27 use `M=Bpub²−||s||²>0`, `σ0≥sqrt(2)η_ε(Z)`, and `Bpub²≥n Blwe²+1` in the scalar case. Other flooding, modulus and underlying FHE conditions are independent and have not been instantiated here.

**[SOURCE-SHAPED CONDITIONAL INSTANCE]** At finite `κ=128`, let `ε=2^-128`, `n=128`, coefficient/secret bound `Blwe=1`, and conditional bounded secret `s=(1,0,...,0)`, so `||s||²=1`. Take `Bpub=338`, `σ0=8`.
Then `Bpub²=114244≥129=nBlwe²+1`. Lemma 3.4 implies `η_ε(Z)≤5.334978203`, so `sqrt(2)η_ε(Z)≤7.544798529<8`. Thus the relevant original padding-width/secret-bound constraints are met. **Do not claim a complete 128-bit LWE security instantiation, a typical secret distribution, or a practical Bpub choice**: this is a source-allowed *conditional integer padding-shape* witness.

`M=338²−1=114243=1+2(239²)`. Specify the primitive five-term Gram root `a=(1,239,239,0,0)`: gcd is 1 and `sum ai²=M`.

### Exact distributional separation via modulo 239 [DERIVED]

Let `G0,G1,G2 iid D_(Z,8)` and
`W=G0+239(G1+G2)`. Target `T∼D_(Z,S)` with `S=8 sqrt(114243)=2703.988165654576...`. Although `||a||²=M`, the congruence `W mod239=G0 mod239` means the large-factor Gaussian randomness is erased by this residue test.

Let `E⊂Z/239Z` be the 41 centered classes represented by `[-20,20]`. Then `Pr[W mod239∈E]≥Pr[|G0|≤20]`. Since the unnormalized discrete Gaussian tail is dominated by a geometric series and `ρ_8(Z)≥1`,

`Pr[|G0|≥21] ≤ 2 exp(-π·21²/8²)/(1−exp(-π·43/8²)) < 9.031×10^-10.`

For `T∼D_(Z,S)`, Poisson summation on each residue class and `ρ_S(Z)≥S` give
`Pr[T mod239=r] ≤ (1+θ)/239`, where
`θ ≤ 2u/(1−u³),  u=exp(-π(S/239)²)`.
Here `θ<4.564×10^-175` (computed at 100 decimal digits).

Thus `Pr[T mod239∈E]≤(41/239)(1+θ)`, and the data-processing/event characterization of total variation yields
`
 TV(Law(W),Law(T))
 ≥ Pr[W mod239∈E]−Pr[T mod239∈E]
 > 0.82845188194.
`
The lower bound is a **provable inequality**, not an FFT/Monte-Carlo estimate. Exact rational parameter equalities, an analytic tail estimate, and the Poisson bound are evaluated by high-precision mpmath; no repeated sampling is necessary.

**Reproducer** in this session: `/mnt/data/thfhe_cgs02_modular_residue_obstruction.py`, SHA256 `6bc2d89c3c96f37ab907b0e8bc7739663ac5c5c656f8faba9be30f23712a4428`. Local script is not committed via Research MCP.

### Significance and limitations

**[NEGATIVE, decisive for specified construction]** A primitive five-square integer Gram root **can fail spectacularly** to simulate the required discrete Gaussian at `σ0` that already meets source Lemma 6.1's minimal scalar-width condition. The parity test in CGS-01 was only the simplest example; now **even gcd-one full support** can have a large arithmetic-congruence discrepancy.

**[PRIOR ART CONNECTION]** Applying already-source-cited Lemma 3.7 as a *sufficient*, conservative condition to `a=(1,239,239)` requires `σ0≥2·239·η_ε(Z)`. Using the p13 Lemma 3.4 upper estimate gives a sufficient concrete setting `σ0≥2550.12`, >318× our `σ0=8`. This is not a necessary lower bound for all possible samplers and does not imply no improvement over Lemma 3.7 is possible.

**[DO NOT OVERCLAIM]** This only kills the choice `a=(1,239,239,0,0)` with `σ0=8` and any general argument that relies solely on primitive gcd + Gram equality. It does **not** show every primitive factor for M=114243 fails, every source-realistic Bpub suffers, or the original ThFHE protocol fails. Real output distribution includes other independent flooding/rounding noises, which can hide some padding-only distinctions; no full residual-transcript attack is established. No 128-bit ThFHE instantiation was evaluated. Existing I184–I187 nonlinear/PRSS failures remain unchanged. **NOVELTY NOT VERIFIED**; modular character distinguishers and Gaussian smoothing are standard tools.

### End of CGS-02

**STATUS:** **FAIL** for the selected primitive five-square direct sampler at the source-admissible width; **PASS** rigorous quantitative modular-residue certificate; **UNCLEAR** optimized integer roots, multivariate MLWE, hidden-innovation threshold execution.
**RESULT:** Explicit primitive source-shaped M114243 root gives `TV>0.82845188194` at `σ0=8`; existing source Lemma 3.7 already supplies the relevant convolution bound, highlighting an enormous possible gap between source's base σ0 and a sufficient coefficient-sensitive σ0. Selecting Gram roots only by `AA^T=Σ` and gcd is not enough; kernel-lattice smoothing / modular mixing must enter selection.
**NEXT_ACTION (CGS-03; one hypothesis/test only):** For the **SAME** `M=114243, σ0=8`, choose one deliberately **balanced primitive 5-square factorization** (not the prior `(1,239,239,0,0)`), derive a *certified* upper bound on kernel-lattice smoothing error (or one decisive modular-residue lower bound) with a fixed ε target. This distinguishes an inherent five-square/source-width obstruction from an avoidable *bad-root-selection* artifact before spending resources on MPC/PCF integration. First check whether source Lemma 3.7 or a tighter kernel argument already applies. No FHE implementation yet.
**STATE_UPDATE:** NO to independent vFHE `STATE.md`; **CGS TOPIC_RECORD_UPDATE:** YES (this append only).

---

## 7. CGS-03 — a balanced, distinct, primitive 5-square root still has a 6.13% Fourier defect (2026-10-14)

**Independent track:** CGS-03; NOT an I-series / vFHE iteration. One primary hypothesis and one decisive harmonic-distribution test. This record is append-only to the topic home.

### Source / prior-state verification

[FACT: repository] Read existing CGS-01/02, AGENT.md, RESEARCH_PHILOSOPHY.md and the unchanged vFHE STATE.md (at beginning of CGS-03 blob `fe796ef9aa9a193415db8575dfb04cf885491856`; it reports I196). I184–I187 and the CGS-02 bad-root certificate remain archived, not repeated or reinterpreted.

[FACT: original] Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, Research MCP 40pp mirrored PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301` (latest official binary `VERSION_UNVERIFIED`), §3.3 p13 Lemma 3.4 (smoothing upper bound), p14 **Lemma 3.7** (MP13 Theorem 3.3, Gaussian linear combination), Algorithm 6 p26 and Lemma 6.1 pp26–27 (secret-dependent scalar padding and `σ0≥sqrt(2)η_ε(Z)`). Direct original pages were re-read through Research MCP. Ducas–Galbraith–Prest–Yu EUROCRYPT 2020, *Integral Matrix Gram Root and Lattice Gaussian Sampling without Floats* (ePrint 2019/320), is relevant **known prior art** on integral decompositions and perturbation sampling, NOT a privacy-preserving threshold sampler.

### ONE primary hypothesis / ONE falsifier

[HYPOTHESIS] At the **same scalar source-shaped instance** `M=114243, σ0=8` used in CGS-02, deliberately balancing and making all five integer Gram-root coefficients distinct might eliminate the gross discrete-distribution obstruction of `(1,239,239,0,0)` and yield negligible-error Gaussian convolution without increasing σ0.

[FALSIFIER / one minimum test] Construct one such balanced primitive 5-square vector and evaluate the single bounded Fourier character `f(z)=cos(2πz/Q)` at a suitably chosen integer period Q. If its expectation differs from the target Gaussian by a constant, total variation is bounded below by half that difference. This avoids any cryptographic implementation or Monte Carlo.

### Specified parameter instance and chosen factor [DERIVED + exact integer checks]

At `κ=128, ε=2^-128, n=128, Blwe=1`, conditional secret `s=(1,0,...,0)`, `||s||²=1`, `Bpub=338, σ0=8`:
- `M=Bpub²−||s||²=338²−1=114243`; `Bpub²=114244≥n Blwe²+1=129`.
- Lemma 3.4: `η_ε(Z)≤sqrt(ln(2(1+1/ε))/π)≈5.33497820236` and so `sqrt(2)η_ε(Z)≤7.54479852875<σ0=8`.
- These are **only the relevant padding-shape restrictions**, NOT a complete cryptographically secure FHE/ThFHE parameter set and NOT a high-probability sample of the author's secret distribution.

Choose `a=(143,144,151,156,161)`. Exact checks:
- `||a||²=143²+144²+151²+156²+161²=114243=M`;
- `gcd(a)=1`, all five entries are nonzero and pairwise distinct;
- `max(a)/min(a)=161/143≈1.125874`, compared with extremely imbalanced CGS-02 coefficients.

Define `G_i iid D_(Z,8)`, `W=Σ_i a_i G_i`, and `T∼D_(Z,S)` with `S=8 sqrt(M)`.

### Rigorous single-character lower bound [DERIVED]

Set `Q=151`, `f(z)=cos(2πz/Q)`. The residues are
`r_i=a_i−Q=(-8,-7,0,5,10)` and `Σ r_i²=238`.

The characteristic function of a centered discrete Gaussian, by Poisson summation, is
`
 φ_σ(t)=E[exp(2πitG)]
       = [Σ_{k∈Z}exp(-πσ²(k-t)²)]/[Σ_{k∈Z}exp(-πσ² k²)]
`
(real and nonnegative). At `t=a_i/Q`, use integer periodicity to replace it by `r_i/Q`. The `k=0` term and a geometric upper bound on the denominator give
`
 E[f(W)] = Π_i φ_8(a_i/Q)
 ≥ exp(-π·64·238/Q²) / D_upper^5,
 D_upper = 1 + 2u/(1-u³),  u=exp(-π·64).
`
This lower bound is `0.122614216174631953209771851045...`. A separate high-precision direct finite-series evaluation of all five characteristic functions (each `G_i` truncated at ±90, tails negligible) agrees to the printed precision; the formal claim uses Poisson/geometric inequalities, not truncation.

For the target, `S²=64M=7,311,552`, and at `t=1/Q`, the Poisson expression (denominator at least one) gives
`
 E[f(T)]
 ≤ exp(-π S² / Q²)
   + 2 exp(-π S²(1−1/Q)²) / (1−exp(-π S²))
 < 3.077·10^-438.
`
The second term bounds both nonzero dual indices by a geometric series; thus no approximation/sampling assumption is needed.

Because `|f|≤1` and `TV(P,Q)≥|E_Pf−E_Qf|/2`, conclude the quantitative **distribution** certificate
`
 TV(Law(W),D_(Z,8 sqrt(114243)))
 > 0.0613071080873159 > 6.13%.
`
This is far from `2^-128`. It does not establish the true TV or prove the balanced example is better/worse than CGS-02; both numbers are LOWER bounds of different strength.

### Mechanistic significance, published theorem cross-check and boundaries

[NEGATIVE] Balancing the coefficients, choosing gcd 1, and matching Gram shape **still do not guarantee discrete-Gaussian statistical closeness at the original allowed σ0**. Unlike CGS-02's `(1,239,239,0,0)` where modulo 239 deletes all large-factor noise, the new vector has distinct comparable entries, but their near-equality modulo 151 creates a nonnegligible Fourier mode. This exposes **short dual arithmetic frequencies / kernel smoothing**, not a full ThFHE scheme flaw.

[PRIOR ART / SOURCE TEST] Original p14 Lemma 3.7 already requires `σ0≥2||a||∞ η_ε(Z)` as a conservative **sufficient** condition for Gaussian linear-sum closeness. At `||a||∞=161`, applying Lemma 3.4's explicit upper estimate yields the safe (but not necessary) setting `σ0≥1717.863`, versus 8 here. No originality claim for Fourier characters or the theorem, and no proof that every 5-square factorization fails.

[OPEN] Other factorizations, a larger number of smaller coefficients, alternative conditional Gaussian samplers, improved smoothing estimates, and nonlinear secret-correlated PRSS/PCF remain unresolved. The original source's independent flooding and rounding may mask a padding-only distribution discrepancy; this test is NOT an attack on the original scheme nor an adversary on its complete joint transcript. No privacy, all-qualified-subset Shamir correctness, unlimited fresh sid, or full cost model established. **NOVELTY NOT VERIFIED**.

### Reproducibility

One deterministic mpmath script created and executed in this session:
`/mnt/data/thfhe_cgs03_balanced_root_fourier_gate.py`,
SHA256 `3b5e8eadf12245c61f2c39810e4d09a5ad73521c096b2e5bb0932b84e87e8152`.
Output records exact generator/shape/gcd/source width gates, `E f(W)` certified lower bound, `E f(T)` certified upper bound, and the TV inequality. Local work is NOT silently treated as a GitHub file.

### End of CGS-03

**STATUS:** **FAIL** balanced-five-square-is-sufficient hypothesis on one specified instance; **PASS** rigorous Fourier-character `TV>0.061307108...` counterexample. General sampler and complete ThFHE repair **UNCLEAR**.
**RESULT:** Near-common-modulus harmonic defects persist even for distinct primitive balanced integer Gram factors. Shape/coprimality/low max/min ratio are inadequate selection criteria; any next root design must control nonzero dual Fourier modes at source σ0 and its security error budget.
**NEXT_ACTION (CGS-04; PI continuation):** ONE precise hypothesis / one cheapest decisive test: for **the fixed scalar instance M=114243, σ0=8 and exactly 5 independent integer-Gaussian inputs**, determine whether **every** primitive integer factor `a∈Z^5` with `||a||²=M` has a Fourier-character distinguisher `cos(2π t z)` with advantage exceeding `2^-128`; seek a rigorous covering/Diophantine bound or one counterexample factor, **not** another arbitrary handpicked balanced vector. If universal obstruction survives, retire the naive fixed-five-square convolution route and ask PI before changing sampler architecture. Continue to separate mathematical output-distribution tests from corrupted-party simulation / MPC security.
**STATE_UPDATE:** NO to existing vFHE `STATE.md`; **CGS TOPIC_RECORD_UPDATE:** YES, appended CGS-03 only.

---

## 8. CGS-04 — universal 5-term independent-integer-Gaussian Fourier obstruction at the fixed source-shaped parameters (2026-10-14)

**Standalone CGS record** (not the frozen general FHE I counter, and not the independent vFHE V counter). This completes **one primary hypothesis plus one decisive general mathematical test**. No vFHE or global `STATE.md` update.

### Read-before-write / primary source anchors

[FACT — repository] Read previous CGS-01/02/03 sections in this topic file, `AGENT.md`, and `STATE.md`. At beginning of CGS-04 the existing `STATE.md` blob was `db4175bdc29b0fb256a6f4d73d7722a559d749fb`, stating **vFHE V5 COMPLETED** and the old general `I192` counter frozen. This CGS subtrack is explicitly separate; existing I184–I187 negative integration evidence is preserved.

[FACT — original] Re-read ePrint 2025/409, Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, 40 physical pages, Research MCP original mirrored PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, `VERSION_UNVERIFIED`: §3.3 physical p13 Lemma 3.4 (smoothing parameter bound), p14 Lemma 3.7 (linear combinations of lattice Gaussians, citing MP13), Algorithm 6 p26 (the fresh secret-conditioned padding). Paper extraction flags formula/table-layout caveats. The Gaussian distribution is specified by `ρ_s(z)=exp(-πz²/s²)`; all formulas below use this same parameter convention.

### Exactly ONE primary hypothesis / falsification test

**[HYPOTHESIS H-CGS04]** For the fixed source-shaped scalar test regime `κ=128, M=Bpub²−||s||²=114243, σ0=8`, it might still be possible to choose **some** primitive integer root `a∈Z^5` with `Σa_i²=M` so that the five-independent-Gaussian convolution `W_a=Σa_i G_i`, `G_i iid D_(Z,8)`, approximates `T∼D_(Z,8 sqrt(M))` within total variation `2^-128`.

**[MINIMAL DECISIVE TEST]** Prove a **uniform** Fourier-character gap for every such `a`, by a single torus-packing/pigeonhole argument plus Poisson summation; no enumeration of roots, no implementation of Gaussian MPC, and no full FHE security experiment.

### Source-shaped fixed instance

As in CGS-02/03, `Bpub=338`, `||s||²=1`, `M=338²−1=114243`, `σ0=8`; conditional scalar LWE secret with `n=128, Blwe=1` meets the subset of source inequalities `Bpub²≥n Blwe²+1` and `σ0≥sqrt(2)η_(2^-128)(Z)` via p13 Lemma 3.4. These are NOT a full, demonstrated 128-bit LWE parameter set; no lower bound is claimed for all source parameters or MLWE. Five independent terms have identical spherical discrete Gaussian width 8 and integer linear coefficients. The theorem actually holds for **all** `a∈Z^5`, regardless of primitiveness, and therefore in particular for the norm-constrained 5-square factors.

### Universal torus packing lemma [DERIVED / exact]

Let `B=338`. For arbitrary `a=(a_1,...,a_5)∈Z^5`, consider the 195 points on the flat torus `T^5=(R/Z)^5`:

`x_j=(j/B)a mod Z^5, j=0,...,194.`

A geodesic radius-1/4 ball on this flat torus is embedded and has the exact Euclidean volume

`V_5(1/4) = (8π²/15)·(1/4)^5=π²/1920.`

The sum of volumes of 195 such balls is

`195 π²/1920 = 13π²/128 = 1.0023816969856379847... >1 = Vol(T^5).`

Hence not all these balls can be pairwise disjoint. Two centers have torus Euclidean distance **strictly below 1/2**, and subtracting their indices gives `d∈{1,...,194}` such that

`Σ_(i=1)^5 ||d a_i/338||_(R/Z)^2 < 1/4,`

where `||x||_(R/Z)=min_(k∈Z)|x−k|`. This is a **constructive existential bound**: scan 194 integer frequencies and select one satisfying the inequality; no dependence on knowing a special 5-square decomposition, on randomness, or on an asymptotic approximation theorem. If centers coincide, their distance is zero, so the conclusion also holds.

### Exact Fourier-law bound [DERIVED]

For independent `G_i∼D_(Z,σ0)`, define `φ_σ(t)=E[exp(2π i tG)]`. Poisson summation yields the **nonnegative real-valued** characteristic function

`φ_σ(t)= [Σ_(k∈Z) exp(-πσ²(k−t)²)]/[Σ_(k∈Z)exp(-πσ² k²)]`.

For `t=d/338` given by the torus lemma, use the nearest integer dual term in each numerator. With
`u=exp(-π64)` and `D_up=1+2u/(1−u³)`,
`
 E[cos(2πt W_a)]
 = Π_i φ_8(ta_i)
 ≥ exp(-π·64·Σ_i||ta_i||_(R/Z)^2) / D_up^5
 > exp(-16π)/D_up^5
 = 1.4790346159617856525...×10^-22.
`

The target has `S²=64 M=7,311,552`. Since `d∈{1,...,194}`, the distance from `t=d/338` to the nearest integer obeys `dist(t,Z)≥1/338`. Center `t` modulo 1 in `[-1/2,1/2]`. Its Poisson numerator's nearest term is at most `exp(-πS²/338²)`; all nonzero dual terms can be bounded by `2 exp(-πS²/4)/(1−exp(-2πS²))`. The denominator is at least 1, so

`
 0 ≤ E[cos(2πt T)] ≤ exp(-π S²/338²)
      + 2 exp(-π S²/4)/(1−exp(-2πS²))
   = 4.7937754158483940682...×10^-88 + negligible.
`

For `f(z)=cos(2πtz)`, `|f|≤1`, hence `TV(P,Q)≥|E_P f−E_Q f|/2`. Uniformly for **every** `a∈Z^5` with `Σ a_i²=M`,

`
  TV(Law(W_a),D_(Z,8 sqrt(114243)))
  > [ exp(-16π)/D_up^5 − target_upper ] /2
  = 7.3951730798089282627...×10^-23
  > 2^-128 = 2.9387358770557187699...×10^-39.
`

**Theorem is rigorous** under the exact independent integer-Gaussian + five-term model. The decimals are high-precision evaluations of explicitly proved positive bounds, not sampled estimates. The torus argument is classical metric packing; the Gaussian Fourier transform/Poisson formula is standard. **No originality claim has been made or verified**.

### Constructive example sanity checks [COMPUTED]

A local independent script scans `d=1,...,194` and identifies matching low-frequency certificate:
- CGS-02 `a=(1,239,239,0,0)`: `d=17`, centered residues `(17,7,7,0,0)`, squared residual sum `387/338²<1/4`; numerical Fourier witness gives `TV≥0.25303138667...` (not tight versus CGS-02's separate `TV>0.82845` event witness).
- CGS-03 `a=(143,144,151,156,161)`: `d=2`, centered residues `(-52,-50,-36,-26,-16)`, squared residual sum `7432/338²<1/4`; numerical Fourier witness gives `TV≥1.043449×10^-6` (not tight versus CGS-03's previous `>0.061307` certificate).

These are consistency checks for **the same torus-Fourier mechanism**, not separate hypothesis tests or exact TV computations.

**Local, deterministic reproducer**: `/mnt/data/thfhe_cgs04_universal_five_term_fourier.py` SHA256 `4045025f2c321efd5f900c2584413a02c5efce8fa94acbbb64d8cf98b868ee03`. Results JSON `/mnt/data/thfhe_cgs04_universal_five_term_fourier_results.json` SHA256 `e51105e275019fad409483d0f63fa5c7f625087f0ea7f9182e9923d79f138e68`. Both were actually generated and executed in the current container, not GitHub Notes repository files.

### Scope, limits and connection to the ORIGINAL parent gap

**[NEGATIVE] KILL / archive** the **entire exactly-five-term independent `D_(Z,8)` integer Gram-root sum** as a statistically `2^-128`-close direct replacement to the required scalar `D_(Z,8 sqrt(114243))`. This excludes any optimized/balanced/primitive five-square choice **in this fixed source-shaped test regime**, not merely the two prior choices.

**[FACT PRIOR ART]** Source Lemma 3.7 already links Gaussian linear-sum correctness to coefficient-sensitive smoothing; this theorem is a new direct exercise/application of standard torus packing and Poisson tools to our exact question, **NOVELTY NOT VERIFIED**, not a publishable ThFHE improvement.

**[OPEN]** The result does **NOT** rule out: k>5 independent terms, variable widths, affine/correlated/nonlinear samplers, rejection correction, secure interactive MPC, cryptographic PRSS/PCF approaches, or a different σ0/Bpub/security regime. It says nothing about maintaining Shamir-degree-(T−1) shared outputs, hidden innovations, simulation security against corrupt-party views, multi-query statistical accumulation, noise flooding/rounding, or total communication/latency. Gaussian padding **alone** can be far in TV even where total published decrypt-residual is smoothed by additional independent flooding; NO original-paper proof gap or deployed attack is established. The Fourier d depends on the selected root a, so even the concrete distinguisher might not be available to a party who does not know the secret-conditioned factor; a *distribution* lower bound is distinct from an efficient view-based adversary.

### End CGS-04

**STATUS:** **FAIL** existence of any statistically 2^-128-close **five independent base-width-8 integer-Gaussian** factor for this fixed M; **PASS** universal quantitative harmonic obstruction proof; **HUMAN_REVIEW** recommended for choice of next sub-architecture.
**RESULT:** For any integer 5-square Gram root with norm²=114243, proved `TV>7.3951730798e-23>2^-128` via a single dimension-five torus packing and Poisson-character argument. This **decisively closes exactly this mathematical sampler family at these parameters**, with precisely stated boundaries; does not fix original secret-conditioned threshold Gaussian generation.
**NEXT_ACTION:** PI chooses whether to test **ONE** broadened integer-Gaussian sampler family with more than five terms (define k and concrete cost budget first) **or** investigate one named, previously published nonlinear Gaussian correlation / threshold sampling mechanism with a source-compatible security interface; do not automatically pivot, do not repeat roots or run full ThFHE implementation. If choosing a dimension-scaling branch, a smallest next test is a quantitative torus-volume necessary-condition calculation for `k>5` at the same M, σ0 and 2^-128 goal.
**STATE_UPDATE:** NO to global/vFHE `STATE.md`; **CGS TOPIC_RECORD_UPDATE:** YES (this section appended only).

---

## 9. CGS-05 — dimension/cost gate: even SEVEN integer-Gaussian terms fail the fixed 128-bit TV target (2026-10-14)

**Independent CGS track, one hypothesis + one cheapest decisive test.** This is CGS-05, not a vFHE V-round or legacy I-round. Parent CGS remains an open ThFHE correlated-Gaussian sampling problem; prior I184–I187 and CGS-01–04 findings remain intact.

### Read-before-write / sources

[FACT] Re-read this topic file, `AGENT.md`, and global `STATE.md` (at test start blob `4efa09926b695956e1618906f434eec16c883f94`, frozen old global I192, independently tracked vFHE V6). Verified primary Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, current MCP mirror 40pp SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, latest parity `VERSION_UNVERIFIED`: §3.3 pp13–14 Lemma 3.4 smoothing and Lemma 3.7 (citing MP13) Gaussian convolution, Algorithm 6 p26 scalar source padding. A small outside-literature search surfaced familiar Poisson/smoothing and circle-random-walk machinery, but **does not establish novelty** of this packing argument or any protocol.

### ONE primary hypothesis and decisive test

[HYPOTHESIS H-CGS05] The universal five-term obstruction of CGS-04 might disappear as soon as we allow six or seven independent `D_(Z,8)` terms, so `k>5` alone could make a `2^-128`-close integer Gram-root convolution mathematically possible.

**ONE test:** Generalize the exact CGS-04 **torus-volume + Poisson character** certificate from 5 to k dimensions while allowing the character denominator Q to change. Determine the largest k for which this quantitative **sufficient exclusion test** proves a TV lower bound above `2^-128`. Do not enumerate all roots or attempt MPC.

### Fixed tested model [SOURCE-SHAPED CONDITION, NOT FULL SECURITY]

Hold `M=Bpub²−||s||²=338²−1=114243`, `σ0=8`, `κ=128` and the conditional scalar source-bound envelope of CGS-02/03. For arbitrary integer coefficients `a∈Z^k` with `Σa_i²=M`, set
`
 W_a=Σ_(i=1)^k a_i G_i, G_i iid D_(Z,8), 
 T∼D_(Z,8 sqrt(M)).
`
This requirement concerns the **padding sample itself**, not the subsequently flooded and rounded original decryption transcript. `ε=2^-128` is a concrete test threshold, not the sole asymptotic parameter choice mandated by the original paper.

### General torus-volume/Fourier lemma [DERIVED]

For any integers k≥1, Q≥2, let `v_k=π^(k/2)/Γ(k/2+1)`, `r_(k,Q)=(1/(Q v_k))^(1/k)`. When `r_(k,Q)<1/2`, consider Q centers `x_j=(ja/Q) mod Z^k` in the flat torus `T^k`, for j=0,...,Q−1. For any `r>r_(k,Q)` sufficiently close and <1/2, Q embedded radius-r Euclidean torus balls have total volume >1; hence two intersect. Their index difference d satisfies `1≤d≤Q−1` and
`
 Σ_i ||d a_i/Q||_(R/Z)^2 ≤ 4r_(k,Q)^2.
`
The limit is valid because only finitely many d occur. Duplicate points are fine (distance zero).

Write `S²=64M=7,311,552`,
`u=exp(−64π)`, `D_up=1+2u/(1−u³)`. Applying the source-convention Gaussian characteristic function / Poisson identity to `f(z)=cos(2πdz/Q)`, where d is the guaranteed difference, gives:
`
 L(k,Q) = exp(−π·64·4r_(k,Q)^2) / D_up^k
     ≤ E[f(W_a)].
`
Since d is a nonzero residue in [1,Q−1], `dist(d/Q,Z)≥1/Q`. For the target:
`
 0≤ E[f(T)] ≤ U(Q)
 := exp(−π S²/Q²)
     + 2 exp(−π S²/4)/(1−exp(−2π S²)).
`
Thus **for every integer coefficient vector** `a∈Z^k` with norm² M,
`
 TV(Law(W_a), Law(T)) ≥ max(0, (L(k,Q)−U(Q))/2)
`
for each Q for which the embedded-ball condition holds. This is a rigorous coefficient-uniform inequality. Quantitative decimal bounds below result from high-precision deterministic evaluation of these explicit constants; the underlying analytic inequality does not rely on Monte Carlo.

### One dimensional threshold test [COMPUTED CERTIFICATE]

Use selected integer denominators (found by a cheap exploratory Q scan over 30..3999, NOT proved globally optimal). High precision exact-constant evaluation:

| k | Q | certified uniform TV lower bound | exceeds 2^-128? |
|---|---:|---:|---|
| 5 | 889 | 5.28405156104e-13 | YES |
| 6 | 642 | 1.593464226914e-24 | YES |
| **7** | **508** | **6.98341203170453e-39** | **YES** |
| 8 | 426 | 2.87778654572910e-55 | NO CERTIFICATE |

For the decisive k=7, Q=508 witness:
- `v_7=16π³/105`;
- `r_(7,508)=0.32893341809271527<1/2`;
- `4r²=0.43278877415262810<0.43279`;
- `L(7,508)=1.6175091334061144e-38`;
- `U(508)=2.2082672706520839e-39`;
- `(L−U)/2=6.98341203170453008e-39 > 2^-128=2.93873587705571877e-39`, by a factor 2.3763319753.

This improves CGS-04's Q=338 test (which does not reach a 128-bit exclusion at k=7) simply by selecting a better Fourier character denominator, without changing the one-hypothesis mathematical test. The q-scan was only a way to find **explicit valid certificates**, not an assumption of optimality.

### Scientific interpretation / scope

**[NEGATIVE, PROVED]** For this **fixed scalar M and σ0** and exact model of **independent identically distributed `D_(Z,8)` integer-linear components**, NO factor using k≤7 nonzero terms can yield padding TV≤2^-128: if k<7, append zero coefficients and apply the k=7 theorem. Thus, **k≥8 nonzero independent Gaussian draws is a necessary arithmetic condition** for this proposed direct convolution architecture at these parameters.

**[NO POSITIVE CLAIM]** The row k=8 has lower bound <2^-128, so the evaluated spherical-volume proof **does not exclude** 8-term constructions; it does NOT prove an 8-term construction exists, has small TV, or preserves privacy. Other Q values, geometric inequalities, or Fourier characters could still obstruct k=8. Do not convert a lack of certificate into a feasibility proof.

**[COST FLOOR / NOT A PROTOCOL BENCHMARK]** Any direct sampler of this exact form targeting TV≤2^-128 needs at least 8 independent base-width discrete Gaussian draws per scalar padding (and corresponding coefficient-weighted summation). Relative to the CGS-04 five-draw architecture, the *random draw count alone* is at least 8/5=1.6×, but this is NOT a fair latency comparison with native variable-width discrete Gaussian sampling, and says nothing about the much greater distributed multiplication/interaction/secret-sharing costs. This does NOT eliminate original O(LDec) storage, does not implement fresh noninteractive sessions, and does not give an MLWE sampler.

**[PRIOR ART]** Torus volume/pigeonhole, Poisson summation, and original Lemma 3.7 Gaussian convolution are familiar, not established as original results. NOVELTY NOT VERIFIED. No claim of a flaw or attack on the Okada–Takagi source scheme.

### Reproduction and scope of saved artifacts

Local deterministic Python script: `/mnt/data/thfhe_cgs05_dimension_packing_gate.py`, SHA256 `1b894a174ad784a2294a35eb62950f3aa02b8307af00f319b1dde29c06100063`.
Local JSON results: `/mnt/data/thfhe_cgs05_dimension_packing_results.json`, SHA256 `f2854472f6921d12ff82ee6ff3bb543091ee9b12a3724e364627eec2a0c0f8ed`.
Both exist in the working container, not silently promoted to GitHub Notes.

### End CGS-05

**STATUS:** **FAIL** H-CGS05 that six/seven terms escape the fixed 128-bit quantitative Fourier obstruction; **PASS** uniform torus-volume lower bound for all k≤7; **HUMAN_REVIEW / UNCLEAR** at k≥8 and at the actual Threshold FHE protocol level.
**RESULT:** Generalized the five-term obstruction; a specific Q=508 certificate forces `TV≥6.98341203e-39>2^-128` for every norm-constrained seven-term integer-Gaussian convolution. At least eight independent Gaussian terms are NECESSARY at this fixed parameter regime, not proven sufficient.
**NEXT_ACTION (CGS-06, requires PI continuation):** For the **same M=114243, σ0=8, k=8**, select ONE explicitly specified primitive 8-square integer factor using a stated criterion minimizing low-frequency torus/Fourier concentrations, then run a **single source-independent decisive Fourier-frequency falsifier** (a certified >2^-128 gap), or if that fails, produce a legitimate tighter closeness upper-bound plan. Do NOT interpret absence of a small-frequency distinguisher as success. Before any FHE build, still require hidden secret-conditioned sampling, Shamir all-subset reconstruction, nonlinear threshold sharing/security and end-to-end cost.
**STATE_UPDATE:** NO to global/vFHE STATE.md; **CGS TOPIC_RECORD_UPDATE:** YES, append this section only.

---

## 10. CGS-06 — a reproducibly selected eight-term candidate still fails the Gaussian Fourier gate (2026-10-14)

**Independent CGS subtrack** (not general frozen I counter, not vFHE V counter). One primary hypothesis and one decisive candidate-specific Fourier test; **no universal k=8 failure claim**.

### Recovery, provenance and already-known boundaries

[FACT, REPO] Re-read previous CGS-01...05 sections of this same file, `AGENT.md` and `STATE.md` before writing. At start of iteration topic SHA `7bed58427e8966992573f66128c7d92f92f1a342`, global state SHA `4efa09926b695956e1618906f434eec16c883f94` (general I192 frozen, vFHE V6). Do not alter these state files.

[FACT, SOURCE] Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, 40 physical-page Research MCP mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, `VERSION_UNVERIFIED`. Original §3.3 Lemma 3.7 p14 gives a sufficient condition for discrete-Gaussian integer linear sums, and Algorithm 6 p26 samples scalar `ζ∼D_(Z,σ0 sqrt(Bpub²−||s||²))`, which is Shamir-pre-shared per session. We retain CGS-02 through CGS-05's fixed *padding-only* instance, not a full 128-bit secure FHE parameter instantiation.

[FACT, RELATED PRIOR ART] Genise–Micciancio–Peikert–Walter, *Improved Discrete Gaussian and Subgaussian Analysis for Lattice Cryptography*, PKC 2020, full preprint at https://cseweb.ucsd.edu/~daniele/papers/PKC2020.pdf. The paper's **Theorem 1** treats linear images of lattice discrete Gaussians under smoothing of `Λ∩ker(T)`, and its convolution theorem family includes independent integer combinations (**Theorem 4**). The conceptual kernel-lattice gate is established prior art, **NOT our novel technique**. The web PDF's visual screenshot failed cache retrieval; text was available, and any theorem-level application to a prospective sampler must still verify exact statement/assumptions against reliable original pages. This is a promising **next verification instrument**, not a current proved positive sampler.

### One primary hypothesis and falsifier

**H-CGS06 [HYPOTHESIS]** Once k=8 avoids the *uniform* k≤7 obstruction of CGS-05, an explicitly selected well-dispersed eight-square integer root under the fixed `M=114243,σ0=8` may give `TV≤2^-128` between `W_a=Σ_i a_iG_i` (`G_i iid D_(Z,8)`) and target `T∼D_(Z,8 sqrt(M))`.

**ONE DECISIVE TEST:** Reproducibly select one candidate using an explicit worst-nontrivial-Fourier-mode proxy; then exhibit **one exact rational character** `f(z)=cos(2πtz)` and analytically certified `TV>2^-128`. An arbitrary floating-grid absence of a character would NOT prove success.

### Candidate selection with deterministic, stated limitation [COMPUTED]

Source-shaped padding instance: `Bpub=338`, conditional `||s||²=1`, `M=338²−1=114243`, `σ0=8, κ=128`. Source only allows the **padding-width/secret-bound subset** of conditions already checked CGS-02/03; real LWE security, typical secret-key distribution, the original joint transcript, and any threshold Gaussian sampler remain unverified.

1. Fixed `random.Random(20261014)`, 25,000 proposals of six coefficients in `[30,182]`; complete each by all positive `u²+v²=remaining` with `15≤u≤v≤209`, sorted roots, keep 8 pairwise-distinct primitive entries. This produces **5,288 unique roots**. 
2. Consider **the first 5,000 roots sorted lexicographically**. For each, maximize the *conservative dispersion proxy* `min_(1/400≤t≤1/2) Σ_i dist(a_i t,Z)²`, calculated by enumerating nearest-integer transition boundaries `t=(j+1/2)/a_i`; inside each interval the objective is a quadratic and its minimizer is the clipped rational `(a·n)/M`. This is deterministic finite search, **not a global optimum over all eight-square roots, not a proof of closeness**, and the proxy is not the true TV.
3. Selected `a=(66,68,93,96,116,129,130,201)`. Exact check: `Σa_i²=114243`, `gcd(a)=1`, all eight entries distinct; floating proxy `min S(t)≈0.2365396566966897`.

### Exact Fourier distinguisher [DERIVED: rational certificate]

The selected minimizer occurs in a cell with nearest integers
`n=(24,25,34,35,42,47,47,73)`.
Its exact rational frequency and energy satisfy
`
 a·n=41524,   t=(a·n)/(a·a)=41524/114243,
 Σ_i (t a_i−n_i)² = Σ_i n_i²−(a·n)²/M = 27023/114243.
`
All are exact integer/rational equalities independent of floating scanning. `1/400<t<1/2`.

Let `φ_σ(x)=E_(G←D_Z,σ)[exp(2πixG)]`. Poisson summation gives
`
 φ_σ(x) =
 [Σ_(j∈Z) exp(−πσ²(j−x)²)]
 / [Σ_(j∈Z) exp(−πσ² j²)] ≥0.
`
Set `u=exp(−64π)` and `D_up=1+2u/(1−u³)`. For `W_a=Σ_i a_iG_i` and `f(z)=cos(2πtz)`, by independence and the nearest term of each numerator:
`
 E[f(W_a)]=Π_i φ_8(t a_i)
 ≥ exp(−π64·27023/114243)/D_up^8
 = 2.2148110523356737699108...·10^-21.
`
For target `T∼D_(Z,S)`, `S²=64M=7,311,552`, since `t∈[1/400,1/2]`, the **uniform** Poisson upper bound is
`
 E[f(T)] ≤ exp(−πS²/400²)
           +2 exp(−πS²/4)/(1−exp(−2πS²))
 = 4.4856035130069068787490...·10^-63.
`
Therefore, using `|f|≤1` and the bounded-function TV inequality,
`
 TV(Law(W_a),D_(Z,8sqrt(M)))
 ≥ (E[f(W_a)]−E[f(T)])/2
 > 1.1074055261678368849554...·10^-21
 > 3.76830573585718792·10^17 · 2^-128.
`
This is a **rigorous numeric constant from exact analytic inequalities**, with high-precision decimal evaluations, not simulated ciphertext security. A second direct evaluation of the product of five-to-eight discrete-Gaussian characteristic functions agrees with the analytic bound.

### Reproducer and SHA [COMPUTED]

- `/mnt/data/thfhe_cgs06_eight_term_fourier_falsifier.py`, SHA256 `86ec1fc1b2b21690952261dc410f4e0366b1c1dd85c60326b42d349b1d924a5c`.
- `/mnt/data/thfhe_cgs06_eight_term_fourier_results.json`, SHA256 `a92c290cb650e7c768fa0bb3093aa49cb1ae5cf2508fc6dcfd7fa9cb683eb7f0`.
Both have been run, hash-verified and left as **local reproducibility files**, not uploaded into GitHub Notes.

### Meaning, negative result and limitations

**FAIL (candidate only):** Even the **best by the stated proxy among a deterministic sample of 5,000 valid k=8 roots** has a single Fourier character with TV far beyond the (2^{-128}) test threshold. CGS-05's failure to exclude k=8 uniformly was NOT a positive existence theorem; we now have one specifically falsified eight-term candidate, **not a no-go theorem for all eight-term roots**.

**No novelty claim:** Torus/Fourier/Poisson tests and lattice kernel smoothing are traditional tools. The explicitly named Genise–Micciancio–Peikert–Walter theorem already handles linear-image smoothing in general. The candidate/constant are problem-specific numerical-algebraic checks, not a publishable primitive by themselves.

**Not addressed:** The original source's full decrypted residual includes independent flooding/rounding and adversary corruption; the actual protocol's distinguishability and security may differ from the padding-only TV. No attack on the source, no simulator, no compression of O(LDec) shares, no private factor selection, no hidden fresh Gaussian innovations, no Shamir degree reduction, no MLWE covariance sampling, no full parameter/communication cost assessment.

### End CGS-06

**STATUS:** **FAIL** for one deliberately selected eight-term convolution; **PASS** exact Fourier TV certificate; **UNCLEAR/HUMAN_REVIEW** for all-eight-term family and complete Threshold FHE correlated sampling.
**RESULT:** Deterministic pool of 5,288 primitive eight-square roots; selected candidate among 5,000 under a stated minimax Fourier-energy proxy; exact rational witness `t=41524/114243` with energy `27023/114243`, proving `TV>1.107405526e-21` for that candidate at source-shaped σ0=8. The k≥8 *necessary* lower bound from CGS-05 remains valid, but eight terms are not sufficient merely by dimension.
**NEXT_ACTION (CGS-07, only on PI's next continuation):** **Stop selecting arbitrary new k=8 integer roots.** Read Genise–Micciancio–Peikert–Walter PKC 2020 **Theorem 1 + Theorem 4** (original reliable full text), derive one explicit **kernel-lattice smoothing sufficient condition** for integer map `a:Z^k→Z` at source σ0. Then perform ONE cheap feasibility/cost gate for a **specified scalable dimension k or structured small-coefficient factor** that *provably* satisfies it, or falsify parameter feasibility. Treat correlated-secret Shamir/PCF and original simulation as separate mandatory stages. If impossible to beat direct native Gaussian pre-sharing cost, recommend ARCHIVE fixed-sum engineering direction and ask PI.
**STATE_UPDATE:** **NO** to global/vFHE `STATE.md`; **CGS TOPIC_RECORD_UPDATE:** YES, this section appended only.


---
## CGS-09 (2026-10-14): two-scale structure, 19 ones + 7139 fours

**Primary hypothesis:** At M=114243 and sigma0=8, does W=U+4Y, where U is the sum of 19 independent D_Z,8 variables and Y the sum of 7139 such variables, approximate D_Z,8sqrt(M) within 2^-128?

**One decisive test [PASS]:** By PKC 2020 ePrint 2020/337 Theorem 3.1 (physical p12) and Theorem 4.6 (p18), analyze the A18 and A7138 root-lattice smoothing and the 1D kernel of (u,v)->u+v on Z x 4Z. With epsilon=2^-180, analytic upper bounds on the three dual theta excesses are 1.230e-64, 4.620e-62, and 4.224e-104, respectively, all less than epsilon. Their output errors compose to TV <= 6 epsilon/(1-epsilon) < 3.916e-54. Exact squared Gaussian shapes: 1216+7310336=7311552=64M.

**Cost:** 7158 independent base Gaussian draws per padding, 74.94% fewer than CGS-08's 28563, but still vastly more than one direct wide Gaussian. This does NOT solve private secret-dependent coefficients, correlated Shamir shares, unlimited decryption queries, joint-view simulation, or end-to-end FHE cost. Not a protocol result; novelty unverified. Full proof and reproducible code saved as local CGS-09 artifacts.

**STATUS:** PASS single-output distribution; overall Threshold FHE sampler UNCLEAR.
**RESULT:** Rigorous near-Gaussian convolution using 19 ones and 7139 fours.
**NEXT_ACTION:** Do not continue a coefficient-compression treadmill. Revisit the original Algorithm 6 O(LDec) storage obstacle and test one source-compatible seeded/secret-conditioned Shamir correlation-generation mechanism, with the corrupted-party joint view as the primary gate. Only extend Gaussian sum dimensions if this protocol interface becomes plausible.
**STATE_UPDATE:** NO to global/vFHE state. CGS-topic update only.


---
## Historical recovery: CGS-07 and CGS-08 (original local records, earlier GitHub append failures)

This is a **backfill of two already completed earlier rounds**, not new research and not a renumbering.

**CGS-07** — all-unit factor with exactly M=114243 independent D_Z,8 draws. Kernel root lattice A_114242: explicit dual theta excess <7.393e-61 <2^-180; PKC 2020 ePrint 2020/337 Theorem 3.1 gives output TV <1.306e-54 against D_Z,8sqrt(M). **PASS padding law**, but 114243 draws/sample and no Shamir correlation/secret-conditioning protocol. Complete original record in local `CGS-07_threshold_FHE_root_lattice_smoothing.md`; source SHA256 ePrint 2020/337 `cc7866d675863eea9f2d05c476a865bcead6c9eacb297fea0dde8dd25067737a`.

**CGS-08** — factor containing 3 ones and 28560 twos (norm squared 3+4*28560=M). Using smoothing of A_2, A_28559 and the pairwise convolution kernel on Z x 2Z yields three dual excesses <3.671e-58, <1.849e-61, <6.497e-66, all below 2^-180. Hence TV <3.916e-54 with 28563 independent D_Z,8 draws. **PASS padding law**, no FHE protocol improvement. Complete original local record in `CGS-08_threshold_FHE_two_scale_gaussian_smoothing.md`.

Both results use established lattice Gaussian linear-image/convolution tools, not novel threshold sampling. Both local full records predate the GH commit for CGS-09; the earlier GH writes were blocked and are not falsely claimed to have succeeded. CGS-09 is the next completed round and already separately recorded above. The original O(LDec) storage and corrupted-party simulation problem is OPEN.


---
## CGS-10 — public-key PCF master-secret binding gate (2026-10-14)

**Track:** Independent CGS, following CGS-09; no I-series or V-series updates. One primary hypothesis and one source-syntax falsifier. Earlier I185/I187 ruled out conventional secret-independent PRSS and naive locally nonlinear Shamir evaluation; this test examines a **different published primitive**, namely general reverse-samplable public-key PCFs.

### Source provenance [FACT]

**Baseline**: Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, original 40pp mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, version unverified. Original Algorithm 6 physical p26: external FHE.KeyGen first produces `s`; setup samples independent session pads `ζ^(sid) ← D_(Z,σ0 sqrt(Bpub²−||s||²))`, distributes Shamir shares; PartDec applies Lagrange coefficients for any qualified active subset. Real goal is eliminate `O(LDec)` storage without changing the security/simulation interface.

**Concrete prior art**: Damiano Abram, Peter Scholl, Sophia Yakoubov, *Distributed (Correlation) Samplers: How to Remove a Trusted Dealer in One Round*, IACR ePrint **2022/535**, https://eprint.iacr.org/2022/535, complete 73 physical-page PDF acquired via Research MCP, GitHub mirror SHA256 `01049b2f0bd222fad71ee380838f3409ef560b75da02521b29b0d6d65c6bb0b3`, latest official binary version unverified. Original §6.1 pp33–35 **Definition 6.1**, §6.2 pp35–38 **Definitions 6.2–6.4**, §6.3 p40–41 **Theorem 6.7 and Figure 19**, §6.4 pp41–43 **Theorems 6.8–6.10**, examined directly; printed formula extraction may require visual parity checks. Source's public-key PCF supports correlated outputs at multiple nonces and can support *internally generated* master secrets; this is important, real prior art. The relevant circuit is iO of a puncturable-PRF-driven correlation sampler with per-party PKE encryption, hence **not a lightweight symmetric PRSS**. Theorem 6.7 restricts the nonce length to polylog(lambda) with polynomially secure primitives, allowing poly(lambda) nonce length under sub-exponentially secure assumptions; not equivalent to a practical unlimited-session implementation.

**Alternative prior art**: Boyle–Couteau–Gilboa–Ishai–Kohl–Scholl, *Correlated Pseudorandom Functions from Variable-Density LPN*, FOCS 2020, ePrint **2020/1417**, original 80pp full PDF acquired via Research MCP SHA256 `ff897169e970009ba138524f782c9417a78c8df7240e9292f438b0620f63f688`. Establishes insider-security and (for supported correlations) reverse-sampleability, not an existing arbitrary hidden-norm Shamir Gaussian PCF.

### Exactly one hypothesis / decisive test

**H-CGS10 [HYPOTHESIS]** A **literal independent plug-in** of the 2022/535 Figure 19 public-key PCF — independent one-time PCF initialization, each party evaluates on nonce `sid`, *without* modifying the existing FHE.KeyGen to generate a coupled secret — can replace Algorithm 6's pre-shared padding shares while preserving its *external* FHE-key-dependent Gaussian distribution.

**One decisive source-syntax test**: Inspect Figure 19's concrete dataflow for **any input or setup binding to the already-existing external FHE secret**. Figure 19's `Gen(1^λ,i)` samples a standalone PKE key pair; `Eval(i,CGP,pk_1,..,pk_N,sk_i,x)` calls the obfuscated `PCG` and decrypts its output. The obfuscated PCG computes its PRF seeds from the *PCF public keys* (and nonce), calls `mk_i←Secret(1^λ,i;seed_i)`, and calls `C(1^λ,mk_1,..,mk_N;randomness)`. **No external `FHE.s` or original FHE.KeyGen output appears as an input**.

If these independent coins are actually independent of the existing FHE.KeyGen and nonce is simply a public `sid`, conditional on fixed external s the PCF output law is the SAME for all candidate s, whereas Algorithm6 requires the law `D_(Z,σ0 sqrt(Bpub²−||s||²))` to change with s. This is a semantic coupling mismatch. As in prior I185, two permitted secrets of differing squared norm give different target likelihood ratios; the novel point here is the **published generic PCF's actual Figure19 KeyGen/Extract/Sampler interface**, not a rediscovery of the two-secret algebra. This does not prove non-negligible distinguisher advantage in a full source protocol; other FHE flooding and simulators remain relevant.

**RESULT [FAIL, tightly scoped]:** The unmodified *independently initialized* PCF is **NOT a direct drop-in** for externally generated secret-conditioned padding. Master-secret support in Definition 6.1 is not an `InputExistingFHESecret(s)` facility. Do NOT generalize this to an impossibility of PCFs, reverse-samplable Shamir-Gaussian correlations, or cryptographically coupled joint key generation. In particular, a future redesigned `FHE.KeyGen + correlation C` could conceivably generate FHE sk and pcfs' master state *jointly*, but would need a new distribution/security reduction, public-key compatibility and a full corrupted-party simulator.

**Threat-model/efficiency boundaries [FACT + INFERENCE]:** Theorem6.7 Figure19 setup relies on iO, PKE and puncturable PRFs; Eval runs an obfuscated circuit that generates the whole vector of correlated outputs and encrypts each to one party, so a nominally communication-free local evaluation is not free computation. Theorems6.8–6.10 also require a distributed setup sampler and, for active security, RO/anti-rushing or URS/NIZK/subexponential assumptions. Baseline source uses one online partial-decryption share per party, so a fair comparison must include the added setup/key generation, per-session iO/circuit work, PKE and its security assumptions. No quantitative benchmark or performance improvement established.

**STATUS:** **FAIL** literal stand-alone Public-Key PCF plug-in; **PASS** concrete prior-art interface audit; **UNCLEAR** coupled PCF/FHE-keygen and corruption security. No original paper flaw, exploit or new cryptographic primitive claimed. NOVELTY NOT VERIFIED.
**NEXT_ACTION (CGS-11, only on human continuation):** Examine ONE precise **coupled-keygen** correlation `C` where the same hidden s determines both FHE public-key material and Shamir Gaussian padding shares: does published Definition 6.1 **reverse sampleability** continue to hold when the public FHE key and ≤T−1 corrupted secret shares are in the joint view? Give one actual conditional re-sampling algorithm or a minimal obstruction with the published definition. Do not implement iO, do not re-run the old PRSS squaring example, and do not claim cost improvements until this gate passes.
**STATE_UPDATE:** NO global or vFHE `STATE.md`; **CGS TOPIC_RECORD_UPDATE:** YES, append this section only.


---
## CGS-11 — a joint FHE-key/share correlation is not automatically reverse samplable (2026-10-14)

**Independent CGS track, one primary hypothesis + one decisive test.** Read AGENT.md, RESEARCH_PHILOSOPHY.md, unchanged global STATE.md (at start blob `528741fd2b38609fad2547721044474ea9e259cb`) and previous CGS-10 before testing; no V/I counter changes.

**Original sources [FACT]:** Abram–Scholl–Yakoubov, *Distributed (Correlation) Samplers: How to Remove a Trusted Dealer in One Round*, ePrint 2022/535, original 73-physical-page Research MCP mirror SHA256 `01049b2f0bd222fad71ee380838f3409ef560b75da02521b29b0d6d65c6bb0b3`, VERSION_UNVERIFIED; Definition 6.1 physical pp34–35 gives the reverse-sampleability game, Definitions 6.2–6.3 p35 the public-key PCF, Theorem 6.7 and Figure 19 pp40–41 the conditional iO/PKE PCF. Okada–Takagi ePrint 2025/409 Algorithm6 p26, source PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, requires fresh Shamir-shared D_(Z,sigma0 sqrt(Bpub²−||s||²)) padding for existing FHE s. The source's FHE pk is LWE-derived, NOT the following toy's group commitment.

**H-CGS11 [one hypothesis]:** Instead of independent PCF initialization (CGS-10 failure), jointly generate the SAME hidden s for both a publicly checkable pk and degree-one Shamir key shares, add s-conditioned Gaussian-padding shares, and output the whole tuple as one correlation C. Hypothesize that generic ePrint 2022/535 Definition6.1 reverse-samplability applies, enabling Theorem6.7.

**One falsifier [DERIVED; DLog-conditional]:** Choose a cyclic group G=<g> of prime order q where DLog is hard. Take s,r,u independent uniform in Fq, pk=g^s, Gaussian padding zeta from any positive s-conditioned efficiently samplable width, and form 
`alpha=s+r, beta=s+2r; omega=zeta+u, nu=zeta+2u (mod q)`.
Return two correlation outputs `R1=(pk,alpha,omega)`, `R2=(pk,beta,nu)`. The per-party 'master secrets' in the published Definition6.1 can be independent dummy values; C jointly generates these linked outputs. This is a **mathematical 2-out-of-2 key-sharing toy**, not an LWE-FHE instantiation. In real outputs the efficient predicate `pk(R1)=pk(R2) and g^(2alpha−beta)=pk` ALWAYS passes.

Given a random DLog challenge y=g^s, an inversion reduction samples independently uniform alpha,omega and supplies the corrupted view `R1=(y,alpha,omega)` to a hypothetical PPT reverse sampler for corruption set {1}. This view has EXACTLY the honest correlation's marginal law because r,u mask alpha and omega uniformly independently even when zeta depends on s; y is uniform in G. Parse produced honest output's beta and output `s'=2alpha−beta (mod q)`. Definition6.1 demands computational indistinguishability of the full tuple; the public predicate therefore passes with probability 1−negl. Hence `g^s'=y` with probability 1−negl, breaking DLog. **Thus this fully coupled pk+keyshares+padding correlation is NOT reverse samplable under the DLog assumption.** The obstruction already exists in the pk/key-share components and is independent of Gaussian details.

**Exact toy verification [COMPUTED, not security proof]:** q=101, p=607, g=64 (group order 101), s=7,r=11, so `pk=482,alpha=18,beta=29`, `2alpha−beta=7` and `64^7 mod607=482`. Exhaustive q² enumeration verifies the corrupted key/pad-share pair is uniform for two fixed values of s and zeta. Deterministic local files: `/mnt/data/thfhe_cgs11_reverse_sampler_oneway_gate.py` SHA256 `d5b588c03b244d5f1fe608e524546d3aface63e207930e192ee74133552a8ba6`, and `/mnt/data/thfhe_cgs11_reverse_sampler_oneway_results.json` SHA256 `cd3d4c72c62e7146bcea6ca5be1eda14aadc0bb3c35210b86ffd80c724f60e6a`. Full local proof/report: `/mnt/data/CGS-11_joint_keygen_reverse_sampling_obstruction.md` SHA256 `25c68cd0c978dfcede7256ed7ce72a2ac84ee06ce398a18ad0dc238b7c3efeda`.

**Boundaries / novelty:** This rules out the one **specified** 2-of-2 group-key correlation under DLog, and falsifies any inference that 'coupled keygen' automatically meets Definition6.1. The actual LWE pk+secret shares require a separate search-LWE-style reduction; this is NOT a proof of impossibility for Okada–Takagi or all PCFs. Keeping pk/key shares OUTSIDE the correlation output may avoid this specific inversion argument, but then calls for an explicit auxiliary-input / externally-linked-state security definition and proof; the published Theorem6.7 does not automatically supply it. Source notes that other types of correlation may not be reverse samplable. Elementary one-wayness consistency obstruction is NOT VERIFIED NOVEL and is not claimed as a new protocol.

**STATUS:** **FAIL** for naive complete joint-KeyGen correlation's reverse-samplability; **PASS** conditional DLog reduction and exact toy sanity; **UNCLEAR** secret-dependent padding-shares-only PCF / actual ThFHE.
**RESULT:** Binding all pk, Shamir key shares and Gaussian shares inside a reverse-sampled output can require recovering one-way key material when filling in honest-party shares. It does not solve O(LDec) storage and offers no efficiency result.
**NEXT_ACTION (CGS-12, human continuation):** Define ONE *padding-shares-only* correlation where pre-existing FHE pk and sk shares remain fixed as external auxiliary state, and for a two-party corruption view test whether honest Gaussian pad-share conditional resampling is possible without s, and whether a published theorem actually supports the required externally-linked auxiliary-input security notion. Do not re-run the key-share inversion model and do not conflate an impossibility for one correlation with all PCFs.
**STATE_UPDATE:** NO global/vFHE STATE.md; **CGS TOPIC_RECORD_UPDATE:** YES (append only).


---
## CGS-12 — padding-only reverse-sampling versus hidden external Gaussian width (2026-10-14)

**Standalone CGS track, one hypothesis / one decisive test.** Read AGENT.md, RESEARCH_PHILOSOPHY.md, previous CGS-10/11, and STATE.md before testing. No updates to general I or vFHE V counters.

**Sources [FACT]:** Abram–Scholl–Yakoubov, *Distributed (Correlation) Samplers: How to Remove a Trusted Dealer in One Round*, EUROCRYPT 2022, ePrint **2022/535**, full Research MCP 73pp mirror SHA256 `01049b2f0bd222fad71ee380838f3409ef560b75da02521b29b0d6d65c6bb0b3`, VERSION_UNVERIFIED. Definition 6.1 physical pp34–35 states reverse-sampling for full correlation-output vectors, Figure 15 p37 its PCF security game and Theorem 6.7/Figure 19 pp40–41 the generic construction. **Important:** this definition has NO general arbitrary external encrypted auxiliary-input binding interface. Baseline Okada–Takagi, ePrint **2025/409**, full 40pp mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED: Algorithm 5 p23 observable partial-decryption transcript; Algorithm 6 p26 secret-conditioned Gaussian pads; Lemma 6.1 pp26–27 and Theorem 6.3 p28 simulate the *combined decryption residual* without knowing the secret norm under source assumptions.

**H-CGS12:** Keep public FHE key and Shamir key shares as fixed external auxiliary state, and generate ONLY Gaussian padding shares. Hypothesize a public-auxiliary-input *full-pad-vector* reverse sampler can, without knowing the hidden Gaussian width, complete corrupted pad shares so that all reconstructed pads have the correct secret-conditioned law. Test via one 2-of-2 Gaussian conditional sampling / IND-CPA toy, deliberately avoiding CGS-11's key-share reconstruction obstruction.

**POSITIVE CONTROL [DERIVED]:** Over odd prime field Fq, share zeta using f(X)=zeta+rX, so pad shares (alpha,beta)=(zeta+r,zeta+2r). A corrupted alpha is uniform independent of zeta and sigma. If the sampler is *given* sigma, sample zeta' from D_Z,sigma and output beta'=2alpha-zeta' modq. This is EXACTLY the conditional distribution of the honest pad share. More generally <T Shamir evaluations alone reveal nothing about zeta and can be extended to valid degree-(T-1) polynomials conditioned on a fresh sampled secret.

**ONE NEGATIVE AUXILIARY-INPUT TEST [DERIVED]:** An externally hidden bit b is published only as c=Enc_PKE(b) under an IND-CPA secure encryption. Set Gaussian width sigma_b=8 if b=0 and 16 if b=1. Corrupted external Shamir share of b and corrupted pad share alpha are independent uniform Fq, exactly simulatable from ciphertext c without b. Hypothetical PPT RSample_Aux(c, corrupt-key-share, alpha) produces honest pad share beta and is required to make the **FULL joint padding output** computationally indistinguishable from real samples for BOTH b. For q=257, let reconstructed zeta=center_257(2alpha-beta), and use test E=[|zeta|>=8]. Strictly tail-certified Gaussian sums yield
`P(E|b=0)=0.0182938871081869...`, `P(E|b=1)=0.2395206177804640...`, gap `>0.22122673067227`.
The certified omitted Gaussian tail for width 16 using |z|<=128 is <4.263e-89, for width 8 <3.483e-355. An IND-CPA adversary given challenge c samples corrupt shares independently uniformly, calls RSample_Aux, and outputs E. Its IND-CPA success advantage is >0.1106133653-negl, contradiction. For asymptotic analysis q can grow polynomially with lambda; q=257 is only the smallest numerical illustration. This is a **strong auxiliary-state FULL-vector simulation impossibility in a hidden-bit toy**, NOT an attack or impossibility theorem for real LWE FHE or all PCFs.

**CRITICAL SECURITY-SEPARATION:** An adversary corrupting fewer than threshold parties can see only its own *raw* padding shares, which are uniform and trivially simulatable. Source Algorithm5 gives it masked partial-decryption shares, not all original pad shares. Theorem6.3 p28 already replaces `-e+zeta` with a distribution having PUBLIC width; this motivates a weaker `transcript-only` simulation interface. The negative auxiliary-full-vector toy does NOT refute that weaker interface. New PCF security/composition theorems are still required to handle publicly linked FHE keys, adaptive sid, authorized active subsets and all observable shares. No original paper flaw, novel primitive or speedup claimed. NOVELTY NOT VERIFIED.

**Reproducibility:** Complete local research note: `/mnt/data/CGS-12_padding_only_auxiliary_reverse_sampling_gate.md` SHA256 `6813c47bb61de893ad06c162a3a78490c3e129e6935f0a1251cb0439eafc3876`. Deterministic local Gaussian certificate script `/mnt/data/thfhe_cgs12_padding_only_reverse_sampling_gate.py` SHA256 `81881c0bc9f4f887727ac5a9a93bd357b19d42fcdb6f3f010b6585c41aad4621`. JSON `/mnt/data/thfhe_cgs12_padding_only_reverse_sampling_results.json` SHA256 `08bfb8f83a8c38ca7712ef59747ad261c14f97b47c70b7eb4fceb701b82524fa`. Scripts tested exact finite-field relations and mathematical Gaussian tail bounds; no simulation of PKE insecurity required.

**STATUS:** PASS parameter-known exact padding-only reverse sampler; FAIL parameter-blind full-output auxiliary-input reverse sampling for one IND-CPA toy; actual Threshold FHE security/efficiency UNCLEAR.
**RESULT:** Correct target is likely combined decryption-transcript simulation, not raw full-pad-vector correlation sampling. Original source Theorem6.3 already proves an s-free aggregate-noise hybrid for the baseline.
**NEXT_ACTION (CGS-13, PI continuation):** Read Algorithm5 pp23–24, Lemma6.1 pp26–27 and Theorem6.3 p28 in source 2025/409. Define ONE exact transcript-only correlation interface and test whether fresh nonce-derived padding shares could use the existing aggregate-noise hybrid while preserving all corrupted-party views and adaptive qualified active sets; seek ONE cheapest falsifier, not further width-factor enumeration or toy PKE.
**STATE_UPDATE:** NO to global/vFHE STATE.md; CGS topic append only.


---

## CGS-13 — adaptive decryption transcript freshness is an independent obligation (2026-10-14)

**Independent CGS track; ONE hypothesis / ONE decisive two-session test.** Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md (start blob `81afc8e0eec830370b19756824cab07e576f5435`) and CGS-12 before testing. No updates to frozen global I or independent vFHE V states.

### Primary source verification [FACT]

Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, mirror PDF 40 physical pp SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED; re-read directly: Lemma5.1 physical pp20–21 Eq.(13) (unpadded residual `e`); Algorithm5 p23 (ODec reveals `ctdec` AND all active partial shares to adversary); Algorithm6 p26 line9 (Shamir-shared `ζ^(sid)`, PRF masks); Theorem6.2 p27 Eq.(24) (sum of partial shares); Theorem6.3 p28 (aggregate-noise simulation using Lemma6.1). Important non-collusion of original server with parties does not prevent the **Algorithm5 adversarial oracle** from returning the all-active partial-share transcript.

### Primary hypothesis and cheapest falsifier

**H-CGS13 [HYPOTHESIS]:** If a compact seeded generator delivers individually correct `D_(Z,σ(s))` Gaussian padding marginals for each `sid` and preserves all-qualified-set Shamir reconstruction, the existing Theorem6.3 proof can be reused without a further *joint/multi-sid security condition*.

**[DERIVED public observable from exact source algebra]:** For `ctdec=(a,b)`, known chosen plaintext `µ`, and all active partial-decryption shares, Eq.(13)+Eq.(24) give the efficiently observable
`
R_sid = b−Σ_(i∈act) pd_i−floor(q/2)µ
      = e_sid−ζ^(sid) mod q.
`
Secret terms `a^T s` and all honest/corrupt PRF masks cancel. This holds for every qualified `act`. Thus source-visible *aggregate transcript* can expose cross-session padding correlations even though raw honest pad shares are hidden.

**ONE exact two-session test [DERIVED / analytic, explicit idealized noise model]:** Compare two worlds with `e1,e2 iid D_(Z,σ)`, `σ²=64*114243=7311552`, prime `q=1000003`; this is a **Gaussianized toy source-residual model**, NOT the exact original rounded/flooded e. For two sessions, the **Fresh** world samples independent `ζ1,ζ2∼D_(Z,σ)` and outputs `R_j=e_j−ζ_j modq`; the **Reused** world uses a single `ζ∼D_(Z,σ)` and outputs `R_j=e_j−ζ modq`. Both worlds have EXACTLY equal one-session residual marginals and correctly reconstructable Shamir padding secrets. Choose the field character
`F(R1,R2)=cos(2π*185*(R1−R2)/1000003)`.
Using centered discrete Gaussian characteristic `φ_σ(t)` (Poisson summation) with `t=185/1000003`, obtain
`
E_Fresh F = φ_σ(t)^4 ≈ 0.04308575212909598,
E_Reused F = φ_σ(t)^2 ≈ 0.20757107729425114.
`
Analytic dual Gaussian-series upper/lower bounds (NOT Monte Carlo) certify
`
TV(Fresh_joint, Reused_joint)
≥ [φ_σ(t)^2*(1−φ_σ(t)^2)]/2
> 0.08224.
`
Since `t=185/q`, the Fourier character is well-defined on residues mod q, with NO wraparound assumption. The gap is between TWO TOY JOINT TRANSCRIPT DISTRIBUTIONS, not a claimed source-protocol attack or a verified source-parameter instantiation.

**[COMPUTED exact sanity]:** At q=1000003, for 2-of-4 Shamir `f_s(X)=23+13X`, `f_ζ(X)=17+19X`, a=71, e=29, µ=0, arbitrary masks `m_i=100+7i`, all three qualified active sets `{1,2}`, `{2,4}`, `{1,2,3}` recover observable `R=12=e−ζ` exactly. This is a deterministic algebra check, not security evidence.

### Scientific boundary and next protocol interface

**FAIL:** One-session marginal Gaussian distribution correctness + qualified-subset Shamir correctness DO NOT imply multi-query transcript security. At least a **joint cross-sid** guarantee must be proved. This is a known general correlation/freshness pitfall, not a new ThFHE attack or novel primitive.

**CONDITIONAL COMPOSITION [DERIVED, not construction]:** A suitable replacement property must be defined for the complete adaptive observable transcript, conditioning on corrupted parties' *FHE secret shares, PCF evaluation keys/seeds, and all past responses*, including public FHE pk, nonces and varying qualified act. If the seeded real transcript and original independent-pad transcript satisfy computational indistinguishability with advantage `Adv_replace`, then the source Theorem6.3 gives `Adv_ThFHE(seeded) ≤ Adv_replace+Adv_ThFHE(original)` via triangle inequality. This does NOT provide a PCF satisfying `Adv_replace`. Actual source `e` is rounded/flooded with a potentially different width and joint dependence, and has NOT been instantiated by the Gaussianized toy; a full source security proof remains OPEN.

**Reproducibility:** Local full report `/mnt/data/CGS-13_threshold_FHE_joint_transcript_freshness_gate.md`, SHA256 `1337682a55d0dcdb4db30ddc1f753709af5debf19c5b59020a8d18b742d004a1`; deterministic analytical-check script `/mnt/data/thfhe_cgs13_joint_transcript_fourier_gate.py`, SHA256 `4f298bce25dd8b63ab6797bf2ba1e8c35a2a430a93c13d85594de7acb2045779`; JSON results `/mnt/data/thfhe_cgs13_joint_transcript_fourier_results.json`, SHA256 `7e6ec091312c36561ca552cfed1682efb2bbe766c677ce8e06b7895c1be18913`. Local files, not silently stored in GitHub.

**STATUS:** **FAIL** H-CGS13 marginal-sufficiency claim; **PASS** explicit source public-residual formula and certified two-query Gaussianized-model Fourier gap; **UNCLEAR/HUMAN_REVIEW** actual seed-conditioned ThFHE PCF transcript composition.

**RESULT:** Exact per-session distribution and Shamir reconstruction are insufficient; an independent adaptive joint-transcript indistinguishability condition is required before applying source multi-query Theorem6.3. No proof gap or vulnerability of original source established.

**NEXT_ACTION (CGS-14; only after PI next continuation):** Select ONE named published PCF/PRSS construction with a precise adaptive multi-nonce security game, and test its security definitions against the **source-visible transcript replacement** property with pre-existing public FHE pk, corrupted FHE secret shares and PCF keys. Identify ONE concrete missing condition or prove one smallest compatible hybrid lemma. Do not repeat trivial reuse examples, coefficient enumeration or old Shamir-square attacks.

**STATE_UPDATE:** NO to global/vFHE STATE.md; CGS topic append only.


---
## CGS-15 — Ideal public-circuit PCF vs hidden FHE norm (2026-10-14)

**Independent CGS track. ONE hypothesis/test.** Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md (global I192 frozen, vFHE V15 independently active), and topic history. The prior CGS-14 full report is local only, not falsely claimed to be already committed.

**Primary sources [FACT]:** Abram–Scholl–Yakoubov ePrint 2022/535, original pp43–48: Definition7.1 specifies public circuit description C as input to ideal Public-Key PCF Eval, with Section7 expressly treating correlations without master secrets; Theorem7.8 builds a general ideal PCF using reusable DUS, ROM and PKE. Section7.2 p48 generates an encrypted output under each participant's PKE key. PDF SHA256 01049b2f0bd222fad71ee380838f3409ef560b75da02521b29b0d6d65c6bb0b3, version unverified. Okada–Takagi ePrint 2025/409 §1.2 p4 cites O(LDec) pre-shared-pad storage as open; Algorithm6 p26 specifies existing hidden FHE s and Gaussian padded Shamir shares with squared scale sigma0²(Bpub²−||s||²). Source PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, parity unverified.

**H-CGS15:** The unmodified Section7 public-circuit PCF can directly provide per-session Shamir Gaussian shares conditioned on an already existing hidden FHE s, with neither new secret-input joint initialization nor norm leakage.

**ONE source-interface test [FAIL]:** With source-shaped Bpub=338, sigma0=8, n=128, compare bounded secret vectors s_A=(1,0,...) and s_B=(1,1,0,...). Their squared norms are 1 and2, hence M=Bpub²−||s||² is 114243 and114242. (A) A literal public correlation circuit C_M whose Gaussian width M is an explicit embedded constant leaks secret norm² exactly. (B) A single fixed C with no s-dependent input, setup or random coins has an identical output law in both worlds and cannot realize both exact discrete Gaussians. The distribution distinction follows from Pr(1)/Pr(0)=exp(−pi/(64M)), with difference 3.761095105975e-12. This DOES NOT prove a negligible-distance lower bound in all real security parameterizations and DOES NOT rule out additional private-input/obfuscation mechanisms, which require new construction and proofs beyond Theorem7.8.

**Cost gate [SOURCE-BASED COUNT]:** Section7.2 encrypts the N-element correlation output vector under N participant public keys for a full Sample invocation. N full redundant executions would perform N² encryptions in the naive literal deployment. This is NOT a universal computational lower bound nor real-world benchmark.

**STATUS:** FAIL direct public-C integration; PASS original source interface/cost check; real hidden-s correlation protocol UNCLEAR/HUMAN_REVIEW.
**RESULT:** The strongest general C-selected published mechanism still needs a hidden FHE state-binding interface; original ThFHE O(LDec) storage and corrupted-share transcript proof remain open. No novelty or paper flaw claimed.
**NEXT_ACTION:** Recommend PARK generic PCF-integration branch for PI decision, unless a concrete secret-conditioned joint-init protocol with a joint-view simulator and competitive cost is identified. Do not continue generic interface counterexamples.
**STATE_UPDATE:** NO global/vFHE STATE.md writes. Only independent CGS topic append.

Full local CGS-15 report: /mnt/data/CGS-15_ideal_pcf_public_circuit_secret_binding_gate.md; SHA256 ed89d4e2de395d05c23e4c8389c24faf521e2f06989b30cae5e7100ae519b7bf. Repro script /mnt/data/thfhe_cgs15_ideal_pcf_circuit_gate.py; SHA256 5146aa856e8ebb8488bf9aa3cee0ce0dcf59d94c805c39f17a71b5425886baa2; JSON results SHA256 69f4696cb0cc0ed5cfc6550ff232766fdaa059fc1225240095cc6d44cbcc5256.


---
## CGS-16 — published PRSS-flooding alternative and source margin incompatibility gate (2026-10-14)

**ONE primary hypothesis:** Noah's Ark's original source-supported on-demand bounded-uniform PRSS noise flooding can simply replace Okada–Takagi Algorithm6's per-sid secret-norm-conditioned Gaussian Shamir padding **without additional modulus/noise-gap expansion**, while inheriting Noah's Ark security and correctness proof.

**Original papers [FACT]:**
- Dahl et al., *Noah's Ark: Efficient Threshold-FHE Using Noise Flooding*, ePrint 2023/815, https://eprint.iacr.org/2023/815. Retrieved full original 33 physical-page PDF through Research MCP (mirror SHA256 2c81ae1da13de8b6ae8e7499ec486e329ddb9166fbfc189c634f15a4407fba50, VERSION_UNVERIFIED). Source §4.1 pp19–21 Figures12–14 and Theorem4.1; §4.2 pp23–24; Switch-n-Squash pp16–18 Table1 p17. For small binomial(n,t), PRSS.Init distributes seeds indexed by subsets A; every decryption consumes PRSS.Next()+PRSS.Next(), producing a bounded uniform-sum flooding value with fresh counters and NOT pre-stored Gaussian pads. For large binomial(n,t), original §4.2 uses per-session consumed preprocessed random-bit sharings or fresh online MPC, and is NOT an unbounded constant-preprocessing scheme.
- Okada and Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint 2025/409, 40 physical-page mirror SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED; §1.2 p4 flags O(LDec) stored Gaussian pad shares; Algorithm6 p26 samples D_Z,sigma0 sqrt(Bpub²−||s||²) per sid, conditional on external hidden FHE s. This is a DIFFERENT distribution/parameter/proof than bounded uniform PRSS flooding.
- Zama public source https://github.com/zama-ai/threshold-fhe README + docs/threshold-benchmark.md shows separate prss-init, explicit preproc-decrypt --num-ctxts 10, threshold-decrypt --preproc-sid 3 operations for a noise-flood-small example. This corroborates a concrete industrial *workflow*, not an inference that all source Protocol1 variants require per-query preprocessing. Repo README now warns this public snapshot is not actively maintained and points to kms/core/threshold.

**ONE exact compatibility test [DERIVED]:** Noah's Ark original §4.1 p20–21 published sufficient conditions are (1) pow >= stat+log2(binomial(n,t)), and (2) 2^(pow+1) B_d <= Delta'/2, where for binary plaintext Delta'=Q/2. Thus both sufficient conditions together REQUIRE Q/B_d >= 2^(stat+3)*binomial(n,t). For source-compatible example n=4, t=1, binomial=4: at stat=40, pow_min=42 requires Q/B_d >=2^45=35,184,372,088,832; at stat=128, pow_min=130 requires >=2^133. Exact integer derivation and code checked.

**[FACT source comparison]** The Noah's Ark Table1 p17 uses Q=2^128, pow=47, while p18 describes Bd approximately 2^70, leaving Q/Bd approx 2^58 vs minimum 2^50: around eight bits of margin in that illustrative source design. It explicitly *creates* this gap by Switch-n-Squash bootstrapping/modulus expansion. Okada–Takagi Theorem6.2 p27 sizes q as sigma_dec times an Omega(kappa) correctness growth term, not as a universal upper bound: **cannot prove that every legal larger q choice is incompatible**. We only reject the unsupported claim that the original source proof automatically works after an unchanged, noise-tight direct substitution: polynomial Q/Bd margin fails an exponential sufficient inequality for stat linear in kappa. This is a theorem-applicability gate, NOT a universal lower bound, original-paper flaw, or end-to-end benchmark.

**STATUS:** FAIL direct unchanged-gap PRSS-flooding substitution; PASS primary-source mechanism identification and exact noise budget; broader cross-scheme adaptation UNCLEAR/HUMAN_REVIEW.
**RESULT:** A published alternative already eliminates per-decryption pre-stored Gaussian pads *in the small-corruption-threshold Noah's Ark model* by using seeded PRSS + modulus/noise-gap expansion. A nontrivial bridge to arbitrary T-out-of-N Okada–Takagi would require redesigned parameters, proof, bootstrapping overhead evaluation and corrupt-view/compact-share security. It would not be original to reintroduce Switch-n-Squash itself.
**REPRODUCIBILITY:** local full CGS-16 report /mnt/data/CGS-16_noahs_ark_prss_margin_gate.md SHA256 1e3fd77637f1aceca40f9a863bef0c057fc58abba1fe8164b36316fa5ad3d3b3; executable gate /mnt/data/thfhe_cgs16_noahs_ark_margin_gate.py SHA256 1fefa061f9494dda581f3f9568b67a3d973f7c66eec22f7b4a047debc756bea4; results /mnt/data/thfhe_cgs16_noahs_ark_margin_results.json SHA256 8e10916b7d7c14e8c5822e73035993e0eaf825bd5de47c6b46869d4502f722f5.
**NEXT_ACTION (CGS-17 only after PI continuation):** PARK generic PCF interface-attack subbranch; test ONE specific parameter bridge: can a cheaper modulus/noise-gap change preserve Okada–Takagi arbitrary T-out-of-N compact shares and adaptively simulated decryptions, with credible cost advantage over Noah's Ark Switch-n-Squash? Otherwise recommend ARCHIVE of broad Gaussian/PCF ThFHE branch and pivot to a fresh concrete FHE target.
**STATE_UPDATE:** CGS topic only, do not alter frozen global I or parallel vFHE STATE.md.


---
## CGS-17 — Noah's Ark subset-PRSS scaling and modulus-gap cost gate (2026-10-14)

**ONE hypothesis / ONE explicit feasibility test:** Merely enlarging the decryption modulus/noise gap while literally retaining Noah's Ark ePrint 2023/815 Figure 12 subset-seed PRSS can give a scalable low-storage bridge to Okada–Takagi 2025/409 arbitrary T-out-of-N threshold decryption. Test N=32, T=11, t=T-1=10, still within Noah's Ark's t<N/3 robustness regime.

**Primary-source audit [FACT]:** Dahl et al., *Noah's Ark: Efficient Threshold-FHE Using Noise Flooding*, https://eprint.iacr.org/2023/815, original full 33-page Research MCP PDF SHA256 2c81ae1da13de8b6ae8e7499ec486e329ddb9166fbfc189c634f15a4407fba50, VERSION_UNVERIFIED: §4.1 p19 explicitly warns about binomial(n,t) growth; Figure12 p20 calls PRSS.Init once for each subset A of size n-t and PRSS.Next locally evaluates ψ(r_A,cnt) for each A containing party i; Figure13 p20 invokes PRSS.Next twice per decryption; §4.1 pp20-21 imposes pow>=stat+log2(binomial(n,t)) and 2^(pow+1)Bd<=Delta'/2; §4.2 p23 supplies an alternative large-subset offline-MPC random-bit-sharing phase, which must be consumed or freshly generated each session. Okada–Takagi, https://eprint.iacr.org/2025/409, full 40-page PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED: §1.2 p4 defines compactness of key/ciphertext/share sizes w.r.t. N and flags O(LDec) padding storage; Algorithm6 p26 has secret-dependent Gaussian pads shared per session. Do not equate source native q with Noah's Ark post-switch Q.

**One exact combinatorial-resource falsifier [DERIVATION]:** N=32,t=10 gives 3t=30<32; system-wide subset/seed agreements C(32,10)=64,512,240; seed subsets containing a fixed participant C(31,10)=44,352,165 (NOT C(31,9)). With 128-bit seed material, each party holds 709,634,640 bytes=676.7603302 MiB in literal r_A alone, excluding coefficients/keys. Exactly two PRSS.Next calls give 88,704,330 per-party PRF summands per decryption in the unoptimized Figure12 computation. These are exact counts, NOT empirical timings or any lower bound on alternative generalized PRSS/PCFs.

**Same test's modulus-budget check:** For binary plaintext Delta'=Q/2, combined published sufficient inequalities imply Q/Bd>=2^(pow+3). Integer pow_min=stat+ceil(log2 C(32,10))=stat+26: at stat40, pow_min66 and Q/Bd>=2^69; at stat128, pow_min154 and ratio>=2^157. Increasing Q does not change the above seed explosion. These are sufficient-theorem applicability conditions of this specific flooding protocol, not universal impossibility bounds.

**Explicit apples-to-apples illustration [CONDITIONAL]:** If a pad share and a PRF seed are BOTH assumed exactly 16 bytes, then LDec=1,000,000 original pre-shared pads would cost 16,000,000 bytes/party, versus 709,634,640 bytes of literal Noah subset-PRSS seeds, ratio 44.352165. Equal-unit storage crosses over only at LDec=44,352,165. Native field-element width is not determined from these source assumptions: no claim of a measured full-system speedup/slowdown.

**Source-respecting limits:** Noah's Ark acknowledges this very scalability issue and switches to offline MPC for large binomial(n,t); this does not magically eliminate fresh per-session preprocessing or require the exact same corruption/security functionality as Okada–Takagi. The source's output decryption shares may still be compact w.r.t. N even though PRSS seed state is not. Nor can Noah's Ark's t<n/3 robustness theorem establish Okada–Takagi's arbitrary T-out-of-N guarantee. This is a negative direct-bridge assessment, NOT a new theorem, source flaw or universal ThFHE impossibility.

**STATUS:** FAIL named literal modulus-only subset-PRSS bridge; PASS source audit and exact cost arithmetic; HUMAN_REVIEW parent direction.
**RESULT:** Even in Noah's Ark's supported corruption range, one N32 T11 instantiation requires ~44.35M seeds/party, ~88.70M PRF terms/decryption and large output modulus margin. There is no source-backed advantage over the paper's own offline MPC alternative or over Okada–Takagi from only tuning Q.
**NEXT_ACTION:** Recommend PARK/ARCHIVE direct generic CGS Gaussian/PCF/Noah-PRSS integration for PI decision; preserve original O(LDec) problem OPEN. Reopen only with a concrete secret-conditioned joint correlation mechanism or a demonstrably lower-cost flooding protocol with full simulator and all-qualified-set compatibility. Otherwise pivot to an independently chosen FHE research target rather than more elementary bridge counterexamples.
**STATE_UPDATE:** Only independent CGS topic append; DO NOT alter global/vFHE STATE.md or auto-archive without PI decision.

**Local proof artifacts (all exact hashes):** /mnt/data/CGS-17_threshold_FHE_PRSS_combinatorial_cost_gate.md SHA256 5486c8a1d273828f048c75b619148fe368d98c181d4878aec8dcda572983061e; /mnt/data/thfhe_cgs17_noahs_ark_subset_gate.py SHA256 55eed74d3aff6bfb85296c9536807eab0da931d311fcb94c824fd45d92ec7478; /mnt/data/thfhe_cgs17_noahs_ark_subset_results.json SHA256 475bc696272806d11d1d6849f396fb9b7221a3f0eabc25b47cf55d554ccdfab7.


---
## CGS-18 — Masked rounding alternative, authors' prior art, exact carry arithmetic (2026-10-15)

**PRIMARY HYPOTHESIS:** With interactive secure comparison and consistently double-shared fresh uniform masks, a divisible-modulus decryption residual can be unmasked and corrected exactly without a secret-conditioned Gaussian pad. The masked opened residue remains perfectly uniform.

**RESULT:** PASS the narrowly specified exact identity and 960/960 exhaustive toy (0 corrected errors, 224 naive no-carry mismatches, all opened masked-value distributions uniform). The comparison and underlying protocol are **ALREADY PUBLISHED**: Ajax ePrint2025/1834 (USENIX Security2026) double sharing/mask-then-open; Zyskind et al. ePrint2025/1781 (CCS2025) private comparator/UC MPC rounding. No new primitive or complete source Algo6 repair claimed. Published protocols consume per-decryption offline correlations/gates; using online MPC instead changes rounds/communication and remains unproven in original arbitrary T-of-N, sanitizing ServerDec, prime-q interface. Gaussian sampling problem under original constraints remains OPEN.

**EVIDENCE:** `findings/cgs-18-masked-carry-no-gaussian-alternative-gate.md` (source locations, exhaustive script SHA, correctness/privacy scope and novelty gate).
**STATUS:** narrow algebraic PASS; novelty of standalone mechanism FAIL (known prior art); full candidate UNCLEAR / HUMAN_REVIEW.
**NEXT_ACTION (only PI continuation):** ONE cost/security interface test of source Algo6 against (a) CCS2025 preprocessed rounder and (b) on-demand comparator, with exact user-selected T,N and threat model; no further generic PRSS/PCF substitutions or automatic research-track pivot.
**STATE_UPDATE:** YES CGS topic only; no edits to SHIP/VFHE/global.
---
## CGS-19 — Source-fixed secure rounding online/offline storage gate (2026-10-15)

**H-CGS19 (FALSIFIED direct-port dual objective):** Published CCS 2025 UC MPC rounding, optionally moved on demand, can directly replace the original Gaussian padding while preserving Okada–Takagi Algorithm 6's one-local-share/party PartDec and eliminating all per-decryption O(LDec) preprocessing. Fixed N=4,T=2 with at most one corrupt active party and a noncolluding semi-trusted Server (no claim CCS shares same setting).

**MINIMAL DECISIVE SOURCE/COST TEST:** Exact CCS2025 §3.4 published k64,m1,b8,d8,s64 equations give 2432 consumed gate-table entries and 346880 bits=43360 bytes authenticated preprocessed gate material per party per decryption. Original Algo6 stores one q-element Gaussian share per session per party and sends one q-element PartDec reply; CCS published online has THREE sequential ABB opens and 656 bits/party excluding commitments, not a one-reply protocol. At LDec=10^6, full precomputed CCS gate payload is 43.36 GB/party; original Gaussian shares at illustrative qbit64/128/256 are 8/16/32 MB respectively. These cross-paper q widths are ILLUSTRATIVE, and NOT same security parameters, threat model, or proof systems. On-demand regeneration removes permanent preproc tables only by adding new live interactive MPC/OT steps in the named source method, with online cost not demonstrated to match original.

**REFERENCES:** Okada–Takagi ePrint2025/409 Algo6 p26 and Def4.2; Zyskind et al. ePrint2025/1781 §§3.3–3.4 pp7–8 Eq5; Ajax ePrint2025/1834 §§2.2,4.3 pp5–6,16–18. Newer Okada–Takagi ePrint2026/957 published at ACISP 2026, but ORIGINAL FULL TEXT SOURCE_BLOCKED, so novelty cannot be certified.

**STATUS:** FAIL for *named literal port preserving both claimed properties*; PASS verified formula/data-flow gate; no impossibility theorem for novel PCFs or on-demand MPC, no end-to-end implementation/simulator and no fresh cryptographic primitive. **PARK this direct integration**, but original O(LDec) research question OPEN.

**FULL EVIDENCE:** `findings/cgs-19-interactive-rounding-online-offline-cost-gate.md`; local exact formula script `/mnt/data/cgs19_gate_check.py` SHA256 7e2fa46ed69778601cfa59b5a69bbffcd4fa4345a1ec0e7e3d56a84a58849340; JSON `/mnt/data/cgs19_cost_gate.json` SHA256 5b993bd1c4baea6146917eb15720cd3e52293370f2e38bd02df3fb1e5da3012f.

**NEXT_ACTION CGS-20 (PI continuation only):** one genuinely new compact reusable-key conditional-correlation or other nontrivial construction within ONE-response interface, exact source transcript simulator/active-set and two-secret/two-session falsification; alternatively first secure original full 2026/957 source to gate novelty. Do not repeat prior-art Ajax/CCS MPC rounding with no new mechanism; never switch SHIP/VFHE. **STATE_UPDATE:** YES CGS only.
---
## CGS-20 — Exact scalar-field key-homomorphic PRF has a public linear distinguisher (2026-10-15)

**H-CGS20 [FAIL]:** A compact `F_q^d` key vector (Shamir-shared across parties) and exact additive key-homomorphic PRF `F(k,sid) in F_q` enable no-interaction on-demand polynomially many coherent pseudo-random Shamir output shares while retaining the original one-reply interface. This strict construction cannot be a secure PRF, independent of eventual Gaussian sampling.

**DECISIVE THEOREM [DERIVED]:** Since `F` is exactly linear in key, on any `d+1` distinct `sid_i` the public `(d+1)×d` matrix of evaluations on standard unit keys has a public nonzero left-kernel vector `alpha`. Then `Σ alpha_i F(k,sid_i)=0` for ALL secret keys, whereas the relation holds with probability exactly `1/q` for a truly random scalar-field function. Hence `d+1`-query PRF distinguishing advantage **`1-1/q`** for polynomial `d`. Full algebra in `findings/cgs-20-exact-scalar-key-homomorphic-prf-no-go.md`.

**MINIMAL EXACT TOY:** `q=101,d=3`, four queries. Public `alpha=(22,20,79,1)`; 10000/10000 family outputs satisfy relation, vs 105/10000 independent uniformly sampled random-function quadruples (theory 1/101). Reproducer `/mnt/data/cgs20_exact_scalar_khprf_linear_attack.py` SHA256 `3d47be2657a25984d9b07d128ed6f86604a9ecb62e437d304beefea6fc52691d`; JSON `/mnt/data/cgs20_exact_scalar_khprf_results.json` SHA256 `0cbc89685a09814cd01eadc914c7f7610e11e90c7a4e4db603ef1a250b9993c9`.

**PRIOR ART / BOUNDARIES:** Published actual DPRFs and key-homomorphic PRFs (Boneh et al. CRYPTO2013; Libert–Stehlé–Titiu TCC2018/ePrint2018/927; Sam Kim ePrint2020/233) use more nuanced GROUP or approximately homomorphic/rounded output; our FIELD-linear scalar no-go does not apply to arbitrary DPRFs and is not claimed a new theorem. Even a sound DPRF does NOT automatically realize secret-conditioned Gaussian joint distributions or same-degree Shamir shares after nonlinear sampling. Full Okada–Takagi 2026/957 source remains inaccessible. No author-contact, no unrelated edits.

**STATUS:** FAIL exact field-key-linear PRF shortcut; PASS formal distinguisher and toy; GENERAL CGS target OPEN / HUMAN_REVIEW. **NEXT_ACTION CGS-21** (PI continuation only): read one actual published DPRF construction and test one concrete almost-key-homomorphic/group-output → *same-degree Shamir Gaussian* conversion with a two-subset/two-session falsifier and realistic cost/security. Otherwise PARK this exact-PRF integration branch. **STATE_UPDATE: YES, CGS ONLY.**
---

## CGS-21 — LST18 DPRF local-rounding-to-Shamir interface gate (2026-10-15)

**PRIMARY HYPOTHESIS [FAIL]:** Actual published noninteractive LWE DPRF partial outputs can be locally transformed by rounding / nonlinear Gaussian postprocessing into a coherent same-degree Shamir Gaussian share, preserving any T-out-of-N reconstruction **without additional online steps or special setup**.

**[SOURCE FACT]** Libert–Stehlé–Titiu, *Adaptively Secure Distributed PRFs from LWE*, TCC 2018/ePrint2018/927 §4.1 (physical pp18–20), uses **integer LISS** (not Okada's field Shamir), local output `Z_p^{m×d_j}`, Combine performs **linear combination first**, then **coarse rounding and extractor π**. Lemma4.1 proves final reconstructed DPRF consistency with overwhelming probability under its modulus-gap assumptions; it does **not** give same-degree Shamir shares of its final output or of a Gaussian sample. Okada–Takagi ePrint2025/409 Algorithm6 p26 still needs secret-conditioned hidden Gaussian padding shares and the Theorem6.3 joint-view simulator.

**[ONE DECISIVE TEST, EXACT]** Hypothetical 2-of-3 Shamir field F101, f(X)=23+11X (shares 34,45,56), two nonce-selectable local maps g_a(x)=nearest_integer(17*((a x) mod101)/101) mod17 with a=1,3. At a=1, local outputs 6,8,9 give legal sets {1,2} -> 4, {2,3} -> 6, while central g_a(23)=4. At a=3, local outputs 0,6,11 give {1,2} -> 11, {2,3} -> 13, central g_a(23)=12. These are **NOT** the source DPRF's native parameters or LISS, and NO source attack is claimed; they falsify an unmodified nonlinear `PEval_i→Gaussian_i` **Shamir adaptation**. For odd prime field q, preserving every affine-Shamir triple with same-field g mathematically forces g to be affine, by Jensen/additivity; separate from cross-field toy and not claimed a new theorem.

**EVIDENCE:** `findings/cgs-21-dprf-local-rounding-shamir-interface-gate.md` contains full paper/section references, proof and caveats. Local reproducer `/mnt/data/cgs21_local_rounding_shamir_gate.py` SHA256 45aa83cf826059e1c2d9d19e0b8f2524bd888704a3217f619b7e179f55188009 and JSON SHA256 01df98af4f18b4d4c6cb2704989e7e6a0c3ffe1dc439f48d857a827cb7ef0dc1; local, not stored in GitHub.

**STATUS:** FAIL naive local nonlinear DPRF-output adaptation; PASS full original paper interface audit, same-plaintext/two-session/two-subset toy and conditional same-field lemma; **GENERAL CGS OPEN / HUMAN_REVIEW**, no novelty asserted.

**NEXT_ACTION (CGS-22, PI continuation only):** Select ONE explicit hidden-output threshold PRF/PCF functionality; design a secret-conditioned Gaussian *shared* output interface that keeps final random seed hidden, then perform a minimal corrupt-view simulation/test with honest active-set consistency and online/setup cost. If concrete special mechanism cannot be identified, PARK this DPRF-based subbranch rather than repeating generic degree/correctness failures. Validate author's 2026/957 primary text before novelty. **STATE_UPDATE: YES, CGS topic + single global STATE.**
---
## CGS-22 — Signed-monomial covariance flattening and native MLWE interface test (2026-10-15)

**H-CGS22 [FAIL as a complete direct bridge]:** Encode binary polynomial secret `s(X)=Σ_j s_j X^j` as `n` ring-secret components `S_j=(2s_j−1)X^j`, so covariance `Σ_S=nI` is known and every component has min singular value 1; hypothesize a direct old-RLWE-to-standard-uniform-MLWE ciphertext embedding with cheap overhead, avoiding all O(LDec) conditional padding.

**POSITIVE ALGEBRA:** Signed monomial multiplication matrices are orthogonal signed permutations, `Σ_j mat(S_j)mat(S_j)^T=nI`. For public H=ΣX^j, `s=(H+Σ_j S_j)/2`; each original RLWE sample `(a,b=a*s+e)` maps to `A'_j=a/2` for all j and `b'=b−aH/2=Σ_j A'_j*S_j+e`. No decryption-noise algebra is lost.

**DECISIVE NEGATIVE INTERFACE:** Transformed `A'_0=...=A'_(n−1)` with probability 1. A standard `U(R_q^n)` MLWE public vector has this property with probability `q^{-n(n-1)}`; simple public distinguisher advantage `1−q^{-n(n−1)}`. This refutes the **specific direct uniform-MLWE embedding**, not underlying RLWE or all variants. Naive native module rank rises from 1 to n; inherited source FHE/Eval security and efficiency are NOT proved. A NEW independent-uniform `A_j` construction is exactly coefficientwise binary **vector LWE** for the sign secret; possibly useful under different assumptions, but not standard small-rank MLWE nor yet an end-to-end FHE.

**ONE exact test:** n4,q17, all 16 binary secrets satisfy `Σ_S=4I`; 1000 random ciphertext identities PASS; transformed A public-vector equality ALWAYS; uniform MLWE A matching event `17^-12≈1.71638e−15`. Reproducer `/mnt/data/cgs22_sign_monomial_covariance_gate.py` SHA256 `4505f6fcd17814f366a8b3c46696133dae13fea668a8e6f5a9c2483a8ae2bbee`, results JSON SHA256 `77132adc377d3df3593bf1df09c228c8546c9329ed2500e7238a60b19e1a6023`. Detailed derivation and original Okada–Takagi p29–30 refs in `findings/cgs-22-signed-monomial-public-covariance-security-interface.md`.

**STATUS:** PASS necessary covariance ingredient / FAIL direct complete secure standard-MLWE embedding / UNKNOWN native full-FHE security and efficiency, HUMAN_REVIEW original CGS. **NEXT_ACTION CGS-23 (next PI continue):** ONE bounded-small-module-rank fixed-covariance secret family with min-entropy/security test (check complementary sequences/Golay prior art), or park if no credible strong contribution. Original hidden-output Gaussian PCF remains OPEN, not magically solved by this observation. **STATE_UPDATE:** YES single global + CGS detail.

---

## CGS-23 — Binary Golay-pair constant covariance meets low-entropy brute-force gate (2026-10-15)

**H-CGS23 [FAIL as a complete security-compatible substitution]:** Use `k=2` secret-polynomial components sampled from the public binary Davis–Jedwab Golay complementary pair family in lieu of `k=n` monomial lifting. This **does** yield exact public covariance `Sigma_s=2nI`, but a practical 128-bit standard-MLWE secret distribution with cheap decryption is NOT obtained by this named family.

**[SOURCE + MATH]** For binary Golay pairs a,b, `a(X)a(X^-1)+b(X)b(X^-1)=2n` as Laurent polynomials, hence `Gram(a)+Gram(b)=2nI` in `Z[X]/(X^n+1)`. Classical Davis–Jedwab family `n=2^m`, `π∈S_m`, m+2 independent Boolean phases, exact publicly enumerable ordered-pair count `m!2^(m+2)`. This counts the **named explicit family, NOT ALL Golay pairs**. At n1024 m10 there are 14,863,564,800 choices (33.791 bits); n4096 42.835 bits; n16384 52.343 bits. Family does not reach even `2^128` choices until `m=29,n=536870912`. Published Golay geometry is not a novel cryptographic trick and different key distributions need separate security results.

**[ONE EXPERIMENT]** Enumerated exact GDJ pairs for n2/4/8/16, getting 8/32/192/1536 unique pairs, verifying all complementary autocorrelation equations (and exact matrix Gram identity for n≤8). In toy native-uniform-public 2-component MLWE, `n=8,q=257`, iid noise coefficients `{-1,0,1}`, public residual check over all 192 candidates uniquely recovered the correct key in 100/100 seeded samples. Under genuinely uniform (A,u), exact union bound false-positive probability `≤192*(3/257)^8≈6.6192×10^-14`. For any enumerable key family K size M with `[-B,B]^n` noise, a public key-scan distinguisher has advantage at least `1−M((2B+1)/q)^n` under 2B+1<q. Gaussian error requires an explicit tail `δ_B`. This is an **O(M) enumeration cost ceiling** on the named family, not a formal PPT no-go for every asymptotic n.

**FULL EVIDENCE:** `findings/cgs-23-golay-fixed-covariance-low-entropy-gate.md`; runnable `/mnt/data/cgs23_golay_entropy_gate.py` SHA256 15fcd9f4f046e90edc868b028adcc2defb36767812833d891afb19cd484d5f26, results `/mnt/data/cgs23_golay_entropy_gate.json` SHA256 033223fa2640c0360fb7cfb1af4dd5bb8358b516952e582474cd2b7f039ee851. Sources Davis–Jedwab (IEEE Trans IT 1999), Fiedler–Jedwab–Parker JCTA 2008, original Okada–Takagi 2025/409 Algorithm7/Lemma7.1. Real FHE KeyGen/Eval/MLWE proof and source `σ_min(mat(s_i))` lower bounds remain unproved.

**STATUS:** PASS covariance/constant module-rank mathematics; FAIL security of direct Davis–Jedwab key choice; original CGS O(LDec) problem OPEN / HUMAN_REVIEW. **NEXT_ACTION CGS-24 (PI continuation):** search ONE explicit genuinely larger-entropy k≤3 complementary secret family and immediately test support size, independent native-public MLWE security interface and individual singular values; if none viable, PARK this covariance-detour rather than further small-entropy examples. Do not infer a lower bound for all complementary pairs. **STATE_UPDATE:** YES, root and CGS detailed state.

---

## CGS-24 — Negaperiodic complementary secrets: proper covariance family (2026-10-15)

**H-CGS24 [PASS finite-scope]:** The appropriate fixed-Gram rank-2 ±1 negacyclic secret family is the **negaperiodic Golay pairs (NGPs)**, which properly contain the ordinary/aperiodic Golay pairs used in CGS-23. At n=16 they provide >100× more choices and some pairs with both individual minimum singular values ≥1. *No practical 128-bit/high-n hardness or complete FHE result is asserted.*

**PRIMARY SOURCE [FACT]:** Balonin–Đoković, *Negaperiodic Golay pairs and Hadamard matrices*, arXiv1508.00640 §3 equations (6),(8),(10), Definitions 2–3: `NAF_a(d)=AF_a(d)−AF_a(n−d)`; `mat(a)mat(a)^T=Σ_d NAF_a(d)N^d`; ordinary Golay pair = periodic ∩ negaperiodic. Actual Okada–Takagi ePrint2025/409 Algo7 p29/Lemma7.1 p30 requires `Σ_s=Σ_i Gram(s_i)` and an individual spectral lower bound. Ordinary Golay was **sufficient but unnecessarily restrictive**.

**ONE EXACT COMPLETE ENUMERATION:** All `2^(2n)` ordered signed coefficient pairs via exact NAF signature counts, for n2,4,8,16:
`NG=(16,128,4096,557056)` vs ordinary `=(8,32,192,1536)`, at n16 362.67× more NG candidates; `log2(557056)=19.08746` bits. `n16` numerical negacyclic spectral test retained **425984** pairs whose BOTH individual min singular values ≥1 (18.70044 bits). Integer matrix checks done for all n≤8 representative complement classes, identities for all pairs proven by NAF. This is finite enumeration, not a growth estimate at n1024. The n16 557056 count is also known in Egan 2017 Table2 (not a new mathematical count).

**EXTRA IMPLICATION SAME SIGNED-BINARY MODEL:** If `4|n`, the negaperiodic lag1 of *every* signed-binary polynomial satisfies `NAF(1)≡2 (mod4)` because product of signed consecutive terms is −1. Therefore exact covariance-flat `k=3` (or any odd rank) is **impossible** for dense ±1 secrets when `4|n`. This says nothing about ternary/wider integer coefficients or approximate flattening.

**LIMITS/SECURITY:** Original MLWE secret distribution is independently coefficient-sampled, whereas NGP keys have strong global algebraic correlations. No reduction from source's standard MLWE, no full FHE evaluation-key security, no efficient high-min-entropy sampler, no useful large-n guaranteed individual `σ_min` bound, no proof that O(LDec) is eliminated securely while retaining the low-communication scheme. Do not interpret this as a new construction, paper bug or published contribution.

**FULL EVIDENCE:** `findings/cgs-24-negaperiodic-golay-covariance-keyspace-gate.md` including published original §3 math and proof; exact enumerator `/mnt/data/cgs24_ngpair_gate.py` SHA256 `ecf4b698e77b2230d77fc136d3b5e69cb96501eee365c657d03f47ceab4e1f38`; results `/mnt/data/cgs24_ngpair_gate.json` SHA256 `243f7a7960baf45c13f1d06b704498b31fb068208c0b19b30051fdce6f810f14`.

**STATUS:** PASS more accurate necessary sufficient source ring condition and larger finite candidate family; UNKNOWN cryptographic-scale security, user-facing ThFHE open. **NEXT_ACTION CGS-25 (PI continuation):** seek ONE **explicit efficiently samplable NGP subfamily at n≈1024** with **provable minimum entropy ≥128 bits**, individually usable spectral margins, and credible standard LWE/MLWE key-distribution argument, then one decisive attack or constructive bound. If unavailable, PARK covariance-detour and return to true secret-conditioned Gaussian padding. **STATE_UPDATE:** YES root/state plus new finding.

---

## CGS-25 — Recursive negaperiodic doubling: exact keyspace 64.09 bits at n1024; 129.09 only at n32768 (2026-10-15)

**H-CGS25 [FAIL n1024 target]:** An explicitly and uniformly sampled binary rank-two NGP family obtained by repeated shifted-involution doubling from all **557056** n16 NGP base pairs provides **≥128-bit H∞ at n1024**, keeps rank two and exactly source-public `Σ_s=2nI`. Counting the entire image of this ONE explicit family refutes the n1024 entropy target.

**NEW CONCRETE GENERATOR [DERIVED, KNOWN MATHEMATICAL LINEAGE]:** In `Z[X]/(X^(2n)+1)`, let `z=X^(2t+1)` for `t∈{0,...,2n−1}` and input NG-pair `(a,b)∈R_n²`. Output `A=a(X²)+z b*(X²)`, `B=b(X²)−z a*(X²)`. Every output coefficient remains ±1; `AA*+BB*=2(aa*+bb*)=4n`. Even positions recover (a,b) and nonzero b* can be canceled over the cyclotomic field, making all **2n** choices of z distinct. Consequently **uniform base + uniform shifts => EXACT uniform output distribution**, `|K_(2^m)|=17·2^(15+Σ_(j=5)^m j)`. This is an explicit shifted variant of prior-art NGP doubling already recognized by Balonin–Đoković arXiv1508.00640 §3 Proposition3; not claimed mathematical novelty.

**PRIMARY MINIMAL TEST:** `n1024` m10 support `17·2^60` = **64.08746284 bits**, FAIL 128-bit minimum-entropy requirement independent of assumed hardness. By contrast n32768 m15 support `17·2^125` = **129.08746284 bits**, PASS **unfiltered keyspace entropy only**, NOT encryption/MLWE security. At intermediate n2048/4096/8192/16384: 75.087/87.087/100.087/114.087 bits. A public-key bounded-residual scan can enumerate this explicit 1024 family in about `2^64.09` secret guesses; real attack costs include polynomial factors and noise-tail probability. It does not bound ALL NGP families.

**EXACT VERIFICATION:** Re-enumerated all n16 NGPs, validated 32 distinct shifts at n16→32, and tested exact integral negaperiodic correlations on generated chains through n1024. Additional **UNPROVEN** empirical singular-value check: 25 n1024 chains -> 20 meet both individual minima ≥1; 30 n32768 chains -> 26 meet both; observed minimum individual singular 0.508 at n1024 / 0.327 at n32768; FFT numerical only, no universal `c` nor lower bound on filtered entropy. `/mnt/data/cgs25_recursive_negaperiodic_entropy_gate.py` SHA256 89a975c682836b2e2936eb784be9903ea2a8d4d7edfce2714a2ddf66671ee4bb; JSON SHA256 7f40eb995c632ce5f242105930b90c292d26c541a07f4532bc1a550d7b6b9c5e. Full formulas, proof and sources in `findings/cgs-25-recursive-negaperiodic-key-entropy-gate.md`.

**CRYPTOGRAPHIC GATE NOT PASSED:** The original Okada–Takagi 2025/409 Lemma7.1 assumes source `χ_mlwe` secret distribution and usable individual min singular values. Our global recursive NG correlations are outside that source. At n32768 a rigorous high-entropy subfamily with a certified positive `c`, standard (M)LWE hardness, FHE evaluation-key security, and competitive latency/key/ciphertext costs remains UNPROVED. The newer author 2026/957 full text remains retrievable only as metadata (PDF blocked on repeat attempt).

**STATUS:** PASS exact math & constructive family; FAIL 128-bit n1024; UNCLEAR n32768 end-to-end security/cost. **NEXT_ACTION CGS-26 (PI next "继续"):** one decisive structural cryptanalysis **or** uniformly bounded individual spectral/smoothing test at n32768, before further protocol work. If no plausible standard-MLWE reduction/strong entropy-preserving spectrum exists, PARK covariance detour; original O(LDec) secret-conditioned Gaussian open problem persists. **STATE_UPDATE:** YES single root and CGS topic.

---

## CGS-26 — Constant Gram does NOT automatically erase source Gaussian padding (2026-10-15)

**PRIMARY HYPOTHESIS [FAIL direct source-interface]:** Our CGS-25 rank-two recursive NGP fixed Gram `Σ_s=2nI` permits us to put `ζ^(sid)=0` in original Okada–Takagi 2025/409 **unchanged** Algorithm7 while retaining its `Bpub`, Lemma7.1 Eq.(26) residual target and Theorem7.5 simulation proof.

**ONE DECISIVE ORIGINAL-PAPER TEST [SOURCE+DERIVED]:** Lemma7.1 original physical pp30–31 Eq(25): unpadded latent Gaussian covariance `V0=p²σ0²Σ_s+σflood²I`. After the source's secret-conditioned Gaussian, Eq(26): `V1=p²σ0²Bpub²I+σflood²I`. Source p31 sufficient positivity/diagonal-dominance condition is `(Bpub²−1)>kn²Bmlwe²`. For proposed `k=2,Bmlwe=1,n=32768`, `Σ_s=2nI=65536I`, source needs `Bpub²>2147483649`. Minimum integer `Bpub=46341` gives `Bpub²=2147488281`; `Σζ=(Bpub²−2n)I=2147422745I` **strictly positive**, so literal no-padding changes the simulator's target covariance. At zero illustrative flood ratio target/no-pad covariance ~32768.0707, while when flood variance equals the source contribution the illustrative ratio is ~16384.5353; **these are symbolic/continuous Gaussian illustrations, not full source-transcript distinguishing bounds nor actual chosen secure source parameters**.

**CONSTRUCTIVE SCOPE:** A **REVISED** no-padding version might start from the first-stage Eq(25) instead of Eq(26), with public fixed covariance and a newly proven simulator/precision/correctness bound. But original Lemma7.1/Theorem7.5 cannot simply be quoted: recursively structured NGP secret is not source iid `χmlwe`, high-entropy filtered key and uniform source-consistent `σmin(mat(s_i))` bound remain unknown, and FHE KeyGen/Eval/evaluation-key security/cost need a fresh proof. The source's `Bpub` condition is a SUFFICIENT requirement for its padding proof, NOT universal necessary for all no-padding protocols. Earlier 'constant covariance removes O(LDec)' should be interpreted only as a conditional potential after designing this full revised protocol. Source §5 already has a known-norm unpadded line, so novelty cannot be assumed.

**FULL RECORD:** `findings/cgs-26-fixed-covariance-does-not-erase-original-padding-gate.md`, source ePrint2025/409 Algorithm7 p29, Lemma7.1 p30–31 Eqs25–26, Theorems7.4/7.5 p32. Local exact script `/mnt/data/cgs26_source_padding_variance_gate.py` SHA256 `db4152f63fde13fdce163cc2e26ce752364e96dd5b66d0ca39390943896304bd` / JSON SHA256 `a90cdbc1e0f767f138faf96735208bedec9a548b6e548d595d8e3b432f30d5dc`.

**STATUS:** FAIL unchanged-original/no-ζ hypothesis; PASS source/cost covariance gate; revised structured-secret no-padding scheme **UNCLEAR/HUMAN_REVIEW**, original CGS O(LDec) OPEN. **NEXT_ACTION CGS-27 (next PI continue):** one decisive original Eq25 simulation/spectral/key-distribution test to determine if the NGP branch merits further work, else PARK it and return to original secret-conditioned Gaussian correlation. **STATE_UPDATE:** YES root one active task and CGS detailed file.

---

## CGS-27 — Mod-two image obstruction for all dense signed NG secret keys (2026-10-15)

**H-CGS27 [FAIL direct smoothing shortcut]:** NG-pair `(a,b)∈{±1}^n×{±1}^n` with `C C^T=2nI` and stacked `C=[mat(a)|mat(b)]` suffices to conclude the **unflooded** integer convolution `a r_1+b r_2` approximates full-lattice spherical discrete Gaussian, without source individual-image-lattice smoothing verification. In fact real Gram isotropy does not imply mod2 lattice surjectivity.

**ONE GENERAL EXACT FALSIFIER [DERIVED]:** Mod2 all coefficient signs coincide, so `a≡b≡H(X)=1+X+...+X^(n−1)`. In F2[X]/(X^n+1), `XH≡H`, hence every column of `mat(a)` and `mat(b)` reduces to all-ones: `rank_F2(C mod2)=1` (EVERY dense ±1 key, including our recursive n32768 NG family). Image `C Z^{2n}` lies in sublattice whose entire coefficient parities agree; lattice index ≥`2^(n−1)`. Test “all parities same” gives probability 1 in unflooded image but `2^(1−n)` for full uniform mod2 vector, advantage `1−2^(1−n)`. This is an exact arithmetic support theorem, not MLWE ciphertext attack.

**SOURCE APPLICATION / BOUNDARY:** Actual Okada–Takagi ePrint2025/409 Lemma7.1 Eqs25–26 original physical pp30–31 has an **independent flooding Gaussian E on a half-integer lattice** added to `r^Ts`. Source Lemma7.3 p32 explicitly controls discrete-lattice convolution/smoothing. The parity distinguisher **DOES NOT APPLY** to the final source distribution after sufficient independent E; E can erase this sublattice support. One cannot substitute stacked Gram `2nI` for all smoothing lemmas without showing E and parameter conditions. This is NOT a flaw in original source nor an impossibility theorem for revised flooded no-padding FHE.

**MINIMAL VERIFICATION:** Exact negacyclic Gram =2nI, F2 rank1 and two-point parity image n2,4,8,16; all binary input cases exhausted n2,4 and standard spanning input vectors tested n8,16, supported by exact general proof. Gaussian toy D_Z,4 target probability all bits same at n16 ≈3.0517578303e−5 vs 1 unflooded. Cyclotomic resultant bound plus NG spectral |a(ζ)|≤√(2n) offers universal lower bound `σ_min≥(2n)^(-(n−1)/2)=2^(−262136)` at n32768, far too conservative as a useful source spectrum certificate; not a proof actual keys have tiny singular values. **FULL REPORT:** `findings/cgs-27-ngpair-mod2-image-smoothing-obstruction.md`, script `/mnt/data/cgs27_ngpair_lattice_image_gate.py` SHA256 `3ed5bbaa29911c1389d0ea32b9365a6ecc5ec63a68fde020483c88ee8dac3d4e`, JSON SHA256 `db4aa2d98dc3c883740b9c36d02cb42aff28875a41e17d779ffbf342a40771e1`.

**SCIENTIFIC ASSESSMENT:** Although we have algebraic fixed covariance at k2 and exact ≈129-bit keyspace count at n32768, there is **NO verified standard MLWE security route** for globally structured NG secrets, no quantitative useful individual `σ_min` bound, no complete revised simulator/evaluation-key proof and no competitive end-to-end cost. More covariance/NGP identity exploration is not justified absent a new mechanism. **RECOMMEND PARK NGP covariance/structured-key branch** (not the parent CGS research), preserving all earlier files.

**STATUS:** FAIL Gram-only discrete-Gaussian shortcut; PASS exact mod2 support theorem + test; original source Gaussian O(LDec) OPEN/HUMAN_REVIEW. **NEXT_ACTION CGS-28 (next PI "继续"):** Return to source-compatible standard-LWE hidden-secret conditioned Gaussian, choose ONE concrete external-secret-linked reusable correlation or another nontrivial source-compatible technical route and falsify it against exact multi-sid active-share transcript + cost. Avoid repeating PRSS/PCF direct ports archived CGS-10–21. **STATE_UPDATE: YES** single global and CGS detailed state.

---

## CGS-28 — Fresh server flooding can cover the entire rounding disturbance (2026-10-15)

**ONE PRIMARY HYPOTHESIS [PASS necessary statistical gate, UNCLEAR full protocol]:** Keep Okada–Takagi 2025/409's original independent standard LWE/MLWE key distribution, server assumptions and one-response Shamir PartDec. Replace all session padding ζ with ZERO but increase fresh *independent* ServerDec flooding Gaussian E so that E hides the full secret-dependent rounding inner-product W (and evaluated/fresh ciphertext noise). No new PRSS/PCF or special secret distribution needed. **Source §5 Algorithm3 p19 already samples independent E, Lemma5.1 pp20–21 Eqs(13)–(18) gives W, Theorem5.5 p24–25 simulator; §6 Algorithm6 p26 and Theorem6.3 p28 currently use stored ζ, §7 Algorithm7 p29/Lemma7.1 p30–31 extend ring covariance.**

**THEOREM [KNOWN SMUDGING, exact proof]:** For `E←D_(hZ,σ)`, any shift τ∈hZ has `TV(E+τ,E)≤|τ|/σ`, by unimodal point probability `TV(E+h,E)=1/Z` and Poisson lower bound `Z≥σ/h`. For independent W with `Pr(|W|>M)≤δ`, even conditional on previous adversarial context excluding internal E, `TV((W,E+W),(W,E))≤δ+M/σ`. For d-coordinate independently flooded vectors, ≤δ+dM/σ. This is the **WHOLE pre-flood conditional residual**, not merely matching Gaussian variances, and supports sequential hybrid over polynomial adaptive sessions when all bounds are conditional.

**SOURCE-SHAPED COST GATE:** On event max |r_i|≤R_r, scalar `M=nB_lwe R_r+2B_eval+1/2`; module rank k / ring dim n each residual coordinate bounded by `M=k n B_mlwe R_r+2B_eval+1/2`. Conservative sufficient `σ_flood≥2^(κ+2)M` scalar, `σ_flood≥2^(κ+2)nM` module, PLUS original σ_flood lower bounds; q/Q must grow. The rounding failure `δ_r`, reworked source hybrid and MLWE/FHE hardness have NOT been established. Toy exact half-lattice Gaussian σ32 shift3: TV `0.093522827246723<3/32`. Unmatched illustrative κ128,n1024,k2,p2^20,σ0=16,B_eval2^30: old bound log2σflood158, new scalar168.011 (+10.011), module179.006 (+21.006). NOT validated source parameters or security.

**NOVELTY:** Noise flooding/smudging is classical and already in source §5; Micciancio 2018 Rademacher fixed norm and source §5 unpadded knLWE are prior art, not alternative novelty. This is a conditional storage-for-q tradeoff, not a new Gaussian primitive or complete secure ThFHE.

**EVIDENCE:** `findings/cgs-28-flooding-no-padding-gate.md`, reproducer `/mnt/data/cgs28_flood_only_statistical_gate.py` SHA256 d1f19f8b66910b54656b49c924086d734cbdbf723660910de26921fc0d22ff19, JSON SHA256 ed73e7ab02b75e3fb181d7ab4957cdecb242ece1c688673914c4fdd30859b10c.

**STATUS:** PASS exact source-aligned statistical smudging interface / UNCLEAR adaptive protocol simulation, parameter choice, LWE/MLWE hardness and concrete low-communication advantage; original O(LDec) open question NOT CLAIMED SOLVED. **NEXT_ACTION CGS-29:** one decisive original-parameter feasibility/security-cost test for q/Q increase (and maybe tighter Gaussian TV alternative) before spending effort on full proof. **STATE_UPDATE YES** root and CGS detailed.

---

## CGS-29 — Modulus security-guideline screen exposes invalid concrete-size inference (2026-10-15)

**ONE PRIMARY HYPOTHESIS [FAIL n1024 illustration]:** The +~21 flooding bits computed in CGS28 mean n1024, rank k2 provides a plausible 128-bit-secure example for removing O(LDec) stored pads. **ONE decisively source-anchored screen** computes ORIGINAL total modulus Q (not just delta), checks the correct effective LWE dimension kn, and compares with the published parameter recommendations of Bossuat et al. *Security Guidelines for Implementing Homomorphic Encryption*, IACR ePrint **2024/463** Table 5.2, for **ternary secret and error std3.19**. The benchmark's maximum classical category128 log2 Q is 53 at total dim2048, 106 at dim4096, 214 at dim8192, 430 at dim16384. This table is NOT a hardness theorem for arbitrary χ_mlwe or other error distributions.

**PRIMARY PAPER [FACT]:** Okada–Takagi ePrint2025/409 **Algorithm 2 p17** defines underlying mFHE abstractly and omits evaluation-key/noise instantiation; **Lemma 7.1 p30** requires `σflood=Ω(2^κ Beval)`, **Theorem7.4 p32** requires `q=σdecΩ(√κ)` with σdec including `σflood/p` and `Q=pq`. Hence `Q=Ω(√κ σflood)=Ω(2^κ √κ Beval)` for this proof even BEFORE additional no-pad flooding. The hidden Ω constants and concrete FHE hardness cannot be filled by assumption.

**EXACT SOURCE-SHAPED NUMERICAL SCREEN [not cryptographic parameter instantiation]:** Keep the PREVIOUS illustrative κ128, ring n1024, module rank2, B1, p2^20, σ0=16, max randomized-rounding bound R=2^28, Beval2^30. Normalize correctness hidden multiplier as ceil√128=12 **for illustration only**. At baseline-source flooding TERM σflood=2^158, `log2 Q_min=161.585`. For no-pad MLWE sufficient σflood≈2^179.006, `log2 Q_min=182.591`: delta=21.006. Effective LWE dimension is `k*n=2048`, NOT n1024, so security reference cap is **53**, not 26. The BASELINE as well as no-pad illustrated Q exceeds this 128-bit reference bound by >100 bits. This falsifies a **concrete n1024 viability inference**, NOT the source paper or general smudging scheme.

**SAME ONE SCREEN / DIMENSION SWEEP** (unphysically holds p/σ0/R/Beval fixed; NOT a valid complete source parameter sweep): k2 ring n2048 => effective dim4096, illustrative Q184.588 > guideline106; ring n4096 => effective dim8192, illustrative Q186.586 < guideline214; ring n8192 => effective dim16384 Q188.586 < guideline430. Later cases are merely **NOT EXCLUDED**, not secure; source Lemma7.1 smoothing and actual BFV/BGV/CKKS Eval security must be rechecked and may require much larger σ0/Beval/q/Q.

**NOVELTY / OPPORTUNITY:** The above only says the CGS28 toy is poor evidence of practical security. It does not give a rigorous ≤128-bit attack for that toy nor exclude larger dimensions. OpenFHE docs https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_NOISE_FLOODING.md give a distinct tighter flooding bound scaling with `2^(s/2)√τ`, but its CKKS security model is NOT a drop-in proof of source Algorithm5's adaptive all-share transcript. Source abstract mFHE lacks parameters, so no valid lattice security estimator run was possible for it without inventing a scheme.

**FULL EVIDENCE:** `findings/cgs-29-modulus-security-screen.md`; exact arithmetic `/mnt/data/cgs29_modulus_security_screen.py` SHA256 `7d39f4da60e65d5ab4b6bb14996d3bf295d9fc92492ada317b41f9e335730077`, JSON `/mnt/data/cgs29_modulus_security_screen.json` SHA256 `83b3013e0c40d180ea490a419075015a3a84ba3b8e69a98ea2afddde3e0cdfa4`. Original 2025/409 40pp version unverified; external 2024/463 Table5.2 text accessed through web, PDF screenshot attempt returned remote cache/403, no claim of visual independent parity check.

**STATUS:** FAIL prior n1024 128-bit viability inference; PASS exact Q accounting / literature-guideline screening, general flooding-only branch UNCLEAR/HUMAN_REVIEW, original O(LDec) problem OPEN. **NEXT_ACTION CGS-30 (upon PI next “继续”):** choose ONE **fully specified actual** FHE parameter family at k2, ring n≥4096 with original source χ, Beval, σ0, Gaussian tail, p,q,Q, and run *both* original smoothing feasibility and 128-bit lattice-estimator / communication gate; or one rigorously source-compatible tighter flooding bound if it directly rescues costs. Do not accept +bits-only claims, nor transplant CKKS bound unproved. **STATE_UPDATE YES** root and CGS topic.

---

## CGS-30 — p-cancellation invalidates small-q rescue of CGS-28 flooding-only sufficient proof (2026-10-15)

**H-CGS30 [FAIL under the named source-shaped sufficiency argument]:** Increasing FHE-to-ThFHE modulus ratio `p=Q/q` should allow the CGS28 super-large fresh Server flooding E (masking not only evaluated noise but ALL randomized-rounding error `r^T s`) to preserve source's **small polynomial-valued decryption modulus** q by making `σ_flood/p` small. The source randomized Gaussian rounding itself depends on p, so this cannot hold under that argument.

**ONE EXACT DECISIVE PAPER CHECK [FACT/DERIVED]:** Actual Okada–Takagi ePrint2025/409 **Lemma7.1 p30 Eq(27)** has `r_ij∼D_(c_ij+pZ,pσ0)`, thus normalized `r_ij/p ∼D_(c_ij/p+Z,σ0)` remains of scale σ0 independently of p. Source **Theorem7.4 p32**: `q≥c√κ·σ_flood/p` (hidden positive c, σdec also includes other noise), `Q=pq`. CGS28 chosen per-session TV sufficient `σ_flood≥2^(κ+2) n M`, `M=knB R_r+2Beval+1/2`; choosing `R_r=pσ0 t` for Gaussian tail cutoff t=Θ(√(κ+log kn)) gives
```
σ_flood/p >= 2^(κ+2) n [knBσ0 t+(2Beval+1/2)/p]
             >= 2^(κ+2) k n² Bσ0 t
q >= c √κ 2^(κ+2) k n² Bσ0 t.
```
So under the **CGS28 translation-TV proof**, any p keeps `q=2^Ω(κ)` for non-negligible source scales, not the paper's target `q=polyκ`. Contrast original source σ_flood≈2^κ Beval term independent of p; increasing p DOES reduce that previous ratio. **The result does NOT show all possible centered Gaussian/flooding proof improvements are impossible.** This is the obstruction to this one specific no-prestorage improvement, not a new source-paper error.

**ONE EXECUTED EXACT P SWEEP:** Previous CGS28 illustrative κ128,k2,n1024,σ0=16,B1,t16,Beval2^30, normalized correctness multiplier ceil√κ=12; p values 2^20,2^64,2^128,2^160 yield new sufficient `log2 q=162.5906,162.5850,162.5850,162.5850`, **all 163-bit**, while original flooding lower TERM `log2 q=141.585,97.585,33.585,1.585`. Note source's true baseline q still has other positive terms and constants. `Q=pq` therefore grows with p instead of allowing cheaper q. Example p2^128 yields `log2Q≈290.585` in NEW flood condition. Exact script `/mnt/data/cgs30_p_cancellation_gate.py` SHA256 64c556b341cb30d988cda2cbadfa1edbeb975d0913f1ca9c3e4ba16376df3418; output JSON SHA256 aa1d925ed9cecfe93f84868419631d1ff24c081480f17b135ece1a2e06ef406f. This is a theoretical parameter screen, NOT a BFV run, security estimator or certified full scheme.

**FHE PARAMETER CROSS-CHECK [SOURCE FACT]:** Microsoft SEAL `native/examples/1_bfv_basics.cpp` and `native/src/seal/util/globals.cpp` actual BFV 128-bit reference modulus bit budget N4096=109, N8192=218, N16384=438; use only as an **external rank-one BFV budget**, not source k2 MLWE proof. Its secret/error sampling and standard plaintext t1024 do not match source Algorithm2's jointly specified χ and ring plaintext R2. Thus no actual fully security-instantiated source-consistent BFV example was established; this is *why* algebraic p-cancellation is the cheapest decisive gate, rather than pretending to run a full FHE estimator with invented parameters.

**CONSTRUCTIVE SYNTHESIS:** Large independent server E can statistically hide r^Ts but may collapse the source's deliberately small q because r∝p. **RECOMMEND PARK naive fresh-Server flooding-only branch CGS28–30 as a route to original low-q objective**. Keep original standard MLWE secret-conditioned hidden Gaussian O(LDec) problem OPEN, not just another round of the same parameter trick. Any viable rescue requires fundamentally tighter/adaptive-safe marginal noise proof or different correlation primitive.

**STATUS:** PASS p-cancellation proof and exact p sweep; FAIL small-q original-goal preservation under CGS28 sufficient bound; no universal flooding impossibility or original-paper bug. **NEXT_ACTION CGS-31** (next PI continue): one focused test whether a *centered* W distribution with unknown secret-induced variance can be masked at source-adaptive security level with polynomial q via a new variance-TV smoothing proof; or prioritize fresh secret-conditioned Gaussian share generator instead. **STATE_UPDATE YES**, root single-task and own detailed finding.

---

## CGS-31 — Centered noise still preserves a secret-dependent variance gap (2026-10-15)

**H-CGS31 [FAIL for source-style common statistical Gaussian simulation]:** Could treating `r^Ts` as CENTERED stochastic Gaussian, not worst-case adversarial shift, let polynomial normalized fresh flooding `F=σ_flood/p` hide all residual dependence on `s` in a uniformly public *Gaussian* sufficiently close for every source secret? **NO for the continuous Gaussian approximation, which has inverse-polynomial two-secret conditional statistical distance at polynomial F.** This does NOT prove an attack on the actual Algorithm5 computational real/ideal security game.

**PRIMARY SOURCE [FACT]:** Okada–Takagi ePrint2025/409 full original `Lemma5.1 Eq(14) pp20–21` approximates unpadded scalar latent `e0←D_((1/2)Z, sqrt(p²σ0²||s||²+σflood²))`; **Lemma7.1 Eq(25) p30** gives ring MLWE latent `Σ=p²σ0²Σ_s+σflood²I` with each Gram diagonal equal to `Σ_i||s_i||²`. Source **Algorithm5 p23** releases *all active partial decryption shares* across adaptive ODec; original §5 known-norm simulator p24 is able to sample its actual conditional Gaussian only because the norm appears in pk. §6/7 use secret-correlated ζ to replace the conditional residual with public covariance.

**ONE MATHEMATICAL TEST [DERIVED]:** Let two secret norm-squares be m and m+Δ, and a centered continuous surrogate for the final residual have variance-width squares `V0=F²+σ0²m+σ1²`, `V1=V0+σ0²Δ=(1+δ)V0`, `δ=σ0²Δ/V0`. The Gaussian event `|X|≤sqrt(v0)`, where v0 is actual continuous variance (width²/(2π)), has probability gap `g(δ)=erf(1/√2)−erf(1/√(2(1+δ)))`. For `0<δ≤1`, derivative of g is at least `c*=exp(−1/4)/(√(2π)·2^(3/2))≈0.10985` on [0,1], so **TV(G0,G1)≥c*δ**; any fixed public target H must be ≥c*δ/2 from at least one of the two. Polynomial F and polynomially separated secret norms imply δ is inverse-polynomial, not negligible. Independent centered Gaussian flooding can improve variance-hiding versus arbitrary fixed translation, but does NOT automatically yield negligible conditional TV at polynomial q.

**EXECUTED EXPERIMENT:** Gaussian continuous model κ16,32,64,128,256, n=κ, norm² m0=κ/2 vs m1=m0+ceil√κ, σ0=4, F=κ², σ1=4, illustrative q=κ³: event gaps ≈2.357e−4,2.215e−5,1.846e−6,1.731e−7,1.442e−8, all WAY above `2^-κ` for realistic κ. One exact finite-grid half-integer-lattice Gaussian model compared widths ~16.523/18.358 and obtained TV≈0.0508982071, confirming discrete surrogate signal; NOT actual source hybrid. Full proof, source positioning and caveats in `findings/cgs-31-centered-variance-public-simulator-gate.md`. Local script `/mnt/data/cgs31_centered_gaussian_variance_gate.py` SHA256 `88ee17bbd908f7cb3859efaa845e1bb0ac335e128b7c902bd3cfc723a6cdd80a`, JSON SHA256 `6d754ad20a8f8c2ef60333a38cbfdabc3b611dc7f04ee1c46de1f69b06434690`.

**PROOF BOUNDARY:** Conditional secret-key comparison ≠ original adversarial distinguisher: s/norm is hidden in §6/7 and source key probability matters, source smoothing and final σ1 rounding/mod q could change distances. No computational impossibility is claimed; a simulator that draws a DUMMY secret norm and proves joint computational decoupling from pk under LWE/MLWE could be different. No such reduction is established here. This is NOT an original source flaw or publishable new theorem.

**STATUS:** PASS explicit conditional Gaussian variance TV lower bound; FAIL universal public Gaussian statistical simulator at polynomial F; original source-conditioned Gaussian O(LDec) challenge OPEN, flooding-only CGS28–31 **PARK** absent new computational hybrid. **NEXT_ACTION CGS-32 (PI next continue):** ONE dummy-secret-norm/covariance **computational hybrid** using actual knLWE/known-covariance MLWE source assumptions and full joint public key + adaptive transcripts; quickest falsifier before any new MPC primitive. If it is a disguised known-norm assumption without standard MLWE reduction, report and park. **STATE_UPDATE YES** sole root and topic.

---

## CGS-32 — Persistent dummy covariance needed; source known-covariance MLWE barrier (2026-10-15)

**ONE PRIMARY HYPOTHESIS [FAIL in per-sid form; UNCLEAR persistent form]:** With true standard-(M)LWE secret key S sampled ONCE at KeyGen, the simulator may pick independent dummy norm/covariance each ODec session: each one-session Gaussian noise mixture is correct, so the whole adaptive multi-session law should match. **FALSE already in a two-session Gaussian-noise-only experiment.** Persistent dummy (one independent fake covariance reused across all ODec) repairs exactly this one marginal joint-distribution obstruction, but needs a separate computational public-key/evaluation-key decoupling theorem.

**PRIMARY SOURCES [FACT]:** Okada–Takagi 2025/409 **p8 §2.2** explicitly says known-norm LWE reduces from standard LWE but known-covariance ring-LWE lacks a known reduction. **Lemma5.1 Eq14 pp20–21** conditional half-integer scalar Gaussian norm-dependent width; **Lemma7.1 Eq25 p30** conditional MLWE covariance `p²σ0²Σ_S+σ_flood²I`; **Algorithm5 p23** gives `(ctdec,{pdi}_act)` per adaptive ODec under one fixed KeyGen secret. **Micciancio–Suhl ePrint2023/1728**, original introduction, likewise identifies its known-covariance Ring-LWE as a nonstandard hardness assumption and reduction question. Source §5 scalar known-norm prior art is NOT new technique.

**ONE EXACT JOINT FALSIFIER [DERIVED]:** Write M=||S||² or K=Σ_S and let `p_M=Pr_{Y←G_M}[Y∈A]` for any test event A. Real sessions share the SAME M, so `Pr[A1∩A2]=E[p_M²]`. If independent fake M'_1,M'_2 are used per sid, `Pr[A1∩A2]=(E[p_M])²`. Difference `Var_M(p_M)>0` when genuine norm variability exists. Each individual Y has the EXACT same marginal under both constructions. If simulator chooses **one** M' and reuses it, the full Gaussian-noise-only lifetime law `E_M[G_M^{⊗L}]` matches the real law IDENTICALLY, but PK and evk correlation is not accounted for.

**ONE EXECUTED TOY:** n8 binary iid secret => M~Binomial(8,1/2). Half-lattice discrete Gaussian with source convention width² `9+4M`. Event `|Y|≤2`: `Pr_real[A1∩A2]=0.5613940170475422`, per-sid fake `=0.5582996107547561`, gap `0.0030944062927861`; persistent dummy = real `0.5613940170475422`. Finite sum |x|≤60, omitted Gaussian mass bound per conditional distribution ≤`3.87×10^(-120)`. Full script `/mnt/data/cgs32_dummy_covariance_joint_gate.py` SHA256 `14fb02f87d50448223f1448f03647b28c8e7566d65241e004ec88587df0decf1`, JSON `/mnt/data/cgs32_dummy_covariance_joint_gate.json` SHA256 `f933913f3daab5443dd5317f70ddfeb74e42264257cbc07f93d0bdf8ee12d503`. This is noise-only surrogate, NOT a source adaptive attack.

**PERSISTENT DUMMY'S ACTUAL COMPUTATIONAL GATE:** For native MLWE PK, `(PK(S),Σ_S)≈c(PK(S),Σ_S')` is needed (plus more for evk). A natural *sufficient* two-hybrid route is `(A,AS+e,Σ_S)≈c(A,U,Σ_S)` = **known-covariance MLWE** (source does not prove from standard MLWE). Standard MLWE without auxiliary Σ does NOT directly imply this. In the continuous Gaussian surrogate, polynomial many noise observations can estimate integer norm/covariance entries by moment concentration; scalar sample variance conditional noise v has variance 2v²/L, so `O(poly)` samples can infer integer M if variance gap a nonnegligible inverse-poly. This justifies why the joint PK–covariance hardness interface is substantive rather than cosmetic. This estimator is NOT proved for source finite-modulus discrete rounded transcript, nor are error/evaluation-key public leakage assumptions satisfied.

**SCIENTIFIC RESULT:** PASS exactly formulated two-sid consistency falsifier and required persistent-key fix. No standard-MLWE reduction or full secure protocol constructed; the persistent dummy may be viable ONLY with a new auxiliary-leakage reduction, a different distribution-specific theorem, or stronger assumption, which may sacrifice claimed original source standardness. No original paper mistake and no novelty claim.

**FULL DETAIL:** `findings/cgs-32-dummy-covariance-multisession-joint-gate.md`. **STATUS:** FAIL independently resampled per-ODec dummy / PASS persistent-only marginal repair / UNCLEAR PK+evk joint security, CGS target OPEN. **NEXT_ACTION CGS-33 (PI next “继续”):** ONE concrete auxiliary-information MLWE reduction gate using scalar known-norm literature as a positive control and ring Σ as the target: construct an explicit hybrid/reduction or specific counterexample for `(PK(S),Σ_S)` versus `(PK(S),Σ_S')`; avoid just asserting “open”. If no credible standard-MLWE proof, park dummy-covariance branch and refocus hidden correlated Gaussian share generation. **STATE_UPDATE:** YES, single root and CGS finding.

---

## CGS-33 — Ternary-preserving ring-unit self-randomization CANNOT change Gram covariance (2026-10-15)

**ONE PRIMARY HYPOTHESIS [FAIL for specific reduction]:** Standard Module-LWE public-key transform `(A,b=As+e)→(A'=Au^-1,b'=b,s'=us)` for randomly chosen unit u should preserve iid small-secret law and uniform public A, while **decorrelating** true `Σ_s` from the public key sufficiently to construct a persistent dummy covariance without known-covariance MLWE.

**PRIMARY PAPERS RE-READ [FACT]:** Source Okada–Takagi ePrint2025/409 **§2.2 p8** identifies known-covariance Ring-LWE not known reducible to standard RLWE; **Algorithm2 p17** native coefficientwise MLWE secret, **Lemma7.1 Eq25 p30** covariance of secret. Micciancio–Suhl ePrint2023/1728 **FULL ORIGINAL acquired this iteration**: **Lemma9 p10** scalar known-norm LWE (leaks **`||s||²+||e||²`**, not just `||s||²`) reduces using **guess polynomial-size norm + specialized search-to-decision proof**, NOT a ring-unit covariance randomizer. Their **Definition12 p16** known-covariance RLWE leaks **`ss^*+Σ_i e_i e_i^*`**, a richer statistic than our dummy secret-only `Σ_s`, and authors explicitly leave reduction open. Author's older ePrint2024/239 has since been **WITHDRAWN** (metadata 2025-03-04), so no new published reduction is inferred from it.

**ONE EXACT GENERAL FALSIFIER [DERIVED]:** Take valid example `χ=U({−1,0,1})` iid for R=Z[X]/(X^n+1). If integer coefficient-linear ring multiplication M_u EXACTLY preserves the whole uniform ternary cube S={−1,0,1}^n, it permutes S, hence for each row r its `max_{s∈S}|r·s|=||r||1≤1`. Every nonzero integer row must have exactly one ±1. Invertibility forces a signed permutation matrix, so the first column `vec(u)=±e_j`, i.e. `u=±X^j`. Such u has `u u*=1` and **`Gram(us)=Gram(s)` EXACTLY for all s**. For module rank k, exactly support-preserving integral GL_k(R) matrix is a signed monomial component permutation; consequently `Σ_(Us)=Σ_s`. Although `A'` remains uniform modulo q, this class cannot generate independent dummy covariance. Statement ONLY for exactly measure-preserving integral ring/module-linear maps under full ternary cube, not generic MLWE impossibility or all χ.

**EXECUTED MINIMAL TEST:** Exhaustive n2,4 ring candidate multiplier columns (`3^n` possibilities) and all ternary secrets, check full support bijection: n2 4/9 allowed, n4 8/81 allowed, exactly 2n signed monomials; **every one preserves Gram**. Toy `n4,q257` transforms A with u=X inverse −X^3, exact public equation and Gram preserved; module rank2 swap+monomial also preserves sum covariance. Distinct secrets s=1 vs s=1+X demonstrably have DIFFERENT covariance, so invariance is substantive. Complete reproduction script `/mnt/data/cgs33_ring_unit_covariance_gate.py` SHA256 `a68f3bf68e55db74fc94541a960903d2aa0d408478c805b7ebf7f8bf7be8478a`, JSON SHA256 `b2913b48066fb4af4d67b49575b35637aef4d0b48681cec22d056b4ee9bf8fe2`.

**JUDGMENT:** This is a restricted algebraic NO-GO for the simplest native-secret/public-key ring-unit self-reduction, not a computational distinguisher of actual source ThFHE. It makes known-covariance leakage-resilient MLWE the actual missing assumption, and no reduction/complete simulation-security proof was constructed. Novelty of signed-monomial stabilizer observation is likely low. **PARK the persistent dummy-covariance branch**, preserving the result. Return to original on-demand **secret-conditioned hidden Shamir Gaussian output** interface.

**FULL FINDING:** `findings/cgs-33-ring-unit-covariance-rerandomization-gate.md`. **STATUS:** FAIL covariance rerandomization / PASS tiny full-support enumeration and matrix proof / original O(LDec) problem OPEN. **NEXT_ACTION CGS-34 (PI next continue):** ONE named source-respecting hidden conditional Gaussian generation construction, e.g. explore whether original semi-honest Server as a fresh-noise dealer can learn any required secret statistic without breaking model and without O(LDec), or an actual paper primitive with original full-text mechanism. Test one concrete privacy/protocol interface, not further dummy/NG identities. **STATE_UPDATE:** YES single state and CGS topic.

---

## CGS-34 — Mask collision in proposed public Server pad delivery exposes key; direct Server shift passes only algebra (2026-10-15)

**H-CGS34 [FAIL]:** On-demand semi-honest Server produces source conditioned Gaussian ζ and Shamir shares ζ_i, publicly sends active-party padding contributions masked with existing decryption PRF m_i, d_i=λ_i ζ_i+m_i, while source PartDec_i=λ_i(a s_i+ζ_i)+m_i. Reusing the SAME PRF value should keep per-party Gaussian output private at no new PRF/domain/ciphertext cost. In fact, because source **Algorithm5 p23** leaks ALL active replies to adversary (and Server/party broadcast is public), any observer subtracts PartDec_i-d_i=λ_i a s_i, sums to a s, and **one unit a∈R_q gives s=a^-1 Σ_i(PartDec_i-d_i) in one session** for RLWE rank1. This is an attack on our NEW candidate, not original ePrint2025/409.

**ONE EXACT TEST:** Ring F_17[X]/(X^4+1), N3 T2 act1,2, λ1=2 λ2=-1, a=1+X (unit with inverse (1-X+X²-X³)/2), s=1-X²+X³. Independently Shamir-share each coefficient of s and arbitrary ζ, generate two random reply masks and proposed broadcast d_i. Observed Σ_i(pd_i-d_i)=X-X² and key recovery s exact. This is an ALL-VALUES cancellation theorem, so toy ζ need not use true Gaussian. For MLWE rankk, it reveals public ⟨a,s⟩ relations, requiring further independent sessions for full rank. Executable /mnt/data/cgs34_server_pad_mask_collision_gate.py SHA256 8256e9dcbbb7815acf9a0594654e18cade1a82b51e6fd00938d4172808003c9b; JSON /mnt/data/cgs34_server_pad_mask_collision_results.json SHA256 a79542d2ae56719326db3f9e931b6a05c6cd5ed361c358aa9cfa27ec9e34d0de.

**PROTOCOL/PRIOR ART:** Original source newer 40pp mirror ePrint2025/409 Algorithm7 p29, Algorithm3 p19-20 (two rounds, Server one processed ciphertext, parties each one reply), §5 p25 semi-honest Server remains untrusted and does NOT receive replies; p25's independent Server plaintext privacy argument only uses original FHE semantic security. Old public 36pp ePrint dated 2025-03-04 has DIFFERENT layout, never mixed. Prior CGS16/19 archived PRSS/interactive rounding cost failures. The original source is **NOT** vulnerable to this key recovery because it never publicly broadcasts d_i.

**REPAIRS/ALTERNATIVE:** Domain-separated independent pad-transport m_pad_i and decryption m_dec_i breaks literal subtraction (verified) but adds |act| extra public ring-valued elements per Server broadcast, abandoning original O(1)-in-N online size. If Server itself knows ζ it can subtract ζ DIRECTLY from ctdec,1 and give parties pad-free replies; exact algebraic residual identity matches original source padding WITHOUT any extra online ring elements or round (also verified). HOWEVER Server would need the secret-conditioned covariance Σ_s to generate ζ; source Server has pk/evk/seeds, not Σ_s, and it is still semi-honest UNTRUSTED. Handing Σ_s privately from trusted KeyGen changes the Server's auxiliary input/privacy assumptions, potentially demanding a known-covariance MLWE security reduction (§5 p25). This is an **UNCLEAR concrete branch for next iteration**, not a complete secure solution under source standard MLWE.

**STATUS:** FAIL naive same-mask public online share transport, PASS full-key RLWE recovery exact, UNCLEAR Server-direct no-extra-message shifted b proposal. Original O(LDec) open. **NEXT CGS-35:** one source-specific Server leakage/security falsifier for algebraically cleaner direct b−ζ Server shift with Σ_s privately supplied from trusted KeyGen, considering ciphertext privacy against semi-honest Server and exact source standardized LWE/MLWE assumption; do not claim unchanged trust. **STATE_UPDATE YES**, one root and CGS detailed file.