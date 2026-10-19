# BOOT B011 failure archive — Universal covariance advantage from GSW reuse

TRACK_ID: BOOT
ITERATION: B011
DATE: 2026-10-19
STATUS: PARKED_NO_UNIFORM_ADVANTAGE

## Hypothesis killed
Shared MPmul GSW selector encryption errors necessarily produce sufficient positive cross-output correlation to provide a uniform constant-factor reduction of the joint failure probability (over the standard per-output union bound), enabling universally smaller gadget parameters.

## Cheap decisive falsifier
2025/686 MPmul Algorithm 1, first bit i=0, n=8, R=Z_Q[X]/(X^16+1). Take trivial zero-noise RLWE ciphertexts c_j=(0,X^{2j}); selector GSW encryption of bit 0, same GSW ciphertext reused for all outputs; exact gadget decomposition with ±1 coefficient digits. For odd nonwrap outputs 1,3,5,7, the SAME GSW error row e(X)=sum e_r X^r contributes constant-phase coefficients
    xi1=e0+e14
    xi3=e10-e12
    xi5=e6-e8
    xi7=e2-e4.
If key noise coefficients are independent, these four output errors are exactly independent despite reuse, as each depends on disjoint source coefficients. Their Gram matrix is 2 I_4. For symmetric i.i.d noise distributions, the marginals match, so joint tail=1-(1-p)^4 ≈ 4p as p→0. There can be no input-uniform nontrivial constant multiplicative union-bound improvement derived from reuse alone. Additional 2-output legal exponent choices produce correlations +1, 0, -1 in a Gaussian coefficient model, so no input-independent positive correlation floor. Source external product/GSW shape and MPmul nonwrap branch checked; no input key-switching or automorphism in the four relevant positions.

## Verification and scope
Exact ring integer coefficient computations; 4x16 Gram =2 I; exhaustive 3^8=6561 finite-alphabet noise assignments factored joint frequencies (625 joint outcomes). This is a cryptographic algebra test, not a run of native FHE, not a typical randomized ciphertext input distribution, not a statement about final whole-ring bootstrapping DFR or all valid output error models. A *distribution-conditioned* theorem or hardware/runtime optimization is still possible with extra conditions and source analysis.

## Decision
PARK covariance-only shared-GSW memory/latency optimizer. Source 2025/686 already gives a per-output Lemma 3.1 bound and does not claim the missing uniform correlation theorem. Not a break or flaw of the paper.
Evidence: findings/boot-B011-four-output-shared-gsw-independent-noise-counterexample.md.
NEXT_ACTION: B012, new BOOT hypothesis combining 2025/1935 matrix-native arithmetic with 2025/696 incomplete-NTT block/butterfly map; source-faithful algebraic interface first, no inherited actions from other tracks.
