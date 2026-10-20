# BOOT-B076 — Dense subring × BatchBoot: binary type and Hamming/entropy gate
Date 2026-10-20 | TRACK_ID BOOT | SHIP PAUSED
STATUS: PASS_SUBRING_MODULE_ALGEBRA / FAIL_DIRECT_BATCHBOOT_BINARY_INTERFACE / FAIL_MATCHED_HAMMING_ENTROPY_GATE / UNCLEAR_SECURITY_MATCHED_HYBRID

## Hypothesis
Replace the BatchBoot sparse binary RLWE key with Ma2025's uniformly sampled ternary key in an embedded dense subring, obtaining comparable 33–42 Hamming weight and 128-bit security evidence without losing EMPmul amortized efficiency. Falsify by exact secret-type identity, sample distribution/entropy bound, and cost before implementation.

## Published source, verified original full texts
[FACT] Zhihao Li et al., BatchBoot, USENIX Security 2026, https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf . PDF page4 Section3 Eq.(1): sparse **binary** s=Σ_(j∈idx(s)) X^j, Hamming h. Page8 Algorithm3 runs h+1 EMPmul full packed or h+k sparse packed (k=N/n). Page20 Table9: BatchBoot Boot2 N2048 h39 Q2^64, Boot4 N2048 h42 Q2^64, Boot6 N4096 h33 Q2^64, Boot8 N4096 h34 Q2^64, all >128-bit security *per paper's original estimation/distribution*.
[FACT] Ma, Huang, Wang, Wang, Practical Dense-Key Bootstrapping with Subring Secret Encapsulation, ASIACRYPT 2025, https://eprint.iacr.org/2025/1594 ; original ePrint cached in connected Research GitHub Notes, physical pp10–12. Public key-switching to uniform ternary subring s'(Y) in R'=Z_Q[Y]/(Y^N'+1), then embedding s(X)=s'(X^r), r=N/N'; security Lemma1 relies on lower-dimension dense RLWE, with matched error distribution. Uniform ternary h~Binomial(N',2/3). Cached PDF SHA256 505960fa3711aec3ead4d0730d7c41adbd8eace41ee6f5382e74a5b63fcc56f6, VERSION_UNVERIFIED.

## Correct algebra but wrong binary interface
[DERIVATION] For any ring R_Q=Z_Q[X]/(X^N+1) with N=r*N', put Y=X^r. Write a(X)=Σ_i X^i a_i(Y). For s(X)=s'(Y), a*s=Σ_i X^i(a_i*s')(Y), yielding r exact module components under **one** lower-ring secret. This is familiar ring switching/RLWE-to-MLWE, no new construction.
[TEST] N16,N'4,q65537,600 randomized ciphertexts,9600 modular coefficient-phase checks PASS. N32,N'8,q2^16, another 600 randomized ciphertexts,19200 modular coefficient-phase checks PASS.
[DERIVATION] Binary BatchBoot uses s=Σ_support X^j; ternary Ma instead has s=Σ_(+)X^j−Σ_(-)X^j. A naive unchanged BatchBoot exponent decryption computes the wrong phase for negative coefficients. Encrypting signs and adapting EMPmul might repair functionality, but changes ciphertext/key/noise type and costs.
[TEST] 1000 random signed key/convolution tests: exact sign-aware expansion PASS1000; naive binary-support-only expansion matches only 2/1000.

## Unconditional 128-bit keyspace necessity vs expected sparsity
For independent uniform ternary keys, number of possibilities is 3^N', brute-force search-space size log2|S|=N'log2 3 bits. At least 2^128 candidates requires N'>=81, forcing E[h]>=54. To attain even Boot4's expected h<=42, N'<=63, providing at most 3^63 ≈2^99.85 candidates, less than 128-bit direct key-search space. This necessary condition is NOT an RLWE security proof at N'>=81, not a lower bound on all possible changed secret distributions, and does not exclude rare low-h samples at larger N'.
At N'=1024/2048/4096: expected h≈683/1365/2731, respectively; for N'4096 vs Boot8 h34 the h-scaling ratio is 80.31x before signed-selector and key-conversion overhead. Sample means from 400 ternary keys per degree: 681.27/1365.53/2731.21. Exact log2 binomial tail Pr[h<=42] for N'=1024/2048/4096 is -1332.11/-2912.51/-6116.21, respectively (these are **not** cryptanalytic probabilities). Illustrative per-message EMPmul polynomial cost ratio in a N8192,N'4096,k2 deployment versus native Boot8 is ~80.4x using matching schematic kernels, NOT actual latency.

## Conditional guideline gate (don't conflate noise scales)
Ma Table1 page11: for *uniform ternary and Gaussian coefficient-domain sigma 3.19*, 128-bit guideline max log2 Q at N'=1024/2048/4096 is 26/53/106. Thus at Q2^64 the first listed guideline-compatible dimension is 4096 **under those assumptions**. BatchBoot's torus-normalized std values like 2^-15 are NOT directly the same noise measure; this is NOT a valid actual BatchBoot security estimate. Its published >128-bit sparse-key estimates cannot be transferred to a dense-subring key. True security/DFR/key transcript requires fresh estimator and proof.

## Decision
FAIL: direct substitution is not interface-compatible and loses h-based cost/entropy target. Positive algebraic module extraction is existing known technique. No actual 128-bit hybrid lattice estimate, no native encrypted Bench, no DFR or runtime claim, no new primitive.
STATUS FAIL_DIRECT_UNIFORM_TERNARY_SUBRING_TO_BATCHBOOT_SPARSE_SECRET_COMPOSITION.
RESULT: falsified one claim through paper reading, exact toy modQ and mod2^w tests, entropy necessity and mean-Hamming work.
NEXT_TEST B077 NOT STARTED: abandon *direct h-scaled substitution*, select ONE different interface able to evaluate dense/subring secret polynomial action without O(h) encrypted monomial steps. Prior-art gates Ma2025, BatchBoot2026, AmortBoot, Liu–Wang2023. Abort if merely existing ring switching or generic encrypted multiplication.
STATE_UPDATE NO: Existing findings/boot-STATE.md lists 187967 bytes but read returned {}; preserve it. SHIP unchanged.
LOCAL ARTIFACT: BOOT_B076_handoff.zip SHA256 bc2eb2f69f2d847e9851c2d96f6533ef003705b01e2bba817502b2f265366cf7 includes full detailed report, both scripts, JSON, logs and manifest. Main JSON SHA256 2f8a82378187026b992c36cad6cb94bb146d4996517284cf9b32e0d300704e86.