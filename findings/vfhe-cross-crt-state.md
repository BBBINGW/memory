# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND:** **V13**. **NEXT:** **V14 NOT STARTED**.
**STATUS:** V13 **FAIL** one 128-bit global INTEGER scalar Fiat–Shamir challenge reduced into 49-bit CRT prime subfields as a one-shot 128-bit batch equality link; **PASS** precise legal two-Boolean-digit discrepancy with ≈1/p_i error and root cause (extension-field arithmetic ≠ extension-uniform challenge distribution). Whole cross-CRT canonical-int commitment, knowledge extraction, ZK/128-bit security composition, cost and novelty still OPEN.
**GLOBAL FHE I192 REMAINS FROZEN.** This is vFHE independent round numbering. Old vFHE I193–I196 aliases mean V1–V4 only and do not extend the general series.

## Independent round trajectory

V1: common bounded integer toy; V2–V3: degree-two/cyclic prefix low-distance negatives; V4: same-prime Fp→F_(p^d) code-distance invariant; V5–V7: small-support CRT-prime determinant/rank gates; V8: legitimate CRT prime divides a legal five-minor (not global attack); V9: global BOUNDED DIGIT integer difference distance inherits binary RAA under strict no-wrap, but not full native-field code distance; V10: sampled whole-codeword Merkle range not deterministic binding; V11: sampled systematic-only range loses distance amplification, one-digit mismatch passes 1−t/m; V12: third-field shared commitment without knowledge-sound per-native linking fails; **V13: 128-bit integer batching scalar modulo 49-bit native p yields only ≈48-bit error bound even when native arithmetic is F_(p^4)**.

## Human-selected parent target / original sources

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286 https://eprint.iacr.org/2025/286. Research-MCP read GitHub-mirror 52-page PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest revision VERSION_UNVERIFIED. §3.1 physical p10: native CRT primes p=1+2aN/d, odd a, native fields F_(p^d); Appendix F.2 physical pp50–51: field-native Merkle/field-linear PCS, NOT an ext-field-based cross-CRT shared integer group commitment.

Original cross-CRT parent issue [legacy general I59–I60]: per-component CRT scalar digit table proves rectangular rather than diagonal set; source-form ideal-oracle toy shows discrepancy; **NOT** authenticated compiled final-version SNARK exploit or an author-confirmed published flaw.

## V13 ONE hypothesis / ONE decisive exact falsifier

**[HYPOTHESIS FALSE]:** A postcommit shared 128-bit integer random challenge α, reduced modulo each source 49-bit p_i and interpreted as a scalar in F_(p_i^4), when used for ONE power-batched equality `Σ α^j(u_i,j−a_j)=0`, automatically affords ≥128-bit soundness for discrepant bounded canonical digit vectors across all CRT components, with no extra cross-field link overhead.

**[DERIVED/FALSIFIER PASS]** Let β=2, m≥2, a=(0,1,0…), native fake/legal u=(1,0,0…), so discrepancy d=(1,−1,0…). Both vectors individually LEGAL Boolean messages. Batched polynomial is 1−α, and falsely accepts iff α≡1 mod p_i, independent of F_(p_i^4)'s larger cardinality because the integer-reduced α is always in Fp_i. For uniform integer α∈[0,2^128−1], exact probability

    [floor((2^128−2)/p_i)+1]/2^128 ≈ 1/p_i.

Source-form N8192,d4 valid 49bit primes p1=281474976829441 and p2=353581838970881 satisfy p_i≡4097 mod8192 and verified prime. Concrete false-accept p1=3.552713677301223447e−15 (48.000000 bits), p2=2.828199556036458081e−15 (48.329038 bits). Adding HONEST components cannot improve the one-bad-component error.

**[CONDITIONAL OPTIONS, NOT REPAIRS]** Independent prime-field checks can compound soundness but must quantify general polynomial degree, component count and FS; for this 2-coordinate witness 3 independent base-field checks give >144 bits for a single component if assumptions hold. A full uniform native extension-field α_i∈F_(p_i^4) makes this degree-1 false equality pass with 1/p_i^4 (~192bits), unlike α∈Fp_i embedded as constant. For a general length-m power-batch nonzero polynomial, Schwartz–Zippel failure≤(m−1)/p_i^d if truly uniform in full extension. This is only an oracle/native field statement: separately proving the aggregate is linked to the actual shared hidden canonical integer commitment over unrelated group scalar field is STILL NOT IMPLEMENTED. A 128bit seed-to-extension map is not automatically statistically uniform on a ~192bit domain. Challenge sampling occurs only AFTER all commitments bind the witness; prechallenge witness choice can force passes.

**Exact executable arithmetic verification:** `/mnt/data/vfhe_v13_prime_subfield_batching_gate.py` SHA256 `7aa6a7e28c5f0f782db89b4e7540273cb9fbf0d77468d234018cdb3a15c0af65`; JSON `/mnt/data/vfhe_v13_prime_subfield_batching_gate_results.json` SHA256 `eb5a40bf1ebdd8f336a55e32175e372071ab3fc7fdddd45e5e3a6a03f76d79df`. Local-only; computes probabilities exactly, checks prime shape/primality, enumerates toy F17/F29/F37 batch root, demonstrates early-challenge failure. No ZK, actual shared commitment, native F.2 extraction, or cost verification.

**Subject finding source:** `findings/vfhe-cross-crt-consistency-research.md` **Section22** (V13), Section21 V12, Section20 V11, Section19 V10, Section18 V9. Maintain topic file rather than per-round findings files.

## NEXT_ACTION V14 — only on PI continuation

ONE explicit extension-field cross-characteristic batch-link feasibility gate: with common hidden canonical digit vector a committed in third-field/group commitment C, and honest native α_i∈F_(p_i^4) sampled postcommit, can we make the batched relation

    z_i = Σ_j α_i^j embed_(p_i^4)(a_j) = Σ_j α_i^j u_i,j

knowledge-sound and ZK WITHOUT silently treating an F_(p_i^4) scalar as an endomorphism of the unrelated commitment scalar group? Cheapest test: express α_i in 4-dimensional F_(p_i)-basis, count required independent native scalar/basis relations or cost; test for group-modulus alias if trying to claim one exponent equation proves equality across fields. If cannot justify cheap link, report UNCLEAR and suggest PI-controlled pivot to existing commit-and-prove/range proof primitives rather than inventing a free cross-field homomorphism. No full PCS coding/performance claim.

## Outstanding blockers

Cross-CRT common witness knowledge extraction from original Brakedown F.2 under arbitrary field challenge; canonical vector commitment hidden but linked; practical bit/range constraints; scalar/extension conversions; Fiat–Shamir and 128-bit soundness; witness privacy; complexity versus paper's native RS optimizations; source official version authentication. V9 bounded-digit code-distance is a conditional lemma only; **no integrated repaired protocol** and **no verified publication novelty**.

## Protocol

Follow AGENT.md and RESEARCH_PHILOSOPHY.md; ONE primary hypothesis + cheapest decisive test; read before write, verify commits by rereading, exact provenance and PASS/FAIL/UNCLEAR. Root STATE.md is only a pointer and freezes global I192. Human PI controls pivots, security disclosures and contribution assessment.
