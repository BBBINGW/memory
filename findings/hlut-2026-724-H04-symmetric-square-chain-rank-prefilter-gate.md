# HLUT H04 — Full-column-rank chains can be structurally incapable of full-row-rank LUT decomposition for every D

**Date:** 2026-10-14 (Asia/Tokyo). Independent one-hypothesis TFHE HLUT pre-screen round H04 after H03. Human PI said continue. Followed read-before-write on `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (concurrent vFHE V28/old global I192 READ ONLY), and `failures/hlut-2026-724-H03-one-chain-affine-basis-rank-no-go.md`. SHIP I226 unaffected. No upstream or global state writes.

## ONE primary hypothesis, cheap decisive test

**H-HLUT-04:** Under author Table1 `s=2,p=3,n=4,lambda=2,t=2` (L=6), the combined cheap prerequisites `rank_F3(U)=L` and paper Equation8 `(t+1)L>=s^n` ensure there EXISTS some matrix `D∈F3^{t×L}` for which the canonical Eq(1) evaluation matrix `A=(U D^T | 1) □ U` has full row rank16. This would justify repeated D sampling whenever the chain passes the author implementation's `rank(U)==L` prerequisite.

**Falsifier:** Identify one legal two-step nonlinear chain with `rank(U)=6`, `(t+1)L=18>=16`, but whose entire *degree-2 column product span* has rank `<16`, proving rank(A)<16 for ALL admissible D even if D sampled from the whole field and regardless of the number t of product terms. One source-shaped sample cohort estimates how often this obstruction occurs after the existing rank(U) check. This is NOT a runtime or new algorithm test.

## Primary source and implementation provenance [FACT]

- Belaïd, Bon, Rivain, *Decomposition of Large Look-Up Tables for Fast Homomorphic Evaluation*, **TCHES 2026 Vol 3**, ePrint 2026/724, https://eprint.iacr.org/2026/724. Research MCP full parsed **32 physical pages**, mirror git revision `108e41a7dc5788eb2d61023f9aecbcb72889d1d9`, PDF SHA256 `cc45b49e20958f5c3fc1e327d84d1549d7fef08bdb4ba973dac75fd3a67efeb4`, **VERSION_UNVERIFIED** against publisher official text. Specifically §4.1/4.3 Eq(1),(4),(6)-(8), pp9–14; Table1 p21, §5.2 encoding switch pp24–25. The authors only state full rank of A is sufficient for arbitrary target LUT y; they DO NOT explicitly assert `rank(U)=L` is sufficient to make A full rank. Therefore H04 is **our hypothesis**, not a refutation of an author theorem.
- Released author artifact https://github.com/CryptoExperts/artifact-HLUT-TCHES pinned `088029cb4cd3a6b33ac10e0c78ea193b1835216d`. `decomposer/src/decomposer/decomposition.py` blob `ce5d25df0ec2296c56a75c24e158f6cbe15f90f1`: `MultiDec.initialize()` samples a fresh chain until `rank(U)==n+lambda` (only first-order test). `Decomposition.initialize()` samples D with `np.random.randint(0,2,...)`, **binary D in released actual code**; paper p14 says D uniform in Fp. A built as `face_splitting(U,V)` with `V=(UD^T|1)`. The first output on failed check actually **reinitializes the chain**; therefore false U-positives do NOT each necessarily cause 50 wasted D retries on first output. Later outputs append product features and may resample D repeatedly with other code paths.
- `decomposer/src/decomposer/atomic_function.py` blob `8599ee4cd39e318b68ca6be9ee03a2d7ef68fb9e` samples α uniform in F3 and ψ among exactly 18 nonlinear unary functions F3→F3; `utils/utils.py` blob `753979e14b237f1dafa2855ae7b75e9a5019f0d7` defines nonlinear function set by removing nine affine unary functions from all 27. `chain.py` blob `5434a5917c9dc413204f0250391c6936d9706bff`: second atomic function uses previous output, matching H01/H03 chain. Existing H03 found a free affine constant `1` repairs one specific U but not one-atomic general method.

## One structural lemma [DERIVATION]

Let `U∈F_p^{M×L}`, M=s^n, with column vectors `u_1,...,u_L` indexed by all original LUT inputs. Define the quadratic-feature column space

`W(U) = span_Fp( {u_j}_{j=1..L} ∪ {u_j⊙u_k}_{1≤j≤k≤L} )`,

where `⊙` denotes entrywise product. Because each row `d_i` of D gives `v_i=Σ_k d_{ik}u_k`, every column of `A=(UD^T|1)□U` is either `u_j` or `u_j⊙v_i=Σ_k d_{ik}(u_j⊙u_k)`. Consequently

`rank_Fp(A) ≤ dim W(U)` **for all t and D**. This is a *necessary* bound; `dim W(U)=M` does NOT imply an A with fixed t and binary D must have rank M. Computing `rank W(U)` once before searching D provides a structural yes/no rejection for full-row-rank demand. If the target output is fixed rather than arbitrary, rank-deficient A may still contain the target y; source §5.2's encoding switching may also yield valid target-specific representations, so the prefilter is not a safe universal discard in that mode.

## Source-compatible decisive counterexample [EXACT]

Use `s=2,p=3,n=4,lambda=2,t=2,L=6,M=16`, exact H01/H03 original two-step chain:

`ψ0(z)=ψ1(z)=z² (mod 3); α0=(2,0,2,1), α1=(2,2,2,0,1)`.

`x4=ψ0(2x0+2x2+x3); x5=ψ1(2x0+2x1+2x2+x4)`.

Set sample binary `D=((1,0,0,0,1,1),(1,1,1,1,1,0))`, with all 16 Boolean input rows and arithmetic in F3. Then

- `rank_F3(U)=6` (passes released author's base-chain check).
- Eq8 number of columns `(t+1)L=3×6=18≥16` (passes paper necessary dimension screen).
- `rank_F3(W(U))=15` for the full 6 singleton + 21 symmetric pairwise-product columns. Therefore every possible A(D) has rank≤15, EVEN when D is arbitrary ternary and t is increased. In particular actual listed binary D gives rank A=15.
- Adding a separate public constant 1 into the basis changes W to a larger space of rank16 for this chain (H03), but is a distinct *modified construction*, not evidence that paper's original A can achieve rank16.

**H-HLUT-04 FAILS** by an exact, D-independent finite-field bound; source paper's claimed full-rank condition itself remains true.

## One sampling sanity / potential magnitude [COMPUTED]

Script `/mnt/data/hlut_H04_quadratic_span_prefilter.py` implements exact mod3 Gaussian elimination and all 16 LUT rows. SHA256 `df9fe840e32ff2b4f2066b7df79e89270df43c8a3de513586572d299a380ca46`. JSON `/mnt/data/hlut_H04_quadratic_span_prefilter_results.json` SHA256 `43b46ec5480ad90f7965c877207a329a05e44c4ac8a7e23c6944b94eb51e6d0d`. Repro Python NumPy/Numba with deterministic seed20261014 and **4096** independent source-shaped two-atomic-function chains, α uniform in F3 and nonlinear ψ uniform among 18 maps (no sampling D needed for structural bound). Executed assertions for exact fixed H01 chain, including updated constant repair.

Counts: 304/4096 chains fail rank(U)=6, **3792 pass rank(U)=6**; among those 3792 **2260/3792=59.5991561%** have `rank W(U)<16` and are **hopeless for universal/full-rank A** for every D, while 1532 have rank W(U)=16. Full quadratic rank distribution conditioned on rank U6: rank13:507, rank14:1005, rank15:748, rank16:1532. This is a reproducible sampling frequency under **one n4, p3, λ2** toy regime, not a formal source probability theorem or estimate across all params.

**Cost/fair-comparison warning:** A rank W(U) check involves a 16×(L+L(L+1)/2)=16×27 feature matrix and finite-field elimination, compared with the original 16×18 A rank test; in the first-output author loop a failed trial already refreshes the entire chain, so the new check could COST MORE time instead of speeding compilation. Also the source accepts some rank-deficient A with encoding switching. To claim an efficiency contribution one MUST benchmark pinned author generator's wall-clock and full functionality with and without the prefilter, particularly later outputs with D retry/backtracking; preserving gamma/PBS budget, encoding-switch behavior and distribution is crucial. Don't assert 59.6% speedup or a guaranteed reduction in repeated sampling; classical quadratic feature-rank screening has NOVELTY NOT VERIFIED.

## End of iteration

**STATUS:** FAIL H-HLUT-04 (source's base-chain full rank plus Equation8 not sufficient for existence of ANY full rank A). PASS exact quadratic-span rank lemma, one original-structure counterexample, and 4096-chain sampling verification. UNCLEAR actual compiler speedup or benefit with encoding switching; no TFHE key generation/ciphertexts/DFR, and no source theorem contradicted. **NOVELTY NOT VERIFIED**.
**RESULT:** There is a real structural precheck `rank W(U)==s^n` necessary for universal LUT decomposability, and 59.6% of base-U-full-rank chains were hopeless for full rank in one source-sized test. However the cost of that test and actual author's loop may negate any speedup; do not pitch as a new optimization without runtime comparison.
**NEXT_ACTION:** Cheapest meaningful follow-up, if PI chooses HLUT: **paired offline compile-time benchmark** of author's pinned `MultiDec` search with and without `W(U)` prefilter for the SAME seeds/targets and matching encoding-switch strategy. Measure number of D draws, full A rank checks, Gaussian-elimination time, and wall-clock at n4 and a larger source size; ensure prefilter never discards a useful rank-defect+encoding solution. If actual saved wall-clock is negligible/negative, PARK H04. Otherwise source-aware multi-output optimization needed for publication novelty. This round does not change the active vFHE main path.
**STATE_UPDATE:** YES one independent finding only; NO writes to global STATE.md, SHIP state, P22 backlog, or upstream code.