# vFHE Cross-CRT Scalar Consistency — Standalone Research Record

**Research theme:** enforce one common *integer* digit/index across CRT components of proof-friendly FHE/ZK range proofs.
**Status (2026-10-14):** STRUCTURAL GAP REMAINS; original I193 weight-two single-accumulator specialization FALSIFIED asymptotically; wider common-integer-code bridge still OPEN/UNPROVEN; NOVELTY NOT VERIFIED.
**Human PI controls:** parent direction, contribution/pivot decisions, author contact, disclosure.
**Maintenance:** This is a *topic-level, independent research file*, not an iteration log. Append or refine only upon a material verified result; preserve the old numbered records as evidence. Each future authorized test still follows AGENT.md: one primary hypothesis + one cheapest decisive test.

## 1. Precise target

Primary: Ignacio Cascudo, Anamaria Costache, Daniele Cozzo, Dario Fiore, Antonio Guimarães, Eduardo Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286, https://eprint.iacr.org/2025/286.

Primary text inspected: 52-physical-page Research MCP GitHub-mirror PDF, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; latest official publisher/ePrint binary **VERSION_UNVERIFIED**. Relevant source: §3.1 CRT product fields, §4.3 Figure 1 / Theorem 4.8, §5 PC compilation, Appendix D.3, Appendix E.2, Appendix F.1–F.3.

Let `R_q ≅ ∏_{k=1}^{μ} F_k` and the intended *diagonal* digit set be
`T_β^diag = {(j·1_{F_1},…,j·1_{F_μ}) : j=0,…,β−1}`.
Per-field membership only enforces
`T_β^rect = ∏_k {0,…,β−1}_{F_k}`, which strictly contains `T_β^diag` for μ≥2 and β≥2.

**[DERIVED, I59–I60] Concrete source-form witness:** `R=Z_77[X]/(X²+1)`, CRT primes 7 and 11; `h=56` maps to (0,1), so h is not a diagonal Boolean digit although each CRT projection is Boolean. Earlier records give valid theorem parameters, honest fieldwise memory transcripts CRT-glued into an identically valid ring grand-product relation, a shared false public `v`, true decomposition sumcheck, and compatible source-style independent field PCS commitments. The inspected ideal PIOP / theorem-level conclusion is challenged. This is **not** a proven exploit against a compiled deployed SNARK, not a confirmed current official-version flaw, and not a claim of confidentiality or 128-bit security compromise.

The underlying obstruction is algebraic: purely componentwise polynomial constraints / per-field witnesses do not bind a *single common table index*. Repeating the same fieldwise condition does not cure this distinction.

## 2. Research objective: a nontrivial fix, not a trivial erratum

Find a **global digit witness-binding mechanism** such that all CRT components must derive from the same bounded integer-index vector, while retaining:
- rigorous completeness + soundness/knowledge-soundness under the original source use-case;
- appropriate privacy / zero knowledge of small indices;
- full source-compatible PCS binding, interaction order, and Fiat–Shamir treatment;
- an explicit and useful *cost comparison* (communication, prover time, verifier time, memory, security parameters) versus the paper's fieldwise F.2/F.3 baseline.

No publishability, algorithmic security, or efficiency breakthrough has yet been established.

## 3. Mechanistic prior-art inspiration (reviewed, not asserted novel)

1. **Golovnev–Lee–Setty–Thaler–Wahby, Brakedown**, CRYPTO 2023, ePrint 2021/1043, §5, pp18–20 of inspected PDF: fast recursively encoded linear codes and code-distance-based commitments. The general-field generator uses nonzero field elements, so it does *not* automatically impose one bounded integer generator shared by every CRT prime.
2. **Block–Fang–Katz–Thaler–Waldner–Zhang, Field-Agnostic SNARKs from Expand-Accumulate Codes**, CRYPTO 2024, ePrint 2024/1871, §2–§4, inspected pp4–8: sparse expansion followed by prefix accumulation; provides structural inspiration. General-field distance analysis for field-specific sampled nonzero coefficients does *not* directly apply when we set all nonzero matrix entries to literal integer 1.
3. **BrakingBase**, ePrint 2024/1825: potentially relevant field-agnostic PCS design tradeoffs; no demonstrated diagonal CRT witness bridge in this research.
4. **Lasso**, EUROCRYPT 2024: indexed lookup inspiration, but independent fieldwise lookups still permit different indices.
5. **Original vFHE Appendix F.1–F.3:** product of native field PC schemes, each coding rows with prime-dependent root-of-unity RS/NTT in F.3. I151 proved **direct comparison of the unchanged native RS-coded Merkle columns fails honest completeness**: with honest x=[0,1], first j=1 encoded symbols for p29/p37 are 12/6 respectively.

**NOVELTY NOT VERIFIED.** Search/inspiration is not proof that no published cross-field integer commitment exists.

## 4. Current repair proposal — COMMON INTEGER-CODE BRIDGE

**[HYPOTHESIS, protocol NOT BUILT]** Instead of taking the original differently rooted per-prime RS-coded columns and trying to equate them, first encode one *common integer* vector by a public small-coefficient integer generator `G∈Z^{m×M}`:

`C=Enc_Z(x)=xG,   x∈{0,…,β−1}^m`.

Choose G and parameters with a no-wrap honest envelope, such as
`max_j ∑_i |G_{ij}|(β−1)<p_min`
(and preferably nonnegative encoded output), so honest columns can have a unique bounded integer interpretation, independent of which CRT prime sees them.

A future protocol might Merkle-commit the **same canonical encoded integer columns** once, then link each native field `F_k` evaluation/testing transcript to its reduction modulo `p_k`. Field-specific response vectors at arbitrary evaluation challenges generally remain different; *only the properly shared encoded column data* is a plausible reuse target. The integer-column commitment may require hiding/blinding and a redesigned extractor/proximity protocol.

**Conditional mathematical lemma [DERIVED]:** If a common committed word C is verified to be within Hamming distance strictly less than `d_min/2` of `Enc_{F_k}(x^(k))` for every k, with all these comparisons living in one *consistently interpreted* alphabet/metric and the encoder injective on the admissible table digits, then triangle inequality + minimum distance imply all `x^(k)` coincide. The difficult step is proving that the actual interactive PCS forces those premises with negligible error; different fields cannot simply be compared in their native arithmetic without a shared canonical representation.

**Warning:** An unsalted Merkle commitment and/or openings of low-entropy digit columns may leak a witness or permit dictionary guessing. A shared commitment does not by itself preserve the original protocol's ZK property.

## 5. Verified minimal feasibility result (prior standalone I193)

One necessary algebraic gate has been tested, not a full protocol.

Parameters: m=8, β=2, source-form N=8, d=4, p0=29, p1=37; both p_i=4a_i+1 with odd a_i.

Define an integer-linear systematic expand-accumulate code
`Enc_Z(x)=(x, Prefix(xA)) ∈ Z^16`,
where `Prefix(y)_j=∑_{t≤j}y_t`, and A is a public 8×8 {0,1} matrix, each row weight 2, with zero-based support:

```text
r0 (4,7)    r1 (1,4)    r2 (1,2)    r3 (0,5)
r4 (3,4)    r5 (3,6)    r6 (5,6)    r7 (2,6)
```

**[DERIVED+REPRODUCED, PASS on this toy]** Honest binary output values lie in [0,16], strictly below both 29 and 37. Therefore the *identical integer codeword* can be used for honest input in both fields. Encoding is O(m) operations for this chosen sparse/accumulator template.

Exact enumeration of all `3^8−1=6560` nonzero differences of binary vectors gives minimum codeword Hamming weight 3, relative distance `3/16`. It can also be proved over **every odd-characteristic field (including extensions)**: weight≥3 inputs are handled by the systematic part; weight-2 inputs give nonzero parity because no two distinct weight-2 rows of A are proportional; a weight-1 input produces two same-sign impulses whose prefix has at least two nonzero positions in odd characteristic. Difference `e_7−e_5` attains total codeword weight exactly 3.

**Recheck on 2026-10-14:** Local `/mnt/data/i193_vfhe_universal_integer_ea_toy.py` (SHA256 `70e27821a362761316d36c2f097ec1634b20349e00c8bcf566d33e07c67d7502`) was rerun successfully. This file is local; the MCP cannot read `local/` or infer that local artifacts are in Git.

**No asymptotic claim:** `3/16` at m=8 does **not** imply code distance Ω(M) for m256 or m1024. This test does not establish the repair's PIOP soundness, witness privacy, author implementation parity, or 128-bit security.

## 6. Preliminary cost opportunity — NOT benchmarked

In an illustrative F.2 evaluation interface with `μ=6144, m=256, t=32`, 25-byte native `F_{p^4}` elements:
- Original repeated native vectors + coded columns: `μ·m·(1+t)·25 = 1,297,612,800 bytes = 1237.5 MiB`.
- Hypothetical shared-integer-column interface with 4-byte bounded symbols and *unchanged* per-field evaluation vectors: `μ·m·25 + t·m·4 = 39,354,368 bytes ≈37.53 MiB`.

This ≈33× **isolated interface calculation** assumes a working shared commitment, the same sampling count, no extra extractor/PCS checks and a safe 4-byte integer representation. It omits privacy, commitment, Merkle, soundness budget, testing, extra protocol messages, and actual implementation costs. **Not an end-to-end gain or an actual usable parameter claim.**

## 7. Known failed routes — do not revive without a new premise

- Ordinary ring-Boolean checks: CRT idempotents pass; cannot impose diagonal scalar membership.
- I95 and I148: public bounded/masked aggregate remedies yield limited or source-expensive communication; no completed low-cost fix.
- I136: sharing terminal Sumcheck suffix challenges weakens repeated soundness.
- I137: generic rank-four query functionals cannot become one unchanged rank-one Brakedown evaluation vector.
- I138: ordinary across-four-evaluations Merkle-column reuse yields <4× isolated saving, not a 10× new PCS.
- I149–I150: single native MLE integer lift violates honest completeness or has insufficient one-point soundness.
- I151: direct same-integer comparison of **existing native RS/NTT coded columns** rejects honest inputs because per-prime roots differ.
- **I193 is NOT I151 repeated**: it studies a replacement field-independent bounded-integer encoder.

For exact negative witnesses read `findings/OPEN_RESEARCH_BRANCHES.md` P1 and relevant files in `failures/`.

## 8. Remaining decisive proof obligations

1. **Uniform distance at source scale:** construct/check a specified small-integer sparse code family with positive constant relative distance over every relevant `F_{p_i^d}`, not just a small binary-message experiment.
2. **No-wrap envelope:** bound all *honestly opened* code symbols with the actual source `m, β, p_min`; distinguish Boolean-domain digits from random-challenge PCS vectors (which are generally not small integers).
3. **Shared commitment soundness:** specify the actual committed object, binding/extractor, word-consistency/proximity proof, sampling order and cross-field errors. Show a cheating CRT vector with inconsistent digits is caught except negligible probability.
4. **Zero knowledge:** hiding, blinding, and unopened/opened low-entropy integer code symbols under leakage adversaries.
5. **Full protocol integration:** source F.2 evaluation testing, field-specific vectors, domain-separated Fiat–Shamir, correct 128-bit soundness budget.
6. **Concrete gain:** match original code rate/encoding runtime, evaluate proof bytes/key/trust assumptions, and compare complete protocol rather than only one message format.
7. **Novelty, version, disclosure:** verify official paper version; check equivalent shared integer bridges in prior art. Do not contact authors or publicly disclose speculative vulnerability without PI approval.

## 9. One next minimal decisive technical test (requires PI continuation)

**Question:** Does the *specific* 0/1 sparse-expand + prefix-accumulate template maintain a constant relative minimum distance, or does it have an explicit family of o(M)-weight codewords when m grows?

**Cheap falsification first:** inspect Block et al. ePrint 2024/1871 §4 to determine exactly where their arbitrary-field distance proof uses independently sampled nonzero field coefficients; seek an explicit small-support cancellation pattern for a fixed-integer-weight generator at `m=256` or `m=1024` (prefer a general mathematical witness over exhaustive large enumerations). If one exists and generalizes, **KILL this particular encoder specialization**, while retaining the abstract shared canonical integer commitment research problem. Do NOT move directly to a full PCS implementation before this gate.

**CURRENT DECISION (superseded by Section 11):** parent target = vFHE cross-CRT consistency (PI-selected). The initial I193 toy passes its finite feasibility test, but I194 proves the full row-weight-two/single-accumulator family has vanishing relative distance. Wider shared-integer commitment research stays OPEN/UNCLEAR.

## 10. Evidence paths (repository)

- `findings/vfhe-crt-lookup-cross-component-soundness.md` — precise ideal-PIOP counterexample.
- `findings/vfhe-crt-full-range-piop-and-commitment-audit.md` — composed range relation and PCS scope.
- `findings/vfhe-confidential-pi-review-package-iteration74.md` — internal evidence review; no author transmission.
- `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md` — why unchanged RS columns fail.
- `findings/vfhe-shared-integer-ea-column-bridge-iteration193.md` — detailed construction and source-first test.
- `findings/OPEN_RESEARCH_BRANCHES.md` P1 — historical backlog / failed strategies.
- `STATE.md` — authoritative session checkpoint (do not use this document to silently override active state).

**Use this file as the single topic-level home for future verified vFHE consistency results. Keep each atomic technical test and full provenance in its numbered archive as needed, but do not force the scientific narrative into a numbered iteration list.**


## 11. New result — single-accumulator, row-weight-2 integer codes have vanishing distance (2026-10-14)

**Status: I194 completed. Scoped FAIL of the entire weight-2/single-prefix-code family; PASS constructive O(sqrt(m)) field-code obstruction. Not a repaired vFHE protocol or a new coding-theory novelty claim.**

### One primary hypothesis / one cheapest decisive falsifier

Hypothesis **H194 [NEGATIVE]**: For some suitable m×m public binary sparse matrix A with **exactly two 1s per row**, the integer-linear systematic code
\`E_A(x)=(x, Prefix(xA))\` of length 2m could have a strictly positive constant relative minimum distance as m grows over all intended odd-characteristic extension fields, and therefore support the common-integer-code PCS idea without changing its structural template.

Cheapest decisive test: exploit each row's two endpoints as a graph edge; find a universally low-weight codeword by a combinatorial argument, plus one exact m=256/1024 source-sized falsification instance. No full PCS implementation.

### Exact cyclic counterexample [DERIVED, TESTED]

For any m≥4 let \`A_i=e_i+e_{i+1 mod m}\`. Take x=e_0−e_1, the difference of two valid **binary** digit vectors. Then
\`xA=(e_0+e_1)−(e_1+e_2)=e_0−e_2\`, hence
\`Prefix(xA)=e_0+e_1\`.
Thus \`E_A(x)=(e_0−e_1, e_0+e_1)\` has Hamming weight **exactly 4 over any field of odd characteristic**, and actually over any field in which ±1 nonzero. Accordingly
\`d_min(E_A)≤4\`, \`δ_m=d_min/(2m)≤2/m→0\`.
At m=256, explicit witness has relative weight 4/512=0.78125%; at m=1024, 4/2048=0.1953125%. No-wrap remains perfectly satisfied for honest binary digits if 2m<p_min (true for large source 49-bit primes), so the flaw is **distance**, not an honest-completeness failure. The same difference lies in {-1,0,1}^m, so it is also a genuine pairwise bounded-digit-distance weakness.

### Stronger theorem: universal upper bound for ANY 2-sparse layout [DERIVED]

**Claim:** For every m×m binary matrix A with exactly two distinct 1s per row and every odd-characteristic field F, the linear code \`E_A:F^m→F^{2m}\` has
\`d_min(E_A)=O(sqrt(m))\` uniformly over the choice of A. Consequently \`δ_m=O(m^{-1/2})\`: **no** row-weight-2, one-prefix-accumulator family of this form can have positive asymptotic relative distance.

**Proof (elementary graph construction; constants absolute):**

Represent columns 0,…,m−1 as labeled vertices of a (multi)graph and rows as edges; hence m vertices and m edges. For edge coefficients x, \`y=xA\` is the unsigned incidence-vector sum and \`z=Prefix(y)\`. If parallel rows occur, their difference gives \`y=0\` and a weight-2 systematic-only codeword. Otherwise work with a simple graph.

Set \`L=ceil(2 sqrt(m))+2\`. For any *even-length path* \`v_0,…,v_{2r}\`, alternating coefficients \`(+1,-1,+1,…,-1)\` on its edges cancel all internal unsigned incidences, giving \`y=e_{v_0}−e_{v_{2r}}\`. Its prefix vector is supported on exactly \`|v_0−v_{2r}|\` coordinates. Therefore the codeword weight is at most the path length plus the numerical gap of its endpoint labels.

**Case A — a connected component has ≥L vertices.** Choose a BFS tree rooted at an arbitrary component vertex. If it has depth at least L, take a root-to-depth-L path: among its ≥L+1 vertices, at least L/2 share the same parity of depth. Among those integer labels in [0,m−1], two have separation \`O(m/L)\` by the pigeonhole principle, and their tree path has even length ≤L. If the BFS depth is <L, instead choose the larger of the two depth-parity classes in the full component (size ≥L/2); again two labels have separation \`O(m/L)\`, while their unique tree path has even length <2L. In either subcase the alternating-path witness has Hamming weight \`O(L+m/L)=O(sqrt(m))\`.

**Case B — every connected component has <L vertices.** Let c be the number of connected components and \`r_C=e_C−v_C+1\` their (nonnegative) cycle ranks. As the whole graph has m edges and m vertices, \`∑_C r_C=c\`. If any component has \`r_C≥2\`, there are at least \`v_C+1\` unsigned incidence columns supported on \`v_C<L\` vertex coordinates, hence a nonzero linear dependence on ≤\`v_C+1=O(L)\` edges. It gives \`xA=0\`, so \`E_A(x)=(x,0)\` of weight \`O(L)\`. Otherwise every component is unicyclic (all \`r_C=1\`). If any cycle is even, alternating edge signs around it give \`xA=0\`, again weight <L. If all cycles are odd, assign alternating ±1 around any chosen cycle to obtain \`y=2e_a\` at a chosen cycle vertex a (over odd characteristic); negate another cycle assignment to obtain \`y=2(e_a−e_b)\`. As each component has <L vertices there are \`c≥m/(L−1)=Ω(sqrt(m))\` such distinct cycle representatives. Two representative integer labels satisfy \`|a−b|=O(m/c)=O(sqrt(m))\` by pigeonhole. The two cycles together use <2L edges; the parity prefix is supported on \`|a−b|\` positions. Again the total codeword weight is \`O(sqrt(m))\`.

This exhaustive case analysis proves the bound. The proof does NOT use the original random-edge distribution or a particular graph layout. It concerns *field-linear minimum distance*, so it decisively kills the field-agnostic code-distance requirement even if certain restricted witness distributions behave differently. It does **not** rule out row weight≥3, multiple accumulators, different block lengths, nonlinear integer codes, or different global-consistency proof mechanisms.

### Independent exact checks [EXPERIMENT]

The reproducible local script \`/mnt/data/vfhe_cross_crt_row2_distance_obstruction.py\` (SHA256 \`955966c21c37f2eba1e6b247405dcf8b88ae4a75dfc41ec1e91c54222053a3f7\`) builds the graph certificate and computes exact integer, mod29 and mod37 weights. Results JSON \`/mnt/data/vfhe_cross_crt_row2_distance_obstruction_results.json\` (SHA256 \`eb6cbce53c3acfebfdcd7a1673f212b114128d215bd8368b58d95269373c61c9\`). No local artifacts are treated as repository files.

- cyclic m=256: certified weight **4/512** over integers, F29, F37.
- cyclic m=1024: certified weight **4/2048** over integers, F29, F37.
- star+chord m256: graph-found certificate weight **3/512**.
- disjoint 85 odd triangles m255: paired odd-cycle certificate weight **8/510**.
- reproducible G(n,m) random simple graphs m64/256/1024: graph-found low-weight certificates, including m1024 **11/2048**.

These are explicit upper-bound witnesses, NOT exhaustive minimum-distance computations or physical vFHE PCS security measurements.

### Prior literature & novelty boundary

Block et al., *Field-Agnostic SNARKs from Expand-Accumulate Codes*, CRYPTO 2024, ePrint 2024/1871, §4.3–4.4 physical pp14–18: its field-general distance proof uses randomized nonzero field edge weights and a support/value argument (in particular Claims 4.4–4.5 and the distribution underlying them). Fixing all edge weights to literal 1 does not inherit that result. Classical repeat-accumulate literature (e.g. Kliewer et al., *Coding Theorems for Repeat Multiple Accumulate Codes*, arXiv:0810.3422) also notes sublinear minimum-distance scaling in ordinary RA ensembles; those are related but not identical ensembles, and the theorem above is derived directly for our exact \`[I|A·Prefix]\` structure. **NOVELTY NOT VERIFIED; do not claim an original coding-theory lower-bound discovery without comprehensive prior-art verification.**

### Decision / next gate

**KILL** the *entire* family with m×m binary A of exact row weight 2 and a single prefix accumulator as a basis for constant-relative-distance Brakedown-like PCS. The m8 I193 PASS remains correct but has no scalable-distance significance.

**PRESERVE** the broader cross-CRT **shared canonical integer codeword / shared commitment** research direction. The next individual minimal hypothesis (only on PI continuation) should specify one genuinely different encoder class—e.g. fixed small-integer row weight≥3, or more than one independently interleaved accumulator—with its own provable/rapidly falsifiable field-distance and no-wrap gate, before building any PCS. Do not infer success for these alternatives from Brakedown/EA theorems.

**End:** STATUS=FAIL (H194 constant-distance possibility for row-weight-2 single accumulator), RESULT=universal \`O(sqrt(m))\` upper bound + exact source-sized codewords, NEXT_ACTION=PI decides whether to test one different encoder family, STATE_UPDATE=YES.
