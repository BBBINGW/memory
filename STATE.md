# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-26. **NEXT ITERATION:** CGS-27 (not started).
**STATUS:** HUMAN_REVIEW; original O(LDec) secret-conditioned Gaussian-padding problem OPEN. No unchanged-source/provably secure/economically competitive no-padding ThFHE constructed.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-26-fixed-covariance-does-not-erase-original-padding-gate.md`: source Okada–Takagi 2025/409 **Lemma7.1 Eqs(25)–(26), pp30–31** distinguish unpadded latent covariance `p²σ0²Σ_s+σflood²I` from padded public target `p²σ0²Bpub²I+σflood²I`. Previous CGS-25 recursive rank2 NGP candidate has `Σ_s=2nI`, but the unchanged original theorem's sufficient parameter requires `Bpub²>1+kn²Bmlwe²`. At n32768,k2,Bmlwe1, `Σ_s=65536I`, integer `Bpub=46341` yields `Σζ=(Bpub²−2n)I=2147422745I`, so **literal ζ=0 is NOT the original Eq26 target**. Numeric variance ratios are algebraic/normal-model illustrations, not a demonstrated source-transcript attack. Source `χmlwe` independent-key security and individual min-singular bounds are also absent for highly structured NGP keys. A reparameterized no-pad protocol might use source's **FIRST-STAGE Eq25** with public covariance, but requires independent FHE/MLWE hardness, simulator, noise and cost proofs. Prior CGS-25 recursion n1024 has only ~64.09 bits, n32768 ~129.09 bits **keyspace entropy only**.
**NEXT_ACTION (upon PI's "继续"):** CGS-27: one decisive source-first-stage Eq25 / *high-entropy n32768 recursive NGP* quantitative spectral and security-distribution gate. Seek a rigorously lower-bounded individual `σ_min` over a large-support key subfamily and a credible standard (M)LWE security route; if unavailable, PARK fixed-covariance secret-distribution branch and refocus on the original conditional Gaussian generator. Do not claim protocol-level Gaussian prestorage removal merely from public Σ_s.
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
