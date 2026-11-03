# BOOT / B158 — Successor Research Turn 13 — shared eight-orbit four-correction-output closure

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE

BACKGROUND_NATIVE_TASK:
    BOOT-T11-R8-SMALL-CANARY-20261103-R2

BACKGROUND_TASK_STATUS:
    PENDING / RESULT UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Read-before-write / authority

GitHub Notes read remains degraded.
Durable context was recovered from the verified local-Git authority at:

    BBBINGW/memory main
    93ce8c686c087042e090455fa206de1947cfff4c

Immediate predecessor:

    findings/boot-successor-turn12-aung-runtime-profile-reproducibility-boundary-2026-11-03.md
    blob 5bc99acc6270c50b89556f8d913d72faf442bedb.

The target Turn-13 path was checked absent before write.

The pending R2 source/work directory/binary/result was not modified, rerun, inspected, or inferred.
No new native task was launched.

## Why this turn is paper-level

The current sparse-R8 candidate was statically specified as:

    five Aung Method-1 projections
    -> sparse coefficient carrier
    -> ONE MultKey
    -> unnormalized RM10
    -> one fused eight-Frobenius recovery map G
    -> scalar-unit28
    -> Aung correction DigitExtract.

This wording hides a completeness question.

Aung correction Algorithm 4 does not consume only z=L0(z).
For e=4 it needs:

    L0(z), L1(z), L2(z), L3(z)

with:

    L_r(z)
      = sum_i a_i * phi(e_i)^(5^r),

all formed from the SAME coefficient lifts a_i.

If current G only recovers L0, the candidate would contain an unaccounted pre-DigitExtract interface/cost.

This turn tests exactly whether all four outputs can be recovered from the same post-RM10 state without:
- another MultKey;
- another RM10;
- another Frobenius/key-switch orbit.

## Closest prior / exact delta

Primary source:
Aung et al., ePrint 2025/350.

Physical p17:
CtxtsToSlots recombines split thin ciphertexts by public basis multipliers and additions and may compute arbitrary additional linear maps by changing those public constants.

Physical pp19-22:
for correction DigitExtract,

    L_r(sum_i a_i phi(e_i))
      = sum_i a_i phi(e_i)^(5^r),

and Algorithm 4 uses L_{j+1}(z) in the outer loop.

This turn adds no new primitive.
It closes the candidate-specific CtxtsToSlots/correction interface after the ONE merged MultKey.

Historical relevant durable results:
- Turn 7 current candidate:
  exact 8-Frobenius fused map for L0-style recovery;
- older rank-5 shared-correction findings:
  a 5-term Moore/Frobenius route exists on the restricted rank-5 domain.

The historical 5-term route is NOT adopted here because doing so would change the currently running R2 canary's recovery map and normalization.
It remains an optional post-correctness optimization only.

NOVELTY_STATUS remains PREFLIGHT.

## Primary hypothesis

H13:

The same eight orbit ciphertexts

    Z, sigma(Z), ..., sigma^7(Z)

already needed by the current Turn-7 fused recovery can be reused to construct all four Aung correction outputs

    L0,L1,L2,L3

with only additional public constant multiplications and additions.

No additional automorphism/key-switch, MultKey, or RM10 is required.

Falsifier:
- the four outputs need different underlying scalar lifts;
- the coefficient-pair routing does not commute with phi(e_i)^(5^r);
- any output requires a new Frobenius image outside j=0,...,7;
- sharing an already-materialized orbit would trigger a new key switch in HElib;
- or correction-map public constants amplify the independent error envelope to the correctness boundary.

## 1. Fixed sparse post-RM10 domain

Use:

    S = Z/625Z
    R = S[X]/(X^16384+1)
    Y = X^1024
    R8 = S[Y]/(Y^16+1).

The post-reconstruction active coefficient locations are:

    J =
      {0,1,2,3,4,8,9,10,11,12}

in the Y basis.

After the unnormalized 10-stage RM10 trace, write the semantic active state as:

    Z
      = 1024 *
        sum_{i=0}^4
          (
            z_i Y^i
            + z_{i+8} Y^(i+8)
          ).

The z_t are arbitrary Z625 lifts produced by the common MultKey reconstruction.

For each physical SIMD slot, the pair:

    z_i + z_{i+8} Y^8

evaluates to one arbitrary Z625 lift of the recovered branch scalar.

The two physical slots may have different arbitrary high 5-adic digits.
Aung Algorithm 4 permits such arbitrary lifts.

## 2. Four exact target maps

Frozen interpolation RMFE basis:

    phi_i = ell_i(X^16)

with:

    ell_0=[1,50,340,260,599]
    ell_1=[0,4,204,314,104]
    ell_2=[0,622,161,623,469]
    ell_3=[0,418,206,522,104]
    ell_4=[0,156,339,156,599].

For r=0,1,2,3 define:

    P_{r,i} := phi_i^(5^r)

in R modulo625.

The desired global two-slot correction map is:

    C_r
      =
      sum_{i=0}^4
        P_{r,i}
        *
        (
          z_i + z_{i+8} Y^8
        ).

For each physical slot this is exactly:

    sum_i a_i phi(e_i)^(5^r)

for the SAME recovered scalar lifts a_i used by C_0.

Therefore:
- C_0 is z=L0(z);
- C_1,C_2,C_3 are exactly the correction-map ciphertexts required by Algorithm 4.

This same-lift property is essential and follows automatically because every output is synthesized from the same coefficient pairs z_i,z_{i+8}.

## 3. Shared eight-Frobenius synthesis

Let:

    sigma(X)=X^5.

On R8:

    sigma(Y)=Y^5

and sigma has order8.

Define:

    T8 = sum_{j=0}^7 sigma^j.

As in Turn 7:

    T8(Y^t)
      = 8Y^t  for t in {0,8},
      = 0     otherwise.

For every r define:

    G_r(W)
      =
      sum_{i=0}^4
        P_{r,i} T8(Y^{-i} W).

Equivalently:

    G_r(W)
      =
      sum_{j=0}^7
        D_{r,j} sigma^j(W),

where:

    D_{r,j}
      =
      sum_{i=0}^4
        P_{r,i} sigma^j(Y^{-i}).

Crucially:
the orbit ciphertexts sigma^j(W) are independent of r.

Thus all four G_r share exactly the same eight orbit states.

## 4. Exact basis proof

Exact sparse full-ring arithmetic modulo:

    X^16384+1
    and 625

was recomputed independently in this turn.

For every:

    r=0,1,2,3
    t=0,...,15

the identities are:

for t=0,...,4:

    G_r(Y^t)
      = 8 phi_t^(5^r);

for t=8,...,12:

    G_r(Y^t)
      =
      8 phi_{t-8}^(5^r) Y^8;

for padding t in:

    {5,6,7,13,14,15}

    G_r(Y^t)=0.

Result:

    4 * 16 = 64/64 exact basis identities PASS.

Therefore by S-linearity, for every active sparse state:

    G_r(Z)
      =
      1024*8*C_r
      =
      8192*C_r.

## 5. One normalization constant works for all four outputs

Exact unit:

    8192^{-1} mod625 = 28.

Therefore each output is normalized by the SAME source-safe scalar unit:

    L_r
      =
      28 * G_r(Z).

Pinned BGV scalar-unit behavior from Turn 7:
- gcd(28,625)=1;
- no physical ciphertext-part magnitude multiplication is needed by the scalar-unit path used in the candidate;
- semantic normalization is represented by intFactor update;
- resulting intFactor is:

      28^{-1} mod625 = 67.

Hence all four Algorithm-4 entry ciphertexts have common type:

    ptxtSpace=625
    keyID=0
    intFactor=67

after the same cleanup/normalization pattern.

This is stronger than merely proving semantic existence:
the correction-map fanout introduces no initial factor mismatch among L0-L3.

## 6. Exact D_{r,j} support / coefficient-L1 table

All values below use centered coefficients in [-312,312].

### r=0

All j=0,...,7:

    support = 21
    Linf = 311
    L1 = 2811

Total:

    A_0 = sum_j ||D_{0,j}||_1
        = 22488.

This recovers the existing Turn-7 result.

### r=1

All j=0,...,7:

    support = 84
    Linf = 310
    L1 = 13610

Total:

    A_1 = 108880.

### r=2

Rows j=0,...,7:

    j0: support315, Linf310, L1=52352
    j1: support359, Linf310, L1=62345
    j2: support380, Linf310, L1=65869
    j3: support380, Linf310, L1=65869
    j4: support315, Linf310, L1=52338
    j5: support359, Linf310, L1=61249
    j6: support380, Linf310, L1=65869
    j7: support380, Linf310, L1=65869

Total:

    A_2 = 491760.

### r=3

Rows j=0,...,7:

    j0: support540, Linf300, L1=90917
    j1: support945, Linf310, L1=169586
    j2: support873, Linf300, L1=157043
    j3: support873, Linf310, L1=156207
    j4: support555, Linf305, L1=96069
    j5: support926, Linf300, L1=165114
    j6: support862, Linf300, L1=154970
    j7: support868, Linf300, L1=149116

Total:

    A_3 = 1139022.

Worst output:
    L3.

## 7. Reproducibility hashes for the new constant families

This turn defines a NEW explicit canonical encoding independent of the older Turn-7 JSON format:

For each r:
- outer JSON array indexed by j=0,...,7;
- each element is an ascending-exponent array of:
      [exponent, centered_coefficient]
- compact JSON separators "," and ":";
- UTF-8;
- no whitespace.

SHA256:

    r=0:
    a66cd85ac5d5eb51d01e43f9546287443888db93390b63e434754f61002fb77c

    r=1:
    392591813d3a5283b2b12a14820963b28cebcf72e03d111416a0c15106aa6f8b

    r=2:
    7d8bbe75654ef0b3815253b781dac16ddc366fea24a43f6bacbe1244fb7a4550

    r=3:
    a5d4f55965a02b68922ecf9ec7d01a5255620fd4795e46153d9b839f1133c3ab.

The r=0 hash differs from the older Turn-7 hash because the serialization format is deliberately redefined here; the mathematical D_{0,j} family and norms agree exactly with Turn 7.

## 8. Shared HElib execution schedule

Start from one cleaned RM10 ciphertext W on ctxtPrimes.

Materialize once:

    orbit[0] = W

and for j=1,...,7:

    orbit[j] = W
    orbit[j].frobeniusAutomorph(j).

Pinned Ctxt::frobeniusAutomorph(j):
- computes p^j;
- calls smartAutomorph;
- key-switches that orbit image as needed.

This happens exactly seven times total.

Then for each r=0,...,3:

    out_r = 0
    for j=0,...,7:
        tmp = orbit[j]
        tmp.multByConstant(D_{r,j})
        out_r += tmp
    out_r.cleanUp()
    out_r.multByConstant(28L).

Pinned multByConstant:
- multiplies by a public plaintext;
- performs no key switch.

Pinned addCtxt:
- may align prime sets;
- harmonizes BGV factors only when needed;
- performs no automorphism/key switch.

Because every orbit is generated from the same W and all four outputs use the same public-key/context/plaintext-space/factor family, no additional correction-output-specific key-switch family is introduced.

Therefore:

    NONIDENTITY_FROBENIUS / KS CALLS:
      7 TOTAL

for all four outputs jointly.

Not:

    7 per output.

Additional fanout work only:
- 32 public ct-pt multiplications;
- 28 ciphertext additions;
- four output cleanups;
- four scalar-unit28 normalizations.

Relative to the already-required L0 recovery, L1-L3 add:
- 24 public ct-pt multiplications;
- 21 additions;
- 3 cleanups;
- 3 scalar-unit metadata normalizations;
- ZERO new Frobenius/key-switch calls.

## 9. Independent coefficient-L1 envelope for every correction output

Reuse Turn-7 fixed post-RM10 envelope:

    E_RM10
      = 1,835,903,626,782,748,867.

Reuse source-sized one-hop temporary-625 Frobenius key-switch bound:

    K = 401,679,183,790,909.

Reuse cleanup rounding bound:

    R = 83,891,200,000.

For each output:

    E_r
      <=
      (
        sum_j ||D_{r,j}||_1
      ) E_RM10
      +
      (
        sum_{j=1}^7 ||D_{r,j}||_1
      ) K
      +
      R.

Exact resulting envelopes:

### L0

    E_0
      <= 41,293,704,600,473,801,437,489

    log2(E_0)
      <= 75.12833994098

    margin to 0.48Q using log2(Q)>=399.5:
      323.31276636996 bits.

### L1

    E_1
      <= 199,931,454,860,029,347,739,390

    log2(E_1)
      <= 77.40385164899

    margin:
      321.03725466195 bits.

### L2

    E_2
      <= 903,000,468,553,559,669,777,792

    log2(E_2)
      <= 79.57907291871

    margin:
      318.86203339224 bits.

### L3

    E_3
      <= 2,091,555,622,746,351,241,865,519

    log2(E_3)
      <= 80.79085064276

    margin:
      317.65025566818 bits.

Thus the correction-map fanout is nowhere near the linear correctness boundary under the same source-sized assumptions as Turn 7.

This does NOT prove the downstream nonlinear Algorithm-4 trajectory.

## 10. Source-interface closure

Aung physical p17 says CtxtsToSlots may compute arbitrary extra linear maps by changing the public basis-image constants.

The current sparse-R8 construction now has the exact analogous interface without materializing five split thin ciphertexts:

    ONE merged MultKey reconstruction
    -> ONE RM10 coefficient-selection state
    -> ONE shared eight-image Frobenius orbit
    -> four public linear combinations
         G0,G1,G2,G3
    -> scalar-unit28 on each
    -> L0,L1,L2,L3
    -> Aung correction Algorithm 4.

Every output uses the SAME arbitrary Z625 lifts.

Therefore Aung's correction-map divisibility theorem applies at the semantic interface established by prior dirty-lift analysis.

## 11. Important terminology correction

The Turn-7 map G0 is NOT the final RMFE Recode in Algorithm 4 line10.

It is the candidate's replacement for the post-MultKey CtxtsToSlots/recovery linear map:
it reconstructs:

    z = L0(z)

from the sparse coefficient carrier.

Aung Algorithm 4 still ends with its own final source Recode after the nonlinear digit-extraction DAG.

Canonical paper description should therefore distinguish:

1. sparse-R8 correction recovery:
       RM10 -> shared G0..G3;

from:

2. final Aung RMFE Recode:
       Algorithm4 line10.

Conflating these two stages would undercount the complete candidate pipeline.

## 12. Optional 5-term Moore optimization remains parked

Older durable findings prove that, on the restricted rank-5 domain, all four correction outputs can also be synthesized using:
- five Frobenius terms;
- four nonidentity automorphism/key-switch calls;
with exact Moore coefficients.

That route is structurally cheaper than the current 8-term trace formulation.

However adopting it now would:
- change the recovery map being tested by pending R2;
- remove the factor8 trace scale;
- change normalization from 28 to 224;
- change Algorithm-4 entry intFactor from the currently tested 67 path.

Therefore:

    OPTIONAL_5_TERM_MOORE_ROUTE = PARKED_POST_CORRECTNESS_OPTIMIZATION.

Do not supersede R2 or the current canonical construction while Native Step 2 is pending.

## Verdict

PASS_SHARED_EIGHT_ORBIT_FOUR_CORRECTION_OUTPUT_CLOSURE.
PASS_64_OF_64_EXACT_CORRECTION_BASIS_IDENTITIES.
PASS_SAME_LIFT_L0_L3_INTERFACE.
PASS_ZERO_ADDITIONAL_CORRECTION_AUTOMORPHISMS.
PASS_L0_L3_STATIC_L1_MARGIN.
PASS_CORRECTION_RECOVERY_VS_FINAL_RECODE_STAGE_SEPARATION.

CURRENT_SHARED_ORBIT_NONIDENTITY_KS:
    7 total for L0-L3 jointly.

WORST_STATIC_CORRECTION_OUTPUT:
    L3

WORST_PRE_ALGORITHM4_LOG2_ERROR:
    80.79085064276

WORST_PRE_ALGORITHM4_MARGIN_TO_0P48Q:
    317.65025566818 bits.

OPTIONAL_5_TERM_MOORE_ROUTE:
    PARKED_POST_CORRECTNESS_OPTIMIZATION.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE:
    BLOCKED.

BASELINE_CORRECTNESS:
    PENDING.

NOVELTY_STATUS:
    PREFLIGHT.

PAPER_READINESS:
    NOT_READY.

## Next action

Do not modify or rerun:

    BOOT-T11-R8-SMALL-CANARY-20261103-R2.

When its result becomes available:
- independently audit the raw artifacts immediately;
- if PASS, Step 3 must use Turn-12's two-tier provenance contract;
- then complete baseline correctness before any benchmark.

If R2 remains pending, continue only independent paper-level BOOT side research.

No new heavy native task is authorized in this turn.
