# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-33. **NEXT ITERATION:** CGS-34 (not started).
**STATUS:** HUMAN_REVIEW. Original standard LWE/MLWE Okada–Takagi ePrint2025/409 secret-conditioned Gaussian O(LDec) persistent pad storage OPEN. Structured-secret NGP CGS22–27 PARKed. Independent flooding CGS28–31 PARKed. CGS32–33 persistent dummy-covariance/no-extra-known-covariance-assumption line PARK RECOMMENDED after conditional multi-session mismatch and native unit-rerandomization obstruction; no universal computational impossibility proved.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-33-ring-unit-covariance-rerandomization-gate.md`: attempted standard MLWE public-key self-randomization `(A,b=As+e)→(Au^-1,b,us)`. For full **uniform iid ternary** secret coefficient law χ={−1,0,1}, every invertible **integer coefficient-linear ring multiplication** preserving χ^n exactly must be a signed monomial u=±X^j. Proof: bijective ternary cube support forces all integer rows have ℓ1≤1, so signed-permutation matrix, first column vec(u)=±e_j. Every allowed transform satisfies `Gram(us)=Gram(s)` EXACTLY. Module rank k analogue: exactly ternary-cube-preserving GL_k(R) maps only permute secret components and apply signed monomials; sum `Σ_s=Σ_i Gram(s_i)` invariant. Hence this exact native uniform-A/self-reduction class CANNOT randomize Σ or simulate persistent independent dummy. Toy n2 4/9 and n4 8/81 coefficient support preserving bijections, all Gram-invariant; n4 q257 public-key equation + k2 module check PASS. THIS DOES NOT rule out other χ, non-linear key changes, augmented computational RLWE/MLWE reductions, or attack original ThFHE.
**SOURCE PRIOR-ART DETAIL:** Micciancio–Suhl ePrint2023/1728 FULL PDF original read §3.2 Lemma9 p10: scalar known-norm variant leaks `||s||²+||e||²`, search reduction guesses polynomial-range statistic and needs specialized decision search-to-decision. §5.3.2 Definition12 p16 separate known-covariance RLWE includes `ss^*+Σ e_i e_i^*`, not identical to source secret-only Σ; reduction from standard RLWE explicitly left open. Okada–Takagi 2025/409 §2.2 p8 concurs. Earlier author 2024/239 withdrawn on 2025-03-04 (historical only).
**NEXT_ACTION (PI next “继续”):** CGS-34 must return to ORIGINAL source secret distribution and O(LDec) session Gaussian problem. Pick ONE actual on-demand secret-conditioned Gaussian threshold-share mechanism, perhaps a new *server-assisted* dealer that uses existing semi-honest noncolluding Server without revealing secret covariance or expanding rounds. Specify precise input/output, setup/online interaction, adversary-visible shares and simulator; run ONE decisive leakage/qualified-set/communication cost falsifier. If no concrete mechanism, report HUMAN_REVIEW instead of repetitive no-go lemmas. Keep one primary hypothesis+one decisive test and read actual source full paper first.
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
