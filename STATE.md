# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-30. **NEXT ITERATION:** CGS-31 (not started).
**STATUS:** HUMAN_REVIEW. Parent Okada–Takagi 2025/409 standard-(M)LWE O(LDec) secret-conditioned Gaussian prestorage problem OPEN. Structured-secret NGP covariance detour CGS22–27 PARKed. **CGS28–30 naive fresh-independent Server flooding-only pad-replacement branch PARK RECOMMENDED** under its existing worst-case translation-TV proof: cannot preserve source's polynomial-valued small q even by scaling p=Q/q. This is NOT a no-go for all smarter centered-distribution/flooding or correlated-sampler schemes.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-30-p-cancellation-flooding-modulus-gate.md`. Original paper Lemma7.1 p30 Eq27: `r_ij∼D_(c_ij+pZ,pσ0)`; hence `r/p∼D_(c/p+Z,σ0)`, so scaling p does NOT reduce normalized random-rounding scale. CGS28 sufficiency required `σ_flood≥2^(κ+2) n (kn B R_r+2 Beval+1/2)` to hide ALL random-rounding W by TV with n coordinates; tail cutoff `R_r=pσ0 t`. Thus `σ_flood/p≥2^(κ+2)kn²Bσ0t`, INDEPENDENT of p. Source Theorem7.4 p32 requires `q≥c√κ σ_flood/p`; source Table1 p3 targets polynomial-valued q, but this particular sufficient argument forces `q=2^Ω(κ)` for non-negligible source scales. EXACT CGS28 demonstration κ128,k2,n1024,B1,σ0=16,t16,Beval2^30, illustrative correctness multiplier12: at p=2^20,64,128,160 new q stays ~162.585 log2 (163-bit) while old flooding term decreases from ~141.585 to ~1.585 log2. Baseline full q has other costs. Microsoft SEAL reference BFV maximum Q N4096=109/N8192=218 bits is only an external security-budget cross-check, not source-compatible MLWE rank2/error/theorem instantiation; no estimator or complete FHE run performed. Source original error/secret distribution intact in conceptual candidate, but proof not completed.
**NEXT_ACTION (upon next PI “继续”):** CGS-31: choose ONE sharper hypothesis for source-original secret distribution: can a centered random `r^Ts` disturbance be hidden, **without revealing its secret-dependent covariance in Algorithm5's adaptive all-active-share transcript**, using a polynomial-valued q? Test minimum one-dimensional two-secret variance distinguishability vs any source-compatible public flooding distribution. If this also requires exponential q or simulator cannot be composed, prioritize a genuinely new secret-conditioned Gaussian share generator; avoid recycling naive flooding or NG identities. Preserve one-hypothesis/one-decisive-test and full original-paper provenance.
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
