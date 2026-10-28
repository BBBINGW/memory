# BOOT State

Updated: 2026-10-29 — Cryptography 10.0, Research Turn 10/25, post source-level SI error-bound derivation.

- TRACK_ID: BOOT
- ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- LATEST_COMPLETED: B175_AUDIT
- NEXT_ITERATION: STATIC_REPRESENTATION_MECHANISM_FEASIBILITY_SCREEN; BOOT-DECISION-001_PENDING
- CURRENT_STATUS: B175_RAW_AUDITED_FAIL / TENSOR_REFERENCE_TERM_DOMINANT / OVERNIGHT_AUTONOMOUS_RESEARCH
- CURRENT_EXPERIMENT: NONE_AUTHORIZED
- CURRENT_RESULT: FAIL_B175_POINTWISE_NOISE
- EVIDENCE: RAW_AUDITED
- ACTIVE_CANDIDATE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- ACTIVE_GEOMETRY: H=8192, s=8
- ACTIVE_CHECKPOINT: k0=32
- STATUS: DIRECT_SI_POINTWISE_COMBINATION_FAILED / PENDING_PI_DECISION
- NOVELTY: NOT_ESTABLISHED
- FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED
- DFR: NOT_ESTABLISHED
- END_TO_END_SPEEDUP: NOT_ESTABLISHED
- PENDING_PI_DECISIONS: BOOT-DECISION-001

Latest completed finding:
findings/boot-B175-source-level-si-error-bounds-2026-10-29.md

Pending PI queue:
findings/boot-PENDING_PI_DECISIONS.md

B175 original ZIP:

    BOOT-B175-B158-CASE1-SI-POINTWISE-NATIVE-20261028.zip
    size: 13,680,154 bytes
    SHA-256: 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa

Independent raw audit established:

- Outer hash, ZIP structure/CRC, and all 65 internal SHA256SUMS entries pass.
- The embedded B174 parent source is byte-identical to the already audited B174 source.
- Exactly one fixed CASE_1 native run was executed; no retry, rescue, parameter sweep, leading multiplication, DFR, benchmark, or later Algorithm-5 stage was run.
- LT8 and GROUPED are valid exact L18 inputs with budgets +72 and +16, respectively.
- The single real SI pointwise ct-ct output is L18 with required bits 664, budget -15, and 32767/32768 decoded mismatches.
- The independently reconstructed pointwise scale is 30059, matching raw evidence.
- Actual ct-ct count through pointwise is 21 basis + 4 grouped + 1 pointwise = 26; leading remains zero.
- Promoting the five required LT keys from L14 to L18 raises reported evaluation-key BinarySize from 965.03 MiB to 1062.54 MiB (+97.50 MiB), eliminating the isolated B174 apparent saving at this interface. This is not RSS or a complete bootstrapping-key measurement.

Scientific boundary:

The fixed-parameter direct composition

    B174 GROUPED + same-context raw-L18 LT8 + direct SI pointwise

is falsified for the authorized CASE_1 gate. This does not falsify all checkpoint-decoupled representations, establish general phase behavior, or establish full Algorithm 5, DFR, or end-to-end performance.

Post-B175 static attribution:

- The 31-bit increase is attributable at coarse path level to the real SI ct-ct tensoring, scale-invariant quantization, and relinearization path, rather than the CASE_1 LT8 slot layout or public expected reference.
- Five SI ct-ct operations in the same run show stable 29--31-bit required-bit increments.
- Current traces do not uniquely separate tensor input-noise propagation, quantization rounding, and relinearization/GadgetProduct noise.
- The minimum decisive separation requires a post-quantization/pre-relinearization degree-two residual and a relinearization-only residual; neither is present in B175.
- If the multiplication-path increment remains 31 bits, a representation-only repair must reduce the worse input from 633 to at most 617 required bits, a conditional 16-bit recovery threshold.

Source-level SI error bounds:

- Scale-invariant quantization contributes less than `2^46` in coefficient infinity norm under deterministic ternary-secret bounds, corresponding to at most 63 required bits in the B175 convention.
- Conservative relinearization/GadgetProduct noise is less than `2^22`, corresponding to at most 39 required bits.
- The measured pointwise residual has coefficient bit length 647 and required bits 664; subtracting both conservative bounds leaves the same 647-bit / 664-required-bit magnitude.
- Therefore the aggregate tensor/reference term, rather than quantization or relinearization, necessarily dominates this B175 failure.
- Fine attribution within the tensor/reference term remains unclear because B175 lacks componentwise centered lifts, coefficient-domain references, and the pre-relinearization degree-two state.

Overnight rule:

Do not launch B176, repeat B175, sweep parameters, change Q/k0/geometry, test DFR, or implement a new representation layer without PI authorization. Continue only independent no-regret work: provenance/reproducibility, literature/novelty, theoretical necessary conditions, and shared cost/security/correctness analysis. Carry BOOT-DECISION-001 through every handoff.

Historical authority:

The B174 finding and post-B174 handoff remain historical parent evidence. The unrelated root STATE.md is known stale for this explicit BOOT recovery and does not override this topical state.
