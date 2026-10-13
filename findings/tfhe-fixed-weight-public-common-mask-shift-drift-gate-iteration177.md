# Iteration 177 — Fixed-Hamming-weight LWE enables secret-free common mask-shift drift tuning, but typical n=834 benefit is modest

**Date:** 2026-10-13. Human PI authorized with “好的，请继续” after I176. Followed `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` (blob `8aaf27cd12e8ffe6fa2a79d8b1a3ef6672a34685`) and `findings/OPEN_RESEARCH_BRANCHES.md` + I176 archive. Human PI's assent interpreted as PARK prior binary jump which original LLKN23 already subsumes. Exactly ONE primary hypothesis with cheapest source-based algebraic + finite-mask numerical test. NO formal scheme security, CKKS/TFHE correctness benchmark, or independent novelty proven.

## Source and prior-art gate

**Main original** Thomas de Ruijter, Jan-Pieter D'Anvers, Ingrid Verbauwhede, *Don't be mean: Reducing Approximation Noise in TFHE through Mean Compensation*, ePrint **2025/809**, https://eprint.iacr.org/2025/809, complete Research MCP **23 physical page** GitHub-mirror PDF SHA256 `3d108a46b6ad5c3342551de289f48bcfd5e96a93c37d13ebbb39a3db3f280118`, official current version **VERSION_UNVERIFIED**. §3.1–3.2 physical pp6–9 discusses mean compensation: for binary i.i.d. secret `s_i∈{0,1}` with mean `μ_s=1/2` and public modulus-switching errors `u_i`, adjusting body by `−μ_s∑u_i` changes mask-rounding term from `∑u_i s_i` to `∑u_i(s_i−μ_s)`; variance formula `σ_u²(n σ_s²+1)` relies on iid binary secret and rounding-model hypotheses. §3.3–3.4 and §4 address ring polynomial gadget decomposition, mean compensation with BKU. §5 pp16–17 acknowledges countermeasures from Bernard et al. and discusses fundamental remaining variance and security estimator heuristics; §7 pp18–20 measures source TFHE-rs improvement; these **source numbers** are NOT benchmark reproduced.

**Prior drift method original** Olivier Bernard, Marc Joye, Nigel Smart, Michael Walter, *Drifting Towards Better Error Probabilities in Fully Homomorphic Encryption Schemes*, EUROCRYPT 2025, ePrint **2024/1718**, full **32pp** Research MCP mirror SHA256 `ed989536365d54e0edac649f3d990de592ce8313683f6f5e82af8e6cbae6723a`, VERSION_UNVERIFIED. Original §5 pp14–16 describes general publicly computable same-message ciphertext transforms **by adding encryptions of zero**, then publicly scoring drift residual vectors; no dedicated known-fixed-weight **all-mask-equal shift** was found in searched/inspected §5, but an exact-public-zero shift is an instance of the broad transform paradigm. **NOVELTY NOT VERIFIED**; no claim first/new. This is closely related existing drift/compensation work.

**Known fixed-weight secret variant original** Bergerat, Chillotti, Ligier, Orfila, Roux-Langlois, Tap, *New Secret Keys for Enhanced Performance in (T)FHE*, ePrint **2023/979**, full **55pp** mirror SHA256 `45988ec46a5577ebd0747822cf7eb8d5b31d55deec0f348db98ca4f1636596a5`, VERSION_UNVERIFIED, Appendix A p36 defines *fixed Hamming weight (FHW)* binary **GLWE** secret with public exact weight h. This establishes such distributions are relevant but does **NOT** establish that a particular **pre-PBS input TLWE secret** has the **exact public binary sum h** condition; e.g. signed sample extraction / KS or key-distribution changes require inspection. All source ePrint PDF extraction text, formula glyph parity current official version not visually verified.

**Source unavailable candidate NOT chosen:** ePrint2026/2310 recent multi-value TFHE LUT optimization was searched; Research MCP returned `RETRIEVAL_BLOCKED` (official 403, exact arxiv no result, fixed mirror missing). No technical claim or reading of that paper; do not construe abstract as verified.

## ONE primary hypothesis and decisive test

**[HYPOTHESIS, performance-gated]** If the TLWE secret is binary with **PUBLIC FIXED EXACT Hamming weight h**, a plaintext-independent publicly computable common mask shift can preserve the plaintext phase *exactly* while the offset is chosen solely from observable mask rounding residues, and produce a **material improvement in the mean-compensated modulus-switching noise** for typical realistic high-dimensional uniform masks at no extra ciphertext material. Strong version: mean reduction is large enough to justify novel TFHE research beyond already known mean compensation/drift.

**FALSIFIER:** Derive exact phase preservation, compute the correct conditional fixed-weight covariance/noise component, choose the best public shift via all circular rounding cut points (not a few arbitrary offsets), then measure at source TFHE LWE dimension n=834 over many independent uniform fractional mask vectors. If even that *optimal* public shift saves only a few percent of the residual **one-component** noise, it is not a strong general optimization, despite a favorable small counterexample. Note default 2025/809 source actually uses **IID** binary secret, so this is an intentional different secret distribution, not an author's mistake.

## Derivation

Let `q` be old torus integer modulus and `q'=2N` the new modulus, with q'|q. TLWE convention `b−<a,s>=m+e (mod q)`. Assume `s∈{0,1}^n` and `∑s_i=h` **is the publicly known exact value**. For any PUBLIC integer t in Zq, define
```
 a'_i=a_i+t mod q,    b'=b+h*t mod q .
 b'−Σ_i a'_i s_i = b−Σ_i a_i s_i   (mod q).
```
No FHE operation/encryption of zero/secret access needed. Note choosing t adaptively based on a is a public postprocessing of an already secure ciphertext, and so cannot reveal more message information than the input ciphertext under its ASSUMED IND-CPA-secure exact-weight key distribution; however security of fixed-weight LWE parameter set is NOT shown here. Direct use for standard iid Bernoulli secret INVALID because Σs_i is secret and random; transformation would add phase error `t(h−Σs_i)`.

Define public normalized rounding residues `u_i(t) = (q'/q)*(a_i+t)−Round((q'/q)*(a_i+t))` (mod quotient with centered choice); uniform iid mask ⇒ iid near-uniform u_i before optimizing t. For fixed h secret uniform over all `n choose h` supports, μ=h/n:
```
 E_s[Σ_i u_i s_i | u] = μ Σ_i u_i
 Var_s(Σ_i u_i(s_i−μ) | u) =
     [h(n−h)/(n(n−1))] Σ_i (u_i−u_bar)^2.
```
This **conditional** finite-population covariance is different from the iid-Bernoulli conditional variance `μ(1−μ) Σu_i²`. Its expected value over iid uniform rounding residues happens to match n μ(1−μ) σ_u², but for each observed u the best direction is minimize centered dispersion. Mean compensation of body by `μΣu_i` as in source §3 addresses deterministic mean; *body rounding residual*, cryptographic encryption error, gadget noises and conditional dependence of b on s remain separately present and are not optimized/proved here.

The centered variance of `u_i(t)` is piecewise **constant between cut points** where one residue crosses the nearest-round boundary: moving t within an interval adds same constant to all nonwrapping residuals and cannot change dispersion. Let sorted residues `r_0≤...≤r_{n−1}` in [0,1). Each possible relative wrap ordering corresponds to vector `v_i=r_i+1` for i<k, `v_i=r_i` otherwise. Precompute prefix sums to evaluate `Var(v)` for each k in O(n), sorting O(n logn), choose minimizing cut; t realizable modulo q/q' granularity to nearest cut in large torus. This is a simple circular variance optimization, not evidence of novelty (indeed directly related to drift-quality optimization).

## ONE exact test: favorable toy + typical realistic dimension

**[Exact integer toy]** q256, q'8, n4, h2, a=(18,20,12,14), shift t16. Mask residual vector before `(-14,-12,+12,+14)/32` and after `(+2,+4,−4,−2)/32`. Population dispersion before `0.166015625` and after `0.009765625`, ratio exactly **17×**. Enumerated all six fixed-weight support sets for s (all h2 combinations), set b=a·s mod256 (e=0, plaintext0) and shifted b'=b+2·16 mod256. Direct modulus-switch outputs phase after rounding: before `(-1,0,0,0,0,+1)` (under support enumeration [01],[02],[03],[12],[13],[23]), after `(0,0,0,0,0,0)`. This is an exact phase-preserving original-q transform and an exact rounding improvement on THIS insecure toy, not evidence of high-dimensional failure-probability advantage.

**[Realistic-dimension mask-only quantitative gate]** n834 from paper §7 Table3, 512 independent uniform fractional `r_i∈[0,1)` pseudorandom mask trials with explicit deterministic 32bit xorshift seeded 0xC0FFEE (a public simulation RNG, not cryptographically secure), and each trial finds the **global optimum circular cut** among n+1 wrap patterns by sorting/prefix moments. Results:
```
 Mean centered variance at default nearest-rounding cut: 0.08324792339422107
 Mean centered variance after optimal public common mask shift: 0.07966410905372323
 Mean trialwise relative dispersion saving: 0.04212059603028668 (~4.21%)
 Median saving: 0.03628258960335351 (~3.63%)
 90th percentile saving: 0.08966199083159154 (~8.97%)
 Maximum observed across 512: 0.16563958562048686 (~16.56%).
```
These are data-derived **simulated publicly observable mask residuals**, at continuous limit of torus64bit resolution (not q64 actual ints), not TFHE execution or post-mean-comp ciphertext error distribution. They are one cheap test of *upper envelope* of this type of one-scalar shift on the residual-mask variance. For iid secret this special zero-plaintext public shift is UNAVAILABLE; fixed-h key security/parameter changes must be separately evaluated. n834 h value not specified in current original default: selecting h=n/2 as exact known weight would CHANGE original secret distribution. Full body-rounding can negate or alter the small improvement; no new performance claims.

## Evidence, novelty and scientific judgment

**[PASS only algebraic precondition]** For exact public binary weight h, common offset `(a+t1,b+ht)` is always a phase-preserving public TLWE transformation. The mask-rounding *conditional* secret-term variance can be optimized offline with a simple O(n logn) circular cut. Some inputs can improve greatly (toy 17×).

**[FAIL strong importance premise at n834]** For IID uniform public mask residues and n834, even full optimal cut yields only **~4.2%** average component variance reduction, not the ~2× approximation-variance improvements established by source's standard mean compensation (for its original parameters). Actual total FHE noise benefit likely smaller, but not quantified. The chosen secret distribution is not source's iid binary key; method cannot be dropped into standard TFHE-rs by changing one line. Security of FHW-key LWE must be separately checked and 128-bit LWE estimate rerun; this may erase gain. Adaptation to GLWE fixed-weight via sample extraction/sign conventions not verified.

**[PRIOR ART WARN]** Bernard et al. ePrint2024/1718 §5 already gives general public same-message ciphertext transformations and drift-quality tests, though using added zero encryptions; this fixed-h noiseless vector shift may be a special inexpensive transform within their general umbrella. FHW keys themselves are known from Bergerat et al. ePrint2023/979. **NOVELTY NOT VERIFIED**. Algebraic identity and circular-optimal one-parameter offset are elementary, NOT standalone contribution.

**[SOURCE LIMIT]** Recent ePrint2026/2310 full PDF unacquired, no technical assertion. All sources GitHub mirrors VERSION_UNVERIFIED; mathematical glyph parity not screenshot-verified (paper means clear from extracted text).

## End of Iteration 177

**STATUS:** **PASS** exact phase-preserving public translation *only for exact-known-weight binary LWE secret* and conditional variance formula; **FAIL** strong typical n834 component variance gain premise (only 4.21% simulation); **UNCLEAR** actual FHE key distribution, end-to-end noise/security/latency and novelty.
**RESULT:** Public family `a' = a+t1, b'=b+ht`, conditional fixed-weight variance `[h(n−h)/(n(n−1))]Σ(u_i−u_bar)^2`; optimize t by circular sorting in O(n log n). Toy q256→8 n4 h2 gives17× smaller residual variance and removes two phase-rounding failures; at n834 512 uniform random mask trials optimal shift saves mean4.21% of mask-component variance, far short of source's ~50% mean compensation, not end-to-end. Technique is structurally a known ciphertext-drifting type transformation, likely low novelty.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK** generic fixed-weight common-offset drift in absence of a real fixed-h **pre-PBS TLWE source path** and large measured practical advantage. Reopen only if one actual FHW TLWE/keyswitch output is source-verified, security/bit-budget matched to baseline, and a concrete structured nonuniform rounding-residue workload leads to material gains at no additional online latency. If PI “继续”, pivot to another sourced high-value FHE question (not toy 4-bit phasors or mean-comp revisits); latest missing ePrint2026/2310 needs user-supplied original bytes before paper audit.
**STATE_UPDATE:** **YES** — one genuinely different TFHE recoding hypothesis/source study with hard precondition and modest typical-gain gate, original binary-secret source assumptions preserved; prior Park binary jump PARKED by PI assent after I176; other prior archives unchanged.
