# PURE-FHE · P0-PRESCOUT-19 — Global Prefix A2B Precision / September 2026 Prior Art Gate

Date: 2026-10-26 Asia/Hong_Kong
TRACK_ID: PURE-FHE
PREVIOUS: P0-PRESCOUT-18
STAGE: P0_PRESCOUT_19
RESULT: FAIL_FIXED_PRECISION_DIRECT_PREFIX_LUT; HIGH_PRIOR_ART_RISK
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN
OTHER_TRACKS: UNCHANGED

## [FACT] Baseline original and update

Gao–Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, CRYPTO 2026, ePrint 2026/233. Original paper PDF cached mirror version unverified (SHA256 f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92); original p15–16 Def.10-11 and Thm1 give the triangle encoding, pre-evaluation coefficient rounding, quotient identity; original pp21–23 §5.2 describe iterative n/w block A2B with batch amortization. Original §9 p30 explicitly asks for non-amortized O(1) A2B.

Author's blog July 27 2026 https://ckks.org/blog/2026/fhe-simd-alu/ explicitly says more direct A2B conversion methods are to be discussed separately; SNU seminar June 11 2026 https://cse.snu.ac.kr/en/community/seminar/1126 reports 2–3 CKKS bootstraps and unspecified new results. This warned of imminent followup.

NEW crucial September 2026 ePrint entries confirmed against public ePrint indexes, titles and author names:
- ePrint 2026/1836, Yuchen Wei, Kaisheng Ma, Mingyu Gao, Hongren Zheng, *FHE for ALU over Large Prime Moduli and Application to One-Round Threshold ECDSA* https://eprint.iacr.org/2026/1836. A third-party summary (Homomorphic Privacy, September 14 2026 https://homomorphicprivacy.com/articles/gao-zheng-single-ciphertext-conversion/) states it achieves single-ciphertext triangle-to-discrete CKKS A2B with O(1) bootstraps but O(log n) extra levels. THIS COMPLEXITY IS SECONDARY-REPORT-LEVEL, NOT VERIFIED FROM ORIGINAL.
- ePrint 2026/1840, Xuan Shen, Zhihao Li, Ruida Wang, Xianhui Lu, *Efficient Homomorphic Arithmetic Logical Units with O(1) Bootstrapping*, https://eprint.iacr.org/2026/1840. Title/author publication metadata verified; secondary summary reports OpenFHE improvement over Gao–Zheng in 64/128/256-bit configurations. Specific circuit, proof, performance figures not verified.
- ePrint 2026/1869, Jiaming Liu, Shihe Ma, Anyu Wang, Xiaoyun Wang, *High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping*, https://eprint.iacr.org/2026/1869. Title/author verified. No formal algorithm or comparable complexity inferred beyond title.
All three original PDFs are RETRIEVAL_BLOCKED: eprint 403, exact arXiv retrieval unavailable, ePrint mirror absent. DO NOT CLAIM original papers were read or open problem has definitively been solved in an exact baseline-comparable cost metric without these originals. For future stage, user may supply authorized original under papers/supplied/. Do not silently edit existing MISSING_SOURCES.md because read_repo_file returns empty.

## One primary falsifiable hypothesis H19

For the canonical global weighted-prefix A2B extraction from the normalized rounded coefficient vector Y=(X-2)I+[m]_t, after one linear transform, a single per-output small-alphabet D-CKKS LUT with constant input-resolution / scale independent of machine-word width n can recover every bit b_j exactly, with no block iterations and uniformly bounded additive input error eta>0.

## [DERIVATION] Exact prefix correctness, then worst-case boundary collision

Let A=Z[X]/(X^n−X+2), t=X−2, [m]_t=Σ_{i=0}^{n−1} b_i X^i. Y=tI+[m]_t=ΣY_iX^i. Since f(2)=2^n, evaluation at X=2 modulo 2^n is a ring homomorphism and Y(2)=m mod2^n. For each 0≤j<n,
 S_j=Σ_{i=0}^j 2^iY_i ≡ m (mod 2^{j+1}).
Therefore b_j=floor((S_j mod2^{j+1})/2^j) (nonnegative residue), or b_j=floor(T_j) mod2 with T_j=S_j/2^j (for ideal integer coefficients and with usual floor).

Take I=0 and two valid messages m_A=2^j−1 and m_B=2^j, n≥j+1. Their target bit b_j differs 0 vs1, but
 T_j(A)=1−2^(−j), T_j(B)=1.
So normalized prefix values are only 2^(−j) apart. Under adversarial additive perturbation |error|≤eta the two measurement intervals overlap whenever eta≥2^(−j−1). Consequently deterministic guaranteed recovery of high bit requires eta<2^(−j−1). For n=64, j=63 requires eta<2^(−64) ≈5.42e−20. With a normalized noise/rounding scale of ~2^−43 (merely a conditional comparison to Gao–Zheng's approx 43-bit experiment scaling; not a measurement of actual transformed error), separation 2^−63 is 2^20 times smaller; naïve 43-bit precision cannot guarantee this direct scalar threshold test.

On the other extreme, direct unnormalized S_j from I=0 ranges across up to 2^(j+1) distinct low-bit residues; a direct full-residue look-up indexed by S_j mod2^(j+1) has exponential alphabet, unless a further structurally different compressed/split transform is provided. This is NOT a lower bound for all possible A2B algorithms, clever LUTs, or high-level FHE circuits; it applies to this specific raw-prefix lookup vs normalized-prefix scalar design.

The exact m_A/m_B test was evaluated with rational arithmetic at j=3,7,15,31,63; all gaps equal 2^-j. The result is independent of unspecified I distributions because I=0 is in the hypothesized domain.

## [DERIVATION] Structural caution

t=X−2 is invertible over the real auxiliary algebra A_R=R[X]/(X^n−X+2); otherwise triangle t^{-1} encoding would not exist. Therefore no nonzero *real-linear functional* can annihilate the entire real image of multiplication by t, as that image is the whole space. Integer overflow is removed by a modular/nonlinear contract, not a free continuous linear projection. This observation does not obstruct elimination modulo 2^n or more complex arithmetic constructions.

## Novelty assessment, deployment

The primitive nonamortized constant-bootstrap goal is already strongly contested by 2026/1836 and 2026/1840, with another adjacent 2026/1869. Put triangle ALU in SOURCE_VERIFICATION_REQUIRED/PARK, no Codex. If author PDF confirms the 1836 conversion method, next research must instead specify a different cost metric and strictly demonstrate improvement on total level/noise/latency/full evaluation key at matched security and use-case.

NEXT_TEST: VERIFY_2026_ALU_CONSTANT_BOOTSTRAP_PRIMARY_SOURCE_GAP, or select a fresh author-explicit unsolved FHE mechanism beyond the crowded ALU once primary source bottleneck is logged. Keep one primary hypothesis and one cheapest decisive test; do not continue ad hoc bit-local optimizations.

END_OF_ITERATION:
STATUS: FAIL_DIRECT_GLOBAL_PREFIX_FIXED_PRECISION
RESULT: PASS_EXACT_GAP_COUNTEREXAMPLE; HIGH_PRIOR_ART_RISK
NEXT_TEST: PRIMARY_2026_ALU_PRIOR_ART_SOURCE_GATE
STATE_UPDATE: YES — isolated finding only
