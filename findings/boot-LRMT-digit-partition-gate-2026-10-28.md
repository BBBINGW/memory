# BOOT — Function-aware digit partitioning for low-rank CKKS FBT

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

## Source target

Supplied source:
papers/supplied/2026-1264.pdf
Git blob SHA: 6f1d2330176bf4add587118b8c4cd274b8a576c7

Title:
"The Power of Low Rank: Fast CKKS Functional Bootstrapping for High-Precision Lookup Tables"

Relevant verified pages:
- pp.3-5: spectral framework and LRMT-FBT overview.
- pp.7-8: LUT matrix notation with general P=alpha*beta.
- pp.11-18: truncated-SVD correctness and exact/numerical low-rank classes.
- pp.19-23: LRMT-FBT algorithm, fixed digit split, KProduct, implementation choice.
- pp.23-26: balanced decomposition and stage-by-stage performance.
- pp.31-32: FDD and KProduct algorithms.

## What 1264 already establishes

For input x in Z_P, reshape the LUT into

    M_f in R^{alpha x beta},   M_f[i,j] = f(i*beta+j),   P=alpha*beta.

If the row/column selector vectors are delta_MSD and delta_LSD, then

    f(x) = delta_MSD^T M_f delta_LSD.

A rank-r factorization

    M_f ~= sum_{k=1}^r sigma_k u_k v_k^T

reduces the LUT stage to:
- r(alpha+beta) scalar multiplications;
- r ciphertext multiplications;
- two multiplicative levels.

For balanced alpha=beta=sqrt(P), this is 2r sqrt(P) scalar multiplications and r ciphertext multiplications.

The paper proves low rank for many common one-input LUT classes and exponential singular-value decay for analytic functions.

## Important unexploited source detail

Algorithm 3 fixes the digit split at

    s = ceil(t/2)

for t radix-p digits:
- low-order digits 0,...,s-1 form delta_LSD;
- high-order digits s,...,t-1 form delta_MSD.

Section 5.2 explicitly chooses the radix so that t is a power of two and uses an even contiguous partition with alpha=beta=sqrt(P), because this balances the two KProduct calls.

The paper does not present a function-aware search over alternative balanced digit subsets.

Appendix Algorithm 6, however, defines KProduct on an arbitrary list of ciphertext vectors. Its multiplication count/depth depends on:
- the number of input digit vectors;
- their lengths;
not on the semantic significance or contiguity of the digit positions.

Therefore a permutation/regrouping of already-produced FDD digit one-hot vectors can change the LUT matrix factorization without adding a new homomorphic primitive.

## Function-aware partition model

Let the radix-p input have t digits

    x = (x_0,...,x_{t-1}),   x_i in [p].

Choose a bipartition

    A union B = [t],   A intersect B = empty.

Define the communication/LUT matrix

    M_f^{A|B}[a,b] = f( merge_A,B(a,b) ),

where rows are assignments to digits in A and columns are assignments to digits in B.

Its dimensions are

    alpha_A = p^{|A|},
    beta_B  = p^{|B|}.

After FDD:
- KProduct(A) creates the row selector;
- KProduct(B) creates the column selector;
- the low-rank evaluator uses an SVD/factorization of M_f^{A|B}.

For balanced partitions |A|=|B|=t/2, every partition has:
- the same row/column dimensions sqrt(P);
- the same number of FDD outputs;
- the same KProduct output sizes;
- the same KProduct multiplicative depth;
- the same asymptotic and exact multiplication count in Algorithm 6, up to bookkeeping/order.

Thus, among balanced partitions, minimizing the numerical rank is an offline optimization with no intrinsic extra homomorphic cost.

Define

    r_epsilon^*(f)
      = min_{A: |A|=t/2} rank_epsilon(M_f^{A|A^c}).

The 1264 baseline uses one particular contiguous A; it need not attain r_epsilon^*(f).

## Theorem — exponential rank gap under a free balanced repartition

Take binary digits, p=2, and t=4q.

Let the standard contiguous partition be

    A0 = {0,...,2q-1},
    B0 = {2q,...,4q-1}.

Let E_L be the q even-position digits lying in A0 and E_R the q even-position digits lying in B0. Let all odd-position digits be irrelevant to the target function.

Define

    f(x) = 1[ x_{E_L} = x_{E_R} ].

### Rank under the standard contiguous split

A row assignment consists of:
- q relevant even bits r;
- q irrelevant odd bits u.

A column assignment consists of:
- q relevant even bits c;
- q irrelevant odd bits v.

Hence, after ordering coordinates as (r,u) and (c,v),

    M_f^{A0|B0} = I_{2^q} tensor J_{2^q},

where J is the all-ones matrix.

Therefore

    rank(M_f^{A0|B0}) = 2^q.

Moreover, the nonzero singular values are all 2^q, so the matrix is not numerically low-rank at any small correctness threshold such as 1/(2P).

### Rank under an alternative balanced split

Let

    A* = all 2q even-position digits,
    B* = all 2q odd-position digits.

Both sides still contain exactly 2q digits, so the selector dimensions remain

    2^{2q} x 2^{2q} = sqrt(P) x sqrt(P).

But f depends only on the row assignment A*. Every column is identical, so

    rank(M_f^{A*|B*}) = 1.

Thus a zero-extra-online-cost balanced digit repartition changes the exact rank by

    2^q -> 1

with

    2^q = P^{1/4}.

This is an exponential separation in the number of digit pairs.

## Practical multi-input examples

The same phenomenon appears in natural multi-input predicates.

### Equality of two m-bit values

Order digits as

    x_0,...,x_{m-1}, y_0,...,y_{m-1}.

The natural contiguous x|y split gives

    M_EQ[x,y] = 1[x=y] = I_{2^m},

so

    rank = 2^m.

Instead group complete bit pairs (x_i,y_i):
- first m/2 pairs into A;
- remaining m/2 pairs into B.

Then

    EQ(x,y)
      = EQ_A * EQ_B,

so the matrix is an outer product and

    rank = 1.

The two partitions have the same number of binary digits on each side, hence the same balanced selector dimensions.

### Less-than comparison

Under the x|y split,

    M_LT[x,y] = 1[x<y]

is a strict triangular matrix of size 2^m, with rank 2^m-1 over R.

Under a partition that keeps high bit-pairs together on one side and low bit-pairs together on the other,

    LT(x,y)
      = LT_high + EQ_high * LT_low.

This is a sum of at most two separable terms, hence

    rank <= 2.

Again the selector dimensions remain balanced.

These examples show that a function can look spectrally flat under one variable split and become exactly low-rank under another.

Caveat: equality and comparison may have cheaper specialized FHE realizations (e.g. subtract-then-test). They prove the structural rank effect but are not yet sufficient application evidence for an LRMT-FBT paper.

## Cost objective

For a general partition A|B, the LRMT LUT-stage work is approximately

    C_LUT(A)
      ~ c_s * r_A * (p^{|A|}+p^{|B|})
        + c_m * r_A,

where r_A is the retained exact/numerical rank and c_s,c_m reflect scalar/ciphertext multiplication costs.

The KProduct stage also scales with the selector sizes, so an unbalanced partition can lose front-end efficiency.

Therefore the real offline objective is not rank alone:

    minimize_A  C_FDD
              + C_KProduct(|A|,|B|)
              + C_LUT(r_A,|A|,|B|)
              + noise/level penalties.

For balanced A, C_FDD and C_KProduct are essentially fixed, so rank minimization is especially clean.

## Value gate from 1264's own profile

At P=2^20 and ReLU rank r=2, the 1264 single-thread breakdown reports approximately:
- FDD: 645 s;
- cleaning: 113 s;
- KProduct: 259 s;
- LUT evaluation: 42.6 s;
- SlotsToCoeffs: 13.7 s.

Thus for functions already having r<=5 under the default split, lowering rank further cannot dramatically improve end-to-end latency because FDD/KProduct dominate.

The candidate is valuable only for functions that:
1. have high/default rank so LUT evaluation is still dominant; and
2. become low-rank under a different no-extra-cost digit partition.

This is the decisive workload criterion.

## Prior-art screen

### Direct FHE/LRMT prior art

Targeted searches for:
- function-aware digit partition + low-rank functional bootstrapping;
- variable partition + CKKS LUT rank;
- communication-matrix rank + FHE lookup tables;
- rank-aware digit grouping for LRMT-FBT

did not surface a direct construction.

The 1264 source itself fixes a contiguous balanced split and motivates it by KProduct balancing, not function-dependent spectral optimization.

This is NOT a novelty proof.

### General theory is old

The matrix M_f^{A|B} is exactly a communication matrix under a variable partition of the input variables.

Communication complexity / knowledge-compilation literature has long studied:
- communication-matrix rank;
- dependence of complexity on variable partition;
- best/worst partitions.

Therefore the abstract mathematical notion
    "choose variables to reduce communication-matrix rank"
is not novel.

Any cryptographic contribution must come from:
- the zero-online-cost compatibility with LRMT-FBT's already-computed FDD outputs;
- FHE-specific cost/noise/depth optimization;
- new function classes or practical workloads where the rank collapse changes bootstrap cost;
- and an efficient partition-selection method.

## Cheapest decisive research gate

Call the candidate:

    RANK_PARTITION_LRMT.

Before any Codex/native work:

1. Reconstruct the exact FDD/KProduct cost for arbitrary balanced digit permutations from 1264.
2. Build a small source-faithful offline analyzer:
   - input LUT and radix-digit metadata;
   - enumerate or search balanced partitions;
   - compute exact or epsilon-numerical rank;
   - report predicted LRMT cost.
3. Test only functions where default rank is nontrivial/high:
   - multi-input LUTs;
   - bit-field predicates;
   - structured control/ALU tables;
   - cryptographic or database predicates not already reducible to a cheaper single-input LUT.
4. Compare against the best algebraic preprocessing (subtract, affine transform, radix remapping) before claiming a win.
5. PARK if all realistic functions that benefit already have a cheaper specialized implementation or default rank <=5.
6. Advance only if at least one realistic function shows a large rank drop at identical balanced selector size and material predicted end-to-end savings.

This first gate does NOT require Codex or a remote server; it is an offline mathematical/source analysis.

## Novelty / priority status

FUNCTION_AWARE_BALANCED_DIGIT_PARTITION:
    ALGEBRAICALLY VALID.

ZERO_EXTRA_HOMOMORPHIC_FRONTEND_COST_FOR_BALANCED_REPARTITION:
    SUPPORTED by 1264 Algorithm 6 structure.

EXPONENTIAL_RANK_SEPARATION:
    PASS (explicit construction).

DIRECT_FHE_PRIOR_ART_COLLISION:
    NOT FOUND IN TARGETED SEARCH.

GENERAL_VARIABLE_PARTITION_RANK_THEORY:
    PRIOR ART outside FHE.

PRACTICAL_WORKLOAD_VALUE:
    NOT ESTABLISHED.

NOVELTY:
    PROMISING_NOT_ESTABLISHED.

CCF_A_B_READINESS:
    NO, requires a real workload class + optimizer + end-to-end cost evidence.

CODEX_REQUIRED_NOW:
    NO.

## Current BOOT paper-only priority

This candidate should be kept alongside the 2026/1779 partial-recovery interaction-rank line.

Suggested order before native access returns:

1. RANK_PARTITION_LRMT — cheapest positive source/algebra gate; supplied full source available.
2. 1779 partial-recovery interaction rank — stronger theory flavor but blocked on missing full text.
3. 2630 lossy-KS -> exact-error bootstrap — lower priority and source-blocked.

B163 remains the highest native gate when Codex quota is explicitly restored by the PI.
