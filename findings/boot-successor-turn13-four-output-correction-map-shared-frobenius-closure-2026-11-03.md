# BOOT / B158 — Successor Research Turn 13 — four-output correction-map closure from one sparse-R8 recovery

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

GitHub Notes read of the Turn-12 predecessor was attempted first and remained degraded.
The exact durable predecessor was recovered through Git at:

    findings/boot-successor-turn12-aung-runtime-profile-reproducibility-boundary-2026-11-03.md
    commit 93ce8c686c087042e090455fa206de1947cfff4c
    blob 5bc99acc6270c50b89556f8d913d72faf442bedb.

The target Turn-13 path was checked absent before write.

The pending R2 task was not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Primary paper source:
- Aung et al., ePrint 2025/350, cached 30-page mirror SHA256
  922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
  source revision 87a21bbd5332f5faea99cad54d1a7499b553ddf8,
  VERSION_UNVERIFIED.

Official ePrint PDF text was also inspected through the web PDF backend.
Visual screenshot verification of the relevant PDF pages was attempted but the official PDF host returned HTTP 403.
No visual-layout-only claim is used.

## Why this turn is paper-level

The current canonical sparse-R8 construction after Turn 7 says:

    five Method-1 projections
    -> sparse R8 coefficient carrier
    -> ONE MultKey
    -> RM10
    -> one fused 8-Frobenius coefficient-to-RMFE recode
    -> scalar-unit28
    -> Aung correction DigitExtract.

Aung Algorithm 4, however, does NOT take only z=L0.
For e=4 it needs correction inputs:

    L0(z), L1(z), L2(z), L3(z),

where for z=phi(x_0,...,x_4):

    L_r(z) = sum_i x_i * phi(e_i)^(5^r),
    r=0,1,2,3.

The paper explicitly states:
- L0 is identity on im(phi);
- correction maps are prepared before DigitExtract;
- Algorithm 4 uses L_{j+1}(z) at each outer iteration.

Therefore a construction that produces only the Turn-7 G_0 output is not yet a complete interface to Algorithm 4.

This turn asks whether the missing L1,L2,L3 require restoring split MultKeys or an additional expensive RMFE recode family.

## Closest prior / exact delta

Aung's split-thin correction workflow already has k separately recovered scalar ciphertexts and forms the L_r outputs using public additions and constant multiplications.

The current candidate instead has ONE merged coefficient-domain MultKey followed by a sparse R8 coordinate state.

The exact candidate-specific question is:

Can the same sparse coordinate state produce all four Aung correction outputs with one shared Frobenius bank, preserving one common set of arbitrary Z625 lifts?

This turn adds no new hardness assumption and no novelty-clear claim.
NOVELTY_STATUS remains PREFLIGHT.

## Primary hypothesis

H13:
After the one merged reconstruction and RM10, all four Aung correction maps can be generated from the SAME R8 coordinate state by replacing the Turn-7 output constants phi_i with phi_i^(5^r), while sharing the same seven nonidentity R8 Frobenius images across r=0,1,2,3.

Falsifier:
- the Turn-7 G map reconstructs only L0 in a way that cannot be generalized to ordinary powers phi_i^(5^r);
- producing L1,L2,L3 requires additional MultKey executions;
- the four outputs necessarily use inconsistent high 5-adic lifts;
- a new family of automorphisms/key switches is needed for each output;
- or the exact public multiplier envelopes consume the available correctness margin.

## 1. Source Algorithm-4 requirement

Aung defines, for 0<=r<=e-1:

    L_r : im(phi) -> E

by:

    L_r(phi(x_0,...,x_4))
      = sum_i x_i * phi(e_i)^(p^r).

For the current p=5,e=4 setting:

    r in {0,1,2,3}
    exponents = {1,5,25,125}.

Algorithm 4 uses:

    u_0,0 = z
    y = L_{j+1}(z)

at the start of outer iterations j=0,1,2.

Thus the candidate must have exactly four mutually consistent inputs L0,L1,L2,L3 before DigitExtract.

## 2. One common sparse coordinate state

Use the current fixed rings:

    S = Z/625Z
    R8 = S[Y]/(Y^16+1)
    Y = X^1024.

After the ONE MultKey reconstruction and unnormalized RM10, the retained sparse plaintext can be written as:

    1024 * Z

with:

    Z = sum_{i=0}^4 Y^i a_i'

and:

    a_i' = z_i + z_{i+8} Y^8
         in S[Y^8]/(Y^16+1).

Each a_i' simultaneously represents the two physical-slot scalar lifts for branch i.

The important point is that ALL later outputs below use these exact same a_i'.

No independent reconstruction is performed per correction map.

## 3. The fixed-coordinate subring is Frobenius invariant

Let sigma be the R8 Frobenius:

    sigma(Y)=Y^5.

Since:

    sigma(Y^8)=Y^40
              =Y^8*(Y^16)^2
              =Y^8,

every a_i' is fixed by sigma.

The order-8 trace is:

    T8(W)=sum_{j=0}^7 sigma^j(W).

For the R8 basis over the fixed subring:

    T8(Y^t)=8Y^t  for t in {0,8}
    T8(Y^t)=0     otherwise.

Equivalently, for Z=sum_i Y^i a_i':

    T8(Y^{-i} Z)=8 a_i'.

This is exactly the coordinate selector already used by Turn 7.

## 4. Four fused correction-output maps

The frozen RMFE basis is:

    phi_i(X)=sum_{k=0}^4 ell_{i,k} X^(16k),

with:

    ell_0=[1,50,340,260,599]
    ell_1=[0,4,204,314,104]
    ell_2=[0,622,161,623,469]
    ell_3=[0,418,206,522,104]
    ell_4=[0,156,339,156,599].

For r=0,1,2,3 define ordinary plaintext-ring powers:

    C_{i,r} := phi_i^(5^r)
               mod (X^16384+1,625).

These are ORDINARY ring powers, matching Aung's correction-map definition.
They are not being replaced by a Frobenius automorphism.

Define:

    G_r(W)
      := sum_{i=0}^4 C_{i,r} * T8(Y^{-i} W).

Expand the trace:

    G_r(W)
      = sum_{j=0}^7 D_{r,j} * sigma^j(W),

where:

    D_{r,j}
      := sum_{i=0}^4 C_{i,r} * sigma^j(Y^{-i}).

The existing Turn-7 fused map is precisely:

    G_0.

Thus L1,L2,L3 require only new PUBLIC multiplier tables D_{r,j}, not a new ciphertext representation.

## 5. Exact semantic identity

Apply G_r to the RM10 plaintext 1024*Z:

    G_r(1024 Z)
      = 1024 * sum_i C_{i,r} * T8(Y^{-i}Z)
      = 8192 * sum_i a_i' * C_{i,r}.

The existing scalar-unit normalization is:

    8192^{-1} mod625 = 28.

Therefore after:

    multByConstant(28L)

the exact semantic plaintext is:

    L_r'
      = sum_i a_i' * phi_i^(5^r).

Let:

    z' = L_0'
       = sum_i a_i' phi_i.

Then:

    L_r' = L_r(z')

for the SAME coefficient vector:

    (a_0',...,a_4') in Z625^5

slotwise.

This same-lift property is stronger than merely requiring each output to be correct modulo5.
It is exactly what Aung's Algorithm-4 divisibility proof needs: one z' and its correction maps derived from the same a_i'.

Therefore arbitrary high 5-adic digits introduced by the one MultKey do not create cross-output inconsistency.

## 6. Exact basis proof

Independent full-ring arithmetic modulo:

    X^16384+1
    and 625

was recomputed for all:

    r=0,1,2,3
    t=0,...,15.

For each r:

    G_r(Y^t)=8*C_{t,r}             for 0<=t<=4
    G_r(Y^t)=8*C_{t-8,r}*Y^8       for 8<=t<=12
    G_r(Y^t)=0                      for t in {5,6,7,13,14,15}.

Result:

    64/64 exact basis identities PASS.

For r=0 the recomputation reproduces the durable Turn-7 map invariants:

    every D_{0,j} support =21
    Linf_balanced =311
    L1_balanced =2811.

This is an internal consistency check against the existing canonical G_0 construction.

## 7. Exact public D_{r,j} coefficient table

All values below use balanced coefficients modulo625.

### r=0, exponent1

For every j=0,...,7:

    support =21
    Linf =311
    L1 =2811.

Aggregate:

    A_0 := sum_j ||D_{0,j}||_1
         =22488.

Nonidentity aggregate:

    B_0 := sum_{j=1}^7 ||D_{0,j}||_1
         =19677.

### r=1, exponent5

For every j=0,...,7:

    support =84
    Linf =310
    L1 =13610.

Aggregate:

    A_1=108880
    B_1=95270.

### r=2, exponent25

Per-j rows (support,Linf,L1):

    j0 (315,310,52352)
    j1 (359,310,62345)
    j2 (380,310,65869)
    j3 (380,310,65869)
    j4 (315,310,52338)
    j5 (359,310,61249)
    j6 (380,310,65869)
    j7 (380,310,65869).

Aggregate:

    A_2=491760
    B_2=439408.

### r=3, exponent125

Per-j rows:

    j0 (540,300,90917)
    j1 (945,310,169586)
    j2 (873,300,157043)
    j3 (873,310,156207)
    j4 (555,305,96069)
    j5 (926,300,165114)
    j6 (862,300,154970)
    j7 (868,300,149116).

Aggregate:

    A_3=1139022
    B_3=1048105.

The worst individual public constant is:

    ||D_{3,1}||_1=169586.

The worst aggregate correction output is L3.

## 8. Canonical exact-map hashes

For reproducibility, this turn defines a NEW canonical serialization schema:

For each r:
- outer JSON array ordered by j=0,...,7;
- each D_{r,j} is an array of [exponent, balanced_coefficient] pairs;
- pairs sorted by exponent ascending;
- UTF-8 JSON with separators "," and ":" and no whitespace.

Under this schema:

    SHA256(r=0)
      a66cd85ac5d5eb51d01e43f9546287443888db93390b63e434754f61002fb77c

    SHA256(r=1)
      392591813d3a5283b2b12a14820963b28cebcf72e03d111416a0c15106aa6f8b

    SHA256(r=2)
      7d8bbe75654ef0b3815253b781dac16ddc366fea24a43f6bacbe1244fb7a4550

    SHA256(r=3)
      a5d4f55965a02b68922ecf9ec7d01a5255620fd4795e46153d9b839f1133c3ab

For the nested r=0..3 array under the same schema:

    SHA256(all 32 D_{r,j})
      4e000d49c67a8f17e26ae2220bcfcb76347d54ae2b95531398104dcbb9403568.

The r=0 hash differs from the earlier Turn-7 hash because the serialization schema is intentionally different.
The underlying r=0 support/Linf/L1/basis identities agree exactly.

## 9. Shared-Frobenius implementation contract

Starting from the CLEANED RM10 ciphertext R:

Compute only once:

    H_0 = R
    H_j = sigma^j(R), j=1,...,7.

This costs exactly:

    7 nonidentity Frobenius automorphisms/key switches.

Then for each r=0,1,2,3 form:

    C_r = sum_{j=0}^7 D_{r,j} H_j.

Each output requires:
- 8 public constant multiplications;
- 7 ciphertext additions;
- one final cleanUp;
- one scalar-unit28 metadata normalization.

Total four-output front end after RM10:

    Frobenius automorphisms/key switches: 7
    public constant multiplications:     32
    ciphertext additions:                28
    output cleanups:                      4
    scalar-unit28 normalizations:         4
    ciphertext-ciphertext multiplications:0.

Relative to the previous single-output G_0 specification, the correction-map closure adds:

    +0 Frobenius automorphisms/key switches
    +24 public constant multiplications
    +21 additions
    +3 cleanups
    +3 scalar-unit metadata normalizations.

The same H_j ciphertext objects are reused across outputs.
No additional MultKey is introduced.

## 10. Exact independent coefficient-L1 output envelopes

Reuse the Turn-7 cleaned RM10 envelope:

    E_RM10
      <=1,835,903,626,782,748,867.

Reuse the source-sized direct temporary-625 Frobenius key-switch envelope:

    K <=401,679,183,790,909.

Reuse the cleanup rounding envelope:

    R <=83,891,200,000.

For each r:

    E_{L_r}
      <= A_r * E_RM10
         + B_r * K
         + R.

The scalar-unit28 operation contributes no physical error multiplication.

Exact bounds:

### L0

    E_L0
      <=41,293,704,600,473,801,437,489
    log2(E_L0)
      <=75.128339940984.

With log2(Q)>=399.5, margin above the 0.48Q sufficient correctness boundary:

    >=323.312766369963 bits.

This exactly reproduces Turn 7.

### L1

    E_L1
      <=199,931,454,860,029,347,739,390
    log2(E_L1)
      <=77.403851648992.

Correctness margin:

    >=321.037254661954 bits.

### L2

    E_L2
      <=903,000,468,553,559,669,777,792
    log2(E_L2)
      <=79.579072918709.

Correctness margin:

    >=318.862033392238 bits.

### L3

    E_L3
      <=2,091,555,622,746,351,241,865,519
    log2(E_L3)
      <=80.790850642763.

Correctness margin:

    >=317.650255668184 bits.

Thus the four-output closure remains overwhelmingly inside the static coefficient-L1 correctness region.

For comparison only, Turn 7's crude optional stress check multiplied the already-built L0 envelope by the old legacy correction factor A3=653905 and obtained:

    log2 error <=94.4470614701.

Directly producing L3 from the sparse coordinate state gives:

    log2 error <=80.7908506428,

a 13.6562108274-bit tighter sufficient envelope.

This is a static correctness improvement, not a runtime performance claim.

## 11. Construction correction

The previous canonical phrase:

    RM10
    -> one fused 8-Frobenius recode G
    -> scalar-unit28
    -> Aung correction DigitExtract

was incomplete as an Algorithm-4 interface.

The corrected canonical construction is:

    five Method-1 projections
    -> sparse R8 merge
    -> ONE coefficient-domain MultKey
    -> ONE rawModSwitch/newMakeDivisible/reconstruction
    -> unnormalized RM10
    -> ONE shared bank {sigma^j(R)}_{j=0}^7
    -> four fused public outputs G_0,G_1,G_2,G_3
    -> scalar-unit28 on each
    -> Aung Algorithm 4 using exact L0,L1,L2,L3
    -> one FINAL source Recode at Algorithm-4 exit.

The single source Recode counted by Aung correction style remains at the end of Algorithm 4.
The four G_r maps are correction-input reconstruction maps, not four source Recode evaluations.

## 12. Why this closes the same-lift problem

A potentially fatal alternative would be:
- independently recover L0,L1,L2,L3 from separate rounded/raw branches;
- obtain different high 5-adic representatives a_i^(r);
- satisfy each map only modulo5 but violate Aung's exact relation
      L_r(z)=sum_i a_i phi_i^(5^r)
  for ONE common z.

The current four-output construction avoids this completely.

All four outputs are deterministic public linear maps of the SAME RM10 coordinate ciphertext.
Hence their high p-adic digits are linked by construction to one exact vector:

    (a_0',...,a_4').

This matches the quantification used by the durable dirty-lift Algorithm-4 proof.

## 13. Native evidence-order consequence

The pending Step-2 canary R2 tests the core one-output recovery chain and remains valid.
It is NOT modified or resubmitted.

A PASS of R2 is still required before Step 3.

After R2 PASS:
- Step 3 exact interface serialization proceeds under the Turn-12 two-tier provenance contract;
- complete candidate correctness must additionally instantiate and assert G_1,G_2,G_3 using the exact maps/hashes above;
- the four outputs must be checked against the SAME reconstruction plaintext coordinate oracle.

No benchmark is authorized before baseline correctness and complete candidate correctness.

## Verdict

FAIL_SINGLE_G0_SUFFICIENT_ALGORITHM4_INTERFACE.
PASS_FOUR_OUTPUT_CORRECTION_MAP_GENERALIZATION.
PASS_SAME_Z625_LIFTS_ACROSS_L0_L3.
PASS_SHARED_SEVEN_FROBENIUS_BANK.
PASS_64_OF_64_EXACT_BASIS_IDENTITIES.
PASS_FOUR_OUTPUT_STATIC_L1_MARGIN.

CORRECTED_FRONT_END:
    RM10
    -> shared 8-Frobenius bank
    -> G0,G1,G2,G3
    -> unit28 each
    -> Algorithm4.

EXTRA_NONIDENTITY_AUTOMORPHISMS_VS_G0_ONLY:
    0.

EXTRA_MULTKEYS:
    0.

WORST_STATIC_OUTPUT:
    L3.

L3_LOG2_ERROR_MAX:
    80.790850642763.

L3_CORRECTNESS_MARGIN:
    317.650255668184 bits.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE:
    BLOCKED.

BASELINE_CORRECTNESS:
    PENDING.

SECURITY_GATE:
    PENDING.

VALUE_GATE:
    PENDING.

AUDIT_GATE:
    PENDING.

NOVELTY_STATUS:
    PREFLIGHT.

PAPER_READINESS:
    NOT_READY.

## Next action while R2 is pending

Do not execute or resubmit another native task.

If BOOT-T11-R8-SMALL-CANARY-20261103-R2 becomes ready, its raw artifacts preempt the next free substantive turn for independent audit.

Otherwise the next side-research unit should remain independent of R2 and may investigate:
- the complete Algorithm-4 nonlinear noise/factor recurrence for the now-correct four-output entry; or
- a bounded novelty/value audit of this shared-Frobenius multi-output correction construction.

Do not benchmark.
