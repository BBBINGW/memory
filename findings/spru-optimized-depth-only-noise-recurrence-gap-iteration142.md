# Iteration 142 — SPRU's optimized h=64 multiplication depth alone does not close the original proof's noise/scale gap

**Date:** 2026-10-13. Human PI said “好的，请继续” following I141, authorizing ONE new research iteration and selection from the long-term backlog. **One primary hypothesis + one exact recurrence/parameter falsifier.** MRFHE I139–141 remains parked due unavailable original non-power-of-two Lattigo custom source; no further generic MRFHE simulators run.

## Read before write / source and prior gate

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I141 (SHA `fe76f8400586a3a2455bbb52ca5fdda9387b09f9`) and `findings/OPEN_RESEARCH_BRANCHES.md`.
- Critical prior archive `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md` (I119): source Theorem1 unoptimized Eq.(8) sufficient condition fails to certify the different optimized Table2 circuit. This finding **does NOT prove any optimized correctness, precision or security failure**, merely absence of a directly applicable guarantee.
- Original FULL ePrint PDF from Research MCP: Jean-Sébastien Coron & Robin Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity* (SPRU), ePrint **2025/651**, https://eprint.iacr.org/2025/651, **42 physical pages**, GitHub mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, cache READY / VERSION_UNVERIFIED against official latest PDF. Directly re-read physical **pp13–16** §4.1–4.4, **pp22–24** Algorithm2 & Table2, **pp40–41** Appendix E. Corroborating arXiv version https://arxiv.org/abs/2607.27401 from web search is July2026, but original theorem and equations anchored to 42-page mirror.
- **Source §4.3 physical pp15–16:** optimized exact-one-per-block binary secret, h blocks of B=N/h positions each; each block's selector-weighted exp sum substitutes for local factor product; global product tree now **h** factors, depth log₂h; total core circuit depth ℓ_c=log₂h+1. This also introduces Tr_{N/2→h}, complex packing and special δ scaling: the actual optimized noise recursion is **not derived in the original Appendix E**. Thus one must NOT simply assert the Appendix E bound applies.
- **Source Appendix E physical p40–41:** original unoptimized real-component complex product tree has noise `E_i ≤ u_i N κ`, initial `u_0=14`, and `u_{i+1}=4u_i+16`. Source uses `Δ≥E_i²` for its conservative multiplication scale condition. Unoptimized full depth log₂N leads to upper estimate `20N³κ` and sufficient `Δ≥(20N³κ)²`. This is a *sufficient theorem-proof heuristic* for unoptimized Eq8, not a tight or necessary CKKS precision bound.
- **Source §6.1 physical pp23–24/Table2:** New boot. N=2¹⁵, h=64, ℓ_c=7, default scaling Δ≈2⁴⁹ (log q₀≈60, log q_i≈49, new boot. ℓ_m8 or9, precision around14bits). This optimized construction differs substantially from original proof circuit. Source §6 p22 explicitly gives public implementation URL https://github.com/coron/spru_boot.
- Fetched PUBLIC AUTHOR REPO using connected GitHub: `coron/spru_boot` `readme.md` blob SHA `42c442fc2035552500fa25039e430342b6f79605`, confirms OpenFHE v1.4.2 source/patch `patches/openfhe-ckksrns-protected.patch` and build+runner `test-new-bootstrapping`; `CMakeLists.txt` blob `7ee15e8462d2c0b553572fb61582f0929949a73e` defines executable and sources. This repository EXISTS and is source-qualified; NOT compiled/executed in I142, and none of its Gaussian sample/operation-specific noise estimates were measured. No author contacted.

## ONE testable technical claim

[HYPOTHESIS] The **depth reduction alone** in optimized SPRU, replacing the unoptimized log₂N-round multiplication tree by log₂h rounds, suffices to explain/certify the source Table2 Δ≈2⁴⁹ **while otherwise retaining Appendix E's per-level conservative noise recursion and its `Δ≥E²` scale condition**. If true, no circuit-specific noise lemma would be required at this first proof/parameter gate.

[FALSIFIER, cheapest] For source Table2 smallest allowed κ=1, N=32768 and h=64, iterate only original `u_0=14, u_{i+1}=4u_i+16` for log₂h=6 tree levels, set `E_6=u_6Nκ`, and check `Δ=2^49≥E_6²`. Failure disproves that depth-only transfer of THIS original sufficient proof certifies Table2; it does NOT disprove that the optimized circuit is correct or that some tighter analysis can justify Table2.

## Exact recurrence result (integer arithmetic)

```
 u_0 = 14
 u_1 = 4*14+16 = 72
 u_2 = 304
 u_3 = 1232
 u_4 = 4944
 u_5 = 19792
 u_6 = 79184

 N = 32768, h = 64, κ=1
 E_6 = (79184)(32768) = 2594701312
 log₂(E_6) ≈ 31.272921326867
 log₂(E_6²) ≈ 62.545842653734
 log₂(Table2 Δ) ≈ 49

 E_6² / 2^49 ≈ 11959.27783203125 > 1
 E_6 / sqrt(2^49) ≈ 109.358483127882 > 1
```

Thus the **modified-depth but unchanged-original-recurrence** sufficient scale condition would require **log₂Δ≥~62.55**, not 49. The conservative symbolic bound `u_6≤20*4^6−6=81914` gives `log₂(Δ)≥~62.64` (also fails). The unoptimized original I119 Theorem1 with N=2¹⁵ would require log₂Δ≥98.64. **The new 13.55-bit gap is NOT the same claim as I119's original 49.64-bit mismatch.**

Crucial: This is a FAIL of the *proposed proof-transfer argument*, **not** a derived lower bound `Δ_min` for any real optimized CKKS computation. The original unoptimized E0 and recurrence may be overly conservative or **structurally inapplicable** to optimized packed complex input, special δ scaling, trace and slot-to-coefficient stages. They were retained *hypothetically* as the precise falsifiable premise. It would be logically invalid to claim the original Table2 parameters fail because a sufficient condition fails or because an inapplicable recurrence is not met.

## Result and interpretation

- [PASS exact falsifier / FAIL hypothesis] Using the source's entire unchanged per-layer conservative recurrence, replacing only tree depth to 6 still needs scale 2^62.55; Table2 uses 2^49. A **genuine circuit-specific** bound must change *more than product depth*, e.g. exploit native-complex packed multiplication, trace selector sparsity, δ scaling, actual fresh encoded RLWE noise, optimized multiplication propagation and particular slot target; or prove directly suitable error distribution with sufficient success probability.
- [NOVELTY] Simple unrolled recurrence, **not** publishable mathematics and not source paper's correctness flaw. I119 already established mismatch of *unoptimized theorem* and optimized settings; I142 refines the cheapest possible rescue attempt and shows it is insufficient by ~13.55bits, a modest research process improvement. Source code publicly available for deeper genuinely different tests.
- [OPEN] An actual new trace-aware refined analytical proof and/or rigorous input-specific distributional error bound matching Table2 ≈14-bit measured precision. No new theorem yet, and source claims empirical precision rather than formal proof extension to optimized path in examined sections.

## End of iteration

**STATUS:** FAIL depth-only carryover of Appendix E proof for source Table2 / PASS exact integer recursion and 13.55-bit residual certificate gap / HUMAN_REVIEW.
**RESULT:** Six-level update of source E-inequality gives E6=2,594,701,312 at N=32768 κ=1, so unchanged `Δ≥E²` requires log₂Δ≥62.5458; measured source config Δ≈2^49. Need new circuit-specific propagation analysis, not merely log-depth adjustment. OpenFHE SPRU author source confirmed accessible; no compiled CKKS test.
**NEXT_ACTION:** I143 only if PI authorizes: choose exactly ONE actual optimized-circuit operation (suggest **Tr_{N/2→h}** before log₂h product tree) and inspect source code/Appendix lemmas to determine **an improved deterministic or high-probability per-slot error invariant**, with a toy/error input that could kill the bound. Do NOT assert 2^49 is unsafe or try to fully reprove entire paper. If proof refinement is routine/not novel, PARK after cheap falsifier and choose another meaningful FHE target.
**STATE_UPDATE:** YES — this materially resolves an obvious (and previously untested) I119 repair shortcut and establishes a precise residual proof requirement, with accessible official author implementation.
