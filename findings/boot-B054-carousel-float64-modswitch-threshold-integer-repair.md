# BOOT-B054 — Carousel float64 modulus-switching threshold discrepancy and exact integer repair

TRACK_ID: BOOT
ITERATION: B054
DATE: 2026-10-20
STATUS: PASS_NATIVE_SOURCE_EQUIVALENT_MISMATCH_REPRODUCTION / PASS_EXACT_INTEGER_REPAIR / UNCLEAR_REAL_DECRYPTION_DFR / LOW_ALGORITHM_NOVELTY
STATE_UPDATE: YES
SHIP PAUSED_BY_PI after I407, no SHIP work.

## Source and recovery

Latest findings/ shows B053 already completed: findings/boot-B053-fefbs-sampled-precision-cinfinity-bump-gate.md SHA 36009822433469f0775d7f0df4561d3e44c1b25d. B054 is next. GitHub Notes read_repo_file latest STATE/B053 returned {} despite list SHAs; do not claim they were text-read. FHE bootstrapping-only source-first independent paper audit.

Paper Hwang–Min–Song, Carousel: Fully Homomorphic Encryption with Bootstrapping over Automorphism Group, ePrint 2024/2032, full 34pp cache PDF SHA256 5ddec99ebbe14b270b413e21ab4923abf0ed5dba8d0f1d053b3fde1c5a35d6c8 VERSION_UNVERIFIED. Author source https://github.com/SNUCP/carousel Git main tree SHA21d5800462920d63afcc58873446455642588297. bootstrap.go blob 53111c68a004cfb36c5f6f368e38a2ccffd6cfae lines35–38 uses ModSwitch(x uint64) = int(math.Round(e.modSwitchConstant*float64(x))) % lookUpTableSize, called on LWE body and masks in both Carousel blind rotation paths. evaluator.go blob35d4e49ece75a59aee46843aea4b8084d5366456 line126 modSwitchConstant=float64(polyExtendFactor) / 2^(64−logPolyDegree); params.go blob05fbbc8edf0a08e52e28d06ad5ecfa3cb1a0513b sets stock PolyDegree=2048, lookUpTableSize=PolyDegree, polyExtendFactor=1. params_list.go blob8fd34601da8fd5d0109790800ee55c58b759ba73 confirms real n=687 and n=788 example configurations, PolyDegree2048.

## One falsifiable hypothesis and analytic proof

Primary: does source float64 ModSwitch EXACTLY implement nearest-integer torus rescaling MS(x)=floor(2048*x/2^64+1/2) mod2048 for all uint64 x, and can an exact integer-only map fix any discrepancy without new FHE key/noise? Cheapest test: derive threshold neighborhood and test all 2048 boundaries using native Go with exact integer reference.

For N=2^11, shift=53, half=2^52, intended exact nearest round-half-up: MS_exact(x)=((x>>53) + ((x & (2^53−1))>=2^52 ? 1 : 0)) &2047. No uint64 overflow because highpart <=2047 and increment <=1. All inputs nonnegative, so Go math.Round ties away from zero agrees with half-up for exact conversion.

Decision thresholds t_j=(2j+1)*2^52 for j0..2047. Float64 has only 53 significand bits. For j in [2^r,2^(r+1)−1], r0..10, binary64 ulp(t_j)=2^(r+1), and t_j is even multiple of the spacing. IEEE ties-to-even turns each input x=t_j−d, 1<=d<=2^r, into exactly t_j, so math.Round then gives j+1 while exact MS gives j. At j0 ulp1 and there are zero mistaken integers. Outside this tiny threshold-left interval the source gives exactly correct integer index. Thus EXACT count wrong unsigned 64bit inputs = SUM r0..10 (2^r thresholds)*(2^r bad integers per threshold) = (4^11−1)/3 = 1,398,101 out of 2^64. Every discrepancy is an erroneous +1 LUT rotation index relative to specified nearest rounding.

Concrete source-compatible witness x=(2*1024+1)*2^52−1 = 9227875636482146303 gives float64 old result1025 but exact intended 1024. This is PUBLIC integer arithmetic divergence; not in itself a cryptographic break.

## Native reproducer

Standalone Go 1.23.2 program written and RUN to /mnt/data/boot_b054_carousel_modswitch.go SHA256 d4773014c68197f145e60f00a47b9f4c2ace58a520a990d40cc2ef418db2c927. It implements source old ModSwitch with coefficient exactly 2^-53 and repaired bit-operations. For EACH j0..2047 enumerate x in [t_j−2100,t_j+2100], total 8,603,648 actual native test inputs. Assert discrepancy iff x lies in exact mathematical bad interval (all 8,603,648 PASS). Native Go result: exact count 1,398,101, P_mismatch uniform uint64 =7.5791207077707812e−14 ≈2^−43.585. Under CONDITIONAL IID uniform masks, chance at least one wrong integer index for n687 ≈5.2068559261e−11, for n788 ≈5.9723471175e−11. These are INDEX DISCREPANCY probabilities, NOT actual decryption failure or DFR: LUT encodes repeated bins, off-by-one may not change decoded value. Real key-switch outputs and body/mask correlations need more analysis.

## Cost, correctness, security, and novelty gates

[CORRECTNESS] Exact shift/mask/compare/increment maps EVERY uint64 x to intended nearest integer for stock power2 size N2048, no key, no additional ciphertext operations. General power-of-two N=2^k can use shift=64−k and carry; non-power2 N requires a 128-bit exact product/quotient, not this specific shift formula. A branchless carry expression is constant-time with respect to public ciphertext coefficients anyway.

[DFR] Off-by-one from floating conversion can change public automorphism exponent, but because encoded LUT bins repeat and have a decision margin, cannot assert every such event causes failed bootstrapping. Full author keyswitch+blindrotate native paired test, plus conditional rarity/security assumptions, necessary before any true DFR claim. Subtlety: old operation may in rare cases choose the adjacent LUT entry, which is equal for most interior locations.

[SECURITY] Correction of public deterministic arithmetic uses no secret-dependent material and does not add keys; not a security proof or an INDCPA attack on authors. Source paper's expected noise bound for ideal nearest MS and code rare misround are different questions.

[RUNTIME] Bit operations cheap and avoid floating conversion/round, but no per-Bootstrap runtime benchmark recorded; no claimed measured speedup.

[NOVELTY] Strong verified implementation precision flaw with exact count and repair, but standard integer torus modulus switching is textbook and NOT a new publishable FHE bootstrapping primitive. Research objective is nontrivial full algorithm, so do not indefinitely polish this numeric code detail.

## End of Iteration

STATUS PASS_NATIVE_MISMATCH_REPRO / PASS_EXACT_INTEGER_REPAIR / UNCLEAR_REAL_DFR / LOW_PUBLICATION_NOVELTY.

RESULT: Found a verified discrepancy in source Go 64-bit torus modulus switch, a concrete counterexample and mathematically exact 1,398,101-input count. Correctness repair needs no key/format changes. It is NOT a paper-ready Bootstrapping improvement.

NEXT_TEST B055: ONE minimal paired original Carousel ciphertext computation with public masks targeted at exact bad thresholds and LUT chosen to make one-index difference observable; compare same underlying key/ciphertext before and after ModSwitch-only fix, and measure what changes in final output and whether real parameter DFR is affected. If negligible / routine numeric bug, archive branch and shift to another novel source-first BOOT algorithm bottleneck. B055 NOT STARTED. SHIP remains PAUSED_BY_PI.

STATE_UPDATE YES. BOOT-only files.