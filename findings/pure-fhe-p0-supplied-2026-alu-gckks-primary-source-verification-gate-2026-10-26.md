# PURE-FHE · P0-PRESCOUT-20 — Primary-source gate: new ALU and GCKKS PDFs

Date: 2026-10-26 (Asia/Hong_Kong)
TRACK_ID: PURE-FHE
Previous: P0-PRESCOUT-19
Primary hypothesis H20: As of Oct 2026, non-amortized O(1)-CKKS-bootstrapping arithmetic-to-Boolean conversion remains unresolved in the triangle ALU setting, so our bounded-window/global-prefix research targets a still-open broad problem.
Cheapest decisive test: directly read primary PDF introductions/contributions/algorithms of the three newly supplied papers rather than constructing more candidates.

STATUS: FAIL_BROAD_OPEN_PROBLEM_H20; PASS_PRIMARY_SOURCE_VERIFICATION
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN
OTHER_TRACKS: UNCHANGED

## [FACT] Verify all five supplied files in GitHub Notes

File list under papers/supplied/ confirmed on 2026-10-26:
- 2026-1836.pdf SHA 71ee2d857cd59bd83fe60316120be7a5f428905a, 42 pages, 850562 bytes
- 2026-1840.pdf SHA fb5f5c20a61030b8a1ecfdb150cf4602d4dcc4ea, 37 pages, 1196040 bytes
- 2026-1869.pdf SHA 9de785af66b3106e509283c84816513d56f6f7dd, 40 pages, 800484 bytes
- 2026-2524.pdf SHA 5e38e0e5f2095604af7142b5cdba4ad5e5e86683, 49 pages, 2578347 bytes
- 2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72, 27 pages, 748302 bytes
All five read_repo_pdf returns original physical-page text, not only abstract. Extracted equations may lose typographic details, figures, or order; do not infer unverified implementation claims.

## [FACT] A2B original papers conclusively change prior art

[2026/1836] Wei, Ma, Gao, Zheng, *FHE for ALU over Large Prime Moduli and Application to One-Round Threshold ECDSA* https://eprint.iacr.org/2026/1836 . Original p3 §1.1: homomorphic canonicalization in 3 CKKS bootstrap operations for power-of-two moduli and 5 for large prime moduli, plus O(log n) CKKS levels. p5–7 §1.2–1.3: explicitly credits related/concurrent Shen et al. and Liu et al., uses A2A-I refresh, multi-value LUT, contracting redundant bit strings, LCtoC parallel carry, and extra wrap-around LUT for prime modulus. p7 explicitly compares SLWL26 and LMWW26: for n=256 LMWW26 indicator state candidate can output 198 indicator ciphertexts with |Lambda|=33, |C|=2, kappa=0; each intermediate carry composition level 264 ct-ct multiplications and 132 rotations for 6 levels; an estimated 237 seconds for this stage in that authors' single-threaded configuration. This is 1836's paper-side estimate about 1869, NOT our benchmark; may reflect source version/parameter choices. P4 reports ECDSA 56s on RTX Pro 6000 GPU, but cannot compare directly to CPU ALU benchmarks.

[2026/1840] Shen, Li, Wang, Lu, *Efficient Homomorphic Arithmetic Logical Units with O(1) Bootstrapping*, https://eprint.iacr.org/2026/1840 . pp1,3–6 §1.1–1.2: general-base triangle encoding, after RefreshI two functional bootstrapping calls, plus leveled parallel carry and bit correction with O(log ell) depth, WITHOUT cross-ciphertext amortization. p5–6 explicitly constructs finite-overflow window difference sk=Dk+I'_{k−1}−D I'_k; one FBT extracts residues and associated quotient, yielding vk=Dk+c_{k−1}−D c_k; second multi-value FBT derives candidate bits and local carry maps, then prefix/tree composition. This directly escapes P0-17/18 coordinate-local no-go by doing nonlocal carry composition. p26 Table3 single-thread N=2^16: d=2, 64 bits 71.47 seconds per batch; 256 bits 104.02s; d=32 has higher packing and best amortized cost 29.84ms/word at 64 bits, 138.51ms/word at 256 bits. Paper p26 says FBT stages dominate ~80%. The two FBT calls are AFTER RefreshI; do not miscount total from arbitrary unrefreshed input. These are paper-reported tests, not independently replicated.

[2026/1869] Liu, Ma, Wang, Wang, *High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping*, https://eprint.iacr.org/2026/1869 . pp1,3–7: general polynomial F_M(X) with F_M(b)=M, CVP search for well-conditioned polynomial, fallback Montgomery. Arith-to-digit / A2B procedure: one FBT to extract residues, linear operations to cancel shared overflow, second multi-value FBT for candidate bits/carry state, associative binary-tree composition O(log ell) depth. p4 claims exactly 2 functional bootstrap calls and logarithmic depth for A2B, not necessarily inclusive of overflow refresh; p5 explicitly says after refreshing overflow I'. Reported 64/128/256 A2B speedups over Gao–Zheng 3.75/6.40/14.17x (source-reported, not our native benchmark).

H20 is rejected: the broad nonamortized constant-bootstrap triangle A2B task has been achieved in primary sources. P0-17/18/19 bounded-window/noise lower bounds are limited to their precise restricted proposals and do not refute these cross-window constructions. No credit for rederiving their carry-state procedure.

## [FACT] GCKKS papers form a sequential pair; no longer a pending first paper's bootstrap open problem

[2026/2524] Ma, Liu, Wang, Wang, *Homomorphic Encryption for High-precision Arithmetic of Approximate Numbers*, https://eprint.iacr.org/2026/2524 ; original pp1–4 and pp7–10: proposes GCKKS encoding/decryption using F-augmented CKKS ciphertext, sacrifices slot capacity for reduced modulus consumption; claims N=2^14, 7 levels, >1000-bit precision, first squaring/rescale 28.16ms. p7 explicitly leaves GCKKS bootstrapping to future work and previews it in p10.

[2026/2600] same group, *High-precision Bootstrapping for GCKKS*, https://eprint.iacr.org/2026/2600 ; original p1 says DRAFT October 22, 2026. Original pp2–4: develops GCKKS bootstrapping using low-precision overflow extraction, iterative precision-doubling and ciphertext splitting, non-unit F conversion with unused-slot-aware bounds. Cost for target p bits and 2N/k useful slots: precision-dependent O(k) homomorphic operations, modulus consumption O((p/k) log k). p24 Alg1 and Lemma3 give a useful-slot-preserving CKKS->GCKKS re-encoding and its correctness condition, including ∥b+as∥_2 + ∥eF∥∞ < Q/2. p25 states <=15k key switchings over precision-doubling stage (source asymptotic upper bound) and O(k) linear work; p26 §6 EXPLICITLY says 'Implementation — Not available yet.' Thus this is a construction with stated theoretical analysis, not already a native-validated high-precision bootstrap. It closes the 2524 'no bootstrapping' issue at the algorithm/proof level, NOT at measured practical level.

## [DERIVATION] FHE innovation/cost frontier

Raw number of CKKS bootstraps is insufficient: compare all refreshing and A2B calls, full multiplicative depth, precision/DFR, number of intermediate ciphertexts, rotations, ct-ct multiplications, evaluation-key memory, latency and useful packing under matched security. 2026/1836 p7 concretely warns about a 1869 indicator explosion; 1840 p26 ~80% is in FBT phases, but a mere low-level optimization without a new mechanism does not establish a crypto publication.

GCKKS 2600 is likely more open for SOURCE-BASED minimal native feasibility because §6 implementation is explicitly absent, especially its conditional CKKS->GCKKS conversion and splitting/memory; but no correctness/security flaw is asserted. Before expensive Codex, pick one falsifiable algebraic/noise bound or toy, and survey contemporaneous Dumezy 2026/2513 and Cheon–Lee 2026/2531 (cited in 2524/2600) for prior art.

## Decision

KILL/PARK: The BROAD 'nonamortized O(1) A2B is unsolved' formulation and direct coefficient-local/global-prefix concepts as novel candidates. All primary sources now available.
P1 recommended: GCKKS implementation-less bootstrapping — exact conditional conversion/noise invariant / cost ledger under fixed target precision and k, with an earliest toy correctness/overflow gate; require PI before native budget.
P2: Specific ALU A2B two-FBT critical-path vs carry-composition and memory Pareto, after matched baselines; no novelty established.
P3: Complete recent source coverage in related 2026/2513 and 2026/2531; no claim of having read them.
Keep user as PI with final direction selection.

END_OF_ITERATION:
STATUS: FAIL_BROAD_OPEN_H20 / PASS_SOURCE_CHECK
RESULT: 5/5 VERIFIED_SOURCES; 3 independent 2026 algorithms report nonamortized constant-FBT A2B; 2026/2600 builds GCKKS bootstrap but implementation NOT AVAILABLE YET.
NEXT_TEST: GCKKS_2600_CONVERSION_MODULUS_BOUND_MINIMAL_GATE after competitor/novelty scan.
STATE_UPDATE: YES (isolated finding only, no global STATE.md edit)
CODEX: NOT_RUN
