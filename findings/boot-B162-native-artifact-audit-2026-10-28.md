# BOOT-B162 — independent native artifact audit

Date: 2026-10-28
TRACK_ID: BOOT
Artifact: BOOT-B162-B158-CORRECTED-ROWKEY-NATIVE-20261028.zip
SHA-256: 5805fab3d00b8a5df804ad6d38418d8b9ee1a8e8a7550518167a072a483195ae

## Integrity

Independent audit:
- outer ZIP SHA-256 matches
- all entries in SHA256SUMS verify
- source, B161->B162 diff, key plan, raw logs, stage noise, rotation noise,
  operation counts, eval-key sizes, environment and pinned modules are present

## Corrected RowRotation key

B158 row Galois key:
- generated at L18
- first actual B158 use at L17

Evaluation-key size:
- old total: 767,060,320 bytes = 731.53 MiB
- new total: 823,685,344 bytes = 785.53 MiB
- increase: 56,625,024 bytes = 54.00 MiB

## Rotation sanity result

The corrected key fully resolves the B159-B161 rotation bug.

S2:
- level L17
- 0/32768 mismatches
- noise budget 560 bits

RowRotation(S2):
- 0/32768 mismatches
- noise budget 560 bits

All 9 RowRotations actually reached before the final stop are exact.
The rotation-noise trace shows identical before/after required-logQ and
noise budget at every tested rotation through k=512.

Therefore:
- B159-B161 k=4 failures were indeed invalid artifacts of the L2 row key.
- B162 establishes valid high-level rotations for B158.

## Genuine B162 native failure

B162 keeps the B161 hybrid schedule:

    selector ct-pt Mul + Rescale
    factor assembly
    MulRelinScaleInvariantNew
    no fused ct-ct Rescale

It is correct through k=512.

Stage trace:

k=1:    logQ 615, required 25,  budget 590
k=2:    logQ 615, required 55,  budget 560
k=4:    logQ 581, required 84,  budget 497
k=8:    logQ 547, required 114, budget 433
k=16:   logQ 513, required 145, budget 368
k=32:   logQ 479, required 175, budget 304
k=64:   logQ 445, required 204, budget 241
k=128:  logQ 411, required 235, budget 176
k=256:  logQ 377, required 265, budget 112
k=512:  logQ 343, required 295, budget 48
k=1024: logQ 309, required 325, budget -16; 32768/32768 mismatches

Actual before stop:
- ct-ct = 10 / 15
- RowRotation = 9 / 14
- selector rescale = 20 / 31

Thus:
- B162_STATUS = FAIL_NATIVE_NOISE_AFTER_KEY_FIX
- this is the first valid native B158 noise failure

## Root-cause shape

For k>=4:
- required-logQ grows only about 29-31 bits per doubling
- available logQ falls by about 34 bits per doubling because selector Rescale
  consumes one Q prime
- hence total noise budget falls about 63-65 bits per doubling

The failure is therefore not caused by RowRotation and is not an abrupt
selector catastrophe.

It is a systematic level/noise-budget mismatch of the B161 hybrid schedule:

    +~30 bits required noise headroom per doubling
    -~34 bits modulus per doubling

This predicts the observed nearly linear budget decline.

## Important consequence

B162 does NOT invalidate every B158 multiplication schedule.

The corrected high-level row key has NOT yet been combined with the B160
schedule:

    scale-one/no-rescale selectors
    + MulRelinScaleInvariantNew
    + no selector Rescale
    + no fused ct-ct Rescale

The original B160 k=4 failure occurred before selector multiplication because
of the under-leveled L2 row key and is therefore invalid.

That corrected-B160 schedule is especially important because it does not
consume one Q prime per B158 doubling.

Therefore B158 practical feasibility remains unresolved until that schedule is
tested with the corrected L18 row key.

## Current state

B158_ALGEBRA = PASS
B158_CTCT_OPTIMALITY = PASS
B159-B161_K4_FAILURES = INVALIDATED_BY_KEY_LEVEL_BUG
B162_B161_HYBRID = VALID_FAIL_AT_K1024
B158_PRACTICAL_LINE = NOT_YET_PARKED
NEXT = B163_CORRECTED_B160_NO_RESCALE_SCALE_INVARIANT_GATE
