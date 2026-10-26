# PURE-FHE · P0-PRESCOUT-36 — Ternary SignBoot stationary points: exact minimum harmonic and Hermite prior-art gate

DATE: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-35, findings/pure-fhe-p0-adaptive-heterogeneous-gadget-schedule-union-certificate-gate-2026-10-27.md, blob d9e7463fc1b784fff3fc00329467f72341b6a402.
STATUS: FAIL_SINGLE_HARMONIC_TERNARY_CLEANING / PASS_MINIMAL_TWO_HARMONIC_HERMITE / FAIL_NOVELTY_DIRECT_PRIOR_ART
NOVELTY: NOT_ESTABLISHED. Original trigonometric Hermite already contains exactly the derived construction.
CODEX_REQUIRED: NO (no native FHE, GPU, remote or infrastructure experiment).
STATE_UPDATE: YES — this isolated PURE-FHE findings file, global STATE.md and all unrelated research tracks unchanged.

## New independent, one falsifiable hypothesis H36

Source: Hong et al., *A White-Box Bootstrapping Approach for High Precision Comparison Over Homomorphic Encryption*, ePrint 2026/418, **full archived 24-page PDF** via GitHub Notes, SHA256 6c277829b8913ee2f4d2a038927a8bc95afe015f7f2e91afd2b8545e2116ef50, VERSION_UNVERIFIED. Physical §3.1–3.2 pp11–13, Alg2 p12, Theorem1 p12 and §5 pp17–18 directly read. Author's sign-bootstrapping maps binary sign plaintext z∈{−1,+1} to ±1/4+integer before EvalSign=sin(2π x), so sin's extrema perform quadratic cleaning while periodicity eliminates ModRaise lift. This is a NEW SOURCE analyzed on P0-36; do not present it as a new construction from this research assistant.

H36: Can the SAME single-harmonic periodic EvalSign-type function, allowing arbitrary real affine combination a+b cos(2πx)+c sin(2πx), be reused for three distinct stable symbols z∈{−1,0,+1} mapped to x=z/3 (mod 1), with exact outputs and vanishing derivative at all three message nodes? A YES would permit an almost free ternary SignBoot without extra function/harmonic evaluation.

Cheapest decisive test: solve the three derivative constraints at x=0,1/3,2/3 in exact trigonometric algebra. If single harmonic fails, exhibit the minimal two-harmonic Hermite solution and FIRST check original full CRYPTO 2025 trigonometric Hermite prior art before treating it as a paper idea. No implementation.

## [DERIVATION] Single-harmonic impossibility in the declared family

Let R(x)=a+b cos(2πx)+c sin(2πx). R'(x)=2π[−b sin(2πx)+c cos(2πx)]. R'(0)=0 forces c=0. R'(1/3)=0 then forces b=0 since sin(2π/3)=sqrt3/2≠0. Consequently R is constant and cannot satisfy R(0)=0, R(1/3)=+1, R(2/3)=−1. This is an exact first-harmonic (Fourier degree≤1) no-go, not a lower bound on all FBT, different encodings, plaintext-modulus scaling, or nonlinear CKKS circuits. Two harmonic terms are necessary within THIS standard period-one trigonometric representation.

## [DERIVATION + TOY_EXECUTED] Minimal exact two-harmonic solution

R3(x) = [2/(3sqrt3)](2 sin(2πx) − sin(4πx)).

Exact symbolic SymPy verifies:
 x=0: value 0, R3'=0, R3''=0, R3'''=32sqrt3 π^3/3.
 x=1/3: value +1, R3'=0, R3''=−8π².
 x=2/3: value −1, R3'=0, R3''=+8π².
Since R3 is period one, R3(z/3+I)=z exactly for all integers I and z∈{−1,0,1}.
At useful exact message nodes for small continuous perturbation u:
 R3(u) = (16 π³/(3sqrt3))u³ + O(u^5)
 R3(1/3+u) = 1−4π²u²+O(u³)
 R3(2/3+u) = −1+4π²u²+O(u³).
Thus mathematical nonlinear postprocessing has quadratic local error suppression at ±1, cubic at 0, absent other errors. It is NOT an end-to-end FHE error guarantee: Eq polynomial approximations, PS coefficient precision, LWE/RLWE scale, StC/CtS, key switching, ModRaise lift, rescale and DFR are all untested.
Crucial cost: two sine harmonics can demand more trigonometric evaluation than original one-harmonic sign (e.g. sin4πx from doubling also involves cosine or an equivalent complex exponential); no latency/modulus claims follow from harmonic count.

## [FACT] Exact first-party prior art supersedes originality

Andreea Alexandru, Andrey Kim, Yuriy Polyakov, *General Functional Bootstrapping using CKKS*, ePrint 2024/1623, CRYPTO 2025, **full archived 52-page PDF** via GitHub Notes SHA256 72f3ce0a332d79b5c5a58f6dc9117b3de20aed8aab73b119c69f700a58f8c629, VERSION_UNVERIFIED. Original physical §3.1 pp15–16 and Theorem1 p16 were reread. They explicitly consider arbitrary discrete maps f: Z_p→Z_p at x=j/p, impose R(j/p)=f(j) and R'(j/p)=0 for quadratic noise cleaning, and derive a UNIQUE periodic trigonometric polynomial using harmonics 1..p−1:
 a0 = (1/p) Σ_l f(l)
 ak = [2(p−k)/p²] Σ_l f(l)cos(2πkl/p)
 bk = [2(p−k)/p²] Σ_l f(l)sin(2πkl/p), for k=1..p−1.
Set p=3, (f(0), f(1), f(2))=(0,+1,−1). Direct exact evaluation of those AUTHOR formulas gives a0=0, a1=a2=0, b1=4sqrt3/9, b2=−2sqrt3/9. Substitution yields R(x)=2/(3sqrt3)(2sin2πx−sin4πx) EXACTLY. Thus proposed multi-valued SignBoot is a literal p=3 case of established CRYPTO 2025 FBT. Zero claim of novelty is justified, not merely similar prior art.
Additionally Polyakov's first-party publication list (https://ypolyakov.gitlab.io/publications.html) names Alexandru–Kim–Polyakov–Zheng *Sparse Hermite Interpolation Method for Discrete-CKKS Functional Bootstrapping* as ASIACRYPT 2026, ePrint 2026/1026. Full PDF was RETRIEVAL_BLOCKED (ePrint403/no exact arXiv/GitHub mirror) and only title/venue can be asserted; its technical algorithms or performance NOT independently examined. This additional near-field prior art greatly heightens any 'sparse p=3' originality burden.

Other web source: https://eprint.iacr.org/2024/1623, https://eprint.iacr.org/2026/418. Full originals were analyzed through the cached reader, not via webpage snippet alone.

## Result and decision
The primary low-cost *single-harmonic ternary* extension H36 FAILS strictly. A two-harmonic construction PASSES mathematical interpolation/noise stationarity, but its closed form is exactly CRYPTO 2025 Theorem1 p=3, so independent contribution novelty FAILS. Neither general Hermite interpolation, noise-cleaning of ternary symbols, nor ordinary harmonic sparsification is a new technique. No native code/extra rescale/parameter analysis warranted before isolating a genuinely distinct transform/noise/security mechanism.
PARK/KILL this specific idea as a publication candidate. Repeated isolated tweaks (p=4, higher Hermite derivative, slight polynomial approximation) are close prior art and should not be spun into more P0 iterations. For a new paper idea, first find a first-party complete source with an unmet and *material* encryption/key/noise complexity bottleneck not already captured by CRYPTO 2025/ASIACRYPT 2026 FBT, TFHE, GCKKS or ALU papers. If the team chooses to explore hardware acceleration, that is separate engineering track and needs PI authorization.

END_OF_ITERATION
STATUS: FAIL_FIRST_HARMONIC_FOR_TERNARY / PASS_HERMITE_TWO_HARMONICS / FAIL_CONTRIBUTION_NOVELTY
RESULT: exact min Fourier degree 2 and stationary 3-level LUT; source CRYPTO 2025 Theorem1 precisely outputs identical formula, no original crypto idea.
NOVELTY: NOT_ESTABLISHED; directly existing mechanism.
NEXT_TEST: source-first different PURE-FHE structural bottleneck with clear novelty window, not another 3-point Hermite variant; PI can stop repetitive scouting and do portfolio-wide HUMAN_REVIEW if necessary.
STATE_UPDATE: YES isolated finding only; global STATE.md and other lines unchanged.
CODEX_REQUIRED: NO, all native work PENDING explicit PI authorization.