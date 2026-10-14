# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V36 COMPLETED**, next **V37 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V36 PASS algebraic same-commitment arbitrary-weight IPA interface after extending the original Pedersen subvector C_a with its blinding exponent omega as an IPA witness coordinate, toy proof 4/4 valid native rows and all tampered sums rejected; BUT FAIL hoped-for 'no additional disclosure beyond original F.2 public y'. Exact native source-form p13/p29, d2, ellstar3, beta4 digit vectors a=(0,0,0,0,0,0,2,0), b=(0,0,0,0,1,3,0,0) give identical F.2 public y=(6,5,12,10), yet different integer lifted sums (6,18,12,10) vs (32,44,70,39), so publishing IPA integer S leaks extra quotient information if such hiding is required. Original Bulletproofs §3 IPA is expressly NOT zero knowledge. At H2^24 simple blinding-coordinate IPA padding to 2H costs ~2.15B source-symbolic group exponentiations across eight rows, despite ~13KB idealized proof bodies; exact Yang structured SRS security and full FS composition unverified. New finding `findings/vfhe-v36-same-commitment-ipa-privacy-and-work-gate.md`; V37 NEXT source-audit ZK arbitrary-linear on SAME C or privacy-preserving hidden-quotient PoK with honest prover cost, else HUMAN_REVIEW/PARK. V31/32 conditional positive remains, Feb2026 original PDF VERSION_UNVERIFIED, global I192 remains frozen.

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
