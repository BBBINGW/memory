# BOOT-B158 — paper-ready recurrence, optimality proof, and refined prior-art gate

Date: 2026-10-28  
TRACK_ID: BOOT  
Status: PAPER_LEVEL_PROMISING / NATIVE_NOT_RUN

No Codex, GPU, remote server, or native benchmark was launched.

## Scope correction

The strongest clean statement is for the dominant full-row call

`EvalPower(ct, r, 1)`

with
- r = 2^ell,
- ell >= 2,
- input encrypting 1_r \otimes (x_0,...,x_{m-1}).

This is exactly the expensive first EvalPower used by the large-polynomial
Algorithm-5 path of ePrint 2026/975.

Do not overclaim the same recurrence for every s<r without a separate proof.
The trivial s=2 call in Algorithm 5 should remain trivial.

## Layout

Let H=r/2.

Under the paper's mat/rvec convention, every logical row j has r columns.
Because r and m are powers of two and N=mr, BFV RowRotation swaps the first H
columns and the second H columns simultaneously for every logical row.

Write

P_k(x)=(1,x,...,x^{k-1}).

For k=2^i with 1 <= k <= H, maintain a ciphertext S_k whose j-th logical row
encrypts

[first half: (H/k) repeated copies of P_k(x_j)
 |
 second half: H copies of x_j^k].

This single ciphertext co-packs:
1. the growing power-basis accumulator;
2. the current binary power x_j^k needed for the next doubling.

## Initialization

The input X has x_j in every slot of logical row j.

Using a public first/second-half selector, construct

S_1 = [1^H | x_j^H]

row-wise.

No ct-ct multiplication is used.

## First doubling: no RowRotation needed

This improves the earlier B158 count.

For k=1, the original input X already supplies x_j in every slot.

Construct a factor F_1 with row

[(1,x_j) repeated H/2 times | x_j^H]

using one public selector on X plus public constants.

Then

S_2 = S_1 * F_1

has row

[P_2(x_j) repeated H/2 times | (x_j^2)^H].

Thus the first ct-ct multiplication does not need RowRotation.

## Regular doubling

For 2 <= k < H, k a power of two, let tau be RowRotation.

By the invariant,

tau(S_k)

has x_j^k in every slot of its first physical half.

Let M_k be the public mask that, in the first half, selects the second k-slot
sub-block of every consecutive 2k-slot block:

M_k =
[(0^k,1^k) repeated H/(2k) times | 0^H].

Construct F_k linearly from S_k, tau(S_k), and public constants so that the
j-th row of F_k is

[(1^k,(x_j^k)^k) repeated H/(2k) times | (x_j^k)^H].

One explicit expression is

F_k =
(L-M_k)
+ M_k * tau(S_k)
+ R * S_k,

where L and R are the first-half and second-half public selectors and all
products here are ciphertext-plaintext selector multiplications.

Then one ct-ct multiplication gives

S_{2k}=S_k * F_k.

Correctness is blockwise:

[P_k,P_k] * [1^k,(x^k)^k]
=
[P_k,x^k P_k]
=
P_{2k},

while the auxiliary half becomes

x^k * x^k = x^{2k}.

Hence the invariant is preserved.

## Final doubling

At k=H,

S_H = [P_H(x_j) | (x_j^H)^H].

RowRotation gives

tau(S_H)=[(x_j^H)^H | P_H(x_j)].

Construct

F_H = [1^H | P_H(x_j)]

from tau(S_H) with a public selector and constants.

Then

S_r = S_H * F_H
    = [P_H(x_j) | x_j^H P_H(x_j)]
    = P_r(x_j).

Therefore the final ciphertext is exactly the target full-row power basis.

## Auxiliary x^(r/2) output

The paper's b=1 interface also returns a ciphertext with x_j^H repeated across
all r slots.

The same final RowRotation already computed above is enough.

For example,

A_H = S_H + L * (tau(S_H)-S_H)

has x_j^H in both halves.

This needs no extra RowRotation and no extra ct-ct multiplication.

Thus B158 is a drop-in algebraic replacement for the dominant
`EvalPower(ct,r,1)` interface.

## Exact operation count

For r=2^ell, ell>=2:

B158:
- ct-ct Mult: ell
- RowRotation: ell-1
- selector ct-pt multiplies: O(ell)
  (one explicit construction uses about 2ell with the auxiliary output)
- distinct new rotation offsets: only the single RowRotation automorphism

For r=32768=2^15:

- ct-ct Mult = 15
- RowRotation = 14

Earlier B158 notes said 15 rotations. That was conservative and is superseded
by this finding: the k=1 round can use the original duplicated input and needs
no rotation.

## Optimality theorem

Claim:
For r=2^ell >=4, any arithmetic SIMD circuit that starts from the repeated
encrypted inputs, uses arbitrary public linear operations (additions,
plaintext multiplications, rotations/Galois automorphisms), and ct-ct
multiplications, and outputs a slot equal to x_j^(r-1), must have ct-ct
multiplicative depth at least ell.

Proof:
Treat each logical input x_j as an independent formal variable. Public linear
operations and rotations do not increase total polynomial degree. A ct-ct
multiplication adds the degrees of its two inputs. Therefore after ct-ct
multiplicative depth d, every output slot has total degree at most 2^d.

The target power basis contains x_j^(r-1), of degree r-1. Hence

2^d >= r-1.

For r=2^ell >=4,

d >= ceil(log2(r-1)) = ell.

The total number of ct-ct multiplication gates is at least the ct-ct depth, so
every such circuit requires at least ell ct-ct multiplications.

B158 uses exactly ell.

Therefore:

`B158_CTCT_MULT_COUNT = OPTIMAL`

within this arithmetic SIMD model.

Special case r=2:
the target [1,x] needs zero ct-ct multiplication and should be handled
trivially, as in the original framework.

## Refined value model

Paper Algorithm 3 for the full-row r=2^ell call:
- 2ell-2 ct-ct Mult
- ell general plaintext-ciphertext Mult
- zero rotations inside EvalPower

B158:
- ell ct-ct Mult
- ell-1 RowRotation
- O(ell) scale-1 selector multiplications

At ell=15:

Paper:
- 28 relinearized/rescaled ct-ct Mult
- roughly 28 relin key-switches

B158:
- 15 relinearized/rescaled ct-ct Mult
- 14 rotation key-switches
- total KS-like count ~=29

Thus B158 increases the key-switch-like count by only one, not two.

It removes 13 full ciphertext tensor multiplications and their rescale steps.

Let:
- M = full ct-ct Mult cost,
- R = RowRotation cost,
- P_old = one original general plaintext multiplication cost,
- P_sel = one B158 scale-1 selector cost.

A coarse matched cost comparison is

Paper = (2ell-2)M + ell P_old

B158 = ell M + (ell-1)R + O(ell)P_sel.

For ell=15, ignoring the small selector-count constant only for intuition,
B158 gets a real latency win whenever the 13 removed full Mults outweigh
14 rotations plus selector overhead.

This is much more favorable than the previously recorded 15-rotation model.

## Prior-art audit

### ePrint 2026/975

Direct source inspection confirms the authors compute:
1. the x,x^2,x^4,... chain separately;
2. the masked-factor accumulator separately.

Algorithm 3 explicitly costs 2log(s)-2 ct-ct multiplications.

No accumulator/current-square co-packing is used.

Direct collision: NO.

### ePrint 2026/1401

The public ePrint abstract was recovered.

It is a TFHE multivariate functional-bootstrapping/LUT-compression paper based
on variable separation, additive inner representations, rounded logarithms,
division/modular-reduction constructions, and compressed multivariate LUTs.

It does not target the sparse BFV EvalPower/power-basis generation problem in
its stated contribution.

Therefore the earlier concern that 1401 might be a direct sequel that already
optimizes 975's BFV power generator is substantially reduced.

Direct collision from stated scope: NO.

### Postage-stamp / source-power methods

Prior PSI/OPE work uses extremal postage-stamp bases to reduce how many
encrypted source powers the client must provide, after which the server builds
the remaining powers with multiplication graphs.

This changes the input contract and communication/depth tradeoff. It does not
derive all powers from the single duplicated encrypted x by co-packing the
accumulator and current square in one ciphertext.

Direct collision: NO.

### Frobenius-based power generation

Packed finite-field FHE can sometimes obtain p-power maps with cheap Frobenius
automorphisms. This is a different plaintext-field mechanism and does not give
the required consecutive power table in the 2026/975 BFV setting with
T=65537 from free binary squaring.

Direct collision: NO.

### Closest conceptual prior: IBM rotate-and-multiply polynomial evaluation

IBM patent family:
- priority 2024-03-13
- US application published 2025-09-18
- US patent granted 2026-02-24

It uses duplicated SIMD slots, rotations, and multiplication by rotated
ciphertexts to reduce a vector of root factors into the single product
prod_i (x-r_i). It also discusses exploiting unused slots / merging
different-degree polynomial evaluations.

This is genuine conceptual prior art for:
- exploiting duplicated/free slots,
- rotate-and-multiply trees,
- SIMD co-location of intermediate work.

However its state invariant and output objective are different:
- it reduces many independent root factors to one product;
- it does not output the consecutive basis 1,x,...,x^(r-1);
- it does not maintain [power-basis accumulator | current x^(2^i)] and use
  the two BFV hypercube halves to fuse accumulator extension with binary
  powering.

Status:
`CLOSE_CONCEPTUAL_PRIOR / NOT_DIRECT_COLLISION`.

Therefore the novelty claim must NOT be "using spare SIMD slots and rotations
to reduce multiplication count." That is too broad.

The defensible narrow claim is:

"an optimal ct-ct-multiplication power-basis generator for the sparse BFV
EvalPower layout, obtained by co-packing the growing consecutive-power basis
and the current binary power in the two hypercube halves so each ciphertext
multiplication performs both accumulator extension and binary-power update."

## Current novelty status

DIRECT_PRIOR_COLLISION: NOT_FOUND
CLOSE_CONCEPTUAL_PRIOR: YES (IBM rotate-multiply polynomial evaluation)
NOVELTY: PROMISING_NOT_ESTABLISHED

The remaining novelty risk is a harder-to-find source using essentially the
same state invariant under another name. Native value remains unresolved.

## Next gate

The next decisive work is no longer another toy algebra test.

1. Check exact noise/scale recurrence for the selector-linear factor F_k.
2. Derive a minimal native patch specification that changes only the dominant
   MonomialGenExtra(r) call.
3. Do not execute it without PI authorization.
