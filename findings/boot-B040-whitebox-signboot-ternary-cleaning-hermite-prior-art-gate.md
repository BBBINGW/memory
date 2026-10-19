# BOOT B040 — White-box SignBoot ternary extension: exact harmonic-degree gate and prior-art falsification

TRACK_ID: BOOT
ITERATION: B040
DATE: 2026-10-20
STATUS: PASS_TERNARY_CLEANING_CONSTRUCTION / FAIL_UNMODIFIED_SINE_QUADRATIC_CLEANING_AT_ZERO / FAIL_CRYPTOGRAPHIC_NOVELTY_VS_TRIG_HERMITE / UNCLEAR_NATIVE_DEPTH_DFR_AND_END_TO_END_SPEED
STATE_UPDATE: YES. BOOT-only. SHIP PAUSED_BY_PI after I407, no SHIP actions.

## Restoration and precise scope
The latest BOOT state through GitHub Notes listing at start of this turn confirmed B039 files already committed:
 findings/boot-B039-fefbs-affine-odd-fourier-symmetry-source-cost-gate.md, SHA 925b706fbd7aae94a7eb79efc77ad45cbab50908;
 failures/boot-B039-fefbs-affine-parity-no-native-gain.md, SHA c83c1e4baaa503ce3abdb76039667fd789db26dd;
 boot-STATE.md SHA f544165342ad13367f6aa2b09f007b1ae5c33d5a, so this iteration correctly starts B040, not B039. GitHub Notes read_repo_file returned {} despite list_repo_files revealing existing paths, and no speculative restoration of its unreturned contents was made.
Research remains ONLY FHE BOOTSTRAPPING algorithmic ideas; no ZK soundness/witness project, no cross-track SHIP research.

## Primary minimal falsifiable hypothesis
Paper Hong–Lee–Kim–Lee "A White-Box Bootstrapping Approach for High Precision Comparison Over Homomorphic Encryption" ePrint2026/418 describes sign bootstrapping (SignBoot) for signed BIT messages z∈{-1,+1}, replacing EvalMod by EvalSign(x)=sin(2πx). Claim to test: "The same period-one EvalSign can clean ternary z∈{-1,0,1} to quadratic or better message error using no extra nonlinear homomorphic operation; if not, can a minimal low-harmonic periodic replacement give a cheap new ternary SignBoot construction that is independent of known multi-valued functional bootstrap methods?"
Cheapest falsifier: derivative at zero, exact harmonic interpolation, source prior-art check (CRYPTO25 trigonometric Hermite). Numerical random input error calculation is only mathematical sanity, not proof of native crypto cost.

## Paper/source provenance and limitations [FACT]
Source full 24-physical-page version-unverified ePrint PDF 2026/418 title-matched, original metadata authors Deokhwa Hong, Heesoo Lee, Young-Sik Kim, Yongwoo Lee, SHA256 6c277829b8913ee2f4d2a038927a8bc95afe015f7f2e91afd2b8545e2116ef50, publicly retrieved via Research Notes IACR ePrint mirror. Physical pp11–13 §3.1–3.2 Algorithm2/Thm1/Cor1: for z∈{±1}, encode near x=(z+τ)/4+I, I integer; apply period1 EvalSign=sin(2πx), decryption phase after lift maps to z cos(πτ/2), error ≤(π²/8)τ². Paper p14+ discusses minimax sign polynomial composition and cleaning; p21 discusses future possible generalization to arbitrary step/multi-valued functions. NO original authors' released SignBoot code found/validated this iteration; no native FHE execution.
Crucial prior art: Alexandru–Kim–Polyakov "General Functional Bootstrapping using CKKS" ePrint 2024/1623 (CRYPTO 2025), original full 52pp ePrint PDF SHA256 72f3ce0a332d79b5c5a58f6dc9117b3de20aed8aab73b119c69f700a58f8c629, version unverified; §§3.1–3.3 and appendices construct arbitrary-valued first-, second-, THIRD-order TRIGONOMETRIC HERMITE INTERPOLATION with zero first/second/third derivatives at discrete message nodes and analyze cleaning of errors. Public OpenFHE doc https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_FUNCTIONAL_BOOTSTRAPING.md explicitly offers GetHermiteTrigCoefficients and first/second/third orders with security/IND-CPA-D caveats. These precede 2026/418 and subsume simple multi-value stationary point construction. This is decisive novelty failure, not evidence original SignBoot is flawed.
Other related source https://ckks.org/blog/2025/high_prec_bootstrap/ describes integer/digit cleaning including ternary trits; also prior art for nonlinear digit cleaning.

## Exact mathematics [DERIVATION]
Let θ=2πx, and x=(z+τ)/4+I, z∈{-1,0,1}, I∈Z. Periodicity eliminates integer I. Source plain sine:
 z=±1: sin(π(z+τ)/2)=z cos(πτ/2), |error|=1−cos(πτ/2)≤π²τ²/8 for |τ|≤1.
 z=0: sin(πτ/2)=(π/2)τ+O(τ³), so relative perturbation is FIRST order, not second. F'(0)=2π ≠0, completely falsifying unchanged sine's claimed ternary quadratic cleaning.
For the period1 Fourier sine series with harmonics k≤3, impose correct values F(0)=0,F(±1/4)=±1 and F'(0)=F'(±1/4)=0. Symmetrize any real-valued candidate to odd part without changing these symmetric constraints, so suppose F(x)=a sin(2πx)+b sin(4πx)+c sin(6πx). At x=1/4 value: a−c=1; derivative there: b=0; derivative at0: a+3c=0. Unique a=3/4, b=0,c=−1/4; no solution with k≤2. Hence minimal-harmonic candidate
  F3(x)=(3/4)sin(2πx)−(1/4)sin(6πx)=sin³(2πx).
On z0, |F3|=|sin(πτ/2)|³ ≤(π|τ|/2)³, i.e. CUBIC cleaning. On z±1, |F3−z|=1−cos³(πτ/2)≤3π²τ²/8; its leading quadratic error is THREE TIMES larger than the source original sine (for nonzero ±1 messages). Thus it is a true local tradeoff not monotone improvement, uses extra non-linear evaluation.
Higher-degree known cleaning option
  P5(u)=(5/2)u³−(3/2)u⁵, F5(x)=P5(sin(2πx)).
At u∈{-1,0,1}, P5(u)=u and P5'(u)=0. For z0, F5= (5/2)(πτ/2)³ +O(τ⁵) (third-order); for z±1, 1−P5(cos(πτ/2))=(15/8)(πτ/2)^4 +O(τ^6), so FOURTH-order at ±1. Requires at least THREE additional sequential ciphertext products u²,u³,u⁵ in a naive circuit (vs TWO for u³), introducing rescale/key-switch/new error; this is standard polynomial Hermite cleaning, already prior art.
Additionally error of approximate exp/sine itself can be magnified by cleaning: sup|P3'(u)|=3 on |u|≤1, sup|P5'(u)|=15/8; cannot set postprocessing error equal to original approximation error. For noise/security, need total e_sign approximation+new arithmetic noise, message margin, actual bootstrap Galois/KS errors and IND-CPA-D; absent.
If plaintext includes z±2 then sin(πz/2)=0, same as zero -> alias; proposed ternary restriction is essential, no global integer-step function claim.

## Reproducible sanity testing [VERIFIED]
Sympy symbolic expansion/derivatives:
 F3(u)=u³; P5(u)=(5u³−3u⁵)/2; polynomial node values ±1,0 preserved.
 F3(sin a)=a³+O(a⁵) near zero, 1−F3(cos a)=3a²/2+O(a^4) at ±1;
 F5(sin a)=5a³/2+O(a⁵), 1−F5(cos a)=15a⁴/8+O(a^6).
For |τ|=.1:
 Original sine at z0 absolute error 0.1564344650, at z±1 0.0123116594.
 Cubic F3 at z0 error0.003828223845, at z±1 0.03648211351.
 Quintic F5 at z0 error0.009430034655, at z±1 0.001113672024.
Independent fixed-seed Python NumPy RNG20261020: 20,000 uniform |τ|≤0.1, uniform z∈{-1,0,1}, random I integers from -10..10, numerical exact periodic evaluation:
 original total max abs error.1564264, z0 max .1564264, nonzero max .0123092;
 F3 total max .0364749, z0 max .00382763, nonzero max .0364749;
 F5 total max .00942859, z0 max .00942859, nonzero max .00111323.
No native RLWE/CKKS encryption and no validated 128-bit security. These numerical samples do NOT verify actual DFR or improved latency.

## Key gates, novelty and decision
CORRECTNESS ideal period1 ternary map: PASS with explicit restricted domain.
UNMODIFIED ORIGINAL SINE ternary noise cleaning: FAIL at z0 (first derivative).
MINIMAL TRIG FOURIER HARMONIC DEGREE for ternary first-order stationary property: at least 3, achieved by sin³, exact under odd symmetrization.
NO extra homomorphic multiplication: FAIL for this construction, F3 uses two extra multiplications, F5 three; no globally minimal FHE circuit lower bound claimed.
INHERIT original noisy EvalSign 2^-128 correctness/IND-CPA-D/level budget unchanged: FAIL/UNCLEAR; new perturbations and approximation errors matter.
CRYPTO NOVELTY: FAIL: trigonometric Hermite of arbitrary LUT and derivative flattening already in 2024/1623 (CRYPTO2025), as does ternary integer cleaning. This is NOT a new FHE primitive and not paper-ready.
Author code 2026/418 not available/verified; prior generic OpenFHE implementation published. Real full scheme runtime/modulus not compared.
RESULT: A simple new-to-this-track but established multi-valued Hermite step yields a correct ternary sign bootstrap model with local precision tradeoff, but there is NO independent publishable contribution, and the original white-box SignBoot is not defective on its stated ±1 domain.
NEXT_TEST B041: Switch BOOT source-first audit to a stronger *core dataflow/encoding* problem with full original paper and preferably author code. One candidate 2026 SIMD Arithmetic Logic Units with amortized O(1) bootstrapping per ciphertext (triangle encoding; compare REFHE/GBFV prior art) rather than further polishing elementary Hermite. Must identify ONE significant falsifiable structural assertion and source-bound whole algorithm cost, not just changing polynomial order. Do not restart SHIP or VFHE. B041 NOT STARTED.
