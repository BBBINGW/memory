# EAI-SYNTH B8 negative — fixed 9logH threshold cannot satisfy this simultaneous envelope certificate
Date: 2026-10-25 | EAI-SYNTH only | one source-first analytic falsifier | no GPU/Codex/model/training.

H-B8 FALSIFIED: Without retuning He's Algorithm2 threshold T0=9ln H/eta, allocate failure probabilities across all active cell counters in one epoch totaling delta=.05, and use a standard independent 2H Laplace max-envelope B(beta) to preserve the source's positive-progress proof condition T0>2B(beta).

[FACT] He–Vershynin–Zhu arXiv2402.08012v3 Algorithm2, Algorithm3, Eq4.1 and Appendix A https://arxiv.org/html/2402.08012v3 . Each Alg2 window uses local eta=eps_{j,i}/2, and original fixed-9 threshold. Original Appendix A uses B=(2/eta)(2lnH+ln2) with about 1/H failure. Prior art Dwork–Naor–Reingold–Rothblum, ASIACRYPT2015 https://omereingold.wordpress.com/wp-content/uploads/2014/10/intervals.pdf , Figure1/Thm3.1 already has beta-dependent private partition thresholds and all-time confidence results; mere threshold retuning is NOT novel.

[ONE TEST / DERIVATION] For integer Lap(2/eta), P(|Z|>B)<=2exp(-eta B/2). A conservative union over 2H potential threshold/test noises gives B(beta)=(2/eta)ln(4H/beta). Then original positive-progress condition is exactly 9lnH>4ln(4H/beta) or beta>4H^(-5/4). Privacy eta cancels, including He Eq4.1 schedule. At global eps=1, spatial d=2, temporal i=8, H=256 and M=sum_{j=1}^8 2^j=510. Each beta must exceed .00390625, so any all-510 envelope allocation needs sum beta>1.9921875, incompatible with delta=.05. Equally allocated beta=.05/510 leads eta*T0=49.9065970 and eta*(2B)=64.6464592, so proof inequality reverses. The same qualitative conclusion holds when the conservative envelope constant 4 is improved to 2 (total >.996>.05).
[NEGATIVE/BOUNDARY] The fixed-threshold *sufficient certificate* fails; this does NOT show actual probability of wrong counting, lower bound on W1, impossibility of adapting, or author algorithm bug. Weighted concentration and known beta-dependent threshold retuning could avoid this proof condition. This is a known confidence calibration issue, not a new DP mechanism or publication.
[NO CODEX] No code required; hold any future requests until explicitly asked.

STATUS: FAIL_B8_FIXED_THRESHOLD_GLOBAL_CONFIDENCE_ENVELOPE
RESULT: Exact finite one-epoch confidence-vs-threshold conflict for the specified union-envelope tactic; existing 2015 confidence-threshold prior art kills trivial retuning novelty.
NOVELTY: FAIL on tested idea, broader line NOT_ESTABLISHED.
NEXT_TEST: Only after PI continuation, source-first weighted-W1 Lemma4.2/COLT2023 stability audit; test ONE claim that all-cell good events are unnecessary when directly bounding diameter-weighted aggregate count errors.
PENDING_CODEX: NONE_REQUIRED_FOR_B8.
STATE_UPDATE: YES after failure file and root STATE both verified.
