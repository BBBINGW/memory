# BOOT — DESCENT_MVB_GATE_2: correct composition target and carrier-rank bound

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state (unchanged)

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Source correction: the previous commutation gate was too strong

The prior finding proved a conditional no-go for trying to commute a function-specific polynomial multiplier B_f through a coefficient-projection-like descent D. That theorem is mathematically valid for that model, but it is NOT the correct decisive gate for composing standard MVB with Descent-PBS.

TCHES 2024 Mono–Kluczniak–Güneysu, Algorithm 1, explicitly performs:
1. one BlindRotate on a common polynomial w, producing macc = w X^{<c,s>};
2. only AFTER the shared blind rotation, multiply the accumulator by each public polynomial v[i];
3. SampleExtract each result.

Thus a Descent × MVB composition does not need D B_f = \tilde B_f D. The correct question is whether the post-descent ring ciphertext is still a sufficiently expressive common carrier for multiple cheap function-specific readouts.

The earlier kernel-preservation theorem remains a valid conditional negative result for schemes that literally try to push B_f across D, but it should no longer be used as the main gate.

## Direct post-descent carrier model

Let K be a coefficient field (or finite coefficient alphabet where the same cardinality argument applies), and let
    R = K[X]/(X^N+1).

For each plaintext-domain point m in a set S of size t, suppose the function-independent prefix of bootstrapping plus descent produces a ring message/carrier
    a_m in R.

For a public post-descent multiplier v in R, define the output
    f_v(m) = L(a_m v),
where L:R->K is a fixed linear extraction, e.g. constant-coefficient SampleExtract at the plaintext-message level.

Choose coefficient vectors for a_m and v. Negacyclic multiplication followed by a fixed coefficient extraction is bilinear, hence for fixed a_m it is linear in v. Therefore there is a matrix
    A_D in K^{t x N}
such that the complete function vector is
    f_v = A_D * vec(v).

This gives the following capacity bound.

### Carrier-rank theorem

The K-linear space of functions S -> K representable from ONE fixed N-dimensional descended carrier using only:
- one public ring multiplication by v, and
- one fixed linear extraction,
has dimension at most rank(A_D) <= N.

Hence if t > N, this direct readout layer cannot realize all K-valued t-entry LUTs.

Equivalent finite-alphabet counting form: if coefficients and outputs range over the same q-element alphabet, there are at most q^N choices of v/readout functions but q^t arbitrary q-valued LUTs; for t>N, surjectivity is impossible.

### Scope

This theorem does NOT say:
- no useful multiple outputs can be read from the same carrier;
- no binary-output family is possible for every q/domain convention;
- Descent-PBS itself cannot evaluate large LUTs.

It only kills the strongest direct proposal:
    large-domain Descent -> one N-dimensional ring carrier -> arbitrary LUT solely by public MVB-style multiplier + linear SampleExtract
when the desired arbitrary function space has dimension t>N.

A small or structured set of target functions can still survive if its function vectors lie in Col(A_D).

## Why this matters specifically for Descent-PBS

The public abstract of ePrint 2026/2616 states that after the first module rotation, truncation/FKS descends the accumulator to the ring, and bootstrapping then continues with Meta-PBS refinements in the ring.

Therefore these refinement stages are not a cosmetic implementation detail: for tables beyond the ring dimension, they must provide additional expressive power beyond a single N-dimensional linear carrier/readout.

This shifts the candidate from:
    "share Descent and then do arbitrary MVB outputs"
to:
    "identify the LATEST function-independent prefix of Descent-PBS, possibly including some ring refinements, and branch only after that prefix."

Call this the LATE-BRANCH candidate.

## Narrow surviving candidate: structured multi-output factorization

For target functions f_1,...,f_k on the same encrypted input, assemble
    F = [f_1 ... f_k] in K^{t x k}.

A direct common-carrier construction exists only if
    F = A_D V
for some V in K^{N x k},
or the appropriate signed/scaled analogue under the scheme's exact plaintext representation.

Thus the cheapest structural test after obtaining the exact Descent-PBS map is:
1. reconstruct the reachable carrier matrix A_D;
2. test whether useful multi-output families lie in Col(A_D);
3. if not, include one additional Meta-PBS refinement and repeat;
4. find the maximal shared prefix / latest legal branch point.

Potential useful families should be chosen for real multi-output demand, not arbitrary synthetic LUTs: bit decomposition, comparison flags, range/category outputs, or several predicates on the same integer. These are examples only; no compatibility is claimed yet.

## Prior-art boundary

This candidate cannot claim novelty from "one function-independent blind rotation, many function-specific outputs." That is established MVB prior art:
- TCHES 2024 gives a practical algorithm using one BlindRotate followed by per-output public polynomial multiplications.
- ePrint 2026/2332 explicitly studies Multi-Value Mode with one function-independent rotation shared by all outputs and exact output-noise amplification.

Any novelty would have to be specifically:
    large-domain Descent-PBS + a newly proved maximal shared prefix / late branch for multiple outputs,
with a useful function family, security/noise correctness, and a material cost win over independent Descent-PBS executions.

## Source-status gate

Exact ePrint 2026/2616 full text is still unavailable through the verified research MCP:
- official IACR PDF: HTTP 403;
- arXiv title query: unavailable/timed out;
- fixed arturo-kong GitHub ePrint mirror: 2026/2616.pdf absent;
- several other public ePrint mirrors were also checked and did not contain this new PDF.

Therefore the following remain UNKNOWN until the full paper is supplied/read:
- exact module accumulator representation;
- exact truncation and merged-column FKS map;
- which Meta-PBS test polynomials/refinements depend on LUT values;
- the exact reachable carrier states after each stage;
- whether a function-independent prefix extends beyond descent;
- noise formulas for a branched multi-output construction.

Do not claim an actual Descent-PBS construction from the abstract.

## Gate decision

PREVIOUS_COMMUTATION_GATE_AS_MAIN_GATE: RETIRED
COEFFICIENT_PROJECTION_NO_GO_THEOREM: RETAIN_AS_CONDITIONAL_LEMMA
DIRECT_POST_DESCENT_ARBITRARY_LUT_FOR_t_GT_N: FAIL_BY_CARRIER_RANK
STRUCTURED_MULTI_OUTPUT_AFTER_DESCENT: UNCLEAR
LATE_BRANCH_DESCENT_MVB: PROMISING_ENOUGH_FOR_SOURCE_GATE
NOVELTY: NOT_ESTABLISHED
NATIVE_REQUIRED_NOW: NO

## Next minimum verification

DESCENT_MVB_GATE_3:
1. acquire exact current ePrint 2026/2616 PDF;
2. mark every stage as function-independent vs LUT-dependent;
3. derive carrier/state map after each shareable stage;
4. form the representability matrix A_j for the first realistic multi-output family;
5. stop immediately if no nontrivial late branch exists;
6. only then do noise/cost/prior-art comparison.

B163 remains untouched until Codex quota is explicitly restored by the PI.
