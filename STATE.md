# FHE Research State — vFHE Cross-CRT Consistency after I196

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED ITERATION:** I196 COMPLETED. I197 NOT STARTED.
**STATUS:** PASS exact prime-to-extension Hamming-distance invariance for integer-generator linear codes; FAIL direct applicability of published weighted nonbinary RAA linear-distance theorem to unweighted repeat-2 two-accumulator target; UNCLEAR prime-field distance and full vFHE repair. HUMAN_REVIEW before next test; NOVELTY NOT VERIFIED.

## HUMAN-SELECTED PARENT TARGET

vFHE cross-CRT common scalar digit-index consistency. Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286 (https://eprint.iacr.org/2025/286). Previously examined 52pp mirrored PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest parity VERSION_UNVERIFIED.

**[DERIVED I59–I60]** Per-field CRT lookup enforces rectangular componentwise membership, not diagonal membership of one bounded scalar digit; source-form R=Z77[X]/(X²+1), h56↦(0,1) shows ideal-oracle PIOP gap under inspected version. NOT a verified real deployed SNARK exploit, nor author-confirmed latest edition vulnerability.

## I196 — ONE PRIMARY HYPOTHESIS / DECISIVE TEST

**Question:** Can extension-field arithmetic produce shorter field-linear codewords for the same bounded-integer generator matrix in a genuine two-independent-interleaver RAA design?

**[DERIVED, PASS]** For ANY G∈F_p^{k×N}, the minimum Hamming distances of the generated codes over F_p and F_(p^d) are EQUAL. Proof: decompose extension input in an F_p-basis b_j, so xG=Σ b_j x_jG; support of xG is the UNION of the supports of x_jG, and every base-field codeword embeds. Thus no extra extension-field min-distance obstruction for integer G reduced mod the same p. This is a standard elementary coding-theory lemma, not a new theorem / novelty.

**[EXACT TEST, PASS]** Genuine independently seeded π1/π2 in repetition-2, two-prefix systematic integer RAA `E(x)=(x,Prefix(P2 Prefix(P1 Rep2(x))))`, m4. Enumerated 3^4−1=80 nonzero F3 messages and 9^4−1=6560 nonzero F9 messages using F9=F3[α]/(α²+1); EXACT dmin=4 in both. Local reproducible script `/mnt/data/vfhe_raa_extension_invariance_gate.py` SHA256 `e0aa5283830e6514a535e8e86394a8571b322f92d85dcb38c94184bb2d9d1d7d`; JSON `/mnt/data/vfhe_raa_extension_invariance_gate_results.json` SHA256 `a433f26af9b3ca768ed4d1a16e65189a97eddb866124a63c8e531975879c071e`. Local files are NOT GitHub files.

**[SOURCE GATE FAIL, model mismatch not counterexample]** Rosnes–Graell i Amat, *On the Analysis of Weighted Nonbinary Repeat Multiple-Accumulate Codes*, arXiv1101.5966 (https://arxiv.org/abs/1101.5966), source Theorems 4/5, analyzes nonbinary RAA **with random nonzero FIELD weights** and a memory-one accumulator with generator 1/(1+D), whereas proposed canonical integer RAA uses fixed 0/1 coefficients and ordinary positive prefix 1/(1−D). Theorem5 linear distance guarantee covers L≥3,n≥2 or L=2,n≥3, **NOT n=2,L=2**; its proven numeric field-size range is 3≤q≤2^25, while p_min in vFHE has ≈49 bits and fields can be degree4. Our invariance lemma reduces source F_(p^4) analysis to F_p but p remains >2^25. Neither the binary RAA result arXiv0810.3422 nor this weighted nonbinary result directly proves constant prime-field distance of the proposed unweighted generator. DO NOT claim new negative theorem about all genuine RAA.

**[CONDITIONAL no-wrap]** With nonnegative digits x∈[0,β−1]^m and two positive accumulators after repeat2, max encoded symbol ≤m(2m+1)(β−1). For m256 or m1024, β2^20, bounds 137707257600 (<2^38) and 2200094899200 (<2^42), both below p_min≥2^48. Not a source-validated β/m mapping or bound for PCS random challenges.

**[EXPLORATORY NOT FULL dmin]** For separately seeded true two-interleaver instances exact weight≤2 signed binary-difference scans yielded observed 123/768 (m256), 133/1536 (m512), 922/3072 (m1024). These are instance-specific upper-bound witnesses; cannot claim asymptotic shrinking/growth because seeds differ or that true dmin was calculated.

## TOPIC FILE / RECORD KEEPING

Authoritative subject research file: `findings/vfhe-cross-crt-consistency-research.md`, **Section 13** for I196, Section12 for I195 cyclic double accumulator no-go, Section11 for I194 row-weight2 single accumulator no-go. Avoid additional numbered findings files unless one distinct major artifact is needed. Old failures I95 and I136–151 remain archived.

## MAIN BLOCKER

Even with extension-field equality proved, **prime-field positive linear Hamming distance** for the actual unweighted small-integer 2-repetition, two-independent-interleaver code is NOT known here. Published field-good weighted proofs assume coefficients unavailable for bounded canonical integer encoding. There is also NO valid shared integer Merkle PCS binding/proximity + privacy/ZK + Fiat–Shamir + 128bit error + end-to-end cost proof. The overall vFHE cross-CRT repair remains OPEN/UNCLEAR.

## NEXT_ACTION — ONLY if PI requests continuation

ONE precise prime-field distance falsifier for the unweighted true independent two-interleaver repeat2/accumulate2 integer code. Prioritize exact low-support or asymptotic codeword family; or one rigorously applicable proof technique without native-field random weights, at source-scale m256/1024. If cannot establish either, report UNCLEAR. An alternative n3,L2 or 3 accumulators is a strategic subbranch requiring PI choice; do not label weighted theorem a turnkey proof.

## OTHER BRANCHES

AKU I190–192 source-version gated; LFBS I188–189, threshold PRSS I184–187, GBFV and dBFV→BGV/GL BigSwitch parked/archived. Agent protocol: ONE hypothesis + ONE cheapest decisive test per authorized iteration, read before write; PI controls parent targets, novelty/strategic pivots, disclosure.
