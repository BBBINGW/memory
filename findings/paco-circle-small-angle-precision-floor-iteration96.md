# Iteration 96 — PaCo circle-group small-angle precision floor reproduces reported scaling

Date: 2026-10-12. Target: Coron and Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, ePrint 2025/886. ONE hypothesis / ONE cheapest decisive analytic Taylor test.

STATUS: **PASS** a conditional ideal deterministic precision ceiling explains the 10-bit separation and approximate order of PaCo I/II reported precision. **UNCLEAR** whether circle bias dominates measured *average* total CKKS error, since experiment precision metric and coefficient distribution differ. No paper correctness/security flaw, no novel correction established.

## Original source and provenance
Read original ePrint 2025/886 35 physical pages (Research MCP GitHub mirror; 2026-10-12 source acquisition) SHA256 `ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a`; official/latest PDF version **VERSION_UNVERIFIED**.
[FACT] §1.2 physical p6 Eq(2), §5.3 physical pp19–20 Eq(10): circle embedding ψ(a)=exp(2π i a/q) and approximate recovery `m ≈ (q/(2π)) Im(ψ(m))` for small |m|/q; this is *explicitly described as approximate* by authors. No false claim of exact recovery; source's 'zero failure probability' refers absence of approximate PERIODIC FUNCTION branch failures, not zero approximation bias.
[FACT] §7.2 physical p26 says only ciphertexts encrypting polynomials with coefficient magnitudes at most **p** are used in tests. PaCo I Table4 log2(q)=29, log2(p)=22, log2(Δ)=32; reported mean retained most-significant coefficient bits 12. PaCo II log2(q)=44, log2(p)=32, log2(Δ)=48; reported mean precision 22 bits. The paper does NOT identify that mean-MSB statistic with a worst-case relative error `E(p)/p`; precise coefficient sampling and measured error metric not specified in inspected text.

## Hypothesis and minimal falsification
Under ideal exact circle arithmetic, no other FHE error, |m|≤p, the polynomial estimate `g(m)=q/(2π) sin(2πm/q)` has intrinsic worst-case relative error ~`(2π²/3)(p/q)^2`. This may explain the experiment's 10-bit reported precision gap and rough precision ceiling. Falsifier: derived normalized precision markedly inconsistent with Table4, or paper's coefficient bound not p.

## Rigorously bounded ideal scalar bias [DERIVATION]
For m≥0, `E(m)=m−q/(2π)sin(2πm/q)`. Since E'(m)=1−cos(2πm/q)≥0, maximum over m∈[-p,p] lies at |m|=p. Let x=2πp/q. For both sources x<0.05, so alternating Taylor series gives
`p(x²/6−x⁴/120)≤E(p)≤p x²/6.`
Equivalently `E(p)/p=(2π²/3)(p/q)^2+O((p/q)^4)`. Note no CKKS encryption/rescale/noise or distribution.
The leading ABSOLUTE error is `(2π²/3)*p³/q²`. Both pairs have `p³/q²=2^8` (PaCo I: 3*22−2*29=8; PaCo II: 3*32−2*44=8), so absolute worst errors are nearly IDENTICAL while relative precision differs 10 bits. This is a direct algebraic source-grounded observation, not an attack.

## High-precision numerical tests [NUMERIC + ANALYTIC BOUNDS]
Used mpmath 100 decimal digits; all reported E(p) lie between explicit analytic lower/upper Taylor bounds; no random adversarial search.
- PaCo I q=2^29, p=2^22: x=0.04908738521234051935; E(p)=1684.209560488440798; E(p)/p≈0.000401547; `−log2(E(p)/p)=11.2821440561` bits; source reports 12 average coefficient MSB bits.
- PaCo II q=2^44, p=2^32: x=0.00153398078788564123; E(p)=1684.412286273291926; E(p)/p≈3.92e-7; `−log2(E(p)/p)=21.2819704115` bits; source reports 22 average coefficient MSB bits.
- The inferred ideal worst-case precision gap is 9.9998263554 bits versus source 10-bit mean reported gap. Same 0.72-bit difference in each comparison is **not proof of dominant error**, because statistic differs.
- **Illustrative ONLY** if input m is CONTINUOUS UNIFORM on [-p,p]: normalized mean-absolute bias bits 13.2820861173/23.2819703549; normalized RMS bias bits 12.6857828910/22.6856478348. Not verified distribution, and output 'mean retained bits' may be mean of `−log2(...)` rather than log of mean/RMS. Do not claim these are author's reported mean.
- Each E(p) ~ 1684 integer units; neither error exponent is a precision security level or a CKKS rescale-error estimate.

## Reproducibility
Local verified `/mnt/data/iteration96_paco_small_angle_precision.py` SHA256 `a371edce82e7e8ef6f470a1e5e160ce619796c3f60db1e3dfb3963d0514abcf0`.
Local JSON `/mnt/data/iteration96_paco_small_angle_precision_results.json` SHA256 `92fbe2e4a8b31246ac62fa55a675a2c1c07329a7fb1774a75f764aed40abf5b4`.
Script assertions PASS: Taylor brackets, same p³/q² order, +10-bit gap and continuous-uniform proxy. NO implemented CKKS, no actual PaCo precision samples.

## Decision
[PASS conditional] First-order ideal error matches experiment order in two independent parameter sets and predicts 10-bit difference solely from p/q. This is unsurprising Taylor analysis, already conceptually acknowledged by source. No identified correctness gap or novel method. The numeric match motivates **one**, rather than many, follow-up on experiment implementation to isolate actual error.
[OPEN] Need author's exact coefficient input distribution, precision statistic, measured per-coefficient absolute errors and any round/rescale noise decomposition. A claimed 'precision bottleneck' requires these rather than comparing mismatched average and worst-case.
NEXT_ACTION (I97): In source-linked public author repo `https://github.com/se-tim/PaCo-Implementation`, inspect only coefficient input generation and precision measurement (search terms precision, bit, error, random, coeff; pin commit), determine whether their measured statistic evaluates max, mean, or RMS after rescale, and check whether resulting statistic expected from ideal circle bias can be directly compared to 12/22. Stop if unavailable and mark EVIDENCE MISSING; no full CKKS implementation or optimization proposed.
STATE_UPDATE: YES — quantitative precision boundary plus narrowly defined missing evidence for next smallest test. No author contact/public disclosure; no novelty claim.
