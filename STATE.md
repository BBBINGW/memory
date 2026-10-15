# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-27. **NEXT ITERATION:** CGS-28 (not started).
**STATUS:** HUMAN_REVIEW; ORIGINAL standard-(M)LWE O(LDec) secret-conditioned Gaussian padding generator still OPEN. **PARK RECOMMENDED** for CGS-22–27 NGP fixed-covariance/structured-secret detour, not for the parent CGS target. No secure cost-competitive ThFHE without stored padding established.
**FULL WORKING HISTORY:** `findings/threshold-fhe-correlated-gaussian-sampling.md`.
**LATEST RESULT:** `findings/cgs-27-ngpair-mod2-image-smoothing-obstruction.md`: for ANY rank2 NG-pair `a,b` with dense coefficients ±1, `CC^T=2nI` in REAL covariance but `rank_F2(C mod2)=1` for `C=[mat(a)|mat(b)]`. Thus the unflooded integer convolution `a r_1+b r_2` always has ALL coefficient parities equal; output lattice index at least `2^(n−1)`; uniform-F2^n parity predicate gives advantage `1−2^(1−n)`. Full-lattice *discrete* Gaussian smoothing cannot be inferred from Gram isotropy alone. **CRITICAL CAVEAT:** Original Lemma7.1 includes independent flooding E; our unflooded parity distinguisher DOES NOT attack original source, because E can smooth the sublattice. Generic algebraic norm/spectral lower certificate for NG components at n32768 is only `2^(−262136)`, too weak for a practical claimed bound; not a proof of actual small spectrum. Recursive NG keys still have no standard-MLWE hardness theorem, quantitatively useful per-key smoothing guarantee, evaluation-key security, simulator or competitive cost. Earlier CGS25 n32768 ~129-bit is merely keyspace entropy, not security.
**NEXT_ACTION (upon PI's "继续"):** CGS-28, return to original source's native standard (Module-)LWE key distribution, maintaining original low-online-communication, corrupted-party/adversarial-oracle transcript and server assumptions. Choose one concrete novel external-secret-linked reusable correlation / conditional-Gaussian mechanism (or a genuinely source-compatible alternative) and run one cheapest adversarial simulation or cost falsifier. Avoid repeating generic PRSS/PCF direct ports and known MPC-rounding results CGS10–21. If no real candidate, report HUMAN_REVIEW rather than indefinitely generating negative folklore lemmas. Preserve CGS22–27 as PARKed evidence until a credible standard-MLWE-security + spectrum + full-protocol path appears.
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
