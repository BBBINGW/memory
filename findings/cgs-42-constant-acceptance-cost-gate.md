# CGS-42: Constant negacyclic Gaussian rejection acceptance and fixed MPC costs

2026-10-15. Single PI-selected CGS track, CGS-41 latest before this round. This research iteration has ONE primary hypothesis and ONE minimal decisive spectral-bound plus public fixed-trial arithmetic check. Original low-round ThFHE O(LDec) Gaussian setup challenge still OPEN.

## Hypothesis and tested condition

H-CGS42: Does secure fixed-trial rejection require O(Bpub*kappa) proposals due to the coarse CGS41 lower bound alpha>1/Bpub, or does the exact SOURCE negacyclic coefficient bound imply a much better, dimension-INDEPENDENT acceptance probability? Test a spectral upper bound for every legal bounded secret and compute the public fixed trial count and optimistic MPC online work at kappa128, n1024, rank k2. This is a mathematical proposal-cost gate, NOT an MPC construction/security proof.

## Original facts and citation provenance

Okada & Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, IACR ePrint 2025/409, https://eprint.iacr.org/2025/409. Original newer 40-physical-page Research MCP PDF, SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Definition3.1 physical p12 defines R=Z[X]/(X^n+1) for n a POWER OF TWO, and Gram(s)=mat(s)mat(s)^T. Bmlwe-bounded means Pr_{X~chi}[|X|>=Bmlwe]=negl(kappa), NOT unconditional |X|<Bmlwe. Thus proof conditions apply on all coefficients within bound, an event of overwhelming probability when kn is polynomial. Algorithm7 physical p29 wants the correlated integer Gaussian D_(Z^n,sigma0 sqrt(Bpub² I−Sigma_s)). Lemma7.1 p30 assumes additional singular-value/noise/smoothing restrictions not fully instantiated here, and Bpub²>k*n²*Bmlwe²+1. Source original two online rounds are explicitly relaxed in this interactive MPC candidate.

CGS41 proved exact PRIVATE spherical proposal rejection: proposal Z from D_(Z^n,sigma0*Bpub), accept with exp(-pi Z^T(C^-1−Bpub^-2 I)Z/sigma0²), C=Bpub²I−Sigma_s. Accepted target law is EXACTLY the source integer discrete Gaussian. Poisson summation bounds acceptance alpha>=sqrt(det(I−Sigma_s/Bpub²))/(1+epsQ), epsQ positive spherical Gaussian dual theta correction, independently of hidden target normalizer. Rejection sampling itself is classical (see Sage integer/lattice Gaussian documentation), no new primitive novelty claimed.

## NEW restricted spectral lemma and constant acceptance bound [DERIVED]

For even n>=2 and any root omega of X^n+1, omega^n=-1 and omega² !=1. For any REAL coefficients |s_j|<=B, using |z|=max_phi Re(e^(-i phi) z),

|s(omega)| <= B max_phi sum_j |cos(j arg omega−phi)|
            <= B sqrt(n sum_j cos²(j arg omega−phi))
            = B n/sqrt(2).

The equality is exact because sum_j omega^(2j)=0, so sum_j cos²(...)=n/2 for all phi. Negacyclic convolution matrix mat(s) is unitarily diagonalized by the roots; Gram eigenvalues are |s(omega)|². Therefore for module k:

lambda_max(Sigma_s) <= k*n²*B²/2;
tr(Sigma_s)=n sum_i ||s_i||² <= k*n²*B².

Let beta=k*n²*B²/Bpub²<1, A=Sigma_s/Bpub². Then all eigenvalues of A lie in [0,beta/2]. Since log(1−x)>=−x/(1−beta/2) on this interval,

log sqrt(det(I−A)) >= −tr(A)/(2(1−beta/2)) >= −beta/(2−beta) > −1.

Thus the exact discrete rejection sampler has UNIFORM acceptance

alpha >= exp(−beta/(2−beta))/(1+epsQ) > exp(−1)/(1+epsQ).

This constant lower bound is conditional on the original source coefficient bound, n a power of two and smoothing sufficient to bound epsQ. It fails as a universal statement for odd n with omega=−1. The proof is elementary Fourier and determinant inequalities and NOT a new hardness result or source paper attack.

## ONE n1024 public fixed-trial cost gate [EXECUTED]

Public demonstrator: kappa128, ring n1024, module rank k2, Bmlwe=2, Bpub=2897, sigma0=4, permitted sessions LDec=2^20. With source strict B-bounded definition, ternary or signed-unit secret distributions have Pr[|coefficient|>=2]=0 (whereas B=1 would NOT satisfy the paper definition for a +/-1 secret). Bpub²=8,392,609 exceeds k*n²*Bmlwe²+1=8,388,609. Other original source sigma0 smoothing, mFHE KeyGen/Eval hardness, q/Q correctness and per-key min singular-value assumptions have NOT been validated. Spherical proposal width=11588 makes epsQ<2^-128 by elementary theta upper bound.

Numerics: beta=0.999523271011434; max normalized eigenvalue rho<=beta/2=0.499761635505718. Old CGS41 coarse alpha lower=0.0003451846738; new universal lower exp(-1)/(1+epsQ)=0.36787944117; beta-specific alpha>=0.36823019873. For all LDec calls to fail with total probability <=2^-128, hide per-call rejection timings by always processing J public candidate slots and privately selecting FIRST accepted sample. Set J=ceil[(128 ln 2+ln LDec)/(-ln(1−alpha_min))]. Coarse old J=297140; new UNIFORM J=224 (about 1326x smaller), with log2 union failure <=-128.22715. Fixing the budget is necessary to avoid leaking key-dependent stopping time; it is not sufficient for real MPC security or correct finite precision.

Full ternary coefficient enumeration n2,n4,n8 verified max |s(omega)|/(n B) <=1/sqrt2, as a sanity test; the proof is general. At n1024,k2,Bpub2897, one randomly selected iid sign secret gave smooth determinant acceptance 0.882529, one iid ternary 0.919473, and all-ones 0.877640. Such acceptance rates are not source-certified FHE security instances; smoothing theta correction is tiny at the illustrative width.

## Online vs original storage comparison [ILLUSTRATIVE MODEL, not implementation]

Each decryption requires J*n=229,376 PRIVATE integer Gaussian coordinate proposals. A direct dense secret quadratic form costs O(J n²) ~234,881,024 private product TERMS, potentially huge. Negacyclic Fourier diagonalization suggests an UNIMPLEMENTED optimistic O(n) PRIVATE multiplications plus O(n log n) public linear FFT operations per candidate IF secret spectral weights are computed and privately pre-shared during KeyGen and correctly handled with secure fixed-point/complex arithmetic. That is not a proven exact gate count, privacy composition or malicious MPC.

Counting just TWO publicly opened field values per multiplication under an illustrative Beaver-style multiplication protocol and assuming exactly n private multiplications per candidate, for 64/128-bit field elements:

Original per-party pre-stored LDec*n coefficients = 8/16 GiB.
Optimistic online opened values PER decryption = 3.5/7.0 MiB, before ALL other MPC costs.
Dense n² product terms PER decryption = 3.5/7.0 GiB of opened values.
Over LDec=2^20 calls, even the optimistic model sums 3.5/7 TiB communicated per party versus the original 8/16 GiB pre-stored across all calls. This compares DISTINCT resources: storage vs traffic. No field bitlength is sourced from actual secure q, and the model is not a measured lower bound. It excludes MPC preprocessing triples, malicious authentication, distribution of private proposals, secret acceptance arithmetic, exponential/compare, private first-accepted selection and dropout/adaptive transcript.

## Reproducibility

Executed /mnt/data/cgs42_constant_acceptance_fixed_budget_gate.py, SHA256 c1c26897e6cb9c4316bd423a82cfbf192c63a0b9504fb75a27c69b7156bebdf4, and /mnt/data/cgs42_constant_acceptance_fixed_budget_results.json, SHA256 2ecdd9e9bd580845d15ba9cf2b2c4630d748dec6dfcc4a35114f35c618db4670. Python big integers for sizes and math for logs, NumPy FFT spectrum for toy checks; NO FHE/OT/MPC implementation or 128-bit hardness estimator.

## End of iteration

STATUS PASS exact negacyclic spectral gap, new uniform constant acceptance and n1024 fixed-budget arithmetic. UNCLEAR practical online MPC, adaptive simulation, source security and scientific novelty; original O(LDec) two-round problem OPEN. Do not call this a solution to original paper's open question.

RESULT: The cost obstacle is NOT an unavoidable polynomially tiny per-proposal acceptance under the source negacyclic/small-secret regime; worst-case oblivious budget at kappa128,n1024 can be 224 trials, not 297140. However hundreds of PRIVATE dimension-1024 quadratic tests per decryption plausibly impose large network cost even with FFT, and source low-round original requirement is not maintained.

NEXT CGS-43 (only on PI next "继续"): ONE specific secure negacyclic frequency-domain quadratic form circuit gate. Determine correct exact algebra/finite fixed-point encoding, true count of secret multiplications, effect of evaluation-key/MLWE q precision, secure preprocessing, and active-set output conditions. If cost kills the scheme, PARK interactive Gaussian MPC and suggest PI pivot. One primary hypothesis and one cheapest falsifier.

STATE_UPDATE YES own finding, CGS main archive and sole root authoritative checkpoint only.