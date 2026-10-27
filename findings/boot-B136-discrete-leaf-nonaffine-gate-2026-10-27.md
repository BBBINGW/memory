# BOOT-B136 — Discrete / finite-domain independent-leaf non-affine gate

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Target: Liang–Ding, ePrint 2026/1779
- Status: COMPLETE
- CODEX_REQUIRED: NO
- Native benchmark: NOT JUSTIFIED
- Novelty: NOT_ESTABLISHED

## Question

After one ring-switch split, can restricting CKKS plaintext values to a finite/discrete domain permit a genuinely non-affine slotwise LUT to be evaluated independently on the leaves and then correctly recombined, without traditional slot recovery?

## Source status

The official ePrint abstract states that unrestricted real CKKS inputs admit independent leaf evaluation exactly for affine continuous slotwise functions. The current ePrint full-text PDF remained blocked to the research MCP, so this iteration does **not** claim to have read the exact theorem/proof text.

The authors' public code is available and exposes the operational split/merge interface. Its ring-packing implementation states, for one split,

[
m(X)=m_0(Y)+X m_1(Y),qquad Y=X^2,
]

and Merge reverses the same decomposition.

## Two-slot / two-leaf algebra

Fix a child-ring slot (Y=eta) and choose (zeta) with (zeta^2=eta). Let the two parent slots be

[
x=m(zeta),qquad y=m(-zeta).
]

Then the two leaf values are

[
a=m_0(eta)=rac{x+y}{2},
qquad
b=m_1(eta)=rac{x-y}{2zeta}.
]

If independent leaf functions (A) and (B) are followed only by the standard linear merge, correctness for a target slotwise function (f) requires

[
f(x)=A(a)+zeta B(b),qquad
f(y)=A(a)-zeta B(b).
]

Equivalently,

[
f(x)+f(y)=2A!left(rac{x+y}{2}ight),
]

and

[
f(x)-f(y)=2zeta B!left(rac{x-y}{2zeta}ight).
]

After the public slotwise normalization (bmapsto zeta b=(x-y)/2), the finite-domain feasibility condition becomes:

1. whenever (x+y=x'+y'),
   [
   f(x)+f(y)=f(x')+f(y');
   ]
2. whenever (x-y=x'-y'),
   [
   f(x)-f(y)=f(x')-f(y').
   ]

These collision conditions are necessary and sufficient for the one-split noiseless algebraic model: if they hold, the two leaf lookup functions can be defined consistently on the finite sum/difference sets.

## Standard integer LUT domain: FAIL

For

[
D_p={0,1,ldots,p-1},
]

the sum-collision condition alone forces affine closure.

For every (k=0,ldots,p-2), the two pairs ((k,1)) and ((k+1,0)) have the same sum (k+1). Therefore

[
f(k)+f(1)=f(k+1)+f(0),
]

so

[
f(k+1)-f(k)=f(1)-f(0)
]

for every (k). Hence

[
f(k)=ak+b
]

on all of (D_p).

Thus discretizing to a consecutive integer alphabet does **not** evade the affine obstruction; no continuity assumption is needed for this finite-grid result.

### Exhaustive smallest cases

For maps (f:D_p	o D_p):

- (p=2): 4/4 maps satisfy the leaf equations, but all four are affine on a two-point set; genuinely non-affine count = 0.
- (p=3): 5/27 maps satisfy them: the 3 constants, identity, and reversal; genuinely non-affine count = 0.
- (p=4): 6/256 maps satisfy them: the 4 constants, identity, and reversal; genuinely non-affine count = 0.

More generally, if the codomain is also (D_p), affine closure plus range preservation leaves only constants, identity, and reversal.

**Decision for the originally proposed domain (D={0,ldots,p-1}): FAIL_NONAFFINE_ESCAPE.**

## General finite sets: finite-domain affine closure is false

The stronger statement “every finite real domain still forces affine (f)” is false.

Take

[
D={0,1,3}
]

and the genuinely non-affine LUT

[
f(0)=0,qquad f(1)=0,qquad f(3)=1.
]

The unordered sums of elements of (D) are all distinct:

[
0,1,2,3,4,6,
]

and the nonzero ordered differences are also unique:

[
pm1,pm2,pm3.
]

Therefore the two collision conditions impose no nontrivial consistency relation, and the required leaf LUTs are well-defined. For example,

[
A((x+y)/2)=rac{f(x)+f(y)}2,
qquad
C((x-y)/2)=rac{f(x)-f(y)}2,
]

with the odd leaf normalized by the public root factor (zeta), gives correct recombination.

This is a minimal 3-point explicit non-affine escape.

More generally, a finite set with Sidon/Golomb-type low additive collision can admit many or even all LUTs under the one-split algebraic criterion.

## Value / prior-art / cost / security gates

### Prior art

No direct hit was found in the initial search for “ring switching + finite-domain/Sidon-codebook independent leaf LUT”.

However, ePrint 2026/1200 (Dumezy–Suvanto, *Character Block Encodings for Discrete CKKS*) is strongly adjacent prior art: it changes the representation of a finite alphabet so that every LUT becomes an affine plaintext map in one multiplicative level. Therefore “change the finite-alphabet representation to escape nonlinear LUT cost” is not novel by itself.

The scalar Sidon-codebook construction differs because it keeps one scalar symbol per logical slot and targets the specific split/merge separability condition, but novelty is not established.

### Cost

For a collision-free alphabet of size (t), the derived even-leaf table lives on up to

[
|D+D|=t(t+1)/2
]

points, and the normalized odd-leaf table on up to

[
|D-D|=t(t-1)+1
]

points.

Thus a generic arbitrary LUT can expand from (t) input points to (Theta(t^2)) leaf-domain points. A direct polynomial interpolation can therefore have worst-case degree (Theta(t^2)), versus degree at most (t-1) for the original LUT.

For the explicit (D={0,1,3}), (f=(0,0,1)) example, direct interpolation has degree 2, while the induced even/odd leaf interpolants already reach degree 5.

This makes generic arbitrary-LUT value doubtful despite the smaller leaf ring.

### Encoding / precision

Integer Sidon/Golomb codebooks of size (t) require substantially larger span than the consecutive alphabet; asymptotically the natural scalar span is quadratic in (t). That increases CKKS dynamic range and leaves less precision/noise margin. Irregular interpolation nodes may further worsen coefficient growth/conditioning.

The public (zeta) and (zeta^{-1}) slotwise normalizations have unit magnitude and do not themselves create a new cryptographic assumption, but they are extra arithmetic unless fused with existing transforms.

### Security

The algebraic escape does not require a new secret distribution or a new hardness assumption. It changes plaintext representation/domain, so the main new risks are correctness, precision/noise, and cost rather than RLWE security. This remains conditional on using the authors' ring-switching construction/parameters correctly; the full 2026/1779 paper has not been independently audited here.

## B136 decision

- Standard consecutive discrete LUT domain (D={0,ldots,p-1}): **FAIL** — affine closure holds exactly.
- Universal finite-domain impossibility: **REFUTED** — nonuniform finite codebooks can admit genuinely non-affine independent-leaf LUTs.
- Generic scalar-codebook research value: **PARK / LOW-TO-MEDIUM** — algebraically real, but generic leaf LUT domains grow quadratically and representation-change prior art (2026/1200) is stronger on generic LUT depth.
- Novelty: **NOT_ESTABLISHED**.
- Codex/native: **NO**.

## Recommended next action

Do not implement the generic Sidon-codebook construction.

Highest-value follow-up, if continuing this family, is a paper-only algebraic/source scout asking whether there is a **structured finite encoding already natural in discrete CKKS** for which:
1. the split-leaf sum/difference functions remain low-degree / low-depth,
2. one logical value does not require a large multi-slot block,
3. the construction is not subsumed by 2026/1200,
4. and the full 2026/1779 theorem does not already cover it.

Otherwise move to a fresh bootstrapping candidate. If ePrint 2026/2119 full PDF appears in `papers/supplied/`, immediately preempt this scout and resume B135 fairness audit.
