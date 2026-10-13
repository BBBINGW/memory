# Iteration 167 — Cussen AHE PC-MM Algorithm 3 line 8 is mathematical shorthand, not a second uncompressed scalar-multiplication loop

**Date:** 2026-10-13. The human PI answered “好的，请继续” after I166 recommended parking TFHE HFP generic covariance microaudits and pivoting to source-available high-impact work. Asst interprets assent to PARK the specific I165–166 generic correlated-noise line, not as proof the whole Bergerat et al. paper has no research problems. One new source and ONE primary claim/ONE decisive test. No FHE speedup claim.

## Protocol and provenance

Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` (after I166 blob `2a3475d3dfdbca15825a4d60010afba736e1123a`) → `findings/OPEN_RESEARCH_BRANCHES.md` → I166. Archived matrix/packing/GL/MRFHE/LEAF failures checked to avoid reopen by label. Official source:

- Krishna Sai Tarun Ramapragada and Utsav Banerjee, *Fast Plaintext-Ciphertext Matrix Multiplication from Additively Homomorphic Encryption*, ePrint **2025/711**, https://eprint.iacr.org/2025/711, arXiv 2504.14497v1, published in IACR Communications in Cryptology 2025. Research MCP acquired a **33-page** verified parsed PDF from `ALTERNATE_SOURCE`, SHA256 `347e7ffd1aefeb1c75c7561fda545becf33845b32d43aeed0a926c33570d2c81`; this version has **not** been authenticated to any later official paper PDF revision. Inspected §3.2 Algorithm 2 physical p10, §3.3 Algorithm 3 physical p13, source code paragraph p16.
- Independent official ePrint web PDF and arXiv PDF text were accessed. Rendering via web PDF screenshot was attempted twice, both returned cache-miss errors, hence **mathematical glyph visual parity unverified**. Key loop index and operation names in text are legible and independently confirmed by author's code.
- Authors' public repository is **https://github.com/sinesyslab/fast_pcmm_ahe_cic25**; fixed inspected main commit `191acd3b3c35db1d2a23b5984e46af8ee019e5b1` (commit date 2025-04-02), file `test_pcmm_proposed.c` blob `6b88d523101ef66037e220a2e03577187b2891be`. Fetched via **connected GitHub**, not an unverified snippet. Relevant lines ~470–650.

## ONE primary hypothesis and cheapest falsifier

**[HYPOTHESIS]** Algorithm 3's line 8 expression `C_ij += (a_ik B_{kj})` literally triggers a NEW uncompressed plaintext-scalar×ciphertext multiplication for every original matrix entry `a_ik`, in addition to its compressed scalar multiplies at line 5 and reconstruction at line 6. If so, no source code using Algorithm3 as written can realize the advertised savings.

**[FALSIFIER / one source cross-check]** Locate in the authors' concrete C implementation whether the outer-product accumulation re-invokes ECSM on original `A[i][k]` for each i, or uses the already reconstructed ciphertext vector produced from compressed `A_post_compression`. Check loop counts against Algorithm 2/3 and the source's 8-entry toy example; if only compressed inputs undergo scalar multiplication, reject the supposed algorithmic cost inconsistency.

## Exact source/code result

**[FACT PAPER]** Alg 2 compresses the original plaintext length `m` to `m'≤m` using repeated sort/eliminate duplicates/consecutive differences, computes exactly `m'` ciphertext scalar products, then reverses the transforms via ciphertext group additions, duplication, permutation. Alg 3 lines 3,5–6 apply precisely this to each plaintext column `A[:,k]` and each ciphertext `B_{kj}`; line 8 mathematically displays `C_{ij} += a_{ik} B_{kj}` (same value as reconstructed ciphertext), which on its own is ambiguous as an operation-level instruction. The **intent** shown in prose and Fig5 is that reconstructed values are used. Authors' toy length8→compressed3 saves 5 scalar products per group component (for EC ElGamal: 16→6 full point scalar operations). Paper §3.3 pp12–13 explicitly emphasizes compression reused across l columns of outer products and reconstruction in step6.

**[FACT CODE]** Source `test_pcmm_proposed.c`:
- For each original plaintext column and encrypted B element, line ~498 loop `index < length_of_vector_after_iter[col_index]`, initializes `output_vector_cussen_approach[index] = B[col_index][col_ct_matrix]` and invokes `ECP_NIST256_pinmul(..., A_post_compression[index][col_index], BIT_WIDTH_EACH_PLAINTEXT)`. Only compressed `m'` products, no original `m` multiplication at this point.
- Lines ~507–560 reverse compression using stored `pointer_array_iter1...iter4` and `ECP_NIST256_add` to restore all m plaintext-scalar times encrypted original B point.
- Lines ~553–564 write recovered elements to `result_outer_product[index][col_ct_matrix]`, then use `add_ECP_Matrices(result1_cussen, result_outer_product,...)` or initial copy. The second EC ciphertext point component repeats the same operation in lines ~572–643; it does not recompute `A[i][k] B` directly. The separate **schoolbook benchmark** in the same file (about lines301/319) *does* use `ECP_NIST256_pinmul(..., A[i][k])`; it is a baseline, not part of the proposed path.
- Source is **AHE**, elliptic-curve ElGamal group operations with no packed SIMD slots; its cost benefit hinges on small plaintext integer alphabet and scalar point multiplication being expensive relative to point addition. **No demonstrated transfer to BFV/CKKS/TFHE packed matrix multiplication**, so do not label a new FHE optimization.

**[DERIVED]** In the source implemented compressed path, for each plaintext column k and each encrypted matrix column j, the number of proposed-point scalar multiplications is `m'_k` PER EC component, whereas direct schoolbook uses `m`, giving exact saved scalar multiplications `2 l∑_{k=1}^n (m−m'_k)` before reconstruction group additions (additional constant/structural notes for zero-multiply optimizations). The alleged extra `2mnl` point-scalar operations of a *literal recomputation* do NOT appear. No runtime result reproduced.

## Judgment

**STATUS = FAIL** the candidate source-algorithm mismatch hypothesis. The printed line8 is mathematical shorthand for the ciphertext values previously reconstructed in line6, not a forced second execution; authors' code validates their intended compressed operation counts. It would be misleading to claim a paper/code bug, missing algorithmic cost, or wrong benchmark. Observed ambiguity is at most notation; **not novel/publishable**.

**[OPEN]** A genuinely different target might evaluate low-precision public-weight compression in **unpacked** or very sparsely packed RLWE use; however packed CKKS SIMD cost is structurally different, and authors openly limit their scheme to non-packed AHE. No source-supported new benefit/cost theorem or missing application case identified here. Do not continue polishing Algorithm3 expression or blindly transfer Cussen to CKKS.

## End of Iteration 167

**STATUS:** **FAIL** alleged duplicate uncompressed scalar computation from Algorithm3 line8; **PASS** exact source-vs-implementation cost-path audit; **UNCLEAR** any genuinely novel transfer of this AHE algorithm to packed FHE.
**RESULT:** Author code only performs scalar multiplications on compressed `A_post_compression` entries, reconstructs with `ECP_NIST256_add`, and accumulates reconstructed outer products. The alternative literal reading of line8 does not describe implementation. Source 2025/711 and pinned implementation accessible; no correctness/benchmark exploit or FHE performance improvement.
**NEXT_ACTION:** Recommend **PARK** this AHE notation mini-audit; select **one actual BFV/CKKS/TFHE FHE source** with a concrete expensive primitive/parameter frontier, avoiding archived failures and source-gated targets. No more literal-source cosmetic audits. PI retains decision.
**STATE_UPDATE:** **YES** — records PI-parked TFHE previous microaudit, new distinct source/code gate and exact no-bug result; updates STATE checkpoint and next target priority.
