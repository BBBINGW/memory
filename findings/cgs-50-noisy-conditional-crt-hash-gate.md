# CGS-50 — Exact noisy conditional collision identity for one CRT factor

Date: 2026-10-15. Active PI-selected single CGS, last root checkpoint CGS49. One primary hypothesis plus one cheapest decisive algebraic test. Parent Okada–Takagi 2025/409 original two-round, standard Module-LWE and no O(LDec) secret-dependent Gaussian pad storage remains OPEN. NO new FHE, security attack or new leftover-hash lemma claimed.

## Primary hypothesis and falsifiable interface

H-CGS50: Can CGS49's per-CRT joint conditional collision entropy given published full secret-only Gram hint be directly turned into a meaningful MULTI-SAMPLE decision-MLWE statistical security guarantee using standard random-linear leftover hashing, without accounting for the projected MLWE error? We seek an EXACT formula that exposes whether the secret entropy or the projected error controls the joint hint+public-matrix+output distribution. A basic raw hash without error should fail for sample count m at least native module rank d, and the genuine noisy output may behave differently.

## Source and prior art [FACT]

1. Okada & Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, IACR ePrint2025/409 https://eprint.iacr.org/2025/409. Actual newer 40-page primary Research MCP PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Algorithm7 physical p29 uses secret Gram Sigma_s=sum_i Gram(s_i) to privately set fresh Gaussian pads for LDec sessions, with public/eval keys from the source mFHE, original two rounds. This iteration considers a PROPOSED modified known-covariance hint h(s), NOT the actual source's publicly leaked data.
2. Lin, Wang, Zhuang, Wang, Hardness of Entropic Module-LWE, Theoretical Computer Science 999 (2024) 114553, https://doi.org/10.1016/j.tcs.2024.114553. Actual published paper says its generalized leftover hash lemma requires adequate entropy in each CRT prime-ideal factor; its specific auxiliary leakage is a masked secret s+e and its decision reduction has additional assumptions. Our one-factor elementary identity does NOT reproduce or supersede their theorem.
3. Boudgoust et al., Hardness of M-LWE with General Distributions and Applications to Leaky Variants, PKC2026 / ePrint2025/1472 https://eprint.iacr.org/2025/1472, original 35-page Research MCP full PDF SHA256 63d6367243af89b4f495ed9a720c64f424a54221cbb71e6f82d627c8a4a417cb, VERSION_UNVERIFIED; source Theorem4.1 pp17-18 concerns SEARCH reductions from decision M-LWE/M-SIS, Appendix A high-rank HNF x*x known-covariance. NOT a direct low-rank secret-only Gram DECISION proof.
4. Exact CGS49 prior data findings/cgs-49-native-ternary-gram-crt-entropy-gate.md: n4,q97,rank d2, independent uniform ternary coefficients, FULL secret Gram h with 39 possible values; for each CRT root the joint V=(s1(rho),s2(rho)) is injective across all 6561 small keys, giving conditional collision probability CPbar(V|H)=39/6561. Projected independent ternary error e(rho) at rho33 has EXACTLY 81 equiprobable residues in F97, hence CP(mu)=1/81. This is a small algebra experiment, not original KeyGen security parameters.

## Exact one-factor noisy random-hash theorem [DERIVED]

Let H be ANY public leakage correlated with the master secret, and let V in F_q^d have an arbitrary distribution conditioned on H. Draw A independently uniformly from F_q^(m x d). Draw E=(E1,...,Em) independently of A,V,H, with each Ej independent distributed as fixed mu on F_q. Set Y=AV+E in F_q^m. Let CPbar(V|H)=sum_h P(h) sum_v P(v|h)^2 and CP(mu)=sum_e mu(e)^2. Then the EXACT chi-square divergence of the joint public transcript from uniform outputs, including leaked H, is

  chi2( (A,H,Y) || (A,H,U_m) )
     = CPbar(V|H) * ( (q*CP(mu))^m - 1 ).

Proof: draw V,V' independently conditional on H, errors E,E' independently. For V=V' (probability CP(V|h)), output collision after hashing requires E=E', probability CP(mu)^m. For V!=V', A(V-V') is uniform on F_q^m, so collision probability q^(-m), independent of E,E'. Thus E_{A|h} CP(Y|A,h)=CP(V|h)CP(mu)^m+(1-CP(V|h))/q^m. Multiply by q^m, subtract 1, and average h. Pins down exactly which randomness the LHL uses. By Cauchy-Schwarz

  TV( (A,H,Y), (A,H,U_m) )
    <= 1/2 sqrt( CPbar(V|H)*((q CP(mu))^m-1) ).

This is an upper bound, not an exact computational distinguishing advantage. It is about ONE CRT FIELD factor, with independent uniformly random A and iid additive errors; fixed-key public/eval-key correlations, original adaptive threshold transcripts and different CRT factors are NOT covered.

Boundary checks: If mu uniform F_q, CP(mu)=1/q and result chi2=0 for ANY V and hint H, as expected. If mu=pointmass at 0, result reduces to CPbar(V|H)(q^m-1); since CPbar(V|H)>=q^(-d), direct noiseless leftover hashing cannot prove negligible chi2 at m>=d. This does NOT refute genuine noisy decisional MLWE, which can rely on computational lattice hardness and specialized hybrid reductions. The number of FHE public/eval keys may exceed d; the elementary direct raw-hash method cannot simply absorb them as independent extractors.

For iid ternary error coefficients e_j and root rho mod q, let phi(u)=E_{e_j}[exp(2 pi i u e_j/q)]=(1+2cos(2 pi u/q))/3. Character orthogonality gives an independent general-n formula

  q CP(mu_rho)
     = sum_(u in Fq) prod_(j=0)^(n-1) |phi(u*rho^j)|^2.

The u=0 contribution is 1. This expression can be used for analytic bounds at general n and an ACTUAL coefficient error chi, but does not by itself give a full-ring security proof.

## ONE decisive exact test [EXECUTED]

Script /mnt/data/cgs50_noisy_conditional_hash_gate.py SHA256 6f74fd02553d0f46451477d3e9d6e4c69d286932dbbc283b68f85ac7b3300c54.
JSON /mnt/data/cgs50_noisy_conditional_hash_results.json SHA256 947ad99c38ca0b9eca907af6b878f504be083b35004e1bde0d7810e1fc606245.
Real executed Python exhaustive Fraction arithmetic, no Monte Carlo.

INDEPENDENT validation: q7,d2, V uniform over {-1,0,1}², hint H=sum_i V_i² mod7, independent projected error mu uniform {-1,0,1}. Every possible A in F7^(m x2), secret and error outcome is enumerated for m1 (49 matrices) and m2 (2401 matrices). Expected chi2 EXACTLY 4/9 for m1 and 40/27 for m2; right-side formula gives IDENTICAL exact rational values in each case.

Source-shaped n4/q97/d2 control: insert independently confirmed CGS49 CPbar(V|h)=39/6561, CP(mu)=1/81. Hence exact chi2(m)= (39/6561)*[(97/81)^m-1]. Corresponding one-factor joint-TV upper bounds: m1 0.01713305, m2 0.02539816, m5 0.04662443, m10 0.08676184, m20 0.23062186; m40 chi2≈8.0397 yields vacuous (>1) TV bound. Without additive error, m1 TV bound 0.37770, m2 chi2≈55.92 already vacuous, m3≈5425.12. These are EXACT-formula-derived chi2 and computed upper bounds, not sampled adversary advantage. The ternary error Fourier power sum independently matches q CP(mu)=97/81 to <1e-10.

A crucial joint-spectrum limitation: uniformly sample random constant polynomial E(X)=u in R_q with u uniform F_q and all other coefficients zero. EVERY separate CRT marginal E(rho) is exactly uniform F_q, but the FULL CRT vector is (u,...,u), supported on only q of q^n possibilities, hence joint TV to uniform is exactly 1-q^(1-n). At n4,q97 this is >0.9999989. This artificial noise distribution is a scope counterexample, NOT source chi; it proves no assertion about FULL decision Ring/Module-LWE may be inferred from individually uniform CRT marginals alone.

## Research verdict

PASS: exact noisy conditional collision identity under explicit assumptions, verified rational q7 exhaustive test, CGS49 q97 application and general error Fourier formula. FAIL: premise that CGS49 conditional secret entropy alone gives an unconditional multi-sample raw-hash/decision security bound; error mixing, sample count and CRT cross-correlations all matter. UNCLEAR: analytic small-secret full-ring GRAM-conditioned decision reduction under original FHE/evaluation-key distribution, security λ128, and original source O(LDec) removal. No new primitive/publishable theorem claimed; pair-collision identities are elementary/standard LHL material.

NEXT CGS51 only if PI continues: ONE full-ring correlation gate, starting from the joint character distribution of iid coefficientwise error across the n CRT factors under a public Gram hint, or a tightly scoped real reduction from standard decision-MLWE (including evaluation keys). Must NOT confuse marginal one-factor smoothing with whole ring; if no viable end-to-end proof interface, recommend PI PARK/pivot instead of accumulating toy entropy statistics. HUMAN_REVIEW.
STATE_UPDATE YES own finding, CGS cumulative archive and sole root STATE, unrelated projects untouched.