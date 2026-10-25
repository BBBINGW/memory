# EAI-SYNTH B11 — Sparse-counter empty-segment retries and noise-sampling semantics

Date: 2026-10-25 Asia/Singapore
TRACK_ID=EAI; ACTIVE_TOPIC=SYNTHETIC_DATA; ACTIVE_SUBLINE=EAI-SYNTH.
Previous latest completed: SYNTH-B10. This is one PI-authorized original-source + analytic gate, no algorithm changes, Codex, CPU/GPU benchmark, model training, or remote experiment. EAI-SYS/FHE/all other tracks unchanged.

## ONE primary falsifiable research hypothesis and cheapest decisive test
H-B11: He2024 Algorithm2 as PRINTED gives, without clarifying noise resampling, a deterministic segment-index bound K<=T+O(1) (or a uniform geometric tail), so the standard maximal prefix-noise expectation estimate from B10 transfers directly to the actual algorithm.

ONE cheapest source-first falsifier: inspect exact nested while-loop, noise indices and Appendix A count assertion in original arXiv PDF, then analytically consider ONE starting state (time t with current segment count N_j=0) under two natural meanings of lambda'_t. Compare to cited predecessor's Figure 1 to see whether processing a record is mandatory before closing. No simulations, no code.

## Original papers and exact provenance [FACT]
1. Yiyun He, Roman Vershynin, Yizhe Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv:2402.08012v3, 2024-10-23, https://arxiv.org/html/2402.08012v3 and https://arxiv.org/pdf/2402.08012 . In §3.3 Algorithm2 (original PDF printed p.7, physical index6, screenshot visually inspected) outer loop `while t<=T`, initialize fresh threshold `T0+lambda_j`, inner loop condition `while t<=T and N_j+lambda'_t <= T0+lambda_j`, then *inside body* update `t <- t+1; N_j <- N_j+X_t`; outside inner loop always end segment j, increment j, append N_{j-1} to Binary Mechanism. Thus when N_j=0 and lambda'_t>T0+lambda_j, the code can close an empty segment with t unchanged, and advance subroutine index.
2. Same paper Appendix A Lemma3.2 proof (original PDF printed p.20, physical index19, screenshot inspected), explicitly states 'there are 2T many independent Lap(2/eps) random variables in total' and if uniform event fails it takes 'trivial upper bound T for number of segments'. Such statements are not literally justified by printed precheck-on-every-outer-iteration control flow when empty segments occur. The favorable good event *does* ensure a positive input on every sealed segment, so its pathwise argument remains possible.
3. Dwork, Naor, Reingold, Rothblum, 'Pure Differential Privacy for Rectangle Queries via Private Partitions', ASIACRYPT2015, author-hosted original PDF https://omereingold.wordpress.com/wp-content/uploads/2014/10/intervals.pdf , Figure1 physical PDF index7 screenshot visually inspected: its segment loop explicitly *increments i and consumes x_i* BEFORE performing noisy segment sealing test. No zero-progress closure occurs from a pre-test. The papers are structurally related (He says modified from [24]); cannot silently identify the printed Algorithm2 with the older, safer control flow.
4. Original He Algorithm2 uses notation lambda'_t (suggestive of one noise per timestamp), but draws `lambda'_t ~ Lap` inside the while-condition (suggestive of fresh evaluation). The paper does NOT unambiguously stipulate reusing or resampling lambda'_t if same t is encountered multiple times following empty segment closure. It has an additional finite-horizon `t<=T` versus `X_{t+1}` off-by-one possibility at t=T; classify as pseudocode/boundary ambiguity, NOT demonstrated deployed out-of-range access.

## ONE decisive calculation under two interpretations [DERIVATION]
Let epsilon>0, integer-Laplace scale b=2/epsilon, q=exp(-epsilon/2) in (0,1), c=(1-q)/(1+q), so for Z~Lap_Z(b): P(Z=k)=c q^{|k|}. Set positive threshold A=T0=9ln T/epsilon (assume T>1), a=floor A.

At a fresh segment, N_j=0, so the initial test is lambda'_t <= A+lambda_j. Its failure closes an empty segment without consuming x_{t+1}.

(A) FRESH RESAMPLING at every condition evaluation, including same timestamp retry:
Each outer segment opening uses an independent pair (lambda_j,lambda'_t). Since difference lambda'_t-lambda_j is symmetric about 0, P(pass first test)=P(lambda'_t-lambda_j<=A)>=1/2. A pass consumes at least one record; a fail consumes none. Coupling the opening-success indicators to independent Bernoulli(1/2) yields at most M=T+1 productive openings for literal `t<=T` (M=T with guard corrected to t<T). Let K be the number of outer segment openings until exit. For every integer m,
  P(K>m) <= P(Binomial(m,1/2) < M).
Consequently E[K] <= 2M, P(K>4M)<=exp(-M/4), and for every delta in (0,1):
  P(K > 4M + 16 ln(1/delta)) <= delta
(by lower-tail Chernoff, with conservative constants).
This repairs a deterministic cap by a standard high-prob random cap in the FRESH-EACH-EVALUATION semantics, not a novel theorem. Nonetheless a fixed-length T-instance Binary Mechanism may need explicit behavior when K>T, because such an event has strictly positive probability; the paper does not spell out dynamic horizon extension here.

(B) REUSE one lambda'_t for a given absolute time t while fresh lambda_j is sampled for each new segment:
Condition on the reusable value Z=lambda'_t=z. Each empty attempt resamples only L=lambda_j, so the first-test acceptance probability for integer z>=a+1 is
 p_z = P(L>=ceil(z-A))=P(L>=z-a)=q^(z-a)/(1+q).
The number R of fresh thresholds sampled until the first acceptance is Geometric(p_z) with conditional mean 1/p_z. Since P(Z=z)=c q^z for all z>=a+1,
 E[R] >= sum_{z=a+1}^infty P(Z=z)/p_z
      = sum_{z=a+1}^infty [(1-q)/(1+q)] q^z [(1+q) q^(a-z)]
      = sum_{z=a+1}^infty (1-q) q^a
      = +infinity.
Each R is finite almost surely because p_z>0 for every finite z, but the mean is infinite. This is an exact equality for conditional geometric waiting with identically scaled discrete Laplace noise. It implies no finite expected number of threshold draws for this particular interpretation even at one fixed timestamp; it is NOT a formal runtime analysis of a settled author implementation because sampling semantics remain ambiguous.

Regardless of semantic choice, there is always positive probability of an immediate empty-segment closure, so no ABSOLUTE deterministic K<=T+1 follows directly from printed pseudocode. On the paper's high-prob threshold-good event, its argument K<=n+1 remains useful, conditioned on that event only.

## Scope / falsification / novelty
[FACT] The prior 2015 private partition algorithm processes an input BEFORE checking to close a segment; the 2024 printed algorithm tests BEFORE consuming. This is a material control-flow difference.
[DERIVATION] FRESH test noise => elementary geometric cap; REUSED per-timestamp test noise => exact E[R]=infinity due to matched exponential tails, without implying nontermination almost surely.
[UNCLEAR] Which sampling convention is intended, how a finite-horizon Binary Mechanism behaves if K>T, whether author's IEEE final published version or separate reference code resolves it, and whether a routine reorder/clarification repairs privacy+utility fully. None checked here; no assertion of an actual implementation bug, privacy flaw, or theorem falsification.
[UNCLEAR] Original Appendix A fixed-stream expected count bound, adaptive expected weighted W1 and strong probability tails need proof after concrete semantics clarified. A well-known source-aligned 'consume then test' fix may immediately remove the empty retry issue. Not publishable originality by itself.

STATUS: HUMAN_REVIEW_B11_NOISE_SAMPLING_SEMANTICS / FAIL_UNQUALIFIED_DETERMINISTIC_SEGMENT_CAP
RESULT: Printed pretest permits empty segments; fresh-noise version has standard geometric retry upper tails; timestamp-reuse version has exact infinite mean threshold-retry attempts. Both interpretations affect Appendix A's claimed global 2T noise/segment count.
NOVELTY: NOT_ESTABLISHED (potential pseudocode/analysis ambiguity, not an original construction or validated vulnerability).
NEXT_TEST: HOLD and seek independent original author/journal implementation or explicit clarification of test-noise lifetime and timestamp handling. Only after confirming semantics, one source-level check of expected sparse-count proof and finite Binary Mechanism index support; do not iterate adjacent toy cases. PI should decide whether to PARK EAI-SYNTH sparse-count subline and pivot to a more promising synthetic-data question.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO (no tasks executed; no Codex prompt to user). Only surface any instruction if PI explicitly requests; direct author-source/version/manual semantics verification is higher priority than simulation.
STATE_UPDATE: YES only upon GitHub finding + negative archive (if created) + root checkpoint exact readback.
