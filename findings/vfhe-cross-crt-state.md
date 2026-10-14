# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo).
**LAST COMPLETED vFHE ROUND: V18. V19 NOT STARTED.**
**STATUS:** V17 FAIL the source-interface assumption that native CRT field commitments automatically extract SAME bounded integer digit vector; PASS exact SOURCE-FORM p13/N4/d2 nontrivial idempotent refuting a concrete implication in inspected source Appendix E.2 Theorem 4.8 proof. Original compiled SNARK exploit, final paper version and complete ideal PIOP transcript NOT VERIFIED. V16 abstract random folding remains mathematically correct in its IDEAL common-a model; no actual original-source cost or 128-bit PCS repair established.
**GLOBAL GENERAL FHE ITERATION COUNTER:** FROZEN I192. vFHE has own V-series. Legacy V1–V4 once labeled I193–I196; preserve historical filenames/iterations without advancing global sequence.

## Independent progress

V1–V3 integer RAA toy and weak-distance negative families; V4 prime-to-extension code-distance equality; V5–V8 low-support CRT rank audit and a legal prime-divisible minor; V9 bounded digit pair global distance under integer no-wrap and binary RAA; V10/V11 Merkle sampled-range and systematic-only failures; V12 third-field commitment without explicit cross-field ZK link fails; V13 integer challenge mod49bit prime subfield cannot claim 128-bit single-test soundness; V14 correct extension-field link needs four base-coordinate integer quotient constraints; V15 direct Pedersen/standard separate IPA work O(Fm) despite short proof bytes; V16 random fold all d*(N/d) link residuals per native prime into one length-m functional per round ONLY IF a common compact scalar integer vector is already soundly bound/extracted; **V17 original CRT polynomial/data interface does NOT itself give that critical shared-a assumption, and original Appendix E.2 proof makes a false diagonal-membership inference.**

## Primary original-paper source / anchored proof discrepancy

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint2025/286, https://eprint.iacr.org/2025/286. Research MCP cache: 52 physical pages, github-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, version_status VERSION_UNVERIFIED. Source §3.1 p10 decomposes EACH p_i into k=N/d field factors R_(i,j)=Fp_i[X]/(X^d−ζ^(2j+1)). Source §4.3 pp20–23: TB is coefficient-range ring table and t_beta={0,...,β−1} is SCALAR digit table inside ring R_q; Theorem4.8 on p23 asserts sound ring-range PIOP under β<pmin,2^ellstar<pmin; Remark4.9 p24 discusses previous revisions. Original §5 p25 and Appendix F.1/F.2 pp50–51: independent field-projection polynomial commitments and Brakedown field matrices, do not enforce one diagonal native scalar digit merely by binding each factor. F.2 PCS row dimension m_PCS=2^(ell/2) from MLE matrix, distinct from our hypothetical m_digit.

**Original Appendix E.2 physical p48 proof explicitly asserts**: if a ring lookup htilde is NOT in scalar table t_beta, there EXISTS a CRT component k whose projected htilde is NOT in t_beta. This implication is FALSE for product rings with at least two factors, even under Theorem4.8 stated conditions.

## V17 ONE hypothesis / decisive exact counterexample

**[HYPOTHESIS FALSIFIED]** The original split-field CRT PCS and t_beta membership predicate force every native field to extract one COMMON scalar bounded integer witness without additional diagonal proof; hence V16's same compact length-m vector is directly the source polynomial encoding object.

**[EXACT SOURCE-FORM COUNTEREXAMPLE]** Choose N4,d2,k2, native p13=1+(2N/d)*3 with ODD 3. Polynomial X⁴+1=(X²−5)(X²+5) over F13; ±5 are nonsquares so factors both irreducible, giving R=F13[X]/(X⁴+1)≅F_(13²)×F_(13²). Let β2, t2={0,1}⊂R and e(X)=7+4X². Then Φ_(X²−5)(e)=1, Φ_(X²+5)(e)=0, while e itself is NOT ring-scalar 0 or 1. Moreover e²=e (CRT idempotent). Thus e∉t2 although BOTH native factors individually lie in t2; this directly refutes Appendix E.2 p48 “some component must fail” inference. For ellstar1, 2^ellstar=2<p13 and β2<p13 meet theorem side conditions. The source PIOP's full proof transcript and full compiled SNARK have NOT been tested here.

**DISTINCT INTERFACES:** Honest scalar digit a∈t_beta has diagonal projection (a,a,…), but that is the desired relation, NOT a property automatically enforced by independent field commitments. General ring element f(X)=Σ_(j<N) f_jX^j instead maps to DIFFERENT polynomial-remainder values per factor. Example f=2+3X+4X²+5X³ projects to (9,2) and (8,4) in the two F13² coordinate bases. A canonical ring-coefficient vector uses N coefficients per ring value and factor-dependent PUBLIC LINEAR MAPS; it is not simply one copy of the same scalar digit per factor. Digit-vector length m_digit, ring coefficient length N, and source F.2 m_PCS=2^(ell/2) are different quantities absent further mapping.

**[EXPERIMENT PASS]** Local stdlib `/mnt/data/vfhe_v17_crt_factor_interface_audit.py` SHA256 `ef95aa14980245ea65e693a0be690970e7e6e4ed692a15ee98a453219d95aabd`; JSON `/mnt/data/vfhe_v17_crt_factor_interface_audit_results.json` SHA256 `2e7ddf329a0f4546c046b328591236c1c82e8d83d396d323e41d9206a5f2d33a`. Two deterministic executions matched. Explicit factor irreducibility, idempotence, source-form prime congruence, invalid scalar-table membership, valid EACH-field table membership, and factor-dependent projections. No formal cryptographic attack or compiled proof generated; latest official version parity unverified.

**Full findings with source excerpts:** `findings/vfhe-cross-crt-consistency-research.md` §26 (V17); prior §25 (V16).

## NEXT_ACTION — V18 only on PI continuation

ONE source-faithful **ideal PIOP** counterexample/completeness gate: instantiate Theorem4.8 Π_beta_range Figure1 (§4.3 pp22–23, Appendix E.2 pp47–49) with the ring-valued constant oracle htilde=e=(1,0) and legitimate β2,ellstar1, source-form p13,N4,d2. Construct per-field honest memory-counter/grand-product oracles (one factor sees digit1, the other sees digit0), CRT-glue prover oracle polynomials, and check all relevant ring verifier identities and challenge ordering. This tests whether erroneous proof implication is exploitable in the IDEAL PIOP, not whether compiled real-world SNARK is exploitable. If an additional mechanism forces diagonal equality, identify it. If ideal PIOP accepts an invalid witness, archive proof-level failure carefully and research one minimal source-specific fix. Do not claim real-world exploitation, author confirmation or novelty without stronger evidence.

## Authority and workflow

Global root `STATE.md` holds I192 frozen and points here. This file is the sole independent V-round counter, topic file holds full evidence. Follow AGENT.md and RESEARCH_PHILOSOPHY.md one falsifiable hypothesis + cheapest decisive test, read-before-write, reread after commit, [FACT]/[DERIVATION]/[EXPERIMENT] separation. Human PI controls research direction, disclosure, and contribution assessment.


## V18 — source Figure1 IDEAL PIOP transcript, PASS (2026-10-14)

Confirmed CRT-idempotent false range lookup htilde=e=7+4X² over R=F13[X]/(X⁴+1), N4,d2,p13, beta2,ellstar1. This non-scalar ring element maps to native field digit pair (1,0) while each native component individually passes scalar digit table membership. One prechallenge read counter with leaves (0,1), one prechallenge final counter with ring leaves [2(1−e),2e], then four post-(sigma,tau) grand product oracle trees (interpolated to MLE), satisfy *every* printed Figure1 GP recursion, both virtual zero-sum obligations and final grand product root equality identically for ring challenges; no diagonal consistency enforced. Exact experiment tested 676 parameter configurations. This is a constructed **source-specified ideal PIOP soundness counterexample**, not a proven compiled cryptographic SNARK exploit, not official latest PDF authentication; avoid confusing levels.

Technical section `findings/vfhe-cross-crt-consistency-research.md` §27. Local script `/mnt/data/vfhe_v18_ideal_piop_crt_attack.py` SHA256 e80af660f6b79d7da47fd11cc6eb7a4efa4ff3271f622659ec456c0affe534e3, JSON `/mnt/data/vfhe_v18_ideal_piop_crt_attack_results.json` SHA256 d68f436ad2308b6d9b81edf2b23e43df49ab1864ef0438efc7e43edc8765704b. Script proves ground equations, not full separate interactive sumcheck transcript; both sum claims true, hence honest ideal sumcheck prover exists.

**NEXT_ACTION V19 only if PI continues:** audit §2.2 and F.1/F.2 compiler: can ring oracle family via CRT be independently committed fieldwise in source PCS with NO implicit diagonal extraction, or is there a hidden global consistency check? Also check current author PDF edition before security claim. No author outreach until human PI.
