# BOOT — Stabilizer-aware temporary subfield secrets for packed bootstrapping

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Source basis

### Ma–Huang–Wang–Wang, ASIACRYPT 2025 / ePrint 2025/1594

Supplied source:
papers/supplied/2025-1594.pdf
Git blob SHA:
049872913a58b55d7833688e66756b01371745a3

"Practical Dense-Key Bootstrapping with Subring Secret Encapsulation"

Verified source facts:
- temporary dense key is placed in a smaller subring before bootstrapping;
- smaller dimension/Hamming weight reduces CKKS EvalMod range and BGV/BFV digit-removal range;
- automorphisms that agree on the subring key can share/hoist a key switch;
- in BGV/BFV the paper explicitly characterizes ker(f), including cases where rotation automorphisms, Frobenius automorphisms, or both fix the subring;
- non-power-of-two cyclotomics are explicitly mentioned as also benefiting, by analyzing automorphism orders in the subring;
- concrete implementation chooses a standard subring dimension N' rather than treating the orientation of a same-degree fixed field as an optimization variable.

### Peikert–Pepin, ePrint 2025/1760

Supplied source:
papers/supplied/2025-1760.pdf
Git blob SHA:
b8f280f2b200b018c1d3a995a0f7010dfe03cecc

"Vive Galois! Part 1: Optimal SIMD Packing and Packed Bootstrapping for FHE"

Research-MCP mirror PDF SHA256:
8ba86be8499106ec5ff5aedbd4921835c89e8c90379525f3e70de0aa0ffac858
VERSION_UNVERIFIED.

Verified source facts:
- packed bootstrapping over broad abelian/cyclotomic subfields;
- intermediate fields correspond to fixed fields L^H of Galois subgroups H;
- CRT transforms factor along towers and are homomorphically evaluated as sparse linear combinations of automorphisms;
- Remark 5.12 gives direct-product tensor factorizations where independent Galois factors act independently along separate slot dimensions;
- Appendix B gives concrete multidimensional packed-FHE field constructions;
- implementation/optimization of these theoretical constructions is left as future work.

### Dangerous adjacent prior art checked

- GHPS field switching / ring switching: old mechanism for switching to smaller-field keys; does not by itself optimize the temporary key stabilizer against a transform support.
- Carousel, ePrint 2024/2032: uses automorphism groups and decomposition/subrings for blind rotation, but targeted source search did not expose the present temporary-key stabilizer/coset-hoisting optimization.
- 1594 itself already exploits automorphisms fixing a standard subring key. Therefore novelty cannot be "a stabilizer lets us hoist automorphism key switches."

Targeted public searches for combinations of fixed-field/subfield key + transform-support/stabilizer-aware key-switch hoisting did not locate a direct construction. This is not a novelty proof.

## General coset-hoisting lemma

Let L/F be a finite Galois extension with group

    G = Gal(L/F).

Let the temporary bootstrap key s belong to the fixed field

    K = L^H

for a subgroup H <= G. Thus

    h(s) = s   for every h in H.

Consider a homomorphic linear transform whose plaintext action is

    T(x) = sum_{g in S} a_g * g(x),

for public coefficients a_g and automorphism support S subseteq G.

Applying g to a ciphertext under s produces a ciphertext under source key g(s).

If g1 and g2 belong to the same right coset of H, write

    g2 = g1 h

for h in H. Then

    g2(s) = g1(h(s)) = g1(s).

Hence all automorphism terms from one coset C=gH decrypt under the same source key g(s).

Therefore we may first form

    u_C = sum_{tau in S intersect C} a_tau * tau(c)

and key-switch u_C only once.

### Consequence

Let pi_H : G -> G/H be the quotient map.

The number of distinct source-key classes needed by the stage is at most

    |pi_H(S)|.

If the identity coset H appears, terms in that coset already decrypt under s and require no key switch.

Thus the number of nontrivial source-key key-switch classes is at most

    |pi_H(S)| - 1

when S contains the identity.

This generalizes the "rotation offsets congruent modulo the subring period share a key switch" phenomenon in 1594.

## Subgroup-support corollary

If the support S=T is itself a subgroup of G, then

    |pi_H(T)| = [T : T intersect H].

Therefore, when identity is included, the exact number of nontrivial source-key classes is

    [T : T intersect H] - 1

provided the key stabilizer is exactly H and the stage genuinely uses representatives from all quotient classes.

This gives an explicit design objective:

    maximize |T intersect H|

for stages whose automorphism support is T.

For multiple stages S_j, a first-order key-switch objective is

    C_KS(H) = sum_j w_j * ( |pi_H(S_j)| - 1 ),

with stage weights w_j reflecting modulus level, gadget cost, and frequency of use.

## Same-degree orientation gap

The temporary key degree is determined by |H|:

    [L^H : F] = |G| / |H|.

Therefore two stabilizers of equal size give temporary-key fields of equal algebraic degree, but can have very different intersections with a transform support.

### Toy group

Let

    G = C2 x C2 = <a> x <b>,
    T = <a>.

Choose

    H1=<a>,
    H2=<b>.

Then |H1|=|H2|=2, so the two fixed fields have the same degree.

But

    [T:T intersect H1]-1 = 0,

while

    [T:T intersect H2]-1 = 1.

Thus equal key dimension does not determine linear-transform key-switch cost.

### General vector-space gap

Let

    G = (C_p)^r

and identify subgroups with F_p-subspaces.

If dim(T)=t and dim(H)=h, then

    [T:T intersect H]
      = p^{t-dim(T intersect H)}.

At fixed h, rotating H from maximal alignment with T to transverse orientation changes the number of source-key classes exponentially in the change of intersection dimension.

So "choose only the temporary key dimension" can leave an exponential group-theoretic factor on the table in multidimensional abelian settings.

## Concrete source-faithful example from 1760 Appendix B.2

1760 constructs

    L =
      C_3^(1) C_5^(1) C_7^(3) C_11^(5)
      C_13^(3) C_17^(1) C_19^(9) C_31^(5)

with

    [L:Q] = 24576

and 3072 F_{2^8} slots.

Let

    J = C_17^(1).

Appendix B.2 states:
- for K in {C_3^(1), C_5^(1), C_7^(3), C_11^(5), C_13^(3), C_19^(9), C_31^(5)},
  the extensions JK/J have pairwise independent tensor factors;
- their automorphisms act independently along the corresponding slot-tensor dimensions.

Two of those factors have equal degree four:

    [C_5^(1):Q]  = 4,
    [C_13^(3):Q] = 4.

Hence the corresponding independent Galois directions in Gal(L/J) each have order four.

Let T be the order-four subgroup acting along the C_5^(1) tensor dimension.

Compare two temporary-key stabilizers:

    H5  = T,

and

    H13 = the independent order-four subgroup acting along C_13^(3).

Both have order four. Therefore both fixed fields inside L have the same degree

    24576 / 4 = 6144.

The ambient plaintext field L is unchanged, so the source construction's F_{2^8} slot type and total slot count remain properties of the plaintext ring rather than of the temporary-key orientation.

For a transform stage supported on T:

Aligned choice H5:
    T intersect H5 = T,
    [T:T intersect H5]-1 = 0.

So all automorphisms in this stage fix the temporary key and require no nontrivial source-key key switching.

Misaligned same-degree choice H13:
    T intersect H13 = {1}
because the tensor factors are independent, so

    [T:T intersect H13]-1 = 4-1 = 3.

Thus, in a field family explicitly constructed by 1760:

    SAME TEMPORARY KEY DEGREE: 6144
    SAME AMBIENT PLAINTEXT FIELD/SLOT LAYOUT
    SAME TRANSFORM SUPPORT SIZE: 4
    DIFFERENT KEY ORIENTATION:
        0 versus 3 nontrivial source-key KS classes for that factor stage.

This is a source-faithful witness that subfield orientation is a real optimization variable, not merely an abstract C2 x C2 example.

It is not yet an end-to-end bootstrap speedup: the full transform uses several factors and other costs may move in the opposite direction.

## Negative theorem for standard power-of-two CKKS

The candidate should NOT be marketed as an improvement to ordinary power-of-two CKKS.

In the standard CKKS power-of-two cyclotomic setting, the relevant CtS/StC rotation automorphisms lie in the cyclic rotation subgroup

    T = <5>.

At fixed stabilizer size |H| <= |T|,

    |T intersect H| <= |H|,

hence

    [T:T intersect H] >= |T|/|H|,

with equality exactly when H is contained in T.

Because T is cyclic, it has a unique subgroup of each order.

The standard smaller power-of-two subring used by 1594 corresponds to precisely such an aligned subgroup of rotations. Therefore, for a rotation-only full-support stage and fixed temporary-key degree:

    STANDARD_POWER_OF_TWO_SUBRING_IS_KS_OPTIMAL

inside the stabilizer/coset-hoisting model.

Choosing a same-size subgroup with a conjugation component can only decrease T intersect H and weakly increase the number of source-key classes.

This closes the obvious CKKS generalization and prevents a false-positive contribution claim.

## Critical SECRET_NORM / GEOMETRY gate

The source-faithful orientation witness above proves only a linear-transform KS difference.

1594 obtains its nonlinear benefit because a dense key in a standard subring has fewer ambient coefficients / smaller effective Hamming weight, reducing the homomorphic-decryption or rounding range.

For a general fixed field L^H, equal algebraic degree does NOT automatically imply equal:
- coefficient support in the ambient basis;
- canonical norm;
- decryption-coordinate bound;
- gadget-decomposition norm;
- basis condition number;
- or bootstrap failure probability.

1760 supplies short structured bases and explicit canonical-norm bounds, but those bounds depend on the chosen subfield/tower.

Therefore a positive construction must pass:

    SECRET_NORM_GATE.

For every candidate H:
1. specify the fixed field K=L^H;
2. specify an integral/dual basis and key distribution in O_K;
3. embed the key into O_L exactly as the bootstrap decryption circuit sees it;
4. bound the relevant decryption-coordinate / canonical norm;
5. derive the nonlinear Decode/digit-removal range;
6. compare at the same security target and failure probability;
7. include any larger basis/gadget cost in the linear-stage savings.

PARK if the aligned stabilizer reduces KS but worsens key geometry enough to erase the gain.

## Security gate

A temporary key sampled from a fixed subfield is not an ordinary full-degree RLWE key in L.

1594's security argument is source-specific to its subring-key construction.

1760 establishes standard Ring-LWE hardness tools and bases for broad number fields, but this does not automatically prove that every embedded fixed-field key distribution used as an ambient key has the exact desired security property.

Required:
- formulate the encryption/key-switch distribution precisely;
- identify whether security reduces to RLWE over K=L^H, field switching, or a related-key assumption;
- estimate concrete security with the smaller degree and actual modulus;
- account for bootstrapping/evaluation keys under automorphic relatives of the temporary key.

No security claim beyond "same fixed-field degree" is made here.

## Prior-art boundary

Already known:
- field/ring switching;
- subring/decomposition-field FHE;
- subring-key encapsulation;
- automorphism fixing a temporary subring key enables key-switch-free/hoisted transforms;
- arbitrary abelian subfields and structured CRT transforms;
- designing slot tensor shape via Galois factorization.

Potential surviving novelty:

    choose the temporary bootstrap fixed field itself,
    among same/similar-degree candidate subfields,
    to optimize its stabilizer intersection with the actual automorphism supports
    of packed-bootstrap linear-transform stages,
    jointly with key geometry/security/slot constraints.

Call this:

    STABILIZER_AWARE_SUBFIELD_SECRET.

No direct source was found in the targeted prior-art search that formulates this joint optimization.

This is NOT a novelty proof.

## Cheapest decisive next gate

Do not implement yet.

STABILIZER_SUBFIELD_GATE_2:

1. Use 1760's Appendix B.2 field/tower.
2. Recover the exact automorphism support S_j of each homomorphic CRT-transform stage from Sections 4-6.
3. Enumerate candidate temporary-key subgroups H of one or more fixed orders.
4. Compute
       C_KS(H)=sum_j w_j(|pi_H(S_j)|-1)
   first with unit weights, then with level-aware key-switch weights.
5. For the best H candidates, compute 1760 short-basis norm bounds for K=L^H.
6. Compare against a dimension-matched but orientation-agnostic/default candidate.
7. Check slot structure and security.
8. PARK if the global transform savings vanish after summing all stages or if basis/security cost dominates.
9. Advance only if one H gives a strict end-to-end symbolic advantage at equal security degree/slot functionality.

No Codex is needed for this gate.

## Current status

COSET_HOISTING_LEMMA:
    PASS.

SUBGROUP_SUPPORT_FORMULA:
    PASS.

SAME_DEGREE_ORIENTATION_GAP:
    PASS.

SOURCE_FAITHFUL_1760_B2_ORIENTATION_WITNESS:
    PASS.

STANDARD_POWER_OF_TWO_CKKS_POSITIVE_EXTENSION:
    FAIL / ALREADY KS-OPTIMAL IN THIS MODEL.

MULTIDIMENSIONAL_ABELIAN_PACKED_BOOTSTRAP:
    PROMISING_NOT_ESTABLISHED.

SECRET_NORM_GATE:
    NOT_RUN.

SECURITY_GATE:
    NOT_RUN.

END_TO_END_VALUE:
    NOT_ESTABLISHED.

DIRECT_PRIOR_ART_COLLISION:
    NOT FOUND IN TARGETED SEARCH.

CCF_A_B_READINESS:
    NO.

CODEX_REQUIRED_NOW:
    NO.

## Paper-only BOOT priority

1. STABILIZER_AWARE_SUBFIELD_SECRET — active source/algebra gate, full primary sources available.
2. 2026/1779 partial-recovery interaction rank — strong theoretical candidate but blocked on missing full text.
3. 2026/2630 lossy-KS -> exact-error bootstrap — source-gated, lower priority.
4. RANK_PARTITION_LRMT — HOLD_NO_WORKLOAD.

B163 remains the highest native gate when Codex quota is explicitly restored by the PI.


## Global direct-product allocation gate — correction to the single-stage witness

The 0-versus-3 KS-class example above is only a **stage-local** witness. A complete CRT transform evaluates several tensor-factor stages. If two equal-size factors have symmetric stage costs, choosing a stabilizer aligned with one merely moves the free stage from one factor to the other, and the global KS total can remain unchanged.

Therefore the real optimization variable is a **stabilizer budget allocation across factors**, not merely "pick any aligned subfield."

### Direct-product model

Suppose the packed-bootstrap Galois group factors as

    G = T_1 x ... x T_m,

and the i-th structured-transform stage has automorphism support

    S_i subseteq T_i.

This is exactly the factor-wise picture supplied by 1760 Remark 5.12 / Appendix B, where independent Galois factors act independently on slot-tensor dimensions.

For a product stabilizer

    H = H_1 x ... x H_m,
    H_i <= T_i,

the i-th source-key class count is bounded by

    |pi_H(S_i)| - 1.

If the full factor T_i is used as support, this becomes

    [T_i:H_i] - 1.

If H_i=T_i, the entire i-th automorphism stage is key-switch-free.

The temporary fixed-field degree is controlled by the total stabilizer order:

    [L^H:Q] = [L:Q] / product_i |H_i|.

Thus a fixed security-dimension budget constrains the product of |H_i|, while the linear-transform objective is an additive weighted sum of quotient sizes.

This is a genuine allocation problem.

### Same-order global comparison inside 1760 Appendix B.2

The B.2 field has independent factor degrees

    2, 4, 2, 2, 4, 2, 6

over J for the seven external tensor dimensions.

Consider a stabilizer budget of order four, so every candidate temporary fixed field has degree

    24576 / 4 = 6144.

Two source-supported product choices are:

A. Concentrated order-four stabilizer:
    H_A = full C_5^(1) tensor-factor subgroup, |H_A|=4.

B. Split order-two-by-order-two stabilizer:
    H_B = (C_3^(1) factor subgroup) x (C_7^(3) factor subgroup),
    |H_B|=2*2=4.

Under the full-support cost model for those factor stages:

- H_A makes the degree-four stage key-switch-free, eliminating up to
      4-1 = 3
  nontrivial source-key classes.

- H_B makes two degree-two stages key-switch-free, eliminating up to
      (2-1)+(2-1) = 2
  classes.

So at identical fixed-field degree, the factor allocation can change the transform-side KS budget.

The strict arithmetic identity behind this effect is

    (ab-1) - [(a-1)+(b-1)]
      = (a-1)(b-1) > 0

for a,b>1.

Concentrating a multiplicative stabilizer-order budget into one larger transform factor can eliminate more class transitions than spreading the same order across smaller independent factors, when the corresponding stage weights are comparable.

### Important exact-support caveat

1760 Lemma 5.13 gives a **support upper bound**:
for the favorable direct-product case, nonzero automorphism coefficients are contained in the selected transversal subgroup T_i and there are at most |T_i| relevant automorphisms.

The source does not state that every element of each T_i necessarily has a nonzero coefficient for every concrete CRT-transform stage.

Therefore the "3 versus 2" comparison above is a source-faithful **full-support cost model**, not yet an exact operation count.

The next source-level task must recover the actual nonzero support S_i for the concrete B.2 bases/transforms before claiming an exact saving.

Nevertheless, if H_i contains the actual support subgroup, that stage is rigorously key-switch-free regardless of sparsity.

## First SECRET_GEOMETRY proxy from the same Appendix B.2 construction

The single-stage KS benefit is not free: different same-degree fixed fields can have different structured-basis geometry.

1760 B.2 bounds a short structured basis of the full field using the product

    1*1*3*5*3*8*9*5 = 16200

inside the square-root norm bound.

Using the same tensor-basis construction on a fixed subcomposite gives a first conservative geometry proxy.

### Choice H_A: remove the C_5^(1) degree-four factor

The C_5^(1) basis factor carries d=1 in the B.2 bound.

For the fixed field of degree 6144, the inherited bound is therefore approximately

    B_A <= sqrt(16200 * 6144)
        ~= 9976.61.

### Choice H_B: remove C_3^(1) and C_7^(3)

Their basis factors carry d=1 and d=3.

For the same fixed-field degree 6144,

    B_B <= sqrt((16200/3) * 6144)
        = 5760.

Thus the available source bound differs by

    B_A / B_B <= sqrt(3)
                ~= 1.732,

or about

    log2(sqrt(3)) ~= 0.7925 bits.

Interpretation:
- H_A has the better transform-side full-support KS count (up to one fewer class per transform direction in this comparison);
- H_B has the better available structured-basis norm upper bound by a factor sqrt(3).

This is precisely the kind of tradeoff the candidate is supposed to optimize jointly.

### Critical limitation of this proxy

Do **not** equate the above basis-norm bound with the actual EvalMod/digit-removal range.

1760's short-basis bounds concern canonical geometry of number-ring bases.
1594's nonlinear-range gain is derived in its own subring/coefficient representation and depends on the effective secret/noise behavior of that construction.

For a general fixed field, a full secret-distribution analysis is still required:
- choose how the temporary key is sampled in the fixed-field basis;
- derive its embedded canonical/coefficient covariance;
- derive the exact modulus-raising/decryption-error contribution used by the chosen bootstrap;
- then translate that into the nonlinear Decode/digit-removal parameter.

The sqrt(3) calculation is only a conservative **geometry warning/proxy**, not an end-to-end error theorem.

## Refined Gate-2 status

The candidate survives the global correction, but the bar is now clearer:

    STAGE_LOCAL_ORIENTATION_EFFECT = PASS.
    GLOBAL_EQUAL_WEIGHT_EFFECT = NOT AUTOMATIC.
    DIRECT_PRODUCT_BUDGET_ALLOCATION = PASS as a symbolic optimization model.
    B2_ORDER4_ALLOCATION_DIFFERENCE = PASS under full-support model.
    EXACT_B2_AUTOMORPHISM_SUPPORT = NOT YET RECOVERED.
    SECRET_GEOMETRY_PROXY = DIFFERENT BY sqrt(3) in one same-degree comparison.
    EXACT_BOOTSTRAP_ERROR/RANGE_EFFECT = UNKNOWN.

Next:
1. derive exact nonzero S_i for at least the B.2 degree-4 and degree-2 factor stages;
2. compute exact forward+inverse KS counts for H_A and H_B;
3. only then decide whether the transform saving survives before a full security/noise analysis.


## Source-incomplete gate and B.2 Pareto frontier

### Exact-support blocker

Part 1 (1760) proves only that the nonzero automorphism support of a structured transform stage is contained in a small set/subgroup derived from the transversal. Lemma 5.13 is a necessary-support statement, not an exact coefficient formula for the concrete short bases used in Appendix B.2.

The paper repeatedly refers the explicit short structured bases / associated fast transforms to:

    Vive Galois! Part 2: Short structured bases and fast transforms

listed in Part 1 as "in preparation."

As of 2026-10-28, targeted web search and Chris Peikert's current publication page did not surface a public Part 2 paper. The public page lists Part 1 (TCC 2025) but not Part 2.

Therefore:
    EXACT_B2_SUPPORT_S_i = SOURCE_INCOMPLETE.

Do not turn Lemma 5.13's |T_i| support upper bound into an exact operation count.

### What can still be optimized symbolically

For the seven external tensor factors of B.2, the factor degrees are

    2, 4, 2, 2, 4, 2, 6.

Under the full-support/unit-weight proxy, making a full factor subgroup part of H eliminates at most

    degree_i - 1

nontrivial source-key classes for that factor stage.

For a product stabilizer H made from whole independent factors:
- stabilizer order is the product of selected factor degrees;
- fixed-field degree is 24576/|H|;
- proxy KS saving is the sum of (degree_i-1).

The B.2 structured-basis norm bound contains the factor

    D = 1*1*3*5*3*8*9*5 = 16200.

For a fixed subcomposite obtained by removing selected independent factor fields, applying the same tensor-basis bound to the remaining factors gives the conservative proxy

    B_proxy(H)
      = sqrt( (16200 / product selected basis-d_i) * (24576/|H|) ).

Again: this is a basis-geometry proxy, not an exact secret-error bound.

### Fixed order |H|=4

All candidates have fixed-field degree 6144.

Representative Pareto points:

1. H = full C_13^(3) factor
   - proxy KS saving: 3
   - removed basis-d product: 3
   - B_proxy = 5760

2. H = C_11^(5) factor x C_19^(9) factor
   - proxy KS saving: 2
   - removed basis-d product: 5*9=45
   - B_proxy ~= 1487.23

The second has one fewer proxy KS saving but a roughly

    5760 / 1487.23 ~= 3.87

times better available structured-basis bound.

The alternative full C_5^(1) factor also gives proxy saving 3, but B_proxy ~= 9976.61, so it is dominated by C_13^(3) under this two-axis proxy.

### Fixed order |H|=8

All candidates have fixed-field degree 3072.

Two representative frontier points:

1. H = C_13^(3) x C_19^(9)
   - proxy KS saving: 4
   - removed basis-d product: 27
   - B_proxy ~= 1357.65

2. H = C_7^(3) x C_11^(5) x C_19^(9)
   - proxy KS saving: 3
   - removed basis-d product: 135
   - B_proxy ~= 607.16

Again, extra transform-side class elimination trades against a noticeably worse geometry bound.

### Fixed order |H|=16

All candidates have fixed-field degree 1536.

Representative frontier points:

1. H = C_5^(1) x C_13^(3)
   - proxy KS saving: 6
   - B_proxy = 2880

2. H = C_11^(5) x C_13^(3) x C_19^(9)
   - proxy KS saving: 5
   - B_proxy ~= 429.33

The geometry gap becomes much larger.

### Interpretation

Even before exact support/noise formulas are available, the source parameters already show that the candidate is not a monotone "align more = always better" trick.

It is naturally a Pareto optimization over:
- transform-side automorphism/key-switch classes;
- fixed-field degree/security;
- structured-basis geometry;
- eventually the exact bootstrapping error/nonlinear range.

This strengthens the conceptual contribution if the construction survives, but also raises the bar for a positive result.

## Refined status after Gate 2

COSET_HOISTING_ALGEBRA:
    PASS.

SOURCE_FAITHFUL_MULTIDIMENSIONAL_FIELD:
    PASS.

GLOBAL_STABILIZER_ALLOCATION_MODEL:
    PASS.

B2_PARETO_STRUCTURE:
    PASS under source-derived support/geometry upper-bound proxies.

EXACT_AUTOMORPHISM_SUPPORT:
    BLOCKED_BY_UNPUBLISHED_PART2 / NOT_ESTABLISHED.

EXACT_SECRET_ERROR_GEOMETRY:
    NOT_ESTABLISHED.

END_TO_END_KS_SAVING:
    NOT ESTABLISHED.

CURRENT_LABEL:
    PROMISING_SOURCE_INCOMPLETE.

Do not run Codex/native work.

Reopen exact Gate 2 immediately if Part 2 or an equivalent explicit basis/transform construction becomes available.
