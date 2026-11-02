# BOOT / B158 — Research Turn 15/25 — recovery-tree coefficient-L1 envelope gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes reads remain degraded and return empty objects. Durable context was recovered from BBBINGW/memory main at:

    8f7f42dd1bcea2f0fd40076307af90aef79cbc06

Immediate prerequisites:
- Turn14 repaired pure-inverse exit cleanup and independent coefficient-L1 inverse envelope;
- Turn7 exact 13-level / 17-call split recurrence theorem;
- frozen recovery-only canary blob 6ae4bc7e48e0390f8dec97429f4ddb89565928c0.

The target path was checked absent before write.

No native execution occurred. The frozen Step2 recovery-only canary remains unexecuted.

## Why this turn is necessary

Turn14 leaves the repaired recovery root on ctxtPrimes with ptxtSpace625, keyID0, intFactor67 and an independent coefficient-L1 error envelope:

    E_root <= 1.2327282569105341e27.

The next production stage is the target-pruned binary recovery tree. Although only 17 physical Frobenius calls are executed globally, every selected output leaf has depth exactly 13. The missing question is whether the key-switch/cleanup error along one selected path remains below the BGV correctness boundary.

## Closest implementation prior / exact delta

The recovery algebra is inherited from Geelen-style binary unpacking and was already proven exact in Turn7. The frozen HElib canary already implements the source-faithful shape:

    tmp = parent;
    tmp.frobeniusAutomorph(j);
    tmp.cleanUp();
    even = parent + tmp;
    odd  = X^(-s) * (parent - tmp).

Turn15 adds no novelty claim. Its exact delta is a deterministic coefficient-L1 noise envelope for this already-established 13-level recovery realization.

## Primary hypothesis

Under the same exact modulus-chain envelope used in Turn14, every selected recovery leaf remains decryptable after all 13 split levels without relying on HElib's floating embeddingLargestCoeff estimator.

## Falsifier

FAIL if the per-level recurrence implied by direct Frobenius key switching, explicit cleanup, branch addition/subtraction and odd-child monomial multiplication drives the 13-level leaf bound to or above 0.48Q.

## 1. Frozen canary proves the exact state transition shape

For every active parent the frozen canary performs one direct Frobenius matrix at ptxtSpace625, then immediately calls cleanUp(). It asserts after cleanup:

    ptxtSpace == 625
    keyID == 0
    primeSet == basePrimeSet.

The direct-matrix checks require:

    W.fromKey.getPowerOfX() == k
    W.ptxtSpace == 625.

Hence each physical parent Frobenius is exactly one direct automorphism/key-switch plus one cleanup, not a multi-hop reachability chain.

## 2. intFactor and type state remain stable

The repaired root enters recovery with intFactor67 after scalar-unit28.

Raw automorph does not change intFactor. reLinearize copies the current intFactor into its temporary ciphertext. The real mod-switch branch in cleanUp does not modify intFactor. Parent and cleaned Frobenius child therefore have the same factor67, so even/odd addition requires no harmonization scaling.

The odd-child multiplication by X^(-s) multiplies ciphertext parts by a public monomial but does not alter intFactor.

Thus every selected leaf remains:

    ptxtSpace625
    keyID0
    primeSet=ctxtPrimes
    intFactor67.

## 3. Per-Frobenius normalized error bound

Reuse Turn14's exact runtime key-switch quantity:

    K := K_KS_L1
       = 8125 * phi^2 * (sum_i D_i)/S,

where S is the product of special primes and D_i are the digit-prime products.

Reuse Turn14's cleanup rounding envelope:

    R := R_L1
       <= 83,891,200,000.

For a parent with coefficient-L1 decryption-error envelope E, the direct Frobenius automorphism preserves the canonical norm. reLinearize first scales the old error by S and adds key-switch error K_pre. The subsequent cleanup divides by S and adds rounding error R.

Therefore the cleaned Frobenius result satisfies:

    E_frob <= E + K + R.

This statement is independent of HElib's floating noiseBound metadata.

## 4. Split recurrence

Even child:

    even = parent + cleaned_frob.

Odd child:

    odd = X^(-s) * (parent - cleaned_frob).

For m=2^15, multiplication by X^(-s) is a signed coefficient permutation modulo X^16384+1 and has canonical magnitude one at every primitive root. It therefore does not increase the decryption-error norm.

Hence both child types obey the same recurrence:

    E_(l+1) <= 2 E_l + K + R.

## 5. Why 17 physical calls do not mean 17 noise additions per leaf

Turn7 and the frozen canary give the parent-count sequence:

    1,1,1,1,1,1,1,1,1,1,1,2,4

and child-count sequence:

    1,1,1,1,1,1,1,1,1,1,2,4,5.

The global physical call count is 17 because later levels contain multiple active parents. Each final selected leaf nevertheless has exactly one parent at each of the 13 levels.

Therefore one leaf accumulates 13 key-switch/cleanup events, not 17.

## 6. Closed-form leaf envelope

Solving:

    E_(l+1) <= 2 E_l + K + R

for 13 levels gives:

    E_leaf
      <= 2^13 E_root + (2^13 - 1)(K+R)
      = 8192 E_root + 8191(K+R).

This exact symbolic form is the production audit formula. Step3 should instantiate it from runtime S and D_i.

## 7. Source-sizing preflight

Use Turn14's deliberately conservative sufficient preflight:

    E_root <= 1.2327282569105341e27
    K <= 401,679,183,790,908.6
    R <= 83,891,200,000.

Then:

    E_leaf <= 1.0098509880614386e31
    log2(E_leaf) <= 102.9939133685.

With the source-faithful bits_HElib=400 modulus lower bound:

    log2(Q) >= 399.5,

we obtain:

    log2(Q/E_leaf) >= 296.5060866315 bits.

Turn11's current-ring correctness threshold is:

    log2(1/0.48) = 1.0588936891 bits.

So every selected leaf retains at least:

    295.4471929424 bits

above the HElib decryption-correctness boundary under the stated sufficient preflight.

## 8. Recovery pruning does not worsen the per-leaf bound

The pruned tree shares ancestors computationally but never adds unrelated sibling ciphertexts into one selected leaf. The only operations along a selected path are one Frobenius+cleanup and one plus/minus split per level.

Therefore the worst-leaf bound depends on depth13 and not on the total number of active nodes or global call count17.

## 9. Consequence for the construction

The independent coefficient-L1 correctness envelope now propagates through:

    shared reconstruction
    -> repaired pure inverse + cleanup
    -> scalar-unit28
    -> full 13-level selected recovery leaves.

No additional cleanup repair is needed inside recovery because the frozen source-faithful canary already performs tmp.cleanUp() immediately after every Frobenius.

## 10. Step3 exact assertions

After mandatory Step2 PASS, Step3 must compute exact:

    S = product(specialPrimes)
    every D_i
    K = 8125*phi^2*(sum_i D_i)/S
    R = 312.5*phi*(1+phi)
    E_leaf_bound = 8192*E_root + 8191*(K+R).

At every recovery Frobenius after cleanup assert:

    primeSet == ctxtPrimes
    ptxtSpace == 625
    keyID == 0
    intFactor == 67.

Do not substitute the global 17-call count into the per-leaf recurrence.

## Verdict

PASS_RECOVERY_PER_LEVEL_L1_RECURRENCE
PASS_SELECTED_LEAF_DEPTH13_NOT_GLOBAL_CALL17
PASS_CONDITIONAL_RECOVERY_TREE_COEFFICIENT_L1_ENVELOPE

SOURCE_SIZING_PREFLIGHT_LEAF_ERROR_MAX:
  1.0098509880614386e31

SOURCE_SIZING_PREFLIGHT_LOG2_Q_OVER_LEAF_ERROR:
  296.5060866315 bits

SOURCE_SIZING_PREFLIGHT_CORRECTNESS_MARGIN:
  295.4471929424 bits

EXACT_RUNTIME_RECURRENCE:
  E_leaf <= 8192*E_root + 8191*(K_KS_L1 + R_L1)

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

This turn propagates the independent coefficient-L1 envelope through the selected recovery leaves only.

It does not yet cover:
- the five-leaf public L0-L3 correction accumulations;
- Algorithm4 and its six divideByP boundaries;
- final Recode;
- final DFR.

## Next decisive test

Mandatory evidence order remains Step2: execute the frozen revised recovery-only canary unchanged against homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON and require the exact PASS output.

After Step2 PASS, Step3 must instantiate the repaired pure inverse and the exact runtime S/D_i coefficient-L1 envelope, then verify the 13-level leaf recurrence above before entering L0-L3 / Algorithm4.