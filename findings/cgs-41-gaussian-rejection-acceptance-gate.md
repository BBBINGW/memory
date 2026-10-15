# CGS-41 — Spherical discrete-Gaussian rejection has inverse-polynomial acceptance under source Bpub bound

Date: 2026-10-15. Single active PI-selected CGS target, previous CGS-40. ONE primary hypothesis and ONE decisive exact acceptance-probability bound with a numerical sanity check. Original Okada–Takagi ePrint2025/409 O(LDec) on-demand Gaussian pad challenge remains OPEN.

## H-CGS41 [PASS mathematical acceptance gate, not ThFHE feasibility]

Given source MLWE secret covariance Sigma_s=sum_i Gram(s_i), target pad is D_(Z^n,sigma0 sqrt(C)) where C=Bpub² I−Sigma_s. The proposal is PUBLICLY PARAMETERIZED spherical integer Gaussian Q=D_(Z^n,sigma0 Bpub I), but all candidate samples, random acceptance coins, accepted output and intermediate accept bits MUST remain PRIVATE within a hypothetical secure MPC. Check whether exact rejection sampling has exponentially small success as dimension n increases, or whether the ORIGINAL source's unusual Bpub safety margin yields polynomial acceptance.

## Source [FACT]

Original Hiroki Okada/Tsuyoshi Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, IACR ePrint2025/409 https://eprint.iacr.org/2025/409. Full newer cached 40-physical-page PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Algorithm7 physical p29 requires INTEGER correlated lattice Gaussian conditioned on Sigma_s, Shamir pre-shared per sid. Lemma7.1 physical p30 requires coefficientwise |s_ij|<=B_mlwe and Bpub²>k n² B_mlwe²+1 (read also proof physical p31 positive diagonal dominance); also imposes additional min-singular-value, smoothing and noise assumptions NOT checked by this acceptance-only candidate. Original Server should not learn Sigma or raw zeta. Source has original TWO online broadcast phases; this proposal RELAXES ONLINE MPC interaction and does not preserve that property.

Prior art: rejection sampling for integer lattice Gaussians is standard, e.g. Sage integer sampler docs https://doc-gitlab.sagemath.org/html/en/reference/stats/sage/stats/distributions/discrete_gaussian_integer.html and lattice sampler docs https://passagemath.org/docs/latest/html/en/reference/stats/sage/stats/distributions/discrete_gaussian_lattice.html. No new primitive, nor novelty claim for elementary envelope construction.

## Correct target law: exact DISCRETE mass identity [DERIVATION]

Work over actual integer Z^n, not continuous Gaussian. Let Qwidth=sigma0 Bpub I; target width Twidth=sigma0 sqrt(C). Since Sigma_s PSD and C=Bpub²I−Sigma_s is positive definite, C<=Bpub² I and the matrix
M=C^-1−Bpub^-2 I is PSD.
Draw private X from spherical discrete Gaussian Q with probability proportional to exp(−pi||x||²/(sigma0²Bpub²)). Privately ACCEPT with probability
 a_s(x)=exp(−pi x^T M x /sigma0²), in (0,1].
Then proposal mass times acceptance is proportional to exp(−pi x^T C^-1 x /sigma0²), EXACTLY the original D_(Z^n,sigma0 sqrt(C)) mass at every integer x. Hence the acceptance-conditioned output has the exact target lattice Gaussian law. Only real-arithmetic mathematical functionality established: secure finite-precision MPC Bernoulli, inversion and rounding require new analysis.

Acceptance probability
 alpha_s=Z_Zn(sigma0 sqrt(C)) / Z_Zn(sigma0 Bpub I),
where Z is lattice Gaussian partition sum, since the unnormalized mass ratio was chosen with proposal at 0 equal target at 0.

## Source-anchored inverse-polynomial LOWER BOUND [DERIVATION]

Define theta(A)=sum_(w in Z^n) exp(−pi w^T A w), A SPD. Poisson summation gives
 Z_Zn(sigma0 sqrt(C))=sigma0^n sqrt(det C) theta(sigma0² C),
 Z_Zn(sigma0 Bpub I)=(sigma0 Bpub)^n theta(sigma0² Bpub² I).

Write eps_Q=theta(sigma0² Bpub² I)−1≥0, typically negligible when the source's smoothing-scale conditions hold. Since theta(sigma0² C)>=1,
 alpha_s >= sqrt(det C)/Bpub^n / (1+eps_Q)
          = sqrt(det(I−Sigma_s/Bpub²))/(1+eps_Q).

If gamma_j are nonnegative eigenvalues of Sigma_s, each <=tr Sigma_s <Bpub², then for t_j=gamma_j/Bpub²∈[0,1),
 product_j(1−t_j) >=1−sum_j t_j.
This elementary inequality yields
 alpha_s >= sqrt(1−tr(Sigma_s)/Bpub²)/(1+eps_Q).

Since each ring multiplication matrix mat(s_i) has n columns, all same squared coefficient norm, tr(Sigma_s)=n sum_i ||s_i||² <=k n² B_mlwe². Therefore
 alpha_s >= sqrt(1−k n² B_mlwe²/Bpub²)/(1+eps_Q)
           > 1/[Bpub(1+eps_Q)],
using Bpub²>k n² B_mlwe²+1. This is polynomially bounded expected number of rejection proposals whenever Bpub is polynomial in κ and eps_Q is bounded (as in a smoothed source parameter family). In particular the accepted distribution is the exact discrete one, not continuous approximation or linear pushforward as in failed CGS36–38.

To hide secret-dependent acceptance timing in an ACTUAL MPC, one option is a FIXED public trial budget J >= (1/alpha_min)(κ ln2 + ln LDec + safety margin), and privately select the first accepted proposal while hiding all intermediate accept flags. The no-accept failure probability is at most exp(−J alpha_min), and total across LDec sessions can be made negligible. This is polynomial but may be extremely costly. J, finite-precision correctness and private MPC protocol MUST be independently verified; the bound does not automatically prove source adaptive transcript security.

## ONE executable numerical check [EXECUTED]

Python /mnt/data/cgs41_secret_covariance_rejection_gate.py, SHA256 5a3544f0ce6a3a1f36ff467fd1158703fd090794051caf3f4a38870a79859aa4.
JSON /mnt/data/cgs41_secret_covariance_rejection_results.json, SHA256 8d6514aa9690bab8123a97a4d75671eef42be201295afde15e7b76df2522a294.
Toy: negacyclic ring n=8, k=2, coefficient bound B=1, s1=1+X, s2=1, public Bpub=12, sigma0=4. Actual source displayed bound holds Bpub²=144>k n² B²+1=129. Gram trace=24, C min eigenvalue≈139.152. Infinite-Gaussian acceptance is exact theta ratio; the smooth continuous determinant term is 0.919049909975703 and rigorous trace lower bound is 0.912870929175277; more conservative source-bound-only lower bound is 1/3. Proposal dual-theta correction eps_Q has log10 upper bound below -3142, target dual correction also tiny since sigma0²*lambda_min(C)>2200.

Exactly 120000 independent draws from truncated-per-coordinate D_Z,48 PMF (rigorous union bound for proposal coordinate truncation <3.935e-35) and independent acceptance uniforms; observed success 0.9192583333, standard error 0.00078646, consistent with determinant ratio. Empirical accepted target second-moment diagonals within 1.1% of expected smooth Gaussian value; this is a sanity check, NOT exact security/performance evidence. Python numpy RNG NOT MPC/cryptographic. No q/OT/FHE implementation, no full source noise smoothing or hardness verification.

## Limitations and novelty judgment

PASS acceptance probability and EXACT discrete target mass formula in mathematical ideal functionality; this is a narrow but constructive surprise compared with an expected exponential rejection overhead. Source's conservative Bpub margin is essential. It does NOT prove the full MLWE construction is efficient or secure:
- The covariance Sigma_s and inverse C^-1 must be computed from hidden key shares inside secure MPC or prepared as PRIVATE shared key setup with correct finite precision; full normalizer never needs to be computed for acceptance.
- All private Gaussian proposals and Bernoulli acceptance coins, including rejection timing, must remain private. Public proposal/transcript dependence can leak Sigma_s; Server gets neither.
- For a publicly fixed trial budget the worst-case alpha_min≈1/Bpub can force J=Omega(Bpub κ) proposal candidates PER session; each includes O(n²) generic private quadratic form and nonlinear exponential/compare. q and MPC field precision, ring FHE security, authentic malicious 2PC/MPC, dropout T-of-N, adaptive Algorithm5 transcript and no added setup per session are unproved.
- Source KeyGen has a trusted dealer and each secret Gram has negacyclic structure, potentially enabling O(n) shared covariance descriptor rather than O(n²) generic matrix; efficient secure inverse/circuit still unproved. The source covariance and original Lemma7.1 other conditions do not follow from positivity alone.
- Literature already has rejection techniques. One full end-to-end implementation/overhead gain and a genuinely different insight would be needed for publication. This scheme EXPLICITLY sacrifices the source's original two-round online requirement.

END ITERATION: CGS-41.
STATUS: PASS exact mass identity and source-uniform inverse-poly acceptance bound, toy verified; UNCLEAR/human-review actual MPC security/communication and scientific novelty, original O(LDec) low-round standard-MLWE problem OPEN.
NEXT CGS-42 (ONLY on PI next "继续"): one decisive full online COST/FIXED-TRIAL gate at κ128, n=1024 or larger with source Bpub, σ0, acceptable LDec; evaluate realistic number of private quadratic-form checks to hide rejection timing, secure fixed-point precision, and whether any practical win survives versus O(LDec) pad storage. If generic bound requires too much, test ONE justified tighter key distribution acceptance bound, not vague optimism. If cost infeasible, PARK interactive rejection sampler and request PI direction/constraint relaxation. STATE_UPDATE YES own finding and single active repo checkpoint, no other workstreams.