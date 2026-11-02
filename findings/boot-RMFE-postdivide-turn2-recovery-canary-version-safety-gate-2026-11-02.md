# BOOT / B158 — Research Turn 2/25 — frozen recovery-canary version-safety gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation

## Provenance / read-before-write
GitHub Notes reads returned empty objects, so current durable inputs were recovered from the same BBBINGW/memory repository at verified handoff head 9f2a23973288e9ee8bdacb89dfc47c0ac9f0db26.

Inputs:
- frozen canary source: findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt
  SHA 6ae4bc7e48e0390f8dec97429f4ddb89565928c0
- Turn25 static closure:
  findings/boot-RMFE-postdivide-turn25-end-to-end-static-correctness-closure-2026-11-02.md
  SHA 6885ab59af403b71e0fdbc91d8e2b139fbf6a93c
- Turn24 mod5/Z625 bridge:
  findings/boot-RMFE-postdivide-turn24-forward-mod5-z625-lift-bridge-gate-2026-11-02.md
  SHA 1903cfb6d76647d487c56bfa12145e4a03b90b70

No native execution occurred.

## Primary hypothesis
The frozen revised Turn-11 recovery-only canary remains a valid Step-2 small-correctness canary for the CURRENT Turn-25 candidate after the Turn24/25 supersessions. It must not rely on production-forward-over-Z625, exact higher-adic rho coherence, factor1 after scalar-unit normalization, a one-shared-forward architecture, or stale count19.

## Falsifier
FAIL if the source instantiates/asserts production forward as Z625, forces common cross-slot lifts, requires exact lifted rho/182 coherence, assumes factor1 after x28, contains the superseded shared-forward architecture, uses stale branch/routing metadata, or claims to test production rho/443 correction when it does not.

## Minimal decisive test
Compare the exact frozen source against the current Turn24/25 typed path and mechanically recompute fixed normalization/routing constants.

## 1. No stale Z625-forward assumption
The canary explicitly states application context r=1 and that SecKey::Encrypt(...,625) is TEST SETUP ONLY. It does not execute the production tagged forward. It directly constructs a synthetic two-slot Z625 state rootUnnormalized=crtPairPoly(A,B) solely to exercise recovery.

Thus Turn24 remains the production theorem:
tagged forward exact over Z5 -> arbitrary Z625 lift bridge.

Result:
PASS_NO_STALE_Z625_FORWARD_ASSUMPTION_IN_CANARY

## 2. Independent cross-slot dirty lifts
The canary constructs distinct A and B vectors. Selected values are dirtied independently by different multiples of 5, and off-target 5-divisible dirt is also distinct. It never asserts A=B, a common Hensel lift, or exact lifted rho coherence.

Result:
PASS_INDEPENDENT_CROSS_SLOT_DIRTY_LIFTS_IN_CANARY

## 3. Scalar-unit28 boundary is current
The canary executes root.multByConstant(28L) immediately before the split tree and checks unchanged noiseBound, ptxtSpace=625, keyID=0, primeSet, plus exact semantic decryption.

Mechanical identities:
- 8192 mod625 = 67
- 67*28 mod625 = 1
- 28^{-1} mod625 = 67

Therefore the Step-2 semantic unit path matches the CURRENT candidate.

The source does NOT explicitly read private intFactor==67. Exact decryption + unchanged-noise validates the semantic scalar-unit path, while explicit factor67 metadata remains a Step-3 interface assertion.

Results:
PASS_SCALAR_UNIT_28_CANARY_SEMANTICS
FACTOR67_METADATA_EXPLICIT_ASSERTION=NOT_TESTED_BY_STEP2

## 4. 17-call pruned recovery / routing order
Current:
J=[0,1024,7168,2048,6144]
labels=[2,0,3,1,4].

Canary active-parent counts:
[1,1,1,1,1,1,1,1,1,1,1,2,4]

Child counts:
[1,1,1,1,1,1,1,1,1,1,2,4,5]

Total Frobenius calls: 17.

Natural output coordinate order:
[0,2048,6144,1024,7168]

Mapping through current labels gives branch order:
[2,1,4,0,3]

The source's branch-reorder indices:
[3,1,0,4,2]

Independent recomputation matches both vectors.

Result:
PASS_CURRENT_PRUNED_COORD_BRANCH_ROUTING_ORDER

## 5. Exact selected dirty lifts are a valid canary oracle
The canary deliberately chooses noncanonical Z625 selected coefficients with higher base-5 digits. For this synthetic plaintext, the split circuit must return those exact coefficients. This does NOT claim production reconstruction chooses the same representatives; production only requires correct residues modulo5.

Result:
PASS_EXACT_SELECTED_DIRTY_LIFT_ORACLE_SCOPE

## 6. Exact L0,L1,L2,L3 on the chosen lifts
The canary computes all four correction outputs from the recovered leaves using exponents 1,5,25,125 and independently constructs exact polynomial references. Each ciphertext is decrypt-compared to its reference. The two physical slots use independent arbitrary lift vectors.

Result:
PASS_FOUR_CORRECTION_OUTPUT_CANARY_SCOPE

## 7. Scope refinement: production rho/443 correction is NOT tested
The synthetic second-slot vector B is already placed in the same branch-aligned selected coordinates as A. The canary does NOT feed a production-shaped second-slot state with rho-permuted residues and residue unit 182 mod5=2, and it does NOT execute the public443 correction.

Its phiInv constants are the second CRT component of the RMFE public constant; they are not the Turn25 public443 residue-correction step.

Therefore Step-2 "exact routing" means only:
- pruned coordinate order;
- coordinate-to-branch order;
- source-branch reorder indices.

It must NOT be interpreted as evidence that production second-slot rho/443 correction has executed correctly. That remains mandatory in Step3 exact parameter/interface verification.

Current arithmetic:
- 182 mod5=2
- 443 mod5=3
- 3*2=1 mod5
- 182*443=1 mod625

Results:
REFINE_STEP2_ROUTING_SCOPE_TO_PRUNED_COORD_BRANCH_ROUTING
RHO_443_PRODUCTION_CORRECTION=NOT_TESTED_BY_STEP2

## 8. Other stale architecture statements are absent
The canary has no branch-local forward stage, no aggregation/reconstruction stage, no transform-side 19/23 count, no Algorithm4, no final Recode, and no f_in restoration. It cannot silently reintroduce the old shared-forward architecture, stale count19, or old Algorithm4 factor1 statement.

## Decisive interpretation
The frozen source is version-safe as a recovery-only Step-2 canary.

A native PASS would establish only:
1. direct ptxtSpace625 Frobenius targets for the 13 required powers work in the canary;
2. semantic scalar-unit28 normalization works in the canary state;
3. the 17-call pruned split returns exact selected dirty Z625 coefficients;
4. current coordinate/branch reorder metadata are correct;
5. exact L0..L3 recombinations work on the chosen independent arbitrary slot-lift vectors.

A PASS would NOT establish:
- production ptxtSpace5 tagged-forward correctness;
- mod5->Z625 reconstruction bridge;
- real normal_basis=false inverse;
- explicit factor67 metadata;
- production second-slot rho/443 correction;
- Algorithm4 divide/factor trajectory;
- final Recode;
- f_in restoration;
- baseline correctness;
- full candidate correctness.

## Verdict
PASS_FROZEN_RECOVERY_CANARY_VERSION_SAFE
PASS_NO_STALE_Z625_FORWARD_ASSUMPTION_IN_CANARY
PASS_INDEPENDENT_CROSS_SLOT_DIRTY_LIFTS_IN_CANARY
PASS_SCALAR_UNIT_28_CANARY_SEMANTICS
PASS_CURRENT_PRUNED_COORD_BRANCH_ROUTING_ORDER
PASS_EXACT_SELECTED_DIRTY_LIFT_ORACLE_SCOPE
PASS_FOUR_CORRECTION_OUTPUT_CANARY_SCOPE

REFINE_STEP2_ROUTING_SCOPE_TO_PRUNED_COORD_BRANCH_ROUTING
FACTOR67_METADATA_EXPLICIT_ASSERTION=NOT_TESTED_BY_STEP2
RHO_443_PRODUCTION_CORRECTION=NOT_TESTED_BY_STEP2

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Next decisive test
Execute the frozen source unchanged against homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

Require:
- PASS_HELIB_RECOVERY_ONLY_EXACT_Z625_CANARY
- calls=17
- exact pruned coordinate/branch order
- scalar_unit_28=PASS
- selected_dirty_lifts=PASS
- L0_L3_exact=PASS

Do not infer rho/443, explicit factor67 metadata, forward bridge, Algorithm4, baseline correctness, or full candidate correctness from Step-2 PASS. Those remain in the preregistered Step3+ gates.
