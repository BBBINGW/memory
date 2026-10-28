# BOOT B175 audit — direct L18 SI pointwise composition fails on noise

Date: 2026-10-28
Research session: Cryptography 10.0, Research Turn 6/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
MEMORY_PARENT: 75cfd147d8e9b024dd558d54727552d440be7609

## Independent disposition

- STATUS: FAIL
- RESULT: FAIL_B175_POINTWISE_NOISE
- ATTRIBUTION: POINTWISE_NOISE
- FIRST_FAILING_PROPERTY: POINTWISE_DECODED_MISMATCHES
- EVIDENCE: RAW_AUDITED, not NATIVE_REEXECUTED
- LATEST_COMPLETED: B175_AUDIT
- NEXT_EXPERIMENT: NOT_AUTHORIZED
- FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED
- DFR: NOT_ESTABLISHED
- END_TO_END_SPEEDUP: NOT_ESTABLISHED

The single authorized B175 gate falsifies the current fixed-parameter direct SI pointwise composition. Both encrypted inputs are valid, exact, positive-budget L18 ciphertexts. One actual `MulRelinScaleInvariantNew(LT8, GROUPED)` then produces negative residual budget and 32767/32768 decoded mismatches. No rescue or retry was performed.

## Artifact integrity and lineage

Original artifact:

    BOOT-B175-B158-CASE1-SI-POINTWISE-NATIVE-20261028.zip
    size: 13,680,154 bytes
    SHA-256: 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa

Independent read-only audit results:

- ZIP structure and CRC: PASS.
- Internal `SHA256SUMS`: 65/65 PASS.
- Embedded `parent-b174/main.go` hash equals the already audited B174 source hash `769cd351b91b17e0843e32738459b27d1df459fbbe388f61f7233b3d5bcd2d89`.
- Build/run exit codes: 0/0.
- Raw operation events: 117.
- Full decoded/expected arrays: 32,768 rows per stage.
- Full coefficient residual arrays: 32,768 rows per stage.
- The audit parsed evidence as data and did not execute ZIP scripts or binaries.

This raw artifact audit establishes consistency and attribution of the preserved native evidence. It is not a second native execution.

## Fixed scope

Only CASE_1 was executed:

    message=0
    phase_error=1
    phase_x=1
    N=32768
    T=65537
    k0=32
    H=8192
    s=8

The B174 checkpoint-32 basis and GROUPED construction were reused. A source-equivalent raw-L18 LT8 was constructed in the same secret/evaluation-key context. The five actually required LT rotation keys were minimally promoted from L14 to L18. There was no parameter sweep, second randomness trial, B176, k0=16, Q change, leading multiplication, post-pointwise aggregation, extraction, DFR test, benchmark, or end-to-end timing.

## Independent reference and noise recomputation

All 65,536 public lower-polynomial coefficients were read and reduced into eight independent block sums:

    [11087, 58815, 18874, 28124, 40315, 9695, 16678, 37121]

These reconstruct all 32,768 public expected slots. Since CASE_1 has x=1, GROUPED expected is the all-one vector and POINTWISE expected equals the LT8 block-sum reference. Thus the comparison is not generated from decrypted outputs.

For every stage, required bits were recomputed from all coefficient residuals using the preserved rule:

    required_bits = bit_length(2 * T * max_abs_centered_coefficient_residual)
    budget = bit_length(Q_L18) - required_bits

| Object | Level | Scale mod T | Required bits | Budget | Decoded mismatches |
| --- | ---: | ---: | ---: | ---: | ---: |
| LT8 | L18 | 43352 | 577 | +72 | 0/32768 |
| GROUPED | L18 | 43178 | 633 | +16 | 0/32768 |
| POINTWISE | L18 | 30059 | 664 | -15 | 32767/32768 |

The scale is independently closed by the B174 L18 SI multiplier:

    43352 * 43178 * 44421 mod 65537 = 30059

The pointwise multiplication adds 31 required bits relative to the noisier input:

    664 - max(577, 633) = 31
    16 - 31 = -15

This matches the observed negative budget and almost-total decoded failure. The single matching slot does not rescue the gate because the authorized criterion requires 0/32768 mismatches and positive budget.

## Actual operation and key cost

Independent counts from 117 raw operation events:

| Segment | Actual operations |
| --- | --- |
| Step1 | Rescale 1 |
| Basis | SI ct-ct 21; ct-pt 19; rotations 13; key switches 13 |
| GROUPED | SI ct-ct 4; ct-pt 3; rotation/key switch 1 each |
| LT8 | ct-pt 8; column rotations 15; row rotation 1; key switches 16 |
| POINTWISE | SI ct-ct 1 |
| Leading | ct-ct 0 |

Total actual ct-ct through pointwise is 26. No later Algorithm-5 operation was executed.

Minimal key promotion changes the reported level distribution from `L14:5,L18:1,L19:11` to `L18:6,L19:11`:

    before: 1,011,911,360 bytes = 965.03 MiB
    after:  1,114,150,880 bytes = 1062.54 MiB
    delta:    102,239,520 bytes = 97.50 MiB

These are native `BinarySize()` totals for relin/Galois keys, not measured RSS or total bootstrapping-key material. They show that the B174 isolated-harness apparent saving is not preserved after making LT8 genuinely usable at L18.

## Scientific conclusion and boundary

[NEGATIVE] Under the unchanged parameter point and the one authorized CASE_1 randomness, valid exact L18 LT8 and GROUPED inputs cannot be composed by the current direct SI pointwise multiplication while preserving decryption correctness.

The falsified mechanism is exactly:

    B174 GROUPED
    + same-context raw-L18 LT8
    + direct SI pointwise

This does not falsify every checkpoint-decoupled representation or authorize a new representation. It does not establish nontrivial y^4=-1 phase behavior at the integrated interface, complete Algorithm 5, DFR, or speedup.

## Pending decision and no-regret continuation

Directional choice `BOOT-DECISION-001` is pending: kill the fixed direct combination outright, or permit one bounded representation-layer redesign proposal for later PI authorization.

Researcher recommendation: treat the direct SI pointwise combination as killed and avoid parameter rescue or repeated native testing. While PI judgment is pending, continue only work useful under either choice: literature/novelty search, exact necessary-condition derivation, representation-layer feasibility bounds, shared cost/security/correctness analysis, provenance, and reproducibility.

STATE_UPDATE: YES. Update the topical BOOT state and durable PI queue. Preserve B174 and the original B175 artifact as parent evidence.
