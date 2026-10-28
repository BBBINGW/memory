# BOOT — B166 native artifact audit and level-policy diagnosis

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B166-B158-HALFBASIS-4BLOCK-LOWER-NATIVE-20261028.zip\`

Reported and independently recomputed SHA-256:
\`92118fd0ec4bc78b786129ae9cabe54da46da7b9f1ce2f25f24e8c9b6f70bb28\`

Internal SHA256SUMS:
- 25/25 entries PASS
- no mismatches

B166 packaged parent source:
\`source/main.b165-parent.go\`
SHA-256:
\`54309edf282b1ba541c95648ec9a89892ff5e14c689a484c62192fe0a2faf845\`

This is byte-for-byte identical to \`source/main.b165.go\` from the independently audited B165 artifact.

The two packaged B165-to-B166 diffs are byte-identical.

Therefore the B166 failure is accepted as a valid native result of the specified patch.

## Native result

\`STATUS = FAIL_B166_HALFBASIS_4BLOCK_LOWER\`

All three fixed cases first reproduce the B165 half basis exactly and with positive budget.

Half-basis counts remain:
- main ct×ct = 14
- auxiliary ct×ct = 8
- total ct×ct = 22
- RowRotation = 14

ParallelLT executes exactly the expected operation structure:
- ct×pt = 4
- baby rotations = 1
- giant rotations = 1
- sum-column rotations = 12
- final row rotation = 1
- total rotations = 15

All cases then fail at the LT output:
- level L15
- logQ = 547
- required_logQ = 563
- budget = -16

Mismatches:
- CASE_0 x=0: 32768/32768
- CASE_1 x=1: 32766/32768
- CASE_2 x=16321: 32766/32768

No grouped powers, pointwise multiplication, rotate-and-sum, leading term, or tail is executed.

## Critical diagnosis: failure occurs after an already-invalid pre-drop

B166 implements:

\`groupedPredictedLevel := phRep.Level() - 3\`

With PH_REP at L18, this predicts grouped powers at L15. The existing “extra-level” Algorithm-5 policy is then invoked, producing:

- PH_REP input: L18
- predicted grouped: L15
- ParallelLT input: L16
- post-LT target: L15
- pre-drop: 2 levels

This is visible in the native log:

\`PH_REP=L18 predicted-GROUPED=L15 ParallelLT-input=L16 post-target=L15 pre-drop=2\`

But immediately before this policy, the three PH_REP ciphertexts have:

- CASE_0: required_logQ = 594, budget 55 at L18/logQ649
- CASE_1: required_logQ = 593, budget 56
- CASE_2: required_logQ = 593, budget 56

At L16, the available modulus is only about 581 bits.

A plain DropLevel does not divide the existing error by the dropped primes. Therefore, before any ParallelLT arithmetic, the dropped ciphertext is already approximately:

- CASE_0: 581 - 594 = -13 bits
- CASE_1/2: 581 - 593 = -12 bits

of coefficient-noise budget.

Thus:

\[
\boxed{\text{B166 does not establish that 4-block ParallelLT is intrinsically noise-infeasible.}}
\]

It establishes that the original pre-drop level policy is incompatible with the much noisier checkpoint-generated half basis.

## Why the observed -16 is consistent with this diagnosis

The LT result is then rescaled once from L16 to L15.

Since BGV Rescale approximately divides both ciphertext modulus and absolute error by the dropped prime, it approximately preserves noise budget.

The observed L15 budget of -16 is therefore consistent with an already-negative L16 input plus only a few additional bits of LT/key-switch noise.

Heuristically, the L15 required_logQ=563 corresponds to roughly 597 bits before the final ~34-bit rescale, only about 3–4 bits above the original PH_REP required_logQ 593–594.

This is a diagnostic inference, not a substitute for a native pre-rescale probe.

## Next minimal gate

B167 should modify only the LT level policy:

1. keep PH_REP at L18;
2. perform the exact same four-block ParallelLT at L18;
3. probe the raw LT output at L18 before any Rescale;
4. Rescale one level at a time L18->L17->L16->L15;
5. probe correctness/noise after every Rescale;
6. stop at the L15 LT output;
7. do not generate grouped powers or continue Algorithm 5.

No Q primes, N, T, secret, checkpoint, keys, or algorithmic structure change.

Hypothesis:
if the LT itself adds only a few bits of required noise as the B166 result suggests, raw L18 LT should retain roughly 50 bits of headroom and sequential Rescale should retain similar headroom down to L15.

If B167 fails already at raw L18 LT, the four-block LT representation is genuinely noise-infeasible at this parameter point.
If raw L18 LT passes but a Rescale step destroys correctness unexpectedly, investigate BGV scale/level semantics.
If L15 passes with positive/strong headroom, B166 is classified as a level-policy failure and the lower-path integration should resume in the next gate.

## State

- B165 checkpoint half-basis robustness: PASS_STRONG
- B166 original-policy downstream integration: FAIL_LEVEL_POLICY
- four-block ParallelLT intrinsic feasibility: STILL OPEN
- checkpoint-decoupled half-basis candidate: remains ACTIVE_NATIVE_CANDIDATE
- full lower polynomial: NOT_ESTABLISHED
- full Algorithm 5: NOT_ESTABLISHED
