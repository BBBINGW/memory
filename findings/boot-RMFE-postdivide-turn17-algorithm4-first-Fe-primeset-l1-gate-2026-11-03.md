# BOOT / B158 — Research Turn 17/25 — Algorithm4 first-Fe prime-set / L1 gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al. ePrint 2025/350 / PKC 2025

## Read-before-write / provenance

GitHub Notes reads remain degraded. Durable context was recovered by direct GitHub fetch from BBBINGW/memory main at:

    7d01fbd092135acd140bb2c08e5c0e54230028fd

Immediate prerequisite:
- Turn16 exact rho443 / L0-L3 coefficient-L1 Algorithm4-entry envelope.

The target path was checked absent before write.

No native execution occurred. Mandatory Step2 recovery canary remains unexecuted.

## Why this turn matters

Turn16 reaches Algorithm4 entry with a large independent coefficient-L1 bound, but Algorithm4 immediately evaluates the Halevi-Shoup lifting polynomial Fe on L0. This is the first nonlinear ciphertext-ciphertext multiplication after the current candidate-specific linear machinery.

The paper-first question is therefore not another linear interface fact. It is whether the independent source-level envelope can cross even the FIRST nonlinear Fe multiplication without relying on HElib's heuristic noise metadata or runtime-selected prime set.

## Closest prior / exact delta

Aung Algorithm4 is source prior art and inherits Halevi-Shoup digit extraction. HElib's pinned extractDigits/polyEval implementation is the concrete evaluation prior.

Turn17 adds no novelty claim. Its exact delta is candidate-specific:
- instantiate the exact p=5,e=4 lifting polynomial;
- identify the first ciphertext multiplication actually executed by pinned polyEval;
- derive an estimator-independent sufficient correctness inequality for that multiplication;
- test whether pinned source alone guarantees the required multiplication modulus.

## Primary hypothesis

Turn16's independent coefficient-L1 correctness envelope can be propagated through the first Fe nonlinear multiplication from source alone, without requiring runtime prime-set evidence.

## Falsifier

FAIL the source-only form if the first multiplication's chosen ciphertext modulus q is runtime/heuristic dependent and pinned source provides no lower bound strong enough to satisfy the independent correctness inequality.

## 1. Exact lifting polynomial for p=5,e=4

Pinned HElib buildDigitPolynomial computes a degree-p polynomial by interpolating:

    z - z^p

at balanced representatives z in {-2,-1,0,1,2}, modulo p^e=625, and then adds X^p.

For p=5:

    z-z^5 = [30,0,0,0,-30]

on z=[-2,-1,0,1,2].

The unique degree<=4 interpolation is:

    5X - 5X^3.

Hence the exact pinned lifting polynomial is:

    F4(X) = X^5 - 5X^3 + 5X.

This is exactly of Aung's source form X^p+pG(X).

## 2. Pinned polyEval first nonlinear operation

For degree5 and default k selection, pinned polyEval chooses k=1.

Tracing the exact Paterson-Stockmeyer recursion gives:

    F4(x) = (x^3 - 5x - 1) * x^2 + (x^2 + 5x),

with:

    x^3 - 5x - 1 = x*(x^2-6) + (x-1).

Thus the first ciphertext-ciphertext multiplication needed by Fe is the materialization of:

    x^2.

DynamicCtxtPowers computes this via Ctxt::multiplyBy on x with itself.

## 3. Important terminology refinement

Pinned HElib BGV noiseBound and debugging compare against the canonical norm of the centered pre-plaintext-reduction decryption representative pp=<sk,ct> mod Q, not against a separately isolated residual-error polynomial.

Therefore the independent Turn13-16 coefficient-L1 quantities are most precisely interpreted as:

    total centered pre-mod-p decryption-representative envelopes.

This refinement does not change any earlier inequalities. It is exactly the quantity needed for:
- HElib isCorrect;
- BGV tensorProduct, whose tracked bound multiplies;
- the present independent multiplication proof.

## 4. Mod-down before the first square

Let the Turn16 L0 input state have:

    old modulus Q0,
    independent representative bound E0.

Current source-sized preflight gives:

    log2(Q0) >= 399.5
    E0 <= 1.1433532886831608e35.

Before squaring, pinned multLowLvl calls:

    bringToSet(naturalPrimeSet()).

Let the selected multiplication modulus be q.

Using Turn14's independent BGV modulus-switch rounding envelope:

    R <= 83,891,200,000,

the centered representative after mod-down satisfies:

    E_down <= (q/Q0)*E0 + R.

This statement is independent of HElib's floating embedding norm estimator.

## 5. Square + relinearization inequality

Pinned tensorProduct for BGV sets the tracked product bound to the product of its two operand bounds. Algebraically, the centered decryption representative of the tensor product is the product of the two input representatives modulo q, so coefficient/canonical submultiplicativity gives the same independent sufficient envelope:

    E_square_raw <= E_down^2.

Then reLinearize temporarily adds special primes and key-switches. Normalize Turn14's exact key-switch bound by the special-prime product. Let:

    K(q) = 8125*phi^2*(sum_i D_i(q))/S.

Because q uses a subset of ctxtPrimes, every retained digit product D_i(q) is at most its full-chain value. Thus Turn14's conservative source-sized preflight remains valid:

    K(q) <= 401,679,183,790,908.6.

At the relinearized modulus q*S, a sufficient decryption-correctness condition is:

    S*E_down^2 + S*K(q) < 0.48*q*S.

Equivalently:

    E_down^2 + K(q) < 0.48*q.

This is the exact runtime acceptance inequality for the first nonlinear square under the independent envelope.

## 6. Conservative scalar threshold

Substitute only the source-sized worst-case values:

    Q0 >= 2^399.5
    E0 <= 1.1433532886831608e35
    R <= 83,891,200,000
    K <= 401,679,183,790,908.6.

The inequality:

    ((q/Q0)*E0 + R)^2 + K < 0.48*q

has its relevant lower crossing at:

    log2(q) = 73.63449463535464.

The second crossing is far above the available chain and is irrelevant here.

Therefore a simple sufficient runtime assertion is:

    log2(q) >= 74.

At q=2^74, the left/right ratio is at most about:

    0.7762.

So two ordinary single-word ctxt primes would normally provide ample room; however cardinality and exact prime sizes are runtime facts, not a pinned source contract for this state.

## 7. Source does NOT guarantee the required 74-bit floor

Pinned ModuliSizes::init explicitly inserts prefix sets of the ctxt-prime chain.

On its first ctxt-prime iteration the prefix s contains exactly one ctxt prime, so a singleton ctxt-prime set is a valid entry in the modulus-size table.

naturalPrimeSet calls ModuliSizes::getSet4Size using a target interval computed from:

    current log(modulus)
    current HElib noiseBound
    modSwitchAddedNoiseBound.

The first two of these depend on the current runtime state, and HElib noiseBound is itself a heuristic/high-probability estimator rather than the independent certified envelope.

getSet4Size has no assertion:

    cardinality >= 2

and no assertion:

    log2(product(targetPrimeSet)) >= 73.6345.

Consequently the pinned source permits a one-ctxt-prime candidate whenever its heuristic target interval selects it. The source-only correctness theorem cannot replace the actual selected q by a guaranteed >=74-bit modulus.

This is a genuine boundary of the independent static proof, not a correctness counterexample to the candidate.

## 8. Why this does not kill Algorithm4

The exact native q may be much larger than the sufficient threshold.

Also, the 73.6345-bit threshold deliberately uses:
- the worst h<=phi cleanup envelope;
- the full-chain conservative K bound;
- the Turn16 common worst-case L0 envelope;
- no exact native cancellation or tighter mod-switch delta.

For example, smaller actual secret-key Hamming weight materially reduces the independent cleanup envelope. But Aung's exact skHwt remains UNKNOWN and must not be assumed.

Therefore the correct classification is:

    source-only deterministic propagation: FAIL / not closed
    runtime-conditioned first-square theorem: PASS
    candidate correctness: still UNKNOWN pending native evidence.

## 9. Exact Step3 runtime oracle

After mandatory Step2 PASS, production Step3 must instrument the first Algorithm4 Fe evaluation before any timing claim.

Record:

    Q0 = product(input primeSet)
    E0_runtime = exact accumulated independent L1 envelope from prior stages
    targetSet = input.naturalPrimeSet()
    q = product(targetSet)
    actual context.getHwt()
    S = product(specialPrimes)
    D_i(q) = product(context digit i intersect targetSet).

Compute:

    R_runtime = 312.5*phi*(1 + actual secret coefficient-L1 bound)

using the source ternary-secret structure; a coarser phi bound remains valid.

Compute:

    K_runtime = 8125*phi^2*(sum_i D_i(q))/S.

Hard acceptance assertion:

    ((q/Q0)*E0_runtime + R_runtime)^2 + K_runtime < 0.48*q.

A simpler conservative sufficient assertion is:

    log2(q) >= 74

under the current Turn16/14 source-sized maxima.

Then execute the square and record:

    selected primeSet
    ptxtSpace
    intFactor
    isCorrect()
    exact debug decrypt equality.

Failure of the exact inequality is:

    FAIL_ALGORITHM4_FIRST_FE_INDEPENDENT_L1_GATE.

## 10. Paper-level consequence

Turn13-16 established an estimator-independent chain through Algorithm4 entry. Turn17 shows exactly where static propagation becomes runtime-conditioned:

    first Fe ciphertext square.

The blocker is not the algebraic lifting polynomial, arbitrary-lift theorem, factor unit-ness, or divideByP semantics. It is HElib's runtime naturalPrimeSet choice before nonlinear multiplication.

Thus no more source-only deterministic L1 propagation through Algorithm4 should be claimed without pinning the actual prime-set trajectory.

## Verdict

PASS_EXACT_F4_POLYNOMIAL_X5_MINUS5X3_PLUS5X
PASS_FIRST_FE_SQUARE_RUNTIME_L1_INEQUALITY
PASS_FIRST_FE_QBITS_74_SUFFICIENT_PREFLIGHT
FAIL_SOURCE_ONLY_ALGORITHM4_FIRST_FE_L1_PROPAGATION
REQUIRE_NATIVE_FIRST_FE_PRIMESET_ORACLE

FIRST_FE_RUNTIME_CONDITION:
    ((q/Q0)*E0 + R)^2 + K(q) < 0.48*q

CONSERVATIVE_Q_THRESHOLD_BITS:
    73.63449463535464

SIMPLE_SUFFICIENT_RUNTIME_ASSERTION:
    log2(q) >= 74

INDEPENDENT_L1_STATIC_CLOSURE_ENDS_AT:
    L0-L3 / Algorithm4 entry

NATIVE_EXECUTION:
    NOT_OBTAINED

RECOVERY_CANARY:
    NOT_EXECUTED

CORRECTNESS_GATE:
    BLOCKED

BASELINE_CORRECTNESS:
    PENDING

NOVELTY_STATUS:
    PREFLIGHT

SECURITY_GATE:
    PENDING

VALUE_GATE:
    PENDING

AUDIT_GATE:
    PENDING

PAPER_READINESS:
    NOT_READY

## Next decisive test

The mandatory evidence-order action remains execution of the frozen recovery-only canary.

After Step2 PASS, Step3 must include the first-Fe naturalPrimeSet oracle above. Only if that exact runtime inequality passes may the independent coefficient-L1 proof be extended into Algorithm4. No timing or final DFR conclusion is authorized from this source-only turn.