# Iteration 33 — MRFHE joint Y-packing does not preserve cross-batch noise isolation

Date: 2026-10-10
STATUS: FAIL for **noise-isolated/zero-overhead** joint packing. This does NOT negate Iteration 32's plaintext algebraic noninterference or rule out a noise-budgeted implementation.

## One primary hypothesis / decisive test

[HYPOTHESIS — FALSIFIED] In the W-heavy MRFHE auxiliary S^(omega) ring, joining K=2 independent n1-batches in distinct Y-power coefficients and using the existing auxiliary PCMM/key-switching keys preserves *per-batch output noise independence*, i.e., batch B does not contribute key-switch error to output coefficient positions of batch A.

[FAILURE CONDITION] A legal input gadget digit in one batch and a small switching-key error produce a nonzero noise term in another batch's Y-power coefficient. One counterexample suffices.

## Source evidence / scope

[FACT] Cheon et al., *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, IACR ePrint 2026/853, original 18-page PDF `2026-853.pdf` in user's ChatGPT Library, extracted physical pp. 9–11 and Appendix D.2 physical pp. 15–16. This source is Library full text, **not** successful Research MCP ePrint acquisition:
- §5.1, physical p.9: `S^(omega)=Z[omega][W,Y,U]/(W^d-omega,Y^d-omega,U^(2n1)+1)`, d=n2/2.
- §5.2, Proposition 5.7, physical p.10: D2' is a left W-evaluation transform preserving each plaintext Y^j coefficient.
- Algorithm 1, physical p.10: star involution, switch s* -> s, PPMM reduction for d circledast, second switch s* -> s, rescale.
- Algorithm 2, physical p.11: packing via ring conversion and two auxiliary PCMMs.
- Prior positive partial result: `findings/mrfhe-aux-ring-cross-batch-coefficient-packing.md` (Iteration 32). It established *message* noninterference but explicitly left *noise/key-switch correctness* open.

## Exact cross-batch noise counterexample

[DERIVED] Standard coefficientwise gadget key switching has `a = sum_l d_l(a)G^l` and switching-key encryptions `B_l+A_l s_out=G^l s_in + eps_l`, so the new decryption error is `e + sum_l d_l(a)*eps_l` (all ring products). MRFHE's auxiliary Y-polynomial obeys Y^d=omega.

For w2=3,w3=2,n1=2,n2=18,d=9, place batch A in Y^0,Y^1 and batch B in Y^2,Y^3. A *valid single gadget digit* supported entirely in batch B is `d_0(a)=Y^2`; a switching-key small error can be `eps_0=Y^7`. Hence

`d_0(a)*eps_0=Y^9=omega * Y^0 !=0.`

Thus a batch B auxiliary ciphertext component injects *key-switch error* into Y^0 (batch A). This is a deterministic counterexample. No FFT, noise estimator, or float approximation is required. The original plaintext map still has no cross-batch mixing. The existence of extra error does not establish that a correctly sized q would fail to decrypt.

## Actual toy homomorphic auxiliary PCMM / key-switch experiment

[EXPERIMENT] Full runnable local code: `/mnt/data/iteration33_homomorphic_pcmm_audit.py` (seed 20261043). q=433; ring S^(omega) with W^9=Y^9=omega and U^4=-1. Represents the *two* q-split omega embeddings simultaneously (roots 198,234), so conjugation exchanges components; does NOT falsely assume it is an F433 field automorphism. Exact modular coefficient operations.

- Use D2' Vandermonde map encoded as 9x9 bivariate plaintext polynomial; implement star as conjugate+inverse+W/Y swap, `circledast` as explicit coefficient-zero trace contraction, and both Galois-conjugate key transformations.
- Standard (unscaled) gadget key switch: G=16, 3 balanced centered digits; switching keys encrypt G^l*s_in under s_out, with small one-sparse E_l. Common source key s(W,U)=W+U, independent of Y but *not* independent of W. Shared switching keys are reused for K=1 and K=2.
- Actual chain executed: `star(ct)` -> gadget KS(sstar to s) -> `d circledast (ct)` -> gadget KS(sstar to s), for the D2' PCMM stage. No rescale, R^(i) <-> R^(omega) conversion, second masked PCMM, or full CKKS bootstrapping.
- Verified `d circledast m* = D2'(m)` modulo 433, star involution, and secret-action equivariance.
- With E_l=0, for both K=1 and K=2, final decryption-minus-target equals exactly the DFT-transformed *nonzero source errors*, and none of the previously unused Y coefficients has error. This is a true noise-bearing RLWE relation, albeit toy-sized.
- With small nonzero E_l, the noise in original batch A differs when batch B is added, and additional noise appears in unused Y^4..Y^8 positions. First two batch A Y coefficients change between K=1 and K=2. Deterministic Y^2*Y^7=omega check also passed.
- Typical run measured centered modulo-433 output noise average absolute coefficient about 101.96 for K=1 and 108.28 for K=2; both max 216. These numbers are **wrapped/saturated modulo q**, are not an additive noise bound, and cannot be used as a meaningful noise growth or CKKS precision estimate. Toy one-sparse errors are NOT a Gaussian security parameterization.

## What fails, what survives

[NEGATIVE] The stronger assumption of no cross-batch key-switch noise or unchanged per-batch noise fails. Global switching-key errors are polynomials in Y and multiply gadget decompositions; they couple Y-power columns even though the desired linear transformation is block-diagonal in Y. A direct independent-noise argument and a free-performance-gain assertion are invalid.

[SURVIVES] The algebraic ability to pack multiple same-key batches, the zero-switch-error/plaintext correctness, and conditional amortized switching-equivalent operation counts from Iteration 32. Shared switching keys are not by themselves shown impossible; sufficient modulus/noise budgets may still make the idea correct.

[OPEN] Evaluate *unwrapped* per-stage error using lifting and realistic switching/rescale/modulus/noise parameters; then actual latency and packing cost. Any claim of improved key-switch equivalence translating to throughput needs explicit benchmarking. Current q=433 experiment is not a security estimate and deliberately omits full bootstrapping.

[PRIOR ART / NOVELTY] Original MRFHE & CKL (2025/1957) already use structured batch packing; this obstruction is routine polynomial gadget noise algebra, not a new cryptanalytic result. NOVELTY NOT VERIFIED. No flaw in either paper is claimed.

## End of Iteration

STATUS: FAIL (noise-isolated joint packing hypothesis).
RESULT: Explicit Y^2*Y^7=Y^9=omega cross-batch key-switch noise term; exact homomorphic toy PCMM confirms plaintext correctness with noise-free switching and cross-batch noise effects with noisy switching.
NEXT_ACTION: PI decide whether the joint-packing branch merits **one** lifted-integer error-bound experiment for auxiliary key switching before any implementation; do not continue on the assumption of zero cross-batch noise.
STATE_UPDATE: NO. `STATE.md` continues to hold the distinct parked RIG-HE state; Iteration 32 positive finding remains unchanged.
