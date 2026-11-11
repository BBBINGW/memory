# BOOT / B158_OVERALL — Research Turn 19/25
## PROBLEM_SELECTION — adaptive zero-codebook gauge shaping

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-adaptive-zero-codebook-gauge-shaping-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 19 had ACTIVE=UNKNOWN. This candidate does not reopen or rename any recent closed candidate. It is distinct from the prior B175 unselected zero-rerandomization screen: instead of adding one uncontrolled Enc(0), the evaluator receives a finite offline codebook of valid zero encryptions and publicly selects the codeword that gives the most favorable ciphertext-component representative before the failing B175 SI pointwise multiplication.

## Mechanism

Let C=(c0,c1) be the low-headroom operand to be gauge-shaped before SI multiplication. The key owner precomputes K valid secret-key zero encryptions
  Z_j=(z0_j,z1_j),  j=1,...,K,
under the same key, level and modulus. The evaluator may inspect all public ciphertext components and choose
  j* = argmin_j ||cent_Q(c1+z1_j)||_infinity,
then use C'=C+Z_j* in the pointwise multiplication.

Because adding an encryption of zero preserves the plaintext modulo T while changing the public ciphertext representative, this mechanism attempts to exploit the B175 gauge sensitivity without online secret access.

For the optimistic screen, grant the candidate the strongest useful assumption: a b-bit reduction in the centered c1 infinity norm is credited one-for-one as b bits of recovered downstream required-logQ. This is deliberately favorable; the real SI output need not improve by that much.

## Registered decisive test

QUESTION: Can a finite offline Enc(0) codebook with public best-of-K selection produce the approximately 16-bit representation improvement required by the B175 fixed-Q pointwise deficit at any remotely acceptable storage/runtime cost?

CURRENT_BELIEF: No. In Lattigo secret-key zero encryption the second component shift is uniform over R_Q. Requiring all N coefficients of the selected representative to lie in a centered box narrower by 2^16 is a high-dimensional covering problem whose success fraction is about 2^(-16N).

CHEAPEST_DECISIVE_TEST: Prove the exact best-of-K central-box probability/covering bound for a uniform R_Q gauge shift, instantiate N=32768 and b=16, and compare the required K with even a free-storage/free-generation optimistic ceiling. Use the existing 9.50 MiB degree-one ciphertext payload only as a concrete secondary cost illustration.

IF_PASS: If a polynomial or practically storable K can give material success probability, admit the candidate ACTIVE and next audit the public score, added zero-encryption error, security and real DFR on B175 operands.

IF_FAIL: If non-negligible success requires K exponential in bN, PARK immediately. Do not run native B175 rerandomization or benchmark an exponentially large search.

IF_UNCLEAR: Keep the broader adaptive-rerandomization family unclassified, but do not admit this explicit finite-codebook c1-shaping mechanism.

WHICH_PAPER_GATE_CHANGES: Killer gate (3), optimistic end-to-end value ceiling, after semantic and source feasibility are checked. It also bounds the probabilistic correctness/DFR ceiling of this explicit shaping target.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: The candidate has scientific value only if favorable gauges are searchable with a realistic codebook. If the required codebook is exponential in the ring dimension, implementation and native testing cannot change the paper decision.

## Killer gate (1): exact semantic oracle

Each Z_j is a valid encryption of plaintext zero under the same plaintext modulus and secret. Therefore
  Dec(C+Z_j) = Dec(C) + 0 mod T
whenever ordinary ciphertext correctness holds. Public selection among valid Z_j does not change this message identity.

The added encryption error remains a separate correctness/noise cost; it is not assumed away in a full construction. For the present fail-fast value screen we grant it for free, which is favorable to the candidate.

Semantic result: PASS for message preservation.

## Killer gate (2): source/interface feasibility

Durable B175 source audit already established for Lattigo secret-key zero encryption:
  Z_sk(a,e)=(e-a*s, a),
with the second component a uniform in R_Q. CRT and NTT are bijections, so a is uniform over the coefficient-vector space R_Q ~= (Z_Q)^N.

An offline key owner can therefore generate valid same-key zero ciphertexts and provide them to the evaluator. The current B175 path does not contain such a codebook, but no new cryptographic primitive is needed merely to materialize and add these ciphertexts.

Source/interface result: PASS in the optimistic offline-preprocessing model.

## Killer gate (3): exact covering/value bound

Represent the second ciphertext component by its coefficient vector x in (Z_Q)^N. For b>=0 define the centered target box
  B_b = {v : |cent_Q(v_i)| <= Q / 2^(b+1) for every coefficient i}.

Up to the irrelevant integer rounding of the boundary, the fraction of all ring elements lying in B_b is at most
  p_b <= (2^(-b) + 1/Q)^N.

### Random best-of-K codebook

For any fixed starting c1=x and any independently sampled zero-encryption shifts a_j uniform in R_Q, each x+a_j is uniform in R_Q. Even after public adaptive selection of the best candidate, the union bound gives
  Pr[exists j: x+a_j in B_b] <= K * (2^(-b)+1/Q)^N.

For the actual Q, 1/Q is negligible. Thus constant success probability requires approximately
  log2 K >= b*N.

### Deterministic offline codebook

The same exponent is a covering-number lower bound, not merely a random-sampling artifact. A fixed shift a_j covers exactly one translate of B_b in the possible-x space. K translates cover at most K*|B_b| targets. To guarantee the b-bit centered-box target for every x,
  K >= |R_Q|/|B_b| ~= 2^(bN).

Thus no clever deterministic choice of a finite explicit codebook removes the dimensional exponent.

## B175 instantiation

Use the fixed B158/B175 ring dimension
  N = 32768.

The B175 direct SI pointwise failure has a conditional 16-required-bit recovery target. Grant the candidate the maximally favorable one-for-one assumption that shrinking the public c1 centered infinity norm by b=16 would provide all 16 missing output bits.

Then
  b*N = 16*32768 = 524288,
so a constant-success explicit codebook needs on the order of
  K ~= 2^524288
valid zero ciphertexts.

Even absurdly large practical search budgets are useless. If K=2^64, the central-box shrink exponent available at constant probability is only
  b_eff ~= log2(K)/N = 64/32768 = 0.001953125 bits.

For K=2^20,
  b_eff ~= 0.0006103515625 bits.

These are not downstream SI-noise claims. They quantify only the candidate's own explicit public component-shaping objective, under the most favorable mapping from component shrink to final benefit.

## Storage and online-cost consequence

The durable B175 audit reports about 9.50 MiB raw Q-coefficient payload for one degree-one L18 ciphertext. Storing 2^524288 such zero ciphertexts is physically meaningless.

More importantly, the failure does not depend on storage accounting: even granting free storage and free zero-cipher generation, a literal best-of-K public search over K candidates is exponential. Any structured combinatorial generator that represents exponentially many gauges without materializing K standalone ciphertexts would be a different mechanism and requires a new source/noise/cost analysis; it is not silently included in this candidate.

## Prior-art boundary

Adding Enc(0) for rerandomization is established FHE practice and was already analyzed in the durable B175 rerandomization findings. The only candidate delta here is public adaptive best-of-K codebook selection for favorable component geometry before the SI multiplication.

No independent novelty audit is performed because the candidate fails the optimistic value gate before admission.

## Decision

FAIL_VALUE_CEILING -> PARKED.

Candidate:
  boot-b158-adaptive-zero-codebook-gauge-shaping-v1

The mechanism is semantically valid and source-feasible in an optimistic offline model, but an explicit finite codebook cannot give the required material component shaping at realistic scale. The obstacle is high-dimensional covering: b bits of simultaneous coefficient shrink require about bN bits of codebook-selection entropy, i.e. K~=2^(bN) explicit gauges.

No native execution is justified.

## Reopen condition

Reopen only with a genuinely different structured gauge-generation mechanism that does not enumerate an explicit K-sized codebook and that supplies all of the following:
1. public generation/selection of at least 2^(Omega(bN)) effective gauge choices from compact evaluation material;
2. a source-backed proof that the chosen structured combinations remain valid zero encryptions with controlled accumulated error;
3. a polynomial-time selection algorithm for the B175 tensor/quantization objective;
4. an end-to-end bound showing at least the required fixed-Q recovery (about 16 required bits at the B175 pointwise gate) with useful DFR;
5. total key/storage/runtime cost that beats the existing same-ring checkpoint/PS alternatives.

A larger explicit codebook, repeated unselected rerandomization, or secret-dependent exact gauge selection does not satisfy this condition.

## Eliminated uncertainty

Eliminated: Can explicit best-of-K zero-encryption rerandomization make public component-centered gauge shaping a practical B175 rescue by searching many offline gauges?

Answer: No for the explicit finite-codebook mechanism. At N=32768, even a favorably credited 16-bit centered-box improvement requires about 2^524288 candidates for constant success.

## Evidence references

- findings/boot-B175-zero-rerandomization-support-guarantee-2026-10-29.md.
- findings/boot-B175-common-lineage-gauge-accessibility-2026-10-29.md.
- findings/boot-B175-decryption-fiber-gauge-realizability-2026-10-29.md.
- findings/boot-B175-representation-mechanism-negative-screen-2026-10-29.md.
- B175 ZIP SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.
- B175 source/main.go SHA256 a2f6ed20981e182519de044703bf50b6c1981245a5a6df67dfdf3f90b992cd20.