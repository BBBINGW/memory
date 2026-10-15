# Start FHE Research Session — Single Active Research Target

**Mode:** ONE PI-selected active research task at a time. Use the existing single GitHub Notes / Research MCP; no per-track login, OAuth scope, hostname, independent instance or mandatory track-lock process.

## Restore

Read in order:
1. `RESEARCH_PHILOSOPHY.md`
2. `AGENT.md`
3. `STATE.md` — active target, latest checkpoint and NEXT_ACTION
4. Relevant topic's original `findings/` and `failures/`, with source pointers and previously falsified mechanisms.

The older `findings/TRACK_ISOLATION_POLICY.md` and `findings/RESEARCH_TRACK_INDEX.md` are retired archival descriptions and MUST NOT restrict ordinary research, determine the active target or demand new MCP infrastructure.

## Work

- Honor the user's latest explicit target; otherwise "继续" continues the existing active subject in `STATE.md`.
- One falsifiable primary hypothesis + one cheapest decisive test per iteration, followed by progressively deeper verification only if warranted.
- Apply Constructive Synthesis: convert correct components into one coherent, sound/secure, costed mechanism rather than accumulating isolated pieces.
- Check original papers, newer versions and prior art; distinguish [FACT], [DERIVED], [HYPOTHESIS], [NEGATIVE] and provenance limitations.
- No false novelty, no background/autonomous research, no silent pivot when a target is blocked.
- Existing numbering (`CGS-20`, `SHIP-I226`, `V43`, etc.) remains historical identification; it does not create separate permissions.

## Save and hand off

Update `STATE.md` as the one active-status entrypoint when a meaningful iteration completes or the PI switches topics. Keep detailed derivations, proofs and failures in original topic files; never delete or overwrite historical evidence. Read files before updates and re-read to verify. The existing writer lacks caller-provided atomic expected_sha, so avoid concurrent edits.

End an iteration with `STATUS / RESULT / NEXT_TEST / STATE_UPDATE`. Before a chat hits its length limit, ensure `STATE.md` points to the current source-backed result and smallest next action, so a new chat resumes from it without starting again.

**Local backend caveat:** A previously implemented experimental per-track server branch was reportedly not pushed/deployed as of this rollback request. The GitHub notes repository cannot revert the user's local Codex workspace; do not deploy or require that branch.
