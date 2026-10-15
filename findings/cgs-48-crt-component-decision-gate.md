# CGS-48: Global Gram-conditioned entropy does not imply decisional MLWE

Date 2026-10-15. Single active PI-selected CGS, prior CGS47. ONE primary hypothesis, ONE small exact CRT falsifier. Not an attack on the original Okada–Takagi construction; not a novel cryptographic theorem. Parent two-round standard MLWE no-O(LDec) Gaussian issue OPEN.

## Primary hypothesis and failure condition

H-CGS48 (FAIL): Because Boudgoust et al. PKC2026 give search hardness with a known-covariance quadratic hint under sufficient overall average conditional min-entropy, perhaps checking high global Htilde_inf(s|h(s)) alone suffices to obtain low-rank DECISION known-covariance MLWE hardness for semantic FHE. FALSIFIER: a legal negacyclic quotient and high-global-entropy rank2 secret distribution where h(s)=sum_i s_i s_i* is public, yet one CRT component is deterministically zero, permitting an exact decision distinguisher under short errors.

## Original sources

1. Lin, Wang, Zhuang, Wang, Hardness of Entropic Module-LWE, Theoretical Computer Science 999 (2024), 114553, DOI https://doi.org/10.1016/j.tcs.2024.114553. Final published 26-physical-page PDF from TU Delft https://repository.tudelft.nl/file/File_feeb7873-5fbd-46fa-b16d-dc10b38ec991, article introduction physical PDF p4 §1.1. The authors EXPLICITLY distinguish search-vs-decision entropic MLWE: highly entropic secrets can be supported inside a proper CRT ideal, making a factor of MLWE output equal to small error, not uniform. Decision-entropic guarantees in Theorems 8 and 9 §4.2 require enough entropy in EVERY prime ideal factor. Their custom leftover hash analysis treats secret plus noise leakage and does NOT automatically handle a distinct public nonlinear Gram h(s). Web screenshot attempt on PDF returned cache miss; equation assertions based on provided PDF text and original publication.
2. Boudgoust, Jeudy, Tairi, Wen, Hardness of M-LWE with General Distributions and Applications to Leaky Variants, PKC2026/ePrint2025/1472 https://eprint.iacr.org/2025/1472, original 35-physical-page Research MCP PDF SHA256 63d6367243af89b4f495ed9a720c64f424a54221cbb71e6f82d627c8a4a417cb, VERSION_UNVERIFIED. Theorem4.1 pp17-18 and Appendix A pp30-32 conclude SEARCH MLWE in their model, at theoretical high rank; §1.2 p6 explicitly states no corresponding decision theorem. §6.2.2 p25-26 considers HNF secret-ERROR x*x hint rather than automatically the standalone FHE SECRET-only Gram h(s). This CGS48 does not refute it.
3. Okada, Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, ePrint2025/409 https://eprint.iacr.org/2025/409; latest full original 40-physical-page Research MCP PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Algorithm7 physical p29 uses secret Gram covariance Σ_s=sum Gram(s_i), hidden during its standard-MLWE Gaussian-padding approach. This toy uses a CRT-CONSTRAINED secret UNIFORM MOD q, not its bounded iid small coefficient secret, and is not a ciphertext security attack.

## The ONE exact counterexample [DERIVED]

Ring R_q=F_97[X]/(X^4+1), rank d=2. Mod97, X^4+1 has four distinct roots 33,47,50,64. Choose public rho=33, rho^-1=50. The evaluation map ev_rho:R_q→F_97 is a CRT coordinate. Draw the two secret ring elements independently UNIFORMLY from the kernel {s : s(rho)=0}, which is an F_97-linear space of dimension3 for each secret. Thus total secret choices=97^6 and H_inf(s)=6log2(97)=39.599477 bits, while the projected secret ev_rho(s1,s2) is ALWAYS (0,0), entropy ZERO.

Expose the SECRET-only autocorrelation/Gram hint h(s)=s1 s1*+s2 s2*, where star maps X→X^-1 mod X^4+1. For odd q and n4, h=h* forces h(X)=c0+c1(X-X^3); coefficient at X²=0 and at X³=−c1. Since each si(rho)=0, h(rho)=sum si(rho)si(rho^-1)=0. This linear constraint fixes c0 given c1, so |Image(h)|<=97. For UNIFORM secret s and deterministic h, the AVERAGE conditional min-entropy satisfies exactly Htilde_inf(s|h) = log2(|Support(s)|/|Image(h)|), hence

Htilde_inf(s|h) >= (6−1)log2(97) = 32.99956421093564 bits.

This is substantial TOTAL entropy for a toy, although the per-ideal (rho) conditional entropy is exactly 0. The hint h itself satisfies h(rho)=0 and can be given to adversary; it is not used by the distinguisher.

Take short coefficient error e_j iid uniform {-1,0,1}, public A=(a1,a2) uniform in R_q^2, real b=a1*s1+a2*s2+e. Then b(rho)=e(rho) ALWAYS. Enumerating all 3^4=81 error coefficient tuples gives |E|=81 for E={sum_j e_j*rho^j mod97}. The uniform challenge branch b←U(R_q) has ev_rho(b) uniform F_97. Distinguisher D=[ev_rho(b)∈E] accepts real with probability1, uniform with probability81/97. Exact one-sample advantage 16/97≈0.16494845360824742. With 20 independent public samples from same fixed secret, independent errors and uniform challenge outputs, advantage 1−(81/97)^20≈0.9728189836218548.

This shows GLOBAL Gram-conditioned min-entropy ALONE cannot imply decision hardness. It is a source-shaped toy of the *algebraic ring* but NOT the SOURCE χ distribution, not a proven search-hard family nor a 128-bit attack. The underlying conceptual CRT secret support obstruction is prior art from Lin et al. 2024, not newly discovered cryptography. It does not imply real iid coefficientwise bounded MLWE secrets have a deterministic zero ideal component or are weak. Search hardness of the toy itself is NOT demonstrated and need not be for this falsification of the proposed simplistic entropy implication.

## Minimal executable validation [EXACT]

Script /mnt/data/cgs48_crt_decision_leakage_gate.py SHA256 066bbc9b218d30d04c70e038486a83f2eabfbebc871864f019587504bf0adabd.
JSON /mnt/data/cgs48_crt_decision_leakage_results.json SHA256 01268f69c11db7bbfdb5ebf0ad3aca8093b59bdd4dc7967cf8a5e1bfe01ea7bc.
Plain Python finite-field/negacyclic polynomial code: 4 CRT roots found, 81 exact ternary error projection residues, exact rational one/20-sample advantage, q^6 secret count and ≤q hint values. 512 seed-controlled random uniformly CRT-constrained secret pairs verify zero secret projection, selfadjoint h, h(rho)=0, and for real b, b(rho)=e(rho)∈E. No network/FHE/cryptographic security experiment.

## Scientific interpretation / next action

PASS complete original prior-art theorem-scope review plus explicit secret-ONLY Gram-conditioned CRT counterexample; FAIL H-CGS48 inference from global conditional minentropy to decisional source MLWE. The legitimate decision-entropy result in Lin2024 requires per-factor entropy, but its actual proved auxiliary leakage is not arbitrary Gram. Therefore even adequate ideal-wise minentropy does not automatically imply a complete known-covariance decision theorem without a new masked-secret/leakage reduction matching the source.

NEXT (ONLY on PI next "继续"): CGS49 should run ONE genuinely SOURCE-SHAPED coefficientwise uniform ternary low-rank small-ring n4/q97/d2 exhaustive 3^8=6561 conditional CRT-ideal minentropy after SECRET-only Gram. Verify whether zero-factor attack is absent and quantify actual conditional per-ideal entropy; no extrapolation to real q/security parameters. Then decide if a plausible new decision-hint leftover-hash mechanism exists, or PARK again. Do not repeat constructed CRT-supported toy. PI alone decides pivot or new assumptions.

ITERATION CGS-48. STATUS FAIL global-entropy-only decision inference; PASS exact algebraic falsifier and prior-art alignment; HUMAN_REVIEW strict CGS two-round O(LDec) goal remains OPEN; no FHE construction/new attack/novelty. STATE_UPDATE YES own finding, cumulative CGS and sole root; no other targets modified.