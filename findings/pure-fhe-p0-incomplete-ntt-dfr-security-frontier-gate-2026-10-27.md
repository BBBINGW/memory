# PURE-FHE · P0-PRESCOUT-37 — Incomplete-NTT amortized bootstrapping: 8-bit DFR frontier gate

Date: 2026-10-27 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-36; findings/pure-fhe-p0-ternary-signboot-trigonometric-hermite-prior-art-gate-2026-10-27.md
STATUS: FAIL_H37_SAME_FAST_8BIT_AT_2^-128_DFR_WITHIN_PUBLISHED_CONFIGS / PASS_SAME_SOURCE_LATENCY_DFR_FRONTIER / NO_NEW_CONSTRUCTION
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO. Native/GPU/remote/Codex work not authorized or run.
STATE_UPDATE: YES isolated finding; global STATE.md and other tracks untouched.

## Problem-first one primary falsifiable hypothesis

H37: In Paiva et al. ePrint 2025/696's amortized GSW/NTT approach, the claimed free incompleteness speed benefit is available at 8-bit message precision with both (i) author-estimated ≥128-bit LWE computational security and (ii) model-predicted decryption failure probability ≤2^-128, without increasing amortized time relative to the 584.7 ms author-fastest configuration.

Cheapest decisive test: use the same author's Table 2 8-bit cases only, retain N,p,p*,w,ell and DFR, filter by exact (ii), then compute source within-experiment time penalty. Explain what incomplete NTT algebra does/does not alter, and compare cross-family results ONLY as nonmatched context.

## [FACT] Direct primary-source evidence

Paper: T. B. Paiva, G. De Micheli, S. M. Hafiz, M. A. Simplicio Jr., B. Yildiz, *Faster amortized bootstrapping using the incomplete NTT for free*, ePrint 2025/696, https://eprint.iacr.org/2025/696. 26ish-page cached official-ish GitHub mirror available through GitHub Notes get_eprint_paper, VERSION_UNVERIFIED; physical pp3–4,8–15,19–21 were read. Original §4.1 describes NTT butterfly factorization M=MB MA with incompleteness parameter ell and split alpha, and §4.2 embeds base multiplication into the first half so moderate ell has no extra homomorphic depth. It is an author's published method, NEVER OUR NEW TECHNIQUE. For N=1024 alpha=6, ell≤lgN−alpha=4 is 'free' in its specific two-part depth model. Its DFR correctness bound Eq.(1) in §3.2 p10 depends on N,p,p*,w and message bitwidth κ, not directly on ell, so incompleteness adds allowed congruence primes p rather than reducing noise for fixed p. It uses RingGSW over a circulant ring with p-dependent automorphism keys and special cyclotomic constraints, NOT the modern BatchBoot architecture.
Original §5.2 Table 2 physical p20 (all author claimed ≥128-bit computational LWE security, median single-thread on Xeon Platinum8260 2.4GHz):
  original GPVL23 N1024,p12289,ell0,κ8 model DFR 2^-17.3, amortized1237.9ms/msg.
  author's N1024,p7681,ell2,κ8 DFR 2^-8.8, 585.6ms/msg.
  author's N1024,p7937,ell3,κ8 DFR 2^-9.3, 584.7ms/msg (their FASTEST).
  author's N1024,p16001,ell4,κ8 DFR 2^-24.1, 1311.1ms/msg.
  author's N2048,p7681,ell3,κ8 DFR 2^-39.1, 879.8ms/msg.
  author's N2048,p7937,ell4,κ8 DFR 2^-41.5, 882.7ms/msg.
  author's N2048,p12289,ell0,κ8 DFR 2^-90.2, 1872.5ms/msg.
  author's N2048,p15361,ell2,κ8 DFR 2^-131.9, 1931.5ms/msg (only listed meeting ≤2^-128 at 8bit).
Original §5.2 p20 says (N2048,p7681) about 50GB RAM, old GPVL23 N1024,p12289 about 87GB RAM. The p-dependent automorphism keys dominate RAM according to author footnote; DO NOT interpolate a precise memory number at unmeasured p15361 or treat listed RAM as BSK-only. The author explicitly notes 2.12× speedup is under a *worse* DFR and says lowering DFR while preserving fast run is future work. §5.3 p21 compares against TFHE-rs 1.0, not 2026 BatchBoot: 660.68ms/msg TFHE PBS in author's benchmark, and 584.7ms/msg for own configuration. Source-aligned historical statement only.

## [DERIVATION + TOY_EXECUTED] Same-table 8bit security-conditioned frontier

Filter the author table at the strict 8bit model-DFR threshold ≤2^-128. Sole feasible listed candidate is N2048,p15361,ell2 at 1931.5ms/msg. Fastest listed (N1024,p7937,ell3) has DFR 2^-9.3 and fails the high-reliability constraint by 118.7 exponent bits. Slowdown 1931.5/584.7=3.303403454763126. For a relaxed 2^-64 bound, fastest listed 8bit configuration is (N2048,p12289,ell0) at1872.5ms/msg; for 2^-128 only the 1931.5ms configuration. This is NOT an impossibility result over untested parameters or newer algorithms; it falsifies H37 ONLY for this author's explicit tested parameter list.
The original 2.12× claims speedup versus GPVL23's 1237.9ms at DFR 2^-17.3 using 584.7ms at DFR 2^-9.3, i.e., those **are not matched on DFR**. Conversely comparing secure 1931.5ms to old GPVL23 1237.9ms is also NOT same-DFR and does not establish lack of overall algorithmic acceleration at equal DFR. Both comparisons must be stated with target limitations.
Mechanistic reason: incomplete NTT grants access to primes satisfying weaker root-of-unity congruence, which allows p to be smaller but then source DFR model changes via p. It does not itself provide independent low-noise/ciphertext-quality improvement at fixed p in published Eq.(1). Original linear-algebra formula and two-stage split do not evade p-sized automorphism-key memory; this cost can only be reduced by a genuinely DIFFERENT key/dataflow scheme, not by simple ell tuning, in this source setup.

## [FACT] Competing modern prior art, no cross-configuration speedup claims

Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security2026, https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao, source-vetted previously under PURE-FHE P0-PRESCOUT-10 in findings/pure-fhe-p0-amortboot-batchboot-sixbit-time-key-pareto-gate-2026-10-26.md. Official Table4 reports **different** algorithm/hardware/parameters: BatchBoot 8bit n4096 amortized 25.11ms/msg, nominal DFR 2^-62, displayed BSK 205.3MB, but not the whole set of keys or peak RSS, and not the 2^-128 DFR condition above. These two source numbers show a much faster contemporary research direction in incomparable settings, NOT a valid head-to-head speed/security comparison, nor a proof that 2025/696 is 'universally' worse or insecure. Also BatchBoot incorporates prior FFT-sharing, multibit CMux, and packing; those are prior art, not novel opportunities.
HasteBoots and Descent-PBS are separate recent achievements; do not borrow their results as if reviewed in this source.

## Novelty/candidate decision

PASS same-source throughput-versus-DFR numerical gate; FAIL H37 that 'free incomplete NTT' preserves fastest high precision 8bit 2^-128 DFR in author's actual table. The memory bottleneck and its p dependence remain material in the author's older approach but are acknowledged in its paper; no novel key compression, improved DFR or performance mechanism derived. It would be a mistake to launch Codex tuning old amortized NTT without security-matched contemporary baselines, a clear specific new dataflow, and an all-keys/peak-memory ledger.
RECOMMEND: PARK old 2025/696 as a direct paper idea. A next iteration MUST find a new FHE source-backed representational/keys/noise mechanism with author-grounded overhead and valid nearby prior art. Given repeated P0 failures, HUMAN_REVIEW/STAGNATION may be preferable to further low-value table or toy scans. Only the human PI can select official change of research direction.

END_OF_ITERATION
STATUS: PASS_8BIT_DFR_CONDITIONED_FRONTIER / FAIL_FAST_CONFIG_AT_2^-128 / NO_NOVEL_CRYPTO_MECHANISM
RESULT: at 8bit author's model fastest 584.7ms at 2^-9.3 vs sole reported ≤2^-128 case 1931.5ms at 2^-131.9 (~3.30x slowdown); free incomplete NTT is a modulus-feasibility lever, not a separate independent noise certificate; original source reports GB-scale automorphism key memory.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: stop this family absent a new mechanism capable of reducing p/auto-key overhead while retaining ≥128bit lattice security and DFR≤2^-128; compare with newer sublinear-memory alternatives only on matched parameters.
STATE_UPDATE: YES isolated PURE-FHE finding only; global STATE.md and all other track states unchanged.
CODEX_REQUIRED: NO; all engineering pending explicit PI approval.