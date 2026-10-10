# Iteration 42 — Two-rotation real/imag repack from pruned full CtS to sparse CtS format

Date: 2026-10-10
Branch: CKKS sparse-packing compatibility with LCR+AKS
STATUS: PASS only for exact **plaintext Fourier and slot-format compatibility** with **zero added multiplicative depth**. Not a running homomorphic CKKS implementation, not a measured performance optimization, novelty NOT VERIFIED.

## Continuity / research protocol
[FACT] Before working, read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, `failures/ckks-lcr-aks-bitreversed-pruning-no-free-cost.md` (I41), and `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md` (I40). STATE.md tracks unrelated parked RIG-HE; unchanged.

## Primary hypothesis and minimal test
[HYPOTHESIS — PASSED at plaintext/slot level] Under I40/I41's exact Fourier trace projection and correctly pruned full CtS, the two fully-packed outputs for the real and imaginary coefficient vectors can be converted into the **same one-ciphertext sparse CtS plaintext layout** required by Lattigo's subsequent sparse EvalMod and StC, using only existing rotation/addition primitives and **no extra rescale / multiplicative level**.
[FALSIFICATION CONDITION] If no shift-and-add formula can simultaneously (i) place the 512 real and 512 imaginary coefficients in their required positions and (ii) ensure the resulting full-slot vector is fixed by the subring embedding's period-1024 symmetry, the simple no-depth repack fails.
[TEST] One fixed toy n=32,m=8,t=4 over F_12289, exact full/small canonical Fourier inverses, bit-reversed coefficient location, comparison of 1 vs 2 Galois slot shifts, verification of subring coefficient invariant. No expensive FHE implementation.

## Sources read (read at pinned public repository branch)
[FACT / SOURCE CODE] `Fainabi/Lattigo-LCR-AKS`, public branch `lcr`, GitHub branch HEAD `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4` retrieved through connected GitHub app:
- `circuits/ckks/dft/dft.go`, lines 383–470: `CoeffsToSlotsNew` returns two ciphertexts when full LogSlots==LogMaxSlots, and one when sparse LogSlots<LogMaxSlots; `CoeffsToSlots` forms real and imaginary outputs by conjugation and additions and, for sparse, rotates imaginary by `1<<ctIn.LogDimensions.Cols` before adding to real.
- `circuits/ckks/dft/dft.go`, lines 515–560: result `LogDimensions=inputLogSlots` is retained across DFT. Lines 666–728 implement the CoeffsToSlots inverse butterfly. Lines 985–993 zero the upper-half rows when `RepackImagAsReal` is used in sparse IFFT, while `ifftPlainVec` duplicates twiddle vectors across two halves of size `slots`. Thus the *unrepacked* sparse CtS DFT output has a period 2m and active half m.
- `circuits/ckks/dft/dft.go`, lines 474–516: `SlotsToCoeffsNew(ctReal,ctImag,...)` has two paths, and `ctImag=nil` chooses the sparse one-ciphertext path. `circuits/ckks/dft/dft_test.go` lines 120–250 and 305–419 explicitly test sparse real||imag format and coefficient decoding.
- `schemes/ckks/evaluator.go`, lines 1193–1205: `Rotate` is a left cyclic shift in SIMD coordinates and invokes `Automorphism` with a Galois key. To realize mathematical **right** shifts in our formula, pass the corresponding negative CKKS rotation parameters, i.e. -m and -2m modulo full SIMD length n, not the paper's unqualified positive signs.
- `circuits/ckks/bootstrapping/evaluator.go`, lines 688–716: EvalMod invokes once if sparse ctImag=nil, twice for full ctImag !=nil.
- `circuits/ckks/bootstrapping/evaluator.go`, lines 933–964: `ModUp` ends with `Trace` and `SlotsToCoeffs` passes through the dft evaluator.
- `circuits/common/lintrans/lintrans.go`, lines 320–367: BSGS ratio / rotation counts from preceding I41.
The underlying PKC 2026 paper Yan et al., ePrint 2025/1403, §3 Remark1 physical p.14 and §5.1 pp.23–24 remains the baseline. Source code version is public lcr branch commit above; **no local Go end-to-end CKKS test** was run.

## Derivation and exact structural format
[DERIVED] Let CKKS ring degree N=4096, full n=N/2=2048 SIMD slots, original sparse meaningful m=n/t=512 slots and t=4. Under the I40 Fourier-projection and I41 bit-reversed pruning, the two *ideal plaintext* split ciphertext outputs have full-slot vectors
  C_R=(r,0,0,0),  C_I=(i,0,0,0),
where every block contains m=512 slots. The original sparse CtS output is NOT merely `(r,i,0,0)`. Due to the author's sparse RepackImagAsReal encoding in a subring with 2m distinct slots, its correct full-slot vector is `(r,i,r,i)` (period 2m=1024). In other words its plaintext polynomial lies in the subring with `Y=X^2`, concretely `F_q[Y]/(Y^(N/2)+1)` inside `F_q[X]/(X^N+1)` when working over a suitable CRT prime q.

Define `Sh^R_k` as the RIGHT cyclic slot shift of the full n-SIMD vector by k, equivalent to Lattigo left `Rotate(-k)`.
  T := C_R + Sh^R_m(C_I) = (r,i,0,0)
  C_sparse := T + Sh^R_(2m)(T) = (r,i,r,i).
Therefore two rotations (by -m and -2m in the public API convention) and two ciphertext additions suffice to produce the required periodic ciphertext **plaintext layout** with zero extra multiplications/rescalings. Actual rotations add key-switch noise and need ordinary Galois keys. Before the second shift, (r,i,0,0) is generically not in the requisite Y=X^2 subring and cannot be passed off as an equivalent sparse result.

A separate scalar issue: the I40 mask includes factor t=4 and original small CtS/trace has own normalization, so equal scaling must be absorbed into factor matrices. This is assumed when we write r,i as the final desired outputs; exact toy confirms full versus small normalization at finite-field level for the chosen transform conventions.

## Independent exact finite-field test
[EXPERIMENT] Script `/mnt/data/iteration42_sparse_cts_repacking_audit.py`, stdout `/mnt/data/iteration42_sparse_cts_repacking_results.txt`; random seed 20261042, N=64, n=32, t=4, m=8, q=12289, primitive generator 11. Exact modular Gauss–Jordan inverses for full Galois-ordered Fourier F_n and subring Fourier F_m. Verify full trace/fusion coefficient relation for independent arbitrary z_R and z_I:
  `(F_m^-1 (S_t z)|_(first m))_k = t (F_n^-1 z)_(t*k)` modulo q.
Physical coefficient outputs have bit-reversal, so selected full physical rows are `bitrev_5(4k)`, which form the set 0..m-1 BUT are not in increasing k order. In the code-level physical order the small-output values are `[c_(bitrev_3(j))]_(j=0..m-1)`; this permutation was caught by the initial assertion failure and corrected, no invalid order assumption remains.

Test 300 independently sampled pairs:
- 600/600 full-to-small Fourier identities exact PASS.
- 300/300 two-rotation layout equality `(r,i,r,i)` exact PASS.
- 300/300 output period-2m invariant exact PASS.
- 300/300 inverse full Fourier coefficients vanish at odd monomial degrees, checking the `X^2) subring condition.
- 300/300 single-rotation-only candidate `(r,i,0,0)` fails this subring invariant; this is an empirical witness for the chosen random inputs, not a universal minimum-rotation lower bound.

This is finite-field plaintext algebra, NOT Lattigo CKKS encryption, actual Galois keys, key-switch noise, scale/ModDown or numerical precision. The existence of a two-rotation solution is rigorous from slot algebra. Compatibility of the entire CKKS pipeline has not been tested.

## Cost implications / unresolved issues
[DERIVED / CONDITIONAL] Previous I41 nominal counts were 29 pruned-full-with-LCR versus 20 baseline Trace+small-CtS, EXCLUDING output real/imag repack. Counting the natural output repack in BOTH options gives:
- pruned full: 29 + TWO rotations = 31 events;
- conventional sparse: 20 + ONE existing repack rotation = 21 events.
Difference +10 nominal switch/automorphism events in this simple source-level model. They are NOT equivalent-walltime events: LCR+AKS/GHS keys can differ in cost from ordinary switches, and hoisting can alter latency. Baseline also does not receive LCR's one-level saving.
[OPEN] Is `Rotate(-m)`, `Rotate(-2m)` already present in the existing Galois-key set? The first factor's *aggregated* level-conserved keys do not automatically serve as ordinary Galois keys; key material may grow. Not checked.
[OPEN] How to correctly encode/zero the last factor, match the actual error/scale metadata, insert the two-rotation custom repack into Go `CoeffsToSlots`, and preserve `LogDimensions` and `IsBatched` under real ciphertext operations? Not implemented. Note `dft.go` propagates input LogDimensions but full matrix is instantiated for LogSlots=11; runtime checks/format assumptions may require explicit handling.
[OPEN] EvalMod precision and S2C correctness with the new noise and modified data flow. Need a true ciphertext-level test before any claims.
[PRIOR ART] SIMD rotate-and-add, sparse repacking and trace are standard; this 2-rotation construction is not evidence of a publishable contribution. I40 Fourier fusion + I41 bit reversal remains conditional and non-cost-neutral.

## End of iteration
STATUS: PASS (plaintext slot and subring-format compatibility; zero additional multiplicative depth), but UNCLEAR for ciphertext implementation and full bootstrapping.
RESULT: Correct sparse result requires (r,i,r,i), not (r,i,0,0). Two cyclic SIMD shifts by m and 2m with two additions yield it exactly; one shift alone fails periodicity. In the simple source-count model it adds one more rotation than ordinary sparse CtS and makes the count ~31 vs21, not a free performance win.
NEXT_ACTION: If PI authorizes continued work on the branch, inspect whether the existing normal (nonaggregated) rotation-key set includes -512 and -1024 at N=4096,t=4, then implement ONE ciphertext-level Lattigo CKKS test matching real/imag split, two rotations, and sparse SlotsToCoeffs plaintext result, including metadata and numerical error. Stop if missing keys or incorrect output format before benchmark.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged.
