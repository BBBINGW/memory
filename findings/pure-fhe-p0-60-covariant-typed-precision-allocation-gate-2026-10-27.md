# PURE-FHE P0-PRESCOUT-60 — Covariant / Typed Precision Allocation in CKKS

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-60
LATEST_COMPLETED: P0-PRESCOUT-60
NEXT_ITERATION: P0-PRESCOUT-61 NOT_STARTED
STATUS: PASS_TYPED_ALGEBRA / PASS_STRICT_FIXED_UNIT_SEPARATION / PRIOR_ART_PARTIAL / HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## 1. Source-defined gap

Primary source:

Zhaoyang Liang, Runkun Liu, Jingwei Fang, Dan Ding,
"A New Approach to Reducing Modulus Requirements in Homomorphic Computation: Precision Allocation in CKKS,"
ePrint 2026/2562, revision current on 2026-10-27.

The paper represents a CKKS ciphertext ct=(c0,c1) with a public ring multiplier p through

  p(c0+c1 s) = M mod Q,
  sigma(M)=Delta(x+e).

Its Section 7.1 explicitly states:

  "We keep the multiplier p fixed throughout homomorphic evaluation."

With fixed p:
- ciphertext multiplication multiplies every tensor component by p before relinearization;
- an automorphism tau uses public correction q_tau=tau(p)p^{-1} when p is a unit;
- new relinearization, key-switching and rescaling errors acquire the restoration factor p;
- Lemma 7.2 makes the operation-local error proportional to |sigma_j(p)|.

The source also says its propagated error depends on the chosen unit and scales, so its ideal fixed-common-bound allocation cannot simply be optimized independently node by node.

This leaves a concrete question:

Can the multiplier be treated as a PUBLIC CIPHERTEXT TYPE p_v that changes across circuit nodes, while preserving the logical restored polynomial exactly?

## 2. Concurrent prior art boundary

### GCKKS conversion, ePrint 2026/2600

Ma–Liu–Wang–Wang give a generic GCKKS ciphertext-conversion framework between different decryption factors F,F' and useful-slot counts.

This DIRECTLY prior-arts the broad idea "change a decryption factor during homomorphic computation."

However, their k-preserving conversion is primarily a reinterpretation of the same stored RLWE pair under F':
  uF -> uF'.

Useful-slot scale changes by c'_m/c_m, and Section 4 separately controls unused slots and the new rescaling divisor.

Our candidate below is narrower:
- p_a and p_v are units;
- stored components are PUBLICLY multiplied by p_a p_v^{-1};
- the restored polynomial M is EXACTLY unchanged;
- logical value, logical error, and CKKS scale are unchanged.

Therefore factor conversion itself is not a novelty claim. The candidate is a typed, message-preserving scheduling framework.

### Focused CKKS, ePrint 2026/2531

Public abstract:
- cyclotomic units;
- different precision requirements across slots;
- focused rescaling/key switching;
- bootstrapping with precision-dependent splitting.

The full PDF was SOURCE_BLOCKED in the current acquisition routes, so it is unknown whether its full construction already transports or dynamically changes focus units across arbitrary leveled circuits.

Therefore NOVELTY remains NOT_ESTABLISHED.

### Shaped rounding, ePrint 2026/2513

The author describes the unit case as a public change of coordinates and uses fixed shaping profiles / restricted rotations preserving the profile. This is strong algebraic prior art for the coordinate-change viewpoint, but does not by currently accessible evidence establish circuit-wide typed unit scheduling.

## 3. Typed invariant

Assign every ciphertext node v a public unit p_v in R^x.

Maintain

  p_v (c_{v,0}+c_{v,1}s) = M_v mod Q_v,

with

  sigma(M_v)=Delta_v(x_v+e_v).

The unit label p_v is public metadata, analogous to level/scale metadata.

## 4. Exact message-preserving rebase

For an edge a -> v, define

  r_{a->v}=p_a p_v^{-1} in R.

Publicly multiply both ciphertext components by r:

  RB_{a->v}(ct_a)
    = (r c_{a,0}, r c_{a,1}) mod Q.

Then

  p_v r(c_{a,0}+c_{a,1}s)
    = p_a(c_{a,0}+c_{a,1}s)
    = M_a mod Q.

Therefore:

- restored polynomial M is exactly unchanged;
- logical value x is unchanged;
- existing logical error e is unchanged;
- scale Delta is unchanged;
- no rescaling or evaluation key is needed.

This is stronger than GCKKS reinterpretation, which intentionally changes the decryption-factor-scaled plaintext.

## 5. Typed operations

### Addition

For inputs with labels p_a,p_b and desired output label p_v:

  ct_v = RB_{a->v}(ct_a)+RB_{b->v}(ct_b).

Then

  M_v=M_a+M_b.

### Ciphertext multiplication

Raw phases satisfy

  z_a=M_a/p_a,
  z_b=M_b/p_b.

Tensor them and multiply every tensor component by

  r_mult = p_a p_b p_v^{-1}.

Before relinearization,

  p_v r_mult z_a z_b
    = M_a M_b.

If relinearization adds raw phase error kappa_v, restoration gives

  M_v = M_a M_b + p_v kappa_v.

After ordinary rescaling by D, with rounding residue rho_v,

  M_v'
    = (M_aM_b + p_v kappa_v - p_v rho_v)/D.

Thus:
- propagated logical input error is independent of p_a,p_b after restoration;
- NEW relin/rescale error at v is shaped by p_v.

Fixed-p Section 7.1 is the special case p_a=p_b=p_v=p.

### Automorphism

Apply tau to an input with label p_a.

The natural restoration factor becomes tau(p_a).

For desired output label p_v, multiply by

  q_{tau,a->v}=tau(p_a)p_v^{-1}

before key switching.

If key switching adds raw phase error kappa_tau, the restored polynomial is

  M_v=tau(M_a)+p_v kappa_tau.

Again:
- prior logical error is only permuted;
- newly injected KS error is shaped by p_v.

Most importantly, choose the COVARIANT label

  p_v=tau(p_a).

Then

  q_{tau,a->v}=1.

So an automorphism needs NO public factor correction at all, while the precision profile moves with the data.

This differs from fixed-p ePrint 2026/2562, which forces p_v=p_a=p and therefore pays q_tau=tau(p)p^{-1}.

## 6. Error-separation principle

In restored logical-error coordinates:
- exact rebasing does not change past errors;
- automorphisms permute past errors;
- each relin/KS/rescale operation injects a new term scaled by the OUTPUT label p_v.

Therefore a node-wise schedule can spend the unit norm budget on the slots that are important AT THAT NODE.

A fixed unit must protect the union of all slot positions that become important at any time.

This distinction is absent when the active precision profile is static.

## 7. [TOY_DERIVATION] Exact two-class strict separation

Use the standard two-embedding real toy ring Z[sqrt(2)] from the shaped-rounding exposition.

Its fundamental positive unit is

  U=1+sqrt(2),

with absolute embedding magnitudes

  t=1+sqrt(2) ~=2.414213562,
  t^{-1}=sqrt(2)-1 ~=0.414213562.

The rank-one unit group has absolute profiles

  (t^k,t^{-k}), k in Z,

up to signs and swapping by the nontrivial Galois automorphism tau.

Consider two slot classes A,B and a two-stage circuit:

1. Stage-1 Mul+Rescale produces the useful value in class A.
2. Automorphism tau swaps A and B.
3. Stage-2 Mul+Rescale operates on the moved useful value in class B.
4. Only the moved data path is precision-critical; the complementary class is dummy/guard at each stage.

Assume, only for the cheapest separation test, that each of:
- stage-1 relin/rescale,
- rotation key switch,
- stage-2 relin/rescale

has the same pre-restoration primitive bound nu.

Ignore input approximation error so only operation-local injected noise is compared.

### Any fixed unit

Let the fixed profile be

  w_A=t^k,
  w_B=t^{-k}.

- Stage-1 noise in A: nu w_A.
- That restored error moves to B unchanged under tau.
- Rotation KS adds nu w_B in B.
- Stage-2 adds another nu w_B in B.

Final required-slot bound:

  E_fixed(k)
    = nu(t^k + 2 t^{-k}).

Over integer k:
- k=0 gives 3nu;
- k=1 gives nu(t+2/t) ~=3.2426nu;
- k=-1 gives nu(1/t+2t) ~=5.2426nu;
- |k|>=2 is larger.

Hence

  min_{k in Z} E_fixed(k)=3nu.

### Covariant typed schedule

Choose stage-1 label

  p_1=U^{-1},

so the active A weight is t^{-1}.

After tau, choose

  p_2=tau(p_1).

Its active B weight is also t^{-1}.

Moreover p_2=tau(p_1), so the rotation correction is exactly one.

All three injected terms on the useful path are bounded by nu/t:

  E_typed <=3nu/t
          ~=1.242640687 nu.

Thus

  E_fixed^*/E_typed
    >=t
    =1+sqrt(2)
    ~=2.414213562.

Equivalently, at this toy gate the same final tolerance permits about

  log2(1+sqrt(2))
    ~=1.271553 bits

less scale / more precision headroom, before global recovery constraints.

This is a strict separation against ALL fixed units in this rank-one toy unit group.

## 8. Why the toy is meaningful but not yet a systems result

The toy proves a mathematical point:

  time-varying liveness + automorphisms can make one fixed precision profile strictly suboptimal.

It does NOT yet prove end-to-end modulus savings.

Potential killers still include:

1. Global recovery / coefficient-wrap constraints.
   Large errors placed into the current dummy class still contribute to the restored polynomial norm. Theorem 6.1 / equation (21)-type recovery constraints may cap t strongly enough to erase scale savings.

2. General unit availability.
   The full ring has a discrete unit lattice. Node-wise desired profiles must be approximated by actual units, using the 2562 Fourier construction or Focused-CKKS-style unit search.

3. Branch joins.
   Addition of ciphertexts with different labels requires explicit rebasing to a common label. A schedule with many joins may pay extra public modular products.

4. Linear transforms.
   Many rotations followed by sums may lose the correction-free covariant property because rotated branches must be aligned before addition.

5. Public-factor cost.
   A standalone rebase costs two ciphertext-component public multiplications per active RNS prime. However:
   - fixed-p multiplication already has one public correction; typed multiplication only changes its value;
   - fixed-p automorphism already has q_tau; typed covariant automorphism can make q_tau=1;
   so along multiply/rotate-heavy paths the dynamic schedule need not increase kernel count and may reduce it.

6. Concurrent prior art.
   Full 2026/2531 remains unavailable, and 2026/2600 already has stage-wise decryption-factor conversion inside GCKKS bootstrapping.

## 9. Security sanity

Let the initial input label p_root be fixed public data before key generation/encryption.

All subsequent label changes are deterministic public homomorphic maps:
- multiply ciphertext components by public ring units;
- use standard relin/key-switch/rescale.

Thus typed rebasing introduces no new secret key material or assumption.

A full reduction can compose ePrint 2026/2562 Proposition 7.1 for the initial encoding with deterministic post-processing closure of IND-CPA.

Security is therefore PLAUSIBLE but not separately promoted to a theorem in this prescout.

## 10. Prior-art judgment

Known/concurrent work covers:
- fixed unit precision allocation (2562);
- focused units and general per-slot requirements (2531 abstract);
- public change-of-coordinate view (2513);
- generic changing decryption factors / slot counts, including stage-wise conversion in GCKKS bootstrap (2600).

Current accessible sources do NOT explicitly establish:
- a per-ciphertext unit type p_v for arbitrary leveled CKKS circuits;
- exact message-preserving rebase p_a p_v^{-1};
- covariant automorphism typing p_out=tau(p_in) eliminating q_tau;
- a global node-label optimization exploiting time-varying slot liveness.

Because 2531 full text is blocked, NOVELTY remains NOT_ESTABLISHED.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-60

STATUS:
PASS_TYPED_ALGEBRA /
PASS_COVARIANT_AUTOMORPHISM /
PASS_STRICT_FIXED_UNIT_SEPARATION /
PRIOR_ART_PARTIAL /
HUMAN_REVIEW.

PRIMARY_HYPOTHESIS:
Treat the precision-allocation unit as public ciphertext type metadata and optimize it per circuit node. Covariant transport under automorphisms lets the precision profile follow data movement and can strictly beat every fixed unit when the active slot set changes over time.

SMALLEST_TEST:
Exact typed algebra + rank-one two-class unit toy.

RESULT:
- Exact message-preserving rebasing is algebraically valid.
- New operation noise is shaped by the output unit; past logical error is unchanged by rebase.
- Setting p_out=tau(p_in) makes automorphism correction equal one.
- In the Z[sqrt(2)] two-class toy, dynamic typing reduces final operation-local error by exactly at least 1+sqrt(2) ~=2.414x versus the best fixed unit.

NOVELTY:
NOT_ESTABLISHED due concurrent 2531/2600 overlap.

COMPLETE MODULUS / RECOVERY BENEFIT:
NOT YET ESTABLISHED.

CODEX_REQUIRED:
NO.

NEXT_TEST P0-61:
Do exactly one source-faithful modulus/recovery gate before any implementation:
1. extend 2562's restored-error recurrence and recovery condition to node labels p_v;
2. instantiate a minimal rotation-changing-active-set circuit with actual source primitive bounds and actual cyclotomic units;
3. jointly optimize scale Delta, modulus Q, and p_v schedule;
4. compare against the best fixed p under the SAME output precision and recovery constraint;
5. include public-correction operation counts.

If the global recovery bound cancels the local 2.414x error advantage, KILL.
If a strict modulus/RNS-prime reduction survives, then perform a deeper 2531 prior-art audit before any native implementation.

STATE_UPDATE: YES — this finding only.
