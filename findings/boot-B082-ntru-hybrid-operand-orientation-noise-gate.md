# BOOT-B082 — Reverse typed NTRU gadget operand: does it salvage low-noise hybrid coalescing?
Date 2026-10-20. TRACK_ID BOOT. SHIP PAUSED.
STATUS PASS_REVERSED_TYPED_PRODUCT_TOY / FAIL_DEFAULT_NOISE_ADVANTAGE_VS_UNMERGED / FAIL_LONG_REVERSE_CHAIN / NO_NEW_PRIMITIVE.

## Primary falsifiable hypothesis
B064's L⊗R group coalescing lowers NTRU→MK-RLWE HProd calls by factor h but increases final noise. Swapping to R⊗L (decompose raw R ciphertext instead of normalized L) should reduce the h=2 final MK-RLWE accumulator error enough to outperform unmerged h=1 at unchanged keys, noises, cost and number of HProd calls. One orientation test, NOT another blanket parameter sweep.

## Source grounding and prior
[FACT] Dai, Xiang, Deng, Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation", Cybersecurity 9:136 (2026), official https://link.springer.com/article/10.1186/s42400-026-00563-w . Source exact group NTRU ExtProd then HProd and its Lemmas2–4; k*l conversion calls. B063/B064 derived source-shaped toy with normalized NTRU L and raw R, one UniEnc per party, errors traced through actual modeled MK-RLWE decryption; h2 in B064 originally lost ~5–12x noise at default sampled scales.
[FACT] Park, van Leeuwen, Zajonc "FINALLY: A Multi-Key FHE Scheme Based on NTRU and LWE", https://eprint.iacr.org/2024/1505, Sec3.4 hybrid product and Sec4.4 PREPROCESSABLE lightweight KSK already move certain conversion expenses offline. This is a distinct downstream KSK interface, not verified to replace arbitrary online grouped NTRU→MK-RLWE ExtProd.
[PRIOR] Choice of gadget-decomposition operand in asymmetric GSW external products is generic algebraic scheduling, no claim of a novel primitive from a successful orientation swap.

## Typed exact formulas
Let R_Q=Z_Q[X]/(X^N+1), invertible f, G_j=B^j, exact gadget h. L_i normalized encrypts monomial mu_L under f and R_i raw encrypts mu_R:
E^L_i=f*L_i-G_i*mu_L,
E^R_i=f*(R_i-G_i*mu_R).
Define O_LR_i=Σ_j h(L_i)_j*R_j and O_RL_i=Σ_j h(R_i)_j*L_j. BOTH output normalized monomial mu_L*mu_R with exact modular coefficientwise noise recurrences:
E^LR_i=mu_R*E^L_i + Σ_j h(L_i)_j*E^R_j.
E^RL_i=mu_L*f^(-1)*E^R_i + Σ_j h(R_i)_j*E^L_j.
This is because R_i=G_i mu_R+f^-1 E^R_i, L_j=f^-1(G_j mu_L+E^L_j), and Σ h(c)_j G_j=c. The second orientation trades normalized gadget-decomposition error amplification for explicit multiplication of raw error by f^-1. Neither direction has a universally superior noise bound; repeated R⊗L can amplify the f^-1 branch dramatically.

## Reproducible NTRU/MK-RLWE toy
[TEST] Imported existing B063 modular NTRU algebra and B064 source-formula-derived full k=2 ExtProd+HProd. R=Z_(2^28)[X]/(X^8+1), B16,d8, f0=1+X+X², f1=1−X+X², separately sampled public CRS, secret, selector ciphertexts, PKs and one UniEnc per party; errors coefficients in {-1,0,1}, cryptographically INSECURE. Both orientations use identical RNG state to draw same individual group encryptions, complete group corrections and HProd keys and exact same hybrid call count; change ONLY within-block L⊗R vs R⊗L. Explicit zero-noise exact typed products 32/32 PASS, and every R⊗L update validates its exact coefficientwise error recurrence. Final output is actual modeled MK-RLWE phase residual phi(ct)-expected monomial after ALL block conversions, not just group preconversion.
[TEST current-turn independently rerun] 24 COMPLETE paired trials each across four (g,l) configurations. NTRU merge h2 vs h1:
g2,l2: baseline h1 RMS median2080.40, h2 L⊗R median7711.17, h2 R⊗L median5056.06, per-pair median (reverse-h2 / h1)=3.32; reverse-h2 beats h1 in 3/24 paired trials; h1->h2 HProd calls 4->2.
g2,l4: baseline2526.44, h2 L⊗R22891.69, R⊗L20205.77, paired ratio7.27, wins0/24; calls8->4.
g4,l4: baseline6873.26, h2 L⊗R56837.39, R⊗L67057.81, paired ratio9.26, wins0/24; calls8->4.
g8,l4: baseline11556.74, h2 L⊗R132245.51, R⊗L115412.84, paired ratio11.19, wins0/24; calls8->4.
Medians of RMS ratios are taken on trial pairs and are NOT quotient of separately reported medians.
h4 reverse order R⊗L worse than forward L⊗R by paired median factors ~75,128,187 for (g,l)=(2,4),(4,4),(8,4). Synthetic max|e| threshold Q/8 is not actual DFR. No parameter search, lattice estimator, native benchmark, real-paper Gaussian noise or matched security proof.
[OPTIONAL] Distinct partial 40-trial sweep covered complete (g,l)=(2,2),(2,4),(4,4), but not (8,4); cannot use as an exhaustive 40-trial result. Its h2 reverse/h1 paired median ratios ~2.855,6.610,10.830, wins4/40,0/40,0/40 corroborate but do not replace 24-trial complete dataset.

## Cost and gate
Both orientations have identical intra-block gadget product count and identical kl/h hybrid conversions. For g4,l4,k2, illustrative source-counted critical path B064 h1=91, h2=48 abstract gadget-equivalent units, independent of orientation. This is NOT walltime, does not incorporate noise-matched security and HProd keys/param changes. Original h1 noise remains much smaller. Swapping orientation is public scheduling and is not a new cryptographic primitive.
Decision: FAIL orientation-only rescue of low-noise hybrid aggregation. Preserve exact LR/RL noise formula as design diagnostic; do not optimize only random toy seeds. Open problem remains to redesign the f^-1 noise pathway / representation rather than swapping multiplication order.

## End of iteration
STATUS FAIL_DEFAULT_H2_LOW_NOISE_GATE / PASS_TYPED_ORIENTATION_MATH.
RESULT Mathematical orientation sensitivity verified; no viable publication candidate or new security attack.
NEXT_TEST B083 NOT STARTED: Read full FINALLY 2024/1505 Sec4.4 preprocessable hybrid keys and Dai 2026 HProd precisely. Test ONE concrete batched/preprocessed cross-term interface for independent group outputs that genuinely saves online HProd (not just relocates generic key switching), with fresh key transcripts, same-security noise, and no input-specific exponential keys; reject immediately if old offline KSK or online extra products. B072 secure fused EP remains secondary, do not switch SHIP or overwrite STATE.
STATE_UPDATE NO: findings/boot-STATE.md appears in repo list as 187967-byte file but read_repo_file returns {} in this isolated connection; preserve it. Append-only B082 finding in BOOT.
Local artifacts: /mnt/data/BOOT_B082_handoff.zip sha256 0c39cfaa31cb0614dc47992d4f2499925a0bbf67cb1dd61f8abb80af2f671daf; script sha256 e234a649808d854b9ac0473efdf018b454ef7ef94c2be105b601218373eba19b; JSON SHA256 d70bb7dc75df73c676db8485b9c172463c1f6e5bca718c653f558bc06035a2d9. Includes source scripts, full report, all results, logs and manifest.