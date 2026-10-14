# HERDS H-HERDS-04 — Paper Table 3 Set V trace gadget differs from pinned author Go code



**Date**: 2026-10-14 Asia/Tokyo. Independent HERDS round 4, after H-HERDS-03. Read before write: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (parallel vFHE V24; READ ONLY), and findings/herds-2025-1804-Vprime-full-noise-worksheet-gate.md SHA e19a5613944e1a2a62d0eb68d773805f28075a26. Independent SHIP I226 READ ONLY. No global-state or upstream-code changes.



## ONE primary hypothesis / ONE source-level decisive test



**H-HERDS-04 [FALSIFIABLE]:** In the published author Go reference source, the built-in **32-party, 100-bit preset** `ParamsBinaryParty32` generates the actual *trace* switching keys with exactly the separate Table 3 Set V TRK gadget `(B_tr,d_tr)=(2^5,8)`, rather than reusing the BRK gadget `(2^9,4)`. Test by following the pinned preset -> `GenEvaluationKey` -> `GenTraceKey` -> actual evaluator Galois-key registration -> `TraceRLWEToRLevAssign`, and, crucially, verify the pinned `tfhe-go` library consumes the passed gadget. Only if source equality confirmed PASS.



## Precise primary source provenance [FACT]



- Binwu Xiang et al., *HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping*, EUROCRYPT 2026 / IACR ePrint **2025/1804**, https://eprint.iacr.org/2025/1804. Complete 46-physical-page Research MCP paper mirror SHA256 `c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7`, source revision d68d3723d26dc2978fcb8f0506946a6314eca0c9, **VERSION_UNVERIFIED** vs publisher. Physical **p27 Table 3** has Set V (k32, labelled λ100): n560, N2048, q2^64, beta normalized 1.2×10^-19, BRK base2^9/length4, **TRK base2^5/length8**, pk/rlk base2^4/length10, packed accumulator length d8. Physical pp16/18/19 and 40–42 contain Lemmas5–7 and approximation caveats. Paper PDF text extracted but not pixel-verified against publisher; the tabular numbers are clear. The 128-bit V-prime has n636, beta4.4×10^-16 but matching official Go preset is **not available** in the pinned repository; do not claim validated V-prime implementation.



- Public author Go repository **`SNUCP/mktfhe-parallel-go@e3b8f56d92a5bc535e9b2f0853f4b7135dcbe53a`** (commit pinned from native GitHub source search, not inferred HEAD). `mktfhe/params_list.go`, blob SHA `8e18f4dea1c438109b6d6b7a7c68350796089d6f`, **lines 157–193**: `ParamsBinaryParty32` has n560, GLWEStdDev 1.2e-19, `BlindRotateParameters {Base:1<<9,Level:4}`, `AccumulatorParameters {Base:1<<5,Level:8}`, `RelinKeyParameters {Base:1<<4,Level:10}`. The **accumulator gadget**, `(2^5,8)`, happens to equal the paper's reported TRK gadget, but it is NOT passed to trace key generation. Repo has only 100-bit built-in 2/4/8/16/32 presets; no Table 3 I-prime--V-prime built-in entries visible in this pinned complete `params_list.go`.

- `mktfhe/bootstrap_keygen.go` blob SHA `50f8832061ceadfb6ec2e4c00b6891f603847f7b`, `GenEvaluationKey` lines 14–19 calls `GenTraceKey()`, and **line 73** explicitly calls `GenGLWEKeySwitchKey(skAut, e.Parameters.BlindRotateParameters())`. Thus the actual Galois trace key uses the BRK gadget (2^9,4), not accumulator gadget (2^5,8).

- `mktfhe/evaluator.go` lines 102–109 registers all `evk[i].TraceKey[j]` as BFV `GaloisKeys`; `mktfhe/bootstrap.go` lines 136–150 `TraceRLWEToRLevAssign` calls `SingleKeyBFVEvaluators[idx].PermuteAssign` for each trace stage. Therefore these exact keys lie on the actual decoding path, not dead code.

- `go.mod` blob SHA `fbf63e1d1affbde922d269b09d5fff2b732772a4` requires `github.com/sp301415/tfhe-go v0.6.0`. In the same dependency at **ref v0.6.0**, `tfhe/keyswitch_keygen.go` blob SHA `85aec596287b7914a227569a7736cbded02cf7c4` lines 15–20, `GenGLWEKeySwitchKey(skIn,gadgetParams)` invokes `NewGLWEKeySwitchKey(e.Parameters,len(skIn.Value),gadgetParams)` and encrypts into that key; the supplied gadget argument is **actually used**.



## Noise unit gate [FACT, narrowly scoped]



Go `mktfhe/params.go` blob SHA `7b2f10e449d4c95c67beaef1b88b1fbe66b193d0` documents `GLWEStdDev` as **normalized** and `GLWEStdDevQ` as `GLWEStdDev * Q`. `mktfhe/bootstrap_keygen.go` line 53 calls `GaussianSampler.SamplePolyAssign(e.Parameters.GLWEStdDevQ(),...)` for the CRS pk, and `mktfhe/glwe_enc.go` + `mktfhe/fourier_glwe_enc.go` also call `SamplePolyAddAssign(GLWEStdDevQ())` for uni/evaluation keys. Thus **H03's beta*q coefficient-noise-unit assumption is consistent with these checked sample-generation paths**; this does not establish every sampler's exact distribution/rounding or prove Lemma7's approximate variance.



## ONE minimal impact sanity check, not a new hypothesis [DERIVATION/COMPUTED]



Using the SAME transcribed Lemma5–7 formulas and same source Table3 Set V k32/n560/N2048/q=2^64/dpacked8/ell2/beta=1.2e-19, vary ONLY TRK `(B_tr,d_tr)` while holding BRK `(2^9,4)` and hybrid `(2^4,10)` fixed. Noise unit sigma_key = beta*q ≈2.213609288845146 coefficient units:

- Paper Table3 trace `(2^5,8)`: modeled sigma_ks≈**4.38353264e8**, final 6sigma_out/q≈**0.03597613906468846736**.

- Pinned author Go source trace `(2^9,4)`: modeled sigma_ks≈**7.01365222e9** (≈16×), final 6sigma_out/q≈**0.03664147810521434576** (≈1.01849× final sigma).

- Both modeled ratios are less than 1/16=0.0625. This is an **approximate source-formula worksheet**, NOT a measured noise statistic, output-D FR proof, correctness failure, security hardness estimate or proof that the paper's timings used exactly this commit. Trace gadget row count halves (d4 vs d8), but actual key bytes, latency and trade-off have NOT been measured.



Reproducible independently executed Python Decimal script `/mnt/data/herds_H04_code_paper_trace_gadget_gate.py`, SHA256 `255917f57eef35187355641661acff5d9b104e41f5de3c933a0cd43d14c4800a`; output `/mnt/data/herds_H04_code_paper_trace_gadget_results.json`, SHA256 `845e347c3d65c0174cfe5e7cc518bacfc1d2b9495483ad5b5ca0eeaf53e9aff1`. Exact source links: https://github.com/SNUCP/mktfhe-parallel-go/blob/e3b8f56d92a5bc535e9b2f0853f4b7135dcbe53a/mktfhe/bootstrap_keygen.go#L66-L75 , https://github.com/SNUCP/mktfhe-parallel-go/blob/e3b8f56d92a5bc535e9b2f0853f4b7135dcbe53a/mktfhe/params_list.go#L157-L193 ; dependency https://github.com/sp301415/tfhe-go/blob/v0.6.0/tfhe/keyswitch_keygen.go .



## Research verdict



**STATUS: FAIL H-HERDS-04** exact paper Table3 vs pinned code TRK parity. **PASS concrete source-call-chain mismatch**; **PASS narrow normalized→coefficient noise-unit audit**. **UNCLEAR** whether change is intentional implementation tuning, stale code compared to published paper, relevant to published benchmark revision, formal 128-bit presets and actual DFR. Source code branch is 100-bit only; **do not project mismatch onto 128-bit V-prime as a confirmed software defect**.

**RESULT:** Set V's claimed trace `(B=2^5,d=8)` equals Go's *accumulator* parameters while actual `GenTraceKey()` receives *BlindRotate* `(B=2^9,d=4)`. This changes noise model materially at trace operation but barely changes the approximate final output noise for k32 in this one model; neither setting fails 6σ/q<1/16. The discrepancy is a **reproducibility/parameter-reporting question**, not a cryptanalytic attack or demonstrated proof gap. Generic 'mismatch => paper wrong' claim is unjustified.

**NEXT_ACTION:** Seek publication-matched author implementation/tag/commit, exact benchmark configuration and 128-bit preset provenance. If available, do ONE real `GenTraceKey` parameter introspection/DFR evaluation at Set V and Table3 intended TRK, controlling random seed/backend; check whether reported Table3 values reflect code or a different branch. Alternatively present the precise discrepancy to maintainers as a question only after PI approval. If no tag/runner, HUMAN_REVIEW/PARK rather than more static noise worksheets. Preserve global I192/vFHE and SHIP state. **NOVELTY NOT VERIFIED**.

**STATE_UPDATE: YES** independent HERDS finding only; global/SHIP/vFHE untouched.