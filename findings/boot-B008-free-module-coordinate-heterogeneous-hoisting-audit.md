# BOOT-B008 — Free-module coordinate-heterogeneous gadget: rotation-equivariance falsifier

TRACK_ID: BOOT
ITERATION: B008
DATE: 2026-10-19
STATUS: FAIL_NAIVE_HOISTED_COORDINATE_DECOMP / SOURCE_BLOCKED / HUMAN_REVIEW
STATE_UPDATE: YES
NEXT_TEST: B009 P4 (ePrint 2025/686 × 2025/696; source PDFs are available). Leave P3 unclosed until a verified full-text copy of 2025/1753 is supplied.

## Primary hypothesis
[HYPOTHESIS — specifically an independently proposed composition, not a description of source] For free-module accumulator coordinates and coordinate-dependent approximate gadget resolutions h_j (inspired by Hong–Lee ePrint 2025/1892), we may hoist a single coordinatewise decomposition D_h(c), reuse its result after module monomial rotation P, and obtain exactly the same result as re-decomposing Pc with the same fixed heterogeneous parameter profile: P D_h(c) = D_h(Pc) for all c.

## Source and provenance
[FACT — official HTML abstract only] Ruida Wang, Jikang Bai, Yijian Liu, Xinxuan Zhang, Xianhui Lu, Lutan Zhao, Kunpeng Wang, Rui Hou, "Bootstrapping over Free R-Module", ePrint 2025/1753, https://eprint.iacr.org/2025/1753 . The IACR official abstract introduces the free R_N module M = direct sum_{i=0}^{tau-1} R_N X^i to decouple input modulus q from base dimension N; its latest revision date shown is 2026-04-15 (second revision). The official abstract states a 1.40x–2.77x experimental improvement over sorted extended bootstrapping; these are authors' own reported results. The *PDF / detailed algorithms / theorems were NOT read*.
[SOURCE FAILURE] Research MCP get_eprint_paper(2025/1753) returned INVALID_PDF. Official PDF HTTP 403; exact-title arXiv fallback unavailable; GitHub ePrint mirror rejected due PDF title identity mismatch. Web PDF click likewise HTTP 403; broad/targeted web searches revealed no trusted exact paper full-text. The BOOT repository papers/supplied did not contain 2025/1753 as of this round. NEVER use a wrong-title mirror as proof of what the paper actually implements.
[FACT — PDF physically read, mirror version unverified] Hong–Lee, "Optimizing FHEW-Like Homomorphic Encryption Schemes with Smooth Performance-Failure Trade-Offs", ePrint 2025/1892, Theorem 3.1 and 3.2, PDF pp. 12–13, SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018. These theorems parameterize independent RGSW blind-rotation KEY instances by gadget base B_g,i, length d_g,i, and approximation delta_i, not independent free-module coordinates. Translating key-wise heterogeneity to *coordinate-wise* heterogeneity is an additional new hypothesis and must not be attributed to the source.

## Cheapest decisive algebraic test (abstract algebra only)
[DEFINITION] Define A=Z_32[X]/(X^2+1), which is a free rank-two module over R=Z_32 with basis (1,X). Multiplication by X on coefficients is P(a,b)=(-b,a) mod 32. This is a mathematically valid toy for investigating a *cyclic* free-module coordinate rotation, but is NOT claimed to be the specific algebra or algorithm of 2025/1753.
Define h_0=4,h_1=8 and D_h(a,b)=(round-to-nearest-multiple-of-4(a),round-to-nearest-multiple-of-8(b)), residue classes mod 32. The counterexample uses no tie cases.
[DERIVATION] Take c=(5,0). Then D_h(c)=(4,0), P D_h(c)=(0,4); whereas Pc=(0,5), D_h(Pc)=(0,8), unequal mod 32. Hence fixed-profile heterogeneous scalar quantization and cyclic module rotation DO NOT COMMUTE. This kills any implementation optimization that assumes P D_h = D_h P for *all inputs*.
[INDEPENDENT TEST] Python integer reference enumerated all centered coefficient pairs (a,b) in [-16,15]^2, excluding values tied at either nearest-4 or nearest-8 boundaries; 400 pairs remain, 256/400 violate P D_h=D_h P. This is a toy algebraic enumeration, NOT a native TFHE test nor evidence of a correctness issue in either original paper.

## General necessary condition for rotation-equivariant coordinate profiles
[DERIVATION] If an operator P shifts the module basis components transitively and, away from its wrap, (Pv)_{j+1}=v_j, while D=(D_0,...,D_{tau-1}) acts coordinatewise, P D = D P for all v implies D_j(z)=D_{j+1}(z) for all z. Thus for a single cyclic orbit all coordinate quantization operators must coincide (up to any explicit conjugation by the wrap automorphism). This is a necessary condition for reusing a fixed coordinatewise decomposition under rotation, NOT a sufficient condition for full ring/FHE correctness. Parameter profiles may instead move with data: D^(new)=P D P^{-1}; this trivially restores D^(new) P = P D, but costs and key representation may change.
[DERIVATION] Recomputing D after each rotation also avoids the algebraic obstruction, but loses the *specific* proposed pre-decomposition reuse. There is no proof that free-module bootstrapping requires hoisting or that its source operation uses this P.

## Cost, security, and novelty gate
[FAIL] The naive hoisted fixed-coordinate heterogeneous-gadget reuse fails in a 2-coordinate zero-noise counterexample.
[UNCLEAR] Independent per-update heterogeneity can still be algebraically possible and is already common in 2025/1892 for RGSW key instances. A module-specific speedup would require the exact 2025/1753 ciphertext/BSK structure, multiplication implementation, noise and key layout to identify saved transforms/products/storage without illegal reuse. Not possible from abstract alone.
[UNCLEAR] No source-grade algorithm/page of 2025/1753 to confirm whether the module multiplication permutes components in precisely this form, whether a hoisted decomposition is part of its construction, or whether componentwise gadget choices even exist. No security/DFR/benchmark or novel algorithm established. Do NOT archive the entire P3 theory from this toy result.

## Decision and work continuity
STATUS: FAIL_NAIVE_HOISTED_COORDINATE_DECOMP / SOURCE_BLOCKED
RESULT: A specific tempting optimization (fixed-frame coordinate-heterogeneous hoisting) is algebraically false in a natural cyclic free-module toy. Authors' actual 2025/1753 algorithm remains unaudited. Request an authenticated copy of ePrint 2025/1753 (prefer 2026-04-15 revision or later) under papers/supplied/2025-1753.pdf to continue source-faithful P3.
NEXT_TEST: While P3 awaits verified PDF, BOOT B009 moves to independent P4: interaction between amortized bootstrapping 2025/686 and incomplete-NTT 2025/696. Both source PDFs were acquired as VERSION_UNVERIFIED mirrors and can be read, but check exact latest versions and algebra before any conclusions.
STATE_UPDATE: YES, only BOOT files may be changed.
