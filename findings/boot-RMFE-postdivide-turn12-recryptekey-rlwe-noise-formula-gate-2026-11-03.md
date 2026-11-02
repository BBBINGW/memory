# BOOT / B158 — Research Turn 12/25 — recryptEkey RLWE noise-formula gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read remains degraded for repository findings. Durable authority was recovered from
BBBINGW/memory at verified HEAD:

    ceae292be7175ebf8bc4765b0503724013ceb836

Immediate relevant findings:
- Turn8 exact-L1 shared-reconstruction capacity floor:
  findings/boot-RMFE-postdivide-turn8-exact-l1-guard-capacity-floor-gate-2026-11-02.md
- Turn10 recryptEkey plaintext-bound soundness:
  findings/boot-RMFE-postdivide-turn10-recryptekey-plaintext-bound-soundness-gate-2026-11-03.md
- Turn11 HElib capacity/isCorrect margin:
  findings/boot-RMFE-postdivide-turn11-capacity-api-iscorrect-margin-gate-2026-11-03.md

The target path was checked absent before write.

No native execution occurred.

## Why this turn matters

Turns8-11 rely numerically on the recryptEkey source-level bound:

    N_E
      <= 625*3.2*sqrt(16384*ln(16384))
         + noiseBoundForMod(625,16384)
      = 1,028,414.4400229623.

A hidden extra term inside SecKey::skEncrypt's RLWE generation would invalidate:
- the 354.9156-bit shared-reconstruction capacity floor;
- the 353.8567-bit isCorrect margin;
- the current local correctness contract.

The main risk is that constructing an RLWE ciphertext under secret key s might incur an additional
secret-key multiplication/noise term beyond p*e.

## Closest implementation prior / exact delta

Relevant prior is pinned HElib's own RLWE helper used by secret-key encryption.

No novelty claim is added.

Exact delta:
audit the algebra and returned bound of:

    RLWE(c0,c1,s,p)
      -> RLWE1(c0,c1,s,p)

for the exact recryptEkey call:

    p = 625.

## Primary hypothesis

Pinned RLWE constructs c0,c1 so that the decryption polynomial satisfies exactly:

    c0 + s*c1 = p*e

for one bounded Gaussian error polynomial e.

Therefore:
- the random c1 term and secret-key product cancel algebraically in decryption;
- there is no second Gaussian term;
- there is no secret-key-norm multiplier in the returned error bound;
- for the current power-of-two ring, RLWE returns exactly:

      p * stdev * sqrt(phi(m)*ln(phi(m)))

  after rejection-bounded sampling.

Consequently Turn8's RLWE contribution:

    797,474.332347112

is source-exact and contains no omitted term.

## Falsifier

FAIL if pinned source shows any of:
1. RLWE samples more than one independent error term;
2. decryption leaves a residual c1*s contribution;
3. returned bound multiplies by a secret-key norm;
4. non-power-of-two stdev scaling is also applied at m=32768;
5. sampleGaussianBounded is only heuristic and may return a sample above its reported bound;
6. or skEncrypt transforms the RLWE return value before storing it in noiseBound.

## Minimal decisive test

Audit only:
- src/keys.cpp::RLWE1;
- src/keys.cpp::RLWE;
- src/sample.cpp::sampleGaussianBounded;
- src/sample.cpp::sampleGaussianBoundedEffectiveBound;
- SecKey::skEncrypt assignment.

No benchmark or native run is required.

## 1. RLWE decryption identity is exact

Pinned RLWE first randomizes c1, then calls RLWE1.

RLWE1:
1. samples a bounded Gaussian error into c0;
2. if p>1, multiplies both c0 and the returned bound by p;
3. computes tmp=c1*s;
4. sets:

       c0 <- c0 - tmp.

Thus the final stored pair is:

    c0 = p*e - c1*s
    c1 = random.

Decrypting relative to secret s gives:

    c0 + s*c1
      = p*e - c1*s + s*c1
      = p*e.

The ring is commutative, so the two product terms cancel exactly.

Therefore neither:
- the size of c1;
- nor the canonical norm of s;
- nor a product bound ||c1||*||s||

appears in the actual decryption error.

## 2. Returned RLWE bound tracks exactly p*e

Pinned RLWE1 records:

    bound = c0.sampleGaussianBounded(stdev)

before c0 is multiplied by p.

Then for p>1:

    c0 *= p;
    bound *= p.

After subtracting c1*s it returns this same bound.

Because subtraction only creates the ciphertext representation while decryption cancels that
product, the returned quantity is exactly a bound for the canonical embedding of:

    p*e.

No hidden adjustment is performed after subtraction.

Pinned function comments agree with this semantics:
RLWE1 returns a bound on the canonical embedding of the decryption of (c0,c1) relative to s.

## 3. Current power-of-two ring uses unmodified stdev=3.2

RLWE1 reads:

    stdev = context.getStdev().

It only applies:

    stdev *= sqrt(m)

when:

    palg.getPow2() == 0.

Current:

    m=32768=2^15

has:

    getPow2()!=0.

Therefore:

    stdev = 3.2

exactly.

The non-power-of-two sqrt(m) multiplier is unreachable.

## 4. sampleGaussianBounded enforces the reported bound

For a power-of-two ring, sampleGaussianBoundedEffectiveBound returns:

    sqrt(phi(m)*ln(phi(m))).

sampleGaussianBounded therefore sets:

    B_e
      = stdev*sqrt(phi(m)*ln(phi(m))).

It repeatedly samples an error polynomial and measures:

    embeddingLargestCoeff(e)

until:

    embeddingLargestCoeff(e) <= B_e.

If the retry budget is exhausted without success, it throws instead of returning an out-of-bound
sample.

Thus on successful RLWE generation:

    ||e||_emb
      <= 3.2*sqrt(16384*ln(16384)).

This is enforced by rejection, not merely a high-probability metadata estimate for the returned
sample.

## 5. Exact current RLWE contribution

Multiplying by the recrypt plaintext space:

    p_boot = 625

gives:

    N_RLWE
      <= 625*3.2*sqrt(16384*ln(16384))
      = 797,474.332347112.

This reproduces Turn8 exactly.

There is no:
- skHwt;
- skBound;
- c1 norm;
- c1*s norm;
- second error polynomial

in this term.

## 6. skEncrypt stores this return value directly

Pinned SecKey::skEncrypt performs:

    ctxt.noiseBound = RLWE(...,ptxtSpace);

with:

    ptxtSpace = 625.

Only afterward it adds the plaintext allowance audited in Turn10.

Therefore:

    N_E
      = N_RLWE + N_ptxt_bound

with no intermediate multiplier or additive error term.

Using Turn10:

    N_ptxt_bound
      = 230,940.1076758503.

Hence:

    N_E
      <= 797,474.332347112
         + 230,940.1076758503
      = 1,028,414.4400229623.

The Turn8 value is source-exact under the pinned default stdev/scale and current successful bounded
sampling path.

## 7. Consequence for Turns8-11

The shared-reconstruction worst-case bound remains:

    N_shared
      <= N_E*S1 + |f|*S0

with:

    S0,S1 <= 25,640,960
    |f| <= 312.

Therefore the already-derived:

    log2(N_shared)
      <= 44.58437490144962

and:

    capacity_shared
      >= 354.9156250985504 bits

require no correction.

Combined with Turn11:

    isCorrect threshold
      = 1.0588936890535685 bits,

the local correctness margin remains:

    >=353.85673140949683 bits.

## 8. Important scope boundary

This result is specific to secret-key RLWE encryption of recryptEkey.

It does NOT provide a generic bound for:
- public-key encryption noise;
- key-switch added noise;
- automorphism/relinearization noise;
- pure inverse;
- 17-call recovery;
- Algorithm4;
- final DFR.

In particular, the exact algebraic cancellation c1*s is an encryption-construction identity and
must not be reused to bound later key-switch operations.

## 9. Native Step3 refinement

After mandatory Step2 PASS, Step3 should optionally record the generated recryptEkey:

    recryptEkey.getNoiseBound()

and independently recompute the static source ceiling:

    N_E_static
      = 625*3.2*sqrt(16384*ln(16384))
        + noiseBoundForMod(625,16384).

Acceptance requires:

    recryptEkey.getNoiseBound() <= N_E_static

up to ordinary floating evaluation tolerance.

Together with Turn10 it should also verify ptxt_ratio<=1.

A larger native recryptEkey noiseBound under the exact pinned context indicates:
- altered stdev/scale;
- different source version;
- or a different encryption path.

## Verdict

PASS_RECRYPTEKEY_RLWE_SINGLE_ERROR_IDENTITY
PASS_SECRET_PRODUCT_EXACT_CANCELLATION
PASS_NO_SECRETKEY_NORM_TERM_IN_RLWE_BOUND
PASS_TURN8_RECRYPTEKEY_NOISE_FORMULA_EXACT
PASS_TURN8_TURN11_CAPACITY_MARGIN_UNCHANGED

N_RLWE_MAX:
  797474.332347112

N_E_MAX:
  1028414.4400229623

SHARED_CAPACITY_FLOOR:
  354.9156250985504 bits

SHARED_ISCORRECT_MARGIN:
  353.85673140949683 bits

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

The mandatory evidence-order blocker remains Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 should include the Turns8-12 recryptEkey static ceiling and local
capacity/isCorrect assertions before proceeding to baseline and complete candidate native
correctness.
