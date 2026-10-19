# BOOT P2 parked — heterogeneous scale moduli do not beat continuous uniform baseline

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATIONS: B006–B007
STATUS: PARKED_STRUCTURAL_ADVANTAGE_FAIL

## What was attempted
Combine 2025/1711 squared Mat-MGSW scale-based external product with 2025/1892 heterogeneous approximate gadget choices to accelerate FHEW-like bootstrapping.

## Primary kill tests
1. B006: Directly substituting (B,d,delta) into square-gadget external product is not defined: square Mat-MGSW uses coefficientwise Round(Q/T*C*c), no G^{-1}(c). Naively reducing message scale without adjusting output scaling fails a noiseless scalar matrix example; compensating factor cancels and amplifies noise, without fewer ring products.
2. B007: Proposed heterogeneous per-key T_i does admit a no-noise algebraic composition in the scale-domain; 512/512 source-domain-compatible two-step monomial tests passed, but with source-homogeneous noise coefficients the continuous relaxation per-step variance is v_i=A(Q²/T_i)^2+B with A>0,B>0, strictly convex in log T_i. Jensen shows uniform geometric-mean T minimizes variance at fixed modeled logarithmic key size. Operation counts 2(k+r) FFT/NTT and (k+r)^2 pointwise products remain unchanged.
3. Discrete prime screen at source STD128 *shape* N=512,k=3,r=1,n=512,Q=2^18: synthetic 40/41-bit NTT-friendly primes give just 0.6098% theoretically bit-packed key-size saving for a mixed schedule under an arbitrarily chosen variance proxy; with both represented in 64-bit native coefficients key array bytes are identical, while mixed has higher modeled noise than uniform 41-bit. This is not a real secure, DFR-matched benchmark. Varying actual T_i also changes joint security and possible transform preparation cost.
4. The B006 toy Q=16,T=128/256 was outside Delta Q²<T and explicitly corrected in a read-before-append addendum to the B006 file. Source-admissible B007 toy uses T=769/1153.

## Decision
PARK not mathematically forbid mixed moduli; it may benefit discrete packing or stage-dependent weights A_i under a different scheme, but no distinct novel/speed/memory contribution was established here. Reopen only if one can prove unequal per-stage noise weights from the real algorithm, find a real machine-limb/packing advantage, establish security of joint multi-modulus keys, and benchmark versus optimal uniform T under identical DFR.

Technical evidence: findings/boot-B006-squared-gadget-heterogeneous-interface.md; findings/boot-B007-heterogeneous-scale-modulus-convexity-gate.md.
NEXT_ACTION: BOOT B008 P3 2025/1753 + 2025/1892 exact free-module/approximate-gadget interface test. Unrelated tracks untouched.
