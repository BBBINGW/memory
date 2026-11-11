# BOOT / B158_OVERALL — Research Turn 18/25
## PROBLEM_SELECTION — late lazy relinearization for B158

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-late-lazy-relinearization-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 18 had ACTIVE=UNKNOWN. This candidate does not reopen or rename the q0 sparse gateway, leaf-ring clean-factor sidecar, composite multiprime LCR, pre-raise sparse-subsum, or retry families. It is also distinct from the same-ring checkpoint-decoupled half-basis route. The new mechanism changes the ciphertext degree/relinearization schedule of the original late B158 fused recurrence itself.

## Hypothesis

Late B163/B158 stages pay a relinearization after each fused ct-ct multiplication. Since the audited late-stage required_logQ jump after the fused step is approximately 29–31 bits above the larger operand budget, one plausible source is relinearization/key-switch noise.

Candidate hypothesis: allow a fused multiplication to output a degree-2 ciphertext, keep that degree-2 state across at least one later B158 stage, and relinearize less frequently. If one relinearization can be removed rather than merely moved, late noise and evaluation-key work may fall enough to recover correctness.

## Registered decisive test

QUESTION: Can B158 late fused output be kept as degree-2 across at least one subsequent recurrence stage under the exact Lattigo v6.2.0 interfaces, so that at least one relinearization is eliminated rather than rescheduled?

CURRENT_BELIEF: No. B158's next stage needs RowRotation(S_k), and Lattigo automorphisms require degree-1 ciphertexts. The next ct-ct multiplication also rejects operands of degree >1. Therefore a degree-2 output will have to be relinearized before any next-stage nonlinear/rotation work.

CHEAPEST_DECISIVE_TEST: Use exact v6.2.0 source contracts for BGV Mul/MulNew without relinearization, RLWE Automorphism/rotation, and the library's own lazy PowerBasis schedule; then derive the B158 stage dependency graph. No native execution unless a stock-compatible stage can actually skip a relinearization.

IF_PASS: If at least one full B158 stage can consume the unrelinearized degree-2 state and produce the next recurrence state without a new evaluation-key family or custom higher-degree multiplication, admit the candidate ACTIVE and run one small native noise canary comparing immediate vs deferred relin.

IF_FAIL: If the very next RowRotation or multiplication requires degree 1 and therefore the same relinearization must occur before the next stage, PARK. A pure temporal move with the same key switch count/noise injection is insufficient.

IF_UNCLEAR: Resolve only the exact degree/type contract; do not start native work.

WHICH_PAPER_GATE_CHANGES: Killer gate (2), source/interface feasibility. The same fact also determines the optimistic value ceiling because a schedule that removes zero relinearizations cannot materially change the frontier.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: The mechanism is valuable only if it deletes at least one late relin. If stock interfaces force one relin per fused stage, native benchmarking would test a schedule permutation rather than a new algorithmic mechanism.

## Exact Lattigo v6.2.0 source facts

### BGV multiplication

Source: tuneinsight/lattigo tag v6.2.0, schemes/bgv/evaluator.go, blob SHA 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.

The Mul documentation explicitly states that no-relinearization multiplication returns the tensor product; tensoring increases noise; either ciphertext operand with degree higher than 1 is rejected; and output degree is the sum of operand degrees.

Thus two ordinary degree-1 B158 ciphertexts can produce degree 2, but that degree-2 output cannot be fed directly into another ciphertext-ciphertext Mul.

### Automorphism / RowRotation

Source: core/rlwe/evaluator_automorphism.go, blob SHA 527b1fdf8fdd92b705896b555597c9cc40ee2609.

Automorphism explicitly returns an error unless both input and output ciphertext degree are exactly 1. B158's RowRotation is a Galois automorphism. Therefore a degree-2 B158 state cannot enter the next stage's RowRotation using the stock evaluator.

### Library lazy-power precedent

Source: circuits/common/polynomial/power_basis.go, blob SHA 38bb155dbdca0de9da7c1cd5b7910f014ae26899.

The library's GenPower(..., lazy=true, ...) does permit a multiplication to leave a degree-2 ciphertext. But before a degree-2 power is recursively reused, it explicitly calls eval.Relinearize(...) on that operand and only then calls the next MulNew.

This is exactly the maximum lazy scope supported by the current interfaces: one may postpone relin while a degree-2 result is a temporary leaf, but not carry it through another multiplicative dependency.

## B158 dependency proof

For the regular B158 doubling stage at k:
1. state S_k;
2. compute tau(S_k) by RowRotation;
3. construct factor F_k from S_k, tau(S_k) and public selectors;
4. compute fused product S_{2k}=S_k * F_k.

Suppose step 4 uses no-relin MulNew, producing degree-2 S_{2k}. The next recurrence stage requires tau(S_{2k}) before its next factor can be constructed. But stock Automorphism requires degree 1. Therefore Relinearize(S_{2k}) must occur before the first structurally necessary operation of the next stage.

Even if RowRotation were somehow avoided, the next fused multiplication also cannot accept S_{2k} as a degree-2 operand under stock BGV Mul.

Hence every recurrent fused output that will be used in another B158 stage still incurs exactly one relinearization before that next stage.

There is no operation window in which delaying relin removes a key switch: current schedule is tensor -> relin -> next-stage rotation; proposed stock-compatible lazy schedule is tensor -> no structurally useful work -> relin -> next-stage rotation. The relinearization count is unchanged.

## Copy-selective relin gate

A micro-variant could keep degree-2 S_{2k}, clone/relinearize one copy for tau(S_{2k}), and keep the original degree-2 copy for the right-half factor. This is strictly worse under stock interfaces because the next fused ct-ct multiplication still rejects the degree-2 original, so the original must also be relinearized before multiplication. That produces two relinearizations instead of one.

## Higher-degree automorphism would be a different mechanism

A custom automorphism for degree-2 ciphertexts would need to transform/key-switch all secret-power components, not merely the ordinary degree-1 c1 component. Likewise custom degree-2 x degree-1 or degree-2 x degree-2 multiplication would require higher-degree ciphertext support and eventual degree reduction.

That is not a scheduling tweak. It is a different higher-degree RLWE evaluation mechanism with new evaluation-key interfaces, noise analysis, ciphertext memory traffic and later relinearization cost. It cannot be silently added to this candidate after source-gate failure.

## Relation to B163 failure

Authoritative native evidence: findings/boot-B163-native-artifact-audit-2026-10-28.md; artifact SHA256 bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad.

B163 is exact through k=4096; the next selector factors remain exact; the fused k=4096->8192 output fails with required_logQ=665 versus logQ=649. Reducing post-multiply noise is therefore scientifically relevant.

However this candidate does not remove a post-multiply relinearization. It merely relocates it from the end of one stage to the beginning of the next, before the required rotation. Therefore it offers no structural reason for a lower next-stage noise state.

## Optimistic value ceiling

Best stock-compatible outcome:
- relinearization count unchanged: one per recurrent fused result that is reused;
- Galois rotation count unchanged;
- ct-ct multiplication count unchanged;
- relinearization key family unchanged;
- ciphertext degree at every rotation and next multiply still 1.

Potential value is therefore only implementation-order constant effects, not an algorithmic frontier change. That fails the paper-first value requirement before benchmark.

## Decision

FAIL_SOURCE_INTERFACE / FAIL_VALUE_CEILING -> PARKED.

Candidate: boot-b158-late-lazy-relinearization-v1.

The late B158 noise problem is real, but ordinary lazy relinearization cannot change it because the recurrence's immediate next dependency is a degree-1-only automorphism and then another degree-1-only ciphertext multiplication.

## Reopen condition

Reopen only with a genuinely new, source-backed higher-degree evaluation mechanism that can: (1) apply the required B158 RowRotation to a degree-2 state, or otherwise construct the same exact factor without first reducing to degree 1; (2) carry degree-2 state through at least one additional fused recurrence step; (3) provably reduce total relinearization/key-switch noise or count, rather than defer it; (4) include higher-secret-power evaluation keys, security/noise analysis and memory/runtime cost; and (5) retain positive end-to-end value versus same-ring checkpoint-decoupling and the original B158 schedule.

Simply moving Relinearize to immediately before the next rotation/multiplication does not satisfy this condition.

## Eliminated uncertainty

Eliminated: Can stock Lattigo v6.2.0 lazy relinearization carry an unrelinearized B158 fused state through a later recurrence stage and thereby remove a late relin?

Answer: No. Both the required next-stage automorphism and the next ciphertext multiplication require degree-1 operands. The same relinearization must be paid before progress resumes.

## Evidence references

- findings/boot-B163-native-artifact-audit-2026-10-28.md; artifact SHA256 bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad.
- findings/boot-B158-formal-recurrence-optimality-prior-art-2026-10-28.md.
- Lattigo v6.2.0 schemes/bgv/evaluator.go, blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.
- Lattigo v6.2.0 core/rlwe/evaluator_automorphism.go, blob 527b1fdf8fdd92b705896b555597c9cc40ee2609.
- Lattigo v6.2.0 circuits/common/polynomial/power_basis.go, blob 38bb155dbdca0de9da7c1cd5b7910f014ae26899.