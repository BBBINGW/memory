# BOOT / B158 — Successor Research Turn 10 — Native evidence Step-2 small-canary execution contract

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE

AUTHORIZED_NATIVE_TASK:
    BOOT-T10-R8-SMALL-CANARY-20261103-R1

TASK STATUS AT END OF TURN:
    READY_TO_EXECUTE / NOT_EXECUTED

## Read-before-write / authority

GitHub Notes was attempted first for the Turn-9 predecessor and returned an empty body.
Exact Git fetch at the user-supplied authority commit

    717bcb2e7d78ebb4ed2b5f43bca8d65b77190e11

verified:

    findings/boot-successor-turn9-small-canary-oracle-execution-contract-gate-2026-11-03.md
    blob 9b5a28dc5501ecb69ac692fbb4c5e16d84c61708.

The target Turn-10 finding path was checked absent before write.

No newer main artifact is used as scientific authority in this turn.

## Why this turn is an execution launch, not another static micro-audit

Turn 8 closed the merged pre-raw absolute-capacity theorem.
Turn 9 closed:
- exact Method-1 trace-dual constants;
- 2560/2560 power-basis projection checks;
- the arbitrary-Z625-lift correction to the pre-DigitExtract oracle;
- the exact two-layer native acceptance contract.

Native evidence order therefore blocks all later gates until Step 2 is actually run.

The current Chat container cannot execute the task:
- no HElib checkout;
- no NTL installation;
- Debian package metadata is unavailable locally;
- DNS fails;
- direct known-IP TCP attempts to GitHub and Debian mirrors are also rejected;
- GitHub Notes is restricted to research-memory paths;
- the general GitHub integration cannot create source/workflow files in BBBINGW/memory and returns
  403 Resource not accessible by integration.

These are infrastructure facts only. They are NOT scientific evidence and do not alter the candidate verdict.

## Closest prior / exact delta

Closest prior remains Aung et al. ePrint 2025/350 Algorithm 2 and Method-1 SlotsToCtxts.

No new algorithmic delta is introduced in Turn 10.

The only purpose of the authorized task is to test the already-defined candidate-specific delta:

    five Aung Method-1 projections
    -> sparse R8 carrier
    -> ONE coefficient-domain MultKey
    -> unnormalized RM10
    -> fused eight-Frobenius recode
    -> scalar-unit28,

under pinned HElib source semantics.

NOVELTY_STATUS remains PREFLIGHT.

## One primary hypothesis

H10:
A deterministic source-faithful native execution of the already-specified small canary under

    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

will satisfy all Step-2 semantic/state assertions before DigitExtract.

Falsifier:
the first exact native assertion failure at any of:
- Method-1 scalar projection;
- sparse-R8 coefficient representation;
- Turn-8 raw correctness condition;
- HElib rawModSwitch gate;
- reconstruction low-digit semantics;
- RM10 coefficient selection;
- fused D_j recode;
- scalar-unit28 intFactor state;
- final exact Z625 plaintext oracle.

A build/dependency/infrastructure failure is not a scientific falsifier.

## Important harness correction: lift Method-1 theta through EncryptedArray slot encoding

Turn 9 derived the local-slot trace dual for x in {0,1,2,3,4}:

    theta_x
      = 448 + sum_{j=1}^{511} 286*x^j*xi^(512-j) mod625

in

    G'=Z625[xi]/(xi^512+182),
    xi=X^16.

At application plaintext modulus5 this becomes:

    theta_x mod5
      = 3 + sum_{j=1}^{511} x^j*xi^(512-j).

For native SIMD evaluation, do NOT assume that simply inserting this local polynomial as one raw
global ZZX is the canonical slot-wise multiplier.

Pinned HElib EncryptedArray encoding explicitly embeds a vector of slot elements into the CRT
plaintext ring.

Therefore the source-faithful canary shall form the public Method-1 multiplier as:

    local_theta_i = theta_{x_i} mod5;
    global_theta_i = EA_5.encode({local_theta_i, local_theta_i});

and then execute:

    c_i = global_theta_i * c;
    for t=0,...,8:
        c_i <- c_i + Frobenius^(2^t)(c_i).

This resolves only the test-harness representation.
It does not modify Aung's projection map or the candidate mechanism.

## Fixed native environment

Pin exactly:

    HElib commit:
      acdb264e1a991eaee35fd8b3c31bebe9528c49a1

Context:
    m = 32768
    p = 5
    r = 1
    bits = 400
    c = 3
    resolution = 3
    bitsInSpecialPrimes = 0
    skHwt argument = 0
    bootstrappable = true
    mvec = [32768]
    build_cache = false
    alsoThick = false
    threads = 1
    deterministic NTL seed = 20261103

The c/skHwt/special-prime choices above are standard pinned-HElib canary settings only.
They are NOT claimed to reconstruct unpublished Aung artifact parameters.
Exact matched parameter/interface verification remains evidence Step 3.

Mandatory context assertions:

    phi(m) = 16384
    ord_m(5) = 8192
    physical slot count = 2
    rcData.e = 4
    rcData.ePrime = 1
    q_boot = 5^4 + 1 = 626
    temporary recryption plaintext space = 625.

## Evaluation keys

Generate exactly the matrices needed by the canary, not the full 8191-Frobenius family.

Method-1 Frobenius targets:
    p^(2^t) mod m, t=0,...,8.

Fused-recode Frobenius targets:
    p^j mod m, j=1,...,7.

RM10 direct targets:
    u_t=(m>>(t+1))+1, t=0,...,9
    =
    {16385,8193,4097,2049,1025,513,257,129,65,33}.

All are key0 -> key0 direct matrices under the pinned bootstrappable context.

Then call:
    SecKey::genRecryptData()

and use the ACTUAL returned recryptKeyID and ACTUAL stored recryptEkey.

Do not synthesize a replacement recryption-key ciphertext.

## Test-only instrumentation boundary

Allowed read-only test instrumentation:

1. expose:
       Ctxt::intFactor
   through a test-only const getter;

2. expose:
       PubKey::recryptEkey
   through a test-only const getter.

Do not alter:
- Ctxt arithmetic;
- rawModSwitch;
- key generation;
- newMakeDivisible semantics;
- recryptEkey sample;
- key-switch matrices.

For newMakeDivisible:
- either invoke the exact file-static helper from an internal test location; or
- copy the exact pinned helper logic into the canary byte-for-semantics.

No secret-key operation is allowed to create candidate runtime state.
Secret-key decryption is permitted only for correctness assertions/oracles.

## Deterministic plaintext input

Use two physical RMFE slots:

    slot +:
      (0,1,2,3,4)

    slot -:
      (4,3,2,1,0).

Use the already-fixed interpolation basis:

    ell_0=[1,50,340,260,599]
    ell_1=[0,4,204,314,104]
    ell_2=[0,622,161,623,469]
    ell_3=[0,418,206,522,104]
    ell_4=[0,156,339,156,599].

At application modulus5 encode:

    phi(e_i)=ell_i(X^16) mod5

inside each physical slot, then use EA_5.encode to form the global input plaintext.

## Stage A — five Method-1 projections

For each i=0,...,4:

1. build local theta_i mod5 from the closed-form trace dual;
2. encode identical local theta_i into both physical slots with EA_5.encode;
3. constant-multiply the common input;
4. evaluate the nine recursive Frobenius trace stages.

Require for every branch:

    ptxtSpace = 5
    keyID = 0
    common intFactor unchanged
    physical slot + decrypts to x_{i,+}
    physical slot - decrypts to x_{i,-}
    both slot values have zero nonconstant slot coefficients.

Acceptance:
    METHOD1_PROJECTIONS = PASS_5_OF_5.

## Stage B — sparse R8 merge

Let:

    Y=X^1024.

Form:

    A(c)=sum_{i=0}^4 Y^i c_i.

Require:

    ptxtSpace=5
    keyID=0
    common intFactor unchanged.

Decrypt the global plaintext modulo5.

Support must be contained exactly in:

    J_active =
      {0,1024,2048,3072,4096,
       8192,9216,10240,11264,12288}.

Additionally check all ten active coefficients against the two-slot closed form:

    b_i=(a_{i,+}+a_{i,-})/2 mod5
    c_i=(a_{i,+}-a_{i,-})/(2I) mod5
    I=182 mod5=2,

with:

    [X^(1024i)]A=b_i
    [X^(1024(i+8))]A=c_i.

Acceptance:
    SPARSE_R8_SUPPORT = PASS
    SPARSE_R8_COEFFICIENTS = PASS_10_OF_10.

## Stage C — ONE MultKey pre-raw prefix

Follow pinned thin-recryption source ordering after the omitted SlotsToCoeff:

1. canonicalize if needed;
2. remove special primes from the target set;
3. retain at most the first three ciphertext primes exactly as stock source does;
4. real modDownToSet;
5. reLinearize(recryptKeyID).

Require immediately before rawModSwitch:

    ptxtSpace=5
    keyID=recryptKeyID
    prime set = selected <=3 ciphertext primes.

### Turn-8 theoretical sufficient condition

Let E_in be the actual coefficient-L1 encryption error, computed by secret-key-only instrumentation
from the raw pre-reduction decryption representative.

Evaluate the exact Turn-8 sufficient ratio using:

    A_merge = 5*2^24
    K_625 <= 401679183790908.6
    K_5 <= 3213433470327.2688
    R_5 <= 671129600
    F_tau = 511*K_625 +255*R_5
    beta_raw=((2/3)*5*boundForRecryption)/626.

Require:

    [
      A_merge*(E_in/Q0)
      +5*F_tau/Q0
      +(R_5+K_5)/Q3
    ] / beta_raw
    < 1.

Record the numeric value.

### Independent actual pre-raw ratio

Using the exact secret-key raw decryption representative immediately before rawModSwitch,
compute a centered coefficient-L1 error E_pre_raw modulo Q3 and record:

    actual_l1_raw_ratio
      =
      (626/Q3)*E_pre_raw
      /
      ((2/3)*5*boundForRecryption).

Require:
    actual_l1_raw_ratio < 1.

### HElib tracked gate

Call:
    rawModSwitch(zzParts,626)

and compute the source tracked ratio exactly as recryption.cpp does.

Require:
    zzParts.size()==2
    tracked_raw_ratio <=1.

## Stage D — divisibility and common reconstruction

Apply exact newMakeDivisible semantics with:

    p^(e')=5
    q=626,

to both raw parts, then divide both by5.

Reconstruct from the ACTUAL stored recryptEkey:

    reconstruction = recryptEkey
    reconstruction.multByConstant(zzParts[1], exact_L1_bound_if_available)
    reconstruction.addConstant(zzParts[0], exact_L1_bound_if_available).

Require:

    ptxtSpace=625
    keyID=0
    intFactor=1
    primeSet=context.ctxtPrimes.

Let semantic reconstruction plaintext be P(X).

For t=0,...,15 define:

    z_t=[X^(1024t)]P mod625.

Low-digit carrier correctness requires:

    z_i mod5
      = [X^(1024i)]A
    z_{i+8} mod5
      = [X^(1024(i+8))]A

for i=0,...,4.

Acceptance:
    RECONSTRUCTION_LOW_DIGITS = PASS_10_OF_10.

Do NOT require canonical high 5-adic digits.

## Stage E — unnormalized RM10

Starting from reconstruction:

for t=0,...,9:
    tmp = current
    tmp.smartAutomorph(u_t)
    current += tmp

with u_t listed above.

Then:
    cleanUp().

Require:
    ptxtSpace=625
    keyID=0
    primeSet=ctxtPrimes.

Do NOT multiply by224.

## Stage F — fused 8-Frobenius recode

Use:

    phi_i=ell_i(X^16)

in the full outer ring and:

    D_j=sum_{i=0}^4 phi_i * sigma^j(Y^{-i}),
    j=0,...,7,
    sigma(X)=X^5.

Before ciphertext evaluation, independently regenerate all eight D_j in exact integer arithmetic
modulo:

    X^16384+1
    and 625.

Require for every j:

    support(D_j)=21
    Linf_centered(D_j)=311
    L1_centered(D_j)=2811.

Also require the canonical all-D_j encoding hash:

    SHA256
    7b0a2a5c004cd02c20d259dd444d0234e909ea93ba75d45ffd3e941392df3581

using the same canonical JSON sparse-dictionary encoding from Turn 7.

Evaluate:

    fused =
      D_0*rm
      +sum_{j=1}^7 D_j*sigma^j(rm).

Then:
    cleanUp().

Require:
    ptxtSpace=625
    keyID=0
    primeSet=ctxtPrimes
    intFactor=1 before final scalar normalization.

## Stage G — scalar-unit28 and exact oracle

Call:

    fused.multByConstant(28L).

Require:

    ptxtSpace=625
    keyID=0
    intFactor=67.

Construct an implementation-independent plaintext oracle only from the reconstruction plaintext P:

    O(P)
      =
      sum_{i=0}^4
        phi(e_i) *
        (
          z_i + z_{i+8} X^8192
        )
      mod (X^16384+1,625).

Decrypt fused semantically modulo625.

Require exact coefficient equality:

    fused_plaintext == O(P) mod625.

Acceptance:
    FINAL_EXACT_Z625_ORACLE = PASS.

Stop here.

DO NOT run DigitExtract.
DO NOT run Algorithm 4.
DO NOT benchmark.

## PASS criterion

The task returns:

    PASS_SMALL_CORRECTNESS_CANARY

iff ALL of the following pass in the same deterministic run:

    context parameter assertions
    METHOD1_PROJECTIONS = 5/5
    SPARSE_R8_SUPPORT
    SPARSE_R8_COEFFICIENTS = 10/10
    TURN8_THEOREM_RAW_RATIO <1
    ACTUAL_L1_RAW_RATIO <1
    HELIB_TRACKED_RAW_RATIO <=1
    RECONSTRUCTION_LOW_DIGITS = 10/10
    D_j support/Linf/L1 = (21,311,2811) for all j
    D_j aggregate SHA256 exact match
    RM10 state assertions
    fused-recode state assertions
    final intFactor=67
    FINAL_EXACT_Z625_ORACLE.

A first scientific assertion failure returns:

    FAIL_SMALL_CORRECTNESS_CANARY

with:
    first_failure_stage
    expected
    observed
    preceding state dump.

An infrastructure/build/dependency error returns:

    INFRA_BLOCKED

and MUST NOT be interpreted as candidate FAIL.

## Required raw artifacts

Persist unedited:

1. exact canary source;
2. minimal test-only HElib patch/diff;
3. compiler + CMake + NTL + GMP version record;
4. HElib git status and exact HEAD;
5. complete stdout/stderr;
6. result JSON;
7. SHA256 for every artifact.

Result JSON must include at least:

    task_id
    verdict
    helib_commit
    context parameters
    actual context e/ePrime
    exact prime sets at named stages
    ptxtSpace/keyID/intFactor at named stages
    Method-1 5 branch results
    sparse 10 coefficient comparison
    input actual L1 capacity
    Turn-8 theorem raw ratio
    actual pre-raw L1 ratio
    HElib tracked raw ratio
    reconstruction 10 low-digit comparison
    8 D_j invariant rows
    D_j aggregate SHA256
    final intFactor
    exact-Z625-oracle result.

No latency field is needed and no timer should be interpreted.

## Scientific state after issuing task

The task is fully specified and authorized but not executed in this Chat turn.

Therefore:

    NATIVE_EVIDENCE_STEP_2=PENDING
    CORRECTNESS_GATE=BLOCKED
    BASELINE_CORRECTNESS=PENDING
    SECURITY_GATE=PENDING
    VALUE_GATE=PENDING
    AUDIT_GATE=PENDING
    PAPER_READINESS=NOT_READY.

No candidate conclusion is changed.

## Next scientific action after execution

The next substantive research turn must independently audit the raw Step-2 artifacts.

If PASS:
- mark SMALL_CANARY=PASS;
- then, and only then, advance to Native evidence Step 3 exact parameter/interface verification.

If scientific FAIL:
- localize the first failed assertion;
- do not execute Step 3;
- decide whether the failure is a harness/type mismatch or a candidate correctness failure before redesign.

If INFRA_BLOCKED:
- retain Step 2 as pending and repair only the execution environment/provenance.
