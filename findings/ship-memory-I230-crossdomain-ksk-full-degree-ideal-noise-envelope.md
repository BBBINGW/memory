# SHIP-I230 — Full-degree source-shaped ideal-torus noise envelope for I229 HMux one-hot completion

Date 2026-10-15 (Asia/Tokyo); independent SHIP I230 after I229. PI said continue. Scientific parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT2025 / ePrint 2025/784. Original PDF acquired with Research MCP, GitHub mirror **VERSION_UNVERIFIED**, 33 pages, PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`; physical p23 §5.1, Algorithm5 HMux gadget keys and p24 B-way mux; no claim this third-party backend is author's HEaaN.

## ONE primary falsifiable claim and cheapest decisive test

**H230:** For I229's fixed **corrected key-domain** onehot completion at the source-shaped third-party Poulpy IFMA parameters `N=16384,h=32,denseHW=192,theta4,group bases [4,4,4,3],B=2^52,k_ct468`, the *additional* direct Gaussian encryption-key sample errors and unavoidable ideal coefficient-grid normalization after publicly switching gadget rows across secret domains **already exceed** an illustrative `2^-18.1` complete-output numerical tolerance, even with an exact convolution backend. The source-modulus guard matters; tiny-ring unguarded tests are not decisive.

**One decisive test:** Derive a conservative deterministic max-coefficient error bound from the pinned GGLWE source parameters with `|e|<=19`, `N=2^14` arbitrary negacyclic convolutions, `||t||_1=192`, appropriate 52-bit key guard and 520-bit source-row resolution. Propagate through all 4 HMux groups, worst-case CKKS slot evaluation `||Eval(f)||<=N||f||_infty`, scale 40, `h=32` ideal bounded product-tree leaves, and final real conjugation. No Gaussian Monte Carlo or tiny toy replacement. Bound is conditional on ideal exact torus gadget/DFT arithmetic except for coefficient normalization; NOT an actual complete CKKS correctness/error theorem.

## Read-before-write and exact source evidence

- `findings/ship-memory-I229-onehot-completion-cross-keydomain-gate.md` has the algebra, named I229 scheme, 23.5396% conditional prepared-key-byte saving, 6336 *preprocessing key-row-to-key-row* KSK operations, and unproven security/novelty.
- `findings/ship-memory-I215-full-degree-row11-rounding-envelope.md`, `findings/ship-memory-M04-source-gadget-noise-bound.md`: earlier source-shape precise-noise analyses with narrow ideal-rounding assumptions; do NOT treat as actual compiled precision.
- **Pinned independent third-party `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`**, NOT original HEaaN:
  - `poulpy-ckks/src/layouts/ship/keyset.rs`, blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `hmux_rot_key_encrypt_sk` 351–413: input `(beta*s,beta)` under `t_d=sigma_(g_d^-1)(s)`, with `dnum=ceil(k_ct/B)=9,k_aux=B=52`, so row physical `key.k=9*52+52=520`.
  - `poulpy-core/src/reference/encryption/gglwe.rs`, blob `499c7b22daace7b74428d945a5fca808a07d0`: each GGLWE row randomized GLWE encryption of gadget message, encrypted at its source key physical precision.
  - `poulpy-core/src/noise_distribution.rs`, blob `e231917a72be54a5e8dca47ece9f7d8672828020`: `Noise::ENCRYPTION` Gaussian sigma3.2 **truncated** to `|e_i|<=19` at the integer key grid.
  - `poulpy-core/src/reference/keyswitching/glwe.rs`, blob `67fd537f256687a95bf1c7c719392a0d49fe5827`, `glwe_keyswitch_reference` 497–620: prepared gadget multiplication and source body copy, IDFT and normalization at result precision. For input original row `k=520`, source-form rank1 cross-secret KSK has `D'=ceil(520/52)=10` and `k_aux=52` ⇒ physical key precision **k'=572**, returned row still k520 (with output secret t_ell).
  - `poulpy-ckks/src/reference/ship/mux.rs`, blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: rank2 input DFT, `B` key VMP+candidate Galois, sum followed by output `vec_znx_big_normalize` at current accumulator precision.
  - `poulpy-ckks/src/reference/ship/bootstrap.rs`, blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: four mux digit groups per one of h32 leaves then h+1 leaves product tree and root+conjugate; `ShipPlan::raised_k(52)=468`, source mask active k428.
  - `poulpy-ckks/src/test_suite/mod.rs`, blob `e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb`, BASE52_PARAMS_F64 dense secret fixed ternary **HW192**, base52. **N=16384 is a source-shaped manually specified setting, NOT the test-suite default N=256**. Neither high-key modulus nor secret distribution is established 128-bit secure by the generic parameter guideline (I216).

## Conservative exact bound [DERIVED under explicit ideal arithmetic assumptions]

Use normalized torus coefficient unit where a fresh encrypted evaluation-key row at physical k has sampled error `e*2^-k` with `|e|<=19`. At each ring coefficient, product of two polynomials has <=N negacyclic summands. Bound radix digit absolute coefficients `|d_i| <= B-1`, `B=2^52`. Output secret Hamming weight H=192 ⇒ decryption error from independently normalizing mask and body each to k bits, using **conservative <=1 output-grid-unit** per coefficient (NOT claiming backend nearest rounding), at most `(1+H) 2^-k`.

I229 key-to-key switching a source HMux encrypted gadget *row* under t_d from k520 to t_ell at same k520, via 10-digit auxiliary-guard rank1 KSK at k572, gives one switched row's *additional* coefficient torus error:
```
E_switch = N*(10)*(B-1)*19*2^(-572) + (1+192)*2^(-520).
```
In destination k520 integer units: `2^520 E_switch <= 3,113,153` (exact supremum under the chosen digit and truncation bounds). The original row's fresh error remains <=19 in the same units.

Missing `ell=b-1` HMux rank2 row is constructed from one fresh unconditional Enc_(t_ell)(G_i*s) with |e|<=19 plus (b-1) switched source rows. By triangle inequality:
```
E_rec(b) <= 19 + (b-1)*(19 + 2^520 E_switch)
```
in k520 integer units, for BOTH gadget columns conservatively. For b4: `E_rec<=9,339,535` ≈2^23.155 units; for b3: <=6,226,363 ≈2^22.57 units. The second constant column can be public trivial and has less unconditional base noise; bound conservatively includes it.

Input masked accumulator active `k428`, and each of 4 radix groups produces at most D_hmux=9 digit rows, two input columns. Each group with b original candidates replaced by (b-1) source rows and one missing reconstructed row contributes key-sample decryption coefficient error at most
```
 E_group_key_coeff(b) <= N*9*2*(B-1) * ( E_rec(b)+(b-1)*19 ) * 2^(-520).
```
Each group's final accumulator normalization at k428 further contributes <=`(1+192)*2^-428` torus coefficient error in this *ideal normalization* model. A source candidate Galois automorphism permutes coefficients with signs and thus does not increase coefficient sup-norm. The ideal one-hot MuxRot is a permutation of CKKS slots, thus propagates already accumulated **slot** error without additional slot sup-norm amplification. Upper bound canonical CKKS slot error by `2^40*N` times coefficient torus error, summing all 4 groups. This includes *every candidate key's sample error*, not just new switched keys:
```
 delta_leaf <= 2^40 * N * sum_{b in [4,4,4,3]} (
   N*9*2*(B-1)*(E_rec(b)+(b-1)*19)*2^-520
   + (1+192)*2^-428
 ).
```
This is a deliberately pessimistic coefficient-sup-norm then slot transform bound, conditioned on exact gadget/automorphism arithmetic, key error support and one output-grid-unit normalization, *not* a bound on unrelated CKKS masking/intermediate error. `delta_leaf <= 2.030185251972566628e-110 ≈2^-364.3905`.

Assume ideal SHIP product factors `|f_j|<=1`, and original remaining operations are exact except the specified key+group normalization. For h32 perturbed factors, real root+conjugate perturbation is
```
 E_output <= 2*((1+delta_leaf)^32 - 1).
```
Executed `fractions.Fraction` plus 170-digit Decimal arithmetic:
- **Full-degree bound on candidate sample+group-normalization contribution:** `E_output <= 1.299318561262442642e-108≈2^-358.39047906`.
- Difference against an **independently randomized** original HMux key realization cannot simply subtract error bounds; a proper triangle-inequality bound on both noise realizations (including group rounding twice) yields `E_difference <= 2.583359702659838342e-108≈2^-357.3990`.
- Illustrative reference tolerance `2^-18.1 =3.55923840155e-6`, **NOT a proven bound for this source test plan**. The full specified candidate error contribution is ~340.29 bits smaller than this scale.

**Reproducibility:** `/mnt/data/ship_i230_noise_envelope.py`, script SHA256 `15e6077a6b2b9ed1ebe8453e143937ba8cb9f6d97e16fc360e174991c9ff5c31`; `/mnt/data/ship_i230_noise_envelope.json`, JSON SHA256 `97c0c1e5b778a8b1c7b9c0e026358551acc8ccf09d282aefcd14b7cb7b9b3cb6`. Script executed with rational assertion checks and emits all intermediate quantities. One preliminary calculation omitted the **output normalize** errors of every group and produced a smaller bound ~2^-364.8 *after* product; it was superseded by current conservative **2^-358.39**, which does include group normalizations. No compiler, no real ciphertexts, no FFT/NTT backend measurements.

## What this does NOT prove [OPEN]

1. Backend `VmpPMat` DFT / IFMA fixed-point/FFT errors and long-limb arithmetic, real rounding semantics or potential precision loss across key switching at physical k572 and HMux operations k520/428 were **not modeled**; a backend numerical execution could independently invalidate correct source-torus idealization.
2. Original SHIP masking/encoding error, noise from earlier encapsulation, CKKS full product-tree relinearization/tensor and conjugation keys, accumulated precision, failure probabilities and all implementation-specific errors are omitted. The result is not a proof that original baseline achieves 18.1 bits, nor that I229 safely preserves baseline precision in a full run.
3. Joint security of 11 extra cross-secret KSK and 4 unconditional keys correlated to original hidden selectors/dense secret, security-matched k572 and fixedHW192 parameters, and advantage of **23.54% source-shaped stored prepared bytes vs 6,336 key-to-key switching preprocessings** remain unverified. Not an implementation or cryptographic novelty proof. No source SHIP bug or attack established.
4. If producing a *prepared* omitted HMux from switched raw rows requires retaining large intermediate buffers, the 23.54% resident prepared payload saving may disappear; no measured peak RAM or latency.

## End of I230

**STATUS:** **FAIL H230** claim that **ideal source Gaussian samples + bounded coefficient normalization alone** exceed reference precision; **PASS a full N16384 source-shaped analytic upper bound** for exactly these two error families; **UNCLEAR** physical backend accuracy, total bootstrapping error, joint security, real memory/runtime and novelty. HUMAN_REVIEW parent.

**RESULT:** I229 is NOT noise-forbidden by these ideal key-sample/normalization mechanisms even when the reconstructed b4 row error grows to ~2^23.15 *at a 520-bit integer grid*. The remaining decisive blockers are runtime/prepared-peak after 6,336 KSK recomputations, actual IFMA precision and security of the augmented high-q key distribution. Treat ~2^-358.4 as a **term-specific upper bound** only, not a true operating precision.

**NEXT_TEST:** Before any I231 small toy repetition, run one **source-shaped economics/novelty decision gate**: is it even plausible that on-demand rebuilding 128 omitted prepared keys via 6,336 high-q KSKs can improve an end-to-end memory/time Pareto curve at realistic reuse B, or does eager recreation restore/worsen original peak footprint? If a real Poulpy runner is not available, use exact key-material I/O, persistent-versus-ephemeral prepared memory, count/prep complexity and an explicit reuse threshold, then PARK/HUMAN_REVIEW rather than inventing timing. Alternatively a source/parameter-specific augmented-key security theorem would justify deeper numerical work. PI decides any pivot.

**STATE_UPDATE:** YES finding + root/topic checkpoint, no overwrites, reread verify.
