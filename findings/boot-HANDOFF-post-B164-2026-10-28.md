# BOOT handoff — post B164 audit

Date: 2026-10-28

## Authoritative state

- TRACK_ID: BOOT
- LATEST_COMPLETED: B164_AUDIT
- B163 full co-packed B158: PARKED
- B164 checkpoint-decoupled half-basis: PASS_NATIVE_MECHANISM
- ACTIVE_CANDIDATE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- FULL_ALG5_FEASIBILITY: NOT_ESTABLISHED
- INPUT_DOMAIN_ROBUSTNESS: NOT_ESTABLISHED
- END_TO_END_SPEEDUP: NOT_ESTABLISHED
- NOVELTY: PROMISING_NOT_ESTABLISHED

## B164 native PASS

Fixed source/security point:
- xiaopeng-stu/bfv-functional-bootstrapping@b113742d83d772fd0d1b353e72ac6e31f2838bea
- N=32768, m=1, degree=65536, T=65537, p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048, h=512
- k0=64
- no Rescale in selector/main/aux paths
- main/aux ct×ct use MulRelinScaleInvariantNew

Artifact:
BOOT-B164-B158-CHECKPOINT-DECOUPLED-NATIVE-20261028.zip

SHA-256:
58f042898724d7401ec74e4d3bc616d3515c2322281f62644c59ac99924fa72e

Independent audit:
- outer hash matches
- all 25 SHA256SUMS entries pass
- B164 parent source is byte-identical to independently audited B163 source
- source confirms no R*S_k after checkpoint
- no hidden Rescale/DropLevel/refresh in B164 gate
- intentional terminal PASS exit before Algorithm 5

Final native metrics:
- S16384 0/32768, budget 57
- A16384 0/32768, budget 78
- L_H 0/32768, budget 57
- P_H^rep 0/32768, budget 57
- minimum final budget 57
- main fused ct×ct 14
- auxiliary squares 8
- total ct×ct to P_H^rep 22
- RowRotation 14
- R selector after k0 0
- all Rescale counts 0

Noise mechanism:
aux required_logQ trajectory 325,355,386,417,447,478,509,540,571, i.e. about +30/+31 bits per auxiliary square.
Main budget at k8192 is +89 versus B163 -16; main budget at k16384 is +57.

## Important limitation

B164 used deterministic message=0, phase_error=+1 => x=1.

For the 9-bit source setting, legal phase values are generated as
x = 128*m + e mod 65537,
m in Z_512 and |e|<64 by default.

Thus B164 proves mechanism feasibility at the pinned x=1 point and validates the checkpoint-decoupling noise hypothesis, but does not yet prove robustness over the legal phase domain.

## Next gate

B165 should be a fixed-parameter B164 half-basis phase-value robustness sweep before implementing the four-block ParallelLT.

Suggested cases should include:
- x=1 baseline
- e-boundary values around ±63 for m=0
- representative message centers and boundaries such as m=1,127,255,256,511 with e in {0,+63,-63}
- a small deterministic seeded-random set from the legal phase generator

For each case record:
- correctness of S16384, A16384, L_H, P_H^rep
- minimum per-stage budget
- final S/A/P budgets
- first failing object/stage if any

Keep all security/parameter choices and k0=64 unchanged.
Do not implement modified ParallelLT or benchmark until B165 passes with positive headroom across the selected sweep.
