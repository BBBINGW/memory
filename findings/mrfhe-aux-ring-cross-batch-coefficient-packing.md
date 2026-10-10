# Iteration 32: MRFHE cross-batch packing across Y coefficients preserves the W-axis transform

Date: 2026-10-10
Branch: MRFHE (ePrint 2026/853) / previous Iteration 31 unbalanced-radix cost boundary
Status: PASS only for the **algebraic coefficient-independence and conditional operation-count** hypothesis. NOT a proven production optimization; NOVELTY NOT VERIFIED.

## Primary hypothesis and decisive falsification
[HYPOTHESIS] In a W-heavy setting n2>2n1, take K independently formed S^(i) batches under the **same original secret** s(U,W), with K*n1 <= n2/2. Can we concatenate their n1 R^(omega) coefficients into the Y power-basis of ONE S^(omega) ciphertext, apply MRFHE's D2' W-axis batch PCMM, and unpack independent transformed outputs without cross-batch message mixing?

[FAILURE CONDITION] The D2' linear transformation or its masked/Theorem 5.6 composition contains a nonzero off-block map from coefficients indexed Y^(g*n1+j) into Y^(g'*n1+j') for g!=g'. An explicit nonzero cross coefficient refutes the proposed packing as a free batching interface.

## Primary original-paper evidence
[FACT] Cheon et al., *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, IACR ePrint 2026/853, original full text read from ChatGPT Library copy `2026-853.pdf` (18 physical pages, 844,699 bytes). The GitHub Notes ePrint endpoint for this ID was previously RETRIEVAL_BLOCKED and was **not** the source of this PDF.
- §5.1 physical p.9 defines `S^(omega)=Z[omega][W,Y,U]/(W^d-omega,Y^d-omega,U^(2n1)+1)`, d=n2/2, and Theorem 5.2 as the auxiliary-ring batch MM analogue.
- §5.2 physical p.10, Proposition 5.7 states that the D2' *left* matrix action satisfies `psi^(omega)(m'_j) = D2' psi^(omega)(m_j)` **for each Y-power coefficient j**, even though D2' is dense in the W-slot basis.
- §5.2 Theorem 5.6 (physical p.10) and Appendix D.3 (physical p.16) express full W-axis right multiplication using two D2' W-axis actions plus masks depending on U and W automorphism; none requires mixing the separate Y coefficient indices.
- §5 Algorithm 2 physical p.11: (i) one S^(i) PCMM for U-axis, (ii) W -> W^-1 automorphism in S^(i), (iii) coefficient ring conversion and packing into L=ceil(2n1/n2) S^(omega) blocks, (iv) two PCMM operations per S^(omega) block, (v) ring conversion back.
- §5 Cost Analysis physical p.11: 3 S^(i) switches and 4L S^(omega) switches per single n1-batch; `[S^(i):Z]=n1*[R:Z]`, `[S^(omega):Z]=d*[R:Z]`. Base-rank switching is assumed linear in Z-rank.
- §5 opening (physical p.8) discusses batching `min{n1,n2/2}` ciphertexts and §6.3 (physical p.12) uses n1 batches for reported experiments. The multi-S^(i)-batch Y-concatenation tested here is an interface extension, **not an implementation shown in that text**.

## Derivation: packing correctness without restricting W-dependence of secret
[DERIVED] Let c_g in (S^(i)_q)^2 encrypt `m_g = sum_(j=0)^(n1-1) m_(g,j)(U,W) V^j`, with all c_g under the *same* original key s(U,W) in R^(i), which is allowed to depend on both U and W.

For g=0..K-1, transform each coefficient polynomial via the public ring presentation isomorphism R^(i) -> R^(omega), keeping the full s and error representation (not the archived W-independent special-key assumption).

Define joint auxiliary-ring ciphertext components:
`A(W,Y,U)=sum_(g,j) tilde a_(g,j)(W,U) Y^(g*n1+j)`,
`B(W,Y,U)=sum_(g,j) tilde b_(g,j)(W,U) Y^(g*n1+j)`.
Because the same secret tilde s(W,U) has **no Y dependence**, 
`B+A*tilde s=sum_(g,j) (tilde m_(g,j)+tilde e_(g,j))Y^(g*n1+j)`
in S^(omega)_q. No Y power wraps since K*n1<=d.

Let `T_D` denote the ideal plaintext transformation associated to the D2' PCMM of Proposition 5.7. By its theorem statement and Lemma D.1, for `M=sum_j f_j(W,U)Y^j`,
`T_D(M)=sum_j T_D(f_j)Y^j`.
The dense D2' acts on the internal W evaluation direction, NOT on the ciphertext-batch index j. The U-dependent masks and W inverse automorphism in Theorem 5.6 likewise leave Y exponent unchanged. Thus cross-batch **plaintext** interference is mathematically zero, conditional on common key and the stated ring-conversion interface.

All original plaintext coefficients can be reconstructed by extracting Y-power coefficients after the PCMM and re-grouping them into K distinct S^(i) ciphertexts. This is a public coefficient-layout operation, not logically a secret-key switch. It does require data movement and cannot be counted as literally zero CPU/memory cost.

## Exact finite-field minimal verification
[FACT/EXPERIMENT] Reproducible script `/mnt/data/iteration32_auxiliary_batch_audit.py`, fixed seed 20261042, no floating-point arithmetic. q=433 prime; q-1=432 is divisible by 216=3N for N=72, with w2=3,w3=2,n1=2,n2=18,d=9. Primitive generator 5, omega=198 order3, eta=17 order27, rho=354 order8. Ring R_q^(omega)=F433[W,U]/(W^9-omega,U^4+1), S_q^(omega)=R_q^(omega)[Y]/(Y^9-omega). Two groups of two messages each occupy Y^0,Y^1 and Y^2,Y^3; Y^4..Y^8 are zero.

Construct four arbitrary message coefficients and their toy RLWE ciphertext components under the SAME arbitrary full s(W,U), and verify B + A*s = M by exact quotient-ring multiplication. Evaluate every message at 9 W roots and 4 U roots. Apply explicit invertible 9x9 D2' W-Vandermonde for every Y root, then recover every Y coefficient by 9x9 modular Vandermonde inverse.

Results: 144/144 explicit shared-secret decryption/evaluation checks pass; 4,374/4,374 individual Y-coefficient noninterference checks pass (includes 50 additional randomized matrices); all unused Y^4..Y^8 coefficient slots remain zero after W transform. This experiment directly tests plaintext coefficient algebra and basic encryption relation. It does **not** implement homomorphic PCMM (including conjugation and switching), actual RingConv, CKKS rescale, key-switch noise, or latency.

## Conditional operation count
[DERIVED] With K independent n1-batches jointly in ceil(K*n1/d) auxiliary blocks, the baseline generalized switching-equivalent count is
`3 K n1 + 4 d ceil(K*n1/d)`
in R^(i)-switch units. Per original R^(i) ciphertext:
`C_K=3+(4d/(K*n1))*ceil(K*n1/d)=3+(2n2/(K*n1))*ceil(2K*n1/n2)`.
If K*n1<=d, exactly one block:
`C_K=3+2n2/(K*n1)`.
For n1=2,n2=18: K1=>21, K2=>12, K3=>9, K4=>7.5. Maximum K for one block is 4, using 8/9 positions. These are **rank-linear switching-equivalent counts**, not total CPU time. Compared to K=1, K=2 reduces this model's amortized count by 42.857%; K=4 by 64.286%.

The cost reduction is contingent on availability of K independent SAME-KEY batches, unchanged auxiliary switching-key security, and performing conversions by coefficient-layout changes as in §5. If K must increase with n2/n1, the needed total simultaneous input ciphertexts are Omega(n2), a throughput-vs-batch-size trade-off.

## Critical unresolved issues; no premature contribution claim
[OPEN] Extra occupied Y components might affect actual key-switch decomposition norm, noise correlations, precision, NTT/PPMM cost, memory, or resource overhead; the toy only checks exact plaintext action and shared-secret algebra.
[OPEN] A full homomorphic PCMM / RingConv experiment must verify no cross-batch noise or correctness regression and measure total throughput. Even if correctness passes, the speedup in base-switch-equivalent units need not translate to runtime improvement.
[PRIOR ART] Cheon–Kang–Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, ePrint 2025/1957, cached GitHub Notes primary PDF, physical p.3 §1.1, already emphasizes packing many independent matrices into a common coefficient-ring representation with flexible batch size. MRFHE itself uses a closely related batch MM framework. The conceptual act of fully occupying unused Y coefficients is therefore *likely a straightforward packing extension*, not evidence of novelty. A narrowly scoped literature review found no directly matching MRFHE combined-batch implementation. NOVELTY NOT VERIFIED; no publishable contribution established.

## End of Iteration
STATUS: PASS for no-cross-batch **plaintext** mixing and shared-key packing algebra; HUMAN_REVIEW for whether to spend resources on implementation/noise verification.
RESULT: Earlier proposed dense-D2' cross-batch obstruction fails; Y-axis column indexing survives D2' left multiplication. A conditional generalized C_K cost formula demonstrates how filling multiple n1-batches into S^(omega) can amortize auxiliary PCMM better.
NEXT_ACTION: If the human wishes to continue, implement one exact toy noise-bearing **homomorphic** auxiliary PCMM/keyswitch over q=433 for K=1 versus K=2, keeping the same secret and switching keys, and compare coefficient-level output noise and conversion cost; stop on any correctness or noise failure. Do not claim deployment-level speedups before this.
STATE_UPDATE: NO; the distinct RIG-HE parked state remains in STATE.md, unchanged.
