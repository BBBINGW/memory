# Iteration 44 — Sparse LCR+AKS: asymmetric CtS/StC cannot be configured as an unmodified drop-in

Date: 2026-10-10
Branch: CKKS sparse SubSum–Fourier fusion, follow-up to I40–I43.
STATUS: FAIL for the specific **unmodified bootstrapping parameter/API drop-in** hypothesis; UNCLEAR for actual ciphertext correctness because the real Go test could not execute.
NOVELTY NOT VERIFIED / LOW: this is an implementation-composition barrier and missing end-to-end evidence, not a published-algorithm correctness attack or proven Pareto gain.

## Read-before-write / prior work
Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, I42 finding `findings/ckks-sparse-cts-two-rotation-repack.md` and I41 failure `failures/ckks-lcr-aks-bitreversed-pruning-no-free-cost.md`. Source-level rationale from I40–I43 preserved. Do NOT alter STATE.md (distinct parked RIG-HE direction).

## Exact source provenance
[FACT] Public author's fork `Fainabi/Lattigo-LCR-AKS`, branch `lcr`, commit `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4` via connected GitHub app; primary Yan et al. *Faster Bootstrapping for CKKS with Less Modulus Consumption*, ePrint 2025/1403 §3 Remark1, §5.1 (cached full paper last iterations, PDF mirror VERSION_UNVERIFIED).
- `circuits/ckks/bootstrapping/parameters.go`, `NewParametersFromLiteral`, lines ~98–113, obtains **one** `LogSlots` from `btpLit.GetLogSlots()`, uses it to construct both CoeffsToSlots and SlotsToCoeffs factor scales/depth.
- Same `parameters.go`, lines ~135–145: `S2CParams.LogSlots = LogSlots`; lines ~210–221: `C2SParams.LogSlots = LogSlots`. There is no independently exposed C2S/S2C LogSlots parameter in this constructor. A proposal needing **full CtS LogSlots=11** and **sparse StC LogSlots=9** therefore cannot be configured through this original literal alone. This does NOT preclude source changes or direct, carefully recomputed Parameters struct manipulation.
- `circuits/ckks/bootstrapping/evaluator.go`, `ModUp` at ~934, unconditionally finishes with `eval.Trace(ctIn, eval.CoeffsToSlotsParameters.LogSlots, ctIn)`. LCR must happen before SubSum rotations/KS; simply changing CtS matrix settings does NOT remove Trace. An explicit bypass and rebalancing of subsequent matrix metadata are required.
- `circuits/ckks/bootstrapping/parameters.go`, `GaloisElementsRemoveAggregatedFlags` lines ~502–526, generates ordinary rotation keys for `i = p.LogMaxDimensions().Cols ... LogN-2`; `p.LogMaxDimensions().Cols` from `SlotsToCoeffsParameters.LogSlots`, not necessarily new CtS. With S2C still at 9, both original ordinary trace keys +512/+1024 remain included: Galois elements 6145 and 4097 modulo 8192 (N=4096).
- `circuits/ckks/bootstrapping/keys.go`, `GenEvaluationKeys` at ~118–146 stores these as normal Galois keys in `MemEvaluationKeySet` separate from `EvkAggregatedGaloisKeys`. No extra key types needed for *the ideal left-rotation repack* in this conditional configuration.
- `circuits/ckks/dft/dft.go` lines ~383–516: CtS full returns 2 ciphertexts; sparse StC expects `ctImag=nil` and one real||imag ciphertext; `dftLevelConserved` preserves input `LogDimensions` and first-factor LCR evaluation is separate. `core/rlwe/evaluator_automorphism.go` copies input metadata on automorphism, does not turn full into sparse for free.
- `circuits/ckks/bootstrapping/evaluator.go` ~48–150 `NewEvaluator` also checks the CtS/EvalMod/StC level chain and the required evaluation keys; any dimension-specific patch must be accompanied by coherent matrix regeneration, level, metadata and key regeneration.

## Primary hypothesis and falsification condition
[HYPOTHESIS — FAIL] The two-rotation repack proven algebraically in I42/I43 can be integrated end-to-end as a config-only/unchanged-source replacement of pre-CtS SubSum by a full pruned `LogSlots=11` CtS, retaining sparse `LogSlots=9` StC in the author's bootstrapping API.
[FALSIFIER] Any hard-coded single `LogSlots` coupling CtS and StC, or an unconditional `ModUp -> Trace` that has no configuration switch, blocks this exact no-source-change hypothesis.
[TEST — decisive source-level] Inspect pinned source definitions. Found BOTH obstacles as above. This is not evidence the algorithm could never be implemented by changing the source.

## Key-reuse and exact algebra rechecked
[DERIVED / REPRODUCED] For N=4096, full slots n=2048, t=4,m=512:
  R=(r,0,0,0), I=(i,0,0,0),
  T=R+RotateLeft(I,+512)=(r,0,0,i),
  C=T+RotateLeft(T,+1024)=(r,i,r,i).
  IDs: 5^512 mod8192=6145; 5^1024 mod8192=4097. With sparse S2C LogSlots=9 the original ordinary trace key-generation loop includes both. The *prior I43 right-rotation* alternative requires -512 whose ID=2049 is not guaranteed by this same loop.
[EXACT EXPERIMENT] Reran in current container `/mnt/data/iteration43_sparse_repack_galois_audit.py`: 100/100 independent q=12289 full 2048-slot tests passed; reran `/mnt/data/iteration42_sparse_cts_repacking_audit.py` which verified finite-field Fourier and subring conditions 600/600 and 300/300. These are **plaintext toy tests** only, not ciphertext proof.
[CONDITIONAL COST] Full pruned LCR+two rotations vs baseline sparse estimated 31 vs 21 **nominal** automorphism/key-switch events, but these are not apples-to-apples latency or security/precision metrics. The algebraic key reuse does NOT eliminate extra switching work.

## Actual Go ciphertext test — attempted but BLOCKED
[EXPERIMENT / NOT EXECUTED] Existing `/mnt/data/iteration43_lattigo_sparse_repack_test.go` is present and gofmt syntax check passed under Go 1.23.2. Test source intends to encrypt two zero-padded full-SIMD vectors, apply Rotate+512/+1024 and adds, decrypt and verify slots and metadata, set LogDimensions=9, and compare sparse SlotsToCoeffsNew with directly encrypted baseline. It is a standalone repack/StC test, **not** a test of actual pruned full CtS, LCR, EvalMod or entire bootstrapping.
- No fork source or Lattigo v6 modules cached on local filesystem. `git ls-remote https://github.com/Fainabi/Lattigo-LCR-AKS.git HEAD` failed DNS resolution; `curl https://proxy.golang.org` failed DNS resolution. A temporary Go module probe with the author's go.mod requires and `GOPROXY=off GOSUMDB=off go mod download all` failed: `go: module lookup disabled by GOPROXY=off`.
- Therefore NO actual `go test` was executed in an authentic fork tree; no ciphertext-level result exists. The proposed test is uncompiled against real package definitions, hence may have runtime/API errors.
- Explicitly changing `LogDimensions.Cols` in a test is a metadata interface compatibility probe, not an algebraic equivalence proof. Follow-up tests must ensure numeric correct, scale, levels, IsBatched and trace-normalization with exact author pipeline.

## Result and strategic disposition
[NEGATIVE] The bare configuration-only replacement of Trace + sparse CtS by full CtS and later sparse StC is blocked by concrete source-level LogSlots coupling and unconditional Trace. This is a narrow claim; not a proof that a revised pipeline or CKKS scheme cannot do it.
[POSITIVE] Existing ordinary Galois keys remain reusable IF S2C stays LogSlots=9; two-left-rotation repack exactly maps target slots and uses no extra multiplication depth.
[OPEN] Actual ciphertext correctness (pruned CtS input/output messages, modified bootstrapping source, metadata, precision, EvalMod and StC) remains untested due missing Go dependencies/network. Pruned matrices, first-stage LCR scale, and output-format-specific key generation must all be checked. No benchmark and no Pareto improvement established.
[PRIOR ART/NOVELTY] Relative trace and FFT pruning/repacking are established; this source-level integration work is routine engineering until a new technical mechanism removes cost. NOVELTY LOW/NOT VERIFIED. Do not spend more iterations on nearby plaintext toy checks.

## End of Iteration
STATUS: FAIL (config-only seamless integration), UNCLEAR (actual ciphertext).
RESULT: Single public LogSlots populates both CtS and StC; ModUp invokes Trace unconditionally; therefore full-CtS/sparse-StC+no-Trace needs source changes. Keys +512/+1024 already exist under original sparse S2C setting, but Go ciphertext test is blocked by dependency availability.
NEXT_ACTION: HUMAN_REVIEW: decide ARCHIVE this low-priority, cost-negative branch or explicitly fund a local Lattigo checkout/build and ONE end-to-end test in a source-modified fork. If continuing, first obtain a working copy with dependencies and implement asymmetrical C2S=11/S2C=9 plus ModUp Trace bypass, then execute the single previously drafted repack/StC Go test, without benchmarking until correctness passes.
STATE_UPDATE: NO; preserve unrelated parked RIG-HE STATE.md.
