# FHE Research State — After Iteration 121
Checkpoint: **2026-10-12, after Iteration 121**.

## CURRENT TARGET
**None ACTIVE.** Most recent target: Guimarães–Pereira, *Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead*, ePrint 2025/686, I120–121 bounded-gap sparse-secret/KeyGen audit. I120's exponential uniform rejection-sampling counterfamily is preserved; I121 **KILLED the naive exact-one-per-block repair as nonnovel/same-assumption-inapplicable**, and PARKED the direct block-key adaptation. No FAB benchmark failure shown. FEFBS I117–118 and SPRU proof-bound I119 remain PARKED.

## LAST COMPLETED ITERATION
**121**. I122 has NOT started.

## CURRENT QUESTION
**HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS:** Decide whether to authorize ONE narrowly specified I122 test about existing **polynomial-hardness reductions for the exact one-per-block RLWE secret** in FAB's setting (not an implementation or correctness test), or PARK this entire bounded-gap direction and select a different structural FHE question.

## PRIMARY HYPOTHESIS
**NONE ACTIVE / PI_DECISION_PENDING.** I121 [NEGATIVE]: exactly-one-per-block keys solve FAB's interior maximum-gap condition but are already public prior art (SPRU §4.3); the original uniform fixed-weight distribution does NOT transfer automatically under a negligible-probability conditioning event. I120 rejection-sampling obstruction remains a valid earlier result, not a new attack.

## CURRENT EVIDENCE
- [FACT] I121 original primary sources: block binary at-most-one including empty blocks [LMSS23, ePrint **2023/958**, §3 physical p6, mirror SHA256 `0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de`]; exactly-one-per-block already used [SPRU, ePrint **2025/651**, §4.3 p15 and security analysis §4.5 p18]. Published block-key analyses are distribution-specific and not automatically a polynomial-hardness theorem for FAB RLWE. I121 detailed note `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`.
- [DERIVED/NEGATIVE] I121 one structural/prior-art falsifier: n=hL, exactly one selector per block gives adjacent interior gap `j_{b+1}-j_b∈[1,2L−1]` so `B=2n/h`, O(h) direct KeyGen; however under uniform fixed-h secrets this structure occurs with probability `L^h/binom(Lh,h)=2^{−Ω(h)}` for fixed L>1 (exponent at L=16: ~1.39664h bits). Thus naive conditioning loses exponential factor and does not preserve the original distribution or establish security. NOVELTY NOT VERIFIED for any new proof.
- [FACT] I120 original ePrint **2025/686**, §6.1–6.2 pp21–22, Appendix C pp33–34: paper uses rejection sampling to enforce bounded interior sparse-key spacing, and reports finite concrete acceptance/security loss δ. It derives amortized SAB work `O(h log B)`, and discusses setting `B=O(n/h)` to reach `O(h log(n/h))` and `O(h)` in a specified linear-h regime.
- [DERIVED/NEGATIVE] I120 one mathematical test: `n=128t, h=8t=n/16, B=32=2n/h`, uniform size-h support. Conditional-Bernoulli counting yields
  `Pr[all consecutive interior gaps < B] ≤ (n+1)[(1-(15/16)^32)^(n/64)+2(15/16)^(n/4)] = poly(n)·exp(-Ω(n))`. Hence naive uniform rejection sampling needs exponential expected trials; **not** a refutation of the paper's finite measurements or FHE algebra. Detailed proof: `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
- [FACT] I119 SPRU ePrint 2025/651 (**42 physical pages**, mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, `VERSION_UNVERIFIED`; rendered arXiv 2607.27401v1 cross-check): Theorem 1 §4.1 p14 requires `Δ ≥ max(4N²κq,(20N³κ)²)` for unoptimized Eq.(8), with positive integer `κ` (§3.1 p7). Table 2 §6.1 p24 reports optimized New boot. `N=2^15, Δ≈2^49, h=64`, ~14-bit precision.
- [DERIVED/NEGATIVE] I119 ONE decisive substitution test at **κ=1**: required `Δ ≥ 400·2^90 ≈ 2^98.64`, ~49.64 bits above Table 2 scale. Thus published **sufficient** theorem bound cannot certify the reported parameters directly; this is NOT an algorithmic correctness/security/benchmark failure, and optimized noise proof may be substantially tighter. NOVELTY NOT VERIFIED.
- [FACT] I117: pinned `fourier_calculator.py` and `fourier_extension.py` use fixed **300** composite Simpson-3/8 panels for each half-period Fourier integral independent of harmonic index. Python source call chain is real.
- [DERIVED] I117 exact, source-equivalent *plaintext* test for `f(x)=x`, high-degree `n=216`, bridge smoothness `speed=2`: at harmonic 216, analytic `b_216≈+7.6806923566e−8`, 300-panel `b_216≈−2.3543473241e−5`; panel-refinement converges to analytic value. At harmonic 201, spuriously `b_201≈−0.0615958932`. Across 2,049 sample points, full Fourier reconstruction max error ≈0.125 versus ≈3.11e−6 with analytic coefficients. This is a reproducible **preprocessing numerical problem**, not a CKKS security/noise failure.
- [FACT] I118: author pin's **39 modified paths across 7 commits** provide continuous `gelu_test.cpp` **n44/speed12**, sigmoid n34, exp n29, boot n25, and corresponding shipped coefficient files. Explicit path: `gelu_test.cpp → fbs_utils.h → src/core/lib/math/fourier.cpp → fourier_calculator.py` when online; `-f` bypasses Python and loads precomputed `gelucoeff.txt` header44.
- [NEGATIVE] No public pinned dedicated **discrete LUTGeLU n216** example or coefficients found in this author's changed-file inventory. Thus **NO demonstrated effect on published Table 3 LUTGeLU n216**, no verified published precision error, no actual encrypted benchmark run, and no proof of cryptographic novelty.

## MAIN OBSTRUCTION
The bounded-gap keygen barrier is real for uniformly random fixed-weight supports (I120), but the obvious efficient structured sampler is **known prior art**, and the changed key distribution needs independently justified (R)LWE hardness/noise parameters. Without a nontrivial applicable reduction and measurable FAB gain, this is not a publishable FHE contribution. Earlier FEFBS/SPRU audits remain parked.

## OPEN UNCERTAINTY
[OPEN] Is there a rigorous reduction with **polynomial approximation factor** that establishes suitable RLWE security for exact-one-per-block secrets under FAB's sparse-polynomial ring and parameters (as opposed to concrete estimator-only 128-bit assessments)? Even if yes, is it genuinely new and improves FAB beyond existing block-key literature? HUMAN_REVIEW.
[OPEN/PARKED] I119 tight optimized SPRU noise bound; I117–118 FEFBS LUTGeLU coefficient provenance; older original vFHE CRT lookup ideal-IOP discrepancy retained, no compiled forgery.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION
**Do not initiate I122 without PI decision.** PI must either (A) authorize one primary literature/security hypothesis: does a **known formal low-approximation-factor RLWE reduction** already cover exact-one-per-block keys suitable for SAB's setting, and what assumption changes are required? First cheapest test is theorem-assumption alignment in primary sources; OR (B) PARK bounded-gap distribution and select a different FHE structural paper/claim. Do not restart sparse-SAB terminal sign I110–111 or naive block-key adaptation.

## RELEVANT FILES — READ IN NEW CHAT
1. `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, **this `STATE.md`**.
2. **I121** `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`.
3. **I120** `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
4. **I119** `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
5. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`
6. `findings/fefbs-lutgelu-216-coefficient-provenance-gate-iteration118.md`
7. `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`
8. **Exact complete prior verbose STATE**: `logs/state-pre-session-handoff-2026-10-12-iteration118.md` (preserved blob SHA `935d61d8d7e1cf23c21771223ec67dbb7d70d492`).
9. Historical state chain `logs/state-pre-iteration115-prca-handoff.md`, `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; retrieve specific findings/failures **only if** the PI selects those topics.

## BRANCH STATUS / DO NOT DELETE
**HUMAN_REVIEW/PARKED:** FAB bounded-gap I120–121 (I120 exponential rejection barrier retained; I121 naive exact-one-block fix already known and not same-assumption). **PARKED:** SPRU Theorem-1/Table-2 proof-bound mismatch I119 (not a practical failure). **PARKED:** FEFBS I117–118; LFBS PRCA I114–116 (`failures/lfbs-prca-source-only-layout-low-novelty-parked-iteration116.md`); Paiva incomplete-NTT key portability I112–113; sparse-SAB local terminal sign I110–111; Carousel rounding I108–109; SIMD-ALU cutoff I103–107; Nested-RNS I99–102; PaCo precision I95–98; RIG. **ARCHIVED:** GL generic BigSwitch; specific vFHE bounded-public-A/direct Brakedown repair. **PRESERVED OPEN FINDING, not ACTIVE:** original vFHE CRT lookup ideal-IOP discrepancy ePrint2025/286. All historical results retained in archives and exact STATE snapshots.

## STATUS
**I121_CLOSED / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS.** Last iteration 121 completed. I122 not begun. No author contact, issues, PRs, or disclosure.

## RESEARCH PROTOCOL
Read before write. One smallest falsifiable hypothesis plus one cheapest decisive test per iteration. Mark [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN]; distinguish noiseless algebra, numeric approximation, CKKS feasibility and actual compiled tests. Preserve evidence provenance, hashes and negative results. Do not modify `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or `START_RESEARCH_SESSION.md` as part of handoff.
