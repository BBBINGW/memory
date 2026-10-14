# SHIP-M15 — Mixed DFT accumulation needs explicit radix alignment

**Date:** 2026-10-14 (Asia/Tokyo). **Independent SHIP M-series:** M15 COMPLETED; M16 NOT STARTED. The PI authorized this one round by saying “好的，请继续”. **STATUS:** FAIL naive mixed DFT direct addition / M14 offset-92 interpretation; PASS abstract exact torus algebra with an explicit 52-bit reweighting; UNCLEAR actual Poulpy IFMA correctness, timing, key security and memory. No SHIP original-paper flaw alleged.

## Read before write; research boundary

Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, findings/ship-memory-M14-beta-glwe-public-polynomial-convolution-source-gate.md SHA 00f36e9e94f7b01423c93b2538b1d2f3d79a0dec, M13 SHA 66ac0b0bc5a70742ab872fc19b507bf7147270aa; inspected concurrent findings/ship-memory-STATE.md SHA 949917e68aee56c946cc3827e2392517796e88f1 (independent I214) and global STATE.md SHA 7af97fb3ee38ae139fd12f867fd9eccb18d22d16 (independent vFHE V17). The M15 target was absent. Do not overwrite either shared state. This M15 file is the independent recovery checkpoint.

Scientific parent SHIP (Cheon, Hanrot, Kim, Stehlé, EUROCRYPT 2025 / IACR ePrint 2025/784), §5.1 Algorithm 5. Source: independent Poulpy code pinned to commit 250d4392656cd313f92ca66d96d8865702d39ddf, **not** authors' HEaaN. No executable Rust Poulpy run or full HEAA-N benchmark this round.

Background M14: retain first βs gadget column of each HMux GGLWE and replace its second β gadget column by one 520-bit GLWE encoding β2^92; multiplied by public 428-bit body B. Previously estimated 90→47.5MiB per mux key and 44.73% saving in the specifically named complete prepared-key payload. Those numbers are conditional allocation formulas, not measured RSS, with major accuracy/security and runtime gaps.

## ONE falsifiable primary hypothesis, ONE decisive test

**[PRIMARY HYPOTHESIS M15]** Since both retained βs-GGLWE product and new β-GLWE×public-body convolution live in Poulpy VecZnxDft, their candidate results can be directly summed after public Galois twists without any numeric radix-weight conversion, before a single group normalization, while preserving the torus phase that each path would produce if separately normalized.

**[FALSIFIER]** Compare the pinned source normalization offsets and construct a two-candidate exact negacyclic torus-phase test with nontrivial public Galois twist. If unmodified sum differs from separately normalized path, FAIL direct fusion. An explicit scale-adapted algebraic fix is allowed as a diagnostic, NOT counted as implementation success.

## Precise pinned source [FACT]

- poulpy-ckks/src/reference/ship/mux.rs blob e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce: original per-candidate gglwe_product_dft_reference + vec_znx_dft_automorphism_with_plan + sum_dft, once-per-group IDFT and vec_znx_big_normalize at signed res_offset=0. Existing gadget product DFT output ~10 limbs for the illustrative parameter.
- poulpy-core/src/reference/keyswitching/glwe.rs blob 67fd537f256687a95bf1c7c719392a0d49fe5827: with dsize=1, product dispatches vmp_apply_dft_to_dft, which outputs in VecZnxDft and pads surplus limbs with zeros; its comments warn lower limbs can affect later normalization by carry.
- poulpy-hal/src/api/vmp_pmat.rs blob e8bf2d438a399213a5bb199c7c8c506e4c66ee22: VMP DFT product supports destination wider than prepared key and zero fills limbs beyond pmat size. This by itself does NOT fix scale.
- poulpy-core/src/reference/operations/glwe.rs blob f8a53bdca1f3c02348da45c96327a82f8bf0c852: glwe_mul_plain_reference convolves (10-limb helper GLWE)×(9-limb integer body) into a 19-limb DFT, then IDFT+normalizes EACH candidate. The exact function cnv_offset_to_limb_offset(v,w) maps v=0,w=52 to (hi=0,lo=-52), and v=92,w=52 to (hi=0,lo=+40). Both use the SAME raw convolution DFT window hi=0. Only the last signed normalizer factor changes by **2^92**.
- poulpy-hal/src/api/vec_znx_big.rs blob 13cf51f2d3c6be966bfbad6c6cfab36833193a6f: vec_znx_big_normalize's contract scales the BigWord torus value by 2^res_offset before canonical output rounding at target precision. Therefore cnv_offset92 does **NOT** automatically implement 520→428-bit drop of βhelper guard; M14 erroneously equated these operations. The target res_k precision is a separate contract.
- poulpy-hal/src/api/convolution.rs blob fbf6ac2db6b44368643e5676a31d700a08352602 and poulpy-hal/src/api/vec_znx_dft.rs blob 0978684f3abdb8f0e3afc892e7158915e10cbf33: source DFT addition, prepared polynomial convolution, automorphisms exist, but there is no demonstrated ready-made **mixed-radix scaling adapter**.
- poulpy-cpu-avx512/src/ntt3x42_ifma/vmp.rs blob 78f8a8494a46964440a12fa2b4adb2fa248ade45: per-output zero-fill confirmed. poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs blob 3e2bc4c38b80533f0c758a0c869a395c1938736f: IFMA DFT bytes = N*cols*size*16. No compiled mixed-source fusion present.

## Derivation [DERIVATION], including needed correction of M14

Abstractly treat G_d as the first-branch BigWord torus value (original signed offset0), H_d as the new convolution BigWord torus value (correct integer-polynomial multiply with signed offset -52 when cnv_offset=0). Ignoring final rounding, the intended per-candidate result is

    sigma_g( G_d + 2^(-52) H_d ) mod 1.

An unscaled shared accumulator normalized at -52 instead produces

    sigma_g( 2^(-52)(G_d + H_d) ) mod 1,

which differs by sigma_g((1-2^(-52))G_d). Applying public sigma_g before summing candidates does not repair numeric radix weighting.

An explicit abstract fix is to reweight the old gadget term by 2^52 before merging and use shared -52 normalization:

    sigma_g( 2^(-52) (2^52 G_d + H_d) ) mod 1

which matches independent branches exactly before rounding. This **does not yet specify a safe backend 52-bit limb shift**, and cannot simply be implemented as entrywise DFT addition: it must respect digit order, CRT coefficient signed ranges, carry from discarded low limbs, masked-body torus-to-integer representation, and the output precision k. A 19-limb group accumulator is conceivable but untested. No general impossibility of fusion claimed.

**Correction to M14:** M14 called cnv_offset=92 a direct "92-bit helper guard drop". In the source same high-window index hi=0, choosing 92 instead of 0 moves signed normalizer from -52 to +40 and scales the SAME upstream polynomial by 2^92. Lowering the torus ciphertext precision to k428 is separately set using output res_k. This correction is substantive; the earlier M14 offset claim must NOT be reused without qualification.

## ONE executed exact source-semantics witness

Actually executed local script:
- /mnt/data/ship_m15_dft_scale_alignment_gate.py, SHA256 189c0aab815b780283b62c753b8aa9c59386182bde673dd7900f6004f504355f
- /mnt/data/ship_m15_dft_scale_alignment_results.json, SHA256 cc4f3798c0b64208964863a0ac5701459a3e1e1a64d1d5bfd874f869b066906c

Reproduced source split rule exactly; for same upstream torus-phase number x=2^-100, normalization at -52 gives 2^-152 and +40 gives 2^-60, exact factor2^92, both below 1 so no wrap ambiguity.

One exact Fraction-based toy in R=Q[X]/(X^8+1), canonical output torus precision 2^428, 2 GLWE component columns, two candidates with Galois elements (1,5), contains nonzero GGLWE abstract term G and raw β-helper convolution term H per candidate. Original per-path normalization+twists compared with direct unscaled mixed accumulator+twists modulo1: **4/16 coefficient phases disagree**, max torus circular distance 4503599627370495/18014398509481984 ≈0.25; explicit 2^52 G correction gives **16/16 coefficient phases exactly equal**, zero mismatches. This toy is not encrypted FHE and does NOT validate IFMA carry/CRT or a real HMux key.

At N16384, a two-column 10-limb group DFT buffer is **5MiB**, two-column 19-limb buffer is **9.5MiB** (+4.5MiB per simultaneously live buffer), or +13.5MiB if three DFT scratch buffers all widen (sum/prod/rot). Does not quantify overall RSS or online runtime. Original M14's conditional 44.73% long-lived evaluation-key payload saving may remain an attractive hypothesis, but no performance advantage is established.

## End of iteration

**STATUS:** FAIL naive same-type direct DFT fusion; PASS exact abstract scale-aligned identity; UNCLEAR/HUMAN_REVIEW source-correct fused carry kernel, actual SHIP correctness, security, runtime, RSS, novelty.
**RESULT:** M14 was wrong to equate cnv_offset92 to guard drop; normalizers actually use 0 vs -52 in proposed separate paths, and offset92 changes same convolution BigWord scaling by +92 bits. Galois-twisted 2-candidate torus toy gives ~0.25 error if directly added; correct explicit 52-bit term reweighting fixes ideal algebra. Source allows wider VMP DFT output but not an already validated mixed numeric scale adapter.
**NEXT_ACTION — SHIP-M16 only on PI continuation:** ONE minimal pinned backend radix-shift/carry-window safety gate: can GGLWE 10-limb DFT data be lifted with correct 52-bit weighting into a 19-limb convolution accumulator before public Galois twists, preserving signed carry and output k428 under one normalization? Verify with source-level limb layout and an exact near-boundary carry counterexample; if unsafe/no implementable contract, PARK this optimization and request a compiled variant before further theoretical expansion. Avoid repeating Gaussian simulations and parallel SHIP I-series β-sharing work.
**STATE_UPDATE:** YES this standalone M15 finding only; NO edits to global STATE.md or concurrent findings/ship-memory-STATE.md.
