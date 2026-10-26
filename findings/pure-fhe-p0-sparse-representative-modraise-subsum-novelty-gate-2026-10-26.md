# PURE-FHE · P0-PRESCOUT-13 — Representative Extraction after ModRaise / SubSum Prior-Art Gate

- Date: 2026-10-26 (Asia/Hong_Kong)
- TRACK_ID: PURE-FHE
- PREVIOUS: P0-PRESCOUT-12
- H13: For periodic CKKS message slots, simply retain a small set of slots immediately after ModRaise, homomorphically EvalMod those representatives, and replicate to reconstruct the full vector; can this bypass generic CoeffToSlot/key switching?
- MINIMAL_TEST: exact cyclotomic toy R=Z[X]/(X^8+1), CKKS four slots at exponents 1,5,9,13; q=16.
- STATUS: FAIL_NAIVE_REPRESENTATIVE_EVALMOD; PASS_TOY_TRACE_CORRECTNESS; FAIL_NOVELTY_SUBSUM_PRIOR_ART.
- NOVELTY: NOT_ESTABLISHED. No implementation / no security claim.

## [DERIVATION] Exact CKKS embedding counterexample

Let ζ=e^(2πi/16) and the four canonical slots be σ_j(f)=f(ζ^(5^j)), j=0..3. Let m(X)=1+X². Since ζ^(2*5^j)=(-1)^j ζ², σ(m)=(a,b,a,b), a=1+ζ² and b=1−ζ²; hence m is invariant under the σ_9 two-slot rotation.

ModRaise is modeled at plaintext level as m'=m+qI; choose q=16, I=X. Then σ_j(m')=σ_j(m)+16ζ^(5^j), and σ_0(m')−σ_2(m')=32ζ ≠ 0. Hence direct post-ModRaise representative-copy is not correct in general.

Even the simplistic coordinatewise (real and imaginary) centered mod 16 does not eliminate the lifted term: σ_0(m)=1.70710678+0.70710678i; σ_0(m')=16.4891793+6.8300417i; coordinatewise centered reduction gives 0.4891793+6.8300417i, not σ_0(m). This only kills the naive Cartesian EvalMod, not all possible non-Cartesian nonlinear representations.

J=X is a valid algebraic ModRaise quotient term, but this toy does not prove that this exact quotient is realized by a particular prescribed key/ciphertext sampler; no distributional security statement.

## [DERIVATION] Repair equals old SubSum

In R, X^9=-X. Define τ(f)=f(X^9)=f(-X) and formal P=(Id+τ)/2. It extracts only even coefficients. Thus for m∈Z[X²]/(X^8+1), P(m+qI)=m+qP(I). E.g. I=X+X² yields P(m+16I)=1+17X². The general degree ratio k counterpart is an averaging relative trace across a Galois subgroup; it selects a subring before CoeffToSlot.

The factor 1/2 is a *formal integer-plaintext* projection; when 2 is not invertible mod ciphertext modulus, implementation must use unnormalized trace and account for scaling, and automation of τ on an encrypted ciphertext usually needs evaluation-key/key-switching. This is neither free nor guaranteed to improve end-to-end.

## [FACT] Prior Art and Scope

- Min, Lee, Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, ePrint 2025/429, §2.4, physical page 5 (0-index p4) explicitly uses ModRaise→SubSum→CoeffToSlot→EvalMod→SlotToCoeff for sparse packed ciphertexts; the Q0I term generally exits the subring and a trace-like map extracts the appropriate coefficient subset. https://eprint.iacr.org/2025/429.pdf (web text lines 253–285; web PDF screenshot request returned 403).
- Coron–Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, pp. 36–67; source PDF shows conventional ModRaise m+qJ and moving integer coefficients into slots (original preprint physical pp.2–4) and a different new partial CtS construction. https://orbilu.uni.lu/bitstream/10993/64983/1/PaCo.pdf (web screenshot cache miss; ePrint mirror connector version unverified).
- CKKS bootstrapping survey (2025), sparse packing and coefficient-selection background: https://link.springer.com/article/10.1186/s42400-025-00384-3 .
- High-Precision Bootstrapping of RNS-CKKS (EUROCRYPT 2021), original CoeffToSlot EvalMod accounting: https://iacr.org/archive/eurocrypt2021/126960128/126960128.pdf .

## [DERIVATION] Cost / security consequences

Naive physical slot replication cannot fix arbitrary qI in the canonical embedding. The correct relative trace/P_H may need automorphism evaluation keys, key switching, normalization of the trace multiplier, and enlarged noise. Sparse representation decreases independent message capacity, but fixed-N ciphertext multiplication complexity need not decrease. Total bootstrap complexity includes ModRaise, SubSum, CtS, EvalMod, StC, full eval-key memory and precision/DFR.

## Decision

Kill direct representative-slot copy and ordinary coordinate EvalMod proposal. Do not present known sparse SubSum as new. The abstract possibility of another representation/evaluator remains open, but requires a concrete new invariant and a measured cost frontier.

NEXT_TEST: PRETRACE_VS_POSTTRACE_LIFT_NONCOMMUTATIVITY_GATE — can moving an exact subring projection before ModRaise retain its intended effect without altering ciphertext semantics? Kill via coefficient-level modular lifting toy and then audit prior schemes. One primary hypothesis, one decisive cheapest test.

END_OF_ITERATION:
STATUS: FAIL
RESULT: post-ModRaise slot periodicity fails; normalized trace gives correct selected-coefficient algebra; SubSum covers idea.
NEXT_TEST: PRETRACE_VS_POSTTRACE_LIFT_NONCOMMUTATIVITY_GATE
STATE_UPDATE: YES (this finding only; do not modify other tracks/STATE.md)
CODEX: NOT_RUN
