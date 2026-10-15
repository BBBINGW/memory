# SHIP-I239 — Direct first-gadget-row public modulus projection: single-sample low-noise RLWE from original Poulpy HMux keys

Date 2026-10-16 (Asia/Tokyo). **ACTIVE PI topic SHIP HMux evaluation-key memory/security-matched baseline.** Read-before-write: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, root STATE.md, findings/ship-memory-STATE.md (I238 latest), findings/ship-memory-I238-original-hmux-onehot-public-rlwe-closure.md, earlier I233 attack family and I216 parameter warning. This is a narrow independent *security interface* audit of the illustrative pinned THIRD-PARTY Poulpy HMux key format, not a claim of a flaw in SHIP original authors' HEaaN, a key recovery, or a complete bit-security computation.

## One primary hypothesis and one cheapest decisive test

**H239:** The problem left in I238 (having to evaluate publicly derived onehot-summed q520 RLWE with **sigma≈5.54/6.4**) is NOT necessary for the strongest obvious attack screening: in the unmodified source HMux gadget-key rows, some β-dependent messages are divisible by a large power of 2, so reducing a single public GLWE row modulo that power already yields known-zero RLWE under the SAME fixed-weight dense secret with **single-source ENCRYPTION Gaussian σ3.2 and no onehot summation**. In pinned base52,dnum9,k_aux52, a candidate modulus is **2^468**, making the specialized 2026 sigma3.2 rotated-primal-hybrid reference table immediately relevant as a **parameter warning**. Falsify if the gadget weight exponent, bottom-noise position, output-key secret alignment or sample randomness is wrong. The hypothesis is about extracting and matching a *reference input*; it does NOT hypothesize a proven attack of <128 bits without exact estimator and finite-sample/marginal-distribution checks.

**ONE cheapest decisive test:** Read source gadget generator, limb ordering, key physical width and bottom-sampled encryption noise, derive exact key-first-row scale, test both secret and constant β gadget columns with independent random β (NO onehot), random masks and truncated Gaussian noise in an exact negacyclic ring; compare extracted parameters to exact specialized attack estimator source/table; check Sage availability and sample cap before making any concrete security claim.

## Primary sources [FACT]

- Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT2025, ePrint2025/784, original §5.1 Algorithm5 physical pp23–24; original paper explicitly uses different security-tested key widths (its §5.2 p24, e.g. N2^14 and log2(Pq0)=100 with sparse h31) than the **independently chosen illustrative** source layout below. Its PDF cached from GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, 33 physical pp, VERSION_UNVERIFIED. NOT an attack on original authors' scheme.
- **Independent third-party pinned Poulpy `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:**
  - `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` `hmux_rot_key_encrypt_sk`: rank-in2 messages `(beta*s,beta)`; output secret `t_d=sigma_(g_d^-1)(s)`; `dnum=ceil(k_ct/base2k)=9` for raised k_ct=468 and base2k52, `k_aux=52`; `generate` creates h32×15=480 HMux key objects in the selected source-shaped model, candidate g_d public.
  - `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5fca808a07d0`, lines~127–154: for every `col_i∈{0,1}`, `row_i=0...8`, initializes plaintext `tmp_pt` and calls `vec_znx_add_scalar_assign(...,(dsize-1)+row_i*dsize,...)`; for dsize1, **FIRST row_i0 message is stored in TOP limb index0**, i.e. numerical torus 1*2^-52. Each row has freshly sampled independent `a` via `fill_glwe_mask_from_source`, then fresh `e` via `glwe_encrypt_sk_internal`.
  - `poulpy-core/src/layouts/mod.rs` blob `c1e953bed001d3129188f4c0c5d35073a82ee59d`, `key_k=dnum*dsize*base2k+k_aux`; key physical width `9×52+52=520`. The auxiliary bottom guard is an explicit error region. `poulpy-hal/src/api/vec_znx.rs` blob `01bca5331f68db07dd03fd2cc312524a354cf44f` describes uniform sample limbs in increasing index order; coefficient torus top limb0 has scale 2^-52, so at precision k520 it is the integer multiple **2^(520−52)=2^468**.
  - `poulpy-core/src/reference/encryption/glwe.rs` blob `8caec305a9412fa769bf36ccea122cbeae3bd697`, `glwe_encrypt_sk_internal`: fresh-noise addition to body via `vec_znx_add_noise(base2k,k,...Noise::ENCRYPTION)` at physical bottom. `poulpy-core/src/noise_distribution.rs` blob `e231917a72be54a5e8dca47ece9f7d8672828020`: nominal Gaussian sigma3.2, truncated coefficient abs≤19. Physical compiled IFMA sampled ciphertexts were not inspected; this source-semantics inference could be checked directly with an actual runner in future.
  - `poulpy-ckks/src/test_suite/ship.rs` blob `a5e89638c430886e57c036e001093827293bfae0`: dense secret generation uses `glwe_secret_fill_ternary_hw(params.hw)`; `poulpy-cpu-oracle/src/scalar_znx_fill.rs` implements TernaryFixed(hw) with exactly hw nonzeros but **each sign chosen independently as ±1**. Thus it is NOT identical to the estimator's EXACTLY hw/2 positive and hw/2 negative secret prior.
- SPECIALIZED PUBLIC SECURITY REFERENCE: Tabitha Ogilvie, *On the Concrete Hardness Gap Between MLWE and LWE*, ePrint2026/279 (merged into Hou–Jiang–Ogilvie, *Careful with the Ring!*, CRYPTO2026), and Jules Dumezy `jdumezy/sparse-key-estimate` source `Precomputed-Tables/128bits_security.md` blob `350df85fa8198351fbc096b5ab49caa6073280ea`: at logn14,h192,sigma3.2 reference max logq **367** for target≥128 model bits. `PrimalHybrid/sparse_estimates.py` blob `d0d59eb0bf6ac514e6eeb56a08af7485dd504fbd`: uses `Xs=ND.SparseTernary(p=h//2,m=h-h//2,n=n)`, `Xe=ND.DiscreteGaussian(stddev=sigma)`, unlike independently chosen sign counts in Poulpy. `PrimalHybrid/lwe_rot_primal.py` blob `a2bea82715f23089afc606398933623122c583c4` has `m=oo` default sample parameter. The reference table is heuristic/attack-estimate threshold, NOT a proof of insecurity for every prior.
- Environment direct check `command -v sage`, `importlib.util.find_spec('sage')`, `find_spec('fpylll')`: **NO Sage/fpylll** installed; no proper matching 960-ring-sample exact-signed-dist run, no BKZ/actual secret recovery. Do not report invented security-bit counts.

## Exact public reduction [DERIVED]

Let `R_q=Z_q[X]/(X^N+1)`, `q_key=2^520`, gadget dnum9 digits of base `2^52` and one 52-bit guard limb. Source row index `r=0` has plaintext gadget `G_0=2^468` in physical-q integer units. In BOTH of source rank2 input gadget columns:
```
  A_{j,g,d,c,0} ∈ R_(2^520) uniform;
  B_{j,g,d,c,0} + A_{j,g,d,c,0} t_d
     = 2^468 * M_{j,g,d,c} + e_{j,g,d,c,0} (mod 2^520),
  c=0: M=beta_{j,g,d}*s; c=1: M=beta_{j,g,d}.
  t_d=sigma_(g_d^-1)(s), beta∈{0,1}.
```
All coefficients of `M` are integers. Apply the **public** ring homomorphism reduction modulo `q'=2^468` separately to A and B (nothing secret, no product or interpolation):
```
  B' + A' t_d = e_{j,g,d,c,0} (mod 2^468).
```
Optional public `sigma_gd` alignment puts each sample under the original dense key `s` with sign-permuted same-small error:
```
  σ_gd(B') + σ_gd(A') * s = σ_gd(e) (mod 2^468).
```
The coefficient signed permutation preserves the sampled bounded discrete Gaussian distribution and fixed-weight ternary secret. Uniformly random masks modulo q520 remain uniform modulo q' after reduction, assuming source's independently generated uniform limbs. No onehot summation, no β knowledge, NO gaussian sigma sqrt(radix) growth, no new cryptographic key generated. This does not rely on a known plaintext attack beyond standard RLWE and does not prove key-recovery feasibility at the target parameters.

**Source-shaped count:** h32, group candidate total 4+4+4+3=15 =>480 HMux key GGLWE objects, each first row 2 independently sampled input gadget columns => **960 q2^468 known-zero RLWE ring samples** at source nominal sigma3.2 under publicly aligned common dense secret. Further gadget rows have lower message-shift widths (416,...,52) and also can be publicly projected, but are dominated by higher 468-bit modulus for this first specific parameter-screen. Independently sourced masks and distinct GLWE rows ⇒ no forced reuse; full real sampling correlations and uniformity require a compiled backend confirmation.

## Executed minimal test [PASS]

Local stdlib script `/mnt/data/ship_i239_direct_gadget_projection.py`, SHA256 `56b0f5e3e99e18b89992948bbe58f30826d692e498526c31a69149ada8914337`; JSON `/mnt/data/ship_i239_direct_gadget_projection.json`, SHA256 `b42865947bf98463eb56f801fd3e2588bcd9c6f85122f204ea8b83f8ca22e3ec`. Executed exact negacyclic `R_(2^32)` degree16 with base2k8/dnum3 +8-bit guard, first-row `G_0=2^24`; 24 trial batches ×16 supports×4 public g candidates×2 gadget columns = **3,072/3,072 exact publicly reduced known-zero sample phase equations PASS** under nonzero ternary secret, independently sampled uniform masks, β chosen independently **without onehot**, error coefficients drawn from rounded gaussian σ3.2 clipped abs19. Observed max abs error13. Toy uses s only to SAMPLE/encryption and privately verify phases; public reduction algorithm does not know s. This validates integer-ring algebra for same structure but NOT actual source prepared DFT, full N or a real key recovery.

## Security outcome and exact limitations

At **the extracted sample's matching nominal sigma**, the 2026 rotated-primal-hybrid 128-bit *reference table* for N2^14,h192 says threshold logq367, whereas our public sample has logq468 (**+101 modulus bits**). This is **strong evidence that the illustrative N16384/HW192 source-shaped evaluation key width should NOT be claimed λ128-secure**, but the table cannot directly certify a lower attack work factor on the *actual* secret and sample distribution because:
1. Dumezy's estimator assumes **96 positive+96 negative** ternary coefficients (fixed split). Poulpy samples exactly 192 nonzero positions but independent random ± signs. Conditioning changes distribution. A corrected mixed-sign-count attack estimate is needed.
2. Rotated primal-hybrid helper's default `m=oo` treats sufficiently many LWE samples as available. Here 960 **ring** samples are produced, each unpacking into N structured LWE equations; finite m vs optimized lattice dimension/independence requirements not yet checked. Do not equate 960 ring samples to 960 scalar LWE samples or assert unlimited oracle.
3. Poulpy error is clipped ±19, while estimator assumes its own `ND.DiscreteGaussian(stddev=3.2)`. Physical DFT/IFMA encryption roundoff and q-alignment not measured.
4. The original SHIP authors **did not use this illustrative q520 denseHW192 key layout** for their security-evaluated paper parameters; the earlier 44.54GiB baseline is not a secure baseline until properly reparameterized.

These are NOT reasons to disregard the q468 extraction; it is an exact explicit model reduction and an immediate mandatory security gate. They are reasons to avoid claiming a proven IND-CPA break, practical secret recovery, a precise <128 bit attack cost or a publishable vulnerability. The original HMux key security includes conventional high-modulus evaluation-key considerations even without onehot; direct projection is elementary prior art (modulus projection of gadget-scaled encryption), not an invented cryptanalytic algorithm.

## End of iteration

**STATUS:** **PASS** precise publicly extractable q2^468 sigma3.2 RLWE family from source-shaped first HMux gadget rows, both cols; **PASS** 3,072 exact toy ciphertext checks and exact source/table parameter audit; **FAIL** I238 premise that a matched-noise security analysis *requires* sigma6.4 summed samples; **UNCLEAR / NOT COMPUTED** concrete attack cost on actual fixedHW192 independent signs/finite samples and real compiled source. **Not a security-certification result or a break of original authors' SHIP.**

**RESULT:** 960 first-row high-modulus HMux samples in unmodified third-party Poulpy layout project publicly to zero-message RLWE under dense HW192, q2^468, nominal sigma3.2 without onehot or noise growth. The published rotated-primal-hybrid threshold logq367 for N16384/HW192 sigma3.2 creates a strong parameter mismatch warning, though finite-sample and ± sign-count assumptions require independent exact estimator verification. Security-matched memory comparisons I203–I238 remain blocked until parameter certificate. This is a better source-based audit than another HMux key-compression variation.

**NEXT_TEST (only on PI continue, SHIP-I240):** run/mod the 2026 rotated-primal-hybrid estimator with (i) actual fixedHW192 but independently random sign count, (ii) ≤960 independent RLWE ring samples (the estimator's effective m), (iii) clipped sigma3.2, at N16384 q468; obtain ATTACK FAMILY and log2 estimated bit work, or explicitly SOURCE_BLOCKED if Sage still unavailable. As prerequisite, byte-level source IFMA test of top row q reduction would address representation error. Do NOT assert a practical attack or novelty without matched run. Also consider security matched N and original SHIP author's parameters; PI owns decision to PARK overall crypto key compression branch.

**STATE_UPDATE:** YES detailed finding and root/topic checkpoint only, read back; no other research lines modified.
