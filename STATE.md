# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V25 COMPLETED**, next **V26 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V25 FALSIFIED an append-only additive hiding repair of native F.2 PCS row-vector disclosures. Under inspected ePrint2025/286 mirror §5/Appendix F.2, publicly sent v=rU_f and v'=q1U_f are checked against encoded Merkle-committed U_f and original y=f(a). Mask v/v' alone violates native coding; mask the precommitted U_f as well and authenticated code equalities pass, but the claimed y changes by a nonzero precommitted mask b(a), with chance of accidental equality ≤ell/|F| for a uniform high-entropy native field query. Exact source-form F113² [4,2]-RS test: original y=(57,32), b(a)=(3,58), masked y=(60,90); 4096 deterministic random-mask trials and 16384 linear-code checks corroborate. This is a candidate REPAIR failure and interface requirement, not an attack or original ZK fault. V24 direct shared-small-integer point repair and companion unmasked MLE privacy leakage also fail cheap shortcuts. V20 INSPECTED-MIRROR ideal Pi_range false-witness evidence remains source-version-gated; official Feb2026 full PDF and real compiled SNARK exploit unresolved. V26: a published hiding PC or actual mask-cancellation commitment/proof architecture with F.1/F.2 security and cost. See findings §34 and separate vFHE state. General I192 FROZEN.

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
