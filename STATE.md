# Global FHE Research State — Independent vFHE Track

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**GLOBAL GENERAL FHE ITERATION COUNTER:** **I192 is the last completed global round. This counter is FROZEN** while the human PI directs independent vFHE work. Do not start I193+ as a continuation of the old general sequence merely because the vFHE project continues.

## CURRENT PI-SELECTED WORKSTREAM (SEPARATE COUNTER)

**vFHE cross-CRT scalar digit/index consistency**, independent round **V32 COMPLETED**, next **V33 NOT STARTED**.

**Authoritative separate round state:** `findings/vfhe-cross-crt-state.md`.
**Technical evidence + research story:** `findings/vfhe-cross-crt-consistency-research.md`.
**Current status:** V32 PASS an actual auditable but CRYPTOGRAPHICALLY INSECURE toy Pedersen-bit/OR-Schnorr + quotient/Schnorr native-to-cross-prime linking interface: original source Appendix F.2 Merkle/RS PCS PUBLICLY authenticates y first, then third-field proof takes EXACT same y as common public input rather than rechecking SHA/Merkle within SNARK. Exact p13/p29,N4,d2,ellstar3,H8,beta4 honest native F.2 and 36 OR plus four aggregate Schnorr proof verifications pass; native mixed CRT261 (mod13=1,mod29=0) with shared canonical a0 passes independent native F.2 but is rejected by p13 integer CP. Group subgroup order r1009 is trivial to break, so NO actual 128bit soundness, proof extraction, FS composition, zero knowledge or original source compiled exploit established. Nonaggregated source-sized H2^24,beta4 cost ~1GiB Pedersen bit commitments plus ~6GiB OR proof transcript; NOT practical, not a lower bound. V32 standalone finding `findings/vfhe-v32-public-y-cp-glue.md`, V32 checkpoint in separate state. **NEXT V33** evaluate one published succinct aggregate bit/vector proof retaining authenticated public F.2 y or human-review source version; global FHE I192 FROZEN.

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
