# BOOT / B158 — Successor Research Turn 14 — Algorithm-4 u0 three-Fe certificate-capacity no-go

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

GitHub Notes read of the Turn-13 predecessor was attempted first and remained degraded.
The exact durable predecessor was recovered through Git at:

    findings/boot-successor-turn13-four-output-correction-map-shared-frobenius-closure-2026-11-03.md
    commit aacb6daf679d29b862bf4b70d97527e89ab050cc
    blob 722fc64969c87b3c632a7018b185d39f55211bc0.

The target Turn-14 path was checked absent before write.

The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Pinned HElib source:

    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Relevant pinned source facts rechecked:
- CMake HELIB_SP_NBITS override is legal only in [1,64];
- Context::ctxtPrimeSize requires target ciphertext-prime size >=30;
- PrimeGenerator::B=3, so every T-bit ctxt prime lies in [(7/8)2^T,2^T);
- bootstrappable buildModChain maps skHwt=0 to BOOT_DFLT_SK_HWT=120;
- DoubleCRT::scaleDownToSet performs plaintext-space-divisible coefficient rounding before division by the dropped-prime product.

## Why this turn is paper-level

Turn 13 repaired the candidate's Algorithm-4 front end and gives exact mutually consistent L0,L1,L2,L3 with large full-chain static margins.

The next paper-level correctness issue is not another linear map.
For e=4, Aung Algorithm 4 necessarily contains the chain:

    u_0,1 = F4(z)
    u_0,2 = F4(u_0,1)
    u_0,3 = F4(u_0,2)

all at plaintext space625.

These three states are NOT divideByP outputs.
They therefore require three sequential nonlinear lifting-polynomial evaluations before the final source schedule is complete.

Historical legacy work showed that a particular fixed-prefix coefficient-L1 proof failed during the second Fe.
That result was candidate-specific and used a much larger old entry envelope.

Turn 14 asks the stronger current-candidate question:

Can Turn 13's much tighter sparse-R8 entry envelope make the same deterministic total-raw coefficient-L1 proof architecture close the complete u0 three-Fe chain if modulus-down prefixes are chosen optimally between Fe evaluations?

## Closest prior / exact delta

Closest source prior:
- Aung Algorithm 4;
- Halevi-Shoup lifting polynomial;
- pinned HElib BGV modulus switching and multiplication.

Closest durable proof prior:
- the legacy fixed-prefix Fe coefficient-L1 analysis.

Current delta:
- use the new Turn-13 L0 absolute envelope;
- remove any particular fixed-prefix policy;
- permit an arbitrary descending sequence of source-valid ctxt-prime targets;
- derive an optimal certificate-capacity recurrence.

No novelty claim is added.

## Primary hypothesis

H14:
The current Turn-13 L0 certificate is sufficiently small that a proof-driven sequence of modulus-down targets can certify all three source-order u0 lifting-polynomial evaluations under the R2 reference profile using the existing deterministic coefficient-L1/mod-switch proof rules.

Falsifier:
prove that even the best possible modulus-target schedule under those rules loses more certified capacity than the entire bits=400 context can supply.

## 1. Exact F4 fact reused

Pinned/source-faithful lifting polynomial for p=5 is:

    F4(X)=X^5-5X^3+5X.

The existing source-faithful fixed-target evaluation certificate has nonnegative terms and contains the leading multiplication chain:

    A
    -> A^2
    -> A^3
    -> A^5.

Therefore for any certified input envelope A:

    E_F4_cert >= A^5

as a statement about the VALUE of this sufficient upper-bound expression.

Important:
this is NOT a lower bound on actual ciphertext error.
It is a lower bound on what the current deterministic certificate architecture itself must carry.

## 2. Generic mod-down certificate

Let a ciphertext before one Fe call have:
- modulus Q_prev;
- certified total centered raw-decryption coefficient-L1 envelope E_prev.

Choose ANY smaller valid ctxt-prime target Q.

The current source-derived real-BGV mod-down certificate is:

    A
      = (Q/Q_prev) E_prev + R.

At plaintext space625, using a ternary secret coefficient-L1 bound h:

    R(h)
      = (625/2) * phi(m) * (1+h)
      = 5,120,000 * (1+h),

for:

    phi(32768)=16384.

The use of 625/2=312.5 is a conservative exact-real envelope;
the source balanced rounding coefficient is never larger than ptxtSpace/2.

Define base-2 logs:

    q      = log2 Q
    q_prev = log2 Q_prev
    e      = log2 E
    e_prev = log2 E_prev
    r      = log2 R(h).

Since A is a positive sum:

    log2 A
      >= max(
            r,
            e_prev + q - q_prev
          ).

The Fe certificate therefore obeys:

    e
      >= 5 * max(
                   r,
                   e_prev + q - q_prev
                 ).

## 3. Certificate-capacity recurrence

Define certified capacity:

    d = q-e.

Before the Fe call:

    d_prev = q_prev-e_prev.

For ANY target q<=q_prev:

    d
      <= q - 5*max(r, q-d_prev).

Now maximize the right-hand side over all possible q.

Case 1:
    q-d_prev <= r.

Then:
    q <= d_prev+r

and:

    d <= q-5r
      <= d_prev-4r.

Case 2:
    q-d_prev >= r.

Then:

    d <= q-5(q-d_prev)
      = 5d_prev-4q.

Since q>=d_prev+r:

    d <= d_prev-4r.

Therefore, independently of the selected prefix:

    d_after_one_Fe
      <= d_before_Fe - 4r.                 (T14.1)

This is the BEST possible capacity evolution permitted by the current proof architecture.

The optimum occurs at the intuitive balance point where the scaled inherited term and fresh rounding floor meet.

## 4. Three-Fe necessary condition

The Algorithm-4 u0 chain has three sequential F4 evaluations at ptxtSpace625.

Iterating (T14.1):

    d_3
      <= d_0 - 12r.

BGV sufficient correctness at the end of each certified state requires:

    E < 0.48 Q.

Equivalently:

    d > log2(1/0.48).

Define:

    c48
      = log2(1/0.48)
      = 1.0588936890535685...

Thus a NECESSARY condition for this deterministic certificate architecture to close the full u0 chain is:

    d_0
      > 12r + c48.                         (T14.2)

This result already allows an arbitrary optimal modulus-down schedule.
Choosing another fixed prefix cannot beat it.

## 5. Universal upper bound on the bits=400 ctxt-prime modulus

Turn 13 uses the full-chain L0 certificate before Algorithm 4.

To test (T14.2) we need an upper, not lower, bound on log2(Q0).

Pinned HElib source:
- CMake permits HELIB_SP_NBITS H <=64;
- a successful ctxtPrimeSize build requires target T>=30;
- PrimeGenerator B=3 gives bit_loss=log2(8/7);
- ctxtPrimeSize computes:
      n=ceil(400/(H-bit_loss))
  and decreases T according to the pinned while-loop;
- addCtxtPrimes stops once accumulated bit length is >=399.5.

A complete finite evaluation of every integer:

    H=30,...,64

under the exact pinned source formulas gives:

    max n*T = 420,

attained only at:

    H=30,
    n=14,
    T=30.

For every such successful build:

    n*(T-bit_loss) >=400,

so at most n generated primes are required.
Every generated prime is strictly below 2^T.

Hence universally for a successful pinned bits=400 build:

    log2(Q0) < 420.                        (T14.3)

Minimal reproducibility code:

    import math
    b=math.log2(8/7)
    mx=0
    for H in range(30,65):
        n=math.ceil(400/(H-b))
        T=H
        while (10*(T-1)>=9*H
               and T-1>=30
               and ((T-1)-b)*n>=400):
            T-=1
        assert n*(T-b)>=400
        mx=max(mx,n*T)
    assert mx==420

No native prime values are assumed.

## 6. Current Turn-13 L0 certificate

Turn 13 gives:

    E_L0
      <=41,293,704,600,473,801,437,489

and:

    log2(E_L0)
      <=75.12833994098358.

Combining with (T14.3), the current certificate can have at most:

    d_0
      <420 -75.12833994098358
      =344.87166005901645 bits.            (T14.4)

This deliberately gives the proof architecture every possible advantage from HElib prime-chain overshoot.

## 7. R2 reference profile forces h=120

The pending R2 task itself remains unknown and untouched.

Its already-authorized context contract calls pinned bootstrappable buildModChain with:

    skHwt argument =0.

Pinned Context::buildModChain maps this to:

    BOOT_DFLT_SK_HWT
      =120.

The same context hwt is used for the ternary secret generated by SecKey::GenSecKey.

Therefore the R2 reference profile has:

    h=120.

Its ptxt625 mod-down certificate floor is:

    R_120
      =5,120,000*(1+120)
      =619,520,000,

so:

    r_120
      =log2(619,520,000)
      =29.206575616824043 bits.

The necessary three-Fe entry capacity from (T14.2) is:

    12*r_120+c48
      =351.5378010909421 bits.

But (T14.4) gives:

    d_0 <344.87166005901645 bits.

Deficit:

    >6.666141031925633 bits.

Equivalently, with the current Turn-13 L0 certificate the R2-profile deterministic proof would require:

    log2(Q0)
      >75.12833994098358
       +351.5378010909421
      =426.6661410319257 bits,

while pinned bits=400 source guarantees:

    log2(Q0)<420.

Therefore:

    NO modulus-down prefix schedule can close
    u_0,1,u_0,2,u_0,3

under the current deterministic total-raw coefficient-L1 + generic rounding proof architecture for the R2 h=120 reference profile.

## 8. General h threshold under the current entry certificate

Using the generous universal Q0<2^420 bound, condition (T14.2) can only possibly hold when:

    log2(5,120,000*(1+h))
      <
      (344.87166005901645-c48)/12
      =
      28.651063864163575.

This gives:

    h <81.33029467292565.

Hence:

    h>=82
      => impossible for this proof architecture

under the current Turn-13 L0 certificate and pinned bits=400 source envelope.

Examples:

    h=81:
      necessary capacity
      =344.80206629906394 bits
      (not ruled out by this necessary test)

    h=82:
      necessary capacity
      =345.01191541981007 bits
      >344.87166005901645

    h=120:
      necessary capacity
      =351.5378010909421 bits
      FAIL by >6.666 bits.

This does NOT establish sufficiency for h<=81.
It is only a necessary-condition boundary.

## 9. Why modulus-up cannot rescue the certificate

After a real modulus-down, one might ask whether re-adding dropped primes could restore room.

A pure BGV modulus-up/add-primes-and-scale operation scales both the ciphertext modulus and the inherited raw representative by the same added-prime product.

Therefore it does not increase:

    log2(Q/E).

It cannot recover any of the 4r certificate-capacity loss paid per Fe evaluation.

Thus restricting the optimization to descending target moduli is without loss for this certificate-capacity theorem.

## 10. What this result does and does NOT mean

This turn proves:

    FAIL_CURRENT_DETERMINISTIC_L1_ARCHITECTURE_FOR_FULL_U0_CHAIN
    under the R2 h=120 reference profile.

It does NOT prove:
- actual F4 ciphertext evaluation fails;
- Aung Algorithm4 is incorrect;
- the sparse-R8 candidate is incorrect;
- the pending R2 canary fails.

R2 stops before DigitExtract, so this theorem neither predicts nor modifies its result.

The obstruction is specifically the combination of:
1. total-raw coefficient-L1 propagation;
2. the generic source-level modulus-switch rounding envelope;
3. source-faithful sequential degree-5 Fe evaluation;
4. the h=120 reference profile.

Actual HElib noise may be dramatically below this worst-case certificate.
A tighter norm/rounding theorem or native/probabilistic DFR evidence can still support complete correctness.

## 11. Paper-first consequence

Further turns that merely:
- choose another prefix;
- use exact q mod625 residues;
- shrink K(q);
- tune public-unit aligners;

cannot close this deterministic proof architecture for h=120, because (T14.1) already optimizes over all q and ignores all positive K/public-constant terms.

Therefore those local loops should stop.

Credible reopen mechanisms are qualitatively different:

A. derive a materially tighter certified modulus-switch rounding envelope R;

B. replace coefficient-L1 propagation with a tighter certified norm that remains submultiplicative and source-compatible;

C. use a repeated-Fe representation/evaluation schedule whose certificate does not contain the same degree-5 capacity loss;

D. obtain native raw evidence plus a justified probabilistic/DFR analysis instead of claiming deterministic L1 closure.

No such redesign is attempted in this turn.

The candidate remains ACTIVE because this is not an actual-algorithm no-go and mandatory native evidence is still pending.

## Verdict

PASS_THREE_FE_CERTIFICATE_CAPACITY_RECURRENCE.
PASS_BITS400_UNIVERSAL_Q0_UPPER_BOUND_420.
FAIL_R2_H120_FULL_U0_DETERMINISTIC_L1_CLOSURE.
PASS_HWT82_AND_ABOVE_NECESSARY_NO_GO_FOR_CURRENT_CERTIFICATE.

OBSTRUCTION_CLASS:
    deterministic proof architecture,
    not actual ciphertext correctness.

STRICT_ALGORITHMIC_NO_GO:
    NO.

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

Do not modify, resubmit, or duplicate the background native task.

If BOOT-T11-R8-SMALL-CANARY-20261103-R2 becomes ready, its raw artifacts preempt the next free substantive turn for independent audit.

Otherwise do NOT spend another turn on prefix/residue/K-factor tuning for this L1 proof architecture.
Prefer one independent paper-level unit such as:
- bounded novelty/prior-art audit of the sparse-R8 + shared-four-output mechanism; or
- a genuinely different certified repeated-Fe norm/rounding route.

No benchmark.
