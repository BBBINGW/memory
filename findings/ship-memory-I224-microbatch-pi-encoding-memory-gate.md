# SHIP I224 — Microbatch input-dependent pi encoding memory is material

**Date:** 2026-10-14 Asia/Tokyo. Independent SHIP evaluation-key-memory follow-up I224 after I223, where PI said continue. Read before write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` (concurrent vFHE V18, READ ONLY), independent `findings/ship-memory-STATE.md` I223 SHA `9bcced79400e2e17b1b1d6f5b65e805345ace1ca`, and `findings/ship-memory-I223-hmux-microbatch-group-reuse-gate.md`. Do not edit unrelated global/vFHE state or upstream code.

**Scientific parent:** Cheon–Hanrot–Kim–Stehlé, SHIP, EUROCRYPT 2025 / ePrint 2025/784. **Code source:** independent third-party Poulpy, NOT authors' HEaaN, PINNED `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`. Numbers refer ONLY to a source-shaped **illustrative N16384** / h32 / theta4 / radix52 / working scale40 / raised k468 / real (one-half) instance, not a validated 128bit secure deployment or process RSS.

## ONE primary hypothesis and ONE minimal decisive test

**H224 [FALSIFIABLE]:** The request-specific coefficient encoding `enc.pi`, omitted from I223's `2.875GiB resident key + 33×2.25MiB leaves per request` simplified payload estimate, consumes enough memory **if eagerly retained for B32 requests** to increase the originally quoted B32 `5.1953125GiB` key+leaf payload by at least **50%**.

**Falsifier:** Trace pinned concrete `ShipCoeffEncodings`, the `ship_coeff_encodings_host` allocations and precision, core plaintext rank/limbs, and `ship_bootstrap_roots` consumer lifetime; compute exact coefficient byte payload with integer arithmetic. Show whether pi really has 32×16 full-degree plaintexts per request and whether the source retains all simultaneously. No synthetic runtime, no folklore estimates, no unrelated second hypothesis.

## Source [FACT]

- `poulpy-ckks/src/layouts/ship/mod.rs` blob `c76c18d6c6e38bd9c9885734e37b11c8b77f758d`: `ShipCoeffEncodings` fields `pt0`, optional `pt0_2`, and `pi: Vec<Vec<CKKSPlaintext<...>>>`. Real case has no `pt0_2`.
- `poulpy-ckks/src/encoding/ship/coeff_enc.rs` blob `e0b5bb3e2cd5bb681a22b1798039061429ba17fe`: host encoder derives public bottom-mask cos/sin phases, sets `k_pi=ld+base2k`, then **for each slot in 0..h**, and `c=0..theta`, produces **four** full-ring `pi` plaintexts each via `encode_reim_pt(... k_pi ...)`. That function calls `module.ckks_pt_vec_alloc` (NOT compact) and returns `ShipCoeffEncodings {pt0,pt0_2,pi}` with all `h×4θ` entries allocated. `pt0` uses k=raised_k and occupies one plaintext polynomial.
- `poulpy-ckks/src/layouts/alloc.rs`: `ckks_pt_vec_alloc` uses full ring degree and `ckks_plaintext_alloc` uses `ceil(k/base2k)` limbs. `poulpy-ckks/src/layouts/plaintext.rs`: plaintext wraps **GLWEPlaintext**, not ciphertext with two columns. `poulpy-core/src/layouts/glwe_plaintext.rs`: `GLWEPlaintextLayout.rank()=0` (one polynomial column), so each plaintext coefficient consumes one i64 word per limb in this backend.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: `let enc = ...coeff_encodings_impl(...)?` creates complete pi table before leaves; later `for(slot,ik)` takes `&enc.pi[slot]` once and calls `ship_masking_accumulate`; no further dependence on prior pi plaintexts or future slots before their use. The original enc variable remains in scope until roots creation. For I223 **B request** microbatch, if the current whole-enc API returns and retains all B sets, all B×512 pi plaintexts must be held.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`: each masking call uses only `pis` for CURRENT support slot, and independently prepares **16 right convolution operands in scratch** before summing. The per-call scratch (e.g. 16×N×2×16 bytes for IFMA DFT prepared-right at pi precision = 8MiB if full N/2 limbs) is ADDITIONAL to resident raw pi, not represented in the table; if B masking calls are sequential, scratch can be reused.
- Source baseline `findings/ship-memory-I223-hmux-microbatch-group-reuse-gate.md`: disk-backed raw group + prepared group + all other prepared keys = **2.875GiB named key residency**, each rank1 ciphertext at k468 N16384 uses 2.25MiB and 33 leaves give 74.25MiB per real bootstrap. This undercounts enc.pi and numerous buffers, explicitly admitted by I223.

## Minimal exact allocation calculation [DERIVATION + EXECUTED]

Use `N=16384,h=32,theta=4,ld=40,base2k=52,raised_k=468`.

- `k_pi=ld+base2k=92 bits`, `pi_limbs=ceil(92/52)=2`.
- **One full-degree pi plaintext = N×1poly×2limbs×8bytes =262,144 bytes =256KiB =0.25MiB.**
- 4θ=16 pi per support; `h×4θ=32×16=512` pi per request.
- **All pi per request =512×0.25MiB=128MiB=0.125GiB**; 32-request microbatch pi alone **4.0GiB**.
- **Only current support slot's pi per request =16×0.25MiB=4MiB**; B32 current-slot pi **128MiB=0.125GiB**. This slot-wise construction is a proposed new API/lifetime policy, not current code. Source cos/sin phases computed globally from public bottom ciphertext are reusable between slot encodings; precisely preserving their arithmetic and encoder state requires refactor and correctness checks.
- Real `pt0` at k468 is another `N×9limbs×8=1.125MiB` per request; excluded from the principal table below, as are input a_sparse, accumulator, pi encode host temp arrays, all scratch, and product-tree overhead.
- Current B32 I223 key+leaf model =2.875+32×74.25/1024=**5.1953125GiB**.
- Add eager pi at B32 =4.0GiB ⇒ **9.1953125GiB**, relative increase **76.992481203%** ⇒ **H224 PASS** threshold ≥50%.
- Add only CURRENT slot pi at B32 =0.125GiB ⇒ **5.3203125GiB** named keys+leaves+one-slot pi, compared with eager version9.195GiB. Again no claim this is peak RAM or a validated integrated implementation.

Table:
| B | keys + leaves (GiB) | + eager ALL pi | + one-slot pi | amort raw HMux disk GiB/request |
|---|---:|---:|---:|---:|
|1|2.947509765625|3.072509765625|2.951416015625|21.09375|
|8|3.455078125|4.455078125|3.486328125|2.63671875|
|32|5.1953125|9.1953125|5.3203125|0.6591796875|
|64|7.515625|15.515625|7.765625|0.32958984375|
|128|12.15625|28.15625|12.65625|0.164794921875|

**Reproducibility:** Executed deterministic Python integer assertions, no Rust runner:
- `/mnt/data/ship_i224_pi_residency_gate.py` SHA256 `bf8f2c870b4afc29a2e8eaa61aa57c61ceb7b73839e47ab1f81a588589b32bee`;
- `/mnt/data/ship_i224_pi_residency_results.json` SHA256 `db237579ee16152164be8909c873ae052defe4174aecfe419c01df559393629f`.

## Scope, safeguards, decision

**STATUS:** **PASS H224** size omission is material (+77% at B32); **PASS** source code allows the mathematical pi for each support to be computed from publicly obtained mask phases without previous slot pi; **UNCLEAR** implementation of slot-lazy encoder, backend numerical identity, staging cost, peak RSS/performance. No compiled changes, correctness tests or throughput measurements. No original-paper correctness issue or 128bit assessment. **NOVELTY NOT VERIFIED**.

**RESULT:** I223’s B32 5.20GiB is undercounted if its batch implementation preserves the current eager `ShipCoeffEncodings` lifetime; the source-shaped named payload estimate becomes 9.195GiB with all pi or 5.320GiB with hypothetical one-slot pi generation. For large B the request-specific encoding allocation becomes dominant; reducing key residency must be co-designed with coefficient-encoding lifetime. Neither remedy reduces total evaluation-key byte size.

**NEXT_ACTION:** Require ONE real pinned Rust IFMA memory profile/benchmark before using these numbers as real peak RSS, with B1/B8/B32 and explicit encoding policy (full `pi` vs slot-lazy) and one source exact numeric-equivalence check on a slot before throughput/latency claims. If no runner, recommend PI **PARK** this systems candidate; no more adjacent static RAM mini-optimizations solely to produce iterations. Original I207 HMux key-sharing security/performance remains independently blocked. Never modify unrelated global vFHE state or upstream code.
**STATE_UPDATE:** YES independent SHIP checkpoint only.
