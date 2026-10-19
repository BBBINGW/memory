# BOOT — Independent Bootstrapping Optimization Track

TRACK_ID: BOOT
STATUS: HUMAN_REVIEW
LATEST_ITERATION: B001
DATE: 2026-10-19

## Scope and isolation
New independent research line on combining bootstrapping optimizations. Read-only prior-art comparison allowed; do not modify SHIP, CGS, VFHE, EXPLORE, or global STATE. BOOT owns findings/boot-* and failures/boot-* only. This initial state must not be mistaken for an established new construction.

## Sources and verification
- Hong–Lee, ePrint 2025/1892, manuscript mirror SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, version unverified, physical pp. 11–13 examined.
- Lee et al., ePrint 2023/958, mirror SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de, version unverified, physical pp. 3–6 examined.
- Other comparison papers: 2025/1711, 2025/1753, 2025/686, 2025/696, 2026/853, 2026/975, 2025/1935 (initial abstract-level map only).

## B001 Primary hypothesis
[HYPOTHESIS] Block-binary TFHE (2023/958) can support blockwise heterogeneous approximate gadget decomposition modeled on Hong–Lee (2025/1892), with one common gadget format per block and different formats across blocks; this may improve constrained latency/key-size/DFR Pareto optimization over uniform gadget settings.

## Cheapest decisive test and result
[FACT] Hong–Lee Theorems 3.1–3.2 already permit heterogeneous base and approximation factors per RGSW operation; reported CGGI variance is additive over operations (pp. 12–13). Their CGGI exact cost expression does not apply mechanically to a block-binary blind rotation.
[FACT] Lee et al. (2023/958) block-binary distribution puts at most one 1 in each block. The blind rotation processes each block with one external product after combining selector TRGSWs (pp. 3, 6). Its security changes with block dimension and entropy, so original binary-secret security estimates cannot be reused.
[DERIVATION] Toy block selector: if s=(1,0) and E_1=Enc_G(X^{a_1}-1), E_2=Enc_G(X^{a_2}-1), then Enc_G(s_1(X^{a_1}-1)+s_2(X^{a_2}-1))=E_1 (up to noise). Same common gadget G is required to add ciphertext rows componentwise. Distinct bases or gadget lengths inside one selector combination have incompatible shapes without an explicit conversion interface. Thus naive per-coordinate heterogeneous gadgets DO NOT directly compose with the block selection technique. Setting common G_j within block j, different G_j across blocks, removes this algebraic shape obstruction.
[OPEN] Whether cross-block noise variance is additive with the same independence and conditioning assumptions as in Hong–Lee; whether selector construction changes noise factor, dependence, runtime, key size, or DFR; whether the combined optimizer improves over already-optimized baselines at the same measured security. Not proved.

STATUS: HUMAN_REVIEW (a structural compatibility condition is identified; not a validated optimization).
RESULT: Restrict heterogeneity to the selector's composition unit (block), rather than individual secret coordinates, unless conversion is developed. This is a plausible interface, not a new theorem.
NEXT_TEST: Read 2023/958 full block blind rotation algorithm + noise bound and 2025/1892 Thm 3.2 in source; derive exact blockwise noise covariance and cost with unequal (B_j,d_j,delta_j), construct a two-block symbolic/toy counterexample to naive independence, then security estimate and benchmark against uniform block keys.
STATE_UPDATE: YES.

## Further gates
Cross-algebra combinations (MRFHE / matrix FHE / BFV sparse packing) deferred until interfaces and conversion costs established. Compare recent prior art including 2025/1711 squared gadget and 2025/1753 module bootstrapping; no claims of novelty or speedups yet.

## B002 — 2026-10-19 — Falsify direct blockwise scalar DFR transfer
STATUS: FAIL for naive variance/erfc transfer; PASS for single-gadget-per-block structural compatibility.
RESULT: 2023/958 Algorithm 2 combines all ell_j TRGSW keys including zero-secret keys; they contribute fresh encryption noise. Tiny N=4 exact linearized Gaussian example yields Var((X^a-1)e)_0 in {0,2,4}beta^2 depending on exponent. Mixing over public a produces non-Gaussian tails: at t=5beta exact 0.0018576303 versus mean-variance erfc estimate 0.0004069520. Exact conditional fresh-key variance equals beta_j^2 sum_{i,r} ||rho M(h_{j,r})(T_{a_i}-I)||_2^2, with conservative upper bound 8 beta_j^2 ell_j d_j N D_j^2 per output coefficient if digit norms <=D_j. This does NOT establish concrete full-bootstrapping DFR, exact approximate-gadget residual, or practical speedup. Full technical record: findings/boot-B002-block-key-noise-heterogeneous-gadget-audit.md.
NEXT_TEST: B003 source-faithful mixed-vs-uniform block gadget parameter comparison with 2023 real parameter sizes and independent noise/DFR and security gates; kill if overhead or bounds negate advantage.
STATE_UPDATE: YES. Other tracks unchanged.
