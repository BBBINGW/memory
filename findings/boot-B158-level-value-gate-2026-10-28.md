# BOOT-B158 — level/value gate after co-packed EvalPower algebra

Date: 2026-10-28  
TRACK_ID: BOOT  
Parent: boot-B158-copacked-optimal-evalpower-2026-10-28.md

No native execution was launched.

## Drop-in interface gate

The 2026/975 Algorithm-5 implementation calls MonomialGenExtra and requires:
1. the full power-basis ciphertext;
2. an auxiliary ciphertext encrypting x^(s/2) in all relevant slots.

B158 preserves this interface.

Immediately before the final fused multiplication, the second physical half of
the state already contains x^(s/2). The RowRotation needed by the final fused
step is also sufficient to copy that value into the first half. Public selectors
can therefore construct a full-slot x^(s/2) auxiliary ciphertext with no
additional ct-ct multiplication and no additional rotation.

Result:
- OUTPUT_LAYOUT: PASS
- EXTRA_HALF_POWER_INTERFACE: PASS
- ALGORITHM_5_DROP_IN_ALGEBRA: PASS

## Exact current 9-bit level schedule

From the current public implementation's planner:

Current parameters:
- MaxLevel = L19
- LWE->RLWE Step1 normalization consumes one level
- polynomial input = L18
- r = 32768 = 2^15
- d = 65536
- s = d/r = 2

Paper MonomialGen levels:
- ctP = L18 - 15 - 1 = L2
- ctHalf = x^(r/2) at L18-(15-1) = L4
- ctR=x^r after one square = L3
- second MonomialGen(s=2): ctG=L2, ctDHalf=L3
- LT/collapse lower branch -> L1
- leading x^d branch -> L1
- polynomial output -> L1
- m=1 tail normalizes L1 -> Qprime L0

## B158 at the same Q chain

Co-packed first basis:
- 15 sequential ct-ct Mults
- ctP = L3
- x^(r/2) extra = L4

The s=2 grouped basis does not need a ct-ct Mult and can be constructed using
scale-1 public selectors without a level drop:
- ctR=x^r = L3
- ctG = L3
- ctDHalf = L3

Hence:
- LT can run at L3
- lower collapse branch reaches L2
- leading branch still reaches L1
- final polynomial output is still bounded by leading branch at L1

Therefore the same chain gains one spare level in the lower branch but does not
automatically change the final output level.

## One-Q-prime reduction candidate

Remove one Q prime:
- MaxLevel L18
- after Step1 normalization polynomial input L17

Then B158 predicts:
- ctP L2
- x^(r/2) L3
- x^r L2
- ctG L2
- LT/collapse lower branch L1
- leading branch: x^d square L1, leading plaintext multiplication L0

The current m=1 extraction code accepts a polynomial output at L0: it only
performs the final Q->Qprime normalization when ctCoeff.Level()>0.

Thus there is no hard level-count blocker to a one-prime-smaller chain.

However the lower branch would need a proper L1->L0 normalization before
combining with the L0 leading term (rather than a blind DropLevel) to preserve
the intended scale/noise semantics.

Decision:
- ONE_Q_PRIME_REDUCTION: PLAUSIBLE
- PARAMETER_SECURITY: WOULD_ONLY_IMPROVE
- PRECISION/NOISE: NOT_ESTABLISHED
- DO NOT CLAIM PARAMETER PASS BEFORE NATIVE TRACE

## Key-switch accounting

For s=2^ell:

Paper EvalPower:
- ct-ct Mult = 2ell-2
- therefore approximately 2ell-2 relinearization key switches

B158:
- ct-ct Mult = ell -> ell relinearization KS
- RowRotation = ell -> ell rotation KS
- total KS-like operations = 2ell

At ell=15:
- paper: 28 relinearization KS
- B158: 15 relinearization KS + 15 rotation KS = 30 KS

So B158 does NOT win by reducing key switching count.

It removes:
- 13 ciphertext tensor multiplications
- 13 associated rescale/modulus-reduction steps

while adding:
- 15 automorphism permutations
- 2 net extra key-switch operations
- O(ell) scale-1 selector plaintext multiplications

A useful simplified break-even model is:

Let
- K = cost of one key-switch/relinearization core,
- M = extra tensor+rescale cost of a ct-ct Mult beyond K,
- A = automorphism/permutation overhead of RowRotation,
ignoring selector cost.

Paper ~ 28(K+M)
B158 ~ 15(K+M)+15(K+A)

B158 wins iff:

2K + 15A < 13M.

If A is negligible, this is K/M < 6.5.

Therefore a speedup is plausible even when key switching dominates moderately,
but it is not guaranteed. This is exactly what the native gate must measure.

## Rotation-key memory

Standalone EvalPower needs one RowRotation Galois element independent of ell.

In the complete 2026/975 bootstrapping pipeline RowRotation already exists in
the low-level polynomial/linear-transform key set. B158 would raise the required
level of that same Galois key to the polynomial-input region rather than add ell
different rotation keys.

So:
- GALOIS_ELEMENT_COUNT_INCREASE: at most 0/1 depending on standalone context
- HIGH_LEVEL_ROW_KEY_SIZE_INCREASE: YES
- asymptotic key-count growth with ell: NONE

## Remaining decisive paper-level blocker

Selector multiplication noise.

B158 uses repeated public 0/1 slot-selector plaintext multiplications without
rescaling. Lattigo permits this at the API/level level, but the encoded selector
polynomials can still amplify coefficient-basis BFV noise. The construction
therefore has:
- LEVEL_GATE: PASS
- NOISE_GATE: UNRESOLVED

This must not be inferred from the exact slot algebra.

## Current B158 status

- ALGEBRA: PASS
- BATCH GENERALIZATION: PASS
- CT-CT MULT COUNT: OPTIMAL (ell)
- DROP-IN LAYOUT: PASS
- EXTRA HALF-POWER OUTPUT: PASS
- LEVEL/API GATE: PASS
- ONE-Q-PRIME REDUCTION: PLAUSIBLE, NOT PROVEN
- KEY-SWITCH COUNT: NOT REDUCED (28 -> ~30 at ell=15)
- NOISE: UNRESOLVED
- NATIVE VALUE: UNRESOLVED
- PRIOR COLLISION: NOT_FOUND_PRELIMINARY

No Codex/native run should be started without PI authorization.
