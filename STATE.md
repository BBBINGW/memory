# FHE Research State — After Iteration 166

**Checkpoint:** 2026-10-13 · `main` · I166 completed, I167 **NOT STARTED**.
**Authority:** Follow `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`. Historical long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md`, project opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides research target, major pivots, novelty, disclosures and parking; agent executes **one smallest falsifiable technical claim plus one cheapest decisive test** per authorized iteration, then stops.

## CURRENT TARGET

**TFHE Gets Real**, Bergerat–Chillotti–Ligier–Orfila–Tap, ePrint **2025/257** Algorithm2 IntSub* independence assumption → Algorithm7 AlignMantissa → Algorithm9 Addition source-input-composability audit **HUMAN_REVIEW / RECOMMEND PARK after I166**. Full 59pp GitHub mirror acquired via Research MCP SHA256 `8544b4f2a8c0a22ba9d1d8f0a306e81a014243c7e12a8773e2d36cccf1f61ee2`, latest official VERSION_UNVERIFIED. I165 shows generic LWE c,-c invalidates **unjustified extension** of author's explicitly **independent-noise** line6 variance2σ². I166 checked one **legitimate** HFP two-step DAG using the same Algorithm6 refreshed ciphertext twice in Algorithm9: exponent subtraction `ce-ce` cancels noise, variance **0**, not dangerous 4σ². No valid HFP program with negative covariance or threshold failure identified. **Recommend PARK this low-novelty noise scope track rather than further textbook covariance toys; human PI final decision**.

**Other preserved branches:** 2025/429 CKKS p1-only derivative weighting PARKED by PI after I164 (3.5% ideal p1-only d53/d25 improvement, dominated by p2); SPRU 2025/651 noise toy I156–159 PARKED; 2025/286 vFHE P1 CRT common scalar-digit issue OPEN/SOURCE-GATED pending authentic current official February 2026 PDF; integer-encoder I152–154 PARKED. Older closed/reopen-if targets preserved.

## LAST COMPLETED ITERATION

**I166 (2026-10-13); I167 NOT STARTED.** ONE legal composition falsifier `F' = CarryPropagateFloat(F)`, then `Addition(F',F')`, so Algorithm9 line1→Algorithm7 line1→Algorithm2 IntSub*(ce,ce) with the same refreshed HFP exponent limb. Legitimate reuse with identical noise E on both limbs yields difference0, **Cov=+σ²**, Var(E−E)=0; does NOT realize I165's harmful abstract c,-c negative-covariance pair. Original paper §3.4 Algorithm6 pp26–27 refresh; §4.2 Algorithm9 pp37–40 explicitly chains addition and assumes outputs of Algorithm6, but no proof of independence of aliased inputs. Finding `findings/tfhe-gets-real-hfp-input-alias-correlation-gate-iteration166.md` SHA `c20546f21b1d5be7556490812d9cd188c7da7a7b`.

## CURRENT QUESTION

Is there a **source-valid, naturally arising HFP DAG** with negative enough correlation of exponent ciphertext noise reaching IntSub* that it yields a **new nontrivial parameter/correctness/cost issue** beyond the authors' explicit independence assumption? I166's obvious legal self-alias **does not** witness this: it makes variance smaller. Hence **NONE ACTIVE**; recommend PARK unless actual concrete workflow plus failure/cost target is supplied.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I165 was generic covariance extension failure outside paper assumptions. I166 source-lawful self-reuse yields correlated inputs but **no harmful inflation**; no actual implementation or parameter/security claim.

## CURRENT EVIDENCE

- **[I166 FAIL harmful self-alias hypothesis, PASS actual legal source call path]** §3.4 Algorithm6 physical pp26–27 refreshes, §4.2 Algorithm9 pp37–40 accepts two HFPs and calls Algorithm7 line1 and IntSub* to subtract exponents. Passing same refreshed ciphertext `F'` twice yields exponent `ce-ce` and error `E-E=0`, Var0, not an independent-model 2σ² or negative-cov 4σ². This contradicts automatic harmfulness of input re-use; does NOT prove all legal HFP input correlations safe, or that all refresh outputs independent. Archive `findings/tfhe-gets-real-hfp-input-alias-correlation-gate-iteration166.md`.
- **[I165 DERIVED narrow, source verified]** Paper ePrint 2025/257 Lemma2/Proof2 physical p16 assumes input LWE noises independent centered Gaussian var σ_in²; line6 subtracts and uses 2σ_in². For generic dependent inputs (c,−c), covariance −σ² yields variance4σ², attained general max under equal marginal variances by Cauchy–Schwarz. This is **outside source assumptions**, not a proof bug. Algorithm7 AlignMantissa line1 physical p30 invokes IntSub* on two encrypted exponents, real compositional context; author does not prove arbitrary prior exponent-noise independence on inspected pp29–33. Original PDF 59pp Research MCP GitHub mirror SHA256 `8544b4f2a8c0a22ba9d1d8f0a306e81a014243c7e12a8773e2d36cccf1f61ee2` VERSION_UNVERIFIED. Archive `findings/tfhe-gets-real-intsub-dependent-input-noise-scope-iteration165.md`.
- **[SOURCE ePrint 2025/429 Table3/4]** Authors Table3 **Set I K=23, ε=2^-6**; Table4 r=5 polynomial degree set **(53,25)**, logPQ1547, level11, avg **27.12 bits** bootstrapping precision, #relin20, BTS24.9sec. Authors' §3.2 odd-r p2 sparse `q∘((-1)^((r−1)/2)T_r)` allows r5 `p2=q5◦T5` with q5 approximating scaled asin; §5.1 stage-specific Remez and §5.2 Lattigo implementation. **These metrics are from paper, not measured here.** Full mirror PDF available but version parity UNVERIFIED, original exact p1/p2 arrays not provided.
- **[I164 NEW numerical source-shaped independent test]** `D=union_{j=-22}^{22}[j−1/64,j+1/64]`, r5, common degree25 outer `p2(y)=q5(T5(y))`; odd q5 fitted by a scaled-residual minimax LP to `asin(z)/(2π)` on `|z|≤sin(2πε)=0.0980171403295606`. Unweighted U and derivative-weighted W each use an odd degree53 p1, same input/domain, minimax LP after **analytically subtracting a degree53 Chebyshev–Bessel sine series reference**, scaling tail residual by `10^13` to avoid HiGHS incorrectly returning objective0 for errors ∼1e−12. Max dense-grid error on **45×257=11565** independent points U **1.0612731179970858e−11**, W **1.0251376136860557e−11**, ratio **1.035249418**, ∼**0.0499 ideal bits**. 45×33-point refitting changes ratio to **1.035220864**, stable. Max p2 error on exact f1 alone≈**9.794569669e−12**, whereas derivative-weighted p1 stage U≈8.21266e−13 and W≈4.60114e−13, explaining outer domination. `|p1|<1`, `|T5(p1)|≈0.098`; no branch breakdown. `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md`.
- **[I164 REPRODUCTION]** Local experiment script `/mnt/data/fhe_iteration164_reproduction.py` SHA256 `84b361f336f39381b85ccc8633b68a0b27a725b72ad2047973f61f8666da9f48`; NumPy2.3.5, SciPy1.17.0. Script is user-visible conversation artifact, not a GitHub source file or original Lattigo implementation. Dense-grid numbers not certified continuous global suprema; double precision can affect digits far below reported effect. No encrypted CKKS trace or time/level measurement.
- **[I163 SOURCE-GATED]** No author original Set I r5 (53,25) coefficients, fitting source and benchmark manifest retrieved via scoped GitHub/web search, first-author/lab pages or PDF; tracking `MISSING_SOURCES.md`, prior `findings/ckks-generalized-composite-source-artifact-gate-iteration163.md`. Missing public artifact **not proof none exists**.
- **[I162]** Different example K26 eps2^-8, d43, **exact ideal f2**: U final sampled error2.2671330e−5 vs W1.0584773e−5, factor **2.14188×**, valid only for that toy; **NOT** current Set I source parameters. `findings/ckks-generalized-composite-fixed-degree-weighted-minimax-test-iteration162.md`.
- **[I161/I160]** Paper §§3.3/5.1 stage-specific approximate objectives **do not explicitly optimize first-stage f2'-weight**, but §5.2 **does measure full bootstrapping precision**; ideal source `f2'` can scale `Theta(r²)` at valid odd-r center; math sensitivity alone is standard analysis, not source paper error. Findings `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` and `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
- **[OLDER]** SPRU I156–159 parked; vFHE I59–60 official-source-gated, vFHE fast integer repairs I152–154 parked. All earlier files preserved.

## MAIN OBSTRUCTION

Trivial LWE covariance and straightforward legal aliasing are not FHE contribution; original Lemma2 explicitly assumes independent Gaussian inputs. No source-valid negative exponent noise correlation, actual t bound violation, distribution of PBS/CMux output dependencies, or quantified true system gain established. Do NOT describe a verified HFP bug, and do not run more c,c / c,-c toy variations.

## OPEN UNCERTAINTY

[UNCLEAR] Whether a *nontrivial* correlated exponent pair with negative covariance arises after permitted HFP circuit bootstrapping and preserves representation, and whether its variance breaks authors' declared preconditions. Novelty relative to variance-aware cryptographic noise analyses not reviewed. Without a concrete constructive path and measurable outcome, recommend park.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I167 NOT STARTED; HUMAN_REVIEW/PARK recommendation**. PI assent to PARK TFHE 2025/257 generic covariance microaudits and pivot to a distinct verified primary-source accessible FHE question, consulting `findings/OPEN_RESEARCH_BRANCHES.md` and previous archives; OR give a genuinely new source-valid HFP two-step DAG with **negative** covariance and concrete threshold failure or efficiency gain. Do not overextend I165–166 as paper flaw; no further paired-noise toy. vFHE P1 stays source-gated and prior archives unchanged.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/tfhe-gets-real-hfp-input-alias-correlation-gate-iteration166.md` — exact legal source DAG and failure of harmful-noise claim.
3. `findings/tfhe-gets-real-intsub-dependent-input-noise-scope-iteration165.md` — earlier generic independent-premise boundary.
4. Original ePrint 2025/257 p16 and pp26–27, pp29–30, pp37–40.
5. `findings/OPEN_RESEARCH_BRANCHES.md` — long-term backlog, old sources as needed.

## STATUS

**I166 CLOSED: FAIL hypothesis that a legal self-aliased HFP two-step DAG yields the harmful negative-covariance 4σ² case; PASS exact `ce-ce` cancellation in actual Alg6→Alg9→Alg7→Alg2 source flow. I167 NOT STARTED.** Source Lemma2 explicitly assumes independent noise, no paper flaw or actual floating point failure shown. Recommend **PARK 2025/257 generic covariance noise microaudit** (PI decision). CKKS p1-only weighting and SPRU prior branches PARKED, vFHE P1 OPEN/SOURCE-GATED; other archives retained.
