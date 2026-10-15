# Immutable reference snapshot of previous global STATE.md

Captured 2026-10-15 before root STATE.md is converted into an index-only file. This is a *historical snapshot*, not an executable NEXT_ACTION. The original Git commit history also preserves this text. All active per-track states remain in their original files.

---

# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI STRATEGIC DECISION — 2026-10-15

**Active strategic theme (PI approved): NONTRIVIAL FHE OPTIMIZATION COMPOSITION OBSTRUCTIONS.** Seek a source-verified A+B incompatibility in CKKS/TFHE/FHEW bootstrapping, linear transforms, packing, matrix operations, moduli/scales, key-switch/rotation-key interfaces, noise/precision or security, then develop and verify a new technical repair R with formal and end-to-end cost evidence. Prioritize new structural understanding and clear baseline/novelty over minor paper bugs, simple overflow, known trade-offs, repetitive toy audits and missing-source conjectures.

**Historical integration:** findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md (read after core protocols); linked backlog findings/OPEN_RESEARCH_BRANCHES.md. Global I1–I192 FROZEN; V1–V43 independent; PVFHE P01–P27 independent; TFHE-ISA T01–T02 independent. Do not renumber P/T/V as I193+, do not conflate legacy backlog P1–P22 with PVFHE P01–P22. Existing findings/failures remain authoritative.

**Completed independent strands:** PVFHE P27 SOURCE_BLOCKED/HUMAN_REVIEW (author 2024/1764 compiler & Coeff helper-bit mapping missing); PVFHE PCS/FS P05–P22 PARK; TFHE-ISA T01 and T02 LOW NOVELTY/PARK. vFHE V43 source-text gate PASSED and historical CRT flaw author-acknowledged/repaired in Oct 2026; the old attack does not pass the new Figure 2. V44 not started/HUMAN_REVIEW; no full compiled-SNARG exploit claimed. Other source-blocked branches remain parked.

**NEXT_ACTION:** PI-approved research *selection* stage. Identify ONE genuinely new, full-primary-source-accessible FHE composition obstacle after checking historical findings, author discussions and prior art; write ONE smallest falsifiable technical hypothesis and decisive test. Do not automatically start any blocked legacy branch. PI retains ultimate target/contribution/pivot decision.

---

## HISTORICAL PI-SELECTED vFHE WORKSTREAM (SEPARATE COUNTER; OCT 2026 REVISION AUDITED)

**vFHE cross-CRT scalar digit/index consistency**, independent **V43 COMPLETED**; **V44 NOT STARTED — HUMAN_REVIEW / PARK RECOMMENDED**.

**Authoritative separate state:** `findings/vfhe-cross-crt-state.md`.
**Current one-round evidence:** `findings/vfhe-v43-oct2026-range-repair-gate.md`.
**Historical evidence:** `findings/vfhe-cross-crt-consistency-research.md` and `findings/vfhe-v42-official-current-pdf-byte-gate.md`.

**Current source status:** PI/user uploaded `papers/supplied/eprint-2025-286-official-2026-revision.pdf` (Git blob `3431dd8acbac7141cad2592d45eb13c38510b1e4`, 902276 bytes, **58 pages**); Research MCP read the actual new §§4.3/E.2. Live IACR landing reports **2026-10-01** second revision and a fixed **range-check protocol**. Author Remark4.12 p26 explicitly recognizes previous native CRT-component membership does NOT entail one globally bounded integer digit, and cites GlueLUT (ePrint2026/494). Revised Figure2 p26 + Theorem4.11 add an auxiliary F_p scalar-digit oracle and a native-prime integer congruence link. The precise older counterexample `e=7+4X²` (CRT `(1,0)`) cannot satisfy the new consistency check against scalar digits `0` or `1`; H-V43 old-attack transfer **FAIL**. No live-version flaw or compiled-security exploit proven. **Source TEXT is supplied/readable; raw official-origin PDF byte equivalence was not independently established** (public official PDF returned HTTP403); this provenance qualifier remains. `MISSING_SOURCES.md` updated to SUPPLIED_READABLE with caveat. Historical V42 blockage and 52pp mirror remain archived, not a current next action.

**NEXT_ACTION:** Human PI decides whether to close the historical vFHE cross-CRT bug-hunt and select one source-complete FHE optimization composition target (existing strategic preference), or explicitly authorizes a *new* sharply framed revised Figure2 cost/security optimization against GlueLUT. **Never jump from independent SHIP I226 or CGS-17 dialogues to this vFHE state on a generic “continue”.** General I192 frozen; other track files unchanged. No unsolicited author contact/disclosure.

### Legacy numbering mapping — provenance only

An earlier short run of vFHE exploration was inadvertently recorded as global I193–I196. Reinterpret only those *vFHE-specific* records as independent **V1, V2, V3, V4** in that order. This is a bookkeeping correction, not an erasure, renumbering of file paths, or change to the earlier *general* FHE I1–I192 history. Subsequent vFHE research begins at **V5**, and increments V6, V7, ... only. Existing vFHE theory/audit files from much older global iterations (e.g. I59–I151) remain historical evidence under their original filenames.

## GLOBAL GENERAL FHE WORKSTREAM — PARKED AT I192

**Last global audited topic (I190–I192):** Qi Zhang, Mingqiang Wang, Xiaopeng Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, CANS 2025, ePrint 2025/381, https://eprint.iacr.org/2025/381.

**Status:** PARKED — SOURCE_VERSION_GATED / HUMAN_REVIEW. Original author-edition §5.1 equations and exact DFR estimation/experimental artifact not authenticated. Existing discrepancy is conditional model/table comparison, **NOT** established published erratum, cryptographic exploit, or true DFR. For a future *PI-authorized* resumption, see archived I190–I192 evidence and `MISSING_SOURCES.md`. Do not conflate this with the currently active vFHE V-series.

Other branches including LFBS PRCA, threshold FHE PRSS, GBFV, dBFV→BGV and GL generic BigSwitch retain their prior parked/archived status in `findings/OPEN_RESEARCH_BRANCHES.md`.

## RESEARCH PROCESS

- Human PI chooses targets, major pivots, claims of contribution, and any disclosure.
- Agent follows `AGENT.md` and `RESEARCH_PHILOSOPHY.md`: read before write, one smallest falsifiable claim + one decisive test, rigorously distinguish FACT / DERIVATION / SPECULATION, verify every GitHub write by rereading.
- When working on vFHE, read its **separate state** and independent research file; do NOT use/increment the old 190+ global round sequence.
