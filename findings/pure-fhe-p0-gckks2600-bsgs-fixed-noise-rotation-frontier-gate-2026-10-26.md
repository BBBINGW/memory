# PURE-FHE · P0-PRESCOUT-27 — BSGS noise-certificate / rotations Pareto gate

DATE: 2026-10-26 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-26, isolated finding pure-fhe-p0-gckks2600-first-split-norm-unit-escape-priorart-gate-2026-10-26.md
STATUS: PASS_CONDITIONAL_FIXED_K_CERTIFICATE_FRONTIER / FAIL_UNCONDITIONAL_SQRT_L_CERTIFICATION / NOVELTY_NOT_ESTABLISHED
CODEX: NOT_RUN. No GPU / remote / native implementation.
OTHER_TRACKS: UNCHANGED. No shared STATE.md edit.

## Primary hypothesis H27 and cheapest test
H27: For the single-ciphertext partial StC in original GCKKS 2026/2600, does the ordinary BSGS rotation-optimal grouping g≈sqrt(L) automatically retain the paper's fixed normalized unused-slot noise invariant K merely by increasing the rescaling ratio r, without increasing rotation work?
Cheapest decisive test: directly algebraically rearrange the source p23 BSGS propagation certificate, then instantiate one transparent fixed-K example. All conclusions are ABOUT THIS PAPER'S SUFFICIENT UPPER-BOUND CERTIFICATE, not lower bounds on actual ciphertext noise or all linear-transform schedules.

## [FACT] Primary source

User-supplied papers/supplied/2026-2600.pdf, blob 8db712155d087284d21e924623496bc48e36eb72, original physical pp22–23 §5.3, freshly reread on Oct26:
After k-dependent multi-ct reconstruction, the remaining single-ct StC size is L=2N/k. BSGS for g|L evaluates L diagonals via inner baby rotations and outer giant rotations. Under the slot-aware model, the printed normalized bound is
  g_BSGS,r(B)=(L Brnd /r)(B+Bks)+(L/g)Bks+Bms.
Here r is defined via rescale ρ≥r |F(ξ)| at all relevant unused slots, and Bks, Brnd, Bms bound normalized key switching, plaintext mask rounding, and modulus switching errors. Authors require B_BSGS(r)≤K<B_mult^+(r) and give a choice r=max(2L Brnd, (2+2L/g)Bks+4Bms) in their parameter analysis. Original §4 pp14–16 additionally requires ρ≥max(1,r c_e) with c_e=max_unused |F(ξ)| and may need H/scale adjustment.
This is SOURCE-ALREADY-ACKNOWLEDGED BSGS noise control, NOT an author correctness bug.

## [DERIVATION] Fixed-K certificate region

For a FIXED target normalized unused-slot budget K with Bks>0, requiring g_BSGS,r(K)≤K yields
  (L Brnd/r)(K+Bks)+(L/g)Bks+Bms≤K.
Even taking r→∞ leaves (L/g)Bks+Bms. Thus this particular sufficient upper bound can certify fixed K only if
  K>Bms and g> L Bks/(K−Bms).
When this holds, the exact minimum (non-strict) acceptable r from the inequality is
  r≥ L Brnd(K+Bks)/(K−Bms−(L/g)Bks).
A classic rotation proxy is (g−1)+(L/g−1)=g+L/g−2 and is minimized near sqrt(L) without noise constraints. At fixed K,Bks,Bms independent of L, the SOURCE CERTIFICATE instead requires g=Omega(L). This is NOT an actual lower bound on rotations: the paper's bound is conservative and the user may allow K to change with r,L, reduce Bks, or use different noise analysis/algorithm.

## [TOY_NUMERIC, deterministic rational arithmetic, NOT AUTHOR PARAMETERS]

Take N=65536, k=256 => L=512. For illustration ONLY set Brnd=Bks=Bms=1, K=16, and a normalized rescale parameter r=2048.
  g=32: L/g=16, certificate residual floor (L/g)Bks+Bms=17>K, thus NO finite r will certify K=16. Rotation proxy = 32+16−2=46. At r=2048 the bound evaluates 21.25.
  g=64: floor =8+1=9<K, required r_min=512*(16+1)/(16−1−8)=8704/7≈1243.4286. r=2048 certifies g_BSGS,r(K)=512*17/2048+8+1=13.25≤16. Rotation proxy =64+8−2=70, +24 (=52.17%) relative to g32.
  g=128: floor=5, required r_min=8704/11≈791.27, rotation proxy=128+4−2=130.
These example noise magnitudes are invented mathematical stress-test inputs and NOT claimed as Ma–Liu–Wang–Wang's encryption parameters or measured native rotations; the rotation proxy ignores automorphism overlap/hoisting, keys and preprocessing. At fixed K, increasing g can buy a smaller r at the cost of more baby rotations.

## [DERIVATION] Additional scale-floor screen

If using the paper's displayed sufficient choice r≥2L Brnd in §5.3, the corresponding sufficient minimum for normalized noise control is ρ≥max(1,2L Brnd c_e), with c_e the maximum unused factor magnitude of the ciphertext at THIS transform. For L=512 and illustrative Brnd*c_e=1 this is ρ≥1024 (10 bits). If Brnd*c_e is far below one, or output scale is large, the floor can be negligible; actual c_e, Δ' and modulus primes are unspecified. Do NOT claim 1024 as author-required or an extra actual level, and do NOT call the displayed sufficient r a mathematical lower bound for every construction.

## Prior art and novelty limit

Known CKKS linear-transform cost optimization includes LCR+AKS, ePrint 2025/1403 and author's 2026-06-29 writeup https://ckks.org/blog/2026/less-mod-ckks/ (AKS also usable for StC, according to author), and standard BSGS noise/rotation tuning. Rewriting the published bound, selecting a different g, or importing ordinary AKS is NOT a new FHE contribution.
A candidate new mechanism would need to change the **GCKKS-specific outer key-switching normalized-noise vs rotation frontier** (perhaps preserving the nonunit F after hoisting/aggregation), prove correctness/security/unused-slot bounds, and show matched end-to-end key, memory, prime-bit and runtime gain. No such mechanism is constructed this round.

## Decision

H27 as an unconditional auto-certificate for g≈sqrt(L) under fixed K FAILS: source's g-independent-of-r outer term can exceed K. A larger g can restore this particular certificate; no claim of actual ciphertext break. This gives a precise feasibility diagnostic but NOT a novel construction, and does not prove all balanced BSGS schedules are invalid.
PI should consider the correct strategic value question: only pursue if an independent new GCKKS-specific key-switching/error-representation technique can shrink (L/g)Bks without a compensating cost. Otherwise PARK, avoiding further algebraic bookkeeping loops. The next technical test, if PI continues lightweight analysis, must first compare source 2025/1403 (AKS at StC) and 2600's restricted rotations/key conversion for an exact *nontrivial* composition obstruction; reject if it is ordinary AKS+BSGS.
Cheon–Lee 2026/2531 revised full §6 remains SOURCE_BLOCKED in supplied source list and public attempts; avoid treating 2600's secondhand algorithm description as first-party verified.

END_OF_ITERATION:
STATUS: PASS_FIXED_K_BSGS_CERTIFICATE_TRADEOFF / FAIL_BALANCED_G_AUTOCERTIFICATION
RESULT: Exact inequality g> L Bks/(K−Bms) and r≥L Brnd(K+Bks)/(K−Bms−(L/g)Bks); illustrative L512 g32 not certifiable K16, g64 r2048 certifiable, rotations proxy 46→70. Not a paper bug or native performance claim.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Prior-art-first exact AKS (2025/1403) versus GCKKS restricted-rotation/normalized-unused-noise interface. Kill if trivial transfer; obtain actual source before any construction or Codex. Alternatively PI may park this line and select a different Pure FHE high-value gap.
STATE_UPDATE: YES — isolated PURE-FHE finding only; shared STATE.md untouched.
CODEX_REQUIRED: NO (PENDING future native only with PI authorization).
