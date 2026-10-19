# BOOT B056 — Error in equating blind-rotation index mismatch with decryption DFR; valid functional boundary witness

TRACK_ID BOOT
ITERATION B056
DATE 2026-10-20
STATUS FAIL_EVERY_WRONG_INDEX_BREAKS_FUNCTION / PASS_VALID_LWE_FUNCTIONAL_MISMATCH / NO_NOVEL_BOOT_ALGORITHM
STATE_UPDATE YES. BOOT only, SHIP paused.

Source: https://github.com/SNUCP/carousel at main tree 21d5800462920d63afcc58873446455642588297. bootstrap.go blob53111c68a004cfb36c5f6f368e38a2ccffd6cfae uses float64 cast+math.Round on uint64 for T=2048. bootstrap_lut.go blob71acac44c868cc15d408edebad8b35d0c9dae037 fills bins width2048/p, rotates LEFT by half-bin: identity lookup F_p(z)=floor((((z+2048/(2p))%2048))/(2048/p)).
Earlier B055 valid noiseless LWE gave float phase2047 vs exact0, BUT source p=4/8/16 LUT maps both to same message0; an index mismatch alone does NOT imply real PBS DFR. All source default message centers ±1 remain same identity LUT output: 84/84 checks over p4,8,16, margins256,128,64 respectively.

Actual new zero-input-noise syntactically valid binary LWE counterexample for output-level impact with source p16: n_active130 ones, remainder secret 0, Q2^64, first a0=9227875636482146303 = (2*1024+1)*2^52-1, next129 a_i=4503599627370497=2^52+1, b=(a0+129*a_good) modQ=9808839988412940416. Exact original phase (b−〈a,s〉)modQ=0, plaintext message0. Source float64 modswitch yields blind-rotation exponent1983, correct integer bits.Mul64 yields1984. Identity LUT F16(1983)=15 (incorrect), F16(1984)=0 (correct). Source-matched native standalone Go reproducer /mnt/data/boot_B056_carousel_lut_phase.go SHA256 84fd2841affe1fbf97801b487c6110175ee06865a02c2aeaa0973974ecad19f6 PASS. No complete native encrypted Carousel evaluation performed. This witness EXHAUSTS LUT-boundary margin using engineered nonuniform public a; not an IND-CPA security attack, not evidence honest random DFR is high or within paper's sufficient noise gate.

Exact float64 scalar index mismatch count for uniform uint64: 1,398,101 /2^64 =7.579120707770781e-14. If each switched coordinate marginal uniform, union upper bounds for n687/n788/n828:5.214e-11/5.980e-11/6.283e-11 respectively for ANY COORDINATE discrepancy, not decrypted-output DFR and no conditioning on real KSK distribution. Average true functional error may be much smaller due to message margins or cancellation.

Native arithmetic-only Go benchmark on AMD EPYC 9V74, -benchtime=100ms count3: float64 10.30–10.98ns/op, exact power2 integer shift1.041–1.091ns/op, bits.Mul64 exact1.046–1.178ns/op. No full-PBS timing. Replacement requires only public integer arithmetic, no new keys; exact code is known/standard in TFHE tooling and is an upstream engineering fix, NOT a novel cryptographic algorithm. Do not characterize the earlier B054/B055 threshold mismatch as crypto DFR evidence.

FINDING findings/boot-B056-carousel-valid-lwe-functional-lut-guard-and-kernel-cost-gate.md
NEXT B057: Archive this trivial scalar precision correction as research line; audit a DIFFERENT contemporary BOOT primitive with a core nontrivial dataflow/noise/key optimization, source code and full paper, one falsifiable hypothesis, true novelty/performance/security gate. SHIP remains PAUSED_BY_PI. B057 NOT STARTED.
