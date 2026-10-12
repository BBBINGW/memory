# Iteration 91 — Batch all post-commit Boolean masked-digit aggregate claims into ONE native ring sumcheck / PCS opening

Date: 2026-10-12
Active vFHE repair: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286.
**STATUS: FAIL** naive premise that t independent mask checks necessarily require t native ring sumchecks/t original-h PCS evaluation openings; **PASS CONDITIONAL** batching lemma gives one degree-2 ring sumcheck and one new same-h ring evaluation, plus O(t) announced public integers and mask evaluation work. **UNCLEAR** end-to-end soundness/FIat–Shamir/privacy/concrete verification speed and novelty. No author contact, disclosure, implementation of full PIOP, or original protocol forgery.

## Read-before-write and direct source evidence
Read AGENT.md, RESEARCH_PHILOSOPHY.md, current STATE.md (I90 next I91), I87 and I90 finding. Read cached complete primary ePrint 2025/286 via connected Research MCP, PDF SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, latest official PDF VERSION_UNVERIFIED.
[FACT] §2.2 physical p8 Definition2.1 exceptional S⊂Rq: distinct elements have UNIT differences; p9 Πsum reduces Boolean sum of individual-degree d polynomial to one terminal evaluation; Thm2.6 error d*l/|S|.
[FACT] §4.3 p24 Πrange verifier makes 25 ring-oracle queries, q=25, with O(ell+nu+gamma+b/c) PIOP work. Table2 physical p27 shows for D depth: Πrange 3D sumchecks, 7D commitments, 25D evaluation proofs (D=1 baseline q25 in author's summarized row). The 25 includes *multiple source oracle identities*, not all accesses to h.
[FACT] §5 p25 and Appendix F.1 p50: one Rq polynomial evaluation entails verifying ALL μ CRT finite-field component PCS openings, NOT one cheap single-prime proof. §5 p26 and Appendix F.2 p51: repeat evaluations against the same Brakedown PCS commitment may REUSE its testing phase once, but have an evaluation phase at each distinct point. The source does not claim full free reuse of the evaluation phase.
[FACT/INTERPRETATION] Source §6.3 p29 Medium circuit (W,D,L,N,c)=(1,1,3,8192,5), d4, 49-bit RNS, '20-bit lookup table'; published maximum range input 286720 ring elements; I90 used padded envelope M=2^19=524288 (mathematical conservative capacity, not an asserted author MLE layout). Source's c=5 example versus formal c=2^gamma digit decomposition in §4.3 remains UNVERIFIED; β≤2^20 conditional interpretation. All t-counts below assume this padded M and a SAME-h oracle.
[FACT] §2.2 p8 virtual oracles permit composing polynomials from already committed constituents; h is shared in §4.3 p21, and Appendix D.3 p43–44 compiles point openings to PCS proofs.

## ONE hypothesis and cheap decisive falsifier
[HYPOTHESIS — FAIL] The I88/89 public-A consistency repair is fatally expensive at original-PCS opening count because t=128 independent full Bernoulli masks (I78) or t=309 independent rank-one Bernoulli masks (I87) must each incur ONE separate Πsum and ONE new opening of original h, i.e. 128/309 EXTRA ring PCS evaluations besides original 25D, necessarily losing succinctness.
[FALSIFIER / TEST] Inspect Appendix F.2 test-phase reuse and derive ONE sound random-linear-combination of t masked aggregate CLAIMS after A_i fixed, using the same virtual `h~` oracle. Test linear-combination soundness over a genuinely composite ring with zero divisors. Count additional evaluations/rounds in naive and batched interfaces, not clock time.

## Naive sequential interface costs
Let m=M=2^19, ell=19 variables. To obtain standalone miss probability ≤2^-128, t_full=128 since any precommitted discrepancy detected with prob≥1/2/full Boolean mask, and t_rank=ceil(128/log2(4/3))=309 since rank-one detected ≥1/4. These are ONLY mask-detection probabilities, not complete VC knowledge-soundness parameter choices.
If each check is an independent source Πsum of degree≤2 over ell=19 variables:
- full: 128*19=2432 added sumcheck variable-rounds, 128 terminal ring evaluations, 25+128=153 ring evaluation claims for baseline D1;
- rank-one: 309*19=5871 rounds, 309 terminal ring evaluations, 25+309=334 D1 claims.
Even though the same h commitment and Brakedown testing phase can be reused, F.2 ordinarily retains an evaluation phase for each different queried h~(r_i). Each ring evaluation is a μ-field PC evaluation family, and costs are source-parameter dependent. NO claim that 25D baseline alone contains all CKKS application proof work.

## Batched native ring sumcheck derivation (OUR modification)
1. Lock original h polynomial commitment(s) C_h and requisite prover oracle material BEFORE mask challenges. Verifier samples t independent public Bernoulli mask vectors α^(i) (full or rank-one).
2. AFTER α^(i), prover announces **ordinary bounded canonical integers** A_i∈[0,T] with T=m(β−1)<p_min (I88), and transcript commits to all A_i. No separate committed integer vector is introduced.
3. ONLY AFTER ALL A_i FIXED, verifier samples independently ρ_i∈S, an exceptional set in Rq with pairwise UNIT differences.
4. Define public virtual polynomial F(X)=Σ_i ρ_i α~^(i)(X), and public ring claim Y=Σ_i ρ_i A_i*1_Rq. F is multilinear (linear combination of multilinear masks). g(X)=F(X)*h~(X) has individual degree≤2.
5. Run ONE native Πsum over ell variables to prove Σ_(x∈{0,1}^ell) g(x)=Y. Terminal evaluator computes F(r) publicly and invokes original C_h VerEval for exactly ONE NEW ring point evaluation h~(r). NO new product PCS and NO t repeated h point-opening proofs.
6. Source Appendix D.3 compilation is only a potential compilation interface; binding order, Fiat-Shamir domain separation and full knowledge-soundness need a NEW formal proof. As a PIOP-style test this is directly compatible with the source virtual-oracle sumcheck.

## Composite-ring batching soundness lemma
Let E_i=Σ_x α^(i)(x)h(x)−A_i*1_Rq. For fixed h, masks and **all A_i already fixed** before ρ_i sampling, if some E_j ≠0 in Rq, condition on ρ_i for i≠j. Two distinct ρ_j,ρ'_j ∈ S that both satisfy Σρ_i E_i=0 would imply (ρ_j−ρ'_j)E_j=0. Since ρ_j−ρ'_j is a unit by Definition2.1, this forces E_j=0, contradiction. Hence at most one ρ_j∈S solves; `Pr[batch equation passes | any E_i nonzero] ≤1/|S|` without assuming Rq is a field. This is an ideal-computation probability; actual Πsum adds ≤2ell/|S|, PCS errors and original lookup errors.
Combining with I78/I87 conditional fixed-vector discrepancy detection, a *simple union bound* gives mask failure ≤2^(-t) or (3/4)^t, plus batching ≤1/|S|, sumcheck ≤2ell/|S|, and PCS/lookup/Fiat–Shamir errors. t=128/309 **does not** by itself provide overall ≤2^-128 after additive errors. Need explicit security budgeting and exceptional-set size (paper uses extension-field components and potentially |S|≈pmin^d, not automatically 2^128 for scalar integer subset S).

## One exact adversarial toy + integer cost arithmetic
Script and reproducibility:
- /mnt/data/iteration91_vfhe_batched_aggregate_cost.py SHA256 b157f86149e3e64bc40a1717e41823a334224b229c5dcba06a612d55ad5d86f0
- /mnt/data/iteration91_vfhe_batched_aggregate_cost_results.json SHA256 ab1b7bb34fe2f981688869de537e5e9e49ec262780c990b41671e5807d6cb8c2
Run exact Python, assertions PASS. For R=Z_(29*37)=Z_1073, exceptional diagonal S={0,...,28}, two fixed nonzero E1=E2=407 (1 mod29,0 mod37), exhaustive all29^2 mixing pairs show exactly29 false accepts, i.e. 1/|S| tight. Another concrete precommitted bad h=(407,0,1,0), masks α1=(1,1,0,0), α2=(1,0,1,0), purported bounded A1=1,A2=2: true defects E1=E2=406 (0 mod29,−1 mod37), and exactly21 of841 mix pairs pass, <1/29. Not an attack on actual paper's source protocol, just bounded cancellation test.
Conservative M=2^19: full explicit mask challenge bits t*M=128*524288=67,108,864 bits=8MiB, naive public MLE F(r) evaluation O(t M). Rank-one reshape 512x1024 uses 1536 bits/mask; 309 masks =474,624 bits=59,328 bytes, verifier evaluates F(r) via 309 products u~_i(r_X)v~_i(r_Y) and scalar mixing in O(309*(512+1024))≈474,624 native-ring scalar operations, plus proof/PCS processing; that's substantially sublinear in M but an enormous multiple of the source O(log M) PIOP verification (and t public A_i). These are asymptotic cost scales, not actual cycle counts or 128-bit end-to-end performance.

## Concrete research decision
[NEGATIVE] Cannot dismiss I88–89 merely by multiplying t times Brakedown evaluation costs. Appendix F.2 already amortizes testing and a standard random-linear-combination at PIOP level reduces terminal evaluation families from t to ONE, independent of t and still under original h commitment.
[OPEN MAIN BOTTLENECK] Public random mask *description/evaluation* and t integers A_i, plus security budget and 128-bit proof/PCS costs, NOT unavoidable t evaluation phases. Full masks cost O(tM) verifier effort, incompatible with original succinct goal as-is; rank-one masks still O(t√M), potentially viable only under explicit budget and privacy. No claim of optimized fully compiled repair or novel primitive; random batching is a known technique.

## End of Iteration 91
STATUS: **FAIL** 't openings unavoidable'; **PASS** one-ring-sumcheck/one-new-same-h-evaluation batching lemma; **UNCLEAR** practical verifier efficiency/full protocol.
RESULT: Standalone t=128/309 masked claims can be checked, after committed A_i and fresh exceptional-set ρ, via ONE degree-2 Πsum and ONE terminal ring h PCS opening, with extra algebraic aggregation failure ≤1/|S|. Brakedown testing phase can be reused. Explicit full-mask cost 8MiB random bits and O(tM) public mask evaluation; rank-one 59KiB-ish random bits and O(t√M).
NEXT_ACTION (I92): ONE verifier-cost falsification on the surviving rank-one batched construction: compute the *lower-level* source Brakedown per-component evaluation-phase communication/work and |S| soundness budget for a single additional h opening at Medium-circuit scale, then compare 474,624 mask-evaluation work plus 309 public A_i to original 25D source queries. If a missing transcript order or per-field exceptional-set representation makes claimed 128-bit security impossible, archive. No protocol implementation/new mask family until this decisive test. No outreach.
STATE_UPDATE: YES — a material source-compatible batching lemma removes the previously suspected linear-in-t PCS opening count and sharpens dominant cost.
