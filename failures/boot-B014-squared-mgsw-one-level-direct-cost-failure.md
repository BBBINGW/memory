# BOOT B014 failure archive — squared Mat-MGSW does not beat one-level MPmul FBS key by source operation count

TRACK_ID: BOOT
ITERATION: B014
DATE: 2026-10-19
STATUS: FAIL_DIRECT_SINGLE_LEVEL_COST_ADVANTAGE / DO_NOT_KILL_RELAXED_MODULUS_HYPOTHESIS

## Original hypothesis
Directly replace 2025/686 rank-one GSW selector external product with 2025/1711 k=r=1 squared Mat-MGSW at unchanged Q, N, security, DFR, thereby reducing the number of transforms or key-size footprint.

## Decisive source-parameter observation
2025/686 Table 3 (physical p.23) actually uses approximate GSW FBS1 ell_A=1, log2 beta=23, N=2048,Q=2^64; FBS2 ell_A=1, log2 beta=22,N=8192,Q=2^64. Other Table 4 ell_A=12–20 are HW-reducing KSK parameters, not the GSW BSK baseline. A misleading multi-level comparison would be invalid.

2025/1711 Section 3.3 at k=r=1 reports:
  standard GSW ell=1: 4 transforms, 4 pointwise N-ring products;
  squared Mat-MGSW: 4 transforms, 4 pointwise N-ring products, PLUS coefficientwise Q/T rounding.
Source Cor.3.5/Section 4 use Delta Q²<T with Delta>=1: for Q=2^64, T>2^128 (>=129-bit), compared to standard 64-bit Q. Each key is four polynomials of N coefficients. Tight-packed raw coefficient bits squared/standard >=129/64≈2.0156; straightforward 64-bit limb coefficient storage 3 vs1. No *count* savings and expanded modulus, absent other changes.
These are source-model representation and operation-count gates, NOT a proven end-to-end timing lower bound or secure-comparison benchmark. Changing Q,N, T, key compression, optimized kernels or security estimates might change conclusion.

## Positive compatibility (not failure)
Source 2025/686 RLWE phase b−a z maps to 2025/1711 Vec-MLWE phase b+S a with S=−z. One-bit Mat-MGSW(b) acts on the difference c1−c0 and supports ordinary CMUX. Independent exact integer test at N=4,Q=256,T=65537, t=8, S=1+X, random uniform public masks in input ciphertexts and Mat-GSW key with E=0: 2048/2048 selector-bit 0/1 negacyclic CMUX cases valid, max decrypted coefficient error1 < threshold16. This is small insecure noiseless-key test, not native execution. Thus the primitive interface is compatible; only its immediate claimed advantage fails.

## Exception / future gate
2025/1711's basic construction and Lemma3.4 begin with T>Q. The stronger Delta Q²<T is a sufficient analytic regime, not a fundamental algebraic impossibility below Q². B015 may investigate a noise/security/DFR justified parameter region Q<T<=Q² specialized to bit selectors, and must compare real implementation and secure parameter sets against the true ell=1 2025/686 baseline. This is not evidence that such an optimization exists.

Sources: ePrint 2025/686 PDF pp9-12,23-25,33; ePrint 2025/1711 pp10-16,21-23. PDFs version-unverified. Full evidence: findings/boot-B014-squared-mgsw-mpmul-single-level-gate.md.
NEXT_ACTION: BOOT B015, one minimal bound/security gate for reduced T. Do not write other research tracks.
