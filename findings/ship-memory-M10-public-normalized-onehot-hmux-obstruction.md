# SHIP-M10 — Public Galois normalization does NOT repair one-hot HMux-key complement

**Date:** 2026-10-14 (Asia/Tokyo). **Series:** independent **SHIP-M10 COMPLETED, SHIP-M11 NOT STARTED**; distinct from concurrent SHIP I-series and vFHE V-series. PI authorized the M09 next action by “好的，请继续”.
**Original paper:** Jung Hee Cheon, Guillaume Hanrot, Jongmin Kim, Damien Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, §5.1 Algorithm 5. Full mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, `VERSION_UNVERIFIED`. This test specifically checks the **independent Poulpy implementation**, not the authors' HEaaN.
**STATUS:** **FAIL** naive identity candidate key omission via public Galois normalization + onehot subtraction; **PASS** exact algebraic obstruction and randomized toy GLWE witness. **NO novel research gap asserted**: concurrent `findings/ship-memory-I204-hmux-key-domain-obstruction.md` already derived the post-normalization twisted-secret first-row obstacle; M10 adds a noisy-key, source-shaped crosscheck under a favorable shared total key.
**No claim:** SHIP paper flaw, general mux-key count lower bound, impossibility of alternate key-layout factoring, or actual performance/security break.

## Read before write and concurrency

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, M09 `findings/ship-memory-M09-key-major-batched-mux-preparation-gate.md` SHA `223719e11db3b323f411a6ab742640bff821b11e`, M06, shared SHIP `findings/ship-memory-STATE.md` SHA `912b977293cf3b79126bb282f198f2a0f358a8dc` (already concurrently I207), global `STATE.md` SHA `528741fd2b38609fad2547721044474ea9e259cb` (separate vFHE V11), and prior `findings/ship-memory-I204-hmux-key-domain-obstruction.md` SHA `3577c813d212ca1353584d59718a6c22b3639ff8`, plus I207 SHA `2112daf6d81db9808d5d85946613fd0450bfda39` for overlap. **DO NOT overwrite global STATE or concurrently maintained SHIP STATE.** Only new immutable M10 file is written.

Prior M05–M09: prepared rank2 HMux GGLWE dominates estimated memory at source-shaped N16384, h32, theta4; independent seeded compressed keys with stream+key-major batching trade memory for preparation and remain unbenchmarked. Current M10 returns to the next structural key-count problem chosen by the PI.

## Pinned implementation evidence [FACT]

Repo `poulpy-fhe/poulpy`, commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` function `hmux_rot_key_encrypt_sk`: for candidate d and onehot beta_d, source GGLWE rank-in2 secret is `(beta_d*s, beta_d)`; output is `s'_d=sigma_(g_d^-1)(s)`; `g_d=5^((m-(rot_d % m))%m) (mod 2N)` with `m=N/2`; rank-out1. The zero-rotation d0 has g0=1. Real independent GGLWE keys contain randomized encryption noise; nothing here attacks their correctness.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce` performs each candidate's rank2 GGLWE multiplication in its own key domain, applies per-candidate public Galois output automorphism **before** summation.
- `poulpy-hal/src/layouts/module.rs`: Galois generator is 5 on negacyclic R.
- Concurrent I204 record **already observed** that raw key-row affine addition mismatches output key domains, and stated in derived prose that publicly automorphizing each key gives first plaintext beta_d*sigma_gd(s). **M10 explicitly tests** the stronger apparent workaround `K_0'=K_total - Σ_{d>0}sigma_gd(K_d)` using actual randomized GLWE ciphertext row samples and one free reusable total key. It corroborates, does not rediscover a separate contribution.

## ONE primary hypothesis and ONE cheapest decisive test

**[PRIMARY HYPOTHESIS M10]** Even though original rank2 HMux keys have candidate-specific destination secrets `s'_d`, the one-hot constraint `Σβ_d=1` lets an evaluator omit the d0 (identity Galois) rank2 HMux key **without another secret-dependent correction** by publicly normalizing all the remaining keys to s and computing:
`K'_0=K_all-Σ_(d>0)sigma_gd(K_d)`,
where we grant an extra, shared reusable `K_all` encrypting gadget-scaled `(s,1)` under s **for free**. This hypothetical is deliberately favorable to the compression proposal.

**[FALSIFIER]** Find one legitimate ternary s and legal public distinct candidate Galois elements for which the extracted first reconstructed input-secret gadget row does NOT encrypt `β0*G*s` within keygen noise, even though the second row reconstructs `β0*G` and all original individual keys are valid. Test the two one-hot legal secret digit states β0=1 and β1=1 as one control+counterexample with randomized encrypted samples.

### Mathematical obstruction [DERIVED]

For each candidate let `K_d` under `s'_d=σ_gd^-1(s)` encrypt rank2 gadget plaintext rows `G β_d s` and `G β_d`. Publicly applying σ_gd to both ciphertext components changes destination secret to **s** but transforms plaintext rows into `G β_d σ_gd(s)`, `G β_d`. Supposing a reusable `K_all` under s encrypts `Gs`, `G`, then public subtraction has reconstructed plaintext:
```
first: G*(s - Σ_(d>0) β_d σ_gd(s))
second: G*(1 - Σ_(d>0) β_d) = Gβ0.
```
Required first is `G β0 s = G*(s - Σ_(d>0) β_d s)`. Hence systematic first-row error:
```
GΔ = G*Σ_(d>0)β_d (s − σ_gd(s)).
```
Unless secret s is invariant under the selected nontrivial automorphism, this generally is nonzero. Onehot alone constrains only scalar bits, not the transformed secret orbit. Public correction would have to create secret-dependent cross-domain terms, which this candidate explicitly forbids. This does **not** preclude other nontrivial factorizations, new key types, encrypted-β control or extra nonlinear costs.

### Exactly one executed source-shaped random-GLWE witness

**Script (local):** `/mnt/data/ship_m10_onehot_hmux_automorphism_obstruction.py`, SHA256 `0080f0e2de94de4ea57e066c7684e522afc8b6f8e8ea1e70c9e738384cd65916`.
**Results JSON (local):** `/mnt/data/ship_m10_onehot_hmux_obstruction_results.json`, SHA256 `0ddd2f62683631ad461abf2b9a4404541b0399feade742619351eb0eb4020230`. These are sandbox files, not persisted as executable code in GitHub.

Model: `R_q=Z_12289[X]/(X^64+1)`, m32, θ4, first B4 mux group rotations `r_d=4d` with `g_d=[1,17,33,49]` derived directly from pinned code's generator 5; secret ternary coefficient polynomial `s=1+X−X²`; single gadget scalar G128; onehot beta control as d0 or d1 active. Keygen samples random uniform RLWE a polynomial and independent encryption noise `e_i∈{-1,0,1}`, forms `b=message−a*s'_d+e` under each destination s'_d. `K_all` independently encrypts `(Gs,G)` under s. Each input key row is confirmed to decrypt to its intended gadget plaintext within coefficient |noise|≤1.

One test enumerates **two legal onehot states × eight fixed RNG seeds =16 instances**:
- β0=1 **control**: Galois-normalized other keys have zero plaintext, complement K0' has correct row plaintext up to accumulated error ≤4; **8/8 PASS**.
- β1=1 **counterexample**: `σ_17(s)=1+X^17−X^34`, hence `Δ=X−X²−X^17+X^34`, with first row coefficient discrepancies **±128** before noise, while second row still correctly encrypts zero up to ≤4 noise; **8/8 FAIL** missing-key validity.
- Maximum residual random encryption noise on first row after removing analytically predicted systematic error =4 across runs. For β1 test X-coefficient discrepancy observed between 125 and 131; no chance that magnitude 128 comes from the ±4 noise. All 16 original K_d valid. `σ_17` is a nontrivial legal negacyclic automorphism.
- For this narrow public-linear construction, failure already follows from noiseless polynomial algebra. The RNG trials confirm it remains detectable at encryption level, **not** a proof of impossibility under security parameters.

**Limits:** This N64 toy is a source-shaped rotation-group example but not 128-bit security and is NOT a compiled Poulpy CKKS key-switching or full SHIP bootstrap execution. The script tests one representative GGLWE gadget scalar and 2 rank2 input rows, not full dnum RNS, key switching rounding, NTT backend precision, peak RAM, actual throughput, or novelty.

## End of iteration: stop / preserve provenance

**STATUS:** **FAIL** source-form public Galois-aligned onehot key-complement strategy; **PASS** toy randomized RLWE witness and exact derived discrepancy; **UNCLEAR** any broader key-count/rank-reduction research and real benchmark; **NOVELTY NOT VERIFIED**.
**RESULT:** Public alignment repairs mixed destination domains of I204, but breaks the first gadget message via `σ_g(s)`, so the one-hot complement still cannot reconstruct omitted key. This is a **strengthened reproduction of the previously archived I204 obstacle**, not an unrecognized paper bug or new contribution. Avoid repeating this obstruction in a future session.
**NEXT_ACTION (only upon PI continuation, SHIP-M11):** **ONE narrow security/cost gate on a DIFFERENT candidate**, not the already archived I204/M10 complement. The concurrent SHIP **I205–I207** track already formulated 15 shared beta-independent HMux GGLWE keys + 480 independently encrypted beta controls and found a conditional **81.45%** full prepared-payload saving at widened 624-bit modulus, but security distribution and +480 CT×CT operations are **not verified**. Read its latest state and do NOT independently repeat its pending security gate or claim novelty. If a distinct falsifiable source obstruction cannot be named, stop and request PI to choose between compiled validation of seeded-batching M09 or refocusing on entirely new candidate. Human has strategic authority.
**STATE_UPDATE:** YES immutable M10 only, no modifications to global `STATE.md` / concurrent `findings/ship-memory-STATE.md`.
