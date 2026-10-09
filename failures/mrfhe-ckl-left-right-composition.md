# Archived negative test: MRFHE DFT left multiplication via CKL SinC column encryption

Date: 2026-10-09
Status: NEGATIVE — reject the zero-format-conversion substitution, NOT all CKL/MRFHE compositions.

## Sources / provenance
- Jung Hee Cheon, Minsik Kang, Junho Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, ePrint 2025/1957. Research MCP acquired 32 physical pages, PDF SHA-256 ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a, VERSION_UNVERIFIED. Section 4.1 Theorem 2 pp. 15-16: B+Toep(s)A≈M. Section 4.2 Algorithm 1 p. 17: right plaintext matrix multiplication (B·U,A·U). Section 5.1 Algorithm 3 pp. 18-20: CMT converts between column and row matrix-encryption formats using d automorphism key switchings per conversion in the original power-of-two-ring algorithm.
- Cheon et al., *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, ePrint 2026/853, full 18-page conversation/library PDF. Connected ePrint MCP returned RETRIEVAL_BLOCKED for this ID; do not claim MCP read it. Theorem 5.3, Corollary 5.4 and Proposition 5.5, pp. 9-10: left multiplication by D1 on the canonical U-slot matrix. Algorithm 1 p. 10 and §5 cost analysis p. 11: one PCMM entails two switches over S^(i), where rank_Z(S^(i)) = n1 rank_Z(R^(i)).

## Primary hypothesis / falsification
[HYPOTHESIS, FAILED] Replace MRFHE left-DFT PCMM directly with CKL column-wise SinC matrix encryption's two plaintext matrix multiplications, without ciphertext format changes or key switching.

[DERIVED] For a column matrix encryption B+T(s)A=M, CKL's right multiply is free: BU+T(s)(AU)=MU. But naive left-multiply (LB,LA) decrypts as LB+T(s)LA instead of LM=LB+LT(s)A, leaving mismatch (T(s)L-LT(s))A. To work for all secrets/data by this method, L must commute with all secret multiplication matrices T(s).

[DERIVED] In a cyclic monogenic free module with basis 1,U,...,U^(d-1), any linear map commuting with T(U) is itself polynomial multiplication by an R-element. These maps are diagonal in the canonical evaluation/slot basis, and cannot represent general DFT mixing between slot coordinates. In MRFHE, the desired left multiplication by D1 on slot matrices induces on the U-coefficients the map F_U^{-1} D1 F_U = F_U, since D1=F_U. Thus the desired map is generically not in the secret-multiplication commutant.

[EXACT TOY] Work in q=17, choose i=4 with i²=-1 and U²=i=4; evaluate U at ±2, so F=[[1,2],[1,-2]] mod17. For s=U, T(s)=[[0,4],[1,0]]; F T(s)-T(s) F=[[15,12],[14,2]] !=0. With B=0,A=(1,0)^T the desired F(B+T(s)A)=(2,15)^T, while naive F B+T(s) F A=(4,1)^T. Independently seeded 1000 toy trials: 937 mismatches for naive left operation, 1000/1000 correct for CKL right multiplication.
Reproduction (conversation sandbox): /mnt/data/fhe_audits/mrfhe_ckl_left_right_interface_audit.py .

## Cost/compatibility consequences
- To obtain LM from CKL's right-multiplication interface, a natural hypothetical workaround is transpose (CMT) -> right-multiply L^T -> transpose back (CMT), costing two CMTs.
- In 2025/1957's ORIGINAL power-of-two-ring construction, each CMT requires d key switchings; hence two CMTs cost 2d base-ring key switchings, plus TWEAK/adjust operations. By comparison MRFHE's 2 S^(i) switches have dimension-scaled cost about 2d R^(i) switch units, assuming linear cost in integer rank. This is NOT a concrete timing equivalence and the CKL CMT algorithm has NOT been shown to port verbatim to MRFHE's mixed-radix ring.
- Packing d base ciphertexts back to one extension-ring polynomial is a cheap rearrangement under the shared secret; it is the noncommuting LEFT-linear transform and orientation conversion that cost extra.
- CKL's lightweight CMT may reduce *stored key material*, not automatically the d key-switch operations.
- This does not exclude native row-wise representations, alternative transpose methods, or a future mixed-radix CMT improvement.

## Decision
Status: FAIL for no-conversion CKL substitution; archive this specific branch. Do not claim a correctness flaw in either published paper.
Novelty: NONE for the commutator obstruction itself; it is standard algebra.
Next minimal test (separate hypothesis): Determine whether MRFHE's required right multiplication by D2^T acts on CKL's ciphertext-matrix index or *inside* the coefficient subring CRT slots. If it acts inside the coefficient ring, CKL's free right matrix multiplication still cannot replace the MRFHE S^(ω) ring conversion without changing encoding.
STATE.md is left unchanged because it currently holds a distinct, not-closed RIG research state.
