# BOOT / B158 — Turn 19 — fixed-ring module carrier theorem and p=3 value prescout

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes read of Turn 18 was attempted first and remained degraded.
Exact Turn-18 durable finding:
    findings/boot-successor-turn18-bounded-novelty-value-preflight-sparse-r8-one-multkey-2026-11-03.md
    commit a682237a745b93a38ab700a168657464c8e99407
    blob 73fda6fe35b2074e9072ba9dedc5c5f3e48fead7.

The target Turn-19 path was checked absent before write.
The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Primary source:
Aung et al., ePrint 2025/350 / PKC 2025, cached mirror
SHA256 922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
VERSION_UNVERIFIED.

## Primary hypothesis

H19:
The current p=5,k=5 sparse-R8 construction is not an isolated parameter accident.
It is a special case of a fixed-ring module carrier theorem:

For a power-of-two carrier C embedded in the outer BGV plaintext ring, if the carrier Frobenius fixed ring equals the ring of scalar tuples over the physical slots and the carrier has module rank at least k over that fixed ring, then k Method-1 outputs can be merged before ONE MultKey and recovered afterward by trace-dual coefficient functionals from one dirty reconstruction.

Falsifier:
- p=3,k=7 requires a larger or qualitatively different carrier;
- the two physical scalar-slot values do not lie in the Frobenius fixed ring;
- the carrier is not free of sufficient rank over the fixed ring;
- trace-dual recovery cannot preserve arbitrary higher-p-adic scalar lifts;
- or p=3 requires an additional MultKey / new automorphism family.

## 1. Aung p=3 correction parameters

Aung Table 5 for m=32768,w=512 gives:

    p=3
    e=5
    Corr./TnM
    k=7
    before/after capacity 392/136
    latency 14.9 s
    throughput ratio vs thin 0.764.

Thin bootstrap on the same row:

    capacity 392/179
    latency 2.14 s
    throughput ratio 1.

Correction style requires:

    eta = p^(e-1) = 3^4 =81.

For w=512, Aung Corollary 1 gives:

    k <= min(p^s+1, floor((w-1)/eta)+1)
      = min(3^s+1,7).

s=1 allows only k<=4.
s=2 allows k<=7.

Hence the published k=7 correction point necessarily uses at least:

    G = GR(3^5,2),

and sw=1024 divides d=8192 as required.

The input payload remains restricted by Aung to:

    (Z_243)^7 subset G^7.

## 2. Outer physical-slot structure

Let:

    S=Z/243Z
    m=32768
    R=S[X]/(X^16384+1).

Exact number theory:

    ord_32768(3)=8192.

Therefore R decomposes into:

    16384/8192 =2

physical plaintext slots, each an unramified degree-8192 Galois-ring component.

This matches the two-slot structure used by the current p=5 candidate.

## 3. Use the SAME degree-16 carrier as p=5

Set:

    Y=X^1024.

Then Y has order32 and define:

    C = S[Y]/(Y^16+1)
      = S[Y]/Phi_32(Y).

For p=3:

    ord_32(3)=8.

Hence Phi_32 splits over S into exactly:

    phi(32)/8 =16/8 =2

unramified degree-8 factors.

Thus:

    C ≅ GR(243,8) x GR(243,8).

Let sigma be the p-Frobenius:

    sigma(Y)=Y^3.

Within each degree-8 factor, sigma has order8.

Therefore its fixed ring is:

    B = C^{<sigma>}
      ≅ S x S.

This B is exactly the ring of independently chosen scalar values in the two physical slots.

This observation is the key generalization.

## 4. Method-1 outputs lie in B

For each RMFE component i, Aung Method 1 returns in every physical slot the projected integer:

    a_{i,+}, a_{i,-} in S.

Therefore the plaintext of the i-th thin projection ciphertext is exactly one element:

    h_i in B ≅ S x S,

whose two components are:

    (a_{i,+},a_{i,-}).

No extra slot-to-coefficient conversion is needed to regard h_i as a carrier coefficient over B.

This is true even though, in the ordinary S-coefficient basis of C, h_i may occupy several monomials.

## 5. C is rank 8 over B

Since each factor of C is degree8 over S and B supplies one scalar S coordinate per factor:

    rank_B(C)=8.

Moreover:

    {1,Y,...,Y^7}

is a B-basis:
within each degree-8 factor, Y has minimal polynomial degree8, and B contains the factor idempotents.

Therefore any:

    k <=8

Method-1 outputs h_0,...,h_{k-1} in B can be encoded injectively as:

    A = sum_{i=0}^{k-1} Y^i h_i.

For the Aung p=3,w=512 correction point:

    k=7 <=8.

Thus the SAME carrier used by the current p=5 construction has enough module rank.

No degree-32 carrier is required.

## 6. Concrete S-coordinate witness

The abstract B-module statement can be checked explicitly.

Let:

    U=Y^4=X^4096.

Then U has order8 and:

    U^4+1
      =(U^2+22U-1)(U^2-22U-1) mod243.

Both quadratic factors reduce modulo3 to irreducible quadratics.

Exact CRT idempotents are:

    e_+ =122 +127U +127U^3
    e_- =122 +116U +116U^3

mod243, satisfying:

    e_+^2=e_+
    e_-^2=e_-
    e_+e_-=0
    e_+ + e_-=1.

They project to (1,0) and (0,1) across the two physical factors.

Thus a scalar pair (a_+,a_-) is represented as:

    h=a_+e_+ +a_-e_-
     =c + d(U+U^3),

with:

    c=122(a_+ +a_-)
    d=127a_+ +116a_-.

The map is invertible because its determinant is:

    116 mod243,

a unit, with exact inverse:

    a_+ = c -22d
    a_- = c +22d
    mod243.

So B really is the scalar-pair ring.

## 7. Seven-branch merge is injective despite coefficient overlap

For k=7 use:

    A=sum_{i=0}^6 Y^i(c_i+d_i(Y^4+Y^12)).

In the ordinary S-coefficient basis z_0,...,z_15:

    z0 =c0-d4
    z1 =c1-d5
    z2 =c2-d6
    z3 =c3
    z4 =c4+d0
    z5 =c5+d1
    z6 =c6+d2
    z7 =d3
    z8 =d4
    z9 =d5
    z10=d6
    z11=0
    z12=d0
    z13=d1
    z14=d2
    z15=d3.

Exact left inverse:

    d0=z12
    d1=z13
    d2=z14
    d3=z7
    d4=z8
    d5=z9
    d6=z10

    c0=z0+z8
    c1=z1+z9
    c2=z2+z10
    c3=z3
    c4=z4-z12
    c5=z5-z13
    c6=z6-z14.

Therefore the 14 scalar degrees of freedom are embedded injectively in the 16-coordinate carrier.

The ordinary S-coordinate support can be as large as 15/16 positions.
So for p=3 this is better described as a:

    B-module sparse carrier

rather than an ordinary sparse S-coefficient carrier.

This distinction matters for paper framing.

## 8. One MultKey and RM10 remain unchanged

The outer-to-carrier coefficient clearing is the SAME as p=5 because the carrier is still Phi_32 with:

    Y=X^1024.

Use the same ten-stage coefficient clearing:

    RM10.

Its automorphism targets remain:

    {16385,8193,4097,2049,1025,513,257,129,65,33}.

It retains exponents divisible by1024 and contributes common scale:

    1024.

After ONE ordinary coefficient-domain MultKey/reconstruction and RM10, obtain a dirty carrier:

    Z in C

such that:

    Z ≡ A mod3.

All higher 3-adic coordinates may be arbitrary.

## 9. Perfect trace pairing recovers arbitrary scalar lifts

The extension:

    C/B

is a product of unramified degree-8 Galois extensions.

Its trace pairing is perfect.

Therefore there exists a B-trace-dual basis:

    beta_0,...,beta_7 in C

such that:

    Tr_{C/B}(beta_i Y^j)=delta_ij.

Equivalently use unnormalized duals:

    	ilde beta_i =8 beta_i

so:

    Tr(	ilde beta_i Y^j)=8 delta_ij.

Define:

    lambda_i(Z)
      =Tr(	ilde beta_i Z).

For an exact codeword A:

    lambda_i(A)=8 h_i.

For dirty Z congruent A mod3:

    8^{-1}lambda_i(Z)
      =h_i' in B

and:

    h_i' ≡ h_i mod3.

Since:

    B ≅ S x S,

each h_i' corresponds to a UNIQUE pair:

    (a'_{i,+},a'_{i,-}) in S^2,

with:

    a'_{i,+} ≡ a_{i,+} mod3
    a'_{i,-} ≡ a_{i,-} mod3.

Thus the one MultKey produces one common arbitrary Z243 lift vector in each physical slot, exactly the domain required by Aung Algorithm 4.

No canonical high digits are required.

## 10. Five correction outputs from one shared Frobenius bank

For p=3,e=5, Algorithm 4 requires:

    L_0,...,L_4.

For each r=0,...,4 define public basis constants:

    Phi_{i,r}
      = phi(e_i)^(3^r).

Set:

    G_r(Z)
      = sum_{i=0}^6 Phi_{i,r} lambda_i(Z).

Expand trace:

    lambda_i(Z)
      = sum_{j=0}^7 sigma^j(	ilde beta_i) sigma^j(Z),

hence:

    G_r(Z)
      = sum_{j=0}^7 D_{r,j} sigma^j(Z)

with:

    D_{r,j}
      = sum_i Phi_{i,r} sigma^j(	ilde beta_i).

Therefore all five correction outputs share exactly:

    one bank {sigma^j(Z)}_{j=0}^7

and require only:

    7 nonidentity Frobenius automorphisms/key switches.

This is the same Frobenius-bank width as the p=5,k=5 candidate.

The p=3 generalization changes only the public D_{r,j} tables and adds one additional correction output.

## 11. Common normalization scale

RM10 contributes scale:

    1024.

The unnormalized trace-dual maps contribute scale:

    8.

Therefore every G_r output carries the common scale:

    1024*8=8192.

Modulo243:

    8192 ≡173.

Exact inverse:

    8192^{-1} mod243 =59.

So apply:

    multByConstant(59L)

to every correction output.

Pinned BGV scalar-unit semantics then update metadata intFactor by:

    59^{-1} mod243 =173.

Thus the p=3 analogue of p=5's scalar-unit28/factor67 pair is:

    scalar normalization =59
    resulting intFactor =173.

Both are 3-adic units.

## 12. Fixed-ring module carrier theorem

The p=3 derivation exposes the general structure.

Let:
- outer m=2^15;
- S=Z/(p^e);
- d=ord_m(p);
- f=phi(m)/d = number of physical slots.

Choose carrier cyclotomic order 2^q and:

    Y=X^(m/2^q).

Let:

    C_q=S[Y]/Phi_{2^q}(Y)
    d_q=ord_{2^q}(p)
    f_q=phi(2^q)/d_q.

If:

    f_q=f
and
    k<=d_q,

then:

1. the Frobenius fixed ring:
       B_q=C_q^sigma ≅ S^f
   exactly represents arbitrary scalar physical-slot tuples;

2. C_q is free rank d_q over B_q;

3. Method-1 outputs h_i in B_q can be packed as:
       A=sum_{i=0}^{k-1} Y^i h_i;

4. coefficient clearing from the outer ring to C_q followed by one MultKey/reconstruction yields a dirty carrier Z congruent A mod p;

5. perfect trace-dual functionals recover arbitrary scalar p^e-lifts h_i' in B_q;

6. all Aung correction maps can be fused into one shared d_q-Frobenius bank.

The unnormalized coefficient-clear scale is:

    2^(15-q),

and the trace-dual scale is:

    d_q.

Because f_q=f:

    2^(15-q) * d_q
      = phi(m)/f
      = d.

Thus the combined normalization scale is ALWAYS:

    ord_m(p),

independent of the chosen carrier q.

This explains the p=5 value 8192 and p=3 value 8192 as one theorem.

## 13. p=3,w=512 structural cost versus p=5,w=512

Both p=3 and p=5 use:

    q=5
    carrier Phi_32
    RM10
    d_q=8
    7 nonidentity Frobenius images.

Thus recovery automorphism count is identical:

    10 RM stages +7 Frobenius
      =17.

Correction output arithmetic:

p=5,e=4:
    4 outputs
    32 public constant multiplications
    28 additions.

p=3,e=5:
    5 outputs
    40 public constant multiplications
    35 additions.

So p=3 adds:
    +0 recovery automorphisms/key switches
    +8 public multiplications
    +7 additions
    +1 output cleanup/normalization.

At the same time the direct baseline eliminates:

p=5:
    5 ->1 MultKeys
    saves4 split executions.

p=3:
    7 ->1 MultKeys
    saves6 split executions.

Therefore p=3 eliminates 50% more split MultKey executions while keeping the expensive recovery-automorphism count unchanged.

This is STRUCTURAL value evidence only, not runtime evidence.

## 14. p=3 throughput preregistration

Aung p=3,w=512 Corr./TnM publishes:

    capacity C_base=136
    latency T_base=14.9 s
    throughput ratio rho_base=0.764.

The candidate preserves k=7 slot packing.

Therefore, for candidate post capacity C_fast and latency T_fast:

    rho_fast
      =0.764*(C_fast/136)*(14.9/T_fast).

Candidate throughput exceeds published thin bootstrapping only if:

    T_fast
      <0.764*14.9*(C_fast/136)

      =11.3836*(C_fast/136) seconds.

If:

    C_fast ≈136,

the candidate must reach:

    T_fast <11.3836 s.

That means at least:

    14.9-11.3836
      =3.5164 s

of latency reduction is required to cross the thin-throughput frontier at unchanged capacity.

## 15. Why no p=3 direct latency-overhead budget is claimed

Unlike p=5 Table 2, the inspected source does not provide a p=3 stage-by-stage MultKey latency breakdown.

Therefore Turn 19 does NOT infer:
- p=3 MultKey time;
- ideal p=3 one-MultKey latency;
- a numerical p=3 recovery-overhead budget.

Transferring the p=5 per-branch MultKey cost to p=3 would be an unsupported interface/performance assumption because e, plaintext modulus and runtime state differ.

The only preregistered p=3 value test is the directly source-supported total/throughput formula above.

## 16. Generalization boundary

This theorem shows that the p=5 sparse-R8 mechanism has a broader algebraic family.

However:
- p=3's ordinary S-coefficient carrier is nearly dense;
- its trace-dual constants are not the p=5 constants;
- exact D_{r,j} coefficient/noise envelopes are not yet derived;
- rawModSwitch/noise gates must be redone for p=3;
- Algorithm 4 has e=5 and ten divide boundaries rather than six;
- no p=3 native evidence exists.

Therefore p=3 is NOT promoted to an active or backup paper candidate in this turn.

It is a high-value GENERALIZATION PRESCOUT gated on the p=5 core mechanism surviving native evidence.

## Verdict

PASS_FIXED_RING_MODULE_CARRIER_THEOREM.
PASS_P3_K7_SAME_PHI32_CARRIER.
PASS_P3_ONE_MULTKEY_SAME_LIFT_RECOVERY_EXISTENCE.
PASS_P3_SHARED_EIGHT_FROBENIUS_BANK.
PASS_P3_COMMON_SCALE_8192_NORMALIZATION_59.
PASS_P3_STRUCTURAL_VALUE_PRESCOUT.

FAIL_P3_ORDINARY_S_COEFFICIENT_SPARSITY_AS_P5_STYLE.
P3_EXACT_NOISE_D_MAPS=NONDERVIED.
P3_NATIVE_EVIDENCE=NONE.
P3_VALUE_RUNTIME=UNKNOWN.

NATIVE_STEP2_RESULT=UNKNOWN / PENDING.
CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
NOVELTY_STATUS=PREFLIGHT.
PAPER_READINESS=NOT_READY.

## AI provisional choice

Keep p=5,k=5 as the only active candidate.

Record p=3,k=7 as a durable high-value generalization prescout:
if p=5 native Step 2 and later value gates pass, p=3 should be the first generalization benchmark because it eliminates six rather than four split MultKeys while retaining the same RM10+7-Frobenius recovery automorphism count.

Do not spend native resources on p=3 before the active p=5 evidence order permits it.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise the next side unit should remain cheap and paper-level.
Good options:
- derive the fixed-ring module carrier's exact feasibility table across Aung correction rows without native work;
- or perform a value review of whether the active p=5 contribution remains paper-worthy given the bounded 1.5x ceiling and newly discovered generalization family.

No benchmark.
