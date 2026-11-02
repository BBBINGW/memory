# BOOT Research Turn 23/25 — factor-67 Algorithm-4 unit-closure / divideByP gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

Turn 16 superseded Turn 15's current-candidate Algorithm-4 initial factor:

  OLD: 1
  CURRENT: 67 mod625

because public scalar-unit normalization by 28 leaves ciphertext parts/noise unchanged and updates
the BGV metadata factor to 28^{-1}=67.

Turn 23 asks whether the actual pinned HElib metadata rules used inside Aung Algorithm 4 preserve
5-adic unit-ness starting from factor67 through:
- Fe ciphertext multiplications;
- factor harmonization at y-u subtractions;
- all six divideByP boundaries.

Hypothesis:
starting from intFactor 67 at plaintext space625, every factor appearing anywhere in the
Algorithm-4 DAG remains a unit modulo the current power of5. Therefore:
- every HElib InvMod needed by add/sub harmonization is well-defined;
- divideByP's intFactor reduction remains a unit;
- the source semantic quotient proof from Turn15 applies unchanged;
- no hidden factor-divisibility correctness failure is introduced by the Turn16 normalization.

Falsifier:
- tensorProduct can create an intFactor divisible by5;
- harmonization can multiply by a nonunit;
- divideByP can turn a unit modulo 5^s into a nonunit modulo 5^(s-1);
- or a current Algorithm-4 operation uses a factor-changing rule not covered by these closures.

No native execution or capacity prediction is claimed.

## 1. Initial factor is exactly a 5-adic unit

After shared reconstruction:
  ptxtSpace = 625
  intFactor = 1.

The pure normal_basis=false EvalMap inverse preserves that factor.

Turn16's public scalar normalization:

  multByConstant(28L)

uses the BGV scalar-unit fast path.

Because:
  gcd(28,625)=1
  28^{-1}=67 mod625,

the new metadata factor is exactly:

  f0 = 67.

And:
  gcd(67,5)=1.

So f0 belongs to the unit group:
  (Z/625Z)^*.

This is the only current-candidate initial factor for Algorithm4.

## 2. Public polynomial operations preserve the factor

The recovery tree, L0..L3 recombination, and Aung correction-map constants use public polynomial
multiplication/addition.

Pinned ZZX/DoubleCRT multByConstant does not change intFactor.

Pinned addConstant does not change intFactor.

Hence public linear operations preserve the current unit factor exactly.

## 3. Ciphertext multiplication preserves unit-ness

Pinned Ctxt::tensorProduct for BGV sets, at plaintext space P:

  f_out = f1 * f2 * q mod P,

where:
  q = productOfPrimes(currentPrimeSet) mod P.

The ciphertext modulus Q = productOfPrimes(currentPrimeSet) is invertible modulo the BGV plaintext
space. This coprimality is an explicit HElib requirement whenever Q^{-1} modulo the plaintext space
is used; pinned rawModSwitch, for example, computes that inverse and requires coprimality.

For current Algorithm4:
  P is one of 625,125,25,5.

Every P is a power of the same plaintext prime5.

Therefore:
  q is a unit modulo P.

If f1 and f2 are units modulo P, then:
  f_out = f1*f2*q

is also a unit modulo P.

Thus EVERY Fe ciphertext multiplication preserves 5-adic unit-ness, even though the exact numeric
factor depends on the runtime current prime set.

This is why an exact numeric factor trajectory cannot be fixed statically, but invertibility can.

## 4. Modulus maintenance does not create a nonunit factor

Pinned real modDownToSet, the active BGV path, leaves intFactor unchanged.

The disabled degenerate-drop path would multiply intFactor by a product-of-dropped-primes residue,
which is also a plaintext-space unit when the modulus chain is valid, but the pinned active path does
not use it.

modUpToSet scales ciphertext parts/noise and does not change BGV intFactor.

Hence dynamic prime-set selection inside multiplication/relinearization can change q and noise, but
not the invariant:

  gcd(intFactor,5)=1.

## 5. Factor harmonization uses only units

Pinned Ctxt::addCtxt handles different BGV factors f1,f2 by computing:

  ratio = f2 * f1^{-1} mod P,

which already requires f1 to be invertible.

It runs extended Euclid to choose e1,e2 satisfying:

  e1*f1 = e2*f2 mod P

and explicitly asserts:

  gcd(e1,P)=1
  gcd(e2,P)=1.

Then mulIntFactor(e) updates:

  intFactor <- intFactor*e mod P

while multiplying ciphertext parts by the same balanced e.

Therefore harmonization multiplies a unit factor by another unit and preserves unit-ness.

There is no path by which the y-u subtraction can create a factor divisible by5.

## 6. divideByP preserves unit-ness under reduction

Pinned Ctxt::divideByP requires:
  p divides P
  P > p,

then performs:
  ciphertext parts *= p^{-1} mod Q
  noiseBound /= p
  ptxtSpace <- P/p
  intFactor <- intFactor mod (P/p).

Let:
  P = 5^s
and let f be a unit modulo P.

Then:
  5 does not divide f.

Reducing f modulo:
  P' = 5^(s-1)

cannot make it divisible by5.

Therefore:
  f mod P'

is also a unit.

So every one of the six Algorithm4 boundaries preserves invertibility as the ladder moves:

  625 ->125 ->25 ->5.

For the initial factor67 specifically, if no intervening multiplication/harmonization altered the
numeric factor, its direct reductions would be:

  67 mod625 = 67
  67 mod125 = 67
  67 mod25  = 17
  67 mod5   = 2,

all units.

These numeric reductions are illustrative only; the actual factors after Fe are q-dependent.

## 7. Inductive unit-closure theorem for the full Algorithm-4 DAG

Define property U(c):

  gcd(c.intFactor,5)=1.

Base:
  L0,L1,L2,L3 enter Algorithm4 with factor67, so U holds.

Inductive operations:

1. public polynomial multiplication:
   factor unchanged -> U preserved;

2. public addition of constants:
   factor unchanged -> U preserved;

3. ciphertext multiplication:
   f_out=f1*f2*q with all three units -> U preserved;

4. automorphism/relinearization/active real mod-switch:
   factor unchanged or reduced through compatible plaintext-space gcd -> U preserved;

5. add/sub harmonization:
   factor multiplied only by asserted units -> U preserved;

6. divideByP:
   unit modulo 5^s reduces to unit modulo 5^(s-1) -> U preserved.

Therefore every ciphertext state reachable in Algorithm4 from current L0..L3 satisfies U.

Conclusion:

  NO Algorithm4 factor can become a multiple of5.

This closes the correctness concern created by replacing initial factor1 with factor67.

## 8. divideByP semantic quotient remains exactly Turn15's theorem

Turn15 proved pinned divideByP implements the semantic quotient:

  m = 5*m'
  -> divideByP encrypts m'

at the reduced plaintext space.

That proof was parameterized by an arbitrary metadata factor f and required only that the HElib
representation remain valid.

Turn23 now proves the current factor67 path satisfies the needed invertibility invariant throughout
the DAG.

Thus the six semantic quotient claims remain valid with the CURRENT normalization path.

No Turn15 dirty-lift or divisibility theorem needs redesign.

## 9. Exact six-boundary correctness contract remains unchanged

The Algorithm4 plaintext-space schedule stays:

  B1: 625 ->125
  B2: 625 ->125
  B3: 125 ->25
  B4: 625 ->125
  B5: 125 ->25
  B6: 25  ->5.

At every pre-subtraction boundary:
- y and u have the same plaintext space;
- their factors are units;
- addCtxt can harmonize them if numerically different;
- semantic subtraction remains y-u;
- Aung's theorem supplies divisibility by5;
- divideByP returns the exact quotient and a unit factor in the lower space.

So factor67 introduces no new correctness branch in this ladder.

## 10. What cannot be closed statically

The exact NUMERIC factor after Fe cannot be frozen from source alone because multiplication uses:

  q = Q mod P

with Q determined by the runtime prime set selected by naturalPrimeSet / bringToSet / relinearize.

Therefore:
  exact factor trajectory = runtime-state dependent.

Likewise:
- harmonization choices e1,e2 depend on actual factors and noise bounds;
- noise cost depends on balanced representatives of e1,e2;
- prime-set trajectory affects multiplication factor q and capacity.

Turn23 proves only the algebraic/unit invariant needed for correctness.

It does NOT prove a capacity bound or low harmonization cost.

## 11. Native instrumentation refinement

After the mandatory recovery canary and exact interface gates pass, the first full candidate run
must instrument for each Fe multiplication and each of the six subtraction/division boundaries:

  ptxtSpace
  intFactor
  gcd(intFactor,5)
  primeSet
  Q mod current ptxtSpace
  noiseBound.

Hard assertions:

  gcd(intFactor,5)==1 at every observation point;

before each divideByP:
  semantic/debug numerator divisible by5;

after each divideByP:
  ptxtSpace follows the frozen ladder;
  gcd(intFactor,5)==1.

Any failure of unit-ness is:

  FAIL_FACTOR67_ALGORITHM4_UNIT_CLOSURE

before any timing interpretation.

## Verdict

PASS_FACTOR67_ALGORITHM4_UNIT_CLOSURE
PASS_CTXT_MULTIPLICATION_PRESERVES_5ADIC_UNIT_FACTOR
PASS_HARMONIZATION_PRESERVES_5ADIC_UNIT_FACTOR
PASS_DIVIDEBYP_PRESERVES_5ADIC_UNIT_FACTOR
PASS_FACTOR67_DIVIDEBYP_SEMANTIC_COMPATIBILITY
SUPERSEDE_TURN15_INITIAL_FACTOR_ONE_ONLY

EXACT_ALGORITHM4_FACTOR_TRAJECTORY=RUNTIME_STATE_DEPENDENT
CAPACITY_EFFECT=UNRESOLVED
NATIVE_EXECUTION=NOT_OBTAINED

This closes the specific correctness risk introduced by Turn16's factor67 normalization.

It does NOT advance the native evidence order beyond source/math correctness.

CORRECTNESS_GATE remains BLOCKED.
BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Primary evidence-order blocker remains the frozen revised recovery-only HElib canary.

After that PASS and exact parameter/interface verification, the first full candidate correctness run
must add the factor-unit instrumentation above at every Algorithm4 multiplication and all six
divideByP boundaries.

No capacity or timing conclusion is authorized from this unit-closure PASS.
