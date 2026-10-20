# BOOT-B064 — Partial NTRU group coalescing: full hybrid noise gate
DATE: 2026-10-20
TRACK_ID: BOOT; SHIP PAUSED.
STATUS: PASS_SOURCE_FORMULA_TOY_HYBRID / FAIL_DEFAULT_NOISE_GATE / UNCLEAR_REAL_SECURITY_MATCHED_REGIME_AND_NOVELTY.

## One primary hypothesis
For Dai et al. (2026) grouped MKFHE, merge h=2 adjacent NTRU inner-product groups before applying each NTRU-to-MK-RLWE ExtProd/HProd; reducing calls k*l to k*l/2 might outweigh extra merged NTRU error when measuring FINAL MK-RLWE accumulator noise under matched source-shaped toy distributions. Compare to h=1 original grouping and h=l full coalescing; do not just compare pre-hybrid vector noise.

## Sources
[FACT] Dai, Xiang, Deng, Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation," Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w ; accessible Springer HTML, Improved hybrid product, External product for hybrid ciphertext, Lemmas 2-4, App. proof Lemma3.
HProd formulas with gadget h(c) and one UniEnc per party: pk_j=-s_j*a_com+e_pk_j (j>=1), implicit pk_0=-a_com for s0=1 (algebraically derived in our check); d0=r*a_com+f*G+e0; d1=-s_i*b_com+r*G+e1. v=sum_j<h(c_j),pk_j>, u_j=<h(c_j),d0>, out_0=u_0+<h(v),d1>, out_i=u_i+<h(v),b_com>. Dai Lemma2 hybrid noise H=(k/2)||f||²N² Var(e_uec)+gamma Var(e_pk); Lemma3 σ_exp²=N/2(Var(e)+gamma Var(gct))+H, only under its noise assumptions. CPA condition: publish only one UniEnc per party.
[PRIOR] FINALLY Park et al ePrint2024/1505 preprocesses hybrid-product-derived key switching, not a proven substitution here; Li et al TCHES2024 NTRU CMux binary selectors already known. B059-B062 bit selector not novel.

## Construction and cost
At each participant i and h|l, within each block of h groups generate first group's normalized NTRU vector L_f and all later groups raw R_f, multiply h-1 times via typed L*R->L, preserve final group correction X^(-sum_j s_ij). One ExtProd+HProd for each merged block, reusing one UniEnc per party. Intermediate raw R*R inside raw groups is our unproven extension and changes key transcript.
Conditional critical-path cost: T_h=(g-1)+(h-1)+(3k+5)k(l/h), g=n/l, excludes secure parameter changes, public affine ops, memory, real hardware. For g4,l4,k2: h1=91 h2=48 h4=28 abstract units. NOT timing.

## Exact source-formula-derived toy implementation
[TEST] Script b064_partial_merge_hybrid_toy.py SHA256 90fbaa7b0230933e15872e9a33eb0a2a55dcbdbf9359040549fdc175bf6e1cd3, depends on previous b063_coalesce_hybrid_toy.py (bundled local handoff). Ring Z_(2^28)[X]/(X^8+1), B16,d8,k2,f0=1+X+X²,f1=1-X+X², RLWE toy secrets 1±X²±X^5, uniform public CRS a,b, one UniEnc per party and public keys; primitive error coefficients independently uniform -1,0,1 unless artificial UniEnc scaling explicitly noted. Precise signed gadget decomposition, modular ring multiplications, scalar NTRU ext products, full HProd exactly per formula; decryption phi(ct)=ct0+Σctj*sj tracked at every intermediate and at final output. Same leaf errors, CRS, PK, UniEnc between h strategies. 36/36 noiseless ExtProd+HProd checks PASS including nonzero ct1,ct2; full zero-noise phase and exact center-Q noise measured.
[TEST] 40 paired trials EACH (g,l)=(2,2),(2,4),(4,4),(8,4), multiplier1:
 (g2,l2) h1 median final RMS 1753.24 h2 8961.33, paired median ratio5.36;
 (g2,l4) 2371.85 vs23965.89, paired ratio8.67, h4 median19498.58;
 (g4,l4) 6288.97 vs55042.15, paired ratio9.71, h4 median54105.29;
 (g8,l4) 10639.72 vs115199.05, paired ratio11.85, h4 median120428.03.
No Q/8 *synthetic* coefficient threshold exceeded in default tests; threshold is not a real DFR. Result is tiny toy, not native authors' OpenFHE or real secure parameters, input GIP is B059/B062 CMux not Dai automorphism baseline.

## Sensitivity gate and caveats
[TEST] Artificially scale ONLY UniEnc error amplitudes σmult in {1,100,400}, with all other random primitive draws matching. g4,l4, 20 pairs each, final-MK-RLWE paired median ratios h2/h1: 8.81,3.50,0.927, with h2 lower than h1 in 0/20,0/20,11/20. h4/h1 paired ratio:9.11,3.47,0.810, with h4 lower in 0/20,2/20,14/20.
[TEST] Two schedule orders, 12 paired samples for g4,l4, scaled UniEnc error400: block-major h2/h1 1.130 (5/12 better) and party-major 1.244 (4/12 better). At unit error scale both orders clearly worse for h2 (ratios13.70 and8.81). Thus the apparent high-σ noise improvement is NOT robust evidence of a useful secure regime.
[DERIVATION] Very conditional source-Lemma3 independent-call proxy W_h≈(l/h){N/2[E+gamma V_h]+H}, H defined above. h2 improves h1 only if H > (N/2){gamma(V2-2V1)-E}. The real reused UniEnc creates cross-call correlations and E changes with intermediate MK-RLWE ciphertext; this is NOT a certified bound.

## Decision
At normal tested primitive noise, partially merged h2 **FAILS** final accumulator noise gate despite ideal 8->4 HProd count. An artificial noise-dominated crossover is conceivable but unstable and does NOT establish a secure DFR/runtime gain or novel primitive. **Do not promote h2 nor claim broad impossibility.**
STATUS=PASS_TOY_FULL_HYBRID / FAIL_DEFAULT_NOISE / UNCLEAR_REAL_PARAMETER_NOISE_AND_NOVELTY.
NEXT_TEST B065 NOT STARTED: read published concrete N,Q,B,d,gamma,sigma_G,sigma_uec,sigma_pk and security/DFR estimates, independently check whether h2 crossover is reachable under matched 128-bit security and native cost. If no realistic regime, archive group coalescing. Consider alternative designs that remove Hybrid Product without forcing noisy raw group products.
STATE_UPDATE NO: existing findings/boot-STATE.md is 187967B and read_repo_file returns {}, so do not overwrite. Append-only new B064 findings file, no cross-track writes.
LOCAL: BOOT_B064_handoff.zip with full >9KB study, scripts, raw JSON, logs, B063 dependency.