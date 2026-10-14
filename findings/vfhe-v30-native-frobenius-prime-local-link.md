# vFHE V30 — Authenticated native MLE factor alignment and Frobenius twist are prime-local only

**Date:** 2026-10-15. **GLOBAL FHE I192 FROZEN**. One independent V30 iteration, one primary hypothesis, one cheapest decisive exact test.

**Primary H-V30:** Can we use the *existing* separately binding source F.1/F.2 native field MLE evaluation oracles to certify that every digit at Boolean points is a **common F_p scalar across all factors belonging to one prime p**, without V29's potentially unauthenticated coefficient-vector Galois recomposition witnesses? Crucially, do NOT presume this suffices for one canonical INTEGER digit across DISTINCT primes.

**STATUS: PASS conditional native-PCS prime-local scalarity gate / FAIL complete multi-prime canonical integer digit repair.** This is a math/source-interface result, not an implemented compiler, authored-paper exploit, zero-knowledge proof, field commitment benchmark or publishable novelty claim. Actual official Feb2026 ePrint2025/286 binary VERSION_UNVERIFIED.

## Primary original source [FACT]

Cascudo et al. *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025 / ePrint2025/286, inspected 52 physical page Research MCP GitHub mirror, SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19. Section3.1 p10: p_i=1+(2N/d)*odd, R_p product k=N/d distinct degree-d field factors. Appendix F.1 p50: a ring-valued polynomial commitment is the tuple of independent native field polynomial commitments, eval points and output projected via CRT. Appendix F.2 p51: native Brakedown/Merkle/RS polynomial evaluation sends actual native v' and verifies y=<v',q2> and sample-coded columns. Section4.3 pp20–24: per-field digit table t_beta={0,...,beta−1}⊂F_p. Native field-isomorphism normalization/Frobenius gate below is OUR proposed extra checker, not source protocol text.

## Scoped derived lemma [DERIVATION]

Fix ONE p, product R_p ≅∏_(j=0)^(k−1) K_j, K_j≈F_(p^d). Pick a common canonical K=F_(p^d) and publicly specified F_p-isomorphisms psi_j:K_j→K. Each genuine *precommitted* native h_j is an ell-variate multilinear polynomial whose Boolean coefficient vector is (h_(j,b))_b. Define normalized K-valued MLE P_j(X)=Σ_b psi_j(h_(j,b))eq(X,b). Note P_j(r)=psi_j(h_j(psi_j^−1(r))) with inverse applied to all evaluation point coordinates.

Verifier samples uniform r∈K^ell AFTER PCs bind. Demand each P_j(r)=P_0(r), j=1..k−1, by authentic native F.1/F.2 evaluations. Demand P_0(r^p)=P_0(r)^p using ONE additional native F.2 evaluation at psi_0^-1(r^p). Since
P_0(r^p)−P_0(r)^p=Σ_b (a_b−a_b^p)eq(r^p,b),
the Frobenius identity as a polynomial in r^p holds iff every normalized Boolean coefficient a_b belongs to the fixed subfield F_p. Cross-factor polynomial identities hold iff all factors have the exact same normalized a_b. Conversely common scalar F_p coefficients pass for all r.

If any native Boolean coordinate family fails one-prime scalarity, at least one of these difference MLEs is nonzero of total degree≤ell (the Frobenius comparison is considered in independent variable s=r^p, and this map permutes K uniformly). Standard Schwartz–Zippel thus bounds conditional algebraic false acceptance by ell/p^d, ADD native PCS opening/binding failure probabilities. This is NOT a full interactive proof/composition theorem; correlated native eval points and F.2 sample order must be handled explicitly.

**Important cost reduction:** If the original per-native-field beta lookup is already **knowledge-sound** and enforces h_(j,b)∈{0,...,beta−1}⊂F_p, the Frobenius assertion becomes redundant. Then only k mapped native PCS evaluations per p enforce *same digit within that p*. Without assuming the original native table relation, k+1 openings are used to certify F_p membership directly, independently of the fake coefficient-gadget from V29. This can use F.1 ring challenge containing componentwise mapped field points; it cannot be called "free" or automatically ZK.

## Exact reproducible test [EXPERIMENT]

Source parameters N4,d2,ell3,H8,beta4, p13=1+4*3 and p29=1+4*7, satisfying beta4<pmin13 and 2^ell8<pmin13. Both x4+1 factor as (x²−z)(x²+z): z_ref5 mod13 and12 mod29, with ±z irreducible. For p13 the other field K8 is mapped to reference K5 by u8→5u5 (square=8); for p29 K17 maps to K12 by u17→12u12 (square=17). Isomorphisms are checked algebraically. Original canonical digits table a=(0,1,2,3,0,1,2,3). Three independent toy cases:
- honest: both factor MLEs derived from same basefield digits. Cross-factor alignment and Frobenius PASS in all challenges;
- inconsistent prime-local factor: only second native factor's Boolean index0 changes by +1. Cross-factor alignment rejects except if chi_000(r)=0; reference Frobenius alone (correctly) cannot detect it;
- both factors identically share a normalized NONBASEFIELD coefficient (+u_ref) at Boolean index0. Cross-factor alignment always accepts; Frobenius twisted check rejects except if chi_000(r^p)=0.

For each prime 8192 seeded *true degree2 full-extension challenge* rounds:
p13: honest failures 0, factor-mismatch rejects 8039, nonbasefield Frobenius rejects 8039;
p29: honest failures 0, factor-mismatch rejects 8171, nonbasefield Frobenius rejects 8171.
In these single-position cases exact algebraic miss probability 1−(1−1/p²)^3, p13 ≈0.01764665, p29≈0.00356294, below 3/p². Both runs deterministic, no float as source of truth.

**CRITICAL cross-PRIME obstruction remains:** composite R_377 with canonical integer e=261, e mod13=1 and mod29=0, beta4. All factors within EACH prime are equal F_p digits and pass both alignment and Frobenius EVERY challenge; nevertheless e∉t4={0,1,2,3} in Z_377. V30 does NOT prove one globally bounded digit. A new noncomponentwise knowledge-sound integer commitment/reduction/evaluation proof is still mandatory.

## Cost/implementation flags

Direct gate: k=N/d bound native MLE evaluations at aligned full-extension points + ONE reference Frobenius-twisted evaluation per prime, or k only conditional on original sound native beta lookup. For illustrative N16384,d4 and TWO primes, k4096 gives 8194 vs 8192 native individual evals per checked oracle. A single ring F.1 ProveEval packs native components but does not eliminate each native F.2 cost. Already-existing sumcheck evals potentially reusable if challenges and transcript can legally be coordinated; this is UNVERIFIED. Original F.2 exposes v,v',y publicly; no hiding of small digits or ZK claimed. Native field isomorphisms may require offline computation. No actual source PCS compiler implementation, Merkle proof integration, timings, novel savings or 128bit integration measured.

**Primary decision:** Prime-local scalarity can be checked noncircularly with existing oracle interface (conditional correctness + native PCS soundness), but this is not the target cross-prime canonical INTEGER link. Do not spend more rounds optimizing the already cheap *partial* gate without an actual globally binding CP protocol; prefer HUMAN_REVIEW or continue V31 with ONE precise original-PCS-bound common integer witness proof, native field reduction and explicit cost against V12–V16 baselines. Official Feb2026 ePrint PDF source still SHA-unverified; no author contact without PI decision.

**End iteration:** STATUS PASS conditional prime-local / FAIL full cross-prime; RESULT source-compatible theorem/exact test; NEXT_ACTION V31 conditional integer-to-native linking proof, STATE_UPDATE YES independent V30, GLOBAL I192 FROZEN.

**Local files:** /mnt/data/VFHE_V30_Native_Frobenius_PrimeLocal_Gate_2026_10_15.md SHA256 3fc1f1da6c5bfe61800d0288edf7ebb53446cbdef1b57be94462ba9ad08d54db; script /mnt/data/vfhe_v30_native_frobenius_scalar_gate.py SHA256 03fcc8f22ebeb3153765457d1d2f0fbd97b5e21f879e31e0483c25c0ff4cb34b; JSON /mnt/data/vfhe_v30_native_frobenius_scalar_gate_results.json SHA256 69f127bcac210899fc80d2b066de779abdc8383ce794847d7f180c6875d33185.
