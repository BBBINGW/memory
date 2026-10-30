# BOOT — ePrint 2026/2119 two-root shared-leaf noise/covariance gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 6/25

Status:
PASS_STATIC_SHARED_LEAF_NOISE_GATE /
PASS_DETERMINISTIC_ENVELOPE_NO_WORSENING /
PASS_IDEAL_SLOT_SHARED_ROOT_COVARIANCE_ANNIHILATION /
PASS_SECURITY_MONOTONICITY /
FINITE_CKKS_MASK_LEAKAGE_AND_NATIVE_PRECISION_UNVERIFIED /
NATIVE_SETUP_GATE_REACHED

## Parent result restored

Parent finding:
findings/boot-2119-two-root-selector-packing-gate-2026-10-30.md
commit 2ee6820a81726483b9fdef5f39b7d3c33dabc14b
blob f5ac1ad086e3d35ed9c8331ab9d816246af441f1

Parent result:
- current supplied 2026/2119 Section 6 packs four coefficient-selector roots;
- post-narrow private selector information can be factored into only the two candidate/sign bit families b^+, b^-;
- two packed roots suffice functionally;
- root storage 4 -> 2;
- one-time coefficient-decompression substitutions 4(N-1) -> 2(N-1);
- online evaluation-ready key and 8.2 ms / 4.6 ms path unchanged;
- unresolved gate was noise/covariance when head and tail reuse the same decompressed indicator leaves.

## Primary source

Rending Ouyang et al.,
"CKKS Bootstrapping in less than 10ms", ePrint 2026/2119.

Supplied durable source:
papers/supplied/2026-2119.pdf
Git blob SHA 5de485db8242148144f74de0c857cfcd698f0f35
35 physical pages.

Relevant source:
- pp10-12: head/tail layouts and Theorem 3.1;
- pp13-16: complex packing of positive/negative selector bits;
- pp18-20: coefficient packing, binary decompression, public reconstruction of head/tail selectors;
- pp22-27: implementation/performance; reconstructed blind-rotation keys resident on GPU; setup reconstruction excluded from timing.

Current official ePrint byte parity was not freshly authenticated in this turn.

## ONE primary hypothesis

Reusing the same decompressed positive/negative indicator leaves to derive both head and tail selectors introduces harmful correlated selector noise that invalidates the two-root optimization before native evaluation.

Cheapest decisive test:
trace only the shared-root error provenance through the source narrow dataflow and determine whether one output slot can receive two copies of the same shared-root error. Separately check deterministic norm bounds, which do not rely on stochastic independence.

No native benchmark and no new key format beyond the Turn-5 two-root construction.

## 1. Source disjoint-support projectors

Source head computation uses

    beta' = Ecdslot([omega^{b_0},...,omega^{b_{n-g}}] || 0_{g-1})

and produces gamma' with intended support only on

    I_head = {0,...,n-g}.

Source tail computation uses

    beta'' = Ecdslot(0_{n-g+1} || [omega^{b_{n-g+1}},...,omega^{b_{n-1}}])

and produces gamma'' with intended support only on

    I_tail = {n-g+1,...,n-1}.

Thus at the ideal slot-vector level,

    beta'_i * beta''_i = 0    for every i.

Theorem 3.1 combines

    gamma_narrow = gamma' + gamma''.

The head/tail plaintext supports form a partition.

## 2. Shared-leaf model

Let L_j^+ and L_j^- be the decompressed indicator ciphertext leaves from the proposed two-root key.

Write their slot decryptions as

    L_j^+ = b_j^+ * 1 + e_j^+,
    L_j^- = b_j^- * 1 + e_j^-,

where e_j^+, e_j^- collect root-encryption noise plus all substitution-tree key-switching noise already present after coefficient decompression.

The current four-root construction would give separate copies

    L_{H,j}^±, L_{T,j}^±

with the same intended bit and comparable marginal noise, but distinct encryption/decompression randomness.

The two-root construction instead applies public linear maps to the same L_j^±.

## 3. Selector reconstruction does not amplify the leaf error norm

Head selector reconstruction multiplies the replicated bit leaves by the public head mask and then complex-packs the positive/negative indicators.

Tail selector reconstruction applies the public packed-tail placement masks and then the same complex packing.

At the intended slot-vector level these public masks contain only 0/1 entries.

Therefore, for slot sup norm,

    ||M * e||_infinity <= ||e||_infinity

for every reconstruction mask M.

Complex packing gives at most the same sqrt(2) / triangle-factor envelope already present in the current Section-4 construction; reuse changes correlation, not a per-branch norm.

Thus every deterministic per-selector error bound that was valid for an independently reconstructed head or tail selector remains valid for the corresponding shared-leaf-derived selector.

## 4. Exact ideal-slot covariance annihilation

The important point is NOT that the two branches are independent. They are not.

The important source structure is the final disjoint projection.

Write the two branch outputs schematically as

    gamma'_i  = beta'_i  * H_i(E, R_H),
    gamma''_i = beta''_i * T_i(E, R_T),

where:
- E denotes ALL shared indicator-leaf errors;
- R_H and R_T denote branch-local fresh operation/evaluation-key contributions;
- H_i and T_i may be nonlinear because of product trees;
- all pre-beta rotations, conjugations and products are included inside H_i/T_i.

For every slot i, either beta'_i=0 or beta''_i=0 at the ideal semantic level.

Therefore the part of the final error depending on the shared E satisfies, pointwise,

    shared_error_i
      = beta'_i * H_i(E) + beta''_i * T_i(E),

with at most ONE nonzero coefficient.

Consequently, for any random model on E,

    Cov(shared_head_i, shared_tail_i) = 0

after the ideal source projector, even though the same E generated both branches.

There is no same-slot doubling of shared-root variance.

This argument does not require independence among coefficient-decompression key-switch noises.

## 5. Why product-tree / tail rotations do not invalidate the static gate

The tail source explicitly allows intermediate packed ciphertexts to contain nonzero values outside the ultimate tail coordinates. Proposition 3.3 then multiplies by beta'' whose head slots are zero. Likewise beta' has zero tail.

Therefore rotations or nonlinear product-tree computations before the final beta multiplication do not matter for the shared-root covariance question: their root-derived contribution is projected out on the opposite output region.

Fresh relinearization/key-switch errors generated AFTER/BETWEEN those computations may remain on nominal-zero message slots, but those errors are branch-local operation errors, not duplicated shared-root errors created by the two-root reuse.

Moreover, source key-switch/evaluation-key errors are themselves reused/fixed across operations, so the original four-root construction does not justify a blanket branch-independence assumption either.

## 6. Deterministic correctness envelopes are exactly correlation-insensitive

Suppose a correctness analysis only knows absolute bounds

    |E_H,i| <= B_H,i,
    |E_T,i| <= B_T,i.

Then for the final sum,

    |E_H,i + E_T,i| <= B_H,i + B_T,i

regardless of whether the variables are independent, positively correlated, negatively correlated, or identical.

The two-root rewrite does not increase either branch's marginal deterministic bound, because the public reconstruction maps are unchanged and contractive in the ideal slot mask model.

Therefore ANY source-style deterministic infinity-norm correctness certificate based on triangle/submultiplicative inequalities is not worsened by changing independent duplicate roots into a reused root.

This is stronger and safer than asserting Gaussian independence.

## 7. Finite CKKS plaintext-encoding leakage

The source writes Ecdslot of zero-one masks and beta vectors as ideal slot values.

In an actual CKKS implementation, coefficient rounding means a plaintext whose intended slot value is zero can decode to a small nonzero residual.

Let epsilon_mask bound the off-support decoded magnitude of a public projector.

Then a shared leaf can leak into the inactive branch with coefficient at most epsilon_mask.

For one shared scalar error contribution E, a simple covariance correction has magnitude bounded by

    2 * epsilon_mask * (1 + epsilon_mask) * Var(E)

relative to ideal unit-active / zero-inactive coefficients.

More generally, Cauchy-Schwarz gives

    |2 Cov(E_H,E_T)|
      <= 2 sqrt(Var(E_H) Var(E_T)),

and the inactive shared-root variance is second order in the off-support mask amplitude.

This does NOT establish a concrete negligible correction because the supplied paper does not give the exact serialized public-mask scaling / rounding residual needed for a source-parameter numerical bound.

Important: this finite-encoding leakage exists in the current four-root implementation too. The new issue is covariance of that leakage, not the existence of leakage.

## 8. Security monotonicity

Under the Turn-5 established identity of the private indicator families, the current four-root key publishes independent encryptions of duplicated selector-bit information.

The two-root public key view is obtained by:
1. retaining one positive root and one negative root;
2. discarding the duplicate roots;
3. deriving head/tail layouts through public deterministic homomorphic maps.

Any adversary against the two-root view can therefore be simulated from the four-root view by discarding the extra ciphertexts and applying the same public derivation.

Hence the rewrite does not require a NEW secret-dependent plaintext/KDM function.

Subject to the security of the original published key format, publishing fewer duplicate encryptions is security-monotone in this narrow sense.

This is not a fresh complete circular-security theorem for 2026/2119.

## 9. Verdict

Primary hypothesis "shared-leaf correlation statically kills two-root packing" FAILS.

PASS:
- public selector reconstruction keeps the same per-branch deterministic noise envelope;
- ideal head/tail projectors annihilate shared-root same-slot covariance exactly;
- deterministic correctness bounds are correlation-insensitive;
- no new KDM plaintext family is introduced; security view is a public post-processing/subview of duplicated information.

UNCLEAR:
- concrete finite-precision CKKS mask leakage covariance;
- actual output max-error/precision distribution;
- native setup reconstruction correctness and timing;
- total serialized key bytes including substitution keys;
- novelty versus compressed-query/key-packing literature.

## 10. Research decision

The two-root candidate survives the cheapest static noise/security gate.

There is now no remaining static algebra/type/noise blocker that justifies killing it.

The next decisive step should be ONE native/source-compatible setup experiment or author-code audit measuring:
- exact reconstructed selector parity versus four-root baseline;
- output precision parity over a bounded fixed parameter case;
- root-key serialized bytes;
- one-time reconstruction latency;
- peak setup memory.

Do NOT interpret a setup win as an improvement to the published 8.2 ms online bootstrapping latency, because Section 8 explicitly excludes reconstruction and keeps the evaluation-ready key resident.

No Codex/native execution was launched in this turn.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_CODEX_TASKS: none.
