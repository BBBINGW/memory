# Iteration 191 — AKU Gaussian FHEW DFR audit: upstream OpenFHE final ModSwitch kernel does not explain away the paper-model discrepancy

**Date:** 2026-10-14 (Asia/Tokyo); user PI authorized one I191 after I190. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I190 SHA `bc2b254fa8b7a908dc93c800ffef0345b88c3f18`, and `findings/fhew-aku-gaussian-dfr-consistency-iteration190.md`. ONE primary hypothesis + ONE decisive code-conformant final-modulus-switch test. No user cryptosystem experiments or author's specific fork reproduced.

## Sources / provenance

- **[FACT, primary]** Qi Zhang, Mingqiang Wang, Xiaopeng Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, **CANS 2025**, ePrint 2025/381 https://eprint.iacr.org/2025/381 ; full 27-physical-page Research MCP GitHub mirror, PDF SHA256 `bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf`, latest official binary VERSION_UNVERIFIED. Independently fetched official ePrint PDF text via web `turn514880view0` / `turn677595view0`, §5.1 physical p19, Table2 and §5.2 Table3 physical p21. **MANDATORY web PDF screen pageno18 ATTEMPTED AGAIN, FAILED `Cache miss`**; visual formula glyph parity, and later CANS 2025 proceedings version parity, UNVERIFIED. CANS paper DOI https://doi.org/10.1007/978-981-95-4434-9_14, publisher full chapter apparently restricted; do not assume identical formula without it.
- **[FACT, current upstream reference implementation, NOT author's 2025 version]** `openfheorg/openfhe-development` default branch `src/binfhe/lib/lwe-pke.cpp`, GitHub fetched blob SHA `68dc58e1cbea0ceedb014b6c9d6de81c32df3bcb`, https://github.com/openfheorg/openfhe-development/blob/main/src/binfhe/lib/lwe-pke.cpp : `KeyGenGaussian(uint32_t size, NativeInteger modulus)` instantiates `DiscreteGaussianGeneratorImpl<NativeVector> dgg(3.19)`; `RoundqQ` returns `floor(0.5+v*q/Q)%q` (floating double for ratio); `LWEEncryptionScheme::ModSwitch` applies RoundqQ separately to all n mask coefficients and body; `SwitchCTtoqn` does ModSwitch to qKS, KeySwitch, then **ModSwitch to q**.
- **[FACT, current upstream routing]** `openfheorg/openfhe-development` `src/binfhe/lib/binfhecontext.cpp` blob SHA `d67c6d366ef81e36ef1ab6202112fe21e5267878`, https://github.com/openfheorg/openfhe-development/blob/main/src/binfhe/lib/binfhecontext.cpp : for `GetKeyDist()==GAUSSIAN`, `BinFHEContext::KeyGen` calls `m_LWEscheme->KeyGenGaussian(Getn(), GetqKS())`. Thus **upstream Gaussian small LWE key** matches the stated n and Gaussian parameter; final ModSwitch outputs under that LWE key. No source evidence located of a separate AUTHOR AKU GitHub repository or author-pinned commit. Searching GitHub terms AKU/Qi Zhang/Mingqiang Wang yielded CANS bibliographic listings but no implementation.
- **[FACT paper expression extracted, visually unconfirmed]** §5.1 Table2 Algorithm6: n447, q1024, Qks=2^14=16384, σ=3.19 for Gaussian-key, Q=2^28; `σms2²=(||s||₂²+1)/12`, `||s||₂²≈nσ²`, `β²=(q²/Qks²)[(Qks²/Q²)σacc²+σms1²+σks²]+σms2²` as extracted; `DFR=1-erf((q/8)/(2β))`; Table3 Algorithm6 `2^-36`, Algorithm5 `2^-37`, stated goal `<2^-32`. Source §5.1 printed text clearly says final NAND standard deviation √2 β, supporting extracted `2β` denominator in erfc. **This is a source-conditional model** and not a proven exact probabilistic statement about real encrypted executions.

## ONE I191 primary hypothesis and decisive check

**[H191 to falsify]** The large I190 DFR gap is *entirely* an artefact of an incorrect `σ=3.19` convention or use of a crude uniform-rounding `1/12` approximation for the last `Qks→q` ModSwitch; the actual upstream implementation's Gaussian-key generation and exact scale-round operation should yield an MS2 variance smaller by a factor sufficient to make the published `2^-36` plausible.

**[FALSIFIER]** Inspect actual code for final LWE secret distribution and per-component qKS→q rounding, compute exact one-coordinate rounding error distribution at ratio16 (Qks16384, q1024), derive key-weighted phase-noise variance under the source-like uniform-mask idealization, then do ONE deterministic zero-input LWE integer simulation to ensure direct code-level quotient/phase operations match the derivation. If exact variance remains near 1/12 and code uses Gaussian std3.19 with n447, the proposed resolution fails. No author code is required to reject the *upstream-implementation version* of this supposed resolution; author-specific behavior remains gated.

## Integer-level derivation and numerical results [DERIVATION]

`RoundqQ(v)=floor(0.5+v/16)` for 0≤v<Qks, reduced mod1024. For uniform `v mod16=r∈{0,...,15}` and the scaled q-domain phase, define
```
 ε(r)=floor(0.5+r/16)−r/16.
 ε(r) = {0,−1/16,−2/16,...,−7/16,+8/16,+7/16,...,+1/16}.
 E[ε]=+1/32 (IMPORTANT: ties-to-PLUS; initial streaming result wrongly stated −1/32, see correction).
 E[ε²]=43/512 = 0.083984375.
 Var[ε]=255/3072 = 0.0830078125.
```
This last variance differs from `1/12` by only `(1/12−255/3072)/(1/12)=1/256` (0.390625%); does not fix 18-bit DFR exponent gap. With LWE phase convention `b=〈a,s〉+m+e` (the sign in actual OpenFHE `Decrypt`; source may use a sign-renamed convention, variance invariant), and no input encryption error, the exact final switched phase perturbation is
```
 E_MS2 = ε(b mod16) − Σ_i s_i ε(a_i mod16).
```
For independent uniformly sampled mask residues `a_i mod16`, if at least TWO components of fixed integer s are odd, then b mod16 is uniform and pairwise independent of each a_i mod16; all cross-covariances vanish and
```
 E[E_MS2 | s]=(1−Σ_i s_i)/32,
 Var(E_MS2|s)=(1+||s||₂²)·255/3072.
```
The proof uses invertibility of an odd secret coefficient mod16 to uniformize the body residue even conditioning on any ONE mask residue; no assertion all residuals jointly independent, just zero pairwise covariance. For source's typical Gaussian norm estimate `447·3.19²=4548.7167`, the variance is
```
 (4548.7167+1)·255/3072=377.66203076171877,
 beta_MS2=19.433529..., 
 erfc((1024/8)/(2 beta_MS2)) ≈ 3.202317030684388e−6 =2^(−18.25245).
```
This is STILL about 220,000× larger than Table3 Alg6 `2^-36`, within the same heuristic β model. It is a **model-internal necessity**, not an unconditional actual-failure lower bound. Note rounding error mean is NOT zero, a potential additional key-dependent bias; the pure variance test alone excludes the claimed factor-change rescue.

**Independent deterministic integer test** (model-level, not real OpenFHE bootstrapping):
- `rng=np.random.default_rng(19102)`; draw five independent length447 vectors with components `np.rint(Normal(0,3.19))`, use fifth as a **Gaussian-like representative** (not exact discrete Gaussian sampler): `Σs_i=−23`, `||s||²=4589`. Sample 24,000 independent 16-residue vectors using RNG seed19103; take body `b≡Σ a_i s_i (mod16)` from valid zero-message/zero-error LWE and perform exact floor-half-up qKS/q component switching. Measured `E_MS2` mean0.90075 vs exact prediction `(1−(−23))/32=0.75`; empirical sample variance 376.60498 vs predicted `(4589+1)·255/3072=381.00586`; observed SD19.4063 vs predicted19.5194. Small sampling discrepancies are expected, not evidence of variance shrinkage.
- Independently construct **500 entire qKS=16384 uniform mask ciphertexts** (random seed19104), `b=〈a,s〉 mod16384`, apply exact `(a',b')=(floor(a/16+0.5),floor(b/16+0.5)) mod1024`, compute centered output phase `[b'−〈a',s〉]_1024`. Compare to direct residual formula above: all 500 equal exactly, max difference 0.
- No 2^-36 tail can be empirically confirmed by 24k trials, nor a 2^-18 rate estimated robustly by 24k trials. This test checks the **size/variance of the isolated final ModSwitch term**, not the full β, key-switch/gadget/accumulator noise or actual plaintext failure.

## Interpretation and scientific caution

**[FAIL H191 narrow explanation]** Under the actual upstream OpenFHE Gaussian small-key generation path and final ModSwitch scale-round semantics, neither a smaller σ convention nor finite ratio16 rounding reduces the mandatory MS2 contribution enough to reconcile the ePrint's **extracted independent variance model** with Table3. This corroborates I190's *model/table inconsistency* and elevates it to higher-priority original code-version audit. It does **not** confirm an actual false experimental DFR; the author's 2025 CANS fork, compiler options, complete noise paths and published print/PDF revision were NOT obtained, and negative covariance from other operations could invalidate an unsafely assumed nonnegative-term decomposition as a physical bound. Current upstream github file may have changed after paper experiments; no pinned 2025 author version identified. The exact Gaussian tail approximation `1−erf(...)` is itself a modeling choice. 128-bit lattice hardness, measured 30.41ms, 257MB keys and 20.7% relative speedup not proven false.
**[SOURCE RENDER CHECK]** Web `screen|turn514880view0|18` returned CACHE MISS; ePrint source text and MCP extract show matching `2β` denominator, and prose clearly says √2β NAND noise SD. Physical p19 rendered equation remains not independently verified. Published CANS 2025 pp292–312 DOI is known but its full text not independently obtained. Do not send authors a strong error allegation without actual paper glyph/code check.
**[SELF CORRECTION]** During result streaming assistant incorrectly gave `E[ε]=−1/32`, because Python `round` uses tie-to-even, while source OpenFHE `floor(0.5+x)` ties upward. Correct value is `+1/32`; `Var[ε]=255/3072` and the full DFR inconsistency conclusion remain unchanged.

## End of Iteration 191

**STATUS:** **FAIL** hypothesized simple Gaussian-σ/rounding approximation resolution in current OpenFHE implementation; **PASS** source-code verification of Gaussian n and final ModSwitch, exact finite 16-residue variance and whole-ciphertext arithmetic test, plus reproducible variance example; **UNCLEAR** author-specific exact code, full β, PDF visual formula/edition, true model-vs-actual DFR and 20.7% matched-failure benefit.
**RESULT:** Upstream Gaussian key has std3.19; last qKS→q coefficientwise round gives variance `255/3072≈0.083008`, essentially paper 1/12, and **typical** final MS2 variance ∼377.662 (β≥19.4335 under source sum-of-variance model), corresponding modeled DFR floor ∼3.20e−6 vs paper2^-36. No safe source-code convention explanation established.
**NEXT_ACTION:** **I192 NOT STARTED, HIGH-PRIORITY HUMAN_REVIEW / conditional CONTINUE**: seek original author's exact code/commit or CANS proceedings rendered equation, verify whether published DFR numbers were obtained using a differently scaled final secret, correlation accounting, or parameter typo. Before another algebraic toy, get reproducible author parameters or a validated full local OpenFHE run (several parameter/key draws) and full noise-budget breakdown; compare model vs physical ciphertext noise. If artifacts unobtainable, label SOURCE_VERSION_GATED and park the alleged paper defect pending user-supplied author code/PDF. Only after verification derive corrected security+DFR+latency Pareto frontier; no unsupported attack claim. No independent new FHE algorithm proposed.
**STATE_UPDATE:** YES. One primary gate resolved; source code and exact variance added, user-visible sign convention corrected, preserved gap/source caveats.
