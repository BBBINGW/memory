# CGS-31 — Centered Gaussian variance still obstructs one public, uniformly statistical no-padding simulator

**Date:** 2026-10-15. **Research task:** Single active CGS, continuing from CGS-30. Previous rank-two NGP branch CGS22–27 and naive worst-case independent flooding CGS28–30 are PARKed. One precise hypothesis and one cheapest decisive test. Original Okada–Takagi 2025/409 O(LDec) conditioned-Gaussian sharing problem remains OPEN.

## Primary hypothesis and exact limit of result

**H-CGS31 [FAIL in the specified statistical sense]:** Replace CGS28's pessimistic treatment of rounding noise `r^T s` as an arbitrary deterministic shift with its **centered Gaussian** distribution. Then a fresh independent Gaussian of normalized polynomial width `F=σ_flood/p=poly(κ)` should make residual distributions for *each* legitimate secret `s` negligible-statistically-close to **the same publicly sampleable Gaussian distribution** without conditioned ζ, enabling the source's Hyb6-style statistical simulation and polynomial-valued `q`.

**ONE decisive test:** Start from source §5 Lemma5.1 exact stated Gaussian approximation of first-stage noise (and §7 Lemma7.1 for MLWE). Take two norm-squared values m and m+Δ. Test one interval-event probability and obtain an explicit lower bound on their total variation distance after independent flooding. If the residual two-secret distance is inverse-polynomial for F=polyκ, no one public Gaussian can be negligibly close to **both** conditioned distributions. Do NOT promote such a *conditional* divergence to an attack on the actual Algorithm5 secret-hidden computational game; the secret is not revealed to the adversary.

## Primary paper source [FACT]

Okada & Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025 / IACR ePrint 2025/409, https://eprint.iacr.org/2025/409. Cached original mirror: 40 physical pp, SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. Relevant **original pages read**:
- **§5 Lemma5.1 Eq(14), physical pp20–21:** scalar unpadded `e≈s randomized-round_σ1[(1/p)e0 + {q/2}μ]`, `e0←D_((1/2)Z, sqrt((pσ0 ||s||)^2+σ_flood²))`. Thus after scaling, Gaussian width squared `V_s=σ0²||s||²+(σ_flood/p)²`; the independent final rounding σ1 adds further public noise rather than canceling the secret difference.
- **§7 Lemma7.1 Eq(25), physical p30:** MLWE unpadded latent `e0←R(D_((1/2)Z^n, sqrt(p²σ0²Σ_s+σ_flood² I)))` with `Σ_s=Σ_i Gram(s_i)`. The diagonal entry at each coefficient equals `Σ_i ||s_i||²`. A one-coordinate projection already has secret-norm-dependent variance, independent of more complicated off-diagonal terms.
- **§6 Algorithm6 p26 / §7 Algorithm7 p29:** original solution pre-shares one conditioned Gaussian pad per session to make noise covariance fixed and public; in §6 Theorem6.3 p28 the simulator uses that public covariance.
- **Algorithm5 physical p23 and §5 proof sketch p24:** the computational ideal/real game reveals `(ctdec, all active pdi)` for adaptive ODec queries; the §5 known-norm public key includes `||s||`, allowing public sampling of conditional e. The §6/7 source security needs INDISTINGUISHABILITY of **whole transcript**, not merely equality of two latent Gaussian laws.
- **Prior art:** variance-based noise-flooding is established. OpenFHE docs https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_NOISE_FLOODING.md use tighter model-specific `2^(s/2)` flooding width and explicitly warn its multiquery security/precision must be accounted for. Our continuous-Gaussian event bound is an elementary inequality, NOT claimed a novel theorem.

## Derivation of strict lower bound [DERIVED]

Consider continuous *model* Gaussians `G0=N(0,v0)`, `G1=N(0,v1)` with `v1=v0(1+δ)`, `0<δ<=1`, where source-predicted width squared `V_s` is proportional to v_s with common Gaussian convention. If final independent Gaussian rounding has width σ1 in the continuous surrogate, add σ1² equally to both widths; hence the relative difference is

```
δ = σ0²·Δ / [F² + σ0² m + σ1²],  F=σ_flood/p,
m=||s0||², m+Δ=||s1||².
```

(For source's LATENT e0 alone, omit σ1². This is a *continuous final-noise surrogate*, not an exact equality for the source's randomized discrete rounding operation.)

Define event `A={|X|≤sqrt(v0)}`. Its probability gap is exactly
```
g(δ) = erf(1/sqrt(2)) - erf(1/sqrt(2(1+δ))).
```
Calculus gives
```
g'(t) = exp[-1/(2(1+t))] / [sqrt(2π)(1+t)^(3/2)].
```
For `0≤t≤1`, `g'` decreases, with minimum
```
c_* = exp(-1/4)/(sqrt(2π)*2^(3/2)) ≈ 0.10985.
```
Therefore
```
TV(G0,G1) ≥ g(δ) ≥ c_*·δ.
```

For ANY *fixed secret-independent* distribution H, triangle inequality forces
```
max(TV(G0,H),TV(G1,H)) ≥ (c_*/2)·δ.
```
When `F,σ0,σ1,m,Δ` have polynomial/bounded parameters and `σ0²Δ` is ≥inverse polynomial, δ is ≥inverse polynomial. Thus there is **no negligibly accurate secret-by-secret public Gaussian surrogate** at polynomial F from this argument. This is a real distinction versus CGS30's deterministic-shift smudging: centering may improve the required σ exponent, but cannot by itself turn an inverse-polynomial residual variance gap into negligible without superpolynomial F or another hiding technique. This result is conditional on the Gaussian approximation (and on selecting two secrets within the valid source domain), with source approximation errors to be subtracted using a triangle inequality.

**Important non-implication:** The two-secret conditional experiment supplies a hypothetical observer knowledge of which s/norm is used. Actual Okada–Takagi Algorithm5 does NOT provide s/norm to its standard-LWE challenger in §6/7, and computational simulation may exploit hiding of that correlation. A simulator could conceivably mix over a fake key norm, if a suitable **joint computational independence** hybrid under standard MLWE exists; none is established here. The actual source key distribution may assign negligible probability to a particular pair of exact secrets; hence an event separating two individually named secrets is NOT automatically a feasible original-game distinguisher. For a Bernoulli (0/1) secret with n=κ, binomial norm² has typical √κ-scale fluctuations; this observation is only indicative, not a full joint-key leakage proof.

## ONE reproducible mathematical/numerical test [EXECUTED]

File `/mnt/data/cgs31_centered_gaussian_variance_gate.py` SHA256 `88ee17bbd908f7cb3859efaa845e1bb0ac335e128b7c902bd3cfc723a6cdd80a`. JSON `/mnt/data/cgs31_centered_gaussian_variance_gate.json` SHA256 `6d754ad20a8f8c2ef60333a38cbfdabc3b611dc7f04ee1c46de1f69b06434690`. Reproduced by executing the script in the active session; this is not a cryptosystem implementation.

Choose `n=κ`, a Bernoulli-secret norm-class example `m0=κ/2`, `m1=κ/2+ceil√κ`, `σ0=4`, normalized F=κ², σ1=4, and **illustrative polynomial q=κ³** (not a verified original-paper security/correctness parameter tuple). Compute the exact rational δ from integer widths, the analytic erf gap, and rigorous c*δ bound:

| κ | relative δ | event gap, continuous | rigorous TV lower c*δ | 2^(-κ) target |
|--:|--:|--:|--:|--:|
| 16 | 9.744e-4 | 2.357e-4 | 1.070e-4 | 1.526e-5 |
| 32 | 9.153e-5 | 2.215e-5 | 1.005e-5 | 2.328e-10 |
| 64 | 7.629e-6 | 1.846e-6 | 8.380e-7 | 5.421e-20 |
| 128 | 7.153e-7 | 1.731e-7 | 7.857e-8 | 2.939e-39 |
| 256 | 5.960e-8 | 1.442e-8 | 6.547e-9 | 8.636e-78 |

A distinct **discrete-lattice sanity test** (source-form density `exp(-πx²/width²)`) on `(1/2)Z` compared the two **modeled** Gaussian widths `sqrt(12²+4²·8+1²)≈16.523` and `sqrt(12²+4²·12+1²)≈18.358`, with an explicitly summed symmetric tail grid (883 points). Direct TV=**0.050898207127648**, while event `|X|≤sqrt(v0)` yields probability gap **0.050898207127648** up to numerical rounding. This is a Gaussian **surrogate** with corresponding covariances, not a direct sample from full source Algorithm5 hybrid; finite-grid omitted Gaussian mass is tiny and could be bounded by standard e^{-πx²/w²} tails.

The alternative `p` can be exponentially large to satisfy original **pre-division** smudging lower bounds while F remains polynomial, but Q=pq may then be huge and its concrete standard LWE/MLWE hardness is unverified. This test does NOT certify a κ128 FHE construction. Conditioned pair noise gap is stronger evidence against *universal statistical simulator strategy* than against *computational* security under hidden s.

## Synthesis / next research decision

**PASS** one explicit source-aligned Gaussian variance obstruction and mathematical proof, with discrete Gaussian sanity. **FAIL** H-CGS31 as a uniform secret-by-secret negligible-statistical-public-noise simulation claim using polynomial F. The branch CGS28–31 of just replacing correlated ζ with larger uncorrelated Gaussian E, whether treating W as a fixed bounded shift or as centered Gaussian, does not provide the original statistical Gaussian-target hybrid with `q=polyκ` under the currently tested techniques. **PARK this source-native flooding-only replacement** pending a fundamentally different computational hybrid, a truly new hidden-output conditional-noise-share generator, or concrete source-compatible security breakthrough.

**CRITICAL LIMIT:** No universal computational impossibility, no source attack, no proof that *all* polynomial-q fresh-server-noise constructions fail, no claim that final discrete mod-q TV automatically equals continuous latent TV, and no original-game advantage bound.

**END OF ITERATION**
- `ITERATION: CGS-31`.
- `STATUS: FAIL` public-uniform conditional negligible statistical simulation hypothesis; `PASS` exact Gaussian event proof + continuous/discrete surrogate tests; `HUMAN_REVIEW` original CGS open.
- `NEXT_TEST CGS-32 (if PI next "继续"):` ONE concrete **computational** alternative rather than continuing flooding scale adjustments: can the simulator generate a **dummy secret norm/covariance** and decouple it computationally from public key and randomized decryption transcript using a known-norm LWE reduction (scalar) or a genuinely new known-covariance MLWE hybrid, *without* publishing the norm? Define the joint indistinguishability game and cheapest falsifier. If source assumptions are insufficient or this simply restates known-norm LWE, PARK and redirect to the original hidden-shared Gaussian primitive. Do not revive NGP/PRSS old failures without a new interface.
- `STATE_UPDATE: YES` own findings, CGS detailed current progress and sole root STATE; other work intact.
