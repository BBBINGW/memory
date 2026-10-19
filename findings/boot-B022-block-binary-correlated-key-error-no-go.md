# BOOT-B022 — Correlated errors inside block-binary bootstrapping keys: a source-faithful noise/security gate

TRACK_ID: BOOT
ITERATION: B022
DATE: 2026-10-19
STATUS: PASS_FORMAL_NOISE_INTERFERENCE_IDEA / FAIL_UNIMODULAR_SECURE-BY-DESIGN_REKEY_GAIN / UNCLEAR_GENERAL_CORRELATED_ERROR_SECURITY
STATE_UPDATE: YES

## One primary hypothesis and one minimal test
Research scope has been restored to genuine FHE BOOTSTRAPPING algorithm improvements (PI clarification in findings/boot-RESEARCH-STRATEGY-constructive-synthesis.md). Start with original seed ePrint 2023/958 + 2025/1892, plus fresh work on shared masks/batching. One source-specific proposed construction: generate keys in each 2023/958 one-hot block as encryptions of publicly invertible *prefix-coded* secret bits and publicly difference adjacent RGSW keys, producing NEGATIVELY CORRELATED RGSW noise. Will this reduce the expected block selector's noise under the same number of block external products and a security assumption no stronger than fresh independent RGSW keys? Primary decisive test: exact covariance/energy calculation under uniformly distributed public modswitch rotation exponents, backed by exhaustive finite negacyclic rotation enumeration. A tiny Gaussian toy/variance reduction is NOT enough; compare the concrete integer public-rekey encoding to independent-key baseline.

## Sources (original full-text PDFs inspected where available)
[FACT] Lee–Min–Seo–Song, "Faster TFHE Bootstrapping with Block Binary Keys," ePrint 2023/958, title-matched 19-page VERSION_UNVERIFIED mirror PDF SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de, physical pp. 10–12, Algorithm 2/Lemma 1. One-hot block I_j: sum_i s_i≤1; key aggregation for one block K=Σ_i(X^{a_i}−1)BRK_i; update ACC <- ACC + ACC ⊡ K; ONE external product per block, vs ℓ separate. Important: a_i are *public* modulus-switched LWE coefficients and normally uniformish over Z_(2N); ring R=Z[X]/(X^N+1); BRK_i are RGSW encryptions of secret bits.
[FACT] Hong–Lee, "Optimizing FHEW-Like Homomorphic Encryption Schemes with Smooth Performance–Failure Trade-Offs," ePrint 2025/1892, title-matched 26-page VERSION_UNVERIFIED mirror PDF SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, physical pp. 4, 11–12: heterogeneous per-BRK gadget bases; smooth performance/failure selection and optional offline duplication/gray area. Their Theorem3.1 variance model assumes the original independent encryption-key error contributions; this B022 covariance design is NOT an already established corollary.
[FACT] Bergerat et al., "Sharing the Mask: TFHE Bootstrapping on Packed Messages," TCHES 2025(4), pp925–971, DOI 10.46586/tches.v2025.i4.925-971, ePrint 2025/2112. Public official/author abstract https://eprint.iacr.org/2025/2112 and https://www.iacr.org/news/index.php?next=27151 says common-mask ciphertexts use a Matrix-LWE approach to batch message bodies; this is distinct from *correlated RGSW encryption errors*. Research-MCP requested full ePrint 2025/2112 but rejected retrieved mirror PDF identity (authors mismatch), so the complete text was NOT source-inspected; do not assert it solves our covariance approach or that our approach has novelty.
[FACT] Newer BatchBoot, USENIX Security 2026, published multi-bit/FFT-hoisted packed PBS, https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao, requires real end-to-end comparison if a construction survives. Source 2026/853 MRFHE full PDF not acquired (research MCP blocked); do not claim full source reading. Public source cross-check also searched "correlated evaluation-key error / RGSW noise / TFHE" and found no verified direct proof; ABSENCE OF SEARCH RESULTS IS NOT NOVELTY PROOF.
[QUALITY] Original sources are version-unverified mirrors, mathematical model idealized and stated below. B022 does not modify scheme parameters, run native PBS ciphertexts, estimate concrete MLWE/RLWE hardness, or prove IND-CPA/DFR. Do not claim 25% security-preserving improvement.

## Exact block noise proxy under independent uniform public masks
Work on ONE corresponding RGSW encryption error row. Let e_i∈R^N be encryption error polynomial from BRK_i, and P^a the signed negacyclic monomial multiplication matrix for X^a in R, with P^N=-I and P^(2N)=I. Put M_a=P^a-I. The aggregate key error at that row is
  η=Σ_(i=1)^ℓ M_(a_i)e_i.
Assume each coefficient-position error vector (e_1[t],...,e_ℓ[t]) is mean-zero with positive-semidefinite covariance matrix C, independent across t; public a_i are INDEPENDENT UNIFORM in Z_(2N), independent of errors. For fixed masks,
  E_e||η||²=Σ_ij C_ij Tr(M_ai M_aj^T).
Averaging over independent uniform a_i: E[P^a]=0 because P^(a+N)=−P^a. Therefore
  E_a Tr(M_ai M_aj^T)/N=2 if i=j, and 1 if i≠j.
Thus the exact expected total row-error energy is
  E_a,e||η||² = N (Tr C + 1^T C 1) = N Tr[(I+11^T) C].                  (★)
For C=σ²I, baseline =2ℓNσ².
For equal marginal variances and common offdiag correlation ρ, C=σ²[(1−ρ)I+ρ11^T], with ρ∈[−1/(ℓ−1),1], energy =Nσ²[2ℓ+ℓ(ℓ−1)ρ]. For ℓ4, ρ=−1/6 yields 6Nσ² vs baseline8Nσ², **25% reduction in ideal expected ONE-ROW ERROR ENERGY**, not a measured FHE DFR or runtime improvement. Requires checking other rows/noise sources and key-hardness.

## Native RGSW-compatible public integer-prefix encoding: a concrete construction
For ℓ=4, let
 U=[[1,0,0,0],[-1,1,0,0],[0,-1,1,0],[0,0,-1,1]].
U is integer unimodular. Define t=U^(-1) s = prefix sums (s1,s1+s2,s1+s2+s3,s1+s2+s3+s4). Under the ONE-HOT block secret s, all t_j∈{0,1} (a suffix of ones or all zero). Generate independent RGSW encryptions C_j=RGSW(t_j) with fresh independent error polynomials e'_j of covariance σ²I. Publish the legal linear difference keys BRK_i=Σ_j U_ij C_j=RGSW(s_i), using identical gadget encoding and same RLWE secret; their error vector e=Ue' has covariance C=σ² UU^T, negative adjacent offdiag.
Correctness: by linearity of RLWE/RGSW message embedding, the published BRK_i encrypt exactly s_i. The block selector Σ(X^ai−1)BRK_i has exactly the same monomial plaintext as 2023/958, so native one-external-product-per-block algebra is preserved. No new multiplication primitive is required; offline keys remain ℓ RGSW objects, although additional offline additions/subtractions are needed.
SECURITY QUALIFICATION: standard multi-message IND-CPA for independent C_j would make *public deterministic postprocessing* BRK no less secure under the SAME assumptions, PROVIDED that key-dependent/circular plaintext t_j derived from underlying secret distribution is handled by original threat model. Do not promote to a formal RLWE security reduction without resolving key-dependency; we conservatively assess performance in this permitted-by-analogy class.

## Decisive exact failure for this construction
For integer U above, C/σ²=UU^T, Tr C/σ²=7, 1^T C 1/σ²=1; hence (★) gives E||η||²=8Nσ², exactly the SAME as independent ℓ4 baseline. Negative covariance cancels one piece but increased noise variance of the difference-encrypted RGSW keys cancels that gain. No 25% noise improvement.

Stronger no-go within this *restricted*, security-compatible linear-key-recoding family:
For ANY ℓ×ℓ invertible INTEGER U, using independently encrypted transformed secrets then published BRK=U Enc(U^(-1)s), write columns v_j∈Z^ℓ. By (★),
  E||η||²/(Nσ²)=||U||_F²+||1^T U||²
    =Σ_j (||v_j||² + (1^T v_j)²).
Every column v_j is a NONZERO integer vector. If its coordinate sum ≠0, then ||v_j||²≥1 and (sum v_j)²≥1, so contribution≥2. If its sum=0, nonzero integer vector needs at least two nonzero entries, so ||v_j||²≥2. Therefore total≥2ℓ, which is precisely independent-key baseline. This is an exact lower bound for publicly inverted INTEGER linear remix of independent equal-noise RGSW key rows under independent uniform a_i, **NOT** a no-go for arbitrary correlated discrete Gaussian errors, nonuniform public rotations, changes to underlying ring/key structure, or a different security assumption.

## Additional conservative security gate for arbitrary correlated Gaussian error
A directly sampled covariance can beat 2ℓ with equal marginal noise, BUT it introduces a lower-noise public linear combination. For ℓ=4, ρ=−1/6 has covariance eigenvalues {0.5, 7/6,7/6,7/6}*σ², so publicly summing key ciphertexts exposes a direction with HALF the variance of the baseline. Security estimates for independent RLWE errors cannot simply be inherited.
If one imposes the deliberately conservative sufficient design condition C ≽ σ²I (every public real-valued linear combination retains at least baseline error variance), then since K=I+11^T ≽0, Tr(K C)≥Tr(K σ²I)=2ℓσ²; NO reduction is possible. Scaling the candidate covariance by 2 to restore λ_min=σ² increases energy from 6Nσ² to 12Nσ² (+50% vs original8Nσ²). **A spectral lower bound on noise is a design/screening assumption, not a proven necessary condition for RLWE hardness!** More exotic correlated error may preserve computational security despite λmin<σ², but requires a fresh joint-error RLWE security proof/estimator and cannot claim same-key security on the basis of marginal variances alone.
At boundary ρ=−1/(ℓ−1), covariance is singular with Σ_i e_i=0 deterministically. Publicly summing RGSW keys then yields NOISELESS encryption of Σ_i s_i∈{0,1} for every row; with enough invertible random masks and known gadget factors, guessing that bit and solving linear ring equations can reveal the ring secret. This is dangerous and must not be passed off as viable encryption.

## Independently reproduced smallest decisive exact test
Use N=4, ℓ=4, q arbitrary large/no-wrap error model, exponent indices a_i uniform over Z_8. Construct the 8 exact signed rotation matrices P^a with P^4=−I. Enumerate ALL 8^4=4096 possible public exponent tuples. Form G_ij=(1/N)Tr[(P^ai−I)(P^aj−I)^T] and average entrywise.
RESULT exact mean Gram G has diagonal2 and offdiagonal1.
Feed C values into Tr(G C):
  independent I: 8;
  unimodular-prefix U U^T: 8 (NO GAIN);
  negative equicorrelation ρ=−1/6: 6 (25% algebraic noise reduction, UNSCREENED SECURITY);
  same candidate rescaled to λ_min(C)=1: 12 (+50% noise vs baseline).
Matches symbolic (★) exactly, all 4096/4096 public tuples, no Gaussian Monte Carlo approximations.
This is one-row expected coefficient-energy, NOT actual tail probability, extreme fixed-a bound, security, ciphertext correctness under modulus reductions, or actual PBS benchmark. The source's GSW digit decomposition and NTT error correlations may add other variance terms.

## Repair search, choice, next step
[REPAIR ATTEMPT] Unimodular prefix recoding carefully preserves one-hot encrypted plaintexts and full native block external-product interface, but fails the decisive noise-value test due to unavoidable increased variance along other directions. Direct negative joint errors can show 25% proxy savings only by weakening an observable error eigen-direction and needing new security assumptions; keygen singular correlation is dangerous. No credible new bootstrapping performance improvement has been established. Do not claim a theorem about ALL secure correlated-RLWE distributions.
STATUS: FAIL_PUBLIC_INVERTIBLE_INTEGER_KEY_RECODING_GAIN / UNCLEAR_GENERAL_PSD_CORRELATED_ERROR_SECURITY / PASS_SOURCE_AND_SMALL_EXACT_TEST.
RESULT: B022 identifies a precise invariant/no-go in an interesting construction family, not just another source interface mismatch. Original focus remains ACTIVE; one failed new construction does NOT justify a topic pivot.
NEXT_TEST B023: Stay with 2023/958 one-hot block aggregation and 2025/1892 key costs, but explore a DIFFERENT expense after error correlation fails: common-mask/Matrix-LWE-style sharing of *public RGSW evaluation-key masks across ONE block* (inspired by Bergerat et al. TCHES 2025 "Sharing the Mask"). One primary necessary condition: can such a shared-mask key be secure for encrypted one-hot selector bits AND usable by 2023/958's ONE external product under the SAME ring secret, or does differencing the publicly shared-mask ciphertexts expose the selector position? Cheapest test: exact toy RLWE ciphertext difference/phase analysis for one-hot secret and known gadget magnitudes, then check whether per-body distinct mask secret/key switching can repair without erasing key-memory/online-work gain. Full official/verified source 2025/2112 is MISSING from research MCP; read official TCHES source via browser or request permitted original PDF if needed. Do not treat common-mask vs common-error as equivalent. Do one hypothesis one decisive test only.
STATE_UPDATE: YES; changes only BOOT paths.
