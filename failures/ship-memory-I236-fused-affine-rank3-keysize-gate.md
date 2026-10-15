# SHIP-I236 — Fused affine-default B-way MuxRot via rank-3 GGLWE: correct but worse key memory and product count

Date: 2026-10-15 (PI explicitly said "继续"); SHIP evaluation-key memory active. One primary hypothesis and one decisive test. Follows I235. **Failure is of an invented optimization candidate, NOT original SHIP.**

## Primary hypothesis, regime and falsifier

**H236**: At fixed source-shaped Poulpy IFMA parameterization N=16384, h=32, B=2^52 gadget radix, dnum=9, physical key size=10 DFT limbs, four per-support mux digit groups of sizes [4,4,4,3], use affine one-hot default `beta_0=1−sum_{d>0}beta_d` and **fuse** selection `beta_d` with automorphism difference `sigma_g(ct)−ct` inside a single key switching/GGLWE product per nonidentity branch. This should preserve ideal plaintext correctness while (a) avoiding the 352 extra online ordinary automorphism KSK in I234, (b) strictly reducing **total prepared-key payload** relative to original unchanged SHIP, and (c) not increasing online symbolic ring-product slots, without new high-q control keys or expensive offline key re-expansion. Falsify if the direct mathematically correct fused GGLWE requires too many input secret columns, negating key-count savings.

**Cheapest decisive test:** Derive ALL source/target secrets and gadget-message columns; run exact randomized noiseless negacyclic RLWE/GGLWE toy for full onehot MuxRot; calculate prepared VmpPMat dimensions and ring-product slots at the pinned source input sizes. No real Rust runner, no parameter sweep.

## Provenance [FACT]

- Cheon, Hanrot, Kim, Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint **2025/784**, §4.2 binary MuxRot, §5.1 **Algorithm 5** physical p23 and B-way mux p23–24. Original PDF Research MCP GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, 33 physical pages, VERSION_UNVERIFIED. Paper already employs fused B-way HMuxRot. No security flaw alleged.
- Pinned **independent third-party** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, NOT author HEaaN:
  - `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: original `hmux_rot_key_encrypt_sk` rank_in2 rank_out1; source messages `(beta*s,beta)` under key `t_d=sigma_(g_d^-1)(s)`.
  - `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: original uses GGLWE rank2 VMP, public output automorphism in DFT and one grouped IDFT/normalize.
  - `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: prepared `VmpPMat(n,dnum,rank_in,rank_out+1,key_size,PrepareHint::Reuse)` => n*dnum*rank_in*(rank_out+1)*size*16 bytes at IFMA DFTWord16.
  - `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5fca808a07d0`: one independently encrypted row for each gadget input column and digit, general `rank_in`.
- Prior local I234 `failures/ship-memory-I234-onehot-default-gsw-rotation-frontier.md`: original onehot default + rank2 same-key GGSW + standard online automorphism KSK saved bytes but added 352 KSKs. I227 conventional binary route. I235 unsafe shared mask leakage. Baseline I203/I222 source prepared keys and group streaming.
- Standard affine CMux `ct_0+EncGSW(beta)*(ct_1-ct_0)` is established (Zama's TFHE technical explanation https://www.zama.org/post/tfhe-deep-dive-part-3). **No literature novelty** is claimed for the affine identity, GGSW or automorphism. No complete literature proof that this exact rank3 proposal never appeared.

## Constructive synthesis: one rank-3 GGLWE per nonidentity choice [DERIVED]

Convention: source `ct=(a,b)`, `Dec_s(ct)=b+a*s=m` in ring `R=Z_q[X]/(X^N+1)`, `sigma_g(X)=X^g`, `g` odd. The desired plaintext delta is:
```
sigma_g(m)-m = [sigma_g(b)-b] + sigma_g(a)*sigma_g(s) - a*s.
```
Input **three public polynomials** `x=(sigma_g(a), -a, sigma_g(b)-b)` should be paired with encrypted selection-dependent gadget messages **under the one common original output key s**:
```
K^(0)_{d,i} = Enc_s(G_i* beta_d*sigma_g(s)),
K^(1)_{d,i} = Enc_s(G_i* beta_d*s),
K^(2)_{d,i} = Enc_s(G_i* beta_d).
```
For each nonidentity d, evaluate one rank_in3/rank_out1 GGLWE gadget product
```
 D_d = ExtProd_3( x, K_d ) = Enc_s(beta_d*(sigma_g(m)-m))  (ideal modulo q).
```
Output `ct + sum_{d=1}^{B−1}D_d`. Since `sum_d beta_d=1` and `sigma_g0=id`, this decrypts to `sum_d beta_d sigma_gd(m)`, same as B-way SHIP MuxRot. All outputs under SAME dense s and **no separate online ordinary rotation key switching**, extra high-q key, key-to-key preprocessing or ciphertext×ciphertext multiplication. However the ring automorphism and original mask both survive the delta, so one needs BOTH `sigma_g(s)` and `s` as independent *message columns within this direct linear gadget representation*. Their being deterministically related by automorphism does not make their products with separate input `sigma_g(a)` and `a` merge into a single ordinary ring multiplication.

**Narrow one-mask-column obstruction demonstration (NOT a universal rank lower bound):** If one tries a replacement for `sigma_g(a)sigma_g(s)-as = a*t` for all public a, plugging a=1 forces `t=sigma_g(s)-s`, while plugging a=X gives the additional condition `(X^g-X)*sigma_g(s)=0`. For an explicit nontrivial s in `Z_(2^16)[X]/(X^16+1)`, g=5, this is FALSE (exact test). Thus that naive linear mask reuse cannot collapse source rank back to one; other sophisticated transformations/representations are not ruled out.

## Executed exact toy and full-source-shape arithmetic

Script `/mnt/data/ship_i236_fused_affine_rank_gate.py`, sha256 `3e3ed473add5405ca63e813f75a7231949c580532945ba5711f1c7db728d6ec5`; JSON `/mnt/data/ship_i236_fused_affine_rank_gate.json`, sha256 `6b43e983d021572628387a89ce6e3967b0626d53f0bc58566a018d1d63eab271`; executed and asserted 2026-10-15. Exact negacyclic `R_(2^16)=Z/(65536)[X]/(X^16+1)`, ternary secret `s=X+X²−X⁵`, four Galois exponents [1,5,9,13], randomized uniform RLWE masks, base16 four digits, fresh noiseless GGLWE encryption of all **three gadget columns**. **128/128 complete 4-way onehot MuxRot checks and 384/384 nonidentity delta checks PASS**. No Gaussian noise, CKKS scale, physical IFMA backend or KDM/related-key security tested.

Prepared payload and symbolic online work at source IFMA N16384 h32 groups [4,4,4,3], radix52 dnum9 key_size10, 16 bytes per IFMA prepared DFT word, other prepared keys 2404MiB:
```
original count = h*(4+4+4+3) = 480 keys rank_in2,
candidate count = h*(3+3+3+2) = 352 keys rank_in3.
original per key = N*9*2*2*10*16 = 90MiB.
candidate per key = N*9*3*2*10*16 = 135MiB.
original full prepared = (480*90+2404)/1024 = 44.53515625GiB.
candidate full prepared = (352*135+2404)/1024 = 48.75390625GiB,
CHANGE = +4.21875GiB = **+9.47285%**, opposite of H236(b).
original symbolic online ring product slots = 480*9*2*2 = 17280.
candidate symbolic online ring product slots = 352*9*3*2 = 19008,
CHANGE = **+10%**, opposite of H236(c).
```
For same-policy current-group disk-backed raw→prepared staging: original max base4 group `other2404 +4*45 raw+4*90 prepared =2944MiB=2.875GiB`; candidate `other2404+3*67.5 raw+3*135 prepared=3011.5MiB=2.94091796875GiB` (**+67.5MiB** named key buffer). This excludes input temporary 3-column DFT, transform scratch, online input ciphertext/leaf/pi, real peak RSS; likely source's single shared 2-column input DFT cannot be reused exactly because different candidates use differing public `sigma_g(a)`, though FFT-domain permutations could be optimized. Therefore the cost conclusion is already negative **before** extra dataflow implementation overhead.

**Security & novelty:** Candidate uses new correlated GGLWE keys encrypting `beta_d*sigma_g(s)`, `beta_d*s`, `beta_d` under same s, nominal k520. Joint evaluation-key KDM/circular proof is not inherited automatically; fixed N16384/HW192/q520 not 128bit security-matched (I216, I233). No actual compiled backend/latency/error. Simple affine GGSW fusion is not claimed novel. This failure is only of the direct rank3 GGLWE construction; not a theorem that all lower rank fused select-rotate is impossible.

## End of Iteration

**STATUS: FAIL H236 joint crypto-memory/online Pareto condition**, PASS precise ideal algebra and full-source-shape integer bytes/VMP count; security/noise/novelty/runtime UNCLEAR. **RESULT:** Even removing online automorphism KSK from I234, direct fused `beta*(sigma_g(ct)-ct)` needs a third gadget-source column to handle both `sigma_g(s)` and `s`; count saving 480→352 keys is outweighed by rank2→rank3 widening, yielding **+9.47% total prepared key payload** and **+10% online VMP product slots**. Matched streaming peak named buffer also worsens. The direct attempt is PARK; neither source SHIP nor other potential fusion mechanisms disproved.

**NEXT_TEST / PI gate:** Do **not** spin I237 as a simple digit/default rotation, radix or rank reshuffle. At I237 only proceed on credible *rank-2 or lower* fused affine delta primitive using a genuinely different representation (e.g., non-R-linear transform with provable correct secret handling) and explicitly counted security/online cost, or move SHIP crypto-key-memory to PARK if no such primitive. User PI owns overall research pivot. **STATE_UPDATE YES** finding failure+topic and root latest-checkpoint; re-read verification, unrelated branches preserved.
