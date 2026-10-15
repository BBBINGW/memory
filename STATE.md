# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-34. **NEXT ITERATION:** CGS-35 (not started).
**STATUS:** HUMAN_REVIEW. Original Okada–Takagi ePrint 2025/409 standard-(Module-)LWE secret-conditioned Gaussian O(LDec) preprocessing storage OPEN. CGS22–27 structured-secret NG; CGS28–31 flooding-only; CGS32–33 persistent dummy/known-covariance detours PARKed. CGS34 naive Server online *public* Gaussian pad-share delivery using the SAME original PartDec PRF mask is PROVABLY BROKEN with one-session RLWE full-key recovery for invertible public a. An alternative direct Server ciphertext b−ζ shifting mechanism passes aggregate algebra ONLY, and may need NEW trust/known-covariance MLWE assumption.
**FULL WORKING HISTORY:** findings/threshold-fhe-correlated-gaussian-sampling.md.
**LATEST RESULT:** findings/cgs-34-pad-transport-mask-collision-gate.md. Source Algo7 physical p29 PartDec_i=λ_i(a s_i+ζ_i)+m_i; Algo5 p23 adversarial ODec sees ALL active replies; original server broadcasts only processed ciphertext and never obtains replies under noncollusion. If a proposed new Server dealer publicly delivers per-recipient contribution d_i=λ_i ζ_i+m_i REUSING the same existing m_i=PRF(seed_i,sid), then observable difference PartDec_i−d_i=λ_i a s_i, and sum over active set yields a s. For R_q=F_17[X]/(X^4+1), N3 T2 act(1,2), λ=(2,−1), a=1+X invertible, s=1−X²+X³, deterministic exact toy recovers entire s from ONE session without any honest seeds/shares. The original paper has no such d_i broadcast, so NO original-scheme attack. Independent domain-separated transport masks avert literal cancellation but cost O(|act|) new online ring elements, breaking O(1) broadcast in N. If Server instead subtracts freshly generated ζ directly from processed ciphertext second coordinate and parties use pad-free PartDec, recovered aggregate residual matches source padded scheme exactly with no extra online messages. BUT Server must learn secret-conditioned covariance Σ_s, whereas source §5 p25 privacy against untrusted semi-honest Server relies on original FHE semantic security without this auxiliary leakage; setting up Server with Σ_s is a model/assumption change potentially requiring known-covariance MLWE. No complete simulation or ciphertext privacy established.
**NEXT_ACTION (upon PI next “继续”):** CGS-35 test ONE concrete security and trust leakage gate for Server-direct b−ζ variant: can source trusted KeyGen supply Σ_s privately to Server while still proving Server-side plaintext confidentiality from ORIGINAL standard MLWE? Formalize (pk,evk,Σ_s,Enc(pk,m)) leakage, compare known-covariance MLWE and smaller secret leakage, run cheapest source-consistent two-message/ciphertext distinguishing test or reduction gate. If requires genuinely stronger auxiliary-info assumption, PARK dealer despite aggregate correctness and seek hidden conditional Gaussian sampling without giving Σ_s to Server. One hypothesis one falsifier, no repeated PRF bugs.

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
