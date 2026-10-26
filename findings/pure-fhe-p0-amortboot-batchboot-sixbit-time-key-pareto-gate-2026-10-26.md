# Pure FHE P0 — AmortBoot vs BatchBoot: Matched 6-bit Time–Key Pareto Falsification

**2026-10-26 Asia/Singapore | PURE-FHE-P0-PRESCOUT-10 | NOT A BOOT ITERATION**
**STATUS: FAIL_UNIFORM_TIME_AND_BSK_PARETO / NO_NEW_ALGORITHM / PARK_NAIVE_AMORTBOOT_TUNING**
**Evidence:** cached 2025/686 full PDF (VERSION_UNVERIFIED), officially published USENIX 2026 original author prepublication PDF (20p, PDF visually checked), numerical source-grounded comparison. NO native experiments/Codex; no security proof or implementation. PI retains choices.
**Source and provenance:**
1. Antonio Guimarães, Hilder V. L. Pereira, *Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead*, CCS 2025, ePrint 2025/686 `https://eprint.iacr.org/2025/686`, DOI 10.1145/3719027.3765181, official https://antonioguimaraes.org/publication/guimaraes-fast-2025/ ; original author code `https://github.com/antoniocgj/Fast-Amortized-Bootstrapping`. GitHub Notes acquired mirrored **34-physical-page PDF** SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335` version UNVERIFIED. Physical pp10–12 Alg1/Lemma3.1 MPmul, pp13–17 Algorithms2–4 chained decryption, pp20–22 Section6.2 rejection sampling, pp23–27 Tables3–6 author benchmarks, and physical pp25–27 **key-size caveat**. Direct official currently indexed ePrint PDF snippet has a different Table5 than the cached historical 34p mirror; therefore **do not compare numbers from these paper versions as though they were identical or final**.
2. Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026; official paper `https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf`, conference `https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao`. Original **20p official author PDF**: physical p2 (§1.2) FFT-sharing/multibit CMux/sparse RLWE→MLWE, p8 Algorithm3, **physical p12 (zero-index web screenshot 11) Table4** paired measurements on same Xeon Gold6258R @ 2.70GHz with 32GB RAM, single-thread, using AmortBoot code as their comparator. This table is our **ONE self-consistent numerical baseline**, not mixed with 2025/686 mirror. USENIX report asserts up-to 2.4× versus CCS2025 predecessor, not all bit widths.
3. Historical relevant negative constructions: `findings/boot-B075-shared-selector-interleaved-ap-packing-cost-gate.md` and `findings/boot-B076-batchboot-subring-hamming-gate.md` previously falsified no-net-arithmetic doubled-ring shared-selector and naive binary→ternary dense-subring sparse-key security/performance. Also older Boot portfolio has explored many TFHE/BatchBoot variations; do not claim FFT hoisting, batched CMux, simple key shrinking, or sparse packing are new. No BOOT files edited.

## One primary falsifiable claim / cheapest decisive test

**H_UNIFORM_PARETO:** After BatchBoot's published improvements over AmortBoot, BatchBoot weakly dominates AmortBoot in *both* amortized per-message runtime and displayed Bootstrapping Key memory **at every tested precision** (2,4,6,8 bits), with a significant speed improvement for each configuration.

**Minimal decisive test:** Pair exactly the corresponding `AmortBoot Bootk` and `BatchBoot Bootk` rows in the **same** author's USENIX2026 Table4, preserving batch n and output precision, reported failure bound and author machine. Evaluate `T_A/T_B` and `K_B/K_A`. Do not compare to current standalone AmortBoot author's differently revised PDF Table5.

| Output bits | Messages | Reported DFR | Amort ms/msg | Batch ms/msg | Batch speedup | Amort BSK MB | Batch BSK MB | BSK multiple |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 2 | 2048 | 2^-120 | 8.09 | 3.57 | 2.266× | 17.1 | 59.6 | 3.485× |
| 4 | 2048 | 2^-94 | 8.65 | 3.60 | 2.403× | 18.4 | 64.1 | 3.484× |
| 6 | 4096 | 2^-64 | 8.92 | 8.43 | 1.058× | 18.6 | 120.1 | 6.457× |
| 8 | 4096 | 2^-62 | 57.34 | 25.11 | 2.284× | 76.6 | 205.3 | 2.680× |

Concrete 6-bit test: `8.92/8.43=1.058125...` i.e. **5.49% time saved** vs displayed BSK **120.1/18.6=6.45699×**, for same messages (4096), nominal tested DFR (2^-64), author-chosen security constraints, hardware and reported workload. Under **64 MB *BSK-only*** memory cap, AmortBoot's displayed 6-bit BSK fits, BatchBoot 6bit BSK does not; **does not imply either full program fits in 64MB** because repacking keys, runtime buffers and other KSKs are excluded/unclear. All tested BatchBoot points have larger displayed BSKs, hence no `uniform weak Pareto dominance` in the pair of displayed (runtime, BSK) dimensions. Even for high-speed 2/4/8 bit settings there is a nontrivial memory price.

**FAIL H_UNIFORM_PARETO**. This is a source-level Pareto/capacity observation, not a new cryptographic theorem and not an assertion the authors promised Pareto dominance. The `significant speed benefit at every precision` clause is also contradicted in the 6-bit configuration. BatchBoot is **not worse overall**—it offers speed-performance tradeoffs and notably new functionalities; standard Pareto dominance fails because keys larger.

## More severe, separately source-explicit memory caveat

2025/686 older mirror p25 Table5 displays Bootstrapping Key ~17–80MB (depending on setting) and at pp26–27 §7.2 explicitly reports **traditional repacking KSK 128MB to 2GB**. Source footnote specifies table Bootstrapping Key includes automorphism keys **within bootstrapping**, not *external* key switching for repacking. Authors already propose their own packed key method but state higher computation cost and suggest RLWE Conversion or Partial LWE for further key shrinkage (existing primitives, NOT OUR novelty). Thus comparing just displayed BSK columns is not a complete end-to-end peak memory or key material comparison. The USENIX paper also reports ~360MB peak memory in a specific 2/4-bit run, showing measured peak memory can exceed the listed BSK. Need source-aligned **all-keys and peak RSS** for any real engineering claim.

## Security, correctness and novelty gates

- Comparison is within same USENIX experimental reporting, same *nominal* DFR. The parameter sets/secrets/actual lattice hardness estimates differ by publication-specific tuning; we **did not re-estimate 128-bit security** nor read each key transcript. Do not call it cryptographically proof-equivalent solely due matching printed DFR.
- `B` bound on private sparse-index gaps in 2025/686 §6.2 is enforced by rejection sampling, *with estimated loss δ in security bits*; changing per-gap public runtime schedules can expose private support and invalidate original security. Thus naive gap-adaptive branching is not automatically valid/new. Source already handles B and rejection sampling; BOOT old lines studied keys. No concrete gap optimization in this iteration.
- BatchBoot already applies multi-bit CMux and FFT/automorphism reuse, plus sparse RTM extraction; any `mix known radix schedule` is at best tuning without a new invariant. The main available 6-bit improvement headroom is relative to faster modern BatchBoot, not historical AmortBoot.
- Caution alternative costs: whole-system batch performance depends on cold key loading, key-RAM cap, more than one amortized batch and memory bandwidth, throughput, peak RSS, packing cost, DFR and actual secret security. Bootstrapping-only BSK memory is insufficient for a speed×memory publication claim.

## G1 decision / conditional next concept

**PARK naïve AmortBoot tuning and its direct FFT-key composition.** 2026 BatchBoot supersedes key subroutines and historical BOOT-B075/B076 has audited obvious mixed-primitive ideas. A specific documented **engineering/dataflow tension** survives: at 6bits, moving from 18.6 MB AmortBoot BSK to 120.1 MB BatchBoot BSK returns only ~5.5% time gain. This may matter for edge-memory constrained deployment and evaluation-key storage research, but a new method must address it by a distinct representation for multi-bit selectors/FFT-domain key precomputation with full noise/DFR, same security and actual memory. No current construction or guaranteed key compression.
- **Do not authorize Codex** on this bare headroom. It is too close to prior BOOT and SHIP optimizations.
- Next high-value P0 should read a **different newest full source** with an author-identified bottleneck, not do incremental scheme mixing or parameter scans. Consider a theorem, functional/forward error lower bound or computational primitive with proof-worthy mechanics, but no claim before evidence.
- Preserve user-requested prior parked engineering candidates FHE×MPC bitsharing and FHE×ZK hoisted KS independently.

## End

`STATUS: FAIL_UNIFORM_PARETO / NO_CONSTRUCTION`
`RESULT: SOURCE_MATCHED_6BIT_TIME_KEY_TRADEOFF + MEM_ACCOUNTING_WARNING`
`NOVELTY: NOT_ESTABLISHED`
`NEXT_TEST: NEW_SOURCE_COMPLETE_PURE_FHE_STRUCTURAL_PROBLEM_WITH_DECISIVE_INVARIANT`
`CODEX: NOT_RUN; STATE_UPDATE: THIS_FINDING_ONLY; NO_ROOT_STATE_MODIFIED`
