# BOOT / B158_OVERALL — successor Research Turn 1/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-terminal-standard-bgv-tensor-mode-switch-v1
Outcome: PARKED / FAIL_SOURCE_DISTINCTNESS / FAIL_PAPER_VALUE_PREFLIGHT
No native/Codex task started.

## Authority / provenance
Handoff checkpoint supplied: 3fb324bda661036caf3594e3301e01e09eca2c5d (not independently reachable through the GitHub commit search in this tool session). Authoritative scientific Turn25: findings/boot-b158-turn25-centered-qmul-lift-problem-selection-2026-11-12.md, verified blob 6af6b2a1e815d1eac54996a36a15e410d99f024d, parent scientific-result remote commit 8b0541fdce9b19b8d9c8ab1034d6f3a4b297064f. Baseline B175: findings/boot-B175-source-level-si-error-bounds-2026-10-29.md and findings/boot-B175-hybrid-frontier-research-value-ceiling-2026-10-29.md. More recent GitHub main also contains separately recorded UI-recovery artifacts at commits a9ba9f139e71e8ff4765df55977c874bb4547f58 and fed0cf36c09b73a5b294c16c55762253d24f8b21, neither is reused or counted as this successor turn. Handoff durable active paper candidate UNKNOWN, backups NONE; no pending native task.

## New candidate and pre-registration
QUESTION: At the *terminal* B175 pointwise ciphertext-ciphertext multiplication, can switching from BFV-style MulRelinScaleInvariant to standard BGV MulRelin (with scale metadata interpreted consistently, and without a mandatory following rescale if output is terminal) provide a novel complete paper mechanism that avoids the observed 16-required-bit deficit?
CURRENT_BELIEF: Both operations are stock documented modes of the SAME pinned BGV evaluator. Final-use mode choice is an ordinary known hybrid BGV optimization, not a new algorithm. Standard tensoring may have different actual noise (unknown without matched raw test); no source-backed bound currently establishes a B175 >=16-bit recovery or independent paper value.
CHEAPEST_DECISIVE_TEST: Read pinned v6.2.0 BGV public API definitions/description of MulRelin, MulRelinScaleInvariant, and their scale update laws; screen the purported technical delta and optimistic paper value before native execution. Confirm that mode choice is already stock.
IF_PASS: If there is an identifiable source-distinct representation or theorem beyond simply selecting stock standard mode, admit ACTIVE for full correctness/source/value construction, preserving 32768-slot semantics.
IF_FAIL: If the entire proposal is the built-in terminal standard multiply and scale handling, PARK because no new mechanism/novelty even if an instance works.
IF_UNCLEAR: Preserve UNKNOWN and inspect the exact evaluator flag dispatch and scale handling; do not run native work for a non-novel mode flip.
WHICH_PAPER_GATE_CHANGES: gate (1) whole-output scale semantics, gate (2) stock/source distinctness, gate (3) independent end-to-end scientific value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A paper requires a technically distinct mechanism and demonstrated global benefit, not mere selection between two pre-existing multiplication choices. Verifying stock support prevents a non-publishable native campaign.

## Primary stock evidence and technical analysis
Primary pinned v6.2.0 package documentation: https://pkg.go.dev/github.com/baahl-nyu/lattigo/v6@v6.2.0/schemes/bgv . Pinned source provenance from prior audit: tuneinsight/lattigo v6.2.0 schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f. The source API explicitly documents:
- Evaluator.MulRelin uses standard BGV/CKKS-style tensoring when Evaluator.ScaleInvariant=false, and otherwise BFV-style invariant tensoring.
- Evaluator.MulRelinScaleInvariant is a separate direct BFV-style entry point.
- For ciphertext operand, standard MulRelin updates scale to s0*s1; invariant MulRelinScaleInvariant updates scale to s0*s1*(-Q mod T)^-1 mod T.
- Documentation warns ordinary standard tensoring generally increases noise multiplicatively with plaintext/noise norms and typically requires a rescaling for subsequent multiplications; BFV-style invariant tensoring has different noise growth.
Exact delta proposed: replace ONLY final SI call with standard MulRelin and interpret output at the ordinary product scale; no new algorithm, ciphertext type, key edge, representation, or arithmetic identity. Plaintext semantics are intended to be equivalent under their respective scale conventions; complete B175 decryption correctness is UNKNOWN, and no wrap/carry/noise/DFR certificate is claimed. If the output is terminal, a later rescale MAY be avoidable; this does not create new capability and cannot be asserted for a downstream pipeline without checking output requirements.
The existing H175 failure remains: LT8 required bits 577 (PASS), GROUPED 633 (PASS), SI POINTWISE 664 (FAIL), Q bitlength 649, target <=648. A different multiplication mode does not itself prove recovery of 16 bits; data insufficient for numerical claims about actual standard-mode B175 noise.

## Killer gates and paper value
(1) Exact semantic oracle: algebraic decoded plaintext is product if standard BGV input noise is sufficiently bounded; output scale differs by known unit. Whole-output carry and actual decryption noise NOT VERIFIED. Mark candidate correctness BLOCKED, not FAIL.
(2) Source/novelty feasibility: FAIL_SOURCE_DISTINCTNESS. Both standard mode and scale-invariant mode are existing v6.2.0 interfaces. No source-level new primitive or missing type/key edge. This is a baseline mode selection, and the proposed technique collides directly with stock hybrid BGV. NOVELTY_STATUS=COLLISION for exactly this stock-mode mechanism (not a universal prior-art audit of all alternative BGV multiplication methods).
(3) Optimistic whole-system paper value: no changed asymptotic ct-ct count, rotation/key schedule, or new correctness region theorem. A successful last-stage standard mode trial would be a parameter-specific stock configuration choice, without a distinct scientific construction or credible proof. Potential practical instance performance/noise difference remains UNKNOWN; it must not be misreported as known failure.
No native canary warranted for paper-selection goal.

## Verdict and reopening condition
PARKED: NO_CREDIBLE_NEW_MECHANISM for simply selecting final stock standard BGV multiplication; no ACTIVE candidate remains. Does not assert standard multiplication always fails, or that conditional switching with a new proven decision criterion is impossible.
Reopen only with a technically new, source-backed adaptive mode-selection or mixed-encoding invariant with a complete legal-domain semantic oracle, substantial B175 fixed-Q correctness/DFR gain, sound security/noise proof, costs for conversion/rescale/keys/memory, and a prior-art-distinct paper-level thesis. Merely changing one evaluator flag or avoiding a terminal rescale is insufficient.
Named eliminated uncertainty: Is the proposed final standard multiplication a new primitive or unimplemented construction needing paper-level evaluation? No; it is existing stock BGV hybrid-mode functionality.
DECISION_CHANGED=true: proposed distinct candidate was rejected by exact source collision before native work.
Evidence grade STATIC. Citation: pinned pkg.go.dev v6.2.0 docs and existing repository file paths above.
