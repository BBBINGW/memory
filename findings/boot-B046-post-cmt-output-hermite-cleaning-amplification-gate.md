# BOOT B046 — Output-alphabet post-CMT Hermite cleaning versus one-hot pre-CMT cleaning: amplification and ciphertext-type gate

TRACK_ID: BOOT
ITERATION: B046
DATE: 2026-10-20
STATUS: PASS_CONDITIONAL_BOOLEAN_POST_CLEANING_ALGEBRA / FAIL_UNCONDITIONAL_NOISE_CORRECTNESS / FAIL_FREE_DEPTH_OR_MAJOR_OPERATION_GAIN / LOW_NOVELTY
STATE_UPDATE: YES
ISOLATION: BOOT-ONLY WRITES. SHIP remains PAUSED_BY_PI after I407.
PREVIOUS: B045 is latest CONFIRMED completed iteration (repo listings), so B046 is the next number. Notes read_repo_file consistently returned {} despite list_repo_files SHA-confirmed existing B045 sources. B045 filename: findings/boot-B045-cmt-bit-influence-partial-hermite-cleaning-gate.md, failure: failures/boot-B045-selective-cleaning-not-universal-depth-or-novelty.md. Respect its archived partial bit influence idea; B046 differs by moving the clean operation AFTER all tensor LUT contraction for Boolean-valued outputs. Do not assert having read B045 body live.

## One falsifiable primary hypothesis
In Dumezy–Alexandru–Polyakov–Clet–Chakraborty–Boudguiga, "Evaluating Larger Lookup Tables using CKKS" (ePrint 2025/1301, TCHES 2026(1) pp559–591), CMT-FBT Algorithm7 cleans each of p*d noisy Kronecker digit selectors before CMT, with d=ceil(log_p P). For Boolean LUT f:Z_P→{0,1}, can instead evaluate the ENTIRE CMT tree on uncleaned selectors in CKKS slots, then apply ONE G(x)=3x²−2x³ cleaning to the Boolean output before SlotsToCoeffs, preserving the final integer message/noise/DFR while substantially reducing key/runtime/level cost? This is an output-alphabet-based *placement* change, unlike B045's partial per-input-bit cleaning. Cheap tests: source-exact algorithm shape, onehot tensor with sum-to-one perturbations and a publicly chosen legitimate Boolean LUT, exact polynomial error test; complete source encodings and operation counts. User PI controls whether any new direction is worth pursuing.

## Evidence and provenance
[FACT] Original IACR ePrint 2025/1301 cached GitHub mirror copy title-verified VERSION_UNVERIFIED, source https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/1301.pdf, PDF SHA256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19, 35 physical pages. Sections and verified extracted physical pages:
 - p17–18 §4.2: BLEACH-derived cubic Hermite cleaner G_id=3X²−2X³ applied to binary digits before BMT, 2 multiplicative levels; known preclean not novel.
 - p19–20 §5 Algorithm6 defines CMT via tensor Kronecker onehot product, LUT scalar multiplications and sums; p20 Algorithm7 runs FDD (p onehot selector ciphertexts for each of d digits) → clean ALL p*d selector ciphertexts → CMT → SlotsToCoeffs → output modulus switch. It analyzes output worst-case noise O(P² d)*input selector error and CMT cost Θ(P) ct multiplications and P scalar ct multiplications/adds.
 - p23–25 §7 and benchmark: lazy rescaling and relinearization already implemented, cleaning large LUT inputs causes +2 levels; CMT large LUT scalar operations are dominant.
 - p26 notes at LUT input >18 bits need 2+ cleaning rounds; memory for P20 128GB class and output errors critical. No reason to assume unclean tree is safe at p16,d4.
 - Original authors' method precleans onehot digit indicators. This B046 does NOT claim authors lacked any equivalent output cleaning elsewhere, only that source Algorithm7 doesn't instantiate this placement.
[PRIOR ART] OpenFHE already implements Hermite-trigonometric integer LUTs, e.g. https://openfhe-development.readthedocs.io/en/latest/api/classlbcrypto_1_1FHECKKSRNS.html ; FPT etc. Alexandru–Kim–Polyakov–Zheng ePrint 2026/1026 "Sparse Hermite Interpolation Method for Discrete-CKKS Functional Bootstrapping" ABSTRACT verified at https://eprint.iacr.org/2026/1026 explicitly develops sparse arbitrary-order Hermite cleaning with noise-budget metric; FULL PDF retrieval through Research Notes FAILED HTTP403 and fixed mirror absent, so do not claim read this full paper. Its public abstract means merely using Hermite output correction is already heavily prior-art adjacent, not a new primitive. Do not extrapolate statements about the full 2026 method.

## Algebraic legitimate adversarial Boolean LUT toy
Let p=4 digits d=4, LUT input domain size P=p^d=256, actual encrypted digit tuple all 0. At each digit take APPROXIMATE onehot selector vector:
   z=(1+epsilon,−epsilon,0,0), epsilon≥0.
This has Σ_j z_j=1 EXACTLY and each incorrect component is bounded by epsilon. It is compatible with a onehot selector's ordinary approximate CKKS interpretation; not claimed to exactly represent secure MVB error distribution. For each tuple a=(a0,...,a_(d-1)), unclean tensor weight w_a=Π_k z_(a_k). Then Σ_a w_a=1 and ||w||_1=(1+2epsilon)^d. Define a perfectly LEGAL publicly chosen Boolean LUT f(a)=1 iff w_a>0, otherwise f(a)=0; since w_(0,0,0,0)=(1+epsilon)^d>0, correct plaintext f(0,...,0)=1.
CMT contraction is therefore
   y=Σ_a f(a)w_a=(1+||w||_1)/2=1+delta,
   delta=((1+2epsilon)^d−1)/2.
The ordinary Boolean cubic cleaning G(x)=3x²−2x³ satisfies
   G(1+delta)−1=−3delta²−2delta³.
Its absolute error is 3delta²+2delta³, which exceeds the original delta WHEN delta > delta*=(sqrt(17)−3)/4=0.2807764064. Hence adding ONLY a final Hermite gate can WORSEN exact final error even for legitimate Boolean LUT with sum-to-one approximate digit indicators.
For d4 with only one erroneous alternative selector/digit, criterion delta<delta* requires epsilon<[(1+2delta*)^(1/4)−1]/2≈0.0589322561. At epsilon=.07 (each digit selector error small, sum exactly1), delta=.34448008; unclean y=1.34448008; G(y) deviates from desired1 by .437756085 (> .34448008), so postclean makes noise WORSE. At epsilon=.10 it catastrophically overshoots: delta=.5368, postclean error1.173825.
More general pessimistic selector class for p>=2: z_true=1+(p−1)epsilon, each p−1 false onehot =−epsilon, giving ||z||_1=1+2(p−1)epsilon. Under d tensor levels choose f=1 on positive product weights, ftrue=1. Worst positive output deviation delta=((1+2(p−1)epsilon)^d−1)/2, so for cubic cleaning to improve this adversarial class sufficient AND necessary epsilon<[ (1+2delta*)^(1/d)−1 ]/[2(p−1)]. At p16,d4 threshold≈0.00392881707. This is a strong BEST-CASE ALGEBRAIC REGIME gate on max selector error; it is NOT a measured real CKKS MVB error or a proven failure probability, and actual digit errors may have special dependencies that rule out this adversarial sign configuration.
This is a decisive counterexample against the UNQUALIFIED hypothesis: "Boolean output means one terminal Hermite cleaner replaces all onehot cleaning with no accuracy/DFR loss." It is not an attack on the published paper.

## Preclean vs postclean exact paired numerical test (private reproducible math)
At the same input use two layouts:
  ORIGINAL-like: clean each z selector BEFORE CMT using G(z). Because G(1+epsilon)+G(−epsilon)=1 and each transformed component is nonnegative for small eps, the new tensor weights form a nonnegative partition of unity, so final Boolean y_pre∈[0,1] for arbitrary LUT and the adversarial f error is far smaller.
  CANDIDATE: tensor contraction uncleaned y first, compute G(y) ONCE.
For p4,d4, legitimate LUT f=indicator of positive unclean weights, exact double polynomial:
 eps 0.01: |unclean−1| .04121608; |post−1| .005236329; |pre−1| .001206906.
 eps 0.02: .08492928; .022864135; .004846285.
 eps 0.05: .23205; .186532094; .030286669.
 eps 0.07: .34448008; .437756085; .058761081.
 eps 0.10: .5368; 1.173825112; .116227899.
Even for eps0.01, post output cleaner is ~4.34x WORSE than per-digit cleaning in this instance despite being better than UNclean. The noise-vs-online-work frontier might be appropriate in a special low-noise workload, not a universal substitute for author's correctness margin.
These are exact polynomial contractions evaluated with Python floating point but symbols are simple rational polynomials; no native FHE ciphertext, digit-decomp output noise, secret security, or probability experiment.

## Important end-to-end ciphertext representation/type gate
Postclean can ONLY be performed while output is still CKKS SLOT-encoded (after CMT and BEFORE SlotsToCoeffs). If delayed until after SlotsToCoeffs, the output is encoded as independent plaintext COEFFICIENTS of RLWE ring, not SIMD CKKS slots: ordinary homomorphic multiplication is polynomial NEGACYCLIC CONVOLUTION, not coefficientwise. Exact no-noise counterexample in R=Z[X]/(X^4+1): intended independent Boolean coefficients m(X)=1+X => coefficientwise G(1)=G(1)=1, target 1+X, but RING evaluation:
   G(m)=3(1+X)^2−2(1+X)^3
       =1−3X²−2X³ ≠1+X.
Hence after-decoding polynomial clean is WRONG even without noise; correcting would require CoeffsToSlots, CKKS slot processing, SlotsToCoeffs AGAIN, at added key/modulus/precision cost. Placement matters critically, not just the identity on 0 and 1.

## Operation/cost gates and security
Source Algorithm7 for P=p^d cleans p*d Kronecker-selector CKKS ciphertexts using cubic G before CMT when log2P>12; each G requires two ciphertext multiplications and ~2 levels, in parallel across p*d inputs. For p16,d4 P65536: 64 cleaners ~128 ct-ct multiplications total at two multiplicative levels, vs ONE output cleaner ~2 multiplications at two multiplicative levels. Looks like126 ct multiplies saved in this particular cleaning phase (assuming no extra scale/normalization); but CMT itself costs Θ(P)=~65536 ciphertext products PLUS P LUT scalar multiplications; the 126 savings are ≈0.19% relative JUST to nominal P products, not measured end-to-end wall-time, and FDD/cleaning may have specific memory and scheduling costs. Both cleaning placements consume two further sequential multiplicative levels, and postcleaning after CMT raises required remaining modulus at a late stage; author strategy deliberately precleans to avoid high-error CMT multiplies. No key-storage reduction or improvement in core Θ(P) unstructured LUT cost.
Related B045 bit-influence selective Hermite cleaning is already archived; moving an identical existing cubic from many selectors to one output is NOT a new Hermite interpolator and likely too elementary for standalone cryptography publication. 2026/1026 explicitly arbitrary-order sparse Hermite prior-art warning. Real DFR requires complete FDD selector noise joint law, EvalMult/relin/rescale, post CMT scale, LUT output margin, SlotsToCoeffs error, modulus-switch, circular/KDM security assumptions unchanged but cannot claim stronger correctness/precision.
For Boolean output, one may be able to bound precleaned onehot error and find a low-noise regime where postcleaning is safe by provable W<delta*, but practical secure parameters / benchmark not established and could cost less to simply OMIT original cleaning when P not too large (<2^12 per paper). Not new BOOT algorithm as presented.

## End-of-iteration judgment
STATUS: FAIL_UNCONDITIONAL_POST_CMT_CLEANING / PASS_CONDITIONAL_BOOLEAN_SCALAR_PROJECTION / FAIL_POST_DECODING_RING_TYPE / NO_PUBLISHABLE_SPEEDUP.
RESULT: Algebraic adversarial Boolean-LUT toy disproves the stronger expected correctness/noise monotonicity of moving p*d preclean Hermite gates after CMT. Even when safe, output cleaning is weaker; same mult depth, negligible saving relative to P scalar/mul operations for large unstructured LUT, and no clean after coefficient decoding. Prior art confirms cubic BLEACH cleaning and 2026 arbitrary-order Hermite. Archive proposed cheap swap, but retain bound as a rigorous source-specific filter and a lesson on full dataflow.
NEXT_TEST B047: BOOT only. Stop revisiting CMT partial Hermite placement, selective bit cleaning, lowrank LUT layout (B040/B045/B046); choose a DIFFERENT actual FHE bootstrapping paper with full source and core algorithmic open problem, prioritizing amortized parameter/dataflow change with a measurable asymptotic or meaningful operation-count edge and whole correctness/noise/security gates. Candidate other 2026 new functional approaches may have limited source PDFs: sparse Hermite 2026/1026 FULL PDF not acquired (HTTP403 and mirror absent), record missing source if critically needed. Alternatively find full 2026 TCHES original code. Do not begin B047 in this iteration. SHIP remains PAUSED_BY_PI.
STATE_UPDATE YES — only BOOT paths.
