# EAI-SYNTH B6 — Uniform-noise gate for causal-adaptive sparse continual counting
Date: 2026-10-25 Asia/Singapore
TRACK_ID: EAI | ACTIVE_TOPIC: SYNTHETIC_DATA | ACTIVE_SUBLINE: EAI-SYNTH
B6 follows B5; strictly independent from EAI-SYS, EAI-P, EAI-SEC, FHE, SHIP, BOOT, CGS, VFHE, EXPLORE.
No Codex, remote/GPU, model download, training, source modification or large experiment. PENDING_CODEX: NONE; do not issue Codex instructions unless PI requests.

## ONE primary hypothesis and ONE decisive test
[HYPOTHESIS H-B6] Existing **input-independent uniform noise events** for He's Algorithm 2 sparse counter and standard Binary Mechanism yield a nonvacuous, finite-horizon, **high-probability accuracy bound against any causally feedback-adaptive Boolean stream**, without conditioning on the realized stream. The claim is deliberately limited to count accuracy, not identical original expected W1 rate or a new primitive.
[CHEAPEST TEST] Source-read Algorithm2, Lemma3.1–3.2 and Appendix A and independently combine (a) a threshold-noise uniform event with (b) a simultaneous noise-only prefix bound for the additive Binary Mechanism. Verify causal adaptivity does not invalidate the pathwise decomposition and identify precise loss.

## Primary original source [FACT]
He, Vershynin, Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv:2402.08012v3 2024-10-23; https://arxiv.org/html/2402.08012v3 and https://arxiv.org/pdf/2402.08012 . PDF printed page 7 Algorithm2; p8 Lemma3.1–3.2 / Algorithm3; p20 Appendix A proof Lemma3.2, p21 expectation wrap-up. Browser PDF page indices 6,7,19,20 visually inspected.
- Algorithm2: fixed finite horizon T and epsilon, threshold T0=9log(T)/epsilon, one private threshold noise lambda_j~integer Lap(2/epsilon) per segment and one test noise lambda'_t~same scale per threshold test; current segment's true Boolean count S_j; closed-segment counts fed to a Binary Mechanism Asub with budget epsilon/2. While a segment is active, private output equals previous-segment noisy prefix; uncommitted current true segment mass R_t is omitted.
- Appendix A proof Lemma3.2: on a common noise-good event of probability at least 1-1/T, preallocated <=2T relevant threshold variables have |lambda|<=B=2(2log T+log2)/epsilon; for T>16, T0-2B>0, every sealed segment has >=1 positive bit, so #segments <=n+1 where n is total count of 1s. Residual current segment S_j <=T0+2B up to a unit offset from update/check ordering.
- Lemma A.1 from Chan et al. [14], same Appendix: for standard Binary Mechanism (with its own epsilon_sub), at each fixed index m<=H, the additive counting noise obeys a tail of the form Pr(|Z_m|>C epsilon_sub^-1 log^(3/2)(H) log(1/beta)) <= beta. Lemma applies to a fixed-index noise variable. Standard binary tree counter outputs true prefix + sum of a fixed index-dependent subset of internal independent noise variables. This deterministic algebraic decomposition permits a simultaneous noise-only event **even when the input sequence depends on past released outputs**.
Original Binary Mechanism: Chan, Shi, Song, 'Private and Continual Release of Statistics' (2011), https://eprint.iacr.org/2010/076 and author/publisher evidence https://people.eecs.berkeley.edu/~dawnsong/papers/2011%20Private%20and%20Continual%20Release_a26-chan.pdf . Mechanism/prior art is known.

## Single decisive derived calculation [DERIVATION]
Fix any bounded horizon T>16 and any causal policy selecting x_t∈{0,1} from past released noisy outputs; its realized number of positive bits n_T can be random.
1. Pre-sample 2T independent threshold/test noises and define G_th by max of their magnitudes <=B. He Appendix A gives Pr(G_th)>=1-1/T. On G_th, by induction every sealed segment consumes at least one 1-bit; no zero-progress segment can occur, so no more than n_T+1<=T+1 segments or <=2T threshold noises are actually used. This induction makes the presampling self-consistent. For every t<=T with a released count, unfinished mass R_t<=T0+2B+1. All implications are PATHWISE and do not depend on independence between x_t and prior noise.
2. Write the standard Binary Mechanism prefix at *segment index* m as Q_m = sum_{k<=m} N_k + Z_m, where Z_m is a fixed algebraic sum of time-indexed/tree-node noises. Although m=J(t) is adaptive, every Z_m exists on one predetermined random tape, independent of which stream values are later chosen. Using Lemma A.1 with H=m+1, epsilon_sub=epsilon/2, assign beta_m=(6 delta)/(pi^2(m+1)^2) (or a normalized summable sequence). A union bound over ALL m>=1 yields a single G_bin with probability >=1-delta, on which simultaneously
  |Z_m| <= (C/epsilon) log^(3/2)(m+1) log(C0 (m+1)^2/delta)
for all segment indices m<=T+1. This step is an application of fixed-index TAIL bounds to **noise-only** variables, NOT conditional expectations given a data-dependent stopping index.
3. The true prefix decomposes as C_t=sum_{k<=J(t)}N_k + R_t. The reported prefix equals sum_{k<=J(t)}N_k + Z_{J(t)} (including m=0 convention Z_0=0), so **pathwise**
   |C_t - Q_{J(t)}| <= R_t + |Z_{J(t)}|
   <= T0+2B+1+sup_{m<=n_T+1}|Z_m|.
On G_th ∩ G_bin (probability >=1-1/T-delta), this implies for ALL t<=T:
   |C_t-Q_{J(t)}| <= (9logT+8logT+4log2)/epsilon +1
        +(C/epsilon) log^(3/2)(n_T+2) log(C0(n_T+2)^2/delta).
Equivalently big O: (logT + log^(3/2)(n_T+2)*log((n_T+2)^2/delta))/epsilon (+1), for fixed epsilon and usual asymptotics.
For delta=1/T, O((log T+log^(3/2)(n_T+2)log(T(n_T+2)))/epsilon), high-prob ≥1-2/T; for fixed delta, O((logT+log^(5/2)(n_T+2)+log^(3/2)(n_T+2)log(1/delta))/epsilon).
4. In particular the bound is input-adaptive and retains n_T sparsity dependency, **but has an extra logarithmic factor** relative to the fixed-stream expected error O((logT+log^(3/2)(n+1))/epsilon). It is HIGH PROBABILITY only; does NOT immediately give E error on the bad event, same optimal rate, or a multi-cell infinite-time W1 guarantee.
5. CAREFUL BAD EVENT LIMIT: Algorithm2 pseudocode can, under sufficiently extreme threshold noise, close a segment before consuming any record. The Appendix A sentence '2T noise variables in total' is rigorously justified on the good event by the induction, NOT globally without controlling zero-progress loops. Consequently do not infer a tail-expectation bound for all sample paths or a deployed nontermination vulnerability from this argument. Does not undermine the proved good-event calculation.

## Falsification, novelty and limitations
[PASS MATH, narrow] H-B6 survives at the finite-T high-prob count level under the standard additive binary counter/noise model: an explicit pathwise uniform event exists. This directly weakens the claim that adaptive inputs intrinsically require a new DP mechanism even for polylog count utility.
[PRIOR ART] The proof ingredients are exactly textbook union bounds, source Appendix A uniform event, and classic additive Binary Mechanism. **No publishable novelty** in the B6 bound; this is an independent limited derivation, not claimed as an author theorem nor a general new result.
[UNCLEAR] Original expected sparse rate under feedback, cost of rare zero-progress behavior, propagation to full He Algorithm3 multiple levels and partition cells, and W1 expectation/convergence with private dynamic P_t or recursive generator remain unverified.
[UNCLEAR] No code/data benchmark is necessary for this mathematical gate. Any future Codex need is PENDING (not to be executed or supplied unless PI requests); B6 itself has NO CODEX TASK.

STATUS: PASS_B6_CAUSAL_ADAPTIVE_HIGH_PROB_COUNT_BOUND
RESULT: A single simultaneous threshold/tree-noise event gives O((logT + log^(3/2)(n_T+2) log((n_T+2)^2/delta))/epsilon) count accuracy for all t<=T with failure <=1/T+delta, under specified mechanism/timing assumptions; expected He W1 bound NOT proved.
NOVELTY: FAIL for B6 proof idea (known technique); broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: Only on PI continuation, ONE B7 source-level gate: inspect whether the per-segment uniform tail certificate plus Algorithm3 accumulated level-noise can be propagated through He Lemma4.2/Eq(4.4) to a **finite-horizon adaptive W1 high-prob** bound without an exponential-in-depth union penalty. Compare exact error/epsilon allocation to author's §4.2. Stop if standard union bounds give a useful rate; do not start models/experiments.
PENDING_CODEX: NONE_REQUIRED_FOR_B6. Future Codex asks are deferred until PI explicitly requests them.
STATE_UPDATE: YES after GitHub append and reread verification.
