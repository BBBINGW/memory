# BOOT — ePrint 2026/1264 spectral-rank vs max-norm approximate-rank gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 17/25

Status:
PASS_MAXNORM_APPROXIMATE_RANK_IS_THE_FHE_RELEVANT_NOTION /
FAIL_SPECTRAL_THRESHOLD_AS_MINIMAL_RANK_CHARACTERIZATION /
PASS_EXPLICIT_SQRT_P_RANK_GAP_COUNTEREXAMPLE /
PASS_LRMT_COMPATIBLE_GENERAL_OUTER_PRODUCT_EVALUATION /
NO_SOURCE_THEOREM_1_MATH_ERROR /
NEW_LRMT_OBJECTIVE_KEEP

## Context

Turn 16 parked the direct post-Truncate arbitrary-M transfer because the boundary equation tightens the first-FBT coefficient-error envelope by 1+delta/D.

The independent 2026/1836 fused arbitrary-prime 5->4 candidate remains the strongest BOOT survivor but its native task is execution-blocked in this runtime:
BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.

This turn reprioritizes to:
Zhihao Li, Xuan Shen, Cheng Hong, Ruida Wang, Xianhui Lu, Tao Wei,
"The Power of Low Rank: Fast CKKS Functional Bootstrapping for High-Precision Lookup Tables",
supplied paper papers/supplied/2026-1264.pdf, Git blob 6f1d2330176bf4add587118b8c4cd274b8a576c7.

## Primary hypothesis

The LRMT-FBT spectral criterion
  sigma_{r+1}(M_f) <= epsilon
characterizes the minimum rank needed for FHE-correct LUT evaluation at the paper's entrywise correctness threshold epsilon=1/(2P).

Cheapest decisive falsifier:
construct a valid normalized LUT matrix whose rank-r approximation is entrywise within epsilon for very small r, while every spectral truncation criterion sigma_{r+1}<=epsilon forces r to be asymptotically much larger.

## Source facts

For P=alpha*beta, the paper reshapes
  M_f[i,j]=f(i beta+j).

The encrypted selectors are one-hot:
  delta_MSD=e_i,
  delta_LSD=e_j.

Thus evaluation returns exactly one selected entry:
  delta_MSD^T M delta_LSD = M[i,j].

The paper correctly proves in Theorem 1 that for truncated SVD:
  |M[i,j]-M_r[i,j]| <= ||M-M_r||_2 = sigma_{r+1}(M).

This is a sufficient entrywise error bound.

The paper then uses epsilon=1/(2P) as the CKKS correctness threshold and defines/names numerical rank through the singular-value threshold sigma_{r+1}<=epsilon. Its surrounding discussion treats the singular spectrum as determining the attainable rank reduction / whether acceleration is feasible.

## 1. Relevant optimization metric

Because the selectors are one-hot, the deterministic LUT approximation error is exactly

  max_{i,j} |M[i,j]-A[i,j]| = ||M-A||_max.

Therefore define the FHE-relevant approximate rank

  r_max(epsilon;M)
    := min { rank(A) : ||M-A||_max < epsilon }.

This is distinct from the spectral-threshold rank

  r_spec(epsilon;M)
    := min { r : sigma_{r+1}(M) <= epsilon }.

Eckart-Young establishes optimality of truncated SVD in spectral/Frobenius norm, not max-entry norm.

Theorem 1 remains mathematically correct:
  sigma_{r+1}<=epsilon => entrywise error<=epsilon.

But the converse is false in general.

## 2. Explicit asymptotic counterexample

Let
  P=m^2
with m a power of two, m>=32, and use the balanced reshape alpha=beta=m exactly as LRMT-FBT does at P=2^20.

Let H be a Sylvester Hadamard matrix of order m:
  H in {+1,-1}^{m x m},
  H H^T = m I.

Let
  epsilon = 1/(2P)=1/(2m^2),
  q=1/4,
and define the valid normalized LUT matrix

  M = (1/2) J + q epsilon H,

where J is the all-ones matrix.

Every entry of M lies in [0,1], since q epsilon << 1/2.

### Max-norm rank

Take the rank-one approximation
  A=(1/2)J.

Then
  ||M-A||_max = q epsilon = epsilon/4 < epsilon.

Rank zero cannot satisfy the threshold because every M[i,j] is about 1/2.

Hence

  r_max(epsilon;M)=1.

This approximation also leaves 3/4 of the approximation budget unused for homomorphic noise.

### Spectral criterion

Let
  E=q epsilon H.

Every singular value of E equals
  s=q epsilon sqrt(m).

M differs from E by the rank-one matrix (1/2)J.

Rank-one singular-value interlacing gives, for i=1,...,m-1,

  sigma_i(M) >= sigma_{i+1}(E)=s.

For m>=32 and q=1/4,

  s/epsilon = q sqrt(m) > 1.

Therefore

  sigma_i(M) > epsilon
for all i<=m-1.

Thus the paper's spectral threshold cannot certify any
  r <= m-2,

so

  r_spec(epsilon;M) >= m-1 = Theta(sqrt(P)).

At the paper's largest precision:
  P=2^20,
  m=1024,

the gap is

  r_max=1,
  r_spec>=1023.

Verdict:
PASS_EXPLICIT_SQRT_P_RANK_GAP_COUNTEREXAMPLE.

## 3. This is not a pathological-factor trick

The rank-one approximation
  A=(1/2)J
has a perfectly conditioned separable factorization

  A = g h^T,
  g=h=(1/sqrt(2)) * 1.

All factor entries have magnitude 1/sqrt(2), independent of P.

Thus the low max-norm rank is not obtained by using huge compensating factors that would obviously destroy CKKS precision.

## 4. Compatibility with LRMT evaluation machinery

Algorithm 2 computes a sum of rank-one separable terms.

Its homomorphic structure does not fundamentally require orthonormal SVD factors; for any public factorization

  A = sum_{k=1}^r g_k h_k^T,

the same selector semantics gives

  e_i^T A e_j
    = sum_k (g_k^T e_i)(h_k^T e_j).

Homomorphically:
- linearly combine row-selector ciphertexts with public g_k entries;
- linearly combine column-selector ciphertexts with public h_k entries;
- multiply the two ciphertexts;
- sum over k.

The operation count remains
  r(alpha+beta) public-scalar multiplications
and
  r ciphertext multiplications,
up to the same rescale pattern.

The SVD-specific noise bound in the paper uses orthonormality and singular values, so a general factorization requires a new factor-norm-aware noise analysis.

For the explicit counterexample, the rank-one factors are bounded constants, so no large-factor obstruction appears.

Verdict:
PASS_LRMT_COMPATIBLE_GENERAL_OUTER_PRODUCT_EVALUATION.

## 5. Precise scope of the source issue

NO_SOURCE_THEOREM_1_MATH_ERROR.

Theorem 1 is a valid sufficient inequality:
  entry error <= spectral residual.

The scientific gap is the stronger interpretation that spectral numerical rank determines the minimum rank / attainable compression for FHE correctness.

Because the actual LUT semantics selects one entry, the correct approximation problem is max-norm low-rank approximation, not spectral-norm low-rank approximation.

Therefore:

FAIL_SPECTRAL_THRESHOLD_AS_MINIMAL_RANK_CHARACTERIZATION.

The source spectral taxonomy remains useful as a sufficient/computable classification, but it is not complete as a characterization of whether low-rank FHE acceleration is feasible.

## 6. Exploratory concrete check (NOT used in verdict)

A private non-source-exact reconstruction of the paper's P=2^20 balanced LUTs over [-64,64] suggests that actual max-entry error of truncated SVD can cross epsilon one rank earlier than the sigma_{r+1} criterion for several smooth activations.

However, the paper's exact normalization/sampling details were not fully reconstructed in this turn, so this is PRESCOUT_ONLY and must not be cited as a source-exact benchmark result.

## 7. Research consequence

A new optimization objective is exposed:

  minimize rank(A)
  subject to
    ||M_f-A||_max <= epsilon_app
    and
    factor norms small enough for CKKS noise.

This is stronger and more FHE-specific than truncated SVD.

A publishable route would require BOTH:
1. a practical algorithm for max-norm / entrywise low-rank factorization with controlled factor norms;
2. real benchmark LUTs where it reduces rank/runtime beyond LRMT-SVD while preserving total CKKS error.

The artificial Hadamard counterexample alone is conceptual evidence, not a paper contribution.

## Verdict

PASS_MAXNORM_APPROXIMATE_RANK_IS_THE_FHE_RELEVANT_NOTION.
FAIL_SPECTRAL_THRESHOLD_AS_MINIMAL_RANK_CHARACTERIZATION.
PASS_EXPLICIT_SQRT_P_RANK_GAP_COUNTEREXAMPLE.
PASS_LRMT_COMPATIBLE_GENERAL_OUTER_PRODUCT_EVALUATION.
NO_SOURCE_THEOREM_1_MATH_ERROR.

AI_PROVISIONAL_CHOICE:
KEEP this as a new BOOT candidate.

Next highest-information gate:
reproduce one source-exact Class-B LUT matrix and solve/upper-bound the smallest max-norm rank with controlled factor norms. Kill if it gives no rank reduction over the source SVD selection; expand only if a real benchmark gains at least one rank without worsening noise enough to erase the runtime saving.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked.
