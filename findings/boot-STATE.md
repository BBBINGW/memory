# BOOT State

Updated: 2026-10-28 — Research Turn 2/25, post independent B174 artifact audit.

- TRACK_ID: BOOT
- ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- LATEST_COMPLETED: B174_AUDIT
- NEXT_ITERATION: B175_CANDIDATE_PI_REVIEW; B175_NOT_STARTED
- CURRENT_STATUS: B174_AUDITED / WAIT_PI
- CURRENT_EXPERIMENT: NONE_AUTHORIZED; B175_NOT_STARTED
- CURRENT_RESULT: PASS_B174_SCALE_INVARIANT_GROUPED
- HEADROOM: MARGINAL
- EVIDENCE: RAW_AUDITED
- ACTIVE_CANDIDATE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- ACTIVE_GEOMETRY: H=8192, s=8
- ACTIVE_CHECKPOINT: k0=32
- STATUS: ACTIVE_NATIVE_CANDIDATE / WAIT_PI
- NOVELTY: PROMISING_NOT_ESTABLISHED
- FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED
- END_TO_END_SPEEDUP: NOT_ESTABLISHED

Authoritative handoff:
findings/boot-HANDOFF-post-B174-audit-waiting-PI-2026-10-28.md

Latest completed finding:
findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md

B174 original ZIP SHA-256:
9232a9b3e57fe08adb0daf84c2bfe3183e4fb49a7de4695396720d96decfe4d8

Independently checked: outer hash, 29/29 internal checksums, original B173 parent byte identity, exact diff, unchanged parameter/security/mask/comparator scope, all 11 CSVs/119 rows, 36 stage probes, exact public references, scale/noise/counts, and evaluation-key report.

Established: three fixed cases exact at L18, final GROUPED budgets 15/14/15, final scale43178. Actual25 ct-ct to grouped;27 remains projected. Eval keys965.03 MiB use an inherited L14 LT plan and are not the final all-L18 composition cost. Nonzero y^4=-1 phase coverage, whole Algorithm5, DFR and speedup remain unestablished.

Only pending candidate:
A single CASE_1 same-context L18 LT8 x GROUPED SI pointwise falsifier, with actual LT key levels checked/promoted to >=18. Stop at pointwise; no benchmark or later stages. This is a proposal requiring PI judgment, not an execution instruction.

Important rule:
Do not restart B174 or launch B175 without PI authorization. No Codex/native experiment was launched in this audit. Preserve the prior B173 audit and B174-running handoff as history. The unrelated root STATE.md is known stale for this explicit BOOT recovery and is not the active research authority.
