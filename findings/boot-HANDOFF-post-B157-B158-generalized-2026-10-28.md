# BOOT handoff — post B157 / B158 generalized paper-level completion

Date: 2026-10-28
TRACK_ID: BOOT

## Authoritative BOOT transition

LATEST_COMPLETED: B157_AUDIT

B157:
- SECURITY: PASS at exact HEStd_128_classic point
- CLEAR ALGEBRA: PASS
- NATIVE PRECISION: FAIL
- NATIVE PERFORMANCE: FAIL
- NATIVE VALUE: FAIL

B145:
- algebraic pre-bootstrap adjacent-window cancellation remains
  VALID / POTENTIALLY_NOVEL
- current B145+B152 implementation/backend:
  PARK / FAIL_NATIVE_VALUE

Do not resume local B145/B152 tuning unless a genuinely different 4096-domain
backend can plausibly make the shared-powers+8-LUT block roughly <=20 s with
robust precision.

## Active fresh candidate: B158

Source target:
ePrint 2026/975 sparse-BFV functional bootstrapping.

B158 contribution:
co-pack the growing consecutive-power basis and current binary power inside one
BFV ciphertext, using the two hypercube halves.

Each fused round performs with one ct-ct multiplication:
1. P_k=(1,x,...,x^(k-1)) -> P_2k
2. x^k -> x^(2k)

## Generalized theorem

For power-of-two s<=r:

s=1 or s=2:
- 0 ct-ct Mult
- 0 RowRotation

4<=s<=r/2, s=2^ell:
- ell ct-ct Mult
- ell RowRotation

s=r=2^ell:
- ell ct-ct Mult
- ell-1 RowRotation

The output is exactly the EvalPower power table required by 2026/975, including
the optional x^(s/2) auxiliary output.

Exact exponent-level falsification passed for:
- r in {8,16,32,64,128}
- every power-of-two s<=r

For s>=4, ell ct-ct Mult is optimal under the arithmetic SIMD model because the
target contains x^(s-1) and public linear/rotation operations do not increase
algebraic degree.

Important 9-bit full-row case:
- r=32768=2^15
- source Algorithm 3: 28 ct-ct Mult
- B158: 15 ct-ct Mult + 14 RowRotation
- ct-ct reduction: 46.43%

Corrected KS-like count:
- source: ~28 relin KS
- B158: 15 relin KS + 14 rotation KS ~=29
- net KS-like count increase is about ONE, not two.

The expected value comes from deleting 13 full tensor multiplications + rescale
operations, not from reducing key-switch count.

## Current public implementation bottleneck

Current 2026/975 repository 9-bit m=1:
- online ~2.061 s
- Step1 ~0.693 s
- polynomial evaluation ~1.284 s
- BuildBasis ~1.141 s

BuildBasis remains the largest individual online substage.

## Level/noise state

Same-Q chain:
- source full basis naturally ends around L2
- B158 naturally ends around L3
- B158 therefore carries one extra ~34-bit Q prime through the important
  full-row basis pipeline.

Exact Lattigo canonical-mask analysis:
- max original Algorithm-3 bit-mask log2 canonical norm ~=23.181
- max new B158 regular mask ~=22.733

Therefore the new selectors are not worse in canonical norm than plaintext
masks already used successfully by the source algorithm.

Pinned Lattigo default BFV/RLWE secret is uniform ternary
ring.Ternary{P:2/3}; do NOT use the external LWE h=512 as the BFV ring-secret
weight.

No paper-level noise blocker was found, but native per-stage noise remains
required.

One-Q-prime-smaller chain:
- algebraically/level-wise plausible
- HOLD / secondary experiment only after SAME-Q success.

## Key memory

B158 does not appear to add a distinct Galois element in the complete 9-bit
pipeline.

The row-swap key already exists at low level; B158 promotes it to roughly L18.

Prescout estimate:
- low row key ~3.5 MiB
- promoted L18 row key ~57.5 MiB
- incremental eval-key memory ~54 MiB (~7-8%)

Native BinarySize must verify.

## Prior-art boundary

Direct collision: NOT FOUND.

Strong related prior art exists:
1. ePrint 2023/1407:
   explicitly identifies ct-ct work to compute all powers as OPE bottleneck,
   but uses receiver-provided independent powers-of-two ciphertexts and
   Paterson-Stockmeyer.
2. CCS 2021 / ePrint 2021/1116:
   extremal postage-stamp source powers + multiplication graphs; receiver sends
   multiple encrypted source powers.
3. IBM patent family:
   duplicated SIMD slots + rotate-and-multiply product trees for polynomial
   factor products.

Therefore do NOT claim generic novelty in:
- noticing all-power generation cost,
- source-power multiplication graphs,
- spare-slot rotation/multiplication.

Narrow B158 claim:
an optimal ct-ct-multiplication power-basis generator for the sparse BFV
EvalPower layout, obtained by co-packing the consecutive-power accumulator and
current binary power in the hypercube halves, without additional encrypted
source powers.

NOVELTY: PROMISING_NOT_ESTABLISHED

Broad prior-art micro-search has diminishing value.

## Native gate

A minimal matched native gate is fully specified in:
findings/boot-B158-minimal-native-gate-spec-2026-10-28.md

Cheapest test:
- generate one real noisy Step1 output ciphertext
- clone it into baseline / B158 arms
- compare ONLY MonomialGenExtra(r=32768,wantExtra=true)
- SAME Q chain first
- exact layout/correctness
- level/scale trace
- per-stage noise trace
- isolated paired latency
- promoted row-key BinarySize

Derived value gate from current source timing:
- >=17% BuildBasis speedup: PASS isolated value
- 10-17%: CONDITIONAL
- <10%: FAIL current native value absent separate parameter benefit
- slower: immediate FAIL

DO NOT RUN without explicit PI authorization.

## Current authoritative state

TRACK_ID: BOOT
LATEST_COMPLETED: B157_AUDIT

B145_ALGEBRA_STATUS: VALID / POTENTIALLY_NOVEL
B145+B152_STATUS: PARK / FAIL_NATIVE_VALUE

ACTIVE_FRESH_CANDIDATE: B158
B158_ALGEBRA: PASS
B158_GENERALIZATION: PASS
B158_CTCT_OPTIMALITY: PASS
B158_PAPER_NOISE_BLOCKER: NOT_FOUND
B158_PRIOR_ART: DIRECT_COLLISION_NOT_FOUND / STRONG_RELATED_PRIOR_EXISTS
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_CORRECTNESS: NOT_RUN
B158_NATIVE_NOISE: NOT_RUN
B158_NATIVE_VALUE: NOT_RUN

B158_CODEX_REQUIRED_FOR_DECISIVE_GATE: YES
DO_NOT_AUTO_RUN_CODEX: YES

MAIN_POSITIVE_CANDIDATE:
- no native-positive candidate after B157
- B158 is the strongest paper-level candidate awaiting native validation

NEXT_WHILE_NO_NATIVE_AUTH:
- resume fresh whole-bootstrap source scouting
- do not spend repeated rounds micro-optimizing B158 on paper.
