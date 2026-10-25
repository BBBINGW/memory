# EAI-SYNTH C02 negative — False positives force p^-2 certification cost in binary-only verifier oracle
Date: 2026-10-25 Asia/Singapore, ACTIVE EAI-SYNTH only, C01 completed, B11/B12 sparse counter parked. No Code/GPU/remote/model/training/Codex.

H-C02 [FALSIFIED]: With fixed known TPR s and FPR f, 0<f<s<1, IID binary-only verifier outputs can decide whether model rare-mode prevalence q is zero or at least p at fixed constant error with O(1/p) calls as for a perfect verifier.

Source-first evidence (not a new lower-bound theorem): Rogan & Gladen, American Journal of Epidemiology 1978 107(1):71-76 https://pubmed.ncbi.nlm.nih.gov/623091/ (prevalence sensitivity/specificity adjustment); Fernandes Vaz, Izbicki, Stern JMLR2019 https://www.jmlr.org/papers/v20/18-456.html (quantification risk lower bound and approx minimax estimators, publisher abstract); Micheli et al Machine Learning 2025 https://link.springer.com/article/10.1007/s10994-025-06915-w Appendix A Eq(A2) (ACC formula); Yi et al ICLR2026 https://proceedings.iclr.cc/paper_files/paper/2026/hash/29806b2e4dcb35e42abed21d43e2b7d8-Abstract-Conference.html (fallible verifier long-term bias); Qiao et al ICML2026 full https://arxiv.org/html/2606.13732v2 (siloed verification/selection tail bias); Li–Sun–Deng ICML2026 https://proceedings.mlr.press/v306/li26fp.html (information-open synthetic pipeline). Only the first three are DIRECT classic prior art for this binary prevalence calculation; no claim any paper explicitly states these constants.

ONE exact two-world derivation: H0:q=0 gives Y~Bern(f); H1:q=p gives Y~Bern(f+(s-f)p). For n IID verifier bits, KL(P1^n||P0^n)<=n(s-f)^2p²/[f(1-f)]. If both testing errors <=beta<.5, TV>=1-2beta, Pinsker yields n>=2 f(1-f)(1-2beta)^2 / [(s-f)^2p²]. At fixed 0<f<s<1, beta fixed, this is Omega(p^-2). Perfect f=0,s=1: choose n>=ln(beta)/ln(1-p)=Theta(p^-1 log(1/beta)) to see >=one positive with probability >=1-beta under H1. An ACC calibrated estimator based on sample mean Ybar corrects qhat=(Ybar-f)/(s-f), with standard Hoeffding O(p^-2 log1/beta) calls to distinguish; matching sample complexity is already known.
Numeric p=.001 f=.05 s=.90 beta=.05 => a1=.05085, necessary Pinsker n>=106506; Bernoulli KL≈7.564779448e-6 also allows stronger standard BH bound n>=212755, while perfect verifier n=2995 is sufficient under H1. Only binary outputs / stationary known error rates / IID candidates; not general multimodal generator impossibility, not a DP lower bound, not training fidelity theorem.

STATUS: FAIL_C02_PERFECT_ORACLE_RATE_WITH_FIXED_FALSE_POSITIVES.
RESULT: False-positive floor creates classic p^-2 binary hypothesis-testing burden; statistical quantification literature already covers correction/minimax issues.
NOVELTY: FAIL for this scope; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: Only on PI continuation, one mechanism-specific strong-prior-art C03 gate on structured verification / calibration under explicit costs; don't repeat nearby confusion-matrix toy checks.
PENDING_CODEX: carry OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO unexecuted; none newly required C02.
STATE_UPDATE: YES after readback and STATE checkpoint.
