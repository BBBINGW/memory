# BOOT — B168 artifact audit: diagnostic invalidated by LT Galois-key level plan

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact

Artifact:
\`BOOT-B168-B158-LT-NOISE-ATTRIBUTION-20261028.zip\`

Reported and independently recomputed SHA-256:
\`837c9a549c723275dd611b3c028e935d7144450880890f294a084590ea6e4844\`

Internal SHA256SUMS:
- 26/26 listed entries PASS
- no mismatches

B168 parent source:
\`source/main.b167-parent.go\`
SHA-256:
\`eef4f52f7010fb9e7494acf662a9c74dc980b08f87f58bc1a5e308242b48e5b0\`

This is byte-for-byte identical to \`source/main.go\` in the independently audited B167 artifact.

The two packaged B167->B168 diff copies are byte-identical:
\`59added1f9d6426c85db24eefeeae99e6561ca99e06a2fecb7ecc5226b503bcf\`.

Thus the artifact itself is internally consistent.

## Reported result

\`STATUS = FAIL_B168_DIAGNOSTIC_SEMANTICS\`

All three B168 attribution cases failed at the first full FINAL_LT replay:
- L18
- logQ=649
- required_logQ=665
- budget=-16
- essentially all slots wrong.

The same compiled binary, when run in B167 control mode, passed all three raw-L18 LT cases with positive budgets 20, 24, and 23 bits.

Therefore the B167 algorithmic result remains valid.

## Root cause

The failure is caused by a B168 experiment-harness key-plan bug, not by the four-block LT arithmetic.

The rotation plan contains an explicit promotion of all raw-L18 ParallelLT rotation keys only under:

\`if globalB167LTNoPreDrop { ... AddColRotation(..., polyInputLevelForPlan, ...) ... }\`

B168 sets:
\`globalB168LTNoiseAttribution=true\`

but does **not** set:
\`globalB167LTNoPreDrop=true\`.

Therefore B168 executes ParallelLT at L18 without inheriting B167's explicit L18 rotation-key promotion.

Native key summaries prove the mismatch.

### B168 attribution run

- total Galois keys: 15
- L2: 3 keys
- L18: 1 key
- L19: 11 keys

The sole L18 key is the corrected B158 row key.

Thus three column-rotation keys required by the L18 LT remain only at L2.

### Same binary, B167 control

- total Galois keys: 15
- L2: 0 keys
- L18: 4 keys
- L19: 11 keys

The three previously-L2 column keys are promoted to L18.

The control raw-L18 LT then passes.

This exactly explains why the B168 attribution replay returns an invalid L18 ciphertext while the B167 control succeeds.

## Consequence

The B168 result is not a research-level negative result.

Classify:

- \`B168_DIAGNOSTIC_RESULT = INVALID_HARNESS_KEYPLAN\`
- \`FOUR_BLOCK_LT_FEASIBILITY = PASS_MARGINAL\` from B167
- \`LT_NOISE_ATTRIBUTION = NOT_RUN_VALIDLY\`
- \`DOMINANT_NOISE_SOURCE = UNKNOWN\`

Do not infer any LT-noise-source conclusion from B168's -16-bit FINAL_LT value.

## Correct next gate

B169 should rerun exactly the B168 attribution experiment with one substantive harness fix:

change the raw-L18 LT rotation-key promotion condition to cover both modes:

\[
\texttt{globalB167LTNoPreDrop || globalB168LTNoiseAttribution}.
\]

Before executing any attribution case, assert that every Galois element used by the physical-r=32768, ell=4 LT has an evaluation key with LevelQ >= 18.

The required elements are:
- column rotations for shifts 1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192;
- final row rotation.

The key-plan assertion, rather than aggregate key counts alone, is authoritative.

B169 should first execute an uninstrumented B167-equivalence control under the B169 key plan and require exact raw-L18 LT correctness. Only then run the internal attribution replays.

No algorithm, parameter, mask, level, or modulus change is justified.

## State

- B165 checkpoint half-basis robustness: PASS_STRONG
- B167 four-block raw-L18 LT: PASS_MARGINAL
- B168: INVALID_HARNESS_KEYPLAN
- LT internal noise attribution: OPEN
- active candidate: ACTIVE_NATIVE_CANDIDATE
