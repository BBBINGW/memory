# Global FHE Research State — Track Index Only

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**Role:** GLOBAL STRATEGY + TRACK REGISTRY POINTERS ONLY. **NOT AN EXECUTABLE RESEARCH NEXT_ACTION.**

## Research management

- **Human PI** decides research targets, prioritization, pivots and contribution acceptance.
- Global research philosophy: `RESEARCH_PHILOSOPHY.md`; agent rules: `AGENT.md`.
- Mandatory multi-session target and write policy: `findings/TRACK_ISOLATION_POLICY.md`.
- Canonical track identities and individual authoritative states: `findings/RESEARCH_TRACK_INDEX.md`.
- Per-session startup: `START_RESEARCH_SESSION.md`. Resolve the current session's TRACK_ID **BEFORE** selecting a research state. Never treat this index or its modification time as the target.

## Independent research tracks (read the named STATE for any Next Action)

| TRACK_ID | Authoritative state | Last completed | Current disposition |
| --- | --- | --- | --- |
| SHIP | `findings/ship-memory-STATE.md` | **SHIP-I226** | HUMAN_REVIEW: HMux prepared-key memory dominant; repeated identical zero-key ciphertext reuse is unsafe, no security-matched benchmarked large memory compression |
| CGS | `findings/threshold-fhe-correlated-gaussian-sampling.md` | **CGS-17** | HUMAN_REVIEW: Okada–Takagi correlated secret-conditioned Gaussian padding/storage problem OPEN; direct seeded integration attempts did not solve it |
| VFHE | `findings/vfhe-cross-crt-state.md` | **V43** | HUMAN_REVIEW / PARK recommended: older CRT scalar-digit soundness flaw acknowledged; new Oct-2026 protocol blocks original witness |
| GENERAL (archived) | `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` | **I192 FROZEN** | Historical general FHE research, no automatic I193 |
| Other independent work | `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` | PVFHE P27, TFHE-ISA T02 etc. | Historical/parked: see index; do not merge numbering with backlog P1–P22 |

## Global strategy — not a cross-track instruction

PI-approved preference (2026-10-15): pursue **nontrivial, primary-source-grounded FHE optimization composition obstructions** with a meaningful corrective technique, formal correctness/security/noise or precision and concrete end-to-end costs. This informs **PI target selection** only; it never causes a SHIP, CGS or VFHE session to switch tracks on "继续".

## No global executable next task

There is **intentionally no global NEXT_ACTION**. Each independent track state contains its own `NEXT_ACTION` and HUMAN_REVIEW/PARK gate. A track-specific "continue" may act only within its already locked track and only as authorized by PI; it cannot read a global action as a fallback.

**Ordinary track writes:** track-owned state, findings and failures only. Changes to this global file, policy, research integration or shared MISSING_SOURCES are separate PI-authorized **GLOBAL_MAINTENANCE** tasks.

## Provenance / preservation

The former long vFHE-focused root state is preserved verbatim at `findings/legacy-global-STATE-before-track-isolation-2026-10-15.md` and in Git history. Detailed research remains in original track documents; no research evidence was removed or renumbered by this restructuring.

**Server-enforcement caveat:** Currently GitHub Notes path policy is documented but not proven enforced per track. Hard-scoped write authorization and compare-and-swap require a backend upgrade; see `findings/MCP_TRACK_GUARD_CODEX_SPEC.md`.
