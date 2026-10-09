# MRFHE W-axis DFT vs CKL native right CPMM — direct composition fails

Archived: 2026-10-09
Status: NEGATIVE (zero-switch, pure-reindexing composition only)
Primary question: Can the W-slot-axis action M -> M D2^T in MRFHE ePrint 2026/853 be effected as the native matrix-column right multiplication of Cheon–Kang–Lee's SinC matrix encryption (ePrint 2025/1957), without new switching / ciphertext-format conversion?

## Sources / evidence
- [FACT] MRFHE (Cheon et al., 2026/853), Section 5.2 Corollary 5.4: slot matrix Psi(m) in C^{n1 x n2} is multiplied on the right by D2^T, transforming W-slots **within each ciphertext**. Algorithm 2 performs an auxiliary-ring conversion and PCMM to implement this action. Source basis: existing conversation PDF 2026-853.pdf, 18 physical pages. MCP get_eprint_paper(2026/853) previously blocked; do not claim that MCP fetched it.
- [FACT] CKL 2025/1957 Theorem 2 and Algorithm 1, MCP-read physical pages 15-17: B+Toep(s) A ≈ M, with each matrix column being one separate RLWE ciphertext. The native free ciphertext/plaintext PPMM yields (B P, A P), i.e. M P. CKL Section 5.1/Algorithm 3 (pages 18-20) requires relative traces and Galois automorphisms / key switches to transpose the ciphertext matrix.
- CKL source ePrint ID 2025/1957; MCP SHA-256 ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a, VERSION_UNVERIFIED.

## Decisive test / algebra
[DERIVED] Treat the W-axis as a module direction. K ciphertexts give B+T_W(s)A=M with n2 rows (within-ciphertext W coefficients) and K columns (ciphertext index). CKL's native PPMM is M P, P in Mat_K. To apply W-axis L in Mat_{n2}, the desired output is L M. Directly applying L to both ciphertext parts decrypts as LB+T_W(s)LA, whereas L M = LB+L T_W(s) A. Necessary and sufficient condition is [L,T_W(s)] = 0.

On W-slot evaluations, T_W(s) is diagonal diag(s_0,...,s_{n2-1}). For MRFHE L=D2 on column slot vectors (equivalent to M -> M D2^T on row slot matrices); each D2 entry is a root of unity and thus nonzero. Hence [L,diag(s)]=0 iff all s_j are equal (within each fixed U row). A generic secret with W-dependence violates this. A restricted W-constant secret may satisfy it, but changes the key distribution / underlying security and is NOT an unconditional replacement.

[FACT: exact experiment] Minimal legitimate MRFHE shape w2=3,w3=1,n1=2,n2=6, q=73. Let eta=2 of order 9 and W-embedding roots eta^{1,4,7,8,5,2}. For secret s(W)=W and noiseless zero encryption a(W)=1, b(W)=-W, correct L(b+as) is 0. Applying L to a and b separately, then decrypting under the same s, yields slot vector [31,53,41,72,37,5] != 0 mod73. The same test verifies CKL's native matrix-right action B P + T(s)(A P)=(B+T(s)A)P for 300 seeded random cases.
Reproducible artifact: /mnt/data/fhe_audits/mrfhe_ckl_waxis_interface_audit.py.

## Interpretation
- [NEGATIVE] The W-slot dimension is a row/module direction inside each RLWE ciphertext, NOT the separate-ciphertext column dimension on which CKL's free right multiplication acts.
- Transposing the plaintext matrix is not simply a free ciphertext reindexing: column encryption under T(s) turns into row encryption under T(s)^T. Restoring the target orientation requires a nontrivial transformation (e.g. a CMT mechanism) with security/noise/cost that must be accounted for.
- CKL's concrete CMT is analyzed for power-of-two negacyclic rings; MRFHE is mixed-radix cyclotomic. Extension of that specific algorithm is not established here. The auxiliary ring conversion in MRFHE should not be equated automatically with a key switch or assumed costly.
- The toy secret s(W)=W and q=73 are algebraic counterexamples, NOT claims about 128-bit deployment parameter security or a sampled full-Hamming-weight secret.

## Decision
Archive this restricted *zero-key-switch direct CKL right multiplication* composition hypothesis. It is NOT a proof of an impossibility bound against alternate ciphertext formats / new keys. No novel practical speedup has been obtained.

Next smallest test if pursuing a different assumption: Is the W-constant secret needed to force commutation cryptographically equivalent to a smaller-degree RLWE instance? Test via a subring projection/restriction before proposing special-secret CKKS optimization.
