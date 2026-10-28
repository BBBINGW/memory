# BOOT — B164 checkpoint-decoupled half-basis native artifact audit

Date: 2026-10-28  
TRACK_ID: BOOT

## Artifact

Artifact:
\`BOOT-B164-B158-CHECKPOINT-DECOUPLED-NATIVE-20261028.zip\`

User/Codex-reported SHA-256:

\`58f042898724d7401ec74e4d3bc616d3515c2322281f62644c59ac99924fa72e\`

Independent audit of the uploaded ZIP produced the same SHA-256 exactly.

All 25 entries listed in the internal \`SHA256SUMS\` verified successfully.

The packaged B164 parent source has SHA-256:

\`eae7e82401e51c7799dc359374b31cff9d8928415ce841f66ee7d9dd5fa9b01c\`

This is byte-for-byte identical to the previously independently audited B163 source
\`/source/main.b163.go\`.

The packaged top-level and source-copy B163→B164 diffs are identical.

## Fixed source and environment

Upstream:

\`xiaopeng-stu/bfv-functional-bootstrapping@b113742d83d772fd0d1b353e72ac6e31f2838bea\`

Toolchain:
- Go 1.25.0
- Lattigo v6.2.0

Host:
- AMD Ryzen Threadripper PRO 7975WX
- Ubuntu/Linux 6.8.0-124
- 64 logical CPUs
- about 251 GiB RAM

Fixed B163/B164 cryptographic parameters:
- N=32768
- m=1
- r=32768
- degree=65536
- T=65537
- p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048
- LWE h=512
- checkpoint k0=64
- last main stage=16384
- no bootstrap/refresh
- no selector/main/aux Rescale
- main and auxiliary ct×ct use \`MulRelinScaleInvariantNew\`

The corrected L18 row key from B162/B163 is reused. No new rotation element is introduced.

## Native result

\`STATUS = PASS_B164_CHECKPOINT_HALF_BASIS\`

\`HEADROOM = STRONG\`

Exact final objects:
- S16384: 0/32768 mismatches, required_logQ=592, budget=57
- A16384: 0/32768 mismatches, required_logQ=571, budget=78
- L_H=S_H-A_H: 0/32768 mismatches, budget=57
- P_H^rep=L_H+RowSwap(L_H): 0/32768 mismatches, required_logQ=592, budget=57

Final minimum coefficient-noise budget is 57 bits.

## Exact operation counts

- main fused ct×ct = 14
- auxiliary ct×ct squares = 8
- total ct×ct to P_H^rep = 22
- RowRotation = 14
- M-selector ct×pt = 14
- R-selector ct×pt = 7
- R-selector after checkpoint k=64 = 0
- selector Rescale = 0
- fused Rescale = 0
- auxiliary Rescale = 0

The source audit confirms that for k>=64 the factor is built as

\[
M_k\cdot\operatorname{RowSwap}(A_k)+A_k+\text{public constant},
\]

rather than using \(R S_k\) again.

Auxiliary update is

\[
A_{2k}=A_k^2
\]

with \`MulRelinScaleInvariantNew\`.

The gate stops before Algorithm 5; the process exit status 2 is an intentional terminal PASS panic, not a correctness failure.

## Noise trajectory

Auxiliary required_logQ / budget:

- k=64: 325 / 324
- k=128: 355 / 294
- k=256: 386 / 263
- k=512: 417 / 232
- k=1024: 447 / 202
- k=2048: 478 / 171
- k=4096: 509 / 140
- k=8192: 540 / 109
- k=16384: 571 / 78

Thus isolated auxiliary squares increase required_logQ by about 30–31 bits per doubling, essentially matching the paper-level forecast.

Post-checkpoint main-state required_logQ / budget:

- k=64: 309 / 340
- k=128: 375 / 274
- k=256: 406 / 243
- k=512: 437 / 212
- k=1024: 467 / 182
- k=2048: 498 / 151
- k=4096: 530 / 119
- k=8192: 560 / 89
- k=16384: 592 / 57

For comparison, B163 first failed at k=8192 with budget -16. B164 has +89 bits at the same stage, a 105-bit recovery, and continues to k=16384 with +57 bits.

This strongly validates the mechanism-level hypothesis that late selector multiplication on the dirty recurrent B158 state was a major source of the B163 failure, and that checkpoint-decoupling breaks that feedback.

## Important limitation

The B164 native gate uses the deterministic source point:

- message=0
- phase_error=+1
- therefore x=1

This was deliberate for an isolated noise-mechanism gate and is directly comparable with B163.

It is not yet a certificate for the entire legal phase/correction domain. For the 9-bit setting,
\[
x=\Delta m+e,\qquad \Delta=\lfloor T/p\rfloor=128,
\]
with \(m\in\mathbb Z_{512}\) and the default legal error range \(|e|<64\).

The power-basis plaintext values, and hence BFV multiplication noise, can be message/phase dependent. Therefore B164 establishes mechanism feasibility at the pinned x=1 point, not complete input-domain feasibility.

## State decision

- B163 full co-packed B158: remains PARKED.
- B164 checkpoint-decoupled half-basis mechanism: PASS_NATIVE_MECHANISM.
- B158_CHECKPOINT_DECOUPLED_HALF_BASIS: promote from PROMISING_PAPER_GATE to ACTIVE_NATIVE_CANDIDATE.
- Full Algorithm-5 feasibility: NOT YET ESTABLISHED.
- Input-domain robustness: NOT YET ESTABLISHED.
- End-to-end speedup: NOT YET ESTABLISHED.
- Novelty: PROMISING_NOT_ESTABLISHED.

## Recommended next gate

Before implementing the four-block ParallelLT, run a small fixed-parameter phase-value robustness sweep of the B164 half-basis gate.

The next experiment should keep all cryptographic parameters and k0=64 fixed and evaluate representative legal phase values, including boundary and seeded-random cases, while recording final and minimum per-stage noise budgets.

Only if checkpoint-decoupling remains correct with positive headroom across that sweep should the project spend implementation effort on the modified four-block ParallelLT.

No performance benchmark is justified yet.
