# BOOT / B158_OVERALL — Successor Research Turn 16/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-three-independent-galois-involution-selector-axes-v1
Status: PARKED — FAIL_THREE_AXIS_GALOIS_GROUP_SEMANTICS / NO_CREDIBLE_NEW_MECHANISM
No native / Codex execution.

## Authority, read-before-write and distinctness
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL; entering ACTIVE=UNKNOWN; backups none.
Read and independently verified:
- findings/boot-b158-successor-turn15-plaintext-scale-tagged-mask-numerator-value-ceiling-2026-11-12.md blob db0c2fd47cd334bb95cda93a5ae5482c29159395 (PARKED).
- findings/boot-B158-residual-structural-rescue-scout-2026-10-28.md blob d87795880d9df2f16c710f38fc7dfd94a0f4d771: B163 late masks add 20 and 26 required-logQ bits; current two-row layout cannot produce patterned selector from uniform x^k row with only row-preserving rotations/public linear combinations; scout explicitly floated a DIFFERENT multidimensional hypercube layout as high-risk.
- findings/boot-B175-post-claim-boundary-synthesis-2026-10-29.md blob 3b61d23d11e78e7f0bf111a905d3c6b99d918ccb: no valid B175 fixed-Q end-to-end result.
- findings/boot-B176-order8-crt-trace-linearization-2026-10-29.md blob f3313571adb32e0fa6628eb9843a0799eddccc66: public automorphisms/trace do not eliminate encrypted dynamic bilinear evaluation.
- Primary source Lattigo tag v6.2.0, schemes/bgv/encoder.go blob db146d55271b67f868a53fca94ebf7a6d3a01974, function permuteMatrix lines110–132: defines GaloisGen, iterates a single cyclic generator pow mod 2N and pairs it with sign-conjugate mirror position. Consistent with the standard C_(N/2) x C2 automorphism structure.
The candidate is NOT the closed public mask lift, metadata scaling, LWE tensor, degree2 extraction, or quadratic polarization. It proposes physically different slot-axis layout with THREE independent order-two Galois actions to realize three different binary selector dimensions without plaintext mask amplification at the original fixed ring. This exact requested primitive is not part of the previous two-row no-go (which assumes current layout); we audit the Galois-group existence before layout engineering. This is a limited distinct hypothesis, NOT a claim against all alternative layouts.

## Preregistered decision
QUESTION: Keeping the B158/B175 fixed cyclotomic ring R_Q=Z_Q[X]/(X^32768+1) and native Lattigo Galois automorphisms, can we choose THREE independent commuting order-two automorphisms g0,g1,g2 (g_i²=id; no nonempty product=id) as three hypercube selector-bit axes, each available as a standard rotation/key edge, and thereby eliminate the corresponding heavy selector masks without changing the ring/security or adding nonlinear products?
CURRENT_BELIEF: No. The cyclotomic automorphism group (Z/(2N)Z)^× at N=32768 is C2 x C16384, whose order-two subgroup has only four elements; three independent involutions would demand eight.
CHEAPEST_DECISIVE_TEST: Enumerate all odd residues g mod65536 satisfying g²≡1 mod65536 and prove maximal elementary 2-subgroup rank from structure of units of 2-powers. Compare to the exact proposed 3D hypercube action; no experiment.
IF_PASS: If eight independent order-two actions are actually supported in the same source ring, retain ACTIVE to construct explicit compatible slot permutation/selector recurrence, exact whole-output, typed keys and all-in cost.
IF_FAIL: If only four involutive automorphisms exist, PARK the exact 3-axis involution hypercube mechanism before native.
IF_UNCLEAR: If Lattigo uses other allowed automorphisms/slot operations, audit typed source to distinguish higher-order cyclic actions from involutions; do not infer three axes from arbitrary bit labels.
WHICH_PAPER_GATE_CHANGES: killer gate1 exact permutation/slot semantics and gate2 existence of source Galois keys, then system-value/noise and novelty.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A design requiring 3 independent source automorphisms of order2 cannot be implemented if the native ring has rank2 2-torsion; no amount of mask refactoring or benchmarking can fix the absent key edges.

## Exact mathematical source-interface gate
Fix N=32768=2^15, cyclotomic index m=2N=65536=2^16. Standard automorphisms of R_Q=Z_Q[X]/(X^N+1) come from odd exponents a mod m via sigma_a: X->X^a; these compose multiplicatively mod m. The unit group has structure
 G=(Z/2^16 Z)^× ~= C2 x C_(2^14)
so |G|=2^15=32768 but its 2-torsion subgroup G[2]={g:g²=id} has exactly 2²=4 elements.
Direct exhaustive enumeration over all odd representatives 1<=a<65536 gives
 a in {1,32767,32769,65535}
for a² ≡1 mod65536. (The identity is 1; three nonidentity involutions exist, but they are NOT independent: the product of two distinct nonidentity involutions is the third.)
To obtain three independent coordinate flips g0,g1,g2, the subgroup they generate must have 2^3=8 distinct elements. This contradicts |G[2]|=4. Therefore no three independent commuting order-two Galois automorphism axes exist in the SAME fixed cyclotomic ring.
For standard Lattigo batching, one nontrivial order-two operation is row-conjugation and the other is the half-turn of the cyclic rotation generator. A third distinct nontrivial order-two operation equals their product; it cannot flip a third independent binary coordinate. This is a group-theoretic source SEMANTICS impossibility, not a measured noise effect.
The exact criterion is stronger than counting visually labelled hypercube axes; assigning a logical bit axis to a power of a HIGHER-ORDER cyclic rotation does not satisfy the candidate's independently-involutive-axis contract. Noninvolutive operations may still support other layouts with carry/rotation/key costs; untouched.

## Full output and prior-art boundaries
Even if a hypothetical 3D involution group existed, whether fixed automorphisms eliminate DATA-DEPENDENT selection is a second, distinct issue: for arbitrary encrypted y, dynamic selection generally needs a nonlinear product, external product, CMux or function-specific key. Archived B176 order-8 CRT/trace proof already establishes that simple public fixed linear transformations cannot replace F(y) for all encrypted y and legal root=0. Hence source existence gate is the *first* fatal blocker for this candidate; do not spend time/cost on a hypothetical algebraically absent 3-axis implementation.
A modified cyclotomic ring with higher 2-rank is a genuinely different parameter/security/packing change and is not silently allowed by N=32768; nor is a multi-ciphertext state or non-Galois selector a drop-in replacement.
This does NOT prove all 3D logical layouts are impossible in power-of-two rings, nor forbid non-involutive Galois rotations, custom linear transforms, decomposition into multiple ciphertexts, or other cyclotomics. It establishes impossibility ONLY for three independent order-two Galois coordinate flips at the specified ring and source. Closest prior art: standard cyclotomic unit-group structure, common two-row batching/HElib-style hypercube slot notions, Lattigo permuteMatrix and prior B158 current-layout mask-free no-go. No independent research novelty or paper theorem claimed.

## Cost, noise and decision
An absent 3-axis Galois subgroup fails semantic/source feasibility before any optimistic value test: no stock keys can instantiate those missing automorphisms, no valid mask-free recurrence, no output/noise DFR or full security can be claimed. Even ideal zero-cost automorphisms are irrelevant if the intended exact axis permutation does not exist. This was a one-gate first-order killer; no native, benchmark or new source modifications.
Candidate PARKED; NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for the three independent involutions design.
Reopen condition: a distinct, exact supported slot action which implements needed B158 selector semantics (including root0 and full outputs) without three independent involutions, with a typed source construction, quantified noise/DFR, key/rotation/conversion cost, security and novelty, OR a specifically authorized changed cyclotomic/security setting with fully compared baseline. No mere renaming of three arbitrary Galois powers as independent involutions.
ELIMINATED_UNCERTAINTY: Existence of three independent Galois involutions at m=65536 for fixed B158 slot ring. Exactly four solutions to a²=1; rank2 only, hence impossible.
DECISION_CHANGED=true; research_frontier_exhausted=false; further independent BOOT problem selection still conceptually available.
