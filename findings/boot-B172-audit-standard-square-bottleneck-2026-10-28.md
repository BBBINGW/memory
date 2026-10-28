# BOOT — B172 audit: source-faithful standard square is the grouped-power bottleneck

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B172-B158-PS8192-CHECKPOINT32-GROUPED-NATIVE-20261028.zip\`

Reported and independently recomputed SHA-256:
\`3f4d051f81b14841f2127a0895fea0a658e72748836ba3f0a2adb4156155813c\`

Internal SHA256SUMS:
- 26/26 listed entries PASS
- no mismatches

The packaged \`parent-b171/main.go\` SHA-256 is:
\`e8e1823896bb710042e2acd0cf8b138f042f7a2d2d9b36d8cc4d31bb7e2da99c\`

It is byte-for-byte identical to the previously audited B171 \`source/main.go\`.

Thus B172 is accepted as a valid isolated checkpoint-32 experiment.

## Native result

\`STATUS = FAIL_B172_POWER_Y2\`

All three cases:
- A32 exact at L18, budget 372--373
- PH8192 exact at L18, budget 103--105
- Y_REP exact at L18, budget 125
- POWER_Y2 fails immediately at L17 with:
  - logQ = 615
  - required_logQ = 631
  - budget = -16
  - 32768/32768 mismatches

POWER_Y4 and final grouped output are downstream failures.

Native counts:
- main fused ct×ct = 13
- auxiliary square ct×ct = 8
- basis total ct×ct = 21
- grouped ct×ct = 4
- grouped ct×pt = 3
- grouped Rescale = 7
- no LT / pointwise / final rotate-sum executed

## Checkpoint-32 worked, but does not address the real bottleneck

Relative to B171, checkpoint 32 improves Y_REP by:
- +18 bits CASE_0
- +18 bits CASE_1
- +20 bits CASE_2

B172 Y_REP:
\[
\text{required}=524,\qquad \text{budget}=125.
\]

But the first source-faithful grouped square
\[
y\mapsto y^2
\]
implemented by
\[
\texttt{MulRelinNew + Rescale}
\]
produces:
\[
\text{required}=631,\qquad \text{budget}=-16.
\]

Thus one standard-tensoring square increases required-logQ by about 107 bits even after consuming one ~34-bit Q prime via Rescale.

This effect is essentially phase-independent in the three fixed cases, including x=0 and x=1.

Therefore further moving the checkpoint from 32 to 16 is not the right next move: the observed checkpoint improvement is only O(20) bits while the first grouped standard square requires O(100) extra bits.

## Contrast with the validated scale-invariant chain

The checkpoint auxiliary chain uses:
\[
\texttt{MulRelinScaleInvariantNew}
\]
with no Rescale.

Across B164--B172 it repeatedly shows only about 30--31 required-logQ bits per square while preserving exact correctness at L18.

Lattigo v6.2.0 explicitly documents:
- standard tensoring: noise increases multiplicatively with plaintext/noise norms and usually requires Rescale;
- scale-invariant tensoring: noise increases by a constant factor regardless of current noise, and no Rescale is required for subsequent invariant multiplications.

Therefore the next decisive question is no longer checkpoint placement. It is whether the grouped-power binary-power subchain can use the already validated scale-invariant tensoring regime.

## Important scheduling caveat

Simply replacing only the two power-chain squares is not enough to declare the full grouped helper rescued.

The source helper also assumes descending plaintext-mask levels:
- bit-0 factor around L17,
- bit-1 around L16,
- bit-2 around L15,
and standard ct×ct accumulator combines with Rescale.

If y²/y⁴ are kept at L18 with scale-invariant tensoring, later low-level plaintext masks would implicitly truncate them before multiplication and could destroy the recovered headroom.

Thus the next gate should first isolate the multiplication primitive on the same Y_REP before modifying the whole grouped helper.

## Recommended next gate

B173 = standard-vs-scale-invariant square primitive diagnostic on the same B172 Y_REP.

For each of the same three cases:

1. reproduce checkpoint-32 Y_REP at L18;
2. branch copies from the same Y_REP;
3. standard branch:
   - \`MulRelinNew(Y,Y)\`, probe RAW at L18 before Rescale;
   - Rescale once to L17, probe again;
4. scale-invariant branch:
   - \`MulRelinScaleInvariantNew(Y,Y)\` at L18, no Rescale;
   - probe exact y²;
   - square again with \`MulRelinScaleInvariantNew\` to y⁴, probe exact y⁴;
5. report scale metadata as well as logQ/required/budget;
6. stop; do not build factors or grouped accumulator.

Decision:
- if SI y²/y⁴ remain exact with strong positive budget, the next candidate is a fully high-level scale-invariant grouped generator;
- if SI also fails, the B158-v2 downstream path is likely blocked more fundamentally;
- do not test k0=16 before this primitive comparison.

## State

- B170 PS8192 LT8: PASS_STRONG
- B171 source-faithful grouped: FAIL
- B172 checkpoint32 source-faithful grouped: FAIL at first y² square
- checkpoint32 effect: validated but insufficient
- source-faithful standard grouped multiplication schedule: incompatible with B158-v2 Y_REP
- scale-invariant grouped-power rescue: OPEN / HIGHEST PRIORITY
- active candidate remains ACTIVE_NATIVE_CANDIDATE pending B173
