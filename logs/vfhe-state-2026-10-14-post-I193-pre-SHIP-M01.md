# Archived STATE.md before independent SHIP-M01 pivot

Preserved verbatim below, source `STATE.md` GitHub blob SHA `de08a0d82d905de5d386c7902022828f30a5cf6b` on 2026-10-14. vFHE I193 remains completed, I194 not started. This is an archive only; SHIP uses independent M numbering.

---

# FHE Research State — after Iteration 193

**Checkpoint date:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED ITERATION:** **I193 COMPLETED**. **I194 NOT STARTED**.
**STATUS:** I193 necessary algebraic gate **PASS**; scalable protocol/security/performance **UNCLEAR**; `NOVELTY NOT VERIFIED`. **No active technical hypothesis during handoff**; vFHE is the PI-selected parent target, not a confirmed repaired protocol. Await PI before executing I194.

## CURRENT TARGET

**vFHE cross-CRT scalar-index consistency**, Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, https://eprint.iacr.org/2025/286. Primary source 52pp Research MCP GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; publisher/latest official byte-equivalence VERSION_UNVERIFIED.

**Original gap [DERIVED I59–I60]:** native CRT-field lookup validates the rectangular product of digit tables, not the diagonal common scalar-digit relation. Exact source-form idempotent counterexample R=Z77[X]/(X²+1), h56, standalone and full ideal Pi_range PIOP, survives original componentwise §5/F.1 commitments under analyzed source. **NOT** an authenticated final-version compiled-SNARK exploit, nor confirmed actual deployed compromise. Prior I95, I136–I151 simple repairs archived: do not repeat direct RS Merkle column integer equality (FAIL honest completeness), same-point/one-point integer lifts, basic masked aggregations, shared challenge or Merkle-only batching.

## CURRENT QUESTION

Could a new **common bounded-integer encoded witness / shared Merkle coded-column commitment** bind all CRT factors to the SAME small integer digit, while permitting native field-linear PCS evaluation checks with adequate distance and with practical proof/privacy cost?

## MOST RECENT COMPLETED TEST: I193

[FACT/source] §5/F.1–F.3 of 2025/286 commits to prime-specific coded matrices and RS/NTT roots. Brakedown (ePrint 2021/1043) and field-agnostic Expand-Accumulate Codes (ePrint 2024/1871) supply linear-code/accumulator ingredients, but their arbitrary-field proofs do NOT directly imply a bounded integer common generator when random nonzero field coefficients are replaced by integer 1.

[DERIVED+EXACT] Toy systematic integer code Enc(x)=(x,prefix(xA)), m8,beta2,p29,p37, A eight distinct weight-two {0,1} rows. Honest encoded values ≤16<p_min29; hence identical integer-coded columns at both primes. Exhaustive 3^8−1=6560 bounded nonzero differences and an independent full odd-characteristic extension-field argument establish exact minimum Hamming distance **3/16**. A mismatch e7 vs e5 changes exactly 3 positions. Local executable `/mnt/data/i193_vfhe_universal_integer_ea_toy.py` SHA256 `70e27821a362761316d36c2f097ec1634b20349e00c8bcf566d33e07c67d7502` (LOCAL ONLY, not GitHub MCP accessible).

[OPEN / NOT PROVEN] Uniform constant distance for source m256/1024 and all odd-characteristic extensions; new **one shared integer Merkle commitment** PC binding/proximity and cross-field extraction; hiding and digit leakage; random-query order/FS; 128-bit parameter/error budget; actual total bandwidth/runtime at source security. Illustration only: one F.2 evaluation's raw columns and vectors could drop ~1237.5 MiB to ~37.53 MiB under mu6144,m256,t32 and 4-byte encoded integer IF all shared-column assumptions hold; **NOT** proven total vFHE gain. Novelty vs published codes/PCS NOT verified.

Detailed source, method, proof, caveats: `findings/vfhe-shared-integer-ea-column-bridge-iteration193.md`.
Original gap: `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`.
Earlier failed direct coded-column idea: `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`.
Further historical branches: `findings/OPEN_RESEARCH_BRANCHES.md` (P1), which is long-term index and not active-state authority.

## MAIN OBSTRUCTION

The I193 result proves only a SMALL toy code; it does not establish a family with **uniformly positive relative distance and O(m) or near-NTT encoding** on native fields when all generator coefficients are small bounded integers. Brakedown/EA arbitrary-field analyses use field-dependent random coefficients. Even a suitable code would require an entirely new shared-commitment soundness and privacy proof; original fieldwise commitments do not automatically enforce diagonal digits.

## NEXT_ACTION — I194 only if PI confirms CONTINUE

**ONE decisive source-sized integer-EA distance gate:** For a specific sparse {0,1}-coefficient expand-accumulate code family inspired by Block et al. ePrint 2024/1871 §2–§4, analyze whether fixing all nonzero weights to 1 yields a constant lower bound on relative Hamming distance over *all* relevant odd-characteristic extension fields at m=256 or1024. Prefer search for an explicit low-weight/codeword or asymptotic cancelling pattern that kills distance, before any large implementation. If no distance survives, KILL this simple code specialization; keep abstract common-integer commitment problem but do not auto-launch a different research parent.

## PARKED / OTHER BRANCHES

AKU ePrint 2025/381 **PARKED — SOURCE_VERSION_GATED** after I190–I192; modeled Gaussian-DFR/table discrepancy conditional only, original author §5.1 rendered final chapter/code missing (`MISSING_SOURCES.md`). LFBS PRCA I188–189 simple hoisting/bookkeeping PARKED; threshold FHE PRSS I184–187 direct repairs PARKED; GBFV I182–183, direct dBFV→BGV I178–181, and GL generic BigSwitch archived/parked in branch index. Do not repeat these without new material premise.

Rule: ONE primary falsifiable claim and ONE cheapest decisive test per authorized iteration; read before write, evidence provenance, preserve archive, PI chooses all strategic pivots and public disclosure.
