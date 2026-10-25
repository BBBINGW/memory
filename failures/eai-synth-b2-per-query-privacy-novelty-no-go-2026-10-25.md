# EAI-SYNTH B2 negative result: adaptive tail queries need not cost privacy per query

**2026-10-25 | TRACK_ID EAI | Active topic SYNTH-B2 | no GPU/Codex/model runs.**

## One killed claim

Under one frozen database with exactly one public atom from a fixed d-category universe per individual, a downstream analyst necessarily spends incremental differential-privacy budget each time it adaptively selects a new rare-category query. **FALSE.**

## Decisive standard construction and proof

Histogram replace-one L1 global sensitivity **2**. One-time `Y=h(D)+iid Lap(2/epsilon)` is pure central `epsilon`-DP, by joint density-ratio bound `exp(||h(D)-h(D')||_1/(2/epsilon)) <= e^epsilon`. Arbitrarily many adaptive follow-up queries whose answers are computed only from Y satisfy the **same epsilon-DP** by post-processing, not sequential composition. No per-query privacy cost.

For discoverable singleton counts in the public d-domain, with `epsilon=1,d=1000,alpha=beta=0.05`, threshold `t=2 ln(1000/(2*.05))=18.42068074395`. Union false positives for zero bins ≤alpha. A present bin with empirical c≥24 has FN probability ≤0.05 (actually at c24, ~0.030721); at c10 true detect probability is ~0.007420657955, so utility is *poor* for some rare modes, even though privacy reuse is perfect.

This example **does not** establish a universal utility bound for large/subgroup subset queries, unknown domains, changing private reference data or local DP; it is a cheap killer for the supposed per-query budget necessity. It does **not** establish a new positive research construction, lower bound on optimal privacy sample complexity, or guarantee preserving recursive model-training tails.

## Why nearby proposals are not new

- [Kaplan et al., COLT 2021](https://proceedings.mlr.press/v134/kaplan21a.html) Sparse Vector Technique Revisited already addresses unbounded adaptive threshold queries.
- [Chen et al., ICML 2025](https://arxiv.org/html/2502.08878) **MAD/MAD2R** addresses even unknown/unbounded item support and low-frequency private partition discovery under user-level DP; see §§3–6.
- [Braun et al. ePrint 2024/469](https://eprint.iacr.org/2024/469) covers malicious-secure sparse private histograms under its two-server trust model.
- [Asiaee–Aryan, UAI 2026](https://arxiv.org/html/2607.08122) already combines adaptive DP query workload and reusable synthetic release; [Qiao et al., ICML 2026](https://arxiv.org/html/2606.13732) Appendix C.6 explicitly contains private OT under their assumptions.

### STOP and next decision

**STATUS:** `FAIL_B2_GENERIC_ADAPTIVE_PER_QUERY_PRIVACY_CLAIM / PASS_CLASSIC_ONE_SHOT_DP_COUNTEREXAMPLE`.
**RESULT:** Finite-domain adaptive query novelty false, large/open domain has direct prior art; no new verified solution for rare semantic subgroup coverage under generator feedback.
**NOVELTY:** `NOT_ESTABLISHED`.
**NEXT_TEST:** none for per-query budget hypothesis. Optional, **only on PI continuation**, B3 source-first comparison of *changing* real-data reference and recursive feedback vs available continual DP synthetic-data release and private verification theory.
**NEXT_ACTION:** `PI_REVIEW_B2_PARK_AND_OPTIONAL_B3_CONTINUAL_REFERENCE_SOURCE_GATE`.
**STATE_UPDATE:** `YES` after GitHub commit/readback.
