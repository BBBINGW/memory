# BOOT-B152 — Eight-LUT backend for B145 with hidden correction synthesis

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B151
- Status: PASS_ALGEBRA / PASS_OPERATION_COUNT_MODEL / PRECISION_NATIVE_GATED
- CODEX_REQUIRED: NOT YET

## Problem

B151 reduces B145 to twelve real 4096-point lookup outputs:

    F_k(b)=bit_k(b),
    D_k(b,c)=L(c)(F_k(b-1)-F_k(b)),   k=0,...,5,

with F5,D5 also serving as the carry affine state.

AKP/MVB shares ModRaise, CtS, EvalExp and root powers across outputs, but the source explicitly repeats the per-LUT Paterson-Stockmeyer EvalLUT branch. Thus reducing the number of LUT outputs still matters.

## Algebraic synthesis of lower-bit corrections

For k>=0 define

    Z_k(b) = product_{r=0}^{k-1} (1-F_r(b)),   Z_0=1.

Subtracting one changes bit k iff all lower k bits are zero. Exactly,

    F_k(b-1)-F_k(b) = Z_k(b)(1-2F_k(b)).

Therefore

    D_k = L(c) Z_k(b)(1-2F_k(b)).

Only D5 is needed immediately by the carry prefix. D0,...,D4 can be synthesized while the six-round prefix is already running.

## Eight direct LUT outputs

Request only:

    F0,F1,F2,F3,F4,F5,L,D5.

So the direct 4096-point MVB has eight real outputs, not twelve.

The carry prefix uses (F5,D5) immediately.

In parallel compute the lower corrections.

Let a_r=1-F_r.

Depth 1:
    p01=a0*a1,
    p23=a2*a3.                        [2 CMult]

Depth 2:
    Z3=p01*a2,
    Z4=p01*p23.                       [2 CMult]

The other prefixes are free:
    Z1=a0,
    Z2=p01.

Depth 3:
    A1=L*Z1,
    A2=L*Z2,
    A3=L*Z3,
    A4=L*Z4,
    D0=L*(1-2F0).                     [5 CMult]

Depth 4:
    Dk=Ak*(1-2Fk), k=1,...,4.         [4 CMult]

Total correction synthesis:
- 13 CMult;
- multiplicative depth 4.

The carry prefix has depth H=ceil(log2 u). At n=256, B=64:
    u=ceil(256/6)=43,
    H=6.

Hence the four-level correction synthesis completes before the six-level carry prefix. After both are ready, five final bit corrections F_k + carry*D_k for k=0,...,4 use one further level. The MSB is already the prefix intercept.

Critical post-LUT depth therefore remains:

    max(4,6)+1 = 7,

exactly the same as B151's twelve-LUT construction.

## Operation-count tradeoff

B151:
- 12 per-LUT EvalLUT branches;
- 6 prefix CMult;
- 5 final correction CMult;
- post-LUT non-LUT CMult = 11.

B152:
- 8 per-LUT EvalLUT branches;
- 13 correction-synthesis CMult;
- 6 prefix CMult;
- 5 final correction CMult;
- post-LUT non-LUT CMult = 24.

So B152 spends 13 additional ordinary CMults to eliminate four full 4096-point EvalLUT branches.

Source-backed complexity:
- 1264 Appendix C.1: MVB shares all steps through EvalPower, but repeats the PS EvalLUT for every LUT output.
- 1840 Section 4: a p-entry LUT has PS cost on the order of sqrt(p) ciphertext multiplications; its multi-output second FBS cost scales linearly with the number of jointly evaluated output functions.

At p=4096, each removed branch is therefore a roughly sqrt(4096)=64-scale PS object (up to method constants/shared-power accounting). Four removed branches represent an O(256)-scale reduction in LUT-evaluation multiplications, versus 13 extra CMults.

The exact constant must be measured in the chosen library, but the source-level operation-count sign is strongly favorable.

## Within-2368 timing sanity check

2368 provides an unusually useful same-implementation comparison:
- sign path: one Root_4096 and one complex lookup = two real LUTs, plus prefix, around 16-18 s;
- digit-function path: same one Root_4096 architecture but four real LUTs, plus prefix/final correction, around 22-24 s.

At matched u values, adding two real LUT branches costs roughly 5-6 s in that HEaaN2/8-thread implementation.

A crude linear extrapolation from four to twelve LUTs would put the B151 lookup-heavy path in the low-to-high 40-second range on that environment, not 3x the full four-LUT latency, because root production and power generation are shared.

B152 removes one third of those per-output branches. This timing extrapolation is diagnostic only; it is not a matched prediction for OpenFHE/1869.

## Precision caveat

The synthesized D0,...,D4 are products of approximate bit/range outputs rather than direct Hermite-cleaned LUT outputs. Their exact targets remain in {0,±1}, but error is multiplied through up to four additional levels before the final correction.

This does not change multiplicative depth of the whole post-LUT path because the work is hidden under the prefix, but it can change:
- required scale per level;
- output error;
- failure margin after final bit rounding.

A native or detailed CKKS error calculation is therefore still required before claiming correctness at the same 8-10 bit output precision as the source implementations.

## Decision

- Algebra: PASS.
- Direct LUT outputs: 12 -> 8.
- Critical post-LUT depth: unchanged at 7 for n=256.
- Non-LUT CMult: 11 -> 24.
- Source-level operation count: favorable because four O(sqrt(4096)) PS branches are replaced by 13 CMult.
- Native/Codex: not yet; first perform a conservative error/modulus headroom gate.

B152 becomes the preferred B145 backend over the twelve-LUT baseline.
