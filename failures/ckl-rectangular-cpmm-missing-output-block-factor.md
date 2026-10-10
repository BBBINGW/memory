# Iteration 38 — CKL rectangular CPMM retains the output-column-block k/2 factor

Date: 2026-10-10
Research theme: FHE matrix-multiplication cost audit; continuation after GL I37, independent from archived MRFHE CKL left/right substitutions.
STATUS: FAIL for **the unchanged-Algorithm-5 O(k*T_PPMM(d)) reuse hypothesis**. No proven correctness bug and no novelty.

## State recovery and original sources
[FACT] Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, failures/gl-gaussian-inversion-fixed-i-naive-map.md, failures/mrfhe-ckl-left-right-composition.md and failures/mrfhe-ckl-waxis-native-right-mul.md, and repo failure/finding indices before this iteration. The RIG-HE parked state in STATE.md is unchanged. Did NOT reopen GL BigSwitch, MRFHE W-axis CKL conversion, or MRFHE joint-packing branches.

[FACT] Primary original source: Cheon, Kang, Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, IACR ePrint 2025/1957. Research MCP fetched/cached 32 physical pages, GitHub mirror, PDF SHA256 ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a, VERSION_UNVERIFIED. Read:
- §1.1 physical p.3: rectangular CPMM and CCMM described with complexities `2 k^2 T_PPMM(d)` and `4 k^2 T_PPMM(d)` for d x (N/2) by (N/2) x (N/2); in scalar naive multiplication terms O(d N^2).
- §4.2 Algorithm 1, physical pp.16–17: an r=k/2 batch of square d×d CPMMs uses two PPMMs over R_{q,k}; scalar-residue cost `2 k T_PPMM(d) + O(d² k log k)` per d-column output group, including rescale transform cost.
- §6.1 physical pp.22–23: M=[M_0|...|M_{r-1}] with M_i d×d; U vertically split into U_i d×(N/2); rectangular multiplication MU=Σ_i M_i U_i.
- §6.2 Theorem 3 and Algorithm 5 physical p.24: compute batch CPMM for output, then apply CMT_{N/2} and CMT_k to aggregate SinC batches. The parsed text at the end of §6.2 renders rectangular CPMM `2k · T_PPMM(d) + O-tilde(N²)`, which disagrees with p.3 and with the explicit matrix dimensions; possible lost superscript 2 in PDF extraction or an isolated manuscript typo. **Page-image verification unavailable**; NEVER claim this is a confirmed printed erratum.
- Confirming external evidence: peer-reviewed CRYPTO 2026 publication record at Seoul National University (snu.elsevierpure.com/en/publications/fast-batch-matrix-multiplication-in-ciphertexts/) reports O(dN²) and confirms the paper's overall claim (not its specific p.24 text).

[SOURCE LIMITATION] ePrint MCP returns *parsed PDF text* only, and the ePrint cache is VERSION_UNVERIFIED compared to the peer-reviewed conference revision. Attempts to open an ePrint PDF using web resulted in HTTP 403, and public PDF mirrors were not opened for visual inspection. Treat any difference in superscripts as EVIDENCE-UNCLEAR, while the independently derived cost under the described Algorithm 5 is definite.

## Primary hypothesis / failure condition
[HYPOTHESIS — FALSE IN UNCHANGED ALGORITHM] CKL rectangular CPMM can reuse one k/2-batched square CPMM for all output column blocks at cost 2k T_PPMM(d), with no new algorithmic primitive or restriction on the dense plaintext right matrix U.
[DECISIVE TEST] Expand dimensions, show independent right-hand plaintext blocks U_{i,j}, count the square-batch CPMM calls required by Algorithm 5. No need for encryption, benchmark, or estimator.

## Exact derivation
Put N=d k, r=k/2. Rectangular matrices M∈F^{d×rd} and U∈F^{rd×rd}, with M=[M_0|...|M_{r-1}], M_i∈F^{d×d}, and U vertically partitioned into U_i∈F^{d×rd}. Next write U_i=[U_{i,0}|...|U_{i,r-1}] where each U_{i,j}∈F^{d×d}. Then the j-th d-column output block V_j satisfies

  V_j = Σ_{i=0}^{r-1} M_i U_{i,j}.

SinC batching shares the r input-pair products *at fixed j* as one batched square CPMM, cost 2k T_PPMM(d) in the baseline residue-ring model. But j ranges over r independent output blocks and the U_{i,j} are arbitrary dense independent plaintext matrices. No single fixed-j call determines arbitrary U_{i,j'} at another j' without additional computation in the unchanged algorithm.

Hence total square-CPMM oracle cost = r*(2k T_PPMM(d)) = **k² T_PPMM(d)**. At T_PPMM(d)=Θ(d³), it is Θ(d N²), consistent with §1.1 and abstract. The CMT aggregation adds separate O-tilde(N²) cost; neither term vanishes simply by SinC parallelism. This is an *algorithmic operation-count statement*, NOT a universal algebraic-complexity lower bound: new fast rectangular matrix multiply, structural U, extra batched transforms or amortization over many different M might change the model.

The apparently smaller `2k` local formula from extracted p.24, if printed as such, omits the r output-group count and cannot be generalized unchanged to arbitrary dense right U. PDF typography not visually verified.

## Exact finite-field minimal check
[EXPERIMENT] Reproducible local script `/mnt/data/iteration38_ckl_rectangular_ppmm_count.py` (seed 20261038, q=257) explicitly compares direct dense MU and blockwise Σ_i M_i U_{i,j}, with paired perturbations to independent right-hand U_{i,j} blocks.
- d=2, k=4, r=2: 120/120 identities and target-only-block dependencies; square-PPMM unit count 2kr=16 vs rejected 2k=8.
- d=4, k=8, r=4: 120/120 identities and target-only-block dependencies; unit count 2kr=64 vs 2k=16.
- Symbolic d=64,k=128,r=64: 16,384 vs 256 such units. A dense randomized 4096×4096 toy was attempted but timed out, was recognized as unnecessary, and REMOVED from the verification script; it contributes no evidence.
- This experiment checks plaintext block algebra + stated algorithmic operation counts; it does not implement encrypted SinC, CMT, noise, rescale, timing, or novel lower bounds.

## Outcome / research value
[NEGATIVE] Merely reusing the SinC input encoding does not eliminate the r=k/2 output-column factor for arbitrary dense U in unchanged CKL Algorithm 5. No O(k) improvement from the hypothesized *zero-modification* trick.
[FACT] Original §1.1/abstract already claim O(dN²), so no conflict with authors' principal theorem/cost claim. Potential p.24 discrepancy may be extraction-only.
[NOVELTY] NONE for baseline operation count; the block expansion is standard linear algebra. Do not spend further iterations on this local k-exponent issue unless the actual typeset PDF or a revised algorithm becomes material.

## End of iteration
STATUS: FAIL — unmodified Algorithm 5 does not have universal rectangular CPMM cost 2k T_PPMM(d).
RESULT: Need r=k/2 independently varying output-column groups; baseline count k² T_PPMM(d)=Θ(dN²) with schoolbook PPMM. Exactly matches main paper claim.
NEXT_ACTION: Select a genuinely nontrivial, proof-level FHE research hypothesis rather than another notation/counting discrepancy; if returning to CKL, identify a specific new structural assumption on U (e.g. block-circulant) and quantify a saved full-ring multiplication or key switch BEFORE experimentation.
STATE_UPDATE: NO — preserve parked RIG-HE STATE.md unchanged.
