# PURE-FHE P0-PRESCOUT-61 — Covariant Typed Precision: Recovery / Modulus Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-61
LATEST_COMPLETED: P0-PRESCOUT-61
NEXT_ITERATION: P0-PRESCOUT-62 NOT_STARTED
STATUS: PASS_TYPED_RECOVERY_GATE / PASS_STRICT_SOURCE_BOUND_MODULUS_SEPARATION / PASS_PUBLIC_CORRECTION_COUNT / SECURITY_PARAMETER_NOT_CLOSED / NOVELTY_NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Question

P0-60 established exact message-preserving unit rebasing and a toy local-error separation for a public ciphertext type p_v.

P0-61 asks the promised decisive question:

Does the advantage survive the source's GLOBAL coefficient-recovery constraint once:
- all dummy/background slots are included;
- source-shaped fresh encryption, key-switch/relinearization, and rescaling bounds are used;
- the best FIXED unit is optimized too;
- scale Delta and output modulus Q are jointly optimized;
- public correction costs are counted?

If not, kill the candidate before implementation.

## 2. Primary source

Zhaoyang Liang, Runkun Liu, Jingwei Fang, Dan Ding,
"A New Approach to Reducing Modulus Requirements in Homomorphic Computation: Precision Allocation in CKKS,"
ePrint 2026/2562, revision 2026-10-22.

Verified full PDF via eprint.iacr.asia.

Source facts used:

### Recovery

Equation (7) gives the sufficient final recovery condition

  ||sigma^{-1}(x_out)||_{coef,infty}
  + (1/r) sum_j |sigma_j(p)| B_out,j
  < Q_out/(2 Delta_out).

Every slot contributes, including unused/dummy slots.

### Two-class unit

Section 4.2 gives the exact d=2 unit

  U = 1 + sqrt(2)

with embedding magnitudes

  (t, t^{-1}),
  t = 1+sqrt(2),
  log2 t = 1.271553303...

Integer powers U^k are actual cyclotomic units.

### Source primitive bounds

Appendix D, N=2^15 example:
- input messages in [3/4,7/8];
- log2 B_enc = 14.349;
- log2 B_dec = 25.111;
- log2 K_1 = log2 K_2 = 107.546;
- log2 R_1 = log2 R_2 = 118.111;
- scale-rounding mismatch |chi_t-1| < 2^-1023;
- numerical decoder error <=2^-734.

Thus use

  B_fresh := B_enc+B_dec,
  log2 B_fresh ~=25.111831,

  K :=2^107.546,

  C := K+R,
  log2 C ~=118.111952.

The source defines K_v for relinearization or key switching. For the minimal constructed rotation we instantiate its switching key with the same decomposition/noise bound as K_1.

This is a source-shaped analytical instantiation, not a measured author benchmark for this new circuit.

### Operation costs

Section 7.3:
- a nontrivial precision-allocation multiplication correction multiplies three ciphertext-product components, costing 3 N L_Q modular products;
- a nontrivial automorphism correction q_tau costs 2 N L_Q modular products;
- q_tau=1 costs no public correction.

## 3. Typed restored-error recurrence

Let

  E_{v,j}:=|sigma_j(p_v)| B_{v,j}

be the restored logical-error bound.

This is the quantity that enters both precision and recovery.

For typed ciphertexts the source formulas become especially simple.

### Fresh input

  E_{0,j}
    <= w_{0,j}(B_enc+B_dec)/Delta_0,

where

  w_{0,j}:=|sigma_j(p_0)|.

### Exact public rebase

For

  r=p_a p_v^{-1},

multiplying the ciphertext components by r preserves the restored polynomial exactly.

Therefore

  E_{v,j}=E_{a,j}

for a pure rebase.

### Automorphism

If tau moves input slot k to output slot j, choose output type p_v and public correction

  q=tau(p_a)p_v^{-1}.

The restored-error recurrence is

  E_{v,j}
    <= E_{a,k} + w_{v,j} K_v/Delta_v.

In the covariant choice

  p_v=tau(p_a),

q=1.

### Multiplication + rescaling

Starting from the exact typed invariant and applying the source Lemma-7.2 expansion gives

  E_{v,j}
  <= A_{a,j} E_{b,j}
   + A_{b,j} E_{a,j}
   + E_{a,j}E_{b,j}
   + w_{v,j}(K_v+R_v)/(D_v Delta_v),

for exact scale arithmetic.

For squaring:

  E_v
  <=2 A E_a + E_a^2
    +w_v C/(D Delta_v).

When input/output scales are kept equal to Delta,

  D approximately Delta,

so the last term is approximately

  w_v C/Delta^2.

This is the source recurrence rewritten in restored coordinates. Past logical error is not multiplied again by a new unit; only NEW primitive error carries the output type.

## 4. Minimal source-shaped circuit

Use two equal slot classes A and B in the d=2 subfield.

Logical circuit:

1. Input:
   - A contains x in [3/4,7/8];
   - B contains dummy zero.
2. Square + Rescale.
3. Automorphism tau swaps A and B.
4. Square + Rescale.
5. Required output is the moved value in B.

The output active magnitude is bounded by

  A_out=(7/8)^4 ~=0.58618.

Required active-slot absolute precision:

  epsilon=2^-160.

For recovery, using

  ||sigma^{-1}(x_out)||_{coef,infty} <= A_out

is a conservative bound.

A sharper exact periodic half-slot bound A_out/2 was also tested; the final separation changes by less than one bit.

Both multiplications use C above.
The rotation uses K above.

No plaintext-addition errors are present.

## 5. Best fixed-unit optimization

Let the one fixed unit be

  p=U^m,

with weights

  w_A=t^m,
  w_B=t^{-m}.

Importantly, the best fixed unit is NOT p=1.

It can sacrifice early precision in A in order to suppress the later B-side rotation error.

For each integer m and continuous log2 Delta:
- propagate the complete restored recurrence;
- require E_out,B <=2^-160;
- set the minimal recovery output modulus by

    Q_out > 2 Delta (A_out + (E_out,A+E_out,B)/2);

- with two same-scale rescalings, take the continuous initial-modulus certificate

    log2 Q_0
      = log2 Q_out + 2 log2 Delta.

Joint optimization gives approximately:

  m = 32,
  log2 |sigma_A(p)| = +40.6897,
  log2 |sigma_B(p)| = -40.6897,

  log2 Delta_fixed = 228.3526,

  log2 Q_out,fixed = 228.5820
  under the conservative A_out recovery bound,

  log2 Q_0,fixed = 685.2872 bits.

Using the sharper exact half-slot coefficient bound instead gives
  log2 Q_0,fixed ~=684.2872.

The difference is irrelevant to the separation.

At the precision boundary, the fixed unit balances:
- fresh input error amplified in A;
- future rotation/key-switch error suppressed in B.

This is why P0-60's equal-local-noise toy was not yet sufficient.

## 6. Best covariant typed optimization

Use

  p_1=U^{-k}

before the rotation, so

  (w_A,w_B)=(t^{-k},t^k).

After the swap set

  p_2=tau(p_1),

so the weights swap:

  (w_A,w_B)=(t^k,t^{-k}).

Therefore:
- initial/fresh error on active A is suppressed;
- first multiplication error on active A is suppressed;
- after rotation the same logical data lands in B, where the NEW KS error is also suppressed;
- stage-2 multiplication error in B is suppressed;
- q_tau=1 exactly.

The dummy branch accepts the reciprocal amplification and is charged in final recovery.

Joint integer-k / scale / recovery optimization with conservative A_out gives approximately:

  k=64,
  log2 t^k =81.3794 bits,

  log2 Delta_typed =186.7813,

  log2 Q_out,typed =191.1536,

  log2 Q_0,typed =564.7162 bits.

With the sharper exact half-slot coefficient bound, the optimizer is k=63 and gives

  log2 Delta_typed ~=188.0529,
  log2 Q_out,typed ~=188.2686,
  log2 Q_0,typed ~=564.3743.

Thus the result is robust to the coefficient-message bound.

## 7. Global recovery is ACTIVE, not omitted

This is the key check.

In the sharper k=63 optimum:

  final required B-slot error ~=2^-160,

but the dummy A-slot error is approximately

  E_out,A ~=0.575.

Hence the average restored-error contribution to recovery is approximately

  (E_out,A+E_out,B)/2
    ~=0.2876.

The ideal-message coefficient term is about 0.293 in the exact periodic half-slot calculation.

So the typed optimizer deliberately uses essentially the whole recovery room:

  message term ~=0.293,
  dummy-error term ~=0.288.

This proves the advantage is NOT an artifact of forgetting dummy slots.

By contrast, at the best fixed optimum the average error term is negligible compared with the ideal-message term.

This is exactly the precision-vs-recovery tradeoff described by Sections 6 and 8 of the source, now optimized over a time-varying type schedule.

## 8. Strict modulus separation

Using the conservative recovery bound:

  fixed:
    log2 Q_0 ~=685.287 bits,

  typed:
    log2 Q_0 ~=564.716 bits.

Gap:

  G_Q ~=120.571 bits.

Using the sharper exact periodic recovery term:

  G_Q ~=119.913 bits.

Therefore conservatively report:

  **about 120 bits of continuous initial-modulus headroom.**

The source's RNS primes in Appendix D are roughly 46--49 bits.

120 bits is larger than two 49-bit primes:

  120 > 98,

and smaller than three 46-bit primes:

  120 < 138.

Thus the analytical headroom is robustly worth **at least two source-sized RNS primes** if an integer RNS chain can realize the continuous optimum.

A concrete NTT-prime schedule has NOT yet been instantiated, so no claim of an exact prime count is made.

## 9. Why typed beats the fully optimized fixed unit

The fixed unit faces a temporal conflict.

To protect the fresh input and first multiplication it wants

  w_A <<1.

To protect the post-rotation key-switch and final output it wants

  w_B <<1.

Because w_A w_B=1, a single fixed unit cannot do both.

The optimizer chooses only moderate imbalance, m=32.

Typed scheduling removes that temporal conflict:

  p_1 protects A;
  p_2=tau(p_1) protects B.

The large reciprocal weights are pushed into the slot class that is dummy at that time.

Final recovery, not local precision, becomes the limiting factor.

## 10. Public-correction operation count

This gate does not hide an extra correction kernel.

### Best fixed p=U^32

Both multiplications have nontrivial p and therefore pay the source's
  3 N L_Q
public modular products each.

The A<->B automorphism does not fix U^32, so q_tau!=1 and pays an additional
  2 N L_Q
public modular products.

### Typed schedule

Both multiplications also have one nontrivial public type correction, so their correction-count class is unchanged.

For the rotation,

  p_2=tau(p_1),

hence

  q_tau=1.

Therefore the typed path pays **zero** automorphism-correction modular products.

There is no separate standalone rebase on this single path.

Thus, before accounting for the smaller L_Q from the reduced modulus, typed scheduling already has no larger correction count and saves the fixed method's rotation correction.

## 11. Security boundary

This round is NOT a complete secure-parameter instantiation.

The source Appendix-D N=2^15 parameter set has approximately:
- 469 bits of Q_0;
- four ~28-bit auxiliary primes, about 112 bits of P;
and its archived estimator result exceeds 128-bit security.

The new 160-bit toy continuous candidates have larger Q_0:
- fixed about 685 bits;
- typed about 565 bits.

Therefore the source's archived security statement cannot simply be copied to this new circuit.

What is true structurally:
- typed uses a strictly smaller Q than the matched fixed construction;
- for any fixed N / secret / error distribution, this does not make RLWE security worse than the fixed candidate.

But an actual >=128-bit parameter point requires a new RNS chain and a pinned estimator run, possibly at a larger N.

Do NOT claim a concrete secure runtime yet.

## 12. Prior-art boundary

P0-60 already established:
- generic changing of a decryption factor is concurrent prior art in GCKKS 2026/2600;
- fixed precision-allocation units are 2026/2562;
- Focused CKKS 2026/2531 is the largest unresolved concurrent-overlap risk.

The full 2531 text was not yet audited in this iteration.

Therefore:

  NOVELTY: NOT_ESTABLISHED.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-61

STATUS:
PASS_TYPED_RECOVERY_GATE /
PASS_STRICT_SOURCE_BOUND_MODULUS_SEPARATION /
PASS_PUBLIC_CORRECTION_COUNT /
SECURITY_PARAMETER_NOT_CLOSED /
NOVELTY_NOT_ESTABLISHED /
HUMAN_REVIEW.

RESULT:
- After including all-slot recovery, fresh encryption error, source Appendix-D KS/relinearization/rescale bounds, and the BEST fixed unit, covariant typed precision still wins.
- The best fixed unit is U^32, not 1.
- The best typed two-stage schedule is approximately U^-63/U^-64 followed by its Galois conjugate, depending on the conservative recovery bound.
- Same 160-bit active output precision admits about 120 bits less continuous initial modulus.
- The advantage is recovery-limited: typed intentionally fills dummy-slot recovery room.
- Public-correction count does not erase the gain; covariant rotation removes one correction that the best fixed unit needs.
- No native implementation is warranted yet.

CODEX_REQUIRED:
NO.

NEXT_TEST P0-62:
Do novelty before implementation/security tuning.

1. Acquire and audit the full current 2026/2531 Focused CKKS paper.
2. Search specifically for:
   - ciphertexts carrying a changing focus/unit type;
   - message-preserving unit rebase p_a p_v^{-1};
   - Galois-covariant transport p_out=tau(p_in);
   - circuit-wide or node-wise unit schedules;
   - changing active/focus slot sets during ordinary leveled evaluation.
3. If 2531 already contains the typed/covariant construction, KILL/PARK this line immediately.
4. If it does not, then P0-63 should instantiate one integer RNS chain and run a pinned >=128-bit estimator before any native code.

STATE_UPDATE:
YES — this finding only.
