# Start a research session — LOCK THE TRACK FIRST

**Binding rule:** this file starts a **single independent research track**, not whichever project most recently changed the shared GitHub repository. See `findings/TRACK_ISOLATION_POLICY.md` and `findings/RESEARCH_TRACK_INDEX.md`.

## 0. Resolve research identity before following any task

From (a) the human PI's explicit instruction, else (b) the current conversation's already locked research target, else (c) an explicit track ID in a saved handoff, resolve:

```text
TRACK_ID: SHIP | CGS | VFHE | EXPLORE | (other PI-named track)
TRACK_STATE: exact authoritative track-state path from registry
LAST_ITERATION: last completed round in THAT track
TARGET: named active scientific problem
WRITE_SCOPE: that track's authorized files ONLY
```

**Never infer a TRACK_ID from root `STATE.md`, its `NEXT_ACTION`, GitHub file timestamps, another conversation's commits or global strategic priorities.** Bare “继续” / “continue” inherits the existing track. If no track is recoverable in a NEW conversation, request the one missing choice from the PI; do not silently pick a different research target.

## 1. Read protocol and the matching state

Read in order:

1. `RESEARCH_PHILOSOPHY.md`
2. `AGENT.md`
3. `findings/TRACK_ISOLATION_POLICY.md`
4. `findings/RESEARCH_TRACK_INDEX.md`
5. **The selected `TRACK_STATE` only** for authority over the track's next test
6. That track's pertinent `findings/` and `failures/` for precise source and previous negative results

`STATE.md` can be read for the global strategy/index but **never supplies an executable task**. The thematic map `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` and `findings/OPEN_RESEARCH_BRANCHES.md` may inform prior-art checks, not override the selected track.

If a source is missing, consult `MISSING_SOURCES.md` for historical references, `papers/README.md` for provenance and `LOCAL_WORKSPACE.md` for storage. Use `read_repo_pdf` on a permitted supplied source and check the precise pages. PDF metadata/automated text alone may be insufficient for intricate formulas.

## 2. Scientific iteration discipline

Execute only a **PI-authorized NEXT_ACTION of the selected track**, one smallest falsifiable primary hypothesis and one decisive test.

If that track is SOURCE_BLOCKED, PARKED, or HUMAN_REVIEW, do **not** interpret bare “continue” as an instruction to switch to VFHE/global/any other track or to bypass the gate. Report the evidence/status and the specific PI decision/source needed.

Keep [FACT], [DERIVED], [HYPOTHESIS], [NEGATIVE] distinct. Check relevant original-paper prior art, avoid repeating archived failures, and remember algebraic correctness alone does not establish FHE security/noise or performance.

## 3. Read-before-write and scope gate

Ordinary track research iterations MAY write only this track's exact state and the approved `findings/`/`failures/` filename prefixes from `findings/TRACK_ISOLATION_POLICY.md`.

Normal SHIP/CGS/VFHE/EXPLORE iterations MUST NOT modify:
- root `STATE.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or this startup file
- another track's state/findings/failures
- `MISSING_SOURCES.md`, shared research indexes, or `papers/supplied/`

Only a **separate PI-authorized GLOBAL_MAINTENANCE/source-supply operation** may edit shared metadata. A missing paper for a track may be logged in that track's own notes without silently editing the global missing-source registry.

Read the file first; verify allowed path/expected SHA and write once per coherent update. Re-read to verify content. **Current GitHub Notes write tool has no caller expected_sha and is not an atomic compare-and-swap**: never perform concurrent writes to the same path using it.

## 4. End of iteration and handoff

Report:

```text
TRACK_ID:
ITERATION_ID:
STATUS: PASS / FAIL / UNCLEAR / HUMAN_REVIEW
PRIMARY_HYPOTHESIS:
RESULT:
NEXT_ACTION: one smallest PI-contingent action within THIS track
STATE_UPDATE: YES / NO
CHANGED_FILES: (only if written)
```

When handing off into a new ChatGPT conversation, repeat the fixed TRACK_ID, authoritative state path, latest round, active question, blocker and permitted file scope. **Never import an unrelated track's NEXT_ACTION.** Do not initiate background autonomous iterations or cross-track writes on your own.

## 5. Hard-isolation limitation

The above is a documented behavioral/session lock, not proof of server-side track write authorization. For a real deny-on-write guard, the deployed Research MCP must enforce actor/credential-to-track binding and canonical path checks, plus expected-SHA conflicts. See `findings/MCP_TRACK_GUARD_CODEX_SPEC.md` for the Codex implementation task.
