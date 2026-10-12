# Iteration 107 — Conditional contractive LUTID three-lag feedback invariant for Gao–Zheng A2B

Date: 2026-10-12. Primary: Mingyu Gao, Hongren Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, IACR ePrint **2026/233**, verified Research MCP 43 physical-page PDF SHA256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`; GitHub mirror; `VERSION_UNVERIFIED` against latest official binary.

## One hypothesis / cheapest decisive test
[HYPOTHESIS] In the **ideal one-coordinate scalar digit model**, source-pinned LUTID polynomial approximation error, fed into the next three digit positions with weights 16^-1,16^-2,16^-3, does not grow with A2B iteration count (16 / 64); there is an inductive uniform input-error interval near the source cutoff 2^-16, **provided each stage's other perturbations are bounded**.
[FALSIFIER] Exact source-derived normalized LUTID error envelope K_ID(R) and feedback coefficient sum make `R >= 2^-16 + η + (273/4096) K_ID(R)` impossible for a plausible narrow radius, or nonlinear scalar error grows with d. Chosen single test uses R=1.01*2^-16 and derives the maximal admissible symbolic η, not presumed from the paper.

## Read-before-write and primary evidence
Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md I106, original I106 and I105 findings; inspected the exact pinned author C++ and primary PDF p27–28 through Research MCP.
[FACT] ePrint2026/233 §2.4 Def8 physical p14: a single D-CKKS LUT takes noisy input; §5.2 physical p22: only previous three w=4 digit contributions are removed with A2B-cutoff −16; §7.1 Theorem6 physical p27 gives C3(∥v∥p/Δ)^(κ+1)<∥e_B∥p/Δ, proof refers to Def8 but is not an explicitly indexed multiround noise recurrence. §7.3 physical p28 gives cutoff−16, log2Δ≈43, and key switching settings. Table3 physical p25 reports empirical boolean-bottom log2(∥e_B∥/Δ)≈−20.4, **not a worst-case budget**.
[FACT] Pinned public author repo `tsinghua-ideal/fhe-simd-alu` commit `08f1eb87434e7be072cba889270a8400bbffc08e`:
- `src/pke/lib/scheme/ckksrns/z-fhe.cpp` blob `8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02` lines534–565 shows `rotationIndex=(iter-nextIter)*w`, break if `rotationIndex<=-16`, `scaled=EvalMultInC(lut,2^(diff*w))`, then `EvalRotate`, `ModReduceInPlace`, `EvalSubWithAdjustInPlace(core,scaled)`. Hence distance s=1,2,3 previous LUTID outputs feed a later digit with scalar coefficient 16^-s, while older digit contributions s>=4 are left as noise. This is a scalar projection, not CKKS operator-norm equality.
- `src/pke/lib/scheme/ckksrns/z-fhe-precompute.cpp` blob `7412caec6bb755ee43eb08785158159983c37e92`, p16 Hermite order1 MSB and ID LUT functions (ID f(0)=0, f(j)=j−16 otherwise, divided by p16).
- `src/core/lib/math/hermite.cpp` blob `a6de002fcd0f46ed13a7e6806225fd6797a72b1b` order1 16-point DFT coefficient implementation and double conversion.
- `src/pke/include/scheme/ckksrns/z-fhe-constants.h` blob `992e2dfa3e38bc59c45c861a7ed5e7edc739a6f9` contains 47 dyadic degree46 exponential-Chebyshev coefficients; `z-fhe.cpp` lines868–955 evaluates the exp approximation, squares twice, Hermite degree15 in z and adds its conjugate to produce 2Re.
- Important grid convention: source D-CKKS input x=−j/16 corresponds to **lookup index (−j) mod16**, not j. I105 initial indexing error already fixed.

## Minimal scalar derivation [DERIVATION] — conditional
Let E_j denote normalized input perturbation at digit j from its exact grid, η_j denote ALL base/fresh stage perturbations not explained by the low-bit cutoff and previously computed LUTID errors, and ε^ID_i the IDEAL-POLYNOMIAL approximation error of previous LUTID from its exact discrete value. The source scalar digit projection motivates:
`E_j=H_j+η_j−Σ_(s=1)^(min(3,j)) 16^-s ε^ID_(j-s)`.
I104 exact tail bound `|H_j|<h=2^-16` uniformly d, with H_j first nonzero at j4 and geometric saturation.
Write `K_ID(R)=max_(j=0..15) sup_(|u|≤R) |F_ID(−j/16+u)−f_ID((-j)mod16)/16|`; analogously K_MSB(R).
For R=1.01h=1.5411376953125e-5, the validated high-precision, finite-source polynomial Taylor majorant (same I106 algebra applied to BOTH ID/MSB coefficients) yields:
- `K_ID(R)≤1.5410496517620034e−7`,
- `K_MSB(R)≤1.691229975680964e−7`,
- `L_ID(R)=max_(grid neighborhoods) sup |F'_ID|≤0.01877756830351625`,
where each output K includes a conservative 4e−9 Hermite coefficient allowance, under the I106 conditional 1e−10 individual coefficient error assumption and 105-digit mpmath calculation, NOT independent formally outward-rounded interval verification of compiled code.
Source scalar feedback sum `α=16^-1+16^-2+16^-3=273/4096=0.066650390625`; conditional **Lipschitz gain** `α L_ID(R)≤0.00125153226241698 <1`.
If initial |E_i|≤R, and for every later stage `|η_j|≤η_max`, induction gives
`|E_j|≤h+η_max+αK_ID(R)`.
Thus choose `η_max≤R−h−αK_ID(R)=1.4231673449875423e−7`. This is a **sufficient not necessary** condition for all d, including d=16 and d=64. It is NOT claimed or proven that CKKS operations actually satisfy η_max.
At η=0 worst-case envelope `h+αK_ID(R)=1.5269060218626247e−5<R`.
Source scalar MSB error under the same R has K_MSB(R)≤1.69123e−7, or 23.4% of empirical e_B/Δ≈7.2275e−7; this is only a *scale comparison*, not a guaranteed remaining noise budget.

## One test and independent sanity check [NUMERIC]
For the source-compatible scalar loop, evaluated BOTH dimensions d16/d64:
- Worst pessimistic recursion using max bounded ID error at every older stage: max |E_j| =1.5269060218626193e−5 (d16); 1.5269060218626247e−5 (d64), both below R.
- Independently evaluated actual polynomial LUTID for one explicit repeated negative digit q=1 (ideal xgrid=−15/16) at each step, with signed ideal-tail and feedback from the *actual preceding computed* F_ID errors. Measured max |E|=1.52656682075681e−5 for d16/d64; max actual |ε_ID|=1.03212374356e−7, max actual |ε_MSB|=1.04432144087e−7; within the derived K_ID, K_MSB and R. Still a scalar one-path spot check, not sample from encrypted input distribution.
- Derivative bound uses finite polynomial local Chebyshev expansion, analytic binomial bound on E^4, and polynomial derivative variation, not just grid sampling. Formula: if E=e0+u, |u|≤A1, |E'−e1|≤D2, then `|z'−z0'|≤4(3(|e0|+A1)^2 A1(|e1|+D2)+|e0|^3 D2)` for z=E^4; Hermite derivative centered at z0 bounded by binomial expansion of P'(z). These are exact algebraic inequalities conditional on numerical coefficient and rounding bounds.

## Critical limits
- **Main missing stage parameter**: no proven per-round bound `|η_j|≤1.42317e−7` in the actual CKKS setting. η_j lumps original arithmetic noise, Z-to-C/Rotate/Mask, sparse encapsulated switching/ModRaise, rescale/rounding and LUT evaluation noise. These may have different units or nonlinear transformations; they have NOT been proven to reduce to one scalar eta_j as written. Without the CKKS stage operator-norm and error model, the present proof cannot be promoted to a ciphertext correctness guarantee.
- I106 Hermite coefficient discrepancy assumption and 105-digit mp numeric arithmetic do not equal formal directed-rounding certificate. The `L_ID` derivative bound is conditional on analytic reconstructed coefficients; implemented C++ double/fixed coefficients may differ slightly and would need explicit propagation, not assumed zero.
- The source Theorem6 input condition is a per-ciphertext statement. We have NOT demonstrated a valid counterexample, an actual decryption failure, a failure probability, a computationally meaningful improvement or a proof that authors overlooked cutoff (they explicitly describe it).
- The comparison to empirical bottom e_B/Δ is **not** a worst-case or security claim. Difference η_max vs empirical e_B does NOT prove parameter violation: they describe different quantities.

## Reproducibility
`/mnt/data/iteration107_simd_alu_lutid_feedback_invariant.py` SHA256 `4af4d7268e8d254acdfeecbbc3d9fdccbbdeb1393ce122f08a82b9e8da49f11d`; exact JSON `/mnt/data/iteration107_simd_alu_lutid_feedback_invariant_results.json` SHA256 `2f1f581143d79d88c7daae857f1f3873b98f919fb924a8e7965244e1ec3123de`. Script imports the verified I106 source reconstructor and checks both variants and explicit one-path recurrence; all calculations use 105-digit mpmath. All exact user-download paths locally verified before linking.

## End of iteration
STATUS: **PASS (conditional scalar LUTID feedback contraction and all-round invariant)**; **UNCLEAR (real CKKS per-round η bound, actual theorem correctness and novelty)**; **HUMAN_REVIEW for research continuation**.
RESULT: finite Hermite LUTID/MSB interval bounds and feedback factor α give a uniform R=1.01*2^-16 error envelope for d16 and64 *provided extra per-stage eta≤1.42317e−7*. Explicit scalar recurrence numerics agree. This is source-consistent, but only a sufficient ideal-model condition.
NEXT_ACTION: PI choose A: one limited **actual implementation stage-noise audit** on author source and existing benchmark/debug logs to determine whether a coherent normalized η_j can be extracted and compared to the derived η_max (without full benchmark initially). Or B (recommended): park I103–107 basic scalar cutoff/noise micro-audit due lack of verified paper flaw/nontrivial improvement; pick an independent primary-source FHE technical gap. Do not automatically launch new I108; no outreach or public disclosure.
STATE_UPDATE: YES.
