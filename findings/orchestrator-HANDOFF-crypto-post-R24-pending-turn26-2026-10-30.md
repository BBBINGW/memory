# BOOT Session Handoff — Turn 26 HANDOFF ONLY

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
SESSION_STATUS: Research Turns 9–25 complete; Turn 26 is HANDOFF ONLY.
CONTINUOUS_AUTONOMOUS_RESEARCH: enabled
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false
RESEARCH_FRONTIER_EXHAUSTED: false
PENDING_PI_DECISIONS: none

## Authorized background native task — DO NOT TOUCH

TASK_ID: BOOT-RMFE-P5W512-SOURCE-R1-R8-ONECORE-CORRECTNESS-CAPACITY-20261029-R24-01
STATUS: UNKNOWN / BACKGROUND
RESULT_DELIVERED: false
DO_NOT_RERUN: true
DO_NOT_RESUBMIT: true
DO_NOT_MODIFY_SOURCE_WORKDIR_BINARY: true
DO_NOT_START_ANOTHER_HEAVY_LOCAL_NATIVE_TASK_WHILE_THIS_SLOT_IS_OCCUPIED: true

If this result becomes available, it preempts the next free substantive turn in the latest active session for independent audit.
No session-local research turn is reserved for it.

## Fixed candidate lineage / parameters

p=5, r=1, m=32768, w=512, k=5, eta=125, normal_basis=false.
HElib pinned source: acdb264e1a991eaee35fd8b3c31bebe9528c49a1.
e=5, ePrime=2, q=3126, post-core plaintext modulus=625.
Normalized trace/RM10 scale: 1024^{-1} mod 625 = 224.
Current one-core concept:
RMFE projections -> rank-8 envelope -> one HElib raw recryption core -> RM10/restriction -> rank-8 C2S/unpack -> five scalar retained coordinates -> source-r1 scalar DigitExtract oracle / eventual Aung correction path.

## Turns 9–25 authoritative synthesis

### Turn 9 — performance frontier
Correct candidate performance variable is B=M+H, not M alone, where H is envelope-merge cost.
T_cand = 6.602 + H + M seconds under published p=5 Aung anchors.
Absolute thin-throughput kill: final capacity <=70.68 cannot beat vanilla thin even with free middle.
At C=101: B<4.736s beats Aung RMFE; B<2.832s beats vanilla thin; B<1.974s reaches >=1.10x thin.
If H≈0.078s proxy: M thresholds 4.658 / 2.754 / 1.896s.

### Turns 10–13 — major novelty downgrade
HElib already has packedRecrypt: multiple ciphertexts -> one packed ciphertext -> one general reCrypt -> unpack.
Geelen 2024 and Ma 2024 already cover subring packing, low extension degree, post-inner-product trace/coefficient selection, and RM_k-type restriction.
Our RM10 is exactly normalized trace/coefficient selection for N/N'=1024.
Generic low-rank/subring packed bootstrapping and "one core instead of k cores" are NOT standalone novelty.
Current one-core candidate should be treated as compositional engineering unless it yields unusually strong systems value or a new theorem not derivable from prior building blocks.
Direct exact prior for the full RMFE-specific composition was not found, but all central primitives/placements have strong prior art.
Generic theorem choosing d'=2^ceil(log2 k)<2k while preserving SIMD slot count is mathematically valid but routine/prior-derived, not a strong new theorem.
No new RMFE-specific nonlinear obstacle was found in the one-core transport itself.

### Turns 14–16 — GIKV prescout and correction of an error
Turns 14–15 initially interpreted P3-F=5H as a relevant null-defect and derived an "Aung linear correction impossible" obstruction.
THIS WAS WRONG AND IS SUPERSEDED.
GIKV P3 is a higher-precision lowest-digit-retain polynomial, not the same scalar function as a single HElib lifting F.
Authoritative Turn 16 correction:
- GIKV p=5 optimized representatives satisfy P_i(X) ≡ X^5 mod 5.
- Aung's first-step correction framework therefore applies statically to each such polynomial if degree <= eta.
- Mixed compositions of maps each congruent to X^5 mod5 increase p-adic congruence by one per composition.
- The old H-nonlinearity impossibility claim is RETRACTED.

### Turn 17 — Frobenius-height constraint
Scalar functional equivalence is insufficient for RMFE correction.
Define Frobenius height h(C) by C(X) ≡ X^{5^h} mod5.
A direct high-precision GIKV representative with height1 cannot replace an Aung correction-tree node requiring height2.
For z=xi in the actual degree-512 RMFE image, xi^25-xi^5 !=0 mod5, so direct substitution fails.
Function composition can preserve the required height.

### Turn 18 — partially superseded
Turn 18 used poly5_1_5 -> poly5_5_6 as if they were successive extraction rows.
This was NOT source-faithful; they are composition stages inside one GIKV row.
Its specific L2* repair is SUPERSEDED.
Do not carry that construction as evidence.

### Turn 19 — source-faithful GIKV h=3 gate
Correct source-faithful p=5,e=4 sequence for current source-r1 setting:
g4=poly5_1_4, g3=poly5_1_3, g2=poly5_1_2.
The first two rows admit static correction closure with max polynomial degree 117 < eta=125.
At third row, the required residual R3 satisfies R3 mod5=0, but
(R3/5) mod5 =
X^25 + 3X^125 + 2X^175 + 3X^225 + 3X^275 + 3X^325.
Hence first nontrivial correction degree=325>125.
One-final-Recode direct GIKV extension therefore FAILS THE CURRENT eta CERTIFICATE.
This is not an impossibility theorem for all representatives.

### Turn 20 — one intermediate Recode fallback
Insert exactly one intermediate Recode after h=2:
rows 4->3 -> Recode -> row2 -> final Recode.
Static correctness closes; pre-Recode max degree 117, post-reset final row degree5.
But value headroom is weak.
Even granting an optimistic 2.6x GIKV digit-extraction speedup, extra Recode must be <2.62s to beat current Aung RMFE at C=101 and <0.714s to beat vanilla thin, before accounting for capacity loss.
Park as fallback.

### Turn 21 — RMFE-aware null-lattice rescue
Ordinary null-lattice freedom can reduce the first third-row correction digit to degree125 exactly.
However the second p-adic correction digit has degree845.
Invariant witness: coefficient of z^135 is 4 mod5, with 135>eta and 135 not divisible by25.
Ordinary second-order lifts only change z^(25j) terms or have zero effect, so z^135 survives.
Exhaustive low-degree representative search (84 perturbation directions, representative degree <=25) found NO SOLUTION.
Deeper first-order null redesign begins at degree >=15; the simplest degree-15 test worsened residual 845 ->1125.
Park GIKV successor absent a new structural idea.

### Turn 22 — security assumptions
One-core candidate introduces no new secret, secret distribution, secret-dependent ciphertext, KDM/circular relation, or incremental bootstrap evaluation-key class.
It inherits standard HElib/BGV secret-dependent evaluation-key / circular-security assumptions.
Restricted plaintext support is NOT restricted-secret RLWE; old RIG attacks do not apply.
Public projection/envelope correlation does not create new IND-CPA leakage.
Circuit privacy is NOT established.
Secret-dependent debug instrumentation is audit-only and must not enter a production evaluator.

### Turn 23 — DFR/correlation model
HElib recryption parameterization controls one global full-ring powerful-basis l_infinity event.
The five retained outputs share this ONE core-failure event; do NOT multiply core DFR by5 and do NOT treat the five outputs as independent samples.
Total failure can be bounded as:
P_fail <= P_core + sum_j P_post,j.
If post-core deterministic closure is later proved, P_fail<=P_core.
Same numeric DFR as thin baseline is NOT established because envelope input noise distribution differs.
Future statistical unit is one aggregated bootstrap invocation producing a 5-output vector, not five flattened Bernoulli samples.
noise_rat<1 is a run-level safety gate, not a formal DFR proof.

### Turns 24–25 — relaxed functional bootstrapping prescout
ASIACRYPT 2024 RFB offers large speedups by requiring correctness only on a known valid set, but existing construction is scalar-domain and is not a drop-in RMFE bootstrap.
RMFE image V has dimension5 and size3125 inside F_(5^512).
Positive structure: every k-dimensional F_p subspace has a linearized subspace polynomial with only k+1 Frobenius monomials, so membership/syndrome can be O(k), not O(p^k).
However direct relaxed identity bootstrapping on V fails the key error-separation requirement.
General deterministic identity decoding requires (V-V) ∩ (E-E) = {0}; for linear V this is V ∩ (E-E)={0}.
Current V contains 1, xi, xi^2, xi^3, xi^4, so errors with nonzero V-component create valid-message ambiguity.
Subspace polynomial detects off-V syndrome but cannot distinguish errors lying inside V.
DIRECT_RMFE_SUBSPACE_RELAXED_IDENTITY_BOOTSTRAP = FAIL.
Only reopening family: coded-subspace embedding J(V) with real error separation against modulus-switch contamination. This is a new representation family, not a drop-in successor.
Any RFB successor must incorporate the CCS-2025 security-fixed randomized modulus-switching approach at minimum.

## Current portfolio after Turn 25

1. R24 one-core RMFE:
   - correctness/capacity native gate: UNKNOWN/BACKGROUND.
   - security assumption boundary: PASS_NO_NEW_SECURITY_ASSUMPTION_STATIC.
   - core DFR bookkeeping: one global event, post-core DFR unresolved.
   - novelty: weak/compositional after packedRecrypt/subring/trace prior.
   - engineering value remains possible if native correctness/capacity/runtime are unusually strong.

2. GIKV x RMFE:
   - one-final-Recode path: parked by p-adic correction-degree obstruction / low-degree null-lattice invariant.
   - two-Recode fallback: static correctness pass, performance headroom weak.
   - do not reopen without a new structural idea.

3. B176/B158 geometry-changing family:
   - parked at soft budget; no validated candidate or deterministic 16-bit contraction.

4. Direct RMFE-subspace RFB:
   - killed by error-separation ambiguity.

5. Coded-subspace RFB:
   - prescout only / not started.
   - potentially distinct mechanism family, but requires new representation, error metric/code design, homomorphic compatibility, rate/value, and CCS-2025 security fix.

## Successor-session controller

- This session is closed for substantive research.
- If R24 result is available at successor start or arrives later, independently audit it BEFORE choosing any next BOOT experiment.
- Do not rerun/resubmit R24.
- If R24 remains pending, successor may continue independent BOOT research under the existing continuous-autonomous policy; no session-local turn is reserved for R24.
- Prefer a cheapest decisive static gate over implementation/native work.
- Do not revive GIKV local null-lattice search or B176 without a genuinely new invariant.
- Coded-subspace RFB is the highest-novelty unopened prescout, but requires a mathematical feasibility/value gate before any implementation.
