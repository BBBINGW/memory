# 密码学 19.0 handoff

# Resume research — Session Handoff

## 0. Session identity and continuity

This is the successor to the completed research conversation 密码学 18.0.

Continue the SAME logical BOOT research program. Do not restart the research, reset the scientific state, or treat the handoff as a new research hypothesis.

NEXT_CONVERSATION_NAME: 密码学 19.0

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
LATEST_COMPLETED: Research Turn 25/25 — RMFE HElib rounding/carry commutation audit
CURRENT_STATUS: SESSION_RESEARCH_COMPLETE
NEXT_ITERATION: Research Turn 1/25 of the successor session, after restoring authoritative state
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
CONTINUOUS_AUTONOMOUS_RESEARCH: enabled

The current response is Research Turn 26 — HANDOFF ONLY. It performs no new substantive research and does not increment the completed session's research counter.

## 1. Durable Git authority

Repository: BBBINGW/memory
Branch: main

LATEST_REPORTED_CHECKPOINT:
011c7a17dabeeb9eca6e12059e14768e01c8416d

The session controller reports that the read-before-write Git checkpoint succeeded at this commit.

Earlier fallback authority:
24daf458c8100482c99a98017845dc548b93c059

The newer checkpoint supersedes the earlier fallback reference for this handoff. These commit values are supplied by the session controller, not independently obtained from a GitHub connector in this response.

GitHub Notes was unhealthy during the session. The verified local Git clone was designated as durable authority.

The successor must restore the latest authoritative BOOT state before making any scientific claim or repository modification.

Read, where available:

- RESEARCH_PHILOSOPHY.md
- AGENT.md
- findings/boot-STATE.md
- BOOT session handoff/checkpoint findings associated with commit 011c7a17
- Research Turn 23–25 findings
- Relevant B158 correctness, capacity, cost, and native-evidence findings
- findings/boot-PENDING_PI_DECISIONS.md, if present

Some supplied legacy STATE.md excerpts concern CGS and vFHE. They must not override the current explicitly selected BOOT track.

Do not claim connector-derived evidence unless the connector actually returns it.

Use read-before-write, preserve provenance, and verify any successful persistent checkpoint.

## 2. Research philosophy and authority

The human is the PI and retains final authority over:

- Research direction and major strategic pivots.
- The importance and publication value of a research gap.
- Acceptable cryptographic assumptions and trade-offs.
- Final scientific judgments.

The assistant acts as an autonomous FHE research student.

Core philosophy:

Existing work → exact gap → structural obstruction → smallest nontrivial repair → correctness/security/cost verification → publication judgment.

Default iteration:

smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only when warranted.

Each substantive research turn must pursue ONE primary hypothesis and ONE minimal decisive test.

Every hypothesis must have an explicit falsifier and conclude PASS, FAIL, or UNCLEAR.

Distinguish original source facts, mathematical derivations, native measurements, assumptions, and unverified conjectures.

Never interpret an implementation failure as a mathematical impossibility without supporting evidence.

A failed candidate should be KILLed or PARKed, followed by autonomous reprioritization within the current top-level research objective.

Candidate substantive-turn budgets:

SOFT_LIMIT: 8
HARD_LIMIT: 12

Prioritize important, technically nontrivial, measurable contributions rather than minor bookkeeping improvements.

## 3. Active BOOT research direction

ACTIVE_SUBLINE:
B158_CHECKPOINT_DECOUPLED_HALF_BASIS

Current focus:

RMFE-based BGV bootstrapping, particularly the possibility of reducing repeated bootstrapping-key reconstruction while preserving RMFE correction semantics, one non-linear DigitExtract, and practical throughput.

Relevant regime:

p = 5
w = 512
k = 5

The source-based and implementation comparisons involve HElib, Aung et al. PKC 2025, thin bootstrapping, Corr./TnM, and correction-style RMFE reconstruction.

The surviving technical direction is a carry-aware fusion candidate.

It must establish:

1. Correct plaintext semantics.
2. Correct modular rounding and carry handling.
3. Correct powerful-basis/slot/coefficient transformations.
4. Noise and capacity preservation.
5. Compatible evaluation-key assumptions.
6. Favorable latency and throughput.
7. A contribution not already subsumed by prior packed bootstrapping.

No publishable novelty or performance improvement has yet been established.

## 4. Session accomplishments — Turns 23–25

### Turn 23 — RMFE packedRecrypt prior-art boundary

Result:
PASS_PRIOR_ART_BOUNDARY_AUDIT

Key conclusions:

HElib's existing packedRecrypt and classical thick BGV/BFV bootstrapping already demonstrate shared bootstrapping-key operations.

Therefore, the generic idea of combining multiple ciphertexts into one bootstrapping-key inner product cannot independently establish novelty.

The checked HElib packedRecrypt interface uses binary plaintext reduction, while its digit-extraction path still processes multiple components.

It does not directly establish the requested p=5, k=5, RMFE correction-style fusion.

The narrower research opportunity is to combine shared reconstruction with thin-style single DigitExtract, including nontrivial rounding and representation correction.

Decision:

KILL the generic one-inner-product novelty claim.

CONTINUE examining the narrower carry-aware construction.

Artifact:
BOOT-T23-RMFE-PACKED-RECRYPT-PRIOR-ART-BOUNDARY-20261101.md

SHA256:
d98233a8955e6cde6171dfa943eae9af8060083faae23fd18221a0be7ae56007

### Turn 24 — Same-regime latency and throughput necessary conditions

Result:
PASS_NECESSARY_COST_GATE

Aung et al. PKC 2025 Table 2, for p=5, w=512, k=5:

SlotsToCtxts: 2.284 s
MultKey: 4.732 s
CtxtsToSlots: 0.078 s
DigitExtract: 4.240 s
Total: 11.334 s

Crucial qualification:

MultKey includes more than InnerProduct; it also includes modulus switching and linear transformations.

The whole MultKey time must not be counted as removable.

Conditional cost model:

T_new = 11.334 - 3.7856 alpha + H

alpha is the fraction of MultKey time that actually scales with the five-to-one fusion.

H is extra fusion overhead.

Under this model:

10% latency reduction with H=0 requires alpha >= 0.299.

20% latency reduction with H=0 requires alpha >= 0.599.

With H=0.5 s, the 20% target requires alpha >= 0.731.

The idealized upper-bound reduction is approximately 33.4%, not a measured prediction.

The historical source-reported correction/TnM throughput ratio against thin is approximately 0.832.

Under the stated fixed-output assumptions, exceeding that thin-throughput reference requires approximately:

T_new < 9.43 s

Do not mix absolute timings from different hardware environments to declare a native throughput victory.

Decision:

CONTINUE only if the native paired comparison demonstrates real performance improvement while preserving correctness, capacity, and security conditions.

Artifact:
BOOT-T24-P5W512-MULTKEY-AMDahl-THROUGHPUT-NECESSARY-GATE-20261101.md

SHA256:
dffdf1282fa76054c5d6015f5fbc06ee485fe9ec73475cc793f31615085bcb36

### Turn 25 — HElib modular rounding and carry commutation

Result:
FAIL_NAIVE_ADDITIVE_PREPROCESSING

Primary hypothesis:

Can the newMakeDivisible-and-division preprocessing be exchanged with summation without changing plaintext semantics?

Consider:

p = 5
q = 626
e' = 1

D(z) = (z + q v(z))/5

where v(z) belongs to {-2,-1,0,1,2} and is chosen so that the numerator is divisible by 5.

Exact counterexample:

D(1) = -125
D(2) = -250
D(3) = 251

Therefore:

D(3) - D(1) - D(2) = 626

and:

626 mod 5 = 1.

Thus the rounding-and-division operation is not additive even modulo the plaintext prime.

A source-shaped scalar rawModSwitch test used Q=65537, with original inputs 27, 29, and 56, yielding corresponding scaled outputs 1, 2, and 3.

Although the scaled outputs add correctly, preprocessing still creates the nonzero discrepancy.

This is a scalar arithmetic obstruction, not a demonstrated failure of a full encrypted BGV construction.

For five unweighted inputs, the exact identity is:

D(sum_i z_i) - sum_i D(z_i) = q C

where:

C = (v(sum_i z_i) - sum_i v(z_i))/5.

For five unweighted summands:

C belongs to {-2,-1,0,1,2}.

A lightweight exhaustive check examined all 3125 residue combinations and verified the identity.

Important limitation:

This bound does not automatically generalize to weighted RMFE reconstruction, arbitrary basis transformations, or ciphertext metadata.

Decision:

KILL naive additive preprocessing without carry compensation.

CONTINUE the carry-aware B158 candidate.

Do not interpret this counterexample as disproving an implementation that already accounts for carries.

Artifacts:

BOOT-T25-HELIB-P5-ROUNDING-CARRY-EXACT-GATE-20261101.md

SHA256:
4ba56f26d05ddc38116e262a8e254e2503120a00588eabbfe186cdd967b10717

BOOT-T25-P5-CARRY-ROUNDING-COUNTEREXAMPLE-20261101.py

SHA256:
684df8b792f88f424f838f1e4625c6a9bc6f56bb8d160733530ecfb7ac3d5411

The four Turn 23–25 artifact hashes were verified against accessible files in the conversation environment.

These artifacts were created in the conversation working environment. Their availability in the user's local Git checkout must be verified rather than assumed.

The session controller separately reports a successful Git checkpoint at 011c7a17dabeeb9eca6e12059e14768e01c8416d.

## 5. Latest Codex/native evidence

The authoritative handoff reports the following native execution result.

TASK_ID:
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

STATUS:
COMPLETED

RESULT:
FAIL_NATIVE_CORRECTNESS

Measured observations:

Vanilla HElib thin correctness:
PASS

Source-faithful Aung Corr./TnM:
Correctness mismatch in the first smoke test.

Candidate:
NOT EXECUTED

Formal five-warmup/twenty-measurement benchmarking:
NOT STARTED

Capacity:
NO VERDICT

Confidence intervals:
NO VERDICT

Throughput:
NO VERDICT

The experiment correctly stopped as required by the correctness-first contract.

The mismatch cannot automatically be attributed to the candidate because its execution was never reached.

The missing RM10/joint physical-hop audit prevents a stronger scientific conclusion from this comparator failure alone.

The exact keyset was generated and saved:

KEYSET_SIZE:
741 MiB

The keyset must be preserved. Do not repeat approximately 5.5 hours of key generation unless an independently justified new task explicitly requires it.

Native implementation commit reported:

4326551c9825f719414e094935ec1db554f0c6fc

No result from this experiment demonstrates a candidate performance improvement or scientific failure.

## 6. Codex task provenance — preserve exactly

The following entry is inherited from the orchestrator's durable task registry.

TASK_ID:
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

origin_session_id:
1f28610c-0aa3-4cce-9ec9-158d114c5ae8

origin_session:
密码学 17.0

origin_turn:
4

original_hypothesis:
Research Turn 4/25 — paired same-machine throughput gate.

The original gate established that absolute timings on different machines are not directly comparable. The next native comparison must measure vanilla thin, source-faithful Aung Corr./TnM, and the post-raw fusion candidate on the same machine and under a common protocol.

The original_hypothesis transport text was truncated by the session controller. The complete original value remains in orchestrator.db. Restore that complete value from the authoritative task registry when required; do not reconstruct missing words.

The supplied contract specifies:

HElib commit: acdb264…
m = 32768
p = 5
r = 1
bits = 400
single-thread execution
same BSGS+10 direct-RM10 evaluation-key set
same warmup and measurement protocol

Paired comparisons:

R_prior = (C_cand/T_cand)/(C_prior/T_prior)

R_thin = 5(C_cand/T_cand)/(C_thin/T_thin)

The factor 5 accounts for candidate packing of 10 slots against thin's 2 slots.

Original verdict rules:

STRONG_PASS:
lower95(R_prior) > 1 and lower95(R_thin) > 1

NO_PRIOR_WORK_GAIN:
upper95(R_prior) <= 1

PRIOR_ONLY_PASS_BUT_THIN_FAIL:
lower95(R_prior) > 1 and upper95(R_thin) <= 1

UNCLEAR:
Relevant confidence interval crosses 1.

Any candidate correctness mismatch must preempt performance interpretation.

working_directory:
/Users/bingwu/Developer/research-orchestrator

execution_backend:
Codex CLI / codex exec

model:
gpt-5.6-sol

reasoning:
medium

pid_or_remote_execution_identity:
54891

start_time:
2026-10-31T19:00:21.095Z

current_status:
COMPLETED

expected_artifacts:
[]

artifact_count:
197

evidence_status:
AVAILABLE

audit_status:
DELIVERED

result_delivered:
true

do_not_rerun:
true

commit:
4326551c9825f719414e094935ec1db554f0c6fc

durable_evidence_reference:
orchestrator.db codex_tasks.task_id=BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

Evidence paths:

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-run.log

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/artifact/logs/preflight2-progress.jsonl

/Users/bingwu/Developer/research-orchestrator/work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/source/benchmark.cpp

Task lifecycle rule:

This task is durable historical background state, NOT a request to execute.

The latest supplied registry status is COMPLETED, evidence AVAILABLE, audit DELIVERED, and result_delivered=true.

Do not reinterpret it as still running.

Do not restart, resubmit, duplicate, modify, or repeat this task.

Do not touch its source directory, working directory, binary, keyset, or original evidence except through a separately authorized, non-destructive read-only audit.

If other Codex tasks remain active in the authoritative orchestrator registry, they may cross session boundaries. Their results remain UNKNOWN until actually delivered.

Never restart background work merely because a research conversation has changed.

When the orchestrator delivers an outstanding native result, independently audit it on the latest active research session's next free substantive turn.

Do not reserve session-local turns for pending native results.

## 7. Current scientific boundaries and killed routes

Killed or parked conclusions:

- Generic one-inner-product novelty: already substantially covered by existing packed/thick bootstrapping.
- Naive additive preprocessing without carry compensation: disproven by exact arithmetic counterexample.
- Cross-branch HElib hoisting without compatible ciphertext identity: previously found unsupported.
- Earlier representation-only RMFE rescues: insufficient concrete improvement.
- Prior single-linear-phase novelty claim: not independently publishable.
- Current paired-throughput native run: comparator correctness failure; candidate and throughput remain untested.

Do not silently reopen a failed route without identifying a new assumption, technique, or falsifiable reopening condition.

The strongest surviving direction is carry-aware RMFE fused reconstruction, subject to all original correctness, capacity, security, and concrete-performance gates.

## 8. Next independent research action

The new conversation may begin a fresh substantive research turn only after restoring the latest BOOT authority and reconciling the task registry.

Choose the next highest-expected-information-gain, cheapest decisive test.

Priority should be given to unresolved correctness, representation, source-comparator, or evaluation-frontier questions that are independent of already running native work.

Possible existing audit obligations include:

- The source-faithful comparator's physical-hop correctness boundary.
- Actual carry correction versus weighted RMFE reconstruction.
- Powerful-basis and slot semantics.
- Evaluation-key compatibility.
- Same-machine throughput comparability.
- Noise/capacity and the publication-value frontier.

These are inherited audit priorities, not automatically authorized new primary hypotheses. Select only ONE after checking the latest durable state and avoiding duplicate work.

Do not fabricate a native result, operation count, or benchmark.

If the comparator has an implementation problem, distinguish that from a failure of the published construction.

If a candidate cannot cross the publication-value frontier, park or kill it and autonomously reprioritize within the BOOT objective.

## 9. PI decisions and autonomous continuation

PENDING_PI_DECISIONS:
none

PENDING_PI_DECISION is an advisory queue, not automatically a blocking state.

If future decisions enter the queue:

- Record the decision and exactly what it blocks.
- Separate blocked actions from reversible independent work.
- Record AI_PROVISIONAL_CHOICE when appropriate.
- Do not misrepresent provisional choices as PI approvals.

CONTINUOUS_AUTONOMOUS_RESEARCH:
enabled

NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION:
false

Routine authorized cheapest-decisive research and eligible Codex delegation do not require per-task PI approval.

However, never launch a duplicate native task, overwrite existing evidence, or interfere with an active Codex execution slot.

Respect model/reasoning requirements established by the current authoritative execution contract. Do not silently substitute another model, reasoning level, or paid API route.

WAIT_PI/STOP is permitted only when the reasonable top-level research frontier is exhausted, and the response must explicitly declare:

research_frontier_exhausted: true

## 10. Strict control protocol

Every normal substantive response in the successor conversation MUST end with exactly one valid control block:

<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

The displayed alternatives must be replaced with one concrete value each.

Additional mandatory rules:

For action=EXECUTE:
Include task_id containing the exact established identifier. Use EXECUTE only for a genuinely new, authorized execution task. Never use it to restart a pending or completed task.

For action=CONTINUE:
The assistant may perform further in-scope autonomous research. This is the required action while an existing native execution slot is occupied and independent research remains available.

For requires_pi=true:
The control block must explicitly include independent_research_available.

For action=WAIT_PI or action=STOP:
The control block must include:

research_frontier_exhausted: true

WAIT_PI/STOP must not be used simply because a candidate failed, a connector is unhealthy, a PI advisory decision exists, or one native task remains pending.

For milestone=true:
Use only for an actual substantial checkpoint or well-supported scientific milestone, not routine turn completion.

Every standard research answer should include:

- One primary hypothesis.
- One minimal decisive test.
- The evidence and result.
- PASS, FAIL, or UNCLEAR.
- Continue, refine, park, or kill recommendation.
- Durable provenance/checkpoint status.
- The valid ORCHESTRATOR_CONTROL block.

## 11. Session-transition directive

The completed session has exhausted Research Turns 1–25.

Do not perform any additional research in that completed session.

This handoff transfers the BOOT research authority, latest scientific conclusions, execution provenance, pending-task lifecycle rules, and autonomous-continuation policy to 密码学 19.0.

The successor should restore the latest Git state, reconcile the task registry, and proceed from the cheapest unresolved decisive test without restarting completed native work.

END_HANDOFF
