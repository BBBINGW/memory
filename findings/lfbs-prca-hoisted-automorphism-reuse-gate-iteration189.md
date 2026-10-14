# Iteration 189 — Standard Halevi–Shoup hoisting cannot reduce PRCA binary-tree key-switch calls by sharing across equal automorphism indices

**Date:** 2026-10-14 JST. PI authorized exactly ONE continuation. Read START_RESEARCH_SESSION.md → RESEARCH_PHILOSOPHY.md → AGENT.md → STATE.md after I188 SHA `fe680d0b786039c3edfd8005c94521c13bcf6178`, I188 finding and branch index. One primary test of **unmodified PRCA Algorithm5 + conventional hoisting**; no ciphertext implementation/benchmark and no universal packing lower bound.

## Primary source [FACT] and provenance

1. **Zhihao Li et al.** *Leveled Functional Bootstrapping via External Product Tree*, IACR ePrint **2025/022**, https://eprint.iacr.org/2025/022, full **35 physical-page official web PDF** https://eprint.iacr.org/2025/022.pdf, text/web source `turn374480view0` (PDF p16–17, printed pp17–18). Prior I188 archive holds author metadata, exact per-PRCA count `B−1+log2(N/B)`, and note Table3's O(logN) expression requires a fixed-small-B or restricted-B interpretation. Research MCP acquisition remained `SOURCE_UNAVAILABLE` because apparently normalizes leading-zero ePrint ID 2025/022 incorrectly to 2025/22; no verified current PDF SHA or edition. Web PDF screenshot (p17 zero-index) attempted in I189 but returned HTTP403. Hence primary math source is accessible PDF text but image glyph parity still unverified.
2. **Shai Halevi and Victor Shoup**, *Faster Homomorphic Linear Transformations in HElib*, CRYPTO2018, IACR ePrint **2018/244**, https://eprint.iacr.org/2018/244. Read complete source through Research MCP, **25 physical pages** `github-mirror` PDF SHA256 `eb1175dbdd733bb3c6776b5f1424c9ba61c40ce0c9bcc712389391e3efd29ae0`, official latest VERSION_UNVERIFIED; §4.2 physical p10 and §5 physical pp11–13 (web text `turn374480view1`), source specifically uses hoisting when **ONE fixed ciphertext v has MANY distinct automorphisms ψ**, allowing costly gadget digit decomposition of v's switched component to be computed once, while **each desired ψ(v) still requires its own automorphism-specific evaluation-key application**. Source §4.1 baby-step/giant-step changes rotation work structurally; §4.5 Horner-like circuit is also a **different algorithm**, not a claim that hoisting alone reduces number of distinct rotations. Web original PDF screenshot at p10 zero-index attempted and returned HTTP403; MCP source PDF text §§4.2/5 legible.
3. **OpenFHE developer documentation**, official `https://openfhe-development.readthedocs.io/en/latest/api/classlbcrypto_1_1CryptoContextImpl.html`, shows `EvalFastRotationPrecompute(ct)` provides reusable digit decomposition **of the input ct**, and `EvalFastRotation(ct,index,digits)` still executes the individual automorphism and key-switch portion. This is background implementation corroboration, not a measured speedup in PRCA.

## ONE hypothesis

**[HYPOTHESIS to falsify]** At each level i of LFBS Algorithm5 PRCA, the same automorphism index ψ_i is used B/2^i times. Therefore those calls can be hoisted to ONE actual ciphertext key switch per level using precomputation reuse, without changing Algorithm5's operands or adding new cryptographic primitives; this would reduce tree key-switch calls from B−1 to O(logB).

**[CHEAP falsification condition]** Standard hoisting's necessary reuse condition is that **the same ciphertext operand** v is rotated by more than one index. Extract each Algorithm5 `HomoAuto` argument as a formal expression in independent original RLWE input ciphertexts, enumerate its input-support at all tree levels, and test whether any two calls share the SAME operand (or same support); if all B−1 operands are distinct and each used exactly once, conventional precomputed decomposition offers no saving of work/call count under the algorithm as written. This does NOT exclude a totally redesigned packing or sharing between identical sub-LUTs.

## Exact PRCA recurrence and proof [FACT / DERIVATION]

Source Alg5 line5 (PDF physical p18) for i=1,...,log₂ B and j=0,...,B/2^i−1:
```
u_(i,j) = c^(i−1)_(2j) − X^(N/2^i) c^(i−1)_(2j+1),
c^(i)_j = c^(i−1)_(2j) + X^(N/2^i) c^(i−1)_(2j+1)
          + HomoAuto_(ψ_i)(u_(i,j), ATK).
```
The public ψ_i is shared by all j at stage i, but `u_(i,j)` is DIFFERENT for each j because child ciphertexts are distinct disjoint-subtree reductions. Given independent leaf inputs `ct_0,...,ct_(B−1)`, let support(node) mean the set of original leaf ciphertext indices the node depends on. By induction, each stage i operand `u_(i,j)` depends on **exactly the 2^i original leaves** `{2^i j,...,2^i(j+1)−1}`; those sets are disjoint for different j at fixed i. For different i their cardinalities differ, so they cannot be identical supports. Thus **every one of the B−1 tree automorphism inputs is distinct**; no single input operand is processed by multiple ψ_i, and standard single-operand hoisting offers zero decomposition reuse in this direct tree. Each argument independently needs its own switched-component digit decomposition. Reusing the SAME evaluation key ψ_i across many independent operands can reduce **stored distinct key count**, but not the number of input digit decompositions or automorphism-specific switching calls.

**[Exact deterministic DAG test]** Construct each node's bitset support and propagate `support(parent)=support(left)∪support(right)`; enumerate all i,j. For B ∈ {4,8,16,64,256}:
```
 B    tree HomoAuto calls   distinct input supports   maximum repeats
 4         3                       3                     1
 8         7                       7                     1
16        15                      15                     1
64        63                      63                     1
256      255                     255                     1
```
At any level i: exactly B/2^i auto calls, **B/2^i distinct operands**, ONE distinct automorphism type ψ_i. Every support corresponds to a separate independent ciphertext-dependent expression. For full PRCA trace, same original `B−1+log₂(N/B)` count still applies. Test is a symbolic dependency/DAG counterexample to hoisting precondition, not execution of FHE encryptions or a runtime estimate.

**Important boundaries of falsifier:**
- Conventional hoisting *does* improve many rotations of the SAME ciphertext, as in Halevi–Shoup. We are NOT proving it never speeds anything in LFBS (e.g. final HomTrace or other repeated-rotation contexts). Just PRCA **binary tree's B−1 calls** use distinct inputs; an implementation could choose to hoist within a different stage if it reuses a ciphertext for multiple rotations.
- Different inputs could be **batched in hardware** or their key-switch products vectorized, lowering wall-clock and memory access cost without changing B−1 logical operations; not tested here.
- An algebraically REFACTORED packing tree might move rotations across additions, employ transform domain batching, defer key switching, or use fundamentally different evaluation keys/secret domains and reduce B dependence. Such a scheme would require a novel proof of correctness/noise/security plus cost comparison, and is NOT ruled out by this restricted DAG observation.
- No unconditional Ω(B) lower bound for arbitrary packing or assumptions established. No reduction to security hardness. No new theorem or paper error; source correctly describes its precise B−1 cost in §4.2.
- Cross PRCA invocations (same initial ciphertexts or identical LUTs) could admit separate shared computations in special regimes; not part of the general arbitrary B ciphertext PRCA test.

## End of Iteration 189

**STATUS:** **FAIL** direct existing hoisted-auto reduction of PRCA tree's B−1 calls to O(logB) / **PASS** exact independent-operand DAG check and original Halevi–Shoup hoisting-prerequisite prior art / **UNCLEAR** a genuinely different sublinear-in-B ciphertext packing algorithm, parameter-matched speedup, noise and key storage.
**RESULT:** At level i, B/2^i automorphism calls have different `u_(i,j)` operands; all tree B−1 operands appear once, so conventional hoisting does not share any expensive decomposition across these calls. Same ψ_i **key** across nodes is not same v **ciphertext**. The restricted optimization is killed.
**NEXT_ACTION:** **I190 NOT STARTED; HUMAN_REVIEW / recommend PARK LFBS simple complexity-bookkeeping+hoisting branch**. If PI continues, pivot to a distinct, complete-source, high-value FHE target unless a specific new *algebraic packing* rewrite (not hoisting itself) is available with correctness+noise+total-work proposal. Source ePrint2025/022 35pp PDF equation visuals remain unverified from web screenshot 403; no proof of authored LFBS defect. Do not repeat B−1 counting or claim a universal packing lower bound.
**STATE_UPDATE:** **YES** — closes I188 proposed mechanism after exact prior-art and binary-tree dependency falsification, prevents pursuit of already known hoisting with false reuse premise, preserves full-source and version caveat.
