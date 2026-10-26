# PURE-FHE · P0-PRESCOUT-48 — MOSFHET source audit for shared-Auk gadget digits and conditional key-noise tails

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
PREVIOUS: P0-PRESCOUT-47, findings/pure-fhe-p0-47-batchboot-shared-auk-digit-mean-covariance-tail-gate-2026-10-27.md; commit cc02798095008b6f2127e173768660d22ce2ab25
LATEST_COMPLETED: P0-PRESCOUT-48
NEXT_ITERATION: P0-PRESCOUT-49 NOT_STARTED, HUMAN_REVIEW/GATE_REQUIRED
STATUS: PASS_UPSTREAM_SOURCE_BALANCED_NONCENTERED_DIGITS / FAIL_NAIVE_ZERO_MEAN / FAIL_UNMODIFIED_64BIT_B4_D32_PATH / PASS_CONDITIONAL_HOEFFDING_ROW_TAIL / ACTUAL_BATCHBOOT_ARTIFACT_UNREAD / FULL_DFR_UNCLEAR
NOVELTY: NOT_ESTABLISHED. Conditional Hoeffding and secret-key automorphism are standard; no new FHE scheme.
STATE_UPDATE: YES only this isolated PURE-FHE finding; shared STATE.md and SHIP/BOOT/CGS/VFHE/EAI untouched.
CODEX_REQUIRED: NO. No GPU, native tests, model downloads, environment/install or infrastructure writes.

## One falsifiable H48

Can the publicly accessible source used as BatchBoot's cited base implementation certify an actually zero-mean gadget decomposition that lets distinct transformed RGSW rows derived with the same added Auk_tau be treated as independent Gaussian for 6-bit DFR? And can the proposed low-base retune B_A=4,d_A=32 even enter the unmodified upstream key-switch decomposition routine?

Cheapest test: identify the official BatchBoot artifact, locate the cited MOSFHET upstream source, examine exact signed digit extraction and KSK generation/use; calculate conditional-on-fixed-key concentration. This is source analysis + mathematical derivation ONLY.

## [FACT] Sources, exact provenance and important missing source

BatchBoot original paper: Zhihao Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026, official publisher PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf , §2.2 physical page 3, §6.1 / experimental description physical page 12, Open Science physical page 14, appendix pages 18–20. These PDF pages were read and SCREENSHOTS visually inspected in current turn. It states its algorithms are executed in 'MOSFHE [32]' and reference [32] is Guimarães, Borin, Aranha, 'MOSFHET: Optimized Software for FHE over the Torus', J Cryptographic Engineering 2024. Its §2.2 Decom defines a gadget reconstruction relation and remainder bound, but does not uniquely identify signed digit representatives or the random distribution of the digits on a fixed public key. Its Appendix C.4 computes a *Gaussian approximation* for DFR, not a joint tail theorem for the newly proposed shared-Auk derived keys.

**NEW SOURCE DISCOVERED:** USENIX Security 2026 Artifact Evaluation lists BatchBoot with 'Artifacts Available' badge and a real official code archive at https://zenodo.org/records/17936945 (DOI 10.5281/zenodo.17936945). Evidence: https://secartifacts.github.io/usenixsec2026/results and source PDF Open Science. The Zenodo archive itself was not accessible through available public page/fetch routes in this turn (cache miss/network blocked), so authors' BatchBoot artifact's source tree, exact fork/patch, BSK object serialization, KeyGen, prepared key representation and Decom are **NOT** independently inspected. Artifact AVAILABLE != artifact READ. Any inference from the upstream library to authors' final fork is conditional.

**ACTUALLY READ upstream source:** GitHub https://github.com/antoniocgj/MOSFHET at pinned commit a6e7fbb47cd4451ebcc6693027e65a27d934a399. Files directly fetched:
- src/polynomial.c blob e120e9bc36caa2bc437e4018cce1232fa4e92b6a, lines 55–93, containing polynomial_decompose() and polynomial_decompose_i().
- src/keyswitch.c blob 2bfac0912413c4e351eef65d9ceef66e1c5a53c4, lines 13–35 (TRLWE_KS_Key generation via trlwe_sample) and 162–187 (trlwe_keyswitch invoking polynomial_decompose_i).
- include/mosfhet.h, lines 1–24, where default Torus is uint64_t unless TORUS32 defined. Repository source is a close technological BASELINE/ancestor, NOT evidence of exactly identical authors' batch artifact.

## [FACT + DERIVATION] Upstream has balanced signed but NONZERO-MEAN radix digits

Upstream src/polynomial.c extracts digit
  uint64_t half_Bg=(1ULL<<(Bg_bit-1));
  uint64_t h_mask=(1ULL<<Bg_bit)-1;
  out->coeffs[c]=((coeff_off>>h_bit)&h_mask)-half_Bg;
with a deterministic offset added before bit extraction. For Bg_bit=2 this is mathematical set {-2,-1,0,1}, represented modulo 2^64 by Torus. If input mask polynomial coefficients are independently uniform mod 2^64 and extraction shifts are valid, adding a constant preserves uniformity of the selected two-bit blocks; for the complete selected digit blocks, each digit is uniform over these 4 possibilities:
   E[D]=-1/2; E[D²]=3/2; Var(D)=5/4.
The P0-47 deterministic-balanced case is therefore ACTUALLY implemented in this cited upstream library; it is no longer merely an arbitrary invented digit model. Still, whether BatchBoot authors' distinct archive uses precisely it is not verified.

## [FACT/STATIC-CHECK] P0-45 d=32 is not directly supported by one upstream code path

The key-switch routine trlwe_keyswitch() calls polynomial_decompose_i(). The latter computes:
  const int bit_size=sizeof(Torus)*8;
  uint64_t offset=1ULL << (bit_size-l*Bg_bit-1);
before its digit loop. In the default uint64_t Torus mode, Bg_bit=2,l=32 sets shift amount 64-32*2-1=-1, which is INVALID / undefined behavior in C. There is no demonstrated safe check or alternate path in the fetched source. This is a STATIC source-level limit for this specific upstream function; it is NOT a claim that BatchBoot shipped code uses d32 (its source native Auk d=1) or a discovered flaw in published BatchBoot.
Using Bg_bit=2,l=31 yields shift amount +1, and last digit h_bit=64-(31*2)=2; both are in range. The upstream keygen's powers 2^(64-(j+1)*2) likewise remain within valid range for j=0..30. Complete 64-bit reconstruction is not achieved: Q/B^31=4 and the source gadget truncation/rounding bound must be charged. Thus b=2,d=31 avoids THIS undefined shift and has a small truncation term in the P0-45 source variance formula. It is not a real compiled native test, nor proof all other code paths support these large t values.

Illustrative theoretical source variance model with Q=2^64,N=4096,B_A=4, hypothetical sigma_A=2^-53:
  sigma_model(d=31)≈4.56815068052058e-14 ≈2^-44.3153831;
  sigma_model(d=32)≈4.64124571588986e-14 ≈2^-44.2924813.
These are model-calculated row-noise scales not observed values. The source Table9 sigma 2^-53 is for its other parameter row, not certified for a *new* 4096-dimensional Auk_tau. Replacing 32 with 31 only repairs the highlighted upstream bit-shift and hardly addresses actual DFR/security/novelty.

## [DERIVATION] Exact fixed-key conditional decomposition of noise

Let E=(E_1,...,E_r) be the fresh **once at key generation** KSK error coefficients; r=N*d in the one-output-coordinate convolution expansion. Suppose the masked digit vectors D_i for distinct derived rows are iid uniform over {-2,-1,0,1}, independent of E, as a SIMPLIFYING pre-EP model. Each converted-row added scalar error is Z_i=<D_i,E> (convolution carries index signs but has the same norm/mean structure coefficient-wise when indexed correctly).

For a FIXED E=e,
  b(e)=E_D[Z_i|E=e]=mu * sum_j e_j with mu=-1/2,
  Var_D(Z_i|E=e)=(5/4)*||e||_2^2.
Conditional on E=e and independence of different input masks, the Z_i are conditionally independent AROUND THE SHARED BIAS b(e). They are not zero-mean conditional on E. This distinguishes conditional independence of centered rows from the globally independent zero-mean assumption falsely used in P0-46 Gaussian proxy.

For M independently masked derived rows reusing e, let S_M=sum_i Z_i. Then exactly
  E[S_M|E=e]=M*b(e),
  Var(S_M|E=e)=(5/4)*M*||e||_2².
For any real t, Hoeffding's lemma for each centered D_ij-mu supported in [-3/2,3/2] gives
  E[exp(t*(S_M-M*b(e)))|E=e] <= exp( (9/8)*M*t²*||e||_2² ),
and therefore
  Pr(|S_M-M*b(e)| >= x | E=e) <= 2 exp(-2*x²/(9*M*||e||_2²)).
This is a VALID conservative fixed-key conditional subgaussian TAIL for the SPECIFIED linearized iid-digit model. It is not a Gaussian identity and it does not bound the absolute error until the common drift M*b(e) is also controlled by an appropriate high-prob key-generation guarantee. Conditional tails across real BatchBoot EPs need additional source proofs: actual Decom input coefficients, difference/cancellation signs, reuse of intermediate ciphertexts, and potentially non-independence of masks.

Unconditionally, if E_j are iid mean-zero with Var(E_j)=sigma_A²,
  Var(S_M)=r*sigma_A²*((5/4)*M+(1/4)*M²),
whereas independent centered-row summation would claim r*sigma_A²*(3/2)*M. The ratio is (M+5)/6, yielding SD inflation sqrt((M+5)/6) under this exact toy sum model; at M=612 the factor is 10.140677. Again, M=612 is the P0-46 count of TWISTED external product CONTRIBUTIONS in one worst-case output-lineage envelope, NOT 612 independent identically weighted RGSW rows. Therefore 10.14 is NOT an actual BatchBoot DFR inflation claim.

Illustrative b=2,d=31,N=4096,sigma_A=2^-53: common-key per-output-coefficient drift over key generation has SD |mu|sqrt(Nd)*sigma_A≈1.9780672612e-14; in a deliberately artificial all-positive 612-term sum SD≈1.21057716e-11. The conditional fluctuation term at M612 has RMS ~1.09421274e-12. These are far below an EP-amplified full-circuit DFR analysis and must NEVER be treated as measured physical error or real final margin.

Proof implications: even if a randomized balanced gadget made digit mean 0, the P0-47 Rademacher-times-common-Gaussian fourth-moment example shows conditional-key mixture tails need not be Gaussian. Need a full fixed-evaluation-key conditional/martingale concentration theorem and the actual BatchBoot EP pipeline, not another mean-zero scan.

## Decision / novelty gate

H48 that a direct source read proves zero-mean independent Gaussian derived rows: FAIL for the upstream library (actually nonzero mean) and unproven for the separate author's archive (not read). One genuine step beyond P0-47: source-grounded deterministic signed decomposition, an exact row-level FIXED KEY Hoeffding inequality replacing unconditional Gaussian wishful thinking, and precise d32 undefined-shift limitation plus d31 workaround for this upstream code.

However these observations are established probability and implementation facts, not a positive original FHE construction. Remaining task is substantial: read actual BatchBoot Zenodo artifact, inspect changes to MOSFHET's source and KeyGen, exact σ_A and dimension, prove key-conditioned convergence through full Alg2 under 34 repeated operations and packing/RKS/MS, run full all-key peak RAM ledger and compare to prior key representation methods. Programmatic novelty still not established. Given 48 rounds and user preference for publishable pure-FHE technique, prioritize PARK/HUMAN_REVIEW. Do not start Codex merely for upstream d31 instrumentation. A follow-up P0-49 is justified ONLY if source artifact and a concrete way to beat full noise/key/latency budget is independently available.

END_OF_ITERATION
STATUS: PASS_CITED_UPSTREAM_DIGIT_STATIC_AUDIT / PASS_CONDITIONAL_HOEFFDING_ROW_LEMMA / FAIL_ZERO_MEAN_GAUSSIAN_ASSUMPTION / BATCHBOOT_NATIVE_ARTIFACT_BLOCKED
RESULT: upstream MOSFHET radix4 signed digits {-2,-1,0,1} E[D]=-1/2; reused key yields per-key drift and conditional subgaussian fluctuations. Unmodified upstream trlwe_keyswitch path has C invalid shift for d32 in 64-bit torus; d31 valid in highlighted path with ≈same modeled marginal noise.
NOVELTY: NOT_ESTABLISHED; NOT AN IMPLEMENTED FHE SPEEDUP.
NEXT_TEST: SOURCE_GATE (BatchBoot Zenodo DOI 10.5281/zenodo.17936945 artifact, exact decomposition/keys) before any further P0 math or code; P0-49 NOT_STARTED.
STATE_UPDATE: YES isolated finding only.
CODEX_REQUIRED: NO.