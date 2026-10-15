# SHIP-I247 — Prepared/NTT-domain onehot scalar-column reconstruction: mathematically feasible, no significant fair resident-memory Pareto

Date: 2026-10-16; PI explicitly said continue; **SHIP track only**, immediately following committed I246. One primary falsifiable claim + one decisive math/source memory test. Do not touch CGS/VFHE/EXPLORE or original authors' 2025/784 security audit (I245 remains SOURCE_BLOCKED).

## Primary technical hypothesis H247 and decisive falsifier

**H247:** Given I246's scalar beta-column key omission, inline reconstructing the missing HMux column **directly in prepared/DFT domain** can (a) preserve the original rank2 VMP semantics without added KSK, and (b) attain at least **5% lower peak named key-buffer memory** than a *like-for-like four-candidate group-staged original*, while not adding material re-preparation, scratch, or online latency. This is a concrete target, not a universal lower bound.

**Cheapest decisive test:** Check pinned source `gglwe_prepare` and IFMA `vmp_prepare_ifma` NTT line/limb transformations and original `ship_mux_rotate` rank2 full-key input contract; construct exact negacyclic NTT (not floating FFT) gadget limb equivalence to test `prepare(T−Σsigma(C)) == prepare(T)−ΣNTT_sigma(prepare(C))` modulo original torus Q; calculate **best-case even with ZERO extra scratch / ZERO added CPU cost** at the same four-key staging memory model. If savings <5% without any extra costs, KILL H247 regardless of actual Rust latency. Do not pretend Python toy is compiled AVX512-IFMA RSS test.

## Primary source facts

- Cheon et al., SHIP EUROCRYPT2025 / ePrint2025/784 §4.2 and §5.1 Algorithm5, author security matched warning I245 still SOURCE_BLOCKED.
- Pinned **independent THIRD PARTY**, not author HEaaN: `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.
  - `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: rank2 HMux input keys encrypt `(beta*s,beta)` into `t_d=sigma_(g_d^-1)(s)`, one-hot beta within each group.
  - `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: original `ship_mux_rotate(module,ct,keys:&[HMuxRotKeyPrepared],plans,scratch)` takes entire prepared group; hoists rank2 input DFT ONCE, loops over candidates doing VMP and final public output automorphism, accumulates one shared DFT sum then IDFT/normalize ONCE. Stock API expects **all complete rank2 keys** in the provided slice; it does NOT implement partial on-demand columns / stream-from-disk.
  - `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b61`: `gglwe_prepare` calls `vmp_prepare` for each standard MatZnx row/col/word layout, creating a VmpPMat with `N*dnum*rank_in*(rank_out+1)*size`.
  - `poulpy-cpu-avx512/src/ntt3x42_ifma/vmp.rs` blob `78f8a8494a46964440a12fa2b4adb2fa248ade45`: `vmp_prepare_ifma` transforms each signed integer limb as triple 42-bit-prime NTT/CRT and packs 3 residues into 16-byte DFT element using SIMD block-major layout; tmp size `6*n*sizeof(u64)`. This is evidence for a linear-per-limb transform, NOT evidence that prepared-key automorphism/add public APIs exist or dynamic range is automatically safe for 3-key differences.
  - Prior I246 `findings/ship-memory-I246-onehot-scalar-column-public-galois-completion.md` blob `901d126386fb38dce06549f8f045255738e196ad`: `C^(beta)_(ell,i)=(0,G_i)-Σ_{d≠ell}σ_(gell^-1*gd)(C^(beta)_(d,i))` in scalar plaintext after secret domain alignment; exact 128/128 full noisy MuxRot toy, reduced 128 scalar prepared columns at rest (12.63% of total prepared), but no demonstrated resident RAM reduction with group streaming. Still requires all original first `beta*s` columns.

## Precise prepared-domain relationship [DERIVATION]

Let `P` apply the prepared ring NTT separately to integer-represented torus limbs (RNS/CRT) of mask/body polynomials. Let `A_r` permute negacyclic NTT evaluations according to `j -> r*(2j+1) mod(2N)`. Then **as an abstract linear CRT transform of integer limbs**:
```
P(C_ell_beta) = P((0,G_i)) - Σ_{d≠ell} A_(gell^-1*gd) P(C_d_beta)
```
where each packed component/limb needs correct CRT and canonicalization semantics. This equality holds as a *represented torus polynomial modulo Q* even when integer limb arrays after subtraction are NONCANONICAL / negative. It does NOT establish safe unmodified IFMA prepared-array byte arithmetic (packed residues, modular reductions, row/col strides), VMP noise/reduction equivalence at finite precision or equal latency.

Using a publicly known trivial `T_i=(mask=0, body=G_i)` does not require a new secret-dependent key. The original complete HMux remains one rank2 VMP per candidate if the missing column is reconstructed, with no additional online KSK. But source `ship_mux_rotate` currently provides no way to splice a per-limb virtual/missing prepared column: **implementing this without a complete 45MiB prepared scalar column requires a new tiled/fused input-output VMP kernel** (not just a call to already present helper methods).

## ONE executed exact NTT experiment [PASS representation semantics]

Executable standard-library Python `/mnt/data/ship_i247_prepared_domain_frontier.py`, SHA256 **825eae9238a539a793eb87dd1bc6673f79645d4f55be397f46df3de07470b62d**. JSON `/mnt/data/ship_i247_prepared_domain_frontier.json` SHA256 **68dd9cd76d2ac94808d59a53f481de8416c15ab3948490170f9147a0bff6b6cb**. Test `R_Q=Z_(2^40)[X]/(X^16+1)`, 5 x 8bit base limbs, NTT over 31-bit prime `p=2013265921` with primitive32nd root, random independent 40bit public ciphertext coefficient words, Galois [1,5,9,13], all 4 gadget values (2^32,2^24,2^16,2^8), mask/body columns, 40 fresh randomized public samples per value.

Exact `NTT^{-1}( P(T)−ΣNTT_automorphism(P(C_d)) )` with signed unnormalized limb recombination modulo original Q **EQUAL** coefficient-domain `T−Σsigma(C_d)` in **320/320** checks (no FFT floating approximation). Some unnormalized reconstructed limb coefficients are negative, and observed max absolute signed reconstructed digit **739** (normal digit range0..255); this flags actual IFMA CRT headroom/carry/normalization checks required. Only one NTT prime in toy vs source **three CRT primes**; no target CPU AVX512 run, no IFMA key prepare throughput or peak RSS measured. Not a claim all source packed AVX512 instructions accept raw arithmetic and automatically normalize.

## Honest source-shaped memory & latency screening [DERIVED]

Source example `N=16384,h=32,bases=[4,4,4,3],base2k52,dnum9,keysize10`, full HMux rank2 90MiB prepared/45MiB raw; **scalar beta input column 45MiB prepared/22.5MiB raw**; `other_prepared=2404MiB`. Original *I222 same four-key group staging* peak **named buffer**:
```
  other prepared: 2404MiB
  four current full raw key objects: 4×45=180MiB
  four current full prepared keys: 4×90=360MiB
  sum: 2944MiB = 2.875GiB
```
Candidate best-case even with a CUSTOM perfectly fused **tile-wise** reconstruction kernel, zero extra scratch/no new retained materialization and zero performance cost:
```
  other: 2404MiB
  raw: 4×45−22.5 =157.5MiB
  prepared: 4×90−45=315MiB
  optimistic sum: 2876.5MiB=2.80908203125GiB
  MAX possible differential under SAME group staging = 67.5MiB
  MAX PERCENTAGE = 67.5/2944 = 2.29279891304%
```
**H247 5% material-memory condition is FALSE even in an idealized implementation.** The real source kernel requires 4 completed rank2 prepared keys; naive prepare/reconstruct just restores 2944MiB plus extra scratch. A truly tile-fused implementation would add ~3168 public GLWE automorphism transforms across full fixed-key set (I246), component adds, extra memory traffic; this is not measured latency.

**Fairer optional baseline possibility, NOT implemented/benchmark-verified**: unchanged original keys could be streamed ONE candidate at a time while holding shared hoisted input DFT and DFT output accumulator across the whole group. Named memory under same other resident/stage-one-key assumptions: `2404+45+90=2539MiB=2.4794921875GiB`, already below the ideal 4-key I247 number by 337.5MiB. That also requires adapting original stock API (which accepts whole group). It is a **valid mathematical schedule and hypothetical memory frontier, not measured source RSS**. Thus comparison claiming >2.29% against original while denying single-key streaming baseline is unfair.

If other2404MiB are streamed too, denominators change and only active-group difference 67.5MiB absolute remains; no universal platform-wide peak RSS bound claimed. At-rest saved 5.625GiB/12.63% from I246 persists as a serialization niche, but **cannot be used as evidence for 12.63% resident RAM saving**.

## Security, noise, novelty, exact caveats

Existing source original evalkey baseline not λ128 security-matched to author SHIP: I245 original author h31 security audit SOURCE_BLOCKED; third-party Poulpy h32/HW192 q520 distinct. Reduced stored beta-column collection is literal subset of original random keys; public reconstruction cannot leak more than the original full collection under appropriate joint security notion, not a proof of 128bit. Reconstructed row errors accumulate b−1 source Gaussian errors; full IFMA N16384 and CKKS noise unverified. Prepared-domain linear combination is a known transform/property, no publication novelty asserted. No memory profiler or actual Rust binary run: cargo/rustc absent, git remote cannot resolve github.com in container; GitHub connector **source reads** are primary verified evidence, not compiled backend.

## End of Iteration

**STATUS: PASS** exact mathematical torus/NTT commutation (320/320) and source interface/word-size screening; **FAIL H247 substantive RAM improvement** (≤2.293% under fixed four-key staging, before any new scratch/latency); **SOURCE_BLOCKED** real compiled AVX512-IFMA RSS/latency/error test, **UNCLEAR** transform word headroom with noncanonical reconstructed digits. This does NOT prove source author's SHIP wrong, nor a universal no-go for all compression.

**RESULT:** Moving I246's onehot public scalar completion directly into prepared/NTT domain is theoretically implementable, but not within unmodified `ship_mux_rotate`, and the best possible ideal group-buffer reduction is only 67.5MiB against 2944MiB; the unmodified-key source can theoretically use finer one-key streaming and do better. Additional 3168 public ring automorphisms and scratch only hurt; no meaningful resident-memory Pareto for this route. Recommend PARK the I246–I247 onehot scalar column as main resident RAM optimization. At-rest/serialized-key compression remains modest (12.63%) and likely low novelty.

**NEXT_TEST / PI gate:** Do NOT build a new compiled IFMA fused VMP solely to chase ≤2.3% model memory gain unless a NEW actual workload demonstrates bottleneck and source-independent perf benefit, or the explicit target changes to persisted/transport keys with reliable prior-art differentiation. Reopen SHIP only for a new cryptographically nontrivial, source/security-matched >5–10% Pareto improvement under fair streaming, not another radix, toy repetition or security bits guess. PI decides PARK/pivot. I245 author-security is separate SOURCE_BLOCKED. **STATE_UPDATE YES** finding + root and topical only, reread verification.
