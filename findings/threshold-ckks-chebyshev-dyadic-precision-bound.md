# Iteration 53 — Exact fixed-precision boundary for dyadic ScaledChebyshev indicator degrees

Date: 2026-10-10
Research target: Min, Hanrot, Park, Passelègue, Stehlé, *Distributed Key Generation for Efficient Threshold-CKKS*, ePrint 2025/2057 (CCS 2026).
STATUS: PASS for a **conditional ideal-polynomial precision boundary**; UNCLEAR for real FHE stage applicability, implementation, performance and novelty.
NOVELTY: LOW — the paper ALREADY explicitly acknowledges the boundary-point derivative versus non-target approximation trade-off in Appendix B.3 and permits non-dyadic degrees in §3.1. No correctness gap, publishable algorithm or CKKS speedup demonstrated.

## Protocol and provenance
[FACT] Read latest GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and previous I52 failure `failures/threshold-ckks-fixedhw-onehot-count-already-optimal.md` before setting hypothesis. The previous Grafting sprout branch remains archived. STATE.md is an unrelated parked RIG-HE project and is NOT changed.
[PRIMARY SOURCE] Full original PDF ePrint 2025/2057, 52 physical pages, GitHub mirror acquired by Research MCP, PDF SHA256 `519d1c9672c743b49307de8ebaa1015ba44ff089fae0d1e754482abe40ef764d`, VERSION_UNVERIFIED:
- §3.1 physical p.11–12, Lemma1: `W_(B,d)(x)=T_d((B+1−2x)/(B−1))/T_d((B+1)/(B−1))`, equals 1 at x=0 and bounded by inverse denominator for all x∈[1,B]; power-of-two degrees via ScaledChebyshev; the paragraph directly states extension to general d via Chebyshev identity `T_(2l+1)=2T_l T_(l+1)−X`.
- §3.1 Lemma2 p.12: power-of-two d=2^m uses m+1 multiplicative levels under the *unfused* affine transform and O(m) ciphertext-ciphertext multiplications; §5.1 p.25 notes affine plaintext multiplication can be folded upstream to avoid one level.
- §3.2 p.13–14, Theorem1: for one-hot K=2^k, the final boundary indicator is `δ_(k,k)` applied to a Hamming-comparison vector w, so B=k=log2(K). For actual K=2^16, B=16.
- Appendix B.3 physical p.35, Lemma5: derivative at x=0 has magnitude approximately `d/sqrt(B)` (exact: `(d/sqrt(B))*tanh(d*acosh((B+1)/(B-1)))`). Authors ALREADY describe accuracy improving exponentially on [1,B] but degrading around 0 as `2^-p d/sqrt(B)`, and suggest balancing these errors.
- §5.2 pp.25–26: actual input baseline scaling factor 2^30; mentions worst-case need ~26.5 precision bits for entire rotate-and-sum component and total 6 multiplicative levels for one-hot generation. **This does NOT imply the local indicator input has deterministic <=2^-30 error, nor that every indicator stage individually must achieve 26.5 bits**. Those are deliberately imposed conditional hypotheses in this test, not a statement about implemented pipeline or security.

## One primary hypothesis and decisive condition
[HYPOTHESIS — FALSE] In the natural real-world one-hot dimension K=65536 (so B=16), if an indicator receives real inputs within ±2^-30 of the appropriate integers and needs worst-case ideal indicator error ≤2^-26.5, a dyadic-degree `d=2^m` ScaledChebyshev alone can attain that precision without additional input cleaning or a change in degree family.
[FALSIFIER] Show an exact lower-bound witness for every dyadic degree: if d≤32 the non-target error is too large, whereas if d≥64 a small negative input perturbation at the target forces an error too large. Also check a single non-dyadic d is not fundamentally prohibited by polynomial approximation itself.
[ONE CHEAP TEST] Use the exact paper polynomial in the two real input regions with Fraction rational arithmetic (no CKKS ciphertext, floating-point decisions, stochastic tests or parameter sweep). Fixed values B=16, δ=2^-30, target τ=2^-26.5.

## Exact mathematical verification
[DERIVED] The candidate degree-d polynomial is
 W_d(x)=T_d((17−2x)/15)/T_d(17/15).
Take **target** interval x∈[−δ,δ]; t=(17−2x)/15>1, T_d(t) strictly increasing with t, so the maximum of |W_d(x)−1| occurs at an endpoint x=−δ or δ.
Take **non-target** interval x∈[1−δ,16+δ]; t ranges in [−1−2δ/15, 1+2δ/15], so by the Chebyshev bound |T_d(t)|≤T_d(1+2δ/15) and the upper bound is attained at an endpoint; hence
  E_target(d)=max(|W_d(−δ)−1|, |W_d(δ)−1|),
  E_non(d)=T_d(1+2δ/15)/T_d(17/15),
  E_worst(d)=max(E_target(d),E_non(d)).
These are exact rational numbers for all integer d, and check against τ via `E_worst(d)^2 <= 2^-53`, avoiding irrational floating-point threshold ambiguities.
For d=16: non=2^-10.79145, target=2^-28.0000, FAIL.
For d=32: non=2^-22.58290, target=2^-27.0000, FAIL.
For d=38: non=2^-27.00469, target=2^-26.75207, PASS.
For d=39,40: both PASS.
For d=64: non=2^-46.16580, target=2^-25.99999999, FAIL.
For d=128: target=2^-24.99999998, FAIL.
Monotone proof for **all** dyadic degrees: for d≤32, T_d(17/15)≤T_32(17/15) so |W_d(1)|≥|W_32(1)|>τ; for d≥64, `W_d(−δ)=cosh(d*a)/cosh(d*b)` with `a=acosh((17+2δ)/15)>b=acosh(17/15)>0` is strictly increasing in d since `a*tanh(ad)−b*tanh(bd)>0`, so |W_d(−δ)−1|≥|W_64(−δ)−1|>τ. Thus no dyadic d works.
[CRITICAL] d=38 is not a novel function and its ideal polynomial precision feasibility is **not** a CKKS evaluation cost result: evaluation of general Chebyshev degrees needs a different addition chain and potentially more ciphertext multiplications than the six-squaring d64 circuit. Real evaluations suffer additional rounding, rescale, key-switch and encoding noise, none included here.

## Reproducible experiment
[EXPERIMENT] Exact Fraction script `/mnt/data/iteration53_threshold_ckks_indicator_precision_audit.py`, SHA256 `35e7502e6c14c3e77a6afc31449ac0cbd308207f31633aff084b0667993ca3e3`; stdout `/mnt/data/iteration53_threshold_ckks_indicator_precision_results.txt`, SHA256 `2dd6219384c8d1e1497d4e703c57ca70c185e601cb489c347c8055e13294e89f`. Assertions for all reported degrees and exact squared-error comparisons PASS. Decimal bit counts used only for display, not logic.
[NO FHE TEST] No encrypted ciphertext was evaluated; no assertion on formal DKG end-to-end correctness, the exact numerical distribution or actual noise in the authors' implemented stage.

## Interpretation, novelty & scope
[PASS CONDITIONAL] With p=30 input and a 26.5-bit desired *per-indicator* tolerance, the inherent trade-off of the exact boundary indicator forbids all dyadic degrees but accepts general degree38 in the ideal real polynomial evaluation model. This is a precise interesting parameter boundary and confirms the paper's qualitative B.3 analysis rather than contradicting it.
[NOT VERIFIED] That the actual one-hot input indeed only has p=30 immediately before the indicator, or that the whole routine requires 26.5-bit per-indicator accuracy, is NOT shown by the paper. It explicitly cleans bits/trits in §5.1, so the real effective precision may be higher. No claim that Theorem1, DKG implementation or the security proof is flawed.
[ANTI-NOVELTY] The authors already allow non-dyadic Chebyshev degree; choosing 38 is plain precision-sensitive parameter tuning and does not establish an advance in modulus/latency/key material. More multiplications may erase any precision advantage. Therefore do not start HEaaN implementation until a substantive new method appears.

## End of iteration
STATUS: PASS for a source-grounded conditional dyadic precision impossibility; UNCLEAR regarding applicability to the actual CKKS implementation.
RESULT: For B16,p30,tau=2^-26.5, every dyadic degree fails (proven beyond finite test), while general d38 satisfies exact ideal-polynomial output error across perturbed target/non-target intervals; paper B.3 already states mechanism. Novelty low.
NEXT_ACTION: Inspect the paper's actual §5.1 implementation design or available source for **the boundary indicator degree and input-error bound at the moment it is applied**. If those are unavailable, archive this degree-tuning branch rather than spend another iteration tuning toy parameters; if available and p≈30, first compare the *multiplication/level counts* for existing degree vs degree38 before any numerical CKKS test.
STATE_UPDATE: NO — distinct parked RIG-HE STATE.md unchanged.
