# SHIP I221 — Fresh PK→D2S masks can be conditionally iid, but NOT statistically uniform RLWE masks

**Date:** 2026-10-14 Asia/Tokyo. **Independent SHIP evaluation-key memory iteration I221**, immediately following I220. Read-before-write checked START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, concurrent global STATE.md (vFHE V17, READ ONLY), findings/ship-memory-STATE.md I220 SHA bc0c34db4b3b0ed1b012588883f16835240beb3d, and findings/ship-memory-I220-d2s-public-derivation-no-new-sparse-randomness.md. No changes to global STATE/vFHE or upstream Poulpy.

## One primary falsifiable hypothesis and one cheapest decisive test

**H221:** In a *PK-enabled* variant of the source-shaped SHIP instance, with fixed public dense pk_s and fixed published D2S key K, if every query uses fresh independent public-encryption coins, the derived q0=2^52 ciphertext masks are **conditionally iid UNIFORM random polynomials** over R_{2^52}, so one may feed them directly to a classical independent uniform-mask sparse RLWE attack estimator.

**Falsifier:** Read the pinned public-key encryption sampler and D2S deterministic code, then count the maximal number of distinct output mask polynomials possible for **one** fixed public key bundle using only ephemeral and fresh mask-error randomness. If the support is strictly smaller than 2^(52N), the uniform-mask premise is mathematically false. Crucially separate **conditional independence** (which may hold!) from **uniform marginal** (which fails). No sampling necessary; source-specific combinatorial support count is decisive.

## Source provenance [FACT]

Original scientific parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / ePrint 2025/784, prior cached mirror PDF physical p10 §2.1 standard CKKS PK+Enc model. PDF version status VERSION_UNVERIFIED, SHA256 3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742. Audited **independent third-party Poulpy, NOT the authors' HEaaN** pinned poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf.

- `poulpy-core/src/reference/encryption/glwe.rs` blob 8caec305a9412fa769bf36ccea122cbeae3bd697: `glwe_encrypt_pk_internal` lines ~432–487 gets ephemeral distribution `dist=*pk.dist()` inherited from secret distribution, rejects zero/encapsulated, calls `scalar_znx_fill_distribution(...,dist,source_xu)` **once for each PK entry**, forms public product `vmp_apply_dft_to_dft(u,pk.data)`, then adds fresh Gaussian `Noise::ENCRYPTION` from `source_xe` separately for all mask columns. The result's canonical normalization is deterministic. For rank1 source test, ONE ephemeral polynomial u and ONE mask error polynomial e_a suffice to determine the output mask when pk is fixed.
- `poulpy-core/src/oep/derived/encryption.rs` blob 8e8f0ef66a6bfc1406c9d643ea3f3e912149d0a6: `glwe_encrypt_pk_derived` passes new `source_xu` and `source_xe` to the reference public-key sampler.
- `poulpy-core/src/dist.rs`: `Distribution::TernaryFixed(h)` means exactly h nonzero entries from {-1,0,+1}. Source `poulpy-ckks/src/test_suite/mod.rs` blob e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb sets BASE52_PARAMS_F64 `hw=192`, base2k52 and rank1; `poulpy-ckks/src/test_suite/ship.rs` creates matching dense secret with `glwe_secret_fill_ternary_hw(params.hw)`. The test-suite default N is 256; **N16384 is an explicitly chosen source-shaped SHIP benchmark setting/override, not the unmodified test-suite default nor a claim about the original authors' deployment**.
- `poulpy-core/src/noise_distribution.rs` blob e231917a72be54a5e8dca47ece9f7d8672828020: `Noise::ENCRYPTION = Gaussian{sigma:3.2}`, cutoff coefficient exactly -19 to +19, so at most 39 integer error possibilities per coefficient on the selected sampling precision grid. Whether `k_sample` is 52 or 104, normalization after adding this noise is deterministic.
- `poulpy-core/src/reference/keyswitching/glwe.rs` blob 67fd537f256687a95bf1c7c719392a0d49fe5827: public `glwe_keyswitch_reference` has no RNG; output mask from input mask and fixed public K only. Separate initial D2S key generated once with physical k104, output is bottom q52, as I218.
- **Interface qualifier:** bare `ShipKeySet` does **not** store matching dense PK; its external publication is an extra explicit assumption from I219.

## Exact source-specific bound [DERIVATION + EXECUTED]

Fix the entire public dense PK, fixed D2S key K, modulus q0=2^52, one **rank1** ring dimension N=16384 and source-shaped fixed Hamming weight hw=192. Select a fixed known message m (zero suffices). One fresh public-key encryption draws one ephemeral polynomial u with ≤C(N,192)*2^192 possible values and one fresh independent mask error polynomial e_a with **≤39^N** possible values. Given fixed pk, input mask is a deterministic function of (u,e_a). Given fixed K, output sparse mask is a deterministic function of that input mask. No further randomness is introduced by public switching or truncation.

Thus |Supp(M_sparse | pk_s,K,m)| ≤ C(16384,192)*2^192*39^16384, even allowing all worst-case Gaussian tails. By contrast, a uniformly distributed q0=2^52 rank1 GLWE mask has exactly (2^52)^16384=2^851968 possible ring polynomials. In particular:
- log2 ephemeral support upper = 1693.944886052657.
- log2 fresh mask error polynomial support upper = 86596.02995383908.
- log2 switched mask support upper = 88289.97483989174.
- log2 all truly uniform q0 masks = 851968.
- gap > 763678.0251601082 bits.

For any probability distribution P supported on S and true U uniform on a finite set Ω, TV(P,U) ≥ 1-|S|/|Ω|. Consequently TV(M_sparse | pk_s,K,m, U_uniform(q0)^N) ≥ 1 - 2^(-763678.0251601082). This is **near maximal STATISTICAL distance** for the mask in the fixed-PK version of our explicitly stated source-shaped parameter model. It is **not** computational distance, no distinguisher running in polynomial time is demonstrated, and not a scheme insecurity claim. The same cardinality objection applies to many standard PKE systems; a security reduction can make even statistically sparse public encryptions computationally pseudorandom.

**Conditional independence correction to I220:** With fixed public (pk_s,K) and **independent** fresh calls using independent (source_xu,source_xe) and same chosen plaintext, the observable output ciphertexts Y_i = D2S_K(Enc_pk_s(m;R_i)) are **independent and identically distributed CONDITIONAL ON pk_s,K**, simply because deterministic functions preserve independence of independent R_i. Thus sharing a published K by itself does NOT invalidate conditional independence. The errors relative to unknown s_sp and assumptions of uniform mask / bounded independent scalar error must be analysed separately. Across adaptive chosen messages or correlated RNG sources there is no blanket iid assertion. Unconditionally over randomly generated keys, they share public randomness and need not be iid; fixed-key conditioning is essential.

## Reproducibility

Source-shaped exact big integer count and source-support assertions were executed as a standalone Python script, not as a Rust ciphertext run:
- `/mnt/data/ship_i221_conditional_mask_support_gate.py` SHA256 `4d0b8830f40f7116f81ddcf005e3c0c60cf9d4a83e723bef31b1f1a7bbf36b06`.
- `/mnt/data/ship_i221_conditional_mask_support_results.json` SHA256 `7023c9fd77a7ce498f50afac9018a331975486bcebf77d5387ecaadfcbb3e41a`.

## Interpretation / scope

**STATUS: FAIL H221** direct *conditional uniform-mask RLWE* claim; **PASS** correct theorem: fresh independent PK encryptions yield **conditionally iid public derived ciphertexts** under the same fixed keys but their mask support is minuscule relative to uniform q0^N, so no information-theoretic i.i.d. *standard RLWE* reduction by naive substitution. Statistical far-from-uniform does **not** prove computational distinguishability, insecurity of original SHIP, or cryptanalytic novelty. A computational RLWE/PKE-to-derived-output reduction might exist, with auxiliary key distribution caveats, but is unproven here.

**RESULT:** Reconciles I219/I220: repeated same-mask outputs are trivially non-independent; *fresh* conditional outputs ARE iid, but **not statistically uniform-mask RLWE**. Direct q104 one-row D2S key and q52 derived outputs remain distinct; high q676 HMux under dense s, structured sparse h32 key, KDM and dense fixed-HW192 security assessment remain open.

**NEXT_ACTION:** HUMAN_REVIEW / PARK unless PI identifies a concrete **computational** reduction/attack exploiting the public PK + D2S correlated-key distribution, plus a matched dense-key high-q estimator, or provides a real Rust benchmarking runner. More source-shaped entropy counts and toy iid sampling should NOT be pursued merely to increment iterations. Security-matched N and q, joint auxiliary-key KDM/circular assumptions, and ~480 additional high-precision CT×CT operations remain decisive blockers for conditional I207 ~81.45% prepared-key memory gain. The PI decides pivot/continue/archive.
**STATE_UPDATE: YES** independent SHIP state and finding. Global vFHE STATE and upstream untouched. **NOVELTY NOT VERIFIED.**