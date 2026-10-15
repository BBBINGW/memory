# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-32. **NEXT ITERATION:** CGS-33 (not started).
**STATUS:** HUMAN_REVIEW. Original Okada–Takagi ePrint2025/409 O(LDec) secret-conditioned Gaussian per-session pre-sharing from standard (Module-)LWE remains OPEN. CGS22–27 structured-secret NGP and CGS28–31 stronger independent flooding branches remain PARKed. CGS32 refutes dummy-covariance re-sampling independently per sid, but a PERSISTENT single dummy covariance still lacks needed public-key/evaluation-key joint computational reduction.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-32-dummy-covariance-multisession-joint-gate.md`. Source **Algorithm5 p23** adversary receives `(ctdec,{pdi}_act)` across adaptive decryption oracles under ONE KeyGen secret. Source **Lemma5.1 Eq14 pp20–21** / **Lemma7.1 Eq25 p30** conditional residual Gaussian depends on SAME secret norm/covariance across all sid. For event A and `p_M=Pr[Y∈A|M]`, two real sessions share M and satisfy `Pr[A1∧A2]=E[p_M²]`; independently resampled fake M'_sid gives `(E[p_M])²` with gap `Var_M(p_M)`, even while each one-session marginal is IDENTICAL. Exact n8 iid-bit, half-lattice Gaussian with width² `9+4M`, event |Y|≤2 test yields joint event 0.5613940170 vs fresh-per-session dummy 0.5582996108, gap 0.0030944063, numerical tail <3.87e−120. Sampling ONE fake M' at simulator initialization and reusing it EXACTLY matches residual-only Gaussian mixture joint distribution for all sessions, but NOT the public-key correlation. Needed native-MLWE computational hybrid `(PK(S),Σ_S)≈c(PK(S),Σ_{S'})`, s' independent, would follow from stronger known-covariance MLWE, which authors ePrint2025/409 §2.2 p8 explicitly say lacks a reduction from standard ring/MLWE; scalar knLWE has separate specialized prior reduction Micciancio–Suhl 2023/1728. Eval key/circular security further complicates. Estimating secret covariance from polynomial Gaussian-surrogate residual observations is mathematically possible under parameter bounds, but no source mod-q adaptive attack was demonstrated.
**NEXT_ACTION (PI next “继续”):** CGS-33: ONE real auxiliary-leakage MLWE reduction attempt or concrete counterexample for `(PK(S),Σ_S)≈(PK(S),Σ_{S'})`, contrasting scalar known-norm LWE prior theorem and ring covariance; test smallest dimension and exact original standard-MLWE assumptions. If no source-compatible proof route, PARK persistent dummy and return to genuine secret-dependent Gaussian threshold-shareable sampler. No fake finished ThFHE, no unproved novelty.
## Other research files — archives, not access-control partitions

The following research progress is preserved as historical knowledge and can be resumed **only when the PI requests a topic switch**. The older series names/numbers are retained solely for provenance; do not rename, re-number or erase existing work.

- **SHIP**: `findings/ship-memory-STATE.md`; SHIP-I226 last completed, memory-compression candidates and negative fingerprint result archived.
- **vFHE**: `findings/vfhe-cross-crt-state.md`; V43 last completed, author's October 2026 range-PIoP revision resolves the historical CRT counterexample.
- **General historical series**: `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md`, `findings/OPEN_RESEARCH_BRANCHES.md`; original global I1–I192 retained as history.
- **EXPLORE**: `findings/explore-STATE.md` is a dormant draft, not a required separate role, MCP instance or isolation policy.
- **Old isolation registry/spec**: `findings/RESEARCH_TRACK_INDEX.md`, `findings/TRACK_ISOLATION_POLICY.md`, `findings/MCP_TRACK_GUARD_CODEX_SPEC.md` are **historical/retired** and are not startup requirements.

## Simple workflow

1. Read `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`, then THIS `STATE.md` and the relevant topic findings/failures.
2. Work only on the current PI-selected subject. "继续" retains it; an explicit PI request can switch to another existing topic or initiate new research. Save a proper checkpoint and update THIS state when switching.
3. Store important paper evidence, derivations and falsified hypotheses in topical `findings/` and `failures/`; update topic progress AND `STATE.md` as appropriate. No requirement for track-prefix-only write authorization.
4. Follow read-before-write and verification. Current legacy GitHub Notes writer has no caller-supplied atomic expected_sha; do not run concurrent writers. Never claim a server-side write lock.
5. Human PI makes contribution/pivot decisions. Preserve source provenance and the constructive-synthesis lesson; do not automatically continue parked mechanisms.

## Preservation

The previous long root state is archived at `findings/legacy-global-STATE-before-track-isolation-2026-10-15.md`. All prior CGS, SHIP, vFHE, EXPLORE, and other findings/failures and commits remain intact. No local Codex branch/source code was modified by this GitHub note change.
