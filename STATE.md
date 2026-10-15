# FHE Research State — Single Active Session

**Checkpoint:** 2026-10-15. **Operating mode:** ONE research conversation/task at a time, ONE existing GitHub Notes/Research MCP, NO enforced separate research-track identities, permissions, instances, OAuth scopes or dedicated endpoints. This supersedes the retired track isolation policy.

## Current PI-selected active research

**TARGET:** CGS — Okada–Takagi threshold-FHE secret-conditioned correlated Gaussian padding and the O(LDec) preprocessing/storage open problem.
**LATEST COMPLETED:** CGS-35. **NEXT ITERATION:** CGS-36 (not started).
**STATUS:** HUMAN_REVIEW. Parent Okada–Takagi ePrint2025/409 from standard (Module-)LWE with secret-conditioned per-sid Shamir Gaussian pads and O(LDec) pre-storage remains OPEN. CGS22–27 structured NG-covariance, CGS28–31 independent flooding, CGS32–33 dummy/known-covariance, and CGS34 reuse-PRF masked transport branches PARKed or broken. The CGS34 direct Server b−zeta alternative has correct aggregate algebra but changing Server secret-statistic visibility is a NEW auxiliary-leakage/trust assumption; CGS35 shows an opaque Server-LOCAL conditional sampler does NOT hide its covariance under polynomial raw-sample access. No plaintext/FHE key-recovery attack on original source is asserted.
**FULL WORKING HISTORY:** findings/threshold-fhe-correlated-gaussian-sampling.md.
**LATEST RESULT:** findings/cgs-35-server-sampler-covariance-fingerprinting-gate.md. Source Algorithm7 p29 zeta^(sid)~D_{Z^n, sigma0 sqrt(Bpub² I−Sigma_s)} depends on integer Sigma_s=sum_i Gram(s_i). Source §5 p25 distinguishes party-corruption simulation Def5.4 from separate confidentiality of semi-honest UNTRUSTED Server, which originally sees encrypted inputs and public materials but not Sigma_s. In the continuous analogue, true Gaussian covariance C_s=sigma0²(Bpub²I−Sigma_s)/(2π). A locally sampling Server that receives L independent raw zeta_t can estimate C_hat=(1/L)Σ zeta_t zeta_tᵀ and round Sigma_hat=Bpub²I−(2π/sigma0²)C_hat entrywise to recover integer Sigma_s; Wick + Chebyshev + n² union gives probability≥3/4 with L≥32 n² Bpub^4, amplified to overwhelming with O(κ+log n) independent blocks. For n,Bpub polynomial this is polynomial total samples. This proof is CONTINUOUS model, not a general theorem about all discrete conditioned Gaussians. Separately for ACTUAL scalar discrete lattice Gaussian, n_secret=2, secrets norms m1/2, Bpub=3,σ0=8: exact discrete second moments 81.48733 and 71.30141; Monte Carlo with 10k independent integer Gaussian outputs/trial recovers exact norm m in 100/100 trials for each m via rounded sample variance; truncation mass <4.22e−198. Script /mnt/data/cgs35_server_conditional_gaussian_covariance_leak.py SHA256 aeab5ac22269e464725a881080efd4ebc4782225aefb3f42d09a37c2b37d06a6; JSON SHA256 ec6c98489e790d0b48a7692fd1885f01e3d14edb2622cd0bceabb1725704deb4. Revealing covariance does NOT necessarily reveal s or plaintext; no actual underlying FHE semantic break shown. If Server receives Sigma explicitly from trusted KeyGen, the extra leakage is even more direct, and original underlying MLWE IND-CPA theorem cannot simply be invoked with this key-dependent auxiliary view. Original Algorithm5 formal party simulation may still be separable; full protocol unproven. Direct Server b−zeta remains an algebraic potential if PI ACCEPTS changed Server trust model.
**NEXT_ACTION (PI next "继续"):** CGS-36: Pick ONE concretely specified DISTRIBUTED on-demand secret-conditioned Gaussian share generator where Server sees NEITHER raw Gaussian output NOR Sigma_s, from actual prior-art MPC/PRSS/PCF or a minimal new protocol. Test first cost and adaptive all-active-share transcript/threshold consistency under original T,N, no extra rounds and fixed setup memory, avoiding repeats of CGS10–21. If impossible without changed assumptions, prepare HUMAN_REVIEW/pivot rather than inventing broad cryptographic promises. Maintain only one primary hypothesis and one cheapest decisive test.

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


---

## Latest overriding checkpoint: CGS-36 (2026-10-15)

**This section supersedes the older CGS-35 checkpoint in the Current PI-selected active research heading above.** Latest completed: CGS-36. Next: CGS-37 (not yet begun). Current target remains original Okada-Takagi 2025/409 O(LDec) correlated Gaussian padding storage problem; still OPEN. The direct linear Shamir factor/public Gaussian candidate is rejected only as an EXACT integer discrete-Gaussian sampler, while threshold interpolation is correct.

Full finding: findings/cgs-36-public-gaussian-shamir-linear-factor-discrete-support-gate.md. Short result: share one secret-conditioned Gaussian matrix factor once; for any qualified T-of-N active set, local multiplication by one common public integer random value interpolates correctly. However with factor 2 and input G from D_Z,2 the output 2G is always even, whereas the required D_Z,4 gives odd values with probability 0.499996512657643791; total variation is exactly that value. Precise finite-grid verification and all T2-of-N3 subsets PASS. Public input randomness also raises joint-view leakage concerns; secret-sharing it instead incurs local multiplication degree growth. No full source algorithm attack or completed alternative ThFHE is claimed.

**Next CGS-37:** ONE named threshold protocol addressing the exact discrete-Gaussian support problem, testing any-T correctness, public-view privacy and memory/round costs before claiming feasibility; avoid repeating CGS-21 local nonlinear rounding. User remains PI for research pivot decisions. STATUS: PASS algebra and test; FAIL exact output Gaussian; HUMAN_REVIEW for parent target.
