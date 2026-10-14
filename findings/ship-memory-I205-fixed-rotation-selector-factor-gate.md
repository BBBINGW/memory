# I205 — SHIP HMux same-rotation shared-key factorization requires encrypted mixed-input gate

**Date:** 2026-10-14 (Asia/Tokyo). **Track:** PI-selected independent SHIP HMux GGLWE prepared-key memory, following I204. NOT global frozen I-series, NOT concurrently edited vFHE V-series. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, current global `STATE.md` (vFHE V10; untouched), independent `findings/ship-memory-STATE.md` (I204 last, SHA `edd0f0b2a6b7415b92eb034a74ae38e7fece6072`), `findings/ship-memory-I204-hmux-key-domain-obstruction.md`.

## Primary source

Original parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784 (§5.1/Algorithm 5). Code evidence is the **independent Poulpy implementation**, not authors' HEaaN: `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.

**[FACT from pinned source]** `poulpy-ckks/src/layouts/ship/keyset.rs` (blob `8be6ab92846168330100efeabe9fa19dbd9720e4`), `hmux_rot_key_encrypt_sk` ~351–418 and `generate` ~485–545: for each support j, mux digit and choice d, constructs switching key for `s_in,j,d=(beta_jd*s,beta_jd)`, `beta_jd∈{0,1}`, with output `t_d=sigma_(g_d^-1)(s)`, where the Galois element `g_d` depends on public rotation d, **not support j**. Different supports at the **same digit/rotation** have the same output secret t_d. In `poulpy-ckks/src/reference/ship/mux.rs` (blob `e9df6b5e4958fea1af6af3334d99fcb8b8f5ce`), source applies one prepared GGLWE product to rank2 `(0,a_mask,a_body)` per candidate, then performs the corresponding output automorphism before adding all candidate terms. The resulting selected message is `beta_jd * Rot_d(a_mask*s + a_body)` in ideal algebra.
- Previous I203 selected IFMA plan: HMux prepared key payload `42.1875 GiB` of complete `44.53515625 GiB` (94.73%), **layout only**, no measured RSS/author implementation.
- Independent existing primitive context: TFHE / GGSW CMux typically accomplishes encrypted `beta * ciphertext` via **external product**, not mere ciphertext-linear operations; cf. guide https://eprint.iacr.org/2021/1402 (PDF text from public web search; not re-derived as evidence for the specific Poulpy code). No novelty implication.

## ONE primary hypothesis and ONE cheapest decisive test

**H205 [HYPOTHESIS]:** For one identical rotation d across **two** independent sparse-secret support slots, replace their two beta-dependent rank2 HMux GGLWE keys with ONE reused beta-independent switching key `K_d^{shared}: (s,1)→t_d` and one small encrypted bit `E_j=Enc(beta_jd)` per support, and recover the same selected output for all legal inputs using **only ciphertext-linear operations** (additions, public constants/ct×pt, public automorphisms) after the shared keyswitch, with **no** extra ciphertext×ciphertext or external-product operation and without revealing beta.

**Falsification condition:** In ideal plaintext algebra, common shared key recovers `x=a_mask*s+a_body` under common t_d (or its public rotation under dense s); for independent hidden `beta∈{0,1}` must output `beta*x`. Find four legal `(beta,x)∈{0,1}²` cases that no affine linear readout of two ciphertext inputs can realize. Show secret-offset assignments giving beta=0 and beta=1 independently for two legal supports at the SAME d. This is one direct information/algebra gate, not a low-precision toy noise screen.

## [DERIVED + EXECUTED] Exact gate

Source-legal `ShipPlan` example: `N=16, h=2, window=3, theta=1, mux_base=2`, with any source-valid auxiliary `log_gamma,log_delta_work,log_budget_out`, e.g. `6,40,104`. First mux digit candidates `d=0,1`; take fixed `d=1`, `rot=1`, so `g=5^7 mod32=13`, `g^-1=5`; for a valid dense secret `s=X`, the common destination secret is `t_d=X^5`, independent of support.

`ShipSecretSpec::offset(plan,slot)=(j-slot*(N/h)+window) mod N`. For each support slot `j=0,1`, choose `u_j=0` or `1`; full support indices are `j_0=-3+u_0 mod16∈{13,14}` and `j_1=5+u_1∈{5,6}`. Both satisfy source's distinct support, correct window, and either sign; first mux digit beta_j,d=1 iff u_j=1. Thus **all four two-support bit patterns 00,01,10,11 are legal** with the same public d,g and same dense s.

For each (independently controllable) ciphertext input `x∈{0,1}` (take zero rank2 GLWE mask and body x; the KSK correctness domain includes such trivial ciphertexts), required ideal functionality is:
`F(beta,x)=beta*x`.

Truth table:
`(beta,x)=(0,0)→0,(0,1)→0,(1,0)→0,(1,1)→1`.

The decryption of a computation formed only from additive/linear ciphertext operations on two independent inputs `Enc(x),Enc(beta)`, plus static public key material, is **affine** in the two messages at fixed key: `L(x)+M(beta)+c`. Restricting to scalar constants in a single chosen slot (or the ring's constant embedding), this reads `alpha*x+gamma*beta+delta`. This necessarily has vanishing mixed finite difference:
`F(1,1)-F(1,0)-F(0,1)+F(0,0)=0`.
But beta*x has mixed difference `1`. Equivalently the four equations `delta=0;alpha+delta=0;gamma+delta=0;alpha+gamma+delta=1` are inconsistent. Exact SymPy affine design matrix rank=3, augmented rank=4. **H205 FAIL**.

**Narrow logical boundary:** This rules out **the restricted public-linear two-ciphertext readout** from a shared beta-independent key plus one ciphertext Enc(beta), not all compressions or even all ways to reuse the shared GGLWE key. A ciphertext-ciphertext CKKS multiplication, GGSW external product, nonlinear precomputed selector-conditioned evaluation key, joint packings or fusion across candidates can implement the missing bilinear interaction at other cost. Treat the source's existing beta-dependent GGLWE product as **already carrying the selector-function bilinearity in its static key material**; replacing this with a beta-independent key necessarily relocates secret-dependent selection somewhere else. The proof does NOT establish one additional ct-ct multiplication **per support per digit**, nor lower-bound all batched circuits. It also does NOT prove that an extra multiplication is necessarily prohibitive under measured runtime; that is a separate open cost/noise gate.

**Next plausible mechanism for a different iteration, NOT tested here:** Apply fixed-d shared `K_1` to get `Enc_(t_d)(x)`, then source Galois automorphism first to recover `Enc_s(Rot_d(x))`; encrypt `beta_jd` under dense s, then multiply using the already existing dense-secret CKKS tensor/relinearization key. This uses an extra online ciphertext-ciphertext product and probably additional noise/modulus budget, but **requires source-specific cost/precision validation before any performance claim**. Plain GGSW control is an alternative with large prepared encrypted selector material, not free linear compaction.

## Reproduction

Executed exact symbolic test and source-legal support enumeration locally:
- `/mnt/data/ship_i205_fixed_rotation_selector_gate.py` SHA256 `9c09917ce36b57e048328e341827ff0e68c95dc52826d6db5186a3d4d75adf95`
- `/mnt/data/ship_i205_fixed_rotation_selector_results.json` SHA256 `2ecf6a9edc84261eb362dba52c8f71105bd4666aff0c26c2bf5713a24422bccc`.
Four support-bit patterns, rank(A)=3, rank([A|b])=4, mixed difference=1; local Python+SymPy, **not** a Rust/Poulpy ciphertext encryption/decryption or latency/noise/peak memory benchmark.

## End of iteration

**STATUS:** **FAIL H205 affine-only fixed-rotation key sharing**, **PASS precise necessary encrypted-bilinear-control barrier** in a legal source plan. **UNCLEAR** nonlinear selector factorization feasibility, key payload, online performance/noise, overall security, and novelty. **NOVELTY NOT VERIFIED**.

**RESULT:** Cross-support fixed-d common-output-secret alignment alone is insufficient to compress HMux GGLWE key arrays with *only cheap linear encrypted selectors*. The implicit beta×input operation currently resides in each support's prepared GGLWE key; moving beta to a small separate ciphertext requires some operation capable of multiplying two unknown plaintexts, or other beta-dependent material.

**NEXT_ACTION (one cheapest next iteration if PI continues):** Trace ONE exact source-compatible factorization with **existing dense tensor key**: `shared K1 → per-d output automorphism → CKKS ct-ct multiply with Enc_s(beta)`; check level/scale/key-noise and count minimum per-candidate extra product, then a high-level memory-vs-operation necessary gate. Do not implement/benchmark without runner, do not claim latency-neutral compaction. Alternately PI may PARK key-reuse family on grounds of unavoidable online nonlinear gate. All progress is independent of global vFHE.

**STATE_UPDATE:** YES independent SHIP checkpoint; NO `STATE.md` global. No upstream repo edits.
