# BOOT / B158 — Research Turn 5/25 — exact coefficient-L1 shared-reconstruction noise guard

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / duplicate audit

GitHub Notes read remains degraded for existing files, so durable state was recovered from BBBINGW/memory at verified HEAD:

    2eead4f0183c884b2b874aba429722966c8b018a

Immediate predecessors:
- Turn3 explicit stock-estimator envelope fallback:
  findings/boot-RMFE-postdivide-turn3-shared-reconstruction-noisebound-explicit-envelope-gate-2026-11-02.md
- Turn4 path-transparency gate:
  findings/boot-RMFE-postdivide-turn4-noise-envelope-path-transparency-gate-2026-11-02.md

No prior BOOT finding established the exact coefficient-L1 guard below.
The target path was absent before write.

No native execution occurred.

## Closest implementation prior / exact delta

Closest prior implementation remains stock HElib recryption.

Stock reconstruction estimates a constant polynomial's canonical-embedding size through floating
embeddingLargestCoeff and then updates noiseBound.

Turn3 showed that branchwise stock estimates could be upward-summed and passed through the public
size arguments, but that fallback still inherited floating-estimator semantics.

This turn asks whether the fixed current parameters permit a deterministic exact-integer bound that
eliminates this candidate-specific floating dependency entirely.

No novelty claim is added.

## Primary hypothesis

For current parameters:

    p=5
    e=4
    ePrime=1
    q=5^4+1=626
    m=32768
    phi(m)=16384
    mvec=[32768]

every exact post-newMakeDivisible /5 branch component z0_i,z1_i has polynomial coefficients bounded
by 313 in absolute value.

Because mvec has length one, HElib's powerful and polynomial bases are identical.
Therefore an exact coefficient-L1 norm of each ZZX is a rigorous upper bound on every canonical
embedding magnitude.

The sum across five branches is small enough to be exactly representable in IEEE double, so the
shared reconstruction can use this exact integer L1 envelope directly through the public HElib
size arguments, with no floating embeddingLargestCoeff or nextafter accumulation required.

## Falsifier

FAIL if any of the following is false:
1. rawModSwitch(q=626) stores every powerful coefficient in [-313,313];
2. newMakeDivisible with p^{ePrime}=5 adds q*v with |v|<=2;
3. after exact /5, a powerful coefficient can exceed 313 in absolute value;
4. PowerfulDCRT with mvec=[32768] is nontrivial or can amplify coefficients on powerfulToZZX;
5. coefficient-L1 fails to upper-bound the canonical embedding;
6. the five-branch exact L1 totals can exceed the exact-integer range of double.

## Minimal decisive test

Audit only:
- pinned rawModSwitch coefficient reduction;
- pinned newMakeDivisible;
- pinned PowerfulDCRT trivial-basis branch;
then derive a hard numerical envelope for current fixed parameters.

## 1. Exact rawModSwitch range

Pinned Ctxt::rawModSwitch converts each ciphertext part to the powerful representation and scales it
to q.

Before storing each powerful coefficient x, it performs symmetric reduction mod q:

    if x > q/2 ... x -= q
    else if x < -q/2 ... x += q

with randomized tie handling for even q.

For:

    q = 626
    q/2 = 313

the stored coefficient therefore satisfies exactly:

    -313 <= x <= 313.                                  (1)

This bound is deterministic and independent of the incoming ciphertext magnitude once rawModSwitch
has successfully completed its own source checks.

## 2. newMakeDivisible and exact /5 preserve the same 313 bound

Pinned newMakeDivisible uses:

    p2e = p^{ePrime} = 5

and computes the balanced residue v needed to make x+qv divisible by 5.

Its source comment and implementation give:

    |v| <= p2e/2

and for odd p2e=5 the actual possibilities are:

    v in {-2,-1,0,1,2}.

Thus before division:

    z' = x + 626*v

and using (1):

    |z'| <= 313 + 2*626 = 1565.

The source then performs exact integer division:

    z = z'/5.

Hence:

    |z| <= 1565/5 = 313.                               (2)

This applies independently to both z0_i and z1_i for every branch i.

## 3. Current powerful-to-polynomial conversion is exactly identity

Pinned PowerfulDCRT constructor sets:

    triv = (mvec.length() == 1)

with source comment:

    "triv means poly and pwfl bases are identical".

For current:

    mvec=[32768]

we have triv=true.

Pinned conversions then execute:

    ZZXtoPowerful: VectorCopy(out, poly, phim)
    powerfulToZZX: conv(poly, powerful)

with no nontrivial basis transform.

Therefore bound (2) is also the exact ordinary ZZX coefficient bound:

    for all polynomial coefficients c_j of every post-divide z0_i,z1_i,
    |c_j| <= 313.                                      (3)

No conversion amplification exists for this fixed parameter set.

## 4. Exact coefficient-L1 canonical-embedding bound

For any canonical embedding corresponding to a primitive m-th root zeta, |zeta|=1.

For:

    f(X) = sum_{j=0}^{phi(m)-1} c_j X^j,

triangle inequality gives:

    |f(zeta)|
      <= sum_j |c_j|
      = ||f||_1.                                      (4)

Thus the exact integer coefficient-L1 norm is a rigorous upper bound on the L-infinity norm of the
canonical embedding.

This is stronger than the Turn3 dependency on HElib's floating embeddingLargestCoeff estimator.

Pinned Ctxt.h explicitly documents the explicit size parameter as a bound on canonical-embedding
L-infinity for addConstant; multByConstant uses the same size as the multiplicative noiseBound
factor and HElib matrix code itself supplies canonical-embedding size estimates there.

## 5. Hard current-instance numerical limits

Current:

    phi(32768)=16384.

From (3):

    ||z||_1
      <= 16384 * 313
      = 5,128,192                                     (5)

for every one of the ten post-divide polynomials
(z0_i,z1_i), i=1..5.

For each component family:

    S0_L1 = sum_i ||z0_i||_1
    S1_L1 = sum_i ||z1_i||_1.

Therefore:

    S0_L1 <= 25,640,960
    S1_L1 <= 25,640,960.                              (6)

All these are exact integers strictly below 2^25, hence far below 2^53.
Every integer in this range is exactly representable as IEEE binary64 double.

Consequences:
- no overflow;
- no infinity;
- no NaN from accumulation;
- no rounding loss in integer->double conversion;
- no nextafter is required.

A simple uint64_t accumulator is already vastly sufficient for these fixed parameters.

## 6. Canonical reconstruction guard

Canonical correctness implementation should now compute:

    l0_i = exact sum_j abs(coeff(z0_i,j))
    l1_i = exact sum_j abs(coeff(z1_i,j))

using integer arithmetic.

Then:

    S0 = sum_i l0_i
    S1 = sum_i l1_i

and assert:

    S0 <= 25,640,960
    S1 <= 25,640,960.

Execute the single reconstruction:

    ctxt = recryptEkey;
    ctxt.multByConstant(Z1, double(S1));
    ctxt.addConstant(Z0, double(S0));

where:

    Z1=sum_i z1_i
    Z0=sum_i z0_i.

Because:

    ||Z1||_embed
      <= sum_i ||z1_i||_embed
      <= sum_i ||z1_i||_1
      = S1,

and similarly for Z0, the supplied explicit sizes are true deterministic bounds for the actual
shared constants.

## 7. Exact shared-vs-separate conservative envelope parity

Define a hypothetical separate reconstruction using the SAME rigorous L1 sizes.

For branch i:

    N_i^L1
      = N_E * l1_i
        + |f_E| * l0_i.

Summing the five separate conservative envelopes:

    N_sep^L1
      = N_E * S1 + |f_E| * S0.

The one shared guarded reconstruction receives exactly the same metadata formula:

    N_shared^L1
      = N_E * S1 + |f_E| * S0
      = N_sep^L1.                                    (7)

Thus exact parity is obtained without:
- five reconstructed ciphertexts;
- floating canonical-norm estimates;
- floating upward accumulation;
- private noiseBound mutation.

The exact ciphertext identity remains unchanged:

    R_shared = E*Z1+Z0 = sum_i R_i.

## 8. Supersession / relation to Turn3

Turn3's stock-estimator-sum fallback remains a valid optional diagnostic/comparator construction,
but it is no longer the canonical correctness guard.

Canonical guard is now:

    exact coefficient-L1 sizes -> exact integer five-branch sums -> explicit HElib size arguments.

This eliminates the candidate-specific uncertainty noted in Turn3 that HElib's floating
embeddingLargestCoeff implementation itself is only a software estimator.

Step3 may still record stock embeddingLargestCoeff values for comparison, but correctness acceptance
should use the exact-L1 ledger.

Turn4 path-transparency applies unchanged because it depends only on supplying a conservative
explicit size value, not on how that value was obtained.

## 9. Scope boundary

This turn does NOT prove:
- final capacity is positive;
- the L1 guard is tight enough for practical performance;
- native recovery correctness;
- Algorithm4 native noise trajectory;
- DFR;
- matched benchmark value.

The exact-L1 guard can be much more conservative than the true canonical norm.
If it drives native capacity below a required correctness margin, that is useful evidence that this
safe guard is too pessimistic or that the current parameter budget is insufficient.

The important correctness result is that there is no floating overflow/NaN or estimator-validity
dependency at the shared reconstruction boundary for the fixed candidate.

## Verdict

PASS_POSTDIVIDE_COEFFICIENT_BOUND_313
PASS_TRIV_POWERFUL_POLY_BASIS_IDENTITY
PASS_EXACT_L1_CANONICAL_EMBEDDING_GUARD
PASS_EXACT_DOUBLE_REPRESENTABILITY
PASS_EXACT_L1_SHARED_SEPARATE_ENVELOPE_PARITY

REFINE_CANONICAL_SHARED_RECONSTRUCTION_GUARD_TO_EXACT_COEFFICIENT_L1
SUPERSEDE_NEXTAFTER_STOCK_ESTIMATOR_SUM_AS_CANONICAL_CORRECTNESS_GUARD

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Step3 instrumentation refinement

After Step2 PASS, exact-interface verification should:
1. for each exact post-divide z0_i,z1_i assert every ZZX coefficient |c|<=313;
2. compute exact integer l0_i,l1_i;
3. assert each <=5,128,192;
4. compute exact S0,S1 and assert each <=25,640,960;
5. reconstruct once with explicit double(S1),double(S0);
6. verify shared noiseBound against equation (7);
7. optionally record stock embeddingLargestCoeff values diagnostically, but do not use them as the
   correctness oracle;
8. continue with Turn4 prime-set/path assertions and the previously preregistered exact-interface
   checks.

## Next decisive test

Evidence order remains blocked at Step2:
execute the frozen revised recovery-only canary against the pinned HElib commit with HELIB_DEBUG=ON.

No timing or performance conclusion is authorized before correctness prerequisites pass.
