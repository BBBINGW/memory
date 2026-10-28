# BOOT — B173 audit: scale-invariant grouped power chain rescue

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B173-B158-GROUPED-STANDARD-VS-SI-SQUARE-20261028.zip\`

Reported and independently recomputed SHA-256:
\`1bff68640c185038868c34181c6d0d11bc057659cbde4b1c98cf90a204c4498c\`

Internal SHA256SUMS:
- 26/26 listed entries PASS
- no mismatches

The packaged \`parent-b172/main.go\` SHA-256 is:
\`bb58b628fb47c84187f0c549192fc19155a61fad0b7cf53d8bee5debab9e8435\`

It is byte-for-byte identical to the independently audited B172 \`source/main.go\`.

The B172->B173 diff is isolated to the standard-vs-scale-invariant tensoring diagnostic and does not change the cryptographic parameters, checkpoint, H/s geometry, or source input generation.

## Native result

\`STATUS = PASS_B173_SCALE_INVARIANT_POWER_CHAIN\`
\`HEADROOM = STRONG\`

Common Y input:
- L18 / logQ=649
- scale mod T = 43352
- required_logQ = 524, 524, 525
- budgets = 125, 125, 124
- all exact

### Standard tensoring branch

Raw standard square:
\[
Y^2 = \texttt{MulRelinNew}(Y,Y)
\]

Before any Rescale:
- L18
- required_logQ = 665
- budget = -16
- 32768/32768 mismatches in all cases

Thus standard tensoring itself already fails.

One genuine Rescale:
- L18 -> L17
- logQ: 649 -> 615 (-34)
- required: 665 -> 631 (-34)
- budget remains -16
- mismatch remains complete

Therefore:
\[
\boxed{\text{Rescale does not cause the B171/B172 failure; standard tensoring does.}}
\]

### Scale-invariant branch

\[
SI\_Y2=\texttt{MulRelinScaleInvariantNew}(Y,Y)
\]
at L18, no Rescale:
- budgets = 95,93,93
- required-logQ increment = 30--32 bits
- all exact

Then
\[
SI\_Y4=\texttt{MulRelinScaleInvariantNew}(SI\_Y2,SI\_Y2)
\]
at L18, no Rescale:
- budgets = 64,62,62
- incremental required-logQ = 31 bits
- all exact

Scale metadata is deterministic across cases:
- Y: 43352
- standard raw Y2: 56892
- standard rescaled Y2: 32129
- SI Y2: 27275
- SI Y4: 35478

The largest standard-raw versus SI-Y2 required-logQ gap is 111 bits.

## Lattigo implementation interpretation

Lattigo v6.2.0 implements:
- standard ciphertext-ciphertext tensoring with noise growth depending on operand plaintext/noise norms;
- scale-invariant ciphertext-ciphertext tensoring through quantization by approximately t/Q, with constant-factor noise growth and no mandatory Rescale.

This exactly matches the B173 native behavior.

For ciphertext-plaintext multiplication, \`MulScaleInvariantNew(ct, []uint64)\` still uses standard plaintext tensoring internally, but constructs a scale-one plaintext and preserves the ciphertext scale/level without Rescale. Therefore a high-level grouped generator can use:
- SI ct×ct for binary powers and accumulator combines;
- scale-one no-Rescale ct×pt masks for the public bit factors.

## Consequence

The source-faithful grouped helper's multiplication regime is incompatible with the B158-v2 Y input, but the grouped power chain itself is not intrinsically infeasible.

Classify:
- source-faithful grouped standard tensoring: FAIL
- SI binary power chain: PASS_STRONG
- checkpoint32: sufficient for the tested SI power chain
- k0=16: not justified
- full SI grouped generator: OPEN / HIGHEST PRIORITY

## Recommended next gate

B174 should implement an isolated all-L18 scale-invariant grouped generator for s=8:

1. input Y at L18 from checkpoint32;
2. compute Y2 and Y4 using \`MulRelinScaleInvariantNew\`, no Rescale;
3. construct all three source-equivalent public bit factors at L18 using scale-one vector masks and \`MulScaleInvariantNew\` (no Rescale);
4. verify each factor exactly and record scale/noise;
5. combine factors with two \`MulRelinScaleInvariantNew\` accumulator multiplications, no Rescale;
6. verify final grouped pattern \([1,y,\ldots,y^7]\) exactly at L18;
7. retain Y4 as the leading-power extra;
8. stop before LT / pointwise.

Important:
- do not use the old descending L17/L16/L15 plaintext mask schedule;
- do not Rescale inside grouped generation;
- do not change the logical factorization or mask values;
- use independent exact references for factors and accumulator outputs.

If B174 passes with final grouped budget >=30--40 bits, then grouped and B170 LT8 can coexist naturally at L18 and the next gate can test the SI pointwise multiplication directly.

## State

- B170 PS8192 LT8: PASS_STRONG
- B172 source-faithful grouped: FAIL at first standard square
- B173 SI power chain: PASS_STRONG
- full scale-invariant grouped generator: NOT_RUN
- active candidate: ACTIVE_NATIVE_CANDIDATE
