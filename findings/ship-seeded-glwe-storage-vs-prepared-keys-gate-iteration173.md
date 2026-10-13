# Iteration 173 — Seeded GLWE cuts persisted SHIP selector bytes ~50%, not existing eagerly prepared-key footprint

**Date:** 2026-10-13. PI approved one further source-grounded iteration with “好的，请继续” after I172. Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` (I172 blob `57ac7895d29be2f5e2c3496538e9039a1c3d4fbd`) → `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md`. ONE primary hypothesis and ONE decisive real-code layout-and-prepare test, supplemented by exact storage arithmetic. No encryption benchmark or measured peak memory.

## Evidence provenance and source versions

- **Original publication, context only:** Cheon, Hanrot, Kim, Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, ePrint **2025/784** https://eprint.iacr.org/2025/784, complete 33pp GitHub-mirror Research MCP PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742` (latest official bytes VERSION_UNVERIFIED). §§3.3/4.4 already discuss encrypted mask and algebraic sum memory reduction. This iteration does **not** measure original authors' HEaaN memory or claim source-equivalent implementation.
- **Tested pinned independent third-party implementation:** Poulpy GitHub `poulpy-fhe/poulpy` `main` commit **`250d4392656cd313f92ca66d96d8865702d39ddf`** (2026-10-11), source fetched via connected GitHub, and the following blob-grounded files:
  - `poulpy-core/src/layouts/compressed/glwe.rs`, blob `19654f6adbbfeb6312e59ed33a03175c89ca468f`: seeded `GLWECompressed` with one body `VecZnx` + public **32-byte seed**; `bytes_of` for one coefficient polynomial p299–301; `GLWEDecompress` p343–377 reconstructs all mask polynomials from seed.
  - `poulpy-core/src/reference/encryption/compressed/glwe_ct.rs`, blob `94a482c25cac797c1f0c175cb52ce841dadedf61`: reference `glwe_compressed_encrypt_sk_reference` constructs full temporary GLWE with mask **generated from seed before encryption**, adds plaintext and noise, copies body into compressed representation and retains seed, lines66–107. This **must be used when creating ciphertext**, not an arbitrary lossless seed recovery from existing random mask bits; seeded compression is already known/generic Poulpy code.
  - `poulpy-core/src/layouts/glwe.rs` blob `d437d5b1eaa456f2e8c108920c88391b195082b6`: rank1 standard GLWE has body and one mask polynomial; `GLWE::bytes_of = VecZnx::bytes_of(N,2,ceil(k/base2k))`.
  - `poulpy-hal/src/layouts/vec_znx.rs` blob `a4bf4ccaf6a4bba8fa9cacaeffcdf8029329e52f`: `VecZnx::bytes_of=N*cols*limbs*sizeof(W)`.
  - `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `ShipIndexKeys` requires `h` groups of **4θ independent full CKKSCiphertext** masks (plus separate 4θ masks2 for complex), `ShipKeySet::generate` calls `ckks_encrypt_sk` without compression, `ShipKeySet::prepare` lines267–301 maps each full ciphertext to a separately allocated/prepared `CnvPVecL(n,2,mask_size,Reuse)`, all stored in `ShipKeysPrepared`.
  - `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: lines174–192 consumes `ik.masks()/ik.masks2()` and calls `ship_masking_accumulate`; no consumption of seeded encoding or direct single-polynomial selector here.

## Primary hypothesis (ONE) and falsifier

**[HYPOTHESIS]** Replacing all full-rank1 SHIP selector encryptions with Poulpy's already implemented seeded GLWE format is a **no-additional-online-transform** compression that reduces BOTH (i) persistent/serialized key data and (ii) the full set of prepared convolution operands resident during bootstrapping, at equal selector functionality.

**[DECISIVE CODE TEST]** Inspect real seeded GLWE layout+encrypt/decompress and SHIP `ShipKeySet::prepare` / evaluator signature at one pinned commit. Compare the selector raw-buffer bytes using verified `GLWE::bytes_of` vs `GLWECompressed::bytes_of`, and count prepared `CnvPVecL` objects and columns. If seeded representation must regenerate full GLWE and SHIP prepares every selector as two-polynomial left convolution operand, the conjunction FAILS even though persistent storage shrinks.

## Exact derivation and one illustrative source-format arithmetic check

For real SHIP with `M=4hθ` masks, rank-1 GLWE ring degree `N`, torus limbs `L=ceil(k_raised/base2k)` and word width `W_bytes=sizeof(W)`:
```
Full per mask raw coefficients              = 2 N L W_bytes.
Seeded per mask raw coefficients plus seed =   N L W_bytes + 32.
S_full(M)    = M · 2 N L W_bytes.
S_seeded(M)  = M · (N L W_bytes + 32).
saving       = M · (N L W_bytes − 32).
saved_ratio  = 1/2 − 32/(2 N L W_bytes).
```
These are **raw coefficient buffers** with added 32 seed bytes, NOT exact serialized size: binary format includes shape, metadata, noise component etc; no actual serialization timed. Source's GLWECompressed Writer writes seed and metadata, so these are payload-level expressions. The same formula doubles `M` in complex version. Security/correctness of using per-ciphertext independent seeded randomness follows ordinary seeded GLWE encryption model conditionally on a secure PRNG and appropriate seed generation; this audit does not independently prove formal security.

One fixed **illustrative** Poulpy-compatible shape (NOT paper LL14/HT15, no implementation measured) from I172:
`h32,θ4,base2k52,k_raised468, L9, W_bytes8`; M=512. Exact integer arithmetic:
| N | full raw GiB | seeded raw+seed GiB | saving raw GiB | remaining prepared mask count |
|---:|---:|---:|---:|---:|
|8192|0.562500|0.281265259|0.281234741|512|
|16384|1.125000|0.562515259|0.562484741|512|
|32768|2.250000|1.125015259|1.124984741|512|
Total public seeds = 512×32 B = 16KiB. So raw long-term storage saves **near 50%**. At the exact same `ShipKeySet::prepare` interface, all **512** selector ciphertext masks must eventually be regenerated into full rank1 coefficient representation and individually preprocessed into 512 two-column `CnvPVecL` objects. The prepared backend memory is `M*module.bytes_of_cnv_pvec_left(N,2,L,Reuse)` **conditional on backend**; no generic GiB claim without fixing backend and runtime. Existing code does eager `Vec<CnvPVecL>`; it does not keep or evaluate the seed itself.

**Crucial distinction:** If a new program stores ONLY seeded key data until startup, then expands+prepares once, it saves disk/transport and may reduce pre-start in-RAM stored raw keys. If it keeps both raw uncompressed keys and prepared keys, raw transient memory can be optimized by dropping originals; but seeded format alone **does not alter the number and format of resident prepared keys**, and adds a seed PRNG expansion and preparation step. Streaming/on-demand prep could reduce peak resident prepared memory **at a cost to online latency/bandwidth**; this is **a different scheduling/representation mechanism**, not proven in I173.

## Scientific result and next gate

**STATUS: FAIL the combined no-extra-online-work persistent+prepared memory hypothesis**; **PASS trivial/published generic ~50% raw-payload persistent storage compression** under source-compatible seeded encryption from outset; **PASS existing prepared path remains full M two-column convolution operands**. `GLWECompressed` already implements the trick; this is not novel. Validity under same masking secret and output precision requires correct cryptographic seeded encryption wiring, re-expansion metadata and parameter matching; was source-inspected, not coded/benchmarked.

**No new finding of paper bug or publishable improvement.** SHIP paper already flags mask relations and third-party repo has seeded encrypt/decrypt primitive, so 'compress disk by 2×' is **known technology**. Generic seeded-only persistent compression candidate **PARK**. The broader SHIP in-memory prepared-key compression remains a potentially real technical question only if one can derive a confidentiality-preserving representation that eliminates prepared objects or demonstrates measurable latency-neutral memory savings; none is yet provided. Avoid repeated theta/ring size toy data.

## End of Iteration 173

**STATUS:** FAIL strong no-online-change dual-storage-compression hypothesis; PASS near-half persistent payload bound and source proof of unchanged full prepared count; UNCLEAR novel runtime-memory and real HEaaN impact.
**RESULT:** Existing Poulpy generic `GLWECompressed` keeps one body+32-byte seed (rather than body+mask); seeded encryption uses pre-generated uniform-looking pseudorandom masks; `ShipKeySet::prepare` still generates all `M=4hθ` two-column convolution left operands, and evaluator uses them all. Example M512,N16384,9limbs,W8: 1.125GiB raw→0.562515GiB raw+seed, but 512 prepared operands remain. Not a measured memory/time benchmark.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK seeded-only SHIP storage optimization**. If PI wants broad SHIP direction to continue, require ONE nontrivial algorithmic candidate for **prepared-key** sharing/reduction that provably hides selector index/sign, preserves CKKS correctness/security and avoids extra online heavy operations; first ensure original §3.3 sum-mask relation is not already equivalent. Otherwise recommend PARK entire SHIP simple memory-audit track and choose distinct FHE cost frontier. No more simple source count/sizing repetitions.
**STATE_UPDATE:** **YES** — material negative feasibility gate closes anticipated quick compression path; preserve I171–I172 genuine third-party key-memory evidence.
