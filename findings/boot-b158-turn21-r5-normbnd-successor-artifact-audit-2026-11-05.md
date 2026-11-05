# BOOT / B158 — Research Turn 21/25
## R5 NormBnd successor independent audit — preserved-artifact access boundary

Date: 2026-11-05 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE / VALUE_GATE blocked on Step-2 correctness
TASK_ID: BOOT-B158-STEP2-NORMBND-GATE-SUCCESSOR-20261104-R5
TASK_IMMUTABILITY: DO_NOT_RERUN
TURN_ACCOUNTING: this finding is Research Turn 21/25; Turn 20 is the last previously counted turn.

## Durable authority recovery

GitHub Notes repository BBBINGW/memory main is reachable for directory listing and writes. The latest remotely persisted scientific findings for this logical session before this audit are:

- Turn 19: findings/boot-b158-turn19-r4-mfac-context-assertion-static-repair-2026-11-04.md
  - blob 0330b0094289bb9c70a320b8d4d87ef78f4f90e1
  - commit 8c07d7883f2c16749d96d1cdf2bee6a9c5767f82
- Turn 20: findings/boot-b158-turn20-r4-summary-level-unique-mfac-failure-candidate-2026-11-04.md
  - blob 5c40ede90dc419bb96d72145a89f8f9223041455
  - commit 40024a78aa2f17bf0ded12fd4fbeafc3a207b1e3

Turn 20 established only a summary-level uniqueness result: among the R4 fields shown in its compact diagnostic, mfac was the only remaining visible mismatch candidate. It explicitly did NOT establish the exact R4 exit predicate and did NOT establish full dirty-lift correctness.

The remote STATE.md currently contains no R5 task identifier or R5 result payload. No post-Turn-20 GitHub Notes finding containing R5 scientific evidence was present before this write.

## Independent R5 execution-status verification

The current Research Orchestrator page reports:

- TASK_ID = BOOT-B158-STEP2-NORMBND-GATE-SUCCESSOR-20261104-R5
- task status = COMPLETED
- audit status = DELIVERED
- Codex/native = IDLE
- task is the audit task attached to the same logical Turn 21 migration
- preserved native stdout path =
  /Users/bingwu/Developer/research-orchestrator/logs/codex/BOOT-B158-STEP2-NORMBND-GATE-SUCCESSOR-20261104-R5/remote-artifact/logs/native.stdout
- latest milestone timestamp = 2026-11-04T08:05:22.797Z
- migration event records sameLogicalSession=true, logicalTurn=21, auditTask=R5, doNotRerun=true.

This verifies that R5 completed and that a preserved artifact bundle exists locally. It does NOT establish any scientific PASS/FAIL predicate.

## Preserved-artifact accessibility audit

The current research surface does not expose the immutable R5 artifact bytes:

1. GitHub Notes listing contains no R5 finding or artifact.
2. Remote STATE.md contains no R5 identifier/result payload.
3. Library/conversation file search contains no R5 native.stdout, result.json, canary source, or equivalent raw result.
4. Browser access to the local Orchestrator exposes the preserved native.stdout path but not its contents.
5. The local /Users/bingwu/... path is not mounted in the current execution container.
6. The prior ChatGPT transport that may have received the audit payload is blocked from read access by browser host security; no bypass was attempted.

Therefore the preserved artifacts are known to exist, but their bytes are not currently available to this independent auditor.

## Scientific verdict

R5_EXECUTION_COMPLETED = TRUE
R5_IMMUTABLE = TRUE
R5_DO_NOT_RERUN = TRUE

R5_INDEPENDENT_RAW_AUDIT = BLOCKED_ARTIFACT_BYTES_UNAVAILABLE

NORMBND_REPAIR_PASS = UNKNOWN
FIRST_REAL_FAILING_INTERFACE = UNKNOWN
FULL_DIRTY_LIFT_REACHED = UNKNOWN
L0_L3_EQUALITY_REACHED = UNKNOWN

No scientific conclusion is inferred from the word COMPLETED or from the task name.

In particular, the Turn-19 static result remains valid:
- exact-literal mfac==1 is not a source-valid portable contract;
- the pinned HElib expression can evaluate to 1.0000000000000002 (0x1.0000000000001p+0);
- a successor should serialize the runtime NormBnd/mfac value and compare it under an explicit ULP/tolerance rule while using the runtime value in capacity/noise calculations.

But that static repair must NOT be projected onto R5 as a native PASS until R5 raw output is read.

Likewise, R4's last audited state remains:
FAIL_CONTEXT_ASSERTION / FULL_DIRTY_LIFT_UNTESTED.
That state must NOT be projected onto R5 either.

## Narrow next decisive research unit

Do NOT launch a new native task.

The cheapest decisive unit is artifact-only and non-executing:

1. Materialize/read the immutable R5 preserved artifact bundle, starting with the exact native.stdout path already recorded by the Orchestrator.
2. Read the corresponding immutable result/manifest and canary source from the same preserved bundle if present; record hashes before interpretation.
3. Identify the exact NormBnd predicate and its observed decimal/hexfloat value.
4. Determine the first stage after the NormBnd/context gate that actually fails, using the canary's stage order rather than inferred summaries.
5. Determine whether execution entered the full GR(625,d) dirty-lift comparison; if it did, record the first mismatching coordinate/value and whether the L0..L3 comparison was reached.
6. Stop after this raw audit. Do not run Algorithm 4, security/DFR, benchmarking, or a new successor task.

Only after those immutable bytes are audited is a new experiment scientifically admissible. Its scope must be restricted to the single first real failing interface exposed by R5; no broad Step-2 rerun is justified.

## Gate state

CORRECTNESS_GATE: BLOCKED_ON_R5_RAW_AUDIT
SECURITY_GATE: PENDING
VALUE_GATE: PENDING
AUDIT_GATE: BLOCKED_ON_ARTIFACT_ACCESS
NOVELTY_STATUS: PREFLIGHT
PAPER_READINESS: NOT_READY
RESEARCH_FRONTIER_EXHAUSTED: FALSE
