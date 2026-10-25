# EAI-SYNTH B2 — Adaptive tail discovery: known-domain DP histogram falsification gate

- Date: 2026-10-25 (Asia/Singapore).
- Track: EAI / SYNTH-B2, following user-authorized B1. **Not EAI-SYS S55, not FHE**; no remote GPU, Codex, new model training.
- **STATUS:** `PASS_CLASSIC_DP_CONSTRUCTION / FAIL_GENERIC_ADAPTIVE_QUERY_NOVELTY / HUMAN_REVIEW`.
- **Provenance:** original full arXiv HTML inspected for Qiao ICML2026, Chen et al. ICML2025, Asiaee–Aryan UAI2026; Kaplan et al. COLT2021 PMLR abstract and Braun et al. ePrint2024/469 abstract as explicitly indicated; locally independent derivation for histogram construction.

## One primary hypothesis

Under **fixed public finite atom vocabulary** `[d]`, centralized item-level `(epsilon,0)`-DP with replace-one neighbors and a frozen real dataset distributed across silos, an adaptive analyst selecting rare category tests after seeing past results MUST interact with private data and consume an additional privacy allocation for each test in order to reliably detect supported bins.

**Falsifier:** exhibit one single `epsilon`-DP release that can be *postprocessed* into any later adaptive sequence of singleton membership/tail-frequency threshold queries without extra privacy, with a nontrivial simultaneous false-positive and false-negative accuracy bound for sufficiently populated bins. This is **not** a guarantee for arbitrary unbounded semantic groups, streaming fresh private data, silo-level DP, or arbitrary subset-size utility.

## Baseline and proof [DERIVED / textbook mechanism]

Dataset `D=(x_1,...,x_n)`, every user contributes exactly one atom from public `[d]`. Histogram `h(D)=(h_1,...,h_d)`. A replace-one neighbor moves one count `-1` and one `+1` (or none); `max_neighbors ||h(D)-h(D')||_1 = 2`.

Release ONCE `Y_i = h_i + Lap(b)` independently, `b=2/epsilon`. Joint density ratio bounded by `exp(||h(D)-h(D')||_1/b) <= exp(epsilon)`: pure central DP. Subsequent analyst-chosen sequences computed ONLY from Y are postprocessing: **arbitrary number of adaptive requests costs no further epsilon**. For known `d` categories and queries of subset unions, return sums of corresponding noisy counts; these may be highly inaccurate for broad subsets. For unknown or subsequently introduced features/categories, the release is not sufficient.

One simple **simultaneous singleton-tail discovery rule**: report bin i if `Y_i >= t`, with familywise false-positive target `alpha`. For any count-zero bin, `Pr[Y_i>=t]=0.5 exp(-t/b)` for `t>=0`. By union bound across at most d bins, require `t=b ln(d/(2 alpha))`, assuming `d >= 2alpha`. For fixed empirical true count `c>=t`, false negative `Pr[c+Lap(b) < t]=0.5 exp(-(c-t)/b)`. For per-active-bin miss probability ≤ `beta`, a sufficient condition is `c >= t + b ln(1/(2 beta))` when `beta<=0.5`.

**Concrete, independently recalculated from analytical Laplace tails (NOT real privacy experiment):** `epsilon=1,d=1000,alpha=beta=0.05,b=2`. Threshold `t=18.420680743952367`; count for advertised 95% per-present-bin detection needs `c>=23.02585092994046`, i.e. integer `c>=24`. At `c=10`, detection `0.007420657955128824` (~0.74%); at `c=24`, detection ~`0.969278938233359`. False positive *any zero bin* ≤ 5% for all d. If 1% rare class at **fixed empirical n=1000** gives c=10, this conservative simultaneous mechanism misses it with ~99.26% probability despite DP; c=100 could be easy when n=10000 but dataset sampling still affects realized count. All numbers conditional on empirical c; population support vs empirical count and downstream recursive generator preservation are DIFFERENT claims.

**Caveats:** This is a deliberately simple, often overconservative rule. Better adaptive/private partition selection may beat this benchmark. It is **not** a lower bound for arbitrary DP algorithms; the utility regime cannot be generalized to high-dimensional/free-text/open vocabulary from d=1000; all future queries must be functions of one fixed Y, not new private data or features. The union bound controls false-discovery of zero bins even under post-hoc selection of a zero bin from Y; it does NOT give a uniformly tight error bound for arbitrary adaptively selected large unions. For cross-silo raw data, assume a trusted central aggregator or a separate authorized secure aggregation; **no protocol for untrusted/malicious server was newly constructed**.

## Closest original prior art (do not rediscover)

1. **Kaplan, Mansour, Stemmer**, COLT2021, `The Sparse Vector Technique, Revisited`, proceedings https://proceedings.mlr.press/v134/kaplan21a.html . Already handles adaptively chosen threshold tests using DP budget driven by sparse positives, not merely the number of queries. PMLR abstract seen; full COLT proof not independently reconstructed.
2. **Chen, Cohen-Addad, Epasto, Zadimoghaddam**, ICML2025, `Scalable Private Partition Selection via Adaptive Weighting`, full https://arxiv.org/html/2502.08878 , §§1,3–6. Their **MAD/MAD2R** selects lesser-frequency items from a **potentially unbounded** category universe in user-level DP via adaptive degree weights. This is directly overlapping prior art for unknown rare-label discovery, stronger in scope than our public finite d histogram. Their user-level multi-item privacy differs from our central item-level single-record setting.
3. **Braun et al.**, ePrint2024/469, https://eprint.iacr.org/2024/469 , original abstract: malicious-secure **two noncolluding-server** sparse private histogram, input-linear costs and error scale `O(log(1/delta)/epsilon)` independent of universe size under its claimed assumptions. Original full paper/proof not read in this B2 gate. Cross-silo secure histogram is **already prior art**, not our construction.
4. **Asiaee and Aryan**, UAI2026, `Workload-Preserving Differentially Private Synthetic Data for Causal Inference via Maximum-Entropy Calibration`, full https://arxiv.org/html/2607.08122 , §§4.2–4.5, 6 and Appendix. **Causal-AIM** adaptively chooses query workload, releases DP moments once, supports later subgroup estimation without more privacy budget; task-specific fidelity and uncertainty propagation already explicit. It is not a proof of full rare-mode guarantee in our desired setting, but forbids novelty claims for reuse of a DP synthetic release.
5. **Qiao et al.**, ICML2026, full https://arxiv.org/html/2606.13732 , §§4.3–4.4 and App C.6. Their Wasserstein silo proxy and private OT uses **Gaussian randomized projected data**, not scalar moment summaries; §C.6 gives projected noise and `(epsilon,delta)` DP condition and reports epsilon1 gradient alignment. Does **not** demonstrate a universal all-rare-mode probability guarantee. Our simple histogram is NOT an attack on their method.

## Result and next research boundary

**[NEGATIVE]:** Generic “adaptive querying unknown tail classes must spend privacy per query / requires brand-new DP mechanism” is **false** in finite known d. Unbounded-domain private discovery also has strong direct existing solutions (MAD, sparse hist). No novel mechanism was developed and no actual synthetic model training was performed.

**[OPEN, conditional]:** Potentially meaningful future research may lie at the intersection of *private target-specific semantic verification, continuously changing source/generator distributions, rare modes and recursive collapse guarantees*, but 2024 continual synthetic-data release and 2026 causal-workload DP are strong pre-existing literature. Must first identify one exact source theorem/assumption mismatch and consequential nontrivial fix; do NOT call new because these keywords were combined.

**STATUS:** `PASS_EXACT_KNOWN_DOMAIN_DP_BASELINE / FAIL_B2_GENERIC_ADAPTIVE_PRIVACY_NOVELTY / HUMAN_REVIEW`.
**RESULT:** One release answers arbitrary adaptive post-processing of a fixed public-domain histogram under a single epsilon; rare-count threshold bound quantified; no new tail-preserving synthetic data theorem or algorithm.
**NEXT_TEST:** `B3_SOURCE_FIRST_DYNAMIC_REFERENCE_VS_REUSE_STALENESS_GATE` **only upon user continuation** — compare Qiao's fixed DP OT proxy and its convergence assumptions with established *continual release of DP synthetic data*, and determine whether any important online-changing-distribution setting has a source-backed, unaddressed error/communication bound before new protocol ideas. If fully covered or impossible, park synthetic subline.
**NEXT_ACTION:** `PI_REVIEW_B2_NEGATIVE_AND_OPTIONALLY_CONTINUE_B3_DYNAMIC_REFERENCE_AUDIT` (no automatic Codex/GPU).
**STATE_UPDATE:** `YES` after GitHub write plus readback.
