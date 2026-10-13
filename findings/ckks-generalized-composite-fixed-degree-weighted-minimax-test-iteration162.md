# Iteration 162 — Source-domain equal-degree derivative-weighted p1 improves ideal f2∘p1 worst-case error (numerical toy)

**Date:** 2026-10-13. User authorized “好的，请继续” after I161. ONE hypothesis and ONE paired controlled experiment. No claim of paper bug, novel solver, Lattigo execution, real CKKS bit precision or speedup. Read-before-write: `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` SHA `557dba1fddc354fafa44e33ca3aaba42d4c157e8`; I161 and I160 findings.

## Original source grounding

Min, Lee, Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, IACR ePrint **2025/429** https://eprint.iacr.org/2025/429, complete 19pp Research MCP GitHub mirror PDF SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, `VERSION_UNVERIFIED`. Source §3.1 physical pp6–7 uses odd `r` with `f1(x)=sin(2πx/r)`, exact local target `t(x)=x−round(x)` on intervals centered at legal integers and ideal f2 built via r-angle sine plus inverse sine. Source §3.3 p10 example uses **K26**, half-width **eps=2^−8**. Source §5.1 p16 selects approximation degrees/levels separately, §5.2 p17 Table4 **r5 degree set (53,25)** in Set I with 27.12 average CKKS BTS bits — NOT our toy's degree43 or ideal outer. §3.3 presents stage unweighted approximation analysis, but the actual paper also tests whole bootstrapping; I161 `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` verified scope. I160 `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md` proves exact local f2 amplification.

## ONE primary hypothesis and falsifier

**[HYPOTHESIS]** On the paper's legal odd-r near-integer domain, for one *fixed* polynomial degree `d=43`, optimizing first-stage **derivative-weighted uniform approximation** strictly decreases the TRUE ideal end-to-end `sup |f2(p1(x))−t(x)|` compared with *unweighted* uniform approximation at the same degree, same domain, and same fixed exact f2.

**[FALSIFIER / one minimal paired test]** Fit both candidate degree43 Chebyshev polynomials by independent discrete minimax linear programs on an **identical** sampled legal union domain (17 points per interval), and evaluate their true ideal second-stage composition error on an **independently denser** grid (257 points per interval). Verify `|p1(x)|<1` and that f2 stays in the correct local branch; repeat fitting with 33 points per interval as a numerical solver stability check, not another hypothesis. If weighted true max error ≥ unweighted, reject/PARK.

## Fixed experiment specification (reproducible)

Choose:
```
r=5, K=26, eps=2^-8 = 0.00390625, degree d=43
D = UNION over j=-25..25 of [j-eps, j+eps]   (51 disjoint intervals)
f1(x) = sin(2*pi*x/5)
t(x)  = x-round(x)
W(x)  = |f2'(f1(x))| = 5 / (2*pi*|cos(2*pi*x/5)|) on D
f2(y) = asin(sin(5*asin(y)))/(2*pi), |y|<1
p_c(x) = sum_{i=0}^{43} c_i*T_i(x/R), R=25+eps
objective U: min_(c,z) z s.t. |p_c(x)-f1(x)| <= z on fit grid
objective W: min_(c,z) z s.t. W(x)*|p_c(x)-f1(x)| <= z on fit grid
true error: max_(x in verification grid) | f2(p_c(x)) - t(x) |
```
SciPy `optimize.linprog(method='highs')`, NumPy `polynomial.chebyshev.chebvander/chebval`, and standard trigonometry. Fit grid = 51*17=**867** points, verify on 51*257=**13107** points independently with uniform spacing inside each small interval. Both problems have exactly 44 free Chebyshev coefficients and one epigraph variable, unconstrained coefficient signs. The fitter solves linear programs, **not continuous-certified Remez**. The source paper §3.3's least squares and §5 actual multi-interval Remez are not identical to this experiment's unweighted discrete minimax baseline; comparisons are between two purpose-built toy optimizers, not source implementation.

## Exactly computed evidence

| Quantity | Unweighted U | Weighted W |
|---|---:|---:|
| Discrete LP fit epigraph bound | 8.67105847287073e−6 | 1.0583394465049063e−5 |
| Dense-grid stage1 UNweighted max error | 8.677612457770709e−6 | 1.3301194693899742e−5 |
| Dense-grid stage1 WEIGHTED max error | 2.267234083708204e−5 | 1.0584773110835954e−5 |
| Dense-grid TRUE ideal composition max error | **2.2671330049287963e−5** | **1.0584772978635857e−5** |
| Max |p1| on dense grid | 0.9525705606142557 | 0.9525659832878274 |
| Smallest distance of f2(p1) from ±1/4 folding cusp (output units) | 0.24607119720198908 | 0.246083166382957 |

Observed dense-grid TRUE error ratio U/W = **2.1418815590138234×** = **1.098878704669038 ideal bits** at equal degree. The weighted p1 actually has **larger raw stage1 max error**, providing a clean example where error redistribution (toward lower-sensitivity inputs) beats pure stage1 minimax in the exact composition. The absolute values of both stage1 p1s stay <1 and the exact f2 branch matches t at all verification points; exact identity `max |f2(f1(x))−t(x)| ≈ 4.414e−15` was independently checked.

**Numerical stability repeat (same hypothesis):** re-fit both at **51*33=1683** points, independently evaluate on the same 13107-point grid. U true max error `2.2671340731993984e−5`, W true max error `1.0584395786811425e−5`, ratio **2.141958897667392×**. The ratio persists with denser fitting grids and is not a 17-point-only artifact. No rigorous interval arithmetic or continuous supremum certificate: values are dense-grid **numerical upper observations**, not a formally proven global minmax improvement.

**Sampling limitation:** 257-point-per-interval validation could miss narrow excursions; reliable continuous-domain theorem would require interval bounds on p1, derivatives or a certified exchange method. Nonlinear f2 polynomial approximants, finite CKKS scale, and ciphertext noise have not been introduced.

## Source and research interpretation

**[PASS narrow numerical hypothesis]** There is an **actual ideal-composition numerical opportunity** at the same first-stage degree when moving from unweighted to sensitivity-weighted fitting. The different objectives matter beyond the elementary inverse-derivative argument of I160. The improvement is approximately **2.14×** in ideal worst-case output approximation error for one deliberately non-source degree d43 and legal source K26/r5 domain.

**[CRITICAL LIMITS]**
- This is a **toy** exact outer f2, not the source's degree25 approximate inverse-sine / r-angle polynomial; no bounded error from p2 has been included, nor CKKS ciphertext arithmetic error, modulus levels or Lattigo timing. Source Set I r5 uses **degree53 first-stage** and achieves measured **27.12-bit average** full bootstrapping precision; our toy has max output error ~1e−5 (~15–17-bit ideal worst-case), not comparable.
- An approximately **1.10-bit worst-case ideal error reduction** does NOT automatically mean a 1.10-bit *real* CKKS precision gain, let alone fewer multiplication levels or relinearizations; a 53-degree source-aligned experiment may shrink this benefit.
- The source does not explicitly minimize this weight in §§3.3/5.1 (I161), but §5.2 empirically checks end-to-end output. No author flaw or new principle is claimed. Derivative-weighted minimax and equal-degree comparison are standard approximation techniques. Novelty vs existing multi-interval weighted Remez / error-aware polynomial EvalMod is UNVERIFIED.
- PDF mirror version status `VERSION_UNVERIFIED`; although the defining sine / interval formulas were legible and previously audited, no official-current PDF equality claim.

## End of Iteration 162

**STATUS:** **PASS** distinct fixed-degree ideal-output comparison **in a dense-grid numerical toy**; **UNCLEAR** actual source-parameter improvement, CKKS cost, novelty.
**RESULT:** With r5,K26,eps2^-8,d43, weighted true ideal output max error 1.0584773e−5 vs unweighted 2.2671330e−5 (2.142× / 1.099 ideal bits), repeated denser fitting stable, branch safe and same degree.
**NEXT_ACTION:** Human decision for I163: ONE higher-value source-realism gate, **retrieve and inspect ePrint 2025/429's actual polynomial-generation implementation or published coefficients for Table4 Set I r5 degree set (53,25)**. If available, compare source p2-aware error and resource levels for one source-matched weighted p1; if unavailable record MISSING SOURCES and do not claim a source-grade gain. An alternative lower-cost gate is a source-comparable high-degree ideal-outer test, but that alone may be numerically unstable and low novelty. Do not repeatedly sweep arbitrary d or r.
**STATE_UPDATE:** **YES** — source-domain test moves from derivative plausibility to positive controlled toy while retaining strict separation from source CKKS performance.
