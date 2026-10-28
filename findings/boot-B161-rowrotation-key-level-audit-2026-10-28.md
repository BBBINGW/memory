# BOOT-B161 — independent artifact audit: high-level RowRotation key mismatch invalidates B159-B161 noise conclusions

Date: 2026-10-28
TRACK_ID: BOOT
Artifact: BOOT-B161-B158-HYBRID-SELECTOR-RESCALE-NATIVE-20261028.zip
Artifact SHA-256: 1778b08e5ec3479dc7d159fa6a424d7d8960875ddcf5524af9cece6a9c42d31e

## Artifact integrity

Independent audit:
- outer ZIP SHA-256 matches
- all SHA256SUMS entries verify
- source, diff, commands, logs, stage-noise, selector-noise, operation counts,
  environment, and pinned modules are present

## Apparent B161 result

The submitted run reported:
- S_2 at L17: exact, 0/32768 mismatches, noise budget 560 bits
- first B158 RowRotation(S_2), before selector multiplication:
  32767/32768 mismatches
  noise budget -16 bits
- unrotated selector branch at the same stage:
  exact before selector
  544-bit budget after selector Mul and after Rescale

Therefore the failure occurs before the rotated selector multiplication.

## Key-plan audit

The evaluation-key summary in the artifact is:

- Relinearization: L18, count 1
- Galois/rotation: L2, count 4
- Galois/rotation: L19, count 11

The B159/B160/B161 co-packed recurrence introduces a NEW RowRotation during
power-basis generation at high levels:

- first B158 RowRotation occurs on S_2 at L17 in B161
- later B158 RowRotations would occur at successively lower levels

However the rotation-key planner was not updated to account for these new
high-level B158 RowRotation uses.

The existing planner still derives RowRotation demand from the source-faithful
2026/975 Algorithm-5 path. In that old path the row-rotation Galois element is
needed only at the low polynomial/ParallelLT/final-sum levels, so the row key
remains in the L2 rotation-key group.

No B159/B160/B161 code adds:

    plan.AddRowRotation(..., L17 or higher, "B158 co-packed EvalPower")

to the level-aware key plan.

Therefore the new B158 RowRotation at L17 reuses a Galois key generated only
for L2.

## Why this is invalid

Lattigo's Automorphism calls GadgetProduct using the ciphertext level.

But GadgetProduct begins with:

    levelQ = min(levelQ, gadgetCt.LevelQ())

Hence for:

- ciphertext level = L17
- Galois-key level = L2

the actual key-switch gadget product is clipped to L2.

Automorphism then continues with an output/ring view at L17.

Thus this is not a valid L17 automorphism/key-switch evaluation. The high RNS
limbs are not supported by the L2 Galois key.

This directly explains the observed signature:

- input S_2@L17 is exact
- immediately after RowRotation, before any selector:
  almost all slots are wrong
  coefficient-noise trace becomes nonsensical/catastrophic

## Decision

The previous conclusions must be corrected:

B159:
- reported FAIL_NOISE at k=4
- INVALID_AS_B158_FALSIFICATION due to under-leveled RowRotation key

B160:
- reported FAIL_SCALE_INVARIANT_RESCUE at k=4
- INVALID_AS_B158_FALSIFICATION for the same reason

B161:
- reported FAIL_B161_HYBRID_RESCUE at k=4
- INVALID_AS_B158_FALSIFICATION for the same reason

These runs still validate:
- recurrence implementation through S_2
- operation counting through the reached stages
- selector-rescale behavior on the UNROTATED branch

But they do NOT establish that B158 fails natively at k=4.

## Corrected next gate: B162

Generate the B158 RowRotation Galois key at a level >= every B158 use.

For the B161 hybrid schedule:
- first RowRotation is on S_2 at L17
- therefore a row-rotation Galois key at L17 is sufficient
- generating it at L18 is also conservative and compatible with all lower
  B158 rotations

Because the planner stores one key per Galois element at the maximum requested
level, add the B158 row-rotation use explicitly before key generation, e.g.:

    plan.AddRowRotation(params, polyInputLevelForPlan, "B158 co-packed EvalPower")

or at the exact first-use level L17 if the implementation prefers the minimum
sufficient key.

Do NOT change:
- N/T/Q/P
- secret/security
- recurrence
- selector schedule
- B161 hybrid arithmetic

The first corrected test should run ONLY x=1 and confirm:

1. S_2 exact
2. RowRotation(S_2) exact BEFORE selector multiplication
3. then continue k=4,8,... until failure or full completion

If corrected RowRotation itself is not exact, stop as implementation failure.

Only after the corrected key passes the rotation sanity gate may any noise
conclusion about B158 be accepted.

## Current authoritative interpretation

B158_ALGEBRA = PASS
B158_CTCT_OPTIMALITY = PASS
B159-B161_NATIVE_NOISE_CONCLUSIONS = INVALIDATED_BY_KEY_LEVEL_BUG
B158_NATIVE_FEASIBILITY = UNRESOLVED
NEXT = B162_CORRECTED_ROW_KEY_NATIVE_GATE
DO_NOT_AUTO_RUN_CODEX = YES
