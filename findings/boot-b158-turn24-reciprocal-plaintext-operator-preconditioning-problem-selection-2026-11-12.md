# BOOT / B158_OVERALL — Research Turn 24/25
## PROBLEM_SELECTION — reciprocal plaintext-operator preconditioning

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-reciprocal-plaintext-operator-preconditioning-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 24 had ACTIVE=UNKNOWN. This candidate is a genuine non-scalar extension of Turn 23 and therefore directly tests the exact reopen condition left by the reciprocal-scalar result.

Instead of scalar units lambda,mu in Z_T, choose arbitrary public plaintext-ring units U,V in R_T=F_T[X]/(X^N+1) such that U*V=1 in R_T. These may be nonconstant coefficient polynomials / nonuniform slotwise units.

## Candidate mechanism

Let L=LT8 and G=GROUPED be the B175 pointwise operands. Encode U,V as scale-one BGV plaintext operators and compute
  L' = U * L,
  G' = V * G,
then execute the unchanged MulRelinScaleInvariant(L',G').

Because U*V=1 in the plaintext ring, the decoded plaintext product is unchanged. The hoped-for mechanism was that non-scalar convolution by U and V could reshape coefficient geometry before the failing SI tensor.

## Registered decisive test

QUESTION: Can arbitrary non-scalar public plaintext-ring units U,V with U*V=1 preserve B175 plaintext semantics while giving a source-backed coefficient/tensor contraction of at least the approximately 16 required bits missing at the pointwise gate?

CURRENT_BELIEF: Stock BGV plaintext multiplication applies the same Q-lifted plaintext operator to every ciphertext component. Bilinearity should therefore collapse the two-sided preconditioner to one common convolution H=U_tilde*V_tilde acting identically on all three raw tensor components. Since H reduces to 1 modulo T, any nontrivial integer lift is H=1+T*K and necessarily has a coefficient of magnitude at least T-1=2^16. This gives no component-relative balancing or universal contraction.

CHEAPEST_DECISIVE_TEST: Use exact Lattigo v6.2.0 Encoder.RingT2Q and tensorStandard source to derive the effective Q-ring plaintext operator; prove that all three raw tensor components are multiplied by the same H; prove the integer lift relation H=1+T*K and its minimum nontrivial coefficient magnitude; then test whether any key/input-universal contraction invariant survives. No native execution unless it does.

IF_PASS: If a nontrivial U,V pair yields a source-backed common-operator contraction of at least the required fixed-Q margin across the B175 legal domain, admit ACTIVE and run one matched native canary.

IF_FAIL: If every reciprocal pair reduces to a fixed common convolution H with no universal contraction and any possible benefit depends only on actual component cancellation / modular quantization cells, PARK.

IF_UNCLEAR: If only B175-instance-specific cancellation remains unresolved because raw tensor components are not persisted, do not native-search it; classify it as instance tuning rather than a paper mechanism.

WHICH_PAPER_GATE_CHANGES: Killer gate (1) exact semantic oracle and killer gate (3) optimistic end-to-end value/noise ceiling.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: This is the cheapest and broadest same-ring non-scalar public preconditioner after Turn 23. If it still collapses to one common operator without a contraction invariant, no low-cost public invertible preconditioning survivor remains in this class.

## Source semantics

Primary source:
  tuneinsight/lattigo v6.2.0
  schemes/bgv/encoder.go, blob db146d55271b67f868a53fca94ebf7a6d3a01974
  schemes/bgv/evaluator.go, blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.

For batched scale-one plaintext encoding, Encoder.Encode calls EmbedScale with scaleUp=true. RingT2Q copies the RingT coefficient polynomial into each Q limb and multiplies by T^{-1} mod Q.

When MulScaleInvariant receives a plaintext/vector operand, it creates a scale-one plaintext and dispatches to tensorStandard. tensorStandard multiplies that plaintext component by T before component multiplication.

Therefore the T^{-1} encoding factor and the tensorStandard T factor cancel. The effective public operator on each ciphertext component is exactly the canonical RingT coefficient polynomial lifted into R_Q.

Thus no extra BGV scale metadata change or hidden operator is available to the candidate.

## Exact tensor-collapse theorem

Let the effective lifted public operators be U_tilde,V_tilde in R_Q and write
  L=(l0,l1), G=(g0,g1).

After plaintext multiplication:
  L'=(U_tilde*l0, U_tilde*l1),
  G'=(V_tilde*g0, V_tilde*g1).

The three raw degree-two tensor components before SI quantization are then
  u0' = (U_tilde*V_tilde) * l0*g0,
  u1' = (U_tilde*V_tilde) * (l0*g1+l1*g0),
  u2' = (U_tilde*V_tilde) * l1*g1.

Define
  H := U_tilde*V_tilde.

Then
  (u0',u1',u2') = H * (u0,u1,u2).

So arbitrary reciprocal public plaintext operators do NOT independently rebalance the three tensor components. They apply one identical public convolution operator H to the complete raw tensor.

## Exact integer-lift relation H = 1 + T*K

At the fixed B175 parameters:
  N=32768,
  T=65537,
  log2 Q approximately 649.

RingT2Q uses canonical coefficients in [0,T-1]. For any U_tilde,V_tilde produced this way, every coefficient of their integer negacyclic product has magnitude at most
  N*(T-1)^2 = 2^47,
which is astronomically smaller than Q/2.

Therefore the centered R_Q product H is represented by the same ordinary integer negacyclic product; there is no hidden modulo-Q ambiguity in the public-operator product itself.

Because U*V=1 in R_T, coefficientwise modulo T:
  H_0 = 1 mod T,
  H_i = 0 mod T for i != 0.

Hence over the integer negacyclic ring
  H = 1 + T*K
for an integer polynomial K.

If H=1, the raw tensor is exactly the original raw tensor and the preconditioner is representation-trivial.

If H is nontrivial, then either:
- the constant coefficient is 1+kT with k nonzero, whose minimum absolute value is T-1=65536; or
- a nonconstant coefficient equals kT with k nonzero, whose absolute value is at least T=65537.

Therefore every nontrivial reciprocal plaintext-operator pair satisfies
  ||H||_infinity >= T-1 = 65536 = 2^16.

## No universal contraction

For a monomial ring vector X^j, multiplication by H is a signed cyclic shift of H. Thus
  ||H*X^j||_infinity = ||H||_infinity.

For every nontrivial H this is at least 2^16, whereas ||X^j||_infinity=1.

So no nontrivial H from this reciprocal-plaintext class is a contraction on all ring inputs. The candidate therefore has no key/input-universal coefficient-norm contraction theorem.

This statement is about the public convolution operator. It does not assert that an actual B175 tensor component cannot happen to cancel against H on one fixed execution.

## B175-specific boundary

The actual B175 artifact does not persist the complete pre-quantization tensor components u0,u1,u2. Durable source-level work explicitly identified those component lifts as missing evidence for fine attribution.

Therefore one cannot rule out accidental instance-specific cancellation for some H on the fixed CASE_1 trace without new native instrumentation.

But such cancellation would not establish a complete mechanism:
- H is fixed and applies identically to all three tensor components;
- there is no all-input or legal-domain contraction invariant;
- H=1 is exactly trivial;
- H!=1 contains a coefficient of magnitude at least 2^16;
- any improvement can only come from input-specific convolution cancellation and/or movement across centered-Q / SI quantization cells.

Durable B175 quantization-cell analysis already classifies such cell-sensitive behavior as non-transferable without actual component states and a DFR argument.

Therefore a native search over public reciprocal plaintext units would test engineering instance tuning, not a paper-level construction.

## Optimistic value ceiling

The public plaintext multiplications themselves require no new evaluation keys and are relatively cheap compared with ciphertext-ciphertext multiplication.

However the candidate offers no deterministic reduction in:
- ciphertext-ciphertext count;
- relinearization count;
- rotation count;
- modulus level;
- ring dimension;
- secret norm;
- dominant aggregate tensor/reference error.

Its only possible benefit is input-specific cancellation under a common H. Without a correctness/DFR invariant this has no positive paper-level end-to-end value ceiling.

## Prior-art boundary

A bounded literature search surfaced standard BGV/BFV plaintext multiplication and multiplication-noise analyses, but no direct claim matching reciprocal non-scalar plaintext-unit preconditioning as a general SI-noise contraction method.

This is not a novelty clearance. Novelty remains PREFLIGHT and is not advanced because the mechanism fails before admission.

## Decision

FAIL_COMMON_OPERATOR_COLLAPSE / FAIL_VALUE_CEILING -> PARKED.

Candidate:
  boot-b158-reciprocal-plaintext-operator-preconditioning-v1.

NO_CREDIBLE_NEW_MECHANISM remains after the exact common-operator reduction.

No native execution is justified.

## Reopen condition

Reopen only with a public preconditioner that does NOT reduce to one common plaintext convolution H on all raw tensor components, or with a source-backed proof that a specific nontrivial H contracts the entire legal B175 tensor family by at least the needed fixed-Q margin.

Any reopening must include:
1. exact whole-output plaintext relation;
2. complete Q-lift/carry/quantization analysis;
3. deterministic or useful probabilistic contraction / DFR over the legal B175 domain;
4. public-linear/key/runtime cost;
5. publication value beyond fixed-instance cancellation.

Searching more reciprocal plaintext units on one native trace, relying on accidental coefficient cancellation, or exploiting one favorable quantization cell does not satisfy this condition.

## Eliminated uncertainty

Eliminated:
Can non-scalar reciprocal plaintext-ring units evade the Turn-23 scalar-collapse obstruction by separately reshaping LT8 and GROUPED?

Answer:
No at the raw-tensor interface. Stock BGV plaintext multiplication makes both sides collapse to the same common operator H=U_tilde*V_tilde on all three tensor components. Because H=1+T*K and nontrivial H has ||H||_infinity>=2^16, the construction has no universal contraction invariant; only instance-specific cancellation remains.

## Evidence references

- findings/boot-b158-turn23-reciprocal-unit-preconditioning-problem-selection-2026-11-12.md; blob ab3e97b5cc7ad95541bc4febeedf941b0afdb2e6.
- findings/boot-B175-public-mask-operator-kernel-screen-2026-10-29.md; blob 36798b49f9cbfacf05e303943d559e166aef774b.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; blob c75aa60e080b28b688de7ee8859c5df4d1951c02.
- findings/boot-B175-quantization-cell-robustness-2026-10-29.md; blob e869da4a9c2cab397b9aab5d4b2850a7059561a3.
- Lattigo v6.2.0 schemes/bgv/encoder.go blob db146d55271b67f868a53fca94ebf7a6d3a01974.
- Lattigo v6.2.0 schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.