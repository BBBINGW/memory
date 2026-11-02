# BOOT Research Turn 15/25 — dirty-Z625 lifts to Algorithm-4 divideByP / final-factor correctness gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., ePrint 2025/350 / PKC 2025

## Primary hypothesis

Given the current recovery contract, the five selected branch values are exact arbitrary lifts

  a_i in Z_625

rather than canonical representatives in F_5.

Turn 15 asks whether those dirty lifts are still a valid exact input to Aung Algorithm 4 all the
way through its six y-u / divideByP boundaries and final recode, under pinned HElib BGV
plaintext-space/intFactor semantics.

Falsifier:
- Aung's divisibility proof quantifies only over canonical mod-5 representatives;
- a correction boundary subtracts ciphertexts at incompatible plaintext spaces;
- HElib intFactor harmonization changes semantic plaintext and can destroy divisibility;
- divideByP does not implement the quotient assumed by the proof;
- or the current late-aggregation recovery enters Algorithm 4 with a stale representation factor
  incompatible with the exact L0..L3 semantics.

## 1. Aung's theorem already quantifies over arbitrary Z_{p^e} lifts

Aung Algorithm 4 defines, for z=phi(x_1,...,x_k),

  L_r(z) = sum_i x_i * phi(e_i)^(p^r).

The paper's divisibility proof explicitly assumes

  z = sum_t a_t phi(e_t)

with

  a_1,...,a_k in Z_{p^e}.

The base-case proof uses only that

  a_t - a_t^p

is divisible by p.

It does NOT assume:
- a_t lies in {0,...,p-1};
- a_t is Teichmuller/canonical;
- higher p-adic digits vanish.

The induction then proves the next numerator is divisible by p using Lemma 1 and Lemma 2, and
concludes that Algorithm 4 runs without division failure and carries digit extraction correctly to
the integers RMFE-packed into z.

Therefore, for current p=5,e=4:

  arbitrary a_i in Z_625

are exactly within the source theorem's quantified domain.

The current candidate's selected 5-adic dirty lifts are not an extension of the source theorem;
they are a direct instance of it.

## 2. Current eta meets the source correction requirement exactly

The current durable construction fixes:

  eta = 125.

Aung Algorithm 4 requires

  eta >= p^(e-1).

Here:

  p^(e-1) = 5^3 = 125.

Hence the candidate sits exactly at the theorem threshold:

  eta = p^(e-1).

No extra multiplicative-friendliness assumption is needed for dirty lifts beyond the already-fixed
RMFE construction.

## 3. The current aligned L0..L3 are exactly the source Algorithm-4 inputs

Turns 8-9 supersede the old raw-coordinate rho compensation and establish aligned global outputs.

For each physical slot independently, after current coordinate routing the branch scalars are

  a_0,...,a_4 in Z_625

and the four ciphertexts are exactly:

  L0 = sum_i a_i phi(e_i)
  L1 = sum_i a_i phi(e_i)^5
  L2 = sum_i a_i phi(e_i)^25
  L3 = sum_i a_i phi(e_i)^125.

These are exact Z_625 equalities, not merely mod-5 equalities.

Thus:

  L0 in im(phi)

and L1,L2,L3 are exactly the correction maps required by Algorithm 4.

The same statement holds slotwise for both physical slots because the Turn-8/9 global
rho-intertwining result already transports the slot conjugation inside the global recovery. No
post-unpack rho_pos/443 operation is introduced here.

## 4. Exact e=4 plaintext-space ladder in Algorithm 4

For p=5,e=4 the outer loop has j=0,1,2 and exactly six divide boundaries.

Let P(x) denote the HElib plaintext space of ciphertext x.

Initial correction-map ciphertexts:

  P(L0)=P(L1)=P(L2)=P(L3)=625.

Fe evaluation preserves the current plaintext space of its input.

The exact schedule is:

Boundary B1: j=0,i=0
  y=L1                   : 625
  u_0,1=Fe(u_0,0)       : 625
  subtract/divide       : 625 -> 125
  u_1,1                 : 125

Boundary B2: j=1,i=0
  y=L2                   : 625
  u_0,2=Fe(u_0,1)       : 625
  subtract/divide       : 625 -> 125

Boundary B3: j=1,i=1
  y after B2             : 125
  u_1,2=Fe(u_1,1)       : 125
  subtract/divide       : 125 -> 25
  u_2,2                 : 25

Boundary B4: j=2,i=0
  y=L3                   : 625
  u_0,3=Fe(u_0,2)       : 625
  subtract/divide       : 625 -> 125

Boundary B5: j=2,i=1
  y after B4             : 125
  u_1,3=Fe(u_1,2)       : 125
  subtract/divide       : 125 -> 25

Boundary B6: j=2,i=2
  y after B5             : 25
  u_2,3=Fe(u_2,2)       : 25
  subtract/divide       : 25 -> 5
  u_3,3                 : 5.

Therefore the six source divisibility boundaries are exactly:

  3 x 625,
  2 x 125,
  1 x 25,

and every HElib subtraction is between ciphertexts at the SAME plaintext space.

No accidental gcd-based plaintext-space reduction is needed before any divideByP.

## 5. HElib factor harmonization does not alter the semantic numerator

Pinned Ctxt::addCtxt harmonizes differing BGV intFactors before addition/subtraction.

If factors are f1 and f2, it chooses units e1,e2 such that

  e1*f1 = e2*f2 mod P

and then applies mulIntFactor(e1/e2) to the representations.

Pinned mulIntFactor(e):
- multiplies every ciphertext part by e;
- multiplies intFactor by the same e.

Under HElib's BGV invariant

  rawDec(c) = intFactor * Q * m mod P,

this leaves the semantic plaintext m unchanged.

Hence factor harmonization may change:
- representation;
- noiseBound;
- capacity;

but it does NOT change y or u as plaintext elements.

Therefore if Aung's theorem says

  y-u in pE,

the HElib-harmonized subtraction still encrypts that same semantic y-u and retains the same
p-divisibility property.

This closes correctness but NOT capacity: factor-harmonization noise remains runtime-state
dependent and is outside this gate.

## 6. divideByP implements the exact quotient required by Algorithm 4

Pinned Ctxt::divideByP requires:
- P=ptxtSpace divisible by p;
- P>p;
- the semantic plaintext is zero modulo p.

It multiplies all ciphertext parts by p^{-1} modulo the current ciphertext modulus Q, then sets:

  ptxtSpace <- P/p
  intFactor <- intFactor mod (P/p).

Let the semantic plaintext be

  m = p*m'

in plaintext space P=p*P'.

Under the BGV invariant, an integer coefficient of the raw decryption satisfies

  D = f*Q*p*m' + P*h
    = p*(f*Q*m' + P'*h).

Thus D is coefficientwise divisible by p.

Let u=p^{-1} mod Q. Since p*u=1+tQ,

  u*D mod Q

is the same Q-residue as

  f*Q*m' + P'*h.

Reducing the result modulo P' gives

  f*Q*m' mod P'.

Since divideByP also reduces the metadata factor to f mod P', subsequent HElib decryption returns
exactly m'.

Therefore pinned divideByP is precisely the ciphertext-level realization of the quotient step in
Aung Algorithm 4 whenever the source theorem's divisibility condition holds.

## 7. intFactor remains a unit throughout the Algorithm-4 DAG

The current Algorithm-4 input representation starts from a unit factor.

More generally, the pinned HElib operations preserve unit-ness:

- ciphertext multiplication:
    f_out = f1*f2*(Q mod P) mod P,
  and Q is coprime to p;
- add/sub harmonization multiplies factors only by units e1,e2;
- public constant multiplication does not change intFactor;
- divideByP reduces a p-adic unit modulo the smaller p-power, which remains a unit.

Hence every InvMod used by HElib factor harmonization remains well-typed throughout all six
boundaries.

There is no hidden correctness failure caused by a noninvertible intFactor.

## 8. Current late-aggregation candidate enters Algorithm 4 at common intFactor=1

This is an important current-candidate distinction.

Pinned SecKey::skEncrypt initializes intFactor=1, and recryptEkey is generated through that
encryption path at the temporary bootstrapping plaintext space.

The current shared reconstruction begins from:

  ctxt = recryptEkey

and then uses only:
- multByConstant;
- addConstant.

Neither changes intFactor.

The normalized pure inverse folds the factor 28 into PUBLIC linear constants. Public constant
multiplication does not modify intFactor.

The global recovery tree uses:
- Frobenius;
- source-faithful cleanUp;
- addition/subtraction of same-factor parent/Frobenius copies;
- public monomial multiplication.

For the active real mod-switch cleanup path established in Turn 13, none changes intFactor.

All five final leaves therefore have one common factor 1.

The aligned L0..L3 are public linear combinations of those leaves and likewise enter Algorithm 4
with:

  intFactor(L0)=intFactor(L1)=intFactor(L2)=intFactor(L3)=1.

Any historical analysis whose premise is that THIS current candidate necessarily enters
DigitExtract with intFactor=399 is therefore stale for the present late-aggregation construction.

This does NOT imply DigitExtract has zero factor-harmonization cost: Fe's ciphertext
multiplications create nontrivial factors dynamically. It only removes the obsolete INITIAL
factor-399 premise.

## 9. Final application intFactor restoration remains at the stock final point

The original application ciphertext factor f_in is saved before the bootstrapping middle.

Pinned HElib thinReCrypt deliberately resets representation through recryptEkey and restores the
saved factor only AFTER digit extraction:

  ctxt.intFactor =
      ctxt.intFactor * f_in mod ptxtSpace.

The current candidate must retain exactly this placement.

For e=4,r=1, Algorithm 4 ends with:

  u_3,3 at ptxtSpace=5,
  then final Recode at ptxtSpace=5.

Only after that final Recode should the saved application intFactor be restored modulo 5.

This is source-aligned and avoids changing the nonlinear Algorithm-4 input representation.

## 10. Scientific boundary

This turn closes:

  exact dirty Z_625 lift admissibility for Algorithm 4;
  exact six-boundary plaintext-space typing;
  semantic safety of HElib factor harmonization;
  semantic quotient correctness of divideByP;
  current initial intFactor=1 interface;
  final stock intFactor-restoration placement.

It does NOT close:
- native recovery correctness;
- actual six-boundary noise/capacity trajectory;
- actual prime sets selected inside Fe multiplications;
- source-faithful Aung artifact implementation details;
- baseline correctness;
- end-to-end candidate native correctness.

The historical conclusion that exact factor/capacity recurrence is runtime-state dependent remains
valid in general; Turn 15 only removes the obsolete initial-factor-399 premise for the CURRENT
late-aggregation candidate.

## Verdict

PASS_DIRTY_Z625_ALGORITHM4_DOMAIN
PASS_SIX_DIVIDEBYP_PLAINTEXTSPACE_LADDER
PASS_HELIB_DIVIDEBYP_SEMANTIC_QUOTIENT
PASS_FACTOR_HARMONIZATION_SEMANTIC_INVARIANCE
PASS_CURRENT_ALGORITHM4_INITIAL_INTFACTOR_ONE
PASS_FINAL_INTFACTOR_RESTORE_PLACEMENT

NATIVE_EXECUTION=NOT_OBTAINED
CAPACITY_RECURRENCE=RUNTIME_STATE_DEPENDENT
AUNG_ARTIFACT_IMPLEMENTATION=UNVERIFIED

CORRECTNESS_GATE remains BLOCKED because the native small recovery canary and later end-to-end
candidate correctness are still missing.

NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Primary blocker remains the frozen recovery-only HElib canary execution.

Once execution is available, after recovery PASS the first end-to-end candidate correctness run
must instrument all six Algorithm-4 y-u/divideByP boundaries and assert:
- incoming operand ptxtSpace equality;
- semantic/debug divisibility before divideByP;
- ptxtSpace ladder 625,625,125,625,125,25;
- resulting spaces 125,125,25,125,25,5;
- intFactor/noise/primeSet before and after harmonization;
- final Recode at ptxtSpace=5;
- saved application intFactor restored only afterward;
- final decrypt equals stock/source plaintext.

Do not infer capacity from this semantic PASS.
