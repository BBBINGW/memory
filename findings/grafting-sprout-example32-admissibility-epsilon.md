# Iteration 51 — Grafting Example 3.2: fixed-target sprout-choice uniqueness and incorrect stated epsilon

Date: 2026-10-10
Research branch: Grafting, Cheon et al. IACR ePrint 2024/1014 (CCS 2025).
PRIMARY STATUS: FAIL — for a single fixed realistic scaling target and the **paper's explicitly curated 61 sprouts**, two sufficiently scale-admissible choices do NOT exist; cannot use a hardware-cost-based selector to improve this target.
SECONDARY SOURCE-LEVEL FINDING: The paper's Example 3.2 claims epsilon < 2^-13, but its own exact parameters violate the hypothesis of Theorem 3.4 at gamma=45. Correct required epsilon for the stated 61 options, AND even all 64 divisors, is epsilon >= 2^-12 - 2^-30. This is a small quantitative / constant-bound issue, NOT a failure of the theorem or a CKKS correctness attack.
NOVELTY/IMPORTANCE: likely low (correctable numeric parameter mismatch). No new FHE construction or speedup claimed.

## Protocol, parent branch, and source evidence
[FACT] Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and I50 `failures/grafting-sprout-ks-gadget-monotonicity.md` before starting. STATE.md tracks separately parked RIG-HE; do not alter.
[PRIMARY ORIGINAL] Cheon et al., *Grafting: Decoupled Scale Factors and Modulus in RNS-CKKS*, complete 20-physical-page ePrint 2024/1014 mirror, SHA256 `f50de6671019f6f71c69f24f7686f21a21ab1cb5dd70bb2f66cb12a96da1ce4c`, VERSION_UNVERIFIED. §3.2 Theorem 3.4 physical p.8, Example 3.2 and Algorithm 3 physical p.9, Algorithm 4 physical p.10.
[INDEPENDENT OFFICIAL-PRINT VISUAL CROSS-CHECK] CCS 2025 15-page postprint PDF https://orbilu.uni.lu/bitstream/10993/68347/1/3719027.3765083.pdf , visual PDF physical p.8–9 (0-based page 7/8), Theorem3.4 and Example3.2. Both contain exactly the assertion "epsilon < 2^-13" for the example, r1=2^16+1, r2=2^30-2^18+1, selected 61 sprout divisors. Theorem itself conditions for every integer gamma in [1,omega] on existence of a divisor r that is within relative epsilon of 2^gamma and derives relative rescale precision n*eta+2*epsilon+O(eta²+epsilon²). No alleged flaw in the theorem.
[ORIGINAL ARCHITECTURE] Algorithm 3 selects sprout by proximity of log2(r) to target (residual word) bit length; Algorithm 4 key switching uses normalized Q_inter and active gadget blocks. I50 already showed smaller sprout need not reduce gadget count or sprout arithmetic NTT channels. The present iteration strictly addresses *whether two output moduli are simultaneously admissible at ONE fixed target*.

## Primary hypothesis and decisive falsifier
[HYPOTHESIS — FALSIFIED for this target/curated set] Under Theorem3.4-like small relative scale-mismatch tolerance, the paper's curated Example3.2 61-sprout output modulus family admits two different outputs for ONE fixed target, enabling a choice based on lower gadget count / conversion-NTT cost.
[FALSIFICATION CONDITION] Enumerate all reachable Q'=prod(q0..q_(ell-1))*r with ell in [0,5], r from exact 61 selected divisors, and show only one meets an explicit even-generous relative tolerance around Q_target.
[ONE MINIMAL TEST] Fixed N=32768 and one target Q_target; exact integer / rational calculations, not broad parameter tuning and no FHE runtime.

## Exact paper 61-sprout set
[FACT/DERIVATION] Let r1=65537, r2=1073479681, r_top=2^15*r1*r2=2305315237189943296. Example 3.2 explicitly selects the following 61 among all 64 positive divisors:
  S = {2^a:1<=a<=15}
    union {2^a*r1:0<=a<=13}
    union {2^a*r2:0<=a<=15}
    union {2^a*r1*r2:0<=a<=15}.
They are pairwise distinct, sorted, all divide r_top. The near-duplicate 2^14*r1 is NOT among the 61 (although it is a divisor); footnote9 says near-duplicate moduli deliberately omitted.
The smallest ratio of consecutive selected sprout values is (r2)/(2^13*r1)=1073479681/536879104 ≈1.99948121095. Thus **within one fixed ell** no two selected sprouts can both be within relative <0.1% of one target. The actual test ALSO includes all changes of ell.

## Single fixed high-dimensional admissibility test
[EXPERIMENT] N=2^15, choose five pairwise distinct 61-bit NTT primes q_i ≡1 mod 2N, all individually primality-checked:
  q0=2305843009211662337,
  q1=2305843009211596801,
  q2=2305843009211400193,
  q3=2305843009210023937,
  q4=2305843009208713217.
These lie extremely close to 2^61, so eta=max_i |q_i/2^61−1|≈2.16004948303e−12, satisfying Theorem3.4's near-word-size hypothesis.
  Q_in=r_top*prod_(i=0..4) q_i.
  Q_target=(q0 q1 q2)*r2 (output is a divisor of Q_in).
  Desired rescaling Δ=Q_in/Q_target=q3*q4*2^15*r1, 154-bit integer, n=ceil(log2Δ/61)=3.
Enumerate every Q'=prod_(i<ell)q_i*r with ell in [0,5], r in S, requiring Q'|Q_in (all 366 states satisfy divisibility).
Use an EXPLICIT even generous tolerance tau=2*epsilon_actual+3*eta+10*(epsilon_actual²+eta²)≈0.0004888754 (0.0489%); epsilon_actual determined independently below. This numerical tau is a **user-defined test cutoff** motivated by Theorem3.4's leading nη+2ε term plus surplus margin, not a literal numeric claim made by the paper. Even if tau is relaxed to 0.1%, uniqueness persists.
  Eligible output count: exactly ONE, ell=3, r=r2.
  Next nearest distinct output in the 61 set: ell=3, r=2^13*r1, relative error≈0.4998702691 (49.987%).
  Active gadget count for winner at alpha=2: d=ceil((ell+1)/2)=2; no other eligible candidate has different d to compare.
[IMPORTANT SCOPE] The paper says "for all possible sprouts" divisors of r_top, but its *recommended 61* differs from all 64. In the all-64 set the omitted r=2^14*r1 gives relative gap≈0.00025946 from r2, which falls within our generous tau. We therefore DO NOT claim uniqueness for every mathematically possible sprout—only the **explicitly selected 61** used by this one test. Even the omitted contender may not improve cost and was excluded by the authors.
[NO IMPLEMENTATION] Counts are exact modulus candidates and gadget counts, NOT measured runtime, KS error, CKKS scale/precision, or a proven optimality theorem for any other target.

## Secondary exact quantitative mismatch in Example 3.2's epsilon
[FACT / SOURCE] Example3.2 explicitly claims the top sprout example meets Theorem3.4 with epsilon < 2^-13. This assertion appears in BOTH the 20pp ePrint text and the visually checked CCS 2025 PDF p.9.
[DERIVATION] For gamma=45, the closest sprout to 2^45 among ALL 64 divisors (and the curated61) is 2^15*r2. Its relative deviation from 2^45 is EXACTLY:
   epsilon_needed >= |(2^15*r2)/2^45−1|
     = |r2/2^30−1|
     = 2^-12 − 2^-30
     = 0.00024413969367742538.
This exceeds claimed upper threshold 2^-13=0.0001220703125 by approximately a factor 2. A second independent witness at gamma=61: r_top is the LARGEST divisor and |r_top/2^61−1|≈0.00022888463 > 2^-13.
[EXHAUSTIVE CHECK] For every gamma=1..61, compute min_(r in S) |r/2^gamma−1|; maximum exactly 2^-12−2^-30 at gamma=45. Repeating over **all 64** divisors gives exactly the same maximum. So omitted near-duplicates do not repair the epsilon bound. A safe simple replacement is epsilon=2^-12 (which is larger than required actual value); Theorem3.4's 2ε term correspondingly becomes about twice as large as the text's claimed epsilon would suggest.
[CAUTION] This is a quantitative example-instantiation mismatch, NOT a counterexample to Theorem3.4 (the theorem has a conditional hypothesis) and NOT a decryption failure. It is too small/elementary to stand alone as a publishable cryptographic contribution without showing it affects a meaningful precision/security boundary.
[TEXT/FIGURE VERIFICATION] Both theorem assumption and numerical claim verified on CCS PDF screenshot pp.8–9, avoiding OCR/column/LaTeX extraction errors.

## Reproduction and audit
[EXPERIMENT] Exact Python script `/mnt/data/iteration51_grafting_sprout_admissibility_audit.py`, SHA256 `cc4cad697e2bb649ecb00d140a448fc745d6e9bff426545786d4de05ab3`; stdout `/mnt/data/iteration51_grafting_sprout_admissibility_results.txt`, SHA256 `db3c6a63d2b18d1a99abde576c6f5ae3b69ed493126c81ed0df86bf9f52c0e37`. Python uses exact Fraction arithmetic for all norm/gap/admissibility checks and optional sympy.isprime verification of chosen constants; floats ONLY to format results. Executed PASS. No key switching or encrypted CKKS experiment.

## Research judgment
[NEGATIVE PRIMARY] For the fixed target and curated 61-sprout implementation design, no nontrivial hardware-aware selection comparison is possible within tight relative error: only one admissible choice. Generic "choose another nearby cheaper sprout" is not a valid optimization at that target.
[POSITIVE MINOR AUDIT] Example3.2's epsilon <2^-13 does not actually satisfy Theorem3.4's all-gamma closeness assumption; epsilon ~2^-12 is appropriate. Easy numeric correction, little research value unless demonstrated precision consequence.
[PRIOR ART] Authors already deliberately curated 61/64 candidates and discussed sprout hardware representations Appendix A.2. No new Pareto point, technique, or meaningful implementation advantage found.
[STAGNATION] Iterations 49,50,51 provide negative or minor bookkeeping results, none novel/publishable. According to AGENT.md stagnation protocol, avoid further sprout micro-variants and request PI direction review rather than let this become endless toy testing.

## End of iteration
STATUS: FAIL (primary alternate-admissible-sprout hypothesis); MINOR FACTUAL FINDING (Example 3.2 epsilon mismatch); HUMAN_REVIEW for further Grafting pursuit.
RESULT: 366 reachable paper-selected output moduli, one eligible at fixed q-prefix target with 0.0489% tolerance (also unique with 0.1%). An independently source-verified numeric example condition epsilon<2^-13 is false; actual epsilon_min=2^-12−2^-30. No Grafting core theorem or security failure shown.
NEXT_ACTION: PI to decide ARCHIVE the Grafting sprout cost branch (recommended) and pivot to a distinct full-text FHE construction, or authorize exactly one specific error-bound impact test of the epsilon correction if application parameters make it relevant; avoid further arbitrary sprout sweeps.
STATE_UPDATE: NO — parked RIG-HE STATE.md unchanged.
