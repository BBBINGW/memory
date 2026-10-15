# CGS-26 — Fixed Gram does NOT eliminate the source's fresh padding at unchanged Bpub

**Date:** 2026-10-15. **Single active project:** CGS as selected in root `STATE.md`. **Previous:** CGS-25. **One primary hypothesis, one cheapest decisive source-parameter test.**

## Primary hypothesis / falsifier

**H-CGS26 [FALSIFIED under unchanged source parameters]:** The recursive binary NG-pair secret in CGS-25 has `Σ_s=2nI` at native module rank `k=2`; therefore we can set all pre-shared `ζ^(sid)=0` in the **UNCHANGED Okada–Takagi ePrint 2025/409 Algorithm 7**, retain its existing public `Bpub` condition, Lemma 7.1 / Theorem 7.5 simulator's prescribed Gaussian noise distribution, and automatically remove `O(LDec)` preprocessing storage without new proofs or additional setup.

**One cheap decisive gate:** Plug `Σ_s=2nI` into the actual source's `Bpub` inequality and Equation (26), compute whether `Σζ=Bpub² I−Σ_s` vanishes and whether no-padding Equation (25) equals the source's target Equation (26).

## Full original source [FACT]

**Hiroki Okada and Tsuyoshi Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, https://eprint.iacr.org/2025/409, ePrint 2025/409. Full 40-physical-page GitHub mirror PDF previously acquired; SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. Original physical **p29 Algorithm 7**: `Σ_s=Σ_i Gram(s_i)`, per sid `ζ^(sid)←D_(Z^n,σ0 sqrt(Bpub²I−Σ_s))`; share ζ via Shamir; `PartDec` adds corresponding ζ_i.
- **p30 Lemma 7.1 Equation (25):** unpadded `e` is statistically approximated by a rounded discrete Gaussian having latent covariance `p²σ0²Σ_s+σflood² I`. The first half of the lemma conditions on bounded secret coefficients and individual `σmin(mat(s_i))≥c>0`; proof uses smoothing and the generalized lattice Gaussian sum lemma p31–32.
- **p30–31 Lemma 7.1 Equation (26):** after adding the independent secret-conditioned padding, latent covariance becomes `p²σ0²Bpub²I+σflood²I`, explicitly **independent of s**. The proof invokes positive definiteness and a convenient sufficient public parameter condition, stated on p31 as
  `(Bpub² −1) − k n² Bmlwe² > 0`,
  hence `Bpub²>1+k n² Bmlwe²`.
- **p32 Theorem 7.4:** correctness uses `σdec` involving `σ0 Bpub`; **p32 Theorem 7.5** security uses the original key distribution `χmlwe` with its MLWE hypothesis and the source security proof. Replacing `χmlwe` by a highly correlated NG-pair distribution is **NOT** within this unchanged theorem.
- Source's newer ePrint2026/957 full PDF still blocked via Research MCP (IACR403, mirror absent) on CGS-25 repeated attempt; novelty cannot be certified.

## Exact decisive equation [DERIVED]

For ANY fixed-Gram family `Σ_s=2n I`, one has

```
Σζ = (Bpub² − 2n) I.
V0 = (p² σ0² ⋅ 2n + σflood²) I             [Eq.(25), no ζ]
V1 = (p² σ0² ⋅ Bpub² + σflood²) I          [Eq.(26), with ζ]
V1 − V0 = p² σ0² (Bpub² − 2n) I.
```

To retain the original target covariance WITHOUT padding, it would be necessary to set `Bpub²=2n`. Under the original Lemma7.1 sufficient inequality, this requires `2n>1+k n²Bmlwe²`. With `k=2,Bmlwe=1,n>=1` this is impossible: `2n <= 2n² < 1+2n²` for n≥1. Thus the proposed unchanged-parameter `ζ≡0` replacement does NOT preserve source Eq(26). This is a deterministic parameter/interface incompatibility, not a new attack on the source.

**Concrete n32768:** `k=2,n=32768,Bmlwe=1`. Source inequality demands `Bpub²>2147483649`. The minimum **integer Bpub** is `46341`, `Bpub²=2147488281`. Fixed NGP `Σ_s=65536 I`. Original positive padding covariance is

```
(Bpub²−2n) I = 2147422745 I   ≠ 0.
```

Ignoring the common `p²σ0²` and setting flood variance to zero purely to compare contributions, the source target variance exceeds the unpadded covariance by factor `2147488281/65536≈32768.0707`. If instead `σflood²=p²σ0²⋅2n` (a **normalized illustrative ratio**, NOT a source-instantiated parameter set), the variance ratio is `2147553817/131072≈16384.5353`.

**An illustration, NOT a ThFHE distinguisher:** For two real-valued centered normals with that latter variance ratio and the event `|X|≤sqrt(V0)`, the unpadded probability is `erf(1/√2)=0.68268949` and padded-target probability `erf(sqrt(V0/V1)/√2)=0.00623331`, gap ≈`0.67645618`. This shows why **disparate covariance is not a negligible bookkeeping error**. Actual original distribution is discrete/coset, subjected to rounding and reduced modulo q: this calculation DOES NOT prove a quantitative distinguisher against source's actual adaptive decrypted transcript for any named secure parameters.

Local exact numeric reproduction: `/mnt/data/cgs26_source_padding_variance_gate.py` SHA256 `db4152f63fde13fdce163cc2e26ce752364e96dd5b66d0ca39390943896304bd`, and `/mnt/data/cgs26_source_padding_variance_gate.json` SHA256 `a90cdbc1e0f767f138faf96735208bedec9a548b6e548d595d8e3b432f30d5dc`. Exact integer inequality and fractions use Python `fractions.Fraction`; floating error functions apply only to labeled illustrative normal comparison.

## Important constructive possibility rather than an overclaimed no-go [HYPOTHESIS]

The above does **NOT** rule out a REVISED different protocol. The source's `Bpub` condition is a sufficient condition to justify **adding** padding; it is NOT a theorem that all no-padding schemes are impossible. If a secure altered KeyGen produced constant `Σ_s=C I`, one could try to start **directly from Eq(25)** (whose covariance would already be public), REPLACE the simulation target distribution by one with latent `p²σ0²CI+σflood²I`, DROP the padding entirely, and reprove an appropriate counterpart of Theorems 7.4/7.5 with new `σdec`.

However, this requires ALL of:
1. A credible LWE/MLWE hardness/security reduction for the **globally correlated, recursively generated NGP secret** rather than the source's independent per-coefficient `χmlwe`; CGS-23–25 have supplied only mathematical covariance and family-size counts, not standard-MLWE hardness.
2. A **uniform quantitative individual** `σmin(mat(s_i))≥c` for an efficiently sampled high-min-entropy key subfamily, with smoothing/noise parameters tied to c; CGS-25 sampled some spectral values but did NOT certify a universal c or selection fraction.
3. Revised **simulation security**, including source ciphertext sanitization / PRF masked share joint adaptive transcript, secret key sharing, evaluation-key/circular-security assumptions, and actual end-to-end time/size improvements. Merely omitting ζ from Algorithm7 and citing its existing theorem is incorrect.
4. Novelty versus known **known-norm/known-covariance LWE** methods (the original paper already describes a known-norm unpadded Section 5 construction); cannot claim the constant-Gram mathematical idea itself is new.

**Research interpretation:** Earlier CGS-22–25 phrases that fixed covariance by itself 'eliminates pre-shared Gaussian padding' must be read as conditional on an independently validated **reparameterized unpadded protocol**, not an achieved result under original Algorithm7. This CGS26 clarifies a missing constructive link rather than falsifying all fixed-covariance research.

## End-of-iteration checkpoint

- **STATUS:** FAIL the named source-parameter-preserving no-padding direct substitution; PASS exact source Eq25-vs-Eq26 algebra and integer parameter test; UNCLEAR reparameterized fixed-Gram secure FHE / HUMAN_REVIEW. This is not a source paper bug or publishable standalone theorem.
- **RESULT:** At n32768,k2,B1 original Lemma7.1 condition forces `Σζ` strictly positive; with minimal integer Bpub, factor `2147422745 I`, so literal ζ removal doesn't produce the source simulator's claimed distribution.
- **NEXT_TEST CGS-27 (PI next continue):** one decisive **source first-stage Eq.(25) + structured-key spectral** gate: choose one explicit n32768 uniform recursive NGP subfamily with a *provable* lower bound c and at least 128-bit **filtered** min entropy, OR show that the source's Eq25 / MLWE security assumption cannot carry over. If neither can be established cheaply, PARK the NGP covariance/known-norm detour; return focus to original conditional Gaussian PCF problem. Do not endlessly enumerate known Golay identities.
- **STATE_UPDATE:** YES (only own finding, CGS topic checkpoint and one root STATE); current single-workflow MCP remains unchanged.
