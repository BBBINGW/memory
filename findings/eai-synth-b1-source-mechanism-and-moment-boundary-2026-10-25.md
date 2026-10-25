# EAI Synthetic Data — B1 source-mechanism and observable-statistics boundary (2026-10-25)

**Research track:** EAI, AI-direction synthetic-data screening `SYNTH-B1`; first explicitly PI-authorized finite-support minimal gate after Agent A1. **Not** EAI-SYS S55, EAI-P, any FHE iteration or model/GPU experiment. One primary hypothesis + one cheapest decisive test. User PI makes strategic choices.

## Source and mechanism anchors — original text not abstract-only

**[FACT] Qiao et al.** `When Sample Selection Bias Precipitates Model Collapse`, ICML2026, arXiv:2606.13732 **v2 dated July 2, 2026**, [full HTML](https://arxiv.org/html/2606.13732). §§2–3: Accumulate-Subsample, bounded top-alpha selection, `Theorem 1` local-biased reference leads to variance collapse and mean drift; `Theorem 2` rate; `Theorem 3` (§3.3) gives downstream risk bound that depends on Wasserstein discrepancy under Assumption 2. §4.1 OT sensitivity based on dual potentials, §4.3 **Scheme I** multi-silo geodesic interpolations and selection (eq22-24, concave submodular objective with greedy 1−1/e), §4.4 **Scheme II** distributed Wasserstein barycenter proxy (eq25, Theorem5), not simply releasing means/variances. Critically Appendix **§C.6** explicitly integrates *differentially private optimal transport* via sanitized random projections/noisy distance matrices and reports tests for ε=1; cannot claim private OT is absent. Authors' method also lacks a universal certified exact rare-support recovery theorem. This is a boundary, not a criticism of claimed guarantees. Anchor https://arxiv.org/html/2606.13732 .

**[FACT] Yi et al.**, `Escaping Model Collapse via Synthetic Data Verification: Near-term Improvements and Long-term Convergence`, ICLR2026, arXiv:2510.16657, [original full HTML](https://arxiv.org/html/2510.16657): §§2–4 binary-feedback imperfect verifier, verifier `knowledge center`, Theorems 3.1 and 4.1 short-run vs long-run; verifier bias can cause late plateau/reversal. This already motivates verified synthetic curation and bias-aware analysis, not new.

**[FACT] Xie et al.**, `FedUSD: Unbiased Synthetic Data for Federated Learning`, ICML2026, [PMLR full landing](https://proceedings.mlr.press/v306/xie26l.html): HOB principal representation and residual variance matching in federation. Only landing/abstract checked in this gate; the HOB-specific theorem/full proof was not inspected. Do NOT equate FedUSD to releasing only two scalar moments.

**[FACT] Earlier verification**, Feng et al. ICLR2025 `Beyond Model Collapse: Scaling Up with Synthesized Data Requires Verification`, [paper](https://proceedings.iclr.cc/paper_files/paper/2025/hash/df2d62b96a4003203450cf89cd338bb7-Abstract-Conference.html), already models verification against collapse. Generic verifiers and dataset-filtering are not novel.

## What our B1 test actually assumes

**H-B1 (falsified):** For an *unknown* finite-support real-data reference `P` on a publicly known 4-category domain `{0,1,2,3}`, revealing only **exact normalized count, mean E[X], and second raw moment E[X²]** across silos is sufficient for any downstream verifier to always correctly decide whether real tail category `x=3` has positive probability. Public candidate synthetic pool, selected samples, local scoring rules and verifier randomness can be fixed identically between worlds. Every silo may return the same aggregate sufficient-statistic triplet; no OT geodesic/score vectors/other data-dependent transcript is available.

**Cheapest decisive test:** one exact rational four-support paired distribution with identical first two moments but differing tail presence, verifying identities arithmetically. See `failures/eai-synth-b1-moment-tail-coverage-no-go-2026-10-25.md`.

A generic probability-law statement: A statistic T can guarantee a predicate `g(P)` uniformly over admitted class `C` only if g is constant on each fiber `{P in C:T(P)=t}`. Here it is NOT constant. This is classical finite moment identifiability, **not a new theorem**.

## What survived and what did not

**RESULT:** `FAIL_MOMENT_ONLY_EXACT_TAIL_IDENTIFIABILITY`. It does not falsify Qiao's §4 Wasserstein proxy approach: their messages can encode more than low-order moments and the two worlds have positive Wasserstein distance. It does not establish the impossibility of DP count queries, secure aggregation, higher-order moments, group-aware verifier, or other richer protocols. Neither scalar two-moment synthetic curation nor 'multi-silo' is a publishable construction.

**Potential future scientifically useful boundary (not yet a hypothesis that passed novelty):** Adaptive tail/group queries and limited privacy/communication budget can create an identifiable-vs-private/expensive information frontier, but DP histograms, secure aggregation, private OT and heavy-tail learning all have extensive prior art. Source-first identify a *concrete* application/query class, estimator mechanism, exact privacy model and nontrivial impossibility/achievability gap **beyond existing mechanisms**. Never present an ordinary DP Laplace rare-count threshold as new.

**STATUS:** `PASS_ORIGINAL_SOURCE_METHOD_AUDIT / FAIL_B1_MOMENT_SUFFICIENCY / NOVELTY_NOT_ESTABLISHED / HUMAN_REVIEW`.
**RESULT:** First two moments are insufficient to certify tail-presence even with exact noiseless disclosure; Wasserstein multi-silo proxies/DPOT in prior work are richer mechanisms already studied.
**NEXT_TEST:** One **literature-first** comparison of adaptive subgroup/rare-mode DP certified coverage, Qiao §C.6 privacy+tail assumptions, and existing private histogram/coverage confidence bounds. Test whether ANY nontrivial source-compatible gap remains under a precisely stated extra query interface. No model training/Codex.
**NEXT_ACTION:** `B2_PRIORART_FIRST_ADAPTIVE_DP_TAIL_COVERAGE_INTERFACE_GATE` only if PI chooses to continue synthetic-data track.
**STATE_UPDATE:** `YES` after git commit and reread.
