# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V34 COMPLETED**, next **V35 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V34 FAIL proposed off-the-shelf Spartan/R1CS **postchallenge existential a** as a replacement for PRECOMMITTED global canonical CRT digit witness. Original native per-prime constant1 (p13) and constant0 (p29) oracle commitments can both be valid; when full extension evaluation points are known, a single legal bounded a can be selected afterward to satisfy their two fieldpoint claims in 372/1024 exact random toy trials, despite incompatible Boolean digit tables. Strong succinct R1CS PoK is not a temporal prebinding relation across separately committed native PCS. Quantified H2^24 naive bit-gates/canonical-lift linear coefficients and original Spartan 2019/550 source §2.1. Full finding `findings/vfhe-v34-spartan-postchallenge-adaptive-integer-witness-gate.md`; V35 requires actual PRECHALLENGE compact VC/external proof and binding to original native F.2 y. Existing V31/V32 conditional positive link NOT refuted. Latest official original vFHE Feb2026 PDF remains VERSION_UNVERIFIED. Global I192 remains frozen.

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
