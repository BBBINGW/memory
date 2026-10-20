# BOOT-B093 — SPRU strided secret at pinned OpenFHE v1.4.2: exact auxiliary prime and incomplete security gate
Date 2026-10-20 | TRACK_ID BOOT only; SHIP eval-key memory track untouched.
STATUS PASS_PINNED_AUX_PRIME / PASS_PUBLIC_SUBRING_KSK_PROJECTION / PASS_506_TOY_EQUATIONS / BLOCKED_SAGE_LATTICE_ESTIMATOR / UNCLEAR_REAL_128BIT_INSECURITY.

## Primary falsifiable hypothesis
B092 proved nondefault SPRU stride t changes the sparse secret from general block-onehot to s(X)=s'(X^t), and publicly exposes small-ring RLWE zero samples via the key-switch auxiliary limb. B093 tests whether this entails a concrete below-128bit attack at exactly the author's pinned OpenFHE auxiliary modulus, real noise and public sample count, rather than inferring insecurity from halving N. Decisive test is a source-pinned actual (N/t,p,sigma,m, secret-support) model plus validated lattice estimator or explicit attack. The estimator/attack threshold was NOT met this iteration; no false security conclusion.

## Fully grounded original paper and pinned author code
[FACT] Coron-Köstler Low-Latency Bootstrapping for CKKS using Roots of Unity (SPRU), ePrint2025/651 https://eprint.iacr.org/2025/651 . Research Notes full original cached 42 physical pages, SHA256 2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6, VERSION_UNVERIFIED. Physical pp15-16 §4.3-4.4 secret one-hot per block, pp19-22 §5 Algorithms1-2 key generation and selector trace/product, p24 Table2 128bit default and Table3 recorded performance, not claimed for stride>1.
[FACT] Author source https://github.com/coron/spru_boot pinned commit ad00b57ad15e5a32d227e36c713253c5667cfe3e. readme.md blob 42c442fc2035552500fa25039e430342b6f79605 explicitly requires OpenFHE tag v1.4.2 plus a public visibility patch, NOT latest main. src/keygen.cpp blob a367acf060fec5f85601d65974a2f1d989320f76, lines6-25: secret positions j*B+step*ind, first fixed at zero, lines97-120 generate KSK from old dense to new strided sparse secret. src/multiple_slot.cpp blob 7ffb1fff5d99dc8e0f947ae77083455d163afa64, lines150-200 produces 2n/step selector ciphertexts, lines203-301 online phase products/trace. test-new-bootstrapping.cpp blob 88192a9424d0bf86293a261298d0106766b4ff8, line183 sets step=1, h=64 around line68. src/params.cpp blob 3237e54f65039ca27752ef45759e0c50691d6d42 sets first CKKS limb 60 bits, following limbs49 bits, FIXEDAUTO. n default auto-selected by 128bit security standard; paper uses N=2^15 for SPRU.
[FACT] OpenFHE v1.4.2, DIFFERENT FROM MAIN. src/pke/lib/scheme/ckksrns/ckksrns-fhe.cpp blob c895b3e3e57514c4e1aa7712e327c1b218cdf901, lines3285-3344: KeySwitchGenSparse publishes an independently uniform a over a TWO LIMB RNS ring (q0,p). q limb b_q=-a_q*s_new+p*s_old+e_q; AUX p limb b_p=-a_p*s_new+e_p exactly. Only GetParamsP()->GetParams()[0] selected as p. This leaks a true zero-RLWE sample under s_new, so dense old secret cancels without unknown-plaintext concern.
[FACT] Same tag src/pke/lib/scheme/ckksrns/ckksrns-parametergeneration.cpp blob 3bab993c86ee66d4f434d5b345e66f12b0428a03 lines46-55 AUXMODSIZE60 for 64bit backend, 118-137 chooses aux bits; lines416-523 source First/LastPrime q0. src/pke/lib/schemerns/rns-cryptoparameters.cpp blob d5ac1bbeb4b7fd6df60fa80d3c69e8c7edee3bb7 lines135-167 special prime allocation, skip P-Q collisions; src/pke/lib/scheme/ckksrns/ckksrns-cryptoparameters.cpp blob c7723535adfc00d9bef85941ac19376d13042ca9 lines186-189 prime modulus step 2N. src/core/include/math/nbtheory-impl.h blob 86d52fbef979d96736a3aa2de3fd0c0ef3657c13 lines329-391 exact FirstPrime/LastPrime/PreviousPrime conventions. src/pke/include/scheme/gen-cryptocontext-params-defaults.h lines50,53 gives default sigma=3.19 Gaussian, HYBRID switching, normal 128-classic security choice (not a custom proof for ephemeral strided keys).

## Source-derived exact 60bit prime, not a runtime dump
At N32768, 64bit backend, M=2N=65536.
FirstPrime(60,M)=1152921504608747521 strictly >2^60.
LastPrime(60,M)=q0=1152921504606584833.
PreviousPrime(FirstPrime(60,M),M)=q0, so auxiliary candidate initially collides with ciphertext q0 and is skipped.
The next previous prime is p=1152921504598720513, 60 bits, p mod65536=1; independently checked via deterministic 64bit Miller-Rabin primality bases [2,325,9375,28178,450775,9780504,1795265022] in Python reconstruction. This is reconstructed from pinned source, NOT verified via native OpenFHE GetParamsP execution. No evidence other backend selections have identical p.

## Exact reduction, parameters, attack obligations
For stride t dividing N and B=N/h=512, let R_p=F_p[X]/(X^N+1), R'_p=F_p[Y]/(Y^(N/t)+1) with Y=X^t. Strided block-onehot s(X)=s'(X^t). Decompose a=Σ_r X^r a_r(Y), b and e likewise. Public auxiliary KSK limb b=-a*s+e modulo p therefore yields t exact projected small-ring samples
  b_r(Y)=-a_r(Y)*s'(Y)+e_r(Y) (mod p)
under SAME secret. a_r independently uniform from a uniform full-ring a; projection does not amplify coefficient errors. Actual small secret has h64 positive secret coefficients, first at zero publicly forced, remaining 63 lie one each in their prescribed smaller blocks. This is NOT an ordinary uniform sparse ternary distribution.
At N32768,h64:
 t=1: n'=32768, KSK projected ring samples=1, block secret support entropy log2 S=567
 t=2: n'=16384, ring samples=2, log2S=504
 t=4: n'=8192, ring samples=4, log2S=441
 t=8: n'=4096, ring samples=8, log2S=378
 t=16: n'=2048, ring samples=16, log2S=315.
Heuristic scalar flattening gives t*n'=32768 coefficient relations in all cases, but samples have special ring-circulant structure, so generic IID LWE estimators need caution. q=p≈2^60, sigma3.19. Paper's S^(1/4) type May21 attack lower-bound thought experiment gives numeric exponents141.75,126,110.25,94.5,78.75. THIS IS NOT A PROVEN ATTACK UPPER BOUND AND VALUES BELOW 128 DO NOT PROVE AN ATTACK.

## Evidence reproduced
Local stdlib verify_b093.py reconstructs v1.4.2 P/Q collision and p with deterministic 64bit primality test and tests 7 Ntoy32/64/128, h4/8,t1/2/4/8 configurations, at the SOURCE-DERIVED REAL p60bit. Uses source-shaped random independent uniform public mask a and independently rounded Gaussian errors as a TOY stand-in for native DGG. Exact full negacyclic product split into t reduced negacyclic ring products; total 506/506 projected zero-RLWE equations PASS. Does not constitute real attack, production sampler, or native OpenFHE.

A separate sage_estimator_diagnostic.sage is included but NOT RUN: SageMath and malb lattice-estimator are absent here. It specifies each N/t, actual p and sigma, t projected ring samples flattened for an APPROXIMATE LWE model; subtracts the public fixed s0=1 and models remaining h-1 positive bits as uniform SparseTernary over dimension N/t-1. This does NOT capture source's one-per-block constraint nor exact ring sample dependencies, thus cannot certify actual security even if run; true block-structured hybrid analysis remains necessary. Estimator source https://github.com/malb/lattice-estimator , Sage required. No fabricated numerical BKZ/dual/primal security estimates.

## Prior art and decision
Ma et al Practical Dense-Key Bootstrapping with Subring Secret Encapsulation ePrint2025/1594 https://eprint.iacr.org/2025/1594 studies known subring secret security context; this is a source-specific audit, not a new general attack primitive. Default published SPRU step=1 benchmark and security parameters are unaffected. We have proven that naive security neutrality for stride>1 cannot be inferred; we have NOT proven 128bit insecurity nor security. No native OpenFHE run, no credible Lattice Estimator output or explicit efficient key recovery for real N.

END OF ITERATION:
STATUS PASS_PINNED_PUBLIC_SAMPLE / BLOCKED_LATTICE_ESTIMATOR / UNCLEAR_128BIT.
RESULT Source-derived exact 60bit auxiliary p and sigma3.19, full source key relationship, 506/506 toy projected equations, no sub128bit attack.
NEXT_TEST B094 NOT STARTED: Unless human provides Sage/lattice-estimator and a live pinned-v1.4.2 OpenFHE runtime parameter dump, retain SPRU-stride as UNCLEAR security audit only, and prioritize independent fully sourced BOOT primitive search. If resumed, first compare t1/t2 real block-onehot distribution with estimator + independent attack model; do not misuse uniform sparse ternary model as certification.
STATE_UPDATE NO, existing boot-STATE.md huge and unreadable via isolated notes; preserve. SHIP untouched. Only BOOT-B093 appended.
REPRO /mnt/data/BOOT_B093_handoff.zip SHA256 ef07a9db47248e06a46ac9b1858e9b62b408e7ba66bbe52a0df5e00052016e9e. Complete report SHA256 0537e6360c372398d20c261971cc5de764839ffcf1ba1b3114f0650fb67ceb7b, verifier SHA256 a906831e0b80ac76353dcae130c5de38d93167496f9d357fd5148a4f6e00aad4, estimator script, JSON, logs, README and manifest; ZIP CRC and checksums verified.