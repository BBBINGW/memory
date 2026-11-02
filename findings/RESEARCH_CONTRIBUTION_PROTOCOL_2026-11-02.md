# Paper-First Research Contribution Protocol — 2026-11-02

**Status:** Normative methodology and persistence upgrade for future orchestrated research. This protocol does not change any existing scientific conclusion, active `TRACK_ID` / `ACTIVE_SUBLINE`, pause decision, task identity, artifact provenance, or Research Turn count.

## Objective

The research controller optimizes for a complete publishable contribution:

```text
Important Problem
→ Novelty Preflight
→ Constructive Design
→ Complete Correctness
→ Security
→ Scientific Value
→ Independent Audit
→ Paper Contribution
```

The smallest falsifiable claim and cheapest decisive test remain mandatory, but are no longer sufficient by themselves. Every test must reduce a named uncertainty for the complete paper thesis, construction, correctness, security, value, or audit verdict.

## Durable PAPER_CANDIDATE

Maintain exactly one `ACTIVE` candidate and at most two ranked `BACKUP` candidates. Preserve these fields across turns and handoffs:

```text
PAPER_THESIS
IMPORTANT_PROBLEM
BASELINE
CLOSEST_PRIOR_ART
NEW_MECHANISM
CONTRIBUTION_TYPE = ALGORITHM | SYSTEM | SECURITY | THEORY | UNKNOWN
FULL_CONSTRUCTION
CORRECTNESS
SECURITY
NOISE_PRECISION_DFR
VALUE
CRITICAL_BLOCKER
NEXT_DECISIVE_TEST
NOVELTY_STATUS
PAPER_READINESS
REOPEN_CONDITION
CONSTRUCTIVE_DESIGN_SPEC
CORRECTNESS_GATE
SECURITY_GATE
VALUE_GATE
AUDIT_GATE
BASELINE_CORRECTNESS
```

`UNKNOWN` is a valid state and must never be rewritten as a scientific PASS or FAIL without evidence. `PAPER_READY` requires novelty clear plus PASS for complete baseline correctness, candidate correctness, security/noise compatibility, scientific value, and independent raw audit.

## Phases and transitions

The durable phases are:

1. `PROBLEM_SELECTION`
2. `NOVELTY_PREFLIGHT`
3. `CONSTRUCTIVE_DESIGN`
4. `CORRECTNESS_GATE`
5. `SECURITY_GATE`
6. `VALUE_GATE`
7. `PAPER_AUDIT`

Novelty preflight precedes expensive derivation or execution. A prior-art collision blocks novelty passage. A promising candidate must state a constructive design covering algorithms, interfaces, parameters, and invariants. If no credible new mechanism exists, record `NO_CREDIBLE_NEW_MECHANISM` and PARK it.

A valuable obstruction that is not a strict no-go permits one bounded representation/protocol redesign. Repeated local FAIL results without mechanism progress do not justify endless variants. If a candidate fails and a backup remains, promote the highest-ranked backup; do not wait for PI merely because the first candidate failed.

After two consecutive low-information turns, issue `VALUE_REVIEW`; three are an absolute review point. Count progress only when a turn advances a mechanism, theorem, correctness, security, value, novelty, or named critical uncertainty. The 25 substantive turns are capacity, not a quota. Turn 26 is handoff only.

## Synchronized evidence gates

Correctness, security, and value advance together. `PASS_TOY`, `PASS_STATIC`, and `PASS_MATH` are evidence grades, not paper readiness. A performance verdict is blocked until the baseline is correct and conditions are matched.

Native work follows this order:

1. Source audit
2. Small correctness canary
3. Exact parameter/interface verification
4. Complete baseline correctness
5. Candidate correctness
6. Noise/security compatibility
7. Matched benchmark
8. Independent raw audit

Pending or cross-session Codex/native work retains its original task id, origin session/turn, hypothesis, working directory, backend, model/reasoning provenance, process identity, start time, status, expected artifacts, evidence/audit status, result-delivery state, and `do_not_rerun=true`. Never infer a pending result, restart it during handoff, or reserve a session-local turn for it.

## Memory and control-plane rules

GitHub Notes is the primary memory interface when healthy. If it is unavailable, only a verified local Git clone with checked branch/head may act as fallback authority. Connector failure alone is not a scientific blocker.

The paper-candidate update is durable research state, not a new control-plane action. Existing `ORCHESTRATOR_CONTROL` actions and exactly-once reconciliation rules remain unchanged. Infrastructure repair may reconcile an already-complete turn; it must not alter scientific content, fabricate progress, duplicate a task, or increment a logical turn twice.

