# BOOT-B158 — generalized EvalPower family theorem

Date: 2026-10-28
TRACK_ID: BOOT
Status: ALGEBRA_PASS / GENERALIZATION_PASS / NATIVE_NOT_RUN

This finding supersedes the earlier conservative restriction of B158 to only
the full-row s=r call.

No native FHE execution was performed.

## Setting

Let:
- N = m r,
- r = 2^R,
- s = 2^ell <= r,
- input ciphertext encrypt row-wise repeated x_j exactly as in ePrint 2026/975
  Algorithm 3.

Let H=r/2 and P_k(x)=(1,x,...,x^(k-1)).

The two BFV physical hypercube halves correspond to the first H and second H
columns of every logical row under the paper's mat/rvec layout.

## Cases s=1 and s=2

s=1:
- output is the all-one power basis;
- zero ct-ct multiplications and zero rotations.

s=2:
- desired output is repeated (1,x_j);
- because the input already contains x_j in every slot, a public scale-1
  selector constructs this directly;
- zero ct-ct multiplications and zero rotations;
- if b=1, the auxiliary x^(s/2)=x is the original input.

Thus the degree lower bound is attained trivially.

## Case 4 <= s <= r/2

Maintain for k=1,2,4,...,s:

S_k(j) =
[first half: (H/k) copies of P_k(x_j)
 |
 second half: H copies of x_j^k].

Initialization and doubling are exactly the B158 recurrence already proved.

After ell ct-ct doublings:

S_s(j) =
[first half: (H/s) copies of P_s(x_j)
 |
 second half: H copies of x_j^s].

The target Algorithm-3 output requires r/s copies of P_s(x_j), i.e. the same
basis repeated in both physical halves.

One final RowRotation gives P_s in the second half. A public half selector then
copies that rotated first-half basis into the second half while leaving the
first half unchanged.

Therefore the exact Algorithm-3 output is recovered.

Operation count:

- ct-ct Mult: ell
- RowRotation used during doubling: ell-1
- final basis duplication RowRotation: +1

Total:

ct-ct Mult = ell
RowRotation = ell.

If b=1, the auxiliary x_j^(s/2) is available in the second half of
S_(s/2). The RowRotation already needed for the final doubling from s/2 to s
can be reused to broadcast this value to both halves with only a public
selector. No additional rotation or ct-ct multiplication is required.

## Case s=r

This is the previously formalized full-row special case.

At k=H:

S_H(j)=[P_H(x_j) | (x_j^H)^H].

The final RowRotation is used inside the final multiplication itself so that
the second half becomes x_j^H P_H(x_j), completing P_r.

No post-generation copy is needed.

Operation count:

- ct-ct Mult = ell
- RowRotation = ell-1

Optional x^(r/2) output is recovered with the same final RowRotation and a
public selector.

## Correctness theorem

For every power-of-two s<=r, B158 produces exactly the same logical power table
required by Algorithm 3.

Proof:
- s=1,2 are direct.
- for 4<=s<=r/2, induction proves the S_k invariant through k=s, after which
  RowRotation+selection copies the correct first-half P_s repetitions into the
  second half.
- for s=r, the special final multiplication maps
  [P_H | x^H] to [P_H | x^H P_H]=P_r.

The construction is row-local and RowRotation acts simultaneously on every
logical row, so the proof holds for arbitrary batch m under the same
mat/rvec layout.

## Exact falsification

Exponent-level exact tests were run for:

r in {8,16,32,64,128}

and every power-of-two s<=r.

All generated exponent tables exactly matched:

[0,1,...,s-1] repeated r/s times.

Observed counts matched the theorem.

Examples for r=128:

- s=1:   0 Mult, 0 Rot
- s=2:   0 Mult, 0 Rot
- s=4:   2 Mult, 2 Rot
- s=8:   3 Mult, 3 Rot
- s=16:  4 Mult, 4 Rot
- s=32:  5 Mult, 5 Rot
- s=64:  6 Mult, 6 Rot
- s=128: 7 Mult, 6 Rot

## Optimality

For s>=4 the target contains x^(s-1).

Public linear operations do not increase algebraic degree. After ct-ct
multiplicative depth d, degree is at most 2^d.

Hence:

d >= ceil(log2(s-1)) = log2(s) = ell.

Every arithmetic SIMD circuit in this model therefore needs at least ell ct-ct
multiplications.

B158 uses exactly ell.

Thus the ct-ct multiplication count is optimal for every power-of-two s>=4.

For s=1,2 the trivial zero-multiplication constructions are also optimal.

## Comparison to 2026/975 Algorithm 3

Original for s=2^ell:
- ct-ct Mult = 2ell-2
- rotations inside EvalPower = 0

B158:

s=1,2:
- 0 Mult, 0 Rot

4<=s<=r/2:
- ell Mult
- ell RowRotations

s=r:
- ell Mult
- ell-1 RowRotations

Ct-ct Mult saving for s>=4:

(2ell-2) - ell = ell-2.

Therefore:

- s=4 (ell=2): no ct-ct saving; likely poor native trade.
- s=8: save 1 ct-ct Mult but add 3 rotations.
- benefits increase with s.
- full-row r=32768 (ell=15): save 13 ct-ct Mult, add 14 rotations.

So theoretical optimality does NOT imply native value for small s.

## Algorithm-5 consequence

The important 9-bit large-polynomial path has:

1. first EvalPower with s=r=32768:
   major B158 target, 28 -> 15 ct-ct Mult.

2. second grouped EvalPower with s=2:
   original already has zero ct-ct Mult, but consumes a plaintext-mask
   normalization level;
   B158's trivial scale-1 selector form can avoid ct-ct work and may avoid that
   extra plaintext rescale.

The first full-row call remains the dominant performance target.

## Revised claim

B158 is not merely a special optimization for one parameter point.

The paper-level contribution can be stated as:

"An optimal ct-ct-multiplication family for power-of-two sparse BFV EvalPower,
using co-packed accumulator/binary-power state and hypercube-half routing.
For large s it trades ell-2 ciphertext multiplications for O(ell) uses of one
row automorphism; for s=r the rotation count is ell-1."

Native-value claims must still be restricted to configurations that actually
beat the original operation mix.

## Status

GENERAL_ALGEBRA: PASS
BATCH_GENERALIZATION: PASS
ALL_POWER_OF_TWO_s: PASS
CTCT_MULT_OPTIMALITY: PASS
SMALL_s_NATIVE_VALUE: NOT_ESTABLISHED / LIKELY_LOW
FULL_ROW_NATIVE_VALUE: ACTIVE_CANDIDATE
NATIVE_NOISE: NOT_RUN
NATIVE_LATENCY: NOT_RUN
