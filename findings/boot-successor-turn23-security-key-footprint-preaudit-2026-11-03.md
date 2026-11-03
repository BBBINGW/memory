# BOOT / B158 — Turn 23 — security and evaluation-key footprint pre-audit

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes read-before-write was attempted first and remains degraded.
Exact Turn-22 durable finding:
    findings/boot-successor-turn22-independent-style-fixed-ring-prior-art-stress-test-2026-11-03.md
    commit 161f5ce54efaec5df8b45b5d2adc65f1b64a9ea3
    blob 94ab146271fc9f68194b2fc92cefb078095fed37.

The target Turn-23 path was checked absent before write.
The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Pinned HElib:
    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Primary source:
Aung et al., ePrint 2025/350, cached mirror
SHA256 922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
VERSION_UNVERIFIED.

This turn is a SECURITY / KEY-FOOTPRINT pre-audit only.
It does not claim final concrete-security bits or exact paper-author key inventory.

## Primary hypothesis

H23:
The active unguarded p=5 candidate does not introduce a new RLWE secret/ring/assumption family relative to source-faithful HElib bootstrapping. Under the standard pinned HElib bootstrapping key-generation profile, all candidate automorphism targets are already contained in the baseline full Frobenius key family. Any incremental key material can only arise under a deliberately minimized baseline keyset and must be measured from the serialized runtime inventory.

Falsifier:
- candidate requires a new secret-key ID;
- candidate requires automorphism keys outside the outer-ring Frobenius subgroup;
- candidate requires a new subring/field-switching secret;
- candidate requires another recryption key / circular-encryption edge;
- or candidate automorphism targets are absent from standard HElib bootstrapping evaluation keys.

## 1. What stock HElib bootstrapping already publishes

Pinned standard thin/fat bootstrapping harnesses generate:

    SecKey::GenSecKey()
    addSome1DMatrices(secretKey)
    addFrbMatrices(secretKey)
    secretKey.genRecryptData().

Pinned addFrbMatrices is maximal:
    addSomeFrbMatrices(...,LONG_MAX)
    -> add1Dmats4dim(...,-1)
    -> for j=1,...,ord_p-1:
           GenKeySWmatrix(1,p^j mod m,key0,key0).

For active:
    m=32768
    p=5
    ord_m(5)=8192.

Therefore standard addFrbMatrices generates:

    8191 direct Frobenius matrices

of form:

    W[s_0(X^(5^j)) -> s_0(X)],
    j=1,...,8191.

In a bootstrappable BGV context, omitted ptxtSpace in GenKeySWmatrix defaults to the larger bootstrapping plaintext space.

Pinned addSome1DMatrices separately generates the regular slot-rotation dimension matrices used by ordinary EvalMap/ThinEvalMap operations.

Pinned genRecryptData generates:
- one additional bootstrapping secret key key1;
- one key-switch matrix from key0 to key1 at application plaintext space p^r;
- one recryptEkey encrypting key1 under key0 at the recryption plaintext space.

This is the baseline two-key bootstrapping cycle.

## 2. Candidate needs no new secret key

Candidate steps:
- Method-1 projections;
- sparse/fixed-ring carrier construction;
- one stock MultKey raw reconstruction;
- RM10;
- shared correction-map Frobenius bank;
- Algorithm 4;
- final source Recode.

Only the stock MultKey step uses:

    reLinearize(recryptKeyID=key1).

After recryptEkey reconstruction the ciphertext is again under key0.

RM10 and all shared recovery automorphisms are:
    key0 -> key0.

Algorithm-4 ciphertext multiplication uses ordinary relinearization under key0.
Pinned GenSecKey defaults to maxDegKswitch=3 and therefore already generates:
    s0^2 -> s0
    s0^3 -> s0
matrices.

Final Method-1 Recode also uses key0 Frobenius automorphisms.

Therefore candidate requires:

    secret key IDs = {key0,key1}

exactly as baseline.

No:
- key2;
- subring secret;
- field-switched secret;
- lower-dimensional RLWE secret;
- new ring modulus/dimension.

## 3. Candidate direct Frobenius target set

For a direct-matrix implementation, the active candidate uses three Frobenius-target families.

### A. Method-1 projection / final Recode

Recursive trace exponents:

    J_method =
      {1,2,4,8,16,32,64,128,256}

meaning automorphisms:
    X -> X^(5^j).

Count:
    9.

### B. Shared four-output recovery bank

    J_recovery={1,2,3,4,5,6,7}.

Count:
    7.

Overlap with J_method:
    {1,2,4}.

### C. RM10 coefficient clearing

The ten Turn-10/13 automorphism multipliers are:

    {16385,8193,4097,2049,1025,513,257,129,65,33}.

Exact discrete logs in the p=5 Frobenius subgroup are:

    16385 =5^4096 mod32768
    8193  =5^6144
    4097  =5^7168
    2049  =5^7680
    1025  =5^7936
    513   =5^3968
    257   =5^6080
    129   =5^5088
    65    =5^2032
    33    =5^888.

Thus:

    J_RM10 =
      {888,2032,3968,4096,5088,6080,6144,7168,7680,7936}.

Count:
    10.

All are inside:
    <5> subset Z_32768^*.

No regular-slot automorphism dimension is introduced by RM10.

### Union

Direct candidate Frobenius exponent set:

    J_candidate =
    {1,2,3,4,5,6,7,8,16,32,64,128,256,
     888,2032,3968,4096,5088,6080,6144,7168,7680,7936}.

Count:
    23 unique direct key-switch matrices.

Every one is a member of the standard 8191-matrix addFrbMatrices family.

## 4. Standard-profile incremental key footprint is zero

Under the pinned STANDARD BOOTSTRAPPING PROFILE:

    addSome1DMatrices
    + addFrbMatrices
    + genRecryptData,

the matched baseline already has:
- full regular 1D matrices chosen by addSome1DMatrices;
- all 8191 direct Frobenius matrices;
- main-key relinearization matrices;
- key0->key1 recryption key-switch matrix;
- recryptEkey.

The candidate's 23 direct Frobenius matrices are a strict subset of the existing 8191 full family.

The candidate uses the same:
    key0
    key1
    recryptEkey
    key0->key1 switch.

Therefore:

    DELTA_STANDARD_FROBENIUS_KEYS =0
    DELTA_STANDARD_SECRET_KEYS =0
    DELTA_STANDARD_RECRYPT_EKEYS =0.

For a guarded fast+fallback wrapper, if baseline standard keys are retained:

    Keys_guarded
      = Keys_baseline union Keys_candidate
      = Keys_baseline

with respect to automorphism/recryption key material.

This REFines the earlier generic Turn-17 statement
    Keys_guarded = union(candidate,baseline):
the set-theoretic statement remains true, but under the standard pinned profile the union collapses to the baseline key set.

Snapshot ciphertext memory remains an independent guarded cost.

## 5. Candidate may use fewer regular key matrices than baseline

Aung's split MultKey branch includes:
    SlotsToCoeff
    ...
    CoeffToSlots.

Pinned HElib thin bootstrapping implements these with ThinEvalMap/EvalMap machinery and standard keygen provisions:
    addSome1DMatrices
    addFrbMatrices.

The active candidate removes those per-split SlotsToCoeff/CoeffToSlots maps from the one-MultKey carrier path.

Its carrier merge is public polynomial multiplication/addition.
Its RM10 and recovery use only Frobenius-subgroup automorphisms.

Therefore an UNGUARDED candidate-specific minimized keyset can plausibly omit some regular 1D slot-rotation matrices required by the split baseline.

However:
- Aung's paper does not publish its exact key inventory;
- Turn 12 already proves runtime/key profile under-specification;
- HElib standard keygen may overprovision matrices.

So no key-size reduction is claimed before exact serialized inventory comparison.

## 6. Minimal-direct candidate key profile

If one intentionally avoids full addFrbMatrices and creates direct matrices only for candidate automorphisms, an explicit sufficient candidate Frobenius set has:

    23 direct key0->key0 matrices.

This is not claimed to be globally optimal in memory/runtime:
- composed BSGS strategies can use different smaller/larger matrix sets;
- direct matrices trade memory for fewer chained key switches.

It is merely a reproducible upper/sufficient direct profile.

Relative to a hypothetical Method-1-only Frobenius baseline with only:

    J_method (9 direct matrices),

candidate adds at most:

    14 additional direct Frobenius targets.

But the real matched split baseline also needs SlotsToCoeff/CoeffToSlots and may already contain many/all of these targets.

Therefore the actual candidate-minus-baseline delta satisfies:

    UNKNOWN until serialized key inventory,

and should NOT be reported as +14.

## 7. RLWE sample exposure

Pinned GenKeySWmatrix creates, for every key-switch matrix:

    nDigits = context.getDigits().size()

RLWE encryption columns under the target secret key.

Each matrix therefore contributes approximately nDigits public RLWE samples/columns, together with a PRG seed for the a-values.

Thus if a minimized candidate profile adds Delta_M matrices beyond a minimized matched baseline, the concrete public-sample exposure increases by roughly:

    Delta_samples = Delta_M * nDigits

for the relevant target secret.

This does NOT introduce a new hardness assumption.
It can affect concrete security estimates because the number of available RLWE samples changes.

Step 6 must therefore serialize and account:
- unique KeySwitch tuples;
- nDigits for each;
- target key IDs;
- matrix plaintext spaces;
- modulus chain/dimension;
- total public RLWE sample count.

Do not infer unchanged bit security solely from unchanged n,q,secret distribution.

## 8. Circular/key-dependent material

Pinned genRecryptData creates:
- a key-switch matrix encrypting main secret material under the bootstrapping secret;
- recryptEkey encrypting the bootstrapping secret under key0.

The candidate uses exactly the same bootstrapping data as the baseline stock MultKey.

It does NOT:
- generate another encrypted secret;
- add another circular edge;
- add a field-switching/subring-secret key.

Therefore:

    CIRCULAR_SECURITY_STRUCTURE = baseline-identical

for the active unguarded candidate.

Guarded mode also reuses the same objects.

## 9. Plaintext spaces of matrices

Pinned GenKeySWmatrix behavior in bootstrappable BGV:
- default ptxtSpace for ordinary automorphism/relinearization matrices is the larger bootstrapping plaintext space;
- genRecryptData explicitly generates key0->key1 at application p^r.

For the active R2 reference profile:
- application p^r=5;
- temporary/recryption plaintext space is625.

Therefore candidate automorphism matrices are source-compatible with the same bootstrapping plaintext-space family as the baseline.

No new plaintext-modulus key family is required.

Exact realized values remain Step-3 serialized facts because Turn 12 showed author runtime under-specification.

## 10. Security comparison with classical field switching

Turn 22 found classical field switching switches to a secret inside a smaller subring and bases security on RLWE over the smaller field.

The active candidate does NOT do this.

Its carrier is a plaintext representation inside the existing outer BGV ring.
All automorphism key switches still encrypt relations among automorphisms of the same outer secret key.

Therefore the candidate avoids:
- a small-ring secret;
- a smaller-dimensional RLWE hardness requirement;
- a field-switching key family.

This supports the paper statement:

    "no new cryptographic assumption relative to the matched HElib/Aung baseline"

at the ASSUMPTION-FAMILY level.

It does NOT yet prove identical concrete security bits.

## 11. Step-3/4 exact key-inventory contract

Native Step 3 must serialize every public key-dependent object.

For each KeySwitch:
    fromSPower
    fromXPower
    fromKeyID
    toKeyID
    ptxtSpace
    nDigits
    number/prime sets of b-columns
    noiseBound
    serialized byte size.

Also record:
    pubEncrKey size
    recryptKeyID
    recryptEkey size
    stored skBounds
    regular-dimension KS strategies
    Frobenius KS strategy
    total serialized evaluation-key bytes.

For Step 4 matched baseline:
construct the exact set:
    K_base.

For Step 5 candidate:
construct:
    K_fast.

For guarded mode:
    K_guard = K_base union K_fast.

Report:
    |K_fast \ K_base|
    |K_base \ K_fast|
    bytes(K_fast)
    bytes(K_base)
    bytes(K_guard).

This prevents standard HElib overprovisioning from being mistaken for a mathematically necessary key footprint.

## 12. Fair benchmark/security profiles

Two fair profiles should be distinguished.

### COMMON-STANDARD PROFILE

Both baseline and candidate use the same pinned standard bootstrapping evaluation-key set.

Advantages:
- clean latency/correctness comparison;
- candidate incremental key material is zero;
- guarded union is baseline-identical.

Disadvantage:
- cannot demonstrate minimal key-size improvements.

### MINIMIZED-PER-WORKFLOW PROFILE

Generate only the exact matrices required by each workflow.

Advantages:
- exposes true key-size/memory Pareto behavior.

Requirements:
- both baseline and candidate must be minimized symmetrically;
- exact key inventories serialized;
- security re-estimated with actual sample counts;
- key-generation policy included in benchmark methodology.

Do not mix standard baseline keys with minimized candidate keys when claiming key-size wins.

## 13. Current security/key-footprint classification

ASSUMPTION_FAMILY:
    unchanged from matched HElib/Aung BGV bootstrapping.

SECRET_KEY_IDS:
    same {key0,key1}.

NEW_SUBRING_SECRET:
    NO.

NEW_RECRYPT_EKEY:
    NO.

NEW_CIRCULAR_EDGE:
    NO.

CANDIDATE_DIRECT_FROBENIUS_TARGETS:
    23.

STANDARD_FULL_FROBENIUS_TARGETS:
    8191.

STANDARD_PROFILE_INCREMENTAL_FROBENIUS_MATRICES:
    0.

MINIMIZED_PROFILE_INCREMENT:
    UNKNOWN until exact baseline inventory.

GUARDED_STANDARD_KEYSET:
    equal to standard baseline keyset.

GUARDED_SNAPSHOT_MEMORY:
    still additional and must be measured.

CONCRETE_SECURITY_BITS:
    UNKNOWN / Step 6.

## Verdict

PASS_NO_NEW_SECRET_OR_RING_ASSUMPTION.
PASS_CANDIDATE_AUTOMORPHISMS_ALL_IN_BASELINE_FROBENIUS_SUBGROUP.
PASS_STANDARD_PROFILE_ZERO_INCREMENTAL_FROBENIUS_KEYS.
PASS_BASELINE_IDENTICAL_RECRYPTION_KEY_STRUCTURE.
PASS_GUARDED_STANDARD_UNION_COLLAPSES_TO_BASELINE_KEYSET.

MINIMIZED_KEY_SIZE_DELTA:
    UNKNOWN, must be serialized.

CONCRETE_MULTI_SAMPLE_SECURITY:
    PENDING.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
NOVELTY_STATUS=PREFLIGHT.
PAPER_READINESS=NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise no further side turn should repeat key-footprint bookkeeping.
The remaining highest-value independent tasks are:
- a handoff/readiness audit for Turns 8-23 to identify any unresolved paper-level semantic edge before the 25-turn ceiling;
or
- a bounded exact source audit of the baseline ThinEvalMap interface needed for Step 4.

No benchmark.
No generalization native work.
