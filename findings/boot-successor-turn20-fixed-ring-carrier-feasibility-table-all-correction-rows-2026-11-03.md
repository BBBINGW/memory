# BOOT / B158 — Turn 20 — fixed-ring carrier feasibility table across all published correction rows

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes read of the Turn-19 path was attempted first and remains degraded.
Turn-18 exact durable authority available through Git:
    findings/boot-successor-turn18-bounded-novelty-value-preflight-sparse-r8-one-multkey-2026-11-03.md
    commit a682237a745b93a38ab700a168657464c8e99407
    blob 73fda6fe35b2074e9072ba9dedc5c5f3e48fead7.

The current turn request supplies the already-persisted Turn-19 session state, including the fixed-ring module carrier theorem and p=3 prescout.
No connector-derived state is claimed to override the user-supplied local authority.

The target Turn-20 path was checked absent before write.
The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Primary source:
Aung et al., ePrint 2025/350 / PKC 2025,
cached mirror SHA256 922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82,
VERSION_UNVERIFIED.

Source experiment rows are taken from Table 5 for correction trace-and-merge at:
    p in {3,5,7,11,13}
    w in {128,256,512,1024}
where a correction RMFE exists.

## Primary hypothesis

H20:
Every published Aung correction/TnM RMFE row admits a fixed-ring carrier of the Turn-19 type inside the same outer power-of-two BGV ring, and the minimum feasible carrier also minimizes the structural recovery-automorphism count.

Falsifier:
- some published correction row has no q<=15 with carrier fixed-ring factor count equal to the outer physical-slot count and module rank at least k;
- the required carrier does not embed in the outer ring;
- or increasing q can reduce the total coefficient-clear plus Frobenius automorphism count.

## 1. General fixed-ring feasibility criterion

Outer plaintext ring:
    R=S[X]/Phi_32768(X),
    S=Z/(p^e).

Define:
    d_out = ord_32768(p),
    f_out = phi(32768)/d_out = 16384/d_out.

Thus f_out is the number of physical plaintext factors/slots.

For carrier order 2^q, q<=15, define:
    Y=X^(2^(15-q)),
    C_q=S[Y]/Phi_{2^q}(Y).

Let:
    d_q = ord_{2^q}(p),
    f_q = phi(2^q)/d_q = 2^(q-1)/d_q.

Then:
    C_q ≅ product_{t=1}^{f_q} GR(p^e,d_q)

and its p-Frobenius fixed ring is:
    B_q=C_q^sigma ≅ S^(f_q).

A published Method-1 output is one scalar S-value per physical outer slot.
Therefore C_q is an exact scalar-tuple carrier iff:
    f_q=f_out.

When this holds:
    rank_{B_q}(C_q)=d_q.

Hence k projection outputs fit iff:
    k<=d_q.

FEASIBILITY:
    f_q=f_out
    and
    k<=d_q.                                  (T20.1)

## 2. Recovery cost for a feasible carrier

When f_q=f_out:
    d_out/d_q = 2^(15-q).

The unnormalized trace from the outer slot extension to C_q therefore has:
    scale_clear = d_out/d_q =2^(15-q)

and can be evaluated recursively in:
    r_clear =15-q
nonidentity trace-doubling automorphism stages.

The trace-dual coordinate recovery over C_q/B_q needs:
    d_q
Frobenius images, of which:
    d_q-1
are nonidentity.

Thus structural recovery automorphism count is:
    A(q)
      =(15-q)+(d_q-1).                       (T20.2)

All e correction outputs can reuse that one Frobenius bank.

Public output arithmetic:
    N_const = e*d_q
    N_add   = e*(d_q-1).                     (T20.3)

The combined unnormalized scale is:
    scale_clear*d_q=d_out.                   (T20.4)

Therefore the final scalar-unit normalization is always:
    d_out^(-1) mod p^e,

independent of q.

## 3. Minimum feasible q is structural-cost optimal

For the source primes after the factor-count f_q has stabilized to f_out, increasing q by one doubles d_q:
    d_{q+1}=2d_q.

Then:
    A(q+1)-A(q)
      =[(14-q)+(2d_q-1)]-[(15-q)+(d_q-1)]
      =d_q-1.

Every nontrivial published correction row has minimum feasible d_q>=2.
Therefore:
    A(q+1)>A(q).

So the smallest q satisfying (T20.1) also minimizes the recovery automorphism count among all larger same-factor-count carriers.

There is no hidden benefit from choosing an oversized carrier merely to reduce RM-clear depth.

## 4. Outer slot counts

Exact orders at m=32768:

    p=3:
      d_out=8192
      f_out=2

    p=5:
      d_out=8192
      f_out=2

    p=7:
      d_out=4096
      f_out=4

    p=11:
      d_out=8192
      f_out=2

    p=13:
      d_out=8192
      f_out=2.

Thus p=7 is the only published correction prime in Table 5 with four physical factors.
The fixed-ring theorem handles it without changing the conceptual construction:
    B_q ≅ S^4.

## 5. Exact feasibility/cost table

Columns:
- q: minimum carrier order exponent, carrier cyclotomic order=2^q;
- d_q: module rank / number of shared Frobenius images;
- clear: RM-clear trace stages=15-q;
- Frob: nonidentity Frobenius images=d_q-1;
- A: total recovery automorphism stages=clear+Frob;
- const/add: public arithmetic for all correction outputs L_0,...,L_{e-1};
- save: split MultKeys eliminated, k-1.

### p=3, e=5, f_out=2, d_out=8192, normalization=59 mod243

    w=128,  k=2:
      q=3, d_q=2,  clear=12, Frob=1,  A=13
      const/add=10/5
      save=1

    w=256,  k=4:
      q=4, d_q=4,  clear=11, Frob=3,  A=14
      const/add=20/15
      save=3

    w=512,  k=7:
      q=5, d_q=8,  clear=10, Frob=7,  A=17
      const/add=40/35
      save=6

    w=1024, k=13:
      q=6, d_q=16, clear=9,  Frob=15, A=24
      const/add=80/75
      save=12.

### p=5, e=4, f_out=2, d_out=8192, normalization=28 mod625

    w=128,  k=2:
      q=3, d_q=2,  clear=12, Frob=1,  A=13
      const/add=8/4
      save=1

    w=256,  k=3:
      q=4, d_q=4,  clear=11, Frob=3,  A=14
      const/add=16/12
      save=2

    w=512,  k=5:
      q=5, d_q=8,  clear=10, Frob=7,  A=17
      const/add=32/28
      save=4

    w=1024, k=9:
      q=6, d_q=16, clear=9,  Frob=15, A=24
      const/add=64/60
      save=8.

### p=7, e=4, f_out=4, d_out=4096, normalization=806 mod2401

    w=128,  k=3:
      q=5, d_q=4,  clear=10, Frob=3,  A=13
      const/add=16/12
      save=2

    w=256,  k=6:
      q=6, d_q=8,  clear=9,  Frob=7,  A=16
      const/add=32/28
      save=5

    w=512,  k=11:
      q=7, d_q=16, clear=8,  Frob=15, A=23
      const/add=64/60
      save=10

    w=1024, k=21:
      q=8, d_q=32, clear=7,  Frob=31, A=38
      const/add=128/124
      save=20.

### p=11, e=3, f_out=2, d_out=8192, normalization=84 mod1331

    w=128,  k=2:
      q=3, d_q=2,  clear=12, Frob=1,  A=13
      const/add=6/3
      save=1

    w=256,  k=3:
      q=4, d_q=4,  clear=11, Frob=3,  A=14
      const/add=12/9
      save=2

    w=512,  k=5:
      q=5, d_q=8,  clear=10, Frob=7,  A=17
      const/add=24/21
      save=4

    w=1024, k=9:
      q=6, d_q=16, clear=9,  Frob=15, A=24
      const/add=48/45
      save=8.

### p=13, e=3, f_out=2, d_out=8192, normalization=2009 mod2197

Aung Table 5 marks correction w=128 as DNE, so there is no source RMFE row to accelerate.

    w=256,  k=2:
      q=3, d_q=2,  clear=12, Frob=1,  A=13
      const/add=6/3
      save=1

    w=512,  k=4:
      q=4, d_q=4,  clear=11, Frob=3,  A=14
      const/add=12/9
      save=3

    w=1024, k=7:
      q=5, d_q=8,  clear=10, Frob=7,  A=17
      const/add=24/21
      save=6.

Result:
    ALL 19 published non-DNE correction/TnM rows satisfy (T20.1).

Largest required carrier:
    p=7,w=1024:
      q=8
      phi(2^q)=128
      d_q=32.

Even this carrier has degree128 versus outer degree16384.

## 6. Normalization constants and metadata factors

Because combined scale is always d_out:

p=3,e=5:
    scale=8192 ≡173 mod243
    normalization=59
    post-normalization intFactor=173.

p=5,e=4:
    scale=8192 ≡67 mod625
    normalization=28
    post-normalization intFactor=67.

p=7,e=4:
    scale=4096 ≡1695 mod2401
    normalization=806
    post-normalization intFactor=1695.

p=11,e=3:
    scale=8192 ≡206 mod1331
    normalization=84
    post-normalization intFactor=206.

p=13,e=3:
    scale=8192 ≡1601 mod2197
    normalization=2009
    post-normalization intFactor=1601.

All are p-adic units.

## 7. Structural leverage table

Define a NONPERFORMANCE prescout index:

    leverage = (k-1)/A(q),

i.e. eliminated split MultKeys per recovery automorphism stage.

This does not equate one MultKey with one automorphism.
It is only useful to rank generalization rows before expensive work.

Selected values:

    p=5,w=512:
      4/17  =0.235

    p=3,w=512:
      6/17  =0.353

    p=5,w=1024:
      8/24  =0.333

    p=3,w=1024:
      12/24 =0.500

    p=7,w=512:
      10/23 =0.435

    p=7,w=1024:
      20/38 =0.526

    p=13,w=1024:
      6/17  =0.353.

Structurally, the largest-k rows improve branch-elimination leverage rather than suffering a proportional recovery-automorphism explosion.

This is consistent with the fixed-ring theorem:
doubling carrier rank doubles Frobenius bank width but can admit nearly twice as many component branches while RM-clear depth decreases by one.

## 8. Source-derived throughput-crossing gates

For each published correction/TnM row, Aung reports total latency T, post capacity C, and throughput ratio rho against thin.

For a same-k candidate with post capacity C_fast:
    rho_fast
      =rho*(C_fast/C)*(T/T_fast).

Thus candidate throughput exceeds the published thin baseline iff:
    T_fast < rho*T*(C_fast/C).              (T20.5)

At unchanged capacity C_fast=C, selected exact thresholds are:

### w=512

    p=3,k=7:
      T=14.9, rho=.764
      T_fast <11.3836 s
      required reduction >3.5164 s.

    p=5,k=5:
      T=11.3, rho=.832
      T_fast <9.4016 s
      required reduction >1.8984 s.

    p=7,k=11:
      T=18.4, rho=.844
      T_fast <15.5296 s
      required reduction >2.8704 s.

    p=11,k=5:
      T=11.1, rho=.773
      T_fast <8.5803 s
      required reduction >2.5197 s.

    p=13,k=4:
      T=9.29, rho=.710
      T_fast <6.5959 s
      required reduction >2.6941 s.

### w=1024

    p=3,k=13:
      T=30.5, rho=.657
      T_fast <20.0385 s
      required reduction >10.4615 s.

    p=5,k=9:
      T=21.2, rho=.778
      T_fast <16.4936 s
      required reduction >4.7064 s.

    p=7,k=21:
      T=36.2, rho=.794
      T_fast <28.7428 s
      required reduction >7.4572 s.

    p=11,k=9:
      T=20.3, rho=.718
      T_fast <14.5754 s
      required reduction >5.7246 s.

    p=13,k=7:
      T=16.0, rho=.691
      T_fast <11.0560 s
      required reduction >4.9440 s.

These are preregistered source-supported value gates, not performance predictions.

## 9. Generalization ranking

No new active candidate is created.

If active p=5 survives native evidence and value gates, the highest-value generalization sequence should NOT simply follow increasing prime.

Two especially informative rows are:

1. p=3,w=1024,k=13
   - same f_out=2 family as active p=5;
   - carrier q=6;
   - 24 recovery automorphism stages;
   - eliminates 12 split MultKeys;
   - five correction outputs;
   - large total-latency gap to thin.

2. p=7,w=1024,k=21
   - tests the genuinely new f_out=4 fixed-ring case;
   - carrier q=8;
   - 38 recovery automorphism stages;
   - eliminates 20 split MultKeys;
   - strongest structural leverage index.

For a first low-risk generalization, p=3,w=512 remains attractive:
same q=5/d_q=8/RM10+7-Frobenius geometry as active p=5, differing mainly in fixed-ring representation, modulus and one extra correction output.

## 10. Paper contribution implication

Turn 20 strengthens the paper framing.

The representation mechanism is not:
    "one clever sparse layout for p=5."

It is:
    "a fixed-ring module carrier principle for delaying RMFE component separation across the expensive coefficient-domain MultKey."

The active p=5 sparse ten-coordinate layout is the easiest concrete instance.
p=3 demonstrates a nontrivial module-sparse instance.
p=7 shows the theorem also handles more than two physical factors.

If native/value evidence eventually supports more than one row, the contribution can be presented as a parameterized algorithmic family rather than a one-parameter implementation trick.

This does NOT change NOVELTY_STATUS from PREFLIGHT.

## 11. Scientific boundaries

Turn 20 proves algebraic FEASIBILITY only for the carrier/recovery interface.

It does NOT prove, for rows other than active p=5:
- rawModSwitch capacity;
- exact D_{r,j} coefficient/canonical norms;
- complete Algorithm-4 correctness;
- DFR;
- matched latency;
- security;
- artifact implementation.

Do not transfer p=5 noise results across rows.

## Verdict

PASS_ALL_PUBLISHED_CORRECTION_ROWS_FIXED_RING_FEASIBLE.
PASS_MINIMUM_FEASIBLE_CARRIER_IS_AUTOMORPHISM_OPTIMAL.
PASS_COMBINED_SCALE_EQUALS_OUTER_SLOT_DEGREE.
PASS_P7_FOUR_PHYSICAL_FACTOR_GENERALIZATION.
PASS_GENERALIZATION_VALUE_GATE_TABLE.

ACTIVE_CANDIDATE remains:
    p=5,w=512,k=5 only.

GENERALIZATION_PRESCOUT:
    p=3,w=512 first low-risk;
    p=3,w=1024 and p=7,w=1024 high-value later rows.

NATIVE_STEP2_RESULT=UNKNOWN / PENDING.
CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
NOVELTY_STATUS=PREFLIGHT.
PAPER_READINESS=NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise the next side turn should perform a paper-level VALUE_REVIEW rather than another algebraic generalization:
decide whether the active p=5 instance remains a credible paper anchor given its approximately1.5x published-row ceiling, now that a parameterized family with higher-k rows is mathematically available.

No native generalization.
No benchmark.
