# EAI-SYNTH C06 — Wasserstein fidelity and downstream regression risk can rank synthetic distributions oppositely
Date: 2026-10-26 (Asia/Singapore)
TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH
Previous latest C05. This C06 is a new REAL synthetic-selection objective-interface screen, NOT another C01–C05 binary-verifier test. Original C01–C05 negatives and B11/B12 He sparse semantics PARK preserved. No Codex, training, GPU/server, model download, environment/source changes; one PI-authorized source-first mathematical derivation only. Any Codex need remains PENDING without execution/prompt.

## ONE precise technical hypothesis and ONE cheapest decisive test
[HYPOTHESIS H-C06, FALSE IN SPECIFIED HIGH-DIMENSIONAL REGIME]
Given target P and two Gaussian synthetic candidates QA,QB obeying Rezaei–Kovacevic–Locatello–Mondelli ICLR2026 assumptions (mixed real+synthetic high-dimensional min-norm linear regression, same label β, underparameterized samples n>d, trace-normalized bounded positive covariance eigenvalues), smaller W2(P,Q) **necessarily implies** smaller asymptotic target test excess risk. If true, W2 reference proximity could safely substitute direct downstream-risk selection, without additional task-aware objectives.
[ONE cheapest decisive test] Read original Rezaei ICLR2026 Theorems 4.1, 4.3 and assumptions and Qiao ICML2026 Theorem3+§4 selection (distinguish risk upper bound from risk ranking). Construct ONE high-dimensional Gaussian pair with swapped mean/covariance discrepancies; evaluate exact Gaussian W2 plus Theorem4.1 scalar fixed-point limit risk. Do not run a model or a synthetic benchmark.

## Original-source provenance [FACT]
1. Rezaei, Kovacevic, Locatello, Mondelli, 'High-dimensional Analysis of Synthetic Data Selection', ICLR2026 official full publisher PDF https://proceedings.iclr.cc/paper_files/paper/2026/file/97c5b2707228e7e3fb67e4ecc2e0e607-Paper-Conference.pdf ; original PDF pages physical p3 (assumptions and risk definitions), p4 Theorem4.1 / Proposition4.2, p5 Theorem4.3, p6 Theorem4.4/4.5 screenshot visually audited via web PDF screenshot. Theorem4.1 under mixed real+synthetic underparameterized min-norm linear regression shared conditional linear β, bounded spectrum and proportional sample sizes gives asymptotic risk equivalent to (sigma²/n) Tr[(alpha1 M^T M+alpha2 I)^(-1)] with M=Sigma_s^(1/2) Sigma_t^(-1/2), positive alpha1+alpha2=1-d/n and alpha1+(1/n) sum_k(lambda_k alpha1/(lambda_k alpha1+alpha2))=n_s/n. It does NOT depend on mean mismatch. Theorem4.3 under Tr(M^TM)=d proves any optimizer has eigenvalues all equal one, i.e., covariance match is optimal. Proposition4.2 explicitly says the mean can matter again if *only synthetic data* is used. Do NOT generalize the mean irrelevance outside model conditions (including common β and nontrivial n_t).
2. Qiao et al., 'When Sample Selection Bias Precipitates Model Collapse', ICML2026 PMLR306:101222-101268, original complete arXiv v2 https://arxiv.org/html/2606.13732v2 . §3.3 Theorem3 gives an UPPER BOUND on target risk by Wasserstein discrepancy and source filtered-data risk plus cross-Lipschitz violation error under Assumption2; §4.1 Eq18 uses dual OT potentials for reweight/prune score; §§4.3–4.4 collaborative private-silo proxies. NO claim that smaller W2 MUST strictly rank downstream risks. This C06 pair is NOT a counterexample to their theorem or a claim their exact selector picks one of these distributions in practice; it is a cross-objective non-equivalence witness under a common ideal reference.
3. Closest practical alternative is already Rezaei's ICLR2026 covariance matching with theorems and experiments (200 real + 800 synthetic/class CIFAR-10, class-selective feature covariance). Other active similar 2026 prior art includes Liu et al arXiv2607.02637 https://arxiv.org/abs/2607.02637 post-gen fidelity-diversity curation, and Yondem et al PMLR329 2026 https://proceedings.mlr.press/v329/yondem26a.html conformal reliability-aware synthetic selection. Their full theorem/proof not audited and not essential to one hypothesis. Li–Sun–Deng ICML2026 https://proceedings.mlr.press/v306/li26fp.html information-open synthetic loops, original publisher abstract verified; can't call generic 'task-relevant external signal' new.

## ONE exact source-aligned Gaussian calculation [DERIVATION]
Take any even feature dimension d→∞; target feature distribution
 P=N(mu_t,I_d), mu_t=0.3 sqrt(d) e1.
Real training n_t=d; synthetic n_s=d; total n=2d>d; common y=x^T beta+xi, iid zero-mean xi with variance sigma². These proportional sample fractions stay positive. Means have norm 0.3sqrt(d) (valid constant-radius scaling). Compare:
 QA=N(mu_A,I_d), mu_A=0.3sqrt(d) e2 (angle pi/2 vs target, valid constant nonzero angle).
 QB=N(mu_t,Sigma_B), Sigma_B=diag(1.5 repeated d/2, 0.5 repeated d/2) (means aligned, allowed angle zero as discussed in paper footnote). Covariances positive/ bounded 0.5..1.5 and trace normalized Tr Sigma_A=Tr Sigma_B=d, so Rezaei Thm4.1 and4.3 relevant. The fact the paper's source-specific technical mean-angle requirement permits cos phi=1 or <=1-delta is recorded; it does NOT justify applying to arbitrary means or model shift.

(A) Gaussian W2 squared for target covariance I:
 W2²(P,QA)=||mu_t-mu_A||²=0.18d.
 W2²(P,QB)=(d/2)[(sqrt(1.5)-1)²+(sqrt(.5)-1)²]
                =0.06814834742186339*d.
 Thus W2(P,QA)/sqrt(d)=0.4242640687119285, W2(P,QB)/sqrt(d)=0.2610523844401031. The GLOBAL W2-fidelity order prefers QB over QA.

(B) Rezaei Thm4.1 risk order. Here lambda eigenvalues of M^TM=Sigma_s and alpha1+alpha2=1-d/n=1/2, alpha1+(1/n)sum(lambda_k alpha1/(lambda_k alpha1+alpha2))=n_s/n=1/2.
 For QA lambda all1: alpha1=alpha2=1/4; risk limit R_A=(sigma²/(2d)) Tr[(.5 I)^(-1)]=sigma².
 For QB half lambda=1.5, half=.5, write a=alpha1, alpha2=.5-a; solve scalar equation
  a + (1/4)[3a/(1+a)+a/(1-a)] = 1/2.
 Unique positive solution a=0.25865202250415276, alpha2=0.24134797749584724.
 Then limiting risk R_B=(sigma²/4)[1/(.5+.5a)+1/(.5-.5a)] = sigma²/(1-a²)
           =1.0716974933365797*sigma².
 Therefore W2(P,QB)<W2(P,QA) but R_B>R_A by ~7.1697% in high-dimensional asymptotic target excess risk.
 This is a derived STRICT order reversal under source conditions. No finite-dimension measured accuracy, and no source theorem states the Gaussian pair explicitly. No runtime/Codex benchmark run.
(C) Why no contradiction: Qiao §3.3 bounds target risk above by Wp gap + filtered-data risk + violation term; bound may rank differently from exact risk. It never asserts equivalence. Rezaei §4.1 already explicitly derives covariance-dominant asymptotic risk and optimal covariance matching (published prior art), so 'use downstream-task covariance' is NOT our innovation. The example may be conceptually helpful for comparing privacy/OT fidelity to task-aware training but not a publishable cross-paper attack.

## Novelty/importance/cost decision
[NEGATIVE] H-C06 FALSE in specified high-dimensional mixed training regime; W2 proximity, even to EXACT real P without proxy error, does not induce correct downstream risk ordering. This is a source-derived objective mismatch; not a new theorem/primitive or a bug in Qiao.
[PRIOR ART KILL] Rezaei ICLR2026 Theorems4.1 and4.3 already supply the key covariance-vs-mean/risk effect AND an existing covariance-matching selection algorithm, including real experiments. Merely adding covariance term to Qiao proxy selection is an obvious composition without new proof/quality/privacy/communication or Pareto gain. Both methods target distinct metrics; optimizing both would need a truly joint task/geometry criterion with nontrivial min-cost implementation and its assumptions verified. No such new construct provided in C06.
[UNCLEAR] Whether secure multi-silo proxy OT transport + task-specific covariance could be approximated privately under realistic resource budget, with finite-sample generalization and actual downstream improvements beyond both baselines. Any candidate must survive full original source prior art and a meaningful cost/benefit bound before models.
[RECOMMENDATION] PARK the bare 'W2 vs downstream-risk ranking' as already-explained by source. Next PI continuation, if any, ONE C07 costed *composition obstruction* test: source-first determine whether privacy-safe OT proxy + target-feature covariance under matched silos can actually compute an estimator of task-aware risk without disclosing labels/feature covariances and whether published covariance matching/federated domain adaptation/DP covariance estimators already solve. Demand a true obstruction and nontrivial new element, otherwise strategic pivot. Do not launch automatically.

STATUS: FAIL_C06_WASSERSTEIN_ORDER_IMPLIES_DOWNSTREAM_RISK_ORDER
RESULT: Exact high-dimensional Gaussian construction obeying ICLR2026 Thm4.1/4.3 assumptions has W2(P,QB)<W2(P,QA) but R_B≈1.071697σ²>R_A=σ². Strongest direct prior art already proves covariance-optimal synthetic selection.
NOVELTY: FAIL for discrepancy/risk non-equivalence and covariance replacement; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: Only upon PI continuation, ONE C07 source-first precise nontrivial composition/permission/cost gate at W2 proxy vs target task risk; not another simple mean/covariance toy, no automatic code.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO carried unchanged, no C06 task, no Codex prompts/execution until explicit PI ask.
STATE_UPDATE: YES after exact GitHub findings/negative archive and root checkpoint.
