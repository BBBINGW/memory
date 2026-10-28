# BOOT-B158 — prior-art audit closure after connection recovery

Date: 2026-10-28
TRACK_ID: BOOT
Parent: boot-B158-formal-recurrence-optimality-prior-art-2026-10-28.md

No Codex/native execution was launched.

## 2026/1401 blocker resolved at abstract scope

The official IACR ePrint page for 2026/1401 is accessible and its abstract was
verified directly.

Its stated problem is TFHE multivariate functional bootstrapping / LUT
compression:
- variable separation,
- additive inner representations,
- logarithmic decomposition for division with remainder,
- rounded logarithms,
- modular reduction / truncated division,
- universal representation f(x_1,...,x_l)=q(sum_i p_i(x_i)),
- search for small-span representations.

This is not the sparse-BFV consecutive-power generation problem of 2026/975.

Therefore:
- 2026/1401 is NOT a direct collision with B158 from its official stated scope.
- The earlier concern that it might be a direct follow-up optimizing the 975
  EvalPower recurrence is substantially reduced.

A full-text audit is still desirable before a publication-level novelty claim,
but 1401 is no longer a blocker for continuing B158.

## Closest conceptual prior

IBM patent family:
"Fast polynomial evaluation under fully homomorphic encryption by products of
differences from roots using rotations"
- priority/filed: 2024-03-13
- application publication: 2025-09-18
- US patent grant: 2026-02-24

It uses:
- duplicated SIMD input values,
- free/unused slots,
- rotation of an intermediate ciphertext,
- multiplication by the rotated ciphertext,
- merging different-degree polynomial jobs into unused slots.

This is important prior art for the broad idea:
"use spare SIMD slots plus rotation/multiplication to reduce nonlinear work."

However, its invariant/output is different:
- it reduces root factors to one polynomial value;
- it does not output the consecutive basis 1,x,...,x^(r-1);
- it does not co-pack [growing power basis | current binary power];
- it does not fuse accumulator extension with x^(2^i)->x^(2^(i+1)) in one
  multiplication.

Therefore:
- BROAD_SIMD_ROTATE_MULTIPLY_NOVELTY: REJECTED
- B158_SPECIFIC_STATE_INVARIANT: NO_DIRECT_COLLISION_FOUND

## Refined B158 claim

The narrow claim that remains defensible is:

"An optimal ciphertext-ciphertext-multiplication generator for the sparse-BFV
consecutive power basis, obtained by co-packing the growing basis accumulator
and the current binary power in the two BFV hypercube halves, so that each
ciphertext multiplication simultaneously extends the basis and advances the
binary-power chain."

For r=2^ell, ell>=2:
- ct-ct Mult = ell
- RowRotation = ell-1
- the first k=1 doubling uses the original duplicated input and needs no
  RowRotation
- ct-ct Mult count is optimal under the ordinary arithmetic-SIMD model because
  the output contains x^(r-1), forcing multiplicative depth >= ell.

For r=32768:
- original 2026/975 EvalPower: 28 ct-ct Mult
- B158: 15 ct-ct Mult + 14 RowRotation
- ct-ct Mult reduction: 46.43%

## Current novelty decision

DIRECT_PRIOR_COLLISION: NOT_FOUND
CLOSE_CONCEPTUAL_PRIOR: YES
2026_1401_DIRECT_COLLISION: NO_FROM_OFFICIAL_SCOPE
NOVELTY: PROMISING_NOT_ESTABLISHED

B158 remains the active BOOT fresh candidate.

Do not launch native/Codex automatically.
