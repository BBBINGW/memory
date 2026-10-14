# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-15 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V38 COMPLETED**, next **V39 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V38 FAIL naive direct BP++ ePrint2022/510 ONE-precommitted-VECTOR ZK circuit with ONLY 2*d=8 native RNS quotient rows, but PASS actual paper's genuine same-vector commitment input mechanism under its OWN CRS. The original §5 source Eq(29)–(32) vector wV has dimension H; any f_l=1 or f_m=1 requires N_l=H or N_m=H, not just eight source quotient checks. Full toy p13/p29,d2,H8 native lifted y/quotients PASS with correct dummy factors; leaving dummy multiplication wires free makes the attempted simplified circuit UNSOUND, since bad native y can be absorbed by wL*wR. At H2^24 eight naive canonical coefficient rows comprise 134,217,728 cells (4GiB uncompressed 32B) and H input-sized constraints; no full BP++ prover or end-to-end vFHE benchmark. Full finding findings/vfhe-v38-bulletproofspp-vector-input-constraint-dimension-gate.md. NEXT V39/HUMAN_REVIEW seek OFFICIAL revised February2026 original source 2025/286 to decide if source-version gated actual Theorem4.8/Appendix E.2 gap survives before any further million-gate external proof engineering. General I192 frozen, SHIP I226 untouched.

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
