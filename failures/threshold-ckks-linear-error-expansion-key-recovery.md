# Iteration 57 — Key recovery from public-key/evaluation-key errors reused by a public ring automorphism

Date: 2026-10-10
Target: Min, Hanrot, Park, Passelègue, Stehlé, *Distributed Key Generation for Efficient Threshold-CKKS*, ePrint 2025/2057 (CCS 2026), §4.4 physical p.23.
PRIMARY STATUS: FAIL — a proposed LOW-DEPTH MODIFICATION of §4.4 using e_auto=phi(e_pk), derived from one secret error e by a **public known ring automorphism**, catastrophically reveals the common secret key with high probability. 
CRITICAL: This is NOT an attack on the paper's original protocol, which proposes well-distributed (PRF-based) independent-like errors. NOT a claim that every form of error reuse is insecure. NOVELTY LOW: classic correlated/noise-cancellation intuition and direct algebra; no new viable FHE algorithm.

## Protocol continuity and provenance
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, parked RIG-HE STATE.md and previous I56 `failures/threshold-ckks-prg-seeded-error-joint-distribution.md` before setting this hypothesis; reserved STATE.md untouched. I55–I56 shared-seed PRF candidate archived. One primary hypothesis with one minimal decisive attack.
[PRIMARY FULL PAPER] Min et al. IACR ePrint 2025/2057, complete 52 physical-page PDF via connected Research MCP, SHA256 `519d1c9672c743b49307de8ebaa1015ba44ff089fae0d1e754482abe40ef764d`, VERSION_UNVERIFIED. §4.4 p.23 (not implemented main 4-round scheme): authors say the public-key term is computed as `a ⊙ ct_sk + ct_err`, and automorphism-key term as `a ⊙ ct_sk + P*phi(ct_sk)+ct_err`; after decryption these yield ring expressions `b_pk=a0*s+e_pk`, `b_auto=a1*s+P*phi(s)+e_auto` under common final s. Modulus PQ and its RNS factors; choose a single odd NTT-compatible CRT prime q|Q with q coprime to P. The source uses distinct well-distributed errors; NO relationship `e_auto=phi(e_pk)` is claimed by the authors.
[ADDITIONAL SOURCE] §4.1 Footnote 6 p.18, §4.2 p.20 mention PRF-expanded shared randomness; neither proposes a public linear automorphism of ONE error across final key types.
[PRIOR ART] Koo, Lee, No, Kim, *Key Reduction in Multi-Key and Threshold Multi-Key Homomorphic Encryptions by Reusing Error*, IEEE Access 11:50310–50324 (2023), DOI 10.1109/ACCESS.2023.3277862, publisher https://ieeexplore.ieee.org/document/10129910/; existing ReRLWE work explicitly studies *structured* error reuse under a modified key/sampling formulation and an RLWE-related assumption. Its cited sample has form `(a, a*s+x, a*x+e)`; this is NOT the publicly cancelable relation studied in the present attack. Do not assert their proposed scheme is broken or that all forms of error reuse fail. Relevant adjacent CKKS key recovery literature: Guo et al., USENIX Security 2024 on non-worst-case noise flooding https://www.usenix.org/conference/usenixsecurity24/presentation/guo-qian ; a different attack context, not proof of ours.

## Primary hypothesis and predeclared falsifier
[HYPOTHESIS — FALSIFIED] To avoid a costly homomorphic PRF for each final public/evaluation key error, homomorphically generate one well-distributed small error e and form further error e_auto=phi(e) using a known low-depth automorphism (which preserves the marginal signed-coefficient distribution), while retaining the secret-key security of the public + automorphism keys.
[FALSIFIER] Show a public efficient transformation eliminating BOTH errors and recovering common final s by solving a linear system over a CRT prime factor of the evaluation-key modulus.
[CHEAPEST DECISIVE TEST] Exact symbolic cancellation + invertibility argument for all NTT-friendly q, verified by a deterministic exact negacyclic 8-degree numerical witness (single instance, independent-error control, NO parameter sweep, NO real encrypted DKG).

## Exact general attack
[DERIVED] Work in R_q=F_q[X]/(X^N+1), q prime, q≡1 mod 2N. Let phi be a nontrivial public cyclotomic automorphism phi(X)=X^k, gcd(k,2N)=1. Take one final secret s, publicly uniform a0,a1 in R_q, nonzero auxiliary P mod q and independent small error e. Publish:
 b0 = a0*s + e,
 b1 = a1*s + P*phi(s) + phi(e).
Both e and phi(e) individually have the same marginal coefficient distribution whenever the error is iid symmetric under coefficient sign; their JOINT distribution is intentionally correlated.
Adversary computes:
 c := b1-phi(b0)
   = a1*s + (P-phi(a0))*phi(s).
This is a PUBLIC and **NOISE-FREE** F_q-linear equation in s (phi is F_q-linear), even though s is not known.
Let A=a1, C=P-phi(a0), and let primitive evaluation roots {zeta_i} be the N roots of X^N+1 in F_q. In the NTT basis, phi simply permutes S_i=s(zeta_i) by pi determined by zeta_i→zeta_i^k:
 c_i = A_i*S_i + C_i*S_{pi(i)}.
For each cycle of pi, the linear-system determinant is a polynomial in the independent uniform A_i with total degree equal to cycle length, including monomial prod_(cycle) A_i with coefficient 1, so it is NONZERO. The full determinant is nonzero polynomial of total degree N. Since A_i are independent uniform F_q for uniform a1∈R_q, Schwartz–Zippel gives Pr[singular] ≤ N/q, for every fixed a0. Thus polynomial-time Gaussian elimination in F_q or an NTT-cycle solver recovers all S_i with probability ≥1−N/q; inverse NTT recovers exact s modulo q. For q≈2^60,N=2^16, singularity ≤2^-44. CRT across prime factors is not even needed: one q reveals small ternary s coefficients uniquely if q>2. A single CRT component may suffice if its public residues are available.
This is a **key recovery**, not just a distribution distinguisher. The attack is not constrained by e's size, because cancellation is exact.
If e_auto were instead independently sampled e2, then public combination c would contain residual e2-phi(e), and cannot be solved exactly by this noiseless linear system; no claim independent errors guarantee other security properties.

## Deterministic exact witness
[EXPERIMENT] Python `/mnt/data/iteration57_linear_error_automorphism_attack.py`, SHA256 `d0f093988a15aeb0441477774641b0f121679a602304278ff7a8e29c98d17faa`. Output `/mnt/data/iteration57_linear_error_automorphism_attack_results.txt`, SHA256 `3d889781b669be4a56f6b5723e6a266b9137eaee3ae326f8bf7b44b71077c579`.
R=F_97[X]/(X^8+1), k=3, P=5. Random fixed a0/a1 generated reproducibly (seed 20261010); s=[1,0,-1,0,1,0,0,-1], error e=[0,1,0,-1,0,1,0,0]; b0,b1 exactly as above. Construct public linear map L(v)=a1*v+(P-phi(a0))*phi(v), 8x8 matrix from its monomial basis columns; invert mod97; exact recovered s=[1,0,96,0,1,0,0,96] mod97, PASS. Independent-error control substitutes e_auto=[1,0,1,0,-1,0,1,0], confirms residual e_auto−phi(e) nonzero. Does NOT instantiate BFV/CKKS encryption, relinearization, distributed decryption, Gaussian errors, realistic security, or runtime. The general inversion argument is mathematical and is not dependent on the toy dimension.

## Research and security judgment
[NEGATIVE] Publicly linearly related error samples across a public key and an automorphism key with same secret can destroy secret-key secrecy despite each sample having the correct marginal RLWE error distribution. This specifically kills "one encrypted error + derive all errors by known ring automorphisms", a proposed near-zero PRF-depth candidate.
[NOT UNIVERSAL] Strong multioutput PRGs can yield computationally pseudorandom correlated errors; such correlations are *not publicly algebraically cancelable*. Koo et al. 2023 ReRLWE uses error in a structurally different secret role under a modified assumption. Do not generalize this attack to all error-reuse schemes or challenge their proof without inspecting their actual schemes/assumptions.
[NOT ORIGINAL PAPER ATTACK] Original Min et al. §4.4 has no mandated public linear-error reuse. Author notes proper PRF error sampling and other methods. The attacked construction is OUR hypothetical modification; paper is unaffected.
[NOVELTY] Despite a crisp exact high-success key recovery, mechanism is elementary linear algebra/noise cancellation, anticipated by literature on structured RLWE noise, so probably not a publishable cryptographic contribution. Do not implement real scheme or continue trivial variants.
[OPEN] Whether a secure, *low-depth*, computational PRG/PRF-based full error sampler actually saves bootstraps and meets distributed transcript security remains open. Plain SIMD and simple shared-seed ideas already audited in I55–I56; no new secure sampler produced.

## End of iteration 57
STATUS: FAIL — public automorphism-expanded error sampler would reveal final secret under the tested pair of published key component forms.
RESULT: Exact identity c=b_auto−phi(b_pk)=a_auto*s+(P−phi(a_pk))*phi(s) and invertibility probability ≥1−N/q for q≡1 mod2N (assuming uniform public a); one explicit exact ring example recovers s; independent error control removes the noiseless equation. ReRLWE prior art limits novelty and universality.
NEXT_ACTION: HUMAN_REVIEW recommended: ARCHIVE the Threshold-CKKS §4.4 PRF-error-sampling subbranch unless a new candidate simultaneously offers a security-appropriate NONLINEAR pseudorandom map and a concrete reduced-depth BFV circuit. For a productive next independent target, return to full-text construction-level matrix-FHE literature (e.g. ePrint 2025/1935), with one precise nontrivial algebraic/precision assumption; avoid more trivial error-correlation variants. Human retains final pivot decision.
STATE_UPDATE: NO — parked RIG-HE STATE.md untouched.
