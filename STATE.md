# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V29 COMPLETED**, next **V30 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V29 investigated whether two Galois automorphism invariance gates plus a root polynomial and the source Remark4.1 permutation arithmetization could enforce canonical common bounded integer digits across the original composite-RNS CRT factors. PASS a useful restricted lemma: for odd prime p, N>=4 power2, sigma_-1 and sigma_5 fix precisely the scalars Fp in Fp[X]/(X^N+1); exact source-compatible N4/8/16 rank tests confirm. FAIL the proposed cheap complete repair: q=13*29,h=261 has digit residues1 and0, satisfies ALL genuine Galois invariances and h(h-1)=0 mod377, but is not global digit0/1. Also the ring-linear permutation/recomposition portion of source Remark4.1 alone does NOT authenticate actual automorphism: without independently certified scalar-coefficient vector, fake w=(e,0,0,0) with e=7+4X^2 yields false claimed equality though sigma7(e)=1-e. This is a failure of OUR deliberately incomplete integration, NOT a published proof error; the authors explicitly describe scalar coefficient witnesses. Latest Feb2026 full paper remains VERSION_UNVERIFIED; no actual full SNARK exploit or proven low-cost noncircular cross-prime patch. Full source-grounded §38 index and findings/vfhe-v29-galois-scalarity-bridge.md, independent V29 checkpoint. V30 next: test ONE independently sound coefficient-extraction / authentic automorphism interface and its cross-prime integer-link F.1/F.2 PCS cost against V12–V16, else PI HUMAN_REVIEW/pivot. No author outreach without PI. GLOBAL I192 remains FROZEN.

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
