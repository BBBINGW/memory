# PURE-FHE · P0-PRESCOUT-45 — Twisted RGSW on-demand derivation: native BatchBoot gadget-noise and DFR-budget kill gate

DATE: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
PREVIOUS: P0-PRESCOUT-44, findings/pure-fhe-p0-44-batchboot-twisted-rgsw-on-demand-key-derivation-gate-2026-10-27.md, commit 8a0c7912dbbf01845a233e7c2070640cc5dc3c63.
LATEST_COMPLETED: P0-PRESCOUT-45
NEXT_ITERATION: P0-PRESCOUT-46 NOT_STARTED; conditional PI approval and nontrivial novel mechanism required
STATUS: FAIL_UNMODIFIED_AUK_PARAMETERS_DFR_CERTIFICATE / PASS_SYMBOLIC_NOISE_BUDGET / RETUNED_KSK_PARETO_UNCLEAR
NOVELTY: NOT_ESTABLISHED (standard automorphism and RLWE key switch)
CODEX_REQUIRED: NO. No native CPU/GPU experiments, remote actions, new code, binary downloads or infrastructure writes.
STATE_UPDATE: YES one isolated PURE-FHE finding only, do not touch global STATE.md/other BOOT/SHIP/CGS/VFHE/EAI lines.

## ONE primary falsifiable H45

Given previous P0-44 ideal-plaintext identity K^-_s(u)=KS_{tau(s)→s}(tau(K^+_s(u))) for scalar one-hot u, can replacing native special RGSW keys with lazily generated twisted keys, using source BatchBoot Boot6's *unchanged* RLWE automorphism-key gadget parameters B_Auk=2^23,d_Auk=1, retain the paper's noise-variance and DFR=2^-64 certificate for six-bit message packing? Cheapest test: substitute into original author B.2–B.3,C.2–C.4 noise bound and Gaussian DFR equation, with explicitly declared normalization and provenance of any approximated σ_Auk. Avoid treating a theorem's upper bound as a measured lower bound or ignoring correlated reused key noises.

## [FACT] Direct FIRST-PARTY primary source

Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026 original official 20-page prepublication PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf. Inspected original page-aware web PDF plus SCREENSHOTS physical 6,7,8,12,18,19,20 (zero-index 5,6,7,11,17,18,19). Original §4.1 Table1/Eqs7–9 physical p6: normal RGSW_s(u) and twisted RGSW_s^tau(u) require different secret-related first-row messages; §4.2 Alg2 physical p7 4 external products per 2-bit pair stage; Alg3 p8 h+1 EMPmul stages plus Repack/Auk and Rlk. Appendix B.2–B.3 p17; Appendix C.2 p18; C.4/D.1 p20; Table4 p12 directly verified.
- Parameter set Boot6: p=2^6, n=2^12=4096, h=33, N=2^12=4096, Q=2^64 (in Table9), B_Bsk=2^23,d_Bsk=1, B_Auk=2^23,d_Auk=1, B_Rlk=2,d_Rlk=17. Single-thread full-pack source nominal 6-bit DFR 2^-64, 4096 msgs, Table4 8.43ms/message and printed Key Sizes120.1MB (not a verified complete peak-RAM or BSK-only breakout), measured full-process peak RAM1425MB Table13.
- Table9 Boot6 has TWO parameter rows: h=33,N=4096,Std=2^-21 and h=512,N=2048,Std=2^-53, both Q=2^64 and reported >128-bit lattice-estimator security. Important: the second row DOES NOT alone establish that the proposed extra direct Auk_tau at ring N4096 has σ=2^-53. We use σ_Auk=σ_native_BSK=2^-53 below as a FAVORABLE MODELING ASSUMPTION, not a source-certified exact key allocation. Source did not list a -1 automorphism key among its repacking Auk_i; adding it is a separate secret-dependent evaluation-key security obligation.
- Author Appendix B.2 (after restoring scale in integer modulus Q) gives V_GP ≤ (B²/12)dN Var(key row) + N/12 ceil(Q/B^d)²; V_EP ≤ (B²/6)dN Var(RGSW row) + N/12 ceil(Q/B^d)². Appendix B.3 says KS output noise is GP variance. C.2 Lemma4.1 V_EMP < Var(cin)+2ell V_EP for ell=log2 n, and Lemma4.2 V_Boot < (h+1) V_EMP+V_Pack+V_RKS (under fresh authors' keys and noise assumptions). C.4 assumes a Gaussian approximation and P(|e|>Q/2^(p+2))=erfc((Q/2^(p+2))/(sqrt2 StdM)); StdM=sqrt(V_Boot+V_MS). Actual DFR not verified after derived keys.
- Source authors assume additive noise and independently-generated keys; after deriving many RGSW rows from the SAME Auk_tau, independent-noise addition is a further UNPROVEN assumption. Any existing certificate cannot be copied without conditioning on shared evaluation-key noise.

## [DERIVATION] Normalize torus scale and compute unchanged-parameter KS error scale

For Q=2^64, normalize variances by Q². Let σ_A be normalized per-row KSK encryptor noise and σ_+ native BSK row noise. Under the source's GP/KS noise model, proposed freshly derived row has model upper-budget:
  v_der ≲ σ_+² + (B_A² d_A N/12) σ_A² + (N/12)(ceil(Q/B_A^d_A)/Q)².
This is a variance model/certificate accounting, not a proven lower bound on every actual row or deterministic ciphertext. Actual correlated shared KS errors could be worse than its naive independent additive use.

For source unchanged B_A=2^23,d_A=1,N=4096,Q=2^64:
  σ_KS,trunc = sqrt(N/12)*(Q/B_A)/Q
             = sqrt(4096/12)*2^-23 ≈ 2^-18.7923932.
This term is INDEPENDENT of assuming σ_A as tiny as 2^-53. Since the mask components of RGSW' are (pseudo)uniform, losing the low 41 bits of a uniform 64-bit mask by one-digit gadget truncation induces a huge *model* row error relative to original σ_+=2^-53. This fails to certify that derived special RGSW can be fed into normal EMP with the original DFR proof.

Even if we retain the SAME base B_A=2^23 but increase digits d_A=3 (enough to cover 64 bits), the truncation term falls to sigma ≈2^-59.792 (ceil(Q/B_A^3)=1), BUT the input KSK error term then dominates at
  σ_KS,encrypt = (B_A sqrt(d_A N/12)) * 2^-53 ≈ 2^-25.000.
This is still disastrously larger than freshly generated special RGSW row noise and DOES NOT fix the unchanged-base problem. This is a distinct precision and key-noise obstruction, not just lack of enough gadget digits.

## [DERIVATION + TOY_NUMERIC] Source EP amplification and DFR ceiling

Use original EP formula with B_B=2^23,d_B=1,N=4096:
  A_EP = B_B² d_B N/6 = 2^55.415037499... .
  R_EP = N/12*(ceil(Q/B_B^d_B)/Q)² ≈ 2^-37.584962501.
  V_EP(v) ≲ A_EP*v + R_EP.
If native σ_+=2^-53, source-structured EP std from above is ≈2^-18.7924 and the theoretical (h+1)*2ell=34*24=816 EP-variance accumulation proxy std ≈2^-13.9562 excluding packing, final RKS, modswitch and input noise. In other words even native EP is already mostly gadget truncation; author's DFR budget also has other components.

At p=6, normalized failure threshold t=Q/2^(p+2)/Q=1/256=2^-8. For the stated Gaussian-tail MODEL to have P_fail≤2^-64, the aggregate normalized σ_M must be no larger than
  σ_budget = (2^-8)/(sqrt2 * erfcinv(2^-64))
           ≈0.000426665719=2^-11.19460618
with corresponding normal z=9.15529377.
If, hypothetically, ALL 816 EP contributions are charged at the same derived-row v and all other error sources vanish (an intentionally optimistic but also all-EP-replaced accounting assumption), enforcing this conservative certificate gives an allowed derived-row normalized σ of at most ≈2^-43.75419. **Important**: this all-816 identical-derived model is NOT the actual branch pattern; source four EPs per branch contain both original and derived keys, and extra memory/packing terms are nonzero. Therefore 2^-43.75 is NOT a theorem of minimal necessary noise for the real modified algorithm. It is a convenient consistent envelope to reject a parameter set whose bound is off by many orders of magnitude. A true branch-typed key-noise calculation is necessary for borderline retuned cases.

Under FAVORABLE ILLUSTRATIVE per-row σ_A=σ_+=2^-53, with d_A=ceil(64/b), N=4096 and Q=2^64, execute high-precision mpmath deterministic arithmetic of the above SOURCE-derived noise accounting:

  b=23,d=1 (source unchanged): KS σ_model=2^-18.79; resulting single EP σ_model=2^8.92 (far outside small-error/torus Gaussian regime; DO NOT interpret Gaussian failure probability numerically).
  b=23,d=3: KS σ_model=2^-25.00; single EP σ_model=2^2.71, again outside small-error regime.
  b=8,d=8: KS σ_model=2^-39.29, 816-EP proxy σ=2^-6.75 (>2^-11.19).
  b=4,d=16: KS σ_model=2^-42.79, 816-EP proxy σ=2^-10.24 (>budget).
  b=3,d=22: KS σ_model=2^-43.56, 816-EP proxy σ=2^-11.01 (>budget).
  b=2,d=32: KS σ_model=2^-44.29, 816-EP proxy σ=2^-11.72 (<budget ONLY if zero other terms AND same branches as proxy; actual source RKS/Pack/MS and repeated Auk correlations unaccounted).
  b=1,d=64: KS σ_model=2^-44.79, 816-EP proxy σ=2^-12.18 (<budget in same artificial zero-other-terms proxy).
The all-816 output SD proxy is not meaningful as a physical exact Gaussian if ≥1 torus unit; use only to show catastrophic lack of certificate. None of these figures are actual native execution measurements nor claims of 128-bit IND-CPA-D security.

In the ACTUAL Alg2 each two-bit stage uses four EPs but mixes ordinary and τ-twisted RGSW according to output index; a reliable P0 continuation must propagate separate V_EP^+ and V_EP^- by each branch and stage, not set all 816 contributions to V_EP^- just to gain an unjustified tight result. In addition, reuse of one Auk_tau makes terms dependent. With σ_budget already close to author-predicted DFR, a borderline b2,d32 calculation above is NOT a PASS.

## [DERIVATION] More accurate extra-key memory and online duty

Reducing persistent BSK from 4 plus 3 special to 4 ordinary RGSW per group would save up to 3/7 nominal key OBJECTS if they are physically independent/equal-size and present; this is NOT a 42.9% RAM saving. Boot6 full batch has roughly (h+1)*(log2n/2)=34*6=204 selector groups and 3 special keys each (=612 special RGSW groups), but actual stored/prepared layout remains unverified. To retune the proposed *new* τ_-1 Auk key from d=1 to d=32 (base4), single such evaluation key gadget ciphertext grows about 32-fold compared with ONE d=1 Auk at equal N/Q; it is not the entire evaluation-key memory growing32x. Each derived K^- requires key switching each of its RLWE' rows (2*d_B rows). In Boot6 d_B=1, a crude one-batch count is 612*2*32=39,168 gadget-multiplication constituent calls for materialization, plus FFT/preparing and public permutes. This is BEFORE benchmarking cost per operation and assumes only one-time key materialization for each group, reused by all 4096 samples in its stage. Stage-wise eviction and required repeat derivations need an explicit key lifetime model.
The existing paper does not provide Bsk+/Bsk-/Auk separate byte counts, and Table4 "Key Sizes"120.1MB plus Table13 peak RAM1425MB cannot be converted into claimed new RAM savings.
Also NEW Auk_-1 security cannot simply inherit that of published Auk indices: one more key-dependent RLWE encrypting τ_-1(s) can change circular/KDM assumptions.

## Conclusion and strict next gate

H45 FAILS for **unchanged source Auk gadget parameters**: source-derived additive noise upper-accounting is orders of magnitude outside the ordinary special-RGSW noise regime and will NOT certify 6-bit 2^-64 DFR. Simply increasing digits while retaining base2^23 also does NOT repair the issue, as key encryption noise is amplified by B. This is NOT a formal general lower bound or proof of actual failure on every ciphertext.
A DIFFERENT retuned key B_A=2^2,d_A=32 (or B_A=2,d_A=64) might reduce the modeled derived-row noise sufficiently to re-enter budget on an unrealistic zero-other-terms proxy, but actual source baseline already has packing/KS/MS error and key correlations. Retuning adds key bytes, offline/on-demand time and security obligations. Its originality remains NOT_ESTABLISHED. Do not equate any such "plausible numeric" with a cryptographic construction.

End of Iteration:
STATUS: FAIL_UNCHANGED_AUK_GADGET_6BIT_DFR_CERTIFICATION / RETUNED_VARIANT_NOT_CERTIFIED / NOVELTY_NOT_ESTABLISHED
RESULT: source Boot6 B_Auk2^23,d1 gives truncation σ≈2^-18.79 normalized per derived row; changing only d=3 retains amplified KSK σ≈2^-25. Strict 2^-64 single-Gaussian output target σ_budget≈2^-11.19, while BSK EP amplification A≈2^55.415. Retuned low bases need separate full branch/noise/cost/security proof.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: HUMAN_REVIEW before P0-46. If and only if pursuing this ONE surviving variant, do exact Alg2 output-index-aware plus reused-Auk correlation-aware covariance or valid worst-case bound with b=2,d=32 and original full V_pack+V_RKS+V_MS, then determine noise budget. Falsify on full cost before requesting Codex. Otherwise PARK candidate and leave PURE-FHE in stagnation.
STATE_UPDATE: YES, this single isolated finding only; do not change global STATE.md or other research tracks.
CODEX_REQUIRED: NO.
