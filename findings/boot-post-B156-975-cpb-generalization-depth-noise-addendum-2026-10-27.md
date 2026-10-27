# BOOT post-B156 — 2026/975 CPB generalization / depth / noise addendum

Date: 2026-10-27
TRACK_ID: BOOT
Parent finding: findings/boot-post-B156-975-copacked-dyadic-power-basis-gate-2026-10-27.md
State impact: NONE. Do not modify B157 pending state.
No Codex / GPU / remote execution was used.

## 1. Correction retained: actual Lattigo evaluator mode

The author repository imports Lattigo `schemes/bgv` under the local alias `bfv` and constructs:

`bfv.NewEvaluator(params, evaluationKeys, false)`

so the implementation is using standard BGV-style tensoring rather than BFV scale-invariant tensoring.

However, Lattigo v6.2.0 standard BGV `Mul(ct, []uint64)` still:
- copies ciphertext metadata into a temporary plaintext,
- explicitly sets plaintext scale to 1,
- encodes the slot vector,
- applies standard tensoring.

Thus a public 0/1 selector multiplication through `MulNew(ct, selector)`:
- preserves level,
- preserves ciphertext scale,
- does not require an immediate rescale for metadata/scale compatibility.

The prior parent conclusion `SELECTOR_SCALE_LEVEL_GATE=PASS_SOURCE` therefore remains valid, but for the corrected reason.

## 2. Plaintext-selector coefficient-domain audit

The exact Lattigo BGV encoding path was reconstructed from source:
- slot permutation from powers of GaloisGen=5 via `permuteMatrix`;
- plaintext-ring INTT;
- centered representatives modulo T.

Audit parameters:
- N=32768
- T=65537
- same split-slot ordering as the author implementation.

Compared:
A. baseline 2026/975 bit masks `c_i[k]=(k>>i)&1`;
B. CPB heavy selector = the same dyadic bit selector restricted to physical row0;
C. pure physical-row selectors.

Representative centered coefficient statistics:

- baseline c_0: L1 = 34,808; nonzero = 3; maxabs = 32,768
- CPB heavy M_0: L1 = 17,476; nonzero = 4; maxabs = 16,384

- baseline c_1: L1 = 155,652; nonzero = 5
- CPB heavy M_1: L1 = 85,825; nonzero = 6

- baseline c_5: L1 = 1,058,556; nonzero = 65
- CPB heavy M_5: L1 = 1,151,314; nonzero = 66

- baseline c_10: L1 = 32,725,348; nonzero = 2,049
- CPB heavy M_10: L1 = 33,570,588; nonzero = 2,050

- baseline c_13: L1 = 267,609,134; nonzero = 16,385; maxabs = 32,768
- CPB heavy M_13: L1 = 269,549,952; nonzero = 16,386; maxabs = 32,767

At the largest relevant bit the L1 difference is only about 0.7%.

Pure row selectors are exceptionally simple in coefficient form:
- 2 nonzero coefficients;
- centered L1 = 32,896;
- one row selector has coefficients approximately (-32768, -128) at indices (0,N/2);
- the complement has approximately (-32768,+128).

Conclusion:
CPB does not introduce a qualitatively worse family of dense selector plaintexts.
Each layer has:
- one heavy selector with coefficient norm essentially comparable to a baseline EvalPower bit mask;
- one very light row selector.

STATUS:
- SELECTOR_COEFFICIENT_NORM_GATE: PASS_RELATIVE_TO_BASELINE
- FULL_NOISE_GATE: STILL_NOT_RUN

Important caveat:
baseline MonomialGen rescales its masked factors, whereas CPB proposes no-rescale selectors before a subsequent ct-ct product. Similar mask norms do not prove intermediate decryptability.

## 3. One-Q-prime depth schedule

Current public 9-bit m=1 path:
- MaxLevel L19
- Step1 normalization -> polynomial input L18
- baseline ctP/basis -> L2
- retained x^(r/2) -> L4
- x^r -> L3
- grouped s=2 output -> L2
- downstream pointwise / leading / tail ends around L1/L0.

CPB structural levels:
- full r-basis at input-log2(r)
- x^(r/2) remains at input-(log2(r)-1).

Therefore with one 34-bit Q prime removed:
- MaxLevel L18
- Step1 normalization -> polynomial input L17
- CPB ctP -> L2
- x^(r/2) -> L3
- x^r -> L2
- grouped s=2 -> L1
- BatchLT may consume L2 input and normalize to L1
- pointwise / leading term can finish at L0
- m=1 skip-StC path already permits the output to finish at L0.

Thus the depth schedule itself closes with one fewer Q prime.

STATUS:
- ONE_Q_PRIME_REMOVAL: PASS_LEVEL_SCHEDULE
- ONE_Q_PRIME_REMOVAL_NOISE: UNVERIFIED
- SECURITY_DIRECTION: IMPROVES at fixed N because log(QP) decreases; correctness/noise is the unresolved constraint.

## 4. General CPBGen(s) primitive

Let:
- N = r*m,
- r=2^R,
- s=2^ell <= r,
- logical slots be indexed by (k,j) where 0<=k<r is the repetition coordinate and 0<=j<m is the message coordinate,
- input encrypts x_j at every (k,j).

Since r is even and N=rm, the two physical BFV/BGV rows correspond exactly to:
- row0: 0 <= k < r/2,
- row1: r/2 <= k < r.

Thus one physical RowRotation swaps the two repetition-coordinate halves simultaneously for every j; it never mixes different logical messages.

### State invariant

For i>=0, define:
- B_i(x_j)=(1,x_j,...,x_j^(2^i-1))
- a_i(x_j)=x_j^(2^i).

Maintain C_i such that:
- on row0, for every j, B_i(x_j) repeats over the repetition coordinate;
- on row1, every copy of message j equals a_i(x_j).

Initialization:
- row0 = 1,
- row1 = x_j,
obtained with one row selector multiplication and plaintext addition.

### Recurrence

For i < ell:
construct F_i from:
- tau(C_i), where tau is physical row-swap,
- C_i,
- public dyadic row0 masks,
- public row1 mask,
- plaintext ones.

On row0:
- first half of every 2^(i+1)-block: factor 1;
- second half: factor a_i(x_j), taken from tau(C_i).

On row1:
- factor a_i(x_j), taken from C_i.

Then one ct-ct multiplication C_i*F_i gives:
- row0 basis B_(i+1)(x_j);
- row1 auxiliary a_(i+1)(x_j).

This holds simultaneously for all j.

### Output when s<r

Because s divides r/2, after ell recurrences row0 already contains the desired B_ell pattern repeated across row0. Row1 contains x_j^s.

One final row-swap plus row masks copies row0's basis pattern into row1 with no ct-ct multiplication and no additional depth.

Output:
for every repetition coordinate k and message j,
y[k,j]=x_j^(k mod s),
which matches the 2026/975 MonomialGen layout.

### Output when s=r

After ell-1 ordinary recurrences:
- row0 contains powers 0..r/2-1;
- row1 contains x_j^(r/2).

A special final ct-ct step uses tau(C) on row1 to multiply the retained x_j^(r/2) by powers 0..r/2-1, producing powers r/2..r-1 directly.

Thus the full r-power basis is produced in ell ct-ct multiplications.

### Auxiliary output

The required x_j^(s/2) ciphertext is present in row1 immediately before the last basis-expansion multiplication and can be copied without a homomorphic operation.

## 5. Complexity comparison

For s=2^ell and ell>=2:

Baseline 2026/975 MonomialGen:
- ct-ct: 2ell-2
- pt-ct masked multiplications: ell, with rescale
- depth: ell+1
- rotations: 0

CPBGen:
- ct-ct: ell
- row automorphisms: ell if s=r, ell+1 if s<r
- selector pt-ct: O(ell), approximately two per recurrence, intended no-rescale
- depth: ell
- one RowRotation Galois element reused at multiple levels

Structural delta:
- saves ell-2 ct-ct operations,
- saves one multiplicative level,
- pays O(ell) row automorphisms and additional no-rescale selectors.

For ell<=2 the operation-count advantage is absent; use the original method.

## 6. Author benchmark-wide ct-ct reduction

Using the author's eight current benchmark settings:

| Setting | r | s=d/r | first Monomial saving | second Monomial saving | total ct-ct saving |
|---|---:|---:|---:|---:|---:|
| 9-bit m=1 | 32768 | 2 | 13 | 0 | 13 |
| 9-bit m=128 | 256 | 256 | 6 | 6 | 12 |
| 12-bit m=1 | 65536 | 16 | 14 | 2 | 16 |
| 12-bit m=64 | 1024 | 1024 | 8 | 8 | 16 |
| 14-bit m=1 | 65536 | 64 | 14 | 4 | 18 |
| 14-bit m=32 | 2048 | 2048 | 9 | 9 | 18 |
| 16-bit m=1 | 65536 | 128 | 14 | 5 | 19 |
| 16-bit m=16 | 4096 | 2048 | 10 | 9 | 19 |

Therefore CPB is not a single-ciphertext-only trick. It applies to the first and, when profitable, second monomial-generation stages across the complete benchmark family.

## 7. Attempted automorphism/relinearization fusion

Let canonical secret be s and row-swap secret be t=tau(s).

If row-swap key switching is delayed, a CPB factor has generic secret basis:
F = f0 + f_s*s + f_t*t.

Multiplying canonical C=c0+c1*s by F produces terms under:
- 1
- s
- t
- s^2
- s*t.

Thus the noncanonical source-secret monomials are generically:
- t
- s^2
- s*t.

The eager implementation instead:
1. key-switches t -> s for the automorphism;
2. multiplies under s;
3. relinearizes s^2 -> s.

So eager needs two source-secret switch classes.

Naively deferring the automorphism switch creates three source-secret classes, not fewer.

Additionally, hybrid/generalized key switching already supports accumulating multiple switched terms in the extended QP basis before a single ModDown/division-by-P. Therefore "share one final ModDown across multiple source-key terms" is established key-switching technique rather than a new CPB contribution.

Decision:
- NAIVE_AUTOMORPHISM_RELIN_FUSION: FAIL_NO_SWITCH_COUNT_REDUCTION
- SHARED_MODDOWN_FUSION_NOVELTY: FAIL_PRIOR_ART
- WILD_KEY_BASIS_ROUTE: PARK

Do not spend further BOOT effort on this fusion unless a CPB-specific algebraic cancellation is found.

## 8. Prior-art status after generalization

Known nearby ideas:
- repetitive/sparse packing preserves rotation structure;
- CKKS/HE work uses spare SIMD slots, masks, and rotations extensively;
- IBM root-product polynomial-evaluation patent uses duplicated x, known roots, rotations and multiplications;
- Okada-Player-Pohmann and Zhao et al. use within-slot extension-field/Galois structure to lower multiplication counts.

No source found in this gate directly gives:
- exact arbitrary finite-field LUT support,
- fully split rank-1 BFV/BGV slots,
- no polynomial factorization / no extension-field slot assumption,
- a dyadic co-packed basis recurrence matching 2026/975 sparse repeated layout,
- 2log(s)-2 -> log(s) ct-ct reduction while retaining x^(s/2).

Therefore:
- BROAD_SIMD_ROTATION_IDEA: PRIOR ART
- EXACT_CPBGEN_COLLISION: NOT_FOUND
- NOVELTY: STILL UNCLEAR, REQUIRES DEEPER SOURCE SEARCH

Full 2026/1089 text is still source-blocked in the configured ePrint path, so abstract-level non-collision is not enough for a final novelty claim.

## 9. Updated candidate assessment

CPB / CPBGen status:
- ALGEBRAIC_CORRECTNESS: PASS
- GENERALIZATION_TO_BATCHED_975_LAYOUT: PASS
- CTCT_COUNT_REDUCTION: PASS
- DEPTH_REDUCTION_BY_ONE: PASS
- ONE_Q_PRIME_LEVEL_SCHEDULE: PASS
- SELECTOR_RELATIVE_COEFFICIENT_NORM: PASS
- FUSION_STRENGTHENING: FAIL / PARK
- NATIVE_CORRECTNESS: NOT_RUN
- NATIVE_NOISE: NOT_RUN
- NATIVE_SPEED: NOT_RUN
- EXACT_NOVELTY: UNCLEAR
- CURRENT_VALUE: PROMISING_THEORY_BROAD / NATIVE_AND_NOVELTY_GATES_REQUIRED

It still does not supersede B145+B152 and does not alter B157.
