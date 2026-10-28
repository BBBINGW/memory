# Post-B175 Claim-Boundary Synthesis

Date: 2026-10-29  
Session: Cryptography 10.0, Research Turn 23/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Classification

- CLASSIFICATION: PASS
- SCOPE: POST_B175_CLAIM_BOUNDARY_SYNTHESIS
- STATIC_INFORMATION_FRONTIER_REACHED: YES
- SUBSTANTIVE_NO_PI_NO_NATIVE_TEST_REMAINING: NO
- VALIDATED_REDESIGN_CANDIDATE: NONE
- POTENTIAL_PAPER_CONTRIBUTION: NOT_ESTABLISHED
- BOOT-DECISION-001: PENDING_PI_DECISION
- B176: NOT_AUTHORIZED

## Synthesis

Post-B175 static work has established the real failure boundary, coarse error category, negative screens for low-value repairs, and the remaining claim space. B174's isolated GROUPED endpoint passes three fixed cases with marginal headroom, while the valid L18 B175 direct LT8-by-GROUPED SI pointwise gate fails with budget -15 and 32767/32768 mismatches. Source-level bounds show the aggregate tensor/reference geometry dominates, but fine decomposition requires missing component lifts and quantization states.

Backend/local-noise repair, pure LT scheduling, simple permutation, reconstructing the same GROUPED value before multiplication, and the explicit eight-branch delayed recombination are statically killed. Frontier A has no independent value beyond an engineering repair. Frontier B retains only distributional, instance-specific, or exact-public-lineage-specific low-ceiling claim space. Universal schedule dominance over all legal component representatives is excluded in both directions.

There is no remaining substantive test that is simultaneously independent of PI, non-native, authorized, and non-duplicative of Turns 10--22. Remaining identifiable questions require actual frontier components/common lineage, new native instrumentation, DFR data, implementation of a new representation layer, or resolution of BOOT-DECISION-001.

## Claim matrix summary

The full synthesis classified 46 claims:

| Classification | Count |
|---|---:|
| RAW_PASS | 5 |
| RAW_FAIL | 1 |
| STATIC_PASS_WITH_SCOPE | 8 |
| STATIC_FAIL | 13 |
| UNCLEAR | 6 |
| PI_BLOCKED | 4 |
| NOT_ESTABLISHED | 9 |

Key dispositions:

| Claim | Classification | Strongest evidence | Scope/disposition |
|---|---|---|---|
| B174 isolated GROUPED three-case correctness | RAW_PASS | raw native | fixed cases only |
| B174 GROUPED headroom 15/14/15 | RAW_PASS | raw native | positive but marginal |
| B174 general phase / DFR | NOT_ESTABLISHED | raw boundary | needs new native/distribution evidence |
| B175 inputs and key-level prerequisites | RAW_PASS | raw native | valid gate inputs |
| Direct LT8 x GROUPED SI pointwise | RAW_FAIL | raw native | composition falsified |
| 26 ct-ct and reported key BinarySize | RAW_PASS | raw native | operation/BinarySize scope only |
| 965.03 MiB complete key saving | STATIC_FAIL | raw audit | L18 LT integration removes isolated saving |
| Aggregate tensor/reference dominance | STATIC_PASS_WITH_SCOPE | source audit | coarse attribution only |
| Fine error decomposition | UNCLEAR | source audit | components/QMul states missing |
| Conditional 16-bit recovery threshold | STATIC_PASS_WITH_SCOPE | source audit | fixed 31-bit-increment assumption |
| Backend/local-noise-only repair | STATIC_FAIL | source audit | killed |
| Pure LT/permutation/same-GROUPED regrouping | STATIC_FAIL | source audit | killed |
| Explicit eight-branch delayed recombination | STATIC_FAIL | best-case cost | 34 ct-ct, aligned score 655 |
| Frontier A structural circuit | STATIC_PASS_WITH_SCOPE | component algebra | exists, not a candidate |
| Frontier A native correctness | UNCLEAR | component algebra | decisive components missing |
| Frontier A independent contribution | STATIC_FAIL | best-case cost | engineering repair only |
| Frontier B structural circuit | STATIC_PASS_WITH_SCOPE | component algebra | exists, not a candidate |
| Frontier B native correctness | UNCLEAR | component algebra | high branch/final SI absent |
| Frontier B independent contribution | UNCLEAR | best-case cost | low-ceiling residual claim space |
| Healthy-operand mask growth 17--18 bits | STATIC_PASS_WITH_SCOPE | source audit | operand-specific warning |
| Operator-only mask lower bound | STATIC_FAIL | component algebra | inverse/cancellation counterexamples |
| Persisted summaries determine frontier verdict | STATIC_FAIL | component algebra | opposite completions exist |
| SI gauge sensitivity | STATIC_PASS_WITH_SCOPE | component algebra | explanatory only |
| Current-lineage public exact gauge | STATIC_FAIL | source audit | secret-only/unreachable |
| Unselected rerandomization worst-case guarantee | STATIC_FAIL | support-only | PASS and FAIL both in support |
| Practical rerandomization DFR | UNCLEAR | support-only | synthetic mass not transferable |
| A/B/current universal dominance | STATIC_FAIL | component algebra | exact ranking reversals |
| Full Algorithm 5 / leading | NOT_ESTABLISHED | none/raw boundary | never executed |
| DFR | NOT_ESTABLISHED | support-only | no actual probability result |
| Runtime/end-to-end speedup | NOT_ESTABLISHED | none | no benchmark |
| Peak RSS / complete memory advantage | NOT_ESTABLISHED | raw boundary | BinarySize is not RSS |
| Novelty / paper contribution | NOT_ESTABLISHED | related-work | no validated candidate |
| B176, parameter rescue, new representation implementation | PI_BLOCKED | governance | awaits PI |

## Disposition boundary

Killed ideas include the current direct composition, local/backend-only rescues, pure LT or permutation repairs, the current explicit delayed-recombination form, Frontier A as an independent contribution, operator-only mask lower bounds, public exact-gauge rescue in the current lineage, worst-case rescue by one unselected rerandomization, and universal component-representative schedule dominance.

Gauge sensitivity, healthy-operand mask growth, and zero-encryption support/quantization-cell witnesses remain explanatory evidence only. They are not a rescue, candidate, DFR result, or paper contribution. External-product and ring/field-switching concepts remain unvalidated strategic families without recovery, cost, security, or novelty closure.

## Checkpoint path

Turn 24 must perform provenance and checkpoint audit only: verify durable files/digests, local/remote commit equality, state/latest-finding/pending-queue consistency, the single canonical pending decision, B176 not authorized, no candidate/contribution promotion, and the fields required for Turn 25.

If that audit passes and PI provides no new decision, Turn 25 should record a milestone with `POST_B175_STATIC_SYNTHESIS=COMPLETE`, `STATIC_INFORMATION_FRONTIER=REACHED`, no authorized experiment or validated redesign, `NEXT_ITERATION=PENDING_PI_DECISION / NO_INDEPENDENT_RESEARCH_REMAINING`, and BOOT-DECISION-001 pending. Turn 26 remains HANDOFF ONLY.

No Codex/native execution, B175 rerun, B176, parameter change, DFR test, implementation, or track/subline change occurred.

## Research-GPT evidence identifiers

- SYNTHESIS_SHA256: `42790f8483f237686958c16ad3bfb0783145ef3fcb17f7bf030161b10c49d4eb`
- MATRIX_JSON_SHA256: `27705bbb1c2bafa5b2c62c56aaa21431e440f1f27c83ff95bd6d8ad4a0ca9851`
- MORNING_SOURCE_SHA256: `21cd5000972f19986db87332b4d0a286096c29a86999f855bfce2ce151fb4bbf`

