# BOOT Pending PI Decisions

Updated: 2026-10-29, Cryptography 10.0 Research Turn 11/25.

PENDING_PI_DECISIONS:

- BOOT-DECISION-001

## BOOT-DECISION-001

- status: PENDING_PI_DECISION
- question: After the raw-audited B175 pointwise-noise failure, should the fixed-parameter direct SI pointwise combination be killed outright, or may one bounded representation-layer redesign be developed for later PI authorization?
- why_pi_needed: B175 decisively falsifies the authorized direct composition. Whether a materially different representation-layer design merits implementation is a strategic research-allocation choice reserved to PI.
- available_options:
  1. Kill the current direct SI pointwise combination and retain its audited negative result.
  2. Permit one bounded representation-layer redesign proposal; any native experiment remains separately PI-authorized.
- current_evidence: Valid exact L18 LT8 budget +72 and GROUPED budget +16; one real SI pointwise gives required bits 664, budget -15, and 32767/32768 mismatches. Minimal L18 LT8 key promotion adds 97.50 MiB and raises key BinarySize to 1062.54 MiB. Static source derivation bounds SI quantization below `2^46` and conservative relinearization noise below `2^22`, while the measured coefficient residual has bit length 647; the aggregate tensor/reference term necessarily dominates. The subsequent mechanism screen kills backend-only, key-switch-only, pure LT-scheduling, simple-permutation, and reconstruct-before-multiply rescues. Delayed recombination, external-product representation, and ring/field switching survive only as unvalidated geometry-changing families; no candidate has an established 16-bit recovery, complete cost/security case, or novelty claim.
- recommended_option: Treat the direct combination as killed. If PI permits one bounded redesign, require it to materially change tensor/reference geometry and pass the fixed-Q conditional 16-required-bit feasibility screen before any implementation; quantization, key-switch, or few-bit local-noise tuning should not be authorized as a rescue.
- what_is_blocked_by_this_decision: B176/native follow-up; parameter rescue/sweep; Q, k0, or geometry changes; implementation of a new representation layer; full Algorithm 5; DFR; end-to-end benchmark.
- what_can_continue_without_this_decision: B175 evidence persistence and reproducibility; related-work/novelty search; theoretical noise/scale necessary conditions; shared cost/security/correctness comparison; cheap non-experimental falsification of representation-layer ideas.
- source: findings/boot-B175-audit-direct-si-pointwise-noise-failure-2026-10-28.md; findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; findings/boot-B175-representation-mechanism-negative-screen-2026-10-29.md
- carry_forward: REQUIRED in every Turn-26 handoff and successor session until PI resolves it.

The overnight operating rule is `requires_pi != stop`. Research continues on independent no-regret work. Enter WAIT_PI only when no independent research remains or another authorized stop condition occurs.
