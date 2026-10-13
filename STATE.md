# FHE Research State — After Iteration 164

**Checkpoint:** 2026-10-13 · `main` · I164 completed, I165 **NOT STARTED**.
**Authority:** Follow `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`. Historical long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md`, project opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides research target, major pivots, novelty, disclosures and parking; agent executes **one smallest falsifiable technical claim plus one cheapest decisive test** per authorized iteration, then stops.

## CURRENT TARGET

**Min–Lee–Song ePrint 2025/429 odd-r CKKS EvalMod generalized polynomial composition, p1-only derivative-weighted error allocation: HUMAN_REVIEW / RECOMMEND PARK after I164.** Full 19 physical-page Research MCP GitHub mirror ePrint **2025/429**, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, current official binary VERSION_UNVERIFIED; §3.1/§3.2, §5.1–5.2 and Table 3–4. Author’s actual Table4 (53,25) coefficients/Lattigo scripts **MISSING_AUTHOR_ARTIFACT**, tracked in `MISSING_SOURCES.md`; not independently verified or reproduced. In I164, the human's “好的，请继续” after prior recommendation for clearly labeled independent reimplementation authorized an **independent mathematical polynomial-only** approximation test, **NOT claiming Lattigo/author code replication**. I164 source-shaped matched p1d53/p2d25 result is only **3.5%** max-approximation error gain under independent fitted shared p2, largely limited by p2. Proposed **PARK this p1-only weighting micro-direction**, pending PI final approval. Any future continuation needs a **materially distinct quantified cost/resource mechanism**, not repeated polynomial degree grid sweeps.

**Other targets unchanged:** SPRU 2025/651 I156–I159 HYBRID KeySwitch rounding-noise microaudits **PARKED by PI assent**; original Cascudo et al. vFHE ePrint 2025/286 P1 ideal PIOP CRT scalar-digit issue I59–I60 **OPEN/HUMAN_REVIEW/SOURCE-GATED** (latest official 2026-02-16 revised PDF raw bytes unavailable; no compiled exploit); I152–I154 integer repair **PARKED**. MRFHE/GL/LFBS/Nested-RNS and other older archives remain. No author outreach without PI approval.

## LAST COMPLETED ITERATION

**I164 (2026-10-13); I165 NOT STARTED.** Record `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md`, blob SHA `e98e0e9724514ed827001c66f19a7d334f43a3f8`. New source-parameter fixed-degree independent p1-only weighting falsifier: **FAIL material-transfer claim**, **PASS tiny positive weighted numerical difference**; no CKKS benchmark.

## CURRENT QUESTION

Is the **p1-only derivative-weighted approximation** genuinely publishable/relevant to a CKKS performance budget when matching actual source parameter Set I r5 K23 eps2^-6, p1 degree53, p2 degree25? I164 found weak ~**1.03525×/3.5%** effect on sampled ideal plaintext composite error, **p2 standalone approximation ≈9.79e−12 dominates first-stage error ≲8.3e−13**. No realized level, modulus or time improvement or demonstrably new technique. Recommend human **PARK** rather than run additional toys; a different **joint p1+p2 precision and CKKS noise/latency** target would require a novel hypothesis and value-of-cost statement before further tests.

## PRIMARY HYPOTHESIS

**NONE ACTIVE**. I164 hypothesis that I162 ~2.14× at *non-source d43 with exact f2* transfers as a **material** gain under source-shaped d53 and approximate d25 **FAILS** in one independent reproducible numerical instantiation. Distinguish weaker statement that p1 weighted vs unweighted at same d53 with shared p2 still changes sign positively: **PASS small ~1.035×**. This is *not* a proof that no weighted method could work on any source parameters.

## CURRENT EVIDENCE

- **[SOURCE ePrint 2025/429 Table3/4]** Authors Table3 **Set I K=23, ε=2^-6**; Table4 r=5 polynomial degree set **(53,25)**, logPQ1547, level11, avg **27.12 bits** bootstrapping precision, #relin20, BTS24.9sec. Authors' §3.2 odd-r p2 sparse `q∘((-1)^((r−1)/2)T_r)` allows r5 `p2=q5◦T5` with q5 approximating scaled asin; §5.1 stage-specific Remez and §5.2 Lattigo implementation. **These metrics are from paper, not measured here.** Full mirror PDF available but version parity UNVERIFIED, original exact p1/p2 arrays not provided.
- **[I164 NEW numerical source-shaped independent test]** `D=union_{j=-22}^{22}[j−1/64,j+1/64]`, r5, common degree25 outer `p2(y)=q5(T5(y))`; odd q5 fitted by a scaled-residual minimax LP to `asin(z)/(2π)` on `|z|≤sin(2πε)=0.0980171403295606`. Unweighted U and derivative-weighted W each use an odd degree53 p1, same input/domain, minimax LP after **analytically subtracting a degree53 Chebyshev–Bessel sine series reference**, scaling tail residual by `10^13` to avoid HiGHS incorrectly returning objective0 for errors ∼1e−12. Max dense-grid error on **45×257=11565** independent points U **1.0612731179970858e−11**, W **1.0251376136860557e−11**, ratio **1.035249418**, ∼**0.0499 ideal bits**. 45×33-point refitting changes ratio to **1.035220864**, stable. Max p2 error on exact f1 alone≈**9.794569669e−12**, whereas derivative-weighted p1 stage U≈8.21266e−13 and W≈4.60114e−13, explaining outer domination. `|p1|<1`, `|T5(p1)|≈0.098`; no branch breakdown. `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md`.
- **[I164 REPRODUCTION]** Local experiment script `/mnt/data/fhe_iteration164_reproduction.py` SHA256 `84b361f336f39381b85ccc8633b68a0b27a725b72ad2047973f61f8666da9f48`; NumPy2.3.5, SciPy1.17.0. Script is user-visible conversation artifact, not a GitHub source file or original Lattigo implementation. Dense-grid numbers not certified continuous global suprema; double precision can affect digits far below reported effect. No encrypted CKKS trace or time/level measurement.
- **[I163 SOURCE-GATED]** No author original Set I r5 (53,25) coefficients, fitting source and benchmark manifest retrieved via scoped GitHub/web search, first-author/lab pages or PDF; tracking `MISSING_SOURCES.md`, prior `findings/ckks-generalized-composite-source-artifact-gate-iteration163.md`. Missing public artifact **not proof none exists**.
- **[I162]** Different example K26 eps2^-8, d43, **exact ideal f2**: U final sampled error2.2671330e−5 vs W1.0584773e−5, factor **2.14188×**, valid only for that toy; **NOT** current Set I source parameters. `findings/ckks-generalized-composite-fixed-degree-weighted-minimax-test-iteration162.md`.
- **[I161/I160]** Paper §§3.3/5.1 stage-specific approximate objectives **do not explicitly optimize first-stage f2'-weight**, but §5.2 **does measure full bootstrapping precision**; ideal source `f2'` can scale `Theta(r²)` at valid odd-r center; math sensitivity alone is standard analysis, not source paper error. Findings `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` and `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
- **[OLDER]** SPRU I156–159 parked; vFHE I59–60 official-source-gated, vFHE fast integer repairs I152–154 parked. All earlier files preserved.

## MAIN OBSTRUCTION

At real Table4 source shape, the independent fitted **p2 approximation error dominates** already tiny p1 error, making p1-only weighted reallocation a minuscule end-to-end ideal plaintext effect. No evidence this changes **CKKS multiplication levels, relinearizations, modulus, runtime, or actually measured 27.12 bits**, and the **actual author's hidden degree(53,25) polynomial coefficient vectors** were not reproduced. A pure 0.05-bit ideal max-error improvement, with different error statistic from paper's avg CKKS bits, is unlikely alone to merit a research project. No novelty comparison with prior weighted minimax literature has been concluded.

## OPEN UNCERTAINTY

Actual Table4 polynomial coefficients and source code, real encryption noise/scale/rescaling, precise stage competition in actual implementation, full Lattigo output precision, alternative jointly optimized polynomial designs, resource constraints/novelty. The published source's version equality to mirror remains VERSION_UNVERIFIED. Do not claim a proof of absolute optimality or that weighted fitting never helps in any regime.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I165 NOT STARTED. HUMAN_REVIEW/PARK GATE:** Recommend PI approve **PARK p1-only weighted CKKS EvalMod** after I164's source-shaped independent comparison because p2 error dominates. If PI wants continuation instead, require a *genuinely distinct* source-grounded and cost-quantified hypothesis (e.g. joint p1/p2 error/level allocation with a precise reduction of one multiplication/rescale or prime against named baseline, and an accessible pinned implementation) before any experiment; avoid arbitrary d/r scans, repeat near-identical polynomial toy tests or claim source Table4 reproduction. If PI approves PARK and pivot, consult `findings/OPEN_RESEARCH_BRANCHES.md` to choose **one** high-value source-available, nonarchived technical claim. vFHE current official document remains SOURCE-GATED and SPRU rounding toys PARKED.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md` — latest source-shaped numbers and limitation.
3. `findings/ckks-generalized-composite-source-artifact-gate-iteration163.md` and `MISSING_SOURCES.md` — author-code missing source.
4. `findings/ckks-generalized-composite-fixed-degree-weighted-minimax-test-iteration162.md` — d43 ideal outer historical positive, different parameter regime.
5. `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md`; `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
6. `findings/OPEN_RESEARCH_BRANCHES.md` — research backlog; must not override active STATE.

## STATUS

**I164 CLOSED: FAIL material source-parameter transfer of I162 improvement / PASS tiny 3.525% same-p1-degree and shared-p2 ideal numerical improvement / UNCLEAR true author 27.12-bit CKKS and performance/novelty. I165 NOT STARTED.** Recommend **PARK p1-only weighted stage** subject to PI. No Lattigo or actual original code execution, no security/correctness error, precision upgrade, algorithmic or speedup claim. SPRU I156–159 PARKED; vFHE P1 OPEN/SOURCE-GATED, fast integer-encoder replacement failures PARKED.
