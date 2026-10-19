# BOOT B011 — Shared GSW key reuse does not guarantee favorable joint DFR

TRACK_ID: BOOT
ITERATION: B011
DATE: 2026-10-19
STATUS: FAIL_UNIFORM_CORRELATION_ADVANTAGE / PASS_EXACT_FOUR_OUTPUT_CONSTRUCTION
STATE_UPDATE: YES

## Exactly one primary hypothesis
[HYPOTHESIS] Because a bit-selector GSW evaluation key is shared across all outputs of the MPmul loop in Guimarães–Pereira (2025/686), the shared key errors necessarily induce enough uniformly positive cross-output correlation to certify a constant-factor improvement over per-output union-bound decryption failure probability for *every admissible MPmul input*. This would enable lower-precision gadget settings and smaller keys at fixed joint DFR.

## Provenance
[FACT] Guimarães, Pereira, "Fast amortized bootstrapping with small keys and polynomial noise overhead", ePrint 2025/686, 34 physical pages; version-unverified mirrored PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335. Physical pp. 9–10: RLWE/GSW encryption forms and external product noise; pp. 11–12: MPmul Algorithm 1 and Lemma 3.1; pp. 13–14: bin-SAB Algorithm 2 and Lemma 4.1. Author's source https://github.com/antoniocgj/Fast-Amortized-Bootstrapping . DOI 10.1145/3719027.3765181 (CCS 2025).
[FACT] The standard RLWE form (a,b=a*z+e+m) accepts an error-free trivial encryption with a=0,b=m as a valid *correctness test* for any secret z. It does not emulate the usual randomized encryption distribution.
[FACT] GSW key for encrypted selector v=0 consists of independently sampled RLWE rows (a_r,a_r*z+e_r) plus zero gadget-message part. For a fixed gadget-decomposed ciphertext difference c, its external-product decryption error is an explicit row-weighted sum of the same e_r used in all outputs.
[PRIOR ART] The elementary union bound and covariance identity are classical, not claimed novel. Public literature search (including 2025/686 and GPvL23) found no directly verified theorem guaranteeing a positive correlation floor for arbitrary MPmul inputs. This is not proof of absence of such work.

## Cheapest decisive source-aligned exact counterexample
[DERIVATION] Use n=8 MPmul coefficient positions and RLWE ring R_Q=Z_Q[X]/(X^16+1), with Q divisible by gadget base β>=4 (take e.g. Q=2^16, β=16), exact balanced gadget decomposition, and selector bit v_0=0 at bit stage i=0 (shift s=1). Pick valid zero-input-noise trivial RLWE ciphertexts c_j=(0,X^{u_j}) encrypting exponent monomial X^{u_j}, with
    (u_0,...,u_7)=(0,2,4,6,8,10,12,14).
Each non-wrapped odd output j∈{1,3,5,7} follows source Algorithm 1:
    c'_j = c_j + (c_{j-1}-c_j) ⊙ GSW(0).
No automorphism/keyswitch is involved in these four branches. The difference polynomial is Delta_j=X^{u_{j-1}}-X^{u_j}; the a-branch difference is exactly zero.
[DERIVATION] With β=16 and coefficient ±1, each Delta_j has one b-side gadget level with digits ±1 and all other gadget levels zero (this uses exact decomposition; any alternative centered digit convention that does this uniformly also works). The SAME b-side GSW key-error row polynomial e(X)=sum_{r=0}^{15} e_r X^r enters the four outputs. Extract constant terms of the freshly added key error:
    xi_1 = [(1-X^2)e]_0 = e_0+e_14
    xi_3 = [(X^4-X^6)e]_0 = e_10-e_12
    xi_5 = [(X^8-X^10)e]_0 = e_6-e_8
    xi_7 = [(X^12-X^14)e]_0 = e_2-e_4.
All eight source error coordinates are distinct; if coefficients e_r are independent identically distributed and symmetric about 0 (e.g. independent discrete Gaussians, as in ordinary key-generation models), the four xi_j are independent and identically distributed, despite *reusing the identical encrypted selector key*.
[DERIVATION] Let M be the 4x16 integer matrix of these coefficient-0 linear maps. Its nonzero rows have exactly two signed entries. Exact Gram matrix:
    M M^T = diag(2,2,2,2).
Thus for independent coefficients of variance sigma², Cov(xi)=2sigma² I_4. If Gaussian, xi_j are i.i.d. N(0,2sigma²). Independence itself does not require Gaussian because the underlying coordinates are disjoint; it also holds with discrete Gaussian coefficient distributions as long as coefficients are independent.
[INDEPENDENT REPRODUCIBLE TEST] Verified all 4 difference-support identities via direct negacyclic integer multiplication and Gram matrix (rank 4) with exact Python integer operations. Exhaustively enumerated the 8 involved source error coefficients from alphabet {-1,0,1} (3^8=6561 cases) and checked exact joint frequency factorization into four identical marginals. All 625 joint support tuples satisfy count(x_1,x_3,x_5,x_7)=prod_j count_marg(x_j), 6561/6561 error configurations accounted for. This is an exact finite-distribution toy test, NOT native FHE or real discrete-Gaussian DFR measurement.

## Conditional correlation may range from -1 to +1
[DERIVATION] Keeping j=1,j=3 and u0=0,u1=2, choose:
  - u2=4,u3=6: Delta3=X^4-X^6; rho=0;
  - u2=0,u3=2: Delta3=1-X^2=Delta1; rho=+1;
  - u2=2,u3=0: Delta3=X^2-1=-Delta1; rho=-1.
All are allowed exponent-encoded inputs for the abstract MPmul Algorithm 1; same GSW row used. With independent Gaussian coefficients their covariance Gram matrices divided by sigma² respectively [[2,0],[0,2]], [[2,2],[2,2]], [[2,-2],[-2,2]]. This falsifies any *input-independent* sign or positive lower bound on output correlation based solely on key reuse.

## Probability implication
Let F_j={|xi_j|>T}; in the four-output independent construction with identical marginal failure p, exact joint failure is
    Pr[union_{j∈{1,3,5,7}} F_j] = 1-(1-p)^4 = 4p-6p²+4p³-p⁴.
The union bound is 4p. Their ratio goes to 1 as p->0; hence no universal multiplicative improvement factor smaller than 1 by a constant can be proved merely from key reuse, over all admissible inputs and thresholds.
Gaussian illustration with T=3sqrt(2)sigma gives p=erfc(3/sqrt(2))=0.00269979606326, 4p=0.01079918425304, exact=0.01075552952137. This is a probability-structure illustration, not real MPmul/FHE DFR.
Because the overall maximum-over-outputs failure event contains that four-output subevent, a universal high-confidence multi-output bound improving by constant factor via correlation would need additional assumptions or structural restrictions beyond generic shared GSW key reuse.

## Limitations and critical qualification
- Legitimate source-operation interface, but test uses *trivial error-free RLWE ciphertexts*, exact gadget decomposition, zero initial noise, a selector encrypting zero, and one MPmul stage. Such ciphertexts are atypical under randomized RLWE encryption and do not show average-case correlation under the actual bootstrap input distribution.
- The selector's GSW error is sampled once; multiple external products *must not* be falsely treated as independent fresh GSW encryptions. Here output independence arises from different coordinates of the SAME error polynomial; this is a distinct property with explicit proof.
- This construction only concerns *one extracted coefficient per output*. It does not certify full-ring infinity-norm joint DFR, later MPmul rounds, packing, output key-switching, adversarial CCA/key reuse, or actual full bootstrap correctness/noise.
- For coefficient errors from a discrete Gaussian, the independence follows from disjoint supports; for a subgaussian coefficient distribution with arbitrary dependence, even the toy independence statement requires independent coefficients.
- A tighter *input-conditioned* covariance-based bound for realistic ciphertext distributions could still be possible. No universal covariance lower bound exists for all valid plaintext ciphertexts from the shared-key property alone.

## Decision
[RESULT] FAIL the uniform positive correlation / fixed-factor union-bound improvement hypothesis. PASS a source-aligned exact four-output independence falsifier. Do not claim key memory/latency/DFR improvement or a bug in either paper.
[PARK] B010–B011 "generic shared-selector covariance -> key-size reduction" path. Reopen only if a precisely characterized input distribution and a robust source-faithful error/joint-failure bound survive conditioning on actual adaptive gadget digits and key reuse, AND lead to better security/DFR-matched parameters. Small Gaussian toy rank reduction alone does not justify work.
[NEXT_TEST] BOOT B012: shift from generic correlation to a new structural interface: 2025/1935 native matrix arithmetic × 2025/696 two-part incomplete-NTT butterfly representation. Start by verifying whether one butterfly/block-linear map is realizable natively without ring conversion or ciphertext-ciphertext matrix multiplication, and cost it against source baseline. The 2025/1935 cached full PDF is available; do not import any OTHER research track's NEXT_ACTION. This is a candidate hypothesis only, not a validated optimization.
END: STATUS FAIL_UNIFORM_CORRELATION_ADVANTAGE / PASS_EXACT_FOUR_OUTPUT_CONSTRUCTION; RESULT no universal gain; NEXT_TEST B012; STATE_UPDATE YES.
