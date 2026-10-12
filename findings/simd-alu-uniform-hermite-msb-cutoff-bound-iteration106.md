# Iteration 106 — Uniform cutoff-interval majorant for source-pinned Gao–Zheng A2B Hermite MSB polynomial

Date: 2026-10-12. Source: Mingyu Gao and Hongren Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, ePrint 2026/233. Research MCP full 43 physical pages, PDF SHA256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`, official/latest `VERSION_UNVERIFIED`.
STATUS: **PASS** a conditionally uniform all-interval analytic majorant for the author's NOISELESS source-Hermite MSB polynomial. **FAIL** the proposal that an unsampled internal error peak within the 16 cutoff intervals alone necessarily exceeds the empirical output-noise scale. **UNCLEAR** all-round real CKKS correctness, numerical formally directed certification, empirical noise variance and potential publishable significance. NO NEW PAPER BUG OR ATTACK.

## Read-before-write
Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, active STATE.md ending I105, findings I105 and I104. Source pinned `tsinghua-ideal/fhe-simd-alu` `08f1eb87434e7be072cba889270a8400bbffc08e`. I105 reconstruction basis has been independently checked, not substituted with unrelated generic Hermite mathematics.

## One primary hypothesis/falsifier
[HYPOTHESIS] Although I105 checked only the endpoints x_j ± 2^-16 for the 16 grids x_j=−j/16, a source polynomial may peak INSIDE one interval, with |F_MSB(x)−f_MSB((-j) mod16)| greater than the author's empirical bottom noise |e_B|/Δ≈2^-20.4. 
[DECISIVE TEST] Construct finite Taylor-coefficient **majorants** for the EXACT SOURCE-PINNED exp/Chebyshev 46th-degree polynomial, followed by its source order1 Hermite MSB polynomial and two squarings, valid for every real δ in [−2^-16,2^-16], for each of 16 centers. This is a universal analytic-in-the-interval test, not a dense-grid heuristic.

## Source provenance
[FACT] Original paper ePrint 2026/233 §2.4 Definition8 physical p14 D-CKKS LUT single-step noise; §5.2 physical pp21–23 partial digit subtraction and A2B-cutoff −16; §7.1 physical p25 Table3 empirical boolean bottom `log2(||e_B||/Δ)≈−20.4`, Theorem6 physical p27; §7.3 physical p28 w4, order κ1.
[FACT] Author pinned `src/pke/include/scheme/ckksrns/z-fhe-constants.h` SHA `992e2dfa3e38bc59c45c861a7ed5e7edc739a6f9` records ALL 47 degree46 Chebyshev coefficients as signed BigFixedPoint dyadic rational numbers with denominator 2^128. Script manually transcribed and uses each exact dyadic as input; independently compared **all 47 coefficients** to author `cheby.py` generator to max abs difference ~1.397365e−39 (consistent with 128-bit rounding).
[FACT] `src/core/lib/math/hermite.cpp` SHA `a6de002fcd0f46ed13a7e6806225fd6797a72b1b`, order1 coefficients `c_i=(p−i)/(p²·scale) ∑_{j=0}^{p−1} f(j)e^{−2πiij/p}`, first coefficient then halved. `z-fhe-precompute.cpp` SHA `7412caec6bb755ee43eb08785158159983c37e92`, p=16, MSB table f(j)=1 for j=1..8 else0, scale1. `z-fhe.cpp` SHA `8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02` doubles (squares) exp approximation twice, then 2Re of Hermite polynomial.
[FACT] C++ source uses complex-double trig for generating Hermite coeff and BigComplex(fromDouble); direct independently repeated Python binary64 double version differs from high-precision Hermite analytic DFT coefficients by ≤8.626e−17 in this test. Any claim about platform `std::exp` exact rounding remains an assumption, not a verified portable C++ numerical guarantee.

## Polynomial expression [DERIVATION]
Source exp polynomial `E(x) = Σ_(k=0)^46 e_k T_k(x/16)`, where first Chebyshev term is halved **in evaluation**, while source header stores it unhalved. For each real x0=−j/16, expand the **finite polynomial exactly in local δ**
`E(x0+δ) = a0 + a1 δ + Σ_(k=2)^46 a_k δ^k`.
The coefficient arrays are computed by the symbolic recurrence of Chebyshev polynomials under x=x0+δ using source dyadic e_k; evaluating numerically with mpmath 105 decimal digits.
For h=2^-16 set A1=Σ_(k≥1)|a_k|h^k, A2=Σ_(k≥2)|a_k|h^k; EVERY real |δ|≤h satisfies |E−a0|≤A1 and |E−a0−a1δ|≤A2 by triangle inequality.
Set z=E^4, z0=a0^4, z1=4a0³a1. For all |δ|≤h,
`|z−z0| ≤ DZ=4(|a0|+A1)^3 A1`,
`|z−z0−z1 δ| ≤ ZR=4|a0|³A2+6|a0|²A1²+4|a0|A1³+A1⁴`.
Let `P(z)=Σ_(i=0)^15 c_i z^i` be source Hermite MSB polynomial; F=2Re P(z). Then the exact finite binomial identity yields:
`|F(x0+δ)−f_j| ≤ |F(x0)−f_j| + |F'(x0)| h + 2( |P'(z0)| ZR + Σ_(i=2)^15 |c_i| Σ_(t=2)^i binom(i,t)|z0|^(i−t)DZ^t )`,
where `f_j=f_MSB((-j) mod16)` (NEGATIVE FRACTION index convention) and `F'(x0)=2Re(P'(z0)z1)`. All positive terms are computable; no unseen interior maxima can evade this **mathematical polynomial inequality**. This bound is not a statement about actual ciphertext noise.
The calculation uses reconstructed analytic Hermite DFT values, plus a *conditional* conservative 4e−9 absolute output allowance for <=1e−10 per Hermite complex coefficient difference (source double emulation yields ~8.6e−17). A 1e−35 additional arithmetic-computation allowance is explicit but mpmath 105dps is not a formally outward-rounded interval engine. Thus label **conditional validated high-precision numerical majorant**, not a fully formally certified C++ end-to-end bound.

## Results [COMPUTED / CONDITIONAL]
- At j=8, x0=−0.5, max unpadded uniform all-δ bound across all 16 grid neighborhoods is **1.6206916542072262e−7**; center error 1.0163486438606054e−8, slope term |F'(x0)|h=1.3141382681e−11, higher-order Taylor majorant 1.5189253759943557e−7.
- Adding conservative Hermite coefficient allowance 4e−9 (plus 1e−35 arithmetic guard) yields worst **1.6606916542072262e−7** for every real |δ|≤2^-16 in each of 16 intervals, **conditional** on coefficient and arithmetic bound assumptions.
- Source empirical boolean e_B/Δ=2^-20.4≈**7.227499802162161e−7**. Conditional majorant is **0.2298** (22.98%) of the empirical scale. The 1.66e−7 bound is deliberately larger than I105's maximal sampled endpoint **1.0902292055e−7**.
- Uniform bound for all 16 j ranges from ~1.4303e−7 to ~1.6207e−7 before padding; grid j8 gives maximum.
- The supplied script double-checks all 47 source exp constants against independent I105 coefficient generator and the final F(±h) endpoint values against independent I105 evaluator. All 16 endpoint/center values lie BELOW their analytically derived uniform bounds.
- Importantly, the statement **'inside interval cannot exceed 1.66e−7'** refers to this single, noiseless, coefficient-conditional scalar polynomial. It does NOT imply actual CKKS LUT errors stay below 1.66e−7 or that entire A2B stays below the empirical e_B.

## Limits and scientific decision
[OPEN] No controlled CKKS rescaling/key-switch/linear transform or LUTID feedback error. Theorem6 original input condition may be intended as a per-round invariant not explicitly spelled out; neither an implementation break nor a global proof defect has been verified. Empirical bottom e_B does NOT give worst-case noise clearance; comparison is only a plausibility check.
[PRECISION QUALIFIER] The finite majorant algebra is an exact statement for any specified coefficients. Reported numeric bound uses 105-digit mpmath rather than a rigorously independently outward-rounded interval tool, and the Hermite coefficient-difference 1e−10 bound is a numerical assumption about corresponding compiled libm behavior. Thus the data are **strong reproducible conditional evidence**, not an independently formal mathematical certificate for the production binary.
[NOVELTY] Simple local polynomial Taylor majorant of a known Hermite cutoff is not a publishable FHE contribution; do not make one up.
[DECISION] The I104–I106 toy scalar cutoff-alone attack avenue looks low value. One remaining *composition* question is potentially more substantive but should be a SINGLE narrow test rather than yet another sine/LUT scalar variation.

## Reproducibility
Executed `/mnt/data/iteration106_simd_alu_hermite_interval_certificate.py`, SHA256 `5c1ace8132df28279eb1a334cbf4154f91d1df466848a56e77aec0a6d6e87228`.
JSON `/mnt/data/iteration106_simd_alu_hermite_interval_certificate_results.json`, SHA256 `3787a33e0f64d3f0130815d997180fab30f5d97bbf99ee5387a06a109db23681`.
These exact files were executed/verified locally. No full OpenFHE encrypted benchmark or nonpublic secrets needed.

## End of iteration
STATUS: **PASS (conditional scalar all-interval majorant)**; **FAIL (existential hidden interior peak as a standalone empirical-budget failure)**; **UNCLEAR (global A2B correctness, noise security and novelty)**.
RESULT: for all 16 signed digit grids and every real ε∈[−2^-16,2^-16], source-reconstructed noiseless MSB response error is conditionally upper bounded by 1.66e−7, below empirical 7.23e−7. No author theorem disproved.
NEXT_ACTION (I107): ONE compositional model test, no full CKKS: use source-pinned ID and MSB LUT coefficients and the explicit three-lag feedback factors 16^-1,16^-2,16^-3 to derive an induction/contractive invariant for *ideal* iterative A2B including both cutoff tail and source Hermite LUTID error for d16 and d64. Either show a uniform scalar effective-input bound under a clearly stated fresh-op-noise allowance, or expose the precise missing stage parameter; stop/review if the bound is too weak. Do NOT claim a CKKS correctness theorem from a scalar contraction.
STATE_UPDATE: YES. No author email/contact/public disclosure.
