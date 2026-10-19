# BOOT-B002 — Block-Binary Key Noise vs Heterogeneous Gadget Variance

TRACK_ID: BOOT
ITERATION: B002
DATE: 2026-10-19
STATUS: FAIL (naive variance/DFR transport); PASS (restricted algebraic interface and toy falsifier)
NEXT_TEST: B003 — bounded-noise, source-faithful Pareto comparison with real block-binary parameters
STATE_UPDATE: YES

## Primary hypothesis
[HYPOTHESIS] The heterogeneous gadget/approximate decomposition formula from Hong–Lee ePrint 2025/1892, Theorems 3.1–3.2, can be substituted per block into Lee–Min–Seo–Song ePrint 2023/958, Algorithm 2, and its scalar sum-of-per-operation noise variance can be used without modification to forecast bootstrapping failure probability.

## Provenance / source scope
[FACT] 2023/958 physical page 11, Algorithm 2 and Lemma 1; physical pp. 15–16, FFT and scalar multiplication cost analysis / Table 2 (web ePrint pdf 0-index pp. 10, 14–15). Reference: https://eprint.iacr.org/2023/958.pdf, mirror PDF SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de.
[FACT] 2025/1892 physical pp. 10–13, failure probability model and Theorems 3.1–3.2. Reference: https://eprint.iacr.org/2025/1892, mirror PDF SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018.
Both mirrored versions VERSION_UNVERIFIED; formula extraction may be imperfect. All new formulas below are explicitly independent derivations in a simplified noise model; not asserted as theorems of either paper.

## Structural compatibility
[DERIVATION] In block I_j with at most one nonzero secret coordinate, let P_a = (X^a - 1), and C_j = sum_{i in I_j} P_{a_i} TRGSW_{G_j}(s_i). A single common gadget G_j must serve all TRGSW rows combined inside the block, otherwise matrix addition is undefined without conversion. Different blocks may use different G_j because the accumulator is re-decomposed at each step. This is an algebraic interface, NOT a noise/security/performance theorem.

[FACT] Algorithm 2 of 2023/958 uses one external product per block but a sum of all TRGSW ciphertexts in the block. It is therefore false to count only the active secret index as contributing fresh key-error. The Lemma 1 bound already scales with n=ell*k rather than only k for the TRGSW noise term.

## Minimal toy falsifier — an inactive selector still contributes noise
[DERIVATION] Work over the real negacyclic ring R=R[X]/(X^4+1), and use one independent Gaussian error polynomial per secret coordinate, coefficient variance beta^2, in a single-row linearized TRGSW noise model (gadget coefficient 1). Take secret s=(1,0) and public exponents a=(0,4). Then
    sum_i (X^{a_i}-1)e_i = (X^0-1)e_1 + (X^4-1)e_2 = -2e_2.
The secret coordinate for e_2 is zero yet its error remains. The output coefficient has variance 4 beta^2. This shows that 'one external product' does not mean 'one error source'. It does not refute 2023/958.

## A stronger falsifier — unconditional variance does not fix the tail
[DERIVATION] For one independent Gaussian error polynomial e with variance beta^2 per coefficient and a uniform over {0,...,7}, let Z=[(X^a-1)e]_0. The conditional variance multiplier V_a/beta^2 is exactly [0,2,2,2,4,2,2,2]. Its mean equals 2. The exact unconditional Gaussian-mixture tail is
P(|Z|>t) = (6/8) erfc(t/(2 beta)) + (1/8) erfc(t/(2 sqrt(2) beta)).
Using N(0,2 beta^2) instead gives erfc(t/(2 beta)), different in general.
At t=5 beta: exact 0.0018576303; mean-variance Gaussian 0.0004069520; ratio approximately 4.5647. At 6 beta: exact 0.0003540424 vs 0.0000220905; ratio 16.0269.
[CONCLUSION] Naively substituting an unconditional additive scalar variance into one Gaussian error function is NOT an exact DFR calculation for this block-key noise model. This is a toy model only: neither a concrete TFHE DFR estimate nor a contradiction to the correctness/security claims of either cited paper.

## Conditional, source-faithful noise expression (new derivation)
Let T_a be the signed negacyclic permutation matrix for multiplication by X^a. Let P_a=T_a-I. At block j define h_{j,r} as its 2d_j gadget-digit polynomials of ACC_j and E_{i,r} as independent, coefficientwise zero-mean Gaussian TRGSW key errors of variance beta_j^2. Ignoring approximation-residual terms for the moment,
    z_j = sum_{i in I_j} sum_{r=1}^{2d_j} h_{j,r} * P_{a_i} * E_{i,r}.
Conditioning on the pre-block transcript F_j and public exponents a, all E_{i,r} for fresh, non-reused keys of block j are independent of F_j. For a fixed output coefficient row rho (including deterministic monomial rotations following block j),
    Var(rho z_j | F_j,a,s) = beta_j^2 sum_{i in I_j} sum_{r=1}^{2d_j} || rho M(h_{j,r}) P_{a_i} ||_2^2.
Here M(h) is the negacyclic convolution matrix. The formula depends on a_i and on the actual adaptive gadget digits h_{j,r}; it is not in general a function only of d_j, B_j, and beta_j.

If ||h_{j,r}||_infty <= D_j, then ||rho M(h_{j,r})P_{a_i}||_2^2 <= 4 N D_j^2, since T_a is orthogonal and ||P_a||_op<=2. Thus per-output-coefficient
    Var(rho z_j | F_j,a,s) <= 8 beta_j^2 ell_j d_j N D_j^2.
For the sum of rotated fresh independent key errors across blocks, a predictable-variance Gaussian-martingale tail bound gives P(|sum_j rho_j z_j|>t) <= 2 exp(-t^2/(2 V)) with V=sum_j 8 beta_j^2 ell_j d_j N D_j^2. This requires fresh independent Gaussian errors and an a priori bound on adaptive decomposition digits. It does not incorporate approximate-gadget rounding/residual, key switching, mod switching, or correlated/reused keys.

If a deterministic total bound R for all gadget approximation/rounding errors can separately be established, then P(|noise_BR|>T) <= 2 exp(-(T-R)^2/(2V)) for T>R, under the same assumptions. Conservative (potentially much too weak), not an exact DFR formula. With approximate decomposition, R must be re-derived rather than copied from the exact-decomposition Lemma 1 of 2023/958.

## Cost accounting
[FACT] 2023/958 Table 2 reports uniform-d block-binary FFT count (2d+2)k and scalar multiplication count (4d+2)nN (excluding other overheads).
[DERIVATION] For per-block lengths d_j and sizes ell_j, a first structural estimate is
    FFT ~= sum_j(2d_j+2),    scalar-mults ~= N sum_j ell_j(4d_j+2),    BRK size proportional to sum_j ell_j d_j.
This is NOT a benchmark, and differs from the NTT-based 2025/1892 cost environment. Any optimization must compare against the 2023 block-key code and include key-switching, transforms, memory, security, and actual noise.

## Decision
[RESULT] FAIL the proposed drop-in transfer of a scalar variance/erfc DFR expression. PASS the single-gadget-per-block algebraic shape check. Corrected research interface: optimize a risk-constrained blockwise schedule using a conditional covariance model or a rigorously bounded tail, accounting explicitly for every noisy key in a block. Main blocker is developing useful (not vacuous) DFR bounds after approximate decomposition and adaptive ACC digits.

## NEXT_TEST B003
Read 2023/958 implementation details / Table 2 and 2025/1892 Theorem 3.2 + Appendix B; use 2023 real n,N,ell,noise parameter configurations, source-derived gadget formats, and compare uniform per-block d vs mixed d schedules under conservative, independently checked bounds. Kill this direction if bounds make any apparent gains disappear. Examine concrete prior art on blockwise gadget mixing, and only then claim novelty. Keep unrelated tracks untouched.
