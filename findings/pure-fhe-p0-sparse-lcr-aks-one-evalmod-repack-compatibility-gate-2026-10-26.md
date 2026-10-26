# PURE FHE P0 — Sparse LCR+AKS: One-EvalMod Packing Compatibility Gate

**Date:** 2026-10-26 Asia/Singapore
**Stage:** `PURE-FHE-P0-PRESCOUT-03`; independent P0 broad research, NOT a BOOT/SHIP/CGS series increment.
**Status:** `FAIL_DROPIN_ONE_ROTATION_PACKING / PARK_SPARSE_LCR_AKS_CURRENT_MECHANISM`.
**Scope:** ONE primary hypothesis and ONE minimal exact static counterexample; no raw ciphertext execution, no Go compile, no GPU/Codex or formal correctness theorem.

## Read-before-write & source evidence

- Archived source/previous derivation: `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md`; `findings/pure-fhe-p0-sparse-lcr-aks-ctS-full-vs-sparse-diagonal-cost-prescout-2026-10-26.md`; `findings/pure-fhe-p0-sparse-lcr-aks-backward-fft-pruning-evalmod-packing-gate-2026-10-26.md`.
- Original Yan et al. *Faster Bootstrapping for CKKS with Less Modulus Consumption*, PKC 2026, ePrint 2025/1403, §3.1 Remark1 explicitly **does not support sparsely packed** CKKS with conventional Trace before LCR; only full packing (possibly sparse-SECRET encapsulation). Official author explainer https://ckks.org/blog/2026/less-mod-ckks/ (June29 2026) and source mirror PDF pp13–15,23–27 (version not independently authenticated); reported 20–35% full-packing gain, 1 saved level, NOT sparse-packing performance.
- Actual pinned author code `Fainabi/Lattigo-LCR-AKS@3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4`, `circuits/ckks/dft/dft.go` blob `69dcb735c7bc55b6edf18e3dbe694f6544303d22`, `circuits/ckks/bootstrapping/evaluator.go` blob `130e0da53f61a430ee8ad4b9336ec282602b018f`, `circuits/ckks/bootstrapping/parameters.go` blob `3261982d8c3d4c8ed13f8eb454923893c0a94def`. Source states sparse CtS `ctReal=Ecd(vReal||vImag)`, `ctImag=nil`, with `RepackImagAsReal`; full `ctReal=Ecd(vReal)`, `ctImag=Ecd(vImag)`, both nonnil; `bootstrap` calls `EvalMod` separately for both nonnil outputs then calls `SlotsToCoeffs`. Existing full/dense `SlotsToCoeffs(ctReal,ctImag)` merges `ctReal + i ctImag`, whereas sparse `SlotsToCoeffs(ctReal,nil)` simply evaluates its sparse-domain STC DFT. `dftLevelConserved` sets output `LogDimensions` from **input** metadata, not matrix's declared `LogSlots`. Thus swapping `LogSlots` in matrix literal is NOT a verified runnable dense substitute for sparsely packed input.
- Source nearest: OpenFHE CKKS bootstrapping docs https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_BOOTSTRAPPING.md note full-real slots use 1 ciphertext inside **SlotsToCoeffs-first** but 2 in **ModRaise-first**. This is a DIFFERENT bootstrapping order, not identical LCR mechanism. Already published sparse re-packing, hoisting, pruned FFT and partial CtS techniques; generic single-EvalMod packed SIMD is not novel by itself.

## One hypothesis and cheapest exact falsifier

`H_ONE_ROTATION_DROPIN`: For n=N/2=32768 complex full slots and t=4, after replacing conventional post-ModRaise Trace by an output Fourier projection `D4=4diag(1_{4|j})` and retaining full LCR+AKS first CtS, a **single slot rotation + addition** of the two projected real/imag ciphertexts creates a *drop-in input for the author's UNCHANGED sparse (`LogSlots=13`) SlotToCoeffs*, without an additional cryptographic compaction or different linear transform, while using one EvalMod.

**Assume ideal mathematical slot model first**: due to the projection each real component A has value a_j at slot 4j, the imaginary B has b_j at slot 4j, j=0,...,8191, and zeros elsewhere; normalizing the global factor t is not asserted. A rotation by +1 creates P=A+Rot(B,+1) with interleaved layout:
`P[4j]=a_j; P[4j+1]=b_j; P[4j+2]=P[4j+3]=0`.
For the textbook **contiguous sparse representation** expected by a `Ecd(vReal || vImag)`-style source, one would instead require:
`U[j]=a_j; U[8192+j]=b_j,` possibly with source-specific repeated slot-lane embedding. The author's sparse STC is defined against that packed representation; it does **not** include an automatic stride-four compaction.

**Concrete witness disproving the claimed drop-in input equality:** set a_1=1 and all other a_j,b_j=0. Then P has nonzero slot **4**, while the flattened U has nonzero slot **1**. No fixed single cyclic rotation can map all real positions `4j` to `j`: for j=0 must rotate by 0; for j=1 must rotate by -3 modulo n. This is a SOURCE-INFORMED **interface mismatch**, not an impossibility proof for a *custom* STC transform. Not testing underlying CKKS RNS or numerical error.

**One-layer diagonal-transform cost stress (conditional canonical layout):** the permute-to-compact map has offsets `δ_A(j)=j−4j=−3j (mod32768)` and `δ_B(j)=8192+j−(4j+1)=8191−3j (mod32768)`. One pure JS set-enumeration across all 8192 j gave A offsets **8192 distinct**, B **8192 distinct**, **union 16384 distinct** (zero overlap). Therefore directly implementing that exact contiguous compaction as one plain CKKS diagonal-matrix transform would need 16384 shift diagonals in this representation — not a plausible free one-matrix tweak. THIS IS NOT 16384 actual evaluation keys/runtime rotations: BSGS or multi-stage bit-permutation network can use fewer rotations, and the real `LogDimensions`, slot repetition and numeric coefficient realization need to be checked before any cost prediction. The calculation merely falsifies *one rotation+add then unmodified sparse S2C*.

### Can a single EvalMod still exist algebraically?

Conditionally yes: for arbitrary slotwise evaluation polynomial f, selected classes (0 and 1 mod4) of `f(P)` equal f(A), shifted f(B), respectively. If f(0)≠0 or CKKS noise causes residuals in inactive lanes, those lanes require appropriate clearing or must be ignored in the inverse transform; false-to-zero equality must NOT be assumed. Thus **one EvalMod is not algebraically impossible**, but correct extraction/packing back into expected `SlotsToCoeffs` representation needs *another* nontrivial linear transformation `C` or **re-derived** STC `StC ∘ C`. Its key count, input scaling, RNS/lift, noise, level and semantics are unknown. The new one-rotation pack additionally incurs an evaluation key / keyswitch and changes the active input layout of EvalMod.

### Additional gating obligations

- Source `ModUp` unconditionally concludes with `Trace(...LogSlots)`; a no-Trace candidate requires implementation modification, different first-factor GHS-type LCR+AKS keys bound to its public diagonals, and a verification that immediately post-ModRaise *unreduced* `<ct,s>` small-lift holds under the right dense/sparse secret.
- Full CtS has 4-factor diagonal supports `[32,15,15,31]` versus native sparse `[32,7,7,31]`. Output D4-mask (existing P0-02 test) reduces last factor to 28; full masked 90 vs native sparse77 (13 extra supports). Those are source-shaped index-map supports, not physical latency or independent key count.
- Dense CtS physically returns two ciphertexts; original `bootstrap` calls EvalMod twice. A new packing path avoids the second only if the custom interface is correct and **does not add uncounted rescale/level and reconstruction cost**. Standard full CtS + untouched `SlotsToCoeffs` still uses two EvalMods.
- Exact sparsity of the two real/imag CtS branches and 4-stride slot placement after full CtS are only a **conditional ideal Fourier projection assumption**, not established code execution with real coefficients or metadata. The source bit-reversal, canonical Galois ordering, `LogDimensions` and nonlinear `EvalMod` approximation all require more work; cannot assert a definitive incorrectness bug or native impossibility.
- Original t=4 Trace uses rotation/key switching operations, but exact source-related NTT/rotation count was NOT measured; hence no credible paired speedup or net modulus advantage.

## Decision and value review

`FAIL H_ONE_ROTATION_DROPIN`. The obvious candidate cannot both keep original sparse STC interface and get a free one-EvalMod dense CtS path. Extra compact permutation/custom STC, >native middle-factor supports, key/rounding/RNS/precision obligations are substantial, while **no nontrivial novel mechanism** has emerged after three P0 gates and earlier I40/168/169. This does **not** prove all sparse-LCR extensions impossible, and saving a modulus level can still have system value with slower runtime. However, in the absence of a new invariant or evidence of a favorable **end-to-end** cost versus source baselines, DO NOT open another adjacent toy or authorize Codex just to implement naive packing.

`DECISION: PARK_SPARSE_LCR_AKS_CURRENT_MECHANISM; PRIORITIZE_DIFFERENT_PURE_FHE_STRUCTURAL_PROBLEM`.
Retain earlier source notes as reusable engineering/negative results; the I40 exact trace Fourier identity remains valid, and our P0 negative tests are limited to direct unchanged-factor/pruned/packed route.

**Next source-first selection:** find a different pure FHE high-cost operations class with a **complete, current** algorithm baseline and real numerical performance table (not new matrix-indexing tricks); audit original bottleneck and closest 2025–2026 literature before one primary hypothesis. Reuse SHIP/BOOT historical methods as *knowledge only*, do not restart their iteration series.

**END:** `STATUS=FAIL_DROPIN_REPACK; NOVELTY=NOT_ESTABLISHED; RESULT=STRUCTURAL_INTERFACE_MISMATCH; EVIDENCE=SOURCE_READ+EXACT_MODEL_COUNTEREXAMPLE; CODEX=NOT_RUN; STATE_UPDATE=THIS_FINDING_ONLY`.
