# BOOT / B158 — Research Turn 11/25 — HElib capacity API / isCorrect margin gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read remains degraded for repository findings. Current durable authority was recovered
from BBBINGW/memory at verified HEAD:

    0c40dc31c4bb98df02bc12a9a99e3c7330ce48e3

Immediate relevant findings:
- Turn8 exact-L1 reconstruction-capacity floor:
  findings/boot-RMFE-postdivide-turn8-exact-l1-guard-capacity-floor-gate-2026-11-02.md
- Turn10 recryptEkey plaintext-bound soundness:
  findings/boot-RMFE-postdivide-turn10-recryptekey-plaintext-bound-soundness-gate-2026-11-03.md

Target path was absent before write.

No native execution occurred.

## Why this turn matters

Turn8/10 derived the local shared-reconstruction floor:

    capacity_shared >= 354.915625 bits.

That result assumed HElib's BGV capacity is exactly:

    log2(Q / noiseBound).

A hidden factor in Ctxt::capacity(), totalNoiseBound(), or correctness testing could invalidate either:
- the numerical 354.9-bit statement;
- or the interpretation that this is ample local correctness margin.

This turn audits that API boundary exactly.

## Closest implementation prior / exact delta

The relevant implementation prior is stock HElib Ctxt bookkeeping.

No novelty claim is added.

Exact delta:
verify the exact source semantics of:
- totalNoiseBound();
- capacity();
- bitCapacity();
- isCorrect();
- PAlgebra::getPolyNormBnd()

for the fixed BGV power-of-two instance.

## Primary hypothesis

For BGV with m=32768=2^15:

1. Ctxt::totalNoiseBound() equals noiseBound exactly;
2. Ctxt::capacity() is exactly log2(Q/max(noiseBound,1));
3. Ctxt::bitCapacity() only truncates capacity() to long;
4. intFactor, ptxtSpace, skHwt, secret-key bound, and plaintext magnitude do not appear in capacity();
5. PAlgebra::polyNormBnd=1 for m a power of two;
6. therefore Ctxt::isCorrect() reduces to:

       noiseBound <= 0.48 Q,

   equivalently:

       capacity >= log2(1/0.48) = 1.058893689... bits.

Consequently the Turn8/10 floor 354.915625 bits implies an isCorrect safety margin of at least
353.856731 bits at the shared-reconstruction boundary.

## Falsifier

FAIL if any pinned-source fact shows:
- BGV totalNoiseBound includes another state variable;
- capacity includes a hidden multiplicative or additive factor;
- bitCapacity applies a nontrivial offset;
- m=32768 has polyNormBnd != 1;
- isCorrect uses a secret-key bound or plaintext-space dependent term;
- or Turn8's formula is inconsistent with the actual API.

## Minimal decisive test

Audit only the pinned implementations of:
- Ctxt::totalNoiseBound;
- Ctxt::capacity / bitCapacity;
- Ctxt::isCorrect;
- calcPolyNormBnd / PAlgebra construction.

No native execution or benchmark is needed.

## 1. BGV totalNoiseBound is exactly noiseBound

Pinned Ctxt.h:

    totalNoiseBound():
      if CKKS:
        ptxtMag*ratFactor + noiseBound
      else:
        noiseBound.

The current candidate is BGV.

Therefore:

    totalNoiseBound = noiseBound.

Neither ptxtMag nor ratFactor enters the BGV capacity ledger.

## 2. Ctxt::capacity is exactly the Turn8 formula

Pinned Ctxt::capacity():

    return
      (logOfPrimeSet()
       - log(max(totalNoiseBound(),1)))
      / log(2).

For BGV:

    capacity
      = log2(Q)
        - log2(max(noiseBound,1))
      = log2(Q/max(noiseBound,1)).

There is no additional:
- skHwt factor;
- getSKeyBound factor;
- ptxtSpace factor;
- intFactor factor;
- security slack;
- polyNormBnd factor.

Thus Turn8's numerical capacity definition is source-exact.

## 3. bitCapacity only truncates

Pinned:

    long bitCapacity() const
    {
      return long(capacity());
    }

So the floating capacity floor:

    354.915625...

implies:

    bitCapacity >= 354

provided the same source-derived bounds hold.

No hidden "bits per level" conversion occurs here.

## 4. isCorrect is a different, stricter predicate

Pinned Ctxt::isCorrect() computes:

    xQ = product(primeSet)

then chooses:

    bnd = getPolyNormBnd()

for the current power-of-two m, because the powerful-basis branch is only used when m is not a
power of two.

It returns:

    totalNoiseBound()*bnd <= 0.48*xQ.

So capacity itself contains no correctness factor, but decryption correctness has a separate
basis-conversion/safety condition.

This distinction must be explicit:
- capacity is a modulus/noise ratio metric;
- isCorrect is the HElib decryption-safety predicate.

## 5. polyNormBnd is exactly 1 for m=32768

Pinned PAlgebra constructor sets:

    polyNormBnd = calcPolyNormBnd(m).

calcPolyNormBnd first repeatedly divides m by 2.

For:

    m=32768=2^15,

this leaves:

    m=1.

The function then returns:

    1.

Therefore:

    getPolyNormBnd() = 1

exactly for the current ring.

No numerical approximation or asymptotic estimate is needed.

## 6. Exact isCorrect threshold in capacity bits

For the current BGV power-of-two ring:

    isCorrect
      iff noiseBound <= 0.48 Q.

Equivalently, for noiseBound>=1:

    Q/noiseBound >= 1/0.48

and hence:

    capacity >= log2(1/0.48).

Numerically:

    log2(1/0.48)
      = 1.0588936890535685 bits.

So a ciphertext can have positive capacity but still fail isCorrect if capacity is between 0 and
about 1.059 bits.

This corrects any informal use of "positive capacity implies correctness".

## 7. Apply to the Turn8/10 shared reconstruction floor

Turns8-10, under their stated conditions, establish:

    capacity_shared
      >= 354.9156250985504 bits.

Subtracting the exact HElib isCorrect threshold:

    correctness_margin_bits
      >= 354.9156250985504
         - 1.0588936890535685
      = 353.85673140949683 bits.

Therefore:

    shared reconstruction isCorrect() == true

is mathematically guaranteed under the full Turn8-10 assumptions, with at least:

    353.8567 bits

of HElib capacity margin above the source correctness threshold.

This is a local statement immediately after the guarded shared reconstruction.

## 8. Consequence for the construction contract

The Turn8 local floor may now be stated precisely as both:

1. exact HElib capacity lower bound:
       capacity_shared >= 354.9156;

2. actual HElib local correctness guarantee:
       isCorrect(shared) = true,

   with:
       margin >=353.8567 bits

   above the current power-of-two correctness threshold.

This upgrade relies on Turn10's condition:

    0 < matched skHwt <= 16384

so that the recryptEkey noise ledger is sound rather than metadata-only.

## 9. What remains unresolved

This does not prove final candidate correctness.

Later operations may consume capacity and add path-dependent key-switch noise:
- pure EvalMap inverse;
- 17 recovery Frobenius calls;
- L0..L3 correction maps;
- Algorithm4;
- final Recode.

Historical work already showed later key-switch noise cannot be derived from scalar capacity alone.

Therefore no downstream or final capacity extrapolation is allowed.

## 10. Native Step3 refinement

After mandatory Step2 PASS, Step3 should print and assert:

    shared.capacity()
    shared.bitCapacity()
    shared.isCorrect()
    context.getZMStar().getPolyNormBnd()

Acceptance for the exact matched context:

    polyNormBnd == 1
    shared.capacity() >= 354.9
    shared.bitCapacity() >= 354
    shared.isCorrect() == true.

It should also record:

    isCorrect_threshold_bits
      = log2(polyNormBnd/0.48)
      = 1.058893689...

for this ring.

Any native contradiction under the same exact source/parameter assumptions indicates an
implementation or bookkeeping mismatch.

## Verdict

PASS_HELIB_CAPACITY_FORMULA_EXACT
PASS_BGV_TOTALNOISEBOUND_EQUALS_NOISEBOUND
PASS_POWER2_POLYNORMBND_ONE
PASS_SHARED_RECONSTRUCTION_ISCORRECT_MARGIN_353P86

TURN8_CAPACITY_FLOOR:
  PRESERVED EXACTLY

TURN10_SOUNDNESS_CONDITION:
  0 < matched skHwt <= 16384

LOCAL_SHARED_ISCORRECT:
  PROVEN UNDER TURNS5-10 ASSUMPTIONS

RECOVERY_CANARY:
  NOT_EXECUTED

NATIVE_EXECUTION:
  NOT_OBTAINED

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

## Next decisive test

Mandatory evidence order remains blocked at Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 must include the Turn11 capacity/bitCapacity/isCorrect/polyNormBnd assertions
before proceeding to baseline and candidate native correctness.
