# SHIP-M01 — Complex-paired encrypted selector masks: algebraic prepared-key compression gate

**Date:** 2026-10-14.
**Independent SHIP research sequence:** SHIP-M01, **NOT** global FHE iteration I194, and **NOT** a continuation/extension of vFHE I193.
**PI instruction:** Focus on SHIP evaluation-key **resident prepared memory**, seek transfer techniques and mathematics, record each SHIP round in its own file, keep the vFHE I193 archive intact.
**Status:** PASS scoped slot-level algebraic identity and conditional prepared-selector-count calculation; UNCLEAR CKKS circuit/noise/latency/safety/novelty. No authors contacted or publication/security claims.

## Research target and read-before-write

Cheon, Hanrot, Kim, Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, https://eprint.iacr.org/2025/784, especially §3.3 Lemma 1 / Eq.(4), §4.1 Eq.(6), §4.4 Eq.(7)/(8)/Algorithm 4, pp16–22 (physical PDF).
Research MCP 33pp github-mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, **VERSION_UNVERIFIED**. MCP plain text may misparse symbols; separate web PDF screenshot attempts failed cache miss; validate against visual original before implementing.
Prior internal findings read before this test:
- `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md` — 4hθ conditional ciphertext count and tabulated LL14/HT15 maximal-PQ memory envelopes.
- `findings/ship-poulpy-real-key-layout-selector-compression-gate-iteration172.md` — pinned Poulpy stores / prepares all real masks.
- `findings/ship-seeded-glwe-storage-vs-prepared-keys-gate-iteration173.md` — generic ~50% persisted GLWE seed does NOT halve eager prepared operands.
- `findings/ship-hybrid-four-mask-sum-onehot-affine-obstruction-iteration174.md` — hybrid per-candidate sum of four masks is secret onehot, not public one, preventing free per-column one-of-four deletion.
- `findings/OPEN_RESEARCH_BRANCHES.md` as historical index only. `STATE.md` was vFHE I193 at start; not a SHIP research source.

**Source code, distinct from author HEaaN:** `poulpy-fhe/poulpy` GitHub pinned commit `250d4392656cd313f92ca66d96d8865702d39ddf` (2026-10-11):
- `poulpy-ckks/src/encoding/ship/masks.rs` blob `2754eafd1ad24c1eca1382204d37005449f88cca`: `ship_pre_rotated_masks`, `ship_pre_rotated_masks_omega2`, `ship_mask_slot_vectors` generate source-shaped 4θ **real-valued** mask vectors per support.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: all 4θ ciphertext masks stored separately; `prepare` maps each to a 2-column `CnvPVecL`. `generate` uses `ckks_encode_reim_into` with zero imaginary part, `ckks_encrypt_sk` under **dense key**. A **dense-key conjugation automorphism key** is already generated/prepared at `gal_el=-1`, BUT usable modulus/level and stage remain unverified.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`: masking accumulator is a linear `sum masks[i] * pis[i]` of prepared left convolution operands and public plaintext right operands; original evaluator uses one DFT-domain sum, one IDFT/normalization per accumulator.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: one masking accumulation for each sparse support and each real/complex half, then mux rotations, then product tree.
These code facts do NOT measure author HEaaN memory or performance.

## Technique-transfer landscape (discovery, not multiple active hypotheses)

- [FACT/KNOWN] CKKS *complexification* packs two real values in real/imaginary slot coordinates and extracts with conjugation. A May 2026 public Google HEIR discussion explicitly cites **Thor, Powerformer, Tricycle**, https://github.com/google/heir/issues/2930, and identifies conjugation as a **key-switching** operation. This is known; do NOT claim complex packing novel.
- [FACT/KNOWN] OpenFHE `simple-complex-numbers.cpp` explicitly generates a conjugation automorphism key, https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/simple-complex-numbers.cpp.
- [TRANSFER-ONLY] TFHE YATA (TCHES 2026, Matsuoka/Sato, DOI 10.46586/tches.v2026.i1.325-352) and a 2025 TFHE-like 30× key-size paper (DOI 10.1049/ise2/7097351) motivate key-layout/online-scheduling redesign, but neither provides a drop-in SHIP selector compression proof. LCR+AKS for CKKS rotations reports reduced rotation-key bytes (PKC 2026, ePrint 2025/1403); those are **different key types**.
- [NOVELTY] No directly matching exact SHIP complex-paired selector rewrite established in limited search. **NOVELTY NOT VERIFIED**. The algebra is an elementary real/imaginary packing identity; it is not by itself a contribution.

## Exactly ONE primary hypothesis

[HYPOTHESIS] In source-form SHIP's **plaintext-linear masked-sum** subroutine, group the 4θ original **real-valued** encrypted masks into 2θ **complex-packed** encrypted masks. Without any ciphertext-ciphertext multiplication or additional ciphertext-plaintext multiplication terms, reconstruct the same masked sum using ONE ciphertext conjugation per full masking accumulator, rather than per pair. This should halve the **number of resident prepared mask ciphertext operands** (conditional on a backend supporting complex-packed selector masks with unchanged rank/limb width).

[DECISIVE MINIMAL TEST] Use exactly the pinned source's Boolean mask generator, including secret position j, sign, u mod θ, rotations and optional omega2 half. For arbitrary complex PUBLIC operands P, compare original `Σ M_k P_k` with the paired formula slot by slot. Count stored ciphertext operands and additional conjugation/accumulator operations. A single source-legal mismatch would KILL the proposed algebraic rewrite. Do NOT attempt full CKKS benchmarks, privacy proof or new other hypotheses in this round.

## Construction and mathematical proof — ideal CKKS slot semantics

For **ANY** real-valued masks M1,M2 and arbitrary public complex plaintext vectors P1,P2, encrypt **one complex mask**
`C = Enc(M1 + i M2)` instead of independent `Enc(M1)`, `Enc(M2)`.

Under decryption (ignore approximation errors temporarily), let
```
U = C · (P1 - i P2)
V = C · (conj(P1) - i conj(P2)).
```
Then
```
(U + conj(V))/2
= ((M1+iM2)(P1-iP2)+(M1-iM2)(P1+iP2))/2
= M1 P1 + M2 P2.
```
This identity is **real-linear but not complex-linear** in C; the complex conjugation is ESSENTIAL. It remains true for input masks depending on SECRET j/sign (unlike the naive public-sign-state factorization ruled out by I174). The keygen knows each mask and encrypts the complex combination; evaluator needs no secret index/sign.

Now pair k=(1,2),(3,4) for every candidate c. With one ciphertext C_(c,t) per pair and public P_(c,k), aggregate
```
U_total = Σ_(c,t) C_(c,t) * (P_(c,2t-1) - i P_(c,2t))
V_total = Σ_(c,t) C_(c,t) * (conj(P_(c,2t-1)) - i conj(P_(c,2t))).
F = (U_total + Conj(V_total))/2.
```
**ONE Conj per entire masked accumulator**, NOT per mask pair. Must perform a proper ciphertext Galois automorphism + key switching to return to same secret; plaintext complex conjugation alone is not a homomorphic implementation.

Only the *real masks* are paired: SHIP's optional distinct omega2 half is handled analogously with its own 2θ packed keys; do not conflate `masks2` with imaginary coordinate packing.

## One executed deterministic test

Script: `/mnt/data/ship_m01_complex_pair_toy.py` **LOCAL ONLY** SHA256 `ae932f5b7a6b9fef7c37d19c847a4832566029a1582cb97db0f7d661e0576af8`.
Faithfully translates pinned Rust `ship_pre_rotated_masks`, `ship_pre_rotated_masks_omega2`, `ship_mask_slot_vectors`.
Parameters: m=8, θ=4, public p=3. Exhaustive j∈[0,15], s∈{−1,+1}, u0∈[0,3], omega2∈{false,true} = **256** secret/half configurations × 8 slots = **2048** checks. Public P[c,k] are distinct deterministic complex values, including independently varying real/imaginary parts and c,k,j,x dependence. Source-style partition-of-unity verified for each case.
```
cases = 256
slot_comparisons = 2048
max_rounding_residual = 2.2887833992611187e-16
old_selector_count_per_support = 4 θ = 16
new_selector_count_per_support = 2 θ = 8
extra_ctpt_mul_terms = 0
extra_ciphertext_conjugations = 1 per masked accumulator
```
**PASS** exact algebra up to deterministic floating rounding. The code is NOT an FHE execution or a noise/security/latency benchmark.

## Storage and online cost (separated carefully)

[DERIVED, CONDITIONAL on same rank-1/limb/modulus precision]
- Stored + individually prepared selector ciphertexts per support, per output half: **4θ → 2θ (50% reduction)**. For h=31: LL14 θ9 original 1116 →558, HT15 θ17 original 2108 →1054; a complex SHIP implementation with a distinct omega2 half doubles both counts before/after.
- Reinterpreting I171 literal full-PQ **bit-packed raw selector envelopes** only (NOT measured): LL14 1.8604 GiB→~0.9302 GiB, HT15 14.1689 GiB→~7.0845 GiB. Original HEaaN memory and levels unverified; these are not performance claims.
- With the I172 illustrative **Poulpy torus-limb** N16384,h32,θ4,9 limbs,W8 source-layout: 512 full masks 1.125 GiB raw→256 packed masks 0.5625 GiB raw, independent of any prepared-backend overhead. Prepared left operands should halve in *count* if they retain same CnvPVecL shape, not necessarily halve total application peak RAM.
- Original 4θ ciphertext-plaintext convolution terms versus new **2×(2θ)=4θ** terms: **same leading term count**, NOT half online work.
- Original ONE masking DFT sum + ONE IDFT/normalize. New TWO masking sums U,V + likely TWO IDFT/normalizes, TWO live accumulators, an encrypted `Conj(V)` key switching and joining/dividing by 2. Approximate plaintext weights P±iQ may be up to 2× in magnitude, affecting precision. The common conjugation can be amortized over 2θ pairs inside **a support**, but the bootstrap has h independent masked leaves: **about h extra conjugations per real output half**, or up to 2h for separate omega2 halves, before tree/mux. Costs are **not** shown latency-neutral.
- Original SHIP uses auxiliary P for a cheap fused column-stage rescale WITHOUT KS. Placing a Galois key switch BEFORE this rescale may clash with that P usage; doing TWO rescaled accumulators then conj at Q might preserve multiplicative depth, but requires a **key-switch noise / scale / modulus** analysis and suitable evaluation key at this precise level. The pinned Poulpy dense-secret conjugation key is a promising EXISTING artifact but not proof that it works at this stage; no actual code modified.
- Security not shown: plaintext mask pack is a deterministic transform of secret-derived masks encrypted under dense key. Need check original secret-/evaluation-key dependence assumptions (potential KDM/circularity), noise correlations and extraction. Using ordinary IND-CPA slogan alone does not discharge all SHIP security obligations.
- Communication/disk cannot be conflated with RAM; *prepared* memory in a modified codepath remains to be verified.

## Verdict and next decisive gate

**STATUS:** PASS **narrow algebraic compression identity/source-compatible mask test**. UNCLEAR practical FHE implementation, key-switch error, runtime, peak memory, novelty.
**RESULT:** Unlike I174's failed cost-free public-affine drop, a **non-complex-linear** packing uses CKKS's real/imaginary channels + ONE global conjugation to combine two private masks per stored ciphertext. This avoids revealing secret support/sign, and in a source-shaped exact toy the original masked result is preserved for all tested inputs. It promises **2× fewer resident selector prepared objects** only if the same-shape packed keys are supported. Potential price: per-support Galois key-switch and twice the accumulator transform path; could erase SHIP's key latency advantage.
**NEXT_ACTION:** **SHIP-M02, only on PI continue:** ONE **source-specific modulus/noise/latency gate** on implementing packed (U,V) in pinned Poulpy: inspect exact conjugation eval-key modulus/precision and `raised_k` vs post-masking `RescaleP` interface; construct *one* minimal real CKKS rank-1 convolution+conjugation test for a pair with nontrivial public complex P1,P2. If the source method cannot conjugate V at the right level without adding a prohibitive large key, level loss, or noise amplification, KILL the packed candidate before large benchmark. If passes, only then benchmark memory/latency. Do not automatically change parent direction.
**STATE_UPDATE:** YES — PI explicitly selected independent SHIP branch, new compact algebraic candidate; leave vFHE I193 provenance intact.
