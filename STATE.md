# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V26 COMPLETED**, next **V27 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V26 tested one real published ZK masking technique, HyperPlonk ePrint2022/1355 Appendix A.2 Lemma A.1 single-axis mask f*=f+X_j(1−X_j)R(X_j), against inspected vFHE2025/286 Fig1's SAME GP oracle queried at (r',0),(r',1). For all nonfinal j the mask shifts coincide and their difference cancels, exposing original oracle pair difference; for final j Z=0 at both Boolean endpoints, exposing both values. Thus NO axis meets HyperPlonk's published checker, and original vFHE F.2 multilinear Merkle/RS PCS cannot bind offcube evaluations of a nonmultilinear degree≥2 masked polynomial using the same Boolean MLE matrix. Exact F113² reproduction: 4096/4096 structural mask/query failures, 0 admissible axes. This FAILS only our drop-in masking repair idea, not HyperPlonk ZK or original vFHE confidentiality; neither full ZK + cross-prime common integer binding nor competitive cost is yet established. Original V20 IDEAL range PIOP gap remains restricted to inspected 52pp VERSION_UNVERIFIED mirror and Feb2026 official revision is byte-unverified. V27 next: ONE genuinely query-rewritten, degree-aware hiding PCS plus noncomponentwise shared bounded-integer CRT bridge (or recover official PDF), shortest falsifiable soundness/PCS-cost gate. No author contact without PI. See findings §35 and separate state; global I192 FROZEN.

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
