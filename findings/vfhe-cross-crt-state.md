# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo).
**LAST COMPLETED vFHE ROUND: V14. V15 NOT STARTED.**
**V14 STATUS:** FAIL the shortcut claiming a single full-extension-field random batched link can be directly checked against an unrelated-prime Pedersen/vector commitment without canonical integer quotient links; PASS explicit 4-basis-coordinate modular quotient relation and exact arithmetic toy. Whole vFHE PCS proof, witness extraction, zero knowledge and efficiency UNKNOWN. NOVELTY NOT VERIFIED.
**GLOBAL FHE GENERAL COUNTER:** FROZEN at I192. Independent vFHE V1–V4 were historically mislabeled I193–I196; preserve those legacy evidence labels, do not advance global I-series.

## Independent round map

V1 bounded integer code toy; V2 one-prefix degree-two no-good-distance; V3 cyclic first + second interleaver no-go; V4 base-to-extension code distance invariant; V5–V7 small-support CRT-prime determinant thresholds; V8 actual source-form 49bit prime divides a 5x5 parity minor (NOT whole code-distance collapse); V9 bounded digit-pair global distance reduction to binary RAA under no-wrap; V10 naive sampled encoded-Merkle range binding FAIL; V11 systematic-only random sample detection 1−t/m FAIL; V12 common commitment without explicit cross-characteristic link/range FAIL; V13 shared 128-bit integer challenge reduced mod native p gives only ~48-bit one-shot test; **V14 full-extension challenge removes that sampling issue but NOT cross-characteristic commitment aggregation / modulo-p quotient proof.**

## Parent scientific target

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, IACR ePrint2025/286, https://eprint.iacr.org/2025/286. 52pp research-MCP mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; official PDF revision VERSION_UNVERIFIED. Original §3.1 p10 native CRT fields F_(p_i^d), Appendix F.2 pp50–51 native field-linear Brakedown Merkle PCS. Original cross-CRT scalar lookup gap only source-form ideal-oracle audit, not authenticated compiled attack. Proposed common-integer Pedersen bridge is NOT in source.

## V14: ONE hypothesis / cheapest decisive test

**[HYPOTHESIS FALSIFIED]** With α uniform in F_(p^4), homomorphic aggregation of a third-prime commitment containing a canonical integer vector a can be directly equated to z=Σ α^j a_j in the native field, without any explicit cross-characteristic arithmetic/functional opening proof.

**[DERIVED EXACT RELATION]** Expand α^j=Σ_(t=0)^3 c_(j,t) θ^t in chosen Fp basis; choose 0≤ctilde_(j,t)<p. Integer aggregate S_t=Σ_j ctilde_(j,t) a_j. Native z_t=S_t mod p. Need FOUR component equations S_t=z_t+p*k_t with z_t∈[0,p−1], 0≤k_t≤floor(m(p−1)(β−1)/p); these may be proven jointly in one succinct proof. Group aggregation binds S_t mod commitment order r, NOT z_t mod p. A compact vector Pedersen commitment may additionally require nontrivial weighted linear-functional opening/IPA; no free homomorphism between different characteristics.

**[EXACT TEST PASS]** Toy irreducible F29^4=F29[θ]/(θ^4+θ+5), α=28+θ genuinely not base-subfield, β16,m5, honest digit vector a=(2,3,5,7,11), unrelated scalar prime r10007. Integer S=(562,423,253,282), reduced native z=(11,17,21,21), quotients k=(19,14,8,9). All S_t<r, proving failure is native-p reduction, NOT r-wrap. Even honest input fails naive direct S=z checks. Fully exact polynomial arithmetic scripted.

**[SOURCE-SIZE CONDITIONAL]** p=281474976829441 (~49 bits), m1024,β2^20 implies S_t≤302231166800824369152000 (78 bits), k_t≤1073740799 (<2^30). A typical ~255bit group order suffices for non-wrap of this canonical lifted S, but the modulo-p quotient link remains required. Neither beta/m nor commitment scalar group has been mapped to a specific complete original-paper construction.

**[REPRODUCIBLE LOCAL FILES]** `/mnt/data/vfhe_v14_extension_field_link_gate.py` SHA256 `cf972c3fa8b95ad43075ed7859dea48bdd5b18b033805643a17702f81527da44`; `/mnt/data/vfhe_v14_extension_field_link_results.json` SHA256 `1948173a26ffdffb415500541686450a1cfe688eecb27eaafa2e934b3e96b452`. Not checked into repository. These are algebraic tests, NOT a CP-SNARK, ZK proof or performance measurement.

**PRIOR ART** cross-system modEq/range CP-ZK is known; Benarroch et al., *Zero-knowledge proofs for set membership: efficient, succinct, modular*, DCC2023 DOI 10.1007/s10623-023-01245-1. No novelty claim.

**Full technical record:** `findings/vfhe-cross-crt-consistency-research.md`, Section **23** V14; §§22 V13,21 V12,20 V11.

## NEXT_ACTION: V15 only with PI continuation

One precise feasible operation-count comparison: proving the corrected FOUR-coordinate extension aggregate using (A) individually homomorphic digit commitments or (B) one compact vector commitment with a linear-functional/IPA proof, including quotient constraints, native F_(p^4) arithmetic and Fiat–Shamir binding. Determine whether the amortized proposal actually saves work over per-coordinate proofs, WITHOUT assuming free linear-functional openings. If no decisive operation saving can be established, report UNCLEAR/HUMAN_REVIEW. Original F.2 native-field extraction, global diagonal consistency, ZK/hiding, 128-bit soundness, and paper-version authentication still OPEN.

## Workflow

Root STATE.md is only a pointer, global I192 frozen. Human PI decides pivots and contributions. Agent follows AGENT.md one hypothesis + one cheap decisive test, read before write and verify by reread.
