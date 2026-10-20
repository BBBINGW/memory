# BOOT-B085 — Fused AP external product, uniform-mask noise and short-gadget capacity
Date 2026-10-20 | TRACK_ID BOOT ONLY | SHIP PAUSED
STATUS: PASS_AP_FUSED_PHASE_IDENTITY / FAIL_EXACT_ONE_ROW_SHORT_DECOMPOSITION / PASS_KNOWN_APPROXIMATE_GADGET / FAIL_NEW_PRIMITIVE

## Primary falsifiable hypothesis
Can a fixed short-coefficient, one-row publicly computable mask decomposition preserve exact automorphism-parametrized fused external-product functionality for every full-support uniform GLWE input mask, keep low noise, and avoid the usual multirow GLev/AP-GGSW key? B072 had already found direct one-row fusion to have massive mask-times-error noise and that forcing secret-dependent mask correlations risks leakage. This iteration chooses one smallest counterexample and its known repair; no new noise hyperparameter sweep.

## Original sources and prior-art status
[FACT] Bernard–Joye, "Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys", ePrint 2025/163 https://eprint.iacr.org/2025/163 ; mirror PDF sha256 ce81021fca19132729765ad652a2f4a8f1d27d6b9c7f084777b6386fa5e08387, VERSION_UNVERIFIED. Physical p14 Definitions4.1/4.2 show AP external product using GLev rows of mu and -psi(s)*mu and decomposition of psi(input mask/body); p15 Proposition4.3 gives error formula including quality beta and approximation precision; p16 shares the body key across automorphism variants. THIS published algorithm already repairs direct mask-noise amplification by gadget decomposition.
[FACT] Bernard–Joye, "Approximate CRT-Based Gadget Decomposition and Application to TFHE Blind Rotation", ePrint 2024/909 https://eprint.iacr.org/2024/909 ; mirror PDF sha256 5047de57cb080f2ed419c58f257a6fdf6ee1973d5ef21c02925c901ad1d1f1ff, VERSION_UNVERIFIED. Physical p4 Definition1 defines quality beta and precision epsilon, p5 treats radix/mixed radix approximate decomposition with low digits dropped; CRT approximate also published. Three-level truncation below is KNOWN PRIOR ART.
[PRIOR BOOT] B071 and B072 already showed factorization costs extra online extprod, direct single-row fuse explodes noise with fresh independent mask, naive secret-correlated mask constraints leak; B057 likewise warned public secret-dependent mask kernels.

## Exact GLWE algebra, toy rank-1 psi=id
Work R_Q=Z_Q[X]/(X^N+1) with GLWE ciphertext C=(A,B), phase B−A*s=m+e_in. Let evaluation keys K_B=Enc_s(mu), K_A=Enc_s(-s*mu), each with INDEPENDENT FULL UNIFORM fresh GLWE mask and small independent errors e_B,e_A. Then fused output
Y_raw=B*K_B + A*K_A
has plaintext phase:
Dec_s(Y_raw)=mu*m+mu*e_in+B*e_B+A*e_A.
This is correct functionally but high noise. If e_A is an invertible ring element (in particular the unit polynomial 1), multiplication A*e_A is exactly uniform over R_Q conditional on fixed e_A, so no universally small phase-error guarantee follows for a full-support A. This is a support/worst-case proof, NOT a general statistical claim about actual Gaussian RLWE and NOT a cryptanalytic attack.

Repair via fixed radix-B gadget decomposition with G_j=16^j, Q=2^16, d4:
K_B,j=Enc_s(G_j*mu), K_A,j=Enc_s(-G_j*s*mu).
For public B=sum_j B_j G_j, A=sum_j A_j G_j modulo Q, where every digit polynomial has coefficient abs<=8, compute
Y_exact=sum_j (B_j*K_B,j+A_j*K_A,j).
Its phase equals mu*m+mu*e_in+sum_j (B_j*e_B,j+A_j*e_A,j).
This is STANDARD GLev/AP-GGSW; independent masks still used and key material goes from 2 GLWE rows to 2d=8 rows (shared-body AP construction can change actual multi-automorphism total; not double counted here).

Known approximate gadget alternative: discard low radix16 digit, use d3 levels 16,256,4096, reconstruct A_hat,B_hat with coefficient error each abs<=8, then
Dec(Y_approx)-mu*m=mu*e_in+sum_j(dB_j*eB_j+dA_j*eA_j)+mu*((B_hat-B)-(A_hat-A)*s).
This precise new rounding term must not be dropped from full DFR analysis. Its 6 rows are less than 8 but the exchange was already studied in Bernard–Joye and prior TFHE approximate gadget work.

## Counting bound: arbitrary uniform masks versus short fixed encoding
A gadget with d public R_Q elements and each of d digit polynomials coefficientwise in [-K,K] can produce at most (2K+1)^(dN) reconstruction codewords, versus Q^N possible full-support inputs in R_Q. Exact coverage requires (2K+1)^d>=Q. With coefficientwise reconstruction residual abs<=epsilon, each codeword covers at most (2epsilon+1)^N inputs, so necessary
(2K+1)^d (2epsilon+1)>=Q.
Proof valid for arbitrary fixed *ring* gadget elements, not only coefficientwise powers B^j. NOT a general lower bound on nonlinear operations, tensor packing, expanded dimensions or altered mask/security distributions. For Q65536, K8 with optimistic 17-choice digit alphabet, minimum epsilon for d=1,2,3,4 respectively 1928,113,7,0. A single exact short row is impossible for all q-ary masks. The d3 constructed radix16 approximate scheme has observed rounding error max8, above information-theoretic min7.

## Reproducible experiment
Local stdlib file /mnt/data/boot_B085/verify_b085.py ; seed850177; N8 Q65536 radix16 d4; 800 independently randomized trials with ternary secret, monomial selector, fresh input and evaluation-key GLWE masks uniform in [0,Q), independently sampled small ternary errors. Exact arithmetic over negacyclic ring with independent decryption and error recurrence checks. Raw & exact 12800 coefficient-phase checks PASS, additional approx3 6400 coefficient error checks PASS. No security-matched FHE lattice estimate, KDM proof, native AP latency, or real DFR.
median centered RMS: RAW18842.90138; exact d4 28.64219; approx d3 27.22361. For illustrative per-coefficient threshold |err|>=Q/8, raw 800/800 trials with some crossing; exact 0/800, approx3 0/800. This threshold is NOT a certified decoding threshold. Approx3 slightly lower median in 800 toy tests is seed/parameter dependent and NOT evidence of optimality. The raw uniform-unit-witness synthetic coefficient threshold count ~0.761 is consistent with true uniform distribution.

## Decision
FAIL primary one-short-row exact/noise-safe hypothesis. Correct fix uses existing GLev/AP-GGSW, reducing row count by accepting approximation is likewise existing prior art. No new fusion primitive, no security attack, no actual performance result. A genuinely different mechanism would have to provide a secure *joint error-cancellation key transcript* with full-support public masks, not just replace multiply by a new name.
STATUS PASS_EXISTING_GADGET_REPAIR / FAIL_ONE_ROW_SHORT_EXACTNESS / FAIL_STANDALONE_NOVELTY.
NEXT_TEST B086 NOT STARTED: test ONE cancellation-correlated AP evaluation-key construction with independent GLWE zero-encryption rerandomization. Derive whether restoring full-support public masks preserves cancellation or brings back independent amplified error. If no genuinely new mechanism exists, archive B072 family, then search other primitive families.
STATE_UPDATE NO: findings/boot-STATE.md listed size187967 but Notes file read returned {} in prior turns; preserve it, append only this BOOT finding. SHIP unchanged.
REPRO: /mnt/data/BOOT_B085_handoff.zip SHA256 2445f4b321038ecc8ada9cd72a1d7cd7d0905b2149bcf0ee83842b20aca3dbc7 (ZIP integrity verified); includes BOOT_B085_REPORT.md SHA256 0e1736a57a029125cef248f721f628e64fcb7581542473c3d3c265ca3164c623, verify_b085.py SHA256 57c802135ad8a252095d179ba0d512ad8178f9237396a412b55643cd96c3c833, b085_results.json SHA256 78353c7f0d16a95a583238751bca53e6c25bd58fb1281d4b685dda464862cf3b, run log, README, SHA256 manifest.
