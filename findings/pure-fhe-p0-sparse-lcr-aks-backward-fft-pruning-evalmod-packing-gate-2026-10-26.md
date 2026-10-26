# PURE FHE P0 — Backward FFT-Pruning and EvalMod Fanout Gate for Sparse LCR+AKS

**Date:** 2026-10-26 Asia/Singapore
**Stage:** `PURE-FHE-P0-PRESCOUT-02` (PI-authorized broad pure-FHE selection; DOES NOT resume BOOT, SHIP, CGS or any numbered formal iteration).
**Status:** `FAIL_NAIVE_BACKWARD_ROW_PRUNING / FAIL_FREE_SINGLE_EVALMOD / BOUNDED_REDESIGN_OPTIONAL`.
**Evidence:** pinned author Go source + existing PDF prior archival analysis + independently executed pure-graph static Python. NOT a compiled FHE, performance/precision/security experiment. No Codex run.

## G0, source and earlier work

- Earlier gate: `findings/pure-fhe-p0-sparse-lcr-aks-ctS-full-vs-sparse-diagonal-cost-prescout-2026-10-26.md`, established author source-congruent four-level *support index counts* for `N=65536`, `LogSlots=13` sparse `[32,7,7,31]` total 77 versus `LogSlots=15` full `[32,15,15,31]` total 93.
- Older original algebra: `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md` exact Fourier identity `F^{-1} S_t = D_t F^{-1}`, `D_t=t diag(1_{t|j})`; tested earlier under standard canonical index ordering. **This current study is NOT a proof of entire CKKS matrix map correctness**, especially after CoeffsToSlots real/imag and packing.
- Original paper: Yan, Zeng, Cao, Song, Wang, *Faster Bootstrapping for CKKS with Less Modulus Consumption*, PKC 2026, ePrint **2025/1403**, manuscript 51 physical pages acquired under `VERSION_UNVERIFIED` mirror SHA256 `784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29`. Source PDF physical p14 §3 Remark1 says LCR excludes **sparsely PACKED** CKKS because the post-ModRaise `SubSum` / `Trace` uses rotations+KeySwitch, destroying the low-unreduced-integer-decryption precondition; this differs from source *sparse-secret* encapsulation for FULLY packed encrypted vectors (§6.3 pp26–27). Table4 physical p26 4 CtS factors `32,15,15,31` and only FULL-slot output, stated throughput improvement 1.20–1.35× at similar matched parameter sets, not sparse-slot benchmark.
- Pinned author GitHub **`Fainabi/Lattigo-LCR-AKS@3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4`**:
  - `circuits/ckks/dft/dft.go` blob `69dcb735c7bc55b6edf18e3dbe694f6544303d22`: `ifftPlainVec`, `GenMatrices`, `genWfftIndexMap`, `nextLevelfftIndexMap` plus `CoeffsToSlotsNew`, `CoeffsToSlots`, `dftLevelConserved`.
  - `circuits/ckks/bootstrapping/evaluator.go` blob `130e0da53f61a430ee8ad4b9336ec282602b018f`: actual `ModUp` ends in `Trace`; `bootstrap` calls CoeffsToSlots then `EvalMod(ctReal)`, and **additionally** `EvalMod(ctImag)` if nonnil, then SlotsToCoeffs.
  - `circuits/ckks/bootstrapping/parameters.go` blob `3261982d8c3d4c8ed13f8eb454923893c0a94def`: `C2SParams.Type=HomomorphicEncode`, `Format=RepackImagAsReal`, default `BitReversed=false`; separate `LogSlots` determines sparse vs full.
  - Code URLs: https://github.com/Fainabi/Lattigo-LCR-AKS/blob/3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4/circuits/ckks/dft/dft.go and https://github.com/Fainabi/Lattigo-LCR-AKS/blob/3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4/circuits/ckks/bootstrapping/evaluator.go .

## Exactly one primary hypothesis

**H0:** For `t=4`, moving the original SubSum after CoeffsToSlots by row projection `D_4` and performing *backward live-row pruning* of the AUTHOR'S UNCHANGED four-factor full-slot iFFT reduces the two extra middle factors down to sparse-native 7+7 diagonal supports **without additional encrypted compaction or another EvalMod execution**.

**Cheapest falsifier:** Use the exact radix-2 butterfly connectivity of the author `ifftPlainVec` to backward-track output indices kept by `D_4` through the **last merged four butterfly steps (8,4,2,1)**. If ALL 32768 input positions to that final factor are live, previous middle factors cannot be row-pruned by backward liveness alone. Audit `CoeffstoSlotsNew` to see whether dense vs sparse is the same EvalMod ciphertext arity.

## Results — independent static executed test

A reproducible standalone source-shaped Python dependency test was executed and saved locally (NOT in GitHub repo):
- `/mnt/data/pure_fhe_p0_pruned_fft_dependency_gate.py` SHA256 `2e348a71070e4c0aad2f5bde97951dbc2f699e83e16e8ded5b30c71b845e7861`
- `/mnt/data/pure_fhe_p0_pruned_fft_dependency_results.json` SHA256 `6622a597328c105fc493b19e3164963887c7df0f3bde6acb8f33c3f12abcbebe`

The script reproduces the source 4-factor `HomomorphicEncode / BitReversed=false` merge schedule `[5,3,3,4]` for full `LogSlots=15`; per-layer butterfly steps `[16384,8192,4096,2048,1024]`, `[512,256,128]`, `[64,32,16]`, `[8,4,2,1]`. The last group is a block-diagonal 16×16 full-support butterfly transform: every selected output row within a block depends on **all 16 input positions**, since each radix-2 butterfly has nonzero complex twiddle coefficients; no independent output coordinate can bypass any input in its group merely by dropping other output rows.

Keeping j divisible by4 selects **8192 / 32768 output rows**, but the union of their exact last-factor predecessor rows is **32768 / 32768**. Thus simple backwards liveness mask cannot prune stages 2 and 3: their support counts remain **15+15**, not **7+7**.

The D4 mask actually makes the last factor diagonal support **28 rather than 31**, not zero savings: within each 16-row butterfly block, selected j=0,4,8,12 have candidate input columns k=0..15, so modulo-global-slot offsets `k−j` range `−12,...,+15`. Hence the removed last-stage diagonal offsets are precisely `−15,−14,−13`. This yields the *static support* count:
```
Sparse native factor support      32 +  7 +  7 + 31 = 77
Full native factor support        32 + 15 + 15 + 31 = 93
Full plus final D4 mask support   32 + 15 + 15 + 28 = 90
Difference masked-full vs sparse                       +13 (+16.88%)
```
This is **sum of per-matrix cyclic-diagonal offsets, not count of distinct Galois keys, rotations, NTTs, ciphertext×plaintext multiplications, nor native runtime**. Output mask reduces last factor *row-by-column logical nonzero products* 524288→131072 in this boolean structural model, but slot masks normally encode to dense coefficient plaintexts and each remaining whole-ciphertext diagonal multiplication still processes a whole RLWE ciphertext. Actual numeric code `GenMatrices` was not Go executed and source coefficients/rounding/bitreversal phase not numerically verified here. A second `LogSlots=12` control reproduces same masked last factor 31→28 and all live prior rows; it is only source-shaped internal graph validation.

### A more serious **output-arity cost gate**

The actual `dft.go` implementation allocates:
```
ctReal = NewCiphertext(...)
if ctsMatrices.LogSlots == eval.parameters.LogMaxSlots() {
    ctImag = NewCiphertext(...)
}
```
Source comments: sparse `n<N/2` uses `ctReal=Ecd(vReal||vImag)`, `ctImag=nil`; full `n=N/2` uses TWO ciphertexts. And actual source `bootstrap` invokes **two** `EvalMod` evaluations whenever `ctImag!=nil`, versus **one** for sparse output. Hence naive 'remove Trace, set LogSlots to full, mask rows' **also changes EvalMod ciphertext count 1→2** unless a new (costed) repacking/reindexing protocol is added BEFORE EvalMod. This extra EvalMod can dominate any trace rotation saving. **This is a source-level conditional execution consequence, not a measured time ratio or proof that a custom modified pipeline must evaluate twice.** Also input `LogDimensions`, S2C mapping and ciphertext scale need checking for any full-matrix type switch; setting `LogSlots=15` is not a verified executable patch.

## New linking invariant required; bounded representation option

Potential `PACK_COMPACT` path to keep one EvalMod: after the D4 outputs, `ctReal` and `ctImag` have values on the same stride-four support (in the ideal Fourier/sparse-projection model). Public one-slot rotation of one branch would place its values on disjoint residue class modulo4, allowing `ctPack=ctReal+Rot(ctImag,1)`; a slotwise EvalMod could evaluate both if all active slots are valid inputs and inactive-slot behavior/approximating polynomial's value at0 are handled. **This is only a known SIMD packing observation, not new or a verified CKKS operation**, and it adds at least a rotation+KeySwitch and requires a new S2C decoding/repacking map or costly coefficient masking; plaintext mask encoding may itself consume scale/modulus. Correct ring coefficient order, output `LogDimensions`, conjugate real/imag splitting, `f(0)`, approximate precision, and RNS/noise are not audited. It may become unattractive or duplicate existing sparse CtS/repacking prior art.

Closest selected comparison work:
- Bossuat et al. ePrint 2020/1203, sparse-subring trace and normalization fusion, previous full textual audit in I40. Conventional FFT factor pruning and sparse CKKS packing known.
- Sung et al. **EvalRound+ Bootstrapping and Its Rigorous Analysis**, IEEE Access 2025, DOI `10.1109/ACCESS.2025.3595177` explicitly discusses `Sparsity Patterns of FFT Matrices`, closest 'change FFT support' prior-art family; full new algorithm not yet audited.
- Coron–Seuré, **PaCo: Bootstrapping for CKKS via Partial CoeffToSlot**, ASIACRYPT 2025, DOI `10.1007/978-981-95-5122-4_2`, uses **a different blind-rotation-based CKKS bootstrap and partial CtS**, **NOT** equivalent to this specific LCR+AKS output-masking claim; exclude misleading novelty of phrase 'partial CtS'.
- Seuré, `SCORE` ePrint 2025/1983 for real-vector CKKS SlotToCoeff optimization, another conditional application regime; does not prove our interface.

## Decision

**`FAIL H0` for unchanged-factor backwards pruning and unmodified full CtS arity.** Do not infer impossibility of every reordered/partially factored FFT scheme or fused Trace-LCR construction. **PARK** simple `D_t` output-only pruned full CtS as a research-contribution route, despite its correct algebraic identity. Retain ONE bounded genuinely different interface redesign option (`PACK_COMPACT` or `Trace fused into first AKS`), but only after a specific, matched end-to-end symbolic cost/precision/soundness and nearest-prior-art check. With no new invariant and credible net gain, pivot P0 to a different source-complete pure-FHE bottleneck rather than iteration roulette.

**NEXT cheapest discriminator:** Under one fixed sparse `N=65536, LogSlots=13, t=4` and exact source `Q/P` levels, compare existing `Trace→SparseCtS→1×EvalMod→StC` against **one** explicitly defined packed candidate `NoTrace→FullCtS→stride4-selected two outputs→public rotation/merge→1×EvalMod→typed inverse packing/S2C`. Before any running code, enumerate exact rotations, NTTs, ciphertext plaintext masks, extra levels, keys/bytes, real and imag coefficient order, and verify author `LCR` small integer lifting precondition. If static candidate cannot avoid an additional costly level or cannot beat baseline even optimistically, PARK whole sparse-LCR branch. Do not try two independent redesigns in same iteration.

**End:** `STATUS=FAIL_BACKWARD_PRUNING + FAIL_NAIVE_SINGLE_EVALMOD`, `RESULT=SOURCE_BIFURCATION_AND_EXACT_GRAPH`, `NOVELTY=UNVERIFIED`, `EVIDENCE=READ_SOURCE+STATIC_EXECUTED_PY`, `CODEX=NOT_RUN`, `STATE_UPDATE=THIS_PRESCOUT_FINDING_ONLY`. Root `STATE.md` remains large/historically stale and is NOT overwritten, to avoid unreconciled multi-line research state loss.
