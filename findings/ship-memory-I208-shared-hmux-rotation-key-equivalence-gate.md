# SHIP I208 — The beta-independent shared HMux key is an ordinary rotation/automorphism key plus a public constant gadget

**Date:** 2026-10-14 (Asia/Tokyo). **Independent SHIP** numbering; PI “好的，请继续” authorizes one I208 security-distribution gate following I207. Do NOT alter the independently active vFHE global `STATE.md` (read SHA `528741fd2b38609fad2547721044474ea9e259cb`, V11) or previously archived SHIP findings. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, `findings/ship-memory-STATE.md` I207 (SHA `912b977293cf3b79126bb282f198f2a0f358a8dc`), and I207/I205 findings BEFORE writing.

## Primary evidence

Original **Jung Hee Cheon, Guillaume Hanrot, Jongmin Kim, Damien Stehlé**, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint **2025/784**. Research-MCP cached *full* PDF 33 physical pages, SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, GitHub mirror `arturo-kong/IACR-eprint-mirror@c0d63cf...`, **VERSION_UNVERIFIED** versus current official PDF. Acquired/read original:
- physical p10, §2.1: ordinary key switching `swk_{sk'→sk}` encrypts key-dependent plaintext `P·sk'` under `sk`.
- physical p11, §2.1: CKKS rotation key for Galois power is `rotk_r=swk_{sk(X^{5^r})→sk}` and conjugation has `-1`.
- physical p19, §4.2 Definition 1 and Lemma 2: HMuxRot key encrypts `P·β·sk(X^{5^j})` and `P·β` under the (same) destination key `sk`, with β secret onehot bit; correctness of its encrypted selection is separate from a confidentiality/security theorem.
- physical pp23–24, §5.1 Algorithm 5: gadget-decomposed HMux key rows likewise encrypt `P·β·γ_i·sk(X^{5^j})` and `P·β·γ_i`. Proof/source extraction is legible for plaintext message structure; complicated symbols/reading order may need visual check before formal proof. **No explicit security theorem for the NEW joint key distribution was identified in those inspected sections**; this is not a blanket assertion of absence throughout all versions.

Pinned independent third-party implementation (NOT author HEaaN):
- `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `hmux_rot_key_encrypt_sk` around lines 351–411 creates a rank2 switching key with **input** `(βs,β)` and **output** `t_g=σ_{g^-1}(s)`, and `ShipKeySet::generate` ~553–559 creates a tensor key and ONLY the Galois `p=-1` conjugation key in addition to beta-dependent HMux keys. The `p=g` general rotation keys are **NOT already stored as distinct keys** by this SHIP bundle.
- `poulpy-core/src/reference/encryption/glwe_automorphism_key.rs` blob `b584a17659347200c3fb8da8653f33f0a776ed8c`: `glwe_automorphism_key_encrypt_sk_reference(res,p,sk,...)` explicitly creates `sk_out=σ_{p^-1}(sk)` (by `vec_znx_automorphism(module.galois_element_inv(p),...)`), then calls `gglwe_encrypt_sk(res,&sk_data_ref,&sk_out_prepared,...)`. Thus **at p=g the standard automorphism key's encrypted input-message secret s and output key t_g match exactly the beta-independent shared HMux key's FIRST rank1 input column**. The encryption is still randomized and may be key-dependent/circular in its security modeling; it is not magically a public encrypt-from-original operation.
- `poulpy-core/src/reference/encryption/glwe_switching_key.rs` blob `20ce62e3791e343958862a2f77de0067c9b27fcc`: general switching key encrypts designated input secret under designated output secret in GGLWE rows, confirming operation semantics.

## ONE primary hypothesis and ONE minimal decisive test

**H208 [FALSIFIABLE TECHNICAL CLAIM]:** The beta-independent shared rank2 HMux switch-key material `(s,1)→σ_{g^-1}(s)` required by the I207 memory candidate is a qualitatively different **secret-dependent encryption primitive** from a normal CKKS Galois/automorphism/rotation key and cannot be assembled from (1) an ordinary `p=g` rank1 automorphism key and (2) **public** gadget plaintext material using only structural source transformations.

**Minimal decisive falsifier:** Compare exact `sk_in`, `sk_out` from pinned source ordinary automorphism key versus proposed shared KSK. Show that the secret-dependent row is identical up to gadget sizes and representation, and that a trivial GLWE row with public mask `a=0` and body `b=G_i` encrypts the constant-gadget input 1 under any `t_g`. Verify the resulting 2-input output decryption identity for a nonzero secret and nonidentity g on a small exact negacyclic ring. If it works, H208 FAIL; no security/IND-CPA theorem is proved merely by the algebra.

## Source-anchored exact derivation [FACT/DERIVED]

Let `R=Z_q[X]/(X^N+1)` and odd unit `g∈(Z/2N)^×`. Set `s∈R`, `t_g=σ_{g^-1}(s)`.

The standard Poulpy `GLWEAutomorphismKeyEncryptSk` for `p=g` produces gadget rows encrypting **`G_i s` under `t_g`** with random RLWE masks. This is *exactly* the proposed shared beta-independent HMux row for rank2 input component 1, `s`.

For the second rank2 input component `1`, generate a TRIVIAL publicly known (not statistically indistinguishable from normally randomized!) GLWE gadget ciphertext under t_g: `(b=G_i,a=0)`, which decrypts to `G_i` under ANY destination key. Therefore the resulting mixed GGLWE key for input `(s,1)` has the intended **decryption functionality** of the proposed shared `(s,1)→t_g` switching key, with a public noiseless second row. Applies to every gadget index i, provided the source's row order/gadget basis is matched when implementing. If the source HMux input is `(0,a_mask,a_body)`, its switching output decrypts to `a_mask*s+a_body` under t_g (modulo scale, gadget decomposition/rounding), just as I205 assumed.

In standard paper CKKS rotation-key orientation, `rotk_g` is an encryption of `σ_g(s)` under `s`. Applying the public ring automorphism `σ_{g^-1}` to all its ciphertext components changes the destination secret to `σ_{g^-1}(s)=t_g` and its message to `σ_{g^-1}(σ_g(s))=s`; so **that orientation** is also publicly convertible to the Poulpy `p=g` key. Need respect the underlying package's Galois-key direction, noise, gadget layout and modulus; not an asserted byte-for-byte identity.

Toy exact source-compatible negacyclic witness:
`N=16,q=257,g=13,g^-1=5 mod32,s=X+X^2,t=X^5+X^10`.
Build one noiseless encrypted gadget row with `G=7`, `a=1+X^3+X^5`, `b=G*s−a*t` in `R_q`; `b+a*t=G*s`. Public 1-row `(b=G,a=0)`. For arbitrary public scalar inputs `x=3,y=5`, linear application of both rows decrypts exactly to `G*(x*s+y)` under t, after including the trivial constant row. All statements verified with exact modular negacyclic polynomial arithmetic. This is NOT real key generation, cryptographic security, or FHE noise testing.

Executed local reproducibility files:
- `/mnt/data/ship_i208_rotation_key_structure_gate.py`, SHA256 `ea7f953f0af85fb832097c0c84b8e0debcfa785ece32793d7339d78bf1ea7bcc`.
- `/mnt/data/ship_i208_rotation_key_structure_results.json`, SHA256 `0ecefd0a46eebfb603040046a3133d39d07dbaa8efa74156a4dc572412912800`.

## Critical security/distribution limits [OPEN]

1. **FAIL H208 exotic primitive necessity** does NOT imply a public postprocessing reduction from the *actual original SHIP bundle*. In pinned `ShipKeySet`, original evaluation keys include conjugation `p=-1`, product tensor, source beta-gated mux keys and encrypted mask selectors, but **not separate general `p=g` rotation keys**. A new key generator that adds 15 standard automorphism keys is not the same joint distribution as original SHIP's keygen. So the I201 exact `Key_new=T(Key_old)` data-processing proof **is not established** for I207. No impossibility theorem against all possible full-bundle simulators is claimed.
2. **No unusual KDM *type* needed** if one explicitly assumes security for the augmented collection of standard ordinary rotation keys `p=g` together with tensor/conjugation/dense-to-sparse/masks and encryption of secret-offset bits β. But standard decisional RLWE alone should NOT be silently asserted to justify encryptions of secret-dependent plaintexts `s` under correlated Galois secrets. Formal joint-key KDM/circular-security assumptions remain to be stated/proved by a future security game/hybrid or referenced security theorem. The original paper pp10–11 provides CKKS primitives, pp19/23 defines HMux; it is not a fresh security proof for this augmented key distribution.
3. **Randomness / distribution:** the public `1` gadget row is a zero-mask trivial encryption, hence NOT distributed identically to a freshly randomized row of `GLWESwitchingKeyEncryptSk`. For functionality it is valid, and constant message need not be secret, but implementation noise/lifecycle/stamping differs; cannot claim exact key distribution equivalence or same numerical error.
4. **Public unknown β:** `Enc_s(β_{j,d})` is a normal encrypted bit under dense s, but β depends on the hidden sparse-secret support spec. Original SHIP public bundle contains related β-dependent material and encrypted masks. Semantic security of the *joint* augmented distribution must account for such correlations.
5. **Physical runtime and costs:** I207 conditionally counted 15 rank2 shared KSK objects (2.285GiB at k624). This gate suggests one **rank1 standard automorphism key** per rotation + a virtual public second row, which could be smaller, but a new cost/correctness/scheduling analysis is needed. I206's ~480 extra high-precision CT×CT products and four extra serial levels remain unchanged. No live runner available or actual FHE experiment performed; no claim of 81% actual memory saving.
6. **NOVELTY NOT VERIFIED:** this is a standard structural equivalence in key switching, not a publication claim.

## End of iteration

**STATUS:** **FAIL H208** (necessity of exotic new KDM key structure), **PASS source-anchored key-structure equivalence** with exact toy functional test; **UNCLEAR** original-SHIP-only public simulator, joint-security assumption for new key bundle, FHE correctness/noise/online cost, and novelty.

**RESULT:** The secret-dependent part of the proposed shared HMux key is simply a conventional standard CKKS `p=g` rotation/automorphism key. The public second rank2 input component `1` can be supplied as trivial gadget material. This narrows the security analysis: rather than inventing a novel KDM primitive, specify/security-justify an **augmented standard rotation-key collection + encrypted β**. However the original SHIP full eval key as implemented only generates conjugation `p=-1` and β-gated HMux keys, **not** those general keys; source-original postprocessing security inheritance remains UNPROVEN.

**NEXT_ACTION (one decisive gate if PI continues):** Formulate an explicit *joint-key hybrid/security experiment* for the augmented **standard 15 rotation keys + tensor, conjugation, original mask ciphertexts, dense-to-sparse key + 480 Enc_s(β) controls**, and check whether the published standard CKKS circular/KDM + IND-CPA assumption can cover the correlated sparse-secret β without a new nonstandard assumption. A security theorem for the *entire joint key distribution* (not just rotation key existence) is required before declaring the candidate proven secure. If such a theorem or assumption cannot be stated with concrete provenance, mark UNCLEAR/HUMAN_REVIEW rather than benchmark 480 nonlinear gates. Do not presume original SHIP's security automatically transfers. Major project pivot remains PI responsibility.

**STATE_UPDATE:** YES independent SHIP checkpoint only; NO global vFHE `STATE.md` and NO upstream modifications.
