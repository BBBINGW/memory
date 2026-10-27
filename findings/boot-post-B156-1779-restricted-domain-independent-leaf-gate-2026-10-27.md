# BOOT post-B156 — 2026/1779 restricted-domain independent-leaf gate

Date: 2026-10-27
TRACK_ID: BOOT
State impact: NONE. Do not modify B157 pending state.
No Codex / GPU / remote execution was used.

## Source status

Target:
- ePrint 2026/1779, Zhaoyang Liang and Dan Ding,
  *Bootstrapping via Ring Switching without Slot Recovery: Independent Leaf Evaluation for SIMD-Packed Ciphertexts*.

Current public abstract (revision dated 2026-10-26) states:
- CKKS and BGV/BFV bootstrapping can proceed after ring switching without slot recovery;
- a continuous slotwise function admits independent leaf evaluation for unrestricted real CKKS inputs iff it is affine;
- CKKS: N=2^17, n=2^16, 1.13x serial, 2.03–2.18x with two leaves parallel;
- BGV: p=65537, N=2^16, n=2^15, 1.30x serial, 1.63x throughput, keygen -50.6%, server-key size -48.6%.

Full 1779 PDF is still not available through the configured ePrint/mirror acquisition path:
- IACR PDF: HTTP 403;
- no exact-title arXiv copy found;
- fixed GitHub ePrint mirror does not contain it.

Therefore this note does NOT claim full-paper coverage.

## Question

Does the affine-only obstruction disappear for the restricted/discrete plaintext domains used by discrete CKKS / functional bootstrapping, allowing a useful nonlinear function to be evaluated independently on ring-switch leaves?

## Factor-2 leaf algebra from standard ring switching

Classical ring switching decomposes a big-ring plaintext as

a(X) = sum_{k=0}^{u-1} X^k * a_k(X^u).

For u=2,

a(X) = a_0(X^2) + X a_1(X^2).

Pair the big-ring slots at zeta and -zeta:

x = a(zeta)
y = a(-zeta).

Define the two small-ring leaf coordinates

A = a_0(zeta^2) = (x+y)/2
B = zeta a_1(zeta^2) = (x-y)/2.

The public scalar zeta can be absorbed into the leaf representation. Thus the essential leaf transform is the two-point Hadamard/sum-difference transform.

Suppose independent leaf functions G and H are applied before reconstruction. To recover a slotwise target f on both original slots, we need

G((x+y)/2) + H((x-y)/2) = f(x)
G((x+y)/2) - H((x-y)/2) = f(y).

Equivalently,

G((x+y)/2) = (f(x)+f(y))/2
H((x-y)/2) = (f(x)-f(y))/2.

This gives an exact finite-domain consistency condition.

## Finite-domain classification

Let S be the allowed slot-value set.

An independent-leaf realization exists on S iff the following values are well-defined:

- f(x)+f(y) depends only on x+y;
- f(x)-f(y) depends only on x-y.

The second condition follows from the first, because

x-y = u-v  <=>  x+v = u+y.

Hence the condition is exactly:

x+y = u+v
  => f(x)+f(y) = f(u)+f(v).

This is a Freiman-2 / additive-relation preservation condition on f restricted to S.

### Ordinary discretized integer alphabet

For an arithmetic progression

S = {a, a+h, ..., a+(p-1)h},

with p >= 3, take three consecutive points x_k, x_{k+1}, x_{k+2}. Since

x_k + x_{k+2} = 2 x_{k+1},

the leaf consistency condition forces

f_k + f_{k+2} = 2 f_{k+1}.

Thus every second finite difference is zero, and f is affine on the entire discrete alphabet.

For p=2 there is no nontrivial constraint, but any function on two points is already the restriction of an affine real function. Therefore the binary case does not create genuinely new nonlinear functionality.

Decision:
- DISCRETE_UNIFORM_ALPHABET_ESCAPE: FAIL
- SMALL_INTEGER_CKKS_ESCAPE: FAIL
- BINARY_ESCAPE: TRIVIAL_ONLY

This directly covers the normal finite-integer/discrete-CKKS use case.

## General arbitrary-LUT escape: Sidon-like codebooks

For every possible LUT f:S->R to satisfy the consistency condition, S must have no nontrivial additive relation

x+y=u+v

between different unordered pairs. In other words, S must be Sidon/Freiman-independent enough that all pair sums are unique.

This is mathematically possible, but creates a structural efficiency penalty.

### Robust range lower bound

For p codepoints, Sidon-ness also forces all p(p-1)/2 positive pair differences to be distinct.

If the encoding must be robust to CKKS error with minimum distinguishable difference separation delta, then these p(p-1)/2 positive differences must occupy a range of at least

Omega(p^2 * delta).

Equivalently, the dynamic-range / resolution ratio is Omega(p^2), costing about 2 log2(p) bits of numerical range/precision.

This argument is not restricted to integer codepoints: with bounded real codepoints and robust minimum separation between the leaf sum/difference values, the same pigeonhole bound applies.

### Leaf-function domain size

A Sidon-like p-point codebook produces Theta(p^2) distinct pair sums/differences. Therefore the independently evaluated leaf functions G/H are specified on Theta(p^2) input points.

For a generic arbitrary LUT f, no special algebraic structure can be assumed in those induced G/H values. Interpolation-based realization therefore moves from a p-point target problem toward a p^2-point leaf problem.

This defeats the intended reason for eliminating slot recovery.

Decision:
- SIDON_CODEBOOK_ESCAPE: MATHEMATICALLY_POSSIBLE
- SIDON_CODEBOOK_VALUE: LOW / RANGE_AND_LUT_SIZE_BLOWUP
- PURSUE_AS_BOOTSTRAP_OPTIMIZATION: NO

## Relevance to current discrete-CKKS work

Contemporary discrete-CKKS functional bootstrapping works encode finite integer domains and evaluate LUT/interpolation functions over those integer messages. This is the arithmetic-progression case above, so the affine-only obstruction survives discretization.

## Current decision

The natural restricted-domain extension of 2026/1779 does NOT yield a useful nonlinear independent-leaf functional bootstrap:

- unrestricted real: affine only, per 1779 public abstract;
- ordinary finite integer / discretized CKKS domain with >=3 points: affine only by exact finite-difference argument;
- two-point domain: all functions are trivially affine on two points;
- arbitrary nonlinear LUT requires Sidon-like recoding, which produces quadratic dynamic-range and leaf-domain growth.

STATUS:
- RESTRICTED_DOMAIN_NONLINEAR_LEAF_EVAL: FAIL_FOR_STANDARD_DOMAINS
- SPECIAL_CODEBOOK_ESCAPE: LOW_VALUE
- FULL_1779_SOURCE: STILL_REQUIRED before attributing any theorem details beyond the public abstract
- NOVELTY_CLAIM: NONE

Do not spend native/Codex resources on this branch.
