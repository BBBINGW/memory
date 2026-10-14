# SHIP-M07 — Independently seeded GGLWE mux keys and one-at-a-time preparation

**Date:** 2026-10-14 (Asia/Tokyo). **Research series:** SHIP-M07, independently numbered. PI authorized continuation after M06 by saying "好的，请继续". **Do not merge into global vFHE V-series or concurrent SHIP I-series.**
**Target:** SHIP prepared evaluation-key *resident memory* while preserving mux-digit privacy.
**STATUS:** **PASS** narrow pinned-source *structural/representation* feasibility for **seeded bodies + per-key on-demand decompression/preparation** and conditional >=50% resident mux-buffer saving in one illustrative backend/plan; **FAIL** seed-only reconstruction (missing secret-dependent body). Actual Rust FHE compile, precision, security proof, RSS, wall time and contribution novelty **UNCLEAR / IMPLEMENTATION BLOCKED**.

## Read before write / independent state safety

Before writing read in order `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-M06-public-zero-template-galois-linkability.md` blob `052f458cc9f53b796b9f52753837b06ac6b4d86b`, `findings/ship-memory-M05-mux-dominates-prepared-key-memory.md` blob `83afac0b0a9de2c41baa6760710ae50d9cfd5785`, `findings/ship-memory-STATE.md` blob `f77e5b1a48e6d8c7d2cfbefe53a29615599071d8` **already advanced independently to I201**, and shared global `STATE.md` blob `04e4fc1894c1c3868ba73f7410d45663365e6c4d` **vFHE V7**, for collision detection only. The attempted M-series separate recovery pointer `findings/ship-memory-M-series-STATE.md` does not exist, and M06 had a concurrent write conflict when creating it. **Do not overwrite either live state.** THIS M07 file is self-sufficient: SHIP-M07 COMPLETED, SHIP-M08 NOT STARTED, NEXT_ACTION below; previous M files remain untouched.
No Rust toolchain available locally (`cargo` and `rustc` absent), GitHub archive was accessed through user-connected tools, **no compiled Poulpy code run**, third-party code unmodified.

## Source, provenance, and previous obstruction

**SHIP paper:** Cheon, Hanrot, Kim and Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, physical pp22–24/§4.4 and §5.1 Algorithm 5; prior Research MCP cache 33 pages mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, `VERSION_UNVERIFIED`; some PDF extracted formulas garbled. The ePrint paper uses gadget-decomposed HMuxRot and B-to-1 mux keys; exact implementation facts are sourced to independent Poulpy pinned repository, not authors' HEaaN.
**Independent implementation source:** `poulpy-fhe/poulpy` commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**.

Previous M05 source-shaped example `N16384,h32,theta4,window256,mux_base4,base2k52,ld40,output_budget104,mux_dsize1`: 480 prepared rank2→rank1 mux keys contain 42.1875 GiB backing buffers on IFMA (NTT3x42) 16-byte-per-prepared-word layout, exceeding selectors 2.25 GiB. These are allocation formulas under illustrative source-shaped plan, **not actual production key RAM or measured performance**. M06 FAILed publicly related zero-key-template sharing because inverted public automorphisms expose deterministic cross-key equality and secret rotation digit. M07 preserves per-key independent randomness and stores encrypted bodies; it does NOT reuse the same zero ciphertext across beta0 candidates.

## ONE primary hypothesis and ONE cheapest decisive test

**[HYPOTHESIS M07]** In the pinned Poulpy HMuxRot mux path, independent key material can be stored as **seeded GLWE switching keys (body+individual mask seeds)**, then each key decompressed and NTT-prepared **one at a time** immediately before the existing hoisted DFT product and public output automorphism, requiring no evaluation secret and no simultaneous storage of all prepared mux matrices; at a representative source-shaped IFMA parameter choice, the resident mux backing-buffer budget will be less than half the original eager 480-prepared-key buffer budget.

**[FALSIFIER / MINIMAL TEST]** Inspect pinned `GLWESwitchingKeyCompressed` and `GGLWECompressed` data model, compressed key-generation, `decompress_glwe_switching_key`, `glwe_switching_key_prepare`, and actual `ship_mux_rotate` DFT loop. If any *required* encryption body or PRG mask needs the private secret at evaluator, if all prepared keys must physically coexist to compute the DFT sum, or if exact allocated compressed + one raw + one prepared buffer is >=half full-prepared mux memory, FAIL the narrow hypothesis. Perform ONE arithmetic instance, no parameter sweep/benchmarks.

## Fixed-code facts [FACT]

1. `poulpy-core/src/layouts/compressed/gglwe.rs` blob `8bf91603acce63a4cf5f1e7233bf3bf2f89c7334`: `GGLWECompressed` stores **one output body column** per gadget-row/input-column and a `Vec<[u8;32]>` PRNG seed for every row/input-column, not seed-only. `GGLWEDecompress::decompress_gglwe` iterates all row/columns and invokes `GLWEDecompress`.
2. `poulpy-core/src/layouts/compressed/glwe_switching_key.rs` blob `843dd332d13dd2c7e6f912acaae2ea71bfe7f99c`: `GLWESwitchingKeyCompressed`, `GLWESwitchingKeyDecompress` are already implemented and copy input/output degree metadata.
3. `poulpy-core/src/reference/encryption/compressed/gglwe.rs` blob `c4bf11cc70fa40cedab82e39929d640af9f18107`: compressed key generation takes `sk_in`, `sk_out` **at keygen**, derives per-row mask seeds using `Source::branch()`, fills each GLWE mask deterministically, encrypts the gadget plaintext under private `sk_out` and stores the **resulting body**. Evaluator with compressed key never needs the private key to expand masks.
4. `poulpy-core/src/reference/encryption/compressed/glwe_switching_key.rs`: `glwe_switching_key_compressed_encrypt_sk_reference` publicly exposed source trait uses private keys only at generator, seed parameter `seed_xa` and `source_xe`; can independently sample distinct source mask seeds per candidate. This does NOT prove joint security or prevent seed collisions under bad keygen, but avoids M06 deterministic common-template reuse.
5. `poulpy-core/src/layouts/compressed/glwe.rs`: `GLWEDecompress` reads stored body, regenerates pseudorandom mask from each stored seed and is a public operation under original encryption sampling.
6. `poulpy-core/src/layouts/prepared/glwe_switching_key.rs` blob `af00859831a910692b2d77d664af8f89f278240a`: standard uncompressed `GLWESwitchingKey` converts via `glwe_switching_key_prepare` -> `gglwe_prepare`; `poulpy-core/src/layouts/prepared/gglwe.rs` -> `vmp_prepare`.
7. `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: EXISTING SHIP implementation generates full uncompressed HMuxRot keys and **eagerly prepares every key**. It does NOT offer a ready-to-use streaming SHIP mode; must add compressed HMux keyset variant or external loader and update key prepare/runtime APIs.
8. `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: `ship_mux_rotate(keys:&[HMuxRotKeyPrepared],plans,...)` DFTs rank2 input once, then loops `for key in keys`: per-key GGLWE product -> public automorphism -> add into `sum_dft`, finally **one** IDFT and normalization for group. No algebraic need to retain earlier prepared key after its product is accumulated. BUT existing function signature, precomputed plan setup (`ship_mux_plans` assumes prepared keys), and keyset struct require a source refactor. The only persistent state across keys should be DFT'd input, sum accumulators, plan map, and scratch.
9. `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` blob `3e2bc4c38b80533f0c758a0c869a395c1938736f` sets `bytes_of_vmp_pmat = n*rows*cols_in*cols_out*size*16` and similar DFT layouts. `poulpy-cpu-avx512/src/ntt3x42_ifma/vmp.rs` blob `78f8a8494a46964440a12fa2b4adb2fa248ade45` implements `vmp_prepare_ifma` with `nrows=rows*cols_in`, `ncols=cols_out*size` and forward NTT for each pair — a **repeated online preprocessing cost** under streaming, not an existing prepped cache. 
10. `poulpy-hal/src/api/vmp_pmat.rs` blob `e8bf2d438a399213a5bb199c7c8c506e4c66ee22` describes the format and preparation abstract semantics; no special parallel caching assured.

**[LOGICAL LIMIT]** **Seed-only** regeneration would have evaluator reconstruct `a` but not `b=m-as_{out}+e`; the latter depends on secret values and encrypted selector digit. A public encryption key could change the workflow and sampling assumptions, but is not present in this claimed seed-only scheme. Hence full key must store at least encrypted body or equivalent secret-dependent material. This is a scope correction, not a universal ciphertext compression lower bound.

## Single instantiated source-allocation calculation

Inputs `N=16384,h=32,θ=4,window=256,mux_base=4,base2k=52,ld40,out_budget104,mux_dsize1,rank_in2,rank_out1,ZnxWord i64,DftWord packed IFMA 2*u64`.
```
tree_depth=6, raised_k=468, k_aux=52,
mux_bases=[4,4,4,3], total mux keys K=32*(4+4+4+3)=480.
dnum=9; stored limb size=ceil((9*52+52)/52)=10.

Per key:
  Prepared VmpPMat: N*9*2*2*10*16 = 90 MiB.
  Full coefficient-domain raw GGLWE: N*9*2*2*10*8 = 45 MiB.
  GGLWECompressed secret-dependent body column: N*9*2*1*10*8 = 22.5 MiB.
  Independent seeds: dnum*rank_in*32 = 576 bytes/key.
  Total compressed key material = 22.5 MiB + 576 B (+ small struct/header metadata).

All mux keys eager prepared in source: 480*90 MiB = 42.1875 GiB.
All independent compressed bodies+seeds in resident memory: 10.547132492 GiB.
Online one-key scratch coefficient+prepared: 45+90=135 MiB.
Total compressed key material + 1 inflight raw/prepared pair = 10.67896843 GiB,
a **74.68688965% reduction** relative to the 42.1875GiB prepared-only mux payload.

If 32 independent workers each need their own raw+prepared key, static mux
material+workspace = 14.76588249 GiB, **64.99938965% lower** than 42.1875GiB.
Other shared scratch, DFT accumulators, selectors, and key material are excluded.
```

**[REQUIRED ONLINE COST]** `vmp_prepare_ifma` iterates `(dnum * rank_in) * (rank_out+1)*size =9*2*2*10=360` N-length polynomial-limb transforms per mux key. Re-preparing all 480 mux keys from seed+body for **each** real bootstrap => **480 key decompressions/preparations and 172,800 N-length forward NTT transform invocations** before/while doing the original 480 GGLWE products. This is a count of source preparation-loop calls, NOT cycle/time. Also each bootstrap writes ~42.1875GiB to transient prepared-key buffers (if each full key is materialized), plus raw mask regeneration/reads. Unmodified source amortizes initial preparation across many bootstraps and doesn't pay it for every evaluation. This may **destroy SHIP's low-latency goal** and make streaming useful only in memory-constrained, infrequent-bootstrap or throughput/workload regimes; no measured timings.

A bounded LRU/cache with T prepared entries reuses some preparations if workload repeats and is a Pareto surface, not tested here. Running multiple independent threads uses >=T inflight raw/prepared buffers, hence memory savings depend on concurrency.

**[EXECUTED AUDIT]** Standalone local source-formula Python script `/mnt/data/ship_m07_seeded_mux_streaming_audit.py`, SHA256 `387a0bc37151883514a8b28cb6550644a55b1945cd6535cdfb4af52675905661`; JSON output `/mnt/data/ship_m07_seeded_mux_streaming_audit.json`, SHA256 `6fe284d73c5ad5f33f5d15497c32905bdfed0239dcc252a0496681e3b0a35d44`. All arithmetic shape assertions PASS. Not an executed FHE correctness or security experiment.

## Privacy and correctness gate — what is and is not proven

- **Source-construction reasoning:** Independently sampled seeds for each key and independent encryption error streams preserve the *intended original per-key ciphertext distribution*, rather than forcing a publicly recognizable equality pattern like M06. Decompression replays the PRG to recover original randomized masks exactly, copies corresponding body, and preparation is a representation change: in an ideal correct backend, the stream product matches the fully prepared compressed-key result. This is **conditional on PRG security and proper seed isolation, not a new formal joint key-security proof**. Original SHIP uses full independent keys but may rely on circular/key-dependent security in either representation; NOT audited.
- **Source-level interface obstruction:** SHIP `ShipKeySet::generate/prepare`, `ShipIndexKeysPrepared`, `ship_mux_plans`, and `ship_mux_rotate` currently assume eager prepared vectors. **Refactoring is necessary** to pass candidate metadata with compressed keys and schedule the decompress+prepare+product loop; `&[HMuxRotKeyPrepared]` cannot simply be changed to `&[GLWESwitchingKeyCompressed]` without modifying code. No end-to-end compiled integration exists.
- No proof of production plaintext correctness, precision/noise equivalence under actual optimized IFMA, real speed, peak RSS, full hardware feasibility, security of the compressed public evaluation-key family, or publishable novelty. Seeded GLWE/GGLWE is already implemented: naive streaming by itself may be a useful engineering memory mode rather than a cryptographic research contribution.

## End of M07 — one test, stop

**STATUS:** **PASS** static API/representation feasibility and conditional mux-prepared buffer budget (<half at source-shaped IFMA plan); **FAIL** seed-only regeneration; **UNCLEAR / IMPLEMENTATION BLOCKED** integrated CKKS correctness, timing, RAM, security and novelty.
**RESULT:** Existing key compression stores independent mask seeds **and secret-dependent ciphertext bodies**; evaluator can decompress without knowing s and prepare each key when used. M05's 42.1875GiB resident prepared mux buffers can be exchanged for ~10.679GiB conditional resident compressed+single-worker workspace (~74.69% reduction) BUT with 480 online key preparations, **172,800 extra NTT polynomial-limb preparations** per bootstrap. This is a potentially severe memory–latency trade-off, not a benchmark or automatic contribution.
**NEXT_ACTION (SHIP-M08 only if PI continues):** Test **ONE reuse-aware caching breakpoint** on a source-compatible SHIP *workload of repeated bootstraps*, comparing offline eager prepare once vs online seeded-streaming per-bootstrap preparations, and derive a break-even criterion in *measured* `T_prepare_per_mux_key`, `T_product_per_mux_key`, available RAM and #bootstrap operations. Prefer real Poulpy runner; without runnable Rust, derive symbolic threshold and report HUMAN_REVIEW rather than inventing timings. An alternate PI choice is to PARK this straightforward engineering approach and examine source-secure mux *rank or key layout* reductions for deeper crypto novelty; do not choose without PI.
**STATE_UPDATE:** YES standalone M07 finding, **NO global `STATE.md` or concurrent SHIP I201 `findings/ship-memory-STATE.md` edit**. Recover M-series next round from this M07 file.
