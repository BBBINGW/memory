# SHIP-I258 — Directly shortening gadget dnum drops the most significant row

2026-10-16 · TRACK_ID SHIP ONLY · following I257. Self-contained failure archive. Current GitHub Notes `read_repo_file` is STILL broken (returns `{}` for all existing SHIP states), but `list_repo_files` and immutable public GitHub source reading work. Do NOT modify existing shared states without Read Before Write. No cross-track edits.

## One primary falsifiable hypothesis

**H258:** At pinned third-party Poulpy source-shape `N16384,h32,radix[4,4,4,3],theta4,k468,base2k52,dsize1,dnum9`, later radix groups can use `dnum8` with the rest of the source key-generation/key-product interfaces unchanged and negligible accuracy/noise loss, since the later groups allegedly need less gadget precision. This would nominally reduce keys/online digit products.

**Smallest decisive test:** Inspect EXACT source gadget-digit order and instantiate an exact, noiseless, valid onehot HMux input with only the omitted high digit nonzero. Check whether skipping row `dnum-1` preserves the selected `beta(a*s+b)`, and whether subsequent Galois group rotations attenuate any error.

## Provenance [FACT]

Independent third-party `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, **NOT original author's HEaaN/security-matched h31 configuration**:

- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` lines399-410: `dnum=ceil(k_ct/(b2k*dsize))`, `k_aux=b2k*dsize`, rank2->1.
- `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5b6fca808a07d0` lines134-145: row `row_i` is placed at **physical limb `(dsize−1)+row_i*dsize`**, increasing low→high.
- `poulpy-core/src/reference/keyswitching/glwe.rs` blob `67fd537f256687a95bf1c7c719392a0d49fe5827` lines203-214,303-320: product consumes `dnum`/the rows in precisely that order; reducing dnum blindly removes top, not bottom limb.
- Original SHIP ePrint 2025/784; the illustrative Poulpy `k468` cost model is not certified original-author HEaaN or a matched 128-bit security setup.

## One exact falsifier [DERIVATION, EXECUTED]

In toy `R=Z_(2^24)[X]/(X^16+1)`, base `B=256`, old dnum3 vs new dnum2, take legal onehot `beta=1`, ternary `s=X-X^3`, public input `a=(q/4)*X`, `b=0`. The digits of a at low rows i0/i1 vanish, while its high row i2 contains 64. Full correct selected result is `(q/4)(X^2-X^4)`; truncated key gives `0`, hence `||error||_infty=q/4=4194304`. A later Galois automorphism is a signed negacyclic monomial permutation, preserving `||error||_infty`; **16/16 exact tests** spanning four group positions and four Galois alternatives retained q/4 residual after three more rotations. Sampling 2048 uniform full-width coefficients, `1052/2048` have circular omitted-top-digit residual ≥q/4. These are plaintext algebra checks, not a compiled CKKS error measurement, security attack or performance benchmark.

The tempting source-shaped change 480 keys×90MiB→80MiB, reducing total nominal eager prepared 44.535GiB by **4.6875GiB (10.53%)** and symbolic dnum products by 11.1%, is **INVALID** under H258 because correctness fails.

### Exact local provenance

`/mnt/data/ship_i258_dnum_high_limb_gate.py` SHA256 `ea1026fd22fc222f5dac4ff7432f33f9d33f293246df49d95ecd4a2d63341a93`.
`/mnt/data/ship_i258_dnum_high_limb_gate.json` SHA256 `67b4f561cb59b086599db898e3a9361d3e33ff5c6031996dc2ceb4fd87c1eedd`.

## Verdict and remaining scope

**STATUS FAIL H258 / PASS source row index audit and exact noiseless counterexample.** Source-compatible dnum-- DOES NOT approximate away insignificant low digits: it removes **the highest digit**, with `O(q)` worst-case error. This applies regardless of whether the shortened group is early or late, since subsequent rotations do not reduce coefficient infinity norm. This does NOT rule out a redesigned *reindexed gadget* preserving high rows while skipping low ones, with fresh bounded-error, IFMA normalization, KDM and precision analysis. That variant needs a genuinely new kernel or changed virtual row mapping—not just one fewer dnum.

**NEXT_TEST:** Only if an explicit reindexed high-row-preserving low-row compression exhibits >5-10% **fair** memory/latency improvement under an error budget/security-matched complete bootstrap. Avoid generic digit/radix sweeps. Core SHIP crypto eval-key memory still recommends HUMAN_REVIEW/PARK; original-author security I245 SOURCE_BLOCKED. PI controls any pivot.

**STATE_UPDATE:** Standalone file only; shared STATE/SHIP-STATE not edited because Notes reads remain empty and safe read-before-write cannot be performed.
