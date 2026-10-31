# BOOT RMFE Rank-5 Shared-Correction Recovery Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 6/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task

`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01`

remains pending and is not modified, rerun, or assumed complete.

This side-research turn tests one independent structural question left open by Turn 5:

> After the established R8 C2S map, can the active rank-5 E8 slot state be converted directly into the four correction-style RMFE outputs using shared Frobenius images, avoiding the explicit 8->5 scalar unpack?

No native task, Codex submission, parameter change, or heavy local execution occurred.

## Source facts

Aung et al. ePrint 2025/350, Proposition 3:

Let G=GR(p^r,s), let G' extend G, and let V be a free rank-k G-submodule of G'. Any G-linear map f:V->G' has a unique representation

f(x) = sum_{j=0}^{k-1} theta_j sigma^{s j}(x),

where sigma is the Frobenius automorphism.

For the correction workflow with p=5 and plaintext modulus 625=5^4, Algorithm 4 requires four linear outputs

L_0(z), L_1(z), L_2(z), L_3(z).

Section 5.1 states that CtxtsToSlots forms these outputs by multiplying the k scalar thin ciphertexts by precomputed constants and summing.

## Correct active-domain rank

The established R8 recovery interface uses

S = Z/625Z,
E8 = GR(625,8),

with only the first five coordinates active. The padding coordinates 5,6,7 are zero.

Therefore, after the already-established exact R8 C2S transform, each slot lies not in arbitrary E8 but in the free rank-5 S-submodule

V = span_S{u_0,...,u_4} subset E8 subset E.

This is the key correction to the generic rank-16 direct-map view used in Turn 5.

## Four correction maps on V

For t in {0,1,2,3}, define

D_t : V -> E

by

D_t(sum_i x_i u_i)
  = sum_i x_i phi(e_i)^(5^t).

These are exactly the main RMFE reconstruction and the three correction-map images required by the p=5, e=4 correction workflow.

Each D_t is S-linear.

Apply Aung Proposition 3 with:

G=S,
s=1,
rank(V)=5.

For every t there exist unique coefficients theta_{t,0},...,theta_{t,4} in E such that

D_t(x)
 = theta_{t,0} x
 + theta_{t,1} sigma(x)
 + theta_{t,2} sigma^2(x)
 + theta_{t,3} sigma^3(x)
 + theta_{t,4} sigma^4(x).

Critically, the Frobenius basis

{x, sigma(x), ..., sigma^4(x)}

is common to all four outputs.

## Shared execution schedule

For one ciphertext whose slot state is x in V:

1. compute sigma(x), sigma^2(x), sigma^3(x), sigma^4(x);
2. reuse those five orbit ciphertexts for all D_0,D_1,D_2,D_3;
3. for each output t, multiply the five orbit ciphertexts by the corresponding public theta_{t,j} and sum.

Automorphism/key-switch count:

4 nonidentity Frobenius automorphisms total.

The four outputs require at most 20 ct-pt constant multiplications plus additions before coefficient sparsity is exploited.

No scalar-branch ciphertexts need to be materialized.

This is exactly the same-output-sharing regime in which HElib-style automorphism precomputation is valid: all automorphisms originate from one ciphertext, unlike the killed cross-branch hoisting route.

## Key-set compatibility

The required Frobenius exponents are

5, 25, 125, 625.

The existing BOOT/RMFE fixed-Q ledger already retains the standard Frobenius key set containing these exponents.

Therefore this shared-correction recovery requires no new automorphism-key family.

## Cost impact

Previous conservative candidate transform count:

- five thin S2C: 5
- RM10: 10
- R8 C2S: 6
- E8 unpack: 7

total = 28 automorphism/key-switch-scale calls.

Replace only the explicit E8 unpack + scalar CtxtsToSlots interface with the rank-5 shared-correction map:

- five thin S2C: 5
- RM10: 10
- R8 C2S: 6
- shared rank-5 correction recovery: 4

total = 25.

Thus:

75 -> 25

versus the five-branch baseline transform-side count, a 66.67% structural reduction.

Post-raw inverse/recovery side:

70 -> 20,

a 71.43% structural reduction.

The exact 5->1 boot-key reconstruction from Turn 2 remains unchanged.

## Relation to Turn 5

Turn 5 correctly killed a generic direct rank-16 four-output map:

R8 coefficient state -> four RMFE outputs

with an optimistic 15-automorphism schedule versus current 13.

This turn does not contradict that result.

Instead it keeps the already-efficient 6-automorphism R8 C2S transform, then exploits the fact that the resulting slot state lies in a rank-5 active submodule:

R8 coefficients
  -> R8 C2S
  -> rank-5 V state
  -> shared 4-Frobenius correction outputs.

Cost:

6 + 4 = 10

versus current

6 + 7 = 13.

So the factorized rank-5 route strictly dominates the previously retained explicit-unpack route in automorphism count.

## Important non-claim

Do not identify the correction maps with literal Frobenius powers:

D_t(x) != sigma^t(x)

in general.

The useful structure is Proposition-3 representation on a rank-5 submodule, not equality of each correction map with one Frobenius automorphism.

The Moore coefficients theta_{t,j} may have large plaintext norms; capacity/noise cost is not established by this turn.

## Verdict

RESULT:
  PASS_STATIC_RANK5_SHARED_CORRECTION_RECOVERY

GENERIC_RANK16_DIRECT_RECOVERY:
  remains KILLED_AS_DEFAULT

R8_C2S:
  retained

EXPLICIT_E8_UNPACK:
  structurally DOMINATED

CORRECTION_OUTPUTS:
  4 (L0,L1,L2,L3)

SHARED_NONIDENTITY_FROBENIUS_CALLS:
  4

OLD_CANDIDATE_TRANSFORM_COUNT:
  28

NEW_CANDIDATE_TRANSFORM_COUNT:
  25

BASELINE_TRANSFORM_COUNT:
  75

STRUCTURAL_REDUCTION:
  66.67%

NEW_AUTOMORPHISM_KEY_FAMILY:
  NO

NATIVE_LATENCY:
  NOT_ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT_ESTABLISHED

NOVELTY:
  NOT_ESTABLISHED

## Pending native task interaction

The existing baseline timer task remains valid and must not be rerun.

Its hard-kill ratio rho_ret >= 0.5984704142 remains a sufficient kill condition because the new recovery still has strictly positive cost.

If the timing gate later passes, this rank-5 shared-correction recovery should replace the old 7-automorphism explicit-unpack path before any candidate native implementation.

## Next independent static gate

Before candidate implementation, compute the exact Moore coefficients theta_{t,j} for the established deterministic p=5,w=512 RMFE / R8 interface and audit:

- coefficient support;
- canonical multiplier norms;
- HElib public-multiplier capacity tax;
- whether any theta_{t,j}=0 permits fewer than four nonidentity Frobenius calls.

This remains cheap/static and independent of the pending baseline timing result.

AI_PROVISIONAL_CHOICE:
  RETAIN_POST_RAW_FUSION
  REPLACE_EXPLICIT_UNPACK_WITH_RANK5_SHARED_CORRECTION_RECOVERY
  REQUIRE_EXACT_MOORE_COEFFICIENT_NORM_GATE_BEFORE_NATIVE_CANDIDATE_IMPLEMENTATION

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
