# CGS-51 — Full-ring ideal collision formula and statistical-method no-go

Date: 2026-10-15. Single PI-selected CGS, prior CGS50. ONE primary hypothesis and ONE decisive full-ring exact enumeration plus support-size proof. Original Okada–Takagi ePrint2025/409 standard MLWE two-round T-out-of-N removal of O(LDec) Gaussian pads remains OPEN.

## H-CGS51

Can the CGS50 one-CRT noise-aware collision identity be generalized to the COMPLETE finite ring with secret-only Gram leakage, then provide negligible statistical distance for the native small-secret/small-error low-rank M-LWE output? Verdict: exact ring identity PASS; statistically-close-to-uniform inference FAIL for the regime with small coefficient supports. This DOES NOT break computational MLWE, or the unchanged source paper.

## Source provenance / prior art

Okada–Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025/ePrint2025/409, https://eprint.iacr.org/2025/409, full newer Research MCP original 40pp SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301 (VERSION_UNVERIFIED). Algorithm7 physical p29 constructs private per-session Gaussian based on secret Gram Sigma_s. The public Gram H=h(S) in CGS51 is an expressly altered setting, NOT an actual source exposure. Evaluation keys, adaptive ODec and threshold simulation are OUT of this lemma.

Lin, Wang, Zhuang, Wang, Hardness of Entropic Module-LWE, TCS999 (2024) 114553, https://doi.org/10.1016/j.tcs.2024.114553, source full text https://www.sciencedirect.com/science/article/pii/S0304397524001683 explicitly treats prime-ideal entropy and a specialized computational decisional reduction; its generalized leftover hash lemma uses its own auxiliary leakage distribution, not the source standalone Gram. Boudgoust et al., Hardness of M-LWE with General Distributions and Applications to Leaky Variants, PKC2026/ePrint2025/1472, full original 35pp MCP SHA256 63d6367243af89b4f495ed9a720c64f424a54221cbb71e6f82d627c8a4a417cb (VERSION_UNVERIFIED), supplies SEARCH high-rank known-covariance hardness for HNF secret+ERROR quadratic hint, not the desired low-rank DECISION result. No novelty claimed for elementary pair-collision/ideal algebra.

## Exact ideal-quotient identity [DERIVED]

Let R be ANY finite commutative ring, S in R^d with arbitrary distribution, public H=h(S), independent random A uniform R^(m x d), iid error samples E_j from a full-R distribution mu independent of S,H,A. Set Y=AS+E. Draw S,S' independently conditional on the same H and define ideal I_D generated over R by all coordinates S_i-S'_i. Denote by pi_I the quotient map R->R/I_D. Then

chi2(P_(A,H,Y) || P_(A,H) times Uniform(R^m))
 = E_(H,S,S'|H) [ ( |R/I_D| CP(pi_I mu) )^m ] - 1.

Proof: For fixed D=S-S', a uniform R-linear row A maps D UNIFORMLY onto the ideal I_D because the linear map R^d->I_D has fibers of equal size. Two independent error variables E,E' obey Pr(A D=E'-E)=CP(pi_I mu)/|I_D|. Across m independent rows the collision probability is [CP(pi_I mu)/|I_D|]^m. Multiply expected conditional output collision by |R|^m and subtract 1 to obtain the exact chi2 formula. All cross-factor dependencies are included in the quotient error CP; no assumption of independent CRT marginals.

If prime q completely splits the negacyclic ring Rq as F_q^n, for each secret pair define Z={CRT j : S_i(rho_j)=S'_i(rho_j) for EVERY i}. Then R/I_D is the field product F_q^Z, and the exact special form is

chi2 = E_(H,S,S'|H) [ (q^|Z| CP(mu_Z))^m ] - 1,

where mu_Z is the JOINT projected error distribution on Z, never the product of its one-root marginals unless independence is proved. TV<=0.5 sqrt(chi2). All formulas are information theoretic and do not prove computational indistinguishability.

## ONE executable full-ring check [EXECUTED]

Python /mnt/data/cgs51_fullring_joint_crt_collision_gate.py SHA256 0afca9954ebb012f0a362b1b15fb7d12754274ac906183e718464c3f387bdf9d.
JSON /mnt/data/cgs51_fullring_joint_crt_results.json SHA256 e792a6a1e72589cbe274e959999e4b922719e1df96234ea73371b64231d0f104.
Pure Python exact fractions, enumerated all A, full-ring outputs Y, conditional hint classes and independent secret/error samples; re-executed identically.

Toy R=F5[X]/(X^2+1), split CRT roots 2,3, rank d1, ternary coefficient secret/error (9 ring elements each), full integer Gram hint h=s*s*=s0^2+s1^2, class sizes 1,4,4. Enumerated all 25 A matrices for m1 and 625 A matrices for m2. Direct joint chi2 of (A,H,Y) against uniform equals independent CRT collision prediction, EXACT rational:
m1 direct=16/27, formula=16/27;
m2 direct=544/243, formula=544/243.
Error marginal CRT CP at EACH root=17/81, joint two-root CP=1/9, whereas marginal product=289/6561 != 1/9. Therefore naive product of single-CRT collision terms is genuinely incorrect even for iid ternary error COEFFICIENTS.

## Decisive statistical support-size obstruction [DERIVED]

For rank d, degree n, coefficientwise small secret support size b_s and independent small ERROR support size b_e (e.g. each=3), conditioned on ANY public A and H, possible Y outputs across m rows have cardinality at most b_s^(nd) b_e^(nm). The reference uniform distribution has q^(nm) outputs. The union of reachable outputs is an event accepted with probability 1 under real MLWE, while the uniform branch hits it with probability at most min(1,b_s^(nd)(b_e/q)^(nm)). Hence

TV((A,H,Y),(A,H,U(Rq^m)))
 >= 1 - min(1, b_s^(nd) (b_e/q)^(nm)).

This is an INFORMATION-THEORETIC support test and may require EXPONENTIAL time to implement. Therefore it is NOT a polynomial-time break of standard decision MLWE.

For iid ternary secret and ternary error, d2,m1,q97, bound equals TV >=1-(27/97)^n, and at n4 >=0.993997003. At n1024, log2((27/97)^n)≈-1889.306, though q97 does NOT fully split n1024 and this is just a quotient-ring support calculation, NOT a valid source-certified FHE parameter set. Unbounded discrete Gaussian error needs a high-probability truncated-support version plus tail bound; do not transplant finite ternary support theorem as-is. Large q or large n actually makes computational MLWE statistically further from uniform for fixed small secret/error supports; standard MLWE security is computational, not statistical.

## End iteration and decision

STATUS: PASS exact arbitrary finite-ring ideal-quotient noisy chi2 identity and full split toy verification; FAIL claim that such direct statistical LHL can justify decision security for full-ring low-rank tiny-support key/error at q sufficiently large. This is a proof-route falsifier, NOT insecurity of the actual source, NOT a novel cryptographic result. Parent strict CGS two-round O(LDec) remains OPEN.

RESULT: Full ring exact chi2 needs secret-pair generated ideal and joint projected error CP. One-root entropy/mixing can be misleading. With small supports, statistical closeness to uniform is information-theoretically impossible, requiring a computational reduction/real security assumption.

NEXT_ACTION HUMAN_REVIEW: Recommend PARK this sequence of entropy/CRT toy refinements. A genuinely new low-rank decision known-covariance result requires ONE explicit COMPUTATIONAL reduction with source-matched secret-only Gram leakage and public/evaluation-key distributions, not more unconditional statistical entropy estimates. PI retains final decision to authorize such proof research or pivot; don't switch unrelated targets autonomously. STATE_UPDATE YES own finding, cumulative CGS and root STATE only.