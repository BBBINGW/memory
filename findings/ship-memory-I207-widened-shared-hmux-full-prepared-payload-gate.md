# SHIP I207 — Full prepared-key memory gate for widened shared-HMux / encrypted-selector construction

**Date:** 2026-10-14 Asia/Tokyo. Independent SHIP continuation after I206. PI's “好的，请继续” selects I206's proposed cost check, not a new parent research direction. Read-before-write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` (separate vFHE V10; do not edit), independent `findings/ship-memory-STATE.md` SHA `055da5b31a7d67579565a3376b344253bfa6e270`, I206 budget finding and I203 total-key memory finding. No modifications to Poulpy or global vFHE.

## Sources [FACT]

Original scientific target: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784. **Audited code is independently developed Poulpy, NOT authors' HEaaN** at immutable commit `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.

- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: tree_depth6 for h32, `raised_k=round_up_base2k((depth+2)*ld+budget_out)`; window256/mux candidates129/mux bases [4,4,4,3].
- `poulpy-ckks/src/test_suite/ship.rs` and `poulpy-ckks/src/test_suite/mod.rs` blob `e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb`: key auxiliary guard `dsize*base2k+log2(N)` for rank1 tensor and Galois.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: original 4*h*theta=512 selector CKKS ciphertexts; HMux rank-in2/rank-out1 switching keys with `dnum=ceil(k/(base2k*dsize))` and aux `base2k*dsize`, at every support and digit candidate; dense-to-sparse key one rank1, dnum1; eagerly prepares all.
- `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: `VmpPMat(N,dnum,rank_in,rank_out+1,key_size)` where `key_size=ceil((dnum*dsize*base2k+k_aux)/base2k)` per `poulpy-core/src/layouts/mod.rs`.
- `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs` blob `3e2bc4c38b80533f0c758a0c869a395c1938736f`: IFMA `VmpPMat`, `CnvPVecL` and `CnvPVecR` all store each prepared coefficient/limb at **2×u64=16 bytes**.
- `poulpy-ckks/src/reference/mul.rs` blob `783a231eb98b8871107270e2f3354884644bfcfd`: `ckks_prepare_right_reference` allocates `CnvPVecR(N,rank+1,ceil(k/base2k))` and uses effective k. `ckks_mul_prepared_assign_reference` uses the existing tensor key to relinearize; no lower-cost encrypted selector multiplication is assumed or established.
- I206 `findings/ship-memory-I206-shared-hmux-ctmul-budget-gate.md` established for the **specific full-scale CT×CT selector-gating variant**: baseline k468 leaves budget148; four added mux-depth CT×CT products at 40-bit scale cause underflow at k468; to retain ≥104-bit root budget requires `k>=584` and 52-bit limb rounding gives `k_new=624`, ideal root budget144. **This is metadata only**, not numerical/physical error/security proof.

## ONE primary hypothesis and one falsifier

**H207:** Despite widening k from 468 to 624 to pay for the four serial encrypted-selector CT×CT levels, a candidate storing exactly **15 beta-independent rank2 HMux KSK prepared objects reused across h=32 supports**, **480 distinct full-width beta=Enc_s(beta) selector ciphertexts prepared as right CT operands** (one per support per digit choice), the **original 512 selector masks** at widened k, **one widened tensor key, one widened Galois key, and the original bottom dense-to-sparse key** would reduce the **complete modeled prepared-key payload** by at least **50%** versus the original source-compatible k468 layout with the same ≥104-bit final output budget target.

**Falsifier / one minimal test:** Apply exact source prepared-backend byte formulas and counts to *all named retained objects* at their correct 468 / 624 precision, with **no selective omission of encrypted beta**, and sum. If candidate ≥0.5×baseline, H207 fails. Do not assume packed beta, duplicate-rotation dedup, shortened beta, zero-cost selector or runtime speed. This is a conditional **candidate representation** not implemented in original Poulpy; full correctness/security remain separate gates.

## [DERIVED; EXECUTED exact integer allocation arithmetic]

Parameters `N=16384, h=32, theta=4, base2k=52, window=256, mux_bases=[4,4,4,3], ld=40, budget_out=104, dsize=1, tree_depth=6`. IFMA prepared coefficient size16 bytes.

**Original k468 baseline (exact prior I203 reproduced)**
- rank2 HMux prepared `VmpPMat`: dnum9,size10,rank_in2,rank_out1, 90 MiB each × 480 = **42.1875 GiB**.
- 512 prepared selector masks `CnvPVecL(N,2,9)`: 4.5 MiB each = **2.25 GiB**.
- rank1 tensor and Galois prepared keys: dnum9,size11,49.5 MiB each = 99 MiB.
- dense-to-sparse key dnum1,size2=1 MiB.
- **TOTAL = 47,819,259,904 bytes = 44.53515625 GiB**. Metadata root budget 148 bits.

**Widened candidate k624, same target output budget**
- assume 15 public *(digit,choice)* rotations have one **shared across supports** beta-independent prepared HMux KSK each: dnum12,size13,rank-in2,out1, **156 MiB each ×15 = 2340 MiB = 2.28515625 GiB**. Conservative: d=0 repeated in different groups not deduplicated.
- keep all 512 original selector masks (no original selector compression!), widened `CnvPVecL(N,2,12)` each6 MiB → **3072 MiB=3.0 GiB**.
- use **all 480** encrypted scalar/slot beta ciphertexts as full 624-bit rank1 `CnvPVecR(N,2,12)` prepared-right, each **6 MiB ×480=2880 MiB=2.8125 GiB**. No optimistic beta bit packing/seed compression/streaming used; this is a safe numerator if such ciphertexts exist and can be correctly encrypted.
- tensor and Galois prepared keys: `dnum12,k_aux=52+log2(N)=66,key_size14`, rank1, **84 MiB each=168 MiB=0.1640625 GiB**.
- unchanged bottom dense-to-sparse switching key: **1 MiB**.
- **TOTAL conditional prepared candidate payload = 8461 MiB = 8.2626953125 GiB = 8,871,182,336 bytes**.
- **SAVING = 44.53515625 −8.2626953125 = 36.2724609375 GiB (81.4468029120%)**. **H207 PASS** strict arithmetic under stated conditional key format.
- With optimally stage-sized instead of **full width** beta (one independent secondary accounting note, not a second primary test), the four groups' minimum beta ciphertext effective widths to have budget≥current leaf budget would be k=[584,544,504,464] (prepared limbs [12,11,10,9]); candidate total ~7.93457 GiB, BUT numerical noise/security/actual feasibility not tested and the primary claim does not need this additional assumption.

**Why comparison is fair but limited:** The original k468 yields root log_budget148 and widened candidate best-case k624 yields root log_budget144; both exceed stated ≥104 threshold, i.e. candidate is **not** quietly dropping target output budget. Exact root budgets are metadata under zero additional KSK/Galois numerical penalty, NOT a precision guarantee. IFMA prepared buffers are not process RSS. Longer k may increase runtime substantially: ~480 **new CT×CT products**, 4 extra serial levels for a leaf, plus the existing 480 shared-KSK **applications** and product-tree costs. Shared KSK reduces *number of retained prepared key objects*, not necessarily applications. The candidate is not in Poulpy code and runtime cannot presently be benchmarked.

## Critical unverified constraints [OPEN]

1. **KDM/circular security:** new reusable key switching material for `(s,1)→sigma_g^{-1}(s)` and separate `Enc_s(beta)` is a *different joint key distribution* from source SHIP's correlated beta-dependent `(beta*s,beta)`; no security reduction from original SHIP keygen was established (unlike I201's purely public selector compaction). Could be blocked independently.
2. **CKKS correctness/physical precision:** need proper encrypted beta encoding (all slots same bit, scale40), source-aligned Galois, gates, potential key-switch noise, and k624 support; metadata budget≥104 is insufficient as proof. Buffering full beta ciphertext at 624 may also be overkill; any optimization requires new gate.
3. **The 8.263GiB total is conditional** on actually replacing 480 original per-support HMux objects with 15 shared keys + 480 newly encrypted beta operands while leaving other keys intact. No source-based implementation exists; cannot claim actual application memory, keygen peak, network transport or external author-HEaaN numbers. No `cargo`/`rustc` runner, no compiled ciphertext benchmark.
4. **Latency and work:** simple implementation adds **~480 ciphertext×ciphertext multiplications**, fully high-precision, and 4 serial product levels per leaf. Even large memory savings may be a Pareto trade-off unacceptable in practice. No timing benchmark or cost lower bound on alternative factorizations.
5. **Novelty:** NOT VERIFIED. Known encrypted-control machinery/CMux exists; this is a conditional transplantation and memory counter, not publishable evidence.

## Reproducibility

Script executed successfully with asserts against the I203 original total and exact component sizes:
`/mnt/data/ship_i207_widened_shared_hmux_prepared_payload.py`, SHA256 `eb910ed65a151c376e2cb1c83358ad88b7bcc63b70452b68def020cb3f397096`.
`/mnt/data/ship_i207_widened_shared_hmux_prepared_payload.json`, SHA256 `56b1e9cecb1ca5f58635b0b3aa9fa71ea0d4369ea2deda63beb66091e04fbdfe`.
Local simulation of layouts only; not a complete algorithm implementation.

## End of iteration

**STATUS: PASS H207 (strict conditional prepared payload threshold).** **UNCLEAR** construction security, correct FHE realization, noise, implementation, end-to-end memory/latency, and novelty. **NOVELTY NOT VERIFIED**.

**RESULT:** I206's required 156-bit modulus increase does NOT automatically destroy the prepared-key memory saving: even counting 480 full-width (expensive) beta controls, the proposed cross-support shared-HMux layout remains 81.45% smaller by source IFMA formulas. But the added online CT×CT ×480 and new key distribution could independently kill the research idea. This is a *conditional resource frontier question*, not a usable FHE optimization.

**NEXT_ACTION:** For PI continuation, first **ONE decisive security-distribution audit** on the required reusable beta-independent rank2 switching key bundle: Does the source original SHIP **joint evaluation-key KDM/security assumption actually cover** the new shared `(s,1)→sigma_g^-1(s)` KSK + separately encrypted hidden beta bits? Try reduction by efficient public postprocessing of existing full SHIP keys (I201 precedent), or exhibit a clear distributional mismatch/uncertified assumption. If this cannot be justified, mark HUMAN_REVIEW/PAUSE instead of investing in 480 high-precision nonlinear gates. Only if security survives check a realistic online cost. Do not modify global STATE or upstream code automatically.

**STATE_UPDATE:** YES independent SHIP only; NO global vFHE STATE.md.
