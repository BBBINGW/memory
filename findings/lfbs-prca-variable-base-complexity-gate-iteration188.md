# I188 — LFBS/PRCA: a variable-base factor omitted in the summary asymptotic key-switching count

**Date:** 2026-10-14 JST; human PI authorized one iteration with “好的，请继续.” Protocol read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md SHA `372c7e3b5d723b8beb684b66cad4ff783d785965`, OPEN_RESEARCH_BRANCHES and I187 finding; on PI assent recommend PARK I184–187 direct PRSS Gaussian seed-compression branch, leaving larger unbounded-LDec problem open.

## Primary original source / limits

**[FACT]** Zhihao Li, Xuan Shen, Xianhui Lu, Ruida Wang, Yuan Zhao, Zhiwei Wang, Benqiang Wei, *Leveled Functional Bootstrapping via External Product Tree*, IACR ePrint **2025/022**, https://eprint.iacr.org/2025/022. Current ePrint metadata at URL confirms preprint and Jan 2025 approved; **35-page original official PDF extracted via web.open** `https://eprint.iacr.org/2025/022.pdf`, web PDF ref `turn324214view0`. IACR original source primary text from physical PDF P4 (printed p5) intro, P16 (printed p17) packing analysis, P17 (printed p18) **Algorithm5 PRCA**, P18 (printed p19) **Algorithm6 LFBS**, P19 (printed p20) **Table3**, §4.3. **PDF image screenshots were attempted for pp4,16,17,19 through web screenshot but returned 403/cache misses**, so equation typography is grounded by independent raw PDF text and arithmetic, not visually rechecked; don't invent screenshot verification, page refs or PDF checksum. Research MCP `get_eprint_paper(2025/022)` **SOURCE_UNAVAILABLE** due apparent zero-padding normalization to `2025/22` and metadata404, so no MCP-verified PDF SHA/version parity. This uncertainty cannot be silently ignored, especially if later revised edition is released.

Paper's contribution is leveled functional bootstrapping (LFBS) by converting digit-wise LWE inputs to cyclic-encoded RGSW and doing external-product tree LUT evaluation; source claims **l blind rotations** rather than exponential number of blind rotations in TFBS, and major empirical improvements on 12-/16-bit LUTs. **None of those tested speedups, ciphertext correctness, or blind-rotation count is challenged here.**

### Exact tension within SAME original source

**[FACT/source intro physical P4 lines147–159]** Packing B RLWEs via automorphisms + HomTrace claimed `O(log N)` gadget products; Table1 introductory comparison specifies `log N < B < N` in the displayed regime (subject to interpretation of which parameter is variable).

**[FACT/source algorithm physical P16 lines947–984, P17 lines1001–1019]** §4.2 derives **EXACT** per-PRCA RLWE key switches:
```
 B/2 + B/4 + ... + 1 + log2(N/B)
    = B−1 + log2(N/B).
```
Algorithm5 lines3–6 loops `i=1..log2 B, j=0..B/2^i−1` with ONE `HomoAuto` each inner iteration. At the end, `Tr_{KN/KN/B}` costs `log2(N/B)` key switches in original source accounting. Any bona-fide HomoAuto includes a key switch to the original RLWE secret, as original §2 automorphism definition states. **No counting interpretation can make these B−1 individual calls disappear** from the unmodified algorithm; DAG depth is log B, but total *work* is B−1. **Key MATERIAL distinct types may be only O(logN) because same automorphism key is reused at each level.** Do not confuse storage and calls.

**[FACT/source Table3 physical P19 lines1135–1158]** Summary table states LFBS `O(log N·l'·B^(l−2))` RLWE key switching and `O(n·l + log N·l'·B^(l−2))` gadget product components, while the source Algorithm5 uses B−1 key switch calls per PRCA. **[FACT/source Algorithm6 physical P18 lines1072–1085]** For l input digits, l' outputs, number of PRCA invocations is `l'Σ_(j=0)^(l−2) B^j` if no degenerate l=1, so actual calls for ALGORITHM AS WRITTEN:
```
K_PRCA(N,B) = B−1 + log2(N/B) = Θ(B+log N),
M_PRCA(B,l,l') = l' (B^(l−1)−1)/(B−1),
K_LFBS_PRCA = M_PRCA · K_PRCA
             = Θ(l' B^(l−2) (B+log N))     for B≥2, fixed l≥2.
```
This is not uniformly bounded by `O(l'B^(l−2)log N)` if B grows asymptotically faster than logN. For `B=Θ(N^α)`, α>0 with B|N (e.g. B=√N power2), per packing Θ(B), not Θ(log N). **[Important scope]** If authors define B to be a fixed constant while N→∞, the two asymptotic O forms are compatible! The source implementation explicitly benchmarks B=4,16 (Table5); for such fixed choices, a constant 2× discrepancy in gadget-call count does NOT itself invalidate any reported runtime. The statement should be framed as **parameter uniformity/complexity bookkeeping**, not a proven paper theorem error under its intended asymptotic model.

**Crucial distinct counts:** (a) automorphism/KS CALLS: may scale with B; (b) unique automorphism EVALUATION KEYS: can remain O(logN) since keys shared per level; (c) multiplicative depth: O(logN) due balanced tree; (d) number of external-product operations at other LFBS layers already scales like O(l'B^(l−1)) so the *total* fixed-l work order can still be Θ(l'B^(l−1)) even with corrected PRCA term. The original headline linear BLIND ROTATIONS is unaffected.

## ONE primary falsifiable claim/test

**[HYPOTHESIS to KILL]** The complete Algorithm5 PRCA key-switch workload is bounded by O(log N) **uniformly in N and admissible growing B**; therefore the Table3 O(l'B^(l−2)logN) bound holds without a B-fixed caveat.

**[FALSIFIER]** Enumerate nested Algorithm5 `HomoAuto` calls, append HomTrace calls exactly as same source, and calculate LFBS total Algorithm6 invokes for representative power2 N and divisor B. A growing B family with Ω(B) calls kills uniform O(logN).

**[PASS independent exact count]** functions.exec JS deterministic enumeration (no encrypted FHE implementation). Tested:
```
N    B     per PRCA: tree + trace = total    log2N
1024 4     3 + 8 = 11                       10
2048 16    15 + 7 = 22                      11
4096 64    63 + 6 = 69                      12
4096 256   255 + 4 = 259                    12
4096 1024  1023 + 2 = 1025                  12
```
Under l=3,l'=1, number of PRCAs B+1. N2048,B16 →17×22=374 calls vs comparison 17×log2N=187. N4096,B256 →257×259=66563 vs 257×12=3084. Entire discrepancy grows with B if treated as independent variable.

## Verdict / next gate

**STATUS:** **FAIL** uniformly-in-B O(log N) PRCA call-count hypothesis; **PASS** exact source self-reported sum, independent loop enumeration and LFBS propagation; **UNCLEAR** whether published asymptotic scope explicitly fixes B, any unaccounted implementation optimization/parallelism eliminating total work, and current revised PDF version parity. Neither new FHE algorithm nor a cryptographic/security/correctness problem discovered; source body already states exact B−1 cost, so not an undisclosed technical obstruction. A **potential cost-model overclaim**, worth precise review but likely not publication-level by itself.

**NEXT_ACTION:** **I189 NOT STARTED, HUMAN_REVIEW.** If PI continues, ONE decisive higher-value gate: determine whether there is a **nontrivial, source-compatible way to compute the B-to-1 packed RLWE output with sublinear-in-B RLWE key-switch CALLS**, while maintaining key storage, noise and correctness and comparing to Algorithm5. First test a candidate *batch/hoisted automorphism* mechanism using source and prior art; distinguish hoisting reducing decomposition work vs actual number of key switches. If no candidate survives prior-art gate, PARK LFBS mere table bookkeeping and pivot. Alternatively check fresh official PDF visual if available, and author contact only on PI approval. Do not call a complexity-parameter mismatch a novel FHE primitive.
**STATE_UPDATE:** YES — materially source-grounded variable-base parameter audit; separate conditional negative result from practical and security claims.
