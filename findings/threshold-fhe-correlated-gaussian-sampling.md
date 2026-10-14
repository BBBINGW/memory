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
