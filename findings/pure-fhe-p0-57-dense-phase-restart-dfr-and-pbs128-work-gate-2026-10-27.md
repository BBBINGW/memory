# PURE-FHE P0-PRESCOUT-57 — Dense PhaseDecomp: 64-bit Restart DFR vs 128-bit No-Restart Work Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-57
LATEST_COMPLETED: P0-PRESCOUT-57
NEXT_ITERATION: NOT_STARTED / HUMAN_REVIEW
STATUS: FAIL_64BIT_RESTART_DFR / PASS_128BIT_NO_RESTART_NOISE_MAGNITUDE / FAIL_128BIT_MATCHED_WORK_ADVANTAGE / KILL_CURRENT_DENSE_SINGLE_CHAIN_CONSTRUCTION / PRESERVE_ALL_DIGIT_CERTIFICATE
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## Question

P0-55/P0-56 left one candidate: use a rigorous all-digit probabilistic phase certificate to run Schild–Abidin–Preneel PhaseDecomp on a dense standard binary secret in ONE radix chain, avoiding the source's Gamma-block dense fallback and its expensive encrypted digit-vector addition.

P0-57 asks whether one concrete parameterization can simultaneously satisfy source-faithful exact exponent correctness, total failure <=2^-128, >=128-bit computational security using current TFHE-compatible parameters, and a matched total-work advantage over the source dense fallback.

No native implementation, Codex, GPU benchmark, server work, or unrelated-track write was performed.

## Sources

### PhaseDecomp / DigitDec
Leonard Schild, Aysajan Abidin, Bart Preneel, "On Phase Decompositions with Applications to Digit Decomposition," ePrint 2026/537, revision 2026-10-25. Verified full PDF via eprint.iacr.asia.

Relevant source facts:
- Algorithm 3 / Theorem 4: one blind rotation per radix digit, l-1 HomTruncTrace calls.
- Theorem 4 recurrence: sigma_i^2 <= alpha sigma_{i-1}^2 + (N/alpha)sigma_Trace^2 + sigma_br^2, and sigma_out,i^2 <= N(alpha^2+2)/12 * sigma_i^2.
- Theorem 3 / Algorithm 2 are written for odd accumulator modulus Q, but the paper explicitly says even-modulus homomorphic-trace alternatives exist in [36].
- Section IV-A(a): restart extracts carry h=floor(g/alpha), key-switches to the original LWE key, modulus-switches to 2N with scale Delta_h and requires |e|<Delta_h/2; after adding Delta_h/2 it re-enters the exponent below N. One restart costs one extra blind rotation + one key switch.
- Section IV-A(c): dense fallback partitions public indices into Gamma blocks and pays Gamma*l blind rotations, Gamma(l-1) truncations, (Gamma-1)l*c_f encrypted digit-function evaluations, plus intermediate KS/MS. The paper says c_f is about two blind rotations.
- Section IV-A(d): probabilistic phase narrowing is source prior art in spirit, but high digits are treated heuristically in the paper.

### Even-modulus trace
Kang Hoon Lee, Ji Won Yoon, "Homomorphic Field Trace Revisited: Breaking the Cubic Noise Barrier," ePrint 2025/1088 / TCHES 2026.

### Current TFHE-rs reference
Pinned source: zama-ai/tfhe-rs@8252d52fdcd25e08f482e0a7230d15e0d9917d4e

NIST submission compute parameters:
- n=886; k=1; N=2048; native q=2^64;
- binary secret; LWE TUniform(45); GLWE TUniform(16);
- PBS base log 23, level 1; KS base log 4, level 4;
- log2_p_fail=-128; CenteredMeanNoiseReduction.

NIST noise-squashing parameters:
- native q=2^128; k=2; N=2048; GLWE TUniform(27);
- decomposition base log 24, level 3;
- CenteredMeanNoiseReduction.

Current TFHE-rs PBS variance formula: tfhe/src/core_crypto/commons/noise_formulas/lwe_programmable_bootstrap.rs
Current centered modulus-switch implementation: tfhe/src/core_crypto/algorithms/modulus_switch.rs

## 1. Standard iid binary secret suffices

Let W~Binomial(886,1/2). Exact two-sided probability Pr[W<248 or W>638] is approximately 2^-132.9112. Define good-key event 248<=W<=638.

Take alpha=4, l=32, q=2^64. Conditional on a fixed key weight w, each mask-digit sum is S_i=sum_{j:s_j=1} a_{j,i} with iid a_{j,i} uniform in {0,1,2,3}. For worst good-key weight w=638, exact-MGF Chernoff half-width t=384 gives, after union bound over 32 digits and both tails, probability at most about 2^-132.1058.

Across all good weights choose global L=0, U=1341, P=1341. Since phi_i=P-S_i+b_i and 0<=b_i<=3, all pseudo-phases satisfy 0<=phi_i<=1344. The combined key-weight + mask-tail bound is about 2^-131.453.

Thus ordinary iid binary secret works; no fixed-weight secret assumption is needed.

## 2. Correct accumulated-exponent gate

Algorithm 3 needs g_i = phi_i + floor(g_{i-1}/4) < N, not merely each phi_i<N.

With phi_i<=1344, the worst recurrence is 1344, 1680, 1764, 1785, 1790, 1791, ... Hence g_i<=1791<2048.

This corrects P0-55's simpler sufficiency statement.

## 3. 64-bit noise magnitude

Using the current TFHE-rs 132-bit-security TUniform PBS variance formula at n=886,k=1,N=2048,B_pbs=2^23,L_pbs=1, FFT mantissa=53,q=2^64 gives V_br ~=1.1422512257e-9 and sigma_br ~=3.37972e-5 in normalized torus units.

Source-shaped RevHomTrace noise is far below this BR term. A Gaussian/subgaussian heuristic would suggest restart every roughly three digits, but such a heuristic is not a 2^-128 DFR proof under reused evaluation keys, FFT rounding, and adaptive accumulator state.

## 4. Restart exponent-capacity constraint

On the certified phase event phi_i<=1344 and g_i<=1791.

If restarting immediately after the first digit, h=floor(g/4)<=336. If restarting after two or more digits, the worst carry reaches at least 420 and eventually 447.

The source restart must re-enter the exponent below N after adding half a scale. Optimistically require Delta_h(h+1)<2048. Therefore:
- restart after digit 0: Delta_h<=6;
- restart after >=2 digits: Delta_h<=4.

Since restart correctness also needs |e_ms|<Delta_h/2, even the best schedule requires |e_ms|<3; later restarts require |e_ms|<2.

## 5. Centered modulus switching still has constant-probability failure

For q=2^64 -> 2N=4096, one output unit is M=2^52 input units. A uniform mask coefficient has an almost-uniform discrete rounding residual r in [-1/2,1/2], with exact moments essentially E[r^2]=1/12 and E[r^4]=1/80.

TFHE-rs CenteredMeanNoiseReduction explicitly computes public mask rounding errors and adds approximately half their sum to the body. Its source comment states that the expectancy of the error is removed. It uses no auxiliary zero-encryption key; the separate DriftTechniqueNoiseReduction variant stores modulus_switch_zeros.

Ignoring the deterministic LUT-centering half-case, the random centered residual contains S = -sum_{j=1}^n (s_j-1/2) r_j plus a body rounding residual bounded by 1/2.

For iid binary s_j and uniform mask residuals, X_j=(s_j-1/2)r_j has E[X_j^2] ~=1/48 and E[X_j^4] ~=1/1280. At n=886:
- E[S^2] ~=886/48 =18.458333...
- E[S^4] ~= n/1280 + 3n(n-1)/48^2 =1021.66875.

For the best restart threshold |e|<3, allow the body residual its full 1/2 cancellation. Event |S|>3.5 still forces |e|>3. Applying the second-moment/fourth-moment Cauchy-Paley bound to Y=S^2 gives Pr[|S|>3.5] >= (E[S^2]-3.5^2)^2/E[S^4] ~=0.0377.

For later threshold |e|<2, event |S|>2.5 gives Pr[|S|>2.5] >= approximately 0.1459.

These are conservative constant-probability lower bounds, not Gaussian estimates. CenteredMeanNoiseReduction changes the mean placement but does not remove the sqrt(n)-scale fluctuation.

Therefore the source restart cannot satisfy 2^-128 correctness in this dense single-chain regime.

## 6. 64-bit realization decision

Without restart, Theorem 4 multiplies previous variance by alpha=4 every digit and current 64-bit injection noise becomes catastrophic over 32 digits. With restart, the modulus-switch-to-2N carry step fails with constant probability even after centered-mean correction.

64-bit + restart: FAIL_DFR.

## 7. Obvious escape: 128-bit accumulator without restart

Current TFHE-rs NIST noise-squashing parameters provide a concrete 128-bit native GLWE point q=2^128,k=2,N=2048,TUniform(27),B=2^24,L=3.

Using the current TFHE-rs TUniform PBS variance formula with n=886 and 104-bit FFT mantissa gives V_br,128 ~=6.75746e-39 and sigma_br,128 ~=8.2204e-20.

A source-shaped 128-bit RevHomTrace automorphism-key choice has trace noise far below this scale. Propagating Theorem 4 for all 32 digits with no restart gives a representative final output standard deviation about 1.14e-8 against natural digit half-spacing 1/8.

This is not a complete 2^-128 DFR proof, but it decisively passes the cheap noise-magnitude falsifier. Therefore the all-digit idea is not algebraically impossible.

## 8. 128-bit path loses the matched-work advantage

A TFHE GGSW external product with GLWE dimension k and gadget level L has L(k+1)^2 polynomial-product channels.

Pinned 64-bit compute PBS: k=1,L=1 =>4 channels.
Pinned 128-bit NIST noise-squashing PBS: k=2,L=3 =>27 channels.

So one 128-bit blind rotation has at least 27/4=6.75 times the polynomial-product channel count of the 64-bit baseline, before charging higher-precision f128/FFT arithmetic.

The alpha=4 candidate needs 32 sequential blind rotations, so its BR core alone is at least 32*6.75=216 64-bit BR-core channel-equivalents.

P0-56's matched n=886 source dense fallback at alpha=16 has Gamma=ceil(886/127)=7 and approximately:
- 16 full-n BR-core equivalents across blocks;
- about 7.8 BR-equivalent truncation work under the source EvalAuto convention;
- (Gamma-1)l=96 encrypted digit-function evaluations;
- c_f about two BRs, hence about 192 BR-equivalents in the adder;
- plus intermediate KS/MS and final conversion.

So the fallback is roughly 215.8 64-bit BR-equivalents before KS/MS.

The 128-bit candidate's blind rotations ALONE already consume roughly the whole prior fallback budget, before 31 HomTruncTrace calls, 15,903 automorphism evaluations for alpha=4,N=2048, output handling, and the non-free high-precision FFT arithmetic.

Current TFHE-rs releases separately optimize PBS128/f128 performance; it is a distinct high-precision cost regime, not a free representation change.

Therefore the analytical total-work headroom motivating P0-55/P0-56 disappears before native benchmarking. No wall-clock ratio is claimed.

## 9. Final decision

64-bit/restart endpoint: cheap enough, but restart DFR fails by a constant-probability modulus-switch residual.

128-bit/no-restart endpoint: noise magnitude is easy, but high-precision PBS destroys the matched total-work advantage and also worsens sequential latency.

Hence the CURRENT dense-single-chain construction fails the predeclared gate: it cannot simultaneously preserve the correctness/DFR path and the matched work advantage.

## 10. What survives

The P0-55 all-digit certificate remains valid and reusable:
  phi_i=P-S_i+b_i, 0<=b_i<=alpha-1.

P0-57 strengthens it:
- standard iid binary secret suffices;
- a public key-weight tail plus conditional mask-digit tail yields one fixed global P;
- accumulated exponent g_i can also be certified below N.

This certificate may matter in a future scheme with a cheap carry refresh not based on dense LWE modulus switch to 2N, a genuinely cheap high-precision accumulator, or another setting where probabilistic phase narrowing matters without long accumulator-noise chains.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-57
STATUS: FAIL_64BIT_RESTART_DFR / PASS_128BIT_NO_RESTART_NOISE_MAGNITUDE / FAIL_128BIT_MATCHED_WORK_ADVANTAGE / KILL_CURRENT_DENSE_SINGLE_CHAIN_CONSTRUCTION / PRESERVE_ALL_DIGIT_CERTIFICATE / HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RESULT:
- standard iid binary n=886 replaces fixed-weight beta=900;
- all-digit and accumulated-exponent correctness pass;
- 64-bit restart cannot meet 2^-128 because centered dense modulus switching retains sqrt(n) rounding fluctuation;
- 128-bit no-restart avoids the noise problem but loses the matched total-work headroom before native benchmarking;
- no native implementation is warranted.

NEXT:
Do NOT start native implementation and do NOT automatically launch P0-58.
Archive/PARK the current dense-single-chain PhaseDecomp construction.
Preserve the all-digit certificate as a reusable lemma.
Return to HUMAN_REVIEW / problem-level reselection for another PURE-FHE core bottleneck. Do not automatically add DriftTechniqueNoiseReduction, cache/system tricks, or parameter micro-tuning.

STATE_UPDATE: YES — this finding only.