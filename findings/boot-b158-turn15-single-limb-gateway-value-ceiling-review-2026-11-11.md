# BOOT / B158_OVERALL — Research Turn 15/25
## Mandatory VALUE_REVIEW — optimistic end-to-end ceiling for q0 sparse gateway

Date: 2026-11-11 (Asia/Singapore)
Candidate: boot-b158-single-limb-sparse-gateway-composite-v1
Entering durable phase: VALUE_GATE
This is a static VALUE_REVIEW, not a matched performance result.

## Pre-registration

QUESTION:
Even if the bounded q0-provenance repair from Turn 14 is correct, is the maximum plausible whole-system benefit of replacing the large-bottom h=64/K=28 FBT path by h=32/K=16 large enough to justify a candidate-native correctness canary after accounting for conversion, key, noise/DFR, memory and offline costs? If the optimistic ceiling is not materially positive, PARK before spending native effort.

CURRENT_BELIEF:
The target K=16 tables cross a real Paterson-Stockmeyer depth boundary relative to K=28, so the candidate should save one logical FBT level in the target regime. The gateway adds only linear-RNS conversion work if the construction stays within Turn 14's bounded repair. The main risks are hidden security-driven N growth and whether the native q1 restore actually remains public/linear.

CHEAPEST_DECISIVE_TEST:
Use OpenFHE's exact FBT coefficient degrees, depth table, PS multiplication-count formula, composite-degree tower accounting, and sparse-key parameter generation to compute a static best-case ceiling. Count mandatory extra candidate operations and key/table footprint. Do not benchmark because candidate correctness has not passed.

IF_PASS:
If the ceiling includes a strict one-level saving plus nontrivial operation/key savings with no mandatory compensating ct×ct multiplication, new evaluation-key family, or reliability downgrade, mark VALUE_REVIEW completed and return next to the candidate-native CORRECTNESS canary. Full VALUE_GATE remains pending until matched measurements and security pass.

IF_FAIL:
If the saved level is cancelled by a mandatory extra level, equivalent expensive key switching, larger ring dimension already forced by known source constraints, or a mandatory reliability/precision loss, PARK the candidate before native implementation.

IF_UNCLEAR:
If the source does not decide whether the intended q1 rescale/restore is linear/public or whether the K=16 path really changes chain length, keep VALUE_GATE pending and resolve only that ambiguity before native work.

WHICH_PAPER_GATE_CHANGES:
Mandatory VALUE_REVIEW / optimistic killer gate (3). A PASS here does not pass the full VALUE_GATE.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
The candidate already consumed a bounded source repair. Without a positive whole-system ceiling, the protocol requires parking rather than continuing local correctness work. A positive ceiling is the justification for spending the next native turn on the exact canary.

## Exact delta to closest stock paths

OpenFHE PR #1318 states:
- SPARSE_ENCAPSULATED h=32 uses K=16 for first moduli <=60 bits.
- h=64 uses K=28 above 60 bits.
- For FBT, the K=28 replacement crosses the 59-degree Paterson-Stockmeyer depth boundary and costs one additional level in the affected small/arbitrary-LUT and binary regimes.
- The extra level cannot be removed by simply changing double-angle count.

OpenFHE current/merged source implements the corresponding FBT tables:
- h32/K16 complex exponential: coeff_exp_16_double_46, degree 46.
- h64/K28 complex exponential: coeff_exp_28_double_69, degree 69.
- h32/K16 cosine: coeff_cos_16_double_50, degree 50.
- h64/K28 cosine: coeff_cos_28_double_68, degree 68.
- Both sparse regimes use R_SPARSE_FBT=2 double-angle iterations in this FBT path.

OpenFHE GetDepthByDegree table:
- degree 28..59 -> depth 7.
- degree 60..119 -> depth 8.

Therefore the target replacement produces an exact static reduction of one multiplicative level:
- complex exp 69 -> 46: 8 -> 7.
- binary cosine 68 -> 50: 8 -> 7.
The equal double-angle term means the total FBT depth difference remains exactly one in those branches.

OpenFHE ComputeDegreesPS gives the homomorphic multiplication count
  k + 2m + 2^(m-1) - 4
for the selected PS parameters.
For the relevant degrees:
- degree 46: m=3,k=7 -> 13 multiplications.
- degree 69: m=3,k=10 -> 16 multiplications.
- degree 50: m=3,k=8 -> 14 multiplications.
- degree 68: m=3,k=10 -> 16 multiplications.
Thus the K16 route statically removes 3 PS multiplications for the complex-exponential branch and 2 for the binary cosine branch, before considering the cheaper chain produced by the lower depth.

## Composite-scaling amplification of the saved level

PR #1286/source documents that composite-scaling level accounting is multiplied by compositeDegree and that all relevant FBT tower counts are scaled accordingly.

For the active degree-2 regime:
- one logical FBT level = two physical Q limbs.
- eliminating the K28-only level therefore eliminates two chain towers at fixed levels-after-bootstrap.
- equivalently it removes approximately one scaling-modulus worth of log Q, represented by those two native primes.

No claim is made here that N can be reduced. A smaller Q may improve the security margin or later permit a smaller N in some parameter sets, but that requires the security gate and is not counted in the positive ceiling.

## Low sparse-switch key / offline footprint

Stock composite sparse encapsulation precomputes Ql with sizeQl=compositeDegree and sizes the auxiliary sparse modulus against the whole bottom modulus.

For the degree-2 >60-bit baseline:
- Ql has 2 limbs.
- auxBitsSparse=127.
With 64-bit register words and MAX_MODULUS_SIZE=60, the source's splitting loop requires 3 auxiliary primes (~43 bits each), so the low sparse key lives over 2+3=5 towers.

Candidate q0 gateway:
- Qg has 1 limb.
- the h32 one-limb rule uses ~66 auxiliary bits.
At 64-bit register size this is 2 auxiliary primes (~33 bits), hence 1+2=3 towers.

Static local key-tower reduction for this low transition key:
  5 -> 3, i.e. 40% fewer towers in each a/b polynomial of that key.

At 32-bit register size:
- 127 bits requires 5 auxiliary primes (~26 bits): 2+5=7 towers.
- 66 bits requires 3 auxiliary primes (~22 bits): 1+3=4 towers.
Local reduction:
  7 -> 4, about 43%.

This is not a whole-key-set percentage. It is only the mandatory low sparse-transition key. The candidate does not require keeping the baseline degree-2 low key in a fair candidate-only context.

## Raise-switch key footprint

Turn 14 established that the candidate reuses PR #1381's one-row exact-q0-lift KeySwitchRaise path. The stock degree-2 path has at least one digit/row and may have more depending on the raised-basis partition. Therefore the candidate's mandatory raise-switch row count is not larger than the stock minimum of one; no strict global key-memory saving is claimed without concrete parameters.

The public q1 restoration requires no evaluation key in the intended construction.

## Mandatory candidate runtime costs

Relative to stock degree-2 PR #1381, the candidate adds:
1. one physical q1 rescale/drop before the low sparse switch;
2. one public q1 restoration after sparse-to-dense switch-back and before R normalization;
3. candidate-local Qg/Pg tables and a provenance/dispatch condition.

Under the Turn-14 construction these are linear RNS/basis operations on existing ciphertext components. They do not introduce:
- a ciphertext-ciphertext multiplication;
- a new multiplicative level;
- a new independent key-switch family;
- a second sparse secret;
- an additional bootstrapping iteration.

Conversely, candidate work is cheaper in two existing components:
- low sparse switch runs on Qg={q0} with ~66-bit Pg instead of two-limb Ql with ~127-bit P';
- raise switch uses the exact-q0-lift single-digit path rather than the generic degree-2 decomposition path.

The exact wall-clock crossover is intentionally not claimed before a matched native benchmark.

## Noise / precision / DFR ceiling

Source documentation for h32/K16 SPARSE_ENCAPSULATED reports full-packing overflow failure below approximately 2^-137/2^-138 at N=2^16 and about 2^-137 at N=2^17, while h64/K28 remains similarly negligible.

UnitTestSparseKS source documents the h32 one-limb switch with ~66-bit P' as having key-switch term below one per coefficient and measured maximum added noise around 2^3 in its calibration regime.

Turn 13 already established algebraically that restoring q1 does not amplify switch error relative to the restored B=q0q1 period:
  q1*epsilon/B = epsilon/q0.

Therefore the optimistic ceiling contains no mandatory precision/DFR penalty. This is conditional: candidate-native epsilon_L/epsilon_H tails and exact whole-output DFR remain pending and can still kill the candidate.

## Security ceiling

No fresh concrete security estimator has passed.

The stock library already uses h32 sparse encapsulation for <=60-bit first moduli, so h32 itself is not an unsupported primitive. However the candidate exposes h32-related evaluation keys inside an ambient degree-2 / larger-Q context, and the source's existing h64 choice above 60 bits cannot be assumed to be purely a DFR policy without a dedicated security audit.

Consequently this VALUE_REVIEW does NOT assume a proven same-N security result. It records a conditional positive ceiling:
- if the security gate accepts the existing N, the system-level ceiling is materially positive;
- if security forces a larger N, the matched VALUE_GATE must include that cost and may fail.

Because security is ordered after candidate correctness, this unresolved item does not justify a benchmark now.

## Static ceiling summary

Benefits that are source-exact in the target branch:
- 1 fewer logical multiplicative level.
- degree 2 -> 2 fewer physical Q towers at equal output-depth target.
- 3 fewer PS homomorphic multiplications for complex-exp arbitrary-LUT path (16 -> 13).
- 2 fewer PS homomorphic multiplications for binary cosine path (16 -> 14).
- low sparse-transition key footprint 5 -> 3 towers in the 64-bit-register case, 7 -> 4 in the 32-bit-register case.
- candidate raise-key row count no larger than the one-row minimum; possible additional saving not counted.

Mandatory added costs:
- one q1 physical rescale/drop;
- one public q1 restoration;
- small candidate-specific RNS tables/metadata.
No mandatory added multiplicative level or ct×ct multiplication is present in the bounded design.

Unresolved costs excluded from a performance verdict:
- security-driven N change;
- candidate-native noise tails / DFR;
- actual NTT and memory-traffic cost of q1 restore;
- exact raise digit count of the matched baseline;
- implementation overhead / cache effects.

## Decision

VALUE_REVIEW_STATIC_CEILING_PASS.

The optimistic end-to-end ceiling is materially positive and is not a mere bookkeeping improvement. Even before any possible raise-switch simplification, the mechanism targets a strict depth boundary and removes 2-3 homomorphic multiplications while the mandatory gateway additions are linear/public RNS operations.

This is sufficient to justify one candidate-native correctness canary.

It is NOT a performance claim and does NOT pass VALUE_GATE:
- BASELINE_MATCHED=false;
- no wall-clock benchmark was run;
- security is unresolved;
- candidate correctness is unresolved.

The next research action must return to CORRECTNESS_GATE and run the exact candidate-native canary specified in Turn 14. Only after correctness and security pass should a matched reduced-chain benchmark be performed.

## Eliminated uncertainty

Eliminated:
"Could the candidate be incapable of material whole-system value even in the optimistic case because its mandatory gateway overhead necessarily cancels the K16 depth benefit?"

Answer: no. Stock source gives a strict one-level/two-tower and 2-3 PS-multiplication advantage, while the bounded gateway requires no mandatory compensating level, ct×ct multiplication or extra eval-key family.

Still open:
actual runtime gain; same-N security; native correctness; precision/DFR tails; exact matched key memory.

## Evidence references

- OpenFHE PR #1318: h32/K16 vs h64/K28 and the one-level FBT boundary.
- OpenFHE src/pke/include/scheme/ckksrns/ckksrns-fhe.h: coeff_exp_16_double_46, coeff_exp_28_double_69, coeff_cos_16_double_50, coeff_cos_28_double_68, R_SPARSE_FBT=2, K_SPARSE_ENCAPSULATED=16, K_SPARSE=28.
- OpenFHE src/pke/lib/scheme/ckksrns/ckksrns-utils.cpp: GetDepthByDegree ranges and ComputeDegreesPS multiplication-count formula.
- OpenFHE PR #1286 / composite-scaling source: logical level/tower accounting by compositeDegree.
- OpenFHE src/pke/lib/scheme/ckksrns/ckksrns-cryptoparameters.cpp: sparse auxiliary modulus rules (66 vs 127 bits) and prime splitting.
- OpenFHE UnitTestSparseKS.cpp source comment: h32/~66-bit low-switch calibration.
- Turn 13 durable result supplied in active state: q1 restoration relative-noise identity.
- Turn 14 durable finding: bounded source-interface repair and exact-q0-lift raise path.
