# vFHE Cross-CRT Scalar Consistency — Standalone Research Record

## Independent vFHE numbering (effective 2026-10-14)

This project maintains a **separate vFHE counter**, independent of the earlier general FHE I1–I192 sequence.

| New vFHE round | Historical vFHE note label | Core finding |
|---|---|---|
| **V1** | previously labeled I193 | Bounded-integer shared-codeword toy m8, minimum distance 3/16; finite feasibility only |
| **V2** | previously labeled I194 | Universal O(√m) distance upper bound for binary row-weight-2, single-accumulator code |
| **V3** | previously labeled I195 | Cyclic first expansion plus arbitrary second permutation/accumulator still O(√m) |
| **V4** | previously labeled I196 | Base-prime to extension-field distance equality for prime-field generator; nonbinary weighted RAA theorem mismatch |
| **V5** | first solely vFHE-numbered round | For source-style 49-bit primes, all ≤3-input-support subcodes have the same minimum distance across different CRT prime reductions |

Historical archived filenames/older internal labels remain unchanged for auditability. **Do not advance the global FHE iteration count** for vFHE work. The latest vFHE status is held in `findings/vfhe-cross-crt-state.md`, and this file remains the topic-level technical source of truth.


**Research theme:** enforce one common *integer* digit/index across CRT components of proof-friendly FHE/ZK range proofs.
**Status (2026-10-14):** STRUCTURAL GAP REMAINS; both the exact row-weight-two single-accumulator specialization and its cyclic-first-layer + arbitrary-second-interleaver/two-accumulator extension have VANISHING RELATIVE DISTANCE; the wider shared-integer-code bridge remains OPEN/UNPROVEN; NOVELTY NOT VERIFIED.
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
`E_A(x)=(x, Prefix(xA))` of length 2m could have a strictly positive constant relative minimum distance as m grows over all intended odd-characteristic extension fields, and therefore support the common-integer-code PCS idea without changing its structural template.

Cheapest decisive test: exploit each row's two endpoints as a graph edge; find a universally low-weight codeword by a combinatorial argument, plus one exact m=256/1024 source-sized falsification instance. No full PCS implementation.

### Exact cyclic counterexample [DERIVED, TESTED]

For any m≥4 let `A_i=e_i+e_{i+1 mod m}`. Take x=e_0−e_1, the difference of two valid **binary** digit vectors. Then
`xA=(e_0+e_1)−(e_1+e_2)=e_0−e_2`, hence
`Prefix(xA)=e_0+e_1`.
Thus `E_A(x)=(e_0−e_1, e_0+e_1)` has Hamming weight **exactly 4 over any field of odd characteristic**, and actually over any field in which ±1 nonzero. Accordingly
`d_min(E_A)≤4`, `δ_m=d_min/(2m)≤2/m→0`.
At m=256, explicit witness has relative weight 4/512=0.78125%; at m=1024, 4/2048=0.1953125%. No-wrap remains perfectly satisfied for honest binary digits if 2m<p_min (true for large source 49-bit primes), so the flaw is **distance**, not an honest-completeness failure. The same difference lies in {-1,0,1}^m, so it is also a genuine pairwise bounded-digit-distance weakness.

### Stronger theorem: universal upper bound for ANY 2-sparse layout [DERIVED]

**Claim:** For every m×m binary matrix A with exactly two distinct 1s per row and every odd-characteristic field F, the linear code `E_A:F^m→F^{2m}` has
`d_min(E_A)=O(sqrt(m))` uniformly over the choice of A. Consequently `δ_m=O(m^{-1/2})`: **no** row-weight-2, one-prefix-accumulator family of this form can have positive asymptotic relative distance.

**Proof (elementary graph construction; constants absolute):**

Represent columns 0,…,m−1 as labeled vertices of a (multi)graph and rows as edges; hence m vertices and m edges. For edge coefficients x, `y=xA` is the unsigned incidence-vector sum and `z=Prefix(y)`. If parallel rows occur, their difference gives `y=0` and a weight-2 systematic-only codeword. Otherwise work with a simple graph.

Set `L=ceil(2 sqrt(m))+2`. For any *even-length path* `v_0,…,v_{2r}`, alternating coefficients `(+1,-1,+1,…,-1)` on its edges cancel all internal unsigned incidences, giving `y=e_{v_0}−e_{v_{2r}}`. Its prefix vector is supported on exactly `|v_0−v_{2r}|` coordinates. Therefore the codeword weight is at most the path length plus the numerical gap of its endpoint labels.

**Case A — a connected component has ≥L vertices.** Choose a BFS tree rooted at an arbitrary component vertex. If it has depth at least L, take a root-to-depth-L path: among its ≥L+1 vertices, at least L/2 share the same parity of depth. Among those integer labels in [0,m−1], two have separation `O(m/L)` by the pigeonhole principle, and their tree path has even length ≤L. If the BFS depth is <L, instead choose the larger of the two depth-parity classes in the full component (size ≥L/2); again two labels have separation `O(m/L)`, while their unique tree path has even length <2L. In either subcase the alternating-path witness has Hamming weight `O(L+m/L)=O(sqrt(m))`.

**Case B — every connected component has <L vertices.** Let c be the number of connected components and `r_C=e_C−v_C+1` their (nonnegative) cycle ranks. As the whole graph has m edges and m vertices, `∑_C r_C=c`. If any component has `r_C≥2`, there are at least `v_C+1` unsigned incidence columns supported on `v_C<L` vertex coordinates, hence a nonzero linear dependence on ≤`v_C+1=O(L)` edges. It gives `xA=0`, so `E_A(x)=(x,0)` of weight `O(L)`. Otherwise every component is unicyclic (all `r_C=1`). If any cycle is even, alternating edge signs around it give `xA=0`, again weight <L. If all cycles are odd, assign alternating ±1 around any chosen cycle to obtain `y=2e_a` at a chosen cycle vertex a (over odd characteristic); negate another cycle assignment to obtain `y=2(e_a−e_b)`. As each component has <L vertices there are `c≥m/(L−1)=Ω(sqrt(m))` such distinct cycle representatives. Two representative integer labels satisfy `|a−b|=O(m/c)=O(sqrt(m))` by pigeonhole. The two cycles together use <2L edges; the parity prefix is supported on `|a−b|` positions. Again the total codeword weight is `O(sqrt(m))`.

This exhaustive case analysis proves the bound. The proof does NOT use the original random-edge distribution or a particular graph layout. It concerns *field-linear minimum distance*, so it decisively kills the field-agnostic code-distance requirement even if certain restricted witness distributions behave differently. It does **not** rule out row weight≥3, multiple accumulators, different block lengths, nonlinear integer codes, or different global-consistency proof mechanisms.

### Independent exact checks [EXPERIMENT]

The reproducible local script `/mnt/data/vfhe_cross_crt_row2_distance_obstruction.py` (SHA256 `955966c21c37f2eba1e6b247405dcf8b88ae4a75dfc41ec1e91c54222053a3f7`) builds the graph certificate and computes exact integer, mod29 and mod37 weights. Results JSON `/mnt/data/vfhe_cross_crt_row2_distance_obstruction_results.json` (SHA256 `eb6cbce53c3acfebfdcd7a1673f212b114128d215bd8368b58d95269373c61c9`). No local artifacts are treated as repository files.

- cyclic m=256: certified weight **4/512** over integers, F29, F37.
- cyclic m=1024: certified weight **4/2048** over integers, F29, F37.
- star+chord m256: graph-found certificate weight **3/512**.
- disjoint 85 odd triangles m255: paired odd-cycle certificate weight **8/510**.
- reproducible G(n,m) random simple graphs m64/256/1024: graph-found low-weight certificates, including m1024 **11/2048**.

These are explicit upper-bound witnesses, NOT exhaustive minimum-distance computations or physical vFHE PCS security measurements.

### Prior literature & novelty boundary

Block et al., *Field-Agnostic SNARKs from Expand-Accumulate Codes*, CRYPTO 2024, ePrint 2024/1871, §4.3–4.4 physical pp14–18: its field-general distance proof uses randomized nonzero field edge weights and a support/value argument (in particular Claims 4.4–4.5 and the distribution underlying them). Fixing all edge weights to literal 1 does not inherit that result. Classical repeat-accumulate literature (e.g. Kliewer et al., *Coding Theorems for Repeat Multiple Accumulate Codes*, arXiv:0810.3422) also notes sublinear minimum-distance scaling in ordinary RA ensembles; those are related but not identical ensembles, and the theorem above is derived directly for our exact `[I|A·Prefix]` structure. **NOVELTY NOT VERIFIED; do not claim an original coding-theory lower-bound discovery without comprehensive prior-art verification.**

### Decision / next gate

**KILL** the *entire* family with m×m binary A of exact row weight 2 and a single prefix accumulator as a basis for constant-relative-distance Brakedown-like PCS. The m8 I193 PASS remains correct but has no scalable-distance significance.

**PRESERVE** the broader cross-CRT **shared canonical integer codeword / shared commitment** research direction. The next individual minimal hypothesis (only on PI continuation) should specify one genuinely different encoder class—e.g. fixed small-integer row weight≥3, or more than one independently interleaved accumulator—with its own provable/rapidly falsifiable field-distance and no-wrap gate, before building any PCS. Do not infer success for these alternatives from Brakedown/EA theorems.

**End:** STATUS=FAIL (H194 constant-distance possibility for row-weight-2 single accumulator), RESULT=universal `O(sqrt(m))` upper bound + exact source-sized codewords, NEXT_ACTION=PI decides whether to test one different encoder family, STATE_UPDATE=YES.


## 12. New result — adding one arbitrary second interleaver + accumulator to cyclic row-2 expansion still has vanishing distance (2026-10-14)

**Decision:** I195 finished. FAIL the specifically defined cyclic-first-row-weight-two plus arbitrary *single second permutation* and two-prefix systematic code. PASS a uniform-in-the-second-permutation explicit low-weight *bounded-digit-difference* theorem. Preserve broader RAA with **independent first interleaver** and the cross-CRT common integer codeword research target. No full repaired protocol, no original source exploit, no novelty claim.

### Prior art and exact scope [FACT]

- Kliewer, Zigangirov, Koller, Costello, *Coding Theorems for Repeat Multiple Accumulate Codes*, arXiv:0810.3422, abstract/introduction https://arxiv.org/abs/0810.3422: classical RAA ensembles with random interleavers and repetition code have linear asymptotic distance at rates ≤1/3 under their model. This DOES NOT cover our fixed cyclic first sparse layout and just one free second permutation, or extension-field integer canonical lift/privacy.
- *Explicit Interleavers for a Repeat Accumulate Accumulate (RAA) Code Construction*, IEEE ISIT 2008, https://doi.org/10.1109/ISIT.2008.4595333, motivates genuinely nontrivial first interleaver and graph constructions for positive RAA distance. It is not a ready-made vFHE repair.
- Prior parent paper Cascudo et al., ePrint 2025/286 Appendix F.2/F.3, uses prime-dependent RS fields; a field-agnostic linear encoder alone does not enforce a common CRT scalar index absent a new shared commitment/proximity protocol.

### Primary hypothesis and decisive gate

[HYPOTHESIS — FALSIFIED] Keeping first-stage cyclic sparse matrix with exactly two ones per row and appending one **arbitrary** second permutation followed by one more prefix accumulator is sufficient to admit a positive-constant-relative-distance family, perhaps via well-chosen interleavers.

[ONE TEST] Derive a short valid binary-digit input difference for EVERY second permutation (not just random samples), then instantiate at m256/m1024 with independent exact integer and modular arithmetic. No full PCS work.

### Constructive theorem [DERIVED]

Let m≥64, F any odd-characteristic field or its extensions. Rows of A∈{0,1}^{m×m} are `A_i=e_i+e_{i+1 mod m}`. Prefix operator `U(y)_k=∑_{t=0}^k y_t`. For **arbitrary** permutation π of [m], define `P_πz` by `(P_πz)_{π(k)}=z_k`, and

`C_π(x)=(x, U(xA), U(P_π U(xA))) ∈ F^{3m}`.

Then there are two honest bounded Boolean input vectors a,b∈{0,1}^m whose distinct codewords satisfy

`wt(C_π(a)−C_π(b)) ≤ 2⌈2√m⌉+6`.

Consequently `d_min(C_π)/(3m)=O(m^{-1/2})→0` **uniformly over the second permutation**. Even the restricted binary-digit-pair distance deteriorates.

**Proof:** Set `B=⌈2√m⌉`. Restrict to candidate disjoint pairs `(i,i+1)` with i even and 0≤i≤m−3. Their number is `⌊(m−1)/2⌋`. Partition all m output positions into `K=⌈m/B⌉` consecutive blocks, each of length at most B. For m≥64 one checks `⌊(m−1)/2⌋ > K²`. Associate to each i the ordered block-ID pair `(floor(π(i)/B),floor(π(i+1)/B))`. By pigeonhole, distinct, disjoint i,j lie in the same block-pair class.

For each admissible i, take `u_i=e_i−e_{i+1}`. As the first matrix is cyclic, `u_iA=e_i−e_{i+2}` and `U(u_iA)=e_i+e_{i+1}`. Let `x=u_i−u_j=e_i−e_{i+1}−e_j+e_{j+1}`. It is literally the difference of two legal binary vectors `a=e_i+e_{j+1}` and `b=e_{i+1}+e_j` (disjoint positions).

Then `wt(x)=4`, `wt(z)=wt(U(xA))=4`, and the permuted first-prefix output is `P_πz=e_{π(i)}+e_{π(i+1)}−e_{π(j)}−e_{π(j+1)}`. Two impulses of opposite signs lie in ONE short block, and the other pair of opposite signs in ONE possibly different short block. Each block thus has net coefficient zero (also if the two blocks coincide). The prefix sum of this vector is zero outside the union of those blocks and has at most B−1 nonzero positions in each. Thus `wt(U(P_πz))≤2(B−1)`, and the full codeword weight is at most `4+4+2(B−1)=2B+6`. All equalities hold over Z and all intended odd-characteristic fields. QED.

This bound does **not** extend to arbitrary first-stage row-weight-two matrices with two random independent interleavers or to classic RAA ensembles; there is a deliberate fixed *cyclic* first-stage restriction.

### Exact source-scale minimal verification [EXPERIMENT]

Standalone deterministic local script `/mnt/data/vfhe_cross_crt_double_accumulator_gate.py` SHA256 `558b5daa8ac9782f97bf2d5c25e4d41b704e755f4aa206c68ca0e57a3a7d4a20`. JSON output `/mnt/data/vfhe_cross_crt_double_accumulator_gate_results.json` SHA256 `e89ed32b6d9780e480ba3b395ab05c31875f9099356aa11edb1f72ce8d61709a`. Tests construct legal a,b, confirm every component of `C(a)−C(b)` exactly, verify Hamming weights in Z,F29,F37,F65537 and the general bound:

| m | π | witnessed wt / 3m | theorem upper bound |
|---:|---|---:|---:|
| 256 | identity | 11/768 | 70 |
| 256 | reverse | 11/768 | 70 |
| 256 | seeded random | 32/768 | 70 |
| 1024 | identity | 11/3072 | 134 |
| 1024 | reverse | 11/3072 | 134 |
| 1024 | seeded random | 70/3072 | 134 |

This is an explicit upper-bound certificate, NOT the exact d_min. Strong universal statement is from the proof, not six tests.

Honest digit no-wrap is not the issue in this particular regime: for x∈[0,β−1]^m, first-stage y entries ≤2(β−1), z entries ≤2m(β−1), second prefix entries ≤2m²(β−1). For m1024, β=2^20, this is <2^41<2^48, hence compatible with p_min>2^48 as a **conditional source-style parameter envelope**. For small test p29/p37, no-wrap of arbitrary honest vectors is **NOT** claimed; those moduli are only used for algebraic codeword verification.

### Research consequence / next unique gate

**KILL:** fixed cyclic A with row support {i,i+1}, even when followed by arbitrary π and a second prefix accumulator, as the constant-relative-distance commitment code. Do not keep retrying different π: the theorem is uniform.

**KEEP:** true RAA architecture with TWO independently designed/randomized interleavers (not fixed cyclic expansion), shared integer coefficient matrix/no-wrap, and extension-field soundness. Binary classical RAA results are suggestive **but neither the proof over all odd extension fields nor the cross-CRT zero-knowledge PCS exists**.

**NEXT_ACTION, only if PI continues:** Specify one true double-interleaver, repetition-two, two-accumulator systematic integer encoder; first minimal test for a field/prime-induced or combinatorial low-weight word that breaks constant distance, and separately check no-wrap. Do not import binary RAA theorem or claim a novel code without careful provenance.

**End:** STATUS=FAIL (cyclic first-stage + any second interleaver); RESULT=uniform O(√m) distance bound with explicit binary pair and source-scale checks; NEXT_ACTION=true independent-two-interleaver RAA smallest falsifier; STATE_UPDATE=YES.


## 13. I196 — extension-field invariance of integer-generator code distance; true two-interleaver RAA literature boundary (2026-10-14)

**One primary hypothesis/test (authorized PI continuation):**
Can a *truly independently interleaved* repetition-two, two-prefix-accumulator, **unweighted small-integer** systematic RAA encoder develop **new shorter codewords solely from extending its coefficient field from F_p to F_(p^d)**, as in source vFHE extension-field CRT components? An F9 brute-force example and an algebraic basis-decomposition proof decisively test this. A separate original-literature **applicability check** prevents claiming the full RAA distance theorem without its hypotheses.

**Status:** PASS exact extension invariance lemma + F3/F9 exhaustive check. FAIL importing the cited WNRMA nonbinary *linear-distance guarantee* into the unweighted repeat-2/two-accumulator source architecture. Whether the prime-field code at m256/1024 has positive asymptotic relative distance: **UNCLEAR/OPEN**. vFHE full cross-CRT commitment STILL UNCONSTRUCTED. NOVELTY NOT VERIFIED; the algebraic lemma is a standard base-field generator-matrix fact, not a new coding-theory theorem.

### General exact lemma [DERIVED — rigorous]

Let G∈F_p^{k×N} be a public matrix with coefficients in the **prime subfield**, for example any integer matrix reduced modulo p. Let K=F_(p^d), with d≥1, and consider the two *linear* codes

C_p={xG : x∈F_p^k}, and C_K={xG : x∈K^k}.

**Claim: d_min(C_K)=d_min(C_p)** (assuming G has nonzero rank; if degenerate, define d_min of nonzero codewords in both).

Proof: Choose F_p-basis b_1,…,b_d for K, and decompose any x∈K^k uniquely as x=Σ_j b_j x^(j), x^(j)∈F_p^k. Because G entries are in F_p,

xG=Σ_j b_j(x^(j)G).

By F_p-linear independence of the basis, at each coordinate t, (xG)_t=0 in K iff **all** (x^(j)G)_t=0 in F_p. Thus

supp(xG)=∪_j supp(x^(j)G).

For any nonzero codeword xG, at least one nonzero x^(j)G exists, so wt(xG)≥d_min(C_p). Conversely C_p embeds in C_K, so d_min(C_K)≤d_min(C_p). Equality follows.

**Scope caveat:** This lemma is for the *same generator G reduced modulo the same prime p* and its degree-d field extension. It does NOT equate distances of G mod **different** CRT primes p_i; characteristic-dependent rank/cancellation can differ. It also does NOT establish positive constant distance in F_p at any scale. A source’s random field weights outside F_p break the base-subfield assumption.

### Exact smallest test [EXPERIMENT]

Define the genuinely two-independent-permutation integer RAA encoder

Rep_2(x)=(x_0,x_0,…,x_{m−1},x_{m−1}) in Z^{2m};
r_1=P_{π1} Rep_2(x); z=Prefix(r_1);
r_2=P_{π2} z; w=Prefix(r_2);
E(x)=(x,w)∈Z^{3m}.

Use two independently seeded permutations pi1 and pi2 (not fixed cyclic first layout) and m=4. Enumerate all 3^4−1=80 nonzero input vectors over F3. Then represent F9=F3[a]/(a²+1) and independently enumerate all 9^4−1=6560 nonzero extension-field input vectors. Confirm both distances are **exactly 4**, with matching matrix construction and no reliance on floating point. The full integer generator matrix, permutations, and witnesses are in the reproducible local JSON.

Artifacts **local, not in Git**:
- `/mnt/data/vfhe_raa_extension_invariance_gate.py` SHA256 `e0aa5283830e6514a535e8e86394a8571b322f92d85dcb38c94184bb2d9d1d7d`.
- `/mnt/data/vfhe_raa_extension_invariance_gate_results.json` SHA256 `a433f26af9b3ca768ed4d1a16e65189a97eddb866124a63c8e531975879c071e`.

For nonnegative honest bounded digits x∈[0,β−1]^m the final accumulator entry obeys the conservative integer bound

`max_j |w_j| ≤ m(2m+1)(β−1)`.

At m256 or m1024, β=2^20, bounds are exactly 137707257600 (38 bits) and 2200094899200 (42 bits), each <2^48; thus **a conditional honest no-wrap feasibility envelope** for source-like p_min≥2^48 exists. This is NOT a bound on arbitrary prover or PCS random-evaluation vectors, and no concrete original paper parameter reconciliation has been proved.

### Source-theorem gate [FACT, relevant but distinct from our proof]

Rosnes & Graell i Amat, *On the Analysis of Weighted Nonbinary Repeat Multiple-Accumulate Codes*, arXiv:1101.5966 (2011), https://arxiv.org/abs/1101.5966, original Sections I–III, in particular Fig.1, Theorems 4 and 5:

- Source analyzes **weighted** nonbinary ensembles; each encoder stage includes random nonzero field weight multipliers. These are NOT the all-{0,±1}-integer fixed generator we need for a common canonical integer codeword.
- Theorem 5 explicitly establishes typical linear min-distance for (L≥3,n≥2) OR (L=2,n≥3); the tempting (L=2,n=2) is **NOT** among these sufficient regimes.
- Its proved numerical field-size range in Theorem 5 is 3≤q≤2^25; source vFHE works with ≈49-bit prime p_i and degree-d extensions (e.g. p_i^4), far beyond that range. By the new exact lemma we need only analyze **p_i**, not the much larger p_i^d, but p_i itself still exceeds 2^25.
- Published nonbinary accumulators use generator 1/(1+D) plus randomized weights; our positive prefix U corresponds to 1/(1−D). Sign conjugations may relate constituent accumulators in isolation, but cannot be used to silently transfer an entire repeated, interleaved, unweighted ensemble theorem.
- Binary RAA result Kliewer et al., arXiv:0810.3422, likewise cannot be read as a nonbinary/unweighted prime-field guarantee.

These differences block *direct theorem citation*, not prove the actual proposed integer code has bad distance.

### Small exploratory observation, NOT a distance certificate

For true independent permutations and the **particular signed weight≤2 Boolean difference family**, exact integer generation and search found candidate codewords at m256 (min observed 123/768) and m512 (133/1536); different random seeds and the shrinking ratio are NOT an asymptotic proof. A complete two-symbol pair scan at m1024 with a different seed found 922/3072. None gives global d_min or rules out full-weight low codewords. Do not treat these independent seed samples as an estimate of a guaranteed distance constant. The decisive contribution of I196 is the **extension-field equality proof and precise imported-theorem boundary**, not the exploratory ratios.

### Technical decision

The previous two negative results I194–195 do NOT by themselves kill this genuine two-interleaver RAA integer generator. However, the classical nonbinary positive-distance theorem cannot currently certify our precise unweighted (n=2,L=2) scheme. We have removed one concern for free: testing over F_(p^d) is mathematically redundant once G mod p is fixed.

**NEXT_ACTION (only after PI continuation):** One new falsifier for *prime-field* distance of the genuine (n=2,L=2), unweighted two-interleaver integer RAA at source-scale m; target an explicit low-support generator dependency/short codeword **or** a carefully delimited proof via a prior ensemble whose coefficient distribution genuinely matches small integer weights. If no source-compatible distance result or short counterexample appears, mark UNCLEAR and consider PI-controlled pivot to n=3 or a genuinely different bounded-code family. Separately, the global cross-CRT Merkle commitment, proximity, hiding, Fiat–Shamir, and end-to-end cost remain OPEN.

**End I196:** STATUS=PASS prime→extension minimum-distance invariance, FAIL automatic source-theorem transfer, UNCLEAR prime-field linear-distance / full repair; RESULT exact lemma + F3/F9 exhaustive check + verified source mismatch; STATE_UPDATE=YES.


## 14. vFHE V5 — cross-prime invariance of ≤3-sparse input distance for integer RAA (2026-10-14)

**Primary falsifiable claim.** For the *specific fixed* repetition-two, TWO independent-interleaver, double-positive-prefix **integer-generator** code, can selecting different native CRT primes p_i≈2^49 introduce new low-weight codewords with message support ≤3, even though each G mod p_i has the same integer origin? The source-sized 49-bit prime range admits a strong determinant threshold: falsify by finding a nonzero integer determinant of order≤3 which vanishes modulo an allowed CRT prime.

**[DERIVATION — PASS, small-support invariance theorem]**

Let G∈Z^{m×N} and |G_{ij}|≤B. For k≤t, every k×k integer minor M satisfies by direct permutation expansion |det M|≤k!B^k. If prime p>t!B^t (and B≥1), every nonzero minor of order at most t stays nonzero under reduction mod p; zero minors obviously remain zero. Thus for **every** choice of ≤t rows S, ranks of every column submatrix G_{S,J} over Q and over F_p are the same.

For a fixed S of k≤t rows, the minimum nonzero output weight in span(G_S) equals N−max{|J| : rank(G_{S,J})<k}. Indeed a nonzero row coefficient vector x annihilates exactly the columns in some hyperplane, and conversely rank<k gives an annihilating nonzero x; maximize the attainable vanishing-column set. Since every relevant rank agrees over Q and Fp, the restricted code minimum weight agrees. Taking minimum over S with 1≤|S|≤t gives:

    d_{≤t}(G;Q) = d_{≤t}(G mod p;Fp)

where d_{≤t} means minimum over **nonzero codewords generated by messages of support ≤t**, NOT unrestricted d_min. By the prior V4 extension-field invariance lemma, the same equality holds for the extension field F_(p^d), and across any different primes p_i satisfying the determinant condition.

This is a standard small-minor/rank preservation fact; **NOT a novel coding theorem**, no claim about all input supports.

**[SPECIALIZATION]**

For genuine double-interleaver unweighted RAA, define U as cumulative sum on 2m coordinates and

    G = [I_m | U P₂ U P₁ Repeat₂]

(with matrix orientation interpreted as linear map from row messages). Every unit-message basis row has TWO +1 repeated symbols; after first prefix entries are in {0,1,2}, after second prefix each entry is ≤2(2m)=4m. Thus B≤4m and, for t=3:

    p > 3!(4m)^3 = 384 m³.

Under a **conditional** source benchmark regime p_i > 2^48 (49-bit primes), even m=8192 satisfies 384m³=211106232532992 < 2^48. Cases m256,m1024,m2048 are more comfortably below threshold. The source §6 uses 49-bit benchmark primes, but this does not assert every setting in paper has p_i > 2^48, and m here is the chosen message row dimension, not automatically the CKKS polynomial ring dimension N.

**[EXPERIMENT — PASS]**

Reproducible local script `/mnt/data/vfhe_v5_sparse_support_prime_stability.py`, SHA256 `d8bc466c6295fa6ad46e7f727bce328aa3d06d060862a90e221544718f02b855`. JSON `/mnt/data/vfhe_v5_sparse_support_prime_stability_results.json` SHA256 `5c21fb5d24728f3371acac224613483307336ba2e9108d573a201c9f4c421ff1`. Created within this turn, executed and rerun successfully; local only, **not** mounted in GitHub Notes.

Set m=8, N=24, random independent π₁,π₂ with fixed seed 20261014, B≤32, t3 bound=196608. Primes p1=1000003, p2=1000033 both exceed bound. Exhaustively compare exact integer zero status against both modular statuses for ALL **121264** square submatrices of orders1,2,3 of the actual G. PASS.

Independently optimize codeword Hamming weight for all message supports |S|≤3 using normals to rank≤2 hyperplanes; answer d≤3=8 over Q, Fp1 and Fp2. One witnessed optimum message coefficient pair (5,−5) on input coordinates [3,7], equivalent to the binary admissible difference (1,−1) for the same zero pattern. The result is **not the unrestricted minimum distance** of this code.

Source-sized sufficient determinant caps from the same formula:

| m | B=4m | 6B³ | below 2^48 |
|---:|---:|---:|:---:|
| 256 | 1024 | 6442450944 | YES |
| 1024 | 4096 | 412316860416 | YES |
| 2048 | 8192 | 3298534883328 | YES |
| 8192 | 32768 | 211106232532992 | YES |

**[PRIOR ART AND PROVENANCE]** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint 2025/286 §6 (benchmark 49-bit primes) and §3.1 (CRT extension-field factors), original mirrored PDF 52pp SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest exact version unverified. Kliewer et al., *Coding Theorems for Repeat Multiple Accumulate Codes*, arXiv0810.3422; Rosnes–Graell i Amat, *On the Analysis of Weighted Nonbinary Repeat Multiple-Accumulate Codes*, arXiv1101.5966, apply DIFFERENT ensemble assumptions, and no positive min-distance claim is imported.

**Scientific interpretation.** For every **fixed** integer G of the specified size, ≤3-input-support minimum-weight search in Q (or one qualifying prime) is mathematically reusable across every p_i satisfying p_i>384m³, including its F_(p_i^d) extensions. This closes a small technical branch: different CRT primes **cannot create new short codewords supported on ≤3 input coordinates** in this parameter regime.

**Limitations / remaining primary obstacle.** Submatrices of order≥4 are NOT protected by this inequality for all 49-bit p. An adversarial low-weight input with support≥4 may exist, and there is **no proof of constant relative global distance** for unweighted repeat2/accumulate2. Existence of a shared integer Merkle codeword PCS with extraction, ZK/hiding, Fiat–Shamir, and compelling total protocol savings remains entirely open. Algebraic invariance of low-support rows is not a cross-CRT consistency proof.

**END V5.** STATUS=PASS strictly scoped low-support cross-prime invariance and exact recheck; RESULT=explicit determinant bound p>384m³ for input support≤3; NEXT_TEST (only on PI continuation)=investigate support≥4 short-codeword obstructions, preferably a minimal support-4 integer dependency that differs across source-form primes, or a rigorous global distance argument; STATE_UPDATE=YES in *independent vFHE state only*, not global iteration numbering.


## 15. vFHE V6 — monotone parity minors certify cross-prime four-support distance (2026-10-14)

**ONE primary hypothesis / one decisive exact test.**
V5 left open whether a **message support-4** codeword can appear or disappear merely by selecting a different legitimate native ≈49-bit CRT prime, because naive generic determinant bound 4!(4m)^4 > 2^48. Specific falsifier: exhibit a nonzero 4×4 minor of the SAME integer repeat2/double-independent-interleaver/double-positive-prefix generator matrix that becomes zero modulo a source-form p>2^48; or give a rigorous *structural* upper bound excluding such an effect.

**RESULT: PASS stronger structural exclusion for m≤1024.** No 49-bit-prime-specific rank change is possible in ANY submatrix of at most four input rows for the described encoder, under p>2^48. Global distance/support≥5 remains UNCLEAR. This is not a completed vFHE proof system or novel coding-theory claim.

### Original-source anchor [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint 2025/286 (https://eprint.iacr.org/2025/286). Research MCP cached 52-physical-page GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest VERSION_UNVERIFIED. §3.1 physical p10: native p has format p=1+(2N/d)a for ODD integer a; §6 physical p27: benchmarks with 49-bit primes, including ring N=2^13 and 2^14 and d=2/4 (p27–29). Code input *m* below is the putative code-message length, NOT the original ring N. Claims about source scale are CONDITIONAL on p_i>2^48.

### Structural monotone-minor lemma [DERIVED, exact]

Let P∈Z_{\ge0}^{m×n} have every ROW weakly increasing in COLUMN order, with max entry at most B≥1. Let G=[I_m | P]. For any k≥1 and any k×k submatrix H of G,

    |det H| ≤ B^k.

**Proof:** Expanding along s selected unit columns of I_m reduces H to a (k−s)×(k−s) minor M of P (possibly zero). Sort parity columns, which changes determinant only by a sign. Each row of M has nonnegative increasing entries M_{i,1}≤⋯≤M_{i,r}≤B. Define nonnegative row differences D_{i,1}=M_{i,1}, D_{i,j}=M_{i,j}−M_{i,j−1} for j≥2. With the standard upper-triangular prefix matrix U (unit diagonal), M=D U and det U=1. Expand det D and use triangle inequality / nonnegative entries:

    |det D| ≤ Σ_{σ∈S_r} ∏_i D_{i,σ(i)}
            ≤ ∏_i (Σ_j D_{i,j})
             =∏_i M_{i,r}≤B^r.

Since r≤k and B≥1, ≤B^k. No probability assumptions, no hidden generic Hadamard or field-specific randomness.

**Distance corollary:** If p>B^t, every square minor of order ≤t in integer G has zero/nonzero status unchanged under mod p. Consequently every rank of every submatrix from ≤t selected input rows is unchanged between Q and F_p. By the rank characterization

    d_{≤t}(G;F) = nG − max_{S, J; 1≤|S|≤t, rank(G_{S,J})<|S|}|J|,

where J ranges columns and S input row supports, the minimum nonzero output weight for input support≤t is IDENTICAL over Q and F_p. V4's extension-field basis lemma gives same value over F_(p^d). Distances need NOT match across fields in the unrestricted (support>t) code.

### Application to unweighted true 2-interleaver double-prefix integer RAA

For x∈F^m, define Rep2(x) (each input repeated twice), independent permutations π1,π2 on 2m coordinates, and positive prefix operator U. Encoder:

    Enc(x)=(x, U(P2 U(P1 Rep2(x)))) ∈F^{3m}.

The parity-generator row for a unit input e_i is the second positive cumulative sum of a vector with exactly two 1s, so it is nonnegative, weakly increasing across output positions, and every entry is ≤4m (since its first accumulator values are each ≤2 and there are 2m prefix steps). Therefore the lemma applies with B=4m.

For k≤4, all relevant minors have magnitude ≤(4m)^4, **without the factor 4!** in the generic V5 bound. When m≤1024, (4m)^4≤2^48. All primes p>2^48 preserve them, including source-form choices; distinct qualifying CRT primes and their extensions have identical restricted Hamming distance d_{≤4} for fixed integer G.

Thresholds:
- m256: (4m)^4 =2^40.
- m512: 2^44.
- m1024: 2^48.
- m2048: 2^52; no unconditional promise for 49-bit primes using this lemma.
- m8192: 2^60; no unconditional promise for 49-bit primes using this lemma.

Important: p>(4m)^4 is a **sufficient** guarantee, not a necessary condition. Its failure for m≥2048 is not evidence of an actual CRT-induced codeword.

### Exact independent verification [EXPERIMENT]

Local reproducer `/mnt/data/vfhe_v6_monotone_minor_gate.py`, SHA256 `aa98b19c0783e33e9997c9d4bc26f18017bc42633ea3bd6e931154d3a71193f3`; JSON results `/mnt/data/vfhe_v6_monotone_minor_gate_results.json`, SHA256 `e1d0182f1c3758622cdf347ffc2e6161bfea37c5201531dc02922e6770e48557`. Local artifacts are NOT GitHub repository files.

- Generate two actual source-compatible 49-bit primes for N=8192,d=4 with p=1+4096a, a ODD:
  p1=281474976829441, p2=281474976894977; both verified prime, both >2^48, p mod8192=4097.
- Independently random π1/π2 seed20261014, m8, G shape8×24. EXACT integer computation of ALL binom(8,4)·binom(24,4)=743820 4×4 minors; all zero/nonzero flags agree over Z, Fp1, Fp2. Max observed |det|=128, while B^4=32^4=1048576.
- Source-scale random (not exhaustive) parity-only four-minor checks: m256 500 tests max |det|346630, m1024 500 max9710256, m2048 100 max29228634; no modular mismatch. For m≤1024 the proof certifies EVERY minor, independent of sampling; for m2048 no such proof, the 100 clean samples imply nothing universal.

**Scientific status:** This is standard elementary integer linear algebra plus positive-prefix monotonicity; its use for this exact candidate is a valid narrow result, NOT new coding-theory novelty and NOT a cross-CRT PCS soundness repair.

**V6 conclusion:** PASS preserve cross-prime/Fp→F_(p^d) message-support≤4 restricted distance at m≤1024,p>2^48. FAIL the *suspicion* that generic 4!B^4 crossing p must entail a 4-support mismatch. The actual unrestricted prime-field minimum distance, shared canonical Merkle commitment, zero knowledge, Fiat–Shamir, 128bit bound and end-to-end cost still OPEN.

**NEXT_ACTION (V7 only with PI continuation):** cheapest falsification of prime-specific rank/distance effects at support 5 (since B^5 can exceed 49-bit p even for m1024); test one concrete bounded-integer minor structure or short-codeword family, not random-only confidence or a whole PCS build.

**End V6:** STATUS=PASS scoped structural minor theorem and source-form exact arithmetic, NEXT_TEST=message support5, STATE_UPDATE=YES independent V-series only. No global I-series iteration advanced.


## 16. vFHE V7 — Cauchy–Binet five-minor bound is nearly tight; partial 49-bit cross-prime stability (2026-10-14)

**ONE primary falsifiable hypothesis and minimal decisive test:** At true independent-first/second-interleaver repeat2/accumulate2 integer code size m=1024, can the generic V6 t=5 failure to keep |det| below 49-bit p be resolved by the actual TWO-stage prefix matrix structure? Seek an exact structural upper bound, with a near-maximizing legal permutation/5×5-minor test to determine whether this is a useful improvement or merely an artifact of loose inequalities. Does NOT attempt a full code-distance or PCS proof.

**STATUS:** PASS stronger universal integer five-minor bound and a sharpness witness; PASS restricted d_{≤5} cross-prime invariance **only for 49-bit primes above a new explicit threshold**; **UNCLEAR** for small 49-bit primes p just over 2^48; **NO** new prime-specific rank-changing codeword found or claimed; vFHE protocol repair and novelty still OPEN/NOT VERIFIED.

### Grounded original paper

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286 (https://eprint.iacr.org/2025/286), previously examined full 52-page MCP mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest version VERSION_UNVERIFIED. Original §3.1 physical p10: CRT primes p=1+(2N/d)a with a odd. Original §6 physical p27 benchmarks with 49-bit primes, but does NOT equate candidate code input m with CKKS N.

### New two-stage factorization theorem [DERIVED + PROVED]

Let m≥1, n=2m, and G=[I_m | P] where P is the integer-linear parity matrix

    P = Rep₂ · Perm₁ · U₁ · Perm₂ · U₂,

for arbitrary (including independently sampled) permutations on n positions. Here Rep₂∈{0,1}^{m×n} repeats each input twice, U₁,U₂∈{0,1}^{n×n} are **positive prefix** upper-triangular matrices (entry U_{i,j}=1 iff i≤j), and all products are interpreted for row-vector encoding. Define A=Rep₂·Perm₁·U₁, Z=A·Perm₂, so P=Z·U₂.

**Claim (exact structural bound):** For EVERY r×r parity minor P_{S,J},

    |det(P_{S,J})| ≤ D(n,r) := 2^r q^{r−h}(q+1)^h,

where n=qr+h, 0≤h<r. More generally, an arbitrary r×r minor of systematic G reduces, after expanding any identity columns, to a smaller s×s parity minor, s≤r. Thus every minor of size at most t is bounded by max_{1≤s≤t} D(2m,s).

**Proof:** Since each row of A consists of prefix sums of two 1s, it is nonnegative monotone in original first-stage position and its maximum is exactly 2. By V6's monotone-row-minor lemma, any r×r subdeterminant of A has absolute value ≤2^r; permuting its columns (Z=A Perm₂) changes a selected determinant only by sign, so |det Z_{S,T}|≤2^r for every column subset T.

By Cauchy–Binet:

    det P_{S,J} = ∑_{T⊂[n],|T|=r} det Z_{S,T} · det (U₂)_{T,J}.

Take sorted parity column indices 0≤j1<...<jr<n and j0=−1. The prefix matrix U₂ has det(U₂)_{T,J}=1 precisely for sorted row positions t_i with j_{i−1}<t_i≤j_i for each i, and equals 0 otherwise. This is shown by subtracting consecutive prefix columns or by the staircase shape. Consequently the number of nonzero Cauchy–Binet terms is EXACTLY

    ∏_{i=1}^r (j_i−j_{i−1}).

Set ℓ_i=j_i−j_{i−1}>0. They have sum ∑ℓ_i=j_r+1≤n. The product of r positive integers with sum≤n is at most q^{r−h}(q+1)^h for n=qr+h by integer AM–GM / balancing. Bound each term's |det Z| by 2^r and sum absolute values, yielding claimed inequality. QED.

The new bound is approximately (4m/r)^r, improving V6's (4m)^r by about r^r. It relies critically on **two** positive prefix layers and repeat factor exactly 2; it does not cover native randomized-field-weight RAA variants, or arbitrary encoders.

**Coding-distance corollary (strictly restricted support):** If prime p>max_{1≤r≤t} D(2m,r), EVERY generator minor of order≤t keeps its zero/nonzero status when reducing integer G modulo p. Therefore for every input support S of size ≤t, ranks of all its column submatrices agree over Q, Fp, and F_(p^d); hence the minimum nonzero codeword Hamming weight among messages of support ≤t is field/CRT-prime independent across all such p. This is the rank argument from V5 and extension-field equality from V4. **NO consequence about unrestricted d_min or cross-CRT PCS proof** follows.

### Explicit source-style 49-bit threshold at m=1024

Here n=2048 and t=5. The maximum max_{1≤r≤5} D(2048,r) occurs at r=5:

    D(2048,5) = 2^5 · 409^2 · 410^3 = 368933561632000.

A qualifying 49-bit source-form prime must exceed this exact number; note 2^48=281474976710656, so the bound is NOT enough for all 49-bit primes. Concrete VERIFIED source-form examples for ring N=8192,d=4, with p=4096a+1 and odd a, p mod 8192=4097, both primality-tested:
- lower p_L=281474976829441 (<D): theorem DOES NOT certify support≤5;
- higher p_H=368933562830849 (>D): theorem DOES certify support≤5.
Both are within [2^48,2^49). The p_L failure is **failure of this sufficient criterion only**, not an actual detected rank change.

At m256, D(512,5)=360267381504; at m512 D(1024,5)=11529104880000, both <2^48: ALL 49-bit primes p>2^48 preserve support≤5 restricted distance there. At m2048 D(4096,5)=11805909173735040 >2^49: this criterion does not certify typical source primes.

### Near-tight constructed legal permutation [DERIVED + EXACT TEST]

To see whether D(2048,5) is a very loose bound, construct an actual legal first permutation on all 2m=2048 repeat positions, selecting message rows 0..4, such that in the FIRST accumulator the two copies of selected row i appear at the beginning of consecutive blocks with lengths [410,410,410,409,409], and all other (unselected) repeated symbols fill the remaining 2038 slots. Choose the SECOND permutation to be identity. This is a **legal deterministic permutation instance**, not a claim about typical random double-interleaver ensembles.

Sample the five parity output columns at endpoints of these blocks. The resulting exact 5×5 matrix is

    [[819,1639,2459,3277,4095],
     [0,819,1639,2457,3275],
     [0,0,819,1637,2455],
     [0,0,0,817,1635],
     [0,0,0,0,817]].

It is upper-triangular, so its determinant equals

    819^3 × 817^2 = 366687257496651,

which is **99.3911%** of D(2048,5), and importantly is **larger than p_L**. Thus no generic claim |5×5 minor|<p_L holds for this encoder family. However

    (det mod p_L) = 85212280667210 ≠0

and the determinant is also nonzero mod p_H. This witness does **NOT** show an actual CRT-prime-dependent rank change, new short codeword, or soundness attack.

### Minimal independent verification [EXPERIMENT]

Reusable Python script `/mnt/data/vfhe_v7_cauchy_binet_five_support.py`; SHA256 `1e4c90e62215a45dd73ba1cfc91841919719819acbb0b72ba1eef66f670afda1`.
Results JSON `/mnt/data/vfhe_v7_cauchy_binet_five_support_results.json`; SHA256 `cee8f200a75d5ce890dca8b4c0dfa92ed96a42480fd3f86bcce7d5f058f03142`. Created and executed in current runtime; these are LOCAL artifacts, NOT Git repository files.

- Verify actual 49-bit source-form primes by deterministic primality checks.
- Verify above m1024 5×5 matrix from exact repeat2, first permutation, identity second permutation, and TWO actual positive cumulative sums; determinant exactly matches factorization; 99.39% tightness.
- Independently check a SMALL Cauchy–Binet identity m6,r3: 60 enumerated nonzero prefix-subdeterminants, direct parity minor det−16 equals sum of terms−16, maximum first-stage subdeterminant2≤2^3.
- Additional NONEXHAUSTIVE seeded random parity minors: m256 180, m1024 180, m2048 60; verified all exact 5×5 determinants ≤D(2m,5), no zero/mod-p mismatches in these samples. Such samples NEVER replace the theorem and say nothing universal about the lower p_L or m2048.

### End-of-iteration decision

**STATUS: PASS for derived structural upper bound and upper-49-bit subset; UNCLEAR for ALL 49-bit primes or actual source-prime-induced new support-5 dependencies.** The near-tight extremizer is a warning that just tweaking elementary determinant inequalities will not certify p_L, and the research need is a **prime-divisibility/rank mechanism**, not merely |det| bounds. More important, local support t checks do not establish the globally constant relative distance or valid hiding shared-commitment architecture.

**NEXT_TEST (V8 only if PI continues):** One decisive attempt to find a *real* 49-bit source-form prime divisor of a nonzero 5×5 parity minor of a legal repeat2/two-prefix instance, **or** derive a precise arithmetic non-divisibility constraint for such minors. If neither is available cheaply, park low-support micro-optimizations and request PI strategic choice to tackle global distance / shared PCS architecture directly. No general claim of vFHE repair, new code, security/128-bit improvement or novelty.

**STATE_UPDATE: YES, independent V-series only**; global general FHE round remains I192.


## 17. vFHE V8 — exact source-form 49-bit prime divides a legal five-row RAA parity minor (2026-10-14)

**Primary hypothesis / one decisive test:** The V7 threshold p>D(2048,5) is only sufficient, but is its missing lower-49-bit range a *real* rank-preservation gap? Search for a nonzero five-row/five-parity-column integer minor of a LEGAL unweighted repetition-two, two-free-permutation, two-positive-prefix systematic code whose exact determinant is divisible by an actually prime 49-bit source-form CRT modulus p=1+4096a (a odd for source N=8192,d=4).

**STATUS: PASS — explicit, independently verified prime-specific MINOR-RANK DROP.** The stronger hypothesis that every actual five-minor remains of identical rank across all source-form 49-bit CRT primes is **FALSIFIED**. The example does NOT establish a change in global minimum distance, a low-weight codeword, a binary-digit-difference witness, a shared-PCS attack, a privacy compromise, or an actual vFHE compiled-SNARK exploit. Novelty / utility as a paper contribution: NOT VERIFIED.

### Primary source evidence [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286 https://eprint.iacr.org/2025/286, §3.1, physical PDF p10: p=1+(2N/d)a with a odd; §6 physical PDF p27 benchmarks 49-bit CRT primes. Inspected cached GitHub-mirror PDF 52 pages, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official binary edition VERSION_UNVERIFIED. The candidate auxiliary integer code's message length m is NOT source ring dimension N.

### The actual finite-field rank-changing certificate [DERIVATION+EXACT COMPUTATION]

Take CKKS **source-form** ring N=8192,d=4; candidate integer RAA code input length m=1024 and accumulator length n=2m=2048. Its systematic generator is

    G = [I_m | P],
    P = Repeat₂ · Perm₁ · U₁ · Perm₂ · U₂,

with every nonzero Repeat₂ coefficient literally integer 1, both positive prefix U_j and both permutation matrices integral, and NO native-field random edge weights.

Choose five selected input rows S={0,1,2,3,4}. In the first interleaver, place the two repeated positions of each selected row consecutively in order i=0,…,4 (first copy at start of its stage, second copy immediately next), with 2038 other inputs' repeat labels filling the remaining stage positions. Partition the 2048 first-stage output positions into five successive blocks of lengths

    L = [357,400,421,373,497].

Within block i, there is one first-copy *odd transitional* position with first-prefix value
`o_i=2(e_0+...+e_{i−1})+e_i`
and L_i−1 positions with plateau first-prefix value
`v_i=2(e_0+...+e_i)`.
These stages are all physically present in a valid first permutation; selected rows' copies are among the first 10 original Repeat₂ labels, unused original labels fill the other stages.

The second permutation is a valid explicitly **chosen** permutation of all 2048 stage positions. In its block j it places L_j−1 positions of plateau type v_j, plus one transitional position o_i for which

    σ(i)=j,  σ=[4,1,0,2,3].

Choose the FIVE parity output coordinates at the ends of the resulting second-prefix blocks:

    J=[356,756,1177,1550,2047].

The five consecutive block-sum columns form the **exact** integer matrix

    H =
    [[714,800,842,746,993],
     [2,799,842,746,992],
     [1,0,842,746,992],
     [0,0,1,746,992],
     [0,0,0,1,992]].

The actual parity submatrix at the sampled SECOND prefix coordinates is the cumulative-column matrix M=H·U_5, with det(U_5)=1:

    M =
    [[714,1514,2356,3102,4095],
     [2,801,1643,2389,3381],
     [1,1,843,1589,2581],
     [0,0,1,747,1739],
     [0,0,0,1,993]].

**Independent exact determinant calculations** (SymPy exact and manually implemented integer Bareiss) both give

    det(H)=det(M)=353581838970881=:p_star.

SymPy's primality verifier gives p_star PRIME; also 2^48<p_star<2^49, and

    p_star=1+4096·86323691155; 86323691155 is odd,
    p_star mod 8192 =4097.

Thus p_star is a LEGAL source-form 49-bit CRT prime for N8192,d4. By construction,

    rank_Q(M)=5,  rank_Fp_star(M)=4.

For the distinct source-form 49-bit prime `p_other=281474976829441`, which does not divide det(M),

    rank_Fp_other(M)=5.

The full **systematic** code remains full row rank over BOTH primes because of I_m; this local selected-parity minor rank drop is a different assertion.

### Independent modular codeword check [EXPERIMENT]

The explicit nonzero LEFT kernel of M modulo p_star, coefficients on the five selected input rows, is

    x=(248360433806974,147393490404705,227528283364297,265412092786493,1).

All five sampled parity outputs (xM)_j are zero modulo p_star, and nonzero over the ordinary integers. Computing the WHOLE systematic codeword of length 3m=3072 for the SAME lifted integer coefficients gives:

- Hamming weight over Q: **2053**;
- Hamming weight modulo p_star: **2048**;
- Hamming weight modulo p_other: **2053**.

Thus five extra parity-coordinate zeroes genuinely arise at this source-form CRT prime for this fixed coefficient vector. This is an **ordinary high-weight** codeword, **NOT** an exhibited globally short codeword, and it does not prove the code's minimum distance differs.

Furthermore the displayed x has HUGE entries modulo p_star: it is NOT the difference of two genuine bounded Boolean indices or a source-compatible beta=2^20 digit witness. It is a valid diagnostic for **field-linear** rank/PCS-distance assumptions only. A repair protocol may impose extra bounds restricting such algebraic inputs; no attack claim.

### Deterministic reproducibility and limits

Standalone script: `/mnt/data/vfhe_v8_prime_divisible_minor.py`, SHA256 `7ef42c152a386db4cafa5a526f1c047f17eb69e7d4ed928d75993cb983a85355`.

Full JSON including selected row/column coordinates, construction L/σ, stage matrix H, exact parity matrix M, exact determinants, primality, ranks, modular null vector, whole codeword weights:
`/mnt/data/vfhe_v8_prime_divisible_minor_results.json`, SHA256 `6d66f63e957a1686af7376d8f18f0f87a50ea63abd948b2b1016efb0d65492c4`.

These are **local files, not GitHub Notes file bytes**. The script was executed twice and the same SHA256 outputs obtained. Reproducible deterministic seed=1826 searched 165987 structured length/permutation proposals, yielding 35 source-congruent 49-bit determinant candidates before first prime success. This is **targeted search** with selection bias, not a frequency estimate of random interleavers. The first and second permutation of the final witness are specifically coordinated, not independent random samples from an ensemble; each is individually a valid permutation, and the pair is in the support of the independent-uniform-permutation ensemble, but no typical/random success probability is shown.

The rank mismatch occurs at input support **five**, consistent with V6's theorem ensuring all supports≤4 are stable for m1024,p>2^48. V7's upper bound `D(2048,5)=368933561632000` is respected: p_star=353581838970881<D. Therefore V8 is a genuine example showing the V7 lower-prime coverage gap is *not merely a proof-artifact* for arbitrary five-minor ranks.

### Research decision / stop condition

**Scoped conclusion:** cross-prime rank invariance for ALL 5×5 minors at m1024 is FALSE within the allowed 49-bit prime class. This proves that merely ensuring a *canonical integer generator* is common across CRT primes does not imply identical low-support linear dependence structure. It does NOT disprove uniform lower bounds on each prime's minimum distance or a well-constructed cross-CRT PCS; even with a rank drop in a few minors, the code may retain excellent global distance.

**V9 NEXT_ACTION (only if PI continues):** STOP raising the support threshold t. One global falsification/proof gate: rigorously test whether the **unweighted true two-interleaver repeat2 double-prefix** code can have positive constant relative minimum distance over all relevant large primes, using a proof that actually matches integer 0/1 coefficients and NOT the weighted nonbinary RAA theorem. If that cannot be proved or decisively falsified by a cheap global obstruction, declare UNCLEAR and move to a **shared-commitment cross-CRT extraction** gate only at PI direction. Do not frame this isolated linear-rank witness as a cryptographic attack or contribution.

**End V8:** STATUS=PASS real CRT-prime-specific five-parity-minor rank witness; RESULT=first genuine divisibility, exact full encoding construction and same-codeword weight comparison; STATE_UPDATE=YES independent vFHE V-series, global FHE iteration remains I192.


## 18. vFHE V9 — global bounded-digit distance via binary RAA reduction plus integer no-wrap (2026-10-14)

**Primary falsifiable hypothesis [PASS in stated restricted model]:** Does the genuine *unweighted* repeat-two / two-independent-interleaver / two-positive-prefix **integer** systematic code inherit a **globally linear relative distance among LEGAL bounded integer digit vectors**, simultaneously over all source CRT primes, from the known binary RAA ensemble theorem, even though V8 exhibits a field-specific five-minor rank difference for unrestricted large-coefficient Fp witnesses?

One decisive test: prove/reject a uniform zero-pattern transfer from the Z code to all Fp under a quantified no-wrap bound, then independently exhaust all bounded input-difference vectors in a toy instance and compare binary, integer, and multiple base-field weights.

**STATUS: PASS** exact deterministic inequality and exhaustive toy. This closes a necessary **bounded-digit code-distance** gate (conditioned on a random two-interleaver realization satisfying the classical binary RAA distance guarantee and source p>no-wrap threshold). **UNCLEAR** unrestricted native Fp-linear code distance, genuine Brakedown F.2 PCS soundness, cross-CRT binding/proximity, hiding/ZK, Fiat–Shamir, parameterized 128-bit error, or protocol performance. **NOT** a completed vFHE repair, not established novelty.

### Exact mathematical result [DERIVED]

Write n=2m and the integral row-vector code generator

    G_Z=[I_m | Repeat2·Perm1·U1·Perm2·U2] in Z^(m×3m),

with two arbitrary permutations on n points, positive prefix U_j, and duplicate-each-coordinate Repeat2. Let beta≥2 and define legal digit set A_beta={0,…,beta−1}^m. For a≠b∈A_beta, set x=a−b, so |x_i|≤beta−1.

**Lemma 1 (exact integer no-wrap, UNIFORM across primes):**
Each individual parity generator entry G_{i,m+j} is a nonnegative integer. Its COLUMN sum across all input rows has maximum EXACTLY

    B(m)=1+2+⋯+(2m)=m(2m+1),

at the final second-accumulator output coordinate, independent of the two interleavers. Indeed summing unit-input contributions across all m rows gives the all-ones length-n vector at the repeat stage, whose first cumulative vector is (1,2,…,n), irrespective of Perm1; Perm2 only reorders the entries; the largest second prefix sums all n entries. Thus for any admissible x,

    |(xG_Z)_j|≤B(m)(beta−1)  for all j,

including systematic coordinates. If EVERY selected CRT base prime p_i satisfies

    p_i > B(m)(beta−1),

then zero/nonzero support of the ENTIRE same integer codeword xG_Z is unchanged under reduction modulo each p_i and inside each extension F_(p_i^d):

    supp_Z(xG_Z)=supp_Fpi(xG_Z mod p_i)
                   =supp_F_(pi^d)(xG_Z mod p_i),

and consequently all these weights are exactly equal. This is a statement for **legal bounded integer differences**, not arbitrary p_i-field messages. The bound is strict <p; centered lifts not required just for zero preservation (although honest nonnegative canonical symbols also fit into [0,p−1]).

**Lemma 2 (mod-2 distance transfer, GLOBAL over all message supports):**
For any nonzero x∈Z^m, let g=gcd(|x_1|,…,|x_m|)>0 and x'=x/g∈Z^m primitive. By definition some x'_i is odd, so u=x' mod2 is a NONZERO binary message. Because G_Z is integral,

    E_F2(u)=(x'G_Z) mod 2.

Every integer zero coordinate of x'G_Z is also a zero coordinate of E_F2(u), so
    wt_Z(xG_Z)=wt_Z(x'G_Z)≥wt_F2(E_F2(u))≥d_min(C_F2(G mod2)).

This holds with NO restriction on input weight/support and without any determinant/minor assumptions. It is an elementary code-over-Z→mod2 support argument; not original coding theory.

**Combined restricted distance theorem:**

For every fixed choice of two permutations, every source collection of primes satisfying p_min>B(m)(beta−1), and every two DISTINCT legal digit vectors a,b,

    wt_F_(p_i^d) (E(a)−E(b))
        =wt_Z(E_Z(a−b))
        ≥d_min(C_F2(G mod2)), for ALL i.

Hence the restricted, LEGAL-DIGIT-pair minimum distance over every CRT field is at least the SAME binary-code min distance; and the codeword weights are identical across primes. This entirely bypasses V8's prime-divisible five-minor example because its modular null coefficients are vastly outside legal digit-difference range.

**Published probabilistic global consequence:** Guruswami & Machmouchi, *Explicit Interleavers for a Repeat Accumulate Accumulate (RAA) Code Construction*, ISIT 2008, DOI https://doi.org/10.1109/ISIT.2008.4595333, Definition 1 / Theorem 1 quoting Bazzi–Mahdian–Spielman 2003, gives for repeat factor k≥2 and TWO independent uniform random interleavers, for each fixed failure-probability tolerance δ>0 an epsilon>0 such that, for sufficiently large m, the BINARY (non-systematic) RAA parity code has d_min≥epsilon m with probability≥1−δ. The binary systematic [I|P] version used here has distance at least as large as that parity code, so the SAME event implies

    min_(a≠b∈A_beta) wt_Fpi(E(a)−E(b)) ≥epsilon m

simultaneously for EVERY native CRT p_i satisfying the deterministic no-wrap bound. For code length 3m, relative restricted distance is ≥epsilon/3. This is asymptotic with p_i sufficiently large AS A FUNCTION OF m and beta; for fixed 49-bit p it cannot be extended to arbitrary growing m. The published theorem is a **probabilistic binary ensemble** statement, not 128-bit finite-length guarantee or an explicit certified pair of source-size permutations.

***Provenance caveat:*** The quoted theorem is for binary RAA with FULL two random interleavers; Guruswami–Machmouchi's different inner-systematic construction and its second-permutation length 3m are NOT the one used here. We specifically use their Definition1/Theorem1 non-systematic RAA, append an external systematic copy x (which cannot decrease binary distance), and do NOT conflate the two encoder definitions. Rosnes–Graell i Amat 2011 *weighted nonbinary* RAA theorem is likewise NOT imported into this unweighted construction.

### Original vFHE PCS F.2 scope: why this PASS is still NOT an operational PC repair

Original source ePrint2025/286, Appendix F.2, physical PDF pp50–51:
- The committed row code is a FIELD-LINEAR Enc:F^m→F^M, with all witness rows originally native field vectors.
- Testing verifier samples **arbitrary r∈F^m** and checks at queried Merkle columns `Enc(r·U_f)|Q = r·Uhat_f[:,Q]`; evaluation uses **arbitrary field q1** similarly.
- These linear combinations are NOT guaranteed to lie in the bounded digit box A_beta. In a naive drop-in replacement of F.2's Enc with our integer RAA, V9's *restricted* distance DOES NOT justify the standard field-linear proximity/soundness argument. The prover also has not yet been forced to bind a shared canonical integer codeword across primes.
- Any future use of V9 needs a separately sound proof that the committed underlying message/rows are bound to **one canonical bounded integer vector** BEFORE applying this restricted-distance lemma; otherwise citing the binary RAA theorem for native field PCS is unsound/circular. Privacy/hiding for low-entropy digit Merkle leaves and Fiat–Shamir remain open.

### Source-form parameter sanity and independent minimal exact test

At m=1024,beta=2^20, exact maximum absolute honest difference-coded parity coefficient is bounded by

    B(m)(beta−1) = 1024·2049·1048575
                = 2200094899200 < 2^42 < 2^48.

Thus ANY source-form 49-bit p_i>2^48 satisfies no-wrap for all legal digit pairs with those m,beta. This includes V8's exceptional p_star=353581838970881; the exceptional arbitrary Fp-field vector lies outside this admitted bounded-difference domain. Source ePrint2025/286 §6 physical p29 uses 20-bit lookup-table example, but m1024 and beta=2^20 here are still **an explicitly chosen hypothetical code/lookup parameter envelope**, not a verified full paper instantiation. For m growing and fixed beta, p must grow at least quadratically for this particular sufficient bound to persist.

**EXPERIMENT EXACT:**
- Standalone deterministic `/mnt/data/vfhe_v9_bounded_digit_global_distance.py`, SHA256 `47a53d738e23f0cfa13733e9b5faed6dcf09c7b79c5beae8122a315ac3d76936`.
- JSON `/mnt/data/vfhe_v9_bounded_digit_global_distance_results.json`, SHA256 `2fc1fd4a19aa9126890a8e0309d0fe761f89393ad50a2fb95441f521b8dc4758`. LOCAL-only artifacts, not Git.
- For each of 3 independently seeded genuine π1,π2 pairs (seeds2,11,2026), take m6,beta3, no-wrap threshold 6·13·2=156. **Exhaust all 5^6−1=15624 nonzero admissible differences per seed**, total 46872 differences. Compare exact integer codeword support against reductions mod 257,263 and two 49-bit source-form primes p=281474976829441 and p=353581838970881. ALL match exactly. For each vector, divide by coefficient gcd, reduce primitive message mod2 and verify `wt_Z≥wt_F2≥binary_dmin`.
- Exact binary linear-code minimum distances for seeds2,11,2026: **4,3,3** (code length18); exact minimum Hamming weights over all bounded integer differences: **4,8,5**, respectively. These demonstrate the theorem's inequality; equality is not required. The experiment was run twice with identical SHA256 digests.
- No source-size full dmin search, performance benchmark, or new 128bit parameter was attempted.

### Decision and NEXT_ACTION

**PASS** a globally quantified, common-prime, bounded-digit-distance gate, transferred from authentic binary RAA prior art via exact integer no-wrap. **NOT** a proof of the *unrestricted full Fp code's* global minimum distance. No repaired commitment/proximity/SNARK or new cryptographic contribution has been produced.

**Next V10 (only when PI continues):** test ONE sound non-circular **binding/extraction interface** that makes original Appendix F.2's prover/committed object genuinely a *shared canonical bounded integer witness* before relying on V9's restricted-codeword distance. Cheap falsifier: does a proposed shared-Merkle column commitment plus range-constrained openings actually enforce the boundedness of UNOPENED columns against malicious CRT-lifted inconsistent prover vectors? If not, KILL that naïve interface before building any larger PCS. No more local minor-rank checks unless new reasoning requires them.

**End V9:** STATUS=PASS bounded-digit global restricted-distance theorem and exhaustive finite check; OPEN unrestricted PCS and integration; RESULT positive proof gate with exact no-wrap, binary RAA citation and F.2 obstacle; STATE_UPDATE=YES independent vFHE; global general I192 unchanged.


## 19. vFHE V10 — one shared integer Merkle root does not deterministically bind CRT digits from sampled range checks (2026-10-14)

**One primary falsifiable hypothesis:** Suppose we improve the proposed *shared canonical-integer Merkle codeword* architecture by committing to ONE integer array Y of encoded columns, using the same leaf root for all CRT native fields. Do postcommit sample openings checking honest integer leaf range alone already **force the entire unopened array** to encode a SINGLE bounded digit witness (no new proof layer) when the original Appendix F.2 linear field consistency checks pass?

**Result: FAIL for the deterministic implication.** An explicit two-prime CRT-lifted Y has ONE genuinely authenticated Merkle root and is an EXACT valid (but DIFFERENT) bounded-digit codeword in each native field, despite having invalid large integer lifts at only a few coordinates. It passes all field-linear code-consistency identities regardless of challenge; a verifier that checks the common-integer *range only on t postcommit columns* accepts precisely when it misses those bad columns, with quantifiable probability. This is a scoped attack on the NAIVE **proposed repair**, NOT on original vFHE or the actual F.2 PCS.

### Primary source anchor [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint2025/286, Appendix F.2 physical pp50–51 from Research MCP mirror (52pp, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest version VERSION_UNVERIFIED):
- F.2 commits to a FIELD matrix Uhat_f whose columns are authenticated as Merkle leaves.
- Testing verifier sends random r∈F^m; prover gives v=r·U_f; then verifier samples column set Q uniformly AFTER the encoded commitment, checks openings and Enc(v)|Q = r·Uhat_f[:,Q].
- Evaluation uses a field vector q1 and other sampled columns.
- Source F.2 does NOT introduce our new shared-integer-root/CRT canonical leaf-range check; that hypothetical auxiliary modification is ONLY OUR design target. We must not describe this example as an exploit of the published protocol.

### Smallest exact attack [DERIVATION / EXPERIMENT]

Take m=8, beta=2, length M=3m=24. Use the genuine UNWEIGHTED public integer generator G=[I_m | Repeat2 Perm1 U1 Perm2 U2] with two independent seeded permutations, seed 20261014. Two **legal Boolean digit vectors**

    a=e_6,  b=e_2,

are distinct, and E_Z(a),E_Z(b) differ in EXACTLY d=5 positions

    D={2,6,15,22,23} (0-based indices).

All honest codeword entries are nonnegative and bounded by

    H=m(2m+1)(beta−1)=8·17=136.

Select TWO different genuine SOURCE-FORM 49-bit CRT primes (original N=8192,d=4; p=4096·odd+1):

    p=281474976829441,
    q=353581838970881,

both prime, both >H, both ≡4097(mod 8192).

For EACH j in [M], set unique representative Y_j∈[0,pq) by coordinatewise CRT:

    Y_j = A_j + p·(((B_j−A_j)·p^{-1}) mod q),

where A=E_Z(a), B=E_Z(b). Then **for every coordinate**, not only sampled ones,

    Y mod p = Enc_Fp(a),
    Y mod q = Enc_Fq(b).

Consequently EVERY original-style **FIELD LINEARITY** check (including arbitrary r·U_f) passes perfectly in each component provided native underlying matrices are respectively the valid a and b. A Merkle tree over all 24 canonical pq-residues Y has ONE SHA256 root, and all 24 leaf authentication paths verify. There is no hash collision.

**Exact range criterion:** Because A_j,B_j∈[0,H] and H<min(p,q), the CRT representative Y_j∈[0,H] iff A_j=B_j. Proof: if Y_j≤H then its residues modulo p and q both equal itself, forcing A_j=B_j=Y_j; if A_j=B_j the unique [0,pq) CRT lift is the common small value. Thus

    {j:Y_j>H} = supp(E_Z(a−b)) = D,

exactly FIVE invalid (too large) leaves, with 19 valid-looking leaves. A one-root commit cannot deterministically certify ALL leaves by checking only a proper random subset.

**Postcommit sampling:** Fix the single Merkle root before Q is drawn uniformly without replacement, |Q|=t. The native field linear checks never reject; verifier rejects precisely when Q intersects D, hence

    Pr[PASS] = C(M−d,t)/C(M,t).

Exact toy probabilities:
- t1:19/24 =79.1667%
- t2:171/276=61.9565%
- t4:3876/10626=36.4766%
- t8:75582/735471=10.2767%
- t12:50388/2704156=1.86335%
- t16:969/735471=0.131752%
- t20:0.

Independently enumerate ALL 10,626 4-subsets: EXACTLY 3,876 miss all invalid leaves, matching the closed formula. If sample indexes are announced BEFORE the commitment, a cheating prover can choose bad positions outside them and the above postcommit bound does NOT apply: commit-before-random-query ordering is mandatory. This is a demonstration of a missing binding requirement, NOT a claim that all properly calibrated Merkle sampling is insecure.

### Conditional positive sampling lemma [DERIVED, NOT A PCS PROOF]

Suppose (a) the shared root is fixed before sample selection; (b) in every CRT field some mechanism INDEPENDENTLY proves/extracts an EXACT codeword encoding of a legitimate a_i∈[0,beta−1]^m; (c) canonical integer samples Y_j are range-tested in [0,H] with H<mink p_k; (d) V9 bounded-integer no-wrap holds; and (e) G has bounded-digit minimum distance at least d0 between every distinct pair of LEGAL bounded digit vectors.

For any two CRT components having a_i≠a_l, the cross-field CRT lift must violate the common integer range on at least

    d0≤wt_Z(E_Z(a_i−a_l))

coordinates (a small leaf congruent to two honest coordinates forces equality of those coordinates). Therefore the probability that t uniform postcommit openings miss ALL invalid columns is at most

    C(M−d0,t)/C(M,t) ≤ (1−d0/M)^t ≤exp(−t d0/M).

If binary RAA interleavers satisfy the classical good-distance event, V9 gives d0≥epsilon m, M=3m, so the last bound is ≤exp(−epsilon t/3), conditional on exact-codeword extraction. One could *in principle* choose t based on actual concrete epsilon, number of CRT comparisons, target 128-bit soundness, and all other failure terms.

**Major unresolved circularity:** Original F.2 tests arbitrary native-field r·U_f and q1·U_f, NOT bounded digit vectors. V9's restricted-distance lower bound does not show those arbitrary FIELD-LINEAR committed rows are close to/extractable as bounded integer codewords. Hence premises (b) and (e) as used in an operational shared PCS are NOT certified by the currently proposed scheme. Treat the conditional lemma as a design obligation, not a security theorem for the full protocol.

### Independent actual verification [EXPERIMENT]

Single reproducible local Python script

    /mnt/data/vfhe_v10_shared_merkle_crt_lift_gate.py
    SHA256 fc7de6805b5ad9ff5adecaa02aa02bfa6e7522a06161d0c105d76ff114cea9e7

Result JSON

    /mnt/data/vfhe_v10_shared_merkle_crt_lift_gate_results.json
    SHA256 19848a3da4bcba881d6b671f499ab767554c80dab06285768c2244e0413383fa

- Exhaust ALL 3^8−1=6560 nonzero bounded Boolean difference vectors for this fixed seed and find exact restricted code pair distance d=5, witness e6−e2.
- Build both genuine two-permutation/two-prefix integer codewords from scratch and recombine coordinatewise CRT into ONE integer leaf array.
- Verify all 24 Merkle leaf hash-authenticated openings against one root, and a modified leaf fails authentication.
- Verify TWO fields' exact encoding relations on ALL 24 coordinates for several arbitrary field-linear scalars.
- Find exact five invalid leaves; exhaustive t4 sampling + combinatorial t1,t2,t3,t4,t6,t8,t12,t16,t20,t24 probabilities.
- Source primes satisfy N8192,d4 CRT-congruence shape.
- This is a constructed toy attack on sampled range checking; not a statistical estimate over random real-world interleavers or an actual bit-security assessment.

### Decision and next falsifiable gate

**KILL as a deterministic assertion:** "Shared Merkle root + finite sampled range checks (by themselves) force all unopened leaves to be one canonical bounded integer codeword." One root DOES NOT imply bounded-range validity or equal CRT digit witnesses.

**KEEP as a conditional probabilistic option:** With a proven native-field exact-codeword extractor, V9 restricted distance, rigorous sampling/FS order, and enough queries, canonical leaf range samples can catch different digit vectors with probability at least 1−C(M−d0,t)/C(M,t). It may also require masking/pseudorandomization to preserve ZK of low-entropy digit data, secure leaf-size encoding (~98-bit CRT lifts vs ~49-bit honest), and cost accounting.

**V11 NEXT_ACTION only on PI continuation:** One cheapest test of a NON-CIRCULAR **field-codeword-to-integer-witness extraction** mechanism before the Merkle sampling step. Ask if a seemingly natural "use original F.2 field-linear test, then interpret the committed systematic coordinates as a bounded integer vector" actually extracts ONE vector shared across CRT fields; seek a CRT-idempotent counterexample when systematic coordinates are fieldwise different, even if all fieldwise codeword checks are perfect. This is a distinct extraction hypothesis, NOT one more sampled leaf microcase.

**End V10:** STATUS=FAIL naive deterministic global binding; PASS precise CRT-lift toy certificate & conditional sampling bound; OPEN full shared PCS and soundness/zero-knowledge; STATE_UPDATE=YES independent vFHE, global general FHE I192 unchanged.
