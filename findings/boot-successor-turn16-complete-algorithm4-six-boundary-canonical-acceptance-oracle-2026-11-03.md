# BOOT / B158 — Successor Research Turn 16 — complete Algorithm-4 six-boundary exact-canonical acceptance oracle

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

GitHub Notes read of the Turn-15 predecessor was attempted first and remained degraded.
The exact Turn-15 durable finding was recovered by exact Git fetch:

    findings/boot-successor-turn15-exact-canonical-runtime-certificate-route-2026-11-03.md
    commit 77c905389b3621847fea75f744ee736e388281dc
    blob 149ab763b8829e78de0d57688247eeb30296ae91.

The target Turn-16 path was checked absent before write.

The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Pinned HElib:
    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Primary source:
    Aung et al., ePrint 2025/350 / PKC 2025.

The official PDF text backend was inspected for Algorithm 4.
A screenshot attempt of the relevant PDF page was made as required by the research runtime, but the official PDF host returned HTTP 403.
No visual-layout-only claim is used.

## Why this turn is paper-level

Turn 15 establishes a credible exact-canonical runtime-certificate route beyond the Turn-14 coefficient-L1 proof obstruction.

That result is not yet enough for complete candidate correctness because Aung Algorithm 4 contains six semantically meaningful
subtract/divide boundaries spread across three plaintext spaces.

A native run must not be judged by a vague final capacity check.
It needs one frozen oracle that answers, at every operation:

- what exact plaintext state is expected;
- what plaintext space is expected;
- what intFactor invariant is required;
- what prime-set transition occurred;
- what canonical certificate update is valid;
- where divisibility by5 must be checked;
- and where wraparound would invalidate the trace even if a later state decrypts correctly by accident.

This turn formalizes that oracle.

## Closest prior / exact delta

Closest source prior:
- Aung Algorithm 4 correction-style digit extraction;
- pinned HElib BGV arithmetic and noise bookkeeping.

Closest durable candidate prior:
- Turn 13 exact common-lift L0..L3;
- Turn 15 exact-canonical certificate route.

Turn-16 delta:
construct one implementation-independent acceptance oracle for the complete six-boundary Algorithm-4 trace.

No new cryptographic mechanism, key family or hardness assumption is introduced.
NOVELTY_STATUS remains PREFLIGHT.

## Primary hypothesis

H16:
Given exact common-lift L0,L1,L2,L3 and a parallel upward-certified canonical ledger C, every semantic and noise/capacity requirement of Aung Algorithm 4 can be reduced to a finite sequence of source-local assertions.

If all assertions pass, the complete Algorithm-4 portion of a native candidate trace is correctness-certified for that realized key/ciphertext/context.

Falsifier:
- one Algorithm-4 operation lacks a source-compatible canonical certificate transition;
- an intermediate state can wrap modulo Q without being detected by the oracle;
- divideByP cannot be linked to an exact quotient oracle;
- or the six-boundary semantic state cannot be reconstructed from the source algorithm.

## 1. Exact Aung state machine for e=4

Aung Algorithm 4:

    u_0,0 <- z
    for j=0,...,e-2:
        y <- L_{j+1}(z)
        for i=0,...,j:
            u_{i,j+1} <- F_e(u_{i,j})
            y <- (y-u_{i,j+1})/p
        u_{j+1,j+1} <- y
    u_{e-1,e-1} <- Recode(u_{e-1,e-1})

For p=5,e=4 define:

    F(X)=X^5-5X^3+5X.

The exact six-boundary schedule is:

B1:
    u_0,1 = F(u_0,0)        in Z625
    N_1   = L1-u_0,1        in Z625
    u_1,1 = N_1/5           in Z125

B2:
    u_0,2 = F(u_0,1)        in Z625
    N_2   = L2-u_0,2        in Z625
    y_2,0 = N_2/5           in Z125

B3:
    u_1,2 = F(u_1,1)        in Z125
    N_3   = y_2,0-u_1,2     in Z125
    u_2,2 = N_3/5           in Z25

B4:
    u_0,3 = F(u_0,2)        in Z625
    N_4   = L3-u_0,3        in Z625
    y_3,0 = N_4/5           in Z125

B5:
    u_1,3 = F(u_1,2)        in Z125
    N_5   = y_3,0-u_1,3     in Z125
    y_3,1 = N_5/5           in Z25

B6:
    u_2,3 = F(u_2,2)        in Z25
    N_6   = y_3,1-u_2,3     in Z25
    u_3,3 = N_6/5           in Z5

Final:
    out = Recode(u_3,3)     in Z5.

The source proof guarantees each N_b is divisible by5 for an input
z=sum_i a_i phi(e_i) with arbitrary a_i in Z625, provided L0..L3 are computed from the SAME a_i.

Turn 13 supplies exactly that same-lift condition.

## 2. Plaintext-space and diagonal-state invariant

Define row index i by its p-adic level.

Every u_{i,j} must satisfy:

    ptxtSpace(u_{i,j}) = 5^(4-i).

Thus:

    i=0 ->625
    i=1 ->125
    i=2 ->25
    i=3 ->5.

Fe preserves the ptxtSpace of its input.

The six divide boundaries are therefore frozen as:

    625->125
    625->125
    125->25
    625->125
    125->25
    25->5.

Any deviation is:

    FAIL_ALGORITHM4_PTXTSPACE_LADDER.

No implicit gcd-based reduction is accepted as a substitute for the source schedule.

## 3. Parallel canonical certificate state

For every live ciphertext state c maintain:

    Cert(c) = C_c

such that C_c is an independently recomputed upward upper bound on the L-infinity norm of the canonical embedding
of the TOTAL centered raw decryption representative.

The certificate is separate from HElib's floating noiseBound.

Initial values at Algorithm-4 entry may conservatively use Turn-13 absolute coefficient-L1 envelopes because:

    ||f||_can,infty <= ||coeff(f)||_1.

Thus:

    C(L0) <= 41,293,704,600,473,801,437,489
    C(L1) <=199,931,454,860,029,347,739,390
    C(L2) <=903,000,468,553,559,669,777,792
    C(L3) <=2,091,555,622,746,351,241,865,519.

A tighter direct canonical entry certificate is permitted but not required.

## 4. Correctness threshold is especially simple for m=32768

Pinned PAlgebra::calcPolyNormBnd removes powers of two and returns1 if the residual m is1.

For:

    m=32768=2^15,

therefore:

    polyNormBnd =1.

Pinned Ctxt::isCorrect uses:

    totalNoiseBound * polyNormBnd <=0.48*Q.

The parallel verifier therefore uses the exact sufficient threshold:

    C_c <0.48*Q_c.                         (T16.1)

No hidden canonical-to-polynomial conversion factor is present for this power-of-two ring.

Every arithmetic event that can reduce modulo Q must satisfy (T16.1) after the event.

Checking only before divideByP is insufficient.

## 5. Event-level certificate rules

The verifier replays the ACTUAL trace.

### E-MODUP

Pinned modUpToSet adds prime product F and scales every ciphertext part by F.

Update:

    Q' = FQ
    C' = FC.

Capacity Q/C is unchanged.

### E-MODDOWN

For dropped product F, retain exact source delta_i polynomials BEFORE floating conversion.

For each part i define exact rational:

    fdelta_i = delta_i/F.

Compute an outward-certified canonical norm:

    D_i >= ||fdelta_i||_can,infty.

Let the source handle be:
- one: weight1;
- secret-key power d: use stored rejection-enforced S_key^d.

Update:

    C' = C/F + sum_i D_i*S_i^d.           (T16.2)

The floating source value is diagnostic only.

### E-TENSOR

For same-Q operands:

    C_tensor <= C1*C2.                    (T16.3)

Require immediately:

    C_tensor <0.48Q.

This catches a multiplication wrap before any later relinearization.

### E-RELINEARIZE / KEY SWITCH

Pinned reLinearize first scales to include special-prime product S.

Base inherited certificate becomes:

    C_scaled = S*C_in.

For every actual nonbase part, pinned breakIntoDigits reconstructs the actual digit polynomials.

For each digit k compute upward certificate:

    G_k >= ||digit_k||_can,infty.

Pinned KeySwitch W has rejection-enforced:

    W.noiseBound >= ||RLWE_error_W||_can,infty.

Charge:

    Delta_KS = (sum_k G_k)*W.noiseBound.

Combine all switched/base parts by triangle inequality.

After cleanup, every real special-prime drop is certified by E-MODDOWN using its own actual fdelta.

No noiseBoundForUniform estimate enters the independent ledger.

### E-AUTOMORPH

Canonical embedding coordinates are permuted.

Update:

    C'=C.

Any following key switch is charged separately.

### E-MUL-PUBLIC-POLY

For public polynomial g:

    G >= ||g||_can,infty

from outward interval evaluation.

Update:

    C' <= G*C.

### E-MUL-SCALAR-UNIT / FACTOR ALIGNMENT

Pinned mulIntFactor(e) multiplies all parts by:

    b=balRem(e,P).

Update:

    C' = |b|*C.

Metadata:

    intFactor' = e*intFactor modP.

### E-ADD-CONSTANT

For FatEncoded/ZZX BGV constant g, pinned source scales by:

    f=balRem(intFactor*(Q modP),P)

when applicable.

With certified public canonical norm G:

    C' <= C + |f|*G.                      (T16.4)

For the EncodedPtxt path, certify the actual balanced scaled polynomial produced by source.

### E-ADD/SUB

After the actual source prime-set matching and factor harmonization choices have been logged:

    C' <= |b1|*C1 + |b2|*C2,

where b1,b2 are the exact balanced multipliers actually applied by harmonization.

If no harmonization occurs:

    C'<=C1+C2.

The verifier does NOT rerun HElib's heuristic decision logic.
It certifies the decisions actually taken.

### E-DIVIDE-BY-P

Semantic precondition:
    plaintext numerator belongs to 5E.

Pinned divideByP:

    C' = C/5
    P' = P/5
    Q' = Q
    intFactor' = intFactor mod P'.

No new noise is introduced.

## 6. Interval/upward canonical-norm requirement

Source embeddingLargestCoeff uses ordinary floating arithmetic and is not itself a formal outward upper bound.

The verifier must independently recompute every critical canonical norm.

For integer polynomial g:
- preserve exact integer coefficients;
- evaluate g at all primitive 32768-th roots using rigorous complex intervals or equivalent certified FFT;
- outward-round the maximum magnitude.

For mod-down fdelta:
- preserve exact integer delta and exact dropped-prime product F;
- evaluate delta/F as exact rationals with outward-rounded complex intervals.

For a digit polynomial:
- preserve the exact reconstructed integer polynomial returned by the source-equivalent digit decomposition;
- certify its canonical norm independently.

Hash the exact coefficient object and store:
    precision
    interval backend/version
    lower/upper norm interval
    chosen upper endpoint.

A plain double from embeddingLargestCoeff is not sufficient paper evidence.

## 7. Exact semantic oracle

In the correctness harness, secret-key decryption is permitted only for assertions.

Maintain a plaintext oracle independently from ciphertext operations.

Entry:
    U_0,0 = plaintext(L0)
    L1,L2,L3 are the exact Turn-13 common-lift correction maps.

Fe:
    U_i,j+1 = F(U_i,j)
    in Z_(5^(4-i)).

At boundary b:
    N_b^oracle = Y_b^oracle-U_b^oracle.

Require:

    N_b^oracle mod5 =0.

Define the exact quotient coefficientwise modulo the lower p-power:

    Quot5(N_b) in Z_(P/5).

Before divideByP:
- decrypt the numerator;
- require equality with N_b^oracle;
- require every coefficient/slot is divisible by5.

After divideByP:
- decrypt;
- require equality with Quot5(N_b^oracle).

This is stronger than merely checking that divideByP did not throw.

Failure codes:

    FAIL_B1_SEMANTIC_ORACLE
    ...
    FAIL_B6_SEMANTIC_ORACLE.

## 8. intFactor invariant

From Turn 13, Algorithm-4 inputs enter with:

    intFactor=67 mod625.

At every named event require:

    gcd(intFactor,5)=1.

Pinned tensorProduct:
    f_out=f1*f2*(Q modP) modP

preserves unit-ness.

Factor harmonization uses units.

Real mod-down leaves intFactor unchanged.

divideByP reduces a 5-adic unit to a lower p-power unit.

Therefore any observed nonunit factor is an implementation/state failure:

    FAIL_ALGORITHM4_NONUNIT_FACTOR.

The exact numeric factor trajectory is logged but not pre-frozen.

## 9. Prime-set invariant

At every named checkpoint serialize:

    primeSet
    Q=product(primeSet)
    whether special/small primes are present.

At semantic checkpoints:
- after each Fe cleanUp;
- immediately before each subtraction/divide boundary;
- after each divideByP;

require no small/special primes unless the exact source operation explicitly places the checkpoint inside relinearization.

A divideByP must leave primeSet unchanged.

The verifier accepts source-selected/natural prime sets provided every transition is independently certified.
It does not require a preselected prefix.

## 10. Six-boundary acceptance table

Boundary B1:
    operands:
      L1, u_0,1
    P=625
    numerator N1
    output u_1,1
    output P=125.

Boundary B2:
    operands:
      L2, u_0,2
    P=625
    numerator N2
    output y_2,0
    output P=125.

Boundary B3:
    operands:
      y_2,0, u_1,2
    P=125
    numerator N3
    output u_2,2
    output P=25.

Boundary B4:
    operands:
      L3, u_0,3
    P=625
    numerator N4
    output y_3,0
    output P=125.

Boundary B5:
    operands:
      y_3,0, u_1,3
    P=125
    numerator N5
    output y_3,1
    output P=25.

Boundary B6:
    operands:
      y_3,1, u_2,3
    P=25
    numerator N6
    output u_3,3
    output P=5.

For EACH boundary require:

1. both operands decrypt to their independent semantic-oracle values;
2. same ptxtSpace P;
3. both intFactors are 5-adic units;
4. actual prime/factor matching decisions are serialized;
5. every event-level canonical certificate passes C<0.48Q;
6. numerator decrypt equals oracle numerator;
7. numerator is divisible by5;
8. divideByP leaves primeSet unchanged;
9. resulting ptxtSpace=P/5;
10. resulting intFactor remains a 5-adic unit;
11. resulting certificate is C_num/5;
12. output decrypt equals exact quotient oracle.

No boundary may be skipped because the final plaintext happens to decrypt correctly.

## 11. Final Recode acceptance

Aung Algorithm 4 ends with one Recode on:

    u_3,3 at ptxtSpace5.

Require:
- input decrypt equals the exact u_3,3 oracle;
- ptxtSpace=5;
- intFactor unit;
- every automorphism/key-switch/public-linear Recode event certified by the same canonical ledger;
- output decrypt equals the source RMFE recode oracle;
- every intermediate arithmetic event satisfies C<0.48Q.

Only after final Recode may the saved application intFactor be restored, following source placement.

## 12. Deterministic power-of-two fallback sanity bounds

For m=32768, n=16384:

    csc(pi/(2n))
      =10430.378366449419

and R2 h=120 stored secret bound:

    S_120
      =34.12458444202227.

For a canonical two-part ciphertext and plaintext space P, a deterministic fallback on one normalized mod-down rounding contribution is:

    Delta_det(P)
      <= (P/2)*csc(pi/(2n))*(1+S_120).

Thus:

    P=625:
      Delta_det <=114,488,345.52956091
      log2 <=26.77062550412444

    P=125:
      Delta_det <=22,897,669.105912182
      log2 <=24.448697409237077

    P=25:
      Delta_det <=4,579,533.821182436
      log2 <=22.126769314349712.

These are fallback guards only.
The authoritative runtime certificate uses actual fdelta norms and can be much tighter.

The decreasing P ladder is therefore naturally favorable to later boundaries.

## 13. Trace artifact schema

The complete candidate correctness artifact must contain one ordered event stream.

Per event:

    event_index
    algorithm4_node
    operation
    input_state_ids
    output_state_id
    ptxtSpace_before/after
    intFactor_before/after
    primeSet_before/after
    exact Q_before/after
    secret-handle metadata
    public constant identifier/hash if any
    exact delta/digit object hash if any
    certified canonical norm interval
    certificate_C_before
    certificate_increment/scaling
    certificate_C_after
    0.48Q threshold
    pass/fail.

Per boundary:

    numerator plaintext hash
    numerator mod5-zero assertion
    exact quotient plaintext hash
    decrypt-before equality
    decrypt-after equality
    divideByP state transition.

Global provenance:

    HElib exact commit
    context serialization
    key hashes
    KeySwitch W identifiers and stored W.noiseBound
    secret stored skBound
    interval backend/version/precision
    source/test patch hashes.

## 14. Failure taxonomy

Scientific failures are localized:

    FAIL_CANONICAL_CERTIFICATE_EVENT_<k>
      C_after >=0.48Q after an arithmetic event;

    FAIL_ALGORITHM4_PTXTSPACE_LADDER
      source state has wrong plaintext space;

    FAIL_ALGORITHM4_NONUNIT_FACTOR
      gcd(intFactor,5)!=1;

    FAIL_Bn_DIVISIBILITY
      semantic numerator is not in5E;

    FAIL_Bn_SEMANTIC_ORACLE
      decrypt/plaintext trace disagrees with exact oracle;

    FAIL_DIVIDEBYP_STATE
      primeSet/PTXT/factor transition differs from pinned source;

    FAIL_RECODE_ORACLE
      final Recode differs from source map;

    FAIL_CERTIFICATE_PROVENANCE
      exact norm inputs/hashes or interval proof are missing.

An infrastructure failure remains:

    INFRA_BLOCKED

and is not a scientific candidate FAIL.

## 15. Soundness theorem for a realized trace

Assume:

A1. Turn-13 exact common-lift L0..L3 theorem.
A2. Honest pinned HElib key generation successfully returns, so stored skBounds/W.noiseBound satisfy their source-enforced rejection bounds.
A3. Every external canonical norm in the parallel ledger is a valid outward upper bound.
A4. Every runtime primitive is recorded and certified by the source-shaped transition above.
A5. Every arithmetic event satisfies C<0.48Q.
A6. All six semantic numerator/quotient assertions pass.
A7. Final Recode oracle passes.

Then, by induction over the event stream:
- every ciphertext raw representative remains inside the source sufficient decryption region;
- every semantic operation equals the intended ring operation;
- all six divideByP calls realize the exact Aung quotients;
- the final ptxtSpace5 result equals Aung Algorithm-4 output for the same arbitrary Z625 lift vector.

Therefore:

    PASS_COMPLETE_ALGORITHM4_CANONICAL_TRACE

is a scientifically valid candidate-correctness result for that realized serialized context/key/input trace.

This is sample/trace correctness.
It is NOT by itself a distributional DFR theorem.

## 16. DFR/security boundary

The acceptance oracle converts one native trace into a deterministic post-hoc correctness certificate.

It does not answer:

    Pr_randomness[certificate fails].

A paper-level Step-6 DFR claim therefore needs one of:

1. a formal probabilistic bound on the exact-canonical events;
2. sufficiently justified sampling/statistical evidence with a declared confidence model;
3. a runtime guard/fallback design, where non-aborting traces are correctness-certified and abort/fallback probability is separately measured/bounded.

Do not reinterpret a single PASS trace as negligible DFR.

## Verdict

PASS_COMPLETE_SIX_BOUNDARY_SEMANTIC_ORACLE.
PASS_EVENT_LEVEL_EXACT_CANONICAL_CERTIFICATE_RULES.
PASS_POWER2_POLYNORMBND_ONE_BINDING.
PASS_COMPLETE_ALGORITHM4_REALIZED_TRACE_SOUNDNESS_CONTRACT.
PASS_LOCALIZED_FAILURE_TAXONOMY.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

COMPLETE_ALGORITHM4_NATIVE_TRACE:
    NOT_EXECUTED.

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

Do not touch, duplicate or resubmit the background task.

If BOOT-T11-R8-SMALL-CANARY-20261103-R2 becomes ready, independently audit it immediately.

Otherwise a further correctness side-turn should only be spent if it attacks a genuinely new uncertainty, such as:
- whether the exact-canonical trace certificate can be converted into a quantitative DFR theorem without a runtime guard;
or switch to bounded novelty/value audit.

Do not return to coefficient-L1 prefix tuning.
Do not benchmark.
