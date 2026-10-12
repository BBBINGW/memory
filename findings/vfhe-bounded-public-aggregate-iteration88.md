# Iteration 88 — Bounded public aggregate

Conditional result: For native scalar digits in [0,beta-1] committed before sampling a binary mask, let T=m(beta-1)<pmin. A public integer A in [0,T] which equals the masked sum modulo every CRT prime must equal each masked sum over the integers. Thus the same A provides a common comparison without an extra external integer-vector commitment, provided every modular sum is authenticated against the original committed witness.

With two different fixed digit vectors, an independently sampled binary mask reveals different sums with probability at least 1/2. This does not establish a complete protocol. If T>=pmin, the claim need not hold: for p=29,37, m=16, beta=4 and all-one mask, legal sums 29 and 0 both match A=0 in their respective fields. This extra bound is not implied by the source's separate beta<pmin and m<pmin conditions.

Source: Cascudo et al., ePrint 2025/286 §4.3 pp20-24, §5 p25 and Appendix D.3 pp43-44, cached mirror version unverified. Earlier related evidence: I78, I87.

Test: /mnt/data/iteration88_vfhe_bounded_public_A.py and JSON result, exact exhaustive m=3 p29/p41 PASS. No PCS compiled or privacy argument.

STATUS: PASS conditional arithmetic; UNCLEAR complete proof.
NEXT_ACTION: I89 check whether the original ring sumcheck can authenticate the masked sum against the SAME pre-challenge committed digit oracle.
STATE_UPDATE: YES if repository write succeeds.
