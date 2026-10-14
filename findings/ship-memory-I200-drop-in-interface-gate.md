# I200 — SHIP complex-packed selectors cannot be a drop-in keyset replacement

**Date:** 2026-10-14 (Asia/Tokyo). PI continuation after I199. **Independent SHIP research numbering only**, not legacy general-FHE I counter and not the separate vFHE V-series.

## Read-before-write / scope

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, independent `findings/ship-memory-STATE.md` SHA `28bbf48b318d3cd4495e6dee7de7a10d58670eff`, `findings/ship-memory-ifma-runner-availability-gate-iteration199.md` and previous I198 source-cost result.
- `STATE.md` is the concurrently updated **vFHE V-series** state (SHA `4efa09926b695956e1618906f434eec16c883f94` on read). No writes to it.
- [FACT: environment check on I200] `uname -m = x86_64`, `avx512f/avx512ifma/avx512vl` flags present; no `rustc`/`cargo`, no Poulpy checkout in `/mnt/data`, and `getent hosts github.com` and `getent hosts index.crates.io` produce no addresses. The connected GitHub tools retrieve source but do not offer a directly executable command runner or general workflow dispatch.
- [FACT: original target] *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, Cheon–Hanrot–Kim–Stehlé, EUROCRYPT 2025, ePrint 2025/784. Audit implementation is independent third-party `poulpy-fhe/poulpy` fixed at commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**, not authors' HEaaN.

## ONE primary hypothesis / ONE minimal decisive source test

**H200 [hypothesis to falsify]:** The I198 complex-paired selector candidate is **drop-in compatible** with Poulpy's existing SHIP masking/keyset interfaces: one can merely replace per-support selector arrays of length `4*theta` by complex-packed arrays of length `2*theta` and reuse the currently compiled `ShipKeySet::new/prepare` and `ship_masking_accumulate` unmodified to execute the same operation.

**Minimal decisive test:** Inspect the exact pinned source function entry contracts for `ShipKeySet::new → validate_material`, `bootstrap::ship_bootstrap... → masking loop`, and `masking::ship_masking_accumulate`. Find just one enforced size mismatch or missing two-output computation that refutes no-change drop-in compatibility. No repeated noise model, toy implementation or operation-count sweep.

## Source trace [FACT: pinned code]

1. `poulpy-ckks/src/layouts/ship/keyset.rs` (blob `8be6ab92846168330100efeabe9fa19dbd9720e4`), around lines 576–615: `validate_material` sets `mask_count=4*plan.theta()`; for each support `ensure!(ik.masks.len() == mask_count)`, and complex half `masks2` must also be `mask_count` if enabled. A candidate length `2*theta` is explicitly rejected. `ShipKeySet::generate`, around lines 488–532, creates one independently encrypted CKKS ciphertext for each of the original `4*theta` vectors; it does not generate packed pairs.
2. `poulpy-ckks/src/reference/ship/bootstrap.rs` (blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`), lines ~182–192: `pi.len()==4*theta` checked; then exactly one `ship_masking_accumulate(...,masks,pi,...)` for each leaf/half, followed immediately by mux rotations. Original public `pi` array is **not** split into the two different transformed operand arrays required by complex pairing.
3. `poulpy-ckks/src/reference/ship/masking.rs` (blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`), lines ~44–143: `ensure!(!masks.is_empty() && masks.len()==pis.len())`; one DFT sum ciphertext is accumulated using the current plaintext operand array and one IDFT+normalization per ciphertext column. Therefore simply substituting a length-`2*theta` selector array while passing the unmodified length-`4*theta` `pi` causes an error even if keyset validation is bypassed.
4. `poulpy-ckks/src/reference/ship/mod.rs` (blob `6bec93d73b3ae4ef09505609463d03f6449256dd`) marks `masking` and `bootstrap` `pub(crate)`; the masking implementation itself is `pub(crate) fn ship_masking_accumulate`. The `ShipIndexKeys` and `ShipIndexKeysPrepared` fields are also `pub(crate)` in `keyset.rs`. An **external** benchmark crate cannot directly replace those fields or call that kernel through its normal public API. A feature-gated in-crate test or a small controlled public/test-only adapter is needed to benchmark the exact source kernel, though high-level CKKS arithmetic APIs could implement a different stand-alone comparison.

## Derived technical consequence

For **two real masks** `M1,M2` and **two public slot operands** `P1,P2`, existing M01's exact identity is
`C=Enc(M1+i M2), U=C(P1-iP2), V=C(conj(P1)-i conj(P2)), F=(U+Conj(V))/2`.

Unlike a single source `sum_j mask_j*pi_j` call, the candidate needs:
- generation and preparation of `2*theta` packed selector ciphertexts per support (not plain compression of arbitrary already encrypted individual ciphertexts);
- formation of **two different** derived public-plaintext operand arrays for U,V, each length `2*theta`, with correct CKKS encoding/scale and conjugation handling;
- **two** masking accumulations and then **one real Galois-conjugation key switch** plus averaging for each leaf before the existing mux steps;
- modifications to keyset count validation/representation and runtime orchestration, ideally in a minimal feature-gated internal test rather than a broad public API rewrite.

These are an **interface/computation dependency** for this specific candidate, not a cryptographic impossibility theorem. All prior I198 conditional 512→256 prepared objects and extra cost remain **unmeasured**; neither this source inspection nor I197/SHIP-M04 proves real error/latency/memory behavior.

## End of iteration

**STATUS:** **FAIL H200 drop-in-compatible replacement** (decisive source checks); **UNCLEAR / IMPLEMENTATION BLOCKED** for real compiled matched baseline-versus-packed masking-leaf FHE experiment. **NOVELTY NOT VERIFIED**.

**RESULT:** Two independent concrete code-level mismatches force a dual-accumulator masking implementation; third-party Poulpy original keyset validator enforces `4*theta` masks, source bootstrap enforces `4*theta` public plaintext operands, and single-accumulator kernel enforces matched lengths. An external crate cannot directly call crate-private masking internals. Native ISA is present, but there is no compiler/source checkout or connected executable runner. Nothing has been compiled or benchmarked.

**NEXT_ACTION (requires actual executable environment, no more toy screens):** In a reachable pinned Poulpy checkout with Rust `nightly-2026-05-14`, create ONE isolated **in-crate test-only dual-accumulator masking leaf** with `2*theta` complex packed keys and matched U,V derived public operands; run it against original single-leaf baseline under the same secret/parameters at `N=16384,h=32,theta=4,ld=40`; record decryption max-slot error, per-leaf runtime incl. actual high-precision Galois key switch, prepared selector bytes and peak live buffers. Do not change upstream/default keyset APIs or claim a performance improvement until actual code passes. If connected execution remains unavailable, HUMAN_REVIEW before further iterations.

**STATE_UPDATE:** YES in independent `findings/ship-memory-STATE.md` only; NO in global vFHE `STATE.md`.
