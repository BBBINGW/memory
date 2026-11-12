# BOOT / B158_OVERALL — VALID logical Research Turn 22/25 (UI identity replay)
2026-11-12, Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
PHASE: PROBLEM_SELECTION
CANDIDATE_ID: boot-b158-step1-l19-free-unspent-qi-precision-budget-v1
FINAL DECISION: PARKED — FAIL_GUARANTEED_FREE_30BIT_HEADROOM
NOVELTY_STATUS: PREFLIGHT
PAPER_READINESS: NOT_READY
NATIVE/CODEX: NOT RUN
RESEARCH_FRONTIER_EXHAUSTED: false
VALUE_REVIEW_COMPLETED: false

## Infrastructure replay provenance
The PI explicitly disqualified the preceding assistant Turn22 as infrastructure output and required reprocessing the same original research instruction using ordinary Chat GPT-5.6 Sol Extra High. The previous file findings/boot-b158-successor-turn22-defer-step1-rescale-l19-free-headroom-source-gate-2026-11-12.md is actually present at verified Git blob 16b63d055d8ea38bcd6248f8034e83acf8d7359f; it is retained as an invalidated UI episode, not a counted research iteration. We DO NOT overwrite or silently erase it. This is a separately labeled valid replay. Candidate named distinctly as an independently scoped guarantee hypothesis. It is not proposed as a reopening of a closed research candidate: the earlier UI-invalid research output does not carry active scientific authority for this replay. Do not double count these as two substantive rounds.

Read-before-write actual primary materials:
- findings/boot-b158-successor-turn21-fixed-logq-small-inverse-residue-si-tensor-value-gate-2026-11-12.md, independent Git blob 9d7c17a33e4c580e4201c05246cc8f9e19f73878 (PARKED, VALUE_REVIEW_COMPLETED=true);
- findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md independent Git blob ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29 (inherited Step1 L19->L18 normalization happens BEFORE baby basis, B174 GROUPED portion does not rescale; parameters LogQ=[36,34x18,30], N32768,T65537);
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md independent Git blob c75aa60e080b28b688de7ee8859c5df4d1951c02 (terminal SI requires664 bits vs L18 logQ649, failure by 15 bits; dominant tensor/reference error);
- Lattigo v6.2.0 schemes/bgv/evaluator.go, independently fetched Git blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f, exact lines 1353–1392.

## Pre-registration: one paper-level gate with distinct outcomes
QUESTION: Is B174/B175's pre-basis Step1 L19->L18 rescale a gratuitous 30-bit modulus sacrifice, so preserving L19 must grant at least 16 **additional relative noise-budget bits** at unchanged phase, output semantics and full costs?
CURRENT_BELIEF: No. Lattigo's real Rescale divides ciphertext coefficients and carries noise reduction, and updates plaintext Scale; it is no-op if ScaleInvariant evaluator. However L19 might improve a newly designed full SI tensor schedule through nontrivial CRT/carry mechanisms; no general impossibility claim.
CHEAPEST_DECISIVE_TEST: Primary-source read of Rescale level/noise/scale dataflow, matched with B174 audit, plus exact symbolic countermodel to the alleged guarantee. No native or new RNS primes.
IF_PASS: Only if a source-typed L19 algorithm proves equal semantic phase and equal original residuals while gaining at least 16 final budget bits at verified acceptable full cost, keep ACTIVE and test exact canary/security/DFR.
IF_FAIL: If unrescaled ciphertext can carry proportionately greater error and non-equivalent scale, no FREE guaranteed 30-bit budget follows; PARK this standalone promise and do not run native.
IF_UNCLEAR: An alternative L19 noise/carry geometry can remain UNKNOWN under a different complete algorithm, but is not a PASS for the present candidate. No rebranding of old candidate as ACTIVE.
WHICH_PAPER_GATE_CHANGES: killer1 all-message, all-phase/carry and scale correctness; killer2 stock evaluator mode, keys; killer3 claimed 16-bit relative error improvement under all-in costs.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: If headroom is guaranteed, the -15-bit B175 failure has a cheap solution; if it is only a routine Rescale tradeoff, selecting an L19 algorithm requires a separate original noise mechanism before any native spend.

## Exact source audit, not merely a heuristic
Lattigo BGV v6.2.0 evaluator.go:
- lines 1353–1362: rounding division by last modulus q_i, noise division and plaintext Scale update by q_i inverse mod T documented.
- lines 1363–1366: with ScaleInvariant evaluator, calling Rescale returns immediately (NO-OP).
- line 1385: ringQ.DivRoundByLastModulusNTT(...), actual coefficient transformation, not just metadata resize.
- line 1388: output Level decreases by 1.
- line 1391: out.Scale=op0.Scale.Div(params.NewScale(q_i)).
The B174 audit supplies proof of an L19->L18 normalization in the inherited Step1 but does not in itself reveal the exact evaluator-mode/call graph. Therefore we cannot claim it uses an SI evaluator's Rescale, nor bypass the mode check.

## Exact countermodel to the guaranteed free-headroom inference
Let positive integers Q18 and q coprime with T, Q19=q Q18. Consider ideal noise/reference representation at Q19 with e19=q e18, all values small enough to avoid modular centered wrap, and reference embedding M19=q M18. The perfect division by q maps the L19 ciphertext phase to its L18 counterpart. Then
  Q19/|e19|=(q Q18)/(q|e18|)=Q18/|e18|.
Therefore the source's full 30-bit extra Q modulus can coexist with ZERO relative noise-margin improvement. This is an algebraic witness disproving the implication 'retaining the original prime guarantees +30 bits'. With rounding, e18≈e19/q + ε subject to plaintext-embedding and secret-dependent carry, so no unconditional residual improvement can be inferred without exact ciphertext traces.

Scope caveat essential: there are also mathematical configurations e19 much smaller than q e18 where L19 relative margin may improve, and a changed SI tensor at L19 could alter carry and error. This turn does not prove L19 cannot work, nor that the actual B175 e19=q e18. No real L19 noise snapshots are present. Thus **FAIL applies to the claimed FREE GUARANTEE**, not to all L19 RNS schedules or any novelty claim.

## Complete value and source gate
Current B175 native data: Q18 bitlength649, terminal required664, wrong32767/32768. At Q19 the extra q limb adds about30 modulus bits, but a new source-typed branch preserving the intended phase is REQUIRED; no correct NTT/key-switch/rotation/relin evaluation-key path with full-SI L19 has been established. Every online multiplication and rotation may be more costly by one limb, and the offline key material and security parameters must be reaudited. A bare native side-by-side comparison without a semantics-matched baseline would be irrelevant; the first canary is blocked by source semantics, not pending. Originality: standard BGV rescale scheduling is prior art. Conditional algebra is not a novel construction.

FIRST_KILLER_GATE: the asserted unchanged phase/Scale/residual after omitting Step1 Rescale is FALSE as a general source semantic claim.
SECOND_KILLER_GATE: L19 exact typed algorithm/keys UNKNOWN; source rescale mode is known.
THIRD_KILLER_GATE: free all-in +16 bits fails; real L19 value UNKNOWN.
STATUS=PARKED, NO_CREDIBLE_NEW_MECHANISM, no ACTIVE/backup.
REOPEN_CONDITION: A separately specified L19 Step1 normalization that preserves the original legal phase and full output, correct Scale and Q-carry, a source-compatible complete evaluation-key schedule, demonstrated >=16-bit actual final DFR benefit versus matched L18 at same security, counted offline/online/runtime/RSS and independently verified novelty. Keeping q_i alone is insufficient.
ELIMINATED_UNCERTAINTY: Does L19->L18 Rescale merely drop an unused prime, preserving error and output Scale, so skipping it guarantees a 30-bit relative accuracy gain? No: source transforms ciphertext and Scale; an exact e19=q e18 countermodel eliminates a universal gain guarantee.
DECISION_CHANGED=true, research_frontier_exhausted=false; next new substantive Research Turn 23/25.
