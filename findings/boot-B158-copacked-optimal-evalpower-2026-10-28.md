# BOOT-B158 — Co-packed optimal EvalPower for sparse BFV functional bootstrapping

Date: 2026-10-28  
TRACK_ID: BOOT  
Status: PAPER_LEVEL_PROMISING / NATIVE_NOT_RUN  
No Codex / GPU / remote native execution was launched.

## Motivation

Post-B157, B145+B152 is parked because the exact secure native realization
fails both precision and performance. Fresh BOOT work therefore resumed on
whole-bootstrap bottlenecks.

The full text and current public implementation of ePrint 2026/975,
"Functional Bootstrapping for a Single LWE Ciphertext with O~(1) Polynomial
Multiplications", were inspected.

Its current public implementation still shows the power-basis generation
(BuildBasis / EvalPower) as the dominant single online substage in the 9-bit
m=1 setting.

Paper Algorithm 3 generates the vector of powers by maintaining two logically
separate ciphertext computations:

1. the squaring chain x, x^2, x^4, ...;
2. an accumulator that multiplies the masked factors
   (C_i * x^(2^i) + D_i).

For s=2^ell this costs:
- 2*ell - 2 ciphertext-ciphertext multiplications,
- ell plaintext-ciphertext multiplications,
- no rotations inside EvalPower,
with multiplicative depth reported as ell+1.

## Core observation

The duplicated-slot representation has enough redundant SIMD capacity to keep
the accumulator and the current squaring-chain value inside *one ciphertext*.

The BFV plaintext slots are viewed as a 2 x (N/2) hypercube. The paper's
mat/rvec layout stacks the m logical rows column by column, so RowRotation swaps
the first and second r/2 columns of every logical row simultaneously.

For each encrypted input x_j, define

P_k(x_j) = (1, x_j, ..., x_j^(k-1)),  k a power of two.

At stage k, maintain one ciphertext S_k whose j-th logical row is

[first half: repeated copies of P_k(x_j) | second half: x_j^k repeated].

The initial S_1 is obtained from the input by public selector masks:
first half = 1, second half = x_j. No ciphertext-ciphertext multiplication is
needed.

Let tau be RowRotation. Then tau(S_k) has x_j^k repeated in its first half.

Using public 0/1 selector masks, construct a factor F_k such that, in the first
half, each pair of consecutive k-slot blocks is multiplied by

[1 on the first k slots, x_j^k on the next k slots],

while the second half is multiplied by x_j^k.

Therefore one ciphertext-ciphertext multiplication

S_k * F_k

simultaneously performs:

- P_k -> P_(2k) in the accumulator lane;
- x_j^k -> x_j^(2k) in the auxiliary lane.

The two logical multiplications that Algorithm 3 performs separately are fused
into one SIMD multiplication.

At the final stage, the two physical halves are combined with the same
RowRotation and public selector masks so that the last multiplication emits the
complete requested power basis and no auxiliary lane remains.

## Exact algebra gate

Exact modular simulations were run locally for:
- N = 2,4,8,16,32,64 in the single-input case;
- m = 1,2,4,8 and per-row r = 4,8,16 in the batched column-stacked layout.

All tested slots matched the exact target powers.

This is only an algebraic falsification test; no native FHE execution was run.

## Operation count

For s = 2^ell:

Paper Algorithm 3:
- ct-ct Mult: 2ell - 2
- plaintext CMult: ell
- RowRotation: 0

Co-packed construction:
- ct-ct Mult: ell
- RowRotation: ell
- O(ell) public 0/1 selector CMults and additions

For the important 9-bit basis with s=r=32768=2^15:

Paper:
- 28 ct-ct Mult

Co-packed:
- 15 ct-ct Mult
- 15 uses of the SAME RowRotation key

ct-ct multiplication count reduction:
- 13 / 28 = 46.43%

Only one additional Galois element (the row swap) is required independent of
ell.

## Multiplication lower bound

The construction is optimal in ct-ct multiplication count under the ordinary
arithmetic-circuit model.

A target slot contains x^(s-1). Starting from degree-1 encrypted inputs, after
multiplicative depth d the algebraic degree is at most 2^d. Thus

d >= ceil(log2(s-1)) = ell

for power-of-two s.

Total ct-ct multiplication count is at least multiplicative depth, hence every
such circuit needs at least ell ct-ct multiplications.

The co-packed construction uses exactly ell.

Therefore:
- `PASS_CTXT_MULT_LOWER_BOUND`
- `OPTIMAL_CTXT_MULT_COUNT = ell`

## BFV scale / level gate

A possible blocker was that the 0/1 selector masks might consume an extra level
each stage.

Inspection of Lattigo v6.2.0 (the implementation used by 2026/975) shows that
in scale-invariant BFV mode, vector plaintext operands (`[]uint64`) are encoded
with plaintext scale 1 and `MulScaleInvariant` uses standard ciphertext-
plaintext tensoring without an implicit rescale or level drop.

Therefore selector masking does NOT force an extra modulus level per stage.

This removes the main precision/depth blocker.

Potential depth effect:
- co-packed sequential ct-ct depth is ell;
- paper reports EvalPower depth ell+1.

A one-level modulus saving may therefore be possible, but is NOT yet claimed as
a secure parameter reduction until the complete downstream chain is checked.

## Value gate

This is a trade:
- remove ell-2 expensive relinearized/rescaled ct-ct multiplications,
- add ell RowRotations/key-switches,
- add cheap scale-1 public selector masks.

At equal level, a relinearized BFV ct-ct multiplication contains tensor
multiplication + relinearization key switching + rescaling, whereas RowRotation
contains automorphism + key switching. Thus a latency win is plausible, but
not guaranteed.

The current public 2026/975 implementation reports for 9-bit m=1 roughly:
- online total ~2.061 s
- BuildBasis ~1.141 s
- Step 1 ~0.693 s

so BuildBasis remains the largest individual online component after the
authors' post-paper optimizations.

No native timing claim is made for B158.

## Prior-art gate

A broad search was performed for:
- packed/SIMD power-basis generation,
- duplicated-slot power generation,
- rotation-based all-powers generation,
- co-packed power chains.

Generic SIMD circuit packing, rotation-based routing, polynomial evaluation,
and rotation-based products are well-known. However, no direct source was found
that gives this specific fusion:

"store the EvalPower accumulator and the current 2^i-th power in the two BFV
hypercube halves, then use the same RowRotation each round so one ct-ct
multiplication performs both accumulator extension and power squaring."

The current 2026/975 paper and its public MonomialGen implementation do not use
this construction: they materialize the x^(2^i) squaring chain separately and
then multiply the masked factors into an accumulator.

Status:
- `DIRECT_PRIOR_COLLISION: NOT_FOUND_PRELIMINARY`
- `NOVELTY: PROMISING_NOT_ESTABLISHED`

## Security / correctness expectations

The construction changes only the homomorphic evaluation schedule and slot
layout. It does not change:
- LWE/RLWE secret distributions,
- ring dimension,
- plaintext modulus,
- security target,
- semantic target function.

Security assumptions are therefore unchanged.

Native noise remains unresolved:
- fewer ct-ct multiplications/relinearizations,
- more rotation key switches.

This must be measured; do not infer a noise win from operation count.

## Decision

B158 is currently the strongest fresh BOOT candidate after B157.

Status:
- ALGEBRA: PASS
- GENERALIZATION_TO_BATCH_LAYOUT: PASS
- CTXT_MULT_LOWER_BOUND: PASS / OPTIMAL
- SCALE_LEVEL_GATE: PASS
- PRIOR_ART: NO_DIRECT_COLLISION_FOUND_PRELIM
- NATIVE_CORRECTNESS: NOT_RUN
- NATIVE_LATENCY: NOT_RUN
- NATIVE_NOISE: NOT_RUN
- NOVELTY: PROMISING_NOT_ESTABLISHED

Do not launch Codex/native execution automatically.

## Next cheapest gates

1. Formalize the recurrence and operation counts for arbitrary m,r,s.
2. Check whether the final output layout is exactly drop-in compatible with
   Algorithm 4/5 without an extra permutation.
3. Audit the complete level schedule to see whether the ell+1 -> ell depth
   saving actually removes one Q prime in the 9-bit parameter set.
4. Only after those gates, if PI authorizes native work, implement a minimal
   B158 replacement for MonomialGenExtra and compare:
   - bit-exact plaintext slots,
   - level/scale trace,
   - noise,
   - BuildBasis latency,
   - total online latency,
   - row-rotation-key memory,
   - matched security parameters.
