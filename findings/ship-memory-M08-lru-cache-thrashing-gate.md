# SHIP-M08 — Uniform mux-key scan defeats sub-capacity LRU; pinned prepared set helps only linearly

**Date:** 2026-10-14 (Asia/Tokyo). **Independent series:** SHIP-M08, NOT global FHE I-series, concurrent SHIP I-series, or vFHE V-series.
**PI authorization:** “好的，请继续” following M07.
**Primary target:** evaluate M07 seeded GGLWE mux-key streaming under **repeated real SHIP bootstraps on the same fixed keyset**. No new primitive or switch in parent research direction.
**STATUS:** **FAIL** sub-full-capacity LRU can amortize any mux-key preparation across repetitions in source access order; **PASS** deterministic source-trace cache falsifier and bounded pinned-set alternative; **UNCLEAR** actual Poulpy timing, error, total RAM, implementation/security details and publication novelty.

## Read-before-write and source provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-M07-seeded-gglwe-streaming-feasibility.md` SHA `bbec6947815d523794949c8ea72142ef04db89a8`, M06, independent SHIP `findings/ship-memory-STATE.md` SHA `f77e5b1a48e6d8c7d2cfbefe53a29615599071d8` (concurrent unrelated SHIP I201), and global `STATE.md` SHA `04e4fc1894c1c3868ba73f7410d45663365e6c4d` (separate vFHE V7), strictly to avoid state collision. M08 is a **new independent file**; shared states remain unchanged.

**Original SHIP:** Jung Hee Cheon, Guillaume Hanrot, Jongmin Kim, Damien Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / ePrint 2025/784, especially §5.1 HMuxRot, physical pp23–24, cached Research MCP github mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, `VERSION_UNVERIFIED`. This M08 result depends on **independent Poulpy implementation**, not author HEaaN performance.

**Pinned independent source:** `poulpy-fhe/poulpy`, commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: for `slot in spec.support()`, for each digit-group `b`, keygen produces every candidate `d=0,...,b-1`, **even β=0**, uniquely indexed by (slot,group,d).
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: real `halves=1`, sequential `for (slot,ik) in index_keys.iter().enumerate()` then `for group in ik.mux_keys()`, invoke `ship_mux_rotate` once for each group; same keyset reused for next bootstrap.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: group operation hoists CT DFT then `for key in keys`, performs one GGLWE product and publicly rotates/adds to sum; **every candidate key is used once per group**, no early exit for private digit.
- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: `mux_candidates=ceil((2window+1)/theta)` and mixed-radix `mux_bases`; for source-shaped illustrative `N16384,h32,theta4,window256,mux_base4`, candidates129 and bases `[4,4,4,3]`.
- `poulpy-core/src/layouts/compressed/gglwe.rs`, `poulpy-core/src/layouts/prepared/glwe_switching_key.rs`, `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs`: seeded bodies+independent seeds, decompression/NTT preparation and 16-byte IFMA prepared DFT layout, as source-verified in M07.

**No real Rust run:** In present container, `cargo` and `rustc` are absent; no compiled Poulpy modified evaluator, heap profiler or wall-clock timings. Python below is an **exact source-derived access-trace/cache and byte formula simulation**, not a cryptographic or runtime benchmark.

## ONE primary hypothesis and ONE falsifier

**[HYPOTHESIS M08]** For repeated *real* SHIP bootstraps on a fixed keyset, an otherwise unmodified conventional capacity-limited **LRU cache**, with `0<C<K` simultaneously resident prepared mux GGLWE entries, acquires a positive steady-state cache hit rate and amortizes nonzero numbers of GGLWE NTT preparations relative to seed-only streaming.

**[DECISIVE TEST]** Reconstruct the exact sequence of key IDs `(slot, group, candidate)` from pinned source for ONE bootstrap, repeat it ten times for the same keyset, and simulate LRU at several capacities `C<K` against a static `C`-key pinned prepared set with a separate ephemeral key scratch. A positive LRU hit for C<K would avoid falsification. Derive necessary per-key access distance mathematically rather than relying solely on code.

## Source-trace theorem and deterministic verification

From `h=32`, group sizes `[4,4,4,3]`:
```
K = h*(4+4+4+3) = 480 distinct mux GGLWE keys.
Trace of one real bootstrap:
  [(slot,group,d) for slot in 0..31
                  for (group,b) in enumerate([4,4,4,3])
                  for d in 0..b-1].
```
Every ID occurs **exactly once** in this trace; the trace repeats in **identical order** across real bootstraps using one fixed keyset. For any key, the next occurrence is preceded by exactly K−1 **distinct other keys**. Thus its LRU stack/reuse distance is K, and if `C<K`, it must be evicted before that occurrence. This proof holds for all repeated runs regardless of number of repeats (starting from an empty or warm cache, after reaching this trace's cyclic steady state); a cache initially populated with a specially crafted out-of-phase subset may see a short transient, but no sustained hits in the cyclic trace.

**[EXECUTED ONE TEST]** Python script `/mnt/data/ship_m08_mux_cache_reuse_audit.py` SHA256 `5a2696ebcff8cc7752a2431eddeef257d11181b4021d3913bf93c4e7f43d3bd2`; JSON `/mnt/data/ship_m08_mux_cache_reuse_audit.json` SHA256 `e3bce6ffc1e5bed40930fc727b5f7e1a8583dce1f36efc49f0a4ca1f390e47da`. Standalone script derives source shape, optional cross-checks local M07 JSON, simulates **ten repetitions** of the same 480-key trace with fully specified LRU and pinned policies, and asserts exact formulas for `C∈{0,1,4,60,479,480}`.

| Prepared cache C | LRU hits/boot (steady) | pinned hits/boot (after first pass) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 4 | 0 | 4 |
| 60 | 0 | 60 |
| 479 | 0 | 479 |
| 480 | 480 | 480 |

Pinned cache retains a chosen fixed subset of size C and **uses a separate transient buffer for all remaining keys**, so streaming uncached keys cannot evict the pinned subset. Under this policy:
```
N_LRU(B,C<K) = B*K                           preparations from empty
N_PIN(B,C)   = K + (B-1)*(K-C)                 preparations from empty
N_EAGER(B)   = K                               preparations once; retain all K
```
With ten bootstrap operations and C60: LRU 4800 preparations, pinned 4260 preparations; 12.5% lower **steady** prep count, 11.25% lower across these ten. No key products are eliminated: still `B*K` GGLWE products.

**[Mem bound, same illustrative source IFMA layout from M07]**
```
N=16384,h32,theta4,window256,mux_base4,base2k52,ld40,budget104,dsize1
raised_k=468,dnum9,kaux52,key_size_limbs10
Each mux prepared key P = 90 MiB
Each unprepared key R = 45 MiB
Each compressed body+18 independent PRG seeds=22.5 MiB + 576 bytes
All 480 compressed = 10.547132492 GiB
One ephemeral R+P = 135 MiB
Base streaming resident mux-related buffers M0 = 10.678968430 GiB
With explicit mux-related cap Mmax=16 GiB:
  Cmax=floor((Mmax-M0)/90 MiB) = 60
  memory used M0+60*90MiB ≈ 15.95240593 GiB
Prepared key visits per bootstrap after warm: 420 misses.
NTT polynomial-limb calls: 420*360 = 151,200 per bootstrap
(versus 480*360=172,800 for LRU/no-pinning).
```
The 16GiB budget applies **only to these mux-related representation buffers**; NOT entire SHIP keyset, peak process RSS, all DFT scratch, OS cache and parallel-inflight buffers. For >1 worker memory formula changes.

**[Symbolic time breakpoint — no invented timing]**
Let `T_m` denote real one-key GGLWE product elapsed time, `T_p` real decompression+DFT preparation per key, `T_other` remainder of bootstrap; assume same T_m and T_other across layouts, and ignore contention, allocator, file IO, backend concurrency effects.
```
T_eager(B) = K*T_p + B*K*T_m + B*T_other
T_pin(B,C) = [K + (B-1)*(K-C)]*T_p + B*K*T_m + B*T_other
T_LRU(B,C<K) = B*K*T_p + B*K*T_m + B*T_other
```
In warmed steady-state, restricting **mux-only** online slowdown relative to preprepared all-K baseline to ≤δ requires
`(K-C)*T_p <= δ*K*T_m`.
For C60, δ0.1, `T_p/T_m <= (0.1*480)/420 ≈ 0.1142857143`.
This is a **conditional, measurable criterion**, NOT evidence real Poulpy meets or fails it. Inclusion of other stage latency `T_other` would alter a *total bootstrap* 10% comparison.

## Judgment and limitations

**[FAIL primary hypothesis]** Normal LRU with C<K has zero steady prepared-key reuse for the fixed-keyset real SHIP execution trace; merely adding LRU does not amortize preparation.
**[PASS conditional alternative]** Static pinning of C prepared keys yields precisely C reused prepared entries per warm real bootstrap and leaves all other keys compressed+streamed. At 16GiB *mux-only* budget, C≤60, so 420/480 still need online preparation and at least 151,200 polynomial-limb forward NTT operations per real bootstrap under the M07 method.
**[OPEN]** No compiled timing, error or RSS; no quantitative evidence that T_p/T_m <=0.1143; cryptographic security relies on the exact underlying independent seeded key material, whose original joint security was not newly proven. Cache policy itself does not change ciphertext bytes. No claim of new cryptographic contribution. Big batches with key-major ordering, complex SHIP halves reusing keys, multiple keysets, or a different cache replacement policy produce different traces; M08 does **not** establish a universal cache impossibility. Source parameter shape illustrative, not security-certified.

## End of iteration

**STATUS:** **FAIL** LRU amortization hypothesis; **PASS** source access-pattern cache-thrashing witness; **UNCLEAR** production performance / security / peak RAM / novelty; **HUMAN_REVIEW** on whether to pursue straightforward caching.
**RESULT:** Fixed order all-480-key cyclic scan forces LRU(C<480) hit rate 0. Pin C avoids this at explicit capacity price; under 16GiB mux-buffer example C=60, warm preparation count 420, and a <10% mux-only slowdown demands T_p/T_m≤0.1143, currently unmeasured.
**NEXT_ACTION — ONLY IF PI CONTINUES (SHIP-M09):** ONE **key-major batching schedule feasibility gate**: test whether Q independent bootstrap ciphertexts can process a common mux digit group in lockstep, prepare each candidate key once, apply that prepared key across all Q per-ciphertext DFT accumulators, then release it; verify source dependency/order constraints and bound Q-fold extra live accumulator memory. One primary hypothesis and one source-specific cheapest proof/counterexample; no real speed claim without toolchain. Alternative HUMAN_REVIEW: park engineering cache branch and pivot to deeper rank/dsize/mux-key-count reduction, PI decides.
**STATE_UPDATE:** YES this standalone `findings/ship-memory-M08-lru-cache-thrashing-gate.md`; shared `STATE.md` and concurrently advanced `findings/ship-memory-STATE.md` NOT modified; M08 self-contained, next M09 not started.
