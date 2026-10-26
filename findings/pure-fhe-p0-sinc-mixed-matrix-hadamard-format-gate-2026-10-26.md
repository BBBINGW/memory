# PURE FHE P0 — SinC Batched MM × Native Hadamard Mixed-Operator Format Gate

**Date:** 2026-10-26 Asia/Singapore
**Stage:** `PURE-FHE-P0-PRESCOUT-06` (separate from BOOT/SHIP/CGS official numbering)
**STATUS:** `FAIL_FREE_SINC_HADAMARD / FAIL_GENERIC_DUAL_OPERATION_NOVELTY / OPEN_MATCHED_FORMAT_BRIDGE_COST`
**EVIDENCE:** FULL_MIRRORED_PDF_READ + EXACT_RING_COUNTEREXAMPLE + AUTHOR_EXPERIMENT_TABLE, not native FHE run, not original theorem or proposed scheme.
**CODEX:** `NOT_RUN`.
**STATE_UPDATE:** THIS_FINDING_ONLY. No change to root STATE.md or other tracks. Existing FHE×MPC malicious-bitsharing and FHE×ZK hoisted KS engineering candidate records remain parked/intact.

## G0 — Primary-source and prior-record provenance

Historical pure-FHE P0 previous stages PRESCOUT-01...05 archived in `findings/pure-fhe-p0-*.md`. Sparse LCR+AKS actual model PARKED; shaped rounding / focal units are source-blocked for latest full texts. Review of `findings/OPEN_RESEARCH_BRANCHES.md` and `findings/RESEARCH_PROGRAM_INTEGRATION_2026-10-15.md` confirms avoid resurrecting trivial subroutine/lazy relinearization or claiming known RLWE tricks as novelty.

**CRYPTO 2026** Jung Hee Cheon, Minsik Kang, Junho Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, ePrint `2025/1957`, https://eprint.iacr.org/2025/1957 ; proceedings confirmed on SNU https://snu.elsevierpure.com/en/publications/fast-batch-matrix-multiplication-in-ciphertexts/ and author https://mskang0503.github.io/publications/ . 32 physical-page `VERSION_UNVERIFIED` mirrored original text read by research MCP; SHA256 `ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a`. Relevant physical pages 3–7 (SinC encoding and new rectangular reduction), 11–17 (SinC/PPMM algorithm), 18–24 (batch CMT + rectangular algorithms), 25–28 (actual benchmark/security/accuracy setup and tables), 31–32 (SinC conversion and SinCBoot full reported results). **Mirror source text is not authenticated byte-equal to final CRYPTO proceedings.**

**CRYPTO 2026** Craig Gentry and Yongwoo Lee, *Fully Homomorphic Encryption for Matrix Arithmetic*, ePrint `2025/1935`, https://eprint.iacr.org/2025/1935 ; proceeding info https://doi.org/10.1007/978-3-032-35374-0_12 ; 27 physical-page mirror SHA256 `985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84`, VERSION_UNVERIFIED. Physical p16 §3.6 explicitly implements **native Hadamard** using ordinary ciphertext multiplication and `Switchsmall` key switch/relinearization; p22 Table2 reports 2.779s Hadamard, 11.582s CC matrix multiply on its **different** 16×M256(C), ring and CPU configuration. This ALREADY supports both native matrix multiplication and Hadamard with a specialized matrix ciphertext representation. No blanket novelty for `matrix+Hadamard FHE`.

**Further strongest prior art/competition:** Same Cheon/Kang/Lee authors list `Fast Batch Bootstrapping in CKKS` as ASIACRYPT 2026 (https://mskang0503.github.io/publications/). Current full text/precise SinC interoperability **NOT VERIFIED**, cannot infer this paper does or does not solve SinC↔slot conversion cost. Park Eurocrypt2025 2025/1935 references and Bae et al CRYPTO2024 CPMM already deliver PPMM reduction. Ordinary common subexpression reuse of CMT is not novel.

## ONE primary hypothesis, decisively falsified

`H_FREE_SINC_HADAMARD`: An RLWE ciphertext whose *SinC* plaintext encodes a batch of d×d matrices can use one native ciphertext-ciphertext multiplication `m(X)·u(X)` **directly** to implement elementwise Hadamard product of corresponding matrices, without a change in basis or special linear transform.

**Falsifier exact ring:** Work in `R=Z_17[X]/(X^4+1)`, `d=2,k=2,N=4`, and `Y=X²` with `Y²=-1`. The one-batch (k/2=1) SinC column-coefficient representation `Vec'(m)=(m0(Y),m1(Y))` is well-typed. Let m(X)=1+X and u(X)=1−X; these represent two coefficients (1,1) and (1,−1) in the X row dimension, with entries in subring R_k. The *coefficientwise desired* Hadamard is `h(X)=1−X`, whereas actual ring multiplication is `m(X)u(X)=1−X²=1−Y ≠ h(X)`. This is due to `X²=Y` **cross-row convolution**, not special behavior of TFHE or CKKS noise. One single direct ciphertext multiplication is **not** the Hadamard operation on the SinC matrix-coordinate representation. Three more independent Z_17 negacyclic multiply random-like controls were evaluated with JS and all showed inequality; exactly (m=[1,1,0,0],u=[1,16,0,0]) => product coeffs [1,0,16,0] vs Hadamard [1,16,0,0]. This is a minimal algebraic falsifier only; does not rule out algorithms using extra transforms or custom native scheme.

**Critical nuance:** SinC's `iDFT` over *Y*-coefficients DOES make multiplication across its **batch slots** componentwise: `iDFT(a_ℓ)·iDFT(b_ℓ)=iDFT(a_ℓ b_ℓ)` holds as a property in R_k. Our counterexample concerns mixing between the distinct **X-matrix-row coefficient positions** in R_N. Do not claim SinC batching fails or has a security bug. Authors never assert that a raw ring product equals matrix Hadamard.

## Full-system gate grounded in source performance

Author 2025/1957 p27 Table2 (S13b, N=8192 single-core Xeon Gold6542Y, 20 repetitions):
- `d=64, batch=128 complex matrices`: 0.199s **CPMM**, 0.912s **CCMM**, 15.6 and 15.7 measured accuracy bits, normal CCMM key 41.9MB, lightweight 0.79MB. These numbers are *batch* timings not per-matrix latencies. **Do not** promote the p3 older `1.3s` CCMM to definitive when p1 abstract/p27 Table2 say ~0.91s.
- p26 remarks lower SinC accuracy than authors' specific Bae/Park comparators due local small-ring slot encoding noise factor (pdf math is extracted ambiguously; avoid exact sqrt-vs-linear bound without rendered formula).
- p32 Table5, **DIFFERENT FTm parameter N=32768**, one-ciphertext SinC conversion and SinCBoot, restore 3 levels from0, reported:
```
k     Conversion time    SinCBoot time    Conversion accuracy SinCBoot accuracy
32    4.24s              1.55s           9.38bits            9.04bits
64    2.13s              1.73s           9.04bits            9.01bits
128   1.10s              1.89s           8.97bits            9.20bits
256   0.569s             2.34s           8.22bits            9.13bits
512   0.295s             3.45s           7.76bits            8.66bits
```
**Never compare these directly to S13b MM time to claim mixed-workload crossover, as different ring, levels, scale and precision.** A mixed operator full workload requires a matched dataset and parameterization, and n-column conversion cost and reuse must be concretely typed; one ciphertext experiment is not d-column MM conversion benchmark.
- p21 §5.3 already provides `lightweight CMT`: one master automorphism key and one relinearization key with online generation of dependent rotation keys; p32 Table6 provides time/memory tradeoff. A generic CMT-key caching proposal is already existing prior art.

## Interpretation / value gate

A real potential application bottleneck is **mixed workloads** with several SinC-batched PPMM-based CCMMs and intermixed elementwise nonlinear operations, custom activations or layer normalization. SinC strong arithmetic dimension X and batch dimension Y behave differently. A multi-operation **representation bridge** or native entrywise operation may be necessary and its time/precision/security dominates the full system. Gentry–Lee's newer matrix-native encoding has already solved the abstract `matrix multiplication+Hadamard` objective using a different setup, so a new contribution must show **quantified superiority** on a fixed small-matrix batched and nonlinear workload at equal N, 128-bit-estimate, true precision, key memory, and full conversion pipeline.

**Explicit nearest-future-source gate:** Authored 2026 `Fast Batch Bootstrapping in CKKS` by same SinC authors, ASIACRYPT2026, is listed but no compatible full theorem or code audited. Before novelty claim or system experiment, determine whether that paper already provides exact conversion/bootstrapping fusion in the relevant SinC pipeline. Its public author citation is NOT evidence that it does.

**P0 DECISION:** `PARK_FREE_SINC_HADAMARD`; no paper-level new scheme. Preserve a **bounded opportunity** in *matrix-operator interoperability*, but do NOT run many toy format transformations. Next cheap test: derive a single *matched workload* (e.g. SinC-encoded two CCMMs with one coordinatewise square between), enumerate d ciphertexts, conversions, precision and necessary keys; compare to Gentry–Lee native matrix scheme and SinC with explicit conversion, both with same logical matrices and target security. If latest fast batch CKKS bootstrap already avoids the expense, kill this opening. NO Codex until a source-faithful expected system gain or novel typed invariant survives.

`END_STATUS: FAIL_NAIVE_MIXED_OPERATOR / PRIOR_ART_MIXED_OPERATION_EXISTS`
`RESULT: SOURCE_CONVERSION_BOTTLENECK_MEASURABLE_BUT_UNMATCHED; ELEMENTARY_COUNTEREXAMPLE`
`NEXT_TEST: AUTHOR_NEWER_BATCH_BOOTSTRAP_SOURCE_GATE_OR_MATCHED_INTEROPERABILITY_COST`
`STATE_UPDATE: THIS_FINDING_ONLY; no root state or other line updates`.
