# HERDS 2025/1804 — Power-of-two modulus raising residual is killed by homomorphic-decode trace

**Date:** 2026-10-14 Asia/Tokyo. **Workstream:** independent newly screened FHE primary-source test after the source-blocked Levis MKFHE branch; NOT the concurrent vFHE state V22 nor global frozen I192 nor SHIP I226. Read-before-write: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, concurrent STATE.md (READ ONLY), findings/ship-memory-STATE.md (READ ONLY), previous findings/mkfhe-levis-2026-2263-extension-free-novelty-source-gate.md, and MISSING_SOURCES.md. No edits to other workstreams.

## Paper, version and exact source locations [FACT]

Binwu Xiang, Seonhong Min, Intak Hwang, Zhiwei Wang, Haoqi He, Yuanju Wei, Kang Yang, Jiang Zhang, Yi Deng, Yu Yu, *HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping*, EUROCRYPT 2026; IACR ePrint **2025/1804**, https://eprint.iacr.org/2025/1804 . Official ePrint landing page states latest revision 2026-03-04, category MK-FHE/Bootstrapping, published EUROCRYPT2026. Research MCP `get_eprint_paper("2025/1804")` returned **READY**, 46 physical PDF pages, cached pinned public GitHub mirror source revision `d68d3723d26dc2978fcb8f0506946a6314eca0c9`, SHA256 `c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7`, **VERSION_UNVERIFIED** relative to official current version. The PDF was text-extracted via Research MCP, NOT visually authenticated; symbolic glyphs/complex formulas need visual confirmation for publisher-level attribution.

Original §3.1 physical p16 (power-of-two FFT-friendly q) states modulus reduction q→q′=q/d followed by lifting q′→q, producing an additive residual **q′ζ=qζ/d**, ζ∈Z[X]/(X^N+1), in the ciphertext phase. §3.1 p17 Algorithms 2/3 implement automorphism+key-switch decode and assume `d=2^ell`. Appendix **B.6 pp39–40** proves that full decoding projects the polynomial onto exponents divisible by d with factor d, then derives noise involving blind-rotation, modulus-switch and key-switch contributions, but not standalone q′ζ; Algorithm 2 proof omitted in paper and Algorithm 3 proof written in Appendix B.6. The source's published noise bound is **NOT** thereby independently audited for all noise correlations and finite-ring backend errors.

## ONE primary hypothesis and ONE decisive source-correctness test

**H-HERDS-01 [FALSIFIABLE, our concern, not authors' claim]:** In HERDS with q=2^w, d=2^ell>1 dividing q, the raw huge `(q/d)*ζ` correction created by modulus raising **generally survives** the subsequent power-of-two homomorphic-decoding trace and therefore cannot be omitted from the final small-error model.

**Falsifier:** Compute the EXACT linear map induced by Algorithms 2/3's successive stages `I+σ_{1+N/2^w}` on `R=Z[X]/(X^N+1)`, 0≤w<ell; show that for every integral ζ and every allowed index shift X^(−j), the trace maps `(q/d)*X^(−j)ζ` to a multiple of q, hence zero mod q. Use a single set of elementary source-valid small parameter rings and exhaustive basis testing, NOT a toy encryption run.

## Exact algebra [DERIVATION]

Assume N=2^m and d=2^ell with 2≤d≤N/2, and q=d*q′ (all source-shaped power-of-two settings). For w=0,..,ell−1 define σ_w(f(X))=f(X^(1+N/2^w)) on the negacyclic ring R=Z[X]/(X^N+1). Exponents 1+N/2^w are odd (valid automorphisms since w<ell≤m−1). Let `T_d=(I+σ_{ell−1}) ... (I+σ_0)`. By induction, for integer coefficient polynomial f=Σ_{j=0}^{N−1} f_j X^j,

`T_d(f)=d * Σ_{0≤j<N, j≡0 mod d} f_j X^j.`

Proof of one stage: if exponent j divisible by 2^w, σ_w acts on X^j as `X^{j+(N/2^w)j} = (-1)^{j/2^w} X^j` modulo X^N+1 (provided j multiple of 2^w), so I+σ_w cancels exponents with v2(j)=w and doubles those with v2(j)>w. The preceding w stages have already eliminated exponents not divisible by 2^w. After ell stages surviving terms have exponents divisible by d and coefficient multiplied by d. Covers j=0 separately (survives all). Multiplication by X^(-j0) beforehand simply yields another integral polynomial in R, so the identity holds for every shifted ζ as well.

Thus
`T_d((q/d)*ζ)=(q/d)*d*Proj_d(ζ)=q*Proj_d(ζ)=0 mod q.`
The same holds for all j-output paths `T_d(X^(-j)ζ)`. This kills the *entire modulus-lifting correction* algebraically, even if ζ has large coefficients. It does **not** kill new trace key-switch noise, blind-rotation error e/d, or modulus-switch rounding; these terms require bounds (and are treated in authors' Lemma 6).

**Important caveat:** Cancellation relies on completing the entire exact trace, d power of 2 with d≤N/2, d|q, and using the source's automorphism indices. A generic arbitrary automorphism or early exit does not justify the same conclusion. Incomplete decode retains q′ζ terms.

## One minimal exact integer test [COMPUTED]

Reproducible source-independent Python script `/mnt/data/herds_trace_modraise_gate.py` SHA256 `cf7de87f0efdeac3a92aa69a2641b851d3f18d4798af8f0cf496b77dabba85d3`. Results JSON `/mnt/data/herds_trace_modraise_results.json` SHA256 `e63cb85b12eaf4df199449ff4188b17014b503b2db11e4ac98ce11bfec1464e7`.

For N∈{8,16,32,64} and d∈{2,4,8,16} with d≤N/2 (13 source-shaped pairs), implement exact negacyclic polynomial automorphism and test `T_d(X^j)=dX^j` for d|j, else 0 for every j=0..N−1: **448/448 basis monomials PASS**; also signed arbitrary ζ shifted by X^(-3) and q=2^16, q′=q/d show `(q/d)*T_d(X^(-3)ζ)=0 mod q`. A specific N16,d4,q65536,q′16384 example has nonzero raw q′X but complete trace T4(X)=0 and vanishes. No cryptographic keys, error distributions, or runtime were simulated.

## Result and honest scientific decision

**STATUS: FAIL H-HERDS-01** hypothesized surviving modulus-raising offset / **PASS exact algebraic cancellation**. Consistent with source Appendix B.6, **NOT** a paper defect, source bug, new cryptographic attack, noise/security proof or novelty claim. The ordinary noise budget still must include e/d, switching noise and blind-rotation error; the verified identity removes only the q′ζ correction.

**RESULT:** A potentially alarming q/d lifting error is intentionally eliminated by the decoder's exact trace/projection, not silently ignored. This mechanism explains and supports the omission of q′ζ in the final Lemma 6 error expression. The Levis extension-free full-text remains independently SOURCE_BLOCKED; this HERDS trace result does NOT resolve it and should not be conflated with MPS plain-model MKFHE (HERDS uses different bootstrapping/key assumptions).

**NEXT_ACTION:** Do not repeat similar q′ζ toy cases or claim flaw. If PI continues source-grounded HERDS research, select one *different* precise, technically nontrivial security/noise/complexity claim with full source/parameters, e.g. source Theorem 1's O(kn) cost compared with actual gadget-base scaling and q security; focus ONE falsifier, including an actual applicability condition, before further work. If no convincing technical gap beyond textbook trace identities, PARK HERDS screening. Preserve independent SHIP I226 and concurrent vFHE state. **NOVELTY NOT VERIFIED.**

**STATE_UPDATE: YES this one finding only. NO** changes to global STATE.md, SHIP checkpoint, MISSING_SOURCES (Levis already registered), OPEN_RESEARCH_BRANCHES, or upstream code.