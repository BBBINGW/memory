# SHIP-M05 — Source-allocated mux keys dominate packed-selector memory savings

**Date:** 2026-10-14 (Asia/Tokyo). **Series:** SHIP-M05 ONLY; independent of all vFHE I-series work.
**PI:** explicit continuation “好的，请继续” after M04.
**Primary target:** SHIP evaluation-key **resident prepared memory**. Original SHIP Cheon–Hanrot–Kim–Stehlé, EUROCRYPT 2025 / ePrint 2025/784 (source §3.3, §4.4/5, mirrored PDF 33pp SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official version-unverified).
**STATUS:** **FAIL** proposed >=10% whole-prepared-key memory-savings target at one explicitly stated source-shaped parameter regime for complex-paired selectors alone. **PASS** exact source-derived **prepared selector + mux buffer allocation** computation under chosen backend; **UNCLEAR** actual RSS, real runtime, full CKKS error and novelty.

## Read before write, environment, and isolation

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-STATE.md` blob `f4c70d60e7cd43ce7caa515a3d1bdb1d48a27adf`, `findings/ship-memory-M04-source-gadget-noise-bound.md` blob `2ece75ca17b97e5df49a9968c82b8c41d5595656`; checked shared `STATE.md` blob `fe796ef9aa9a193415db8575dfb04cf885491856` which belongs to concurrently advancing **vFHE I196**, DO NOT WRITE IT. M01–M04 remain separate.

Local executable check: `cargo`, `rustc` absent; `git` available, source cloning cannot be assumed. Therefore **no real Poulpy benchmark was run**, no actual heap allocation or timing was measured. Follow M04's explicit fallback to one source-pinned memory/cost gate.

## ONE primary falsifiable hypothesis

[HYPOTHESIS] Applying M01 complex-paired selector packing (4hθ→2hθ) to the *existing, otherwise unchanged SHIP keyset* reduces the total resident **prepared evaluation-key bytes** by at least **10%** in the illustrative Poulpy-shaped real-bootstrap plan from M02–M04:
`N=16384,h=32,θ=4,base2k=52,log_delta_work=40,log_budget_out=104,mux_base=4,mux_dsize=1,window=(N/h)/2`.

[FALSIFIER — ONE test] Use *actual pinned allocation formulas* to count all resident prepared selector **CnvPVecL** and all prepared hoisted mux **GLWESwitchingKeyPrepared / VmpPMat** bytes, including encrypted β=0 keys. These are a nonnegative **subset** of all evaluation keys. If `selector_bytes_saved/(selector_bytes_original + mux_bytes) < 10%`, then the hypothesis **fails even before counting all other keys or online costs**.

NB: The plan is **illustrative source-shaped only**, not confirmed executable on every named backend at N16384, base2k52, and NOT a 128-bit-security parameter choice. The correctness of the *source allocation formula conditional on chosen parameters* is what is tested, not backend preflight/benchmark.

## Pinned primary source exact allocation provenance

Independent implementation `poulpy-fhe/poulpy` fixed commit **250d4392656cd313f92ca66d96d8865702d39ddf**, **not original authors' HEaaN**.

1. `poulpy-ckks/src/layouts/ship/plan.rs` — source `tree_depth=(h+1).next_power_of_two().ilog2()`, `raised_k = roundUp(((tree_depth+2)*ld + outbudget),base2k)`, `mux_candidates=ceil((2*window+1)/theta)`, `mux_bases` uses mixed radix capped by `mux_base`.
2. `poulpy-ckks/src/test_suite/ship.rs` — source sample plan `h=32,` `window=(N/32)/2,` `mux_base=4,` `theta=4,` `log_budget_out=2*base2k`; the present N16384/ld40/base52 variant is an *extrapolation of those plan rules*, not an executed test.
3. `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`:
   - per support per real half `masks: Vec<CKKSCiphertext>` with **4θ** masks;
   - `ShipKeySet::prepare` eagerly stores every mask as `cnv_pvec_left_alloc(module.n(),2,mask_size,PrepareHint::Reuse)`, `mask_size=ceil(raised_k/base2k)`;
   - for EACH support and for EACH digit group base `b`, `generate` creates **b independent HMuxRotKey** objects, **including β=0** values; `prepare` eagerly prepares ALL of them, no skipping zero-switch selection;
   - `hmux_rot_key_encrypt_sk` sets `dnum=ceil(raised_k/(base2k*mux_dsize))`, `k_aux=base2k*mux_dsize`, **rank_in=2, rank_out=1**.
   - Only one `gal_el=-1` conjugation key is prepared and can be reused; key quantity unchanged under the candidate. Other prepared keys tensor and dense-to-sparse also remain.
4. `poulpy-core/src/layouts/prepared/gglwe.rs` — `GGLWEPreparedFactory::gglwe_prepared_alloc_from_infos` calls `vmp_pmat_alloc(n,dnum,rank_in,rank_out+1,key_size,Reuse)`, `key_size=ceil((dnum*dsize*base2k+k_aux)/base2k)`. Source base key size formula in `poulpy-core/src/layouts/mod.rs`.
5. `poulpy-hal/src/layouts/module.rs` blob `9c4b3bd787b93a47b92945df86f1662491812894` — `bytes_of_cnv_pvec_left = N*cols*size*sizeof(DftWord)` and `bytes_of_vmp_pmat = N*rows*cols_in*cols_out*size*sizeof(DftWord)`, unless backend overrides.
6. `poulpy-cpu-avx/src/ntt4x30/mod.rs` — AVX2 NTT4x30 `DftWord=4*u32` (16 bytes), backend default bytes rule. `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` blob `3e2bc4c38b80533f0c758a0c869a395c1938736f` explicitly overrides `bytes_of_cnv_pvec_left`, `bytes_of_vmp_pmat` to **2*u64** (16 bytes). `poulpy-cpu-portable/src/ntt4x30/mod.rs` — portable `DftWord=4*u64` (32 bytes).
7. `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d` — baseline 4θ masking products per support and **one** DFT accumulator+IDFT+normalize; packed M01 formula still uses 4θ ct×pt product terms, **two** masking accumulators and two IDFT/normalization paths.
8. `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542` — masking→mux→tree; baseline real bootstrap has one final root conjugation. Packed rewrite adds approximately one **early** conjugation per support, leaving the existing root conjugation.

## Executed source-allocation arithmetic: SINGLE falsifier

Plan `N=16384,h=32,θ=4,window=256` gives `mux_candidates=ceil(513/4)=129`; `mux_bases=[4,4,4,3]`, 15 keys per support, **480 mux prepared keys**. Product tree depth=6, `raised_k=ceil((8*40+104)/52)*52=468` bits.

- selector `mask_size=ceil(468/52)=9` limbs; original **512** prepared selector operands; paired candidate **256**.
- mux `dnum=ceil(468/52)=9`, `k_aux=52`, `key_size=ceil((9*52+52)/52)=10` limbs, `rank_in=2`, `rank_out+1=2`.
- For any backend with 16-byte prepared DFT words:
  - **per prepared selector**: `16384 * 2 * 9 * 16 = 4,718,592 bytes = 4.5 MiB`.
  - **per prepared mux key**: `16384 * 9 * 2 * 2 * 10 * 16 = 94,371,840 bytes = 90 MiB`.
  - Original selector buffers: `512*4.5 MiB=2.25 GiB`.
  - Paired selector buffers: `256*4.5 MiB=1.125 GiB`.
  - **Mux buffers unchanged:** `480*90 MiB=42.1875 GiB`.
  - **At least selector+mux baseline=44.4375 GiB**, candidate=43.3125 GiB; saved 1.125 GiB.
  - Therefore `saved/(baseline_selector+mux)=1.125/44.4375=2.531645569620253%`. Since tensor/automorphism/dense-to-sparse keys are nonnegative unchanged resident prepared buffers, this is a rigorous **UPPER BOUND ON THE PERCENTAGE reduction in the FULL RESIDENT PREPARED KEY MATERIAL**, assuming packed selector key representation has equal modulus/rank/limb width, all mux keys remain as source, and both variants residently prepare all keys.
- Portable 32-byte NTT word gives baseline selector=4.5GiB, packed=2.25GiB, mux=84.375GiB, same upper-bound percentage 2.53%. This is one source-allocation formula instantiated under supported word representations, NOT 2 separate experiments.

**Optional lower-bound incremental live accumulator:** real baseline ~one masked leaf accumulator. Packed rewriter needs U and V before conjugating; at k_mask≈428, one extra live rank1 ciphertext at least `N*2*ceil(428/52)*8≈2.25MiB` of coefficient payload, excluding DFT scratch, plaintext right preps, keys and allocator metadata. It is small versus 1.125GiB gross key saved, but actual peak scratch is not bounded above here. Since M01 doubles masking finalization **32→64** and adds **32 high-k conjugations**, the runtime memory–latency Pareto frontier cannot be decided from these byte counts alone.

**Operations:** real SHIP baseline 512 masking ct×pt terms, 32 masked-sum finalizations, baseline 1 root conjugation, unchanged 480 mux gadget group terms. Packed variant 512 masking ct×pt terms, 64 masking finalizations, 32 additional early conjugations + existing 1 root conjugation, unchanged 480 mux gadget group terms. These are stage invocation counts, **NOT measured latency or cryptographic work units**; unequal precision means don't treat one KS at k428 as one KS at root k188 in cost.

**LOCAL reproducer (not automatically in GitHub):**
- `/mnt/data/ship_m05_poulpy_prepared_memory_audit.py`, SHA256 `a4b991982c8c8e81caea2fca84fd3ebdbd855c7b443a6d4aeb286c5b0c379e20`.
- `/mnt/data/ship_m05_poulpy_prepared_memory_audit.json`, SHA256 `40ce4ab45a18dd92b7b4b36f6c1929034ae8abf42981573307b3f879a3ab9a52`.
Python executed and all assertions pass.

## Interpretation / negative result

**[FAIL]** The ≥10%-of-entire-prepared-key memory reduction hypothesis is decisively false for this source-shaped plan **even if the packed method is algebraically perfect and its online conjugations cost zero**. It gives at most **~2.53%** of the whole keyset prepared buffers in the unchanged mux-key design, NOT ~50%. This is much more decisive for a **total evaluation-key-memory** contribution than M03's unrelated low-precision toy noise.

**[LIMITS]** The absolute 42GiB mux figure extrapolates an illustrative plan and uses actual **allocation formulas**, not a measured heap/resident-set or verified secure production preset. Multiprocess replication, concurrent raw+prepared storage, GPU placement, pruned mux group layout, optimized author HEaaN and alternative mux-dsize/plan could change absolute sizes. This result does not exclude high benefit in a very different regime with no mux keys or with separately compressed mux keys. It does not prove packing is cryptographically sound, efficient or novel.

**[RECOMMENDATION]** For the PI's stated **total SHIP evaluation-key memory** target, **PARK complex-paired selectors as a primary strategy** in this original source-shaped mux layout unless other larger key families are reduced first, or a sharply differentiated parameter regime makes selectors dominant. M01–M04 remain valid narrow findings. Most promising *problem target* from this gate is **privacy-preserving mux switching-key compression/restructuring**, not merely selector encoding; this is a recommendation, NOT an automatic new research hypothesis or pivot.

## End of M05

**STATUS:** **FAIL** ≥10% full prepared-key memory gain hypothesis (specific source-shaped layout); **PASS** source allocation arithmetic; **UNCLEAR** other regimes and runtime/precision/novelty.
**RESULT:** At n16384,h32,θ4,b52,ld40, 480 prepared 90MiB mux GGLWE keys dominate 512 prepared 4.5MiB selector operands. Packing saves 1.125GiB but cannot save more than 2.53165% of the unchanged total prepared key memory. Also costs +32 early Galois KS and doubles masking finalizations in real bootstrap.
**NEXT_ACTION:** **HUMAN_REVIEW** before SHIP-M06. PI to choose whether to (A) park M01 complex selector packing and audit the mux-key bottleneck within SHIP, or (B) deliberately pursue a niche selector-dominated regime or benchmark the packed selector rewrite. If PI authorizes A, M06 should pick **ONE** narrowly falsifiable mux-key structural-compression hypothesis with a cheapest exact-source test; do NOT inherit a new parent silently.
**STATE_UPDATE:** YES to independent `findings/ship-memory-STATE.md` only; **NO** shared `STATE.md` changes. Research files separate from vFHE I193–I196.
