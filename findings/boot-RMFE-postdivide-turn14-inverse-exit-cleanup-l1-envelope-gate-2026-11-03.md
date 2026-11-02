# BOOT / B158 — Research Turn 14/25 — pure-inverse exit cleanup / coefficient-L1 envelope gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes reads remain degraded and return empty objects. Durable context was recovered from
BBBINGW/memory main at:

    26bb6f66e5e8495f8d43010b4dcbdc81969c0a23

Immediate prerequisites:
- Turn13 independent coefficient-L1 shared-reconstruction envelope;
- historical Turn16 pure normal_basis=false Z625 inverse realization;
- historical Turn17 pure-inverse keyset parity;
- Turn4 special-prime/control-flow path audit.

The target path was checked absent before write.

No native execution occurred. The frozen Step2 recovery-only canary remains unexecuted.

## Why this turn is necessary

Turn13 gives an estimator-independent coefficient-L1 error envelope immediately after the one
shared reconstruction:

    E_shared <= 6,957,728,854,835,200
    log2(Q/E_shared) >= 346.872462 bits.

The production pipeline then applies:

    EvalMap(... invert=true, normal_basis=false)
    -> scalar-unit 28
    -> 17-call recovery.

The earlier construction implicitly treated the pure-inverse output as a recovery root on the
ordinary ctxt-prime set. That assumption was never source-proven.

Turn14 tests exactly whether:
1. the pure inverse exits on the recovery-canary-compatible prime set; and
2. Turn13's independent coefficient-L1 envelope can cross that boundary without falling back to
   HElib's non-certified floating FFT norm estimator.

## Closest implementation prior / exact delta

Closest implementation prior remains stock HElib EvalMap / BlockMatMul1DExec.

Turn16 proved the algebra/API realization of the pure inverse.
Turn17 proved the current order-2 + FULL-Frobenius keyset is already available at ptxtSpace625.

Turn14's exact candidate-specific delta is the EXIT STATE of this transform:
- primeSet;
- cleanup/mod-switch boundary;
- actual-error envelope.

No novelty claim is added.

## Primary hypothesis

The current construction:

    shared reconstruction
    -> pure inverse
    -> scalar-unit 28
    -> recovery

is already correctly normalized at the pure-inverse exit, or can be repaired by exactly one
source-faithful cleanup that preserves ptxtSpace/intFactor/plaintext semantics and still leaves a
large independent coefficient-L1 correctness margin.

## Falsifier

The unrepaired construction FAILS if EvalMap may return with special primes and there is no explicit
cleanup before the recovery root.

The bounded repair FAILS if:
- cleanUp cannot restore ctxtPrimes;
- cleanUp changes ptxtSpace or semantic intFactor unexpectedly;
- or the coefficient-L1 error bound after pure inverse + cleanup reaches the BGV correctness
  boundary.

## Minimal decisive test

Audit only the reachable pinned-source path:

    EvalMap::apply
    -> BlockMatMul1DExec::mul
    -> BasicAutomorphPrecon / smartAutomorph
    -> MulAdd / addCtxt
    -> cleanUp
    -> dropSmallAndSpecialPrimes
    -> modDownToSet / scaleDownToSet.

Then derive one conservative coefficient-L1 bound for the cleaned pure-inverse output.

## 1. Current pure inverse is a single block transform

For:

    mvec=[32768]
    phi(m)=16384
    d=ord_m(5)=8192
    nslots=2,

EvalMap has:

    nfactors=1
    matvec.length()=0.

Thus inverse EvalMap::apply executes only:

    mat1->mul(ctxt).

The BlockMatMul has:

    D=2
    d=8192
    strategy=-1.

So the pure inverse is exactly one 2-by-extension block transformation.

## 2. EvalMap has no exit cleanup

BlockMatMul1DExec::mul calls ctxt.cleanUp() at ENTRY.

But EvalMap::apply simply calls mat1->mul(ctxt) and returns.
There is no ctxt.cleanUp() after the block transform.

The default:

    fhe_test_force_hoist = 0

activates GeneralAutomorphPrecon according to the configured KS strategy. Current Turn17 resource
contract gives FULL Frobenius and FULL outer-order-2 resources.

BasicAutomorphPrecon::automorph constructs every nontrivial transformed result on:

    ctxt.primeSet | context.getSpecialPrimes().

It explicitly sets result->primeSet to that union before key switching.

MulAdd copies those transformed ciphertexts, multiplies by public constants and adds them into
accumulators. Ctxt::addCtxt matches prime sets by MOD-UP, not by automatically cleaning the operand.

Therefore once a nontrivial automorphism term enters an accumulator, the accumulator may remain on:

    ctxtPrimes | specialPrimes.

The current inverse matrix is nontrivial and consumes the Frobenius/outer resources identified in
Turn17.

Hence the source provides no postcondition that the EvalMap output primeSet equals ctxtPrimes.

Verdict for the unrepaired boundary:

    FAIL_ASSUMED_PURE_INVERSE_EXIT_CTXT_PRIMES.

## 3. Minimal repair: one explicit cleanUp after pure inverse

Canonical repaired sequence:

    pureInverse.apply(ctxt)
    -> ctxt.cleanUp()
    -> ctxt.multByConstant(28L)
    -> recovery.

At the pure-inverse exit, accumulated linear terms are under keyID0 after their automorphism /
key-switch operations. If the state is noncanonical, cleanUp first relinearizes.

After that, this path contains:
- ctxtPrimes;
- possible specialPrimes;
- no smallPrimes.

Therefore cleanUp takes:

    dropSmallAndSpecialPrimes()
      -> modDownToSet(context.getCtxtPrimes()).

The degenerate drop branch in modDownToSet is disabled in the pinned source, so the executed path is
the real BGV modulus switch.

After the explicit cleanup:

    primeSet == ctxtPrimes.

## 4. Cleanup preserves the required semantic type

DoubleCRT::scaleDownToSet makes every rounding delta divisible by the current plaintext space before
division by the dropped-prime product.

At this boundary:

    ptxtSpace = 625.

The real modulus-switch branch does not alter ptxtSpace and does not apply the degenerate-drop
intFactor multiplication.

Hence:

    ptxtSpace = 625
    intFactor = 1
    keyID = 0
    primeSet = ctxtPrimes

after repaired cleanup.

Only then execute scalar-unit 28. Turn16 gives:

    intFactor = 67 mod625

without direct ciphertext-part/noise multiplication.

This repaired state matches the frozen recovery-canary root type.

## 5. Exact runtime coefficient-L1 key-switch envelope

Let:

    phi = 16384
    S = product(specialPrimes)
    D_i = product(primes in key-switch digit i).

For one key-switch matrix row, pinned RLWE1 at temporary plaintext space625 has exact error 625*e_i.

Turn13's source coefficient envelope gives:

    ||e_i||_1 <= 26*phi.

breakIntoDigits obtains each digit from the centered coefficient representative modulo D_i, so:

    ||d_i||_1 <= phi*D_i/2.

Thus fresh key-switch error before dropping special primes obeys:

    K_pre
      <= 625 * sum_i ||d_i||_1 ||e_i||_1
      <= 8125 * phi^2 * sum_i D_i.

After division by the special-prime product define the exact native-checkable envelope:

    K_KS_L1
      := 8125 * phi^2 * (sum_i D_i)/S.

This formula depends only on exact integer modulus-chain objects and the source coefficient ranges.
It does not use embeddingLargestCoeff.

## 6. Mod-switch rounding envelope

scaleDownToSet first obtains a centered coefficient representative modulo S and then changes each
coefficient by -S*r, with r balanced modulo625.

After division by S every rounding-polynomial coefficient therefore has absolute value at most312.5.

For a canonical two-part BGV ciphertext and a ternary secret with coefficient-L1 at most phi:

    R_L1
      <= 312.5 * phi * (1+phi)
      = 83,891,200,000.

This also avoids the floating canonical-norm estimator.

## 7. Source-sizing sufficient preflight

When bitsInSpecialPrimes uses the standard zero setting, Context::addSpecialPrimes derives the
special-prime budget from:

    maxDigitLog
    + log(p2e)
    + log(stdev)
    + 0.5 log(12)
    + log(nDigits)
    - 0.5 log(log(phi))
    - 2 log(p)
    - log(h).

For:

    p2e=625
    p=5
    stdev=3.2

and the production assertion:

    0 < context.getHwt() <= phi,

the digit-count and maximum-digit factors cancel in the worst-case normalized K_KS_L1 expression.

Taking h=phi gives the conservative source-sizing preflight:

    K_KS_L1 <= 401,679,183,790,908.6
    log2(K_KS_L1) <= 48.51304.

The standard bootstrappable HElib path replaces caller skHwt=0 by BOOT_DFLT_SK_HWT=120, so h=phi is
deliberately much more conservative.

Aung's exact skHwt, digit count and any custom bitsInSpecialPrimes remain unpublished. Therefore
production Step3 must still compute exact S and D_i and evaluate K_KS_L1 directly. The inequality
above is a sufficient source-sizing preflight, not a substitute for native provenance.

## 8. Public constant envelope inside pure EvalMap

Every EvalMap diagonal multiplier is ultimately stored from balanced_zzX over the temporary
plaintext algebra modulo625.

Thus each coefficient has absolute value at most312 and degree below phi.

Every public multiplier therefore satisfies:

    B_const <= 312*phi = 5,111,808

in coefficient-L1 norm.

This remains a valid physical ring-element envelope if the cache upgrades the multiplier to
DoubleCRT and stores a floating size estimate.

## 9. Conservative transform term count

For the current block transform:

    D*d = 2*8192 = 16384.

To cover both native and nonnative/two-cache implementation branches without relying on that
classification, use:

    M_terms <= 2*D*d = 32768.

The nonnative branch can additionally apply at most three outer smartAutomorph operations to partial
accumulators before the final sum.

This deliberately overcounts the current transform.

## 10. Coefficient-L1 pure-inverse exit bound

Let Turn13's cleaned shared-reconstruction envelope be:

    E0 = 6,957,728,854,835,200.

At modulus Q*S, one direct hoisted automorphism has error bounded by:

    S*E0 + K_pre.

After public-constant multiplication and accumulation, at most three outer
automorph/relinearization events, and the NEW final explicit cleanUp, a conservative normalized
bound is:

    E_inverse_clean
      <= M_terms * B_const * (E0 + K_KS_L1)
         + 3*(K_KS_L1 + R_L1)
         + R_L1.

Using the h=phi source-sizing sufficient preflight:

    E_inverse_clean
      <= 1.2327282569105341e27
    log2(E_inverse_clean)
      <= 89.9939133685.

With bits_HElib=400:

    log2(Q) >= 399.5,

so:

    log2(Q/E_inverse_clean)
      >= 309.5060866315 bits.

Turn11's current-ring correctness threshold is:

    log2(1/0.48)
      = 1.0588936891 bits.

Thus the repaired pure-inverse exit retains at least:

    308.4471929424 bits

above that threshold under the stated source-sizing sufficient condition.

Therefore Turn13's independent coefficient-L1 proof does not structurally stop at the shared
reconstruction. It crosses the pure inverse after the missing cleanup is inserted.

## 11. Construction update

Supersede:

    shared reconstruction
    -> pure inverse
    -> scalar-unit28
    -> recovery

with:

    shared reconstruction
    -> pure inverse
    -> EXPLICIT cleanUp / special-prime mod-down
    -> scalar-unit28
    -> recovery.

The cleanup is now part of the correctness contract, not optional instrumentation.

No performance conclusion follows. It may overlap work a later key-switch would otherwise force,
but that must be measured rather than assumed.

## 12. Step3 exact assertions

After mandatory Step2 canary PASS, production Step3 must record/assert:

Before pure inverse:
    primeSet == ctxtPrimes.

Immediately after pure inverse:
    record actual primeSet and special-prime presence.

After explicit cleanUp:
    primeSet == ctxtPrimes
    ptxtSpace == 625
    keyID == 0
    intFactor == 1.

After scalar28:
    primeSet == ctxtPrimes
    ptxtSpace == 625
    keyID == 0
    intFactor == 67.

For the deterministic envelope record exact:
    S = product(specialPrimes)
    every D_i
    K_KS_L1 = 8125*phi^2*(sum_i D_i)/S.

If the exact instantiated value invalidates the preflight margin, the downstream deterministic
envelope must be reopened.

## Verdict

FAIL_ASSUMED_PURE_INVERSE_EXIT_CTXT_PRIMES
PASS_EXPLICIT_INVERSE_EXIT_CLEANUP_REPAIR
PASS_INVERSE_EXIT_TYPE_STATE_AFTER_CLEANUP
PASS_CONDITIONAL_PURE_INVERSE_COEFFICIENT_L1_ENVELOPE

REPAIRED_PIPELINE:
  shared reconstruction
  -> pure inverse
  -> cleanUp
  -> scalar-unit28
  -> recovery

SOURCE_SIZING_PREFLIGHT_KKS_L1_MAX:
  401679183790908.6

SOURCE_SIZING_PREFLIGHT_INVERSE_ERROR_MAX:
  1.2327282569105341e27

SOURCE_SIZING_PREFLIGHT_LOG2_Q_OVER_ERROR:
  309.5060866315 bits

SOURCE_SIZING_PREFLIGHT_CORRECTNESS_MARGIN:
  308.4471929424 bits

EXACT_RUNTIME_L1_FORMULA:
  K_KS_L1 = 8125*phi^2*(sum_i D_i)/S

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

## Scope boundary

This turn propagates the independent coefficient-L1 correctness envelope through the repaired pure
inverse boundary only.

It does not yet propagate it through:
- the 17-call recovery tree;
- L0-L3 public correction accumulations;
- Algorithm4;
- final Recode.

Those remain downstream gates.

## Next decisive test

Mandatory evidence order remains Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 must instantiate the REAL pure inverse and verify the newly mandatory
inverse-exit cleanUp boundary plus exact S/D_i coefficient-L1 audit before entering the recovery
tree.
