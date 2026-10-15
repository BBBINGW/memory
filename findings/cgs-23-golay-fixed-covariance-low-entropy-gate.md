# CGS-23 — Constant-rank Golay-pair covariance is correct, but Davis–Jedwab key support is exhaustible

**Date:** 2026-10-15. **Operating mode:** PI-selected one active FHE project via root `STATE.md` (no multi-instance track isolation). **Last completed before this iteration:** CGS-22.

**ITERATION:** CGS-23.
**PRIMARY HYPOTHESIS H-CGS23:** The publicly known binary Davis–Jedwab Golay complementary-pair family with `k=2` components can replace CGS-22's `k=n` signed-monomial lifted secret in a **practical standard-MLWE-secure low-storage threshold FHE**: (i) secret-independent `Sigma_s=2n I`, (ii) ordinary independently uniform public A, (iii) enough secret-key entropy for 128-bit security around ordinary n=1024..16384, (iv) no per-query conditional Gaussian, with otherwise source-like overhead.

**ONE cheapest decisive security test:** Compute the cardinality of the *specific named published family* and exhaustively test small `m` under a single independent-uniform-public-module sample with bounded error. If `|K| << 2^128` at relevant n, publicly enumerable secret candidates give a small-key brute-force distinguisher and the combined claim fails even if the Gram identity passes.

## Original source & prior art [FACT]

- **Okada, Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint 2025/409, https://eprint.iacr.org/2025/409. Actual full 40-physical-page MCP mirror previously read; PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **Algorithm 7 p29 and Lemma 7.1 p30** define `Sigma_s = sum_i Gram(s_i)` and private covariance-dependent per-session Gaussian `ζ∼R(D_{Z^n,σ0 sqrt(Bpub² I−Sigma_s)})`. Their key distribution `chi_mlwe`, singular-value lower bounds, underlying FHE, and adaptive simulation theorem cannot be reused without a new security reduction.
- **Davis and Jedwab 1999**, *Peak-to-mean power control in OFDM, Golay complementary sequences, and Reed–Muller codes*, IEEE Transactions on Information Theory 45 (1999), pp2397–2417. Standard binary (`h=1`) Davis–Jedwab ordered pair family of length `n=2^m` has exactly `m!·2^(m+2)` **ordered pairs**, using permutation/Boolean linear phases. This number is for the explicit published *GDJ family*, **NOT** the upper bound on every possible binary Golay pair.
- **Fiedler–Jedwab–Parker 2008**, *A multi-dimensional approach to the construction and enumeration of Golay complementary sequences*, Journal of Combinatorial Theory A 115:753–776, DOI https://doi.org/10.1016/j.jcta.2007.10.001. Counts/organizes known complementary construction classes, which are established communications mathematics prior art, not a new CGS innovation. The authors' page https://www.sfu.ca/~jed/Research/golay.html and the openly accessible text https://www.researchgate.net/publication/244955942_A_Framework_for_the_Construction_of_Golay_Sequences also state the `m!·2^{h(m+2)}` ordered-pair count.
- For broader special-secret security, see the *Hardness of Entropic Module-LWE* study https://www.sciencedirect.com/science/article/pii/S0304397524001683 and small-secret LWE analysis https://link.springer.com/article/10.1007/s44007-024-00111-3. These works **do not supply a black-box standard-MLWE security reduction for the small, highly structured GDJ key distribution**. A high min-entropy bound alone would not prove hardness either.

## The exact positive identity [DERIVATION]

Work over `R=Z[X]/(X^n+1)`. Let `a,b ∈ {±1}^n` be binary *aperiodic Golay* sequences: for all `1≤d<n`,

```
C_a(d)+C_b(d)=0,
C_a(d)=sum_(j=0)^(n-1-d) a_j a_(j+d).
```

As ordinary Laurent polynomials, `a(X)a(X^{-1})+b(X)b(X^{-1})=2n` **exactly**. In negacyclic ring representation, transpose of the multiplication matrix corresponds to `X→X^{-1}`; thus

```
Sigma_(a,b) = mat(a) mat(a)^T + mat(b) mat(b)^T
            = mat(2n) = 2n I_n.
```

This is a genuine **k=2**, key-independent covariance and nonnegative definite matrix. It removes the covariance-dependent *sampling distribution* in an appropriately redesigned scheme. It does not establish the source's independent-secret assumption or a secure short-share FHE. Moreover, exact sum-of-Gram being nonsingular does not alone give the paper's **individual** `σ_min(mat(a)),σ_min(mat(b)) ≥ c` lower bounds with practical c. That condition needs its own check.

## Published Davis–Jedwab binary family and entropy [FACT + DERIVATION]

For `m≥1,n=2^m`, choose permutation `π∈S_m`, independent bits `c_1,...,c_m,c,c'∈F_2`; for Boolean coordinate `x=(x_1,...,x_m)`, set:

```
f(x)=sum_(j=1)^(m-1) x_(π(j))x_(π(j+1)) + sum_(j=1)^m c_j x_j  (mod 2)
a[x]=(-1)^(f(x)+c)
b[x]=(-1)^(f(x)+x_(π(1))+c').
```

Known Golay pair. Its parameter count and documented number of distinct ordered pairs is

`M_m=m!·2^(m+2)`; key entropy `H_∞(K)≤log₂ M_m=log₂(m!)+m+2=O(log n loglog n)`.

A biased sampler only reduces min-entropy, and a deterministic secret transform cannot increase the number of possible secret keys. **n=1024, m=10:** `M_10=14,863,564,800 < 2^34`, exactly `log2 M=33.7910611147` bits. `m=12,n=4096`: 42.8354552 bits; `m=14,n=16384`: 52.3432499 bits; `m=16,n=65536`: 62.2501405 bits. The first `m` for which this **particular family count** reaches `2^128` is `m=29`, `n=536,870,912`. This is a counting threshold only, not a 128-bit security proof at that dimension.

## Public-sample exhaustive distinguisher [DERIVATION, conditional on bounded noise]

Use ordinary independent-uniform module public components `A_1,A_2 ← U(R_q)`, `b=A_1a+A_2bkey+e`, with secret `(a,bkey)` from a PUBLICLY enumerable family `K` of size `M`. Here `bkey` avoids collision with the sample name. Let the error `e` have coefficients in `[-B,B]`, where `2B+1 < q`.

Attacker enumerates all `(a',b')∈K`, computes centered residual `r=b-A_1a'-A_2b'`, and accepts REAL if **any** candidate has every residual coefficient in `[-B,B]`. This takes `O(M·poly(n,log q))` ring operations, no advanced lattice algorithm.

For a REAL sample, the true key always passes (if noise bounded). For uniformly random sample `(A_1,A_2,u)`, for **each fixed candidate** the residual is uniform in `R_q` because u is independent uniform. Thus

```
Pr[accept RANDOM] ≤ M*((2B+1)/q)^n,
Distinguishing advantage ≥ 1−M*((2B+1)/q)^n.
```

This is rigorous under the stated bounded coefficient noise. With discrete Gaussian tails, the real acceptance becomes `≥1−δ_B` and advantage `≥1−δ_B−M*((2B+1)/q)^n`, where δ_B is a genuine tail bound that must be parameterized in a real security estimate. It is an **exhaustive-work upper bound** on concrete security, not a PPT mathematical impossibility for every asymptotic n and not an attack on ordinary non-GDJ secret distributions.

## One exact toy test [EXECUTED]

Script `/mnt/data/cgs23_golay_entropy_gate.py` SHA256 `15fcd9f4f046e90edc868b028adcc2defb36767812833d891afb19cd484d5f26`; JSON `/mnt/data/cgs23_golay_entropy_gate.json` SHA256 `033223fa2640c0360fb7cfb1af4dd5bb8358b516952e582474cd2b7f039ee851`. No real cryptosystem implementation or secure random seed.

- Exhaustive all GDJ parameterizations `m=1,2,3,4`: exact distinct ordered pairs `8,32,192,1536`, respectively. Checked ALL aperiodic autocorrelation equations; checked matrix covariance exactly for `m≤3`.
- Toy `m=3,n=8,q=257`, error coefficients independently sampled from `{-1,0,+1}`. For each of **100** independent deterministic seeded trials, generate two independent uniformly random public ring components, one secret from the 192-member family, and one sample `b=A_1a+A_2bkey+e`. Exhaustively compare all 192 candidates against the coefficient bound `B=1`: in **100/100** trials the true secret was the ONLY surviving candidate. This is a tiny parameter control test, not a statement about Gaussian security at n1024.
- For this toy, the *rigorous* uniform-sample union upper bound is `192*(3/257)^8≈6.61921×10^-14`; empirical uniqueness is consistent but does not establish this analytic probability.

## Outcome, novelty and synthesis

**CGS-23 named candidate FAIL** as a practical 128-bit-secure, standard-MLWE-grounded zero-Gaussian workaround. It provides a clean *mathematical* low-rank solution to the covariance equation; BUT the family secret support is disastrously small and publicly enumerable. No published theorem guarantees that this highly structured secret is as hard as the original source's MLWE distribution. Even a bigger Golay family would need its own entropy/hardness/individual-spectral-bottom bound and KeyGen/FHE circular security proof. The fixed-covariance identity and GDJ construction are prior art, not paper contributions.

**Critical scope:** This test does NOT upper-bound the number of *all possible* negacyclic complementary pairs; other unpublished/known constructions, quaternary/complex coefficients, randomized transforms, larger k or a genuinely different security assumption are not excluded. Nor does it rule out source-compatible secret-conditioned Gaussian PCFs with an entirely different interface. This iteration ONLY kills straightforward use of **named GDJ binary pair family**.

**STATUS:** PASS fixed k=2 Gram identity and exact enumeration; FAIL intended concrete-security/standard-MLWE-safe direct port; original CGS open, HUMAN_REVIEW.

**NEXT_TEST (CGS-24, only on PI next “继续”):** Given a single concrete **larger-entropy fixed-covariance** ring-secret family with k=2 or 3 (not standard GDJ), test whether it admits a non-enumerable key distribution and plausible standard-MLWE reduction at n≈1024 under source individual-invertibility and cost gates; OR if no concrete nontrivial construction, PARK covariance-flattening line and return to the original Gaussian conditional-correlation open problem / PI-selected other FHE issue. Check author latest paper 2026/957 full source before claiming novelty. One primary test only, do not repeatedly rediscover Golay identities.

**STATE_UPDATE:** YES: own finding, CGS detailed archive checkpoint, and root `STATE.md` as one active task. No changes to other projects.
