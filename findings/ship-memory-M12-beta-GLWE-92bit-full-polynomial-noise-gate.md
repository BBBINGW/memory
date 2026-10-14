# SHIP-M12 — 92-bit β-GLWE helper guard: full polynomial worst-case precision gate

**Date:** 2026-10-14 (Asia/Tokyo). **Independent M-series:** M12 COMPLETED, M13 NOT STARTED. **PI:** “好的，请继续” following M11. **Separate from concurrently edited SHIP I-series and global vFHE V-series.**
**Research target:** reduce SHIP HMux rank2→1 prepared GGLWE memory by retaining first (βs) gadget column but replacing second (β) gadget column with one full-precision ordinary rank1 GLWE, multiplied by the publicly available input ciphertext-body polynomial.
**STATUS:** **FAIL** source-conditioned **universal worst-case 18.1-bit precision guarantee** for a **t=92-bit** auxiliary β-GLWE noise term in an ideal h32 SHIP-shaped mux/product tree; **PASS** actual 520-bit full-length exact negacyclic GLWE encryption, public polynomial multiplication, coefficient reduction and canonical slot evaluation, plus a clearly conditional repeated-leaf witness; **UNCLEAR** realistically sampled error probability, original SHIP-reachable leaf distribution, actual Poulpy numerical correctness, security, resource usage and contribution novelty. **NOT** an attack on original SHIP, **NOT** an actual full SHIP failure.

## Read-before-write, source and provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, preceding `findings/ship-memory-M11-single-scaled-bit-GLWE-second-column-precision-gate.md` SHA `4893d6bf11181f19cc8013693aeab2d93fa2af04`, current concurrent `findings/ship-memory-STATE.md` SHA `d242a19c4aff0fac2737cccdfbbfa7a20a9e9592` (**I211 in separate SHIP counter**) and shared `STATE.md` SHA `b02afcecbeb84fbcbed6f9ae675920ea56689bd8` (**vFHE V15**), latter two *only to prevent collisions*. **Do not overwrite either.** Earlier M05–M11 archives preserved. The M-series checkpoint is THIS self-contained immutable M12 record.

Scientific parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint **2025/784**, relevant §5.1/Algorithm 5 and real bootstrap output; cached Github mirror 33pp SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, original `VERSION_UNVERIFIED`. **The 18.1-bit output-precision reference is from a different cited original-paper setting; it is NOT a guarantee of the illustrative Poulpy parameter plan.**
Implementation sources from **independent Poulpy** pinned at `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, NOT authors' HEaaN:
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `hmux_rot_key_encrypt_sk` input secret `(β_d*s,β_d)`, output `σ_(g_d^-1)(s)`; full GGLWE rank_in2, rank_out1; `dnum=ceil(k_ct/(base2k*dsize)),k_aux=base2k*dsize`. Baseline source k_ct468,base2k52,dsize1 key precision 520 bits. **There is NO single-β-GLWE optimization in this code**.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: each mux group uses **all** candidate keys (including β0 keys with nonzero key encryption noise); candidate groups composed serially and Galois output automorphisms are applied per candidate.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: h32 leaf masked/mux phases feed a binary multiplication tree, real output is `root+Conj(root)`, which introduces an upper factor 2 on added root error.
- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: illustrative N16384,h32,theta4,window256,muxbase4,ld40,outputbudget104,base2k52 => `raised_k=468`, `mux_bases=[4,4,4,3]`, 15 candidate keys per support across four serial groups. Previous M02/M11 model of masked leaf effective precision k=428.
- `poulpy-core/src/noise_distribution.rs` blob `e231917a72be54a5e8dca47ece9f7d8672828020`: encrypted GLWE noise `Noise::ENCRYPTION = Gaussian{sigma:3.2}`, discrete Gaussian conditioned on integer coefficient `|e_i| <= floor(6*sigma)=19`; individual extreme support values are legal, **simultaneous 16384 extreme samples astronomically unlikely**. Their joint probability has NOT been calculated.
- No Poulpy Rust compiler or author-HEaaN execution is available for this session; all claims below are a mathematically exact **alternative helper model** and reproducible Python, not timing/precision measurements of Poulpy.

## ONE falsifiable primary hypothesis and ONE minimal gate

**[HYPOTHESIS M12]** At t=92 bits auxiliary guard (q=2^428 input, Q=2^520 β-GLWE helper, CKKS log_delta_work40), **all legal** independent β-key encryption noise coefficient vectors with |e_i|<=19, and all legal centered masked-body ciphertext polynomials |B_i|<q/2, can be substituted for the original β gadget column while **guaranteeing** the total extra error after 15 mux candidate-key contributions per leaf, h32 leaf-product tree and final real extraction is < the **reference** 2^-18.1 target, in an otherwise ideal stage model with all exact intended leaf factors of modulus <=1.

**[FALSIFIER]** First derive conservative full negacyclic ring norm+canonical slot bound. If > threshold, do **not** declare FAIL from the bound alone. Then find an explicit *legal helper encryption* (nonzero sampled-error vector within source support, real GLWE masking and secret), high-coefficient body B, and actual complex canonical slot error that, when inserted into a distinct ideal h32 real-output tree with all baseline factors 1, crosses threshold even when only ONE helper key per leaf contributes. A witness falsifies the asserted universal guarantee **in the stated independently admissible helper+ideal-tree model**. It does NOT show the exact family of intermediate B ciphertexts is reachable from the original SHIP `masking` stage for a single shared bootstrap input.

## Representation, rounding and noise assumptions [DERIVATION]

Let `R=Z[X]/(X^N+1)`, input-body integer polynomial `B∈R_q` at q=2^k, and a candidate replacement GLWE helper `Eβ=(a,b)∈R_Q^2` at Q=2^(k+t) decrypting to `β 2^t+e(X)` modulo Q, under fixed rank1 output secret s'. The evaluator publicly computes `B·(a,b)` modulo Q, then **independently rounds** a and b coefficientwise down t bits to R_q and GLWE-decrypts under s'. The desired decoded contribution is β B modulo q, while the extra error phase in integer q units is:
```
  E_out(X) = [B(X)*e(X)]/2^t + e_round(X)
```
where each normalized component contributes <=1/2 integer coefficient rounding, so `||e_round||_∞ <= (1+||s'||_1)/2` for ternary s' (independent of input q); for source-sized dense `||s'||_1<=N`, this gives a (very tiny on the huge torus precision) message-slot term ≤`N*(1+N)*2^(log_delta-k-1)`. No unproven statement that this exact helper/normalization exists as an optimised Poulpy kernel.

For `||B||∞<2^(k-1),||e||∞<=19`, negacyclic convolution `||B*e||∞ <= N *2^(k-1)*19`. Evaluate a q-torus ciphertext polynomial at CKKS canonical slot `ζ=e^(iπ/N)` (or any primitive odd 2N-th root): `|E(ζ)|<=N||E||∞`. Convert q-torus phase to message units by `2^(log_delta)/q`. Thus per helper candidate:
```
  eta_key <= 19*N*N*2^(log_delta-t-1)
          + N*(1+||s'||_1)*2^(log_delta-k-1).
```
At `N=16384,t92,log_delta40,k428`, the first term is **5.662441253662109375e-7 ≈2^-20.752**, and rounding bound using ||s'||1<=N is <2^-360.
Since all b candidate helper keys contribute nonzero noise even for β=0, summed candidate counts across four source mux groups `[4,4,4,3]` give `15 eta_key = 8.4936618804931640625e-6` extra slot error per leaf, provided ideal mux transforms preserve slot sup norm. Taking all ideal leaf factors |f_j|<=1 and h32 leaves, the root+conjugate extra error bound:
```
  eps_final <= 2*((1+15*eta_key)^32 - 1)
            = 0.0005436659315842420... (ignoring negligible rounding)
```
versus reference `2^-18.1=0.00000355923840155...` => bound about 153× reference. **This upper bound alone is NOT an actual correctness failure**, only insufficiency of a worst-case certificate. The calculation uses the paper's precision as a reference, NOT an actual Poulpy decoded precision.

For the **same very pessimistic helper-noise envelope alone** (giving it the entire original-error allowance, unrealistically), t=99 yields final bound ~4.246835308e-6 (FAIL certificate), t=100 yields ~2.123416562e-6 (PASS that very narrow numerical envelope). `t>=100` is therefore only a **sufficient precision threshold for this modeled sampled-noise term**, not a security estimate, latency bound, or recommendation; competing existing errors need their own margin.

## Executed 520-bit full-polynomial GLWE witness: not merely a loose upper bound

**Local runnable script (actually executed):** `/mnt/data/ship_m12_high_guard_full_polynomial_gate.py` SHA256 **`60a16a5a73154ea6048caaf898e20a1d6619ddb0564f6c965b1c8e5f43`**.
**Local result JSON:** `/mnt/data/ship_m12_high_guard_full_polynomial_results.json` SHA256 **`8f906af89a8bf502db10df10daf8167dbc138f5404e2f94351ab2aec92d12d9d`**.

At full N16384, with q2^428, Q2^520 and auxiliary t92, define
```
U(X) = (1+X+...+X^(N/2-1)) - (X^(N/2)+...+X^(N-1))
B(X) = (2^427-1) * U(X)                         (legal centered q body)
e(X) = 19 * U(X)                                 (every |e_i|=19, legal sampler support)
s'(X) = 1 + X^3 - X^7                            (ternary output secret)
ζ = exp(i*pi/N)
```
Each original helper plaintext is `β 2^t` constant in coefficient domain, and the test takes `β=0,1` × seeds `17,37,71,131`, generating **16,384 uniform pseudorandom auxiliary-modulus mask coefficients** per sample; body `b=β2^t + e - a*s'` modulo Q. The script exactly verifies that the true helper GLWE decrypts to `β2^t+e`. It then performs **actual** polynomial multiplication by B in R_Q, componentwise rounding t bits, decryption under s' at q, and evaluation of normalized **full-length error polynomial** at ζ. Polynomial arithmetic is **exact bigint ring arithmetic** optimized to O(N) for this specific explicit U (not general full-schoolbook O(N²)). It analytically checks `U²=-2 X^{N/2}(Σ_{i=0}^{N/2-1}X^i)² mod X^N+1`, with sample coefficients brute-force checked; final slot evaluation uses double-precision trigonometric summation (negligible numerical error at the reported scale). The helper noise e(X) is independently supported, not a repeated common ciphertext: M06 forbidden key-template equality is **not** introduced by these public-noise vectors alone.

**Results, 8/8 exact helper and output tests**:
- All helper encryptions/decryptions valid and componentwise coefficient rounding changes the noise polynomial by **<=2 integer coefficient units** relative to rational torus polynomial. Beta both 0 and 1 behave identically in the added-noise measurement.
- One candidate's *actual decoded canonical slot* noise at ζ has **Re ≈ 2.29490096535e-7** (Im tiny, ~−4.4e-11), which is **less than 2^-18.1**.
- The analytic closed-form slot calculation is
```
U(ζ) = exp(-i*pi/(2N)) / sin(pi/(2N)),
delta_slot = (19*(2^427-1)/2^428) * 2^(40-92) * U(ζ)^2.
```
- When **one** such valid helper error is hypothetically applied to each of 32 independent leaves with ideal leaf value 1 and all other mux/errors taken zero, the **separate ideal product-tree** formula `2*Re[(1+delta_slot)^32 - 1]` gives **1.46874184e-5 > 3.5592384e-6**, i.e. over **4.1×** the reference threshold, even without using all 15 mux candidate errors per leaf.
- **CRITICAL LIMITATION**: `B(X)=(q/2-1)U(X)` for all leaves, all source-candidate per-key β positions, and all 32 ideal factors =1 were *chosen at independently valid helper/key/slot levels*. We have **NOT proven they can co-occur as 32 masking/mux leaf states derived from a single real SHIP input and original encrypted selector masks**, hence **no published-SHIP full-execution counterexample or numerical failure probability follows**. Extreme e_i=±19 simultaneously over N coefficients is astronomically improbable under sigma3.2; no statistical soundness/security failure claim is justified. The conditional tree is an algebraic stress test, not a compiled end-to-end test.

## Judgment / end-of-iteration protocol

**[FACT]** Poulpy HMux original key uses gadget decomposition and auxiliary precision; source error sampler Gaussian sigma3.2 truncated at ±19; the second column encodes β in rank2 input secret. Original SHIP is unchanged.
**[DERIVATION]** A single 520-bit scaled-β GLWE helper with unrestricted legal large-body multipliers amplifies sampled encryption error by `B(X)e(X)/2^92`, full polynomial and slot amplification can exhaust a pessimistic output budget. Tight analytic N-specific legal support witness exists for the independent-helper plus ideal-product-tree model; **NOT a full SHIP source-input reachability witness**.
**[SPECULATION]** Realistic independent Gaussian e with typical ∼3.2 coefficient magnitude and ciphertext body distributions may lead to far smaller *probabilistic* slot errors via cancellation; needs a valid joint distribution or measured Poulpy runner; worst-case support events are not evidence of practical failure. t100 guard is not a guarantee against backend rounding, security, first βs gadget column or original bootstrap errors.
**STATUS:** FAIL M12's universal worst-case **idealized** t92 output guarantee; PASS deterministic bigint GLWE witness/source noise envelope; UNCLEAR practical end-to-end CKKS precision/latency/security/memory, **NO novelty verified**.
**RESULT:** `eta_key≤5.66e-7`, 15-candidate/leaf bounded `8.49e-6`, final h32 real output pessimistic ≤`5.44e-4`, above nominal `3.56e-6`; exact legal e=19U,B=(q/2-1)U at full N yields canonical slot `2.295e-7`, ideal 32-leaf/re-extract amplification `1.469e-5`. Pessimistic helper-only margin would need t>=100.
**NEXT_ACTION (SHIP-M13 only on PI continuation):** ONE **distribution-aware practical precision gate**, not another extreme-error support witness. Ground a variance/tail estimate in the *joint distribution of actual masked leaf bodies and independently sampled beta helpers*, including public per-rotation automorphisms and selector correlations, or implement a real Poulpy dual-kernel experiment to measure noise/precision and latency. If the true masked-body distribution cannot be independently authenticated from source or compiled, mark **UNCLEAR/HUMAN_REVIEW** rather than inventing Gaussian independence/tail bounds. If a large-guard helper requires ~528bit precision and expensive public-wide polynomial multiplication, separately decide whether expected prepared-key payload savings justify online work. Avoid overlapping I211+ security work; no automatic new parent.
**STATE_UPDATE:** YES standalone M12 immutable finding; **NO edits** to global vFHE `STATE.md` or concurrently managed SHIP `findings/ship-memory-STATE.md`. This record is sufficient to resume M13 without guessing.
