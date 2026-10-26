# Start FHE Research Session — Single Active Research Target

**Mode:** ONE PI-selected active research task at a time. Use the existing single GitHub Notes / Research MCP; no per-track login, OAuth scope, hostname, independent instance or mandatory track-lock process.

## Restore

Read in order:
1. `RESEARCH_PHILOSOPHY.md`
2. `AGENT.md`
3. [`findings/RESEARCH_QUALITY_EXECUTION_2026-10-26.md`](findings/RESEARCH_QUALITY_EXECUTION_2026-10-26.md) — P0–P2 and seven mandatory quality fixes.
4. `STATE.md` **and the newest verifiable dated handoff** — compare before treating any old heading or NEXT_ACTION as current. Mark `STATE_STALE/RECONCILE_REQUIRED` if they disagree.
5. Relevant topic's original `findings/` and `failures/`, plus `MISSING_SOURCES.md`, with source pointers and previously falsified mechanisms.

The older `findings/TRACK_ISOLATION_POLICY.md` and `findings/RESEARCH_TRACK_INDEX.md` are retired archival descriptions and MUST NOT demand new MCP infrastructure. This does NOT override the PI's explicit active-topic selection or research-line pause decisions.

## Work

- Honor the user's latest explicit target; otherwise "继续" continues that selected subject. If root `STATE.md` is stale, first reconcile with the latest trustworthy handoff; never silently pivot or reopen a paused topic.
- One falsifiable primary hypothesis + one cheapest decisive test per iteration, followed by progressively deeper verification only if warranted.
- Apply Constructive Synthesis: convert correct components into one coherent, sound/secure, costed mechanism rather than accumulating isolated pieces.
- **P0:** Start with a significant source-backed baseline bottleneck, not paper-by-paper technique roulette. For a high-value interface obstruction, assess one bounded representation/protocol redesign.
- **P1:** Before intensive work, screen current original Algorithm/KeyGen/interface, nearest equivalent prior art, NEW linking invariant and optimistic end-to-end benefit. Critical original source missing ⇒ `SOURCE_BLOCKED`; do not loop source-dependent toys.
- **P2:** Reuse read-only lessons from prior track `findings/` and `failures/`; classify obstruction and record what a new technique must overcome.
- Preserve one primary falsifiable claim, one cheapest decisive test and progressive proof. Distinguish [FACT], [DERIVED], [HYPOTHESIS], [NEGATIVE], [OPEN], and `DERIVED` vs actually executed toy vs `CODEX_REPORTED` vs `RAW_AUDITED` vs `NATIVE_REEXECUTED`. Two or three low-information probes ⇒ `VALUE_REVIEW`.
- No false novelty, no background/autonomous research, no silent pivot when a target is blocked.
- Existing numbering (`CGS-20`, `SHIP-I226`, `V43`, etc.) remains historical identification; it does not create separate permissions.

## Save and hand off

Update `STATE.md` as a compact active-status entrypoint when a meaningful authorized iteration completes or the PI switches topics, **after** reconciling stale older headings with newer independently verifiable evidence. Keep detailed derivations, proofs and failures in original topic files; never delete or overwrite historical evidence. Read files before updates and re-read to verify. The existing writer lacks caller-provided atomic expected_sha, so avoid concurrent edits.

End an iteration with `TRACK + OFFICIAL/PRESCOUT / STATUS / EVIDENCE LEVEL / RESULT + LIMITATIONS / NOVELTY + IMPORTANCE / FULL GATES / DECISION / NEXT_TEST / STATE_UPDATE` (template in the quality guide). Before a chat hits its length limit, ensure `STATE.md` points to the current source-backed result and smallest next action, so a new chat resumes from it without starting again.

**Local backend caveat:** A previously implemented experimental per-track server branch was reportedly not pushed/deployed as of this rollback request. The GitHub notes repository cannot revert the user's local Codex workspace; do not deploy or require that branch.
