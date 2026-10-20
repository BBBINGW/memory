# BOOT-B069 — Public twisted stabilizer: zero-key-switch correctness and fixed-field dimension gate
Date 2026-10-20. TRACK_ID BOOT. SHIP PAUSED.
STATUS PASS_TWISTED_AUTOMORPHISM_TOY / FAIL_FULL_DIMENSION_PUBLIC_TWIST_HYPOTHESIS / NO_REAL_RLWE_ATTACK_CLAIM

## Primary falsifiable hypothesis
H069: A public nontrivial RLWE secret relation sigma(s)=u*s+v permits a no-Galois-key-switch automorphism of RLWE ciphertexts while preserving a substantially full N-dimensional secret family. Test algebraic correctness and secret-space rank before any implementation.

## Sources and novelty
[FACT] Ma, Huang, Wang, Wang, "Practical Dense-Key Bootstrapping with Subring Secret Encapsulation", ASIACRYPT 2025 / IACR ePrint2025/1594, https://eprint.iacr.org/2025/1594 , PDF physical pp3–4 explicitly exploit automorphisms fixing a subring secret to omit key switching; security is based on dense RLWE in the smaller ring. Thus the fixed-secret special case is established prior art, not a novelty claim.
[FACT] Bernard and Joye, "Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys", ASIACRYPT 2025 / ePrint2025/163, https://eprint.iacr.org/2025/163 ; their automorphism-parametrized external product combines operations using full secret distributions, a distinct prior-art route for saving separate switches.
[MATH SOURCE] Cyclic Hilbert 90 and fixed-field characterization, https://math.ucla.edu/~sharifi/notes/algebra-ch10.html Theorem 10.1.12.

## Mathematical derivation
Let K=Q(zeta_(2N)), sigma of finite order r, E=K^{<sigma>}. Use decryption convention b-a*s=m+e. If public unit u and public v satisfy sigma(s)=u*s+v, define a'=u*sigma(a), b'=sigma(b)-v*sigma(a). Then b'-a'*s=sigma(m)+sigma(e). Since cyclotomic sigma is a signed permutation on the power basis for negacyclic rings, direct coefficient automorphism does not increase error infinity norm. This is exact public transformation, not a generic key switch.

The secret constraint is a hard limit: if w !=0 satisfies sigma(w)=u*w, every solution is w*z for z in E (because sigma(s/w)=s/w). Thus a nonempty homogeneous solution space has Q-vector dimension dim_Q(E)=N/r, not N. If no w exists, nonzero secret solution count zero. For fixed public v, differences of two solutions obey homogeneous relation; hence any affine family has the same maximum dimension. Hilbert 90 shows consistent field-level twists u amount to a change of basis of a fixed-field solution set. A field witness may be nonintegral or nonshort; do NOT assume any twist yields an FHE-suitable distribution. For public monomial w=X, u=X^(t-1), the change of basis is explicit, short and a signed coefficient permutation. Public affine c gives s=X*z+c and v=sigma(c)-u*c. This does not improve secret entropy or automatically prove insecurity at a desired dimension.

## Reproducible exact finite-ring tests
[TEST] Script verify_b069_twisted_stabilizer.py SHA256 f23559c0135c1f43aae26732e77a28fda1ad4b69f06cde33c20bb6e283897bf5, R=F_257[X]/(X^16+1), q≡1 mod32, exact signed automorphism and polynomial ring operations and modular-Gaussian-elimination kernel basis.
Kernel dimensions for u in {1,X^(t-1),-1}:
  t31 order2: nullity8/16 for all three u
  t9 order4: nullity4/16 for all
  t5 order8: nullity2/16 for all
  t15 order2: nullity8/16 for all.
These confirm the N/r exact dimension bound for these choices in the split finite-ring toy, but do NOT prove a universal modular 2^w rank theorem.

For t31,9,5, 100 randomly sampled structured secret/mask/message/error cases each: 300/300 exact transformed RLWE decryptions, 300/300 public affine corrections, 300/300 trace reductions, and 300/300 coefficient error infinity-norm preservation. Omitting twist correction led to mismatch in 294/300 cases (remaining cases can coincide). Trace: with s=X*z, sigma(z)=z and A=X*a, Tr_H(b)=Tr_H(A)*z+Tr_H(m+e); trace noise may be correlated and grows with r.

For t5 fixed rank2, ternary coefficients on two signed-orbit basis vectors give 3²=9 toy candidate secrets, vs 3^16 ordinary ternary input coefficient possibilities. Two public noisy ring samples after group trace leave exactly 1/9 candidates, correct (1,-1). This is a specially restricted toy family, not a cryptanalytic attack on published RLWE/FHE or a 128-bit cost estimator.
Result JSON b069_results.json SHA256 9236c30a09a2fb10e8609ae1e1c0cbbbc73af34d18103f2eb97b4b1707e423e0 and full BOOT_B069_handoff.zip in local sandbox.

## Decision
PASS: public twisted stabilizer removes selected online key switching at correct same-secret decryption type.
FAIL H069 as a **new full-dimensional secret construction**: fixed u,v reduce to a subfield/fixed-field coset of rational dimension N/r. Already exploited in Ma2025 subring method, and monomial twist is only a public rotated version.
SECURITY: dimension reduction alone is not a break; smaller subring can be secure with adequate parameters. No native FHE implementation, proof of end-to-end DFR, key bytes or runtime measured. Avoid calling this new publishable primitive.
STATUS FAIL_NEW_PUBLIC_TWIST_NOVELTY_AND_FULL_DIMENSION.
RESULT Exact construction passes; entropy and prior-art gates kill proposed new primitive; preserve safe subring technique as known reference.
NEXT_TEST B070 (not started): choose exactly one full-entropy-secret online switch-amortization candidate using orbit-labelled GLWE ciphertexts, compare with Bernard-Joye automorphism-parametrized ExtProd before any construction; test whether adjacent gadget products can compose under transformed keys without exponential orbit-specific GGSW keys. Analyze key transcript and noise; early stop on interface/key explosion.
STATE_UPDATE NO: original findings/boot-STATE.md returns empty object using connected GitHub Notes despite listing 187967 bytes; do not overwrite. Append-only B069 findings created, SHIP unchanged.
