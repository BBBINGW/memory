# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-29. **NEXT ITERATION:** CGS-30 (not started).
**STATUS:** HUMAN_REVIEW. Original Okada–Takagi standard-LWE/MLWE O(LDec) secret-conditioned Gaussian prestorage problem OPEN. The CGS-22–27 structured-NGP key branch remains PARKed. Stronger fresh-Server-flooding-only tradeoff CGS28 is CONDITIONAL, without end-to-end security; the illustrative n1024,k2 128-bit implementation inference was REJECTED in CGS29.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-29-modulus-security-screen.md`. Original ePrint2025/409 **Algorithm2 p17** leaves actual underlying mFHE parameters unspecified; **Lemma7.1 p30** requires σflood=Ω(2^κ Beval); **Thm7.4 p32** q=σdec Ω(√κ) with σdec including σflood/p, and Q=pq, so `Q=Ω(2^κ √κ Beval)` already before stronger no-pad flooding. Compare external Bossuat et al. ePrint2024/463 **Table5.2** reference *ternary-secret, Gaussian-error std3.19 classical category-128* maximum log2 Q of 53 for **effective LWE dimension kn=2048** (rank2 ring n1024), 106 at kn4096, 214 at kn8192, 430 at kn16384. CGS28's explicit DEMONSTRATION (κ128 n1024 k2 B1 p2^20 σ0=16 rounding cutoff2^28 Beval2^30 and illustrative q-normalization ceil√128=12) gives original σflood LOWER-TERM log2Q≈161.585, no-pad stronger flood log2Q≈182.591, +21.006 bits. Both FAR outside that 128-bit *reference-class* guideline; **NOT** a formal attack on arbitrary source χ/error nor evidence of fully source-compatible parameters. Holding toy parameters fixed at ring n4096 k2 gives Q≈186.586 vs reference cap214, merely NOT EXCLUDED; actual source smoothing, χ, Beval, q/Q and FHE KeyGen/Eval are UNVERIFIED. Published OpenFHE CKKS flooding uses tighter but DIFFERENT security model, not drop-in.
**NEXT_ACTION (next PI “继续”):** CGS-30: choose ONE genuinely fully specified ring/MLWE FHE underlying parameter family, preferably k2 n≥4096, with χ, eval-noise bound, σ0, rounding tails, p,q,Q and proper evaluation-key/circular-security assumptions. Run ONE cheapest source-smoothing + LWE/MLWE concrete 128-bit estimator/communication feasibility falsifier for stronger-flood no-pad; or derive a rigorously source-compatible tighter bound that directly changes feasibility. Since original paper leaves base FHE abstract, DO NOT invent secure parameters or infer security from guideline screening alone. If not viable, PARK flooding-only branch; parent original correlated-Gaussian open question remains.
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
