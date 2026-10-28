# BOOT-B163 — corrected B160 no-rescale scale-invariant native gate

Date: 2026-10-28
TRACK_ID: BOOT
Status: NATIVE_GATE_NOT_RUN

## Motivation

B160 intended to test:

    no-rescale selector masks
    + scale-invariant fused ct-ct multiplication
    + no fused ct-ct rescale

but its k=4 failure was invalid because the new B158 RowRotation reused an L2
Galois key on an L17 ciphertext.

B162 fixed the RowRotation key and proved all reached rotations exact.

B162 then tested a DIFFERENT schedule (B161 hybrid):

    selector Rescale every round
    + scale-invariant fused ct-ct

and genuinely failed at k=1024 because each doubling simultaneously:
- raises required-logQ by ~30 bits
- drops Q by ~34 bits

Thus the untested schedule with the highest remaining value is corrected B160.

## B163 exact question

With:
- correct L18 B158 RowRotation key
- the same B158 recurrence
- the same source/security parameters

can:

    scale-one/no-rescale selectors
    + MulRelinScaleInvariantNew
    + no explicit Rescale in the B158 recurrence

complete all 15 doublings?

## Why it may differ materially

In B162 the required-logQ grows only ~30 bits per doubling.
The catastrophic budget slope comes mainly from also consuming a ~34-bit prime
every round.

B163 keeps the full L18 Q modulus during the recurrence, so it removes that
systematic 34-bit-per-round loss.

The old B160 result cannot answer this because the first high-level rotation
was invalid.

## Native gate

Start from the B160 arithmetic schedule but import ONLY the B162 key-plan fix:
- add B158 RowRotation at L18 before key generation
- assert row-key level >= first use

Do not import B161 selector Rescale.

For deterministic x=1:
- check every RowRotation before/after
- check every selector output
- check every fused multiplication
- record required-logQ/noise budget at k=1,2,4,...,32768

Stop at first mismatch or non-positive budget.

No performance benchmark unless the complete basis is correct.

## Decision

If corrected B163 fails very early with a monotone required-logQ slope that
cannot fit within L18/649 bits by k=32768:
- PARK B158 practical line unless a new algebraic/noise mechanism appears.

If B163 reaches substantially farther but fails near the end:
- inspect whether one/few strategically placed Rescales can rescue it;
- do NOT immediately add Q primes.

If B163 completes:
- run matched BuildBasis performance gate
- then revisit full pipeline and one-prime reduction.

Do not auto-run Codex.
