# BOOT / B158_OVERALL — Research Turn 16/25
## Exact q1-rescale carry / whole-output oracle for the single-limb sparse gateway

Date: 2026-11-12 (Asia/Singapore)
Candidate: boot-b158-single-limb-sparse-gateway-composite-v1
Phase: CORRECTNESS_GATE
Status entering turn: ACTIVE
Evidence grade: MATH + exact-source STATIC; native candidate execution remains PENDING.

## Execution-channel note

The pre-registered Turn-14/15 next test was an exact-PR-#1381 candidate-native canary. The current runtime has no mounted OpenFHE source/binary. GitHub's public source and CI are readable, but the connected GitHub App rejected both temporary-ref creation and temporary Actions-workflow creation with HTTP 403 "Resource not accessible by integration". No native candidate task was launched or restarted, and no native result is inferred.

Rather than consume the turn on infrastructure, this turn advances an independent correctness gate for the SAME active candidate: exact whole-period/carry semantics of the physical q1 rescale followed by public q1 restoration. This gate is decision-changing: failure would PARK the gateway independently of any implementation.

## Pre-registration

QUESTION:
When the degree-2 ciphertext components c0,c1 modulo B=q0*q1 are independently CKKS-rescaled by physically dropping q1 before the sparse switch, do the centered-residue choices and later multiplication by the dense secret create an uncancelled carry/alias that changes the restored whole-output semantics modulo B? What exact rounding term must be charged to the candidate noise budget?

CURRENT_BELIEF:
Because OpenFHE's DropLastElementAndScale computes the exact quotient after subtracting each component's centered q1 representative, the componentwise carries should combine into exact multiples of B after public q1 restoration. However, a nonzero standard rescale-rounding polynomial involving the dense secret should remain and has not yet been included in the candidate's epsilon budget.

CHEAPEST_DECISIVE_TEST:
1. Read the exact PR #1381 source implementation inherited from DCRTPolyImpl::DropLastElementAndScale.
2. Derive the decryption identity over R=Z[X]/(X^N+1).
3. Exhaustively verify a scalar finite analogue and deterministically stress a small negacyclic polynomial analogue, including cases with nonzero B-alias carries.

IF_PASS:
Retain candidate ACTIVE. Mark the whole-period/carry ambiguity resolved, but add the newly derived pre-gateway rescale rounding term epsilon_pre to the mandatory candidate-native instrumentation and precision/DFR budget.

IF_FAIL:
PARK the candidate. An uncancelled B-period carry introduced before the sparse switch would invalidate the core claim that the logical B=q0*q1 semantics survive the q0 gateway.

IF_UNCLEAR:
Keep CORRECTNESS_GATE=PENDING and do not run the full FBT canary until the source rounding convention or representative identity is resolved exactly.

WHICH_PAPER_GATE_CHANGES:
Exact semantic/correctness killer gate (1), specifically carry and whole-output semantics; also NOISE_PRECISION_DFR bookkeeping.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
If carry aliases survive, no amount of switch-noise tuning can repair the construction. If they cancel exactly, native work is justified, but its precision oracle must include the exact rescale-rounding term derived here.

## Exact source semantics

Exact PR #1381 head:
  f389e3c8b07955cbc49c9814053fa8eed1b07cc7

Inherited source:
  src/core/include/lattice/hal/default/dcrtpoly-impl.h
  DCRTPolyImpl<VecType>::DropLastElementAndScale

The source comment states that CKKS rescaling computes
  round(x/q_l) = (x - [x]_{q_l}) * [q_l^{-1}]_{q_i},
where [x]_{q_l} is the centered representative, and that the subtraction makes x-[x]_{q_l} exactly divisible by q_l. The implementation performs this coefficientwise on each DCRT polynomial component.

For the candidate q_l=q1 and only q0 remains.

## Ring derivation

Work coefficientwise in the integer polynomial ring R_Z = Z[X]/(X^N+1); congruences are coefficientwise modulo the indicated coefficient modulus.

Let the pre-gateway ciphertext be
  c=(c0,c1) in R_B^2,
  B=q0*q1,
under the main dense secret s.

Choose any integer lifts of c0,c1. Define
  r_j = cent_{q1}(c_j)      for j=0,1,
coefficientwise, so every coefficient of r_j lies in [-(q1-1)/2,(q1-1)/2].

OpenFHE physical q1 rescaling gives
  d_j = (c_j-r_j)/q1 mod q0.

Therefore decryption after the componentwise rescale is

  d0+d1*s
    = (c0+c1*s - (r0+r1*s))/q1     mod q0.

Define
  eta_pre := r0 + r1*s.

Let d_tilde be any integer-polynomial representative of d0+d1*s modulo q0. Then by equality modulo q0 there exists k in R_Z such that

  q1*d_tilde
    = c0+c1*s - eta_pre + q0*q1*k
    = c0+c1*s - eta_pre + B*k.          (1)

Hence, after the candidate's public q1 restoration,

  q1*d_tilde - (c0+c1*s)
    = -eta_pre mod B.                    (2)

This proves two separate facts.

### Whole-period/carry theorem

All representative/carry ambiguity introduced by independently centered-rescaling c0 and c1, then multiplying d1 by s, is exactly B*k.

Therefore those carries are invisible modulo the original logical period B. There is NO additional carry term that can move the restored result to a wrong B-period class.

The whole-output semantic effect of physical q1 rescale + public q1 restoration is exactly the standard CKKS rescale rounding term -eta_pre modulo B.

### Exact coefficient-norm bound

By the negacyclic convolution l_infinity/l_1 inequality,

  ||r1*s||_infinity <= ||r1||_infinity ||s||_1.

Since
  ||r0||_infinity, ||r1||_infinity <= (q1-1)/2,

we obtain

  ||eta_pre||_infinity
    <= (1+||s||_1)(q1-1)/2.              (3)

Relative to the restored logical period B=q0*q1,

  ||eta_pre||_infinity / B
    <= (1+||s||_1)(q1-1)/(2 q0 q1)
     < (1+||s||_1)/(2 q0).               (4)

The normal SPARSE_ENCAPSULATED main secret remains a sparse ternary secret of Hamming weight 192; OpenFHE base key generation explicitly samples weight 192 for SPARSE_ENCAPSULATED outside the temporary encapsulated bootstrap secret.

Thus ||s||_1=192 and

  ||eta_pre||_infinity / B < 96.5/q0.    (5)

This term is distinct from:
- epsilon_L: q0-only h32 low sparse-switch error;
- epsilon_H: raised sparse-to-dense switch-back / ApproxModDown error;
- later approximation/linear-transform errors.

Turn 13's identity for an already-existing switch error,
  q1*epsilon/B = epsilon/q0,
remains valid; equation (5) adds the previously missing error created by the physical q1 rescale itself.

## Precision implication

This is not a failure of exact B-period semantics, but it can dominate the precision budget at the smaller end of the degree-2 regime.

Using the worst-case h=192 norm bound alone, the available relative precision from eta_pre is approximately
  log2(q0) - log2(96.5)
bits.

Representative ceilings:
- q0 about 2^31: ~24.4 bits;
- q0 about 2^36: ~29.4 bits;
- q0 about 2^45: ~38.4 bits.

These are conservative worst-case bounds, not measured errors and not final FBT precision. They show why the paper thesis must remain explicitly moderate-precision unless native tails establish more slack.

## Deterministic verification

Artifact:
  /mnt/data/b158_turn16_q1_rescale_carry_oracle.py
  SHA256 31656afc6404a1c7576db6d2be998bede07ad635b052cf8d5ea00efcc5e3a091

Result:
  /mnt/data/b158_turn16_q1_rescale_carry_oracle.json
  SHA256 b9fef51e645f27a82b122fea79576ae3084a1f5d524191b91875567d9494535e

### Exhaustive scalar control

q0=13, q1=17, B=221.
Secrets s from -4 through 4.
All c0,c1 in {0,...,B-1}.

Checked:
  439,569 cases.

For every case:
  q1*d_tilde - (c0+s*c1-eta_pre) is divisible by B,
and
  cent_B(q1*d_tilde-(c0+s*c1)) = cent_B(-eta_pre).

318,990 cases had a NONZERO B-alias integer k, so the test is not vacuous: large representative carries were present and cancelled exactly as theorem (1) predicts.

Observed max |eta_pre| = 40, exactly matching the scalar bound
  (1+4)(17-1)/2 = 40.

### Negacyclic polynomial stress control

R=Z[X]/(X^4+1), q0=17, q1=41, B=697.

Enumerated all 80 nonzero ternary secrets in {-1,0,1}^4 and ran 250 deterministic random ciphertext-vector trials per secret:
  20,000 polynomial cases,
  80,000 checked coefficients.

For every coefficient:
  restored difference equals -eta_pre modulo B,
and every alias discrepancy is a multiple of B.

52,876 checked coefficients had a nonzero B-alias carry.
Max observed |eta_pre| was 94, within the corresponding l1 bound.

No counterexample was found.

## Decision

PASS_MATH: EXACT_CARRY_ORACLE_PASS.

Candidate remains ACTIVE, CORRECTNESS_GATE remains PENDING because the actual candidate binary has still not run.

The decisive semantic uncertainty eliminated this turn is:
  componentwise physical q1 rescaling does NOT create an uncancelled B-period carry after dense-secret decryption and public q1 restoration.

The candidate noise model is changed:
  epsilon_total must now explicitly contain eta_pre in addition to epsilon_L, epsilon_H and downstream FBT error.

This is decision-changing because the native canary is no longer allowed to report success from zero modular LUT error alone. It must separately instrument or upper-bound eta_pre and verify the total precision/DFR budget in the intended moderate-precision parameter point.

## Next decisive test

When a native execution path is available, run the exact candidate canary from Turns 14-15, but add:

1. Immediately before physical q1 rescale, record the exact centered q1 residues r0,r1 of both ciphertext components.
2. Compute/decrypt eta_pre=r0+r1*s_dense, or equivalently measure the pre-gateway restored residual against the original B-period oracle.
3. Report max/quantiles of eta_pre/B over >=7 independent trials.
4. Separately record epsilon_L and epsilon_H.
5. Verify the combined restored residual modulo B, R-normalization metadata/towers, and zero modular 8-bit LUT error.
6. Check achieved precision against the claimed moderate-precision target.

A mechanism-level failure of the exact q0 lift / q1 restore / R normalization, or a total error incompatible with the claimed target parameter regime, PARKS the candidate. No second structural redesign is authorized.

## Evidence references

- Exact PR #1381 head f389e3c8b07955cbc49c9814053fa8eed1b07cc7.
- OpenFHE src/core/include/lattice/hal/default/dcrtpoly-impl.h, DCRTPolyImpl::DropLastElementAndScale.
- OpenFHE src/pke/lib/schemebase/base-pke.cpp, SPARSE_ENCAPSULATED main-secret key generation at Hamming weight 192.
- findings/boot-b158-turn14-single-limb-gateway-source-interface-gate-2026-11-11.md, blob 9c255ea41e7801e7bcffbf7860d12e711fb9fc72.
- findings/boot-b158-turn15-single-limb-gateway-value-ceiling-review-2026-11-11.md, blob 083b20347001dc16ab5d37c0e8060ad5e8a9bc1f.
- b158_turn16_q1_rescale_carry_oracle.py SHA256 31656afc6404a1c7576db6d2be998bede07ad635b052cf8d5ea00efcc5e3a091.
- b158_turn16_q1_rescale_carry_oracle.json SHA256 b9fef51e645f27a82b122fea79576ae3084a1f5d524191b91875567d9494535e.
