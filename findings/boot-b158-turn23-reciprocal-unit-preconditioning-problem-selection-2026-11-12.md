# BOOT / B158_OVERALL — Research Turn 23/25
## PROBLEM_SELECTION — reciprocal public-unit preconditioning

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-reciprocal-unit-preconditioning-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 23 had ACTIVE=UNKNOWN. This candidate is distinct from the recently closed gauge-search, public-key programmable-gauge, sparse-key, ring-switch, lazy-relinearization and external-product families.

The mechanism uses only FREE public scalar multiplication under the existing same-ring key and modulus chain. It therefore tests whether a zero-key-cost public preconditioner can change the B175 pointwise tensor/reference geometry.

## Candidate mechanism

Let the B175 pointwise operands be L=LT8 and G=GROUPED. Choose nonzero plaintext units lambda, mu in Z_T with
  lambda * mu = 1 mod T.

Apply the centered scalar representatives to ciphertext components:
  L' = lambda * L,
  G' = mu * G,
then execute the same MulRelinScaleInvariant(L',G').

Because lambda*mu=1 mod T, the plaintext product is unchanged. The hoped-for effect was that different operand representatives might move the componentwise scale-invariant tensor/quantization into a lower-noise region.

## Registered decisive test

QUESTION: Can reciprocal public-unit preconditioning preserve the B175 plaintext product while creating a source-backed tensor/reference contraction of at least the approximately 16 required bits missing at the pointwise gate?

CURRENT_BELIEF: Scalar multiplication is componentwise and leaves BGV scale metadata unchanged. Therefore the degree-two tensor should collapse to a single global scalar K=lambda*mu times the original tensor. For nontrivial centered reciprocal pairs, K is an integer congruent to 1 mod T but has magnitude at least T-1=2^16, so there is no balancing effect.

CHEAPEST_DECISIVE_TEST: Inspect exact Lattigo scalar-multiply semantics; derive the three tensor components after reciprocal preconditioning; prove the exact arithmetic lower bound on nontrivial centered reciprocal products for T=65537; compare no-wrap and wrap regimes with the durable B175 quantization-cell boundary. No native execution unless a deterministic contraction invariant survives.

IF_PASS: If a nontrivial reciprocal pair produces a genuine source-backed contraction, admit ACTIVE and run one matched B175 scalar-preconditioned correctness/noise canary.

IF_FAIL: If every nontrivial pair is exactly a global tensor scalar with no deterministic norm contraction and no-wrap behavior worsens by at least 16 bits, PARK immediately.

IF_UNCLEAR: If only instance-specific modular-wrap tuning remains, do not promote; classify that as low-value quantization-cell tuning rather than a new paper mechanism.

WHICH_PAPER_GATE_CHANGES: Killer gate (1) exact semantic oracle and killer gate (3) optimistic value/noise ceiling.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: This is essentially zero key cost and negligible public-linear cost. If even this cheapest same-ring preconditioner has no contraction invariant, native exploration of scalar tuning is not paper-level research.

## Killer gate (1): exact semantics and source

Lattigo v6.2.0 source:
  schemes/bgv/evaluator.go
  blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.

For scalar `*big.Int` multiplication, the evaluator:
1. reduces the scalar modulo T;
2. chooses its centered representative by subtracting T when above T/2;
3. multiplies every ciphertext component by that centered integer in RingQ;
4. does not modify the ciphertext metadata scale.

Thus for lambda*mu=1 mod T, the decoded plaintext product of lambda*L and mu*G is the original plaintext product modulo T.

Semantic gate: PASS.

## Exact tensor-collapse theorem

Write
  L=(l0,l1),
  G=(g0,g1).

The ordinary raw degree-two tensor components before SI quantization are
  u0=l0*g0,
  u1=l0*g1+l1*g0,
  u2=l1*g1.

After scalar preconditioning:
  u0'=(lambda*l0)(mu*g0)=K*u0,
  u1'=(lambda*l0)(mu*g1)+(lambda*l1)(mu*g0)=K*u1,
  u2'=(lambda*l1)(mu*g1)=K*u2,
where
  K=lambda*mu
as an integer product of the centered scalar representatives.

Therefore reciprocal scalar preconditioning does NOT independently rebalance the tensor components. It applies one common scalar K to the complete degree-two tensor before the componentwise SI quantizer.

## Exact reciprocal arithmetic at T=65537

Let lambda,mu be centered nonzero representatives in [-32768,32768] with
  lambda*mu = 1 mod 65537.

Then for some integer k,
  lambda*mu = 1 + k*65537.

If k=0 then lambda*mu=1. Since lambda and mu are integers, the only centered pairs are
  (lambda,mu)=(1,1) or (-1,-1).
Both are tensor-trivial because K=1.

If k is nonzero, then
  |K| = |1+k*65537| >= 65536 = 2^16.

Hence every nontrivial reciprocal pair globally scales every raw tensor component by at least 2^16 in absolute integer magnitude before reduction modulo Q.

The minimax bound follows immediately:
  max(|lambda|,|mu|) >= sqrt(|lambda*mu|) >= 256.

It is tight, achieved by (256,-256) and (-256,256), for which K=-65536.

## No-wrap regime

For any coefficient whose centered raw tensor value u satisfies
  |u| < Q/(2*|K|),
the centered product does not wrap modulo Q and
  cent_Q(K*u)=K*u.

Therefore the raw component magnitude is multiplied by |K|. For every nontrivial reciprocal pair this is at least 2^16.

Under the same local quantization cell, the preconditioner cannot provide the desired 16-bit recovery; it moves in the opposite direction by at least 16 bits before any rounding benefit.

This is a local exact statement, not a claim that every B175 tensor coefficient is in the no-wrap regime.

## Wrap regime

If K*u crosses centered Q boundaries, the map is
  u -> cent_Q(K*u).

For gcd(K,Q)=1 this is an invertible permutation of the residue ring; even without assuming invertibility, the source provides no monotone norm contraction.

Thus modular wrap can make some particular coefficients smaller and others larger, but there is no deterministic worst-case or all-input contraction.

Durable B175 finding
  findings/boot-B175-quantization-cell-robustness-2026-10-29.md
already establishes that SI success/failure can change across componentwise centered-quotient cells and that such cell effects do not transfer to a useful B175 DFR without actual component states.

Therefore the only possible surviving effect of nontrivial reciprocal scalar preconditioning is instance-specific quantization-cell tuning.

## Optimistic value ceiling

Public scalar multiplication itself is cheap and requires no new keys. However:
- K=1 gives only the trivial pairs (1,1) and (-1,-1), with exactly the original tensor;
- every nontrivial pair applies a global |K|>=2^16 tensor multiplier;
- there is no relative component rebalance;
- no-wrap behavior worsens the raw geometry by at least 16 bits;
- wrap-based improvement has no correctness/DFR invariant and is only instance-specific cell search.

A fixed scalar that happens to repair one B175 deterministic source point would therefore be an engineering/quantization-cell tuning result, not a complete B158 correctness mechanism. It cannot satisfy the paper-first requirement for the legal phase domain or useful DFR.

Value gate: FAIL for a paper candidate.

## Closest prior-art boundary

The closest source-level primitive is ordinary public scalar/plaintext multiplication in BGV/BFV, which scales ciphertext error with the plaintext multiplier. The candidate delta is only the paired reciprocal-unit scheduling around a later ciphertext product.

A bounded search did not identify a direct prior-art claim using reciprocal BGV/BFV plaintext units specifically to contract scale-invariant tensor geometry. Novelty is nevertheless not promoted because the construction fails the mechanism/value gate.

## Decision

FAIL_GLOBAL_SCALAR_COLLAPSE / FAIL_VALUE_CEILING -> PARKED.

Candidate:
  boot-b158-reciprocal-unit-preconditioning-v1.

Reciprocal scalar preconditioning preserves the plaintext product but collapses exactly to a single global tensor multiplier K. The only tensor-neutral K is 1, which gives the trivial +/-1 pairs. Every nontrivial centered reciprocal pair has |K|>=2^16 and provides no deterministic contraction.

No native experiment is justified.

## Reopen condition

Reopen only with a genuinely non-scalar public preconditioner that changes relative tensor-component or coefficient geometry while remaining invertible on the plaintext semantics, together with:
1. an exact whole-output correctness relation;
2. a source-backed deterministic or useful probabilistic contraction of at least the needed B175 fixed-Q margin;
3. complete carry/quantization analysis and DFR;
4. public-linear/key/runtime cost;
5. novelty/value beyond instance-specific quantization-cell tuning.

Trying more reciprocal scalars, choosing a scalar from one deterministic B175 trace, or relying on modular-wrap luck does not satisfy this condition.

## Eliminated uncertainty

Eliminated:
Can free reciprocal scalar preconditioning rebalance the B175 operands and reduce the pointwise SI tensor noise?

Answer:
No. It does not rebalance the tensor at all: all three raw tensor components are multiplied by the same K=lambda*mu. Nontrivial plaintext-reciprocal centered pairs have |K|>=65536, while K=1 is exactly the trivial original tensor.

## Evidence references

- findings/boot-B175-quantization-cell-robustness-2026-10-29.md; blob e869da4a9c2cab397b9aab5d4b2850a7059561a3.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; blob c75aa60e080b28b688de7ee8859c5df4d1951c02.
- Lattigo v6.2.0 schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.