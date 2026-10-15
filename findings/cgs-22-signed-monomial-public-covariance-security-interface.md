# CGS-22 — Signed-monomial secret lifting flattens MLWE rounding covariance but a direct RLWE embedding is not uniform-MLWE

**Date:** 2026-10-15. **Mode:** single active research stream, PI-authorized continuation of CGS-21 via root `STATE.md`. **STATUS:** FAIL **the specific direct standard-uniform MLWE embedding**; PASS exact variance-flattening construction and ciphertext identity; UNKNOWN efficient FHE security, novel contribution, and full Okada–Takagi replacement. Does NOT solve the original arbitrary-standard-MLWE/low-cost/O(LDec) problem or claim a general no-go.

## One precise hypothesis and decisive gate

**H-CGS22 [FALSIFIED as stated]:** For binary-secret negacyclic RLWE with secret polynomial `s(X)`, a signed-monomial lifting `S_j=(2s_j-1)X^j` makes the secret-dependent MLWE rounding covariance EXACTLY public `nI`, AND a direct black-box sample transformation from one ordinary binary-secret RLWE sample produces an **ordinary, uniform-public-matrix** MLWE sample under the lifted secret, so the original pre-shared conditional-Gaussian padding can be bypassed with the original standard-MLWE security argument and cheap overhead.

**Falsification:** Derive the transformed `A'_j` needed to preserve the exact LWE inner product. Test whether its public distribution satisfies the standard MLWE requirement `A'_j iid U(R_q)`. One public-coordinate equality test kills direct use of the standard MLWE assumption. Positive covariance alone is not a full construction.

## Original-source context [FACT]

- Hiroki Okada and Tsuyoshi Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, https://eprint.iacr.org/2025/409, complete 40 physical-page primary mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. Physical **p4 §1.2** identifies O(LDec) pads as open; **p29 Algorithm 7** specifies `Sigma_s=Σ_i Gram(s_i)` and fresh hidden-shape Gaussian `ζ^(sid)∼D_(Z^n,σ0 sqrt(Bpub² I−Sigma_s))` which is precomputed/shamir-shared for every session. **p30 Lemma 7.1** requires each source `mat(s_i)` to have singular value ≥c; its proof also assumes a specific small independently coefficient-sampled source `χ_mlwe`. Our structured key distribution cannot automatically inherit its full FHE security theorem. **pp3–4 and §5** also present known-norm LWE as an existing unpadded route: simply making norm public is NOT novel in itself.
- Daniele Micciancio, *On the Hardness of Learning With Errors with Binary Secrets*, Theory of Computing 14(13), 2018, https://www.theoryofcomputing.org/articles/v014a013/. Establishes a standard-LWE-to-binary-LWE hardness reduction with quantified sample/parameter tradeoffs; this DOES NOT prove standard module-LWE for any of our structured secret vectors nor FHE circular/evaluation-key security.
- Related newer Okada–Takagi *Threshold FHE with Short Decryption Shares Without a Semi-trusted Server*, ACISP 2026, ePrint 2026/957, abstract describes a serverless Shamir-based scheme, but exact full source remains unavailable: originality cannot be certified.

## Correct algebraic component [DERIVED]

Work over `R=Z[X]/(X^n+1)` and `R_q` with ODD prime q. Let original binary-secret `s(X)=Σ_(j=0)^(n-1) s_j X^j`, `s_j∈{0,1}`. Define `ε_j=2s_j−1∈{−1,+1}`, `S_j=ε_j X^j` and public `H(X)=Σ_j X^j`.

Then `s=(H+Σ_j S_j)/2 mod q`. Integer multiplication by `X^j` in the canonical negacyclic basis is a signed permutation, hence `mat(S_j)mat(S_j)^T=I_n`, each `σ_min(mat(S_j))=1`, and

```
Σ_S := Σ_(j=0)^(n−1) Gram(S_j)
     = Σ_j mat(S_j) mat(S_j)^T
     = n I_n
```

**independently of the actual secret bits.** Thus the source-style smoothing covariance could be public in an FHE scheme whose KeyGen secret really is S; this does NOT by itself demonstrate secure decryption or apply Algorithm7 under its original key distribution.

## The one decisive standard-MLWE interface falsifier [DERIVED]

Given ONE original binary-secret RLWE sample `(a,b=a*s+e)`, the straightforward algebra-preserving lift publishes

```
A'_j := a/2            for every j=0,...,n−1,
b'   := b − a*H/2.
```

Then `b' = Σ_j A'_j*S_j+e` exactly mod q, since `Σ_j S_j=2s−H`. However `A'_0=...=A'_(n−1)` holds with probability **1** in the transformed distribution. For independent uniform standard MLWE public vector `(A'_0,...,A'_(n−1)) ← U(R_q^n)`, the same event has probability `|R_q|^{-(n−1)}=q^{-n(n−1)}`. Public distinguisher `D(A')=1 iff all coordinates identical` has advantage **1−q^{-n(n−1)}**. This is a complete, unconditional distributional distinguisher between **THIS transformation** and uniform-public standard-MLWE; it is NOT an attack on the original binary RLWE instance.

For n=4,q=17, standard-vector uniform probability `17^-12≈1.7163780167e-15`, advantage `1−17^-12`. One cannot treat this transformed sample as a new ordinary MLWE sample with standard-MLWE hardness proof simply because the equation is correct.

## One exact toy test [EXECUTED]

- n=4,q=17,R=F17[X]/(X⁴+1)
- ALL 2^4=16 binary secrets tested: `Σ_S=4I` EXACTLY; every signed monomial multiplier has singular values 1.
- 1000 seeded random ciphertexts with small errors, checked exact `b'==ΣA'_j S_j+e mod17`.
- Checked `A'_j=a/2` for all j in every transformed sample.
- Exact support-combinatorics probability `17^-12` (not Monte Carlo security estimation).

Reproducible local `/mnt/data/cgs22_sign_monomial_covariance_gate.py` SHA256 `4505f6fcd17814f366a8b3c46696133dae13fea668a8e6f5a9c2483a8ae2bbee`; JSON `/mnt/data/cgs22_sign_monomial_results.json` SHA256 `77132adc377d3df3593bf1df09c228c8546c9329ed2500e7238a60b19e1a6023`.

## Security alternative vs cost [DERIVATION + LIMITS]

**Important constructive observation:** Rather than transforming old RLWE samples, generate NEW independent uniform `A_j ← U(R_q)` and `b=Σ_j A_j S_j+e`. For fixed `ε_j∈{±1}`, the coefficient vector of `A_j X^j` is a uniformly random vector in `F_q^n` (negacyclic signed permutation); across independent j the entire coefficient matrix is iid uniform. Thus in coefficient representation this distribution is EXACTLY `n` vector-LWE samples with a `n`-bit `±1` secret ε (after public recentering, binary-secret vector LWE). This suggests a potential alternative **standard vector-LWE** security reduction using known results, but **not** the original rank-small standard MLWE claim, and crucially **NOT** a complete new FHE scheme/key-switching/evaluation-key security proof. It also increases module rank from 1 to n, so a naive ring-key/ciphertext representation scales from O(n) coefficients to O(n²) coefficients; the exact end-to-end cost may differ under new specialized compression, which has not been designed.

The original target was standard (Module-)LWE with compact keys and communication. Even if the public covariance is flattened without on-demand correlated Gaussian, the specific tested transformation simultaneously breaks native uniform-public MLWE distribution and loses the small-module-rank interface. `chi_mlwe` independence conditions and other FHE key-generation assumptions change. The result is **not novel by itself** (monomial orthogonality is elementary), and a useful new work would need a small-rank, high-entropy, standard-MLWE-hard fixed-covariance key family or a redesigned efficient FHE, with exact security and noise proof.

## Constructive Synthesis gate

Pieces found:
(a) legitimate high-entropy (2^n possible) binary secrecy;
(b) publicly constant covariance `Σ_S=nI` while each secret ring component is non-singular;
(c) algebraic ciphertext inner-product-preserving transform.

Missing **joint viable construction:** uniform public module distribution under standard MLWE with this simple transform (impossible for these displayed A'_j), source KeyGen/Enc/Eval security, and practical native-module-rank complexity. Therefore the correct result is a useful REPRESENTATION insight but a **FAIL** for the hypothesized direct standard-MLWE/efficient source replacement. Do not repeat generic hidden-output PCF ports from CGS-10–21 absent a new interface.

## END OF ITERATION

- `ITERATION: CGS-22`.
- `STATUS: FAIL` direct transformed STANDARD-MLWE distribution; `PASS` covariance/nondegeneracy/inner-product identity; `UNCLEAR` native uniform-A vector-LWE/FHE system and novelty; `HUMAN_REVIEW` target.
- `RESULT:` Monomial secret lifting removes hidden covariance but direct published-standard-MLWE reduction fails publicly; significant rank inflation.
- `NEXT_TEST (CGS-23, upon next PI continue):` ONE narrow cost/security gate: Can a **bounded module rank k=O(1)** and high-entropy standard-MLWE-hard secret distribution have **exact public Σ_s**, avoiding padding, without degenerating into an efficiently enumerable or readily distinguishable secret family? Search Golay/complementary-polynomial prior art and try ONE concrete bounded-rank candidate with min-entropy and native-uniform-A test. If unable to construct under standard MLWE, recommend PARK the covariance-flattening detour, leaving original O(LDec) primitive open. Do not overgeneralize this single transform's failure.
- `STATE_UPDATE: YES` root STATE + CGS detailed topic + own findings, no other research topics edited.
