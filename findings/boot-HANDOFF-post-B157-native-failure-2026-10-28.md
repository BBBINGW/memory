# Resume BOOT — Post B157 Native Failure

Date: 2026-10-28
TRACK_ID: BOOT

## Authoritative session status

LATEST_COMPLETED: B157_NATIVE
B157_STATUS: FAIL_PRECISION + FAIL_NATIVE_VALUE
B157_SECURITY_CONTEXT: PASS
B157_PLAINTEXT_ALGEBRA: PASS
MAIN_POSITIVE_CANDIDATE: NONE
B145_ALGEBRA_STATUS: SURVIVES
B145+B152_CURRENT_NATIVE_BACKEND: KILLED
NOVELTY: ALGEBRAICALLY_PROMISING_BUT_NO_VIABLE_NATIVE_REALIZATION

Do not describe B157 as pending.

## B157 decisive evidence

Fixed secure candidate:
- N=65536
- depth=32
- scaleBits=50
- NumLargeDigits=33
- HEStd_128_classic
- Q=1650, P=60, QP=1710
- no optional output repacking
- 256 words/ciphertext
- Root4096 + 8 LUTs

Security:
- native HEStd_128_classic context instantiated
- QP is 36 bits below the approximately 1746-bit paper-derived bound
- independent malb/lattice-estimator not run due missing SageMath

Native correctness:
- 3615 / 65536 correct bits
- 256 / 256 failed words
- max error 1,053,561.2516
- pre-Root/LUT max integer residual 0.01414467
- degree-4095 LUT evaluation catastrophically amplifies the residual

Plaintext schedule:
- 1,057,488 / 1,057,488 cases pass

Native value:
- candidate core latency 288.337001 s
- fair baseline 48.99471343 s
- slowdown 5.885x
- shared powers + 8 LUTs alone 259.090102 s
- peak memory approximately 201 GiB
- setup/keygen 101.858 s

Decision:
Do not tune this backend further. Precision repair alone cannot rescue the value gate.

Artifact reported by PI:
BOOT-B157-DEPTH32-NATIVE-20261028.zip
SHA-256 c0510f3bf0ad1edd1d012aecf550bd66f696eeb08811179a32ff0bed432c380c
Raw artifact has not yet been independently audited in ChatGPT because the ZIP bytes are not available through the current conversation/library mount.

## Post-B157 fresh scout

### ePrint 2026/975
Full PDF and author implementation were audited.

Dominant current author-repo 9-bit m=1 timings:
- online 2.061226016 s
- Step1 0.693407006 s
- poly eval 1.284264686 s
- BuildBasis 1.141456575 s

A co-packed EvalPower recurrence can algebraically combine power-block extension and auxiliary squaring in one ct-ct multiply per layer using row swap + selector masks.

Gates:
- symbolic algebra: survives
- BFV scale/level semantics for 0/1 masks: survives
- value: marginal/negative because saved ct-ct multiplies are replaced by roughly the same number of high-level row rotations plus masks

Status:
PARK_VALUE_MARGINAL
Do not implement unless a future construction removes/shares the rotations.

### ePrint 2026/1730 / CRYPTO 2026
Priority source.
Public claims:
- sparse-secret line reduces work from ~O(n^2) to ~O(nh)
- Binary-NTT RLWE line reduces sequential NTT/INTT depth to 3 while retaining comparable total word-operation count
- public material suggests parallel/GPU latency potential, but full algorithm-level source is still required before making any Binary-NTT security or implementation claim

Research question:
Can the 3-layer Binary-NTT construction be made genuinely work-efficient / memory-traffic-efficient, not merely shallow?

Status:
SOURCE_REQUIRED_FOR_ALGORITHM_LEVEL_GATE

### ePrint 2026/2630
Direct free fusion of arbitrary functional PBS into an error-index-only blind rotation was structurally rejected in the standard fixed-public-accumulator model.

Remaining possible space:
mixed refresh-only / functional-PBS graph scheduling or other source-specific structure.

Status:
LOWER_PRIORITY / FULL_SOURCE_REQUIRED

### ePrint 2026/2616 Descent-PBS
Real memory/key-size bottleneck remains.
Generic seeded compression is prior art.
Only Descent-specific module-to-ring key sharing/reconstruction is worth considering.

Status:
CONDITIONAL_SOURCE_REQUIRED

## Next research priority

1. 2026/1730 full algorithm/source audit
2. fresh whole-bootstrap source scouting for stage deletion / sequential-dependence reduction / security-modulus changes
3. 2026/2630 full-source novelty gate
4. 2026/2616 Descent-specific memory structure

Avoid:
- B145/B152 micro-tuning
- 975 co-packed implementation
- generic NTT/permutation micro-optimizations
- generic sparse-secret GPU transplant
