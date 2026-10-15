# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-31. **NEXT ITERATION:** CGS-32 (not started).
**STATUS:** HUMAN_REVIEW. Parent Okada–Takagi 2025/409 standard-(M)LWE secret-conditioned Gaussian O(LDec) pad-prestorage problem OPEN. The CGS22–27 structured-secret NGP branch is PARKed. **CGS28–31 unconditional fresh flooding-only / one common public statistical Gaussian branch is PARKed** after p-cancellation (CGS30) and an explicit centered-variance conditional Gaussian TV lower bound (CGS31). No complete provably secure small-q modification.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-31-centered-variance-public-simulator-gate.md`. Original ePrint2025/409 **Lemma5.1 Eq(14) p20–21**: unpadded latent noise e0 conditional on secret s is approximately half-lattice discrete Gaussian with width squared `p²σ0²||s||²+σ_flood²`; §7 **Lemma7.1 Eq25 p30** has multivariate width `p²σ0²Σ_s+σ_flood²I` and coefficient-marginal Gram diagonal `Σ||s_i||²`. Continuous Gaussian surrogate including public final σ1 has width² `V_s=F²+σ0²||s||²+σ1²`, `F=σ_flood/p`. For two secret norm squares differing Δ, relative variance gap `δ=σ0²Δ/V0`. Event `|X|≤√v0` has probability gap `erf(1/√2)−erf(1/√(2(1+δ)))≥c δ` for δ≤1, `c=exp(−1/4)/(√(2π)2^(3/2))≈0.10985`. Thus any ONE fixed public Gaussian target lies ≥cδ/2 TV from one of the secret-conditioned *continuous surrogate* distributions. With polynomial F and polynomial source norm differences, this is inverse-polynomial NOT negligible. Verified continuous toy at κ128 (gap ~1.73e−7 vs 2^-128), discrete half-lattice surrogate TV≈0.0508982. **IMPORTANT:** This is NOT a statistical bound on actual rounded/mod-q transcript and NOT a computational attack in source Algorithm5: unknown secret/norm and public-key correlation can matter; a dummy-norm computational simulator might be conceivable under a new joint knLWE/MLWE reduction.
**NEXT_ACTION (PI next “继续”):** CGS-32, test ONE concretely specified **computational** alternative: can a simulator choose a fresh DUMMY secret norm or covariance drawn from the legitimate source χ while decoupling it from public key and entire adaptive Algorithm5 transcript using existing known-norm LWE (scalar) or a nontrivial known-covariance MLWE reduction? Locate actual source assumptions and prove/falsify ONE smallest joint distinguishing game. Do not claim full scheme from merely sampling fake independent norm. If not source-compatible, PARK and focus on genuinely reusable hidden-output conditioned-Gaussian share primitive; avoid extending NGP or naive flooding.

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
