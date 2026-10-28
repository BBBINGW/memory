# BOOT — Polynomial-cleaning split-tree lower bound and higher-radix prior-art closure

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

## Source trigger

Two supplied current papers were read directly from papers/supplied:

1. ePrint 2026/2600 — Ma, Liu, Wang, Wang,
   "High-precision Bootstrapping for GCKKS"
   repository source: papers/supplied/2026-2600.pdf
   Git blob SHA: 8db712155d087284d21e924623496bc48e36eb72

2. ePrint 2026/2531 — Cheon, Lee,
   "High-Precision CKKS with Focal Units"
   repository source: papers/supplied/2026-2531.pdf
   Git blob SHA: ca85d988bc85d7a242bf3f07b55df4687556b567

Relevant verified pages:
- 2600 pp.18-25: iterative split/precision-doubling, joint clean-before-split, complexity.
- 2531 pp.34-38: order-M focused cleaning, iterated cleaning, tree-like cleaning, higher-radix split statement.

## What 2600 already does

For the bit-cleaning polynomial
    h1(x)=3x^2-2x^3,
2600 deliberately delays the ciphertext split:
- compute the needed powers x^2 and x^3 on one parent ciphertext;
- keep the tensor/relinearization work shared;
- only then apply even/odd masks and create two cleaned children.

The paper explicitly states that the purpose is to carry out a larger portion of the computation on one ciphertext rather than duplicate it after splitting.

Its precision-doubling stage:
- starts from k=4;
- performs log2(k/4) split iterations;
- doubles the number of ciphertexts every iteration;
- consumes three scale layers per iteration in the concrete design;
- has total key-switching count bounded by 15k.

Therefore:
    "share h1 power computations before binary split"
is DIRECT PRIOR ART in 2600.

## Higher-radix split is also direct prior art

2531 gives a general order-M cleaning polynomial P for a discrete set D.

Its Proposition 16 states that an order-M cleaner improves focus-slot precision approximately by a factor M+1 in one cleaning.

The tree-like cleaning section (physical p.36) explicitly states:

- h1 roughly doubles precision and therefore splits one ciphertext into two;
- for an order-M cleaning polynomial, the same tree construction splits into M+1 parts instead of two.

Thus the direct idea
    "replace several binary split-clean rounds by a higher-order cleaner and higher-radix split"
is already explicitly recognized in current prior art.

Status:
    HIGHER_RADIX_SPLIT_WITH_ORDER_M_CLEANER = PRIOR ART.

## Model-level polynomial depth lower bound

We can still derive a useful structural lower bound explaining why the precision-growth tree cannot be collapsed to O(1) multiplicative depth within a polynomial-cleaning model.

### Definition

Let P in K[x] be a cleaner for Boolean points {0,1} over a field K.

Say P has local cleaning order r>=2 if

    P(x) = O(x^r)              as x -> 0,
    1-P(1+x) = O(x^r)         as x -> 0.

Equivalently,

    P(0)=0, P(1)=1,

and

    P^(j)(0)=P^(j)(1)=0
for every 1<=j<r.

This means an input error epsilon near either Boolean fixed point is reduced to O(epsilon^r).

### Theorem — degree lower bound

If char(K)=0 or char(K)>deg(P), every order-r Boolean cleaner satisfies

    deg(P) >= 2r-1.

Proof:
P' has a zero of multiplicity at least r-1 at x=0 and another zero of multiplicity at least r-1 at x=1. These are distinct roots, so

    deg(P') >= 2(r-1),

hence

    deg(P) >= 2r-1.

The bound is tight: the normalized integral

    P_r(x)
      = [ integral_0^x t^(r-1)(1-t)^(r-1) dt ]
        / [ integral_0^1 t^(r-1)(1-t)^(r-1) dt ]

has degree 2r-1 and satisfies exactly these endpoint multiplicity conditions.

For r=2 this gives the cubic smoothstep
    3x^2-2x^3,
the cleaner used in 2600/CKSS-style precision doubling.

### Corollary — multiplicative-depth lower bound

An arithmetic circuit starting from x and constants, using additions and multiplications, with multiplicative depth D, computes a polynomial of degree at most 2^D.

Therefore an order-r cleaner needs

    D >= ceil(log2(2r-1)).

If the precision must grow by a factor r=2^m, then

    D = Omega(m).

For split-tree schemes where the precision/slot tradeoff requires r on the order of the final slot-reduction factor k, this gives an unavoidable Omega(log k) multiplicative-depth dependence inside the polynomial-cleaning model.

## Interpretation for 2600 and 2531

This does NOT prove that the exact concrete 2600 design is constant-factor optimal.

2600 uses three scale layers per binary iteration, whereas the abstract polynomial degree lower bound gives only roughly one to two multiplicative-depth units per precision-doubling factor.

2531 also notes constant-factor improvements from "thrifty" evaluation and allows order-M cleaners.

Therefore constant-factor modulus-depth improvements may remain possible.

But the broad target

    "collapse log k precision-growth iterations to O(1) depth by a direct higher-order polynomial"

is impossible in this model.

Furthermore, the natural higher-radix construction itself is already present in 2531.

## Capacity lower bound on ciphertext count

A separate information/capacity observation reinforces the tree structure.

If a representation with parameter k stores only a 1/k fraction of the original useful slots per ciphertext, preserving all original values after increasing k by a factor r requires at least r ciphertext carriers, absent a change in ciphertext representation.

Thus:
- binary precision doubling naturally produces two children;
- an r-fold slot reduction requires at least r output carriers if all values are retained.

This does not constrain how the computation is scheduled, but it rules out reducing the final carrier count solely by changing the cleaner.

## Prior-art / novelty decision

SHARED_CLEAN_BEFORE_BINARY_SPLIT:
    DIRECT PRIOR ART (2600).

HIGHER_ORDER_CLEANER:
    EXISTING GENERAL CLEANING / HERMITE PRIOR ART.

HIGHER_RADIX_TREE_SPLIT:
    DIRECT PRIOR ART (2531).

O(1)_DEPTH_PRECISION_GROWTH_BY_POLYNOMIAL_CLEANING:
    FAIL by degree/depth lower bound.

ASYMPTOTIC_LOG_K_PRECISION_GROWTH_DEPTH:
    STRUCTURALLY NECESSARY in the stated polynomial-cleaning model.

CONSTANT_FACTOR_IMPROVEMENT:
    MAY REMAIN, but not a strong standalone CCF-A/B direction without another structural ingredient.

NOVELTY:
    NOT ESTABLISHED.

CODEX/NATIVE:
    NOT REQUIRED.

## Research decision

PARK this branch.

Do not spend BOOT cycles on:
- higher-radix split as a standalone idea;
- direct replacement of repeated h1 with a high-order smoothstep as the main contribution;
- claims that log k cleaning depth can be removed inside an ordinary polynomial-cleaning model.

A future revisit would require a non-polynomial cleaner, a new ciphertext representation, or a cross-stage fusion that changes the model rather than optimizing the same split-clean tree.

B163 remains the highest native gate once Codex quota returns.
