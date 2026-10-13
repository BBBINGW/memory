# Iteration 164 — Independent (53,25) source-shaped reconstruction reduces derivative-weighting benefit to ~3.5%

**Date:** 2026-10-13. The PI responded “好的，请继续” immediately after I163's explicit alternatives and recommendation in favor of a clean-room independent reconstruction. Interpreted this as permission for **independent polynomial-only reconstruction** rather than author-original source verification, not permission to claim author's Lattigo experiment has been reproduced. ONE primary hypothesis + ONE paired test, with denser grid stability check.

## Read-before-write and provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I163 blob SHA `96c09ae4f9fb39a0eab4e000a3fd7c423431c8bb`, I163 source-realism missing-artifact gate and I162 source-domain degree43 numerical toy. Complete **19 physical-page** Research MCP GitHub mirror PDF Min–Lee–Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, ePrint **2025/429**, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, **VERSION_UNVERIFIED**. Specifically re-read §3.2 physical p7, §5.1 p16, Table3–4 physical p17.

**[SOURCE FACTS]** Table3 Set I: **K=23, epsilon=2^(-6)**, while I162 had used the *different* §3.3 illustration K26, epsilon2^(-8). Table4 Set I "Ours" r5 degree set **(53,25)**, logPQ1547, level11, measured average bootstrapping precision27.12 bits, relinearizations20, time24.9sec. These are **the AUTHORS' REPORTED figures**, not reproduced by this round. Source §3.2 odd-r says `p2=q ◦ ((-1)^((r-1)/2)*T_r)` with q an odd degree-d inverse-sine polynomial; r5 gives `p2=q5◦T5` degree25. Source §5.1 uses separate stage precision and multi-interval Remez; no published original coefficient arrays were found I163.

## ONE hypothesis, decisive falsifier

**[HYPOTHESIS]** The large first-stage derivative-weighted benefit seen in I162 (**2.14188× actual ideal-output error for degree43 with exact outer f2** and §3.3 K26/eps2^-8) **persists materially** at the author's **Table4 Set I r5** parameter shape, with independently reconstructed odd first-stage degree53 and *common approximate second-stage degree25*, enough to suggest a source-relevant approximation-precision frontier.

**[FALSIFIER / ONE PAIRED TEST]** On identical `D=union_{j=-22}^{22}[j−1/64,j+1/64]`, construct (U) uniform degree53 odd-polynomial minimax fit for `f1(x)=sin(2πx/5)`; (W) same degree/domain *derivative-weighted* minimax fit, `w(x)=5/(2π|cos(2πx/5)|)`. Construct ONE common source-shape odd 25th-degree `p2(y)=q5(T5(y))`, fitting `q5(z)≈asin(z)/(2π)` for `|z|≤sin(2π/64)=0.0980171403295606`. Compare on independent dense legal domain `max|p2(p_U(x))−(x−round(x))|` versus weighted. For source relevance require a **material** improvement in total composition error, not just first-stage errors. Same fixed degrees and same p2 in both. **No actual Lattigo executable/code and no exact author coefficient claim.**

## Reproducible method with crucial numerical conditioning safeguard

Local working script was run in Python 3 / NumPy **2.3.5** / SciPy **1.17.0**, committed numeric conclusions only; a stand-alone replay file was generated as **conversation attachment** `/mnt/data/fhe_iteration164_reproduction.py` SHA256 `84b361f336f39381b85ccc8633b68a0b27a725b72ad2047973f61f8666da9f48`. These are implementation versions used in THIS run, not pinning original author's library.

**Important failure of naive approach (solved):** Direct degree53 Chebyshev minimax linear programming at 1e-12 error returns objective0 due to floating HiGHS feasibility threshold. This is NOT mathematical perfect approximation. Avoided by extracting an exact **analytic high-quality Chebyshev–Bessel reference** for the odd sine:
```
  a=2π*(22+1/64)/5, u=x/(22+1/64),
  f1(x)= 2 ∑_{m≥0} (-1)^m J_{2m+1}(a) T_{2m+1}(u).
  p_ref= terms through degree53,
  tail= terms 55,57,...,89 ; global tail absolute coefficient sum≈2.7900511083363925e−12,
  p1=p_ref + ∑_{odd n≤53} c_n T_n(u);
```
and fitting the **scaled residual** `10^13 * (tail - ∑ c_n T_n)` by HiGHS. Since the reference sine-minus-polynomial residual is represented analytically as a Chebyshev tail, no catastrophic subtraction of two ~O(1) numbers is used to fit the ~1e−12 errors. Even terms set zero for both fits, source-compatible odd symmetry.

For common p2, start with degree5 arcsin Taylor `q_base(z)=(z+z^3/6+3z^5/40)/(2π)` and fit its scaled degree5 odd correction `10^12*(asin(z)/(2π)−q_base)` on 2001 z samples via constrained LP. Dense q5 error≈**9.7930700e−12**, degree exactly 5; then p2=q5(T5(y)) degree at most25 with source-form sparsity. This is an **independent approximation choice** and is not guaranteed identical to authors' multi-interval Remez solution. Numerical p1 stage fitting used **45×17=765** points and 45×33=1485-point re-fit, validating each against **45×257=11,565** separate dense-grid samples. Source K23 eps1/64 was kept identical for both U/W. Chebyshev odd coefficients were not constrained to paper's original hidden fit arrays.

## Exact observed results (dense-grid numerical, NOT certified continuous suprema)

With 17-point fitting per interval and identical q5 for U/W:

| Metric | Unweighted p1 U | Weighted p1 W |
|---|---:|---:|
| Dense-grid max UNweighted stage1 | 3.008330606e−13 | 5.738811211e−13 |
| Dense-grid max DERIVATIVE-WEIGHTED stage1 | 8.212660505e−13 | 4.601138207e−13 |
| Dense-grid max TRUE **ideal outer f2** output error | 8.217627967e−13 | 4.600425943e−13 |
| Dense-grid max **common 25-degree p2** output error | **1.0612731179970858e−11** | **1.0251376136860557e−11** |
| RMS of final sampled output error | 6.940271529e−12 | 6.935309573e−12 |
| Max |p1| / max |T5(p1)| | 0.956940335733 / 0.098017140335 | 0.956940335732 / 0.098017140332 |

**Ratio U/W in true approximated p2∘p1 worst sampled error = 1.035249418**, only **3.525%** improvement in max error (≈0.0499 ideal bits), versus I162's 2.14188× ideal outer at degree43 with a DIFFERENT domain. Shared 25-degree outer alone contributes up to **9.794569669e−12** of source-shaped approximation error evaluated on exact f1, overwhelming the improved stage1 term (≈8e−13→4.6e−13).

**Stability:** Repeat fit on 45×33=1485 points, evaluate on identical 11,565 points. U max **1.0612731179970858e−11**, W max **1.0251658896787141e−11**, ratio **1.035220864**. Both fitting grids yield same qualitative result. The q5 inverse-sine max on dense z-grid is **9.7930700e−12**. Both |p1|<1, T5 outputs within expected z near±0.0981, and local composite branches valid. No numerical exact-continuous max theorem and no rounding/CKKS simulation.

**[Numerical caveats]** Absolute errors ~1e−11 require precise residual scaling; remaining double-precision errors ~1e−16 can affect last decimal digits but not ~3.5% separation. No interval arithmetic or certified exchange conditions. The global Cheb–Bessel tail coefficient sum bounds *reference truncation*, not the optimized fit's continuous extrema. Benchmark numeric timing and source-compatible ciphertext effects untested.

## Interpretation and scientific significance

**[PASS in the narrow positive sense]** At fixed d53/d25 and Set I legal domain, independently derivative-weighted p1 has slightly lower **sampled** output max error than independently unweighted p1. So the sign of the I162 benefit still survives the replacement of ideal outer f2 by a degree25 p2 in this specific independent construction.

**[FAIL for the hypothesis of a MATERIAL transferable advantage]** Magnitude drops from ideal d43 ratio2.14× to **1.035× / 3.5%** for source-shaped Set I d53/d25; an **outer approximation error floor** is a principal bottleneck here. Single-stage reweighting is not a high-upside route without **joint p1/p2** or a source-grade noise/level mechanism. An improvement of ≈0.05 ideal worst-case bits is not an established reduction in modulus prime count or multiplicative depth, and cannot be equated to the authors' original average 27.12-bit CKKS precision (different statistics and authors' unknown coefficients). The source already performs full end-to-end benchmarking. No source bug, new primitive, novel weighted approximation algorithm, or validated FHE performance gain. No novelty/prior-art proof.

**[RECOMMEND PARK/HUMAN_REVIEW]** Pause the *p1-only derivative-weighting* subbranch rather than continuing arbitrary degrees/r sweeps; it is low-value at source-shaped real degrees. A **materially distinct** potential future hypothesis would explicitly jointly optimize p1/p2/CKKS-level noise, but must first identify a quantified **FHE cost** or source-backed scenario; do NOT reopen by simply shifting p2 degrees or claiming a generic derivative-weighted minimax is novel. Parent 2025/429 question may remain an index entry but no active I165 experiment without PI choice.

## End of Iteration 164

**STATUS:** **FAIL material-transfer hypothesis**, while **PASS small positive direction** under independent polynomial-only dense-grid experiment; **UNCLEAR** real source coefficient match, CKKS precision, performance and novelty.
**RESULT:** For K23, eps2^-6, r5, matched odd p1 degree53 and common q5∘T5 p2 degree25, U output max1.061273118e−11 versus W1.025137614e−11 (1.03525× / 3.525% / ≈0.05 ideal bits); p2 standalone error ≈9.79e−12 dominates. Fit-grid stability 17 vs33 samples per 45 intervals. Includes numerical rescue via analytic Cheb Bessel residual rather than invalid zero-LP.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK p1-only weighting**. If PI requests continuation, require one new source-valid quantified joint p1/p2 noise-level **resource-saving** falsifier, not arbitrary additional scalar polynomial tests. Original author matched source remains MISSING in `MISSING_SOURCES.md` and should not be marked resolved; this is separate *independent* reconstruction, not Lattigo.
**STATE_UPDATE:** **YES** — significant negative source-parameter result resolves I163's decision to try independent reconstruction, updates research status and parks recommendation. All other failures/branches unchanged.
