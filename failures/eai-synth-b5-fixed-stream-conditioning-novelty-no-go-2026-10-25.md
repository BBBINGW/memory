# EAI-SYNTH B5 — Generic fixed-stream conditioning shortcut is false (negative archive)
2026-10-25 | EAI-SYNTH only | ONE two-round analytic test | NO model, GPU, Codex.

H-B5 [NEGATIVE]: For adaptive data, fixed-stream expected counter noise error bound E|lambda|<=b can always be promoted to E[|lambda| | realized stream] <=b for the same realized stream. FALSE.

One precise test [DERIVATION]: eta~Laplace(0,b), x1=0, released Z=eta, x2=1{|Z|>K}. In an illustrative reused-noise two-round prefix count Y2=x1+x2+eta, lambda2=eta. For every fixed x2, E|lambda2|=b; but P(x2=1)=exp(-K/b), and E[|lambda2| | x2=1]=K+b. K=3b gives 4b versus b. Unconditionally E|lambda2|=b even under feedback. Thus it falsifies naïve conditionalization ONLY, not unconditional accuracy or DP. This toy is NOT He's Algorithm2/3 and does NOT demonstrate any bug in it.

[FACT] He–Vershynin–Zhu, arXiv2402.08012v3 https://arxiv.org/pdf/2402.08012, original §3 Lemma3.2–3.4, §4 Lemma4.2 and Eq.(4.4)–(4.6), Appendix A: fixed deterministic stream expected sparse count error feeds expected W1; its Appendix A also uses uniform high-probability control over at most 2T noises, which may support causal-adaptive pathwise proof. Their Lemma4.2 geometry is not disproved; Eq.(4.4) is not claimed incorrect.
[FACT] Bun–Gaboardi–Wagaman FORC2026 https://drops.dagstuhl.de/storage/00lipics/lipics-vol368-forc2026/html/LIPIcs.FORC.2026.22/LIPIcs.FORC.2026.22.html proves separation in different correlated-vector accuracy task; Li–Wang–Ye arXiv2608.20230 https://arxiv.org/abs/2608.20230 proves task-dependent adaptive accuracy contrasts in relative-error continual release. None independently proves He's feedback-W1 failure.

STATUS: FAIL_B5_NAIVE_FIXED_STREAM_CONDITIONALIZATION
RESULT: Fixed-data expected error cannot simply be conditioned on adaptively selected stream. Actual He unconditional adaptive W1 error unknown; no He-specific flaw or new contribution established.
NOVELTY: FAIL generic conditioning fact; He-specific gap NOT_ESTABLISHED.
NEXT_TEST: Only on PI continuation, ONE B6 uniform-good-event audit of He Appendix A Lemma3.2 and Algorithm2 stopping: establish whether a pathwise noise bound holds for causally adaptive inputs and whether the ensuing W1 cost is useful, with exact log factors.
STATE_UPDATE: YES only after readback/STATE append verified.
