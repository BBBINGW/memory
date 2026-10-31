# BOOT RMFE recryptEkey Noise / intFactor Bookkeeping Gate

Date: 2026-11-01
Session: 密码学 16.0
Logical Research Turn: 19/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task

`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01`

remains RUNNING/PENDING and is not modified, restarted, resubmitted, or treated as complete.

This turn closes the remaining caveat left by Turn 18:

> If five stock `recryptEkey` reconstructions are replaced by one reconstruction of the aggregated public pair ((A,B)), does HElib's BGV `noiseBound/intFactor` bookkeeping remain sound enough to use the same local correctness/capacity gate?

No native execution, source mutation, key generation, parameter change, or benchmark occurred.

Pinned source:

`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Relevant source:

- `include/helib/Ctxt.h`;
- `src/Ctxt.cpp`;
- `src/keys.cpp`;
- `src/norms.cpp`.

Durable prerequisites:

- Turn 16: `intFactor` semantics are valid for the single-reconstruction path;
- Turn 18: the one reconstruction is an exact `CtxtPart`/handle identity relative to five stock reconstructions followed by public (Y^i) shifts and addition.

## 1. HElib BGV capacity depends only on primeSet and noiseBound

Pinned `Ctxt::totalNoiseBound()` returns exactly

[
	exttt{noiseBound}
]

for BGV.

Pinned `Ctxt::capacity()` is

[
rac{
log Q-log(max(	exttt{noiseBound},1))
}{log 2},
]

where (Q) is the product of the current `primeSet`.

Pinned `Ctxt::isCorrect()` likewise applies a monotone threshold to `totalNoiseBound` at the same modulus.

Thus at a fixed BGV `primeSet`:

[

u_1le
u_2
quadLongrightarrowquad
operatorname{capacity}_1geoperatorname{capacity}_2.
]

`ptxtMag` and `ratFactor` do not enter the BGV capacity ledger.

Therefore the bookkeeping question reduces to:
1. do fused and comparator states have the same `primeSet`?
2. is fused `noiseBound` no larger?
3. is `intFactor` semantically identical?

## 2. One stock reconstruction ledger

Let

[
E=	exttt{recryptEkey}
]

with

- BGV `noiseBound` (
u_E);
- plaintext space (P_{m boot});
- prime set (S_E);
- `intFactor=1`.

Turn 16/source audit established the last item.

For one public post-round pair ((a_i,b_i)), stock HElib executes

[
C_i=operatorname{Rec}(a_i,b_i):
]

[
	exttt{ctxt = recryptEkey};
quad
	exttt{ctxt.multByConstant}(b_i);
quad
	exttt{ctxt.addConstant}(a_i).
]

Define HElib's canonical-embedding norm

[
|u|_{m emb}
=
	exttt{embeddingLargestCoeff}(u).
]

Pinned BGV `multByConstant(const ZZX&)` sets

[

u
leftarrow

ucdot|b_i|_{m emb}.
]

Pinned BGV `addConstant(const ZZX&)` then adds

[
|f|,|a_i|_{m emb},
]

where

[
f=
operatorname{balRem}
left(
	exttt{intFactor}cdot Q_E,
P_{m boot}
ight)
]

with (Q_E) the prime-product modulo the plaintext space.

Since every reconstruction begins from the same `recryptEkey`, all branches have the same (f).

Therefore the stock branch ledger immediately after reconstruction is

[
oxed{

u_i
=

u_E|b_i|_{m emb}
+
|f||a_i|_{m emb}.
}
]

Neither operation changes `primeSet` or `intFactor`.

## 3. Public (Y^i) shifts do not increase that ledger

The current envelope has

[
Y=X^{1024}.
]

For any primitive (m)-th root (zeta),

[
|zeta^{1024i}|=1.
]

Hence

[
|Y^iu|_{m emb}
=
|u|_{m emb}.
]

If the five stock reconstruction ciphertexts are hypothetically shifted by public polynomial multiplication (Y^i), the BGV `multByConstant` size is exactly 1 mathematically, so the noise ledger remains (
u_i).

All five shifted ciphertexts have identical:

- `ptxtSpace=P_boot`;
- `primeSet=S_E`;
- `intFactor=1`.

Therefore `Ctxt::addCtxt` triggers neither factor harmonization nor prime-set mod-up. Its final source step simply adds the noise bounds.

The five-stock-reconstruction comparator state therefore has

[
oxed{

u_{m sep}
=
sum_{i=0}^{4}
left(

u_E|b_i|_{m emb}
+
|f||a_i|_{m emb}
ight).
}
]

Its `intFactor` remains exactly 1.

## 4. Fused reconstruction ledger

Turn 18 defined

[
A=sum_{i=0}^{4}Y^ia_i,
qquad
B=sum_{i=0}^{4}Y^ib_i.
]

The fused HElib path executes

[
operatorname{Rec}(A,B)
]

from the same `recryptEkey`.

Therefore its source-level BGV ledger is

[
oxed{

u_{m fused}
=

u_E|B|_{m emb}
+
|f||A|_{m emb}.
}
]

Using the canonical-embedding triangle inequality and (|Y^iu|_{m emb}=|u|_{m emb}),

[
|B|_{m emb}
=
left|sum_iY^ib_iight|_{m emb}
le
sum_i|b_i|_{m emb},
]

and

[
|A|_{m emb}
le
sum_i|a_i|_{m emb}.
]

Hence

[
oxed{

u_{m fused}
le

u_{m sep}.
}
]

This is the decisive bookkeeping result.

## 5. Why the tighter fused bound is legitimate

This is not an unjustified assumption that five independent errors cancel.

The five stock reconstructions all copy the **same** `recryptEkey`. The encrypted boot-key error is therefore one common error polynomial multiplied by different public (b_i)'s.

After shifted summation the exact common-error term is

[
e_Esum_iY^ib_i
=
e_EB.
]

The fused reconstruction represents exactly this same ciphertext/error term directly.

Thus

[

u_E|B|_{m emb}
]

is the natural correlated/common-source bound, while

[

u_Esum_i|b_i|_{m emb}
]

from separately bounding five copies and then adding them is merely a looser triangle-bound ledger.

Turn 18 already proved the underlying `CtxtPart` equality, so the fused path is not changing the actual ciphertext polynomial to obtain this tighter estimate.

## 6. intFactor, ptxtSpace, and primeSet are exactly preserved

For both schedules:

- each reconstruction starts by assigning the same `recryptEkey`;
- `recryptEkey.intFactor=1`;
- polynomial `multByConstant` does not modify `intFactor`;
- `addConstant` does not modify `intFactor`;
- public (Y^i) polynomial multiplication does not modify `intFactor`;
- adding equal-factor BGV ciphertexts does not enter HElib's factor-harmonization branch.

Therefore

[
oxed{
	exttt{intFactor}_{m fused}
=
	exttt{intFactor}_{m sep}
=
1
}
]

at the reconstruction boundary.

Likewise:

[
oxed{
	exttt{ptxtSpace}_{m fused}
=
	exttt{ptxtSpace}_{m sep}
=
P_{m boot}
}
]

and

[
oxed{
	exttt{primeSet}_{m fused}
=
	exttt{primeSet}_{m sep}
=
S_E.
}
]

No reconstruction-fusion-specific modulus mismatch exists.

The later RM10 unit normalization (224) changing `intFactor: 1 -> 399 mod 625` is a downstream operation already audited in Turn 16 and is not part of this reconstruction comparison.

## 7. Local capacity/correctness consequence

Because the comparator and fused states have the same BGV `primeSet`, and

[

u_{m fused}le
u_{m sep},
]

the pinned HElib capacity formula gives

[
oxed{
C_{m fused}
ge
C_{m sep}
}
]

for this exact reconstruction boundary.

Likewise, if the hypothetical five-reconstruction shifted-sum comparator satisfies HElib's `isCorrect()` inequality at this boundary, the fused state also satisfies it.

Therefore fusion introduces **no hidden reconstruction-specific capacity penalty** in HElib bookkeeping.

This result is local. It does **not** prove:

- (C_{m fused}) is at least the capacity of every individual stock branch;
- the final revised pipeline has capacity at least the published stock pipeline;
- RM10/joint-recovery key-switch noise is free;
- correction DigitExtract has the same final capacity.

Those remain downstream/native questions.

## 8. New representation-level implementation hazard

The source audit found one concrete implementation trap not explicit in Turns 16-18.

For (m=32768),

[
phi(m)=m/2=16384.
]

HElib's power-of-two `embeddingLargestCoeff` fast path (`half/quarter_embeddingLargestCoeff`) explicitly requires the input polynomial vector length to be at most

[
m/2=16384.
]

Otherwise it throws

`vector too big f canonicalEmbedding`.

Both

- `multByConstant(const ZZX&)`;
- `addConstant(const ZZX&)`

compute `embeddingLargestCoeff(poly)` **before** converting the polynomial to `DoubleCRT`.

A naive polynomial construction of

[
Y^ib_i=X^{1024i}b_i
]

can have formal degree above (16383), even though the ring element is perfectly valid modulo

[
Phi_{32768}(X)=X^{16384}+1.
]

Therefore the aggregate (A,B) must not be passed to these APIs as unreduced high-degree `ZZX` polynomials.

Required implementation rule:

[
oxed{
A,B	ext{ must first be reduced in }
mathbb Z[X]/(X^{16384}+1)
}
]

using the exact signed negacyclic shift/wrap

[
X^{16384}=-1.
]

After reduction:

[
deg A,deg B<16384,
]

and the default HElib norm bookkeeping is well-typed.

This is not merely an optimization. Without it, an otherwise-correct candidate can fail at the bookkeeping API before cryptographic execution.

## 9. Required eventual native assertions

Any later candidate implementation should record/assert at the reconstruction boundary:

```text
A_DEGREE < 16384
B_DEGREE < 16384
A_B_NEGACYCLIC_REDUCTION = EXACT

RECRYPTEKEY_INTFACTOR = 1
FUSED_INTFACTOR = 1
FUSED_PTXTSPACE = RECRYPTEKEY_PTXTSPACE
FUSED_PRIMESET = RECRYPTEKEY_PRIMESET

NOISE_FUSED =
  noise_recryptEkey * emb_norm(B)
  + abs(f) * emb_norm(A)

NOISE_SEPARATE_LEDGER =
  sum_i [
    noise_recryptEkey * emb_norm(b_i)
    + abs(f) * emb_norm(a_i)
  ]

ASSERT:
  NOISE_FUSED <= NOISE_SEPARATE_LEDGER + numerical_tolerance
```

Do not override the `size` argument with an optimistic hand-computed value smaller than HElib's canonical-embedding norm. Use the default norm path after exact ring reduction, or record a separately verified conservative bound.

## Verdict

```text
RESULT:
  PASS_STATIC_RECONSTRUCTION_BOOKKEEPING_DOMINANCE

FUSED_INTFACTOR:
  1 / EXACTLY SAME AS FIVE-STOCK SHIFTED-SUM COMPARATOR

FUSED_PTXTSPACE:
  SAME AS recryptEkey

FUSED_PRIMESET:
  SAME AS recryptEkey

FUSED_NOISEBOUND:
  <= FIVE-STOCK-RECONSTRUCTION SHIFTED-SUM LEDGER

FUSED_LOCAL_CAPACITY:
  >= FIVE-STOCK-RECONSTRUCTION SHIFTED-SUM COMPARATOR

FUSED_LOCAL_ISCORRECT_GATE:
  NO WORSE THAN COMPARATOR

COMMON_RECRYPTEKEY_NOISE_CORRELATION:
  EXPLICITLY CAPTURED BY emb_norm(B)

HIDDEN_RECONSTRUCTION_CAPACITY_PENALTY:
  NONE FOUND

NEW_IMPLEMENTATION_HAZARD:
  UNREDUCED HIGH-DEGREE A/B CAN BREAK embeddingLargestCoeff

REQUIRED_RING_REPRESENTATIVE:
  DEGREE < 16384 VIA X^16384 = -1 NEGACYCLIC REDUCTION

WHOLE_PIPELINE_CAPACITY:
  STILL UNRESOLVED

RM10_AND_JOINT_RECOVERY_KS_NOISE:
  STILL UNRESOLVED

DIGITEXTRACT_FINAL_CAPACITY:
  STILL UNRESOLVED

NATIVE_END_TO_END_CORRECTNESS:
  NOT ESTABLISHED

PENDING_NATIVE_TASK:
  UNCHANGED / STILL RUNNING-PENDING

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
```

## Scientific disposition

Turn 18's remaining bookkeeping caveat does not kill the candidate.

At the exact post-reconstruction state, the single fused reconstruction has a source-proven HElib BGV noise ledger no worse than the algebraically equivalent five-reconstruction shifted-sum schedule, while preserving the same `intFactor`, `ptxtSpace`, and `primeSet`.

The important new implementation invariant is representation-level: aggregate public polynomials must be exact degree-(<16384) negacyclic representatives before invoking HElib's default `ZZX` constant APIs.

No conclusion is transferred to the downstream RM10/joint-recovery/DigitExtract capacity without native or additional source evidence.
