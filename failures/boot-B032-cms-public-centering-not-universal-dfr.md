# BOOT B032 failure archive — CMS bias centering is not a uniform DFR/security improvement

TRACK_ID: BOOT
ITERATION: B032
DATE: 2026-10-19
STATUS: FAIL_PER_INSTANCE_ERROR_IMPROVEMENT / PASS_BINARY_MEAN_CENTERING / LOW_NOVELTY

Source Bergerat et al. ePrint 2025/2214 'Accelerating TFHE with Sorted Bootstrapping Techniques', 48pp title verified VERSION_UNVERIFIED PDF SHA256 8e342f162db953a4c26d2103f66406b5148b6fa798c7775478342900d9850d84, §4 Algorithm3 pp19–23 Sorted Extended Bootstrapping, §5 CMS Lemma8 pp23–27. Original CMS publicly changes d rounded LWE mask coefficients a'_i by δ_i=±1 to shift into cheaper 2-adic sorted CMUX class. This introduces phase perturbation −Σ δ_i s_i.

Hypothesis repair: for iid uniform binary s_i, compute public D=Σδ_i and shift body b' by nearest_integer(D/2). Exact phase perturbation t−Σδ_i s_i has conditional mean abs≤1/2 and variance d/4, compared to uncompensated mean−D/2 and same variance. This is elementary public-body centering; it does not modify CMS mask classes or keys, and only holds for the stated prior on secret. The paper already provides CMS mean/variance, so nonzero bias by itself is not a new cryptographic finding. The standard MS body rounding and other FHE errors are NOT removed.

50000 seeded Bernoulli-key toy samples for all δ+1 per d:
 d8: mean -4.00106→-0.00106, |error|≥2: .9643→.28936;
 d16: -7.99588→+.00412, |error|≥4: .9898→.07764;
 d32: -15.99478→+.00522, |error|≥8: .99902→.00718;
 d64: -31.9974→+.0026, |error|≥16:1.0→0.00002.
These are illustrative perturbation-only tails, not genuine bootstrapping DFR or IND-CPA-D model. Variance unchanged by deterministic body adjustment, and total-error covariance untested.

DECISIVE COUNTEREXAMPLE to a stronger 'never worse' statement: d4,δ_i=+1 all, actual secret bits all0. Original CMS perturbation 0; public correction +2 yields error2; strictly worsens a legitimate instance. With ternary zero-mean secrets the binary-target centering can be systematically wrong. No source native code, noise tail proof, end-to-end KS-PBS time or security estimator run. Cannot claim a new bootstrapping performance/security innovation or universal improvement.

Finding: findings/boot-B032-sorted-cms-public-body-bias-centering-gate.md
NEXT B033: If pursuing source CMS, smallest genuine novel question is whether PUBLIC input-specific constrained sign/rounding selection, with exact noise/cost tradeoffs and binary/ternary secret model, beats paper's existing d-parameter tuning under full IND-CPA-D and net key/time cost. First exhaustive finite optimization and direct prior art check, one hypothesis only; otherwise archive branch and audit next BOOT paper. BOOT only; B033 not started.
