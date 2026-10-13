# Iteration 170 — Directly collapsing source-compatible BGV homomorphic NTT into one diagonal transform loses butterfly sparsity

**Date:** 2026-10-13 (JST +0800 session); PI “好的，请继续” after I169 recommendation to PARK textbook public-basis AKS key synthesis. Interpreted as consent to PARK **that generic AKS microline**, not a claim all AKS research is exhausted. ONE new FHE paper, ONE primary hypothesis and ONE exact finite-field falsifier. No FHE implementation or author-performance/precision/security assertion.

## Read-before-write, provenance, source gate

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I169 blob SHA `b90354b6b598a8effebdd60e81fde427b68cad3d`, `findings/OPEN_RESEARCH_BRANCHES.md`, and I169 archive. Avoid reopening source-blocked vFHE P1, SPRU noise, CKKS p1-only fitting, TFHE HFP covariance, AHE Algorithm3 or generic AKS key linearity. External original sources were investigated. ePrint **2024/115** (Ma et al. BGV large-p null-polynomials) was considered but **Research MCP returned INVALID_PDF/RETRIEVAL_BLOCKED**, so no unsupported original-source claim was made. Another candidate ePrint 2026/811 remained unacquired due RETRIEVAL_BLOCKED. SHIP ePrint 2025/784 and mean-compensation TFHE ePrint 2025/809 were acquired/read briefly but not chosen for this iteration as their initial apparent bottlenecks were already openly discussed. ONE selected target below.

**Primary selected source [FACT]:** Shihe Ma, Tairong Huang, Anyu Wang, Xiaoyun Wang, *Faster BGV Bootstrapping for Power-of-Two Cyclotomics through Homomorphic NTT*, IACR ePrint **2024/164**, https://eprint.iacr.org/2024/164, complete **42 physical pages** via Research MCP `github-mirror`, SHA256 `89099f7efc7ab93d1e8b15d2e13c345d0493028f364ac8d9cf3cce289a43abd4`, official latest revision parity **VERSION_UNVERIFIED**. Inspected §2.6–§3 physical pp11–14 (NTT/iNTT definition, Theorem1, p=1mod4 sparse stage structures), §4.1 p21 (level-collapsing tradeoff and Lemma8 diagonal-support upper bound), §4.3 pp24–25 (bit-reversal is deliberately absorbed, no hidden free BR assumption). Text extraction of some formulas has glyph warnings; key parameter and structural formulas were clear and independently derived.

## ONE primary hypothesis and cheapest decisive falsifier

**[HYPOTHESIS TO FALSIFY]** For the paper's p≡1 mod4 power-of-two cyclotomic BGV NTT, all several 1D sparse layers can be collapsed into **one** slot-diagonal linear transform **while still keeping at most three cyclic nonzero diagonals overall** (i.e. depth savings with the same sparse plaintext-diagonal support, without relying on a different representation or BSGS rearrangement).

**[FALSIFIER]** Instantiate a valid source p≡1 mod4 example with L>3 and compute the exact original polynomial coefficient-block to CRT factor map, checking every coefficient of its L×L coefficient-block matrix over F_p. If it has >3 nonzero cyclic diagonals, the proposed universal sparsity-preserving one-layer collapse is false. Invert matrix exactly as independent algebraic correctness check and relate the source's stated level-collapsing tradeoff; DO NOT derive hardware latencies or treat BSGS rotation counts as number of diagonals.

## Exact source-compatible finite-field CRT case

Let cyclotomic order `M=512` and plaintext prime `p=97≡1 mod4`. p is coprime to M. Direct exact modular order computation gives
```
 Φ_M(X)=X^256+1  over F_97,
 d=ord_512(97)=16,
 L=φ(512)/d=256/16=16,
 D=L/2=8, two-slot (minor) dimension2.
```
This matches source Theorem1(1) p≡1 mod4, with `log2(D)+1=4` sparse NTT-like stages (3 major plus 1 minor).

A primitive 32nd root in F97 is `ζ=19` (`ζ^32=1,ζ^16=−1` mod97). Let `ω=ζ²=70`, a primitive 16th root, and `α_j=ζ^(2j+1)` for j=0,…,15. They are precisely the 16 distinct 16th roots of −1 in F97, so
```
 X^256+1 = ∏_{j=0}^{15} (X^16−α_j)  in F97[X].
```
Each factor is degree16 irreducible because roots of X^16−α_j are primitive 512th roots and ord_512(97)=16. Group coefficients as `m(X)=∑_{k=0}^{15} X^(16k) m_k(X)`, where deg m_k<16. Then the source's exact CRT coefficient-block map Red is:
```
 y_j(X)=m(X) mod (X^16−α_j)= ∑_{k=0}^{15} α_j^k m_k(X).
 V_{j,k}=α_j^k = ζ^k ω^(jk) ∈ F97*.
```
ALL 256 matrix entries are **nonzero** field units. In particular the cyclic diagonal support of V is `{0,1,...,15}` (16 diagonals), regardless of permutation of its rows/columns; in a direct naive single diagonal linear-transform expression there can be no 3-diagonal representation of the whole full-coordinate map.

The exact inverse is
```
 W_{k,j}= 16^(-1) ζ^(−k) ω^(−jk) mod97,
 WV=I mod97,
```
which was checked exhaustively for all 16×16 entries with integer modular JS arithmetic in `functions.exec`. W also has all 256 entries nonzero. The 16 distinct α_j were checked and the equality α_j^16=−1, ζ orders and `WV=I` asserted; all PASS. Sample first V rows: row0 = sixteen 1's; row1 starts `[1,19,70,69,...]` under first factor ordering (source output enumeration may use different coset representatives). The straightforward standard binary-butterfly *support envelope* on a 16-point NTT grows from {0,8} to 4, then 8, then all16 cyclic shifts when layers are folded; however that generic butterfly support check is **not** a claim that the paper's particular individual `N_j` matrices each have exactly two diagonals. The exact dense V,W suffices.

**[Crucial cost distinction]** The paper Theorem1 gives source-specific sparse sublayers with ≤3 diagonals each (for major dimension; plus minor), and §4.1 **explicitly already discusses combining layers to trade depth for time**, giving **upper** diagonal support Lemma8. This iteration verifies that a fully collapsed map can be dense; it does NOT determine optimal BSGS key count, exact rotation runtime, plaintext multiplications with hoisting, level rescale implementation or practical encrypted HElib throughput. BSGS can reduce rotations **without** reducing the number of nonzero diagonals; do NOT claim lower bound of 16 rotations. The generic direct diagonal expression needs 16 nonzero diagonals in this coordinate-block basis; no universal lower bound against all other factorization or alternative SIMD algorithms is implied.

## Decision, not a paper bug

**[FAIL narrow primary hypothesis]** There is a valid and exactly computed paper-compatible parameter set where the overall direct CRT matrix is fully dense; merely fusing the existing sparse NTT layers into a single diagonal map cannot retain three-diagonal sparsity. The source's already-known `depth vs support/time` tradeoff is therefore REAL, not a new overlooked optimization.

**[FACT original paper already handles]** §4.1 starts by noting each `MatMul1D/BlockMatMul1D` consumes constant-mult depth, so all layers cost `log2 L`, and combining consecutive stages reduces depth while increasing support and possible time; source Lemma8 bounds `DiagSet` growth. §4.3 explicitly says the bit-reversal permutations `BR` and inverse are **not** evaluated homomorphically; source tracks permuted slot layout across digit-removal stages. There is no newfound missing permutation-cost gap in the inspected explanation. The paper's reported 2.4–55.1x throughput improvements remain separate benchmarks, not reproduced or contradicted here.

**[Novelty/scope]** DFT/Vandermonde density under factor CRT and radix-2 butterfly fill-in is **elementary known FFT algebra**, not publishable in itself. This ONE gate should promptly **PARK 'free no-density layer collapse'** rather than expand parameter sweeps. The original Galois-ring p^r extension, BSGS implementation details and §4.3 basis/permutation optimization are not attacked.

## End of Iteration 170

**STATUS:** **FAIL** universal sparse-to-one-layer 3-diagonal hypothesis; **PASS** exact source-compatible `M512,p97,d16,L16,D8` CRT diagonal-support counterexample and inverse check; **UNCLEAR** any practical alternative performance or novel contribution.
**RESULT:** All 16×16 CRT coefficient-block map entries and inverse entries nonzero in F97, so all 16 cyclic diagonals survive when direct transform is formed; source's multilevel layers cost low diagonal counts but consume multiplicative depth, and §4.1 explicitly describes the tradeoff. No paper error, implementation or latency gain.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK** this free-collapse/bit-reversal suspicion as known source-treated issues. A next research attempt should target a **different, source-available FHE bottleneck** with credible *new* complexity/noise/security idea and specific performance frontier; inspect backlog before choosing and resist toy restatements. The original source, paper mirror, numerical CRT matrix case and conditional SHA have been recorded. vFHE P1 OPEN/SOURCE-GATED and prior archives remain.
**STATE_UPDATE:** **YES** — PI assent parks generic I168–169 AKS key linearity; new BGV source and exact failed collapse gate archived; no other prior research changed.
