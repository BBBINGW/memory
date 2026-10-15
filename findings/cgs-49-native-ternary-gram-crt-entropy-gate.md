# CGS-49: exhaustive native ternary Gram-conditioned CRT entropy

Date: 2026-10-15. Single active PI-chosen CGS research task, CGS-48 previous. ONE hypothesis and ONE complete exact enumeration. Strict original Okada–Takagi 2025/409 standard MLWE two-round no-O(LDec) padding remains OPEN.

## Primary H-CGS49 and minimum decisive test

Does CGS-48's deliberately CRT-kernel-supported secret, whose selected CRT component is ZERO with probability one, reflect realistic iid small-coefficient MLWE KeyGen secrets? Switch to iid uniform ternary coefficients in ring R=F97[X]/(X^4+1), native module rank d=2. Enumerate all 3^8=6561 equiprobable key pairs (s1,s2). Publish the COMPLETE integer secret-only Gram autocorrelation hint h=s1*s1*+s2*s2*. For each of four CRT roots, compute the conditional joint module secret vector V_rho=(s1(rho),s2(rho)) average min-entropy, average collision entropy, probability V_rho=0, and the exact CGS48 error-support distinguisher advantage. Do not imply actual standard MLWE security or real FHE parameters.

## Source facts

Okada–Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, ePrint2025/409 https://eprint.iacr.org/2025/409, full original newer 40 physical-page Research MCP PDF, SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Definition3.1 p12 specifies negacyclic ring and secret Gram; Algorithm7 p29 privately uses Sigma_s=sum Gram(s_i) to sample secret-conditioned Gaussian pads per session. Publishing Gram is a PROPOSED changed interface, not original protocol. The source's real KeyGen, error/flooding, singularity and security parameters are not modelled.

Lin et al., Hardness of Entropic Module-LWE, TCS999 (2024) 114553, DOI https://doi.org/10.1016/j.tcs.2024.114553, requires high enough per-prime-ideal secret entropy for its decision result under a specific masked-secret auxiliary-information game, not automatically arbitrary public Gram h. Boudgoust et al., Hardness of M-LWE with General Distributions and Applications to Leaky Variants, PKC2026/ePrint2025/1472 https://eprint.iacr.org/2025/1472, original 35pp PDF SHA256 63d6367243af89b4f495ed9a720c64f424a54221cbb71e6f82d627c8a4a417cb, proves SEARCH known-covariance M-LWE in theoretical high-rank HNF secret+error hint scenario, not low-rank decision secret-only Gram hardness. The CGS-48 CRT secret in a proper ideal was not iid small coefficient KeyGen.

## Exact derivation and enumeration

Take n=4,q=97, rank d=2, coefficients independent uniform {-1,0,1}. Roots of X^4+1 in F97 are rho=33,47,50,64. Compute true INTEGER negacyclic involution X->X^-1 and h=s1*s1*+s2*s2*. Every h has form c0+c1(X-X^3), coefficient c0=sum of all eight squared secret coefficients in [0,8]. All 6561 keys generate exactly 39 distinct COMPLETE h hints, class sizes 1 through 448. h=0 has only one key, the all-zero key, and public h=1 has 16 preimages.

For each rho, single-polynomial evaluation is INJECTIVE over the 81 ternary coefficient polynomials in this particular tiny field. Thus the two-component map S->V_rho is injective over all 6561 keys. Its unconditional min/collision entropy is log2(6561)=12.679700005769249 bits. Given each exact h, its conditional joint V_rho distribution is UNIFORM on the preimage of h. Hence the average conditional min-entropy and average conditional collision entropy both equal:
   -log2[39/6561] = log2(6561/39) = 7.394297786907001 bits
for EACH of the four roots. The drop is log2(39)=5.285402218862249 bits in these specific entropy measures; not a general high-dimension loss theorem or Shannon mutual information statement. For the FIRST module component alone instead of the joint module vector, average conditional min=4.090985370186986 and conditional collision=4.372967253452686 bits. Worst-case conditioned-on-a-particular-h min-entropy is ZERO at h=0, but this hint has only 1/6561 probability in the toy.

At every root the zero CRT rank2 vector V_rho=(0,0) occurs ONLY for the all-zero secret; exact probability 1/6561 instead of probability one in the contrived CGS48 CRT-kernel distribution. For a public uniform module row A and independent coefficientwise ternary error, when V_rho!=0 the projected b(rho)=A(rho)dot V_rho+e(rho) is EXACTLY uniform F97; when V_rho=0 it is e(rho). The ternary error projection support E at rho=33 has exactly 81 residues. Thus the unchanged CGS48 support-membership distinguisher has exact ONE sample advantage:
   (1/6561)*(1-81/97) = 16/636417 = 2.5140748911484138e-5.
For 20 independent public samples on the SAME underlying secret, testing that ALL projected samples lie in E has exact advantage:
   (1/6561)*(1-(81/97)^20) = 0.00014827297418409615.
Public Gram h=0 already identifies the rare all-zero key. The unusual small-q injectivity and its entropies cannot be extrapolated to n1024 or lambda128, and these are NOT attacks on unmodified source.

## Reproducible one test

Executable Python: /mnt/data/cgs49_iid_ternary_gram_crt_gate.py
SHA256 8085d929781bf021b8c77dfbaa5beec8151a05f40c8b79df1cdc93f330bce71e.
Machine-readable data: /mnt/data/cgs49_iid_ternary_gram_crt_results.json
SHA256 5d3ac3ef0179d5ff7587c61f3c9075fac23e303cdc6d8825bdba3496d241768b.
Pure Python exact exhaustive 6561 secrets, integer negacyclic ring arithmetic, full Gram/hint distribution, 4 CRT roots, conditional count tables, exact rational membership advantages; floating log2 only to display entropy in bits. Ran twice with identical hashes. No Monte Carlo, MPC/FHE implementation or cryptographic hardness estimate.

## Scientific verdict

STATUS PASS exact model comparison and per-ideal Gram-conditioned min/collision entropy; FAIL extrapolating CGS48's constant probability CRT-zero attack to iid ternary KeyGen; UNCLEAR actual decision MLWE semantic security. The toy confirms full secret Gram is statistically informative but cannot justify a full crypto claim. No novel primitive, no original-paper attack or security theorem established. Parent O(LDec) two-round hidden-Gaussian issue remains OPEN/HUMAN_REVIEW.

NEXT CGS-50 only on the next PI continuation: attempt ONE analytic, asymptotic bound for average conditional collision entropy of EACH rank-d CRT secret vector given actual secret-only integer Gram h under specified source chi_mlwe and q splitting, aligned to a decision leftover-hash theorem or a concrete counterexample. Do not infer hardness solely from a toy or from positive entropy. If no fresh proof interface, recommend PI park/pivot rather than repeating 3^n enumerations. STATE_UPDATE YES: finding, cumulative CGS, single authoritative root; no unrelated workstreams.