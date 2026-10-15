# Codex Task — Enforce Three-Layer Research Track Isolation in Research MCP

> **RETIRED / DO NOT IMPLEMENT OR DEPLOY FOR CURRENT WORKFLOW (PI decision 2026-10-15).** Separate per-track MCP write authorization is paused. Keep this document only as historical technical design; continue with the existing single MCP and centralized `STATE.md`. The experimental local feature commit must be reverted/abandoned by Codex if the user wishes; this note does not change local code.


**Repository to modify:** The actual implementation repository of the PI's Research MCP server, not merely the connected GitHub Notes data repository. Inspect its real layout first; do not assume Python/FastAPI/Node or a particular deployment path.

**Current client-facing research repository:** GitHub Notes fixed notes repo on branch `main`. Soft policies ALREADY IMPLEMENTED on 2026-10-15:
- `STATE.md`: global index only
- `findings/RESEARCH_TRACK_INDEX.md`: canonical track registry
- `findings/TRACK_ISOLATION_POLICY.md`: behavioral + security policy
- `START_RESEARCH_SESSION.md`: lock identity before reading task
- `AGENT.md`: independent state authority
- SHIP `findings/ship-memory-STATE.md` (SHIP-I226)
- CGS `findings/threshold-fhe-correlated-gaussian-sampling.md` (CGS-17)
- VFHE `findings/vfhe-cross-crt-state.md` (V43)

DO NOT delete, rename, reformat or migrate existing research data. No new scientific exploration or metadata rewriting in this task. Old global root file preserved at `findings/legacy-global-STATE-before-track-isolation-2026-10-15.md`.

## Objective

Make **server-enforced, fail-closed, authenticated per-TRACK write scopes**, with no alternate-tool bypass and race-safe GitHub writes. Keep normal cross-track READS available. The same GitHub repo may be used for all tracks, but sessions may not overwrite another track.

## 0. Security prerequisite: trust boundary

Three concurrent ChatGPT conversations using the SAME connector credential and the SAME unscoped MCP server are indistinguishable to the server. An ordinary model-supplied `track_id` argument is UNTRUSTED and does not constitute hard isolation.

Implement a trusted server-side principal with `role=research_track` and `scope=SHIP|CGS|VFHE`, bound to a distinct authenticated connection/deployment/authorized OAuth client/token. The principal must be established from validated authentication or server-side configuration **not freely selected by tool-call arguments**. If existing Auth0/OAuth configuration does not support reliable track identity, deploy **three isolated MCP endpoints/instances** with immutable server env `RESEARCH_TRACK=SHIP|CGS|VFHE`, each configured as a separate ChatGPT connector, plus an optional **separately authenticated** `GLOBAL_MAINTENANCE` connector for shared files. An agent in SHIP connection must not be able to ask the same connector to act as VFHE.

Preserve current TLS/OAuth/Auth0 authorization; validate issuer, audience, signature, expiry, scopes, and the connection-to-track mapping. Do not accept arbitrary `X-Track` header, query parameter, path argument or user-editable prompt as the authorization source. Do not expose credentials in repository/logs.

## 1. Centralized exact write-authorization

Implement a single trusted `authorize_write(principal, operation, normalized_repo_path)` used in EVERY GitHub-modifying endpoint, including current `write_repo_file`, `append_repo_file` and any update/delete/commit/upload/rename endpoints. Prevent bypass through generic GitHub-commit operations or alternate tool names.

Permit during track research only:

- `SHIP`: exact existing `findings/ship-memory-STATE.md`, or NEW/EXISTING research `findings/ship-memory-*.md` and `failures/ship-memory-*.md`.
- `CGS`: exact existing `findings/threshold-fhe-correlated-gaussian-sampling.md`, or `findings/cgs-*.md`, `failures/cgs-*.md`.
- `VFHE`: exact existing `findings/vfhe-cross-crt-state.md`, or `findings/vfhe-*.md`, `failures/vfhe-*.md`.

Path prefix checks must be on **canonical complete segments**, not loose substrings like `startswith("findings/ship")`. Explicitly distinguish privileged metadata:
`STATE.md`, `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, `MISSING_SOURCES.md`, `README.md`, `papers/supplied/`, `findings/RESEARCH_TRACK_INDEX.md`, `findings/TRACK_ISOLATION_POLICY.md`, `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md`, other track states and cross-track findings are **READ ONLY** for ordinary track principals.

`GLOBAL_MAINTENANCE` (separate stronger authentication) may edit global metadata via intentional tools; its presence must not let ordinary track credentials escalate. For generic paper upload, require explicit PI upload action via the admin connection (do not confuse PDF reading or `get_eprint_paper` cache with Git commits).

Reject absolute paths, `..`, `.` segments, repeated/empty segments, backslashes, NUL, percent/double-encoded traversal, Unicode/confusable path aliases and symlinks as appropriate for backend/GitHub semantics. Accept only simple ASCII POSIX relative paths for tool writes. Normalize and validate BEFORE access; fail closed on ambiguity. Prevent update via case variants, path substitution or alternate source branches/refs.

## 2. Race-safe writes and audit

Current GitHub Notes `write_repo_file`/`append_repo_file` do not expose caller-supplied `expected_sha`, so mere read-before-write is NOT a true atomic check. Add new **mandatory** `expected_sha` (for updates/appends) and explicit create-only semantics (for newly created files); a mismatch must return a typed conflict and NOT retry blind overwrite. Prefer GitHub Contents API or a tested server-side conditional mechanism; verify that GitHub's SHA checks are actually atomic enough under concurrent writes. Do not retain a legacy unguarded write/append tool accessible to research principals as a bypass.

On append, read existing content only after checking access, condition on the specific SHA the caller saw, and reject stale updates. Use idempotency tokens or compare-before-retry where feasible; do not duplicate an append after timeouts.

Audit each accepted/denied write with authenticated track, normalized path, operation, old/new blob SHA, commit SHA, timestamp and reason. Keep secrets and paper content out of logs. Do not change GitHub repo content before tests validate permissions.

## 3. Read boundary & compatibility

Research principals MAY read global protocols, other tracks' state/findings, public PDFs and missing sources as prior art. `get_eprint_paper`, `search_eprint_text`, `read_eprint_pages`, `read_repo_file`, `read_repo_pdf`, `list_repo_files` should remain readable within existing data-leak/privacy policy. Cross-track reading never changes principal TRACK_ID or authorization scope. Do not relax existing denylist (sensitive paths), size limits, OAuth and fixed-repo binding.

Metadata and source ownership for pre-isolation files remain unchanged. Do not automatically move 100+ archived files into `tracks/`; current Research MCP allowlist rejected that directory. Only future work needs the approved path prefixes.

## 4. Required automated tests

With isolated test repository/branch and mocked GitHub HTTP where suitable:

- Three positive tests: SHIP writes only SHIP state/finding; CGS only CGS; VFHE only VFHE.
- Six cross-track negatives (every principal against both other states), plus each principal against root `STATE.md`, `MISSING_SOURCES.md`, index files and `papers/supplied`.
- A SHIP call with tool argument `track_id=VFHE` or spoofed header must remain SHIP and be denied for VFHE paths.
- Both `write_repo_file` AND `append_repo_file` (and all other mutators) must deny bypass attempts.
- Reject traversal `../`, URL encodings, backslashes, absolute paths, prefix-collision `findings/ship-memory-STATE.md/../vfhe...`, alternate separators/Unicode, aliases/symlinks.
- Two simultaneous clients using the same expected SHA: exactly one commit succeeds and the second returns `CONFLICT_STALE_SHA` without lost updates. Test append timeout/retry doesn't duplicate.
- GLOBAL_MAINTENANCE can edit a shared file only with correct independent authorization; track principal cannot mint/admin-swap claims.
- Check that reading a VFHE source while in SHIP does not affect SHIP write scope, even after repeated tool calls.
- Smoke test actual deployed MCP connection/authentication and OAuth principal mapping **after deployment**; local unit tests alone are not a production PASS.

## 5. Safe execution / deployment

- Read existing repository code, tests, deployment manifests and environment configs first. Write minimal code changes on a feature branch with reviewable commits; run lint/tests, check backwards compatibility, document new connector setup.
- No production secrets in commits, no broad new network exposure, no unreviewed auto-deployment, no overwrite/rewrite of research findings.
- Report: files changed, exact access mapping, tests (pass/fail with command), potential security bypasses, deployed vs not deployed, feature branch/commit, migration/setup instructions and how to configure 3 scoped ChatGPT connections. Do not claim hard isolation until a deployed negative-write test succeeds.

**Definition of done:** three separately authenticated/constrained ChatGPT Research MCP connections are verified to REJECT cross-track writes and stale SHA updates while supporting allowed same-track writes and cross-track reads. Until that is true, report `LAYER_3_SOFT_ONLY`.
