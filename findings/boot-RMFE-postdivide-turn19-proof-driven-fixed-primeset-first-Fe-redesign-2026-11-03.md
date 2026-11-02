# BOOT / B158 — Research Turn 19/25 — proof-driven fixed-prime-set first-Fe redesign

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write

GitHub Notes reads remain degraded. Direct durable authority recovered:
- Turn17 first-Fe naturalPrimeSet gate;
- Turn18 retry infrastructure exhaustion;
- repository main before write: f0fcd0bdccc22c5bd5971ff2f68b28e8f93f1d8f.

Target path was checked absent before write.

## Why this turn is paper-level

Turn17 isolated the first nonlinear Algorithm4 Fe square as the exact point where the independent coefficient-L1 proof becomes conditioned on stock HElib naturalPrimeSet(). Turn18 established that native execution is currently unreachable. Repeating infrastructure probes or continuing source-only noise propagation would therefore be low-value.

The highest-information reversible redesign is to ask whether the naturalPrimeSet dependency is fundamental or merely a stock HElib policy artifact.

## Closest prior / exact delta

Closest implementation prior is pinned stock HElib Ctxt::multLowLvl/multiplyBy:
- for squaring, multLowLvl calls bringToSet(naturalPrimeSet());
- tensorProduct then performs the exact ciphertext tensor product;
- multiplyBy finally calls reLinearize().

Turn19 changes ONLY the prime-set selection policy for the first Algorithm4 Fe square. It does not change the polynomial F4, plaintext ring, key-switch matrices, secret key, evaluation keys, or Algorithm4 semantics.

No novelty CLEAR claim is made.

## Primary hypothesis

The Turn17 runtime prime-set obstruction is not fundamental: the first Fe square can be evaluated at a proof-driven fixed ctxt-prime prefix selected from public context data and the independent coefficient-L1 envelope, thereby eliminating reliance on HElib's heuristic naturalPrimeSet() while preserving exact BGV semantics and the existing key-switch resource set.

## Falsifier

FAIL if any of the following holds:
- no ctxt-prime prefix satisfies the Turn17 independent correctness inequality;
- fixed-prefix multiplication cannot be implemented without exposing secret-key material or adding a new key family;
- reLinearize silently replaces the fixed prefix using heuristic noise metadata;
- partial final key-switch digits are unsupported;
- or tensorProduct/intFactor semantics differ from stock multiplication at the same chosen modulus.

## 1. Define a proof-driven prefix selector

Let the Algorithm4-entry L0 ciphertext have full ctxt-prime modulus Q0 and independent centered pre-mod-p representative envelope E0.

From Turn16/17 conservative preflight:
    log2(Q0) >= 399.5
    E0 <= 1.1433532886831608e35
    R <= 83,891,200,000.

For every ordered prefix P_j of context.getCtxtPrimes(), define:
    q_j = product(P_j)
and exact context-derived:
    K_j = 8125*phi^2*(sum_i D_i(P_j))/S.

Choose:

    P* = shortest prefix P_j satisfying

    ((q_j/Q0)*E0 + R)^2 + K_j < 0.48*q_j.

This selector uses only:
- public Context prime sets;
- public key-switch digit partition;
- public special-prime product;
- the already-derived candidate-independent envelope constants.

It does NOT use:
- ciphertext secret data;
- HElib noiseBound;
- embeddingLargestCoeff;
- naturalPrimeSet();
- capacity().

## 2. P* provably exists

The complete ctxt-prime set itself is an allowed prefix, so set q=Q0.

Using the conservative full-chain key-switch bound:
    K_full <= 401,679,183,790,908.6,

the full-set left-hand side obeys:
    (E0 + R)^2 + K_full
with:
    log2(left) <= 232.92150915364357.

The full-set correctness threshold is:
    log2(0.48*Q0) >= 398.44110631094645.

Therefore the complete set satisfies the inequality with at least:
    165.51959715730285 bits
of conservative margin.

Hence P* always exists under the already-pinned bits_HElib=400 / Turn16 envelope assumptions.

This existence theorem is independent of prime granularity or the number of HElib ctxt primes.

## 3. Minimal HElib patch

tensorProduct is private, but multLowLvl/multiplyBy are Ctxt members. A minimal sibling API can therefore bypass only the adaptive set selection while reusing the exact stock arithmetic:

    void Ctxt::squareAtSet(const IndexSet& target)
    {
      assertTrue(target <= primeSet, "target not contained in current prime set");
      bringToSet(target);
      Ctxt tmp(pubKey, ptxtSpace);
      tmp.tensorProduct(*this, *this);
      *this = tmp;
      reLinearize();
    }

The exact implementation may keep this helper internal rather than public; the scientific contract is the same.

At Algorithm4 first Fe square call:

    x2 = x;
    x2.squareAtSet(P*);

in place of stock:

    x2 = x;
    x2.square();

for that one materialization.

## 4. Semantic parity with stock multiplication

Before tensoring, bringToSet(P*) uses ordinary BGV modulus switching and preserves the encrypted plaintext semantics with HElib's normal intFactor adjustment.

tensorProduct is exactly the same routine called by stock multLowLvl. For BGV it computes:

    intFactor_out
      = intFactor_in^2 * (q* mod ptxtSpace) mod ptxtSpace,

where q* is product(P*).

This is precisely HElib's stock BGV product convention.

The plaintext space remains625 and no new key is introduced.

Therefore fixed-set square and stock square at the same modulus q* have identical ciphertext algebra, intFactor semantics and key-switch target.

## 5. reLinearize does NOT reintroduce naturalPrimeSet

After tensorProduct the prime set is exactly P*, consisting only of ctxt primes.

Pinned reLinearize begins with dropSmallAndSpecialPrimes(). Its first branch is:

    if primeSet is disjoint from smallPrimes:
        modDownToSet(context.getCtxtPrimes()).

Since P* is already a subset of ctxtPrimes and contains no small/special primes, this call leaves P* unchanged.

The heuristic compensation branch is entered ONLY when smallPrimes are present.

Thus reLinearize cannot silently enlarge or shrink P* using HElib noiseBound before the key switch.

It then mod-ups by the standard special-prime set and performs the ordinary existing relinearization.

## 6. Partial digit intersections are explicitly supported

P* need not end on a key-switch digit boundary.

Pinned DoubleCRT::breakIntoDigits does:

    digitPrimes = context.getDigits().at(n);
    digitPrimes.retain(remainingPrimes);

and stops once remainingPrimes is empty.

Therefore a final partially populated digit is an explicit supported source path.

The existing key-switch matrix stores at least the full context digit count, so no new key-switch matrix or key family is needed.

## 7. Correctness theorem for the redesigned first square

Let q*=product(P*) and K*=K(P*). By definition of P*:

    E_down <= (q*/Q0)*E0 + R,

and:

    E_down^2 + K* < 0.48*q*.

tensorProduct followed by standard relinearization therefore remains inside the same BGV decryption-correctness boundary established in Turn17.

The proof is now static with respect to the candidate design: P* is selected by the proof inequality itself, not by a heuristic noise estimator.

Stock HElib noiseBound may still be tracked for implementation diagnostics, but it is no longer an assumption in this first-square correctness proof.

## 8. Optional simple guard

Turn17 proved the conservative scalar threshold:
    log2(q) > 73.63449463535464.

So an implementation may additionally assert:
    log2(q*) >= 74.

However the authoritative selector remains the exact prefix inequality, which is stronger and automatically adapts to the actual context digit/special-prime structure.

## 9. Scope

This redesign closes ONLY the first nonlinear Fe square.

It does not yet prove:
- the later x^3 construction;
- the final degree-5 combination;
- later Algorithm4 Fe evaluations;
- y-u factor harmonization;
- any divideByP boundary;
- final Recode or final DFR.

Those remain pending and should be approached using the same proof-driven fixed-set principle only if the next nonlinear gate warrants it.

## 10. Value/performance boundary

P* may contain more ctxt primes than stock naturalPrimeSet() would choose, so this repair can increase multiplication/key-switch cost.

No latency/value claim is permitted until native correctness and matched benchmarking.

The point of this turn is correctness architecture: it shows the Turn17 obstruction is a removable implementation-policy artifact rather than an algebraic no-go.

## Verdict

PASS_PROOF_DRIVEN_PREFIX_EXISTENCE
PASS_FIXED_SET_FIRST_FE_SEMANTIC_PARITY
PASS_PARTIAL_DIGIT_KEYSWITCH_COMPATIBILITY
PASS_FIRST_FE_NATURALPRIMESET_OBSTRUCTION_REPAIR

FIRST_FE_FIXED_SET_SELECTOR:
    P* = shortest ctxt-prime prefix satisfying
    ((q/Q0)*E0 + R)^2 + K(q) < 0.48*q

FULL_SET_EXISTENCE_MARGIN:
    >= 165.51959715730285 bits

NEW_KEY_FAMILY:
    NO

NEW_SECURITY_ASSUMPTION:
    NO

NATIVE_EXECUTION:
    NOT_OBTAINED

RECOVERY_CANARY:
    NOT_EXECUTED

CORRECTNESS_GATE:
    BLOCKED

BASELINE_CORRECTNESS:
    PENDING

SECURITY_GATE:
    PENDING

VALUE_GATE:
    PENDING

AUDIT_GATE:
    PENDING

PAPER_READINESS:
    NOT_READY

## Next decisive test

Mandatory native evidence order still requires the frozen Step2 recovery canary first when execution becomes available.

After Step2 PASS, Step3 must instantiate P* from the actual context, assert the exact selector inequality, execute the fixed-set first Fe square, and compare exact decrypt/plaintext semantics against stock Fe evaluation on a correctness-safe native path before any later Algorithm4 gate or performance claim.