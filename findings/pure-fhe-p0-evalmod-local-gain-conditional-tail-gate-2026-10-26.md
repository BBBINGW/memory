# PURE-FHE · P0-PRESCOUT-16 — EvalMod Local-Gain / Conditional Tail Gate

- Date: 2026-10-26 (Asia/Hong_Kong)
- TRACK_ID: PURE-FHE
- PREVIOUS: P0-PRESCOUT-15
- STATUS: FAIL_NONLINEAR_NOISE_CONTRACTION_H16
- MATH: PASS_ANALYTIC_LOCAL_GAIN_BOUND
- NOVELTY: NOT_ESTABLISHED
- CODEX: NOT_RUN
- OTHER_TRACKS: UNCHANGED

## Primary H16 / cheapest decisive test

Hypothesis H16: In a fixed simple sine-based CKKS EvalMod stage **without explicit upstream-error cancellation**, nonlinear EvalMod alone can substantially suppress CoeffToSlot input perturbations within the valid integer-neighborhood domain, enough to justify relaxing precision / dropping an RNS level at the same targeted numerical failure probability.

Minimal test (favorable ideal function; NO approximation, ciphertext, rescale, or keyswitch noise): f(t)=sin(2πt)/(2π), t=k+ε with k integer, |ε|≤1/8. Prove a deterministic input-to-output gain lower bound.

[DERIVATION] f'(k)=1 for all integers k, f(k+ε)=ε−(2π)^2 ε^3/6+O(ε^5). Since sin(y)/y decreases on [0,π/4], for |ε|≤1/8,
    (2sqrt(2)/π)|ε| ≤ |f(k+ε)−f(k)| ≤ |ε|.
Numerically 2sqrt(2)/π = 0.900316316157..., so even at the very edge of the chosen neighborhood, ideal sine attenuation can reduce amplitude by at most 9.97%, equivalent to <=log2(π/(2sqrt(2)))=0.15150 bits. This alone cannot explain a full 30–60 bit modulus-prime reduction; that requires different arithmetic/cancellation/scale changes. This conclusion is strictly about f; it does not rule out alternative scheme-wide error cancellation or large savings by rescale scheduling.

[DERIVATION] A separate certification-budget example, not a CKKS DFR assertion:
- n=2^15, numerical error threshold τ=2^-20, total numerical tail target δ=2^-128.
- If marginal per-slot errors ε_i are zero-mean sub-Gaussian with a common proxy σ², union bound, no independence needed:
  Pr(max_i|ε_i|>τ) ≤ 2n exp(−τ²/(2σ²)).
  Sufficient condition σ ≤ τ / sqrt(2 ln(2n/δ)) ≈ 2^-23.8206 ≈6.7498e−8; multiplier ≈14.1289.
- For the ideal sine f around each integer, |f(k+ε)| ≤ |ε| globally; thus this condition is also sufficient for stage-output error ≤τ. On |ε|≤1/8, the lower bound above prevents treating the sine stage as arbitrarily strong error shrinkage.
- If budget δ must also accommodate out-of-domain integer lift, allocate fractions δ_I+δ_in≤δ and change the formula accordingly; e.g. δ_in=δ/2 yields multiplier 14.1779.
- This is only a toy conditional input-noise precision-tail calculation. δ here is an explicit numerical accuracy event, NOT automatically IND-CPA-D advantage, decryption failure, or the probability that the ModRaise integer I exceeds K. Sub-Gaussian marginals for actual correlated CKKS rounding noises must be proven; variance alone is not enough (P0-15).
- This model alone does not quantify prime-bit savings because the map from actual CTS scales and RNS levels to sigma, and from sigma to final precision, is unavailable. No evidence of >=1 prime saved.

## [FACT] Prior source review

1. Sung–Seo–Kim–Min, 'EvalRound+ Bootstrapping and its Rigorous Analysis for CKKS Scheme', ePrint 2024/1379 / IEEE Access 2025, https://eprint.iacr.org/2024/1379. Acquired mirror has SHA256 8551ce29009e0e0a9a2c54b0862b6e3db68a816fd2042b311306b7821b619e4e; VERSION_UNVERIFIED. Original extracted PDF physical page 14 §4.1 explicitly relates EvalMod's sine approximation and the 3 error types, p15 §4.2 analyzes cubic Taylor term; p12 explicitly shows EvalRound+ can cancel selected CTS error using skip connections and is NOT equivalent to pure sine attenuation. Web PDF screenshot attempted but cache missed/403.
2. Yan–Zeng–Song–Wang, PKC 2026, 'Faster Bootstrapping for CKKS with Less Modulus Consumption', https://eprint.iacr.org/2025/1403 , https://ckks.org/blog/2026/less-mod-ckks/ . Level-conserving rescaling and aggregated keyswitching actually eliminate one modulus level while keeping reported precision/failure probability; not evidence of tail-bound-alone savings.
3. Ma et al., 'Practical Dense-Key Bootstrapping with Subring Secret Encapsulation', supplied source papers/supplied/2025-1594.pdf physical p13 §3.1 explicitly discusses a lack of precise L1 noise analysis for predicting EvalMod polynomial degree/double-angle count in that setting. This narrower gap is not erased by the toy bound; novelty still unestablished.
4. CKKS Bootstrapping optimization survey (2026) https://link.springer.com/article/10.1186/s42400-026-00571-w already catalogs precision/degree tradeoffs.

## Result, scope, research decision

H16 FAIL as a generic route to expensive-bit savings through ideal sine contraction alone. Analytic test passes and rejects further speculative Codex work. This does not refute Eq.4 of EvalRound+ or claims about its skip connections, does not refute non-sine EvalMod/EvalRound, and does not prove all certified probabilistic parameter tuning is useless. A tight end-to-end gain would require an actual parameter ledger and an original mechanism; neither is shown.

After P0-11..16 repeated failures around representation conversion, SubSum, and local EvalMod error contract, park this local optimization family. Pivot structurally with fresh paper-source evidence and one author-explicit unresolved functional/cost limitation; do not repeat small variants.

END_OF_ITERATION:
STATUS: FAIL_NONLINEAR_NOISE_CONTRACTION
RESULT: PASS_LOCAL_GAIN_BOUND; NO_FULL_RNS_LEVEL_SAVING_ESTABLISHED
NEXT_TEST: FRESH_STRUCTURAL_FHE_UNRESOLVED_LIMITATION_SOURCE_SCOUT
STATE_UPDATE: YES — ONLY isolated finding in PURE-FHE path; no global STATE.md
