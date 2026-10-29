# BOOT Pending Native Task — Cross-Session Provenance

Date: 2026-10-29
Purpose: durable provenance only; NOT a handoff and NOT a scientific result.

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

task_id: BOOT-RMFE-P5W512-CONSECUTIVE-R8-MERGED-MIDDLE-FIXEDQ-NATIVE-20261029-R21-RECOVERY-01
logical_task: BOOT-RMFE-P5W512-CONSECUTIVE-R8-MERGED-MIDDLE-FIXEDQ-NATIVE-20261029-R20-01
origin_session: 密码学 11.0
origin_session_id: 7eef5c84-77e9-4683-81d4-60c462debf0c
origin_turn: 21/25
working_directory: /Users/bingwu/Developer/research-orchestrator
execution_backend: local orchestrator executor using ChatGPT/Codex included-quota backend
codex_model: gpt-5.6-sol
codex_reasoning: xhigh
zero_api_billing: true
paid_api_fallback: forbidden
silent_model_or_reasoning_downgrade: forbidden
native_pid: 18809
codex_wrapper_pid: 17657
start_time_local: 2026-10-29 12:27:09 +08:00
start_time_utc: 2026-10-29T04:27:09Z
last_observed_status: RUNNING_HEALTHY / WAITING_CODEX
last_observed_phase: HElib ContextBuilder -> ThinRecryptData -> ThinEvalMap -> ThinStep1Matrix -> NTL TraceMap
last_observed_progress: UNKNOWN
progress_protocol: ORCHESTRATOR_PROGRESS_FILE
instrumentation_commit: d9d6827
adapter_commit: 0c89159329663cc739c62cc1940135431cd9dee1
native_run_log_last_observed: native-run.log, 0 bytes
evidence_directory_last_observed: empty / not yet flushed
result_delivered: false
evidence_status: PENDING
audit_status: PENDING
do_not_rerun: true

## Original hypothesis / fixed gate

The corrected consecutive adapter [1,Y,Y^2,Y^3,Y^4] had passed the exact plaintext composed-interface gate: retained matrix I_10, rank 10, zero unused-coordinate leakage, exact sentinel recovery.

Fixed native gate:
- HElib acdb264e1a991eaee35fd8b3c31bebe9528c49a1;
- m=32768, p=5, r=4, bits=400, c=3;
- plaintext modulus 625;
- normal_basis=false;
- Y=X^1024;
- J_consecutive(phi(e_i))=Y^i;
- normalization 224;
- one deterministic non-production seed;
- no retry, rescue, parameter sweep, alternate exponent set, or surrogate.

Logical middle path:
  one ModSwitch
  -> exact merged R8 S2C
  -> one InnerProduct/MultKey
  -> one RM10
  -> scalar normalization
  -> exact merged R8 C2S
  -> unpack/recover first five coordinates.

Scientific result remains UNKNOWN.

## Expected evidence / artifacts

The exact final artifact filename was not recovered from prior context and is intentionally not invented.

Expected evidence categories:
- final native evidence ZIP/package if produced;
- raw native logs;
- artifact path, byte size, outer SHA-256, internal hashes;
- Git before/after/status;
- exact source diff / source snapshot;
- commands/spec/report establishing one execution and no retry;
- native correctness/noise/capacity metrics for the bounded middle gate.

Known carried static evidence:
- consecutive-interface ZIP SHA-256: 519240d0de9c8a995a781da8071f242b18dd4ccd8be20f0474d46d78639eabe8
- deterministic RMFE instance SHA-256: d3713553cc386a228dd70b2f099b7d55fdb3f5d91b273d4b9e8e0fa2013b4ea9
- exact R8 maps/source ledger SHA-256: 469a07c41f1a89bd838e4bf7ef57ab105673ca66561344955d8f9ab228fef0fc

## Cross-session rule

PENDING_CODEX_TASKS_MAY_CROSS_SESSION_BOUNDARIES=true.

Do not cancel, restart, modify, duplicate, or infer the result.
Do not start another heavy native task on this host while this task remains active.
When raw evidence is delivered, the successor Research GPT must independently audit it before accepting any scientific PASS/FAIL claim.
On scientific FAIL, park the RMFE-R8 single-MultKey family.
On PASS, do not automatically expand beyond the bounded middle gate.
