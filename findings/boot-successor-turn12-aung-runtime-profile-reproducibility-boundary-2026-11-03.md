# BOOT / B158 — Successor Research Turn 12 — Aung runtime-profile reproducibility boundary / Step-3 provenance contract

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE

BACKGROUND_NATIVE_TASK:
    BOOT-T11-R8-SMALL-CANARY-20261103-R2

BACKGROUND_TASK_STATUS:
    PENDING / RESULT UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Read-before-write / authority

GitHub Notes read of the Turn-11 predecessor was attempted first and remained degraded.
The exact durable predecessor was recovered through Git at:

    findings/boot-successor-turn11-raw-l1-source-semantics-canary-contract-repair-2026-11-03.md
    commit ab255eb50098e728cbec0f56d1e4c9633267aab8
    blob f0197c9254b8b1512d3a0ceea78d7d21c0be4b4d.

The target Turn-12 path was checked absent before write.

The pending R2 task was not read, modified, resubmitted, inferred, or duplicated.
No local native task was started.

## Why this side-research is paper-level

If R2 passes, Native evidence Step 3 is exact parameter/interface verification.
That gate can be scientifically valid only if it distinguishes:

1. parameters explicitly recoverable from Aung et al.'s paper; from
2. implementation/runtime fields that the paper does not disclose and that must therefore be serialized from the actual reference context.

Silently filling missing fields with HElib defaults would create a false "paper-exact" baseline and could later invalidate:
- rawModSwitch correctness accounting;
- key-switch noise accounting;
- special-prime sizing;
- concrete security comparison;
- matched benchmark fairness.

This turn asks only whether the publication plus its pinned HElib commit uniquely determines the runtime profile.

## Closest prior / exact delta

Primary source:
- Aung et al., "Bootstrapping with RMFE for Fully Homomorphic Encryption", ePrint 2025/350 / PKC 2025.
- Cached mirror SHA256:
  922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82
- cached source revision:
  87a21bbd5332f5faea99cad54d1a7499b553ddf8
- VERSION_UNVERIFIED relative to any later edition.

Pinned implementation dependency explicitly cited by the paper:
    homenc/HElib commit acdb264
expanded in this research state to:
    acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

No new algorithmic mechanism is proposed in Turn 12.
The delta is a reproducibility/provenance theorem for the already-active candidate and its future matched baseline.

NOVELTY_STATUS remains PREFLIGHT.

## Primary hypothesis

H12:
Aung's publication plus the pinned HElib commit does NOT uniquely specify the exact HElib runtime context needed for a paper-exact reproduction of the p=5,m=32768,w=512,k=5,bits=400 experiment.

The missing fields are correctness/value relevant, so Step 3 must use a two-tier provenance contract:
- PAPER_EXPLICIT;
- NATIVE_SERIALIZED.

Falsifier:
the paper or a discoverable author artifact fixes all runtime-relevant HElib fields, or the omitted fields are provably irrelevant to correctness/noise/value.

## 1. What the primary paper does fix

Aung §6.1 explicitly states:
- Intel Xeon Platinum 8368Q;
- maximum turbo 3.7 GHz;
- 571 GB RAM;
- no multithreading;
- cyclotomic polynomial Phi_32768(X)=X^16384+1;
- varying p;
- HElib initialization with bits=400;
- maximum ciphertext bit-width ranging 538 to 541 bits;
- at least 100-bit estimated security;
- Magma used to generate RMFEs.

Table 2 fixes the target comparison row:
- m=32768;
- p=5;
- w_RMFE=512;
- Corr.(TnM);
- k=5;
- #rec=1;
and reports the published stage capacities/latencies.

Table 3 labels the p=5 row with e=4.

The bibliography explicitly cites:
    HElib, Sep 2022, commit acdb264.

The previously durable parameter audit already correctly separates:
    w_RMFE=512
from HElib secret-key Hamming weight:
    skHwt.

These are PAPER_EXPLICIT fields or published observables.

## 2. What the paper does NOT fix in extracted full text

Bounded full-text searches of the 30-page source found no explicit specification for:
- skHwt / Hamming weight;
- bitsInSpecialPrimes / special-prime budget;
- key-switch digit count c;
- HElib build-cache setting;
- HElib scale;
- HElib stdev;
- exact small/ctxt/special prime sets;
- exact digit partition;
- exact mvec/gens/ords;
- HElib compile flags such as HEXL / HELIB_SP_NBITS override;
- exact NTL/GMP build versions.

The paper gives no source-code or artifact URL for its own implementation in the inspected text.
A bounded GitHub repository/code search by paper title, Aung/RMFE/HElib terms, SlotsToCtxts/CtxtsToSlots identifiers, and prior-FIMD terms found no identifiable author implementation repository.

This is a bounded availability result, not a proof that no private or later artifact exists.

## 3. The pinned HElib commit itself has multiple plausible profiles

Pinned source blobs inspected:

    src/Context.cpp
      f698110d0eba50c249c29c84d27c13444e181408

    include/helib/Context.h
      1723b43108101c2bc25c6ba582decf1236e7d0f0

    src/macro.h
      f4fc77ee258a040ac0b4cfea04fb2e1a739eca2a

    misc/legacy_tests/Test_thinboot.cpp
      b8b2d7a5911ca8806147c4fc27103b4cb612eeea

    tests/GTestThinboot.cpp
      d8f3554f66a85bd8b08623727f641b34d4215267

    benchmarks/bgv_thinboot.cpp
      a8a9c02ce122ffb5f307fd66b8d9c07283762fb2.

### ContextBuilder defaults

Pinned ContextBuilder<BGV> defaults include:

    c=3
    bits=300
    skHwt=0
    resolution=3
    bitsInSpecialPrimes=0
    stdev=3.2
    scale=10
    build_cache=false
    thick=false.

When buildModChain is bootstrappable and skHwt=0, pinned source replaces it with:

    BOOT_DFLT_SK_HWT = MIN_SK_HWT = 120.

Thus a builder-style boot context can have effective skHwt=120.

### Legacy thinboot defaults

Pinned legacy thinboot defaults include:

    c=3
    t/skHwt=64
    nthreads=1
    seed=0
    useCache=1
    special_bits=0
    scale=0  -> leaves Context default scale=10
    c_m=100.

It requires explicit gens/ords/mvec and calls:

    enableBootStrapping(mvec,useCache,false).

Therefore the same HElib commit already supplies at least two plausible thin-bootstrap profiles differing in:
- effective skHwt: 120 vs 64;
- cache: false vs true.

### Other shipped utility defaults

Pinned create-context/key-gen utilities expose another default:

    scale=4.

Therefore "HElib@acdb264" is not a complete runtime profile.

## 4. Missing fields are correctness-relevant

Pinned source defines:

    stdDevForRecryption()
      = 0.5 * sqrt((phi(m)/m) * skHwt * 2^k / 3),

where k is the number of prime factors of m.

For m=32768=2^15:

    phi(m)/m = 1/2
    k=1,

hence:

    stdDevForRecryption()
      = 0.5*sqrt(skHwt/3).

Pinned source then defines:

    boundForRecryption
      = 0.5 + scale*stdDevForRecryption.

Thus skHwt and scale directly affect:
- RecryptData::setAE;
- the rawModSwitch accepted-noise bound.

Pinned Context::addSpecialPrimes also sizes the special modulus using:
- maxDigitLog;
- p^(e-e'+r);
- stdev;
- nDgts/c;
- skHwt;
- p;
- phi(m),
unless an explicit bitsInSpecialPrimes override is supplied.

Therefore c, skHwt, scale, and bitsInSpecialPrimes are not cosmetic metadata.
They can change the actual key-switching/noise interface used by the paper-level claim.

## 5. Paper e=4 is not recoverable from one universal HElib default

Aung Table 3 explicitly labels the p=5 experiment with:

    e=4.

The paper's BGV bootstrapping discussion uses e/e' in the Halevi-Shoup/HElib bootstrapping sense, so e=4 is an important published observable.

Pinned RecryptData::setAE was evaluated exactly under the source formulas.

For m=32768,p=5,r=1,stdev=3.2:

### Builder-default boot profile

    effective skHwt = 120
    scale = 10

gives:

    boundForRecryption
      = 0.5 + 10*0.5*sqrt(120/3)
      = 32.122776601683796

and pinned setAE returns:

    (e,e') = (5,2).

### Legacy-thinboot default profile

    skHwt = 64
    scale = 10

gives:

    boundForRecryption
      = 23.59401076758503

and pinned setAE returns:

    (e,e') = (5,2).

### Shipped scale=4 plus builder boot-default HWT

For:

    skHwt = 120
    scale = 4

the same source gives:

    boundForRecryption
      = 13.149110640673518

and:

    (e,e') = (4,1).

This does NOT prove that Aung used scale=4 or skHwt=120.

It proves the stronger reproducibility point:
different perfectly ordinary entry profiles within the SAME pinned HElib commit induce different bootstrapping exponents, and the paper does not state enough fields to identify which runtime profile generated its e=4 observable.

Accordingly:
- do not call scale=4 an Aung parameter;
- do not call skHwt=64 or 120 an Aung parameter;
- do not silently infer ePrime=1 from the paper.

If a native reference context yields e=4,ePrime=1, that is a NATIVE_SERIALIZED fact for that profile, not a paper-explicit fact about ePrime.

## 6. Ciphertext bit-width cannot uniquely repair the omission

The paper reports maximum ciphertext bit-width 538--541 while requesting bits=400.

It is tempting to reverse-engineer c/special-prime parameters from the extra width.

Pinned HElib makes that unsafe without build provenance.

HELIB_SP_NBITS is compile-time dependent:

    49 with USE_INTEL_HEXL;

otherwise it is:

    NTL_SP_NBITS,

which is supplied by the NTL/platform build.

PrimeGenerator target widths, ctxtPrimeSize, and automatic special-prime sizing use this compile-time value.

Therefore the published 538--541-bit observable is useful as a fingerprint but is not, by itself, a unique inverse map to:
- c;
- skHwt;
- bitsInSpecialPrimes;
- compile flags.

## 7. Two-tier Step-3 provenance contract

If and only if the pending Step-2 R2 canary receives a scientific PASS, Native evidence Step 3 must use the following contract.

### Tier A — PAPER_EXPLICIT / primary-source constraints

At minimum record and assert:

    HElib source commit = acdb264...
    m = 32768
    p = 5
    application r = 1 for the current BGV target
    bits_HElib = 400
    w_RMFE = 512
    k = 5
    workflow = Corr.(TnM)
    paper e observable = 4
    single-thread execution

and record as published consistency fingerprints:

    maximum ciphertext bit-width = 538..541
    Table-2 initial capacity ~=391.1
    Table-2 stage capacities/latencies

without treating those floating observables as exact correctness contracts.

### Tier B — NATIVE_SERIALIZED / reference-profile facts

Serialize verbatim from the actual context/harness:

    c / nDigits
    effective skHwt / hwt_param
    scale
    stdev
    resolution
    bitsInSpecialPrimes input
    exact smallPrimes
    exact ctxtPrimes
    exact specialPrimes
    exact prime products
    exact digit partition D_i
    e_param / ePrime_param
    rcData.e / rcData.ePrime
    mvec
    gens
    ords
    build_cache
    alsoThick
    HELIB_SP_NBITS
    USE_INTEL_HEXL / relevant compile flags
    NTL version/build/platform
    GMP version
    exact key-switch matrix inventory
    each required matrix plaintext space
    direct-reachability strategy.

No Tier-B value may be labelled "paper-exact" unless an author artifact or explicit primary-source statement is later recovered.

## 8. Step-3 acceptance semantics

Step 3 must NOT ask:

    "Does our native context match every unpublished Aung setting?"

That predicate is untestable from the currently available publication.

The valid predicate is:

1. every Tier-A source-published field matches;
2. every Tier-B field is fully serialized and internally source-consistent;
3. the candidate and matched split-thin baseline use the SAME Tier-B profile;
4. paper observables are compared as fingerprints and any mismatch is reported;
5. any benchmark later claims only:
       matched source-faithful reference-profile comparison
   unless author runtime artifacts are recovered.

If rcData.e !=4 under the chosen reference profile, Step 3 must mark:

    PAPER_PROFILE_FINGERPRINT_MISMATCH

and investigate before baseline/candidate benchmarking.

If rcData.e=4 but ePrime is not source-published, record the realized ePrime without claiming author identity.

## 9. Consequence for current static results

This turn does NOT invalidate the active sparse-R8 mechanism.

Existing Turn-7/8 mathematics should be read with its explicit parameter assumptions.

In particular:
- bits_HElib=400 is primary-source bound;
- w_RMFE=512,k=5,m=32768,p=5 are primary-source bound;
- any use of an exact ePrime or exact special-prime/key-switch inventory is a reference-profile assumption until native Step 3 serializes it.

The pending R2 task already has a fixed execution contract and remains untouched.
Its result, whatever it is, must be audited on its own terms.

If R2 returns a context-parameter assertion failure, this Turn-12 finding provides the correct classification boundary:
first distinguish a reference-profile mismatch from an algebraic candidate failure.

## Verdict

FAIL_UNIQUE_PAPER_EXACT_RUNTIME_PROFILE.

PASS_AUNG_PRIMARY_SOURCE_BITS400_M32768_P5_W512_K5_BINDING.
PASS_PINNED_HELIB_MULTIPLE_RUNTIME_PROFILE_WITNESS.
PASS_UNDER_SPECIFIED_FIELDS_ARE_CORRECTNESS_RELEVANT.
PASS_DEFAULT_PROFILE_E_OBSERVABLE_NONUNIQUENESS.
PASS_TWO_TIER_STEP3_PARAMETER_PROVENANCE_CONTRACT.

NATIVE_STEP2_RESULT = UNKNOWN / PENDING.
CORRECTNESS_GATE = BLOCKED.
BASELINE_CORRECTNESS = PENDING.
SECURITY_GATE = PENDING.
VALUE_GATE = PENDING.
AUDIT_GATE = PENDING.
NOVELTY_STATUS = PREFLIGHT.
PAPER_READINESS = NOT_READY.

## Next action while R2 is pending

Do not execute another native task.

If BOOT-T11-R8-SMALL-CANARY-20261103-R2 becomes ready, its raw artifacts preempt the next free substantive turn for independent audit.

Otherwise continue one independent BOOT paper-level side-research unit that does not depend on R2.

After R2 scientific PASS, Step 3 must implement the two-tier provenance contract above before any baseline correctness or performance work.
