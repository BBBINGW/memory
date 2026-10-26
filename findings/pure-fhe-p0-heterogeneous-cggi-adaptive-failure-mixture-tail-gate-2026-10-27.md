# PURE-FHE · P0-PRESCOUT-34 — Adaptive heterogeneous RGSW schedules: Gaussian variance-mixture tail gate

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-33, findings/pure-fhe-p0-arbitrary-modulus-a2d-lambda-integer-gauge-obstruction-2026-10-26.md, commit a3b0db214050e258946b6a9e77aeac61059a4679.
STATUS: FAIL_UNCONDITIONAL_MEAN_VARIANCE_FAILURE_CERTIFICATE / PASS_EXPLICIT_GAUSSIAN_MIXTURE_COUNTEREXAMPLE / NOVELTY_NOT_ESTABLISHED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO. No GPU, remote, native FHE, infrastructure changes or model downloads.
STATE_UPDATE: YES isolated PURE-FHE finding only, global STATE.md and unrelated historical tracks untouched.

## Single smallest H34 (one test)
Under the paper's gray-area server-controlled heterogeneous gadget decomposition and its publicly observed modulus-switch quality statistic Z*, can an unconditional **single Gaussian** using the *average* noise variance or an empirical E[Z*] ±10sigma range automatically certify an entire adaptive service's extreme (e.g. 2^-128) decryption failure probability, without conditioning on the quality event or budgeting its tail?
Cheapest decisive test: assume the conditional errors really are perfect centered Gaussians. Give two public quality buckets with different conditional variances but the SAME overall mean variance as the single-Gaussian comparator. Compare exact erfc tail probabilities at one prescribed decryption threshold; this removes ALL complications about non-Gaussian FHE noise and isolates invalid averaging. Then check source's actual modest claim and current rare-event FHE prior art before originality judgment.

## [FACT] Primary sources, carefully scoped
Hong and Lee, *Optimizing FHEW-Like Homomorphic Encryption Schemes with Smooth Performance–Failure Trade-Offs*, ePrint 2025/1892 original archived github-mirror 26 pages, SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, VERSION_UNVERIFIED, via GitHub Notes get_eprint_paper and read_eprint_pages, original physical §2.4 p10–11, §3.1 Theorem3.1 p12, §3.2 pp12–14, §5 pp18–19.
- §3.1 Theorem3.1 already introduces heterogeneous gadget bases for CGGI blind-rotation keys, and §3.2 approximate gadget decomposition. Repackaging it for TFHE is not new.
- §5.1 considers fixed N independent publicly evaluated modulus-switch quality samples Z^(1)...Z^(N), chooses Z*=min_i Z^(i), estimates its first two moments empirically. The quality statistic is a public-data proxy for a secret-dependent switching error, not a deterministic upper bound on the realized error for every secret.
- §5.2 proposes gray-area **duplicated** brk with fast/slow decomposition for server runtime/performance-failure tradeoff without receiver interaction. States that observed switching noise level can guide selection. Source Table4 p19 marks its failure probability *range* an **approximation** using E[Z*]±10 standard deviations as best/worst scenarios; NOT a proved tail event or all-input DFR theorem. Table4 estimates e.g. 2^-130 to 2^-126 with 10 trials using the author's specific approximation. Do NOT allege original paper promised formal 2^-128 dynamic reliability or has a validated security error.
- §2.4 p11 reports Gaussian-erf FP expression for source noise variance. It does not give an exact finite-sample secret-conditional distribution in this table.
Ballandras, Orfila, Tap *Concrete Estimation of Correctness and IND-CPA-D Security for FHE via Rare Event Simulation*, ePrint 2026/610, original archived github-mirror PDF 45 pages, SHA256 a202bddc7abefa96aa2cd931eb071552a5d2605e70eaaf89322a48d3b1ba3ee5, VERSION_UNVERIFIED, acquired & read pp1–4,13–15,36–38. Original explicitly provides rare-event importance-splitting verification of FHE failure probabilities as low as 2^-128, refined Irwin–Hall noise model, Gaussian approximation analysis, and drift mitigation with **public ciphertext quality test** including original noise, plus extension to multi-bit. Hence neither 'correct the Gaussian tail' nor 'quality-based modulus-switch choice' is a novel general primitive. A construction covering heterogeneous per-key schedules jointly with conditional rare-event certificate is NOT directly verified in these pages; absence of an identified matching theorem is NOT evidence of novelty.
Public metadata: https://eprint.iacr.org/2025/1892 and https://eprint.iacr.org/2026/610 ; relevant poster/source https://www.zama.org/post/zama-at-fhe-org-2026-eight-contributions-from-taipei.

## [DERIVATION] Exact mixture law
Let W be any publicly observable quality bucket that selects an available gadget schedule. Suppose E|W=w is exactly N(0,V_w), and let T>0 be a threshold. Then without independence across multiple executions, for one execution law of total probability gives:
  Pr(|E|>=T) = sum_w Pr(W=w) erfc(T/sqrt(2 V_w)).
The heuristic shortcut:
  erfc(T/sqrt(2 E[V_W]))
is **in general not equal** and is not a one-sided bound; Jensen's inequality cannot be applied globally without checking the curvature at the actual threshold and variance range.

## [TOY_EXECUTED] Decisive Gaussian example — no FHE parameter claim
Let W∈{0,1} with both probabilities 1/2, V_0=1, V_1=9, and T=12. Both CONDITIONAL laws are perfect Gaussians. Average variance E[V]=5, so one unconditional N(0,5) surrogate has:
  p_avg = erfc(12/sqrt(10)) = 8.02511126692759e-8.
Actual mixture:
  p_mix = 0.5 erfc(12/sqrt(2)) + 0.5 erfc(12/sqrt(18))
        = 3.1671241833119884e-5.
Ratio p_mix/p_avg = 394.6517472429414, meaning an average-variance certificate *understates risk by ~395x* even though the conditional Gaussian assumption is exact.
For T=6 the same mixture has p_mix=0.02275013293477 vs p_avg=0.00729035809154 (3.12x). Hence this is not solely an extreme floating-point issue.
This mathematical example is NOT a counterexample to Theorem3.1 of Hong and Lee: they aggregate variance for a **fixed chosen gadget vector**, and p19 dynamic table already distinguishes high/low quality scenarios. This test rejects a tempting naive extension to adaptively varying schedules, not an author-guaranteed theorem.

## [DERIVATION] The '10 sigma' statistical reach vs 128-bit cryptographic requirement
Even IF the quality statistic Z* were an exact Gaussian (unverified and not assumed true), a two-sided interval mean±10 std would leave probability
  P(|Z*−mu|>10sigma) = erfc(10/sqrt(2)) = 1.5239706048321186e-23 ≈ 2^(-75.7965).
This exceeds 2^-128 by roughly 2^52.2. A Gaussian 2^-128 two-sided quantile is ~13.1086 sigma, not 10sigma. In source Table4 the ±10σ envelope is explicitly an **approximation**, not a cryptographic guarantee. Without proving how conditional failure behaves in the uncovered tails, no general 2^-128 DFR certificate follows. For non-Gaussian Z*, even the numerical 10σ probability cannot be asserted; an explicit distribution/rare-event certificate is needed.
Safe general proof contract: choose disjoint public-quality buckets G_i with certified occurrence probabilities p_i, and schedule S_i with a **valid conditional** error-tail bound δ_i in that bucket, plus a residual bad event B with probability β, then
  Pr(failure) <= Σ_i p_i δ_i + β.
Alternatively per-bucket worst-case uniform δ_max plus β yields δ_max+β. These are standard total-probability/union calculations, not cryptographic novelty. Reuse of a fixed secret and adversarially adaptive ciphertexts may invalidate naive independence assumptions on quality and secret and needs a separate security model/conditioning proof. No IND-CPAD claim from a one-query average law.

## Candidate research value, prior-art kill gate
A fully usable conditional-risk-certified scheduler would jointly choose which duplicated gadget base to use given public quality, track key-storage union, expected latency, and tail guarantee under a fixed-key multi-query model. This is a *speculative integration*: the functional ingredients are strongly preexisting in 2025/1892 heterogeneous base and quality-based gray area, Bernard drift mitigation, and 2026/610 importance splitting and theoretical tail certification. We have NOT constructed any complete new privacy/security mechanism, actual risk estimator, or matched security/noise/key/runtime ledger. Especially no proof of conditional independence when the same secret is reused and ciphertexts are adversarially chosen; this is the main next obstacle if pursuing this exact line.
The important present contribution is only a statistical correctness-of-certification gate. A statement 'DFR can be tuned precisely' must be interpreted with its probability space, schedule randomness, failure tails, and whether the source reports a model-based estimate or a cryptographic guarantee. No attack on authors demonstrated.
Given many failed adjacent P0 scouts and close prior-art, **PARK** as a theoretical risk-contract question unless a precise new mechanism beyond 1892+610 survives original theorem comparison. Do not start Codex to estimate 2^-128 tails by simple Monte Carlo.

END_OF_ITERATION
STATUS: FAIL_H34_AVERAGE_VARIANCE_CERTIFICATE / PASS_GAUSSIAN_MIXTURE_FALSIFIER / PRIOR_ART_HIGH
RESULT: exact conditional-mixture tail formula, numerical 395x underestimate at T=12 (toy), ±10σ Gaussian exclusion ~2^-75.8—not automatically a 2^-128 certificate; 2026/610 already addresses rare-event estimates.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: Before any new gadget scheduler theory, identify a concrete part of 2025/1892 dynamic schedule contract that 2026/610's conditional noise/rare-event methods do NOT already handle, with a complete error/secret-adaptivity/cost mechanism; else KILL and prioritize a source-backed independent PURE-FHE construction. User PI decides major topic.
STATE_UPDATE: YES only this isolated file. No root STATE.md edits.
CODEX_REQUIRED: NO.