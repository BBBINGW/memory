# FHE Research State — After Iteration 165

**Checkpoint:** 2026-10-13 · `main` · I165 completed, I166 **NOT STARTED**.
**Authority:** Follow `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`. Historical long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md`, project opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides research target, major pivots, novelty, disclosures and parking; agent executes **one smallest falsifiable technical claim plus one cheapest decisive test** per authorized iteration, then stops.

## CURRENT TARGET

**Bergerat–Chillotti–Ligier–Orfila–Tap, “TFHE Gets Real: an Efficient and Flexible Homomorphic Floating-Point Arithmetic,” IACR ePrint 2025/257, §2.4 Algorithm2/Lemma2 and §4.1.1 Algorithm7 — OPEN / HUMAN_REVIEW after I165.** Research MCP obtained 59pp original GitHub mirror SHA256 `8544b4f2a8c0a22ba9d1d8f0a306e81a014243c7e12a8773e2d36cccf1f61ee2`, VERSION_UNVERIFIED. I165 exposes a standard **scope boundary**: Lemma2 explicitly assumes independently sampled input ciphertext noises; generic correlated LWE ciphertexts, including c and −c, invalidate its 2σ² subtraction variance if this assumption is removed. This is **not a paper defect** under Lemma2's own assumptions. Algorithm7 AlignMantissa uses IntSub* on encrypted exponents and is a real path; whether an actual legal HFP composition can produce such dependence is **UNCLEAR**. Need one genuine source-specific DAG; no more abstract Gaussian-toy variants.

**PI-parked targets:** I164 p1-only derivative-weighted CKKS EvalMod ePrint 2025/429 **PARKED by latest continuation assent**, result ~3.525% independent ideal plaintext output improvement at d53/d25, second-stage error floor dominating; authors' code unavailable, no real level/gain. SPRU 2025/651 I156–159 HYBRID KS rounding microaudit PARKED by PI prior assent. Cascudo et al. vFHE ePrint 2025/286 P1 CRT digit scalar consistency OPEN/SOURCE-GATED (current official revised 2026-02-16 PDF raw bytes missing; no latest-version defect or compiled exploit); I152–154 integer replacement failures PARKED. All other repositories/branches preserve prior status.

## LAST COMPLETED ITERATION

**I165 (2026-10-13), I166 NOT STARTED.** Exact one-gate input-dependence counterexample, archived `findings/tfhe-gets-real-intsub-dependent-input-noise-scope-iteration165.md` blob `dc520576a54530ba745f5011177ff30394794850`. Source §2.4 Algorithm2 line6 and Lemma2 Proof2 physical p16 explicitly assume E1,E2 independent centered Gaussian varσ², so subtracting has variance2σ². Taking legitimate same-secret LWE c1=c (encrypt zero), c2=−c has marginal centered noises E and −E with covariance−σ²; subtraction noise2E variance4σ², exactly factor2 above independence model. Abstract exact enumeration E=±1 verified independently; Gaussian covariance identity is algebraic. §4.1.1 Algorithm7 physical pp29–30 calls IntSub* to compare encrypted exponents; no legal program trace demonstrating such strongly correlated exponents yet.

## CURRENT QUESTION

Can **one actual legal HFP two-step evaluation DAG** create input exponent ciphertexts to Algorithm7 whose noises are correlated (e.g. common refreshed input, sign-flip/linear dependence) so that the independent-noise Lemma2 budget is not composable without an explicit HFP-input independence condition? Any effect must survive source-relevant freshness/PBS/carry representation and noise parameter bound; mere abstract LWE reusing c and −c is **not enough**. Verify by tracing relevant Alg7 exponent outputs, HFP Fp addition/normalization and PBS refresh; if input independence always follows from source preconditions, PARK; if source permits correlated inputs, only a boundary condition—not an attack—unless quantified failure.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I165 narrowly **FAILS the unjustified unconditional marginal-variance-only extension**. Paper explicitly assumes independence, hence no original Lemma2 theorem contradiction. Source pipeline legal-use applicability untested. Next cheapest gate is concrete HFP DAG + source-congruent covariance and threshold check.

## CURRENT EVIDENCE

- **[I165 DERIVED narrow, source verified]** Paper ePrint 2025/257 Lemma2/Proof2 physical p16 assumes input LWE noises independent centered Gaussian var σ_in²; line6 subtracts and uses 2σ_in². For generic dependent inputs (c,−c), covariance −σ² yields variance4σ², attained general max under equal marginal variances by Cauchy–Schwarz. This is **outside source assumptions**, not a proof bug. Algorithm7 AlignMantissa line1 physical p30 invokes IntSub* on two encrypted exponents, real compositional context; author does not prove arbitrary prior exponent-noise independence on inspected pp29–33. Original PDF 59pp Research MCP GitHub mirror SHA256 `8544b4f2a8c0a22ba9d1d8f0a306e81a014243c7e12a8773e2d36cccf1f61ee2` VERSION_UNVERIFIED. Archive `findings/tfhe-gets-real-intsub-dependent-input-noise-scope-iteration165.md`.
- **[SOURCE ePrint 2025/429 Table3/4]** Authors Table3 **Set I K=23, ε=2^-6**; Table4 r=5 polynomial degree set **(53,25)**, logPQ1547, level11, avg **27.12 bits** bootstrapping precision, #relin20, BTS24.9sec. Authors' §3.2 odd-r p2 sparse `q∘((-1)^((r−1)/2)T_r)` allows r5 `p2=q5◦T5` with q5 approximating scaled asin; §5.1 stage-specific Remez and §5.2 Lattigo implementation. **These metrics are from paper, not measured here.** Full mirror PDF available but version parity UNVERIFIED, original exact p1/p2 arrays not provided.
- **[I164 NEW numerical source-shaped independent test]** `D=union_{j=-22}^{22}[j−1/64,j+1/64]`, r5, common degree25 outer `p2(y)=q5(T5(y))`; odd q5 fitted by a scaled-residual minimax LP to `asin(z)/(2π)` on `|z|≤sin(2πε)=0.0980171403295606`. Unweighted U and derivative-weighted W each use an odd degree53 p1, same input/domain, minimax LP after **analytically subtracting a degree53 Chebyshev–Bessel sine series reference**, scaling tail residual by `10^13` to avoid HiGHS incorrectly returning objective0 for errors ∼1e−12. Max dense-grid error on **45×257=11565** independent points U **1.0612731179970858e−11**, W **1.0251376136860557e−11**, ratio **1.035249418**, ∼**0.0499 ideal bits**. 45×33-point refitting changes ratio to **1.035220864**, stable. Max p2 error on exact f1 alone≈**9.794569669e−12**, whereas derivative-weighted p1 stage U≈8.21266e−13 and W≈4.60114e−13, explaining outer domination. `|p1|<1`, `|T5(p1)|≈0.098`; no branch breakdown. `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md`.
- **[I164 REPRODUCTION]** Local experiment script `/mnt/data/fhe_iteration164_reproduction.py` SHA256 `84b361f336f39381b85ccc8633b68a0b27a725b72ad2047973f61f8666da9f48`; NumPy2.3.5, SciPy1.17.0. Script is user-visible conversation artifact, not a GitHub source file or original Lattigo implementation. Dense-grid numbers not certified continuous global suprema; double precision can affect digits far below reported effect. No encrypted CKKS trace or time/level measurement.
- **[I163 SOURCE-GATED]** No author original Set I r5 (53,25) coefficients, fitting source and benchmark manifest retrieved via scoped GitHub/web search, first-author/lab pages or PDF; tracking `MISSING_SOURCES.md`, prior `findings/ckks-generalized-composite-source-artifact-gate-iteration163.md`. Missing public artifact **not proof none exists**.
- **[I162]** Different example K26 eps2^-8, d43, **exact ideal f2**: U final sampled error2.2671330e−5 vs W1.0584773e−5, factor **2.14188×**, valid only for that toy; **NOT** current Set I source parameters. `findings/ckks-generalized-composite-fixed-degree-weighted-minimax-test-iteration162.md`.
- **[I161/I160]** Paper §§3.3/5.1 stage-specific approximate objectives **do not explicitly optimize first-stage f2'-weight**, but §5.2 **does measure full bootstrapping precision**; ideal source `f2'` can scale `Theta(r²)` at valid odd-r center; math sensitivity alone is standard analysis, not source paper error. Findings `findings/ckks-generalized-composite-weighted-error-treatment-audit-iteration161.md` and `findings/ckks-generalized-composite-f1-f2-quadratic-sensitivity-iteration160.md`.
- **[OLDER]** SPRU I156–159 parked; vFHE I59–60 official-source-gated, vFHE fast integer repairs I152–154 parked. All earlier files preserved.

## MAIN OBSTRUCTION

The dependence counterexample is a textbook covariance identity, **not a publishable HFP result**; it uses valid LWE arithmetic but not a demonstrated legal HFP exponent-input pipeline with preserved scaling/magnitude/bias/refresh conditions. Since Lemma2 explicitly states independence, only a source-supported failure to maintain that precondition in a real HFP DAG could create a new proof obligation; threshold and actual failure probabilities remain unknown. Stop if no material source example.

## OPEN UNCERTAINTY

Whether HFP Algo7 receives genuinely independently refreshed exponent ciphertexts under source's full operator API after feedback/reuse; whether correlations from extended CMux, input aliasing and prior subtraction survive KS/PBS; whether any allowed correlations meaningfully affect t² bound, not just proof's conservative variance expression. **No claimed actual protocol bug**.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I166 only if PI authorizes.** ONE source-grounded genuine composability falsifier: trace source §4.1.1 Alg7 and one previous HFP operation (add or mul output exponent), plus any PBS refresh semantics, to construct **one legal two-step HFP computation DAG** feeding jointly dependent exponent ciphertexts into `IntSub*`, or prove source refresh/input restriction precludes the proposed covariance. If cannot realize a valid noise dependence within source, **PARK** as standard independent-assumption scope. No more simple c,-c arithmetic; no author outreach/bug claims.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/tfhe-gets-real-intsub-dependent-input-noise-scope-iteration165.md` — latest scoped result.
3. Research MCP ePrint **2025/257** physical pp15–18 (Algorithm2/Lemma2), pp29–33 (Alg7 input and noise), relevant arithmetic pp37–42 as needed.
4. `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md` — newly parked prior question.
5. `findings/OPEN_RESEARCH_BRANCHES.md` — backlog. vFHE P1/MISSING_SOURCES only if returning with new evidence.

## STATUS

**I165 CLOSED: FAIL unjustified generic correlated-input version of 2σ_in² variance statement / PASS exact covariance counterexample outside author assumption and verified Algorithm7 source call / UNCLEAR relevance to any legitimate two-step HFP floating-point operation. I166 NOT STARTED.** Previous CKKS p1-only weighting ePrint 2025/429 now **PARKED by PI continuation assent**; SPRU microaudit PARKED; vFHE P1 OPEN/SOURCE-GATED. No proven source correctness/soundness failure or FHE performance improvement.
