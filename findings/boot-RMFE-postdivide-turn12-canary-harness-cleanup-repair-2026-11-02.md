# BOOT Research Turn 12/25 — HElib recovery canary harness falsification and cleanup repair

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

The durable Turn-11 recovery-only canary source is already source-faithful enough that, once a compatible HElib toolchain is available, compiling/running it would cleanly test the intended 17-call recovery rather than fail because of test-harness assumptions.

Falsifier:
- any canary assertion contradicts pinned HElib's own source behavior;
- any required HElib maintenance operation is missing from the Turn-10/11 implementation contract;
- a HElib diagnostic known by the pinned source to be unreliable is incorrectly promoted to an acceptance criterion.

## Result

FAIL_TURN11_CANARY_HARNESS_AS_WRITTEN
ATTRIBUTION: TEST_HARNESS / IMPLEMENTATION_CONTRACT
ALGORITHMIC_OBSTRUCTION: NO

Two independent source-level falsifiers were found.

## 1. Frobenius does not preserve the root primeSet by itself

Turn 10 stated that a recovery-node Frobenius preserves primeSet, so Turn 11 asserted

  tmp.getPrimeSet() == basePrimeSet

immediately after

  tmp.frobeniusAutomorph(j).

Pinned src/Ctxt.cpp shows this is false for smartAutomorph:

- smartAutomorph applies automorph(amt);
- then calls reLinearize(keyID);
- reLinearize first drops small/special primes from its input;
- it creates the output temporary ciphertext with

    tmp.primeSet = primeSet | context.getSpecialPrimes();

- and assigns that temporary back to the ciphertext.

Therefore a direct Frobenius call normally exits with the special primes attached.

If Turn-11 were compiled exactly as originally written, the first

  assert(tmp.getPrimeSet() == basePrimeSet)

would be expected to fail even when the automorphism and plaintext semantics were correct.

### Source-faithful repair

Pinned src/intraSlot.cpp already establishes the intended HElib pattern. In unpack_pa_impl, every Frobenius image is computed as

  frob[j] = ctxt;
  frob[j].frobeniusAutomorph(j);
  frob[j].cleanUp();

The source even contains the comment asking why cleanup is applied after Frobenius, but the behavior is unambiguous.

Ctxt::cleanUp():
- reLinearize() is a no-op when the ciphertext is already canonical;
- then drops special/small primes if present.

Thus the corrected recovery node is:

  tmp = c;
  tmp.frobeniusAutomorph(j);
  tmp.cleanUp();
  even = c + tmp;
  odd  = X^{-s}(c - tmp).

With this source-faithful cleanup, parent and Frobenius child return to the same base primeSet before addition/subtraction.

### Consequence for the operation contract

The canonical recovery specification is now:

- 17 Frobenius/smartAutomorph direct-key-switch calls;
- 17 post-Frobenius cleanUp/drop-special operations;
- 21 retained additions/subtractions;
- 5 retained global monomial multiplications.

The number 17 remains the exact Frobenius/key-switch count. It is NOT the total recovery operation count.

This does not by itself invalidate prior value or capacity conclusions, because those were explicitly not matched native predictions and did not model automorphism/key-switch noise. However, all future matched noise/value evidence must include the source-faithful cleanup operations.

## 2. Ctxt::isCorrect() is not a valid hard acceptance oracle here

Turn-11 assertDecrypt originally contained:

  assert(c.isCorrect());

Pinned tests/GTestExtractDigits.cpp explicitly disables this check:

  // Removed isCorrect for now, as it is not correctly defined

before decrypting digit ciphertexts.

Pinned src/keys.cpp nevertheless calls ciphertxt.isCorrect() inside SecKey::Decrypt. In a normal non-HELIB_DEBUG build, a false result throws LogicError before decryption; with HELIB_DEBUG defined, HElib emits a warning and continues.

Therefore merely deleting the external assert is insufficient. A release build could still turn an unreliable tracked-noise estimate into a false correctness failure.

### Source-faithful canary repair

The canary is now required to be linked against HElib configured with

  -DHELIB_DEBUG=ON

and contains a compile-time #error when HELIB_DEBUG is absent.

It also calls

  helib::setupDebugGlobals(&sk, context.shareEA())

and cleanupDebugGlobals(), matching pinned HElib test practice.

isCorrect() is retained only as a printed diagnostic. The decisive acceptance oracle is:

  SecKey::Decrypt in HELIB_DEBUG mode
  +
  exact coefficient-by-coefficient equality modulo 625
  against the independent global-ring oracle.

This preserves actual decrypt/intFactor semantics while preventing a known-unreliable estimate from becoming the theorem oracle.

## 3. Additional compile-harness correction

During the repair, re-reading the persisted source found an accidental literal "\n" between two include directives introduced by the first text patch. That was a pure source-editing compile error, not an HElib issue. It was removed before freezing the revised source.

The final durable canary source is:

  findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt

blob SHA:

  2a3fc5e2e318a851532f998987139cd2cfa7634d

commit carrying the final source repair:

  2a5e354b676bec877cd3099369c20ab3f7d4c748

## 4. What remains unchanged in the canary

The repaired source still enforces:

- application-style context r=1;
- TEST-ONLY SecKey::Encrypt(...,625) to avoid a mod-5 false positive;
- exactly 13 targeted direct Frobenius matrices generated with ptxtSpace=625;
- production normalization 28 before the tree;
- selected coordinates carrying distinct 5-divisible dirty higher digits;
- additional off-target 5-divisible dirty state;
- coordinate-labelled pruning;
- exact source-style final order [0,2048,6144,1024,7168];
- 17 Frobenius calls;
- no post-unpack rho_pos+443 correction;
- exact dirty-Z625 five-leaf comparison;
- exact L0,L1,L2,L3 comparison.

## 5. Execution-path audit

This turn attempted to execute the already-constructed canary without starting bootstrapping or performance work.

Current sandbox:
- cmake and g++ available;
- GMP runtime/dev package available;
- NTL headers/library absent;
- apt reports no libntl-dev candidate before refresh;
- apt-get update did not complete within the bounded attempt;
- direct GitHub DNS resolution is unavailable.

GitHub execution alternatives:
- normal GitHub App branch creation / contents write returned 403 Resource not accessible by integration;
- GitHub Notes correctly persists findings but blocks hidden .github/workflows paths;
- therefore a one-shot Actions workflow could not be created from the available tools.

No native correctness result was obtained.

These infrastructure failures are NOT evidence against the candidate.

## Complete-paper uncertainty reduced

Before Turn 12, a future failed canary could have been misclassified as candidate failure merely because:
1. the harness expected primeSet invariance immediately after frobeniusAutomorph; or
2. isCorrect() rejected a ciphertext before exact semantic comparison.

Both false-failure channels are now removed.

The remaining correctness uncertainty is narrower:

  Does the repaired source-faithful HElib circuit, including per-Frobenius cleanUp, actually decrypt to the exact Turn-9 global-ring oracle at every node and at L0..L3?

## Verdict

PRIMARY_HYPOTHESIS: FAIL

FAIL_TURN11_CANARY_HARNESS_AS_WRITTEN
PASS_BOUNDED_HARNESS_REPAIR
PASS_SOURCE_FAITHFUL_FROBENIUS_CLEANUP_CONTRACT
PASS_EXACT_DECRYPT_ORACLE_POLICY
ALGORITHMIC_OBSTRUCTION: NO
NATIVE_EXECUTION: NOT_OBTAINED

CORRECTNESS_GATE remains BLOCKED.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Compile pinned HElib with HELIB_DEBUG=ON and run exactly the revised durable canary source.

No timing and no full bootstrapping.

Acceptance requires:
- every exact per-node decrypt comparison mod625;
- 17 Frobenius calls;
- source-faithful cleanUp after every Frobenius;
- exact pruned routing;
- exact dirty Z625 leaves;
- exact L0..L3.

A false isCorrect diagnostic alone is NOT failure. An exact decryption/oracle mismatch is failure and must be localized to the first node.
