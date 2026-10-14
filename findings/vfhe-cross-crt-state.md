# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo).
**LAST COMPLETED vFHE ROUND: V16. V17 NOT STARTED.**
**STATUS:** V16 PASS precise prime-field random-vector folding of native extension-factor link residuals into one challenge-dependent cross-characteristic modular quotient relation per CRT prime and independent fold round. Exact conditional error 1/p per round and real symbolic saving of GROUP MSM terms versus V15's separately opened standard Pedersen/IPA links. **UNCLEAR:** source-level single-canonical-vector mapping across all k factors; native F.2 PCS extraction, field-to-hidden-commitment linking knowledge soundness, ZK, FS security composition, overall computation/benchmark and true novelty. **General FHE counter FROZEN I192**; this project has separate V-series (legacy vFHE I193–I196 correspond only to V1–V4).

## Independent V-round index

V1: integer code toy. V2/V3: weak binary-prefix distance families rejected. V4: Fp-to-extension code-distance equality. V5–V8: CRT low-support minor rank analysis and actual source-prime-divisible five-minor (not whole-code attack). V9: global BOUNDED digit-difference distance via no-wrap + binary RAA. V10: sampled encoded Merkle leaf range alone not deterministic binding. V11: systematic-only range sampling loses distance. V12: unrelated-prime shared commitment must explicitly link native digits and canonical bounds. V13: base-subfield 128-bit integer challenge only ~48-bit single-check soundness. V14: genuine extension-field links need four basis modular quotient relations and actual commitment functional openings. V15: separate direct Pedersen or IPA functional openings have O(Fm) MSM input terms despite O(log m) IPA communication. **V16: all 4k constraints PER NATIVE PRIME p can be randomly folded into ONE ordinary length-m coefficient functional per independent Fp challenge, conditional on a shared canonical a and ideal native/code and commitment extractors.**

## Scientific source

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, IACR ePrint2025/286 https://eprint.iacr.org/2025/286. Inspected 52pp research-MCP PDF mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official revision VERSION_UNVERIFIED. §3.1 physical p10 has k=N/d native F_(p_i^d) factors for each CRT prime; Appendix F.1/F.2 pp50–51 has per-prime PCS and field-linear Brakedown. Our third-field commitment, integer RAA and cross-factor folding are NOT in original work. Original rectangular vs diagonal lookup issue is a source-form ideal-oracle audit, NOT an authenticated current compiled SNARK exploit.

## V16 ONE hypothesis / cheapest decisive test

**[HYPOTHESIS PASS in IDEAL extracted fixed-witness setting]** Suppose for one p all k extension factors' L=4k base-coordinate linear linking claims involve the SAME canonical vector a∈[0,beta−1]^m, already hidden/bound to a third-field vector commitment C, and each native z_l is separately knowledge-soundly bound to its native field witness BEFORE fold randomness. Can choose lambda∈Fp^L postcommit to reduce L claims `<c_l,a>=z_l (mod p)` to one `<cbar,a>=zbar (mod p)` with known false acceptance even if L large?

**[DERIVATION PASS]** cbar_j=Σ_l lambda_l c_lj mod p, zbar=Σ_l lambda_l z_l mod p. For any fixed nonzero residual e∈Fp^L, Pr_lambda[<lambda,e>=0]=1/p EXACT via solving for one uniform lambda coordinate. s INDEPENDENT fold vectors give p^-s. The canonical-integer/third-field proof still needs `Sbar=Σ_j ctildebar_j*a_j = ztildebar+p*kbar` with 0≤Sbar≤m(p−1)(beta−1), 0≤kbar≤floor(Smax/p), and a sound functional opening to original C. Reducing cbar first in Fp keeps quotient bound independent of L. The native side must prove zbar comes from ALL already-bound native z_l, not an arbitrary adversarial postchallenge value. If a or native vector is editable after lambda, the probability proof fails.

**[SOURCE-LIKE CONDITIONAL COST]** m1024, N8192,d4,k2048 => L8192 per prime, CRT primes mu4, repeat s3. Separate V15 direct linear openings have 8,388,608 MSM terms per prime, 33,554,432 total. Folded s openings have 3072 MSM terms per prime, 12,288 total, 2730.67x fewer MSM scalar-base input terms ONLY in directly compared implementations (not elapsed time). Separate IPA illustrated L/R group fold messages 163,840 per prime vs folded 60 per prime. But unoptimized coefficient folding still processes sLm=25,165,824 BASE-FIELD multiply/add terms per prime, 100,663,296 total, plus native original-value checks, FS challenge expansion and ZK/quotient constraints. Original source has NOT been shown to need one proof per k factor or to admit single compact a across all factors, so these are illustrative conditional numbers, not source benchmark or universal lower bounds.

With p_min>2^48, mu4, s3, conditional union error ≤4 p_min^-3<2^-142, FOLDING part only. This does not certify full protocol 128-bit soundness; native extraction, binding, third-field CP proofs, FS, ZK, and other failures not accounted. Random challenge is full random VECTOR in Fp^L, not one power-batched small-seed field scalar. A short hash/PRG seed must be specified with computational assumptions to imitate this challenge distribution.

**[EXACT EXPERIMENT]** Toy F29^4=F29[theta]/(theta^4+theta+5), k3 native extension factors with independent challenges, L12 coefficient statements, m5, beta16, a=(2,3,5,7,11), and r10007 third arithmetic modulus. 75 random fold vectors all satisfy honest Sbar=zbar+29*kbar exactly, no commitment-order wrap; one intentionally falsified native z_l gives residual e with support1 and exact acceptances 1/29, 1/841, 1/24389 under 1,2,3 independent uniform folds. Dense-error uniqueness check also passes. This is exact algebraic testing, not a Pedersen/IPA, SNARK or cost benchmark.

Local script `/mnt/data/vfhe_v16_cross_factor_folding_gate.py` SHA256 `8f196a439ff50037ad69b0c5d4a8d53ceb967d129649b2f4b4a84f587be78d1e`; JSON `/mnt/data/vfhe_v16_cross_factor_folding_gate_results.json` SHA256 `1011e1368c0d8e7bbb1330dd74fae21f41c04217f57da707cba2d7658e988e8b`. LOCAL ONLY, not Git bytes.

**Full detailed subject finding:** `findings/vfhe-cross-crt-consistency-research.md` Section **25** V16. Original paper source terms accurately separated from this hypothetical design.

## NEXT_ACTION — V17 only at PI continuation

ONE decisive interface audit on ORIGINAL §3.1 + Appendix F.1/F.2 and vFHE digit tables: do all k extension factors for one p encode independent *images of the SAME canonical integer vector a of length m*, or do they genuinely have factor-specific a^(t) requiring vector size k*m? If the latter, V16's one-length-m functional reduction is not valid for that original object; formally revise model. Then test needed original-code extractor and knowledge-sound connecting proof; no false claim of published flaw or usable 128-bit protocol before this gate. A nontrivial avenue is to instantiate known batched commit-and-prove proof with actual native data representation.

## Workflow / authority

Global root `STATE.md` freezes I192 and references the independent V-series. Human PI controls research pivots/novelty/disclosures. AGENT.md: read before write, one primary hypothesis and one cheapest decisive test, archive only material result and verify after write.
