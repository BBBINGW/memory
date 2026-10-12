# Iteration 93 — Diagonal base-scalar exceptional-set shortcut cannot certify 128-bit with ONE ring sumcheck

Date: 2026-10-12. Active target: Cascudo et al., CRYPTO 2025, ePrint 2025/286, I88–92 bounded-public-A cross-CRT digit coherence.
STATUS: **FAIL** direct single-run scalar-challenge shortcut; **PASS** tight scalar cardinality theorem and explicit false-aggregate Πsum transcript; **HUMAN_REVIEW** whether to test amplification or archive this repair branch. Not a compiled original-vFHE SNARK forgery and NOT a universal impossibility theorem. No external contact/public disclosure. NOVELTY NOT VERIFIED.

## Read before write, source
Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, live STATE.md (I92 next I93), I92 finding. Read complete ePrint 2025/286 primary cached mirror physical pp7–11 via Research MCP: PDF SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; VERSION_UNVERIFIED vs latest official.
[FACT] §2.1 Definition2.1, p7, requires distinct exceptional-set elements have UNIT differences in R. §2.2 p9 Theorem2.6 for per-variable degree d and ell variables gives ideal Πsum soundness <=d*ell/|S|. §3.1 pp10–11 decomposes R_q into CRT finite fields F_(p_i^d); the largest *unrestricted* R-exceptional set has size min p_i^d (extension field degree d). §6 p27 uses 49-bit RNS primes; I92 source notes factor count and conditional cost. This finding concerns a STRICTER scalar-only subset, NOT all ring exceptional sets.

## ONE hypothesis and cheap falsifier
Can all sumcheck and mixing challenges be confined to a common base-scalar subring Z_q*1_R, enabling evaluation of public mask polynomials once (up to per-prime reduction) instead of across thousands of field factors, WITHOUT losing a one-run 128-bit Πsum guarantee?
Falsifier: prove max scalar exceptional-set cardinality <=p_min and exhibit an actual bad Πsum transcript with ~1/p_min chance to pass.

## Tight scalar-exceptional-set bound [DERIVED]
Let R=Z_q[X]/(X^N+1), q=prod_i p_i distinct primes, pmin=min p_i. Let S be any exceptional subset of the scalar subring {a*1_R:a∈Z_q}. The map S -> F_(pmin), a*1_R ↦ a mod pmin, MUST be injective: if distinct a,b give the same residue, a-b is zero in every CRT field factor over pmin, so a-b is NOT a unit, contradicting Definition2.1. Thus |S|<=pmin. Equality is achieved by S={0,1,...,pmin-1}*1_R because for any a≠b in that set, 0<|a-b|<pmin≤p_i, so difference is nonzero in every p_i and is a unit in R.
This remains true even if different CRT primes are allowed independent base-subfield scalar residues, as long as ALL components of a given p_i lie in F_(p_i), because projection into the smallest PRIME subfield is injective on exceptional S. It does NOT exclude shared-coefficient degree<d extension-field challenges, which have potentially pmin^d values but require different projections/arithmetic; that is outside this one test.

## Actual single-run soundness limitation
At Medium M<=2^19, virtual aggregate sumcheck has ell=19 and individual degree<=2, so Theorem2.6 guarantees <=38/|S|. Even at maximal scalar |S|=pmin and 49-bit pmin∈[2^48,2^49), theorem exponent log2(pmin/38) lies in [42.752,43.752), far below 128. This is an INSUFFICIENT THEOREM GUARANTEE, not alone an attack.
Stronger EXPLICIT cheating transcript: original committed h~(X)=0 (honest valid digits, hence virtual g=alpha~ h~=0), prover announces false bounded integer aggregate A=1 (assuming beta>=2, m>=1). On ONE-variable native sumcheck for false public y=1, prover sends degree1 polynomial g1(Z)=Z. Its endpoint sum g1(0)+g1(1)=1 passes. Verifier samples r∈S; its TRUE terminal virtual oracle g(r)=0. Claimed g1(r)=r equals 0 exactly when r=0, which occurs with probability 1/|S| for maximal scalar S. For ell>=2, after the first challenge r1=0, prover sends ZERO polynomials for all remaining rounds, and every terminal check succeeds; event prob 1/|S|. This is a genuine PIOP-level error for the *new false aggregate claim*, not a forgery of the original CKKS range relation or full compiled original SNARK. An analogous 1/|S| false-claim event arises in batched random mixing when one E_i !=0 and its coefficient rho_i=0, if 0∈S.
Thus a single restricted-scalar sumcheck/mixing implementation has explicit incorrect-aggregate pass probability >=1/pmin >2^-49 in these examples and cannot certify 128-bit as a one-run replacement.

## Exact reproducible toy
R=Z_(29*37)[X]/(X^8+1), q=1073, S=0..28. All distinct scalar pairs in S have gcd(a-b,1073)=1; the pair 0 and29 has gcd(29,1073)=29, so cannot coexist in exceptional S. Exhaustively checked each of 29 residue fibers modulo29: any two elements sharing a fiber are incompatible as scalar challenges.
For ell=2 with g=0, false y=1, send g1(Z)=Z and if first r1=0 send g2(Z)=0. Over 29^2=841 challenge pairs, exactly29 accepted, probability29/841=1/29. No PCS simulation.
Executed /mnt/data/iteration93_vfhe_scalar_exceptional_set_no_go.py SHA256 4e705989ceb39edb3bca1448afd9d040033167396f7a043de5b348d2eae8a1e8.
JSON /mnt/data/iteration93_vfhe_scalar_exceptional_set_no_go_results.json SHA256 890bf06b55793decc180358dfa2c76a0a4d106050ad21164025e9ec4af3224c8.

## Scope, cost consequence, strategic review
Positive: common scalar evaluation of alpha~(r) may be shared symbolically or as an integer then projected into different p_i; field residues need not be numerically identical. Negative: single-run challenge entropy collapses from possible pmin^4 (>2^192) to at most pmin (<2^49) for d4, losing the original one-run high-soundness guarantee and admitting ~1/pmin cheating probability.
NOT ruled out: independently repeated restricted-scalar sumchecks (at cost of more distinct h evaluation proofs), different high-entropy exceptional challenge encodings, degree<d common-coefficient challenges, revised PCS compression or exploiting special aggregate structure. Repetition count and costs must be separately audited; NOT a proof every scalar-based protocol insecure.
Previous I92 shows 1 ring opening can be a huge μ-field Brakedown evaluation phase in source's ordinary uncompressed encoding, though those concrete estimates depend on author packing; no confirmed full proof-size benchmark. I91 masked aggregates may be batched with random rho but cannot assume scalar restriction preserves 128bit.

## End of iteration 93
STATUS: **FAIL** direct common base-scalar one-run shortcut; **HUMAN_REVIEW** strategic continuation.
RESULT: |S_scalar|<=pmin tight and one false sumcheck claim is accepted with exactly 1/pmin for maximal scalar S, while source guarantee for ell19,d2 is only 42.75–43.75 soundness bits with 49-bit primes. High-entropy native challenges or soundness amplification are necessary for this path.
NEXT_ACTION: PI decides between (A) ONE narrowly scoped I94 cost/soundness test of FOUR independent scalar-challenge repetitions (including four same-h Brakedown evaluation phases and per-component PCS error budget), or (B) archive public-A repair as currently impractical and pivot to a different FHE hole. Do not autonomously select, broaden or contact authors.
STATE_UPDATE: YES — proved an additional tight negative protocol boundary and reached strategic human review.
