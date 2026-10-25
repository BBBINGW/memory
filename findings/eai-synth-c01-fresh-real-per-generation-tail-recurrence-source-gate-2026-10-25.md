# EAI-SYNTH C01 — Fresh-real-data fraction does not guarantee eventual perpetual rare-mode presence
Date: 2026-10-25 Asia/Singapore
TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH
C01 is a NEW fresh-direction source-first falsification, NOT B13 and not reopening PARKED B11/B12 Sparse Counting. Prior latest completed B12. All EAI-SYS, EAI-P, EAI-SEC and FHE tracks unchanged. No Codex, GPU, model download, training, remote benchmark, or code changes. All Codex tasks held PENDING without prompts until PI expressly asks.

## Exactly one falsifiable primary hypothesis / one cheapest decisive test
[HYPOTHESIS H-C01, FALSE] A fixed fraction alpha=1/2 of genuine fresh iid real data every recursive generation, together with perfect empirical-distribution fitting, implies with probability one that there is SOME finite generation after which the fitted model never completely loses the positive-probability rare category. That is, for all p>0, with probability one exists t0 such that q_t>0 for ALL t>=t0. This is a strictly stronger pathwise claim than mean stability, convergence in expected loss, or asymptotic model-parameter stability. Not attributed to any cited paper's theorem.
[ONE CHEAPEST DECISIVE TEST] Construct the exact minimum 2-state-category, 2-training-record, finite-state Markov recursion, solve stationary distribution and recurrence. No noisy private proxy, verifier, Qiao mechanism, program or training experiment.

## Strongest directly adjacent original prior art [FACT, source-depth explicit]
1. Fu, Wang, Chen, Tian, Tao, 'A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training Loops', ICLR 2025 official accepted abstract https://proceedings.iclr.cc/paper_files/paper/2025/hash/e92e6d20f7b5db5c2a1b23964d170fe2-Abstract-Conference.html (arXiv 2502.18865 abstract). Source describes recursive stability, architecture and real/synthetic mix, including convergence with constant-sized real fraction in its specified settings. Full technical theorem proof NOT checked in this iteration: do not extrapolate it to literal all-round Bernoulli tail presence or claim contradiction.
2. Kazdan et al. 'Collapse or Thrive: Perils and Promises of Synthetic Data in a Self-Generating World', ICML2025, PMLR267:29469–29494, original https://proceedings.mlr.press/v267/kazdan25a.html. Compares replacement vs accumulate vs fixed-size subsample workflows; reports bounded/stable losses in accumulated data. This does not state every future empirical generation retains each rare atom.
3. He, Xu, Cheng, 'Recursive learning without collapse: a weighting-based stabilization framework', JRSS-B accepted 6 June/published 1 July 2026, DOI 10.1093/jrsssb/qkag099, official abstract https://academic.oup.com/jrsssb/advance-article-abstract/doi/10.1093/jrsssb/qkag099/8722982. Specifies fresh real + prior synthetic and weighted statistical learning; full article proof was NOT accessed. Thus only bibliography/abstract verified.
4. Qiao et al., 'When Sample Selection Bias Precipitates Model Collapse', ICML2026 PMLR306:101222–101268, original FULL HTML https://arxiv.org/html/2606.13732v2 §2 Replace/Accumulate/Accumulate-Subsample and §3 biased selection, and publisher https://proceedings.mlr.press/v306/qiao26c.html. Tail decay and verifier/sample selection bias already theorized; this C01 toy has NO selection/filtering/DP and should not be cast as their specific algorithm's failure.
5. Shumailov et al. Nature 2024 'AI models collapse when trained on recursively generated data', updated correction Mar2025, original full open access https://pmc.ncbi.nlm.nih.gov/articles/PMC11269175/ and https://www.nature.com/articles/s41586-024-07566-y . Their theoretical intuition explicitly discusses finite resampling/Markov absorbing states for PURE synthetic recursion. This C01 adds a fresh real sample so is an IRREDUCIBLE nonabsorbing Markov chain; applying their absorbing-state conclusion to this setting would be false. The finite-sample information-loss mechanism is strongly prior art.
6. Related: Seddik et al. arXiv2404.05090 https://arxiv.org/abs/2404.05090, real/synthetic mixing threshold; Fu et al. NeurIPS2025 self-verification and Yi et al. ICLR2026 unreliable external verifier. Exact full proofs not independently audited. No new originality is supported by absence of a matching exact toy in a limited search.

## One fully explicit analytical test [DERIVATION]
Let true categorical distribution P=Bernoulli(p), 0<p<1. Rare state is 1. At EACH generation, observe one fresh real sample R_t~Bern(p), independently across t, and one synthetic sample S_t|q_t~Bern(q_t), independently of R_t conditional on q_t. PERFECT empirical-distribution fitting to the two observations yields q_{t+1}=(R_t+S_t)/2. This uses EXACT alpha=1/2 fresh real fraction, no privacy noise and no biased verifier.
After first round, q_t ∈ {0,1/2,1}, with ordered transition matrix
 M = [[1-p,p,0],
      [(1-p)/2,1/2,p/2],
      [0,1-p,p]].
For every p∈(0,1), this finite-state chain is IRREDUCIBLE (0↔1/2↔1) and APERIODIC (positive diagonal), so each state, including the zero-tail state q=0, is recurrent and visited infinitely often almost surely. An exact stationary probability vector is
 pi = ((1-p)^2, 2p(1-p), p^2).
Check direct detailed balance pi0*p=piHalf*(1-p)/2 and piHalf*p/2=pi1*(1-p), plus sum=1.
Consequences:
 (i) lim_t Pr(q_t=0)=(1-p)^2>0;
 (ii) Pr(q_t=0 infinitely often)=1.
Hence claimed eventual perpetual tail presence `exists t0 forall t>=t0 q_t>0` has probability ZERO; H-C01 FALSE.
Yet conditional mean E[q_{t+1}|q_t]=(p+q_t)/2, hence E q_t=p+2^{-t}(q_0-p), recovering expected rare-mode frequency p. Finite recurring absence does NOT mean monotone model collapse or failure of expectation stability; in particular from q=0, future fresh real sampling gives probability p of returning to q=1/2 on the next step.
At p=.01 stationary distribution (0.9801,0.0198,0.0001), so q=0 about 98.01% of generations in stationary time-frequency, even though each generation uses 50% real data. This is due to only TWO records; do not extrapolate numeric fraction to substantial models or claim such poor cover is induced specifically by synthetic recurrence. Distribution pi happens to equal Binomial(2,p)/2 in this tiny model.

## Verdict / scope
[NEGATIVE] H-C01 FALSE: constant positive fresh-real share does not imply time-uniform PATHWISE support/rare-group guarantee with fixed tiny generation samples. A basic finite irreducible Markov chain and classical recurrence prove it; the idea is NOT publishably novel. Prior work on mixture learning performance/stability and selection-driven collapse uses distinct contracts and is not contradicted.
[UNCLEAR] Any improved finite-resource tail coverage under (epsilon,delta)-DP, verifier imperfections, changing real reference, multiple silos and recurrent feedback would require additional assumptions and direct closest theorem comparison; no such new method or stronger lower bound established. Don't loop back into B1 static moment or B2 fixed-domain histogram no-go.
[AGENT RECOMMENDATION] Record C01 as negative scope clarification; do NOT claim fixed alpha prevents every-epoch loss. If PI continues fresh synthetic-data work, consider ONE next falsifiable **nontrivial trade-off** between finite-window high-confidence rare support and real-data acquisition/verification cost, FIRST checking existing sample-complexity and private adaptive-selection lower bounds. Avoid further adjacent finite-state toy sweeps or unsupported claim that log-horizon sample allocation is novel.

STATUS: FAIL_C01_POSITIVE_REAL_FRACTION_IMPLIES_EVENTUAL_PATHWISE_RARE_COVERAGE
RESULT: Exact three-state Markov chain has positive stationary zero-tail probability and zero-tail infinitely often a.s.; average q_t nonetheless converges to true p.
NOVELTY: FAIL for tested elementary recurrence argument; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: IF PI continues, select ONE C02 prior-art-first coverage-vs-sample-budget or feedback-verifier information-interface claim with a precise regime and a cheapest source-level falsifier, not another constant-fraction folklore claim.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO carried from B12 unexecuted; none newly required for C01; withhold prompts until explicit PI request.
STATE_UPDATE: YES only after finding/negative file/root STATE exact readback.
