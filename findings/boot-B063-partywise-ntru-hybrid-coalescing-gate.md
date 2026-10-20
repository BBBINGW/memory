# BOOT-B063 — Partywise coalescing grouped NTRU outputs before hybrid conversion

Date: 2026-10-20. TRACK_ID BOOT. SHIP remains PAUSED.
STATUS: PASS_EXACT_TYPED_TOY / PASS_NOISY_GADGET_RECURRENCE / FAIL_TOY_LOW_NOISE_EXPECTATION / UNCLEAR_SECURITY_DFR_NATIVE_SPEED_NOVELTY.

## One falsifiable hypothesis
Dai et al. 2026 perform k*l separate hybrid NTRU-to-MK-RLWE conversions after k*l parallel grouped inner products. Instead retain one normalized NTRU group per participant i, generate other group outputs in raw NTRU representation, coalesce same-party outputs by the typed gadget product before a **single** NTRU-to-MK-RLWE conversion per participant. Test whether k*l -> k costly cross-key conversions can occur algebraically without unacceptable added noise. This is a group-aggregation algorithm candidate, **not** free hoisting of independent inputs.

## Verified source
[FACT] Yiran Dai, Binwu Xiang, Yi Deng, Jiang Zhang, Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w , authoritative PDF physical pp 7-8 and online Algorithms 2,3. Their ExtProd takes k+1 vector NTRU/MK-RLWE component gadget products, then a Hybrid Product with 2k+4 gadget products: (3k+5) per conversion in gadget-equivalent units; k*l such calls after grouped GIP. The paper's cost model T(l)=2n/l+(3k+5)kl. Hybrid HProd uses h(c_j) in v=sum<h(c_j),pk_j> and u_j=<h(c_j),d_i0>, so **within the same invocation** the digit decomposition can already be shared; successive updated accumulators differ. The source's 2-CRS UniEnc assumes one UniEnc per party for CPA security. Preserve it.
[PRIOR ART] Li et al., Faster NTRU-based Bootstrapping in Less Than 4 ms, TCHES 2024(3), https://d-nb.info/1336785470/34 , NTRU CMux and binary selector preexisting. Park, van Leeuwen and Zajonc, FINALLY: A Multi-Key FHE Scheme Based on NTRU and LWE, ePrint 2024/1505, p2 and section4.4, https://eprint.iacr.org/2024/1505 , amortizes some hybrid-product work via preprocessable key switching: distinct interface, but mandatory novelty comparator. Li et al 2026 MGHE group partitions parties, whereas Dai's groups are LWE secret coordinate blocks; do not conflate.

## Explicit typed construction
Let R_Q=Z_Q[X]/(X^N+1), secret f invertible, gadget G=(B^j). Abstract noiseless normalized L_f(mu)_j=B^j*mu/f; raw R_f(mu)_j=B^j*mu. For each participant i, produce its first group's monomial mu_i0 under L and remaining group monomials under R. Use candidate typed products L*R->L, R*R->R, to obtain A_i=L_f(product_m mu_im) before performing original ExtProd once for this party and combining across parties. Preserve the original last-group correction X^(-sum s_ij). Produce raw group factors with known binary-selector identity X^(w*s)=1+(X^w-1)s; this is existing CMux and does NOT establish novelty. The source formally proves L*R noise, **not** this R*R extension.

## Exact paired toy audit
[TEST] Reproducible Python file b063_coalesce_hybrid_toy.py SHA256 0b447a19624cc6bcb737037147798dacd205ceb73504be72f09a8bed5e29b940; ring N8, Q=2^16, signed centered digit base B=8 or B=16, d=ceil(log_B Q)+1, two invertible short f=1+X+X^2 and 1-X+X^2, per-limb independent primitive errors uniformly in {-1,0,1}. Original normalized group and candidate normalized/raw grouped inputs reuse corresponding per-bit error samples. Exact per-node modular noise recurrence is verified for both L*R and the candidate R*R:
 e_out,j = v*e_left,j + sum_h gadget_digit_h(C_left,j)*e_right,h (mod Q).
Group parameter configurations: (g,l)=(2,1),(2,2),(2,4),(4,2),(4,4),(8,2),(8,4), 40 trials for each combination of B in {8,16} and f in two options. Total 1120 individual noisy party runs. Separately 128 noiseless two-party aggregate plaintext-product cases and 256 party normalized/raw type and final group correction cases PASS. Hoist check h(X) != h(X^3) for distinct secret monomials PASS.

[RESULT] f=1+X+X² representative median max baseline individual normalized GROUP noise RMS vs candidate merged PARTY noise RMS:
 B8 g2 l2: 10.15 vs79.66 (7.85x); g4 l2: 19.19 vs154.91 (8.07x); g4 l4:19.54 vs307.10 (15.72x); g8 l4:31.96 vs535.79 (16.76x).
 B16 g2 l2: 15.21 vs191.11 (12.56x); g4 l2:30.85 vs428.03 (13.88x); g4 l4:35.03 vs967.96 (27.63x); g8 l4:56.52 vs1743.42 (30.85x).
 Second f shows comparable trends. Full logs and JSON supplied in local BOOT_B063_handoff.zip. Both B8 and B16 scripts have been independently rerun and output logs exactly match stored evidence (diff -q reports no differences).
IMPORTANT: Baseline is **each individual normalized group**, not a completed source MK-RLWE bootstrap after kl ExtProd. Ratios do NOT equal real final noise ratios or DFR. No synthetic Q/8 threshold crossings (NOT a true decryption correctness estimate). No native OpenFHE run.

## Conditional cost and gates
beta(k)=(3k+5)k. Published ideal model T_Dai(l)=2n/l+beta*l; B062 serial-CMux abstract T_CMux(l)=n/l+beta*l; candidate coalesced T_COAL(l)=n/l+(l-1)+beta, excluding all public affine ops, key/key-generation, actual ring/gadget cost differences, noise-parameter increase, hardware and hybrid conversion cost. Optimal l restricted to divisors n. Examples: n512 k4 Dai528 (l4), B062 CMux392(l2), coalesced115(l16); n1024 k8 Dai1440(l4), B062 CMux976(l2), coalesced295(l32). These are conditional gadget-equivalent cost models, NOT native performance.
Noise risk: l-1 extra gadget products use raw group outputs as noisy right operands; heuristic Var_out <= Var_left+gamma Var_right can greatly magnify accumulated noise. Since original scheme does multiple hybrid products, real final comparison MUST include their noise and correlations and precise matched security parameters. The extra change of raw group encoding, reuse of unit encryption, circular/KDM security and security of one UniEnc must be audited. Key transcript and native DFR have NOT been proven.
Prior art: grouping and pre-hybrid coalescing can be regarded as elementary schedule changes; FINALLY's offline preprocessable hybrid idea must be compared. No claim of a novel secure cryptographic primitive.

## End iteration
STATUS PASS_EXACT_TYPED_TOY / FAIL_TOY_LOW_NOISE_EXPECTATION / UNCLEAR_FULL_FHE_VIABILITY_AND_NOVELTY.
RESULT Ideal k*l to k conversion algebra exists, and exact small-parameter typed tests pass; source-shaped toy finds serious pre-hybrid NTRU noise amplification. No claim of end-to-end improvement.
NEXT_TEST B064 (NOT STARTED): ONE partial coalescing/block-size=2 group merge with complete matched hybrid noise model compared with h=1 direct and h=l full coalescing; include noise from each source ExtProd and HProd, not merely raw group RMS. If no favorable matched noise/cost regime, archive.
STATE_UPDATE NO: existing findings/boot-STATE.md (187967 bytes) returns {} from GitHub Notes read_repo_file; preserve original. Only append-only B063 findings update, no modifications to other tracks.
