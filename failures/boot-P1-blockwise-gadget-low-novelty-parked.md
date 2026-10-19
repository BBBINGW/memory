# BOOT P1 archive — Blockwise heterogeneous gadget is not yet a new optimization

TRACK_ID: BOOT
DATE: 2026-10-19
STATUS: PARKED_LOW_NOVELTY
ITERATIONS: B001–B005

Original candidate: Combine block-binary TFHE 2023/958 with per-operation heterogeneous and approximate gadget of 2025/1892.

Falsifiers:
1. B002: one external product per block does not mean one random key-error source. Inactive selector ciphertexts still contribute noise; direct Gaussian tail transport is unsound.
2. B003: conservative Lemma 1 error bound is too loose to certify the already-implemented uniform d=3 baseline.
3. B004: actual source has signed digits [-64,63], but deterministic discarded low 11 bits have biased residual [0,2^-21), so half-ULP assumption fails.
4. B005: Bernoulli stochastic rounding is algebraically feasible and improves a one-shot noise-tail certificate in an idealized model. Nevertheless efficient randomized gadget decomposition is established prior art (ePrint 2023/535 and FINAL 2022/074), and no reduction in transform count, evaluation key size, or actual latency at the same full DFR/security was shown. The cheapest d=2 parameter proxy fails a 2^-128 sufficient bound.

Do not infer an attack on any original paper. Do not infer insecurity or actual DFR from non-tight upper bounds. Reactivate P1 only if a specific novel block-specific algorithmic advantage is identified and compared with relevant prior art and cost of fresh randomness.

Evidence files: findings/boot-B002-block-key-noise-heterogeneous-gadget-audit.md; findings/boot-B003-lemma1-certification-and-mixed-gadget-screen.md; findings/boot-B004-source-faithful-digit-truncation-tail-gate.md; findings/boot-B005-stochastic-truncation-priorart-gate.md.
NEXT_ACTION: BOOT B006 — 2025/1711 squared gadget + 2025/1892 heterogeneous approximate gadget interface gate.
