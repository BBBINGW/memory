# SHIP-I256 — Galois-Fourier amortization within each SHIP leaf succeeds, but product-tree global sharing fails algebraically

Date: 2026-10-16. Active fixed PI track SHIP only, one primary falsifiable hypothesis, one cheapest decisive test. Follow-up to I255 (native 2-adic Galois-Fourier scalar eigenbasis impossible), I254 (simple single selector ring multiply), I249 historical contribution readiness. No pivots to CGS/VFHE/EXPLORE. GitHub Notes read_repo_file remains broken (returns {} for known research files), but list_repo_files works; avoid touching shared STATE/older findings without read-before-write. This standalone failure archive is to be written and listed back.

## H256 primary hypothesis, falsification and minimum test

**H256:** A *single* Galois-orbit Fourier basis transformation on the SHIP bootstrap ciphertext can be amortized over **all h support leaves and their product tree**, allowing the secret-selected rotation by packed spectral multiplication everywhere, without restoring the original CKKS ring multiplication or adding a new cross-frequency nonlinear multiplication and new general automorphism keys.

**Falsifier:** The source SHIP implementation materializes separate independently masked leaf ciphertexts and then multiplies them using native CKKS ciphertext products; its required ring plaintext multiplication **is not preserved by orbit Fourier transform**. Find one exact unit input counterexample `U(1*m) != U(1)⊙U(m)` in a valid splitting cyclotomic ring, while verifying the within-leaf Galois diagonalization itself succeeds. A second cost note comparing per-group vs per-leaf transforms is *within the SAME gate*, not a separate hypothesis.

## Source evidence [FACT, pinned]

The *independent third-party* `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf` is not original SHIP HEaaN, and N16384/h32 examples here are not the original author h31 security-certified parameters. Source read directly via GitHub connector:
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob **edbec7d8ad60493d53aa5c11c842da1f30cff542**, lines 137, 172–193: `halves=2 if complex else 1`; for each support j and half, compute `ship_masking_accumulate(acc,...)` then iterate **four consecutive** `ship_mux_rotate(acc,group)` without intervening per-group masks. Each j, half yields **a separate leaf**.
- Same `bootstrap.rs` lines 196–211: following all supports, the algorithm forms a binary `product tree` of the leaves using **real CKKS ciphertext-ciphertext multiplication** `module.ckks_mul_into(... keys.tensor_key())`. This part is NOT a linear rotation/select-only map, and is not free in a new Fourier representation.
- `poulpy-ckks/src/reference/ship/mux.rs` blob **e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce**, lines 65–169: each group hoists once, does a key-specific VMP per candidate and a public DFT-domain automorphism. This is a **native NTT of key/ciphertext coefficients**, not the extra *Galois-orbit Fourier across CKKS slots* used in H256.
- `poulpy-ckks/src/reference/ship/masking.rs` blob **91ba98e08ea7172b34c492d9fcc69ef18628820d**: masking uses ciphertext×plaintext convolution and constructs a separately masked acc for each support.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob **8be6ab92846168330100efeabe9fa19dbd9720e4**, lines 509–531: four source radix groups `[4,4,4,3]` with publicly fixed θ-weight rotations `4,16,64,256` and 480 key objects across h32.
- I255 `failures/ship-memory-I255-native-torus-spectral-packed-selector-root-obstruction.md`: no invertible scalar native Z_(2^k) eigenbasis for source σ_(5^4); odd-prime or complex representation possible but adds other costs/security assumptions. The complex/odd-prime toy here does NOT refute native torus obstruction.

## One exact mathematical gate [DERIVED]

Under a chosen odd prime `q≡1 mod 2N`, CRT evaluation identifies `R_q=F_q[X]/(X^N+1)` with `F_q^N`, where **ring multiplication = coordinatewise multiplication of evaluation slots**. An odd Galois automorphism `σ_g` PERMUTES these CRT slots according to `t↦gt mod2N`.

Let `U` be the normalized Fourier transform across *orbits of this slot permutation*. The Galois action becomes diagonal in U coordinates; a sequence of onehot choices over four groups becomes product of spectral scalars. **This is a valid per-leaf algebraic optimization**. But `U` mixes distinct CRT slots and is NOT a plaintext ring homomorphism: `U(1)=(1,0,..0)` in each nontrivial orbit, not the all-ones vector which is the unit for coordinatewise multiplication. For any `m` with nonzero orbit-frequency, `U(1*m)=U(m)`, whereas `U(1)⊙U(m)` erases the non-DC frequencies. Hence `U(x*y) != U(x)⊙U(y)` generally. A native CKKS ciphertext multiplication tree cannot simply remain in U and multiply coordinates pointwise. It must **inverse-transform leaves** or replace the product tree with a special frequency mixing convolution (and analyze FHE nonlinear cost + keys); a single U at whole-bootstrap input and a single U^-1 at its final output are not sufficient in this representation.

## Exact actual test (executed)

Source script `/mnt/data/ship_i256_global_fourier_product_tree_gate.py` SHA256 **26a389ca67d6c5673c5110c019d9f63e08b990f5297e8937dabda2de822c42fc**. JSON `/mnt/data/ship_i256_global_fourier_product_tree_gate.json` SHA256 **a31d193ae2194c7ee7b1131efc3e4af6f6d8e30e550a54e9d1e4e7139c8eb65b**. Executed locally in standard-library Python:
- Toy **N128, q12289** with primitive 256th root `ζ=8340`, Galois `g=5^4 mod256=113`. 128 odd CRT evaluation slots form 8 disjoint orbits of length 16 under σ113; normalized 16-point FFT `U` well-defined over F12289.
- **160/160** independently chosen random four-group onehot shifts (scaled toy weights [1,2,4,8], not original large-N weights) yield exact agreement between direct four sequential Galois slot permutations and `U^-1(diag(λ_1...λ_4) U(v))`.
- **12/12** exact random negacyclic ring polynomial products agree with coordinatewise CRT evaluation-slot products.
- **160/160** random nonconstant slot vectors witness `U(1*y) != U(1)⊙U(y)`; exact algebra and U inverse checked.
- Not a Rust IFMA compilation, encrypted FFT, secret-security proof or practical CKKS approximation/noise evaluation.

## Corrected cost boundary versus I255 [DERIVED, not benchmark]

At pinned third-party Poulpy source N16384 θ4 radices [4,4,4,3], representative Galois orbits for four weights have lengths **[2048,512,128,32]**, representing **[11,9,7,5]** radix-2 FFT stages respectively; the biggest common basis for g=5^4 has **11** levels. One forward plus one inverse Fourier transform for **each group/leaf**, ignoring special optimizations, gives `2×(11+9+7+5)=64` butterfly-stage instances/leaf. Since **the four groups within a leaf are consecutive and commute**, one common U/U^-1 for that leaf gives `2×11=22` stage instances/leaf, a **65.625% symbolic decrease in NEW Fourier transforms**, not in original SHIP costs:
- **Real mode:** 32 source support leaves: per-group **2048** stages vs per-leaf **704**, difference1344.
- **Complex mode:** source branches `halves=2` and 32 supports → **64 leaves**, per-group **4096** stages vs per-leaf **1408**, difference2688. I255's 2048 count corresponds to REAL one-half mode and should NOT be cited for full complex bootstrap. This is illustrative per-leaf standard FFT counts, NOT actual source native NTT cost, actual keys/RSS/latency or any unavoidable lower bound; CKKS homomorphic FFT needs rotations, plain twiddles, key switching/scale.
- Real/complex groupwise baseline source has 32×15=480 **candidate key applications per half**; in complex two halves key material is reused but **960 candidate applications** happen. Previous records treating 480 as whole-bootstrap calls need qualify "per half". VMP limb work similarly doubles for 2 halves. Source prepared-key storage does NOT double (keys reused).

The source original prepared set only creates general conjugation `p=-1` key, not a full spectral FFT rotation collection; a homomorphic U would need new keys/rotation ops. More fundamentally, even ideal within-leaf Fourier savings are **of a substitute algorithm's newly added work**, not an improvement of native source which already hoists VMP per digit and retains 480 original key objects until a safe alternative is actually constructed.

## End I256

**STATUS:** **FAIL H256 global cross-support/product-tree FFT persistence**, PASS **nontrivial intra-leaf amortization algebra**, PASS exact ring/CRT counterexample and source control-flow audit; UNCLEAR encrypted implementation and novelty/precision.

**RESULT:** No way to amortize single U at whole bootstrapping input and U^-1 at final output while retaining source CKKS product tree's pointwise slot multiplication. Source support-specific masking produces many independently formed leaves. Existing spectral operator per leaf can commute across its four Galois layers, but cannot pass through the subsequent multiplicative tree at zero cost. Corrected complex half counts relative to I255. No credible finished key-memory Pareto improvement or FHE security claim.

**NEXT_TEST:** Suspend further spectrum-only toy variants. Only reopen with an actual efficient homomorphic U keyset/noise model and a valid transformed multiplication rule + concrete amortization across independent leaves that dominates original source VMP/streaming. Otherwise recommend HUMAN_REVIEW/PARK SHIP key-memory line; I245 original author h31-security audit SOURCE_BLOCKED. PI retains final choice, no unrelated tracks touched.

**STATE_UPDATE:** standalone failure archive to commit and list-verify; shared root/topic `STATE.md` not mutated while `read_repo_file` returns empty, to preserve read-before-write.
