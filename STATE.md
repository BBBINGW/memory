# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V23 COMPLETED**, next **V24 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V23 found a rigorous NO-GO for repair proposals adding only conjunctive R_q-polynomial constraints and existential ring-valued witness oracles: under CRT R_q≈∏F_k such relations are coordinatewise/product-closed, so cannot enforce a common small scalar digit diagonal across distinct CRT fields. Source-shaped R=F13[X]/(X⁴+1), e=7+4X²→(1,0) verifies degree-4 root equation although e is not a scalar 0..3; 250 deterministic exact random-ring-polynomial identity checks PASS. This eliminates only a precisely defined cheap repair class, not all possible cross-CRT ZK links. V20 IDEAL Pi_range false-range transcript, V21 illustrative mini-PCS challenge experiments remain strictly inspected 52pp version-unverified mirror findings, NOT an authenticated latest Feb2026 official published defect, complete 128-bit compiled SNARK exploit, or novel solution. Official IACR landing dates theorem-proof revision 2026-02-16; current exact PDF binary and complete released range verifier remain unavailable. V24 next: choose ONE genuinely non-componentwise shared-digit binding mechanism and falsify its soundness/cost using original F.1–F.3. See §32 independent research archive; keep MISSING_SOURCES unchanged and no author outreach without PI decision. General I192 FROZEN.

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
