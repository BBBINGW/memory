# BOOT-B155 — Minimum radix lower bound for one-window arithmetic A2B

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145
- Status: PASS_LOCAL_IMPOSSIBILITY / B=64 MINIMAL_POWER_OF_TWO_UNDER_E=16
- CODEX_REQUIRED: NO

## Question

Can B145 reduce the radix from B=64 to B=32, shrinking the one-bootstrap lookup domain from B^2=4096 to 1024, while retaining deterministic recovery from one adjacent window under the source-backed overflow bound |U|<=16?

## Abstract local-window model

After the B145 adjacent cancellation and public shift E, one window has the exact form

    w = B d + a + r   (mod B^2),

where:
- d in Z_B is the target high radix digit;
- a in Z_B is the previous digit;
- U in [-E,E] is the remaining boundary overflow;
- r=E+U is an unknown integer in [0,2E].

A deterministic one-window recovery algorithm receives only w (equivalently its quotient/remainder b,c modulo B) and must recover d for every allowed d,a,r.

## Collision lower bound

Suppose B<=2E.

Then both

    r0=0
and
    r1=B

belong to the allowed interval [0,2E].

Choose any 1<=d<=B-1 and any a in Z_B.

Instance A:
    true digit d_A=d,
    previous digit a_A=a,
    r_A=0.

Its window is

    w_A = B d + a.

Instance B:
    true digit d_B=d-1,
    previous digit a_B=a,
    r_B=B.

Its window is

    w_B = B(d-1)+a+B
        = B d+a
        = w_A.

Thus the same observed window is compatible with two distinct correct high digits:

    d_A=d != d-1=d_B.

Therefore no deterministic function

    g : Z_(B^2) -> Z_B

can recover the high digit correctly for every allowed overflow whenever B<=2E.

This argument is information-theoretic inside the local-window model; it does not depend on a particular carry recurrence or interpolation method.

## Consequence for the 1869 bound

2026/1869 supplies the conservative refreshed-overflow bound

    E=16.

Hence any deterministic B145-style single-window digit recovery valid for the full source-supported overflow range requires

    B>32.

The radix is chosen as a power of two, B=2^s. Therefore the smallest admissible radix is

    B_min=64.

Consequently the smallest corresponding direct window domain is

    B_min^2=4096.

So the B145 choice B=64 is not merely a heuristic tradeoff; it is minimal among power-of-two radices under:
1. the full worst-case bound |U|<=16;
2. one adjacent B^2 window per digit position;
3. deterministic local LUT recovery before the global carry scan.

## Scope

This is NOT a universal impossibility of radix 32.

B=32 could become possible if one changes the model, for example:
- prove a strictly smaller overflow support, such as |U|<=15 with the required failure probability;
- use information from multiple adjacent windows jointly before the LUT;
- keep an additional side channel/state that distinguishes the endpoint overflow;
- accept probabilistic rather than full-range correctness.

Those alternatives need separate analysis.

## Decision

PASS_LOCAL_IMPOSSIBILITY.

For the current source-faithful worst-case model, B=64 is the minimum power-of-two radix for a deterministic one-window construction.

This strengthens B145:
- the 4096-point domain is not an avoidable artifact of a loose recurrence;
- reducing it to 1024 requires a new source bound or a richer observation model.
