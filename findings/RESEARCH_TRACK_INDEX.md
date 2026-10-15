# FHE Research Track Registry

**Status:** TRACK REGISTRY, NOT A TASK QUEUE.
**Created:** 2026-10-15. Human PI controls research target selection and cross-track pivot.
**Source of authority:** `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`, and `findings/TRACK_ISOLATION_POLICY.md`.

## Canonical track IDs and authoritative states

| TRACK_ID | Research target | Authoritative mutable track state | Last documented iteration | Status | Relevant historic result |
| --- | --- | --- | --- | --- | --- |
| SHIP | SHIP evaluation-key memory and HMux/selector keys | `findings/ship-memory-STATE.md` | SHIP-I226 | HUMAN_REVIEW; memory bottleneck audited, zero-HMux ciphertext-byte reuse candidate rejected | `failures/ship-memory-I226-reused-zero-hmux-key-fingerprint-leak.md` |
| CGS | Threshold FHE secret-conditioned correlated Gaussian sampling | `findings/threshold-fhe-correlated-gaussian-sampling.md` | CGS-17 | HUMAN_REVIEW; original O(LDec) storage problem OPEN, direct PRSS/PCF/Noah subset migration not solved | Final `CGS-17` section in track state |
| VFHE | vFHE CRT integer-digit consistency | `findings/vfhe-cross-crt-state.md` | V43 | HUMAN_REVIEW / PARK recommended; October 2026 protocol blocks archived CRT witness | `findings/vfhe-v43-oct2026-range-repair-gate.md` |
| GENERAL | Older independent FHE research program | `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` + archived findings | I192 (FROZEN) | HISTORY / PI decision only; do not auto-start I193 | `findings/OPEN_RESEARCH_BRANCHES.md` |

Other independent namespaces (PVFHE P01–P27, TFHE-ISA T01–T02, and backlog P01–P22) keep their original identities; this table is not an exhaustive full research directory.

## Resolution rule

1. Determine `TRACK_ID` from the PI's explicit message or the **existing current ChatGPT conversation**, never from modification times or root `STATE.md`.
2. Read global principles/protocols and the SINGLE matching authoritative track state.
3. Read other tracks strictly as prior art, with no change of active target.
4. "继续", "continue" and similar follow-ups inherit the previous TRACK_ID; parked/HUMAN_REVIEW status does not authorize a pivot.
5. If a new conversation has **no recoverable prior track identity**, request a track selection rather than guess from recently edited GitHub files.
6. Research iterations write exclusively to track-owned files; shared metadata changes require explicit global-maintenance instruction.

## Existing owned file path conventions — no mass move

- SHIP: state `findings/ship-memory-STATE.md`, future `findings/ship-memory-*.md` and `failures/ship-memory-*.md` (existing `failures/ship-i*.md` retained as historical).
- CGS: state `findings/threshold-fhe-correlated-gaussian-sampling.md`; new results should use `findings/cgs-*.md` and `failures/cgs-*.md` (older `threshold-fhe-*` / `thfhe-*` files remain historical references).
- VFHE: state `findings/vfhe-cross-crt-state.md`; future `findings/vfhe-*.md` and `failures/vfhe-*.md`.
- Shared `STATE.md`, `START_RESEARCH_SESSION.md`, `AGENT.md`, `MISSING_SOURCES.md`, integrated index and track policy are **global metadata**; ordinary SHIP/CGS/VFHE iterations must not rewrite them.

Prior root state: `findings/legacy-global-STATE-before-track-isolation-2026-10-15.md` (historical snapshot). The Git repository/commit history contains the complete original results; no previous evidence has been deleted or renumbered.

**Security caveat:** This registry and written rules are SOFT restrictions. They are not a server-side authorization mechanism. Real hard enforcement requires track-scoped MCP credentials/tools, canonical-path authorization and conflicting-write protection described in `findings/MCP_TRACK_GUARD_CODEX_SPEC.md`.
