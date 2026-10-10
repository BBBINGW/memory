# Iteration 61 — Revised CRYPTO 2025 Ring lookup CRT soundness: degree-four robustness and official-version limit

Date: 2026-10-10
Research target: Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286.
STATUS: **PASS** — I59–I60's polynomial identity soundness obstruction holds in a new exact parameter set with **N=8,d=4** and four finite-field CRT factors; not limited to the N=2,d=2 toy. **UNCLEAR** — official latest PDF byte identity could not be authenticated by current tools. Human/author review warranted; no deployed full-SNARK exploitation claimed.
NOVELTY STATUS: To be checked by authors; this is a structural issue in the *stated* scalar-table lookup/range PIOP, not an attack on ciphertext confidentiality.

## Read-before-write and one hypothesis
[FACT] Read current GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, parked RIG-HE STATE.md, I59 `findings/vfhe-crt-lookup-cross-component-soundness.md`, I60 `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`. Left those files and STATE.md unchanged. The 61st iteration does not open a new research direction.
[PRIMARY HYPOTHESIS — FALSIFIED] The CRT lookup inconsistency from I59/I60 may only arise in the small degree-two ring N=2 and disappear in the paper's proof-friendly incomplete-NTT **degree-four** structure or when using a larger exceptional set.
[FALSIFIER] One legal paper-style N=8,d=4 ring with required prime form, full factorization into extension fields of degree4, revised Theorem4.8 inequalities, illegal digit h and public v; legitimate Pi_decomp recomposition and fieldwise lookup grand-products glued to a **ring polynomial identity** for all challenges.
[CHEAPEST TEST] Independently construct a new N=8,d=4 CRT parameter point and check exact finite-field factorization plus 18-factor polynomial grand product. No code-level SNARK attack or FHE execution.

## Version and source provenance: separate results; do not conflate
[PRIMARY REVISED-TEXT CANDIDATE] Research MCP has full 52-physical-page text for ePrint 2025/286, source GitHub fixed mirror `https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf`, Git blob `a549654c5dffa3484e95e8244056f4a27c48c3e6`, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; 836746 bytes, version status VERSION_UNVERIFIED. Contains revised Theorem4.8 parameter restrictions and **Remark4.9**, which explicitly describes the earlier correction; Appendix E.2 physical p.48 still asserts false cross-CRT implication.
[CURRENT OFFICIAL LANDING] https://eprint.iacr.org/2025/286 official HTML confirms 2026-02-16 revision and note "Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements." The official PDF route https://eprint.iacr.org/2025/286.pdf as served to the web search renderer is a stale **50pp** crawl predating the official revision and must NEVER be used to verify the current corrected 52pp statement. The official "See all versions" action and fresh cache-busting PDF URLs errored in this run; direct fresh download likewise failed. Thus official latest SHA comparison remains **UNRESOLVED**. Revision metadata plus revised Remark4.9 in mirrored 52pp is strong but NOT byte-level authentication.
[SCOPING] The exact target is the 52pp MIRROR's §3.1 p.10, §4.3 pp.20–24 (Theorem4.8/Fig1/Remark4.9), Appendix E.2 pp.47–49, §5 p.25, Appendix D.3 pp.43–44. This iteration does NOT claim an independently acquired newer official author PDF.

## Completely independent legal d=4 counterexample
Take N=8,d=4 and two primes p0=29,p1=37 with `p_i=2a_i N/d+1=4a_i+1` for odd a_i=(7,9). Thus q=1073 and
 `R=Z_1073[X]/(X^8+1)`.
Exact irreducible factorizations:
 - mod 29: `X^8+1=(X^4+12)(X^4−12)`, both factors irreducible degree4.
 - mod 37: `X^8+1=(X^4+6)(X^4−6)`, both factors irreducible degree4.
Therefore `R ≅ F_(29^4)^2 × F_(37^4)^2` as required by incomplete-NTT proof-friendly §3.1.
Choose `B=beta=2, ell=1, nu=3, gamma=0, b=1, c=1`, hence `ell*=ell+nu+gamma=4`, `2^ell*=16<p_min=29` and `beta=2<p_min`: ALL revised Thm4.8 hypotheses satisfied.
CRT idempotents:
 `e0=407` corresponding to (1 mod29,0 mod37);
 `e1=667` corresponding to (0 mod29,1 mod37).
`e0+e1=1 mod1073`, `e0e1=0`, `e1^2=e1`, yet `e1=667 notin{0,1}` as a scalar ring element.
False public coefficient range witness:
 `v(0)=v(1)=e1`;
 common digit oracle `h(i,j)=e1` for `j=0` and zero for `j=1..7`, `i=0,1`, total 16 Boolean points.
The public v is NOT in the coefficient-range table `T_2=\{Σ_(j=0..7) a_j X^j : a_j∈\{0,1\}\}`, but `Pi_decomp` has a **TRUE** ring equation for all challenges:
 `v(i) = Σ_(j=0..7)h(i,j)X^j=e1`.
Every projected h digit lies in `{0,1}` in every individual finite-field factor.
For each p separately, simulate entirely honest scalar-table memory accesses with the projected digit sequence. Its projected transcript has a real multiset equality. CRT-glue the two fields' read_ts and final_cts:
 - field mod29: all 16 h digits=0; final counts (16,0).
 - field mod37: two h digits=1 and 14=0; final counts (14,2).
 - after CRT: `final_cts=[828,261]`; read_ts 16 elements from coefficientwise CRT glue (see executable script).
With `WS=(table entries,0)∪(h_t,read_t+1)`, `RS=(h_t,read_t)`, `Sfinal=(t,final_counts_t)`, the **R-valued multisets are NOT equal**. Their projections are individually equal for both primes (and hence their quartic factors). Nonetheless for the paper's factor `a+sigma*b−tau`,
 `G_WS(sigma,tau) = G_(RS∪Sfinal)(sigma,tau)`
as a complete polynomial identity in `R[sigma,tau]` (in fact in scalar `Z_1073[sigma,tau]`). Independent exact bivariate polynomial multiplication yields matching 65 nonzero monomials, total degree18. No random point sampling or floating-point comparisons.

## Exceptional set with 707281 legal challenges
Set `S={a0+a1 X+a2 X²+a3 X³ : each a_i in [0,28]}`, cardinality `29^4=707281`. For distinct elements, their difference has degree <4 and at least one nonzero coefficient mod29. Since coefficient differences lie in [-28,28], the difference is ALSO nonzero modulo37 (unless identical integers). In every degree4 irreducible quotient at both primes, a nonzero polynomial of degree<4 remains nonzero and thus invertible. Hence differences are units in R and S is a valid exceptional set. No need to enumerate 707281 choose2 pairs.
[BOUNDED SCALING] At arbitrary larger legal primes (e.g. both congruent5 mod8, choosing two distinct such primes), the same construction works with independent field memory traces; |S| grows as p_min^4. Thus acceptance1 is incompatible with the *asymptotic* O((2^ell*+2^(b/c))/|S|) soundness expectation, not a small-p constant issue. Do not claim actual security λ from this tiny exemplar.

## Reproducibility / result limits
[EXPERIMENT] Script executed without exception in current container:
 `/mnt/data/iteration61_vfhe_d4_crt_soundness_audit.py`
 SHA256 `ba58b94194f3aa8b3c89e9260e92a6aece892dbc29d940d2c0da9f2756bb3c97`
 stdout `/mnt/data/iteration61_vfhe_d4_crt_soundness_results.txt`
 SHA256 `5d970177cc837fe48c0ac8e9247c7a9ae680b765104e928f8641b08ab47e37c9`.
 The script verifies exact factorization, parameters, projection memory traces, false table membership, true decomposition, false original R-multiset equality, **exact** bivariate 18-factor grand-product identity. This is an independently built d=4 construction, not a transformed copy of the I59/I60 toy implementation.
[PAPER TEST BOUNDARY] The script does not implement all compiler messages, an actual polynomial commitment scheme, Fiat–Shamir, or real CKKS ciphertext computation; I60 already separately checked the oracle product-tree/sum-check checks for N=2. No deployed or practical end-to-end forgery claimed.
[CORE ERROR] Appendix E.2 false implication `ring h not in scalar t_beta => exists CRT field k where projected h not in projected t_beta` is invalid because CRT-wise rectangular digit closure strictly contains the diagonal table. Idempotence constraints cannot fix e1²=e1.
[REPAIR STATUS] Need enforce same integer digit/index across CRT components, perhaps a separate scalar-subring/index consistency argument; no proven low-overhead fix yet.
[DISCLOSURE] No email sent, no issue opened, no public disclosure. Human PI should approve any author contact only after independently fetching latest official PDF or confirming 52pp revised mirror bytes.

## End of Iteration 61
STATUS: PASS for parameter-robust d=4 algebraic soundness counterexample; UNCLEAR official latest version identity; HUMAN_REVIEW for author-reachout and downstream impact.
RESULT: Valid degree4 incomplete-NTT CRT ring R_1073 with four extension-field factors admits false range witness v=(667,667) but both PIOP subrelations can be satisfied, with 18-factor symbolic polynomial product equality and large exceptional set size707281. Upstream official landing revised2026-02-16; tool served older50pp vs revised-looking mirror52pp; current official byte identity not established.
NEXT_ACTION: Under PI approval, CONFIDENTIALLY ask corresponding authors to confirm whether the latest official 2026-02-16 version includes any omitted cross-component scalar index consistency check and whether its Theorem4.8/§4.3 claim accounts for CRT-inconsistent digits; cite both exact parameter witnesses (N2,d2 and N8,d4) and request authoritative PDF/hash. Otherwise first obtain authoritative official PDF bytes without incorrectly claiming verification; no further toy variants.
STATE_UPDATE: NO — parked RIG-HE STATE.md unchanged.
