# Iteration 34: Lifted-integer auxiliary key-switch noise under joint MRFHE Y packing

Date: 2026-10-10
Status: PASS for **single key-switch added-error bound in a specified toy model**; NO full-PCMM noise proof, NO real CKKS precision/security evidence; NOVELTY NOT VERIFIED.

## Origin, source and protocol

Read GitHub Notes `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, `STATE.md`, `failures/mrfhe-joint-packing-noise-isolation.md`, and `findings/mrfhe-aux-ring-cross-batch-coefficient-packing.md` before performing this iteration. The RIG-HE contents of STATE.md remain parked and must not be rewritten.

[FACT / SOURCE] Cheon et al., *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, IACR ePrint 2026/853; full 18-page original paper supplied in user's ChatGPT Library as `2026-853.pdf`; this iteration re-read source PDF parsed text physical pp. 9-10 (auxiliary ring / Proposition 5.7 / Algorithm 1). This is **Library** source, not a successful Research MCP ePrint PDF download.
- §5.1, physical p.9: `S^(omega)=Z[omega][W,Y,U]/(W^d-omega,Y^d-omega,U^(2n1)+1)` where d=n2/2.
- §5.2, physical p.10, Algorithm 1: PCMM comprises star, first secret key switch, reduction to PPMM, second switch, rescale. The following analysis treats one gadget key-switch **added error term** only.
- For joint packing and its conditional operation-count improvement, see Iteration 32; for cross-batch key-switch noise counterexample Y^2*Y^7=omega, see Iteration 33.

## Primary hypothesis and decisive test

[HYPOTHESIS, NEGATIVE IN ITS "NECESSARILY" FORM] Cross-batch switching-key noise induced by taking two rather than one n1-batch necessarily forces the modulus to increase or makes the single auxiliary-ring key switch incorrect. Falsify this necessity with one fully **unwrapped** integer setting in which all permitted gadget digits and key errors have rigorous |coefficient error| < q/2 for K=2.

[MINIMAL TEST] Exact integer coefficient convolution in S^(omega), with a precisely stated coefficient noise model; compare K=1 and K=2 under the same preexisting input digit coefficients and same error-key samples, and independently certify a worst-case bound. Do not attempt full bootstrapping, noisy DFT evaluation, estimator, or benchmark yet.

## Toy parameters and reproducibility

- `w2=3, w3=2, n1=2, n2=18, d=9`; `S=Z[omega,W,Y,U]/(omega^2+omega+1, W^9-omega, Y^9-omega, U^4+1)`.
- Prime `q=101089`, satisfying `q ≡ 1 (mod 216)`; `q/2=50544.5`. `G=16`, `L=5` balanced digit levels, digits in [-8,7]. Both Z[omega] basis components are represented explicitly.
- Each coefficient of each independent switching-key error is sampled from {-1,0,1}. This is a bounded ternary **toy distribution**, not a claim about the exact Gaussian or RNS distributions of deployed MRFHE.
- For each trial generate a modular-uniform input polynomial a in four Y positions, represent centered modulo q, verify exact balanced base-16 gadget reconstruction. K=1 retains Y^0,Y^1; K=2 additionally has Y^2,Y^3. They reuse the identical original Y^0,Y^1 inputs and all error polynomials.
- Error is **lifted**: `E_K = sum_{l=0}^{L-1} d_l(a_K)*epsilon_l` is evaluated in the integral cyclotomic quotient ring, not modulo q. The only modulo q operation checks that these integers would reduce and center back to the same values.
- `/mnt/data/iteration34_lifted_ks_noise_audit.py`; seed 20261034; 80 paired trials; verified 1000/1000 additional independent monomial quotient-ring multiplication checks.

## Certified coefficient bound

[DERIVATION] In basis 1,omega, enumerate all pairs of gadget components in [-8,7], error components in {-1,0,1}, and omega^t for t=0,1,2 (the possible W and Y wrap factors), with U wrap supplying only ± sign. The greatest absolute resulting basis coefficient is 23 (attained for a=-8, b=7, e=-1, f=1, t=1 yielding output components (22,23)).

For each fixed output coefficient and each gadget level, every occupied Y exponent j, W exponent i, and U exponent k determines exactly one complementary error-key exponent contributing to that output. There are at most `J*9*4` such contributions when J=2K Y coefficients are occupied. Triangle inequality therefore yields a universal bound for THIS SPECIFIED digit/error model:
`||E_K||_infty <= 23 * 5 * 9 * 4 * (2K) = 8280*K`.
Hence K=1 bound 8280; K=2 bound 16560, both below q/2=50544.5. This certifies absence of modular coefficient wrap for the isolated switch-error term, even in worst case; it does NOT bound the total noise of either PCMM or bootstrapping.

## Exact observed results

[EXPERIMENT] 80 paired fixed-seed trials:
- target original batch coefficients Y^0,Y^1: mean RMS(K=1)=108.9826; mean RMS(K=2)=154.2449; ratio 1.4153 (close to sqrt(2)); K2 target RMS larger in 80/80 paired trials.
- maximum absolute output integer error across the ring and 80 trials: K1=491, K2=797.
- new source contribution to original target Y^0,Y^1 has mean RMS=108.3938.
- every trial obeyed rigorous universal K-specific bounds; every q-centered re-encoding of the lifted K2 noise returned exactly the same integer coefficient (no alias).
- a separate independent 1000-case monomial test of integral quotient-ring multiplication, including omega^2=-1-omega, W/Y omega wraps and U sign wrap, passed 1000/1000.

## Interpretation / limitations

[FACT / DERIVATION] A higher K can increase noise in original target coefficients, as Iteration 33 showed, but an extra batch does **not necessarily** demand a larger q for a **single** auxiliary switching operation. The deterministic worst-case bound grows linearly in K while observed RMS follows a roughly sqrt(K) pattern **only for this chosen model and these 80 runs**.

[OPEN] After the first key switching, PCMM performs a nontrivial plaintext `d circledast` (DFT) transform and a second key switching plus rescale. Noise multiplication and subsequent gadget digits can invalidate this single-switch bound. The actual parameter selection, security level, RNS modulus chain, input error, and precision are untested. Neither a throughput speedup nor overall correctness of MRFHE K=2 joint packing has been proved.

[PRIOR ART] CKL 2025/1957 and MRFHE already use batching; convolution-noise accounting and coefficient-wise centered lifting are routine. Nothing here establishes a new FHE technique. NOVELTY NOT VERIFIED, contribution priority LOW absent a distinctly better cost-noise frontier.

## End of Iteration

STATUS: PASS for strictly bounded/no-wrap single-switch added error under chosen toy model; the claim that joint-packing noise **necessarily** makes such switching infeasible is FAIL. Full homomorphic claim remains OPEN.
RESULT: Certified ||E_K||_infty <= 8280 K for K=1,2, with q/2=50544.5, and exact pairwise observed error growth ≈1.415x RMS on original batch at K=2. Cross-batch noise occurs yet need not saturate the modulus.
NEXT_ACTION: If PI wishes to pursue this low-novelty branch, take the **second switching's input digit decomposition after the actual D2' PPMM step**, using a noise-safe modulus and identical K1/K2 keys, and decide if one-stage slack survives the second switch/rescale. Do not claim complete noise feasibility from this note alone.
STATE_UPDATE: NO; keep unrelated parked RIG-HE state untouched.
