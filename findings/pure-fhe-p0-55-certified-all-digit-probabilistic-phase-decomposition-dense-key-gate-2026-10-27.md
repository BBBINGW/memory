# PURE-FHE P0-PRESCOUT-55 — Certified All-Digit Probabilistic Phase Decomposition for Dense Fixed-Weight Keys

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-55
STATUS: PASS_ALL_DIGIT_TAIL_CERTIFICATE / PASS_DENSE_FIXED_WEIGHT_PARAMETER_GATE / HUMAN_REVIEW_NOVELTY_SECURITY_AND_INPUT_DISTRIBUTION
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## Primary falsifiable hypothesis

The probabilistic phase-width idea sketched in Schild–Abidin–Preneel ePrint 2026/537 can be made rigorous for EVERY radix digit, not just digit 0, without modeling the borrow process, by using only the range of the public b-digit.

With a quantile-based global correction shift P, this should support a dense fixed-Hamming-weight binary LWE secret in a single PhaseDecomp chain, avoiding the paper's Gamma-block dense-key fallback while preserving exact phase recombination.

Smallest decisive test:
1. derive a borrow-independent all-digit tail bound;
2. exhaustively verify exact recombination on a small instance with arbitrary borrows;
3. test one source-shaped dense parameter point with a rigorous Chernoff bound at total failure <=2^-128.

No native implementation or performance benchmark is authorized or needed at this stage.

## Primary source

Leonard Schild, Aysajan Abidin, Bart Preneel,
"On Phase Decompositions with Applications to Digit Decomposition,"
ePrint 2026/537, revision dated 2026-10-25.

Verified full PDF acquired from the eprint.iacr.asia mirror, 17 pages.
Relevant source facts:
- Algorithm 1 PhaseDecomp, physical p.4.
- Theorem 1: for binary secret Hamming weight <=beta and P=(alpha-1)beta, every pseudo-phase lies in [0,(alpha-1)(beta+1)] and recombines exactly.
- Algorithm 3 DigitDec, physical p.9: one blind rotation per digit plus l-1 exact exponent truncations.
- Section IV-A(c), physical p.13: dense keys are handled by partitioning indices into Gamma blocks, decomposing independently, and homomorphically adding digit vectors; the authors state total work grows linearly in Gamma and is competitive only for moderate weight.
- Section IV-A(d), physical p.13: for digit 0, if mask a is uniform modulo q=alpha^l, the mask digits are independent uniform and the overflow distribution is exact. For digits i>=1 the paper says b-digits depend on borrows and "we heuristically assume the same distribution."
- The paper explicitly leaves a full probabilistic treatment, including variants of rounding/modulus/key distributions, to future work.
- Table II, physical p.14: deterministic efficient condition alpha(beta+1)<=N; truncation cost is secondary relative to blind rotation.

This P0-55 does NOT claim the paper is incorrect. It replaces one heuristic step by a rigorous upper tail certificate and explores its parameter consequence.

## Generalized correction shift

Let q=alpha^l and c=(a,b) be an LWE sample under binary secret s of fixed known Hamming weight beta.

Algorithm 1 can use ANY integer correction P, not only P=(alpha-1)beta, provided the input body is first shifted by

  kappa = P * sum_{i=0}^{l-1} alpha^i
        = P * (q-1)/(alpha-1).

Let cbar = c - [0,kappa] mod q.
Write the coefficient-wise base-alpha decomposition

  cbar = sum_i alpha^i d_i

where d_i=(a_i,b_i) has every coordinate in [0,alpha-1].

Define the corrected pseudo-sample

  c_i = d_i + [0,P].

Then exactly

  sum_i alpha^i phi(c_i)
    = phi(cbar) + P sum_i alpha^i
    = phi(c) - kappa + kappa
    = phi(c) mod q.

So exact phase recombination is preserved for arbitrary P.

This is the same algebra as Theorem 1; only the choice of P changes.

## [DERIVATION] Borrow-independent all-digit identity

For each digit i define

  S_i = sum_{j:s_j=1} a_{j,i},

where a_{j,i} is the i-th base-alpha digit of the j-th public LWE mask coefficient.

Because the i-th pseudo-sample is d_i+[0,P],

  phi_i := phi(c_i)
         = b_i - S_i + P.

Crucially, regardless of ALL lower-digit borrows,

  0 <= b_i <= alpha-1.

Therefore deterministically

  P - S_i
    <= phi_i
    <= P - S_i + alpha - 1.        (A)

This holds for EVERY digit i.

No probabilistic model of b_i, no carry independence, and no heuristic about high digits is required.

If for some interval [L,U]

  L <= S_i <= U,

choose

  P = U.

Then by (A),

  0 <= phi_i <= U-L+alpha-1.

Thus the only random quantity that needs a tail bound is S_i.

## [DERIVATION] Uniform-mask distribution and global failure certificate

Assume the input LWE mask a is uniform in Z_q^n and q=alpha^l.

Then for every fixed digit i, the mask digits a_{j,i} are independent uniform variables on

  {0,...,alpha-1}.

For a fixed binary secret of Hamming weight beta,

  S_i = U_1 + ... + U_beta,
  U_j iid Uniform{0,...,alpha-1}.

The distribution is the same for every digit i.
Independence ACROSS digits is not needed because a union bound suffices.

Let

  mu = beta(alpha-1)/2.

For centered U, the exact moment generating function is

  M_alpha(lambda)
    = sinh(alpha lambda/2)
      / (alpha sinh(lambda/2)).

Hence for t>0,

  Pr[ |S_i-mu| >= t ]
    <= 2 exp(-I_{alpha,beta}(t)),

where

  I_{alpha,beta}(t)
    = sup_{lambda>0}
        { lambda t - beta log M_alpha(lambda) }.

For l digits,

  Pr[ exists i: |S_i-mu| >= t ]
    <= 2l exp(-I_{alpha,beta}(t)).       (B)

Choose integer interval

  L = ceil(mu-t) or a conservative floor,
  U = ceil(mu+t),

and set P=U.

On the good event, every pseudo-phase lies in

  [0, U-L+alpha-1].

If

  U-L+alpha-1 < N,

then all blind rotations are exact and avoid the X^N=-1 sign flip, for all digits simultaneously.

This resolves the paper's high-digit borrow dependence at the level needed for a correctness tail bound.

## [TEST] Exhaustive exact small-instance verification

Independent exact integer verification:

  alpha=4,
  l=3,
  q=64,
  n=2,
  arbitrary correction P=3.

Enumerated:
- all 64^2 public masks a,
- all 2^2 binary secrets s,
- all 64 possible phases.

Total:
  1,048,576 valid LWE arithmetic instances.

For each instance:
1. construct b=<a,s>+phi mod q;
2. apply the generalized global shift kappa=P sum_i alpha^i;
3. base-alpha decompose every ciphertext coefficient;
4. form corrected pseudo-samples;
5. verify
     sum_i alpha^i phi_i = phi mod q;
6. verify every digit satisfies
     P-S_i <= phi_i <= P-S_i+alpha-1.

Results:
  exact recombination PASS 1,048,576 / 1,048,576;
  all-digit deterministic interval identity PASS 1,048,576 / 1,048,576.

This test includes arbitrary borrow patterns in the body decomposition.
It is an arithmetic test, not a secure FHE benchmark.

## [PARAMETER GATE] Dense fixed-weight source-shaped point

Use the source's representative blind-rotation ring size and LWE dimension:

  N = 2^11 = 2048,
  n = 1800,

and take a fixed-weight dense binary secret

  beta = 900.

Take

  q = 2^64,
  alpha = 4,
  l = log_alpha q = 32.

Require TOTAL all-digit phase overflow probability <=2^-128.

By (B), it is enough that

  2l exp(-I(t)) <= 2^-128.

Since 2l=64=2^6, target rate is

  I(t) >= 134 ln 2.

Numerically optimizing the EXACT discrete-uniform MGF Chernoff exponent gives the smallest tested integer

  t = 452,

for which

  I(t)/ln2 - log2(64)
    ~= 128.156 bits.

The certified all-digit interval width is

  W = 2t + (alpha-1)
    = 904 + 3
    = 907
    < N=2048.

With
  mu=900*3/2=1350,
one may take approximately

  L=898,
  U=1802,
  P=U=1802.

Thus, under the uniform-mask and fixed-weight assumptions, a single PhaseDecomp chain supports beta=900 at total overflow probability below 2^-128.

For comparison, the paper's deterministic alpha=16 condition is

  16(beta_block+1) <= 2048
  => beta_block <= 127.

A beta=900 key therefore needs at least

  Gamma >= ceil(900/127) = 8

weight-bounded blocks if one uses deterministic weight partitioning based on actual fixed Hamming weight, before the paper's homomorphic signed-digit addition overhead.

The paper itself states that its dense-key fallback performs about Gamma*l blind rotations and Gamma(l-1) truncations for the decompositions, plus homomorphic additions, and that total work grows linearly in Gamma.

Our alpha=4 candidate uses l=32 blind rotations in one chain.
The simple source operation-count comparison is therefore:
- deterministic dense fallback, alpha=16: at least 8*16 = 128 decomposition blind-rotation calls, plus digit additions;
- certified probabilistic single-chain, alpha=4: 32 blind-rotation calls.

This is a 4x reduction in blind-rotation CALL COUNT relative to that simple fixed-weight block count, NOT a 4x runtime claim. Block dimensions, key-switch cost, truncation cost, parallelism, and concrete parameters must be matched before any speed claim.

## Stronger sanity point

If one formally plugs beta=1800 into the same alpha=4 Chernoff bound, the smallest tested integer t satisfying the same 32-digit total 2^-128 target is

  t=643,

giving

  W=2*643+3=1289 < 2048.

This shows the probabilistic width itself scales like sqrt(beta), not beta.

However this DOES NOT give a usable fixed P for an unknown random Hamming weight: the interval CENTER depends on beta.
The clean candidate therefore uses a fixed-weight binary secret distribution with public beta.
A Bernoulli secret with random unknown weight requires an additional key-weight tail or a different centering argument.

## Input-distribution limitation

The rigorous bound relies on a uniform LWE mask.

This is true for honestly generated fresh LWE ciphertexts by definition, but not automatically for arbitrary derived/adversarial ciphertexts.

Public ciphertext rerandomization by adding a fresh encryption of zero is known and already implemented in modern TFHE-rs; it can restore fresh-looking masks in settings where the required public encryption/rerandomization interface is available.

That is NOT claimed as a P0-55 primitive or novelty.

A follow-up must distinguish:
- honest fresh-input correctness;
- derived ciphertexts after key/modulus switching;
- adversarial/sIND-CPA^D inputs;
- rerandomized inputs and the added noise/key cost.

## Novelty status

The source itself already proposes probabilistic phase bounds for digit 0 and explicitly says high digits are treated heuristically. Therefore:
- "use average-case/probabilistic phase width" is NOT new;
- the new technical observation in this iteration is the borrow-independent inequality (A), which turns the digit-0 distribution into a rigorous ALL-DIGIT tail certificate with no borrow model;
- quantile-based arbitrary P is an immediate extension of the source correction algebra;
- the dense alpha=4 parameter point is derived, not source-reported.

This is potentially useful but not yet a publication claim.
A broader prior-art search found general average-case modulus-switch analyses and known TFHE rerandomization, but no exact match for this all-digit PhaseDecomp certificate. NOVELTY remains NOT_ESTABLISHED pending targeted search and author-version comparison.

## Security / systems blockers

1. Dense fixed-weight binary secret security must be estimated at the matched q,n,noise parameters. Do not assume beta=900 at n=1800 preserves the source's target security automatically.
2. The probability in this note is a PHASE-OVERFLOW correctness probability only. It must be combined with blind-rotation, truncation, key-switch, sample-extraction and restart noise/DFR.
3. The paper's accumulator-noise recurrence still grows with digit index. A dense-key phase certificate does not remove accumulator noise.
4. alpha=4 doubles digit count versus alpha=16. Full cost must include 32 blind rotations, 31 HomTruncTrace operations, output conversion, and any restarts.
5. The simple 128-vs-32 blind-rotation-call comparison does not account for different block dimensions or parallel execution.
6. Uniform-mask correctness scope must be pinned to the application. Rerandomization is known but adds its own key/noise/runtime.
7. Exact PairSwitch/other-track findings are unrelated; no cross-track write or merge occurred.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-55
STATUS: PASS_ALL_DIGIT_TAIL_CERTIFICATE / PASS_DENSE_FIXED_WEIGHT_PARAMETER_GATE / HUMAN_REVIEW
PRIMARY_HYPOTHESIS:
A quantile-shifted probabilistic PhaseDecomp can rigorously support dense fixed-weight binary keys in one chain by bounding every digit through the independent public mask digits, avoiding the source's Gamma-block dense fallback.

SMALLEST_TEST:
Borrow-independent phase inequality + exhaustive exact arithmetic + source-shaped Chernoff parameter gate.

EVIDENCE:
- verified full source PDF and screenshots;
- exact derivation;
- 1,048,576-instance exhaustive arithmetic verification;
- exact-MGF Chernoff numerical optimization.
NO native FHE experiment.

RESULT:
The mathematical core PASSES. High-digit borrows do not prevent a rigorous tail certificate because b_i is always in [0,alpha-1]. At N=2048,n=1800,beta=900,q=2^64,alpha=4, 32 digits fit inside N with total phase-overflow bound below 2^-128 using t=452 and interval width 907.

NOVELTY:
NOT_ESTABLISHED. The paper already suggests probabilistic bounds; this iteration rigorously removes its high-digit heuristic and derives a dense-key regime.

SECURITY/DFR:
UNCLEAR / NOT COMPLETE.

COMPLETE SPEED:
NOT CLAIMED.

CODEX_REQUIRED:
NO.

NEXT_TEST P0-56:
Before any implementation, do exactly one matched feasibility gate:
1. estimate security for fixed-weight dense binary beta=900 at source-compatible n,q/noise;
2. include the source Theorem 4 accumulator-noise recurrence and output conversion/restart cost;
3. compare total analytical work against the paper's Gamma-block dense fallback under matched block dimensions, not raw blind-rotation counts.
If security or full noise/cost erases the advantage, KILL.
If it survives, only then consider native implementation authorization.

STATE_UPDATE: YES — this finding only.
