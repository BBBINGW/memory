# SHIP I206 — Fixed-source modulus-budget falsifier for shared HMux key plus CKKS encrypted bit multiplication

**Date:** 2026-10-14 (Asia/Tokyo). Independent SHIP sequence I206, after I205. Separate from frozen global FHE I192 counter and independently active vFHE V-series. PI explicitly continued the current HMux key-memory track. No upstream Poulpy edits, no compiled CKKS experiments.

## Read before write / source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, current global `STATE.md` SHA `8a4835f55cf2b778c7aac29f89c9a826226410c8` (parallel vFHE V10; **do not edit**), `findings/ship-memory-STATE.md` SHA `cd1f3357484ae9591c924e0b87d64d6a0e916c40` (I205 completed), and `findings/ship-memory-I205-fixed-rotation-selector-factor-gate.md`. Prior H205 disproved affine-only reuse, leaving nonlinear encrypted bit gating open.

Original scientific parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784. **Inspected implementation is independent third-party Poulpy**, not author HEaaN: fixed `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.
- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: tree_depth = ceil(log2(h+1)), raised_k = limb-roundup((tree_depth+2)*ld+log_budget_out), mux_candidates and mux_bases.
- `poulpy-ckks/src/test_suite/ship.rs` ship_suite_plan: h32, window=(N/h)/2, theta4, mux_base4, work precision=min(test precision,40), budget_out=2*base2k.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`: masking accumulator stamps scale=ld, budget=raised_k−2ld at matched input scales; no newer standalone rescale invocation.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f5ce`: original HMux uses GGLWE VMP+Galois DFT domain sum, **does not perform ct×ct multiplication or deduct ld from log_budget metadata per mux digit**.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: sequential **all mux digit groups** per support precede a binary ciphertext×ciphertext product tree over `h+1` leaves, odd entries carried; product-tree checks available budget and consumes max input scale.
- `poulpy-ckks/src/api/mul.rs` blob `e365dc087bd2d20fb62447031d04c8d95c8c468a` and `reference/mul.rs` blob `783a231eb98b8871107270e2f3354884644bfcfd`: source ct×ct multiplication metadata `budget_new=min(budget_a,budget_b)−max(scale_a,scale_b)−max(0,natural_k−dst.k)`, `scale_out=min(scale_a,scale_b)`. `poulpy-ckks/src/error.rs` blob `cd56a881438a226915224b94b33ca849cad9a637`, `checked_mul_ct_log_budget`: fails with `MultiplicationPrecisionUnderflow` when the minimum budget is lower than maximum input log_delta.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: currently has only support-specific HMux GGLWE keys; shared-beta-independent key and encrypted beta ct **not yet implemented**. Existing dense tensor/relinearization key generated at raised precision for existing tree.

## ONE PRIMARY HYPOTHESIS + ONE MINIMAL DECISIVE TEST

**H206 [HYPOTHESIS TO FALSIFY]:** At the I203 source-selected IFMA real-SHIP parameters `N16384,h32,theta4,base2k52,ld40,budget_out104,mux_base4`, the fixed-rotation *shared HMux KSK → output Galois alignment → Enc_s(beta)×Enc_s(Rot_d(x))* factorization can replace original mux groups WITHOUT increasing `ShipPlan::raised_k` and still execute the existing entire `h+1` product tree, retaining the original `log_budget_out>=104` target, **provided encrypted selectors have the same 40-bit scale and sufficient input budget**.

**One falsifier:** Following source's exact budgets at ONE representative leaf as it traverses four mux digits and then a maximum-depth (six-level) product-tree path, find any multiplication precision underflow or root budget <104 under unchanged raised_k. This is a necessary metadata budget gate, not security/correctness/physical error, and not an assumption that the variant is implemented.

## Exact arithmetic and witnessed failure [DERIVED, EXECUTED]

Using source test-plan-shaped parameters:
`N=16384, h=32,window=256, theta=4,base2k=52,ld=40,budget_out=104,mux_base=4`.
`tree_depth=ceil(log2(33))=6`.
`mux_candidates=ceil((2*256+1)/4)=129`; `mux_bases=[4,4,4,3]`: **four serial mux digit groups**.
`raised_k=52*ceil(((6+2)*40+104)/52)=468`.
After original masking: `scale=40, budget=468−2*40=388, effective_k=428`.

**BASELINE:** Original mux VMP does not reduce the metadata budget: after four digits still 388. Along a six-multiplication source tree path (take equal scale40), budget `388→348→308→268→228→188→148`. Root target `148>=104`, spare 44 bits.

**CANDIDATE:** Assume best-case public shared KSK/Galois itself costs no additional metadata budget (optimistic) and every `Enc_s(beta)` operand has scale40 and budget **at least the left current operand's budget**. Every inserted ciphertext×ciphertext product *necessarily* consumes 40 bits in the source contract. Four serial mux groups: `388→348→308→268→228`, effective k at end `268`. Tree then `228→188→148→108→68→28`; at level 6, source checks `min_budget>=40` and finds `28<40`: exact `MultiplicationPrecisionUnderflow` (other carried branch at budget228 is enough). Therefore **H206 FAIL**, regardless of Galois key noise or timing. If beta ciphertext has insufficient budget or ct destination is narrowed, this only fails earlier.

Equivalent candidate full path requires 4 extra **multiplicative levels** at scale40. To preserve **original target** `root_budget>=104`, a best-case unrounded necessary input width is `(2+6+4)*40+104=584` bits; source-required limb rounding to 52-bit multiples gives `raised_k_candidate>=624`, an increase of **156 bits**, with true root budget `624−2*40−4*40−6*40=144>=104`. The source's existing `raised_k=468` cannot accommodate the variant without revising parameters; simply retaining k468 and accepting lower precision is **not even executable through all six tree levels** under the unchanged source multiplication API.

**IMPORTANT QUANTIFIER:** These are **worst-case/deepest-path, sequential four-digit, equal 40-bit-scale** calculations for the explicit candidate described in I205, not a lower bound against all possible encrypted-control representations. A lower-precision selector, changing the mux grouping/radix, batching gate placement, GGSW external product, higher k, bootstrapping/relinearization changes, or an entirely different FHE design could have distinct depth behavior and needs separate verification. Raising k would itself increase every key's gadget dimensions and encryption/NTT cost, even if shared HMux object count drops; thus naive original-versus-shared key memory numbers **must not** be compared at the same 468-bit layout. No security proof: a shared KSK of (s,1) under every rotation-dependent key may create new KDM-key exposure not automatically covered by the original SHIP joint-key security game.

**Online operation burden (derived from explicit naive factorization, not a universal minimum):** For each of h supports and every public mux candidate, the proposal must select one encrypted β without revealing it. Source counts `sum mux_bases=4+4+4+3=15` candidates/leaf, hence the direct unfused variant would use up to `h*15=480` **additional ciphertext×ciphertext multiplications** (plus the shared KSK applications and original final 32-support product tree), with 4 extra serial levels along each support leaf. Some β=0 does not allow the server to skip a candidate without revealing selection; pre-public skips are not justified. This count does not prove all optimized gate batching needs 480 multiplications.

## Reproducibility and limits

Executed deterministic local Python to reproduce exact source formulas and tree-pairing order, including the actual odd-leaf carry across 33 leaves:
- `/mnt/data/ship_i206_hmux_shared_control_budget_gate.py` SHA256 `c74d8f6146e3f2ccfdfc0eba6963595aa27c5ec00f83e385c7d68c26c63a4034`
- `/mnt/data/ship_i206_hmux_shared_control_budget_results.json` SHA256 `9e7a4a8a31e17967d3c425ee65a9670ce2373ffbd68ee199e72d2f4fb0bd3dea`.
Script asserts: 4 digit groups, source raised_k468, baseline root budget148, candidate fails level6 with input budget28 vs scale40, and candidate raised_k624 gives root budget144. **NOT a compiled Poulpy or actual encrypted ciphertext test, no noise/security/latency/physical memory result**.

## End of Iteration

**STATUS:** **FAIL H206 same-width full-pipeline feasibility**. **PASS** source-budget necessary-gate falsifier. **UNCLEAR** feasibility with raised modulus / lower-scale selectors, performance/memory frontier, actual CKKS correctness/security, and novelty. **NOVELTY NOT VERIFIED**.

**RESULT:** A fixed-d shared-beta-independent KSK with one CT×CT encrypted selector multiplication per mux digit stage inserts 4 additional serial 40-bit multiplications. For the pinned illustrative plan, the original raised_k468 becomes insufficient: source product tree fails at level6. Restoring 104-bit root budget requires raised_k≥624 (plus actual noise margins), which makes the previous I203 468-bit HMux memory baseline **not directly comparable** to any redesigned shared-key system.

**NEXT_ACTION:** **HUMAN_REVIEW**: strongly recommend PARK this specific dense-CKKS-CT×CT-per-digit HMux key sharing variant as low-priority because it fails fixed parameters and shifts 4 full depth levels / ~480 online multiplications; do not claim universal compression impossibility. If PI insists on this cost frontier, next *one* quantitative check is total prepared payload incl. shared KSKs, encrypted beta ciphertexts and widened tensor/automorphism/selector keys at the 624-bit setting, before implementation. If PI instead approves a meaningfully different HMux technique, select its smallest falsifiable claim only after prior-art/source review. No changes to globally separate vFHE state.

**STATE_UPDATE:** YES independent SHIP checkpoint; NO global STATE.md; no upstream changes.
