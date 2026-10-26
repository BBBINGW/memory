# PURE FHE P0 — Sparse-Packed CKKS × Level-Conserving Rescaling Cost Gate

2026-10-26 (Asia/Singapore) | **P0-PRESCOUT-01**; **not** a BOOT/SHIP/CGS or global I-series iteration. PI authorized starting P0 structural-FHE topic and preserving separate FHE×MPC backend engineering idea. One primary technical claim, one cheapest source-faithful static counting test. No native HE execution, no Codex, no experiment authorization implied.

## G0 & Source Provenance

- Research Quality Guide (2026-10-26), AGENT.md, RESEARCH_PHILOSOPHY.md, root STATE.md (historically stale top heading; see latest overriding context) and old findings were reviewed before this note.
- Paper **Lianglin Yan, Pengfei Zeng, Heyang Cao, Peizhe Song, Mingsheng Wang**, `Faster Bootstrapping for CKKS with Less Modulus Consumption`, PKC 2026/ePrint **2025/1403**, public author blog `https://ckks.org/blog/2026/less-mod-ckks/`. Full prior Research MCP PDF mirror physical pp12–15, 21–27 checked, **51 pages**, SHA256 `784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29`, VERSION_UNVERIFIED. Author paper §3.1 Remark1 physical p14 explicitly excludes **sparsely packed ciphertexts** from LCR because a post-ModRaise SubSum trace uses rotations/key-switching and destroys its small-unreduced-decryption invariant. The author's successful experiments use **fully packed ciphertexts** plus sparse-*secret* encapsulation; do NOT confuse sparse secret with sparse packing. §5–6 physical pp23–26: first CtS factor LCR+AKS; Table4 baseline first 32 and other 15,15,31 diagonals, roughly 20–35% higher reported throughput and +1 level saved for FULL packing only. Original source's exact first-matrix key binds encoded public diagonal (source equation (5)); author keygen code confirms.
- Exact author-code **Fainabi/Lattigo-LCR-AKS@3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4**, retrieved live GitHub:
  - `circuits/ckks/bootstrapping/evaluator.go` blob `130e0da53f61a430ee8ad4b9336ec282602b018f`: `ModUp` ends with `eval.Trace(ctIn, eval.CoeffsToSlotsParameters.LogSlots,...)`, and then `CoeffstoSlots` calls `eval.DFTEvaluator.CoeffsToSlotsNew(...C2SDFTMatrix)`.
  - `circuits/ckks/bootstrapping/parameters.go` blob `3261982d8c3d4c8ed13f8eb454923893c0a94def`: C2S matrix literal `Type: HomomorphicEncode`, `Format: RepackImagAsReal`, `LogSlots: LogSlots`, `Levels: CoeffsToSlotsLevels`.
  - `circuits/ckks/dft/dft.go` blob `69dcb735c7bc55b6edf18e3dbe694f6544303d22`, `computeBootstrappingDFTIndexMap`, `GenMatrices`, `genWfftIndexMap`, `nextLevelfftIndexMap`: explicitly allocate sparse diagonal supports and merge FFT butterfly factors as function of `LogSlots`. Note `GaloisElements` uses BSGS, so diagonal support counts are NOT count of actual rotation-key objects.

## Old research already available / no re-claim

`findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md` (Oct10 I40) previously proved the algebraic identity `F^{-1} S_t = D_t F^{-1}`, with coefficient projection `D_t=t diag(1_{t|j})`, and support non-expansion for multiplying the CHRONOLOGICALLY LAST Fourier factor by D_t. This is **existing archived work**, not new in this prescout. It did NOT establish full circuit equivalence/precision/cost to source implementation.
`findings/ckks-lcr-aks-plaintext-bound-rotation-key-reuse-iteration168.md` and `findings/ckks-lcr-aks-public-basis-key-synthesis-roundoff-noise-iteration169.md` already ruled out direct unchanged AKS key reuse across public diagonal changes and checked the error of linear key synthesis; do not propose them again.

## ONE primary hypothesis / static falsifier

`H_ZERO_EXTRA_SUPPORT`: If for sparse packing `t=4` we remove the pre-CtS SubSum/Trace to make the first LCR legal, and instead preserve the previous I40 Fourier trace projection at the output, then using the source's standard **FULL-DOMAIN four-factor CtS** is *diagonal-support neutral* relative to the source **SPARSE-DOMAIN four-factor CtS** — i.e., not only the final factor, but the entire FFT factor chain has no extra nonzero diagonal positions.

`FALSIFIER`: Same author `computeBootstrappingDFTIndexMap` on fixed `N=2^16`, 4 FFT factors, `HomomorphicEncode`, `BitReversed=false`, `RepackImagAsReal`, compare `LogSlots=13` (sparse) vs `LogSlots=15` (full), preserving same full ciphertext ring dimension and pre/post DFT semantics. An increase in diagonal supports kills this **specific** zero-overhead claim. This is NOT whole-protocol equivalence or a cryptographic lower bound.

## Results [SOURCE-CODE-BASED REPRODUCTION / DERIVED, NOT NATIVE]

A pure JS transcription inside the connected research session reproduced the **index-map set operations**, `merge` schedule, and `HomomorphicEncode` rotation offsets (`genWfftIndexMap` and repeated `nextLevelfftIndexMap`), no compiled Go and no ciphertexts:
```
full  N=65536, LogSlots=15, four factors, merge=[5,3,3,4],
    per-factor nonzero-diagonal SUPPORT = [32,15,15,31], sum=93;
sparse N=65536, LogSlots=13, four factors, merge=[5,2,2,4],
    per-factor nonzero-diagonal SUPPORT = [32,7,7,31], sum=77.
```
The full pattern `[32,15,15,31]` independently agrees with the author's Table4 full-packing example, useful validation of translation scope. For middle factors, [15,15] versus [7,7] = **16 extra nonzero diagonal positions** in full path, total SUPPORT +16/77 ≈20.78%. This is `FAIL_H_ZERO_EXTRA_SUPPORT`. The previous I40 output projection `D_t` is a ROW MASK on the last full factor; it cannot retroactively remove existing internal supported rotations without a NEW equivalent factorization/pruning/flow invariant. Some diagonal supports might cancel when populated with actual complex coefficients or after row mask; source index map is an upper/support construction rather than exact compiled nonzero plaintext count under every numerical parameter. The count is not end-to-end KEY COUNT, plaintext multiplications, latency, noise, security, precision or throughput.

**Important:** The original sparse `Trace` before CtS costs homomorphic automorphisms/keys; removing it might save those. Full-domain CtS has extra supported diagonals. Without matched cost of trace, FFT, GHS-first AKS key types, later BSGS factors and output format, **cannot conclude which full bootstrapping is faster or even source correct.**

## G1 gate, novelty and next bounded mechanism

Baseline: sparse packing `LogSlots=13`, N16 same author pipeline `ModUp→Trace→sparse CtS→EvalMod→StC`, fixed CKKS error/security/precision; candidate: no pre-CtS Trace, full CtS augmented with output coefficient projection `D_t`, with first-factor LCR+AKS and rest BSGS, correct final slot/coefficient output format. **NEW needed** beyond prior I40: a trace-aware/pruned **homomorphic FFT factorization** that enforces `D_t F^{-1}` while retaining source LCR's small-unreduced-decryption precondition and source's small-domain CtS cost; exact keys/coefficients, Q/P/RNS and bootstrapping scaling/noise must all match. Naive D_t multiplication into final factor alone does not meet this budget; ordinary 'pruned FFT' is strong prior art, so novelty remains UNVERIFIED. This is high-importance *problem setting* but source Table4 gives NO sparse-packing end-to-end baseline runtime.

**NEXT single lowest-cost followup if PI continues P0:** source code's actual `GenMatrices` for two fixed matching full/sparse scenarios with coefficient values and no extra stages, then propagate the final row projection backwards through **just the middle two FFT factors**. Determine whether a legal factor pruning eliminates the extra 8+8 supported diagonals or whether a costed shared trace/FFT interface is necessary. If no sizable savings after full cost accounting, PARK, not dozens of toy variants. No claim it produces a new mechanism until prior-art equivalent mechanisms (truncated FFT, partial homomorphic DFT, 2020/1203 SubSum absorption, recent CtS repacking) have been checked.

`END STATUS: FAIL_ZERO_EXTRA_SUPPORT / OPEN_COSTED_PRUNING_GATE`
`EVIDENCE: READ_SOURCE_CODE + PAPER_TEXT + CODE_INDEX_SET_DERIVATION; NATIVE_NOT_RUN`
`RESULT: middle factor overhead, prior I40 identity insufficient; not an impossibility`
`NOVELTY: UNVERIFIED; NO_NEW_SCHEME`
`DECISION: BOUNDED_REDESIGN_ONE_GATE, no Codex`
`STATE_UPDATE: THIS_FILE_ONLY; root STATE deferred reconciliation`.
