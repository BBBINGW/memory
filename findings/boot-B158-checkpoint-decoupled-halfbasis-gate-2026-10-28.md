# BOOT — B158 checkpoint-decoupling + half-basis Paterson–Stockmeyer gate

Date: 2026-10-28  
TRACK_ID: BOOT

## Status

This is a paper/source-level gate only. No Codex/native/server run and no parameter/security change was performed.

Authoritative native state remains:

- B163 = \`FAIL_B163_NATIVE_NOISE\`
- B158 full co-packed practical realization = PARK
- B158 algebra and 15-ct×ct lower-bound result remain PASS

New candidate:

\`B158_CHECKPOINT_DECOUPLED_HALF_BASIS = PROMISING_PAPER_GATE\`

## Motivation from B163

B163 exposed two late noise mechanisms:

1. the recurrent fused state becomes increasingly noisy;
2. the public stage selector \(M_k\) multiplies that already-noisy state and contributes about 16–26 required-logQ bits in late stages.

The selector-norm gate established that this amplification is structural: the centered coefficient \(\ell_1\) norm of \(M_k\) grows to about \(2^{27}\) at \(k=4096\), while equivalent coefficient lifts and simple Galois/GF(2)-linear reindexings do not provide the required reduction.

Hence a rescue should stop \(M_k\) from acting on the dirty recurrent state.

## Checkpoint-decoupling construction

Let \(H=16384\). B158 maintains

\[
S_k=[P_k\text{ repeated }H/k\mid x^k\mathbf 1_H].
\]

At a chosen checkpoint \(k_0\), the ordinary B158 factor construction already computes

\[
A_{k_0}:=R\cdot S_{k_0}=[0\mid x^{k_0}\mathbf 1_H].
\]

Retain this ciphertext instead of discarding it. This adds no selector multiplication at the checkpoint.

For each later doubling,

\[
A_{2k}=A_k^2=[0\mid x^{2k}\mathbf 1_H]
\]

using one independent scale-invariant ct×ct square.

For the main B158 factor at stage \(k\), use

\[
\operatorname{RowSwap}(A_k)=[x^k\mathbf1_H\mid0]
\]

as the input to \(M_k\), rather than \(\operatorname{RowSwap}(S_k)\). The right-half variable factor is simply \(A_k\), so the later \(R\cdot S_k\) selector multiplication disappears.

The main state still performs one fused ct×ct per doubling.

This breaks the accumulator-to-selector feedback: the high-norm \(M_k\) acts on a cleaner independent binary-power chain.

## Stop at H instead of materializing \(P_{2H}\)

The original B158 final step applies a noisy selector to \(S_H\) and one final fused ct×ct to materialize

\[
P_{2H}=P_{32768}.
\]

This is unnecessary if Algorithm 5 uses baby-step size \(H\).

At \(k=H\),

\[
S_H=[P_H\mid x^H\mathbf1_H],
\qquad
A_H=[0\mid x^H\mathbf1_H].
\]

First subtract the auxiliary:

\[
L_H:=S_H-A_H=[P_H\mid0].
\]

Then

\[
P_H^{\mathrm{rep}}
=
L_H+\operatorname{RowSwap}(L_H)
=
[P_H\mid P_H].
\]

Thus the final conversion needs only one RowRotation plus additions/subtraction, with no selector and no ct×ct.

There are 13 per-stage RowRotations through the \(k=8192\to H\) main recurrence, plus this final one, so the total remains 14 RowRotations—the same as original B158. No new Galois-key type is required. Auxiliary squaring uses the already-present relinearization key.

The candidate deliberately never constructs \(P_{32768}\).

## Half-basis Paterson–Stockmeyer identity

For the 9-bit split-top source case,

\[
d=65536=4H.
\]

Write the lower polynomial as

\[
f_{<d}(x)
=
f_0(x)+x^Hf_1(x)+x^{2H}f_2(x)+x^{3H}f_3(x),
\qquad
\deg f_i<H.
\]

The duplicated baby basis

\[
[P_H\mid P_H]
\]

is sufficient for a linear transform to compute the four block values \(f_i(x)\).

A grouped-power ciphertext carrying

\[
[1,x^H,x^{2H},x^{3H}]
\]

in the corresponding block pattern then permits the usual Algorithm-5 structure:

\[
\text{linear transform}
\to
\text{one pointwise ct×ct}
\to
\text{rotate-and-sum}.
\]

This is ordinary Paterson–Stockmeyer with baby-step size \(H\) rather than \(2H\), coupled to the checkpoint-decoupled B158 representation.

## Exact slot-level verification of modified ParallelLT

The author's exact plaintext-slot semantics for:

- \`parallelLT2FirstStageBSGSHoisted\`
- \`buildShiftedMaskVectorInPlace\`
- \`parallelLT2SumColumns\`
- \`parallelLT3BSGSHoisted\`

were independently reimplemented algebraically.

For toy physical repetition sizes \(r=8,16,32,64\):

- \(H=r/2\);
- input was \([P_H\mid P_H]\);
- four random coefficient blocks of length \(H\) were used;
- each row of \(U\) was represented as \([f_i\text{ coefficients}\mid0^H]\);
- random \(x\) values were tested modulo 65537.

All tested cases exactly produced the desired periodic layout

\[
[f_0(x),f_1(x),f_2(x),f_3(x)].
\]

Therefore:

\`HALF_BASIS_PARALLEL_LT_ALGEBRA = PASS\`.

This is an algebra/plaintext verification, not a native encrypted run.

## ParallelLT operation-count impact

Current 9-bit \(r=32768,s=2\) short-branch LT:

- BSGS \(\ell=2\): \(g=2,b=1\);
- baby rotations: 1;
- giant rotations: 0;
- sum-column rotations: 13;
- final row swap: 1;
- ct-pt LT products: 2.

Half-basis version keeps physical \(r=32768\) but uses \(\ell=4\):

- \(g=2,b=2\);
- baby rotations: 1;
- giant rotations: 1;
- sum-column rotations: 12;
- final row swap: 1;
- ct-pt LT products: 4.

Thus total LT rotations stay at approximately 15 in both variants. The primary LT surcharge is only two extra ct-pt products.

## ct×ct count

For the source 9-bit \(d=65536\) path, the current author Algorithm-5 power/evaluation skeleton has approximately:

- full \(P_{32768}\) generation: 28 ct×ct;
- \(x^{32768}\) from \(x^{16384}\): 1;
- \(s=2\) grouped-power generation: 0;
- line-5 pointwise multiply: 1;
- leading \(x^{65536}\) square: 1.

Total: 31 ct×ct.

Checkpoint-decoupled half-basis:

- main fused chain only through \(H\): 14 ct×ct;
- auxiliary squares from \(k_0\) to \(H\): \(\log_2(H/k_0)\);
- grouped basis \([1,y,y^2,y^3]\), \(y=x^H\): 2 ct×ct;
- line-5 pointwise multiply: 1;
- \(y^4=x^{65536}\) leading power: 1.

Total:

\[
18+\log_2(H/k_0).
\]

Examples:

- \(k_0=32\): 27 ct×ct, saving 4/31 = 12.9%;
- \(k_0=64\): 26 ct×ct, saving 5/31 = 16.1%;
- \(k_0=128\): 25 ct×ct, saving 6/31 = 19.4%.

Compared only with the author's 28-ct×ct full-basis generator, pre-LT state-generation counts are 23, 22, and 21 respectively.

## Source-calibrated noise forecast

For all correct late B163 fused stages,

\[
\operatorname{requiredLogQ}(\text{after fused})
-
\max(
\operatorname{requiredLogQ}(\text{state}),
\operatorname{requiredLogQ}(\text{factor})
)
\]

was approximately 29–31 bits.

The fixed \(R\) selector adds about 16–17 bits.

Using the retained \(R S_k\) ciphertext at the checkpoint and modeling each independent auxiliary scale-invariant square by a conservative \(C\)-bit increment gives the following forecast for final \(S_H\).

For \(k_0=64\):

- \(C=31\): required ≈ 601, budget ≈ 48;
- \(C=32\): 609, budget ≈ 40;
- \(C=33\): 617, budget ≈ 32;
- \(C=34\): 625, budget ≈ 24;
- \(C=35\): 633, budget ≈ 16;
- \(C=36\): 641, budget ≈ 8.

For \(k_0=128\):

- \(C=31\): required ≈ 619, budget ≈ 30;
- \(C=32\): 626, budget ≈ 23;
- \(C=33\): 633, budget ≈ 16;
- \(C=34\): 640, budget ≈ 9;
- \(C=35\): 647, budget ≈ 2;
- \(C\ge36\): predicted failure.

This model is not a correctness proof because the exact isolated auxiliary-square increment has not yet been measured.

Decision:

- \(k_0=64\) is the best first native gate: 5-ct×ct saving with substantial modeled headroom.
- \(k_0=128\) is a later optimization only if \(k_0=64\) passes comfortably.

## Prior-art screen

A targeted current search found standard Paterson–Stockmeyer power-basis generation, reusable/shared power bases, packed polynomial evaluation, and rotate-and-multiply techniques, but no direct match for the combined mechanism:

- initially fused recurrent power-basis state;
- fork a clean binary-power auxiliary at a checkpoint;
- use it only for late selectors;
- stop at half basis;
- duplicate \(P_H\) linearly;
- retune PS from 2 blocks to 4 blocks.

This is not a novelty determination.

\`NOVELTY = PROMISING_NOT_ESTABLISHED\`.

## Recommended next gate

If native experimentation is authorized, do not implement the entire modified polynomial evaluator first.

B164 should be the smallest decisive native gate:

1. fixed B163 source/security parameters;
2. checkpoint \(k_0=64\);
3. retain the already-computed \(R S_{64}\) as auxiliary;
4. later \(M_k\) selectors act on \(\operatorname{RowSwap}(A_k)\);
5. \(A_k\) directly supplies the right-half variable term;
6. update \(A_{2k}=A_k^2\) with \`MulRelinScaleInvariantNew\`, no Rescale;
7. stop at \(S_H\), \(H=16384\);
8. form \(L_H=S_H-A_H\);
9. form \(P_H^{\rm rep}=L_H+\operatorname{RowSwap}(L_H)\);
10. verify exact slots and positive coefficient-noise budgets for \(S_H,A_H,P_H^{\rm rep}\);
11. report per-stage main/aux/factor requiredLogQ and exact operation counts;
12. do not yet implement modified ParallelLT or run a performance benchmark.

Pass criterion:

all three final objects exact with positive budget at fixed parameters.

If this fails before \(H\), park checkpoint rescue.

If it passes with at least about 15–20 bits final headroom, implement the four-block ParallelLT as the next gate.

No Q-prime, \(N\), \(T\), secret, security, or packing changes are allowed.
