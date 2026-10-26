# Pure FHE P0 — SinC↔Slot Mixed-Operator Roundtrip / Fast Batch Bootstrapping Prior-Art Gate

Date 2026-10-26, Asia/Singapore. **STAGE: PURE-FHE-P0-PRESCOUT-07**, separate from SHIP/BOOT/CGS official iterations.
**STATUS: FAIL_GENERIC_FUSED_CONVERSION_NOVELTY / PASS_SOURCE_COST_INTERFACE / SOURCE_BLOCKED_AUTHOR_2026_FAST_BATCHBOOT**.
PI-selected independent P0 pure-FHE research; previous `findings/pure-fhe-p0-sinc-mixed-matrix-hadamard-format-gate-2026-10-26.md` explicitly allowed ONE bounded source and cost follow-up. No Codex, GPU, codebase writes, running FHE or official branch state update.

## Read-before-write and primary source

1. Jung Hee Cheon, Minsik Kang, Junho Lee, **Fast Batch Matrix Multiplication in Ciphertexts**, CRYPTO 2026, https://eprint.iacr.org/2025/1957 ; 32 physical-page full text cached, PDF SHA256 `ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a`, mirror **VERSION_UNVERIFIED**. **Physical pp12–14 §3.1–3.2**: Theorem1 gives `<z>_SinC=<S_{N←k} z>_slot` with partial DFT and Remark1 `S2C=SinC∘CinS`; §3.2 explicitly proposes **SinCBoot=HalfBoot+homomorphic S_{k←1}**, outputs *standard slot encoding* from SinC after bootstrapping, and claims format conversion can be fused with existing S2C (no ADDITIONAL encoding-conversion computation in the specified bootstrap, NOT zero bootstrap latency). p14 author states one can then evaluate nonlinear functions under slot encoding.
2. Same PI-independent full text pp31–32 Appendix B **Table4 FTm** `log2 N=15, log2 Δ=28, log2 Qbase=38, four 28-bit multiplication primes, QP745, dnum4, hwt256`. Authors benchmark *each operation separately* on one ciphertext: `SinCBoot` lifts ciphertext level 0→3; `Conversion` slot→SinC consumes from level 2→1. FTm deliberately low precision, *separate operation* accuracy around 7.76–9.38 bits. Table5 timings transcribed exactly below.
3. Same original p27 **Table2 S13b** `N=8192`, d=64, batch=128: CPMM 0.199s, CCMM 0.912s, CCMM ~15.7bits. **DIFFERENT parameter set**, cannot compare MM 0.912s directly with FTm conversions or assert end-to-end speedup/slowdown.
4. Craig Gentry and Yongwoo Lee, **Fully Homomorphic Encryption for Matrix Arithmetic**, CRYPTO 2026 ePrint 2025/1935, mirror 27 physical pages SHA256 `985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84` VERSION_UNVERIFIED. p16 §3.6 already has native matrix Hadamard through ordinary polynomial ct×ct with `Switchsmall`; no generic novelty for matrix + Hadamard support.
5. Eric Crockett, Craig Gentry, Hyojun Kim, Yeongmin Lee, Yongwoo Lee, **Efficient Bootstrapping in Fully Homomorphic Encryption for Matrix Arithmetic**, CRYPTO 2026, ePrint **2026/956**, official landing https://eprint.iacr.org/2026/956, DOI https://doi.org/10.1007/978-3-032-35374-0_16; public published abstract says CtS/StC formulated as native ciphertext–plaintext matrix multiplications, **linear transformations 20.1%** of bootstrapping vs 62.0–72.8% for comparison, amortized CtS 2.62x versus Lattigo. THIS IS **Gentry–Lee matrix scheme**, NOT SinC CKKS, numbers not SinC costs. **Full PDF 2026/956 unavailable** to Research MCP 2026-10-26 (official HTTP403, no authenticated matching mirror); abstract-level competition only.
6. Jung Hee Cheon, Minsik Kang, Junho Lee, **Fast Batch Bootstrapping in CKKS**, **ASIACRYPT 2026 accepted**, confirmed author's up-to-date publication page https://mskang0503.github.io/publications/ and blog https://mskang0503.github.io/ ; repeated targeted web author-title/ePrint/abstract/ArXiv lookup yielded **NO VERIFIED FULL PAPER OR ALGORITHM ID** as of 2026-10-26. DO NOT claim newest author work already solves or fails SinC↔slot conversion. Explicit source gap should be registered.
7. Related previous prescout `P0-PRESCOUT-06` showed naive SinC coefficientwise Hadamard fails: `(1+X)(1-X)=1-X²` in Z17[X]/(X⁴+1), not coefficientwise 1-X. Therefore mixed workload needs representation change or custom nonlinear representation (which may exist in stronger papers), not a free native ring product.

## ONE primary source-check hypothesis and cheapest decisive typed/cost check

**H:** Combining already-published SinCBoot with a slotwise nonlinear activation gives a **zero-extra-cost reusable SinC↔slot interface** for the sequence `SinC MM→f(pointwise)→SinC MM` without any further return-to-SinC conversion, level consumption or nontrivial ciphertext work, hence simply 'fusing conversion with bootstrapping' is a novel new solution.

**Falsifier from exact source types and Table5**:
```
SinC ct @ level 0
    ↓ SinCBoot (source §3.2)
Slot ct @ level 3
    ↓ f(x)=x² + CKKS rescale (one level, conditional)
Slot ct @ level 2
    ↓ source's separately measured Slot→SinC conversion
SinC ct @ level 1
    ↓ next CCMM in SinC domain (additional level budget required)
```
Source SinCBoot is directional SinC→Slot, **not** Slot→SinC. Thus there is necessarily *a separate return transformation* for this particular unchanged SinC MM source interface. It already exists in the original paper. Opposite-direction conversion cannot be omitted merely because forward path was fused into bootstrapping.

**Reported FTm times (individual single-ciphertext operations)**:
| k | SinCBoot (s) | Slot→SinC Conv (s) | sum (s) | SinCBoot accuracy bit | Conv accuracy bit |
|---:|---:|---:|---:|---:|---:|
| 32 | 1.55 | 4.24 | 5.79 | 9.04 | 9.38 |
| 64 | 1.73 | 2.13 | 3.86 | 9.01 | 9.04 |
| 128 | 1.89 | 1.10 | 2.99 | 9.20 | 8.97 |
| 256 | 2.34 | 0.569 | 2.909 | 9.13 | 8.22 |
| 512 | 3.45 | 0.295 | 3.745 | 8.66 | 7.76 |

`T_two_ops(k)=T_SinCBoot(k)+T_Conv(k)` is an **arithmetic sum of two individually benchmarked distinct stages, at the same FTm source parameter set**, NOT a measured sequential paired benchmark. A true MM→activation→MM pipeline requires (a) correct number d of SinC matrix ciphertext columns, (b) activation mult/relin/rescale with sufficient levels and scale, (c) conversion scheduling/batching and possibly shared bootstrapping keys, (d) precision after sequential stages, not min of independent accuracies, (e) total memory/security/communication, and (f) comparison against native matrix FHE same workload. Full pipeline may amortize shared transformations or fuse more steps, hence no lower bound on ALL possible new methods is claimed.

**Result:** `FAIL_ZERO_EXTRA_COST_AND_NOVEL_FUSION` for **straight source pipeline**, not a generic impossibility of all native hybrid representations. The source *already contains* the forward-fused format conversion and both directional conversion benchmarks. A generic 'SinCBoot then slot activation then convert back' is a direct composition of published operations, engineering at best. Existing GL native Hadamard plus GL bootstrapping also closes generic 'dual-op+matrix-native bootstrap' novelty, although no matched same-parameter benchmark exists.

## Decision and future ROI

The newest ASIACRYPT Fast Batch Bootstrapping paper remains **SOURCE_BLOCKED**; cannot infer its solution scope or headroom from title alone. Independent strong competing 2026/956 matrix-bootstrap published abstract explicitly shifts bottleneck from linear transformations to EvalMod, so simplistic CtS/StC-as-PPMM fusion is known in a different scheme.

**PARK** current generic SinC↔slot hybrid conversion research for *cryptographic originality*. Retain as engineering benchmark candidate ONLY if PI requests, with pinned FTm and correct level/precision, d-column scaling and native-Gentry–Lee comparison. No Codex task needed. To reopen theoretical contribution, require a NEW typed invariant e.g. direct nonlinearity in SinC at low switching complexity (beyond known native GL Hadamard) OR strict same-parameter end-to-end improvement with a previously unknown packing/bootstrapping mechanism. No repeated toy re-indexing.

**Next P0:** switch to a different source-complete pure-FHE primitive with author cost table and genuinely unaddressed bottleneck; optionally retrieve `Fast Batch Bootstrapping in CKKS` final preprint when it becomes publicly accessible, but do not block broad P0 research on it.

## End

`STATUS: FAIL_GENERIC_FUSION_NOVELTY / SOURCE_BLOCKED_NEWER_AUTHOR_PAPER`
`RESULT: SINCBOOT_IS_ALREADY_FUSED; RETURN_CONVERSION_COST_EXPLICIT_IN_APPENDIX`
`NEXT_TEST: DIFFERENT_SOURCE_COMPLETE_PURE_FHE_MECHANISM / OR LATER FAST_BATCHBOOT_FULL_TEXT`
`EVIDENCE: 2025_1957_FULL_SOURCE_READ + 2025_1935_FULL_SOURCE_READ + 2026_956_PUBLISHED_ABSTRACT + AUTHOR_PUBLICATION_ONLY`
`NOVELTY: NOT_ESTABLISHED`; `STATE_UPDATE: THIS_FINDING_ONLY`; `CODEX: NOT_RUN`.
