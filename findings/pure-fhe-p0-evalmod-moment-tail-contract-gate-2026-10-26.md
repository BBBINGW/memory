# PURE-FHE · P0-PRESCOUT-15 — EvalMod Moment / Tail Contract Gate

Date: 2026-10-26 Asia/Hong_Kong
TRACK_ID: PURE-FHE
PREVIOUS: P0-PRESCOUT-14
ONE PRIMARY HYPOTHESIS H15: An EvalMod error budget that retains only an error's mean/variance (or the Gaussian high moments inferred from that variance) can by itself certify a very small failure probability such as 2^-128, without validating its input-noise distribution or tail.
ONE MINIMAL DECISIVE TEST: variance-matched sparse-tail vs Gaussian distribution propagated through cubic Taylor error.
STATUS: FAIL_VARIANCE_ONLY_TAIL_CERTIFICATION; PASS_ANALYTIC_COUNTEREXAMPLE
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN

## [FACT] Sources and exact scope

1. User-supplied papers/supplied/2025-1594.pdf, physical p13 (page footer 13), §3.1 end: Ma et al., "Practical Dense-Key Bootstrapping with Subring Secret Encapsulation" (ASIACRYPT 2025), explicitly says precise L1 noise analysis of EvalMod is lacking for predicting polynomial degree and double-angle count. It does NOT say there is no error analysis of any kind. URL https://eprint.iacr.org/2025/1594 .
2. Sung, Seo, Kim, Min, "EvalRound+ Bootstrapping and its Rigorous Analysis for CKKS Scheme" ePrint 2024/1379, published IEEE Access 2025 (DOI 10.1109/ACCESS.2025.3595177). Connector mirror version unverified, SHA256 8551ce29009e0e0a9a2c54b0862b6e3db68a816fd2042b311306b7821b619e4e. Physical PDF pp16-18: Taylor-error approximation of (2π)^2/6 (pt/q + eCTS)^3; computes even Gaussian moments from coordinate variance (including sixth moment 15σ^6); states a postulate derived from empirical variance patterns and *assumes* independence of decomposed errors for variance additivity. This is useful mean-square error / parameter modeling, not independently proof of a 2^-128 whole-pipeline tail. Source: https://eprint.iacr.org/2024/1379.pdf ; PDF screenshot via web failed due cache miss, so important typography and version remain partly unverified.
3. Seo and Min, "Optimal Design of Key Switching Parameters for Efficient CKKS Bootstrapping," IEEE Access 2025, DOI 10.1109/ACCESS.2025.3610909: rigorous error accounting of key-switch parameters; abstract reports two extra levels at common settings. https://pure.ewha.ac.kr/en/publications/optimal-design-of-key-switching-parameters-for-efficient-ckks-boo/
4. Bossuat et al., "Security Guidelines for Implementing Homomorphic Encryption", Communications in Cryptology vol 1 no 4, Appendix A printed p39. The PDF screenshot was successfully inspected. Distinguishes out-of-range EvalMod failure |I(Y)|>K, gives a formula using an Irwin-Hall CDF (fixed Hamming weight), and corrections for non-fixed ternary weight. This ALREADY covers the outer-integer-range DFR under its statistical model, but does not alone cover approximate polynomial/rescale/keyswitch pipeline accuracy. https://cic.iacr.org/p/1/4/26/pdf .
5. Other current developments: 2024 EvalComp, 2025 EvalRound+, 2025 Seo-Min, 2026 LCR+AKS, and surveys. Parameter-only contributions face strong prior art. 2026 survey https://link.springer.com/article/10.1186/s42400-026-00571-w .

## [DERIVATION] Single exact counterexample

Let independent? No independence assumptions are required for this *single scalar* random variable. Define epsilon=0 with probability 1-2^-40, and epsilon=+2^-10 or -2^-10 each with probability 2^-41.
Mean=0; variance E[epsilon^2]=2^-60. Sixth moment E[epsilon^6]=2^-100.
By contrast a Gaussian G~N(0,2^-60) has E[G^6]=15*(2^-60)^3=15*2^-180.
Ratio sixth moments =2^80/15, despite equal mean and variance.
Taking pt/q=0 and Taylor map T(z)=(2π)^2/6*z^3 yields E[T(epsilon)^2] / E[T(G)^2]=2^80/15.
At threshold a=2^-11, actual P(|epsilon|>a)=2^-40, exceeding any desired 2^-128 failure budget. Variance alone gives at best generic Chebyshev bound 2^-60 / (2^-11)^2 =2^-38 (without further distribution information).
This is a counterexample to *promoting second moments alone* to an unconditional tail guarantee. It is NOT a CKKS-native distribution, a cryptanalytic attack, or evidence that EvalRound+ authors themselves promised a distribution-free 2^-128 tail guarantee.

## [DERIVATION] Distinct contracts

A. Out-of-domain bootstrap failure: |I(Y)|>K; probability explicitly modeled by standard FHE guidelines using Irwin-Hall and Hamming-weight distribution. Already existing.
B. In-domain precision failure: conditioned on |I(Y)|≤K, require a bound on CtS perturbation, polynomial/functional approximation error, rescaling and key-switching error, including dependence and possibly complex coordinates.
Variance/RMS estimates for B alone do not establish an exponentially small overall failure probability.
Union bounds and/or conditional tail estimates could establish a total certificate, but are standard probability tools, not themselves new algorithm design. Need hard evidence that sharper bounds reduce polynomial degree/double-angle iterations/RNS moduli AND survive independent native measurements at the target DFR before prioritizing.

## Decision

Do not call this an unresolved all-EvalMod-error problem; do not claim an error in EvalRound+ without its actual stochastic assumptions. Mathematical rejection applies only to the proposed variance-only universal certificate. The published appendix already addresses A. No practical improvement, no original mathematical construct, no need for Codex.

End of iteration:
STATUS: FAIL_VARIANCE_ONLY_TAIL_CERTIFICATION
RESULT: variance matched counterexample demonstrates sixth-moment and 2^-128 DFR gap; prior art already bounds integer-overflow failure.
NEXT_TEST: CONDITIONAL_IN_DOMAIN_NOISE_CONTRACT_GATE — from one concrete existing CKKS EvalMod pipeline, decide whether a proven conditional per-slot tail can save ≥1 actual level under identical precision/DFR; stop immediately if known or if benefit is only analytic.
STATE_UPDATE: YES (single isolated finding)
OTHER_TRACKS: UNCHANGED
