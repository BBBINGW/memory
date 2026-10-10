# Iteration 54 — Published DKG parameters do not establish the local Chebyshev precision premises

Date: 2026-10-10
Research target: Min, Hanrot, Park, Passelègue, Stehlé, *Distributed Key Generation for Efficient Threshold-CKKS* (CCS 2026), IACR ePrint 2025/2057.
STATUS: UNCLEAR (actual indicator degree and local input-error bound); FAIL (attempt to infer that the I53 conditional precision obstruction applies to the implemented DKG solely from the publicly stated global scale/level counts).
NOVELTY / CONTRIBUTION: NONE; I53 mathematical conditional boundary is correct in its own explicitly ideal model, but does NOT substantiate a paper bug or speedup. Archive this degree-tuning direction rather than running more toy sweeps.

## Read-before-write / state discipline
[FACT] Prior to choosing the hypothesis, read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and I53 `findings/threshold-ckks-chebyshev-dyadic-precision-bound.md`; preserved unrelated parked RIG-HE STATE.md. Single primary hypothesis and one decisive primary-source+public-code availability audit, no CKKS implementation.

## Primary exact source
[FACT] Min et al., IACR ePrint 2025/2057, full 52 physical pages obtained through Research MCP from fixed GitHub mirror; PDF SHA256 `519d1c9672c743b49307de8ebaa1015ba44ff089fae0d1e754482abe40ef764d`, VERSION_UNVERIFIED:
- §3.1 physical pp.11–12, Lemmas 1–2, `W_(B,d)(x)=T_d((B+1−2x)/(B−1))/T_d((B+1)/(B−1))`; power-of-two-degree ScaledChebyshev described, general degrees also explicitly allowed via `T_(2l+1)=2 T_l T_(l+1)−X`. Author does not restrict all implementations to dyadic degrees.
- §3.2 physical pp.13–14 Theorem 1: `OneHotVecGen` uses a boundary integer indicator for B=k=log2 K. With implementation K=N=65536, B=16.
- Appendix B.3 physical p.35, Lemma 5: target zero derivative ∼d/sqrt B and rising with d, while nonzero leakage drops exponentially; authors ALREADY explain limited-input-precision degree tradeoff.
- §5.1 physical pp.24–25: bit cleaner `p1(x)=3x²−2x³` evaluated twice before sampling rotate-and-sum, and additional cleaning for final secret key; efficient ScaledChebyshev initial affine/plaintext multiplication can be fused upstream to avoid a full level. These are stage-specific and alter local precision.
- §5.2 physical pp.25–26: implemented parameter N=2^16, h=32, H=45, **baseline scaling factor 2^30**, total homomorphic sampling 20 levels partitioned as 3 random-bit generation + 6 one-hot generation + 11 homomorphic sampling, and *approximate* worst-case precision requirement `log(H−h)+log N+log K≈26.5 bits` for the rotate-and-sum of sparse binary sampling. This last requirement is NOT stated as an independent 26.5-bit accuracy for each `δ_{16,16}` evaluator. Also the K=160 later on that page is a different EvalMod range parameter.
- Search `degree 64`, `degree-64`, `d = 64`, `T64`, `degree 32`, `d = 32`, `ScaledChebyshev` and named functions in PDF: no *explicit instantiation of the boundary one-hot indicator polynomial degree* found. This is a negative search observation, not proof it is absent from all versions/files.

## Single primary hypothesis / failure condition
[HYPOTHESIS — UNSUPPORTED / FAIL TO ESTABLISH] From §5.2's one-hot generation 6-level budget and baseline scale 2^30, infer an actual dyadic indicator instance at B16 receiving entrywise errors bounded by exactly ~2^-30 and required to output ≤2^-26.5 pointwise error. Then claim I53's dyadic impossibility exposes an actual weakness in the published implementation.
[FALSIFIER] Any of (i) source does not specify a degree, (ii) input scale is not a proved bound on local accumulated error, (iii) stage-global precision condition is not the local output tolerance, (iv) non-dyadic degrees are allowed and/or extra cleaning invalidates the model's premise. The paper evidences all four ambiguities; hence no actual implementation error can be inferred.
[ONE MINIMAL DECISIVE TEST] Directly check §3.1, §3.2, §5.1–5.2, App. B.3 and search openly accessible author's GitHub/code links for the actual degree and local error metrics, not run any new numerical toy simulation.

## What was directly verified / evidence limits
[FACT] Author pages:
 - Seonhong Min publications https://minsh.info/pages/publications
 - Alain Passelègue publications https://perso.ens-lyon.fr/alain.passelegue/publications.html
 - Jai Hyun Park homepage https://jaihyun.com/
Each lists the CCS 2026 paper, but **the checked listings did not supply a reproducible source-code/configuration link for the paper-specific one-hot indicator**.
[SEARCH OBSERVATION] Targeted public GitHub code and repository searches for full paper title, `FixedHWSampler`, `OneHotVecGen`, `ScaledChebyshev` returned no clearly attributable author implementation. This does not establish that private or unindexed source does not exist.
[FACT] §5 reports a proof-of-concept on HEaaN and GPU/CPU benchmarks; 'no verified public source' does NOT mean the authors did not implement it.
[DERIVED] A CKKS ciphertext scale Δ=2^30 does not establish an absolute error bound 2^-30 at an arbitrary intermediate step. Error depends on encoding, prior operations, rescaling, key switching, and precision from bit cleaning. Six *total* levels do not uniquely identify polynomial degree because (a) the initial affine transform may be fused and (b) a chain of varying degrees / other operations can fit the same total depth.
[DERIVED] I53's exact ideal-model math remains mathematically true: for B16, inputs ±2^-30, per-indicator desired 2^-26.5, all dyadic degrees fail, general d38 works (exact Fraction witness). But none of its crucial precision premises can currently be grounded in the implementation. Paper §3.1 already permits general degrees, making d38 parameter tuning rather than a new technique.

## Conclusion and scope
[NEGATIVE] No ground to present I53 as a real-world ciphertext-level correctness/precision bug in Theorem1 or the implementation. Neither proof nor implementation-level degree can be audited fully with obtained primary text. The gap is **missing public stage-level evidence**, not confirmed false operation or erroneous claimed theorem.
[OPEN] Actual implemented one-hot boundary polynomial degree d; chosen evaluation schedule and coefficient approximation; per-slot precision immediately before indicator; empirical/proved error budget; any cost benefit from alternative degrees. These require released code/config logs or targeted author clarification.
[RESEARCH JUDGMENT] This is the second adjacent conditional/no-source iteration; avoid continuing degree tuning or making new toy precision examples. No new FHE algorithm or identified Pareto-frontier movement.

## End of Iteration
STATUS: UNCLEAR (actual stage parameters), FAIL (specific evidence-based applicability hypothesis).
RESULT: Primary §5 confirms K=2^16, 6 one-hot levels, baseline scale 2^30 and 26.5-bit **sampling-stage** precision estimate, but supplies no reliably identified degree and no local input error guarantee. Theoretical I53 boundary cannot be promoted to an actual flaw. No attributable public DKG implementation obtained during targeted repository/author-page search.
NEXT_ACTION: ARCHIVE I53–I54 degree-tuning candidate. For next distinct single-hypothesis technical audit, open **the same paper §4.4 physical pp.22–23**, and test whether its proposed two-round key-generation strategy's stated `Ω(ℓ)` bootstrapping bottleneck for ℓ homomorphic PRF-generated evaluation-key errors is an inherent sequential limitation or an unproven assumption under batch/SIMD PRF evaluation. First locate existing CKKS batched PRF-evaluation prior art before proposing any technique.
STATE_UPDATE: NO — separate parked RIG-HE STATE.md unchanged.
