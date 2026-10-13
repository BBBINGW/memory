# Iteration 168 — LCR+AKS evaluation keys bind the plaintext diagonal; ordinary rotation-key reuse does not directly transfer to dynamic transforms

**Date:** 2026-10-13. Human PI approved next research iteration with “好的，请继续” after I167. Research assistant interpreted assent to PARK the minor AHE Algorithm3 notation audit and select a **true FHE** source-available target. ONE primary hypothesis, ONE cheapest original-paper + actual source-code falsifier, exact scalar sanity check only. No FHE runtime/cryptographic performance or publication claim.

## Read-before-write and provenance

Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I167 blob `f6a66ce12ddf45500b089513ba8cf9351da9fdbf`, `findings/OPEN_RESEARCH_BRANCHES.md`, and I167 archived negative result. Excluded archived SPRU, CKKS p1-only, TFHE HFP noise, MR-FHE, LFBS, vFHE blocked P1 and related trivial optimizations from immediate re-opening.

**Primary paper [FACT]:** Lianglin Yan, Pengfei Zeng, Heyang Cao, Peizhe Song, Mingsheng Wang, *Faster Bootstrapping for CKKS with Less Modulus Consumption*, ePrint **2025/1403** (PKC 2026), https://eprint.iacr.org/2025/1403. Full Research MCP mirror **51 physical pages**, source_kind `github-mirror`, SHA256 `784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29`, official current version **VERSION_UNVERIFIED**. Source inspected §4.2 physical pp19–22, §5.1 p23, §6.1–6.3 pp24–27, Appendix B.2 p38–39. Paper's own footnote p24 contains code repository `https://github.com/Fainabi/Lattigo-LCR-AKS`; default branch `lcr`.

**Pinned author code [FACT]:** `Fainabi/Lattigo-LCR-AKS` commit `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4` (committed 2025-10-23, exact source inspection via connected GitHub). `circuits/ckks/bootstrapping/keys.go` blob `51e432b47c2c6ce8c398b3d81527113f9572aebb`, functions `genEncapsulationEvaluationAndLevelConservedKeysNew` approx lines176–264 and `genAggregatedGaloisKeys` lines266–307. `core/rlwe/keygenerator.go` blob `3b1ffc4553e1ad142cd3fd9833d9d34f43a3`, functions `GenAggregatedLevelConservedKeyNew` approx lines377–465 and `GenAggregatedGaloisKeysNew` approx lines467–500. **Pinned code implements actual RLWE encryption and rescale-like preprocessing of P*m*sk/q; no code compiled or benchmarked here.** This pinned commit may not be the exact one used in author's published experiments; do not conflate revision with paper's code revision.

## ONE primary hypothesis and single minimal test

**[HYPOTHESIS TO FALSIFY]** For a fixed CKKS secret, modulus level and rotation index, the aggregated switching key used by LCR+AKS is as reusable across **different public encoded plaintext diagonals** as an ordinary rotation key. Hence the online linear transform may change from m0 to m1 without any corresponding key update, and fusion continues to evaluate the new m1 correctly.

**[FALSIFIER]** Locate the exact m-dependent secret term in the author's §4.2 AKS key equation and verify that its *implemented* keygen embeds the actual DFT diagonal m. If present, derive what plain-multiplication term an unmodified m0-key evaluates when asked to implement m1, and show one non-negligible algebraic mismatch. This one source+code test decides direct-reuse claim. Do NOT assume a new-key object cannot be derived from old public keys by additional operations—only direct unchanged reuse is under test.

## Results

**[FACT PAPER]** §4.2 p19–20 defines AKS evaluation key (`evk_m,j`) whose secret-dependent embedded plaintext is approximately
```
   mu_m,j = round( P * m * sOld * gadget_j / q_l )  mod P Q_L.
   evk_m,j = ( -a_j sNew + mu_m,j + e_j, a_j ).
```
For aggregated Galois keys, `m_i` is the **encoded shifted diagonal** of the public matrix `M`, not just a Galois index. In §5.1 GHS-type first CtS matrix, paper equation (5) similarly uses `round(P*m_i*s/q_L)`; this fuses plaintext multiplication+rescale with key switching and saves a modulus level for **first** transform under small-coefficient precondition. Algorithm in §4.2 consumes `{m_i}` and corresponding `{rtk_{i,j}}`. With m0-key unchanged, the fused secret term remains the m0 term, not m1. General fresh ciphertext input with nonzero c1 then outputs the **wrong linear transform**, up to rounding/KS noise. This is not a correctness error of the paper's stated algorithm: paper precomputes keys for the fixed bootstrapping DFT diagonals.

**[FACT CODE]** `keys.go`:
- first CtS matrix: `for rot, diagonal := range btpEval.C2SDFTMatrix.Matrices[0].Vec`, calculate inverse-automorphism on that **diagonal**, then `GenAggregatedLevelConservedKeyNew(..., &matVec)`; the function's explicit comment says `Enc(skDense, P*m*skSparse/q_L), forall m in diagonal matrices`.
- other AKS levels: `for rot, diagonal := range matrix.Vec`, transform the diagonal then `GenAggregatedGaloisKeysNew(..., &matVec,qModuli[level])`.
- `core/rlwe/keygenerator.go` actually multiplies secret-key representation by `matrix.Q`, by P, and rescales by q_L; `GenAggregatedLevelConservedKeyNew` has centered integer rounding and `EncryptZero` then adds precomputed message; `GenAggregatedGaloisKeysNew` calls `genAggregatedEvaluationKey` on `P*skIn*matrix`.
- This is a genuine **message-dependent switching key / functional rotation key**, unlike ordinary rotation keys that depend on Galois element and secret but NOT encoded transform diagonal.

**[DERIVATION]** In the scalar abstraction of a single gadget/coeff, m0-key carries `round(P*m0*s/q)`, while correctly generated m1-key carries `round(P*m1*s/q)`. The effective fused output difference for switching input c1 (ignoring deliberate additional ciphertext-body handling) has main term `(m0-m1) s c1/q` plus discrete rounding. This generally cannot be dismissed as a key-switch error even if m0 and m1 are both publicly known or rotation index unchanged. One deterministic sanity check P101, q7, s1, c1=1, m0=1,m1=2 has key messages round(101/7)=14 vs round(202/7)=29; their P-normalized key contributions are 14/101≈0.13861 and29/101≈0.28713. Reusing old when new target is2/7≈0.28571 gives mismatch≈−0.14710, much larger than each key's rounding error. **This is NOT a valid full RNS-CKKS parameter set or ciphertext evaluation benchmark.**

**[PAPER PERFORMANCE SCOPE]** Table4 p26 Set I baseline vs I′ reports **CtS rotation key** size **5.47 GB vs 4.82 GB** (~11.9% reduction), bootstrapping time 25.98 vs23.20 s, output precision both 27.8 bits; sets II and III show 15.2% and15.1% CtS key size reductions. Table legend explicitly: **rtk size only contains rotation keys in CtS**, NOT total evaluation-key storage across full bootstrapping, key generation cost, arbitrary model collections or multitenant deployments. The paper's first CtS DFT has fixed diagonals by CKKS parameters, so key dependence causes **no defect or direct scalability claim violation** for their fixed-transform bootstrapping use. This source benchmark also uses LCR, sparse-secret encapsulation, GHS-type keys and changed parameter sets; cannot attribute measured speedup to individual dependency alone.

## Scientific judgment

**STATUS = FAIL** ordinary-key **direct unchanged key reuse** for a different public transform; **PASS source+code binding evidence**. This is a real **applicability and key provisioning** boundary for trying to apply AKS to *dynamic* public matrices (e.g. frequently changing model weights, transform libraries) but is **NOT a new security weakness/algorithm error or publishable contribution**. In fixed DFT bootstrapping the matrix is static, so claimed author benefit survives.

**[Potential follow-up (NOT TESTED)]** Because evaluation keys themselves are RLWE encryptions and public, if a family of public diagonals belongs to a small basis span, could an evaluator derive aggregated keys for new diagonals via **linear combinations of pre-encrypted basis evaluation keys**, eliminating new secret-key keygen? A key-specific rounding nonlinearity, evaluation key noise amplification, modulus and key-material memory/NTT costs may negate the hoped benefit. This is not automatically a new algorithm: public homomorphic combinations of evalkeys is standard linearity; need a **precise source-compatible error/security and budget test** before treating it as research. More important FHE frontier would be concrete `K` public weight updates vs `r` diagonals, memory/per-update key generation vs runtime savings at real CKKS parameters, not a generic example with arbitrary m.

**[NEXT_ACTION]** I169 only if PI authorizes: ONE small analytic source-key test of public linear synthesis of AKS keys, including deterministic rounding mismatch and random key-noise growth for just two fixed basis plaintexts (same rotation, same RLWE secret), and derive whether resultant key is both *valid* and likely beneficial. If false or only conventional prohibitive key size, PARK dynamically adaptable AKS and consult higher-priority FHE backlog. Do NOT simply test another m0≠m1 scalar mismatch, do not claim general composability/security or speedup.

## End of Iteration 168

**STATUS:** **FAIL** hypothesis that original AKS key can directly support a different plaintext diagonal; **PASS** paper+tagged author code dependency and scope check; **UNCLEAR** any truly useful dynamic-transform key-adaptation technique.
**RESULT:** ePrint 2025/1403 §4.2 and §5.1 keys carry `round(P m s/q)`; author's pinned `keys.go` loops over actual source DFT diagonals and calls `GenAggregatedLevelConservedKeyNew` / `GenAggregatedGaloisKeysNew` passing m. Reusing unchanged key for m'≠m computes stale linear function, not new transformation. Bootstrapping DFT fixed, so paper claim unaffected; CtS rotation key size savings are specifically CtS-only.
**NEXT_ACTION:** one two-basis **public key synthesis** source-equation gate, with new key noise and deterministic roundoff bounds, only on explicit PI continue; if low value, park. Avoid repetitive trivial scope observations.
**STATE_UPDATE:** YES — new real CKKS target, sourced author implementation and pinned key-generator internals, archived one decisive gate and next action. Other prior branches remain parked/source-gated.
