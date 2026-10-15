# CGS-32 — Dummy covariance: fresh per-session noise has wrong JOINT law; persistent dummy needs known-covariance MLWE

**Date:** 2026-10-15. **One active FHE research task:** CGS, root `STATE.md` previous CGS-31. One primary technical hypothesis and the cheapest two-session probability test. No dedicated research-track MCP; no unrelated repository topics edited.

## Primary hypothesis and test

**H-CGS32 [FAIL for per-session dummy; UNCLEAR for ONE persistent dummy]:** In Okada–Takagi 2025/409 §7, omit secret-conditioned session-specific shared Gaussian ζ and let a simulator sample an **independent fake secret covariance Σ'** from the legitimate source secret distribution. Because each Gaussian noise marginal after averaging the secret is correct, one can sample a new Σ' for EACH ODec session without violating the adaptive multi-session joint transcript. Moreover, switching to ONE persistent Σ' across all sessions should be justifiable directly from original STANDARD MLWE with no extra leakage assumption.

**ONE cheapest decisive test:** Fix one Gaussian-surrogate secret distribution with nonconstant norm M, choose a bounded event A on the leaked decrypted residual, and compare the probability of A in TWO sessions for (i) real common key M, (ii) fake M'_sid resampled each session, (iii) one persistent fake M' sampled once. Then identify the exact missing public-key joint computational assumption of (iii), rather than mistaking Gaussian marginal correctness for ThFHE security.

## Original sources, verified claim boundary [FACT]

- **Hiroki Okada, Tsuyoshi Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025 / IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409. Full cached original physical 40pp, SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, version status unverified. **Physical p8 §2.2** explicitly states that known-norm LWE has a standard-LWE reduction but **known-covariance ring-LWE lacks a known reduction from standard RLWE**. Source **Definition3.15/3.16 p15** distinguishes knLWE vs ordinary MLWE. **Algorithm5 physical p23** releases `(ctdec,{pdi}_{i∈act})` for each adaptive ODec, while **Algorithm3 p19/Algorithm7 p29** use one fixed underlying secret for all sessions.
- **Source Lemma5.1 Eq(14) pp20–21:** after smoothing/rounding analysis, the conditioned scalar latent error `e0` is close to half-integer-lattice Gaussian of squared width `(pσ0||s||)²+σflood²`. **Lemma7.1 Eq25 p30** generalizes to matrix width `p²σ0²Σ_s+σflood² I`. This dependence is on the ONE original secret across all sessions; the source's per-sid ζ removes it. **Theorem5.5 p24 and Theorem7.5 p32** show original simulator obligations, which are significantly stronger than checking the noisy marginal distribution.
- **Daniele Micciancio and Adam Suhl**, *Simulation-Secure Threshold PKE from LWE with Polynomial Modulus*, ePrint **2023/1728**, https://eprint.iacr.org/2023/1728. Public full article intro says scalar known-norm LWE equivalent/reducible to standard LWE, but a ring extension called **known-covariance RLWE** is introduced as a separate assumption, with demonstrating equivalence to standard RLWE explicitly left open. This exact prior-art limitation is consistent with Okada–Takagi 2025/409; no 2026 standard-MLWE reduction has been verified in this iteration.

## A general two-session theorem, including the FIX [DERIVATION]

Let `S` be sampled ONCE per KeyGen from any source key distribution; `M=f(S)` is its norm/covariance, and `G_m` is a probability distribution for one source-style decrypted noise residual. Assume independent session noise conditional on M, as in the idealized Gaussian-surrogate source lemma. For any bounded measurable event A, define `p_m=Pr_{Y←G_m}[Y∈A]`.

**Real fixed-key residuals:** `M←D_M; Y_1,Y_2|M iid G_M`. 
**Fresh-per-session dummy:** `M'_1,M'_2 iid D_M; Y_t|M'_t←G_{M'_t}`.
Both have **identical one-session marginal** `Y∼E_M[G_M]`, but
```
Pr_real[Y1∈A and Y2∈A] = E_M[p_M²],
Pr_fresh[Y1∈A and Y2∈A] = (E_M[p_M])²,
DIFFERENCE = Var_M(p_M) >=0.
```
Whenever p_M is not almost surely constant, the event `A×A` is an unconditional TWO-session distinguisher between these noise-only mixture laws. This is a one-line variance-identity, not a new cryptographic result. With polynomially separated conditional event probabilities, the gap can remain inverse-polynomial asymptotically (the toy alone does not prove universal asymptotic security failure).

**Fix for that one problem:** Sample `M'←D_M` ONCE at simulator startup, then use that SAME M' in every session. With no public key/side information, the complete residual-only mixture `E_M[G_M^{⊗L}]` is IDENTICALLY DISTRIBUTED for real M and persistent independent fake M' for ANY L. Hence the two-session noise-only attack DOES NOT apply to a persistent dummy. A fake M' independently redrawn **per query** is genuinely invalid. The source ideal game also uses multiple active sets and joint masks; no claim that the Gaussian-only equality proves its correctness.

## The real COMPUTATIONAL obstacle for one persistent dummy [DERIVATION / unproved assumption]

Let `PK(S)` be the native Module-LWE public key under a key S, and `K(S)=Σ_S` its secret-conditioned covariance. The persistent-dummy computational hybrid needs something at least as strong as
```
(PK(S), K(S)) ≈c (PK(S), K(S')),   S' independent from S and identically sampled,
```
with analogous augmentation for evaluation keys and other public material. A NATURAL SUFFICIENT ASSUMPTION is known-covariance MLWE:
```
(A, A S+e, Σ_S) ≈c (A, U, Σ_S).
```
Then triangle + ordinary MLWE hybrid gives the desired decorrelation for **native PK only**:
```
(PK(S), Σ_S)
  ≈c (UniformPK, Σ_S)
  ≡  (UniformPK, Σ_S')
  ≈c (PK(S), Σ_S').
```
But ordinary `(A,AS+e)≈c(A,U)` **without Σ_S side information** is NOT a direct reduction to known-covariance MLWE. The challenger’s secret S is hidden from an ordinary-MLWE reduction, so this standard black-box hybrid has a missing interface. It cannot be repaired merely by sampling an independent fake norm. **Scalar known-norm LWE has specialized prior-art reductions; transferring them to ring-structured Σ is exactly the open technical issue identified by the authors.** And underlying FHE evaluation keys depending on S may require even stronger augmented hardness/circular-security assumptions.

**Why transcript estimation makes this a substantive barrier:** In an idealized continuous Gaussian scalar setting with `Y_t|M∼N(0,v_0+a M)`, `a>0`, `M` is an integer polynomially bounded and `v_0+aM` polynomial, a polynomial number of noise samples recovers M to high probability: sample variance has `Var[(1/L)Σ_t Y_t²|M]=2(v_0+aM)²/L`. Round `(sample_variance−v_0)/a` to nearest integer; Chebyshev gives probability of error at most `8(v_0+aM)²/(L a²)`. Choose L polynomially large and use a median-of-means amplification (O(κ) blocks) for 2^-κ failure. Analogously, from n-dimensional continuous Gaussian samples with width covariance public background + `σ0² Σ_S`, one can polynomially estimate the bounded integer covariance entries. Hence, **in the Gaussian-surrogate joint experiment with enough sessions, leaking noisy residual samples computationally approximates revealing K(S)**. A hybrid that substitutes an independent persistent K' thus requires joint PK–K decoupling, not just matching noise marginals. This is a conditional analogy, NOT an established estimator guarantee for actual source discrete randomized rounding, mod-q wrap, PRF masked/reshaped adaptive transcript, or source q parameters.

## ONE reproducible exact mixture experiment [EXECUTED]

Local script `/mnt/data/cgs32_dummy_covariance_joint_gate.py`, SHA256 `14fb02f87d50448223f1448f03647b28c8e7566d65241e004ec88587df0decf1`; JSON `/mnt/data/cgs32_dummy_covariance_joint_gate.json`, SHA256 `f933913f3daab5443dd5317f70ddfeb74e42264257cbc07f93d0bdf8ee12d503`. Independent toy: n=8 binary key bits iid Ber(1/2), `M=||s||²∼Binomial(8,1/2)`; scalar noise `Y|M∼D_{(1/2)Z, sqrt(9+4M)}`, with Gaussian convention mass `exp(-πy²/(9+4M))`. Event A: `|Y|≤2`. Compute p_m using a symmetric half-lattice grid through |x|=60; Gaussian tail mass bound per distribution <`3.87×10^-120`.

```
Pr_real[A1 and A2]                     = 0.5613940170475422
Pr_fresh_dummy_per_session[A1 and A2] = 0.5582996107547561
Difference                            = 0.0030944062927861
Pr_persistent_dummy[A1 and A2]        = 0.5613940170475422
```

Thus we have a concrete, observable two-session event even when EACH separate Y has exactly the correct mixture distribution. This is toy **noise-only** mathematics, **not** an attack on Okada–Takagi full adaptive Algorithm5, which also includes public key, ciphertexts, potentially non-independent errors and output modular reduction. It establishes the necessary per-key correlation rule for any dummy-noise protocol proof.

## Constructive synthesis and decision

- **PASS** two-session analytic counterexample to independent per-ODec dummy covariance; independently validated discrete Gaussian finite mixture.
- **PASS** correction: ONE fixed dummy covariance sampled at KeyGen is exactly marginally consistent for Gaussian-noise-only whole lifetime, without public PK.
- **OPEN** persistent dummy + public PK/Eval joint computational proof; would require existing or new known-covariance MLWE-style leakage-resilient reduction (or a novel simulator that avoids that requirement).
- **NOT NOVEL** simply resampling dummy norm, nor the binomial mixture variance formula, nor scalar known-norm LWE. No complete secure low-q ThFHE or removal of O(LDec) under standard MLWE is obtained.

**END OF ITERATION**
- `ITERATION: CGS-32`.
- `STATUS: FAIL` fresh-per-session dummy; `PASS` minimal joint-view failure and persistent dummy marginal repair; `HUMAN_REVIEW/UNCLEAR` native MLWE public-key/evaluation-key joint simulator.
- `RESULT:` Need ONE hidden per-key covariance shared across all sessions; fake once avoids marginal consistency objection but brings us back to source identified known-covariance RLWE/MLWE security gap. O(LDec) original problem OPEN.
- `NEXT_TEST CGS-33 (PI next continue):` ONE **real source-law and computational-security** gate for persistent dummy: formulate exact auxiliary-input MLWE challenge with `Σ_S` (or a lower-dimensional trace/secret-norm leakage) and check whether a *specific* existing reduction from standard MLWE, perhaps using distribution-preserving rerandomization, yields required `(PK,Σ_S)≈(PK,Σ_{S'})`. Prioritize scalar knLWE theorem assumptions as positive control vs ring covariance failure; do NOT just state “known covariance open”. If no reduction/valid construction, PARK dummy covariance and return to genuinely secret-dependent, threshold-shareable Gaussian sampler. Consider actual evk/circular security only after base joint reduction passes. One hypothesis one falsifier.
- `STATE_UPDATE: YES` own finding + detailed CGS checkpoint + single root STATE.
