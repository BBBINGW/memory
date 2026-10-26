# PURE-FHE P0-PRESCOUT-33 — Odd-modulus obstruction to candidate-free integer carry shift

Date: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-32
STATUS: FAIL_PUBLIC_INTEGER_AFFINE_GAUGE_FOR_ODD_MODULUS / PASS_EXACT_DIVISIBILITY_OBSTRUCTION
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO (no GPU, native, server, code or environment modifications)
STATE_UPDATE: YES, isolated finding only; global STATE.md and other tracks unchanged.

## One falsifiable H33
Hypothesis: In the general arbitrary-modulus A2D of Liu, Ma, Wang, Wang, ePrint 2026/1869, choose public integers H_j so that shifting all bounded integer carries as c_j=tilde_c_j+lambda*H_j completely removes the unknown lambda from the radix transition equations, preserves the canonical radix digits d_j, and retains a known lambda-independent initial carry c0=0. This could avoid materializing |Lambda| candidate-specific transitions after the second multi-value functional bootstrap.

Cheapest decisive test: derive exact divisibility from the original equation and verify two exact source polynomials. No CKKS operation or benchmarking necessary if the recurrence fails.

## [FACT] Primary source and prior art
Original user-supplied papers/supplied/2026-1869.pdf SHA 9de785af66b3106e509283c84816513d56f6f7dd, §3.1 p11, §3.4 p16, §5.2 pp21–23, Appendix C.1–C.3 pp36–39. The paper defines monic F_M(X)=X^d+sum_{i<d}f_iX^i with F_M(b)=M. Its Eq(2) gives
 a_j=d_j+c_j−B*c_{j+1}−lambda*alpha_j
with c0=0, lambda=kappa+I'_{d−1} and B=b^s, except last radix b^h. The candidate-dependent carry transition is f_{j,lambda}(c), Eq(3). The authors' Eq(5) already states m_{0,lambda}+kappa_lambda b^d=m+(lambda−lambda*)M; hence an M-dependent ambiguity is explicitly part of their derivation. Appendix C.2 p39: second FBT produces |Lambda|(|C|²+|C|(1+h_kappa)) ciphertexts; carry composition complexity includes |Lambda||C|³. That is the source-side motivation but not evidence of an unavoidable lower bound.
The supplied contemporary ePrint 2026/1840 already handles the *power-of-two* binary carry map by a compressed three-state representation (p19–20); it does not establish the generic prime-modulus quotient elimination proposed here. Source-first search found no independently verified equivalent positive construction, but lack of hits is not evidence of novelty.

## [DERIVATION] Gauge obstruction
Use varying radices R_j=B for j<ell−1 and R_(ell−1)=b^h with h=d−s(ell−1), ell=ceil(d/s). Source eq:
 a_j=d_j+c_j−R_j*c_{j+1}−lambda*alpha_j.
Try c_j=tilde_c_j+lambda*H_j for public H_j integers, preserving canonical d_j and known initial zero carry. Substitution gives
 a_j=d_j+tilde_c_j−R_j*tilde_c_{j+1}+lambda*(H_j−R_j*H_{j+1}−alpha_j).
Removal of lambda requires H_(j+1)=(H_j−alpha_j)/R_j. Since c0=0 and unknown lambda can vary by one, a lambda-independent zero tilde_c0 forces H0=0. The first shift H1=−alpha0/B must be integral.
Here alpha0=sum_{r=0}^{s−1} b^r f_r; because F_M(b)=M and d>=s, all remaining groups and leading b^d are divisible by B=b^s, so alpha0 ≡ M (mod B). Consequently a necessary condition is B|M. For odd M and B=32 this fails universally irrespective of choosing a different defining polynomial F_M with the same value M at b.

For all j, let P_j=product_{u<j}R_u, P0=1 and P_ell=b^d. The recurrence implies P_(j+1)H_(j+1)=P_jH_j−P_j alpha_j. Summing:
 b^d H_ell = −sum_j P_j alpha_j = −sum_{i=0}^{d−1} b^i f_i = b^d−M.
Hence EXACT H_ell=1−M/b^d. Requiring an integer shift for the final carry additionally forces b^d|M (necessary, not sufficient for all intermediate shifts). If gcd(M,b)=1, its reduced denominator is b^d.
Allowing H0 nonzero simply moves unknown lambda to the initial state. Allowing rational shifts, a different digit representation, an extra bootstrap or a non-affine quotient mechanism escapes the scope of this particular no-go.

## [TOY_EXECUTED] Independent exact integer/fraction checks
Executed Python with arbitrary-precision integers and fractions, verifying author F(2)=M, alpha0, recurrence H_j across the entire radix chain and H_ell=1−M/2^d:

1. P-384: d=384, b=2, B=32, M=2^384−2^128−2^96+2^32−1. Source F=X^384−X^128−X^96+X^32−X²+3. alpha0=3−4=−1=M mod32 (31), H1=1/32 noninteger. ell=77 with final radix16. Reduced denominator of H_ell is 2^384.
2. Curve25519: d=254,b=2,B=32,M=2^255−19. Source F=sum_{i=0}^{254}X^i−X^4−X²+2, so f0=3,f1=1,f2=0,f3=1,f4=0. alpha0=3+2+8=13=M mod32. H1=−13/32 noninteger. ell=51 with final radix16. Reduced denominator H_ell is 2^254.
3. Control: if M=b^d and F=X^d−X+b, all alpha groups vanish (s>=2), H_j=0 and the known binary carry specialization is consistent.

## Scientific decision
FAIL the specific free public-integer affine carry gauge for arbitrary odd prime moduli. This is an exact representational obstruction and explains why the binary/power-of-two case is special. It is NOT a lower bound against all candidate-independent A2D protocols, two-FBT constructions, integer computation or cryptographic security; unknown lambda can be carried in other representations or selected after computation. The result is a straightforward corollary of paper Eq(2) and Eq(5), not an originality claim and no new positive FHE mechanism. No additional same-family toy variants warranted.

END_OF_ITERATION:
STATUS: FAIL_INTEGER_GAUGE_FOR_ODD_MODULI / PASS_DIVISIBILITY_GATE
RESULT: necessary B|M and b^d|M for the specified complete integer gauge, falsified on exact P384 and Curve25519 author polynomials.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: source-first independent PURE-FHE mechanism candidate, not another lambda carry-shift reparametrization. If future work revisits arbitrary-M A2D it needs non-affine candidate-free representation with exact terminal validation and full noise/time/key costs.
STATE_UPDATE: YES isolated PURE-FHE finding only.
CODEX_REQUIRED: NO, engineering PENDING explicit PI authorization.
