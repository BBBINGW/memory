# CGS-25 — Injective negaperiodic doubling gives exact 64-bit support at n=1024, 129-bit support only at n=32768

**2026-10-15** · Single PI-selected active research workflow (root `STATE.md`). Last completed CGS-24. **One hypothesis + one cheapest decisive test.**

**PRIMARY HYPOTHESIS H-CGS25:** A concrete efficiently sampleable high-entropy **binary rank-two negaperiodic-Golay (NGP)** secret family can be derived from the complete n=16 NGP set via repeated low-cost signed shift/involution doubling, achieving simultaneously:
(a) exact public source-style Gram covariance `2nI`, (b) a provable uniform keyspace min-entropy **>=128 bits at n=1024**, and (c) an immediately usable lower bound on each `σ_min(mat(s_i))` / plausible unchanged-source MLWE hardness.

**DECISIVE TEST:** Give the exact recursive algorithm, show injectivity and count its WHOLE image, not merely a biased sampler or heuristic lower bound. If the count falls below 2^128 at n=1024, the named 1024-dimension candidate FAILS independent of MLWE difficulty. Check the algebra with exact small-to-medium integer negaperiodic autocorrelation, then assess higher dimensions and singular values only as boundary conditions.

## Primary sources [FACT]

1. Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025 / ePrint **2025/409**, https://eprint.iacr.org/2025/409. Research MCP acquired and parsed all 40 physical pages, SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, **VERSION_UNVERIFIED**. The actual Section 7, **Algorithm 7 (physical p29), Lemma 7.1 (physical p30)** requires `Σ_s=Σ_i Gram(s_i)`, `χ_mlwe` small coefficientwise independent original secret distribution, and for **each** `mat(s_i)` a minimum singular value ≥ a usable source parameter `c>0`. It samples secret-shape conditional Gaussian padding `D_{Z^n,σ0 sqrt(Bpub²I−Σ_s)}` once per session. Merely making Σ public does NOT grant the original MLWE/FHE theorem under a replacement globally correlated secret distribution.
2. N. A. Balonin and D. Ž. Đoković, *Negaperiodic Golay pairs and Hadamard matrices*, arXiv **1508.00640**, https://arxiv.org/abs/1508.00640, original author text §3 Definitions 2–3 and Proposition 3. **Existing prior art:** product maps `GP_g × NGP_v → NGP_{gv}`, and in particular `NGP_v→NGP_{2v}`. The recursion below is an algebraically explicit shifted-involution variant of such a doubling phenomenon; **DO NOT CLAIM novel negaperiodic family or first constant-covariance insight**.
3. CGS-24 `findings/cgs-24-negaperiodic-golay-covariance-keyspace-gate.md`: complete exact enumeration of **557056=17·2^15** ordered NGPs at n=16, and numerical singular value gates. The small-n count is grounded by this executable enumeration, not asymptotic extrapolation.
4. Related newest author 2026/957, *Threshold FHE with Short Decryption Shares Without a Semi-trusted Server*, known public ACISP 2026 bibliographic source, BUT **the full original PDF retrieval was retried 2026-10-15 and BLOCKED** (IACR 403, ePrint mirror absent, arXiv exact-title unavailable). No claims about its detailed novelty overlap.

## An explicit **binary** doubling with independently chosen odd monomial phase [DERIVED]

Let `n=2^j`, `R_n=Z[Y]/(Y^n+1)`, and let an NGP `(a(Y),b(Y))` have all coefficients in `{±1}`, with `aa*+bb*=2n` mod `Y^n+1`, where involution `p*(Y)=p(Y^-1)`. Work in `R_(2n)=Z[X]/(X^(2n)+1)`; embed `Y→X²` (well-defined). Pick independent integer `t∈{0,...,2n−1}`, so `z=X^(2t+1)` ranges over ALL 2n distinct odd monomials modulo `X^(2n)+1`. Define:

```
A(X)=a(X²)+z b*(X²)
B(X)=b(X²)−z a*(X²).
```

The even coefficients of A,B are exactly a,b. The odd coefficients are a shifted/signed permutation of the inverse-polynomial coefficients of b,a, respectively; thus **ALL output coefficients remain ±1**. Involution is a ring automorphism. Expand:

```
AA*+BB*=[aa*+bb*+z a*b*+z^-1 ab]
        +[bb*+aa*−z b*a*−z^-1 ba]
       =2(aa*+bb*)=4n
```

in `R_(2n)`. Hence (A,B) is an NGP at length 2n with exact `Σ_(A,B)=4nI_(2n)`.

**Injectivity proof:** The even positions reveal input (a,b) uniquely. Given the input, the odd positions determine `z b*(X²)`. For n a power of two, `X^(2n)+1=Φ_(4n)(X)` is irreducible over Q, so the quotient over Q is a field and the nonzero `b*(X²)` is cancellable. Thus different odd monomials z yield different output pairs. At every level, exactly `2n` independent choices yield exactly as many distinct outputs. This is not a hypothetical random collision assumption.

## Exact entropy, not a heuristic [DERIVED]

Let `K_16` be the **full** 557056-member n16 ordered NGP set, which is fixed and efficiently enumerable once. Sample a uniform base pair in K16, and at each doubling independently select a uniform odd monomial shift. By injectivity, the output distribution on the explicitly generated family is exactly UNIFORM.

For n=2^m (m>=4),

```
|K_(2^m)| = |K_16| ⋅ ∏_(j=5)^m 2^j
          = 17 ⋅ 2^(15+Σ_(j=5)^m j).
H_inf[K_(2^m)] = log2 |K| = log2(17)+15+Σ_(j=5)^m j.
```

This is exact for THIS recursion, **not the set of all possible NGPs of length n**.

| n | exact min entropy |
| 1024 | 64.087462841 bits |
| 2048 | 75.087462841 bits |
| 4096 | 87.087462841 bits |
| 8192 | 100.087462841 bits |
| 16384 | 114.087462841 bits |
| 32768 | 129.087462841 bits |

At n1024, `K=17·2^60 ≈ 1.95997×10^19 < 2^65`, **FAIL 128-bit entropy** by nearly 64 bits. Thus an attacker with bounded-noise public MLWE samples can in principle enumerate no more than 2^64.087 candidates and perform a bounded-residual consistency check as in CGS-23, a concrete security-cost ceiling for this NAMED family, not a mathematical PPT no-go for all asymptotic n.

At n32768, `K=17·2^125` and the **unfiltered** full family with uniform sampling has `H∞≈129.087` bits. This passes ONLY a necessary support/min-entropy condition for potential 128-bit hardness; 128-bit **LWE/MLWE security is NOT proved**. In particular, recursively constrained highly structured secrets might admit vastly faster key recovery than exhaustive enumeration.

## One reproducible algebraic test [EXECUTED]

Self-contained Python script: `/mnt/data/cgs25_recursive_negaperiodic_entropy_gate.py`, SHA256 `89a975c682836b2e2936eb784be9903ea2a8d4d7edfce2714a2ddf66671ee4bb`. Exact JSON output `/mnt/data/cgs25_recursive_negaperiodic_entropy_gate.json`, SHA256 `7f40eb995c632ce5f242105930b90c292d26c541a07f4532bc1a550d7b6b9c5e`.

- Regenerated ALL 557056 length-16 ordered NGP pairs by exact NAF-signature enumeration.
- Checked exact one-step n16→32 map injective over ALL 32 possible odd shifts of one fixed base pair.
- Ran one independently seeded chain to each target n32,64,128,256,512,1024 and checked exact full INTEGRAL `NAF_A(d)+NAF_B(d)=0` at every sidelobe for each chain. All passed. This is a computation sanity check; the proof above covers every key.
- Sampled n1024 **25** chains and n32768 **30** chains, measured two individual polynomials' min singular values via FFT at roots `ζ^n=-1` (DOUBLE PRECISION, empirical only). n1024 20/25 had BOTH min singular values ≥1; observed smallest pairwise min ≈0.508. n32768 26/30 had BOTH ≥1; smallest min ≈0.327. **These sampled percentages do NOT establish asymptotic spectral lower bound, valid-key fraction, conditional min entropy or any FHE security**. Every individual binary polynomial is nonzero and invertible over the characteristic-zero cyclotomic field, but its smallest singular value can be very small; the original source's quantitative parameter c is not automatically reusable.
- Printed exact counts and proofs as JSON. Random generator is for reproducibility only, NOT cryptographically secure KeyGen.

## Constructive synthesis gate and novelty

We now have ACTUAL:
1. efficient ±1 binary secret pair generator at power-of-two n;
2. exact key-independent rank-2 Gram `Σ_s=2nI`;
3. unconditional injection/count theorem and 128-bit *entropy-support* threshold n32768.

Still MISSING:
1. at target n1024, the named recursion has H_inf only ~64: **FAIL**;
2. at n32768, a rigorous polynomially usable **minimum individual σ_min** bound over an efficient high-entropy (possibly filtered) subfamily (or a complete smoothing parameter and overhead accounting);
3. any credible hardness reduction for *this* recursively structured non-iid secret distribution from ordinary LWE/MLWE, plus FHE Eval/KDM/evaluation-key security, concrete q/noise/key size and the exact multi-session transcript simulator;
4. author 2026/957 full source for reliable novelty audit.

**Security warning:** Mathematically constant covariance does not imply encryption is pseudorandom or secure. This is not a new ThFHE scheme and it does not establish removal of O(LDec) under source assumptions.

## End of CGS-25

- **STATUS:** PASS recursive NG mathematical and exact entropy gate; **FAIL** H-CGS25's 128-bit-at-n1024 objective; **UNCLEAR** n32768 actual source security and spectral/noise viability; **HUMAN_REVIEW** parent CGS problem.
- **RESULT:** Explicit recursive family size `17·2^60` at n1024 (64.087 bits); `17·2^125` at n32768 (129.087 bits). Fixed Gram `2nI` at every level.
- **NEXT_TEST CGS-26 (PI next continue only):** ONE decisive security-vs-smoothing test at n32768: does the highly structured family admit a quantitatively bounded per-individual singular value **without sacrificing the >128-bit min entropy support**, AND can we identify an actual plausible standard (M)LWE hardness route? Prioritize an explicit polynomial-time/subexponential structural key recovery or certified spectral lower bound. If neither has support, **PARK covariance family and return to the original conditional-Gaussian PCF/primitive question** rather than deriving more simple Golay identities.
- **STATE_UPDATE:** YES to own CGS finding + CGS topic checkpoint + sole root `STATE.md`; scientific archive of other projects untouched.
