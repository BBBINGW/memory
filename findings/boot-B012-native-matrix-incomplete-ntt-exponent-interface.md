# BOOT-B012 — Native Matrix Arithmetic versus Incomplete-NTT Exponent Linear Maps

TRACK_ID: BOOT
ITERATION: B012
DATE: 2026-10-19
STATUS: FAIL_DROPIN_PTCT_MATRIX_SUBSTITUTION / PASS_EXACT_SOURCE_GROUNDED_ALGEBRA
STATE_UPDATE: YES

## Primary hypothesis and cheapest test

[HYPOTHESIS] The native plaintext–ciphertext matrix multiplication of Gentry–Lee (2025/1935) can directly implement one 2×2 butterfly (and thus the two-part inverse incomplete NTT) of Paiva et al. (2025/696) on the ALREADY AVAILABLE input evaluation keys Zi, reducing homomorphic dot products, without introducing a new ciphertext representation or a costly conversion.

[CHEAPEST TEST] Compare the actual source input/output plaintext types. If two exponent-encrypted inputs have plaintext X^{-z1}, X^{-z2}, does applying the public 2×2 butterfly H=[[1,1],[1,-1]] as ordinary matrix linear arithmetic yield X^{-(z1+z2)}, X^{-(z1-z2)}? Construct a noiseless ring counterexample and a finite-difference impossibility proof for affine maps.

## Provenance and source limits

[FACT] Gentry–Lee, "Fully Homomorphic Encryption for Matrix Arithmetic", ePrint 2025/1935, physical PDF pp. 1,5–6 (overview/ring), 9–10 (Sec.3.1, 3.2 matrix-encoded ciphertext type), 12–13 (Theorems 3.5/3.6 trace formula), 16 (Sec.3.6 plaintext–ciphertext matrix multiplication), 18–20 (Sec.4 BGV-like integer matrices). Cached PDF identity verified, version UNVERIFIED, SHA256 985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84. Scheme plaintext space R'_t = Z_t[i][X,Y,W]/(X^n-i,Y^n-i,Phi_{p_aux}(W)), encoding n×n matrices; ciphertext is n separate RLWE ciphertexts in R_q, with secret s(X,W) independent of Y; pt-ct matrix multiplication uses native trace/matrix arithmetic, which is linear in the encrypted numerical matrix input for public other operand.
[FACT] Paiva et al., "Faster amortized bootstrapping using the incomplete NTT for free", ePrint 2025/696, physical pp. 4–5 (circulant ring/GSW), 11–15 (two-part incomplete INTT matrices, Section 4.2, Algorithm 3). Cached PDF identity checked, version UNVERIFIED, SHA256 100140416417ad19daf56cc556713ce29d30c68780a9009d7d6234d36f68f85a. In Algorithm 3, public N×N matrix X = M_A A, and M_B, act on an exponent-encoded secret transform vector zhat in Z_p^N: INPUT Zi are *GSW encryptions of X^{-zhat_i}* in a circulant ring Rtilde_Q=Z_Q[X]/(X^p-1). The homomorphic dot_product with public row u returns GSW encryption of X^{-<u,zhat>}. The two parts are homomorphic dot products, not ordinary plaintext-linear arithmetic on ciphertexts encrypting numerical zhat_i.
[QUALITY] IACR PDF URLs returned 403 through web; physical page text read through Research MCP from authenticated-title GitHub mirrors, versions not verified, equations should undergo visual PDF checks when official PDFs accessible. Some parsed math symbols garbled; core monomial/exponent relationship cross-checked in two source locations. No native code benchmarks.

## One decisive zero-noise test

[DERIVATION] Drop the global exponent sign to simplify notation; replacing z by -z changes nothing. Let H=[[1,1],[1,-1]], input z=(1,1) ∈ Z_41^2. Required output in exponent representation:
    (X^(z1+z2), X^(z1-z2)) = (X², 1).
Plaintext matrix application on the already-encoded monomial vector (X,X) instead gives:
    H · (X,X)^T = (2X,0)^T ≠ (X²,1)^T.
This discrepancy occurs in the coefficient ring before encryption, without noise, rounding, key switching, or implementation constraints. It cannot be repaired by merely choosing gadget/key sizes.

[GENERAL DERIVATION] Let S=Z_(2^16)[X]/(X^41−1). For a,b∈Z_41 define F(a,b)=X^(a+b mod41) ∈ S. Any affine map of separately monomial-encoded inputs A(X^a)+B(X^b)+c is additively separable in (a,b), so its mixed finite difference must vanish. But
    F(a+1,b+1)−F(a+1,b)−F(a,b+1)+F(a,b)
       = X^(a+b) (X−1)^2
       ≠ 0 in S
for every a,b, as (X−1)^2=1−2X+X² is a nonzero degree-two polynomial in the quotient, and X is invertible (X^41=1). Consequently a single ordinary plaintext-linear/affine matrix operation over the input exponent monomial components CANNOT implement source homomorphic_dot_product for arbitrary secret z.
[TEST] Independent exact integer arithmetic over Z_65536 group ring: checked all 41²=1681 mixed differences, 1681/1681 nonzero with exactly 3 nonzero coefficients, including wrap modulo X^41−1. Also directly checked H·(X,X)=(2X,0) versus desired (X²,1). PASS. This is a noiseless plaintext/ciphertext-type incompatibility proof, not a security attack and not native FHE.

## Not merely incompatible number theoretic moduli

[DERIVATION/source parameter check] Use incomplete-negacyclic ring with N=8, ell=1, prime p=41. Then p−1=40 divisible by 2N/2^ell=8 but not by 2N=16; it supports the relevant incomplete NTT, not the complete one. Meanwhile Gentry–Lee BGV-style integer native matrices of size n_mat=2 with auxiliary odd p_aux=5 can use plaintext modulus t=41, as t−1=40 divisible by 4 n_mat p_aux=40 (Sec. 4.1). Therefore source-relevant 2×2 integer matrix arithmetic can exist at the SAME numerical plaintext prime 41 in an independent encryption design, yet the exponent-vs-numeric incompatibility above persists. This isolates the actual interface obstruction.

[SECONDARY OBSERVATION, NOT primary falsifier] If one instead tries to natively encode the FULL 8×8 transform matrix with n_mat=8, same p_aux=5, and t=41, the required t≡1(mod 4n_mat p_aux)=1(mod160) fails, as does even the weaker primitive-32nd-root requirement (40 not divisible by32). Shrinking matrices to n=2 blocks may avoid this root requirement but requires data-layout and encryption/interface redesign. It is false to assert that ALL incomplete NTT parameter moduli are incompatible with ALL GL matrix dimensions.

## Cost and correctness implications

[FACT] 2025/696's base multiplication is ALREADY absorbed into the first 2-part INTT; at ell <= log2 N−alpha, the matrix X=M_A A has the same block sparsity and O(N²/2^alpha) coefficient-linear work as M_A, while M_B adds O(N 2^alpha). Merely writing these public matrices in 2025/1935 matrix-encoding form does not reduce the number of exponent-domain GSW dot products; they are a different primitive.
[FACT] 2025/1935 pt-ct matrix multiply is linear on NATIVE matrix-encrypted numerical entries; 2025/696 outputs GSW monomials X^{z'_j}, needed for later partial decryption, automorphisms and extraction. It is not legal to reinterpret a GSW monomial ciphertext over circulant Rtilde_Q as a Gentry–Lee RLWE matrix ciphertext over cyclotomic R'_q (different plaintext, ciphertext dimensions/rings/secrets and evaluation keys).
[DERIVATION] A prospective redesign could (i) encrypt actual zhat_i as BGV-like GL matrix entries at BSK generation time, (ii) perform linear inverse-NTT as pt-ct native matrix arithmetic, (iii) convert the resulting encrypted integers back into circulant-GSW monomial ciphertexts X^{z'_j}. Steps (i) and (iii) change BSK structure, security assumptions and noise, and (iii) is nonlinear in z and NOT supplied by either source. Without a proven inexpensive exact/approximate conversion including ciphertext modulus/t and key switching, no end-to-end latency/key-memory gain follows. Mat-Mat ciphertext multiplication or regular representation P^z may emulate exponent addition algebraically, but it is not an immediate pt-ct linear replacement and may entail large rank/relins/levels. No lower bound on all possible bridges is claimed.
[UNCLEAR] Cost of conversion, joint security in altered key distributions, DFR, ciphertext scale/modulus matching, matrix dimension/root constraints, and actual implementation all remain unproven. No benchmarks or performance percentages claimed.

## Research decision
STATUS: FAIL_DROPIN_PTCT_MATRIX_SUBSTITUTION / PASS_ALGEBRA.
RESULT: Structural operation mismatch: regular linear transform on encoded monomials is not exponent-encoded linear transform; even when a compatible 2×2 plaintext modulus exists. A direct speedup replacing homomorphic_dot_product by GL pt-ct matrix multiply is invalid. Theoretical hybrid requires a new representation/conversion protocol, not merely applying the faster matrix primitive.

NEXT_TEST (BOOT B013): One smallest structural bridge hypothesis: Can a regular representation z ↦ P^z (where P is the p-cycle permutation matrix) let GL-native matrix ciphertext multiplication emulate ONE exponent-domain dot product without more ring operations or key memory than the original GSW homomorphic_dot_product? First seek rank/dimension and key-format obstruction for p=41 and n_mat power-of-two, along with a p=5 two-input toy; if overhead unavoidable under the proposed bridge, archive it and pivot to a different BOOT subtopic. Never assume the regular representation is the only possible bridge. Do not inherit other tracks' NEXT_ACTION.
END: STATUS FAIL_DROPIN_PTCT_MATRIX_SUBSTITUTION; NEXT_TEST B013; STATE_UPDATE YES.
