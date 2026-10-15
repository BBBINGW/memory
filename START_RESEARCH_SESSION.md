# Start a research session

Read in order: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`.
Read `MISSING_SOURCES.md` only if the current work depends on missing evidence.
Follow the relevant entry's Repository Path to the specific `papers/supplied/` file,
use `read_repo_pdf(path, start_page, end_page)` for the required pages, verify
that the needed evidence is legible, then resume the recorded technical check.
A prior SUPPLIED status does not guarantee that every equation/figure extracts
correctly; if access or extraction fails, report the blocker and keep verification pending.
Consult `LOCAL_WORKSPACE.md` for storage/promotion and `papers/README.md` when
acquiring evidence; retrieve findings, failures, notes and supplied sources only
as needed. Do not load every paper or the whole conversation history.

Execute the Next Action of the **current user-selected research track**, not an unrelated track found in the shared root STATE.md: one primary hypothesis and one decisive test.
Use local tools for scratch work; the GitHub MCP cannot access `local/`.
Return PASS / FAIL / UNCLEAR / HUMAN_REVIEW, promote a useful concise result if
warranted, update STATE only on material change, then stop for the human.
If no active question exists, ask the human to choose it; do not invent one.

For missing critical primary evidence, update `MISSING_SOURCES.md`, report
MISSING CRITICAL SOURCE, and stop the dependent verification. Do not fake completion.


## Strategic resumption gate (PI approved 2026-10-15)

Before proposing a new independent target, also read `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` and the pertinent `findings/OPEN_RESEARCH_BRANCHES.md` entries. Prefer a FHE optimization **composition obstacle** with a genuinely new mechanism and verified current primary source. Screen for prior-art acknowledgment/trivial repair first. Preserve I192 frozen and all separate namespaces (V, PVFHE, TFHE-ISA). Missing-source branches are not next actions; request human PI direction when no specific active question is set. Do not infer that a user saying “continue” authorizes reopening an explicitly parked source-blocked line.


## Session target lock — independent research conversations (2026-10-15)

- At entry/resumption, identify the active target from the user's explicit instruction or this conversation's already-established track; open **that track's** authoritative state (e.g., vFHE V-series: `findings/vfhe-cross-crt-state.md`; SHIP: `findings/ship-memory-STATE.md`; threshold CGS: `findings/threshold-fhe-correlated-gaussian-sampling.md`). Root `STATE.md` is a global index and strategy, **not** a universal automatic next-target selector.
- An unqualified user message such as **“继续” / “please continue”** continues the same active target; NEVER move SHIP, CGS, vFHE, or other independent conversations into another track because a root file has a later timestamp or different NEXT_ACTION.
- Read other tracks only for contextual prior art, not for advancing their counters, editing their state, or taking over their work. Require an **explicit human PI instruction** for cross-track change, including any global composition-first strategy pivot. Keep existing independent round namespaces and counters intact.
- If the active track is explicitly parked or source-blocked, resume only when the user provides the missing source/other gate or explicitly authorizes a specific new test; otherwise present the human-review decision package instead of silently choosing another branch. Always read-before-write and verify any change.
