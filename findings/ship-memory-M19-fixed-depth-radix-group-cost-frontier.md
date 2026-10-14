# SHIP-M19 — Fixed-depth mixed-radix schedules weakly dominate greedy in *source-counted* costs, not stochastic precision

**Date:** 2026-10-14 (Asia/Tokyo). **Independent SHIP M-series:** **M19 COMPLETED**; no M20 started. **Research parent** SHIP prepared evaluation-key HMux memory. PI said "好的，请继续" after M18. **STATUS: PASS SOURCE-COUNTED COST FRONTIER**, **UNCLEAR** real CKKS precision/noise, compiled latency, memory RSS, security or publishable novelty. Engineering-level result; **not** a bug/attack on original authors' HEaaN.

## Read before write, provenance and isolation

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (separate vFHE SHA `7af97fb3ee38ae139fd12f867fd9eccb18d22d16`), parallel `findings/ship-memory-STATE.md` (already separate I219, SHA `02d3e03010f2b78c8a8f02d2b5d3dafe6843a8f2`), M18 `findings/ship-memory-M18-fixed-depth-mixed-radix-key-minimization.md` SHA `dd735832c4dbb1accc6edf1f4dd40e996c159419`. Target M19 did not exist. **Do not edit either shared state, earlier M findings, parallel I-series files, original paper, or upstream Poulpy**. M17's separate beta-GLWE fused engineering track remains **PARKED** with no Rust runner.

**Scientific paper**: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / IACR ePrint 2025/784, §5.1 base-B mux and §5.2, original authors' HEaaN. Previous cached original mirror 33pp PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. This M19 compares **pinned independent Poulpy** source, NOT authors' exact experimental setting.
**Independent code**: `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.

## ONE falsifiable primary hypothesis + ONE cheapest decisive source test

**[HYPOTHESIS M19]** For source-shaped `N16384, h32, w256,theta4,mux_base4,base2k52,dsize1,dnum9,k_aux52,prepared key.size10,ct precision468`, **all six** minimal-key four-group mixed-radix tuples with multiset `{3,3,4,4}`, as discovered M18, **weakly dominate** greedy tuple `[4,4,4,3]` in the source-counted metrics: total prepared-key payload, GGLWE/VMP product calls, nontrivial per-candidate DFT-domain Galois actions and reusable unique Galois plans, total group count, output guard limbs, output DFT buffer shape and stage peak scratch shape. **No conjecture of stochastic noise, bitwise ciphertext parity or real elapsed-time dominance is included.**

**[DECISIVE FALSIFIER]** Inspect pinned source `gglwe_product_accumulation_output_size`, `gadget_product_guard_limbs`, `ship_mux_rotate_tmp_bytes` and actual Galois per candidate; enumerate all six schedules, faithfully evaluate term_count b3/b4 with source formula and compare every named static resource. A single config with extra output limb or larger group stage scratch, additional group, more transform/candidate operations or no key saving falsifies universal source-counted dominance. Also recheck legal `u0..512` × all 32 slot public-index rotations as a consistency control.

## Original source contracts [FACT]

- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: source greedy `mux_bases=(4,4,4,3)` with 129 high-digit candidates. Source plan's greedy generation would need modification to deploy a chosen optimized tuple, and validation/key generation MUST use the same tuple; deleting random keys is invalid.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: one independent encrypted HMux GGLWE **per candidate d per group per support**, input rank2, output rank1, per candidate public rotation `r=(d*weight) mod m`, weight starts theta and multiplies by each radix. Generated key shape does not depend on d or rotation. Source full prepared rank2 GGLWE size is 90MiB/key for selected example.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: once per group prepare two-column input DFT, per candidate one `gglwe_product_dft_reference` (VMP for dsize1), only for d>0 public nonidentity Galois DFT automorphism before accumulation, two-column IDFT and `vec_znx_big_normalize` once at group close. `ship_mux_plans` constructs one plan per **distinct nonidentity Galois element**. Scratch helper:
```
a_size=ct.size()
output_size=gglwe_product_accumulation_output_size(ct,ct,key,term_count=b)
product_tmp=gglwe_product_dft_tmp_bytes_reference(output_size,a_size,key)
mux_tmp = 2*bytes_of_vec_znx_dft(N,2,output_size)+product_tmp
final_tmp = bytes_of_vec_znx_big(N,2,output_size)+normalize_tmp
total=bytes_of_vec_znx_dft(N,2,a_size)
      +bytes_of_vec_znx_dft(N,2,output_size)
      +max(mux_tmp,final_tmp).
```
The selected dsize1/VMP product scratch is a function of key geometry and output_size, NOT candidate count directly.
- `poulpy-core/src/reference/keyswitching/glwe.rs` blob `67fd537f256687a95bf1c7c719392a0d49fe5827`: `gglwe_product_accumulation_output_size` computes `product_terms=N*dnum*dsize*rank_in*term_count` then calls `gadget_product_output_size`, source `term_count` **does matter** to sizing; `dsize1` execution invokes one VMP per key, `term_count` input to VMP is not another candidate loop.
- `poulpy-core/src/layouts/mod.rs` blob `c1e953bed001d3129188f4c0c5d35073a82ee59d`: `key_work_size=min(key_size,ceil(k/(base2k*dsize))*dsize+ceil(kaux/base2k))`; live `ceil(max(input_k,output_k)/base2k)`; guard `gadget_product_guard_limbs(base2k,product_terms)` uses an **assumed probabilistic centered digit tail model**, but the returned integer is just a source buffer-size formula, NOT an independent proven output error probability; `output_size=min(work_size,live+guard)`. Here `key_size=10,work_size10,live9`.
- IFMA prepared DFT polylimb `N*16` bytes, group 2-column DFT `N*2*output_size*16`, from `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` blob `3e2bc4c38b80533f0c758a0c869a395c1938736f`.
- No Rust toolchain/clone/network per prior M17; no compiled error/latency/RSS test or new independent KDM/security claim this round.

## Executed one cost/frontier gate [DERIVATION]

For b3 versus b4, exact source `product_terms`:
```
 b=3 => 16384*9*1*2*3 =   884,736
 b=4 => 16384*9*1*2*4 = 1,179,648
```
Both return `gadget_product_limbs=3, gadget_product_guard_limbs=2, work=10, live=9, output_size=10`. Each group therefore has an identical **10-limb two-column output DFT buffer = 5MiB**, input DFT `ceil(468/52)=9` limbs => 4.5MiB. The source scratch expression takes the same values for either b under constant key geometry/size; group maxima and number of group-IDFT/normalize steps therefore unchanged. The full Rust allocator does NOT execute, so precise actual RSS is unverified.

For all six minimum tuples
```
 [3,3,4,4], [3,4,3,4], [3,4,4,3],
 [4,3,3,4], [4,3,4,3], [4,4,3,3]
```
we independently enumerated each `u∈{0,...,512}` and each support-slot index j0..31; all **16,416/16,416** mask-low-digit plus mux-weight rotation index identities hold. All d>0 candidate rotations are nonzero and **pairwise distinct across 4 groups** in the selected ring m8192, so each has exactly one nonidentity Galois key plan and one DFT automorphism per use. Identity candidate d0 is always present once per group.

| Source-counted metric | Original greedy | Any of six minimal tuples |
|---|---:|---:|
| Radix sum per support | 15 | 14 |
| Number of independent prepared mux keys | 480 | 448 |
| Per bootstrap GGLWE/VMP candidate calls | 480 | 448 |
| Per bootstrap nontrivial DFT Galois candidate actions | 352 | 320 |
| Distinct reusable Galois transform plans | 11 | 10 |
| Four sequential mux groups per each 32 support positions | 128 | 128 |
| Per-group output limbs | [10,10,10,10] | [10,10,10,10] |
| Per-group gadget guard limbs | [2,2,2,2] | [2,2,2,2] |
| Max group DFT buffer bytes | 5MiB | 5MiB |
| Max stage source scratch-shape signature | unchanged | unchanged |
| Prepared mux-key GiB (selected IFMA assumption) | 42.1875 | 39.375 |
| All **named** evaluation-key payload GiB | 44.53515625 | 41.72265625 |

Saved per bootstrap **32 VMP calls +32 nonidentity automorphism actions**, one distinct Galois plan (11→10), and **2.8125GiB prepared-key-only storage** = 6.6667% mux-key category and 6.3152355% total *named* payload. Same number of input DFTs per group and final IDFT+normalizations; **not** necessarily 6.67% wall time due S2C, masks, tensor, key bandwidth, pipeline overlap. All six tuples TIE in this tracked static metric, although per-group digit order and rotation/key distributions differ.

**CRITICAL NOISE/SECURITY LIMITS:** Each public rotation g encrypts β-dependent messages under a different g-automorphed output secret. Different radix order changes where source-encrypted zero candidate noises are injected in the four serial mux stages; shrinking total candidates does not establish a monotone distribution of final noise after nonlinear/composed rounding. The cited `gadget_product_guard_limbs=2` is a source-designed buffer allocation based on its assumed digit-tail probability, NOT a measurement or full ciphertext-noise theorem for the alternate schedule. Existing sparse-window secret security concerns from independent I216-I219 and M13 KDM/helper hypotheses not repaired by changing radix. The original authors' HEaaN parameters differ; don't call this a paper correction or baseline authors' improvement without genuine prior-art/implementation check.

## Reproducible executed script/results

- Python script (executed): `/mnt/data/ship_m19_group_cost_frontier.py`, verified SHA256 `d83b7eaf4b3643efbd889395f97a4e17994ca52a2f774fa9955ea86983d14797`.
- JSON report: `/mnt/data/ship_m19_group_cost_frontier_results.json`, verified SHA256 `3287f2b8de1935e818669d2419e8a92cc0b219f8c96dc580c3df6645beeae98c`.
- The program implements the **pinned Rust formulas exactly** for `gadget_product_limbs`, the f64 `gadget_product_guard_limbs` approximation/inequality, key_work/live windows and group cost shape; computes all six 4-layer schedules, tests all rotations and compares resource vectors against original. Its assertions PASS. It does not compile/run Rust, encrypt GLWE/GGLWE or measure wall time.

## End of iteration / research judgment

**STATUS:** **PASS** the narrowly defined **source-counted** weak dominance for all six fixed-depth minimal-key tuples; **UNCLEAR** real noisy CKKS correctness, statistical precision, joint security, actual end-to-end latency/RSS, novelty. **No security theorem/attack claimed.**
**RESULT:** M18's 480→448 key count is not cancelled by any additional group guard/window or scratch in source formulas; 32 fewer VMP and Galois actions; 128 mux stages and selected scratch envelope unchanged. All six tuples indistinguishable in tracked operation counts. No evidence of a bigger theory contribution; engineering size delta around 6.3% total named prepared key payload.
**NEXT_ACTION:** **PARK** further paperless/rustless microaudits of this same mixed-radix scheduling; research value unlikely sufficient for a theory paper alone. If PI wants this implementation path, source patch `ShipPlan::mux_bases` to return selected explicit tuple, regenerate keyset/validate, then compile original and candidate on a verified Rust/IFMA runner and compare decrypted CKKS slot error, keygen, time and RSS at security-matched parameters. If PI continues theory research, pivot to a new parent with a nontrivial proof/security correctness gap rather than automatic M20 radix sweeps.
**STATE_UPDATE:** YES standalone M19 record only; neither concurrently edited `findings/ship-memory-STATE.md` nor global vFHE `STATE.md` modified. This M19 file is the M-series recovery checkpoint.
