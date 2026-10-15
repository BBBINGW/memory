# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-22. **NEXT ITERATION:** CGS-23 (not started).
**STATUS:** HUMAN_REVIEW / original secret-conditioned Gaussian and O(LDec) preprocessing problem OPEN; no complete secure efficient replacement.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-22-signed-monomial-public-covariance-security-interface.md`: for binary negacyclic RLWE secret s(X)=Σs_jX^j, lifted n-component secret S_j=(2s_j−1)X^j has publicly fixed Gram covariance nI, every component signed-permutation invertible. However the direct ciphertext-preserving lift A'_j=a/2 has all coordinates equal and is publicly distinguishable from *standard independent-uniform MLWE* public vectors with advantage 1−q^{-n(n−1)}. This does NOT show structured RLWE is insecure or yield end-to-end FHE; rank inflates 1→n. One exact n4 q17 toy verified all 16 secrets and 1000 ciphertext identities. PRIOR: CGS-21 DPRF local nonlinear Shamir obstruction, CGS-20 scalar-linear PRF distinguisher.
**NEXT_ACTION (when PI says "继续"):** CGS-23: test ONE concrete small-constant-module-rank k=O(1) fixed-public-covariance secret family, checking whether its keyspace retains enough entropy and credible standard MLWE hardness. Consult complementary-sequence/Golay prior art and try ONE minimum case. If it cannot avoid entropy/security/overhead pitfalls, PARK covariance-detour, retaining parent CGS's O(LDec) open problem. Do not claim any new ThFHE before proof of KeyGen/Enc/Eval/security/rounding/noise and competitive costs.

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
