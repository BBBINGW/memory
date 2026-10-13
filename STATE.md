# FHE Research State — After Iteration 173

**Checkpoint:** 2026-10-13 · `main` · **I173 COMPLETED; I174 NOT STARTED**.
**Authority:** Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`. Human PI chooses final contribution, direction and park; agent executes ONE smallest falsifiable claim + ONE cheapest decisive test, explicit [FACT]/[DERIVATION]/[SPECULATION], then archives and stops. Earlier 151-iteration historical log: `logs/state-pre-session-handoff-2026-10-13-iteration151.md`, opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`.

## CURRENT TARGET

**SHIP encrypted-selector evaluation-key memory — HUMAN_REVIEW / recommend PARK generic seeded-persistent-storage subbranch after I173.** Original paper Cheon–Hanrot–Kim–Stehlé *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, IACR ePrint **2025/784**, Research MCP full 33pp mirror PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742` VERSION_UNVERIFIED. §3.3 already describes algebraic four-mask sum storage relation; §4.4 uses four encrypted selector masks per candidate and has paper-vs-implementation hybrid-stage reversal; author HEaaN source/RAM unknown.

**Pinned third-party code** Poulpy `poulpy-fhe/poulpy` `main` SHA `250d4392656cd313f92ca66d96d8865702d39ddf` (2026-10-11) is NOT authors' HEaaN or byte-identical implementation. I172 confirmed real SHIP `M=4hθ` individually encrypted rank1 selector CKKS ciphertexts (complex 8hθ), `ShipKeySet::prepare` eagerly creates M (or 2M) separate prepared two-column convolution operands `CnvPVecL`. I173 tests **existing generic seeded GLWE** as an alternate key **storage** format: one body polynomial + public 32-byte PRNG seed vs full rank1 body+mask, saving close to HALF persistent coefficient bytes, but `GLWEDecompress` fully regenerates the mask, and current SHIP prepare path STILL allocates/prepares M full two-column convolution buffers; bootstrap consumes them. Thus **FAIL claim persistent seed compression automatically cuts prepared/runtime key residency without new algorithm**. Known seeded compression cannot be claimed novel. No actual HEaaN memory or benchmark, no novel secure prepared-key sharing scheme yet. Recommend PI PARK generic SHIP selector memory audits unless a true nontrivial secret-choice-hiding prepared-key representation is found; PI decides.

**Previous targets PARKED by PI assent:** I170 ePrint 2024/164 BGV NTT collapse; I168–169 2025/1403 AKS generic basis key linearity; I167 2025/711 unpacked AHE cosmetic; I165–166 2025/257 HFP covariance; I160–164 2025/429 CKKS first-stage weighted fitting; I156–159 SPRU rounded-noise microaudit. Cascudo vFHE ePrint 2025/286 CRT scalar digit ideal-PI OP P1 remains OPEN/SOURCE-GATED, latest revised official 2026 PDF unavailable. Earlier MRFHE source-fork gate and all archived failures preserved.

## LAST COMPLETED ITERATION

**I173 (2026-10-13), I174 NOT STARTED.** Record `findings/ship-seeded-glwe-storage-vs-prepared-keys-gate-iteration173.md` blob `78554f7e5b92b5eb65e9b0b2680d31298b0ea647`; ONE decisive pinned implementation test. Standard Poulpy `GLWECompressed` one-column body+seed `poulpy-core/src/layouts/compressed/glwe.rs` blob `19654f6adbbfeb6312e59ed33a03175c89ca468f` and actual `glwe_compressed_encrypt_sk_reference` `poulpy-core/src/reference/encryption/compressed/glwe_ct.rs` blob `94a482c25cac797c1f0c175cb52ce841dadedf61` show **seed must be chosen for mask at ENCRYPTION TIME**, not assigned to existing arbitrary mask; decompression expands full mask from seed. `poulpy-ckks/src/layouts/ship/keyset.rs` pinned blob `8be6ab92846168330100efeabe9fa19dbd9720e4` `ShipKeySet::prepare` then allocates `CnvPVecL(N,2,ceil(kk/base2k))` for each mask. Bootstrap `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542` consumes all. **Same runtime preparedness arrays persist in the unchanged evaluator.** Strictly not a performance/memory peak benchmark.

## CURRENT QUESTION

Can SHIP eliminate or share a large fraction of **prepared (not just serialized)** selector operands in a representation whose index/sign occupancy remains computationally hidden and without adding prohibitive per-bootstrap preparation time, rotations, ciphertext noise, or key storage elsewhere? I173 establishes seeded-only persistent compression is **not enough** and is known. NO new active candidate proven. Recommend PI PARK if only ordinary GLWE seeded serialization was proposed.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I173 FAILS joint persistent+prepared reduction without extra online transform using generic seeded GLWE; PASS near-50% raw persistent payload and proof full prepared operands remain in existing evaluator. A novel runtime-key compression requires a new technique. No HEaaN author-code comparison.

## CURRENT EVIDENCE

- **[I173 exact source-code+arithmetic gate]** Poulpy `GLWECompressed` format is one body polynomial and 32-byte seed, with `GLWEDecompress` regenerating the mask from seed; generic seeded encryption route exists and explicitly generates mask from chosen seed BEFORE encrypting. For M=4hθ rank1 selector ciphertexts, `S_full=M·2N L W` and `S_seeded=M·(N L W+32)`, `L=ceil(k_raised/base2k)`, W=coefficient word byte count. Example (illustrative, not measured) h32 θ4, N16384, L9, W8, M512: **1.125GiB** uncompressed coefficient buffers vs **0.562515GiB** seeded body+seeds, ~50% payload saved; 16KiB public seeds. However unchanged `ShipKeySet::prepare` still creates M distinct `CnvPVecL(n,2,L)` left convolution operands and runtime bootstrap reads all, so **prepared-key memory count/format does NOT decrease**. Source code `poulpy-core/src/reference/encryption/compressed/glwe_ct.rs`, `poulpy-core/src/layouts/compressed/glwe.rs`, `keyset.rs` and `bootstrap.rs` pinned commit `250d4392656cd313f92ca66d96d8865702d39ddf`. Not new algorithm, no HEaaN-source or peak measurement. Archive `findings/ship-seeded-glwe-storage-vs-prepared-keys-gate-iteration173.md`.
- **[I172 exact PINNED CODE]** `poulpy-fhe/poulpy` main commit `250d4392656cd313f92ca66d96d8865702d39ddf`, `keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `masks.rs` blob `2754eafd1ad24c1eca1382204d37005449f88cca`, `plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: for each support index, `ShipKeySet::generate` produces 4θ fully randomized `CKKSCiphertext` encryptions, and if complex another 4θ; `validate_material` requires exact counts; `ShipKeySet::prepare` turns every one into `CnvPVecL` individually. The raw coefficients are rank1 standard `GLWE` with width `kk` torus limbs. Source stores no compressed or masked-selector-sum encoding in this exact path. Its separate `poulpy-core/src/layouts/compressed/glwe.rs` seeded GLWE type is NOT used by inspected SHIP keygen. Mask plaintext zero structure: only secret `u%θ` column, at most two of four bands nonzero; direct public sparse omission would reveal secret choice. Finding `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md`.
- **[I172 DERIVED exact formula]** Raw unprepared selector coefficients:
```
S = (4hθ) * 2N * ceil(raised_k/base2k) * sizeof(W),   real
S_complex = 2S,
raised_k = base2k*ceil((((ceil(log2(h+1))+2)*log_delta_work)+log_budget_out)/base2k).
```
Illustrative but **NOT deployment-tested** Poulpy-compatible h32 θ4, base2k52, logDelta40, logBudgetOut104, W=8byte: depth6, raised_k468, limbs9, count512; N8192→0.5625GiB, N16384→1.125GiB, N32768→2.25GiB **raw masks only** (complex double). Not from paper's LL14/HT15 RNS table; actual HEaaN unknown. Prepared backend convolution memory cannot be inferred as exactly 2× and is not measured.
- **[I171 FACT SOURCE]** Original ePrint2025/784 §3.3–4.4 and Table2+Table3: for literal independent full-PQ RNS selector storage, source LL14 (`N16384,h31,θ9`) has 1116 masks/2.7246GiB **conditional RNS64** and HT15 (`N32768,h31,θ17`) 2108 masks/20.5859GiB **conditional RNS64**; dense bitpacked capacities 1.8604 and14.1689GiB. No original HEaaN measurements and authors explicitly mention mask-sum storage sharing. Do not represent estimates as HEaaN RAM or Poulpy runtime.
- **[OTHER ARCHIVES]** I170 BGV HomNTT complete direct CRT full diagonal density already treated in original §4.1, PARKED. I169 generic AKS basis key combination known RLWE linearity with extra noise, PARKED. I164 p1-only weighting 3.5% ideal improvement, PARKED. I166 correlated HFP input failure outside paper premise, PARKED. vFHE P1 SOURCE-GATED as before.

## MAIN OBSTRUCTION

Standard seeded GLWE encryption is **already implemented** and reduces only persistent full ciphertext payload about half; evaluating SHIP still needs all M full left-convolution prepared masks at the same backend memory layout if the current eager plan is unchanged. Reconstructing original masks adds PRNG/DFT work at key preparation; caching prepared forms retains memory; streaming can trade memory for runtime/parallelism and may spoil SHIP's primary low-latency contribution. Direct omission of encryptions of zero would reveal secret selection/sign. Original authors already flag the four-mask algebraic relation. No unseen innovation should be claimed from generic serialization. No actual author HEaaN key-layout/peak memory or latency checked.

## OPEN UNCERTAINTY

Original HEaaN high-precision real key residency, exact CPU portable/AVX prepared DFT bytes, possibility of confidential mask-sharing based on *public* encrypted relation with fewer prepared operands at no additional heavy rotations; tradeoff of per-query recomputation and secrecy of sparse secret support; actual novel security/noise/cost improvement. No evidence of a suitable new scheme yet.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I174 NOT STARTED — HUMAN_REVIEW/PARK.** Recommend PI PARK the **generic seeded-storage compression** micro-direction immediately: known technique, cannot eliminate prepared runtime mask count. If PI wants to continue **SHIP** specifically, formulate ONE genuinely new source-aware compression of **prepared selector operands** that uses ciphertext-safe algebraic relations and preserves hiding of `u mod θ` and sign and preserves the 32-core low-latency benefit; first read original SHIP §3.3 four-mask relation so as not to rediscover published sharing. Require explicit cost/precision/security statement before another experiment. If no plausible nontrivial mechanism, park broader SHIP simple-memory track and pivot to distinct source-accessible FHE algorithm challenge. No more elementary parameter count or generic PRNG seed examples.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md`.
2. `findings/ship-seeded-glwe-storage-vs-prepared-keys-gate-iteration173.md` — current full source gate.
3. `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md`; `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md` — prior genuine count and source estimates.
4. Public Poulpy pinned full `keyset.rs`, `compressed/glwe.rs`, `reference/encryption/compressed/glwe_ct.rs`; ePrint2025/784 §3.3, §4.4.
5. `findings/OPEN_RESEARCH_BRANCHES.md` optional archival status; vFHE P1 and prior parks unchanged.

## STATUS

**I173 CLOSED: FAIL strong no-online-change hypothesis that seeded GLWE compression shrinks both stored+prepared SHIP keys / PASS ~half raw unprepared coefficient storage saving from generic seeded encryption and source confirmation M prepared masks remain / UNCLEAR novel prepared-key sharing or original HEaaN memory. I174 NOT STARTED.** Recommend PARK seeded serialization idea subject to PI, keep broader SHIP direction HUMAN_REVIEW only with genuinely new prepared-key mechanism. No source paper security/correctness flaw, benchmark, measured performance or novelty claim. Older archives intact.
