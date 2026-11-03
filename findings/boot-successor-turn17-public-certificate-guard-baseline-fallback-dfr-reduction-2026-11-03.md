# BOOT / B158 — Turn 17 — public certificate guard and baseline fallback DFR reduction

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority
GitHub Notes read of Turn 16 was attempted first and remained degraded.
Turn-16 finding is:
findings/boot-successor-turn16-complete-algorithm4-six-boundary-canonical-acceptance-oracle-2026-11-03.md
commit 7e88e69d0282b991eb20a3258b45a81987ec7f64
blob 99a826eb815bdd77951ef8bb02935cee634f2ef0.
User-supplied verified local authority for this turn is BBBINGW/memory HEAD==origin/main at c0960a278b9a5cf0a30f3c5b25277fcb6e9ebdcf. That local clone is not mounted here, so no connector-derived state is claimed to supersede it.
Pinned HElib: acdb264e1a991eaee35fd8b3c31bebe9528c49a1.
Primary paper: Aung et al. ePrint 2025/350, cached mirror SHA256 922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82, VERSION_UNVERIFIED.

## Primary hypothesis
The Turn-16 exact-canonical certificate can be used as a PUBLIC runtime guard. Preserve the five Method-1 outputs before sparse merge; run the one-MultKey candidate only on copies; on first guard failure discard candidate descendants and execute the source-faithful Aung split-thin tail from the preserved states.

Claim: successful fast traces are deterministically certified; fallback traces have matched-baseline correctness; hybrid DFR is no worse than matched baseline DFR, without proving guard-failure probability negligible.

## Source common branch point
Aung Algorithm 2 first computes:
c1,...,ck <- SlotsToCtxts(c)
and only then, for each ci, runs ModSwitch -> SlotsToCoeff -> InnerProduct -> CoeffToSlots.
Aung Sec.5.1 says Method 1 implements SlotsToCtxts with the projection maps tau_i.

The active candidate starts from the same five Method-1 outputs. Define:
S_i := tau_i(c), i=0,...,4.

Guarded execution:
1. compute S_0,...,S_4 once;
2. retain immutable snapshots;
3. construct sparse-R8 candidate only from copies;
4. if every fast-path certificate passes, return fast result;
5. otherwise discard fast descendants and execute the Aung five-split tail on S_i.

No decrypt/re-encrypt or surrogate boot key is needed.

Pinned HElib Ctxt has a default copy constructor; mutable ciphertext state is value-owned. Context/PubKey are const references. A guarded implementation must still hash/serialize snapshots before the fast branch and verify unchanged hashes before fallback. Mutation is a scientific implementation failure.

## Public-only guard
Production guard does not use Turn-16 secret-key debug decryption. Debug decrypt remains research-only implementation validation.

All certificate quantities are public/runtime:
- ciphertext parts and prime sets;
- context primes;
- exact mod-down delta polynomials;
- exact key-switch digit polynomials;
- public constants and intFactors;
- PubKey::getSKeyBound();
- public KeySwitch objects and KeySwitch::noiseBound.

The static Aung divisibility theorem plus Turn-13 common-lift theorem supplies semantic divide-by-5 validity for the verified implementation. Production guard therefore needs no secret polynomial or plaintext.

GUARD_PUBLIC_ONLY = YES.

## Guard scope
Fast-path guard is the conjunction of:
- Turn-8/11 rawModSwitch conditions and source raw gate;
- exact reconstruction/RM10/fused-map state invariants;
- every Turn-16 event-level canonical certificate C<0.48Q;
- ptxtSpace ladder;
- 5-adic-unit intFactor invariant;
- complete certificate provenance;
- successful outward canonical-norm certification.

Any missing certificate data, interval failure, malformed state, or conservative overflow is GUARD_FAIL and triggers fallback. False-positive failures affect value only; a false-pass is forbidden by the certificate contract.

A guard may fail after an operation whose candidate output is already unsafe. This is still safe because candidate operations use copies and all candidate descendants are discarded. Fallback restarts from untouched S_i.

## DFR reduction theorem
Let:
G = all fast-path guard checks pass.
F_fast = fast output incorrect.
F_base = matched baseline output incorrect.
F_hyb = guarded output incorrect.

Turn-16 trace soundness gives:
G => not F_fast.

On not G, guarded execution returns Base(S). Therefore:
F_hyb subseteq (not G) intersect F_base.

Hence, with no independence assumption:
Pr[F_hyb] <= Pr[F_base].

If the matched baseline has DFR bound delta_base:
Pr[F_hyb] <= delta_base.

Thus guard-failure probability is not needed for correctness/DFR. It becomes a value/availability metric.

This theorem assumes:
- verified fast-path semantic implementation;
- sound outward certificate;
- immutable snapshots;
- source-faithful matched fallback baseline.

## Standard confidentiality
The guard decision is a PPT function of public key/evaluation keys/public ciphertext state. In standard IND-CPA public-key FHE, revealing this public branch decision or choosing one of two public evaluation procedures does not require a new cryptographic assumption: any distinguisher for the public guard/evaluation transcript composes into a distinguisher for the underlying ciphertext distribution.

No circuit-privacy or physical side-channel claim is made.

## Key/memory/value cost
Fallback requires all baseline evaluation resources. Therefore:
Keys_guarded = Keys_candidate union Keys_baseline.

Until measured, guarded execution cannot claim reduced total evaluation-key size or removal of baseline automorphism keys.

Canonical fallback retains five pre-merge thin ciphertext snapshots until fast success/failure. Snapshot memory must be measured from actual serialized profile. A lower-memory recompute fallback is a separate Pareto variant.

Let:
T_shared = SlotsToCtxts time;
T_fast = complete guarded fast tail including certificate overhead;
T_base = baseline tail from preserved S_i;
p_fb = Pr[guard fails].

Conservative expected latency:
E[T_guarded] <= T_shared + T_fast + p_fb*T_base.

Matched baseline:
T_baseline = T_shared + T_base.

A sufficient expected-speedup condition is:
p_fb < 1 - T_fast/T_base,
which already requires T_fast<T_base.

Worst-case structural latency:
T_shared + T_fast + T_base.

No numerical performance claim is made.

## Evidence-order consequence
Step 2 remains pending R2.
Step 3 remains exact serialized profile.
Step 4 matched baseline correctness becomes a prerequisite for fallback correctness.
Step 5 must execute Turn-16 fast-path correctness and forced-fallback tests.
Step 6 may reduce candidate-specific DFR to:
delta_guarded <= delta_baseline
plus guard-soundness audit.
Fallback rate moves to VALUE.
Step 7 must measure fast latency, guard overhead, fallback rate, expected/worst-case latency, snapshot memory, and union key footprint.
Step 8 must independently audit both fast and forced-fallback traces.

Forced-fallback correctness tests must trigger failure at:
- before sparse merge;
- after one MultKey;
- inside first F4;
- immediately before B6;
and require the fallback output to match standalone matched baseline from the same S_i.

## Verdict
PASS_SOURCE_COMMON_FALLBACK_POINT.
PASS_IMMUTABLE_PREMERGE_SNAPSHOT_ROUTE.
PASS_PUBLIC_ONLY_CANONICAL_GUARD.
PASS_GUARDED_HYBRID_DFR_REDUCTION_TO_BASELINE.
PASS_NO_NEW_STANDARD_INDCPA_ASSUMPTION_FOR_GUARD_BIT.
PASS_EXPECTED_VALUE_THRESHOLD_FORMULA.

GUARDED_VARIANT=CREDIBLE.
FAST_PATH_MULTKEY_COUNT=1.
FALLBACK_MULTKEY_COUNT=5 split baseline MultKeys.
KEY_FOOTPRINT=UNION(candidate,baseline).
DFR_IF_BASELINE_BOUND=delta_guarded<=delta_baseline.
FALLBACK_RATE=UNKNOWN / VALUE METRIC.
NATIVE_STEP2_RESULT=UNKNOWN / PENDING.
CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
NOVELTY_STATUS=PREFLIGHT.
PAPER_READINESS=NOT_READY.

## AI provisional choice
Carry the guarded fallback as the preferred reversible correctness wrapper for later Step-5/6 evaluation, but do not replace the core paper thesis yet. If guard overhead, snapshot memory, union key footprint or fallback rate destroys the VALUE/PARETO case, remove the wrapper and require an independent DFR theorem for the unguarded candidate.

## Next action while R2 is pending
Do not modify/resubmit R2.
If R2 becomes ready, audit it immediately.
Otherwise move away from further correctness bookkeeping and perform a bounded novelty/value preflight of the sparse-R8 + shared-four-output mechanism, including later direct-RMFE-MultKey or shared multi-output Frobenius work.
No benchmark.
