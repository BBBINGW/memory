# Iteration 190 — FHEW Adaptive Key Update: Gaussian-key DFR parameter table versus final ModSwitch variance

**Date:** 2026-10-14 JST. One human-authorized research iteration. Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md at SHA `133a6002e8046086156f44505f14d4ab643449a5`, I189 archive and branch index. On PI assent recommend PARK the trivial LFBS packing/hoisting I188–189 branch; parent packing problem not proved impossible. One new primary falsifiable claim and one cheapest decisive model-internal noise variance lower-bound check; no full ciphertext simulation, no author contact.

## Original primary paper [FACT]

Qi Zhang, Mingqiang Wang and Xiaopeng Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, IACR ePrint **2025/381**, https://eprint.iacr.org/2025/381, **27 physical pages**. Read full original via Research MCP mirror PDF SHA256 `bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf`; source_kind github-mirror, official latest binary **VERSION_UNVERIFIED**. Also independently opened official ePrint PDF https://eprint.iacr.org/2025/381.pdf, web PDF ref `turn309630view0`, section §5.1 p19 (web p18, lines1364–1435) and Table3 physical p21 (web p20 lines1456–1479). Attempt to view web PDF screenshot physical p19 returned **cache miss**. Thus the exact glyphs of source sqrt and erf denominator could not be visually rechecked, though web PDF text and Research MCP extraction independently agree. No PDF screenshot parity claimed.

**Source §5.1/Table2** for Gaussian-key methods: n=447, q=1024, RLWE ring N=1024, Q=2^28, Qks=2^14, Gaussian parameter σ=3.19 (listed as secret-key Gaussian standard deviation), and the paper's Gaussian norm substitution `||s||₂ = sqrt(n σ²)`. Window size w=10 for Algorithm5, w=5 for Algorithm6. Paper explicitly targets DFR less than 2^-32.

**Source §5.1 error model** (extract legible in both sources):
```
 β² = (q²/Qks²) [ (Qks²/Q²)σacc² + σms1² + σks² ] + σms2².
 σms2² = (||s||₂² + 1)/12.
```
Source treats the refreshed NAND gate's maximum noise standard deviation as `sqrt(2)β`, failure threshold as q/8, and writes
```
 P_fail_model = 1−erf( (q/8)/(2β) ) = erfc( (q/8)/(2β) ).
```
**Table3 p21** reports LMKC+ DFR2^-34, LLWW+2^-35, authors' Algorithm5 2^-37, Algorithm6 2^-36; source Algorithm6 reports 77 RLWE key switchings, 30.41ms bootstrapping and 257.07MB keys vs LLWW+ 301 switches, 38.38ms, 110.41MB. These observed runtimes and cryptographic 128-bit *hardness estimates* are not challenged by this numerical check.

## ONE primary hypothesis and decisive test

**[HYPOTHESIS to falsify]** For authors' specified Gaussian-key parameter choice and §5.1 Gaussian/noise approximation, the **reported DFR2^-36** for Algorithm6 (and required <2^-32) can be numerically obtained from the stated beta-variance equation, even with normal source assumptions.

**[Cheap FALSIFIER]** Omit *all* positive error contributions except the FINAL q modulus switching term σms2²; that gives an unrealistically favorable **lower bound** on beta and modeled DFR, if their own independent nonnegative variance-sum formula is used. If this minimum modeled DFR already exceeds the reported table, no positive choices of preceding error variances can reconcile the table with the stated formula.

### Exact arithmetic + numerical tail [DERIVATION]

At n447, Gaussian std σ3.19 (source's direct norm estimate):
```
 ||s||₂² = 447*(3.19)² = 4548.7167;
 σms2²=(4548.7167+1)/12 =379.14305833333333;
 β²≥379.14305833333333; β≥19.471596193772438;
 q/8=1024/8=128;
 P_fail_model≥erfc(128/(2 sqrt(379.1430583)))
             =erfc(3.2868389095121535)
             =3.346946255388498·10^-6 ≈ 2^-18.18872.
```
Compare Table3 Algorithm6 `2^-36≈1.4551915228366852e-11` (lower bound/report ratio **230,000.4**); target `2^-32≈2.3283064365386963e-10` (ratio **14,375.0**). Algorithm5's `2^-37` is also below this floor for same n,σ,q if formula used identically. Reverse check:
```
 To achieve P_fail ≤ 2^-36 under P=erfc(128/(2β)),
 β≤ 13.4042714644, β²≤179.674..., and 
 ||s||₂² ≤12 β²−1 ≈2155.094 (even with other variance terms zero).
```
But paper's Gaussian norm estimate is4548.72; contradiction under source arithmetic.

**Robustness to visual-glyph uncertainty:** If, hypothetically, failure were instead modeled as `erfc(128/(sqrt(2)β))` (standard deviation β vs source text's sqrt2β), the same final-modswitch term forces `P_fail≥4.9087387196e-11≈2^-34.24586`, still *above reported Algorithm5 2^-37 and Algorithm6 2^-36*, though not above the <2^-32 target. This alternate formula is NOT claimed to be the original source. Both computations used scipy.special.erfc and erfcinv; no ciphertext execution.

## Scientific boundaries, priorities, uncertainty

**[FAIL internal model/table numeric consistency]** Under the source **as extracted**, the Gaussian method's norm and mandatory final modulus-switching variance alone cannot produce the claimed modeled per-gate DFR2^-36 (or <2^-32 with the displayed sqrt2β NAND factor). This is a concrete potential correctness-margin modeling/parameter inconsistency, not merely "Gaussian key norm random"; indeed source uses a mean/typical `||s||²=nσ²` instead of a per-key tail bound, which is a SEPARATE unresolved question.

**[UNCLEAR real scheme]** This does **not** prove the deployed implementation fails with probability 2^-18: source's Gaussian/independent-noise model might be an approximation or contain normalization/standard deviation notation not faithfully represented by extracted formula; the OpenFHE implementation may sample a different final LWE key, define σ=3.19 differently, use distinct modulus-switch rounding correlations, or contain an omitted scaling factor. The official PDF rendered formula and code must be checked before proclaiming an author error or cryptographic break. A 128-bit security claim and 2^-32 DFR are distinct properties. No evidence on actual algorithm's speed/size or 128-bit lattice hardness contradicted.

**[NO original protocol improvement yet]** This is a substantially more concrete source-specific TECHNICAL AUDIT than a toy false optimization, but alone is not a new FHE algorithm, a confirmed erratum or a publishable contribution. Require independent implementation/parameter replication and source version check.

## End of Iteration 190

**STATUS:** FAIL consistency of source §5.1 Gaussian secret variance substitution, Table2 parameters, and Table3 quoted Algorithm6 DFR under extracted formula; PASS exact necessary nonnegative-variance floor and high-precision Gaussian erfc bound; UNCLEAR rendered formula and code normalization / actual DFR.
**RESULT:** β≥19.4716 from final ModSwitch alone; under extracted paper formula `P_fail≥3.34695e-6≈2^-18.19`, about230000 times reported Algorithm6 2^-36. Need check PDF equation glyph and OpenFHE secret/noise setup before declaring a real correctness defect.
**NEXT_ACTION:** I191 NOT STARTED, HUMAN_REVIEW/conditional CONTINUE: verify official rendered §5.1 DFR expression and implementation Gaussian secret sigma conventions and final ModSwitch normalization; reproduce FULL β calculation with code-author parameter values, then if discrepancy persists reselect parameters meeting actual <2^-32 and check whether matched DFR security performance improvement remains. If source reveals a missing factor/notation mistake, correct archive promptly.
**STATE_UPDATE:** YES: concrete source-specific high-value noise/correctness parameter gate; exact necessary bound and experiment need.
