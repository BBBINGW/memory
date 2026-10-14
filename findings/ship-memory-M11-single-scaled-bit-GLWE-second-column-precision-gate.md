# SHIP-M11 — Naively replacing the second HMux gadget column with one scaled-beta GLWE needs enough auxiliary precision

**Date:** 2026-10-14 (Asia/Tokyo). **Research stream:** independent SHIP M-series; **M11 COMPLETED**, M12 NOT STARTED. PI said “好的，请继续” after M10. This M11 is separate from concurrent SHIP I-series and vFHE V-series.
**STATUS:** **FAIL** narrowly specified ordinary-beta-GLWE substitution at **k_input=428, t=40 auxiliary guard bits**, for single noisily encrypted β ciphertext multiplied by an arbitrary legal public ciphertext body. **PASS** exact scaled-GLWE arithmetic counterexample. **UNCLEAR** higher-guard version, full SHIP correctness, privacy/security, real memory-versus-latency, and novelty.
**Original parent:** Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / ePrint 2025/784 §5.1 Algorithm 5, original cached github mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. Audited source is **independent Poulpy**, not authors' HEaaN.

## Read before write and branch collision avoidance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, previous `findings/ship-memory-M10-public-normalized-onehot-hmux-obstruction.md` SHA `f9ef8df50d87abc6bfd79d643788649db379d431`, concurrently updated SHIP state `findings/ship-memory-STATE.md` SHA `52a27b251f7c7144b7efd9ac9fd5291c81370ded` (already I210) and I205, I207 literature notes. Global vFHE state remains separately managed. **Do not change either shared state file**. M11's question is **different** from I205–I210's 15 shared β-independent HMux keys + online CT×CT scalar gating: M11 **retains a per-candidate secret-dependent first gadget column** and attempts to replace **only its second input gadget column** by a much smaller β-GLWE plus **ciphertext×PUBLIC-input-body** polynomial multiplication (not another encrypted selector CT×CT).

## One primary falsifiable hypothesis, one decisive test

**[HYPOTHESIS]** For a fixed candidate d, an otherwise intact HMux GGLWE input-rank2→output-rank1 key (first gadget column encrypting `β_d*s` and second encrypting `β_d` under target `s'_d=σ_gd^{-1}(s)`) can drop the **second full gadget column**, replacing it with ONE ordinary rank1 GLWE ciphertext encrypting a scaled constant selector `β_d 2^t` at auxiliary key modulus `Q=2^{k+t}`, with **t=40** extra bits above the input/body `q=2^k,k=428`, multiplying publicly by the input body's integer polynomial `B(X)` and dropping t low bits, **without causing errors on the order of the final SHIP reference 18.1-bit message-output tolerance** for arbitrary legal GLWE body coefficients.

**[FALSIFIER]** Exhibit ONE legal public ciphertext body coefficient magnitude ∼q and one legal small beta-encryption noise coefficient where a *properly encrypted* `β2^40` with one-glwe replacement adds >2^-18.1 in scaled message units, even if the existing first gadget column were exact. This is a necessary precision gate for the narrow substitution; no real HE run required.

## Pinned code facts [FACT]

- Repo `poulpy-fhe/poulpy` commit **`250d4392656cd313f92ca66d96d8865702d39ddf`**.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `hmux_rot_key_encrypt_sk` makes rank_in2 `sk_in=(βs,β)` and output `s'_d=σ_(g_d^-1)(s)`, with rank_out1 GGLWE key at gadget `dnum=ceil(k_ct/(base2k*dsize))`, `k_aux=base2k*dsize`; for b52, dsize1, k_ct468, `key.k=520` bits. Existing code includes BOTH full gadget columns, **no ordinary-GLWE replacement exists**.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: hoisted mux consumes a rank2 ciphertext input `(0,a_mask,a_body)`, per-key GGLWE product, public Galois output transformation, and sum. The body `a_body` is **publicly visible but in general high-modulus torus coefficient polynomial**, not a small low-degree ordinary plaintext.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d`, plus M02 source gate: masking result may have effective k≈428 with `log_delta=40`, high ciphertext coefficient precision; exact source normalization must be checked in any implementation variant.
- `poulpy-core/src/layouts/prepared/gglwe.rs` and `poulpy-cpu-avx512/src/ntt3x42_ifma/module.rs`: existing prepared rank2→1 HMux is ~90MiB per candidate for N16384, dnum9, key_size10, 16-byte IFMA DFT word. Proposed first gadget column alone would be ~45MiB; a coefficient-domain rank1 β-GLWE at k_key520 would carry ~2.5MiB payload. **These are speculative candidate-layout bytes, not tested and not a full-keyset new upper bound**.
- Existing independent I205–I210 shared-key + encrypted β CT×CT construction is **NOT** reused or independently re-tested here.

## Correctness/noise mechanics [DERIVATION]

Choose torus/radix integer modulus `q=2^k` for current input body and an auxiliary key modulus `Q=2^(k+t)=q*2^t`. A single rank1 GLWE encryption under output secret s'_d satisfies:
```
Dec_s'(Eβ) = β*2^t + e(X)   mod Q
```
with independent low-integer noise e(X); `β∈{0,1}`. This **does not encode an ordinary CKKS-scale-40 β**: the 40 here is auxiliary headroom, and the torus phase β*2^t/Q is β*2^-k. The input rank2 ciphertext's public body has torus representation `B(X)/q`, with `B(X)` an arbitrary visible polynomial with coefficients centered in `[-q/2,q/2)`.

Proposed evaluator publicly multiplies both GLWE components by the *integer polynomial* B(X) in the negacyclic ring modulo Q and coefficientwise rounds/shifts down t bits to modulus q. In ideal no-error model:
```
 (B(X) * β 2^t) / 2^t = β B(X) mod q.
```
With key encryption noise, additional output integer error approximates
```
 e_out(X) = (B(X)*e(X))/2^t
```
plus ≤O(1+||s'||_1) coefficient rounding from separately truncated GLWE components. This is a multiplication by a **large public torus integer**. For input body coefficient B≈q/3, e=1, resulting torus phase error is ≈(1/3)*2^-t. CKKS message-scale error with log_delta_work=40 becomes ≈`2^(40-t)/3`. At t=40, this is ≈**1/3**, overwhelmingly larger than nominal 2^-18.1 reference.

The original full GGLWE gadget column avoids this large-integer multiplication by decomposing B into radix digits and carrying **one evaluation-key sample per gadget digit** with auxiliary guard; replacing it with one β ciphertext is **not** a mathematically free rank reduction. Alternative high auxiliary guard t may absorb noise but needs its own complete test; no general impossibility is claimed.

## Executed one exact randomized GLWE witness

**Script:** `/mnt/data/ship_m11_scaled_beta_single_glwe_precision_falsifier.py`, SHA256 `55566b836c51371a7fe66ebc27e75d4553d2ed738fb37c63e943cba1565dcd6d`.
**JSON:** `/mnt/data/ship_m11_scaled_beta_single_glwe_precision_results.json`, SHA256 `58941aae5ed64f66f23e9f88f21f51c8ae234d4da00bcf3ab704e1f70e2fd19a`.
Local Python was **actually executed**. No source Poulpy Rust/HEaaN binary executed, and no cryptographic security proof.

Test ring `R=Z_Q[X]/(X^8+1)`, q=2^428, helper Q=2^468, t=40. Dense toy ternary secret `s=(1,0,-1,1,0,0,0,0)`, **valid but deliberately tiny/non-secure**. For each β=0 or1 and each of 8 PRNG seeds `[7,19,37,101,271,541,1091,2203]`, independently sample uniformly random GLWE mask a∈R_Q, use supported error e(X)=1, form `b=β2^t+e-a*s` mod Q; decrypt to confirm **exact** `β2^t+e`. Body public polynomial `B(X)=floor(q/3)` constant (legitimate centered GLWE ciphertext body component). Multiply *both* key GLWE coefficients by B modQ, then round each to modulus q by `(v+2^(t−1))//2^t`, then decrypt under s. Against correct selector output βB modq:
- **16/16 original β GLWE encrypt/decrypt checks pass**.
- **16/16 replacement output errors exceed 2^-18.1 message reference**; coefficient-0 after output normalization/scaling gives message error **0.333333333333...** for all seeds, while other coefficient deviations are at most 1 integer unit.
- The injected noise e(X)=1 is **inside original source's discretized encryption noise support**, so this is a source-style legal witness of the claimed universal precision guarantee failure. Using input public B from ciphertext distribution isn't a guarantee that specific constant B is *likely*; falsifies an unconditional all-legal-body claim only.
- The q, Q and one-row β ciphertext are **our proposed idealized replacement semantics** and not a real measured Poulpy operation.

**Guard sensitivity:** for the same one-coefficient toy if t=92, a negligible idealized *single-coefficient* message error `(1/3)*2^-52≈7.4e-17` is possible under this model, so **do not** conclude that any single-GLWE β replacement fails. Original `GGLWE key.k=520` provides 92 bits above k428, meaning such a helper would have similar total precision if implemented. It might have different security and multiplication costs. Complete N-dimensional key noise amplification, slot evaluation, multiple mux depths, masking scale and SHIP product tree may independently invalidate or permit it.

## End of iteration / decision

**STATUS:** FAIL **only** t=40-guard one-GLWE substitution with current source-shaped k428; PASS exact RLWE noise witness; UNCLEAR higher-guard variant at t~92, actual HE execution, security, memory/latency, novelty.
**RESULT:** Replacing HMux β-input GGLWE digit column with one insufficiently guarded β-GLWE incurs error `B*e/2^t` where B has up to k bits. One legal single-noise sample gives ~1/3 message error at t40, versus 18.1-bit paper reference. The original GGLWE gadget/decomposition protects precisely against this high-modulus body multiplication. M11 is a **candidate-design obstruction**, NOT an attack on SHIP.
**NEXT_ACTION (SHIP-M12 only after PI continuation):** ONE source-conditioned **full-polynomial noise-bound feasibility/falsifier for a 520-bit β-GLWE with t=92**; include worst-case coefficient N-fold convolution, slot transform, scale40, per-mux four-stage accumulation and h32 product-tree propagation, and juxtapose realistic source noise support and nominal reference margin. If worst-case bound exceeds tolerance, report only “worst-case guarantee cannot be certified” (an upper-bound failure does NOT prove actual keygen likely fails); seek explicit legal witness before declaring FAIL. Crucially distinguish beta-helper noise from the untouched first gadget column and from backend errors. If high-guard feasible, recommend compiled Poulpy next rather than indefinite toy iterations. Avoid concurrent I210's already analyzed shared-key CT×CT security distribution.
**STATE_UPDATE:** YES only this immutable M11 file. Neither global `STATE.md` nor concurrent `findings/ship-memory-STATE.md` touched. M11 self-contained for next session.
