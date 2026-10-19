# BOOT-B055 — Carousel ModSwitch: valid-LWE phase counterexample and exact integer correction

TRACK_ID: BOOT
ITERATION: B055
DATE: 2026-10-20
STATUS: PASS_VALID_LWE_NONCANCELLATION / PASS_EXACT_NATIVE_GO_INTEGER_REPAIR / PASS_LOCAL_MICROBENCH / LOW_NOVELTY
STATE_UPDATE: YES
ISOLATION: BOOT ONLY; SHIP paused by PI, no SHIP read or write.

## Recovery and one falsifiable claim
On reconnect, repo findings listed B054 as latest, with findings/boot-B054-carousel-float64-modswitch-threshold-integer-repair.md SHA 4ffcbe6c06e9198087debd4d85ad78cc9e3e17f6. There are also historical duplicate B040/B041 files; preserve untouched. GitHub Notes read_repo_file returns empty object for old contents, so base B054 content was recovered instead from mounted /mnt/data/boot_b054_carousel_modswitch.go and verified current GitHub author code. Do NOT assert old full STATE.md text was actually read.
PRIMARY: B054 found isolated FLOAT64 rounding differences in mod-switch uint64 to LUT integer. Are these ALWAYS canceled when one applies the same conversion to b and all masks of a mathematically legal noiseless LWE encryption, such that blind-rotation phase is unaffected? Test source-exact nearest switch on constructed LWE with real source default LUT and derive efficient integer repair, full phase—not one coefficient.

## Author source and version
[FACT] Park et al., Carousel: Fully Homomorphic Encryption, ePrint 2024/2032, https://eprint.iacr.org/2024/2032.pdf ; author repo https://github.com/SNUCP/carousel default branch Git tree SHA 21d5800462920d63afcc58873446455642588297. carousel/bootstrap.go Git BLOB 53111c68a004cfb36c5f6f368e38a2ccffd6cfae, lines35–37:
  func (e *Evaluator) ModSwitch(x uint64) int {
    return int(math.Round(e.modSwitchConstant*float64(x))) % e.Parameters.lookUpTableSize
  }
And lines60–154 use ModSwitch for the initial LWE body and each LWE mask in blind rotation. carousel/params.go Git BLOB 05fbbc8edf0a08e52e28d06ad5ecfa3cb1a0513b, lines246–248 require power-of-2 PolyDegree and line267 sets lookUpTableSize=PolyDegree; carousel/params_list.go Git BLOB8fd34601da8fd5d0109790800ee55c58b759ba73 has PolyDegree2048 in listed presets. math/num/num.go Git BLOB25a503f5b404ac23c3d43f8f351d30f9eab30d39 has DivRoundBits, which the source ModSwitch does NOT call. Individual file blobs pinned; no modifications made to authors repo.
Exact torus q=2^64, LUT T=2048=2^11, grid G=q/T=2^53, midpoint H=G/2=2^52. Intended canonical unsigned nearest switch M(x)=floor(x/G+1/2) moduloT (ties up).

## Decisive full-LWE noiseless counterexample [DERIVATION + GO NATIVE]
Choose binary secret s=(1,1) (not a secure secret distribution instance) and message m=0, encryption error e=0. Let j=1024 and
 a1=(2j+1)H−1 = 9227875636482146303
 a2=−G/4 mod2^64 = 18444492273895866368
 b=(a1+a2) mod2^64 = 9225623836668461055.
Then the ciphertext is ALGEBRAICALLY VALID with b−a1−a2=0 mod2^64.
Source FLOAT64 ModSwitch returns indexes for [b,a1,a2]=[1024,1025,0]. Exact M returns [1024,1024,0]. Thus corresponding ideal blind-rotation exponent from LWE phase moduloT is source −1=2047 versus mathematically intended0. The coefficient errors DO NOT ALWAYS cancel, even for noiseless valid LWE input; the actual LUT evaluation can differ if adjacent positions do not map to same output. Not proof that standard params lose decoded correctness/INDCPA, because +1 LUT exponent shift might be inside margin and this adversarially chosen public mask pattern is extremely rare under fresh uniform mask.
General constructive family: for all j=0..2047, a1=(2j+1)H−1, a2=(-G/4) mod q, b=a1+a2 modq yields true phase0; source float mask switching and full phase WRONG in 2047/2048 cases (only j0 lacks float error). Distinct input examples, NOT distributional DFR data.

## Public constant-time integer repair [DERIVATION]
For any uint64 x and positive LUT L<=2^63-1 use 128-bit exact unsigned multiplication:
 hi,lo := bits.Mul64(x,uint64(L))
 if lo >= uint64(1)<<63 {hi++}
 return int(hi%uint64(L))
Because x*L=hi*2^64+lo, nearest(x*L/2^64)=hi+1_[lo>=2^63], ties up, then moduloL. No floating conversion, extra keys, modulus or phase rounding beyond intended modswitch.
Power-of-2 special case L=2048 uses q=x>>53; if x&((1<<53)-1)>=1<<52 then q++; return int(q&2047).
[VERIFIED] Standalone compiled Go1.23.2 native x86-64 script /mnt/data/boot_B055_carousel_phase.go SHA256 f307c55aceb509d031374afda74518a8830ab40c12a447c9999c0a11f43f2c60. Native output:
 - exact legal zero-noise LWE constructed; source indexes [1024,1025,0], exact [1024,1024,0]; phases 2047 vs0 PASS;
 - 2048/2048 source-near-threshold bit-shift/Mul64 agreement;
 - 255000/255000 (x,L) pairs across17 moduli incl non powers of2 and large moduli using independent math/big exact 128+bit quotient+remainder reference PASS;
 - 2047/2048 threshold-picked legal full LWE phase failure for float path, all exact path zero.
[CROSSCHECK PRIOR B054] Re-ran mounted /mnt/data/boot_b054_carousel_modswitch.go SHA256 d4773014c68197f145e60f00a47b9f4c2ace58a520a990d40cc2ef418db2c927: 8,603,648 immediate threshold inputs in Go PASS; exact single uniformly random raw uint64 index-mismatch count1,398,101/2^64, probability7.5791207077707812e-14. For 687 independent uniform masks union bound <=5.20685592624e-11 for ANY index mismatch (not measured DFR or broken output probability). The threshold-crafted ensemble is intentionally nonuniform, cannot equate 2047/2048 to a real FHE failure rate.

## Local native arithmetic microbenchmark and scope
Created /mnt/data/boot_B055_bench/modswitch_test.go SHA256 d4ae3eb84390570bae9a7ff8e55a4f1323155877dd906656e76ece27a3254385. Go1.23.2 linux amd64 AMD EPYC9V74, deterministic 65536 uint64 corpus, 3 x 400ms measurements per function:
 Float source-like 9.412, 9.816,10.57 ns/op;
 Exact power2 bitshift 1.022,1.053,1.051 ns/op;
 bits.Mul64 with compiler constant L2048 1.082,1.107,1.028 ns/op.
 0B alloc/op. So ~9–10x local source arithmetic microbench improvement, NOT end-to-end bootstrapping acceleration, not generic variable LUT performance; FFT/BlindRotate dominates total and CPU compiler differs. Two test files were actually run; NO author full source code compiled nor full ciphertext encrypted benchmark.

## Noise/security/novelty and final decision
[CORRECTNESS] Float64 can shift ideal BR exponent even for valid noiseless LWE; exact public int formula repairs this implementation defect.
[NOISE] Source's intended integer switch still has unavoidable rounding noise; a one-LUT-index offset need not exceed final decoding tolerance. No actual LUT-specific decrypt failure / noise budget or correlated ciphertext experiment validated.
[SECURITY] Pure public numeric arithmetic; no key distributions or hard problems altered. No cryptographic attack claimed.
[PRIOR ART] bit-shift nearest torus modulus switching, fixed point integer product and 128bit arithmetic are basic implementation techniques, even used elsewhere in codebase (math/num DivRoundBits). The correction is valuable implementation hygiene/bug report but NOT a publishable new FHE Bootstrapping primitive; don't stretch it into an indefinite microbranch.
[DECISION] PASS valid-full-phase falsifier and patch. No new algorithmic bootstrapping optimization. Archive B054–B055 Carousel float precision microbranch. Recommend B056 pick different real full-source FHE bootstrap algorithm with substantive unexploited stage/secret/dataflow, not another trivial index rounding/BSGS/key-row memory adjustment. Still one primary hypothesis, cheapest decisive test, full source/noise/security/cost/novelty gates. Ship remains PAUSED_BY_PI after I407.
END ITERATION: STATUS PASS / RESULT as above / NEXT_TEST B056 source-first genuine algorithm bottleneck / STATE_UPDATE YES.
