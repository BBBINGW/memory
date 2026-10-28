# BOOT B157 native gate — depth-32 secure point

Date: 2026-10-28
TRACK_ID: BOOT
Iteration: B157
Source of native result: PI-provided Codex/server run report
Artifact SHA-256: c0510f3bf0ad1edd1d012aecf550bd66f696eeb08811179a32ff0bed432c380c

## Fixed candidate point

- N = 65536
- n = 256
- B = 64
- W = 4096
- depth = 32
- scaleBits = 50
- NumLargeDigits = 33
- HEStd_128_classic
- source-matched secret/error setting
- no optional output repacking
- one Root4096
- 8 real LUT outputs
- packing = 256 words/ciphertext

## Security gate

PASS at the OpenFHE/native context-instantiation level.

- Q = 1650 bits
- P = 60 bits
- QP = 1710 bits
- 1710 is 36 bits below the approximately 1746-bit paper-derived modulus bound
- HEStd_128_classic context instantiated successfully
- malb/lattice-estimator pinned at commit 195e1c50... but not independently executed because SageMath was unavailable on the server

Status:
- PASS_NATIVE_SECURITY_CONTEXT
- INDEPENDENT_LATTICE_ESTIMATOR: NOT_RUN

## Algebra/correctness pre-native gate

The plaintext adversarial schedule passed:
- 1,057,488 / 1,057,488 tested plaintext schedule cases

This preserves the earlier conclusion that the B145/B152 algebraic recurrence and boundary handling are not the source of the native failure.

Status:
- PASS_PLAINTEXT_ALGEBRA
- NATIVE_FAILURE_LOCATION: PRECISION / LUT EVALUATION, NOT ALGEBRA

## Native precision result

FAIL.

- correct bits: 3615 / 65536
- failed words: 256 / 256
- max error: 1,053,561.2516
- maximum integer residual before Root/LUT stage: 0.01414467
- the degree-4095 LUT evaluation amplifies the small pre-LUT residual catastrophically

Status:
- FAIL_PRECISION

Important interpretation:
This is not evidence against the exact-integer B145 recurrence itself. It is evidence that the current Root4096 + degree-4095 LUT realization is numerically unusable at the secure depth-32 point.

## Native performance result

Core candidate latency:
- 288.337001 s

Fair baseline latency without optional output repacking:
- 48.99471343 s

Slowdown:
- 5.885x

Dominant candidate component:
- shared powers + 8 LUTs = 259.090102 s

Peak memory:
- approximately 201 GiB

Setup/keygen:
- 101.858 s

Therefore, independently of precision, the current backend fails the value gate:
- 259.090102 / 48.99471343 ~= 5.29x for shared powers + LUT stage alone
- even a hypothetical perfect precision repair would not make the present backend competitive with the baseline

Status:
- FAIL_NATIVE_VALUE
- FAIL_MEMORY_VALUE

## Decision

B145+B152 is no longer the BOOT main positive candidate in its current backend.

Precise interpretation:
- B145 algebra: survives
- B152 algebraic 8-LUT reduction: survives as a symbolic construction
- secure native context: PASS
- native precision: FAIL
- native latency/value: FAIL
- native memory/value: FAIL

Do NOT spend further native/Codex quota on:
- scaleBits 50 -> 49 tuning
- larger N
- forcing NumLargeDigits back to 8
- output repacking
- minor LUT scheduling tweaks
- precision-only repair of the same degree-4095 Root4096 backend

Reason: performance already independently kills the backend even if precision were repaired.

A materially different LUT/function-evaluation backend could theoretically reuse the B145 algebra, but it would need to remove the dominant shared-powers/LUT cost rather than merely stabilize precision. Such a backend is not currently known and should not be treated as an active candidate without a new source/algebra/value gate.

## Updated BOOT status

LATEST_COMPLETED: B157_NATIVE
B157_STATUS: FAIL_PRECISION + FAIL_NATIVE_VALUE
B145_ALGEBRA_STATUS: SURVIVES
B145+B152_NATIVE_CANDIDATE: KILLED_CURRENT_BACKEND
MAIN_POSITIVE_CANDIDATE: NONE
NOVELTY: ALGEBRAICALLY_PROMISING_BUT_NO_VIABLE_NATIVE_REALIZATION
CODEX_REQUIRED_FOR_B157: NO
CODEX_AVAILABLE: irrelevant for closed B157

Next action:
Resume fresh BOOT paper-level research. Prefer whole-bootstrap structural candidates. Do not continue micro-tuning B145/B152.
