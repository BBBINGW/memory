# PURE-FHE P0-PRESCOUT-38 — Portfolio-Wide Stagnation / Conditional Priority Review

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_PORTFOLIO_REVIEW
LATEST_COMPLETED: P0-PRESCOUT-38
NEXT_ITERATION: P0-PRESCOUT-39 NOT_STARTED
STATUS: FAIL_ANY_READY_TO_BUILD_ORIGINAL_CONSTRUCTION / PASS_PORTFOLIO_TRIAGE / HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO — no GPU, server, native execution, or infrastructure changes
STATE_UPDATE: YES, isolated PURE-FHE finding ONLY. Global STATE.md and other tracks unchanged.

## One falsifiable research-program H38

Is there at least one surviving candidate from P0-01..37 that satisfies ALL:
(A) explicitly differentiated NEW cryptographic mechanism vs 2025–26 first-party prior art;
(B) typed algebraic correctness, noise and security pathway with no known decisive counterexample; and
(C) measurable whole-system improvement headroom under matched precision, DFR, key memory, N and security?
Cheapest test: source-first read of prior GitHub findings and primary numerical tables, not another toy constructive claim or native benchmark.

## Evidence inspected in repo (read-before-write)

GitHub Notes findings index: 497 file entries, including around 37 distinct PURE-FHE findings (P0-10 generated several separate ones). Read or rechecked key files from the sublines:
- pure-fhe-p0-amortboot-batchboot-sixbit-time-key-pareto-gate-2026-10-26.md
- pure-fhe-p0-amortboot-packing-key-memory-vs-latency-headroom-gate-2026-10-26.md
- pure-fhe-p0-sinc-mixed-matrix-hadamard-format-gate-2026-10-26.md
- pure-fhe-p0-sinc-batchboot-mixed-operator-roundtrip-source-gate-2026-10-26.md
- pure-fhe-p0-heterogeneous-cggi-adaptive-failure-mixture-tail-gate-2026-10-27.md
- pure-fhe-p0-adaptive-heterogeneous-gadget-schedule-union-certificate-gate-2026-10-27.md
- pure-fhe-p0-gckks2600-aks-bsgs-rescale-relaxation-kill-gate-2026-10-26.md
- pure-fhe-p0-gckks2600-first-split-norm-unit-escape-priorart-gate-2026-10-26.md
- pure-fhe-p0-gckks2600-step8-factor-parseval-headroom-gate-2026-10-26.md
- pure-fhe-p0-alu-binary-carry-affine-prefix-priorart-gate-2026-10-26.md
- pure-fhe-p0-arbitrary-modulus-a2d-lambda-integer-gauge-obstruction-2026-10-26.md
- pure-fhe-p0-ternary-signboot-trigonometric-hermite-prior-art-gate-2026-10-27.md
- pure-fhe-p0-revhomtrace-conversion-amdahl-headroom-gate-2026-10-26.md
- pure-fhe-p0-cbs-shared-relative-trace-testpolynomial-collision-gate-2026-10-26.md
- pure-fhe-p0-seeded-linear-ciphertext-lineage-bxt-gate-2026-10-26.md
- pure-fhe-p0-rboot-orbit-level-scale-range-functional-placement-gate-2026-10-26.md
- pure-fhe-p0-incomplete-ntt-dfr-security-frontier-gate-2026-10-27.md
- plus related early sparse LCR+AKS, preTrace, slot subalgebra, EvalMod-tail, shaped-rounding findings and historical OPEN_RESEARCH_BRANCHES.md read ONLY as context. Official other tracks are not re-opened, merged, or renumbered.

## Concrete first-party evidence and current novelty ceiling

(1) USENIX Security 2026 BatchBoot official paper https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao and official PDF sec26_prepub_li-zhihao.pdf, Table4, tested same machine and parameters at six-bit n4096 and nominal DFR 2^-64: source-paired AmortBoot 8.92ms per message, BSK 18.6MB; BatchBoot 8.43ms per message, BSK 120.1MB. The 5.49% latency gain costs 6.457x displayed BSK. **Only BSK**, NOT all PCK/KSK/automorphism key/peak RSS. New 2^-128 DFR data absent; never extrapolate or claim a 128-bit DFR. Prior BOOT B075/B076 already rejected naive shared-selector and dense subring transplanted mechanisms.
(2) CKKS mixed matrix operator: CRYPTO2026 Cheon/Kang/Lee SinC already has typed matrix multiplication / conversion methods; Gentry–Lee native matrix representation supports Hadamard and competing bootstrap. Generic free SinC Hadamard is false, generic convert-and-fuse is prior art. The newest Fast Batch Bootstrapping in CKKS is recorded on author's live website https://mskang0503.github.io/publications/ as ASIACRYPT2026, but full paper's precise algorithms remain unverified. An actual new mixed-operator/representation bridge and matched workload cost are missing.
(3) TFHE dynamic noise: 2025/1892 Hong–Lee heterogeneous gadgets and online key selection, 2026/610 Ballandras–Orfila–Tap tail probability importance splitting are first-party prior art. The latter source §5.2 openly reports difficulty directly resampling whole KeySwitch→ModSwitch pipeline, but static-per-schedule δ does not imply adaptive same δ. Elementary finite schedule union bound |S|δ already provides a sound conservative single-query fallback. No actual joint conditional sampler or quantified gain demonstrated; IND-CPA-D multiquery requires separate model.
(4) GCKKS: 2026/2600 source verified but P0-23..30 proposed cheap fixes fail or reduce to existing bounds/unit shaping. Simplified BSGS outer-noise apparent fixed floor is author proof relaxation removed by retaining 1/rho. Step8 has conditional Parseval norm headroom and no forced precision-growing extra penalty. Revised Focused CKKS 2026/2531 and shaped rounding 2026/2513 full texts remain source-blocked; do not invent their algorithms.
(5) ALU: 2026/1840 already includes compact ternary carry state; 2026/1869 integer public gauge fails odd modulus B|M. CRYPTO2025 trigonometric Hermite source ePrint2024/1623 Theorem1 subsumes ternary SignBoot. No novel scheme.
(6) CBS and RevHomTrace: ordinary relative trace already exists; packed output test polynomial collision under naive sharing; some trace-only cost savings capped by source application-specific Amdahl ratios. SinC nonlinearity representation and key compressed BXT linear lineage are conditional systems ideas without independent cryptographic mechanism.
(7) Incomplete NTT ePrint2025/696 source Table2: fastest eight-bit 584.7ms at model DFR 2^-9.3; only table-listed 2^-128-or-better eight-bit setup 1931.5ms at 2^-131.9 (~3.30x slower). Cipher security 128bit and DFR 2^-128 are different; new incomplete NTT dataflow is original paper's technique already, not ours.

## H38 answer: FAIL, honest risk distinction

No candidate has passed A+B+C concurrently; no newly constructed algorithm ready for implementation, novel theorem or independent performance result. This is evidence-supported STUDY-LEVEL stagnation, not a theorem that no publishable FHE improvements exist. Negative findings are useful falsification, but publishing/implementing without original mechanism is premature.

### Conditional priority order for next cheap falsification, NOT estimated publication odds

P1 (BEST MEASURABLE FIRST GATE): Modern BatchBoot evaluation-key memory vs speed in 6-bit. The source is complete and presents measurable tension. However 6.457x pertains displayed BSK not full storage, and nominal DFR only 2^-64; BOOT/SHIP similarities severely threaten originality. REQUIRE first-party typed audit of key generation and allocation: keys representing independent random ciphertexts vs public rearrangements vs prepared duplication; stage-by-stage size/lifetime/key-usage counts, FFT/CMux parameters and source already-used compression/hoisting. New construct must preserve correctness, security/DFR and show same-system speed/RAM improvement; trivial compression, parameter tuning, and old SHIP/BOOT ideas KILL. This is first priority for CHEAP CLEAR FALSIFICATION, not because publishability has been established.

P2 (HIGHER REPRESENTATION IDEA POTENTIAL, BLOCKED): Native mixed-operator matrix FHE across CCMM→entrywise nonlinear op→CCMM and bootstrap; close general prior art (2025/1957, 2025/1935, latest ASIACRYPT2026) and no complete newest author PDF. REQUIRE nearest-source gate and one fixed typed workflow with all conversions, levels, precision, keys and rival Gentry–Lee baseline. If ordinary conversion is fine, KILL.

P3 (PROOF-ORIENTED, PRIOR ART HIGH): Conditional tail guarantees under online heterogeneous gadget schedule. Need entirely new sound rare-event conditional sampler/verification algorithm for discontinuous KS→MS source process with an actual improvement over elementary finite-union risk budget; proof on fixed-key adaptive queries is harder. Otherwise KILL, not another Gaussian-mixture toy.

NOT PROMOTED: pure GCKKS masked splitting, AKS Step7, trivial Hermite A2B/carry, static guard slots, incomplete-NTT tweaking, naive shared CBS trace, BXT seeded DAG without proven GPU break-even, compiler range-tracking, old packing-only acceleration. These are CLOSED MECHANISMS or PARKED, not proofs that all broader problems are impossible.
SOURCE_GATED: ePrint2026/2513,2531,2562,2616,2618,1026, the full ASIACRYPT2026 Fast Batch Bootstrapping in CKKS. No source means no current detailed novelty assertion, but independent work need not await unavailable PDFs unless directly competing.

## Exact proposed next iteration, NOT executed here

P0-PRESCOUT-39 H39 draft:
Is the BatchBoot six-bit larger BSK mostly due to *semantically redundant* encryption/key-preparation representations that can potentially be shared without losing its FFT/CMux benefit, or is it mostly independently required secret-dependent key material? Start with the full official USENIX author key-generation and algorithm sections, inventory all bootstrapping, packing, conversion and KSK/automorphism keys, distinguish stored/prepared forms, determine which actual components cause 18.6→120.1MB. Make one precise rank/independence/reuse inference. Kill if trivial existing compression or no credible memory-speed frontier. No Codex yet, and do not confuse cost of BSK with total memory. User PI decides whether to start next iteration and/or change track.

## End of Iteration

STATUS: FAIL_ANY_BUILD_READY_MECHANISM / PASS_EVIDENCE_PORTFOLIO / HUMAN_REVIEW
RESULT: Three CONDITIONAL candidates ranked with explicit source, risk, criteria; BatchBoot key material source-gate first; all current ideas remain NOT ESTABLISHED in novelty.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: P0-39 BatchBoot full key inventory / representation-redundancy source test, only upon PI continued request.
STATE_UPDATE: YES this isolated findings file; root STATE.md and all other tracks unchanged.
CODEX_REQUIRED: NO.