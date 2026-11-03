# BOOT / B158 — Successor Research Turn 8 — merged pre-raw Method-1 / rawModSwitch absolute-capacity gate

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
TURN PHASE: CONSTRUCTIVE_DESIGN
Native execution: NONE

## Authority / read-before-write

Primary GitHub Notes read was attempted first and failed with repository/file access degradation.
The user-supplied verified fallback authority is BBBINGW/memory HEAD=origin/main at:

    b46b0da8f010b5f6d525622484420f6edae4e280.

The target path was checked absent both at that authority ref and at current main before write.

Immediate durable predecessor:

    findings/boot-successor-turn7-dirtylift-e8-direct-coefficient-recode-envelope-2026-11-03.md
    verification commit b46b0da8f010b5f6d525622484420f6edae4e280
    blob 415cb4341b2eb526a47bc6c08a0d0a52494fa1e0.

Turn 7 supersedes the older generic E8 SlotToCoeff/CoeffToSlots construction. The canonical candidate entering this turn is:

    five Aung Method-1 projections tau_i
    -> A(c)=sum_i Y^i tau_i(c), Y=X^1024
       already sparse in the R8 coefficient basis
    -> ONE coefficient-domain MultKey
    -> unnormalized RM10
    -> fused 8-Frobenius RMFE recode
    -> scalar-unit 28 normalization
    -> existing Aung correction DigitExtract.

Relevant fixed durable prerequisites:
- Aung bits=400 / p=5,m=32768,w=512,k=5 binding:
  findings/boot-RMFE-postdivide-turn9-aung-bits400-w512-parameter-binding-gate-2026-11-03.md,
  blob 93b2cab9536d71e63fb2757ca42018af2bce48ae;
- Aung Method-1 common factor/source interface:
  findings/boot-RMFE-postdivide-turn19-slotstoctxts-common-factor-gate-2026-11-02.md,
  blob 50612d... (full blob recovered from authority during this turn);
- deterministic key-switch/mod-down coefficient-L1 envelopes:
  findings/boot-RMFE-postdivide-turn14-inverse-exit-cleanup-l1-envelope-gate-2026-11-03.md,
  blob c09d29185d9f3e0941d313fcc8af560eb488dfc6;
- HElib parameter binding for temporary recryption plaintext:
  findings/boot-RMFE-postdivide-turn8-exact-l1-guard-capacity-floor-gate-2026-11-02.md,
  blob 8d9d0ea97adabebe80e4bc0b3e7f93b1477c6d98.

Pinned HElib source:
    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Primary paper source inspected:
    Aung et al., ePrint 2025/350, cached mirror SHA256
    922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
    VERSION_UNVERIFIED.

No native result is inferred.

## Closest prior and exact delta

Aung Method 1 already computes each projection as

    tau_i(x)
      = (id+sigma^s)
        o (id+sigma^(2s))
        o ...
        o (id+sigma^((w/2)s))
        (theta_i x),

so w=512 gives exactly 9 recursive trace stages per branch and k=5 branches.

The candidate does NOT modify those projection maps. Its delta is that the five projected thin states
are monomial-shifted and merged BEFORE the ordinary coefficient-domain MultKey:

    A(c)=sum_{i=0}^4 Y^i tau_i(c),

rather than running five independent MultKey instances.

This turn adds no new primitive or novelty claim. It asks whether the 5-way merge destroys the
source HElib rawModSwitch correctness precondition.

NOVELTY_STATUS remains PREFLIGHT.

## One primary hypothesis

H8:
For the fixed p=5,m=32768,w=512,k=5,bits=400 source row, a provenance-complete deterministic
coefficient-L1 propagation through the five Method-1 projections and their sparse merge gives a
finite rawModSwitch input-capacity precondition that differs from one source Method-1 branch by
only the expected factor 5 (about 2.322 bits), with all source-sized fresh key-switch/mod-down
terms negligible at the published full-chain modulus.

Falsifier:
- the Method-1 public constants or trace recursion require an unbounded coefficient multiplier;
- full Frobenius evaluation requires an uncontrolled multi-hop key-switch path;
- the five-way merge introduces a nonlinear operation before rawModSwitch;
- or the resulting sufficient input-capacity threshold consumes the available source benchmark
  margin or cannot even satisfy HElib's own raw gate.

## 1. Exact Method-1 source shape

For each i, Aung Method 1 uses one public multiplier theta_i and nine maps

    z <- z + sigma^{2^t s}(z),  t=0,...,8.

At plaintext space 5, every public plaintext ring element has a degree<phi(m) balanced power-basis
representative with coefficients in {-2,-1,0,1,2}. Hence, without knowing the actual theta_i,

    ||theta_i||_1 <= 2*phi(m)
                  = 2*16384
                  = 32768
                  = 2^15.

Because m=32768 is a power of two, every outer automorphism X->X^u is a signed permutation of the
coefficient basis and preserves coefficient-L1 exactly.

The later monomials Y^i=X^(1024i) are also signed coefficient permutations, so the sparse merge
itself adds no multiplier amplification beyond summing the five branches.

## 2. Full Frobenius key path is one-hop under the source-faithful key contract

Pinned HElib addFrbMatrices calls add1Dmats4dim for the Frobenius dimension. That routine generates

    GenKeySWmatrix(1, p^j mod m, keyID, keyID)

for every 1<=j<ord_m(p) and sets the strategy to HELIB_KSS_FULL.

Thus every Frobenius power needed by the nine Method-1 trace stages has a direct matrix under the
full-Frobenius key contract; smartAutomorph does not need a multi-hop chain for these targets.

This is the same key family required by the source Method-1 baseline. Exact production key presence
must still be asserted in the later parameter/interface canary.

Important source correction discovered this turn:
GenKeySWmatrix called with its default plaintext-space argument in a bootstrappable context does NOT
generate the Frobenius matrices at p^r=5. It substitutes the larger recryption algebra plaintext
space

    context.getRcData().alMod->getPPowR() = 625

for the fixed candidate context.

Therefore the trace-stage fresh key-switch envelope must use the prior ptxtSpace-625 bound K_625.
It would be incorrect to divide every Frobenius key-switch term by 125.

By contrast, SecKey::genRecryptData explicitly generates the final key0 -> recryptKeyID matrix with

    ptxtSpace = p^r = 5,

so only that final pre-raw key switch uses the ptxtSpace-5 scaled envelope.

## 3. Deterministic fresh-error constants

Turn 14 established the source-sized coefficient-L1 normalized key-switch bound at plaintext 625:

    K_625 <= 401,679,183,790,908.6.

The bound is linear in the key-switch matrix plaintext multiplier p because RLWE1 contributes p*e.
The explicitly ptxtSpace-5 recrypt-key matrix therefore satisfies

    K_5 <= K_625 * 5/625
        <= 3,213,433,470,327.2688.

The same Turn-14 mod-switch argument gives, for a canonical two-part BGV ciphertext, rounding
coefficient magnitude at most ptxtSpace/2. Hence at plaintext space 5:

    R_5
      <= 2.5 * phi * (1+phi)
      = 671,129,600.

These are independent coefficient-L1 sufficient envelopes, not HElib floating noiseBound claims.

## 4. Exact nine-stage Method-1 recurrence

Let E_in be an actual coefficient-L1 error envelope of the input ciphertext at non-special modulus
Q_0.

After multiplication by theta_i:

    E_theta <= 32768 E_in.

The first Frobenius trace step starts on Q_0. Its direct key switch mod-ups the special-prime product
S and injects K_625. Normalize the output error by S. Then:

    e_1 <= 2 E_theta + K_625.

At every later trace stage the accumulator already carries S. smartAutomorph reLinearize first
drops S, injecting at most R_5, then mod-ups S and applies one direct Frobenius key switch, injecting
K_625. Addition with the untouched accumulator copy doubles the existing normalized error. Thus for
t=2,...,9:

    e_t <= 2 e_{t-1} + K_625 + R_5.

Solving exactly:

    e_9
      <= 512*32768*E_in
         +511*K_625
         +255*R_5

      = 2^24 E_in + F_tau,

where

    F_tau
      = 511*K_625 +255*R_5
      <= 205,258,234,055,202,294.6.

This is one Method-1 projection branch, normalized by S.

## 5. Five-way sparse merge

All five projected branches have the same plaintext space, common BGV factor, key ID and Q_0*S
prime set under the source contract.

Multiplication by Y^i is a coefficient-L1 isometry. Summing five branches therefore gives

    e_A
      <= 5*2^24 E_in + 5 F_tau.

Define

    A_merge = 5*2^24 = 83,886,080.

No nonlinear operation has occurred. This is the exact deterministic structural penalty of moving
from one Method-1 branch to the merged sparse carrier.

## 6. Propagation through the ONE MultKey pre-raw prefix

The merged trace state is already canonical under key0 and carries Q_0*S.

The source-faithful MultKey prefix first retains at most the first three ciphertext primes and drops
all others, including S, by real modulus switching. Let Q_3 be the retained non-special product.
Existing normalized error scales by Q_3/Q_0 and fresh rounding contributes R_5:

    E_after_down
      <= e_A * Q_3/Q_0 + R_5.

Then reLinearize(recryptKeyID) mod-ups S and uses the explicitly plaintext-5 key-switch matrix.
Normalizing again by S gives:

    E_pre_raw_bar
      <= e_A * Q_3/Q_0 + R_5 + K_5.

Pinned rawModSwitch returns the current error scaled by q/(Q_3*S). For m=2^15 the HElib powerful
basis norm factor is exactly 1. Therefore the raw noise estimate is bounded by

    noise_est
      <= q * [
           A_merge * E_in/Q_0
           + 5 F_tau/Q_0
           + (R_5+K_5)/Q_3
         ].

The source raw gate accepts when

    noise_est
      <= HELIB_MIN_CAP_FRAC * p^r * boundForRecryption,

with HELIB_MIN_CAP_FRAC=2/3 and p^r=5.

For this fixed HElib context the durable parameter audit gives

    e=4, e'=1, q=p^e+1=626,
    p^(e-e'+r)=625.

Thus define the dimensionless raw allowance

    beta_raw
      := ((2/3)*5*boundForRecryption)/626.

A sufficient absolute candidate condition is

    A_merge * (E_in/Q_0)
      +5F_tau/Q_0
      +(R_5+K_5)/Q_3
      < beta_raw.                                  (H8.1)

This is the complete pre-raw deterministic inequality for the current construction.

## 7. Source-derived lower bound on beta_raw without guessing secret-key Hamming weight

The exact Aung artifact does not publish the HElib secret-key Hamming weight, so this turn does NOT
guess it.

Two source-level bounds are available.

### 7a. Universal fallback

HElib defines

    boundForRecryption = 0.5 + scale*stdDevForRecryption.

Under the ordinary nonnegative recryption parameters this is at least 0.5. Therefore

    beta_raw >= ((2/3)*5*0.5)/626
             = 0.002662406815761448.

This bound alone is enough for the final conclusion.

### 7b. Stronger fixed-(e,e') inference

Pinned RecryptData::setAE selects e,e' by minimizing e-e' subject to its Appendix-A inequality.
The fixed context has final pair (e,e')=(4,1).

If pair (4,2) had satisfied the setAE inequality, it would have had smaller difference 2 instead of
3 and would have replaced (4,1). Hence (4,2) necessarily failed.

For p=5, r=1:

    frstTerm = 2*p^r+2 = 12,
    compute_fudge(25,625) = 1+1/625 = 1.0016.

Failure of (4,2) gives

    625
      < 2*(25*1.0016 + 12)*boundForRecryption,

so

    boundForRecryption
      > 8.43682505399568.

Consequently the fixed source-built context has

    beta_raw
      > 0.044924521054290095.

This inference depends only on the pinned setAE source plus the already-durable (e,e')=(4,1)
parameter binding; it does not assume an unpublished skHwt value.

## 8. Full-chain bits=400 instantiation

For the published bits=400 benchmark initialization, HElib addCtxtPrimes creates a full ciphertext
modulus with

    log2 Q_0 >= 399.5.

For the retained first three ciphertext primes, Context::ctxtPrimeSize never goes below 30 bits.
PrimeGenerator with B=3 guarantees each target-length prime is at least (7/8)*2^30.
Therefore a build-independent conservative floor is

    log2 Q_3
      >= 3*(30 + log2(7/8))
      = 89.42206476617281.

At these floors:

    5F_tau/Q_0
      <= 5.6206601238e-103,

and

    (R_5+K_5)/Q_3
      <= 3.87557581891741e-15.

Thus the dominant term in (H8.1) is the propagated input error, not fresh key-switch/mod-down error.

Let actual input capacity be

    C_in := log2(Q_0/E_in).

Using only the universal beta_raw floor 0.0026624068 gives the sufficient candidate condition

    C_in > 34.8749813477 bits.

Using the stronger fixed-(e,e') source inference gives

    C_in > 30.7982811616 bits.

For one unmerged Method-1 baseline branch, the same derivation replaces A_merge by 2^24 and
5F_tau by F_tau. The corresponding thresholds are:

    universal:
      C_in > 32.5530532528 bits;

    fixed-(e,e') source inference:
      C_in > 28.4763530667 bits.

Hence the structural five-way merge tightens the input-capacity requirement by

    log2(5) = 2.32192809488736 bits

up to an astronomically small correction from the 5-versus-1 projection fresh term at the
bits=400 full-chain modulus.

This is the quantitative paper-level answer to the pre-raw blocker.

## 9. Relation to the published capacity table

Aung's p=5,m=32768,w=512 correction/TnM table reports an initial HElib capacity of 391.1 and 369.2
after SlotsToCtxts.

Those are useful consistency/value context only. This turn does NOT reinterpret HElib's floating
tracked capacity as a certified actual coefficient-L1 bound.

The theorem above is instead an explicit sufficient condition on the ACTUAL input error E_in.
For any input satisfying that condition, the merged candidate reaches rawModSwitch inside the
source gate by deterministic coefficient-L1 propagation.

## 10. Constructive-design consequence

The previously missing merged pre-raw quantitative gate is closed at MATH/STATIC level.

The complete canonical construction is now specified through both sides of rawModSwitch:

    five Method-1 projections
    -> sparse R8 merge A(c)
    -> source MultKey pre-raw prefix
    -> ONE rawModSwitch/newMakeDivisible/reconstruction
    -> unnormalized RM10
    -> fused 8-Frobenius RMFE recode
    -> scalar-unit28 normalization
    -> Aung correction DigitExtract.

Turn 7 already provides a 323.31-bit independent pre-DigitExtract post-raw margin conditioned on
raw success. Turn 8 now supplies the missing sufficient raw-success input condition.

This does NOT prove:
- an actual production ciphertext always has C_in above the sufficient threshold;
- native execution of the merged raw path;
- exact runtime keyset/prime objects;
- complete Algorithm-4 nonlinear noise/DFR;
- matched baseline correctness;
- security/value/audit gates.

Therefore PAPER_READY remains false.

## Verdict

PASS_MERGED_METHOD1_ABSOLUTE_TRACE_ENVELOPE.
PASS_FULL_FROBENIUS_ONE_HOP_SOURCE_CONTRACT.
PASS_CORRECTED_FROBENIUS_K625_BOOKKEEPING.
PASS_MERGED_PRERAW_RAWMODSWITCH_STATIC_GATE.
PASS_SOURCE_INPUT_CAPACITY_THRESHOLD.

Fixed-(e,e') sufficient input capacity:
    >30.7982811616 bits.

Universal source-floor sufficient input capacity:
    >34.8749813477 bits.

Relative to one Method-1 branch:
    +2.3219280949 bits structural merge requirement.

The candidate remains ACTIVE.

CONSTRUCTIVE_DESIGN is complete enough to advance the next substantive turn to CORRECTNESS_GATE.
No performance claim is authorized.

## Next decisive test

Native evidence order now becomes binding.

The next test should be a SMALL correctness canary, not a benchmark and not a full candidate run:

1. instantiate the pinned p=5,m=32768,bits=400 context and full Frobenius matrices;
2. encrypt deterministic two-physical-slot RMFE inputs with an input state satisfying the derived
   raw-capacity precondition;
3. execute the five Method-1 projections, sparse Y^i merge and the ONE MultKey pre-raw path;
4. assert exact primeSet/keyID/ptxtSpace/intFactor states and rawModSwitch noise ratio <=1;
5. continue through RM10 + fused recode + scalar-unit28;
6. decrypt before DigitExtract and compare exactly modulo625 with the direct RMFE scalar oracle.

Stop there. Do not benchmark and do not enter full Algorithm4 until this small canary passes.

If the canary contradicts the static interface or raw gate under the exact pinned parameters, mark
CORRECTNESS_GATE FAIL/BLOCKED and investigate that specific mismatch before any broader redesign.
