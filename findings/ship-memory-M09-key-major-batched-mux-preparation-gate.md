# SHIP-M09 — Key-major batching amortizes seeded HMuxRot preparation across independent CKKS ciphertexts

**Date:** 2026-10-14, Asia/Tokyo. **Research branch:** SHIP independent `M`-series, **M09 COMPLETED, M10 NOT STARTED**. **PI authorization:** “好的，请继续” following M08.
**Parent research target:** reduce *resident/prepared SHIP evaluation-key memory* while retaining key-digit secrecy and tolerable performance.
**STATUS:** **PASS** source-loop dependency reordering / exact toy ring-operator equivalence and conditional prepared-key work count; **UNCLEAR / IMPLEMENTATION_BLOCKED** actual CKKS precision, real latency, RSS, full key security, novelty.
**Scope:** simultaneous batch Q independent **real SHIP bootstraps under exactly the same keyset and parameters**, not cross-keyset batches or arbitrary single-input latency.

## Read before write & conflict isolation

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, M08 `findings/ship-memory-M08-lru-cache-thrashing-gate.md` SHA `a740c1b0749a29472139b0b29f45e3bc0aeaa1a6`, M07 SHA `bbec6947815d523794949c8ea72142ef04db89a8`, concurrent SHIP `findings/ship-memory-STATE.md` SHA `734e89ae809492d54c0b7e340735de3a98e474b1` **I202**, and shared `STATE.md` SHA `b3a529a05dd7d3250a12b978d914aab873d9ff24` **vFHE V8**, only for context/collision detection. They are separately maintained; **do not overwrite** either. This standalone M09 record contains next action.

**Original paper:** Cheon, Hanrot, Kim and Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, §5.1 HMuxRot and its hoisting discussion, source mirror PDF 33pp SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. SHIP authors' HEaaN **not** tested.
**Independent verified code:** `poulpy-fhe/poulpy` **pinned at `250d4392656cd313f92ca66d96d8865702d39ddf`**.

## Prior branch findings

M05 source allocation of illustrative `N16384,h32,theta4,base2k52,ld40,outputbudget104,muxbase4,dsize1`: prepared mux keys 480×90MiB=42.1875GiB vs prepared selector 2.25GiB. M06 **FAIL** single related encrypted-zero key copied by public Galois transforms: equality of normalized keys leaks private digit. M07 **PASS conditional** independent seeded **body+mask seeds**, decompress/prepare one mux key at a time, at compressed 480-key material+one key workspace ≈10.679GiB but at **480 preparations per bootstrap** and 172800 forward polyn-limb NTTs. M08 **FAIL** ordinary LRU with C<480 over fixed cyclic scan: hit rate zero; static pinned C keys offers only linear partial reuse.

## ONE primary falsifiable hypothesis + one cheapest decisive gate

**[HYPOTHESIS]** When `Q>=2` independent encrypted inputs are bootstrapped using the **same** fixed SHIP keyset, the `ship_mux_rotate` stage can interchange iteration order across ciphertexts and candidates **within each fixed (support slot, mux group)**: prepare each independently seeded candidate key once, apply it to all Q independent ciphertext DFT accumulators, then discard it. This leaves each ciphertext's candidate-group sum and per-group normalization algebraically equal to original ciphertext-major execution, reduces **online key preparation events from QK to K per batch** for K distinct mux keys, and introduces bounded O(Q) live per-group ciphertext scratch instead of O(K) permanently prepared mux keys. It does not remove QK products.

**[FALSIFIER]** Inspect exact pinned source for any per-candidate state mutation, ciphertext-specific key material, non-commutable dependency between distinct ciphertexts, or demand for all keys simultaneously. Construct ONE executable exact `Z_q[X]/(X^N+1)` rank2→rank1 2×2 polynomial-gadget **operator schedule** with candidate-dependent nonidentity Galois transforms and per-group normalization, compare ciphertext-major vs key-major schedules bit-for-bit for a fixed batch of Q ciphertexts. If any leaf differs or key must depend on input ciphertext, FAIL. Derive source-backed buffers and transform invocations as a second *accounting part* of this one schedule-equivalence test.

## Pinned source facts

- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: each encrypted input uses `ckks_ship_coeff_encodings_impl` and `ship_masking_accumulate` (dependent on **that** input); `for (slot,ik) in keys.index_keys().iter()` loops each slot; each mux `group` is sequentially applied to same leaf ciphertext before moving to next group. Each input is otherwise independent and uses the same keyset. Roots/product trees are after all leaves.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: keygen `for slot, for digit-group, for candidate d` builds key of **secret digit** and public rotation only, not dependent on runtime ciphertext; `beta_d` one-hot is fixed by key material; `mux_keys` fully shared across all evaluated inputs.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: computes `a_dft` once **per ciphertext-group**, initializes `sum_dft`, iterates candidate keys in order, calls `gglwe_product_dft_reference(a_dft,key)`, publicly applies output Galois automorphism, accumulates in `sum_dft`; only AFTER finishing group, one IDFT+normalize to advance ciphertext to next group. Candidate keys are immutable to evaluator, but current signature `keys:&[HMuxRotKeyPrepared]` demands refactoring, batch live buffers and scratch isolation. The `term_count` argument must remain group size, not batch size.
- `poulpy-core/src/reference/keyswitching/glwe.rs` `gglwe_product_accumulation_output_size` computes the output DFT limb width for term count and source precision; `poulpy-core/src/layouts/mod.rs` `gadget_product_output_size` limits output size to key size.
- `poulpy-core/src/layouts/compressed/glwe_switching_key.rs`, `compressed/gglwe.rs`, `prepared/glwe_switching_key.rs` checked in M07 implement seeded body+individual-mask seeds, public decompression, independent prepare; no secret key needed online.
- `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` IFMA `VmpPMat` and `VecZnxDft` byte formulas use 16 B per prepared coefficient/limb. **These are formula-driven buffers, not sampled process RSS.**
- **No Rust toolchain** locally (`cargo` / `rustc` absent). No compiled variant or real FHE experiment executed.

## Minimal executed ring schedule test

Local exact toy script: `/mnt/data/ship_m09_key_major_batching_audit.py`, SHA256 `d75dea4b0da3ad5ac577bdeb92d8c811dc616e60af7b8b441b227f0bc01d363c`; results JSON `/mnt/data/ship_m09_key_major_batching_results.json`, SHA256 `8aa84e2ab2093cdf931ae3603a2b5d02f30ec0af1e453322175f10ce2abbe8d0`. Python run PASS on source-shaped small legal `ShipPlan` geometry N64,h4,window16,theta4,muxbase4,m=N/2=32, groups `[4,3]`, K=28. Ring `Z_{12289}[X]/(X^64+1)`, Q=8 independent inputs, four leaf slots each. For each candidate uses an independent **arbitrary 2×2 polynomial key operator (NOT encrypted key!)**, with Galois `X↦X^{g_d}` derived as source `g=5^((m-rot)%m) (mod 2N)`, nonidentity transforms present.

**Toy computation:** for each ciphertext leaf, apply successive groups; in each group, accumulate candidate key's transformed rank2 GLWE-column polynomial vector modulo 12289, and only then advance to the next group. Compare original loops (ciphertext→slot→group→candidate) vs proposed loops (slot→group→candidate→ciphertext), keeping **per-ciphertext group/candidate addition order identical**.
- `8 ciphertexts×4 leaves=32/32` final leaf pairs matched **coefficient-exact**, max difference=0.
- `QK=224` original prepared-key events → `K=28` key-major prepared-key events, one batch; **all 224 key products unchanged**.
- This test demonstrates only **finite-ring scheduling invariance**. Arbitrary key matrices do not model encrypted GGLWE gadget decomposition, NTT numerical rounding, metadata, scale, noise, CKKS correctness, security, or a speed benchmark.
- Algebraic reason: for each j and group t, `ct'_{j,t} = Normalize(∑_d σ_{g_d}(Product(K_{slot,t,d},DFT(ct_{j,t}))))`. Every summand depends solely on that input j, a fixed key, and candidate d, not any other input. Evaluating K_d across j then K_{d+1} preserves each j's exact sequence and Normalize location. This is a loop interchange, not a new FHE identity.

## One source-shaped 480-key memory/operation budget

Parameters `N16384,h32,theta4,window256,muxbase4,base2k52,ld40,out_budget104,dsize1,IFMA16B DFT, i64 raw`: `mux_bases=[4,4,4,3]`, `K=480`, `raised_k=468`, `k_mask=428`, `dnum9`, key size10 limbs, **Q=8**.

- Per-key prepared mux GGLWE **90 MiB**, raw **45 MiB**, compressed body+seeds ~**22.50055 MiB**.
- Compressed 480 + single raw + one prepared work buffer = **10.6789684 GiB** (M07 same conditional budget), vs eager all-key prepared **42.1875 GiB**.
- All 480 preparation required **once per batch** instead of once per evaluated ciphertext: ordinary streaming **3840** key preparations per 8-input batch, key-major **480**; original 3840 GGLWE products unchanged.
- Source IFMA `vmp_prepare` stage does 360 polynomial-limb transforms per key: ordinary streaming batch total **1,382,400** vs key-major **172,800**; amortized per ciphertext **21,600** transforms, eightfold less.
- For one masking/mux leaf stage at `k_mask=428`, input `a_dft` width `ceil(428/52)=9` limbs, two columns: **4.5MiB/ct**. Source `gglwe_product_accumulation_output_size` for this parameter+four-term group is at most key size 10 limbs (and source guard formula evaluates to 10): `sum_dft` two columns **5.0MiB/ct**. Thus both simultaneously required DFT representations consume **9.5MiB/ct**; Q8 group **76MiB**, **66.5MiB extra** relative to one such group. Q input leaf ciphertext coefficient payload is **2.25MiB** each (2 columns×9 limbs×8 bytes×N), and must be alive or otherwise reloadable. Producer/consumer scheduling and memory reuse may reduce overlap; these are explicit representative buffer shapes, NOT total scratch.
- Naively retaining Q8×(h+1=33) coefficient leaves for the product tree uses up to **594MiB** raw coefficient payload alone, plus **76MiB** for the batch DFT input+sum accumulators at a stage; total key+these payloads **~11.3333 GiB** if these selected buffers coexist. Other keys, scratch, input encodings, product tree, allocator overhead, worker parallelism **excluded**. Lower-memory online tree accumulation/scheduling is not proven or required for this gate.
- This illustrates a potentially useful memory–throughput regime: key prepare amortized at modest Q without restoring large all-key prepared memory, BUT 8-input batching may increase first-input latency, buffering, and reduce scheduling flexibility.

**[Conditional throughput threshold]** Let measured `T_p`=decompress+prepare cost **per key**, `T_m`=GGLWE product cost per ciphertext+key, same cost independent of input, ignoring other work/resource contention. For Q ciphertexts:
```
T_eager_mux(Q)=Q*K*T_m
T_stream_mux(Q)=Q*K*(T_p+T_m)
T_batch_mux(Q)=K*T_p+Q*K*T_m
```
Mux-only slowdown vs eagerly preprepared is `T_p/(Q*T_m)`; target <=10% for **Q8** iff `T_p/T_m <= 0.8`. This is a symbolic measurable condition, **NOT** evidence it is met by Poulpy. Compared with one-at-a-time streaming, positive T_p yields prep work saving without removing product operations. Increasing Q raises memory/latency requirements; cross-keyset batching does not reuse same key identity.

## Scope / falsification / importance

**PASS:** For fixed independent ciphertexts with the same keyset and preserving group/key addition order, candidate-outer/ciphertext-inner scheduling is algebraically valid in exact ring toy and source dependency DAG. A single independent compressed key can be prepared once per Q-input batch and reused across Q products, no deterministic public zero-key reuse introduced. Stage-buffer byte formulas show O(Q) live scratch; source K=480 key preparation count reduces by factor Q8.
**UNCLEAR:** Real CKKS arithmetic precision and security, key refactoring, numerical bitwise parity with IFMA, wall clock, large Q memory, 128-bit secure parameterization, overhead for simultaneous inputs, and novelty. No Poulpy compiled run. As prepared-key sharing across batch is a standard scheduling/hoisting pattern, **engineering-only novelty likely insufficient for crypto-paper contribution absent a new nontrivial technique or measured tradeoff**. Do not claim a new lower bound, security proof or publication.
**HUMAN_REVIEW:** If PI prioritizes throughput under constrained RAM, actual implementation and measurements are next; if PI prioritizes a theory FHE publication, consider parking straightforward batching and returning to mux rank/dsize or genuine key-count reductions.

## End of iteration

**STATUS:** PASS narrow schedule equivalence / source-derived 8× reduction in *preparation count* for Q8; UNCLEAR real CKKS throughput/latency/memory/security/novelty (IMPLEMENTATION_BLOCKED).
**RESULT:** Exact nontrivial Galois rank2 polynomial mux toy: 32 leaf outputs identical for Q8, prep events 224→28, products unchanged. At source K480, 3840→480 preparations, 1,382,400→172,800 polynomial-limb NTTs per Q8 batch, +66.5MiB selected per-group DFT accum buffer vs one CT; eager mux key 42.1875GiB vs compressed+single key buffers ~10.679GiB before Q stages. Conditional slowdown <=10% if T_p/T_m<=0.8 in mux-only model, unmeasured.
**NEXT_ACTION (ONLY PI CONTINUATION SHIP-M10):** **ONE** source-level **rank/key-count reduction structural hypothesis**, or, if PI explicitly prefers batching work, pursue **one actual compiled Poulpy integration** of key-major streaming and measure 8-input max decrypted slot error, warm-stage mux prep/product timings and peak RSS. Do not run another synthetic cache/batching speed proxy in place of compiled measurements. Keep key material independent and do not disclose secret digits.
**STATE_UPDATE:** YES this standalone M09 file. DO NOT overwrite shared `STATE.md` nor concurrent `findings/ship-memory-STATE.md`. M09 contains full recovery/checkpoint and M10 pending human decision.
