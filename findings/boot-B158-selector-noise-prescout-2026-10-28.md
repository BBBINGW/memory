# BOOT-B158 — selector plaintext norm / noise prescout

Date: 2026-10-28  
TRACK_ID: BOOT  
Parent: B158 co-packed EvalPower

No native FHE execution was run.

## Question

B158 relies on public 0/1 slot selectors without an immediate rescale.
Lattigo permits this at the API/level level, but does the encoded plaintext
polynomial have a small enough coefficient norm for this to be plausibly safe?

## Exact batching-order reconstruction

Lattigo v6.2.0 BGV/BFV encoder source was inspected.

It uses:
- Galois generator 5,
- `permuteMatrix(logN)`,
- slot values placed at the permuted NTT locations,
- inverse NTT to produce the plaintext polynomial.

For the matched 9-bit parameter set:
- N = 32768
- T = 65537
- 2N = 65536

The exact slot-to-root ordering was reconstructed and inverse-CRT/INTT
calculations were performed modulo T. Round-trip reconstruction of random slot
vectors was checked exactly before using the transform for selector norms.

## Result: selectors are NOT small-coefficient plaintexts

Physical first/second-half selector:
- nonzero centered coefficients: 2
- max |coefficient|: 32768
- l2 norm ~= 32768.25 ~= 2^15
- l1 norm ~= 32896

For B158 first-half high-block selectors, the norm grows with stage.

Representative late stages:

- k=2^10: l2 ~= 2^19.71
- k=2^11: l2 ~= 2^20.21
- k=2^12: l2 ~= 2^20.71
- k=2^13: l2 ~= 2^21.21

At k=2^13:
- nonzero coefficients: 16386
- max |coefficient|: 32767
- l1 ~= 2^28.01
- l2 ~= 2^21.21

Therefore:
- `SELECTOR_SMALL_COEFFICIENT_ASSUMPTION: FALSE`
- no-rescale selector multiplication must not be described as noise-neutral.

## Why this is not yet a FAIL

The selector multiplication is not followed by an arbitrarily long no-rescale
chain. In B158, the selected factor is consumed by the next fused ct-ct
multiplication, which performs the normal BFV rescale/modulus reduction.

The current 9-bit Q chain uses approximately 34-bit intermediate primes.
Using the selector coefficient l2 norm only as a rough noise-growth proxy:

- worst selector proxy growth ~= 21.2 bits
- next prime reduction ~= 34 bits
- nominal difference ~= 12.8 bits

This is not a proof because BFV scale-invariant multiplication has cross terms,
relinearization noise, and exact coefficient-distribution effects.

But it rules out the simplest paper-level objection that selector growth is
obviously larger than an entire modulus prime.

The current public 9-bit implementation also reports substantial final
correctness headroom, so a native noise test is warranted rather than a
paper-level rejection.

## Decision

- SELECTOR_NORM_RISK: REAL
- LEVEL_GATE: PASS
- PAPER_LEVEL_NOISE_BLOCKER: NOT_FOUND
- NATIVE_NOISE: REQUIRED
- STATUS: PROMISING_NOT_ESTABLISHED

The decisive native test, if later authorized, must log noise/level immediately:
1. after RowRotation,
2. after selector construction,
3. after the fused ct-ct Mult/rescale,
for every stage, rather than only final decryption correctness.
