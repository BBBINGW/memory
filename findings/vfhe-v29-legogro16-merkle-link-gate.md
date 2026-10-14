# vFHE V29 — LegoGro16 root-to-Merkle commitment interface gate

Date: 2026-10-15. Independent V29, global general FHE I192 frozen.

**ONE PRIMARY HYPOTHESIS [FAIL]:** A published LegoGro16 Pedersen commitment-link gadget can be added to the original vFHE F.2 native Merkle/RS commitment to knowledge-soundly bind hidden GP roots at negligible prover work, without also proving the native SHA/Merkle/RS authentication and evaluation relation. This is OUR hypothetical repair; neither paper claims it.

**STATUS: FAIL cheap drop-in Pedersen-only CP linkage; PASS exact source-shaped finite-field falsifier and a concrete SHA/Merkle circuit work census.** This does not refute the security of LegoGro16 or the original unmodified vFHE, nor prove an unavoidable cost bound for alternative zk-friendly commitments. A properly specified generic CP relation could in principle prove the link; no real LegoGro16 ZK proof or timing benchmark was executed.

## Source evidence [FACT]
* Campanelli, Fiore, Querol, LegoSNARK (CCS2019), IACR ePrint2019/142, source obtained via Research MCP 72 physical pages, SHA256 9c9a5ae7763ed3f476e1c5810d500af8826abbc8634cb578f558bffddbe68648, version unverified. §3.1 pp12–13 Definition3.1 CP relation; §4.1 pp20–21 CPlink specifically for Pedersen-verification-compatible commitments. §7.1 p40 compares commitment-link overhead only (n2048, LegoGro16 0.08s vs embedding Pedersen into Groth16 428s) and explicitly states the R-dependent relation cost is the SAME. The 5000x finding is not a hash-circuit speedup and cannot apply here without analysis.
* Cascudo et al., Verifiable Computation for Approximate Homomorphic Encryption Schemes, ePrint2025/286, inspected 52pp mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, official Feb2026 PDF version unverified. Fig1 physical p23 requires authentic four GP root evaluation identity. Appendix F.1 p50 CRT field PCs; F.2 pp50–51 commits by Merkle tree to RS-encoded MATRIX COLUMNS, each leaf a whole m-field-element column; native verifier checks public v'=q1Uf, Enc(v')|Q=q1Uhat|Q, and y=<v',q2>. F.3 pp51–52 describes piecewise RS. Its source commitment is NOT a Pedersen commitment.

## Decisive toy test [EXPERIMENT, not a SNARK implementation]

Legal source N4,d2,p13, native K5,K8 both isomorphic to F13². Use the V28 false final-count memory transcript at sigma4,tau2 with actual GP roots WSh8,RS10,WSt2,S2; original root relation 2*8=3 differs from 10*2=7 mod13. Choose a detached Pedersen-committed fake WSh root10 so 2*10=10*2 passes. The real WSh F.2 MLE second row [8,0] has source F.3 toy piecewise RS encoding [8,8,0,0], authenticated by correct SHA256 Merkle paths. To claim fake root10, the private native row vector must be [10,0], encoded [10,10,0,0]. All C(4,2)=6 sampled two-column query subsets and BOTH true quadratic extension factor arithmetic were exhausted: a proof only of detached Pedersen roots/products accepts all 6; a correct CP circuit checking source Merkle-verified sampled RS relation additionally accepts ONLY Q={2,3}, 1/6, because it misses the changed first block. This preserves original small-code sampled error, not a new original-vFHE vulnerability; the missing Merkle/RS relation is essential.

## Correct conditional CP statement [DERIVED]

For EACH native factor i and GP oracle alpha, a knowledge-sound (and, if required, hiding) proof must use public original Merkle root cm_(i,alpha), sampled Q and original challenges, and private committed P, Pedersen opening rho, native v', encoded sampled columns, and Merkle paths. It must prove:
1. C_P = PedersenCommit(P,rho);
2. EVERY Merkle path verifies to the original source cm;
3. Enc(v') restricted to Q equals q1 times the authenticated Uhat columns, and P equals <v',q2> in ACTUAL native F_(p^d), with proper cross-characteristic arithmetic;
4. Four hidden roots satisfy source GP product identity over EVERY factor;
5. The root/claim (or appropriate native v' binding) is fixed before Q and any source Fiat–Shamir challenge ordering is respected.
Original F.2 testing stage also sends v=rUf publicly; further privacy redesign is required for full ZK. Merely employing LegoGro16 CPlink between two Pedersen-like commitment slots does NOT establish an equality with a separately hashed Merkle/RS witness.

## Cost gate [EXACT deterministic model, NOT an end-to-end benchmark or lower bound]

Illustrative source-form N=2^14,d4, two CRT primes gives mu=8192 native factors. A GP oracle with ellstar24 has 25 variables, padded to 26 for native F.2 square matrix m8192. Illustratively choose source F.3 encoding two [8192,4096] RS blocks, M16384; t32 sampled encoded columns; four independent GP root PC Merkle trees per factor. Seed 20261015 yields 32 selected leaves, 282 DISTINCT internal Merkle hash nodes after combining overlapping authentication paths, hence 314 hash nodes/root. Across mu8192 and four roots = **10,289,152 total hash nodes** (9,240,576 internal). Naive disjoint-path bound would count 14,680,064 internal; our exact sampled architecture shares paths.

Critically F.2 hashes WHOLE coded column vectors. Packing one F_(p^4) ~49bit-prime element as an illustrative 25 bytes, each m8192 vector has 204,800 raw bytes; a one-byte tagged SHA256 Merkle instantiation uses 3201 64-byte compression blocks per LEAF and 2 per internal tagged node. Across 8192 factors, 4 roots, 32 leaf openings = 200 GiB TOTAL RAW COLUMN INPUTS (already potentially transmitted by original F.2, NOT new network bytes); verifying these hashes INSIDE an uncomplicated LegoGro16/R1CS circuit entails **3,374,972,928 SHA256 compression blocks** in this chosen architecture, before field arithmetic/zk proof overhead. This is NOT a runtime estimate or universal minimum: change SHA to a SNARK-friendly hash, use alternative PCS, aggregate roots, alter t/m, etc., and counts differ. LegoSNARK's 5000x Pedersen-overhead benchmark cannot be used to extrapolate the new relation workload.

## Decision and next test

**FAIL:** inexpensive append-only LegoGro16 Pedersen root proof is insufficient; actual Merkle/RS opening integrity must be proven in a CP-compatible relation, possibly at huge additional in-circuit cost for a direct SHA256 instantiation. **UNCLEAR:** proof-system performance after specialized optimization and 128bit secure integration. The optional hidden GP-root ZK branch has now had multiple high-risk interface failures and does NOT solve the separate primary CRT canonical bounded INTEGER digit soundness gap. **RECOMMEND PARK/HUMAN_REVIEW** of hidden-root ZK reconstruction and refocus on the original source-version-gated soundness repair.

NEXT V30 ONLY if PI continues: one source-specific NONCIRCULAR common-integer-digit knowledge-binding proof or official Feb2026 revised PDF authentication. No author contact without human approval. Global I192 frozen.

Local self-contained reproducibility:
- /mnt/data/VFHE_V29_LegoGro16_Merkle_CP_Cost_Gate_2026_10_15.md SHA256 0a98178bbe907253d627fe51bec360b8feb2ee11297a8edb12ef0b8e02034bd7
- /mnt/data/vfhe_v29_legogro16_merkle_cost_gate.py SHA256 1293343318d729305d1ac4a7eb7a45d8daa6845e6ebfcd6b98c51b7aac1e4cd8
- /mnt/data/vfhe_v29_legogro16_merkle_cost_results.json SHA256 cdc74254c117803bc3c3221b73fda36ea1c607fc2b82ca6fd9ee26deba146226

END OF ITERATION: STATUS FAIL cheap CP shortcut, RESULT proof obligation + exact Merkle census, NEXT_ACTION original soundness/official source, STATE_UPDATE YES independent V29.
