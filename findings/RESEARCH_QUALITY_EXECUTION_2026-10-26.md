# Cryptography Research Quality & Execution — 2026-10-26

**Status:** PI-requested methodology upgrade. This document is normative for future research methodology but **does not authorize restarting paused tracks, Codex/remote runs, editing other tracks, or rewriting historical findings**. Complement `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, and `START_RESEARCH_SESSION.md`. Existing contradictory older statements need explicit reconciliation; never silently reinterpret scientific outcomes.

## Preserve proven strengths

- One smallest falsifiable **primary hypothesis** and one cheapest decisive test each iteration; proactively find counterexamples, not evidence confirming a favorite idea.
- Progressive verification: primary source → plausibility/novelty → minimal toy/derivation → correctness → assumptions/security → noise/precision/DFR → complete cost → reproducible native performance, only as warranted.
- Original citations include paper version, section, algorithm, theorem, equations/pages and code revision where accessible. Keep [FACT], [DERIVED], [SPECULATION], [NEGATIVE], [OPEN] separate.
- Read-before-write, coherent updates, evidence and negative-result preservation, raw artifact audit; never conflate Codex-reported with native independently repeated.
- Human PI selects topics, accepts assumptions/tradeoffs, approves heavy work, and judges contribution; AI research student actively recommends continue / bounded redesign / park / kill / pivot / human review.
- VFHE lesson: several correct necessary lemmas are **not** a complete repair. Require a sufficient combined representation, transcript, proof and cost. October 2026 repaired vFHE range protocol is **author prior art**, not ours.

## Immediate strategic changes — P0/P1/P2

**P0: Problem-first, stop paper roulette.** Start with a source-verified significant unsolved bottleneck and concrete baseline, not reading arbitrary new papers and attaching techniques. Work one PI-selected track and one primary hypothesis. For a truly valuable *interface* obstruction, consider one bounded alternative representation/protocol redesign rather than abandoning at the first naive patch; do not indefinitely generate variants.

**P1: Early triple pre-screen.** Before long derivations, Codex or benchmarks, verify **current primary source + nearest equivalent prior art + genuinely new mechanism/invariant + optimistic end-to-end gain**. Quantify the entire baseline and candidate at matched security/precision/DFR. If critical Algorithm/Definition/KeyGen/proof is unreadable, record `SOURCE_BLOCKED` and `MISSING_SOURCES.md`; at most one useful *source-independent* necessary-condition test, then park dependent work. No abstract reconstruction presented as actual author algorithm.

**P2: Convert failures into reusable mechanisms.** At each important failure, cross-read related prior track findings as read-only and record: `obstruction → naive repair and why it fails → potential new interface/invariant → one cheapest killer test → source/evidence`. Do not restart paused research merely by comparing its lessons.

## Seven observed problems → actionable fixes

| Failure | Required mitigation |
| --- | --- |
| 1. Topics scattered, repeated pivots | Maintain a small ranked backlog (normally 2–3); one active PI-selected subject, and a reason to read each paper in terms of its actual bottleneck. 'Continue' is not permission to switch tracks. |
| 2. Missing original technical text | Fetch current PDF, source equations, code or ask PI for full source. If inaccessible: SOURCE_BLOCKED, mark provenance, stop source-dependent toy loops. |
| 3. Novelty reviewed too late | Mechanism-level equivalence search *before* heavy proof/experiment; search exact method under alternate vocabulary, author's own limitations, stronger nearby techniques. Reaudit before contribution claim. |
| 4. Too many local PASS labels | Clearly distinguish PASS_MATH, PASS_TOY_EXECUTED, PASS_NATIVE, SECURITY_PROVED and PUBLISHABLE. Give hypotheses, quantifiers and restricted calculation models. A valid algebraic identity or source-shaped cost is not an end-to-end algorithm. |
| 5. No full gain criterion | Fix baseline, workloads, params, key assumptions, DFR/precision/security. Count EP, KS, NTT/FFT, conversion, RNS/modulus/scale/rescale, key material, offline work, online latency, throughput, memory/RSS, communication. Estimate optimistic net gain; if immaterial, park. PI decides threshold. |
| 6. Failure not converted to ideas | Classify fundamental lower bound vs current-interface vs secret/security/noise vs performance vs prior-art vs missing source; for important interfaces, attempt ONE falsifiable representation-level repair before pivoting. Avoid cosmetic repeated toy variants. |
| 7. Stale fragmented state | Mark OFFICIAL_COMPLETED vs PRESCOUT/PARTIAL vs PAUSED. Reconcile root STATE with latest *verified* snapshots and preserve both until reconciled; never turn a Codex summary or planned script into an audited native artifact. |

**Value-review trigger:** After 2–3 low-information probes (even mathematical PASSes) without a source-backed new invariant and plausible end-to-end gain, stop and issue `VALUE_REVIEW`: why work stalled, retain/reformulate/park recommendation, missing evidence, and PI decision if needed. The existing three-iteration stagnation rule still applies. No automatic stop or pivot without PI judgment.

## Execution gates

### G0 — Restore

Read `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, this guide, `START_RESEARCH_SESSION.md`, root `STATE.md`, relevant topical findings/failures and the latest verified dated handoff. PI's explicit latest selection overrides a stale heading. If sources conflict, mark `STATE_STALE / RECONCILE_REQUIRED`, not blindly overwrite. The old track infrastructure policy documents are historical; that does not undo PI-enforced research boundaries or pause decisions.

### G1 — Candidate preflight card

```text
TRACK / OFFICIAL_COMPLETED or PRESCOUT or PAUSED:
SOURCE: paper, date/revision, exact Algorithm/Definition/Lemma/page, version and hash if verified
BASELINE: source/code commit, workload, secret, N/q/slots, key assumptions, precision/DFR/security
IMPORTANT GAP: exact costly operator/limitation and why previous work cannot avoid it
CLOSEST PRIOR ART: mechanism equivalence and novelty status (UNVERIFIED unless substantiated)
NEW MECHANISM: old interface → obstruction → NEW linking invariant/representation
OPTIMISTIC NET COST: baseline vs proposed with all new keys, conversion, noise and levels
ONE PRIMARY HYPOTHESIS: Under A, method M on B produces E in R
ONE CHEAP FALSIFIER / stopping condition:
DECISION: TEST / BOUNDED_REDESIGN / PARK / HUMAN_REVIEW
```

### G2 — Typed construction, not superficial combination

Track input/output ciphertext types; coefficient/slot basis; key lineage and secret correlation; gadget digits/automorphisms; modulus, RNS, scale/rescale and guard slots; all ciphertext outputs and the next stage's requirements. First show where naive A+B fails. Propose a genuinely new joint invariant with a **complete** correctness/security/noise/cost path. If an added normalizer needs quadratic KDM keys, secret ratios, extra levels or independent error, it is not free. For important obstacles allow one bounded redesign and retest.

### G3 — One decisive falsifier

Prefer actual source-equation contradiction, small exact counterexample, clear secret/interface compatibility condition, nearest-prior-art equivalence or optimistic ceiling. If mathematical only, label DERIVED; if code was truly executed, save reproducible input/output. Explain whether failure kills generic algorithm or only a restricted representation. Do not present toy results as honest DFR.

### G4 — Complete contribution checks

1. Correctness of *whole* ciphertext/output, not just plaintext scalar.
2. Security game/assumptions and concrete parameters (KDM/circular/related keys/hints).
3. Noise, precision/DFR, error tails, rounding, guard slots and modulus budgets.
4. Matched complete end-to-end latency, throughput, online/offline, keys, memory, scratch, EP/KS/FFT/NTT, conversions and communication.
5. Novelty audit of true mechanisms, not search-result headlines; identify what was not known before.

### G5 — Native work only when justified and authorized

Require PI approval for Codex/GPU/server/model/code changes. Pin original revision and exact candidate; compare matched security, parameters, input distributions, keys, warmup, paired repeated trials, all relevant costs, correctness and failure thresholds. Do not claim speed from symbolic counts or success from an unaudited ZIP.

**Evidence levels:** `DERIVED`; `TOY_EXECUTED`; `CODEX_REPORTED`; `RAW_AUDITED` (raw source/manifest independently inspected, not rerun); `NATIVE_REEXECUTED`; unresolved `SOURCE_BLOCKED`, `NOVELTY_UNVERIFIED`, `SECURITY_UNCLEAR`, `DFR_UNCLEAR`.

## Cross-track transferable warnings

- **VFHE:** partial CRT/field checks require a global binding invariant; authors already published their October repair.
- **SHIP:** one-hot selector identities may be existing CMux techniques; secret-coupled columns and key security remain, even with proven prepared-payload savings. RSS delta ≠ intrinsic key bytes.
- **CGS:** disclosing one correlated hint is not equivalent to safely disclosing shifted hints for multiple related secrets; don't attack a stronger game and call it original.
- **BOOT NTRU:** type-preserving transformations may demand encrypted key powers and amplify noise; check key and automorphism interfaces.
- **BOOT CKKS:** reducing FFT diagonals often increases modulus-level costs; show real Pareto not just arithmetic counts.
- **BOOT TFHE:** sample extraction requires a complete LWE mask; removing a KS may shift work to the next PBS.

## Closing record and state discipline

```text
TRACK / OFFICIAL or PRESCOUT / SOURCE VERSION:
PRIMARY HYPOTHESIS + SINGLE MINIMAL TEST:
STATUS: PASS / FAIL / UNCLEAR / SOURCE_BLOCKED / HUMAN_REVIEW
EVIDENCE: DERIVED / TOY_EXECUTED / CODEX_REPORTED / RAW_AUDITED / NATIVE_REEXECUTED
RESULT / precise limitations:
NOVELTY / IMPORTANCE / optimistic complete net gain:
GATES: correctness | security | noise/DFR | total cost | prior art
DECISION: CONTINUE / BOUNDED_REDESIGN / PARK / KILL / PIVOT / HUMAN_REVIEW
NEXT_TEST: executable single check or NONE_WHILE_PAUSED
STATE_UPDATE: YES (verified path+commit) / NO (reason)
PI_DECISION_NEEDED:
```

Only promote decision-changing reproducible work into proper topic findings/failures. Methodology updates **do not** advance BOOT-B123, SHIP-I407, CGS-52, VFHE-V43 or change their pause/selection decisions. Read-before-write, smallest coherent edit, reread content and actual commit verification. A strong negative test is progress *only if it changes the next research decision*.
