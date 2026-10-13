# I172 — Pinned independent Poulpy SHIP stores full rank-1 selector ciphertexts (no key-layout sharing in inspected path)

**Date:** 2026-10-13. PI approved by “好的，请继续”. ONE primary source/code gate: whether a real independently implemented SHIP already compresses or shares away the `4hθ` raw selector ciphertext layout estimated conditionally from the original paper in I171. Not an attempt to reproduce HEaaN, actual author benchmark or byte size.

## Read-before-write / source provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I171 blob `c22f5e97d45498f212251c4d8dd0a71b8cb527bf`, and `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md`. The authors' primary source SHIP ePrint **2025/784**, complete 33 physical page Research MCP GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official version status VERSION_UNVERIFIED, §3.3 and §4.4. Source describes four masked selectors per candidate/secret support, and explicitly notes an algebraic four-mask relationship. The exact author HEaaN implementation and original key sizes remain **not inspected**.

Public independently maintained Poulpy SHIP implementation, documentation `https://www.poulpy.dev/docs/ship/`, explicitly credits source SHIP. GitHub repository `poulpy-fhe/poulpy`, default `main`, pinned commit **`250d4392656cd313f92ca66d96d8865702d39ddf`** (2026-10-11). All references below from GitHub connector pinned SHA, not page snippets.

| File (at pinned commit) | Exact blob SHA | Relevant lines |
|--|--|--|
| `poulpy-ckks/src/layouts/ship/keyset.rs` | `8be6ab92846168330100efeabe9fa19dbd9720e4` | 106–120, 225–310, 467–568, 574–615 |
| `poulpy-ckks/src/layouts/ship/plan.rs` | `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2` | 131–161 |
| `poulpy-ckks/src/encoding/ship/masks.rs` | `2754eafd1ad24c1eca1382204d37005449f88cca` | 9–29, 41–77 |
| `poulpy-ckks/src/reference/ship/masking.rs` | `91ba98e08ea7172b34c492d9fcc69ef18628820d` | 24–38, 58–111 |
| `poulpy-ckks/src/reference/ship/bootstrap.rs` | `edbec7d8ad60493d53aa5c11c842da1f30cff542` | 174–192 |
| `poulpy-ckks/src/test_suite/ship.rs` | `a5e89638c430886e57c036e001093827293bfae0` | 45–63, 409–450 |
| `poulpy-core/src/layouts/glwe.rs` | `d437d5b1eaa456f2e8c108920c88391b195082b6` | 316–359 |
| `poulpy-hal/src/layouts/vec_znx.rs` | (read at same pinned commit) | `VecZnx::bytes_of` expression `n*cols*limbs*size_of::<W>()` |
| `poulpy-core/src/layouts/compressed/glwe.rs` | `19654f6adbbfeb6312e59ed33a03175c89ca468f` | 25–36, separate `GLWECompressed` with PRNG seed |

## Primary hypothesis — ONE

**HYPOTHESIS:** The *actual* Poulpy SHIP key-generation / key-preparation source employs selector sharing, seeded GLWE compression or some equivalently compact store so that `4hθ` separately encrypted full rank-1 selector objects **do not** remain resident/prepared. If true the I171 full-key count would not reflect a real SHIP implementation layout.

**FALSIFIER:** At one pinned code revision, trace `ship_mask_slot_vectors → ShipKeySet::generate → ShipKeySet::validate_material → ShipKeySet::prepare → bootstrap mask use`; see if all 4θ per support are independently `CKKSCiphertext` and become 4θ separately prepared convolution operands; inspect required k/modulus-limb and GLWE bytes accounting. A separate generic compression API is insufficient unless called in this SHIP path.

## Exact code findings

1. **[FACT: encrypted-key objects/count]** `ShipIndexKeys` stores `masks: Vec<CKKSCiphertext<D,W,Standard>>`; `masks2` optional complex half. For each support slot of h nonzero sparse-secret coefficients, `ShipKeySet::generate` iterates exactly the `ship_mask_slot_vectors(plan,...)` of length **4θ** and on **each** vector creates a plaintext then `module.ckks_ciphertext_alloc(base2k,kk)` and `module.ckks_encrypt_sk`, with independent calls passing key-encryption random streams `source_xe/source_xa`. Key `validate_material` enforces `index_keys.len()==h`, each `masks.len()==4θ`, `masks2.len()==4θ` if complex, else0. Thus **real SHIP =4hθ full ciphertexts**, and **complex SHIP=8hθ** before preparation at this commit. No four-mask relationship-based reduction or seeded GLWE allocation occurs in this inspected keygen path.
2. **[FACT: preparation/evaluation]** `ShipKeySet::prepare` iterates every ciphertext in every mask vector and allocates an individual `CnvPVecL` with `module.cnv_pvec_left_alloc(n,2,mask_size,PrepareHint::Reuse)`, then calls `cnv_prepare_left`; it does not aggregate keys via shared sum relation. The result `ShipKeysPrepared` stores a full `Vec<CnvPVecL>` per slot/half. `bootstrap.rs` uses `ik.masks()`/ `ik.masks2()` and `ship_masking_accumulate` consumes all `4θ` convolution operands. Prepared buffers have backend-specific size; **do not assert exactly 2× the raw bytes or a measured peak-memory figure**.
3. **[FACT: actual key precision/layout]** `ShipPlan::raised_k(base2k)=roundUp_{base2k}((tree_depth+2)*log_delta_work+log_budget_out)`, `tree_depth=ceil(log2(h+1))`; `kk` is calculated in generator and all selector ciphertexts are allocated at rank1 and full width `kk`. `CKKSCiphertext` wraps normal `GLWE`, whose rank1 ciphertext stores body+one mask (2 polys). `GLWE::bytes_of` delegates to `VecZnx::bytes_of(n,rank+1,ceil(kk/base2k))`; latter is `n*cols*limbs*sizeof(W)`. Therefore **unprepared selector coefficient-buffer bytes** are exactly:
```
 S_masks = 4hθ · 2N · ceil(raised_k(base2k)/base2k) · size_of(W);
 raised_k = base2k * ceil(((ceil(log2(h+1))+2)*log_delta_work+log_budget_out)/base2k).
```
Does not include heap Vec, metadata, mux/conjugation/tensor/encapsulation keys, DFT-prepared masks, scratch and any allocator overhead. This is **Poulpy torus-limb backend**, not paper's RNS prime-limb table, so **I171 LL14/HT15 20.5859GiB RNS figure cannot be directly imported**.
4. **[FACT: compaction distinction]** Repository separately implements seeded `GLWECompressed` (stores one body and seed for mask regeneration), but the inspected `ShipKeySet::generate` stores `CKKSCiphertext`, not this type, and `ShipKeySet::prepare` converts each full ciphertext to a full prepared operand. Therefore compressed GLWE's existence does **not** demonstrate SHIP use of compression. No key-level algebraic mask relation savings implemented in the inspected construction.
5. **[FACT: encoded selector zero structure; not a separate test]** `ship_mask_slot_vectors` loops over θ candidate c, sets the public plaintext vector to ZERO when `c ≠ u % θ`, and uses up to two nonzero band mask vectors for the matching candidate determined by secret sign. At most **2 out of 4θ plaintext mask messages per support slot** can be nonzero; HOWEVER **all 4θ independently randomized ciphertexts are still encrypted and stored** to keep the encrypted choice secret. Replacing zero-message encryptions by publicly recognizable zero ciphertexts would reveal the secret candidate/sign and is NOT a safe compression method. This security observation is a structural warning, NOT a proven cryptographic lower bound.
6. **[DERIVED ILLUSTRATIVE, NOT DEPLOYMENT MEASURE]** One plausible SHIP plan shape `h=32, θ=4, base2k=52, log_delta_work=40, log_budget_out=104, size_of(W)=8` gives tree_depth **6** (`ceil(log2(33))=6`), raised `kk=468` bits and **9 torus limbs**, 512 selector ciphertexts. Coefficient-buffer sizes N8192 **0.5625GiB**, N16384 **1.125GiB**, N32768 **2.25GiB**; corresponding *complex* mask halves double these numbers. These are **parameter-conditioned source-layout calculations** from verified allocation formula, NOT measured Poulpy configs/HEaaN benchmark or true memory allocation. Code test-plan uses `h32, θ4, log_delta_work=min(actual CKKS scale,40), budget=2*base2k`, consistent with illustration only where parameter values match.

## Verdict and value

**STATUS: FAIL** source-key-layout **already shares/seed-compresses away 4hθ full selectors** hypothesis **for the pinned independent Poulpy implementation**. **PASS** exactly 4hθ full rank1 CKKSCiphertexts (real), 8hθ (complex), explicit `raised_k` torus-limb sizing and 4θ prepared operands per secret support slot. **UNCLEAR** original author's HEaaN actual memory, total peak RAM, actual error and latency, and whether replacing the current layout can create a novel/source-secure compression.

Source research caveat: The published SHIP paper already discusses four-mask memory relation and extant seeded compression is known; hence it would be incorrect to claim novelty from merely noticing zeros or halving ciphertext storage with a PRNG. There IS a validated key-material bottleneck in this *independent implementation*, but so far NO new algorithm, measured memory, proof of memory lower bound or actual FHE speedup.

## End of Iteration 172

**STATUS:** **PASS key-layout source verification / FAIL “already compresses all selectors” claim in pinned Poulpy / UNCLEAR author HEaaN storage & original method gap.**
**RESULT:** Exact pinned Poulpy code carries `h × 4θ` full rank1 selector CKKS ciphertexts, and prepares each individually to `CnvPVecL` at k_raised; formula above. Zero plaintext sparsity **cannot be naively exposed**. Illustrative N16384 ~1.125GiB and N32768 ~2.25GiB raw masks for h32 θ4, 52bit limbs/9 limbs; not physical benchmarks. Does not resolve HEaaN.
**NEXT_ACTION:** **I173 only with PI continue:** ONE **nontrivial** source-code compression-value gate, compare exact **Poulpy current full mask storage** vs an explicitly safe, source-valid **seeded-encryption-only** alternative: estimate exact payload reduction and *online preparation/reconstruction memory/time costs*, check whether such seeded saving is already generic prior-art and **not novelty**; if no more substantial independent memory/latency frontier, PARK the SHIP mask-storage paper direction and pivot. Alternatively, require one algebraic relation that reduces both serialized+prepared mask arrays **without leaking selector index or sign** and without extra online expensive operations; do not claim this exists without proof. Do not mix third-party Poulpy with author HEaaN. No arbitrary θ table sweeps.
**STATE_UPDATE:** YES — real independent source evidence materially confirms key-object count and contradicts “already compacted” alternative, with exact parameterized byte sizing and no claims of author implementation.
