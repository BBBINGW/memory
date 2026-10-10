# Iteration 41 — CKKS sparse SubSum bypass: bit-reversed pruning is possible, but not operation-neutral

Date: 2026-10-10
Branch: Iteration 40 CKKS LCR+AKS sparse-packing compatibility (2025/1403).
STATUS: FAIL for the claim that simply substituting a pruned full CtS for SubSum + small-subring CtS **preserves the original nominal rotation/key-switch operation count**. Positive result: precise backward pruning IS possible after correcting the implementation's bit-reversed output order. Real runtime, precision, security and novelty remain UNVERIFIED.

## Read-before-write and provenance
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and the complete prior finding `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md` before this iteration. Existing STATE.md tracks separate parked RIG-HE and was not changed.
[FACT] Primary paper: Yan et al., *Faster Bootstrapping for CKKS with Less Modulus Consumption*, PKC 2026, ePrint 2025/1403 §3 Remark 1 (physical p.14, sparse packed excluded due SubSum keys before LCR), §5.1 (first matrix LCR+AKS). Source paper cached in Research MCP last iteration, full 51 pp, mirror VERSION_UNVERIFIED, sha256 `784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29`. Bossuat et al. ePrint 2020/1203 §5.2 pp.17-18 supports conventional SubSum + reduced-domain CtS baseline.

[FACT / SOURCE CODE] Actual author fork `Fainabi/Lattigo-LCR-AKS`, public GitHub default branch `lcr`, inspected commit `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4` via authenticated GitHub read tools, NOT inferred from paper alone.
- `circuits/ckks/bootstrapping/evaluator.go` ~773–935: `ModUp` *always* ends by `eval.Trace(ctIn, eval.CoeffsToSlotsParameters.LogSlots, ctIn)`; for sparse packing this performs pre-CtS SubSum. The `EvkSparseToDense` path for sparse-**secret** encapsulation is a distinct optimization and does NOT automatically address sparse **slot** packing.
- `circuits/ckks/dft/dft.go` ~768–839: `computeBootstrappingDFTIndexMap` chooses merged radix-2 stages. For CoeffsToSlots (`HomomorphicEncode`), `BitReversed=false`, `Levels=[1,1,1,1]`, `LogSlots=11` merges [4,2,2,3] stages; for `LogSlots=9` merges [4,1,1,3].
- `dft.go` ~666–728: `ifftPlainVec` produces **descending decimation-in-frequency butterflies**, so natural coefficient index k is at physical output row `bitreverse_11(k)`. This crucial ordering detail was MISSED in the first cheap manual attempt during Iteration 41; corrected by exact modular checks and archived here. Row mask selecting natural indices k divisible by t=4 maps to contiguous physical output indices 0..511, NOT every fourth physical row. No actual matrix row permutation is inserted in `BitReversed=false` code.
- `dft.go` ~317–380, ~516–555: when level-conserved, first **executed** factor uses `EvaluateLevelConserved` and disables BSGS (`LogBabyStepGiantStepRatio=-1`), later ones use AKS when flagged else BSGS Evaluate/Rescale. `parameters_literal.go` default four-factor depth. `parameters.go` ~210–258 adjusts top level when LCR saves one level.
- `dft.go` ~383–470: sparse LogSlots<LogMaxSlots returns `ctReal=real||imag,ctImag=nil` after a repacking rotation; full LogSlots returns TWO ciphertexts, ctReal and ctImag. So a naive full-width replacement changes the downstream EvalMod ciphertext count/format.
- `circuits/common/lintrans/lintrans.go` ~320–367: `FindBestBSGSRatio` and `BSGSIndex` select baby/giant rotations, used in the operation-count audit.
Public code link: https://github.com/Fainabi/Lattigo-LCR-AKS/tree/lcr/circuits/ckks/dft

## Single primary hypothesis / falsifier
[HYPOTHESIS — FALSIFIED IN SOURCE-LEVEL NOMINAL COUNT] Given the exact Iter40 algebraic identity `F^-1 S_t=D_t F^-1`, simply removing pre-LCR SubSum, using a full `LogSlots=11` CtS, absorbing the mask into the final factor, and applying backward zero-row pruning should preserve the nominal number of online Galois/key-switch calls required by the conventional t=4 sparse `LogSlots=9` CtS pipeline, with no other necessary format conversion.
[TEST] Fixed N=4096,t=4. Reproduce author FFT factor diagonal offsets, infer reachable rows backwards under the CORRECT bit-reversed output mask, compute factor matrices' exact structural nonzeros, and compute source-level nominal BSGS / no-BSGS rotation counts. No FHE benchmark, parameter sweep or lattice estimator.

## Exact ordering / pruning
[DERIVED] For a complex-half Fourier matrix `F_{j,k}=zeta^(k*5^j)`, the author's `ifftPlainVec` outputs `T=n*P_bitrev*F^-1` up to subsequent global scaling. For t=4, Iter40's `D_t=4*diag(1_{4|k})` becomes a physical row mask `P_bitrev D_t P_bitrev^-1` selecting **first 512 rows**. This is *not* the incorrect mask selecting physical output rows 0,4,8,... The previous provisional claim of no early-factor pruning from the incorrect mask was explicitly corrected in the same iteration.

[DERIVED] Source-level full factor stages [11,10,9,8], [7,6], [5,4], [3,2,1], in execution order. Backward dependency from physical output rows 0..511:
  last factor: 512 requested rows need 512 predecessor rows
  third factor: 512 ->512
  second factor: 512 ->512
  first factor: 512 ->2048 input rows.
Thus prune all intermediate factor OUTPUTS to first 512, but the first input remains a full 2048 slot vector.

Structural matrix-nonzero locations under this exact factorization:
  factor             1      2     3      4       total
  pruned full        8192  2048  2048   4096    16384
  small-subring      8192  1024  1024   4096    14336
ratio=8/7≈1.142857 of complex matrix positions. This is NOT a bound on full RNS encoded plaintext memory or runtime; even masked slot vectors can encode into dense ring polynomials.

Exact distinct diagonal-offset supports:
  pruned full: [16,7,7,15], sum=45
  small:       [16,3,3,15], sum=37.
The final mask does not reduce the count of diagonal OFFSETS in this particular true bit-reversed layout (despite reducing nonzero rows).

## Nominal key switching/rotation counts
[DERIVED / MODEL] Mirrored the actual GitHub source `FindBestBSGSRatio` under LogBabyStepGiantStepRatio=1; for the full LCR first factor, BSGS is disabled as code requires. Unhoisted nominal nontrivial automorphism/event counts are:
   stage               factor0 factor1 factor2 factor3  Trace total
   full + LCR (pruned)    15      4       4       6      0    29
   ordinary small CtS      6      3       3       6      2    20
Thus the simple drop-in proposal requires **9 more nominal automorphism/key-switch operations**, although its first step differs in key switching type (LCR+AKS, not ordinary Rotate) and it saves one modulus level. The counts are NOT wall-clock comparable timings; optimized hoisting, GHS scaling, NTT, key memory and AKS preprocessing may change actual trade-off.
Output-format conversion is EXCLUDED: conventional small CtS returns one ciphertext holding both real/imag halves and incurs a repacking rotation; full CtS returns two ciphertexts. To preserve one-ciphertext sparse EvalMod, an ADDITIONAL custom repacking change (likely including a rotation/mask and metadata handling) is needed. The naive full-width code path otherwise processes two ciphertexts in EvalMod, which is not an equal comparison. Do not claim this has been correctly implemented.

## Exact independent verification
[EXPERIMENT] Reproducible `/mnt/data/iteration41_fft_pruning_audit.py`. Follows source algorithms only as independently replicated exact support, not Go runtime execution:
- Exact finite-field q=257: n=8,16 inverse Fourier matrices via modular Gauss–Jordan; `ifftPlainVec` butterfly product equals n*bitreverse(F^-1) on every row, verified.
- q=12289: n=128,t=4, 30/30 random independent input trials verify factor-by-factor zeroing of output rows >=n/4 after each merged factor yields EXACTLY the same retained outputs as the unpruned code's butterflies.
- N=4096,t=4 structural boolean support: 2048 ->512 only in first factor, remaining factors 512 ->512; diagonal support/nominal BSGS counts as above.
- This does not implement CKKS message modraise, LCR/GHS key switching, dual real/imag ciphertext repacking, rescale noise, or performance measurements.

## Outcome / novelty
[NEGATIVE] A bare `Trace -> no Trace; small CtS -> pruned full CtS` substitution is not cost-neutral in the nominal code model and is not a drop-in correct complete pipeline: +9 nominal switches (29 vs20, excluding extra repacking) and a changed ciphertext output interface. No 3–4 factor zero-rotation miracle.
[POSITIVE] The crucial bit-reversal-aware projection permits much stronger factor-wise pruning than an every-fourth-physical-row mask would suggest; encoded plaintext diagonal support *indices* remain limited, and nonzero complex factor entries increase by only 14.3% vs small CtS. Thus a zero-row-pruned full Fourier calculation may still be viable.
[OPEN] One saved modulus level may be worth +9 switches; without empirical or sharper implementation-specific operation weights we cannot conclude runtime superiority/inferiority. Full FHE correctness requires handling conjugate outputs, repacking, precise natural output ordering, trace normalization, scale, and small unreduced integer-lift LCR hypothesis. Implementation status: NOT DONE. Novelty/prior art: existing FFT pruning/trace and scalar fusion are standard; no demonstrated publishable new technique.

## End of Iteration
STATUS: FAIL for the narrow **operation-neutral drop-in** hypothesis, but positive precise bit-reversed pruning finding preserved.
RESULT: Correct output mask selects first 512 physical rows, allowing intermediate rows to prune to 512, but the source BSGS/AKS structure still gives 29 vs 20 nominal switch events plus separate repacking problems.
NEXT_ACTION: PI decides whether +9 model switching calls and a custom real/imag repack justify one tightly scoped LCR precondition + ciphertext-format correctness test at N=4096,t=4 before any benchmark. Default recommendation: pause straightforward SubSum fusion as a novel optimization unless a new mechanism removes the extra switching and format cost.
STATE_UPDATE: NO; RIG-HE parked state in STATE.md remains untouched.
