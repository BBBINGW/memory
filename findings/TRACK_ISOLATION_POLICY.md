# FHE Research: Track Isolation Policy

Effective: 2026-10-15. This policy applies to concurrent ChatGPT research sessions using the SAME GitHub Notes repository. Human PI authorizes targets and major pivots.

## Three layers

### Layer 1 — State isolation

- `STATE.md` is an **INDEX and global strategy only**. It must NOT contain an executable global `NEXT_ACTION`, an "active track" that all sessions must follow, or a shared iteration counter to advance.
- Each track owns exactly ONE authoritative state: see `findings/RESEARCH_TRACK_INDEX.md`. All research updates and `NEXT_ACTION` reside there.
- Preserve existing historical filenames, counters and findings. No branch renumbering; SHIP-I226, CGS-17, V43, and frozen GENERAL-I192 are separate.

### Layer 2 — Session identity lock

At the beginning of each conversation or session handoff, resolve and retain:

```text
TRACK_ID = SHIP | CGS | VFHE | (explicit PI-selected other track)
TRACK_STATE = authoritative file from registry
LAST_ITERATION = from that state
ACTIVE_TARGET = named technical problem in that state/conversation
WRITE_SCOPE = only this track's approved state/findings/failures
```

Precedence for `TRACK_ID`: explicit PI selection > this conversation's previously locked target > resumable handoff indicating exact prior track. Global `STATE.md` / most recent commit / newest paper never chooses the track.

A bare "continue" preserves TRACK_ID and can run only a non-parked, PI-authorized next test. If the track is blocked/PARK/HUMAN_REVIEW, report that status and the smallest decision, **without switching topics**. Explicit PI approval is required to change TRACK_ID. "New general strategic theme" does not automatically change a session's track.

### Layer 3 — Write isolation (currently DOCUMENTED, NOT server-enforced)

**Normal track iteration** writes only:
- SHIP: `findings/ship-memory-STATE.md`, new `findings/ship-memory-*.md`, new `failures/ship-memory-*.md`.
- CGS: `findings/threshold-fhe-correlated-gaussian-sampling.md`, new `findings/cgs-*.md`, new `failures/cgs-*.md`.
- VFHE: `findings/vfhe-cross-crt-state.md`, new `findings/vfhe-*.md`, new `failures/vfhe-*.md`.

Everything else, including other tracks' states, root `STATE.md`, `MISSING_SOURCES.md`, the integration files, protocols, and `papers/supplied/`, is **read-only during a normal track iteration**. To update shared metadata or supply a paper, run a separate PI-authorized GLOBAL_MAINTENANCE action. Human-uploaded PDFs are handled as explicit source supply, not as an implicit track switch.

A historical filename from the old mixed I-series is reference material, not a new write permission. Never edit another track's notes merely because they mention the same paper.

### Commit/concurrency discipline

- One logical update per commit, with `track(SHIP): ...`, `track(CGS): ...`, `track(VFHE): ...`, or `meta: ...` in the commit message.
- Before every write: resolve active identity, validate exact normalized target path, read target content/SHA and check expected current version. After writing, re-read and verify.
- **The current GitHub Notes `write_repo_file` does NOT expose a caller-provided expected SHA.** Therefore this is NOT an atomic compare-and-swap safeguard. Do not run concurrent writes to the same file through this tool. For guaranteed optimistic concurrency, extend the Research MCP backend with `expected_sha` / conditional update and fail closed on mismatch.
- If the current connected tool does not enforce track restrictions on the server, never label Layer 3 "enforced". A prompt or a client-supplied `track_id` is insufficient authorization.

### Minimal smoke tests

1. SHIP session: "继续" reads only SHIP state for next action, never initiates VFHE/C​​GS.
2. CGS session: "继续" keeps CGS-17 and its HUMAN_REVIEW gate.
3. VFHE session: "继续" keeps V43 and does not increment SHIP/general counters.
4. SHIP writer attempts `findings/vfhe-cross-crt-state.md` -> MUST be DENIED by future hard-scoped MCP.
5. CGS writer attempts `STATE.md` -> MUST be DENIED by future hard-scoped MCP.
6. Two writes with the same old `expected_sha` -> exactly one succeeds; one raises conflict, without auto-overwriting.
7. Path traversal `../`, encoded traversal, absolute paths, symlinks, alternate slash, case/Unicode alias, and basename prefix tricks -> MUST be normalized/rejected before path authorization.
8. A read-only cross-track citation is allowed and must not alter target selection.

### Scope of this change

This document is a behavioral protocol plus a specification for backend work; it **does not claim** that the deployed Research MCP has track-scoped credentials, conditional SHA writes or strict path authorization implemented. See `findings/MCP_TRACK_GUARD_CODEX_SPEC.md` for a precise Codex task.
