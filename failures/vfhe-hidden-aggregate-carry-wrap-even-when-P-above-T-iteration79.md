# Iteration 79 — Hidden aggregate bridge: modular carry equation unsound even when external field P>T

Date: 2026-10-12
Parent paper: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286, original §4.3 Eq(21)–(23) and §5 per-field polynomial commitments.
**STATUS: FAIL** for precise naive external SNARK-field carry relation; **PASS** for mathematically sound range-strengthened version; **UNCLEAR** for existence/cost of non-native zero-knowledge cross-domain PC links.
**NO CONTACT**: User explicitly instructed no email to authors; did not contact anyone or create any Gmail draft, public issue, or disclosure. **STATE_UPDATE: NO** (unrelated RIG-HE STATE.md untouched).

## Read-before-write and provenance
Read connected AGENT.md, RESEARCH_PHILOSOPHY.md, read-only STATE.md, I78 `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`, I77 `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md` and I64–65 previous repair failures. Read primary 52-physical-page Research MCP version of ePrint 2025/286 pp24–27: §5 explicitly constructs Rq polynomial commitments component-by-component from commitments for fields F_(p_i^d), via Brakedown. The paper does NOT propose our external aggregate bridge. PDF mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official newest bytes VERSION_UNVERIFIED.
Prior-art check (public): Ganesh, Nair, Sharma, *Dual Polynomial Commitment Schemes and Applications to Commit-and-Prove SNARKs*, CCS 2024, https://doi.org/10.1145/3658644.3690219 or https://cris.technion.ac.il/en/publications/dual-polynomial-commitment-schemes-and-applications-to-commit-and/; their paper links univariate and multilinear commitments and demonstrates linear-witness relationships within their constructions, NOT a verified cross-characteristic vFHE integer bridge. Lycklama et al., *Artemis*, https://arxiv.org/abs/2409.12055, generic CP-SNARK techniques, also not proof of an off-the-shelf cross-CRT compatibility. These indicate generic linking alone is prior art; no novelty claim for our arithmetic gadget.

## ONE primary hypothesis, smallest falsifier
[HYPOTHESIS — FAIL] Let hidden common external committed Boolean/digit vector b∈{0,...,β−1}^m, public random Boolean coefficients α∈{0,1}^m, its exact integer aggregate A=Σα_ib_i ∈[0,T], T=m(β−1). An external SNARK proof field F_P with P>T, coupled with separate range constraints 0≤u_k<p_k and 0≤c_k≤floor(T/p_k), suffices to make the field equation `A=u_k+p_k*c_k (mod P)` certify the **integer** residue u_k=A mod p_k.
[FALSIFIER] Exhibit P prime>T and individually range-compliant A,u,c where equality holds mod P but is false over integers, together with legal field digit vectors whose sums yield claimed u.
[CHEAP TEST] Reuse single I72 family prime list (149,157,173), with m=128, beta16, T1920 and one explicitly fixed all-one alpha; test P1931 and safe prime P2081, prove parameter bound and count bitness overhead. This is a test of **one arithmetic sub-relation**; not a random-challenge security advantage, nor a zero-knowledge implementation.

## Formal proposed protocol API (conditional, NOT yet implemented)
**Public prechallenge:** A binding/hiding external vector commitment C_b to canonical small integer digits b; separately binding field PCS commitments D_k to h_k∈F_k^m. Both committed *before* sampling α.
**Public coin:** α uniform in {0,1}^m after all these commitments.
**Private subsequent witnesses:** integer A in [0,T], canonical residues u_k∈[0,p_k), quotient c_k, commitments C_A,C_{u_k}, and local opening/aggregate claims.
**External ZK relation Π_ext:** Prove knowledge of the SAME b opening in C_b; digit range; commit C_A to exact A, C_{u_k} to u_k; prove A=Σαb as integer and A=u_k+p_kc_k *as an integer*, with no-wrap safeguards and ranges. (C_A may be committed after α because it is linked to the prechallenge C_b).
**Native field relation Π_field,k:** Prove from original D_k via a field-native PC opening/linear-sumcheck that S_k=Σα_i h_{k,i} equals u_k·1_Fk.
**MISSING HARD PRIMITIVE Π_link,k:** Must zero-knowledge LINK the *same hidden u_k* across the F_(p_k^d) field-native aggregate proof and external C_{u_k}. A field PC opening/commitment being cryptographically binding *separately* does NOT imply this equality. Publishing u_k could trivially bind it but leaks information about A and b. Merely comparing CRT residues or two unrelated commitments recreates I77–78 flaws. Generic non-native proof of the field PC's opening could implement such a link at potentially high cost; none supplied.
Security conditional on all binding/extraction, ZK composability, and field linkage; the naive arithmetic relation below FAILS even supposing the links were ideal/perfect.

## Exact P>T wrap counterexample
Take m128, β16, T=m(β−1)=1920. Original-style RNS primes (149,157,173). Choose EXTERNAL proof prime P=1931 (>T). Public mask α=all ones, ONE explicitly fixed witness (not an assertion of non-negligible cheating probability):
 - Shared committed small-digit integer vector b=[15]*9+[9]+[0]*118 (all in 0..15), true exact aggregate A=9*15+9=144.
 - Honest field vectors h149=h157=b so their field sums are u149=u157=144 with c149=c157=0.
 - Malicious but individually valid field vector h173=[15]*11+[7]+[0]*116, all values in 0..15, sum=172, so its FIELD-native aggregate claim u173=172 is truthful.
 - External quotient witness c173=11 satisfies 0≤c173≤floor(1920/173)=11. Canonical u173=172 satisfies 0≤u173<173.
 - Recombined right side 172+173*11=2075=144+1931=A+P, so A=u173+173*c173 in F_1931; all separate native & external proof equations can pass despite **144 mod173=144 ≠172**. Therefore P>T and independent quotient/residue bounds DO NOT suffice for correct hidden modular reduction.
This is an ACCEPTING FALSE *bridge relation assignment for fixed alpha*, not yet a security break of repeated randomly chosen alpha. Do NOT claim an adversary succeeds with non-negligible probability under actual batch randomized challenge: h vectors must precommit before alpha, and only one explicit alpha has been tested.
The true-b witness here and both field vectors are explicit; the attack does not rely on uncommitted field aggregate value.

## Minimal rigorous fixes
For each prime p_k and T bound, define `RHSmax_k = floor(T/p_k)*p_k + (p_k−1)` under the simple independent range constraints. To ensure A and RHS injectively embedded into F_P, it SUFFICES to choose
 `P > max(T, RHSmax_1,...,RHSmax_mu)`.
For p149,157,173 and T1920, RHSmax=(1936,2040,2075). So the prime P=2081 exceeds all maxima. I79 exact attack is rejected: 144 !=2075 mod2081. Honest residues u_k=A modp_k and quotients c_k=floor(A/p_k) pass with zero difference.
Alternatively retain P=1931>T but add an explicit integer upper-bound constraint `0 ≤ u_k+p_k c_k ≤ T`. Then **both** sides of the equation are in [0,T]⊂[0,P), so equality modulo P forces exact integer equality. The attempted 2075 RHS fails upper-bound. An even simpler canonical witness formulation can derive c as floor division and prove a no-wrap carry without separate RHS bound if P satisfies the stronger RHSmax condition.
One **important refinement** to I78's stated P>T criterion: it is sufficient only if integer RHS is ALSO enforced ≤T. Standalone P>T plus separately bounded u,c is NOT sufficient.
Formal numerical check executed with exact code and positive controls, no probabilistic cryptography involved.

## Resource cost / actual bottleneck
This concrete instance requires external vector digit-range bits 128*log2(16)=512; A as integer needs ceil(log2(1921))=11 bits. Each canonical residue u_k needs 8 bits; each quotient c_k needs 4 bits, i.e. 12 bits per field and 36 over three primes. THESE ARE witness bits, NOT measured R1CS constraints or proof sizes. Additional no-wrap comparison or choosing large P is cheap relative to 128*4 digit checks.
For large real SNARK proof fields (~2^255), and paper's 49-bit RNS primes with realistic mβ, choosing P above the RHSmax will normally be trivial, so carry soundness is a parameter/gadget correctness requirement, not the hard unsolved research bottleneck.
The hard issue remains Π_link,k: privacy-preserving equality between field-native polynomial-commitment aggregate and the same *externally* bound canonical residue u_k across **different characteristics**, avoiding a direct O(m·mu) native-PCS verification / massive nonnative arithmetic. There is no proof of an efficient instantiation in this iteration. An optimistic cost `O(m log β + μ log T)` counts only arithmetic witness constraints and must NOT be advertised as the full construction cost.
Knowledge soundness of naive protocol fails at subrelation level for this explicit fixed challenge. Repaired integer gadget by itself does not give cross-field soundness without Π_link,k.

## Artifact hashes and execution
- `/mnt/data/iteration79_vfhe_hidden_aggregate_carry_wrap.py`; SHA256 `e1045da88b767110af3b371f992007e539f261264e162707c8fd5ccc1b05fc62`, 4802 bytes.
- `/mnt/data/iteration79_vfhe_hidden_aggregate_carry_wrap_results.json`; SHA256 `980e9399afcb01979d6b3d20470e85ef8d8e13856b75cfab4a01495fa05ed14a`, 2170 bytes.
Executed stdlib Python, all assertions passed. P1931 and P2081 checked prime by integer trial division; malicious and honest positive controls verified.

## End
STATUS: FAIL — proposed P>T + separate residue/quotient range conditions as sound integer CRT bridge; PASS — bound refinement and concrete no-wrap proof; UNCLEAR — efficient ZK Π_link,k to original field PCS.
RESULT: Explicit m128 beta16 instance A144, false residue u173=172, quotient11 passes all naive F1931 external equations and honest field-side sums even though u!=A mod173. P2081 or RHS≤T fixes gadget. No claim of actual randomized soundness break or full ZK repair.
NEXT_ACTION: One focused interface/cost audit: inspect original paper §5's Brakedown field-PC evaluation opening and one existing dual-PCS/CP-SNARK construction to determine whether there is a **specific witness-binding interface** that can prove hidden canonical u_k equals native `Σα_i h_{k,i}` without importing an entire field-PC verifier into the external SNARK. If not, derive concrete lower/upper cost bounds and recommend HUMAN_REVIEW instead of another toy arithmetic variant.
STATE_UPDATE: NO — RIG-HE STATE.md untouched.
