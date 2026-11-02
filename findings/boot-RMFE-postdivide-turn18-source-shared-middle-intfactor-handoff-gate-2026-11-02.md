# BOOT Research Turn 18/25 — source-faithful post-divide aggregation hook / intFactor handoff gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

The current candidate requires five tagged branches to cross HElib's nonlinear recryption
preprocessing independently through:

  canonicalization / level preparation
  -> reLinearize(recryptKeyID)
  -> rawModSwitch(q)
  -> newMakeDivisible(p^ePrime)
  -> exact integer division by p^ePrime

and only THEN aggregate their two integer representatives before one shared:

  recryptEkey * Z1 + Z0

reconstruction.

Hypothesis:
this exact boundary can be implemented source-faithfully with ONE narrow candidate-facing PubKey
entry point, while preserving HElib encapsulation and without exposing recryptEkey,
recryptKeyID, newMakeDivisible, or arbitrary Ctxt::intFactor mutation.

Falsifier:
- stock reCrypt/thinReCrypt preprocessing blocks differ in a way that prevents one source-shared
  helper;
- post-divide ZZX aggregation cannot be represented exactly without an extra modulus/reduction;
- the candidate cannot save/restore the application intFactor under the public API;
- implementing the hook requires evaluator secret-key access;
- or a helper necessarily moves aggregation before the source nonlinear boundary.

## Closest existing mechanism and exact delta

The parent implementation is pinned PubKey::thinReCrypt / PubKey::reCrypt.

The current candidate does NOT alter:
- rawModSwitch;
- newMakeDivisible;
- recryption-key generation;
- recryptEkey;
- bootstrapping key ID;
- the source noise-ratio checks.

Its exact delta is only:

  stock:
    preprocess branch i
    -> reconstruct branch i
    repeated 5 times

  candidate:
    preprocess branch i
    repeated 5 times
    -> exact integer sum of the five post-divide pairs
    -> reconstruct once.

The legal aggregation cut is therefore an implementation boundary, not a replacement arithmetic
primitive.

## 1. Pinned reCrypt and thinReCrypt contain the same middle block

A direct pinned-source comparison shows that, after the relevant forward transform, both routines
execute the same body:

  if (!ctxt.inCanonicalForm())
      ctxt.reLinearize();

  s = ctxt.primeSet / specialPrimes;
  retain at most first three ctxt primes;
  ctxt.modDownToSet(s);

  ctxt.reLinearize(recryptKeyID);

  ctxt.rawModSwitch(zzParts, q);

  check source raw-mod-switch noise ratio;
  require exactly two parts;

  for each part:
      newMakeDivisible(part, p2ePrime, q, context, v);

  optional HELIB_DEBUG recryption-bound checks;

  for each part:
      part /= p2ePrime;

  ctxt = recryptEkey;
  ctxt.multByConstant(zzParts[1]);
  ctxt.addConstant(zzParts[0]).

The two copies differ only in surrounding timer/check labels and in the transform performed before
this shared middle.

Therefore a single source-shared middle implementation is structurally available.

## 2. newMakeDivisible is deliberately file-local and should remain so

Pinned recryption.cpp declares:

  static void newMakeDivisible(...).

It:
- converts the raw ZZX representative to the powerful basis;
- for every integer powerful coefficient z chooses a bounded v such that
    z + q*v == 0 mod p2ePrime;
- writes the adjusted exact integer value back;
- converts to ZZX.

For current:

  p=5,
  ePrime=1,
  p2ePrime=5,
  q=626 == 1 mod5.

The p=2 random tie-breaking branch is inactive.

Hence the current p=5 mapping is deterministic for a fixed rawModSwitch output.

There is no scientific reason to expose this function outside recryption.cpp.

## 3. recryptKeyID and recryptEkey should also remain private

Pinned PubKey stores both:

  long recryptKeyID;
  Ctxt recryptEkey;

in its private section.

This is useful encapsulation:
- candidate evaluation should use existing public bootstrapping material;
- it should not receive a mutable/raw handle to the encrypted recryption key;
- it should not independently reconstruct HElib's private bootstrapping state.

The implementation should therefore remain a PubKey member path.

No getter for recryptEkey/recryptKeyID is required.

## 4. Source refactor: two file-local helpers, one candidate-facing entry point

The source-clean refactor is:

### A. file-local source-shared post-forward preprocessor

Conceptually:

  static void preprocessRecryptParts(
      Ctxt& ctxt,
      long recryptKeyID,
      std::vector<ZZX>& postDivideParts)

It contains EXACTLY the pinned block from:
- canonical-form check
through
- rawModSwitch,
- source noise checks,
- newMakeDivisible,
- division by p^ePrime,

and RETURNS before:

  ctxt = recryptEkey.

Stock reCrypt and thinReCrypt call this helper instead of their duplicated code.

No arithmetic is changed.

### B. file-local reconstruction helper

Conceptually:

  static void reconstructRecryptParts(
      Ctxt& out,
      const Ctxt& recryptEkey,
      const std::vector<ZZX>& parts)

with exactly:

  assert parts.size()==2;
  out = recryptEkey;
  out.multByConstant(parts[1]);
  out.addConstant(parts[0]).

Stock reCrypt/thinReCrypt immediately call this after helper A, reproducing the old behavior.

### C. one narrow PubKey candidate entry point

Conceptually:

  long PubKey::lateAggregateThinMiddle(
      Ctxt& out,
      std::vector<Ctxt>& taggedBranches) const;

The method:
1. requires a nonempty fixed-k branch vector (current k=5);
2. checks common context/public key/application plaintext space;
3. reads the common branch intFactor using PubKey's friend access to Ctxt;
4. requires every branch to have the same intFactor/key state;
5. performs the stock thin pre-forward preparation and forward ThinEvalMap PER BRANCH;
6. invokes helper A independently on every branch;
7. sums only the resulting two post-divide ZZX representatives;
8. invokes helper B ONCE on the two sums;
9. returns the saved application intFactor as read-only metadata.

This is the only new candidate-facing core entry point required for the middle.

## 5. The entry point must include the stock pre-forward level preparation

Pinned thinReCrypt does, before slotToCoeff:

  ctxt.dropSmallAndSpecialPrimes();

and, under the pinned always-defined DROP_BEFORE_THIN_RECRYPT path:

  first = first ctxt prime;
  last  = min(last ctxt prime, first+2);
  ctxt.bringToSet(IndexSet(first,last));

then:

  trcData.slotToCoeff->apply(ctxt).

Therefore the canonical current candidate should NOT be described as merely:

  tagged branch -> slotToCoeff -> post-forward preprocessing.

The source-faithful branch path is refined to:

  tagged branch
  -> dropSmallAndSpecialPrimes
  -> bringToSet(first <=3 ctxt primes)
  -> trcData.slotToCoeff->apply
  -> helper-A post-forward preprocessing.

All five branches execute this independently before the legal aggregation cut.

This refinement is important for matched source/noise behavior even though it introduces no new
plaintext algebra.

## 6. Exact post-divide aggregation is representable with no hidden reduction

After helper A each branch yields:

  z_i = (z0_i,z1_i)

as NTL::ZZX polynomials whose coefficients are arbitrary-precision NTL::ZZ integers.

The candidate performs:

  Z0 = sum_i z0_i
  Z1 = sum_i z1_i

using ordinary exact ZZX addition.

There is:
- no reduction mod q;
- no reduction mod625;
- no machine-word overflow assumption;
- no extra rounding.

This is exactly the integer-level aggregation point proved legal in the earlier late-aggregation
theorem.

Only after this exact sum does helper B embed the pair back through the existing recryptEkey.

## 7. Source debug/noise checks remain branch-local

The helper-A refactor must preserve, for EACH branch:
- rawModSwitch scaled-noise estimate;
- HELIB_MIN_CAP_FRAC bound;
- warning/throw behavior;
- exactly-two-parts assertion;
- HELIB_DEBUG checkRecryptBounds;
- HELIB_DEBUG checkRecryptBounds_v;
- HELIB_DEBUG checkCriticalValue.

These checks occur BEFORE aggregation.

Therefore the candidate cannot use aggregation to hide an invalid individual branch from the stock
recryption correctness preconditions.

This is the correct source-faithful interpretation of "five branch-local nonlinear preprocesses".

## 8. The old Turn-22 one-helper description is refined, not reused literally

Historical Turn 22 proposed a conceptual helper that included:

  preprocess -> ctxt=recryptEkey -> reconstruction

and said the shared middle should call it once.

That is incompatible with the CURRENT post-divide late-aggregation placement if interpreted
literally: calling such a full helper once would move aggregation before the nonlinear preprocessing,
while calling it five times would reconstruct five times and lose the target saving.

The correct current structure is:

  five calls to source-shared helper A
  -> one exact ZZX pair sum
  -> one call to source-shared helper B.

A SINGLE candidate-facing PubKey method can encapsulate this three-stage structure, so the public/core
patch surface remains narrow even though the internal semantic cut is now explicit.

## 9. intFactor access-control issue and exact low-risk resolution

Pinned Ctxt::intFactor is private and has no public getter/setter.

Stock thinReCrypt can save:

  long intFactor = ctxt.intFactor

and restore it later only because PubKey is declared a friend of Ctxt.

Therefore a purely external current-candidate implementation cannot literally implement the old
instruction "save f_in, restore f_in" without changing the API.

The new PubKey aggregate-middle entry point solves the READ side:
- it reads the common input factor internally;
- returns only the numeric saved factor f_in.

No arbitrary intFactor setter is added.

For current application r=1:

  initial ptxtSpace=5,

and HElib BGV invariants imply f_in is a unit modulo5.

## 10. Final restoration can use an existing public scalar-unit operation

Pinned stock restoration after DigitExtract is metadata-only:

  ctxt.intFactor =
      ctxt.intFactor * f_in mod ptxtSpace.

At the candidate's final boundary:

  ptxtSpace=5.

Let:

  c = f_in^{-1} mod5.

Pinned BGV:

  ctxt.multByConstant(c)

for unit c has gcd(c,5)=1, so:
- ciphertext parts are NOT multiplied;
- noiseBound is unchanged;
- intFactor is multiplied by c^{-1}=f_in.

Therefore:

  final.multByConstant(InvMod(f_in,5))

produces EXACTLY the same intFactor update as stock's private-field restoration, without adding a
setter and without direct noise growth.

This uses the same unit-scalar mechanism established in Turn 16 for normalization by 28.

Required runtime assertion:

  final.getPtxtSpace()==5
  gcd(f_in,5)==1

before this restoration.

## 11. Security/encapsulation boundary

The proposed patch:
- exposes no secret key;
- exposes no recryptKeyID;
- exposes no recryptEkey;
- exposes no raw newMakeDivisible function;
- introduces no new evaluation key;
- returns only the existing BGV intFactor metadata already implicit in ciphertext representation.

The two ZZX post-divide pairs remain ephemeral inside the PubKey member and need not be surfaced to
the application.

This is not a full security proof, but it avoids creating a new evaluator-visible intermediate API
surface beyond the candidate operation itself.

## 12. Revised canonical production middle

The current canonical path is now source-shaped as:

  five Aung SlotsToCtxts scalar branches
  -> global monomial tag per branch
  -> for EACH branch:
       dropSmallAndSpecialPrimes
       bringToSet(first <=3 ctxt primes)
       ThinEvalMap slotToCoeff
       canonicalize/modDown
       reLinearize(recryptKeyID)
       rawModSwitch(q=626)
       branch-local source bounds
       newMakeDivisible(5)
       divide exact integer ZZX parts by5
  -> exact integer ZZX sums Z0,Z1
  -> ONE recryptEkey reconstruction
  -> Turn-16 pure normal_basis=false EvalMap inverse
  -> scalar-unit 28 normalization (factor 67)
  -> 17-call recovery
  -> exact L0..L3
  -> Algorithm 4 / final Recode
  -> scalar-unit restore using InvMod(f_in,5).

This supersedes older shorthand that omitted the stock pre-forward level preparation or described
the full preprocessing/reconstruction as one call.

## Verdict

PASS_SOURCE_SHARED_POSTDIVIDE_HOOK_DESIGN
PASS_FIVE_PREPROCESS_ONE_RECONSTRUCTION_SOURCE_CUT
PASS_EXACT_ZZX_AGGREGATION_IMPLEMENTABILITY
PASS_INTFACTOR_HANDOFF_WITHOUT_SETTER
PASS_PUBLIC_UNIT_SCALAR_FINAL_RESTORE
REFINE_THIN_BRANCH_PATH_WITH_STOCK_PREFORWARD_LEVEL_PREP

NATIVE_EXECUTION=NOT_OBTAINED

This closes a previously unresolved implementation/encapsulation blocker at source-design level.

It does NOT establish:
- compiled patch correctness;
- actual branch-local source assertions;
- recovery-canary correctness;
- full candidate correctness;
- capacity/performance.

CORRECTNESS_GATE remains BLOCKED.

BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

The smallest native test remains the revised recovery-only canary because evidence order still lacks
the small correctness canary.

After that PASS, the exact parameter/interface implementation gate should add this Turn-18 source
refactor and first test the shared middle itself:

1. run the refactored stock thinReCrypt on a control and confirm byte/semantic equivalence at its
   old reconstruction boundary;
2. run five tagged branches through helper A;
3. assert all five branch-local source bounds pass;
4. independently reconstruct each pair as a test oracle;
5. sum post-divide pairs and reconstruct once;
6. verify exact ciphertext semantic equality:
     shared reconstruction == sum of five separate reconstructions;
7. carry the shared ciphertext through Turn-16/17 EvalMap+scalar28+recovery.

No timing or capacity interpretation before these correctness assertions pass.
