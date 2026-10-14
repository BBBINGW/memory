# vFHE V31 — Transitive Per-Prime Representative Link for Canonical CRT Digits

Date 2026-10-15. **Independent V31**, global FHE I192 FROZEN.

## One primary hypothesis and one decisive test

**H-V31:** Conditioned on sound F.1/F.2 native polynomial commitments and an actually knowledge-sound shared, range-bounded canonical integer commitment/evaluation CP, can the V30 prime-local native field-isomorphism alignment REDUCE the number of expensive cross-characteristic evaluations from ONE PER CRT EXTENSION FACTOR to ONE PER RNS PRIME, without losing a malicious factor mismatch? Test a source-form p13/p29 two-factor case with a nonreference-only mismatch and a whole-prime mismatch, and verify canonical integer quotient constraints exactly.

**STATUS PASS conditional transitive theorem and exact finite extension toy; UNPROVEN actual cryptographic CP implementation, true end-to-end cost, privacy and publication novelty.** All results refer to our proposed repair, NOT original paper. Existing latest official Feb2026 ePrint PDF binary VERSION_UNVERIFIED.

## Paper evidence [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025/ePrint2025/286, inspected GitHub mirror 52 physical pages SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19:
- §3.1 physical p10: p=1+(2N/d)*odd, each prime factor splits into k=N/d degree-d native extension fields.
- §4.3 pp20–24: native digit-table lookup; our common-integer CP is not present in this source.
- Appendix F.1 p50: polynomial commitment for Rq is a tuple of native F_(p^d) polynomial commitments. The CRT decomposition supports prescribing each factor's evaluation point separately.
- Appendix F.2 p51: native Merkle/RS field evaluation publicly sends v'=q1 Uf and checks Enc(v') on Q' and y=<v',q2>. Any hypothetical cross-char proof must authenticate THIS evaluation; Pedersen binding alone cannot be assumed to do so.

Prior vFHE V14/V16 derived the exact required base-coordinate quotient witnesses and folded native residuals CONDITIONALLY on a common bounded a; V30 gave per-prime factor alignment. V31 is an explicit COMPOSITION of these known ideas, not an assertion of a new proof primitive.

## Transitivity theorem [DERIVATION]

For native prime p_i, let K_(i,j)≈F_(p_i^d), j=0,…,k−1; publicly fixed Fp-linear field isomorphisms psi_(i,j):K_(i,j)→K_i. Let native precommitted MLE h_(i,j)(X) have ell variables and fix ONE precommitted global canonical integer vector a∈{0,…,beta−1}^{2^ell}. Let A_i(X) be the multilinear extension over K_i of the canonical reductions a mod p_i. AFTER all commitments, independently sample full-extension point r_i←K_i^ell. With original sound native PCS authenticate each native evaluation and demand normalized identity

  psi_(i,j)(h_(i,j)(psi_(i,j)^−1(r_i))) = psi_(i,0)(h_(i,0)(psi_(i,0)^−1(r_i))) for every j>0.

Use ONE sound cross-characteristic CP statement PER PRIME requiring the reference native value at r_i equals A_i(r_i), proven using the SAME precommitted canonical a. Every native factor must then agree with common a at that point by transitivity. If a polynomial coefficient is wrong anywhere, at least one difference MLE above is a nonzero polynomial of total degree ≤ell. Fix that difference before challenge. By Schwartz–Zippel over native K_i, Pr[false algebraic accept]≤ell/p_i^d, plus sound native PCS and CP errors (challenge order mandatory). No k penalty is required for a fixed violated equality. This is not yet a composition theorem for the actual compiled F.2/Fiat–Shamir protocol.

### Cross-characteristic proof MUST be explicit

For reference-field evaluation y_i in K_i, write chi_b(r_i)=Σ_(t=0)^(d−1)c_(i,b,t)theta^t, canonically lift coefficient c_(i,b,t) to integers [0,p_i−1], and each native PCS-authenticated y_(i,t) to [0,p_i−1]. Genuine cross-characteristic CP must prove KNOWLEDGE of same a and bounded integer quotients k_(i,t) satisfying
  S_(i,t)=Σ_b lift(c_(i,b,t))*a_b = lift(y_(i,t))+p_i*k_(i,t),
each 0≤a_b<beta; ensure 0≤S_(i,t)<r, proof-scalar field order r, plus genuine ranges and native PCS-extracted y. The in-ring field coordinate map is not a homomorphism into unrelated proof field. Neither the source F.2 nor bare Pedersen commitment establishes this. Can pack all d relations into a CP circuit; number of constraints/proof size not automatically d.

## One exact finite-field reproduction [EXPERIMENT]

Source-form N4,d2, ell3,H8,beta4, p13=1+4·3,p29=1+4·7. Each prime has TWO quadratic extension factors. Choose respective reference u²=5,u²=12, secondary u²=8,u²=17, with true isomorphism secondary u→5u_ref (p13), →12u_ref (p29). Irreducible quadratics and isomorphisms verified independently by code. Fix canonical integer vector a=(0,...,0) BEFORE challenges and use ideal native evaluation and integer-checking interface; toy SHA digest only records input, not a real commitment. External demonstration scalar r=1009 is PRIME and >3*8*(29−1)=672 so no wrap in any honest toy lifted linear sum.

For EACH p run 8192 uniform full-degree2 extension challenge r∈K^3:
- Honest two factors both all-zero digits: both alignment+ideal CP accept 8192/8192 for each p.
- Attack A, reference all0, secondary one Boolean digit1: CP reference accepts 8192/8192, factor alignment accepts ONLY 175/8192 at p13 and 35/8192 at p29; joint also only 175/35.
- Attack B, both factors same one Boolean digit1, but shared precommitted canonical a all0: alignment accepts 8192/8192, ideal CP accepts ONLY 175/8192 at p13 and 35/8192 at p29. Thus each layer rejects the cheating family invisible to the other layer.

Exact one-coordinate miss probability 1−(1−1/p²)^3: p13 85177/4826809, p29 2119321/594823321. Samples merely corroborate derived expression. Nontrivial honest canonical a=(0,1,2,3,0,1,2,3) with r=(2+3u,4+5u,6+7u):
p13 native y=(10,0), integer S=(88,104), exact quotient k=(6,8);
p29 native y=(10,13), integer S=(242,187), quotient k=(8,6).
All satisfy S=y+p*k and fit r1009. Modifying y by +1 FAILS the toy canonical quotient constraint. Our toy integer verifier is NOT a ZK/knowledge-sound CP and does not prove the native Merkle source binding. Previous illegal CRT value261 mod377 (1 mod13,0 mod29) passes within-prime alignment but fails an authenticated common-a representative link for mismatching prime except with the polynomial identity-test collision probability.

## Conditional cost and limitations

Illustrative source-like N16384,d4,L2 primes, k4096 native extension factors/p, mu8192 total, ellstar24,H2^24. Naively linking each factor to the common a costs mu=8192 separate cross-characteristic evaluation relations, with direct unoptimized base-coordinate digit/weight operations mu*d*H=549755813888. Our V30-alignment composition needs L=2 such cross-characteristic relations with dense direct L*d*H=134217728 operations, **4096x fewer LINKS and dense CP-layer coefficient products**. However it STILL needs 8192 native factor F.2 evaluations, extra internal comparisons, and ONE actual strong CP circuit on a 16M-entry bounded integer vector; no measurable network/time/memory improvement, proof size or published uniqueness established. For compatible 49-bit p_i, S_i direct canonical lifted sum is at most 74 bits and fits within a 253bit proof scalar field once bounded; quotient constraints remain compulsory.

**Decision:** PASS conditional algebraic transitivity, FAIL any assertion it delivers a full cryptographic vFHE soundness repair or 4096-fold overall speedup. High risk original F.2 Merkle binding+non-native CP dominates; optional ZK hidden-root branch already PARKED. Official revised 2026 IACR binary still not authenticated. Avoid author contact absent PI instruction.

**Next V32 only with PI continuation:** one real knowledge-sound CP for the REPRESENTATIVE original native Merkle/RS evaluation+bounded integer quotient equality, with clear prover work and challenger-order binding; compare against V12–V16 and prior art. Otherwise HUMAN_REVIEW and acquire authoritative current PDF.

**Artifacts (local, created and run twice):** script /mnt/data/vfhe_v31_representative_link_gate.py SHA256 1d4c9e0762f631706dbf6f5fc5f27e254a346fcaa08ffc0cae9dd3db7a0618e1; JSON /mnt/data/vfhe_v31_transitive_representative_gate_results.json SHA256 9c3ac6670f9f3c95ee367473f42af915453aabb7072cafe7ad335b651e950a11; complete report /mnt/data/VFHE_V31_Transitive_Representative_CRT_Link_Gate_2026_10_15.md SHA256 872dc42b964329ac8ee1d6f3e5261bf5d7644a661da78329c27af62e1e9d1d85.

End: STATUS PASS conditional toy / UNCLEAR real CP, RESULT full interface + two independent attack-detection gates, NEXT_TEST V32 representative authentic CP cost, STATE_UPDATE YES vFHE only; global I192 frozen.
