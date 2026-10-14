# CKL independent audit CKL-01 — Subring CMT trace normalization requires d invertible in ciphertext coefficient modulus

**Date:** 2026-10-15 (Asia/Tokyo). Human PI said continue. This is a **new independent source-complete** technical audit, NOT V40 and NOT reopening vFHE V39 SOURCE_VERSION_GATED/HUMAN_REVIEW; globally frozen I192 stays untouched, SHIP I226 untouched. Read-before-write START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, current STATE.md showing **vFHE V39 COMPLETE/V40 HUMAN_REVIEW**, findings/vfhe-cross-crt-state.md, OPEN_RESEARCH_BRANCHES.md (separate CKL/RNS composition branch already archived, but this modulus edge was not among the indexed CKL findings). A read attempt confirmed no file exists at this exact new path before creation.

## ONE primary falsifiable hypothesis and cheapest decisive test

**H-CKL-01 (OUR test, not a quoted author claim):** The original CKL §5.1 subring ciphertext-matrix transpose CMT has an invertible, implementation-independent subring coefficient-extraction step for **all** q≥2 allowed by its preliminary R_{q,N} notation, including q=2^w, with N=dk and d>1 a power of two, using the stated trace Tr^N_k and a d^{-1} modular normalization.

**Falsifier:** Inspect original CKL §2.1 q≥2, §2.4 definition and explicit identity Tr^N_k(m)=d*m0(Y), §5.1 Adjust normalization d^{-1}, and Algorithm3; demonstrate a legal small even modulus q and two different plaintext subring components with identical trace, while an odd modulus q with d invertible recovers component exactly. This checks the algorithm *as written*, not possible redesigns that extract coefficients without trace nor concrete HEaaN implementation parameters.

## Original source provenance [FACT]

- Jung Hee Cheon, Minsik Kang, Junho Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, IACR ePrint **2025/1957**, https://eprint.iacr.org/2025/1957, complete 32 physical-page Research MCP GitHub original full-text public mirror, SHA256 **ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a**, **VERSION_UNVERIFIED** versus current publisher/official revised binary. External official ePrint PDF HTTP403 and public raw mirror web cache miss, but authenticated MCP PDF text clearly includes required formulas. No visual screenshot of exact PDF was obtainable through web; formulas here were also checked against independent integer computations.
- Original physical p8 §2.1 explicitly defines R_{q,N}=Z_q[X]/(X^N+1) for N power-of-two and **q≥2** with no primality/oddness attached to notation.
- Original physical p11 §2.4 defines H={2kt+1 : t∈[d]} in (Z/2N)×, trace Tr^N_k=Σ_{h∈H}σ_h, and ‘Tr^N_k(m)=d*m0(Y)’ for m=Σ_{i<d}m_i(Y)X^i and Y=X^d; says this discussion extends to R_{q,N}.
- Original physical p18 §5.1 uses normalization **d^{-1}** in the Adjust step, from Tr^N_k(X^{-i}m_j)=d*M_{i,j}; physical p20 Algorithm3 line4 writes **(d^{-1} mod Q)*aux**, where Q is the active ciphertext modulus in that pseudocode. Requirement is really gcd(d, active Q)=1 for that step; do not silently conflate manuscript q with its Algorithm3 Q unless they are the same step modulus.
- Original physical p25 §7.1 implementation uses **HEaaN CKKS**, which commonly uses RNS odd primes; the paper's Table4 parameters are not fully authenticated here. Thus NO claim actual CKL benchmark contains a broken even-Q instantiation, and no challenge to its reported CKKS timings.

## Exact ring computation and decisive collision [DERIVATION/EXECUTED]

Choose N8,k4,d2,Y=X² and H={1,9}. For each coefficient q, negacyclic R_{q,8}=Z_q[X]/(X^8+1); σ_9(X)=X^9=−X, σ_9(X^{2j})=X^{2j}; hence Tr^8_4(m)=m+σ_9(m)=2*m_even(Y). The trace projection onto even-exponent subring is therefore multiplication by 2.

For **q16** (allowed by unqualified q≥2 notation), distinct constant plaintext polynomials m1=0 and m2=8 satisfy Tr(m1)=0 and Tr(m2)=8+8=16=0 in Z_16. Both have distinct nonzero subring components m0(Y), but same complete trace. This is a genuine **noninjective information collapse**, not merely lack of an inverse formula: NO deterministic or randomized algorithm given ONLY Tr(m) can always recover the original m0(Y). For any even modulus q with d even, choose m2=q/gcd(q,d) in the constant position; d*m2=0 modq while m2≠0. More generally, recovering m0 as an R_q-linear functional of d*m0 needs d a unit, equivalently gcd(d,q)=1.

For **q17**, gcd(2,17)=1 and 2^{-1}=9 mod17; multiplying every trace coefficient by 9 exactly recovers m0(Y). For **q97**, inverse49 similarly. For even q32, distinct constant m0=0 and m0=16 collide under trace. Thus odd active modulus is sufficient when d is a power of two. The source original CMT modulo-Q 'd^{-1}' step needs gcd(d,Q)=1 (or a different exact coefficient extraction method).

Executed a self-contained standard-Python ring implementation, using σ_h monomial reduction modulo X^8+1 and summing traces at H={1,9}, for q∈{16,17,32,97}. For each q verified all 8 polynomial basis elements and 64 additional deterministic polynomials obey Tr(m)=2*m_even(Y). For odd q verified recovery by inverse for 64 further polys. For even q verified zero-trace collision as given. All asserts pass.

**Reproducibility files:** `/mnt/data/ckl_cmt_trace_modulus_gate.py`, SHA256 `66e7d4e51b14dbf9fcb61be81a2024e7f042a94f7620fb4fbd08ea18ecfe315a`; `/mnt/data/ckl_cmt_trace_modulus_gate_results.json`, SHA256 `a17ee09cf1151d17a2733317187784ff407ec51fd466364604291a8943447516`. This is plaintext ring-level algebra, NOT a ciphertext run, FHE DFR check, or formal noise proof.

## Implications, limits, novelty

**STATUS: FAIL H-CKL-01** universal q≥2 no-adjustment compatibility. **PASS** mathematically exact necessary invertibility condition and original-style small counterexample; odd-modulus positive control. **RESULT:** The §5.1 trace-based CMT as written does not directly port to even active coefficient modulus q/Q when d shares a factor. This is an **algebraic scope/portability precondition**, not a proved cryptographic attack or correctness problem for CKKS when q or Q is the usual odd RNS modulus.

Possible alternative CKKS behavior: rational plaintext scaling, approximate 1/d encoding with separate rescale, or coefficient-extraction redesign might avoid explicit modular inversion at extra precision/level/key cost, but NONE of these repairs is constructed or verified here. To make a novel contribution would require an actually efficient invertibility-free CMT for even-modulus RLWE and a concrete advantage/soundness/noise theorem over known methods. The classical group-trace averaging invertibility condition is elementary/known; **NOVELTY NOT VERIFIED** and this alone is NOT publishable.

**NEXT_ACTION:** **PARK this exact trivial even-modulus CMT scope audit**, because the authors' implemented CKKS likely uses odd Q and the premise is apparent at original §5.1. If PI independently asks for even-modulus CMT port, pursue a distinct one-hypothesis design with exact ring-linear obstruction/security/precision budget; otherwise pick a new source-complete FHE gap rather than repeated q-parity tweaks. Do NOT advance vFHE V40 while true Feb2026 original ePrint remains unverified; its independent state remains V39/HUMAN_REVIEW. No author outreach.

**STATE_UPDATE: YES this ONE independent finding only. NO edits to root STATE.md, independent vFHE state, SHIP state, OPEN_RESEARCH_BRANCHES.md, prior CKL branches or paper author's source.**