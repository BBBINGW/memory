# BOOT-B054 archive — Carousel float64 ModSwitch differs from exact torus nearest rounding

TRACK_ID: BOOT
ITERATION: B054
DATE: 2026-10-20
STATUS: FAIL_FLOAT64_EXACTNESS / PASS_INTEGER_REPAIR / UNCLEAR_END_TO_END_DFR
STATE_UPDATE YES
SHIP PAUSED_BY_PI, untouched.

Source Hwang–Min–Song Carousel ePrint2024/2032; source github.com/SNUCP/carousel code bootstrap.go blob53111c68a004cfb36c5f6f368e38a2ccffd6cfae lines36–38 uses int(math.Round(modSwitchConstant*float64(x))) %2048 for uint64 x. evaluator.go blob35d4e49ece75a59aee46843aea4b8084d5366456 line126 sets modSwitchConstant=2^-53. Stock params_list.go blob8fd34601da8fd5d0109790800ee55c58b759ba73 poly degree2048, LWEDim687/788.

False identity: float64 conversion rounds away >53bit low information before desired nearest bin rounding. For exact integer x=(2049)*2^52−1=9227875636482146303, author output index1025, exact mathematical nearest modular switch index1024. For j-th threshold t_j=(2j+1)*2^52, all x in [t_j−2^r,t_j−1] erroneously rounded UP when j in [2^r,2^(r+1)−1], r0..10. Total precisely sum4^r=(4^11−1)/3=1,398,101 uint64 values (P_uniform=7.5791207e−14), confirmed source-identical Go code with exhaustive 8,603,648 near-boundary test input validations. Reproducer /mnt/data/boot_b054_carousel_modswitch.go SHA256 d4773014c68197f145e60f00a47b9f4c2ace58a520a990d40cc2ef418db2c927.

Repair: exact nearest half-up q2^64 to N2048 with quotient=(x>>53); rem=x&((1<<53)−1); if rem>=(1<<52) quotient++; return quotient&2047. No new eval key or secret dependence. Generalize only for target N powers of2. May need a source native integration test to ensure default parameters and all call paths. Not yet patched original repository.

DECISIVE LIMITATION: A wrong LUT rotation index does NOT automatically mean wrong decoded plaintext. Carousel LUT repeats same value over contiguous bucket, so a one-position automorphism shift can be harmless except near an encoded-message boundary; real key-switch and accumulation may not be iid uniform. Probability P(ANY INDEX difference) for 687 iid uniform masks ≈5.20685593e−11 IS NOT real output DFR nor proof source security bound broken. Need paired native end-to-end targeted boundary test first. Standard exact integer torus modulus switching is known implementation arithmetic, not a new cryptographic algorithm or paper-ready innovation. Keep precise result, do not claim new scheme.

FINDING findings/boot-B054-carousel-float64-modswitch-threshold-integer-repair.md

NEXT B055: one minimal target-mask original Carousel native integration test; determine whether final decoded message differs, compare correct integer fix and baseline under same keys. If only simple bug, archive Carousel and audit a genuinely new bootstrapping computation bottleneck. SHIP paused, BOOT only. B055 NOT STARTED.