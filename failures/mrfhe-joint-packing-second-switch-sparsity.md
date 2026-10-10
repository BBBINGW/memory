# Iteration 35 — No sparse Y gadget support at MRFHE auxiliary PCMM's second key switching

Date: 2026-10-10
Status: FAIL for **the specific sparse-YSUPPORT hypothesis**, not for joint packing correctness or original MRFHE. NOVELTY NOT VERIFIED.

## Source and continuity

Read GitHub Notes AGENT.md, STATE.md, `findings/mrfhe-joint-packing-lifted-ks-noise.md` (Iteration 34), `failures/mrfhe-joint-packing-noise-isolation.md` (Iteration 33), and `findings/mrfhe-aux-ring-cross-batch-coefficient-packing.md` (Iteration 32) before this run. STATE.md contains separate parked RIG-HE and is not modified.

[FACT / SOURCE] Cheon et al., *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, ePrint 2026/853. Actual original paper 18 physical pages in the user's Library file `2026-853.pdf`, read §5.1–5.2 physical pp.9–10, Algorithm 1 physical p.10, and Proposition 5.7 (same page). Research MCP acquisition of this ePrint was previously blocked; **not** an ePrint MCP cache claim.

- Auxiliary ring `S^(omega)=Z[omega][W,Y,U]/(W^d-omega,Y^d-omega,U^(2n1)+1)`, `d=n2/2`.
- `star(a)(W,Y,U)=bar(a(Y^-1,W^-1,U^-1))`; involution **swaps W and Y**.
- Algorithm 1: star(ciphertext) -> KS(s* to s) -> `d circledast` plaintext matrix contraction -> KS(s* to s) -> rescale. Only the **second switching's input support**, not rescale, is the decisive test.

## Primary hypothesis and failure condition

[HYPOTHESIS — FALSE] Joint packing with K=1 or K=2 original n1-batches (occupying J=2K distinct Y coefficients) leaves the input to the *second* gadget key switching similarly Y-sparse (at most J active Y coefficients), permitting reapplication of Iteration 34's sparse-input `8280K` lifted switching-error bound unchanged to the second switch.

[FAILURE CONDITION] Produce one legitimate ciphertext with input Y-support J but auxiliary PCMM's second KS input occupying >J (in particular all d=9) Y positions.

## Exact derivation and obstruction

[DERIVED] Consider even one input Y coefficient `a(W,Y,U)=sum_(i=0)^(d-1) a_i(U) W^i` with every a_i nonzero. Then
`star(a)=sum_i bar(a_i(U^-1))Y^-i` (in the appropriate omega coefficient conjugation), and since `Y^d=omega`, `Y^-i=omega^-1 Y^(d-i)` for i>0.
Thus `star(a)` fills *all d Y exponents*, even when original a was supported only in Y^0. However, star mainly permutes W/Y monomial positions (up to omega units/conjugation), so the total active position count can still be bounded by J*d*(2n1) for the **first** switch. Iteration 34's bound could be transferred by counting total active monomial positions, NOT by asserting Y sparsity after star.

The first switching's second component is `a_1=sum_l digit_l(star(a)) * A_l`, where A_l are public pseudorandom/full-ring switching-key components. Even if digit_l(star(a)) is sparse, multiplication by dense A_l makes `a_1` generally dense across both Y and W. The `d circledast` PPMM step gives `a_2` (the input of KS2), which has no general sparse-Y support guarantee. This is independent of whether the key-switch error polynomials are zero and does NOT require constraining the secret to be W-independent.

## Exact toy PCMM intermediate test

[EXPERIMENT] Self-contained reproducible `/mnt/data/iteration35_pcmm_second_digit_support.py`, output `/mnt/data/iteration35_pcmm_support_results.txt`. Adapted the fully finite-ring tested source from Iteration 33 and inspected actual PCMM intermediate ciphertexts:
- w2=3, w3=2; n1=2,n2=18,d=9; q=101089 prime, q-1 divisible by 216, G=16, 5 balanced gadget levels;
- both roots of omega are retained simultaneously (finite-field CRT representation of Z_q[omega]), full common secret s=W+U;
- K=1 has two source Y coefficients, K=2 has four; SAME input coefficients for the common two, SAME switch key and secret;
- first KS has *zero switching-key error* to isolate the ciphertext-component support phenomenon. Execute actual star, polynomial gadget switching, and D2' `circledast` PPMM from Algorithm 1, then inspect the actual input to KS2 and its balanced gadget digits. All relevant decrypt-equals-target modular identities are asserted.
- exact locations count a pair over Z_q[omega] as one W,Y,U position; total positions d*d*2n1=9*9*4=324.

Results:
`K=1: source Y 2/9; KS1 input Y 9/9, monomial positions 72; KS2 input Y 9/9, monomial positions 324; KS2 digit nonzero in 648 omega-CRT field coordinates.`
`K=2: source Y 4/9; KS1 input Y 9/9, monomial positions 144; KS2 input Y 9/9, monomial positions 324; KS2 digit nonzero in 648 omega-CRT field coordinates.`
Therefore the proposed second-switch sparse-support assumption fails under the tested normal full-ring switching keys.

This is a q-modular **support test**, NOT lifted total-noise experiment or production key-generation/noise implementation; neither switching-key error nor rescaling was included in the support audit. We do not infer Gaussian magnitudes from modular coefficients.

## Conditional isolated KS noise bounds and their proper interpretation

[DERIVED] In exactly Iteration 34's model (omega-pair digits in [-8,7], switching-key error omega-pair coefficients in {-1,0,1}, L=5, monomial product coefficient bound 23), for a switch whose gadget digits occupy M out of 324 possible W,Y,U locations, a conservative coefficient bound is `23*5*M`. 
- KS1 after star: total M<=2K*9*4 gives `B_1<=8280K` (8280 for K=1, 16560 for K=2). This is a reinterpreted support-count argument, not preservation of Y-sparsity.
- KS2 can have M=9*9*4=324 for either K, so `B_2<=37260` in the same toy switching-key-error distribution, not `8280K`.
- q/2=50544.5. EACH isolated bound B1 for K<=2 and B2 is below q/2. But adding B1+B2 is **NOT a correctness/no-wrap bound** for a full PCMM: the first error undergoes `d circledast` with potentially large coefficient amplification, and there is rescaling plus input encryption error. A purely formal sum ignoring transformation is 45540 for K=1 and 53820 for K=2, and is expressly NOT the total PCMM noise.
- A full second-switch input does NOT automatically imply that K2 has more *second-switch* noise than K1: they may already be dense at K1. That is the opposite of naively applying a K-proportional sparse bound to KS2.

## What survives and what is rejected

[NEGATIVE] Cannot inherit a sparse-Y noise model across the complete auxiliary PCMM. In particular using `B2=8280K` simply by pointing to the original packed Y support is invalid.
[SURVIVES] Iteration 32 message noninterference and conditional switching-equivalent arithmetic count; Iteration 34's **single isolated switch** bound under its stated monomial-count hypothesis; the possibility that some sufficiently large q/noise budget allows K2.
[OPEN] Need realistic decomposition/error chain through both switches, PPMM kernel, rescale, and actual modulus/precision/security; the q=101089 DFT toy is unscaled and has no CKKS precision interpretation.
[PRIOR ART] Generic full-ring key-switching density is standard RLWE algebra. No novelty claimed; not an original paper correctness bug.

## End of Iteration
STATUS: FAIL — second-switch sparse-support hypothesis.
RESULT: Exact star axis swap followed by dense public switching-key multiplication removes the assumed sparse Y-support; 9/9 Y positions (324/324 W,Y,U coefficient locations) at KS2 for K=1 AND K=2 in q=101089 toy; isolated full-support KS2 noise bound 37260 in the Iteration34 noise model, not 8280K.
NEXT_ACTION: Return to PI for a strategic choice: archive this low-novelty joint-packing branch or authorize a different **real CKKS scale-aware** bound for both KS + PPMM + rescale. Do not repeat toy support sweeps.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged.
