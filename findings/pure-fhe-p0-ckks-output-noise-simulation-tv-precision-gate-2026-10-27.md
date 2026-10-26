# PURE-FHE · P0-PRESCOUT-41 — CKKS independent output perturbation: statistical privacy versus numerical precision

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: APPROXIMATE_FHE_OUTPUT_RANDOMIZATION_SOURCE_GATE
PREVIOUS: P0-PRESCOUT-40, findings/pure-fhe-p0-gl-matrix-karatsuba-bilinear-rank-gate-2026-10-27.md, commit 37d7c970be1d457ed975964741bc7859a8fc34f8
LATEST_COMPLETED: P0-PRESCOUT-41
NEXT_ITERATION: P0-PRESCOUT-42 NOT_STARTED
STATUS: FAIL_CHEAP_INDEPENDENT_GAUSSIAN_STRONG_STATISTICAL_HIDING / PASS_EXACT_TV_GATE / CURRENT_PUBLISHABLE_NOVELTY_NOT_ESTABLISHED
CODEX_REQUIRED: NO (no native FHE, GPU, remote environment, models or code changes).
STATE_UPDATE: YES this isolated PURE-FHE findings file; root STATE.md and unrelated active research lines unchanged.

## One primary falsifiable H41

Consider approximate CKKS homomorphic evaluations C0, C1 which have the SAME ideal normalized numerical output m but small different numerical residuals e0 != e1 at a single real coordinate. Can the evaluator merely append a SMALL FRESH INDEPENDENT Gaussian noise Z~N(0,sigma^2) to the decrypted numerical output (or homomorphically before final decryption) and thereby achieve **strong statistical hiding** of the computation-dependent residual, with total-variation distinguishing advantage ≤2^-128, while preserving useful high precision?

The question is intentionally narrower and STRONGER than established 2025/203 BFV ciphertext simulatability (which gives the simulator the circuit C, sk, evk, input ciphertexts and ideal output) and different from 2025/382 CKKS differentially private homomorphic evaluation (DPHE), which bounds max-divergence under its approximate result idealization. Do NOT claim either source proved a general CKKS statistical full circuit-privacy guarantee or that the exact same security notions are compared.

Minimal decisive test: for idealized deterministic residual shifts, compute EXACT total variation of the two normally distributed numerical outputs, then compare the sigma required for statistical 2^-128 to a fixed numerical precision budget. This is a **one-coordinate lower bound** and does not require any native cryptography, noise tail assumptions from FHE, or GPU experiment.

## [FACT] Primary first-party-source checks

1. Hwang, Min, Song, *Ciphertext-Simulatable HE from BFV with Randomized Evaluation*, ePrint 2025/203, https://eprint.iacr.org/2025/203, 44-page cached PDF from Github Notes, SHA256 cc94c3a7025e97445ca1df7b5ed0aed5123aa07a8a11c742c37327583c54fdb1, VERSION_UNVERIFIED. Physical pp3–5 §1.1–1.2, p20 Table1 and p21–22 §5.4 Theorems3,4 read. Definition gives BFV ciphertext simulator explicit sk, evk, original input ciphertexts, actual output m, known *public* circuit C, but NOT evaluator's private server data. It does NOT aim to hide circuit shape in the strong CP sense. Author randomized evaluation comprises randomized lifting and smoothing, ciphertext randomizer, Beaver-like plaintext masking for ciphertext multiply, randomness at each relevant gate; reported up to 7.20× speedup versus BFV traditional flooding in source's application example and about 30% slowdown to ordinary BFV under its setup. Its Theorem3 checks error simulatable when B_out≤Delta/2; Theorem4 also requires B_out+B_rand≤Delta/2. This is a sophisticated gate-by-gate **AUTHOR** construction, and output-only additive Gaussian perturbation is NOT its algorithm.
2. Hwang, Min, Seo, Song, *On the Security and Privacy of CKKS-based Homomorphic Evaluation Protocols*, ePrint 2025/382, https://eprint.iacr.org/2025/382, 49-page cached PDF SHA256 29494a3144f20cc732e18fad12997d8fa0e49c58ec5c5fe4d9e8ad71b24c9331, VERSION_UNVERIFIED. Physical pp1–5 §1, pp6–8 §2.1–2.2 inspected. It introduces CKKS-specific DPHE and a Laplace-noise compiler with Enc(0), explicit scale Delta and receiver well-formedness ZKAoK for malicious receivers; purposefully RELAXES the exact circuit-simulation requirement to a DP-like divergence/privacy goal. It already observes strong exact-HE noise flooding has utility loss in approximate CKKS. This is strong prior art and the direct motivation of this exact gate.
3. ePrint 2025/395 *Provably Secure Approximate Computation Protocols from CKKS* listed on Yongsoo Song's first-party publications https://yongsoosong.github.io/publications/, but the PDF could not be acquired in current Notes due INVALID_PDF. Do NOT assume its proofs, circuit privacy guarantees, or algorithm details. Current latest October 2026 ePrint2026/2546 also revisits BFV/BGV IND-CPA-D attack scope, but its full text has not been reviewed; no concrete implication or parameter assertion transferred to this H41.
4. Similar 2026 recent approaches focusing on shaped rounding/precision allocation explicitly trade slot count or change representation; do not assert simply adding Gaussian output noise competes with them.

## [DERIVATION] Exact total-variation law

Fix a real numerical output m. Suppose the ideal residuals e0,e1 are deterministic and differ by d=|e0−e1|>0. After appending an independent centered Gaussian Z~N(0,sigma^2), the receiver sees
 Y0=m+e0+Z, Y1=m+e1+Z.
These distributions are N(m+e0,sigma^2) and N(m+e1,sigma^2). Their exact total variation (optimal one-sample distinguishing advantage in the convention sup_A |P0(A)−P1(A)|) is
 TV(Y0,Y1)=2 Phi(d/(2sigma))−1=erf(d/(2sqrt(2)*sigma)).
Consequently, TV≤2^-lambda iff
 sigma≥ d/(2sqrt(2)*erfinv(2^-lambda)).
For large lambda, erfinv(eps)~sqrt(pi)*eps/2, so
 sigma ≳ (2^lambda/sqrt(2pi))*d.
This is a simple classical statistical no-go for **independent output-only Gaussian smoothing** under the demanding 2^-lambda statistical privacy target. It is NOT a no-go for all circuit-randomized FHE constructions, computational circuit privacy, ciphertext simulatability, or DPHE.

## [TOY_EXECUTED] High-precision output numerical example

Use d=2^-40 in decrypted numerical units and demand TV≤2^-128. High-precision mpmath erfinv gives
 sigma_min=1.23466655568187191e26 ≈2^86.67425193526384.
Conversely fix useful output numerical standard-deviation budget sigma=2^-20, then
 TV=erf(2^-20/(2sqrt(2)))=3.8046100654737239816e-7≈2^-21.325748064736214.
This greatly exceeds 2^-128. The toy's e0/e1 and sigma are schematic, NOT measured CKKS error distributions or a theorem that these shifts necessarily occur at this magnitude in published BFV/CKKS implementations. Scaling is expressed in already-decrypted numerical coordinates (no omitted CKKS Delta factors); no inference of exact RNS modulus Q or DFR.

Note: Residual difference d is a difference in circuit-leakage observables; full circuit privacy may condition on hidden circuit whereas the 2025/203 simulator is explicitly given C. The two security games are not equivalent. An algorithm which designs its noise distribution gate-by-gate so that conditional errors do NOT differ by d after simulation (as in 2025/203), or uses a DPHE goal (2025/382), escapes this toy bound.

## Novelty/practical decision

H41 FAIL: independent final-output tiny Gaussian noise cannot guarantee a 2^-128 statistical hiding of nonzero residual shifts in a general model while retaining useful precision. This follows from textbook Gaussian TV and is already the motivation behind source literature's more involved randomization/security notions. No new positive cryptographic primitive, native performance improvement, security attack, or flaw in the two original papers demonstrated.

Potential high-value *separate* fundamental question: whether a circuit-aware, CKKS-specific **error simulator** can use randomized relinearization/rescale/eval to hide residual dependence at a bounded precision cost, but existing 2025/382 DPHE and newer 2025/395 first-party work need FULL source and exact threat-game comparison. A trivial output-only noise addition, flooding or ordinary randomized lifting is high prior art. Do NOT open many similar Gaussian-param toy rounds. More productive future portfolio decision is whether PI wishes to prioritize Pure-FHE cryptographic schemes or security/verification/compiler applications; current broad source-first P0 has stagnated after 41 screens.

End of iteration:
STATUS: FAIL_OUTPUT_GAUSSIAN_CIRCUIT_RESIDUAL_2^-128 / PASS_TV_PRECISION_LOWER_BOUND / HUMAN_REVIEW_FOR_FURTHER_P0
RESULT: exact TV=erf(d/(2sqrt2 sigma)); to mask d=2^-40 with advantage≤2^-128 sigma must be ~2^86.674 in output units; fixed sigma=2^-20 gives advantage~2^-21.326. Existing DPHE/rand-BFV already addresses different source threat models.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Stop naive output-noise privacy variants; independent source-complete new Pure-FHE key/dataflow scheme, or source-based full 2025/395 theorem comparison if continuing approx FHE privacy. No Codex without PI approval.
STATE_UPDATE: YES this isolated finding only.
CODEX_REQUIRED: NO.