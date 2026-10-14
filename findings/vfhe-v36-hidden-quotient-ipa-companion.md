# vFHE V36 Companion — Same prebound C_a, HIDDEN quotient k, PUBLIC original native F.2 y

2026-10-15. COMPANION to canonical ALREADY-COMPLETED V36 (the raw public-S Bulletproofs IPA privacy/cost finding). NOT a new numbered round; preserve V37 NOT STARTED and GLOBAL general I192 FROZEN.

## One falsifiable companion hypothesis and cheapest test

Can the V36 proposed arbitrary-weight IPA be reformulated on SAME prechallenge global canonical digit commitment T such that only original source F.2 authenticated native evaluation y (NOT additional canonical-lifted integer S) is PUBLIC, by proving the inner product of an augmented secret vector (a,k) with public weights (c,-p)? **PASS exact arithmetic relation and 8/8 small-group IPA checks; FAIL any complete privacy or integrity claim absent a proven ZK IPA, knowledge-binding under suitable bases, quotient range proof, and native-PCS/FS composition.** No actual secure cryptographic deployment tested.

## Source anchors [FACT]

Bünz et al., Bulletproofs, ePrint2017/1066 §3, 45pp Research MCP public mirror SHA256 c79f9c32d061c6814e57d1d4007958efed66923f0194497e8596aa3edd387a53, VERSION_UNVERIFIED: ordinary arbitrary-weight IPA but not a ZK proof by itself. Segev 2025, Bulletproofs for R1CS: Bridging the Completeness-Soundness Gap and a ZK Extension, ePrint2025/327 §2.2 Theorem2.6, 31pp mirror SHA256 029c913fbd6b4f9e1146b9ccdad4e2c0f5b5af860645cc2272603970cd0331c6, VERSION_UNVERIFIED: P=<u,G>+<v,H>+alpha H0, omega=<u,v>, a public-coin proof with perfect special-HVZK and computational witness-extended emulation under the published independent-generator DL assumptions. Yang et al., ePrint2024/827 §4 uses ONE Pedersen subvector T=product G_j^a_j H0^eta but its indexed structured pairing SRS is NOT automatically a BP/Segev independent-generator CRS. Cascudo et al., vFHE ePrint2025/286, F.1/F.2 native Merkle/RS PCM public y: inspected 52pp mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; official 2026 revision VERSION_UNVERIFIED. Our proposal and toy are NOT the authors' algorithm or a published vulnerability.

## Relation [DERIVATION]

Commit before native r: T = product_(j<H) G_j^(a_j) H0^eta, global a_j integers in [0,beta). After native original F.2 authenticates y_t in one degree-d factor over prime p at challenge r, canonically lift its Boolean MLE weights c_j in [0,p-1], and set secret bounded integer quotient k=(sum c_j a_j - y_t)/p. Commit K=G_k^k H0^rho AFTER r, with a fresh blind. Define secret u=(a_0,...,a_(H-1),k), public v=(c_0,...,c_(H-1),-p), public P=T*K*product H_j^(v_j), and public inner-product TARGET omega=y_t. Then P=<u,G>+<v,H>+(eta+rho)H0 and omega=<u,v> equals y_t exactly. An actual Segev extended RIP PoK might provide zero knowledge for this statement under its own proof and generator assumptions. V36 public-S IPA not needed for this relation. The quotient K is perfectly hiding with uniformly random rho but a PROVEN ZK proof transcript is still required; plain §3 IPA itself is not zero knowledge.

A separate 0<=k<=Kmax RANGE PROOF on exactly K is CRITICAL; otherwise the IPA proves only equality mod the proof scalar group order. Also require global digit range on exactly T, original F.2 native source binding, prechallenge order for T, independently secure generators, and composed Fiat-Shamir/simulation/extraction; none of these are automatic from a toy IPA.

## One exact test + soundness negative control [EXPERIMENT]

Actual original-style F.2 Merkle/RS full encoded-column tests using existing V32 verified toy. Legal N4,d2,ellstar3,H8,beta4,p13=1+4*3,p29=1+4*7, native extension K13=F13[u]/(u^2-5) and K29=F29[v]/(v^2-12). Challenge r_p=(2+u,3+2u,4+3u) for each p in its own field.

Use TWO legitimate globally canonical digit vectors in V32's low-bit-first Boolean index convention:
 a=(0,0,0,0,0,1,0,0), b=(0,0,0,0,1,0,2,0).
Original native SHA256-Merkle/RS F.2 authenticates EXACT same PUBLIC y coordinates (p13 first/second, p29 first/second)=(10,12,20,8) for both. But integer sums S(a)=(10,12,20,8), S(b)=(10,12,20,37) differ by 29 in fourth coordinate. Publish native y ONLY; k is privately committed in eight random Pedersen K values. For each a/b, one unchanged prebound T is reused across four source native evaluations. An algebraic 4-round ordinary folding IPA is ACTUALLY CONSTRUCTED and VERIFIED for every coordinate: 8/8 honest toy proofs ACCEPT; all 8 changed public y+1 versions FAIL. The quotient K commitment's marginal distribution is EXACTLY uniform for each k in the toy order1009 subgroup when rho ranges over all1009 blinders. THIS DOES NOT PROVE THE IPA TRANSCRIPT IS ZK. The toy group has trivial discrete logs, no security claim.

Negative control: even if T binds a=0, a fraudulent native y=1 under p13 can pass modular inner product using k=388 because 0 = 1+13*388 (mod1009). An executable IPA **ACCEPTED** this wrong native-y statement. Requiring 0<=k<=23 rejects it. Hence **hidden-quotient IPA without the quotient RANGE is unsound as a canonical INTEGER link**, not an issue in original source.

### Native table ordering reconciliation

Authoritative V36 earlier collision pair used MSB-first Boolean indexing, V32 encoded PCS toy uses LSB-first. 3-bit reversal [0,4,2,6,1,5,3,7] maps the earlier two reported vectors into the V32 index convention and reproduces precisely their reported integer sums (6,18,12,10) vs (32,44,70,39). This is only a Boolean-bit ordering convention difference, NOT an invalid earlier counterexample. The new a/b above uses native V32 indexing directly. Any real transcript must specify the same ordering as the actual F.2 matrix encoding.

## Work and limits

Illustrative H=2^24, two p,d4 -> eight IPA coordinate statements. An unoptimized standard power-two folding with appended k and blinding coordinate pads H+2 to 2^25 witness positions; 50 group +2 scalar proof objects per ordinary IPA -> 1664B, 8 proof bodies 13,312B, plus eight new quotient commitments ≈256B, single T, original F.2, digit and quotient range, and CRS. For Segev's own HVZK RIP theorem at such length its source stated proof is 2log2 n+2 group and 3 scalars => 1760B per opening, 14,080B for eight, BUT our small-group ordinary folding is NOT that actual published proof. Source-based O(H) prover/verifier group work remains high (V36 main >2bn symbolic group operations for eight unbatched padded proofs). No actual deployment benchmark, ZK simulation, source F.2 compiled code, independent-generators-from-Yang-SRS proof, or end-to-end soundness.

**STATUS PASS scoped algebra/8 IPA toy / FAIL range-free claim / UNCLEAR actual ZK source composition.** Preserve V36 main H-V36 FAIL public lifted-S disclosure. **NEXT V37** remain one published ZK arbitrary linear opening/hidden quotient with same prebound T and authentic range, source code performance, or HUMAN_REVIEW/PARK. Global I192 frozen and no unsolicited author disclosure.

Local reproduction twice-identical:
Python /mnt/data/vfhe_v36_hidden_quotient_ipa_companion.py SHA256 58ce12cc211e5bdf35a9a6d4582fb415aae38f4dbad2b04272311b7baee819bb
JSON /mnt/data/vfhe_v36_hidden_quotient_ipa_companion_results.json SHA256 0797990d607a616010777b193ab01d47dd2ea9a3f2f961c944861aa6c3f20260
Complete report /mnt/data/VFHE_V36_Hidden_Quotient_Same_VC_IPA_Companion_2026_10_15.md SHA256 c18f2916b7e11ba98eadbd2f3ad6899c44dc1d3207ddee297ea7929496560cd8
Depends on existing V32 native Merkle/RS Python SHA256 071243936179dc9e0ffa2c6141fac69c72a721fc9e0bfc51ba311ac41f1b02c5.
