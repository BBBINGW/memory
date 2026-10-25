# EAI-SYNTH B9 — Source-first weighted Wasserstein pathwise stability gate
Date: 2026-10-25 (Asia/Singapore)
TRACK_ID=EAI, ACTIVE_TOPIC=SYNTHETIC_DATA, ACTIVE_SUBLINE=EAI-SYNTH. LATEST_PREVIOUS=SYNTH-B8. All EAI-SYS/FHE/other EAI lines untouched. No Codex, training, GPU, server, model downloads or code modifications. Any future Codex tasks are PENDING ONLY until explicit PI request.

## ONE falsifiable primary hypothesis and cheapest decisive test
[HYPOTHESIS H-B9, FALSIFIED] To obtain any meaningful *fixed-time high-probability Wasserstein* guarantee from He's spatially weighted private counts, one MUST prove that every one of the spatial sparse counters is simultaneously inside its threshold-good event. Therefore B8's failed full-tree union certificate creates a necessary obstacle to high-probability W1 accuracy.
[ONE CHEAPEST DECISIVE TEST] Read full original COLT2023 consistency/stability proof on publisher PDF, locate precise inequality BEFORE taking expectation; combine it with He2024 fixed-deterministic-stream expectation bound via Markov for a fixed t. If this already yields a nontrivial high-confidence W1 statement without all-counters-good, H-B9 fails. NO synthetic experiment.

## Exact source facts and provenance
[FACT, original] He, Vershynin, Zhu, 'Algorithmically Effective Differentially Private Synthetic Data', COLT2023, PMLR 195:3941–3968, PDF https://proceedings.mlr.press/v195/he23a/he23a.pdf. Section 4.4 *Theorem 10* states expected W1 accuracy for offline Algorithm4. Section 4.5 Lemmas 16–18 and proof of Theorem 10, especially PDF **physical pages 11–12** (printed pp.12–13), Eq.(4.2)–(4.4), give the transport construction: correct total count, redistribute bounded sibling flux, then relocate within leaf cells. Lemma17 bounds sibling flux by max of the two child absolute raw count errors. The proof obtains a **DETERMINISTIC** weighted W1 inequality prior to a separate explicit 'Taking expectation' step. Original PDF page screenshots p9,p11,p12 visually verified in this session.
[FACT, original] He–Vershynin–Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv:2402.08012v3 2024-10-23, https://arxiv.org/html/2402.08012v3 . §3.5 Algorithm4 is the same consistency principle; §4.2 Lemma4.2 reuses this offline stability geometry in EXPECTATION form, Eq.(4.4) bounds fixed-stream expected cell count error, Eq.(4.5) sums sibling maxima with parent diameter and Eq.(4.6) provides a depth-weighted sum. Theorem1.1 explicitly says its guarantee concerns **all deterministic datasets**, §1.3, with for d>=2 (at sufficiently large t) E W1(mu_Xt,mu_Yt) <= C log(t)(epsilon t)^(-1/d), C implicit depending on standard theorem conditions. In COLT2023 published full PDF, relevant result is called **Theorem 10**, whereas online2024 calls its imported lemma 'Lemma4.2 ([36], Theorem4.2)'; treat this as edition/numbering difference, not an attack.
[IMPORTANT SOURCE BOUNDARY] COLT2023 offline Algorithm4 may output m!=n points because of noisy root count. Its PATHWISE bound includes |lambda_empty|*diam(Omega)/n. Online2024 Theorem1.1 promises t output points, but don't erase the root term in a generic restatement unless root handling is independently specified. If counts are inconsistent or output empty, the transport lemma's stated assumptions need checking; do not call it unconditionally true for arbitrary invalid count vectors. No assumption that lambda coordinates are mutually independent is needed for its *deterministic* geometry.

## ONE decisive derived calculation
[DERIVATION: deterministic transport]
For any fixed valid true counts and private counts on a finite binary partition, after the same comparable-child consistency/postprocessing, define actual raw errors lambda_theta = private count_theta - true count_theta; let D0=diam(Omega), delta_r=max_{|theta|=r}diam(Omega_theta), and
 A = |lambda_empty| D0 + sum_{j=0}^{r-1} sum_{|theta|=j} max(|lambda_theta0|,|lambda_theta1|) diam(Omega_theta).
The COLT2023 §4.5 construction gives PATHWISE
 W1(mu_X,mu_Y) <= A/n + delta_r
(for its well-defined nonempty output and applicable count framework).
No requirement G=intersection of every sparse counter's threshold-noise good event. Errors are *arbitrary realized* values, potentially correlated with adaptive prior transcript, at this geometry stage.

[DERIVATION: fixed-stream high probability]
Let f_{epsilon,d}(t) be the He2024 Theorem1.1 bound on E W1 for a *deterministic fixed* stream, at a specified t. Nonnegativity of W1 and Markov imply for any beta∈(0,1):
  Pr_M{W1(mu_Xt,mu_Yt) > f_{epsilon,d}(t)/beta} <= beta.
For d>=2 and t>=C_epsilon, f(t)=C log(t)(epsilon t)^(-1/d), yielding a fixed-time 1-beta confidence rate O(beta^-1 log(t)(epsilon t)^(-1/d)).
At beta=0.05, the Markov multiplier is 20. It can be vacuous for small t or extremely high confidence, but tends to zero as t grows for fixed beta,epsilon,d. This bound uses source expected W1 and standard Markov; it does NOT require all sparse counters' simultaneous good event. For an arbitrary finite set of observation times one can union-bound these *aggregate W1 events* (pay confidence factor), not the individual count-event failures. None is novel.
[DERIVATION / adaptive conditional boundary] For an adaptive feedback-controlled stream X_t the PATHWISE transport relation still holds on every well-defined output, but it only implies
  Pr{W1 > delta_r+u} <= E[A]/(n u)
if a suitable bound on E[A] for the JOINT feedback/randomized law has been independently proved. He2024 fixed-deterministic-stream E[A] estimates via Lemma3.4/Eq4.4 do NOT automatically transfer to feedback-selected random X_t (B5). Markov cannot create that missing expected-accuracy premise. This B9 is not a full adaptive accuracy theorem, impossibility, or He bug.

## Science judgment and stop
[NEGATIVE] H-B9 is FALSE: all-good spatial counter events are unnecessary for a meaningful FIXED-TIME fixed-stream W1 high-prob upper bound. The COLT2023 pathwise weighted transport inequality plus He2024 expected W1 and textbook Markov already resolves this narrow geometric/probability obstacle. Thus B7-B8's union-confidence issue is not an obstacle to the ordinary fixed-stream high-prob W1 claim.
[UNCLEAR] Adaptive-stream E[A] at the same useful rate remains unproven; even when a geometric pathwise bound holds, sparse counter count errors may depend on adaptive stopping and error distribution. No novel construction or lower bound established.
[PRIOR ART] Deterministic flux/weighted geometric proof is directly in authors' COLT2023 §4.5; Markov is elementary. Do NOT represent these as discoveries, new Wasserstein concentration, or high-prob algorithmic improvements. Park B7/B8 all-good-event proof idea.

STATUS: FAIL_B9_ALL_COUNTERS_GOOD_NECESSITY / PASS_ORIGINAL_PATHWISE_TRANSPORT_IDENTIFICATION
RESULT: Existing deterministic weighted transport bypasses full-tree all-good event for Wasserstein geometry; fixed-stream single-time high-prob follows from original expectation by Markov. Adaptive E[weighted errors] still UNKNOWN.
NOVELTY: FAIL for pathwise geometry and fixed-stream high-prob; NOT_ESTABLISHED for feedback-adaptive synthetic-data research.
NEXT_TEST: ONLY ON PI CONTINUATION, ONE B10 source-first adaptive weighted-moment falsifier: inspect He2024 Appendix A Lemma3.2 sparse stopping and §3.4 Lemma3.4, and test whether their fixed-stream expected sparse-count bound can be upgraded to a JOINT adaptive `E[A_t]` bound without relying on per-counter conditioning. Identify an explicit problematic noise-dependent stopping expectation or derive a uniform moment bound; do not claim a gap unless source-aligned proof fails beyond known techniques. No repeated toy or training.
PENDING_CODEX: NONE_REQUIRED_FOR_B9; any future requirement remains pending and instructions must NOT be sent until PI asks.
STATE_UPDATE: YES only upon finding/negative archive/STATE writes plus exact re-read verification.
