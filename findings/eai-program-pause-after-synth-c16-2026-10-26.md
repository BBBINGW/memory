# EAI program pause — PI handoff after SYNTH-C16
Date: 2026-10-26 (Asia/Singapore)
AUTHORITY: Direct PI instruction: "暂时封存AI这条line，我们先开个对话继续搞密码学的内容，保存该保存的在github相关内容里，给出新对话的指令".

## Decision and research isolation
- **EAI research program: PAUSED_BY_PI / FROZEN**, including the currently active EAI-SYNTH work. Do NOT automatically resume EAI-SYNTH, EAI-SYS, EAI-P or EAI-SEC, schedule new AI research, or run pending Codex jobs. Sibling program files are NOT altered by this handoff; their own checkpoints remain authoritative if explicitly reactivated later.
- Active AI subline at handoff: TRACK_ID=EAI; ACTIVE_TOPIC=SYNTHETIC_DATA; ACTIVE_SUBLINE=EAI-SYNTH.
- **LATEST_COMPLETED=SYNTH-C16; SYNTH-C17_NOT_STARTED; NEXT_ACTION=NONE_AUTOMATIC; STATE=PAUSED_BY_PI.**
- Human PI decides future restart, scope, research novelty, expensive experiments, and Codex authorization.
- No model downloads, training, remote API tests, GPU/Codex or environment modifications were performed while creating this handoff.
- All FHE/cryptography research lines remain separate; this AI pause DOES NOT pick a new cryptography target, change crypto checkpoints, or authorize a crypto experiment.

## Completed AI research and honest technical summary
- EAI-SYNTH has completed **28 research iterations**: B01–B12 (12) and C01–C16 (16).
- B01–B12: online/private synthetic data methods, sparse noise-accounting and source-semantics issues; no confirmed author vulnerability or publishable new primitive. B11/B12 preserved with source ambiguity.
- C01–C11: rare-mode coverage, verifier quality, Gaussian/OT risks, gradient-based utility, optimizer-aware selection, teacher+training budget; strongest ideas directly covered or challenged by mature prior art; no original end-to-end method.
- C12: a simulator conditioned only on SAME-APP history cannot certify hidden shared resource state across apps; this is an information boundary, not an attack on Apple SimSAT.
- C13: for a KNOWN relation/contract, keyed IVM/materialized views and serializable transaction isolation already solve compact projection and safe booking; not novel.
- C14: successful APIPilot/REST API dependency execution (2xx) does not imply hidden cross-app causal/business correctness; paper itself states limit, other API testing prior art.
- C15: short same-ID interventions in deterministic finite-state one-register setting reduce to register-automata active learning; Dierl et al. SL^lambda (Journal of Automated Reasoning 2026) direct prior, with ideal oracle limits.
- C16: unknown synchronization alphabets over deterministic finite global action traces reduce to Henry et al. **CoalA CONCUR2025** compositional active learning via counterexample-guided alphabet refinement; behavioral equivalence is NOT physical service decomposition or authentic transaction-level causal state. Additional FDRRestTest ESEM2026 original abstract indicates budget-aware API dependency/logical-oracle testing is already explored.
- **Scientific disposition:** C13–C16 are consecutive negative novelty/mechanism gates. A research-worthy new algorithm with nontrivial proof, reproducible end-to-end synthetic environment advantage and verified novelty HAS NOT BEEN ESTABLISHED. Broad regime of unknown cross-app identity translation, asynchronous transactions, concurrency/rollback, stochastic/partial reset, irreversible side effects, and joint query/reset/token budgets remains OPEN/UNCERTIFIED, NOT a claimed contribution. On eventual PI restart, first require materially new original-source-vetted technical claim and one cheapest falsifier rather than C17 adjacent toy.

## Canonical files to preserve (read; do not modify/rewrite)
1. `findings/eai-synth-STATE.md` — independent latest checkpoint (this pause should be appended after C16).
2. `findings/eai-synth-c16-unknown-synchronization-action-alphabet-coala-gate-2026-10-26.md`.
3. `failures/eai-synth-c16-new-cross-app-action-synchronization-learner-necessity-no-go-2026-10-26.md`.
4. `findings/eai-synth-c15-register-automata-cross-app-intervention-priorart-gate-2026-10-26.md`.
5. `failures/eai-synth-c15-low-reset-cross-app-same-key-query-priorart-no-go-2026-10-26.md`.
6. `findings/eai-synth-session-handoff-2026-10-26.md` (EARLIER C14 handoff, superseded by C15/C16/pause checkpoint).
7. `findings/eai-synth-pending-codex-b11-author-semantics-audit-2026-10-26.md` — optional historical task ONLY, not authorized to execute.
8. `AGENT.md`, `RESEARCH_PHILOSOPHY.md` — research discipline.
- Root `STATE.md` is near size limit and MUST NOT be appended, overwritten, or truncated.

## Codex
`PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO`; instructions were displayed in a previous ChatGPT message, but neither submission nor execution is confirmed. **PAUSED, DO NOT EXECUTE**.
No C15/C16 Codex task exists.

## Crypto handoff: STRICT VERIFICATION WARNING
PI requests a NEW conversation to resume earlier cryptography research, but has NOT yet selected one specific cryptography subline in this message. Do NOT silently resume an AI NEXT_ACTION or select a crypto line solely by an old root STATE.md.
Prior conversation reports (not revalidated as current crypto repo checkpoints in this PAUSE write):
- BOOT last reported completed B123, B124 NOT_STARTED, previously PI-paused; available separate artifact `BOOT_STATE_SNAPSHOT_B123_2026-10-21.md`.
- SHIP last reported completed I407, I408 NOT_STARTED, previously PI-paused.
- vFHE V43 latest source-revision repair audit (revised author paper addresses historical CRT issue); V44 NOT_STARTED; historical attack must not be revived without checking author revision.
- CGS completed CGS-52; later attempt only with genuinely new security reduction/primitive; CGS-53 NOT_STARTED.
**Repo divergence encountered while preparing this pause:** live GitHub `findings/boot-STATE.md` tail reads B056, and `findings/ship-memory-STATE.md` tail reads I251, OLDER than the separately reported BOOT B123 and SHIP I407 snapshots. It is unsafe to pretend these old modular state tails are latest; no crypto files were changed. New chat must read all available dated repo findings / dedicated snapshots and reconcile source provenance, version, and latest authorization BEFORE proposing a research round or writing crypto states.
- New crypto chat should first return a brief evidence-grounded priority table of BOOT / SHIP / vFHE / CGS, with conflicts clearly marked, let PI choose ONE line (or use explicit PI choice in new prompt). Do not run Codex, remote/hardware tests or live source modifications until separate PI authorization.
- Use smallest falsifiable hypothesis → cheapest decisive test → minimal verification → expand only if warranted; ONE round per PI authorization, no autonomous loop.

## Release conditions
- EAI remains PAUSED_BY_PI until a future explicit instruction lifts the pause.
- Beginning crypto work does not implicitly unpause EAI.
- `SYNTH-C17_NOT_STARTED`, no default future SYNTH iteration.
- Append this pause checkpoint ONLY to independent `findings/eai-synth-STATE.md`; do not overwrite EAI siblings or root STATE.md.

STATUS: PAUSED_BY_PI
RESULT: EAI-SYNTH C16 results archived; EAI program frozen, future crypto priority to be selected after fresh evidence reconciliation.
NOVELTY: EAI-SYNTH overall NOT_ESTABLISHED.
NEXT_ACTION: NONE_AUTOMATIC for EAI; new independent cryptography chat must read, compare, and request PI selection of specific active crypto line.
PENDING_CODEX: B11 optional task PENDING/PAUSED, not executed.
STATE_UPDATE: YES only after both pause handoff and independent state append exact readback.
