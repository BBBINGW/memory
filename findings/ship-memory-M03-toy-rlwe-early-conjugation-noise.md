# SHIP-M03 — Actual toy RLWE/CKKS arithmetic test isolates early Galois key-switching noise

**Date:** 2026-10-14; **sequence:** independent `SHIP-M03`, not vFHE I193/I194/I195 and not a global I-round.
**PI authorization:** “好的，请继续” after M02; target unchanged: SHIP prepared evaluation-key memory.
**Status:** **PASS toy arithmetic reconstruction; FAIL toy precision parity at chosen simplistic key-switch parameters; UNCLEAR source-Poulpy secure-parameter correctness / prepared RAM / latency / novelty**.

## Read before write

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-STATE.md` (SHA `9b12d5e96bf3f390bd29ca219d9108e6a729f476`), M02 `findings/ship-memory-M02-early-conjugation-source-modulus-gate.md` (SHA `7423b2d3a60778a947c08070f1ca716ccad69a5e`), and checked global `STATE.md` only to avoid concurrent changes. Global `STATE.md` belongs to a different vFHE workstream (I195 at start); DO NOT overwrite it.

### Primary sources and source-code provenance

SHIP publication: Cheon et al., *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, https://eprint.iacr.org/2025/784, source §3.3 four masks and §4.4 fused column selection; source ePrint 33pp mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, publisher/latest version unverified.
Independent Poulpy implementation (NOT author HEaaN) pinned `poulpy-fhe/poulpy` at `250d4392656cd313f92ca66d96d8865702d39ddf` as verified in M01/M02:
- `poulpy-ckks/src/encoding/ship/masks.rs` generates source-shaped zero/one hybrid masks, dependent on private secret support/sign and column candidate.
- `poulpy-ckks/src/reference/ship/masking.rs` performs ciphertext×public-plaintext accumulation; `poulpy-ckks/src/reference/ship/bootstrap.rs` performs mux/product tree after masking; contains pre-existing Galois -1 key used once at output.
- `poulpy-ckks/src/reference/conjugate.rs` and `poulpy-ckks/src/oep/derived/conjugate.rs` show Galois conjugation uses key switching. M02 demonstrates no obvious level mismatch; no numeric test was made.

## ONE primary hypothesis and ONE minimal test

**[HYPOTHESIS]** With encrypted, source-shaped real SHIP selector masks, CKKS complex pairing reconstructs the same encrypted masked-sum leaf after Galois automorphism + key switching, at fixed scale, with negligible *added* noise relative to a two-mask baseline under a representative **toy** RLWE/CKKS arithmetic model.

**[DECISIVE TEST FOR THE LIMITED MODEL]** Implement an independent, executable negacyclic RLWE/CKKS toy reference with actual randomized encryption and an independently encrypted radix-decomposition Galois automorphism key; compare encrypted/decrypted source-style (M_1P_1+M_2P_2) against the packed formula across 8 predetermined seeds. Isolate key-switch noise by decrypting `phi(V)` directly under transformed secret `phi(s)` (same ciphertext without key switching). If significant precision degradation appears, FAIL the *toy negligible-overhead hypothesis*, not the general high-precision SHIP construction.

## Environment and executed artifact

No `rustc` or `cargo` installed; no internet DNS from container for GitHub; no Poulpy compiled binary/libraries. Cannot execute any real Poulpy CKKS run. Did **not** modify or fork original code.
**Local executable script** `/mnt/data/ship_m03_toy_rlwe_conjugate.py`, SHA256 `2642ad66d313a548c9dbd973521ecf1eeb2e464798da53dc02b6b81e83dd03f0`.
**Local JSON results** `/mnt/data/ship_m03_toy_rlwe_results.json`, SHA256 `2f3f3e2b7d6811151dc663dfe58c443c692be44c60d242d58eb6d8856436e7dc`.
Files are LOCAL ONLY and have not been moved to GitHub.

**[FACT executed, model]** Script implements:
- exact integer `Z_q[X]/(X^16+1)` negacyclic product; q=2^104, scale Δ=2^30; 8 complex CKKS slots via conjugate-symmetric evaluation at odd 32nd roots;
- secret ternary polynomial, independently sampled uniform RLWE masks and ternary coefficient noise; (a,b) decrypts to b+as;
- homomorphic ct×pt ring multiplication, coefficient-center rounding division by Δ, switching to `q'=2^74`;
- Galois automorphism X→X^-1 on both ciphertext components; encrypted evaluation key with radix `B=64`, `L=13` ciphertext digits targeting `s'=phi(s)`, ordinary digit decomposition/key-switch at q'; decrypted output under original secret;
- secret-dependent binary source-compatible masks with j=3, s_j=+1, p=1, column candidate c=u mod θ=2, m=8, θ=4, satisfying j=(p+u) mod m; pairs **k=1 and k=4** (both nonzero over different slots). Distinct complex unit-modulus plaintext operands with per-slot varying phases. Pairing (1,4) rather than (1,2) is allowed in M01's arbitrary two-real-mask compression identity; still source generated masks.
- 8 deterministic independent encryption/key-generation streams [17,37,71,131,271,541,1091,2203].
This is NOT a secure CKKS parameter set, not complete bootstrapping, no prepared-key DFT buffers, no runtime timing benchmark or correctness/security proof. Encoding is an elementary canonical-slot model, not Poulpy's production encoder.

## Mathematical identity and measured outcomes

Original:
`B = Dec(Enc(M1) * P1 + Enc(M2) * P2)`.
Packed:
`C=Enc(M1+iM2)`, `U=C*(P1-iP2)`, `V=C*(conj(P1)-i conj(P2))`;
`T = (U+KS(phi_{-1}(V)))/2` under final scale Δ. One real mask ciphertext rather than two. Key switching required because `phi(s)≠s` in general.

At the source-shaped encrypted toy, **worst per-trial maximum slot absolute errors**, 8 fixed seeds:
```
baseline worst            = 1.9594663457003924e-08
packed worst              = 3.150877916287913e-06
KS-only addition worst    = 3.1525569148800527e-06
packed no KS              ≈ 1e-08
```
All packed toy outputs passed the coarse absolute check `<0.001` but toy packed loses roughly 2 orders of magnitude vs baseline, primarily from key switching. The `KS-only` quantity is independently computed from `Dec_{s'}(phi(V))` vs `Dec_s(KS(phi(V)))` over slots; it isolates evaluation-key error, not generic CKKS rounding. No common same-input real-world decryption comparison was executed.

**[DERIVATION, no-go for 'zero added KS noise' intuition]** Let evk digit ciphertext i satisfy
`b_i+a_i*s=B^i*phi(s)+e_i (mod q')`. For rotated `a' = Σ_i B^i d_i(a')`, the key-switched decryption is
`b'+a'phi(s)+Σ_i d_i(a') e_i`.
Thus extra error polynomial is exactly `e_KS=Σ_i d_i(a')e_i` in this model. Unless evaluation-key noise or digit coefficients vanish/cancel, the packed method has nonzero new error. Increasing key-switch precision/decomposition settings could reduce it; this test does NOT imply a general memory-vs-noise impossibility.

**[CORRECTNESS LIMIT]** The toy uses independent Galois keys and RLWE samples, not a production hybrid RNS/PQ modulus, and does not model potential plaintext phase re-encoding, extra two FFT/IDFT accumulations, actual mux-rotate and product tree, or software memory. Baseline vs packed are different independently randomized ciphertexts (fair in distribution, not paired-noise controlled). Benchmark numbers should NOT be read as SHIP performance.

## Judgment, independent state and next gate

**STATUS:** **PASS** toy encrypted algebraic feasibility; **FAIL** strong 'negligible extra key-switch noise under chosen toy params'; **UNCLEAR** production secure-parameter viability and latency, **NOVELTY NOT VERIFIED**.
**RESULT:** First executable ciphertext-level test of M01 uses a genuine Galois evaluation-key switch, not just plaintext conjugation. In chosen toy parameters, 8 seeds all reconstruct a correct mask combination but show the Galois noise term dominating the new error: worst ~3.15e-6 vs ~1.96e-8 baseline. This is a **warning**, not a proof of high-precision SHIP failure.
**NEXT_ACTION, ONLY with PI continuation (SHIP-M04):** **ONE** parameter-grounded Galois-noise falsifier using actual pinned Poulpy automorphism-key decomposition and normalization code: derive a conservative `k=428` early-key-switch noise envelope and compare with a defensible SHIP output-error budget. If the derived worst-case noise cannot fit even with source parameters, KILL complex-packed selectors; if bounds are loose, request ONE real Poulpy runner for benchmark rather than repeatedly scanning synthetic configurations. Do not attempt any new competing algorithm in same round.
**STATE_UPDATE:** YES, SHIP-specific `findings/ship-memory-STATE.md` only. Do not modify global vFHE `STATE.md`.
