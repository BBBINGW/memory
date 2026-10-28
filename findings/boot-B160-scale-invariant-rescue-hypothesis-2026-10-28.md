# BOOT-B160 — scale-invariant BFV rescue hypothesis for B158

Date: 2026-10-28
TRACK_ID: BOOT
Status: PAPER_LEVEL_RESCUE_HYPOTHESIS / NATIVE_NOT_RUN

No Codex/native execution was launched.

## Motivation

B159 failed at k=4 because the scale-one no-rescale selector factor was fed
into regular ct-ct tensoring and exhausted the coefficient-noise budget.

Do not rescue this by:
- adding Q primes
- increasing N
- changing security
- weakening correctness
- tuning unrelated parameters

The only currently justified rescue is to change the multiplication/noise
mechanism while preserving the B158 recurrence and matched cryptographic point.

## Lattigo source fact

Lattigo's BFV implementation is the scale-invariant specialization of the
unified BGV evaluator.

Its official BFV documentation states that enabling the scale-invariant
evaluator replaces:
- Mul / MulNew
- MulRelin / MulRelinNew
- Rescale

with scale-invariant alternatives.

The documented purpose is that scale-invariant tensoring can support subsequent
multiplications without the usual per-multiplication rescale schedule, with
noise growth comparable to textbook BFV.

The public 2026/975 implementation currently constructs its evaluator with the
scale-invariant flag set to false and follows the regular tensoring + explicit
rescale schedule.

B159 also tested that regular schedule for ct-ct products.

Therefore the Lattigo scale-invariant multiplication path was not tested by
B159.

## B160 smallest falsifiable claim

Keep:
- the exact B158 slot recurrence
- the exact 15 ct-ct / 14 RowRotation operation structure
- the exact 9-bit m=1 source point
- the same N/T/Q/P/security/secret
- the same Step1/BatchLT/tail

Change only the B158 recurrence's multiplication implementation:

1. retain scale-one selector plaintext construction initially;
2. use the explicit scale-invariant BFV multiplication/relinearization path
   for the fused ct-ct recurrence products;
3. do not globally change unrelated pipeline arithmetic unless the API requires
   a local evaluator object sharing the same parameters/keys.

Question:

Can scale-invariant tensoring prevent the k=4 catastrophic noise amplification
while preserving the B158 recurrence and matched parameters?

## Why this is a justified rescue

The B159 failure is specifically a multiplication-noise failure:
- k=1 correct
- k=2 correct
- k=4 coefficient-noise budget = -16 bits

It is not:
- a slot-layout failure
- a wrong recurrence
- a security failure
- a modulus-instantiation failure

Scale-invariant BFV tensoring directly targets repeated multiplication noise
without requiring an extra Q-prime after each product.

Therefore it is materially different from simply giving the failed B159 path
more modulus.

## Important caveat

Selector ct-pt multiplication itself still uses a structured plaintext mask.
Scale-invariant ct-ct multiplication may or may not be enough because the factor
ciphertext can already carry substantial selector-induced noise.

Thus B160 is only a falsifiable rescue hypothesis, not a predicted PASS.

## Decisive gate

The cheapest native test, if PI later authorizes Codex, should run only the
deterministic x=1 stage trace first.

Required checkpoints:
- k=1
- k=2
- k=4
- k=8
- continue powers of two only while noise budget remains positive

Do not benchmark unless the complete r=32768 basis is correct.

Decision:

- if k=4 still fails/noise budget <=0:
  B158 practical line should be PARKed; do not pursue more modulus tricks.

- if k=4 passes but a later stage fails:
  record first failing k and compare noise-growth slope; only continue if there
  is a clear structural reason for one more paper-level fix.

- if all stages pass:
  then run matched correctness and performance, and only afterwards revisit
  the one-Q-prime hypothesis.

## Current BOOT state

B145+B152: PARK / FAIL_NATIVE_VALUE
B158 algebra: PASS / optimal ct-ct count
B159: FAIL_NOISE for regular tensoring realization
B160: SCALE_INVARIANT_RESCUE_HYPOTHESIS / NOT_RUN

Do not auto-run Codex.
