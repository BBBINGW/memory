# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V42 COMPLETED (SOURCE_BLOCKED)**, next **V43 NOT STARTED (HUMAN_REVIEW / NO AUTO CONTINUATION)**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V42 SOURCE_BLOCKED / HUMAN_REVIEW after live official ePrint2025/286 page shows 2026-02-16 revision/fixed Theorem4.8 proof, but no official CURRENT PDF binary bytes or SHA256 are accessible: official PDF web index stale 50pp; versions click/screenshot fail; direct container official HTTP/DNS and independent download fail; fresh variants and independent Asia mirror paper PDF unavailable. Research MCP still returns unchanged 52pp mirror Git SHA a549654c5dffa3484e95e8244056f4a27c48c3e6, PDF SHA 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19 with VERSION_UNVERIFIED, though V41 independently documented PDF build metadata dated 2026-02-16 and Apr28 later mirror commit. NO official byte parity, actual current published Theorem4.8 diagnosis, or full source SNARK exploit established. An offline SHA byte comparison tool is prepared and self-tested (source record findings/vfhe-v42-official-current-pdf-byte-gate.md, local complete report /mnt/data/VFHE_V42_Official_Current_PDF_Byte_Authentication_Gate_2026_10_15.md). MISSING_SOURCES.md original official current PDF remains MISSING_CURRENT_OFFICIAL_BINARY; do not mark resolved. V43 NOT STARTED; HARD HUMAN_REVIEW, no more speculative BP/IPA/wrapper research without official paper bytes or explicit PI pivot to source-complete FHE. No author outreach/public disclosure. Global general I192 FROZEN, independent SHIP state unchanged.

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
