# BOOT-B013 failure archive: generic GL regular-permutation bridge as a drop-in GSW butterfly replacement

TRACK_ID: BOOT
ITERATION: B013
DATE: 2026-10-19
STATUS: PARKED_NONCOMPETITIVE_BRIDGE (not a universal impossibility result)

The cyclic permutation representation z ↦ P^z is a valid additive-group homomorphism. GL 2025/1935 integer branches satisfy P^+ = n^-1 U^+ (V^-)^T, P^- = n^-1 U^- (V^+)^T. With U^±=P^a,V^+=P^b,V^-=(P^b)^T, one native ct-ct GL multiplication *at the plaintext matrix level* produces both P^(a+b) and P^(a-b) up to public normalization. Verified 25/25 pairs for p=5,n=8,t=97,p_aux=3, and 36/36 pairs p=41,n=64,t=769,p_aux=3 by independent exact integer matrices. Source-root congruence t≡1(mod4 n p_aux) passes. No encrypted computation/DFR/security benchmark.

This DOES NOT supply a cheap bridge from 2025/696: original encrypted exponent inputs are GSW(X^-z) over the circulant ring Z_Q[X]/(X^p−1), and the outputs of Algorithm 3 also require GSW ciphertexts under the original key. No secure efficient conversion to/from n-matrix GL ciphertexts is supplied by either source. For prime p=41 any faithful *permutation* representation requires dimension >=41, thus GL's power-of-2 matrix size >=64. Full n=64,p_aux=3 integer GL ciphertext contains 4n²φ(p_aux)=32768 ring-coefficient coordinates vs an illustrative rank-one GSW ciphertext with 4 d p =492 coordinates for p=41,d=3. Even fully packing GL's four integer matrices gives >=8192 coordinates per represented matrix, ~16.65x nominal coefficient count. Comparisons are NOT matched moduli, bytes, noise, security, or actual performance. GL ct-ct uses four coefficient-matrix multiplications plus two Switchbig keys and level/noise, not a free homomorphic dot product.

Prior art directly kills novelty for cyclic permutation bootstrapping: Alperin-Sheriff & Peikert (CRYPTO 2014), ePrint 2014/094 Sec2.2; compact circulant representation is explicitly recognized. Liu & Li (2023), arXiv:2310.12441, use monic monomial permutation matrices in large-plaintext functional bootstrapping. Group ring f(X)->f(P) already compresses a circulant matrix to p coefficients, so converting to generic dense GL matrices throws away the native compression. The exact GL +/- layout may be a mathematical combination, not a demonstrated publishable algorithmic improvement.

Decision: archive this specific noncompetitive conversion-only bridge; do NOT assert all permutation-matrix FHE hybrids impossible. Reopen only if a new compressed ciphertext conversion plus security/noise/cost theorem genuinely beats GPvL/Paiva and prior MMPM constructions at matched parameters.

Primary technical evidence: findings/boot-B013-regular-permutation-matrix-bridge-and-cost-gate.md.
NEXT_ACTION: B014 test a SAME-RING interface: 2025/686 MPmul rank-one RLWE/GSW CMUX versus 2025/1711 squared-gadget rank k=r=1 Mat-MGSW external product, first algebraic/noise and modulus gating.
