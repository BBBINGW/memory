# BOOT B032 — Sorted Bootstrapping CMS public-body bias correction gate

TRACK_ID: BOOT
ITERATION: B032
DATE: 2026-10-19
STATUS: PASS_EXACT_PHASE_IDENTITY / PASS_CONDITIONAL_MEAN_CENTERING / FAIL_WORST_CASE_DFR_GUARANTEE / UNCLEAR_NOVELTY_AND_END_TO_END_BENEFIT
STATE_UPDATE: YES

## Primary falsifiable hypothesis
Audit Bergerat–Orfila–Roux-Langlois–Tap ePrint 2025/2214 sorted extended TFHE bootstrapping, particularly Companion Modulus Switch (CMS). Can an unmodified ciphertext input distribution, NO new evaluation key and NO changed CMUX count, allow a publicly computable adjustment of the CMS output LWE BODY which reduces CMS-induced decryption-error bias, and is this sufficient to guarantee tighter practical security/DFR/latency? Single minimal test: exact LWE phase derivation conditioned on public mask and independent binary secret; exact fixed-sample tails including worst-case counterexample.

## Source provenance
[FACT] ePrint 2025/2214 'Accelerating TFHE with Sorted Bootstrapping Techniques', authors Loris Bergerat, Jean-Baptiste Orfila, Adeline Roux-Langlois, Samuel Tap, full 48-physical-page title-verified PDF retrieved from Github ePrint mirror, SHA256 8e342f162db953a4c26d2103f66406b5148b6fa798c7775478342900d9850d84, VERSION_UNVERIFIED. Physical pp19–23 §4 Lemmas 6–7 and Algorithm3 sorted split look-up table CMUX. Physical pp23–27 §5 CMS and Lemma8, which ALREADY models both E(eCMS) and Var(eCMS), and permits choosing ceil vs floor for d public mask positions. Paper states the additional bias (nonzero mean) under binary secret and its parameters; does not make a default distribution-free zero-mean guarantee. Physical p39–40 Tables5–6 benchmarks full SBS/CMS.
[QUALITY] The PDF text extraction loses some formula layout; algebra below independently reconstructed from the basic public one-unit CMS mask modification and source §5. No verified native repo for sorted CMS in this iteration; do not claim authors did or did not independently publish an equivalent body adjustment elsewhere. Search for 'compens' and 'bias' in extracted paper had no exact matches; absence of match is not prior-art proof. This is analysis of a prospective *modification*, not an attack on source scheme or an assertion source security fails.
[PRIOR ART] Ordinary LWE modulus switching, centering decryption-phase bias, and bias-variance management are elementary; the novelty of mere centering is LOW absent a CMS-specific nontrivial optimal selective rounding/correctness theorem or concrete new parameter frontier. The paper already analyzes mean and variance, so identifying nonzero mean by itself is NOT a novelty claim.

## Exact phase derivation and conditional scope
Let standard modswitched LWE ciphertext c=(a'_0,...,a'_(n−1),b') with binary secret s_i∈{0,1}, and phase φ(c)=b'−Σ_i a'_i s_i (mod q_out). Choose CMS publicly and deterministically from a: a''_i=a'_i+δ_i, δ_i∈{−1,0,1}; all δ known to evaluator, d nonzero coefficients. If no body edit, the added phase perturbation relative to ordinary MS is
  Δφ_uncorr = −Σ_i δ_i s_i.
For independent uniform binary secret bits, conditioned on δ:
  E[Δφ_uncorr|δ] = −D/2,  Var(Δφ_uncorr|δ)=d/4
with D=Σ_i δ_i, d=Σ_iδ_i².
Proposed **body centering**: b''=b'+t (mod q_out), t=nearest_integer(D/2); phase perturbation
  Δφ_corr = t−Σ_iδ_i s_i.
Then E[Δφ_corr|δ] = t−D/2, abs≤1/2, Var=d/4 exactly. More generally, for known independent P(s_i=1)=p_i, choose t≈Σ δ_i p_i; but changing key distribution/security parameters requires separate validation. The derivation assumes δ depends only on public a independent of the binary secret, as in standard LWE key generation. It does NOT cancel the original modulus switching error, body rounding, PBS gadget noise, correlation with conditioned original phase, or enforce output noise zero mean unconditionally across key distributions.
The compensated body adjustment does NOT change input mask classifications, GGSW key selection, sorted CMUX count, secret-key format, bootstrapping algebra, or key storage. It shifts the plaintext phase by a (small) publicly chosen fixed value; in approximate PBS this is additional error, not *exact plaintext preserving* ciphertext operation for every secret.

## Minimal independent toy and decisive counterexample
Fix d∈{8,16,32,64}, all δ_i=+1 and secret bits iid Bernoulli(1/2). Fixed-seed Python random.Random(20261019), 50000 samples each d. Define T=Σs_i, error_uncorr=−T, error_corr=d/2−T. Sampling results:
d8: uncorr mean≈−4.00106,std≈1.417, corr mean≈−0.00106; empirical Pr(|e|≥d/4)=0.9643→0.28936.
d16: uncorr mean≈−7.99588,std≈2.002, corr mean≈+0.00412; Pr(|e|≥d/4)=0.9898→0.07764.
d32: uncorr mean≈−15.99478,std≈2.837,corr mean≈+0.00522; Pr(|e|≥d/4)=0.99902→0.00718.
d64: uncorr mean≈−31.9974,std≈4.012,corr mean≈+0.0026; Pr(|e|≥d/4)=1.0000→0.00002.
These are *added CMS perturbation only*, all positive δ artificially selected; d/4 is an illustrative threshold, NOT the paper's actual decrypt margin or cryptographic DFR. No encrypted native trial. Pairing each s sample trivially checks exact phase difference. The absolute bias reduction is mathematically exact irrespective of toy data.
Counterexample to UNIVERSAL per-ciphertext improvement: d4, δ=(1,1,1,1), s=(0,0,0,0): uncompensated Δφ=0, compensated Δφ=+2, so absolute error WORSENS. For s=(1,1,1,1), uncompensated−4, compensated−2 improves. Therefore no pointwise bound that correction makes EVERY ciphertext closer; it only centers the assumed secret-averaged distribution. Under adversarial secret keys (binary s fixed, not stochastic averaged) correction can be worse; exact IND-CPA-D security needs careful DFR over actual key distribution and chosen/adversarial ciphertext inputs. When D has both signs and is already near0, compensation offers little. For ternary/centered secret with E(s)=0, this binary-specific D/2 is WRONG and raises bias. 
Concrete noise/DFR safety obligation: for target modulus q_out and message gap, bound total e_total=e_standardCMS + Δφ_corr including covariance and tail probabilities; if compared to source Lemma8 average variance, note Var(d/4) unchanged, though squared uncentered error and bias improve. Need handle messages near LUT decision boundaries, correlations with chosen coefficient classes, and correct IND-CPAD adversarial ciphertext/noise assumptions.
Potential better future constructive objective (NOT B032 tested): choose CMS rounding directions subject to exact publicly computed D, cost savings Σ_i(η/µ_class(a_i)) and optimize deviation/variance, then quantify a genuine Pareto frontier and compare paper's optimal d selection. But this is a fresh primary hypothesis, so archive without pretending to have tested it.

## End of iteration
STATUS: PASS_CONDITIONAL_BIAS_CORRECTION / FAIL_POINTWISE_ERROR_MONOTONICITY / UNCLEAR_ACTUAL_DFR_GAIN / LOW_STANDALONE_NOVELTY.
RESULT: A source-specific, local, no-new-key public-body correction is algebraically valid and removes the added CMS mask-rounding *mean* for iid binary keys without affecting variance, and toy error-tail improvements exist under a contrived sign pattern; however it can make particular ciphertexts strictly worse, is no global correctness or real security proof, and is a likely elementary/unpublished-vs-published-prior-art issue. No native end-to-end TFHE implementation, accurate noise-tail security, or measured speedup. NO paper claim.
NEXT_TEST B033: Only BOOT. If pursuing 2025/2214 further, one *nontrivial* primary objective: design and test an input-aware CMS sign-balanced **selection problem** that trades saved CMUX count against a proven tail/noise budget, comparing directly with source fixed d CMS and taking binary/ternary secret distribution and IND-CPAD into account. Cheap falsifier: exhaustive small coefficient class and rounding-direction states to determine whether adaptive selection has strictly better cost/error Pareto frontier than paper's already optimized d and parameter choices. If no true gain or prior art subsumes, archive and choose another genuinely recent full-source bootstrapping gap. B033 NOT STARTED. STATE_UPDATE YES. BOOT-only files.
