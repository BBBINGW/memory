# SHIP-I229 — Cross-output-secret one-hot HMux key completion using guarded key switching

Date 2026-10-15. PI-selected SHIP evaluation-key memory research, following SHIP-I228, one primary construction and minimal mathematical/cost test. Parent: Cheon–Hanrot–Kim–Stehlé, *SHIP*, EUROCRYPT 2025 / ePrint 2025/784. Not a claim of a flaw in source SHIP.

## Primary hypothesis and one decisive minimal test

**H229 (bounded, conditional structural claim):** In a source-shaped fixed HMux radix group with one-hot hidden bits, one may omit exactly ONE encrypted HMux rank2 GGLWE key per support, add publicly available between-automorphed-secret KSKs and an unconditional base switching key, and publicly reconstruct both gadget columns of the missing HMux key *after aligning the destination secret domains*, without knowing any hidden bit and without ciphertext×ciphertext multiplication. For the pinned Poulpy N16384/h32/[4,4,4,3]/base52/k468 fixed prepared layout, this gives at least 20% **conditional stored prepared-key payload saving** even including all NEW converter and unconditional keys. Full real-world online efficiency, security and physical noise are expressly NOT in H229.

**Falsifier and ONE smallest test:** Establish correct key-domain alignment (I204 killed naive summation), prove the ideal gadget-row identity, execute *guarded auxiliary-modulus* noisy ring test with both columns and every legal onehot choice (modulus scaling and rounding NOT omitted), then audit the COMPLETE replacement byte counts and reconstruction application counts. FAIL if any key domain or ideal bit relation incorrect or savings <=20%. Pass does not imply a source-compatible Rust implementation, KDM security, precise noise or runtime benefit.

## Original source audit

- Original SHIP paper ePrint 2025/784 cached PDF 33 physical pp, mirror sha256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, **VERSION_UNVERIFIED**. §4.2 physical p19–20, Definition 1 and Lemma 2 introduce HMux `beta·Rot(ct)`; §5.1 physical p23–24 Algorithm5 gives gadget keys for `beta·s_g` and `beta`, and describes B-to-one mux. This finding studies a new derived storage representation, not original author claims.
- Pinned **third-party** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, not authors' HEaaN:
  - `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `hmux_rot_key_encrypt_sk` rank2 source input `(beta_d*s,beta_d)` under output `t_d=sigma_(g_d^-1)(s)`, with `g_d` based only on public digit rotation d. `generate` creates exactly one `beta=1` per radix digit per support. Same d within different support slots has identical *output secret*, but independently randomized HMux ciphertexts. Original also stores conjugation -1 but no general new cross-domain KSK bundle.
  - `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: applies one source rank2 product for each candidate, aligns with its public automorphism before accumulation. Any reconstructed omitted key MUST have original candidate's output secret t_ell, not a common arbitrary one.
  - `poulpy-core/src/reference/keyswitching/glwe.rs` blob `67fd537f256687a95bf1c7c719392a0d49fe5827`, `glwe_keyswitch_reference` lines ~497–620: prepared GGLWE product, add input body, **IDFT + normalization** to requested result precision. Guard via `k_aux` is relevant: switching key ciphertexts require increased physical modulus. Blind multiplication of raw 52-bit digits times KSK error without the auxiliary normalization is NOT this algorithm.
  - `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: prepared VmpPMat dimensions `N*dnum*rank_in*(rank_out+1)*key_size`.
  - Prior `findings/ship-memory-I204-hmux-key-domain-obstruction.md` killed direct raw summation. The current candidate specifically repairs that narrow key-domain obstruction via additional public KSKs. Prior I228 failed direct multiplication of *full-width body by ordinary Enc(beta)*, which is NOT used here.

## Constructive synthesis [DERIVED]

Fix one radix group `D={0,...,b−1}`, final omitted candidate `ell=b−1`, and support j. One-hot secret control bits `beta_{j,d}` satisfy `sum_d beta_{j,d}=1`. For each digit d the source HMux GGLWE has two gadget-message columns (a source-specific torus gadget weight G_i is used, orientation immaterial here):
```
C^(s)_{j,d,i} = Enc_{t_d}(G_i beta_{j,d} s + e^(s)_{j,d,i});
C^(1)_{j,d,i} = Enc_{t_d}(G_i beta_{j,d} + e^(1)_{j,d,i});
t_d = sigma_(g_d^-1)(s).
```
Add PUBLIC extra `KSK_{t_d -> t_ell}` for every non-omitted d and every **distinct digit-group rotation difference**, plus an unconditional rank1 key (one per group) `U_i=Enc_{t_ell}(G_i s)`. For constant column use public trivial `V_i=(a=0,b=G_i)=Enc_{t_ell}(G_i)`. Key-switch retained source rows into the missing candidate's output key domain:
```
D^(x)_{j,d,i} = KeySwitch_{t_d -> t_ell}( C^(x)_{j,d,i} ), x∈{s,1}.
C^(s)_{j,ell,i} := U_i − ∑_{d≠ell} D^(s)_{j,d,i}.
C^(1)_{j,ell,i} := V_i − ∑_{d≠ell} D^(1)_{j,d,i}.
```
Ignoring switching/encryption/rounding errors, decryption under **t_ell** gives `G_i s*(1−sum_{d≠ell}beta_{j,d})=G_i beta_{j,ell}s` and `G_i beta_{j,ell}`, respectively. The *reconstructed pair* is consumed by original HMux `ship_mux_rotate` as if it were the original last candidate, including its public `g_ell` output automorphism. No encrypted β is decrypted, revealed or byte-reused. However public extra auxiliary key correlations and equality-side information require a security proof, NOT asserted.

## Executed minimal exact noisy-modulus gate [PASS structure, real noise UNCLEAR]

Python `/mnt/data/ship_i229_onehot_completion.py`, SHA256 `4732a6378290f3cc4a1d852bd0ca147a7f0ee98e593a9a24b3f799b79b107533`, produced `/mnt/data/ship_i229_onehot_completion_results.json`, SHA256 `a110b9c6051c044af57123358552002ef2199ca2d453e4313630ccad06a638c3`; both executed/verified in current environment. Ring toy `R=Z_(2^20)[X]/(X^16+1)`, nonzero ternary `s=X+X²−X⁵`, four source-style rotation key domains based on generator5 modulo32, 4 gadget digits base32, and **guarded KSK ciphertexts at 2^25**, normalizing from qP to q by coefficient rounding. Random full-width RLWE masks; valid KSK row errors fixed e∈{0,1,19} (an illustrative allowed bounded Gaussian value, not typical distribution sampling). All 4 one-hot states ×2 source columns ×4 gadget rows =32 reconstructed rows per error level. Errors measured as maximum centered *coefficient* decryption deviation from exact ideal target under omitted output t_ell:
- e_KSK=0: max3, mean1.9375 (rounding only);
- e_KSK=1: max9, mean8.3125;
- e_KSK=19: max168, mean143.25.
The results demonstrate **correct message/key-domain alignment modulo bounded switching/rounding noise** and explicitly show degradation relative to freshly encrypted rows. They DO NOT establish a full 16384-dimensional security or precision guarantee, and do NOT use actual IFMA code. The e_KSK=19 case does not meet the original row Gaussian absolute cutoff 19, so no same-row-noise law holds automatically. The auxiliary 5-bit toy normalization is essential: **a no-auxiliary KSK toy may falsely predict huge noise**; this was experimentally caught and corrected before the checkpoint. With real KSK error polys and dense ring convolution, no full-degree error bound follows from small-toy maxima. The toy also uses simplified base-power gadget weights and rounding rather than exact source torus representation.

## Full source-shaped memory AND reconstruction cost (including additions)

Parameters: `N16384,h32,theta4,mux_bases=[4,4,4,3],B=2^52,k_ct=468, original HMux key k_key=520`, dnum9,key_size10. Exact source-prepared:
- baseline: 480 rank2 HMux×90MiB =42.1875GiB + other2.34765625GiB = **44.53515625GiB**;
- store only `(sum b_i−1)*h = (3+3+3+2)*32=352` original rank2 HMux×90MiB, omitting `4*h=128` keys = **11.25GiB** removed;
- add `4` unconditional **rank1** source-s-switching keys at existing k520, prepared `N*9*1*2*10*16=45MiB` each (second constant column public trivial) =>180MiB;
- add `sum(b_i−1)=11` (conservatively distinct) cross-output-domain rank1 switching keys with **input original HMux ciphertext modulus k520**, hence need 10 gadget rows, physical k572, size11 => `N*10*1*2*11*16=55MiB` each, total605MiB. All extra prepared `785MiB`.
- **compressed named key payload =44.53515625−11.25+785/1024 =34.0517578125GiB**. **23.5396017893% conditional saving**, passes 20% H229 memory threshold. This is conditional **stored prepared-object payload**, not true peak RSS, serialized key compression ratio, physical 128bit security or runtime. New layout API not implemented.
- Reconstruction of all 128 omitted 2-column ×9-digit keys needs `h*sum_g(b_g−1)*2*9=32*11*2*9=6,336` **additional rank1 key-switch operations** to transform the retained candidate key rows into each missing target key domain (before subtractions/preparation). Those are operations on **evaluation-key ciphertexts**, not 6,336 online ciphertext×ciphertext multiplications. If these 128 omitted rank2 keys are **eagerly reconstructed and retained**, the memory savings disappear and prepared payload becomes baseline + 785MiB = **45.3017578125GiB**, worse than baseline. To retain savings they must be lazy-expanded/discarded or prepared once and amortized over a large same-key batch. With lazy reconstruction, additional computation and scratch *do occur during the execution pipeline*, even if no FHE multiplicative depth is consumed on data ciphertext. No measured time/RSS/IO; there is no claim of a Pareto improvement.

## Security and novelty gate

The original SHIP full eval bundle does not contain the 11 between-output-secret KSKs or 4 unconditional key encryptions of s, so original security alone does NOT prove the augmented joint distribution secure. Conditional public postprocessing is safe *given* a security notion for the entire augmented correlated input bundle, but this assumption/reduction is NOT established. The selector β depends on the sparse secret and keys correlate with dense s, so marginal INDCPA is insufficient. Original sparse/dense parameters at k520/k572 still lack matched 128-bit model (I216 etc). Exact onehot linear complementation + ordinary key switching is elementary algebra; no verified literature novelty. One recent prior-art scan found generic FHE key switching and on-the-fly key preparation but no established exact source-equivalent SHIP completion, **absence from a few results is not a novelty guarantee**.

## Final decision

**STATUS:** **PASS H229 narrow structural key-domain/cost gate**; **PASS toy guarded-modulus functionality with quantified noise**; **UNCLEAR** high-degree ring convolution, true RLWE/GGLWE row precision after completion and entire SHIP bootstrap, jointly augmented-key KDM/security, real latency and useful memory-vs-recompute frontier. **NOVELTY NOT VERIFIED / LIKELY LOW** due elementary relation and common KSK.

**RESULT:** I204's direct-domain failure is repairable by adding ordinary public between-secret switches, and a complete ideal gadget-key row can be publicly derived from the other one-hot candidates with a conditional ~23.54% complete prepared-key payload reduction. This is neither free nor a validated cryptographic optimization: it adds 15 prepared auxiliary key objects and 6,336 key-to-key switching operations per complete expansion, and cannot simultaneously claim 23.54% resident RAM saving and zero expansion cost.

**NEXT_TEST:** One full-degree, source-parameter-aware physical **noise gate** for key-to-key KSK + missing-row completion + subsequent HMux: quantify key-row error under actual GGLWE gadget/aux modulus, convolution, rounding and intermediate CKKS slot precision; decisively kill if target 18.1-bit tolerance is exceeded. Only if noise gate survives, assess online rebuild caching/latency/peak RSS and explicit full-bundle security. Do NOT repeat toy n16 or characterize this as publishable. The human PI owns any pivot/PARK.

**STATE_UPDATE:** YES, write finding and append topic + root STATE, read back. All historical files preserved.
