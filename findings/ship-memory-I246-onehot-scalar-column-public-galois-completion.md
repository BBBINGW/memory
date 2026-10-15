# SHIP-I246 — One-hot HMux scalar gadget-column reconstruction via PUBLIC Galois only

**Date:** 2026-10-16, explicitly PI-authorized "继续". **SHIP ONLY**, no CGS/VFHE/EXPLORE pivot or writes. Previous I245 author-SHIP h31 security audit is SOURCE_BLOCKED and remains so; I246 is a separate *new, previously untested within SHIP* HMux key-material candidate, NOT another source-free security estimate. Read-before-write: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`, `STATE.md`, `findings/ship-memory-STATE.md`, I229 and I236 + I245.

## ONE smallest falsifiable H246; ONE source-typed construction/correctness/cost test

**H246 [explicit, source-shaped]:** In original third-party Poulpy's B-way HMux group, one can **omit exactly the second beta-scalar input column of one GGLWE key per onehot group/support** while keeping *all beta*s first columns*, and PUBLICLY recreate the missing scalar gadget rows under the correct output automorphed secret *using only public Galois automorphisms and additions* of existing scalar ciphertext rows. In exact/modular RLWE this preserves full source HMux functionality, requires **no additional secret-dependent KSK, no high-q controls, no new online VMP multiply slots**, and conditionally saves >=10% **stored-at-rest** prepared evaluation key payload. It need NOT reduce **peak RAM against an equally group-streamed original**; tests must audit this honestly. Full IFMA/noise/novelty/runtime and λ128 are separate.

**Falsifier:** A ciphertext-target-secret mismatch, failure of scalar gadget invariance, wrong onehot correction under nontrivial dense secret, or the nominal bytes/extra-source-keys contradict the ≥10% at-rest storage goal. Source-compatible prepared-cache schedule and equal-streaming RSS are independent gates: if no RAM Pareto win, recommend PARK as core memory optimization.

## Primary source provenance [FACT]

- Original author Cheon–Hanrot–Kim–Stehlé, SHIP, EUROCRYPT2025, ePrint **2025/784**, original §4.2 Definition1/§5.1 Algorithm5 physical pp19–24. Original authored implementation was not obtained (I243–I245). No original SHIP weakness asserted.
- **Independent third-party** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, NOT authors' HEaaN:
  - `poulpy-ckks/src/layouts/ship/keyset.rs`, exact blob **8be6ab92846168330100efeabe9fa19dbd9720e4**: source `hmux_rot_key_encrypt_sk` creates **rank_in2** GGLWE rows with plaintext sources `(beta*s, beta)` under candidate output secret `t_d=sigma_(g_d^-1)(s)`, `gal_el` public, and `ShipKeySet::generate` chooses precisely one `beta_d=1` in each group. Source groups [4,4,4,3], h32 when using pinned example; no optional onehot-column omission or reconstruction implementation.
  - `poulpy-ckks/src/reference/ship/mux.rs`, blob **e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce**: `ship_mux_rotate` expects each original rank2 prepared HMux key, applies one shared input DFT and candidate VMP/Galois then group IDFT/normalize. To keep its online work unchanged, one must restore the missing prepared scalar input column **before** this operation, or refactor the VMP API. It is NOT zero preprocessing.
  - `poulpy-core/src/layouts/prepared/gglwe.rs`, blob **80a0d5e63df624cac01a70071da71f735b0b0b61**: prepared matrix shape `N*dnum*rank_in*(rank_out+1)*key_size` with IFMA DFTWord16 bytes.
- Prior same-line I204 denied summation *without output-key alignment*. I229 supplied cross-key KSKs to reconstruct BOTH columns; I231 quantified 6336 KSK and poor batch/RAM frontier. I246 is **NOT** that: public automorphism aligns the destination secret while preserving **scalar beta column plaintext only**; it cannot reconstruct the **beta*s first column** because public automorphism changes the polynomial s in the message. I235 warned never reuse the **same random encryption masks** among different support slots. Current variant DOES NOT reuse encryption masks; it only computes a derived omitted scalar ciphertext via postprocessing independently randomized original retained ciphertexts, yielding bounded correlated noise.
- Existing seeded-key serialization is old prior art; e.g., FRAST ePrint2024/745 Appendix keysize discusses seeded GGSW (not the same method). Scalar onehot affine completion and Galois are elementary operations; no claim of first-of-kind or publication novelty without deeper prior-art survey.

## Constructive synthesis [DERIVATION, correct secret domain]

Take support j, one radix group D of size b (3 or 4), omitted digit ℓ (e.g. last). Let `R=Z_q[X]/(X^N+1)`, `sigma_g(X)=X^g`, and `Dec_t(a,b)=b+a*t`. Each original scalar gadget row for digit d at original HMux high physical modulus Q_key is
```
C^(1)_{j,d,i}=(a,b)  with
Dec_(t_d)(C^(1)_{j,d,i})=G_i*beta_(j,d)+e_(j,d,i),
t_d = sigma_(g_d^-1)(s).
```
Use PUBLIC ring automorphism `rho_d = g_ell^-1*g_d mod2N`, so `sigma_(rho_d)(t_d)=sigma_(g_ell^-1)(s)=t_ell`. Because `G_i*beta` is a scalar (constant polynomial), it is invariant under sigma_rho. Let `T_i=(a=0,b=G_i)`, a known **trivial** GLWE encryption of G_i under ANY output secret (no noise). Define
```
   reconstructed C^(1)_(j,ell,i)
     = T_i - SUM_(d != ell) sigma_(rho_d)(C^(1)_(j,d,i)).
```
Then `Dec_(t_ell) reconstructed = G_i*(1-SUM_(d !=ell)beta_d)-SUM_(d !=ell)sigma_(rho_d)(e_d) = G_i*beta_ell + e'_i`. All automorphisms are public and invertible; no cross-domain KSK or ciphertext×ciphertext multiplication. **Do not attempt same equation for `C^(s)`** because `sigma_rho(beta_d*s)=beta_d*sigma_rho(s)`, not necessarily `beta_d*s`. Retain original independently encrypted `C^(s)_(j,ell,i)` for the missing digit, preserving rank2 source pairing and public final `sigma_(g_ell)`.

Noise: If source fresh high-q scalar row error coeff `|e_{d,i,k}|≤19`, an automorphism is a signed permutation, so `||e'_i||_∞≤(b−1)*19`: radix4 => **≤57**, radix3 => **≤38**. This is at high key ciphertext precision in ideal integer RLWE and excludes actual backend DFT/normalization errors and the full HMux noise propagation. Original row |e|≤19 is no longer sampled independently for omitted column, so do NOT claim equivalent error distribution. Fresh ciphertexts retained use independent random masks; reconstructed random mask is a public sum of their transformed masks, so there is no I235 identical-mask reuse. **Relative security no-worse claim only:** the reduced persistent bundle is a literal subset of the original independent-key bundle. Any derived omitted column is a public deterministic function of that subset. If an original augmented evaluation-key distribution is secure under an appropriate joint KDM/circular game, a distinguisher given just its subset and public postprocessing is simulatable from the original full bundle; this does NOT certify security of either base distribution at claimed λ128.

## Executed ONE exact negacyclic end-to-end toy

`/mnt/data/ship_i246_scalar_column_reconstruction.py` sha256 **352a0fadaac5b761b9cd1a6bb7e2d6116c02ac9225624bf99556e2c410be23f0**; JSON `/mnt/data/ship_i246_scalar_column_reconstruction.json` sha256 **bbc1a6b0fe3a0cc163a8425aa3881e9656d2e922feb7d4b2dcbba8e0b6accc54**. Executed Python standard library, full exact integer `R_(2^40)=Z_(2^40)[X]/(X^16+1)`, gadget base2^8 four levels (top row G2^32), Galois elements [1,5,9,13], nontrivial fixed ternary s, four hidden onehot choices, freshly randomized 40bit RLWE masks for BOTH beta*s and beta gadget columns and independent bounded errors e∈[-19,19], input ciphertext with 32-bit active coefficients and guard8.
- **128/128** complete full B-way HMux plaintext targets checked for BOTH original full and reconstructed missing-column key, including source-galois return to common original secret s.
- **512/512** omitted second-column rows rebuilt; max observed coefficient error **55**, satisfying theoretical ≤57 with 3 other candidate rows.
- Observed maximum final plaintext-decryption error in this toy: original139882; reconstructed132968 (the ordering is only this seed's observed error, NOT a general claim compressed version reduces noise). All under conservative `N*dnum*2*base*19*b` bound.
- Does NOT run real IFMA, full N16384 noise/CKKS scale, or perform any attack/security certification. No source author HEaaN benchmark.

## Correct source-shaped byte accounting and **honest matched streaming gate**

Pinned illustrative third-party source (NOT security-matched author SHIP) N16384,h32,[4,4,4,3],base2k52, dnum9, key physical size10, rank2 key **90MiB prepared =45MiB each column** (raw full key45MiB / one raw input col22.5MiB). Other prepared keys unchanged2404MiB:
```
baseline all eagerly-prepared named payload: (480*90+2404)/1024=44.53515625 GiB.
omit 1 scalar beta column per support/group = 32*4=128 scalar columns.
at-rest compressed prepared payload: (480*90−128*45+2404)/1024=38.91015625 GiB.
conditional persistent-prepared payload saving 5.625GiB=12.6304710%.
extra persistent secret-dependent KSKs = ZERO.
online after fully reconstructing original rank2 keys: original 17280, candidate 17280 symbolic polynomial product slots.
key-loading *public* transforms to reconstruct full material: 32*(3+3+3+2)*9=3168 GLWE polynomial automorphism instances, plus sums/copies/preparation and allocation; not 3168 online KSK.
```
**Critical fairness nuance:** The current Poulpy `ShipKeySet::prepare` eagerly materializes **full** 480 keys; to maintain only 38.91GiB prepared resident while running, **a new source format + just-in-time reconstruction/preparation + eviction is required**. If one expands all 128 missing second columns into full prepared keys and caches, prepared residency returns to **44.535GiB** PLUS staging scratch. With a competent demand loader retaining compressed prepared keys, plus a transient complete rank2 key and raw/transformed rows, a reduction versus **eager all-key resident original** is plausible (temporary ≥90MiB plus work), but needs API implementation, cache lifecycle and output precision verification; NOT a measured RSS improvement.

Against FAIR I222 unchanged original GROUPWISE external raw stream baseline, current max group b4 raw4×45MiB +prepared4×90MiB+other2404MiB=**2944MiB=2.875GiB**. In candidate, for full group evaluation, the missing scalar column must be reconstructed into raw/prepared state, so the four complete GGLWE keys are still present at use; current-source group named buffered **at least same 2944MiB**, potentially MORE due additional reconstruction scratch/need for retained raw rows. A still finer original one-key streaming schedule might lower both, reinforcing lack of demonstrated resident Pareto. If the missing raw/prepared scalar column is never expanded, an entirely new VMP key representation/kernel is required and online-product/work must be re-analyzed separately. No strict matched-policy RAM Pareto advantage is demonstrated.

A stored raw serialized source key saved one beta input column raw per missing digit (128×22.5MiB≈2.8125GiB), **conditional on storage serialization supporting partial keys and public re-expansion**. Seeded GGSW/TLWE compression is established prior art; partial-column reconstruction must demonstrate incremental novelty vs trivial affine onehot identities.

## Decision

**STATUS:** PASS scalar-column secret-domain algebra, exact noisy toy, conditional 12.63% *prepared-at-rest* key-storage arithmetic, unchanged online VMP algebra; FAIL strict source-matched groupwise RAM Pareto; full physical noise/performance/novelty and security parameters UNCLEAR. Candidate **PARK as cryptographic resident-RAM optimization**; perhaps niche as disk/at-rest compression with JIT if benchmark demonstrates value and source format refactoring is worth it. Do NOT falsely describe saving 5.625GiB *actual live RAM* in original key pipeline by deleting bytes before a compulsory expansion.

**NEXT_TEST (I247 only if PI explicitly continues):** no more simple onehot/key-cache microvariants. If investigating this niche further, require one **full source-compatible GGLWE prepare+VMP microbenchmark** comparing changed-format JIT preparation/eviction against a FAIR original groupwise loader at same security levels, reporting actual peak RSS, key-IO, latency, noise. If source runner unavailable, SOURCE_BLOCKED and recommend PI PARK SHIP cryptographic memory line. Separately I245 original author h31 security audit remains SOURCE_BLOCKED: do not silently claim its unresolved issue solved or retest it.
**STATE_UPDATE:** YES, append topical/root checkpoint only; other research tracks unchanged.
