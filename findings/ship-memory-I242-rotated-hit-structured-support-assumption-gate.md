# SHIP-I242 — Original SHIP structured sparse support versus rotated-primal-hybrid hit probabilities: an exact counterexample and a source-distribution compatibility caveat

**Date:** 2026-10-16. **PI-selected SHIP** active research only. I241 completed; I242 executed ONE falsifiable technical hypothesis + ONE minimal test. No pivot to CGS/VFHE/EXPLORE and no new HMux memory primitive. Source original Cheon–Hanrot–Kim–Stehlé SHIP EUROCRYPT2025/ePrint **2025/784** §5.1 p24, §5.2 p24–25. Related attackers: Ogilvie **ePrint2026/279**, Lemmas17–18 p20 (contiguous dropped coordinates, rotational probability approximation); Hou–Jiang **ePrint2026/366**, §3.1 **Assumption1 physical p16**, §5.3 Table5.1 physical p32 (UNIFORM RANDOM dropped index set J, not necessarily contiguous). Preprint cached via Research MCP source_kind github-mirror VERSION_UNVERIFIED. Published combined CRYPTO2026 DOI 10.1007/978-3-032-35377-1_15; **Table5.1 numbers belong to 2026/366 preprint**.

## ONE primary falsifiable hypothesis and decisive test

**H242:** The rotated-hybrid hit formula `P_rot≈1−(1−p_single)^N` calibrated for a uniform fixed-HW secret is **unconditionally accurate for every SHIP secret satisfying its regularly-spaced support-window policy**, so the published Table5.1 estimates (117.7 bits for logN13,h31,logq55; 122.3 for logN14,h31,logq100) may be transferred unchanged WITHOUT separately checking support distribution and rotation correlations.

**One minimum test:** Read Ogilvie's exact Lemma17–18 and Hou–Jiang's Assumption1, including precise dropped-set selection. Derive exact support-window lower bounds and pairwise rotated-event correlations for original SHIP `N=16384,h=31,w=N/(2h)`, supply exact periodic toy counterexample to unconditional independence with random J, then run one controlled seeded source-shaped Monte Carlo check under **clearly named hypothetical independent uniform one-position-per-window secret distribution**. Do not estimate BKZ/security bits or vary attack parameters to pretend to optimize an attack.

## Primary source/provenance [FACT]

- Original SHIP §5.1: support indexed `i_k` must be in circular position window `[kN/h−w,kN/h+w)`, with `w=max(175,N/(2h))` for experiment. SHIP §5.2 uses sparse `h=31` (not third-party illustrative Poulpy HW192), security pairs `(logN,log(Pq0))=(13,55),(14,100),(15,105)`. The original paper **states an assumption on positions**, but does not here establish a complete sampler law `i_k ~ Uniform(W_k)` for actual implementation.
- Ogilvie 2026/279 Lemma17 p20 assumes `s~Uniform(W(h,N))`, uses **contiguous** dropped coefficient prefix/window length `ζ`. `p(ζ,h_g)=sum_{i<=h_g} C(ζ,i) C(N−ζ,h−i)/C(N,h)`. Lemma18 proposes `P_rot≈1−(1−p)^N` using heuristic independence across rotated contiguous windows. This is the correct target of the contiguous-block source-secret obstruction.
- **Crucial correction preventing a false attack refutation:** Hou–Jiang 2026/366 Assumption1 p16 chooses the dropped set **J uniformly randomly among all k-subsets**, then applies all negacyclic monomial rotations `X^r s`. It assumes permutation-sign symmetric χ_s and claims identical probability `1−(1−p_S)^N` for repeated fresh random J and a single random J under N rotations. Because actual SHIP support constraints are position-dependent, χ_s is NOT uniform permutation-invariant; the assumption requires scrutiny, BUT the *one-rotation* hypergeometric marginal with random J is EXACT for ANY fixed weight-h secret, including SHIP: `p_single=sum_{i<=h_g} C(k,i)C(N−k,h−i)/C(N,h)`. The actual issue is rotation EVENT DEPENDENCE, not one-rotation hypergeometric marginal. **A contiguous interval counterexample from Ogilvie must NOT be presented as a direct refutation of Hou–Jiang's Table5.1.**
- Hou–Jiang 2026/366 §5.3 Table5.1 page32 reports **classical heuristic** enhanced HG-MITM model costs 117.7 (N8192,h31,q2^55) and 122.3 (N16384,h31,q2^100), but no actual key recovery, and does not show source-specific SHIP constrained-support distribution matching. No guarantee those estimates change upon matching; attack remains a serious warning.

## Proof A: deterministic impossibility in CONTIGUOUS dropped-set model [DERIVED/EXECUTED]

At `N=16384,h=31,w=N/(2h)=8192/31`, 31 half-open windows `W_k=[kN/h−w,kN/h+w)` modulo N are DISJOINT, partition all N coefficients with **15 lengths528, 16 lengths529**. Each has its one corresponding mandatory secret nonzero coefficient. For each circular interval I of `ζ=4096` consecutive indices, count `L(I)=#{k: W_k⊆I}`. Exact rational endpoints `ceil(kN/h±w)` yield across all 16384 starts:
- `L(I)=6`: **4065** starts,
- `L(I)=7`: **12319** starts.
Thus `HW(s|_I)≥L(I)≥6` for **every** source-compliant secret and **every** rotation. For `h_g=5`, **actual contiguous rotated hit probability =0**. Uniform fixedHW31 model one-window `p=0.17616805920283873`; extrapolated independence `1−(1−p)^16384≈1`. This proves the generic uniform-secret Lemma17/18 expression is not a correct universal formula for all SHIP-window-constrained secrets in the **contiguous** attack model. Note this exact block contradiction cannot be substituted for Hou–Jiang's random-J attack.

## Proof B: Hou–Jiang RANDOM J event correlations [DERIVED/EXECUTED]

Let support S be fixed, |S|=h, J uniformly random among k-subsets. For fixed rotation r define `A_r={J∩(S+r)=∅}` (enumeration threshold h_g=0). Then regardless of S:
```
p = Pr(A_r)=C(N−h,k)/C(N,k).
Pr(A_0∩A_t)=C(N−|S∪(S+t)|,k)/C(N,k).
```
Second expression depends on autocorrelation `|S∩(S+t)|` and is NOT generally `p²`. Construct source-valid centered support `S={round(j N/31) mod N, j=0..30}`. At actual SHIP N16384, shift `t=1057` yields **30** shared locations out of 31; for random-J `k=4096,h_g=0`, `p=0.00013267362202387054`, and `Pr(A_0∩A_1057)/p²≈5649.397893927865`. This is a direct pairwise independence counterexample for a **legal, unusually regular** SHIP secret; it does NOT by itself compute the full union probability or average-case attack cost.

More elementary exact union counterexample within the same structured-secret family at **toy** N256,h8 (h divides N), support `S={0,32,...,224}` legal for disjoint windows; k128, h_g0; only 32 DISTINCT rotated supports, and those 32 disjoint residue classes partition N. By exact inclusion-exclusion:
```
Pr_J(any rotation misses support)=Σ_{j=1}^{32}(-1)^{j+1} C(32,j) C(256−8j,128)/C(256,128)
=0.10717362623527715;
p_single=C(248,128)/C(256,128)=0.003489942284089333;
independent N=256 formula=1−(1−p_single)^256=0.5913874419354315.
```
So unconditional Hou–Jiang Assumption1 equality is FALSE for this particular legal-window deterministic secret. **But** the source attack assumption is phrased for a permutation-sign symmetric *secret DISTRIBUTION*, and this fixed centered secret is not a valid witness under that *stated probabilistic assumption*. Correct conclusion: it cannot be transferred unmodified as a theorem for SHIP's nonpermutation-invariant support family, NOT that Hou–Jiang's own results are logically contradicted under their intended input model.

## Actual-source-shape illustrative Monte Carlo [EXECUTED; controlled but non-author sampler]

Source-like N16384,h31,k4096,h_g0; randomly sampled J uniformly among size4096; test all 16384 shifts with numpy exact integer support indicators, 2500 Bernoulli trials each, independent seeded RNG `20261016`. **Models:**
- LEGAL CENTER FIXED support = the source-valid nonrepresentative center S above: hit **1011/2500 =0.4044**, Wilson 95% **[0.3853,0.4238]**.
- **ASSUMED** independent uniform one position per SHIP partition cell (NOT verified actual author sampler): hit **2222/2500 =0.8888**, Wilson 95% **[0.8759,0.9005]**.
- True fully uniform unstructured fixed-HW31 comparator: hit **2212/2500 =0.8848**, Wilson 95% **[0.8717,0.8967]**.
- Hoe–Jiang independent N-rotation formula with EXACT one-rotation random J marginal: `1−(1−p)^16384=0.8862632639329526`.

This finding **cuts both ways**: exact legal centered support can violate heuristic substantially; but a very natural SHIP-like *random window secret model* yields actual hit probability statistically CONSISTENT with the original attack independence heuristic at this ONE nonoptimized attack point. Thus mere support-space restriction ~2^-40.88 (I241) does NOT establish that prior 117.7/122.3 estimates are too pessimistic, broken, or that SHIP has some proof of security. Never call those two numbers invalid absent optimized distribution-correct re-estimation.

## Reproducibility

`/mnt/data/ship_i242_window_rotated_hit_audit.py` SHA256 `2e77cf1879b9d46e550971837fe92aa8375fa9184fe69cebbdf92bf8c7cd561c`. Executed in active container, including exact source-window endpoint enumeration, support intersection, exact toy inclusion-exclusion rational arithmetic and 3×2500 source-degree numpy trials. JSON `/mnt/data/ship_i242_window_rotated_hit_probability_results.json` SHA256 `0980ce6205ce255af4ca7f5fc5b1202983b056e8edeee845bf62e51b4cafbd07`. One preliminary run had mismatched hg variables in a test assertion and was corrected **before** execution/archiving; final script assertions and all tests PASS. No Sage/fpylll, no BKZ, no actual key recovery, no numerical change to prior security-bit estimates.

## End of Iteration

**STATUS:** **FAIL universal-source-transfer H242** of independence-model probabilities; PASS both formal counterexamples and source-shaped random-J Monte Carlo; **UNCLEAR security cost of original SHIP's actual key generator**, because complete source sampler, optimized attack k/hg/BKZ parameters, and exact estimator remain unverified. This is a falsification of *unqualified assumption transfer* rather than a demonstration that the 2026 paper's listed attacks are nonviable. In fact source-like random-window model is near original heuristic at the tested point.

**RESULT:** Important precise separation: Ogilvie contiguous dropped coordinate Lemma17/18 is rigorously incompatible with SHIP windows for ζ4096,hg5. Hou–Jiang uniform-random dropped J has the EXACT same one-rotation hypergeom marginal for any fixedHW secret, but the rotations' joint success probability depends on structured support autocorrelations. Actual-window random-sampler simulation at k4096,hg0 DOES NOT reduce apparent attack effectiveness; the mismatch alone cannot challenge 117.7/122.3-bit estimates. Do not generalize a special center secret to typical SHIP.

**NEXT_TEST I243 only upon PI continue:** Check source SHIP author's original regular-spacing **sampling algorithm/implementation** and determine whether one-per-cell uniform draws or some other key distribution is actually used. THEN use *actual optimizer's specific k,hg,* not illustrative k4096,hg0, and measure/derive rotational hit probability under that true distribution; if unavailable, mark SOURCE_BLOCKED/HUMAN_REVIEW, **do not claim attack cost revision or novelty**. User PI decides whether to PARK SHIP line, no silent pivot. **STATE_UPDATE YES** findings/topic/root only; preserve all other tracks.
