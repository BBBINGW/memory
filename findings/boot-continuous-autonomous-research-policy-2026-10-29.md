# BOOT Continuous Autonomous Research Policy

Date: 2026-10-29  
PI authority: explicit policy update  
Session at activation: 密码学 11.0, after Research Turn 2/25

## Authorization model

`CONTINUOUS_AUTONOMOUS_RESEARCH: ENABLED`

`NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false`

Within the current PI-authorized top-level BOOT objective, Research GPT may autonomously define and number hypotheses/iterations, search and derive, redesign constructions, perform cheap falsification, choose minimal experiments, delegate necessary native/code/server execution to Codex, audit returned evidence, and continue/refine/park/kill/reprioritize candidates. PI retains top-level direction, final contribution/publication judgment, explicit pause/kill/reprioritization, and strategic changes outside the authorized objective.

## Current top-level objective

Repair the core B158 construction without relying on a simple parameter relaxation. Prioritize structural changes to representation, multiplication law, or noise geometry. If bounded exploration of the B158 redesign family reaches a low-information frontier, park it with complete evidence and autonomously reprioritize the next highest-value surviving BOOT candidate.

## Current boundaries

- `B175_DIRECT_SI_POINTWISE: KILLED`.
- `B158_OVERALL: ACTIVE_REDESIGN`.
- `B176: REPRESENTATION_LAYER_REDESIGN / AUTHORIZED`.
- B177, B178, and later iterations do not require per-iteration PI authorization when they remain inside the top-level objective and existing kill boundaries.
- Cheapest-decisive Codex execution within that scope is automatically authorized; Codex evidence must return to Research GPT for independent audit.

The following cannot be the primary rescue or innovation: only raising Q; only changing k0/H/s; parameter sweeps; gadget-base tuning; few-bit noise tuning; key-switch-only tuning; relinearization-only tuning; quantization-only tuning. A genuinely new construction may later optimize such parameters, but cannot conceal a structural failure behind them.

Priority structural mechanisms include representation change, multiplication-law change, structured selectors, external products, dual-lineage merge, and scheme/ring/interface switching, plus any other construction that genuinely changes the relevant noise geometry.

## Candidate exploration budget

- soft substantive-turn budget: 8;
- hard substantive-turn budget: 12.

At the soft budget, review information gain, mechanism progress, native signal, novelty potential, and expected value of the next test. At the hard budget, park by default if there is no validated candidate, new theorem/claim, positive native signal, credible novelty, or high-value next test. A real breakthrough may justify continuation with an explicit expected-information-gain rationale.

A parked route must record what was tried, why it was parked, what evidence would reopen it, the current best bound, prior art, and artifacts. Park is not permanent kill.

## PI decision semantics and stop rule

`PENDING_PI_DECISION != STOP`. Research GPT may record an `AI_PROVISIONAL_CHOICE` when the choice is reversible, preserves alternatives, has acceptable cost, and stays inside the authorized objective. It is not final PI approval.

The system may enter `WAIT_PI` only after the authorized top-level research frontier is exhausted, or for PI/system terminal blockers such as explicit PI stop, quota exhaustion, unavailable required model/reasoning, unrecoverable adapter/Codex/orchestrator failure, or unsafe durable-memory failure. A failed iteration, candidate, family, milestone, or pending strategic decision is not sufficient.

## Resolution

`BOOT-DECISION-001: RESOLVED_ALLOW_AUTONOMOUS_STRUCTURAL_REDESIGN`

The direct B175 mechanism remains killed, while one bounded proposal is no longer the ceiling: the PI authorizes continuous structural redesign and autonomous in-scope reprioritization under the budgets and boundaries above.

