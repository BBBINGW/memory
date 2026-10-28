# BOOT — B167 native audit and 4-block LT noise bottleneck

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B167-B158-HALFBASIS-LT-NO-PREDROP-NATIVE-20261028.zip\`

Reported and independently recomputed SHA-256:
\`07aaa3faf1a38d5fc3a7b1de1b60c9b166db21160a57c0c015f3c2922d18758e\`

Internal SHA256SUMS:
- 24/24 entries PASS
- no mismatches

B167 packaged parent source:
\`source/main.b166-parent.go\`
SHA-256:
\`f5a01767a2da9366718ce28398b24deef476fc36d5df65da2526da114da6f327\`

This is byte-for-byte identical to \`source/main.go\` from the independently audited B166 artifact.

The two packaged B166-to-B167 diff copies are byte-identical:
\`4a69ab16992f1cba46f85f55a7b3620f9d07320e2f02a83d82f7beb6add6ccc8\`.

Thus B167 is accepted as an isolated level-scheduling change over B166.

## Native result

\`STATUS = PASS_B167_LT_NO_PREDROP\`

\`HEADROOM = MARGINAL\`

All three cases pass exact 4-block ParallelLT at L18 and after sequential genuine Rescale operations to L17/L16/L15.

Per-case budgets:

- CASE_0 x=0:
  - PH_REP L18: 56
  - LT raw L18: 23
  - L17/L16/L15: 23

- CASE_1 x=1:
  - PH_REP L18: 55
  - LT raw L18: 21
  - L17/L16/L15: 21

- CASE_2 x=16321:
  - PH_REP L18: 50
  - LT raw L18: 14
  - L17/L16/L15: 14

Global minimum: 14 bits.

Operation counts:
- half-basis main ct×ct = 14
- auxiliary ct×ct = 8
- total half-basis ct×ct = 22
- half-basis RowRotation = 14
- ParallelLT ct×pt = 4
- ParallelLT total rotations = 15
- pre-LT DropLevel = 0
- post-LT Rescale = 3
- grouped/pointwise/final-sum stages = not executed

## B166 diagnosis confirmed

B166 failed because it first dropped PH_REP from L18 to L16, destroying its existing coefficient-noise budget before LT.

B167 runs the same 4-block LT directly at L18 and passes all cases.

Each subsequent Rescale reduces logQ and required_logQ by exactly 34 bits, preserving budget exactly.

Therefore:
- \`B166 = FAIL_LEVEL_POLICY\`
- \`FOUR_BLOCK_LT_NATIVE_FEASIBILITY = PASS\`

## New bottleneck

The 4-block LT itself adds substantial required noise:

- CASE_0: +33 bits
- CASE_1: +34 bits
- CASE_2: +36 bits

The worst case leaves only 14 bits.

This is too little headroom to safely assume the next Algorithm-5 pointwise ct×ct multiplication will survive. Earlier scale-invariant ct×ct measurements in this research line often add on the order of tens of required-logQ bits.

Therefore do not yet resume the full lower path.

## Structural decomposition of ParallelLT

For physical_r=32768 and ell=4, the current LT consists of:

1. BSGS first stage:
   - one baby rotation
   - four ct×pt mask products
   - two block additions
   - one giant rotation
   - one giant-block addition

2. Sum-columns reduction:
   \[
   q=(r/2)/ell=4096
   \]
   and therefore 12 repeated rotate+add steps with shifts
   \[
   4,8,16,\ldots,8192.
   \]

3. Final row-swap + add.

The 12 sum-columns rotations are not merely decorative replication: they accumulate the 4096 partial contributions needed to evaluate each degree-<H block polynomial. They cannot simply be deleted.

However, the exact noise contribution of:
- dense plaintext-mask multiplication,
- BSGS rotations/additions,
- 12-step sum-columns reduction,
- final row-swap duplication

has not yet been isolated.

## Next minimal gate

B168 should be diagnostic only.

Use the same three B167 cases and same L18 input, but instrument the LT internally and probe exact correctness/noise after:

- PH_REP input
- baby rotation
- each of the four ct×pt terms
- each two-term block sum
- giant rotation
- first-stage accumulator
- each of the 12 sum-columns rotate+add steps
- pre-row-swap output
- row-swapped copy
- final LT output

No Rescale, grouped powers, pointwise multiplication, or benchmark.

The purpose is to compute the incremental required-logQ cost of each substage.

Decision logic:
- if dense ct×pt terms dominate, investigate plaintext-mask representation/scaling/factorization;
- if sum-columns dominates, investigate a deferred/fused reduction with the downstream grouped-power multiply;
- if final row duplication is material, carry one-row sparse LT output downstream and duplicate only after collapse;
- if noise is spread irreducibly across all stages, the 4-block half-basis line may not have enough downstream margin without a deeper representation change.

## State

- B165 checkpoint-half-basis robustness: PASS_STRONG
- B166 old pre-drop integration: FAIL_LEVEL_POLICY
- B167 4-block LT no-pre-drop: PASS_MARGINAL
- four-block LT intrinsic correctness: PASS
- downstream grouped powers / pointwise / lower polynomial: NOT_RUN after corrected level policy
- active candidate: remains ACTIVE_NATIVE_CANDIDATE
- novelty: PROMISING_NOT_ESTABLISHED
