# MRFHE CRT-packed EvalMod: no free relinearization gain (restricted model)

Date: 2026-10-09
Status: NEGATIVE / ARCHIVE THIS DIRECT CONSTRUCTION
Baseline: Cheon et al., "MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping", IACR ePrint 2026/853, Algorithm 3, lines 3-6 (individual EvalMod after batched CtS).
Source provenance: PDF full text from conversation file "2026-853.pdf" (18 pages); connected MCP get_eprint_paper(2026/853) returned RETRIEVAL_BLOCKED on 2026-10-09, so do NOT claim that MCP retrieved this full paper.
Previous hypothesis: CRT packing in extension ring S=R[V]/(f), with secret s in R, makes nonlinear polynomial evaluation component-wise in CRT slots. A toy exact proof/test survived. However, a single extension-ring EvalMod is not necessarily faster than K base-ring EvalMods.

## Primary test

[DERIVED] Under coefficientwise base-ring gadget decomposition and the same evaluation key EK_j=(B_j,A_j) in R^2 encrypting g_j s^2 under s,
  c2(V) = sum_{k=0}^{K-1} c2,k V^k
  h_j(c2(V)) = sum_k h_j(c2,k) V^k
  Relin_S(c2(V)) = sum_j h_j(c2(V))*EK_j
                 = sum_k V^k Relin_R(c2,k).
This is an exact identity over S; nonzero switching-key errors are retained.

[NEGATIVE] Each of L gadget digits must multiply two R-valued switching-key polynomials at K coefficients. Direct cost = 2 K L R-polynomial products, exactly the same as K independent R-relinearizations. Gadget decomposition processes K*dim(R) coefficients per modulus limb. Both methods reuse the same base-ring evaluation key; no automatic K-fold reduction in key material, key reads, R-NTTs, or arithmetic.

[FACT / EXPERIMENT] Reproducible toy script /mnt/data/fhe_audits/mrfhe_evalmod_ks_audit.py uses q=17, R=F17[u]/(u^2+1), S=R[v]/(v^2-u), K=2, gadget [1,4,16] (L=3). 1000 seeded tests passed native S key-switch == K coefficientwise R switches, including nonzero evaluation-key noise. Both used exactly 12 R-polynomial products per relinearization in the chosen direct coefficientwise arithmetic model.

## Limitations
- This does not prove a universal lower bound against every fast algorithm, vectorization strategy, mixed NTT representation, or a different ciphertext format.
- Native S multiplication in a non-CRT coefficient representation can add transform/convolution overhead; concrete NTT timings are not measured.
- The previous CRT algebraic correctness did NOT establish a CKKS scale, noise, or level bound; those remain open independently.
- In the standard SIMD model, slot-wise polynomial evaluation is already a known technique; merely repacking is not novelty.
- The source note concerns EvalMod as a polynomial-operation abstraction, not a complete implementation of approximate modular reduction.

## Decision
Archive this direct CRT-packed EvalMod performance hypothesis: coefficientwise relinearization still costs Θ(K) base-ring work with the standard R evaluation key. Do not claim an actual runtime gain until a specific shared expensive operation is demonstrated and measured.

NEXT: Select a new, independently falsifiable FHE research target; avoid more CRT packing variants without a concrete saved NTT/key-switch/precision term.
