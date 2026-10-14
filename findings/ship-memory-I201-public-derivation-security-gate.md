# I201 — SHIP complex-paired selector public-derivation security gate

**Checkpoint:** 2026-10-14 (Asia/Tokyo). Human PI: “好的，请继续” after I200. Parent remains the PI-selected **independent SHIP evaluation-key prepared-memory** workstream, not general FHE global I-series or parallel vFHE V-series.

## Read before write / provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (parallel vFHE, do not edit), `findings/ship-memory-STATE.md` SHA `f0cec7c08347e2a80cfc92a2b302d610ffcf1cc0`, `findings/ship-memory-I200-drop-in-interface-gate.md`, and earlier SHIP-M01. Pinned **independent, nonauthor** Poulpy GitHub source `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
- `poulpy-ckks/src/layouts/ship/keyset.rs`: 4theta real selector mask messages each separately encoded/encrypted with the same dense secret key, `masks` and `masks2` in the real/complex branches.
- `poulpy-ckks/src/reference/imag.rs` blob `f516cd98804ee83c6643a74a231a216ee6c0f1b5`, and `poulpy-ckks/src/api/imag.rs` blob `ed6595ffd06373daf72d1a5b7ac660ab62d4d8d6`: multiply by `i` on canonical CKKS complex slots via multiplication by monomial `X^(N/2)` modulo `X^N+1`; in-place assign variant has `offset=0`, preserving log_delta and log_budget, no key switch. Source slot-kind becomes Complex.
- `poulpy-ckks/src/api/add.rs` blob `0747ef098b68daaac26ef6ecea0c1e129a6f649d` and `reference/add.rs` blob `73adc9ae3819928e5545d4951685464c018c7eb1`: addition of equal-width/equal-scale ciphertexts preserves nominal log_delta and log_budget without extra modulus drop; clears canonical flag pending normalization. Ciphertext addition is not zero-noise.

Parent publication Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, original proof assumptions not reproduced or independently re-proved in this iteration. The already known M01 algebraic packed pairing and I198 conditional 50% prepared selector object reduction are assumed only as established *conditional* prior findings. No genuine compiled Poulpy execution has happened; local `cargo`/`rustc`, pinned source checkout and DNS remain unavailable in this environment. Do not re-run toy gaussian models.

## ONE primary hypothesis / ONE decisive source-backed algebraic test

**H201 [HYPOTHESIS]:** There is a choice of packed-selector key generation **publicly simulatable** from original full SHIP selector evaluation keys without the secret key and without a new KDM/circular-security assumption. Therefore any computational secrecy/indistinguishability guarantee already proved for the full original evaluation-key distribution transfers by a simple deterministic efficient postprocessing reduction to the *derived* packed-key distribution (including all unmodified accompanying eval keys). This is NOT a proof of the original security assumption.

**One falsifier:** Inspect whether equal-level selector ciphertexts can be combined through a public `i` operator and addition under the *same* secret, with no new eval key; show algebraically that the resulting ciphertext decrypts to `M1+iM2` and that the derived full packed public key bundle is a deterministic polytime function `T(K_old)`. If not, H201 fails. No actual implementation benchmark in this round.

## Derivation [EXACT algebra under the original CKKS ring / decryption convention]

Take `R=Z[X]/(X^N+1)`, `N` power of 2 and `N>=2`, and source-defined CKKS canonical complex slots. Let ciphertexts of two *real-slot* selector vectors satisfy

`Dec_s(C1)=\widetilde{M1}+e1, Dec_s(C2)=\widetilde{M2}+e2`

where tildes are their encoded ring plaintexts; both encrypted under **the same dense GLWE secret** and with matching scale/torus width. Define the *ring monomial* `J=X^(N/2)`, with `J^2=X^N=-1` in R. In canonical slots used by the source, `J` evaluates to the imaginary unit `i` (the source calls this `ckks_mul_i`; not true for arbitrary alternate slot ordering without conventions).

Compute on ciphertexts only:

`Cpair := C1 + RotateMonomial_{N/2}(C2)`.

Because `RotateMonomial` multiplies all GLWE components by `J`, decryption commutes with this operation:
`Dec_s(Cpair) = (\widetilde{M1}+e1) + J(\widetilde{M2}+e2) = \widetilde{M1}+J\widetilde{M2}+(e1+J e2)`.

Thus its complex slot message is `M1+i M2` up to the encoding/noise terms. Crucially this does **not** use encrypted-input ciphertext multiplication, new Galois automorphism keys, secret support knowledge, new key-dependent ciphertext forms, or a modulus level drop in the source exact-width operations. `J` is a signed coefficient permutation, so coefficient infinity/Euclidean norms of `J e2` equal those of `e2`. A **worst-case** noise bound grows by at most `||e1||+||e2||` (no unjustified independence or RMS assertion); this extra selector-encryption noise remains to be checked numerically.

Let `KeyGen_old(s;r)` be the original SHIP key-generation algorithm's *joint* public output, including original selector ciphertexts and ALL supporting mux, tensor, dense-to-sparse, conjugation keys. Define deterministic polynomial-time public `T` which:
1. groups selector ciphertexts into M01's consecutive pairs and replaces each with `C1+i C2` computed using public ring shift/add;
2. leaves the other evaluation keys unchanged;
3. deletes old uncompressed selector ciphertexts after generation.

Define `KeyGen_pair(s;r):=T(KeyGen_old(s;r))`, with **no additional secret sampling**. For ANY efficient packed-key distinguisher `A`, build a full-key distinguisher `B` that, on full key input `K`, evaluates `A(T(K))`. Their distinguishing advantages are **identical** in the same distinguishing game (and therefore bounded by the original full-key secrecy guarantee), since the derived key distribution is exactly T's pushforward. This remains valid even when the original key encryptions were secret-dependent or correlated with other original eval keys, provided the original joint distribution/security statement indeed covers them. It is a standard public postprocessing/data processing argument, not novel and not an independent KDM proof.

Important scope:
- A **new direct-from-secret fresh encryption** `Enc(M1+iM2)` is not claimed to have exactly the same distribution as this derived `C1+iC2`. The postprocessing reduction applies only when the key generator is defined as T of the original key generator (or separately prove computational equivalence).
- The security transfer is a *relative* secrecy/indistinguishability statement, not a full proof of the original SHIP assumptions, RLWE security with all self-dependent eval keys, or correctness of the packed eval circuit. It does not address whether new protocol behavior leaks additional information through unavailable oracle interfaces; a public FHE evaluation circuit can be simulated from the same packed key.
- Original **4hθ** selector ciphertexts are initially generated then compressed offline, so this technique **does not halve keygen work** or necessarily lower *peak key-generation memory*. It can halve *resident prepared selector operands* after originals are discarded and packed ciphertexts alone are prepared, conditional on an implemented dual-accumulator evaluator. Do not confuse this with source `ShipKeySet::new` (I200 showed that current validator rejects 2theta masks).
- Extra selector ciphertext noise is `e1+J e2`; still need precision verification. The new **online** conjugation before mux remains, as do I198's extra masking IDFT and Galois costs.

## End-of-iteration

**STATUS: PASS** narrow **public-postprocessing secrecy transfer** for derived packed-key generation, under whatever original full-key indistinguishability guarantee is assumed, and source-level public CKKS monomial/add compatibility. **UNCLEAR** original security assumptions, full protocol security/correctness, actual ciphertext precision, implementation, end-to-end performance, novelty. **NOVELTY NOT VERIFIED**.

**RESULT:** A secret-dependent complex packed evaluation key can be generated from original same-secret mask ciphertext pairs by just a no-keyswitch ring monomial rotation and addition, making the resulting *joint evaluation-key distribution* an efficient public image of the original. No new KDM/circular-security assumption is required **relative to an already secured original full-key game**; this is a precise security-proof simplification, not an independently new algorithm. Noise may add, original keygen transient remains large, and original source APIs must be adapted.

**NEXT_ACTION:** For ONE pinned Poulpy implementation gate **once actual Rust runner is connected**, compare baseline real SHIP masking leaf and a packed version whose keygen uses this `T` (not fresh independent packed encryption). Evaluate max per-slot error with the original dense secret, extra masking/conjugation runtime, prepared selector bytes, and process peak memory. If runner remains unavailable, stay HUMAN_REVIEW instead of further toy/source bookkeeping. Do not alter production repo or concurrent vFHE STATE automatically.

**STATE_UPDATE: YES, independent SHIP state only**, because this is a material reduction in the security-assumption uncertainty; NO global `STATE.md`.
