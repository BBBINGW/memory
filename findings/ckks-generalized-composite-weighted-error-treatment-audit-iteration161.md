# Iteration 161 — Paper 2025/429 optimizes stage approximation errors and empirically benchmarks full CKKS bootstrapping, but does not explicitly state a derivative-weighted first-stage objective

**Date:** 2026-10-13. PI approved continuation via “好的，请继续.” Read-before-write `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I160 SHA `572bbc48cbc3e07069b7ec1ddfa9014367f146a7`, and I160 finding. ONE primary existing-treatment hypothesis and ONE original-source reading/comparison test. No claim of a source error, new algorithm, actual performance improvement or live Lattigo replication.

## Source and provenance

Min, Lee, Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, IACR ePrint **2025/429**. Full 19-physical-page PDF obtained through Research MCP, source_kind `github-mirror`, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, latest official `VERSION_UNVERIFIED`. Re-acquisition cache_hit true. Examined **§3.3 physical pp8–10** and **§5 pp15–17** including actual optimization text, suggested heuristic and real experimental Table4; bibliography pp18–19 inspected but not used for technical inference. Text extraction has layout glyph warnings on some equations; readable prose/objective descriptions sufficient for narrow finding. Prior I160 derivative is independently derived and only valid on exact local ideal `f2∘f1=t` domain.

## ONE hypothesis and decisive reading gate

**[HYPOTHESIS TO FALSIFY]** The paper's published parameter selection **explicitly** minimizes or constrains the composition's **input-dependent first-stage weighted output error**, such as `|f2'(f1(x))| |p1(x)-f1(x)|`, or an equivalent full-composition minimax objective, so that proposing a first-stage derivative weight is merely restating the source algorithm.

**[DECISIVE TEST]** Read §§3.3 and 5.1–5.2 and locate the actual objective, stage precision constraints, choice of r and degrees, and whether end-to-end precision is measured. Compare these exact source-defined operations with the derivative-weighted criterion. A source-specified composition-error objective would eliminate the novel-weight idea at this level; an explicitly separated criterion leaves only an *unverified candidate design space*, not proof it improves source.

## Findings separated by evidence type

1. **[FACT; §3.3 pp8–10]** Authors define `E(t,p;S)` as averaging polynomial values on integer-shifted intervals and `Var(f,p;S)` as an integrated squared stage-fit loss. They formulate **a constrained least-squares minimization for degree-d polynomial p and selected period classes**, derive Lemma1, and convert to a convex quadratic system, with constraints fixing endpoint/scale to prevent trivial constant solution. Their Fig1 compares stage approximation errors to their stage L2 lower-bound baseline. **No f2 derivative factor or explicit full two-polynomial composition error objective appears in this formulation.** §3.3 is a *stage-level lower-bound analysis*, not necessarily the actual final source Remez routine.

2. **[FACT; §3.1 pp6–7 and §5.1 p16]** Actual sine/inverse-sine composite approximants are obtained via multi-interval Remez; §5.1 starts with intended `eps_bits` output precision, then specifies both p1 and p2 **separately achieve** `eps_bits`-class approximation errors, optimizes inverse-sine/f2 degree, selects r subject to outer stage level and polynomial-degree cost, and finally fits first-stage f1 with the same stated approximation precision. **No explicit derivative-weighted inner error budget `eps_inner(x)≈eps_final/|f2'(f1(x))|`, joint composition minimax, or formal cross-stage error-propagation bound is stated in the inspected text.** Do NOT infer the authors' undocumented implementation ignores this, nor assert an error in parameter selection. Their chosen p2 is a polynomial approximation of f2: I160's exact f2' need not equal p2's derivative everywhere.

3. **[FACT; §5.2 pp16–17]** The paper explicitly implements their algorithm in Lattigo, selecting r and stages under practical level budgets and **measures end-to-end bootstrapping precision** and timings. Table4 reports Set I 'Ours' r5 (degree set 53,25), measured average precision **27.12 bits**; r6 (47,2,15) **27.40 bits**; r12 (31,2,2,15) **26.42 bits**. Set II reports 'Ours' r3 (57,15) **28.70 bits**, r6 (39,2,15) **28.76 bits**, r11 (29,55) **28.75 bits**, r12 (27,2,2,15) **28.76 bits**. These data demonstrate the authors *empirically check actual precision* and explore r tradeoffs; the source does not state that the inner derivative is an unrecognized correctness/soundness issue. Authors’ alternative rescale-fused BSGS linear-transform speedup is a separate, already implemented source contribution not implicated by this audit.

4. **[DERIVATION; I160]** For odd r=4k+1 at allowed k=(r−1)/4, ideal `f1(x)=sin(2πx/r)`, exact local `f2(f1(x))=t(x)` imply `A_r=|f2'(f1(k))|=r/[2π sin(π/(2r))]≈r²/π²`. For independently injected small additive inner-stage δ, `f2(f1(k)+δ)-t(k)≈A_r δ`. This makes the candidate `min_{deg p1=d} max_{x in legal D} |f2'(f1(x))| |p1(x)-f1(x)|` (or a polynomial p2-aware and finite-error variant) **different in form** from §3.3's unweighted surrogate and §5.1's separately required stage-error budgets. However optimization of this new criterion is NOT necessarily better after respecting p2 error/scale/cost.

## Answer to source-existing-treatment hypothesis

**STATUS: FAIL for the hypothesis of an EXPLICIT weighted objective in the inspected original source; PASS as a source-grounded audit of criterion differences; UNCLEAR any positive contribution.** The authors have stage-specific L2/minimax approximation and actual end-to-end precision testing. They do **not explicitly formulate** an input-dependent first-stage f2'-weighted approximation or equivalent full-composition optimization in the inspected §§3.3/5.1. That absence **does not** establish a missed correctness proof, any error, novelty, or actual algorithm improvement. The documented end-to-end performance makes overclaim particularly dangerous.

In general if `p1,p2` replace f1,f2 and `t=f2∘f1`, the source-model decomposition
```
 p2(p1(x))−t(x)
 = [p2(p1(x))−f2(p1(x))]
   +[f2(p1(x))−f2(f1(x))]
```
permits the local linear sensitivity analysis when p1(x) remains in the same differentiable branch. If p1(x) exits the branch or the output is evaluated in CKKS with noise, a derivative at f1(x) is insufficient and a proven domain/tail bound is necessary. §5 actual precision already aggregates errors experimentally.

## ONE recommended next gate (PI-controlled)

**I162 only if authorized.** The cheapest *value-of-contribution falsifier* is ONE source-domain **fixed-degree comparison** (prefer §3.3 K=26, eps_domain=2^−8, odd r=5 with a small explicitly fixed p1 degree `d` and identical f2 ideal branch), comparing:
- independent **unweighted** multi-interval minimax polynomial approximation to `f1(x)=sin(2πx/5)` on legal near-integer domain, and
- **derivative-weighted** minimax approximation at the *same degree* minimizing first-order output error;
calculate actual **true composition max error** `max_{x∈D}|f2(p1(x))-t(x)|` with rigorous or dense-grid error verification. One test/primary hypothesis: fixed-degree derivative weighting strictly reduces actual composite worst-case error; if not, PARK the branch rather than invent a new optimizer. Both would need source-compatible legal r and K, no real CKKS speedup or publishable claim absent actual level/cost change. Avoid interpreting source experimental r5 degree53 p1 as replaceable at small toy degree without a separate source-grade comparison.

## End of Iteration 161

**STATUS:** PASS source criterion audit; FAIL hypothesis of explicit f2'-weighted objective; **UNCLEAR** practical advantage, novelty and source-version parity.
**RESULT:** §3.3 optimizes stage unweighted L2/variance surrogate, §5.1 separately allocates accuracy thresholds to f1 and f2 and chooses r/degree, §5.2 **does** measure end-to-end CKKS precision and speed. Thus I160's sensitivity is not explicitly the objective but cannot be called omitted/unaccounted for in the implementation without a true fixed-degree paired test.
**NEXT_ACTION:** I162 fixed-degree matched-domain weighted vs unweighted composite error **ONE** toy test under PI approval; no other topic/new code scan.
**STATE_UPDATE:** YES — source-backed discriminating feasibility gate and refined exact claim; keep current research direction OPEN, no novelty assertion; SPRU toy branch PARKED, vFHE P1 source-gated.
