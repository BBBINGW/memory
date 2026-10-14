# I198 — SHIP complex-paired selectors: pinned IFMA prepared-memory / online-operation gate

Date: 2026-10-14 (Asia/Tokyo). Human PI authorized "好的，请继续" following explicitly numbered I197. This is **I198**, continuing the **independent SHIP prepared-key memory** target, NOT global concurrent vFHE work. Do NOT alter or repeat the vFHE I194–I196 findings. No third-party code modified.

## Read-before-write and source provenance

- GitHub Notes: `STATE.md` (at read SHA `fe796ef9aa9a193415db8575dfb04cf885491856`) belongs to the independent **vFHE** session I196; do **not** overwrite it.
- SHIP independent state `findings/ship-memory-STATE.md` (read SHA `f4c70d60e7cd43ce7caa515a3d1bdb1d48a27adf`) has M04 completed, and M05 implementation/memory gate next.
- I197 `findings/ship-memory-early-galois-guard-envelope-iteration197.md` (SHA `8704aca92791e25cef68abad940580b92c8c2b96`) contains a related, narrower ideal-noise screen. SHIP-M04 (source GGLWE sample/noise screen) was **also** archived before this test: `findings/ship-memory-M04-source-gadget-noise-bound.md`. Thus do not repeat the guarded-Galois-noise analysis.
- Earlier SHIP mask key layout source check I172, seeded-storage-vs-prepared gate I173, complex-pair identity M01, source-level key modulus M02, toy M03 read as relevant.
- Original paper Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784 §3.3, §4.4 (prior cached 33pp mirror version parity unverified). Source below is from independent **Poulpy, not author HEaaN**, GitHub repo `poulpy-fhe/poulpy` pinned **`250d4392656cd313f92ca66d96d8865702d39ddf`**.

Pinned source files inspected directly using connected GitHub:
1. `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: real SHIP has `h*4theta` selector ciphertexts; `prepare_masks` allocates **one** `CnvPVecL(N,2,L,Reuse)` for **each**. Complex SHIP has a separate omega2 half; the I198 calculation treats real SHIP only.
2. `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`, lines 23–143: each masking leaf accumulates all **4theta** Ct×Pt convolution terms, then calls **one IDFT per ciphertext column (two columns total)** and normalizes.
3. `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`, masking loop 182–193, real root conjugation after product tree: **h** masking leaves and **one existing final conjugation** for real mode.
4. `poulpy-ckks/src/layouts/ship/plan.rs`: `raised_k = ceil_to_base2k(((ceil(log2(h+1))+2)*ld)+budget_out)`.
5. `poulpy-hal/src/layouts/module.rs`, default prepared-byte formula `N*cols*size*sizeof(DftWord)`.
6. `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs`, IFMA `CnvPVecL` override near lines 203–208: `bytes = N*cols*size*2*sizeof(u64)`, i.e. **16 bytes** per prepared coefficient/limb entry; it declares `DftWord=Q126Scalar` (lines ~76–80). This is **one named backend**, not a universal backend byte size.
7. `poulpy-ckks/src/reference/conjugate.rs` and core `reference/automorphism/glwe.rs` show each new early conjugation performs an actual GGLWE key-switch and an automorphism; it is not plaintext free-conjugation.

## ONE primary hypothesis and ONE source-layout falsification gate

**H198 [HYPOTHESIS, narrow]:** Under ONE fixed source-shaped real-SHIP plan and ONE explicitly selected IFMA backend layout, complex-paired real selector ciphertexts can cut resident `CnvPVecL` selector **payload bytes by half**, but do **not** cut the number of mask Ct×Pt convolution terms; instead they necessarily introduce an additional per-leaf IDFT/normalization path and an early Galois key-switch. This is a **memory/latency tradeoff**, not an online speedup theorem or claim about full peak RAM.

**Cheapest test:** Read the pinned `keyset.rs` prepared allocator, IFMA exact prepared-byte override, `masking.rs` accumulator loops, and `bootstrap.rs` leaf/conjugation placement. Instantiate exactly `N=16384,h=32,theta=4,base2k=52,ld=40,budget_out=104`. A mismatch in prepared object count, prepared layout width or Ct×Pt term count would falsify the narrow claim. No parameter sweep or synthetic runtime proxy.

## Source-layout results [DERIVED, EXACT integer arithmetic conditional on candidate implementation]

`tree_depth=6, raised_k=468, L=ceil(468/52)=9`, masking output `k_mask=428`.

Real source baseline has `M_old=4h*theta=512` independently prepared rank-1 selector ciphertexts. The M01 *candidate*, if implemented with same-width complex packed selectors, requires `M_new=2h*theta=256` such objects; it is **not** present in upstream code.

The backend IFMA payload of one selector prepared as `CnvPVecL(N,2,L,Reuse)` is:
`N*2*L*(2*8) = 16384*2*9*16=4,718,592 bytes = 4.5 MiB`.

Therefore:
- **Baseline prepared selector payload:** `512*4,718,592 = 2,415,919,104 bytes = 2.25 GiB`.
- **Candidate prepared selector payload:** `256*4,718,592 = 1,207,959,552 bytes = 1.125 GiB`.
- **Conditional selector-prepared payload saving:** exactly `1.125 GiB` (50%). This excludes other evaluation keys, raw keys held concurrently, heaps/allocator overhead, work buffers, and peak process resident memory.
- For comparison, full **raw coefficient payload** (9 limbs, one `i64` word for each of 2 ciphertext polys) changes `1.125 GiB -> 0.5625 GiB`; this is different from DFT-prepared memory, and the generic seeded-GLWE storage trick I173 only saves raw serialized memory, not prepared operand count.
- One extra live rank-1 ciphertext at masking width `k_mask=428` contains `2*N*ceil(428/52)*8=2,359,296 bytes=2.25 MiB` of raw coefficients (one illustrative buffer, NOT a complete scratch or peak RAM bound). Sequential scheduling might reuse some scratch; source has not implemented either schedule.

**Unavoidable candidate operation-count consequence of the M01 reconstruction algorithm**:
- Source baseline `h*(4theta)=512` prepared left × public right Ct×Pt terms.
- Candidate uses **two** separate sums (U,V) with `2theta` terms each per leaf, hence `h*2*(2theta)=512` Ct×Pt terms: **no multiplication-term reduction**.
- Baseline `2h=64` per-column IDFT/normalization operations in masking. Candidate needs `2*2h=128`: **+64 per-column IDFT/normalization operations**.
- Candidate requires `h=32` **additional early `p=-1` automorphism / Galois key switches** at `k_mask=428`, before mux/product tree. Source baseline already performs one final root conjugation in real SHIP; that existing final operation remains.
- No wall-clock speed ratio follows from call counts; a fused/parallel backend may schedule differently. A source shape may admit additional optimizations not considered here.

**Candidate is a conditional code rewrite, NOT tested CKKS ciphertext functionality**. The earlier M01 ideal slot identity and M03 toy do not establish a compiled IFMA implementation. Security/precision/actual peak RAM and public-operand re-encoding are unresolved. The prepared memory savings formula is a conditional *payload allocation* estimate, **not** a measured process RSS or source-author HEaaN benchmark.

## Environment block and exact verification

Attempted runtime availability gate in this execution environment:
- `cargo`: absent; `rustc`: absent.
- No pinned Poulpy compiled library/checkout available.
- DNS resolution for GitHub and crates.io unavailable to local container. GitHub connector can inspect source but cannot compile/execute code.

Therefore I197's desired **real same-plan encrypt/decrypt/error/timing benchmark** was NOT run. Do not assert FHE quality, actual runtime, or benchmark gains. In accordance with independent SHIP state M04 / AGENT.md, this round uses the source-grounded byte/operation arithmetic and then stops.

Local reproducible arithmetic:
- `/mnt/data/ship_i198_prepared_memory_cost_gate.py`, SHA256 `25ee203079a89a54e63b15a8d8e35b1a9c6013968938f443ba31d6b818ad1fc1`.
- `/mnt/data/ship_i198_prepared_memory_cost_results.json`, SHA256 `9d96092c92f77d49c9400ad97d07710b2614238085c7c9b60fd0763e45a9837b`.
These are **local**, not accessible through Research MCP. Arithmetic was executed successfully.

## Verdict / End of I198

**STATUS: PASS** the narrow IFMA source-layout selector-payload reduction + source call-graph extra-work claim, **UNCLEAR / IMPLEMENTATION BLOCKED** actual compiled CKKS masking-leaf equality, per-slot precision, wall-clock and true peak resident memory. **NOVELTY NOT VERIFIED**.

**RESULT:** For the source-shaped real SHIP plan, 512→256 `CnvPVecL` selector objects is conditionally a **2.25→1.125 GiB prepared-mask payload** saving on IFMA (exact layout arithmetic, not runtime), but the specific pairing formula retains all **512 mask Ct×Pt terms**, doubles IDFT/normalization paths (**64→128 column operations**) and adds **32 high-precision early Galois switches**. The promising axis is memory-constrained Pareto improvement, **not** free speedup. Cannot decide if the expensive online work overwhelms the memory benefit until a true compiled implementation is run.

**NEXT_ACTION (one executable action, subject to PI continue):** Provide/obtain an executable pinned Poulpy Rust environment, then implement ONE `N=16384,h=32,theta=4` **real** masking-leaf paired-vs-baseline test using the existing `ship_masking_accumulate`, `ckks_conjugate_into` and pinned IFMA backend. Record SAME-plan prepared `CnvPVecL` bytes, max decrypted slot errors, wall-clock for masking + early conjugation, and peak bytes. If a real executable runner remains unavailable, request HUMAN_REVIEW to PARK or retain the memory-only candidate; do **not** repeat a third abstract Gaussian or another toy timing run.

**STATE_UPDATE: YES to this independent I198 archived finding only. NO to global `STATE.md` (belongs to concurrent vFHE session).**
