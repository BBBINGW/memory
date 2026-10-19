# BOOT-B034 failure archive — b-dependent CMS selection cannot invoke iid-secret conditional variance; elementary certificate alone is not a new SBS algorithm

TRACK_ID: BOOT
ITERATION: B034
DATE: 2026-10-19
STATUS: FAIL_B_CONDITIONED_BERNOULLI_TAIL / PASS_EXACT_WORST_CASE / PASS_A_ONLY_HONEST_KEY_CERTIFICATE / NO_PUBLISHABLE_NEW_CONSTRUCTION

Original Bergerat–Orfila–Roux-Langlois–Tap, "Accelerating TFHE with Sorted Bootstrapping Techniques" ASIACRYPT2025, ePrint2025/2214, title-verified 48pp mirror sha256 8e342f162db953a4c26d2103f66406b5148b6fa798c7775478342900d9850d84 VERSION_UNVERIFIED. §4 Algorithm3 pp21–22, §5 Lemma8 p24: CMS already permits ANY chosen d locations, simply using the last d for exposition. It already studies nonzero MS noise mean and variance. A public index-aware knapsack is NOT intrinsically new.

CRITICAL FALSE PROOF STEP: Under honest LWE generation b=Σa_i s_i + Δm +e (mod qin), iid Bernoulli secret bits remain iid if conditioned on a only (uniform public a independent of s), but NOT when conditioned on BOTH public a,b. Simple exact n1 a=1,e=m=0,b=s case: observing b1 forces s1=1. Therefore an a,b-ADAPTIVE CMS subset has secret-dependent distribution even though the selected outputs/rounding directions are public, so E[Σr_i s_i|a,b]=Σr_i/2 and conditional Hoeffding do NOT automatically hold. This invalidates an immediate 2^-128 claim or IND-CPA-D reasoning based on independent bits.

SAFE algebraic fallback: with r_i=selected a rounding residual, r_b=body residual, public body shift t, for BINARY secret s:
sup_s |r_b+t−Σr_i s_i|=|r_b+t−(Σr_i)/2|+Σ|r_i|/2 =R_worst.
This is an exact UNMODDED supremum, works for body-adaptive choices and arbitrary s; preserves sufficient correctness when E/alpha+R_worst below message tolerance. 200/200 independent small exact n12 brute-forced cases confirmed. It is often much looser than stochastic tails, so NOT a source-realistic DFR theorem.
Allowed positive but limited repair: Choose CMS indices and public body shift t ONLY from a. For uniform independent Bernoulli s, conditional on a, centered mask sum Z=−Σr_i(s_i−1/2) has mgf ∏cosh(λr_i/2)≤exp(λ²Σr_i²/8), hence for |e_in|≤E:
 Pr(|eout|≥E/alpha+1/2+|t−S/2|+u | a)
 <=2exp(−2u²/Σr_i²),
since |r_b|≤.5 even though it depends on secret. Valid for honest fresh input model, NOT arbitrary chosen ciphertexts, changing secret distribution, or full GGSW/KS noise. The modified output is only same plaintext if its total phase error remains within the LUT margin.
EXACT toy qin1024,qout64,alpha16,eta8,n12,500 public masks, ε=2^-24, public t(a)=round(S/2), select legal beneficial flips to maximize CMUX savings without increasing R_epsilon versus last up-to-3-beneficial-index comparator: 330/500 strictly higher saved CMUX, all 500 certificate ≤ comparator; mean CMUX48.768→44.544, ~8.66% of TOY CMUX ONLY, compared to WEAK fixed-order baseline, NOT best CMS allowed by source. Full 500*4096=2,048,000 exact honest LWE(0) enumerations per variant: illustrative |error|>=2 frequency139552→114680 (6.814%→5.600%); >=3 1762→985 (0.0860%→0.0481%). Nevertheless at |error|>=2 candidate worse on38/500 PUBLIC a masks; bound is not a per-a tail ordering theorem. No native secure parameters, no error tails 2^-128, and subset search is exponential O(2^n), impossible at n≥630 without new efficient algorithm.
b-AWARE conservative envelope 3000 tiny honest examples, under same exact R_worst as fixed comparator, 2221/3000 higher CMS gain, avg bound2.8575→2.6770; but some individual actual errors worsen (see finding). This tests cost vs deterministic bound but no realistic certified performance.
No full SBS/CMUX, GGSW error, correlated reusable secret, IND-CPA-D guarantee, secure parameter search or latency; source already permits arbitrary selected d and standard LWE switching tail techniques. Thus no new publication-worthy algorithm established. DO NOT make a security-vulnerability claim about source paper.
FULL EVIDENCE: findings/boot-B034-body-aware-cms-robust-and-honest-tail-certificate.md
DECISION: end CMS microbranch (B032–B034) unless a genuine efficient tail-aware construction beating best paper CMS and surviving security+native benchmark is identified. B035 choose DIFFERENT full-source modern BOOT bottleneck and one falsifiable repair, no unrelated ZK/VFHE or paused SHIP execution. BOOT only.
STATE_UPDATE YES.