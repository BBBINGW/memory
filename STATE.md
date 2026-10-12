# Research State — 2026-10-12

ACTIVE: **PaCo CKKS bootstrapping — paper-grounded correctness/precision boundary audit**.
PARKED: **RIG-HE**, previous full state `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
ARCHIVED: **GL generic BigSwitch** (`failures/gl-generic-bigswitch-structure.md`); **I88–94 vFHE bounded-public-A/native-Brakedown repair branch** (`failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`). The ORIGINAL vFHE CRT lookup correctness/soundness audit remains a retained research finding, NOT deleted or disproved.
COMPLETE PRE-HANDOFF STATE: `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` (verbatim I94 snapshot). Historical files in `findings/`, `failures/` preserved untouched.

## CURRENT TARGET
Jean-Sébastien Coron and Tim Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, ePrint **2025/886**.
Research MCP full 35-page GitHub mirror, SHA256 `ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a`; latest official binary **VERSION_UNVERIFIED**. Target sections §5.2–5.6 physical pp18–24, §7.2 Table4 physical pp25–26, §8.1 p28–29.
Previously explored newer papers ePrint 2026/975 and 2026/956 were **RETRIEVAL_BLOCKED** by Research MCP (official403, fixed mirror missing): DO NOT claim original technical knowledge from abstract alone; these are not currently critical to PaCo audit.

LAST COMPLETED ITERATION: **97 (2026-10-12)**. PASS source-linked pinned precision metric + input distribution; FAIL ideal-only 12/22 numerical reproduction: predicts 13.736/23.736 instead. Actual CKKS error decomposition OPEN. `findings/paco-precision-benchmark-metric-vs-ideal-bias-iteration97.md`.

PREVIOUS I95: PaCo negacyclic wrap handled by Algorithm4 line8, and vFHE high-cost direct repair archived.
PI's '好的，请继续' after I94 recommended archive/pivot was treated as approval to archive the narrowly scoped vFHE repair and run one new minimal PaCo test.

## CURRENT QUESTION
Now that I97 sourced the real author code precision metric (mean per-coefficient log difference) and exact message sampling (discrete uniform integer [-p,p]), can the ~1.74-bit shortfall from ideal-only 13.736/23.736 to paper's reported 12/22 be traced to an extra deterministic scale/rounding convention or only implementation/CKKS noise?

## PRIMARY HYPOTHESIS — NEXT NOT YET TESTED (I98)
The ideal circle bias model's assumption that the emitted plaintext integer equals round(q/(2π)sin(2πm/q)) may not match the author's `boot_to_nonboot` and `seq_PaCo` scaling/conversion code, even with no encryption noise. Falsifier: source confirms exactly the round(g(m)) coefficient scaling in ideal setting, leaving only the unspecified CKKS noise. One STATIC source check and ONE tiny algebraic test, no full Sage runtime.

## CURRENT EVIDENCE
- [PINNED ORIGINAL IMPLEMENTATION / METRIC CORRECTION, I97] Main PaCo repo `se-tim/PaCo-Implementation` commit `84a91afbd8558eb15facc66609cc1d0098e0da87`, benchmarks.py; that exact commit updates submodule gitlink to `se-tim/CKKS-in-SageMath` commit `2d7eab254f5be4daed5e2099be5d348abbe3ae07`, core `ckks_package/ckks.py`. Code calls `get_random_ciphertext(sk,C//2)`; core L600–643 generates C **independent uniform integer message coefficients** in [-p,p] at multiples of N/C (C=128/256 on source Table4). `CKKS_x.get_precision` halves C for superclass count, core L1505–1553 selects C corresponding symmetric decrypted coefficients and calculates **mean_i[log2(|pt_i|+1)−log2(|e_i|+1)]**, rounded 2 decimals per trial, averaged over num_tests. Initial pt is initial CIPHERTEXT DECRYPTION including fresh small Gaussian encryption noise, not exact sampled message. Ideal-only model `e_ideal(m)=|m−round(q/(2π)sin(2πm/q))|` over exact discrete generator yields 13.736120976 (PaCo I) / 23.736057929 (PaCo II), ~1.736 ABOVE paper's coarsely reported 12/22. This **corrects** prior I96 mismatched worst/RMS statistics; approximated sine explains 10-bit trend, NOT full observed average metric. Code and 1684 integer-error rounding thresholds independently verified with 70-digit mpmath for each parameter set. `findings/paco-precision-benchmark-metric-vs-ideal-bias-iteration97.md`. NO Sage/CKKS benchmark executed.
- [NEW QUANTITATIVE BOUND, I96] Source ePrint 2025/886 §5.3 physical pp19–20 ψ(m)=exp(2πim/q), g(m)=q/(2π)sin(2πm/q) and §7.2 Table4 p26 benchmark |m|≤p, PaCo I (logq29, logp22, reported 12 mean MSB bits), PaCo II (logq44, logp32, reported 22). Deterministic E(m)=|m−g(m)| is monotone in |m|≤p, and for x=2πp/q<0.05, p(x²/6−x⁴/120)≤E(p)≤p x²/6. High precision Emax=1684.20956 (I), 1684.41229 (II); normalized worst −log2(Emax/p)=11.282144, 21.281970 bits, vs reported 12/22 **average** bits. Leading Emax=(2π²/3)p³/q² and both have p³/q²=2^8; ideal error explains 10-bit separation but NOT necessarily dominant observed error, because average precision statistic and coefficient distribution unknown. Hypothetical continuous-uniform input gives normalized RMS 12.6858/22.6856 bits, not the author's measured statistic. `findings/paco-circle-small-angle-precision-floor-iteration96.md`. No CKKS implementation or publishable novelty.
- [NEGATIVE / SOURCE-VERIFIED, I95] Candidate gap: applying secret rotation in negacyclic `Y^C+1` to the circle-encoded polynomial should negate wrapped coefficients, so needs conjugation `ψ(−a)=conj ψ(a)`. Source Algorithm4 physical p24 **already uses `Conj(Rot_C(ct))` (line8)** and adds in line9. Exact F_103 primitive 17th-root toy tests: 8200 checked, all corrected outputs pass; naive no-conjugation wrong in 6832 tests. Do not claim source flaw from lossy overline extraction. Archive `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md`.
- [DECISION / ARCHIVE, I95] Direct bounded-public-A + native Brakedown repair is strategically archived due high cost and incomplete complete security/privacy/novelty, NOT because integer algebra fails. All original vFHE CRT lookup gap counterexamples and proof audit remain in old notes. `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`.
- [PRIMARY PARAMS] PaCo paper §7.2 physical p26 Table4: PaCo I (log N=15, log q=29, log p=22, log Δ=32, measured average precision 12 bits); PaCo II (log N=16, log q=44, log p=32, log Δ=48, measured average precision 22 bits). It states benchmark plaintext coefficient magnitudes at most p. §5.3 physical p19–20 circle/small-angle approximation. Exact coefficient distribution and noise level unverified.

## MAIN OBSTRUCTION
[ACTIVE OPEN] User-visible 12/22 PaCo Table4 precision is an **average of per-coefficient logarithmic bit preservation**, not worst-case -log2(E/p), RMS, or log-of-mean. Source generator samples uniform discrete integer messages, but the actual compared original ciphertext decrypts to **message + fresh encryption error** and PaCo adds approximation/rescaling noise. I97 predicts ideal-only 13.736/23.736 average bits, both ~1.736 above coarse source 12/22. Need one minimal STATIC source check of final plaintext scaling/rounding before claiming whether residual is operational CKKS noise; cannot claim dominant error or novel contribution.

## OPEN UNCERTAINTY
Author Table4 reported integer-bit precision is coarse, exact printed benchmark 2-decimal values and random trial seeds/output not present in paper. Actual rescale/key-switch/encoding error distribution and output coefficient quantization, precise input ciphertext initial Gaussian noise. Original PaCo PDF mirror latest official VERSION_UNVERIFIED; historical vFHE/RIG statuses preserved. No author contact/public disclosure authorized.

## NEXT_ACTION — ONE MINIMAL TEST (I98)
On exact PaCo main 84a91afbd8558eb15facc66609cc1d0098e0da87 and pinned CKKS submodule 2d7eab254f5be4daed5e2099be5d348abbe3ae07, inspect `seq_PaCo` constant `encoded_eta`, `boot_to_nonboot`, final plaintext polynomial extraction/rounding. Check ONE scalar-level ideal scale identity vs model round(q/(2π)sin(2πm/q)); if model sound, attribute unresolved 1.74-bit delta only to unknown operational noise/experimental reporting, STOP iterative ideal sine tuning absent a nontrivial technique. No full Sage CKKS implementation or performance benchmark.

## FILES FOR FAST RESUME
- `AGENT.md`, `RESEARCH_PHILOSOPHY.md` — one primary hypothesis/one decisive cheapest test, evidence provenance, read-before-write, commit and reread.
- `findings/paco-precision-benchmark-metric-vs-ideal-bias-iteration97.md` — last technical iteration; pinned author/main+submodule metric and 13.736/23.736 ideal mean bits.
- `findings/paco-circle-small-angle-precision-floor-iteration96.md` — prior deterministic worst precision, distinct metric.
- `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md` — corrected negacyclic wrap, archived test.
- `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` — archived direct repair; underlying original audit preserved.
- `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` — complete previous vFHE research state and file index.
- `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` — parked RIG state.

STATUS: **ACTIVE PaCo I98 final source-scaling check NEXT**. I97 PASS pinned input/mean-of-logs metric, FAIL ideal-only exact average explanation of Table4 within stated model. No actual CKKS performance proof or new technique; no author contact/public disclosure.