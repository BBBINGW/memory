# BOOT-B140 — GCKKS joint split-and-clean 3-level vs 2-level gate

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Target: ePrint 2026/2600, "High-precision Bootstrapping for GCKKS"
- Supplied PDF: papers/supplied/2026-2600.pdf
- SHA: 8db712155d087284d21e924623496bc48e36eb72
- Status: COMPLETE_SOURCE_AND_ALGEBRA_GATE
- Decision: PASS_BOTTLENECK_TENSION / FAIL_OBVIOUS_3_TO_2_LEVEL_FUSION / IMPLEMENTATION_GATED
- CODEX_REQUIRED: NO

## Source status

The paper is a draft dated 2026-10-22 and explicitly states in Section 6:

"Implementation — Not available yet."

Therefore no native runtime/Amdahl claim is currently justified.

## Relevant construction

The bootstrap uses low-precision overflow extraction followed by iterative precision doubling.

At each precision-doubling iteration:
- input has decryption factor F and useful-slot scale Delta;
- the method computes shared powers x^2 and x^3 before splitting;
- it delays the even/odd split so those power computations and relinearizations are shared;
- each child is produced by plaintext masks selecting alternate useful slots;
- the output is reinterpreted under target factor F' and rescaled.

The paper states this joint GCKKS procedure consumes **three Delta-scale levels per iteration**.

Its parallel-work comparison to revised Focused CKKS says:
- Focused tree: split first, then clean each child separately;
- Focused tree costs **two levels per iteration**;
- GCKKS joint method shares power/relinearization work before splitting but costs **three levels**.

This exposes a genuine computation-vs-modulus-depth tradeoff.

## Cheapest question

Can the paper's joint evaluation retain shared x^2/x^3 work while removing the extra split-mask level, obtaining a 2-level iteration?

## Why the slot-selection mask is structural

When k doubles, half of the source useful slots become target unused slots.

Section 4.3 explicitly requires those soon-to-be-unused useful values to be zeroed **before** changing the decryption factor. Otherwise their normalized unused-slot values remain large and violate the target unused-slot noise invariant.

Indeed, if a source decryption result d under F^2 is simply reinterpreted under F', then at a discarded source-useful embedding eta,

d'(eta) = d(eta) F'(eta)/F(eta)^2,

so after normalizing by the target factor,

|d'(eta)|/|F'(eta)| = |d(eta)|/|F(eta)|^2.

Making F'(eta) small does not help: it cancels from the normalized bound. For a high-precision useful value this remains far above the fresh unused-noise scale.

Therefore the discarded half must be annihilated (up to the controlled rounding/noise error) before or during conversion.

## No depth-free diagonal zero mask from a ring multiplier

A tempting repair is to replace the encoded 0/1 plaintext mask by a monomial/unit/auxiliary decryption-factor multiplier that is "free" in depth.

This cannot implement the required exact diagonal projection.

The plaintext algebra Q[X]/(X^N+1) is a field for power-of-two cyclotomic X^N+1. A nonzero ring element cannot have one canonical embedding equal to zero: if one Galois conjugate is zero, the algebraic element itself is zero, hence all embeddings are zero.

Therefore there is no nonzero plaintext ring element whose canonical values are:
- nonzero on the child useful-slot subset, and
- exactly zero on the discarded source-useful subset.

In particular:
- a monomial has unit-magnitude nonzero values at every embedding;
- the auxiliary H method of Section 4.2 can amplify useful slots without depth, but it cannot serve as an exact 0/1 split mask.

An approximate CKKS/GCKKS slot mask requires encoded nontrivial diagonal values and the corresponding scale/rescale budget.

## Why simple automorphism averaging is not a replacement

Automorphisms permute canonical slots. Linear combinations such as c plus/minus sigma(c) can form sums/differences of paired values, but for arbitrary independent values they do not isolate one original coordinate without an additional diagonal selector.

This matters because the nonlinear cleaning polynomial h1(x)=3x^2-2x^3 must act on the individual approximate bits. Replacing (v_even,v_odd) by mixed sums/differences before cleaning changes the nonlinear function and does not preserve the split-and-clean semantics.

Thus a rotation/automorphism-only butterfly is not an immediate 2-level substitute.

## Other extra level: output-scale mismatch

The paper identifies two extra levels relative to the thrifty CKKS cleaning:
1. GCKKS wants output scale Delta' only slightly above Delta rather than the CKKS output scale Delta^2;
2. the additional slot-mask multiplication.

One could imagine carrying an oversized output scale forward ("lazy" normalization) to defer the first cost. However, that changes the scale/noise invariant used by subsequent GCKKS conversion and unused-slot control, and the current source does not justify it. This remains an unproven scheduling idea, not a passed candidate.

## Complexity context

The precision-doubling phase has log2(k/4) iterations and the paper derives:
- at most about 15k key switchings total;
- O(k) homomorphic operations;
- O((p/k) log k) precision-dependent modulus consumption.

Because the whole point of GCKKS is reduced high-precision modulus consumption, eliminating one of three levels per iteration would be valuable if possible. But the obvious mask-removal route fails structurally.

## B140 decision

- Source/bottleneck tension: PASS.
- Simple shared-power + 2-level split by removing/folding the selector mask: FAIL.
- Depth-free monomial/unit/H mask: FAIL by canonical-embedding nonvanishing.
- Automorphism-only split before nonlinear cleaning: FAIL for arbitrary independent slot values.
- Lazy output-scale normalization: UNCLEAR, would require a new invariant proof.
- Native/value profiling: unavailable because the paper has no implementation.
- CODEX: NO.

Do not claim a universal lower bound that every GCKKS split-and-clean must consume three levels. The negative result applies to the natural current-representation attempts above.

## Next

Read the supplied revised Focused CKKS paper ePrint 2026/2531 and compare its exact 2-level tree split with 2026/2600's 3-level joint method.

The next decisive question is whether a hybrid can share only the expensive prefix (for example x^2/relinearization) before splitting, while moving the remaining nonlinear work after splitting, and still satisfy both target-scale and unused-slot invariants with two levels. If the revised Focused source already contains this tradeoff or if scale algebra still forces a third level, park the branch.
