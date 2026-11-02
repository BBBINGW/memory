# BOOT Research Turn 16/25 — pure EvalMap inverse / scalar-unit normalization realization gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

The current construction needs, after the one shared reconstruction, a pure inverse of the
full evaluation map in the POWER BASIS, followed by normalization by

  8192^{-1} = 28 mod 625,

before the 17-call target-pruned split tree.

Hypothesis:
pinned HElib can realize this boundary source-faithfully using its public API, without stock
normal-basis conversion and without requiring a custom-scaled EvalMap implementation:

  EvalMap(*rcData.ea, minimal=false, rcData.mvec,
          invert=true, build_cache=rcData.build_cache,
          normal_basis=false)
  -> apply(ctxt)
  -> ctxt.multByConstant(28L).

The scalar-unit normalization should be semantically exact, preserve ptxtSpace/key/primeSet,
and add zero direct tracked noise.

Falsifier:
- normal_basis=false is not a true inverse-power-basis mode;
- inverse construction is only valid mod p rather than mod p^4;
- the public scalar 28 path multiplies ciphertext parts/noise by 28;
- EvalMap itself changes the common BGV intFactor unpredictably;
- or a custom internal inverse is still required.

## Closest existing mechanism and exact delta

Pinned stock thick RecryptData constructs:

  firstMap = EvalMap(*ea, minimal, mvec,
                     invert=true, build_cache);

where normal_basis defaults to true.

Therefore the candidate's pure inverse is NOT a new transform family. Its exact source delta from
stock firstMap is:

  same EncryptedArray *rcData.ea
  same mvec
  same inverse direction
  same public MatMul infrastructure
  BUT normal_basis=false.

The subsequent scalar normalization by 28 is an ordinary public BGV scalar operation.

No novelty claim is made from this implementation component.

## 1. normal_basis=false is exactly the pure inverse mode

Pinned include/helib/EvalMap.h documents:
- invert=false: coefficients packed in slots -> polynomial / powerful representation;
- invert=true: inverse transformation;
- normal_basis=true additionally folds a normal-basis transformation into the inverse;
- normal_basis is explicitly optional and may be disabled.

Pinned src/EvalMap.cpp makes the distinction exact.

Step1Matrix first constructs the full evaluation matrix A.

When invert=true it computes:

  A2 = A^{-1}

using ppInvert.

Only AFTER this inversion does it execute:

  if (normal_basis)
      A[i][j] = A[i][j] * CB;

where CB is the normal-basis matrix.

Therefore:

  invert=true, normal_basis=false

is literally the same inverse evaluation matrix with the final normal-basis multiplication
omitted.

There is no hidden alternative basis transform.

## 2. The inverse is exact over Z_625, not merely over F_5

EvalMap's Step1 and Step2 inverse constructors read:

  p = ea.getAlMod().getZMStar().getP();
  r = ea.getAlMod().getR();

and call:

  ppInvert(..., p, r).

For the current temporary recryption EncryptedArray:

  rcData.ea->getAlMod().getR()
    = e-ePrime+r_app
    = 4-1+1
    = 4.

Hence the matrix inversion is performed over the prime-power plaintext algebra modulo

  5^4 = 625.

This is the exact coefficient ring required by the dirty-Z625 recovery theorem.

## 3. Pinned HElib independently tests the same pure inverse mode

tests/GTestEvalMap.cpp constructs:

  EvalMap map(... invert=false, normal_basis=false)
  EvalMap imap(... invert=true,  normal_basis=false)

on a random full plaintext polynomial.

It:
1. converts the random polynomial into powerful-basis coefficients;
2. packs those coefficients into slots;
3. applies the forward map and checks exact decrypted polynomial equality;
4. re-encrypts that polynomial;
5. applies the inverse map with normal_basis=false;
6. decrypts slots and checks equality with the original packed coefficients.

Thus the pinned test itself treats normal_basis=false as an exact forward/inverse round trip on
arbitrary full polynomial states, not merely scalar thin states.

The current candidate consumes exactly this full-domain inverse behavior, because its shared
reconstruction contains arbitrary 5-divisible dirty extension-ring state.

## 4. The pure inverse is constructible even in thin-bootstrap contexts

ThinRecryptData::init first calls RecryptData::init.

RecryptData::init creates, before its optional thick-only early return:

  rcData.mvec
  rcData.alMod
  rcData.ea
  rcData.p2dConv.

Only stock firstMap/secondMap creation is skipped when alsoThick=false.

Therefore even if the baseline uses thin bootstrapping and has no prebuilt thick firstMap, the
candidate can publicly construct:

  EvalMap(*rcData.ea,
          false,
          rcData.mvec,
          true,
          rcData.build_cache,
          false).

No private RecryptData field and no new HElib core hook is needed for THIS inverse stage.

The separate branch-local preprocessing/reconstruction extraction may still require the previously
identified narrow internal hook; Turn 16 does not change that boundary.

## 5. EvalMap preserves the common input intFactor

The shared reconstruction begins from recryptEkey with common intFactor=1.

Pinned EvalMap::apply is a sequence of MatMul1DExec / BlockMatMul1DExec linear maps.

Pinned matmul.cpp realizes these maps using:
- smart automorphisms;
- cleanUp;
- multiplication by encoded PUBLIC polynomial constants;
- ciphertext addition of transformed copies.

ConstMultiplier calls the polynomial/DoubleCRT multByConstant overloads. Those operations do not
change BGV intFactor.

Automorphism and real-modswitch cleanup preserve intFactor, and every transformed copy originates
from the same factor-1 input. Therefore additions do not need factor harmonization.

Hence the output of the pure inverse still has:

  intFactor = 1.

No ciphertext-ciphertext multiplication occurs inside EvalMap.

## 6. Turn-10 normalization implementation assumption was unnecessarily strong

Turn 10 rejected a separate post-inverse multiplication by 28 because the ZZX/public-polynomial
multByConstant overload would multiply tracked noiseBound by the canonical size of the constant.

That statement is correct for the ZZX overload, but it is NOT the only HElib API for a scalar.

Pinned Ctxt::multByConstant(long/ZZ) has a special BGV scalar implementation.

For scalar c, write:

  c0 = c mod ptxtSpace,
  d  = gcd(c0,ptxtSpace),
  c1 = c0/d.

It updates:

  intFactor <- intFactor * c1^{-1} mod ptxtSpace,

and physically multiplies ciphertext parts/noise only by d.

For the current normalization:

  c=28,
  ptxtSpace=625,
  gcd(28,625)=1.

Therefore:

  d=1,
  28^{-1}=67 mod625,

and the function RETURNS after setting:

  intFactor <- 67

without multiplying any ciphertext part and without changing noiseBound.

Thus:

  ctxt.multByConstant(28L)

is an exact semantic multiplication of the plaintext by 28 with ZERO direct tracked-noise
increase.

It also leaves:
- ptxtSpace=625;
- primeSet unchanged;
- keyID unchanged.

## 7. Canonical production normalization is revised

The previous canonical requirement

  custom/folded normalized inverse constants
  [[14,48],[14,-48]]

is no longer required for production correctness or for avoiding a direct x28 noise penalty.

The simpler public-API path is now canonical:

  shared reconstruction
  -> pure EvalMap inverse
       invert=true
       normal_basis=false
  -> BGV scalar-unit multByConstant(28L)
  -> target-pruned recovery tree.

The algebraic folded matrix remains a valid equivalent custom implementation, but it is OPTIONAL,
not required.

This refinement removes one unnecessary custom linear-transform implementation burden.

## 8. Consequence: Algorithm-4 initial intFactor is 67, not 1

After the pure inverse:

  intFactor = 1.

After scalar-unit normalization:

  intFactor = 28^{-1} = 67 mod625.

The recovery tree preserves that common factor because:
- Frobenius/relinearization preserves it;
- cleanUp's active real-modswitch path preserves it;
- even/odd additions subtract same-factor states;
- public monomial multiplication does not change it.

All five selected leaves therefore have common factor 67.

The aligned L0,L1,L2,L3 are public-polynomial linear combinations of these same-factor leaves, so
they also enter Algorithm 4 with:

  intFactor(L0)=...=intFactor(L3)=67.

Therefore Turn 15's specific statement

  PASS_CURRENT_ALGORITHM4_INITIAL_INTFACTOR_ONE

is SUPERSEDED.

The following Turn-15 results remain valid:
- arbitrary dirty Z625 lifts are inside Aung Algorithm-4's theorem domain;
- factor harmonization preserves semantic plaintext;
- divideByP implements the semantic quotient;
- the six 625/125/25 plaintext-space boundaries are correctly typed;
- saved application intFactor is restored only after final Recode.

A non-one initial factor does not break these semantic results because 67 is a unit modulo every
successive power of 5.

It DOES mean that Algorithm-4 factor/noise capacity trajectories remain runtime-state dependent
and must be measured; no factor-neutral capacity claim is made.

## 9. Revised recovery canary

The durable recovery-only canary has been updated to match the production normalization boundary.

It now:
1. encrypts the UNNORMALIZED synthetic post-inverse plaintext at ptxtSpace=625;
2. checks exact decryption;
3. records noiseBound;
4. calls root.multByConstant(28L);
5. asserts noiseBound is unchanged and ptxtSpace/keyID/primeSet are unchanged;
6. checks the normalized semantic plaintext exactly;
7. runs the same 17-call recovery and exact L0..L3 oracle.

New required output includes:

  scalar_unit_28=PASS.

Current durable source:

  findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt

blob SHA:

  6ae4bc7e48e0390f8dec97429f4ddb89565928c0

source-update commit:

  5af025bcbcce3cca1b1d7938183c343c521c65db.

## Verdict

PASS_PURE_EVALMAP_INVERSE_PUBLIC_API
PASS_NORMAL_BASIS_FALSE_POWER_BASIS_SEMANTICS
PASS_Z625_PRIME_POWER_INVERSE
PASS_BGV_SCALAR_UNIT_28_ZERO_DIRECT_NOISE
REFINE_PRODUCTION_NORMALIZATION_TO_SCALAR_UNIT_PATH
SUPERSEDE_ALGORITHM4_INITIAL_INTFACTOR_1_WITH_67

NATIVE_EXECUTION=NOT_OBTAINED

This turn closes the source/API realizability of the previously implicit pure-inverse boundary and
removes an unnecessary custom normalized-inverse requirement.

It does NOT prove the actual inverse/recovery ciphertext path natively and does not close
capacity/noise.

CORRECTNESS_GATE remains BLOCKED.
BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Run the revised frozen recovery-only canary against pinned HElib with HELIB_DEBUG=ON.

Acceptance now additionally requires:

  scalar_unit_28=PASS

before the 17-call tree.

After the small canary passes, exact parameter/interface verification should instantiate the real:

  EvalMap(*rcData.ea,false,rcData.mvec,true,rcData.build_cache,false)

on a reconstructed temporary-625 ciphertext and verify:
- inverse output semantics;
- ptxtSpace/keyID/primeSet;
- factor-1 state before normalization;
- semantic x28 and factor-67 state after scalar normalization;
- then the exact recovery routing.

No performance interpretation is authorized before the native correctness prerequisites pass.
