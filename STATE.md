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


---

## Latest overriding checkpoint: CGS-37 (2026-10-15)

**This latest checkpoint supersedes both the older top-of-file CGS-35 heading and the CGS-36 checkpoint above.** PI-selected active research remains CGS / Okada-Takagi 2025/409 O(LDec) hidden secret-conditioned discrete Gaussian pad generation from standard (Module-)LWE; the original open target is NOT solved. CGS-37 COMPLETED; CGS-38 not started.

**Latest finding:** findings/cgs-37-public-dither-joint-discrete-gaussian-gate.md. Static Shamir-sharing of integer factor L=2, public G~D_Z,2, and PUBLIC U from {0:1/2, +/-1:1/4} gives local ζ_i=L_i G+U and all authorized Shamir interpolation correct with no extra online rounds. This fixes the missing-odd-integer SUPPORT issue of CGS36, but raw ζ=2G+U is statistically WRONG: TV with D_Z,4 is 0.04688397307743988. The public joint (U,ζ) vs public-independent (U,H), H~D_Z,4, has TV 0.51126637352153954; parity relation ζ mod2=U mod2 yields exact distinguishing advantage 0.5 if the raw/output residue is observable. This is a SOURCE DISCRETE SAMPLER substitution test, NOT an attack on original full flooding/rounded Algorithm5 transcript. Over F65537, T2-of-N3, all 492 algebraic qualified-subset checks passed. Python /mnt/data/cgs37_public_dither_joint_gaussian_gate.py SHA256 2c053d68793ed1304f55e8322f77186ec00034bfb1fa47a232a4fee6d5ab56b8; JSON SHA256 89121b8f7b7abf60a4fe9c4e075f6d113eb3286b86e4e58f4d34f0cac96d8689.

**Source/prior art:** Original 2025/409 Algorithm7 p29 requires discrete lattice Gaussian. Read full COSAC ePrint2019/1011 PDF Algorithm3/Theorem3, which employs single-party rejection/acceptance, not a threshold sampler. Read original Franzese et al. ePrint2025/1025 PDF: private MPC lookup discrete-noise sampling for DP includes nonzero measured communication, and it does not natively solve hidden correlated covariance, arbitrary T-out-of-N without extra online interaction.

**STATUS:** FAIL public-dither Gaussian distribution and raw-public joint simulator; PASS fixed Shamir linear reconstruction and test; parent CGS problem OPEN; HUMAN_REVIEW regarding viability/novelty. **NEXT CGS-38 (only upon PI continue):** ONE concrete prior-art private MPC table lookup based discrete Gaussian sampler adapted to source HIDDEN covariance, with decisive gate on online rounds, active-set thresholds, memory and Server privacy. If the existing primitive unavoidably changes source goals, recommend PI tradeoff/pivot, not further small parity variations. Follow one-hypothesis/one-minimal-test discipline. Other projects unchanged.


---

## Latest overriding checkpoint: CGS-38 (2026-10-15)

**This latest checkpoint supersedes the older top-of-file CGS-35 and the CGS-36/37 checkpoints above.** Current PI-selected single active research is CGS, Okada–Takagi 2025/409 O(LDec) correlated secret-conditioned Gaussian pad preprocessing. This OPEN problem is not solved. **CGS-38 COMPLETED; CGS-39 not yet started.** No changes to other project targets or archived directions.

**LATEST RESULT:** findings/cgs-38-public-pmf-lookup-interface-gate.md. Full original Franzese et al. ePrint2025/1025 (CCS2025) checked Algorithm4 p12 and Figure4 Pi_noise p17: it privately selects lookup INDEX and output, while each target table T_i is explicitly PUBLIC to all participants; output is ADDITIVE shares through FABB E2A, not arbitrary T-of-N Shamir; each table layer calls for party->P1 encrypted sends followed by P1->all broadcast (ell128 -> 256 such as-written directed message legs plus FABB functionality), outside source original two-round online flow. The intended scalar/ring Gaussian in Okada–Takagi Algorithm6/7 depends on secret norm/covariance, unavailable publicly. Small exact scalar Alg6 toy: binary s0=(1,0,0,0) vs s1=(1,1,1,1), norm² 1/4, Bpub5 sigma0=16; first 1570-face dice table from truncated conditioned Gaussian PMF has zero-face frequency 20 versus21. Hence DIRECT publication leaks selected norm class for the two promised toy keys. PMF TV=0.03229909136 so a fixed key-independent PMF has worst-case TV >=0.01614954568 for that toy. This is not an attack on original FHE nor a full κ-asymptotic result; scalar known-norm hardness may have special reduction, MLWE Gram leakage not proven secure. The real ring Gaussian is n-dimensional and potentially correlated, not a product of scalar lookups. 2025/1025 actual 16-party/ell128 communication is 22.22MB under its OWN DP MPC benchmark, not a CGS implementation cost.

**REPRODUCER:** /mnt/data/cgs38_public_table_leak_and_rounds_gate.py SHA256 d8fce27462913956485de1ac3459683491733414eb519112007473b9c145fb63; JSON /mnt/data/cgs38_public_table_leak_and_rounds_results.json SHA256 0305754a4d4ce801ccec2a3591552595bac7da84f7a0ec3c32dea184f97652e4. Research MCP ePrint2025/1025 full source cached PDF SHA256 ea7f3a14ddbff6214bad0a1550b2d42e2a81b9a4d01051e41841d6b0ac575d4f, version unverified. GitHub finding re-read and verified.

**STATUS:** FAIL direct existing publicly-table-based private MPC lookup port to source hidden-covariance/two-round/any-T interfaces. PASS exact first-public-die distinguishing test and original source-protocol dependency analysis. Parent secret-conditioned Gaussian O(LDec) remains OPEN/HUMAN_REVIEW. No generic impossible MPC theorem. **NEXT CGS-39 (on PI next '继续'):** ONE actual relaxed-constraint private-target-PMF scheme or change of model (e.g. accept extra online MPC messages or explicit new trust assumption) with exact test of online round/setup cost and adaptation to source secret-covariance hiding. If original constraints all fixed, recommend PI pivot instead of more trivial rejected one-party/distribution methods. One smallest falsifiable hypothesis and cheapest test; no autonomous continuation.
