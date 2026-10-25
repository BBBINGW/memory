# EAI-SYS — EAGLE3 dynamic K0: value/workload gate not met (2026-10-25)

**Scope:** Post-S54 Phase3 negative-result archive. `TRACK_ID=EAI`, `ACTIVE_SUBLINE=EAI-SYS`; `SCOUT-S54_COMPLETED`; `S55_NOT_STARTED`. This is **NOT** a proof of functional incorrectness or general impossibility.

## Hypothesis and smallest decisive test

H: Exact single-layer EAGLE3 K=0 KV-only draft-state maintenance, compared with a true original Full Sync, should yield a *material* real system speedup in plausible dynamic speculative schedules without harming acceptance or later Draft KV. Predeclared E2E signal gate: ~3% or better on a representative K0 workload; separate Native Correctness required.

**Test:** fixed vLLM/Target/Draft, RTX4090, true eager, paired Full Sync / KV-only / No-Spec on three deliberately selected **synthetic schedules**, alongside QL1/8/64 native K0 micro timing; five fresh-process replicates per arm/scenario. Original results were provided as Codex summaries; **raw ZIP not independently audited**.

## What passed

- [FACT — Codex-reported] Native KV parity on QL1/8/64, exact physical future-readable cache, real K0→K>0 recovery, acceptance and complete token sequences matched within reported cases; post-benchmark regression passed.
- [FACT — Codex-reported] K0 micro GPU time reduced **67.63% / 63.10% / 64.72%** (QL1/8/64) with positive paired intervals. The implementation still does full packed QKV; saved work is principally Attention output/o_proj/MLP.

## What failed as a publication-value gate

- [FACT — Codex-reported] In synthetic high-K0 share **82.76%**, KV-only **104.231** vs Full Sync **102.188 tok/s**, relative **+2.000%** (95% CI **[1.952,2.029]%**); this is less than predeclared **~3%** threshold. No-Spec was **105.185 tok/s**, even faster than KV-only in that specific K0-dominant scenario.
- [FACT — Codex-reported] In synthetic K0 shares **31.25%** and **6.45%**, relative E2E gains only **+0.696%** and **+0.090%**, respectively. No production trace shows actual K0 fractions; no production/generalization result.
- [DERIVED] Micro-level 63–68% savings get diluted by Target computation, verification, scheduling and other baseline work (Amdahl); no evidence that extra Kernel Fusion/Q removal/graphs would cross end-to-end gain threshold on a realistic workload.
- [OPEN] Original raw source ZIP located on ephemeral server storage; our independent raw audit PENDING. Research novelty NOT ESTABLISHED: vLLM PR #56441 already contains a KV-only primitive in another Draft architecture, and PR #53426 addresses K0 skip and stale KV problem.

**Dominant obstruction:** limited K0 draft-sync share in full pipeline, no representative real K0 workload, known related KV-only technique. This **does not** rule out future optimized kernels, production traces, alternate hardware or an upstream engineering contribution; no universal upper bound claimed.

## Decision / stopping rule

**STATUS:** `HUMAN_REVIEW / HOLD_WORKLOAD`  
**RESULT:** `PASS_NATIVE_CORRECT (Codex report) / PASS_K0_MICRO_SPEED / FAIL_PREDECLARED_E2E_VALUE_GATE / REAL_WORKLOAD_NOT_ESTABLISHED`  
**NOVELTY:** `NOT_ESTABLISHED`  
**DECISION:** PI accepted `PARK_KV_ONLY_AS_ENGINEERING_RESULT`; no further Phase4, Q-free projection, CUDA Graph, fusion, production integration or synthetic sweeps by default.  
**NEXT_TEST:** None while parked. Reopen only for a realistic production K0 trace or genuinely different valuable mechanism on PI instruction.  
**NEXT_ACTION:** Move to **EAI-P/EAI-010** read-only raw-evidence, quantization accuracy and prior-art audit (separate numbering; do not launch EAI-SYS S55).  
**STATE_UPDATE:** YES if file is committed and reread; see canonical root `STATE.md`.

See [full evidence report](../findings/eai-sys-eagle3-k0-native-phase0-phase3-2026-10-25.md).
