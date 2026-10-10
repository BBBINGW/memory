# Iteration 43 — Reuse ordinary SubSum Galois keys for left-rotation sparse CoeffsToSlots repack

Date: 2026-10-10
Branch: CKKS sparse packing / LCR+AKS SubSum–Fourier fusion, continuation of Iterations 40–42
STATUS: PASS for **key-availability and ideal slot-level compatibility**, UNCLEAR for actual CKKS ciphertext / metadata / precision and full bootstrapping.
NOVELTY: LOW/NOT VERIFIED. This is a key-generation interface observation, not a new FHE primitive.

## Research protocol / prior state
[FACT] Read current GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, I42 finding (`findings/ckks-sparse-cts-two-rotation-repack.md`) and I41 negative result before selecting the test. Preserve STATE.md (unrelated parked RIG-HE) and all existing archives. One active hypothesis, one minimal decisive exact test.
[FACT / ORIGINAL] Yan et al., *Faster Bootstrapping for CKKS with Less Modulus Consumption*, ePrint 2025/1403, PKC 2026, §3 Remark1 physical p.14 and §5.1: pre-LCR sparse SubSum obstruction, LCR+AKS applicable to first CtS layer; full original PDF obtained and checked in I40, 51 physical pp, SHA256 784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29, VERSION_UNVERIFIED.
[FACT / CODE] Public author's fork `Fainabi/Lattigo-LCR-AKS`, branch `lcr`, commit `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4`, inspected through connected GitHub app:
- `circuits/ckks/bootstrapping/parameters.go`, `GaloisElementsRemoveAggregatedFlags` (approx lines 504–525): adds `params.GaloisElement(1<<i)` for all `i` from `p.LogMaxDimensions().Cols` to `params.LogN()-2`; `p.LogMaxDimensions().Cols` comes from sparse `SlotsToCoeffsParameters.LogSlots` (§same file lines 387–395), not necessarily from a full-sized replacement CoeffsToSlots matrix.
- `circuits/ckks/bootstrapping/keys.go` (approx lines 117–130): when `LevelConserved`, builds **ordinary** Galois keys by `GenGaloisKeysNew(p.GaloisElementsRemoveAggregatedFlags(...))`, stored in `MemEvaluationKeySet`; separate from `EvkAggregatedGaloisKeys` and `EvkLevelConserved`.
- `schemes/ckks/evaluator.go` lines 1193–1208: `Rotate(ct,k)` rotates SIMD slots to the **left** by k, requiring a corresponding ordinary Galois key.
- `core/rlwe/evaluator_automorphism.go`: `Automorphism` requires `CheckAndGetGaloisKey(galEl)` and copies ciphertext metadata from input into output; rotation does NOT automatically update full vs sparse LogDimensions.
- `circuits/ckks/dft/dft.go` lines 383–470, 474–516, 515–560: full CtS yields two ciphertexts, sparse CtS yields one with real||imag data; dft output inherits `ctIn.LogDimensions`. SlotsToCoeffs branches on `ctImag==nil`, with a distinct sparse transform.
- `circuits/ckks/bootstrapping/evaluator.go` ~688–716: EvalMod called once if sparse `ctImag=nil`; twice if full.

## Primary hypothesis and cheapest falsifier
[HYPOTHESIS] At N=4096, t=4, n=N/2=2048, m=n/t=512, the already-generated **ordinary** rotation keys of the original sparse `LogSlots=9` bootstrap suffice to repack two pruned-full CtS outputs into one sparse-format ciphertext, with NO NEW Galois key types and NO multiplicative-depth overhead, by choosing a *different shift direction* than the I42 right-shift formula.
[FALSIFIER] Either the required Galois IDs are not in the *nonaggregated* `GaloisElementsRemoveAggregatedFlags` key set, or the alternate shift signs fail the exact `(r,i,r,i)` slot identity.

## Exact key derivation
[DERIVED / VERIFIED] Power-of-two CKKS ring degree N=4096 has 2048-element 5-power rotation subgroup modulo 2N=8192:
  GaloisElement(k)=5^k mod8192.
In the original sparse bootstrap, `SlotsToCoeffsParameters.LogSlots=9` and `LogN=12`. The key-generation loop has `i=9,10` and thus explicitly includes ordinary keys
  rot(+512) -> 5^512 mod8192 = **6145**,
  rot(+1024) -> 5^1024 mod8192 = **4097**.
The I42 **right** shift used `Rotate(-512)` whose key is 5^1536 mod8192 = **2049**, not guaranteed by this loop. `Rotate(-1024)` is self-inverse and uses 4097.
So the alternate LEFT-rotation repack avoids the 2049 key:
  C_R=(r,0,0,0), C_I=(i,0,0,0), each block m slots,
  T = C_R + Rotate(C_I,+512) = (r,0,0,i),
  C = T + Rotate(T,+1024) = (r,i,r,i).
Both operations use **already generated ordinary SubSum keys** *provided the sparse SlotsToCoeffs LogSlots=9 key-generation setting is retained even though pre-LCR Trace execution is removed*. This is a valid conditional no-additional-key-material result, not a claim about configurations in which all LogSlots values are changed to 11.

## One exact minimal test
[EXPERIMENT] `/mnt/data/iteration43_sparse_repack_galois_audit.py` and output `/mnt/data/iteration43_sparse_repack_galois_results.txt`, deterministic Python seed 20261043:
- Verified exact Galois key IDs modulo 8192, presence of +512/+1024, absence of -512 from the explicitly guaranteed SubSum key subset.
- Used q=12289 arithmetic on 2048-slots vectors, 100 randomized independent choices of real/imag 512-slot blocks. All 100 exact modular repacks with +512,+1024 yield (r,i,r,i), equal to the I42 right-shift approach, satisfy period 1024; intermediate T is not periodic.
- No encryption or Lattigo calls in this Python test. Correctness is **plaintext SIMD**, not an actual cryptographic FHE test.

## Attempt to execute real Lattigo ciphertext test and blocker
[EXPERIMENT/ENVIRONMENT BLOCK] Wrote a targeted Go test proposal `/mnt/data/iteration43_lattigo_sparse_repack_test.go`; formatted with `gofmt`; it encrypts two full-SIMD vectors under the same key, calls `Rotate(+512)`, `Rotate(+1024)`, Add, compares decrypted slots, checks Scale/LevelQ, explicitly sets sparse `LogDimensions.Cols=9`, and invokes actual `dft.SlotsToCoeffsNew(repacked,nil,stcMatrices)` versus a directly encrypted sparse reference.
Actual `go test` failed at the SETUP stage: Go 1.23.2 is installed, but the Lattigo v6 packages are absent from the local module cache, and the execution container cannot resolve github.com to download them (`git ls-remote` DNS failure). Thus the Go test source is **unexecuted and not compile-verified against the fork**, and its metadata/numeric assertions are PENDING. Test source has no benchmark and uses insecure small toy parameters by design; do not assert it works.
The requested full Lattigo ciphertext result is therefore NOT obtained, and no claim of full bootstrapping correctness, numeric precision, LCR validity, or EvalMod/StC integration is warranted.

## Consequences / research judgment
[POSITIVE] Missing **ordinary rotation keys** need not be a blocker for a sparse-S2C retaining configuration: the existing +512/+1024 key pair is enough for ideal slot-layout repacking at constant two rotations plus two ciphertext additions, no new multiplicative depth or keys in this scope. Unlike last iteration's right-rotation version, this works with ordinary keys explicitly present by source.
[OPEN] Does the pruned full CtS truly yield independently zero-padded ciphertext *messages* under the same scale and correct metadata as assumed? Does the actual Go code permit reinterpreting `LogDimensions=9` after repack? Does subsequent sparse S2C produce the matching coefficient plaintext, and how much noise do the two rotations add? No actual Go result.
[NEGATIVE / ECONOMICS] The previous nominal operation model remains 31 repacked-pruned-full vs 21 conventional sparse, with different LCR/AKS switch costs and one saved modulus level; reusing keys improves KEY SIZE but does not remove the extra rotation events or prove performance.
[PRIOR ART] Rotation/addition layout packing and reuse of existing SubSum rotation keys are routine CKKS engineering ideas. No nontrivial Pareto improvement, publishable gap or novel technique verified. Preferred strategic recommendation: pause this branch rather than repeatedly extending toy parameter tests, unless the PI specifically prioritizes acquiring a working Lattigo v6 environment and implementing a source-level Pruned C2S for real FHE integration.

## End of Iteration
STATUS: PASS (existing ordinary Galois key sufficiency and alternate exact slot repack), UNCLEAR (true Lattigo ciphertext integration).
RESULT: Substitute rotations +512/+1024 for prior -512/-1024, reusing ordinary SubSum keys (IDs 6145/4097) in `LogSlots=9` configuration; 100/100 exact 2048-slot tests PASS; actual Go test not executed due missing modules/network.
NEXT_ACTION: Human decides whether to prioritize setting up an actual Lattigo test environment and a pruned C2S prototype, or archive this low-novelty cost-negative branch. If approved, first place `iteration43_lattigo_sparse_repack_test.go` in the author fork's `circuits/ckks/dft/` directory and run the single named Go test, then inspect metadata failure before any LCR benchmark. Do not automatically run unrelated branches.
STATE_UPDATE: NO — keep unrelated parked RIG-HE state.
