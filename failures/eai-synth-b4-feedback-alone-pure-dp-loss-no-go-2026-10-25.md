# EAI-SYNTH B4 negative: adaptive feedback alone does not invalidate pure event-level continual DP
Date: 2026-10-25 | EAI / EAI-SYNTH | isolated from EAI-SYS and FHE.

H-B4 (FALSE): Let x_2 depend on first synthetic release Y_1; this alone makes the entire output transcript of He 2024 (epsilon,0)-DP online synthetic-data mechanism cease to have event-level epsilon-DP even if candidate streams differ in only one position.

Source killer [FACT]:
- Denisov et al., NeurIPS2022, §2 **Proposition2.1**, original https://proceedings.neurips.cc/paper_files/paper/2022/file/271ec4d1a9ff5e6b81a6e21d38b1ba96-Paper-Conference.pdf : arbitrary (epsilon,0)-DP continual release mechanism in nonadaptive model has the same parameters in adaptive version when the neighboring-stream model is held fixed.
- He, Vershynin, Zhu, arXiv2402.08012v3, §2.1 Definition2.2, §2.2, §4.1 Proposition4.1, original https://arxiv.org/pdf/2402.08012 : pure epsilon DP for full sequence, with neighboring streams differing by one event.
- Bun, Gaboardi, Wagaman, FORC2026 §1.3 and Def4–5, https://drops.dagstuhl.de/storage/00lipics/lipics-vol368-forc2026/html/LIPIcs.FORC.2026.22/LIPIcs.FORC.2026.22.html : explicitly affirms pure-DP transfer; Theorems7–8 concern ACCURACY impossibility for a specific adaptive correlated-vector task.

ONE minimal two-round neighboring adversarial transcript [DERIVATION]: round1 submit candidate inputs (0,1), observe Y_1; round2 submit (g(Y_1),g(Y_1)), i.e. equal alternatives depending on the observed previous release. Thus each interactive neighbor pair differs in one event only and Denisov Prop2.1 applies to He. Simple surrogate: release Z=x_1+Lap(1/epsilon); then Z+g(Z). Density ratios are bounded in [exp(-epsilon),exp(epsilon)], and the second release is postprocessing. This illustrates the theorem, not an instantiation or proof of He algorithm.

[NEGATIVE] Generic novel "feedback breaks pure continual event-DP" idea KILLED by prior art. If challenge sides change both time positions or one user contributes multiple rounds, He event-level assumption fails and no conclusion about whole-user trajectory privacy follows.
[UNCLEAR] Fixed-stream W1 expected accuracy under feedback-correlated future input is NOT implied by pure-DP transfer; no He-specific accuracy failure or lower bound proved. Existing FORC lower bound is task-specific and not directly transferable to Wasserstein synthetic data.

STATUS: FAIL_B4_GENERIC_FEEDBACK_PURE_DP_PRIVACY_GAP
RESULT: Pure epsilon-DP privacy transfers to valid adaptive event-level continual games, known since NeurIPS2022; narrow research novelty FAIL.
NOVELTY: FAIL; other feedback-dependent accuracy topics NOT_ESTABLISHED.
NEXT_TEST: IF PI approves B5, one He §4.2 expectation/conditional-noise lemma gate under x_2=g(Y_1), preceded by a source-first adaptive W1 utility prior-art check. No GPU or Codex.
STATE_UPDATE: YES only after GitHub negative and root STATE verified.
