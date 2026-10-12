# Research State — 2026-10-12

ACTIVE: **PaCo CKKS bootstrapping — paper-grounded correctness/precision boundary audit**.
PARKED: **RIG-HE**, previous full state `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
ARCHIVED: **GL generic BigSwitch** (`failures/gl-generic-bigswitch-structure.md`); **I88–94 vFHE bounded-public-A/native-Brakedown repair branch** (`failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`). The ORIGINAL vFHE CRT lookup correctness/soundness audit remains a retained research finding, NOT deleted or disproved.
COMPLETE PRE-HANDOFF STATE: `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` (verbatim I94 snapshot). Historical files in `findings/`, `failures/` preserved untouched.

## CURRENT TARGET
Jean-Sébastien Coron and Tim Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, ePrint **2025/886**.
Research MCP full 35-page GitHub mirror, SHA256 `ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a`; latest official binary **VERSION_UNVERIFIED**. Target sections §5.2–5.6 physical pp18–24, §7.2 Table4 physical pp25–26, §8.1 p28–29.
Previously explored newer papers ePrint 2026/975 and 2026/956 were **RETRIEVAL_BLOCKED** by Research MCP (official403, fixed mirror missing): DO NOT claim original technical knowledge from abstract alone; these are not currently critical to PaCo audit.

LAST COMPLETED ITERATION: **96 (2026-10-12)**. Conditional PASS exact Taylor precision boundary for PaCo I/II; actual dominant-error diagnosis UNCLEAR. `findings/paco-circle-small-angle-precision-floor-iteration96.md`.

PREVIOUS I95: PaCo negacyclic wrap handled by Algorithm4 line8, and vFHE high-cost direct repair archived.
PI's '好的，请继续' after I94 recommended archive/pivot was treated as approval to archive the narrowly scoped vFHE repair and run one new minimal PaCo test.

## CURRENT QUESTION
Is PaCo's observed experimental average retained-MSB precision really explained by small-angle circle bias, rather than CKKS noise? I96 derived the ideal error scale close to Table4; direct comparability requires author implementation's coefficient sampling and precision measurement definition.

## PRIMARY HYPOTHESIS — NEXT, NOT YET TESTED (I97)
The author's published PaCo proof-of-concept contains a measurement routine and coefficient sampling specification sufficient to reproduce or sharply bound the reported 12/22 average retained-bit metric from the ideal circle map alone. Falsifier: missing measurement definition/code, markedly different scaling convention, or ideal error not comparable to average due to actual distribution. Only inspect original source's relevant precision/input lines at pinned commit; no new FHE benchmark.

## CURRENT EVIDENCE
- [NEW QUANTITATIVE BOUND, I96] Source ePrint 2025/886 §5.3 physical pp19–20 ψ(m)=exp(2πim/q), g(m)=q/(2π)sin(2πm/q) and §7.2 Table4 p26 benchmark |m|≤p, PaCo I (logq29, logp22, reported 12 mean MSB bits), PaCo II (logq44, logp32, reported 22). Deterministic E(m)=|m−g(m)| is monotone in |m|≤p, and for x=2πp/q<0.05, p(x²/6−x⁴/120)≤E(p)≤p x²/6. High precision Emax=1684.20956 (I), 1684.41229 (II); normalized worst −log2(Emax/p)=11.282144, 21.281970 bits, vs reported 12/22 **average** bits. Leading Emax=(2π²/3)p³/q² and both have p³/q²=2^8; ideal error explains 10-bit separation but NOT necessarily dominant observed error, because average precision statistic and coefficient distribution unknown. Hypothetical continuous-uniform input gives normalized RMS 12.6858/22.6856 bits, not the author's measured statistic. `findings/paco-circle-small-angle-precision-floor-iteration96.md`. No CKKS implementation or publishable novelty.
- [NEGATIVE / SOURCE-VERIFIED, I95] Candidate gap: applying secret rotation in negacyclic `Y^C+1` to the circle-encoded polynomial should negate wrapped coefficients, so needs conjugation `ψ(−a)=conj ψ(a)`. Source Algorithm4 physical p24 **already uses `Conj(Rot_C(ct))` (line8)** and adds in line9. Exact F_103 primitive 17th-root toy tests: 8200 checked, all corrected outputs pass; naive no-conjugation wrong in 6832 tests. Do not claim source flaw from lossy overline extraction. Archive `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md`.
- [DECISION / ARCHIVE, I95] Direct bounded-public-A + native Brakedown repair is strategically archived due high cost and incomplete complete security/privacy/novelty, NOT because integer algebra fails. All original vFHE CRT lookup gap counterexamples and proof audit remain in old notes. `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`.
- [PRIMARY PARAMS] PaCo paper §7.2 physical p26 Table4: PaCo I (log N=15, log q=29, log p=22, log Δ=32, measured average precision 12 bits); PaCo II (log N=16, log q=44, log p=32, log Δ=48, measured average precision 22 bits). It states benchmark plaintext coefficient magnitudes at most p. §5.3 physical p19–20 circle/small-angle approximation. Exact coefficient distribution and noise level unverified.

## MAIN OBSTRUCTION
[ACTIVE OPEN] A simple known sine Taylor term yields ideal circle-map error ≈1684 integers and worst normalized precision 11.28/21.28 bits matching the *scale* and exact 10-bit difference of author's 12/22 **average retained coefficient bits**. However we must not equate worst-case error and average of a possibly different precision metric or infer small-angle bias dominates CKKS error. Need original author's input sampling and exact bit-count definition before further precision-optimization or claims of new contribution.

## OPEN UNCERTAINTY
Original PaCo PDF GitHub mirror official-version UNVERIFIED; actual coefficient distribution, measured error statistic, CKKS rescale/encoding noise, structured secret security; no new correctness/security break or novel improvement. Historical vFHE CRT lookup soundness discrepancy preserved; bounded-public-A direct Brakedown repair archived. No author contact/public disclosure authorized.

## NEXT_ACTION — ONE MINIMAL TEST (I97)
Inspect author's primary public repository `https://github.com/se-tim/PaCo-Implementation` referenced by ePrint 2025/886 §7.1 p25, using connected GitHub tool at pinned commit: locate *actual input coefficient generator* and *precision/bit-count calculation* for Table4 12/22. Compare exactly the author's statistic to I96 ideal deterministic bias for same input setting; if code or data absent, mark EVIDENCE MISSING rather than fabricate. No full implementation or broad parameter study.

## FILES FOR FAST RESUME
- `AGENT.md`, `RESEARCH_PHILOSOPHY.md` — one primary hypothesis/one decisive cheapest test, evidence provenance, read-before-write, commit and reread.
- `findings/paco-circle-small-angle-precision-floor-iteration96.md` — last technical iteration, conditional precision match.
- `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md` — corrected negacyclic wrap, archived test.
- `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` — archived direct repair; underlying original audit preserved.
- `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` — complete previous vFHE research state and file index.
- `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` — parked RIG state.

STATUS: **ACTIVE PaCo I97 source-code metric verification NEXT**. I96 analytic Taylor bound matches reported precision *scale*, not the measured average directly. NOVELTY NOT VERIFIED, no correctness/security claim. All vFHE/RIG preserved or archived as documented. NO AUTHOR CONTACT, EMAIL, OUTREACH OR PUBLIC DISCLOSURE without PI authorization.