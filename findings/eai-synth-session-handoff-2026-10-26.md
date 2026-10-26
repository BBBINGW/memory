# Resume EAI-SYNTH — Chat handoff after SYNTH-C14
Date: 2026-10-26 (Asia/Singapore). This is a HANDOFF, not a research iteration and NOT permission to launch C15, Codex, GPU or training.

## 0. Research identity and hard isolation
- Human is PI, makes the final choice of research question, novelty, substantial pivot, proofs/experiments and Codex authorization.
- Assistant is Efficient AI / synthetic-data research student: original literature, rigorous derivations, counterexamples, novel constructive repair attempts, provenance and state maintenance.
- TRACK_ID: EAI
- ACTIVE_TOPIC: SYNTHETIC_DATA
- ACTIVE_SUBLINE: EAI-SYNTH
- LATEST_COMPLETED: SYNTH-C14
- NEXT_CANDIDATE: SYNTH-C15_NOT_STARTED
- No EAI-SYS (its SCOUT-S54, S55_NOT_STARTED), EAI-P, EAI-SEC, FHE/SHIP/BOOT/CGS/VFHE/EXPLORE writes or NEXT_ACTION inheritance. Read their results only if helpful for prior art with traceable evidence.
- User approves exactly ONE research iteration when saying “好的，请继续” within the active line; never launch successive iterations automatically.
- All Codex tasks stay PENDING unless the PI explicitly requests use; user requested a copyable B11 instruction in prior chat and the assistant DISPLAYED it on 2026-10-26, but NO Codex execution or user submission is confirmed. Do not say no instruction was ever provided.
- No Codex, GPU, model downloads/training, remote server, Docker, environment edits or substantial repo source changes without explicit PI permission. Ordinary allowed research-note GitHub writes must be isolated to EAI-SYNTH findings/failures and modular EAI-SYNTH state; read-before-write; exact readback verification.
- Repository: BBBINGW/memory. Connected GitHub and GitHub Notes available. Root STATE.md is near writer size limit (~260 k characters); DO NOT append, rewrite or truncate root; maintain findings/eai-synth-STATE.md instead.

## 1. Required read order in a new conversation
1) RESEARCH_PHILOSOPHY.md (general research philosophy; FHE examples are not EAI-SYNTH next tasks).
2) AGENT.md (one smallest falsifiable hypothesis + one cheapest decisive test; constructive synthesis gate).
3) findings/eai-synth-STATE.md — read the LAST overriding checkpoint, not the stale header or earlier checkpoints.
4) THIS file findings/eai-synth-session-handoff-2026-10-26.md.
5) findings/eai-synth-c14-executable-edge-vs-cross-app-causal-semantics-gate-2026-10-26.md and failures/eai-synth-c14-executable-success-causal-cross-app-certification-no-go-2026-10-26.md.
6) If C15 proceeds: findings/eai-synth-c12-cross-app-causal-state-local-history-source-gate-2026-10-26.md; findings/eai-synth-c13-causal-projection-ivm-serializable-priorart-gate-2026-10-26.md.
7) Only if B11 is explicitly resumed: findings/eai-synth-b11-sparse-segment-retry-semantics-gate-2026-10-25.md, findings/eai-synth-b12-2025-author-thesis-semantic-resolution-source-gate-2026-10-25.md and findings/eai-synth-pending-codex-b11-author-semantics-audit-2026-10-26.md.

## 2. Honest scientific progress across 26 rounds (B01–B12, C01–C14)
- B01–B10: online DP synthetic data, W1/finite histogram, adaptive streams, sparse counter analysis. Mostly known constructions or technical boundary screens; no original algorithm/method shown.
- B11–B12: He–Vershynin–Zhu `Online Differentially Private Synthetic Data Generation` Algorithm2 pre-test-before-consume permits literal zero-progress empty segment closures. Two mutually incompatible repeated-test-noise semantics: fresh each check => geometric retry tail; reuse same lambda'_t per timestamp with independent fresh lambda_j per segment => a conditional geometric retry with infinite expected number of attempts, proved under that interpretation. 2025 author dissertation repeats ambiguity. Neither authentic author implementation nor complete final IEEE typeset text was independently audited. **NOT a confirmed author privacy bug**; PARK. See exact B11/B12 records. Optional Codex author-source audit P2 only, no execution.
- C01–C05: iterative rare mode, imperfect verifiers, latent third-view identifiability, private moments and two-view covariance test. Classic Markov, survey estimation, Allman identifiability, MPC and DP hypothesis-test methods already cover core insights. FAIL novelty / PARK.
- C06–C07: Gaussian Wasserstein distance can misrank true downstream high-dim regression test risk (Rezaei ICLR2026 covariance optimality), multi-silo Wasserstein barycenter can drop between-silo covariance (Rychener Management Science2026 explicit Gaussian Example1). Real distinct objectives, direct prior art; FAIL novelty / PARK.
- C08–C11: FROST (2026 preprint) uses real-training-gradient EMA to score synthetic data without external verifier. Finite set reuse can violate a conditional population-gradient martingale assumption, but 2015–2020 stability/generalization prior art. Raw gradient score misranks preconditioned optimizer updates, but OPUS ICML2026 already introduces optimizer-aware scoring and sketching. Budgeted teacher synthetic generation Kessler COLM2026 and compute-constrained selection Yin–Rush ICLR2025 already source treatment. All important but prior known; no distinct cost-quality construction; PARK.
- C12: Apple SimSAT arXiv2607.16900v3 §3.3 per-application API history restricts observed context, whereas Gaia2 ICLR2026 Appendix A.3 explicitly recognizes partial unresolved cross-app temporal/relational consistency. Two worlds identical app-local observation but different unseen other-app shared-state write require different response => information sufficiency FAIL. This is NOT proof an Apple claim is false.
- C13: If cross-app shared schema and resource constraints are ALREADY formalized, Noria/DBToaster/DBSP incremental materialized views plus PostgreSQL SSI serializable transaction let a simulator use compact per-key state rather than entire history; generic 'minimal causal projection' is NOT a new primitive. Caveat Noria only eventual consistency; SSI separate.
- C14 LATEST: APIPilot arXiv2608.17546v2 validates LLM-suggested executable API dependency edges, but ORIGINAL §III.D itself says HTTP 2xx confirms executability in context, NOT full business correctness. LoBREST arXiv2604.08007v1 draws business sequences from logs; ARMeta arXiv2605.28321v1 builds/exeutes metamorphic seed/followup pairs and notes systematic cross-API consistency future work; CRUDinfer ICSE2026 infers CRUD semantics by black-box testing; RESTler ICSE2019 already producer-consumer dependencies. Minimal two-world witness: A.reserve(u)=SUCCESS, B.book(v≠u)=SUCCESS identical in independent vs shared slot stores, but followup B.book(u) succeeds vs conflicts. Thus successful-only passive observation is not proof of hidden cross-app causal constraint. Basic issue/repair is prior known; no paper attack/novel algorithm established. C14 status FAIL_C14_SUCCESSFUL_WORKFLOW_IMPLIES_HIDDEN_CROSS_APP_CAUSAL_DEPENDENCE. Research line-wide novelty NOT_ESTABLISHED.

## 3. Current research priorities (PI may revise)
P0 — ONE SYNTH-C15 source-first novelty and feasibility gate on **limited, authorized counterfactual interventions for hidden cross-application business-state/temporal/transactional constraint discovery**, not generic API parameter-dependency inference:
  - Define authorized resettable sandbox, unknown cross-app shared resource/identity mapping, target temporal/transaction semantics, allowed queries, resets/side effects, observability/nondeterminism and consistency oracle. No production API mutations.
  - Read strongest 2025–2026 original prior art with actual method/proof: APIPilot, LoBREST, ARMeta, CRUDinfer, RESTler, Gaia2, StateGen, AWM/EnvFactory, plus active automata learning, black-box stateful testing, causal experiment design, program synthesis.
  - Find ONE material scenario and precise technical claim: e.g. a restricted interventional oracle/budget policy with genuinely lower query/reset/context cost or better verifiable relation soundness than best baselines; do NOT assume novelty just because exact paper not found.
  - ONE cheapest decisive source/theory test FIRST: does a current method already implement exactly the controlled paired-intervention oracle and policy under the target budget? If yes: FAIL/PARK and do NOT elaborate adjacent tiny examples.
  - Only if an actual *unresolved* obstruction survives, propose smallest COMPLETE nontrivial technical repair, correctness/assumption/cost and benchmark plan; novelty still UNCLEAR until substantiated.
P1 — Conditional on surviving P0, minimal reproducible in-sandbox comparison framework with real baseline, reset/query/token/latency budget, ground-truth hidden relation precision/recall, temporal/transaction consistency. Requires separate PI authorization for code/implementation; no GPU/model training by default.
P2 — OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO, independent source/version control-flow audit only, see dedicated Codex prompt file; unlikely to create paper on its own. The copyable prompt was **already shown in last chat**, but NOT executed; avoid falsely recording 'prompt never delivered'.
P3 — Previous failed B/C branches remain archived; no new micro-iteration loop by default.

## 4. Hard science/novelty rules
- No claiming a publication-worthy method from a known missing assumption, toy indistinguishability, run-of-the-mill metamorphic comparison, event log, secure aggregation, obvious optimizer gradient or arithmetic cost sum.
- Explicitly label [FACT] with original URL/section/page, [DERIVATION] with assumptions, [SPECULATION] or [UNCLEAR] for open hypotheses.
- The original work's own limitations often ALREADY acknowledge the problem; neither misrepresent authors nor claim a security/privacy vulnerability absent proof.
- No claiming original published PDF/screenshot was audited when only abstract/indexed extract was available. Author-reported metrics are NOT independently reproduced. Prefer reading full original paper and checking the exact theorem/algorithm before building new idea.
- Evaluate novelty × technical nontriviality × importance × verifiability. Demand one coherent method that beats specified prior work on meaningful quality/cost or proves something genuinely new. Stop on direct prior art.
- At end of any PI-authorized iteration record STATUS/RESULT/NOVELTY/NEXT_TEST/STATE_UPDATE/PENDING_CODEX, one finding and one failure file if negative, append modular state exactly once, verify readback. Root STATE.md is at size limit; do not modify.

## 5. Exact current last state and pending Codex disposition
LATEST_COMPLETED: SYNTH-C14.
NEXT_CANDIDATE: SYNTH-C15_NOT_STARTED; not launched by creating this handoff.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO.
CODEx_PROMPT_PREVIOUSLY_DISPLAYED_TO_PI_IN_CHAT: YES (2026-10-26 summary answer).
CODEX_SUBMISSION_CONFIRMED: NO.
CODEX_EXECUTION_VERIFIED: NO.
C15 needs source-first research only. No C15 Codex task prepared or executed.
EAI-SYS unaffected: SCOUT-S54 latest, S55_NOT_STARTED.
Root STATE.md unchanged by handoff.

## 6. New chat recommended opening
User pastes a prompt explicitly asking to restore EAI-SYNTH from the above files; only once restoration read succeeds, ONE C15 source-first novelty gate, not C16 or broader autonomous loop. If source retrieval is inaccessible, report blocker, do not fake proof. User PI makes decisions.
