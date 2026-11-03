# BOOT / B158 — Successor Research Turn 11 — raw-L1 source semantics / small-canary contract repair

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE

SUPERSEDES UNEXECUTED TASK CONTRACT:
    BOOT-T10-R8-SMALL-CANARY-20261103-R1

AUTHORIZED REPAIRED NATIVE TASK:
    BOOT-T11-R8-SMALL-CANARY-20261103-R2

TASK STATUS AT END OF TURN:
    READY_TO_EXECUTE / NOT_EXECUTED

## Read-before-write / authority

GitHub Notes read of the Turn-10 predecessor was attempted first and returned an empty body.

Direct exact-ref Git authority shows current BBBINGW/memory main remains exactly:

    a584bdfd74a5d18e2b1fba28e67b753d6ce50df7

with no commit after the Turn-10 execution-contract finding.
Repository search found no:
- BOOT-T10-R8-SMALL-CANARY-20261103-R1 result;
- PASS_SMALL_CORRECTNESS_CANARY;
- FAIL_SMALL_CORRECTNESS_CANARY;
- INFRA_BLOCKED;
- canary source/result JSON.

Thus the Turn-10 task was authorized but no scientific execution artifact exists.

Immediate predecessor:

    findings/boot-successor-turn10-native-step2-small-canary-execution-contract-2026-11-03.md
    commit a584bdfd74a5d18e2b1fba28e67b753d6ce50df7
    blob 9b289925b14c8c9eccc7c8e7dbad866fd65c7ae2.

Pinned HElib source:

    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Exact pinned source blobs used in this audit:

    src/keys.cpp        7d3a2dfd3706704edfbddacd556ea44615e959a1
    src/debugging.cpp   c361fd62fd9aee86ef275f25a61ab1c4bf16a0f3
    src/DoubleCRT.cpp   e356d6d731af7df74f6c6d99629edf5f4804d5f9
    src/Ctxt.cpp        b346fcd52ddf6bd5c778a918865cc6bb5143787f.

The target Turn-11 finding path was checked absent before write.

## Why this turn is correctness-critical

Turn 10 froze a native small-canary contract that asks for:
- Turn-8 theorem raw ratio;
- an independently measured actual coefficient-L1 raw ratio;
- HElib's tracked rawModSwitch ratio.

The contract called the first two quantities "actual error" quantities.

That wording is dangerous in HElib BGV:
a natural implementation would subtract the semantic plaintext representative from the raw decryption
polynomial and take the L1 norm of only the residual RLWE error.

That quantity is NOT the quantity propagated by the Turn-8 recurrence and is NOT the quantity HElib
tracks in its BGV noiseBound.

This turn audits only that source-semantic issue.

No candidate algebra is redesigned.
No evidence-order step is skipped.
No native PASS is asserted.

## Closest implementation prior / exact delta

Closest implementation mechanism is the pinned HElib BGV ciphertext/noise invariant and rawModSwitch gate.

No prior-art or novelty status changes.

The candidate-specific delta in this turn is only the native acceptance semantics for Turn-8's
coefficient-L1 sufficient theorem.

NOVELTY_STATUS remains PREFLIGHT.

## Primary hypothesis

H11:
Turn-8's E_in and the native pre-raw L1 consistency check should be instantiated from the centered
RAW decryption polynomial itself, including the plaintext representative, rather than from a
"plaintext-subtracted pure RLWE error".

Falsifier:
- pinned HElib BGV noiseBound excludes the plaintext representative;
- pinned debugging removes plaintext before comparing actual and estimated noise;
- rawModSwitch's source gate is based on a plaintext-subtracted quantity;
- or Turn-8's recurrence separately accounts for the plaintext term.

## 1. Fresh BGV source explicitly includes plaintext in noiseBound

Pinned PubKey::Encrypt for BGV first samples the zero-encryption/random error terms and then forms:

    ptxt_fixed
      = balanced_MulMod(ptxt, Q mod ptxtSpace, ptxtSpace)

and adds ptxt_fixed into ciphertext part 0.

The same source then computes a plaintext magnitude bound:

    ptxt_bound = context.noiseBoundForMod(ptxtSpace, phi(m))

and executes:

    ctxt.noiseBound += ptxt_bound.

Finally:

    ctxt.ptxtSpace = ptxtSpace
    ctxt.intFactor = 1.

Therefore HElib's BGV noiseBound is deliberately a bound on the TOTAL raw decryption magnitude,
not only on the sampled RLWE residual.

This source behavior is essential for correctness because reduction modulo Q can alter the later
mod-p value if the total decryption representative wraps.

## 2. HElib debugging confirms the same "total raw decryption" convention

Pinned SecKey::Decrypt(..., f) computes the secret-key inner product as a DoubleCRT and calls:

    ptxt.toPoly(plaintxt)

with the default:

    positive = false.

Pinned DoubleCRT::toPoly reconstructs every coefficient in the symmetric interval:

    [-Q/2, Q/2).

Before any mod-p reduction, SecKey::Decrypt stores:

    f = plaintxt.

Pinned debugging then defines:

    embeddingLargestCoeff(const Ctxt& ctxt, const SecKey& sk)

by:

    sk.Decrypt(p, ctxt, pp)
    return embeddingLargestCoeff(pp, context.getZMStar()).

It does NOT subtract the semantic plaintext representative.

realToEstimatedNoise and log2_realToEstimatedNoise compare exactly this raw pp magnitude against:

    ctxt.totalNoiseBound(),

which for BGV is:

    noiseBound.

Thus the library's own "real versus estimated noise" diagnostic uses the total centered raw
decryption polynomial including plaintext.

## 3. rawModSwitch source gate also uses the total tracked noiseBound

Pinned Ctxt::rawModSwitch computes:

    ratio = q / Q_current

and returns:

    scaledNoise = noiseBound * ratio.

Pinned recryption.cpp then multiplies by:

    mfac = context.getZMStar().getNormBnd()

and accepts only if:

    scaledNoise * mfac
      <= HELIB_MIN_CAP_FRAC * p^r * boundForRecryption.

For the current power-of-two m=32768 case, durable source audit already established:

    mfac = 1.

No plaintext subtraction occurs anywhere in this gate.

## 4. Turn-8 recurrence is consistent only with the same total raw quantity

Turn 8 defines:

    E_theta <= ||theta_i||_1 * E_in

and then propagates the result through:
- Frobenius automorphisms;
- key switching;
- branch additions;
- five-way merge;
- mod-down;
- recrypt-key switching.

There is no separate term for transformed plaintext magnitude.

Therefore the mathematically consistent interpretation is:

    E_in
      = coefficient-L1 envelope of the centered total raw decryption polynomial
        <sk,c> mod Q_0,

not the coefficient-L1 norm of a semantic-plaintext-subtracted residual.

This repairs terminology, not the Turn-8 inequality.

The existing numeric threshold is unchanged:

    C_in = log2(Q_0 / E_in)

with sufficient conditions:

    C_in > 34.8749813477 bits   (universal source floor)

or:

    C_in > 30.7982811616 bits   (fixed e,e' source inference).

The +log2(5)=2.3219280949-bit merge penalty is unchanged.

## 5. Exact native extraction for R2

For any canary ciphertext c with current prime product Q:

1. call:
       sk.Decrypt(decoded, c, raw);

2. because DoubleCRT::toPoly defaults to positive=false, raw is already coefficientwise centered
   modulo Q;

3. define:
       E_raw_L1(c) = sum_j |raw_j|.

DO NOT:
- subtract decoded plaintext;
- reconstruct balanced_MulMod(decoded, Q*intFactor mod p, p);
- divide by p;
- remove the plaintext representative.

The input theorem measurement is:

    E_in_native = E_raw_L1(input)

    C_in_native
      = log2(Q_0 / E_in_native).

R2 requires:

    C_in_native > 34.8749813477 bits

for the universal Turn-8 sufficient precondition.

The stronger 30.798... threshold may be recorded, but the universal threshold remains the hard
scientific acceptance criterion so the canary does not depend on an implementation-specific
interpretation of the fixed-(e,e') inference.

## 6. Exact pre-raw measured L1 sufficient ratio

Immediately before rawModSwitch, after:

    modDownToSet
    -> reLinearize(recryptKeyID),

let:
- Q_pre = product of the CURRENT primeSet;
- raw_pre = centered raw decryption polynomial from SecKey::Decrypt(..., raw_pre);
- E_pre_native = ||raw_pre||_1;
- q=626;
- raw_bound=(2/3)*5*boundForRecryption.

Define:

    actual_l1_raw_ratio
      =
      (q / Q_pre)
      * E_pre_native
      * mfac
      / raw_bound.

Here:

    mfac=1.

Because coefficient-L1 upper-bounds every canonical evaluation magnitude and, in this power-of-two
case, the source powerful-basis conversion factor is one, this is a valid independent SUFFICIENT
sample check.

R2 records this value and requires:

    actual_l1_raw_ratio < 1.

This check is not substituted for HElib's tracked gate.

## 7. HElib tracked raw ratio remains independently mandatory

R2 must separately call:

    rawModSwitch(zzParts,626)

and record:

    tracked_raw_ratio
      =
      rawModSwitch_return * mfac
      /
      ((2/3)*5*boundForRecryption).

Require:

    tracked_raw_ratio <= 1.

The two checks answer different questions:

- actual_l1_raw_ratio:
    estimator-independent sufficient check on THIS deterministic sample;

- tracked_raw_ratio:
    exact source runtime gate that HElib itself will enforce.

Both must pass.

## 8. Turn-8 theorem ratio in R2

R2 shall evaluate the Turn-8 deterministic theorem using:

    E_in_native = ||raw_input||_1

and the exact instantiated Q_0 and Q_3:

    theorem_raw_ratio
      =
      [
        A_merge*(E_in_native/Q_0)
        +5F_tau/Q_0
        +(R_5+K_5)/Q_3
      ]
      / beta_raw,

where:

    A_merge = 5*2^24
    F_tau = 511*K_625 +255*R_5
    K_625 <=401679183790908.6
    K_5 <=3213433470327.2688
    R_5 <=671129600
    beta_raw=((2/3)*5*boundForRecryption)/626.

Require:

    theorem_raw_ratio < 1.

Again, E_in_native is the total centered raw-decryption L1 magnitude.

## 9. Result classification repair

Turn-10 R1 is superseded BEFORE execution only because its "actual error" wording permits a
source-inconsistent plaintext-subtracted implementation.

No R1 scientific result exists and no previous conclusion is invalidated.

The repaired task is:

    BOOT-T11-R8-SMALL-CANARY-20261103-R2.

All Turn-10 assertions remain unchanged EXCEPT the exact definitions above.

R2 still stops before DigitExtract and still does not benchmark.

### R2 PASS criterion

PASS_SMALL_CORRECTNESS_CANARY iff the same deterministic run satisfies:

    context parameter assertions
    Method-1 5/5 scalar-slot correctness
    sparse R8 support
    sparse ten coefficients 10/10
    C_in_native >34.8749813477 bits
    theorem_raw_ratio <1
    actual_l1_raw_ratio <1
    HElib tracked_raw_ratio <=1
    reconstruction low digits 10/10
    all eight D_j invariants
    exact D_j aggregate hash
    RM10 state assertions
    fused-recode state assertions
    final intFactor=67
    final exact Z625 recovery oracle.

Scientific assertion failure:
    FAIL_SMALL_CORRECTNESS_CANARY.

Dependency/build/runner failure:
    INFRA_BLOCKED.

## 10. Infrastructure disposition

This Chat again attempted to obtain a native execution route.

Observed:
- BBBINGW/memory main has no result artifacts after Turn 10;
- GitHub integration cannot create an execution branch:
      403 Resource not accessible by integration;
- local shell has g++14.2, CMake3.31.6 and GMP6.3 development files;
- NTL is absent;
- apt repository DNS fails;
- controlled binary archive retrieval did not successfully materialize HElib/NTL sources.

These are infrastructure facts only.

They are not candidate correctness evidence.

## Verdict

FAIL_AMBIGUOUS_PLAINTEXT_SUBTRACTED_ERROR_NOTION_FOR_R1_CONTRACT.
PASS_TOTAL_RAW_DECRYPTION_L1_SOURCE_SEMANTICS.
PASS_TURN8_EIN_NATIVE_DEFINITION.
PASS_PRE_RAW_ACTUAL_L1_RATIO_DEFINITION.
PASS_R2_SMALL_CANARY_ACCEPTANCE_REPAIR.

NATIVE_SMALL_CANARY = NOT_EXECUTED.
NATIVE_EVIDENCE_STEP_2 = PENDING.
CORRECTNESS_GATE = BLOCKED.
BASELINE_CORRECTNESS = PENDING.
NOVELTY_STATUS = PREFLIGHT.
PAPER_READINESS = NOT_READY.

The candidate itself remains ACTIVE and unchanged.

## Next decisive test

Execute:

    BOOT-T11-R8-SMALL-CANARY-20261103-R2

using the Turn-10 full execution contract plus this Turn-11 raw-L1 semantic repair.

Do not execute the superseded R1 contract.

After execution:
- independently audit all raw artifacts;
- if scientific PASS, open evidence Step 3 exact parameter/interface verification;
- if scientific FAIL, stop at the first failed stage;
- if INFRA_BLOCKED, keep Step 2 pending.

Do not run DigitExtract.
Do not run Algorithm4.
Do not benchmark.
