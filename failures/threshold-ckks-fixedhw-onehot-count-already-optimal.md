# Iteration 52 — Exact occupancy test: the practical H=45 one-hot count in Threshold-CKKS DKG is already minimal

Date: 2026-10-10
Target: Min, Hanrot, Park, Passelègue, Stehlé, *Distributed Key Generation for Efficient Threshold-CKKS*, IACR ePrint 2025/2057, CCS 2026.
STATUS: FAIL — the hypothesis that the authors overpay for one-hot sampling by using the loose elementary collision bound is **false**.
Novelty: NONE. The published implementation already uses the minimum one-hot count under the independent uniform balls-in-bins target-failure model; no new FHE optimization was discovered.

## Protocol / continuity
Read-before-write: AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, I51 `findings/grafting-sprout-example32-admissibility-epsilon.md` from connected GitHub Notes. Human's "continue" after I51 recommendation selects pivot away from Grafting, which remains archived; parked RIG-HE STATE.md is a distinct branch and is **not changed**. Exactly one primary hypothesis and one exact test this iteration.

## Primary paper and verified original statements
[FACT] Research MCP obtained the **complete 52 physical-page PDF** for ePrint 2025/2057, source kind GitHub mirror; SHA256 `519d1c9672c743b49307de8ebaa1015ba44ff089fae0d1e754482abe40ef764d`; version status unverified.
[FACT] §3.3, physical p.15, **Theorem 2**, evaluates `FixedHWSampler` taking H iid one-hot vectors of dimension K to output a weight-h vector if at least h distinct positions appear among H draws. Condition via occupancy distribution:
 `Pr[#distinct >= h] = sum_(i=h..H) (K)_i S(H,i)/K^H >= 1-epsilon`.
(The paper uses equivalent i! binom(K,i) S(H,i)/K^H.)
It then states a **loose sufficient** inequality `H-h >= (h + ln(1/epsilon)) / ln(K/h)` proven in Appendix B.5.
[FACT] §5.2 physical p.25–26 uses practical `N=2^16`, sparse-secret weight `h=32`, and explicitly says the number of one-hot draws **H=45**, with overall design targeting bootstrapping failure probability <= 2^-128. Note paper also introduces symbol K=160 for EvalMod integer range; this is **not** the K=65536 dimension in Theorem 2! Different scope/notation. Key vector dimension for sampling is K=N=65536.
[FACT] Paper's target and protocol focus: shared DKG without trusted dealer, homomorphic sampling of exactly sparse ternary secret and public eval keys; 4-round implementation CPU/GPU experiments. Different branch from CKKS LCR/Grafting.

## Hypothesis and falsifier
[HYPOTHESIS — FALSIFIED] Since elementary sufficient bound at K=65536,h=32,eps=2^-128 implies H>=48, the paper may actually instantiate H=48 unnecessarily; using a more exact occupancy tail could reduce one-hot generation count by at least 3 and hence expensive CKKS sampling.
[FALSIFICATION CONDITION] Either the paper already selects H<=45 and this is tight by exact occupancy probabilities; or no gap between its chosen H and exact minimum.
[DECISIVE TEST] First read actual §5.2 H; then independently compute the exact probability of having fewer than h distinct bins after H balls using integer recurrence, evaluate exactly against 2^-128 (no stochastic simulation, no CKKS benchmark).

## Exact calculation
[DERIVED] Number of K-ary sequences of length H using exactly k different values is `A(H,k)=(K-k+1)*A(H-1,k-1)+k*A(H-1,k)`, with A(0,0)=1 and A(H,k)=0 outside 0<=k<=H.
 `Pr_fail(H) = sum_(k=0..h-1) A(H,k) / K^H`. Compare exact integers `(2^128)*sum A(H,k) <= K^H`. The failure probability is monotone nonincreasing in H (adding a draw cannot reduce distinct count).
At K=65536,h=32:
 H=44: log2 Pr_fail = -119.928349947, so FAIL vs 2^-128.
 H=45: log2 Pr_fail = -130.120624307, so PASS.
Therefore **H_min=45** is exact for this sampler / failure threshold. Authors **already use H=45**. No extra saving in reducing H without changing the sampler/randomness model/security requirement.
Elementary sufficient bound `H>=48` is 3 vectors/6.25% looser, but not used in the actual implementation. The 6.25% would be a counterfactual improvement over H=48, not a speedup over this paper.
[EXPERIMENT] Exact integer Python script `/mnt/data/iteration52_threshold_ckks_occupancy_exact.py`, SHA256 `f33f3c72349679155ae012c46171e4241f6d7b0343aa4fc83af92eed9f2aec3f`; output `/mnt/data/iteration52_threshold_ckks_occupancy_results.txt` SHA256 `fca4aae275e50550e08bd41a1b1a44868adbd31bb8298e9d1633e82552994e91`. This exact recurrence checks all H=1..50 and verifies total counts K^H, then tests H44 H45 with integer comparisons; Decimal logarithms are only display. All assertions PASS. No HE implementation.

## Scope / potential future research issue
[NEGATIVE] Loose sufficient probability formula in theorem is not evidence of wasted computation: the authors use the exact-minimal H=45. General "improve the collision bound" cannot produce improvement at these parameters.
[IMPORTANT LIMIT] Here 2^-128 addresses **only balls-and-bins fixed-weight sampling failure**, not total statistical correctness of the homomorphic computation: approximate indicator / CKKS decryption rounding, bootstrapping failures, noise flooding, and cryptographic security are separately analyzed and could accumulate. The fact H45 yields ≈2^-130.12 leaves a little margin but does not by itself certify end-to-end <=2^-128. No statement of scheme insecurity is justified without union-bound reconstruction of all independent/conditional failure events and security proof details. Do not conflate §5.2 symbol K=160 (EvalMod approximation range) with vector dimension K=65536.
[PRIOR ART] Theorem2 itself gives exact occupancy expression, and §5.2 picks minimal H already; nothing new.
[RESEARCH NEXT] Meaningful nontrivial new work, if pursued, must change one-hot construction or hardware/nonlinear indicator cost rather than tweak already optimized H. One potentially relevant follow-up is whether §3.1/§3.3 indicator-approximation accuracy at finite CKKS noise requires a stricter bound than their exact-balls probability and whether this can be formalized. However proving an actual gap and novelty before implementation is mandatory; no such gap shown today.

## End of Iteration
STATUS: FAIL — H-overprovision assumption falsified directly by §5.2 and exact combinatorial minimum.
RESULT: Exact H_min=45 vs conservative H>=48, but authors already instantiate H=45, so no one-hot cost improvement. 44 fails and 45 passes 2^-128 occupancy target.
NEXT_ACTION: In the same full paper, read **Theorem 1 and its numerical-error/stability discussion (physical pp.11–14, Appendix B.3)** and test one specific claimed tolerance around the boundary indicator at realistically perturbed CKKS inputs: does it require an additional noise gap which is absent from the asymptotic complexity? Define a falsifier from original text before any further experiment. Do not revisit H count or broad sweeps.
STATE_UPDATE: NO — parked RIG-HE STATE.md remains unchanged.
