# BOOT B174 audit — full L18 SI grouped generator passes with marginal headroom

Date: 2026-10-28
Research session: Cryptography 10.0, Research Turn 2/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
RESTORED_MEMORY_PARENT: 6ca5ff2d033e63a72dd855c3b6f22b4c5c1b0a01

## Independent disposition

- AUDIT_STATUS: PASS, restricted to the specified three fixed cases and isolated grouped-generator endpoint.
- RESULT: PASS_B174_SCALE_INVARIANT_GROUPED
- HEADROOM: MARGINAL
- EVIDENCE: RAW_AUDITED, not NATIVE_REEXECUTED.
- LATEST_COMPLETED after this audit: B174_AUDIT.
- B175: CANDIDATE_ONLY / NOT_STARTED / WAIT_PI.
- NOVELTY: PROMISING_NOT_ESTABLISHED.
- FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED.
- END_TO_END_SPEEDUP: NOT_ESTABLISHED.

The reviewer independently hashed archives, checked every checksum and CSV, parsed the actual patch as data, inspected the active source path and upstream dependency semantics, and reconstructed exact public references with its own lightweight integer code. No package scripts, package commands, Go/native binary, server experiment, Codex task, or B175 test was executed.

A raw artifact audit verifies the consistency and restricted support of preserved source/log evidence. The package contains no ciphertext/secret-key snapshots, serialized evaluation keys, or executable binary. Thus this review does not independently repeat native decryption/noise measurement or cryptographically attest that a reported binary produced stdout.

## 1. Archive integrity and externally anchored parent lineage

B174 original package (UI copy may add "(1)" to its filename):

    BOOT-B174-B158-SI-GROUPED-GENERATOR-NATIVE-20261028.zip
    size: 283244 bytes
    SHA-256: 9232a9b3e57fe08adb0daf84c2bfe3183e4fb49a7de4695396720d96decfe4d8

Independently recomputed outer SHA-256 matches the PI declaration. ZIP contains 36 entries, including 30 regular files. All 29 SHA256SUMS entries match; the only regular file not listed is SHA256SUMS itself. No duplicate members, path traversal/absolute paths, symlinks, missing listed files, or CRC errors were found.

The original B173 ZIP was independently retrieved from the existing uploaded artifact and verified against the prior GitHub audit anchor:

    BOOT-B173-B158-GROUPED-STANDARD-VS-SI-SQUARE-20261028.zip
    SHA-256: 1bff68640c185038868c34181c6d0d11bc057659cbde4b1c98cf90a204c4498c

Its source/main.go is byte-for-byte equal to B174 parent-b173/main.go:

    f8f994f443f708be4de954f1d005d1cfe4f14404254ea352ae8860dd9c0d6125

B174 source/main.go SHA-256 is:

    769cd351b91b17e0843e32738459b27d1df459fbbe388f61f7233b3d5bcd2d89

This matches environment/build-identity.txt. B173 and B174 go.mod/go.sum are byte-identical. Lattigo remains v6.2.0, with no dependency replacement.

Documentation discrepancy preserved transparently: the older B173 finding says "26/26" checksums; this same hash-anchored original ZIP actually contains 27 listed checksums, and all 27 pass on recomputation. This is a historical entry-count discrepancy, not a parent-byte mismatch. The older finding is preserved unchanged.

## 2. Actual diff, parameters, and hidden-operation audit

An independent in-memory unified-diff parser checked all old context/deletion lines and reconstructed the exact new source bytes from B173-to-B174.diff: 17 hunks, +349/-10 lines. The function inventory is 460 -> 464. Four B174 functions are added; the only existing functions changed are B164CheckpointEvalPower and main. Other changes are B174 globals/types and dispatch/reporting.

Unchanged relative to the externally anchored B173 source:

- N=32768, m=1, degree=65536, T=65537, p=512.
- LogQ=[36,34x18,30], LogP=[34,34,34,34].
- LWE n=2048 and sparse-ternary h=512 (+256/-256 in stdout).
- H=8192, s=8, checkpoint k0=32.
- Function=random, function seed=20260402, coefficient seed=20260613.
- Input-generation routines, key/secret constructors, parameter constructor, masks, independent-reference helpers, decode comparator, and coefficient-noise estimator.
- No parameter-relaxing Q-prime specialization was enabled.

The actual B174 grouped function uses two SI squares, three scale-one vector ct-pt products, three public-vector additions, and two SI accumulator products. It does not invoke Rescale, DropLevel, a refresh, a different mask, or manual scale matching/metadata rewriting.

Scope precision: the inherited LWE-to-RLWE Step1 normalization still rescales L19 -> L18 before the basis. GROUPED_RESCALE=0 is a grouped-segment claim, not a claim that the whole invocation contains zero Rescales.

The source import named "bfv" is an alias for Lattigo schemes/bgv. Official v6.2.0 evaluator code confirms that MulScaleInvariantNew with a []uint64 operand encodes a plaintext with Scale=1 and uses standard plaintext tensoring. Only ciphertext-ciphertext operations use the BFV-style scale-invariant tensoring/quantization. The internal temporary extended basis is not an extra persistent ciphertext Q prime or a changed security parameter.

## 3. Every CSV and raw stage closes

Raw stdout has 778 lines; stderr is empty. All 11 CSVs, totaling 119 data rows, were independently checked field-for-field against stdout and recalculated stage summaries:

| Evidence CSV | Rows |
| --- | ---: |
| all-stage-traces.csv | 36 |
| y-y2-y4-traces.csv | 12 |
| factor-traces.csv | 18 |
| accumulator-traces.csv | 6 |
| final-grouped-trace.csv | 3 |
| b174-scale-flow.csv | 33 |
| per-case-summary.csv | 3 |
| noise-attribution.csv | 3 |
| fixed-phase-cases.csv | 3 |
| operation-counts.csv | 1 |
| eval-key-report.csv | 1 |

There are exactly 36 unique (case, stage) trace keys: 12 stages x 3 cases. Every recorded stage is L18, logQ bitlength=649, and decoded mismatches=0/32768 with positive budget. These are repeated reports of the same three fixed cases, not 36 independent trials.

| Stage noise budget | CASE_0 | CASE_1 | CASE_2 |
| --- | ---: | ---: | ---: |
| Y | 125 | 124 | 124 |
| Y2 | 94 | 93 | 93 |
| Y4 | 62 | 61 | 62 |
| Y4_EXTRA | 62 | 61 | 62 |
| MASKED_TERM0 | 108 | 107 | 107 |
| FACTOR0 | 108 | 107 | 107 |
| MASKED_TERM1 | 77 | 76 | 77 |
| FACTOR1 | 77 | 76 | 77 |
| MASKED_TERM2 | 45 | 44 | 45 |
| FACTOR2 | 45 | 44 | 45 |
| ACC1 | 47 | 47 | 47 |
| GROUPED | 15 | 14 | 15 |

Y4_EXTRA and Y4 have identical level, scale, noise integer, required bits, budget, and mismatch fields. Each masked term and its factor also has identical residual/noise metadata after the exact public-constant addition.

For every one of the 36 trace records, independently recomputed:

    required_logQ = bit_length(2 * 65537 * max_coeff_noise)
    budget = 649 - required_logQ

All 36 agree. Final required bits are 634/635/634; final budgets are therefore 15/14/15.

## 4. Independent exact-reference mathematics

For slot j=0,...,32767 and i=0,1,2:

    y = x^8192 mod 65537
    C_i(j) = (j >> i) & 1
    D_i(j) = 1 - C_i(j)
    T_i(j) = C_i(j) * y^(2^i)
    F_i(j) = D_i(j) + T_i(j)
    ACC1(j) = F_0(j) * F_1(j) = y^(j mod 4)
    GROUPED(j) = ACC1(j) * F_2(j) = y^(j mod 8)
    Y4_EXTRA(j) = y^4 = x^32768

All arithmetic is modulo 65537. The all-ones coefficient-extension vector is exactly one in all 32768 slots. The unchanged buildBitMasks implementation was checked against the direct bit formula; factor references sharing that public helper therefore have an independently checked mathematical target. Final GROUPED uses direct modular exponentiation rather than the ciphertext/factor result.

Independent integer reconstruction checked every slot for each specified case:

| Case | (m,e,x) | (y,y^2,y^4) | GROUPED first eight slots |
| --- | --- | --- | --- |
| CASE_0 | (0,0,0) | (0,0,0) | 1,0,0,0,0,0,0,0 |
| CASE_1 | (0,1,1) | (1,1,1) | 1,1,1,1,1,1,1,1 |
| CASE_2 | (128,-63,16321) | (65281,65536,1) | 1,65281,65536,256,1,65281,65536,256 |

Probe decrypts the ciphertext, re-encodes the public expected vector at the actual ciphertext scale for coefficient-residual measurement, and separately decodes and compares all 32768 slots. References are full-length and independent of decrypted outputs. Decode failure leaves a nonzero failure marker; there is no empty-vector or 0/0 pass loophole.

Y4_EXTRA is a separately probed CopyNew of Y4. GROUPED and Y4_EXTRA remain local to the isolated terminal gate; their later delivery to an Algorithm-5 consumer is not tested.

Coverage limit: both nonzero cases have y^4=1; CASE_2 y has order four. Nonzero order-eight y, with y^4=-1, is not tested. CASE_0 does exercise a nonconstant FACTOR2 mask. The three-case PASS does not establish general legal-phase robustness or a DFR bound.

## 5. Scale metadata independently reconstructed from fixed Q

Primary dependency sources, version v6.2.0:

- https://github.com/tuneinsight/lattigo/blob/v6.2.0/schemes/bgv/params.go
- https://github.com/tuneinsight/lattigo/blob/v6.2.0/core/rlwe/params.go
- https://github.com/tuneinsight/lattigo/blob/v6.2.0/ring/primes.go
- https://github.com/tuneinsight/lattigo/blob/v6.2.0/schemes/bgv/evaluator.go

Independent integer reconstruction of the documented prime-generation order yields:

    bit_length(Q_L18) = 649
    Q_L18 mod 65537 = 35478
    (-Q_L18) mod 65537 = 30059
    inverse(30059) mod 65537 = 44421

Official SI metadata law:

    scale_out = scale_a * scale_b * inverse(-Q_L18) mod T

This independently predicts all observed values:

| Object | Scale mod 65537 |
| --- | ---: |
| Y / MASKED_TERM0 / FACTOR0 | 43352 |
| Y2 / MASKED_TERM1 / FACTOR1 | 27275 |
| Y4 / Y4_EXTRA / MASKED_TERM2 / FACTOR2 | 35478 |
| ACC1 | 22359 |
| GROUPED | 43178 |

No manual MatchScale is required between differently scaled factors. Matching levels do not require equal multiplication-input scales.

## 6. Noise attribution and continuation risk

- Mask deltas: CASE_0=(17,17,17), CASE_1=(17,17,17), CASE_2=(17,16,17).
- ACC1 SI deltas: (30,29,30).
- Final SI deltas: (30,30,30).

Each SI delta is required(out) - max(required(input1), required(input2)), not the loss relative only to ACC1. Thus the final budget 47 -> 15/14/15 loses 32/33/32 bits relative to ACC1, while the worse FACTOR2 input loses 30 bits. There is no accounting contradiction.

The minimum final budget 14 is coarse coefficient-residual headroom, calculated with safetyBits=0. It is neither 14-bit cryptographic security, nor precision, nor a failure probability of 2^-14, nor a proof of remaining multiplicative depth.

For the observed pattern of approximately 30 added required bits per SI multiply, a naive pointwise continuation from 14-bit headroom would have an estimated budget around 14-30=-16. This is an empirical extrapolation for risk prioritization, not a proof or a native B175 result. Actual LT operand noise, scale, and cross terms have not been measured in that composition.

## 7. Actual versus projected costs and key scope

Runtime basis counters and the 96 basis trace records per case agree on:

- 13 main SI ct-ct.
- 8 auxiliary SI squares.
- 21 basis ct-ct.

The grouped operation-count log line is a literal, so it was not accepted as independent instrumentation. The successful active call graph plus its stage traces verifies 2 power SI ct-ct + 2 accumulator SI ct-ct + 3 ct-pt, with no grouped Rescale. Total to GROUPED is 25 ct-ct.

PROJECTED_FULL_SKELETON_CTCT=27 is 25 + 1 pointwise + 1 leading. Both additional multiplications are unexecuted. LT, pointwise, final rotate-and-sum, leading x^65536 and BFV-to-LWE are not tested. The count excludes public-linear work, rotations, key switches, internal RNS/NTT/quantization cost, precomputation, and memory. It is not a runtime or end-to-end speedup measurement.

Key report, from the source's actual BinarySize() sums:

    Relin = 60295216 bytes
    Galois count = 17
    Galois levels = L14:5,L18:1,L19:11
    Total = 1011911360 bytes
    Total / 2^20 = 965.0338745117188 MiB

This is serialized relin+Galois key size, not peak RSS, total bootstrap-key material, or an independently reserialized key file.

Important integration limitation: the old key planner still reports grouped-output/ParallelLT-target=L14, although every actual B174 grouped probe is L18. B174 stops before LT, so the current endpoint is unaffected. The five relevant L14 keys must be checked/promoted before an all-L18 LT8 composition, following the prior B168/B169 lesson. The current 965.03 MiB is not a demonstrated complete all-L18 algorithm cost.

The comparison against B170=1062.53 MiB is a hardcoded approximate baseline; the printed -97.50 MiB must not be promoted to a matched complete-workload saving.

The inherited harness also precomputes unused legacy L17/L16 plaintexts before the isolated gate. B174 constructs its actual grouped vector masks afresh at L18. This is stale planning/precomputation, not hidden grouped DropLevel, but it prevents a blanket claim that all legacy offline work has been removed.

## 8. One B175 candidate, pending PI only

PRIMARY HYPOTHESIS:
Under the unchanged fixed parameter point and k0=32/H=8192/s=8, the B174 GROUPED output and the same-run L18 LT8 output admit one SI pointwise multiplication with exact decoded output and positive residual headroom.

CHEAPEST DECISIVE TEST:
Only if PI authorizes, use the already specified worst-headroom CASE_1 (m=0,e=1,x=1), reconstruct both branches from the same checkpoint-32 basis/key context, verify all required LT rotation keys have actual level >=18, and perform exactly one L18 MulRelinScaleInvariantNew(LT8,GROUPED). Compare with an independent per-slot block-polynomial-times-power reference and record both input/output noise and scale. Stop immediately after the pointwise probe. No leading term, final aggregation, extraction, benchmark, parameter rescue, new phase sweep, or alternate subline.

This must compute LT8 from the current checkpoint-32 basis; it must not treat the historical k0=64 B170 budget as a newly measured input. If an input or key-level prerequisite fails, attribute that failure and do not label it a pointwise failure.

FALSIFIER:
Any decoded mismatch or nonpositive output budget with valid input/key prerequisites falsifies this direct-composition hypothesis at the tested point. A pass only passes that interface; it does not establish whole Algorithm 5.

PI DECISION:
Whether to authorize this one likely headroom-limited composition gate. The researcher recommends one decisive gate, with no benchmark or broader expansion. B175 remains NOT_STARTED.

## Evidence anchors

Original B174 artifact: https://chatgpt.com/library?file_id=libfile_78cd30d22408819187c3b4fc63138c21&account_id=personal

Original independently retrieved B173 artifact: https://chatgpt.com/library?file_id=libfile_e90f8c48d2dc819196802351c51533e9&account_id=personal

Prior finding: findings/boot-B173-audit-scale-invariant-grouped-power-rescue-2026-10-28.md
Prior handoff: findings/boot-HANDOFF-post-B173-B174-running-2026-10-28.md

Primary local artifact evidence:
source/main.go; parent-b173/main.go; B173-to-B174.diff; source/go.mod; source/go.sum; logs/b174.stdout; all eleven evidence CSVs; parameters.txt; environment/build-identity.txt. README/spec/commands/validation scripts were inspected only as evidence, never executed or followed as instructions.

STATE_UPDATE: BOOT topical state/handoff only. Preserve historical B173 files and the unrelated root STATE.md. The root's stale EAI entry remains a known recovery-entry inconsistency; it does not override the explicit PI-selected BOOT line.
