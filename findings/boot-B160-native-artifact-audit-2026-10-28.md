# BOOT-B160 — independent native artifact audit

Date: 2026-10-28
TRACK_ID: BOOT
Artifact: BOOT-B160-B158-SCALE-INVARIANT-NATIVE-20261028.zip
SHA-256: 143bb12aa176a8f69859464179ed9dec8c6ae09c8658a2747eb8de085b7498b0

## Integrity

Independent audit:
- outer ZIP SHA-256 matches
- all SHA256SUMS entries verify
- exact B159 parent, B160 source, diff, commands, raw logs, stage-noise table,
  operation counts, environment, go.mod/go.sum are present

## Frozen point

Same as B159:
- upstream commit b113742d83d772fd0d1b353e72ac6e31f2838bea
- Lattigo v6.2.0
- N=32768, m=1, r=32768, degree=65536
- T=65537, p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048, h=512

No cryptographic parameter changed.

## Exact B160 change

Only the B158 fused ct-ct multiplication was changed to:

    (*bgv.Evaluator).MulRelinScaleInvariantNew

No explicit rescale follows the fused ct-ct multiplication.

Selector ct-pt products remained exactly the B159 scale-one/no-rescale path.

Thus B160 tests:

    regular no-rescale selectors
    + scale-invariant ct-ct tensoring

It does NOT test selector-rescale + scale-invariant ct-ct.

## Native result

B159 vs B160:

k=1:
- B159 608-bit budget
- B160 608-bit budget

k=2:
- B159 562-bit budget
- B160 578-bit budget

k=4:
- B159 -16-bit budget
- B160 -16-bit budget
- B160 mismatches: 32767/32768
- required logQ: 665 bits
- available logQ: 649 bits

Mandatory stop was correctly triggered.

Actually executed before stop:
- 2 logical scale-invariant ct-ct multiplications
- 2 relinearizations
- 0 explicit ct-ct rescales
- 1 RowRotation
- no extra encrypted multiplication

No benchmark was run.

Decision:
- B160_STATUS = FAIL_SCALE_INVARIANT_RESCUE
- B158_NO_RESCALE_SELECTOR_REALIZATION = FAIL_NOISE
- scale-invariant ct-ct improves k=2 modestly but does not remove the k=4
  selector-induced failure

## Important API clarification

Lattigo MulScaleInvariant supports plaintext operands, but for degree-0
plaintext operands its implementation calls tensorStandard. For []uint64 masks
it creates a scale-one plaintext and also calls tensorStandard.

Therefore simply replacing the B159 selector call with MulScaleInvariant would
not create a new selector-noise mechanism; it is not a meaningful B161 rescue.

## Root-cause interpretation

The failure is now strongly localized to allowing the large coefficient-domain
selector product to enter the fused multiplication without first normalizing it.

2026/975's source-faithful MonomialGen instead does:

    mask ct-pt multiply
    -> Rescale
    -> add public constant
    -> ct-ct multiply/rescale

The selector-rescale step is therefore an already-native-proven mechanism that
B159/B160 deliberately removed to preserve one-level-per-doubling.

However scale-invariant ct-ct multiplication creates a new hybrid possibility:
move the one level drop back to the selector, and remove it from the fused
ct-ct multiplication.

This motivates B161.

