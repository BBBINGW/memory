# PURE FHE P0 — RevHomTrace Noise-Improvement vs System-Latency Headroom

Date 2026-10-26 (Asia/Singapore) | **PURE-FHE-P0-PRESCOUT-08**, independent from BOOT/SHIP/CGS series. User PI chose problem-first broad pure FHE P0. No Codex, no native experiments, no old-state mutations.

**STATUS: FAIL_TRACE_ONLY_2X_LATENCY_GOAL / PASS_PRIMARY_SOURCE_AND_IMPLEMENTATION / PARK_ONLY_TRACE_REDESIGN**

## G0 / source provenance

Historical findings in `findings/boot-B075-shared-selector-interleaved-ap-packing-cost-gate.md` and `findings/boot-B076-batchboot-subring-hamming-gate.md` already considered TFHE BatchBoot shared-selector packing and dense-secret direct transplant; they failed to show improved native arithmetic/security-matched gains. We did not resume BOOT or recycle BatchBoot hoisting/sparse packing as novelty.

New external source, not found with GitHub Notes repository text search on `RevHomTrace` or `2025/1088` before this study:

1. Kang Hoon Lee and Ji Won Yoon, **Homomorphic Field Trace Revisited: Breaking the Cubic Noise Barrier**, IACR TCHES 2026(1):105–134, IACR ePrint 2025/1088, https://eprint.iacr.org/2025/1088 ; DOI https://doi.org/10.46586/tches.v2026.i1.105-134 . Research MCP cached 30-page full mirrored PDF, SHA256 `4f1033580542c56baa8a493aab178681082df768cd3446cc4470bc75b49589a9`, **VERSION_UNVERIFIED** (not byte-authenticated against TCHES journal version), `2026-10-26`. Physical pp10–15 Alg5/Theorem4/FFT-noise analysis; p15 Table3; pp16–18 Table4, application; pp18–20 Algorithms and Table6 of MS-PackLWEs.
2. Author implementation `https://github.com/Stirling75/RevHomTrace`, read live GitHub:
  `README.md` blob `a85b1cab58e1b69cc2ac4e22f7af3801bc3bee3b`: code includes `src/automorphism_rev.rs`, `src/mod_switch_rev.rs`, `src/ggsw_conv_rev.rs`, `src/glwe_conv_rev.rs`, real Rust benches. `src/automorphism_rev.rs` blob `e760c3f4acfe7a590798d3a0d93512fe12c7a7e8`: `revtrace_partial_assign` loops `for i in (1..=(log_polynomial_size-log_n)).rev()`, computes Galois elt `k=polynomial_size/(1<<(i-1))+1`, invokes `glwe_preprocessing_moddown_1bit(&mut out)` **per stage**, then `auto_key.auto` and ciphertext add. `src/mod_switch_rev.rs` blob `50d8fead98e2cf0440771b8252a9fb2e965096bf` implements 1-bit modulus down and raise. This verifies the *operation order*, not the published noise bound independently.
3. **BatchBoot**, USENIX Security 2026, full public author proceedings PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf (20 pp); P3–P7 Algorithms 2–3 and Lemma 4.2 explicitly already include FFT/automorphism sharing and sparse degree reduction. We visually inspected source pp4 and8 by web PDF screenshots in this session. Prior local BOOT B075/B076 already combined with alternatives; no new proposal to transplant sparse secrets or hoist again.
4. Directly competing functional-bootstrapping recent literature includes `Decoupled TFHE-type Functional Bootstrapping` CCS 2026 **publication announced** and `Homomorphic Field Trace Revisited` full author source. Since Decoupled details not verified, no novelty claim involving it.

## WHAT PAPER ALREADY SOLVES

Old `PreHomTrace` modswitches once by factor N before HomTrace, induces large variance bound O(N³) because early noise is amplified by subsequent trace stages. `RevHomTrace` **reverses automorphism order** and invokes `ModRaise_{q/2→q}∘ModSwitch_{q→q/2}` **at each stage**; Theorem4 proves
`Var(Cout) <= Var(Cin) + 4 log2(N) V_MS + log2(N) V_Auto`, O(N log N) when both per-op variances O(N) as specified. It *does not imply measured error is that upper bound*.
- p15 Table3 for N2048: INT_LHE_64 PreHomTrace 795.7us / 33.58 average-noise bits vs Rev 809.0us /28.99 bits; INT_LHE_256 Pre 847.6us/31.03bits vs Rev867.8us/26.49bits; author reports 1000 zero-encryption experiments, max-noise differences also substantial. The code and statistics are authors', NOT rerun locally.
- p17 Table4 shows HP-LHE complete refresh+GLev-to-GGSW conversion, and author also tries the next obvious noise-headroom→deeper PBS params (“RevHom.+Tweak”), i.e. simply spend freed noise budget on changing PBS gadget is already prior art in this paper.

## ONE primary H and cheapest decisive test

**H_TRACE_2X:** For the full high-precision circuit bootstrapping implementations reported by Lee–Yoon, *optimizing only the Homomorphic Trace/Conversion path*, without changing any PBSManyLUT/Refresh cost, can produce a **>=2x end-to-end latency gain**.

**Falsifier:** Apply Amdahl to exact p17 **Table4**, treating **ENTIRE Conversion time** as removable (extremely optimistic; true HomTrace is only one subset of Conversion). Let T=T_refresh+T_conv. Even a hypothetical zero-time Conversion cannot beat `Smax=T/T_refresh`.

| Param | δ | τ | Refresh (ms) | Conversion (ms) | Total (ms) | Conversion fraction | Absolute Smax zero Conversion |
|---|---:|---:|---:|---:|---:|---:|---:|
| INT_LHE_64 | 6 | 1 | 146.45 | 22.24 | 168.69 | 13.18% | 1.1519× |
| INT_LHE_64 | 6 | 2 | 74.31 | 22.25 | 96.56 | 23.04% | 1.2994× |
| INT_LHE_256 | 8 | 1 | 274.70 | 63.48 | 338.18 | 18.77% | 1.2311× |
| INT_LHE_256 | 8 | 2 | 139.59 | 63.47 | 203.06 | 31.26% | 1.4547× |

Example `203.06/(139.59+0.5·63.47)=1.1852×` for **halving ENTIRE Conversion**. In no shown configuration can trace-only improvement reach 2x even by assuming 100% removal of Conversion. This is a **numerical static falsifier from one author's fixed CPU/parameter workload**, not a universal crypto complexity lower bound, not a statement about throughput, new params, failures, quality or varying total CBS depth. The error improvements from Rev can affect permissible depth/parameters and whole-system workloads independently; paper already exploits a version of this in RevHom.+Tweak.

**RESULT: FAIL_TRACE_ONLY_2X_HEADROOM.** The observed unoptimized major latency fraction is the earlier `Refresh` / PBSManyLUT side, particularly INT_LHE_64; optimizing it might be high leverage, but the original paper **already changes its gadget parameters** as a response to new noise headroom. Don't claim generic PBS-gadget tuning as novel. No observed novel constructive protocol.

## Reframe / future options

`PARK` further trace-only latency variants after RevHomTrace under these fixed workloads. Saving FFTs, moving modulus switches to one global preprocessing, raising the ring size, or changing the stage order toward source PreHomTrace each has strong prior-art/known correctness-noise obstruction; *not* proposed as new methods.

Any new mechanism in this family must improve **cross-stage** PBSManyLUT+Conversion interface at matched post-bootstrapping CMux depth, same noise/DFR/security, RLWE degree, key memory, and full latency — e.g., reduce number of PBSManyLUT refreshes/arity independent of their gadget parameter alone — and check published EP-CBS/BATCHCBOOT/Decoupled TFHE-type FB/other author techniques. No evidence currently that this goal is an unoccupied contribution.

**Next broad P0 source gate:** Prioritize a distinct, source-complete operation with a *whole-system* cost that has more than a 1.45x optimistic saving envelope or a truly missing correctness/security interface. If pursuing CBS, first find an independent speed+depth improvement not reducible to published RevHomTrace + PBS gadget retune. No native experiments/Codex while source comparison and genuine mechanism absent.

**End:** `STATUS=FAIL_TRACE_ONLY_2X_HEADROOM/PARK_TRACE_ONLY`; `RESULT=AUTHOR_ALGORITHM_CODE_VERIFIED + EXACT_AMDAHL_GATE`; `NOVELTY=NOT_ESTABLISHED`; `NEXT_TEST=DIFFERENT_FHE_PRIMITIVE_OR_TRUE_CROSS_STAGE_CBS_INTERFACE`; `STATE_UPDATE=THIS_FINDING_ONLY`; `CODEX=NOT_RUN`.
