# CGS-24 — Negaperiodic (not aperiodic) Golay pairs are the exact low-rank fixed-Gram MLWE condition

**Date:** 2026-10-15. **Active single-task workflow:** Root `STATE.md` selects the current CGS research. Prior CGS-23 used only the standard *aperiodic* Davis–Jedwab Golay family and found a severe enumeration attack against that named small family. PI asked to continue. One primary hypothesis, one exact family-enumeration test.

**ITERATION:** CGS-24.
**PRIMARY HYPOTHESIS H-CGS24:** For binary ±1 ring secret keys of module rank **k=2** in `R=Z[X]/(X^n+1)`, the exact `Sigma_s=2nI` covariance condition is **negaperiodic** complementarity, strictly weaker than ordinary aperiodic Golay complementarity. The class is concretely >100x larger at n=16 and contains actual pairs with individual singular-value bound `σ_min(mat(a)),σ_min(mat(b)) >= 1`; therefore the particular Davis–Jedwab keyspace ceiling of CGS-23 cannot be generalized to *all* fixed-Gram rank-two families.

**ONE decisive exact test:** Exhaust all `(a,b)∈{±1}^{n}×{±1}^{n}` for n=2,4,8,16 via integer-valued negaperiodic autocorrelation signatures, compare with the full ordinary Golay subset, and check at n=16 whether at least one (and how many) NG pairs satisfy `σ_min≥1`. Numerically evaluated spectral thresholds supplement, not replace, exact integer covariance proof. This test assesses finite keyspace support and spectral feasibility, NOT 128-bit key entropy at n≈1024, MLWE hardness, FHE security, or uniqueness.

## Original paper grounding [FACT]

1. **Okada–Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint 2025/409, https://eprint.iacr.org/2025/409, original 40 physical-page MCP mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **Algorithm 7 physical p29 and Lemma 7.1 physical p30:** original secret-dependent covariance is `Sigma_s=sum_i Gram(s_i)`; KeyGen generates source `chi_mlwe` secrets and pre-shares Gaussian `D_(Z^n, sigma0 sqrt(Bpub² I − Sigma_s))` for every sid. Lemma7.1 also imposes individual nonzero lower-singular-value conditions on `mat(s_i)`. Replacing native secrets by ANY special NG family changes the key distribution and needs an independent source-security reduction and new FHE compatibility argument.
2. **N. A. Balonin and D. Ž. Đoković**, *Negaperiodic Golay pairs and Hadamard matrices*, arXiv 1508.00640, https://arxiv.org/abs/1508.00640, **HTML full original §§2–3**, notably §3 equations (6),(8),(10), Defs2–3. Defines aperiodic autocorrelation AF, negaperiodic NAF, binary NG-pairs; establishes `NAF_a(d)=AF_a(d)−AF_a(n−d)`, and negacyclic `mat(a)mat(a)^T = Σ_d NAF_a(d) N^d`. Importantly, ordinary Golay pairs are precisely intersection of periodic and negaperiodic sets. This entire combinatorial object is established prior art; identifying it as the mathematically exact source condition is our research audit/bridge, NOT a new sequence family.
3. **Ronan Egan**, *On equivalence of negaperiodic Golay pairs*, Designs, Codes and Cryptography 85 (2017) 523–532, DOI https://doi.org/10.1007/s10623-016-0320-6. The web-indexed publicly available preprint excerpt for Table2 reports n(8)=557056 NGP pairs of length 16, independently corroborating our exhaustive count; full PDF Table2 not independently visually authenticated this iteration. For rigorous local claim we rely on reproduced full-exhaustion test, not a screenshot-less PDF interpretation.
4. CGS-23 source Davis–Jedwab (IEEE Trans IT 1999) count `m!2^(m+2)` only for its **specific** standard aperiodic binary family. At n=16 (`m=4`) it has 1536 ordered pairs, all included in the NGP family; it never provided a support bound for the entire NGP population.

## Exact ring correspondence [DERIVATION]

For `s=(s_0,...,s_(n-1))∈{±1}^n`, define the signed negacyclic lag-`d` correlation

```
NAF_s(d)=Σ_(j=0)^(n-d-1) s_j s_(j+d)
         − Σ_(j=0)^(d-1) s_j s_(j+n-d)
        = AF_s(d) − AF_s(n−d),   1≤d<n.
```

The `d=0` term is exactly `n`. In `Z[X]/(X^n+1)`, the multiplication matrix of s satisfies

```
mat(s)mat(s)^T = n I_n + Σ_(d=1)^(n-1) NAF_s(d) N^d,
NAF_s(n−d) = − NAF_s(d).
```

Thus a pair of binary ±1 polynomials has **source fixed covariance `2nI` if and only if** `NAF_a(d)+NAF_b(d)=0` for all `d=1..n−1` — exactly an NG-pair. Aperiodic Golay complementarity, which requires `AF_a(d)+AF_b(d)=0` for each positive d, is SUFFICIENT BUT NOT NECESSARY. Crucial: naively restricting to Davis–Jedwab was an unnecessarily severe prior design restriction.

**Non-generalization:** The spectral relation `|a(ζ)|²+|b(ζ)|²=2n` for `ζ^n=−1` bounds **the sum** of eigenvalue magnitudes, but does NOT by itself lower-bound each `|a(ζ)|` away from zero uniformly in n; original Lemma7.1's singular-value assumptions remain independent.

## Exact finite enumeration [EXPERIMENT]

Full self-contained executable source `/mnt/data/cgs24_ngpair_gate.py`, SHA256 `ecf4b698e77b2230d77fc136d3b5e69cb96501eee365c657d03f47ceab4e1f38`; exact JSON output `/mnt/data/cgs24_ngpair_gate.json`, SHA256 `243f7a7960baf45c13f1d06b704498b31fb068208c0b19b30051fdce6f810f14`. Uses finite deterministic enumeration, NumPy **integer** autocorrelation, integer matrix checks n≤8; numerical double-precision FFT only for optional singular-value threshold test n=16, with margins >1e-3 to tested thresholds.

| n | # ordinary ordered Golay pairs | # ordered NGP pairs | NG / ordinary | log2 #NG |
| -: | -: | -: | -: | -: |
| 2 | 8 | 16 | 2.000 | 4 |
| 4 | 32 | 128 | 4.000 | 7 |
| 8 | 192 | 4096 | 21.333 | 12 |
| 16 | 1536 | 557056 | 362.667 | 19.087462841 |

At `n=16`, 425984 of these NGP pairs have **both** `σ_min(mat(s_i))≥1` according to numerical eigenvalue calculation (minimum gap to threshold `1` over all ±1-polynomials approx 0.00286); subset support `log2=18.700439718` bits. At `σ_min≥0.5`, 491520 pairs remain (18.9069 bits). Every counted NGP pair meets `Σ=2nI` by the exact NAF identity; short n=2,4,8 pairs were independently confirmed by exact integer multiplication matrices. These finite spectral cutoffs do not prove asymptotic `c=Ω(1/poly(n))`, let alone source's full smoothing bound/parameter security.

**Finite-security limitation:** n=16 support only 19.09 bits, insufficient for 128-bit concrete cryptographic secrecy; the `n=1024` NGP count and efficiently samplable large-support distribution are **not** established. DO NOT extrapolate the observed 362.7x ratio or entropy differences to n1024. Source 2017 NGP counts so this is not a new mathematical enumeration result.

## Extra necessary restriction for k=3 binary components [DERIVATION, consequence of same NAF gate]

For any n divisible by 4 and any ±1 sequence s, set `t_j=s_j s_(j+1)` for `0≤j<n−1` and `t_(n−1)=−s_(n−1)s_0`. Then

```
NAF_s(1)=Σ_j t_j,
Π_j t_j=−(Π_j s_j)^2=−1.
```

So an odd number of the n signs t_j is negative, implying

`NAF_s(1) = n−2·(odd) ≡ n−2 ≡ 2 (mod4)` for 4|n.

The sum of `k` such correlations is `2k (mod4)` and cannot be 0 for **odd k**. Therefore, for n a positive multiple of 4, **binary ±1 coefficients and equal dense components, any odd module rank (including k=1 and k=3) cannot produce exact zero negaperiodic sidelobes**. This does not restrict ternary (0,±1), wider integer coefficients, different component dimensions, or approximate Gram flatness, and is not claimed as a novel theorem. It DOES eliminate the proposed k3 option within the precise binary signed-coefficient model.

## What this DOES and does NOT mean for cryptography

**PASS mathematical model repair:** rank-two NGP is the exact covariance-flat family; source/NGP literature shows the earlier DJ family is highly restrictive; n16 has more than 362x the DJ population, including candidates with adequate finite-n singular margins. This is a meaningful correction to our own CGS-23 screening, not a fix for the paper.

**NOT PROVED:** large-n 128-bit entropic support, efficient sampling with sufficiently high *min*-entropy, standard MLWE hardness with this globally correlated structured (a,b) key distribution, original source's chi_mlwe assumptions, independent-source KeyGen/Enc/Eval correctness and evaluation-key/circular security, competitive ciphertext/key size, or full reduction of O(LDec) without introducing another assumption. Even if NGP secret selection is secure, using a new key distribution would change baseline scheme and may be a considerably less valuable tradeoff than advertised.

**NO attack on Okada–Takagi original scheme**: all enumeration/security critique targets a proposed *secret-distribution replacement*, not source's unmodified KeyGen or Gaussian padding.

## End of Iteration

- **STATUS:** PASS H-CGS24 finite-scope NG-family enlargement + fixed Gram/spectral existence. Overall ThFHE target **UNCLEAR / HUMAN_REVIEW**; no novel primitive and no claim of practical 128-bit security.
- **RESULT:** Negacyclic MLWE requires NG-pairs, not ordinary Golay; n16 557056 vs1536; k3 binary is modulo-4 impossible when 4|n.
- **NEXT_TEST CGS-25 (only on PI next continue):** Find ONE **explicit, efficiently samplable NGP subfamily at cryptographic n (~1024)** with a rigorous lower bound `H∞≥128` (not merely total existence), and test one cheapest public-sample key-recovery/prior-art objection together with source individual `σ_min` hypothesis. If absent, PARK covariance-flattening and re-focus on original conditional Gaussian sharing; do NOT extrapolate small-n counts or list more generic constructions without security.
- **STATE_UPDATE:** YES, root single-active `STATE.md`, detailed CGS topic state, this finding. No unrelated FHE research archives altered.
