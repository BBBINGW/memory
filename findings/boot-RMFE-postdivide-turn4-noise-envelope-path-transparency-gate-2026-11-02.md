# BOOT / B158 — Research Turn 4/25 — explicit noise-envelope path-transparency gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read calls remain degraded and return empty objects for existing findings. Current durable state was recovered from BBBINGW/memory at verified HEAD:

    2dc155280a87e59bed5bcacf40511e9361723859

Authoritative immediate predecessor:
- findings/boot-RMFE-postdivide-turn3-shared-reconstruction-noisebound-explicit-envelope-gate-2026-11-02.md
- blob 0f8ed29f14a9314d8905bad451fda5e1841ffa3b

Turn3 established a public-API conservative shared-reconstruction noise envelope using explicit size arguments, but did not yet prove that deliberately increasing the software noiseBound cannot alter later adaptive HElib arithmetic/prime-set control flow.

The new target finding path was checked before write and was absent.

No native execution occurred.

## Closest implementation prior / exact delta

Closest implementation prior remains pinned stock HElib recryption and EvalMap/automorphism machinery.

No novelty claim is added.

The exact candidate-specific delta under test is:
Turn3 may set the shared reconstruction noiseBound to a conservative five-branch envelope rather than HElib's default estimator for the summed ZZX constants.

Question:
can that larger metadata value change the actual pure-inverse/recovery computation via noise/capacity-dependent level management?

## Primary hypothesis

For the CURRENT post-divide candidate at the pinned HElib commit, using the Turn3 conservative explicit-size noise envelope changes estimator metadata only throughout:

    shared reconstruction
    -> pure normal_basis=false EvalMap inverse
    -> scalar-unit28
    -> 17-call Frobenius recovery,

and cannot change:
- which ciphertext primes are retained;
- whether a different mod-switch arithmetic branch is selected;
- which key-switch route is used;
- the ciphertext plaintext semantics.

## Falsifier

FAIL if one reachable source path after shared reconstruction:
1. reads noiseBound/capacity and, based on it, changes the target primeSet;
2. selects "drop primes" versus true modulus switching based on noiseBound;
3. selects a different automorphism/key-switch route based on capacity;
4. introduces smallPrimes so that dropSmallAndSpecialPrimes enters its noise-dependent compensation branch;
5. otherwise changes ciphertext arithmetic because the Turn3 guard is larger.

Warnings/statistics alone are not falsifiers.

## Minimal decisive test

Audit only the reachable pinned-source control flow:
1. recryptEkey generation / initial primeSet;
2. EvalMap::apply and matrix-multiply entry cleanup;
3. smartAutomorph/frobeniusAutomorph/reLinearize;
4. cleanUp/dropSmallAndSpecialPrimes/modDownToSet;
5. hoisted automorphism precomputation.

No performance or capacity verdict is inferred.

## 1. Shared reconstruction starts on ctxtPrimes only

Pinned SecKey::genRecryptData encrypts the bootstrapping key using:

    Encrypt(recryptEkey, keyPoly, p2ePr).

Pinned SecKey::skEncrypt initializes:

    ctxt.primeSet = context.getCtxtPrimes();
    ctxt.intFactor = 1;

and creates the ordinary two canonical parts (1,s).

Therefore:

    primeSet(recryptEkey) = ctxtPrimes.

The current reconstruction:

    ctxt = recryptEkey;
    ctxt.multByConstant(Z1, S1);
    ctxt.addConstant(Z0, S0);

does not change the primeSet or secret-key handles.

So immediately after shared reconstruction:

    primeSet = ctxtPrimes
    no smallPrimes
    no specialPrimes
    canonical keyID0 form.

This remains true whether S0,S1 are default or conservative explicit estimator sizes.

## 2. EvalMap entry cleanup is a no-op on primeSet

Pinned EvalMap::apply delegates to MatMul1DExec / BlockMatMul1DExec.

Both matrix multiply entry points call:

    ctxt.cleanUp();

Pinned Ctxt::cleanUp does:

    reLinearize();
    if (special or small primes present)
        dropSmallAndSpecialPrimes();

For the reconstructed ciphertext:
- it is already canonical, so reLinearize returns immediately;
- primeSet is exactly ctxtPrimes, so the small/special test is false.

Therefore the pure-inverse entry cleanup does not inspect noiseBound to alter the prime set.

Result:
PASS_EVALMAP_ENTRY_CLEANUP_PATH_INDEPENDENT_OF_GUARD

## 3. Automorphism/key-switch route is not selected from capacity

Pinned Ctxt::smartAutomorph chooses the key-switch path from:
- target automorphism k;
- keyID;
- public-key reachability / KS matrices.

It does not read capacity/noiseBound to select the route.

Pinned frobeniusAutomorph only maps Frobenius exponent j to the corresponding automorphism and invokes smartAutomorph.

Matrix-multiplication strategy is chosen from:
- transform dimensions;
- minimal/FULL/BSGS key-switch strategy;
- thread availability.

It is not chosen from ciphertext capacity/noiseBound.

Thus the conservative Turn3 guard cannot alter which automorphism/key-switch sequence is executed.

Result:
PASS_AUTOMORPH_ROUTE_INDEPENDENT_OF_GUARD

## 4. reLinearize can add special primes but not small primes on this path

When smartAutomorph makes the ciphertext noncanonical, reLinearize is invoked.

At reLinearize entry, input primeSet is still a subset of ctxtPrimes. Its initial:

    dropSmallAndSpecialPrimes();

therefore sees no smallPrimes and no specialPrimes and performs no prime-set change.

The key-switch itself creates the temporary result on:

    primeSet | specialPrimes.

Thus key switching can introduce specialPrimes, but not smallPrimes.

Subsequent cleanUp sees:
- specialPrimes present;
- smallPrimes absent.

Hence it takes the FIRST branch of dropSmallAndSpecialPrimes:

    if (primeSet.disjointFrom(smallPrimes))
        modDownToSet(ctxtPrimes);

The noise-dependent target-selection branch is only reachable when smallPrimes are present, which is not the case on this reconstruction/EvalMap/recovery path.

Result:
PASS_NO_SMALL_PRIME_NOISE_COMPENSATION_PATH

## 5. modDownToSet target/arithmetic is noise-path independent in pinned commit

Even when cleanup removes temporary special primes, pinned modDownToSet does not choose a different arithmetic branch from noiseBound.

The source contains two potential noise-dependent alternatives, but both are compile-time/runtime disabled:

    if (0 && isCKKS()) { ... }

and:

    if (0 && noiseBound <= addedNoiseBound) {
        // degenerate drop
    } else {
        // real modulus switching
    }

Therefore the executed branch is unconditionally the real modulus-switch path whenever primes are actually removed.

The target remains:

    ctxtPrimes.

noiseBound is used only to update the resulting estimate, not to select drop-versus-modswitch behavior.

Result:
PASS_MODDOWN_EXECUTION_BRANCH_INDEPENDENT_OF_GUARD

## 6. Hoisted automorphism uses guard only in estimator arithmetic

Pinned BasicAutomorphPrecon first cleanUp's a private ciphertext copy.

It then computes:

    noise = ctxt.getNoiseBound() * product(specialPrimes)
    noise += estimated key-switch addedNoise.

This value is assigned to the output automorphism ciphertext's noiseBound.

The only control-flow comparison involving the ratio is:

    if (ratio > 1)
        Warning(...);

It does not change:
- key-switch matrix;
- primeSet;
- automorphism exponent;
- ciphertext parts.

Therefore a larger Turn3 envelope propagates conservatively through hoisted output metadata but does not alter the arithmetic route.

Result:
PASS_HOISTED_PRECON_METADATA_ONLY_DEPENDENCE

## 7. Consequence for scalar-unit28 and 17-call recovery

After the pure inverse, candidate scalar-unit28 uses ordinary BGV constant multiplication.

The 17-call recovery repeats:
- Frobenius smartAutomorph;
- cleanUp;
- additions/subtractions;
- public monomial multiplications.

The same invariants continue:
- no operation introduces smallPrimes;
- temporary specialPrimes arise only from key switching;
- cleanUp removes them to ctxtPrimes by the deterministic first branch;
- no reachable arithmetic/prime-set branch depends on noiseBound/capacity.

Therefore the Turn3 explicit estimator guard is path-transparent through E6/E7 of the current construction.

## 8. Important scope boundary

This is a static source result for the fixed pinned HElib path.

It does NOT prove:
- the conservative envelope is below the available modulus;
- final capacity is positive;
- native recovery succeeds;
- DFR;
- matched performance.

A sufficiently large conservative guard may still make reported capacity small/negative and thereby reveal that the candidate lacks numerical margin. That is a legitimate later native correctness/noise failure.

What this turn proves is narrower:

    changing to the conservative Turn3 guard cannot itself cause HElib
    to silently choose a different pure-inverse/recovery prime-set or
    automorphism algorithm on the fixed path.

Thus native failure under the guarded path should be interpreted as actual margin/interface failure, not as an estimator-induced control-flow artifact.

## Verdict

PASS_EXPLICIT_NOISE_GUARD_PATH_TRANSPARENCY
PASS_EVALMAP_ENTRY_CLEANUP_PATH_INDEPENDENT_OF_GUARD
PASS_AUTOMORPH_ROUTE_INDEPENDENT_OF_GUARD
PASS_NO_SMALL_PRIME_NOISE_COMPENSATION_PATH
PASS_MODDOWN_EXECUTION_BRANCH_INDEPENDENT_OF_GUARD
PASS_HOISTED_PRECON_METADATA_ONLY_DEPENDENCE

REFINE_TURN3_GUARD_AS_SEMANTICALLY_PATH_TRANSPARENT_THROUGH_E6_E7

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Step3 instrumentation refinement

After Step2 native PASS, exact-interface verification should record:
- shared reconstruction primeSet == recryptEkey primeSet == ctxtPrimes;
- no smallPrimes at reconstruction, pure-inverse entry, and each recovery node;
- any temporary specialPrimes arise only around key switching;
- cleanUp returns each instrumented recovery node to the expected ctxt-prime set;
- guarded S0/S1 noise metadata follows Turn3 equation.

No performance claim is authorized.

## Next decisive test

The evidence-order blocker remains unchanged:
execute the frozen revised recovery-only canary against the pinned HElib commit with HELIB_DEBUG=ON.

After Step2 PASS, proceed to the enlarged Step3 exact-interface oracle including the Turn3 estimator ledger and the prime-set/path invariants above.
