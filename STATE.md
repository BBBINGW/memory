# FHE Research State — After Iteration 120
Checkpoint: **2026-10-12, after Iteration 120**.

## CURRENT TARGET
**None ACTIVE.** Most recent target: Guimarães–Pereira, *Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead*, CCS 2025, ePrint **2025/686**, I120. A precise **asymptotic uniform-sparse-key rejection-sampling obstruction** has been established, but is **HUMAN_REVIEW**, not a concrete benchmark/correctness failure or verified novel solution. Primary source: full 34-page ePrint mirror PDF, SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335`, latest `VERSION_UNVERIFIED`.
Previous SPRU proof-bound I119 and FEFBS numerical-provenance I117–118 branches remain PARKED.

## LAST COMPLETED ITERATION
**120**. I121 has NOT started.

## CURRENT QUESTION
**HUMAN_REVIEW:** PI decides whether a NEW hypothesis about a security-preserving bounded-gap key distribution/alternative spacing budget is worth testing, or whether to PARK this new audit and select a different structural FHE target. No ACTIVE hypothesis. Do not automatically pursue variants.

## PRIMARY HYPOTHESIS
**NONE ACTIVE / PI_DECISION_PENDING.** I120 closed [HYPOTHESIS]: uniformly random fixed-Hamming-weight sparse secret keys can be rejection-sampled with polynomial expected work subject to all interior spacings < B = Θ(n/h) throughout n=Θ(λ), h=Θ(λ). **FALSE in general** by rigorous counterfamily. I119's theorem-bound hypothesis remains closed/parked.

## CURRENT EVIDENCE
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
I120 identifies a **key distribution vs cost/security-reduction tension**: asymptotically constant-factor mean-gap filtering of *uniform* sparse secrets has exponentially small acceptance in a valid linear-h family. A directly sampled bounded-gap distribution or increased B may avoid keygen cost, but preserving standard sparse-RLWE security assumptions and a novel FHE frontier is NOT established. Do not confuse an asymptotic sampling observation with a practical cryptographic break. I119/I117–118 parked for earlier reasons.

## OPEN UNCERTAINTY
[OPEN] Can bounded-gap sparse keys be sampled efficiently with a defensible, suitably tight RLWE security reduction and meaningful overall SAB gains over known block-secret/key-switch techniques? Prior art and security model must be audited before claiming novelty. Finite Table 4 security/latency results of ePrint 2025/686 are not disputed.
[OPEN, PARKED] Optimized SPRU circuit tight noise bound (I119); FEFBS published discrete LUTGeLU n216 coefficient provenance (I117–118); older original vFHE CRT lookup ideal-IOP discrepancy remains independently preserved, not a proven compiled forgery.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION
**Do not start I121 without PI decision.** One decision: (A) authorize a new falsifiable hypothesis about a security-preserving, efficiently samplable bounded-gap secret distribution (initial falsifier: stronger existing prior art or unacceptably different hardness/security), OR (B) PARK I120 and select a different FHE paper/structural claim. One hypothesis/one decisive test only. No automated research or outreach.

## RELEVANT FILES — READ IN NEW CHAT
1. `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, **this `STATE.md`**.
2. **I120** `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
3. **I119** `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
4. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`
5. `findings/fefbs-lutgelu-216-coefficient-provenance-gate-iteration118.md`
6. `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`
7. **Exact complete prior verbose STATE**: `logs/state-pre-session-handoff-2026-10-12-iteration118.md` (preserved blob SHA `935d61d8d7e1cf23c21771223ec67dbb7d70d492`).
8. Historical state chain `logs/state-pre-iteration115-prca-handoff.md`, `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; retrieve specific findings/failures **only if** the PI selects those topics.

## BRANCH STATUS / DO NOT DELETE
**HUMAN_REVIEW pending PI:** FAB bounded-gap rejection-sampling I120 (new asymptotic barrier, no direct attack). **PARKED:** SPRU Theorem-1/Table-2 proof-bound mismatch I119 (not a practical failure). **PARKED:** FEFBS I117–118; LFBS PRCA I114–116 (`failures/lfbs-prca-source-only-layout-low-novelty-parked-iteration116.md`); Paiva incomplete-NTT key portability I112–113; sparse-SAB local terminal sign I110–111; Carousel rounding I108–109; SIMD-ALU cutoff I103–107; Nested-RNS I99–102; PaCo precision I95–98; RIG. **ARCHIVED:** GL generic BigSwitch; specific vFHE bounded-public-A/direct Brakedown repair. **PRESERVED OPEN FINDING, not ACTIVE:** original vFHE CRT lookup ideal-IOP discrepancy ePrint2025/286. All historical results retained in archives and exact STATE snapshots.

## STATUS
**I120_CLOSED / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS.** Last Iteration 120 completed; no I121 work begun. No author contact, GitHub issues, PRs, or public disclosure. PI chooses next research direction.

## RESEARCH PROTOCOL
Read before write. One smallest falsifiable hypothesis plus one cheapest decisive test per iteration. Mark [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN]; distinguish noiseless algebra, numeric approximation, CKKS feasibility and actual compiled tests. Preserve evidence provenance, hashes and negative results. Do not modify `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or `START_RESEARCH_SESSION.md` as part of handoff.
