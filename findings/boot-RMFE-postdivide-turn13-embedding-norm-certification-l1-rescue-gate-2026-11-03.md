# BOOT / B158 — Research Turn 13/25 — embedding-norm certification / coefficient-L1 rescue gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes reads remain degraded and return empty objects. Durable context was recovered by direct
GitHub fetch from BBBINGW/memory main at:

    29ed57051e83fabec9675454299a314d840b7c27

Immediate prerequisites:
- Turn8 exact-L1 shared-reconstruction capacity floor;
- Turn10 recryptEkey plaintext-bound audit;
- Turn11 capacity/isCorrect API audit;
- Turn12 exact RLWE algebra/noise-formula audit.

The target finding path was absent before write.

## Native Step2 attempt — infrastructure only

Turn13 first tried to execute the frozen recovery-only canary without modifying its source.

Frozen canary Git blob remains:

    6ae4bc7e48e0390f8dec97429f4ddb89565928c0.

A new materialization route was tested:
- current container has cmake/g++/GMP but no NTL/HElib;
- ordinary git access to github.com fails DNS;
- the dedicated download path was tested for the pinned HElib archive and NTL source;
- GitHub codeload could not be made viewable to the download tool;
- NTL binary/source URL was visible through the official download page, but materialization still failed.

Therefore:

    RECOVERY_CANARY = NOT_EXECUTED.

These are infrastructure facts, not scientific failure evidence.

## Why this turn is necessary

Turns10-12 used sampleGaussianBounded/sampleHWtBounded rejection sampling and described their
returned canonical-embedding bounds as deterministic bounds on the actual generated polynomials.

That wording is only justified if the rejection oracle:

    embeddingLargestCoeff(...)

is itself a certified upper-bound computation.

If it is an ordinary floating FFT norm estimate, then:
- HElib's tracked noise formulas remain valid as HElib bookkeeping;
- but the stronger phrase "deterministic actual canonical-norm bound" is not established;
- and the Turn10-12 local correctness theorem needs either downgrade or an independent rigorous
  replacement bound.

## Closest implementation prior / exact delta

The relevant prior is pinned HElib's own norm and noise machinery.

No novelty claim is added.

Exact delta:
1. classify embeddingLargestCoeff as certified or non-certified;
2. if non-certified, test whether the current recryptEkey/shared reconstruction still admits a
   deterministic coefficient-L1 correctness envelope that preserves a large positive margin.

## Primary hypothesis

The candidate's local shared-reconstruction correctness claim survives a certification audit without
trusting HElib's floating FFT norm oracle.

More precisely:
- embeddingLargestCoeff need not be treated as certified;
- the actual integer structure of the pinned samplers gives a direct coefficient-L1 upper bound on
  the recryptEkey decryption polynomial;
- combining this with Turns5-7 exact-L1 Z0/Z1 bounds still leaves a very large Q/noise correctness
  margin.

## Falsifier

FAIL the local deterministic correctness rescue if:
1. embeddingLargestCoeff is non-certified, AND
2. no source-level coefficient bound can upper-bound the generated recryptEkey decryption polynomial,
   OR
3. the resulting deterministic shared-reconstruction bound reaches/exceeds 0.48Q under bits=400.

## Minimal decisive test

Audit only:
- src/norms.cpp embeddingLargestCoeff path for m=32768;
- HElib's own documentation on noise-bound semantics;
- src/sample.cpp coefficient generation/truncation;
- src/sample.cpp sampleHWt coefficient structure;
- the exact RLWE identity from Turn12;
- Turns5-7 exact-L1 Z0/Z1 bounds.

Then recompute the local shared-reconstruction correctness margin without using an FFT-estimated
canonical norm.

## 1. embeddingLargestCoeff is not a certified upper-bound oracle

For m=32768, embeddingLargestCoeff selects the quarter-FFT implementation.

Pinned src/norms.cpp computes it with:
- std::complex<double>;
- precomputed double roots/twiddle factors;
- floating FFT;
- ordinary std::norm;
- ordinary sqrt.

The function does not use:
- interval arithmetic;
- directed outward rounding;
- a posteriori FFT error bounds;
- nextafter inflation;
- exact algebraic evaluation.

For large ZZX inputs it additionally scales coefficients into double before the same floating
transform.

Therefore the source supports:

    embeddingLargestCoeff = numerical canonical-norm computation

but does NOT establish:

    returned_value >= exact canonical norm

as a machine-certified theorem.

## 2. HElib explicitly classifies its noise model as heuristic/high-probability

Pinned CHANGES.md says the library keeps a "high-probability bound" and "tries to provide at least a
heuristic guarantee of no decryption errors".

Context.h repeatedly labels several fresh-noise bounds "a bit heuristic" and describes scale=10 as a
high-probability normal-tail heuristic.

Therefore Turns10-12 overstated the evidence when they called the FFT-rejection result a
"deterministic actual canonical-norm bound".

Durable refinement:

    HElib tracked/rejection noise model = HIGH-PROBABILITY / HEURISTIC-SOURCE MODEL

not a formal certified norm proof.

This does NOT invalidate the exact algebraic RLWE identity from Turn12.

## 3. The Gaussian sampler gives an independent coefficient bound

For the current power-of-two ring:

    phi(m)=16384
    stdev=3.2.

Pinned sampleGaussian generates each real coefficient as:

    stdev * rr * cos(theta)
or
    stdev * rr * sin(theta),

with:

    rr <= HELIB_GAUSS_TRUNC = 8.

It then rounds each value to an integer.

Hence under the ordinary real-function semantics used by the implementation:

    |e_i| <= round(3.2*8) <= 26.

There are exactly phi(m)=16384 coefficient positions in the power-of-two branch.

Therefore independently of embeddingLargestCoeff and independently of whether the rejection test
numerically underestimates:

    ||e||_1 <= 16384*26
            = 425,984.

For every primitive root zeta with |zeta|=1:

    |e(zeta)| <= ||e||_1.

Thus coefficient L1 gives a direct canonical-embedding upper bound.

## 4. Deterministic RLWE error envelope

Turn12 proved exactly:

    c0 + s*c1 = 625*e.

Therefore:

    ||625e||_emb
      <= 625*||e||_1
      <= 625*425,984
      = 266,240,000.

This bound does not use:
- embeddingLargestCoeff;
- Gaussian-tail assumptions;
- skHwt;
- a secret-key norm.

It is deliberately much looser than HElib's tracked:

    797,474.33...

but is structurally deterministic at the integer-polynomial level.

## 5. Deterministic boot-secret plaintext envelope

Pinned sampleHWt produces a polynomial with coefficients in {-1,0,1} and at most phi(m) nonzero
positions; if a requested Hwt is at least the ring length, the implementation clamps it to n-1.

Hence without knowing Aung's exact skHwt:

    ||keyPoly||_1 <= 16384.

Pinned balanced_MulMod at modulus625 maps every nonzero key coefficient to a balanced scalar with:

    |a| <= 312.

Therefore:

    ||ptxt_fixed||_1
      <= 312*16384
      = 5,111,808.

Again:

    ||ptxt_fixed||_emb <= ||ptxt_fixed||_1.

This removes matched skHwt<=16384 as a prerequisite for the coarse deterministic local envelope.
The actual matched skHwt still must be recorded for reproducibility.

## 6. Deterministic recryptEkey total-decryption envelope

The secret-key encryption decryption polynomial is:

    625e + ptxt_fixed.

Therefore:

    N_E_det
      <= 266,240,000 + 5,111,808
      = 271,351,808.

This is NOT the value stored in HElib noiseBound.

The two ledgers must now be distinguished:

    HElib tracked/high-probability N_E:
      <= 1,028,414.4400229623

    independent coefficient-L1 deterministic envelope:
      <= 271,351,808.

Turn12's formula remains exact for HElib's stored/tracked ledger, but the stronger claim that the
stored value is a certified upper bound on actual canonical norm is superseded.

## 7. Deterministic shared-reconstruction envelope

Turns5-7 establish exact public-polynomial bounds:

    S0,S1 <= 25,640,960

and at the addConstant boundary:

    |f| <= 312.

Using the independent deterministic envelope:

    N_shared_det
      <= N_E_det*S1 + |f|*S0
      <= 271,351,808*25,640,960
         + 312*25,640,960
      = 6,957,728,854,835,200.

Hence:

    log2(N_shared_det)
      <= 52.62753788102554.

Turn8/9 source binding gives:

    log2(Q) >= 399.5

for bits_HElib=400.

Therefore the independent modulus-to-total-decryption ratio satisfies:

    log2(Q/N_shared_det)
      >= 399.5 - 52.62753788102554
      = 346.87246211897445 bits.

This is separate from Ctxt::capacity(), whose stored-metadata floor remains >=354.9156 bits.

## 8. Deterministic correctness margin

Turn11 established for m=32768:

    polyNormBnd = 1

and the HElib correctness boundary:

    total_decryption_bound <= 0.48 Q,

equivalently ratio bits at least:

    log2(1/0.48)
      = 1.0588936890535685.

The coefficient-L1 envelope therefore leaves:

    346.87246211897445
      - 1.0588936890535685
      = 345.8135684299209 bits

above the same decryption-correctness threshold.

Thus even after discarding HElib's FFT norm oracle as a certified proof tool, the local shared
reconstruction remains enormously inside the correctness region.

## 9. Required terminology correction

Supersede the following earlier wording:

    "Turn8/10 N_E <= 1,028,414 is a deterministic actual canonical-norm bound."

Replace it with:

1. HElib tracked/high-probability ledger:
       N_E_tracked <= 1,028,414.4401
       shared.capacity() >=354.9156
   under the pinned HElib estimator semantics;

2. independent coefficient-L1 local correctness envelope:
       N_E_det <=271,351,808
       log2(Q/N_shared_det) >=346.8725
       deterministic-style isCorrect margin >=345.8136 bits.

The exact-L1 public Z0/Z1 guard from Turns5-7 remains fully deterministic and unchanged.

## 10. Consequence for skHwt

Aung's exact skHwt remains UNKNOWN and must still be printed in native provenance.

However the coarse coefficient-L1 local correctness proof does not require an assumption:

    skHwt <=16384

because sampleHWt itself cannot return more than the available ring positions.

Thus Turn10's skHwt condition remains useful for reproducing HElib's tighter heuristic ptxt-bound
story, but is no longer a prerequisite for the independent local correctness rescue.

## 11. Scope boundary

This repair is LOCAL to the shared reconstruction.

It does not certify downstream:
- EvalMap key-switch noise;
- 17-call recovery noise;
- Algorithm4 noise/division trajectory;
- final DFR.

Those stages still need native evidence and later noise/security analysis.

The coefficient-L1 rescue also does not make HElib's general noise estimator formally certified.

## Verdict

FAIL_CERTIFIED_EMBEDDINGLARGESTCOEFF_ORACLE
REFINE_TURNS10_12_DETERMINISTIC_WORDING
PASS_COEFFICIENT_L1_RECRYPTEKEY_RESCUE
PASS_DETERMINISTIC_LOCAL_SHARED_CORRECTNESS_MARGIN

HELIB_TRACKED_N_E_MAX:
  1028414.4400229623

COEFFICIENT_L1_N_E_MAX:
  271351808

HELIB_TRACKED_SHARED_CAPACITY_FLOOR:
  354.9156250985504 bits

INDEPENDENT_L1_Q_OVER_TOTAL_BITS_FLOOR:
  346.87246211897445 bits

INDEPENDENT_L1_CORRECTNESS_MARGIN:
  345.8135684299209 bits

AUNG_SKHWT:
  UNKNOWN / STILL RECORD NATIVELY

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

## Next decisive test

Mandatory evidence order remains Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 should record BOTH ledgers:
- HElib tracked noise/capacity;
- independent coefficient-L1 local correctness envelope.

Do not report HElib's floating FFT noise estimator as a certified mathematical upper bound.
