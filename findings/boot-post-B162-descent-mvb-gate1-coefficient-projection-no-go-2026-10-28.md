# BOOT — DESCENT_MVB_GATE_1: conditional no-go for coefficient truncation
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER-LEVEL ONLY
CODEX: NOT USED
NATIVE: NOT RUN

## Read-before-write / provenance
Prior BOOT state read from findings/boot-HANDOFF-post-B162-B163-pending-2026-10-28.md and previous findings/boot-post-B162-structural-scout-descent-mvm-2026-10-28.md.
Source cross-check: ePrint 2026/2616 (public abstract) says Descent-PBS uses subring-secret-compatible truncation plus merged-column functional key switching to descend module accumulator to ring. Its exact full-text D has NOT yet been verified in this round.
MVB source: Mono/Kluczniak/Güneysu, TCHES 2024, 'Improved Circuit Synthesis with Multi-Value Bootstrapping for FHEW-like Schemes', https://ches.iacr.org/2024/papers-issue-4/4_98.pdf (abstract and mathematical description of function-specific polynomial multiplications).
Do not equate simple coefficient projection below with the actual Descent-PBS FKS without source evidence.

## Abstract intertwining lemma (global version)
Let D:V -> W be linear and B:V -> V linear. An induced linear \tilde B on im(D) with D B = \tilde B D exists iff B(ker D) subset ker D.
Proof: necessity applies both sides to x in ker D; sufficiency defines \tilde B(Dx)=D(Bx), well-defined under the kernel condition.

Important logical limit: this characterizes commutation on ALL V. A construction only on reachable accumulator states A subset V may still exist without this global condition. On A the weaker condition is D(a)=D(a') => D(Ba)=D(Ba') for all a,a' in A.

## New conditional no-go theorem
Take a commutative coefficient ring K with 1!=0; R=K[X]/(X^N+1), 1<=M<N.
Define D_M:R -> K^M by retaining coefficients of X^0,...,X^(M-1).
Let B_b:R -> R be multiplication by public polynomial b=sum_{j=0}^{N-1} b_j X^j.
Then
  B_b(ker D_M) subset ker D_M
holds iff b is a constant polynomial (b_j=0 for all j>=1).

Proof:
Sufficiency of a constant b is immediate.
For necessity, for each j in {1,...,N-1}, choose i in {0,...,M-1} and k in {M,...,N-1} with j=N+i-k; such a pair exists because intervals [1,N-1] are covered by differences (for example i=max(0,j+M-N), k=N+i-j).
Then X^k lies in ker D_M, while the coefficient of X^i in b X^k mod (X^N+1) is exactly -b_j, as k>i and each monomial has a unique exponent mod N.
Thus kernel preservation forces b_j=0. QED.

Note: this proof is coefficientwise; it does not require K to be a field. Valid over Z/qZ, provided 1!=-1 confusion does not matter since -b_j=0 implies b_j=0.

## Decision
If the concrete Descent-PBS map, in the state basis relevant to MVB post-factor multiplication, is equivalent to such a plain coefficient projection, then the global post-descent factor class is only scalar polynomials. That kills the GENERIC whole-space polynomial-multiplication commutation scheme for nontrivial MVB readouts.

But the real 2026/2616 Descent includes module->ring functional key switching and secret/subring structure. We have NOT recovered its exact map or proven that it is the above D_M. Therefore:
  MODEL_CONDITIONAL_NO_GO: PASS
  ACTUAL_DESCENT_PBS_NO_GO: NOT_ESTABLISHED
  DESCENT_MVB_NARROW_CANDIDATE: UNCLEAR
  B163: PENDING_CODEX_QUOTA

## Next cheapest decisive paper gate
1. Obtain full text of ePrint 2026/2616 and identify its exact plaintext/module state transform D including truncation and FKS conventions.
2. Determine the actual reachable accumulator states A (rotations of shared, function-independent test polynomial), not only abstract whole-space V.
3. Check equivalence of function-specific readouts on A by comparing fibers: D(a)=D(a') => target readout(a)=target readout(a'). This weaker sufficient-statistic test may permit meaningful functions even when whole-space intertwining fails.
4. Check public post-descent extraction/output interface and noise amplification; do not assume arbitrary ring multiplication is cheap or output noise-safe.
5. Check MVB/TCHES 2024 and newer multi-readout papers for direct collision.

## Authoritative state (UNCHANGED)
TRACK_ID: BOOT
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN
