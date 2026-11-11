# BOOT / B158_OVERALL — Research Turn 25/25
## PROBLEM_SELECTION — centered Q→QMul lift before B175 SI tensor

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-centered-qmul-lift-pointwise-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: SOURCE / MATH
Native: NOT RUN

## Distinctness

The durable state entering Turn 25 had ACTIVE=UNKNOWN. This candidate is distinct from the recently closed gauge-search, sparse-key, reciprocal public-preconditioning, ring-switch, lazy-relinearization and standard RGSW families.

The candidate directly targets the dominant B175 source-level uncertainty: component-lift / Q-carry geometry inside scale-invariant tensoring. It asks whether the SI path basis-extends ciphertext components from Q into QMul using a non-centered residue representative, and whether replacing that step with an exact centered integer lift could remove enough Q-carry to recover the approximately 16 required-bit deficit.

## Registered decisive test

QUESTION:
Does Lattigo v6.2.0 BGV scale-invariant tensoring use a non-centered Q→QMul component lift, so that replacing it by an exact centered integer lift would constitute a genuine new representation mechanism with a plausible fixed-Q noise benefit?

CURRENT_BELIEF:
`ModUpQtoP` likely already performs a centered basis extension even though its internal helper `ModUpExact` is explicitly non-centered. If the BGV `modUpAndNTT` path calls the centered wrapper, the proposed mechanism is already the stock baseline and cannot be admitted as a new candidate.

CHEAPEST_DECISIVE_TEST:
Audit the exact call chain in Lattigo v6.2.0:
1. `schemes/bgv/evaluator.go::modUpAndNTT`;
2. `ring/basis_extension.go::ModUpQtoP`;
3. internal `ModUpExact`;
and derive the integer representative that reaches QMul for an arbitrary coefficient x mod Q.

IF_PASS:
If stock `modUpAndNTT` extends an uncentered representative and a centered replacement is source-compatible, retain the candidate and next derive an optimistic carry/noise ceiling before any native canary.

IF_FAIL:
If the stock path already maps each Q coefficient to the exact centered integer representative in QMul, PARK immediately as baseline collision. No native execution or implementation is justified.

IF_UNCLEAR:
If the source leaves the representative ambiguous, preserve UNKNOWN and require a tiny source-shaped arithmetic canary only; do not infer benefit.

WHICH_PAPER_GATE_CHANGES:
Killer gate (2), stock/source construction feasibility and distinctness. A FAIL also collapses killer gate (3) because a representation-identical candidate has zero possible whole-system delta.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
The candidate is useful only if it changes the component representative before the dominant B175 tensor/reference term is formed. If stock SI already performs the proposed centered lift, every later result is exactly the baseline path and no implementation experiment can create paper-level novelty or value.

## Source audit

### BGV scale-invariant call chain

Primary source:
  tuneinsight/lattigo v6.2.0
  schemes/bgv/evaluator.go
  blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.

`tensorScaleInvariant` calls
  eval.modUpAndNTT(level, levelQMul, tmp0Q0, tmp0Q1)
for each degree-one operand before forming tensor products.

`modUpAndNTT` does, component by component:
1. INTT from RingQ;
2. `basisExtenderQ1toQ2.ModUpQtoP(level, levelQMul, coeffQ, coeffQMul)`;
3. NTT in RingQMul.

Thus the exact representative policy is determined by `ModUpQtoP`.

### `ModUpQtoP` is centered

Primary source:
  ring/basis_extension.go
  blob fb9f0e877d928984b57b1db9917c03417f2fd211.

The wrapper is:
  QHalf = floor(Q/2)
  ringQ.AddScalarBigint(polQ, QHalf, buffQ)
  ModUpExact(buffQ, polP, ...)
  ringP.SubScalarBigint(polP, QHalf, polP).

`ModUpExact` itself carries the explicit warning:
  values are not centered.

But that warning applies to the INTERNAL helper only. The public `ModUpQtoP` wrapper deliberately shifts by QHalf before exact conversion and shifts back by QHalf in the destination basis.

## Exact representative derivation

Fix one coefficient residue x in Z_Q, represented canonically in [0,Q-1]. Let
  h = floor(Q/2).

`ModUpQtoP` first computes
  y = x + h mod Q.

`ModUpExact` reconstructs exactly the canonical representative y in [0,Q-1] and maps that integer to the target QMul/P basis.

The wrapper then outputs
  y - h
in the target ring.

Case 1: x <= h.
Then x+h < Q except possibly the top centered boundary convention, and
  y-h = x.

Case 2: x > h.
Then
  y = x+h-Q,
so
  y-h = x-Q.

Therefore the integer represented in QMul is exactly
  cent_Q(x) in [-floor(Q/2), ceil(Q/2)-1],
up to the library's deterministic half-boundary convention.

This is precisely the centered integer lift proposed by the candidate.

## Consequence for B175 tensoring

The candidate proposed:
  INTT component in Q
  -> recover centered integer representative
  -> embed that exact signed integer in QMul
  -> tensor there.

The stock path already does exactly this before `tensorLowDeg`.

Therefore:
  CANDIDATE_QMUL_REPRESENTATIVE = STOCK_QMUL_REPRESENTATIVE.

There is no alternative Q-multiple carry removed by the candidate at this interface.

The B175 aggregate `E_tref` term may still contain component-lift/Q-carry phenomena from other steps, notably the interaction of centered Q representatives with multiplication, reference encoding, later reduction and quantization. This turn does NOT claim those effects are absent.

It establishes only that the specific suspected source—non-centered Q→QMul basis extension—is not present.

## Relation to durable B175 attribution

Durable finding
  findings/boot-B175-source-level-si-error-bounds-2026-10-29.md
states that the observed 647-bit coefficient residual is dominated by the aggregate tensor/reference term and that fine decomposition requires the exact component lifts.

Turn 25 removes one ambiguity in that decomposition:
the Q→QMul operand lift used by stock SI is already centered and exact.

Thus a future representation redesign cannot claim novelty or noise recovery merely by changing `ModUpQtoP` from uncentered to centered. It must modify some other part of the representation geometry: the input ciphertext components themselves, the multiplication law, the reference/carry representation, or the location of the nonlinear merge.

## Killer gate outcomes

Killer gate (1), semantic oracle:
NOT REACHED as a distinct candidate, because the proposed construction is source-identical to baseline. There is no new semantic transformation to verify.

Killer gate (2), source/distinctness:
FAIL / COLLISION WITH STOCK IMPLEMENTATION.

The exact primitive required by the candidate already exists and is exactly the path used by B175.

Killer gate (3), value ceiling:
FAIL by identity.

A representation-identical implementation has:
- identical ciphertext components entering tensorLowDeg;
- identical QMul tensor products;
- identical quantization inputs;
- identical relinearization inputs;
- identical operation counts;
- identical key material;
- identical security and DFR.

Hence its best possible end-to-end delta is exactly zero.

## Prior-art / novelty boundary

This candidate does not reach a literature-novelty question. The exact centered-lift mechanism is already implemented in the pinned Lattigo baseline itself.

NOVELTY_STATUS therefore remains PREFLIGHT rather than CLEAR; operationally the mechanism collides with baseline source before external prior-art audit is relevant.

## Decision

FAIL_SOURCE_DISTINCTNESS / FAIL_VALUE_IDENTITY -> PARKED.

Candidate:
  boot-b158-centered-qmul-lift-pointwise-v1.

NO_CREDIBLE_NEW_MECHANISM remains for this specific centered-lift hypothesis.

No native execution is justified.

## Reopen condition

Reopen only with a representation change that is provably different from the stock centered `ModUpQtoP` path and that targets another part of the dominant B175 aggregate tensor/reference geometry.

Acceptable reopening evidence must identify a concrete source-level delta such as:
1. a different input-component representative before Q→QMul lifting;
2. a different multiplication/reduction law;
3. a different reference-encoding/carry invariant;
4. a different location for the nonlinear merge;
and must provide a plausible fixed-Q recovery of at least the needed margin with complete correctness, DFR and whole-system cost.

Replacing `ModUpExact` by a manually centered wrapper, or reimplementing `ModUpQtoP` under another name, does not satisfy the condition.

## Eliminated uncertainty

Eliminated:
Is the B175 scale-invariant pointwise failure plausibly caused by a non-centered Q→QMul operand lift that can be repaired by switching to centered basis extension?

Answer:
No. `modUpAndNTT` already calls a `ModUpQtoP` wrapper that adds Q/2, performs exact basis extension, and subtracts Q/2, yielding the exact centered integer representative in QMul. The proposed repair is already the baseline.

## Evidence references

- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; blob c75aa60e080b28b688de7ee8859c5df4d1951c02.
- findings/boot-B175-static-noise-attribution-audit-2026-10-29.md; blob e31ec2cbee6886ca61b6bc721920938d2a8a072b.
- findings/boot-B158-canonical-noise-rescale-gate-2026-10-28.md; blob 3e18f24c8eb963c707c9eb4bdcfa0106bd2d941a.
- Lattigo v6.2.0 schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.
- Lattigo v6.2.0 ring/basis_extension.go blob fb9f0e877d928984b57b1db9917c03417f2fd211.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.