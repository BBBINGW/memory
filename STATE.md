# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V41 COMPLETED (PROVENANCE_CORROBORATED)**, next **V42 NOT STARTED (HUMAN_REVIEW / SOURCE_VERSION_GATED)**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V41 discovered independently verifiable source revision evidence NOT previously in V40. The cached 52pp GitHub-mirror ePrint2025/286 PDF (Research MCP SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; 836746 bytes; Git blob a549654c5dffa3484e95e8244056f4a27c48c3e6) has PDF Info **CreationDate and ModDate 2026-02-16 10:30:27 +01**, exactly official IACR 2026-02-16 Theorem4.8 proof-revision date; the public GitHub mirror path was ADDED on 2026-04-28 at commit 03d21d9516bb8a5ae39c9882194c252fbd7c2a25, absent from preceding commit. GitHub fetch_file actual PDF bytes/blob match Research MCP cache revision and size. This strongly corroborates an actual February revision BUILD, but the third-party PDF metadata and later mirror commit do NOT supply the official current IACR SHA; thus official byte parity CURRENTLY UNVERIFIED, original published-current theorem diagnosis remains SOURCE_VERSION_GATED. Re-read captured mirror p23 theorem extra bounds, p24 Remark4.9 correction and p48 AppendixE.2 false diagonal CRT implication; earlier e261 source-legal CRT range counterexample still applies to THIS mirror only, not a proven current-official exploit. Full finding `findings/vfhe-v41-feb2026-mirror-pdf-timestamp-provenance-gate.md`; local report with pinned SHA. V42 NEXT only SHA-authenticated official PDF comparison or explicit PI source-complete pivot; no public allegations, authors contact, or speculative large BP++ wrappers. GLOBAL general I192 remains FROZEN. MISSING_SOURCES.md remains OPEN.

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
