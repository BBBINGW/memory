# BOOT / B158 — Research Turn 16/25 — L0-L3 rho/443 coefficient-L1 envelope gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes reads remain degraded. Durable context was recovered by direct GitHub fetch from BBBINGW/memory main at:

    c25e52424b78ede3a16c29d66baacc1083d80b88

Immediate prerequisites:
- Turn15 recovery-tree independent coefficient-L1 leaf envelope;
- Turn25 end-to-end static closure, which supersedes exact lifted rho coherence and reinterprets public443 as a residue correction;
- frozen recovery-only canary exact RMFE basis constants and global CRT idempotents;
- historical exact four-output interface.

The target finding path was checked absent before write.

No native execution occurred. Mandatory Step2 recovery canary remains unexecuted.

## Why this turn matters

Turn15 proves every selected recovered leaf has a large independent coefficient-L1 correctness envelope. The next production edge is:

    five recovered leaves
    -> second-slot rho/permutation/public443 residue correction
    -> four public linear recombinations L0,L1,L2,L3.

This edge is important because Turn25 reintroduced public443 under a new rationale: not exact recovery of a canonical lifted rho relation, but conversion of a second-slot residue 2*b mod5 into an arbitrary correct lift of b. The remaining paper-level uncertainty is whether these public constants amplify the independent actual-error envelope enough to threaten correctness before Algorithm4.

## Closest prior / exact delta

Aung correction-style CtxtsToSlots and the historical four-output interface already establish the semantic formulas. Turn25 establishes the residue-level need for public443.

Turn16 adds no novelty claim. Its exact delta is an estimator-independent, exact full-ring coefficient-L1 audit of the ACTUAL public routing/correction constants used at this boundary.

## Primary hypothesis

After the current residue-based rho/443 correction, the exact public constants used to form L0..L3 have sufficiently small full-ring coefficient-L1 norms that all four Algorithm4 input ciphertexts remain far inside the BGV correctness region.

## Falsifier

FAIL if:
- the current rho/443 correction requires a key switch or a secret-dependent map;
- the effective public constants cannot be represented exactly in the pinned full plaintext ring;
- their exact coefficient-L1 amplification drives any L_r error envelope to or above 0.48Q;
- or addition requires factor/prime-set harmonization that introduces an unaccounted operation.

## 1. Current Turn25 interpretation of rho/443

Turn25 supersedes the older requirement of exact lifted rho coherence.

For every nonzero selected coordinate the raw second physical slot only needs:

    b_tilde mod5 = 2*b.

The public unit:

    443 mod625

satisfies:

    443 mod5 = 3
    3*2 = 1 mod5.

Thus 443*b_tilde is simply another arbitrary Z625 lift of the intended branch scalar b.

At coordinate0 no unit correction is required.

Branch label2 is exactly the coordinate0 branch because J-order labels are [2,0,3,1,4]. Therefore branch2 is the unique branch without the 443 correction; branches0,1,3,4 use it.

## 2. Exact global routing selector

The frozen exact two-slot ring uses CRT idempotents:

    e0 = 313 + 91 X^8192
    e1 = 313 - 91 X^8192

in R=(Z/625Z)[X]/(X^16384+1).

A public constant acting as identity in the first physical slot and 443 in the second is:

    R443 = e0 + 443 e1.

Reducing coefficients modulo625 to balanced representatives gives exactly:

    R443 = 222 - 222 X^8192.

Hence:

    ||R443||_1 = 444.

This is an exact full-ring coefficient-L1 value, not a floating embedding estimate.

## 3. Exact correction constants

The frozen RMFE basis coefficients, indexed by source branch i=0..4, are:

    ell0 = [1,50,340,260,599]
    ell1 = [0,4,204,314,104]
    ell2 = [0,622,161,623,469]
    ell3 = [0,418,206,522,104]
    ell4 = [0,156,339,156,599].

Define:

    phi_i(X) = sum_{k=0}^4 ell_i[k] X^(16k).

For r=0,1,2,3 let exp_r=1,5,25,125.

The global two-slot public correction constant is:

    B_(i,r)
      = e0 * phi_i^(exp_r)
        + e1 * rho(phi_i^(exp_r)),

where rho is the second physical-slot conjugation. In the frozen exact ring representation:

    rho(phi_i)(X) = phi_i(X^(-1)).

These are exactly the global constants whose two physical slots realize:

    phi(e_i)^(5^r)
and
    rho(phi(e_i)^(5^r)).

## 4. Fuse routing with correction before bounding

Even if an implementation applies public443 routing and the correction multiplier as two separate ciphertext-plaintext multiplications, ring associativity means the actual decryption error is multiplied by their PRODUCT element.

Therefore the correct tight estimator-independent bound uses the fused constants:

    F_(2,r) = B_(2,r),
    F_(i,r) = R443 * B_(i,r) for i in {0,1,3,4}.

This is much tighter than multiplying a generic 444 factor by a separate generic B_i,r bound.

All arithmetic below was evaluated exactly modulo625 in the full ring X^16384+1, using balanced integer representatives.

## 5. Exact full-ring coefficient-L1 table

Exact ||F_(i,r)||_1 values are:

r=0:
    branch0 2538
    branch1 2050
    branch2 3064
    branch3 1614
    branch4 2056
    A0 = total = 11322.

r=1:
    branch0 12082
    branch1 7880
    branch2 10304
    branch3 9398
    branch4 9884
    A1 = total = 49548.

r=2:
    branch0 54230
    branch1 51092
    branch2 46402
    branch3 44034
    branch4 44324
    A2 = total = 240082.

r=3:
    branch0 35508
    branch1 154091
    branch2 156124
    branch3 154091
    branch4 154091
    A3 = total = 653905.

Corresponding amplification bits:

    log2(A0) = 13.4668412083
    log2(A1) = 15.5965392039
    log2(A2) = 17.8731677169
    log2(A3) = 19.3187215291.

The worst correction output is therefore L3.

## 6. No fresh cryptographic noise at this edge

At the Turn15 selected-leaf boundary every leaf is already:

    primeSet = ctxtPrimes
    ptxtSpace = 625
    keyID = 0
    intFactor = 67.

Public polynomial multiplication:
- does not key-switch;
- does not add fresh RLWE error;
- does not change primeSet;
- does not change intFactor.

Routing is only a permutation of which recovered leaf is assigned to which branch plus public multiplication by R443 on the four nonzero branches.

All five routed branches retain the same ptxtSpace/keyID/primeSet/factor type.

Adding them to form one L_r therefore requires neither prime-set mod-up nor BGV factor harmonization.

HElib metadata may estimate a public multiplier with embeddingLargestCoeff, but the actual decryption-error envelope here is bounded independently by the exact coefficient-L1 constants above.

## 7. Exact L_r error formula

Let E_i be the independent actual-error envelope of routed branch i BEFORE the correction multiplier. Using a common selected-leaf bound E_leaf from Turn15 gives:

    E(L_r) <= E_leaf * A_r.

More generally Step3 may use:

    E(L_r) <= sum_i E_leaf_i * ||F_(i,r)||_1.

No additive fresh-noise term appears at this boundary.

## 8. Source-sizing preflight

Turn15's deliberately conservative source-sizing preflight is:

    E_leaf <= 1.0098509880614386e31.

Therefore:

    E_L0 <= 1.1433532886831608e35
    E_L1 <= 5.003609675646816e35
    E_L2 <= 2.4244704491576632e36
    E_L3 <= 6.60346610348315e36.

Logs:

    log2(E_L0) <= 116.4607545768
    log2(E_L1) <= 118.5904525724
    log2(E_L2) <= 120.8670810854
    log2(E_L3) <= 122.3126348976.

With bits_HElib=400:

    log2(Q) >= 399.5.

Thus:

    log2(Q/E_L0) >= 283.0392454232
    log2(Q/E_L1) >= 280.9095474276
    log2(Q/E_L2) >= 278.6329189146
    log2(Q/E_L3) >= 277.1873651024.

Subtracting the current-ring correctness threshold log2(1/0.48)=1.0588936891 gives margins:

    L0 >= 281.9803517341 bits
    L1 >= 279.8506537385 bits
    L2 >= 277.5740252256 bits
    L3 >= 276.1284714133 bits.

Therefore all four Algorithm4 input correction ciphertexts remain extremely far inside the decryption-correctness boundary under the current sufficient preflight.

## 9. Exact runtime audit formula

The fixed public amplification factors are context-independent:

    A = [11322,49548,240082,653905].

After native Step3 computes the exact runtime selected-leaf envelope:

    E_leaf_runtime

it may immediately certify:

    E_Lr_runtime <= A_r * E_leaf_runtime.

If leaf-specific bounds are tracked, use the branchwise F_(i,r) table for a tighter result.

## 10. Construction consequence

The independent coefficient-L1 correctness chain now reaches the exact inputs of Aung Algorithm4:

    shared reconstruction
    -> repaired pure inverse + cleanup
    -> scalar-unit28
    -> 13-level target-pruned recovered leaves
    -> slotwise rho/permutation/public443 residue correction
    -> exact L0,L1,L2,L3.

At the L0-L3 output boundary the common metadata type remains:

    primeSet = ctxtPrimes
    ptxtSpace = 625
    keyID = 0
    intFactor = 67.

This agrees with the current Turn23 factor67 Algorithm4 entry theorem.

## Verdict

PASS_RHO443_PUBLIC_SELECTOR_EXACT_L1
PASS_EXACT_FUSED_CORRECTION_CONSTANT_L1_TABLE
PASS_L0_L3_COEFFICIENT_L1_ENVELOPE
PASS_ALGORITHM4_ENTRY_CORRECTNESS_MARGIN

FIXED_PUBLIC_AMPLIFICATION_FACTORS:
    [11322,49548,240082,653905]

WORST_OUTPUT:
    L3

SOURCE_SIZING_PREFLIGHT_L3_ERROR_MAX:
    6.60346610348315e36

SOURCE_SIZING_PREFLIGHT_L3_Q_OVER_ERROR_BITS:
    277.1873651024 bits

SOURCE_SIZING_PREFLIGHT_L3_CORRECTNESS_MARGIN:
    276.1284714133 bits

NATIVE_EXECUTION:
    NOT_OBTAINED

RECOVERY_CANARY:
    NOT_EXECUTED

CORRECTNESS_GATE:
    BLOCKED

BASELINE_CORRECTNESS:
    PENDING

NOVELTY_STATUS:
    PREFLIGHT

SECURITY_GATE:
    PENDING

VALUE_GATE:
    PENDING

AUDIT_GATE:
    PENDING

PAPER_READINESS:
    NOT_READY

## Scope boundary

This turn closes only the recovered-leaf -> rho/443 routing -> L0-L3 public-linear boundary.

It does NOT propagate the independent coefficient-L1 envelope through:
- Algorithm4 Fe ciphertext multiplications;
- factor harmonization choices inside y-u subtraction;
- the six divideByP boundaries;
- final Recode;
- final DFR.

Those remain downstream correctness/noise gates.

## Next decisive test

Mandatory evidence order remains Step2: execute the frozen revised recovery-only canary unchanged against homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON and require the exact PASS output.

After Step2 PASS, Step3 must instantiate the repaired real inverse, exact S/D_i key-switch envelope, recovery leaf recurrence, production rho/443 routing, and the fixed L0-L3 amplification factors above before entering Algorithm4.