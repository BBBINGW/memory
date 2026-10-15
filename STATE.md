# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-24. **NEXT ITERATION:** CGS-25 (not started).
**STATUS:** HUMAN_REVIEW / Okada–Takagi O(LDec) secret-conditioned Gaussian padding remains OPEN; no secure competitive replacement constructed.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-24-negaperiodic-golay-covariance-keyspace-gate.md`: In source-negacyclic ring `R=Z[X]/(X^n+1)`, the EXACT fixed-covariance `k=2` binary ±1 secret condition `Gram(a)+Gram(b)=2nI` is **negaperiodic** Golay pair, weaker than aperiodic Golay used in CGS23. Full exact n2,4,8,16 enumeration: ordinary counts 8,32,192,1536; NG counts 16,128,4096,557056. At n16 NG is 362.67× larger, with 425984 NG pairs retaining both individual numerical singular value thresholds `>=1`. These are known combinatorial sequences (Balonin–Đoković 2015; Egan 2017), **not** a new secure FHE primitive. For dense ±1 secrets at n divisible4, `NAF_s(1)≡2 mod4` proves **any odd k, in particular k3, cannot have exact constant Gram sidelobe cancellation**. At n16 whole NGP support has only 19.09 bits; none of this proves high min-entropy or LWE/MLWE hardness at n1024.
**NEXT_ACTION (when PI says "继续"):** CGS-25: find ONE explicitly and efficiently samplable high-entropy NGP family at cryptographic n≈1024, with a provable `H∞≥128` lower bound and usable individual `σ_min` bounds; test cheapest public-sample key-enumeration attack or source-MLWE secret-distribution obstruction. If no defensible high-entropy, source-security-compatible candidate exists, PARK covariance detour and concentrate on original conditioned-Gaussian setup challenge. Keep source original key distribution, adaptive transcript and end-to-end cost obligations explicit.

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
