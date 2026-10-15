# CGS-36 — Public Gaussian seed + static Shamir-shared covariance factor: interpolation passes, discrete Gaussian law fails

**Date:** 2026-10-15. **Single active PI-selected FHE task:** CGS; prior checkpoint CGS-35. Under research agent's one-primary-hypothesis/one-cheapest-decisive-test rule. Do NOT revive or rewrite retired track isolation; no non-CGS research files modified.

## Primary falsifiable hypothesis (H-CGS36)

**H-CGS36 [FAIL at exact source-discrete-distribution interface]:** Trusted KeyGen can compute a secret-conditioned factor L_s satisfying L_s L_s^T = C_s := Bpub² I−Sigma_s, Shamir-share the factor ONCE to N threshold parties using a T-out-of-N scheme and store fixed-size long-term shares L_i. For every sid, all parties derive ONE common **PUBLIC** independent centered base Gaussian random vector g_sid from public sid/PRG, each computes its **local linear padding share** zeta_i^(sid):=L_i g_sid. Any authorized set combines zeta_i to an on-demand source-distributed Gaussian zeta with secret-dependent covariance C_s, without extra rounds, Server seeing Sigma_s or raw zeta, or storing O(LDec) per-session shares. Crucially, H claims this **direct integer-linear transform of integer discrete Gaussian** produces the actual discrete Gaussian D_(Z^n, sigma0 sqrt(C_s)) of source Algorithm7, not just a covariance-matched continuous Gaussian.

**ONE CHEAP DECISIVE TEST:** First grant an unusually favorable case where the scalar matrix factor L_s is the EXACT INTEGER 2 (no square-root quantization problem). Let common public g <- D_(Z,sigma0=2). Check mathematically whether reconstructed zeta = 2g has source-required distribution D_(Z,4) (since C_s=4). This is independent of Shamir privacy, actual FHE, and PRSS quality. If a simple parity test has non-negligible advantage, the named sampler is incorrect even before transcript security or efficiency testing. Separately sanity-check T2,N3 interpolation for every qualified set, to show that the obstruction is DISTRIBUTIONAL, not polynomial interpolation.

## Original full paper and actual source interface [FACT]

- **Okada and Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409. Original 40-physical-page cached MCP full PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED (p5 printed Ver.4 March 26 2026). **Algorithm7 physical p29** precomputes and shares zeta^(sid) <- R(D_(Z^n,sigma0 sqrt(Bpub² I−Sigma_s))), Sigma_s=sum_i Gram(s_i), for ALL planned sid. **PartDec** p29 returns lambda_i(a^T s_i + zeta_i^(sid)) + PRF(seed_i,sid). **Algorithm5 physical p23** exposes (ctdec, all active pdi) for adaptive ODec. **§5 p25** keeps semi-honest noncolluding Server untrusted and absent FHE key-dependent covariance from its view. Thus on-demand padding is a genuine source interface target.
- Shamir secret sharing: public linear multiplication preserves degree-(T−1) share polynomial and qualified-set interpolation, but local multiplication of TWO secret-shared values increases degree to 2(T−1) (standard MPC degree-reduction obstacle). Accessible supporting literature: *Scalable Multiparty Computation from Non-linear Secret Sharing*, ePrint 2025/1007, https://eprint.iacr.org/2025/1007, discussing local Shamir multiplication degree growth, and *Introduction to secret sharing based secure multiparty computation in health data*, PMC13182292, https://pmc.ncbi.nlm.nih.gov/articles/PMC13182292, describing degree reduction's additional online communication. These are background/prior art, NOT claims of a new MPC theorem. Prior CGS-21 already falsified LOCAL nonlinear rounding of Shamir shares, so that fix should not be re-proposed without a genuinely different primitive.
- CGS-35 established that giving the original untrusted Server a local sampler of secret-dependent raw Gaussian pads leaks secret-covariance statistics under appropriate multiple samples; this candidate intends not to give Server either the factor L_s or the Gaussian zeta.

## The positive algebraic result [DERIVED]

Assume a field/ring in which a matrix factor L_s is REPRESENTABLE, and a trusted setup Shamir-shares each entry: L_i=P(i), where P(X) is a random matrix-valued polynomial of degree at most T−1 and P(0)=L_s. For a PUBLIC vector g_sid shared consistently by all parties, each party locally computes zeta_i=L_i g_sid. The polynomial Q_sid(X)=P(X)g_sid has the SAME degree bound, and any active set |act|>=T reconstructs
\`\`\`
sum_(i in act) lambda_(act,i) zeta_i
  = (sum_i lambda_i L_i)g_sid
  = L_s g_sid.
\`\`\`
This preserves all-subset threshold consistency, one local PartDec per party and no extra interactive degree reduction. It is a REAL advantage of applying a **public** multiplier; it is NOT enough to prove the discrete Gaussian output law, privacy of public g, or proper source-ring factor representation. In general square roots have noninteger entries, so additionally need a finite-field quantization scheme; the one-dimensional positive integer example BELOW gives the candidate the BEST possible case.

## Decisive exact discrete Gaussian support theorem [DERIVED; standard elementary math]

Define D_(Z,sigma) by \`Pr[G=j] = exp(−pi j²/sigma²) / Z(sigma)\`, with theta series \`Z(sigma)=sum_(j∈Z)exp(−pi j²/sigma²)\`. For any integer d>=2, if G~D_(Z,sigma) and Zeta=dG then **Zeta lives on sublattice dZ**, whereas the desired discrete Gaussian D_(Z,d sigma) has POSITIVE mass on every integer.

For z=dj, \`Pr[dG=dj]=exp(−pi j²/sigma²)/Z(sigma)\`, while \`Pr[D_(Z,d sigma)=dj]=exp(−pi j²/sigma²)/Z(d sigma)\`. Thus the two measures are proportional on dZ, with Pr[dG=dj] > Pr[D_target=dj] because Z(d sigma)>Z(sigma). Consequently the EXACT statistical distance is
\`\`\`
TV(d D_(Z,sigma), D_(Z,d sigma))
  = Pr[Y <- D_(Z,d sigma): Y not in dZ].
\`\`\`
For d=2 and sigma=2, the ODD parity event distinguishes with probability 0 in the proposed output versus
\`\`\`
Pr_{Y <- D_(Z,4)}[Y odd] = 0.499996512657643791...,
TV = 0.499996512657643791... .
\`\`\`
This is effectively MAXIMAL failure, not negligible. The mismatch persists with sufficiently large odd modulus q when viewing centered integer representatives, except negligible discrete-Gaussian wrap probability; source first samples zeta on **integer lattice** and only then embeds it in R_q. The test does not require the candidate to satisfy every source parameter inequality: a universal "linear discrete Gaussian square-root sampler" must work even in this trivial favorable one-dimensional factor case. Wider d or n-dimensional non-unimodular integer L creates analogous image-sublattice support.

Importantly, a CONTINUOUS standard Gaussian g~N(0,sigma²/(2pi) I) does satisfy L_s g~N(0,sigma² C_s/(2pi)) for continuous covariance. The two worlds cannot be conflated. Converting continuous output to an integer needs randomized rounding or rejection; applied LOCAL to Shamir shares, a nonlinear mapping generally breaks the same low-degree reconstruction (CGS-21), or requires genuine correlated randomness/interactive MPC. Choosing a secret-dependent base lattice for g would also defeat its alleged public, universally samplable character.

## Another unproved but necessary privacy interface [DERIVED; NOT part of the decisive test]

Since g_sid is PUBLIC, even in the relaxed **continuous** Gaussian output model and with a visible UNWRAPPED aggregate decryption-noise residual Y_sid = E_sid + L_s g_sid, where E is independent centered noise, the joint law obeys
\`\`\`
Cov(g_sid, Y_sid) = Cov(g_sid) L_s^T
\`\`\`
(or Cov(Y,g)=L Cov(g)), even though Y alone may have an appropriate Gaussian marginal. Conditional on exposed public g, the distribution depends on hidden L_s. Over polynomially many sessions in a suitable smooth/no-wrap setting, the public cross-correlation is estimable. The original Algorithm5 exposes all PartDec replies and known OEnc plaintexts, so such a leakage path needs an exact transcript/security proof before calling it private. This is **not a formal attack** on the actual discrete-rounded/mod-q source, and the present iteration does not count it as an extra primary test. It highlights a DIFFERENT obstruction from CGS-35's server-local raw Gaussian samples: now the adversary might know PUBLIC g, not zeta.

If instead the PRSS base randomness g were SECRET-SHARED with per-party Shamir shares g_i, merely setting output zeta_i=L_i g_i makes Q_sid(X)=P_L(X) P_g(X) of degree **2(T−1)**, so only 2T−1 shares generally reconstruct its product; the original source requires ANY T-of-N active set. Standard degree reduction involves communication or additional correlated preprocessing (which must be counted against O(LDec) storage and rounds). This is standard background, not a global impossibility theorem for sophisticated FSS/PCF/noninteractive MPC.

## ONE exact executed minimal experiment [EXECUTED]

Script \`/mnt/data/cgs36_public_gaussian_linear_shamir_gate.py\`, SHA256 **56012b39d223ac5f51d461ff6b73a832e4bb299458f24c1e5ab1c6ba8dbf69e8**; result JSON \`/mnt/data/cgs36_public_gaussian_linear_shamir_results.json\`, SHA256 **dae9a8b97ae619c6c8436e202bd6891629302a48655cd1fa3283c0a49b20eb5a**.

- Shamir toy: T=2,N=3, prime q=65537, favorable integer scalar factor L=2. Independently random degree-1 polynomial P(x)=2+rx modq, shares P(1),P(2),P(3). Checked ALL active subsets of sizes 2 and 3: (1,2),(1,3),(2,3),(1,2,3) interpolate L exactly. Checked for 100 integer toy nonce values g that local output shares P(i)g recombine to Lg modq for all four sets. All PASS; seed from Python random.Random is for reproducibility ONLY.
- EXACT source-style Gaussian pmfs evaluated with arbitrary-precision mpmath (80-digit): base D_Z,2 versus target D_Z,4 and transformed 2D_Z,2. Computed both parity-event lower bound and full TV over integer grid [-100,100]:
\`\`\`
Pr_target(odd)  = 0.499996512657643791...
TV_exact(grid) = 0.499996512657643791...
\`\`\`
Gaussian omitted tail mass upper bound <2.342e−855 under stated normalization bound, so finite-grid approximation is immaterial. The formula already gives exact TV equality without numeric computation.
- No real Gaussian code or underlying FHE library was run; no secure randomness or actual (Module-)LWE parameter instantiation was claimed.

## Scientific interpretation and status

**PASS:** static Shamir-shared linear factor gives constant-memory-per-KeyGen (not per sid) input-dependent on-demand linear output, threshold consistency for ALL active sets, zero extra online rounds in a field toy.

**FAIL:** integer Gaussian scalar-factor approach gives the exact source-required discrete Gaussian law; distance ≈0.5 at tiny favorable parameters. Thus the identified direct construction is not a viable replacement of stored source zeta even BEFORE hardness/simulation-security/cost questions.

**UNKNOWN:** Whether a fully-fledged distributed conditional discrete Gaussian sampler using private Shamir-shared correlated randomness, interaction-free FSS, specially structured lattices, or end-to-end approximate sampling can meet the full original adaptive simulation and efficiency constraints. A public g also creates potential joint leakage despite correct **continuous** Gaussian marginal. KeyGen factor could take O(n²) field elements per party unless ring/circulant/FFT compression is proven, versus original O(LDec n) session pads; this is not necessarily an improvement at moderate LDec. No new primitive or attack on the original source is claimed.

**END ITERATION: CGS-36.**
- STATUS: **FAIL** exact discrete-Gaussian sampling by public integer-Gaussian linear factor; **PASS** Shamir interpolation and exact TV counterexample; **HUMAN_REVIEW** parent CGS open.
- RESULT: For d=2, G~D_Z,2, dG occupies even sublattice; source target D_Z,4 assigns nearly half its probability to odd integers, exact TV ~0.4999965. Shamir reconstruction is not the bottleneck.
- NEXT_TEST (only with PI next "继续"): **CGS-37** choose ONE concrete proposal to fix **discrete Gaussian support** while preserving threshold consistency, e.g. public dither + shared rounding/rejection with a named noninteractive MPC/PCF primitive; FIRST check public randomness leakage and Shamir nonlinear-degree / communication. If no actual mechanism with source-sized setup and no new online rounds, recommend PI pivot or a careful tradeoff with original guarantee; do NOT cycle back to prior CGS21 naive local rounding.
- STATE_UPDATE: YES. Own finding, topic current checkpoint, root single active STATE; no unrelated files.
