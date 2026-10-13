# FHE Research State — After Iteration 172

**Checkpoint:** 2026-10-13 · `main` · **I172 COMPLETED; I173 NOT STARTED**.
**Authority:** Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`. Human PI chooses final contribution, direction and park; agent executes ONE smallest falsifiable claim + ONE cheapest decisive test, explicit [FACT]/[DERIVATION]/[SPECULATION], then archives and stops. Earlier 151-iteration historical log: `logs/state-pre-session-handoff-2026-10-13-iteration151.md`, opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`.

## CURRENT TARGET

**SHIP CKKS bootstrapping encrypted selector-key memory — OPEN / HUMAN_REVIEW after I172, third-party implementational gate PASS.** Original paper Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, IACR ePrint **2025/784**, full 33 physical-page Research MCP GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official latest version still **VERSION_UNVERIFIED**. Paper §3.3–§5.4 shows encrypted masks and hybrid column/mux with authors' algorithm vs implemented ordering reversed, and admits algebraic four-mask sum relation can save memory.

**Independent actual code verified:** `poulpy-fhe/poulpy`, GitHub `main` commit **`250d4392656cd313f92ca66d96d8865702d39ddf`** (2026-10-11), implementing SHIP with a *distinct* Rust/torus-limb backend and independent key design; not source-equivalent to original HEaaN nor its timing metrics. I172 pinned code finds `ShipKeySet::generate` constructs **4hθ separately encrypted full rank1 selectors** for real SHIP and **8hθ** for complex SHIP (`masks2`), at `kk=ShipPlan::raised_k` torus precision; no mask-sharing or seeded compression invoked by examined SHIP key-generation path. `prepare` preprocesses each to a distinct `CnvPVecL`. Therefore original I171 key **COUNT** has an independently verified concrete implementation, but original I171 **RNS GiB counts cannot be transplanted directly** to Poulpy's torus-limb layout. Authors' original HEaaN memory remains unverified. No new cryptographic optimization, proof gap, timing or security claim.

**Former branches retained:** I170 ePrint2024/164 BGV HomNTT free sparse collapse **PARKED by PI assent**; I168–169 2025/1403 AKS public linear synthesis **PARKED**; I167 unpacked AHE 2025/711 note **PARKED**; I165–166 TFHE HFP noise covariance **PARKED**; I160–164 2025/429 CKKS p1-only weighted approximation **PARKED**; I156–159 SPRU ePrint2025/651 rounding audit **PARKED**. vFHE ePrint2025/286 P1 ideal CRT scalar-digit issue **OPEN/SOURCE-GATED** pending current official revised PDF; no published current version bug proven. All older branches and missing-source markers preserved.

## LAST COMPLETED ITERATION

**I172 (2026-10-13), I173 NOT STARTED.** ONE pinned third-party implementation key-layout falsifier; findings `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md` SHA `fa07d771f2fe4b06287fdf893b96ec29a2c2a129`. Poulpy Rust `poulpy-ckks/src/layouts/ship/keyset.rs` SHA `8be6ab92846168330100efeabe9fa19dbd9720e4` lines106–120 and467–568: actual `h` `ShipIndexKeys`, each `masks: Vec<CKKSCiphertext>` of count **4θ** and additional `masks2` count **4θ** if complex, separately `ckks_encrypt_sk` per mask; lines574–615 validate counts, `kk`, rank1. `prepare` lines267–301 creates one `CnvPVecL` per ciphertext at `ceil(kk/base2k)` limbs, and `bootstrap.rs` lines174–192 consumes all. `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2` computes `tree_depth=ceil(log2(h+1))`, `raised_k=roundUp_base2k((depth+2)logDeltaWork+logBudgetOut)`. `poulpy-core/src/layouts/glwe.rs` and `poulpy-hal/src/layouts/vec_znx.rs` use 2 polynomials rank1 and `N*2*ceil(raised_k/base2k)*sizeof(W)` per ciphertext. Separate generic `GLWECompressed` API exists, but `ShipKeySet` does not invoke it; no automatic mask sharing/seed compression. `ship_mask_slot_vectors` zeroes all except one of θ candidate columns and at most two nonzero masks within it; **all encryptions still randomized** and naïvely omitting zero-message keys leaks secret selector/support information.

**Status:** **PASS real layout verified**, **FAIL claim third-party masks already collapsed/seed-compressed**, **UNCLEAR original HEaaN RAM/transferability and actual speed/memory saving**.

## CURRENT QUESTION

Can a source-compatible SHIP masking key compression technique reduce **both persistent key bytes and prepared/evaluation bytes** at unchanged security and without destroying low-latency parallel blind rotations? Third-party Poulpy confirms full h·4θ objects exist in one independent reference code, but simple seeded ciphertext serialization or sum-of-four algebraic relations are known; not automatically publication-worthy.

## PRIMARY HYPOTHESIS

**NONE ACTIVE** after I172. I172's claim that independent verified Poulpy SHIP already compacts away mask ciphertext count **FAILS**: code stores `4hθ` full ciphertexts (or `8hθ` complex). Next iteration must test ONE nontrivial, meaningful memory/time frontier beyond banal compression.

## CURRENT EVIDENCE

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

A source-compatible public-key storage reduction must hide the encrypted choice `u%θ` **and secret sign**: although the *message* masks are mostly zero, exposing which ciphertexts can be omitted would leak key bits. Off-the-shelf seeded ciphertext compression can save persistent bytes but prepared operand arrays still require full size and additional re-expansion/DFT; algebraic known mask-sum relation does not magically yield new research. Need separate correct construction/security/noise and representative byte-time accounting, not generic headline 20GiB from unrelated backend.

## OPEN UNCERTAINTY

Real original HEaaN mask storage/peak allocation; compression already implemented in other SHIP variants; Poulpy actual per-backend W and DFT memory allocation, release serialization pipeline and benchmarks; security of derived correlated selectors, possibility of compressing ciphertext masks while retaining hidden support/sign; actual CKKS precision/latency under any new mechanism. Source latest official version unverified.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I173 only on PI “继续”: ONE compression value falsifier, not another θ/N parameter sweep.** First examine pinned Poulpy `GLWECompressed` seed representation vs full unprepared `CKKSCiphertext` mask layout; compute exact savings for source-compatible single-component seedable GLWE plus per-ciphertext seed, AND whether evaluation still needs reconstructing all prepared `4hθ` objects. If persistent-only compression leaves key-preparation/evaluation memory and bandwidth unchanged, **PARK the trivial seeded-storage candidate** and seek a materially new encrypted-mask sharing approach with provable secret-selection hiding and no added online costly operations. Do not claim paper memory improvement based solely on existing seeded ciphertext compression. If implementational mismatch is found, record and stop. PI decides pivot/park. No original HEaaN equivalence claim.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md` — latest verified independent code path.
3. `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md` — source paper algorithm and parameter-based conditional estimate.
4. Pinned Poulpy `poulpy-ckks/src/layouts/ship/keyset.rs`, `plan.rs`, `poulpy-core/src/layouts/glwe.rs`, `poulpy-core/src/layouts/compressed/glwe.rs`, `poulpy-hal/src/layouts/vec_znx.rs`; original ePrint2025/784 §3.3, §4.4.
5. `findings/OPEN_RESEARCH_BRANCHES.md`, other archives/MISSING_SOURCES as needed.

## STATUS

**I172 CLOSED: PASS pinned independent implementation confirms 4hθ stored unprepared full-rank1 selector ciphertexts, 8hθ complex, with separate prepared objects / FAIL hypothesis mask key count already compressed or algebraically collapsed in Poulpy generator / UNCLEAR original author HEaaN exact memory or publishable memory compression. I173 NOT STARTED.** No measured benchmark, correctness/security flaw, novel method, speedup or source-author claim. Previously parked branches unchanged.
