# I209 — SHIP augmented joint-key game: encrypted beta controls can be publicly extracted from the original HMux second GGLWE column (same-parameter conditional)

**Date:** 2026-10-14 (Asia/Tokyo). **Track:** PI-selected independent SHIP HMux prepared-key-memory project. Previous completed I208; do NOT advance frozen global FHE I192 counter or modify concurrent vFHE `STATE.md`. Read before write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (currently vFHE V12), `findings/ship-memory-STATE.md` SHA `5fba76c57541dfa531a3980f55f8c603df29e17a`, `findings/ship-memory-I208-shared-hmux-rotation-key-equivalence-gate.md`, and I207/I205 findings.

## Primary-source provenance

Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784. Actual paper via connected Research MCP, PDF 33 physical pages, SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742` from GitHub ePrint mirror; **VERSION_UNVERIFIED**. Read physical pages **10–11** (§2.1 ordinary key switching, secret-dependent material/rotation key) and **19, 23** (§4.2 Definition 1/Lemma 2 and §5.1 Algorithm 5): each HMux key includes encrypted `P*β*s(X^g)` AND a separate encrypted `P*β` for every gadget row, not just the former.

Audited independent, not author's HEaaN, backend: `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.
- `poulpy-ckks/src/layouts/ship/keyset.rs` pinned blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, function `hmux_rot_key_encrypt_sk` ~351–411, sets rank2 switching input `sk_in=(β*s,β)`, rank1 output `t_g=σ_(g^-1)(s)`, `g=module.galois_element((m-rot)%m)`, and calls `glwe_switching_key_encrypt_sk` with independent sampled randomness.
- `poulpy-core/src/reference/encryption/glwe_switching_key.rs` pinned blob `20ce62e3791e343958862a2f77de0067c9b27fcc`: `glwe_switching_key_encrypt_sk_reference` invokes `gglwe_encrypt_sk(res,&sk_in,&sk_out_prepared,...)`.
- `poulpy-core/src/reference/encryption/gglwe.rs` pinned blob `499c7b22daace7b74428d945a5ba5fca808a07d0`: nested loops `for col_i in 0..rank_in`, `for row_i in 0..dnum`; `vec_znx_add_scalar_assign(..., col_i)` puts **that input secret column's polynomial at the gadget row's prescribed radix position**; `glwe_encrypt_sk_internal` encrypts separately under same output secret. Thus **col_i=1** encrypts `G_i*β` (gadget scalar `G_i`, explicitly public, large power-of-two) under `t_g`. GGLWE row view is a valid rank1 GLWE ciphertext; it may not carry CKKS message metadata.
- `poulpy-core/src/reference/encryption/glwe_automorphism_key.rs` pinned blob `b584a17659347200c3fb8da8653f33f0a776ed8c` from I208 confirms `σ_g(t_g)=s`, key directions.
- `poulpy-core/src/layouts/gglwe.rs` pinned blob `37fd5350861393263c6b10bd827ad40a67d1a622`: GGLWE gadget description, `at_view(row,col)`; actual `G_i` is dictated by `k_aux,dnum,dsize,base2k`, not arbitrary CKKS scale40.

Related theoretical literature (not a claim that original SHIP proves all): Barak–Haitner–Hofheinz–Ishai, *Bounded Key-Dependent Message Security*, ePrint 2009/511; Brakerski–Vaikuntanathan, *Fully Homomorphic Encryption from Ring-LWE*, CRYPTO 2011 §4 treats linear KDM specially. Ordinary IND-CPA security **does not automatically imply** the required joint KDM/circular security of interrelated key-switch/relin/rotation materials. Parent original paper §2.1 explains key-switching and §4.2/5.1 defines HMux; it is not here taken as a full formal proof of enlarged candidate joint-key security.

## ONE primary H209 and ONE cheapest decisive source-based test

**H209 [TO FALSIFY]:** Each proposed dense-secret encrypted mux control `Enc_s(β_{j,d})` encodes **an entirely new secret-dependent plaintext** that is not already encrypted in the original HMux GGLWE evaluation-key bundle; it cannot be obtained as *any* public transform of one existing HMux key without knowing s or the hidden β. If true, every one of 480 β controls must be an additional independent secret-bearing key generation artifact in security analysis.

**One falsifier:** Inspect source input column 1 of one existing `HMuxRotKey(β,g)`, publicly extract row `i`, and apply coefficientwise `σ_g` to both GLWE ciphertext components. Exhibit decryption to `G_i β` under dense s for both β=0 and β=1, without s or β in transform. This *must not claim* direct correct CKKS scale/width or a matching fresh `Enc_s(β)` distribution.

## [DERIVATION] Exact public extraction identity

Let source GLWE decryption be `Dec_t(b,a)=b+a*t` in `R_q=Z_q[X]/(X^N+1)`, with source `t_g=σ_(g^-1)(s)`. For any original key K=K_(j,d) with public g and hidden β∈{0,1}, its second GGLWE input column's gadget row `R_i=(b_i,a_i)` satisfies

`Dec_(t_g)(R_i)=b_i+a_i*t_g=G_i*β+e_i`.

Here `G_i` is public and β is the *constant polynomial* β, so automorphism fixes it. The public transform (no new encrypted key material or decryption oracle)

`T_(g,i)(R_i)=(σ_g(b_i),σ_g(a_i))`

satisfies

`Dec_s(T_(g,i)(R_i)) = σ_g(b_i+a_i*t_g)=G_i β+σ_g(e_i)`.

This works for all hidden support/choice combinations; g and gadget index are public. **I208's extra general automorphism keys are not needed to perform this coefficient permutation**, since it is applied to a *stored evaluation-key row*, not to a ciphertext whose output must remain under the original s. The output key change is exactly intended.

**[EXECUTED] Small exact noiseless verification:** ring `R=Z_257[X]/(X^16+1)`, secret `s=X+X²`, nontrivial `g=13,g^-1=5 mod32`, t_g=σ_5(s), arbitrary public ciphertext mask `a=3+11X+2X^7`, and gadget factor `G=2^52 mod257=16` (illustrative of a 52-bit power; the toy does NOT represent physical 676-bit Poulpy torus precision). Set `b=Gβ-a*t_g`. For each β=0,1, `Dec_(t_g)(b,a)=Gβ`, and transformed `Dec_s(σ_g(b),σ_g(a))=Gβ`; decrypting original (untransformed) sample under s yields a nonzero wrong-secret residual. Python exact modular negacyclic arithmetic ran with assertions.

Local:
- `/mnt/data/ship_i209_beta_column_public_derivation.py` SHA256 `72736b70ebecf17a66c2f517b5e7bde8ec4bb4b99c19b96bf8a199fe886d796e`.
- `/mnt/data/ship_i209_beta_column_public_derivation.json` SHA256 `472122ceb6a5ce9dddd24eed1999b7a69d882b42a0573cac998a57d81e64706e`.
No Rust execution, measured noise, or actual backend key generation.

## Explicit joint-security game and conditional proof [DERIVED, NOT AN UNCONDITIONAL SECURITY THEOREM]

For a chosen security notion e.g. **support-specification indistinguishability**, define public parameters and a fixed dense encryption secret s (internally sampled by challenger); choose two legal sparse secret specs τ0,τ1 in the same admissible class and indistinguishable public parameters. Challenger samples bit b and outputs a full public evaluation-key view

`K_old^(k)(s,τ_b) = (D2S_(s→τ_b), HMux_(j,d)(β_jd(τ_b), s, t_g), encrypted masks(τ_b), Tensor_s, Conj_s, any public key)`.

The exact leakage/allowed queries, chosen-vs-random τ distribution, chosen-plaintext/bootstrapping eval interface, modulus and any adversarial ciphertext access MUST be specified in a complete formal game before claiming actual IND security. The mixed-secret D2S is a substantial correlated auxiliary object and cannot be discarded from the view.

For fixed matched precision `k=624` (**not I203's original 468**), define additionally `A_g(s)`, normal standard Galois/rotation evaluation keys for all public rotations used by the candidate. Construct `K_old^+(s,τ_b)=(K_old^(624)(s,τ_b), {A_g(s)})`. Define deterministic PPT **public** transform `T`: for every support/group/candidate `(j,d)`, extract `K_old.HMux[j,d].input_column1.gadget_row[i]`, apply `σ_(g_d)`, and keep it as **a derived gadget-scaled dense-secret encrypted β control**; retain original mask, Tensor/Conj, D2S and independent ordinary rotation keys; *discard all bulky old per-support HMux keys after extraction*. This creates a **slightly modified new key format** `K_new^derived=T(K_old^+)`, not I207's assumed freshly sampled Enc_s(β) distribution.

For ANY efficient adversary A distinguishing support specs from `K_new^derived`, adversary B given `K_old^+` applies T and runs A. Thus

`Adv_support^(K_new^derived)(A) = Adv_support^(K_old^+)(B)`

under the same game/environment; no *additional β-message* KDM assumption is required if the augmented original full-key bundle **already** has the relevant joint security. This is a standard postprocessing reduction; **does not prove** joint security of `K_old^+`.

**Nontrivial remaining issue:** Original pinned SHIP bundle does **not** contain the 15 new general rotation keys `A_g`. Adding them is NOT an I201 public postprocessing of the original bundle, and their *joint* relation with sparse-support HMux keys, D2S, Tensor and encrypted masks needs an explicit security justification. Ordinary marginal IND-CPA or separate rotation-key assumptions alone do NOT imply full augmented-bundle IND support secrecy without a joint hybrid/key-dependent-message assumption. **No such theorem was established this round.** Conversely nothing here proves the new bundle insecure. Circle/KDM assumptions are common in FHE evaluation keys but must be stated, not silently attributed to SHIP or standard decisional RLWE.

**CKKS execution scope limitation:** The derived control decrypts to `G_i β` under s, NOT directly to an application-scaled `Δ β`. Adjusting the gadget weight to the required `ld=40` scale, accounting for torus CKKS units, available modulus and source errors, and preparing as `CnvPVecR` for 624-bit CT×CT operations are separate correctness/precision gates. At k624 source GGLWE keys have k_aux52 and full row ciphertext precision larger than their input effective 624; cannot pretend extracted rows automatically match I207's 624-bit prepared-β width, noise, or ciphertext sampling distribution. Public transform may increase engineering costs. Deriving β from old KSK means generating the full widened original **~480** bulky GGLWE keys first then discarding them: **may reduce long-lived resident prepared key memory but not initial keygen work or peak generation memory**. Must not claim original keygen is avoided.

## End of iteration

**STATUS: FAIL H209** (claim all β control ciphertext messages are entirely new). **PASS** public GGLWE-beta-column gadget extraction under dense secret; **PASS conditional** exact public-postprocessing secrecy transfer from an **augmented old key bundle with 15 new ordinary rotation keys** to a **derived-control new key bundle**. **UNCLEAR** augmented-original-bundle security, actual β scale conversion, source-precision error, usefulness of this extra step vs freshly encrypted β, full algorithm performance/noise, original HEaaN applicability, and novelty. **NOVELTY NOT VERIFIED**.

**RESULT:** Original SHIP HMux GGLWE second column already contains β encrypted under rotation-dependent output secret. Public Galois on the stored row yields dense-key encrypted `G_iβ`; this can eliminate a separate *β-message class* in the conditional security argument by defining the control distribution through public extraction. However the new normal rotation-key collection remains a genuinely **additional correlated key publication** not justified from original SHIP-only key distribution. Model memory 81.45% from I207 remains **conditional** and cannot be ported wholesale to transformed-row widths or keygen peak.

**NEXT_ACTION:** HUMAN_REVIEW unless the PI wants a further narrowly scoped study. Scientifically decisive next technical action (if continuing this branch) is to source a **specific, credible joint KDM/circular-security theorem or clearly explicit additional assumption** covering the enlarged `K_old^+` containing correlated SHIP HMux, D2S, Tensor, Conj and all ordinary rotation keys; if unavailable, keep security **UNCLEAR**, and do NOT begin large CKKS implementation or report a publishable key-memory breakthrough. A subsequent separate **one-test** implementation/correctness gate would check converting gadget-weight `G_iβ` to CKKS scale40 with available modulus and actual source backend noise. If PI chooses to PARK this expensive key-sharing route, preserve I203–I209 for future revisit.

**STATE_UPDATE: YES** independent `findings/ship-memory-STATE.md` (material narrowing of security-distribution obstacle); **NO** global vFHE `STATE.md`. Upstream Poulpy untouched.
