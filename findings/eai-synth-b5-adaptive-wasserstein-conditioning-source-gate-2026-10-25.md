# EAI-SYNTH B5 — Feedback-adaptive data and the fixed-stream Wasserstein expectation bound
Date: 2026-10-25 (Asia/Singapore)
TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH
LATEST_PREVIOUS=SYNTH-B4. No EAI-SYS, FHE, GPU, Codex, training or source modifications.

## Single primary hypothesis
[HYPOTHESIS H-B5; falsified]
For a causal feedback-selected two-round binary stream, the accuracy bound for a fixed input stream may ALWAYS be conditioned on the realized input stream with the same error constant, without further assumptions. Therefore fixed-data expectation estimates for the subregion sparse counter in He et al. §4.2 Eq.(4.4) may be transferred to adaptive streams merely by conditioning on the realized stream.

Falsification condition: give one explicit feedback-chosen binary input whose value reveals an unusually large previous release noise, making E[|old noise| | realized input] exceed its unconditional fixed-input bound. ONE minimal two-round construction, NOT a simulation or an attack on He.

## Original-source anchors [FACT]
1. He, Vershynin and Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv 2402.08012v3, 2024-10-23. Full PDF https://arxiv.org/pdf/2402.08012 (original PDF page numbers printed pp.7–8 Algorithm 1–3; p.9 Lemma3.4; p.12 Lemma4.2; p.13 Eq.(4.4)–(4.6); p.20 Appendix A proof of Lemma3.2; p.21 conclusion of proof). Original full HTML https://arxiv.org/html/2402.08012v3.
   - Algorithm1: time-evolving domain partition; Algorithm3 uses sparse private Boolean counters for each cell, with noisy completed-interval state plus noisy current-interval count; then deterministic consistency and synthetic output.
   - Lemma3.2 bounds expected error of Algorithm2 on deterministic fixed stream, in terms of horizon T and fixed number n of nonzero arrivals: O((log T+log^{3/2}(n+1))/epsilon).
   - Lemma3.4 bounds expected count error of Algorithm3 using ignored early input mass, accumulated Laplace noise and Lemma3.2 current block error. Eq.(4.4) transfers this to partition-bin error lambda_theta^(t), and Lemma4.2 (from earlier COLT work) converts subregion errors to expected W1. These source derivations do not explicitly prove their utility theorem against a feedback-adaptive data adversary. Theorem1.1 explicitly calls its guarantee 'for all deterministic datasets' in introductory discussion at arXiv PDF printed p.3.
   - CRITICAL: Lemma4.2 is a deterministic geometry/consistency-to-Wasserstein estimate before expectation; no counterexample to its pathwise statement is claimed. Eq.(4.4) concerns EXPECTED counting noise of the more involved sparse mechanism, not simply a single Laplace perturbation.
   - Appendix A proof of Lemma3.2 uses a union bound over at most 2T Laplace noise variables, a uniform good event, an n+1 segment count, and a fallback bad event. This is potential evidence that an alternative PATHWISE proof can handle some adaptation; no full adaptive-Hey analysis or original rate recovered here.
2. Bun–Gaboardi–Wagaman, FORC 2026, https://drops.dagstuhl.de/storage/00lipics/lipics-vol368-forc2026/html/LIPIcs.FORC.2026.22/LIPIcs.FORC.2026.22.html : Theorem8 demonstrates an adaptive privacy+accuracy separation for *its correlated-vector query task*; not a W1-specific lower bound.
3. Li, Wang, Ye, 'Differentially Private Continual Release with Relative Error', arXiv 2608.20230 (2026-08-20), https://arxiv.org/abs/2608.20230 : original abstract independently checked, gives adaptive-versus-nonadaptive accuracy differences for MaxSum/MinSum/MaxSelect/MinSelect under relative-error objectives; not a theorem about private synthetic Wasserstein error.
4. Kumar–Strohmer–Vershynin, 'An Algorithm for Streaming Differentially Private Data', arXiv 2401.14577, https://arxiv.org/abs/2401.14577 ; and their high-dimensional tabular streaming follow-up arXiv 2409.00322 https://arxiv.org/abs/2409.00322 : related streaming synthetic baselines. Their abstracts do not establish the exact adaptive-W1 theorem sought here.
No directly matching adaptive-input He-W1 guarantee was verified in the limited literature screen; absence of match is NOT evidence of novelty.

## ONE decisive two-round analytic falsifier [DERIVATION]
Fix b=1/epsilon >0 and threshold K>0. At t=1, true Boolean x1=0 and noisy published scalar Z=x1+eta=eta, with eta~Laplace(0,b). Let t=2 new (binary) real input be
    x2 := 1{|Z|>K}.
This is causal (x2 depends only on previous published value), and can be read as a one-bin count input. The full stream (x1,x2) thus records information about the reused previous noise eta.

For a FIXED deterministic x2, the illustrative reused-noise two-round counter
    Y2 := x1+x2+eta
has error lambda2 = Y2-(x1+x2)=eta and E[|lambda2|] = b.

For FEEDBACK x2=1{|eta|>K}:
    P(x2=1) = exp(-K/b)
    E[|lambda2| | x1=0,x2=1] = E[|eta| | |eta|>K] = K+b
by the memoryless exponential tail of |Laplace(b)|.
For K=3b, event probability e^-3 and conditional expected error 4b, whereas the fixed-stream unconditional bound is b. By choosing K arbitrarily large, the conditionalization inference can fail by an arbitrarily large ratio, albeit on increasingly rare events.

Crucial sanity:
    E[|lambda2|] = E[|eta|] = b
for the FEEDBACK stream as well. This is NOT a counterexample to any unconditional expected-error guarantee, and is NOT the actual He Algorithm2/3 implementation. It is a decisive counterexample to the *generic inference* that fixed-data E[noise error] bounds may automatically be conditioned on a feedback-chosen realized input.

Additional observation (not separately tested hypothesis): a decomposition into actual counting noise terms may have a pathwise uniform-noise bound independent of input adaptivity. For simple additive counters, causal x2 cancels exactly in Y2-(x1+x2). The technical question for He specifically is sparse Algorithm2's noisy threshold/segment stopping behavior and whether Appendix A's uniform-good-event argument yields a useful uniform expected W1 rate under feedback. Do not overclaim that Eq.(4.4) itself is false; its deterministic-stream premises may simply be outside this adversarial conditioning procedure.

## Scope and scientific judgment
[NEGATIVE] H-B5 automatic *conditionalization* fails; standard selection/conditioning bias, not a new theorem.
[UNCLEAR] The original He adaptive W1 rate remains unverified, NOT disproved; no He counterexample, no attack, no privacy break, no proof that a nontrivial repair is required. The per-bin concentration and pathwise union bound may close the gap with standard methods, perhaps with logarithmic loss.
[UNCLEAR] Entire recursive retraining model, multi-silo privacy/communication, changing window-specific target P_t and semantic rare-tail fidelity are not analyzed in this B5.

STATUS: FAIL_B5_NAIVE_FIXED_STREAM_CONDITIONALIZATION
RESULT: Exact two-round feedback counterexample invalidates a proof-transplant shortcut but does not violate an unconditional Wasserstein error theorem. Primary sources identify sparse-count stopping/accuracy as the next potentially relevant interface.
NOVELTY: FAIL for the conditioning observation; NOT_ESTABLISHED for any He-specific adaptive-W1 obstruction or publication idea.
NEXT_TEST: Only if PI authorizes SYNTH-B6, inspect He Appendix A proof of Lemma3.2 and Algorithm2 stopping mechanics, and test ONE finite-horizon pathwise good-event error bound uniform over causally adaptive Boolean streams, checking the log(T), log(n) cost and whether this plugs into Eq.(4.4) without unauthorized assumptions. Stop if standard union bounds already suffice at a useful rate; no training/Codex/GPU.
STATE_UPDATE: YES only after readback of this finding, negative archive and STATE.md append.
