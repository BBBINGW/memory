# FHE Research State — After Iteration 119
Checkpoint: **2026-10-12, after Iteration 119**.

## CURRENT TARGET
**None ACTIVE.** The newest audited paper is Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, IACR ePrint **2025/651**, iteration **I119**. Its Theorem-1/Table-2 proof-certification boundary was checked and the narrow audit is **PARKED pending PI review**, not an error claim. Previously, Bian et al., *High-Precision Functional Bootstrapping for CKKS from Fourier Extension*, ePrint **2026/367** (EUROCRYPT 2026), I117–118 fixed-panel audit is also **PARKED**.
Paper: https://eprint.iacr.org/2026/367. Research MCP obtained full **43 physical pages** via ePrint mirror, SHA256 `ee2384e0a8148a0678b3fdb0e0d14eb5f988f19750a94081a378e8fb82966e7a`, mirror revision `6ac42a531dd18744cd7b5097dd93f07dd3b05c74`; official latest version **VERSION_UNVERIFIED**. Pinned author code: `FYHSSGSS/FEFBS` commit `3ed0e4c8f2ae80bc0ca66d87704a71b233b34272`.

## LAST COMPLETED ITERATION
**119**. I120 has **NOT started**. I119 was an actual one-hypothesis/one-test iteration; the prior I118 session handoff was administrative only.

## CURRENT QUESTION
**HUMAN_REVIEW**: PI decides whether to authorize a NEW tightly scoped proof of noise/precision for optimized SPRU, or choose a different independently sourced FHE structural target. No ACTIVE hypothesis remains after I119. Never automatically continue SPRU microaudits.

## PRIMARY HYPOTHESIS
**NONE ACTIVE / PI_DECISION_PENDING.** Last *closed* I119 [HYPOTHESIS] was that SPRU Theorem 1's stated sufficient error/scale conditions directly certify its Table 2 New boot. parameters. [NEGATIVE] This is FALSE as a direct theorem-application claim, but does NOT imply an implementation error. Earlier discrete LUTGeLU n216 coefficient provenance remains unverified.

## CURRENT EVIDENCE
- [FACT] I119 SPRU ePrint 2025/651 (**42 physical pages**, mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, `VERSION_UNVERIFIED`; rendered arXiv 2607.27401v1 cross-check): Theorem 1 §4.1 p14 requires `Δ ≥ max(4N²κq,(20N³κ)²)` for unoptimized Eq.(8), with positive integer `κ` (§3.1 p7). Table 2 §6.1 p24 reports optimized New boot. `N=2^15, Δ≈2^49, h=64`, ~14-bit precision.
- [DERIVED/NEGATIVE] I119 ONE decisive substitution test at **κ=1**: required `Δ ≥ 400·2^90 ≈ 2^98.64`, ~49.64 bits above Table 2 scale. Thus published **sufficient** theorem bound cannot certify the reported parameters directly; this is NOT an algorithmic correctness/security/benchmark failure, and optimized noise proof may be substantially tighter. NOVELTY NOT VERIFIED.
- [FACT] I117: pinned `fourier_calculator.py` and `fourier_extension.py` use fixed **300** composite Simpson-3/8 panels for each half-period Fourier integral independent of harmonic index. Python source call chain is real.
- [DERIVED] I117 exact, source-equivalent *plaintext* test for `f(x)=x`, high-degree `n=216`, bridge smoothness `speed=2`: at harmonic 216, analytic `b_216≈+7.6806923566e−8`, 300-panel `b_216≈−2.3543473241e−5`; panel-refinement converges to analytic value. At harmonic 201, spuriously `b_201≈−0.0615958932`. Across 2,049 sample points, full Fourier reconstruction max error ≈0.125 versus ≈3.11e−6 with analytic coefficients. This is a reproducible **preprocessing numerical problem**, not a CKKS security/noise failure.
- [FACT] I118: author pin's **39 modified paths across 7 commits** provide continuous `gelu_test.cpp` **n44/speed12**, sigmoid n34, exp n29, boot n25, and corresponding shipped coefficient files. Explicit path: `gelu_test.cpp → fbs_utils.h → src/core/lib/math/fourier.cpp → fourier_calculator.py` when online; `-f` bypasses Python and loads precomputed `gelucoeff.txt` header44.
- [NEGATIVE] No public pinned dedicated **discrete LUTGeLU n216** example or coefficients found in this author's changed-file inventory. Thus **NO demonstrated effect on published Table 3 LUTGeLU n216**, no verified published precision error, no actual encrypted benchmark run, and no proof of cryptographic novelty.

## MAIN OBSTRUCTION
I119's **unoptimized worst-case sufficient noise theorem** is much too loose to certify the optimized concrete parameters, but a tighter proof or an actual error has NOT been established; merely observing a loose bound is not a publishable FHE contribution. Previous I117–118 quadrature alias uses known numerical remedies and published benchmark impact remains unverified. Do not continue paper-notation/source-only microaudits for iteration count.

## OPEN UNCERTAINTY
[OPEN] Whether a nontrivial, provably tighter noise/precision theorem for actual SPRU sparse-block trace/product/SlotToCoeff circuit certifies Table 2 under a meaningful failure probability; PI must authorize separately. No verified novel proof or practical cryptographic failure.
[OPEN] Provenance of published discrete LUTGeLU `n216,κ_E=0` coefficients (distinct from the toy `n216,speed2`), any end-to-end CKKS impact, and whether a useful FHE-specific tradeoff exists. These are **parked**, not an invitation to resume automatically. Latest PDF binary versus ePrint mirror remains unverified. Original vFHE CRT lookup **ideal-IOP** discrepancy remains an independent preserved finding, **NOT** a proven compiled SNARK forgery or currently selected active topic.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION
**Do not launch I120 without a PI decision.** PI selects exactly one: (A) authorize a NEW concrete hypothesis about a tight noise bound for optimized SPRU with one cheapest decisive test, or (B) park SPRU and explicitly authorize selecting a different structural FHE claim. Without such decision report `HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS`. Do not recycle historical negative branches. No recurring work or outreach.

## RELEVANT FILES — READ IN NEW CHAT
1. `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, **this `STATE.md`**.
2. **I119** `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
3. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`
4. `findings/fefbs-lutgelu-216-coefficient-provenance-gate-iteration118.md`
5. `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`
6. **Exact complete prior verbose STATE**: `logs/state-pre-session-handoff-2026-10-12-iteration118.md` (preserved blob SHA `935d61d8d7e1cf23c21771223ec67dbb7d70d492`).
7. Historical state chain `logs/state-pre-iteration115-prca-handoff.md`, `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; retrieve specific findings/failures **only if** the PI selects those topics.

## BRANCH STATUS / DO NOT DELETE
**PARKED pending PI:** SPRU Theorem-1/Table-2 proof-bound mismatch I119 (not a practical failure). **PARKED:** FEFBS I117–118; LFBS PRCA I114–116 (`failures/lfbs-prca-source-only-layout-low-novelty-parked-iteration116.md`); Paiva incomplete-NTT key portability I112–113; sparse-SAB local terminal sign I110–111; Carousel rounding I108–109; SIMD-ALU cutoff I103–107; Nested-RNS I99–102; PaCo precision I95–98; RIG. **ARCHIVED:** GL generic BigSwitch; specific vFHE bounded-public-A/direct Brakedown repair. **PRESERVED OPEN FINDING, not ACTIVE:** original vFHE CRT lookup ideal-IOP discrepancy ePrint2025/286. All historical results retained in archives and exact STATE snapshots.

## STATUS
**I119_CLOSED / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS.** Last Iteration 119 completed; no I120 work begun. No author contact, GitHub issues, PRs, or public disclosure. PI decides next direction.

## RESEARCH PROTOCOL
Read before write. One smallest falsifiable hypothesis plus one cheapest decisive test per iteration. Mark [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN]; distinguish noiseless algebra, numeric approximation, CKKS feasibility and actual compiled tests. Preserve evidence provenance, hashes and negative results. Do not modify `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or `START_RESEARCH_SESSION.md` as part of handoff.
