# Iteration 141 — Standard Lattigo v5.0.2 rejects source FHE(8,5) mixed-radix ring; original MRFHE implementation unavailable

**Date:** 2026-10-13. **Human PI authorized:** “好的，请继续” after completed I140. **ONE primary hypothesis + cheapest decisive implementation-source check.** This iteration did NOT perform a source-equivalent full noisy MRFHE/CKKS run, nor infer practical speedup, source bug, or insecurity.

## Read before write / primary evidence

- Read in order `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I140 (GitHub SHA `5ca73ff34773277505a6cdf57cba88e65e53db7d`), `findings/mrfhe-fhe85-crossbatch-ks1-d2prime-slot-error-gate-iteration140.md`, the long-term `findings/OPEN_RESEARCH_BRANCHES.md`, and `MISSING_SOURCES.md`.
- Original Cheon, Hong, Kang, Kim, Kim, Lee, Lee, *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, ePrint **2026/853**, https://eprint.iacr.org/2026/853; previous round obtained 18 physical-page original PDF as Library `2026-853.pdf`. This turn searched within the entire Library PDF for `github`, `source code`, `implementation`: the ONLY `github` citation in its extracted text is original dependency **[26] Tune Insight SA, Lattigo v5.0.2, `https://github.com/tuneinsight/lattigo`**, physical p13. Paper abstract and §1.1 physical p2 state authors *implemented MRFHE on top of Lattigo* and call it first performance-competitive **non-power-of-two cyclotomic ring FHE library**. §6/Table5 p18 specifies `FHE(8,5)`: `N=2^8·3^5=62208`, `logPQ=1658`, `h=31104`, sparse temporary h32, `dnum=5`. No independently identifiable paper-specific author implementation repository or modification patch URL found in full PDF text.
- Connected GitHub repository source `tuneinsight/lattigo`, tag **v5.0.2** (exact version paper references), `ring/ring.go` blob SHA `b9e2c58a2ee7fdfd2f68591758a91e4da4eb1668` at https://github.com/tuneinsight/lattigo/blob/v5.0.2/ring/ring.go, lines 241–280. `NewRing(N,...)` calls `NewRingWithCustomNTT`, which has explicit check `N < MinimumRingDegreeForLoopUnrolledOperations || (N&(N-1)) != 0 && N != 0`, returning `invalid ring degree: must be a power of 2...`. `core/rlwe/params.go` blob `1d9e6174a55a9bfc34dddc9166e422aaf92c3e57` at https://github.com/tuneinsight/lattigo/blob/v5.0.2/core/rlwe/params.go, uses `LogN` / `N=1<<LogN`, ordinary power-two setup.
- Connected GitHub source `tuneinsight/lattigo` v5.0.2 `README.md` blob `0ad498a6bc24688c1f63e5251ad9098332fb02a8`, explicitly says *optimized arithmetic for power-of-two cyclotomic rings*. This is **the public upstream**, not the MRFHE authors' modified fork.
- GitHub repository discovery searched `MRFHE`, `mixed-radix fully homomorphic encryption`, `batch bootstrapping mixed radix`; none of returned repo names corresponded to the authors' MRFHE proof-of-concept (one unrelated `scott-glob/mrfhem` string match). Global GitHub code search `FHE(8,5)`, `MRFHE`, `Batch SlotToCoeff` and exact paper title did not identify source-qualified MRFHE code. Author Seungwan Hong's publicly listed repos via GitHub `user:swanhong` showed 10 repos, no MRFHE-specific repo among them; author `swanhong.github.io/_pages/about.md` blob `ee5ebc17197a06d6a47653ade998acfbd354cade` links the ePrint but not a code artifact. The author's different `swanhong/fully-encrypted-ml` README blob `57343777ec670047aa894b8b721ee1747e8a69ce` is a Rust functional-encryption implementation **unrelated** to MRFHE.
- Web current search for `MRFHE`, `Lattigo`, `Cheon Hong Kang`, GitHub/code references likewise returned paper/author page and generic upstream Lattigo, not a verifiable original MRFHE implementation or a source-issued exact FHE(8,5) experiment harness. **Limited discoverability is NOT proof the code does not exist**, only that it is unavailable in accessible sources inspected.

## ONE hypothesis / direct falsifier

[HYPOTHESIS] A matched secure/noisy `FHE(8,5)`, K1-vs-K2 real complete auxiliary PCMM experiment can be built **directly on the published public vanilla Lattigo v5.0.2 library** cited as [26], without needing source-specific mixed-radix patches/Go module/fork.

[FALSIFIER] At the source's parameter `N=62208`, check the exact tagged upstream `NewRing` constructor's ring-degree precondition. A mandatory rejection of this N kills use of **unmodified public upstream**. Also check the paper for a public patch/repository that would permit an actual real N62208 run without silently swapping rings.

[EXACT TEST]
```
N=2**8 * 3**5 = 62208
N-1=62207
N & (N-1) = 61952 ≠ 0
```
Confirmed with exact 32-bit JavaScript bit operations using `functions.exec`: `{n:62208,bitmask:61952,reject:true}`. Upstream `NewRing` therefore **returns an error at this ring dimension by inspection of its exact tagged code**. No Go runtime compilation was needed because this constructor rejects before NTT or key operations; it is a deterministic source-code precondition.

Thus [NEGATIVE] **vanilla Lattigo cannot instantiate the paper's mixed-radix ring**, and using stock Lattigo/standard power-two CKKS to generate a K2 noise curve would not answer I141's source-equivalent question. The paper's claim that it implemented a custom extension is not contradicted; the public dependency alone is insufficient to reproduce it.

## What was NOT done / why this stops the full-chain test

Actual source-compatible test requires **at least**:
1. Authors' mixed-radix Go ring/NTT, `S^(i)` & `S^(omega)` encoding/keyswitch/PCMM, and R^(i)↔R^(omega) conversions with legitimate full non-W-independent secret, including standard `dnum` gadget and BLAS/FLINT backend dependence;
2. exact Table5 FHE(8,5) `Q/P` RNS prime lists, stages' `Δ`, source default Gaussian key error and secret distributions, rescale/ring-switch logic, security estimator provenance/parameter alignment, and per-stage logging of decrypted coefficient/canonical-slot noise;
3. matched K1 (64 originals) baseline vs K2 (128 originals in ONE auxiliary block) with same shared keys, **both KS1 and KS2 nonzero**, source D′2 kernel, real componentwise rescale, matched output accuracy and data handling, plus packing/extra memory/latency. Compare additional costs with I139's **972** equivalent base-ring switches per K2 cohort.

Some parameter bit sizes are in Table5, but **they do not substitute for an executable algorithm and actual source-specific full keys/rescale chain**. Prior I33–I35 toy results and I140 W-axis error witness are not independently reliable estimators for this complete test.

Therefore actual K2 full-chain CKKS precision/security and real throughput **remain UNCLEAR**. Do not fabricate results, claim the authors' release is absent categorically, rebuild an incompatible stock ring, or insert a generic Gaussian toy as an answer.

## Research judgement

- **STATUS:** **FAIL vanilla-upstream direct-reproduction hypothesis / PASS deterministic source gate / UNCLEAR full source K2 noisy experiment / MISSING_CRITICAL_IMPLEMENTATION / HUMAN_REVIEW**.
- **RESULT:** Public tagged `Lattigo v5.0.2` `ring.NewRing(62208,...)` necessarily rejects N62208 as non-power-of-two (bitmask 61952). No authenticated **MRFHE-specific custom Lattigo implementation/patch** was recovered in searchable source/paper/author repos, so the requested true K1-vs-K2 full two-nonzero-KS/noise/rescale benchmark was **not performed**. I139 K2 ideal 1.7168× KS-equivalent potential and I140 constructed slot-noise risk remain conditional, not overturned or proven practical.
- **NEXT_ACTION:** **PARK MRFHE I139–141 reproducibility/noise branch** pending authentic author custom source/patch and full FHE(8,5) parameter execution manifest. If human PI obtains matching repo/archive, a **single** full K1/K2 noisy matched test is high-value; else reassign to new higher-novelty backlog target (vFHE still open, but its simple Brakedown patches archived). No author contact without PI approval.
- **STATE_UPDATE:** YES — critical source/constructor incompatibility closes the intended source-run gate and materially changes branch status. Register missing original code in `MISSING_SOURCES.md`, update backlog and STATE. I142 not started.
