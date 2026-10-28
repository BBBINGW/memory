# BOOT-B157 — exact secure depth-32 native audit

Date: 2026-10-28  
TRACK_ID: BOOT  
Artifact SHA-256: `c0510f3bf0ad1edd1d012aecf550bd66f696eeb08811179a32ff0bed432c380c`

## Independent artifact audit

The uploaded ZIP was independently inspected.

- outer SHA-256 matches the reported digest
- internal `MANIFEST.sha256`: all listed files PASS
- exact source, patch, raw stdout/stderr, security probe, memory trace, commands,
  environment, generated vectors, and diagnostics are present
- no Codex/GPU/server execution was initiated by this audit

## Fixed point

The native candidate and the separate security probe both fix:

- N = 65536
- word size = 256 bits
- packing = 256 words/ciphertext
- B = 64
- W = 4096
- scaleBits = 50
- multiplicative depth = 32
- HYBRID NumLargeDigits = 33
- secret = UNIFORM_TERNARY_ENCAPSULATED
- security target = HEStd_128_classic
- no output repacking

OpenFHE instantiated the exact point:

- Q = 1650 bits / 33 towers
- P = 60 bits / 1 tower
- QP = 1710 bits
- paper/source modulus bound ~= 1746 bits
- OpenFHE ternary table bound = 1747 bits
- margin = 36--37 bits

Therefore the B156 security concern is resolved positively for this exact point:
`PASS_SECURITY_INSTANTIATION`.

The pinned malb/lattice-estimator commit was recorded but could not be run
because SageMath was unavailable. This does not change the native OpenFHE
HEStd result.

## Native correctness / precision

The exact B145+B152 one-FBS candidate fails decisively:

- exact bits: 3615 / 65536
- failed words: 256 / 256
- maximum absolute decoded-bit error: 1,053,561.251602464
- mean absolute decoded-bit error: 303.354958539
- minimum rounding margin: -1,053,560.751602464
- clear adversarial schedule checks: 1,057,488 PASS

A stop-before-Root diagnostic measured:

- maximum active-window integral residual = 0.0141446716024802

The clear/integer schedule therefore remains algebraically correct; failure is
in the native approximate realization. The degree-4095 LUT path amplifies the
small pre-Root residual catastrophically.

Status:
- `PASS_CLEAR_ALGEBRA`
- `FAIL_NATIVE_PRECISION`

## Performance

Measured core A2B latency:

- preprocessing = 26.287556673 s
- Root/adapter = 0.501512508 s
- shared powers = 43.786710981 s
- eight LUTs = 215.303391468 s
- D0..D4 synthesis = 1.337258477 s
- affine prefix = 1.012296558 s
- final correction = 0.108273041 s
- total core = 288.337000858 s

Fair no-repacking B156 baseline:

- 48.99471343 s

Thus:
- candidate is 5.885063524x slower
- speed ratio = 0.169921700x

The decisive observation is that the Root-postprocessing LUT block alone is:

- shared powers + eight LUTs = 259.090102449 s

This block is separate from the compressed projection-rotation chains in
preprocessing. Therefore repairing projection precision or restoring direct
rotation keys cannot rescue the current backend's performance.

Current non-LUT core cost is approximately:

- 288.337000858 - 259.090102449 = 29.246898409 s

To beat the 48.99471343 s fair baseline while keeping those other costs, the
shared-powers + 8-LUT block would need to fall below:

- 19.747815021 s

Required speedup for the LUT block:

- 259.090102449 / 19.747815021 = 13.11994x

This is a useful reopening threshold. Local B152 micro-optimizations are not
credible as a rescue.

## Memory / system

- sampled peak container memory ~= 201.0 GiB
- approximate steady key/setup footprint ~= 165 GiB
- setup/keygen = 101.857717893 s

The direct projection-key variant was attempted first and hit the machine memory
limit around 202.5 GiB. The completed implementation replaced ~80 direct
projection rotation keys with arithmetic-progression rotation chains and 12
explicit rotation keys. That compression adds key-switch work and contributes
to preprocessing precision loss, but it does not explain the 259.09 s
shared-power/LUT block.

## Decision

B157 is not merely a precision failure. It establishes a native value failure
for the current B145+B152 realization.

Authoritative interpretation:

- `B157_SECURITY = PASS`
- `B157_CLEAR_ALGEBRA = PASS`
- `B157_NATIVE_PRECISION = FAIL`
- `B157_NATIVE_PERFORMANCE = FAIL`
- `B157_NATIVE_VALUE = FAIL`

B145's pre-bootstrap adjacent-window overflow-cancellation algebra remains
valid and potentially novel.

However, B145+B152 as the current practical one-FBS A2B candidate is now:

- `PARK / FAIL_NATIVE_VALUE`

Do not spend further rounds on:
- scale 50 -> 49/51 local tuning
- extra Hermite-order micro-tuning
- output repacking
- NumLargeDigits micro-tuning
- direct projection keys
- local synthesis/prefix depth shaving

Reopen only if a genuinely different one-FBS 4096-domain backend can plausibly:
1. preserve packing,
2. achieve robust native precision, and
3. reduce the shared-power + eight-LUT block from 259.09 s to about <=20 s
   under a matched secure point.

## Track-level consequence

The previous main-positive status for B145+B152 should be retired.

Recommended BOOT state after B157:

- LATEST_COMPLETED: B157_AUDIT
- B157_STATUS: FAIL_NATIVE_PRECISION_AND_PERFORMANCE
- B145_ALGEBRA_STATUS: VALID / POTENTIALLY_NOVEL
- B145+B152_IMPLEMENTATION_STATUS: PARK / FAIL_NATIVE_VALUE
- MAIN_POSITIVE_CANDIDATE: NONE
- NEXT: FRESH_BOOT_WHOLE-BOTTLENECK_SCOUT
- CODEX_REQUIRED: NO for scouting

Fresh scouting should resume from whole-bootstrap structural bottlenecks rather
than local repair of B145+B152.
