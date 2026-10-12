# Research State — 2026-10-12

ACTIVE: **PaCo CKKS bootstrapping — paper-grounded correctness/precision boundary audit**.
PARKED: **RIG-HE**, previous full state `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
ARCHIVED: **GL generic BigSwitch** (`failures/gl-generic-bigswitch-structure.md`); **I88–94 vFHE bounded-public-A/native-Brakedown repair branch** (`failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`). The ORIGINAL vFHE CRT lookup correctness/soundness audit remains a retained research finding, NOT deleted or disproved.
COMPLETE PRE-HANDOFF STATE: `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` (verbatim I94 snapshot). Historical files in `findings/`, `failures/` preserved untouched.

## CURRENT TARGET
Jean-Sébastien Coron and Tim Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, ePrint **2025/886**.
Research MCP full 35-page GitHub mirror, SHA256 `ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a`; latest official binary **VERSION_UNVERIFIED**. Target sections §5.2–5.6 physical pp18–24, §7.2 Table4 physical pp25–26, §8.1 p28–29.
Previously explored newer papers ePrint 2026/975 and 2026/956 were **RETRIEVAL_BLOCKED** by Research MCP (official403, fixed mirror missing): DO NOT claim original technical knowledge from abstract alone; these are not currently critical to PaCo audit.

LAST COMPLETED ITERATION: **95 (2026-10-12)**.
PI's '好的，请继续' after I94 recommended archive/pivot was treated as approval to archive the narrowly scoped vFHE repair and run one new minimal PaCo test.

## CURRENT QUESTION
Does PaCo's ideal circle-group small-angle recovery `q/(2*pi)*sin(2*pi*m/q)` impose a precision floor close to reported Table4 12/22 retained bits under the actual published `|m|<=p` benchmark setting, or is CKKS implementation noise dominant?

## PRIMARY HYPOTHESIS — NEXT, NOT YET TESTED (I96)
With PaCo I (log q=29, log p=22), PaCo II (log q=44, log p=32), ideal scalar bound `|m|<=p`, the relative deterministic circle-map linearization error is Θ((p/q)^2), which may itself explain most of the reported coefficient precision ceiling. Smallest falsifier: evaluate certified worst-case `|m−q/(2*pi)*sin(2*pi*m/q)|`, normalize to p or |m| as appropriate, and compare against Table4 'average most significant bits retained'. If precision metric or input distribution differs, mark UNKNOWN rather than equating an absolute worst-case with reported average.

## CURRENT EVIDENCE
- [NEGATIVE / SOURCE-VERIFIED, I95] Candidate gap: applying secret rotation in negacyclic `Y^C+1` to the circle-encoded polynomial should negate wrapped coefficients, so needs conjugation `ψ(−a)=conj ψ(a)`. Source Algorithm4 physical p24 **already uses `Conj(Rot_C(ct))` (line8)** and adds in line9. Exact F_103 primitive 17th-root toy tests: 8200 checked, all corrected outputs pass; naive no-conjugation wrong in 6832 tests. Do not claim source flaw from lossy overline extraction. Archive `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md`.
- [DECISION / ARCHIVE, I95] Direct bounded-public-A + native Brakedown repair is strategically archived due high cost and incomplete complete security/privacy/novelty, NOT because integer algebra fails. All original vFHE CRT lookup gap counterexamples and proof audit remain in old notes. `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`.
- [PRIMARY PARAMS] PaCo paper §7.2 physical p26 Table4: PaCo I (log N=15, log q=29, log p=22, log Δ=32, measured average precision 12 bits); PaCo II (log N=16, log q=44, log p=32, log Δ=48, measured average precision 22 bits). It states benchmark plaintext coefficient magnitudes at most p. §5.3 physical p19–20 circle/small-angle approximation. Exact coefficient distribution and noise level unverified.

## MAIN OBSTRUCTION
[OPEN] New PaCo challenge is separating ideal circle-map approximation bias from accumulated CKKS encoding/rescaling/key-switch noise and from average coefficient precision metrics. Need numerical bound before any claim of a novel precision optimization. Avoid overreading the statement 'zero failure probability' as zero approximation error; source explicitly uses small-angle approximation. No PaCo correctness defect or contribution has been demonstrated.

## NEXT_ACTION — ONE MINIMAL TEST (I96)
Read PaCo original ePrint 2025/886 §5.3 pp19–20, §7.2 p26 Table4 and precision definition, then analytically bound scalar Taylor remainder for g(m)=q/(2π)sin(2πm/q), m∈[−p,p] at the two published q,p pairs. Compare guaranteed worst-case error/relative error to published average 12/22 precision bits WITHOUT claiming equality; stop if hypothesis contradicted. No full FHE implementation or indiscriminate exploration.

## FILES FOR FAST RESUME
- `AGENT.md`, `RESEARCH_PHILOSOPHY.md` — one primary hypothesis/one decisive cheapest test, evidence provenance, read-before-write, commit and reread.
- `findings/paco-negacyclic-blind-rotation-conjugation-iteration95.md` — last technical iteration.
- `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` — archived direct repair; underlying original audit preserved.
- `logs/vfhe-state-2026-10-12-pre-paco-handoff.md` — complete previous vFHE research state and file index.
- `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` — parked RIG state.

STATUS: **ACTIVE PaCo I96 pending**. I95 falsified trivial missing-conjugation hypothesis by explicit source line. Prior vFHE repair branch archived with PI approval, original audit kept. NOVELTY NOT VERIFIED. No original protocol SNARK forgery or PaCo security claim. **NO AUTHOR CONTACT, EMAIL, OUTREACH OR PUBLIC DISCLOSURE** without explicit PI authorization.