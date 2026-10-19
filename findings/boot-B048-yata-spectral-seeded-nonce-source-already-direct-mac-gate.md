# BOOT B048 — YATA spectral-domain seeded nonce: exact algebra but source already implements it

TRACK_ID: BOOT
ITERATION: B048
DATE: 2026-10-20
STATUS: PASS_SINGLE_PRIME_SPECTRAL_UNIFORMITY / FAIL_NEW_ONLINE_KEY_FORWARD_NTT_REMOVAL / FAIL_UNPAIRED_NONCE_AND_BODY / NO_NEW_BOOT_ALGORITHM
STATE_UPDATE: YES
ISOLATION: BOOT ONLY. SHIP PAUSED_BY_PI after I407, not consulted/modified.

## Session recovery warning
GitHub Notes list_repo_files showed existing findings/boot-B047-hlut-target-undercomplete-boolean-synthesis-gate.md SHA 9c171e129eb2127f69587932acf3de65aa316b58, B040–B047 completed. The read_repo_file endpoint unexpectedly returns empty {} for B047 and boot-STATE.md; their textual full history could not be restored, so do not pretend it was read. This B048 excludes already named CMT/Whitebox/LFBS/CMS/Hermite/hLUT work and follows source-first novel-paper method. Only create B048 docs and append BOOT state; never overwrite.

## Primary falsifiable hypothesis
YATA (TCHES2026) reduces TFHE BlindRotate BSK memory by seeded PRNG expansion. A potentially new optimization: directly derive a uniformly distributed NTT-domain random nonce a_hat from a seed rather than reconstruct coefficient-domain a and apply an online FORWARD NTT to the BSK mask. Hypothesis claims (1) legal RLWE key distribution, (2) one entire online key-mask transform can be removed with unchanged BSK body/noise/key semantics, and (3) source has not done this already. Cheapest decisive test: field/RLWE exact NTT algebra; inspect live original author RTL key stream to MAC for the alleged redundant transform; source/security/novelty gates.

## Original literature and code evidence [FACT]
Kotaro Matsuoka and Takashi Sato, "YATA: Yet Another TFHE Accelerator with Key Compression and Radix-8 NTT", IACR Transactions on Cryptographic Hardware and Embedded Systems 2026(1):325–352, DOI https://doi.org/10.46586/tches.v2026.i1.325-352. This iteration directly inspected public authors' full RTL source repository https://github.com/virtualsecureplatform/YATA and their 2026 FHE conference POSTER PDF with rendered screenshot: https://fhe.org/conferences/conference-2026/resources/posters/%5B10%5D%20-%20YATA_%20Yet%20Another%20TFHE%20Accelerator%20with%20Key%20Compression%20and%20Radix-8%20NTT.pdf . Full paper PDF was not downloaded; article text preview from ResearchGate was read but no completeness proof. Source's ASIC reports N=512, k=2, n=636 blind-rotation iterations, gadget base 2^8 and l=2, single specialized NTT prime P=5^4*2^16+1=40960001, 0.32ms BlindRotate, 5.93mm^2, 22nm, seeded ASCON XOF key compression. Poster explicitly cautions PoC uses Xoshiro128 for some non-nonce parts; this test does NOT independently certify full 128-bit security.
Exact source file Git blob SHAs on current main (whole-repository commit not pinned):
- YATA-RTL/chisel/src/main/scala/KeyCompression.scala SHA dad75d2abe84d2e02512a2238419b49a42953c8e, lines20–58: k lanes ASCONPRNG, rejection sampling of integers 0<=sample<P, immediate 32-bit key output stream; lines60–96 Xoshiro separate key stream.
- YATA-RTL/chisel/src/main/scala/BlindRotate.scala SHA 78fb163d750f815472108edabdaa2b231b95e839, lines445–449 keycompression/seedinitializer; lines476–501 keycompression stream (or noncompressed BK stream) feeds buffer then axisbrmiddle.io.axi4bkin; lines505–506 sends result to later stage.
- YATA-RTL/chisel/src/main/scala/ExternalProduct.scala SHA be536346735a88fc69ca107c08037d8350895361, lines290–326 ExternalProductMiddle receives BK rows as trgswin, multiplies DIRECTLY with INTT-transformed decomposed accumulator using MULandACC. NO forward NTT of these key rows exists. Lines330–350 the NTT of ExternalProductLater transforms the OUTPUT of multiplication, not reexpanded BSK nonce.
- YATA-RTL/chisel/src/main/scala/Config.scala SHA 414c9e23a49a2940676f1d8e75d7a629e83590ab, field/root/NTT definitions.
- YATA-RTL/chisel/src/test/cpp/bktest.cpp SHA 0f6908ae216a9f0bd9b8ce83bbcf48d61d38a35a, lines96–101 produces bsk in NTT format via bkrainttgen; lines137–157 loads spectral BK stream. This tests structural key format but DOES NOT independently prove all seeded branch CSPRNG/body pairing and security for real parameter protocol.

## Mathematical derivation and exact test [DERIVATION]
Let P prime, 2N|(P−1), R_P=Fp[X]/(X^N+1), F be invertible negacyclic NTT: F(a)_j=Σ_i a_i ψ^((2j+1)i), ψ primitive 2N-th root. F is an Fp-linear bijection. Therefore if a←uniform(R_P), then a_hat=F(a) is uniform Fp^N, and conversely sampling uniform independent spectral residues a_hat and setting a=F^-1(a_hat) gives the SAME distribution of uniform coefficients. This basic uniformity equality is classical.

For a VALID small-error ring sample b=a*s+e+m (modP), spectral equation must be b_hat=a_hat⊙s_hat+e_hat+m_hat. In particular the small error e is sampled in coefficient domain then transformed; independently sampling small per-frequency errors is NOT the same distribution. The stored BSK body b MUST be computed consistently with the seeded nonce a. This remains necessary even if key is stored completely in spectral form, and any circular/KDM security must be rechecked for the actual KDF/EvalKey assumptions.

P=40960001 is prime; P−1=2^16 * 5^4, so 2N|P−1 for N8,16 and source N512. Independent Python private exact modular tests fixed RNG seed20261020 using the direct negacyclic NTT and inverse plus independent O(N²) ring multiplication:
- N8, 100/100 randomized input tuples (uniform spectral a_hat, ternary s, small coefficient e∈[-2,2], arbitrary message polynomial m) satisfy F^-1(F(a))=a and b_hat=a_hat·s_hat+e_hat+m_hat at all coefficients.
- N16, 100/100 equivalent trials PASS.
Total200/200 toy tests. No full N512 cryptographic/RTL benchmark or proven DFR; root condition at N512 only checked algebraically.

COUNTEREXAMPLE unpaired nonce replacement: scalar s=1, a=7,e=1,m=300,b=308 modP. If keep stored body b but replace a by freshly generated independent a'=123456, decrypted phase b-a'=m-123448 modP instead of m+e=m+1. Thus any proposal "just use new spectral seed without corresponding body regeneration" FAILS correctness. It is no attack on YATA: its actual generator can/should bind seed and body at keygen.

Cross-modulus caution, NOT YATA current single-prime system: if legacy torus coefficient a∈Z16 represented canonically 0..15, reductions into p1=17,p2=97 can occupy only16 joint pairs out of 17*97=1649; independently drawn residue (16,96) corresponds to NO canonical a. Hence independent spectral masks across multiple CRT primes are not automatically the same distribution as a SINGLE 2^w torus coefficient. Exception: if underlying ciphertext is defined directly modulo Q=p1*p2, CRT independent residues legitimately encode uniform R_Q; full scheme type matters. No generalized multi-prime impossibility claimed.

## Whole-system and novelty result
[CORRECTNESS] Single-P spectral nonce sampling algebra PASS, but requires correctly matching body and coefficient error. [SOURCE COST] Proposed "save forward transform of ASCON-expanded nonce" ALREADY IMPLEMENTED: RTL streams accepted XOF values directly into spectral multiply-accumulate; only accumulator INTT and result NTT exist. So source-specific removed-transform count=0. [SECURITY] XOF pseudorandomness, actual BSK pair generation, KDM and DFR not audited; producer's PoC nonnonce generator caveat. [MODULUS] prime P single, no CRT shortcut needed; torus-vs-Fp embedding requires explicit keygen. [PRIOR ART] Uniformity under invertible NTT and seeded key compression are standard, the paper implements the key aspect. Thus claim of new BOOT optimization FAILS. Hardware speed/area/latency cannot improve solely by moving the seed domain already on chip.

NEXT_TEST B049: Do not pursue spectrally seeded YATA random-mask bypass (source already does it). Prefer new substantive BOOT computational primitive not ordinary seeded-key representation, basic row dedup, CMS knapsack, low-rank LUT or Hermite cleaning. A potentially material YATA open bottleneck is PRNG power (~46% simulated dynamic) after compression; any attempt requires new security-preserving cost/entropy mechanism and original author artifact evidence, not a generic weaker PRNG replacement. Alternatively source-audit different modern BOOT paper. One primary hypothesis and cheapest falsifier only; no automated work. B049 NOT STARTED.
END: STATUS FAIL_NEW_NTT_BYPASS / RESULT existing source uses it / NEXT_TEST B049 / STATE_UPDATE YES.
