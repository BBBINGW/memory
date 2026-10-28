# BOOT State

Updated: 2026-10-29 — Cryptography 10.0, Research Turn 21/25, post hybrid-frontier research-value ceiling.

- TRACK_ID: BOOT
- ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- LATEST_COMPLETED: B175_AUDIT
- NEXT_ITERATION: UNIVERSAL_SCHEDULE_DOMINANCE_IMPOSSIBILITY_SCREEN; BOOT-DECISION-001_PENDING
- CURRENT_STATUS: B175_RAW_AUDITED_FAIL / FRONTIER_A_VALUE_FAIL / FRONTIER_B_UNCLEAR_LOW_CEILING / OVERNIGHT_AUTONOMOUS_RESEARCH
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
findings/boot-B175-hybrid-frontier-research-value-ceiling-2026-10-29.md

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

Representation-mechanism screen:

- Backend-only, key-switch-only, pure LT-scheduling, simple-permutation, and reconstruct-before-multiply decomposition rescues are statically killed for the fixed-`Q` B175 deficit.
- Delayed recombination, external-product representation, and ring/field switching survive only the geometry-changing necessary-condition gate.
- No survivor has an established 16-required-bit recovery, complete cost/security case, or novelty claim; there is no validated redesign candidate.
- The next no-regret test is an optimistic eight-block delayed-recombination ceiling using the existing powers, scales, required-bit traces, accumulation bound, and operation counts.

Delayed-recombination screen:

- The explicit eight-branch distributive expansion requires at least 34 ct-ct operations, versus 26 through the current pointwise gate and 27 for the current projected full skeleton.
- Under an optimistic 29-bit SI increment and zero mask cost, free same-scale accumulation leaves only one bit of margin; exact scale alignment raises the sufficient bound to 655, seven bits above the positive-budget ceiling.
- Passing would require an effective SI increment of at most 25 bits, while every observed SI multiplication adds 29--31 bits.
- The low-count factorized endpoint recurs to 664 required bits; the explicit endpoint fails both count and scale-aware screens.
- Actual partial-product residuals remain unmeasured, and no general representation impossibility theorem is claimed.

Hybrid-selector Pareto screen:

- Forty-three weighted nonisomorphic selector-subcube circuits were statically enumerated; twenty survive the raw optimistic ceiling before dominance filtering.
- Two count-26, selector-endpoint-depth-two mechanism classes form the minimal frontier: an explicit lower-two-bit selector and a high-bit distributed balanced split.
- Their full SI dependency depth remains four, so neither improves full depth.
- Under the optimistic 29-bit increment, zero-mask-cost model, Frontier A scores 644 required bits with four units of slack and Frontier B scores 645 with three units of slack.
- Each fails under small deviations already observed in B175; neither is a validated candidate or established contribution.

Public-mask convolution screen:

- Exact Lattigo coefficient polynomials for `c2`, `d2`, and `M0..M3` were reconstructed and their slot identities and coefficient norms verified.
- On saved healthy residuals, exact mask convolution raises required bits by 17--18; this is strong operand-specific negative evidence against the frontiers' three-to-four-bit slack.
- Frontier B's known low branch reaches 610 required bits after exact mask and scale alignment, but the decisive `c2*SI(LT8,Y^4)` residual is missing.
- Frontier A lacks the full coefficient residuals for `Y`, `Y^2`, and `Y^3`, so none of its decisive masked branches can be evaluated.
- An upper bound from mask `l1` norms is not a lower bound on unknown operands; cancellation and missing component-lift/`Q`-carry state prevent formal elimination.
- Both frontiers remain `UNCLEAR_NOT_ELIMINATED`; no validated redesign candidate exists.

Public-mask operator-kernel screen:

- Across all 19 L18 primes, every raw-lift public-mask operator is a full-rank unit with no NTT spectral zero; the plaintext `RingT` projection geometry does not survive in the residual operator.
- The rigorous finite-field inverse-norm lower bound loses roughly 34--38 bits and cannot force the three-to-four-bit growth needed to eliminate the frontiers.
- Explicit inverse-polynomial and carry-cancellation constructions prove that no operator-only universal positive coefficient-norm lower bound exists for an unknown residual vector.
- A 14.26--15.46-bit conditional integer no-wrap gain explains the historical empirical warning but is inapplicable without no-wrap, carry, and branch-cancellation proofs.
- The operator-only screening hypothesis fails; both frontiers remain `UNCLEAR_NOT_ELIMINATED` and unvalidated.

Hybrid-completion indeterminacy screen:

- At the summary/decryption-residual level, each frontier admits one exact public-affine-compatible completion that passes the fixed-`Q` static bound and one that fails it.
- Frontier A's constructed outputs are 645 and 652 required bits; Frontier B's are 639 and 649.
- Therefore the persisted maxima, scales, exact saved arrays, masks, and affine rules cannot determine either frontier's static verdict; summary-level `UNCLEAR` is information-theoretically unavoidable.
- This does not establish opposite realizable native executions. Common secret, component lifts, `Q_Mul` states, quantization/relinearization errors, cross-stage lineage, and distribution support remain missing.
- Both frontiers remain `UNCLEAR_NOT_ELIMINATED`; no validated redesign candidate or novelty claim exists.

Decryption-fiber gauge screen:

- Exact unquantized tensor decryption is gauge invariant, but componentwise centered lift and `T/Q` quantization break that invariance.
- A fixed-secret, fixed-plaintext, fixed-input-residual, fixed-scale L18 component witness produces a zero-residual PASS for one representative and a nonpositive-budget FAIL for a gauge-related representative.
- This reaches single-SI component-algebra realizability, stronger than residual-only completions, without relying on relinearization error.
- It does not establish common encryption-distribution or B158/B175 cross-stage lineage realizability, nor a public way to select a favorable gauge.
- Gauge sensitivity is established, but no gauge-based repair, native frontier correctness, or novelty claim is validated.

Common-lineage gauge-accessibility screen:

- The current B158/B175 public path contains no rerandomization, public key, fresh zero encryption, or component adjustment between operand completion and pointwise SI multiplication.
- Exact residual-preserving gauge selection is secret-key-only and absent from the gate; it is killed as a current public redesign mechanism.
- Secret-key zero encryption adds at most 22 required bits under a conservative bound but requires online secret access and samples an uncontrolled gauge.
- Counterfactual public-key zero encryption adds at most 32 required bits under a conservative bound and roughly 12 MiB key payload; these costs alone do not prove failure, but the mechanism is probabilistic, unimplemented, and unauthorized.
- Gauge sensitivity is retained only as an explanatory phenomenon. Both frontiers remain unvalidated and native-unclear.

Zero-rerandomization support/guarantee screen:

- Secret-key zero encryption has a uniform second component and bounded error support; its mathematical support contains both Turn-17 PASS and FAIL gauge representatives.
- For a fixed public key, the PASS point is in support while the specified FAIL point is key-dependent; over joint key generation and rerandomization, both are in support.
- Therefore a single unselected zero rerandomization fails as a worst-case all-coins correctness rescue.
- The explicit support events have extremely small idealized mass, so no useful B175/frontier DFR bound follows.
- Probabilistic rerandomization remains an unauthorized new DFR problem, not a validated candidate.

Quantization-cell robustness screen:

- The Turn-17 PASS and FAIL support points each extend to exact, nontrivial discrete quantization cells; the FAIL witness is not isolated.
- The PASS cell has `39^(N+1)` support points and a certified probability of `39*Q^-N`; a single FAIL cell has `39^(N-1)` support points.
- Both verdict cells remain astronomically negligible because their probability is dominated by hitting prescribed uniform ring polynomials.
- The result strengthens only the absence of a worst-case all-coins guarantee; it does not transfer to B175/frontier DFR.
- The static gauge/rerandomization subline has no further independent information gain without actual component states and is closed as an explanatory-only line.

Hybrid-frontier best-case research-value ceiling:

- Even assuming hypothetical native correctness, both frontiers retain 26 ct-ct through output, 27 projected with leading, full SI depth four, 30 rotations/key switches, and the same best-case key material; both increase ct-pt from 30 to 31.
- Their sole structural benefit is reducing selector endpoint depth from three to two, without reducing full depth or establishing latency improvement.
- Frontier A is a distributive lower-two-bit selector expansion with heavier scale/plaintext-interface work and no independent contribution beyond an engineering repair.
- Frontier B is a lower-burden reassociation that breaks the modular GROUPED/LT8 interface; it has only a low research-value ceiling unless a general, prior-art-distinct SI component-lift/Q-carry scheduling theorem can be proved.
- Neither frontier has native correctness, a validated redesign, novelty, count/depth/key/memory advantage, or end-to-end evidence.
- The next no-regret test is a universal schedule-dominance impossibility screen using legal component representatives and gauge sensitivity to seek a relative-noise ranking reversal.

Overnight rule:

Do not launch B176, repeat B175, sweep parameters, change Q/k0/geometry, test DFR, or implement a new representation layer without PI authorization. Continue only independent no-regret work: provenance/reproducibility, literature/novelty, theoretical necessary conditions, and shared cost/security/correctness analysis. Carry BOOT-DECISION-001 through every handoff.

Historical authority:

The B174 finding and post-B174 handoff remain historical parent evidence. The unrelated root STATE.md is known stale for this explicit BOOT recovery and does not override this topical state.
