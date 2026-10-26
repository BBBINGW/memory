# PURE-FHE · P0-PRESCOUT-47 — Shared Auk_-1: exact gadget digit-mean covariance and Gaussian-tail no-go

DATE: 2026-10-27 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
PREVIOUS: P0-PRESCOUT-46, findings/pure-fhe-p0-46-batchboot-branch-typed-twisted-rgsw-covariance-dfr-gate-2026-10-27.md, commit c9f6d98f003cfe472612960731baf5150f5762e1
LATEST_COMPLETED: P0-PRESCOUT-47
NEXT_ITERATION: P0-PRESCOUT-48 NOT_STARTED; retained only if PI explicitly continues
STATUS: FAIL_INDEPENDENT_NOISE_ASSUMPTION_FOR_UNCENTERED_DIGITS / FAIL_GAUSSIAN_TAIL_INFERENCE_FROM_ZERO_COVARIANCE / ACTUAL_BATCHBOOT_DFR_UNCLEAR / NOVELTY_NOT_ESTABLISHED
CODEX_REQUIRED: NO; no code, GPU, native, remote, repository infrastructural edits.
STATE_UPDATE: YES one isolated PURE-FHE finding; root STATE.md and SHIP/BOOT/CGS/VFHE/EAI all untouched.

## Fixed one falsifiable H47

The P0-44 candidate constructs twisted BatchBoot RGSW from ordinary RGSW via tau followed by rowwise RLWE key switching with a SINGLE shared added automorphism key Auk_-1. Under low-base retune B_A=4,d_A=32, is it justified to treat the added noise of separately derived RGSW rows as independent Gaussian, as required to directly propagate author Appendix B / C Gaussian DFR model with only independent per-row variances?

CHEAP DECISIVE TEST: first-party gadget Decom definition and actual source-specific randomness assumptions; derive cross-covariances for independently uniformly random RLWE masks but the SAME public Auk error. Stress-test even a hypothetical zero-mean digit representation via fourth moments. No native code. We distinguish original author claims from conditional model predictions and exclude claims of real decryption failure.

## [FACT] Original source precisely checked

Original USENIX Security 2026 publisher PDF, Zhihao Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf ; publication page https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao .
PDF web screenshot zero-index pages 2 (§2.2 Decom and GP), 5 (§4.1 Eq7-9, Table1, variant RGSW), 6 (Algorithm2), 17 (Appendix C.2 Lemmas4.1/4.2), 19 (Tables9/10,C.4), and PDF textual B.2/B.3 page16 read. Screenshots were explicitly used to interpret source PDF.

Source §2.2 defines g_i=ceil(Q/B^d)B^i, a gadget decomposition satisfying <g^-1(a),g>=a+epsilon with ||epsilon||≤(1/2)ceil(Q/B^d). It DOES NOT, in the paper definitions consulted, uniquely specify the deterministic or randomized choice of signed/unsigned digit representatives or establish E[D]=0 for the new converted rows. Appendix B.2 writes gadget-product variance formula V_GP=(B² dN/12)Var(key RLWE)+(N/12)ceil(Q/B^d)^2; Appendix B.3 explicitly says RLWE key switching has V_RKS same as GP. Source Appendix C.2 Lemma4.1 adds 4 EP error variances per 2-bit stage and Lemma4.2 adds EMP, Pack, RKS variances; Appendix C.4 uses a Gaussian tail approximation. These are THEIR original fresh-key calculations, not a conditional-on-public-key DFR theorem for the new shared-Auk derivation. Table10 native Boot6 parameters B_Bsk=2^23,d_Bsk1, B_Auk=2^23,d_Auk1,N4096; P0-45's proposed NEW Auk_-1 B_A=4,d_A=32 is not in source. Table9 auxiliary std2^-53 is listed for another Boot6 key distribution/ring N2048, not a source-verified new Auk at N4096.

The baseline BSK itself is public and reused across inputs; therefore noting the new shared Auk induces dependence is NOT, by itself, a source paper break or proof stronger security is impossible. The correct novelty/proof goal is *incremental* dependence beyond baseline and whether it creates a forbidden conditional-on-fixed-evaluation-key failure probability.

## [DERIVATION] Exact common-key covariance algebra

Let E=(E_1,...,E_r) be a vector of independently sampled, mean-zero KSK error coefficients with covariance sigma_A² I, and let D_i,D_j be independent gadget digit vectors arising from independent uniform RLWE masks, also independent of E. The schematic extra rowwise KS error (at one coefficient, after rearranging polynomial convolution and signs) has the form
  Z_i = <D_i,E>,    Z_j=<D_j,E>.
Taking averages over both independently randomized RGSW masks and key generation,
  Cov(Z_i,Z_j)=E[D_i^T (sigma_A² I) D_j] = sigma_A² <E[D_i], E[D_j]> for i≠j.
In the true negacyclic polynomial case, the D_i vectors are expanded to all coefficient/digit positions, convolved with KSK error coefficients with signed index permutations. The same *mean-weight cross-covariance* calculation applies at a fixed output coefficient when all coefficient masks are iid uniform. It is not automatically zero just because the RLWE encryption masks a_i are independent. The common E is exactly what makes them dependent.
The derivation assumes iid errors and independently uniform masks and says NOTHING about original source's exact prepared/NTT key generation, balanced decomposition randomization, secret-dependent covariance, or actual nonlinear EP input coefficients.

Set Q=2^64, B=4,d=32 so B^d=Q and the source's gadget exact reconstruction is possible using standard radix representatives. For *two possible source-definition-compatible exact radix encodings* of a uniform mask coefficient (these are possible algorithms, NOT a claim of which one the authors' implementation uses):

 A. UNSIGNED digits uniform {0,1,2,3}:
 mu=3/2; E[D²]=7/2; Var(D)=5/4; per-row Var(DE)=7/2 sigma_A²; distinct-row Cov=9/4 sigma_A²; rho= (9/4)/(7/2)=9/14≈0.642857.
 B. DETERMINISTIC BALANCED digits uniform {-2,-1,0,1}:
 mu=-1/2; E[D²]=3/2; Var(D)=5/4; per-row Var(DE)=3/2 sigma_A²; distinct-row Cov=1/4 sigma_A²; rho=(1/4)/(3/2)=1/6≈0.166667.

For full negacyclic polynomial with N coefficients and d independently uniform complete gadget digits, single-coefficient per-row Var(Z)=Nd E[D²]sigma_A² and cross-covariance between two distinct converted rows is Nd mu² sigma_A². The same correlation ratio persists. For N4096,d32, sigma_A=2^-53 as an *illustrative assumption only*:
  balanced common component sqrt(Nd)|mu|sigma_A=2^-45.5=2.0097183471152322e-14 (torus normalized);
  unsigned common component=2^-43.915037499...=6.029155041345697e-14.
These are not observed distributions nor proof of final DFR.

The source's B²/12 variance expression is an approximate upper-accounting model and cannot by itself be promoted to all moments of a chosen digit distribution; e.g. E[D²] and Var(D) differ when digit means are nonzero.

## [DERIVATION + EXACT NUMERIC] Covariance amplification under a PARTICULAR all-positive reuse workload

For M equally weighted distinct derived row errors with identical marginal sigma_Z² and constant positive pairwise correlation rho,
  Var(Σ_i Z_i)=M sigma_Z²*(1+(M-1)rho);
  SD relative to zero-covariance sqrt(M)*sigma_Z = sqrt(1+(M-1)rho).
For M=612 and balanced rho=1/6 this factor is 10.140677163450837; for unsigned rho=9/14 it is 19.844034727991037. In actual BatchBoot the P0-46 612 is at most a worst-case count of *twisted external product contributions* along 34 EMPs, NOT necessarily 612 distinct single-row noise scalars with equal +1 weights; many terms have additional randomized/decomposed coefficients and branch signs, some may cancel. Therefore these dramatic factors are **toy correlation stress tests, NOT actual Boot6 DFR inflation estimates**. A valid analysis must compute contraction through actual Algorithm2 gadget coefficients and compare covariance with the native direct-BSK baseline.

## [DERIVATION] Zero covariance is insufficient to infer Gaussian tails, EVEN WITH truly centered digits

Take independent Rademacher signs D_i∈{-1,+1} and one shared E~N(0,sigma²); define S=E Σ_{i=1}^M D_i. Each Z_i=D_iE has mean zero, Var=sigma², and Cov(Z_i,Z_j)=0 for i≠j, because E[D_iD_j]=0. Nonetheless S is a *Gaussian scale mixture*, not Gaussian:
  Var(S)=M sigma²,
  E[S⁴]=3 sigma⁴ E[(Σ D_i)^4] =3 sigma⁴ (3M²−2M),
  standardized 4th moment =9−6/M (M=2 gives 6, M→∞ gives 9), compared with 3 for an exact Gaussian.
Thus even mathematically PROVING all new pairwise covariance to vanish by randomized centered gadget digits does NOT justify author Gaussian P_fail=erfc(T/(sqrt2 σ)) for an entire repeated-key circuit. Need conditional-on-fixed-key subgaussian or martingale tail bound for actual algorithm and all queried inputs, or rigorous high-moment/mixture bound and matching DFR. This is an independent mathematical falsification of the variance-only jump, not a performance or security attack on BatchBoot's real implementation. Randomized or centered gadgets are established prior art; the toy is not an original FHE primitive.

More fundamentally, E is public-key-generation randomness fixed for the lifetime of the evaluation key. Sampling fresh input ciphertexts later does not resample E. Unconditional moments over both E and all D_i could underestimate worst-case or high-quantile failure of rare "bad keys." To claim IND-CPA-D multiquery/fixed-key security must explicitly state the keygen-quantifier, conditional input distributions and number/adaptivity of queries; a single Gaussian average DFR is inadequate.

## Evidence and uncertainty decision

H47 "ordinary source model provides independent Gaussian errors for all on-demand converted key rows" FAILS as a general deduction: two legitimate gadget digit representations lead to nonzero common-key covariance; even a hypothetical perfectly centered decomposition gives uncorrelated but non-Gaussian joint sums. The author PDF's gadget bounds alone do not uniquely tell which digit representation its implemented Decom takes, and no actual reused-Auk joint tail theorem has been obtained. Actual algorithm might have cancellations/properties reducing dependence, so this does NOT KILL all possible source-adapted schemes or prove a new attack. No actual DFR bound and no 2^-64 certificate is established for the derived-key proposal.

Remaining full crypto+systems obligations: obtain exact source code or author-level digit decomposition/key generation and prepared-key layout, prove covariance of full EP outputs and key-conditioned rare tails under reused Auk_-1 *relative to baseline reused native BSK*, produce full-parameter noise/DFR/security certificate, and show full all-keys/peak RAM plus on-demand cost advantage. These are substantial and currently not cost-justified given standard nature of aut+KS. Recommend **PARK pending source**, not automatic next noisy parameter scan or Codex task. P0-PRESCOUT-48 remains NOT_STARTED; only if PI directs source acquisition / tight keygen-specific covariance proof.

END_OF_ITERATION:
STATUS: FAIL_NAIVE_INDEPENDENT_ERROR_AND_GAUSSIAN_DFR_JUMP / PASS_EXPLICIT_SHARED_KEY_COVARIANCE_COUNTEREXAMPLE / SOURCE_SPECIFIC_DFR_UNCLEAR
RESULT: exact formula Cov(Z_i,Z_j)=sigma_A²<E[D_i],E[D_j]>; balanced radix4 toy correlation1/6, unsigned9/14; even centered independent Rademacher row digits lead to zero covariance but fourth moment9−6/M vs Gaussian3 under common-key reuse.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: P0-48 NOT_STARTED, optional narrow source-code/author-keygen audit for actual centered gadget decomposition and conditional output tails; do not start native runs without a novel distinct positive construct.
STATE_UPDATE: YES only this isolated findings document; root STATE.md and unrelated project branches not written.
CODEX_REQUIRED: NO.
