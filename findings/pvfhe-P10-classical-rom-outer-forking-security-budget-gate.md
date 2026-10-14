# PVFHE-P10 — Classical ROM selective-query reduction and square-root binding budget

**Date:** 2026-10-15 (Asia/Tokyo). **P10 COMPLETED; P11 NOT STARTED.**
**STATUS:** PASS conditional abstract outer-ROM query-slot derivation and exact finite test; UNCLEAR actual CMNW adaptive Fiat–Shamir PCS joint extraction, SIS instantiation, QROM and original PVFHE repair.

## Read before write and source
Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md SHA a7b184491083f027696160b6204f4ed75483cebe (independent vFHE V28), findings/pvfhe-P09-cmnw-slack-fiat-shamir-composition-gate.md SHA b992992fd2b1173d8128505c77b44eafc1343543 and P08 SHA 96b05e032688f16a5ae24e198a815acc8ed3214f. No shared state edits; destination absent before attempted write.
Sources checked via Research MCP: Huang et al. ePrint 2024/1764, full PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 (29 physical pp, pp8–9,21–22); Cini–Malavolta–Nguyen–Wee, CRYPTO2024/ePrint 2024/281, SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73 (52 physical pp, pp11–15,22–24,39). Both VERSION_UNVERIFIED. CMNW p39 counts 2^64 RO queries and chooses lambda192 for ITS OWN inner FS concrete example, NOT our composition.

## One primary hypothesis and decisive test
**[HYPOTHESIS P10]** Under an explicitly adaptive-online classical FS joint-extraction interface for CMNW's TWO related openings, the P08 fixed-commitment interactive two-fork bound admits an outer classical ROM selective-query reduction with Q_H+1 loss, rather than the unchanged bound falsified in P09.
**[FALSIFIER]** Identify whether a new H_ext query exposes a fresh uniform r *after its C is fixed* despite adaptive choice of future commitments, write the complete conditional reduction and security budget; reject any unconditional transfer of CMNW one-statement interactive extractor to an adaptive multi-proof FS/QROM extractor.

## Conditional classical ROM reduction [DERIVATION]
New proposed transcript (NOT source): fixed public statement/selector -> augmented masked witness commitment C -> external r=H_ext(domain,statement,selector,C) -> fix both claimed values v,v' -> two distinct domain-separated INTERNAL CMNW FS proofs, each binding branch label, C, r, v,v' and proof prefix -> check openings and v=sigma(v'), plus ordinary witness-selector linking.

Suppose for this entire extended protocol each inner FS proof has **adaptive online extraction** under arbitrary classical oracle auxiliary state, two accepted claims on one C jointly extract one valid polynomial except eps_K, and relaxed SIS binding at extracted 2beta_* controls two different openings by eps_B. Suppose false public statement implies every admissible extracted polynomial is non-sigma-invariant, and E has unit-pair differences. P08 then gives fixed-j external-challenge error <= delta+sqrt(eps_B)+eps_K, delta=s/|E|.

Classify an accepted ROM output by index j of its FIRST H_ext query for (statement,selector,C), or unqueried final hash case j=Q_H+1. Simulate adversary up to the chosen fresh query. C is determined by prefix, hence fresh r remains UNIFORM even if prior hashes influenced C. Reuse P08's CLASSICAL resettable two-fork argument and abstract online FS PCS extractor for this fixed query slot. Union bound the Q_H+1 disjoint slots:
  **Adv_bad_classical_ROM <= (Q_H+1)*(s/|E|+sqrt(eps_B)+eps_K).**
This is NOT a completed theorem for concrete CMNW FS proof: its published Definition6 covers SINGLE interactive evaluation knowledge extraction, not the required adaptive joint noninteractive extraction; state rewinding, oracle programming, proof-branch binding, extra witness linkage and runtime need proof. Cannot infer QROM by repetition. Source CMNW p22 beta_*=(2r_fold*kappa)^ell beta, while two extracted differences can have norm 2beta_*; source p24 single-PCS assumptions do not automatically instantiate this additional security requirement. Extended witness may alter folding depth.

## Executed minimal test and security budget
Actually executed Python /mnt/data/pvfhe_p10_rom_outer_slot_budget.py SHA256 637f416f635d85850be3cc7630ba19812912ddda0c1c908913be751afd9c031c.
Results JSON /mnt/data/pvfhe_p10_rom_outer_slot_budget_results.json SHA256 aebc0b8b49fcce7e47388e7cf7703b4947ac502ab78a00a834174c3471dd9864.
Report /mnt/data/PVFHE_P10_Classical_ROM_Outer_Slot_and_Slack_Gate.md SHA256 dff7b09a6ec34ff6db634496b6f9f6ddb5f20dbad7c36948a665ac30c2b917cd.

Tiny ideal RO challenge set F7 and 3 ADAPTIVELY determined target commitments t0=0,t1=(r0+1)%7,t2=(3r0+2r1+4)%7. For every prefix a fresh r_j equals t_j with probability 1/7. Exhaust 7^3=343 RO transcripts: 49 hits each slot, 127/343 any hit, exactly 1-(6/7)^3. This tests fresh query independence, NOT actual CMNW PCS/FS security.

**Main NEW proof cost:** A component of the bound is (Q_H+1)*sqrt(eps_B). At Q_H=2^64, target 2^-128, approximate componentwise threshold eps_B<=2^-384 (plus eps_K<=2^-192, |E|>=2^197 for s32); these at equality are NOT jointly sufficient. Exact Fraction arithmetic verifies the conservative combined allocation Q_H+1<2^65, |E|>=2^200, eps_K<=2^-195, eps_B<=2^-390 gives overall RHS <2^-128. If hypothetically eps_B=2^-192, Q_H sqrt(eps_B)=2^-32. **This is proof-technique weakness, NOT 32-bit real CMNW security nor a lattice attack.** Source CMNW p39's lambda192 concrete example should not be interpreted as an eps_B value for this new protocol.

## End
**STATUS:** PASS conditional classical abstract selective-query lemma and exact arithmetic; UNCLEAR full CMNW adaptive inner-FS joint extraction, real SIS norms/security, large E sampling, full FHE relation, QROM.
**RESULT:** Outer ROM requires Q_H+1 loss; current P08 sqrt(binding) additionally imposes severe binding security budget, motivating improved extraction or linear-binding-loss reduction.
**NEXT_ACTION (PVFHE-P11 only on PI continuation):** Falsify or establish ONE source-grounded mechanism to remove sqrt(eps_B) (prechallenge polynomial extractability or tighter linear-loss binding argument). If impossible/too expensive, PARK direct PCS integration under HUMAN_REVIEW. Do not run repetitive ROM toy audits.
**STATE_UPDATE:** YES only new independent P10 finding; NO edits to STATE.md, SHIP/vFHE, or previous P01–P09.