# Iteration 135 — Rectangular AR24 source/implementation output interface remains unverified

**Date:** 2026-10-13. **PI authorized:** “create long-term Research Opportunity Backlog, then continue from round 134” → execute **I135**, not repeat completed I134. One primary hypothesis and one source/artifact interface falsifier. Before this run created and verified `findings/OPEN_RESEARCH_BRANCHES.md` as long-term opportunity list; linked from STATE (no root file permission). No actual FHE benchmarks.

## Claim to test

**[HYPOTHESIS]** The **published/author-provided implementation** for Aikata & Roy *Secure and Efficient Outsourced Matrix Multiplication with Homomorphic Encryption*, INDOCRYPT 2024, ePrint **2024/1730**, already demonstrates complete **rectangular** D&C matrix output and explicitly performs/accounts for the extra output blocks needed whenever `l t > k p²`, `k=max(l,d,t),p=min(l,d,t)`.

**Falsifier / decisive source gate:** inspect the exact author §4.2 code and output interface for `A_(8×2) B_(2×8)`, where S=32 but 64 explicit output cells. Identify the number of distinct ciphertext products/output ciphertexts; an actual code case with one 32-slot Ct×Ct and all 64 explicit outputs under the I134 standard operator model would be algebraically impossible; code counting ≥2 products/blocks would close the I134 potential omission. If primary artifact cannot be inspected, mark **UNCLEAR/MISSING CRITICAL SOURCE**, not FAIL.

## Original full-paper provenance

- Original IACR ePrint `https://eprint.iacr.org/2024/1730`; Research MCP original 25 physical pages GitHub mirror SHA256 `69847d0bdffe3bd148b1f9bd76278057aa24cfa02f1aab8e8c2e9ac80820a412`, VERSION_UNVERIFIED.
- §3.3 physical p16 Algorithm 4 does `d/s` separate Ct×Ct for **d×d** matrices and emits one row-encoded d×d output; at maximal s=d, one Ct×Ct.
- §4.2 physical pp18–19: geometric D&C of `l×d` by `d×t`, states packing capacity `k p²` with `k=max(l,d,t)`, `p=min(l,d,t)`, and that there is **no increase in Ct–Ct products**. Illustrates (4,2,6) with `S=24=l t` and (2,4,2), both insufficient to distinguish overflow. Section describes matrix splitting but no general rectangular implementation pseudocode or output ciphertext count in available PDF.
- §5 physical p19 refers to `https://anonymous.4open.science/r/MatMul-0568` as original general-solution code/artifact and says rectangular divide-and-conquer timings *can be extrapolated* from square cases; benchmark Table4 p20 lists square/padded dimensions, not (8,2,8).

## Single primary-source/code interface audit

1. **Author-provided artifact `https://anonymous.4open.science/r/MatMul-0568`:** accessed through web browser tool on 2026-10-13; returned `not accessible via this tool`. Full source tree, actual entrypoint, rectangular tests and code for computing/extracting the output thus **NOT READ**. Do not treat lack of access as evidence of absent implementation.
2. **Public official FHERMA winning-code archive** `https://github.com/Fherma-challenges/matrix-mult`, verified connected GitHub fetch of `README.md`, blob SHA `852c326cf27e9e03f2d24b2ddd5f7fc56418f737`. It references the winning Matrix Multiplication Challenge solution and says the repo is archival; no statement of rectangular D&C coverage. This is a related artifact but **NOT verified identical** to the paper's specific MatMul-0568 supplementary repository.
3. **Author Aikata public challenge explanation** `https://hackmd.io/@rqh-_xZ_Tqi4IZJEvUTgMg/HJAD7UlAp`, opened 2026-10-13, §“The FHERMA Challenge Solution” specifies square `d×d` inputs and outputs for Algorithms 1/2 and explicitly discusses *extension to rectangular matrices as a future exploration*. Hence that accessible write-up **does not itself instantiate or validate** §4.2's generalized rectangular output-block scheme. It was associated with FHERMA challenge, not necessarily later complete paper artifact.
4. **Separate independent community reproduction**, `https://github.com/seunghu-kim/matrix-mult-fhe/blob/main/src/matrix_algo_singlePack.h`, fetched using connected GitHub tool, blob SHA `d336186370fec7715d029fb5223a76ea939170da`. The `MatrixMult_AR24` class begins near line 500 with `template<int d>` and `MatrixOperationBase<d>`. It sets `num_slots=d*d*s`, performs loop `i=0...B-1` over `EvalMultAndRelinearize`, and ends `matrixC->SetSlots(d*d)` near line 599. This is clearly a **square** implementation and thus does **not** demonstrate authors' rectangular `l×d,d×t` extension. Independent reproductions are not evidence about exact original submitted code.
5. **Original §4.2 mathematical interface remains ambiguous**. There is a conventional `#CtCt≥ceil(l t/S)` bound for explicit individually represented output entries under linearly prepared/linear-postprocessed S-slot Hadamard products. At (8,2,8), 64 independent bilinear coordinate functions require ≥2 products with S32. If source outputs low-rank compressed factors or computes multiple blocks, the I134 apparent overgeneralization is not established. No source artifact was fetched to tell.

## Scientific judgement and limitations

- **[FACT]** Original full PDF and its claimed slot formula were actually reviewed; original linked artifact URL was checked but unavailable; accessible *FHERMA winning solution* and independent `AR24` reproduction cover only square matrix algorithms in the inspected text/code.
- **[DERIVED]** I134's restricted bilinear dimension/capacity bound remains valid, but says nothing about a low-rank output interface or extra undocumented product calls.
- **[OPEN]** Whether original author MatMul-0568 rectangular D&C code exists, and if so whether it handles output blocks. No author code review, no encrypted execution, no matched-source bug, no novelty.
- **[DECISION RECOMMENDATION]** **PARK the I134–135 rectangular paper-claim audit pending source recovery**. The mathematical lower bound is familiar and output-block bookkeeping alone is low publication value; don't continue iterating toy matrices or infer intentional overclaim. Preserve gap for reopening if original code, exact model, or a nontrivial optimized corrected output representation becomes available.
- **Missing critical source** registered separately in `MISSING_SOURCES.md`. Future analyst should obtain the *paper's own* MatMul-0568 archive, identify rectangular routine and test at the problematic dimensions. Not fair to generalize square-only blog/example to paper-wide code.

## End of iteration

**STATUS:** **UNCLEAR / MISSING_CRITICAL_SOURCE / HUMAN_REVIEW** for the authors' *rectangular artifact implementation* and claimed implicit output-block handling. **PASS** source-interface distinction: publicly accessible example and independently reproduced AR24 code are square-only.
**RESULT:** Cannot confirm that original §4.2 handles/misses the extra `ceil(l t/S)` output factor; published illustrative cases don't test `l t>S`, and the exact author artifact is currently inaccessible. The I134 algebra is a conditional lower bound, not a demonstrated paper bug. No encrypted test/no novelty.
**NEXT_ACTION:** **PARK this paper-claim audit** pending the exact author artifact (or exact published revised rectangular algorithm), and allow PI to choose/delegate one **new higher-value hypothesis** from `findings/OPEN_RESEARCH_BRANCHES.md` (vFHE vs MRFHE especially). If exact code becomes available, a one-test rectangular output block accounting check suffices to close the ambiguity.
**STATE_UPDATE:** YES (source block + direct parent-file admission and corrected branch status).
