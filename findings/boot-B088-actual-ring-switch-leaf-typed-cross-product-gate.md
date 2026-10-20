# BOOT-B088 — Real ring-switch leaf interface and cross-leaf nonlinear arithmetic cost gate
Date: 2026-10-20 | TRACK_ID BOOT | SHIP PAUSED.
STATUS: PASS_REAL_LEAF_TYPES / PASS_TOY_CROSS_LEAF_MULTIPLICATION / FAIL_AUTOMATIC_SQUARE_COST_ADVANTAGE / FAIL_STANDALONE_NOVELTY / UNCLEAR_FOURIER_NATIVE_COST.

## Primary falsifiable hypothesis
B087 proposed evaluating sparse-Fourier nonlinear functions across ring-switched leaf ciphertexts, but assumed additive leaf plaintexts x=a+b without source proof. Can the *real* Liang-Ding leaf ciphertexts multiply under a common small-ring secret, and does a concrete nonlinear function evaluated without forward/reverse slot recovery save work after including all cross-leaf operations? Smallest gate: inspect full original author experiment code, derive exact layout and check f(x)=x^2 through exact field and noise-aware toy GLWE, then compare source recovery circuit costs. No new publication/acceleration claims without complete cost.

## Source provenance (real authors' code, verified via GitHub)
Author repo: https://github.com/Zhaoyang-Liang/bootstrapping-via-ring-switching-without-slot-recovery
[FACT] Source code/table_3_ckks_bootstrapping_and_table_9_slot_recovery/code_ckks_shared/source/main.go, Git blob 6d135b72381b5d14d0049caa0f798f487dbfb421:
lines 887–937 splitTree calls RingPackingEvaluator.SplitNew and mergeTree calls MergeNew; lines 2383–2424 GenRingSwitchingKeys and skLeaf=skMap[leafLogN] then every leaf evaluator and decryptor use the SAME skLeaf. Lines 2565–2630 implement Split → leaf ScaleDown/ModUp/CoeffsToSlots/EvalMod/SlotsToCoeffs → Merge.
[FACT] Vendored Lattigo source code/table_3_ckks_bootstrapping_and_table_9_slot_recovery/code_ckks_shared/source/deps/subring_bts-main/core/rlwe/ring_packing.go, blob 74b7c25eaf199a501251673c6badce9893d0f17e, Split doc lines 191–193 and 248–250, Merge doc lines 394–396, 446–448: exact plaintext ring relation ctN[X]=ctEvenNHalf[Y]+X*ctOddNHalf[Y], Y=X^2. Uses SkN→SkNHalf evaluation key (lines 218–223). Lattigo upstream v6.2.0 core/rlwe/ring_packing.go blob e716d2d2f959e54c74493d1d2a80182941f61856 independently agrees.
[FACT] Author Table9 code/table_3_ckks_bootstrapping_and_table_9_slot_recovery/table_9_ckks_slot_recovery_baseline/source/main.go, blob 8806b327e824ea7703511fb2011a856b0b845e1c, lines 234–245 constructs per-slot public twiddle alpha_j=exp(2 pi i * 5^j/(4n)) in chosen CKKS slot order; lines 283–335 implement forward and inverse slot recovery; lines 462–501 include two leaf bootstraps and merge. Table9 script run_fused.sh blob 7bd162ebac8390de95b85f90ec7eb02c7195b9f4 additionally benchmarks no-recovery/separate-recovery/fused-inverse routes. New methods must beat source's already available fused recovery rather than a naive full-recovery strawman.
[FACT] Original GroupII run script blob 45c88ed998090254d88319995ce29735223f9176 uses top logN17, two layers, leaf logN15; GroupIII blob dd375d633228d6807b5a94ee8575835617418db uses top logN17, one layer, leaf logN16.
[SOURCE LIMITATION] Complete ePrint2026/1779 and SWIFT ePrint2026/1163 PDF not acquired through Research Notes in B087 (HTTP403). No unverifiable theorem numbers or text claims. Source CODE is directly verified. No native build, matched time, performance or security verification.

## Actual plaintext and slot map
Big ring RBig=Z_Q[X]/(X^(2n)+1); small ring RSmall=Z_Q[Y]/(Y^n+1); Y=X².
Split of arbitrary m: m(X)=a(X²)+X b(X²). Both leaf ciphertexts share the same skLeaf: hence an ordinary same-key leaf ct-ct multiplication (with relinearization and noise/levels) is correctly typed. For small root u=alpha², big ring roots ±alpha give CKKS slots zplus=a(u)+alpha b(u), zminus=a(u)-alpha b(u). alpha is public and slot-dependent. Forward recovery is a±alpha b; inverse a=(zplus+zminus)/2, b=(zplus-zminus)/(2alpha). In B087 the hypothetical x=a+b mod m is NOT a faithful CKKS model; actual analytic complex harmonic factorization must account for alpha and two branches.

## Exact nonlinear identity
For f(x)=x²:
(a(X²)+X b(X²))²=[a(Y)²+Y b(Y)²]+X [2a(Y)b(Y)].
Compute a², b², ab via three small-ring ciphertext products under skLeaf, including relinearization, then use a public monomial factor Y and factor 2, MergeNew. This avoids explicit twiddle recovery in the arithmetic toy but is standard polynomial ring arithmetic and NOT an original primitive.

## Independent reproducible experiments
Pure standard-library deterministic Python file verify_b088.py, seed 880426, not Lattigo.
[TEST] F65537 big ring N=16 and small ring n=8, primitive 32nd root. 256/256 fully random big-ring polynomial square identities PASS, 4096/4096 big-root slot and inverse recovery checks PASS.
[TEST] Same small-ring ternary secret for two independently masked encrypted leaf polynomials, uniform full mask, short {-1,0,1} errors, radix16 d5 gadget relinearization key encrypting s² with fresh independent masks/noise. 96/96 full encrypted two-leaf square and 1536/1536 coefficientwise decryption/noise relations PASS, maximum centered residual 282. Toy not 128-bit secure, no CKKS approximate errors or native performance.
[TEST] 256 random complex a,b and four author-ordered public twiddles, both signs: 2048/2048 analytic exponential factorizations PASS, max numerical abs diff 6.67e-16. NO encrypted exponential evaluations performed.

## Decisive cost/novelty gates
For f(x)=square only, author's Table9 separate recovered-slot route uses 1 forward ct-pt alpha multiplication/rescale, 2 small-ring ct-ct branch squares, 2 inverse ct-pt multiplications/rescales, Split and Merge. Thus 2 ct-ct + 3 ct-pt (+3 ct-pt rescales), before keys and level effects.
Our no-recovery even/odd arithmetic uses 3 small-ring ct-ct +3 relinearizations, one public monomial operation and cheap scalar 2, Split and Merge. Fewer ct-pt does NOT guarantee faster when one more ct-ct and relin is necessary; comparison must measure levels/noise. Direct top-ring ciphertext square also exists as one bigger-ring ct-ct multiplication, without Split/Merge, and must be baseline for this toy function. Heuristic NTT cost for three n-vectors vs one 2n-vector gives ratio about 1.5 log2(n)/log2(2n), not favorable for typical sizes, without accounting for key switching and actual RNS.
For one analytic Fourier exponential mode, computing both top branches from unrecovered leaves naively uses 3 unary leaf exponent evaluations (a,+alpha b,-alpha b), then 2 ct-ct products, plus branch reconstruction; recovered-slot method needs 2 unary exponent evaluations and known forward/inverse twiddles. Claimed reciprocal of exp(-b) is not a free FHE operation. Public Fourier/low-rank sharing already studied by SWIFT 2026/1163 and Low Rank FBT 2026/1264; no novel cost advantage established by the identity.

## Final decision
PASS real ciphertext typing and cross-leaf multiplication, correcting B087's missing-key uncertainty; FAIL automatic net benefit for square, generic ring identity known; UNCLEAR any special Fourier-sparse multi-output benefit at matched secure CKKS parameters. No native Lattigo benchmark or independent novelties claimed.
STATUS PASS_TYPED_CROSSLEAF / FAIL_STANDALONE_ALGORITHMIC_NOVELTY / UNCLEAR_SECURE_SPEED.
NEXT_TEST B089 NOT STARTED: only one concrete Fourier-sparse CKKS function and a complete two-branch DAG with ciphertext keys, levels, relin, twiddle recovery/merge. Compare explicitly to authors' Table9 FUSED INVERSE and SWIFT; if no strict full-circuit advantage at same security and output precision, archive this branch. Avoid repeat of toy ranks.
STATE_UPDATE NO: BOOT-STATE.md existing 187967-byte file cannot be safely read via isolated Notes; do not overwrite. No writes to SHIP.
LOCAL ARTIFACT ZIP /mnt/data/BOOT_B088_handoff.zip SHA256 625a14305c3fe37b11f832b6d0a0ffd2dd0df3542d31cdda31bc3c3c784533a7. Contains 10KB report SHA256 ec657ff7ef6a970e76e434cc68239469cb98e0a0050897dd18b9c9d5befb15e1, script SHA256 d578d286e36eedf6203952a9503220ae13a438a62dea37e03b1ae7a62c15b55e, JSON SHA256 3e2c0d1ebba38604e538cd341442cae9a2d8517cae94640fe56e64755e0343e4, full log, README and manifest; ZIP CRC PASS.
