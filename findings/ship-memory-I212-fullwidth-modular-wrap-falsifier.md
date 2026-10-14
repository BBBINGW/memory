# SHIP I212 — Full-width RLWE mask falsifies I211 row10 fractional torus normalization

**Date:** 2026-10-14 (Asia/Tokyo). **Track:** independent SHIP HMux evaluation-key-memory research, following I211; NOT the frozen global general I-counter and NOT the concurrently active vFHE V-series. Read-before-write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` (vFHE V15, read only), independent `findings/ship-memory-STATE.md` SHA `d242a19c4aff0fac2737cccdfbbfa7a20a9e9592` I211 and `findings/ship-memory-I211-gadget-row-to-ckks40-control-source-gate.md`. Parent idea approved as independent SHIP work. No upstream changes.

## Source provenance [FACT]

Scientific parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784 (paper math from prior I208–I211, original version status VERSION_UNVERIFIED). Current source-alignment is the third-party **Poulpy, NOT authors' HEaaN**, immutable `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `hmux_rot_key_encrypt_sk`: GGLWE rank2 input `(βs,β)` under output key `t_g=σ_(g^-1)(s)`.
- `poulpy-core/src/reference/encryption/gglwe.rs` blob `499c7b22daace7b74428d945a5ba5fca808a07d0`: separate encrypted gadget row per input column with β in the second input column.
- `poulpy-core/src/layouts/mod.rs` blob `c1e953bed001d3129188f4c0c5d35073a82ee59d`: at proposed k624, B52, dnum12, kaux52, original row physical key k676, 13 radix limbs.
- `poulpy-hal/src/layouts/encoding.rs` blob `c24822746b5a252bcb177207e005e6148ac33e6f`: torus coefficient value as sum `digit_j*2^(-52*j)`, so row10 β weight `2^-520`, 13-limb bottom fractional quantum `2^-624`.
- `poulpy-hal/src/api/vec_znx.rs` blob `01bca5331f68db07dd03fd2cc312524a354cf44f`: signed `VecZnxNormalize::vec_znx_normalize` computes a **componentwise** scaled/rounded torus representation, `offset=-12` as proposed in I211; source decryption correctness uses torus modular relation, NOT exact equality among arbitrarily lifted integers. I211's previous bounded-mask/no-wrap ring test is archived intact but its **general usability claim is now falsified**.

## ONE primary hypothesis + ONE cheapest decisive test

**H212 [TO FALSIFY]:** The I211 **specific row10** public recipe `σ_g` then **componentwise offset −12** and 13→12-limb normalization at k624 produces a correct scale `2^40` `Enc_s(β)` **even with full-width uniform RLWE masks and modular decryption wrap**, without secret-dependent carry correction. PASS criterion: for both β=0,1 in one source-shaped N16 standard negacyclic ring with encrypted tiny error and uniform mask, output modulo the destination torus decrypts to expected β·2^40 with at most small rounding/noise error. One counterexample falsifies.

**ONE TEST:** explicitly form valid noisy RLWE source row under `t_g` modulo source torus precision, publicly apply automorphism and proposed coefficientwise signed normalization, then decrypt under dense s in **destination torus**. Compare against expected coefficient message. Seed fixed; no secret used by public conversion. Full 624 random fractional bits per coefficient. Includes β=0 and β=1, 5 samples each.

## Exact obstruction [DERIVATION]

Use fractional torus `T=R/Z`; source 13-limb radix 52 represents fractions down to `2^-624`, so take corresponding integer residue modulus `Q=2^624`. Destination 12-limb torus fractions down to `2^-572`, `Q_out=2^572`. Source β gadget row10 has integer plaintext `M=β·2^104` modulo Q (fractional β·2^-520). Desired CKKS scale40 has integer output message `M_out=β·2^40` modulo Q_out (fractional β·2^-532).

I211's public torus operation is multiplying by `2^-12`, which *seems* to match the two fractional plaintexts. On the integer lifted components, it corresponds to independently rounding division by `2^64` (because source/destination grids differ by 52 bits).

But source RLWE decryption holds only **modulo Q**:
`b+a*t_g=M+e (mod Q)`.
After public σ_g, for a chosen centered lift of each component (secret unknown to public transformer), the unwrapped sum has form
`b_g+a_g*s=M+e_g+kQ`,
where `k∈R` is a coefficientwise **integer polynomial**, not necessarily zero. It disappears modulo Q but NOT after division by `2^64` and reduction modulo `Q_out`:
`round(b_g/2^64)+round(a_g/2^64)*s-M_out ≈ k·(Q/2^64)=k·2^560 (mod Q_out)`.
Since `2^560 ≠0 (mod 2^572)`, a wrap `k_j=±1` produces a significant torus message error `±2^-12`, rather than negligible CKKS precision error of about `2^-40`.

**Core reason:** `[x]=[x+1]` in `T`, but `[x/4096]` and `[(x+1)/4096]` are different torus elements; division by 4096 is not a well-defined additive group homomorphism `T→T`. Componentwise public Galois automorphism IS valid; **the negative fractional power-of-two shift** is the failing step for general encryption masks. This is an **exact algebraic objection**, not an issue that more statistical samples could remove.

## [EXECUTED] Full-width uniform-mask exact modular test

- Ring: `Z[X]/(X^16+1)`, torus residues `Z/(2^624)` per coefficient. Source nontrivial `s=X+X²`, `g=13`, `g^-1=5 mod32`, `t=σ_5(s)=X^5+X^10`.
- For each β and trial, sample each coefficient of mask `a` uniformly from `[0,Q)` using exactly 624 random bits, represent residues by canonical centered lifts; sample each source noise coefficient `e∈[-19,19]`. Form `b=[β2^104 + e - at]_Q`, verify exact source correctness modulo Q, then publicly apply σ_13 to both component polynomials, verify decryption under s modulo Q.
- Apply **separate** centered integer division/nearest rounding by `2^64` to both transformed components, reduce modulo destination `Q_out`, decrypt under s modulo Q_out. This exactly models the proposed **fractional torus linear-lift** of I211; it is not a compiled run of the `vec_znx_normalize` implementation.
- Fixed `seed=21220261014`, **10 trials** total (5 for β0, 5 for β1). **ALL TEN fail** the I211-style criterion of <=2 output integer units. The max observed error's bit length is **561** (order `2^560` integer units, i.e. torus `2^-12`), compared with desired β·`2^40` integer coefficient and tiny e. In the **first β=0 sample**, coefficient index6 has secret-dependent wrap quotient **k=+1**. The exact output error there equals `2^560` plus <=3 rounding units; it is not a statistical small-noise event. For every test, remove the explicitly computed `k·2^560` and the remaining rounding/error is at most **3 integer units**, confirming the missing carry is the cause.
- This is a **falsifier**, not a cryptographic distinguisher/security attack. Number of failed random samples is descriptive only, NOT a probability estimate for original SHIP or full production sampler.

Reproducible local files created and executed:
- `/mnt/data/ship_i212_fullwidth_torus_wrap_gate.py` SHA256 `64ca0486f85df973643341c8ca22cb3f8c24db9f8bfed8b66ee69d740d8f7552`
- `/mnt/data/ship_i212_fullwidth_torus_wrap_results.json` SHA256 `ced7491358189a95dd599f1a9ff029cb87fa884ce0f642c5642be4382a3b55fc`.

## Scope, successor ideas, and research decision

**FAIL ONLY** I211's specific **row10/negative-offset** public normalization as a universal ciphertext conversion. The earlier I209 **public Galois extraction of `Enc_s(G_iβ)`** remains algebraically valid, but it does not automatically yield an application-scale CKKS ciphertext. The other I207 candidate counts/memory savings are **conditional**, not invalidated algebraically by this particular conversion failing. Source dimensions large (N16384) and real IFMA/NTT FFT rounding, noise, RS security, keygen peak, and runtime remain untested.

**Not a no-go against all gadget rows:** An adjacent **row11** carries β at weight `2^-572` and would require **public multiplication by `2^40`** to yield target `2^-532` fractional torus plaintext. Integer multiplication by a positive power of two *is* a well-defined torus group endomorphism; it does not exhibit the same `k/4096` obstruction. However source gadget noise is amplified by `2^40` and then must fit output precision, so this is an explicitly **new, untested hypothesis**. Also need look at backend implementation and noise. Do NOT infer success of this alternate row from the I212 failure alone.

Original source SHIP contains the HMux key row and is not broken; our proposed **new public conversion** is wrong. I210 augmented joint eval-key KDM security remains **UNCLEAR/HUMAN_REVIEW**, about **480 extra CT×CT** and four additional multiplicative levels remain unbenchmarked, and I207 **~81.45% prepared payload** is an unimplemented conditional layout estimate.

## End of iteration

**STATUS: FAIL H212** (strong source-shaped exact modular-wrap counterexample), correcting the earlier I211 bounded-no-wrap optimistic assessment. **PASS** explanatory modular-lift equation and exact full-width mask test. **UNCLEAR** row11 alternative, actual real CKKS backend, full candidate security/accuracy/performance, novelty. **NOVELTY NOT VERIFIED**.
**RESULT:** The proposed public `row10, σ_g, res_offset=-12` transform is **not generally valid** for RLWE ciphertexts because division by 4096 is not torus linear: secret-dependent wrap adds an enormous `2^-12` plaintext error. I211 should be **treated as superseded on general correctness**, not overwritten or deleted.
**NEXT_ACTION:** If PI continues, test **one smallest replacement hypothesis**: whether row11 with a **positive** `2^40` torus multiplication followed by target 12-limb normalization avoids the modular-wrap obstruction while keeping the source GGLWE error below CKKS output precision. Check full-width modular masks, both β, tiny source noise, and apply conversion to both components; if it fails park this key-extraction subbranch. Even if it passes, do NOT mistake that for compiled Poulpy FHE correctness or security, and do not initiate new generic KDM paperwork without PI decision. Global vFHE state and upstream Poulpy untouched.
**STATE_UPDATE: YES** to independent SHIP checkpoint and failure archive, **NO** to global `STATE.md`.
