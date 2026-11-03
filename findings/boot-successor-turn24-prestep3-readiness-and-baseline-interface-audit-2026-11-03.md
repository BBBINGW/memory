# BOOT / B158 — Turn 24 — pre-Step3 readiness and matched-baseline interface audit

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes read-before-write was attempted first and remains degraded.

Exact current durable predecessor:
    findings/boot-successor-turn23-security-key-footprint-preaudit-2026-11-03.md
    commit 6a3fda613a6cb3d7d537afad14a1776187bdc4f8
    blob 05d7b5ca6790d7eec3dc40e42bfc36221a8675e3.

The target Turn-24 path was checked absent before write.
The pending R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Pinned HElib:
    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Primary Aung source:
    ePrint 2025/350, cached mirror SHA256
    922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
    VERSION_UNVERIFIED.

This turn asks one readiness question only:

    If R2 receives a scientific PASS, is there any remaining unidentified STATIC
    source-semantic edge that should block opening Native evidence Step 3?

A secondary audit records the exact matched-baseline implementation boundary needed later for Step 4.

## Primary hypothesis

H24:
Conditioned on an independently audited scientific PASS for R2, all presently identified static semantic/type edges of the active p=5 fast path have a durable closure. R2 PASS is therefore sufficient to OPEN Step 3 exact parameter/interface verification, but not to skip Steps 3-5.

Falsifier:
- any active edge lacks a source-compatible domain/codomain;
- any ptxtSpace/intFactor/keyID transition is still only assumed;
- final Recode or Algorithm4 uses an incompatible key family;
- current fixed-ring framing changed the p=5 concrete construction;
- or the matched baseline cannot be defined source-faithfully from pinned HElib/Aung semantics.

## 1. Active fast-path static edge matrix

### E0 — Method-1 projection output type

Input:
    RMFE-packed application ciphertext at ptxtSpace5.

Output:
    five thin Method-1 projection ciphertexts.

Durable closure:
- Aung SlotsToCtxts Method 1 returns physical-slot integers in Z5;
- current Turn-9 exact theta dual closes the deterministic projection oracle;
- predecessor source-domain audit closes the thin scalar-slot interpretation;
- common application intFactor is preserved by the public linear projection.

Status:
    STATIC CLOSED.
    Native sample evidence remains R2.

### E1 — five projections -> p=5 sparse carrier

Current p=5 concrete carrier:
    S=Z625
    Y=X^1024
    C=S[Y]/(Y^16+1).

Each projection scalar pair is encoded in:
    tau_i(c)=b_i+c_iY^8.

The merged carrier is:
    A=sum_{i=0}^4 Y^i tau_i(c).

Turn 7/9 establish exact injective low-digit placement and the ten active coordinates.

Turn 19/20 fixed-ring reframing does NOT change this concrete p=5 encoding.
It is an abstraction/generalization only.

Status:
    STATIC CLOSED.

### E2 — merged pre-raw bootstrapping-key interface

Current source-shaped fast path:
    sparse merge
    -> canonicalize / prime reduction
    -> reLinearize(recryptKeyID)
    -> rawModSwitch
    -> newMakeDivisible
    -> divide by p^ePrime
    -> one recryptEkey reconstruction.

Turn 8 gives a source-aligned sufficient merged rawModSwitch capacity theorem.
Turn 11 repairs the native raw-L1 meaning to HElib's TOTAL centered raw-decryption polynomial.

R2 is the mandatory Native Step-2 canary for this exact edge.

Status:
    STATIC CLOSED / NATIVE PENDING.

A scientific R2 failure reopens only the first failing native semantic/interface stage.
An infrastructure failure does not falsify the edge.

### E3 — common dirty Z625 reconstruction

After recryptEkey reconstruction:
    ptxtSpace=625
    keyID=0
    intFactor=1
under the current reference contract.

Turn 9 proves that only the ten selected coefficients' residues modulo5 must match the source carrier;
canonical high p-adic digits are NOT required.

The reconstruction plaintext P supplies one common arbitrary Z625 lift state.

Status:
    STATIC CLOSED.

### E4 — RM10 carrier recovery

Ten source-liftable automorphism/add stages clear outer coefficients not divisible by1024.
The unnormalized projector scale is1024.

Turn 7/10 close:
- exact ten target automorphisms;
- subring support;
- source key interface;
- no normalization by224 in the physical path.

Status:
    STATIC CLOSED.

### E5 — same-lift correction fanout L0-L3

Turn 13 closes the previously missing Algorithm4 front end.

From one cleaned RM10 state:
    H_j=sigma^j(R), j=0,...,7

and four public maps:
    G_r=sum_j D_{r,j} H_j, r=0,...,3

produce the four correction inputs from the SAME arbitrary lift vector.

No extra MultKey and no second Frobenius bank are required.

Status:
    STATIC CLOSED.

Important evidence-order note:
    R2 validates only the core one-output recovery chain.
    Complete candidate Step 5 must instantiate and check G1,G2,G3 too.
This is an EXPLICIT later evidence task, not an unidentified theorem gap.

### E6 — common normalization / BGV representation

Combined unnormalized scale:
    1024*8=8192.

At ptxtSpace625:
    8192^(-1)=28 mod625.

The source-compatible scalar-unit operation:
    multByConstant(28L)

changes BGV metadata to:
    intFactor=67 mod625.

All four correction outputs begin Algorithm4 with the same ptxtSpace/prime-set/factor family.

Status:
    STATIC CLOSED.

### E7 — complete Algorithm4 nonlinear path

Turn 15 replaces the failed generic coefficient-L1 proof architecture with exact canonical-embedding certification.

Turn 16 freezes:
- six p-adic subtraction/divide boundaries;
- ptxtSpace ladder:
      625->125,
      625->125,
      125->25,
      625->125,
      125->25,
      25->5;
- event-level C<0.48Q certificate;
- factor-unit invariant;
- exact numerator/divide semantic oracle;
- final Recode oracle.

Status:
    STATIC/CERTIFICATE CONTRACT CLOSED.
    Complete Native Step-5 execution remains pending.

### E8 — final Recode and final factor restoration

The inherited source audit proves:
- Algorithm4 final Recode runs at ptxtSpace5;
- existing ptxtSpace625 automorphism matrices are type-compatible through HElib gcd reduction;
- final Recode must occur before restoration of the saved application factor f_in.

Turn 16 incorporates this final acceptance order.

Status:
    STATIC CLOSED.

### E9 — key/security interface

Turn 23 proves:
- same key IDs {key0,key1};
- same recryptEkey/recryption-key cycle;
- all active direct candidate automorphisms lie in the existing p=5 Frobenius subgroup;
- no subring secret or new RLWE ring family.

Status:
    ASSUMPTION-FAMILY CLOSED.
    Concrete serialized sample-count security remains Step 6.

## 2. No newly identified fast-path static semantic edge

Cross-checking E0-E9 against:
- Turns 7-16;
- predecessor final-Recode / arbitrary-lift static closures;
- Turn 23 key-interface pre-audit;
- current fixed-ring family reframing

found no contradiction in:
    domain/codomain,
    ptxtSpace,
    intFactor,
    keyID,
    prime-set semantics,
    arbitrary-lift requirement,
    correction-map ordering,
    final-Recode ordering.

The p=5 concrete implementation remains the same construction selected before the fixed-ring family theorem.
The family theorem does not supersede its exact constants or native acceptance contract.

Therefore:

    NO_NEW_STATIC_FASTPATH_BLOCKER_FOUND.

This statement is deliberately narrower than:
    "candidate correctness is proved."

Native evidence order is still mandatory.

## 3. R2 PASS is sufficient to OPEN Step 3, not later gates

If R2 is independently audited as scientific PASS, the next legal action is:

    Native Step 3 — exact parameter/interface verification

under Turn-12's two-tier provenance contract.

R2 PASS does NOT authorize:
- Step 4 baseline correctness without Step 3;
- Step 5 complete candidate correctness without Step 4;
- performance benchmarking;
- security/value closure.

If R2 is scientific FAIL:
    reopen only the first failing stage.

If R2 is INFRA_BLOCKED:
    Native Step 2 remains pending.

## 4. New audit result: Aung/HElib baseline operation-order ambiguity

Aung's high-level thin/RMFE bootstrapping descriptions write the branch logically as:

    ModSwitch
    -> SlotsToCoeff
    -> InnerProduct
    -> CoeffToSlots.

Algorithm 2 line order is:
    ModSwitch
    SlotsToCoeff
    InnerProduct
    CoeffToSlots.

Table-2 prose says the MultKey stage is Algorithm-2 lines3-6 and lists the same four conceptual operations, with a textual ordering inconsistency between InnerProduct and SlotsToCoeff in that sentence.

Pinned HElib thinReCrypt does NOT expose those as four identical high-level calls in that order.

Its exact source-shaped branch prefix is:

    dropSmallAndSpecialPrimes
    -> bringToSet(first three ctxt primes) under the pinned thin path
    -> slotToCoeff->apply
    -> canonicalize if needed
    -> modDownToSet
    -> reLinearize(recryptKeyID)
    -> rawModSwitch
    -> newMakeDivisible
    -> divide by p^ePrime
    -> recryptEkey reconstruction
    -> coeffToSlot->apply
    -> [stock thinReCrypt would next run extractDigitsThin].

The source "ModSwitch" abstraction therefore does not map one-to-one onto a single HElib call occurring before slotToCoeff.

Aung publishes:
- HElib commit acdb264;
- m,p,bits,w,k;
- stage capacities/timings;

but not the exact experiment source/binary needed to prove the authors' internal ordering and runtime profile byte-for-byte.

This is a BASELINE REPRODUCIBILITY ambiguity, not a candidate correctness contradiction.

## 5. Step-4 matched reference baseline contract

After Step 3 passes, define the baseline as:

    MATCHED_SOURCE_FAITHFUL_REFERENCE_PROFILE,

not:
    AUTHOR_EXACT_REPRODUCTION.

For each of the five Method-1 branches c_i:

1. begin from the exact same SlotsToCtxts output used by the candidate comparator;
2. use the SAME Tier-B serialized context, keys, primes, compilation profile and thread count;
3. execute the pinned HElib thin-recrypt PRE-DIGIT-EXTRACTION branch shape:
       drop/bring prime-set preparation
       -> slotToCoeff
       -> canonicalization/mod-down
       -> boot-key relinearization
       -> rawModSwitch/newMakeDivisible/divide
       -> recryptEkey reconstruction
       -> coeffToSlot;
4. STOP before stock extractDigitsThin;
5. run Aung CtxtsToSlots / correction-map construction on the five branch outputs;
6. execute Aung correction Algorithm4 and the final source Recode.

The baseline harness must assert:
- each c_i initially decrypts to its expected Z5 thin scalar slots;
- every branch uses identical serialized runtime profile;
- source raw-mod-switch gate passes per branch;
- reconstruction moves to the expected temporary ptxtSpace;
- branch semantic oracle is correct after coeffToSlot;
- L0-L3 are built from the five branch outputs in source branch order;
- final output decrypt matches the source plaintext.

## 6. Baseline intFactor policy for the matched reference harness

The pinned HElib recryption middle resets representation through:
    ctxt = recryptEkey.

For the reference baseline, the cleanest auditable convention is:

    branch reconstruction / coeffToSlot states use their realized source factor,
    serialized exactly;

all five branches must be factor-compatible before CtxtsToSlots.

Do NOT hard-code an unpublished author-specific factor-restoration location.

If the reference implementation keeps the standard reconstructed factor through CtxtsToSlots/Algorithm4 and restores the saved application unit at the final source-defined boundary, that is acceptable provided:
- semantic decrypt oracles match;
- factor alignment is serialized;
- both candidate and baseline use the same source-compatible factor convention for fair comparison where applicable.

Any deviation from the pinned HElib source must be explicit and justified.

## 7. Step-7 claim boundary

Aung Table 2 remains the publication fingerprint:

    SlotsToCtxts 369.2 / 2.284s
    MultKey      346.5 / 4.732s
    CtxtsToSlots 333.8 / 0.078s
    DigitExtract 101.0 / 4.240s
    Final                11.33s

But because the exact author implementation/runtime profile is under-specified, later benchmark wording must be:

    "matched source-faithful reference-profile comparison against Aung Corr.(TnM)"

unless author source/runtime artifacts are later recovered.

Do NOT claim:
    "bit-for-bit reproduction of the Aung implementation."

The Table-2 values are fingerprints and external context, not exact Step-4 acceptance values.

## 8. Readiness matrix

### Static fast-path theorem/interface
    READY.

### Native Step 2
    PENDING R2.

### Step 3 contract
    READY TO OPEN ON R2 PASS.

Includes:
- PAPER_EXPLICIT assertions;
- NATIVE_SERIALIZED profile;
- exact key inventory;
- ptxtSpace/key-strategy checks;
- publication fingerprints.

### Step 4 baseline contract
    SOURCE-SHAPED CONTRACT NOW FROZEN.
    EXECUTION PENDING.

### Step 5 candidate contract
    READY IN DESIGN:
    - R2 core chain;
    - G1-G3;
    - complete Turn-16 Algorithm4 event stream;
    - final Recode/factor restore.
    EXECUTION PENDING.

### Step 6 security/noise/DFR
    CONTRACT PARTIAL / EXECUTION PENDING.

### Step 7 benchmark
    VALUE ZONES PRE-REGISTERED / EXECUTION PENDING.

### Step 8 independent audit
    PENDING.

### Novelty
    PREFLIGHT.
    2026/927 full-text source gate remains.

## 9. Scientific classification

This turn does NOT:
- infer R2 success;
- prove baseline correctness;
- prove complete candidate native correctness;
- resolve concrete security;
- resolve performance;
- upgrade novelty.

It DOES close the session-level question:
    "Is another unknown static semantic theorem required before Step 3?"

Answer:
    NO IDENTIFIED ONE.

It also prevents a future methodology error:
    treating Aung's high-level Algorithm2 ordering as an author-exact HElib binary reproduction.

## Verdict

PASS_PRESTEP3_STATIC_READINESS_AUDIT.
PASS_NO_NEW_IDENTIFIED_FASTPATH_SEMANTIC_EDGE.
PASS_R2_PASS_SUFFICIENT_TO_OPEN_STEP3.
PASS_STEP4_SOURCE_SHAPED_BASELINE_CONTRACT.
REFINE_BASELINE_CLAIM_TO_MATCHED_REFERENCE_PROFILE.
FAIL_AUTHOR_EXACT_BASELINE_REPRODUCIBILITY_FROM_PUBLICATION_ALONE.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE:
    BLOCKED.

BASELINE_CORRECTNESS:
    PENDING.

SECURITY_GATE:
    PENDING.

VALUE_GATE:
    PENDING.

AUDIT_GATE:
    PENDING.

NOVELTY_STATUS:
    PREFLIGHT.

PAPER_READINESS:
    NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes available, it must preempt the next free substantive turn for independent audit.

If R2 remains pending for Turn 25, do one final substantive SESSION-CLOSURE audit only:
- freeze the exact successor-handoff state;
- identify no more than the highest-priority remaining independent paper-level uncertainty;
- do not start another broad derivation family or benchmark.

Turn 26, if reached with R2 still pending, is HANDOFF ONLY.
