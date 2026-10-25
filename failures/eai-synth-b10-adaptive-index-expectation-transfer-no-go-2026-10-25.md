# EAI-SYNTH B10 — fixed-index expectations cannot automatically transfer to an adaptively chosen prefix index
Date 2026-10-25. EAI-SYNTH isolated. No Codex/GPU/training.

H-B10 [NEGATIVE] When a private Binary Mechanism's prefix index is selected using past public outputs, every fixed-m noise expectation E|Z_m|<=b automatically ensures E|Z_J|<=b with NO additional maximal-control argument. FALSE.

Exact single cheap test: independent Z1,Z2~Laplace(0,b), J=1 if |Z1|>b otherwise 2. Then E|Z_J|=2b/e + b(1-e^-1) = (1+e^-1)b ≈1.367879b>b. E max(|Z1|,|Z2|)=1.5b confirms standard maximal inequality can cover the penalty. For K noise-only prefixes satisfying fixed-index exponential tail parameter a, E max_{m<=K}|Z_m|<=a(1+ln K), by elementary union bound and integration.

Source anchors: He–Vershynin–Zhu arXiv2402.08012v3 https://arxiv.org/html/2402.08012v3 Algorithm2 §3.3, Lemma3.1–3.2, Algorithm3/Lemma3.4 §3.4, Appendix A Lemma3.2, fixed-deterministic-stream Theorem1.1 commentary §1.3. In He, sparse segment J depends on threshold/test noise and (with adaptive stream) may depend on past released Binary Mechanism noise. The toy is NOT an actual He execution, no expected-W1 or pure-DP theorem has been disproved. For fixed deterministic inputs, the source's use of fixed-index noise bounds may be valid under noise independence. The actual mechanism's stopping/index tail and bad-event behavior require separate audit. This is a generic prior-known selection-bias phenomenon, NOT a new paper result or proven author bug.

STATUS: FAIL_B10_NAIVE_FIXED_INDEX_EXPECTATION_AT_ADAPTIVE_STOPPING
RESULT: Abstract adaptive prefix selection breaks unconditional marginal-bound substitution; maximal noise tools suggest standard repairs with log factor, but real He adaptive bound remains UNCLEAR.
NOVELTY: FAIL for optional-index observation; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: only on PI continuation, one B11 source-level check of Algorithm2 finite-time zero-progress retries and deterministic or tail-bounded segment-index cap K, to see if standard maximal bound applies to actual adaptive release. No Codex until PI requests.
PENDING_CODEX: NONE_REQUIRED_FOR_B10.
STATE_UPDATE: YES only after readback and root checkpoint.
