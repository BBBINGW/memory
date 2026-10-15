# SHIP-I248 — Correct I247: canonical gadget-digit preparation DOES NOT commute with public one-hot reconstruction

Date: 2026-10-16. User PI said 'continue'; **SHIP ONLY**, no CGS/VFHE/EXPLORE edits. After I247, an audit of a key step rather than proposing an adjacent low-value compression trick. Read RESEARCH_PHILOSOPHY.md, AGENT.md, START_RESEARCH_SESSION.md, STATE.md, findings/ship-memory-STATE.md, findings/ship-memory-I247-prepared-domain-onehot-rebuild-peak-memory-frontier.md and I246, read third-party pinned source. **This finding CORRECTS/QUALIFIES one overbroad technical conclusion in I247**. It is NOT a cryptographic flaw or attack on author SHIP.

## ONE falsifiable hypothesis / one cheapest decisive test

**H248:** In source-shaped Poulpy gadget preparation, the *canonical prepared VmpPMat array* of I246's reconstituted missing scalar-beta column equals the simple linear combination of already prepared candidate columns after public NTT-domain Galois permutations:
```
Pcanonical(T−Σ sigma_rho(C_d)) = Pcanonical(T)−Σ Aut_NTT,rho(Pcanonical(C_d))
```
where `Pcanonical` FIRST converts the modulo 2^k torus ciphertext coefficients into **canonical unsigned radix 2^b limbs** and THEN transforms each limb by NTT/CRT. If exact equal in component RNS-prime representation, one could view the missing prepared column as a drop-in array without digit renormalization/carry management. **Falsifier:** any canonical limb vector of modulo 2^k reconstruction differing from linear combination of source canonical limb vectors. This is ONE representation-semantic test, not a fresh memory-layout/scheduling benchmark.

**Cheapest test:** a small exact base-16 carry witness; execute 144 source-like independently randomized GLWE rows under four distinct automorphed secret domains and their onehot beta selection (both mask and body), compare canonical `P` vs algebraically linearly combined per-limb NTT arrays, and separately check whether both arrays decode to the SAME torus polynomial when weighted and reduced modulo 2^k. No AVX512 runtime, no Sage, no misleading alleged physical-RSS improvements.

## Original sources [FACT]

Pinned *independent third-party* `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, NOT original Cheon–Hanrot–Kim–Stehlé HEaaN/SHIP source.
- `poulpy-core/src/layouts/prepared/gglwe.rs`, blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: `gglwe_prepare` delegates to `vmp_prepare`.
- `poulpy-cpu-avx512/src/ntt3x42_ifma/vmp.rs`, blob `78f8a8494a46964440a12fa2b4adb2fa248ade45`: `vmp_prepare_ifma` accepts a `MatZnx` of signed `i64` limbs, converts each row/col/limb through three 42-bit-prime NTTs, then stores 16-byte packed three-prime residues per coefficient. This **linear-in-already-integer-limbs** stage alone DOES NOT make preceding modulo-2^k canonical radix digitization linear. Source hardware CRT/headroom may support NONCANONICAL signed integer limbs if separately proven and validated; do not assert it cannot.
- `poulpy-ckks/src/layouts/ship/keyset.rs`, blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: source HMux rank2 GGLWE encrypts `(beta*s,beta)` under output `t_d=sigma_(g_d^-1)(s)`; onehot digit selection.
- `poulpy-ckks/src/reference/ship/mux.rs`, blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: stock kernel requires a complete prepared rank2 key for each candidate. No prepared virtual-column API.
- I246 `findings/ship-memory-I246-onehot-scalar-column-public-galois-completion.md`: correct GLWE ciphertext-level `C_beta_ell=T_i−Σ_d sigma_(gell^-1 gd)(C_beta_d)` modulo torus precision q; fresh key ciphertext row errors add, but no new secret-key KSK.
- I247 `findings/ship-memory-I247-prepared-domain-onehot-rebuild-peak-memory-frontier.md`: toy PASS only `weighted inverse NTT of LINEAR prepared arrays mod Q == coefficient domain reconstructed ciphertext` (320/320). It did **NOT compare** `linear_prepared` with fresh `prepare(reconstructed ciphertext)`; its prose asserting `P(C_ell)=sum P(C_d)` for canonical prepared representation is **too strong**, not formally proved. I247 memory FAIL (<=67.5MiB/2.29% group-buffers) remains independent/unchanged.

## Exact small counterexample [DERIVATION, source-type-correct]

Set torus q=2^8=256, radix B=16, gadget scalar T=64, 2 retained ciphertext **public coefficient values** 33,33; the complete I246 radix4 version may take the third value0. Reconstructed coefficient is
```
c=(64−33−33) mod256=254,
D_16(c)=(14,15).
D_16(64)=(0,4), D_16(33)=(1,2).
D_16(64)−D_16(33)−D_16(33)=(-2,0) != (14,15).
```
The weighted integers differ by exactly `-256`, so they describe equal **torus residues modulo q** but different INTEGER limb polynomials. NTT of a given integer limb array is linear over its RNS prime p, not over the composite representation `D_16: Z_256→{0..15}²`. Consequently the two prepared `(per-limb NTT mod p)` arrays are **not equal**, because e.g. constant-coefficient limb `-2` vs `14` differs by 16 modulo p (p large, not 2 power). Borrow/carry correction is mathematically necessary if an API demands the *canonical digit arrays*; it is a nonlinear operation, cannot be replaced by mere field-linear NTT permutations/subtractions without further machinery.

**Narrow representation caveat:** This is NOT a counterexample to modular correctness of a noncanonical higher-range limb representation, nor a proof the IFMA VMP will necessarily return a wrong ciphertext when fed linear-combined prepared rows. If the source CRT/normalization and performance/kernel loops can accommodate the noncanonical values and all intermediate values, the two may still compute identical torus-mod-q results. Such a claim would need a precise range invariant, CRT embedding, key-multiplication semantics, full CKKS precision and a compiled backend test, NOT I247's round-trip assertion.

## Executed exact test [PASS falsifier, retained earlier correctness]

`/mnt/data/ship_i248_carry_counterexample.py` SHA256 **fa68ea28ba8508735611216c0ae1be9464eab62156c8641c520eb3298342907a**; `/mnt/data/ship_i248_carry_counterexample.json` SHA256 **86a2fd8ec9d18bc995914dae2eb60bedff49c9d6d628ab45ca86a4c0b0399028**.
- Ring `R_Q=Z_(2^40)[X]/(X^16+1)`, five base-2^8 limbs, exact 31-bit negacyclic NTT prime p2013265921, Galois [1,5,9,13] under correct output secrets `t_d=sigma_(g_d^-1)(s)`, nontrivial ternary `s`.
- Independent uniform 40bit ciphertext masks, bounded ±19 encryption noises, one-hot beta choices, four ciphertext row gadget weights and 36 repetitions per selection, 144 actual row pairs.
- **288/288** first/second ciphertext component comparisons: directly linearly combined NTT arrays DIFFER from *canonical preparation* of the reconstructed modulo-2^40 polynomial.
- **288/288** linear NTT arrays, when inverse NTT + signed weighted limb interpretation + mod Q applied, reconstruct the **same torus polynomial** as coefficient-domain public I246 expression; preserves the specific weaker I247 PASS.
- **144/144** reconstructed scalar-beta GLWE ciphertexts, decrypted under omitted t_ell, pass ≤(4−1)19 coefficient noise bound.
- Max abs unnormalized signed limb observed **736** while canonical base-256 limb values are [0,255]. This flags range and carry contract verification, not proof of packed IFMA overflows or failed decryption.
- NOT actual source IFMA three-prime packed 16byte VMP; no physical RSS/latency/precision or security work.

## Result & corrected interpretation

**H248 FAIL**: `Pcanonical(T−Σsigma(C)) != Pcanonical(T)−ΣAut_NTT(Pcanonical(C))` as arrays in general; I247 had incorrectly promoted a *mod-Q weighted equivalence* into an unqualified canonical-prepared equality. Formal weaker modular equivalence still PASS; raw secret-domain/key-noise construction from I246 also PASS. Backend directly consuming noncanonical prepared rows remains **UNVERIFIED, NOT disproved**. I247's equally staged memory optimistic best saving 67.5MiB/2.29% and PARK recommendation remain intact, and now cannot be treated as implementable for free even at abstract prepared-array level.

**STATUS:** **FAIL canonical-prepared identity**; PASS exact counterexample and 288/288 +144/144 executable checks; **UNCLEAR noncanonical IFMA safe adoption**. No paper flaw nor novel cryptographic primitive/attack. This is a necessary research-integrity correction rather than an attempt to produce additional small savings.

**NEXT_ACTION:** I246/I247 resident-key compression remains PARK. Do NOT launch I249 to patch this tiny saved-column approach by another digit/carry tweak with no ≥5–10% fair RAM/time opportunity. Revive only with a materially different cryptographic mechanism or objective change by PI. Security of true author SHIP under h31 continues SOURCE_BLOCKED per I245. Explicitly append correction to I247 without overwriting older record. **STATE_UPDATE YES**, failure and original finding addendum + root/topic checkpoint read back.
