# BOOT RMFE Recrypt-Key Handle / Exact Linear-Form Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 18/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task `BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01` remains RUNNING/PENDING and was not modified, restarted, resubmitted, or treated as complete.

This turn closes the Turn-16-selected correctness falsifier: whether branch-specific `reLinearize(recryptKeyID)` handles, the (Y^i) envelope shifts, post-raw aggregation/carry correction, and one `recryptEkey` reconstruction preserve HElib's exact two-part secret-key linear form.

Pinned source: `homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`, chiefly `include/helib/Ctxt.h`, `src/Ctxt.cpp`, `src/recryption.cpp`, `src/keys.cpp`, and `src/debugging.cpp`.

No native execution, source mutation, key generation, parameter change, or benchmark occurred.

## 1. The two keys in stock thin recryption

Write (s_0) for the ordinary secret key (key ID 0) and (s_R) for the bootstrapping/recryption secret whose key ID is (R=	exttt{recryptKeyID}).

`SecKey::genRecryptData()` samples a new `keyPoly`, imports it as key (s_R), generates the key-switch matrix from key 0 to key (R), and encrypts the same `keyPoly` into the public member `recryptEkey` under key 0.

Thus stock thin recryption deliberately implements

[
s_0	ext{-ciphertext}
	o
	ext{two-part linear form under }s_R
	o
s_Rmapstooperatorname{Enc}_{s_0}(s_R).
]

## 2. reLinearize(recryptKeyID) removes branch-specific handles

HElib's `SKHandle` denotes (s^r(X^t)) via `powerOfS`, `powerOfX`, and `secretKeyID`.

`inCanonicalForm(R)` requires at most two parts:
- part 0 is `isOne()`;
- part 1 is `isBase(R)`, i.e. handle ((1,1,R)).

For every branch, `Ctxt::reLinearize(R)` either returns because that exact condition already holds, or switches every nonmatching part through a matrix with `toKeyID=R`.

The decisive source is `Ctxt::keySwitchDigits`: the switched secret contribution is inserted with `SKHandle(1,1,W.toKeyID)`, while the constant contribution is inserted with `SKHandle()`.

Therefore after

[
	exttt{ctxt.reLinearize(recryptKeyID)}
]

every valid branch has the same handle basis

[
oxed{(1, s_R(X))}
]

and any earlier branch-dependent (s(X^t)) handle has been consumed by key switching. The target nonconstant part has `powerOfX=1`.

So branch (i) immediately before `rawModSwitch` is exactly

[
C_i=c_{i,0}+c_{i,1}s_R.
]

## 3. rawModSwitch preserves the two channels

`Ctxt::rawModSwitch` iterates over `parts[i]` independently and emits one public `ZZX` per input part; it does not inspect or transform `SKHandle`.

Stock `thinReCrypt` asserts `zzParts.size()==2`.

Pinned `rawDecrypt` in `src/debugging.cpp` explicitly reconstructs

[
oxed{z_0+s_Rz_1}
]

by computing `sKey * zzParts[1] + zzParts[0]`.

Hence after raw switching:
- channel 0 is the coefficient of (1);
- channel 1 is the coefficient of the common (s_R).

There is no third hidden branch-specific secret-handle state.

## 4. (Y^i) must be public ring multiplication, not automorphism

The current envelope uses (Y=X^{1024}) and (M_i(z)=Y^iz). This is multiplication by a public ring monomial.

HElib `multByConstant` multiplies every `CtxtPart` polynomial and leaves all `SKHandle` values unchanged. Thus

[
Y^i(c_{i,0}+c_{i,1}s_R)
=
Y^ic_{i,0}+(Y^ic_{i,1})s_R.
]

This must not be confused with `Ctxt::automorph(k)`. The pinned source explicitly updates every nonconstant handle by

[
	exttt{powerOfX}leftarrow 	exttt{powerOfX}cdot k pmod m,
]

and `smartAutomorph` must relinearize afterward.

Therefore:

[
oxed{	ext{(Y^i) placement is a public polynomial multiplication, never a Galois automorphism.}}
]

Using `automorph`/`smartAutomorph` for the envelope shift would invalidate this proof.

## 5. Post-raw aggregation and carry correction are typed componentwise

Turns 11-12 established exact public carry corrections across the branchwise raw/divisibility boundary. This handle audit adds a required typing rule:

> aggregation, compact-carry accumulation, divisibility correction, and every (Y^i) shift must be performed independently for channel (j=0) and channel (j=1).

Let (D) denote the already-established exact post-raw divisibility-lift/divide semantics including carry compensation. Define

[
a_i=D(z_{i,0}),qquad b_i=D(z_{i,1}),
]

and

[
A=sum_{i=0}^{4}Y^ia_i,qquad
B=sum_{i=0}^{4}Y^ib_i.
]

Equivalently, any compact-carry implementation needs two typed carry streams, one for the one-channel and one for the (s_R)-channel. They must not be cross-mixed.

Then exactly

[
oxed{
A+Bs_R
=
sum_iY^i(a_i+b_is_R).
}
]

Public carry polynomials only change (A) or (B); they do not create an additional secret-key basis element.

## 6. One recryptEkey reconstruction is exact at CtxtPart level

`recryptEkey` is an encryption of (s_R) under (s_0). Write its two actual ciphertext parts as

[
E=(E_0,E_1),
]

with handles one and base(0).

For a public pair ((a,b)), stock HElib reconstructs via

[
	exttt{ctxt = recryptEkey;}
quad
	exttt{ctxt.multByConstant}(b);
quad
	exttt{ctxt.addConstant}(a).
]

Let (f) be the common BGV constant-injection scale for this fixed recrypt-key state (its metadata semantics were audited in Turn 16). The actual part tuple is

[
operatorname{Rec}(a,b)
=
(bE_0+fa, bE_1)
]

with handles ((1,s_0)).

Because public multiplication is ring-linear and handle-preserving, and `addConstant` targets the one-handle part,

[
egin{aligned}
sum_iY^ioperatorname{Rec}(a_i,b_i)
&=
left(
sum_iY^ib_iE_0+fsum_iY^ia_i,;
sum_iY^ib_iE_1
ight)\
&=
(BE_0+fA, BE_1)\
&=
operatorname{Rec}(A,B).
end{aligned}
]

Thus the old algebraic identity is strengthened to an exact HElib `CtxtPart`/handle identity, not merely a plaintext-ring identity.

The single reconstruction returns to the canonical main-key basis ((1,s_0)), exactly like five separate stock reconstructions followed by the same public (Y^i) shifts and sum.

This claim is about the exact secret linear form / ciphertext parts. It does not claim identical HElib noise-bound bookkeeping between the two execution schedules.

## 7. Explicit falsifiers / eventual native assertions

The proof fails if any of these occurs:

1. immediately after `reLinearize(recryptKeyID)`, a branch is not `inCanonicalForm(recryptKeyID)`;
2. the stock raw path does not have exactly two parts;
3. a (Y^i) placement uses `automorph`/`smartAutomorph` rather than public polynomial multiplication;
4. the two raw/carry component channels receive different unintended shifts or are cross-mixed;
5. branches use different `recryptKeyID` or different boot-key ciphertexts.

The pinned stock design rules out item 5 because `recryptKeyID` and `recryptEkey` are single members of the same `PubKey`. Items 1-4 should be explicit assertions in any eventual native candidate implementation.

A one-part dummy ciphertext is not a valid substitute: stock `thinReCrypt` itself asserts exactly two raw-switched parts before reconstruction.

## Verdict

```text
RESULT:
  PASS_STATIC_RECRYPTKEY_HANDLE_LINEAR_FORM

POST_RELINEARIZE_HANDLE_BASIS:
  EXACTLY (ONE, BASE(recryptKeyID))

BRANCH_SPECIFIC_POWEROFX_AFTER_RELINEARIZE:
  ELIMINATED / TARGET powerOfX=1

RAWMODSWITCH_PAIR_MEANING:
  z0 + s_R*z1 / SOURCE-CONFIRMED

Y_SHIFT_TYPE:
  PUBLIC RING MONOMIAL MULTIPLICATION

Y_SHIFT_CHANGES_SKHANDLE:
  NO

GALOIS_AUTOMORPH_AS_Y_SHIFT:
  FORBIDDEN / WOULD CHANGE powerOfX

POST_RAW_AGGREGATION:
  MUST BE COMPONENTWISE FOR j=0,1

CARRY_STATE:
  TWO TYPED CHANNELS / NO CROSS-MIXING

SINGLE_RECRYPTEKEY_RECONSTRUCTION:
  EXACT CtxtPart-LEVEL EQUALITY TO SHIFTED SUM OF FIVE STOCK RECONSTRUCTIONS

OUTPUT_HANDLE_BASIS:
  EXACTLY (ONE, BASE(0))

SECRET_LINEAR_FORM_CORRECTNESS_BLOCKER:
  NONE FOUND

PENDING_NATIVE_TASK:
  UNCHANGED / STILL RUNNING-PENDING

NATIVE_END_TO_END_CORRECTNESS:
  NOT ESTABLISHED

LATENCY_SPEEDUP:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

DFR:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
```

## Scientific disposition

The carry-compensated post-raw fusion survives the secret-handle/type audit.

The implementation invariant is now:

[
oxed{
	ext{canonicalize each branch to }(1,s_R)
	o
	ext{process/shift the two public channels separately but identically}
	o
(A,B)
	o
operatorname{Rec}_{	exttt{recryptEkey}}(A,B)
	ext{ under }(1,s_0).
}
]

There is no hidden branch-specific (s_R(X^t)) term after `reLinearize(recryptKeyID)`.

The pending baseline timer remains untouched and retains its existing protocol/status.
