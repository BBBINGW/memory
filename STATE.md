# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V31 COMPLETED**, next **V32 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V31 PASS an exact but CONDITIONAL canonical integer CRT-link transitivity result, building on V30 prime-local native factor alignment and V14/V16 correct quotient reasoning. One genuine canonical vector a committed before challenges, each prime's k=N/d native F.1/F.2 factors authenticated/aligned at the same normalized random full-extension evaluation point, then ONLY ONE representative native factor per prime linked to the SAME a by a separately knowledge-sound non-native CP proof, is algebraically sufficient (identity failure≤ell/p^d plus PCS/CP errors) to bind all factors. Exact p13/p29,N4,d2,β4,H8 extension-field tests 8192 challenges per prime separately falsify single nonrepresentative-factor mismatches (only alignment detects) and crossprime/global-a mismatches (only representative CP detects); honest no rejects, exact two-coordinate integer quotients verified in external toy F1009. This is NOT an actual CP or published proof fix: original F.2 Merkle y→integer witness link, knowledge extraction, 128-bit proof/ZK/real cost and official Feb2026 source authentication remain OPEN. Conditional link count from 8192 native factorwise CP checks to 2 per-prime CP checks at illustrative N16384,d4,L2 is **not an end-to-end speedup**; 8192 native F.2 checks and ~134M direct integer arithmetic terms remain. Full finding `findings/vfhe-v31-transitive-representative-link.md`, detailed state `findings/vfhe-cross-crt-state.md`. Cumulative topic file reached MAX_FILE_BYTES, so separate finding is authoritative for V31. NEXT V32 authentic source PCS-bound crosscharacteristic CP implementation or HUMAN_REVIEW; global general FHE I192 FROZEN.

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
