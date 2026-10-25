# EAI · Agent A1 — Opaque revocation / irreversible effect no-go (2026-10-25)

**TRACK_ID:** EAI, exploratory AI Agent Reliability subline A1. This is one source-first prescout falsification, not a newly numbered formal EAI-SYS S55 or EAI-P iteration. User is PI.

## One primary falsifiable hypothesis

**H-A1:** Under an opaque external side-effect tool API with (i) a prior separate authorization read, (ii) authorization revocation events not observable at Agent A's mediation boundary until after the effect, and (iii) no atomic target-side auth check + effect commit, a controller can satisfy BOTH:
- S: do not release an irreversible effect after its authority is revoked at the authoritative target;
- L: when authorization remains valid, complete the requested effect instead of blocking all cases.

**Cheapest decisive test:** exactly ONE two-world, two-agent, two-tool indistinguishability trace; inspect published original concurrency/transaction/authorization mechanisms for prior art. No GPU/LLM/remote tool experiments.

## Two agents / two tool interfaces

A = sending agent, B = authority-modification agent; interface 1 is `permission.read_or_revoke` (A reads, B may revoke); interface 2 is `sender.send(payload,dest)` (irreversible, without authoritative conditional authorization at effect time). **Crucial assumption:** B's authoritative revocation event is not shared with A's monitor; otherwise the two worlds are distinguishable and the no-go does not apply.

At t0 authority allows send; A reads `allow=1` and prepares intent.
At t1 W0 B does nothing to that permission (still allowed); W1 B commits revocation (forbidden) at a separate authoritative service, not observed by A's monitor.
At t2 A/monitor with the SAME observation must choose whether to invoke `send`.
Correct W0 outcome = send (L). Correct W1 outcome = block (S).

**[DERIVED — exact proof]** Let `p` be probability of sending after the shared observation. Both worlds induce the same `p`. Unauthorized-effect probability in W1 = `p`; blocked-authorized-effect probability in W0 = `1-p`. Their sum equals 1 and maximal error >=1/2; no deterministic or randomized strategy simultaneously guarantees S and L. A fresh separate permission check merely moves the last-observation boundary; with non-atomic effect, a revocation can still occur in the gap (TOCTOU). This is a classical observation/atomicity impossibility under the stated assumptions, not a new cryptographic theorem.

### Where the impossibility stops

Target-side atomic `send_if_authorized`, a genuinely authoritative effect-time capability check, full mutual visibility/linearizable synchronization of revocation through the mediator, or conservative denial of any ambiguous effects change assumptions and avoid the counterexample. Distinguish dispatch-time vs actual effect-time, especially for asynchronous sends. If a remote call timed out with no idempotency/status receipt, generic exactly-once effect cannot be inferred; compensating an irreversible real-world effect is not the same as undo.

## Direct prior-art checks and exact source limits

**[FACT/full readable original] CoAgent**, https://arxiv.org/html/2606.15376, §5.1 A1–A3 presuppose mediation of every shared-state operation with declared footprints and agent self-healing; §5.3 proves notified serializability at GlobalQuiet; §6.3 explicitly **delays unrecoverable writes** (mail/payment) until all earlier-serialization agents commit. This already combines multi-agent concurrency with handling of irreversible operations **inside its model**. Notified serializability need not guarantee linearizability against an *unobserved external authorization* change, but that is an assumption boundary, not a CoAgent counterexample.

**[FACT/full readable original] Cordon**, https://arxiv.org/html/2606.17573, §3.1 Table2 I3/I5/I6/I8 (staging, complete mediation, scoped authority), §§4.2–4.6 (dispatch interposition, shadow state, effect outbox, idempotency, commit/recovery) explicitly validates effects before release. §6.5 explicitly limits guarantees to mediated observable operations; opaque/unobservable external side effects are out of containment or blocked. Thus “validate authority and stage effects” is already known, and opaque tool exclusion is not a new construction.

**[FACT/publisher abstract ONLY] DelAct**, https://ieeexplore.ieee.org/abstract/document/11661202, IWQoS2026: stable commit identifiers, idempotence, in-doubt verification, compensation, event replay already described; full technical paper unavailable in this audit.

**[FACT/primary abstract ONLY] DelegateGuard**, https://arxiv.org/abs/2610.16005, 2026-10-12: purpose/label/operation/sink bounded capabilities, per-action external reference monitor, delegated revocation trace invariant. Full HTML/PDF unavailable via web in this audit: do not attribute extra theorems.

**[FACT/primary abstract ONLY] From Evidence to Effect / WTB**, https://arxiv.org/abs/2609.08472v4, revised **2026-10-19**: authority-sufficient observations and durable effects bound to execution identities, transactional publication/recovery. Closely overlapping newer prior art; full technical text not accessible this turn.

**[FACT/primary abstract ONLY] ResidualAuth**, https://arxiv.org/abs/2609.08062: residual authorization state and execution-time monitor already studied.

**IMPORTANT:** No claim that any published framework has an exploitable flaw. Under fully mediated tools, the simple situation is substantially covered; outside mediation and target enforcement, the desired S+L combination is unachievable. Full four-system joint theorem audit is NOT claimed: two full texts, multiple abstracts. Need an actually different feasible and prior-art-surviving hypothesis to justify further A1 work.

## Research decision

**STATUS:** `FAIL_A1_OPAQUE_REVOCATION_SAFE_AND_LIVE / PASS_TWO_WORLD_NO_GO / HUMAN_REVIEW`.
**RESULT:** With no observable revoke or atomic effect-time authorization, safe+live effect execution is impossible; with observable/conditional tools, known CoAgent/Cordon/DelegateGuard/WTB mechanisms already overlap heavily. No novel complete protocol or independently validated benchmark gain found.
**NOVELTY:** `NOT_ESTABLISHED`.
**RECOMMENDATION:** `PARK_BROAD_AGENT_A1_CONJUNCTION` pending a genuinely specific distinguishable source-level gap. Do not reinterpret the no-go as a paper theorem or a deployed attack.
**NEXT_TEST:** `NONE_FOR_THIS_OPAQUE_NO_GO`.
**NEXT_ACTION:** `PI_REVIEW_A1_PARK_AND_DECIDE_B1_SYNTHETIC_DATA_BIASED_VERIFIER_COVERAGE_GATE_VS_NEW_AGENT_MECHANISM`; no automatic domain pivot.
**STATE_UPDATE:** `YES` after GitHub commit and readback.
