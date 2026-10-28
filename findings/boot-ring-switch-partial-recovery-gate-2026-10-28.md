# BOOT — Ring-switch partial-recovery / interaction-rank gate

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state (unchanged)

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Source target and blocker

Primary target:
Zhaoyang Liang and Dan Ding,
"Bootstrapping via Ring Switching without Slot Recovery: Independent Leaf Evaluation for SIMD-Packed Ciphertexts",
IACR ePrint 2026/1779, revised 2026-10-26.

Public abstract states:
- ring switching reduces bootstrap arithmetic by moving computation to smaller rings;
- conventional SIMD ring-switch pipelines use slot recovery because slot layout changes;
- slot recovery consumes capacity and requires synchronization across ciphertexts;
- the paper shows CKKS and BGV/BFV bootstrapping can proceed directly after ring switching;
- for unrestricted real CKKS inputs, a continuous slotwise function admits independent leaf evaluation iff it is affine.

Full text was not acquired in this round:
- official IACR PDF: HTTP 403;
- exact-title arXiv fallback: no matching result;
- fixed arturo-kong ePrint mirror: 2026/1779.pdf absent.

Therefore the exact leaf map, recovery transform, key requirements, synchronization primitive, and the scope/proof of the affine-only theorem are SOURCE-GATED. Do not claim the model below is the paper's exact algebra.

Public abstract mirror:
https://eprint.iacr.asia/days/7

## Research question

The 1779 affine-only theorem closes the strongest goal:
    ZERO_RECOVERY + COMPLETELY_INDEPENDENT_LEAVES + GENERAL_CONTINUOUS_NONLINEAR_SLOTWISE_FUNCTION.

A narrower question remains:

Can a nonlinear slotwise function be evaluated after ring switching with *partial* cross-leaf synchronization whose cost scales with the function's interaction/separation rank, instead of full slot recovery?

The goal is not to recover original slots. It is to exchange only sufficient statistics required by the target nonlinearity.

This is a model-level candidate until the exact 1779 leaf representation is recovered.

## Two-leaf linear-mixing model

Assume two leaf plaintext variables u and v encode one original scalar through a nondegenerate linear mix

    x = alpha*u + beta*v,

with alpha,beta nonzero over a field K.

Let p(x) be a polynomial of degree d>=2,

    p(x)=c_0+c_1 x+...+c_d x^d, c_d != 0.

Write

    P(u,v)=p(alpha*u+beta*v).

Allow all purely local terms A(u)+B(v) to be evaluated independently for free. Let M(u,v) be the mixed part containing exactly monomials u^i v^j with i,j>=1.

Define the interaction separation rank r_int(P) as the minimum R such that

    M(u,v) = sum_{r=1}^R g_r(u) h_r(v)

for univariate polynomials g_r,h_r.

This captures the minimum number of multiplicatively separable cross-leaf channels in this algebraic model.

## Theorem: exact two-leaf interaction rank is d-1

Assume char(K)=0 or char(K)>d, and alpha*beta*c_d != 0.

Then

    r_int(p(alpha*u+beta*v)) = d-1.

### Proof

The coefficient of u^i v^j in P for i,j>=1 is

    C_{i,j}
      = c_{i+j} * binom(i+j,i) * alpha^i * beta^j

when i+j<=d, and zero otherwise.

Index i,j from 1 to d-1. The coefficient matrix C represents the mixed bivariate polynomial. A decomposition
    M=sum_r g_r(u)h_r(v)
corresponds exactly to a rank-one outer-product decomposition of C, so the minimum number of separable terms equals rank(C).

Reverse the column order. Entries beyond the anti-diagonal i+j=d are zero, while the anti-diagonal entries are

    c_d * binom(d,i) * alpha^i * beta^(d-i),

for i=1,...,d-1.

Under the characteristic/nondegeneracy assumptions all are nonzero. Therefore the reversed matrix is triangular with nonzero diagonal, so

    rank(C)=d-1.

QED.

## Consequences

### Affine boundary recovered

For d=1 there is no mixed term:
    r_int=0.

This is consistent with the public abstract's affine-only boundary for completely independent leaf evaluation.

This consistency is only conceptual; it is not a reconstruction of the paper's theorem.

### Quadratic nonlinearities need one cross statistic

For p(x)=x^2,

    p(alpha u+beta v)
      = alpha^2 u^2 + 2 alpha beta uv + beta^2 v^2.

All local squares are leaf-local; only uv is cross-leaf.

Thus in the model:
    EXACT_QUADRATIC_CROSS_CHANNELS = 1.

### Cubic degree needs two

For degree 3, the mixed coefficient matrix has rank 2. No single separable cross term can represent the exact mixed part for generic nondegenerate alpha,beta.

### General degree

Exact cross interaction grows linearly with polynomial degree:
    d-1
for two leaves.

Thus the correct structural hope is not "nonlinear for free"; it is:
    low-degree nonlinear function -> few cross-leaf sufficient-statistic channels.

## Multi-leaf caution

For L leaves and a degree-d monomial of a nondegenerate linear form,

    (sum_l alpha_l u_l)^d,

the direct multinomial expansion contains
    binom(L+d-1,d)
degree-d monomials, of which L are pure one-leaf terms.

This is only a naive exact upper bound on mixed statistics, NOT a tensor-rank lower bound.

A two-way flattening gives at least the two-leaf-style d-1 obstruction whenever two leaf groups both enter nondegenerately, but the exact L-way interaction rank may be smaller than the raw multinomial count.

Do not claim combinatorial minimality without a tensor-rank proof.

## Prior-art screen

### ePrint 2026/1779

Directly closes zero-recovery independent nonlinear leaf evaluation for unrestricted real CKKS according to its public abstract. It is the closest source and the exact scheme must be read before claiming this candidate applies.

### PaCo / ePrint 2025/886, ASIACRYPT 2025

"PaCo: Bootstrapping for CKKS via Partial CoeffToSlot" is terminology-adjacent but structurally different at the abstract/full-public-paper level:
- it reformulates the CKKS decryption circuit using blind rotations and modular additions;
- its "partial CoeffToSlot" enables alternative ring structures;
- it is not presented as low-separation-rank cross-leaf nonlinear evaluation after ring switching.

Thus:
    PACO_DIRECT_COLLISION = NOT_ESTABLISHED.
But it must remain in the prior-art set because partial linear-transform/recovery work is already active.

Primary/open source:
https://orbilu.uni.lu/handle/10993/64983
ePrint 2025/886.

### Search result

Targeted public searches for combinations of:
- partial slot recovery + ring switching,
- independent leaf nonlinear evaluation,
- low-rank/separation-rank leaf synchronization,
did not surface a direct construction beyond 2026/1779 and broader partial-CoeffToSlot work.

This is NOT a novelty proof.

## The real scheme gate

The model becomes interesting only if the exact 1779 construction supports a cheap primitive for one cross statistic.

After full text acquisition, reconstruct:

1. Exact plaintext relation between parent slots and leaf slots after ring switching.
2. Number and shape of leaf ciphertexts.
3. What "synchronization" / conventional slot recovery costs:
   - rotations/key switches,
   - extra ciphertext capacity,
   - communication / data movement,
   - modulus levels.
4. Cost of computing ONE mixed statistic such as u*v across leaves.
5. Whether that statistic can stay in small rings or forces promotion/recovery to the parent ring.
6. Whether multiple cross statistics can be batched/shared.
7. Whether the bootstrap's own nonlinear stage or only an additional fused slotwise function is affected.

## Cheapest decisive value test

For a quadratic target, compare:

A. conventional full slot recovery + ordinary nonlinear evaluation;

against

B. no full recovery, leaf-local u^2/v^2 + exactly one cross statistic uv + recombination.

If one uv channel costs essentially the same as full recovery or requires moving both leaves back to the parent representation, then:
    PARTIAL_RECOVERY_VALUE = FAIL.

If one uv channel is substantially cheaper and remains in small-ring arithmetic, then extend to degree d using the proven d-1 interaction-rank bound.

Do NOT jump directly to a high-degree CKKS EvalMod polynomial. High degree may make d-1 synchronization channels erase the advantage.

## Potential contribution standard

A CCF-A/B-level result would need more than the rank lemma.

Required package:
1. exact scheme-level construction compatible with 1779 ring switching;
2. theorem connecting minimal cross-leaf work to interaction/separation rank;
3. at least one useful low-rank nonlinear family;
4. measurable reduction in recovery rotations/key material/capacity or latency;
5. proof that the reduction is not already PaCo/partial-CtS or generic low-rank linear-transform prior art;
6. security/error analysis under CKKS approximation.

Without 1-4 this remains an algebraic observation.

## Gate decision

ZERO_RECOVERY_GENERAL_NONLINEAR:
    CLOSED_BY_1779_ABSTRACT / AFFINE_ONLY.

TWO_LEAF_INTERACTION_RANK_THEOREM:
    PASS (model-level).

DEGREE_d_EXACT_CROSS_CHANNEL_LOWER_BOUND:
    d-1 in the stated two-leaf polynomial model.

QUADRATIC_ONE_CROSS_STATISTIC:
    PASS algebraically in the model.

ACTUAL_1779_SCHEME_COMPATIBILITY:
    UNKNOWN / SOURCE_BLOCKED.

PARTIAL_RECOVERY_VALUE:
    UNKNOWN.

NOVELTY:
    NOT_ESTABLISHED.

CCF_A_B_READINESS:
    NO.

CODEX/NATIVE:
    NOT_REQUIRED_NOW.

## Next gate

RING_SWITCH_PARTIAL_RECOVERY_GATE_2:
- obtain/read current 2026/1779 full text;
- reconstruct exact leaf linear map and recovery operator;
- instantiate the quadratic case first;
- derive exact operation/key/level count for one cross statistic;
- PARK immediately if one cross statistic is not materially cheaper than full recovery.

B163 remains untouched until Codex quota is explicitly restored by the PI.
