# Resume EAI Synthetic-Data Research — Post B2 Handoff (2026-10-25)

## Authority / research identity

- User = human **PI** (topic selection, contribution judgment, pivots and final scientific decisions). Assistant = critical research student.
- Current **TRACK_ID=EAI**, current AI **ACTIVE_TOPIC=SYNTHETIC_DATA / EAI-SYNTH**.
- **LATEST_COMPLETED=SYNTH-B2** (B1 and B2 are bounded source-first falsification gates).
- **NEXT_CANDIDATE=SYNTH-B3_SOURCE_FIRST**, **B3_NOT_STARTED**. These screening labels must not be confused with EAI-SYS `SCOUT-S54` / `S55_NOT_STARTED` or EAI-P EAI-010 / EAI-SEC, or any FHE/BOOT/SHIP/CGS/VFHE counter.
- Current authority comes from most recent PI-selected topic and the **latest overriding tail section** of root `STATE.md`; historically retired `findings/TRACK_ISOLATION_POLICY.md` and `findings/RESEARCH_TRACK_INDEX.md` must not overwrite later single-current-target policy. Preserve previous research findings and notes.
- No autonomous/background continuation, GPU/Codex/remote server/model downloads/code changes/new experiments or repository mutations beyond an explicitly requested current read-only research task/its documentation. A plain PI “继续” in the new chat permits a **single cheapest B3 source/derivation gate**; not a GPU/ML-training test or an arbitrary new project.

## Required restore order (read BEFORE proposing research)

1. `RESEARCH_PHILOSOPHY.md`
2. `AGENT.md`
3. `START_RESEARCH_SESSION.md`
4. ROOT `STATE.md` (**read its latest override near the end**, not obsolete opening section)
5. `findings/eai-ai-three-directions-strategic-screen-2026-10-25.md` (AI domains and scope)
6. `findings/eai-synth-b1-source-mechanism-and-moment-boundary-2026-10-25.md`
7. `failures/eai-synth-b1-moment-tail-coverage-no-go-2026-10-25.md`
8. `findings/eai-synth-b2-known-domain-adaptive-tail-privacy-gate-2026-10-25.md`
9. `failures/eai-synth-b2-per-query-privacy-novelty-no-go-2026-10-25.md`
10. THIS handoff. Related EAI Agent A1 negative note, EAI-P/EAI010 independent raw audit, EAI-SYS EAGLE3 result are historical context; do **not** inherit their NEXT_ACTION.

## Research philosophy

`smallest falsifiable claim → cheapest decisive test → progressive verification → expand only if warranted`.
One **primary technical hypothesis** and ONE decisive minimal test each round. Original source/version/section/equation/page or commit. Separate `[FACT]`, `[DERIVATION]`, `[HYPOTHESIS]`, `[NEGATIVE]`, `[UNCLEAR]`. Before spending resources, establish *exact closest prior art*, its assumptions and why a concrete nontrivial change would be needed; distinguish classic textbook counterexamples from novel theory. Preserve failed candidates. Stop repeated toy sweeps and known methods. Before every GitHub write: read-before-write, make one coherent commit and re-read; old notes remain immutable. End with `STATUS/RESULT/NEXT_TEST(or NEXT_ACTION)/STATE_UPDATE`.

## B1 — completed; what was actually falsified

**H-B1:** for a public fixed 4-category domain `{0,1,2,3}`, releasing only `(sumP,E[X],E[X²])` suffices to certify whether tail category `x=3` has positive mass. **FALSE.**

Exact `P_A=(.70,.20,.09,.01)`, `P_B=(.71,.17,.12,0)`; same normalization, mean `0.41`, second raw moment `0.65`, variance `0.4819`; one has 1% tail, other zero. Signed shift `(+.01,-.03,+.03,-.01)` annihilates polynomials degrees 0,1,2. Deterministic verifier with only these summaries errs in one world; a randomized worst-case binary error ≥1/2. **Classical finite-moment nonidentifiability**, no novel theorem or attack on real synthetic models.

**Do NOT overclaim:** Qiao et al. ICML2026 (arXiv **2606.13732**, original §4.3–4.4, Appendix C.6) already use **Wasserstein interpolation/barycenter private distribution proxies**, including a DP OT adaptation; not merely first and second moments. `W1(P_A,P_B)=0.04`, so richer proxy can distinguish toy worlds. Yi et al. ICLR2026 (**2510.16657**) study fallible verifier and long-term collapse; FedUSD ICML2026 studies federated principal/residual representation and variance matching. Simple multi-silo combination, low-order moments, OT barycenter and generic verifier are **not novel**. No native training evidence.

## B2 — completed; what was actually falsified

**H-B2:** On a **fixed dataset** of individuals, each with exactly one atom of a **known finite public d-domain**, ANY adaptive sequence of private rare-category queries necessarily requires fresh DP budget per query. **FALSE**.

Under **replace-one neighboring database** and centralized item-level DP, histogram `h(D)` has `L1` sensitivity `2`; release once `Y_i=h_i+Lap(2/epsilon)` iid, satisfying pure `epsilon`-DP. An adaptive sequence answering queries by post-processing the fixed Y costs **no additional epsilon**. This **does NOT** automatically cover newly accessed private data, changing query features, unknown/unbounded domain, silo-level DP, private original labels, arbitrary high-dimensional unions or high utility in extremely sparse bins.

Quantitative simple discovery gate: `epsilon=1,d=1000,alpha=beta=.05`. Uniform singleton threshold `t=2 ln(d/(2alpha))=18.420680744` gives familywise chance of at least one false positive among true empty bins ≤5%. To bound **per-present-bin** miss chance by 5%, require empirical `c >=24`; `c=10` detection probability only `0.007420657955` (0.7421%). These are exact Laplace-tail arithmetic for THIS conservative algorithm, **not a lower bound** for all private algorithms or guarantee of generator tail preservation. Population tail probability vs observed empirical count are distinct.

**Prior art:** Sparse Vector Technique (Kaplan–Mansour–Stemmer, COLT2021, `https://proceedings.mlr.press/v134/kaplan21a.html`); private unbounded-domain low-frequency partition selection **MAD/MAD2R** (Chen et al., ICML2025, `https://arxiv.org/html/2502.08878`, §§3–6); malicious-secure two-server sparse histogram (Braun et al., ePrint2024/469 `https://eprint.iacr.org/2024/469`); adaptive DP causal synthetic data **Causal-AIM** (Asiaee–Aryan, UAI2026 `https://arxiv.org/html/2607.08122`); Qiao Appendix C.6's DP optimal transport. The last two and MAD were inspected beyond abstracts; original complete theorem/proof of Braun/Kaplan not independently read, do not overstate. No new adaptive/private tail discovery primitive was produced. B2's broad novelty claim is **PARK**.

## B3 — next minimal research gate (NOT YET STARTED)

**Research question, not a claim of gap:** In *repeated synthetic generation/retraining with changing real reference distribution* `P_t`, does Qiao-style private multi-silo Wasserstein proxy/selection have a source-level unmet **staleness/accuracy/privacy-cost** condition beyond existing **continual release of DP synthetic data** and workload-preserving DP? Prior published continual synthesis is known, so asserting “changing private data + DP” is new would be false.

**Candidate single falsifiable B3 claim to select/REFINE from sources, not pre-approve as true:** For a specified bounded time horizon, public query class, silo trust model and change budget, naive fixed `epsilon`-DP `t=0` reference proxy or textbook continual-release baseline cannot simultaneously maintain a verifiable *rare-mode coverage guarantee* and original Qiao-type Wasserstein selection bound at affordable privacy/communication budget; a new nontrivial technical interface may be needed. **Do not assume the obstruction**. If existing continual DP releases solve it under the same assumptions and task requirements, `FAIL_PRIOR_ART`; if observable transcripts are provably insufficient, `FAIL_UNACHIEVABLE`; if input semantics are missing, `SOURCE_BLOCKED`.

**ONE cheapest next test; READ-ONLY / no Codex/GPU:**
1. Obtain/read exact **original full text** of the 2024 paper `Continual Release of Differentially Private Synthetic Data from Longitudinal Data Collections` (verify actual bibliographic metadata/version rather than guess), Qiao 2606.13732 §§3–4 and App C.6, Asiaee–Aryan 2607.08122; additionally search 2025–Oct 2026 closest evolving-reference/continual DP synthetic-data prior art.
2. Create a **source-anchored assumption/interface table** with `P_t` and query/generator feedback semantics, centralized vs local/user-level DP, `(epsilon,delta)` accounting vs horizon, change regularity/drift, output object (private synthetic dataset vs OT reference proxy vs selected examples), error/convergence guarantees, communication and computation.
3. Pick ONE precise interface mismatch that appears not already addressed. Perform *cheapest decisive derivation/counterexample* using a two-time or two-population distribution. Do not merely show fixed proxies become stale (trivial). Need quantitative meaningful effect that survives strongest matching prior art.
4. If it fails, archive B3 in `failures/eai-synth-...` and recommend park/pivot rather than repeating B1/B2; otherwise give one next needed proof/verification, **not a broad new system plan**.

No unauthorized external server writes, Codex, model downloads, training or GPU activity. Public scholarly source reading and local math checks are authorized when user says `继续`.

## Status / provenance / handoff

**STATUS:** `B1_FAIL_MOMENT_SUFFICIENCY / B2_FAIL_GENERIC_DP_ADAPTIVITY_NOVELTY / B3_NOT_STARTED`.
**RESULT:** Two precise, source-delimited negative gates; synthesis-generation long-term quality/privacy objective remains OPEN with NO verified original method/guarantee or publishable contribution yet.
**NEXT_TEST:** `B3_SOURCE_FIRST_CONTINUAL_REFERENCE_PRIVATE_SYNTHETIC_GAP_FALSIFIER`.
**NEXT_ACTION:** `READ_2024_CONTINUAL_SYNTHETIC_ORIGINAL_COMPARE_QIAO_DPOT_CAUSAL_AIM_CHOOSE_ONE_2TIME_FALSIFIER`.
**STATE_UPDATE:** `YES` only after this handoff and root STATE pointer have been written and reread. 
