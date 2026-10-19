# BOOT-B004 — Source-Faithful Gadget Digit and Residual Tail Gate

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B004
STATUS: PASS_COMPONENT / FAIL_FULL_DFR_CERTIFICATE
STATE_UPDATE: YES

## Primary hypothesis
[HYPOTHESIS] Replacing the crude unsigned gadget-digit and unrestricted binary ring-key bounds used in BOOT-B003 by the actual centered TFHE implementation digits and the block-binary ring-secret Hamming-weight constraint makes a mathematically valid, nonvacuous DFR certificate for the published uniform d=3 configuration at a target single-bootstrap tail of 2^-128, without additional rounding randomization or assuming independence of truncation residuals.

## Sources and technical provenance
- [FACT] Lee–Min–Seo–Song, "Faster TFHE Bootstrapping with Block Binary Keys" ePrint 2023/958, physical pp. 4 (Section 2.3, gadget decomposition), 11 (Algorithm 2, Lemma 1), 14–17 (key generation, security, concrete parameters and FFT costs), mirror sha256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de, VERSION_UNVERIFIED.
- [FACT] Hong–Lee ePrint 2025/1892, physical pp. 11–13 (heterogeneous and approximate gadget construction), 25–26 Appendix B, mirror sha256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, VERSION_UNVERIFIED.
- [FACT] SNUCP/blockkey-tfhe at commit 633c9ed9adae9b6eab095af7dd9f9757acc59300, paths src/libtfhe/tgsw.cpp (offset and gadget representation), src/libtfhe/tgsw-functions.cpp (tGswTorus32PolynomialDecompH), src/libtfhe/lwe-functions.cpp (lweSparseKeyGen), src/libtfhe/tlwe-functions.cpp (tLweSparseKeyGen), src/libtfhe/lwe-bootstrapping-functions-sparse.cpp (blockwise hoisting), src/libtfhe/tgsw-fft-operations.cpp (FFT hoisted external product), src/libtfhe/tfhe_gate_bootstrapping.cpp (parameters). This is read-only source inspection, not an executed native benchmark. Source does use sparse specialized bootstrapping; the ordinary tfhe_blindRotate_FFT path is not the sparse specialized one.

## Cheap decisive verification 1: signed digits vs unsigned truncation residual
[FACT from exact code] For a 32-bit torus input u, B=2^7=128,d=3, digit j is ((u+offset)>>[32-7(j+1)] & 127)-64 with unsigned-32-bit modular addition and offset =64*(2^25+2^18+2^11). Each digit lies in [-64,63]. Reconstructed element modulo 2^32 is
    R(u) = sum_{j=0}^2 h_j(u)*2^{32-7(j+1)} (mod 2^32).
[DERIVATION] Exact identity: R(u) = floor(u/2^11)*2^11 (mod 2^32), hence the discarded residual r(u) = (u-R(u) mod 2^32)/2^32 = (u mod 2^11)/2^32, in [0,2^-21). This is an *unsigned*, biased truncation residual, despite signed/centered digits. For u=2047, h=(0,0,0), r=2047/2^32 > 2^-22, falsifying an automatic half-ULP assumption.
[TEST] Independent integer bit manipulation enumerated all 2048 low-bit values for three representative 32-bit high-word choices including high sign bit; all satisfied the identity. This is a self-contained toy/reference arithmetic test, not native execution of the C++ implementation.

## Cheap decisive verification 2: ring secret weight
[FACT] 2023/958 KeyGen constructs t=(s,s') where s has k=n/ell blocks each with <=1 bit 1, and s' is an arbitrary binary suffix of length N-n. Code lweSparseKeyGen and tLweSparseKeyGen implement the same shape for the reported pairs (ell,n).
[DERIVATION] Hence deterministic weight bound w=HW(t)<=k+(N-n), sharper than generic w<=N. For the torus phase decomposition residual eps_j = r_b -t*r_a, coefficient infinity norm <=(1+w)*eps, eps=2^-21. Since block selector m_j is either zero or X^a-1, ||m_j eps_j||_infty<=2(1+w)eps, and the later monomial rotations preserve coefficient infinity norm. Summing all k blocks gives a rigorous deterministic residual error ceiling
    R_ell = 2*k*(1+k+N-n)*2^-21.
This removes the artificial unconstrained-secret w=N factor but does not infer cancellation or unbiasedness.

| ell | n | k | w_max | R_ell |
|---:|---:|---:|---:|---:|
|2|630|315|709|0.2132892608642578|
|3|687|229|566|0.12382793426513672|
|4|788|197|433|0.08153724670410156|
|5|885|177|316|0.05350971221923828|
|6|978|163|209|0.03264427185058594|

[RESULT] For ell=3,4,5,6, rounding *alone* is now certified below the 1/8 extraction margin. For ell=2 the bound remains above 1/8. Neither case establishes overall DFR.

## Cheap decisive verification 3: key-error concentration under strong favorable simplifications
[ASSUMPTIONS] Fix a non-adaptive input independently chosen from evaluation-key noise, condition on ring secret and public exponents, use ideal independent mean-zero Gaussian fresh TRGSW key errors with per-coefficient variance beta^2=2^-50, ignore modulus switching, key switching, numerical FFT and all other errors; later gadget digits can depend on previous blocks. These assumptions are not a full FHE security/DFR model.
[DERIVATION] The same predictable-coefficient Gaussian martingale upper bound from B002 is V<=8*beta^2*n*d*N*D^2, but correct C++ digit bound is D=64 not 128. At ell=2, V<=5.632638931274414e-5, sigma<=0.00750509. For a hypothetical zero truncation residual at T=1/8, the key-error-only two-sided Chernoff bound 2exp(-T^2/(2V)) is ~2^-199.1, a component-only bound.
[DERIVATION] For the *actual* deterministic residual bound R_ell, if R_ell<T=1/8, the combined simplified bound is
    P(|Err_round + Err_key|>=T) <= min(1, 2 exp(-(T-R_ell)^2/(2V_ell))),
    V_ell=8*(2^-25)^2*n*3*1024*64^2.
This can be used as an upper bound (not exact DFR) only under the assumptions above and consistent torus lifting. Results:

| ell | rounding bound R | sqrt(V) | remaining margin T-R | log2 of raw upper bound |
|---:|---:|---:|---:|---:|
|2|0.2132893|0.0075051|negative|not applicable|
|3|0.1238279|0.0078373|0.0011721|+0.98 (clamp to 1: vacuous)|
|4|0.0815372|0.0083936|0.0434628|-18.34|
|5|0.0535097|0.0088952|0.0714903|-45.59|
|6|0.0326443|0.0093509|0.0923557|-69.37|

[CONCLUSION] Even this optimistic *component-only* bound does not certify 2^-128 once deterministic truncation is included; nor is the actual full DFR measured or proven. The original stated hypothesis FAILS, while the source-faithful arithmetic refinement PASSES.

## Subtle limits and possible path
[FACT] The sign-centering offset shifts digit representations but does NOT dither the low 11 discarded bits. Therefore assuming zero-mean independent rounding errors is unjustified.
[OPEN] Conditional on adaptive encrypted accumulator and fixed/reused evaluation keys, decomp residuals are deterministic functions of ciphertext, correlated with secret t; they cannot be assigned independent Gaussian variance from the code alone. Reuse across queries and adaptive inputs requires a stronger model.
[SPECULATION FOR B005, NOT VALIDATED] Replace deterministic low-bit truncation with independently randomized unbiased rounding at the smallest gadget place, with signed carry as necessary, so each rounded residual is conditionally centered given ACC. Then derive a martingale variance bound for blockwise m_j*eps_j and count true cost/extra randomness. This is not prima facie novel: randomized gadget decompositions occur in FHE literature (for example FINAL: Faster FHE Instantiated with NTRU and LWE, §4.3).
[DECISION] Current blockwise mixed-gadget parameter scheduling alone has no demonstrated performance or novelty gain. B005 should be exactly one cheapest algebraic feasibility falsifier for unbiased randomized centered-lift gadget under 32-bit torus and its interaction with blockwise selector; if it fails or only recreates prior art without benefit, archive P1 and pivot to 2025/1711+2025/1892. Do not start unrelated FHE tracks.

STATUS: PASS_COMPONENT / FAIL_FULL_DFR_CERTIFICATE
RESULT: Signed digit D=64 correct; unsigned remainder remains 2^-21; block-binary ring weight tightens residual; full 2^-128 remains uncertified.
NEXT_TEST: B005 randomized-unbiased decomposition structural correctness/carry/prior art; one minimal falsifier only.
STATE_UPDATE: YES
