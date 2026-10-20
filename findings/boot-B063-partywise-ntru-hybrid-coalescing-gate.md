# BOOT-B063 Partywise grouped NTRU coalescing before hybrid conversion
DATE 2026-10-20. TRACK_ID BOOT. SHIP PAUSED.
STATUS PASS_EXACT_TYPED_TOY / FAIL_TOY_NOISE_COMPETITIVENESS / UNCLEAR_FULL_CRYPTOGRAPHIC_FEASIBILITY_AND_NOVELTY.

## Primary hypothesis
Reduce Dai et al (2026) k*l group-to-MK-RLWE hybrid conversions to k by preparing, per party, one normalized vector NTRU group output L_f(mu1) and l-1 unnormalized outputs R_f(mu2)..R_f(mul); multiplying the same-party group results via vector gadget product into one L_f(prod mu); finally run one NTRU-to-MK-RLWE hybrid conversion for that party. Avoid ungrounded same-input decomposition reuse for distinct ciphertexts. Pay l-1 extra serialized same-key NTRU products; verify correctness and noise with no new external secret-key transcript claimed.

## Source and prior art
[FACT] Dai, Xiang, Deng, Zhang: Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w . Original hybrid ExtProd performs k+1 vector NTRU external products followed by HProd(UniEnc) for d(3k+5) polynomial multiplications; k*l group outputs lead to source cost 2n/l+(3k+5)kl. One reduced-storage UniEnc per party is essential to its quoted CPA-security condition; do not silently publish more.
[PRIOR ART] Li et al TCHES2024 Faster NTRU-based Bootstrapping in less than 4 ms https://d-nb.info/1336785470/34 already has binary CMux / public X^w-1; B061–B062 ruled out novel-primitive claims for binary selector.
[PRIOR ART] Park, van Leeuwen, Zajonc FINALLY, ePrint2024/1505 https://eprint.iacr.org/2024/1505, full text via Notes p2: preprocessable hybrid-product-derived key switching exists; not shown drop-in equivalent to Dai hybrid conversion. Mirror PDF physical29 SHA256 97d2375e041c2c554f25b78cac86165928aa89ff9c3d1f045df6335bf72b5a72, version unverified.
[PRIOR ART] Li, Wen, Liang, Kong, Huang, Multi-Group Fully Homomorphic Encryption Scheme Based on LWE and NTRU, Electronics2026 15(5):940 https://doi.org/10.3390/electronics15050940, concerns joint-key participant groups rather than Dai single-party groups of secret coordinates. Related hybrid aggregation; novel relationship open.
[PRIOR ART] OpenFHE hoisting: https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/advanced-real-numbers.cpp uses decomposition of SAME input for multiple transformations; distinct group ciphertexts and successive MK-RLWE accumulators are not a shared source ciphertext. Toy h(X) vs h(X^3) differs, so naive unchanged decomp cache cannot be re-used for hidden monomial multiplications. No universal lower bound claimed.

## Typed candidate
Noiseless gadget limbs L_f(mu)_j=B^j*mu/f, R_f(mu)_j=B^j*mu. Formal exact external product satisfies L*R->L and R*R->R. Only first group of each party is L; later groups R; group-local binary monomials use known NTRU-CMux affine key reencoding. Last group includes Dai phase correction X^(-sum_j s_ij). Multiply L_f(mu1)*R_f(mu2)*...*R_f(mul)=L_f(prod mu). Conversion once per party, followed by k party conversions, yields correct formal phase. Security, source Lemma4 noise applicability for new R*R gadget ciphertexts, key distribution and all correlated error assumptions UNPROVEN.

## Reproducible toy test
Script b063_coalesce_hybrid_toy.py SHA256 0b447a19624cc6bcb737037147798dacd205ceb73504be72f09a8bed5e29b940. Exact negacyclic Z_65536[X]/(X^8+1), centered gadget B=8 or16, d=ceil(log_B Q)+1, fixed invertible short f=1+X+X² or 1-X+X², fresh primitive error each coeff uniform {-1,0,1}, sharing same bit-error samples for comparable baseline/candidate selectors. Both groups type-checked with exact modular node noise recurrence: e_out=v*e_left + sum_j digit_j(left)*e_right,j.
128 two-party noiseless plaintext-product checks and 256 typed party checks PASS; 1120 party noisy trials across 2 bases *2 f *7 settings *40 each; all exact node recurrences PASS.
Representative f=1+X+X² output RMS medians: for (g,l)=(2,2),(4,2),(4,4),(8,4), base8 coalesced/individual-group-max RMS median ratios 7.85, 8.07, 15.72, 16.76; base16 ratios 12.56, 13.88, 27.63, 30.85. Second f displays same qualitative worsening. These comparisons are against B062 binary-CMux individual normalized group outputs, NOT source-original GIPEval and NOT final MK-RLWE noise/DFR. No actual HybridProduct implementation. Other unresolved security/correlation hypotheses cannot be silently assumed.

## Ideal cost
With beta=(3k+5)k and l|n, ideal conditional online depth: Dai T=2n/l+beta*l; B062 grouped CMux T=n/l+beta*l; candidate partywise coalescing T=n/l+(l-1)+beta. Ignores extra public affine operations, actual polynomial cost/memory, noise-induced modulus/key expansion and security. n512 k4 optimized symbolic costs 528 / 392 / 115; n1024 k8: 1440 / 976 / 295. These are not runtime acceleration ratios.

## Decision
PASS typed candidate math and noisy toy recurrence. FAIL low-noise expectation in tested regime: naive full coalescing severely increases residual noise vs per-group outputs. Complete hybrid noise/DFR/cost proof and prior-art differentiation remain UNCLEAR, so no publication claim.
NEXT_TEST B064: One noise-aware limited-block h=2 coalescing, contrasted with h=1 baseline and h=l fully coalesced under source Lemma3 and genuine security/noise cost. Stop if no parameter regime survives.
STATE_UPDATE NO: original findings/boot-STATE.md still not safely readable (GitHub Notes read_repo_file returns empty object). Do not overwrite 187967-byte state file. Append-only B063 saved. SHIP unchanged.
LOCAL ARTIFACT full report, Python script, raw logs and JSON: BOOT_B063_handoff.zip.