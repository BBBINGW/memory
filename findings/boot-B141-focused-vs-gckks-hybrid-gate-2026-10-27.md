# BOOT-B141 — Focused-CKKS tree vs GCKKS joint cleaning hybrid gate

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Sources:
  - supplied ePrint 2026/2531 revision, "High-Precision CKKS with Focal Units"
  - supplied ePrint 2026/2600, "High-precision Bootstrapping for GCKKS"
- Status: COMPLETE
- Decision: FAIL_PARTIAL_SHARE_TWO_LEVEL_HYBRID / REPRESENTATION_LEVEL_TRADEOFF
- CODEX_REQUIRED: NO
- Native benchmark: NOT JUSTIFIED

## Question

2026/2600 shares x^2 and x^3 before splitting, reducing duplicate relinearization/work but using three Delta-scale levels per precision-doubling iteration.

Revised Focused CKKS 2026/2531 uses a tree-like cleaning that splits the precision focus and is described by 2026/2600 as costing two levels per iteration, but it duplicates cleaning on the children.

Can a hybrid share an expensive prefix such as x^2 before splitting, then finish h1(x)=3x^2-2x^3 after the split, retaining both the shared work and the 2-level modulus behavior?

## Exact Focused-tree invariant

Focused CKKS does not require non-focus slots to decrypt near zero during cleaning.

Proposition 16 assumes:
- every slot contains a message in the discrete set D up to error epsilon;
- only focus slots have high precision;
- background slots are allowed to remain within epsilon of D.

The tree-like construction then:
- halves the focus set at each layer;
- for one child it keeps the first half in place;
- for the other child it rotates the other coset onto the new focus set;
- applies the cleaning polynomial to both children.

The background messages remain present and close to D. They are not forced to become fresh-noise-sized zero values at every split.

Later, the partial S2C keeps only the focus slots and discards the leftover background values.

This is why the Focused tree can avoid a per-split diagonal zero mask.

## Exact GCKKS invariant

GCKKS has a stronger/different invariant.

When k increases, source useful slots that leave the target useful set become target **unused** slots. Section 4.3 of 2026/2600 explicitly requires these values to be zeroed before factor conversion; otherwise their normalized magnitude violates the unused-slot bound.

For a discarded source-useful slot eta, direct conversion from factor F^2 to F' gives

|d'(eta)|/|F'(eta)| = |d(eta)|/|F(eta)|^2.

Thus shrinking F'(eta) does not suppress the normalized value.

A discrete bit value carried at high CKKS-equivalent scale remains a message-sized term, not a fresh-noise-sized unused value.

Therefore Focused CKKS's permission to keep approximate D-valued background messages is not available under the current GCKKS unused-slot invariant.

## Partial-share hybrid test

Suppose we:
1. compute x^2 once before splitting;
2. split/mask x^2 into the two child slot sets;
3. compute x^3 for each child as x times the child x^2;
4. finish h1 separately.

The split still needs a high-accuracy diagonal zero mask before the child is reinterpreted under F'.

If a plaintext mask with encoding scale mu approximates zero on a discarded useful slot, its encoding rounding error leaves a residual of order

Delta^2 / mu

at the x^2 scale (up to the decryption-factor/noise constants). To push a message-sized Delta^2 term down to an unused-noise-sized normalized bound, mu itself must carry high precision. This mask cost cannot simply be replaced by a scale-one exact ring multiplier, by the B140 nonvanishing argument.

If the mask is rescaled immediately, the hybrid spends the mask modulus before the child x^3 multiplication. If rescaling is delayed, the mask scale propagates into x^3 and must still be removed later. Either way, the mask precision is not eliminated; delaying it only changes scheduling.

2026/2600's current joint formula is already efficient in this respect: it folds the slot-selection masks into the weighted x^2/x^3 combination and performs one final rescaling rather than paying an independent early mask-rescale.

Hence "share x^2 then split" does not recover the Focused two-level behavior for free.

## Why this is not a contradiction with Focused CKKS

Focused CKKS and GCKKS optimize related precision/slot tradeoffs under different representations:

- Focused CKKS:
  background **message values may remain**, only their precision is relaxed.

- GCKKS:
  unused slots participate in a magnitude/noise invariant proportional to F; newly unused high-scale message values must be removed.

The Focused tree saves modulus by exploiting the former representation property. GCKKS's joint method pays an extra layer to enforce the latter invariant while sharing nonlinear power computation.

Therefore the 2-vs-3-level difference is not merely an implementation artifact.

## Prior-art position

2026/2600 explicitly identifies revised 2026/2531 as closely related parallel work and already compares:
- split-first / duplicated cleaning / lower level cost;
- delayed split / shared power computation / higher level cost.

So the high-level hybrid tradeoff is already visible to both papers. A contribution would need a genuinely new representation/invariant that changes this frontier, not just a reordering of x^2 and x^3.

## B141 decision

- Reuse Focused tree unchanged inside GCKKS: FAIL, invariant mismatch.
- Share x^2 then split and finish x^3 per child: FAIL to remove the mask/precision cost; at best a schedule change.
- Move the mask earlier: no modulus win and duplicates/propagates scale.
- Current 2026/2600 joint masking is already a natural fusion of selection with h1 coefficients.
- A real 2-level shared-work construction would require changing the representation so discarded slots may legally retain structured messages or finding a new conversion invariant.
- Such a representation change is a substantially different research problem and overlaps the conceptual territory of Focused CKKS.
- CODEX/native: NO.

Overall:
**PARK the local 3->2-level hybrid branch.**

## Next recommendation

Do not continue local reorderings of the split-clean circuit.

The strongest open issue in 2026/2600 is now empirical rather than algebraic: the paper has no implementation, so the practical crossover among:
- Focused CKKS tree cleaning,
- GCKKS joint cleaning,
- Dumezy shaped arithmetic,
is unknown.

But benchmarking that crossover would require a substantial implementation and is not justified as a BOOT contribution without a new algorithmic claim.

Return to fresh bootstrapping scouting rather than start Codex.
