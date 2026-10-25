# EAI-SYNTH B7 — Full partition tree: original per-counter confidence does not naively compose

Date: 2026-10-25 Asia/Singapore
TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH
Previous completed: B6. Current: B7. All EAI-SYS/EAI-P/EAI-SEC/FHE and other track counters untouched.
Execution: original-source read, original PDF screenshots, one exact counting derivation. No GPU/Codex/model download/training/source modification. PENDING_CODEX=NONE_REQUIRED_FOR_B7; all future Codex tasks must remain pending until PI explicitly asks for them.

## ONE falsifiable primary hypothesis
[HYPOTHESIS H-B7, NEGATIVE]
Using B6's original per-counter Algorithm2 threshold-good events with failure upper bound 1/H_i, a direct union bound over all active spatial partition cells and all time epochs is sufficient to certify a high-probability (failure o(1)) full-tree counting-noise event, and thereby a Wasserstein-accuracy statement, without strengthening the per-counter event or changing proof ingredients.
[CHEAPEST DECISIVE TEST]
Count the number of per-cell per-epoch sparse-counter instances in He's Algorithm1/Algorithm3 and sum their original Appendix A threshold-bad probabilities 1/H_i. ONE arithmetic test only. Do not construct a new protocol or assume independent failures.

## Original baseline [FACT]
- He, Vershynin, Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv 2402.08012v3 (2024-10-23), https://arxiv.org/pdf/2402.08012 and https://arxiv.org/html/2402.08012v3 . Original PDF physical pages 7–8 (Algorithm1–3), 11–14 (Eq4.1, Lemma4.2, Eq4.4–4.8), 20 (Appendix A Lemma3.2 proof) visually inspected.
- Algorithm1 creates 2^j cells at spatial depth j and invokes one Algorithm3 subroutine per cell (for d>=2 starting time-level r0=j). Eq4.1 sets eps_{j,i}=C1 eps*2^((j-i)(1-1/d)/2) for j<=i, C1=(1-2^(-(1-1/d)/2))/2. This budget controls privacy across levels but does NOT change combinatorial number of per-cell accuracy events.
- Algorithm3, time-level i, runs one Algorithm2 sparse window for each extant cell with horizon H_i=t_{i+1}-t_i, where t_i=ceil(2^i/eps), H_i=Theta(2^i/eps) for standard eps constant and non-degenerate epochs.
- Algorithm2 threshold T0=9 log(H_i)/eta (eta is its local input privacy parameter), noises integer Lap(2/eta); Appendix A proves a uniform per-window noise threshold-good event of probability >=1-1/H_i, bounding at most 2H_i threshold/test noise variables by B=2(2log H_i+log2)/eta. On event every closed segment is nonempty. B6 separately made Binary Mechanism noise-prefix simultaneous bounds; here we specifically test the **unmodified threshold-good event failure**, the most likely bottleneck before Wasserstein propagation.
- Lemma4.2 is explicitly an EXPECTATION-based Wasserstein consistency lemma, not a directly cited high-prob theorem. Eq4.4–4.7 use expected per-cell noise and Jensen across 2^j spatial nodes to get E W1. Moving to high probability needs additional justification beyond replacing E|lambda| with a candidate uniform pointwise bound.

## One decisive counting argument [DERIVATION]
At time-level i, non-root cells active are all depths 1..i:
 M_i = sum_{j=1}^i 2^j = 2^(i+1)-2.
If each Algorithm2 window uses the Appendix-A event with failure <=1/H_i and we simply union-bound these events, the only bound this route provides on at least one threshold-bad window at epoch i is
 U_i = sum_{j=1}^i 2^j / H_i = (2^(i+1)-2)/H_i = Theta(eps)
when H_i=Theta(2^i/eps).
Across epochs i=1..r, the full simultaneous-event union bound is
 U_{<=r} = sum_{i=1}^r (2^(i+1)-2)/H_i = Theta(eps*r)
for a fixed nontrivial eps and the asymptotic epochs. This is the UNION-BOUND EXPRESSION, NOT a lower bound on the actual failure probability. Once >1 it is vacuous (probability upper bound min{1,U}). At a single deep epoch already U_i=Theta(eps), so for fixed eps one does not obtain failure o(1) through this direct argument.

Exact arithmetic example: eps=1, t_i=2^i, H_i=2^i, U_{<=r}=sum_{i=1}^r(2^(i+1)-2)/2^i = 2r-2(1-2^(-r)). At r=5, this evaluates to 8.0625; at r=10, 18.001953125. These values >1 have NO probability interpretation beyond vacuity. This is exact algebra without a stochastic simulation.

[NEGATIVE] H-B7 false: a straightforward union over unchanged original B6/Appendix-A threshold-good events cannot yield a high-confidence full-tree certificate. It does NOT prove any actual algorithmic error, impossibility, high W1, or new research novelty. The absence of a useful union bound says nothing about correlations between failure events, weighted aggregate losses, or alternative noise-tail allocations.

## What remains technically open and source-compatible
- A more stringent per-cell confidence beta_{j,i} with non-constant threshold B(beta) might allow a simultaneous event, but Algorithm2 hardcodes T0=9logH/eta. To preserve nonempty segments one needs T0>2B(beta), which may fail for aggressive allocation. This interface must be checked *before* assuming an easy union fix. It is possible weighting cells by diameters and/or controlling aggregate noise avoids full uniform success.
- For variable eps or small time levels, H_i=ceil(2^(i+1)/eps)-ceil(2^i/eps) has ceiling effects; Theta arithmetic is for nondegenerate relevant epochs. Exact eps=1 witness avoids ceilings.
- The original Theorem1.1 is fixed-stream E W1 (not an adaptive high-prob theorem). The offline source He–Vershynin–Zhu COLT2023 Theorem4.2, https://proceedings.mlr.press/v195/he23a.html, is an expectation theorem. A deterministic consistency/W1 coupling statement may underlie it, but was NOT fully reproved here. Do not assert a high-prob W1 theorem based only on citation of Lemma4.2.
- Mathematical proof-level barrier here may be resolved by standard confidence allocation or weighted expectation and may be too trivial for a paper. No publishable nontrivial obstruction established.

STATUS: FAIL_B7_NAIVE_UNMODIFIED_GLOBAL_UNION_CONFIDENCE
RESULT: Full spatial/temporal direct union of per-counter 1/H threshold-bad bounds has vacuous O(eps log(eps*t)) failure bound; source-level combinatorial mismatch quantified. No actual Wasserstein lower bound or code flaw proven.
NOVELTY: FAIL for naive certificate transfer; NOT_ESTABLISHED for adaptive Wasserstein/synthetic-data research line.
NEXT_TEST: Only upon PI approval for B8: with the exact original Algorithm2 threshold constant 9 and He Eq4.1 privacy allocation, inspect ONE high-confidence per-cell beta schedule for a fixed time r (e.g., beta_{j,i}~delta/number-of-active-windows), and calculate whether the required B(beta) still satisfies T0>2B for all relevant j,i. Kill if straightforward retuning suffices; do not assume algorithmic flaw or launch experiments.
PENDING_CODEX: NONE_REQUIRED_FOR_B7. Do not execute or provide Codex instructions until PI explicitly requests.
STATE_UPDATE: YES only after commit/write and readback of finding, negative archive and root STATE.
