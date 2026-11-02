# BOOT / B158 — Research Turn 10/25 — recryptEkey plaintext-bound soundness gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., IACR ePrint 2025/350 / PKC 2025

## Read-before-write / provenance

GitHub Notes read remains degraded for repository findings. Current durable authority was recovered
from BBBINGW/memory at verified HEAD:

    fe803e1aefecf76002763bed435bd30c2d54216b

Immediate relevant findings:
- Turn8 exact-L1 guard reconstruction-capacity floor:
  findings/boot-RMFE-postdivide-turn8-exact-l1-guard-capacity-floor-gate-2026-11-02.md
  blob 8d9d0ea97adabebe80e4bc0b3e7f93b1477c6d98
- Turn9 Aung bits=400 / w_RMFE=512 parameter binding:
  findings/boot-RMFE-postdivide-turn9-aung-bits400-w512-parameter-binding-gate-2026-11-03.md
  blob 93b2cab9536d71e63fb2757ca42018af2bce48ae

The target path was checked absent before write.

No native execution occurred.

## Why this turn matters

Turn8 used pinned SecKey::skEncrypt source to compute:

    recryptEkey.noiseBound
      = RLWE_bound + noiseBoundForMod(625,phi(m)),

then derived the local shared-reconstruction capacity floor:

    >= 354.9156 bits

under bits_HElib=400.

However pinned skEncrypt also computes the ACTUAL plaintext contribution:

    ptxt_sz = embeddingLargestCoeff(ptxt_fixed)

and only emits a Warning when:

    ptxt_sz > ptxt_bound.

It still adds only ptxt_bound to noiseBound.

Therefore Turn8 is automatically a stored-metadata statement, but it is an actual sound
noise-bound statement only if the bootstrapping secret-key plaintext encrypted inside recryptEkey
satisfies:

    ptxt_sz <= ptxt_bound.

This turn audits exactly that edge.

## Closest prior implementation / exact delta

The implementation prior is unchanged stock HElib recryptEkey generation:

    sample boot secret keyPoly
    -> Encrypt(recryptEkey,keyPoly,p2ePr)
    -> skEncrypt
    -> balanced_MulMod(keyPoly,QmodP,625)
    -> add plaintext to c0.

No novelty claim is added.

The exact delta is a soundness audit of the Turn8 local-capacity theorem.

## Primary hypothesis

For the fixed power-of-two instance:

    m=32768
    phi(m)=16384
    p_boot=625,

if the HElib recryption secret-key Hamming-weight parameter satisfies:

    skHwt <= phi(m)=16384,

then the source-generated keyPoly and its balanced ptxt_fixed representation satisfy:

    embeddingLargestCoeff(ptxt_fixed)
      <= noiseBoundForMod(625,16384).

Hence skEncrypt's "noise bound exceeded in encryption" warning is unreachable for recryptEkey,
and Turn8's stored recryptEkey noiseBound is a genuine deterministic upper bound on the actual
canonical-embedding decryption polynomial at that boundary.

The default bootstrappable HElib skHwt=120 is inside this regime.

Aung's paper, however, does not report skHwt, so source-faithful application of this strengthened
claim requires Step3/native provenance to print the actual matched skHwt.

## Falsifier

FAIL the strengthened sound-noise interpretation if:
1. ptxt_fixed is not a scalar-balanced image of keyPoly coefficientwise;
2. sampleHWtBounded does not enforce the claimed embedding bound;
3. the ptxt_bound formula is smaller than the maximum allowed boot-secret plaintext norm for a
   matched skHwt;
4. Aung/native matched configuration uses an skHwt outside the proven admissible range;
5. or skEncrypt updates noiseBound differently from Turn8's ledger.

The stored-metadata Turn8 floor itself only fails if item 5 is false.

## Minimal decisive test

Audit pinned source:
- RecryptData::init skHwt provenance;
- genRecryptData keyPoly sampling;
- sampleHWtBounded rejection guarantee;
- balanced_MulMod on {-1,0,1} key coefficients;
- skEncrypt plaintext warning and bookkeeping rule.

Then compare the exact deterministic bounds numerically.

## 1. Bootstrapping secret-key provenance

Pinned RecryptData::init sets:

    skHwt = context.getHwt().

Pinned genRecryptData then executes:

    long hwt = context.getRcData().skHwt;
    sampleHWtBounded(keyPoly,context,hwt);

and encrypts:

    Encrypt(recryptEkey,keyPoly,p2ePr).

Thus the plaintext inside recryptEkey is exactly the bounded-Hamming-weight recryption secret
key polynomial keyPoly.

It is not a generic arbitrary Z625 plaintext.

## 2. sampleHWtBounded gives an enforced canonical bound

For m a power of two, sampleHWt samples keyPoly directly with degree<phi(m) and coefficients:

    {-1,0,1}.

sampleHWtBounded sets:

    B_key = sqrt(skHwt * ln(phi(m)))

and repeatedly samples until:

    embeddingLargestCoeff(keyPoly) <= B_key.

If no sample satisfies this within the hard retry budget, the function throws instead of returning
an out-of-bound key.

Therefore, conditioned on successful recryption-key generation:

    ||keyPoly||_emb <= sqrt(skHwt * ln(16384)).

This is an enforced source bound, not merely an expectation.

## 3. balanced_MulMod preserves scalar structure for odd 625

skEncrypt computes:

    QmodP = productOfPrimes(ctxtPrimes) mod 625

and:

    ptxt_fixed = balanced_MulMod(keyPoly,QmodP,625).

Let:

    a = balRem(QmodP,625).

Because 625 is odd:

    |a| <= 312.

Every nonzero coefficient of keyPoly is exactly +1 or -1.
The pinned balanced_MulMod loop therefore maps it coefficientwise to:

    +a or -a

with no even-modulus randomized tie case.

Hence over the integers:

    ptxt_fixed = a * keyPoly

coefficientwise.

Therefore:

    ||ptxt_fixed||_emb
      = |a| * ||keyPoly||_emb
      <= 312 * sqrt(skHwt * ln(16384)).

## 4. Compare with skEncrypt ptxt_bound

Pinned skEncrypt uses:

    ptxt_bound
      = context.noiseBoundForMod(625,16384).

For odd modulus625 and default context scale=10:

    ptxt_bound
      = 10 * sqrt(16384 * 625^2 / 12)
      = 230,940.1076758503.

If:

    skHwt <= 16384,

then:

    ||ptxt_fixed||_emb
      <= 312 * sqrt(16384 * ln(16384))
      = 124,405.99584614947.

Therefore:

    ||ptxt_fixed||_emb / ptxt_bound
      <= 0.538693763929334
      < 1.

So throughout the entire semantically natural Hamming-weight regime up to the ring dimension:

    ptxt_sz <= ptxt_bound

with more than a factor-1.85 safety margin.

In particular HElib's bootstrappable default:

    BOOT_DFLT_SK_HWT = 120

is far inside this region.

## 5. Exact threshold even beyond phi(m)

Solving:

    312*sqrt(h*ln(16384))
      <=
    10*625*sqrt(16384/12)

gives:

    h <= 56,459.372...

Thus the source bookkeeping remains sound even for any requested:

    skHwt <= 56,459.

However HElib's power-of-two key polynomial itself has only phi(m)=16384 coefficients, so
skHwt values beyond the ring dimension are semantically abnormal and should not be used as the
paper contract.

The clean production assertion is therefore:

    0 < skHwt <= 16384.

## 6. Consequence for the warning branch

Pinned skEncrypt computes actual:

    ptxt_sz = embeddingLargestCoeff(ptxt_fixed)

and warns iff:

    ptxt_sz > ptxt_bound.

Under:

    skHwt <= 16384

and successful sampleHWtBounded generation, the inequality above proves this condition impossible.

Therefore:

    PASS_RECRYPTEKEY_PTXT_WARNING_UNREACHABLE

for the stated parameter regime.

This resolves the concern that Turn8's recryptEkey noiseBound might hide a larger actual
boot-secret plaintext contribution while merely warning.

## 7. Turn8 is strengthened, but only conditionally on matched skHwt provenance

The RLWE component uses sampleGaussianBounded and is likewise rejection-bounded before return.

The plaintext component is now proven below the value that skEncrypt adds to noiseBound.

Therefore for any matched context satisfying:

    skHwt <= 16384,

the Turn8 recryptEkey ledger:

    N_E <= 1,028,414.4400229623

is not merely a stored metadata number; it is a valid deterministic canonical-embedding upper
bound assembled from:
- bounded RLWE error;
- bounded actual plaintext contribution.

Because Turns5-7 supply valid explicit canonical-norm bounds for Z1 and Z0, the downstream shared
reconstruction bound:

    N_shared
      <= N_E*S1 + |f|*S0

is correspondingly sound at that local boundary.

Thus the Turn8:

    capacity_shared >=354.9156 bits

can be interpreted as a sound HElib local noise-ledger capacity floor, not just a metadata floor,
provided the matched skHwt assertion holds.

## 8. Aung artifact boundary

The acquired Aung ePrint mirror:
- confirms bits=400;
- confirms HElib commit acdb264;
- defines w as RMFE dimension;
- contains no extracted-text match for "skHwt" or "Hamming weight".

No public Aung implementation repository was identified in the bounded search.

Therefore:

    AUNG_SKHWT = UNKNOWN

must remain the durable paper-artifact state.

It is not scientifically valid to write:

    Aung skHwt = 120

merely because 120 is HElib's default.

The correct statement is:
- HElib default bootstrappable skHwt is 120;
- the strengthened Turn8 theorem holds for every skHwt<=16384 anyway;
- Step3 must print the actual matched context.getHwt()/rcData.skHwt.

## 9. Native Step3 refinement

After mandatory Step2 PASS, Step3 must now additionally assert:

    skHwt_context = context.getHwt()
    skHwt_recrypt = rcData.skHwt
    skHwt_context == skHwt_recrypt
    0 < skHwt_recrypt <= 16384.

It should record:

    actual embeddingLargestCoeff(ptxt_fixed)
    ptxt_bound = noiseBoundForMod(625,16384)
    ptxt_ratio = ptxt_sz / ptxt_bound

during recryptEkey generation or an exact diagnostic reconstruction.

Acceptance requires:

    ptxt_ratio <= 1.

The source theorem predicts a stronger universal ceiling:

    ptxt_ratio <= 0.538694

for skHwt<=16384.

Any larger matched native ratio indicates:
- non-source-faithful key generation;
- parameter mismatch;
- or an implementation/source-version mismatch.

## Verdict

PASS_RECRYPTEKEY_PTXT_BOUND_FOR_SKHWT_LE_PHIM
PASS_BALANCED_MULMOD_SCALAR_KEYPOLY_STRUCTURE
PASS_SKENCRYPT_WARNING_UNREACHABLE_FOR_SKHWT_LE_16384
PASS_TURN8_LOCAL_NOISE_FLOOR_SOUNDNESS_CONDITIONAL_ON_SKHWT_ASSERTION

AUNG_SKHWT:
  UNKNOWN

HELIB_DEFAULT_BOOT_SKHWT:
  120

PRODUCTION_REQUIRED_ASSERTION:
  0 < skHwt <= 16384

TURN8_CAPACITY_FLOOR_354P9:
  PRESERVED
  UPGRADED FROM METADATA-ONLY TO SOUND LOCAL NOISE-LEDGER FLOOR
  CONDITIONAL ON MATCHED skHwt ASSERTION

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

## Scope boundary

This turn does NOT establish:
- Aung's exact unpublished/local skHwt choice;
- Step2 native recovery correctness;
- Step3 native parameter/interface correctness;
- downstream inverse/recovery/Algorithm4 noise;
- final capacity;
- DFR;
- matched benchmark value.

## Next decisive test

Mandatory evidence order remains blocked at Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 must include the skHwt/ptxt_ratio assertions above before accepting the
Turn8 local capacity floor as a native correctness invariant.
