# BOOT-B033 — Input-adaptive Companion Modulus Switch: certified rounding-cost knapsack and full-LWE-tail falsifier

TRACK_ID: BOOT
ITERATION: B033
DATE: 2026-10-19
STATUS: PASS_EXACT_INPUT_ADAPTIVE_LOCAL_PARETO / FAIL_VARIANCE_BUDGET_AS_FULL_DFR_CERTIFICATE / UNCLEAR_CONFERENCE_PRIOR_ART_AND_PUBLISHABLE_NOVELTY
STATE_UPDATE: YES

## PI scope and primary hypothesis
BOOT problem-first audit; maintain strict research-track isolation. Following B032 of Bergerat et al. sorted extended TFHE PBS, primary falsifiable claim:
**The public input's actual modulus-switching rounding residuals can be used to choose a CMS subset of floor/ceiling flips that saves strictly more sorted CMuxes than the simple fixed-d fixed-order subset at NO greater conditional binary-secret mask-rounding variance and NO greater distribution-free conservative absolute-error envelope, without any new evaluation key.**
The cheap decisive tests were exact combinatorial coefficient-class algebra, exhaustive legal-flip subset knapsack on 500 sampled public LWE mask arrays, and 2^12 full binary-secret enumeration using syntactically valid noiseless LWE ciphertexts to FALSIFY any stronger full-DFR guarantee. One hypothesis; no changes to scheme source or user SHIP project.

## Sources and provenance
[FACT] Bergerat–Orfila–Roux-Langlois–Tap, "Accelerating TFHE with Sorted Bootstrapping Techniques," ASIACRYPT (7) 2025:68–100 DOI 10.1007/978-981-95-5122-4_3, ePrint 2025/2214. Full title-verified 48 physical pp mirror PDF SHA256 8e342f162db953a4c26d2103f66406b5148b6fa798c7775478342900d9850d84 (VERSION_UNVERIFIED). §4 pp19–23 Lemma6/7 Algorithm3: sorted CMux class cost η/µ_k for mask coefficient divisible by µ_k. §5 pp23–27 CMS permits flipping floor/ceil on chosen d coefficients, explicitly says "Any of the ai for the d modified values can be chosen, but to simplify the d last values are taken"; Lemma8 ALREADY analyzes mean and variance, Lemma9 gives d-dependent average and best-case CMux costs; §7 and Appendix benchmarks on pp39–40. Therefore input-dependent *selection of any index* is NOT a new correctness primitive, nor is computing a knapsack from public costs original in general. Absence of native source repo verified here; SOURCE limitations no native FHE benchmarking / IND-CPA-D proof.
[RELATED FACT] Signed/onehot key material may induce key-distribution-specific conditional noise. Public coefficient-dependent rounding changes the input-mask distribution given evaluator strategy, and may interact with attack/failure model; one cannot silently apply unmodified independent uniform error assumptions from source Lemma8.
[SHIP READ-ONLY SCREEN] The user also requested comparing past BOOT techniques to separate SHIP eval-key memory research. Latest SHIP Library snapshot SHIP_PAUSED_STATE_2026-10-19.md shows TRACK_ID SHIP PAUSED_BY_PI after I407, no authorized active iteration; source poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf, N256 Real Quad radix54 IFMA prepared key 72,630,272B ->66,338,816B (6MiB,8.6623%), security/KDM and full noise UNCLEAR, P3 NOT_AUTHORIZED. Core onehot affine completion is known CMux onehot+Galois arithmetic NOVELTY_FAIL_CORE_MECHANISM. Discussion limited to classification of already completed BOOT methodology, NO SHIP new hypothesis/test/literature research, NO SHIP writes or work resumption. An old GitHub Notes ship-memory-STATE.md is NOT authoritative vs 2026-10-19 Library freeze.

## Exact mathematical local objective and eligibility gates
Let α=q_in/q_out be integer for the minimal finite model. A public coefficient a_i has scaled real x_i=a_i/α, standard nearest integer output y_i, alternative legal floor/ceil output y_i'. If x_i is ALREADY INTEGER, floor=ceil and no CMS flip is legal: exclude such a_i; do not mistake y_i+1 for valid "opposite rounding". Nearest tie at half integer uses an explicit fixed tie rule (half-up), and the alternative is the other integer.
Write r_i=y_i−x_i, f_i=|r_i|≤1/2, r_i'=y_i'−x_i. For valid distinct rounding options:
  |r_i'|=1−f_i,
  (r_i')²−r_i²=(1−f_i)²−f_i²=1−2f_i,
  |r_i'|−|r_i|=1−2f_i.
This IS an exact per-coordinate identity.
For SBS power-of-2 η, class cost c(y)=η/gcd(y,η), where c(y)∈{1,2,...,η}. An eligible beneficial flip has g_i=c(y_i)−c(y_i')>0. Let z_i∈{0,1} choose flip, w_i=1−2f_i≥0. Knapsack:
 max Σ_i g_i z_i subject Σ_i w_i z_i ≤W, z_i only on LEGAL CMS positions.
Under IID uniform binary secret s_i independent of PUBLIC a, variance contribution from mask rounding E_mask=−Σ r_i s_i has Var(E_mask|a)=1/4 Σr_i², so the proposed subset increases this variance by exactly ΔVar=1/4Σw_i z_i. It also increases ∑|r_i| by exactly Σw_i z_i; hence the conservative deterministic error envelope |e_MS|≤|e_input|/α+1/2+Σ_i|r_i| (UNMODIFIED standard rounded body, no extra public body shift) never exceeds the comparator under budget matching. This envelope is conservative, with no probabilistic independence assumption about the binary secret. If optionally adding B032's public BODY centering t≈(1/2)Σδ_i, the robust worst-case bound must ALSO add |t|; do not conflate centering with a free worst-case guarantee. This is a local MS error bound, NOT a complete PBS/IND-CPA-D proof.

## Exact combinatorial enumeration at source-shaped small parameters
Parameters q_in=1024, q_out=64, α=16, η=8, n=12, public A_i∈{0,...,1023} uniform IID; deterministic Python Random(20261019), 500 masks. 499 masks contain >=2 beneficial CMS-eligible coefficients after excluding x integer positions. Comparator: take LAST k=min(3,#eligible) eligible positions in index order, mirroring one simple permitted *fixed-position* strategy; it is NOT the whole original author's choice space or the mathematically best original CMS! Let baseline extra rounding budget W_base=Σ_{i selected}w_i. For each public mask, ENUMERATE EVERY subset of the beneficial eligible positions, maximize Σg_i subject Σw_i≤W_base, tie by smaller added noise. Costs computed with integer-scaled r_i (r in numerator units 1/16):
  exact Δ(r_num²)=16*(|r_num_alt|−|r_num_std|), giving rational-budget exact comparisons with no floating ambiguity.
Results:
  legal instances: 499.
  strict higher CMUX saving: 323 / 499.
  equal CMUX saving but strictly lower extra mask-error budget: 35 /499.
  conditional mask-variance increment <= baseline: 499/499.
  average source-mask CMUX cost per 12 public coefficients: fixed order 48.7995992 vs optimal 44.6312625, a reduction (48.7995992−44.6312625)/48.7995992 = 8.5417%, TOY mask-specific CMUX cost only, not end-to-end PBS speedup.
  mean CMUX saving: baseline15.6032064 vs adaptive19.7715431.
  avg total binary mask-rounding variance per 12 coords after modifications: baseline0.5973255 vs adaptive0.5670775, conditional on fixed a, iid Bernoulli keys, excluding body noise.
An exact concrete 12-coordinate instance:
 public A=[149,329,393,491,202,435,623,224,460,544,707,351].
 baseline last three eligible positions (5,6,8) has total CMUX62, ∑|r|=4.625, mask var=0.71484375.
 optimal under SAME extra noise budget selects 6 positions (0,1,2,4,5,8), has total CMUX43, ∑|r|=4.625, mask var=0.71484375.
 Standard nearest rounding (no flips) CMUX78, ∑|r|2.625, mask var0.21484375.
 These are deterministic finite exact results, NOT secure TFHE parameter cases. Increasing number of modified positions does NOT necessarily increase these two noise-budget metrics: near-half-interval flips may be cheap.

## Full valid-LWE exhaustive tail gate: crucial negative result
To avoid the misleading assertion "lower conditional mask variance means lower PBS DFR," independently enumerate all 2^12=4096 binary secrets s for EACH public A. Construct noiseless syntactically VALID LWE encryption of plaintext m=0 at q_in=1024 with b=Σ_i A_i s_i mod1024, so the input phase b−Σa_i s_i=0 (modq_in). Public body nearest rounded to q_out=64. For a CMS subset, optionally apply B032 public body-center correction t=nearest_integer(Σδ_i/2), with δ_i=y'_i−y_i; then compute exact output phase e= centered_mod64( round(b/16)+t−Σ_i y_i^CMS s_i ). This is an exact valid LWE arithmetic test without encryption error; tiny params make secret recoverable in practice and NOT cryptographically secure.
For all 499 public masks and all 4096 secret choices each (=2,043,904 exact cases per variant), compare tail P(|e|≥2):
 adaptive lower tail than fixed comparator in 243 public-mask inputs; equal in176; HIGHER (worse) in80 inputs, despite budget Var(E_mask) ≤ baseline. Average tail across 499 public inputs fixed 0.1348840 and adaptive0.1209186 (not end-to-end DFR, qout64 threshold2 illustrative).
  Concrete A above, with both methods public body-centering, baseline fixed CMUX62, mask var0.71484375 has exact tail Pr(|e|≥2)=0.0771484375 (316/4096), adaptive CMUX43 same mask var0.71484375 has exact tail0.1494140625 (612/4096), WORSE. Adaptive also slightly worsens max abs error from2 to3 on this public A.
WITHOUT body correction the tail-worsening cases are even more numerous: 130/499 worse at |e|≥2; baseline average tail0.1726299, optimized0.1582232. Thus the mean budget is NOT a sufficient proof of improved conditional DFR of a full ciphertext: body rounding r_b depends on secret through VALID ciphertext b, and changes in coefficient directions and public centering can alter correlation and exact tails. This is decisive FAILURE of stronger end-to-end performance/security claim. The conservative distribution-free ∑|r| envelope remains no worse (without body correction), but this bound can be far too coarse to pass a realistic 2^-128 or IND-CPA-D proof.
No native sorted PBS, no full GGSW/KS noise, no different secret distributions, no IND-CPAD adversarial ciphertext attack, no security matched parameter search, no comparative overhead for O(nW) dynamic knapsack. Never claim 8.5% real PBS speedup or security.

## Novelty and author-technique checks
- Paper ALREADY permits arbitrary d coefficient choices and analyzes average/best CMUX savings, nonzero noise mean and variance. Optimization by public cost/weight is a standard knapsack; the fact one can avoid high-error flips is not a new cryptographic primitive. What is NOT established as prior-published is the exact input-aware tail-certified selection policy for SBS under chosen ciphertexts/IND-CPAD and net latency; no scheme/proof exists here. Mark novelty UNCLEAR/LOW.
- A possible genuine next issue (NOT TESTED B033): derive a dependence-aware or deterministic *total-noise* per-input CMS selector that accounts for r_b and adversarial/unknown s, and proves tail/param improvement while avoiding per-input expensive search. However full scalar LWE conditional key distribution vs (a,b) under IND-CPA-D differs dramatically from IID assumption, so do NOT infer a free guarantee.
- The key take-away borrowed from prior BOOT/VFHE methodological history is **jointly optimize an operation's legitimate publicly observable cost and the precise worst-case/correlated noise bound, then test the entire encrypted dataflow, not only averaged margin**. This is research method, not a claim it fixes SHIP.
- SHIP freeze preserved per user constraints: just note mapping high level to already documented I407 6MiB key layout and known affine completion; no SHIP iteration/executable candidate proposed, and no canonical SHIP writes.

## End-of-iteration
STATUS: PASS_ADAPTIVE_COST_ROUNDING_PARETO_IN_LOCAL_MODEL / FAIL_UNIFORM_FULL_LWE_DFR_TAIL_IMPROVEMENT / UNCLEAR_NOVELTY_NO_NATIVE.
RESULT: Public residue-aware subset selection materially improves toy CMUX count under same conservative residual envelope vs simple fixed-position subset, but an exact 2^12-valid-LWE counterexample shows a lower variance budget cannot certify a better actual error tail; original paper already allows arbitrary d positions and public optimization is nontrivial only if coupled to NEW security/noise/DP/online algorithm. No paper-ready scheme now.
NEXT_TEST B034: Continue BOOT-only problem-first audit. One primary hypothesis either (A) attempt a **source-exact, adversarially safe tail-certified CMS selector** with full error/mean/covariance and efficiently evaluable budget, comparing best allowed 2025/2214 CMS choices and secret distributions, OR (B) archive minor input-selection subbranch and audit another recent full-source bootstrapping algorithm's genuine structural bottleneck. Prefer cheap decisive correctness/security/prior-art criterion before bigger experiment. Do not reopen paused SHIP automatically.
STATE_UPDATE: YES. BOOT-only file writes.
