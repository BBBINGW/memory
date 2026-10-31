# BOOT RMFE Post-Raw Baseline Timing-Decomposition Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 4/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

This turn does not implement the post-raw fusion candidate. It closes the minimal execution gate needed to decide whether that candidate is already impossible on latency grounds.

Durable predecessor results:

- Turn 2: `PASS_STATIC_POST_RAW_SINGLE_BOOTKEY_FUSION`.
- Turn 3: `PASS_CONDITIONAL_STATIC_COST_MARGIN`.
- At final capacity C=101, crossing the previously fixed thin-throughput frontier requires reducing the published 4.732 s MultKey block by at least 40.15%.
- Equivalently, retained work plus candidate overhead may consume at most

[
ho_{max}=2.831962/4.732=0.5984704142
]

of the baseline MultKey time.

The highest-information next test is therefore not a candidate implementation. It is a baseline-only timing lower bound.

No native execution was performed in this research turn.

## Source audit

Pinned source for the Aung et al. workflow:

`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

In `src/recryption.cpp::PubKey::thinReCrypt`, the source already contains named timers:

- `AAA_slotToCoeff`;
- `AAA_bootKeySwitch`;
- `AAA_coeffToSlot`;
- `AAA_extractDigitsThin`.

The `AAA_bootKeySwitch` interval contains, in order:

1. canonicalization if needed;
2. mod-down;
3. `reLinearize(recryptKeyID)`;
4. `rawModSwitch`;
5. `newMakeDivisible`;
6. division by (p^{e'});
7. `ctxt = recryptEkey`;
8. `multByConstant(zzParts[1])`;
9. `addConstant(zzParts[0])`.

Thus the existing timers are almost sufficient but do not separate the retained nonlinear/pre-reconstruction portion from the 5->1 reconstruction portion.

`Ctxt::reLinearize` itself uses `HELIB_TIMER_START`, so its function-level time is already observable. `rawModSwitch` and `newMakeDivisible` do not have independent timers in the pinned source.

HElib `timing.h` confirms that `HELIB_NTIMER_START(name)` / `STOP(name)` add arbitrary named timers and `printAllTimers` / `getTime4func` expose them. Therefore adding two nested timing intervals changes no cryptographic semantics.

## Minimal instrumentation

Inside the existing `AAA_bootKeySwitch` interval add exactly two named timers:

### Timer 1: `AAA_preReconstruct`

Start immediately after `AAA_bootKeySwitch` starts and before canonicalization.

Stop after both `zzParts` have been divided by `p2ePrime`, immediately before

`ctxt = recryptEkey;`

This timer therefore includes every operation that the post-raw fusion candidate still has to perform five times:

- optional canonicalization;
- mod-down;
- reLinearize to the recryption key;
- rawModSwitch;
- newMakeDivisible;
- divide by (p^{e'}).

### Timer 2: `AAA_reconstruct`

Start immediately before

`ctxt = recryptEkey;`

and stop immediately after

`ctxt.addConstant(zzParts[0]);`

This timer isolates the exact 5->1 reconstruction component from Turn 2.

The already existing `AAA_coeffToSlot` isolates the branch-local inverse transform that the post-raw candidate replaces by RM10/R8 recovery.

## Hardware-normalized decisive ratio

For each measured five-branch baseline run define:

[
T_{mathrm{MK}}
=
T_{mathrm{S2C}}
+
T_{mathrm{pre}}
+
T_{mathrm{reconstruct}}
+
T_{mathrm{C2S}}.
]

Define the unavoidable retained lower bound

[
ho_{mathrm{ret}}
=
rac{
T_{mathrm{S2C}}+T_{mathrm{pre}}
}{
T_{mathrm{MK}}
}.
]

The post-raw candidate must additionally pay strictly positive time for:

- one reconstruction;
- RM10;
- exact R8 C2S;
- E8 unpack/recovery.

Therefore

[
ho_{mathrm{ret}}ge 0.5984704142
]

is already sufficient to falsify the candidate's C=101 latency target, even under the impossible optimistic assumption that all new recovery work is free.

This is a hardware-normalized lower-bound gate. It does not compare absolute seconds between the paper's Xeon system and the user's server.

## Execution provenance

Existing durable execution context supplies a compatible local workspace:

`/Users/bingwu/Developer/research-orchestrator`

and pinned HElib:

`acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Existing deterministic/source-r=1 RMFE work provides the paper-consistent p=5,w=512,k=5 projection path. The timing task must reuse those verified projection materials and must not substitute five fresh thin encryptions.

Relevant prior artifacts/tasks include:

- `BOOT-RMFE-P5W512-DETERMINISTIC-INSTANCE-MASK-GENERATOR-20261029-R16-01`;
- `BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-CORRECTNESS-CAPACITY-20261029-R24-01`.

The R24 scientific result is not rerun; only its verified source-r=1 lineage may be reused as infrastructure.

## Native task

```text
TASK_ID:
BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01
```

### Required run

- Work in `/Users/bingwu/Developer/research-orchestrator`.
- Use HElib exactly at `acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.
- Fixed parameters: p=5, r=1, m=32768, w=512, k=5, bits=400; single-threaded.
- Reuse the existing deterministic/source-r=1 RMFE instance and actual five projection outputs from one RMFE-packed ciphertext.
- Fresh-encryption thin surrogates are forbidden.
- Do not implement post-raw fusion, RM10, R8 recovery, or any rescue.
- Only add the two named timers described above.
- Keep the existing `AAA_slotToCoeff`, `AAA_bootKeySwitch`, `AAA_coeffToSlot`, and function-level `reLinearize` timers.
- 5 warm-up runs, then 20 measured runs.
- Each measured run begins from clones of the same five valid projected thin ciphertexts.
- Timers are reset per run.
- Report per-run aggregate times across all five branches:
  - `T_slotToCoeff`;
  - `T_preReconstruct`;
  - `T_reconstruct`;
  - `T_coeffToSlot`;
  - `T_bootKeySwitch`;
  - function-level `reLinearize`.
- Define
  `T_MK=T_slotToCoeff+T_preReconstruct+T_reconstruct+T_coeffToSlot`
  and `rho_ret=(T_slotToCoeff+T_preReconstruct)/T_MK`.
- Also report closure error
  [
  epsilon=
  |T_{m bootKeySwitch}-(T_{m pre}+T_{m reconstruct})|
  /T_{m bootKeySwitch}.
  ]
- Preserve correctness: all five scalar thin outputs after stock `thinReCrypt` must decrypt to their original scalar plaintexts for every measured run. `AAA_extractDigitsThin` may execute, but its time is excluded from `T_MK`.
- Produce CSV/JSON for all 20 runs, stdout/stderr logs, exact patch diff, source commit IDs, build/run exit codes, artifact SHA256.

### Statistical decision

Compute the 20 values of (ho_{m ret}) and a deterministic 95% bootstrap confidence interval for the median using a fixed RNG seed recorded in the artifact.

Decision:

- if the lower CI bound is (ge 0.5984704142):
  `FAIL_POSTRAW_TIMING_LOWER_BOUND` and KILL the post-raw fusion family;
- if the upper CI bound is (<0.5984704142):
  `PASS_BASELINE_RETAINED_SHARE_HEADROOM`; do not claim speedup, but proceed to one recovery-cost microbenchmark;
- otherwise:
  `UNCLEAR_THRESHOLD_OVERLAP`; stop without candidate implementation.

If the actual five-projection source lineage cannot be recovered, return `SOURCE_BLOCKED`; do not use a fresh-encryption surrogate.

## Current verdict

```text
RESULT:
  PASS_MINIMAL_NATIVE_TIMING_GATE_DEFINED

EXISTING_HELIB_TIMERS:
  PARTIAL_SUFFICIENCY

SEMANTIC_CODE_CHANGE_REQUIRED:
  NO

NEW_CRYPTOGRAPHIC_IMPLEMENTATION_REQUIRED:
  NO

DECISIVE_HARD_KILL_THRESHOLD:
  rho_ret >= 0.5984704142

TASK_ID:
  BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01

CANDIDATE_STATUS:
  RETAIN_PENDING_BASELINE_TIMING_GATE

INDEPENDENT_RESEARCH_AVAILABLE:
  true

RESEARCH_FRONTIER_EXHAUSTED:
  false
```

## Boundary

This turn establishes execution readiness only. It does not establish latency gain, capacity, DFR, native correctness of the post-raw fusion, or novelty.
