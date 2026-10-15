# SHIP-I231 — One-hot HMux key reconstruction: amortization and matched memory-lifecycle frontier

**Date:** 2026-10-15 (Asia/Tokyo). **PI explicitly said continue SHIP.** Latest previous completion SHIP-I230; I231 is ONE technical test on the I229 compression candidate's memory/work frontier. Original SHIP: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT2025, ePrint 2025/784, physical §4.2/§5.1 Algorithm5; cached original PDF mirrored 33 pages SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, **VERSION_UNVERIFIED**. All backend/source calculations refer ONLY to independent third-party **Poulpy** commit `250d4392656cd313f92ca66d96d8865702d39ddf`, NOT original authors' HEaaN.

## One primary hypothesis + cheapest decisive falsifier

**H231 [bounded source-shaped workload/Pareto target]:** For one batch of **B<=32** real-CKKS SHIP bootstraps using the SAME dense secret and evaluation-key bundle, on-demand I229 onehot-completion with one omitted HMux per slot per radix digit group can *simultaneously* (1) reduce **resident named key bytes** against an unchanged-key I222 **disk-backed current-group streaming** comparator under matched external storage treatment and an explicit prepared-auxiliary cache policy; and (2) require at most **20% additional symbolic ring polynomial-product slots** relative to baseline B×480 SHIP HMux VMPs, even treating a KSK ring-product slot and a baseline HMux ring-product slot as equally expensive. This is not an empirical running-time hypothesis. **FAIL** if either of the two concrete conjunctive budgets fails for the documented cache policies. The arbitrary 20% is an explicit PI-value screening *cost threshold*, not a complexity theorem, practical SLA, or lower bound on all implementations.

**ONE test:** Read the exact pinned source's prepare/consumption lifetimes and VMP dimensions, integer-count KSK preprocessing and named bytes, and calculate B1/8/32/37/74 arithmetic only. Compare against **I222/I223 I224** matched on-demand original key strategy, not only source eager `ShipKeySet::prepare`. No Rust benchmark because no `cargo`/`rustc` runner exists in this container and no Poulpy compiled executable is connected. No repeated n16 numerical toy or unrelated new hypothesis.

## Direct primary-code evidence

At pinned Poulpy:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `ShipKeySet::prepare` around lines 220–321 **eagerly prepares** all keys but each individual HMux can be prepared independently; `ShipKeySet::generate` around lines 500–533 makes for each support and group exactly one hidden onehot digit. `hmux_rot_key_encrypt_sk` around 350–414 gives rank2 input `(beta*s,beta)`, rank1 output and dnum9 k_aux52, physical key k520 at raised ciphertext k468.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`, `ship_bootstrap_roots` lines ~172–230 consumes HMux digit groups sequentially and holds h+1 leaves before a product tree. Each key can be released after its group finishes, given a new source API.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce` performs one rank2 prepared GGLWE VMP per candidate with shared input DFT hoisting, then per-candidate public automorphism/accumulation, one final normalization per digit group.
- `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b0b61` prepared VmpPMat dimensions `N*dnum*rank_in*(rank_out+1)*key_size`, `PrepareHint::Reuse`. In the IFMA plan prepared DFT word16 bytes, raw coefficient word8 bytes. Rank2 original at dnum9,size10=90MiB prepared/45MiB raw. Rank1 extra cross-domain KSK for a source HMux row input k520 at dnum10,size11=55MiB prepared/27.5MiB raw, physical k572. Rank1 unconditional u at dnum9,size10=45MiB prepared/22.5MiB raw.
- `poulpy-core/src/reference/keyswitching/glwe.rs` blob `67fd537f256687a95bf1c7c719392a0d49fe5827`, `gglwe_product_dft_reference` and `gglwe_product_pmat` use prepared `dnum*rank_in*(rank_out+1)` VMP matrix, together with input decomposition, IDFT/normalize (more operations not reflected in simplistic slot count). Rank1 source row is 2 components at k520, 10 limbs =2.5MiB raw.
- Prior independent findings: `findings/ship-memory-I229-onehot-completion-cross-keydomain-gate.md` (I229 exact algebra, 6336 conversions, conditional 23.54% prepared key savings), `findings/ship-memory-I230-crossdomain-ksk-full-degree-ideal-noise-envelope.md` (term-specific exact-torus ideal noise DOES NOT kill the construction, but full error/security unknown), `findings/ship-memory-I222-hmux-groupwise-prepared-residency-gate.md`, `findings/ship-memory-I223-hmux-microbatch-group-reuse-gate.md`, `findings/ship-memory-I224-microbatch-pi-encoding-memory-gate.md`, `findings/ship-memory-I225-key-streaming-batch-novelty-prior-art-gate.md`.

## Matched memory-lifecycle gate [EXECUTED exact integer arithmetic, conditional]

Pinned `N=16384,h=32,theta4,mux_bases=(4,4,4,3),base2k=52,k_ct=468,physical source HMux key k520, extra KSK k572`.

- Source eager prepared-key-only payload I203: `480*90MiB + 2404MiB = **44.53515625GiB**`.
- I229 eager prepared *stored* (without omitted keys materialized): `352*90MiB + 11*55MiB +4*45MiB+2404MiB=**34.0517578125GiB**` =23.5396% smaller, **but this unfairly neglects the original unchanged-key streaming option**.
- Matched **raw-in-RAM + one current prepared group** baseline I222 `480*45MiB+4*90MiB+2404MiB=**23.79296875GiB**`. I229 `352*45MiB+4*90MiB+45MiB reconstructed transient raw+785MiB extra prepared+2404MiB=**18.978515625GiB**` ⇒20.23477% named-memory reduction, assuming stored raw extra aux can be discarded after preparation. This is NOT a process RSS bound.
- Matched **disk-backed original raw HMux**: original resident `180MiB raw current group +360MiB current group prepared +2404MiB other prepared=**2.875GiB**`; I229 current group 135MiB retained raw+45MiB reconstructed raw+360MiB prepared +2404MiB others +**785MiB** all extra prepared aux = **3.6416015625GiB**, **0.7666015625GiB WORSE**. Even if extra prepared aux restricted to only the current maximum radix-4 group (3*55 +1*45=210MiB), model named resident increases to **3.080078125GiB** versus 2.875GiB. Additional KSK/DFT scratch and transient output ciphertexts NOT accounted. More exotic aux staging could trade this RAM for additional I/O/preparation; there is no unconditional memory lower bound for every schedule.
- Raw HMux source storage (outside memory under disk policy) original **21.09375GiB**; I229 stored retained HMux + new extra auxiliary RAW ciphertext keys `352*45MiB +11*27.5MiB+4*22.5MiB = **15.85205078125GiB**` = **24.84954% reduction in this subset's raw storage**. That is a genuine conditional **stored-key-byte** improvement, distinct from online RAM. If missing 128 raw HMux are expanded once and stored to avoid future recompute, add 5.625GiB, making I229 stored raw 21.47705GiB, **more than original**.
- If eager expanding and retaining 128 missing prepared keys (and the 785MiB extra aux), prepared key resident = **45.3017578125GiB** (worse than original full eager44.535), so memory saving requires expansion-on-demand / discard.

### Request-specific batch payload

I223 source real SHIP 33 leaves/request at k468 =**74.25MiB** per request; I224 eager `pi` encodings 512×0.25MiB=**128MiB** per request (slot-lazy `pi` hypothetical **4MiB** per current support). The **eager named live payload** adds 202.25MiB per request, excluding scratch/input/accumulator and unprepared objects.
- B32: same-comparison disk original `2.875 +32*202.25MiB = **9.1953125GiB**`; I229 `3.6416015625 +32*202.25MiB = **9.9619140625GiB**`.
- B74: disk original **17.49072265625GiB**, I229 **18.25732421875GiB**. Memory is named content, not necessarily all live or peak RSS.

## Symmetric symbolic VMP work/accounting [EXECUTED, not measured time]

I229 omits 1 rank2 GGLWE HMux per each support group: `32*4=128` omitted. The source 352 retained are used to reconstitute 128 missing keys. Each contains 2 input-secret columns ×9 gadget rows; each row (a rank1 GLWE ciphertext at k520) is **separately cross-domain keyed**:
```
KSK_calls_per_reconstruction = 32 * [(4-1)+(4-1)+(4-1)+(3-1)] * (2*9)
                             = 6,336.
```
One original HMux VMP has `9*2*2=36` symbolic coefficient-ring polynomial product slots. **480 original HMux per single real bootstrap** ⇒ **17,280** slots. Each key-to-key rank1 KSK has `10*1*2=20` slots; 6336 calls ⇒ **126,720** extra slots per same-key batch before *extra* KSK input decomposition/NTTs, output IDFT/normalize, reconstruction adds, and key `gglwe_prepare`. The 126720/17280=**22/3≈7.3333** proxy for one bootstrap, even if symbolically counting one elementary ring-product slot as equal across key types. Since some KSK products are at wider moduli and source HMux uses shared input hoisting, this equal-cost proxy is generally *optimistic*, but **NOT a formal hardware cost lower bound**: backend optimizations, batching and representations could alter actual work.

If **same key batch B** and missing keys are reconstructed just ONCE while all B requests process the corresponding current support/radix group, extra symbolic ring-product slots per request relative to baseline HMux is `(22/3)/B`:
- B1: **733.33%** extra;
- B8: **91.67%**;
- B16: **45.83%**;
- B32: **22.9167%**;
- B37: **19.82%**;
- B74: **9.91%**;
- B128: **5.73%**.
Threshold for <=20% proxy is **B>=37**; <=10% **B>=74**. These are **necessary only for the naive given symbolic cost model and reuse policy**, NOT hard thresholds for actual runtime or all algorithms. Work on original online data ciphertexts remains 480*B HMux VMP; this is additional *evaluation-key preprocessing*, not ciphertext×ciphertext multiplications or extra multiplicative depth.

Key-ciphertext logical handling per batch: each input source 520-bit GLWE row is 2.5MiB; 6336 inputs cover **15.46875GiB** and 6336 switched outputs another **15.46875GiB logical row volume** (can stream accumulation, not simultaneous memory). KSK prepared keys have **605MiB** combined working set; referencing one 55MiB KSK for each switch corresponds to **340.3125GiB nominal operand sizes summed over calls**, but **NOT evidence of 340GiB actual DRAM or disk reads** (cache and kernel reuse matter).

**H231 verdict:** **FAIL** the conjunction for this explicit matched disk-backed-current-group-policy and B<=32:
- resident named key memory candidate 3.6416GiB > 2.875GiB original; and
- B32 optimistic symbolic extra work22.9167% > threshold20%, worse for B<32.
An in-memory raw-key storage-bound regime retains conditional I229 ~20.23% modeled RAM saving and B>=37 may amortize work; not a logical impossibility of all I229 deployment niches, but no measured end-to-end superiority or new security theorem.

## Novelty, security and full program decision

Prior art for generic inter-operation key reuse, group-major batching, on-demand generation includes:
- Kim et al., **ARK: Fully Homomorphic Encryption Accelerator with Runtime Data Generation and Inter-Operation Key Reuse**, IEEE/ACM MICRO 2022, https://arxiv.org/abs/2205.00922 / DOI 10.1109/MICRO56248.2022.00086. This establishes prior key reuse/generation concepts, NOT identical SHIP onehot cross-secret key completion.
- Putra et al., **Strix: An End-to-End Streaming Architecture with Two-Level Ciphertext Batching for Fully Homomorphic Encryption with Programmable Bootstrapping**, IEEE/ACM MICRO 2023, https://arxiv.org/abs/2305.11423 / DOI 10.1145/3613424.3614264. TFHE-specific implementation, not proof SHIP-specific construction is old.

**I229 security remains UNCLEAR:** new 11 cross-output-secret KSKs and 4 unconditional keys at physical modulus k572 change the joint key distribution; no inherited original SHIP hybrid/KDM proof, no estimator certificate of sparse/dense HW192 λ128 at selected N and high q. I230 bounded only ideal key-sample + coefficient-normalization noise, not full CKKS numerical precision and backend. No end-to-end Rust IFMA compiled runner in this environment. The present budget scan is not a novelty or impossibility theorem.

**STATUS:** **FAIL H231** practical selected matched-policy B<=32 Pareto-screen; **PASS** exact source-shaped integer key-memory and symbolic VMP-work arithmetic; **UNCLEAR** compiled latency/real RSS, security, novelty and B>=37 specialized workloads. **RESULT:** conditional prepared-only 23.54% key saving is mostly overshadowed in resident RAM by source I222 group streaming, while I229 recomputation adds 6336 high-q switches per batch and fails the <=20% additional symbolic product target at B<=32. **RECOMMEND PARK I229/I230 cryptographic-completion candidate** until an independently verified, realistic security-matched source implementation and a SPECIFIC workload benefit overcome the chosen cost gate. **SHIP parent research stays HUMAN_REVIEW / PI-selected**, not automatically renamed or switched to another project. Do not continue small batch-number variants as independent research iterations.

**NEXT_TEST / PI gate:** Before I232, require a genuinely different cryptographic compression/fusion mechanism that avoids large high-precision key-to-key re-expansion, OR actual pinned Rust benchmark with λ128-matched parameters and explicit selected workload (B>=37 with queueing and live pi/leaf residency). If neither, recommend PI PARK SHIP cryptographic optimization and choose another FHE composition target. Do not claim expected runtime win or novelty without those. **STATE_UPDATE:** YES detailed finding + both SHIP/global STATE checkpoints only, after read-before-write and readback verification; old files preserved.

## Reproducible exact calculation

`/mnt/data/ship_i231_cost_gate.py`, SHA256 `c38baf129d5a03930465e43d5c1fe271ab1059dedafc5369b2167b4fd0f5c709`; `/mnt/data/ship_i231_cost_gate.json`, SHA256 `d4934e3b149b84abb2fb4a517398ddf4e5b4ac07ec89610f7c7a21d31161e6e7`. Script executed in current chat, exact rational/integer assertions PASS. Python outputs are local files and not themselves committed; all decisive facts and formulas are recorded here.
