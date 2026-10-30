# BOOT — S2 Non-Frobenius Basis Lower-Bound Gate

**Date:** 2026-10-30  
**TRACK_ID:** BOOT  
**ACTIVE_SUBLINE:** B158_CHECKPOINT_DECOUPLED_HALF_BASIS  
**Logical turn:** Research Turn 24/25 retry; same turn, not a new research turn  
**Result:** FAIL_AFFINE_KUMMER_BASIS_RESCUE / GENERAL_DENSE_NONAFFINE_BASIS_UNCLEAR

## Primary hypothesis

For the surviving s=2 RMFE construction with p=5, e=4, eta=125, k=5, w=512 inside the pinned HElib m=32768 plaintext geometry, a non-Frobenius target generator / G-basis redesign might reduce the worst native HElib decoder-mask L1 norm below

263853 / 10 = 26385.3,

while preserving the degree-125 RMFE correctness interface and the trace/automorphism implementation.

The cheapest decisive test is to exhaust all lifted interpolation points in G for the full affine/Kummer generator family before considering genuinely dense non-affine generators.

## Fixed baseline

R16 worst native projection-mask norms:
- L1 = 263853
- L2 = 8249.83
- Linf = 312

Target 10x gate:
- worst L1 < 26385.3

The degree-eta decoder for k=5 is constrained only through degree

eta(k-1) = 125*4 = 500,

so the favorable extension used here sets the remaining 11 power-basis coordinates to zero.

## Pinned native tower

The full plaintext cyclotomic ring is

R = (Z/625Z)[X]/(X^16384+1).

Because 182^2 = -1 mod625,

X^16384+1 = (X^8192+182)(X^8192-182).

For the s=2 subfield tower, use the relative generator alpha=X^8.  In each physical slot the target subring G' has degree 1024 over Z/625 and degree 512 over the base G=GR(625,2).

Let y be an abstract base generator satisfying y^2=443.  The two possible global embeddings of y into the two physical slots are represented in the full cyclotomic coefficient basis by

orientation A:
y = -221 X^4096 -221 X^12288,

orientation B:
y = 222 X^4096 -222 X^12288.

These are the two Frobenius orientations of the same degree-2 base ring.

For the relative Kummer polynomial T^512-y, the trace-dual of the power basis is

beta_0 = 1/512,
beta_j = alpha^{-j}/512, 1<=j<=511.

Since 512^{-1}=448=-177 mod625 and X^16384=-1,

beta_j = 177 X^(16384-8j)

for 1<=j<=500 in the centered full-ring coefficient representation.  beta_0 has centered coefficient -177.

## Exact lifted-point enumeration

Every x in G is uniquely x=a+b y with a,b in Z/625.

Its powers are updated exactly by

A_{j+1}=A_j a + 443 B_j b mod625,
B_{j+1}=A_j b + B_j a mod625,

starting from (A_0,B_0)=(1,0), so x^j=A_j+B_j y.

For evaluation at x, the correctness-relevant trace mask is

theta_x = sum_{j=0}^{500} x^j beta_j.

For j=1..500 the supports produced by beta_j, beta_j X^4096, and beta_j X^12288 are pairwise disjoint in the canonical coefficient basis.  A collision would require |j-j'|>=512, impossible in the range 0..500.  Hence L1/L2/Linf are accumulated coefficientwise with no hidden cancellation.

I exhaustively enumerated all

|G| = 625^2 = 390625

lifted points under both physical-slot orientations.

Finite interpolation points must have pairwise-unit differences.  In GR(625,2), x-x' is a unit iff their residues modulo 5 are distinct in F25.  Therefore the exact five-point optimization reduces to retaining the best lift in each of the 25 residue classes and then choosing distinct classes, with the projective infinity point handled separately.

Best relevant representatives:

- x=0:
  L1=177, L2=177, Linf=177

- x=24 and x=26:
  L1=78217
  L2=4035.260710288742
  Linf=302

- x=2 and x=3:
  L1=78303
  L2=4038.264354893077
  Linf=312

No third nonzero residue class has best L1 below 78303.

Thus a legal set such as

{infinity, 0, 24, 26, 2}

has exact worst norms

L1 = 78303
L2 = 4038.264354893077
Linf = 312.

This is the optimal worst-L1 value over all lifted G-points for the aligned Kummer basis.

Compared with R16:

263853 / 78303 = 3.3696410099x
8249.83 / 4038.264354893077 = 2.0429147958x.

So the best lifted-point rescue gains only about 1.75 bits in L1, leaving a factor

78303 / 26385.3 ~= 2.9677

still missing from the 10x gate.

## Why this exhausts the affine/Kummer non-Frobenius family

Consider

zeta = a0 + c alpha^r,

with a0 in G, c in G^x, and gcd(r,512)=1.

### Affine shift/scale

Let z=alpha^r and write zeta=a0+c z.

For any polynomial P,

P(zeta)=Q(z), where Q(T)=P(a0+cT).

Evaluation at x in the zeta coordinates equals evaluation at

y0=(x-a0)/c

in the z coordinates.

Since c is a unit, affine transformation preserves pairwise-unit differences.  The exhaustive screen already covers every y0 in G.  Therefore every shift a0 and unit scale c is already included.

### Non-Frobenius Kummer exponent

For z=alpha^r,

beta_j^(r) = z^{-j}/512 = X^{-8rj}/512.

Because r is odd, multiplication by r permutes the relevant monomial residues.  For 0<=j<=500, supports remain collision-free even after the G shifts by 0,4096,12288; a collision would again require a j-difference of at least 512.

Thus changing r only permutes/signs canonical coefficient locations and leaves the coefficient magnitudes, hence L1/L2/Linf, unchanged.

Therefore the complete affine/Kummer family

zeta=a0+c alpha^r

is covered by the exhaustive lifted-point computation and cannot reach the 10x gate.

## What this does not prove

This is NOT a universal impossibility theorem for every degree-512 generator zeta=f(alpha).

A genuinely dense non-affine generator can induce a dense power-basis change and a different inverse-transpose trace-dual geometry.  The affine/Kummer permutation reduction no longer applies, and no rigorous lower bound was obtained that forces every such dense basis to have worst native L1 >=26385.3.

Therefore:

GENERAL_DENSE_NONAFFINE_BASIS = UNCLEAR,

not IMPOSSIBLE.

However, all low-regret sparse freedoms have failed and the dense branch has no positive conditioning signal.

## Decision

- Teichmuller point choice: killed by earlier exhaustive screen.
- Arbitrary lifted G-point choice: FAIL 10x gate.
- Frobenius generator conjugation: exact norm invariance.
- Affine generator shift/scale: fully covered; FAIL.
- Non-Frobenius Kummer exponents: exact norm invariance; FAIL.
- General dense non-affine power generator: UNCLEAR but PARK.

Scientific disposition:

S2_CONDITIONING_RESCUE = PARK.

The obstruction is best localized as incompatibility between RMFE trace-dual geometry and HElib's concrete cyclotomic coefficient-rounding basis, not a missed interpolation point or sparse generator choice.

No native experiment is justified for this branch.

## Next boundary

Do not spend the next research turn on exotic dense-generator search.  Reprioritize within BOOT to a mechanism that changes operation ordering or shares expensive linear work without depending on a lower-conditioned RMFE decoder.
