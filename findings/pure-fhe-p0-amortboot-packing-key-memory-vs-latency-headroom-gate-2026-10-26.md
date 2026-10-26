# PURE FHE P0 — AmortBoot Packing-Key Memory vs End-to-End Latency Gate

**Date** 2026-10-26 (Asia/Singapore)
**Stage:** `PURE-FHE-P0-PRESCOUT-10` (independent, NOT BOOT/SHIP/CGS official series).
**STATUS:** `FAIL_PACKING_ONLY_2X_SPEED / PASS_PACKING_KEY_MEMORY_BOTTLENECK / PARK_LOW_NOVELTY_MEMORY_COMPOSITION`.
**EVIDENCE:** complete 34-page parsed ePrint MIRROR VERSION_UNVERIFIED + official CCS2025 publication + open author code repository + stronger USENIX2026 source; derivation is Amdahl bound from author-reported component fraction; NO new crypto construction / native run.
**CODEX:** `NOT_RUN`; **STATE_UPDATE:** THIS_NOTE_ONLY.

## First-party primary sources read

1. Antonio Guimarães, Hilder V. L. Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025 pp2967–2981, https://eprint.iacr.org/2025/686 ; official conference DOI https://doi.org/10.1145/3719027.3765181 ; full ePrint mirror acquired via GitHub Notes Research MCP, **PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335, 34 physical pages, VERSION_UNVERIFIED**. Physical p5 MPmul innovation, pp12–17 Algorithms 1–4, pp18–19 Packing KeySwitch Algorithm5 and Table2, pp20–21 Algorithm6 + Lemma6.1, pp22–24 selective low-HW parameters and security/rejection δ, pp25–27 Tables5/6, packing KEY footprint & future-work discussion.
2. Author code https://github.com/antoniocgj/Fast-Amortized-Bootstrapping (public C/MOSFHET PoC and build, author confirmed). No native compilation or raw time rerun.
3. Stronger later paper **BatchBoot**, USENIX Security 2026, https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao ; officially hosted author PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf, PDF page1 visually screenshot-audited in this research session; p1 §1.2 shows multi-bit CMux, FFT/automorphism sharing, MLWE-based sparse message packing, BatchCBoot. Official abstract reports **2.4× faster** than Guimarães–Pereira CCS2025 in their paired benchmark; **not** a universal improvement or matched key footprint for all profiles. Historical project BOOT-B075/076 already audited its matched interfaces and ruled out naive two-message ring doubling and direct dense ternary subring-key substitution.
4. Closest packing-key memory prior art: Refined TFHE / Partial LWE / FFT-KS, *Patching and Extending the WWL+ Circuit* (ePrint **2024/1318**), public PDF https://eprint.iacr.org/2024/1318.pdf. Search-index source excerpt Table2 shows substantial LWE→GLWE conversion key-size/latency benefits in its **own** parameters, e.g. PARAM_2_2 32MB packing KS no LWE KS versus 0.52MB using authors' specialized method; this is **not** 2025/686's input-packing interface, and detailed full theorem/keys not reviewed this round. 2025/686 p27 already explicitly cites Partial LWE and RLWE Conversion and says those may reduce packing key memory to few MB but noise/cost impact not evaluated. So generic 'apply Partial LWE / FFT-KS to AmortBoot' is an author-identified and heavily pre-anticipated idea, **NOT** a new primitive/contribution.
5. **Source-version warning:** Public web indexing of ePrint PDF `https://eprint.iacr.org/2025/686.pdf` surfaced at least one Table6 snippet differing from the cached 34p mirror (e.g. some amortized intracoef-batching timings); official PDF endpoint cannot be independently byte-opened currently. Do NOT mix such snippets into the same table, and do not treat 34p mirror as publisher-authenticated. The one mathematical Amdahl claim below is conditional on explicit 34p source §7.1 and its measured fraction, not universal 2026 state of the art.

## One primary falsifiable claim

`H_PACKING_ONLY_2X_LATENCY`: In Guimarães–Pereira's **original** amortized 2025 bootstrapping pipeline, if the LWE→RLWE **Packing KeySwitch** alone is redesigned or removed and the other stages remain unchanged, full amortized bootstrapping will become >=2x faster.

**Cheapest test:** p23 §7.1 authors explicitly say repacking accounts for **only 1%–5%** of execution time. Let f=T_pack/T_total, with 0.01<=f<=0.05. Removing the **entire** packing computation gives `S_max=1/(1-f)`, and `S_max<=1/0.95=1.05263158`. Even an impossible zero-latency packing gets at most **5.263%** speedup on this existing system and timing scope; a partial rewrite gets less. Thus **FAIL** for 2x throughput/latency speedup. Not a lower bound for other key choices, multi-client memory bandwidth, out-of-core serving, swap pressure, full multicore nor BatchBoot 2026.

## Genuine memory problem and author's own already-known solution direction

- p25 Table5 (single-thread Xeon 8488C, 10 runs, parameters author-selected): 2b/2048 batch ~17.09MB dedicated bootstrapping key, 4b/2048 ~18.41MB, 6b/4096 ~18.59MB, 8b/8192 ~70.13MB, and amortized 4.01/4.28/4.79/28.52ms per message for these respective batches. **Bootstrapping Key Size field explicitly excludes other input packing and HW-reduction keys.**
- p26–27 authors' **traditional input Packing KeySwitching Key** takes roughly 128 MB–2GB depending on precision/batch. These ranges are not paired individual benchmark entries, so **do NOT** compute exact total eval-key footprint or claim guaranteed 90% savings.
- p19 §5 Alg5 proposes a lower-noise sparse-packing key with extra computation, and explicitly calls it of **limited practical applicability**. p27 authors instead point to **RLWE Conversion and Partial LWE / FFT-KS** as potential means to reach *few-MB* packing keys, but warn that noise overhead may increase and full integration/benchmark not evaluated.
- p23 §7.1 HW-ReducingKeySwitching is a **separate** key switch after repacking and BEFORE sparse bootstrapping; conflating packing and HW reduction can break input/output secret-key types. Table3 RPCs are higher-HW secret distributions than Table4 bootstrapping sparse keys. A 'fused packing directly under low h' requires full equivalent output noise, error distribution and key-security estimation, not a free lookup swap.

## Cross-system benchmark/security obligations before any re-entry

Compare most recent **BatchBoot 2026** first at matched 128-bit concrete estimator, same input and output precision, failure probability, n/N/h, packed active count, q, available RAM, BSK/PCK/KSK/automorphism key bytes, keys possibly seeded, CPU/GPU environment, setup amortization, online total latency/throughput, and actual LWE→RLWE output noise. Cross-check real security of low-h / subring and conditioned-gap secrets and malicious key/nonce choice if within model. A purported 'memory saving' should measure ALL evaluation keys (not just BSK), peak RSS and page faults under a RAM budget. **No source-equivalent BatchBoot packing-key footprint test or proposed integration is currently done**.
Other source note: author's rejection-sampled maximum gap B and penalty δ are already included in Table4 claimed security, but security reductions and distributions need their original qualifications; this iteration makes no new security claim.

## Research value / decision

**FAIL** latency-target claim. **PASS** that 2025 author measured/acknowledged a substantial memory obstacle in an input packing key distinct from already-tiny BSK. **FAIL_GENERIC_NOVELTY** for 'simply use RLWE Conversion/Partial LWE/FFT-KS', as prior work and original authors anticipated it. BatchBoot 2026 further moved the SOTA and already optimized sparse workloads. **No new cryptographic algorithm** established and no basis to authorize Codex.

`DECISION: PARK_2025_AMORTBOOT_PACKING_LATENCY; RETAIN_MEMORY_BOTTLENECK_AS_ENGINEERING_SCOUT_ONLY`.
If PI later asks for engineering, one bounded same-system comparison would test an actual alternative PCK end-to-end under latest BatchBoot or source-equivalent MOSFHET with security/DFR/accuracy and full-key RAM; generic PCK replacement is not ready as a publishable claim.

**Next P0:** seek an actual latest source-complete high-cost FHE primitive or proof-level security gap; avoid merely replacing a small-work fraction, and avoid more static parameter scans without a novel invariant or adequate whole-system gains. If analyzing sparsity patterns, read and reconcile the source's security-loss δ and post-2026 low-HW attacks first.

## End
`STATUS=FAIL_PACKING_ONLY_2X_LATENCY / PASS_MEMORY_ISSUE`
`RESULT=AUTHOR_1_TO_5_PERCENT_AMDAHL_CEILING_1.05263X`
`NOVELTY=NOT_ESTABLISHED`
`NEXT_TEST=NEW_SOURCE_COMPLETE_P0_CORE_BOTTLENECK_WITH_REAL_SYSTEM_HEADROOM`
`STATE_UPDATE=THIS_FINDING_ONLY`; `CODEX=NOT_RUN`.
