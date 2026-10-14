# FHE Research State — vFHE Cross-CRT Consistency after I195

**Checkpoint:** 2026-10-14, Asia/Tokyo.
**LAST COMPLETED ITERATION:** I195 COMPLETED. **I196 NOT STARTED.**
**STATUS:** FAIL for cyclic row-weight-two double-accumulator with any second permutation; root cross-CRT problem OPEN; candidate global common-integer-code proof system NOT CONSTRUCTED, NOVELTY NOT VERIFIED; HUMAN_REVIEW for next subbranch. No active test until PI authorizes next turn.

## CURRENT HUMAN-SELECTED PARENT TARGET

vFHE *cross-CRT shared scalar digit-index consistency*.
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286 (https://eprint.iacr.org/2025/286). Cached 52pp ePrint mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest VERSION_UNVERIFIED.

**KNOWN STRUCTURAL GAP [I59–I60]:** componentwise CRT-field digit table memberships enforce rectangular closure, not the same diagonal common integer digit. Toy source-form Ring `R=Z77[X]/(X²+1)` with `h56→(0,1)` gives source-level ideal PIOP counterexample under inspected mirror version; original componentwise F.1 PCS does not impose diagonal digit relation. NOT a validated deployed final-version SNARK attack, privacy failure or author-confirmed vulnerability.

## THIS ROUND I195 (ONE PRIMARY HYPOTHESIS, ONE TEST)

**Primary hypothesis (falsified):** adding a second arbitrary permutation and prefix accumulator to the fixed row-two cyclic integer expansion `A_i=e_i+e_{i+1 mod m}`, via
`C_pi(x)=(x,U(xA),U(P_pi U(xA)))∈F^{3m}`, could restore asymptotically positive relative distance.

**[DERIVED PASS mathematical counterexample; FAIL hypothesis]** For EVERY pi and m≥64, let B=ceil(2sqrt(m)), group second-stage output positions into B-blocks. Among nonoverlapping adjacent input pairs `(i,i+1)` with even i, pigeonhole yields distinct i,j whose two permuted position pairs lie respectively in the SAME two short blocks. Binary bounded-digit difference `x=e_i−e_{i+1}−e_j+e_{j+1}`, equal to `(e_i+e_{j+1})−(e_{i+1}+e_j)`, has `wt(x)=4` and `U(xA)=e_i+e_{i+1}−e_j−e_{j+1}` of weight4; after pi each block has +1 and −1 and the second prefix is supported in at most `2(B−1)` positions. Hence
`d_min(C_pi)≤2ceil(2sqrt(m))+6`, `d_min/(3m)=O(m^-1/2)`, uniformly for all second interleavers, over all intended odd-characteristic extension fields and even within legal {0,1} digit pairs. This definitively kills **that concrete cyclic first-stage double accumulator**, not all RAA encoders.

**[EXPERIMENT]** Exact integer and modular checks F29,F37,F65537 for m256/1024, identity/reverse/seeded random permutation all PASS. Witness wt: m256=11,11,32 of768; m1024=11,11,70 of3072. Theorem caps respectively70,134; results are explicit upper bounds not actual d_min. Local script `/mnt/data/vfhe_cross_crt_double_accumulator_gate.py` SHA256 `558b5daa8ac9782f97bf2d5c25e4d41b704e755f4aa206c68ca0e57a3a7d4a20`; output JSON SHA256 `e89ed32b6d9780e480ba3b395ab05c31875f9099356aa11edb1f72ce8d61709a`.

**Honest no-wrap conditional:** for x in [0,beta−1]^m, the second prefix ≤2m²(beta−1); for m1024,beta2^20 this is <2^41<2^48. The negative result is distance, not necessarily modular wrap.

**[PRIOR ART]** Kliewer et al. *Coding Theorems for Repeat Multiple Accumulate Codes*, arXiv0810.3422, proves linear growth for specified classical RAA random-interleaver ensembles, not for this fixed cyclic-first layout or arbitrary odd-characteristic extension fields. IEEE ISIT 2008 `Explicit Interleavers for a Repeat Accumulate Accumulate (RAA) code construction` likewise specifically addresses nontrivial interleaver design. **Do not call double accumulation in general impossible.**

## TOPIC HOME

All precise math, proof, context, negative evidence, assumptions: `findings/vfhe-cross-crt-consistency-research.md`, **Section 12**. This is the topic-level independent Markdown research file requested by PI; do not create another numbered findings file. Section 11 preserves I194 uniform O(sqrt(m)) failure for all row-two single-prefix matrices. Older I193 toy remains a correct finite necessary algebraic check, but not scalable evidence. Other archived failures in `findings/OPEN_RESEARCH_BRANCHES.md` P1, particularly original field-dependent RS Merkle column failure I151.

## MAIN UNSOLVED PROBLEM

A true global consistency repair needs a cross-CRT-binding commitment to ONE canonical bounded integer digit vector, with some fast code of POSITIVE constant relative distance simultaneously over all native extension fields, sufficiently small honest encoded integers (no-wrap), a complete new PCS proximity/extraction protocol, privacy/ZK, Fiat–Shamir, 128-bit security accounting, and source-comparable end-to-end cost. No such complete protocol or valid speedup is proved.

## NEXT_ACTION — only if PI requests continuation

One distinct test of **genuine two-independent-interleaver** repetition-two RAA-inspired small-integer code, where first interleaver is not frozen to cyclic layout. Establish an explicit general-field/canonical-integer distance bottleneck or cheapest precise counterexample, before full PCS implementation. Literature's *binary* random-interleaver linear-distance theorem cannot simply be assumed to cover the actual integer code over large odd primes/extension fields. On a failure, park the exact candidate; no automatic target pivot.

## OTHER ARCHIVES

AKU 2025/381 (I190–192) source-version gated; LFBS PRCA I188–189, threshold PRSS I184–187, GBFV/dBFV→BGV and GL BigSwitch branches remain as previously recorded. Read before write; single hypothesis/test; human PI selects major strategic decision and any author contact/disclosure.
