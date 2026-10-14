# SHIP I216 — 128-bit security-guideline gate invalidates certification of the illustrative N=16384, k=624 comparison

**Date:** 2026-10-14 (Asia/Tokyo). **Independent SHIP** research iteration after I215. The PI said “好的，请继续”. **Read-before-write:** START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (parallel vFHE V17, READ ONLY), findings/ship-memory-STATE.md (I215 checkpoint SHA 6fbb84e8ad9459cb8519f34638f43592c185379b), I215 and I207/I214 source records. No global vFHE or upstream Poulpy modifications.

## One primary falsifiable claim

**H216:** The representative I207 key-memory gain (baseline N=16384, k_ct=468 versus candidate N=16384, k_ct=624, auxiliary per-HMux-key physical width k_key=676 at B=52,dnum12,k_aux52) can be presented as a **128-bit classical-secure parameter-to-parameter comparison certified by the currently published homomorphic-encryption security guideline tables**, without a new sparse-secret-specific estimator or larger ring degree.

**Falsifier / one minimal test:** Compare **largest ciphertext modulus bit length AND key-material modulus bit length** for both instances to a primary-source 128-bit classical target table at ring N16384 (rank1, sigma≈3.2) while checking whether the source secret distribution is actually covered. H216 FAILS if source instance sizes exceed the table's maximum covered modulus or if the secret distribution is outside its estimated family. This is a security-*certification* test, **not** a cryptanalytic attack or assertion of insecurity.

## Independent primary source [FACT]

Published security guidance:
- Jean-Philippe Bossuat et al., **“Security Guidelines for Implementing Homomorphic Encryption,” IACR Communications in Cryptology 1(4) (2024)**, DOI `10.62056/anxra69p1`, ePrint **2024/463**, current inspected PDF `https://eprint.iacr.org/2024/463.pdf` 33 physical pages, Table **5.2** at physical PDF page index **11** / printed page 12 (PDF text lines 451–482). Authoritative community index `https://homomorphicencryption.org/security-guidelines/`; published HTML `https://cic.iacr.org/p/1/4/26`.
- The inspected **2024 ePrint** PDF Table 5.2 (classic Category 128, Gaussian error sigma3.19, uniform ternary secret) states `N=8192→max log2q214; N=16384→430; N=32768→868; N=65536→1747`. For Gaussian secret N16384, it reports 432. **Do not substitute the older 2018/older preview figure 438 for this inspected version's 430.** The table consists of LWE-estimator-based targeted guidelines, not a proof of insecurity above the line and not a universal security upper bound across all secret distributions or auxiliary-key relations.
- The guidelines §2.3 and pp5–6 explicitly note that sparse fixed-Hamming-weight secrets are **NOT INCLUDED** in their standard parameter tables; specialized sparse-secret/hybrid attacks and parameter assessment require further work. It is **not sound** to claim “430 proves 624 insecure” nor to claim “N32768 passes 128 bits” for sparse-secret hw192.
- §5.1/notation Table5.1 clarifies the security modulus `q` is **largest ciphertext modulus**, with auxiliary `P` accounted for in `q=P Q` in RNS key-switching contexts. A separate GGLWE evaluation-key ciphertext generated at physical modulus 2^676 must not be omitted from security-parameter investigation simply because ordinary online ciphertexts run at 2^624.
- The web PDF screenshot call could not render due eprint HTTP403; textual extracted Table5.2 row was legible and independently anchored by the security-standard page; explicit source limitation: **visual PDF page not verified** in this iteration.

Poulpy source (third-party independent of original SHIP author HEaaN) `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
- `poulpy-ckks/src/layouts/ship/plan.rs` `ShipPlan::raised_k(52)=round_up52((tree_depth+2)*ld+log_budget_out)` yields **468** for h32, ld40, desired budget104. I206's naive 4 extra serial 40-bit CT×CT mux gating needs **624** to retain nominal 104 (after limb rounding).
- `poulpy-ckks/src/layouts/ship/keyset.rs` `hmux_rot_key_encrypt_sk` allocates physical key width `k_key=dnum*dsize*base2k+k_aux`, `dnum=ceil(k_ct/52)`, dsize1,k_aux52; baseline k468→dnum9,k_key **520**; candidate k624→dnum12,k_key **676**. `poulpy-core/src/layouts/mod.rs` confirms physical key limbs. This is a cryptographically relevant modulus to assess for an RLWE-based encrypted key material (but a precise estimator has not been run).
- `poulpy-ckks/src/test_suite/mod.rs` `BASE52_PARAMS_F64` has dense secret `hw=192`, and `poulpy-ckks/src/test_suite/ship.rs` `gen_sk_with_host` samples **fixed-weight ternary**, so not the table's uniform ternary distribution. Sparse bootstrap secret h32 is another related secret and joint key relations remain security UNKNOWN (I210).
- `poulpy-core/src/noise_distribution.rs` `Noise::ENCRYPTION` uses sigma3.2 truncated at ±19, sufficiently close to guideline's sigma3.19 for an illustrative warning, **NOT** enough to identify exact LWE attack costs.

## [DERIVED] Exact source-vs-guideline comparison

For **N16384**, 2024 guideline Table5.2 *uniform-ternary* target reference max `log2q=430`:

| Keying instance | ciphertext k | HMux GGLWE physical k | CT excess vs430 | key excess vs430 |
|---|---:|---:|---:|---:|
| illustrative baseline (I203) | 468 | 520 | 38 | 90 |
| widened sharing (I206–I215) | 624 | 676 | 194 | 246 |

**H216 FAIL** as stated: neither instance is already certified by this table, and sparse ternary hw192 is outside the table's actual modeled secret families. This is an *important resource-comparison validity gap* and a potential categorical research dead end for the claimed N16384/128-bit *scenario*. It **does not demonstrate a break of original SHIP**, which may use other parameters and security analyses; source numbers were illustrative, not certified 128-bit. It **does not prove candidate insecure** either.

If one merely uses the **uniform-ternary** 128-bit reference table as a **necessary preliminary screening target** for key-modulus k676, N32768's table figure 868 would be above676, whereas N16384's430 is below676. A **conditional ring-upsize projection** doubling N from16384 to32768 at fixed key counts, gadget width and window would linearly double the I203/I207 *IFMA prepared payload formulas*: baseline 44.53515625→**89.0703125 GiB**; candidate 8.2626953125→**16.525390625 GiB**; modeled relative saving still 81.4468%. **But** fixed sparse hw192 becomes even sparser, rotation windows/plan parameters may change, and actual key security, key generation, noise, performance and memory comparison have NOT been revalidated; these figures are just N-scaling arithmetic, not a new secure design.

## Critical limitations

1. **No LWE estimator executed.** The exact N16384 sparse hw192 / N32768 sparse hw192 attack cost, ring structure, modulus of each related-key sample, m, hybrid attack, truncated discrete noise and key-dependent ciphertext messages all need explicit modeling; standard uniform ternary q table does not apply automatically.
2. **Security target conditional:** the PI has not explicitly fixed lambda=128 as a project design requirement, so this is a significant warning for a plausible deployment target, not an assertion that every academic toy setting must meet 128 bits.
3. **Key material correlation:** Separate joint KDM/circular security failure of proof is archived in I210; ordinary lattice attack security estimation and joint auxiliary-key semantics are independent axes.
4. **Full FHE experiment still blocked:** no rustc/cargo/pinned checkout; compiled Poulpy row11+40 CKKS controls and full mux latency unknown. I215's full-N ideal coefficient rounding bound does not certify cryptographic security.
5. **NOVELTY NOT VERIFIED**; not a paper claim and not a finding against SHIP authors.

## End of iteration

**STATUS:** **FAIL H216 security-table-certification claim**; **PASS** source-vs-2024 guideline precise parameter mismatch test. **UNCLEAR** actual security bits (sparse secret), reparameterized N32768 implementation/budget/cost, augmented joint KDM, latency and novelty.
**RESULT:** We should **not** continue treating the previous 44.535→8.263GiB / 81.45% memory comparison at N16384 as a fair **128-bit secure comparison**. Source's physical HMux key modulus is k676, which exceeds inspected 2024 N16384 uniform-ternary reference ceiling430 by246 bits; even baseline k520 exceeds reference by90 bits. This is independent of the previous numerical-error, I212 row10 wrap, and I210 key-security gates.
**NEXT_ACTION:** Recommend **PARK the specific N16384/k624 “128-bit” comparison**. Before further implementation or performance claims, human PI should choose concrete threat/security target and require a sparse-secret-specific LWE/GLWE + joint-key security assessment for the full evaluation-key family, with all physical key moduli. If lambda128 is a requirement, first screen realistic **N≥32768** candidates in a compatible full parameter configuration (not assume it passes). Only then repeat prepared-key payload and online cost at a *security-matched* baseline and variant and run Rust benchmark. Do not automatically create infrastructure or claim security proof. **STATE_UPDATE:YES** independent SHIP checkpoint only; **NO global vFHE STATE.md**, no upstream changes.
