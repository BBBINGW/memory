# PURE-FHE P0-PRESCOUT-64 — Sparse-Defect Carry Factorization for General A2D

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-64
LATEST_COMPLETED: P0-PRESCOUT-64
NEXT_ITERATION: P0-PRESCOUT-65 NOT_STARTED
STATUS: PASS_STRUCTURAL_CORRECTNESS / PASS_P384_SOURCE_COST_GATE / PRIOR_ART_PARTIAL / NO_NATIVE_IMPLEMENTATION
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Source-selected problem

Primary source:

Jiaming Liu, Shihe Ma, Anyu Wang, Xiaoyun Wang,
"High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping,"
supplied as papers/supplied/2026-1869.pdf.

The paper's general arithmetic-to-digit conversion (A2D) uses exactly two functional bootstrap calls, followed by a finite-state carry computation.

For fixed candidate lambda and carry states c,c' in C, the second FBS outputs transition indicators

  1[f_{j,lambda}(c)=c']

for every radix position j.

The carry functions satisfy

  f_{j,lambda}(c)
    = ceil((c-a_j-lambda alpha_j)/B_j)

up to the paper's final-position radix convention.

The source composes these transition relations by one-hot relation/matrix composition:

  1[f_{i:j,lambda}(c)=c'']
    = sum_{c'} 1[f_{i:m,lambda}(c)=c']
                  1[f_{m+1:j,lambda}(c')=c''].

Appendix C.2 therefore charges, per doubling level,

  |Lambda| |C|^3

ciphertext-ciphertext multiplications.

## 2. Initial sparse-polynomial attempt: FAIL

An initial attempt tried to replace the source Curve25519 polynomial with

  F*(X)=X^256-X^255-2X^4+13,

which satisfies exactly

  F*(2)=2^255-19.

The source arithmetic-growth metric is

  mu(F)=max_l sum_{k=0}^{2d-2} n_k |c_{k,l}|,

where X^k mod F = sum_l c_{k,l} X^l.

Exact integer recurrence reproduces the paper's source value

  mu(F_25519)=2508

for its current Curve25519 polynomial.

For F* the same exact recurrence gives

  mu(F*)=424581,

about 169.3x worse.

Therefore the naive "make F sparse to make A2D sparse" replacement is killed before root-conditioning work.

A broader signed-carry recoding experiment also showed a sharp tradeoff: cancelling many radix-32 block coefficients alpha_j through F -> F+(X-2)H quickly increases mu(F). This is evidence, not a global impossibility theorem.

## 3. Key source observation: P-384 is already defect-sparse

Use the source P-384 defining polynomial at b=2:

  F_384(X)
    = X^384 - X^128 - X^96 + X^32 - X^2 + 3.

Take the general-A2D radix

  B=32=2^5,
  s=5,
  ell=ceil(384/5)=77.

Define, exactly as the source,

  alpha_j = sum_r 2^r f_{5j+r}

over the coefficients f_i of F_384 below degree 384.

Exact calculation gives only four nonzero blocks:

  (j,alpha_j)
    = (0,-1),
      (6, 4),
      (19,-2),
      (25,-8).

All other 73 blocks have

  alpha_j=0.

Therefore their local carry maps

  f_{j,lambda}

are INDEPENDENT OF lambda.

This property is already present in the source polynomial; no new defining polynomial is required.

## 4. Concrete source state sizes

Appendix B.2 gives the P-384 post-refresh overflow bound

  ||I'||_infty <=17.

Since p384 < 2^384, kappa=0.

Hence Appendix C.1 gives

  Lambda={-17,...,17},
  |Lambda|=35.

Using the Appendix-C.1 carry interval and the four alpha values above:

- ordinary B=32, alpha=0 blocks need outgoing carry set {-1,0,1}, size 3;
- j=0, alpha=-1: size 5;
- j=6, alpha=4: size 7;
- j=19, alpha=-2: size 5;
- j=25, alpha=-8: size 11;
- the final partial B=16 block has alpha=0 and needs size 5.

The source instead takes the global union

  C={-5,...,5},
  |C|=11

for all positions and all candidates.

The 11-state worst case is driven by one defect block.

## 5. Primary hypothesis H64

Exploit the sparse set

  D={j:alpha_j !=0}

as candidate-dependent defects.

Between defects, local carry transition relations are lambda-independent.

For each maximal common segment S_t:

1. compute all prefix transition relations inside S_t ONCE;
2. compute its full transfer relation G_t ONCE;
3. for each lambda, cross only the lambda-dependent defect relation D_t^(lambda);
4. use the shared prefix relations to recover every intermediate carry in the following common segment.

Thus candidate dependence is paid only at the defects and at applications of shared segment maps, not at every radix position and every carry-composition level.

This is an exact algebraic refactor of the same deterministic automaton.

## 6. Exact correctness factorization

Let a common segment be positions a,...,b with alpha_j=0.

Define its prefix maps

  P_{a:j}=f_j o ... o f_a,

and full map

  G=P_{a:b}.

These maps are independent of lambda.

If x_lambda is the encrypted carry entering the segment, then all internal carries are

  c_{j+1,lambda}=P_{a:j}(x_lambda).

The collection of P_{a:j} can be represented as encrypted one-hot relation matrices packed across the segment positions.

A single matrix-vector application between:
- the encrypted one-hot vector for x_lambda, and
- the packed prefix-relation entries

recovers all positions of that segment simultaneously.

Therefore no intermediate carry is lost.

### [TOY_EXECUTED]

An exact finite-state simulation used:
- 77 positions;
- defects at {0,6,19,25};
- the source-shaped state sizes 5,7,5,11 and ordinary size 3;
- 35 candidate labels;
- independently generated deterministic local maps.

For every lambda and every one of the 77 positions, the factorized segmented algorithm produced exactly the same carry as direct sequential composition.

This validates the factorization independently of CKKS/noise.

## 7. Source baseline carry cost

Appendix C.2 gives, for the relation composition alone,

  |Lambda| |C|^3 ceil(log2 ell).

For P-384:

  |Lambda|=35,
  |C|=11,
  ell=77,
  ceil(log2 ell)=7.

Thus

  35 * 11^3 * 7
    = 326095 CMult.

This excludes later candidate-selection work, which is mostly unchanged and much smaller.

## 8. Conservative factorized schedule

Use four lambda-dependent defects followed by four lambda-independent common segments:

  j=0  -> positions 1..5,
  j=6  -> positions 7..18,
  j=19 -> positions 20..24,
  j=25 -> positions 26..75,

and handle final position 76 separately.

A conservative ciphertext-multiplication accounting that does NOT assume aggressive cross-lambda SIMD packing is:

### Shared segment-prefix construction

Build the common prefix maps once.

Bounding each segment independently with its actual defect-output domain gives at most about

  1116 CMult

for all shared prefix relations.

### Per lambda

Construct lambda-dependent defect+segment supermaps and all boundary/internal states.

A conservative count is about

  498 CMult per lambda.

For 35 candidates:

  35*498 =17430.

Including the shared work:

  17430+1116 =18546 CMult.

Hence the source-shaped carry-composition reduction is at least

  326095 /18546
    ~=17.58x.

This count explicitly includes:
- defect relation applications;
- supermap construction;
- prefix composition among superblocks;
- recovery of expanded defect states;
- recovery of every internal common-segment carry;
- terminal carry.

It does not hide intermediate carries needed for digit reconstruction.

## 9. Multiplicative depth

The source carry composition needs

  ceil(log2 77)=7

multiplicative levels.

The conservative factorized schedule can be arranged as:

1. defect/common full-map composition;
2-3. prefix composition over the three noninitial 3-state supermaps;
4. apply the initial vector to obtain all superblock boundary states;
5. recover expanded defect states;
6. apply shared segment-prefix maps to recover all internal carries.

The terminal transition is not on the critical path beyond this bound.

So the carry stage needs about

  6 levels,

not more than the source's 7.

The claimed CMult reduction is therefore not obtained by spending extra multiplicative depth.

## 10. Second-FBS output count

Source Appendix C.2 says the second bootstrap returns

  |Lambda| (|C|^2 + |C|(1+h_kappa))

ciphertexts.

For P-384:
- h_kappa=0;
- |Lambda|=35;
- |C|=11.

Thus:

  35(121+11)=4620 outputs.

Under heterogeneous state sets and sparse defects, a conservative construction needs roughly:

- 33 shared B=32 common-transition outputs;
- 15 terminal B=16 transition outputs;
- 33 defect-transition outputs per lambda, sufficient for the union of the four defect shapes;
- 5 final-candidate check outputs per lambda.

Total:

  33+15+35(33+5)
    =1378 outputs.

Reduction:

  4620/1378
    ~=3.35x.

This does not yet exploit omission of one outgoing indicator, candidate-axis SIMD packing, or any compact-state encoding.

## 11. Prior-art boundary

### ePrint 2026/1840

"Efficient Homomorphic Arithmetic Logical Units with O(1) Bootstrapping"
already gives compact parallel propagation for BINARY carries.

It encodes three binary-carry behaviors and combines them with one CMult per doubling step.

Therefore:

  "binary carry does not need a 2x2 one-hot transition matrix"

is NOT novel.

H64 is different:
- it targets the general arbitrary-modulus A2D of 2026/1869;
- it retains the lambda-candidate dimension;
- carry state is not globally binary (P-384 source bound reaches 11 states);
- it exploits sparse lambda-dependence induced by the defining polynomial;
- it uses shared common-segment prefix automata plus heterogeneous state sets.

### ePrint / supplied 2026/1836

The large-prime ALU paper uses canonicalization, 3-to-2 compressors, carry-lookahead, overflow wrapping, and special prime-modulus reductions.

No candidate-lambda sparse-defect automaton factorization was found.

### Web search

Targeted current searches for arithmetic-to-digit carry composition, sparse defining-polynomial carry dependence, and segmented homomorphic carry propagation did not surface this construction.

This is only negative evidence.

Therefore:

  NOVELTY: NOT_ESTABLISHED.

## 12. Important remaining risks

1. Whole-system value:
   the second multi-value FBS is still large even after reducing its output count to about 1378.

2. Noise:
   fewer CMult and one less depth strongly suggest no worse leveled-noise budget, but the altered matrix/vector schedule needs an explicit CKKS error recurrence.

3. Memory:
   thousands of FBS outputs may still dominate memory and make the general P-384 A2D unattractive.

4. Generality:
   the gain is strongest when the defining polynomial has sparse radix-block alpha_j.
   Curve25519's current b=2 polynomial is dense and does not receive the same benefit.

5. Novelty:
   finite-state scan factorization is a broad algorithmic concept; a stronger literature audit is required before claiming a cryptographic contribution.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-64

STATUS:
PASS_STRUCTURAL_CORRECTNESS /
PASS_P384_SOURCE_COST_GATE /
PRIOR_ART_PARTIAL /
NO_NATIVE_IMPLEMENTATION /
HUMAN_REVIEW.

RESULT:
- Naive sparse replacement of Curve25519's defining polynomial fails the source arithmetic-growth metric.
- The source P-384 polynomial itself has only four lambda-dependent radix-32 blocks out of 77.
- Factoring the general A2D carry automaton into shared lambda-independent segments and four candidate-dependent defects exactly preserves all carries.
- Conservative source-shaped counts reduce carry CMult from ~326095 to ~18546 (~17.6x), while reducing carry depth from 7 to about 6.
- The second-FBS transition/check output count falls from 4620 to about 1378 (~3.35x) before more aggressive packing/compression.

CODEX_REQUIRED:
NO.

NEXT_TEST P0-65:
Do a cheapest whole-system value/noise gate before any implementation.

1. Bound CKKS noise for the rectangular relation-matrix/vector products under the source scale and level parameters.
2. Estimate memory for 1378 second-FBS outputs and determine whether this still dominates.
3. Use source/neighboring measured FBS and CMult timings only as a conservative latency proxy.
4. Compare against 2026/1836 prime-modulus A2B and the source's Montgomery alternative for the same P-384 conversion goal.
5. KILL if the residual FBS-output/memory term dominates so strongly that a 17.6x carry reduction cannot change the system conclusion.
6. Only if P0-65 passes should an implementation/Codex task be considered.

STATE_UPDATE:
YES — this finding only.
