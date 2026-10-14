# SHIP I203 — Full prepared-key payload gate: selectors are NOT dominant in pinned Poulpy IFMA plan

Date: 2026-10-14 (Asia/Tokyo). **Independent SHIP** continuation I203; not the frozen general I-series nor the concurrently active vFHE V-series. Read-before-write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` (vFHE V8, separate), `findings/ship-memory-STATE.md` (I202 completed, SHA 734e89ae809492d54c0b7e340735de3a98e474b1), and related SHIP M02/I172/I198/I202 findings. **Do not change the global vFHE STATE.md or prior archives.**

## Exact source provenance

**Original target:** Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784. **Implementation audited here:** independent **Poulpy, not authors' HEaaN**, GitHub commit `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`. All numbers below are **layout allocation payload arithmetic** with one specified IFMA backend, not a benchmark, working memory RSS, or paper-author HEaaN measurement.

Poulpy sources read:
1. `poulpy-ckks/src/test_suite/ship.rs` `ship_suite_plan`: `h=32;window=(N/h)/2; mux_base=4;theta=4;log_budget_out=2*base2k`, `log_delta_work=min(test scale,40)`. For chosen scale=40 and N16384, this gives window=256 and budget_out=104.
2. `poulpy-ckks/src/layouts/ship/plan.rs`: `raised_k=round_up(((ceil(log2(h+1))+2)*ld+budget_out),base2k)`; `mux_candidates=ceil((2*window+1)/theta)`; `mux_bases` via mixed radix (4,4,4,3).
3. `poulpy-ckks/src/layouts/ship/keyset.rs`: `generate` produces h supports, 4theta real selector ciphertexts per support, and a mux key for **every** candidate `d=0..b−1` per mixed-radix digit; `hmux_rot_key_encrypt_sk` uses `GLWESwitchingKeyLayout` with `dnum=ceil(raised_k/(base2k*dsize))`, `k_aux=base2k*dsize`, input rank2, output rank1. `ShipKeySet::prepare` eagerly prepares every selector and EVERY mux, tensor, Galois and dense-to-sparse key, retains all in `ShipKeysPrepared`. Dense-to-sparse is dnum1, k_aux base2k, rank1→1.
4. `poulpy-ckks/src/test_suite/mod.rs`: `big.tsk_layout` and `big.atk_layout` use dnum=ceil(raised_k/(dsize*base2k)), auxiliary guard `k_aux=dsize*base2k+log2(N)`, rank1 at this plan.
5. `poulpy-core/src/layouts/prepared/gglwe.rs`: `GGLWEPreparedFactory::gglwe_prepared_alloc_from_infos` builds a `VmpPMat(N,dnum,rank_in,rank_out+1,key_size,Reuse)`, shared by prepared switching/tensor/automorphism wrapper; tensor input pairs for rank1 equal1 per `poulpy-core/src/layouts/glwe_tensor_key.rs`.
6. `poulpy-core/src/layouts/mod.rs` around lines 1389–1397: `key_size=ceil((dnum*dsize*base2k+k_aux)/base2k)` stored limbs.
7. `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` around lines 193–208: **both** `VmpPMat` and `CnvPVecL` store each NTT/DFT element in 2×u64 (16 bytes), with `VmpPMat bytes=N*rows*cols_in*cols_out*size*16`, `CnvPVecL bytes=N*cols*size*16`.
8. `poulpy-ckks/src/layouts/ship/keyset.rs` original direct selector `CnvPVecL(N,2,raised_k/base2k)` objects. Candidate halving their count is **hypothetical**; unimplemented in upstream.

## ONE primary hypothesis and ONE cheapest decisive test

**H203 [HYPOTHESIS, explicitly thresholded]:** At the pinned source-shaped real-SHIP `N=16384,h=32,theta=4,base2k=52,ld=40,budget_out=104,mux_base=4,mux_dsize=1`, the stored prepared selector payload is large enough that replacing **4hθ→2hθ** selector operands would save **at least 10% of the complete resident prepared key payload** (selector + HMux switching keys + tensor + conjugation + dense-to-sparse), provided packed operands keep the same degree/limb width. FAIL if actual conditional share saved <10% under exact pinned source layout.

**ONE TEST:** instantiate exact `keyset.rs` count/dimension, `GGLWEPreparedFactory` allocations, IFMA backend byte layout for each key category. Sum payload; compare original and candidate. No parameter sweep, no actual ciphertext execution or synthetic timing.

## Derived exact size audit [PASS arithmetic/source layouts, FAIL H203]

Parameter derivation:
`N=16384, h=32, theta=4, window=256, base2k=52, ld=40, budget_out=104,dsize=1.`
`tree_depth=6, raised_k=468, mask_L=9, mux_candidates=ceil(513/4)=129, mux_bases=[4,4,4,3]`.
At every support, mux key groups have `4+4+4+3=15` members, so **480** prepared HMux keys total.
Mux key layout: `dnum=9, rank_in=2, rank_out=1, k_aux=52, size=10` limbs.
Per HMux key: `N*9*2*2*10*16 = 94,371,840 bytes = 90 MiB`.
All HMux: `480*90MiB = 45,298,483,200 bytes = 42.1875 GiB`.

Original selectors: `4*h*theta=512`, per `CnvPVecL(N,2,9)` size `N*2*9*16=4,718,592 bytes = 4.5 MiB`, all `2,415,919,104 bytes = 2.25 GiB`.
Proposed packed selectors (unimplemented): 256 same-shaped prepared operands = 1.125 GiB, saving **1.125 GiB**.
Rank1 tensor key: `N*9*1*2*11*16=51,904,512 bytes = 49.5 MiB` (key aux66, key size11).
Rank1 Galois key: also 49.5 MiB.
Dense-to-sparse key: `N*1*1*2*2*16=1,048,576 bytes = 1 MiB` (dnum1/aux52,size2).

Sum of eagerly prepared **key payloads inside `ShipKeysPrepared`**:
- BASELINE = `47,819,259,904 bytes = 44.53515625 GiB`.
- CANDIDATE CONDITIONALLY = `46,611,300,352 bytes = 43.41015625 GiB`.
- SAVING = `1,207,959,552 bytes = 1.125 GiB = 2.5260942023% of baseline complete prepared-key payload`.
- HMux fraction baseline `42.1875/44.53515625=94.729...%`; selector fraction baseline `2.25/44.53515625=5.052...%`.
**H203 FAIL at 10% threshold.** Total memory saving is roughly 2.5%, although the selector component alone saves exactly 50%.

**Scope limitations:** This is a specific source-compatible illustrative parameter selection (test plan N16384 plus LD40/base52), **NOT** a measured running example, not a claim for all windows/digit bases, HEaaN, other CPU/GPU backend memory, or all FHE applications. Sum is payload **only**: excludes unprepared keys potentially retained at the same time, scratch, container overhead, process RSS, host/device copies, serialized files, and runtime. Larger process-memory denominator can reduce relative savings; memory lifetimes/peak may alter absolute effect. No runtime is connected; packed circuit must still pay two accumulations and h extra Galois switches (I198/I202).

## Reproducible local calculation

- `/mnt/data/ship_i203_total_prepared_key_payload.py` SHA256 `cabd505e7ad59699fdbd32fdd35065ed577b057c8ac1b472b0afe8429cf8f63e`.
- `/mnt/data/ship_i203_total_prepared_key_payload.json` SHA256 `b515a9c161a8b2348d4b6959f3e742d3bb807a6a1ba2e21537ab88e2da99cb66`.
Executed successfully with integer assertions, including exact baseline bytes and mux one-key 90 MiB. Neither file is itself in the connected notes repository; textual formulas are above.

## End-of-iteration / PI decision

**STATUS:** **FAIL H203** thresholded total-key-saving claim; **PASS** pinned IFMA complete-prepared-key allocation arithmetic. **UNCLEAR** actual packed CKKS precision, runtime and RSS, and any publishable novelty.
**RESULT:** In this case the real memory bottleneck is **HMux GGLWE (~42.188/44.535 GiB, ~94.7%)**. A 50% selector payload reduction would save only **~2.526%** of prepared key payload while adding online conjugations and IDFT. This materially weakens the case for high-investment work on this specific selector-only packing candidate as a full-key-size result; it does NOT invalidate algebraic correctness or all parameter regimes.
**NEXT_ACTION:** **HUMAN_REVIEW:** Recommend PARK the *selector-only* SHIP optimization as a priority until decisive real benchmarking or a special selector-dominated regime is identified. PI may approve redirecting **within SHIP key memory** to a **new hypothesis about HMux GGLWE material**, after first reading `findings/OPEN_RESEARCH_BRANCHES.md` and prior mux-key literature. Do not automatically declare that mux keys can be safely compressed; some source mux β values/keys are secret-derived and naïve reuse may expose secret state. If PI instead insists on selector experiment, provide/authorize a real Poulpy runner and test one leaf; no further adjacent toy tests.
**STATE_UPDATE:** YES for independent `findings/ship-memory-STATE.md` checkpoint, no modification to global vFHE `STATE.md`. No upstream code changes.
