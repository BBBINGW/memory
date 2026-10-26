# PURE FHE P0 — CBS Shared Relative-Trace / Multi-Output Test-Polynomial Collision Gate

Date: 2026-10-26 (Asia/Singapore) | **Stage: PURE-FHE-P0-PRESCOUT-09**. This is a source-first, single-hypothesis prescout. User remains PI. NOT a resumption of the separate BOOT, SHIP, CGS official iterations. NO Codex, GPU, native experiment or automatic root STATE changes.

## Primary evidence / source provenance

1. Wang, Wen, Li, Lu, Wei, Liu, Wang, **Circuit Bootstrapping: Faster and Smaller**, EUROCRYPT 2024, ePrint 2024/323 https://eprint.iacr.org/2024/323 . Full 40-physical-page PDF cached and read through research MCP, SHA256 `f25f122bf38f105d29907d7eea7085fc7ab1af13a27b223b75c073b8a66640e4`, **VERSION_UNVERIFIED** compared to publisher. Physical pp12–14 §3: PBSmanyLUT with `ell<=2^vartheta`, LUT arranged in **p blocks each N/p coefficients**, output function values consecutive within a block. Algorithm6 p21 returns ell redundant RLWE outputs by public `X^-j` multiplications. Algorithm1 p14 calls **one full HomTrace per ell independent gadget-row value** before SchemeSwitch. Text p5: trace/scheme switching comprise **3.0%** of the original paper's **different non-high-precision CBS CMUX system**; not the same as RevHomTrace HP-LHE Table4.
2. Lee–Yoon, **Homomorphic Field Trace Revisited: Breaking the Cubic Noise Barrier**, TCHES 2026, ePrint 2025/1088 https://eprint.iacr.org/2025/1088 . Full 30 physical-page PDF source mirror SHA256 `4f1033580542c56baa8a493aab178681082df768cd3446cc4470bc75b49589a9`, VERSION_UNVERIFIED. Physical p11 Alg5 `RevHomTrace(C,n)` ALREADY supports general subring parameter n (partial trace). p11 Theorem4 error bound `Vin+4 logN VMS+logN VAuto`; pp16–17 Table4 `INT_LHE_256,δ=8,τ=2`: Refresh139.59ms, Conv63.47ms, Total203.06ms (31.26% Conv); p17 source computation describes `δ/τ` PBSManyLUT refresh calls, but `δ ell` HomTrace-related conversions. Thus revtrace alone is not the only residual system cost, but among high-precision digit conversion operations it still repeats.
3. Li et al., **BatchBoot**, USENIX Security 2026, complete 20p author prepublication PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf . PDF p8 Alg3 and §4.3 inspected with web PDF screenshot, shows Half.BatchCBS uses batch bootstrapping for RLWE input and extends EP-CBS external product tree. **Batch CBS is already public**, so `share PBS`, `pack secrets`, `external product tree` no novelty.
4. Public CCS 2026 official accepted program https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html and authors https://zhiweiwang.github.io/publications/ confirm **Decoupled TFHE-type Functional Bootstrapping**, Zhihao Li et al. Detailed original text / secure memory+time comparison was **NOT authenticated or parsed**. No claim about its algorithm.
5. Recent `Descent-PBS: Programmable Bootstrapping beyond the Ring Dimension`, ePrint 2026/2616 https://eprint.iacr.org/2026/2616 (public Oct23). Author abstract describes *one* publicly functional keyswitch that collects module components after a rank-cost first rotation. **Abstract-level competition only**, not source proof; subring/module packing and key-format conversion are hot prior art.
6. Relevant historical project BOOT-B075/B076 had already falsified two-message degree doubling with no real arithmetic savings and sparse/dense secret entropy mismatch; these are not new proposals. Source record: `findings/boot-B075-shared-selector-interleaved-ap-packing-cost-gate.md` and `findings/boot-B076-batchboot-subring-hamming-gate.md`.
7. Closest general precedent for *relative trace as a semi-packed coefficient projector* predates these papers (e.g. HElib `Practical Bootstrapping in Quasilinear Time`; authors' actual RevHomTrace already has `n` parameter). Do NOT claim relative trace invention.

## One smallest falsifiable hypothesis and cheapest exact test

**H_FREE_SHARED_TRACE:**
For ell independent outputs `f_j(m)` from a standard `p`-entry PBSmanyLUT on a degree-N single accumulator, we can simply reposition each of ell outputs into a subring-basis coefficient at `j r`, `r=N/ell` (ell divides N) and apply **one** relative `Tr_{R_N/R_ell}` instead of ell full HomTrace evaluations, while retaining the same message-dependent standard blind-rotation offsets `s(m)=m (N/p)`, same full plaintext domain `m∈[0,p)`, one unchanged polynomial, and no additional encrypted permutation / format conversion cost.

**SOURCE-INFORMED MODEL:** In the author's standard many-LUT layout p function-value blocks are length `b=N/p`; for ell outputs require `ell≤b`. If one demands the **fixed** post-rotation output positions j r in the subring, the test polynomial coefficient required for pair (m,j) becomes `a(m,j)≡m b +j r (mod N)` up to one overall sign convention of blind rotation. If two distinct pairs collide at the same polynomial coefficient with arbitrarily different desired values, there is no single legal test polynomial satisfying the claim. This is a **necessary condition restricted to this source-shaped fixed block-shift/reposition map**, not a no-go for alternative LUTs or formats.

**EXACT COUNTEREXAMPLE, computed exhaustively in JS:**
```
N=64; p=16; ell=4; b=N/p=4; r=N/ell=16.
Original adjacent within each block: a_orig(m,j)=m·4+j => 64 distinct positions.
Proposed relative-subring output: a_new(m,j)=m·4+j·16 (mod64).
a_new(0,1)=16 = a_new(4,0).
Hence f_1(0) and f_0(4) must occupy one coefficient; set f_1(0)=1, f_0(4)=0
=> contradiction for arbitrary functions.
Exhaustive count: 16 unique coefficients for all 64 (m,j) source demands;
every used coefficient has four conflicting (m,j) pairs.
```
The phenomenon remains for a larger **illustrative** capacity setup `N=2048,p=256,ell=4,b=8,r=512`: `a_new(0,1)=512=a_new(64,0)`; 1024 demanded positions map to only 256 unique positions. **DO NOT interpret this exact `p=256` as validated concrete `INT_LHE_256` parameter**; it is an abstract test-poly toy on a source-shaped packing pattern. Negacyclic sign/rounding can alter which values coincide up to a sign, but choosing arbitrary independently programmable outputs (incl 0 and 1) still violates a same-coefficient constraint; the explicit toy collision is at identical positions <N.

**STATUS: `FAIL_H_FREE_SHARED_TRACE`**. One plain absolute trace over ell ciphertexts is also insufficient by rank: one field-linear functional of ell arbitrary constant messages cannot produce ell independently specified constants using only public linear operations. A relative trace has dimension ell and avoids that rank loss, but moving outputs into the subring positions **is not free**.

## Repair search, exact existing alternative and cost

Possible **different** interface: keep standard contiguous test polynomial and perform a paid coefficient-permutation/linear-transform on the encrypted accumulator (or redesign the blind-rotation indexing/polynomial and revise source proof) before one relative trace; then construct a batch-aware SchemeSwitch/diagonal output extraction to get ell independent RGSW digit controls.

But:
- Public monomial shift alone cannot send every `j∈[ell]` to `jr` (`j=0` needs shift0; `j=1` needs shift r-1). Thus requires a nontrivial transform / masked permutation / key switching, or an alternate admissible degree/layout tradeoff.
- Relative trace as primitive **already implemented** with `n` in RevHomTrace Algorithm5, so novelty has to be the joint test-poly scheduling + GGSW conversion with lower **whole-system** amortized cost and a genuinely new invariant, not the trace.
- Ciphertext operations must be typed and security preserved (RLWE secret tags and automorphism keys, q/2 MS lifting per stage, key format/dimensions, prepared key memory, noise covariance, DFR, usable output precision, all ell independent gadget weights), and validated against EP-CBS, BatchCBoot, newer Decoupled TFHE-type functional and Descent-PBS.
- EUROCRYPT 2024 original reports its conversion only 3% of *its own* CBS; even free elimination gives max `1/(1-0.03)=1.03093×` total, whereas RevHomTrace HP-LHE INT_LHE_256 δ8 τ2 conversion is 31.26%, upper ceiling1.455×. **Different applications and source hardware**; do NOT transfer either limit across. This makes original EP-CBS a poor latency target, though high-precision mode may have more room. This is an additional value gate, not the primary falsifier.

**DECISION: PARK source-shaped naive fixed-spaced test-poly + single partial trace.** No novel protocol or measurable gain. If the PI later requests re-entry, allow ONE genuinely different candidate with a typed, provable accumulator permutation or multi-output scheme-switch whose cost is demonstrably lower than `ell·logN` full traces at **same high-precision HP-LHE workload**, and confirm closest source papers first. Otherwise pivot P0 to a different true end-to-end bottleneck. Do not loop additional spacing toy variants.

## End of iteration

`STATUS=FAIL_FREE_SHARED_TRACE / PRIOR_ART_OLD_RELATIVE_TRACE`
`RESULT=EXACT_MULTI_LUT_COLLISION / CROSS_SYSTEM_HEADROOM_DISTINCTION`
`EVIDENCE=FULL_SOURCE_2024_323_AND_2025_1088 + BATCHBOOT_AUTHOR_PDF + EXACT_ENUMERATION`
`NOVELTY=NOT_ESTABLISHED; NO_NEW_CONSTRUCTION`
`NEXT_TEST=PROBLEM_FIRST_OTHER_FHE_OR_PAID_REPACK_COST_WITH_NEW_INVARIANT_ONLY`
`CODEX=NOT_RUN; STATE_UPDATE=THIS_FINDING_ONLY`
