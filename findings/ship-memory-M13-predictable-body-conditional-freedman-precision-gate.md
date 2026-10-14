# SHIP-M13 — Conditional bounded-variance precision certificate for the proposed 92-bit β-GLWE helper

**Date:** 2026-10-14 (Asia/Tokyo). **Independent research stream:** SHIP M-series; **M13 COMPLETED, M14 NOT STARTED**. PI authorized M12's next action by “好的，请继续”. **NO edits** to simultaneously maintained SHIP I-series or global vFHE V-series.
**Parent objective:** Reduce dominant per-candidate rank2 HMux prepared GGLWE memory, retaining first (βs) gadget column and replacing *second* β gadget column with one 520-bit scaled-β GLWE plus a ciphertext×public-body polynomial multiplication.
**STATUS:** **PASS — narrow, conditional mathematical concentration certificate for incremental β-helper-only error**, with precise independently sampled noise/predictable-body/ideal-mux conditions stated below. **UNCLEAR / IMPLEMENTATION_BLOCKED** as a claim about an actual secure/publicly supplied Poulpy/SHIP β-helper, output CKKS precision, actual latency/RSS or novelty. The original SHIP implementation has no such helper. **Not a formal 128-bit security proof.**

## Read before write & anti-conflict

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, M12 `findings/ship-memory-M12-beta-GLWE-92bit-full-polynomial-noise-gate.md` SHA `dec65723ff6c58ddd22266e7c454dd7ef06387ec`, M11; concurrently maintained `findings/ship-memory-STATE.md` SHA `3aabc653e6f69164362b1f5f21d0e041ea94ea7a` **I213** and separate global `STATE.md` SHA `7af97fb3ee38ae139fd12f867fd9eccb18d22d16` **vFHE V17** only to avoid conflicts. Neither shared state is written. This file is the sole M13 persistence and contains the restart pointer.

Original scientific parent: Cheon, Hanrot, Kim and Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025 / ePrint 2025/784, §4.4, §5.1 Algorithm 5; previously cached ePrint mirror full PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. The 18.1-bit paper precision reference was reported for a DIFFERENT experimental parameter setting; it is a **chosen diagnostic threshold** here, NOT a validated claim for our illustrative Poulpy configuration. Code source **independent Poulpy, not authors' HEaaN**, pinned immutable commit `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.

## Specific primary hypothesis and decisive test

**[HYPOTHESIS M13]** For **one honest, nonadaptive real SHIP bootstrap** of the source-shaped N=16384,h=32,log_gamma=6,theta=4,base52/log_delta40 setup, let each of the K=480 **NEW** proposed β-helper key-error coefficient samples be conditionally centered, independent truncated-Gaussian `|e_i|<=19,Var(e_i)<=3.2²`, and let each public masked input-body polynomial B be **predictable relative to its current helper noise**, with **no assumption on B's own distribution** beyond centered `|B_i|<2^427`. Assume ideal exact mux Galois transport and ideal error-free cleartext leaf phases, with other FHE errors set to zero. Then the **added helper-only real-output error across all 8192 canonical slots** stays below `2^-18.1` with probability at least `1-2^-128`, even though an unconditional worst-case support error certificate failed in M12.

**[ONE DECISIVE TEST]** Source-audit actual encryption-noise support **and variance**, actual masked phase leaves and non-unit pt0 factor, exact mux tree counts. Derive a conditional martingale Freedman/Bernstein tail that is uniform over **all predictable legal B polynomials**, with nonlinear product-tree remainder bounded deterministically. If its 8192-slot union tail upper bound exceeds 2^-128, hypothesis FAIL or UNCLEAR; **do not substitute a Monte Carlo proxy or assume independent/uniform bodies**.

## Pinned source-grounded facts

1. `poulpy-core/src/noise_distribution.rs` blob `e231917a72be54a5e8dca47ece9f7d8672828020`: `Noise::ENCRYPTION=Gaussian{sigma:3.2}`, every integer sample is clipped to `[-19,19]`; `Noise::variance()` returns `sigma*sigma` as an **upper estimate after clipping**. Thus under the independent-samples probability idealization, variance proxy V_e=10.24 and per-sample absolute support19.
2. `poulpy-core/src/reference/encryption/glwe.rs` blob `8caec305a9412fa769bf36ccea122cbeae3bd697`: real GLWE secret-key encryptor injects `Noise::ENCRYPTION` via `vec_znx_add_noise` in ciphertext body. This establishes the *sampling interface*, **NOT** the independence of proposed NEW β helpers with existing key material.
3. `poulpy-hal/src/source.rs` blob `cf5014e592679995d10aae43575c570631cd93ec`: `Source` uses deterministic `ChaCha8Rng`; its own doc explicitly warns **“Not suitable for cryptographic key generation.”** It is for reproducible tests/noise sampling. The conditional concentration theorem is a statement about an ideal fresh independent noise experiment, not a proof for this concrete PRG's joint output or evaluation-key security. **Do not call it cryptographically secure because the Rust struct has `Source` in its name.**
4. `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: the CURRENT HMux key remains full rank2 GGLWE, `(βs,β)→σ_{g^-1}(s)`; masks and other mux keys generated with shared mutable noise/mask sources in a known loop order. There is **NO single β-GLWE alternative and no source-backed joint-key independence guarantee**.
5. `poulpy-ckks/src/encoding/ship/masks.rs` blob `2754eafd1ad24c1eca1382204d37005449f88cca`: exact cleartext selector bands are onehot, partition unity and choose one public unit phase per slot. `poulpy-ckks/src/encoding/ship/coeff_enc.rs` blob `e0b5bb3e2cd5bb681a22b1798039061429ba17fe`: `pi` values are cos/sin (magnitude1); and **pt0 phase magnitude is γ/(4π)**, not one. This **corrects a missing factor in M12**. `poulpy-ckks/src/test_suite/ship.rs` blob `a5e89638c430886e57c036e001093827293bfae0`: illustrative source log_gamma=6 -> |pt0|=64/(4π)=5.09295817894. Multiplication tree product ideal mux leaves each modulus1, and root+conj factor2.
6. `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: h32, four mux groups [4,4,4,3], 15 candidate GGLWE contributions per leaf. `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542`: h32 nontrivial leaves+pt0, binary tree and real root+conj.
7. ***No actual masked-body probability law is claimed.*** The only B fact used is a centered modular coefficient range, which remains true for any legal normalized ciphertext body. In an honest-input, fresh helper idealization, current B is produced by masks and **previous** mux groups before using current helper error; it may depend on earlier helper errors (predictable martingale coefficients), so normal iid-B simplifications are not required. This predictability **can fail for adaptive inputs selected after inspecting the public evaluation keys**, and is not proven by source alone.

## Math: conditional noise concentration without specifying B's law

Set N=2^14, input modulus q=2^428, helper modulus Q=2^520 (t=92), working message scaling Δ=2^40, h32, four mux groups K/h=4+4+4+3=15 per leaf, total K=480.

For each helper key and any primitive canonical slot ζ, the ideal incremental decoded error from the 2nd-column proposal is
```
    δ_jd(ζ) = 2^(40−428−92) B_jd(ζ) e_jd(ζ)
```
with a negligible coefficientwise GLWE normalization residue bound. Negacyclic product becomes ordinary multiplication under ζ. From `|B_i|<2^427`,
```
  |B(ζ)| < N*2^427,
  |one noise coefficient's complex weight| ≤
  w := (N/2) 2^(40−92) = 1.8189894035458565e-12.
```
Every new helper e coefficient is conditionally centered and bounded |e_i|≤19; variance ≤10.24. Public Galois automorphisms only permute canonical slots and their phases, so do not alter the slot sup bound. An ideal leaf accumulates ≤15 such error terms, each of deterministic absolute slot magnitude at most `η_key=19Nw=5.662441253662109e-7`; hence `η_leaf=15η_key=8.493661880493164e-6`.

The actual source pt0 contributes **A=γ/(4π)=64/(4π)=5.092958...**. Write the real output as `F=2Re[f0 ∏_{j=1}^h (f_j+E_j)]`, with `|f0|=A, |f_j|=1` in the exact desired cleartext representation. Separate first-order helper error L and nonlinear remainder R. By binomial expansion and deterministic clipping,
```
  |R| ≤ 2A * Σ_{r=2}^{h} binom(h,r) η_leaf^r
      = 3.6450929485210726e-7.
```
Independently, if secret s' has ternary coefficients and `||s'||1≤N`, componentwise t-bit round of rank1 GLWE multiplication contributes an ultra-small bound `R_round≤1.05e-105` in message-domain units for this ideal helper; actual backend FFT/NTT error is **not** bounded by this.

For **each fixed real-output canonical slot**, the linear first-order term L is a sum of at most K*N=7,864,320 individual helper error coefficients times (possibly predictable) real weights `c_{jdi}`. Because f0, all other ideal leaves and rotations have modulus bound A,1,1 respectively, every weight satisfies
```
   |c_{jdi}| ≤ c := 2A w = 1.8528073920390492e-11.
```
Under independent fresh coefficient sampling conditional on prior stages, these summands form centered martingale differences. Their total predictable conditional variance is bounded by
```
   V := K*N*10.24*c² = 2.7645323910020433e-14,
```
and each increment absolute value ≤`M:=19*c=3.520334044874194e-10`. The martingale Freedman/Bernstein two-sided tail gives
```
  P(|L| ≥ x) ≤ 2 exp[-x² / (2(V + M*x/3))].
```
Take the **reference** threshold `ε*=2^-18.1=3.5592384015533696e-6`; reserve deterministic nonlinear+rounding margin `x=ε*−R−R_round=3.1947291067012624e-6`. Exponent becomes `x²/[2(V+M x/3)] =182.12381177217082`; per-slot failure bound `≈10^-78.7943` and union over all 8192 slots:
```
  P(exists CKKS slot with helper-only |extra error| ≥ ε*)
       ≤ 8192 * 2 * exp(-182.1238)
       ≈ 1.315e-75 = 2^-248.749.
```
This is **much smaller than 2^-128 in the stated ideal conditional experiment**. It is **not** a 248-bit cryptographic security claim, no estimate of real SHIP input distribution, and does not account for the original scheme's accuracy budget.

**Why the source variance matters:** Applying Hoeffding solely with cutoff|e_i|≤19 in exactly this non-unit pt0 model yields a useless union probability upper bound >1 (real-output exponent only ~5.24). The source variance≤10.24 and Bernstein bounded-increment correction are essential. All non-linear terms are bounded worst-case and are not incorrectly treated as centered or independent.

## Reproducible executed one gate

**Actual Python arithmetic, no CKKS runtime:** `/mnt/data/ship_m13_predictable_body_freedman_gate.py` SHA256 `ed06059410a14cd23b0d06d5bb9eb432cb8ca06240442acaa7c032c58c781ed5`.
**Output JSON:** `/mnt/data/ship_m13_predictable_body_freedman_results.json` SHA256 `b2f8678ed05fcd3720c89e2ae17856f101fb8b677e5c93984cce6c0ea84bce6`.
One exact-integer input-shape + floating mathematical probability-bound calculation was executed; assertions included K480, nonzero positive margin, variance-based union exponent >128 bits. No fake Monte Carlo / timing claims.

## What is PROVEN / not proven

**[FACT]** Source implements clipped Gaussian 3.2 (support[-19,19], variance-upper10.24), cleartext unit-modulus mask-selected phases and **nonunit** pt0 amplitude gamma/(4π), stage counts. Source does **not** implement the proposed β-helper nor a proof that its error is conditionally independent of any future chosen input masked B. `Source` is explicitly documented non-keygen secure.
**[DERIVATION — PASS CONDITIONED]** Under honest non-adaptive inputs, ideal fresh independent β-helper coefficient noise, current-body predictability, exact Galois/mux transport, zero other error, and exact intended leaf magnitudes, a variance-sensitive full h32-tree+pt0+final-real high-probability bound **below** the nominal 18.1-bit threshold exists for t92, even without any assumed B distribution. M12's universal worst-case support FAIL and this *probabilistic* PASS are consistent: M12 uses extreme simultaneous e_i=±19 events of vanishing probability.
**[OPEN / NOT A CLAIM]** Joint key/security distribution; pseudorandom noise independence with public key reuse/chosen inputs; actual masked-body support correlations due original/beta helper keys; potential massive online 520-bit public polynomial multiplication; correctness of exact 520-bit signed coefficient multiply / normalize in Poulpy; finite-precision NTT backend errors; other FHE noise consuming precision margin; actual measured precision, peak RSS, wall time; 18.1-bit applicability; contribution novelty.

## End-of-iteration

**STATUS:** **PASS_CONDITIONAL** source-parameter + mathematical concentration gate for helper-only incremental noise; **UNCLEAR/HUMAN_REVIEW** actual FHE security/accuracy/performance and algorithm integration, **NOVELTY NOT VERIFIED**.
**RESULT:** With f0=5.093 corrected from source and variance proxy10.24, rigorously modeled helper-only all-8192-slot tail ≤2^-248.75 (under explicit independence/predictable B), versus M12 high-probability doubts based on extreme support. This neither repairs M12's universal worst-case counterexample nor establishes implementation success.
**NEXT_ACTION — M14 ONLY IF PI CONTINUES:** One **source-specific online-cost/correctness feasibility gate** for doing a public **428-bit polynomial body × one 520-bit β-GLWE** and 92-bit coefficientwise normalization using available IFMA/NTT primitives without regenerating second gadget column; count buffer bytes, DFT preps/products and any extra high-precision widths. If real Poulpy runner becomes available, prefer implementation and actual decrypted slot-error/latency/peak RSS on pinned hash. Do NOT repeat synthetic Gaussian simulations as if they were FHE benchmarks, and do NOT duplicate concurrent I213+ β-sharing security trajectory. If source refactor/feasibility can't be established, mark UNCLEAR/HUMAN_REVIEW. PI retains decision to park.
**STATE_UPDATE:** YES standalone immutable `findings/ship-memory-M13-predictable-body-conditional-freedman-precision-gate.md`. NO writes to global `STATE.md` or concurrent `findings/ship-memory-STATE.md`. This file is the independent restart/checkpoint.
