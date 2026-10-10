# Iteration 58 — GL transpose via cyclic-diagonal plaintext masks and only small row switches

Date: 2026-10-10
Paper: Craig Gentry, Yongwoo Lee, *Fully Homomorphic Encryption for Matrix Arithmetic*, IACR ePrint 2025/1935 / CRYPTO 2026.
STATUS: PASS (exact algebraic construction), FAIL for a clear novelty claim and for any established performance improvement.
NOVELTY: LOW: plaintext diagonal-mask + rotation + sum is established generic HE permutation methodology; specialization to GL axis-asymmetric row/column rotations may be a memory/runtime tradeoff but no proof of new Pareto point.
Do not conflate with attacks or gaps in the original paper; this is an optional, slower alternative to its correct ordinary transpose mechanism.

## Protocol continuity
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, I57 failure `failures/threshold-ckks-linear-error-expansion-key-recovery.md`, and existing GL/CKL archives including `failures/gl-integer-composite-plaintext-modulus-roots.md`, `failures/gl-gaussian-inversion-fixed-i-naive-map.md`, and CKL complexity records BEFORE attempting the new hypothesis. Following the user-approved continuation, archive previous Threshold-CKKS error-sampler subbranch. STATE.md reserved for parked RIG-HE, untouched.

## Verified full original and prior art
[PRIMARY PAPER] Complete original PDF ePrint 2025/1935 from GitHub fixed mirror, SHA256 `985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84`, 27 physical pages, VERSION_UNVERIFIED. §3.2 physical pp.9–10: encryption uses secret s(X,W) independent of Y and plaintext in extended R'=Z[i][X,Y,W]/(X^n−i,Y^n−i,Φ_p(W)).
§3.6 physical p.16–18:
 - ordinary Hadamard plaintext ct multiplication is component-wise ciphertext multiplication by plaintext m, no key switching; masks can be encoded in ordinary GL plaintext slot basis;
 - row rotation X->X^(5^nu) requires Switchsmall from s(X^(5^nu),W)->s(X,W);
 - column rotation Y->Y^(5^nu) leaves s(X,W) unchanged and needs no switching;
 - transpose swaps X and Y but source key becomes s(Y,W), requiring one *large extended-ring* Switchbig key.
 - p.18 already discusses an alternative transpose via ordinary conjugation plus conjugate transpose reusing a big key already provisioned for matrix multiplication.
 - In p=1 toy case, ζ_j=ζ^(5^j), ζ is primitive 4n-th root and n power of two.
[ADDITIONAL PUBLIC IMPLEMENTATION CONTEXT] DESILO GL documentation https://fhe.desilo.dev/latest/gl_scheme/ identifies 3-axis rotations, transpose and conjugate transpose, but does not prove a performance advantage for this alternate circuit.
[GENERIC PRIOR ART] Jiang et al., *Secure Outsourced Matrix Computation and Application to Neural Networks*, published 2019, open-access https://pmc.ncbi.nlm.nih.gov/articles/PMC6689419/, §3.3 describes homomorphic permutations as diagonalized linear maps using rotations/masks. OpenFHE maintainer https://openfhe.discourse.group/t/generating-all-possible-rotations-of-a-vector-encrypted-in-a-ckks-ciphertext/870/2 discusses mask-and-rotate and BSGS. Therefore no claim that masked transpose or diagonal permutation technique is novel.

## Single primary hypothesis, falsifier and minimal test
[HYPOTHESIS — PASS for algebra] In GL with s(X,W) independent of Y, transpose can be implemented using ONLY n plaintext slot masks, n−1 nontrivial cheap row rotations (Switchsmall), n−1 free column rotations and ciphertext additions, WITHOUT a transpose-specific Switchbig key, provided all small row rotation keys are already provisioned.
[FALSIFIER] A single legal n=4 GL plaintext/ciphertext example for which the masked-rotation sum does not decode to U^T, OR a row/column rotation that unexpectedly requires Y-dependent switching material.
[MINIMUM] Prove universal index identity, then check actual polynomial quotient encoding/ciphertext decryption in ONE complete p=1,n=4 finite-field instance. No GPU/CKKS benchmarks.

## General algebraic construction
Take U∈M_n and define D_d(U)_{j,k}=U_{j,k} if j−k≡d mod n, 0 otherwise. Let (R_a U)_{j,k}=U_{j+a,k} and (C_b U)_{j,k}=U_{j,k+b}, indices modulo n.
Then EXACTLY
 U^T = Σ_(d=0..n−1) R_d C_(−d) (D_d(U)).
Proof: for output (j,k), term d is U_{j+d,k−d} if its source location lies in diagonal index d, i.e. (j+d)−(k−d)≡d ⇒ d≡k−j. At that unique d, source=(k,j), and the output is U_{k,j}. Every other term is masked 0.
In GL, D_d(U) is plaintext Hadamard mask `M_d ⊙ ct(U)`; X automorphism X→X^(5^d) realizes R_d and requires Switchsmall to recover s; Y→Y^(5^(−d mod n)) realizes C_(−d) and requires no switch. Sum n output ciphertexts. For d=0, X rotation identity no switch. Each term remains under common secret s after Switchsmall. The proof is independent of p because mask can be broadcast across W-encoded matrices.
[CRITICAL] All slot masks in exact BGV-like settings require suitable encoding roots; in CKKS their precision is finite, and complex-valued binary diagonal masks are approximate plaintexts (not literally exact zero/one after coefficient rounding). The p=1 finite-field check does NOT certify CKKS approximation/noise/level budget.

## Exact GL quotient-ring verification
[EXPERIMENT] Script `/mnt/data/iteration58_gl_masked_transpose_audit.py` SHA256 `9bd33716329c1078a89ddb5b1657909f986db94f893bfa46a91dcba837f3ba00`.
Ring F_97[X,Y]/(X^4−i,Y^4−i), i=22, primitive order-16 ζ=8; roots ζ_j=ζ^(5^j), j=0..3 equal [8,79,89,18]. Full 4×4 2D inverse Vandermonde encoding; verifies eval(encode(U))=U and all 4 encoded diagonal masks.
Uses fixed-seed random 4×4 U, ternary s(X) independent of Y, random a(X,Y), b=encode(U)−a*s. Computes polynomial componentwise masked multiplication in quotient ring and applies genuine quotient-ring X/Y substitutions. For each row rotation applies IDEAL symbolic key switch `(b',a') ↦ (b'+a'*(σ(s)−s),a')` to isolate semantics: this formula invokes the secret s and is NOT a real public gadget KSK implementation.
Sums 4 branches, checks EXACT **polynomial coefficient equality** of decrypted result vs encode(U^T), as well as eval(decoded)=U^T. PASS. 4 masks; 3 nontrivial X row small switches, 3 Y rotations and 3 ciphertext additions.
The experiment is one exact finite-field construction, no CKKS precision or real security/performance. It does NOT contradict original GL §3.6.

## Real cost and novelty limits
[DERIVED] A big Switchbig key lives in R' with n Y-coefficients and is roughly n times a single R-secret Switchsmall key per equal gadget/level parameters. If the target workload ALREADY provisions all n−1 row rotation keys, this method can avoid a NEW big transpose-specific key. If the workload needs new row rotation keys, n−1 small keys have roughly same raw material as one big key, and the claimed memory saving can disappear.
[DERIVED] One direct transpose big switch costs one extended-ring gadget-switch operation (including Y-axis NTT); masked construction costs O(n) plaintext mask multiplications PLUS n−1 small row-switch operations (each processes n Y coefficients). Hence generally higher online latency/noise; no actual counts/timings measured.
[DERIVED] For standard approximate GL/CKKS, binary diagonal slot masks may require Δ scale and one extra rescale/precision margin. n summands combine errors and n−1 key switches add noise. No direct security problem identified but precision may eliminate usefulness for near-modulus-limit workloads.
[FACT] The source already points out that conjugate-transpose can share the big key used for ordinary matrix multiplication, so transpose has little marginal big-key footprint in multiply-heavy GL applications. Our circuit may have value only in narrowly rotation-heavy key-memory-constrained workloads with row keys already provisioned.
[NOVELTY] Generic permutation with diagonal masks and rotations is extensive HE prior art. We have not found a novel circuit decomposition, optimality bound or practical Pareto improvement specific to GL. Archive as correct but weak candidate, not proposed publication.

## End of iteration
STATUS: PASS for exact algebraic construction; FAIL for novelty / measured improvement.
RESULT: Proved and exactly checked transpose Σ_d R_d C_-d(D_d(U)) under GL encoding and ideal row Switchsmall; removes transpose-specific Switchbig if existing row keys are available, trading for n masks and n−1 switches. No new security result or verified CKKS performance.
NEXT_ACTION: ARCHIVE this GL mask/rotation tradeoff; do NOT allocate CKKS implementation or variants without a concrete workload already provisioning all row keys and a predeclared memory-vs-runtime objective. For the next independent FHE/ZK research iteration, select one **full-text verifiable** vFHE/SNARG construction and audit an explicit algebraic reduction/soundness assumption; ePrint 2026/027 currently suffers a Research MCP zero-padding metadata bug (it normalizes 027 to 27 yielding 404) and should NOT be treated as read until reliable full PDF can be obtained. If not accessible, choose another fully retrieved FHE/ZK paper.
STATE_UPDATE: NO — parked RIG-HE STATE.md unchanged.
