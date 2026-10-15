# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-25. **NEXT ITERATION:** CGS-26 (not started).
**STATUS:** HUMAN_REVIEW / original O(LDec) secret-conditioned Gaussian padding OPEN; no proof of cryptographically secure/economically competitive replacement.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-25-recursive-negaperiodic-key-entropy-gate.md`: explicit binary rank-2 negaperiodic Golay doubling `(a,b)→(a(X²)+X^(2t+1)b*(X²), b(X²)−X^(2t+1)a*(X²))` for `t=0,...,2n−1`. It preserves ±1 coefficients and exact public Gram `Σ=2nI` at every length, and its output is injective in prior pair+odd shift. Starting from all 557056 n16 base NGPs yields exact uniformly samplable support `17·2^60` at n1024 = **64.087 bits**, FAIL target Hinf128. Reaching n32768 yields `17·2^125` = **129.087 bits** of UNFILTERED key entropy, not a security proof. Exact all-lag NAF checked on chains through n1024; numerically sampled n32768 individual min singular values sometimes below 1 (4/30 cases), no certified spectral bound. This doubling has known combinatorial prior art (Balonin–Đoković arXiv1508.00640 §3). Original Okada–Takagi `χ_mlwe` key distribution, security, FHE Eval/evaluation keys, and low-cost requirements are not inherited; 2026/957 full PDF remains source-blocked.
**NEXT_ACTION (upon PI's "继续"):** CGS-26: one cheapest decisive **structural public-sample key-recovery or certified spectrum/noise test** for the n32768 high-support family; explicitly assess whether ≥128-bit min-entropy can coexist with individually usable source `σ_min` bound and credible standard (M)LWE hardness. If no viable security/spectral proof route, PARK fixed-covariance NG-key-distribution detour rather than extending elementary combinatorial identities. Keep original conditioned-Gaussian O(LDec) problem OPEN and prioritize grounded, nontrivial complete-protocol composition if switching back.

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
