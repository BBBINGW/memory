# Iteration 105 — Source-derived order-1 Hermite LUT response to A2B cutoff tail is below empirical boolean bottom noise in noiseless polynomial model

Date 2026-10-12. Primary paper Mingyu Gao and Hongren Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, IACR ePrint **2026/233**, source MCP GitHub-mirror 43 physical pages, PDF SHA256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`, latest official binary VERSION_UNVERIFIED.
STATUS: **PASS** sampled cleartext polynomial-response plausibility check using the author's explicit coefficients/procedure; **UNCLEAR** cryptographic or all-round worst-case noise correctness. No attack, author bug, publishable gap or verified security margin.

## One primary hypothesis / falsifier
I104 left the precise scalar cutoff-tail |ε|<2^-16 under w=4, cutoff=-16, κ=1. Question: In ideal arithmetic, does the **implemented** order1 Hermite LUTMSB/LUTID polynomial map a worst-magnitude cutoff residue into an error that already exceeds the author's empirical boolean bottom-noise scale e_B/Δ≈2^-20.4? Such an excess at a legitimate grid value would be a decisive reason to distrust a naive cutoff-only budget without all the FHE operations; otherwise **do not assert a defect**.
ONE minimal test: faithfully reconstruct pinned degree46 exponential Chebyshev polynomial, 2 squarings, order1 Hermite DFT-based coefficients for both LUTs, evaluate every 16 grid node with two signed endpoints ±2^-16 (32 tests). This is a conservative endpoint *sample*, not a certified continuum worst-case over all intermediate |ε| or CKKS.

## Source [FACT] — pinned exact revision
Read live AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md last iteration104 and I104 finding. Primary ePrint 2026/233 p14 Def8 e' bound with κ, §5.2 p22 cutoff/noise, §7.1 Theorem6 p27, Table3 physical p25 empirical `log2(||e_B||/Δ)=-20.4`, §7.3 p28 w4/cutoff−16.
Pinned author repo `tsinghua-ideal/fhe-simd-alu` commit `08f1eb87434e7be072cba889270a8400bbffc08e`:
- `src/pke/lib/scheme/ckksrns/z-fhe-precompute.cpp` blob SHA `7412caec6bb755ee43eb08785158159983c37e92` p=16, lutOrder1, defines `f_MSB(j)=(1 if 1<=j<=8 else 0)` and `f_ID(j)=(0 if j=0 else j-16)`, generated with `GetHermiteTrigCoefficients(f, p, order=1, scale=1 for MSB, scale=p for ID)`.
- `src/core/lib/math/hermite.cpp` blob `a6de002fcd0f46ed13a7e6806225fd6797a72b1b` computes Hermite order1 complex coeff `c_i=(p-i)/(p^2*scale) sum_(j=0)^(p-1) f(j)exp(-2πi ij/p)`; c_0 halved; zero trim at 2^-32.
- `src/pke/include/scheme/ckksrns/z-fhe-constants.h` blob `992e2dfa3e38bc59c45c861a7ed5e7edc739a6f9`, degree46 complex Chebyshev approximating exp(iπ x/2) on [-16,16], fixed BigFixedPoint 128-bit constants. Three fixed coefficients independently checked against reconstructed generation to <1.3e-39 absolute; Chebyshev generator `cheby.py` blob `7a3eddf1cd00520df50e54ef82768f8d91b7a0a6`. Header keeps coefficient zero UNHALVED; usual Chebyshev evaluator divides c0 by two. This distinction was detected by original coefficient mismatch and corrected before scientific test.
- `src/pke/lib/scheme/ckksrns/z-fhe.cpp` blob `8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02` lines868–955: sparse/full double LUT evaluates degree46 Chebyshev, squares twice, forms polynomial on exp(2πix), then adds its conjugate for 2Re. A2B cutoff earlier-index residual determined in I104 from same file.
- Code's discrete inputs live in negative fraction convention **x=-j/16**, so LUT table index for that input is **(-j) mod16**, NOT j. First test using index j reported ~0.875/1 spurious errors, caught and corrected with a perfect-exponential grid interpolation check. This guards against false bug reports.

## Reconstructed cleartext ideal polynomial [DERIVATION]
For p=16, digit fractions x=-j/16, let q=(-j) mod16. f_ID(q) and f_MSB(q) as source above. Let `C_exp(x)` denote source degree46 Chebyshev approximate exp(iπx/2); evaluate with T_k(x/16) and half its first series coefficient, and compute z=C_exp(x)^4 (two squarings). For respective Hermite coefficients `c_i^{ID,MSB}`, define
`F_ID(x)=2 Re sum_(i=0)^15 c_i^ID z^i` and `F_MSB(x)=2 Re sum_(i=0)^15 c_i^MSB z^i`.
Compare to `f_ID(q)/16` (normalized identity output) and `f_MSB(q)` (boolean bit output).
The exact exponential (not Chebyshev) at all 16 grids gives max <5e−86 absolute grid interpolation mismatch under 85 digit mpmath — strong independent check that table indexing and normalization match source. The implemented Chebyshev exponent polynomial alone at grids yields max ID ≈5.43106623e−9 and MSB≈1.01634864e−8 (no input perturbation).
For each j=0..15 test x=-j/16 ± 1/65536, calculating both channels and comparing to the intended discrete table value. We use exact MAXIMUM MAGNITUDE allowed by I104 cutoff scalar tail although finite d actual tail is strictly lower; signs are conservative endpoint cases, not guaranteed realizable jointly for every j.
- max ID error across 32: **1.0312425555544371e−7**, at j15 sign−1, intended −15/16, computed −0.9374998968757444.
- max MSB error across 32: **1.0902292055142467e−7**, at j8 sign+1, intended 1, computed 0.9999998909770794.
- Source empirical `e_B/Δ=2^{-20.4}≈7.227499802162161e−7`. Ratio maximum ID to empirical≈0.14268; MSB≈0.15084. The worst sampled MSB error is 2.7288652 bits below that *empirical* reported noise magnitude.
- At j8 sign+ (x=−0.5+1/65536), ID error≈1.2735e−9, MSB error≈1.09023e−7; exp approximation stage contribution to MSB ≈1.02e−8 while most error from perturbing an exact Hermite grid input.
- All values correspond to IDEAL, NOISELESS complex polynomial evaluation (80–85 dps), not to any true CKKS decrypted bit or time measurement.

## What this DOES NOT prove
1. Table3 e_B is **empirical average/record**, NOT a worst-case adversarial or security error bound, and it includes algorithmic noise. Our 2.73bit separation is not available headroom guaranteed for additional CKKS noise.
2. Tested ±2^-16 at 16 points (32 total), NOT rigorous maximum over every continuous |ε|<=2^-16, arbitrary other noise terms, interdependence across all 16/64 rounds, nor all residual signs/correlations. No formal bound for derivative/curvature or the entire A2B error recurrence.
3. Source prototype uses `BigFixedPoint::fromDouble` to load Hermite coefficient vectors, and true CKKS multiplications/rescaling/key-switch/additions introduce error. Our reconstructed c_i are high-precision symbolic from the same DFT formula, and original fixed exponential constants were independently matched first three only. We did NOT compile OpenFHE, run real encrypted experiments or extract per-round noise traces.
4. I104's scalar cutoff residual and current results **do not show any correctness failure or security/privacy attack**, especially since authors explicitly acknowledge the cutoff and numerical D-CKKS noise. No novelty established; stop proclaiming 'paper bug' based only on the local input v bound.

## Reproducibility
Script created and executed: `/mnt/data/iteration105_simd_alu_hermite_cutoff_response.py` SHA256 `3f7045bfd516a742660525048e974cc8a17a6ff5cd66b16d5fef587a4f61e91d`.
Results: `/mnt/data/iteration105_simd_alu_hermite_cutoff_response_results.json` SHA256 `7c448de488e9b06b2dc1d5ef5f6d873755c5afc0190df88762fda94dc909d502`.
Both verified paths; script implements direct source formula and 46-Chebyshev evaluation, output lists all 32 tests and 3 fixed constant comparisons. No network needed after source retrieval.

## End of iteration
STATUS: **PASS** source-derived noiseless polynomial endpoint test, **FAIL** hypothesis that a 2^-16 cutoff tail by itself exceeds empirical boolean bottom noise on sampled points, **UNCLEAR** formal full A2B correctness and practicality of any error improvement.
RESULT: Source function reconstruction confirms Hermite interpolation plus exponential polynomial robust to ±2^-16 cutoff at all 16 exact digit grid points in this limited model (worst MSB 1.09e−7 < empirical 7.23e−7). No actual end-to-end CKKS soundness claim.
NEXT_ACTION (I106): Prove ONE uniform **continuum** derivative/Taylor bound for the exactly reconstructed source cleartext MSB polynomial on the intervals `[-j/16−2^-16,-j/16+2^-16]` for all 16 j (rather than testing only endpoints). Check whether the resulting certified worst error still lies below empirical e_B/Δ, while keeping full CKKS noise a separate unknown. If simple interval arithmetic blows up, report UNCLEAR and stop; do not enlarge into vague parameter searches or claim a published theorem failure.
STATE_UPDATE: YES — one source-faithful numeric test with corrected sign indexing and no false security claim. No author contact/email/outreach/public disclosure.
