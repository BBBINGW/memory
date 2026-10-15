# CGS-29 — Source-modulus versus 128-bit FHE hardness-guideline feasibility screen for flooding-only no padding

**Date:** 2026-10-15. **Current selected task:** CGS; previous CGS-28. Single active task, no track-specific MCP restriction. **ONE hypothesis + ONE decisive numerical parameter-screen test.**

## Hypothesis and falsification condition

**H-CGS29 [FAIL for the n=1024 illustration]:** Because CGS-28's no-pad strengthening adds only about 21 bits to the *baseline* flooding modulus in a rank-2 n1024 illustrative setting, that illustration is a credible **128-bit-secure** concrete example of trading O(LDec) stored pads for a small increase in communication.

**Decisive test:** Connect the *original paper's* minimum flooding and correctness relations to the *underlying ciphertext modulus Q*, not just to the increment Δlog q. Compare the resulting minimum Q of the CGS-28 illustrative parameter values with a named, published 128-bit FHE-security table **at the correct effective dimension k·n**. Reject n1024 claim if the BASELINE ALREADY lies far outside reference-table bounds; do NOT infer global impossibility from a table for a different key/error distribution.

## Primary-source relations [FACT]

Original Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409. Original full cached 40-physical-page mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED:
- **Lemma 3.12, physical p14:** original Gaussian smudging σ=Ω(2^κ||c||∞), already prior art.
- **Algorithm 2 physical p17:** abstract underlying MLWE FHE: ring dim n, module rank k, ciphertext/key modulus **Q**, χ_mlwe sampled per coefficient; crucially evaluation key generation details omitted, and no concrete security parameter set is provided.
- **Algorithm 7 physical p29 and Lemma 7.1 pp30–31:** fresh independent Server flooding E and secret-conditioned per-session Gaussian ζ; source requires σ_flood = Ω(2^κ B_eval), along with its smoothing lower bound.
- **Theorem 7.4 physical p32:** correctness q = σ_dec · Ω(√κ), with σ_dec containing σ_flood/p and other noise terms (typeset source expression's square-root placement needs visual parity check; underlying inequality σ_dec≥σ_flood/p is the relevant property); **Q = p q**. Therefore as long as positive hidden Ω constants are respected,
```
Q = Ω(√κ · σ_flood) = Ω(2^κ √κ B_eval).
```
This shows the ORIGINAL proof can demand a HUGE original ciphertext modulus before any extra flooding. Adding a polynomial multiplicative factor to flooding adds O(log κ) bits of q/Q *in an asymptotic bounded-polynomial parameter regime*, but concrete security can still be unacceptable.
- **Definition 3.14–3.16 p15:** LWE/MLWE assumptions are parameter-specific. The original theorem **does not** imply hardness when Q changes.

Independent published concrete-security benchmark: *Security Guidelines for Implementing Homomorphic Encryption*, Bossuat et al., IACR ePrint **2024/463**, https://eprint.iacr.org/2024/463, **Table 5.2 pp11–12** (page numbers printed in the article; physical PDF page index 11), classical category-128, ternary secret and coefficient Gaussian **error standard deviation 3.19**. Maximal log₂ ciphertext modulus allowed **for that modeled LWE/reference family**:

| Total effective LWE dimension N=k·n | Published reference maximum log₂ Q |
|---:|---:|
| 1024 | 26 |
| 2048 | 53 |
| 4096 | 106 |
| 8192 | 214 |
| 16384 | 430 |
| 32768 | 868 |

This is an **external published guideline, NOT a theorem/attack on arbitrary secret or error distributions**. We verified the published text table via the web source; screenshot fetch was attempted but remote PDF returned HTTP403/cache miss. No source-equation correction is asserted based on screenshot. Supporting accessible article code: https://github.com/gong-cr/FHE-Security-Guidelines/blob/main/tables.py. **Critical comparison:** Rank k=2, ring dim n=1024 corresponds to **effective LWE N=2048** for this standard parameter benchmark, not N=1024; compare max **53 bits**, not 26 bits. Structured MLWE versus flattened LWE requires further security scrutiny; the security guideline is only a screening reference.

## ONE exact reproducible numerical screen [COMPUTED]

Input is **identical to the CGS-28 illustrative setup**, not a source-verified valid or 128-bit secure FHE parameter choice:
```
κ=128, ring n=1024, module k=2, B=1, Beval=2^30,
p=2^20, σ0=16, random-rounding cutoff R=2^28.
```
Choose **illustrative** correctness hidden-factor `ceil(sqrt(κ))=12` and for each trial flooding width σ compute
`q_min=ceil(12 σ/p), Q_min=p q_min`. This is an exact integer construction using one concrete normalized factor, **NOT** an assertion that original Ω constants universally equal 1 or that all source correctness hypotheses hold. Actual q could be larger.

From original pre-existing flooding lower **term** choose `σ_flood,baseline=2^κ Beval=2^158`. CGS-28 sufficient full-residual smudging chose `σ_flood,no-pad≥2^(κ+2) n M` with
`M=k n B R +2Beval +1/2`.
Calculations:

| Variant | log₂ flooding σ | log₂ q_min | log₂ Q_min |
|---|---:|---:|---:|
| Original baseline lower flooding TERM (not all source bounds) | 158.000 | 141.585 | 161.585 |
| Scalar LWE no-pad strengthened term | 168.011 | 151.596 | 171.596 |
| Rank-two MLWE no-pad strengthened term | 179.006 | 162.591 | 182.591 |

At rank-two ring1024 the **reference-class** 128-bit maximum log₂ Q is **53** (not 26). Hence baseline 161.585 and proposed 182.591 are **both far above** this external 128-bit reference budget. This immediately falsifies using the **+21-bit increment alone** as evidence that this specific source-shaped example is implementable with reference-class 128-bit security. It does **NOT** prove a breaking attack or rule out modified secret/error/dimension distributions.

Same exact modulus screening across ring n (with k2) while **UNPHYSICALLY HOLDING σ0,R,Beval,p FIXED**:

| ring n | effective dim 2n | illustrative no-pad log₂ Q_min | reference maximum log₂ Q | SCREEN |
|---:|---:|---:|---:|---|
| 1024 | 2048 | 182.591 | 53 | OUTSIDE |
| 2048 | 4096 | 184.588 | 106 | OUTSIDE |
| 4096 | 8192 | 186.586 | 214 | NOT EXCLUDED |
| 8192 | 16384 | 188.586 | 430 | NOT EXCLUDED |

**NOT EXCLUDED does NOT mean PASS.** This sweep does not update σ0 to obey source Lemma7.1 smoothing assumptions, nor adjust Beval for genuine FHE multiplication depth, χ_mlwe coefficient distribution, q/Q decomposition, ciphertext/evaluation key sizes, actual LWE-estimator costs, sample number m, or any parameter-dependent attack. In particular source χ_mlwe may NOT equal the published guideline's ternary secret plus Gaussian(error,std3.19); even the log₂ Q upper-limit cannot be transplanted as a rigorous security theorem.

Independent precise calculation executed 2026-10-15: `/mnt/data/cgs29_modulus_security_screen.py` SHA256 `7d39f4da60e65d5ab4b6bb14996d3bf295d9fc92492ada317b41f9e335730077`; JSON `/mnt/data/cgs29_modulus_security_screen.json` SHA256 `83b3013e0c40d180ea490a419075015a3a84ba3b8e69a98ea2afddde3e0cdfa4`. Script uses arbitrary-precision integer/fraction bounds, no lattice estimator and no cryptosystem implementation.

## Constructive synthesis and caution

This CGS29 result is a **negative SCREEN for one previously used parameter illustration**, not a global negative theorem about fresh Server flooding. We must explicitly CORRECT CGS28's possible misleading inference: 21 bits extra by itself does not demonstrate competitive 128-bit secure parameters. Indeed an original bound σ_flood~2^κ Beval may already force Q outside low-dimension FHE budget.

For large enough effective dimensions, the screening condition may have headroom. However **source abstract Algorithm2** does not furnish concrete scheme-specific FHE parameters, so this iteration cannot supply “the actual secure Q” without explicitly choosing an underlying BFV/BGV/CKKS/FHE parameterized instantiation and its error/KeySwitch/Eval requirements. Claims of either a universal FAIL or universal PASS would be overstatements. Also prior art OpenFHE note https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_NOISE_FLOODING.md gives a **much tighter** Gaussian flooding sufficient width scaling as sqrt(12 τ)·2^(s/2)·error_estimate under its distinct security model. It cannot be copied into source adaptive Algorithm5 without reconciling definitions, but highlights why the conservative 2^κ additive-TV bound may be wasteful and novelty low.

## End of iteration

- **STATUS:** **FAIL** H-CGS29's concrete n1024/128-bit-viability inference; **PASS** original parameter interface and exact security-table dimension-matched numerical screening; **UNCLEAR** large-dimension parameterized ThFHE viability and adaptive simulator. Overall O(LDec) problem OPEN.
- **RESULT:** For previously illustrative k2,n1024, effective dim2048, full-residual flood-only sufficient `log₂Q_min≈182.591` and even original lower-term `≈161.585`, vs published reference 128-bit 53. No 128-bit instantiation certified. k2 n4096 illustrative test falls below reference cap only when holding unrelated params fixed: not a proof of feasibility.
- **NEXT_TEST CGS-30:** One explicit **source-compatible actual FHE instantiation/parameter family** (e.g. BGV/BFV with ring n≥4096 and concrete χ/evaluation-noise bounds). FIRST match source rounding/smoothing and full q/Q, THEN run a suitable lattice estimator / 128-bit security screen and communication + key cost. Alternatively derive a strict tighter smudging bound appropriate to actual Algorithm5 corruption view, documenting any missing composition steps; ONE primary hypothesis and decisive test, no false novelty. If this tradeoff is prohibitive, PARK flooding-only branch and PI select pivot back to conditional Gaussian challenge.
- **STATE_UPDATE:** YES own findings + CGS detailed history + sole root STATE; no unrelated research topics touched.
