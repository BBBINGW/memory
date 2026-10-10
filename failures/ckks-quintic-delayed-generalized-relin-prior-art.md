# Iteration 48 — Prior-art falsification of "combine unrelinearized polynomial terms, then key-switch once"

Date: 2026-10-10
Branch: CKKS generalized relinearization for high-precision bit-cleaning polynomial evaluation.
STATUS: FAIL — **novelty of deferred polynomial-sum relinearization as a standalone technique**.
IMPORTANT: We have NOT proven the exact quintic cleaning implementation/CKKS precision and/or the complete generalized-s^2..s^5 key schedule appear verbatim in any prior paper. Rather, both *the underlying optimization mechanism* and *its higher-degree use* have strong published prior art, so the candidate cannot be represented as independently new.
No implementation or RNS noise experiment was warranted after this inexpensive decisive check.

## Read-before-write / state
[FACT] Read latest GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and I47 failure `failures/ckks-quintic-generalized-relin-single-key-cost.md` before this iteration. RIG-HE parked STATE.md belongs to a separate direction and is unchanged.
[FACT / PREVIOUS BASELINE] Choe, Kim, Stehlé and Suvanto, *Leveraging Discrete CKKS to Bootstrap in High Precision*, CCS 2025, ePrint 2025/1786, §4.2 physical p.11 (full cached 15-page PDF, SHA256 3d1e2277a4a64de6094094c86a941f95374528be50fea611847927d8a68b4230, VERSION_UNVERIFIED) proposes `ct_j = Δ^(k-j) Relin(ct^(⊗j))` for generic integer-coefficient polynomial evaluation. I47 studied a quintic H(x)=10x³−15x⁴+6x⁵: separate direct degree3/4/5 generalized relinearizations need (2+3+4)=9 nominal gadget products, while first combining full unrelinearized polynomial ciphertext terms into one degree5 ciphertext then performing ONE generalized switch would need 4 nominal gadgets, but still uses four independent s²..s⁵ keys in a conventional representation. The possible scheduling saving from 9 to 4 was a tentative research idea, not a validated FHE/noise gain.

## One primary falsifiable hypothesis / test
[HYPOTHESIS — FALSIFIED at technique-novelty level] Taking an RLWE/CKKS polynomial's unrelinearized ciphertext terms, forming linear combinations of their different secret-key degrees, and postponing relinearization until after the combination to reduce key-switch operations, is not already covered by published polynomial-evaluation techniques.
[FALSIFIER] Find a prior publication explicitly evaluating polynomial combinations BEFORE relinearizing and explaining the resulting reduction in relinearization count; ideally also find prior work using ciphertext secret-key degrees >2 with larger switching key material.
[MINIMAL TEST] Targeted prior-art search; fetch/re-read the original full-text primary source and locate exact statement/algorithm. Do NOT execute RNS noise tests or HEaaN benchmark unless novelty survives.

## First exact primary prior art — fully read
[FACT / PRIMARY FULL TEXT] Yongwoo Lee, Joon-Woo Lee, Young-Sik Kim, Yongjune Kim, Jong-Seon No and HyungChul Kang, *High-Precision Bootstrapping for Approximate Homomorphic Encryption by Error Variance Minimization*, EUROCRYPT 2022, IACR ePrint **2020/1549**. Research MCP fetched original full 29-physical-page PDF from GitHub mirror, PDF SHA256 `de0b86f567bdf213d833f23c4cb8b69fcdeb6ec69eea33e47277eab964117735`, VERSION_UNVERIFIED.
- §5.2, Algorithm 2 (Lazy-BSGS), physical p.17: SetupLazy/GiantStepLazy relinearize at selected points, *not after every operation*; after evaluating a polynomial chunk BabyStep, GiantStepLazy first relinearizes `ctq` when it is needed for the next ciphertext multiplication.
- §5.2 physical p.18 explicitly observes that ciphertext plaintext additions, ciphertext additions and scalar multiplication can be done *before relinearization* of a degree2 three-component ciphertext; describes addition `(d0,d1,d2)+(b,a)=(d0+b,d1+a,d2)`. Explains delayed relinearization lowers key-switch count and reduces evaluation error; warns matched scales needed before adding.
- §5.2 physical p.19: `BabyStep` combines plaintext-coefficient Chebyshev terms without relinearizing, returning a three-component ciphertext; relinearization occurs only later when a giant-step multiplication needs it. Provides exact complexity and shows 711-degree example: 33 relins instead of larger baseline.
=> The fundamental "sum first, relinearize later" mechanism was explicitly published in CKKS bootstrapping years before the current candidate. This 2022 approach principally holds degree ≤2 ciphertexts; it does **not alone** prove published quintic direct generalized Relin.

## Second important publication — high-degree lazy relinearization (author technical account)
[FACT / AUTHOR EXPLANATION, NOT FULL ACM PDF] Qingfeng Wang and Li-Ping Wang, *A Novel Asymmetric BSGS Polynomial Evaluation Algorithm under Homomorphic Encryption*, ASIACCS 2025 (conference Aug 25–29, 2025; pp.30–44), DOI `10.1145/3708821.3710822`. Author Qingfeng Wang's dated technical explanation https://ckks.org/blog/2025/asymmetric-BSGS-algorithm/ (Nov 3 2025), especially §3.2:
- Describes unrelinearized ciphertext polynomials in the secret variable of degree up to small parameter `t` and explicitly **postpones all relinearizations until after evaluating polynomial chunks** `y_j=f^(j)(x)`, using a larger key-switching key.
- Explains delayed level-modswitch/relin and higher-degree ciphertexts as the mechanism for reducing cost within asymmetric BSGS.
- Conference publication and authors verified independently by ASIACCS accepted-paper list, DBLP and DOI.
- **CAVEAT** The ACM full PDF was not acquired/read. The technical mechanism is grounded in the author-written explanation and publication metadata, not a paper theorem/pseudocode checked line-by-line. Do not cite a made-up theorem or assert specific parameter conditions from unviewed ACM text.
=> High-degree delayed relinearization with larger evaluation key material is also known prior art. This is substantially closer to I47's generalized degree5 idea than the older degree2-only lazy-BSGS case.

[ADDITIONAL CONTEXT, NOT NECESSARY TO FALSIFY] Wang et al., *Leveraging Tree-based BSGS and Lazy Relinearization for Efficient Homomorphic Evaluation of Bivariate Functions in BFV*, Journal of Information Processing 34:775–784 (published Sep 15 2026), DOI 10.2197/ipsjjip.34.775, is later cross-scheme evidence of a continuing established research line but not an identical CKKS high-precision cleaner. Do not use it as proof of a specific quintic technique.

## Core distinction and residual limitations
[DERIVATION] In the idealized secret-polynomial representation, degree-D ciphertexts `C_j(s)` may be embedded/padded to common degree D and added with aligned scales before one generalized relinearization. Therefore plaintext algebra permits
  `C_raw(s)=10Δ²ct(s)^3−15Δ ct(s)^4+6ct(s)^5`
as a single degree5 encrypted polynomial; switching s²,...,s⁵ once each would perform 4 gadget products, versus 2+3+4=9 if doing separate generalized relins. The arithmetic schedule saving is elementary once this representation is available.

[CRITICAL LIMIT] Real gadget key switching is *not exact coefficient-linear in its error*: digit decomposition, carry/rounding and key-switch noise differ when switching a sum versus switching individual terms. Nor does summing first eliminate s³,s⁴,s⁵ key material. The plaintext equality does not imply equal error, modulus consumption or security. Two thrifty cubics have fourth-order ideal bit-accuracy versus a single quintic third order, so prior raw 9/4 vs cubic 4 counts are not matched-precision comparisons.
[PRIOR ART SCOPE] First primary source establishes general add-before-relin for degree≤2; second author account establishes higher-degree delayed generalized key switching for polynomial evaluation. Neither source was verified to perform the *exact* quintic smootherstep in Choe et al.'s special no-rescale high-precision bit-cleaning model. Specific matched-precision key/noise/latency Pareto improvement remains OPEN — but there is no new nontrivial mechanism or supporting FHE implementation at present. It is not justified to position simple deferred relinearization as a contribution.
[NOVELTY JUDGMENT] Standalone deferred generalized relinearization: FAIL / ALREADY KNOWN; special quintic application novelty NOT VERIFIED and unlikely strong without an entirely new secret-power-key compression or actual cost-bound improvement. Do not keep this branch alive by multiplying toy examples.

## Outcome / next step
STATUS: FAIL (standalone lazy/direct-generalized relinearization schedule novelty).
RESULT: Retrieved EUROCRYPT 2022 ePrint 2020/1549, §5.2 physical pp.17–19, and independently located ASIACCS 2025 author explanation explicitly delaying relins of ciphertexts with degree up to t. This decisively weakens I47's proposed 9→4 gadget-product scheduling as a novel contribution. No new CKKS algorithm or exploit claimed.
NEXT_ACTION: ARCHIVE I46–I48 generalized quintic cleaning schedule as low-priority/known technique. Next independent iteration should inspect ONE *different*, full-text-accessible FHE construction-level bottleneck with a precise falsifiable technical change (e.g., ePrint 2024/1014 Grafting §3–4 and its actual rescaling/noise boundary). First locate and read the relevant Lemma/Algorithm via Research MCP before proposing a replacement; do not revisit lazy-Relin scheduling without a genuinely new mechanism.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md remains unchanged.
