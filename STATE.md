# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V27 COMPLETED**, next **V28 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V27 FALSIFIED an overbroad reading of V26's single-axis HyperPlonk masking impossibility: a two-variable Boolean-vanishing mask M(X,Y)=X(1−X)(A+BY+CX) maps three independent uniform extension-field random coefficients to three jointly uniform masked same-oracle offcube values at (x,0),(x,1),(z,t) whenever x,z are nonBoolean/distinct; determinant Z(x)^2 Z(z)(z−x). Exact source-shaped F113² test passed 4093/4093 nondegenerate random inverse checks and 16,372 Boolean zero checks. This **partial query-aware privacy** result does NOT yield full vFHE lookup ZK: original Figure1 fixed Boolean root (1,0) remains unmasked and the mask's degree 3 exceeds F.2 MLE-only PCS; requires reengineered sumchecks and degree-aware hiding commitments. Furthermore privacy never alone fixes V20 CRT rectangular-vs-diagonal scalar-digit soundness; source has a 52pp VERSION_UNVERIFIED mirror and Feb2026 official PDF remains unverified. V28 NEXT one full-source root-hiding/degree-aware PCS gate or PI-directed re-focus on canonical CRT integer linking and official source. No author outreach. See findings §36 and separate vFHE state; global general I192 FROZEN.

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
