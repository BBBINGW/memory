# CGS-35 — On-demand Server-local secret-conditioned Gaussian samples leak the secret covariance by moments

**Date:** 2026-10-15. **Track:** single active CGS in root STATE.md; last CGS-34. One primary hypothesis, one minimal continuous-theorem + exact discrete-Gaussian toy test. This is a CONDITIONAL auxiliary-secret leakage/privacy gate for a NEW Server-assisted variation; **NOT** an attack on unmodified Okada–Takagi ThFHE.

## Hypothesis and decisive falsifier

H-CGS35: The CGS-34 server-direct ciphertext b−zeta shift may use a secret-conditioned local Gaussian sampler installed by trusted KeyGen, perhaps as an opaque description that hides Sigma_s, while keeping the Server in the ORIGINAL semantic-privacy threat model where it learns only pk, evk, encrypted inputs, PRF seeds, and publicly specified parameters. The fact the sampler outputs only fresh Gaussian noises and not the explicit secret covariance should keep Sigma_s effectively hidden, even over polynomially many decryption sessions.

FALSIFIER: If a noncolluding semi-honest Server can locally see L independent fresh Gaussian integer samples from the source-conditioned distribution for a SINGLE long-lived secret, can it infer the hidden covariance Sigma_s from output moments in polynomial time? Prove sample count for the smooth continuous source surrogate. Independently test the exact INTEGER-lattice distribution D_Z,sigma in a smallest source-shaped scalar LWE example. A positive estimator disproves the opaque-local-sampler secrecy expectation. It does **NOT** establish plaintext insecurity upon learning Sigma_s or an attack against source FHE.

## Source-provenance and original security model [FACT]

Hiroki Okada and Tsuyoshi Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409; read original physical pp24–25,28–30 via Research MCP. Cached 40 physical-page original mirror SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED; its p5 prints a newer 2026-03-26 Ver.4.
- **Algorithm 7 p29, KeyGen lines 2–4:** choose native small secret s from the ORIGINAL chi_mlwe; Sigma_s=sum_i Gram(s_i) is an integer negacyclic Gram covariance; for every planned sid, separately draw Gaussian zeta^(sid) from R(D_{Z^n, sigma0 sqrt(Bpub²I−Sigma_s)}), Shamir-share all zeta values to parties. The original Server does not get Sigma_s or these Gaussian shares.
- **Algorithm7 p29 ServerDec lines 9–15:** existing uncorrupted, semi-honest, noncolluding Server uses only pk/ciphertext, active set, parties' PRF seeds, and its fresh independent flooding E. **Algorithm5 p23** adversarial *party* simulation experiment exposes processed ciphertext and all active PartDec outputs, not Server internal state.
- **§5 p25:** The source distinguishes its formal party-corruption simulation security from its separate semantic-security guarantee **against the untrusted Server**. The server's lack of partial decryptions and ordinary underlying FHE semantic security justify the latter because its view is limited to encrypted inputs and public auxiliary material. Adding covariance Sigma_s as trusted-KeyGen input materially CHANGES this semantic-security reduction; it need not violate Algorithm5 formal party-security definition by itself.
- **§7 Lemma7.1 p30 Eq25–26:** compensating zeta makes secret-conditioned residual width public. Algorithm7 pad covariance Bpub²I−Sigma_s is the exact distribution at issue.
- The authors' newer ePrint 2026/957, *Threshold FHE with Short Decryption Shares without a Semi-trusted Server*, is a real ACISP2026 paper (DOI 10.1007/978-981-92-3015-0_8), but original PDF remained blocked through earlier Research MCP attempts. Its details and any overlap with this variant remain **UNVERIFIED**; do not claim novelty.

## Algebraic equivalence of server shift (positive narrow observation from CGS-34)

With Shamir shares sum_i lambda_i s_i=s and source padded replies pd_i=lambda_i(a s_i+zeta_i)+m_i,
b−sum_i pd_i
= (b−zeta)−sum_i [lambda_i a s_i+m_i]
whenever zeta=sum_i lambda_i zeta_i.
A new Server that knows a correct fresh zeta can broadcast b'=b−zeta and let parties send no-pad pd_i; aggregate residual and final plaintext correctness match source *algebraically*. Broadcast stays one source-shaped processed ciphertext and replies one per party; permanent Server state might reduce O(LDec) to O(n) covariance entries (or structured FFT description), but security and sampling complexity are NOT inherited. Note Sigma_s in negacyclic form has only O(n) independent ring coefficients, not arbitrary O(n²) dense storage, although reconstructing the displayed matrix is O(n²).

## ONE decisive theorem: Gaussian sampling oracle reveals its covariance [DERIVED, continuous model]

Write A_s=Bpub² I_n−Sigma_s, assumed positive definite and bounded by public Bpub² I. Under the usual Gaussian width convention exp(−pi x^T (sigma0² A_s)^−1 x), its corresponding *continuous* covariance is

C_s=(sigma0²/(2pi)) A_s.

Suppose the Server obtains L **independent, unmodded, centered, CONTINUOUS** Gaussian samples Z^(1),...,Z^(L) ∼ N(0,C_s), all tied to the same s. It computes

C_hat=(1/L) sum_t Z^(t)Z^(t)^T,
Sigma_hat=Bpub² I_n−(2pi/sigma0²) C_hat.

Every entry of Sigma_s is integer, because small secret polynomials have integer coefficients and Sigma_s is an integer Gram sum. If every entrywise error of C_hat is less than eps=sigma0²/(4pi), then rounding Sigma_hat entrywise to nearest integer recovers the **entire** Sigma_s.

By Wick/Isserlis,
Var(Z_i Z_j)= (C_s)_{ii}(C_s)_{jj}+(C_s)_{ij}² ≤2V²,
where V=sigma0² Bpub²/(2pi) bounds every diagonal entry. Thus Chebyshev and union bound over all n² entries give

Pr[any |(C_hat)ij−(C_s)ij| >= eps]
   <= 2 n² V²/(L eps²)
   <= 8 n² Bpub^4/L.

Hence **L >=32 n² Bpub^4** suffices for probability at least 3/4 that ALL covariance entries are accurately rounded (assuming exact floating arithmetic for this mathematical theorem). Divide sessions into independent blocks of that length; coordinatewise median over O(kappa+log n) blocks amplifies to negligible failure under standard Chernoff bounds. When n and Bpub are polynomial in kappa, the required number of Server-visible samples is polynomial in kappa. This is a condition-specific **information-theoretic** impossibility of keeping Sigma_s hidden from an unbounded-session local *continuous* sampler. It does not assert the same *exact* formula holds for arbitrary narrow or degenerate INTEGER lattice Gaussians, or if the Server sees only masked outputs and never the underlying Z.

For the actual **integer discrete Gaussian** R(D_{Z^n,sigma0 sqrt(A_s)}), sample covariance may have a discretization bias relative to C_s. Under sufficiently wide lattice Gaussian/smoothing conditions this bias can be negligible, but a full n-dimensional discrete-moment theorem with quantified source eps is NOT supplied here. The independent exact discrete scalar test below demonstrates the leakage in one source-shaped regime.

## ONE verified integer-discrete Gaussian experiment

Executable local /mnt/data/cgs35_server_conditional_gaussian_covariance_leak.py
SHA256 aeab5ac22269e464725a881080efd4ebc4782225aefb3f42d09a37c2b37d06a6.
Exact output JSON /mnt/data/cgs35_server_conditional_gaussian_covariance_leak_results.json
SHA256 ec6c98489e790d0b48a7692fd1885f01e3d14edb2622cd0bceabb1725704deb4.

Take scalar LWE secret n=2, norm² m=1 for s=(1,0) or m=2 for s=(1,1), as allowed by iid binary secret *examples*. Public Bpub=3, hence Bpub²=9, sigma0=8. For each fixed key, the proposed Server samples **ACTUAL lattice pmf** on Z proportional to exp[−pi z²/(64(9−m))], independently by session. The candidate widths are sigma=22.6274169979 for m1 and 21.1660104885 for m2. The discrete second moment from normalized symmetric finite sums (|z|≤12 sigma) is 81.4873308630504 for m1 and 71.3014145051691 for m2. Difference ~10.1859163578813. Discrete-vs-continuous variance biases under this test are <1.5e−14 numerically; rigorous omitted finite-grid mass bound <4.22e−198 in each case (tails from complementary error function).

Using 10,000 independent INTEGER discrete-Gaussian samples per trial and estimator

m_hat = round(9 − (2pi/64) mean(Z²))

recovers true norm-square m in 100/100 seeded trials for m=1 AND 100/100 for m=2. Rng numpy default_rng(351035) is not intended as cryptographic setup; experiment is numerical validation of sample-law distinction, not an FHE key-recovery attack. Server was given raw zeta samples because it was the local dealer; if decryption bound LDec<10000, this specific empirical estimator does not claim enough samples. In the source security asymptotic model LDec may be an arbitrary polynomial supplied in pp, so hiding covariance from a polynomially queryable local dealer is not a generic claim.

**Critical separation:** Recovering m=||s||² or Sigma_s does NOT, in general, recover s or the encrypted plaintext. Proving Server plaintext confidentiality with the extra covariate requires a new auxiliary-secret-leakage security argument, perhaps known-covariance RLWE/MLWE or a scheme-specific reduction, and formal party-security is a DIFFERENT game. This iteration tests disclosure of covariance, not semantic IND-CPA advantage given covariance.

## Research decision / limitations

- PASS: Continuous-sampler moment estimator with polynomial sample bound L>=32 n² Bpub^4 per independent block; tested exact integer scalar law, m recovered 100/100 + 100/100 times with 10k samples, tiny truncation mass.
- FAIL: Claim that supplying Server an opaque but locally queryable correct Gaussian sampler preserves secrecy of Sigma_s itself, under source-shaped polynomial samples and smooth widths. Providing explicit Sigma_s trivially leaks it even at startup.
- UNCLEAR: Whether Server learning Sigma_s ACTUALLY breaks underlying FHE semantic plaintext confidentiality under source-standard MLWE. No explicit attack on full scheme, no proof of known-covariance MLWE hardness, no complete Server security/simulation proof or efficient conditional sampling evaluation. Source formal Algorithm5 security excludes corrupting Server, but intended semi-honest Server privacy is a separate requirement, and original theorem cannot be cited verbatim after adding Sigma_s.
- Conditional model tradeoff: If PI ACCEPTS a **stronger trust model** in which noncolluding Server is permitted to learn Sigma_s, Server-direct shift gives a natural O(LDec) storage-to-O(n)-secret-statistic-state tradeoff algebraically (with new security analysis). Under the originally advertised trust / standard MLWE assumptions this is not yet a secure improvement, let alone publishable.
- Recommendation: PARK naive Server-assisted local Gaussian dealership if unchanged semi-honest Server confidentiality from ordinary MLWE is mandatory; return to a primitive where even the sampler sees only information-theoretically masked/sharded conditional outputs, or seek a rigorous augmented leakage reduction.

## End iteration

ITERATION: CGS-35.
STATUS: PASS covariance-learning theorem for continuous local sampler and exact integer Gaussian scalar control; FAIL hidden-covariance-to-Server hope for that architecture; UNCLEAR end-to-end confidential ThFHE under original source assumptions / HUMAN_REVIEW.
RESULT: Correct conditional Gaussian samples themselves statistically identify their covariance with polynomially many independent samples in continuous model, and in a source-shaped discrete toy recover ||s||². An opaque local sampling descriptor does NOT automatically prevent Server from learning Sigma. Direct b−zeta remains correct algebraically but needs a strengthened trust/auxiliary-leakage proof.
NEXT_TEST CGS-36 (only on next PI “继续”): Switch to ONE explicit *distributed* conditional noise generator where Server learns neither Sigma nor raw zeta, retaining original two-round online flow via pre-established fixed-size seeds and PRF/masked distributed output. Choose one prior-art concrete primitive and falsify source's N/T/active-set + adaptively observed all-share transcript, memory and setup. Alternatively PI HUMAN_REVIEW whether to relax Server leakage requirements; do not enumerate more local covariance-hiding disguises.
STATE_UPDATE: YES. Update only own CGS finding, CGS topic state, and sole root STATE.md.
