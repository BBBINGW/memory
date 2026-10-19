# BOOT B017 failure archive — Naive MPmul difference digit hoisting

TRACK_ID: BOOT
ITERATION: B017
DATE: 2026-10-19
STATUS: FAIL_NO_TRANSFORM_REDUCTION / DENSE_CARRY
PRIMARY HYPOTHESIS: Form FFT(D(c_{j-s}))-FFT(D(c_j)) instead of FFT(D(c_{j-s}-c_j)), exploiting predecomposition of all n input ciphertexts each MPmul bit stage to reduce the number of expensive transforms.

Falsifiers:
1. Source 2025/686 uses FBS1/FBS2 ell_A=1, 64-bit Q, base 2^23 or 2^22. Actual author code src/mosfhet/src/polynomial.c polynomial_decompose_i (called by src/mosfhet/src/trgsw.c rank-one external product) uses **nearest rounded** centered single digit D(x)=((x+2^63+G/2)>>log2 G modB)-B/2, G=Q/B. It is nonlinear: at a=G/4,c=-G/4 modQ, D(a)=D(c)=0 but D(a-c)=1.
2. D(a-c)=D(a)-D(c)+kappa mod B, kappa in {-1,0,+1}. Uniform 64-bit reference samples, 1,048,576 word pairs for each parameter: nonzero kappa 25.0081% for base2^23 and24.9408% for base2^22; signed digit wrap outside centered range ~25% in each. Worst case correction can have all N coefficients nonzero, so not a sparse FFT correction. Without correction, the ideal independent rounded residual difference has 2x the variance of standard freshly rounded residual; do not equate this illustrative variance to actual FHE DFR.
3. Direct 2025/686 main loop src/sparse_amortized_bootstrap.c does trlwe_sub, rank-one trgsw_mul_trlwe_DFT, inverse FFT, add. For n distinct source ciphertexts and n destination differences, naive input hoist still computes 2n forward transforms and 2n inverse transforms per stage (rank-one two-component ciphertext), SAME as baseline (ignoring additional automorphism). Exact FFT(kappa) per output adds work. Next bit stage ciphertexts change, preventing free cross-stage cache reuse.

Very important 2026 prior art: Li et al., "BatchBoot", USENIX Security 2026, official full paper https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf Section4.1 Eq8, Table2: implements DIFFERENT multi-bit CMUX plus parameterized external-product / automorphism FFT hoisting directly optimizing 2025/686. Authors report 2.4x faster than 2025/686. This supersedes novelty claims for generic FFT-hoisting in MPmul and supplies a concrete source to learn from. B016's restricted rank3 scalar-product argument never forbade BatchBoot's changed multi-bit key/FFT-vs-Hadamard pipeline.

Result: Archive only THIS difference-digit preprocessing shortcut, not other well-defined source hoists; no native benchmark, no claimed new performance/security/DFR.
TECHNICAL_EVIDENCE: findings/boot-B017-mpmul-singlelevel-digit-hoisting-carry-fft-gate.md.
NEXT_TEST: B018 verify true d=1 baseline against BatchBoot's official δ=2 FFT/Hadamard/BSK tradeoff; look for an unaddressed technical bottleneck, not repeat published optimization. BOOT file isolation preserved.