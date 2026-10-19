# BOOT-B036 — Source-exact BatchBoot radix-4 shared-GSW-body error incidence through complete RLWE.Repack

TRACK_ID: BOOT
ITERATION: B036
DATE: 2026-10-19
STATUS: PASS_IDEAL_REPACK_ORTHOGONALITY / PASS_SHARED_BODY_FIRST_ORDER_FINAL_VARIANCE / FAIL_GENERIC_UNPROJECTED_COVARIANCE_ARGUMENT_AS_BATCHBOOT_FALSIFIER / UNCLEAR_NATIVE_PRECISION_KDM_AND_NOVELTY
STATE_UPDATE: YES
ISOLATION: BOOT ONLY. SHIP remains PAUSED_BY_PI after I407; no SHIP read/write/iteration.

## Primary hypothesis, cheapest decisive test
B035 showed ordinary RGSW_s(m) and tau_-1-parametrized RGSW_s(m) for the SAME binary selector share the semantic second/body RLWE'_s(m), so physically deduplicating these ciphertext rows could reduce an independent TFHEpp radix-4 EMP key subpayload by 21.43% (3 of 14 RLWE rows). But B035's generic thought experiment showed that if independent direct and inverse outputs carrying the same row error e_B are later literally added, its variance can double. B036's one primary technical question: **Does the ACTUAL BatchBoot Algorithm 2 EMPmul followed by Algorithm 6 RLWE.Repack, including the sparse Homomorphic Trace, cause direct/inverse accesses of the same selector row to add in ANY final ciphertext coefficient, or does a projection/selection invariant eliminate their cross-covariance?** Test one original paired-RGSW row under true radix-4 source/target mapping and exact published repack operator, not an arbitrary output-sum example. Check multiple onehot selection stages as a cheap propagation robustness test. If only an elementary storage dedup remains and source already implicitly defines same row, do NOT claim a new FHE scheme.

## Original sources and source-integrity notes [FACT]
- Original Li et al. "BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications" USENIX Security 2026 original 20-page official prepublication https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf. PDF physical p6 (0-index5) Table1 and Eqs7–9: four ordinary RGSW plus 3 inverse parametrized RGSW, reused SAME selector message row RLWE'_s(m); p7 (0-index6) Algorithm2 EMPmul has outputs indexed j, each onehot branch either direct OR tau_-1 external product for a given output and branch, depending on wrap; p18 (0-index17) Algorithm6 RLWE.Repack and Algorithm5 Homomorphic Trace, plus Appendix C.2 Lemma4.1 additive error variance. PDF page screenshots actually inspected this iteration and the relevant formulas visible.
- The public implementation read is independent (NOT the paper authors' artifact): virtualsecureplatform/TFHEpp, include/tfhe/batchboot.hpp git BLOB SHA db73ed7d1c5c3cf6283711e1a6640be4a513d0c8; lines 102–105 store 4 full direct and 3 full inverse TRGSWFFT; lines 199–225 independently sample matching key rows; lines 343–416 BatchExternalProductAddFD, lines 419–476 BatchEMP source mapping, lines 604–620 BatchHomomorphicTrace, lines 622–658 BatchRepack, lines 660–671 full BatchBootstrap. Original author's Zenodo source DOI 10.5281/zenodo.17936945 was attempted via web DOI/record but inaccessible; do NOT assert author artifact also duplicates these rows. Whole TFHEpp git commit is not pinned; the exact blob SHA is.
- Original PDF Lemma4.1 has an upper bound V_EMP<Var(c_in)+2ell V_EP which ignores context-dependent late-stage repeated FFT/rounding beyond its assumptions; do NOT treat a toy proof as full reproof.

## Mathematical key-noise incidence [DERIVATION]
For one radix-4 digit and a branch r=0,1,2 (meaning shift d=(r+1)2^(2level)), TFHEpp computes for output index j:
 positive-direction:
  inverse(j,r) iff j<d, source(j,r)=(j+n−(d mod n)) mod n;
 negative-direction:
  inverse(j,r) iff j+d>=n, source(j,r)=(j+(d mod n)) mod n.
At each fixed pair (j,r) the same term uses either inverse GSW key or direct GSW key, NEVER BOTH. Direct/param rows for a given r share only the body gadget ciphertext in proposed compact representation; their error is E_r(X), a polynomial. Let body decomposed polynomials at source state t be D_t(X). The BODY row errors injected for that branch are:
  direct: D_source(X) E_r(X);
  inverse: tau(D_source(X)) E_r(X)
where tau:X→X^-1 acts on input decomposed polynomial before parametrized external product, with original key's distinct nonce row handling tau(secret). The two alternatives are mutually exclusive for fixed output j. Distinct output j may see the same E_r, causing cross-output covariance BEFORE repacking.

REPACK PROJECTION LEMMA (ideal exact operations): let n|N both powers of2 and inputs c_0,...,c_(n−1)∈R=Z[X]/(X^N+1). Apply source Algorithm6's butterfly with exact halves and noiseless autos: at each level ell, update
  c_j <- (c_j−X^(N/2^ell)c_(j+n/2^ell))/2 + tau_(2^ell+1)((c_j−X^(N/2^ell)c_(j+n/2^ell))/2) + X^(N/2^ell)c_(j+n/2^ell).
For sparse n<N, apply Algorithm5 Homomorphic Trace (additional power-of-2 autos) to project to subring with active coefficient positions j*N/n.
Then for every j=0..n−1,
  coeff_(j N/n) (Repack(c_0,...,c_(n−1))) = coeff_0(c_j).
and for any k NOT multiple of N/n, coeff_k(Repack(...))=0 (ideal noiseless trace).
For full packing n=N all positions active and the same formula uses stride1.
Consequently, to first order with fixed plaintext gadget digits and exact downstream onehot choices, each final output coefficient depends on precisely ONE EMP output position j, so for a fixed GSW branch r it receives either DIRECT or INVERSE body-row error influence, never both. If L_D,k, L_I,k are the linear maps from one shared key-row error vector e into final coefficient k, their coefficientwise inner product is ZERO:
  <L_D,k,L_I,k>=0.
For independent body samples with covariance σ²I, Var_ind=σ²(||L_D,k||²+||L_I,k||²); sharing makes Var_shared=σ²||L_D,k+L_I,k||², hence Var_shared=Var_ind at these finalized coefficients in THIS ideal first-order model. This is an important positive correction to the B035 generic example, NOT a claim to have rigorously handled real approximate-digits/torus rounding, RGSW/key-switching error dependence, non-Gaussian error, circular/KDM distribution, or subsequent homomorphic operations. The joint covariance ACROSS DISTINCT packed slots may still change, even when every marginal variance does not, affecting probability of simultaneous errors and downstream FHE ciphertext uses.

## Why B035's generic 2x variance thought example does not directly apply [DERIVATION]
If one arbitrarily sums direct+inverse outputs each containing e_B, error2e_B vs e_B+e_B' gives Var factor2. This is a correct generic RLWE statement but NOT the actual Algorithm6 output coefficient map. In source-compatible N8,n4 radix-4 r0 positive mapping and arbitrary public body gadget digits, the PRE-trace intermediate coefficient X1 can receive both paths with common e_B. A simple 2-input witness:
  body digits at source c_0: 1, c_3: X²; others set to zero for this error-channel test.
The map from e_B to intermediate coefficient X¹ is
  A_D=(0,1/4,0,1/4,0,1/4,0,-1/4)
  A_I=(0,1/4,0,1/4,0,-1/4,0,-1/4).
Dot product=1/8; norms²=1/4 each. Therefore independent pretrace var=(1/2)σ², shared pretrace var=(3/4)σ² (50% worse). BUT Algorithm6 sparse Homomorphic Trace annihilates odd exponents, including X¹; after trace, BOTH have 0 variance at that coefficient. This demonstrates the importance of COMPLETE DATAFLOW and why unprojected covariance cannot rule out a final packed-row sharing improvement. As always, automorphism key-switch error added by nonideal trace may repopulate killed positions; no proof of its full joint distribution.
For n=N full packing, there is no trace, BUT all coefficients are active single-source projections, so no unprojected mixed error appears in final coefficients.

## Independent reproducible exact toy verification
Scripts run this turn in local isolated container (not added to repo, but SHA256 and pseudocode documented):
  /tmp/boot_b036.py SHA256 f3be04efa018ea6a5e7161eec892674e940f49c213ff75b4373b53d87ef836fc
  /tmp/boot_b036_verify.py SHA256 8abb828ad5c27df8891fc6a718e666cde2879ffcd3b8cfb4ddf77b32a9043998
  /tmp/boot_b036_full.py SHA256 5e85e48f4c4b3b0cf516908a4861ad383c5ff30c2d4e93f873bd0732654050fc
  /tmp/boot_b036_multistage.py SHA256 e0400c642beba1e3e2a9cf4a82560c99ff818f386b9f67d4efdcb7fce9ca980d
- Implement negacyclic ring polynomial X^N=-1, exact auto tau_g(X^i)=X^(gi), repackage using paper/TFHEpp Algorithm6 with exact /2 (floating double used only for tiny powers2 rational numbers; all specific operations are exactly representable), optional Homomorphic Trace as in code.
- For every basis input polynomial X^k in one of n input ciphertext positions (other inputs zero), across N∈{8,16,32}, n∈{2,4,8,16} with n≤N: 1552/1552 checks verify output active-slot coefficients exactly equal the corresponding input c_j constant coefficient. Sparse offslot projection checked via independent basis and after trace.
- For N8,n4 with 250 independent RNG seeded20261019 random input BODY decomposition polynomial arrays, 3 radix-4 branches, both positive/negative rotation direction, all 8 final coeff each: 250*3*2*8=12000 cross-inner-product checks, exactly0 nonzero after full repack+trace.
- Repeat with one more exact signed-automorphism/array-permutation stage selected by randomly sampled legal digit0..3 (onehot message effect), 500 random input arrays, 3 radix-4 branches, both rotation directions, all8 coefficients: 500*3*2*8=24000 covariance cross checks, exactly0 nonzero. This is a linearized model with exact intermediate plaintext permutations and no new external-product noise.
- Explicit pretrace offslot counterexample above: 1/2 vs3/4 σ² (×1.5); after full trace at same coeff0 vs0. Do NOT call this a production FHE variance benchmark.

## Limits, security and novelty gates
Correctness of exact *individual* shared-key external product established B035 (10000/10000 exact small ring tests with nonzero row errors); B036 strengthens noise-incidence analysis through source repacking and partially through repeated ideal selection, but no native compact key layout built/compiled/performance measured. Approximate decomposition makes new errors depend on cipher digits, including prior key errors; torus halving and actual trace key switching adds discrete rounding and randomized RGSW/Galois key error. One-hot selectors are encrypted; per-key plaintext bit is exact but even zero-bit RGSWs contribute noise. These issues require full joint noise/DFR proof before claiming unchanged 2^-128 or IND-CPA-D.
Joint security: publishing a duplicated ciphertext of the SAME encrypted selector message is not an extra independent LWE sample, so B023 different-message same-mask leak does not apply, but complete correlated evaluation-key transcript and circular/KDM security under paper assumptions unproved.
Input secret Hamming weight/profile leak in independent TFHEpp BatchBoot has caveats in docs/BATCHBOOT.md, unrelated to this local key dedup.
Structural key-memory saving remains a conditional 3/14=21.4286% of EMP digit-key spectral polynomial payload (4 direct+3 inverse RGSWs each2 RLWE rows, share3 body rows); not full BSK size/RSS or online speedup. No reductions of expensive FFT/external-product count, may add memory indirections. Source paper writes both second halves as RLWE'_s(m), and the original AUTHORS' artifact at DOI 10.5281/zenodo.17936945 was INACCESSIBLE in this session, thus originality versus original implementation is UNKNOWN. This is elementary duplicate-row storage and not a new cryptographic primitive; no convincing new publishable Bootstrapping algorithm, even after the positive projection discovery.
Potentially interesting future principle: projection-aware noise sharing uses the final dataflow instead of assuming all shared random errors penalize each individual message; but this itself is standard linear-algebra noise analysis and not a novel protocol. Real algorithms might exploit a more nontrivial structured sharing with *provably orthogonal output supports*, but doing so would require a completely new construction and source-matched comparison.

## End-of-iteration
STATUS: PASS_IDEAL_FULL_REPACK_SHARED_ROW_NOISE_ORTHOGONALITY / PASS_TOY_MULTI_STAGE_PRESERVATION / FAIL_GENERIC_B035_COVARIANCE_AS_SUFFICIENT_COUNTEREXAMPLE / UNCLEAR_REAL_KEYSHARE_SECURITY_DFR / LOW_STANDALONE_PAPER_NOVELTY.
RESULT: A full-source correction: because BatchBoot Algorithm6 projects each input ciphertext's constant coefficient onto its unique active packed coefficient, direct/inverse shared key-error streams do not contribute simultaneously to one finalized coefficient in exact noiseless-selection/linear noise model; sparse trace additionally annihilates intermediates where covariance can be larger. Thus B035's arbitrary-addition example does not kill the particular memory layout. At the same time, no native/proven full speed/security result, and original published formalization already suggests row equality. This subbranch should be archived after B035–B036 to avoid endless trivial key-layout microtasks.
NEXT_TEST B037: PI-approved source-first BOOT research, switch to a DIFFERENT recent algorithmic bootstrapping bottleneck with verifiable full original paper and preferably author code (not this BatchBoot key duplication). First evaluate ONE real whole-dataflow bottleneck/assumption and propose a nontrivial secure/correct construction repair with end-to-end cost/novelty gates. Prioritize a fresh primitive/dataflow not textbook key row dedup or BSGS; check current USENIX26/TCHES26 and original-seed prior art. The SHIP project remains PAUSED_BY_PI, no read or writes. B037 NOT STARTED.
STATE_UPDATE YES, BOOT-only.
