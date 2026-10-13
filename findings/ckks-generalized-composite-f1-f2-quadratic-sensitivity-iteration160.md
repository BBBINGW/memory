# Iteration 160 — Odd-r generalized CKKS EvalMod composition has an exact quadratic local inner-error sensitivity

**Date:** 2026-10-13. PI wrote “好的，请继续” immediately after I159 recommendation to PARK routine SPRU HYBRID noise microaudits and select a new high-upside source-available FHE direction. Thus the I159 low-value SPRU microscopic rounding branch is **PARKED by assent**, and ONE new research target/ONE falsifiable claim/ONE cheapest decisive derivation begins. Old vFHE P1 remains source-gated, no other archived direction reopened.

## Read-before-write and full-paper primary source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (after I159 blob `cb5dea4e80420bda2a62a929f9609e6abdec96be`), `findings/OPEN_RESEARCH_BRANCHES.md` and I159. Checked the backlog and archived LFBS, Nested-RNS, existing SPRU, MRFHE and GL attempts to avoid replaying a closed idea. Original **new** source: Seonhong Min, Joon-Woo Lee and Yongsoo Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, ePrint **2025/429**, https://eprint.iacr.org/2025/429; 19-page complete PDF independently retrieved with **Research MCP** source_kind `github-mirror`, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, version vs current official `VERSION_UNVERIFIED`. Read original **§3.1 physical pp6–7** and **§3.2–3.3 pp7–10**. Source §3.1: near integer centers `i∈{−K+1,…,K−1}`, target `t(x)=x−round(x)` on `|x−i|≤ε`; for **odd r** chooses `f1(x)=sin(2πx/r)`, and a second stage `f2` built from r-angle sine + inverse sine so that `f2∘f1=t` on allowed intervals. Authors optimize polynomial degrees and show near-optimal f1 approximation; **they do not claim error amplification independent of r**. Their examples use K26 and ε=2^−8 (physical p10). Formula extraction includes glyph warnings, but defining `f1` and target equality are legible, algebra was independently checked from standard trigonometry.

## ONE primary technical hypothesis

**[HYPOTHESIS TO FALSIFY]** Enlarging odd r in the source's generalized `t=f2∘f1` method to lower f1's approximation degree can be done **without any inherent r-dependent sensitivity of the composite to small additive f1-stage errors** near all allowed integer centers. If true, changing r would incur no necessary first-stage precision-budget tax apart from the polynomial degree tradeoff.

**[ONE cheapest decisive test]** Choose the valid source integer center `x=k` where `r=4k+1` odd, `k=(r−1)/4`, and `K≥k+1`; compute `f1'(k)` and, from exact local equality `(f2∘f1)'(k)=t'(k)=1`, infer `|f2'(f1(k))|`. A growth `Ω(r²)` falsifies the r-independent sensitivity hypothesis. Verify symbolic identity numerically using a source-faithful local analytical f2 and centered finite differences at specified r; test no unrelated hypotheses.

## Exact mathematical result

For any odd `r=4k+1`, `k∈Z_{≥1}` and allowed source integer-center neighborhood `x≈k`:
```
 f1(x) = sin(2πx/r),
 t(x) = x−k       for |x−k|<min(ε,1/4),
 f1'(k) = (2π/r)cos(2πk/r)
        = (2π/r)sin(π/(2r)).
```
Since `f2(f1(x))=t(x)` on that interval and `f1'(k)>0`, the chain rule yields
```
 f2'(f1(k)) = 1/f1'(k)
            = r / (2π sin(π/(2r)))
            ~ r²/π² as r→∞.
```
Explicit locally correct f2 representative: `f2(y)=(1/(2π))asin(sin(r*asin(y)))`, near y=f1(k), because `asin(f1(k))=2πk/r<π/2` and `r*asin(f1(k))=2πk`, with output local `x−k` for sufficiently small neighborhood. This is used **only near chosen k**, not as a global inverse branch of t.

An additive first-stage approximation/evaluation error `δ` near f1(k) causes
```
 f2(f1(k)+δ) − f2(f1(k)) = A_r·δ + O(δ²),
 A_r = r / [2π sin(π/(2r))] ≈r²/π².
```
To guarantee a fixed **local worst-case** final precision budget η independent of δ's sign, a separate bounded f1 additive error must be at most approximately `η/A_r` for the linear regime, i.e. ≈2log₂r additional precision bits. This is a **conditional local sensitivity bound**, NOT total source CKKS bootstrapping error, optimized polynomial L∞ claim, or proof that authors ignore sensitivity.

## Independently executed cheapest exact check

Executed source-form JavaScript Math trigonometry in `functions.exec`, with odd r∈{5,9,17,33,49}; each integer center `k=(r−1)/4∈{1,2,4,8,12}` is within source experiment K26 integer domain. Computed analytic `A_r`, `f1'(k)A_r=1`, and independent centered difference `[f2(y+10^-8)−f2(y−10^-8)]/(2·10^-8)` at `y=f1(k)`. All relative finite-difference errors < 6·10^-9; no CKKS/FHE implementation run.

| r | k | f1'(k) | exact-form A_r |
| ---: | ---: | ---: | ---: |
| 5 | 1 | 0.388322207745 | 2.575181074002 |
| 9 | 2 | 0.121229297615 | 8.248831096716 |
| 17 | 4 | 0.034102305912 | 29.323530279503 |
| 33 | 8 | 0.009059575588 | 110.380446669864 |
| 49 | 12 | 0.004109918393 | 243.313833588009 |

For r49 vs r5 the local sensitivity factor grows by **94.48×**, imposing **6.562** extra p1-stage worst-case local error precision bits relative to r5 if final target η and all other error sources are fixed. Analytic growth is asymptotic when r and K scale together; K=26 is used only to make all five finite r points admissible, not a claim that source tables benchmark r49.

Additional diagnostic (not second hypothesis): for ε=1/256, the source near-maximum classes at x=k and x=k+1 have f1 image-interval separation
`G_r=cos(2π(1/4+ε)/r)−cos(2π(3/4−ε)/r)≈π²(1−4ε)/r²`;
this matches quadratic crowding. Exact positive for ε<1/4. The derivative result above is the decisive test and sufficient on its own.

## Evidence boundaries / contribution judgment

**[PASS mathematically, FAIL primary no-r-dependence]** The exact source odd-r generalized decomposition has a location at a legal integer center where `f2` locally amplifies f1 errors by `Θ(r²)`. A bigger r that makes f1 smoother necessarily transfers sensitivity to the inverse/composed second stage at that point. This is a genuine source-parameter **precision–arithmetic trade-off to check**, not a source correctness flaw or a new algorithm.

**[NOVELTY UNVERIFIED]** The inverse-function derivative/conditioning argument is elementary. The original §3.3 already analyzes approximation error and §5 jointly chooses degrees, so this effect **may already be fully accounted for** in their numerical Remez pipeline. No published gap, reduction in cost, security issue, actual bootstrapping precision, comparison against source tables, or optimizer improvement has been verified. No disclosure/author outreach.

## End of Iteration 160

**STATUS:** **PASS exact source-derived quadratic local sensitivity / FAIL r-independent inner-error tolerance / HUMAN_REVIEW for research value**.
**RESULT:** For valid odd r4k+1 and integer center k, `A_r=r/(2π sin(π/(2r)))=Θ(r²)`; checked five r and local f2 differential; r5→r49 ≈94.5× gain in inner error amplification ≈6.56 bits. No error/attack against source authors.
**NEXT_ACTION:** **I161 ONLY if PI authorizes:** ONE discriminating source-based check: inspect the paper's concrete §3.3 and §5 polynomial approximation/error/degree selection mechanism and test whether the **end-to-end weighted amplification `|f2'|·|p1−f1|`** (or equivalent) is already explicitly bounded or numerically optimized, vs optimizing unweighted f1 approximant independently. Kill this novel-weighted-objective direction promptly if source already handles it; otherwise one minimal matched-degree toy to quantify actual output-error difference, not new research claim yet.
**STATE_UPDATE:** **YES** — PI assent parked SPRU cheap microaudits; new full-source-available ePrint 2025/429 exact precision-conditioning target with one primary falsifier. vFHE P1 remains source-gated; other archives unchanged.
