# PURE-FHE P0-PRESCOUT-64 — General A2D Carry-Structure / Best-Radix Value Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-64
LATEST_COMPLETED: P0-PRESCOUT-64
NEXT_ITERATION: NOT_STARTED / PROBLEM_RESELECTION
STATUS: PASS_LOCAL_SPARSE_ALPHA_REDUCTION / FAIL_BEST_RADIX_VALUE_ADVANTAGE / PRIOR_ART_COMPACT_PREFIX / KILL_CURRENT_A2D_CARRY_OPTIMIZATION
NOVELTY: NOT ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Primary source and bottleneck

Primary source:

Jiaming Liu, Shihe Ma, Anyu Wang, Xiaoyun Wang,
"High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping,"
ePrint 2026/1869.

Supplied source:
  papers/supplied/2026-1869.pdf
  blob SHA 9de785af66b3106e509283c84816513d56f6f7dd.

The paper's general arithmetic-to-digit (A2D) conversion uses exactly two functional bootstraps followed by logarithmic-depth carry composition.

For radix B=b^s, after the first bootstrap and linear preprocessing the source derives

  a_j = d_j + c_j - B c_{j+1} - lambda alpha_j,

with a last-block radix b^h when needed.

Here:
- d_j is the canonical radix-B digit;
- c_j is the carry;
- lambda = kappa + I'_{d-1} lies in a public finite candidate set Lambda;
- alpha_j is the grouped defining-polynomial coefficient.

For fixed lambda and current carry c, a deterministic unary transition f_{j,lambda}(c) gives the next carry.

The source's Appendix C represents every transition as a one-hot relation over one global carry alphabet C and composes relations by matrix multiplication. Each doubling level costs

  |Lambda| |C|^3

ciphertext-ciphertext multiplications.

This can be enormous for arbitrary moduli.

## 2. Initial H64

H64 initially proposed:

Exploit the sparsity of alpha_j and use position-dependent carry alphabets C_j, sharing lambda-independent transition computation at positions with alpha_j=0.

The concrete test case is P-384 with source defining polynomial

  F_384(X)=X^384-X^128-X^96+X^32-X^2+3,

arithmetic base b=2, and overflow bound |I'_i|<=17.

For B=32 (s=5):
- ell=ceil(384/5)=77;
- Lambda={-17,...,17}, so |Lambda|=35;
- only four radix blocks have nonzero grouped coefficient:

  alpha_0=-1,
  alpha_6=4,
  alpha_19=-2,
  alpha_25=-8.

Thus 73/77 local transitions are lambda-independent.

## 3. [DERIVATION] Local carry alphabets

Using the source Appendix-C nonnegative remainder representatives and its Eq.10-style bound, the local outgoing carry ranges are:

- ordinary alpha_j=0 block: {-1,0,1}, size 3;
- j=0: size 5;
- j=6: size 7;
- j=19: size 5;
- j=25: size 11;
- final short B_last=16 block: size 5.

The source's global union is therefore

  C={-5,...,5},

so |C|=11.

The source-style one-hot composition cost is then

  35 * 11^3 = 46,585 CMult

per carry-composition level.

With ceil(log2 77)=7 levels:

  326,095 CMult

before candidate selection.

## 4. [TOY_EXECUTED] Exact recurrence sanity

An exhaustive-style randomized algebra sanity was executed locally for 10,000 random P-384 representatives using:
- random message bits;
- random overflow coefficients I'_i in [-17,17];
- lambda=I'_{383};
- the source F_384 coefficients;
- source nonnegative radix remainders.

Every tested radix position satisfied exactly

  a_j = d_j + c_j - B_j c_{j+1} - lambda alpha_j.

Observed carry values remained inside the local intervals above.

This is only a sanity check; the source equations and deterministic bounds are the main evidence.

## 5. Same-depth heterogeneous factorization

To avoid buying savings with extra multiplicative depth, the original seven-level doubling topology was retained.

At a doubling distance delta, each composition depends on three boundary state sets:

  C_start x C_mid x C_end.

For positions whose composed interval contains one of the four alpha-active blocks, the transition remains lambda-dependent. Other positions may share one transition composition across all lambda.

Taking the union of necessary state triples at each level gives:

delta | shared triples | lambda-dependent triples
1     | 117            | 171
2     | 117            | 171
4     | 117            | 189
8     | 117            | 207
16    | 117            | 159
32    | 0              | 105
64    | 0              | 27

Totals:
  shared =585,
  dependent=1029.

Hence the same-depth CMult upper bound becomes

  585 + 35*1029 = 36,600.

This is an 8.91x reduction from 326,095 while preserving the seven carry levels.

So the LOCAL sparse-alpha hypothesis is real.

## 6. Why the initial 55x estimate was withdrawn

A sequential segmented propagation can push the candidate-specific count down toward 6-7k CMult, but it serializes the four alpha-active boundaries and/or waits for long segment-prefix maps.

The clean source-matched implementation therefore increases multiplicative depth relative to the original seven-level scan.

Under the project's same-depth comparison rule, the valid result is the 8.91x reduction above, not the earlier rough 45-55x estimate.

## 7. Compact prefix / carry monoid prior art

The broad insight "carry propagation should not be represented as a dense one-hot transition matrix" is not novel.

Concurrent 2026 work includes:
- Shen et al., ePrint 2026/1840, whose binary-carry A2B uses a compact carry state and one ciphertext multiplication per doubling iteration.
- Bkakria et al., arXiv:2607.03631, "Rotation-Optimal Noncommutative Prefix Scans in Bit-Reversed Homomorphic Layouts," which gives generic associative possibly noncommutative packed prefix scans and instantiates them for radix-CKKS carry/borrow.

Therefore:
- compact carry monoids;
- logarithmic prefix scan;
- routing-optimal carry propagation

cannot be novelty claims.

The only potentially distinct aspect of H64 was the source-specific combination of:
- a global candidate parameter lambda;
- sparse lambda-dependent alpha_j positions;
- heterogeneous position-dependent carry alphabets.

## 8. Decisive best-radix killer

The B=32 comparison is not a fair final baseline because the source is free to choose a larger output radix.

The source itself discusses the carry/LUT tradeoff: increasing B reduces radix positions and may reduce carry states, while increasing the lookup domain.

Therefore P-384 was re-evaluated over multiple radix widths.

### Source global one-hot cost using nonnegative representatives

Representative points:

B=16:
  global |C|=7,
  carry cost ~=84,035 CMult.

B=32:
  global |C|=11,
  carry cost ~=326,095.

B=64:
  global |C|=5,
  carry cost ~=26,250.

B=256:
  global |C|=3,
  ell=48,
  six carry levels,
  carry cost ~=5,670.

Thus the source's own best-radix baseline already removes most of the apparent B=32 bottleneck.

## 9. Stronger killer: centered representatives at B=256

Section C.3 of the same source already uses centered remainder representatives in the power-of-two specialization to minimize carry states.

Apply the same valid representative choice to general P-384 A2D:

  -B/2 <= r_j < B/2.

For B=256:
- |I'|<=17;
- the grouped nonzero alpha_j values are only +/-1;
- therefore even with |lambda|<=17, the next-carry numerator always lies strictly between -B and 2B.

The only possible carries are

  C={0,1}.

Hence:

  |C|=2,
  ell=48,
  depth=ceil(log2 48)=6,

and the original one-hot relation composition costs only

  35 * 2^3 * 6 = 1,680 CMult.

This completely changes the value comparison.

The same-depth heterogeneous-state technique can no longer offer a main-term improvement over the best source-shaped radix/representative baseline.

## 10. Representation-switch subprobe

The source also states that for a fixed modulus M, arithmetic representations under different (b,F_M) choices can be converted by a public linear transformation.

A second cheap test asked whether computation could use one arithmetic base and switch to a conversion-friendly base immediately before A2D.

For P-384 the source provides b=2,4,8,16 defining polynomials.

However, once the final digit radix B=b^s is matched, the grouped carry geometry essentially collapses to the same effective radix structure.

For example:

  (b,s)=(2,8),(4,4),(16,2)

all give

  B=256,
  ell=48,

and under centered representatives all have a binary global carry alphabet and the same 1,680-CMult one-hot prefix estimate.

Thus public representation conversion does not create a distinct A2D complexity advantage in this test.

## 11. Sparse defining-polynomial tangent — failed

A separate cheap subprobe tried to redesign the Curve25519 defining polynomial to make alpha_j sparse.

Examples satisfying F(2)=2^255-19 and having no immediate real-root obstruction were found, e.g. sparse forms around degree 256.

However their arithmetic-growth constant mu(F) was orders of magnitude worse than the source polynomial:
- source b=2 Curve25519: mu(F)=2508;
- tested sparse candidates: mu(F) ranged from hundreds of thousands to astronomically larger values.

Therefore "just make F sparse" fails the source's arithmetic-growth admissibility criterion and is not retained.

## 12. Final decision

STATUS:

  PASS_LOCAL_SPARSE_ALPHA_REDUCTION /
  PASS_SAME_DEPTH_8.9X_AT_B32 /
  FAIL_BEST_RADIX_VALUE_ADVANTAGE /
  PRIOR_ART_COMPACT_PREFIX /
  KILL_CURRENT_A2D_CARRY_OPTIMIZATION.

Interpretation:

- Sparse alpha_j and heterogeneous carry alphabets are mathematically real.
- At a fixed poor radix B=32 they cut carry relation composition by 8.9x at the same depth.
- But a fair source-shaped baseline can choose B=256 and centered remainders, reducing the global carry to two states and the one-hot prefix to only ~1,680 CMult.
- The residual heterogeneous-state advantage is no longer a main-term contribution.
- Generic compact carry/prefix machinery is also strong prior art.

No implementation is warranted.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-64

CODEX_REQUIRED:
NO.

NEXT:
Return to problem-level PURE-FHE reselection.
Do not reopen this A2D line for:
- compact binary carry monoids;
- generic prefix-scan routing;
- heterogeneous C_j alone;
- radix parameter micro-tuning;
- sparse F_M without simultaneously passing mu(F)/conditioning.

Only reopen if a new construction changes the two-FBS main term or proves a nontrivial lower/upper bound across the full radix/LUT/carry tradeoff.

STATE_UPDATE:
YES — this finding only.
