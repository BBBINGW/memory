# BOOT — B158 checkpoint-decoupling + half-basis Paterson–Stockmeyer gate

Date: 2026-10-28
TRACK_ID: BOOT

## Status

This is a paper/source-level gate only. No Codex/native/server run and no parameter/security change was performed.

Authoritative native state remains:
- B163 = FAIL_B163_NATIVE_NOISE
- B158 full co-packed practical realization = PARK
- B158 algebra and 15-ct×ct lower-bound result remain PASS

New candidate:
`B158_CHECKPOINT_DECOUPLED_HALF_BASIS = PROMISING_PAPER_GATE`

## Motivation from B163

B163 showed two distinct late noise mechanisms:
1. the recurrent fused state becomes increasingly noisy;
2. the public stage selector (M_k) multiplies that already-noisy state and contributes about 16–26 required-logQ bits in late stages.

The selector-norm gate showed that this amplification is structural: the centered coefficient (ell_1) norm of (M_k) grows to about (2^{27}) at (k=4096), and equivalent lifts/simple reindexings cannot remove it.

Hence a rescue must stop (M_k) from acting on the dirty recurrent state.

## Checkpoint-decoupling construction

B158 state:
[
S_k=[P_k	ext{ repeated }H/kmid x^kmathbf 1_H],qquad H=16384.
]

At a chosen checkpoint (k_0), the ordinary B158 factor construction already computes
[
A_{k_0}:=Rcdot S_{k_0}=[0mid x^{k_0}mathbf 1_H].
]

Retain this ciphertext instead of discarding it. This introduces no additional selector multiplication at the checkpoint.

For every later doubling:
[
A_{2k}=A_k^2=[0mid x^{2k}mathbf 1_H]
]
using one independent scale-invariant ct×ct square.

For the main B158 factor at stage (k), use
[
operatorname{RowSwap}(A_k)=[x^kmathbf1_Hmid0]
]
as the input to (M_k), rather than (operatorname{RowSwap}(S_k)). The right-half variable factor is simply (A_k), so the later (Rcdot S_k) selector multiplication disappears.

The main state still performs one fused ct×ct per doubling.

This breaks the accumulator -> selector noise feedback:
the high-norm (M_k) acts on a cleaner independent binary-power chain.

## Stop at H instead of materializing P_2H

The original B158 final step uses a noisy selector on (S_H) and one final fused ct×ct to materialize
[
P_{2H}=P_{32768}.
]

This is not necessary if Algorithm 5 is changed to use baby-step size (H).

At (k=H), we have
[
S_H=[P_Hmid x^Hmathbf1_H],
qquad
A_H=[0mid x^Hmathbf1_H].
]

Define
[
A_H^{m full}=A_H+operatorname{RowSwap}(A_H)
=[x^Hmathbf1_Hmid x^Hmathbf1_H].
]

Then with only one row swap and additions/subtraction,
[
egin{aligned}
P_H^{m rep}
&=S_H+operatorname{RowSwap}(S_H)-A_H^{m full}\
&=[P_Hmid P_H].
end{aligned}
]

No selector and no ct×ct are needed.

Thus the candidate deliberately never constructs (P_{32768}).

## Half-basis Paterson–Stockmeyer identity

For the 9-bit split-top case, the lower polynomial has block length
[
d=65536=4H.
]

Write
[
f_{<d}(x)
=f_0(x)+x^Hf_1(x)+x^{2H}f_2(x)+x^{3H}f_3(x),
qquad deg f_i < H.
]

The duplicated baby basis
[
[P_Hmid P_H]
]
is sufficient for a linear transform to compute the four block values (f_i(x)).

A grouped-power ciphertext carrying
[
[1,x^H,x^{2H},x^{3H}]
]
in the corresponding block pattern then allows the unchanged Algorithm-5 pattern:
linear transform -> one pointwise ct×ct -> rotate-and-sum.

This is ordinary Paterson–Stockmeyer with baby-step size H rather than 2H, but it is coupled to the checkpoint-decoupled B158 representation.

## Exact slot-level verification of the modified ParallelLT

The author's exact plaintext-slot semantics for:
- `parallelLT2FirstStageBSGSHoisted`,
- `buildShiftedMaskVectorInPlace`,
- `parallelLT2SumColumns`, and
- `parallelLT3BSGSHoisted`

were reimplemented algebraically.

For toy physical repetition sizes r = 8,16,32,64:
- H=r/2;
- input was ([P_Hmid P_H]);
- four random coefficient blocks of length H were used;
- each row of U was represented as ([f_i	ext{ coefficients}mid 0^H]);
- random x values were tested modulo 65537.

All tested cases exactly produced
[
[f_0(x),f_1(x),f_2(x),f_3(x)]
]
in the required periodic slot layout.

Therefore:
`HALF_BASIS_PARALLEL_LT_ALGEBRA = PASS`.

This is a plaintext/algorithmic verification, not yet a native encrypted run.

## ParallelLT operation-count impact

Current 9-bit r=32768, s=2 ParallelLT short branch:
- BSGS ell=2: g=2, b=1;
- baby rotations: 1;
- giant rotations: 0;
- sum-column rotations: log2((r/2)/ell)=13;
- final row swap: 1;
- ct-pt LT products: 2.

Half-basis version uses physical r=32768 but ell=4:
- g=2, b=2;
- baby rotations: 1;
- giant rotations: 1;
- sum-column rotations: 12;
- final row swap: 1;
- ct-pt LT products: 4.

Thus total LT rotations stay approximately 15 in both variants.
The primary LT surcharge is only two extra ct-pt products.

## ct×ct count

For the source 9-bit d=65536 path, the current author Algorithm-5 structure has approximately:
- full P_32768 generation: 28 ct×ct;
- x^32768 from x^16384: 1;
- s=2 grouped-power generation: 0;
- line-5 pointwise multiply: 1;
- leading x^65536 square: 1.

Total in this relevant power/evaluation skeleton: 31 ct×ct.

Checkpoint-decoupled half-basis:
- main fused chain only through H: 14 ct×ct;
- auxiliary squares from k0 to H: log2(H/k0);
- grouped basis [1,y,y^2,y^3], y=x^H: 2 ct×ct;
- line-5 pointwise multiply: 1;
- y^4=x^65536 leading power: 1.

Total:
[
18+log_2(H/k_0).
]

Examples:
- k0=32: 27 ct×ct (save 4/31 = 12.9%);
- k0=64: 26 ct×ct (save 5/31 = 16.1%);
- k0=128: 25 ct×ct (save 6/31 = 19.4%).

Compared only with the author's 28-ct×ct full-basis generator, the pre-LT state-generation counts are:
- k0=32: 23;
- k0=64: 22;
- k0=128: 21.

## Source-calibrated noise forecast

For all correct B163 fused stages after the earliest rounds,
[
	ext{requiredLogQ(after fused)}
-max(	ext{requiredLogQ(state)},	ext{requiredLogQ(factor)})
]
was approximately 29–31 bits.

The fixed R selector adds approximately 16–17 bits.

Using the retained R*S_k ciphertext at the checkpoint and modeling each independent auxiliary scale-invariant square by a conservative constant C bits, the checkpoint construction was propagated using the measured B163 M_k selector deltas.

Predicted requiredLogQ of the final (S_H) state:

- k0=64:
  - C=31 -> about 601 (budget 48);
  - C=32 -> 609 (40);
  - C=33 -> 617 (32);
  - C=34 -> 625 (24);
  - C=35 -> 633 (16);
  - C=36 -> 641 (8).

- k0=128:
  - C=31 -> about 619 (30);
  - C=32 -> 626 (23);
  - C=33 -> 633 (16);
  - C=34 -> 640 (9);
  - C=35 -> 647 (2);
  - C>=36 -> predicted failure.

This model is not a correctness proof because the exact auxiliary-square noise increment has not been measured.

Decision:
- k0=64 is the best first native gate: meaningful 5-ct×ct saving while retaining substantial modeled headroom.
- k0=128 is a later optimization only if k0=64 passes with comfortable budget.

## Prior-art screen

A targeted current search found standard Paterson–Stockmeyer power-basis generation, shared/reusable power bases, general packed polynomial evaluation, and the previously known rotate-and-multiply family, but no direct match for the combined mechanism:
- initially fused recurrent power-basis state;
- fork a clean binary-power auxiliary at a checkpoint;
- use it only for late selectors;
- stop at half basis;
- algebraically duplicate P_H without selectors;
- retune PS from 2 blocks to 4 blocks.

This is not a novelty determination.
`NOVELTY = PROMISING_NOT_ESTABLISHED`.

## Recommended next gate

If/when native experimentation is authorized, do not implement the entire modified polynomial evaluator first.

B164 should be the smallest decisive native gate:
1. fixed B163 source/security parameters;
2. checkpoint k0=64;
3. retain the already-computed R*S_64 as auxiliary;
4. future M_k selectors act on RowSwap(aux), and aux supplies the right half directly;
5. aux squares with MulRelinScaleInvariantNew and no Rescale;
6. stop at S_H (k=16384);
7. construct P_H^rep = S_H + RowSwap(S_H) - (A_H + RowSwap(A_H));
8. verify exact slots and positive coefficient-noise budget for S_H, A_H, and P_H^rep;
9. report per-stage main/aux/factor requiredLogQ and exact operation counts;
10. do NOT yet implement modified ParallelLT or benchmark performance.

Pass criterion:
all three final objects exact with positive budget at fixed parameters.

If this fails before H, park checkpoint rescue.
If it passes with >=15–20 bits final headroom, implement the four-block ParallelLT as the next gate.

No Q-prime, N, T, secret, security, or packing changes are allowed.
