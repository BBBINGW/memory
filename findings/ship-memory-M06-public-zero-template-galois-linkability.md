# SHIP-M06 — Public Galois-shared zero HMuxRot templates leak the secret rotation digit

**Date:** 2026-10-14 (Asia/Tokyo); **independent SHIP M-series round M06**, NOT vFHE I193 onward or the concurrent SHIP I197/I198 side labels.
**PI authorization:** After SHIP-M05, the PI agreed to investigate **SHIP mux evaluation-key memory** by “好的，请继续.”
**STATUS:** **FAIL** the one-template-with-public-automorphism sharing hypothesis on evaluation-key privacy; **PASS** explicit source-shaped linkability counterexample. No claim of breaking original SHIP or general impossibility of mux-key compression; no novelty claim.
**Target:** Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, §5.1 Algorithm 5, physical PDF pp23–24 and §4.4 Algorithm 4 pp22–23.

## Read before write and branch isolation

Read: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-STATE.md` Git blob `de9b97eac83a5eccdb07c75e09df2a5779b24a16`, `findings/ship-memory-M05-mux-dominates-prepared-key-memory.md` SHA `83afac0b0a9de2c41baa6760710ae50d9cfd5785`, and global `STATE.md` at SHA `db4175bdc29b0fb256a6f4d73d7722a559d749fb` **for concurrency detection only**. Global state belongs to separate vFHE V-series, and SHIP state is concurrently edited by another session using SHIP I197/I198 labels. This round writes its own M06 file only and optionally a separately named M-series pointer; does NOT overwrite `STATE.md` or `findings/ship-memory-STATE.md`.
**Recent parent finding (M05):** For an illustrative source-shaped N16384,h32,θ4, mux-base4, b52,dnum9,dsize1, `CnvPVecL` selector prepared buffers total 2.25GiB but 480 prepared rank2→rank1 HMuxRot GGLWE keys total ~42.1875GiB. Therefore halving selector buffers alone saves no more than 2.53165% of unchanged total evaluation-key prepared buffers. M05 does NOT measure actual RSS and is not original authors' HEaaN.
**ePrint Research MCP:** `get_eprint_paper("2025/784")` cache_hit true; cached 33pp `github-mirror` PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official/latest binary `VERSION_UNVERIFIED`. Read physical pp22–25. On p23 §5.1 Algorithm 5 source describes GGLWE gadget keys for HMuxRot, coefficients encrypting `beta * gamma_i * s(X^{5^j})` and `beta*gamma_i`, and B-to-1 mux as sum `beta_j Rot_j(mu)`. PDF extraction mangles exponent/Greek chars, so exact source implementation below is the authority for indexing/sign conventions. On p24 paper explicitly discusses hoisting (HS18/BMTH21) and bases B≥3.
**Source implementation:** Pinned independent `poulpy-fhe/poulpy` commit `250d4392656cd313f92ca66d96d8865702d39ddf` (not authors' HEaaN):
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` function `hmux_rot_key_encrypt_sk`: per candidate `g_d=module.galois_element((m-(rot%m))%m)`, input rank2 secret `(beta*s,beta)` with beta onehot, and output rank1 secret `sigma_{g_d}^{-1}(s)`; `GLWESwitchingKeyLayout` (rank_in2, rank_out1); even beta0 keys freshly generated in original.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce` — evaluator loops **ALL** public candidate keys in each digit group, does rank2 GGLWE product and applies corresponding public output automorphism; keys cannot simply be skipped by plaintext beta without leaking selector.
- `poulpy-core/src/reference/encryption/glwe_switching_key.rs` blob `20ce62e3791e343958862a2f77de0067c9b27fcc`: GGLWE encryption of each input-secret polynomial under target secret.
- `poulpy-hal/src/layouts/module.rs` blob `9c4b3bd787b93a47b92945df86f1662491812894`: `galois_element(` exponent`) ` built from generator 5, ring cyclotomic order 2N.
- Additional `poulpy-core/src/reference/automorphism/gglwe.rs` blob `a9b57ad6db231a0491aafcb9b54983628022c50c` shows GGLWE automorphism manipulations are nontrivial; it does not implement the candidate sharing proposal.

## Transfer inspiration, non-primary literature

Known ideas: TFHE blind-rotation uses encrypted secret selectors and (G)GSW keys, e.g. survey https://link.springer.com/article/10.1186/s42400-026-00571-w; the 2025 IET NTRU-based bootstrapping work https://doi.org/10.1049/ise2/7097351 explores altering the key representation to cut memory but NOT this SHIP-specific mux key reuse; *Fast Blind Rotation for Bootstrapping FHEs*, ePrint 2023/1564 provides another key-layout example. These are motivation, not evidence a technique applies to SHIP nor a novelty search exhaustive enough for publication.
No other hypothesis tested this round.

## ONE primary hypothesis / falsifier

**[HYPOTHESIS M06]** The zero-valued HMuxRot candidate keys (beta=0) under varying automorphed target secrets can be prepared from a single publicly stored zero-key GGLWE template via the corresponding public automorphism, with the unique beta=1 key supplied separately, **without revealing the private selected candidate**.

**[DECISIVE FALSIFICATION]** Because every used automorphism is public and invertible, normalizing each derived key by the inverse automorphism should reveal *exact key coefficient equality* among all beta0 candidates. If one can identify beta1 from this equality pattern (even without knowing the template, encrypting secret, decrypting ciphertext, or oracle), the hypothesis FAILS. One explicit legal 4-candidate instance is enough; enumerate all 4 possible private digit choices and independent seeds to test robustness.

## Algebraic mechanics

Use ring `R_q = Z_q[X]/(X^N+1)`; for odd g∈(Z/2N)^×, define `sigma_g(f(X))=f(X^g)`; it preserves additive/ring operations and is publicly invertible.

For a rank1 GLWE `ct=(b,a)` decrypting via `b+a*s = mu+e`, the public coefficient automorphism `sigma_g^{-1}(ct)` encrypts `sigma_g^{-1}(mu)` under `sigma_g^{-1}(s)`, with correspondingly permuted error. Thus **zero encryption** under s can be transformed *without secret knowledge* to a correct zero encryption under the source HMuxRot output secret `s'_d=sigma_{g_d}^{-1}(s)`.

Let `Kzero=(Enc_s(0), Enc_s(0))` contain the two prepared gadget-row plaintext types, with arbitrary randomized RLWE masks and error. Candidate compression sets, for every beta_d=0,
```
  K_d = sigma_{g_d}^{-1}(Kzero)   (transform both entries' GLWE coefficients)
```
and for the unique beta_j=1 uses a freshly sampled rank2→rank1 key encrypting (G*s,G) under `s'_j`, where G is one small nonzero gadget element. All are **algebraically correct** keys. But the evaluator publicly computes
```
  Khat_d := sigma_{g_d}(K_d).
```
For every unselected d, **coefficient-by-coefficient** `Khat_d=Kzero` (including all noise coefficients), not merely an equality of underlying encrypted messages. For selected d, the second gadget row decrypts under s to nonzero `G` plus error after normalizing, while zero template decrypts to zero plus error; under valid small errors, the two ciphertexts cannot coincide. Even absent the separately published Kzero, if candidate group size B≥3, the unselected B−1 normalized keys have an obvious publicly recognizable equality class; the unique outlier is the secret rotation digit. If common template is available (it must be to generate keys on demand), a B=2 group also leaks by direct equality.

Important: This is a security flaw in *deterministic public-key relation / representation format*. Original SHIP does not adopt this proposal; original beta0 keys have independent randomness and do not have this exact cross-key equality.

**Nonzero active-key algebraic obstruction too:** Direct `sigma_{g_d}^{-1}(Enc_s(s,1))` encrypts `(sigma_{g_d}^{-1}(s),1)` under `s'_d`, whereas source requires `(s,1)`, so direct automorphism of a common beta1 template does **not** generate the desired key unless s has special automorphism invariance. A secret-dependent correction would be required; no claim of impossibility for more sophisticated compaction.

## Executed exact toy RLWE / public-linkability witness

Script `/mnt/data/ship_m06_public_zero_template_linkability.py`, SHA256 `9b6d0dd67aaa2f3c261364376a18e1ba60146d7b7bd5462153ba6c49b7cf69ee`, and JSON `/mnt/data/ship_m06_public_zero_template_linkability.json`, SHA256 `4f53ff17c96b788101e20ca02c9d9aec0abc28ee26c74e52ebeb801148d5d415`, both **local conversation artifacts, NOT installed GitHub code**.
Parameters: N8, q12289, toy gadget G16, base B4, secret s=(1,0,-1,1,0,0,0,0), `m=N/2=4`; source formula with `theta=1`, candidate `rot=d`, gives `g_d = 5^((m-d)%m) mod 2N = (1,13,9,5)`. These are legal power-of-5 Galois elements under the source source rotation formula (small parameters are **NOT security parameters**, and the all-zero ciphertext relation does not require a specific realistic security level).
- `encrypt_s(m)`: random `a←Z_q^N`, `e_i←{-1,0,1}`, `b=m-a*s+e mod q`, with negacyclic multiplication.
- For every selected digit `j∈{0,1,2,3}` and fixed PRNG seed in `{7,19,37,101,271,541,1091,2203}`, generate a fresh two-row Kzero under s; build B−1 beta0 candidate keys by public automorphism, build the unique beta1 key by fresh encryptions of (G*s,G) under s'_j.
- Check key source semantics: first row phase matches beta G*s, second matches beta G*1, component error per polynomial bounded by 1 under the candidate's target secret. PASS in all 32 trials.
- Check fully public normalization: `Khat_d=sigma_{g_d}(K_d)`; for zero candidates keys are **bit-for-bit equal**, active candidate differs. Without even giving the attacker template, SHA-256 hash/equality groups of normalized key coefficient arrays have sizes **(3,1)**, and unique outlier identifies private digit. **32/32 selected digits recovered**, exact deterministic algebraic attack. No secret s or decryption ever used by attacker; toy builds keys knowing s (keygen as usual), not the detector.
- Tested 8 different PRNG seeds as robustness only; **single correct explicit witness suffices** to falsify M06. Results do not support a numerical SHIP runtime/memory claim.

## Research judgment

**[FAIL]** A plain *publicly automorphism-derived shared zero GGLWE template plus one exceptional active key* cannot be a privacy-preserving SHIP mux-key compression, even though it has perfect algebraic switching-key correctness. The key set publicly encodes the private digit in exact cross-key correlations; a basic ciphertext-indistinguishability argument does not apply because ciphertexts are intentionally correlated.
**[OPEN]** This does NOT prove the b distinct keys inherently incompressible. Ways to explore **in later, separately authorized rounds**: candidate-blind key rerandomization without storing b full keys, alternative secret-blind correction packing, reducing rank/precision, PRG-seeded per-key masks combined with one-at-a-time prepared streaming (memory/latency trade-off), or changing the mux primitive as in external-product/CMUX/NTRU work. Each requires its own falsifiable hypothesis and test. If using independently generated encrypted dummies, need account that b re-randomizations can eliminate useful compression or add public keys.
**[CAVEAT]** The 2025/784 cached full PDF is github-mirror `VERSION_UNVERIFIED`; source includes mangled formula extraction; no statement that SHIP authors made this mistake or support this proposed compression.

## End of round (AGENT.md)

**STATUS:** **FAIL** for one-template publicly automorphism-generated zero HMuxRot keys with separately stored active key; **PASS** explicit privacy/linkability counterexample. Full SHIP mux compression UNSOLVED, novelty NOT VERIFIED.
**RESULT:** For every beta=0 candidate, public normalization recovers exactly one ciphertext template; with B4, its 3 identical normalized keys expose the sole active digit. N8/q12289 randomized RLWE test yields 32/32 successful public-index recoveries and verifies correct underlying key semantics. Algebraic key correctness ≠ evaluation-key privacy.
**NEXT_ACTION:** **SHIP-M07 only if PI continues**: ONE **source-specific prepared-memory scheduling/streaming feasibility gate**: determine whether existing Poulpy `ship_mux_rotate` can stream each mux GGLWE from independently seeded raw form into ONE reusable prepared-key buffer and accumulate DFT terms, dropping 480 resident prepared matrices to <=one-per-inflight thread without leaking digit; quantify extra per-bootstrap transforms/preparation and raw-key/seed requirements. First evaluate whether every original key can be independently regenerated from public seeds **without needing secret s** (mask-only seeded keys plus ciphertext bodies) — if not, KILL naive seed-only regeneration. Preserve original independent ciphertext distributions; don't introduce deterministic shared-zero ciphertext correlations. This is a proposed next test, not executed in M06.
**STATE_UPDATE:** YES this standalone M06 finding only; add separate M-series index to avoid overwriting concurrent SHIP I198 / vFHE V-series state.
