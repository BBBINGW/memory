# BOOT handoff — post B173 audit, B174 currently running

Date: 2026-10-28
TRACK_ID: BOOT

## Authoritative status

- LATEST_COMPLETED: B173_AUDIT
- CURRENT_EXPERIMENT: B174_RUNNING / RESULT_NOT_YET_RECEIVED
- ACTIVE_CANDIDATE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- ACTIVE_GEOMETRY: H=8192, s=8
- ACTIVE_CHECKPOINT: k0=32
- NOVELTY: PROMISING_NOT_ESTABLISHED
- END_TO_END_SPEEDUP: NOT_ESTABLISHED
- FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED
- CODEX: B174 has been launched by PI; do not relaunch unless PI explicitly asks.

Do not treat B174 as completed until the PI supplies the result/artifact and the artifact is independently audited.

## Fixed upstream/source point

Upstream:
\`xiaopeng-stu/bfv-functional-bootstrapping\`

Pinned commit:
\`b113742d83d772fd0d1b353e72ac6e31f2838bea\`

Lattigo:
v6.2.0

Fixed source/security parameters:
- N=32768
- m=1
- degree=65536
- T=65537
- p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048
- LWE h=512

No Q/N/T/p/secret/security relaxation is allowed unless PI explicitly authorizes it.

## Research path and validated results

### B158 original full co-packed state

Original B158 reduced the source-relevant full-basis generator from 28 ct×ct to 15 fused ct×ct, algebraically reaching the ordinary arithmetic depth lower bound.

However B163 established that the original recurrent full-co-packed realization is noise-infeasible at the fixed source parameter point:
- first failure k=8192
- budget=-16
- full-co-packed B158 remains PARKED.

### Selector-noise diagnosis

Exact Lattigo batching reconstruction showed that public 0/1 slot selectors can have very large centered coefficient norms.

For example:
\[
\|M_{4096}\|_1=134115624\approx2^{27}.
\]

B163 measured selector growth closely tracks this norm.

Equivalent coefficient lifts, simple Galois reindexing, bit reversal, Gray/GF(2)-linear reindexing did not provide material rescue.

### Checkpoint-decoupling

Core construction:
\[
S_k=[P_k\mid x^k],\qquad
A_k=[0\mid x^k].
\]

At a checkpoint, retain the already-computed right-half term \(A_k=R S_k\).

After checkpoint:
- \(A_{2k}=A_k^2\) with \`MulRelinScaleInvariantNew\`, no Rescale;
- main selector uses \(M_k\operatorname{RowSwap}(A_k)\);
- right-half variable term uses \(A_k\) directly;
- no further \(R S_k\) selector is required.

This breaks the dirty-main-state -> selector -> next-factor noise feedback.

### B164

Checkpoint k0=64, stop at H=16384.

Native:
\`PASS_B164_CHECKPOINT_HALF_BASIS\`

- S16384 exact, budget 57
- A16384 exact, budget 78
- PH_REP exact, budget 57
- total ct×ct to PH_REP = 22
- RowRotation = 14
- no Rescale

Artifact:
\`BOOT-B164-B158-CHECKPOINT-DECOUPLED-NATIVE-20261028.zip\`

SHA-256:
\`58f042898724d7401ec74e4d3bc616d3515c2322281f62644c59ac99924fa72e\`

### B165

Representative legal-phase sweep:
67/67 PASS.

\`PASS_B165_PHASE_ROBUSTNESS\`

Minimum budget:
52 bits.

Artifact SHA-256:
\`b731e40cdf2f3cc58db609ee150257a4e000f86e686dad0ab0074095eb840c76\`

Thus checkpoint-decoupling is robust across the tested legal-phase sample.

### B166/B167/B168/B169 — four-block H=16384 LT line

B166 failed because PH_REP was destructively DropLevel'ed before LT.

B167 removed pre-drop:
\`PASS_B167_LT_NO_PREDROP\`
but worst raw-L18 LT budget was only about 14--23 bits.

B168 attribution result is INVALID due to missing L18 Galois-key promotion in the diagnostic harness.

B169 fixed the key plan and validly attributed LT noise:
\`PASS_B169_LT_NOISE_ATTRIBUTION\`

Approximate LT required-logQ decomposition:
- dense ct×pt masks: 21--22 bits
- first-stage rot/add: 1 bit
- sum-columns: 11--12 bits
- final row duplication: 0--1 bit

Dominant source:
\`DENSE_CTPT_MASKS\`

### Noise-aware PS aspect-ratio invariant

Let:
- degree bound \(D=2^d\);
- checkpoint \(K=2^c\);
- baby basis \(H=2^h\);
- block count \(s=D/H\).

Checkpoint-decoupled full power/evaluation skeleton:
\[
\text{ct×ct total}=2d-c.
\]

Before the Algorithm-5 pointwise multiply:
\[
2d-c-2.
\]

This is independent of baby-basis exponent \(h\).

For the current D=2^16:
- k0=64 (c=6): projected full skeleton 26 ct×ct;
- k0=32 (c=5): projected full skeleton 27 ct×ct.

Thus changing PS aspect ratio can trade public-linear LT work against ciphertext-noise headroom without changing the core ct×ct count for fixed checkpoint.

### B170 — H=8192, s=8

\`PASS_B170_PS8192_LT8\`
\`HEADROOM=STRONG\`

All three fixed cases:
- PH8192 exact at L18
- PH8192 budget = 87
- raw L18 LT8 exact
- LT8 budget = 52--53
- LT added required bits = 34--35

Native executed:
- main fused ct×ct = 13
- auxiliary square ct×ct = 7
- basis total ct×ct = 20
- LT ct×pt = 8
- LT rotations = 16

Projected:
- grouped ct×ct = 4
- full skeleton = 26 ct×ct

Artifact:
\`BOOT-B170-B158-PS8192-8BLOCK-LT-NATIVE-20261028.zip\`

SHA-256:
\`be1970c874a7a89472be6bceceb1f3d27a141ab43dab78e9ea6b36eeea02e7a8\`

Important systems cost:
raw-L18 s=8 LT requires extra high-level rotation keys; B170 eval-key size was about 1.04 GiB, about +115 MiB over B169.

### B171 — source-faithful grouped generator

\`FAIL_B171_GROUPED\`

PH8192 remained healthy, but source-faithful \`MonomialGenExtraPrecomp(s=8)\` failed.

Y_REP budget:
105--107 bits.

Returned \(Y4=y^4\) already failed at L16 with budget -16.

Artifact SHA-256:
\`6d78f48628d56544ce413cfeedbfc030a6447aad4a3245f0d2894876816c6081\`

### B172 — checkpoint32 attempt

Checkpoint moved from 64 to 32.

It successfully made the clean auxiliary and Y_REP substantially cleaner:
- A32 budget = 372--373
- Y_REP budget = 125

But the first source-faithful grouped standard square
\[
Y\to Y^2
\]
still failed immediately:
- standard \`MulRelinNew + Rescale\`
- Y required around 524
- Y2 required around 631 after Rescale
- budget=-16

Thus checkpoint32 worked, but checkpoint placement is not the primary grouped bottleneck.

B172:
\`FAIL_B172_POWER_Y2\`

Artifact:
\`BOOT-B172-B158-PS8192-CHECKPOINT32-GROUPED-NATIVE-20261028.zip\`

SHA-256:
\`3f4d051f81b14841f2127a0895fea0a658e72748836ba3f0a2adb4156155813c\`

### B173 — standard vs scale-invariant tensoring

This is the latest completed/audited result.

Artifact:
\`BOOT-B173-B158-GROUPED-STANDARD-VS-SI-SQUARE-20261028.zip\`

SHA-256:
\`1bff68640c185038868c34181c6d0d11bc057659cbde4b1c98cf90a204c4498c\`

\`PASS_B173_SCALE_INVARIANT_POWER_CHAIN\`
\`HEADROOM=STRONG\`

Common Y:
- L18
- budget 124--125

Standard branch:
\[
Y^2=\texttt{MulRelinNew}(Y,Y)
\]
already fails before Rescale:
- raw L18 required-logQ about 665
- budget=-16
- all slots wrong

A subsequent Rescale only drops logQ and required-logQ by about 34 bits each, keeping budget=-16.

Therefore standard tensoring, not Rescale, causes the source-faithful grouped failure.

Scale-invariant branch:
\[
SI\_Y2=\texttt{MulRelinScaleInvariantNew}(Y,Y)
\]
- exact
- budget 93--95

\[
SI\_Y4=\texttt{MulRelinScaleInvariantNew}(SI\_Y2,SI\_Y2)
\]
- exact
- budget 62--64

Each SI square adds only about 30--32 required-logQ bits.

Deterministic scale metadata from B173:
- Y scale mod T = 43352
- standard raw Y2 = 56892
- standard rescaled Y2 = 32129
- SI Y2 = 27275
- SI Y4 = 35478

Conclusion:
\[
\boxed{\text{source-faithful grouped standard tensoring is incompatible with B158-v2 Y, while SI power generation is strongly feasible.}}
\]

## Current experiment B174

The PI has already launched B174 in Codex.

B174 hypothesis:
build the entire s=8 grouped generator at L18 using:
- SI ct×ct binary-power squares;
- source-equivalent public bit masks at L18 with scale-one plaintext and no Rescale;
- two SI ct×ct accumulator combines;
- no Rescale anywhere inside grouped generation.

Logical factorization remains unchanged:
\[
F_0=D_0+C_0y,
\quad
F_1=D_1+C_1y^2,
\quad
F_2=D_2+C_2y^4,
\]
\[
ACC_1=F_0F_1,
\qquad
G=ACC_1F_2.
\]

Target grouped plaintext:
\[
[1,y,y^2,y^3,y^4,y^5,y^6,y^7]
\]
periodically packed.

Expected native operation counts if successful:
- basis ct×ct = 21
- grouped power SI ct×ct = 2
- grouped accumulator SI ct×ct = 2
- grouped total ct×ct = 4
- grouped ct×pt = 3
- grouped Rescale = 0
- total ct×ct to grouped = 25
- projected pointwise = 1
- projected leading = 1
- projected full skeleton = 27

B174 is NOT completed yet.

Do not infer PASS/FAIL before artifact receipt and audit.

## B174 decision tree when result arrives

1. First independently audit:
   - outer ZIP SHA-256;
   - all internal SHA256SUMS;
   - parent source lineage against audited B173;
   - B173->B174 diff scope;
   - actual operation counts;
   - absence of hidden Rescale/parameter changes.

2. If B174 PASS:
   - inspect factor0/1/2, ACC1, final GROUPED budgets and scale metadata;
   - if final grouped budget >=40, classify strong;
   - next candidate gate should combine B170 LT8 and B174 grouped at L18 and test SI pointwise multiplication only;
   - do not immediately benchmark.

3. If B174 FAIL at a public factor:
   - identify which mask and coefficient-norm/scale-matching mechanism dominates;
   - do not automatically change Q.

4. If factors PASS but ACC1/final accumulator fails:
   - compare SI accumulator required-logQ increments with the validated 30--32 bit SI square behavior;
   - consider multiplication tree/order or PS geometry only after exact attribution.

5. Do not return to k0=16 unless a concrete quantitative deficit justifies it.

## Key research insight accumulated so far

The strongest emerging contribution is not “B158 with fewer multiplications” alone.

It is a coupled design:
\[
\boxed{
\text{checkpoint-decoupled recurrent basis}
+
\text{noise-aware PS aspect ratio}
+
\text{scale-invariant multiplication scheduling}
}
\]

Empirically:
- checkpoint decoupling breaks selector feedback;
- PS aspect ratio H=8192 restores LT headroom without changing fixed-checkpoint ct×ct count;
- standard grouped tensoring is catastrophically incompatible with the new basis;
- SI tensoring restores the power chain with predictable ~31-bit increments.

This coupled mechanism is the current highest-value BOOT candidate.

## Research discipline for continuation

- User is PI; assistant is research student.
- Smallest falsifiable claim -> cheapest decisive test -> minimal verification.
- Do not run Codex/native/server experiments without PI authorization.
- Do not change security parameters to rescue a result.
- Distinguish algebraic PASS, native mechanism PASS, representative robustness, full end-to-end correctness, speedup, and novelty.
- Audit every Codex ZIP before accepting its summary.
- Keep other research tracks isolated.

## Relevant findings already saved

- \`findings/boot-B163-native-artifact-audit-2026-10-28.md\`
- \`findings/boot-B158-selector-norm-lift-layout-gate-2026-10-28.md\`
- \`findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md\`
- \`findings/boot-B164-native-artifact-audit-2026-10-28.md\`
- \`findings/boot-B165-phase-robustness-artifact-audit-2026-10-28.md\`
- \`findings/boot-B166-native-audit-level-policy-diagnosis-2026-10-28.md\`
- \`findings/boot-B167-native-audit-and-LT-noise-bottleneck-2026-10-28.md\`
- \`findings/boot-B168-artifact-audit-keyplan-bug-2026-10-28.md\`
- \`findings/boot-B169-audit-and-noise-aware-PS-aspect-ratio-2026-10-28.md\`
- \`findings/boot-B170-audit-PS8192-strong-and-next-alignment-gate-2026-10-28.md\`
- \`findings/boot-B171-audit-grouped-power-failure-and-checkpoint32-rescue-2026-10-28.md\`
- \`findings/boot-B172-audit-standard-square-bottleneck-2026-10-28.md\`
- \`findings/boot-B173-audit-scale-invariant-grouped-power-rescue-2026-10-28.md\`

