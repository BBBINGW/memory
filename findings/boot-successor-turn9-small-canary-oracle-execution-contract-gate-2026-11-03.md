# BOOT / B158 — Successor Research Turn 9 — small-canary oracle / execution-contract gate

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
Native execution: NOT OBTAINED

## Authority / read-before-write

GitHub Notes was attempted first. Existing-file read remains degraded; the target path was absent through both Notes and repository fetch before write.

Immediate logical predecessor:
- `findings/boot-successor-turn8-merged-preraw-rawmodswitch-capacity-gate-2026-11-03.md`
- current repository blob `841926623a4d0acb240d1cfb3610fc0c054e0889`.

Turn 8 completed the static constructive design and left Native evidence Step 2 as the mandatory next gate:
a small p=5,m=32768,bits=400 correctness canary through
Method-1 projections -> sparse R8 merge -> ONE MultKey -> RM10 -> fused recode -> scalar-unit28,
stopping before DigitExtract.

No benchmark or Algorithm-4 execution is performed here.

## Infrastructure attempts — NOT scientific evidence

The current local container was checked for a reusable native workspace:
- no HElib checkout;
- no BBBINGW/memory local clone;
- compiler/CMake/GMP available;
- NTL headers/library unavailable;
- ordinary container DNS cannot reach GitHub.

A bounded alternative was attempted: create a canary source/workflow in `BBBINGW/memory` and use a GitHub Actions runner.
The general GitHub contents write returned:

    403 Resource not accessible by integration

for both the proposed source and CMake file.

GitHub Notes can still write permitted `findings/` files.

These facts only explain why the native canary could not run in this turn.
They are NOT PASS/FAIL evidence about the candidate.

## One primary correctness hypothesis

H9:
The small-canary acceptance condition from Turn 8 can be made exact and source-faithful without requiring unpublished Magma artifacts or imposing an invalid canonical-Z625 requirement.

Specifically:
1. the deterministic p=5,w=512 interpolation RMFE already fixed in durable BOOT state determines the Method-1 projection constants analytically;
2. the candidate's pre-DigitExtract output should be compared to an exact Z625 oracle derived from the candidate reconstruction plaintext, while only the retained reconstruction coefficients are required to agree with the original sparse carrier modulo5.

Falsifier:
- the Method-1 projection constants cannot be reconstructed from the fixed interpolation RMFE;
- the proposed trace-dual does not evaluate f(x_i);
- arbitrary high 5-adic digits invalidate an exact plaintext recovery oracle;
- or no exact oracle exists independently of the ciphertext RM10/fused-recode implementation.

## Closest source mechanism and exact delta

Aung ePrint 2025/350 Theorem 1 constructs the interpolation RMFE using:

    E1: polynomial f -> (f(x_1),...,f(x_k))
    E2: polynomial f -> f(xi)
    phi = E2 o E1^{-1}
    psi = E1' o E2^{-1}.

For finite evaluation points, the i-th Method-1 projection is therefore literally:

    tau_i(f(xi)) = f(x_i).

Aung Proposition 4 / Method 1 represents this functional as a relative trace:

    tau_i(a) = sum_{j=0}^{w-1} sigma^j(theta_i a)

for the current base G=Z_{5^e} and w=512.

The candidate-specific delta in this turn is NOT a new map.
It is an exact closed form for the already-required theta_i and an exact native-canary oracle for the surviving sparse-R8 construction.

NOVELTY_STATUS remains PREFLIGHT.

## 1. Fixed deterministic RMFE instance is sufficient

The previously persisted deterministic instance is:

    S = Z/625Z
    G' = S[xi]/(xi^512 + 182)
    xi = X^16

inside the HElib physical slot ring

    GR(625,8192) = S[X]/(X^8192 + 182).

Evaluation points are:

    x_i in {0,1,2,3,4}.

The Lagrange basis polynomials are:

    ell_0=[1,50,340,260,599]
    ell_1=[0,4,204,314,104]
    ell_2=[0,622,161,623,469]
    ell_3=[0,418,206,522,104]
    ell_4=[0,156,339,156,599]

and:

    phi(e_i) = ell_i(xi).

Thus no Magma artifact is needed to define the exact Method-1 projection on this fixed source-conforming instance.

## 2. Closed-form trace-dual for Method-1 projections

Let:

    M(T)=T^512+182.

In S, the relation is:

    xi^512 = -182 = 443 mod625.

Newton sums for M give:

    Tr(1)=512,
    Tr(xi^r)=0 for 1<=r<=511,
    Tr(xi^512)=512*443=566 mod625.

Exact inverses are:

    512^{-1} mod625 = 448,
    566^{-1} mod625 = 286.

For evaluation point x in {0,1,2,3,4}, define:

    theta_x
      = 448
        + sum_{j=1}^{511} 286*x^j*xi^(512-j)
        mod625.

Then for every power-basis element xi^j, 0<=j<=511:

- j=0:
      Tr(theta_x)=448*512=1;
- j>=1:
      the only nonzero trace term is theta coefficient at xi^(512-j), so
      Tr(theta_x xi^j)
        =286*x^j*Tr(xi^512)
        =x^j.

Therefore for every f of degree<512:

    Tr(theta_x f(xi)) = f(x).

This is exactly the Method-1 projection functional tau_x.

Independent exact arithmetic verification in this turn checked all:

    5 * 512 = 2560

evaluation/power-basis pairs over Z625.

Result:

    PASS 2560/2560.

It also verified:

    ell_h(x_i)=delta_{i,h}

for all 25 Lagrange-basis pairs.

Canonical coefficient-vector SHA256 values for theta_x over Z625, encoded as JSON length-512 coefficient arrays, are:

    x=0:
    221cee3ff8ea743c07f97c2f7984dba3a2f9b107fcc3e05645bfb8cfc394e555

    x=1:
    3ff1176a1dd90bac95485a06cf242379fefbba4dc6d0a7cefbaf148d2e2f37f8

    x=2:
    b909da5c78502ecb33c84e712e7e403c19e6e007578e179cfcc2a09a0a2a18a1

    x=3:
    829051696b328b326975ea1f90c358ade05bec835670ef6ee92b2a95b87804dc

    x=4:
    57de7e44a4ede0fbfff8913fbdb90b9d69691054089c3cd836398e9fcd509d0c

At application plaintext space5 these reduce to:

    theta_x mod5
      = 3 + sum_{j=1}^{511} x^j xi^(512-j).

Thus the small canary can build exact Method-1 projection constants directly in code.

## 3. Turn-8 canary oracle needed one correction

Turn 8 informally requested:

    decrypt immediately before DigitExtract
    and require exact Z625 equality with the direct RMFE scalar oracle.

This phrase is ambiguous if interpreted as equality with the canonical input integers 0,...,4.

That would be WRONG.

The source Algorithm-4 theorem and the durable Turn-7 construction allow the MultKey reconstruction to produce arbitrary lifts:

    a_i' in Z625

provided:

    a_i' == a_i mod5.

The high p-adic digits before DigitExtract are exactly what DigitExtract is designed to remove.
Therefore a native canary must NOT fail merely because the reconstructed values are not canonical small lifts.

This does not change the candidate theorem; it fixes the test oracle.

## 4. Correct two-layer small-canary oracle

Let the candidate reconstruction ciphertext, immediately after:

    rawModSwitch
    -> newMakeDivisible
    -> divide
    -> recryptEkey reconstruction

decrypt semantically modulo625 to an outer-ring plaintext:

    P(X).

Define the retained R8 coefficients:

    z_t := coeff_{X^(1024t)} P,
    t=0,...,15.

### Layer A — low-digit MultKey correctness

Let A_5(X) be the sparse merged plaintext before MultKey, decrypted modulo5.

The ten active coefficients must satisfy:

    z_i mod5
      = coeff_{X^(1024i)} A_5,
      i=0,...,4,

and

    z_{i+8} mod5
      = coeff_{X^(1024(i+8))} A_5,
      i=0,...,4.

This is the exact semantic requirement for the ONE MultKey carrier.
No equality of high 5-adic digits is required.

### Layer B — exact Z625 recovery correctness

Construct, entirely in plaintext arithmetic:

    O(P)
      = sum_{i=0}^4
          phi(e_i) *
          ( z_i + z_{i+8} X^8192 )
      mod (X^16384+1,625).

Turn 7 proves:
- unnormalized RM10 contributes scale1024;
- the fused T8 recode contributes scale8;
- scalar-unit28 satisfies

      28*(1024*8)=1 mod625.

Hence the candidate ciphertext after:

    unnormalized RM10
    -> fused 8-Frobenius recode
    -> scalar-unit28

must decrypt EXACTLY modulo625 to:

    O(P).

This is an exact Z625 equality and is independent of the ciphertext implementation of RM10/recode:
the oracle uses only the reconstruction plaintext coefficients and public phi(e_i).

Therefore the native acceptance condition is:

    PASS_LOW_DIGIT_10_OF_10
    AND
    PASS_EXACT_Z625_PLAINTEXT_ORACLE.

This accepts valid arbitrary lifts and still detects any RM10/recode/routing/normalization error.

## 5. Required native state assertions

A source-faithful small canary must additionally assert:

Initial application ciphertext:
    ptxtSpace=5
    keyID=0
    common source intFactor

After each Method-1 projection:
    ptxtSpace=5
    keyID=0
    decoded two physical slots are exactly the expected base-ring scalars

After sparse Y^i merge:
    ptxtSpace=5
    keyID=0
    plaintext support modulo5 is contained in
      {0,1024,2048,3072,4096,
       8192,9216,10240,11264,12288}

Before rawModSwitch:
    mod-down retains at most first three ciphertext primes
    reLinearize(recryptKeyID) succeeds
    ptxtSpace=5
    keyID=recryptKeyID

Raw gate:
    HElib tracked raw noise ratio <=1
    and the independent actual coefficient-L1 sufficient ratio from Turn 8 is <1

After common reconstruction:
    ptxtSpace=625
    keyID=0
    intFactor=1
    primeSet=ctxtPrimes

After RM10/fused recode cleanup:
    ptxtSpace=625
    keyID=0
    primeSet=ctxtPrimes

After scalar-unit28:
    ptxtSpace=625
    keyID=0
    intFactor=67

Then apply the two-layer oracle above and STOP BEFORE DigitExtract.

## 6. Minimal source patch / execution contract

The canary does not need a cryptographic redesign.

A minimal HElib test-only patch may expose read-only access to:

    PubKey::recryptKeyID
    PubKey::recryptEkey
    Ctxt::intFactor

or place the canary in an internal friend/test context.

It must reuse the EXISTING recryptEkey generated by SecKey::genRecryptData.
It must not:
- freshly encrypt a replacement recryption key;
- decrypt/re-encrypt an intermediate ciphertext;
- synthesize a surrogate ciphertext;
- modify rawModSwitch rounding;
- benchmark.

For newMakeDivisible, either:
- call the exact file-static source helper from an internal test; or
- copy that exact source logic byte-for-semantics into the canary harness.

The automorphism key set can be bounded to exactly what the canary needs:
- Method-1 Frobenius exponents j in {1,2,4,8,16,32,64,128,256};
- fused recode Frobenius exponents j in {1,...,7};
- ten direct RM10 automorphisms
      (m>>(t+1))+1, t=0,...,9;
- the source recrypt-key switch generated by genRecryptData.

Generating unused full 8191 Frobenius matrices is unnecessary for the correctness canary.

## 7. Scientific disposition

The canary itself has NOT RUN.

Therefore:

    NATIVE_EVIDENCE_STEP_2 = PENDING
    CORRECTNESS_GATE = BLOCKED.

However this turn closes two prerequisites that could otherwise produce a false or non-reproducible Step-2 result:

1. exact Method-1 projection constants are now source-derived and hashable;
2. the pre-DigitExtract acceptance oracle is now mathematically correct for arbitrary Z625 lifts.

This is correctness progress, not a native PASS.

No later evidence-order step is opened.

## Verdict

PASS_METHOD1_TRACE_DUAL_CLOSED_FORM.
PASS_METHOD1_2560_POWER_BASIS_CHECKS.
PASS_CANARY_ARBITRARY_LIFT_ORACLE_CORRECTION.
PASS_EXACT_Z625_RECOVERY_ORACLE_CONTRACT.
PASS_SMALL_CANARY_EXECUTION_SPEC.

NATIVE_SMALL_CANARY = NOT_EXECUTED.
CORRECTNESS_GATE = BLOCKED.
BASELINE_CORRECTNESS = PENDING.
NOVELTY_STATUS = PREFLIGHT.
PAPER_READINESS = NOT_READY.

## Next decisive test

Execute exactly the small canary specified above in a native environment containing:

    HElib acdb264e1a991eaee35fd8b3c31bebe9528c49a1
    NTL
    GMP

with p=5,m=32768,bits=400 and deterministic seed/input.

Acceptance requires, in one run:

    Method-1 projections: 5/5 exact scalar-slot PASS
    sparse R8 support: PASS
    actual Turn-8 raw sufficient condition: PASS
    HElib tracked raw ratio <=1
    reconstruction retained coefficients mod5: 10/10 PASS
    every fused D_j exact L1 =2811
    final exact Z625 plaintext oracle: PASS
    final intFactor=67

Stop before DigitExtract.
Do not benchmark.
Do not advance to exact parameter/interface verification until this canary actually executes and passes.
