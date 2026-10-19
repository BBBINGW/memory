# BOOT-B006: squared-gadget vs heterogeneous approximate-gadget interface

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B006
STATUS: FAIL_DIRECT_PORT / PASS_NOISELESS_FALSIFIER / REFINE_P2
STATE_UPDATE: YES

## Primary hypothesis
[HYPOTHESIS] The heterogeneous approximate gadget parameters (B_i,d_i,delta_i) from Hong–Lee (ePrint 2025/1892) can be dropped into the squared-gadget Mat-MGSW external product of Wang–Luo–Xia–Wang–Hou (ePrint 2025/1711), without changing the square matrix format or the output scale Q/T, preserving correct multiplication and potentially reducing time/key size.

## Sources checked
[FACT] ePrint 2025/1711 version-UNVERIFIED mirror PDF SHA256 0f003b5e91dfb6acd4bb48103e03127e0da94394544aa24eda1b636676ca57ff, 29 physical pages. Phys. pp. 4–7 (intro technical overview), 10–16 (Section 3.1 scale-based construction, Lemma 3.4 proof, Corollary 3.5 and transform costs), 17–20 (Algorithm 1, Theorem 4.1, Table 1) read via Research MCP extracted PDF text. External ePrint HTTP 403; source mathematical symbols may be garbled by extraction; formulas reconstructed from explicit prose and repeated displays. No visual screenshot of original PDF could be obtained via web due blocked downloads.
[FACT] ePrint 2025/1892 mirror PDF SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, VERSION_UNVERIFIED. Phys. pp. 11–13 read: Theorems 3.1–3.2 and approximate gadget lengths d_i, bases B_i and rounding factors delta_i.
[FACT] ePrint 2025/1711 Sec. 3.1 Mat-MGSW uses T>Q, C in R_T^((k+r)x(k+r)), with message encoded using (T/Q) times an identity-like square block, and Vec-MLWE c in R_Q^(k+r) lifted canonically to R_T. Product is coefficientwise round((Q/T)*(C c mod T)) mod Q. No G^{-1}(c), no variable digit count d in this external product. Type-III approximate gadget is discussed as another external-product/key-switching construction in the related overview on p.4.
[FACT] ePrint 2025/1892 optimizes a traditional multicolumn RGSW gadget and its h'_{B,delta}; this maps c into a vector of 2d digit polynomials and multiplies by a rectangular key matrix. It is not an operation in the square scale-based Mat-MGSW product.
[FACT, current implementation context] OpenFHE 1.6.0 development announcement dated September 29, 2026 reports incorporation of a granular FHEW/TFHE parameterization method from 2025/1892. https://openfhe.discourse.group/t/v1-6-0-development-is-released/2389 . Thus even the hetero gadget design is actively implemented prior art, and novelty cannot be claimed for parameterization alone.

## Cheapest decisive falsifier: noiseless, 2x2 matrix with modified signal scale

[ASSUMPTIONS] Degenerate correctness-only toy (not secure): R = Z[x]/(x+1) ~ Z, module rank k=1, number of message coordinates r=1, secret S=0, A=E=0, message m1=1. Q=16, T=128, plaintext modulus t=8, input message m2=2, and Vec-MLWE input c=(Q/t*m2,0)=(4,0). This is within centered [-Q/2,Q/2] range.

[DERIVATION] Native square ciphertext for unit message:
    C = [[T/Q,0],[0,0]] = [[8,0],[0,0]].
Native external product
    round((Q/T) C c) mod Q = (4,0);
Vec-MLWE decoding round((t/Q)*4)=2, equal to m1*m2.

[DERIVATION] Attempt a naive approximate-gadget scale delta=2 with unchanged product and matrix shape:
    C_delta = [[T/(Q*delta),0],[0,0]] = [[4,0],[0,0]].
Then round((Q/T) C_delta c) mod Q = (2,0), decoded round((t/Q)*2)=1 !=2. Algebraic correctness FAILS with zero encryption noise and no modular overflow. This is a counterexample to the naive *translation*, NOT to either original paper (which never prescribes this direct substitution).

[DERIVATION] Repair by changing final scaling to (delta Q/T):
    round((delta Q/T) C_delta c) = (4,0), decoder gives 2. But this trivially cancels the attempted signal-scale reduction. For fixed T and same matrix dimension it does not reduce ring multiplication count, transforms, or nominal key dimensions; any additive encryption error in C_delta is amplified by factor delta in the final rescale. More complex tradeoffs require independent error/security analysis; no concrete benefit established.

[DERIVATION] Structural cost contrast for module dimension h=k+r: conventional d-level gadget external product has h(d+1) transforms and h^2 d pointwise ring products under the complexity accounting in 2025/1711 Sec. 3.3; squared-gadget has 2h transforms and h^2 pointwise products irrespective of traditional d. Thus changing d in 2025/1892 provides no direct cost coordinate in the squared-gadget operation. Both schemes' modulus/ring-security parameters may differ; these are structural operation counts, not end-to-end timing comparisons.

## Alternative interface worth one test
[SPECULATION] An *independently defined* heterogeneous scale modulus T_i, with constant Q and common module ring and dimension, is algebraically plausible: each key C_i in R_Ti^hxh uses scale T_i/Q and outputs a ciphertext in R_Q^h, so the next step could canonically lift it into R_T(i+1)^h. For noise-free monomial/identity messages with Q|T_i and no centered-lift overflow, the output is M_i c mod Q at each step. Unlike changing the gadget digit length, varying T_i could trade larger Mat-MGSW key size (roughly proportional to log T_i), modulus-specific arithmetic, and external-product noise (see Lemma 3.4).
[UNPROVED] General correctness with rounding and negative-coefficient centered lifts; tight failure probability under adaptive operations; security of combined key distributions for different T_i; per-modulus FFT/NTT preparation/hoisting overhead; whether actual T_i choices yield a Pareto improvement over one optimal T; novelty relative to prior art. Important: 2025/1711 Table 1 assumes a single T and notes T must be large enough for noise and security; not permissible to simply reduce T_i at will.
[DERIVATION] A two-step toy where T_1=128, T_2=256, Q=16, centered c_0=(4,0), M_1=M_2=1, and exact zero-noise keys returns c_1=c_2=(4,0). This is only shape/correctness feasibility in trivial case, not evidence of acceleration.

## Decision / next action
STATUS: FAIL_DIRECT_PORT / REFINE_P2
RESULT: no direct 2025/1892 (B,d,delta) degrees of freedom exist inside 2025/1711's squared-gadget external product, and naive signal re-scaling demonstrably loses correctness. A compatible alternative might be heterogeneous Mat-MGSW key moduli T_i, not the 1892 decomposition as such. This is a new hypothesis to falsify, not an established improvement.
NEXT_TEST B007: fix Q,N,k,r and restrict to permitted T_i that satisfy the 2025/1711 correctness/security assumptions; derive a per-key noise contribution as a function of T_i and explicit key byte size plus transform cost. Attempt to kill all non-uniform T_i schedules by convexity/symmetry or modulus-switching cost. Compare to uniform T and original 1711 parameters; no speedups before equal-security comparison and prior-art audit.
STATE_UPDATE: YES
