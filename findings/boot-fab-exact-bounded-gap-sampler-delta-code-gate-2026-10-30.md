# BOOT — FAB exact bounded-gap sampler and delta/code-predicate gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 4/25

Status:
PASS_EXACT_DISTRIBUTION_PRESERVING_SAMPLER /
FAIL_REJECTION_IS_FUNDAMENTAL_KEYGEN_BARRIER /
FAIL_APPENDIXC_ESTIMATOR_MATCHES_AUTHOR_KEYGEN_PREDICATE /
FORMAL_RARE_CONDITIONING_SECURITY_REDUCTION_UNRESOLVED

## Reprioritization boundary

Independent of:
- Turn 1 parked SPRU stride=2 custom cryptanalysis;
- Turn 2 source-gated FHEW AKU matched-DFR repair;
- Turn 3 killed LFBS PRCA one-automorphism-per-level aggregation;
- completed B145–B157 one-FBS 4096-domain backend family.

This reopens FAB I120–I122 only because there is a NEW premise not tested there:
sample the EXACT SAME bounded-gap conditioned fixed-weight secret distribution directly, rather than changing to block-onehot or invoking a new entropic-RLWE theorem.

## Primary source and code provenance

Paper:
Antonio Guimarães and Hilder V. L. Pereira,
"Fast amortized bootstrapping with small keys and polynomial noise overhead",
CCS 2025, IACR ePrint 2025/686.
Research Notes full PDF mirror SHA256:
84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335,
34 physical pages, VERSION_UNVERIFIED.

Relevant paper text:
- §6.2 physical p22: sample sparse key then rejection-sample unless adjacent differences satisfy |d[i]| < B for 1 <= i <= h-1; security loss represented by delta.
- Table 4 physical p24: concrete binary/ternary key parameters and delta values.
- Appendix C physical pp33–34: delta estimated from 100,000 sampled keys.

Author public code:
antoniocgj/Fast-Amortized-Bootstrapping
commit 8938ab5bd42a80c93ed5ee4caef36efbb01bf7ef.

Relevant files:
- src/mosfhet/src/trlwe.c
- src/sparse_amortized_bootstrap.c
- scripts/b_estimator.py

## Primary hypothesis

The exponential expected rejection time found in I120 is NOT a fundamental key-generation barrier for the actual accepted FAB secret distribution.

Hypothesis:
the uniform fixed-Hamming-weight support conditioned on the bounded-gap predicate can be sampled EXACTLY in polynomial time, preserving the identical accepted-key distribution. The same dynamic program should also compute the acceptance probability and delta exactly.

Cheapest falsifier:
construct the exact counting recurrence, prove the backwards sampler is uniform, compare with exhaustive enumeration at small N, and apply the exact count to the source Table-4 parameter points.

No FHE ciphertext execution is required.

## 1. Exact support-counting recurrence

Let a support be

0 <= x_1 < x_2 < ... < x_h < N.

For the paper's interior-gap predicate,

x_j - x_(j-1) < B,  2 <= j <= h.

Define F_j(i) as the number of valid length-j support prefixes ending at x_j=i.

Base:
F_1(i)=1 for 0<=i<N.

Recurrence:
F_j(i)
 = sum_{k=max(0,i-B+1)}^(i-1) F_(j-1)(k).

Therefore

C_paper(N,h,B) = sum_i F_h(i).

Each row can be evaluated with a sliding window, so the arithmetic-operation count is O(Nh), not exponential rejection.

The count integers have O(h log N) bits, hence the bit complexity remains polynomial.

## 2. Exact uniform sampler

After computing all F_j rows:

1. sample x_h=i with probability F_h(i)/C;
2. for j=h,h-1,...,2, given x_j=i, sample predecessor
   k in [max(0,i-B+1),i-1]
   with probability F_(j-1)(k)/F_j(i).

For any valid support (x_1,...,x_h), its probability telescopes:

F_h(x_h)/C
* F_(h-1)(x_(h-1))/F_h(x_h)
* ...
* F_1(x_1)/F_2(x_2)
= 1/C.

Thus every accepted support is sampled with EXACTLY the same probability.

This is the same conditional distribution produced by ideal rejection sampling from a uniform fixed-weight support.

Using prefix sums and exact random integers, backward selection can be implemented without floating probabilities.

## 3. Author C implementation uses a STRONGER predicate

The real fixed-weight binary key generator is source-faithful:
src/mosfhet/src/trlwe.c::gen_sparse_array repeatedly samples indices in [0,N-1], rejects duplicates, and stops at exactly h distinct nonzero positions.

Therefore its support is uniform among all binomial(N,h) fixed-weight supports.

For ternary keys the accepted index order alternates sign. Conditional on a support, the accepted order is a uniform permutation, so the resulting sign assignment is uniform over assignments with the source-fixed numbers of +1 and -1. A distribution-preserving direct generator can sample the support first and then sample that sign partition.

However src/sparse_amortized_bootstrap.c::get_min_prec/check_key uses:
- previous=N before the highest support;
- every interior support difference;
- the final previous after the lowest support.

Hence the implemented predicate is

x_1 < B,
x_j-x_(j-1) < B for 2<=j<=h,
N-x_h < B.

This is stronger than the §6.2 extracted prose that mentions only the h-1 interior differences.

The same DP handles the code predicate by changing boundaries:

F_1(i)=1[i<B],

same interior recurrence,

C_code(N,h,B)
 = sum_{i: N-i < B} F_h(i).

It is still O(Nh), and the same telescoping proof gives an exact uniform sampler for the ACTUAL C rejection output distribution.

## 4. Appendix-C estimator is not sampling the actual key distribution/predicate

Pinned scripts/b_estimator.py uses

key = sorted([random.randint(0,N) for _ in range(h)])

and

diff_set =
  [key[i]-key[i-1] for i in range(1,h)]
  + [N-key[h-1]].

This differs from the real key generator/predicate in THREE ways:

1. random.randint(0,N) is inclusive, so it samples N+1 values and permits index N although the ring key has only coefficients 0,...,N-1.
2. draws are with replacement, so duplicate positions are allowed and the resulting object need not have Hamming weight h.
3. the estimator checks interior gaps and the right endpoint N-max(key), but omits the C predicate's left endpoint min(key).

Therefore Appendix C's Monte-Carlo delta is not an exact Monte-Carlo experiment for the actual author C rejection distribution.

This is a source-code/estimator mismatch, not an RLWE attack.

## 5. Exact small-case verification

Independent exhaustive subset enumeration matched the DP exactly:

N=8,h=3,B=3:
- paper interior count: 20 exhaustive = 20 DP
- code-boundary count: 1 exhaustive = 1 DP

N=10,h=4,B=4:
- paper interior count: 108 = 108
- code-boundary count: 61 = 61

N=12,h=3,B=5:
- paper interior count: 112 = 112
- code-boundary count: 32 = 32

No random/FHE assumptions enter these identities.

## 6. Exact delta for source Table 4

For a true uniform fixed-weight support,

delta = -log2(C / binom(N,h)).

Exact values for the ACTUAL C predicate are:

| Key | N | h | B | Table-4 delta | exact code delta | difference |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 2048 | 39 | 128 | 7.37 | 7.766568 | +0.396568 |
| B2 | 2048 | 42 | 128 | 6.16 | 6.409631 | +0.249631 |
| B3 | 4096 | 33 | 512 | 0.66 | 0.667694 | +0.007694 |
| B4 | 8192 | 27 | 1024 | 1.30 | 1.357886 | +0.057886 |
| B5 | 4096 | 34 | 512 | 0.58 | 0.594171 | +0.014171 |
| B6 | 8192 | 28 | 1024 | 1.15 | 1.205938 | +0.055938 |
| T1 | 2048 | 35 | 128 | 9.34 | 10.123563 | +0.783563 |
| T2 | 2048 | 38 | 128 | 7.81 | 8.289674 | +0.479674 |
| T3 | 4096 | 30 | 512 | 0.92 | 0.948976 | +0.028976 |
| T4 | 8192 | 25 | 1024 | 1.63 | 1.725528 | +0.095529 |
| T5 | 4096 | 32 | 512 | 0.73 | 0.750480 | +0.020480 |
| T6 | 8192 | 26 | 1024 | 1.46 | 1.530071 | +0.070071 |

All exact code-predicate delta values are slightly HIGHER than the table values, with maximum difference about 0.784 bit at T1.

For comparison, exact delta under the paper's interior-only predicate is LOWER than the Table-4 Monte-Carlo values, consistent with the fact that the actual C predicate adds endpoint restrictions.

## 7. Concrete impact

Expected rejection attempts under the actual code distribution are 2^delta.

Examples:
- B1: about 217.76 attempts;
- B2: about 85.01 attempts;
- T1: about 1115.57 attempts;
- T2: about 312.93 attempts.

These are finite and not catastrophic for the published concrete parameter points, but they are unnecessary.

If one treats each Table-4 lambda as "raw estimator result minus tabulated delta", replacing the tabulated loss by exact code delta would lower the listed adjusted lambda by exactly the difference column.

Conditional examples:
- B1: 128.9 -> about 128.50;
- T1: 128.3 -> about 127.52;
- T2: 129.9 -> about 129.42.

This conditional correction assumes every non-delta security-estimator input/result is unchanged. It is NOT an independent lattice-security re-estimation.

Several published values are already around 127.8–127.9, so sub-bit changes should not be presented as a catastrophic security break.

## 8. Asymptotic I120 repair and remaining security boundary

I120's family N=128t, h=8t, B=32 has exponentially small acceptance under uniform fixed-weight sampling.

Exact counting confirms delta grows linearly rather than being a finite-sample artifact; examples for the interior predicate:

h=8:   delta=1.4104
h=16:  delta=4.2043
h=32:  delta=10.4759
h=64:  delta=23.7778
h=96:  delta=37.4170
h=128: delta=51.2002

Therefore rejection sampling has exponential expected attempts, but the DP direct sampler still runs in polynomial time.

So:

FAIL "exponential rejection implies no efficient generator".

PASS exact efficient generator for the IDENTICAL conditioned distribution.

However this does NOT repair the black-box security reduction from ordinary unconditioned sparse-secret RLWE to the rare conditioned distribution.

If an adversary breaks the conditioned scheme with nonnegligible advantage epsilon, a reduction that waits for the event succeeds with epsilon * Pr(E) = epsilon * 2^-delta.

To preserve nonnegligibility by this simple conditioning reduction one needs delta=O(log lambda), not delta=Theta(lambda) or similar superlogarithmic loss.

Direct sampling changes key-generation efficiency, not the probability mass of E in the original distribution.

Thus:
- KeyGen asymptotic barrier: repaired.
- exact delta computation: repaired.
- accepted secret distribution: unchanged.
- ordinary-RLWE same-assumption asymptotic reduction for exponentially rare E: still unresolved.
- no claim that the conditioned secret distribution is insecure.

## 9. Novelty/value boundary

The dynamic program is standard constrained-combinatorial sampling, not a new cryptographic primitive.

Its research value is source-specific:
- it removes the implementation need for rejection without changing accepted keys;
- replaces Appendix-C Monte Carlo by exact delta;
- exposes a paper-script/C-keygen predicate mismatch;
- sharply separates the KeyGen issue from the actual remaining security-assumption issue.

This alone is unlikely to constitute a paper-level BOOT contribution.

A higher-value continuation would require a security argument for the same rare conditioned distribution, or a different secret family with a justified hardness/performance frontier. Do NOT return to known block-onehot I121 or failed BD20 theorem substitution I122 without a new premise.

## Verdict

PASS_EXACT_DISTRIBUTION_PRESERVING_SAMPLER.
FAIL_REJECTION_IS_FUNDAMENTAL_KEYGEN_BARRIER.
FAIL_APPENDIXC_ESTIMATOR_MATCHES_AUTHOR_C_KEYGEN_PREDICATE.
EXACT_CODE_DELTA_MAX_CORRECTION ~= +0.784 bits on Table 4.
FORMAL_RARE_CONDITIONING_SECURITY_REDUCTION = UNRESOLVED.

No native/Codex experiment is justified.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_CODEX_TASKS: none.

NEXT:
Do not spend Turn 5 implementing the sampler as an engineering task. Reprioritize to another BOOT bottleneck unless a new formal security mechanism for rare conditioned sparse Ring-LWE is identified.
