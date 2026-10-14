# FHE Research State — vFHE cross-CRT consistency after I194

**Checkpoint date:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED ITERATION:** **I194 COMPLETED**; **I195 NOT STARTED**.
**STATUS:** **FAIL** narrowly scoped row-weight-2 single-prefix-code family; **OPEN/HUMAN_REVIEW** for parent cross-CRT shared integer commitment; NOVELTY NOT VERIFIED. No active technical hypothesis until PI selects next test.

## CURRENT TARGET (PI-selected)

vFHE common scalar digit/index consistency across CRT fields. Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, https://eprint.iacr.org/2025/286. Original primary 52pp Research MCP GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official parity VERSION_UNVERIFIED.

**Gap [DERIVED I59–I60]:** CRT-product fieldwise digit lookups enforce rectangular per-field membership, not a common diagonal scalar digit. Exact ring-idempotent witness in `R=Z77[X]/(X²+1)` uses h56→(0,1), ideal polynomial-oracle proof accepts a false range relation; original §5 componentwise PCS does not itself cure the abstraction. **Not** authenticated end-to-end SNARK exploit or verified latest-edition vulnerability. Original existing RS-coded column direct integer comparisons FAIL honest completeness (I151); other cheap PCS/lookup repairs archived P1.

## LATEST TEST / EVIDENCE

**I193 positive toy gate:** one 8×8 integer A with each row two 1s, `E_A(x)=(x,Prefix(xA))`, m8,p29/p37,beta2: identical honest bounded integer encodings and minimum weight3/16 over odd-characteristic extension fields. **Finite toy only.**

**I194 decisive negative theorem:** For **every** binary m×m matrix A with exactly two distinct 1s per row, over ANY odd-characteristic field or its extensions, systematic single-prefix code `E_A:F^m→F^{2m}` satisfies `d_min=O(sqrt(m))`. Proof models rows as graph edges: even alternating paths with close numeric endpoints, small-component signless-incidence dependencies, even cycles, or paired odd cycles. Parallel rows yield distance≤2. Therefore **relative distance O(1/sqrt(m))→0**: exact row-weight-2 + one accumulator specialization is UNUSABLE as constant-distance Brakedown/PCS code. Source-size direct cyclic witness x=e0−e1 yields codeword weight4 for every m≥4: m256 4/512 (0.78125%) and m1024 4/2048 (0.1953125%). Additional graph instances independently checked. This is an established algebraic obstruction to this specific encoding, NOT a universal impossibility of small-integer coding, shared commitments, or vFHE repair. Novelty of theorem itself not established.

**TOPIC HOME / DETAILS:** `findings/vfhe-cross-crt-consistency-research.md`, §11. This topic file is the PRIMARY place for subsequent subject-specific results; do not force research into more numbered findings files. Existing numbered findings kept as provenance. Local reproducible script `/mnt/data/vfhe_cross_crt_row2_distance_obstruction.py` SHA256 `955966c21c37f2eba1e6b247405dcf8b88ae4a75dfc41ec1e91c54222053a3f7`; results SHA256 `eb6cbce53c3acfebfdcd7a1673f212b114128d215bd8368b58d95269373c61c9`. Local files not automatically accessible to MCP.

## MAIN OPEN OBSTRUCTION

A usable shared canonical integer-code/Merkle bridge requires a DIFFERENT fast, small-integer, positive-constant-distance code **with proof over all CRT extension fields and honest no-wrap**. Even if found, one must establish shared commitment binding, field-specific F.2 evaluation integration, hiding/ZK for small indices, Fiat–Shamir and global 128bit soundness, and total protocol cost; no working repaired vFHE exists.

## NEXT_ACTION — conditional, requires PI to continue

**One candidate/one minimal test**, to be selected by PI: pick ONE distinct encoder class (e.g. fixed degree≥3 *or* double interleaved accumulator, not both in same iteration); before PCS work seek an explicit o(m)-weight codeword family or derive a positive distance argument under bounded-integer coefficients and source no-wrap constraints at m256/m1024. Also check known RA/RAA and field-agnostic PCS prior art before claiming novelty. Do not resurrect row-degree2 with single prefix. No external author contact/disclosure without PI approval.

## OTHER BRANCHES

AKU ePrint2025/381 I190–192 PARKED SOURCE_VERSION_GATED; LFBS PRCA I188–189 hoisting/bookkeeping PARKED; threshold FHE PRSS I184–187 direct repairs PARKED; GBFV and dBFV→BGV cheap ideas, GL generic BigSwitch archived per `findings/OPEN_RESEARCH_BRANCHES.md`. Preserve history.

**Agent protocol:** ONE hypothesis and ONE cheapest decisive test per authorized turn, [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN] provenance, read before write; PI decides research direction and strategic pivots.
