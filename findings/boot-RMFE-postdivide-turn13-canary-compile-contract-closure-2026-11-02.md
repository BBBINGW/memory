# BOOT Research Turn 13/25 — recovery-canary compile-contract closure

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

After Turn 12's cleanup/isCorrect repair, the recovery-only canary can be closed into a source-faithful compile-ready test without changing the candidate mechanism; any remaining blocker should then be pure execution/toolchain availability rather than another unresolved HElib semantic ambiguity.

Minimal decisive test:
1. re-read the durable Turn-12 finding and repaired canary source;
2. audit every canary-only external HElib interface used by the repaired source against the pinned headers/source;
3. specifically falsify prime-set cleanup, direct-625 key-switch generation, debug-decrypt, and pre-existing-matrix assumptions;
4. search the current runtime for any reusable NTL/HElib build/package cache and execute if one exists;
5. if a bounded source defect is found, repair it once and re-read the durable source.

No performance work, full bootstrapping, or alternative candidate is introduced.

## 1. Execution remains unavailable in the current runtime

A fresh local audit found:

- root access is available;
- cmake and g++ are installed;
- GMP is present;
- no NTL header/library exists under /usr, /usr/local, /opt, /mnt/data or /home/oai within the bounded search;
- no cached libntl/HElib package exists in /var/cache/apt/archives;
- apt-cache has no libntl-dev candidate;
- apt-get update fails because deb.debian.org DNS cannot resolve;
- github.com DNS also does not resolve.

No hidden reusable HElib/NTL build or source tree was found.

Pinned HElib commit acdb264e... has no reusable workflow run/artifact exposed by the available GitHub connector.

Attempts to create a temporary GitHub Actions execution path remain unavailable:
- ordinary GitHub App branch/content writes return 403 Resource not accessible by integration;
- GitHub Notes persists findings/source but blocks hidden .github/workflows paths.

Therefore no native correctness result is produced in Turn 13.

This is infrastructure evidence only and is not candidate evidence.

## 2. One remaining compile defect was found and repaired

Turn 12 correctly changed the canary to require HELIB_DEBUG=ON and call:

  helib::setupDebugGlobals(...)
  helib::cleanupDebugGlobals()

However pinned include/helib/helib.h does NOT include helib/debugging.h.

Therefore the Turn-12 source was not yet compile-closed: the debug functions were used without their declaring header.

The durable source now explicitly includes:

  #include <helib/debugging.h>

This is a test-harness compile repair only.

## 3. cleanUp prime-set contract is source-closed

Pinned Ctxt::smartAutomorph calls automorph followed by reLinearize.

reLinearize creates its result at:

  current ctxt primes | special primes.

The repaired canary then calls Ctxt::cleanUp().

For the recovery-only canary input:
- SecKey::Encrypt initializes primeSet=context.getCtxtPrimes();
- the tree never introduces smallPrimes;
- after direct Frobenius/relinearization the state is
    context.getCtxtPrimes() | context.getSpecialPrimes().

Pinned dropSmallAndSpecialPrimes sees that the primeSet is disjoint from smallPrimes and executes:

  modDownToSet(context.getCtxtPrimes()).

Hence in this exact canary:
- cleanUp removes the special primes;
- it does not select a smaller adaptive ciphertext-prime subset;
- after cleanup, tmp.getPrimeSet()==basePrimeSet is a valid assertion.

The Turn-12 sibling-alignment repair is therefore source-correct.

## 4. cleanup preserves the semantic plaintext interface

The active modDownToSet path is real modulus switching, not the disabled degenerate-drop branch.

It changes the DCRT representatives/noise estimate while preserving the BGV plaintext semantics at the same ptxtSpace. There is no explicit intFactor mutation in this active branch.

Thus after:
  tmp.frobeniusAutomorph(j);
  tmp.cleanUp();

the parent and Frobenius image remain semantically addable in the same temporary Z_625 plaintext space.

The exact decrypt oracle remains the decisive runtime test.

## 5. explicit 625 key-switch matrices cannot be silently shadowed by GenSecKey

GenKeySWmatrix returns early when an identical handle-to-handle matrix already exists, so a possible false-positive risk was:

  GenSecKey creates ptxtSpace=5 Frobenius matrices,
  then the canary's GenKeySWmatrix(...,625) silently no-ops.

Pinned SecKey::GenSecKey/ImportSecKey does not do this.

ImportSecKey generates only degree-relinearization matrices:

  s^e -> s, e=2,...,maxDegKswitch,

with fromXPower=1.

It does not generate nontrivial Frobenius handles s(X^k)->s(X).

Therefore the canary's 13 calls

  GenKeySWmatrix(1, k, 0, 0, 625)

create the intended first matrices for those handles.

The durable source now additionally asserts:

  getNextKSWmatrix(k,0).fromKey.getPowerOfX()==k
  getNextKSWmatrix(k,0).ptxtSpace==625.

This closes both direct-hop and exact temporary-plaintext-space selection at runtime.

## 6. debug-decrypt contract is compile/source consistent

Pinned helib/debugging.h declares setupDebugGlobals and cleanupDebugGlobals with the exact context.shareEA() type used by HElib's own tests.

Pinned build system exposes HELIB_DEBUG as a public compile definition when configured with:

  -DHELIB_DEBUG=ON.

The durable canary has a compile-time #error if HELIB_DEBUG is absent.

Pinned SecKey::Decrypt in HELIB_DEBUG mode warns rather than throws when isCorrect() is false, then continues through the actual DCRT/secret-key decryption and intFactor correction.

Therefore the acceptance hierarchy is now unambiguous:

1. isCorrect=false -> diagnostic only;
2. exact decrypted polynomial != independent oracle mod625 -> scientific FAIL;
3. exact equality -> correctness PASS for that state.

## 7. public-API closure

The remaining public interfaces used by the canary were checked against the pinned headers/source:

- ContextBuilder<BGV>.m().p().r().bits().c().build();
- Context::getM/getP/getOrdP/shareEA;
- SecKey::GenSecKey;
- SecKey::Encrypt(Ctxt&,ZZX,ptxtSpace);
- SecKey::GenKeySWmatrix;
- PubKey::setKeySwitchMap;
- PubKey::haveKeySWmatrix;
- PubKey::isReachable;
- PubKey::getNextKSWmatrix;
- KeySwitch::fromKey and ptxtSpace;
- Ctxt::getPtxtSpace/getKeyID/getPrimeSet/isCorrect;
- Ctxt::frobeniusAutomorph;
- Ctxt::cleanUp;
- Ctxt::multByConstant(ZZX);
- SecKey::Decrypt(ZZX&,Ctxt const&).

No further pinned-source signature contradiction was found.

## 8. Frozen durable canary

Current durable source:

  findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt

blob SHA:

  7e991746ceb7aa940c506ca47ff29fd5ef682eb5

source-update commit:

  3dd1c30ba43b69044e0ca69128990c31150cfe91

The source now includes:
- explicit helib/debugging.h;
- HELIB_DEBUG compile requirement;
- source-faithful post-Frobenius cleanUp;
- exact per-node decrypt oracle;
- exact ptxtSpace=625 direct-matrix assertions;
- selected and off-target dirty lifts;
- exact 17-call routing and exact L0..L3.

## Scientific disposition

Primary hypothesis: PASS after one bounded harness repair.

PASS_CANARY_COMPILE_CONTRACT_CLOSURE
PASS_CLEANUP_BASE_PRIMESET_RETURN
PASS_EXPLICIT_625_DIRECT_KS_CONTRACT
PASS_DEBUG_DECRYPT_ORACLE_CONTRACT
NATIVE_EXECUTION=NOT_OBTAINED

The candidate algorithm is neither passed nor failed by this turn.

Crucially, further source-only micro-audits of this recovery canary are now low-information unless a new contradictory source fact appears. The remaining recovery correctness blocker is genuinely execution evidence.

CORRECTNESS_GATE remains BLOCKED.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Run the frozen durable canary once in any compatible pinned-HElib+NTL environment.

Required HElib configuration:
  HELIB_DEBUG=ON.

No timing and no full bootstrap.

Accept only exact per-node decrypt equality, 17 Frobenius calls, exact pruned routing, exact dirty leaves, and exact L0..L3.

If no executable environment is available in the next turn, do not spend another substantive turn on canary-source micro-audits; instead perform independent correctness work on a different unresolved paper-level interface while preserving this execution blocker.
