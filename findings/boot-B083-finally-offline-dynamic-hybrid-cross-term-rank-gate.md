# BOOT-B083 — FINALLY static preprocessed HybridProduct cannot freely replace Dai dynamic grouped HProd
Date: 2026-10-20. TRACK_ID BOOT ONLY. SHIP PAUSED.
STATUS PASS_EXACT_OFFLINE_SUBSET_KEY_GLWE / FAIL_COMPACT_OFFLINE_LINEAR_GROUP_AGGREGATION / FAIL_GENERIC_MULTIBIT_NOVELTY / UNCLEAR_REAL_MKFHE_SECURITY_NOISE_COST.

## Primary falsifiable claim
Borrow FINALLY's preprocessable HybridProduct key method to replace h online Dai NTRU-to-MK-RLWE grouped HProd conversions by one conversion with a compact, input-independent evaluation key, using only online PUBLIC R-linear combinations, with neither the h−1 noisy NTRU ciphertext multiplications from B064 nor exponentially expanded subset-product keys. Decisive gate: exact source type, two-group mixed-term no-go, bounded-key feature-space rank and a positive expensive construction. No B064 Gaussian/noise parameter sweep.

## Source / provenance
[FACT] Park–van Leeuwen–Zajonc, FINALLY: A Multi-Key FHE Scheme Based on NTRU and LWE, ePrint 2024/1505 https://eprint.iacr.org/2024/1505. Connected Research Notes full source PDF SHA256 97d2375e041c2c554f25b78cac86165928aa89ff9c3d1f045df6335bf72b5a72 VERSION_UNVERIFIED. Physical p21–23 Section4.4 and Figure5: initial x1 encrypts g*f1, then xi = HybridProduct(x_(i-1),hpki,keys) encrypts g*product_(j≤i) f_j. Those f_j are FIXED secret keys, not functions of online ciphertext input. The resulting MK-LWE key-switching key is computed offline, then reused online; p23 explicitly notes the generated key is input-ciphertext-independent.
[FACT] Dai–Xiang–Deng–Zhang, Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026), DOI https://doi.org/10.1186/s42400-026-00563-w. Definitions5, Lemmas2–4, Algorithm3: online k*l grouped NTRU→MK-RLWE ExtProd+HProd evaluations; each group monomial is a function of actual public LWE mask and SECRET selection bits. Thus cannot be a fixed secret polynomial product preprocessed as in FINALLY. B063/B064 NTRU pre-coalescing algebra correct but large final noise; B082 reversed operand order did not fix it.
[PRIOR ART] Multi-bit blind rotation with enlarged BSK is already established (Zhou2018/Joye2022; TFHE-rs official https://docs.zama.org/tfhe-rs/configuration/parallelized-pbs and https://www.zama.org/post/bootstrapping-tfhe-ciphertexts-in-less-than-one-millisecond). Expansion into encrypted secret-bit subset functions is a classical Boolean multilinear representation, not itself a new cryptographic primitive. Do not equate its exact key formats or noise properties to Dai without proof.

## Minimal functional mismatch
For plaintext factors U=X^u and V=X^v in Rq=Zq[X]/(X^N+1), desired output UV=X^(u+v). Public-affine aggregation U+V−1 differs from UV by (U−1)(V−1), nonzero for u=v=1 (polynomial X²−2X+1), q257 and q2^16, N8. Any **separately affine** map of independent inputs has vanishing mixed finite difference; true multiplication need not. A fixed-key HProd's semantic plaintext action on its input is linear multiplication by that key's fixed secret, and so an HProd on a publicly linear input does not conjure the missing group cross term. Gadget decomposition is nonadditive at ciphertext/noise level, which is NOT a route to correct new nonlinear plaintext semantics.
[TEST] 4096 independent mask GLWE input pairs for each q∈{257,2^16}, full random masks, shared toy ternary GLWE secret, zero noise: input decryption 8192/8192 PASS per modulus. Affine result != UV in 3620/4096 for q257,3592/4096 for q65536. Accidental equality (e.g. identity monomial) does not falsify witness.

## Stronger finite-field rank / offline key feature-space gate
Let source secret bits s_i∈{0,1} and a_i∈{0,1} PUBLIC (this small subdomain suffices for a negative test), target F_a(s)=X^(Σ a_i s_i). In odd q257 and Rq with N8, use evaluation at primitive 16th root ζ=2, ζ^8=−1, yielding matrix indexed binary a,s:
 M[a,s] = ζ^(Σ a_i s_i) = [[1,1],[1,ζ]]^(tensor m).
This matrix has determinant (ζ−1)^(m 2^(m−1))≠0 and rank 2^m. Any evaluation with D fixed secret-dependent scalar/ring features and only PUBLIC R-linear coefficients on those features has after evaluation rank≤D, so D≥2^m for universal F_a. This is a capacity result only in the stated fixed key same-ring public-linear online model, not a blanket MKFHE key-size lower bound.
If independent local group outputs with g1 and g2 bits are available, their functional spans cover 2^g1+2^g2−1 independent Boolean-subset terms. The missing cross-feature dimension is exactly (2^g1−1)(2^g2−1). Verified via exact finite-field Gaussian elimination:
 group bits 1+1: needed cross1; 2+2:9; 3+3:49; 4+4:225.
 m=1..8 evaluation-matrix ranks exactly 2,4,8,16,32,64,128,256, respectively.
Caveats: alternate rings, additional slots, automorphisms, nonlinear key evaluation and interaction are excluded and must bear their real cost/security.

## Positive but expensive offline construction
For each nonempty S⊆[m] publish separately randomized GLWE_z encryption K_S of product_(i∈S)s_i under independent bootstrap secret z, and at runtime compute
 C=triv(1)+Σ_(S≠empty) (product_(i∈S)(X^(a_i)−1))*K_S.
Then Dec_z(C)=X^(Σ a_i s_i)+Σ_S c_S(a)*e_S exactly, for any public a modulo 2N, with 2^m−1 keys and corresponding ciphertext/plaintext polynomial multiplications, no online ct-ct product.
[TEST] R_(2^32), N8, keys have independent uniform GLWE masks, independent {-1,0,1} errors, 48 random public input masks per m:
 m4:15 keys,48/48 exact error recurrences, error RMS5.709 max26;
 m6:63 keys,48/48, RMS17.134 max73;
 m8:255 keys,48/48, RMS71.172 max242.
Toy only. This does NOT establish KDM/IND-CPA safety of secret-product key transcript, secure noninteractive cross-party key creation, native Dai equivalence, DFR or 128-bit noise bounds. Eliminating online HProd counts is NOT a proof of low total latency: evaluating exponential many public-ciphertext multiplications and loading larger keys can cost more.

## End of iteration
STATUS FAIL_COMPACT_OFFLINE_LINEAR_HYBRID_AGGREGATION, PASS_BOUNDED_EXPONENTIAL_OFFLINE_SUBSET_KEY_FUNCTIONALITY, FAIL_GENERIC_NOVELTY.
RESULT FINALLY precomputes fixed NTRU secret products, while Dai's grouped rotation factors are dynamic; mixed finite-difference witness and exponentially growing function-space rank obstruct any compact *purely linear* offline replacement in the stated model. New nonlinear interface, secure cross-term key semantics, or different packing capacity is needed for a meaningful improvement.
NEXT_TEST B084 NOT STARTED: test only one narrow 2+2 bit key for NTRU→MK-RLWE joint-group conversion (9 missing cross secret subset features). First inspect existing multi-bit bootstrapping/Lee grouped keys and require a typed secure common-key conversion. Kill before native if it is old multi-bit PBS unrolling, needs original two group HProd conversions, or still incurs 9+ expensive terms making it slower. B072 alternative fused EP remains SECONDARY.
STATE_UPDATE NO: existing findings/boot-STATE.md ~187967 bytes cannot be read reliably through isolated GitHub Notes, do not overwrite. Only append new BOOT finding. SHIP untouched.
REPRO /mnt/data/BOOT_B083_handoff.zip SHA256 f61bc976fcf7e794b8d498b42bee2d2cf139b9a0e8e1c843c9f87cb09faa4d9f. Includes detailed standalone report (SHA256 1e0b0a2c5e842bc6349206b633c38f746a61759c616463512f6de074d8e9d7d4), stdlib script SHA256 a09b1af98c5e6e228ae4ffeb49b0ed4c4d8f863f402f6d3f4220403be91458d1, JSON/log/manifest, zip integrity verified.
