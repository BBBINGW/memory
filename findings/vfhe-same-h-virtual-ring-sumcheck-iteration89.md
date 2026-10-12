# Iteration 89 — Reuse original h PCS through a virtual-ring sumcheck

Date: 2026-10-12. Active: Cascudo et al., CRYPTO 2025, ePrint 2025/286, cross-CRT digit-coherence repair.
STATUS: PASS (PIOP-level interface compatibility); OPEN (complete SNARK security, privacy, concrete cost and parameter feasibility). No new SNARK, no forgery, no novelty claim, no contact/disclosure.

## Read before write and source
Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md (I88 next I89), I88 and I86 archives.
Read full primary ePrint 2025/286 52pp mirror via Research MCP: SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, current official binary VERSION_UNVERIFIED.
[FACT] §2.2 physical pp8–9 defines virtual oracles with point queries computed from constituent oracles; Πsum reduces sum to a terminal point query, Thm2.6 error d*l/|S| for individual degree d and l variables over exceptional S.
[FACT] §4.3 p21 Πrange uses SAME h oracle for Πdecomp and Πbeta-range. §4.3 pp20–24 original h digits must lie in diagonal scalar table, but current proof guarantees only componentwise table (I59–70). §5 p25/Appendix F componentwise CRT PCS; Appendix D.3 p43–44 oracle queries compile to evaluation value+proof for same polynomial commitment.

## One precise hypothesis and cheapest test
Under I88's STRICT extra bound T=m*(beta−1)<pmin and scalar-digit component table validity, one new native Πsum of the virtual product alpha~*h~ should certify a public A as the same-h Boolean masked aggregate over Rq without a separately committed integer digit vector or product polynomial commitment.
Falsifier: source Πsum cannot use a virtual oracle h*public alpha, terminal query requires newly committed h, source challenge order incompatible with prebinding h, or sumcheck polynomials require unsupported degree.
Test: derive an exact source-faithful transcript and check a 2-variable example in R_(29*37).

## Derivation: one virtual oracle, no new digit commitment
1. P publishes/locks the original Πrange h polynomial commitment C_h *before* mask.
2. V samples public Boolean mask alpha on Boolean^l; P responds with a canonical ordinary integer A, 0<=A<=T. All field factors must see the same embedded A*1_Rq. Neither arbitrary CRT ring A nor an external b-vector is allowed.
3. Define virtual oracle g(X)=alpha~(X)*h~(X). Since both are multilinear, individual degree <=2.
4. Run source Πsum on claimed Σ_(x in Boolean^l)g(x)=A*1_Rq. At each of l rounds P sends a univariate degree<=2 sum polynomial; V checks recurrence and samples r_j from an exceptional set S⊂Rq.
5. Terminal query: V uses the ORIGINAL C_h's VerEval to authenticate h~(r), evaluates public alpha~(r), checks g_l(r_l)=alpha~(r)*h~(r). No independently committed product g or external b-vector is needed.
6. Check that Πdecomp, Πbeta-range, and the appended Πaggregate all reference exactly C_h; protect commitment-first mask challenge and later sumcheck randomness in Fiat–Shamir transcript with separation.
[DERIVED] For fixed h, source Πsum error <= 2*l/|S| at the oracle level. Compilation adds PCS and original lookup knowledge-soundness errors. Bound T<pmin turns authenticated native field equalities into literal integer sum equality across CRT factors (I88). For fixed inconsistent pre-bound field digit arrays, uniform Bernoulli masks detect mismatch with >=1/2 per round, but the TOTAL soundness needs combining detection, sumcheck, PCS, and CRT lookup errors under an actual interactive/FS compiler. A public arbitrary Boolean mask's alpha~(r) evaluation costs O(m) naively; rank-one masks from I87 permit O(sqrt m) evaluation but 309 repetitions for raw 128-bit sampling bound.

## Exact elementary test (NOT actual cryptographic proof)
Code: /mnt/data/iteration89_vfhe_same_oracle_sumcheck.py SHA256 d36306702f9543b55c044321795eb837211c9f12bb2e9bff143fc7d293b6c41f.
Result JSON: /mnt/data/iteration89_vfhe_same_oracle_sumcheck_results.json SHA256 788531ad084a1e8c876a95f239c51cbd6ef1cacf30dbcbda7f2db581732e5633.
Take R=Z_1073, p29,p37, m4, beta2, T4<29, h=(1,0,1,0) on (00,01,10,11), alpha=(1,1,0,0) from u=(1,0),v=(1,1). h~(X,Y)=1-Y and alpha~(X,Y)=1-X. Claimed A=1. In R:
  g1(X)=1-X, so g1(0)+g1(1)=1=A;
  challenge r1=2, g1(2)=-1;
  g2(Y)=Y-1, so g2(0)+g2(1)=-1;
  challenge r2=3, g2(3)=2;
  terminal h~(2,3)=-2, alpha~(2,3)=-1, product=2, PASS.
Adversarial CRT-mixed candidate h=(CRT(1 mod29,0 mod37),0,1,0) with CRT scalar 407 has native actual aggregates 1 and0; sum in R is 407, not equal to any canonical A∈[0,4]. Exhaustive all 16x16 binary digit vector pairs for same alpha confirm bounded A exists iff sums equal. These are virtual ring evaluations, not a real commitment or probabilistic SNARK security experiment.

## Status boundary and next cheapest falsifier
[PASS] Source §2.2 explicitly accommodates products via virtual oracle, so a native Πsum terminating in original h PCS opening is interface-compatible; I86's impossibility of converting ONE h point opening to arbitrary A is NOT contradicted: the extra interactive sumcheck supplies the missing authenticated relation.
[OPEN] Check parameter viability: original Thm4.8 only requires beta<pmin and m<pmin; needed T=m(beta−1)<pmin may or may not hold at actual §6 instances. For many published settings c, beta, N and m require exact audit; if impossible, this public-A branch is not practical.
[OPEN] Public A exposure to verifier/server-model privacy, full VC IND-CPA under verification oracle, sumcheck/PCS domain binding, adaptive FS reductions, 128-bit aggregate sampling cost and source-vs-modified PIOP proof remain unproven.
NEXT_ACTION (I90): Read primary §6 parameter choices (including N, digit base b/c, c, total h oracle length m=2^ell*N*c) and original range-oracle aggregation in §4.1. Test ONE real/paper-parameter instance for T=m(beta−1)<pmin and note prover/verifier cost ratio if bound fails or passes. Prefer direct falsification before building a compiler. No author contact.
STATE_UPDATE: YES (explicit source-compatible virtual sumcheck closes the missing interface at ideal PIOP level; cost/security still open).
