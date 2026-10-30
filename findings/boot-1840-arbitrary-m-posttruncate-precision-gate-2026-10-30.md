# BOOT — 2026/1840 arbitrary-M post-Truncate precision / normalization gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 15/25

Status:
PASS_ERROR_AMPLIFICATION_LOCALIZES_TO_RADIX_ROW0 /
PASS_STATIC_PRECISION_VIABILITY_AT_50BIT_N65536_POINT /
FAIL_FREE_SCALAR_NORMALIZATION /
FULL_POSTTRUNCATE_PRECISION_MARGIN_TIGHT_UNVERIFIED /
POSTTRUNCATION_ROUTE_KEEP

## Parent result

Turn 14 derived the unique rank-1 linear localizer for M=d^n-delta:

y_i = x_i + alpha_i x_{n-1},
alpha_0 = 1-delta/d,
alpha_i = -delta/d^{i+1}, i>=1.

It exactly converts the arbitrary-M message recurrence to the standard radix-d recurrence but cannot be inserted before Truncate because it maps integer overflow to fractional overflow.

The surviving repair is:
Truncate old integer overflow first -> apply T -> ModRaise -> fresh integer overflow -> 1840-style shared-overflow A2B.

## Primary hypothesis

The post-Truncate route can survive the apparently huge max |alpha_i| about 2^31 for secp256k1-p because the rank-1 error is algebraically cancelled by the downstream local radix-difference operator; a simple normalization should not be needed to avoid a global 31-bit precision loss.

Cheapest falsifier:
derive the exact error transfer through D_std*T rather than bounding ||T|| in isolation, and prove whether any scalar normalization T/K can reduce the precision requirement without changing the downstream LUT domain.

## 1. Exact downstream error transfer

Let x be the exact post-Truncate message coefficient vector and let e be its coefficient error:
x_tilde = x+e, ||e||_infinity <= E.

Turn 14 established:
D_std T = D_G,

where D_std is the standard radix recurrence
(D_std y)_0=-d y_0,
(D_std y)_1=y_0-d y_1,
(D_std y)_i=y_{i-1}-d y_i for i>=2,

and for G_M(Y)=Y^n-Y+d-delta,

(D_G e)_0 = -d e_0 -(d-delta)e_{n-1},
(D_G e)_1 = e_0-d e_1+e_{n-1},
(D_G e)_i = e_{i-1}-d e_i, i>=2.

Therefore the exact error bounds at the radix outputs are:

row 0: |err_0| <= (d+|d-delta|)E.

For the close-prime regime delta>d:
d+|d-delta| = delta,
so
|err_0| <= delta E.

row 1:
|err_1| <= (d+2)E.

rows i>=2:
|err_i| <= (d+1)E.

Thus the naive operator norm of T is misleading:
- transformed coordinates y_i individually contain coefficients of size about delta/2;
- but those shared rank-1 terms cancel exactly in every local radix recurrence except row 0;
- the large precision penalty is localized to the least-significant radix equation.

Verdict:
PASS_ERROR_AMPLIFICATION_LOCALIZES_TO_RADIX_ROW0.

## 2. Sufficient exact-rounding condition

Let Delta be the CKKS scale at the localized digit representation and let E_abs bound the absolute coefficient error before T in the same unnormalized plaintext units.

The row-0 digit is separated by one integer unit, so a sufficient exact-rounding condition is:

delta * E_abs < Delta/2.

Equivalently:

E_abs < Delta/(2 delta).

If the only available deterministic pre-transform bound is E_abs < N, a sufficient condition is:

Delta > 2 N delta.

This is a much sharper criterion than the naive statement 'T costs 31 bits everywhere'.

## 3. secp256k1-p concrete threshold

For:
d=2,
delta=2^32+977=4,294,968,273,
N=2^16,

the sufficient threshold is:

log2(2 N delta) = 49.000000328... bits.

At the already-inspected 50-bit scale parameter point:

delta*N/2^50 = 0.2500000569.

So the encoding-rounding contribution alone remains below the 1/2 decision boundary.

The residual absolute margin is:

1/2 - delta*N/2^50 = 0.2499999431.

Equivalently, in pre-transform coefficient-error units the additional budget beyond N is:

2^50/(2 delta) - N = 65,535.97018...,

which is essentially one additional factor-of-two of the N-sized error budget.

Interpretation:
- the route is NOT statically killed by the 2^31 coefficient;
- but the deterministic margin is only about one bit at this concrete scale/ring point;
- actual arithmetic, Truncate, key-switch, linear-transform and ModRaise errors must fit inside that remaining margin.

Result:
PASS_STATIC_PRECISION_VIABILITY_AT_50BIT_N65536_POINT,
but FULL_POSTTRUNCATE_PRECISION_MARGIN remains UNVERIFIED.

## 4. No free scalar normalization

Consider replacing T by T/K for K>1 to reduce coefficient magnitudes before ModRaise.

After post-Truncate application and ModRaise, schematically:

z = (T x)/K + (T e)/K + J + eta_MR,

where J is the fresh integer overflow and eta_MR is ModRaise/evaluation error.

To reuse the original 1840 radix recurrence and D-entry / 2D-entry FBTs, the digit spacing must be restored from 1/K to 1.

There are only two generic choices.

Case A: multiply by K before the radix FBT.

Then:
K z = T x + T e + K J + K eta_MR.

If K is integer, KJ remains integer, but the original preexisting error amplification T e is restored exactly. The normalization gives zero benefit and additionally multiplies the ModRaise error by K.

Case B: do not multiply back.

Then the radix outputs are digit/K plus integer-overflow terms. The existing D-point FBT no longer sees unit-spaced representatives. Resolving the scaled digit grid requires K-times finer periodic resolution, equivalently an input domain/order enlarged by a factor K in the straightforward construction.

For K on the order of 2^31, this destroys the low-precision FBT advantage.

If K is non-integer, multiplying back also destroys the clean integer-overflow invariant needed for periodic removal.

Therefore:

FAIL_FREE_SCALAR_NORMALIZATION.

Scalar renormalization can move the precision cost, but cannot remove it while keeping the same radix-LUT interface.

## 5. Structural consequence

The correct precision picture is:

- NOT a global 31-bit loss;
- one high-sensitivity boundary equation (digit 0) with factor delta;
- all other digit equations retain constant-factor error amplification.

This suggests any future repair should target the boundary equation specifically rather than renormalize the whole vector.

Examples of future mechanisms, NOT established here:
- compute the least-significant digit through a separate small-domain correction;
- represent the boundary term in a split high/low form;
- exploit a different arbitrary-M polynomial G whose boundary row has smaller coefficient while preserving a usable local recurrence.

These are side ideas only.

## Verdict

PASS_ERROR_AMPLIFICATION_LOCALIZES_TO_RADIX_ROW0.
PASS_STATIC_PRECISION_VIABILITY_AT_50BIT_N65536_POINT.
FAIL_FREE_SCALAR_NORMALIZATION.

POST_TRUNCATION_PRE_MODRAISE_ROUTE = KEEP_BUT_TIGHT_MARGIN.

FULL_POSTTRUNCATE_PRECISION = UNVERIFIED.
ARBITRARY_PRIME_TWO_FBT_A2B = NOT_ESTABLISHED.

## Decision

Do not kill the post-Truncate arbitrary-M route on the basis of the 2^31 transform coefficient alone.

Do not spend a turn on global scalar normalization; that family is structurally cost-neutral or worse.

Next highest-information gate for this branch:
derive/upper-bound the actual error present immediately after Truncate in the 1840 refresh pipeline and test it against the exact row-0 budget Delta/(2delta). If that source-level error cannot fit the roughly one-bit remaining margin, kill the route before native implementation.

The independent 1836 fused-prime native task remains pending/execution-blocked:
BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked.