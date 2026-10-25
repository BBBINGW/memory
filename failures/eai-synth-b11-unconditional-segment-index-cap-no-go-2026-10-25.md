# EAI-SYNTH B11 negative — Deterministic segment cap does not follow from printed Algorithm2
2026-10-25. EAI-SYNTH isolated. No code, Codex, experiments or models.

H-B11 [NEGATIVE / conditionally resolved]: The exact printed He2024 Algorithm2 guarantees at most T+1 segment index updates for arbitrary noise, so its finite-T Binary Mechanism can be assumed to have a hard index cap without clarifying the test-noise lifetime.

Original source: He–Vershynin–Zhu, arXiv2402.08012v3 Algorithm2 physical PDF printed p.7 https://arxiv.org/pdf/2402.08012 and Appendix A Lemma3.2 printed p.20: pre-test `N_j + lambda'_t <= T0+lambda_j` occurs BEFORE t++; false test seals segment and increments j without consuming an event, with positive probability on Laplace support. The unconditional '2T random variables' and 'trivial T segments even on bad event' phrases in Appendix A are not justified literally by this control-flow ordering. Distinct original ancestor Dwork–Naor–Reingold–Rothblum ASIACRYPT2015 Figure1 https://omereingold.wordpress.com/wp-content/uploads/2014/10/intervals.pdf consumes each input BEFORE a sealing test.

One two-interpretation calculation (see findings record):
A) If lambda'_t is freshly drawn at every check, at each zero-progress retry probability to consume at least one record is >=1/2 by symmetry of the iid Laplace pair. For M<=T+1 record advances (literal t<=T), #segment-start trials K stochastically dominated by time for M successes of iid Ber(1/2): E[K]<=2M, Pr(K>4M)<=e^(-M/4), and Pr(K>4M+16ln(1/delta))<=delta. Standard geometric/Chernoff tail; NO novelty. A fixed T-horizon subcounter needs behavior on K>T positive-probability events to be a total definition.
B) If lambda'_t is sampled ONCE per timestamp and reused on retry, while each lambda_j is fresh, put q=e^(-epsilon/2), c=(1-q)/(1+q), a=floor(9ln T/epsilon), Z=lambda'_t. For z>=a+1, p_z=P(lambda_j>=z-a)=q^(z-a)/(1+q), and conditional retries R~Geom(p_z). Then E R >=sum_{z>=a+1} (c q^z)/p_z =sum_{z>=a+1}(1-q)q^a =infinity. Despite almost-sure eventual progress, expected #threshold draws infinite for this SEMANTICS. This is not an unconditional statement about intended author mechanism: notation `lambda'_t` and Appendix A '2T noises' lean toward one-per-timestamp, but `~Lap` in while predicate could imply redraw each time.
C) Literal `while t<=T`, then t++ and access X_t may read X_{T+1} at t=T; distinct pseudocode indexing boundary issue, not a validated deployed error.

Do not call this an author bug, privacy violation, theorem contradiction, innovation or definite infinite expected runtime without source semantic clarification.

STATUS: HUMAN_REVIEW_B11_NOISE_SAMPLING_SEMANTICS / FAIL_DETERMINISTIC_K_CAP_FROM_LITERAL_PSEUDOCODE.
RESULT: No unconditional hard K cap; fresh draw permits standard random cap, reused draw yields conditional infinite mean.
NOVELTY: NOT_ESTABLISHED; likely a control-flow specification/analysis matter, and prior 2015 consume-before-test flow offers familiar fix.
NEXT_TEST: Author/journal version or canonical code clarifying noise reuse and off-by-one first; if unavailable PARK sparse-counter subline rather than invent a new DP primitive.
PENDING_CODEX: OPTIONAL_B11_AUTHOR_VERSION_SEMANTIC_AND_MINIMAL_CONTROL_FLOW_REPRO; held and no prompt supplied.
STATE_UPDATE: YES only after complete GitHub verification.
