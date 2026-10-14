# SHIP-M18 — Fixed-depth mixed-radix minimization removes 32 unnecessary HMux keys

**Date:** 2026-10-14 (Asia/Tokyo). **Independent research stream:** SHIP-M18 COMPLETED; M19 NOT STARTED. User PI said “好的，请继续” after M17. **Parent research:** SHIP evaluation-key memory; **NEW** subtarget is fixed-depth integer digit geometry, **NOT** reactivation of M11–M17 β-GLWE engineering, nor concurrent I219 sparse-key security. **Original scientific parent:** Cheon, Hanrot, Kim, Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / IACR ePrint **2025/784**, §5.1 / printed page24 base-B discussion.

**STATUS:** **PASS** one narrow, exact source-shaped key-count/rotation-index optimization; **UNCLEAR** production encrypted CKKS correctness, noise, end-to-end latency, source patch/compiled parity, concrete security and publishable novelty. No author HEaaN flaw claimed. This is a **small and probably engineering-level algorithmic layout improvement**, not independently established a new cryptographic contribution.

## Read before write / isolation / primary sources

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, concurrent `findings/ship-memory-STATE.md` **I218** SHA `55fa828f2257c85817d9f6da2db76be620821a2f`, and `findings/ship-memory-M17-fused-hmux-integration-gate.md` SHA `81e2134f7e9f52b67add2cb87ad44d8d3b6d548a`. M17 concluded **PARK β-GLWE fused HMux**, since no Rust toolchain, local repo or Internet/DNS; do NOT generate M18 toy for that old hypothesis. Parallel SHIP I-series is investigating sparse-window security and low-q D2S exposure; do NOT duplicate it or write its active state. The global `STATE.md` belongs to vFHE. **Only this standalone M18 finding is written**, and prior work is preserved.

Original paper `2025/784` read through connected Research MCP: cached 33-page PDF mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, `VERSION_UNVERIFIED`; physical p24 discusses base-B mux decomposition, regular-spaced secret-window assumption, and why B>=3 can be favorable under hoisting; physical p25 table provides authors' actual HEaaN parameter choices, **different from Poulpy illustration below**. Extracted text includes corrupted glyphs and no screenshot available, so the **exact 129 candidate arithmetic is sourced to PINNED POULPY CODE, not asserted to be the paper's measured HEaaN instance**.

Independent Poulpy `poulpy-fhe/poulpy` pinned commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**:
- `poulpy-ckks/src/layouts/ship/plan.rs` blob **`364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`**:
  - `mux_candidates() = ceil((2*window+1)/theta)`;
  - `mux_bases()` uses greedy `b=min(mux_base,ceil(mux_candidates/cap))`, starting cap1, multiply cap by b until cap>=target;
  - `mask_rotation(slot)=(slot*N/h-window) mod (N/2)`.
- `poulpy-ckks/src/layouts/ship/secret.rs` blob **`e570595f803a4a114c0e4d5a62d0a7af96057e9d`**: sampled sparse support offset `u=(j-slot*N/h+w) mod N` and from-support validation guarantees `0<=u<=2w`; source windowed support may have duplicate-rejection correlations, irrelevant to deterministic full-coverage check.
- `poulpy-ckks/src/encoding/ship/masks.rs` blob **`2754eafd1ad24c1eca1382204d37005449f88cca`**: onehot mask selector `c=u mod theta` and public rotation `p+c`. Mask count remains `4*theta`.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob **`8be6ab92846168330100efeabe9fa19dbd9720e4`**: for `weight=theta` and each group base b, selects `digit=(u/weight)%b`, generates **exactly b independent GGLWE HMux key encryptions** with rotations `d*weight mod m` for d0..b-1; then `weight*=b`. Keyset validation derives the expected groups using `plan.mux_bases()`, so changing the schedule **requires updating ShipPlan::mux_bases (or extending plan to store an explicit vector), regenerating all keys and using matching validation**, not merely deleting an existing key.
- `poulpy-ckks/src/reference/ship/mux.rs` blob **`e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`**: one hoisted mux group per digit in fixed serial order, loops all b candidates with VMP products, per-candidate output Galois, once-per-group IDFT/normalize. The proposed schedule has **the same number of groups** and maximum b, but different candidate rotations and independent key samples.
- Conditional existing prepared-IFMA memory count from M05/I203: `N16384,h32,theta4,w256,base2k52,dsize1`, **90MiB per HMux prepared GGLWE**, and complete named baseline evaluation-key payload `44.53515625GiB`. NOT actual RSS nor necessarily cryptographically 128-bit parameters (parallel I216 warns about this).

## ONE primary smallest falsifiable hypothesis + ONE cheap decisive test

**[HYPOTHESIS M18]** Under exactly `N=16384,h=32,w=256,theta=4,mux_base=4`, with exactly **four sequential HMux radix groups** and per-group radix bounds `2<=b_i<=4`, Poulpy's greedy `[4,4,4,3]` is NOT a minimum-sum basis: `[4,4,3,3]` still represents **all** legal offset-index states `u∈[0,512]`, preserves source mask low-digit and public-rotation composition for each support, and reduces each support's total independent HMux key count from15 to14 (32 total), WITHOUT extra mux depth or larger maximum group.

**[FALSIFIER]** Reproduce pinned `ShipPlan::mux_bases` and exact keyset digit+mask index equations, exhaustively enumerate all 513 legal offsets and all h32 support slots, verify new low/mux-rotation sum `(p+c+Σ_j d_j*weight_j) mod m == (p+u) mod m`. Enumerate every four-group tuple `b_i∈{2,3,4}`; if none of sum<=14 covers the 129 high-digit possibilities, or any u/slot fails exact rotation reconstruction, FAIL.

## Exact derivation [DERIVATION]

At `window=w256`, `2w+1=513`, `theta=4`, low digit `c=u mod4`, and the high digit `v=floor(u/4)` has **129** possible values (0..128). All correct mixed-radix plans only need `∏_i b_i >=129`, not necessarily a power of fixed B4.

**Current source greedy**:
```
  b=(4,4,4,3)         cap=192>=129
  sum b=15            HMux keys=h*15=32*15=480
```
**Counterexample to greedy optimality**:
```
  b'=(4,4,3,3)        cap=144>=129
  sum b'=14           HMux keys=h*14=32*14=448
```
The exact digit rule `d_i=(floor(u/(theta*∏_{j<i}b_j))) mod b_i` and `weight_i=theta∏_{j<i}b_j` is the standard unique positional representation of `v=floor(u/theta)` whenever `v<∏b_i`. Therefore
```
  u = (u mod theta) + Σ_i d_i weight_i,
```
and this equality holds in integers for every u0..512. Source public rotation `p=slot*N/h-w (mod m)` and each mux candidate rotates by `d_i weight_i (mod m)`, hence identical overall target rotation modulo m. Public Galois element of each candidate changes as appropriate with that new rotation; keys must be newly generated with their own output-secret automorphism. Neither source group count (4) nor maximum group radix(4) rises. The number of candidate VMP calls per leaf decreases from15 to14 under same keyset schema; actual noise/precision and timing must be established experimentally.

**Optimality only within stated restrictions**: enumerate all 3^4=81 four-group tuples with every b_i between2 and4. Exactly six permutations of (3,3,4,4) attain the minimum sum **14** with product144. Every tuple sum<=13 has product<129 (max is 108 via one 4 + three 3). Choice [4,4,3,3] preserves the original first two group bases, but is not the unique optimizer; no global/security optimality over other theta, count of stages, KDM assumptions or key compression proven.

**Conditional memory**: each prepared mux key90MiB source-shaped ⇒ 480×90MiB = **42.1875GiB** → 448×90MiB = **39.375GiB**, saves **2.8125GiB = 6.6667% mux prepared-key bytes**. Complete prior **named** evaluation-key payload `44.53515625GiB` → **41.72265625GiB** assuming all non-mux categories unchanged, saving **6.31524% of named prepared-key payload**. These comparisons are **not peak RSS**, compile runs or a 128-bit-security-matched Pareto frontier. No exact HEaaN latency claim.

## Executed decisive source-shaped integer verification

**Runnable local script (actually executed):** `/mnt/data/ship_m18_mixed_radix_min_key_audit.py`, SHA256 **`259df7c967d4db8ede3e9eb44a3fa71be9cf905cfb135d05f57d74625601a556`**.
**JSON result:** `/mnt/data/ship_m18_mixed_radix_min_key_results.json`, SHA256 **`ea07616152bea21a14758f045e65bd94eb1cf25a1327639bd727fe53720d2980`**.

Test assertions **PASS**:
- Exact source greedy recovers `[4,4,4,3]`.
- 81/81 enumerated four-group tuples considered; mathematical minimum key sum14 with six solutions including `[4,4,3,3]`.
- 513/513 legal u offsets old and new schedules represent exactly; new schedule all 14 candidate digit labels actually reachable (no merely dead keys counted).
- 32×513=**16,416/16,416** source public mask rotation and mux index combinations identical mod m8192. In particular worst u512 is covered.
- Base/max group4 and 4 sequential mux stages unchanged.
- Conditional memory key count **480→448**, 32 keys and 2.8125GiB saved in the illustrative IFMA prepared-key-only scheme.

**Excluded:** This is an **integer index-level algebraic proof/exhaustive audit**. It is not a full encrypted CKKS correctness result, no one sampled new GGLWE, no full noisy mux loop, no Rust compile, no timing, no memory RSS, no novel cryptographic security theorem, and not a concrete 128-bit security claim for N16384. Rotations changing changes key distribution/cost constants and noisy result, despite ideal index equality.

## End of iteration

**STATUS:** **PASS** exact source geometry, exhaustive rotation correctness, minimum total HMux key count within fixed 4 layers/max radix4; **UNCLEAR** real noisy FHE correctness/security and concrete total cost; **HUMAN_REVIEW** novelty/importance. Independent Poulpy layout audit, NOT a published SHIP flaw.
**RESULT:** At source-shaped w256/θ4, 129 high-digit states require only radices [4,4,3,3], not greedy [4,4,4,3]. K480→448 without extra stage, static named key-payload 44.53515625→41.72265625GiB (6.315% saved), six optimal permutations; no new security assumptions in the *form* of each key, but joint-security cannot be claimed solely from this shape audit.
**NEXT_ACTION (SHIP-M19 only after PI continues):** ONE falsifiable **cost-and-noise frontier gate for mixed-radix schedules** with **the same four stages/max radix4**. Source-audit candidate-specific public Galois operation counts, group output_size `gglwe_product_accumulation_output_size` dependence on term_count, and whether all six minimum-key schedules also weakly dominate [4,4,4,3] in *source-calculated* memory/scratch/operation counts, without quietly asserting equal stochastic noise distributions. If any schedule is technically inferior due increased group guard/buffer or fused-hoist cost, falsify broad dominance and retain only key-count PASS. Existing Rust implementation not available; no fake runtime. PI can opt to park trivial engineering delta instead of M19.
**STATE_UPDATE:** YES new independent M18 file only. **DO NOT** touch concurrent `findings/ship-memory-STATE.md`, global `STATE.md`, or old M17 β-helper archive. M18 is the active checkpoint in this stream.
