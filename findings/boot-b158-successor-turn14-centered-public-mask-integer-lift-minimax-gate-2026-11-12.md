# BOOT / B158_OVERALL — Successor Research Turn 14/25
Date: 2026-11-12 Asia/Singapore
Candidate: boot-b158-same-mask-alternate-integer-lift-minimax-v1
Phase: PROBLEM_SELECTION
Final decision: PARKED / FAIL_INTEGER_LIFT_MINIMAX / NO_CREDIBLE_NEW_MECHANISM
No native/Codex test.

## Durable read-before-write provenance
Entering controller CURRENT ACTIVE=UNKNOWN; no backups. Track BOOT, active subline B158_OVERALL.
Fetched and verified:
- predecessor findings/boot-b158-successor-turn13-preproduct-lwe-tensor-switch-value-gate-2026-11-12.md, blob 0b8fb244d8f9beac85b98dc09f27484ea3aad1e9 (PARKED);
- findings/boot-B158-residual-structural-rescue-scout-2026-10-28.md blob d87795880d9df2f16c710f38fc7dfd94a0f4d771: B163 late selector public mask additions +20 and +26 required-logQ before fused ct×ct, 571->591 and 620->646;
- findings/boot-B175-public-mask-convolution-screen-2026-10-29.md blob 98cf77cd70f589812f48fe904e0d4f8c2c86eb09: reconstructed masks, M0..M3 centered l1=79086, c2/d2 centered l1=214538, 17-18 bit empirical multiplication growth on healthy operands;
- findings/boot-B175-public-mask-operator-kernel-screen-2026-10-29.md blob 36798b49f9cbfacf05e303943d559e166aef774b: R_T projections do not remain projections under L18 Q coefficient lift, all raw mask operators invertible at 19 Q primes, actual residual includes reference carry and Q wrap;
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md blob c75aa60e080b28b688de7ee8859c5df4d1951c02: last SI E_tref is dominant, quantified E_quant and E_relin are subdominant.
This candidate is not an attempt to reopen B175 frontier A/B, failed affine terminal recentering, prior LWE tensor, or quadratic polarization. It tests a distinct *public coefficient representative* minimax mechanism at the earlier B158 mask step, specifically whether changing public integer lifts while preserving EXACT R_T mask values can lower universal coefficient-error amplification without added depth.

## Registered single cheapest test and divergent decisions
QUESTION: For any fixed public selector M ∈ R_T, can another integer polynomial A≡M(mod T) have strictly smaller worst-case coefficient-infinity operator gain under negacyclic integer multiplication than the canonical centered coefficientwise lift A*, and therefore establish a source-independent reduction in B158 late selector-noise worst-case bound without changing plaintext functionality?
CURRENT_BELIEF: No. Each centered coefficient minimizes absolute value individually and the operator norm of signed negacyclic convolution from l_inf^N to l_inf^N is exactly l1 of its kernel.
CHEAPEST_DECISIVE_TEST: Prove exact l_inf-to-l_inf norm for negacyclic integer multiplication and coordinatewise minimization across all integer lifts. Compare against previously verified centered masks. No source compilation/native or parameter sweep.
IF_PASS: An explicit legal A with smaller norm than A* would admit ACTIVE and justify exact Q/T scaling and carry source audit, correctness canary, DFR and full value analysis.
IF_FAIL: Equality/minimax of A* implies no other same-R_T integer coefficient lift reduces the universal no-wrap/no-carry convolution bound; PARK this public-lift-only paper claim.
IF_UNCLEAR: If the complete RNS ciphertext-plaintext encoding and mod-Q carry can behave differently, keep that practical effect UNKNOWN; do not claim universal failure of all mask representations, and do not launch native without a distinct source-backed mechanism.
WHICH_PAPER_GATE_CHANGES: Gate1 plaintext selector semantic equivalence, Gate2 coefficient-representation feasibility, Gate3 dominant mask-noise/worst-case/value frontier.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: This precisely tests whether mere re-encoding of current public masks can be the missing 16-26-bit stage-noise mechanism. If canonical lift is already minimax, searching arbitrary integer lifts for a worst-case universal gain has no research value; useful alternatives must change the encoding algorithm, layout, carry geometry or statistical regime and pay all costs.

## Exact theorem and proof (with scope)
Let R_Z=Z[X]/(X^N+1), T=65537, N=32768. For a public plaintext M∈R_T fix any coefficient residues m_j∈Z_T. Its integer lifts A=Σ a_j X^j∈R_Z satisfy a_j≡m_j(mod T). Let a*_j be the unique centered residue in [-(T-1)/2,(T-1)/2]=[-32768,32768] (T odd). Thus for every integer lift and every j, |a_j|≥|a*_j|; hence ||A||_1≥||A*||_1.
For integer error polynomials e=Σ e_i X^i and *negacyclic convolution* C_A(e)=A*e∈R_Z, each coefficient is a signed permutation of the coefficients of A dot the e vector. Consequently ||C_A(e)||∞≤||A||_1||e||∞. Choose the sign of e_i to match (or oppose) the signed coefficients of one selected output row: e_i∈{−1,+1}, so ||e||∞=1 and one output coefficient has absolute value Σ_j |a_j|. Thus the induced REAL/INTEGER l_inf→l_inf operator norm is EXACTLY ||A||_1, including in the negacyclic ring:
 ||C_A||_{∞→∞}=||A||_1≥||A*||_1=||C_A*||_{∞→∞}.
This is a precise minimax statement for arbitrary bounded integer coefficient errors, not a claim that *every specific error vector* is maximally amplified and not a lower bound for each error vector.
For the existing B175 public masks of the same T,N, the previously verified centered l1 values imply best-possible universal norm at least 79086 (Mi) and 214538 (c2/d2), with log2 values approximately 16.27 and 17.71, respectively. These are worst-case OPERATOR norm/upper-envelope amplification factors, not observed noise growth lower bounds, not an exact equality for B158 late M_k without reconstructing those masks, and not measured DFR.
An alternative integer representative cannot universally improve these induced norms under the SAME coefficientwise mod-T constraint. This is enough to defeat the candidate's specific universal integer-lift minimax thesis.

## Source/carry correctness boundary (important)
Lattigo BGV plaintext vector encoding is NOT just naive multiplication by A* over integers: earlier verified source Lattigo v6.2.0 uses RingT slot permutations/INTT, scale T^-1 in the RNS Q lift and compensating T factor in ciphertext-plaintext multiplication. Prior B175 mask operator audit establishes R_T idempotent projection ≠ raw R_Q projection, all six lifted masks are invertible at every L18 q_j, and complete error is e_mask=rho_Q(A_Q*e+C_A(m)).
Therefore our minimax theorem alone does NOT establish that the canonical integer lift minimizes actual encoded L18 RNS error or expected/statistical DFR. Different Q representatives can produce different carry terms and distributions. For practical variants the necessary first evidence is a typed Q/T encoded-mask construction, exact correct plaintext semantics for arbitrary messages, and a proven carry-aware error/DFR reduction that is not just an integer representative. These are absent.
Also universal worst-case bound minimization is NOT the same as typical error optimization: a different representative might perform better on a particular known correlated error e while doing worse on some other e. Without a complete legal-family error distribution and security-compatible sampling, do not generalize the theorem.

## Paper-value and novelty gate
Relative to baseline the proposal makes no change to ct-ct count, depth, key sets or B158 recurrence. But its ONLY claimed gain is smaller universal coefficient-lift convolution amplification, contradicted exactly. No source-backed improvement at fixed Q, no corrected full Algorithm5 B175 output, no DFR, and no new algorithm. The elementary minimax theorem is too standard to be a standalone theory publication. Its value is a bounded exclusion of one search dimension, not novelty CLEAR.
Status PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM. Closest prior art elementary convolution-operator induced norms and conventional centered lifting, plus existing B158 noise scout and B175 public-mask operator audit. Security/DFR complete candidate not established.
Reopen only with a source-authenticated **non-integer-lift-only** representation: e.g. a genuinely new carry-aware Q encoding or state layout, exact public selector on all legal B158 inputs, a proven reduction in actual E_tref or a DFR bound with positive system-wide value (all conversions, rotations, memory, keys and offline), and independent novelty. Do not simply rename another lift or claim uniform noise reduction from one saved residual array.
ELIMINATED_UNCERTAINTY: Can a different *integer coefficientwise lift* of the same public R_T mask decrease the worst-case no-wrap/no-carry l_inf convolution amplification? No, centered lift is exactly optimal over the entire lift class.
DECISION_CHANGED=true: candidate PARKED without native. research_frontier_exhausted=false; no justified assertion that all BOOT/B158_OVERALL candidates are exhausted.
