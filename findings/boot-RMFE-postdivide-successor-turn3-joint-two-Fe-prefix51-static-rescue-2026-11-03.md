# BOOT / B158 — Successor Research Turn 3 — joint two-Fe fixed-prefix static rescue with 51-bit ctxt-prime granularity

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: legacy-484479fe4613
PHASE: CORRECTNESS_GATE
Native execution: NONE

## Authority / read-before-write

The PI supplied local fallback authority at fdbf8cc..., but current durable GitHub memory already contains the Turn2 finding blob 64f6e335efa9877bd92bd26969c7fd2428624647 and commit ccbb5c3d07d1e953189624150351a9bb5b0cc784. A direct compare confirms ccbb5c3d... is exactly one finding commit ahead of fdbf8cc.... Therefore this turn uses Turn2 only as the current durable scientific predecessor, without treating stale STATE.md as authority over the explicit BOOT handoff.

Read-only prerequisites:
- successor Turn2 blob 64f6e335efa9877bd92bd26969c7fd2428624647;
- Turn23 first-F5 full envelope blob 3afdaa04beb223e630acc5196901d55bfb785b04;
- Turn22 fixed-prefix derivation blob 01381a2a7098e94eace04582f7a14d90505bde8d;
- Turn17 first-Fe modulus-switch proof blob 49b839ccb00201b9f16fa5de74db2855e22a7b50.

Pinned HElib source: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.
New source facts checked this turn:
- CMakeLists.txt permits HELIB_SP_NBITS override in [1,64];
- src/macro.h uses the override directly when set;
- PrimeGenerator::B=3 and each len-bit ciphertext prime lies in [(1-2^-3)2^len, 2^len)=[(7/8)2^len,2^len);
- Context::ctxtPrimeSize(400) and addCtxtPrimes follow the source formulas audited below.

The target finding path was checked absent before write.

## Closest prior / exact delta

Closest prior remains Aung Algorithm4 plus pinned HElib BGV fixed-set multiplication semantics.

Turn2 proved that the inherited first-crossing-183 prefix cannot support the second Fe first square under the current independent coefficient-L1/mod-down proof and a security-compatible hwt.

This turn performs the one allowed bounded structural redesign:
  replace the first-crossing-183 policy by a common prefix chosen for two consecutive Fe evaluations,
and test whether a source-guaranteed discrete HElib prefix can satisfy the COMPLETE first-F5 envelope and COMPLETE second-Fe first-square inequality.

No novelty claim is added.

## Primary hypothesis / falsifier

H3:
There exists a source-guaranteed common fixed ciphertext-prime prefix P_common, available under a legal pinned-HElib build configuration and the current h=120 correctness certificate, such that:
1. the complete first F5 evaluation is independently correct at P_common; and
2. without a second mod-down, the first square of the second F5 is independently correct at the same P_common.

Falsifier:
after accounting for actual HElib prime granularity, no prefix interval can be certified to lie inside the full two-Fe sufficient window.

## 1. Common-q recurrence

Retain the source-faithful first-F5 recurrence from Turn23:
  A = (q/Q0)E0 + R
  E2 = A^2 + K
  E3 = A(E2+1872)+K
  E4 = E3 + H(A+C1)
  EF = E4 E2 + K + U2(E2+5 U1 A).

Use the current h=120 sparse-secret certificate:
  R = 312.5 * 16384 * (1+120)
    = 619,520,000.

Frozen conservative bounds:
  E0 <= 1.1433532886831608e35,
  Q0 >= 2^399.5,
  K(q) <= Khat = 401,679,183,790,909,
  H,C1,U1,U2 <=312.

The complete first-F5 sufficient condition is:
  EF(q) < 0.48 q.

The second Fe begins from W=F5(z), already resident at the SAME prefix P_common. Therefore there is no second modulus switch and no second R charge before its first square.

Its first square has sufficient independent envelope:
  E_sq2(q) <= EF(q)^2 + K(q).

Required second-square condition:
  EF(q)^2 + K(q) < 0.48 q.

Using the above conservative recurrence, the continuous full second-square safe interval is approximately:
  293.1307116155 < log2 q < 313.9382278811.

This interval is a full sufficient result for the recurrence, not merely Turn2's R^5 necessary condition.

For reference, the complete first-F5 condition is much looser in this h=120 regime; its conservative interval is approximately:
  147.0947899594 < log2 q < 353.5343333567.
Hence the second-square condition is the binding one.

## 2. Source-guaranteed discrete prefix by fixing HELIB_SP_NBITS=51

Pinned CMake legally accepts:
  -DHELIB_SP_NBITS=51.

For PrimeGenerator::B=3:
  bit_loss = -log2(1-1/8)=log2(8/7)=0.1926450779423958....

Context::ctxtPrimeSize(400) computes:
  nPrimes = ceil(400/(51-bit_loss)) = 8.

The code only decreases targetSize from 51 to50 if:
  (50-bit_loss)*8 >=400.
But:
  (50-bit_loss)*8 ~=398.4588393765 <400.
Therefore:
  ctxtPrimeSize(400)=51.

addCtxtPrimes then adds 51-bit primes until the accumulated bit length reaches at least399.5. Seven such primes have product strictly below2^(7*51)=2^357, so at least eight ctxt primes exist. Thus the first six ctxt primes always exist.

Each of those six satisfies:
  (7/8)2^51 <= q_i <2^51.

Therefore their product q6 satisfies exactly:
  q_min = ((7/8)^6) 2^306
        = 117649 * 2^288
  <= q6 < 2^306 = q_max.

Hence:
  304.8441295323456... <= log2 q6 <306.

The ENTIRE source-guaranteed six-prime interval lies inside the conservative continuous two-Fe safe interval:
  [304.8441,306) subset (293.1307,313.9382).

This removes the Turn2 prime-granularity uncertainty for this bounded redesign.

## 3. Uniform integer-safe certificate over every possible six-prime product

To avoid relying on the exact generated prime values, maximize the first-F5 input bound at q_max=2^306 and minimize the RHS at q_min=117649*2^288.

Using:
  Q0 >=2^399.5,
  E0 <=1.1433532886831608e35,
  R=619,520,000,
gives:
  A < 627,683,489.73.
Use the integer upward bound:
  Ahat = 627,683,490.

Then:
  E2hat = Ahat^2 + Khat
        = 394,388,242,802,371,009.

  E3hat = Ahat*(E2hat+1872)+Khat
        = 247,550,988,657,562,469,411,225,599.

  E4hat = E3hat +312*(Ahat+312)
        = 247,550,988,657,562,665,248,571,823.

  EFhat_joint
        = E4hat*E2hat + Khat
          +312*(E2hat +5*312*Ahat)
        = 97,631,199,420,645,816,100,334,968,529,769,915,061,277,924.

Thus:
  log2(EFhat_joint) ~=146.1302503351.

For the first F5, an integer-safe uniform certificate is:
  25*EFhat_joint < 12*q_min.
The resulting margin is about157.655 bits, so first-F5 correctness is not close to binding.

For the second Fe first square, the exact integer-safe certificate is:
  25*(EFhat_joint^2 + Khat)
  <
  12*q_min
  =
  12*117649*2^288.

Explicitly:
  LHS =
  238296277507847798434032929027355835856683068024388897956505199783162254546739578838517125

  RHS =
  702114977284499863955262793346703900203742788221885939309837757010039859968330469177062064128

and LHS<RHS.

The uniform second-square margin is:
  log2(RHS/LHS) ~=11.5247351731 bits.

Therefore EVERY possible first-six ctxt-prime product generated by the pinned source under HELIB_SP_NBITS=51 satisfies the conservative complete first-F5 plus second-Fe-first-square correctness inequalities.

No exact prime enumeration is required.

## 4. Same-prime-set and BGV factor ledger

Let a=67 be the Algorithm4-entry factor and q=q6.

Bring the Algorithm4 input to P6 once using the existing fixed-target mechanism.

First F5:
  input factor = a;
  x^2 factor = a^2 q;
  cubic branch factor = a^3 q^2;
  first-F5 output factor:
      d = a^5 q^4 mod625.

All Turn23 explicit sibling aligners remain units because gcd(aq,625)=1.

The first-F5 output W remains on P6. The second Fe first square uses the fixed-target square directly at P6, with no call to a new proof-driven mod-down:
  factor(W^2) = d^2 q
              = a^10 q^9 mod625.

This is again a unit modulo625.

Pinned Turn19 semantics establish that reLinearize on a target containing only ctxt primes does not replace the fixed target by a naturalPrimeSet heuristic; the same P6 is retained through the multiplication/key switch.

Thus the two-Fe square certificate does not rely on stock noise-estimator-driven prime-set selection and charges the modulus-switch rounding term only once.

This turn does NOT claim the complete second F5 has been evaluated. The later second-F5 cubic/outer/sibling nodes and the final L2 subtraction/divide remain downstream.

## 5. Scientific consequence

PASS_JOINT_TWO_FE_COMMON_PREFIX_EXISTENCE.
PASS_SOURCE_GUARANTEED_P6_INTERVAL_WITH_HELIB_SP_NBITS_51.
PASS_COMPLETE_FIRST_F5_AT_P6.
PASS_SECOND_FE_FIRST_SQUARE_AT_P6.
PASS_SAME_PRIME_SET_AND_FACTOR_UNIT_LEDGER_FOR_THIS_BOUNDARY.

Turn2's obstruction is therefore a prefix-policy / modulus-granularity artifact, not a no-go for repeated Fe evaluation.

The active candidate survives its one bounded structural redesign.

However this repair changes an implementation build parameter relative to the previously unspecified author configuration:
  HELIB_SP_NBITS=51.

Therefore:
- no claim that Aung used this value;
- no claim of author-artifact reproduction;
- matched baseline must use the same build when performance is eventually measured;
- final security must be recomputed for the resulting actual full Q and context;
- no value/performance claim is authorized.

## Verdict

Primary H3: PASS at STATIC/MATH evidence grade.

The critical correctness blocker moves from:
  second Fe first square
to:
  remaining second-F5 nodes and the full L2(z)-F5(F5(z)) subtraction/divide boundary on the new P6 construction.

Mandatory recovery-only native canary remains NOT_EXECUTED.

Novelty=PREFLIGHT.
Security=PENDING.
Value=PENDING.
Baseline correctness=PENDING.
Independent audit=PENDING.
Paper readiness=NOT_READY.

## Next decisive Paper-First test

No Native.

Continue on the SAME P6 construction and propagate the independent coefficient-L1 envelope through the remaining source-faithful second-F5 nodes:
  W^2 -> W*(W^2-6)+(W-1) -> outer product -> sibling x^2+5x -> complete F5(W).

Use the current EFhat_joint as the W input envelope and exact factor recurrences. Then test the explicit L2 alignment and the full second 625->125 subtraction/divide numerator.

Do not reopen the inherited Pdagger policy unless this P6 redesign is later falsified.
