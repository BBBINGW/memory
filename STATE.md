# FHE Research State — After Iteration 160

**Checkpoint:** 2026-10-13 · `main` · I160 completed, I161 **NOT STARTED**.
**Authority:** Current compact research session checkpoint; historical 84,552-character state preserved in `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`); opportunity backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides pivots, novelty, disclosure and continuation. Exactly ONE hypothesis/test per authorized iteration.

## CURRENT TARGET

**CKKS generalized polynomial-composite EvalMod conditional precision–arithmetic frontier — ACTIVE RESEARCH DIRECTION / no active experiment after I160.** Seonhong Min, Joon-Woo Lee and Yongsoo Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, ePrint **2025/429**, https://eprint.iacr.org/2025/429; full **19 physical pages** read via Research MCP source_kind **github-mirror**, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, official edition **VERSION_UNVERIFIED**. §3.1–3.3 (physical pp6–10), §5 (pp15–19). Key question: does authors' approximation/parameter pipeline account for the large **local f2 derivative `Θ(r²)`** at certain legal integer centers in the source odd-r `t=f2∘f1` decomposition, and if not, is there any distinct source-backed improvement after joint error/degree check? This is a mathematical conditioning observation, **not a confirmed source flaw, novel algorithm or CKKS precision improvement**.

**Former SPRU target (PI PARK decision):** Coron–Köstler SPRU ePrint **2025/651**, single-slot Trace HYBRID rounding covariance microaudits **I156–I159 now PARKED following PI assent** to prior turn's explicit recommendation to stop and pivot. I159 170-case one-P/Q conditional bias averages to zero over uniform a for *incremental* new-key noise, with separate e0 baseline bias. Full actual multi-prime OpenFHE source Table2 precision still UNCLEAR. No new toy variant unless new material premise; original author code and tagged OpenFHE v1.4.2 available. See `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md`.

**Unresolved earlier parent P1 (not dropped):** Cascudo et al. vFHE ePrint **2025/286**, ideal PIOP CRT diagonal integer scalar-digit membership I59–60 remains **OPEN/HUMAN_REVIEW / SOURCE-GATED**. Mirror 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, current official revised 2026-02-16 PDF bytes unavailable; no compiled-SNARK exploitation or current-official security finding verified. Three fast integer ECC repair variants I152–154 **PARKED**. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md`. All other MRFHE/GL/LFBS/Nested-RNS archives preserved and unchanged.

## LAST COMPLETED ITERATION

**I160 (2026-10-13); I161 NOT STARTED.** Source-anchored odd-r local perturbation sensitivity **PASS**; r-independence hypothesis **FAIL**. See `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md` blob SHA `4e67c4aea41f7d8a3b64de9833d9b8bbfe36d536`. One analytic chain rule + five r cases finite-difference, not FHE implementation.

## CURRENT QUESTION

Source §3.1 sets odd `r`, `f1(x)=sin(2πx/r)` and `f2∘f1(x)=x−round(x)` on legal near-integer domains, and asserts polynomial approximation of f1 and f2 can be selected jointly to improve efficiency. I160 shows a potentially significant error-conditioning effect: **for `r=4k+1`, `x=k` in the allowed source domain**, `f1'(k)=(2π/r)sin(π/(2r))`, hence `f2'(f1(k))=r/(2π sin(π/(2r)))~r²/π²`. Does the actual polynomial selection already optimize a *weighted end-to-end* metric that respects this amplification? If yes, kill speculation about a missed optimization; if not, test a measurable fixed-degree candidate only with a precise source comparable baseline.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I160 hypothesis that increasing r doesn't impose intrinsic r-dependent inner-stage-error sensitivity fails under exact chain rule. Falsifier family `r=4k+1`, valid integer x=k, exact local `t'(k)=1`: `A_r=|f2'(f1(k))|=r/[2π sin(π/(2r))]=Θ(r²)`. In a differentiable f2 ideal target, a *hypothetical independent small* inner error δ is amplified locally `A_r δ+O(δ²)`. This is conditional first-order worst-local sensitivity, **not an assertion of actual f1 polynomial or CKKS ciphertext error**, which can depend on x and potentially cancel.

## CURRENT EVIDENCE

- **[I160 FACT source+DERIVATION]** Original ePrint 2025/429 §3.1 physical pp6–7 exact odd-r sine inner stage, inverse-sine+r-th-angle outer stage; §3.3 pp8–10 independent approximation lower-bound studies, §5 runs joint polynomial degrees. Analytical `f1'(k) A_r=1`. Finite-difference derivative of locally source-faithful `f2(y)=arcsin(sin(r·arcsin y))/(2π)` at y=f1(k), h1e−8, agreement better than 6e−9 relative for r5,9,17,33,49 with K26 legal centers. A_r ≈2.575,8.249,29.324,110.380,243.314; r49/r5 94.48× =6.562 extra *hypothetical local p1 precision bits* for same final tolerance. Paper mirror SHA `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, official version UNVERIFIED, extraction math warnings. Archive `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
- **[I159 PARKED, not re-opened]** SPRU source-shape two-component rounding at one P/Q: conditional fixed a bias vs unconditional zero *incremental e* mean under uniform a; 170 exact pairs, increment variance1/5, noiseless rounding baseline −4/5. Original SPRU source precision/covariance still UNKNOWN. `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md`, earlier I156–158 archives.
- **[P1 SOURCE-GATED]** vFHE I59–60 ideal proof/CRT scalar consistency finding requires authentic latest official 2026-02-16 PDF. I152–154 fast integer code alternatives low minimum distance; PARKED. No attack/bug latest version or source performance established.
- **[OTHER PARKED]** MRFHE mixed-radix source implementation absent; matrix rectangular artifact inaccessible; FAB easy sparse-key block repair already prior art; LFBS 2025/022, Nested RNS 2025/346, GL generic BigSwitch etc already audited and archived. Use backlog before choosing any new target.

## MAIN OBSTRUCTION

Local f2 sensitivity `Θ(r²)` is an **elementary inverse-function condition number**, not by itself a finding the source authors missed an important cost. Their polynomial approximation stages and §5 may explicitly budget it through joint minimax/Remez or per-stage precision. Real CKKS error propagation also includes polynomial approximation residuals, encoded scaling/quantization and multiplicative noise; a local derivative alone cannot demonstrate table-level error or speedup. Work must **first test for existing author treatment**, not build a new approximate-polynomial optimizer from speculation.

## OPEN UNCERTAINTY

Whether authors already fully optimize `|f2'|·|p1−f1|` (or equivalent end-to-end target), error-correlation/cancellation, actual r selected in Tables and their precision, whether weighted polynomial designs yield strict budget improvement at fixed depth/rotations and source-comparable implementation; novelty against prior constrained polynomial approximation work. Latest official 2025/429 PDF unverified; known mirror text sufficient for current conditional derivation, but do not assert latest-edition defect.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I161 only if PI authorizes.** ONE source-grounded decisive **existing-treatment** gate: read ePrint 2025/429 §3.3 (physical pp8–10), §5 parameter selection and experimental description (pp15–19) and identify whether approximation/degree optimization explicitly enforces end-to-end weighted first-stage error `|f2'(f1(x))|·|p1(x)−f1(x)|` or an equivalent true-composition error objective. If already handled, **PARK** a novelty-by-reweighting idea. If absent or only fixed independent error budgets, propose ONE minimal comparable weighted-vs-unweighted **fixed-degree** diagnostic with source parameters; do NOT claim a missing proof or publishable result merely because the weight is not written. No author outreach/disclosure. No return to SPRU rounded-toy or vFHE encoder dead ends.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md` — active target, provenance and exact derivative.
3. Full Research MCP ePrint **2025/429** §3.1–3.3 pp6–10, and §5 pp15–19 **as needed for gate**.
4. `findings/OPEN_RESEARCH_BRANCHES.md` — backlog index; must not override STATE.
5. `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md` — parked prior target (only on need).
6. `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md` — prior source-blocked issue (only if returning).

## STATUS

**I160 CLOSED: PASS exact source odd-r quadratic local inner-error sensitivity / FAIL r-independent error-tolerance hypothesis / UNCLEAR whether author already budgets this effect or it yields any novel optimization. I161 NOT STARTED.** PI assented to PARK SPRU I156–159 microaudits; vFHE P1 stays OPEN/SOURCE-GATED and I152–154 code-repair failures PARKED. New 2025/429 polynomial-composition precision budget question is the current research direction; no source-paper error or FHE implementation performance claim.
