# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-23. **NEXT ITERATION:** CGS-24 (not started).
**STATUS:** HUMAN_REVIEW / original O(LDec) secret-conditioned Gaussian problem OPEN; no complete secure and competitive scheme.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-23-golay-fixed-covariance-low-entropy-gate.md`: standard Davis–Jedwab binary Golay-pair secret family gives native `k=2` Gram covariance exactly `2nI`, solving the formal fixed-covariance/rank goal of CGS-22. However its publicly enumerable support is `m!2^(m+2)` for `n=2^m`: just 33.791 bits at n1024, 52.343 bits at n16384. A native independent-uniform-module public sample with n8 q257 and bounded ±1 error gave unique correct key after enumerating all 192 possibilities in 100/100 toy trials; for a family of size M, public residual-check distinguishing advantage against uniform is at least `1−M((2B+1)/q)^n` under bounded noise. This rejects the **named GDJ family as a practical 128-bit key choice**, not ALL Golay/constant-Gram secret families nor formal MLWE security of another distribution. PREVIOUS: CGS-22 signed-monomial rank n lift.
**NEXT_ACTION (when PI says "继续"):** CGS-24: one explicit larger-support `k≤3` complementary secret family, assess its actual entropy / known constructions and a credible original-MLWE/individual-nonsingularity/noise/cost interface with ONE decisive test. If no promising high-entropy constant-rank mechanism, PARK the covariance-flattening detour and return to PI review of the original conditional Gaussian O(LDec) problem. Do not claim source FHE/evaluation-key security or novelty from covariance identities.

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
