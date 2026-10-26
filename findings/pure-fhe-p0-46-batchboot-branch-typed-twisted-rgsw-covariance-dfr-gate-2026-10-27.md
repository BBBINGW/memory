# PURE-FHE · P0-PRESCOUT-46 — Branch-typed BatchBoot twisted-RGSW noise, common-Auk covariance and DFR certificate

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
PREVIOUS: P0-PRESCOUT-45; findings/pure-fhe-p0-45-batchboot-twisted-rgsw-noise-dfr-key-precision-gate-2026-10-27.md; commit 695145e56cdc9f032c0224e239e65030bbea7ccf.
LATEST_COMPLETED: P0-PRESCOUT-46
NEXT_ITERATION: P0-PRESCOUT-47 NOT_STARTED; PHASE-GATED, PI continuation only
STATUS: PASS_BRANCH_TYPED_COUNT / PASS_CONDITIONAL_INDEPENDENT_VARIANCE_FEASIBILITY / UNCLEAR_RIGOROUS_JOINT_KEY_ERROR_DFR / NOVELTY_UNESTABLISHED
NOVELTY: NOT_ESTABLISHED, shared-secret automorphism key and rowwise RLWE key switching are standard.
CODEX_REQUIRED: NO. No native evaluation/GPU/server/code/infrastructure changes.
STATE_UPDATE: YES one isolated PURE-FHE findings file only; do NOT change global STATE.md or other SHIP/BOOT/CGS/VFHE/EAI.

## ONE falsifiable H46

With P0-44 exact key *plaintext* conversion:
  K^-_s(u)=KS_{tau(s)→s}^{rowwise}(tau(K^+_s(u))), u∈{0,1},
and P0-45 low-base proposed **new** tau_-1 automorphism key B_A=4,d_A=32 (the published source Auk is B_A=2^23,d_A=1), can the ORIGINAL BatchBoot 6-bit target model-DFR <=2^-64 be **certified** when (a) we charge ONLY those specialized external-product branches actually touched, (b) the full packing, ordinary RKS, modulus-switch noises are included, and (c) the same additional Auk_tau key reused across all derivations creates potentially correlated errors?
Cheapest decisive test: original Algorithm 2 exact branch typing and maximum path EP count; original Appendix B/C variance and tail equations; compare (1) conditional independent-variance benchmark with (2) worst-case covariance-safe bound. If former fits but latter fails, status UNCLEAR and isolate a single covariance proof obligation. No native code.

## [FACT] First-party source and physical location

Zhihao Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026, official publisher PDF: https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf .
Web open + screenshots verified PDF zero-based page5 (physical6, Table1 / Eq9 / Lemma4.1), page6 (physical7, Algorithm2), page17 (physical18, Appendix B.4/C.2) and page19 (physical20, Tables9/10 and C.4). Web screenshot zero-based page16 had cache miss, but page16 Appendix B.2–B.3 text was retrieved from the publisher PDF and its algebraic forms are reproduced below. No inferred absent theorem.
Source Algorithm2 lines:
 stage index i=0..ell/2-1, ell=log2n=12 => six stages; each j output has FOUR external product terms;
 group A j∈[0,4^i): 3 twisted (Bsk^-) +1 ordinary (+);
 group B j∈[4^i,2*4^i): 2 twisted+2 ordinary;
 group C j∈[2*4^i,3*4^i): 1 twisted+3 ordinary;
 group D j∈[3*4^i,n): 0 twisted+4 ordinary.
The third output branch uses one tau^-1 product for Bsk^-_i,2; fourth is all Bsk^+. This taxonomy was checked visually, not inferred by treating all four as special keys.
Consequently for a *single output computational path*, there can be at most 3 twisted EP contributions and 4 total per stage (at most 18 twisted and 6 normal IF all 6 stages hit group A, as a pathwise conservative envelope). Different source indices can be routed into j in earlier stages; fixed j's sum of branch labels is not automatically the true expression path after all rotations; the "18+6" bound is a per-stage maximum, not an exact random-output distribution.
For one EMP over all n=4096 output positions, twisted EP CALLS are sum_i 6*4^i=6*(4^6−1)/3=8,190, out of 4*n*6=98,304 EP calls (8.3313%). 34 full-packed EMPs give 278,460 twisted EP CALLS in a batch and 3,342,336 EP calls total. Distinguish full-batch cost count from max output-lineage noise 34*18=612 twisted EP contributions (plus 204 normal) used in conservative branch propagation.
Source §4.2 Lemma4.2 and App.C.2: full packing V_Boot <(h+1) V_EMP +V_Pack+V_RKS, and Lemma4.1 V_EMP < Var(input)+2ell V_EP for directly generated native keys. The author proof says FOUR EP noise contributions per each of ell/2 stages; independence/additivity conditions are not proved for **derived** keys sharing a newly introduced Auk_tau. Source Appendix B.2 variance:
  V_GP = B^2 d N/12 * Var(gadget RLWE row)+N/12 *ceil(Q/B^d)^2;
  V_EP = B^2 d N/6 *Var(RGSW row)+N/12 *ceil(Q/B^d)^2.
RKS uses V_GP. Appendix B.4 for full packing: V_Pack=log2 N*(V_Auto+4 V_MS)+Var(c_in), depending on whether intermediate variance already charged by external V_EMP; avoid double counting without tracking the exact input variable.
C.4 source uses Gaussian tail with output threshold Q/2^(p+2) for message p=6. Model DFR 2^-64 implies normalized output sigma <= 2^-11.194606179588696 ≈0.0004266657189804129.
Tables9/10: Boot6 h33,N4096, Q2^64, input listed Std2^-21; another Boot6 row h512,N2048, Std2^-53. Table10 Boot6 evaluation N4096 and B_Bsk2^23,d_Bsk1, B_Auk2^23,d_Auk1, B_Rlk2,d_Rlk17. **Provenance caveat:** the second Table9 aux row N2048 does not directly certify a newly added Auk_tau under N4096 with sigma 2^-53. The following sigma assumptions are explicitly illustrative. Source measured RAM for full packed 6bit=1425MB (Table13), reported "Key Sizes"=120.1 MB (Table4) not separated by key class.

## [DERIVATION + TOY_EXECUTED] Typed branch variance under favorable illustrative independent noise

Use torus-normalized units, Q=2^64, N=4096, B_B=2^23,d_B=1, h+1=34. Illustrative favorable native Bsk+ and new Auk_tau encryption noise sigma_+=sigma_A=2^-53 — not source-certified for new Auk_tau at matching ring parameters.

New Auk_tau B_A=4,d_A=32 gives derived per-row sigma (original row plus KSK):
 v_A=(B_A² d_A N/12)*sigma_A² + (N/12)*(ceil(Q/B_A^d_A)/Q)^2,
 v_tw=sigma_+²+v_A.
 Numerically sqrt(v_A)=2^-44.29248125, sqrt(v_tw)=2^-44.29247712.

Native and twisted EP marginal variance proxies are
 v_plus=(B_B² d_B N/6)*sigma_+² + (N/12)*(ceil(Q/B_B^d_B)/Q)^2,
 v_minus=(B_B² d_B N/6)*v_tw + (N/12)*(ceil(Q/B_B^d_B)/Q)^2.
 sqrt(v_plus)=2^-18.79239320=2.20255091391824e-6;
 sqrt(v_minus)=2^-16.55191396=1.04082427260789e-5.

*IF* the EP errors are marginally independent/uncorrelated in exactly the way needed for variance addition, a conservative branch-counted single-output proxy (excluding original final RKS, packing and MS) is:
  V_branch_ind =34*(18*v_minus +6*v_plus);
  sqrt(V_branch_ind)=2^-11.91253198=0.000259400345440246;
  Gaussian-tail estimate erfc(2^-8/sqrt(2 V_branch_ind)) ≈3.0236261e-51 (~2^-167.8221).
This is an optimistic *conditional* model, NOT a source-proved DFR; original native EP noise also contributes, and all six stage maxima cannot necessarily occur on one actual output path, so this envelope is not a precise per-slot distribution.
For comparison the original all-normal bound before additional source terms gives sqrt(34*24*v_plus)=2^-13.95618053.

Budget remaining in this conditional model:
 sigma_budget=2^-11.19460618;
 V_branch_ind/sigma_budget²≈0.3696286274;
 remaining source variance fraction≈0.63037137 or residual SD allowance sqrt(sigma_budget²−V_branch_ind)=2^-11.52746922≈0.0003387552.
The residual must pay original input, V_Pack, V_RKS, V_MS etc, plus extra/correlated noise of the new Auk. This is not a pass.
Using *additional* illustrative source-gadget RKS model with B_Rlk=2,d_Rlk=17, RKS encryption row sigma=2^-21 and V_Auto from B_Auk=2^23,d1 with row sigma=2^-53, and minimal modulus-switch rounding, yields:
  V_RKS and 12*(V_Auto+4 V_MS) added ONCE to V_branch_ind → sigma≈2^-11.6830, Gaussian tail≈2^-123.02;
  counting V_branch_ind once more as an intentionally conservative pack-input variance → sigma≈2^-11.2887 and Gaussian tail≈2^-72.52.
These are only conditional source-formula-based proxies. They do not establish whether Appendix B.4's Var(c_in) represents same VEMP and whether double charging is appropriate. Both estimates are *numerically* below 2^-64 when assumed independence holds, and neither validates real security/DFR; even a one-bit change in sigma_A is decisive in the more conservative case.
Algebraic solve of sigma_A sensitivity under these same simplifying assumptions: with once-charged branch budget, requirement sigma_A≲2^-52.364; with twice-charged branch budget, sigma_A≲2^-52.883. The hypothetical sigma_A=2^-53 barely clears the stricter requirement, underscoring lack of robust margin.

## [DERIVATION] Reused Auk_tau correlation is a precise proof blocker

Every converted K^-_{i,j} is a deterministic (given inputs) linear key-switch computation involving a SAME public KSK Auk_tau. Its row error has the schematic form
  e^-_{i,j} = tau(e^+_{i,j}) + <digits(mask'_{i,j}), e_Auk>,
where e_Auk denotes the vector of KSK-encryption errors (possibly automorphed/transformed). For two distinct derived rows a,b, covariance can have a common-key component
  Cov(e^-_a,e^-_b) = Cov(<d_a,e_Auk>,<d_b,e_Auk>) + other covariance terms,
and with independent centered Gaussian key errors of variance sigma_A² and *fixed* decomposition vectors d_a,d_b, conditional covariance is
  sigma_A² * <d_a,d_b>,
modulo polynomial multiplication/coordinate transforms and handling of secret/tag correlations. The actual d vectors are random and can be centered or not according to source gadget representation, and they can be reused across many evaluation calls. Therefore the covariance is NOT automatically zero merely because the ordinary BSK ciphertexts were sampled independently.

For centered Gaussian EP-noise variables Y_j of marginal SD sigma_j, an always sound worst-correlation second-moment upper bound is
  Var(sum_j Y_j) ≤ (sum_j sigma_j)^2
by Cauchy-Schwarz. Applied to 612 twisted and 204 ordinary EP contributions **without** justified decorrelation, this extremely loose envelope yields SD≤612*1.040824e-5 +204*2.20255e-6 ≈0.00681916, far ABOVE the 6bit decryption threshold 0.00390625; no DFR guarantee results. This bound DOES NOT prove actual failure and likely sacrifices much useful structure. Also original directly generated keys are reused; to claim the new Auk actually worsens multiquery DFR, must compare their original covariance model rather than assert perfect correlation.
For a successful new method one must prove an appropriate conditional-on-evaluation-key subgaussian/martingale concentration theorem or exact branch/output joint covariance bound in the actual gadget decomposition (digit centering, KSK row independence, shared mask reuse) and show the resulting tails alongside source key-generation/security assumptions. Gaussian tails cannot be inferred solely from marginal or unconditional variances.

## [FACT + INFERENCE] Key count/storage audit remains unresolved

Bookkeeping: original six-bit full-packed group count estimated (h+1)*6=204, with four normal +three twisted RGSW per group. If every RGSW ciphertext had 2 ordinary 2-polynomial RLWE rows, N4096,Q64,d_Bsk1, naive uncompressed total would be
 204*7*2*(2*4096*8)=187,170,816 bytes (~178.5MiB),
whereas source's Table4 reports 120.1MB "Key Sizes". This nonmatch shows our assumed full-object storage layout/duplication, compression, shared zero keys, or table inclusion semantics are NOT independently established. It is **not** evidence the author data is wrong; "Key Sizes" may count formats differently. Therefore the earlier ideal 3/7 "RGSW object count reduction" must NEVER be represented as a verified 42.9% serialized key or peak RAM reduction. First investigate actual key generator and prepared layout if the noise proof passes.
Even if 612 special keys are derived once per full batch, 2 rows per RGSW ×32 digits Auk yields 612×2×32=39,168 gadget-level constituent calls in a naive expansion; this is not author-measured online time and may be shared/FFT-hoisted. Stagewise generation/eviction and fresh independent transforms are essential to any peak-RAM gain.

## H46 decision, exact next gate, no Codex

H46 "strict source-proved 2^-64 DFR with shared Auk" remains **UNCLEAR**, not PASS, despite the conditional variance proxy satisfying the numeric Gaussian threshold. It is not cleanly killed by branch-aware arithmetic alone; P0-45's "all 816 from special" overcount was needlessly pessimistic. The identified decisive proof obstacle is **shared-key covariance and joint tail behavior** plus author's missing exact σ_Auk generation/matched dimension and memory layout. Thus:
 STATUS PASS_BRANCH_TYPED_COUNT / PASS_CONDITIONAL_NUMERIC_FEASIBILITY / UNCLEAR_FULL_DFR.
 Recommend PARK for PI/HUMAN_REVIEW if a strong proof cannot be obtained without large follow-up cost, rather than automatic costly Codex. Exactly ONE bounded next test, if PI permits P0-47, is to derive conditional covariance for two distinct RGSW rows transformed with shared Auk_tau, based on source key generation and balanced vs unsigned gadget decomp, then see whether cross terms vanish (or give a fatal nonzero floor). If source algorithm omits decomposed mask distribution, mark insufficient and request exact code/source instead of inventing. Also verify baseline author's same-key covariance assumptions; compare against new common-Auk effects. Source first before any new code.
This does NOT establish security under the additional tau automorphism eval key, direct key-size savings or publication novelty. No Codex/GPU/remote testing justified.

END_OF_ITERATION
STATUS: PASS_REAL_BRANCH_INVENTORY / PASS_CONDITIONAL_NOISE_FEASIBILITY / UNCLEAR_CORRELATION_AWARE_DFR / NOVELTY_NOT_ESTABLISHED
RESULT: 0/1/2/3 specialized EP across Algorithm2 branches, worst 18 special+6 ordinary EP per EMP; 612+204 EP path proxy in 34 full-packing EMPs; under hypothetical σA=σ+=2^-53 and independence, pre-pack sigma~2^-11.9125 and modeled DFR tiny, but conservative covariance-safe σ cap~0.00682 > decoding threshold; exact new joint-error certificate unavailable.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: P0-47 shared-Auk key-switch digit covariance proof/test on exact implementation/security model only upon PI continuation; no further generic toy tail estimates.
STATE_UPDATE: YES one isolated PURE-FHE finding; shared STATE.md and unrelated tracks unchanged.
CODEX_REQUIRED: NO.
