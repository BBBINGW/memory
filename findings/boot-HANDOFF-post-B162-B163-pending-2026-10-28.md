# Resume Independent FHE Bootstrapping Research — Post B162 Audit / B163 Pending Codex

Date: 2026-10-28
TRACK_ID: BOOT

## Authoritative status

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

CURRENT_STATUS: ACTIVE_RESEARCH / PAPER_LEVEL_SCOUTING_ALLOWED
MAIN_ACTIVE_CANDIDATE: B158
B158_NATIVE_FEASIBILITY: UNRESOLVED
B158_NOVELTY: PROMISING_NOT_ESTABLISHED

Do not modify SHIP, PURE-FHE, CGS, VFHE, EXPLORE, EAI, or other tracks.

---

## B157 / B145+B152 final status

B145 adjacent-window pre-bootstrap overflow cancellation remains:

- ALGEBRA: VALID
- NOVELTY: POTENTIALLY_NOVEL

However the B145+B152 practical one-FBS backend is parked.

B157 exact secure native point:
- HEStd_128_classic: PASS
- N=65536
- depth=32
- scaleBits=50
- NumLargeDigits=33
- Q=1650 bits
- P=60 bits
- QP=1710 bits
- no output repacking

B157 native result:
- PASS_SECURITY
- PASS_CLEAR_ALGEBRA
- FAIL_NATIVE_PRECISION
- FAIL_NATIVE_PERFORMANCE
- FAIL_NATIVE_VALUE

Key performance fact:
- fair baseline: 48.99471343 s
- candidate: 288.337000858 s
- shared powers + 8 LUTs: 259.090102449 s
- non-LUT core: about 29.2469 s
- to beat baseline, LUT block would need <=19.7478 s
- required LUT-block speedup: about 13.12x

Decision:
B145+B152 = PARK / FAIL_NATIVE_VALUE

Do not spend further BOOT rounds on local B145+B152:
- scale tuning
- NumLargeDigits tuning
- output repacking
- local Hermite tuning
- direct projection keys

Reopen B145 only if a genuinely different 4096-domain one-FBS backend appears.

---

## B158 active fresh candidate

Source framework:
ePrint 2026/975, sparse BFV functional bootstrapping.

B158 idea:
co-pack in one BFV ciphertext:
- growing consecutive-power basis accumulator
- current binary power x^(2^i)

Use the two BFV hypercube halves so that each ct-ct multiplication simultaneously:
1. extends P_k=(1,x,...,x^(k-1)) to P_2k
2. updates x^k -> x^(2k)

For r=2^ell >=4:
- B158 ct-ct Mult = ell
- B158 RowRotation = ell-1
- first k=1 doubling uses original duplicated input, so no RowRotation

For r=32768=2^15:
- original 2026/975 EvalPower: 28 ct-ct Mult
- B158: 15 ct-ct Mult + 14 RowRotation
- ct-ct Mult reduction: 46.43%

Formal lower bound:
the output contains x^(r-1), so any arithmetic SIMD circuit starting from degree-1 inputs and using only linear public operations plus ct-ct multiplication has multiplicative depth at least:

ceil(log2(r-1)) = ell.

Hence any such circuit needs at least ell ct-ct multiplications.

B158 uses exactly ell.

Status:
- ALGEBRA: PASS
- BATCH GENERALIZATION: PASS
- DROP-IN FULL-ROW EvalPower(ct,r,1) INTERFACE: PASS
- AUXILIARY x^(r/2) OUTPUT: PASS
- CTCT_MULT_LOWER_BOUND: PASS / OPTIMAL
- PRIOR_ART_DIRECT_COLLISION: NOT_FOUND
- CLOSE_CONCEPTUAL_PRIOR: YES
- NOVELTY: PROMISING_NOT_ESTABLISHED

Important prior-art boundary:
do NOT claim generic novelty for "spare SIMD slots + rotation + multiplication".
IBM rotate-and-multiply polynomial-evaluation patent family is conceptual prior.
The defensible narrow claim is the B158 state invariant:
[growing consecutive-power basis | current binary power].

---

## B159-B161 correction: old k=4 failures were INVALID

B159 originally reported FAIL_NOISE at k=4.
B160 originally reported FAIL_SCALE_INVARIANT_RESCUE at k=4.
B161 originally reported FAIL_B161_HYBRID_RESCUE at k=4.

Independent audit showed all three were contaminated by the same key-planning bug.

The new B158 RowRotation first occurs on a high-level ciphertext (~L17), but the old 2026/975 level-aware key planner generated the row-rotation Galois key only at L2.

Lattigo Automorphism -> GadgetProduct internally clips:

    levelQ = min(requestedLevel, gadgetCt.LevelQ())

Thus an L2 Galois key was being used for an L17 ciphertext.

Observed signature:
- S2@L17 exact
- immediately after RowRotation(S2), before selector multiplication:
  almost all slots wrong
  noise budget catastrophic

Therefore:

B159-B161_K4_NOISE_CONCLUSIONS = INVALIDATED_BY_KEY_LEVEL_BUG

They remain useful only for:
- early recurrence implementation sanity
- operation-count prefix
- unrotated selector branch behavior

Do not cite their k=4 failures as evidence against B158.

---

## B162 corrected high-level row-key result

B162 fixed the row-rotation key planner.

B158 row key:
- key level L18
- first actual B158 use L17

Key memory:
- old total evaluation-key size:
  767,060,320 bytes = 731.53 MiB
- corrected total:
  823,685,344 bytes = 785.53 MiB
- increase:
  56,625,024 bytes = 54.00 MiB

Rotation sanity:
- S2@L17: 0/32768 mismatches
- S2 noise budget: 560 bits
- RowRotation(S2): 0/32768 mismatches
- RowRotation noise budget: 560 bits
- all 9 RowRotations reached before stop: exact
- rotations did not reduce the measured noise budget

Therefore the key-level bug is conclusively fixed.

B162 arithmetic schedule was the B161 hybrid:
- selector ct-pt Mul + Rescale
- factor assembly
- fused MulRelinScaleInvariantNew
- no fused ct-ct Rescale

Valid stage trace:

k=1:
- logQ 615
- required 25
- budget 590

k=2:
- logQ 615
- required 55
- budget 560

k=4:
- logQ 581
- required 84
- budget 497

k=8:
- logQ 547
- required 114
- budget 433

k=16:
- logQ 513
- required 145
- budget 368

k=32:
- logQ 479
- required 175
- budget 304

k=64:
- logQ 445
- required 204
- budget 241

k=128:
- logQ 411
- required 235
- budget 176

k=256:
- logQ 377
- required 265
- budget 112

k=512:
- logQ 343
- required 295
- budget 48

k=1024:
- logQ 309
- required 325
- budget -16
- 32768/32768 mismatches

B162 actual before stop:
- ct-ct: 10/15
- RowRotation: 9/14

Decision:
B162_B161_HYBRID = VALID_FAIL_AT_K1024

Root cause shape:
- required-logQ grows ~29-31 bits per doubling
- selector Rescale consumes ~34 bits of Q per doubling
- total budget therefore falls ~63-65 bits per doubling

This hybrid schedule is not viable through all 15 doublings.

---

## B163 — decisive pending native gate

B163 is NOT a parameter-tuning rescue.

It is the corrected rerun of the original B160 schedule, which was never validly tested because its old k=4 failure was caused by the L2 row key.

B163 must combine:

1. corrected L18 B158 RowRotation key
2. B158 exact recurrence
3. scale-one / NO-RESCALE selector plaintext products
4. MulRelinScaleInvariantNew for fused ct-ct multiplication
5. NO selector Rescale
6. NO fused ct-ct Rescale

Therefore the B158 recurrence should avoid the systematic ~34-bit Q loss per doubling seen in B162.

Fixed parameters remain:
- N=32768
- m=1
- r=32768
- degree=65536
- T=65537
- p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048
- h=512

Do NOT:
- add Q primes
- increase N
- weaken security
- change T
- change secret
- change packing
- alter Step1/BatchLT/tail

Decisive question:

Can the corrected no-rescale + scale-invariant recurrence complete all 15 doublings while keeping exact slots and positive noise budget?

B163_STATUS: PENDING_CODEX_QUOTA
Do not auto-run until PI says Codex quota is restored.

Interpretation after B163:

If corrected B163 fails early and required-logQ growth clearly cannot fit within the fixed L18 / ~649-bit modulus:
    PARK B158 practical line.

If corrected B163 reaches very late (e.g. 8192/16384) but fails:
    consider only a sparse/strategic rescale schedule.
    Do NOT add Q primes automatically.

If corrected B163 completes:
    run matched BuildBasis performance gate;
    only after that revisit one-Q-prime reduction.

---

## Codex unavailable period: research mode

Until Codex quota returns:

DO NOT:
- launch B163
- run server/native/GPU experiments
- spend rounds locally tuning B158 noise parameters
- change B158 state based on hypothetical native behavior

DO:
- continue fresh BOOT source scouting / paper-level research
- prioritize whole-bootstrap structural bottlenecks
- prefer source -> algebra -> correctness -> security/value gates
- search for candidates that do not depend on B163
- use B158 techniques as inspiration where relevant, but do not mutate its native status
- avoid repeating already-PARKed micro-optimizations

Fresh-scout priority:
1. structural removal/merging of an entire bootstrap stage
2. sequential-depth reduction with no hidden work explosion
3. key/memory bottlenecks with cryptographic structure, not generic compression
4. new representations that change the bootstrap DAG
5. source-level open problems from 2026 papers

Keep B163 as the highest-priority native action when Codex quota returns.

---

## Relevant findings

- findings/boot-B157-depth32-native-audit-2026-10-28.md
- findings/boot-B158-copacked-optimal-evalpower-2026-10-28.md
- findings/boot-B158-level-value-gate-2026-10-28.md
- findings/boot-B158-selector-noise-prescout-2026-10-28.md
- findings/boot-B158-formal-recurrence-optimality-prior-art-2026-10-28.md
- findings/boot-B158-prior-art-audit-closure-2026-10-28.md
- findings/boot-B159-native-artifact-audit-2026-10-28.md
- findings/boot-B160-native-artifact-audit-2026-10-28.md
- findings/boot-B161-rowrotation-key-level-audit-2026-10-28.md
- findings/boot-B162-native-artifact-audit-2026-10-28.md
- findings/boot-B163-corrected-b160-no-rescale-gate-2026-10-28.md

## Final authoritative state

TRACK_ID: BOOT
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO

B145+B152: PARK / FAIL_NATIVE_VALUE
B145_ALGEBRA: VALID / POTENTIALLY_NOVEL

B158:
- ALGEBRA PASS
- OPTIMAL CT-CT MULT COUNT PASS
- NOVELTY PROMISING_NOT_ESTABLISHED
- PRACTICAL NATIVE FEASIBILITY UNRESOLVED

B159-B161 k=4 failures:
- INVALIDATED by under-leveled RowRotation key

B162:
- corrected key PASS
- B161 hybrid VALID FAIL at k=1024

B163:
- corrected no-rescale scale-invariant gate
- PENDING_CODEX_QUOTA
