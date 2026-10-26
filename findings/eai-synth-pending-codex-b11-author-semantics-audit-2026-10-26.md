# EAI-SYNTH optional Codex task — B11/B12 author version and sampling-semantics audit
Status as of 2026-10-26: OPTIONAL_P2 / PENDING / NOT_EXECUTED / SUBMISSION_NOT_CONFIRMED.
THIS FILE SAVES A COPYABLE TASK, IT IS NOT PERMISSION FOR CHATGPT TO EXECUTE IT.
Original full task prompt was already displayed to PI in ChatGPT on 2026-10-26 in answer to '科研进展、Codex、优先级'. No evidence the PI sent it to Codex. Current EAI-SYNTH priority remains C15 original-source novelty gate, NOT this historical B11 task.

## Copyable Codex instruction

# Codex Task — EAI-SYNTH B11/B12 Author Implementation and Noise Semantics Audit

## Identity and isolation
- TRACK_ID: EAI
- ACTIVE_TOPIC: SYNTHETIC_DATA
- ACTIVE_SUBLINE: EAI-SYNTH
- TASK_ID: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO
- Research repository: BBBINGW/memory
- Do NOT launch C15 or make changes outside EAI-SYNTH.
- Perform an independent SOURCE AUDIT first, no assumptions about author code existence.

## Read before any work
1. findings/eai-synth-b11-sparse-segment-retry-semantics-gate-2026-10-25.md
2. findings/eai-synth-b12-2025-author-thesis-semantic-resolution-source-gate-2026-10-25.md
3. findings/eai-synth-STATE.md

Read AUTHORITATIVE sources only:
- He, Vershynin, Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv 2402.08012v3 original https://arxiv.org/pdf/2402.08012
- IEEE Transactions on Privacy (2024), DOI 10.1109/TP.2024.3486687 (final typeset source if genuinely accessible)
- Yiyun He 2025 PhD dissertation https://escholarship.org/uc/item/8pg3c2md , Chapter 5 Algorithm 10

## Primary objective
Determine whether an AUTHOR-MAINTAINED reference implementation, corrected journal version, official erratum, or explicit author clarification settles the lifetime of timestamp-indexed threshold-test noise lambda'_t when the same timestamp is encountered repeatedly after an empty segment.

Answer with exact evidence:
1. Is lambda'_t redrawn at EACH conditional evaluation, or reused once per absolute timestamp?
2. Does actual author's loop permit segment sealing with unchanged time t (zero progress)?
3. Can segment index j exceed the Binary Mechanism horizon / array assumptions?
4. Is indexing X_{t+1} at final timestamp valid under loop guards?
5. Does the final canonical source differ from arXiv v3 or dissertation enough to settle correctness?
6. Are claims about bounded number of independent noises / <=T segments actually justified under the confirmed source semantics?

## Cheapest verification
- First seek exact authoritative function/file/version and lines or publisher page. If unavailable, STATUS=SOURCE_UNRESOLVED and stop; DO NOT invent author intent from a hypothetical implementation, indexed snippet or third-party rewrite.
- Only if necessary to check the mathematics independently, create ONE deterministic, bounded, minimal LOCAL test with explicit maximum iterations:
   A. fresh test noise for each evaluation;
   B. reused timestamp-specific lambda'_t but fresh independent per-segment lambda_j.
- Do NOT attempt endless or expensive Monte Carlo to infer infinite expectation. Check B11 derivation analytically: under semantic B, for Z~discrete Laplace and p_z=P(lambda_j>=z-T0), the product tail P(Z=z)/p_z can be constant on infinitely many z, producing infinite E[R]. Under A initial successful test has probability >=1/2 leading standard geometric retries.
- Distinguish this hypothetical mathematics from confirmed author implementation. No assertion of privacy attack, theorem failure or bug without complete original-source verification.

## Restrictions
- No GPUs, LLM downloads, model training, API fuzzing of production systems, extensive simulations or dependency installations.
- No environment changes or research repository writes.
- No unbounded loops.
- Isolated local ephemeral evidence only if useful.
- If access to final IEEE paper or authentic code is blocked, report SOURCE_UNRESOLVED; no unverified replacement.

## Required final report
STATUS: CONFIRMED_FRESH / CONFIRMED_REUSE / OTHER_AUTHENTIC_SEMANTICS / SOURCE_UNRESOLVED.
SOURCE_EVIDENCE: Exact source origin/version/URL/path/function/page/line; distinguish primary code vs literature excerpt.
CONTROL_FLOW: Concrete same-timestamp retry behavior, segment t+j updates, end indexing.
MATHEMATICAL_CHECK: Confirm/qualify B11 conditional expectations and valid distribution assumptions.
PAPER_IMPACT: Whether this is only pseudocode ambiguity, complexity/support issue, correctness/utility flaw, or actual verified implementation issue.
NOVELTY: Distinguish trivial clarification from a real publishable new technique; never invent.
NEXT_TEST: Only cheapest remaining blocker, if needed.
REPO_CHANGES: NONE.
END.

## Connection to ongoing line
This OPTIONAL task is independent of C15's agent cross-app causal-constraint novelty gate. Do not start it automatically. Human PI may copy it to Codex later; current ChatGPT assistant must keep its execution status as UNVERIFIED until user provides a Codex output/artifact.
