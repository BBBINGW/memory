# EAI-SYNTH B9 negative: all spatial counters good simultaneously is NOT necessary for fixed-time Wasserstein confidence
Date 2026-10-25 | TRACK_ID EAI | EAI-SYNTH only | NO Codex/GPU/model training

[HYPOTHESIS / NEGATIVE] B7-B8 failed to certify every counter's original threshold-good event at confidence 1-beta; therefore no useful fixed-time high-confidence Wasserstein bound can be obtained without that global event. FALSE.

[ONE DECISIVE SOURCE+MATH TEST]
- Original COLT2023 He–Vershynin–Zhu, 'Algorithmically Effective Differentially Private Synthetic Data', https://proceedings.mlr.press/v195/he23a/he23a.pdf §4.5 Theorem10 proof / Lemma17 / Eq4.2–4.4 (PDF physical pp.11–12, printed12–13) proves BEFORE TAKING EXPECTATION the deterministic transport inequality
 W1(mu_X,mu_Y) <= [|lambda_empty|diam(Omega)+sum_{j<r}sum_{|theta|=j}max(|lambda_theta0|,|lambda_theta1|)diam(Omega_theta)]/n+delta_r
for valid consistency processing, including possibly noisy root and n-vs-m output size. It does not require all count errors small nor independent; errors can be arbitrary realisations. Offline source names it Theorem10, whereas online2024 citation says Theorem4.2; edition-number difference, not a discovered flaw.
- Original online He–Vershynin–Zhu arXiv2402.08012v3 https://arxiv.org/html/2402.08012v3 §4.2 Lemma4.2/Eq4.4–4.7 and Theorem1.1 gives for FIXED DETERMINISTIC streams and d>=2: E_M[W1]<=C log(t)(epsilon*t)^(-1/d) for large t. By Markov at ANY fixed t and beta∈(0,1), Pr_M(W1>C log(t)(epsilon*t)^(-1/d)/beta)<=beta. For beta=.05 multiplier20. No full-tree simultaneous counter-event certificate needed. This is classical and can be weak/vacuous at finite t.
- For FEEDBACK-ADAPTIVE input X, the deterministic geometry remains valid on well-defined outputs but E(weighted count errors) need not match fixed-stream noise expectations. Neither Markov nor the offline theorem proves the missing expected accuracy; no adaptive W1 guarantee or counterexample established.

STATUS: FAIL_B9_ALL_COUNTERS_GOOD_NECESSITY
RESULT: Kill B7/B8 all-good-tree event as necessary geometric accuracy requirement. Existing flux/consistency transport and Markov bypass it for fixed streams; feedback-weighted expected counting utility remains UNCLEAR.
NOVELTY: FAIL for geometry/high-prob technique; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: On PI continuation ONE B10 source-first joint adaptive expected weighted count bound/test focused on Algorithm2 stopping and Lemma3.4, NOT training or new algorithm design.
PENDING_CODEX: NONE_REQUIRED_FOR_B9; any later Codex requirements remain pending and undisclosed until requested.
STATE_UPDATE: YES only after GitHub read-back + root checkpoint.
