# FHE Research State — After Iteration 161

**Checkpoint:** 2026-10-13 · `main` · I161 completed, I162 **NOT STARTED**.
**Authority:** Current compact research session checkpoint; historical 84,552-character state preserved in `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (SHA `7641c5eb985497ae77e9284ed9e94a5713f3222d`); opportunity backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides pivots, novelty, disclosure and continuation. Exactly ONE hypothesis/test per authorized iteration.

## CURRENT TARGET

**CKKS generalized composite EvalMod inner-stage approximation objective — OPEN/HUMAN_REVIEW, no active experiment after I161.** Source: Seonhong Min, Joon-Woo Lee, Yongsoo Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, IACR ePrint **2025/429**, https://eprint.iacr.org/2025/429, Research MCP full 19pp `github-mirror` SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, **VERSION_UNVERIFIED**. I160 derives a source-exact odd-r local f2 derivative `Theta(r²)`; I161 audits §3.3/§5's actual optimization. Need decide if a derivative-weighted **fixed-degree** first-stage approximation has any actual end-to-end approximation advantage, then check FHE relevance. This is **NOT a paper flaw, new algorithm, or measured CKKS improvement**.

**PARKED by PI assent after I159:** SPRU ePrint 2025/651 I156–I159 microaudits on source-shaped HYBRID KS conditional rounding bias; uniform public-a averages the toy incremental e bias to zero, full realistic precision unknown. Do not re-run toy variants.

**Preserve vFHE P1:** ePrint 2025/286 CRT diagonal digit consistency I59–60 ideal-PI OP mirror-backed observation remains **OPEN/HUMAN_REVIEW/SOURCE-GATED**, with official 2026-02-16 PDF bytes still missing and compiled SNARK impact unknown; three fast integer-encoder repair failures I152–154 PARKED. Archives and missing-source request unchanged. All earlier MRFHE/GL/LFBS etc backlogs remain unchanged.

## LAST COMPLETED ITERATION

**I161 (2026-10-13); I162 NOT STARTED.** Performed ONE source-existing-treatment gate `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` blob SHA `c01addaa855193067df5636dc4776cc2ba2329bd`. **FAIL hypothesis that §3.3 or §5.1 EXPLICITLY optimizes derivative-weighted end-to-end p1 error. PASS source reading. UNCLEAR real improvement.** Source §3.3 pp8–10 uses unweighted L2/variance stage approximability surrogate with constrained quadratic system and Lemma1; §5.1 p16 separately chooses inverse-sine/f2 and p1 approximation accuracies, r and degrees; §5.2 pp16–17 explicitly benchmarks full CKKS precision and time in Lattigo (Table4), so never assert the authors ignored final error or committed a correctness error.

## CURRENT QUESTION

Can **one fixed-degree, source-domain** derivative-weighted first-stage polynomial approximant `p1` for odd r5, K26, domain halfwidth eps=2^-8 decrease actual true composition max error `||f2∘p1 - t||_∞` compared with the unweighted minimax approximant **without changing degree, outer f2 or legal input domain**? First determine whether any numerical improvement survives a fair same-degree test, *before* asserting CKKS level/latency gain. Source already assesses real bootstrapping precision, novelty is NOT established.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I160 (confirmed) ideal odd-r stage `f1(x)=sin(2πx/r)` satisfies `f2∘f1=t` locally; for r4k+1 valid center xk, `|f2'(f1(k))|=r/[2π sin(π/(2r))]=Theta(r²)`. This makes weighted inner-stage error a plausible objective but NOT proof of a better polynomial approximation or scheme. I161 (source-confirmed) **no explicit weight/composition minimax** in inspected §§3.3/5.1, yet §5.2 **does empirically assess complete bootstrapping precision**. Do not overstate absence: the source may indirectly account for conditioning in Remez degree choices and measured results; official latest version unverifed.

## CURRENT EVIDENCE

- **[I161 FACT; existing-treatment gate PASS / explicit-weight hypothesis FAIL]** Exact original mirror ePrint 2025/429 §3.3 physical pp8–10: unweighted constrained stage L2/`Var(f,p;I)`, Lemma1, Fig1 and linear-system lower bound (not necessarily actual fitting algorithm). §5.1 p16: select inverse-sine approximation error/degree, choose r under outer stage levels and polynomial evaluation cost, then fit f1 with separately specified precision; **no explicitly optimized objective `|f2'(f1)|·|p1−f1|` nor full-composition constrained minimax in those sections**. §5.2 pp16–17 performs actual end-to-end Lattigo precision/timing experiments: Table4 Set I 'Ours' r5 27.12bits, r6 27.40, r12 26.42; Set II r3 28.70, r6 28.76, r11 28.75, r12 28.76. These show authors DO consider output quality empirically; omission claim limited to published formula, not implementation intent. Archive `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md`.
- **[I160 FACT source+DERIVATION]** Original ePrint 2025/429 §3.1 physical pp6–7 exact odd-r sine inner stage, inverse-sine+r-th-angle outer stage; §3.3 pp8–10 independent approximation lower-bound studies, §5 runs joint polynomial degrees. Analytical `f1'(k) A_r=1`. Finite-difference derivative of locally source-faithful `f2(y)=arcsin(sin(r·arcsin y))/(2π)` at y=f1(k), h1e−8, agreement better than 6e−9 relative for r5,9,17,33,49 with K26 legal centers. A_r ≈2.575,8.249,29.324,110.380,243.314; r49/r5 94.48× =6.562 extra *hypothetical local p1 precision bits* for same final tolerance. Paper mirror SHA `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, official version UNVERIFIED, extraction math warnings. Archive `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
- **[I159 PARKED, not re-opened]** SPRU source-shape two-component rounding at one P/Q: conditional fixed a bias vs unconditional zero *incremental e* mean under uniform a; 170 exact pairs, increment variance1/5, noiseless rounding baseline −4/5. Original SPRU source precision/covariance still UNKNOWN. `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md`, earlier I156–158 archives.
- **[P1 SOURCE-GATED]** vFHE I59–60 ideal proof/CRT scalar consistency finding requires authentic latest official 2026-02-16 PDF. I152–154 fast integer code alternatives low minimum distance; PARKED. No attack/bug latest version or source performance established.
- **[OTHER PARKED]** MRFHE mixed-radix source implementation absent; matrix rectangular artifact inaccessible; FAB easy sparse-key block repair already prior art; LFBS 2025/022, Nested RNS 2025/346, GL generic BigSwitch etc already audited and archived. Use backlog before choosing any new target.

## MAIN OBSTRUCTION

The known `Θ(r²)` inverse-composition derivative is an elementary sensitivity observation, and **the source does not explicitly use it in its stage approximation loss**, but authors' real polynomial selection and evaluated end-to-end bootstrapping precision may already render the weighting negligible or redundant. Any weighted alternative must beat the source-appropriate **same polynomial degree and legal multi-interval domain** in true output error, not simply a surrogate L2 error. Distinct f2 polynomial approximations, nonlinear branch constraints, ciphertext noise, key switching, rescaling, CKKS levels and source Table4 performance are still outside the current ideal-function result.

## OPEN UNCERTAINTY

Whether derivative-weighted polynomials improve **true composition max error** at a *fixed degree* vs unweighted counterparts, whether resulting error gains survive approximate p2/CKKS evaluation and yield level/latency reduction, prior-art novelty, whether actual Table4 parameter set already near best. Latest official 2025/429 version UNVERIFIED. vFHE P1 source-gated, SPRU microaudits parked.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I162 only if PI authorizes. ONE falsifiable value-of-contribution gate:** use ePrint 2025/429 §3.3 K26, domain halfwidth 2^-8 and odd r5, and one small explicitly fixed p1 polynomial degree suitable for reproducible fitting. Fit (a) unweighted fixed-degree minimax approximation to `f1(x)=sin(2πx/5)` on *same multi-interval legal domain* and (b) derivative-weighted minimax `|f2'(f1(x))|·|p1−f1|` at exactly the SAME degree. Independently evaluate each actual **ideal** composite output max error `|f2(p1(x))-t(x)|` with branch safety checked (and sampling/verification tolerance reported). If weighted fitting **does not** beat unweighted on true composite output, **PARK direction**; if it does, proceed only with a more precise source-comparable degree/precision cost question, no premature CKKS improvement claim. No other hypothesis, no re-opening SPRU/vFHE failed repairs.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` — latest source objective audit and next test.
3. `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md` — analytical derivative.
4. Research MCP ePrint 2025/429 §3.1–3.3 pp6–10, §5 pp15–17 as needed.
5. `findings/OPEN_RESEARCH_BRANCHES.md` — backlog. SPRU I159 and vFHE I155/MISSING_SOURCES only if needed.

## STATUS

**I161 CLOSED: PASS primary-source objective audit / FAIL exact explicit derivative-weighted objective present in inspected paper §§3.3/5.1 / UNCLEAR actual improvement or novelty. I162 NOT STARTED.** Source explicitly benchmarks complete CKKS bootstrapping output precision, so no conclusion that authors overlooked end-to-end error; unweighted vs weighted fixed-degree toy needed. SPRU I156–159 PARKED, vFHE P1 OPEN/SOURCE-GATED, all other archived failures preserved. No actual performance/correctness/security claim.
