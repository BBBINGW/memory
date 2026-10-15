# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-28. **NEXT ITERATION:** CGS-29 (not started).
**STATUS:** HUMAN_REVIEW. Standard-LWE/MLWE source original O(LDec) Gaussian pad sharing remains an OPEN problem for provably secure, competitive parameters; NG structured-secret covariance detour CGS22–27 PARKed. CGS28 identifies a **CONDITIONAL no-prestored-pad server-flooding tradeoff** with an exact statistical lemma but no complete ThFHE proof or practical security claims.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-28-flooding-no-padding-gate.md`. Source 2025/409 **Algorithm3 p19 and Lemma5.1 pp20–21** already draw independent fresh Server flooding `E←D_(1/2 Z,σ_flood)`; its secret-dependent pre-flood disturbance W includes r^T s and bounded evaluated/fresh ciphertext noises. For E fresh independent of W and any prior context, Gaussian lattice translation TV `TV(E+τ,E)≤|τ|/σ_flood` yields `TV((W,E+W),(W,E))≤δ+M/σ_flood` if `Pr(|W|>M)≤δ`; in n ring coefficients ≤δ+nM/σ_flood. Source-shaped M scalar = nB R_r+2Beval+1/2; rank-k MLWE = knB R_r+2Beval+1/2. Conservative sufficient stronger flooding `σ_flood ≥2^(κ+2) d M` with d=1 scalar or n module, plus source's other bounds; all proof assumes rigorous per-session randomized-rounding tail and privacy of internal server E. A verified half-integer discrete Gaussian example gives TV=0.0935228272467 below 3/32. Illustrative NOT-security-instantiated λ128,n1024,k2 case increases flood log2 by ≈10 bits scalar /21 bits MLWE, potentially also increasing q/Q. **NOT** a completed adaptive Theorem6.3/7.5 simulator, concrete LWE/MLWE hardness, evaluation-key proof, or efficiency comparison. Such flooding is prior art; fixed-norm Rademacher LWE is also prior art (Micciancio2018 and source §5).
**NEXT_ACTION (PI's next “继续”):** CGS-29: one decisive source-derived actual p,q,Q/smoothing/underlying FHE security and communication parameter gate on stronger-Server-flooding no-pad. If sufficient q/Q violates credible MLWE hardness/usable scheme parameters, PARK flooding-only route; otherwise attempt full adaptive Algorithm5 simulator composition, with complete fresh-E conditioning across sessions. Keep one hypothesis and one cheapest decisive test.
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
