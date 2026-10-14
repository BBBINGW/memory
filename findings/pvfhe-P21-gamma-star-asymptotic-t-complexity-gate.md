# PVFHE-P21 — Exponential t_Gamma lower bound for CMNW coordinate-wise stars

**Date:** 2026-10-15 Asia/Tokyo. **P21 COMPLETE; P22 NOT STARTED.**
**STATUS:** PASS general combinatorial lower bound and independently executed deterministic code certificate; FAIL direct 2026 Theorem5 polynomial-time FS extraction via CMNW's EXACT star Γ in standard parameter family; UNCLEAR alternative Γ', CMNW-specific FS extractor, nested classical ROM/QROM/SIS. **HUMAN_REVIEW/PARK** full P11/P12 PCS-security integration unless PI elects one alternative Γ' test. Not an attack on original paper.

## Read before write / provenance
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f5025258cf525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, independent global STATE.md SHA 7147ef8ce01abdc632551a7d50cf13f87569fe64 (concurrent V38), P20 findings/pvfhe-P20-cmnw-adaptive-fs-knowledge-contract-gate.md SHA 0b481967fb10462200149b9b8db0835c2737400e and P19 SHA 4fe559ff472081f3231518df50a485684c23a7ba. P21 was absent before this NEW file. Do not update global STATE.md, prior P-series or parallel SHIP/vFHE.

## Original source contracts
- CMNW Cini–Malavolta–Nguyen–Wee, Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup, CRYPTO 2024/ePrint 2024/281; full Research MCP 52 physical page mirrored PDF SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73, VERSION_UNVERIFIED. Physical p13 §3.4 defines coordinatewise star Γ(S,ξ) as center c with ONE neighbor differing in exactly each coordinate j. p14 Definition9 and Theorem2 bound ITS OWN interactive recursive extractor via (ξ+1)^ell=poly(λ). p17 Figure6 challenge space Σ^ξ with Σ={0,1}^κ and ξ=rκ. p24 Theorem4 multilinear PCS uses r=λ and κ=λ in its asymptotic example. This source does not provide a nested FS/QROM proof for our augmented R1CS witness.
- Attema–Fehr–Klooß–Resch (AFKR), The Fiat–Shamir Transformation of (Γ1,…,Γμ)-Special-Sound Interactive Proofs, J. Cryptology 39 article19 (2026-03-06), DOI https://doi.org/10.1007/s00145-025-09569-y. Authoritative full open HTML https://link.springer.com/article/10.1007/s00145-025-09569-y, §3.2 Definition7 exact USEFUL challenge set UΓ(S)={c not in S: exists A in Γ, S proper subset A, A minus {c} not in Γ}, Definition8 tΓ maximum length of successive useful challenges; §6.7 Theorem5 requires TΓ=product_i(tΓ_i+1) polynomial in statement length and efficient uniform UΓ sampling, yielding near-additive FS extractor success. The paper DOES NOT claim every coordinate-wise access structure has polynomial tΓ.

## ONE falsifiable hypothesis / ONE decisive proof
**HYPOTHESIS P21:** CMNW's ACTUAL coordinatewise-star access structure on Σ={0,1}^κ, ξ=rκ has tΓ=poly(λ), permitting a DIRECT polynomial-time AFKR2026 Theorem5 extraction using that original Γ.

**FALSIFIER / PROVED THEOREM:** For any finite alphabet Σ, b=|Σ|≥2, ξ≥3, let Γ be the monotone upward closure of coordinate-wise stars in C=Σ^ξ. Then
    **tΓ ≥ b^{floor(ξ/3)}.**

**Proof:** Put h=floor(ξ/3), choose a distinguished 0 in Σ and define a code D of all vectors (a1,a1,a1, a2,a2,a2, ..., ah,ah,ah, 0,...,0) as ai range independently in Σ. D has exactly b^h words, pairwise Hamming distance≥3.

List D in ANY order c1,...,c_{b^h}. For prefix S={c1,...,c_{i-1}}, choose c=ci. Since S⊂D and min distance3, S is Γ-free. For each coordinate j select a valid different alphabet symbol and define neighbor n_j by changing ONLY coordinate j of c. Set A=S union {c} union {n_1,...,n_ξ}. Then A∈Γ via star with center c. After REMOVE c, the set A\{c}=S union {n_j} contains NO Hamming-distance-one pair:
  (i) two codewords in S have distance≥3;
  (ii) for s∈S, d(s,n_j)≥d(s,c)-1≥2;
  (iii) for j≠k, d(n_j,n_k)=2.
Any coordinatewise star contains distance-one neighbors, so A\{c}∉Γ. By the EXACT AFKR2026 Definition7, c∈UΓ(S). Every codeword can be added as a USEFUL challenge. AFKR Definition8 therefore gives tΓ≥|D|=b^h. QED.

At CMNW Σ={0,1}^κ (b=2^κ), ξ=rκ:
    **tΓ ≥ 2^{κ floor(rκ/3)}.**
Even ξ≥3 gives t≥2^κ; if source asymptotic r=κ=λ, tΓ≥2^{λ floor(λ²/3)}=2^{Ω(λ³)}, superpolynomial for standard polynomial-size public statements. Therefore TΓ cannot be polynomial under THIS ORIGINAL Γ, so AFKR2026 Theorem5 efficiency premise FAILS for direct transfer. Original CMNW interactive (ξ+1)^ell condition is DISTINCT, not contradicted.

**Scope/limitations:** This is a provable obstruction to the APPLICATION of one general FS theorem, not a proof CMNW FS is insecure or that no alternative polynomial-time extractor exists. A more permissive Γ' based on bounded integer/unimodular spanning challenge sets may avoid the bound; FULL integer bounded norm at 2beta_* must be preserved. Rank mod2 alone insufficient to infer short integral openings. Other routes: dedicated FS extraction, alternative PCS, different transcript. P11/P12 Galois algebra is conditional; nested outer-ROM, source Zq-to-R_Q adaptation, SIS 2beta_* and QROM all unresolved. P17 concrete efficiency PARK.

## ONE independent executed certificate
Python checked the above min-distance-three code and usefulness certificate for alphabet/coordinate cases (b,ξ)=(2,3),(3,3),(4,3),(2,6),(3,6),(4,6),(2,9),(3,9), all PASS. At every codeword prefix, A\{c} was verified to have NO distance-one edge. This is a deterministic cross-check of a symbolic theorem, NOT a brute-force tΓ calculation nor a cryptographic test.

Actual files:
- /mnt/data/pvfhe_p21_gamma_star_code_lower_bound.py SHA256 17e248dc0786f2b0fdb62831d7b143bb995600d86dd2b45ff97ec014bd929edf
- /mnt/data/pvfhe_p21_gamma_star_lower_bound_results.json SHA256 f0b2a8cd8a65de59e3f08e0665c37ffe78d9f44764e80ed204360c18a14a457e
- /mnt/data/PVFHE_P21_Gamma_Star_Exponential_Lower_Bound.md SHA256 b3100e3e21b6206ad6e759cd0d539a94bb4ce7a6d45ff55965e02f738b05dd02

## End of iteration
**STATUS:** PASS general exponential tΓ lower bound / certificate, FAIL direct 2026 AFKR tΓ-poly condition for original CMNW star, UNCLEAR/HUMAN_REVIEW any alternative Γ', full ROM/QROM/SIS. Not an original cryptosystem security claim.
**RESULT:** Arbitrarily long useful sequences are constructed via q-ary distance-three codes, exponential in challenge alphabet's log-size times ξ. No further same-shape finite enumeration needed.
**NEXT_ACTION (P22 only if PI continues):** ONE smallest source-level audit whether CMNW Lemma1 has a STRICTLY LARGER admissible Γ' (integer-unimodular right inverses with bounded coefficients) whose tΓ' might be polynomial. First try to falsify that prospect using a few challenge matrices and norm-slack algebra; if no viable Γ'/extractor in ONE iteration, PARK integrated PCS repair and present PI HUMAN_REVIEW package. Do not assert 2026 theorem applicability merely from span over F2.
**STATE_UPDATE:** YES ONLY this new P21 standalone finding. Do not modify parallel global STATE.md/vFHE/SHIP or P01–P20.
