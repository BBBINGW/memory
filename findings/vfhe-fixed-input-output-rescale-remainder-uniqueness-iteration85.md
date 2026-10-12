# Iteration 85 — Fixed pre-rescale input AND output uniquely determine bounded remainder in equal-bit prime regime

Date: 2026-10-12
Active target: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286 §3.2–3.4 and §4.1, soundness-preserving CRT lookup repair.
STATUS: **FAIL** for proposed fixed-output two-witness nonuniqueness (the initial candidate used the WRONG CRT projector), **PASS** for conditional uniqueness of the bounded rescale remainder under explicit paper-like same-bit CRT-prime assumptions. No compiled SNARK forging or soundness fix. No outreach/disclosure.

## Source and read-before-write
Read connected GitHub Notes `STATE.md` (last I84), `AGENT.md` and `findings/vfhe-rescale-remainder-public-computability-nonuniqueness-iteration84.md` before derivation. Read full 52-page cached primary source via Research MCP, ePrint 2025/286, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED against latest official. Primary anchors physical pp11 §3.2 z_l definition, p12 §3.3 Eq(6), p14 §4.1 Eq(12)–(15), p15 optimized 2^u bound, Appendix B p38.
IMPORTANT: PDF text extraction leaves math formatting fragmented. Our algebra is explicitly **conditioned on reading Eq(6)** as `t_l=[p_l^{-1}]_(q_{j+1}) * z_l`, using the canonical integer representative of the inverse modulo the retained product Q=q_{j+1}. Here `z_l=CRT(1 on retained AND current-to-be-dropped p_l, 0 on already dropped factors)` is exactly as defined in §3.2. A future visual source-check remains prudent if paper edition changes. DO NOT substitute z_(l-1) without source justification.

## One primary hypothesis and cheapest decisive test
[HYPOTHESIS, FALSIFIED] After fixing both pre-rescale component c' and the claimed output w_quot=c'', two distinct bounded remainder witnesses may satisfy the *full ring-level* Eq(13) because t_l has a kernel on the p_l-to-be-dropped component.
[FALSIFIER] Read Eq(6) and §3.2 to see whether t_l includes the dropped component; compute exact kernel for one admissible two-prime level, then prove a coefficient bound argument if possible.
[TEST] Reproduce one N=8,d=2 example in R_(p0*p1)[X]/(X^8+1) and derive a precise equal-bit uniqueness lemma. No FHE implementation or unrelated encoding variants.

## Critical correction to preliminary reasoning
The FIRST proposed example incorrectly used `t_wrong=[p_l^{-1}]_Q*z_(l-1)`, which zeroes the dropped-prime component. With this WRONG projected coefficient, a difference of Q=p0 is invisible, producing an apparent pair r=0 and r=p0 with identical claimed outputs. However, the SOURCE states `z_l`, not `z_(l-1)`, and §3.2 says z_l has CRT value 1 on p_l itself. Thus at the last stage l=L=1, z_l=1, not CRT(1,0).
This distinction is mathematically decisive and the initial nonuniqueness example is **invalid as a counterexample to the paper**. The correction was communicated to the PI explicitly in this round. It is an example of catchable proof interpretation error; do not recirculate the first verdict.

## Exact legally structured small-prime check
Set N=8,d=2, p0=73=8*9+1, p1=89=8*11+1, both distinct odd primes of same 7-bit size, both congruent 9 mod16 so Φ_16=X^8+1 has degree-2 irreducible factors. Let q0=p0*p1=6497, and use j=0, l=L=1 with retained Q=p0=73 and dropped p1=89, range B=2^7=128.
- z_l=z_1=CRT(1,1)=1∈Z_6497, whereas z_(l-1)=z_0=CRT(1,0)=2848.
- canonical [p1^(-1)]_Q=89^(-1) mod73=32.
- SOURCE t_source=32*z_1=32; gcd(t_source,q0)=1 (32 is nonzero modulo 73 and 89).
- WRONG t_wrong=32*z_0 mod6497=178, zero modulo 89.
Fix c'=0 and c''=0. r0=0 is allowed. An attempted alternative r1=73 satisfies 0≤73<128, but yields
   `(0−73)*32 mod6497=4161 !=0`, so it FAILS original Eq(13).
Under WRONG projected t, `(0−73)*178 mod6497=0`, illustrating the origin of error.
Therefore all bounded remainder coefficients are uniquely fixed by c',c'' in this particular ring; indeed t_source is invertible in Z_6497 so uniqueness holds for *any* coefficients in R_6497 here.
Full ring N8 constants (all nonconstant polynomial coefficients zero) tested. This is structural legal toy, NOT secure 49-bit prime setting and NOT a complete SNARK transcript.

## Conditional general uniqueness lemma: equal-bit RNS primes
[DERIVED, subject to exact Eq(6) reading] Suppose for one rescaling step the *active* CRT primes are distinct odd primes p0,...,p_l (l≥1), with each prime in (2^{u−1},2^u), and the prior dropped components are zeroed by z_l. Set Q=∏_{i=0}^{l−1}p_i, q_active=Q*p_l, and a the canonical integer inverse p_l^{-1} mod Q, 1≤a<Q. The source multiplier is t_l=a*z_l, hence at retained factors t_l≡a (modp_i)≠0, and at current dropped factor t_l≡a (modp_l). For fixed pre-output c' and claimed output c'', if two coefficientwise range-legal remainders r,r'∈[0,B)^N, B=2^u, satisfy
  `(c'−r)*t_l = (c'−r')*t_l` in R_q,
then each coefficient Δ of r−r' is divisible by Q.
- If l≥2, Q>2^{2u−2}≥2^u=B for u≥2. Since |Δ|<B, Δ=0 coefficientwise. The dropped factor never needs to be inspected.
- If l=1, Q=p0<B. Need the dropped factor. Here a∈[1,p0−1] and p0,p1 share bit length, so p0<2p1. If a≡0 modp1, then a=p1; this entails p0 divides p1^2−1=(p1−1)(p1+1). Since a=p1<p0, p0>p1; because both odd primes, p0≥p1+2, impossible for p0 to divide p1−1 or p1+1. Thus a≠0 modp1 and t_l is nonzero on BOTH active primes; Δ divisible by p0*p1>B. Therefore Δ=0.
Thus the strict bounded witness r is UNIQUE for fixed c',c'' across the active residue ring, under the above source multiplier and equal-bit assumptions. Polynomial quotient X^N+1 does not introduce a loophole here: t_l is a scalar element, hence its multiplication constrains each coefficient separately in the monomial basis. The proof does not need t_l invertible in the entire *full* q0 ring (it vanishes on already dropped components).
This lemma is not a claim that a verifier can cheaply reconstruct the witness. In §4.2 p16, c' and intermediate ciphertexts may be *prover nondeterministic witness oracles* and not public in full. Uniqueness conditional on **fixed c',c''** does not imply they can be computed from the public input/output alone. Also, this neither proves the original rescaling semantics exactly, nor repairs CRT-digit lookup soundness.

## Exact reproducibility
- `/mnt/data/iteration85_vfhe_fixed_output_remainder_kernel.py` SHA256 `4d3d91f873182f3dc8f6f601e9736a809a0dffa09711106bfa838413b60b0292`
- `/mnt/data/iteration85_vfhe_fixed_output_remainder_kernel_results.json` SHA256 `4aca013883f8df134164586f11bda38dc82ce4ef43ec430e5c51a17c515e8ebb`
Assertions PASS: both legal primes and same bit length, source z1, correct inverse and multiplier, wrong multiplier contrast, no nontrivial kernel for source instance, invalid proposed second r, unique fixed remainder. No crypto protocol emulation, no benchmarks.

## Consequence for active vFHE repair
[PASS] Reject the false kernel-based nonuniqueness attack on fixed c',c''. Under explicit equal-bit RNS assumptions plus source Eq(6) interpretation, prove bounded remainder uniqueness. Do not attribute a new soundness gap to the original paper.
[OPEN] The verifier may not know c' or all intermediate ciphertext coefficients without reconstructing a large circuit. Public A may leak aux witness to a client/verifier even if server computed it. A high-efficiency public-A cross-CRT link still needs a sound exact integer binding to h and field PCS and an end-to-end VC IND-CPA with VO argument. The independent I59–80 CRT lookup gap remains.
[PRIOR ART] CRT unit/injectivity and coefficient-bound argument is elementary ring arithmetic, no novelty claim.

## End of Iteration 85
STATUS: **FAIL** for proposed fixed-output witness ambiguity due to killed-component kernel; **PASS** conditional lemma of uniqueness under same-bit prime/actual multiplier assumptions.
RESULT: Corrected source projector z_l versus z_(l-1); N8,p73,p89 toy fails alternate remainder; fixed c',c'' enforce a unique bounded remainder in the paper-like equal-bit regime. This does not imply cheap *verifier* reconstruction or solve CRT range soundness.
NEXT_ACTION: ONE interface/cost test: given what a succinct verifier actually sees in §4.2/D.3 (input/output ciphertext commitments, oracle evaluations), can it reconstruct the **exact** rescale remainder or proposed public Boolean-mask A without decoding/processing the entire prover intermediate ciphertext witness? Pin down a single missing input / minimum processing obstruction before proposing any new PCS gadget. No author contact.
STATE_UPDATE: YES — correct I84 boundary and close false projected-kernel branch.
