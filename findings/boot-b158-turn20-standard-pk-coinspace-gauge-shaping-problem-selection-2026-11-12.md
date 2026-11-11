# BOOT / B158_OVERALL — Research Turn 20/25
## PROBLEM_SELECTION — compact implicit gauge family via standard public-key zero-encryption coin space

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-standard-pk-coinspace-gauge-shaping-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness and relation to Turn 19

The durable state entering Turn 20 had ACTIVE=UNKNOWN. Turn 19 parked an explicit finite K-entry zero-ciphertext codebook because b-bit simultaneous centered-box shaping in N dimensions needs about K=2^(bN) explicit candidate gauges.

This turn tests a distinct compact escape: do not materialize a K-entry codebook. Instead add a standard public key and let the evaluator exploit the ENTIRE source-supported runtime randomness space of public-key Enc(0), with oracle-optimal public selection of coins. This is stronger than any finite explicit codebook drawn from the same standard public-key encryption distribution.

The turn was initially framed as a compact basis of zero ciphertexts generating exponentially many subset choices. The decisive test is strengthened to a source-dominating upper bound: grant the candidate every standard public-key zero ciphertext reachable from all legal encryption coins for one fixed public key. If even this full support lacks enough covering entropy, any weaker finite basis/codebook realization from the same standard mechanism cannot establish the required generic shaping guarantee.

## Registered decisive test

QUESTION: Can a compact source-supported family of valid zero encryptions, generated from standard Lattigo public-key Enc(0) randomness and selected adaptively by the public evaluator, provide enough effective gauge choices to obtain the approximately 16-bit centered-component improvement targeted at the B175 pointwise gate?

CURRENT_BELIEF: No. The standard public-key zero-encryption coin space is large but finite: the c1 component depends only on an N-coefficient ternary ephemeral secret and an N-coefficient bounded Gaussian error, followed by deterministic basis extension/NTT/product/ModDown. Its support entropy per ring coefficient is therefore far below the 16 bits needed by the explicit centered-box target.

CHEAPEST_DECISIVE_TEST: Inspect exact Lattigo v6.2.0 public-key EncryptZero source, upper-bound the cardinality of the complete reachable c1 shift support for a fixed public key, and compare that support size with the covering number of a centered target box narrowed by 2^16 in every coefficient. Grant oracle-optimal selection and free search/storage to make the test maximally favorable.

IF_PASS: If the complete standard public-key coin space has enough support entropy for constant-probability or worst-case 16-bit covering, admit the candidate ACTIVE and next analyze a polynomial-time coin-selection algorithm, added encryption error, security and actual B175 DFR.

IF_FAIL: If even the entire standard coin space has cardinality too small by an exponential factor, PARK this standard-PK compact gauge mechanism and do not run native rerandomization.

IF_UNCLEAR: Do not promote. Preserve only stronger nonstandard programmable-gauge/evaluation-key mechanisms as a separate future question.

WHICH_PAPER_GATE_CHANGES: Killer gate (3), optimistic end-to-end value/DFR ceiling. Semantic validity and source reachability are granted first.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: If every legal standard public-key zero encryption, even under oracle-optimal selection, cannot cover the required high-dimensional shaping target, implementation and benchmark work cannot establish a generic 16-bit representation rescue for this mechanism.

## Killer gate (1): message semantics

For any legal zero ciphertext Z under the same plaintext modulus/key, adding Z to the B175 operand preserves the plaintext modulo T as long as ordinary encryption correctness holds. Publicly choosing encryption coins before forming Z does not change that algebraic message identity.

Semantic gate: PASS for plaintext preservation.

## Killer gate (2): exact standard Lattigo public-key source

Primary source:
  tuneinsight/lattigo v6.2.0
  core/rlwe/encryptor.go
  blob ce9b051c11e062b9b5db82dd392b86bdf279e52c.

The exact encryptZeroPk path:
1. samples one ephemeral small polynomial u with xsSampler;
2. extends u from Q to QP and transforms it;
3. computes u*pk0 and u*pk1;
4. samples independent bounded errors e0 and e1 with xeSampler;
5. adds e0/e1 to the two QP components;
6. applies deterministic QP->Q ModDown to each component (for an ordinary Q ciphertext);
7. optionally NTT/Montgomery-transforms the result.

Therefore, for a FIXED public key and fixed level/metadata, the runtime support of ct1 is a deterministic image of only (u,e1). The e0 coins do not increase ct1 support.

Durable B175 source audit established the relevant supports at the fixed parameters:
- u has ternary coefficient support {-1,0,1};
- each Gaussian error coefficient has exact bounded support {-19,...,19}, i.e. 39 values.

Hence, regardless of collisions introduced by multiplication and ModDown,
  |Supp(ct1)| <= 3^N * 39^N = 117^N.

For the full degree-one zero ciphertext, a looser bound is
  |Supp(ct0,ct1)| <= 3^N * 39^(2N).

These are SUPPORT UPPER BOUNDS. Deterministic ModDown can only reduce cardinality.

Source/interface gate: PASS. Standard PK Enc(0) provides a compact, publicly generable implicit family, but with the bounded support above.

## Killer gate (3): support-cardinality / covering theorem

Let R_Q be represented coefficientwise as (Z_Q)^N. For the explicit shaping objective define
  B_b = {v : |cent_Q(v_i)| <= Q/2^(b+1) for every i}.

Ignoring boundary rounding,
  |B_b| / |R_Q| <= 2^(-bN).

Let S be ANY set of reachable c1 zero-encryption shifts. An oracle-optimal evaluator succeeds on target component x exactly when
  x + s in B_b
for some s in S.

The union of all targets coverable by S is contained in
  union_{s in S} (B_b - s),
so
  |coverable targets| / |R_Q| <= |S| * 2^(-bN).

Consequences:
1. Worst-case covering of every x requires |S| >= 2^(bN).
2. If x is uniform over R_Q, even an unbounded oracle search over all S succeeds with probability at most |S|*2^(-bN).

This is purely cardinality/covering; it does not assume random sampling of S.

## Instantiate complete standard PK ct1 support

For standard public-key Enc(0),
  log2 |S_c1| <= N*(log2 3 + log2 39)
                   = N*log2(117)
                   ~= 6.8703647*N.

At N=32768:
  log2 |S_c1| <= 225128.11 bits.

The B175 conditional pointwise deficit is about 16 required bits. As in Turn 19, grant the candidate the maximally favorable one-for-one surrogate that a 16-bit simultaneous centered shrink of c1 would recover all 16 downstream bits.

The 16-bit target covering entropy is
  bN = 16*32768 = 524288 bits.

Therefore the STANDARD PK c1 support falls short by
  524288 - 225128.11
  ~= 299159.89 bits.

For a uniform target x, even oracle-optimal search over EVERY standard public-key zero encryption for the fixed key has success probability bounded by approximately
  2^(-299159.89).

For worst-case x, full coverage is impossible because |S_c1| < 2^(16N).

Equivalently, the absolute best simultaneous centered-box shrink that support cardinality could cover for all x is at most about
  log2(117) ~= 6.87 bits per coefficient,
before charging encryption error, selection complexity, or downstream SI behavior.

## Stronger full-ciphertext generosity does not rescue 16-bit entropy

Even if one incorrectly grants the evaluator all e0 randomness as additional independent gauge entropy for a joint two-component score,
  log2 |Supp(ct0,ct1)|
    <= N*(log2 3 + 2 log2 39)
    ~= 398320.17 bits.

This is still below 524288 by about 125967.83 bits.

This full-support comparison is only a generosity check. For the explicit c1 centered-box objective the tighter 225128-bit bound is the relevant one.

## Relation to the initial m-basis idea

A binary basis of m precomputed zero ciphertexts can expose at most 2^m subset choices. Therefore it needs m>=bN=524288 independent choice bits merely to match the 16-bit covering entropy target. With the durable B175 estimate of about 9.50 MiB raw Q payload per degree-one L18 ciphertext, literally storing 524288 full-size basis zero ciphertexts is about 4.75 TiB before metadata and selection work.

This storage number is secondary: the stronger standard-PK source result above shows that the entire normal public-encryption coin space itself contains less than the required c1 covering entropy.

## Important scope limitation

This result DOES NOT prove that every possible compact programmable gauge mechanism fails.

It kills the explicit target:
  standard Lattigo public-key Enc(0) coin optimization -> 16-bit simultaneous centered c1 box shaping.

A nonstandard evaluation key that maps an evaluator-chosen arbitrary gauge polynomial into a controlled zero ciphertext, or another structured mechanism with a much larger effective gauge image than standard PK Enc(0), is outside this result. Such a mechanism must be treated as a new cryptographic construction with its own noise, key-size, security, selection-algorithm and value gates.

The result also does not assert that actual B175 c1 is uniformly distributed. The 2^-299159 figure is a uniform-target coverage ceiling, while the worst-case statement is only that some targets are necessarily uncovered. A B175-lineage-specific probabilistic success claim would require the actual component distribution.

## Prior-art boundary

Public-key rerandomization by adding Enc(0) is standard. The candidate delta is not rerandomization itself but adaptive optimization over the full legal public-key encryption coin space to exploit B175 component-gauge sensitivity.

No independent novelty audit is warranted because the mechanism fails its optimistic covering/value gate.

## Decision

FAIL_STANDARD_PK_SUPPORT_CEILING -> PARKED.

Candidate:
  boot-b158-standard-pk-coinspace-gauge-shaping-v1

Standard public-key zero encryption is semantically valid and compactly/publicly generable, but its entire fixed-key runtime c1 support has only about 6.87 bits of choice entropy per ring coefficient. That is insufficient for the candidate's favorably credited 16-bit simultaneous centered-component shaping target.

No native experiment is justified.

## Reopen condition

Reopen only with a NONSTANDARD source-backed programmable gauge mechanism whose effective fixed-key gauge image is provably much larger than the standard public-key Enc(0) support and that provides:
1. public evaluator control over enough gauge entropy to cover or probabilistically hit the actual B175 favorable tensor/quantization region;
2. a polynomial-time selection/decoding algorithm;
3. controlled zero-encryption/evaluation-key error and useful DFR;
4. a key/storage/runtime model that remains materially better than the existing B158 alternatives;
5. complete security analysis for the new evaluation material.

Adding more random trials from the same standard public-key Enc(0) distribution, exhaustive search over its coin space, or a finite subset/basis of that same support does not satisfy the condition.

## Eliminated uncertainty

Eliminated: Does replacing Turn 19's explicit codebook by the entire compact standard public-key zero-encryption coin space provide enough representational freedom for a generic 16-bit c1-centered shaping rescue?

Answer: No. The complete fixed-key ct1 support is at most 117^N ~= 2^(6.87N), versus approximately 2^(16N) covering entropy for the stated shaping target. At N=32768 the entropy deficit is about 299160 bits.

## Evidence references

- findings/boot-b158-turn19-adaptive-zero-codebook-gauge-shaping-problem-selection-2026-11-12.md; blob 98874687b1b314bd0dccf9ff70dc108b81bef810.
- findings/boot-B175-zero-rerandomization-support-guarantee-2026-10-29.md.
- findings/boot-B175-common-lineage-gauge-accessibility-2026-10-29.md.
- findings/boot-B175-decryption-fiber-gauge-realizability-2026-10-29.md.
- Lattigo v6.2.0 core/rlwe/encryptor.go blob ce9b051c11e062b9b5db82dd392b86bdf279e52c.
- Lattigo v6.2.0 ring/sampler_gaussian.go blob bc1039236d34dd27503c8b487345b95838356182.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.
- B175 source/main.go SHA256 a2f6ed20981e182519de044703bf50b6c1981245a5a6df67dfdf3f90b992cd20.