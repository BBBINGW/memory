# BOOT B056 — Carousel valid-LWE functional LUT error after float64 modulus switch; exact integer repair and full-cost gate

TRACK_ID: BOOT
ITERATION: B056
DATE: 2026-10-20
STATUS: PASS_VALID_ZERO_NOISE_FUNCTIONAL_WITNESS / PASS_INTEGER_CORRECTION / PASS_SCALAR_MICROBENCH / UNCLEAR_ACTUAL_DFR / LOW_CRYPTO_NOVELTY
STATE_UPDATE YES
TRACK BOOT ONLY. SHIP paused by PI after I407. B055 was latest existing GitHub Notes: findings/boot-B055-carousel-valid-lwe-modswitch-phase-exact-repair.md SHA 6eaba8d8e8f391ab3889fac7b9384745cd5b6b6a. GitHub Notes read_repo_file returned {} despite list filenames/sha, so detailed B055 content was corroborated from prior locally mounted /mnt/data/boot_B055_carousel_phase.go and Library. No earlier file overwritten.

## One primary falsifiable hypothesis
B054/55 found source FP64 torus-to-2048 integer index differs from exact in narrow threshold neighborhoods and a VALID noiseless LWE phase example old 2047 vs exact 0. Do those discrepancies EVER change the FINAL FUNCTION lookup under author centered Carousel LUT, or are they categorically masked by the half-bin message margin? A single source-matched functional p16 witness is the cheapest test. Repair exact public integer modular switching and compare pure-kernel cost, actual DFR caveats and prior art.

## Original source verification
Author/public Git repo https://github.com/SNUCP/carousel, main tree SHA 21d5800462920d63afcc58873446455642588297; README says repo under construction. 
carousel/bootstrap.go blob 53111c68a004cfb36c5f6f368e38a2ccffd6cfae: lines35–37 computes int(math.Round(modSwitchConstant*float64(x))) % lookUpTableSize for x uint64; consumes ModSwitch of body and masks during blind rotation.
carousel/evaluator.go blob 35d4e49ece75a59aee46843aea4b8084d5366456 line126 modSwitchConstant=polyExtendFactor/2^(64−logPolyDegree); with published N2048 it is exactly2^-53.
carousel/params.go blob 05fbbc8edf0a08e52e28d06ad5ecfa3cb1a0513b validates power2 degree and LUTsize=PolyDegree=2048.
carousel/params_list.go blob 8fd34601da8fd5d0109790800ee55c58b759ba73: p4,n687; p8,n788; p16,n828; coeffs/slots versions each.
carousel/bootstrap_lut.go blob 71acac44c868cc15d408edebad8b35d0c9dae037 lines115–130 fills identity f(x)=x intervals of width T/p and rotates whole table LEFT by T/(2p); math/vec/vec.go explicitly identifies negative rotate as left; math/num/num.go DivRound uses round. Thus exact source identity LUT mapping F_p(z)=floor((((z+T/(2p)) mod T))/(T/p)).
carousel/carousel_test.go blob 77653a439b5251ca830ad1807537727355182886 contains original bootstrap functional tests; none compiled/executed from original Carousel repo B056. ePrint https://eprint.iacr.org/2024/2032 title/version may differ from cached source, so rely source code for claims.

## Conditional source-matched guard
For p|2048 and p∈{4,8,16}, canonical message center m*T/p, width W=T/p, half-margin h=W/2. A signed phase perturbation d never changes LUT lookup for source-centered message if the exact phase lies at least |d| index units away from the nearest class boundary, with careful ties handled by direct F_p formula. Test every canonical p4/p8/p16 center ±1: (4+8+16)*3=84 PASS, margin p4 256,p8 128,p16 64. In B055 zero-error phase old2047 and exact0, the two indexes map SAME message0 for all 3 source p. Thus one index error does NOT by itself imply a functional mistake or real DFR degradation.

## NEW decisive valid noiseless LWE witness: full identity LUT changes
Use source p16, T2048, Q=2^64, H=2^52, binary secret s=(1 repeated130,0 for rest), embeddable in published n828. Set first public mask:
 a_bad=(2*1024+1)*H−1=9227875636482146303
and subsequent 129 publicly known mask coefficients
 a_good=H+1=4503599627370497,
others a_i=0. Set LWE body b=(a_bad+129*a_good) modQ=9808839988412940416. Then b−〈a,s〉=0 modQ, i.e. a valid zero-error LWE encryption of message0 in the algebraic plaintext definition. Source FP64 ModSwitch causes ONLY the a_bad scalar index to round the wrong direction (it was just 1 below a half threshold), while its exact bits.Mul64 result rounds down. The source-equivalent full phase (body minus masks) yields:
 floating phase 1983 (= -65 mod2048);
 exact phase 1984 (= -64 mod2048).
From the exact source identity LUT p16 (width128, offset64), F_16(1983)=15 (WRONG), F_16(1984)=0 (CORRECT). Thus an erroneous scalar rounding can reach the actual FUNCTION LOOKUP even for a syntactically valid zero-input-error LWE, despite B055 example being invisible at the functional level. The witness deliberately exhausts the modulus-switch noise margin; it does NOT show meaningful failure probability under honest randomly generated a and noise, nor that the published paper's sufficient DFR assumptions hold for this adversarially chosen mask vector.
Standalone native Go source-equivalent reproducer created /mnt/data/boot_B056_carousel_lut_phase.go, SHA256 84fd2841affe1fbf97801b487c6110175ee06865a02c2aeaa0973974ecad19f6. Executed go run and all assertions PASS for 84 center-neighbor probes and witness. Source fill intervals, left-offset, and nearest modulus-switch source formula copied conceptually from original, but no full RLWE/FFT/key-switch/evaluation was executed.

## Scalar mismatch probability and exact arithmetic
For T2048, old float64 mistakes occur on unsigned inputs just LEFT of half-step thresholds (2j+1)*2^52 because float64 rounds an integer up to the exact half-step. Count all affected x by predecessor float64 ULP/2 over j0..2047: EXACT 1,398,101 of 2^64 torus values, probability for single UNIFORM uint64 x = 7.579120707770781e-14.
If n+1 modulus-switched ciphertext coordinates EACH have uniform marginals, union bound any index mismatch <=(n+1)*prob, without requiring independence: n687 <=5.2144350469462974e-11, n788 <=5.979926238431146e-11, n828 <=6.283091066741978e-11. THESE ARE NOT DFR: key-switched input marginals, cancellation in LWE phase, LUT margin and downstream noises are not included. Do not claim this is a security vulnerability probability or actual decryption failure.
Exact power2 torus nearest switch: q=x>>53; if x &((1<<53)-1) >=1<<52 then q++; return q &2047. General source-size T: hi,lo=bits.Mul64(x,T), if lo>=1<<63 then hi++, return hi%T, with appropriate T bounds. B055 previously cross-checked general method versus math/big, not a B056 new theorem.

## Measured native Go arithmetic microbenchmark [BENCH]
Using existing exact local Go bench source /mnt/data/boot_B055_bench/modswitch_test.go, GO111MODULE=off go test -bench Benchmark(Float|Shift|Mul64)$ -benchtime=100ms -count=3, Linux amd64 AMD EPYC 9V74:
 old float64: 10.30,10.98,10.49 ns/op
 exact power2 shift: 1.049,1.091,1.041 ns/op
 exact bits.Mul64: 1.173,1.178,1.046 ns/op.
This is a pure scalar microbenchmark of already available implementations, roughly9–10× faster SCALAR modulus switch; no actual full Carousel PBS latency benefit can be inferred (PBS dominated by costly homomorphic products/FFT). No source repo patch or upstream PR made. No evaluation-key changes.

## Correctness/security/noise/novelty gates
PASS: source-local exact arithmetic and legal LWE algebraic functional output counterexample. FIX: integer exact modulus switch, no secret-dependent data, no evaluation-key changes, likely preserves or improves source implementation arithmetic correctness.
FAIL: automatic implication one-index error => decoded output mistake (guard explains invisible B055 witness).
UNCLEAR: actual key-switch output input distribution, Gaussian LWE noise with published p4/8/16, real security-matched DFR, full runnable source integration, wall-clock speedup.
NOVELTY: nearest integer modulus switching with bit shifts and bits.Mul64 is textbook TFHE engineering and already present in other public TFHE libraries (e.g. TFHE-go). This is a concrete author-code correctness regression and potential upstream bug fix, NOT a publishable new FHE Bootstrapping scheme or algorithm.
DECISION: B054–B056 Carousel float64 source bug branch now audited to functional output and micro-cost gate. Archive it; do not spend more numbered rounds squeezing trivial casting instructions. If user separately requests upstream patch, implement full original-source test using exact source's key structures and submit only with authorization.

## End of iteration
STATUS PASS_VALID_LUT_WRONG_RESULT_WITNESS/PASS_EXACT_PATCH_ALGEBRA/PASS_KERNEL_BENCH/LOW_STANDALONE_NOVELTY; STATE_UPDATE YES.
NEXT_TEST B057: Continue PI's BOOT-only problem-first FHE bootstrapping research on DIFFERENT source/paper core algorithm/dataflow/noise bottleneck with strongest plausible nontrivial publication contribution. One falsifiable technical hypothesis and cheapest decisive correctness/security/performance/prior-art gate. Avoid repeating common precision fixes, CMS knapsack, BSGS, key-row dedup and PaCo multi-C transformations. SHIP remains paused. B057 NOT STARTED.
