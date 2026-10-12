# Iteration 94 — Four independently rebatched scalar sumchecks: soundness amplifies, source Brakedown cost remains high

Date 2026-10-12. Active paper Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286. PI authorized narrowly scoped I94 as option A following I93 HUMAN_REVIEW.
STATUS: **PASS** conditional fourfold ideal PIOP soundness with independent mixing AND sumcheck challenges; **FAIL** purported no-extra-cost cheap scalar shortcut using original §5/Appendix F.2 PCS; **HUMAN_REVIEW** whether to archive this specific public-A repair and pivot. NOVELTY NOT VERIFIED; no compiled SNARK forgery, benchmark, universal lower bound, author contact or public disclosure.

## Source/read-before-write
Read live GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, I91, I92, I93 notes; read source ePrint 2025/286 PDF physical pp7–10,25–27,50–52 using connected Research MCP. Cached PDF mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, latest official VERSION_UNVERIFIED.
[FACT] Definition2.1 p7 exceptional set differences units; §2.2 p9 Theorem2.6 ring Πsum degree-per-variable≤2, ell Boolean variables has soundness error ≤2ell/|S|.
[FACT] §3.1 pp10–11 Rq decomposes into degree-d extension field factors (for d4), with scalar-only exceptional S at most p_min, proved tight I93; paper 49-bit primes p>=2^48.
[FACT] §5 p25/Appendix F.1 p50 source ring PC executes PC(i) for EVERY one of μ CRT fields.
[FACT] Appendix F.2 p51 Brakedown PCS reused TESTING for same commitment with multiple evaluations, but every distinct evaluation is a separate EVALUATION phase: transmit v'=q1 Uf, sample/open encoded columns, verify encoded linear relation and <v',q2>. Source F.2 does NOT prove cross-point evaluation-phase batching.
[FACT] Table2 p27 Πrange D1 25 native ring evaluation claims. §6 p27 Medium N=2^13,d4,L3 and 49-bit primes; I92 μ=6144 vs8192 source L convention unresolved; exact c5 digit layout also unresolved.

## ONE hypothesis and decisive test
Can four independent base-scalar-challenge repetitions (using same precommitted h, same t public bounded A_i but all fresh ρ^(j), r^(j)) rescue the added masked-aggregate relation to a sufficient soundness margin without making source Brakedown verification prohibitively expensive?
Fast falsifier: reuse one ρ across all repeats, prove that gives an unacceptable ~1/p mixing-event floor; then calculate correct fourfold bound and explicit source F.2 vector cost for four independent evaluation phases. Validate with exhaustive small CRT example (not simulated SNARK).

## Crucial ordering and independent mixing lemma [DERIVED]
Before mask: commit original h.
After t masks: prover fixes all t canonical public integer A_i∈[0,T] (with T=m*(β-1)<p_min from I88). These must NOT be chosen after ρ.
For j=1..4, freshly independently sample ρ_i^(j)∈S for all i, define F_j=Σ_iρ_i^(j) α~_i, Y_j=Σ_iρ_i^(j) A_i*1_R and execute ONE fresh degree-2 virtual ring Πsum to assert sum_{Boolean}F_j(x)h~(x)=Y_j, terminating in SAME original C_h PCS evaluation at fresh r^(j)∈S^ell. The source commitment and Brakedown testing phase can be reused. Transcript Fiat–Shamir binding/domain separation is not yet proved.
Let E_i be the fixed masked-aggregate discrepancy. If some E_i!=0 in Rq, independent mixing conditional on previous transcript gives Pr[Σρ_i^(j)E_i=0]≤1/|S|; if mixed relation is false, independent Πsum error ≤2ell/|S| against fixed h. Therefore each j has conditional false acceptance probability ≤(1+2ell)/|S|, and all four independently conditioned rounds ≤((1+2ell)/|S|)^4.
At ell19 and p_min≥2^48: single bound 39/2^48 ≈2^-42.7146, four bound (39/2^48)^4 ≈2^-170.8584. THREE bound ≈2^-128.1438 technically meets mask-independent 128bit target without additive budget; cannot claim full system ≥128bit. Four leaves substantial margin to budget OTHER errors only if their actual bounds are independently established.
Most important BUG/KILL: If all four reuse the SAME rho vector and that vector cancels the wrong E_i, then all repeated Πsum honestly prove a TRUE mixed statement, hence repetition does NOT amplify Pr[mixing cancellation], which can remain ≥1/p. Must regenerate BOTH ρ and sumcheck r each time (and draw PCS testing/evaluation randomness as required).

## Exact toy [DERIVED + ENUMERATED]
Use R=Z_(29*37), scalar exceptional S={0,...,28}, fixed original h~=0, one postcommit public WRONG A=1. Fresh mixing rho∈S produces false mixed claim Y=rho. Cheater sends first-round univariate g1(Z)=rho·Z, which passes g1(0)+g1(1)=Y. True virtual g=0, so terminal check succeeds iff rho*r=0 in R. Exhaustive 29²=841 (rho,r) combinations yield 57 acceptance: 29 with rho=0 and all r, 28 with nonzero rho and r=0. One-run p=57/841≈0.0677765.
For 4 repeated sumchecks with same shared mixing rho but independent r_j, acceptance probability EXACTLY 1/29+28/29^5≈0.0344841, hence a 1/29 floor.
With independent rho_j AND r_j per run, same attack acceptance probability (57/841)^4≈0.0000211016; this is a small toy, not extrapolation to real p or optimal adversary.
Source code: /mnt/data/iteration94_scalar_fourfold_cost.py SHA256 77e70859e72a5d7ef0bdba984c0edb80c9f6f279573be9f046ea27c7f26062b0
JSON: /mnt/data/iteration94_scalar_fourfold_cost_results.json SHA256 405a63e64d92031a3fcde7d72c5833eafe556520e18be79cb586e8931a3d7020
Toy does NOT test PCS/FS, original proof or full vFHE validity.

## Cost boundary from SOURCE Brakedown F.2 (conditional)
Four fresh Πsum over ell19 => 76 variable rounds, and 4 additional distinct terminal h ring evaluations. The source Table2 D1 aggregate original Πrange count was 25 ring evaluations, hence *if attached to ONE Πrange* simple count 25+4=29, NOT 25 existing h proofs +4 and NOT whole circuit cost. Four ring evaluations lead to FOUR μ-field evaluation phases (24,576 or32,768 field phases for μ=6144 or8192), subject to optional testing phase amortization. They do NOT require four NEW commitments nor four PCS testing phases.
For source F.2 explicit uncompressed v'=q1 Uf, each field symbol F_(p^4) with 49bit p requires at least25 FIXED-LENGTH bytes. Because author's h digit packing/c5 unspecified, use conditional scenarios:
- one-component h digit array ~40960 padded to 2^16; even ℓ16 -> Brakedown matrix side m_B=256. Four raw v' across all μ =150 MiB (μ6144) or 200 MiB (μ8192), plus all sampled encoded columns and Merkle proofs.
- hypothetical full-workload h envelope 2^19 zero-padded to 2^20; even ℓ20 -> m_B=1024. Four raw v' aggregate =600 MiB (μ6144) or800 MiB (μ8192), plus sampled encoded columns and Merkle proofs.
These are byte counts for the literal F.2 interface under these exact layouts, NOT measured bandwidth, NOT proven minimum for other PCS designs. Each opened encoded column across μ components carries another μ*m_B field symbols, so any positive column count adds substantially; security column count t_PCS and field-PC error budget still unverified (not the mask count t_mask). Source F.2 explicitly allows same commitment's testing phase to be reused but does not assert reusing evaluation v' for differing point challenges.
Scalar challenge benefit: alpha~_i(r) is scalar, may be evaluated once modulo q / component-reduced instead of μ DIFFERENT extension-field evaluations. But even modulo q ring arithmetic and dense masks have costs; t_mask=328 rank-one challenge bits 503,808 total and 328 public A_i (not 128bit all-in). One 4fold protocol public F_j(r_j) must be computed 4 times, O(4 t_mask (a+b)) ring-scalar operation scale, but μ PCS opening dominates in source's straightforward F.2 interface.

## Soundness accounting and decision
For fixed wrong digit witnesses if mask screening misses inconsistency, likelihood ≤(3/4)^t. If t=328, mask-only ≤2^-136.1323. If detected, fourfold mixing+Πsum ≤2^-170.8584 as above. PCS addition demands 4μ field evaluation proofs. To reserve all four μ≤8192 PCS components ≤2^-136 by naive union bound, per-field error ≤2^-151, excluding any extra testing phases and source Πbeta-range's own error. The original vFHE proof needs independent 128bit budget and privacy/FS argument; no complete security theorem.
[NEGATIVE] Fourfold soundness can mathematically amplify (unlike shared rho), but in source's explicit Brakedown representation it retains LARGE evaluation-phase data. There is no demonstrated low-cost win, no costed optimized new PCS, and no novelty from known repetition/amplification. Thus rational PI review rather than an indefinite nearby repair search.
[UNKNOWN] Whether using existing source's many 25D evaluations one can amortize column opening or leverage hidden/structured compression while retaining knowledge soundness has not been established. The source may have implementation-specific optimizations; no universal impossibility claimed.

## End
STATUS: **PASS conditional IOP error amplification; FAIL cheap direct F.2 workaround; HUMAN_REVIEW on archive or alternative priority.**
RESULT: Bound ((39/p_min)^4)<2^-170.85 IF fresh mixing AND sumcheck random challenges each run. Same mixing repeated 4 times has actual toy ~1/29 failure probability floor. Four source ring evaluation phases imply 4μ native field evaluation phases with source-style uncompressed v'≥150–800MiB conditional on h layout, BEFORE encoded columns.
NEXT_ACTION: PI decide whether to archive/public-A repair cost branch and switch FHE hole (recommended), or explicitly authorize ONE sharply defined separate optimized PCS / proof compression hypothesis with measurable ≥10× source F.2 cost gain. Do NOT auto-pivot, implement additional protocols or contact authors.
STATE_UPDATE: YES — substantive correction on two layers of randomness and quantified fourfold field PCS cost.
