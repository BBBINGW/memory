# SHIP-I227 — Binary GGSW control + shared ordinary rotation keys: source-shaped key-memory/cost and prior-art gate

Date: 2026-10-15. PI explicitly resumed SHIP after CGS PARK and requested continuation. This is the first new technical SHIP iteration after I226; I226 and earlier evidence preserved. Subject: SHIP Cheon–Hanrot–Kim–Stehlé, EUROCRYPT 2025, ePrint 2025/784, original source paper and independently pinned Poulpy IFMA implementation.

## ONE primary hypothesis and cheapest decisive test

**H227 [FALSIFIED for this exact representation/cost contract]:** With the pinned source-shaped real SHIP N=16384, h=32, theta=4, radix groups [4,4,4,3], k_ct=468, base2k=52, dnum=9 and prepared IFMA key_size=10 limbs, replacing per-support, onehot radix-choice HMuxRot GGLWE keys by two GGSW-encrypted binary control bits per group plus shared ordinary rotation/automorphism KSK per bit position will (i) preserve ideal blind-rotation functionality, (ii) reduce the *complete* eagerly retained prepared-key payload by at least **50%**, and (iii) not increase the count of online gadget-product applications. This is a conjunction: failure of either cost gate kills H227's claimed memory/work advantage. It does NOT purport to prove infeasibility of every binary packing, optimized GGSW, new radix architecture or alternative protocol.

**ONE CHEAP DECISIVE GATE:** Derive the complete SAME-WIDTH prepared key matrix dimensions and number of group bit positions, then count GGSW external products and separate ordinary automorphism key-switch products. Verify the ideal algebra with exact small-ring noiseless ciphertexts to ensure cost corresponds to the intended functionality. Do not launch an expensive implementation for an already-known binary CMux pattern with a failed claimed Pareto point.

## Original-source/prior-art check (before novelty claims)

- Original Cheon–Hanrot–Kim–Stehlé *SHIP*, ePrint 2025/784, mirror full 33 physical pages sha256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, **VERSION_UNVERIFIED**. Original §4.2 physical pp19–20, Definition 1/Lemma 2/Algorithm 3 **already develops binary BRotMux using two HMuxRot per bit**. §5.1 physical pp23–24/Algorithm 5 adapts gadget decomposition and B-way HMux, using hoisting and radix B>=3 to reduce practical costs. Thus generic binary blind rotation and key-switched encrypted selection are NOT a new SHIP principle. Text extracted from cached original, official PDF visual rendering was not available in this session.
- Generic GGSW/CMux binary selector is established FHE technology (e.g. publicly documented TFHE blind rotation; Zama TFHE Deep Dive Part IV https://www.zama.org/post/tfhe-deep-dive-part-4 and existing Poulpy GGSW/CMux support). Nothing in our implementation-free algebra proves original cryptographic novelty.
- Independent third-party `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf` (**NOT author HEaaN**), source at that exact commit via GitHub connector:
  - `poulpy-ckks/src/reference/ship/mux.rs`, blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: currently hoisted B-way per-digit `ship_mux_rotate`, one rank2 HMux VMP and candidate post-automorphism each, one IDFT/normalize for the whole digit.
  - `poulpy-core/src/layouts/prepared/gglwe.rs`, blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: `GGLWEPreparedFactory` prepared VmpPMat dimensions N*dnum*rank_in*(rank_out+1)*size.
  - `poulpy-core/src/layouts/prepared/ggsw.rs`, blob `a287a148567ecee920a89f463ba95b6a08241697`: `GGSWPreparedFactory` prepared VmpPMat dimensions N*dnum*(rank+1)^2*size.
  - `poulpy-core/src/layouts/ggsw.rs` describes rank1 GGSW (2x2 encrypted gadget matrix).
  - Prior I208 identified ordinary automorphism KSK under rotated dense secret matching proposed shared key, but original SHIP bundle does NOT contain this ordinary non-conjugation KSK set.

## Ideal functional derivation [DERIVED, not source implementation]

For `ct=(a,b)`, decryption `b+a*s=m` in `R_q=Z_q[X]/(X^N+1)`, let `sigma_g` implement public CKKS slot rotation `r`. Apply `sigma_g` to both ciphertext components (now under `sigma_g(s)`), then a separate ordinary `KSK_{sigma_g(s)->s}`; denote the result `C_r`, decrypting to `sigma_g(m)+e_KS`.

For binary hidden control `beta`, store `GGSW_s(beta)`; define
```
F_(beta,r)(C) = C + ExternalProduct( GGSW_s(beta), C_r - C ).
```
At zero noise, decryption = `(1-beta)m+beta*sigma_g(m)`. Two powers per radix digit, `d=b0+2*b1`, compose `F_(b1,2w)∘F_(b0,w)` to obtain rotation d*w. Across four groups `w=[1,4,16,64]`, all mixed-radix digits `d0∈[0,3],d1∈[0,3],d2∈[0,3],d3∈[0,2]` represent 192 high positions. The original source uses a low theta part separately; this is only the source-shaped high-digit mux replacement, not a replacement of full bootstrap.

**Source-shaped encrypted-domain caveat:** the actual runtime operations need ciphertext delta, automorphism KSK and GGSW external product at proper torus precision/gadget layout, with all key domains and metadata matched. The above is a correct *noiseless functionality* derivation only; actual CKKS level/noise/precision cannot be inferred from it.

## ONE executed exact check / full conditional same-width key cost

Tested exact ring `R_257=Z_257[X]/(X^16+1)` with nonzero s= X−X²+X⁵, fresh randomized *noiseless* ciphertext encrypting an arbitrary ring message, and valid randomized noiseless 1-row ordinary rotation keys and 2-row rank1-GGSW bit keys (plaintext messages beta*s and beta). For each of all 192 legal high mixed-radix positions, separately compose 8 binary CMux gates and compare full coefficient decryption to `sigma_(5^j)(message)`. **192/192 exact PASS**. This does not independently validate the source's 16384-degree IFMA backend, real security, GGSW sampling or noise.

Same pinned arithmetic as I203:
- Each source HMux prepared rank2 switching key `N*9*2*2*10*16=90MiB`. Original `h*(4+4+4+3)=32*15=480` keys, HMux **42.1875GiB**; other prepared key payload **2.34765625GiB**; baseline **44.53515625GiB**.
- Each rank1 prepared GGSW bit key is also `N*9*2*2*10*16=90MiB`. Four radix groups need two bits each (including base3 with forbidden digit 3), hence `32*8=256` GGSW keys = **22.5GiB**.
- One shared ordinary rank1->rank1 rotation KSK per binary position has prepared `N*9*1*2*10*16=45MiB` (no assumption original keyset contains it). Eight public rotation amounts `1,2,4,8,16,32,64,128` in high-digit units → **8*45MiB=0.3515625GiB**. Matching true g/rotation mapping requires actual source integration.
- Other source selectors/tensor/conjugation/D2S held unchanged **2.34765625GiB**.
- **FULL CANDIDATE = 22.5+0.3515625+2.34765625 = 25.19921875GiB**, saving **19.3359375GiB = 43.4172441%**. Thus the claimed ≥50% prepared payload reduction FAILS even with optimistic unchanged gadget widths and all controls kept as regular rank1 GGSW. The 25.199GiB is a conditional eager-prepared payload, NOT process peak RSS / actual implementation key size.
- Original online rank2 HMux VMP applications `32*(4+4+4+3)=480`. Candidate per bit must compute ordinary rotated-and-switched branch **and** GGSW external product: **256 rank1 rotation-KS applications +256 rank2 GGSW products =512 total gadget products**, before differences/additions. Ratio 512/480=1.0666667 count only. Rank1 and rank2 work not equal, hoisting/batching/FFT/normalization differ drastically: do NOT claim candidate time is +6.7%; no actual low-noise analysis. Also eight serial conditionals per support vs four hoisted source radix groups, potentially critical to latency.
- **Security:** new KDM/joint-key distribution includes `GGSW_s(secret_offset_bit)`, ordinary auto keys for nontrivial g, plus existing source eval keys. It is not publicly derivable from source SHIP keys and is not covered automatically by standard IND-CPA. Source I210/I216 unresolved; original params are not a security-matched 128bit claim.

Reproducibility: `/mnt/data/ship_i227_binary_cmux_gate.py` SHA256 `f2319f9206fb693421520b673c08dcca89a5bc3a82519f94f0e88af599f720f3`; `/mnt/data/ship_i227_binary_cmux_gate_results.json` SHA256 `bfc5bacc81f987cb81b4fdb9f658e8065fea04070ed1041ebab7818655f0babf`. Tool execution completed and exact assert passed. These local artifacts are not Git-committed or real Rust tests; all formulas are reproduced above.

## Research contribution judgment and next gate

**STATUS:** FAIL H227 50%-saving/nonincreasing-product conjunctive target; PASS exact noiseless CMux+rotation functionality and source-shaped prepared-byte calculation. **NOVELTY NOT VERIFIED / likely low novelty**, as source already has binary BRotMux and ordinary GGSW CMux precedes this. **NO source SHIP bug** and **NO new secure replacement construction**.

**RESULT:** A naive binary-GGSW/ordinary-rotation reorganization can, in a conditional byte-only model, cut memory by ~43.4%, but it moves rather than removes hidden-control cryptographic work, loses source radix hoisting, requires new correlated keys and is not a credible standalone cryptography novelty in this formulation. It does NOT dominate I207 by modeled memory (I207 conditional ~81.45%) or prove better runtime.

**NEXT_ACTION:** PARK this exact ordinary binary-CMux transplant, do NOT do parameter micro-sweeps. PI decision gate: to continue SHIP *cryptographic* memory research, first name ONE mechanism that genuinely compresses/fuses the GGSW/rotation-key representation **without** reintroducing 2 rank2/1 gadget operations per bit or an unproven security change; require a specific expected memory/runtime frontier and cheapest source-backed falsifier. If none can be specified, PARK SHIP cryptographic branch and select another FHE composition gap. Any purely systems key-streaming branch remains separate and prior-art/benchmark blocked (I222–225).

**STATE_UPDATE:** YES new finding plus topical and root checkpoint only; preserve I226, CGS PARK and all unrelated history.
