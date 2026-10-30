# BOOT — 2026/1840 arbitrary-M rank-1 localization / pre-truncation obstruction gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 14/25

Status:
PASS_EXACT_RANK1_LOCALIZATION_OF_ARBITRARY_M_MESSAGE_RECURRENCE /
FAIL_DIRECT_PRETRUNCATION_TRANSFER_TO_REFRESHI /
PASS_UNIQUE_LINEAR_PRECONDITIONER_OBSTRUCTION /
POST_TRUNCATION_PRE_MODRAISE_REPAIR_PROMISING_UNVERIFIED /
1836_NATIVE_SURVIVOR_UNCHANGED

## Context

Turn 13 established that 2026/1840's published two-FBT A2B is formally scoped to power-of-two digit bases and plaintext modulus d^n; Remark 1's arbitrary-M ring existence does not itself carry the Section-4 A2B theorem.

Turn 14 tests the strongest possible cheap repair:
for M close to d^n, can a public linear coefficient transform restore the exact local radix recurrence used by 1840, without introducing a new nonlinear/bootstrap step?

Source:
papers/supplied/2026-1840.pdf, blob fb5f5c20a61030b8a1ecfdb150cf4602d4dcc4ea.

## Primary hypothesis

For M=d^n-delta, choose

G_M(Y)=Y^n-Y+d-delta,
t=Y-d.

Because G_M(d)=M, this gives the arbitrary-M quotient ring of Remark 1.

Hypothesis:
a rank-1 public coefficient transform can convert the arbitrary-M triangle coefficients into the same local radix-d recurrence as the d^n construction, and can be inserted directly into the existing special-d0 Z-to-R step of RefreshI without invalidating integer-overflow truncation.

Cheapest decisive test:
derive the unique linear transform T satisfying the standard radix difference equations exactly, and inspect whether T maps an integer overflow vector I in Z^n back to an integer vector.

## 1. Arbitrary-M coefficient recurrence

Write

c := d-delta,
G_M(Y)=Y^n-Y+c.

Modulo G_M:

Y^n = Y-c.

For any coefficient vector x=(x_0,...,x_{n-1}), multiplication by t=Y-d gives coefficient equations:

row 0:
-d x_0 - c x_{n-1},

row 1:
x_0 - d x_1 + x_{n-1},

rows i>=2:
x_{i-1} - d x_i.

For a triangle ciphertext normalized by its scale, x=I+g with integer overflow I and message part g=t^{-1}[m], these rows equal the corresponding radix digits plus the same linear operator applied to I.

## 2. Exact rank-1 transform

Define y=T x by

y_i = x_i + alpha_i x_{n-1},

with

alpha_0 = c/d = 1-delta/d,

alpha_i = -delta/d^{i+1},  1<=i<n.

Then:

-d y_0
= -d x_0 - c x_{n-1},

y_0-d y_1
= x_0-d x_1+x_{n-1},

and for every i>=2:

y_{i-1}-d y_i
= x_{i-1}-d x_i.

The second identity follows because

alpha_0-d alpha_1 = 1,

and the later identities because

alpha_{i-1}-d alpha_i = 0.

Therefore T restores EXACTLY the local radix recurrence used in 1840's warm-up:

-d y_0 = digit_0 + transformed-overflow row,

y_{i-1}-d y_i = digit_i + transformed-overflow row.

This is not approximate and does not depend on CKKS noise.

## 3. T strictly generalizes 1840 special-d0

When delta=0, M=d^n and c=d:

alpha_0=1,
alpha_i=0 for i>=1.

Hence:

y_0=x_0+x_{n-1},
y_i=x_i for i>=1,

which is exactly 1840's special-d0 preprocessing.

So the source's special-d0 transform is the delta=0 endpoint of this rank-1 arbitrary-M localization.

## 4. T is the unique exact linear localizer

Let D_std be the standard local radix-d difference operator:

(D_std y)_0=-d y_0,
(D_std y)_1=y_0-d y_1,
(D_std y)_i=y_{i-1}-d y_i for i>=2.

Let D_G be the arbitrary-G_M operator from Section 1.

Any linear transform T satisfying

D_std T = D_G

must equal

T = D_std^{-1} D_G,

because D_std is invertible over Q.

The rank-1 matrix above is exactly this unique transform.

Thus there is no alternative exact linear preconditioner that preserves the same local recurrence while avoiding its coefficient arithmetic.

## 5. Direct insertion before Truncate FAILS

1840 RefreshI performs the special-d0 linear transformation BEFORE CKKS.Truncate.

This works at delta=0 because the special-d0 transform has integer coefficients and therefore maps integer overflow I in Z^n to another integer overflow vector.

For arbitrary M, the unique transform sends

J_i = I_i + alpha_i I_{n-1}.

For any nonzero 0<delta<d^n, not all alpha_i are integers.

In fact, for all alpha_i (i>=1) to be integral one would need d^{i+1} | delta for all i<n, hence d^n | delta, impossible for 0<delta<d^n.

So generic arbitrary-M localization turns the old integer overflow into fractional overflow BEFORE Truncate.

CKKS.Truncate in 1840 is explicitly used to remove an INTEGER overflow while retaining the fractional message.

Once J is fractional, direct reuse of the same truncation argument is invalid.

Therefore:

PASS message-localization algebra,
but
FAIL direct pre-truncation transfer to RefreshI.

## 6. Explicit secp256k1-p obstruction

For d=2, n=256,

M=p=2^256-delta,
delta=2^32+977=4,294,968,273.

Then:

alpha_0 = (2-delta)/2 = -2,147,484,135.5,

alpha_1 = -delta/4 = -1,073,742,068.25,

and so on.

Take an integer overflow vector with I_{255}=1 and all other I_i=0.

Then transformed overflow coordinate

J_0=alpha_0

is a half-integer.

So the exact localizing transform immediately destroys the integer-overflow invariant required by pre-truncation RefreshI.

## 7. Exact toy verification

Independent exact-rational algebra was checked exhaustively on:

- d=2,n=4,M=13 with G=Y^4-Y-1;
- d=2,n=5,M=29 with G=Y^5-Y-1;
- d=4,n=3,M=61 with G=Y^3-Y+1.

For every message m in [0,M), the transformed coefficients satisfy the exact radix recurrence.

Random integer overflow vectors were also injected; in all tested cases the recurrence remained exact when the transformed overflow J=T I was included.

This confirms the symbolic derivation and isolates integrality, not message algebra, as the blocker.

## 8. A nontrivial repair route appears

The obstruction is ordering-specific:

the problem arises because T is applied to ciphertext coordinates while the OLD overflow is still present.

A plausible repair is:

1. ordinary Z-to-R / coefficient exposure under G_M;
2. Truncate first, while overflow coordinates are still integer;
3. apply the rational rank-1 transform T to the message-only residue;
4. then ModRaise;
5. ModRaise introduces a NEW integer overflow directly in the transformed coordinates;
6. continue with 1840-style R-to-C, shared-overflow cancellation, and two-FBT A2B.

This would move the new representation transform ACROSS the truncation boundary.

It is exactly the kind of nontrivial representation/ordering modification sought by the research philosophy.

However this repair is NOT proved in this turn.

Open blockers:
- whether T can be implemented between Truncate and ModRaise without an extra bootstrap;
- CKKS scale/noise amplification from max |alpha_i|;
- whether the modified R-domain linear map can be folded into existing transforms cheaply;
- root/embedding conditioning for G_M;
- full correctness after fresh modulus-raise overflow.

## 9. Concrete conditioning warning for secp256k1-p

For secp256k1-p:

max_i |alpha_i| = |alpha_0| about 2^31.

The L1 norm of the rank-1 correction vector is about 2^32.

So even if post-truncation insertion is type-correct, it may amplify CKKS error by roughly 31 bits in the worst affected coordinate unless the transform/scale is renormalized.

This is the next cheap falsifier, not a result of the present turn.

## Verdict

PASS_EXACT_RANK1_LOCALIZATION_OF_ARBITRARY_M_MESSAGE_RECURRENCE.
PASS_GENERALIZATION_OF_SPECIAL_D0.
PASS_UNIQUE_LINEAR_PRECONDITIONER_OBSTRUCTION.
FAIL_DIRECT_PRETRUNCATION_TRANSFER_TO_REFRESHI.

POST_TRUNCATION_PRE_MODRAISE_REPAIR = PROMISING_UNVERIFIED.

The 1836 fused-prime A2B native survivor is unchanged and remains pending/execution-blocked:
BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.

## Decision

Do NOT claim arbitrary-prime two-FBT A2B yet.

KEEP the post-Truncate/pre-ModRaise rank-1 localization as a new positive BOOT candidate.

Next highest-information static gate:
test whether the post-truncation transform can be normalized/implemented with acceptable precision cost for secp256k1-p, or whether the approximately 2^31 coefficient amplification kills the route before native implementation.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked.