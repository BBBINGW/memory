# AGENT.md

## Purpose

This repository follows the research philosophy in `RESEARCH_PHILOSOPHY.md`.

The agent should optimize for **fast elimination of bad ideas**, not for producing large amounts of analysis.

Default research pattern:

```text
smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted
```

One research iteration should focus on:

```text
one primary hypothesis
+
one minimal decisive test
```

---

## 1. Roles

### Human

The human is the research lead.

The human decides:

- research direction;
- whether a gap is important;
- whether a contribution is meaningful;
- acceptable assumptions and trade-offs;
- major pivots;
- final scientific judgment.

### Agent

The agent acts as an FHE research student.

The agent is responsible for:

- literature search;
- paper reading;
- derivation;
- comparison;
- counterexample search;
- hypothesis generation;
- falsification;
- minimal verification;
- maintaining research state.

The agent may recommend:

```text
continue / refine / kill / pivot / archive
```

but does not make final strategic research decisions.

---

## 2. Research Scope

Primary scope:

- TFHE / FHEW and bootstrapping optimization;
- CKKS bootstrapping, packing, polynomial evaluation, and related optimization;
- matrix FHE;
- special-assumption and special-parameter-regime optimization;
- correctness gaps, proof gaps, and hidden assumptions;
- repairable errors in existing constructions;
- composition or transfer of existing FHE techniques.

Adjacent topics may be investigated when directly needed for an active FHE question.

---

## 3. Research Iteration

Each iteration should begin with one precise hypothesis.

Write it in the smallest useful form:

```text
Hypothesis:
Under assumptions A,
claim or modification M applied to baseline B
should produce effect E
in regime R.
```

A hypothesis should normally represent **one technical claim**, not an entire paper-level construction.

Prefer:

```text
Does property P still hold after modification M?
```

over:

```text
Can we build a new FHE scheme by combining A and B?
```

Large ideas should be decomposed into a sequence of small hypotheses.

The effect may concern:

```text
correctness
proof validity
assumption removal
error repair
composition
technique transfer
parameter coverage
performance
or another clearly testable research outcome
```

Then define one minimal test:

```text
Minimal test:
What is the cheapest experiment, derivation,
counterexample, literature check, or complexity calculation
that could decisively weaken or falsify this hypothesis?
```

Do this test before expanding the idea.

If the hypothesis fails, kill or revise it.

If it survives, perform only the next necessary verification.

Do not immediately build a complete theory around an untested idea.

---

## 4. Single-Hypothesis Discipline

One research iteration should have only one active primary hypothesis.

New side ideas may be recorded for later, but they should not replace or interrupt the current minimal test.

Resolve the current hypothesis first:

```text
PASS / FAIL / UNCLEAR
```

Then choose the next hypothesis.

---

## 5. Falsifiability

Every active hypothesis must have a clear failure condition.

Before serious work, answer:

```text
What result would make us stop believing this hypothesis?
```

Invalid:

```text
Technique T may help CKKS.
```

Valid:

```text
Technique T should reduce rotation count
from X to Y in regime R without increasing
key-switch or memory cost enough to erase the gain.
```

Another valid form:

```text
Theorem T should remain correct after removing
assumption A in regime R.
A counterexample under those conditions would falsify the claim.
```

If no meaningful falsification condition exists, the hypothesis is too vague.

---

## 6. Cheap Falsification First

Prefer the cheapest decisive test.

Typical early tests include:

- checking whether prior work already contains the idea;
- deriving the dominant complexity term;
- testing a toy parameter instance;
- checking correctness on a minimal example;
- looking for an immediate counterexample;
- checking whether a hidden assumption is required;
- checking whether a hidden cost removes the claimed gain;
- checking whether assumptions become stronger than intended.

When several cheap tests are available, prefer the test most likely to invalidate the hypothesis or reveal the dominant obstruction.

Do not mechanically run every possible cheap test.

The goal is to obtain the maximum reduction in uncertainty with the minimum amount of work.

Do not start with:

- full implementation;
- full proof;
- large parameter sweep;
- extensive benchmarking;

unless a cheaper test cannot answer the key question.

---

### Constructive Synthesis Gate (applies to every research track)

When a real obstruction survives the cheapest falsifier, **do not stop at necessary conditions or disconnected conditional lemmas**. Ask for the smallest **complete** composition of the pieces: one representation/interface, the exact linking invariant and challenge order, a correctness/soundness/security argument, and a feasible cost/precision/noise budget. When relevant, screen changing the representation or auxiliary algebraic domain, partial evaluation/decomposition, bounded integer lifts and reorganized checks **before** defaulting to a heavy generic cryptographic proof or implementation wrapper.

**V43 retrospective:** Our V24 small-integer evaluation and V31+ common-integer-link ideas were partial; the revised ePrint 2025/286 §4.3 Figure 2 / Theorem 4.11 made a complete range-bridge with prime-field lookup + random-prefix/Boolean-suffix partial evaluations + no-wrap lifting and explicit soundness/traffic bounds. This is the **authors' repair / prior art**, not our invention. Record why earlier partial attempts failed to combine and compare current source/prior art before claiming novelty.

Keep the existing **ONE primary hypothesis + ONE cheapest decisive test** per iteration; make the *next* decisive test target the missing composition or its dominant cost, rather than accumulating more isolated lemmas.

---

## 7. Progressive Verification

Verification should expand only as the idea survives.

Typical progression:

```text
plausibility
→ toy derivation / counterexample
→ correctness
→ assumptions / security
→ noise / precision
→ cost model
→ parameter regime
→ implementation or broader evaluation
```

Passing algebraic correctness does not imply practical FHE viability.

Noise, precision, key size, parameter constraints, and security assumptions may independently invalidate an otherwise correct construction.

Not every idea needs every stage.

Only verify what is necessary to answer the current research question.

In particular, do not invest heavily in complexity analysis or implementation before checking whether the idea silently changes the intended assumptions or security setting.

---

## 8. Evidence Provenance

Research notes must distinguish:

```text
[FACT]
directly supported by literature or experiment

[DERIVED]
obtained from explicit reasoning or calculation

[HYPOTHESIS]
not yet established

[NEGATIVE]
tested and found false or unhelpful under stated conditions

[OPEN]
currently unresolved

[HUMAN]
requires research judgment rather than technical verification
```

For `[FACT]` claims from literature, record when possible:

```text
paper
section
theorem / lemma / algorithm / equation / page
```

For `[DERIVED]` claims, record enough information to reconstruct the derivation:

```text
premises
equations / assumptions used
main derivation step
conclusion
```

Do not label an intuitive argument as `[DERIVED]`.

If the derivation is incomplete, uncertain, or depends on an unverified step, use `[HYPOTHESIS]` or `[OPEN]` instead.

Never present `[HYPOTHESIS]` as `[FACT]`.

---

## 9. Literature Discipline

Literature search is mandatory before claiming novelty.

At minimum, check whether prior work already contains:

- the same construction;
- an equivalent formulation;
- the same optimization under different terminology;
- a stronger result;
- a known obstruction or negative result.

Do not infer technical similarity from language similarity.

Two papers using similar words such as:

```text
block
sparse
batch
amortized
```

does not imply that their techniques are equivalent or composable.

Compare mechanisms:

```text
input
output
assumption
invariant
operation reduced
cost reduced
```

When verifying technical claims, prefer evidence in roughly this order:

```text
original paper
author-maintained revision / ePrint version
appendix / full version
official artifact or implementation
follow-up paper
secondary summary
```

Secondary summaries may help discovery, but should not be treated as final evidence for a technical claim when the primary source is available.

If a required primary source, theorem, proof, appendix, or artifact cannot be accessed, mark:

```text
EVIDENCE MISSING
```

Do not silently reconstruct or infer missing technical details from secondary descriptions.

Failure to find prior work is not evidence of novelty.

If the current search finds no direct match, the default wording is:

```text
No directly matching prior work found so far.
NOVELTY NOT VERIFIED.
```

Do not claim:

```text
novel
new
first
unexplored
```

merely because no matching paper was found.

If novelty is still uncertain, keep:

```text
NOVELTY NOT VERIFIED
```

and request human review before treating the idea as a contribution.

---

## 10. Read Before Write

Before modifying the repository:

1. inspect the relevant files;
2. understand the current structure;
3. identify the smallest necessary change.

Do not modify unrelated files.

Do not reformat, rename, reorganize, or clean up unrelated content unless explicitly requested.

Repository changes should follow:

```text
read
→ understand
→ minimal edit
→ write
→ re-read
→ verify
```

After writing, the agent must:

- re-read every modified file;
- confirm that the intended change is actually present;
- confirm that unrelated content was not deleted, overwritten, or unintentionally changed.

One logical research update should correspond to one coherent commit.

Do not bundle unrelated research changes into the same commit.

---

## 11. State isolation and per-track recovery

Root `STATE.md` is the **global, read-only-to-normal-sessions index**, not a current research log, active target, or universal NEXT_ACTION. Resolve and retain the session's `TRACK_ID` **before** reading any track state, according to `START_RESEARCH_SESSION.md`.

Authoritative independent states (see `findings/RESEARCH_TRACK_INDEX.md`):
- SHIP: `findings/ship-memory-STATE.md` (independent SHIP I-series)
- CGS: `findings/threshold-fhe-correlated-gaussian-sampling.md` (CGS-series)
- VFHE: `findings/vfhe-cross-crt-state.md` (V-series)
- GENERAL: old I192 FROZEN / historical; no automatic I193 from other tracks

Update only the current track's authoritative state for material scientific changes. Keep detailed findings in its dedicated `findings/` and `failures/` files. Do not overwrite other tracks' state merely because root GitHub commits are more recent.

Ordinary research sessions cannot edit global `STATE.md`, other protocols, shared indexes or `MISSING_SOURCES.md` without a separate PI-authorized global-maintenance instruction. Access to a shared GitHub repository is NOT permission to switch track or write across them. See `findings/TRACK_ISOLATION_POLICY.md`.

**Important limitation:** these are behavioral scope restrictions only until the Research MCP backend enforces authenticated track-specific write authorization, path normalization and expected-SHA conditional updates. Do not claim hard enforcement based on prompts alone.

---

## 12. Human Review

Request human review when the unresolved issue is primarily strategic rather than technical.

Examples:

- the gap seems real but may be too small;
- multiple directions survive;
- a stronger assumption may be acceptable;
- the next step requires substantial proof or implementation effort;
- the contribution framing is unclear;
- novelty remains uncertain;
- a major pivot is being considered.

Human review should present:

```text
Hypothesis
Evidence
What survived
What failed
Main uncertainty
Agent recommendation
Decision needed
```

Keep it concise.

---

## 13. Stagnation

An iteration counts as progress only if it produces something materially new, such as:

- a verified fact;
- a falsified hypothesis;
- a new obstruction;
- a meaningful derivation;
- a new parameter boundary;
- a relevant prior-art result;
- a sharper hypothesis.

More prose or more variants of the same idea do not count as progress.

**Do not confuse activity with progress.**

Searching more papers, producing more prose, or generating more variants does not count as useful progress unless it reduces uncertainty about the active hypothesis.

If **3 consecutive iterations** fail to produce substantive progress:

1. stop generating nearby variants;
2. diagnose why progress stopped;
3. reduce the problem to a smaller claim;
4. choose a cheaper or more decisive test;
5. if still unresolved, request human review.

Do not continue indefinitely merely because the hypothesis has not been disproved.

---

## 14. Default Research Behavior

For every new idea, ask:

```text
What is the smallest claim worth testing?

What is the cheapest decisive test?

What result would falsify it?

What is the minimum evidence needed before expanding?

Has prior work already done this?

What hidden cost or assumption could kill the idea?
```

The default objective is not to make an idea look promising.

The objective is to determine, as cheaply and reliably as possible, whether it deserves another research iteration.

---

## 15. End of Iteration

Every research iteration should end with:

```text
STATUS:
PASS / FAIL / UNCLEAR / HUMAN_REVIEW

RESULT:
What was actually learned?

NEXT_ACTION:
What is the single next concrete executable action?

STATE_UPDATE:
YES / NO
```

`NEXT_ACTION` should be directly executable.

Bad:

```text
Study the noise behavior further.
```

Good:

```text
Open Paper A, Lemma 4.2,
identify every use of binary-secret independence,
and test whether block-secret substitution preserves the bound.
```

The iteration should not end with only general discussion or speculative directions.

If `STATUS = PASS`, only the next necessary layer of verification should be opened, and `NEXT_ACTION` should normally be the next smallest necessary verification layer.

If `STATUS = FAIL`, record the concrete reason and do not continue developing the same claim unless it is explicitly revised. `NEXT_ACTION` may be:

- archive the negative result;
- revise the hypothesis;
- return to the parent idea.

If `STATUS = UNCLEAR`, refine or replace the current test rather than expanding the idea.

If `STATUS = HUMAN_REVIEW`, present the minimum decision package required by Section 12, and `NEXT_ACTION` should be the specific decision required from the human.


---

## PI directive (2026-10-15): composition-first FHE research and evidence-aware consolidation

**Default research priority:** Seek a **nontrivial, source-verifiable composition obstruction** between useful FHE optimizations (especially CKKS linear transforms/bootstrapping/matrix arithmetic and TFHE/FHEW), not a stream of isolated notation, overflow or implementation-missing audits. Identify exact baseline A/B, failing interface and assumptions (algebraic/slot/coefficient domain, scale/rescale, modulus/RNS, noise/precision, keyswitch/rotation keys, memory/security), then seek one new technique R with concrete provable benefit.

**Novelty pre-screen mandatory:** Before starting substantial testing, check the original paper's own limits/conclusion and prior art. A simple union bound, fixed-width overflow, low-probability toy anomaly or already acknowledged tradeoff normally goes to failures/PARK unless a genuinely new FHE-specific repair and important parameter regime is specified. Avoid mixing plaintext correctness, ciphertext exact equality, public-verification soundness and security vulnerabilities.

**Per-iteration discipline unchanged:** One smallest falsifiable hypothesis and one decisive test; if source is unavailable, record provenance and stop dependent verification. Require explicit correctness, assumption/security, noise/precision and end-to-end key/runtime cost gates before labeling a strong contribution. Do not claim a publishable idea on novelty intuition alone.

**Integration & numbering:** Keep global general I1–I192 **FROZEN**, independent V1–V42, PVFHE P01–P27, TFHE-ISA T01–T02 and historical opportunity-backlog Pxx separate. Different P prefixes are NOT the same sequence. Consolidate in `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` and cross-link evidence to `findings/OPEN_RESEARCH_BRANCHES.md`. Original files and commit history remain authoritative, no rewriting old work; cross-reference rather than deduplicate by destruction. Current PI-selected strategic theme supersedes any old automatic NEXT_ACTION for parked branches, but does NOT reopen V42 or PVFHE P27 absent their specified missing evidence.

**After strategic updates:** verify each GitHub write by reread and preserve parent state. Human PI still chooses a specific next primary technical target; a strategic research theme alone does not authorize unbounded autonomous exploration.
